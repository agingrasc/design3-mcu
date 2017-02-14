// pid.c

#include "pid.h"

/**
 * Initialise le PID
 */
void pidInit(void) {
    // Init structure
    PID_data[current_motor].proportionalGain = P_GAIN;
    PID_data[current_motor].integralGain = I_GAIN;
    PID_data[current_motor].derivativeGain = D_GAIN;
    PID_data[current_motor].previousInput = 0;
    PID_data[current_motor].maxCommand = MAX_COMMAND;
    PID_data[current_motor].accumulator = 0;
    PID_data[current_motor].lastTimestamp = 0;
}

/**
 * Limite la commande
 */
float clampCommand(PIDType *pidData, float naiveCommand) {
    if (naiveCommand > pidData->maxCommand) {
        return pidData->maxCommand;
    } else {
        return naiveCommand;
    }
}

/**
 * Limite la valeur de l'accumulator
 */
float clampAccumulator(PIDType *pidData, float accVal) {
    float maxAccumulator = pidData->maxCommand / pidData->integralGain;
    if (accVal > maxAccumulator) {
        pidData->accumulator = maxAccumulator;
        return maxAccumulator;
    } else {
        pidData->accumulator = accVal;
        return accVal;
    }
}

/**
 * Calcul une commande de [0, 1] pour atteindre et maintenir la consigne.
 * Args:
 * - pidData -> struct des données du pid calculé
 * - delta_t -> le timestamp du systeme, doit respecter le DELTA_T_TIMESCALE
 * - targetSpeed -> la consigne en nombre de tick/s
 * - current_speed -> l'état actuel du plant en tick/s
 *
 * Return:
 * La commande [0, 1], où 1 équivaut à 100% de la tension.
 */
float computePIDCommand(PIDType *pidData, uint32_t timestamp, int targetSpeed, int current_speed) {
    float delta_t = (timestamp - pidData->lastTimestamp) / DELTA_T_TIMESCALE;
    float error = targetSpeed - current_speed;
    float pCmd = pidData->proportionalGain * error;
    float iCmd = pidData->accumulator + pidData->integralGain * error * delta_t;
    iCmd = clampAccumulator(pidData, iCmd);
    float inputDerivative = current_speed - pidData->previousInput;
    float dCmd = inputDerivative * pidData->derivativeGain / delta_t;

    float naiveCmd = pCmd + iCmd + dCmd;
    float cmd = clampCommand(pidData, naiveCmd);

    //sauvegarde donnee pour prochain calcul
    pidData->previousInput = current_speed;
    pidData->lastTimestamp = timestamp;
    return cmd;
}

/**
 * Boucle du PID de l'interruption
 */
void updatePID(void) {
    for (int i = 0; i < MOTOR_COUNT; i++) {
        if (PID_mode) {
            float perc_consig = computePIDCommand(&PID_data[i], timestamp, (int) motors[i].input_consigne,
                                                  (int) motors[i].motor_speed);
            uint32_t new_consig = perc_consig * 100;
            setupPWMPercentage(i, new_consig);
        } else {
            setupPWMPercentage(i, motors[i].consigne_percent);
        }
    }
}
