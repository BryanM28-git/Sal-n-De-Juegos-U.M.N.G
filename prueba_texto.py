from oled_game import OLED_Game
from time import sleep

oled = OLED_Game()

oled.limpiar()

oled.texto("GAME ROOM", 28, 8)

oled.texto("1. REFLEJOS", 15, 25)
oled.texto("2. CARRERA", 15, 37)
oled.texto("3. TIRO", 15, 49)

oled.rectangulo(0, 0, 128, 64)

oled.mostrar()

print("Menu enviado correctamente")

while True:
    sleep(1)