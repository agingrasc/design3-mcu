#ifndef _DELAY_H
#define _DELAY_H

#include "stm32f4xx_gpio.h"
#include "stm32f4xx_rcc.h"
#include "stm32f4xx_tim.h"
#include "pid.h"
#include "misc.h"

#define FREQUENCY 1000
#define SYSTICK_RELOAD SystemCoreClock/FREQUENCY
#define TIM9_IRQn 24
uint32_t timestamp;

void initDelay(void);
void initTimer(void);

void delay(uint32_t);
void udelay(uint16_t);

#endif
