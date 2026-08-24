from machine import Pin, SoftSPI
from time import sleep_ms, sleep

SCK = 4
MOSI = 5
RST = 6
DC = 7
CS = 15

spi = SoftSPI(
    baudrate=500_000,
    polarity=0,
    phase=0,
    sck=Pin(SCK),
    mosi=Pin(MOSI),
    miso=Pin(8)
)

rst = Pin(RST, Pin.OUT)
dc = Pin(DC, Pin.OUT)
cs = Pin(CS, Pin.OUT)

cs.value(1)

def comando(valor):
    dc.value(0)
    cs.value(0)
    spi.write(bytes([valor]))
    cs.value(1)

# RESET físico
rst.value(1)
sleep_ms(10)

rst.value(0)
sleep_ms(50)

rst.value(1)
sleep_ms(100)

# Apagar display
comando(0xAE)

# Modo normal
comando(0xA6)

# ENCENDER TODOS LOS PIXELES
comando(0xA5)

# Encender display
comando(0xAF)

print("TODOS LOS PIXELES DEBERIAN ESTAR ENCENDIDOS")

sleep(5)

# Volver a contenido RAM
comando(0xA4)

print("Regresando a memoria RAM")

while True:
    sleep(1)