"""Parámetros ajustables: dimensiones, controles, física y dificultad.

Para cambiar la dificultad o los controles basta con editar este archivo.
"""

import math

import pygame

# ---------------------------------------------------------------------------
# Ventana y tiempo
# ---------------------------------------------------------------------------
ANCHO_VENTANA = 960
ALTO_VENTANA = 600
FPS = 60
PASO = 1 / FPS               # cada actualización simula siempre 1/60 s (paso fijo)
ANCHO_NIVEL = 2880
ALTURA_SUELO = 540           # coordenada Y de la parte superior del suelo

# ---------------------------------------------------------------------------
# Controles
# ---------------------------------------------------------------------------
TECLAS_IZQUIERDA = (pygame.K_a, pygame.K_LEFT)
TECLAS_DERECHA = (pygame.K_d, pygame.K_RIGHT)
TECLAS_AGACHARSE = (pygame.K_s, pygame.K_DOWN)
TECLAS_PROPULSOR = (pygame.K_LSHIFT, pygame.K_RSHIFT)
TECLA_SALTO = pygame.K_SPACE
BOTON_DISPARO = 0            # índice de pygame.mouse.get_pressed(): 0 = botón izquierdo

# ---------------------------------------------------------------------------
# Física (píxeles por paso de 1/60 s)
# ---------------------------------------------------------------------------
GRAVEDAD = 1
VELOCIDAD_SALTO = -17        # negativo = hacia arriba (el eje Y crece hacia abajo)
VELOCIDAD_CAIDA_MAX = 15     # menor que el grosor de las plataformas para no atravesarlas
VELOCIDAD_ROBOT = 5
VELOCIDAD_AGACHADO = 3

# Propulsor
DURACION_PROPULSOR = 2.0     # segundos de uso continuo
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
VIDAS_MAXIMAS = 3
INVULNERABILIDAD = 72        # 1,2 s sin recibir daño después de un golpe
MARGEN_SEGURO = 100          # distancia mínima a los bordes para guardar una posición segura
ANGULO_MAXIMO = 60           # grados hacia arriba o hacia abajo al apuntar
LARGO_ARMA = 20              # distancia del hombro a la boca del arma
VELOCIDAD_PULSO = 8
ALCANCE_PULSO = 350          # distancia máxima recorrida por un pulso
ESPERA_PULSO = 18            # 0,3 s entre disparos
MAX_PULSOS = 2               # pulsos activos al mismo tiempo

# ---------------------------------------------------------------------------
# Enemigos comunes
# ---------------------------------------------------------------------------
VELOCIDAD_ENEMIGO = 3

# ---------------------------------------------------------------------------
# Jefe
# ---------------------------------------------------------------------------
NOMBRE_JEFE = "VOLTARÓN"
VIDA_JEFE = 12
VIDA_SEGUNDA_FASE = 6        # con esta vida o menos empieza la fase 2
VELOCIDAD_JEFE = 2
VELOCIDAD_JEFE_FASE_2 = 2.4  # 20 % más rápido
DURACION_AVISO = 45          # 0,75 s de señal antes de cada ataque
DURACION_ANUNCIO_FASE = 90   # el texto "FASE 2" se muestra 1,5 s
DESCANSO_INICIAL = 120       # 2 s para ubicarse al entrar a la arena
DESCANSO_FASE_1 = 72         # 1,2 s entre patrones
DESCANSO_FASE_2 = 48         # 0,8 s entre patrones
INTERVALO_RAFAGA = 24        # pasos entre los 3 disparos de la ráfaga
INTERVALO_BAJOS = 45         # pasos entre los 3 proyectiles bajos (~225 px de separación)
VELOCIDAD_PROYECTIL = 5
MAX_PROYECTILES = 12

# ---------------------------------------------------------------------------
# Nombres de estados y acciones (compartidos entre módulos)
# ---------------------------------------------------------------------------
INICIO = "inicio"
JUGANDO = "jugando"
PAUSA = "pausa"
DERROTA = "derrota"
VICTORIA = "victoria"

NIVEL = "nivel"
ARENA = "arena"

INICIAR = "iniciar"
PAUSAR = "pausar"
CONTINUAR = "continuar"
SALIR = "salir"
