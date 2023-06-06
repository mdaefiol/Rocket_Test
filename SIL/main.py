import serial
import time
import struct
import sys
import decimal

# Configurações da porta serial
if sys.platform.startswith('win'):
    port = "COM4"                       # Porta serial no Windows
else:
    port = "/dev/ttyUSB0"               # Porta serial no Linux

baudrate = 115200
byte_size = serial.EIGHTBITS
parity = serial.PARITY_NONE
stop_bits = serial.STOPBITS_ONE

# Abre a porta serial
ser = serial.Serial(port, baudrate, byte_size, parity, stop_bits)
time.sleep(1)
# Aguarda a inicialização da porta serial

# Aguarda o byte 0x01 ser recebido
while True:
    data = ser.read()  # Ler um byte pela porta serial
    if data == b'\x01':  # Verifica se é o byte 0x01
        print("Byte 0x01 recebido")
        time.sleep(1)  #
        break

# Abre o arquivo que contem os dados dos sensores em modo leitura
time.sleep(5)  #
with open("data_SIL.txt", "r") as file:
                                                                     # Le os dados linha por linha e envia pela porta serial
    for line in file:
        data_values = line.strip().split()                           # Separa os valores em uma lista
        data_bytes = bytearray()
        for data_value in data_values:
            data_float = decimal.Decimal(data_value)
            data_bytes.extend(struct.pack('>f', data_float))        # Converte o número float para bytes (32 bits) e adiciona à lista

        ser.write(data_bytes)                                       # Envia os 16 bytes pela porta serial
        for i, byte in enumerate(data_bytes):
            print(f"Dado {i+1}: {hex(byte)}", end=' ')              # Imprime cada byte em hexa
        print('')
        data_float_32bit = struct.unpack('>4f', data_bytes)         # Converte os 16 bytes de volta para os 4 floats de 32 bits
        print("Dado float enviado:", data_float_32bit)
        time.sleep(0.005)  # 5ms
# 5000 -> 500ms
# 500 -> 50ms
# 50 -> 5 ms

# Atraso de 10 ms após o envio de todos os dados do arquivo
time.sleep(0.1)

# Fecha o arquivo e a porta serial
file.close()
ser.close()
