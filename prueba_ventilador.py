from machine import Pin, PWM
from time import sleep

ventilador = PWM(Pin(21))
ventilador.freq(1000)

print("APAGADO")
ventilador.duty_u16(0)
sleep(2)

print("BAJO")
ventilador.duty_u16(40000)
sleep(3)

print("MEDIO")
ventilador.duty_u16(52000)
sleep(3)

print("MAXIMO")
ventilador.duty_u16(65535)
sleep(3)

print("APAGADO")
ventilador.duty_u16(0)