#include <dlfcn.h>
#include <stdio.h>
#include <string.h>
#include <stddef.h>

typedef size_t (*CountFn)(void);
typedef int (*InitFn)(void);
typedef int (*UnregisterFn)(const char *);
typedef int (*InvokeFn)(const char *, const void *, size_t, void *, size_t *);

#define LOAD_FUNCTION(type, var, module, symbol) \
    type var = (type)dlsym((module), (symbol)); \
    if (!(var)) { fprintf(stderr, "missing symbol: %s\n", (symbol)); return 2; }

int main(void) {
    void *core = dlopen("build/liblevthcore.so", RTLD_NOW | RTLD_GLOBAL);
    void *setup;
    void *window;
    void *progress;
    char reply[128] = {0};
    size_t reply_size = sizeof(reply);
    if (!core) { fprintf(stderr, "%s\n", dlerror()); return 1; }
    setup = dlopen("build/liblevthsetup.so", RTLD_NOW);
    window = dlopen("build/liblevthwindow.so", RTLD_NOW);
    progress = dlopen("build/liblevthprogressbar.so", RTLD_NOW);
    if (!setup || !window || !progress) { fprintf(stderr, "%s\n", dlerror()); return 1; }

    LOAD_FUNCTION(CountFn, module_count, core, "levth_module_count");
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
        fprintf(stderr, "shared-library bridge invocation failed\n"); return 1;
    }
    if (unregister_module("setup") || unregister_module("window") ||
        unregister_module("progress") || module_count() != 0) {
        fprintf(stderr, "module unregister failed\n"); return 1;
    }
    dlclose(progress); dlclose(window); dlclose(setup); dlclose(core);
    puts("POSIX dynamic shared-library bridge: OK");
    return 0;
}
