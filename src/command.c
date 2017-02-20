#include <sched.h>
#include <stm32f4xx_conf.h>
#include <tm_stm32f4_usb_vcp.h>
#include <delay.h>
#include "command.h"

#define MOVE_CMD 0x00
#define CAMERA_CMD 0x01
#define PENCIL_CMD 0x02
#define LED_CMD 0x03
#define MANUAL_SPEED_CMD 0xa0
#define READ_ENCODER 0xa1
#define TOGGLE_PID 0xa2

#define GREEN_LED GPIO_Pin_15
#define RED_LED GPIO_Pin_14

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
            delay(1);
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
    short x = payload[0];
    short y = payload[1];
    short t = payload[2];

    // on distribue la rotation en creant des differentiels en x et y
    short partial_t = t/4;

    // FIXME: verifier que les bon moteurs recoivent les bonnes consignes
    pid_setpoint(&motors[0], x + partial_t);
    pid_setpoint(&motors[1], x - partial_t);
    pid_setpoint(&motors[2], y + partial_t);
    pid_setpoint(&motors[3], y - partial_t);

    TM_USB_VCP_Putc(CMD_EXECUTE_OK);
}

int cmd_manual_speed(command *cmd) {
    short* payload = cmd->payload;
    short motor_id = payload[0];
    short pwm = payload[1];
    short direction = payload[2];

    uint8_t dir = MC_DIR_BGND;
    if (direction == 0) {
        dir = MC_DIR_CW;
    }
    else if (direction == 1) {
        dir = MC_DIR_CCW;
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
        case (uint8_t) MANUAL_SPEED_CMD:
            cmd_manual_speed(cmd);
            break;
        case (uint8_t) READ_ENCODER:
            cmd_read_encoder(cmd);
            break;
        case (uint8_t) TOGGLE_PID:
            PID_mode = !PID_mode;
            break;
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
