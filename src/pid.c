// pid.c

#include <stdlib.h>
#include "pid.h"

#define P_GAIN 1
#define I_GAIN 0
#define MAX_COMMAND 85
#define MIN_COMMAND 35
#define DELTA_T_TIMESCALE 1000 //ms

#define MAX_SETPOINT 16767
#define MAX_TICK_PER_SECOND 12000


/**
 * Initialise le PID
 */
void pid_init(void) {
    // Init structure
    for (int current_motor = 0; current_motor < MOTOR_COUNT; current_motor++) {
        PID_data[current_motor].kp = P_GAIN;
        PID_data[current_motor].ki = I_GAIN;
        PID_data[current_motor].previous_input = 0;
        PID_data[current_motor].accumulator = 0;
        PID_data[current_motor].last_timestamp = 0;
    }
    PID_mode = 1;
}

void pid_setpoint(Motor *motor, short setpoint) {
    motor->input_consigne = setpoint;
}

/**
 * Boucle du PID de l'interruption
 */
void pid_update(void) {
    for (int i = 0; i < MOTOR_COUNT; i++) {
        uint32_t work_timestamp = timestamp;
        if (PID_mode) {
            uint32_t last_timestamp = PID_data[i].last_timestamp;
            short speed_cmd = pid_compute_cmd(&PID_data[i], last_timestamp, work_timestamp, motors[i].input_consigne,
                                              motors[i].motor_speed);
            int new_consig = (speed_cmd / MAX_COMMAND) * 100;
            setupPWMPercentage(i, new_consig);
        } else {
            setupPWMPercentage(i, motors[i].consigne_percent);
        }
    }
}

/**
 * Limite la commande
 */
float clamp_command(float naiveCommand) {
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
float clamp_accumulator(PIDData *pidData, float accVal) {
    int maxAccumulator = MAX_COMMAND / pidData->ki;
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

float relinearize_command(float cmd) {
    if (cmd > 0) {
        return cmd + MIN_COMMAND;
    } else {
        return cmd - MIN_COMMAND;
    }
}

/**
 * Calcul une commande de [0, 1] pour atteindre et maintenir la consigne.
 * Args:
 * - pidData -> struct des données du pid calculé
 * - delta_t -> le timestamp du systeme, doit respecter le DELTA_T_TIMESCALE
 * - target_speed -> la consigne en nombre de tick/s
 * - current_speed -> l'état actuel du plant en tick/s
 *
 * Return:
 * La commande -12000 à 12000 en nombre de tick par seconde
 */
short
pid_compute_cmd(PIDData *pidData, float last_timestamp, float timestamp, int target_speed, int current_speed) {
    float timescale = DELTA_T_TIMESCALE;
    float delta_t = ((float) (timestamp - last_timestamp) / timescale);
    int error = target_speed - current_speed;
    float pCmd = pidData->kp * error;
    float iCmd = pidData->accumulator + pidData->ki * error * delta_t;
    iCmd = clamp_accumulator(pidData, iCmd);

    float naiveCmd = pCmd + iCmd;
    float cmd = clamp_command(naiveCmd);

    cmd = relinearize_command(cmd);
    //sauvegarde donnee pour prochain calcul
    pidData->previous_input = current_speed;
    pidData->last_timestamp = timestamp;
    return (int) cmd;
}

