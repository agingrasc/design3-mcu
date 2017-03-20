#ifndef DESIGN3_MCU_MANCHESTER_H
#define DESIGN3_MCU_MANCHESTER_H

#include <stdint.h>

#define MAN_ERR_NO_VALID_LOGIC_LEVEL    -1
#define MAN_ERR_SPURIOUS_LEVEL          -2
#define MAN_ERR_PATTERN_NOT_FOUND       -3
#define MAN_ERR_CODE_TOO_LONG           -4
#define MAN_ERR_DUMB_ERROR              -5
#define MAN_ERR_INVALID_CODE            -6

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
