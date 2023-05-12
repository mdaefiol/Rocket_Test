import serial
import time
import struct

# Configurações da porta serial
port = "COM4"
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
    data = ser.read()                           # Ler um byte pela porta serial
    if data == b'\x01':                         # Verifica se é o byte 0x01
        print("Byte 0x01 recebido")
        break

# Abre o arquivo em modo leitura
with open("data_SIL.txt", "r") as file:
    # Le os dados linha por linha e envia pela porta serial
    for line in file:
        data_values = line.strip().split()                                  # Separa os valores em uma lista
        for i, data_value in enumerate(data_values):
            if "E" in data_value:                                           # Verifica se é um número exponencial
                                                                            # Extrai o número base e a exponencial do número exponencial
                base, exp = data_value.split("E")
                data_float = float(base) * pow(10, int(exp))                # Multiplica o número base pela exponencial
            else:
                data_float = float(data_value)                              # Converte o valor p/ um número float

            data_bytes = struct.pack('>f', data_float)                      # Converte o número float para bytes (32 bits) -> 4 bytes
            data_bytes_32bit = struct.pack('>f', data_float)[0:4]           # Obtém apenas os 4 bytes mais significativos

            for i in range(0, 4):
                ser.write(bytes([data_bytes_32bit[i]]))                     # Envia cada byte do número pela porta serial
                print(f"Dado {i+1}: {hex(data_bytes_32bit[i])}", end=' ')   # Imprime o byte em hexa
                time.sleep(0.005)                                           # Atraso para enviar a 200Hz

            print('')
            data_float_32bit = struct.unpack('>f', data_bytes_32bit)        # Converte os 4 bytes p/ float de 32 bits
            print("Número float de 32 bits enviado:", data_float_32bit)

# Atraso de 10 ms após o envio de todos os dados do arquivo
time.sleep(0.01)

# Fecha o arquivo e a porta serial
file.close()
ser.close()
