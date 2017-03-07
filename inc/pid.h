// pid.h

#ifndef _PID_H_
#define _PID_H_

#include "main.h"
#include "motor.h"


//doc: http://brettbeauregard.com/blog/2011/04/improving-the-beginners-pid-introduction/

typedef struct PIDData {
    float kp;
    float ki;
    float kd;
    short previous_input;
    float accumulator;
    uint32_t last_timestamp;
} PIDData;

PIDData PID_data[MOTOR_COUNT];

void pid_init(void);
void pid_setpoint(int, float);
void pid_update(void);
short pid_compute_cmd(PIDData *, float, float, float, int);

#endif
