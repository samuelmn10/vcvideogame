"""
RoboAventura - Mini-juego de plataformas 2D (versión 5).

Controles:
    A / D o flechas izquierda / derecha -> moverse
    Espacio                             -> saltar
    S o flecha abajo (en el suelo)      -> agacharse
    Shift (en el aire)                  -> propulsor (vuelo corto)
    Ratón                               -> apuntar (±60° hacia cada lado)
    Clic izquierdo (se puede mantener)  -> disparar pulsos de energía
    Clic izquierdo en los menús         -> botones: Iniciar, Pausa, Continuar,
                                           Reiniciar, Volver a jugar y Salir
"""

import math
import sys

import pygame

# ---------------------------------------------------------------------------
# Configuración general
# ---------------------------------------------------------------------------
ANCHO_VENTANA = 960
ALTO_VENTANA = 600
ANCHO_NIVEL = 2880
FPS = 60
PASO = 1 / FPS               # cada actualización simula siempre 1/60 s (paso fijo)

# Física: los valores están en píxeles por paso de 1/60 s.
GRAVEDAD = 1
VELOCIDAD_SALTO = -17        # negativo = hacia arriba (el eje Y crece hacia abajo)
VELOCIDAD_CAIDA_MAX = 15     # menor que el grosor de las plataformas para no atravesarlas
VELOCIDAD_JUGADOR = 5
VELOCIDAD_AGACHADO = 3       # más lento al estar agachado
VELOCIDAD_ENEMIGO = 3        # en la versión 1 era 2

# Propulsor (vuelo corto)
# La energía se cuenta en unidades enteras para evitar errores de redondeo:
# 360 unidades duran 2 s de uso (3 por paso) y se recargan en 1,5 s (4 por paso).
ENERGIA_MAXIMA = 360
GASTO_PROPULSOR = 3          # 360 / (2,0 s × 60 pasos)
RECARGA_PROPULSOR = 4        # 360 / (1,5 s × 60 pasos)
EMPUJE_PROPULSOR = 2         # contrarresta la gravedad (1) y deja 1 px/paso² hacia arriba
VELOCIDAD_SUBIDA_MAX = 6     # velocidad máxima de ascenso

# Apuntado
ANGULO_MAXIMO = 60           # grados hacia arriba o hacia abajo desde la horizontal
LARGO_ARMA = 20              # distancia del hombro a la boca del arma

# Pulso de energía
VELOCIDAD_PULSO = 8          # con 8 px/cuadro dura ~44 cuadros, así caben 2 pulsos activos
ALCANCE_PULSO = 350          # distancia máxima en píxeles desde el punto de lanzamiento
ESPERA_PULSO = 18            # 0,3 segundos de espera entre ataques (0,3 × 60 cuadros)
MAX_PULSOS = 2               # pulsos activos al mismo tiempo

# Vidas del robot
VIDAS_MAXIMAS = 3
INVULNERABILIDAD = 72        # 1,2 segundos sin recibir daño después de un golpe
MARGEN_SEGURO = 100          # distancia mínima a los bordes para guardar una posición segura

# Jefe
NOMBRE_JEFE = "VOLTARÓN"
VIDA_JEFE = 12
VIDA_SEGUNDA_FASE = 6        # con esta vida o menos empieza la fase 2
VELOCIDAD_JEFE = 2
VELOCIDAD_JEFE_FASE_2 = 2.4  # 20 % más rápido
DURACION_AVISO = 45          # 0,75 s de señal antes de cada ataque (mínimo pedido: 0,6 s)
DURACION_ANUNCIO_FASE = 90   # el texto "FASE 2" se muestra 1,5 s
DESCANSO_INICIAL = 120       # 2 s para ubicarse al entrar a la arena
DESCANSO_FASE_1 = 72         # 1,2 s entre patrones
DESCANSO_FASE_2 = 48         # 0,8 s entre patrones
INTERVALO_RAFAGA = 24        # cuadros entre los 3 disparos de la ráfaga
INTERVALO_BAJOS = 45         # cuadros entre los 3 proyectiles bajos (~225 px de separación)
VELOCIDAD_PROYECTIL = 5
MAX_PROYECTILES = 12

# Estados posibles del juego (cada uno es una pantalla)
INICIO = "inicio"
JUGANDO = "jugando"
PAUSA = "pausa"
DERROTA = "derrota"
VICTORIA = "victoria"

# Acciones de los botones
INICIAR = "iniciar"
PAUSAR = "pausar"
CONTINUAR = "continuar"
SALIR = "salir"

# Escenas
NIVEL = "nivel"
ARENA = "arena"

# Estados y patrones del jefe
AVISO = "aviso"
ATAQUE = "ataque"
DESCANSO = "descanso"
RAFAGA = "ráfaga"
BAJOS = "proyectiles bajos"

# Colores (R, G, B)
COLOR_CIELO = (22, 26, 52)
COLOR_ESTRELLA = (200, 200, 240)
COLOR_TORRE = (38, 44, 82)
COLOR_SUELO = (70, 62, 90)
COLOR_BORDE_SUELO = (90, 200, 170)
COLOR_PLATAFORMA = (120, 130, 160)
COLOR_BORDE_PLATAFORMA = (90, 200, 170)
COLOR_ROBOT = (205, 215, 230)
COLOR_VISOR = (30, 40, 60)
COLOR_OJO = (80, 230, 255)
COLOR_PECHO = (255, 150, 60)
COLOR_ANTENA = (255, 220, 80)
COLOR_BATERIA = (90, 220, 120)
COLOR_BATERIA_BORDE = (30, 90, 50)
COLOR_ENEMIGO = (210, 60, 90)
COLOR_PORTAL_EXTERIOR = (150, 80, 255)
COLOR_PORTAL_INTERIOR = (90, 40, 200)
COLOR_PORTAL_CENTRO = (220, 200, 255)
COLOR_PULSO = (80, 230, 255)
COLOR_PULSO_CENTRO = (235, 255, 255)
COLOR_LISTO = (90, 220, 120)
COLOR_RECARGANDO = (130, 130, 150)
COLOR_TEXTO = (255, 255, 255)
COLOR_CORAZON = (235, 60, 80)
COLOR_CORAZON_VACIO = (90, 90, 110)
COLOR_ARENA = (34, 20, 44)
COLOR_LUZ_ARENA = (52, 32, 66)
COLOR_JEFE_FASE_1 = (110, 140, 200)
COLOR_JEFE_FASE_2 = (220, 90, 50)
COLOR_AVISO = (255, 220, 60)
COLOR_PROYECTIL = (255, 120, 200)
COLOR_PROYECTIL_BAJO = (255, 140, 40)
COLOR_BOTON = (60, 70, 120)
COLOR_BOTON_ENCIMA = (95, 110, 190)
COLOR_BORDE_BOTON = (130, 140, 190)
COLOR_ARMA = (60, 70, 90)
COLOR_FUEGO = (255, 170, 50)

# ---------------------------------------------------------------------------
# Diseño del nivel
# ---------------------------------------------------------------------------
ALTURA_SUELO = 540  # coordenada Y de la parte superior del suelo

# Tramos de suelo como (x_inicio, ancho). Los espacios entre tramos son los huecos:
#   hueco 1: de x=700 a x=820   |   hueco 2: de x=1700 a x=1830
TRAMOS_SUELO = [
    (0, 700),
    (820, 880),
    (1830, 1050),
]

# Plataformas flotantes como (x, y, ancho). Todas miden 20 px de alto.
# Ninguna está a más de 110 px por encima de la anterior (el salto alcanza 136 px).
# Versión 2: las plataformas 2, 4 y 7 son más altas y angostas, y la 5 es más ancha
# para que un enemigo patrulle encima.
PLATAFORMAS = [
    (300, 440, 140),
    (520, 340, 110),
    (900, 430, 140),
    (1110, 330, 110),
    (1380, 430, 240),
    (1950, 430, 140),
    (2160, 330, 110),
    (2450, 430, 120),
]

# Baterías como (x, y) de su esquina superior izquierda.
BATERIAS = [
    (360, 400),   # sobre la plataforma 1
    (565, 250),   # sobre la plataforma 2 (hay que saltar estando encima)
    (750, 420),   # encima del hueco 1 (se recoge al saltarlo)
    (1155, 290),  # sobre la plataforma 4
    (1490, 390),  # sobre la plataforma 5, donde patrulla un enemigo
    (1755, 440),  # encima del hueco 2 (se recoge al saltarlo)
]

# Zonas de patrulla de los enemigos como (límite_izq, límite_der, y_de_la_superficie).
# El primero empieza a más de 300 px del punto de aparición del jugador.
ZONAS_ENEMIGOS = [
    (430, 690, ALTURA_SUELO),    # suelo del primer tramo, antes del hueco 1
    (1380, 1620, 430),           # encima de la plataforma 5 (sus mismos bordes)
    (2050, 2500, ALTURA_SUELO),  # suelo del último tramo, antes del portal
]
POSICION_INICIAL = (80, ALTURA_SUELO - 48)  # esquina superior izquierda (de pie)
PORTAL =(2740, ALTURA_SUELO - 110, 70, 110)  # (x, y, ancho, alto)

# Arena del jefe: ocupa exactamente la ventana (sin cámara)
POSICION_INICIAL_ARENA = (80, ALTURA_SUELO - 48)  # extremo izquierdo
ZONA_JEFE = (560, 920)  # el jefe se mueve entre estos dos límites (lado derecho)


def crear_solidos():
    """Devuelve la lista de rectángulos sólidos: tramos de suelo y plataformas."""
    solidos = []
    for x, ancho in TRAMOS_SUELO:
        solidos.append(pygame.Rect(x, ALTURA_SUELO, ancho, ALTO_VENTANA - ALTURA_SUELO))
    for x, y, ancho in PLATAFORMAS:
        solidos.append(pygame.Rect(x, y, ancho, 20))
    return solidos


def crear_solidos_arena():
    """La arena solo tiene un suelo continuo de borde a borde."""
    return [pygame.Rect(0, ALTURA_SUELO, ANCHO_VENTANA, ALTO_VENTANA - ALTURA_SUELO)]


def dibujar_corazon(pantalla, x, y, lleno):
    """Corazón hecho con dos círculos y un triángulo."""
    color = COLOR_CORAZON if lleno else COLOR_CORAZON_VACIO
    pygame.draw.circle(pantalla, color, (x + 7, y + 7), 7)
    pygame.draw.circle(pantalla, color, (x + 19, y + 7), 7)
    pygame.draw.polygon(pantalla, color, [(x, y + 9), (x + 26, y + 9), (x + 13, y + 24)])


# ---------------------------------------------------------------------------
# Entidades del juego
# ---------------------------------------------------------------------------
class Jugador:
    """El robot que controla el jugador."""

    ANCHO = 36
    ALTO = 48
    ALTO_AGACHADO = 24  # la mitad: los pies quedan en el mismo lugar

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, self.ANCHO, self.ALTO)
        self.vel_y = 0
        self.en_suelo = False
        self.apoyo = None  # sólido sobre el que está parado (None si está en el aire)
        self.mirando_derecha = True  # lo decide el apuntado, no el movimiento
        self.agachado = False
        self.volando = False
        self.energia = ENERGIA_MAXIMA  # energía del propulsor disponible
        self.angulo = 0.0  # grados respecto a la horizontal (positivo = hacia arriba)
        self.direccion_disparo = (1.0, 0.0)  # vector unitario hacia donde apunta el arma

    # ----- Postura ----------------------------------------------------------
    def agacharse(self):
        pies = self.rect.bottom
        self.rect.height = self.ALTO_AGACHADO
        self.rect.bottom = pies
        self.agachado = True

    def levantarse(self, solidos):
        """Recupera la altura normal solo si hay espacio libre encima."""
        de_pie = pygame.Rect(self.rect.x, self.rect.bottom - self.ALTO, self.ANCHO, self.ALTO)
        if de_pie.top < 0 or de_pie.collidelist(solidos) != -1:
            return False  # se quedaría metido en una plataforma
        self.rect = de_pie
        self.agachado = False
        return True

    def saltar(self, solidos):
        # Solo se puede saltar si está apoyado: así se evita saltar en el aire.
        # Si está agachado, primero intenta ponerse de pie.
        if self.en_suelo:
            if self.agachado and not self.levantarse(solidos):
                return
            self.vel_y = VELOCIDAD_SALTO
            self.en_suelo = False

    # ----- Apuntado ---------------------------------------------------------
    def punto_arma(self):
        """Hombro del robot, desde donde sale el arma. Depende de la postura."""
        altura = 12 if self.agachado else 30
        return self.rect.centerx, self.rect.top + altura

    def origen_disparo(self):
        """Boca del arma: el hombro más el largo del arma en la dirección actual."""
        hombro_x, hombro_y = self.punto_arma()
        dir_x, dir_y = self.direccion_disparo
        return hombro_x + dir_x * LARGO_ARMA, hombro_y + dir_y * LARGO_ARMA

    def apuntar(self, objetivo_x, objetivo_y):
        """Orienta el arma hacia un punto del mundo, con el ángulo limitado a ±60°."""
        hombro_x, hombro_y = self.punto_arma()
        dx = objetivo_x - hombro_x
        dy = objetivo_y - hombro_y
        if math.hypot(dx, dy) < 1:
            return  # cursor sobre el arma: se conserva la última dirección válida
        if dx != 0:
            self.mirando_derecha = dx > 0
        lado = 1 if self.mirando_derecha else -1
        # En pantalla el eje Y crece hacia abajo; con -dy el ángulo positivo es hacia arriba.
        # Con abs(dx) el ángulo se mide desde la horizontal del lado al que se apunta,
        # así el mismo rango sirve reflejado hacia la izquierda.
        angulo = math.degrees(math.atan2(-dy, abs(dx)))
        self.angulo = max(-ANGULO_MAXIMO, min(ANGULO_MAXIMO, angulo))
        radianes = math.radians(self.angulo)
        # cos y sin dan un vector de largo 1: la velocidad no depende de la distancia al cursor
        self.direccion_disparo = (lado * math.cos(radianes), -math.sin(radianes))

    # ----- Movimiento -------------------------------------------------------
    def actualizar(self, teclas, solidos, ancho_mundo):
        # 0) Postura: se agacha solo apoyado; se levanta solo si hay espacio encima
        quiere_agacharse = teclas[pygame.K_s] or teclas[pygame.K_DOWN]
        if quiere_agacharse and self.en_suelo and not self.agachado:
            self.agacharse()
        elif not quiere_agacharse and self.agachado:
            self.levantarse(solidos)

        # 1) Movimiento horizontal según las teclas presionadas
        velocidad = VELOCIDAD_AGACHADO if self.agachado else VELOCIDAD_JUGADOR
        dx = 0
        if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
            dx -= velocidad
        if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
            dx += velocidad

        self.rect.x += dx
        # Si choca de lado con un sólido, se pega a su borde
        for solido in solidos:
            if self.rect.colliderect(solido):
                if dx > 0:
                    self.rect.right = solido.left
                elif dx < 0:
                    self.rect.left = solido.right

        # No puede salir por los extremos del nivel o de la arena
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, ancho_mundo)

        # 2) Gravedad o propulsor (Shift, solo en el aire y con energía)
        usa_propulsor = teclas[pygame.K_LSHIFT] or teclas[pygame.K_RSHIFT]
        self.volando = usa_propulsor and not self.en_suelo and self.energia > 0
        if self.volando:
            self.energia = max(0, self.energia - GASTO_PROPULSOR)
            self.vel_y = max(self.vel_y + GRAVEDAD - EMPUJE_PROPULSOR, -VELOCIDAD_SUBIDA_MAX)
        else:
            self.vel_y = min(self.vel_y + GRAVEDAD, VELOCIDAD_CAIDA_MAX)
        self.rect.y += self.vel_y

        self.en_suelo = False
        self.apoyo = None
        for solido in solidos:
            if self.rect.colliderect(solido):
                if self.vel_y > 0:
                    # Venía cayendo: aterriza encima del sólido
                    self.rect.bottom = solido.top
                    self.en_suelo = True
                    self.apoyo = solido
                elif self.vel_y < 0:
                    # Venía subiendo: se golpea la cabeza por debajo (también volando)
                    self.rect.top = solido.bottom
                self.vel_y = 0

        # Tampoco puede salir por arriba de la pantalla al volar
        if self.rect.top < 0:
            self.rect.top = 0
            self.vel_y = max(self.vel_y, 0)

        # 3) El propulsor se recarga por completo en 1,5 s estando apoyado
        if self.en_suelo:
            self.energia = min(ENERGIA_MAXIMA, self.energia + RECARGA_PROPULSOR)

    # ----- Dibujo -----------------------------------------------------------
    def dibujar(self, pantalla, camara_x):
        x = self.rect.x - camara_x
        y = self.rect.y
        centro_x = x + self.ANCHO // 2
        ojo_x = x + 22 if self.mirando_derecha else x + 14

        if self.agachado:
            # Agachado: cabeza baja, cuerpo comprimido y piernas dobladas
            pygame.draw.rect(pantalla, COLOR_ROBOT, (x + 3, y, 30, 14), border_radius=5)
            pygame.draw.rect(pantalla, COLOR_VISOR, (x + 7, y + 3, 22, 8), border_radius=3)
            pygame.draw.circle(pantalla, COLOR_OJO, (ojo_x, y + 7), 3)
            pygame.draw.rect(pantalla, COLOR_ROBOT, (x + 4, y + 13, 28, 8), border_radius=3)
            pygame.draw.rect(pantalla, COLOR_ROBOT, (x + 6, y + 20, 10, 4))
            pygame.draw.rect(pantalla, COLOR_ROBOT, (x + 20, y + 20, 10, 4))
        else:
            # Antena
            pygame.draw.line(pantalla, COLOR_ROBOT, (centro_x, y + 4), (centro_x, y - 4), 2)
            pygame.draw.circle(pantalla, COLOR_ANTENA, (centro_x, y - 5), 3)
            # Cabeza con visor y un ojo que mira hacia donde apunta
            pygame.draw.rect(pantalla, COLOR_ROBOT, (x + 3, y + 4, 30, 20), border_radius=6)
            pygame.draw.rect(pantalla, COLOR_VISOR, (x + 7, y + 9, 22, 10), border_radius=4)
            pygame.draw.circle(pantalla, COLOR_OJO, (ojo_x, y + 14), 4)
            # Cuerpo con un detalle en el pecho
            pygame.draw.rect(pantalla, COLOR_ROBOT, (x + 6, y + 24, 24, 17), border_radius=4)
            pygame.draw.rect(pantalla, COLOR_PECHO, (x + 14, y + 28, 8, 8), border_radius=2)
            # Piernas
            pygame.draw.rect(pantalla, COLOR_ROBOT, (x + 9, y + 41, 7, 7))
            pygame.draw.rect(pantalla, COLOR_ROBOT, (x + 20, y + 41, 7, 7))

        # Llama del propulsor
        if self.volando:
            base = self.rect.bottom
            pygame.draw.polygon(pantalla, COLOR_FUEGO, [(centro_x - 7, base), (centro_x + 7, base), (centro_x, base + 14)])
            pygame.draw.polygon(pantalla, COLOR_AVISO, [(centro_x - 3, base), (centro_x + 3, base), (centro_x, base + 7)])

        # Arma: un cañón del hombro a la boca, en la dirección real del disparo
        hombro_x, hombro_y = self.punto_arma()
        boca_x, boca_y = self.origen_disparo()
        pygame.draw.line(pantalla, COLOR_ARMA, (hombro_x - camara_x, hombro_y), (boca_x - camara_x, boca_y), 6)
        pygame.draw.circle(pantalla, COLOR_PULSO, (round(boca_x - camara_x), round(boca_y)), 3)


class Enemigo:
    """Un enemigo que camina de un lado a otro dentro de su zona de patrulla."""

    ANCHO = 44
    ALTO = 32

    def __init__(self, limite_izq, limite_der, superficie_y):
        self.limite_izq = limite_izq
        self.limite_der = limite_der
        # Se apoya sobre la superficie indicada (suelo o plataforma)
        self.rect = pygame.Rect(limite_izq, superficie_y - self.ALTO, self.ANCHO, self.ALTO)
        self.direccion = 1  # 1 = derecha, -1 = izquierda

    def actualizar(self):
        self.rect.x += VELOCIDAD_ENEMIGO * self.direccion
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
            pygame.draw.polygon(pantalla, COLOR_ENEMIGO, [(base, y + 8), (base + 5, y - 4), (base + 10, y + 8)])
        # Cuerpo
        pygame.draw.rect(pantalla, COLOR_ENEMIGO, (x, y + 6, self.ANCHO, self.ALTO - 6), border_radius=8)
        # Ojos que miran hacia donde camina
        for ojo_x in (x + 14, x + 30):
            pygame.draw.circle(pantalla, COLOR_TEXTO, (ojo_x, y + 17), 5)
            pygame.draw.circle(pantalla, (0, 0, 0), (ojo_x + 2 * self.direccion, y + 17), 2)


class Pulso:
    """Pulso de energía que viaja en línea recta en la dirección del arma."""

    RADIO = 7

    def __init__(self, origen, direccion, ancho_mundo):
        # Posición con decimales para que las diagonales sean precisas
        self.x, self.y = origen
        self.dir_x, self.dir_y = direccion  # vector unitario (largo 1)
        self.ancho_mundo = ancho_mundo  # ancho del nivel o de la arena
        self.rect = pygame.Rect(0, 0, self.RADIO * 2, self.RADIO * 2)
        self.rect.center = (round(self.x), round(self.y))
        self.recorrido = 0.0  # distancia recorrida desde el lanzamiento

    def actualizar(self):
        # El último paso se recorta para no pasar de ALCANCE_PULSO. Como la dirección
        # mide 1, "paso" es la distancia real recorrida, también en diagonal.
        paso = min(VELOCIDAD_PULSO, ALCANCE_PULSO - self.recorrido)
        self.x += self.dir_x * paso
        self.y += self.dir_y * paso
        self.recorrido += paso
        self.rect.center = (round(self.x), round(self.y))

    def termino_alcance(self):
        """True si ya recorrió su distancia máxima o salió del escenario."""
        return (self.recorrido >= ALCANCE_PULSO
                or self.rect.right < 0 or self.rect.left > self.ancho_mundo
                or self.rect.bottom < 0 or self.rect.top > ALTO_VENTANA)

    def dibujar(self, pantalla, camara_x):
        centro = (self.rect.centerx - camara_x, self.rect.centery)
        pygame.draw.circle(pantalla, COLOR_PULSO, centro, self.RADIO)
        pygame.draw.circle(pantalla, COLOR_PULSO_CENTRO, centro, 3)


class Bateria:
    """Objeto coleccionable. Cada una se cuenta una sola vez."""

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, 20, 28)
        self.recogida = False

    def dibujar(self, pantalla, camara_x):
        if self.recogida:
            return
        x = self.rect.x - camara_x
        y = self.rect.y
        pygame.draw.rect(pantalla, COLOR_BATERIA_BORDE, (x + 6, y, 8, 4))  # terminal
        pygame.draw.rect(pantalla, COLOR_BATERIA, (x, y + 4, 20, 24), border_radius=3)
        pygame.draw.rect(pantalla, COLOR_BATERIA_BORDE, (x, y + 4, 20, 24), 2, border_radius=3)
        pygame.draw.rect(pantalla, COLOR_TEXTO, (x + 4, y + 14, 12, 4))  # franja de carga


class Proyectil:
    """Proyectil del jefe. Viaja en línea recta: no persigue al jugador."""

    def __init__(self, x, y, vel_x, vel_y, bajo):
        # La posición se guarda con decimales para que las diagonales sean precisas
        self.x = x
        self.y = y
        self.vel_x = vel_x
        self.vel_y = vel_y
        self.bajo = bajo  # True = proyectil que rueda por el suelo
        self.rect = pygame.Rect(0, 0, 24, 18) if bajo else pygame.Rect(0, 0, 16, 16)
        self.rect.center = (round(x), round(y))

    def actualizar(self):
        self.x += self.vel_x
        self.y += self.vel_y
        self.rect.center = (round(self.x), round(self.y))

    def fuera_de_arena(self):
        # El suelo también es un límite: un disparo que lo atraviesa ya salió
        return (self.rect.right < 0 or self.rect.left > ANCHO_VENTANA
                or self.rect.bottom < 0 or self.rect.top >= ALTURA_SUELO)

    def dibujar(self, pantalla):
        if self.bajo:
            pygame.draw.ellipse(pantalla, COLOR_PROYECTIL_BAJO, self.rect)
            pygame.draw.ellipse(pantalla, COLOR_AVISO, self.rect.inflate(-10, -8))
        else:
            pygame.draw.circle(pantalla, COLOR_PROYECTIL, self.rect.center, 8)
            pygame.draw.circle(pantalla, COLOR_TEXTO, self.rect.center, 3)


class Jefe:
    """Robot jefe con tres estados (aviso, ataque y descanso) y dos patrones."""

    ANCHO = 100
    ALTO = 120

    def __init__(self):
        self.rect = pygame.Rect(0, 0, self.ANCHO, self.ALTO)
        self.rect.bottomright = (ZONA_JEFE[1], ALTURA_SUELO)  # extremo derecho
        self.x = float(self.rect.x)  # con decimales, porque en la fase 2 avanza 2,4 px
        self.vida = VIDA_JEFE
        self.fase = 1
        self.anuncio_fase = 0  # cuadros que falta mostrar el texto "FASE 2"
        self.direccion = -1
        self.mirando_derecha = False
        self.estado = DESCANSO
        self.temporizador = DESCANSO_INICIAL  # cuadros que faltan en el estado actual
        self.patron = RAFAGA                  # patrón que usará en el próximo ataque
        self.disparos_hechos = 0

    def en_segunda_fase(self):
        return self.fase == 2

    def recibir_impacto(self):
        """Resta un punto de vida y, si corresponde, pasa a la fase 2 (una sola vez)."""
        self.vida = max(0, self.vida - 1)
        if self.fase == 1 and self.vida <= VIDA_SEGUNDA_FASE:
            self.fase = 2
            self.anuncio_fase = DURACION_ANUNCIO_FASE

    def actualizar(self, jugador, proyectiles):
        # Siempre mira hacia el jugador
        self.mirando_derecha = jugador.rect.centerx > self.rect.centerx
        self.temporizador -= 1
        if self.anuncio_fase > 0:
            self.anuncio_fase -= 1

        if self.estado == DESCANSO:
            self.mover()
            if self.temporizador <= 0:
                self.estado = AVISO
                self.temporizador = DURACION_AVISO
        elif self.estado == AVISO:
            if self.temporizador <= 0:
                self.estado = ATAQUE
                self.disparos_hechos = 0
        elif self.estado == ATAQUE and self.temporizador <= 0:
            if self.disparos_hechos < 3:
                self.disparar(jugador, proyectiles)
                self.disparos_hechos += 1
                self.temporizador = INTERVALO_RAFAGA if self.patron == RAFAGA else INTERVALO_BAJOS
            else:
                # Terminó el patrón: descansa y deja listo el otro patrón
                self.estado = DESCANSO
                self.temporizador = DESCANSO_FASE_2 if self.en_segunda_fase() else DESCANSO_FASE_1
                self.patron = BAJOS if self.patron == RAFAGA else RAFAGA

    def mover(self):
        """Se desplaza de un lado a otro dentro de su zona."""
        velocidad = VELOCIDAD_JEFE_FASE_2 if self.en_segunda_fase() else VELOCIDAD_JEFE
        self.x += velocidad * self.direccion
        if self.x <= ZONA_JEFE[0]:
            self.x = ZONA_JEFE[0]
            self.direccion = 1
        elif self.x + self.ANCHO >= ZONA_JEFE[1]:
            self.x = ZONA_JEFE[1] - self.ANCHO
            self.direccion = -1
        self.rect.x = round(self.x)

    def punto_canon(self):
        """El cañón está en el costado que mira al jugador."""
        x = self.rect.right if self.mirando_derecha else self.rect.left
        return x, self.rect.top + 70

    def disparar(self, jugador, proyectiles):
        if len(proyectiles) >= MAX_PROYECTILES:
            return
        x, y = self.punto_canon()
        if self.patron == RAFAGA:
            # Apunta al pecho del jugador en este momento; después sigue recto.
            # Si el robot se agacha después del disparo, el proyectil le pasa por encima.
            dx = jugador.rect.centerx - x
            dy = jugador.rect.top + 10 - y
            distancia = math.hypot(dx, dy) or 1
            proyectiles.append(Proyectil(x, y, dx / distancia * VELOCIDAD_PROYECTIL,
                                         dy / distancia * VELOCIDAD_PROYECTIL, False))
        else:
            # Proyectil bajo que rueda por el suelo hacia el lado del jugador
            sentido = 1 if self.mirando_derecha else -1
            proyectiles.append(Proyectil(x, ALTURA_SUELO - 9, sentido * VELOCIDAD_PROYECTIL, 0, True))

    def dibujar(self, pantalla):
        r = self.rect
        color = COLOR_JEFE_FASE_2 if self.en_segunda_fase() else COLOR_JEFE_FASE_1
        # Orugas
        pygame.draw.rect(pantalla, COLOR_VISOR, (r.x + 4, r.bottom - 20, r.width - 8, 20), border_radius=8)
        # Cuerpo y cabeza
        pygame.draw.rect(pantalla, color, (r.x + 10, r.y + 40, r.width - 20, 62), border_radius=10)
        pygame.draw.rect(pantalla, color, (r.x + 22, r.y, r.width - 44, 44), border_radius=8)
        pygame.draw.rect(pantalla, COLOR_VISOR, (r.x + 28, r.y + 12, r.width - 56, 18), border_radius=5)
        # Ojo: se pone amarillo durante el aviso
        ojo = COLOR_AVISO if self.estado == AVISO else COLOR_OJO
        ojo_x = r.centerx + (10 if self.mirando_derecha else -10)
        pygame.draw.circle(pantalla, ojo, (ojo_x, r.y + 21), 7)
        # Cañón
        canon = pygame.Rect(0, 0, 26, 16)
        canon.center = self.punto_canon()
        pygame.draw.rect(pantalla, COLOR_VISOR, canon, border_radius=4)
        if self.estado == AVISO:
            self.dibujar_aviso(pantalla)

    def dibujar_aviso(self, pantalla):
        """Señal antes de atacar: triángulo con "!" y una pista del patrón."""
        cx, arriba = self.rect.centerx, self.rect.top
        pygame.draw.polygon(pantalla, COLOR_AVISO, [(cx, arriba - 62), (cx - 24, arriba - 18), (cx + 24, arriba - 18)])
        pygame.draw.line(pantalla, COLOR_VISOR, (cx, arriba - 50), (cx, arriba - 32), 4)
        pygame.draw.circle(pantalla, COLOR_VISOR, (cx, arriba - 25), 3)
        if self.patron == RAFAGA:
            # El cañón brilla: viene una ráfaga apuntada
            pygame.draw.circle(pantalla, COLOR_AVISO, self.punto_canon(), 13, 3)
        else:
            # Franja en el suelo del lado del jugador: vienen proyectiles bajos
            ancho = 140
            x = self.rect.right if self.mirando_derecha else self.rect.left - ancho
            pygame.draw.rect(pantalla, COLOR_AVISO, (x, ALTURA_SUELO - 6, ancho, 6))


class Boton:
    """Botón rectangular que se activa con el clic izquierdo."""

    def __init__(self, texto, accion, centro, ancho=260, alto=54):
        self.texto = texto
        self.accion = accion
        self.rect = pygame.Rect(0, 0, ancho, alto)
        self.rect.center = centro

    def dibujar(self, pantalla, fuente, pos_raton):
        # Cambia de color y de borde cuando el cursor está encima
        encima = self.rect.collidepoint(pos_raton)
        color = COLOR_BOTON_ENCIMA if encima else COLOR_BOTON
        borde = COLOR_TEXTO if encima else COLOR_BORDE_BOTON
        pygame.draw.rect(pantalla, color, self.rect, border_radius=10)
        pygame.draw.rect(pantalla, borde, self.rect, 3, border_radius=10)
        texto = fuente.render(self.texto, True, COLOR_TEXTO)
        pantalla.blit(texto, texto.get_rect(center=self.rect.center))


# ---------------------------------------------------------------------------
# Lógica principal de la partida
# ---------------------------------------------------------------------------
class Juego:
    def __init__(self):
        self.fuente = pygame.font.Font(None, 36)          # fuente por defecto de Pygame
        self.fuente_grande = pygame.font.Font(None, 72)
        self.fuente_titulo = pygame.font.Font(None, 96)
        centro = ANCHO_VENTANA // 2
        # Botones de cada pantalla. Ninguno coincide en posición con un botón de la
        # pantalla que aparece después de pulsarlo, para evitar clics accidentales.
        self.botones = {
            INICIO: [Boton("Iniciar", INICIAR, (centro, 440)),
                     Boton("Salir", SALIR, (centro, 510))],
            JUGANDO: [Boton("Pausa", PAUSAR, (ANCHO_VENTANA - 80, 90), 120, 36)],
            PAUSA: [Boton("Continuar", CONTINUAR, (centro, 280)),
                    Boton("Reiniciar", INICIAR, (centro, 350)),
                    Boton("Salir", SALIR, (centro, 420))],
            VICTORIA: [Boton("Volver a jugar", INICIAR, (centro, 420)),
                       Boton("Salir", SALIR, (centro, 490))],
            DERROTA: [Boton("Volver a jugar", INICIAR, (centro, 420)),
                      Boton("Salir", SALIR, (centro, 490))],
        }
        self.reiniciar()
        self.estado = INICIO  # al abrir el juego se ve la pantalla inicial

    def iniciar_partida(self):
        """Usado por "Iniciar", "Reiniciar" y "Volver a jugar"."""
        self.reiniciar()
        self.estado = JUGANDO
        self.esperar_soltar_clic = True  # el clic del botón no debe disparar

    def manejar_clic(self, pos):
        """Ejecuta la acción del botón pulsado (como máximo uno) y la devuelve."""
        for boton in self.botones[self.estado]:
            if boton.rect.collidepoint(pos):
                if boton.accion == INICIAR:
                    self.iniciar_partida()
                elif boton.accion == PAUSAR:
                    self.estado = PAUSA
                elif boton.accion == CONTINUAR:
                    self.estado = JUGANDO
                    self.esperar_soltar_clic = True
                return boton.accion  # SALIR lo atiende el bucle principal
        return None

    def reiniciar(self):
        """Reinicia toda la aventura: nivel, corazones, enemigos, jefe y temporizadores."""
        self.escena = NIVEL
        self.solidos = crear_solidos()
        self.portal = pygame.Rect(PORTAL)
        self.jugador = Jugador(*POSICION_INICIAL)
        self.posicion_segura = self.jugador.rect.bottomleft  # pies en el último lugar seguro
        self.enemigos = [Enemigo(*zona) for zona in ZONAS_ENEMIGOS]
        self.baterias = [Bateria(x, y) for x, y in BATERIAS]
        self.pulsos = []
        self.espera_pulso = 0  # cuadros que faltan para poder atacar de nuevo
        self.vidas = VIDAS_MAXIMAS
        self.invulnerable = 0  # cuadros que faltan de invulnerabilidad
        self.jefe = None
        self.proyectiles = []
        self.esperar_soltar_clic = False  # True: hay que soltar el clic antes de disparar
        self.contador = 0
        self.estado = JUGANDO
        self.motivo_derrota = ""
        self.camara_x = 0

    def ancho_mundo(self):
        return ANCHO_NIVEL if self.escena == NIVEL else ANCHO_VENTANA

    def manejar_tecla(self, tecla):
        # El teclado solo mueve al robot; se dispara y se usan los menús con el ratón
        if self.estado == JUGANDO and tecla == pygame.K_SPACE:
            self.jugador.saltar(self.solidos)

    def puede_atacar(self):
        # En los menús, en pausa o al terminar la partida los ataques están bloqueados
        return (self.estado == JUGANDO and self.espera_pulso == 0
                and len(self.pulsos) < MAX_PULSOS)

    def lanzar_pulso(self):
        # Funciona igual en el suelo o en el aire
        if self.puede_atacar():
            self.pulsos.append(Pulso(self.jugador.origen_disparo(),
                                     self.jugador.direccion_disparo, self.ancho_mundo()))
            self.espera_pulso = ESPERA_PULSO

    def actualizar_pulsos(self):
        """Mueve los pulsos y elimina los que chocan o llegan a su límite."""
        for pulso in self.pulsos[:]:  # se recorre una copia porque se borran elementos
            pulso.actualizar()
            enemigo_golpeado = None
            for enemigo in self.enemigos:
                if pulso.rect.colliderect(enemigo.rect):
                    enemigo_golpeado = enemigo
                    break  # cada pulso elimina a un solo enemigo
            if enemigo_golpeado:
                self.enemigos.remove(enemigo_golpeado)
                self.pulsos.remove(pulso)
            elif self.jefe and pulso.rect.colliderect(self.jefe.rect):
                # Cada impacto al jefe le quita un punto de vida
                self.jefe.recibir_impacto()
                self.pulsos.remove(pulso)
            elif pulso.termino_alcance() or pulso.rect.collidelist(self.solidos) != -1:
                self.pulsos.remove(pulso)

    def recibir_danio(self):
        """Resta un corazón, salvo durante la invulnerabilidad."""
        if self.invulnerable > 0:
            return
        self.vidas -= 1
        self.invulnerable = INVULNERABILIDAD

    def caer_al_vacio(self):
        # Cada caída cuesta un corazón y regresa al robot al último lugar seguro.
        # Como vuelve arriba en el mismo cuadro, la misma caída no daña dos veces.
        self.vidas -= 1
        self.invulnerable = INVULNERABILIDAD
        self.jugador.rect.bottomleft = self.posicion_segura
        self.jugador.vel_y = 0

    def actualizar(self, teclas, pos_raton=None, clic_presionado=False):
        """Avanza el juego un paso fijo de 1/60 s."""
        # En el menú, en pausa o con la partida terminada no se mueve nada:
        # tampoco bajan la espera del ataque, la invulnerabilidad ni la energía.
        if self.estado != JUGANDO:
            return

        if self.espera_pulso > 0:
            self.espera_pulso -= 1
        if self.invulnerable > 0:
            self.invulnerable -= 1
        if not clic_presionado:
            self.esperar_soltar_clic = False

        self.jugador.actualizar(teclas, self.solidos, self.ancho_mundo())
        if self.escena == NIVEL:
            self.actualizar_nivel()
        else:
            self.actualizar_arena()
        if self.estado != JUGANDO:
            return

        # Apuntar: el cursor está en coordenadas de pantalla; sumando la cámara
        # se obtiene su posición en el mundo
        if pos_raton is not None:
            self.jugador.apuntar(pos_raton[0] + self.camara_x, pos_raton[1])
        # Mantener el clic dispara de forma repetida, respetando la espera
        if clic_presionado and not self.esperar_soltar_clic:
            self.lanzar_pulso()

    def actualizar_nivel(self):
        for enemigo in self.enemigos:
            enemigo.actualizar()
        self.actualizar_pulsos()

        for bateria in self.baterias:
            if not bateria.recogida and self.jugador.rect.colliderect(bateria.rect):
                bateria.recogida = True
                self.contador += 1

        # Solo se guarda como segura una posición con margen hacia ambos bordes,
        # para no reaparecer al filo de un hueco y volver a caer
        apoyo = self.jugador.apoyo
        if (apoyo and self.jugador.rect.left - apoyo.left >= MARGEN_SEGURO
                and apoyo.right - self.jugador.rect.right >= MARGEN_SEGURO):
            self.posicion_segura = self.jugador.rect.bottomleft

        # Tocar a un enemigo resta un corazón (el ataque no da invulnerabilidad)
        if self.jugador.rect.collidelist([e.rect for e in self.enemigos]) != -1:
            self.recibir_danio()
        if self.jugador.rect.top > ALTO_VENTANA:
            self.caer_al_vacio()

        if self.vidas <= 0:
            self.estado = DERROTA
            self.motivo_derrota = "Te quedaste sin corazones"
        elif self.jugador.rect.colliderect(self.portal):
            self.entrar_arena()
        else:
            self.actualizar_camara()

    def entrar_arena(self):
        """Pasa a la arena del jefe. Solo ocurre una vez: la arena no tiene portal."""
        self.escena = ARENA
        self.solidos = crear_solidos_arena()
        self.enemigos = []
        self.pulsos = []
        self.proyectiles = []
        self.espera_pulso = 0
        self.vidas = VIDAS_MAXIMAS  # el combate empieza con los tres corazones
        self.invulnerable = 0
        self.jugador = Jugador(*POSICION_INICIAL_ARENA)
        self.jefe = Jefe()
        self.camara_x = 0  # la arena es fija, sin cámara

    def actualizar_arena(self):
        self.jefe.actualizar(self.jugador, self.proyectiles)
        self.actualizar_pulsos()

        for proyectil in self.proyectiles[:]:
            proyectil.actualizar()
            if proyectil.rect.colliderect(self.jugador.rect):
                # Desaparece al impactar, así que solo puede causar daño una vez
                self.proyectiles.remove(proyectil)
                self.recibir_danio()
            elif proyectil.fuera_de_arena():
                self.proyectiles.remove(proyectil)

        if self.jugador.rect.colliderect(self.jefe.rect):
            self.recibir_danio()

        # Si los dos llegan a cero en la misma actualización, gana el jugador
        if self.jefe.vida <= 0:
            self.estado = VICTORIA
            self.proyectiles = []
            self.pulsos = []
        elif self.vidas <= 0:
            self.estado = DERROTA
            self.motivo_derrota = f"{NOMBRE_JEFE} te venció"

    def actualizar_camara(self):
        # Centra al jugador, pero sin mostrar nada fuera del nivel
        objetivo = self.jugador.rect.centerx - ANCHO_VENTANA // 2
        self.camara_x = max(0, min(objetivo, ANCHO_NIVEL - ANCHO_VENTANA))

    # ----- Dibujo -----------------------------------------------------------
    def dibujar(self, pantalla, pos_raton=(-1, -1)):
        if self.estado == INICIO:
            self.dibujar_inicio(pantalla)
        else:
            self.dibujar_partida(pantalla)
            if self.estado == PAUSA:
                self.dibujar_mensaje(pantalla, "Pausa", "El juego está detenido")
            elif self.estado == VICTORIA:
                self.dibujar_mensaje(pantalla, f"¡Derrotaste a {NOMBRE_JEFE}!",
                                     f"Baterías recogidas: {self.contador} de {len(self.baterias)}")
            elif self.estado == DERROTA:
                self.dibujar_mensaje(pantalla, "Fin de la partida", self.motivo_derrota)
        for boton in self.botones[self.estado]:
            boton.dibujar(pantalla, self.fuente, pos_raton)
        if self.estado == JUGANDO:
            self.dibujar_apuntado(pantalla, pos_raton)

    def dibujar_apuntado(self, pantalla, pos_raton):
        """Línea corta con la dirección real (ya limitada) y una mira en el cursor."""
        boca_x, boca_y = self.jugador.origen_disparo()
        dir_x, dir_y = self.jugador.direccion_disparo
        inicio = (boca_x - self.camara_x, boca_y)
        fin = (boca_x - self.camara_x + dir_x * 45, boca_y + dir_y * 45)
        pygame.draw.line(pantalla, COLOR_AVISO, inicio, fin, 2)
        mx, my = pos_raton
        pygame.draw.circle(pantalla, COLOR_TEXTO, (mx, my), 10, 2)
        pygame.draw.line(pantalla, COLOR_TEXTO, (mx - 15, my), (mx - 5, my), 2)
        pygame.draw.line(pantalla, COLOR_TEXTO, (mx + 5, my), (mx + 15, my), 2)
        pygame.draw.line(pantalla, COLOR_TEXTO, (mx, my - 15), (mx, my - 5), 2)
        pygame.draw.line(pantalla, COLOR_TEXTO, (mx, my + 5), (mx, my + 15), 2)

    def dibujar_inicio(self, pantalla):
        self.dibujar_fondo(pantalla)
        titulo = self.fuente_titulo.render("RoboAventura", True, COLOR_TEXTO)
        pantalla.blit(titulo, titulo.get_rect(center=(ANCHO_VENTANA // 2, 110)))
        controles = [
            "A / D o flechas: moverse      Espacio: saltar",
            "S o flecha abajo: agacharse",
            "Shift en el aire: propulsor",
            "Ratón: apuntar      Clic izquierdo: disparar",
        ]
        for i, linea in enumerate(controles):
            texto = self.fuente.render(linea, True, COLOR_TEXTO)
            pantalla.blit(texto, texto.get_rect(center=(ANCHO_VENTANA // 2, 200 + i * 40)))

    def dibujar_partida(self, pantalla):
        if self.escena == NIVEL:
            self.dibujar_fondo(pantalla)
            self.dibujar_escenario(pantalla)
            self.dibujar_portal(pantalla)
            for bateria in self.baterias:
                bateria.dibujar(pantalla, self.camara_x)
            for enemigo in self.enemigos:
                enemigo.dibujar(pantalla, self.camara_x)
        else:
            self.dibujar_fondo_arena(pantalla)
            self.dibujar_escenario(pantalla)
            self.jefe.dibujar(pantalla)
            for proyectil in self.proyectiles:
                proyectil.dibujar(pantalla)

        if self.jugador_visible():
            self.jugador.dibujar(pantalla, self.camara_x)
        for pulso in self.pulsos:
            pulso.dibujar(pantalla, self.camara_x)
        self.dibujar_hud(pantalla)

        # Anuncio breve del cambio de fase (oculto bajo los menús para no encimar textos)
        if self.jefe and self.jefe.anuncio_fase > 0 and self.estado == JUGANDO:
            texto = self.fuente_grande.render("FASE 2", True, COLOR_JEFE_FASE_2)
            pantalla.blit(texto, texto.get_rect(center=(ANCHO_VENTANA // 2, 180)))

    def jugador_visible(self):
        # Durante la invulnerabilidad parpadea: se oculta 6 cuadros, se muestra 6
        if self.estado != JUGANDO or self.invulnerable == 0:
            return True
        return (self.invulnerable // 6) % 2 == 0

    def dibujar_fondo(self, pantalla):
        pantalla.fill(COLOR_CIELO)
        # Estrellas fijas en la pantalla
        for i in range(40):
            pygame.draw.circle(pantalla, COLOR_ESTRELLA, ((i * 137) % ANCHO_VENTANA, (i * 59) % 300), 1)
        # Torres lejanas que se mueven a la mitad de velocidad (efecto de profundidad)
        alturas = (180, 260, 140, 220, 300, 160)
        for i in range(14):
            x = i * 150 - self.camara_x // 2
            alto = alturas[i % len(alturas)]
            pygame.draw.rect(pantalla, COLOR_TORRE, (x, ALTURA_SUELO - alto, 90, alto))

    def dibujar_fondo_arena(self, pantalla):
        pantalla.fill(COLOR_ARENA)
        # Focos de luz decorativos
        for x in (160, 480, 800):
            pygame.draw.circle(pantalla, COLOR_LUZ_ARENA, (x, 260), 120)

    def dibujar_escenario(self, pantalla):
        for solido in self.solidos:
            rect = solido.move(-self.camara_x, 0)
            es_suelo = solido.top == ALTURA_SUELO
            color = COLOR_SUELO if es_suelo else COLOR_PLATAFORMA
            borde = COLOR_BORDE_SUELO if es_suelo else COLOR_BORDE_PLATAFORMA
            pygame.draw.rect(pantalla, color, rect)
            pygame.draw.rect(pantalla, borde, (rect.x, rect.y, rect.width, 5))

    def dibujar_portal(self, pantalla):
        rect = self.portal.move(-self.camara_x, 0)
        pygame.draw.ellipse(pantalla, COLOR_PORTAL_EXTERIOR, rect)
        pygame.draw.ellipse(pantalla, COLOR_PORTAL_INTERIOR, rect.inflate(-16, -16))
        pygame.draw.ellipse(pantalla, COLOR_PORTAL_CENTRO, rect.inflate(-40, -50))

    def dibujar_hud(self, pantalla):
        texto = self.fuente.render(f"Baterías: {self.contador} / {len(self.baterias)}", True, COLOR_TEXTO)
        pantalla.blit(texto, (20, 20))

        # Corazones: uno lleno por cada punto de vida
        for i in range(VIDAS_MAXIMAS):
            dibujar_corazon(pantalla, 20 + i * 34, 56, i < self.vidas)

        # Energía del propulsor
        texto = self.fuente.render("Propulsor", True, COLOR_TEXTO)
        pantalla.blit(texto, (20, 90))
        barra = pygame.Rect(140, 96, 120, 12)
        llena = barra.width * self.jugador.energia // ENERGIA_MAXIMA
        pygame.draw.rect(pantalla, COLOR_CORAZON_VACIO, barra)
        pygame.draw.rect(pantalla, COLOR_PULSO, (barra.x, barra.y, llena, barra.height))
        pygame.draw.rect(pantalla, COLOR_TEXTO, barra, 2)

        # Indicador del ataque: verde si está listo, gris mientras recarga
        if self.puede_atacar():
            color, estado = COLOR_LISTO, "listo"
        else:
            color, estado = COLOR_RECARGANDO, "recargando"
        texto = self.fuente.render(f"Clic: pulso ({estado})", True, color)
        pantalla.blit(texto, texto.get_rect(topright=(ANCHO_VENTANA - 20, 20)))
        # Barra que se llena a medida que termina la espera
        progreso = 1 - self.espera_pulso / ESPERA_PULSO
        barra = pygame.Rect(0, 0, 160, 8)
        barra.topright = (ANCHO_VENTANA - 20, 50)
        pygame.draw.rect(pantalla, COLOR_RECARGANDO, barra, 1)
        pygame.draw.rect(pantalla, color, (barra.x, barra.y, int(barra.width * progreso), barra.height))

        if self.jefe:
            self.dibujar_barra_jefe(pantalla)

    def dibujar_barra_jefe(self, pantalla):
        fase = " · FASE 2" if self.jefe.en_segunda_fase() else ""
        texto = self.fuente.render(f"{NOMBRE_JEFE}  {self.jefe.vida}/{VIDA_JEFE}{fase}", True, COLOR_TEXTO)
        pantalla.blit(texto, texto.get_rect(midtop=(ANCHO_VENTANA // 2, 14)))
        color = COLOR_JEFE_FASE_2 if self.jefe.en_segunda_fase() else COLOR_JEFE_FASE_1
        barra = pygame.Rect(0, 0, 360, 14)
        barra.midtop = (ANCHO_VENTANA // 2, 44)
        pygame.draw.rect(pantalla, COLOR_CORAZON_VACIO, barra)
        pygame.draw.rect(pantalla, color, (barra.x, barra.y, barra.width * self.jefe.vida // VIDA_JEFE, barra.height))
        pygame.draw.rect(pantalla, COLOR_TEXTO, barra, 2)

    def dibujar_mensaje(self, pantalla, titulo, detalle):
        # Capa semitransparente sobre el juego
        capa = pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA), pygame.SRCALPHA)
        capa.fill((0, 0, 0, 170))
        pantalla.blit(capa, (0, 0))

        lineas = [
            (self.fuente_grande, titulo, 150),
            (self.fuente, detalle, 210),
        ]
        for fuente, texto, y in lineas:
            superficie = fuente.render(texto, True, COLOR_TEXTO)
            pantalla.blit(superficie, superficie.get_rect(center=(ANCHO_VENTANA // 2, y)))


def main():
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO_VENTANA, ALTO_VENTANA))
    pygame.display.set_caption("RoboAventura")
    reloj = pygame.time.Clock()
    juego = Juego()

    ejecutando = True
    acumulado = 0.0  # tiempo real pendiente de simular
    while ejecutando:
        # Paso fijo: se simulan tantos pasos de 1/60 s como tiempo real haya pasado.
        # Así el juego va a la misma velocidad aunque la pantalla vaya a más o menos FPS.
        acumulado += min(reloj.tick(FPS) / 1000, 0.25)  # tope para no "saltar" tras un bloqueo
        clic_atendido = False  # como máximo un clic por cuadro: un clic = una acción
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False  # botón de cierre de la ventana
            elif evento.type == pygame.KEYDOWN:
                juego.manejar_tecla(evento.key)
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1 and not clic_atendido:
                clic_atendido = True
                if juego.manejar_clic(evento.pos) == SALIR:
                    ejecutando = False

        teclas = pygame.key.get_pressed()
        pos_raton = pygame.mouse.get_pos()
        clic_presionado = pygame.mouse.get_pressed()[0]
        while acumulado >= PASO:
            juego.actualizar(teclas, pos_raton, clic_presionado)
            acumulado -= PASO

        # Durante la partida se dibuja una mira en lugar del cursor del sistema
        pygame.mouse.set_visible(juego.estado != JUGANDO)
        juego.dibujar(pantalla, pos_raton)
        pygame.display.flip()

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
