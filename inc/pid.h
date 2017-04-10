// pid.h

#ifndef _PID_H_
#define _PID_H_

#include "main.h"
#include "motor.h"


//doc: http://brettbeauregard.com/blog/2011/04/improving-the-beginners-pid-introduction/

typedef struct PIDData {
    float kp[2];
    float ki[2];
    float kd[2];
    short deadzone[2];
    short previous_input;
    float last_command;
    float accumulator;
    uint32_t last_timestamp;
    uint8_t real_direction;
} PIDData;

PIDData PID_data[MOTOR_COUNT];

int PID_mode;

void pid_init(void);
void pid_setpoint(int, float);
void pid_update(void);
float pid_compute_cmd(PIDData *, float, float, float, float);

#endif
