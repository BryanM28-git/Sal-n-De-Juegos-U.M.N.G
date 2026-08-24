from machine import Pin, SPI
from ssd1309 import Display
from time import sleep

spi = SPI(
    1,
    baudrate=100_000,
    polarity=0,
    phase=0,
    sck=Pin(4),
    mosi=Pin(5),
    miso=Pin(8)
)

display = Display(
    spi=spi,
    dc=Pin(7),
    cs=Pin(15),
    rst=Pin(6),
    width=128,
    height=64
)

display.clear()
display.draw_text8x8(24, 10, "GAME ROOM")
display.draw_text8x8(32, 30, "OLED OK!")
display.present()

print("Prueba OLED enviada")

while True:
    sleep(1)