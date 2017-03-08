// main.c

#include "main.h"
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

void updateDisplay() {
    lcd_clear_row(0);
    lcd_set_cursor(0, 0);

    // Convert units to human readable units
    /*for (int i = 0; i < MOTOR_COUNT; i++) {
      uint32_t tmp = (motors[i].last_tick_delta * 60000 * WHEEL_RADIUS)/(motors[i].last_timestamp_delta * 6400);
      motors[i].motor_speed_rpm = tmp;
      }*/

    char buf1[16];
    buf1[15] = '\0';
    sprintf(buf1, "%d %d", motors[0].motor_speed, motors[1].motor_speed);
    for (int i = 0; i < 16; i++) {
        if (buf1[i] == '\0') break;
        lcd_putc(buf1[i]);
    }

    lcd_clear_row(1);
    lcd_set_cursor(1, 0);

    char buf2[16];
    buf2[15] = '\0';
    sprintf(buf2, "%d %d", motors[2].motor_speed, motors[3].motor_speed);
    for (int i = 0; i < 16; i++) {
        if (buf2[i] == '\0') break;
        lcd_putc(buf2[i]);
    }
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
    current_motor = 0;

    initLed();
    /* Initialize USB virtual COM port */
    TM_USB_VCP_Init();
    pid_init();
    motor_controller_init();
    MotorEncodersInit();
    initDelay();
    initTimer();
    //lcd_init();

#ifdef ID_MODE
    id_test_status = 0;
#endif

    unsigned int last_second = 0;

    int cmd_header_ok = 0;
    int cmd_payload_ok = 0;
    while (1) {
        // Check for VCP connection
        checkForVCP();
        //updateDisplay();

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
                TM_USB_VCP_Putc(CMD_INVALID_HEADER);
            }

            if (!valid_checksum) {
                TM_USB_VCP_Putc(CMD_RECEPTION_OK);
            } else {
                cmd_header_ok = 0;
                usb_empty_buffer();
                TM_USB_VCP_Putc(CMD_CHECKSUM_FAILURE);
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

        // Update time line, if necessary
        /*unsigned int mstemp = (unsigned int)(timestamp / 1000);
        if (mstemp != last_second) { // One second elapsed
            // FIXME: sprintf in updateDisplay() crashes the MCU
            updateDisplay(); // Update time on LCD
            last_second = mstemp;

        }*/
    }
}
