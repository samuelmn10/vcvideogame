"""
RoboAventura - Mini-juego de plataformas 2D (versión 1).

Controles:
    A / D o flechas izquierda / derecha -> moverse
    Espacio                             -> saltar
    R                                   -> reiniciar (después de ganar o perder)
    Escape                              -> salir
"""

import sys

import pygame

# ---------------------------------------------------------------------------
# Configuración general
# ---------------------------------------------------------------------------
ANCHO_VENTANA = 960
ALTO_VENTANA = 600
ANCHO_NIVEL = 2880
FPS = 60

# Física: los valores están en píxeles por cuadro (el juego corre a 60 FPS).
GRAVEDAD = 1
VELOCIDAD_SALTO = -17        # negativo = hacia arriba (el eje Y crece hacia abajo)
VELOCIDAD_CAIDA_MAX = 15     # menor que el grosor de las plataformas para no atravesarlas
VELOCIDAD_JUGADOR = 5
VELOCIDAD_ENEMIGO = 2

# Estados posibles de la partida
JUGANDO = "jugando"
DERROTA = "derrota"
VICTORIA = "victoria"

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
COLOR_TEXTO = (255, 255, 255)

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
PLATAFORMAS = [
    (300, 440, 140),
    (520, 360, 120),
    (900, 430, 140),
    (1150, 350, 140),
    (1400, 430, 160),
    (1950, 430, 140),
    (2200, 350, 140),
    (2450, 430, 120),
]

# Baterías como (x, y) de su esquina superior izquierda.
BATERIAS = [
    (360, 400),   # sobre la plataforma 1
    (570, 320),   # sobre la plataforma 2
    (750, 460),   # encima del hueco 1 (se recoge al saltarlo)
    (1210, 310),  # sobre la plataforma 4
    (2010, 390),  # sobre la plataforma 6
    (2260, 310),  # sobre la plataforma 7
]

ZONA_ENEMIGO = (1300, 1650)              # límites izquierdo y derecho de la patrulla
POSICION_INICIAL = (80, ALTURA_SUELO - 48)
PORTAL = (2740, ALTURA_SUELO - 110, 70, 110)  # (x, y, ancho, alto)


def crear_solidos():
    """Devuelve la lista de rectángulos sólidos: tramos de suelo y plataformas."""
    solidos = []
    for x, ancho in TRAMOS_SUELO:
        solidos.append(pygame.Rect(x, ALTURA_SUELO, ancho, ALTO_VENTANA - ALTURA_SUELO))
    for x, y, ancho in PLATAFORMAS:
        solidos.append(pygame.Rect(x, y, ancho, 20))
    return solidos


# ---------------------------------------------------------------------------
# Entidades del juego
# ---------------------------------------------------------------------------
class Jugador:
    """El robot que controla el jugador."""

    ANCHO = 36
    ALTO = 48

    def __init__(self, x, y):
        self.rect = pygame.Rect(x, y, self.ANCHO, self.ALTO)
        self.vel_y = 0
        self.en_suelo = False
        self.mirando_derecha = True

    def saltar(self):
        # Solo se puede saltar si está apoyado: así se evita saltar en el aire.
        if self.en_suelo:
            self.vel_y = VELOCIDAD_SALTO
            self.en_suelo = False

    def actualizar(self, teclas, solidos):
        # 1) Movimiento horizontal según las teclas presionadas
        dx = 0
        if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
            dx -= VELOCIDAD_JUGADOR
        if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
            dx += VELOCIDAD_JUGADOR
        if dx != 0:
            self.mirando_derecha = dx > 0

        self.rect.x += dx
        # Si choca de lado con un sólido, se pega a su borde
        for solido in solidos:
            if self.rect.colliderect(solido):
                if dx > 0:
                    self.rect.right = solido.left
                elif dx < 0:
                    self.rect.left = solido.right

        # No puede salir por los extremos del nivel
        self.rect.left = max(self.rect.left, 0)
        self.rect.right = min(self.rect.right, ANCHO_NIVEL)

        # 2) Gravedad y movimiento vertical
        self.vel_y = min(self.vel_y + GRAVEDAD, VELOCIDAD_CAIDA_MAX)
        self.rect.y += self.vel_y

        self.en_suelo = False
        for solido in solidos:
            if self.rect.colliderect(solido):
                if self.vel_y > 0:
                    # Venía cayendo: aterriza encima del sólido
                    self.rect.bottom = solido.top
                    self.en_suelo = True
                elif self.vel_y < 0:
                    # Venía subiendo: se golpea la cabeza por debajo
                    self.rect.top = solido.bottom
                self.vel_y = 0

    def dibujar(self, pantalla, camara_x):
        x = self.rect.x - camara_x
        y = self.rect.y
        centro_x = x + self.ANCHO // 2

        # Antena
        pygame.draw.line(pantalla, COLOR_ROBOT, (centro_x, y + 4), (centro_x, y - 4), 2)
        pygame.draw.circle(pantalla, COLOR_ANTENA, (centro_x, y - 5), 3)
        # Cabeza con visor y un ojo que mira hacia donde camina
        pygame.draw.rect(pantalla, COLOR_ROBOT, (x + 3, y + 4, 30, 20), border_radius=6)
        pygame.draw.rect(pantalla, COLOR_VISOR, (x + 7, y + 9, 22, 10), border_radius=4)
        ojo_x = x + 22 if self.mirando_derecha else x + 14
        pygame.draw.circle(pantalla, COLOR_OJO, (ojo_x, y + 14), 4)
        # Cuerpo con un detalle en el pecho
        pygame.draw.rect(pantalla, COLOR_ROBOT, (x + 6, y + 24, 24, 17), border_radius=4)
        pygame.draw.rect(pantalla, COLOR_PECHO, (x + 14, y + 28, 8, 8), border_radius=2)
        # Piernas
        pygame.draw.rect(pantalla, COLOR_ROBOT, (x + 9, y + 41, 7, 7))
        pygame.draw.rect(pantalla, COLOR_ROBOT, (x + 20, y + 41, 7, 7))


class Enemigo:
    """Un enemigo que camina de un lado a otro dentro de su zona de patrulla."""

    ANCHO = 44
    ALTO = 32

    def __init__(self, limite_izq, limite_der):
        self.limite_izq = limite_izq
        self.limite_der = limite_der
        self.rect = pygame.Rect(limite_izq, ALTURA_SUELO - self.ALTO, self.ANCHO, self.ALTO)
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


# ---------------------------------------------------------------------------
# Lógica principal de la partida
# ---------------------------------------------------------------------------
class Juego:
    def __init__(self):
        self.solidos = crear_solidos()
        self.portal = pygame.Rect(PORTAL)
        self.fuente = pygame.font.Font(None, 36)          # fuente por defecto de Pygame
        self.fuente_grande = pygame.font.Font(None, 72)
        self.reiniciar()

    def reiniciar(self):
        """Restaura jugador, enemigo, baterías, contador y cámara."""
        self.jugador = Jugador(*POSICION_INICIAL)
        self.enemigo = Enemigo(*ZONA_ENEMIGO)
        self.baterias = [Bateria(x, y) for x, y in BATERIAS]
        self.contador = 0
        self.estado = JUGANDO
        self.motivo_derrota = ""
        self.camara_x = 0

    def manejar_tecla(self, tecla):
        if self.estado == JUGANDO:
            if tecla == pygame.K_SPACE:
                self.jugador.saltar()
        elif tecla == pygame.K_r:
            # Reiniciar solo está disponible después de ganar o perder
            self.reiniciar()

    def actualizar(self, teclas):
        # Si la partida terminó, no se mueve nada hasta reiniciar o salir
        if self.estado != JUGANDO:
            return

        self.jugador.actualizar(teclas, self.solidos)
        self.enemigo.actualizar()

        for bateria in self.baterias:
            if not bateria.recogida and self.jugador.rect.colliderect(bateria.rect):
                bateria.recogida = True
                self.contador += 1

        if self.jugador.rect.colliderect(self.enemigo.rect):
            self.estado = DERROTA
            self.motivo_derrota = "Te atrapó el enemigo"
        elif self.jugador.rect.top > ALTO_VENTANA:
            self.estado = DERROTA
            self.motivo_derrota = "Caíste al vacío"
        elif self.jugador.rect.colliderect(self.portal):
            self.estado = VICTORIA

        self.actualizar_camara()

    def actualizar_camara(self):
        # Centra al jugador, pero sin mostrar nada fuera del nivel
        objetivo = self.jugador.rect.centerx - ANCHO_VENTANA // 2
        self.camara_x = max(0, min(objetivo, ANCHO_NIVEL - ANCHO_VENTANA))

    # ----- Dibujo -----------------------------------------------------------
    def dibujar(self, pantalla):
        self.dibujar_fondo(pantalla)
        self.dibujar_escenario(pantalla)
        self.dibujar_portal(pantalla)
        for bateria in self.baterias:
            bateria.dibujar(pantalla, self.camara_x)
        self.enemigo.dibujar(pantalla, self.camara_x)
        self.jugador.dibujar(pantalla, self.camara_x)
        self.dibujar_hud(pantalla)

        if self.estado == VICTORIA:
            self.dibujar_mensaje(pantalla, "¡Llegaste al portal!",
                                 f"Baterías recogidas: {self.contador} de {len(self.baterias)}")
        elif self.estado == DERROTA:
            self.dibujar_mensaje(pantalla, "Fin de la partida", self.motivo_derrota)

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

    def dibujar_mensaje(self, pantalla, titulo, detalle):
        # Capa semitransparente sobre el juego
        capa = pygame.Surface((ANCHO_VENTANA, ALTO_VENTANA), pygame.SRCALPHA)
        capa.fill((0, 0, 0, 170))
        pantalla.blit(capa, (0, 0))

        lineas = [
            (self.fuente_grande, titulo, 220),
            (self.fuente, detalle, 300),
            (self.fuente, "Presiona R para reiniciar o Escape para salir", 360),
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
    while ejecutando:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False
            elif evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_ESCAPE:
                    ejecutando = False
                else:
                    juego.manejar_tecla(evento.key)

        juego.actualizar(pygame.key.get_pressed())
        juego.dibujar(pantalla)
        pygame.display.flip()
        reloj.tick(FPS)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
