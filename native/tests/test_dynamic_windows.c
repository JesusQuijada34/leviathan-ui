#define WIN32_LEAN_AND_MEAN
#include <windows.h>
#include <stdio.h>
#include <string.h>
#include <stddef.h>

typedef size_t (__cdecl *CoreCountFn)(void);
typedef int (__cdecl *InitFn)(void);
typedef int (__cdecl *UnregisterFn)(const char *);
typedef int (__cdecl *InvokeFn)(const char *, const void *, size_t, void *, size_t *);

#define LOAD_FUNCTION(type, var, module, symbol) \
    type var = (type)GetProcAddress((module), (symbol)); \
    if (!(var)) { fprintf(stderr, "missing export: %s\n", (symbol)); return 2; }

int main(void) {
    HMODULE core = LoadLibraryW(L"build\\windows-x64\\liblevthcore.dll");
    HMODULE setup;
    HMODULE window;
    HMODULE progress;
    char reply[128] = {0};
    size_t reply_size = sizeof(reply);
    if (!core) { fprintf(stderr, "LoadLibrary(core) failed: %lu\n", GetLastError()); return 1; }
    setup = LoadLibraryW(L"build\\windows-x64\\liblevthsetup.dll");
    window = LoadLibraryW(L"build\\windows-x64\\liblevthwindow.dll");
    progress = LoadLibraryW(L"build\\windows-x64\\liblevthprogressbar.dll");
    if (!setup || !window || !progress) { fprintf(stderr, "LoadLibrary(feature DLL) failed: %lu\n", GetLastError()); return 1; }

    LOAD_FUNCTION(CoreCountFn, module_count, core, "levth_module_count");
    LOAD_FUNCTION(InvokeFn, bridge_invoke, core, "levth_bridge_invoke");
    LOAD_FUNCTION(UnregisterFn, unregister_module, core, "levth_module_unregister");
    LOAD_FUNCTION(InitFn, setup_init, setup, "levth_setup_module_initialize");
    LOAD_FUNCTION(InitFn, window_init, window, "levth_window_module_initialize");
    LOAD_FUNCTION(InitFn, progress_init, progress, "levth_progress_module_initialize");

    if (setup_init() || window_init() || progress_init() || module_count() != 3) {
        fprintf(stderr, "module registration failed\n"); return 1;
    }
    if (bridge_invoke("setup", NULL, 0, reply, &reply_size) != 0 ||
        !strstr(reply, "notch-opt-in")) {
        fprintf(stderr, "cross-DLL bridge invocation failed\n"); return 1;
    }
    if (unregister_module("setup") || unregister_module("window") ||
        unregister_module("progress") || module_count() != 0) {
        fprintf(stderr, "module unregister failed\n"); return 1;
    }
    FreeLibrary(progress);
    FreeLibrary(window);
    FreeLibrary(setup);
    FreeLibrary(core);
    puts("Windows dynamic DLL bridge: OK");
    return 0;
}
