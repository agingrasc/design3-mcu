#ifndef DESIGN3_MCU_COMMAND_H
#define DESIGN3_MCU_COMMAND_H

#define CMD_RECEPTION_OK 0x00

#define CMD_CHECKSUM_FAILURE 0x10
#define CMD_INVALID_HEADER 0x11
#define CMD_INVALID_PAYLOAD 0x12

#define CMD_EXECUTE_OK 0x00
#define CMD_EXECUTE_FAILURE 0x20

typedef struct headerData {
    uint8_t type;
    uint8_t size;
    uint8_t checksum;
} headerData;

typedef struct command {
    headerData header;
    char payload[256];
} command;

/**
 * Execute une commande
 * @return 0
 */
int command_execute(command*);

/**
 * Valide le checksum du header
 * @return 0 si valide, 1 si invalide
 */
int checksum_header(headerData*);

#endif //DESIGN3_MCU_COMMAND_H
