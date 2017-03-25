/*
 * adc.c
 *
 *  Created on: Jan 18, 2017
 *      Author: dark
 */

#include <stm32f4xx_adc.h>
#include <usbd_def.h>
#include "stm32f4xx.h"
#include "stm32f4xx_adc.h"
#include "stm32f4xx_dma.h"
#include "adc.h"
#include "manchester.h"

#define DMASX                DMA2_Stream4
#define DMASX_IRQ_NO        DMA2_Stream4_IRQn
#define DMA_STREAM_NO        4

volatile uint16_t adc_values1[TOTAL_CONVERSIONS];
volatile uint16_t adc_values2[TOTAL_CONVERSIONS];

uint8_t status = 0;

/*void DMA2_Stream4_IRQHandler() {
    //TDMA1 Channel0 Transfer Complete interrupt
    if (DMA_GetITStatus(DMASX, DMA_IT_TCIF4) != RESET) {
        // Do something cool with the fetched data
        // You do it, but you do it cool

        uint16_t signal[CONVERSIONS_NUMBER_PER_CHANNEL];
        uint8_t code[MANCHESTER_N_DATA_BITS];
        char high, low;

        adc_get_channel_conversion_values(ADC_MANCHESTER_CODE, signal);

        ManchesterInfo info;
        uint8_t res = (uint8_t)decode(signal, CONVERSIONS_NUMBER_PER_CHANNEL, &info, code);


        int i = 0;

        //DMA_ClearITPendingBit(DMASX, DMA_IT_TCIF4);
    }
}*/

uint16_t adc_convert_value(uint16_t value) {
    return value >> 4;
}

uint16_t *adc_get_current_adc_buffer() {
    uint16_t *retval = adc_values2;

    if (DMA_GetCurrentMemoryTarget(DMASX) == 1)
        retval = adc_values1;

    return retval;
}

void adc_get_channel_conversion_values(uint8_t channel, uint16_t *values) {
    int n = 0;
    uint16_t *cvalues = adc_get_current_adc_buffer();
    for (int i = channel; i < TOTAL_CONVERSIONS; i += TOTAL_CHANNELS) {
        values[n] = adc_convert_value(cvalues[i]);
        n++;
    }
}

uint16_t adc_perform_injected_conversion() {
    // Software trigger the start of injected channels conversion
    ADC_SoftwareStartInjectedConv(ADC1);

    // Wait until the conversion is started
    while (ADC1->CR2 & ADC_CR2_JSWSTART);

    // Wait until injected channel end of conversion flag is raised
    while (ADC_GetFlagStatus(ADC1, ADC_SR_JEOC) != SET);

    uint16_t val = ADC_GetInjectedConversionValue(ADC1, ADC_InjectedChannel_1);

    // Clear the end of conversion flag
    ADC_ClearFlag(ADC1, ADC_SR_JEOC);

    return adc_convert_value(val);
}

// ADC1: DMA2, channel 0, stream 4
void adc_init() {
    ADC_InitTypeDef ADC_init_structure; //Structure for adc confguration
    GPIO_InitTypeDef GPIO_initStructre; //Structure for analog input pin

    //Clock configuration
    RCC_APB2PeriphClockCmd(RCC_APB2Periph_ADC1,
                           ENABLE);//The ADC1 is connected the APB2 peripheral bus thus we will use its clock source
    RCC_AHB1PeriphClockCmd(RCC_AHB1ENR_GPIOCEN, ENABLE);//Clock for the ADC port!! Do not forget about this one ;)

    //Analog pin configuration
    // PC0, PC1, PC2, PC3 <-> ADC_CH10, ADC_CH11, ADC_CH12, ADC_CH13
    GPIO_initStructre.GPIO_Pin = GPIO_Pin_0 | GPIO_Pin_1 | GPIO_Pin_2 | GPIO_Pin_3; //The channel 10 is connected to PC0
    GPIO_initStructre.GPIO_Mode = GPIO_Mode_AN; //The PC0 pin is configured in analog mode
    GPIO_initStructre.GPIO_PuPd = GPIO_PuPd_NOPULL; //We don't need any pull up or pull down
    GPIO_Init(GPIOC, &GPIO_initStructre);//Affecting the port with the initialization structure configuration

    //ADC structure configuration
    ADC_DeInit();

    ADC_init_structure.ADC_DataAlign = ADC_DataAlign_Right;//data converted will be shifted to right
    ADC_init_structure.ADC_Resolution = ADC_Resolution_12b;//Input voltage is converted into a 12bit number giving a maximum value of 4096
    ADC_init_structure.ADC_ContinuousConvMode = ENABLE; //the conversion is continuous, the input data is converted more than once

    // Use trigger only if we wish to get adc conversions at precise intervals through timer trigger interrupts
    //ADC_init_structure.ADC_ExternalTrigConv = ADC_ExternalTrigConv_T8_TRGO;// conversion is synchronous with TIM1 and CC1 (actually I'm not sure about this one :/)
    //ADC_init_structure.ADC_ExternalTrigConvEdge = ADC_ExternalTrigConvEdge_Rising;//no trigger for conversion

    ADC_init_structure.ADC_NbrOfConversion = TOTAL_CHANNELS;// !!!!!!!!!
    ADC_init_structure.ADC_ScanConvMode = ENABLE;//The scan is configured in one channel // TEMP: was disable

    ADC_Init(ADC1, &ADC_init_structure);

    // IMPORTANT: an ADC channel cannot be at the same time a regular channel while being an injected channel.
    // It works but produces unpredictable results.
    ADC_RegularChannelConfig(ADC1, ADC_Channel_10, 1, ADC_SampleTime_480Cycles);
    ADC_RegularChannelConfig(ADC1, ADC_Channel_14, 2, ADC_SampleTime_480Cycles); // Dummy ADC
    ADC_RegularChannelConfig(ADC1, ADC_Channel_12, 3, ADC_SampleTime_480Cycles);
    ADC_RegularChannelConfig(ADC1, ADC_Channel_13, 4, ADC_SampleTime_480Cycles);

    // Sets the injected channels. Once a software conversion is triggered, the current regular channel conversions
    // are stopped and the injected channel conversions are started. When injection conversions are completed, the
    // regular channel conversions are resumed.
    ADC_InjectedSequencerLengthConfig(ADC1, 1);
    ADC_InjectedChannelConfig(ADC1, ADC_Channel_11, 1, ADC_SampleTime_3Cycles);

    //Enable ADC conversion
    ADC_Cmd(ADC1, ENABLE);

    ADC_DMACmd(ADC1, ENABLE);


    // Enable dma clock

    RCC->AHB1ENR |= RCC_AHB1Periph_DMA2;

    // Enable IRQ for stream X of DMAX in NVIC
    NVIC_EnableIRQ(DMASX_IRQ_NO);

    // Set the peripheral port register address
    DMASX->PAR = (uint32_t) &ADC1->DR;

    // Set the memory addresses
    DMASX->M0AR = adc_values1;
    DMASX->M1AR = adc_values2;

    // Set the total number of data items to be transferred
    DMASX->NDTR = TOTAL_CONVERSIONS;

    // Select the right DMA channel
    DMASX->CR |= DMA_Channel_0; // Channel 0 for ADC1

    // Configure the stream priority (PL[1:0] bits in CR register)
    DMASX->CR |= DMA_SxCR_PL_1; // High priority

    // Configure the data transfer direction
    DMASX->CR |= DMA_SxCR_CIRC;
    DMASX->CR |= DMA_SxCR_MINC; // Memory address pointer incremented after each transfer
    DMASX->CR |= DMA_SxCR_MSIZE_0; // half-word (16 bits) memory data size
    DMASX->CR |= DMA_SxCR_PSIZE_0; // half-word (16 bits) peripheral data size
    //DMASX->CR |= DMA_SxCR_DIR_1; // peripheral-to-memory direction
    //DMASX->CR |= DMA_SxCR_TCIE; // transfer complete interrupt enable
    DMASX->CR |= DMA_SxCR_DBM; // enable double buffer mode

    // Enable stream!
    DMASX->CR |= DMA_SxCR_EN;

    //Enable DMA1 Channel transfer
    DMA_Cmd(DMA_Channel_0, ENABLE);

    //Start ADC1 Software Conversion
    ADC_SoftwareStartConv(ADC1);
}
