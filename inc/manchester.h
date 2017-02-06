#ifndef DESIGN3_MCU_MANCHESTER_H
#define DESIGN3_MCU_MANCHESTER_H

#include <stdint.h>

typedef enum Orientation {
    NORTH = 0,
    EAST = 1,
    SOUTH = 2,
    WEST = 3
} Orientation;

typedef enum Scale {
    X2 = 0,
    X4 = 1
} Scale;

typedef struct ManchesterInfo {
    uint32_t figNum;
    Orientation figOrientation;
    Scale figScale;
} ManchesterInfo;

ManchesterInfo decode();
#endif //DESIGN3_MCU_MANCHESTER_H
