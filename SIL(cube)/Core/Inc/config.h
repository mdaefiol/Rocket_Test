/*
 * config.h
 *
 *  Created on: May 10, 2023
 *      Author: mdaef
 */

#ifndef INC_CONFIG_H_
#define INC_CONFIG_H_

#include "stm32f1xx_hal.h"

typedef struct {
	double accel_x;
	double accel_y;
	double accel_z;
	double pressao;
	double altitude;
} SensorData;

void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim);
void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart);

#endif /* INC_CONFIG_H_ */
