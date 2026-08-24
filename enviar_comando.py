import serial
import time

PUERTO = "COM5"

esp32 = serial.Serial(
    PUERTO,
    115200,
    timeout=2
)

time.sleep(2)

print("Conexion abierta")

esp32.write(b"HOLA\n")

time.sleep(0.5)

while esp32.in_waiting:
    respuesta = esp32.readline().decode(
        errors="ignore"
    ).strip()

    print("ESP32:", respuesta)

esp32.close()