#include <sched.h>
#include <stm32f4xx_conf.h>
#include <tm_stm32f4_usb_vcp.h>
#include "command.h"

#define MOVE_CMD 0x00
#define CAMERA_CMD 0x01
#define PENCIL_CMD 0x02
#define LED_CMD 0x03

#define GREEN_LED GPIO_Pin_15
#define RED_LED GPIO_Pin_14

void cmd_led(command* cmd) {
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
        default:
            TM_USB_VCP_Putc(CMD_EXECUTE_FAILURE);
            break;
    }
}

int command_execute(command* cmd) {
    switch (cmd->header.type) {
        case (uint8_t) MOVE_CMD:
            //call pid(cmd.payload[0], cmd.payload[1], cmd.payload[2], delta_t);
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
}

int checksum_header(headerData* header) {
    uint8_t checksum = header->size + header->type + header->checksum;
    if (!checksum) {
        return 0;
    }
    return 1;
}
