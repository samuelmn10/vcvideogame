"""Jefe 2: Embestidor Férreo (dificultad intermedia).

Exige combinar desplazamiento, salto y agacharse: es más rápido que el Centinela,
embiste una distancia fija que el aviso marca en el suelo (se esquiva saliendo de
la zona o saltando por encima) y lanza abanicos dirigidos con espacios entre los
proyectiles. En la fase 2 encadena una embestida con una
ráfaga, separadas por un segundo aviso.
"""

import math

import pygame

import config as c
from entities.bosses.base import AVISO, TRANSICION, JefeBase
from world import theme

# Parámetros (pasos de 1/60 s)
AVISO_PASOS = 40             # 0,67 s (mínimo pedido: 0,6 s)
DESCANSO_PASOS = 60          # 1 s entre secuencias
VELOCIDAD = 3                # patrulla (el Centinela va a 1,5)
VELOCIDAD_FASE_2 = 3.6
VELOCIDAD_EMBESTIDA = 8
VELOCIDAD_EMBESTIDA_2 = 9
DISTANCIA_EMBESTIDA = 320    # recorrido fijo de cada embestida (el aviso marca dónde termina)
DISTANCIA_EMBESTIDA_2 = 400
LIMITES = (0, c.ANCHO_VENTANA)   # nunca sale de la arena
ANGULOS_ABANICO = (-24, -12, 0, 12, 24)  # grados alrededor de la dirección hacia NEXO-7
PAUSA_DOBLE_ABANICO = 30
DESVIO_SEGUNDO_ABANICO = 6   # el segundo abanico se corre 6° para mover los huecos
AVISO_RAFAGA = 40            # aviso entre la embestida y la ráfaga (fase 2)
INTERVALO_RAFAGA = 16

EMBESTIDA = "embestida"
ABANICO = "abanico"
COMBO = "embestida + ráfaga"
DOBLE_ABANICO = "doble abanico"


class EmbestidorFerreo(JefeBase):
    NOMBRE = "Embestidor Férreo"
    DIFICULTAD = "Intermedia"
    DESCRIPCION = (
        "Máquina de carga blindada, más rápida que el Centinela.",
        "Embestida: la franja marca hasta dónde llega. Sal de ella o sáltalo.",
        "Abanico: cinco proyectiles hacia ti con espacios entre ellos.",
        "Fase 2: embestida, segundo aviso y ráfaga. Avisos de 0,67 s.",
    )
    NOMBRE_FASE_1 = "Arremetida"
    NOMBRE_FASE_2 = "Metal al rojo"
    VIDA_FASE_1 = 36
    VIDA_FASE_2 = 48
    AVISO_MINIMO = 36
    DESCANSO_MINIMO = DESCANSO_PASOS
    ANCHO = 84
    ALTO = 56    # bajo y angosto: el salto (136 px) lo supera con margen
    FONDO = "hangar"

    def __init__(self):
        super().__init__()
        self.direccion = -1
        self.direccion_embestida = -1
        self.destino_x = self.x    # dónde termina la embestida (borde izquierdo del jefe)
        self.etapa = ""        # etapa dentro del ataque actual
        self.espera = 0
        self.disparos = 0

    def patrones(self):
        return (EMBESTIDA, ABANICO) if not self.en_segunda_fase() else (COMBO, DOBLE_ABANICO)

    def duracion_aviso(self):
        return AVISO_PASOS

    def duracion_descanso(self):
        return DESCANSO_PASOS

    def mover_en_descanso(self, robot):
        velocidad = VELOCIDAD_FASE_2 if self.en_segunda_fase() else VELOCIDAD
        self.mover_x(velocidad, 40, c.ANCHO_VENTANA - 40)
        return False

    def preparar_aviso(self, robot):
        # La dirección y el punto final se deciden al empezar el aviso y se marcan en el suelo
        self.direccion_embestida = 1 if robot.rect.centerx > self.rect.centerx else -1
        distancia = DISTANCIA_EMBESTIDA_2 if self.en_segunda_fase() else DISTANCIA_EMBESTIDA
        destino = self.x + self.direccion_embestida * distancia
        self.destino_x = max(LIMITES[0], min(LIMITES[1] - self.ANCHO, destino))

    def iniciar_ataque(self, robot):
        self.etapa = "embestir" if self.patron() in (EMBESTIDA, COMBO) else "abanico"
        self.espera = 0
        self.disparos = 0

    def punto_canon(self):
        x = self.rect.right if self.mirando_derecha else self.rect.left
        return x, self.rect.top + 20

    def paso_ataque(self, robot, proyectiles):
        if self.etapa == "embestir":
            velocidad = VELOCIDAD_EMBESTIDA_2 if self.en_segunda_fase() else VELOCIDAD_EMBESTIDA
            self.direccion = self.direccion_embestida
            restante = abs(self.destino_x - self.x)
            self.x += self.direccion * min(velocidad, restante)
            self.rect.x = round(self.x)
            if restante <= velocidad:  # llegó al final marcado
                if self.patron() == EMBESTIDA:
                    return True
                self.etapa = "aviso_rafaga"
                self.espera = AVISO_RAFAGA
            return False
        if self.etapa == "aviso_rafaga":
            self.mirando_derecha = robot.rect.centerx > self.rect.centerx
            self.espera -= 1
            if self.espera <= 0:
                self.etapa = "rafaga"
            return False
        if self.espera > 0:
            self.espera -= 1
            return False
        if self.etapa == "rafaga":
            if self.disparos >= 3:
                return True
            if not self.cabe(proyectiles):
                return False
            x, y = self.punto_canon()
            proyectiles.append(self.disparo_dirigido(x, y, self.pecho(robot)))
            self.disparos += 1
            self.espera = INTERVALO_RAFAGA
            return False
        # Abanico (uno en la fase 1, dos seguidos en la fase 2)
        total = 2 if self.patron() == DOBLE_ABANICO else 1
        if self.disparos >= total:
            return True
        if not self.cabe(proyectiles, len(ANGULOS_ABANICO)):
            return False
        self.mirando_derecha = robot.rect.centerx > self.rect.centerx
        x, y = self.punto_canon()
        pecho = self.pecho(robot)
        centro = math.degrees(math.atan2(-(pecho[1] - y), pecho[0] - x))
        desvio = DESVIO_SEGUNDO_ABANICO if self.disparos == 1 else 0
        for grados in ANGULOS_ABANICO:
            proyectiles.append(self.disparo_en_angulo(x, y, centro + grados + desvio))
        self.disparos += 1
        self.espera = PAUSA_DOBLE_ABANICO
        return False

    # ----- Dibujo -----------------------------------------------------------
    def dibujar(self, pantalla):
        r = self.rect
        color = self.color_actual(theme.EMBESTIDOR_1, theme.EMBESTIDOR_2)
        frente = 1 if (self.mirando_derecha if self.estado != "ataque" or self.etapa != "embestir"
                       else self.direccion_embestida > 0) else -1
        # Orugas y cuerpo blindado
        pygame.draw.rect(pantalla, theme.JEFE_OSCURO, (r.x, r.bottom - 18, r.width, 18), border_radius=8)
        pygame.draw.rect(pantalla, color, (r.x + 4, r.y + 14, r.width - 8, r.height - 30), border_radius=8)
        # Ariete en el frente
        punta_x = r.right + 14 if frente > 0 else r.left - 14
        base_x = r.right - 6 if frente > 0 else r.left + 6
        pygame.draw.polygon(pantalla, theme.JEFE_OSCURO, [(base_x, r.y + 18), (punta_x, r.centery), (base_x, r.bottom - 22)])
        # Visor en ranura
        pygame.draw.rect(pantalla, theme.JEFE_OSCURO, (r.centerx - 30, r.y + 22, 60, 10), border_radius=4)
        brillo = theme.AVISO if (self.estado == AVISO or self.etapa == "aviso_rafaga") and self.fase != TRANSICION else theme.OJO_JEFE
        pygame.draw.rect(pantalla, brillo, (r.centerx - 8 + 14 * frente, r.y + 24, 16, 6), border_radius=3)
        if self.fase == TRANSICION:
            self.dibujar_transicion(pantalla)
            return
        if self.estado == AVISO:
            self.dibujar_senal_aviso(pantalla)
            if self.patron() in (EMBESTIDA, COMBO):
                # Franja en el suelo: la zona exacta que va a recorrer, con la flecha hasta el final
                d = self.direccion_embestida
                inicio = r.right if d > 0 else r.left
                fin = self.destino_x + self.ANCHO if d > 0 else self.destino_x
                izquierda, ancho = min(inicio, fin), abs(fin - inicio)
                pygame.draw.rect(pantalla, theme.AVISO, (izquierda, c.ALTURA_SUELO - 6, ancho, 6))
                y = c.ALTURA_SUELO - 22
                pygame.draw.line(pantalla, theme.AVISO, (inicio + d * 10, y), (fin - d * 18, y), 4)
                pygame.draw.polygon(pantalla, theme.AVISO, [(fin, y), (fin - d * 18, y - 10), (fin - d * 18, y + 10)])
            else:
                x, y = self.punto_canon()
                for grados in (-24, 0, 24):
                    radianes = math.radians(grados)
                    lado = 1 if self.mirando_derecha else -1
                    pygame.draw.line(pantalla, theme.AVISO, (x, y), (x + lado * 50 * math.cos(radianes), y - 50 * math.sin(radianes)), 3)
        elif self.etapa == "aviso_rafaga" and self.estado == "ataque":
            self.dibujar_senal_aviso(pantalla)
            pygame.draw.circle(pantalla, theme.AVISO, self.punto_canon(), 13, 3)
