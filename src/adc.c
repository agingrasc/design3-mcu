/*
 * adc.c
 *
 *  Created on: Jan 18, 2017
 *      Author: dark
 */

#include "adc.h"
#include "stm32f4xx.h"
#include "stm32f4xx_adc.h"
#include "stm32f4xx_dma.h"

#define DMASX                DMA2_Stream4
#define DMASX_IRQ_NO        DMA2_Stream4_IRQn
#define DMA_STREAM_NO        4

#define ARRAY_SIZE    2

volatile uint16_t pwm_values[ARRAY_SIZE];

uint8_t status = 0;

void DMA2_Stream4_IRQHandler() {
    //TDMA1 Channel0 Transfer Complete interrupt
    if (DMA_GetITStatus(DMASX, DMA_IT_TCIF4) != RESET) {
        // Do something cool with the fetched data
        // You do it, but you do it cool
    }
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
    GPIO_initStructre.GPIO_Pin = GPIO_Pin_1 | GPIO_Pin_2; //The channel 10 is connected to PC0
    GPIO_initStructre.GPIO_Mode = GPIO_Mode_AN; //The PC0 pin is configured in analog mode
    GPIO_initStructre.GPIO_PuPd = GPIO_PuPd_NOPULL; //We don't need any pull up or pull down
    GPIO_Init(GPIOC, &GPIO_initStructre);//Affecting the port with the initialization structure configuration

    //ADC structure configuration
    ADC_DeInit();
    ADC_init_structure.ADC_DataAlign = ADC_DataAlign_Right;//data converted will be shifted to right
    ADC_init_structure.ADC_Resolution = ADC_Resolution_12b;//Input voltage is converted into a 12bit number giving a maximum value of 4096
    ADC_init_structure.ADC_ContinuousConvMode = ENABLE; //the conversion is continuous, the input data is converted more than once

    //ADC_init_structure.ADC_ExternalTrigConv = ADC_ExternalTrigConv_T1_CC1;// conversion is synchronous with TIM1 and CC1 (actually I'm not sure about this one :/)
    //ADC_init_structure.ADC_ExternalTrigConvEdge = ADC_ExternalTrigConvEdge_None;//no trigger for conversion
    ADC_init_structure.ADC_NbrOfConversion = 2;// !!!!!!!!!
    ADC_init_structure.ADC_ScanConvMode = ENABLE;//The scan is configured in one channel // TEMP: was disable

    ADC_Init(ADC1, &ADC_init_structure);//Initialize ADC with the previous configuration


    //Select the channel to be read from
    ADC_RegularChannelConfig(ADC1, ADC_Channel_11, 1, ADC_SampleTime_144Cycles);
    ADC_RegularChannelConfig(ADC1, ADC_Channel_12, 2, ADC_SampleTime_144Cycles);

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
    DMASX->M0AR = pwm_values;

    // Set the total number of data items to be transferred
    DMASX->NDTR = ARRAY_SIZE;

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
    DMASX->CR |= DMA_SxCR_TCIE; // transfer complete interrupt enable

    // Enable stream!
    DMASX->CR |= DMA_SxCR_EN;

    //Enable DMA1 Channel transfer
    DMA_Cmd(DMA_Channel_0, ENABLE);

    //Start ADC1 Software Conversion
    ADC_SoftwareStartConv(ADC1);
}
