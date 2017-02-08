#include "uart.h"

#define RING_BUFFER_SIZE 256

//buffer circulaire d'octets
char ring_buffer[RING_BUFFER_SIZE];
//tête d'écriture pour la réception
int write_idx;
//tête d'écriture pour la réception
int read_idx;
//NB: nous n'utilisons pas de buffer ciruclaire pour l'envoie, uniquement pour la réception

#define USARTx	USART1

#define UART_BAUDRATE	19200

/**
 * Init le matériel pour utiliser le USART1
 * documentation: https://github.com/g4lvanix/STM32F4-examples/blob/master/USART/main.c
 */
void init_uart(uint32_t baudrate)
{
    // set buffer and idx buffer
    write_idx = 0;
    read_idx = 0;
    int i;
    for(i = 0; i < RING_BUFFER_SIZE; i++)
        ring_buffer[i] = (char)0x00;

    //PIN: B6 - TX || B7 - RX (old)
    //PIN: A2 - TX || A3 - RX (old)
    //PIN: PC10 - TX | PC11 - RX
    GPIO_InitTypeDef GPIO_InitStruct;
    GPIO_InitStruct.GPIO_Pin = GPIO_Pin_6 | GPIO_Pin_7;
    GPIO_InitStruct.GPIO_Mode = GPIO_Mode_AF;
    GPIO_InitStruct.GPIO_Speed = GPIO_Speed_50MHz;
    GPIO_InitStruct.GPIO_OType = GPIO_OType_PP;
    GPIO_InitStruct.GPIO_PuPd = GPIO_PuPd_UP;
    GPIO_Init(GPIOB, &GPIO_InitStruct);

    //Enable periph clock
    RCC_APB2PeriphClockCmd(RCC_APB2Periph_USART1, ENABLE);
    RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOB, ENABLE);

    //Enable gpio
    GPIO_PinAFConfig(GPIOB, GPIO_PinSource6, GPIO_AF_USART1);
    GPIO_PinAFConfig(GPIOB, GPIO_PinSource7, GPIO_AF_USART1);

    //Enable usart
    USART_InitTypeDef USART_InitStruct;
    USART_InitStruct.USART_BaudRate = baudrate;

    USART_InitStruct.USART_WordLength = USART_WordLength_8b;
    USART_InitStruct.USART_StopBits = USART_StopBits_1;
    USART_InitStruct.USART_Parity = USART_Parity_No;    
    USART_InitStruct.USART_HardwareFlowControl = USART_HardwareFlowControl_None;
    USART_InitStruct.USART_Mode = USART_Mode_Tx | USART_Mode_Rx;
    USART_Init(USARTx, &USART_InitStruct);
    USART_ITConfig(USARTx, USART_IT_RXNE, ENABLE);

    USARTx->CR1 |= 0x8000; // Oversampling by 8
    USARTx->CR1 |= 0x1000; // 9 data bits word length: necessary for parity check to work!!!
    USARTx->CR1 &= ~0x200; // Sets even parity
    USARTx->CR1 |= 0x400; // Enables parity control
    USARTx->CR1 |= 0x100; // Parity error interrupt unable
    USARTx->CR1 |= 0x4; // Receiver enable
    USARTx->CR2 &= ~0x3000; // 1 stop bit

    // Set clock
    uint32_t tmpreg = 0x00, apbclock = 0x00;
	uint32_t integerdivider = 0x00;
	uint32_t fractionaldivider = 0x00;

	apbclock = 84000000;
	integerdivider = ((25 * apbclock) / (2 * (UART_BAUDRATE)));
	tmpreg = (integerdivider / 100) << 4;
	fractionaldivider = integerdivider - (100 * (tmpreg >> 4));
	tmpreg |= ((((fractionaldivider * 8) + 50) / 100)) & ((uint8_t)0x07);
	USARTx->BRR = (uint16_t)tmpreg;

    	//

    //Nvic management
    NVIC_EnableIRQ(USART1_IRQn);

    USART_Cmd(USARTx, ENABLE);
}

/**
 * Envoie un octet par le uart
 */
void uart_write_byte(volatile char p_char)
{
    while(!(USARTx->SR & USART_FLAG_TXE));
	//while (USART_GetFlagStatus(USARTx, USART_FLAG_TC) == RESET);
    //USARTx->DR = (uint16_t)p_char;
    USART_SendData(USARTx, (uint8_t)p_char);
}

/**
 * Lis un octet provenant de l'uart
 */
char uart_read_byte(void){
    read_idx = (read_idx + 1) % RING_BUFFER_SIZE;
    return (char)ring_buffer[read_idx];
}

/**
 * Envoie un buffer d'octets par le uart
 */
void uart_write_buffer(char*buffer, int size){
    int i;
    for(i=0 ; i < size ; i++){
        uart_write_byte(buffer[i]);
    }
    while (USART_GetFlagStatus(USARTx, USART_FLAG_TC) == RESET);
}


/**
 * S'occupe de la logique pour lire un octet du buffer circulaire
 */
uint32_t uart_read_cmd()
{
    read_idx = (read_idx + 1) % RING_BUFFER_SIZE;
    uint32_t command = 0;
    command |= ((uint32_t)ring_buffer[read_idx]);
    command |= ((uint32_t)ring_buffer[(read_idx - 1) % RING_BUFFER_SIZE]) << 8;
    command |= ((uint32_t)ring_buffer[(read_idx - 2) % RING_BUFFER_SIZE]) << 16;
    return command;
}

/**
 * Retourne le nombre d'octets à lire dans le buffer circulaire [0, RING_BUFFER_SIZE]
 */
int uart_available_bytes()
{
    return (write_idx - read_idx) % RING_BUFFER_SIZE;
}

/**
 * Interrupt systeme appelé quand le USART reçoit quelque chose
 * Doit insérer l'octet reçu dans le buffer circulaire
 */
void USART2_IRQHandler()
{
	uint16_t uart_error = 0; // Reset UART error flag

	// Check for parit error
	if ((USARTx->SR & (uint32_t)0x1) == 0x1)
		uart_error |= 1;

	// Check for framing error
	if (((USARTx->SR & (uint32_t)0x2) >> 1) == 0x1)
		uart_error |= 2;

	// Check for noise detection
	if (((USARTx->SR & (uint32_t)0x4) >> 2) == 0x1)
		uart_error |= 3;

	// Check for overrun error
	if (((USARTx->SR & (uint32_t)0x8) >> 3) == 0x1)
		uart_error |= 4;

	if (uart_error != 0) { // error detected
		uint16_t data = USARTx->DR; // dummy read
		return;
	}

    if(USART_GetITStatus(USARTx, USART_IT_RXNE)){

        uint16_t a = USARTx->DR;
        ring_buffer[write_idx] = a;
        write_idx = (write_idx + 1) % RING_BUFFER_SIZE;
        
        uart_write_byte(USARTx->DR);
    }
}
