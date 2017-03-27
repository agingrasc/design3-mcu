// MotorEncoder.h

#ifndef _MOTOR_ENCODER_H_

#include "stm32f4xx_tim.h"
#include "stm32f4xx_rcc.h"
#include "stm32f4xx_gpio.h"
#include "delay.h"
#include "motor.h"
#include "defines.h"

// Init encoders channels
// OK, after some ditching.... MOTOR 1
#define MA_TIMER            TIM5
#define MA_TIMER_CLK        RCC_APB1Periph_TIM5
#define MA_ENCA_PIN            GPIO_Pin_0
#define MA_ENCA_GPIO_PORT    GPIOA
#define MA_ENCA_GPIO_CLK    RCC_AHB1Periph_GPIOA
#define MA_ENCA_SOURCE        GPIO_PinSource0
#define MA_ENCA_AF            GPIO_AF_TIM5
#define MA_ENCB_PIN            GPIO_Pin_1
#define MA_ENCB_GPIO_PORT    GPIOA
#define MA_ENCB_GPIO_CLK    RCC_AHB1Periph_GPIOA
#define MA_ENCB_SOURCE        GPIO_PinSource1
#define MA_ENCB_AF            GPIO_AF_TIM5

// OK MOTOR 2
#define MB_TIMER            TIM4
#define MB_TIMER_CLK        RCC_APB1Periph_TIM4
#define MB_ENCA_PIN            GPIO_Pin_13
#define MB_ENCA_GPIO_PORT    GPIOD
#define MB_ENCA_GPIO_CLK    RCC_AHB1Periph_GPIOD
#define MB_ENCA_SOURCE        GPIO_PinSource13
#define MB_ENCA_AF            GPIO_AF_TIM4
#define MB_ENCB_PIN            GPIO_Pin_12
#define MB_ENCB_GPIO_PORT    GPIOD
#define MB_ENCB_GPIO_CLK    RCC_AHB1Periph_GPIOD
#define MB_ENCB_SOURCE        GPIO_PinSource12
#define MB_ENCB_AF            GPIO_AF_TIM4

// OK MOTOR 3
#define MC_TIMER            TIM2
#define MC_TIMER_CLK        RCC_APB1Periph_TIM2
#define MC_ENCA_PIN            GPIO_Pin_5
#define MC_ENCA_GPIO_PORT    GPIOA
#define MC_ENCA_GPIO_CLK    RCC_AHB1Periph_GPIOA
#define MC_ENCA_SOURCE        GPIO_PinSource5
#define MC_ENCA_AF            GPIO_AF_TIM2
#define MC_ENCB_PIN            GPIO_Pin_3
#define MC_ENCB_GPIO_PORT    GPIOB
#define MC_ENCB_GPIO_CLK    RCC_AHB1Periph_GPIOB
#define MC_ENCB_SOURCE        GPIO_PinSource3
#define MC_ENCB_AF            GPIO_AF_TIM2

// OK MOTOR 4
#define MD_TIMER            TIM1
#define MD_TIMER_CLK        RCC_APB2Periph_TIM1
#define MD_ENCA_PIN            GPIO_Pin_9
#define MD_ENCA_GPIO_PORT    GPIOE
#define MD_ENCA_GPIO_CLK    RCC_AHB1Periph_GPIOE
#define MD_ENCA_SOURCE        GPIO_PinSource9
#define MD_ENCA_AF            GPIO_AF_TIM1
#define MD_ENCB_PIN            GPIO_Pin_11
#define MD_ENCB_GPIO_PORT    GPIOE
#define MD_ENCB_GPIO_CLK    RCC_AHB1Periph_GPIOE
#define MD_ENCB_SOURCE        GPIO_PinSource11
#define MD_ENCB_AF            GPIO_AF_TIM1

// MOTOR INFO
#define TICK_PER_ROT    6400
#define MILLI_PER_MN    60000
#define WHEEL_RADIUS    35    // mm

#define M_PI            3.14159

// Functions

void MotorEncodersInit(void);
void MotorEncodersReset(void);
void MotorEncodersRead(void);

void update_traveled_distance(uint8_t motor, int32_t last_speed, uint32_t time_delta);
void reset_traveled_distance();

#define _MOTOR_ENCODER_H_
#endif
