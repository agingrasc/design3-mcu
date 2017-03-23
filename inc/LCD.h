/*
 * LCD.h
 *
 *  Created on: Nov 25, 2016
 *      Author: dark
 */

#ifndef LCD_H_
#define LCD_H_

#include "manchester.h"

#define MAX_COLS    16 // Maximum LCD screen columns

void lcd_init();

void lcd_send(uint8_t rs, uint8_t cmd);

void lcd_set_cursor(uint8_t row, uint8_t col);

void lcd_clear_row(uint8_t row);

void lcd_putc(char ch);

void lcd_update_display(ManchesterInfo *infos);

#endif /* LCD_H_ */
