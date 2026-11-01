"""Jefe 3: Serafín Voltaico (dificultad avanzada).

Exige apuntar en varias direcciones y aprovechar el propulsor: vuela a posiciones
altas para atacar con abanicos descendentes y ráfagas dirigidas, y descansa en
posiciones bajas (ventanas de ataque alcanzables desde el suelo, con salto o con
el propulsor breve). En la fase 2 se mueve más rápido y combina sus patrones.
"""

import math

import pygame

import config as c
from entities.bosses.base import AVISO, TRANSICION, JefeBase
from world import theme

# Parámetros (pasos de 1/60 s)
AVISO_FASE_1 = 36            # 0,6 s
AVISO_FASE_2 = 30            # 0,5 s (mínimo pedido)
DESCANSO_PASOS = 48          # 0,8 s quieto en la posición baja (ventana de ataque)
VELOCIDAD = 4
VELOCIDAD_FASE_2 = 5.5
# Centros de las posiciones: altas para atacar, bajas para descansar
POSICIONES_ALTAS = ((220, 200), (480, 160), (740, 200))
POSICIONES_BAJAS = ((200, 400), (760, 400))  # lejos de la plataforma: nada tapa los disparos
ANGULOS_ABANICO = (-122, -106, -90, -74, -58)  # hacia abajo, separados 16°
GIRO_SEGUNDO_ABANICO = 8     # el segundo abanico se gira 8° para mover los huecos
PAUSA_ABANICOS = 30
INTERVALO_RAFAGA = 20

ABANICO = "abanico descendente"
RAFAGA = "descarga aérea"
COMBO = "abanico + ráfaga"
DOBLE_ABANICO = "lluvia doble"


class SerafinVoltaico(JefeBase):
    NOMBRE = "Serafín Voltaico"
    DIFICULTAD = "Avanzada"
    DESCRIPCION = (
        "Guardián volador de la cúpula de tormenta.",
        "Ataca desde arriba: abanicos descendentes y ráfagas dirigidas.",
        "Descansa abajo: esas son tus ventanas para dispararle.",
        "Fase 2: más rápido y combina patrones. Avisos de 0,5 s.",
    )
    NOMBRE_FASE_1 = "Vuelo"
    NOMBRE_FASE_2 = "Tormenta voltaica"
    VIDA_FASE_1 = 48
    VIDA_FASE_2 = 64
    AVISO_MINIMO = AVISO_FASE_2
    DESCANSO_MINIMO = DESCANSO_PASOS
    ANCHO = 90
    ALTO = 70
    FONDO = "cupula"
    PLATAFORMAS = ((400, 430, 160),)  # bajo la posición alta central, para alcanzarla sin volar

    def __init__(self):
        super().__init__()
        self.rect.center = POSICIONES_ALTAS[2]
        self.x, self.y = float(self.rect.x), float(self.rect.y)
        self.destino = POSICIONES_BAJAS[1]
        self.ciclo = 0          # para alternar las posiciones
        self.disparos = 0
        self.espera = 0
        self.objetivo = None

    def patrones(self):
        return (ABANICO, RAFAGA) if not self.en_segunda_fase() else (COMBO, DOBLE_ABANICO)

    def duracion_aviso(self):
        return AVISO_FASE_2 if self.en_segunda_fase() else AVISO_FASE_1

    def duracion_descanso(self):
        return DESCANSO_PASOS

    # ----- Vuelo entre posiciones -------------------------------------------
    def volar_hacia(self, destino):
        """Avanza hacia el destino. Devuelve True mientras todavía no llegó."""
        velocidad = VELOCIDAD_FASE_2 if self.en_segunda_fase() else VELOCIDAD
        dx = destino[0] - self.rect.width / 2 - self.x
        dy = destino[1] - self.rect.height / 2 - self.y
        distancia = math.hypot(dx, dy)
        if distancia <= velocidad:
            self.x += dx
            self.y += dy
            llego = True
        else:
            self.x += dx / distancia * velocidad
            self.y += dy / distancia * velocidad
            llego = False
        self.rect.topleft = (round(self.x), round(self.y))
        return not llego

    def mover_en_descanso(self, robot):
        # Baja a una posición baja. Mientras viaja, el descanso todavía no empieza a
        # contar (la clase base no resta el temporizador), así que al llegar se queda
        # quieto el descanso completo: esa es la ventana de ataque.
        self.destino = POSICIONES_BAJAS[self.ciclo % len(POSICIONES_BAJAS)]
        return self.volar_hacia(self.destino)

    def preparar_aviso(self, robot):
        self.ciclo += 1
        self.destino = POSICIONES_ALTAS[self.ciclo % len(POSICIONES_ALTAS)]

    def mover_en_aviso(self):
        return self.volar_hacia(self.destino)

    # ----- Ataques ----------------------------------------------------------
    def iniciar_ataque(self, robot):
        self.disparos = 0
        self.espera = 0

    def boca(self):
        return self.rect.centerx, self.rect.bottom - 6

    def lanzar_abanico(self, proyectiles, giro=0):
        x, y = self.boca()
        for grados in ANGULOS_ABANICO:
            proyectiles.append(self.disparo_en_angulo(x, y, grados + giro))

    def paso_ataque(self, robot, proyectiles):
        if self.espera > 0:
            self.espera -= 1
            return False
        patron = self.patron()
        x, y = self.boca()
        if patron == ABANICO or (patron == DOBLE_ABANICO):
            total = 1 if patron == ABANICO else 2
            if self.disparos >= total:
                return True
            if not self.cabe(proyectiles, len(ANGULOS_ABANICO)):
                return False
            self.lanzar_abanico(proyectiles, GIRO_SEGUNDO_ABANICO * self.disparos * (1 if self.ciclo % 2 else -1))
            self.disparos += 1
            self.espera = PAUSA_ABANICOS
            return False
        if patron == RAFAGA:
            if self.disparos >= 3:
                return True
            if not self.cabe(proyectiles):
                return False
            proyectiles.append(self.disparo_dirigido(x, y, self.pecho(robot)))
            self.disparos += 1
            self.espera = INTERVALO_RAFAGA
            return False
        # COMBO: primero un abanico y enseguida una ráfaga de 3
        if self.disparos >= 4:
            return True
        necesarios = len(ANGULOS_ABANICO) if self.disparos == 0 else 1
        if not self.cabe(proyectiles, necesarios):
            return False
        if self.disparos == 0:
            self.lanzar_abanico(proyectiles)
            self.espera = PAUSA_ABANICOS
        else:
            proyectiles.append(self.disparo_dirigido(x, y, self.pecho(robot)))
            self.espera = INTERVALO_RAFAGA
        self.disparos += 1
        return False

    # ----- Dibujo -----------------------------------------------------------
    def dibujar(self, pantalla):
        r = self.rect
        color = self.color_actual(theme.SERAFIN_1, theme.SERAFIN_2)
        cx, cy = r.center
        # Alas
        pygame.draw.polygon(pantalla, color, [(cx - 12, cy - 6), (r.left - 26, r.top - 4), (r.left + 4, cy + 14)])
        pygame.draw.polygon(pantalla, color, [(cx + 12, cy - 6), (r.right + 26, r.top - 4), (r.right - 4, cy + 14)])
        # Cuerpo en rombo con núcleo
        pygame.draw.polygon(pantalla, theme.JEFE_OSCURO, [(cx, r.top), (r.right - 18, cy), (cx, r.bottom), (r.left + 18, cy)])
        pygame.draw.polygon(pantalla, color, [(cx, r.top + 6), (r.right - 24, cy), (cx, r.bottom - 6), (r.left + 24, cy)], 3)
        brillo = theme.AVISO if self.estado == AVISO and self.fase != TRANSICION else theme.OJO_JEFE
        pygame.draw.circle(pantalla, brillo, (cx, cy), 9)
        # Halo
        pygame.draw.ellipse(pantalla, theme.RAYO, (cx - 22, r.top - 18, 44, 12), 2)
        if self.fase == TRANSICION:
            self.dibujar_transicion(pantalla)
        elif self.estado == AVISO:
            self.dibujar_senal_aviso(pantalla)
            x, y = self.boca()
            if self.patron() in (ABANICO, COMBO, DOBLE_ABANICO):
                for grados in ANGULOS_ABANICO:
                    radianes = math.radians(grados)
                    pygame.draw.line(pantalla, theme.AVISO, (x, y), (x + 50 * math.cos(radianes), y - 50 * math.sin(radianes)), 3)
            if self.patron() in (RAFAGA, COMBO):
                pygame.draw.circle(pantalla, theme.AVISO, (x, y), 14, 3)
