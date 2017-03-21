#include "stm32f4_discovery.h"
#include "stm32f4xx_gpio.h"
#include "stm32f4xx_rcc.h"

#define GREEN  LED4_PIN
#define ORANGE LED3_PIN
#define RED    LED5_PIN
#define BLUE   LED6_PIN
#define ALL_LEDS (GREEN | ORANGE | RED | BLUE) // all leds

#define LEDS_GPIO_PORT (GPIOD)
#define BTN_GPIO_PORT (GPIOD)

#define STATE_CHANGE_DELAY 42000

static uint32_t state_change_accumulator = 0;

enum button_state {
    UP,
    TRANSITION_DOWN,
    DOWN,
    TRANSITION_UP
};

enum button_state current_button_state = UP;

uint8_t current_led_state = 1;

GPIO_InitTypeDef GPIO_InitStructure;
GPIO_InitTypeDef GPIO_Btn_InitStructure;

static void state_hold_up() {
    if (GPIO_ReadInputDataBit(GPIOA, GPIO_Pin_0) == 1) {
        state_change_accumulator = 0;
        current_button_state = TRANSITION_DOWN;
    }
}


static void state_transition_to_down() {
    state_change_accumulator += 1;
    if (state_change_accumulator >= STATE_CHANGE_DELAY) {
        current_button_state = DOWN;
        current_led_state = !current_led_state;
    }
}

static void state_hold_down() {
    if (GPIO_ReadInputDataBit(GPIOA, GPIO_Pin_0)) {
        state_change_accumulator = 0;
        current_button_state = TRANSITION_UP;
    }
}

static void state_transition_to_up() {
    if (GPIO_ReadInputDataBit(GPIOA, GPIO_Pin_0) == 0) {
        state_change_accumulator += 1;
    } else {
        state_change_accumulator = 0;
    }
    if (state_change_accumulator >= STATE_CHANGE_DELAY) {
        current_button_state = UP;
    }
}

static void setup(void) {
    RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOA, ENABLE);
    RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOD, ENABLE);

    GPIO_InitStructure.GPIO_Pin = ALL_LEDS;
    GPIO_Btn_InitStructure.GPIO_Pin = GPIO_Pin_0;

    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_OUT;
    GPIO_Btn_InitStructure.GPIO_Mode = GPIO_Mode_IN;

    GPIO_InitStructure.GPIO_Speed = GPIO_Speed_100MHz;
    GPIO_Btn_InitStructure.GPIO_Speed = GPIO_Speed_100MHz;

    GPIO_InitStructure.GPIO_OType = GPIO_OType_PP;
    GPIO_Btn_InitStructure.GPIO_OType = GPIO_OType_PP;

    GPIO_InitStructure.GPIO_PuPd = GPIO_PuPd_NOPULL;
    GPIO_Btn_InitStructure.GPIO_PuPd = GPIO_PuPd_NOPULL;

    GPIO_Init(LEDS_GPIO_PORT, &GPIO_InitStructure);
    GPIO_Init(GPIOA, &GPIO_Btn_InitStructure);

    GPIO_ResetBits(LEDS_GPIO_PORT, ALL_LEDS);
}

int main(void) {
    setup();
    while (1) {
        if (current_led_state) {
            GPIO_SetBits(LEDS_GPIO_PORT, ALL_LEDS);
        } else {
            GPIO_ResetBits(LEDS_GPIO_PORT, ALL_LEDS);
        }


        switch (current_button_state) {
            case UP:
                state_hold_up();
                break;
            case TRANSITION_DOWN:
                state_transition_to_down();
                break;
            case DOWN:
                state_hold_down();
                break;
            case TRANSITION_UP:
                state_transition_to_up();
                break;
            default:
                break;
        }

    }

    return 0; // never returns actually
}