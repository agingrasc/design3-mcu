#ifndef UART_H
#define UART_H
#include "misc.h"
#include "stm32f4xx_gpio.h"
#include "stm32f4xx_usart.h"

void init_uart(uint32_t);
void uart_write_byte(volatile char);
void uart_write_buffer(char*,int);
uint32_t uart_read_cmd();
char uart_read_byte();
int uart_available_bytes();
void USART2_Handler();

#endif
