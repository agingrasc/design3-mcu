//
// Created by dark on 17/03/17.
//

#include "leds.h"

void init_robot_leds() {
    // Enable clock peripherals
    RCC_AHB1PeriphClockCmd(ROBOT_GREEN_LED_CLK, ENABLE);
    RCC_AHB1PeriphClockCmd(ROBOT_RED_LED_CLK, ENABLE);

    // Set pins as output, pull up
    GPIO_InitTypeDef GPIO_InitStructure;

    GPIO_StructInit(&GPIO_InitStructure);
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_OUT;
    GPIO_InitStructure.GPIO_PuPd = GPIO_PuPd_UP;
    GPIO_InitStructure.GPIO_Pin = ROBOT_GREEN_LED_PIN;

    GPIO_Init(ROBOT_GREEN_LED_PORT, &GPIO_InitStructure);

    GPIO_InitStructure.GPIO_Pin = ROBOT_RED_LED_PIN;
    GPIO_Init(ROBOT_RED_LED_PORT, &GPIO_InitStructure);
}

void _set_robot_led(GPIO_TypeDef *port, uint32_t pin) {
    GPIO_SetBits(port, pin);
}

void _reset_robot_led(GPIO_TypeDef *port, uint32_t pin) {
    GPIO_ResetBits(port, pin);
}

void set_robot_green_led() {
    _set_robot_led(ROBOT_GREEN_LED_PORT, ROBOT_GREEN_LED_PIN);
}

void set_robot_red_led() {
    _set_robot_led(ROBOT_RED_LED_PORT, ROBOT_RED_LED_PIN);
}

void reset_robot_green_led() {
    _reset_robot_led(ROBOT_GREEN_LED_PORT, ROBOT_GREEN_LED_PIN);
}

void reset_robot_red_led() {
    _reset_robot_led(ROBOT_RED_LED_PORT, ROBOT_RED_LED_PIN);
}
