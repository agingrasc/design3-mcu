/*
 * HD44780U.h
 *
 *  Created on: Nov 25, 2016
 *      Author: dark
 */

#ifndef HD44780U_H_
#define HD44780U_H_

// Hitachi HD44780U LCD controller

#define INSTR_CMD	0
#define DATA_CMD	1

// Command address offsets
#define CMD_CLEAR_DISPLAY	0x1	//
#define CMD_RETURN_HOME		0x2 // 1.52 ms delay needed
#define CMD_ENTRY_MODESET	0x4 // 37 uS delay needed
#define CMD_DISPLAY_CTRL	0x8	// same
#define CMD_SHIFT_CTRL		0x10 // same
#define CMD_FUNCTION_SET	0x20 // same
#define CMD_SET_CGRAM		0x40 // same
#define CMD_SET_DDRAM		0x80

#define ENTRY_MODESET_ACC_DISP_SHIFT 0x1
#define ENTRY_MODESET_INCR			 0x2

#define DISPLAY_CTRL_BLINK	0x1
#define DISPLAY_CTRL_CURS	0x2
#define DISPLAY_CTRL_DISP	0x4

#define SHIFT_CTRL_RIGHT	0x4
#define SHIFT_CTRL_DISP		0x8

#define FUCNTION_SET_5x10	0x4
#define FUNCTION_SET_2LINES	0x8
#define FUNCTION_SET_8BITS	0x10

#define LINE2_ADDR_OFFSET	0x40




#endif /* HD44780U_H_ */
