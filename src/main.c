// main.c

#include "main.h"
#include "adc.h"

#define MOVE_DELTA_T_THRESHOLD 500

void initLed() {
    RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOD, ENABLE);

    GPIO_InitTypeDef GPIO_InitStructure;
    GPIO_InitStructure.GPIO_Pin = GPIO_Pin_12 | GPIO_Pin_13 | GPIO_Pin_14 | GPIO_Pin_15;
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_OUT;
    GPIO_InitStructure.GPIO_Speed = GPIO_Speed_100MHz;
    GPIO_InitStructure.GPIO_OType = GPIO_OType_PP;
    GPIO_InitStructure.GPIO_PuPd = GPIO_PuPd_NOPULL;
    GPIO_Init(GPIOD, &GPIO_InitStructure);
    GPIO_ResetBits(GPIOD, GPIO_Pin_12 | GPIO_Pin_13 | GPIO_Pin_14 | GPIO_Pin_15);
}

void checkForVCP() {
    /* USB configured OK, drivers OK */
    TM_USB_VCP_Result res = TM_USB_VCP_GetStatus();
    if (res == TM_USB_VCP_CONNECTED) {
        /* Turn on GREEN led */
        GPIO_ResetBits(GPIOD, GPIO_Pin_14);
        GPIO_SetBits(GPIOD, GPIO_Pin_12);
        /* If something arrived at VCP */

        /*char buffer[5];
          uint16_t len = TM_USB_VCP_Gets(buffer, 5);
          if (len > 0)
          TM_USB_VCP_Puts(buffer);*/
    } else {
        /* USB not OK */
        GPIO_ResetBits(GPIOD, GPIO_Pin_12);
        GPIO_SetBits(GPIOD, GPIO_Pin_14);
    }
}

int main() {
    initLed();
    /* Initialize USB virtual COM port */
    TM_USB_VCP_Init();
    motor_controller_init();
    MotorEncodersInit();
    initDelay();
    initTimer();
    lcd_init();
    pid_init();
    init_robot_leds();
    adc_init();

    reset_robot_green_led();
    reset_robot_red_led();

#ifdef ID_MODE
    id_test_status = 0;
#endif

    last_move_timestamp = 0;
    int cmd_header_ok = 0;
    int cmd_payload_ok = 0;
    while (1) {
        // Check for VCP connection
        checkForVCP();

        command cmd;
        if (!cmd_header_ok && !TM_USB_VCP_BufferEmpty()) {
            char header[3];
            cmd_header_ok = usb_read_cmd_header(header);
            int valid_checksum = 1;
            if (cmd_header_ok == 3) {
                cmd.header.type = header[0];
                cmd.header.size = header[1];
                cmd.header.checksum = header[2];
                valid_checksum = checksum_header(&cmd.header);
            } else if (cmd_header_ok > 0) {
                usb_empty_buffer();
                //TM_USB_VCP_Putc(CMD_INVALID_HEADER);
            }

            if (!valid_checksum) {
                //TM_USB_VCP_Putc(CMD_RECEPTION_OK);
            } else {
                cmd_header_ok = 0;
                usb_empty_buffer();
                //TM_USB_VCP_Putc(CMD_CHECKSUM_FAILURE);
            }
        }

        if (cmd_header_ok && (!TM_USB_VCP_BufferEmpty() || cmd.header.size == 0)) {
            short payload[256];
            usb_read_cmd_payload(payload, cmd.header.size);
            cmd_payload_ok = 1;
            if (cmd_payload_ok) {
                for (int i = 0; i < cmd.header.size; i++) {
                    cmd.payload[i] = payload[i];
                }
            }
        }

        if (cmd_payload_ok) {
            command_execute(&cmd);
            cmd_header_ok = 0;
            cmd_payload_ok = 0;
        }

        uint32_t delta_t = timestamp - last_move_timestamp;
        if (delta_t > MOVE_DELTA_T_THRESHOLD) {
            for (int i = 0; i < MOTOR_COUNT; i++) {
                pid_setpoint(i, 0);
            }
        }
    }
}
