// main.c

#include "main.h"

void initLed()
{
    RCC_AHB1PeriphClockCmd(RCC_AHB1Periph_GPIOD, ENABLE);

    GPIO_InitTypeDef GPIO_InitStructure;
    GPIO_InitStructure.GPIO_Pin = GPIO_Pin_12 | GPIO_Pin_13 | GPIO_Pin_14 | GPIO_Pin_15;
    GPIO_InitStructure.GPIO_Mode = GPIO_Mode_OUT;
    GPIO_InitStructure.GPIO_Speed = GPIO_Speed_100MHz;
    GPIO_InitStructure.GPIO_OType = GPIO_OType_PP;
    GPIO_InitStructure.GPIO_PuPd = GPIO_PuPd_NOPULL;
    GPIO_Init(GPIOD, &GPIO_InitStructure);
    //GPIO_SetBits(GPIOD, GPIO_Pin_12 | GPIO_Pin_13 | GPIO_Pin_14 | GPIO_Pin_15);
}

void updateDisplay() {
	lcd_clear_row(0);
	lcd_set_cursor(0, 0);

	// Convert units to human readable units
	/*for (int i = 0; i < MOTOR_COUNT; i++) {
		uint32_t tmp = (motors[i].last_tick_delta * 60000 * WHEEL_RADIUS)/(motors[i].last_timestamp_delta * 6400);
		motors[i].motor_speed_rpm = tmp;
	}*/

	char buf1[16];

	//sprintf(buf1, "%d %d", motors[current_motor].motor_speed_rpm, motors[current_motor].encoder_cnt);
	sprintf(buf1, "%d %d", motors[0].motor_speed_rpm, motors[1].motor_speed_rpm);
	for (int i = 0; i < 16; i++) {
		if (buf1[i] == '\0') break;
		lcd_putc(buf1[i]);
	}

	lcd_clear_row(1);
	lcd_set_cursor(1, 0);

	char buf2[16];
	//sprintf(buf2, "%d %d", motors[current_motor].motor_speed_rpm, motors[current_motor].encoder_cnt);
	sprintf(buf2, "%d %d%s", motors[2].motor_speed_rpm, motors[3].motor_speed_rpm, getIdTestStatus());
	for (int i = 0; i < 16; i++) {
		if (buf2[i] == '\0') break;
		lcd_putc(buf2[i]);
	}
}

void checkForVCP() {
	/* USB configured OK, drivers OK */
	TM_USB_VCP_Result res = TM_USB_VCP_GetStatus();
	if (res == TM_USB_VCP_CONNECTED) {
		/* Turn on GREEN led */
		GPIO_ResetBits(GPIOD, GPIO_Pin_14);
		GPIO_SetBits(GPIOD, GPIO_Pin_12);
		/* If something arrived at VCP */

		/*char buffer[5];
		uint16_t len = TM_USB_VCP_Gets(buffer, 5);
		if (len > 0)
			TM_USB_VCP_Puts(buffer);*/
	} else {
		/* USB not OK */
		GPIO_ResetBits(GPIOD, GPIO_Pin_12);
		GPIO_SetBits(GPIOD, GPIO_Pin_14);
	}
}

int main(){
 	current_motor = 0;

 	SystemInit();

 	initLed();

 	/* Initialize USB virtual COM port */
 	TM_USB_VCP_Init();

	// Don't know why I have to do this here.
	// This is for motor b
	RCC->AHB1ENR |= RCC_AHB1Periph_GPIOA;
	GPIOA->MODER |= 0x2;
	GPIOA->MODER |= (0x2 << 2);
	GPIOA->PUPDR |= 0x1;
	GPIOA->PUPDR |= (01 << 2);
	GPIOA->AFR[0] |= GPIO_AF_TIM4;
	GPIOA->AFR[0] |= (GPIO_AF_TIM4 << 4);

	// This is for motor d
	RCC->AHB1ENR |= RCC_AHB1Periph_GPIOE;
	GPIOE->MODER |= (0x2 << 18);
	GPIOE->MODER |= (0x2 << 22); // AF
	GPIOE->PUPDR |= (0x1 << 18);
	GPIOE->PUPDR |= (0x1 << 22);
	GPIOE->AFR[1] |= (GPIO_AF_TIM1 << 4);
	GPIOE->AFR[1] |= (GPIO_AF_TIM1 << 12);

	// this is for motor c
	//RCC->AHB1ENR |= RCC_AHB1Periph_GPIOE;
	RCC->APB2ENR |= RCC_APB2Periph_TIM9;
	GPIOE->MODER |= (0x2 << 10);
	GPIOE->PUPDR |= (0x1 << 10);
	GPIOE->AFR[0] |= (GPIO_AF_TIM9 << 20);
	TIM9->CCMR1 |= 0x1;
	TIM9->CCER |= 0x1;
	TIM9->ARR = 0xffff;
	TIM9->SMCR |= (4 << 4);
	TIM9->SMCR |= 5;
	TIM9->CR1 |= 0x1;

    //initDelay();
    initTimer();

    lcd_init();

    motorControllerInit();
#ifndef ID_MODE
    pidInit();
#endif
    cmdHandlerInit();
    MotorEncodersInit();

#ifdef ID_MODE
    id_test_status = 0;
#endif

    initIdTest();
    //startIdTest();

    unsigned int last_second = 0;

    int cmd_header_ok = 0;
    int cmd_payload_ok = 0;
    while(1) {
    	// Check for VCP connection
    	checkForVCP();

		command cmd;
        if (!cmd_header_ok && !TM_USB_VCP_BufferEmpty())
        {
            char header[2];
            cmd_header_ok = usb_read_cmd_header(header);
            if (cmd_header_ok) {
                cmd.header.type = header[0];
                cmd.header.size = header[1];
            }
        }

        if (cmd_header_ok && !TM_USB_VCP_BufferEmpty()) {
            char payload[256];
            cmd_payload_ok = usb_read_cmd_payload(payload, cmd.header.size);
            if (cmd_payload_ok) {
                for (int i = 0; i < cmd.header.size; i++) {
                    cmd.payload[i] = payload[i];
                }
            }
        }

        if (cmd_payload_ok) {
            command_execute(cmd);
            cmd_header_ok = 0;
            cmd_payload_ok = 0;
        }

        // Update time line, if necessary
		unsigned int mstemp = (unsigned int)(timestamp / 1000);
		if (mstemp != last_second) { // One second elapsed
			updateDisplay(); // Update time on LCD
			//uart_write_buffer(id_val_consigne, ID_VAL_COUNT);
			//uart_write_byte('a');
			last_second = mstemp;
		}
    }
}
