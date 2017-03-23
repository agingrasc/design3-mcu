#ifndef DESIGN3_MCU_COMMAND_H
#define DESIGN3_MCU_COMMAND_H

#include "pid.h"

#define CMD_RECEPTION_OK 0x00
#define CMD_CHECKSUM_FAILURE 0x10
#define CMD_INVALID_HEADER 0x11
#define CMD_INVALID_PAYLOAD 0x12
#define CMD_EXECUTE_OK 0x00
#define CMD_EXECUTE_FAILURE 0x20

#define MAX_PAYLOAD_SIZE 256

uint32_t last_move_timestamp = 0;

typedef struct headerData {
    uint8_t type;
    uint8_t size;
    uint8_t checksum;
} headerData;

typedef struct command {
    headerData header;
    short payload[MAX_PAYLOAD_SIZE];
} command;

/**
 * Execute une commande
 * @return 0
 */
int command_execute(command *);

/**
 * Valide le checksum du header
 * @return 0 si valide, 1 si invalide
 */
int checksum_header(headerData *);

#endif //DESIGN3_MCU_COMMAND_H
