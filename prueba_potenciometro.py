from machine import Pin, ADC
from time import sleep

pot = ADC(Pin(1))

while True:
    valor = pot.read_u16()

    print("Potenciometro:", valor)

    sleep(0.2)