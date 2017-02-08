// MotorEncoder.c

#include "MotorEncoder.h"

void MotorEncodersInit(){
    GPIO_InitTypeDef GPIO_InitStructure;

    RCC_AHB1PeriphClockCmd(MA_ENCA_GPIO_CLK, ENABLE);
    RCC_AHB1PeriphClockCmd(MA_ENCB_GPIO_CLK, ENABLE);
    RCC_AHB1PeriphClockCmd(MB_ENCA_GPIO_CLK, ENABLE);
    RCC_AHB1PeriphClockCmd(MB_ENCB_GPIO_CLK, ENABLE);
    //RCC_AHB1PeriphClockCmd(MC_ENCA_GPIO_CLK, ENABLE);
    //RCC_AHB1PeriphClockCmd(MC_ENCB_GPIO_CLK, ENABLE);
    RCC_AHB1PeriphClockCmd(MD_ENCA_GPIO_CLK, ENABLE);
    RCC_AHB1PeriphClockCmd(MD_ENCB_GPIO_CLK, ENABLE);

    // Enable IRQ for TIM2 in NVIC

    //NVIC_EnableIRQ(TIM4_IRQn);

    GPIO_StructInit(&GPIO_InitStructure);
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_AF;
    GPIO_InitStructure.GPIO_PuPd = GPIO_PuPd_UP;

    // Motor A
    GPIO_InitStructure.GPIO_Pin = MA_ENCA_PIN | MA_ENCB_PIN;
    GPIO_Init(MA_ENCA_GPIO_PORT, &GPIO_InitStructure);

    // Motor B
    GPIO_InitStructure.GPIO_Pin = MB_ENCA_PIN | MB_ENCB_PIN;
    GPIO_Init(MB_ENCA_GPIO_PORT, &GPIO_InitStructure);

    // Motor C
    //GPIO_InitStructure.GPIO_Pin = MC_ENCA_PIN | MC_ENCB_PIN;
    //GPIO_Init(MC_ENCA_GPIO_PORT, &GPIO_InitStructure);


    // Motor D
    GPIO_InitStructure.GPIO_Pin = MD_ENCA_PIN | MD_ENCB_PIN;
    GPIO_Init(MD_ENCA_GPIO_PORT, &GPIO_InitStructure);

    GPIO_PinAFConfig(MD_ENCA_GPIO_PORT, MD_ENCA_SOURCE, MD_ENCA_AF);
    GPIO_PinAFConfig(MD_ENCB_GPIO_PORT, MD_ENCB_SOURCE, MD_ENCB_AF);

    GPIO_PinAFConfig(MA_ENCA_GPIO_PORT, MA_ENCA_SOURCE, MA_ENCA_AF);
	GPIO_PinAFConfig(MA_ENCB_GPIO_PORT, MA_ENCB_SOURCE, MA_ENCB_AF);
	GPIO_PinAFConfig(MB_ENCA_GPIO_PORT, MB_ENCA_SOURCE, MB_ENCA_AF);
	GPIO_PinAFConfig(MB_ENCB_GPIO_PORT, MB_ENCB_SOURCE, MB_ENCB_AF);
	//GPIO_PinAFConfig(MC_ENCA_GPIO_PORT, MC_ENCA_SOURCE, MC_ENCA_AF);
	//GPIO_PinAFConfig(MC_ENCB_GPIO_PORT, MC_ENCB_SOURCE, MC_ENCB_AF);

    RCC_APB1PeriphClockCmd(MA_TIMER_CLK, ENABLE);
    RCC_APB1PeriphClockCmd(MB_TIMER_CLK, ENABLE);
    //RCC_APB1PeriphClockCmd(MC_TIMER_CLK, ENABLE); //RCC_APB1PeriphClockCmd(MC_TIMER_CLK, ENABLE);
    RCC_APB2PeriphClockCmd(MD_TIMER_CLK, ENABLE);

    TIM_EncoderInterfaceConfig(MA_TIMER, TIM_EncoderMode_TI12,
                                TIM_ICPolarity_Rising,
                                TIM_ICPolarity_Rising);
    TIM_EncoderInterfaceConfig(MB_TIMER, TIM_EncoderMode_TI12,
                                    TIM_ICPolarity_Rising,
                                    TIM_ICPolarity_Rising);
   /* TIM_EncoderInterfaceConfig(MC_TIMER, TIM_EncoderMode_TI12,
                                    TIM_ICPolarity_Rising,
                                    TIM_ICPolarity_Rising);*/
    TIM_EncoderInterfaceConfig(MD_TIMER, TIM_EncoderMode_TI12,
                                    TIM_ICPolarity_Rising,
                                    TIM_ICPolarity_Rising);

    TIM_SetAutoreload(MA_TIMER, 0xffff);
    TIM_SetAutoreload(MB_TIMER, 0xffff);
    //TIM_SetAutoreload(MC_TIMER, 0xffff);
    TIM_SetAutoreload(MD_TIMER, 0xffff);

    motors[0].ENCx = MA_TIMER;
    motors[1].ENCx = MB_TIMER;
    motors[2].ENCx = TIM9;
    motors[3].ENCx = MD_TIMER;

    TIM_Cmd(MA_TIMER, ENABLE);
    TIM_Cmd(MB_TIMER, ENABLE);
    //TIM_Cmd(MC_TIMER, ENABLE);
    TIM_Cmd(MD_TIMER, ENABLE);

    //GPIOA->MODER |= (1 << 2);
    /*TIM5->CR1 |= (1 << 4);
    GPIOA->AFR[0] |= 0x2;
    GPIOA->AFR[0] |= (0x2 << 2);

    GPIOA->MODER = 0xfea;*/

    // Reset variables
    for (int i = 0; i < MOTOR_COUNT; i++) {
		motors[i].motor_speed_rpm = 0;
		motors[i].old_timestamp = 0;
		motors[i].encoder_cnt = 0;
		motors[i].old_encoder_cnt = 0;
		TIM_SetCounter(motors[i].ENCx, 0);
    }

    MotorEncodersRead();
}

void MotorEncodersRead(){
	// Get encoders count
#ifdef ID_MODE
	int i = 0;
#else
	for (int i = 0; i < MOTOR_COUNT; i++) {
#endif
		motors[i].old_encoder_cnt = motors[i].encoder_cnt;
		motors[i].encoder_cnt = TIM_GetCounter(motors[i].ENCx);

	    // Set speed with encoder count
	    uint32_t tmp_timestamp = timestamp;

	    // RPM
	    //motors[i].motor_speed_rpm = ((motors[i].encoder_cnt - motors[i].old_encoder_cnt)*MILLI_PER_MN)/((tmp_timestamp-motors[i].old_timestamp)*TICK_PER_ROT);
	    //motors[i].motor_speed_rom = ((motors[i].encoder_cnt * 1000)/)
	    // Ticks/second
	    uint32_t last_tick_delta = motors[i].encoder_cnt - motors[i].old_encoder_cnt;
	    uint32_t last_timestamp_delta = tmp_timestamp - motors[i].old_timestamp;
	    motors[i].motor_speed_rpm = (last_tick_delta*1000)/last_timestamp_delta;
	    //motors[i].last_tick_delta = motors[i].encoder_cnt - motors[i].old_encoder_cnt;
	    ///motors[i].last_timestamp_delta = tmp_timestamp - motors[i].old_timestamp;
	    //motors[i].motor_speed_tick_second = (motors[i].last_tick_delta*1000)/motors[i].last_timestamp_delta;

	    motors[i].old_timestamp = tmp_timestamp;

#ifdef ID_MODE
	    collectIdResponse(motors[i].motor_speed_rpm);
#endif
#ifndef ID_MODE
	}
#endif
}
