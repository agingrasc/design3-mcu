/*
 * id.c
 *
 *  Created on: Jan 31, 2017
 *      Author: dark
 */

#include "main.h"

// Initiate variables to prepare dynamic identification test
void initIdTest() {
	id_sample_no = 0;
	id_test_status = ID_TEST_WAITING;
	current_motor = MOTOR_A; // by default, use motor a
	fillIdConsigne();
}

// Fill the consigne buffer with values between 0 and 1, 0 being 0% of max consigne
// and 1 100% of the max consigne
// While performing the test, this buffer will be converted sample by sample to the
// correct consigne to be set in the PWM registers in order to produce the desired duty cycle
void fillIdConsigne() {
	// Description of the test
	/*
	 * First we will stabilise at 20%, then jump at 80%
	 * Finally, we will return back to 20% after steady state has been reached
	 */

	float begin_consigne = 0.60f;
	float end_consigne = 0.9f;

	int i;
	for (i = 0; i < 128; i++)
		id_val_consigne[i] = begin_consigne*PWM_PULSE_LENGTH;

	for (; i < 256; i++)
		id_val_consigne[i] = end_consigne*PWM_PULSE_LENGTH;

	for (; i < ID_VAL_COUNT; i++)
		id_val_consigne[i] = 0;

	id_val_consigne[0] = 0;

	for (i = 0; i < ID_VAL_COUNT; i++)
		id_val_reponse[i] = 0;

}

void collectIdResponse(uint32_t value) {
	if (id_test_status == ID_TEST_RUNNING) {
		id_val_reponse[id_sample_no] = value;
		//TM_USB_VCP_Putc(value);
		//TM_USB_VCP_Send((uint16_t)value, 2);
		/* (id_test_status == ID_TEST_RUNNING)
			uart_write_byte((char)value);*/
		id_sample_no++;
		if (id_sample_no < ID_VAL_COUNT-1)
			setPWMConsigne(current_motor, id_val_consigne[id_sample_no]);
		else
			stopIdTest();
	}
}

void startIdTest() {
	id_sample_no = 0;
	fillIdConsigne();
	id_test_status = ID_TEST_RUNNING;
	int j = 0;
}

void stopIdTest() {
	id_test_status = ID_TEST_DONE;
	setPWMConsigne(current_motor, 0);
	int k = 0;
}

char *getIdTestStatus() {
	char *retval = "";

#ifdef ID_MODE
	if (id_test_status == ID_TEST_WAITING)
		retval = " ID_WAIT";
	else if (id_test_status == ID_TEST_RUNNING)
		retval = " ID_RUN";
	else if (id_test_status == ID_TEST_DONE)
		retval = " ID_DONE";
#endif

	return retval;
}
