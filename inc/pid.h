// pid.h

#ifndef _PID_H_
#define _PID_H_

#include "main.h"
#include "motor.h"


//doc: http://brettbeauregard.com/blog/2011/04/improving-the-beginners-pid-introduction/

typedef struct PIDData {
    short proportionalGain;
    short integralGain;
    short previousInput;
    short accumulator;
    uint32_t lastTimestamp;
} PIDData;

PIDData PID_data[MOTOR_COUNT];

void pidInit(void);
void pid_setpoint(Motor*, short);
void updatePID(void);

#endif
