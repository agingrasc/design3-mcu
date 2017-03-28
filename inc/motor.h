#ifndef MOTOR_H_
#define MOTOR_H_

#define MOTOR_COUNT    4

#define MOTOR_REAR_X            0x0
#define MOTOR_FRONT_Y           0x1
#define MOTOR_FRONT_X           0x2
#define MOTOR_REAR_Y            0x3

#define MOTOR_FORWARD 0
#define MOTOR_BACKWARD 1
#define MOTOR_BREAK 100

typedef struct motor {
    // PWM (speed)
    __IO uint32_t *duty_cycle;
    float input_consigne;
    uint32_t consigne_pulse;
    char old_consigne_percent;
    char consigne_percent;
    // Direction
    GPIO_TypeDef *DIRx_pin1;
    GPIO_TypeDef *DIRx_pin2;
    uint16_t dir_pin1;
    uint16_t dir_pin2;
    // Encoder
    TIM_TypeDef *ENCx;
    volatile int32_t motor_speed;
    volatile uint32_t old_timestamp;
    volatile uint32_t encoder_cnt;
    volatile uint32_t old_encoder_cnt;
    short motor_direction;
    float traveled_distance;

} Motor;

Motor motors[MOTOR_COUNT];

#endif /* MOTOR_H_ */
