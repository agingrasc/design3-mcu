#ifndef DESIGN3_MCU_COMMAND_H
#define DESIGN3_MCU_COMMAND_H

typedef struct headerData {
    uint8_t type;
    uint8_t size;
} headerData;

typedef struct command {
    headerData header;
    char payload[256];
} command;

int command_execute(command);

#endif //DESIGN3_MCU_COMMAND_H
