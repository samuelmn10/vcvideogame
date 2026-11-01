"""El jefe: vida, movimiento, fases y patrones de ataque."""

import math

import pygame

import config as c
from entities.projectiles import Proyectil
from world import theme

# Estados y patrones
AVISO = "aviso"
ATAQUE = "ataque"
DESCANSO = "descanso"
RAFAGA = "ráfaga"
BAJOS = "proyectiles bajos"


class Jefe:
    """Tres estados (aviso, ataque y descanso) y dos patrones alternados."""

    ANCHO = 100
    ALTO = 120

    def __init__(self, zona):
        self.zona = zona  # (límite izquierdo, límite derecho)
        self.rect = pygame.Rect(0, 0, self.ANCHO, self.ALTO)
        self.rect.bottomright = (zona[1], c.ALTURA_SUELO)  # extremo derecho
        self.x = float(self.rect.x)  # con decimales, porque en la fase 2 avanza 2,4 px
        self.vida = c.VIDA_JEFE
        self.fase = 1
        self.anuncio_fase = 0  # pasos que falta mostrar el texto "FASE 2"
        self.direccion = -1
        self.mirando_derecha = False
        self.estado = DESCANSO
        self.temporizador = c.DESCANSO_INICIAL  # pasos que faltan en el estado actual
        self.patron = RAFAGA                    # patrón que usará en el próximo ataque
        self.disparos_hechos = 0

    def en_segunda_fase(self):
        return self.fase == 2

    def vida_maxima(self):
        return c.VIDA_JEFE

    def recibir_impacto(self):
        """Resta un punto de vida y, si corresponde, pasa a la fase 2 (una sola vez)."""
        self.vida = max(0, self.vida - 1)
        if self.fase == 1 and self.vida <= c.VIDA_SEGUNDA_FASE:
            self.fase = 2
            self.anuncio_fase = c.DURACION_ANUNCIO_FASE

    def puede_danar(self):
        return True

    def derrotado(self):
        return self.vida <= 0

    def actualizar(self, robot, proyectiles):
        # Siempre mira hacia el robot
        self.mirando_derecha = robot.rect.centerx > self.rect.centerx
        self.temporizador -= 1
        if self.anuncio_fase > 0:
            self.anuncio_fase -= 1

        if self.estado == DESCANSO:
            self.mover()
            if self.temporizador <= 0:
                self.estado = AVISO
                self.temporizador = c.DURACION_AVISO
        elif self.estado == AVISO:
            if self.temporizador <= 0:
                self.estado = ATAQUE
                self.disparos_hechos = 0
        elif self.estado == ATAQUE and self.temporizador <= 0:
            if self.disparos_hechos < 3:
                self.disparar(robot, proyectiles)
                self.disparos_hechos += 1
                self.temporizador = c.INTERVALO_RAFAGA if self.patron == RAFAGA else c.INTERVALO_BAJOS
            else:
                # Terminó el patrón: descansa y deja listo el otro patrón
                self.estado = DESCANSO
                self.temporizador = c.DESCANSO_FASE_2 if self.en_segunda_fase() else c.DESCANSO_FASE_1
                self.patron = BAJOS if self.patron == RAFAGA else RAFAGA

    def mover(self):
        """Se desplaza de un lado a otro dentro de su zona."""
        velocidad = c.VELOCIDAD_JEFE_FASE_2 if self.en_segunda_fase() else c.VELOCIDAD_JEFE
        self.x += velocidad * self.direccion
        if self.x <= self.zona[0]:
            self.x = self.zona[0]
            self.direccion = 1
        elif self.x + self.ANCHO >= self.zona[1]:
            self.x = self.zona[1] - self.ANCHO
            self.direccion = -1
        self.rect.x = round(self.x)

    def punto_canon(self):
        """El cañón está en el costado que mira al robot."""
        x = self.rect.right if self.mirando_derecha else self.rect.left
        return x, self.rect.top + 70

    def disparar(self, robot, proyectiles):
        if len(proyectiles) >= c.MAX_PROYECTILES:
            return
        x, y = self.punto_canon()
        if self.patron == RAFAGA:
            # Apunta al pecho del robot en este momento; después sigue recto.
            # Si el robot se agacha después del disparo, le pasa por encima.
            dx = robot.rect.centerx - x
            dy = robot.rect.top + 10 - y
            distancia = math.hypot(dx, dy) or 1
            proyectiles.append(Proyectil(x, y, dx / distancia, dy / distancia, c.VELOCIDAD_PROYECTIL, aliado=False))
        else:
            # Proyectil bajo que rueda por el suelo hacia el lado del robot
            sentido = 1 if self.mirando_derecha else -1
            proyectiles.append(Proyectil(x, c.ALTURA_SUELO - 9, sentido, 0, c.VELOCIDAD_PROYECTIL,
                                         aliado=False, bajo=True))

    def dibujar(self, pantalla):
        r = self.rect
        color = theme.JEFE_FASE_2 if self.en_segunda_fase() else theme.JEFE_FASE_1
        # Orugas
        pygame.draw.rect(pantalla, theme.VISOR, (r.x + 4, r.bottom - 20, r.width - 8, 20), border_radius=8)
        # Cuerpo y cabeza
        pygame.draw.rect(pantalla, color, (r.x + 10, r.y + 40, r.width - 20, 62), border_radius=10)
        pygame.draw.rect(pantalla, color, (r.x + 22, r.y, r.width - 44, 44), border_radius=8)
        pygame.draw.rect(pantalla, theme.VISOR, (r.x + 28, r.y + 12, r.width - 56, 18), border_radius=5)
        # Ojo: se pone amarillo durante el aviso
        ojo = theme.AVISO if self.estado == AVISO else theme.OJO
        ojo_x = r.centerx + (10 if self.mirando_derecha else -10)
        pygame.draw.circle(pantalla, ojo, (ojo_x, r.y + 21), 7)
        # Cañón
        canon = pygame.Rect(0, 0, 26, 16)
        canon.center = self.punto_canon()
        pygame.draw.rect(pantalla, theme.VISOR, canon, border_radius=4)
        if self.estado == AVISO:
            self.dibujar_aviso(pantalla)

    def dibujar_aviso(self, pantalla):
        """Señal antes de atacar: triángulo con "!" y una pista del patrón."""
        cx, arriba = self.rect.centerx, self.rect.top
        pygame.draw.polygon(pantalla, theme.AVISO, [(cx, arriba - 62), (cx - 24, arriba - 18), (cx + 24, arriba - 18)])
        pygame.draw.line(pantalla, theme.VISOR, (cx, arriba - 50), (cx, arriba - 32), 4)
        pygame.draw.circle(pantalla, theme.VISOR, (cx, arriba - 25), 3)
        if self.patron == RAFAGA:
            pygame.draw.circle(pantalla, theme.AVISO, self.punto_canon(), 13, 3)
        else:
            ancho = 140
            x = self.rect.right if self.mirando_derecha else self.rect.left - ancho
            pygame.draw.rect(pantalla, theme.AVISO, (x, c.ALTURA_SUELO - 6, ancho, 6))
