/*
 * id.h
 *
 *  Created on: Jan 31, 2017
 *      Author: dark
 */

#ifndef ID_H_
#define ID_H_

#define ID_TEST_WAITING	0x1
#define ID_TEST_RUNNING	0x2
#define ID_TEST_DONE	0x4

#define ID_VAL_COUNT	512

uint16_t id_val_consigne[ID_VAL_COUNT];
uint16_t id_val_reponse[ID_VAL_COUNT];

uint32_t id_sample_no;
uint8_t id_test_status;

void setIdTestStatus(uint8_t status);
void initIdTest();
void fillIdConsigne();
void collectIdResponse(uint32_t value);
char *getIdTestStatus();
void stopIdTest();
void startIdTest();

#endif /* ID_H_ */
