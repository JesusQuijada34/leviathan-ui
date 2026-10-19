CC ?= cc
CFLAGS ?= -O2 -Wall -Wextra -Werror -std=c11
CPPFLAGS += -Iinclude
BUILD := build
CORE := $(BUILD)/liblevthcore.o
SETUP := $(BUILD)/liblevthsetup.o
PROGRESS := $(BUILD)/liblevthprogressbar.o
WINDOW := $(BUILD)/liblevthwindow.o

.PHONY: all test test-dynamic clean
all: test

$(BUILD):
	mkdir -p $(BUILD)

$(CORE): src/liblevthcore.c include/levth.h | $(BUILD)
	$(CC) $(CPPFLAGS) $(CFLAGS) -DLEVTH_CORE_BUILD -c $< -o $@

$(SETUP): src/liblevthsetup.c include/levth.h | $(BUILD)
	$(CC) $(CPPFLAGS) $(CFLAGS) -DLEVTH_MODULE_BUILD -c $< -o $@

$(PROGRESS): src/liblevthprogressbar.c include/levth.h | $(BUILD)
	$(CC) $(CPPFLAGS) $(CFLAGS) -DLEVTH_MODULE_BUILD -c $< -o $@

$(WINDOW): src/liblevthwindow.c include/levth.h | $(BUILD)
	$(CC) $(CPPFLAGS) $(CFLAGS) -DLEVTH_MODULE_BUILD -c $< -o $@

test: $(CORE) $(SETUP) $(PROGRESS) $(WINDOW) tests/test_native.c
	$(CC) $(CPPFLAGS) $(CFLAGS) -DLEVTH_CORE_BUILD -DLEVTH_MODULE_BUILD tests/test_native.c $(CORE) $(SETUP) $(PROGRESS) $(WINDOW) -o $(BUILD)/test_native
	$(BUILD)/test_native

$(BUILD)/liblevthcore.so: src/liblevthcore.c include/levth.h | $(BUILD)
	$(CC) $(CPPFLAGS) $(CFLAGS) -fPIC -DLEVTH_CORE_BUILD -shared $< -o $@

$(BUILD)/liblevthsetup.so: src/liblevthsetup.c include/levth.h $(BUILD)/liblevthcore.so
	$(CC) $(CPPFLAGS) $(CFLAGS) -fPIC -DLEVTH_MODULE_BUILD -shared $< $(BUILD)/liblevthcore.so -Wl,-rpath,'$$ORIGIN' -o $@

$(BUILD)/liblevthprogressbar.so: src/liblevthprogressbar.c include/levth.h $(BUILD)/liblevthcore.so
	$(CC) $(CPPFLAGS) $(CFLAGS) -fPIC -DLEVTH_MODULE_BUILD -shared $< $(BUILD)/liblevthcore.so -Wl,-rpath,'$$ORIGIN' -o $@

$(BUILD)/liblevthwindow.so: src/liblevthwindow.c include/levth.h $(BUILD)/liblevthcore.so
	$(CC) $(CPPFLAGS) $(CFLAGS) -fPIC -DLEVTH_MODULE_BUILD -shared $< $(BUILD)/liblevthcore.so -Wl,-rpath,'$$ORIGIN' -o $@

test-dynamic: $(BUILD)/liblevthcore.so $(BUILD)/liblevthsetup.so $(BUILD)/liblevthprogressbar.so $(BUILD)/liblevthwindow.so tests/test_dynamic_posix.c
	$(CC) $(CFLAGS) tests/test_dynamic_posix.c -ldl -o $(BUILD)/test_dynamic_posix
	$(BUILD)/test_dynamic_posix

test: test-dynamic

clean:
	rm -rf $(BUILD)
