/*
 * Maintained-fork installed-library contract.
 *
 * GNU lightning is free software; you can redistribute it and/or modify it
 * under the terms of the GNU Lesser General Public License as published by
 * the Free Software Foundation; either version 3, or (at your option) any
 * later version.
 */

#include <lightning.h>

typedef int (*answer_function_t)(void);

static jit_state_t *_jit;

int main(int argc, char **argv) {
    answer_function_t answer;
    int result;

    if (argc < 1) {
        return 2;
    }
    init_jit(argv[0]);
    _jit = jit_new_state();
    if (_jit == NULL) {
        finish_jit();
        return 3;
    }

    jit_prolog();
    jit_movi(JIT_R0, 42);
    jit_retr(JIT_R0);
    answer = jit_emit();
    if (answer == NULL) {
        jit_destroy_state();
        finish_jit();
        return 4;
    }

    jit_clear_state();
    result = answer();
    jit_destroy_state();
    finish_jit();
    return result == 42 ? 0 : 5;
}
