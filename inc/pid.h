// pid.h

#ifndef _PID_H_
#define _PID_H_

#include "main.h"
#include "motor.h"
#define P_GAIN 1
#define I_GAIN 0
#define D_GAIN 0
#define MAX_COMMAND 1
#define DELTA_T_TIMESCALE 1000 //ms

//doc: http://brettbeauregard.com/blog/2011/04/improving-the-beginners-pid-introduction/

typedef struct PIDData {
    float proportionalGain;
    float integralGain;
    float derivativeGain;
    float previousInput;
    float maxCommand;
    float accumulator;
    uint32_t lastTimestamp;
} PIDType;

PIDType PID_data[MOTOR_COUNT];

void pidInit(void);
float computePIDCommand(PIDType*, uint32_t, int, int);
void updatePID(void);

#endif
