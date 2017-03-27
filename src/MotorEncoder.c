// MotorEncoder.c

#include "MotorEncoder.h"

void reset_traveled_distance() {
    for (int i = 0; i < MOTOR_COUNT; i++) {
        motors[i].traveled_distance = 0;
    }
}

void update_traveled_distance(uint8_t motor, int32_t last_speed, uint32_t time_delta) {
    // Convert speed to mm/sec
    int32_t metric_speed = last_speed * ((2*M_PI*WHEEL_RADIUS)/(TICK_PER_ROT));

    // Compute traveled distance since last encoder read
    int32_t traveled_distance =  metric_speed * time_delta;

    // Update the overall traveled distance
    motors[motor].traveled_distance += traveled_distance;
}

void MotorEncodersInit() {
    GPIO_InitTypeDef GPIO_InitStructure;

    RCC_AHB1PeriphClockCmd(MA_ENCA_GPIO_CLK, ENABLE);
    RCC_AHB1PeriphClockCmd(MA_ENCB_GPIO_CLK, ENABLE);
    RCC_AHB1PeriphClockCmd(MB_ENCA_GPIO_CLK, ENABLE);
    RCC_AHB1PeriphClockCmd(MB_ENCB_GPIO_CLK, ENABLE);
#ifndef MOTOR3_ENC_ALT
    RCC_AHB1PeriphClockCmd(MC_ENCA_GPIO_CLK, ENABLE);
    RCC_AHB1PeriphClockCmd(MC_ENCB_GPIO_CLK, ENABLE);
#endif
    RCC_AHB1PeriphClockCmd(MD_ENCA_GPIO_CLK, ENABLE);
    RCC_AHB1PeriphClockCmd(MD_ENCB_GPIO_CLK, ENABLE);

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
#ifndef MOTOR3_ENC_ALT
    GPIO_InitStructure.GPIO_Pin = MC_ENCA_PIN | MC_ENCB_PIN;
    GPIO_Init(MC_ENCA_GPIO_PORT, &GPIO_InitStructure);
#endif

    // This is alternative quadrature encoder read pin in case JTAG causes trouble
    // Hope we will never need it
#ifdef MOTOR3_ENC_ALT
    RCC->AHB1ENR |= RCC_AHB1Periph_GPIOE;
    RCC->APB2ENR |= RCC_APB2Periph_TIM9;
    GPIOE->MODER |= (0x2 << 10);
    GPIOE->PUPDR |= (0x1 << 10);
    GPIOE->AFR[0] |= (GPIO_AF_TIM9 << 20);
    TIM9->CCMR1 |= 0x1;
    TIM9->CCER |= 0x1;
    TIM9->ARR = 0xffff;
    TIM9->SMCR |= (4 << 4);
    TIM9->SMCR |= 5;
    TIM9->CR1 |= 0x1;
#endif

    // Motor D
    GPIO_InitStructure.GPIO_Pin = MD_ENCA_PIN | MD_ENCB_PIN;
    GPIO_Init(MD_ENCA_GPIO_PORT, &GPIO_InitStructure);

    GPIO_PinAFConfig(MA_ENCA_GPIO_PORT, MA_ENCA_SOURCE, MA_ENCA_AF);
    GPIO_PinAFConfig(MA_ENCB_GPIO_PORT, MA_ENCB_SOURCE, MA_ENCB_AF);
    GPIO_PinAFConfig(MB_ENCA_GPIO_PORT, MB_ENCA_SOURCE, MB_ENCA_AF);
    GPIO_PinAFConfig(MB_ENCB_GPIO_PORT, MB_ENCB_SOURCE, MB_ENCB_AF);
#ifndef MOTOR3_ENC_ALT
    GPIO_PinAFConfig(MC_ENCA_GPIO_PORT, MC_ENCA_SOURCE, MC_ENCA_AF);
    GPIO_PinAFConfig(MC_ENCB_GPIO_PORT, MC_ENCB_SOURCE, MC_ENCB_AF);
#endif
    GPIO_PinAFConfig(MD_ENCA_GPIO_PORT, MD_ENCA_SOURCE, MD_ENCA_AF);
    GPIO_PinAFConfig(MD_ENCB_GPIO_PORT, MD_ENCB_SOURCE, MD_ENCB_AF);

    RCC_APB1PeriphClockCmd(MA_TIMER_CLK, ENABLE);
    RCC_APB1PeriphClockCmd(MB_TIMER_CLK, ENABLE);
#ifndef MOTOR3_ENC_ALT
    RCC_APB1PeriphClockCmd(MC_TIMER_CLK, ENABLE);
#endif
    RCC_APB2PeriphClockCmd(MD_TIMER_CLK, ENABLE);

    TIM_EncoderInterfaceConfig(MA_TIMER, TIM_EncoderMode_TI12,
                               TIM_ICPolarity_Rising,
                               TIM_ICPolarity_Rising);
    TIM_EncoderInterfaceConfig(MB_TIMER, TIM_EncoderMode_TI12,
                               TIM_ICPolarity_Rising,
                               TIM_ICPolarity_Rising);
#ifndef MOTOR3_ENC_ALT
    TIM_EncoderInterfaceConfig(MC_TIMER, TIM_EncoderMode_TI12,
                               TIM_ICPolarity_Rising,
                               TIM_ICPolarity_Rising);
#endif
    TIM_EncoderInterfaceConfig(MD_TIMER, TIM_EncoderMode_TI12,
                               TIM_ICPolarity_Rising,
                               TIM_ICPolarity_Rising);

    TIM_SetAutoreload(MA_TIMER, 0xffff);
    TIM_SetAutoreload(MB_TIMER, 0xffff);
#ifndef MOTOR3_ENC_ALT
    TIM_SetAutoreload(MC_TIMER, 0xffff);
#endif
    TIM_SetAutoreload(MD_TIMER, 0xffff);

    motors[0].ENCx = MA_TIMER;
    motors[1].ENCx = MB_TIMER;
#ifndef MOTOR3_ENC_ALT
    motors[2].ENCx = MC_TIMER;
#else
    motors[2].ENCx = TIM9;
#endif
    motors[3].ENCx = MD_TIMER;

    // Input filter
    motors[0].ENCx->CCMR1 |= (0x3 << 4);
    motors[0].ENCx->CCMR1 |= (0x3 << 12);

    // Enable timers
    TIM_Cmd(MA_TIMER, ENABLE);
    TIM_Cmd(MB_TIMER, ENABLE);
#ifndef MOTOR3_ENC_ALT
    TIM_Cmd(MC_TIMER, ENABLE);
#endif
    TIM_Cmd(MD_TIMER, ENABLE);

    // Reset variables
    for (int i = 0; i < MOTOR_COUNT; i++) {
        motors[i].motor_speed = 0;
        motors[i].old_timestamp = 0;
        // Set current count to half the autoreload value.
        motors[i].encoder_cnt = TIMER_INIT_VAL;
        motors[i].old_encoder_cnt = TIMER_INIT_VAL;
        motors[i].traveled_distance = 0;
        TIM_SetCounter(motors[i].ENCx, TIMER_INIT_VAL);
    }

    MotorEncodersRead();
}

void MotorEncodersRead() {
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

    int32_t last_tick_delta = motors[i].encoder_cnt - motors[i].old_encoder_cnt;

    // Because the timer always count up, the following should never happen.
    // Then, it will only happen when the timer overflows inbetween two samples
    // However, I have noticed that sometime when killing speed, the counter jitter and in
    // that case, old_encoder_cnt might be greater than encoder_cnt but not very much
    // in that case, we will use old_encoder_cnt - encoder_cnt

    if (last_tick_delta < -30) {
        last_tick_delta = (0xFFFF - motors[i].old_encoder_cnt) + motors[i].encoder_cnt;
    } else if (last_tick_delta < 0) {
        last_tick_delta = motors[i].old_encoder_cnt - motors[i].encoder_cnt;
    }

    // RPM
    //motors[i].motor_speed = ((last_tick_delta)*MILLI_PER_MN)/((tmp_timestamp-motors[i].old_timestamp)*TICK_PER_ROT);
    // Tick/sec

    uint32_t time_delta = (tmp_timestamp - motors[i].old_timestamp);

    motors[i].motor_speed = (last_tick_delta * 1000) / time_delta;

    motors[i].old_timestamp = tmp_timestamp;

    //update_traveled_distance(i, motors[i].motor_speed, time_delta);

#ifdef ID_MODE
    collectIdResponse(motors[i].motor_speed);
#endif
#ifndef ID_MODE
    }
#endif
}
