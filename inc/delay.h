#ifndef _DELAY_H
#define _DELAY_H
#include "stm32f4xx_gpio.h"
#include "stm32f4xx_rcc.h"
#include "stm32f4xx_tim.h"
#include "pid.h"
#include "misc.h"

#define FREQUENCY 1000
#define SYSTICK_RELOAD SystemCoreClock/FREQUENCY
uint32_t timestamp;

void delay(uint32_t);
void udelay(uint16_t);
void initTimer(void);
#endif
