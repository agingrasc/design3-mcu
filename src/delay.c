// delay.c

#include "delay.h"

void initTimer(void) {
    // +++ TIM7 - MicroSecond +++
    RCC_APB1PeriphClockCmd(RCC_APB1Periph_TIM7, ENABLE);
    TIM_TimeBaseInitTypeDef tim7_init_struct;
    tim7_init_struct.TIM_CounterMode = TIM_CounterMode_Up;
    tim7_init_struct.TIM_ClockDivision = TIM_CKD_DIV1;
    // timer_tick_freq = 84000000 / ((2099 + 1 )*(999 + 1)) = 40 (0.025 s = 25 ms)
    tim7_init_struct.TIM_Prescaler = 2099;
    tim7_init_struct.TIM_Period = 999;
    TIM_TimeBaseInit(TIM7, &tim7_init_struct);
    TIM_ITConfig(TIM7, TIM_IT_Update, ENABLE);
    TIM_Cmd(TIM7, ENABLE);

    // +++ NVIC +++
    NVIC_InitTypeDef NVIC1_InitStructure;
    NVIC1_InitStructure.NVIC_IRQChannel = TIM7_IRQn;
    NVIC1_InitStructure.NVIC_IRQChannelCmd = ENABLE;
    NVIC1_InitStructure.NVIC_IRQChannelPreemptionPriority = 0x0F;
    NVIC1_InitStructure.NVIC_IRQChannelSubPriority = 0x0F;
    NVIC_Init(&NVIC1_InitStructure);
}

void TIM7_IRQHandler(void) {
    //GPIO_ToggleBits(GPIOD, GPIO_Pin_15);
    MotorEncodersRead();
#ifndef ID_MODE
    updatePID();
#endif
    TIM_ClearITPendingBit(TIM7, TIM_IT_Update);
}

void delay(uint32_t wait) {

}

void udelay(uint16_t wait) {

}

