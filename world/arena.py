"""Distribución de las arenas: suelo continuo, plataformas opcionales y posición inicial."""

import pygame

import config as c

POSICION_INICIAL_ROBOT = (80, c.ALTURA_SUELO - 48)  # extremo izquierdo, de pie


def crear_solidos(plataformas=()):
    """Suelo de borde a borde y, si el jefe las pide, plataformas como (x, y, ancho)."""
    solidos = [pygame.Rect(0, c.ALTURA_SUELO, c.ANCHO_VENTANA, c.ALTO_VENTANA - c.ALTURA_SUELO)]
    for x, y, ancho in plataformas:
        solidos.append(pygame.Rect(x, y, ancho, 20))
    return solidos
