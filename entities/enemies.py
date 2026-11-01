"""Enemigos comunes del nivel.

Por ahora hay un solo tipo (patrulla). Un tipo nuevo sería otra clase pequeña
con los mismos métodos actualizar() y dibujar().
"""

import pygame

import config as c
from world import theme


class EnemigoPatrulla:
    """Camina de un lado a otro dentro de su zona, sobre el suelo o una plataforma."""

    ANCHO = 44
    ALTO = 32

    def __init__(self, limite_izq, limite_der, superficie_y):
        self.limite_izq = limite_izq
        self.limite_der = limite_der
        self.rect = pygame.Rect(limite_izq, superficie_y - self.ALTO, self.ANCHO, self.ALTO)
        self.direccion = 1  # 1 = derecha, -1 = izquierda

    def actualizar(self):
        self.rect.x += c.VELOCIDAD_ENEMIGO * self.direccion
        # Al llegar a un límite, se corrige la posición y se da la vuelta
        if self.rect.right >= self.limite_der:
            self.rect.right = self.limite_der
            self.direccion = -1
        elif self.rect.left <= self.limite_izq:
            self.rect.left = self.limite_izq
            self.direccion = 1

    def dibujar(self, pantalla, camara_x):
        x = self.rect.x - camara_x
        y = self.rect.y
        # Púas en la parte superior
        for i in range(4):
            base = x + 4 + i * 10
            pygame.draw.polygon(pantalla, theme.ENEMIGO, [(base, y + 8), (base + 5, y - 4), (base + 10, y + 8)])
        # Cuerpo
        pygame.draw.rect(pantalla, theme.ENEMIGO, (x, y + 6, self.ANCHO, self.ALTO - 6), border_radius=8)
        # Ojos que miran hacia donde camina
        for ojo_x in (x + 14, x + 30):
            pygame.draw.circle(pantalla, theme.TEXTO, (ojo_x, y + 17), 5)
            pygame.draw.circle(pantalla, (0, 0, 0), (ojo_x + 2 * self.direccion, y + 17), 2)
