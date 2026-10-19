#include "levth.h"
#include <string.h>
#ifdef _WIN32
#define WIN32_LEAN_AND_MEAN
#include <windows.h>
static SRWLOCK g_lock = SRWLOCK_INIT;
#define lock_registry() AcquireSRWLockExclusive(&g_lock)
#define unlock_registry() ReleaseSRWLockExclusive(&g_lock)
#else
#include <stdatomic.h>
static atomic_flag g_lock = ATOMIC_FLAG_INIT;
#define lock_registry() while (atomic_flag_test_and_set_explicit(&g_lock, memory_order_acquire)) { }
#define unlock_registry() atomic_flag_clear_explicit(&g_lock, memory_order_release)
#endif

#define MODULE_CAPACITY 64u
typedef struct RegistryEntry {
    char name[LEVTH_MAX_MODULE_NAME + 1u];
    uint32_t module_id;
    LevthBridgeCallback invoke;
} RegistryEntry;
static RegistryEntry g_modules[MODULE_CAPACITY];
static size_t g_module_count = 0;

static int valid_name(const char *name) {
    size_t n = 0;
    if (!name || !name[0]) return 0;
    for (; name[n]; ++n) {
        const char c = name[n];
        if (n >= LEVTH_MAX_MODULE_NAME) return 0;
        if (!((c >= 'a' && c <= 'z') || (c >= '0' && c <= '9') || c == '_')) return 0;
    }
    return 1;
}

uint32_t LEVTH_CALL levth_core_abi_version(void) { return LEVTH_ABI_VERSION; }
const char * LEVTH_CALL levth_core_version(void) { return "1.0.5"; }

const char * LEVTH_CALL levth_status_string(int status) {
    switch (status) {
        case LEVTH_OK: return "success";
        case LEVTH_E_INVALID_ARGUMENT: return "invalid argument";
        case LEVTH_E_ABI_MISMATCH: return "ABI version mismatch";
        case LEVTH_E_NOT_FOUND: return "module not found";
        case LEVTH_E_DUPLICATE: return "module already registered";
        case LEVTH_E_CAPACITY: return "module registry full";
        case LEVTH_E_UNSUPPORTED: return "operation unsupported on this platform";
        case LEVTH_E_SYSTEM: return "operating system error";
        default: return "unknown status";
    }
}

int LEVTH_CALL levth_module_register(const LevthModuleDescriptor *module) {
    size_t i;
    if (!module || module->struct_size < sizeof(*module) || !valid_name(module->name) || !module->invoke)
        return LEVTH_E_INVALID_ARGUMENT;
    if (module->abi_version != LEVTH_ABI_VERSION) return LEVTH_E_ABI_MISMATCH;
    lock_registry();
    for (i = 0; i < g_module_count; ++i) {
        if (strcmp(g_modules[i].name, module->name) == 0) {
            unlock_registry();
            return LEVTH_E_DUPLICATE;
        }
    }
    if (g_module_count == MODULE_CAPACITY) {
        unlock_registry();
        return LEVTH_E_CAPACITY;
    }
    strcpy(g_modules[g_module_count].name, module->name);
    g_modules[g_module_count].module_id = module->module_id;
    g_modules[g_module_count].invoke = module->invoke;
    ++g_module_count;
    unlock_registry();
    return LEVTH_OK;
}

int LEVTH_CALL levth_module_unregister(const char *name) {
    size_t i;
    if (!valid_name(name)) return LEVTH_E_INVALID_ARGUMENT;
    lock_registry();
    for (i = 0; i < g_module_count; ++i) {
        if (strcmp(g_modules[i].name, name) == 0) {
            if (i + 1 < g_module_count)
            memmove(&g_modules[i], &g_modules[i + 1], (g_module_count - i - 1) * sizeof(g_modules[0]));
            --g_module_count;
            unlock_registry();
            return LEVTH_OK;
        }
    }
    unlock_registry();
    return LEVTH_E_NOT_FOUND;
}

int LEVTH_CALL levth_bridge_invoke(const char *name, const void *input, size_t input_size,
                                   void *output, size_t *output_size) {
    size_t i;
    LevthBridgeCallback callback = NULL;
    if (!valid_name(name) || (!input && input_size != 0) || !output_size)
        return LEVTH_E_INVALID_ARGUMENT;
    lock_registry();
    for (i = 0; i < g_module_count; ++i) {
        if (strcmp(g_modules[i].name, name) == 0) {
            callback = g_modules[i].invoke;
            break;
        }
    }
    unlock_registry();
    if (!callback) return LEVTH_E_NOT_FOUND;
    return callback(input, input_size, output, output_size);
}

size_t LEVTH_CALL levth_module_count(void) {
    size_t count;
    lock_registry();
    count = g_module_count;
    unlock_registry();
    return count;
}
