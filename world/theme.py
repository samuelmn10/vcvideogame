"""Ambientación: arenas de una estación tecnológica abandonada.

Todas las decisiones visuales están aquí: colores, fuentes, fondos de las arenas,
suelo y plataformas. La lógica del juego no conoce colores; para cambiar la
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
# Proyectiles: aliados cian, hostiles magenta y naranja
PULSO = (80, 235, 255)
PULSO_CENTRO = (235, 255, 255)
PROYECTIL = (255, 90, 190)
PROYECTIL_BAJO = (255, 140, 40)
# Arenas
ARENA = (16, 12, 28)
NUCLEO_EXTERIOR = (40, 30, 70)
NUCLEO_MEDIO = (70, 50, 120)
NUCLEO_CENTRO = (150, 120, 230)
HANGAR = (22, 22, 26)
FRANJA_PELIGRO = (200, 160, 40)
CAJA = (60, 56, 50)
CUPULA = (10, 16, 34)
RAYO = (120, 200, 255)
# Jefes y avisos
JEFE_OSCURO = (24, 20, 40)
OJO_JEFE = (255, 240, 200)
AVISO = (255, 215, 60)
CENTINELA_1 = (88, 82, 160)      # índigo
CENTINELA_2 = (210, 60, 50)      # rojo de sobrecarga
EMBESTIDOR_1 = (130, 120, 110)   # hierro
EMBESTIDOR_2 = (220, 110, 30)    # metal al rojo
SERAFIN_1 = (70, 160, 220)       # azul eléctrico
SERAFIN_2 = (240, 240, 120)      # blanco amarillento de tormenta
# Interfaz
TEXTO = (255, 255, 255)
LISTO = (90, 220, 120)
RECARGANDO = (130, 130, 150)
CORAZON = (235, 60, 80)
CORAZON_VACIO = (80, 86, 104)
BLOQUEADO = (70, 74, 86)
DERROTADO = (90, 220, 120)
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
    """Dibuja los fondos de las tres arenas una sola vez; en cada cuadro solo se copian."""
    fondos = {}

    # Arena 1: cámara del núcleo de energía
    nucleo = pygame.Surface((c.ANCHO_VENTANA, c.ALTO_VENTANA))
    nucleo.fill(ARENA)
    for x in range(0, c.ANCHO_VENTANA, 120):
        pygame.draw.rect(nucleo, VIGA, (x, 0, 16, c.ALTURA_SUELO))
    pygame.draw.rect(nucleo, VIGA, (0, 120, c.ANCHO_VENTANA, 14))
    for radio, color in ((210, NUCLEO_EXTERIOR), (150, NUCLEO_MEDIO), (80, NUCLEO_CENTRO)):
        pygame.draw.circle(nucleo, color, (700, 300), radio)
    pygame.draw.circle(nucleo, ARENA, (700, 300), 40)
    fondos["nucleo"] = nucleo

    # Arena 2: hangar de carga con franjas de peligro y cajas
    hangar = pygame.Surface((c.ANCHO_VENTANA, c.ALTO_VENTANA))
    hangar.fill(HANGAR)
    for x in range(0, c.ANCHO_VENTANA, 160):
        pygame.draw.rect(hangar, VIGA, (x, 0, 24, c.ALTURA_SUELO))
    for x in range(-40, c.ANCHO_VENTANA, 40):
        pygame.draw.polygon(hangar, FRANJA_PELIGRO, [(x, 150), (x + 20, 150), (x + 40, 170), (x + 20, 170)])
    for x, alto in ((60, 70), (140, 40), (780, 60), (860, 90)):
        pygame.draw.rect(hangar, CAJA, (x, c.ALTURA_SUELO - alto - 160, 70, alto))
    fondos["hangar"] = hangar

    # Arena 3: cúpula de tormenta con ventanales y rayos
    cupula = pygame.Surface((c.ANCHO_VENTANA, c.ALTO_VENTANA))
    cupula.fill(CUPULA)
    pygame.draw.circle(cupula, FONDO_LEJANO, (c.ANCHO_VENTANA // 2, c.ALTURA_SUELO), 520, 14)
    for x in range(60, c.ANCHO_VENTANA, 140):
        pygame.draw.rect(cupula, VENTANA_APAGADA, (x, 60, 80, 120), border_radius=8)
    for x0 in (130, 480, 830):
        puntos = [(x0, 70), (x0 - 12, 110), (x0 + 8, 120), (x0 - 6, 170)]
        pygame.draw.lines(cupula, RAYO, False, puntos, 3)
    fondos["cupula"] = cupula
    return fondos


# ---------------------------------------------------------------------------
# Dibujo del escenario
# ---------------------------------------------------------------------------
def dibujar_fondo(pantalla, fondos, nombre):
    pantalla.blit(fondos[nombre], (0, 0))


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
