//
// Created by dark on 17/03/17.
//

#ifndef DESIGN3_MCU_LEDS_H
#define DESIGN3_MCU_LEDS_H

#include "stm32f4xx_gpio.h"

#define ROBOT_GREEN_LED_PIN   GPIO_Pin_4
#define ROBOT_GREEN_LED_PORT  GPIOE
#define ROBOT_GREEN_LED_CLK   RCC_AHB1Periph_GPIOE

#define ROBOT_RED_LED_PIN     GPIO_Pin_6
#define ROBOT_RED_LED_PORT    GPIOE
#define ROBOT_RED_LED_CLK     RCC_AHB1Periph_GPIOE

void init_robot_leds();

void set_robot_green_led();
void set_robot_red_led();
void reset_robot_green_led();
void reset_robot_red_led();

#endif //DESIGN3_MCU_LEDS_H
