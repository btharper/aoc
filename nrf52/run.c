#include "run.h"
#include "nrfx_nrf52833.h"

#define BTN_A (1 << 14)
#define BTN_B (1 << 23)
#define ROW1 (1 << 21)
#define ROW2 (1 << 22)
#define ROW3 (1 << 15)
#define ROW4 (1 << 24)
#define ROW5 (1 << 19)
#define COL1 (1 << 28)
#define COL2 (1 << 11)
#define COL3 (1 << 31)
#define COL4 (1 <<  5)
#define COL5 (1 << 30)

#define GPIO_P0_ROWS (ROW1|ROW2|ROW3|ROW4|ROW5)
#define GPIO_P0_COLS (COL1|COL2|COL3|COL5)
#define GPIO_P1_ROWS (0)
#define GPIO_P1_COLS (COL4)

uint32_t get_rand(void) {
    uint32_t rand;

    while (NRF_RNG->EVENTS_VALRDY == 0);
    rand = NRF_RNG->VALUE;
    NRF_RNG->EVENTS_VALRDY = 0;

    return rand;
}

void run(void) {
    int i;
    //int j;
    //uint32_t set;
    //uint32_t clr;
    uint32_t a_pressed;
    uint32_t b_pressed;

    //uint32_t rand;

    NRF_RNG->CONFIG = 1;
    NRF_RNG->TASKS_START = 1;

    NRF_P0->DIR = (GPIO_P0_ROWS | GPIO_P0_COLS);
    NRF_P1->DIR = (GPIO_P1_ROWS | GPIO_P1_COLS);
    NRF_P0->PIN_CNF[14] = 0;
    NRF_P0->PIN_CNF[23] = 0;

    NRF_P0->OUT = GPIO_P0_ROWS;
    if (get_rand() % 2 == 0) {
        NRF_P0->OUTCLR = ROW1;
    }

    //a_pressed = (NRF_P0->IN & BTN_A);
    //b_pressed = (NRF_P0->IN & BTN_B);
    do {
        a_pressed = NRF_P0->IN | GPIO_P0_ROWS | GPIO_P0_COLS;
        b_pressed = NRF_P1->IN | GPIO_P1_ROWS | GPIO_P1_COLS;
        NRF_P0->OUTCLR = ROW2|ROW4;
        for (i = 0; i < 8333; i++) {
            // 120us per call (debiased RNG), ~1s
            NRF_RADIO->BASE0 = get_rand();
        }
        NRF_P0->OUTSET = ROW2|ROW4;
        for (i = 0; i < 8333; i++) {
            // 120us per call (debiased RNG), ~1s
            NRF_RADIO->BASE0 = get_rand();
        }
    } while (a_pressed == (NRF_P0->IN | GPIO_P0_ROWS | GPIO_P0_COLS) &&
             b_pressed == (NRF_P1->IN | GPIO_P1_ROWS | GPIO_P1_COLS)
            );

    while(1) {
        /*
        for (j = 0; j < 8000; j++) {
            for (i = 0; i < 8000; i++) {
                NRF_P0->OUT ^= (COL3|ROW3);
            }
            NRF_P0->OUT ^= (ROW1|ROW5|COL1|COL5);
        }
        NRF_P0->OUT ^= (ROW2|ROW4|COL2);
        NRF_P1->OUT ^= (COL4);
        */
        /*
        for (i = 0; i < (1 << 16); i++) {
            set = 0;
            clr = 0;
            //if (i % 255 < 255) { set |= ROW1;} else {clr |= ROW1;}
            if (i % 255 < 142) { set |= ROW2;} else {clr |= ROW2;}
            if (i % 255 <  68) { set |= ROW3;} else {clr |= ROW3;}
            if (i % 255 <  25) { set |= ROW4;} else {clr |= ROW4;}
            if (i % 255 <   5) { set |= ROW5;} else {clr |= ROW5;}
            if (NRF_P0->IN & BTN_A) { set |= ROW1;clr|=COL1; } else {set|=COL1;clr |= ROW1;}
            //if (NRF_P0->IN & BTN_B) { set |= ROW5|COL5; } else {clr |= ROW5|COL5;}
            NRF_P0->OUTSET = set;
            NRF_P0->OUTCLR = clr;
        }
        */
        if (NRF_P0->IN & BTN_A) {
            NRF_P0->OUTCLR = ROW1;
        } else {
            NRF_P0->OUTSET = ROW1;
        }
        if (NRF_P0->IN & BTN_B) {
            NRF_P0->OUTCLR = ROW5;
        } else {
            NRF_P0->OUTSET = ROW5;
        }
    }
}

void irq_trap(void) {
    NRF_P0->DIR = 0xFFFFFFFF;
    NRF_P1->DIR = 0xFFFFFFFF;
    NRF_P0->OUTSET = (COL1|ROW1|ROW5|COL5);
    NRF_P0->OUTCLR = (COL2|ROW2|ROW4);
    NRF_P1->OUTSET = (0);
    NRF_P1->OUTCLR = (COL4);
    while (1) {
        NRF_P0->OUT ^= (COL3|ROW3);
    }
}
