"""Lógica común a todos los jefes: dos barras de vida, transición única,
estados (descanso, aviso y ataque) y límite de proyectiles hostiles.

Cada jefe concreto (en su propio módulo) hereda de JefeBase y solo define:
    - sus datos (NOMBRE, VIDA_FASE_1, ...);
    - patrones(): los patrones que alterna en cada fase;
    - duracion_aviso() y duracion_descanso();
    - mover_en_descanso(robot) y, si lo necesita, preparar_aviso(robot);
    - iniciar_ataque(robot) y paso_ataque(robot, proyectiles), que devuelve True al terminar;
    - dibujar(pantalla).
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

# Estados dentro de una fase
DESCANSO = "descanso"
AVISO = "aviso"
ATAQUE = "ataque"


class JefeBase:
    # Datos que cada jefe redefine
    NOMBRE = "Jefe"
    DIFICULTAD = "Inicial"
    DESCRIPCION = ()
    NOMBRE_FASE_1 = "Fase 1"
    NOMBRE_FASE_2 = "Fase 2"
    VIDA_FASE_1 = 10
    VIDA_FASE_2 = 10
    AVISO_MINIMO = 36      # pasos mínimos de aviso que se le exigen a este jefe
    DESCANSO_MINIMO = 60   # pasos mínimos de descanso entre patrones
    ANCHO = 100
    ALTO = 100
    PLATAFORMAS = ()  # plataformas de su arena como (x, y, ancho)
    FONDO = "nucleo"  # fondo de su arena (ver world/theme.py)

    def __init__(self):
        self.rect = pygame.Rect(0, 0, self.ANCHO, self.ALTO)
        self.rect.bottomright = (c.ANCHO_VENTANA - 40, c.ALTURA_SUELO)  # extremo derecho
        self.x = float(self.rect.x)  # posición con decimales para velocidades no enteras
        self.y = float(self.rect.y)
        self.mirando_derecha = False
        self.fase = FASE_1
        self.vida_maxima = self.VIDA_FASE_1
        self.vida = self.VIDA_FASE_1
        self.transicion = 0              # pasos que faltan de la transición
        self.estado = DESCANSO
        self.temporizador = c.DESCANSO_INICIAL
        self.indice_patron = 0           # cuál de los patrones de la fase sigue

    # ----- Consultas --------------------------------------------------------
    def patron(self):
        patrones = self.patrones()
        return patrones[self.indice_patron % len(patrones)]

    def en_segunda_fase(self):
        return self.fase == FASE_2

    def en_transicion(self):
        return self.fase == TRANSICION

    def progreso_transicion(self):
        """De 0 a 1 mientras dura la transición (para la barra que se recarga)."""
        return 1 - self.transicion / c.DURACION_TRANSICION

    def nombre_fase(self):
        return self.NOMBRE_FASE_2 if self.fase != FASE_1 else self.NOMBRE_FASE_1

    def puede_recibir_danio(self):
        return self.fase != TRANSICION and self.vida > 0

    def puede_danar(self):
        # Durante la transición el contacto tampoco hace daño
        return self.fase != TRANSICION and not self.derrotado()

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

    def terminar_transicion(self):
        # Recarga única de la segunda barra: solo se llega aquí desde la fase 1
        self.fase = FASE_2
        self.vida_maxima = self.VIDA_FASE_2
        self.vida = self.VIDA_FASE_2
        self.estado = DESCANSO
        self.temporizador = self.duracion_descanso()
        self.indice_patron = 0

    # ----- Máquina de estados común -----------------------------------------
    def actualizar(self, robot, proyectiles):
        if self.fase == TRANSICION:
            self.transicion -= 1
            if self.transicion <= 0:
                self.terminar_transicion()
            return
        if self.derrotado():
            return

        if self.estado == DESCANSO:
            self.mirando_derecha = robot.rect.centerx > self.rect.centerx
            if self.mover_en_descanso(robot):  # True mientras todavía se está acomodando
                return
            self.temporizador -= 1
            if self.temporizador <= 0:
                self.estado = AVISO
                self.temporizador = self.duracion_aviso()
                self.preparar_aviso(robot)
        elif self.estado == AVISO:
            self.mirando_derecha = robot.rect.centerx > self.rect.centerx
            if self.mover_en_aviso():
                return
            self.temporizador -= 1
            if self.temporizador <= 0:
                self.estado = ATAQUE
                self.iniciar_ataque(robot)
        elif self.paso_ataque(robot, proyectiles):
            # Terminó el ataque: descansa y deja listo el siguiente patrón
            self.estado = DESCANSO
            self.temporizador = self.duracion_descanso()
            self.indice_patron += 1

    # Valores por defecto que cada jefe puede redefinir
    def mover_en_descanso(self, robot):
        return False

    def preparar_aviso(self, robot):
        pass

    def mover_en_aviso(self):
        return False

    # ----- Utilidades para los patrones -------------------------------------
    def cabe(self, proyectiles, cantidad=1):
        """True si se pueden lanzar 'cantidad' proyectiles sin pasar de 12.
        Si no caben, el patrón espera y lo vuelve a intentar en el siguiente paso."""
        return len(proyectiles) + cantidad <= c.MAX_PROYECTILES

    def mover_x(self, velocidad, limite_izq, limite_der):
        """Avanza en la dirección actual y rebota en los límites. Devuelve True si rebotó."""
        self.x += velocidad * self.direccion
        reboto = False
        if self.x <= limite_izq:
            self.x, self.direccion, reboto = limite_izq, 1, True
        elif self.x + self.ANCHO >= limite_der:
            self.x, self.direccion, reboto = limite_der - self.ANCHO, -1, True
        self.rect.x = round(self.x)
        return reboto

    def patrullar(self, robot, velocidad, limite_izq, limite_der):
        """Patrulla de un lado a otro sin acercarse a NEXO-7 más que DISTANCIA_PATRULLA.

        Así, entre ataques el jefe no atropella al robot sin aviso: solo hace daño
        con ataques anunciados, o si el jugador camina hacia él.
        """
        lado_robot = 1 if robot.rect.centerx > self.rect.centerx else -1
        separacion = (robot.rect.left - self.rect.right) if lado_robot > 0 else (self.rect.left - robot.rect.right)
        if separacion - velocidad < c.DISTANCIA_PATRULLA:
            self.direccion = -lado_robot  # demasiado cerca: se aleja del robot
        reboto = self.mover_x(velocidad, limite_izq, limite_der)
        if reboto and self.direccion == lado_robot and separacion < c.DISTANCIA_PATRULLA:
            # Contra la pared y con el robot cerca: se queda quieto en vez de ir hacia él
            self.direccion = -lado_robot
        return reboto

    def disparo_dirigido(self, x, y, objetivo, velocidad=c.VELOCIDAD_PROYECTIL):
        """Proyectil hacia un punto fijo; después sigue recto (no persigue)."""
        dx = objetivo[0] - x
        dy = objetivo[1] - y
        distancia = math.hypot(dx, dy) or 1
        return Proyectil(x, y, dx / distancia, dy / distancia, velocidad, aliado=False)

    def disparo_en_angulo(self, x, y, grados, velocidad=c.VELOCIDAD_PROYECTIL):
        """Proyectil en un ángulo fijo (0° = derecha, 90° = arriba, -90° = abajo)."""
        radianes = math.radians(grados)
        return Proyectil(x, y, math.cos(radianes), -math.sin(radianes), velocidad, aliado=False)

    @staticmethod
    def pecho(robot):
        return robot.rect.centerx, robot.rect.top + 10

    # ----- Dibujo común -----------------------------------------------------
    def color_actual(self, color_fase_1, color_fase_2):
        if self.fase == TRANSICION:
            # Parpadea entre los dos colores mientras cambia de fase
            return color_fase_2 if (self.transicion // 6) % 2 == 0 else color_fase_1
        return color_fase_2 if self.en_segunda_fase() else color_fase_1

    def dibujar_senal_aviso(self, pantalla):
        """Triángulo con "!" sobre el jefe mientras avisa."""
        cx, arriba = self.rect.centerx, self.rect.top
        pygame.draw.polygon(pantalla, theme.AVISO, [(cx, arriba - 58), (cx - 22, arriba - 18), (cx + 22, arriba - 18)])
        pygame.draw.line(pantalla, theme.JEFE_OSCURO, (cx, arriba - 47), (cx, arriba - 31), 4)
        pygame.draw.circle(pantalla, theme.JEFE_OSCURO, (cx, arriba - 25), 3)

    def dibujar_transicion(self, pantalla):
        radio = 40 + int(60 * self.progreso_transicion())
        pygame.draw.circle(pantalla, theme.AVISO, self.rect.center, radio, 3)
