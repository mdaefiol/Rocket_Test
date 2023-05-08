import serial
import time
import struct

# Configurações da porta serial
port = "COM4"
baudrate = 9600  # 115200
byte_size = serial.EIGHTBITS
parity = serial.PARITY_NONE
stop_bits = serial.STOPBITS_ONE

# Abre a porta serial
ser = serial.Serial(port, baudrate, byte_size, parity, stop_bits)
time.sleep(2)  # Aguardar a inicialização da porta serial

# Aguarda o byte 0x01 ser recebido
while True:
    data = ser.read()  # Ler um byte pela porta serial
    if data == b'\x01':  # Verificar se é o byte 0x01
        print("Byte 0x01 recebido")
        break

# Abre o arquivo em modo leitura
with open("data_accx.txt", "r") as file:
    # Le os dados linha por linha e envia pela porta serial
    for line in file:
        data_values = line.strip().split()                  # Separa os valores em uma lista
        for i, data_value in enumerate(data_values):
            data_float = float(data_value)                  # Converte o valor p/ um número float
            data_bytes = struct.pack('>f', data_float)      # Converte o número float para bytes (32 bits) -> 4 bytes
            for i in range(0, 4):
                ser.write(bytes([data_bytes[i]]))           # Envia cada byte do número pela porta serial
                print(f"Dado {i+1}: {hex(data_bytes[i])}", end=' ')  # Imprime o byte em hexa
                time.sleep(0.01)                                     # Atraso p evitar perda de dados na transmissão
            print('')  # Imprimir uma nova linha para separar os pacotes de dados

            data_float = struct.unpack('>f', data_bytes)     # Converte os bytes p/ float
            print("Número float enviado:", data_float)

# Fecha o arquivo e a porta serial
file.close()
ser.close()
