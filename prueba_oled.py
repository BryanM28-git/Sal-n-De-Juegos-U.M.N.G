from machine import Pin, SoftSPI
from ssd1306 import SSD1306_SPI
from time import sleep

# SPI por software
spi = SoftSPI(
    baudrate=1_000_000,
    polarity=0,
    phase=0,
    sck=Pin(4),
    mosi=Pin(5),
    miso=Pin(8)
)

# Pines OLED
dc = Pin(7)
res = Pin(6)
cs = Pin(15)

# Primera prueba: 128 x 64
oled = SSD1306_SPI(
    128,
    64,
    spi,
    dc,
    res,
    cs
)

oled.fill(0)

oled.text("GAME ROOM", 28, 10)
oled.text("OLED OK!", 32, 30)

oled.rect(0, 0, 128, 64, 1)

oled.show()

print("Datos enviados a la OLED")

while True:
    sleep(1)