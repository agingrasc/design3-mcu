// CommandHandler.h

#ifndef _COMMANDHANDLER_H_
#define _COMMANDHNADLER_H_

//#include "stm32f4_discovery.h"
#include "stm32f4xx_rcc.h"
#include "stm32f4xx_gpio.h"
#include "uart.h"
#include "delay.h"
#include "MotorController.h"
#include "MotorEncoder.h"
#include "motor.h"

#define LED_PIN_UART    GPIO_Pin_16
#define LED_PORT_UART   GPIOD
#define LED_UART_ON     GPIO_SetBits(LED_PORT_UART, LED_PIN_UART)
#define LED_UART_OFF    GPIO_ResetBits(LED_PORT_UART, LED_PIN_UART) 

int PID_mode;
uint8_t current_motor;

void cmdHandlerInit(void);
int handleCmd(uint32_t);
int checkSumCmd(uint32_t);
int switchCmd(uint32_t);

uint32_t getInstruction(uint32_t);
uint32_t getParam(uint32_t);
uint32_t getCheck(uint32_t);

#endif
