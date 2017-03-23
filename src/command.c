#include <sched.h>
#include <stm32f4xx_conf.h>
#include <tm_stm32f4_usb_vcp.h>
#include <delay.h>
#include <string.h>
#include <util.h>
#include "command.h"
#include "leds.h"
#include "adc.h"
#include "manchester.h"
#include "LCD.h"

#define MOVE_CMD 0x00
#define CAMERA_CMD 0x01
#define PENCIL_CMD 0x02
#define LED_CMD 0x03
#define SET_PID_CONSTANT 0x04
#define MANUAL_SPEED_CMD 0xa0
#define READ_ENCODER 0xa1
#define SET_PID_MODE 0xa2
#define TEST_PID 0xa3
#define READ_PID_LAST_CMD   0xa4
#define READ_ADC_VALUE      0xa5
#define DECODE_MANCHESTER_CMD      0xb1
#define GET_MANCHESTER_POWER_CMD    0xb2

#define CMD_LED_SET_RED         0
#define CMD_LED_SET_GREEN       1
#define CMD_LED_RESET_RED       2
#define CMD_LED_RESET_GREEN     3
#define CMD_LED_TOGGLE_RED      4
#define CMD_LED_TOGGLE_GREEN    5
#define CMD_LED_SET_BLUE        6
#define CMD_LED_RESET_BLUE      7
#define CMD_LED_TOGGLE_BLUE     8

#define BLUE_LED GPIO_Pin_15

#define PID_SCALING 100000

uint16_t read_uint16(char* arg) {
    uint16_t data = 0;
    memcpy(&data, arg, 2);
    return data;
}

void cmd_get_manchester_power(command *cmd) {
    uint16_t signal[CONVERSIONS_NUMBER_PER_CHANNEL];
    char high, low;

    //adc_get_channel_conversion_values(ADC_MANCHESTER_CODE_POWER, signal);
    uint16_t last_value = adc_perform_injected_conversion();
    //uint16_t last_value = signal[0]; // TODO: really last sampled value?

    high = (last_value >> 8) & 0xff;
    low = last_value & 0xff;

    TM_USB_VCP_Putc(high);
    TM_USB_VCP_Putc(low);

    TM_USB_VCP_Putc(CMD_EXECUTE_OK);
}

void cmd_decode_manchester(command *cmd) {
    uint16_t signal[CONVERSIONS_NUMBER_PER_CHANNEL];
    uint8_t code[MANCHESTER_N_DATA_BITS];
    char high, low;

    adc_get_channel_conversion_values(ADC_MANCHESTER_CODE, signal);

    ManchesterInfo info;
    uint8_t res = (uint8_t)decode(signal, CONVERSIONS_NUMBER_PER_CHANNEL, &info, code);

    // Send decoding success result
    TM_USB_VCP_Putc(res);

    // Send figure #
    TM_USB_VCP_Putc(info.figNum);

    // Send orientation
    TM_USB_VCP_Putc((uint8_t)info.figOrientation);

    // Send scale
    TM_USB_VCP_Putc((uint8_t)info.figScale);

    // Update LCD with values if succeeded
    if (res == 0) {
        lcd_update_display(&info);
    }

    TM_USB_VCP_Putc(CMD_EXECUTE_OK);
}

void cmd_read_adc_value(command *cmd) {
    uint16_t vals[CONVERSIONS_NUMBER_PER_CHANNEL];
    uint16_t nval; // Number of values that will be sent
    char high, low;

    switch (cmd->payload[0]) {
        case ADC_MANCHESTER_CODE_POWER:
            adc_get_channel_conversion_values(ADC_MANCHESTER_CODE_POWER, vals);

            // Send number of values
            nval = 1;
            high = (nval >> 8) & 0xff;
            low = nval & 0xff;
            TM_USB_VCP_Putc(high);
            TM_USB_VCP_Putc(low);

            // Send last value
            high = (vals[0] >> 8) & 0xff; // TODO: return the last index instead, which would be the latest sampled value?
            low = vals[0] & 0xff;
            TM_USB_VCP_Putc(high);
            TM_USB_VCP_Putc(low);

            TM_USB_VCP_Putc(CMD_EXECUTE_OK);
            break;
        case ADC_MANCHESTER_CODE:
            adc_get_channel_conversion_values(ADC_MANCHESTER_CODE, vals);

            // Send number of values
            nval = CONVERSIONS_NUMBER_PER_CHANNEL;
            high = (nval >> 8) & 0xff; // TODO: return the last index instead, which would be the latest sampled value?
            low = nval & 0xff;
            TM_USB_VCP_Putc(high);
            TM_USB_VCP_Putc(low);

            // Send values
            for (int i = 0; i < nval; i++) {
                high = (vals[i] >> 8) & 0xff;
                low = vals[i] & 0xff;

                TM_USB_VCP_Putc(high);
                TM_USB_VCP_Putc(low);
            }

            TM_USB_VCP_Putc(CMD_EXECUTE_OK);
            break;
        case ADC_PENCIL:
            adc_get_channel_conversion_values(ADC_PENCIL, vals);

            // Send number of values
            nval = 1;
            high = (nval >> 8) & 0xff;
            low = nval & 0xff;
            TM_USB_VCP_Putc(high);
            TM_USB_VCP_Putc(low);

            // Send last value
            high = (vals[0] >> 8) & 0xff; // TODO: return the last index instead, which would be the latest sampled value?
            low = vals[0] & 0xff;
            TM_USB_VCP_Putc(high);
            TM_USB_VCP_Putc(low);

            TM_USB_VCP_Putc(CMD_EXECUTE_OK);
            break;
        default:
            TM_USB_VCP_Putc(CMD_EXECUTE_FAILURE);
            break;
    }
}

void cmd_led(command *cmd) {
    switch (cmd->payload[0]) {
        case CMD_LED_SET_RED:
            set_robot_red_led();
            TM_USB_VCP_Putc(CMD_EXECUTE_OK);
            break;
        case CMD_LED_SET_GREEN:
            set_robot_green_led();
            TM_USB_VCP_Putc(CMD_EXECUTE_OK);
            break;
        case CMD_LED_RESET_RED:
            reset_robot_red_led();
            TM_USB_VCP_Putc(CMD_EXECUTE_OK);
            break;
        case CMD_LED_RESET_GREEN:
            reset_robot_green_led();
            TM_USB_VCP_Putc(CMD_EXECUTE_OK);
            break;
        case CMD_LED_TOGGLE_RED:
            set_robot_red_led();
            delay(1000);
            reset_robot_red_led();
            TM_USB_VCP_Putc(CMD_EXECUTE_OK);
            break;
        case CMD_LED_TOGGLE_GREEN:
            set_robot_green_led();
            delay(1000);
            reset_robot_green_led();
            TM_USB_VCP_Putc(CMD_EXECUTE_OK);
            break;
        case CMD_LED_SET_BLUE:
            GPIO_SetBits(GPIOD, BLUE_LED);
            TM_USB_VCP_Putc(CMD_EXECUTE_OK);
            break;
        case CMD_LED_RESET_BLUE:
            GPIO_ResetBits(GPIOD, BLUE_LED);
            TM_USB_VCP_Putc(CMD_EXECUTE_OK);
            break;
        case CMD_LED_TOGGLE_BLUE:
            GPIO_SetBits(GPIOD, BLUE_LED);
            delay(1000);
            GPIO_ResetBits(GPIOD, BLUE_LED);
            TM_USB_VCP_Putc(CMD_EXECUTE_OK);
            break;
        default:
            TM_USB_VCP_Putc(CMD_EXECUTE_FAILURE);
            break;
    }
}

void cmd_move(command* cmd) {
    last_move_timestamp = timestamp;
    short* payload = cmd->payload;

    float tick_per_militer = TICK_PER_ROT / (2 * WHEEL_RADIUS * PI);

    for (int i = 0; i < MOTOR_COUNT; i++) {
        short speed = payload[i];
        float ticks = tick_per_militer * speed;
        pid_setpoint(i, ticks);
    }

    TM_USB_VCP_Putc(CMD_EXECUTE_OK);
}

int cmd_manual_speed(command *cmd) {
    short* payload = cmd->payload;
    short motor_id = payload[0];
    short pwm = payload[1];
    short direction = payload[2];

    uint8_t dir = MC_DIR_BGND;
    if (direction == 0 && (motor_id == 2 || motor_id == 3)) {
        dir = MC_DIR_CW;
    }
    else if (direction == 0 && (motor_id == 0 || motor_id == 1)) {
        dir = MC_DIR_CCW;
    }
    else if (direction == 1 && (motor_id == 2 || motor_id == 3)) {
        dir = MC_DIR_CCW;
    }
    else if (direction == 1 && (motor_id == 0 || motor_id == 1)) {
        dir = MC_DIR_CW;
    }

    motor_set_direction(motor_id, pwm);
    motors[motor_id].consigne_percent = abs(pwm);

    TM_USB_VCP_Putc(CMD_EXECUTE_OK);
}

int cmd_read_encoder(command *cmd) {
    short motor = cmd->payload[0];
    int16_t speed = (int16_t) motors[motor].motor_speed;
    char high = (speed >> 8) & 0xff;
    char low = speed & 0xff;
    TM_USB_VCP_Putc(high);
    TM_USB_VCP_Putc(low);
    TM_USB_VCP_Putc(CMD_EXECUTE_OK);
}

int cmd_set_pid_mode(command *cmd) {
    short status = cmd->payload[0];
    PID_mode = status;
    TM_USB_VCP_Putc(CMD_EXECUTE_OK);
    return 0;
}

int cmd_set_pid_constant(command *cmd) {
    short motor = cmd->payload[0];
    short kp = cmd->payload[1];
    short ki = cmd->payload[2];
    short kd = cmd->payload[3];
    short dz = cmd->payload[4];

    PIDData* pid = &PID_data[motor];
    pid->kp = ((float) kp)/PID_SCALING;
    pid->ki = ((float) ki)/PID_SCALING;
    pid->kd = ((float) kd)/PID_SCALING;
    pid->deadzone = dz;

    TM_USB_VCP_Putc(CMD_EXECUTE_OK);
    return 0;
}

int cmd_test_pid(command *cmd) {

    short motor = cmd->payload[0];
    short delta_t = cmd->payload[1];
    short current_speed = cmd->payload[2];

    PIDData *pid = &PID_data[motor];
    float target_speed = motors[motor].input_consigne;
    int output = pid_compute_cmd(pid, 0, delta_t, target_speed, current_speed);
    TM_USB_VCP_Putc(output & 0xff);
    TM_USB_VCP_Putc(CMD_EXECUTE_OK);
    return 0;
}

int cmd_read_pid_last_cmd(command *cmd) {
    short motor = cmd->payload[0];
    int16_t last_command = (int16_t) PID_data[motor].last_command;
    char high = (last_command >> 8) & 0xff;
    char low = last_command & 0xff;
    TM_USB_VCP_Putc(high);
    TM_USB_VCP_Putc(low);
    TM_USB_VCP_Putc(CMD_EXECUTE_OK);
}

int command_execute(command *cmd) {
    switch (cmd->header.type) {
        case (uint8_t) MOVE_CMD:
            cmd_move(cmd);
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
        case (uint8_t) SET_PID_CONSTANT:
            cmd_set_pid_constant(cmd);
            break;
        case (uint8_t) MANUAL_SPEED_CMD:
            cmd_manual_speed(cmd);
            break;
        case (uint8_t) READ_ENCODER:
            cmd_read_encoder(cmd);
            break;
        case (uint8_t) SET_PID_MODE:
            cmd_set_pid_mode(cmd);
            break;
        case (uint8_t) TEST_PID:
            cmd_test_pid(cmd);
            break;
        case (uint8_t) READ_PID_LAST_CMD:
            cmd_read_pid_last_cmd(cmd);
            break;
        case (uint8_t) READ_ADC_VALUE:
            cmd_read_adc_value(cmd);
            break;
        case (uint8_t) DECODE_MANCHESTER_CMD:
            cmd_decode_manchester(cmd);
            break;
        case (uint8_t) GET_MANCHESTER_POWER_CMD:
            cmd_get_manchester_power(cmd);
            break;
        default:
            break;
    }
    return 0;
}

int checksum_header(headerData *header) {
    uint8_t checksum = header->size + header->type + header->checksum;
    if (!checksum) {
        return 0;
    }
    return 1;
}
