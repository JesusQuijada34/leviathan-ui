#include "levth.h"
#include <string.h>
#ifdef _WIN32
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <dwmapi.h>
#pragma comment(lib, "dwmapi.lib")
#endif

static int LEVTH_CALL window_bridge(const void *input, size_t input_size, void *output, size_t *output_size) {
    static const char capability[] = "win32-hwnd;dwm-rounded;mica;acrylic;layered-ghost";
    (void)input;
    if (input_size != 0 || !output_size) return LEVTH_E_INVALID_ARGUMENT;
    if (!output || *output_size < sizeof(capability)) {
        *output_size = sizeof(capability);
        return LEVTH_E_CAPACITY;
    }
    memcpy(output, capability, sizeof(capability));
    *output_size = sizeof(capability);
    return LEVTH_OK;
}

int LEVTH_CALL levth_window_apply_effect(void *window_handle, LevthWindowEffect effect,
                                         uint32_t corner_radius) {
#ifdef _WIN32
    HWND hwnd = (HWND)window_handle;
    HRESULT hr = S_OK;
    DWORD preference;
    int backdrop;
    (void)corner_radius; /* Windows exposes a corner preference, not a pixel radius. */
    if (!hwnd || !IsWindow(hwnd) || effect < LEVTH_EFFECT_POLISHED || effect > LEVTH_EFFECT_MICA)
        return LEVTH_E_INVALID_ARGUMENT;
    if (effect == LEVTH_EFFECT_POLISHED) {
        preference = 2; /* DWMWCP_ROUND */
        hr = DwmSetWindowAttribute(hwnd, 33, &preference, sizeof(preference));
    } else if (effect == LEVTH_EFFECT_MICA || effect == LEVTH_EFFECT_GHOST_BLUR) {
        backdrop = effect == LEVTH_EFFECT_MICA ? 2 : 3; /* Mica / Acrylic */
        hr = DwmSetWindowAttribute(hwnd, 38, &backdrop, sizeof(backdrop));
    } else {
        LONG_PTR style = GetWindowLongPtrW(hwnd, GWL_EXSTYLE);
        SetLastError(0);
        if (!(style & WS_EX_LAYERED)) {
            SetLastError(0);
            (void)SetWindowLongPtrW(hwnd, GWL_EXSTYLE, style | WS_EX_LAYERED);
            if (GetLastError() != 0) return LEVTH_E_SYSTEM;
        }
        if (!SetLayeredWindowAttributes(hwnd, 0, 1, LWA_ALPHA)) return LEVTH_E_SYSTEM;
    }
    return SUCCEEDED(hr) ? LEVTH_OK : LEVTH_E_UNSUPPORTED;
#else
    (void)window_handle; (void)effect; (void)corner_radius;
    return LEVTH_E_UNSUPPORTED;
#endif
}

int LEVTH_CALL levth_window_module_initialize(void) {
    static const LevthModuleDescriptor descriptor = {
        sizeof(LevthModuleDescriptor), LEVTH_ABI_VERSION, "window", LEVTH_MODULE_WINDOW, window_bridge
    };
    return levth_module_register(&descriptor);
}
