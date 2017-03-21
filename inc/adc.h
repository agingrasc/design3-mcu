/*
 * adc.h
 *
 *  Created on: Jan 18, 2017
 *      Author: dark
 */

#ifndef ADC_H_
#define ADC_H_

#include "stm32f4xx.h"

// ADC channels
#define ADC_NC                      0 // Channel 10, no connect
#define ADC_MANCHESTER_CODE_POWER   1 // Channel 11
#define ADC_MANCHESTER_CODE         2 // Channel 12
#define ADC_PENCIL                  3 // Channel 13

// Number of ADC conversions that will be recorded by DMA
#define CONVERSIONS_NUMBER_PER_CHANNEL  512

// Number of channel ADC must sample
#define TOTAL_CHANNELS                   4

// Total number of conversions that will be performed by ADC
#define TOTAL_CONVERSIONS       CONVERSIONS_NUMBER_PER_CHANNEL*TOTAL_CHANNELS

void adc_init();
void adc_get_channel_conversion_values(uint8_t channel, uint16_t *values);

void DMA2_Stream4_IRQHandler();

volatile uint16_t pencil_voltage;

#endif /* ADC_H_ */
