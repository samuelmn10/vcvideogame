"""Jefe 1: Centinela Eclipse (dificultad inicial).

Enseña a reconocer avisos y esquivar: patrulla despacio por el suelo y alterna
proyectiles bajos (se saltan) y ráfagas dirigidas (se esquivan agachado o moviéndose).
En la fase 2 dispara más seguido y agrega una ráfaga adicional.
"""

import pygame

import config as c
from entities.bosses.base import AVISO, TRANSICION, JefeBase
from entities.projectiles import Proyectil
from world import theme

# Parámetros (pasos de 1/60 s)
AVISO_PASOS = 48             # 0,8 s
DESCANSO_PASOS = 84          # 1,4 s
VELOCIDAD = 1.5              # patrulla lenta
VELOCIDAD_FASE_2 = 1.8
# Fase 1
INTERVALO_BAJOS = 45         # 3 proyectiles bajos separados ~225 px
INTERVALO_RAFAGA = 24        # 3 disparos dirigidos
# Fase 2: más frecuencia y una ráfaga adicional
INTERVALO_BAJOS_2 = 36
INTERVALO_RAFAGA_2 = 18
PAUSA_ENTRE_RAFAGAS = 40     # entre la primera ráfaga y la adicional
LIMITES = (420, 920)         # zona de patrulla

BAJOS = "proyectiles bajos"
RAFAGA = "ráfaga dirigida"
DOBLE_RAFAGA = "ráfaga doble"


class CentinelaEclipse(JefeBase):
    NOMBRE = "Centinela Eclipse"
    DIFICULTAD = "Inicial"
    DESCRIPCION = (
        "Sistema de defensa que patrulla despacio por el suelo.",
        "Fase 1: proyectiles bajos (sáltalos) y ráfagas dirigidas.",
        "Fase 2: dispara más seguido y suma una ráfaga adicional.",
        "Avisos de 0,8 s y descansos de 1,4 s: aprende a leerlos.",
    )
    NOMBRE_FASE_1 = "Vigilancia"
    NOMBRE_FASE_2 = "Sobrecarga"
    VIDA_FASE_1 = 24
    VIDA_FASE_2 = 32
    AVISO_MINIMO = AVISO_PASOS
    DESCANSO_MINIMO = DESCANSO_PASOS
    ANCHO = 100
    ALTO = 120

    def __init__(self):
        super().__init__()
        self.direccion = -1
        self.disparos = 0   # disparos hechos en el ataque actual
        self.espera = 0     # pasos hasta el próximo disparo

    def patrones(self):
        return (BAJOS, RAFAGA) if not self.en_segunda_fase() else (BAJOS, DOBLE_RAFAGA)

    def duracion_aviso(self):
        return AVISO_PASOS

    def duracion_descanso(self):
        return DESCANSO_PASOS

    def mover_en_descanso(self, robot):
        velocidad = VELOCIDAD_FASE_2 if self.en_segunda_fase() else VELOCIDAD
        self.patrullar(robot, velocidad, *LIMITES)
        return False  # patrulla mientras corre el descanso

    def iniciar_ataque(self, robot):
        self.disparos = 0
        self.espera = 0

    def punto_canon(self):
        x = self.rect.right if self.mirando_derecha else self.rect.left
        return x, self.rect.top + 70

    def paso_ataque(self, robot, proyectiles):
        if self.espera > 0:
            self.espera -= 1
            return False
        patron = self.patron()
        total = 6 if patron == DOBLE_RAFAGA else 3
        if self.disparos >= total:
            return True
        if not self.cabe(proyectiles):
            return False  # hay 12 proyectiles: espera
        x, y = self.punto_canon()
        lado = 1 if self.mirando_derecha else -1
        segunda = self.en_segunda_fase()
        if patron == BAJOS:
            proyectiles.append(Proyectil(x, c.ALTURA_SUELO - 9, lado, 0, c.VELOCIDAD_PROYECTIL, aliado=False, bajo=True))
            self.espera = INTERVALO_BAJOS_2 if segunda else INTERVALO_BAJOS
        else:
            # Cada disparo apunta al pecho del robot en ese momento
            proyectiles.append(self.disparo_dirigido(x, y, self.pecho(robot)))
            self.espera = INTERVALO_RAFAGA_2 if segunda else INTERVALO_RAFAGA
            if patron == DOBLE_RAFAGA and self.disparos == 2:
                self.espera = PAUSA_ENTRE_RAFAGAS
        self.disparos += 1
        return False

    def dibujar(self, pantalla):
        r = self.rect
        color = self.color_actual(theme.CENTINELA_1, theme.CENTINELA_2)
        pygame.draw.rect(pantalla, theme.JEFE_OSCURO, (r.x + 4, r.bottom - 20, r.width - 8, 20), border_radius=8)
        pygame.draw.rect(pantalla, color, (r.x + 10, r.y + 40, r.width - 20, 62), border_radius=10)
        pygame.draw.rect(pantalla, color, (r.x + 22, r.y, r.width - 44, 44), border_radius=8)
        rejilla = theme.AVISO if self.en_segunda_fase() else theme.JEFE_OSCURO
        for i in range(3):
            pygame.draw.rect(pantalla, rejilla, (r.x + 24, r.y + 52 + i * 14, r.width - 48, 6), border_radius=3)
        # Ojo de eclipse: aro brillante tapado en parte por un disco oscuro
        ojo_x = r.centerx + (8 if self.mirando_derecha else -8)
        brillo = theme.AVISO if self.estado == AVISO and self.fase != TRANSICION else theme.OJO_JEFE
        pygame.draw.circle(pantalla, brillo, (ojo_x, r.y + 22), 12)
        pygame.draw.circle(pantalla, theme.JEFE_OSCURO, (ojo_x - (5 if self.mirando_derecha else -5), r.y + 20), 10)
        canon = pygame.Rect(0, 0, 26, 16)
        canon.center = self.punto_canon()
        pygame.draw.rect(pantalla, theme.JEFE_OSCURO, canon, border_radius=4)
        if self.fase == TRANSICION:
            self.dibujar_transicion(pantalla)
        elif self.estado == AVISO:
            self.dibujar_senal_aviso(pantalla)
            x, y = self.punto_canon()
            if self.patron() == BAJOS:
                ancho = 140
                inicio = r.right if self.mirando_derecha else r.left - ancho
                pygame.draw.rect(pantalla, theme.AVISO, (inicio, c.ALTURA_SUELO - 6, ancho, 6))
            else:
                pygame.draw.circle(pantalla, theme.AVISO, (x, y), 13, 3)
                if self.patron() == DOBLE_RAFAGA:
                    pygame.draw.circle(pantalla, theme.AVISO, (x, y), 20, 2)
