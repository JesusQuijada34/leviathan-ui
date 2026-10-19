#include "levth.h"
#include <string.h>

static int LEVTH_CALL progress_bridge(const void *input, size_t input_size, void *output, size_t *output_size) {
    static const char capability[] = "bounded-progress;determinate;marquee-state";
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

int LEVTH_CALL levth_progress_init(LevthProgress *progress, int minimum, int maximum) {
    if (!progress || maximum <= minimum) return LEVTH_E_INVALID_ARGUMENT;
    progress->minimum = minimum;
    progress->maximum = maximum;
    progress->value = minimum;
    progress->marquee = 0;
    return LEVTH_OK;
}

int LEVTH_CALL levth_progress_set(LevthProgress *progress, int value) {
    if (!progress || progress->maximum <= progress->minimum) return LEVTH_E_INVALID_ARGUMENT;
    if (value < progress->minimum) value = progress->minimum;
    if (value > progress->maximum) value = progress->maximum;
    progress->value = value;
    return LEVTH_OK;
}

int LEVTH_CALL levth_progress_set_marquee(LevthProgress *progress, uint32_t enabled) {
    if (!progress || enabled > 1) return LEVTH_E_INVALID_ARGUMENT;
    progress->marquee = enabled;
    return LEVTH_OK;
}

int LEVTH_CALL levth_progress_module_initialize(void) {
    static const LevthModuleDescriptor descriptor = {
        sizeof(LevthModuleDescriptor), LEVTH_ABI_VERSION, "progress", LEVTH_MODULE_PROGRESS, progress_bridge
    };
    return levth_module_register(&descriptor);
}
