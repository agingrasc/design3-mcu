#include <sched.h>
#include <stm32f4xx_conf.h>
#include <tm_stm32f4_usb_vcp.h>
#include <delay.h>
#include "command.h"

#define MOVE_CMD 0x00
#define CAMERA_CMD 0x01
#define PENCIL_CMD 0x02
#define LED_CMD 0x03

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
    char* payload = cmd->payload;
    short x = 0;
    x |= (cmd->payload[0] & 0xff) << 8;
    x |= cmd->payload[1] & 0xff;

    short y = 0;
    y |= (cmd->payload[2] & 0xff) << 8;
    y |= (cmd->payload[3] & 0xff);

    short t = 0;
    t |= (cmd->payload[4] & 0xff) << 8;
    t |= (cmd->payload[5] & 0xff);

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
