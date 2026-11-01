"""Parámetros ajustables de NEXO-7: Arena Eclipse: dimensiones, controles, física y robot.

Los parámetros de cada jefe están al principio de su propio módulo en entities/bosses/.
"""

import math
import os

import pygame

TITULO = "NEXO-7: Arena Eclipse"
NOMBRE_ROBOT = "NEXO-7"
# Archivo de progreso (desbloqueos y victorias), junto al código del juego
ARCHIVO_PROGRESO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "progreso.json")

# ---------------------------------------------------------------------------
# Ventana y tiempo
# ---------------------------------------------------------------------------
ANCHO_VENTANA = 960
ALTO_VENTANA = 600
FPS = 60
PASO = 1 / FPS               # cada actualización simula siempre 1/60 s (paso fijo)
ALTURA_SUELO = 540           # coordenada Y de la parte superior del suelo de las arenas

# ---------------------------------------------------------------------------
# Controles
# ---------------------------------------------------------------------------
TECLAS_IZQUIERDA = (pygame.K_a, pygame.K_LEFT)
TECLAS_DERECHA = (pygame.K_d, pygame.K_RIGHT)
TECLAS_AGACHARSE = (pygame.K_s, pygame.K_DOWN)
TECLAS_PROPULSOR = (pygame.K_LSHIFT, pygame.K_RSHIFT)
TECLA_SALTO = pygame.K_SPACE
BOTON_DISPARO = 0            # índice de pygame.mouse.get_pressed(): 0 = botón izquierdo
BOTON_SUPER = 3              # número del botón en los eventos de pygame: 3 = botón derecho

# ---------------------------------------------------------------------------
# Física (píxeles por paso de 1/60 s)
# ---------------------------------------------------------------------------
GRAVEDAD = 1
VELOCIDAD_SALTO = -17        # negativo = hacia arriba (el eje Y crece hacia abajo)
VELOCIDAD_CAIDA_MAX = 15     # menor que el grosor de las plataformas para no atravesarlas
VELOCIDAD_ROBOT = 5
VELOCIDAD_AGACHADO = 3

# Propulsor
DURACION_PROPULSOR = 0.8     # segundos de uso continuo (antes 2,0)
TIEMPO_RECARGA = 1.5         # segundos apoyado para recargar por completo
EMPUJE_PROPULSOR = 2         # contrarresta la gravedad (1) y deja 1 px/paso² hacia arriba
VELOCIDAD_SUBIDA_MAX = 6
# La energía se cuenta en unidades enteras para evitar errores de redondeo:
# el máximo es divisible por los pasos de uso y por los de recarga.
PASOS_USO_PROPULSOR = round(DURACION_PROPULSOR * FPS)
PASOS_RECARGA = round(TIEMPO_RECARGA * FPS)
ENERGIA_MAXIMA = math.lcm(PASOS_USO_PROPULSOR, PASOS_RECARGA)
GASTO_PROPULSOR = ENERGIA_MAXIMA // PASOS_USO_PROPULSOR
RECARGA_PROPULSOR = ENERGIA_MAXIMA // PASOS_RECARGA

# ---------------------------------------------------------------------------
# Robot: vida y ataque
# ---------------------------------------------------------------------------
VIDAS_MAXIMAS = 4
INVULNERABILIDAD = 72        # 1,2 s sin recibir daño después de un golpe
ANGULO_MAXIMO = 60           # en el suelo: grados hacia arriba o abajo (en el aire, 360°)
LARGO_ARMA = 20              # distancia del hombro a la boca del arma
VELOCIDAD_PULSO = 8
ALCANCE_PULSO = 350          # distancia máxima recorrida por un pulso
ESPERA_PULSO = 18            # 0,3 s entre disparos
MAX_PULSOS = 2               # pulsos activos al mismo tiempo

# Superataque (clic derecho): se carga acertando pulsos al jefe
ACIERTOS_SUPER = 10          # pulsos que deben acertar para cargarlo
DANIO_SUPER = 5              # un pulso hace 1
VELOCIDAD_SUPER = 10
ALCANCE_SUPER = 700

# ---------------------------------------------------------------------------
# Reglas comunes de los jefes (tiempos en pasos de 1/60 s)
# ---------------------------------------------------------------------------
DURACION_TRANSICION = 90     # 1,5 s entre la fase 1 y la fase 2, sin ataques ni daño
VELOCIDAD_PROYECTIL = 5      # velocidad de los proyectiles hostiles
MAX_PROYECTILES = 12         # si se llega al máximo, la siguiente emisión espera
DESCANSO_INICIAL = 90        # 1,5 s para ubicarse al empezar el combate
DISTANCIA_PATRULLA = 160     # en el descanso, los jefes de suelo no se acercan más que esto a NEXO-7

# ---------------------------------------------------------------------------
# Pantallas y acciones de los botones (nombres compartidos entre módulos)
# ---------------------------------------------------------------------------
MENU = "menú"
SELECCION = "selección"
DETALLE = "detalle"
JUGANDO = "jugando"
PAUSA = "pausa"
VICTORIA = "victoria"
DERROTA = "derrota"
CAMPANA = "campaña completada"

JUGAR = "jugar"
ELEGIR = "elegir"
VOLVER = "volver"
COMBATIR = "combatir"
PAUSAR = "pausar"
CONTINUAR = "continuar"
REINTENTAR = "reintentar"
IR_A_SELECCION = "ir a selección"
SIGUIENTE = "siguiente jefe"
SALIR = "salir"
