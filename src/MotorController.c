// MotorController.c

#include "MotorController.h"

void motorControllerInit(void){
	int i;
	for (i = 0; i < MOTOR_COUNT; i++) {
		motors[i].input_consigne_rpm = 0x0;
		motors[i].consigne_percent = 0x0;
		motors[i].old_consigne_percent = 0x0;
	}

    setupPWMTimer();
}

void setupPWMTimer(void){
	// Direction setup
	GPIO_InitTypeDef GPIO_InitStructure;

	RCC_AHB1PeriphClockCmd(MCD_CLK_PORT, ENABLE);
	GPIO_InitTypeDef init_gpio_struct;
	init_gpio_struct.GPIO_Pin = MCD_A_PIN1 | MCD_A_PIN2 | MCD_B_PIN1 | MCD_B_PIN2 | MCD_C_PIN1 | MCD_C_PIN2 | MCD_D_PIN1 | MCD_D_PIN2;
	init_gpio_struct.GPIO_OType = GPIO_OType_PP;
	init_gpio_struct.GPIO_PuPd = GPIO_PuPd_NOPULL;
	init_gpio_struct.GPIO_Mode = GPIO_Mode_OUT;
	init_gpio_struct.GPIO_Speed = GPIO_Speed_100MHz;
	GPIO_Init(MCS_PIN_PORT, &init_gpio_struct);

	// PWM setup
    RCC_AHB1PeriphClockCmd(MCS_PIN_CLK, ENABLE);
    GPIO_PinAFConfig(MCS_PIN_PORT, MCS_PIN_SOURCE_A, MCS_PWM_CLK_AF);
    GPIO_PinAFConfig(MCS_PIN_PORT, MCS_PIN_SOURCE_B, MCS_PWM_CLK_AF);
    GPIO_PinAFConfig(MCS_PIN_PORT, MCS_PIN_SOURCE_C, MCS_PWM_CLK_AF);
    GPIO_PinAFConfig(MCS_PIN_PORT, MCS_PIN_SOURCE_D, MCS_PWM_CLK_AF);

    init_gpio_struct.GPIO_Pin = MCS_PIN_A | MCS_PIN_B | MCS_PIN_C | MCS_PIN_D;
    init_gpio_struct.GPIO_OType = GPIO_OType_PP;
    init_gpio_struct.GPIO_PuPd = GPIO_PuPd_UP;
    init_gpio_struct.GPIO_Mode = GPIO_Mode_AF;
    init_gpio_struct.GPIO_Speed = GPIO_Speed_100MHz;
    GPIO_Init(MCS_PIN_PORT, &init_gpio_struct);

    TIM_TimeBaseInitTypeDef init_base_struct;
    RCC_APB1PeriphClockCmd(MCS_PWM_CLK_PORT, ENABLE);
    init_base_struct.TIM_Prescaler = (uint16_t) ((SystemCoreClock /2) / 28000000) - 1;
    init_base_struct.TIM_ClockDivision = 0;
    init_base_struct.TIM_CounterMode = TIM_CounterMode_Up;
    init_base_struct.TIM_Period = PWM_PULSE_LENGTH;
    TIM_TimeBaseInit(MCS_PWM_CLK, &init_base_struct);

    TIM_OCInitTypeDef init_osc_struct;
    init_osc_struct.TIM_OCMode = TIM_OCMode_PWM1;
    init_osc_struct.TIM_OutputState = TIM_OutputState_Enable;
    init_osc_struct.TIM_OCPolarity = TIM_OCPolarity_High;
    init_osc_struct.TIM_Pulse = 0;

    // Enable PWMS
    TIM_OC1Init(MCS_PWM_CLK, &init_osc_struct);
    TIM_OC1PreloadConfig(MCS_PWM_CLK, TIM_OCPreload_Enable);
    TIM_OC2Init(MCS_PWM_CLK, &init_osc_struct);
	TIM_OC2PreloadConfig(MCS_PWM_CLK, TIM_OCPreload_Enable);
	TIM_OC3Init(MCS_PWM_CLK, &init_osc_struct);
	TIM_OC3PreloadConfig(MCS_PWM_CLK, TIM_OCPreload_Enable);
	TIM_OC4Init(MCS_PWM_CLK, &init_osc_struct);
	TIM_OC4PreloadConfig(MCS_PWM_CLK, TIM_OCPreload_Enable);

    TIM_Cmd(MCS_PWM_CLK, ENABLE);

    // assign duty cycle pointers to data structure
    motors[0].duty_cycle = &(MCS_PWM_CLK->CCR1);
    motors[1].duty_cycle = &(MCS_PWM_CLK->CCR2);
    motors[2].duty_cycle = &(MCS_PWM_CLK->CCR3);
    motors[3].duty_cycle = &(MCS_PWM_CLK->CCR4);

    // Default to 0
    *(motors[0].duty_cycle) = 0;
    *(motors[1].duty_cycle) = 0;
    *(motors[2].duty_cycle) = 0;
    *(motors[3].duty_cycle) = 0;
}

void setPWMConsigne(uint8_t motor_id, uint32_t consigne){
    if(consigne > PWM_PULSE_LENGTH*MAX_CONSIGNE/100)
        consigne = PWM_PULSE_LENGTH*MAX_CONSIGNE/100;
    motors[motor_id].consigne_pulse = consigne;
    //MC_PWM_CLK->CCR1 = consigne;
    *(motors[motor_id].duty_cycle) = consigne;
}

void setupPWMPercentage(uint8_t motor_id, uint32_t percentage){
    if((char)percentage > MAX_CONSIGNE) percentage = MAX_CONSIGNE;
    if((char)percentage != motors[motor_id].old_consigne_percent){
    	motors[motor_id].old_consigne_percent = percentage;
        //MC_PWM_CLK->CCR1 = PWM_PULSE_LENGTH * percentage / 100;
    	*(motors[motor_id].duty_cycle) = PWM_PULSE_LENGTH * percentage / 100;
    }
}

uint32_t motorGetTarget(uint8_t motor_id){
    return motors[motor_id].consigne_pulse;
}

uint8_t motorSetDirection(uint8_t motor_id, uint8_t motor_dir) {
	BitAction pv1, pv2;

	switch (motor_dir) {
	case MC_DIR_BGND:
		pv1 = Bit_RESET;
		pv2 = Bit_RESET;
		break;
	case MC_DIR_CW:
		pv1 = Bit_RESET;
		pv2 = Bit_SET;
		break;
	case MC_DIR_CCW:
		pv1 = Bit_SET;
		pv2 = Bit_RESET;
		break;
	case MC_DIR_BVMOTOR:
		pv1 = Bit_SET;
		pv2 = Bit_SET;
		break;
	default:
		return -1;
	}

	GPIO_WriteBit(motors[motor_id].DIRx, motors[motor_id].dir_pin1, pv1);
	GPIO_WriteBit(motors[motor_id].DIRx, motors[motor_id].dir_pin2, pv2);

	return 0;
}
