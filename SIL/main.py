import serial
import time

# Configurações da porta serial
port = "COM4"
baudrate = 9600
byte_size = serial.EIGHTBITS
parity = serial.PARITY_NONE
stop_bits = serial.STOPBITS_ONE

# Abrir a porta serial
ser = serial.Serial(port, baudrate, byte_size, parity, stop_bits)
time.sleep(2) # Aguardar a inicialização da porta serial

# Aguardar o byte 0x01 ser recebido
while True:
    data = ser.read() # Ler um byte pela porta serial
    if data == b'\x01': # Verificar se é o byte 0x01
        print("Byte 0x01 recebido")
        break

# Abrir o arquivo em modo leitura
with open("data_accx.txt", "r") as file:
    # Ler os dados linha por linha e enviar pela porta serial
    for line in file:
        data = int(line.strip(), 8) # Converter a linha para um número inteiro em hexadecimal
        ser.write(bytes([data])) # Enviar o número pela porta serial como um byte
        time.sleep(0.01) # Atraso para evitar perda de dados na transmissão

# Fechar o arquivo e a porta serial
file.close()
ser.close()
