// MotorController.h

#ifndef _MOTOR_CONTROLLER_H_
#define _MOTOR_CONTROLLER_H_

#include "stm32f4xx_tim.h"
#include "stm32f4xx_rcc.h"
#include "stm32f4xx_gpio.h"
#include "motor.h"

// Motor speed control via PWM signal
#define MCS_PWM_CLK_PORT     RCC_APB1Periph_TIM3
#define MCS_PWM_CLK          TIM3
#define MCS_PWM_CLK_AF       GPIO_AF_TIM3
#define MCS_PIN_CLK          RCC_AHB1Periph_GPIOC
#define MCS_PIN_A            GPIO_Pin_6
#define MCS_PIN_B            GPIO_Pin_7
#define MCS_PIN_C            GPIO_Pin_8
#define MCS_PIN_D            GPIO_Pin_9
#define MCS_PIN_SOURCE_A     GPIO_PinSource6
#define MCS_PIN_SOURCE_B     GPIO_PinSource7
#define MCS_PIN_SOURCE_C     GPIO_PinSource8
#define MCS_PIN_SOURCE_D     GPIO_PinSource9
#define MCS_PIN_PORT         GPIOC

// Motor direction control
// Each motor needs two pin:
// 0 0 -> brake to ground
// 0 1 -> clockwise
// 1 0 -> counter clockwise
// 1 1 -> brake to v-motor
#define MC_DIR_BGND            0
#define MC_DIR_CW            1
#define MC_DIR_CCW            2
#define MC_DIR_BVMOTOR        3

#define MCD_A_PIN1_CLK_PORT        RCC_AHB1Periph_GPIOE
#define MCD_A_PIN1_PORT            GPIOE
#define MCD_A_PIN1                GPIO_Pin_1
#define MCD_A_PIN2_CLK_PORT        RCC_AHB1Periph_GPIOE
#define MCD_A_PIN2_PORT            GPIOE
#define MCD_A_PIN2                GPIO_Pin_0

#define MCD_B_PIN1_CLK_PORT        RCC_AHB1Periph_GPIOD
#define MCD_B_PIN1_PORT            GPIOD
#define MCD_B_PIN1                GPIO_Pin_7
#define MCD_B_PIN2_CLK_PORT        RCC_AHB1Periph_GPIOE
#define MCD_B_PIN2_PORT            GPIOE
#define MCD_B_PIN2                GPIO_Pin_2

#define MCD_C_PIN1_CLK_PORT        RCC_AHB1Periph_GPIOC
#define MCD_C_PIN1_PORT            GPIOC
#define MCD_C_PIN1                GPIO_Pin_13
#define MCD_C_PIN2_CLK_PORT        RCC_AHB1Periph_GPIOC
#define MCD_C_PIN2_PORT            GPIOC
#define MCD_C_PIN2                GPIO_Pin_10

#define MCD_D_PIN1_CLK_PORT        RCC_AHB1Periph_GPIOC
#define MCD_D_PIN1_PORT            GPIOC
#define MCD_D_PIN1                GPIO_Pin_11
#define MCD_D_PIN2_CLK_PORT        RCC_AHB1Periph_GPIOC
#define MCD_D_PIN2_PORT            GPIOC
#define MCD_D_PIN2                GPIO_Pin_12

#define MAX_CONSIGNE        100
#define PWM_PULSE_LENGTH    8399
#define MAX_PULSE_LENGTH    PWM_PULSE_LENGTH*MAX_CONSIGNE/100


void motor_controller_init(void);
void motor_set_pwm_percentage(uint8_t, float);
int motor_set_direction(uint8_t, float);

#endif
