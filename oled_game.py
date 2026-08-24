from machine import Pin, SoftSPI
import framebuf
from time import sleep_ms, sleep


class OLED_Game:

    def __init__(self):

        self.width = 128
        self.height = 64

        self.spi = SoftSPI(
            baudrate=500_000,
            polarity=0,
            phase=0,
            sck=Pin(4),
            mosi=Pin(5),
            miso=Pin(8)
        )

        self.rst = Pin(6, Pin.OUT)
        self.dc = Pin(7, Pin.OUT)
        self.cs = Pin(15, Pin.OUT)

        self.cs.value(1)

        # Memoria de imagen
        self.buffer = bytearray(128 * 64 // 8)

        self.frame = framebuf.FrameBuffer(
            self.buffer,
            128,
            64,
            framebuf.MONO_VLSB
        )

        self.reset()
        self.iniciar()

    def comando(self, valor):

        self.dc.value(0)
        self.cs.value(0)

        self.spi.write(bytes([valor]))

        self.cs.value(1)

    def datos(self, datos):

        self.dc.value(1)
        self.cs.value(0)

        self.spi.write(datos)

        self.cs.value(1)

    def reset(self):

        self.rst.value(1)
        sleep_ms(10)

        self.rst.value(0)
        sleep_ms(50)

        self.rst.value(1)
        sleep_ms(100)

    def iniciar(self):

        self.comando(0xAE)
        self.comando(0xA4)
        self.comando(0xA6)
        self.comando(0xA1)
        self.comando(0xC8)

        self.limpiar()
        self.comando(0xAF)

    def limpiar(self):

        self.frame.fill(0)
        self.mostrar()

    def mostrar(self):

        for pagina in range(8):

            self.comando(0xB0 + pagina)

            # Columna 0
            self.comando(0x00)
            self.comando(0x10)

            inicio = pagina * 128
            fin = inicio + 128

            self.datos(self.buffer[inicio:fin])

    def texto(self, texto, x, y):

        self.frame.text(texto, x, y, 1)

    def rectangulo(self, x, y, ancho, alto):

        self.frame.rect(x, y, ancho, alto, 1)