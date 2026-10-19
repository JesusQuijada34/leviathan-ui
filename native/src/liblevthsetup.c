#include "levth.h"
#include <string.h>

static int LEVTH_CALL setup_bridge(const void *input, size_t input_size, void *output, size_t *output_size) {
    static const char capability[] = "wizard-v1;notch-opt-in;island;cutout;user-path-opt-in";
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

int LEVTH_CALL levth_validate_install_options(const LevthInstallOptions *options) {
    if (!options || options->struct_size < sizeof(*options)) return LEVTH_E_INVALID_ARGUMENT;
    if (options->abi_version != LEVTH_ABI_VERSION) return LEVTH_E_ABI_MISMATCH;
    if (options->install_notch > 1 || options->install_bridge_services > 1 ||
        options->add_user_path > 1 || options->start_notch_at_login > 1)
        return LEVTH_E_INVALID_ARGUMENT;
    if (options->install_notch) {
        if (options->notch_style != LEVTH_NOTCH_DYNAMIC_ISLAND &&
            options->notch_style != LEVTH_NOTCH_FULL_CUTOUT)
            return LEVTH_E_INVALID_ARGUMENT;
    } else if (options->notch_style != LEVTH_NOTCH_DISABLED || options->start_notch_at_login) {
        return LEVTH_E_INVALID_ARGUMENT;
    }
    return LEVTH_OK;
}

void LEVTH_CALL levth_wizard_init(LevthWizardState *state) {
    if (!state) return;
    state->current_page = 0;
    state->page_count = 4;
    state->can_go_back = 0;
    state->can_go_forward = 1;
    state->completed = 0;
}

int LEVTH_CALL levth_wizard_next(LevthWizardState *state) {
    if (!state || state->page_count < 2 || state->current_page >= state->page_count)
        return LEVTH_E_INVALID_ARGUMENT;
    if (state->completed) return LEVTH_E_INVALID_ARGUMENT;
    if (state->current_page + 1 >= state->page_count) return LEVTH_E_NOT_FOUND;
    ++state->current_page;
    state->can_go_back = 1;
    state->can_go_forward = state->current_page + 1 < state->page_count;
    if (!state->can_go_forward) state->completed = 1;
    return LEVTH_OK;
}

int LEVTH_CALL levth_wizard_back(LevthWizardState *state) {
    if (!state || state->page_count < 2 || state->current_page >= state->page_count)
        return LEVTH_E_INVALID_ARGUMENT;
    if (state->current_page == 0 || state->completed) return LEVTH_E_NOT_FOUND;
    --state->current_page;
    state->can_go_back = state->current_page != 0;
    state->can_go_forward = 1;
    return LEVTH_OK;
}

int LEVTH_CALL levth_setup_module_initialize(void) {
    static const LevthModuleDescriptor descriptor = {
        sizeof(LevthModuleDescriptor), LEVTH_ABI_VERSION, "setup", LEVTH_MODULE_SETUP, setup_bridge
    };
    return levth_module_register(&descriptor);
}
