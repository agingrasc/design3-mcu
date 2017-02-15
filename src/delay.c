// delay.c

#include <stm32f4xx_tim.h>
#include <misc.h>
#include "delay.h"

void initDelay(void) {
    SysTick_Config(SystemCoreClock/1000);
    NVIC_InitTypeDef systick_init;
    systick_init.NVIC_IRQChannel = SysTick_IRQn;
    systick_init.NVIC_IRQChannelCmd = ENABLE;
    systick_init.NVIC_IRQChannelPreemptionPriority = 0x05;
    systick_init.NVIC_IRQChannelSubPriority = 0x05;
    NVIC_Init(&systick_init);
}

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

    //timer responsable du timestamp
    RCC_APB1PeriphClockCmd(RCC_APB2Periph_TIM9, ENABLE);
    TIM_TimeBaseInitTypeDef tim9_init_struct;
    tim9_init_struct.TIM_CounterMode = TIM_CounterMode_Down;
    tim9_init_struct.TIM_ClockDivision = TIM_CKD_DIV1;
    // timer tick = 168 000 000 / ((499 + 1) * (1 + 1)) = 1000 (1ms)
    tim9_init_struct.TIM_Prescaler = 499;
    tim9_init_struct.TIM_Period = 1;
    TIM_TimeBaseInit(TIM9, &tim9_init_struct);
    TIM_ITConfig(TIM9, TIM_IT_Update, ENABLE);
    TIM_Cmd(TIM9, ENABLE);

    // +++ NVIC +++
    NVIC_InitTypeDef NVIC1_InitStructure;
    NVIC1_InitStructure.NVIC_IRQChannel = TIM7_IRQn;
    NVIC1_InitStructure.NVIC_IRQChannelCmd = ENABLE;
    NVIC1_InitStructure.NVIC_IRQChannelPreemptionPriority = 0x0F;
    NVIC1_InitStructure.NVIC_IRQChannelSubPriority = 0x0F;
    NVIC_Init(&NVIC1_InitStructure);

    NVIC_InitTypeDef nvic2_init;
    nvic2_init.NVIC_IRQChannel = 24; //la table d'interrupt a ete modifie pour pointer vers TIM9_Handler
    nvic2_init.NVIC_IRQChannelCmd = ENABLE;
    nvic2_init.NVIC_IRQChannelPreemptionPriority = 0x0f;
    nvic2_init.NVIC_IRQChannelSubPriority = 0x10;
    NVIC_Init(&nvic2_init);
}

void TIM7_IRQHandler(void) {
    MotorEncodersRead();
#ifndef ID_MODE
    updatePID();
#endif
    TIM_ClearITPendingBit(TIM7, TIM_IT_Update);
}

void TIM9_IRQHandler(void) {
}

void SysTick_Handler(void) {
    timestamp++;
}

void delay(uint32_t wait) {
    uint32_t target = timestamp + wait;
    while (target > timestamp);
}

void udelay(uint16_t wait) {

}

