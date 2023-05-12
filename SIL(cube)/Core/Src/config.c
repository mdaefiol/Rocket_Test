/*
 * config.c
 *
 *  Created on: May 10, 2023
 *      Author: mdaef
 */

#include "config.h"
#include <math.h>

extern UART_HandleTypeDef huart2;
extern TIM_HandleTypeDef htim4;

SensorData sensor_data;
receiv pressure;

static int data_received_count = 0;
uint8_t data_UART;

uint32_t data_hex;
static uint8_t rx_buffer[16];
float data_float;
uint8_t rx_byte[1] = {0x01};


// INTERRUPÇAO CONFIGURADA PARA 200Hz, 1 dado a cada 0,005s -> 16bytes = 0.08
void HAL_TIM_PeriodElapsedCallback(TIM_HandleTypeDef *htim){
	if(htim->Instance == htim4.Instance){
		if (data_received_count == 0) {
			HAL_UART_Transmit_IT(&huart2, rx_byte, 1);
			data_received_count = 1;
		}
		else if (data_received_count != 0){
			HAL_UART_Receive_IT(&huart2, rx_buffer, 16);
			data_UART = 0x01;
			data_received_count++;
		}
	}
}

void HAL_UART_RxCpltCallback(UART_HandleTypeDef *huart){

	if(huart->Instance == huart2.Instance){
		if(data_UART == 0x01) {
			data_hex = (rx_buffer[0] << 24) | (rx_buffer[1] << 16) | (rx_buffer[2] << 8) | rx_buffer[3];
			data_float = *(float*)&data_hex;
			sensor_data.accel_x = data_float;

			data_hex = (rx_buffer[4] << 24) | (rx_buffer[5] << 16) | (rx_buffer[6] << 8) | rx_buffer[7];
			data_float = *(float*)&data_hex;
			sensor_data.accel_y = data_float;

			data_hex = (rx_buffer[8] << 24) | (rx_buffer[9] << 16) | (rx_buffer[10] << 8) | rx_buffer[11];
			data_float = *(float*)&data_hex;
			sensor_data.accel_z = data_float;

			data_hex = (rx_buffer[12] << 24) | (rx_buffer[13] << 16) | (rx_buffer[14] << 8) | rx_buffer[15];
			data_float = *(float*)&data_hex;
			sensor_data.pressao = data_float;

			double pressureSeaLevel = 101325; //Pa

			pressure.altitude = 44330.0*(1.0 - pow((sensor_data.pressao/pressureSeaLevel), 0.1903));
		}
		data_UART = 0x00;
	}
}

