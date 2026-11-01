"""Ambientación: colores, fuentes y dibujo del escenario.

Todas las decisiones visuales están aquí; la lógica del juego no conoce colores.
"""

import pygame

import config as c

# Colores (R, G, B)
CIELO = (22, 26, 52)
ESTRELLA = (200, 200, 240)
TORRE = (38, 44, 82)
SUELO = (70, 62, 90)
BORDE_SUELO = (90, 200, 170)
PLATAFORMA = (120, 130, 160)
BORDE_PLATAFORMA = (90, 200, 170)
ROBOT = (205, 215, 230)
VISOR = (30, 40, 60)
OJO = (80, 230, 255)
PECHO = (255, 150, 60)
ANTENA = (255, 220, 80)
ARMA = (60, 70, 90)
FUEGO = (255, 170, 50)
BATERIA = (90, 220, 120)
BATERIA_BORDE = (30, 90, 50)
ENEMIGO = (210, 60, 90)
PORTAL_EXTERIOR = (150, 80, 255)
PORTAL_INTERIOR = (90, 40, 200)
PORTAL_CENTRO = (220, 200, 255)
PULSO = (80, 230, 255)
PULSO_CENTRO = (235, 255, 255)
PROYECTIL = (255, 120, 200)
PROYECTIL_BAJO = (255, 140, 40)
LISTO = (90, 220, 120)
RECARGANDO = (130, 130, 150)
TEXTO = (255, 255, 255)
CORAZON = (235, 60, 80)
CORAZON_VACIO = (90, 90, 110)
ARENA = (34, 20, 44)
LUZ_ARENA = (52, 32, 66)
JEFE_FASE_1 = (110, 140, 200)
JEFE_FASE_2 = (220, 90, 50)
AVISO = (255, 220, 60)
BOTON = (60, 70, 120)
BOTON_ENCIMA = (95, 110, 190)
BORDE_BOTON = (130, 140, 190)


def crear_fuentes():
    """Se crean una sola vez (fuente por defecto de Pygame, sin archivos externos)."""
    return {
        "normal": pygame.font.Font(None, 36),
        "grande": pygame.font.Font(None, 72),
        "titulo": pygame.font.Font(None, 96),
    }


def crear_capa_oscura():
    """Capa semitransparente para los menús. Se crea una sola vez."""
    capa = pygame.Surface((c.ANCHO_VENTANA, c.ALTO_VENTANA), pygame.SRCALPHA)
    capa.fill((0, 0, 0, 170))
    return capa


def dibujar_fondo_nivel(pantalla, camara_x):
    pantalla.fill(CIELO)
    # Estrellas fijas en la pantalla
    for i in range(40):
        pygame.draw.circle(pantalla, ESTRELLA, ((i * 137) % c.ANCHO_VENTANA, (i * 59) % 300), 1)
    # Torres lejanas que se mueven a la mitad de velocidad (efecto de profundidad)
    alturas = (180, 260, 140, 220, 300, 160)
    for i in range(14):
        x = i * 150 - camara_x // 2
        alto = alturas[i % len(alturas)]
        pygame.draw.rect(pantalla, TORRE, (x, c.ALTURA_SUELO - alto, 90, alto))


def dibujar_fondo_arena(pantalla):
    pantalla.fill(ARENA)
    # Focos de luz decorativos
    for x in (160, 480, 800):
        pygame.draw.circle(pantalla, LUZ_ARENA, (x, 260), 120)


def dibujar_solido(pantalla, rect):
    """Suelo o plataforma (rect ya en coordenadas de pantalla)."""
    es_suelo = rect.top == c.ALTURA_SUELO
    color = SUELO if es_suelo else PLATAFORMA
    borde = BORDE_SUELO if es_suelo else BORDE_PLATAFORMA
    pygame.draw.rect(pantalla, color, rect)
    pygame.draw.rect(pantalla, borde, (rect.x, rect.y, rect.width, 5))


def dibujar_portal(pantalla, rect):
    pygame.draw.ellipse(pantalla, PORTAL_EXTERIOR, rect)
    pygame.draw.ellipse(pantalla, PORTAL_INTERIOR, rect.inflate(-16, -16))
    pygame.draw.ellipse(pantalla, PORTAL_CENTRO, rect.inflate(-40, -50))
