"""NEXO-7, el robot explorador del jugador: salud, postura, energía, apuntado y ataque."""

import math

import pygame

import config as c
from entities.projectiles import Proyectil
from systems import collisions, movement
from world import theme


class Robot:
    ANCHO = 36
    ALTO = 48
    ALTO_AGACHADO = 24  # la mitad: los pies quedan en el mismo lugar

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, self.ANCHO, self.ALTO)
        self.vel_y = 0
        self.en_suelo = False
        self.apoyo = None  # sólido sobre el que está parado (None si está en el aire)
        self.agachado = False
        self.volando = False
        self.energia = c.ENERGIA_MAXIMA
        # Apuntado: lo decide el cursor, no el movimiento
        self.mirando_derecha = True
        self.angulo = 0.0  # grados respecto a la horizontal (positivo = hacia arriba)
        self.direccion_disparo = (1.0, 0.0)  # vector unitario
        # Salud y ataque
        self.vidas = c.VIDAS_MAXIMAS
        self.invulnerable = 0     # pasos que faltan de invulnerabilidad
        self.espera_disparo = 0   # pasos que faltan para poder disparar
        self.carga_super = 0      # pulsos acertados al jefe desde el último superataque

    # ----- Salud ------------------------------------------------------------
    def actualizar_temporizadores(self):
        if self.espera_disparo > 0:
            self.espera_disparo -= 1
        if self.invulnerable > 0:
            self.invulnerable -= 1

    def recibir_danio(self):
        """Resta un corazón, salvo durante la invulnerabilidad."""
        if self.invulnerable > 0:
            return
        self.vidas -= 1
        self.invulnerable = c.INVULNERABILIDAD

    def visible(self):
        # Durante la invulnerabilidad parpadea: se oculta 6 pasos y se muestra 6
        return self.invulnerable == 0 or (self.invulnerable // 6) % 2 == 0

    # ----- Postura ----------------------------------------------------------
    def agacharse(self):
        pies = self.rect.bottom
        self.rect.height = self.ALTO_AGACHADO
        self.rect.bottom = pies
        self.agachado = True

    def levantarse(self, solidos):
        """Recupera la altura normal solo si hay espacio libre encima."""
        de_pie = pygame.Rect(self.rect.x, self.rect.bottom - self.ALTO, self.ANCHO, self.ALTO)
        if not collisions.hay_espacio(de_pie, solidos):
            return False  # se quedaría metido en una plataforma
        self.rect = de_pie
        self.agachado = False
        return True

    def saltar(self, solidos):
        # Solo se puede saltar si está apoyado; si está agachado, primero se levanta
        if self.en_suelo:
            if self.agachado and not self.levantarse(solidos):
                return
            self.vel_y = movement.velocidad_de_salto()
            self.en_suelo = False

    # ----- Apuntado y ataque ------------------------------------------------
    def punto_arma(self):
        """Hombro del robot, desde donde sale el arma. Depende de la postura."""
        altura = 12 if self.agachado else 30
        return self.rect.centerx, self.rect.top + altura

    def origen_disparo(self):
        """Boca del arma: el hombro más el largo del arma en la dirección actual."""
        hombro_x, hombro_y = self.punto_arma()
        dir_x, dir_y = self.direccion_disparo
        return hombro_x + dir_x * c.LARGO_ARMA, hombro_y + dir_y * c.LARGO_ARMA

    def apuntar(self, objetivo_x, objetivo_y):
        """Orienta el arma hacia un punto del mundo.

        En el suelo el ángulo se limita a ±60°; en el aire (saltando, cayendo o
        con el propulsor) se puede apuntar en 360°, incluso hacia abajo.
        """
        hombro_x, hombro_y = self.punto_arma()
        dx = objetivo_x - hombro_x
        dy = objetivo_y - hombro_y
        distancia = math.hypot(dx, dy)
        if distancia < 1:
            return  # cursor sobre el arma: se conserva la última dirección válida
        if dx != 0:
            self.mirando_derecha = dx > 0
        lado = 1 if self.mirando_derecha else -1
        # En pantalla el eje Y crece hacia abajo; con -dy el ángulo positivo es hacia arriba.
        # Con abs(dx) se mide desde la horizontal del lado al que se apunta (rango reflejado).
        angulo = math.degrees(math.atan2(-dy, abs(dx)))
        if not self.en_suelo:
            # En el aire: dirección libre, normalizada (largo 1)
            self.angulo = angulo
            self.direccion_disparo = (dx / distancia, dy / distancia)
            return
        self.angulo = max(-c.ANGULO_MAXIMO, min(c.ANGULO_MAXIMO, angulo))
        radianes = math.radians(self.angulo)
        # cos y sin dan un vector de largo 1: la velocidad no depende de la distancia al cursor
        self.direccion_disparo = (lado * math.cos(radianes), -math.sin(radianes))

    def puede_disparar(self, pulsos_activos):
        return self.espera_disparo == 0 and pulsos_activos < c.MAX_PULSOS

    def registrar_acierto(self):
        """Un pulso acertó al jefe: suma carga al superataque (sin pasar del máximo)."""
        self.carga_super = min(c.ACIERTOS_SUPER, self.carga_super + 1)

    def super_listo(self):
        return self.carga_super >= c.ACIERTOS_SUPER

    def disparar_super(self):
        """Lanza la descarga de núcleo en la dirección del arma y vacía la carga."""
        self.carga_super = 0
        x, y = self.origen_disparo()
        dir_x, dir_y = self.direccion_disparo
        return Proyectil(x, y, dir_x, dir_y, c.VELOCIDAD_SUPER, aliado=True, alcance=c.ALCANCE_SUPER,
                         superataque=True, danio=c.DANIO_SUPER)

    def disparar(self):
        """Crea un pulso en la boca del arma y empieza la espera."""
        self.espera_disparo = c.ESPERA_PULSO
        x, y = self.origen_disparo()
        dir_x, dir_y = self.direccion_disparo
        return Proyectil(x, y, dir_x, dir_y, c.VELOCIDAD_PULSO, aliado=True, alcance=c.ALCANCE_PULSO)

    # ----- Movimiento -------------------------------------------------------
    def actualizar(self, teclas, solidos, ancho_mundo):
        # 0) Postura: se agacha solo apoyado; se levanta solo si hay espacio encima
        quiere_agacharse = movement.alguna_presionada(teclas, c.TECLAS_AGACHARSE)
        if quiere_agacharse and self.en_suelo and not self.agachado:
            self.agacharse()
        elif not quiere_agacharse and self.agachado:
            self.levantarse(solidos)

        # 1) Movimiento horizontal
        velocidad = c.VELOCIDAD_AGACHADO if self.agachado else c.VELOCIDAD_ROBOT
        dx = movement.desplazamiento_horizontal(teclas, velocidad)
        collisions.resolver_horizontal(self.rect, dx, solidos)
        collisions.limitar_horizontal(self.rect, ancho_mundo)

        # 2) Gravedad o propulsor (Shift, solo en el aire y con energía)
        usa_propulsor = movement.alguna_presionada(teclas, c.TECLAS_PROPULSOR)
        self.volando = usa_propulsor and not self.en_suelo and self.energia > 0
        if self.volando:
            self.energia = max(0, self.energia - c.GASTO_PROPULSOR)
            self.vel_y = movement.aplicar_propulsor(self.vel_y)
        else:
            self.vel_y = movement.aplicar_gravedad(self.vel_y)
        self.vel_y, self.apoyo = collisions.resolver_vertical(self.rect, self.vel_y, solidos)
        self.en_suelo = self.apoyo is not None

        # Tampoco puede salir por arriba de la pantalla al volar
        if self.rect.top < 0:
            self.rect.top = 0
            self.vel_y = max(self.vel_y, 0)

        # 3) El propulsor se recarga solo estando apoyado (nunca en el aire):
        #    de vacío a lleno en 1,5 s de contacto continuo
        if self.en_suelo:
            self.energia = min(c.ENERGIA_MAXIMA, self.energia + c.RECARGA_PROPULSOR)

    # ----- Dibujo -----------------------------------------------------------
    def dibujar(self, pantalla, camara_x):
        x = self.rect.x - camara_x
        y = self.rect.y
        centro_x = x + self.ANCHO // 2
        ojo_x = x + 22 if self.mirando_derecha else x + 14

        if self.agachado:
            # Agachado: cabeza baja, cuerpo comprimido y piernas dobladas
            pygame.draw.rect(pantalla, theme.ROBOT, (x + 3, y, 30, 14), border_radius=5)
            pygame.draw.rect(pantalla, theme.VISOR, (x + 7, y + 3, 22, 8), border_radius=3)
            pygame.draw.circle(pantalla, theme.OJO, (ojo_x, y + 7), 3)
            pygame.draw.rect(pantalla, theme.ROBOT, (x + 4, y + 13, 28, 8), border_radius=3)
            pygame.draw.rect(pantalla, theme.ROBOT, (x + 6, y + 20, 10, 4))
            pygame.draw.rect(pantalla, theme.ROBOT, (x + 20, y + 20, 10, 4))
        else:
            # Antena
            pygame.draw.line(pantalla, theme.ROBOT, (centro_x, y + 4), (centro_x, y - 4), 2)
            pygame.draw.circle(pantalla, theme.ANTENA, (centro_x, y - 5), 3)
            # Cabeza con visor y un ojo que mira hacia donde apunta
            pygame.draw.rect(pantalla, theme.ROBOT, (x + 3, y + 4, 30, 20), border_radius=6)
            pygame.draw.rect(pantalla, theme.VISOR, (x + 7, y + 9, 22, 10), border_radius=4)
            pygame.draw.circle(pantalla, theme.OJO, (ojo_x, y + 14), 4)
            # Cuerpo con un detalle en el pecho
            pygame.draw.rect(pantalla, theme.ROBOT, (x + 6, y + 24, 24, 17), border_radius=4)
            # El pecho brilla en amarillo cuando el superataque está listo
            pecho = theme.AVISO if self.super_listo() else theme.PECHO
            pygame.draw.rect(pantalla, pecho, (x + 14, y + 28, 8, 8), border_radius=2)
            # Piernas
            pygame.draw.rect(pantalla, theme.ROBOT, (x + 9, y + 41, 7, 7))
            pygame.draw.rect(pantalla, theme.ROBOT, (x + 20, y + 41, 7, 7))

        # Llama del propulsor
        if self.volando:
            base = self.rect.bottom
            pygame.draw.polygon(pantalla, theme.FUEGO, [(centro_x - 7, base), (centro_x + 7, base), (centro_x, base + 14)])
            pygame.draw.polygon(pantalla, theme.AVISO, [(centro_x - 3, base), (centro_x + 3, base), (centro_x, base + 7)])

        # Arma: un cañón del hombro a la boca, en la dirección real del disparo
        hombro_x, hombro_y = self.punto_arma()
        boca_x, boca_y = self.origen_disparo()
        pygame.draw.line(pantalla, theme.ARMA, (hombro_x - camara_x, hombro_y), (boca_x - camara_x, boca_y), 6)
        pygame.draw.circle(pantalla, theme.PULSO, (round(boca_x - camara_x), round(boca_y)), 3)
