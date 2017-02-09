#include <sched.h>
#include "command.h"

#define MOVE_CMD 0x00
#define CAMERA_CMD 0x01
#define PENCIL_CMD 0x02
#define LED_CMD 0x03

int command_execute(command cmd) {
    switch (cmd.header.type) {
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
            //call switch on led payload[0]
            break;
        default:
            break;
    }
}
