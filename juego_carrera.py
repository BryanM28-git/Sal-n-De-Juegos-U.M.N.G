from machine import Pin, ADC
from time import sleep, ticks_ms, ticks_diff
from random import randint

from oled_game import OLED_Game


oled = OLED_Game()
pot = ADC(Pin(1))

ANCHO = 128
ALTO = 64

CARRO_Y = 50
CARRO_ANCHO = 11
CARRO_ALTO = 10

OBST_ANCHO = 10
OBST_ALTO = 8


def leer_posicion_carro():

    valor = pot.read_u16()

    x = int(
        valor * (ANCHO - CARRO_ANCHO - 10)
        / 65535
    )

    return x + 5


def dibujar_carro(x):

    # cuerpo
    oled.frame.fill_rect(
        x + 2,
        CARRO_Y + 3,
        7,
        7,
        1
    )

    # cabina
    oled.frame.fill_rect(
        x + 4,
        CARRO_Y,
        3,
        3,
        1
    )

    # ruedas
    oled.frame.pixel(
        x,
        CARRO_Y + 5,
        1
    )

    oled.frame.pixel(
        x + 10,
        CARRO_Y + 5,
        1
    )


def dibujar_obstaculo(x, y):

    oled.frame.rect(
        x,
        y,
        OBST_ANCHO,
        OBST_ALTO,
        1
    )

    oled.frame.line(
        x,
        y,
        x + OBST_ANCHO - 1,
        y + OBST_ALTO - 1,
        1
    )

    oled.frame.line(
        x + OBST_ANCHO - 1,
        y,
        x,
        y + OBST_ALTO - 1,
        1
    )


def dibujar_pista():

    # laterales
    oled.frame.vline(
        2,
        10,
        54,
        1
    )

    oled.frame.vline(
        125,
        10,
        54,
        1
    )

    # linea central discontinua
    for y in range(12, 64, 12):

        oled.frame.vline(
            63,
            y,
            6,
            1
        )


def colision(carro_x, obst):

    obst_x = obst["x"]
    obst_y = obst["y"]

    carro_izq = carro_x
    carro_der = carro_x + CARRO_ANCHO

    carro_arriba = CARRO_Y
    carro_abajo = CARRO_Y + CARRO_ALTO

    obst_izq = obst_x
    obst_der = obst_x + OBST_ANCHO

    obst_arriba = obst_y
    obst_abajo = obst_y + OBST_ALTO

    choque_x = (
        carro_izq < obst_der
        and carro_der > obst_izq
    )

    choque_y = (
        carro_arriba < obst_abajo
        and carro_abajo > obst_arriba
    )

    return choque_x and choque_y


def crear_obstaculo(y=-10):

    return {
        "x": randint(
            6,
            ANCHO - OBST_ANCHO - 6
        ),
        "y": y
    }


def cantidad_obstaculos(puntos):

    if puntos < 5:
        return 1

    elif puntos < 10:
        return 2

    else:
        return 3


def velocidad_juego(puntos):

    if puntos < 5:
        return 2

    elif puntos < 10:
        return 3

    elif puntos < 15:
        return 4

    else:
        return 5


def pantalla_inicio():

    oled.limpiar()

    oled.texto(
        "CARRERA",
        36,
        7
    )

    oled.texto(
        "ESQUIVA!",
        32,
        25
    )

    oled.texto(
        "Usa el POT",
        22,
        42
    )

    oled.mostrar()

    sleep(2)

    for numero in [3, 2, 1]:

        oled.limpiar()

        oled.texto(
            "CARRERA",
            36,
            10
        )

        oled.texto(
            str(numero),
            60,
            34
        )

        oled.mostrar()

        sleep(1)


def game_over(puntos):

    oled.limpiar()

    oled.texto(
        "GAME OVER",
        28,
        8
    )

    oled.texto(
        "PUNTOS:",
        32,
        28
    )

    oled.texto(
        str(puntos),
        58,
        42
    )

    if puntos >= 10:

        oled.texto(
            "BUENA PARTIDA!",
            8,
            54
        )

    oled.mostrar()


def jugar_carrera():

    pantalla_inicio()

    puntos = 0

    obstaculos = [
        crear_obstaculo(5)
    ]

    ultimo_movimiento = ticks_ms()

    jugando = True

    while jugando:

        ahora = ticks_ms()

        velocidad = velocidad_juego(
            puntos
        )

        cantidad = cantidad_obstaculos(
            puntos
        )

        # Agregar obstáculos según puntaje
        while len(obstaculos) < cantidad:

            separacion = -20 * len(obstaculos)

            obstaculos.append(
                crear_obstaculo(
                    separacion
                )
            )

        # mover obstáculos
        if ticks_diff(
            ahora,
            ultimo_movimiento
        ) >= 70:

            ultimo_movimiento = ahora

            for obst in obstaculos:

                obst["y"] += velocidad

                if obst["y"] > ALTO:

                    puntos += 1

                    obst["y"] = randint(
                        -30,
                        -10
                    )

                    obst["x"] = randint(
                        6,
                        ANCHO - OBST_ANCHO - 6
                    )

        carro_x = leer_posicion_carro()

        # comprobar choques
        for obst in obstaculos:

            if colision(
                carro_x,
                obst
            ):

                jugando = False

        # limpiar framebuffer
        oled.frame.fill(0)

        # encabezado
        oled.frame.text(
            "P:" + str(puntos),
            4,
            1,
            1
        )

        oled.frame.text(
            "V:" + str(velocidad),
            90,
            1,
            1
        )

        dibujar_pista()

        for obst in obstaculos:

            if obst["y"] > 8:

                dibujar_obstaculo(
                    obst["x"],
                    obst["y"]
                )

        dibujar_carro(
            carro_x
        )

        oled.mostrar()

        sleep(0.01)

    game_over(
        puntos
    )


if __name__ == "__main__":
    jugar_carrera()