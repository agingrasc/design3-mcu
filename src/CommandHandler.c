// CommandHandler.c

#include "CommandHandler.h"

void cmdHandlerInit(void) {
    PID_mode = 0;
}

int handleCmd(uint32_t p_cmd) {
    /** Gère les commandes entrantes **/
    //if(!checkSumCmd(p_cmd)) return -1;
    if (switchCmd(p_cmd)) return -2;
    return 0;
}

int checkSumCmd(uint32_t p_cmd) {
    uint32_t checknumber = getInstruction(p_cmd) + getParam(p_cmd) + getCheck(p_cmd);
    return (checknumber & 0xFF) == 0;
}

uint16_t cur = 0;

int switchCmd(uint32_t p_cmd) {
    uint32_t tmp_motor_speed;
    uint32_t instr = getInstruction(p_cmd);
    uint32_t param = getParam(p_cmd);
    uint32_t ckc = getCheck(p_cmd);
    int j, k;
    uint8_t buf[2 * ID_VAL_COUNT];
    uint16_t *ta;
    switch (getInstruction(p_cmd)) {
        case 0x0F:
            //uart_write_byte(0x0F);
            TM_USB_VCP_Putc(0x0F);
            break;
        case 0x55:
            tmp_motor_speed = motors[current_motor].motor_speed;
            if (tmp_motor_speed > 0xFF) { tmp_motor_speed = 0xFF; }
            //uart_write_byte(tmp_motor_speed);
            TM_USB_VCP_Putc(tmp_motor_speed);
            break;
        case 0x0A:
            PID_mode = getParam(p_cmd) & 0x1;
            break;
        case 0x10:
            if (PID_mode == 0) {
                motors[current_motor].consigne_percent = getParam(p_cmd); //consigne_percent = getParam(p_cmd);
            }
        case 0xaa:
            //uart_write_byte(motors[current_motor].input_consigne);
            TM_USB_VCP_Putc(motors[current_motor].input_consigne);
            break;
        case 0xF0:
            motors[current_motor].input_consigne = (char) getParam(p_cmd);
            break;
#ifdef ID_MODE
        case 0xBB:
            // Init stuff for dynamic identification test
            initIdTest();
            break;
        case 0xCC:
            // Start dynamic identification test
            startIdTest();

            break;
        case 0x60:
            TM_USB_VCP_Putc(id_val_consigne[param]);
            break;
        case 0x58:
            // Request consigne buffer
            //uart_write_buffer((char *)id_val_consigne, ID_VAL_COUNT);
            k = 0;

            for (k = 0; k < ID_VAL_COUNT; k++) {
                // big endian
                //buf[k * 2] = (id_val_consigne[k] >> 8) & 0xFF;
                //buf[k * 2 + 1] = id_val_consigne[k] & 0xFF;
                // little endian
                buf[k * 2] = id_val_consigne[k] & 0xFF;
                buf[k * 2 + 1] = (id_val_consigne[k] >> 8) & 0xFF;
            }
            for (k = 0; k < 2 * ID_VAL_COUNT; k++) {
                TM_USB_VCP_Putc((char) buf[k]);
                delay(10);
            }
            break;
        case 0xEE:
            // Request response buffer
            k = 0;
            //uart_write_buffer((char *)id_val_reponse, ID_VAL_COUNT);
            k = 0;

            for (k = 0; k < ID_VAL_COUNT; k++) {
                // big endian
                //buf[k * 2] = (id_val_consigne[k] >> 8) & 0xFF;
                //buf[k * 2 + 1] = id_val_consigne[k] & 0xFF;
                // little endian
                buf[k * 2] = id_val_reponse[k] & 0xFF;
                buf[k * 2 + 1] = (id_val_reponse[k] >> 8) & 0xFF;
            }
            for (k = 0; k < 2 * ID_VAL_COUNT; k++) {
                TM_USB_VCP_Putc((char) buf[k]);
                delay(10);
            }
            break;
#endif
        default:
            return -1;
    }
    return 0;
}

uint32_t getInstruction(uint32_t p_cmd) {
    return p_cmd >> 16;
}

uint32_t getParam(uint32_t p_cmd) {
    return (p_cmd >> 8) & 0xFF;
}

uint32_t getCheck(uint32_t p_cmd) {
    return p_cmd & 0xFF;
}
