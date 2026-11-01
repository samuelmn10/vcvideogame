"""Ambientación: estación tecnológica abandonada.

Todas las decisiones visuales están aquí: colores, fuentes, fondos, suelo,
plataformas y portal. La lógica del juego no conoce colores; para cambiar la
ambientación basta con editar este archivo.
"""

import pygame

import config as c

# ---------------------------------------------------------------------------
# Paleta
# ---------------------------------------------------------------------------
# Estación (fondo y estructuras)
FONDO = (14, 20, 30)
FONDO_LEJANO = (24, 32, 46)
VIGA = (34, 44, 60)
VENTANA_ENCENDIDA = (90, 200, 190)
VENTANA_APAGADA = (40, 52, 66)
CABLE = (46, 56, 70)
# Superficies metálicas
SUELO = (58, 66, 82)
JUNTA_SUELO = (44, 50, 64)
PLATAFORMA = (112, 124, 146)
BAJO_PLATAFORMA = (76, 86, 104)
REMACHE = (150, 160, 178)
LUZ_BORDE = (70, 210, 200)
# NEXO-7 (jugador): blanco con detalles cian
ROBOT = (215, 225, 238)
VISOR = (26, 34, 52)
OJO = (80, 235, 255)
PECHO = (80, 235, 255)
ANTENA = (255, 215, 90)
ARMA = (60, 70, 90)
FUEGO = (255, 170, 50)
# Enemigos comunes (drones de seguridad): rojo
ENEMIGO = (215, 55, 85)
# Proyectiles: aliados cian, hostiles magenta y naranja
PULSO = (80, 235, 255)
PULSO_CENTRO = (235, 255, 255)
PROYECTIL = (255, 90, 190)
PROYECTIL_BAJO = (255, 140, 40)
# Objetos
BATERIA = (90, 220, 120)
BATERIA_BORDE = (30, 90, 50)
MARCO_PORTAL = (90, 100, 120)
PORTAL_EXTERIOR = (150, 80, 255)
PORTAL_INTERIOR = (90, 40, 200)
PORTAL_CENTRO = (220, 200, 255)
# Arena: cámara del núcleo de energía
ARENA = (16, 12, 28)
NUCLEO_EXTERIOR = (40, 30, 70)
NUCLEO_MEDIO = (70, 50, 120)
NUCLEO_CENTRO = (150, 120, 230)
# Centinela Eclipse
JEFE_FASE_1 = (88, 82, 160)    # índigo
JEFE_FASE_2 = (210, 60, 50)    # rojo de sobrecarga
JEFE_OSCURO = (24, 20, 40)
OJO_JEFE = (255, 240, 200)
AVISO = (255, 215, 60)
# Interfaz
TEXTO = (255, 255, 255)
LISTO = (90, 220, 120)
RECARGANDO = (130, 130, 150)
CORAZON = (235, 60, 80)
CORAZON_VACIO = (80, 86, 104)
BOTON = (44, 62, 90)
BOTON_ENCIMA = (60, 120, 140)
BORDE_BOTON = (90, 140, 160)


# ---------------------------------------------------------------------------
# Recursos que se crean una sola vez
# ---------------------------------------------------------------------------
def crear_fuentes():
    """Fuente por defecto de Pygame, sin archivos externos."""
    return {
        "normal": pygame.font.Font(None, 36),
        "grande": pygame.font.Font(None, 72),
        "titulo": pygame.font.Font(None, 96),
    }


def crear_capa_oscura():
    """Capa semitransparente para los menús."""
    capa = pygame.Surface((c.ANCHO_VENTANA, c.ALTO_VENTANA), pygame.SRCALPHA)
    capa.fill((0, 0, 0, 170))
    return capa


def crear_fondos():
    """Dibuja los fondos una sola vez; en cada cuadro solo se copian (blit)."""
    # El fondo del nivel se mueve a la mitad de velocidad que la cámara (profundidad)
    ancho_lejano = (c.ANCHO_NIVEL - c.ANCHO_VENTANA) // 2 + c.ANCHO_VENTANA
    lejano = pygame.Surface((ancho_lejano, c.ALTO_VENTANA))
    lejano.fill(FONDO)
    alturas = (300, 380, 260, 340, 420, 280)
    for i, x in enumerate(range(0, ancho_lejano, 170)):
        alto = alturas[i % len(alturas)]
        modulo = pygame.Rect(x + 20, c.ALTURA_SUELO - alto, 110, alto)
        pygame.draw.rect(lejano, FONDO_LEJANO, modulo)
        # Ventanas: algunas siguen encendidas, otras están apagadas
        for fila in range(modulo.top + 20, modulo.bottom - 30, 40):
            for col in range(modulo.left + 14, modulo.right - 20, 30):
                encendida = (fila // 40 + col // 30 + i) % 4 == 0
                pygame.draw.rect(lejano, VENTANA_ENCENDIDA if encendida else VENTANA_APAGADA, (col, fila, 14, 10))
    # Vigas horizontales y cables colgantes
    for y in (90, 210):
        pygame.draw.rect(lejano, VIGA, (0, y, ancho_lejano, 12))
    for x in range(60, ancho_lejano, 230):
        pygame.draw.line(lejano, CABLE, (x, 102), (x + 40, 170), 3)

    # Arena: cámara del núcleo de energía con el núcleo detrás del jefe
    arena = pygame.Surface((c.ANCHO_VENTANA, c.ALTO_VENTANA))
    arena.fill(ARENA)
    for x in range(0, c.ANCHO_VENTANA, 120):
        pygame.draw.rect(arena, VIGA, (x, 0, 16, c.ALTURA_SUELO))
    pygame.draw.rect(arena, VIGA, (0, 120, c.ANCHO_VENTANA, 14))
    centro = (700, 300)
    for radio, color in ((210, NUCLEO_EXTERIOR), (150, NUCLEO_MEDIO), (80, NUCLEO_CENTRO)):
        pygame.draw.circle(arena, color, centro, radio)
    pygame.draw.circle(arena, ARENA, centro, 40)  # núcleo apagado en el centro
    return {"nivel": lejano, "arena": arena}


# ---------------------------------------------------------------------------
# Dibujo del escenario
# ---------------------------------------------------------------------------
def dibujar_fondo_nivel(pantalla, fondos, camara_x):
    pantalla.blit(fondos["nivel"], (-(camara_x // 2), 0))


def dibujar_fondo_arena(pantalla, fondos):
    pantalla.blit(fondos["arena"], (0, 0))


def dibujar_solido(pantalla, rect):
    """Suelo o plataforma metálica (rect ya en coordenadas de pantalla)."""
    if rect.top == c.ALTURA_SUELO:
        # Suelo: placas con juntas verticales y una franja de luz arriba
        pygame.draw.rect(pantalla, SUELO, rect)
        for x in range(rect.left + 60, rect.right, 60):
            pygame.draw.line(pantalla, JUNTA_SUELO, (x, rect.top + 6), (x, rect.bottom), 2)
        pygame.draw.rect(pantalla, LUZ_BORDE, (rect.x, rect.y, rect.width, 4))
    else:
        # Plataforma: chapa con parte inferior más oscura y remaches
        pygame.draw.rect(pantalla, PLATAFORMA, rect)
        pygame.draw.rect(pantalla, BAJO_PLATAFORMA, (rect.x, rect.bottom - 6, rect.width, 6))
        pygame.draw.rect(pantalla, LUZ_BORDE, (rect.x, rect.y, rect.width, 3))
        for x in range(rect.left + 10, rect.right - 5, 30):
            pygame.draw.circle(pantalla, REMACHE, (x, rect.y + 10), 2)


def dibujar_portal(pantalla, rect):
    """Compuerta hacia la cámara del núcleo."""
    pygame.draw.rect(pantalla, MARCO_PORTAL, rect.inflate(16, 10), border_radius=12)
    pygame.draw.ellipse(pantalla, PORTAL_EXTERIOR, rect)
    pygame.draw.ellipse(pantalla, PORTAL_INTERIOR, rect.inflate(-16, -16))
    pygame.draw.ellipse(pantalla, PORTAL_CENTRO, rect.inflate(-40, -50))
