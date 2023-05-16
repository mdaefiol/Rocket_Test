import serial
import time
import struct
import sys

# Configurações da porta serial
if sys.platform.startswith('win'):
    port = "COM4"  # Porta serial no Windows (exemplo)
else:
    port = "/dev/ttyUSB0"  # Porta serial no Linux (exemplo)

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

# Abre o arquivo em modo leitura
time.sleep(3)  #
with open("data_SIL.txt", "r") as file:
    # Le os dados linha por linha e envia pela porta serial
    for line in file:
        data_values = line.strip().split()  # Separa os valores em uma lista
        data_bytes = bytearray()
        for data_value in data_values:
            if "E" in data_value:  # Verifica se é um número exponencial
                # Extrai o número base e a exponencial do número exponencial
                base, exp = data_value.split("E")
                data_float = float(base) * pow(10, int(exp))  # Multiplica o número base pela exponencial
            else:
                data_float = float(data_value)  # Converte o valor p/ um número float

            data_bytes.extend(struct.pack('>f', data_float))  # Converte o número float para bytes (32 bits) e adiciona à lista

        ser.write(data_bytes)  # Envia os 16 bytes pela porta serial
        for i, byte in enumerate(data_bytes):
            print(f"Dado {i+1}: {hex(byte)}", end=' ')  # Imprime cada byte em hexa
        print('')
        data_float_32bit = struct.unpack('>4f', data_bytes)  # Converte os 16 bytes de volta para os 4 floats de 32 bits
        print("Números float de 32 bits enviados:", data_float_32bit)
        time.sleep(0.2)  # 100ms


# Atraso de 10 ms após o envio de todos os dados do arquivo
time.sleep(0.1)

# Fecha o arquivo e a porta serial
file.close()
ser.close()
