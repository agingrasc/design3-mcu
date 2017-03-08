// pid.c

#include "pid.h"

#define P_GAIN 0
#define I_GAIN 0
#define MAX_COMMAND 85
#define MIN_COMMAND 35
#define DELTA_T_TIMESCALE 1000 //ms

#define MAX_SETPOINT 16767
#define MAX_TICK_PER_SECOND 12000

int abs(float p) {
    if (p < 0) {
        return (int) p * -1;
    }
    else {
        return (int) p;
    }
}


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

void pid_setpoint(int motor_idx, float setpoint) {
    Motor *motor = &motors[motor_idx];
    PIDData *pid = &PID_data[motor_idx];
    int new_consigne = setpoint;
    int old_consigne = motor->input_consigne;
    motor->input_consigne = setpoint;

    // on reset l'accumulateur si la consigne a change
    if (abs(new_consigne - old_consigne) > 10) {
        pid->accumulator = 0;
    }
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
            motor_set_direction(i, new_consig);
            motor_set_pwm_percentage(i, abs(new_consig));
        } else {
            motor_set_pwm_percentage(i, motors[i].consigne_percent);
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
    if (cmd > 1 && cmd < MIN_COMMAND) {
        return MIN_COMMAND;
    }
    else if (cmd < -1 && cmd > -MIN_COMMAND) {
        return -MIN_COMMAND;
    }
    else if (cmd < 1 && cmd > -1) {
        return 0;
    }
    else {
        return cmd;
    }
}

/**
 * Calcul une commande de [-100, 100] pour atteindre et maintenir la consigne.
 * Args:
 * - pid_data -> struct des données du pid calculé
 * - delta_t -> le timestamp du systeme, doit respecter le DELTA_T_TIMESCALE
 * - target_speed -> la consigne en nombre de tick/s
 * - current_speed -> l'état actuel du plant en tick/s
 *
 * Return:
 * La commande -12000 à 12000 en nombre de tick par seconde
 */
short
pid_compute_cmd(PIDData *pid_data, float last_timestamp, float timestamp, float target_speed, int32_t current_speed) {
    float timescale = DELTA_T_TIMESCALE;
    float delta_t = (timestamp - last_timestamp) / timescale;
    int error = target_speed - current_speed;
    float pCmd = pid_data->kp * error;
    float iCmd = pid_data->accumulator + pid_data->ki * error * delta_t;
    iCmd = clamp_accumulator(pid_data, iCmd);

    float naiveCmd = pCmd + iCmd;
    float cmd = relinearize_command(naiveCmd);
    cmd = clamp_command(cmd);

    //sauvegarde donnee pour prochain calcul
    pid_data->previous_input = current_speed;
    pid_data->last_timestamp = timestamp;
    return (int) cmd;
}

