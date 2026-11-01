"""El jefe Centinela Eclipse: vida, movimiento, fases y patrones de ataque.

Fases:   FASE_1 (40 de vida) -> TRANSICION (1,5 s) -> FASE_2 (60 de vida) -> derrotado
Estados dentro de cada fase: DESCANSO -> AVISO -> ATAQUE -> DESCANSO ...
"""

import math

import pygame

import config as c
from entities.projectiles import Proyectil
from world import theme

# Fases
FASE_1 = "fase 1"
TRANSICION = "transición"
FASE_2 = "fase 2"

# Estados
AVISO = "aviso"
ATAQUE = "ataque"
DESCANSO = "descanso"

# Patrones: cada fase alterna sus dos patrones en este orden
RAFAGA = "ráfaga"
BAJOS = "proyectiles bajos"
ABANICO = "abanico"
RAFAGAS_CORTAS = "ráfagas cortas"
PATRONES = {FASE_1: (RAFAGA, BAJOS), FASE_2: (ABANICO, RAFAGAS_CORTAS)}

# Cuántas emisiones tiene cada patrón (una emisión puede lanzar varios proyectiles)
EMISIONES = {
    RAFAGA: 3,
    BAJOS: 3,
    ABANICO: 1,
    RAFAGAS_CORTAS: c.RAFAGAS_CORTAS * c.DISPAROS_POR_RAFAGA_CORTA,
}


class Jefe:
    ANCHO = 100
    ALTO = 120

    def __init__(self, zona):
        self.zona = zona  # (límite izquierdo, límite derecho)
        self.rect = pygame.Rect(0, 0, self.ANCHO, self.ALTO)
        self.rect.bottomright = (zona[1], c.ALTURA_SUELO)  # extremo derecho
        self.x = float(self.rect.x)  # con decimales, porque en la fase 2 avanza 2,5 px
        self.direccion = -1
        self.mirando_derecha = False
        # Vida y fase
        self.fase = FASE_1
        self.vida_maxima = c.VIDA_FASE_1
        self.vida = c.VIDA_FASE_1
        self.transicion = 0  # pasos que faltan de la transición
        # Estado dentro de la fase
        self.estado = DESCANSO
        self.temporizador = c.DESCANSO_INICIAL  # pasos que faltan en el estado actual
        self.indice_patron = 0                  # 0 o 1: cuál de los dos patrones sigue
        self.emisiones = 0                      # emisiones hechas en el ataque actual
        self.objetivo = None                    # punto fijo de la ráfaga corta actual

    # ----- Consultas --------------------------------------------------------
    def patron(self):
        return PATRONES[self.fase][self.indice_patron]

    def en_segunda_fase(self):
        return self.fase == FASE_2

    def en_transicion(self):
        return self.fase == TRANSICION

    def progreso_transicion(self):
        """De 0 a 1 mientras dura la transición (para la barra que se recarga)."""
        return 1 - self.transicion / c.DURACION_TRANSICION

    def puede_recibir_danio(self):
        return self.fase != TRANSICION and self.vida > 0

    def puede_danar(self):
        # Durante la transición el contacto tampoco hace daño
        return self.fase != TRANSICION

    def derrotado(self):
        return self.fase == FASE_2 and self.vida <= 0

    # ----- Vida y fases -----------------------------------------------------
    def recibir_impacto(self, danio=1):
        if not self.puede_recibir_danio():
            return
        self.vida = max(0, self.vida - danio)
        if self.fase == FASE_1 and self.vida == 0:
            # Empieza la transición única hacia la fase 2
            self.fase = TRANSICION
            self.transicion = c.DURACION_TRANSICION
            self.estado = DESCANSO

    def terminar_transicion(self):
        # Recarga única: solo se llega aquí una vez, desde la fase 1
        self.fase = FASE_2
        self.vida_maxima = c.VIDA_FASE_2
        self.vida = c.VIDA_FASE_2
        self.estado = DESCANSO
        self.temporizador = c.DESCANSO_FASE_2
        self.indice_patron = 0

    # ----- Comportamiento ---------------------------------------------------
    def actualizar(self, robot, proyectiles):
        self.mirando_derecha = robot.rect.centerx > self.rect.centerx  # siempre mira al robot
        if self.fase == TRANSICION:
            self.transicion -= 1
            if self.transicion <= 0:
                self.terminar_transicion()
            return
        if self.derrotado():
            return

        self.temporizador -= 1
        if self.estado == DESCANSO:
            self.mover()
            if self.temporizador <= 0:
                self.estado = AVISO
                self.temporizador = c.AVISO_FASE_2 if self.en_segunda_fase() else c.AVISO_FASE_1
        elif self.estado == AVISO:
            if self.temporizador <= 0:
                self.estado = ATAQUE
                self.emisiones = 0
        elif self.estado == ATAQUE and self.temporizador <= 0:
            if self.emisiones < EMISIONES[self.patron()]:
                if not self.emitir(robot, proyectiles):
                    return  # límite de proyectiles: se reintenta en el próximo paso
                self.emisiones += 1
                self.temporizador = self.espera_tras_emision()
            else:
                # Terminó el patrón: descansa y deja listo el otro
                self.estado = DESCANSO
                self.temporizador = c.DESCANSO_FASE_2 if self.en_segunda_fase() else c.DESCANSO_FASE_1
                self.indice_patron = 1 - self.indice_patron

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

    def espera_tras_emision(self):
        patron = self.patron()
        if patron == RAFAGA:
            return c.INTERVALO_RAFAGA
        if patron == BAJOS:
            return c.INTERVALO_BAJOS
        if patron == ABANICO:
            return c.PAUSA_TRAS_ABANICO
        # Ráfagas cortas: poco tiempo dentro de una ráfaga y más entre ráfagas
        if self.emisiones % c.DISPAROS_POR_RAFAGA_CORTA == 0:
            return c.INTERVALO_ENTRE_RAFAGAS
        return c.INTERVALO_EN_RAFAGA_CORTA

    def punto_canon(self):
        """El cañón está en el costado que mira al robot."""
        x = self.rect.right if self.mirando_derecha else self.rect.left
        return x, self.rect.top + 70

    def emitir(self, robot, proyectiles):
        """Lanza la siguiente emisión del patrón. Devuelve False si debe esperar."""
        patron = self.patron()
        necesarios = len(c.ANGULOS_ABANICO) if patron == ABANICO else 1
        if len(proyectiles) + necesarios > c.MAX_PROYECTILES:
            return False
        x, y = self.punto_canon()
        lado = 1 if self.mirando_derecha else -1
        pecho = (robot.rect.centerx, robot.rect.top + 10)
        if patron == RAFAGA:
            # Cada disparo apunta al pecho del robot en ese momento
            proyectiles.append(self.disparo_dirigido(x, y, pecho))
        elif patron == BAJOS:
            proyectiles.append(Proyectil(x, c.ALTURA_SUELO - 9, lado, 0, c.VELOCIDAD_PROYECTIL,
                                         aliado=False, bajo=True))
        elif patron == ABANICO:
            # Cinco proyectiles separados 15°, desde la horizontal hacia arriba
            for grados in c.ANGULOS_ABANICO:
                radianes = math.radians(grados)
                proyectiles.append(Proyectil(x, y, lado * math.cos(radianes), -math.sin(radianes),
                                             c.VELOCIDAD_PROYECTIL, aliado=False))
        else:
            # Ráfagas cortas: el objetivo se fija al comenzar cada ráfaga
            if self.emisiones % c.DISPAROS_POR_RAFAGA_CORTA == 0:
                self.objetivo = pecho
            proyectiles.append(self.disparo_dirigido(x, y, self.objetivo))
        return True

    def disparo_dirigido(self, x, y, objetivo):
        """Proyectil hacia un punto fijo; después sigue recto (no persigue)."""
        dx = objetivo[0] - x
        dy = objetivo[1] - y
        distancia = math.hypot(dx, dy) or 1
        return Proyectil(x, y, dx / distancia, dy / distancia, c.VELOCIDAD_PROYECTIL, aliado=False)

    # ----- Dibujo -----------------------------------------------------------
    def color_actual(self):
        if self.fase == TRANSICION:
            # Parpadea entre los dos colores mientras se sobrecarga
            return theme.JEFE_FASE_2 if (self.transicion // 6) % 2 == 0 else theme.JEFE_FASE_1
        return theme.JEFE_FASE_2 if self.en_segunda_fase() else theme.JEFE_FASE_1

    def dibujar(self, pantalla):
        r = self.rect
        color = self.color_actual()
        # Base de orugas
        pygame.draw.rect(pantalla, theme.JEFE_OSCURO, (r.x + 4, r.bottom - 20, r.width - 8, 20), border_radius=8)
        # Cuerpo y cabeza
        pygame.draw.rect(pantalla, color, (r.x + 10, r.y + 40, r.width - 20, 62), border_radius=10)
        pygame.draw.rect(pantalla, color, (r.x + 22, r.y, r.width - 44, 44), border_radius=8)
        # Rejillas de ventilación: en la fase 2 brillan por la sobrecarga
        rejilla = theme.AVISO if self.en_segunda_fase() else theme.JEFE_OSCURO
        for i in range(3):
            pygame.draw.rect(pantalla, rejilla, (r.x + 24, r.y + 52 + i * 14, r.width - 48, 6), border_radius=3)
        # Ojo de eclipse: un aro brillante tapado en parte por un disco oscuro
        ojo_x = r.centerx + (8 if self.mirando_derecha else -8)
        brillo = theme.AVISO if self.estado == AVISO and self.fase != TRANSICION else theme.OJO_JEFE
        pygame.draw.circle(pantalla, brillo, (ojo_x, r.y + 22), 12)
        desplazamiento = 5 if self.mirando_derecha else -5
        pygame.draw.circle(pantalla, theme.JEFE_OSCURO, (ojo_x - desplazamiento, r.y + 20), 10)
        # Cañón
        canon = pygame.Rect(0, 0, 26, 16)
        canon.center = self.punto_canon()
        pygame.draw.rect(pantalla, theme.JEFE_OSCURO, canon, border_radius=4)
        if self.fase == TRANSICION:
            # Anillos de energía que crecen durante la sobrecarga
            radio = 40 + int(60 * self.progreso_transicion())
            pygame.draw.circle(pantalla, theme.JEFE_FASE_2, r.center, radio, 3)
        elif self.estado == AVISO:
            self.dibujar_aviso(pantalla)

    def dibujar_aviso(self, pantalla):
        """Señal antes de atacar: triángulo con "!" y una pista del patrón."""
        cx, arriba = self.rect.centerx, self.rect.top
        pygame.draw.polygon(pantalla, theme.AVISO, [(cx, arriba - 62), (cx - 24, arriba - 18), (cx + 24, arriba - 18)])
        pygame.draw.line(pantalla, theme.JEFE_OSCURO, (cx, arriba - 50), (cx, arriba - 32), 4)
        pygame.draw.circle(pantalla, theme.JEFE_OSCURO, (cx, arriba - 25), 3)
        x, y = self.punto_canon()
        lado = 1 if self.mirando_derecha else -1
        patron = self.patron()
        if patron == RAFAGA:
            pygame.draw.circle(pantalla, theme.AVISO, (x, y), 13, 3)
        elif patron == BAJOS:
            ancho = 140
            inicio = self.rect.right if self.mirando_derecha else self.rect.left - ancho
            pygame.draw.rect(pantalla, theme.AVISO, (inicio, c.ALTURA_SUELO - 6, ancho, 6))
        elif patron == ABANICO:
            # Cinco líneas cortas con las direcciones exactas del abanico
            for grados in c.ANGULOS_ABANICO:
                radianes = math.radians(grados)
                fin = (x + lado * math.cos(radianes) * 60, y - math.sin(radianes) * 60)
                pygame.draw.line(pantalla, theme.AVISO, (x, y), fin, 3)
        else:
            # Tres puntos: tres ráfagas cortas
            for i in range(3):
                pygame.draw.circle(pantalla, theme.AVISO, (x + lado * (18 + i * 16), y), 5)
