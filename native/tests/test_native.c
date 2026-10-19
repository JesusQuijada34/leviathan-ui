#include "levth.h"
#include <assert.h>
#include <stdio.h>
#include <string.h>

static int LEVTH_CALL echo_module(const void *input, size_t input_size, void *output, size_t *output_size) {
    if (!output_size) return LEVTH_E_INVALID_ARGUMENT;
    if (!output || *output_size < input_size) { *output_size = input_size; return LEVTH_E_CAPACITY; }
    if (input_size) memcpy(output, input, input_size);
    *output_size = input_size;
    return LEVTH_OK;
}

int main(void) {
    LevthInstallOptions options = { sizeof(options), LEVTH_ABI_VERSION, 0,
        LEVTH_NOTCH_DISABLED, 0, 0, 0 };
    LevthWizardState wizard;
    LevthProgress progress;
    char module_name[] = "echo";
    LevthModuleDescriptor module = { sizeof(module), LEVTH_ABI_VERSION, module_name, 99, echo_module };
    char input[] = "ABI bridge";
    char output[32] = {0};
    size_t output_size = sizeof(output);

    assert(levth_core_abi_version() == LEVTH_ABI_VERSION);
    assert(levth_validate_install_options(&options) == LEVTH_OK);
    options.install_notch = 1;
    options.notch_style = LEVTH_NOTCH_DISABLED;
    assert(levth_validate_install_options(&options) == LEVTH_E_INVALID_ARGUMENT);
    options.notch_style = LEVTH_NOTCH_DYNAMIC_ISLAND;
    options.start_notch_at_login = 1;
    assert(levth_validate_install_options(&options) == LEVTH_OK);
    options.install_notch = 0;
    options.notch_style = LEVTH_NOTCH_DISABLED;
    options.start_notch_at_login = 0;
    options.abi_version++;
    assert(levth_validate_install_options(&options) == LEVTH_E_ABI_MISMATCH);
    options.abi_version = LEVTH_ABI_VERSION;

    levth_wizard_init(&wizard);
    assert(wizard.page_count == 4 && wizard.current_page == 0);
    assert(levth_wizard_back(&wizard) == LEVTH_E_NOT_FOUND);
    assert(levth_wizard_next(&wizard) == LEVTH_OK && wizard.current_page == 1);
    assert(levth_wizard_next(&wizard) == LEVTH_OK && wizard.current_page == 2);
    assert(levth_wizard_next(&wizard) == LEVTH_OK && wizard.current_page == 3 && wizard.completed);
    assert(levth_wizard_next(&wizard) == LEVTH_E_INVALID_ARGUMENT);

    assert(levth_progress_init(&progress, 0, 100) == LEVTH_OK);
    assert(levth_progress_set(&progress, 150) == LEVTH_OK && progress.value == 100);
    assert(levth_progress_set(&progress, -5) == LEVTH_OK && progress.value == 0);
    assert(levth_progress_set_marquee(&progress, 1) == LEVTH_OK && progress.marquee == 1);
    assert(levth_progress_init(&progress, 2, 2) == LEVTH_E_INVALID_ARGUMENT);

    assert(levth_module_register(&module) == LEVTH_OK);
    assert(levth_module_register(&module) == LEVTH_E_DUPLICATE);
    module_name[0] = 'x'; /* The core owns a copy; caller memory may go away. */
    assert(levth_module_count() == 1);
    assert(levth_bridge_invoke("echo", input, sizeof(input), output, &output_size) == LEVTH_OK);
    assert(output_size == sizeof(input) && memcmp(input, output, sizeof(input)) == 0);
    assert(levth_bridge_invoke("missing", input, sizeof(input), output, &output_size) == LEVTH_E_NOT_FOUND);
    assert(levth_module_unregister("echo") == LEVTH_OK);
    assert(levth_module_count() == 0);
    puts("native ABI tests: OK");
    return 0;
}
