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
#define LCD_RW_PIN    5 // Pin number used for read/write

uint8_t col_remaining = MAX_COLS;

// Uses GPIOB[5:0] pins
void lcd_init() {
    GPIO_InitTypeDef GPIO_InitStructure;

    RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOB, ENABLE);

    GPIO_StructInit(&GPIO_InitStructure);
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_OUT;
    GPIO_InitStructure.GPIO_PuPd = GPIO_PuPd_NOPULL;

    // Motor A
    GPIO_InitStructure.GPIO_Pin = GPIO_Pin_0 | GPIO_Pin_1 | GPIO_Pin_2 | GPIO_Pin_3 | GPIO_Pin_4 | GPIO_Pin_5;
    GPIO_Init(GPIOB, &GPIO_InitStructure);

    // Enable clock for GPIOB port
    //RCC->AHB1ENR |= RCC_AHB1Periph_GPIOB;

    // Set GPIOB[5:0] as output
    //GPIOB->MODER = (uint32_t)0x555;

    // Disable pullup/downs for 5:0
    //GPIOB->PUPDR &= ~0xFFF;

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
    GPIOB->ODR &= ~0x3F; // Clear all outputs on 5:0

    GPIOB->ODR |= (rs << LCD_RS_PIN);
    GPIOB->ODR |= cmd;

    GPIOB->ODR |= (1 << LCD_RW_PIN);
    udelay(20);
    GPIOB->ODR &= ~(1 << LCD_RW_PIN);
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
