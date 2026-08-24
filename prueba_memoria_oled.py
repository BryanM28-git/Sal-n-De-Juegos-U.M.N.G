from machine import Pin, SoftSPI
from time import sleep_ms, sleep

spi = SoftSPI(
    baudrate=500_000,
    polarity=0,
    phase=0,
    sck=Pin(4),
    mosi=Pin(5),
    miso=Pin(8)
)

rst = Pin(6, Pin.OUT)
dc  = Pin(7, Pin.OUT)
cs  = Pin(15, Pin.OUT)

cs.value(1)

def comando(valor):
    dc.value(0)
    cs.value(0)
    spi.write(bytes([valor]))
    cs.value(1)

def datos(buffer):
    dc.value(1)
    cs.value(0)
    spi.write(buffer)
    cs.value(1)

# RESET
rst.value(1)
sleep_ms(10)
rst.value(0)
sleep_ms(50)
rst.value(1)
sleep_ms(100)

comando(0xAE)  # Display OFF
comando(0xA4)  # Mostrar RAM
comando(0xA6)  # Normal
comando(0xA1)  # Segment remap
comando(0xC8)  # COM scan direction

# LIMPIAR LAS 8 PAGINAS
for pagina in range(8):

    comando(0xB0 + pagina)

    # Columna 0
    comando(0x00)
    comando(0x10)

    datos(bytes([0x00] * 128))

comando(0xAF)

print("Pantalla limpiada")

sleep(2)

# Dibujar una franja blanca SOLO en la pagina 3
comando(0xB3)
comando(0x00)
comando(0x10)

datos(bytes([0xFF] * 128))

print("Franja dibujada")

while True:
    sleep(1)