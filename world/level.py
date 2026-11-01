"""Distribución del nivel y de la arena: suelo, plataformas, baterías, enemigos y portal."""

import pygame

import config as c
from entities.enemies import EnemigoPatrulla
from world import theme

# Tramos de suelo como (x_inicio, ancho). Los espacios entre tramos son los huecos:
#   hueco 1: de x=700 a x=820   |   hueco 2: de x=1700 a x=1830
TRAMOS_SUELO = [
    (0, 700),
    (820, 880),
    (1830, 1050),
]

# Plataformas flotantes como (x, y, ancho). Todas miden 20 px de alto.
# Ninguna está a más de 110 px por encima de la anterior (el salto alcanza 136 px).
PLATAFORMAS = [
    (300, 440, 140),
    (520, 340, 110),
    (900, 430, 140),
    (1110, 330, 110),
    (1380, 430, 240),
    (1950, 430, 140),
    (2160, 330, 110),
    (2450, 430, 120),
]

# Baterías como (x, y) de su esquina superior izquierda.
BATERIAS = [
    (360, 400),   # sobre la plataforma 1
    (565, 250),   # sobre la plataforma 2 (hay que saltar estando encima)
    (750, 420),   # encima del hueco 1 (se recoge al saltarlo)
    (1155, 290),  # sobre la plataforma 4
    (1490, 390),  # sobre la plataforma 5, donde patrulla un enemigo
    (1755, 440),  # encima del hueco 2 (se recoge al saltarlo)
]

# Zonas de patrulla como (límite_izq, límite_der, y_de_la_superficie).
# El primero empieza a más de 300 px del punto de aparición.
ZONAS_ENEMIGOS = [
    (430, 690, c.ALTURA_SUELO),    # suelo del primer tramo, antes del hueco 1
    (1380, 1620, 430),             # encima de la plataforma 5 (sus mismos bordes)
    (2050, 2500, c.ALTURA_SUELO),  # suelo del último tramo, antes del portal
]
POSICION_INICIAL = (80, c.ALTURA_SUELO - 48)  # esquina superior izquierda (de pie)
PORTAL = (2740, c.ALTURA_SUELO - 110, 70, 110)  # (x, y, ancho, alto)

# Arena del jefe: ocupa exactamente la ventana (sin cámara)
POSICION_INICIAL_ARENA = (80, c.ALTURA_SUELO - 48)  # extremo izquierdo
ZONA_JEFE = (560, 920)  # el jefe se mueve entre estos dos límites (lado derecho)


class Bateria:
    """Objeto coleccionable. Cada una se cuenta una sola vez."""

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 28)
        self.recogida = False

    def dibujar(self, pantalla, camara_x):
        if self.recogida:
            return
        x = self.rect.x - camara_x
        y = self.rect.y
        pygame.draw.rect(pantalla, theme.BATERIA_BORDE, (x + 6, y, 8, 4))  # terminal
        pygame.draw.rect(pantalla, theme.BATERIA, (x, y + 4, 20, 24), border_radius=3)
        pygame.draw.rect(pantalla, theme.BATERIA_BORDE, (x, y + 4, 20, 24), 2, border_radius=3)
        pygame.draw.rect(pantalla, theme.TEXTO, (x + 4, y + 14, 12, 4))  # franja de carga


def crear_solidos():
    """Tramos de suelo y plataformas del nivel."""
    solidos = []
    for x, ancho in TRAMOS_SUELO:
        solidos.append(pygame.Rect(x, c.ALTURA_SUELO, ancho, c.ALTO_VENTANA - c.ALTURA_SUELO))
    for x, y, ancho in PLATAFORMAS:
        solidos.append(pygame.Rect(x, y, ancho, 20))
    return solidos


def crear_solidos_arena():
    """La arena solo tiene un suelo continuo de borde a borde."""
    return [pygame.Rect(0, c.ALTURA_SUELO, c.ANCHO_VENTANA, c.ALTO_VENTANA - c.ALTURA_SUELO)]


def crear_enemigos():
    return [EnemigoPatrulla(*zona) for zona in ZONAS_ENEMIGOS]


def crear_baterias():
    return [Bateria(x, y) for x, y in BATERIAS]


def crear_portal():
    return pygame.Rect(PORTAL)
