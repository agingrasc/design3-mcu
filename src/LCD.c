/*
 * LCD.c
 *
 *  Created on: Sep 30, 2016
 *      Author: dark
 */

#include "stm32f4xx.h"
#include "HD44780U.h"
#include "delay.h"
#include "LCD.h"

#define LCD_RS_PIN    4 // Pin number used for register select
#define LCD_RW_PIN    6 // Pin number used for read/write

uint8_t col_remaining = MAX_COLS;

#define GPIOCLKx	RCC_AHB1Periph_GPIOD
#define GPIOx		GPIOD

// Uses GPIOx[5:0] pins
void lcd_init() {
    GPIO_InitTypeDef GPIO_InitStructure;

    RCC_AHB1PeriphClockCmd(GPIOCLKx, ENABLE);

    GPIO_StructInit(&GPIO_InitStructure);
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_OUT;
    GPIO_InitStructure.GPIO_PuPd = GPIO_PuPd_NOPULL;

    // Motor A
    GPIO_InitStructure.GPIO_Pin = GPIO_Pin_0 | GPIO_Pin_1 | GPIO_Pin_2 | GPIO_Pin_3 | GPIO_Pin_4 | GPIO_Pin_6;
    GPIO_Init(GPIOx, &GPIO_InitStructure);

    // Enable clock for GPIOx port
    //RCC->AHB1ENR |= RCC_AHB1Periph_GPIOx;

    // Set GPIOx[5:0] as output
    //GPIOx->MODER = (uint32_t)0x555;

    // Disable pullup/downs for 5:0
    //GPIOx->PUPDR &= ~0xFFF;

    // Wait a little bit until stabilization
    delay(45);

    // Begin LCD init sequence. Don't know why have to send several times 0x3...
    lcd_send_4bits(0, 0x3);
    delay(5);
    lcd_send_4bits(0, 0x3);
    delay(5);
    lcd_send_4bits(0, 0x3);
    delay(5);
    lcd_send_4bits(0, 0x2); // sets 4bits operations
    udelay(100);

    // Configure the LCD as we want. The arguments speaks by themselves.
    lcd_send(INSTR_CMD, CMD_FUNCTION_SET | FUNCTION_SET_2LINES); // 0x28; sets two line display and 5x10 chars
    lcd_send(INSTR_CMD, CMD_DISPLAY_CTRL | DISPLAY_CTRL_DISP | DISPLAY_CTRL_CURS | DISPLAY_CTRL_BLINK); // 0xc
    lcd_send(INSTR_CMD, CMD_CLEAR_DISPLAY);

    delay(3);

    lcd_send(INSTR_CMD, CMD_ENTRY_MODESET | ENTRY_MODESET_INCR); // 0x6

    delay(5);
}

void lcd_send(uint8_t rs, uint8_t cmd) {
    // Sends a command to the LCD, either instruction or data depending on rs

    // Four bit mode: send the four first upper bits, then send the four lower bits
    lcd_send_4bits(rs, cmd >> 4);
    lcd_send_4bits(rs, cmd & 0x0F);
}

// 5                  0
// EN RS DB7 DB6 DB5 DB4
// RS 0 = instr, 1 = data
void lcd_send_4bits(uint8_t rs, uint8_t cmd) {
    GPIOx->ODR &= ~0x3F; // Clear all outputs on 5:0

    GPIOx->ODR |= (rs << LCD_RS_PIN);
    GPIOx->ODR |= cmd;

    GPIOx->ODR |= (1 << LCD_RW_PIN);
    udelay(20);
    GPIOx->ODR &= ~(1 << LCD_RW_PIN);
    udelay(20);
}

void lcd_set_cursor(uint8_t row, uint8_t col) {
    // Set the cursor on the specified row/col, starting from 0
    // Does not support LCD with more than 2 rows

    uint8_t base = 0;

    if (col > MAX_COLS) return; // invalid column

    col_remaining = MAX_COLS - col; // set remaining char on line

    if (row != 0) base = 0x40; // second row offset

    base += col;

    // SMI: set la drame à l'offset correspondant à la ligne/colonne
    // SMI: attention pour pas pogner des esdis!
    lcd_send(INSTR_CMD, CMD_SET_DDRAM | base);
}

void lcd_putc(char ch) {
    // Write character on screen

    if (col_remaining == 0) {
        return; // don't write char if no more space
    }

    lcd_send(DATA_CMD, (uint8_t) ch);
    col_remaining--;
}

void lcd_clear_row(uint8_t row) {
    // Clear the row the "cheap but working" way

    lcd_set_cursor(row, 0);

    uint8_t count;
    for (count = 0; count <= MAX_COLS; count++) {
        lcd_putc(' ');
    }

    lcd_set_cursor(row, 0);
}

void lcd_update_display(ManchesterInfo *infos) {
    lcd_clear_row(0);
    lcd_set_cursor(0, 0);

    // Convert units to human readable units
    /*for (int i = 0; i < MOTOR_COUNT; i++) {
      uint32_t tmp = (motors[i].last_tick_delta * 60000 * WHEEL_RADIUS)/(motors[i].last_timestamp_delta * 6400);
      motors[i].motor_speed_rpm = tmp;
      }*/


    char row1[16] = {"Figure #X"};
    row1[8] = infos->figNum%10+'0'; // Fig number
    row1[9] = '\0';

    char ori[5];
    switch (infos->figOrientation) {
        case NORTH:
            sprintf(ori, "NORD ");
            break;
        case EAST:
            sprintf(ori, "EST  ");
            break;
        case SOUTH:
            sprintf(ori, "SUD  ");
            break;
        case WEST:
            sprintf(ori, "OUEST");
            break;
    }
    ori[5] = '\0';

    char scale[2];
    switch (infos->figScale) {
        case X2:
            sprintf(scale, "X2");
            break;
        case X4:
            sprintf(scale, "X4");
            break;
    }
    scale[2] = '\0';

    for (int i = 0; i < 16; i++) {
        if (row1[i] == '\0') break;
        lcd_putc(row1[i]);
    }

    lcd_clear_row(1);
    lcd_set_cursor(1, 0);

    for (int i = 0; i < 5; i++) {
        lcd_putc(ori[i]);
    }
    lcd_putc(',');
    lcd_putc(' ');

    for (int i = 0; i < 2; i++) {
        lcd_putc(scale[i]);
    }
}