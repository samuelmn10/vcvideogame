"""Proyectiles: pulsos de NEXO-7 (aliados) y disparos del jefe (hostiles)."""

import pygame

import config as c
from world import theme


class Proyectil:
    """Viaja en línea recta a velocidad constante. No persigue a nadie."""

    def __init__(self, x, y, dir_x, dir_y, velocidad, aliado, alcance=None, bajo=False, superataque=False, danio=1):
        # Posición con decimales para que las diagonales sean precisas
        self.x = x
        self.y = y
        self.dir_x = dir_x  # vector unitario (largo 1)
        self.dir_y = dir_y
        self.velocidad = velocidad
        self.aliado = aliado      # True = pulso de NEXO-7; False = disparo del jefe
        self.alcance = alcance    # distancia máxima o None (sin límite)
        self.bajo = bajo          # proyectil del jefe que rueda por el suelo
        self.superataque = superataque  # descarga de núcleo de NEXO-7 (clic derecho)
        self.danio = danio
        self.recorrido = 0.0
        if superataque:
            self.rect = pygame.Rect(0, 0, 36, 36)
        elif bajo:
            self.rect = pygame.Rect(0, 0, 24, 18)
        elif aliado:
            self.rect = pygame.Rect(0, 0, 14, 14)
        else:
            self.rect = pygame.Rect(0, 0, 16, 16)
        self.rect.center = (round(x), round(y))

    def actualizar(self):
        paso = self.velocidad
        if self.alcance is not None:
            # El último paso se recorta para no pasar del alcance. Como la dirección
            # mide 1, "paso" es la distancia real recorrida, también en diagonal.
            paso = min(paso, self.alcance - self.recorrido)
        self.x += self.dir_x * paso
        self.y += self.dir_y * paso
        self.recorrido += paso
        self.rect.center = (round(self.x), round(self.y))

    def debe_desaparecer(self, ancho_mundo):
        """True si llegó a su alcance o salió del escenario."""
        if self.alcance is not None and self.recorrido >= self.alcance:
            return True
        fuera = (self.rect.right < 0 or self.rect.left > ancho_mundo
                 or self.rect.bottom < 0 or self.rect.top > c.ALTO_VENTANA)
        # Los disparos del jefe también salen de la arena al atravesar el suelo
        return fuera or (not self.aliado and self.rect.top >= c.ALTURA_SUELO)

    def dibujar(self, pantalla, camara_x):
        centro = (self.rect.centerx - camara_x, self.rect.centery)
        if self.superataque:
            pygame.draw.circle(pantalla, theme.PULSO, centro, 18)
            pygame.draw.circle(pantalla, theme.AVISO, centro, 18, 3)
            pygame.draw.circle(pantalla, theme.PULSO_CENTRO, centro, 8)
        elif self.aliado:
            pygame.draw.circle(pantalla, theme.PULSO, centro, 7)
            pygame.draw.circle(pantalla, theme.PULSO_CENTRO, centro, 3)
        elif self.bajo:
            rect = self.rect.move(-camara_x, 0)
            pygame.draw.ellipse(pantalla, theme.PROYECTIL_BAJO, rect)
            pygame.draw.ellipse(pantalla, theme.AVISO, rect.inflate(-10, -8))
        else:
            pygame.draw.circle(pantalla, theme.PROYECTIL, centro, 8)
            pygame.draw.circle(pantalla, theme.TEXTO, centro, 3)
