// main.h

#ifndef _MAIN_H_
#define _MAIN_H_

#include "stm32f4xx_tim.h"
#include "stm32f4xx_rcc.h"
#include "stm32f4xx_gpio.h"
#include "CommandHandler.h"
#include "MotorController.h"
#include "MotorEncoder.h"
#include "LCD.h"
#include "uart.h"
#include "pid.h"
#include "delay.h"
#include "motor.h"
#include "defines.h"
#include "tm_stm32f4_usb_vcp.h"
#include "defines.h"

#ifdef ID_MODE
#include "id.h"
#endif

int main(void);

#endif
