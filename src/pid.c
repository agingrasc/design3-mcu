// pid.c

#include <stdlib.h>
#include "pid.h"

#define P_GAIN 1
#define I_GAIN 0
#define MIN_PERCENTAGE 20
#define MAX_COMMAND 16767
#define MIN_COMMAND (MIN_PERCENTAGE * 16767 / 100)
#define DELTA_T_TIMESCALE 1000 //ms

#define MAX_SETPOINT 16767
#define MAX_TICK_PER_SECOND 12000

short pid_compute_cmd(PIDData*, uint32_t, int, int);

/**
 * Initialise le PID
 */
void pidInit(void) {
    // Init structure
    PID_data[current_motor].proportionalGain = P_GAIN;
    PID_data[current_motor].integralGain = I_GAIN;
    PID_data[current_motor].previousInput = 0;
    PID_data[current_motor].accumulator = 0;
    PID_data[current_motor].lastTimestamp = 0;
    PID_mode = 1;
}

void pid_setpoint(Motor *motor, short setpoint) {
    motor->input_consigne = (setpoint / MAX_SETPOINT) * MAX_TICK_PER_SECOND;
}

/**
 * Boucle du PID de l'interruption
 */
void updatePID(void) {
    for (int i = 0; i < MOTOR_COUNT; i++) {
        uint32_t work_timestamp = timestamp;
        if (PID_mode) {
            short speed_cmd = pid_compute_cmd(&PID_data[i], work_timestamp, motors[i].input_consigne,
                                              motors[i].motor_speed);
            uint32_t new_consig = (speed_cmd / MAX_COMMAND) * 100;
            setupPWMPercentage(i, new_consig);
        }
        else {
            setupPWMPercentage(i, motors[i].consigne_percent);
        }
    }
}

/**
 * Limite la commande
 */
float clampCommand(short naiveCommand) {
    if (naiveCommand > MAX_COMMAND) {
        return MAX_COMMAND;
    } else if (naiveCommand < -MAX_COMMAND) {
        return -MAX_COMMAND;
    } else {
        return naiveCommand;
    }
}

/**
 * Limite la valeur de l'accumulateur
 */
int clampAccumulator(PIDData *pidData, float accVal) {
    int maxAccumulator = MAX_COMMAND / pidData->integralGain;
    if (accVal > maxAccumulator) {
        pidData->accumulator = maxAccumulator;
        return maxAccumulator;
    } else if (accVal < -maxAccumulator) {
        pidData->accumulator = -maxAccumulator;
    } else {
        pidData->accumulator = accVal;
        return accVal;
    }
}

int relinearize_command(int cmd) {
    if (cmd > 0) {
        return cmd+MIN_COMMAND;
    }
    else {
        return cmd-MIN_COMMAND;
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
 * La commande -12000 à 12000 en nombre de tick par seconde
 */
short pid_compute_cmd(PIDData *pidData, uint32_t timestamp, int targetSpeed, int current_speed) {
    uint32_t delta_t = (timestamp - pidData->lastTimestamp) / DELTA_T_TIMESCALE;
    int error = targetSpeed - current_speed;
    int pCmd = pidData->proportionalGain * error;
    int iCmd = pidData->accumulator + pidData->integralGain * error * delta_t;
    iCmd = clampAccumulator(pidData, iCmd);

    int naiveCmd = pCmd + iCmd;
    int cmd = clampCommand(naiveCmd);

    cmd = relinearize_command(cmd);
    //sauvegarde donnee pour prochain calcul
    pidData->previousInput = current_speed;
    pidData->lastTimestamp = timestamp;
    return cmd;
}

