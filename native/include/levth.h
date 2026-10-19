#ifndef LEVTH_H
#define LEVTH_H

#include <stddef.h>
#include <stdint.h>

#if defined(_WIN32)
  #if defined(LEVTH_CORE_BUILD)
    #define LEVTH_API __declspec(dllexport)
  #else
    #define LEVTH_API __declspec(dllimport)
  #endif
  #if defined(LEVTH_MODULE_BUILD)
    #define LEVTH_MODULE_API __declspec(dllexport)
  #else
    #define LEVTH_MODULE_API __declspec(dllimport)
  #endif
  #define LEVTH_CALL __cdecl
#else
  #if defined(LEVTH_CORE_BUILD) || defined(LEVTH_MODULE_BUILD)
    #define LEVTH_API __attribute__((visibility("default")))
    #define LEVTH_MODULE_API __attribute__((visibility("default")))
  #else
    #define LEVTH_API
    #define LEVTH_MODULE_API
  #endif
  #define LEVTH_CALL
#endif

#ifdef __cplusplus
extern "C" {
#endif

#define LEVTH_ABI_VERSION 0x00010000u
#define LEVTH_MAX_MODULE_NAME 63u
#define LEVTH_MAX_ERROR 255u

typedef enum LevthStatus {
    LEVTH_OK = 0,
    LEVTH_E_INVALID_ARGUMENT = 1,
    LEVTH_E_ABI_MISMATCH = 2,
    LEVTH_E_NOT_FOUND = 3,
    LEVTH_E_DUPLICATE = 4,
    LEVTH_E_CAPACITY = 5,
    LEVTH_E_UNSUPPORTED = 6,
    LEVTH_E_SYSTEM = 7
} LevthStatus;

typedef enum LevthModuleId {
    LEVTH_MODULE_CORE = 0,
    LEVTH_MODULE_WINDOW = 1,
    LEVTH_MODULE_SPLASH = 2,
    LEVTH_MODULE_TITLE_BAR = 3,
    LEVTH_MODULE_DIALOGS = 4,
    LEVTH_MODULE_PROGRESS = 5,
    LEVTH_MODULE_TOUCH = 6,
    LEVTH_MODULE_NOTCH = 7,
    LEVTH_MODULE_SETUP = 8
} LevthModuleId;

typedef enum LevthNotchStyle {
    LEVTH_NOTCH_DISABLED = 0,
    LEVTH_NOTCH_DYNAMIC_ISLAND = 1,
    LEVTH_NOTCH_FULL_CUTOUT = 2
} LevthNotchStyle;

typedef enum LevthWindowEffect {
    LEVTH_EFFECT_POLISHED = 0,
    LEVTH_EFFECT_GHOST = 1,
    LEVTH_EFFECT_GHOST_BLUR = 2,
    LEVTH_EFFECT_MICA = 3
} LevthWindowEffect;

typedef struct LevthInstallOptions {
    uint32_t struct_size;
    uint32_t abi_version;
    uint32_t install_notch;
    uint32_t notch_style;
    uint32_t install_bridge_services;
    uint32_t add_user_path;
    uint32_t start_notch_at_login;
} LevthInstallOptions;

typedef struct LevthModuleInfo {
    uint32_t struct_size;
    uint32_t abi_version;
    uint32_t module_id;
    const char *name;
    const char *version;
} LevthModuleInfo;

typedef struct LevthProgress {
    int minimum;
    int maximum;
    int value;
    uint32_t marquee;
} LevthProgress;

typedef struct LevthWizardState {
    uint32_t current_page;
    uint32_t page_count;
    uint32_t can_go_back;
    uint32_t can_go_forward;
    uint32_t completed;
} LevthWizardState;

typedef int (LEVTH_CALL *LevthBridgeCallback)(const void *input, size_t input_size,
                                               void *output, size_t *output_size);
typedef struct LevthModuleDescriptor {
    uint32_t struct_size;
    uint32_t abi_version;
    const char *name;
    uint32_t module_id;
    LevthBridgeCallback invoke;
} LevthModuleDescriptor;

/* Core exports form the stable bridge used by every feature DLL and FFI binding. */
/* Unregister a module and quiesce its callbacks before FreeLibrary on Windows. */
LEVTH_API uint32_t LEVTH_CALL levth_core_abi_version(void);
LEVTH_API const char * LEVTH_CALL levth_core_version(void);
LEVTH_API const char * LEVTH_CALL levth_status_string(int status);
LEVTH_API int LEVTH_CALL levth_module_register(const LevthModuleDescriptor *module);
LEVTH_API int LEVTH_CALL levth_module_unregister(const char *name);
LEVTH_API int LEVTH_CALL levth_bridge_invoke(const char *name, const void *input,
                                              size_t input_size, void *output,
                                              size_t *output_size);
LEVTH_API size_t LEVTH_CALL levth_module_count(void);

/* Installer/wizard configuration model, exported by liblevthsetup.dll. */
LEVTH_MODULE_API int LEVTH_CALL levth_validate_install_options(const LevthInstallOptions *options);
LEVTH_MODULE_API void LEVTH_CALL levth_wizard_init(LevthWizardState *state);
LEVTH_MODULE_API int LEVTH_CALL levth_wizard_next(LevthWizardState *state);
LEVTH_MODULE_API int LEVTH_CALL levth_wizard_back(LevthWizardState *state);
LEVTH_MODULE_API int LEVTH_CALL levth_setup_module_initialize(void);

/* These functions take HWND handles on Windows; values are opaque to FFI callers. */
LEVTH_MODULE_API int LEVTH_CALL levth_window_apply_effect(void *window_handle,
                                                          LevthWindowEffect effect,
                                                          uint32_t corner_radius);
LEVTH_MODULE_API int LEVTH_CALL levth_window_module_initialize(void);
LEVTH_MODULE_API int LEVTH_CALL levth_progress_init(LevthProgress *progress, int minimum, int maximum);
LEVTH_MODULE_API int LEVTH_CALL levth_progress_set(LevthProgress *progress, int value);
LEVTH_MODULE_API int LEVTH_CALL levth_progress_set_marquee(LevthProgress *progress, uint32_t enabled);
LEVTH_MODULE_API int LEVTH_CALL levth_progress_module_initialize(void);

#ifdef __cplusplus
}
#endif
#endif
