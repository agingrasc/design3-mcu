#include <sched.h>
#include <stm32f4xx_conf.h>
#include <tm_stm32f4_usb_vcp.h>
#include <delay.h>
#include <string.h>
#include "command.h"

#define MOVE_CMD 0x00
#define CAMERA_CMD 0x01
#define PENCIL_CMD 0x02
#define LED_CMD 0x03
#define SET_PID_CONSTANT 0x04
#define MANUAL_SPEED_CMD 0xa0
#define READ_ENCODER 0xa1
#define SET_PID_MODE 0xa2
#define TEST_PID 0xa3

#define GREEN_LED GPIO_Pin_15
#define RED_LED GPIO_Pin_14

#define PID_SCALING 100000

uint16_t read_uint16(char* arg) {
    uint16_t data = 0;
    memcpy(&data, arg, 2);
    return data;
}

void cmd_led(command *cmd) {
    switch (cmd->payload[0]) {
        case 0:
            GPIO_SetBits(GPIOD, RED_LED);
            TM_USB_VCP_Putc(CMD_EXECUTE_OK);
            break;
        case 1:
            GPIO_SetBits(GPIOD, GREEN_LED);
            TM_USB_VCP_Putc(CMD_EXECUTE_OK);
            break;
        case 2:
            GPIO_ResetBits(GPIOD, RED_LED);
            TM_USB_VCP_Putc(CMD_EXECUTE_OK);
            break;
        case 3:
            GPIO_ResetBits(GPIOD, GREEN_LED);
            TM_USB_VCP_Putc(CMD_EXECUTE_OK);
            break;
        case 4:
            GPIO_SetBits(GPIOD, RED_LED);
            delay(1000);
            GPIO_ResetBits(GPIOD, RED_LED);
            TM_USB_VCP_Putc(CMD_EXECUTE_OK);
            break;
        case 5:
            GPIO_SetBits(GPIOD, GREEN_LED);
            delay(1000);
            GPIO_ResetBits(GPIOD, GREEN_LED);
            TM_USB_VCP_Putc(CMD_EXECUTE_OK);
            break;
        default:
            TM_USB_VCP_Putc(CMD_EXECUTE_FAILURE);
            break;
    }
}

void cmd_move(command* cmd) {
    short* payload = cmd->payload;
    short x = payload[0]; //mm/s
    short y = payload[1]; //mm/s
    short t = payload[2]; //TBD

    // transformer la vitesse mm/s en tick/s
    float tick_per_militer = TICK_PER_ROT / (2 * WHEEL_RADIUS * PI);
    float x_tick = tick_per_militer * x;
    float y_tick = tick_per_militer * y;

    // on distribue la rotation en creant des differentiels en x et y
    short partial_t = t/4;

    // Les moteurs FRONT recoivent le diff negatif par convention arbitraire
    pid_setpoint(0, x_tick + partial_t); // REAR_X
    pid_setpoint(2, x_tick - partial_t); // FRONT_X
    pid_setpoint(3, y_tick + partial_t); // REAR_Y
    pid_setpoint(1, y_tick - partial_t); // FRONT_Y

    TM_USB_VCP_Putc(CMD_EXECUTE_OK);
}

int cmd_manual_speed(command *cmd) {
    short* payload = cmd->payload;
    short motor_id = payload[0];
    short pwm = payload[1];
    short direction = payload[2];

    uint8_t dir = MC_DIR_BGND;
    if (direction == 0 && (motor_id == 2 || motor_id == 3)) {
        dir = MC_DIR_CW;
    }
    else if (direction == 0 && (motor_id == 0 || motor_id == 1)) {
        dir = MC_DIR_CCW;
    }
    else if (direction == 1 && (motor_id == 2 || motor_id == 3)) {
        dir = MC_DIR_CCW;
    }
    else if (direction == 1 && (motor_id == 0 || motor_id == 1)) {
        dir = MC_DIR_CW;
    }

    motorSetDirection(motor_id, dir);
    motors[motor_id].consigne_percent = pwm;

    TM_USB_VCP_Putc(CMD_EXECUTE_OK);
}

int cmd_read_encoder(command *cmd) {
    short motor = cmd->payload[0];
    int16_t speed = (int16_t) motors[motor].motor_speed;
    char high = (speed >> 8) & 0xff;
    char low = speed & 0xff;
    TM_USB_VCP_Putc(high);
    TM_USB_VCP_Putc(low);
    TM_USB_VCP_Putc(CMD_EXECUTE_OK);
}

int cmd_set_pid_mode(command *cmd) {
    short status = cmd->payload[0];
    PID_mode = status;
    TM_USB_VCP_Putc(CMD_EXECUTE_OK);
    return 0;
}

int cmd_set_pid_constant(command *cmd) {
    short motor = cmd->payload[0];
    short kp = cmd->payload[1];
    short ki = cmd->payload[2];
    short kd = cmd->payload[3];

    PIDData* pid = &PID_data[motor];
    pid->kp = ((float) kp)/PID_SCALING;
    pid->ki = ((float) ki)/PID_SCALING;
    pid->kd = ((float) kd)/PID_SCALING;

    TM_USB_VCP_Putc(CMD_EXECUTE_OK);
    return 0;
}

int cmd_test_pid(command *cmd) {

    short motor = cmd->payload[0];
    short delta_t = cmd->payload[1];
    short current_speed = cmd->payload[2];

    PIDData *pid = &PID_data[motor];
    float target_speed = motors[motor].input_consigne;
    int output = pid_compute_cmd(pid, 0, delta_t, target_speed, current_speed);
    TM_USB_VCP_Putc(output & 0xff);
    TM_USB_VCP_Putc(CMD_EXECUTE_OK);
    return 0;
}

int command_execute(command *cmd) {
    switch (cmd->header.type) {
        case (uint8_t) MOVE_CMD:
            cmd_move(cmd);
            break;
        case (uint8_t) CAMERA_CMD:
            //call move camera angle payload[0], payload[1]
            break;
        case (uint8_t) PENCIL_CMD:
            //call raise/lower pencil payload[0]
            break;
        case (uint8_t) LED_CMD:
            cmd_led(cmd);
            break;
        case (uint8_t) SET_PID_CONSTANT:
            cmd_set_pid_constant(cmd);
            break;
        case (uint8_t) MANUAL_SPEED_CMD:
            cmd_manual_speed(cmd);
            break;
        case (uint8_t) READ_ENCODER:
            cmd_read_encoder(cmd);
            break;
        case (uint8_t) SET_PID_MODE:
            cmd_set_pid_mode(cmd);
            break;
        case (uint8_t) TEST_PID:
            cmd_test_pid(cmd);
        default:
            break;
    }
    return 0;
}

int checksum_header(headerData *header) {
    uint8_t checksum = header->size + header->type + header->checksum;
    if (!checksum) {
        return 0;
    }
    return 1;
}
