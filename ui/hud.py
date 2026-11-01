"""Información en pantalla: corazones, energía, ataque, nombre, fase y vida del jefe, y mira."""

import pygame

import config as c
from world import theme


def dibujar_corazon(pantalla, x, y, lleno):
    """Corazón hecho con dos círculos y un triángulo."""
    color = theme.CORAZON if lleno else theme.CORAZON_VACIO
    pygame.draw.circle(pantalla, color, (x + 7, y + 7), 7)
    pygame.draw.circle(pantalla, color, (x + 19, y + 7), 7)
    pygame.draw.polygon(pantalla, color, [(x, y + 9), (x + 26, y + 9), (x + 13, y + 24)])


def dibujar_hud(pantalla, fuentes, robot, puede_atacar):
    fuente = fuentes["normal"]
    # Nombre y corazones: uno lleno por cada punto de vida
    texto = fuente.render(c.NOMBRE_ROBOT, True, theme.PULSO)
    pantalla.blit(texto, (20, 20))
    for i in range(c.VIDAS_MAXIMAS):
        dibujar_corazon(pantalla, 120 + i * 34, 20, i < robot.vidas)

    # Energía del propulsor
    texto = fuente.render("Propulsor", True, theme.TEXTO)
    pantalla.blit(texto, (20, 58))
    barra = pygame.Rect(140, 64, 120, 12)
    llena = barra.width * robot.energia // c.ENERGIA_MAXIMA
    pygame.draw.rect(pantalla, theme.CORAZON_VACIO, barra)
    pygame.draw.rect(pantalla, theme.PULSO, (barra.x, barra.y, llena, barra.height))
    pygame.draw.rect(pantalla, theme.TEXTO, barra, 2)

    # Indicador del ataque: verde si está listo, gris mientras recarga
    if puede_atacar:
        color, estado = theme.LISTO, "listo"
    else:
        color, estado = theme.RECARGANDO, "recargando"
    texto = fuente.render(f"Pulso: {estado}", True, color)
    pantalla.blit(texto, texto.get_rect(topright=(c.ANCHO_VENTANA - 20, 20)))
    progreso = 1 - robot.espera_disparo / c.ESPERA_PULSO
    barra = pygame.Rect(0, 0, 160, 8)
    barra.topright = (c.ANCHO_VENTANA - 20, 50)
    pygame.draw.rect(pantalla, theme.RECARGANDO, barra, 1)
    pygame.draw.rect(pantalla, color, (barra.x, barra.y, int(barra.width * progreso), barra.height))


def dibujar_barra_jefe(pantalla, fuentes, jefe):
    """Nombre, fase actual y vida de esa fase. En la transición la barra se recarga."""
    if jefe.en_transicion():
        etiqueta = f"Fase 2: {jefe.NOMBRE_FASE_2}"
        vida = "recargando..."
        proporcion = jefe.progreso_transicion()  # solo visual: la vida se fija al terminar
        color = theme.AVISO
    else:
        numero = 2 if jefe.en_segunda_fase() else 1
        etiqueta = f"Fase {numero}: {jefe.nombre_fase()}"
        vida = f"{jefe.vida} / {jefe.vida_maxima}"
        proporcion = jefe.vida / jefe.vida_maxima
        color = theme.AVISO if jefe.en_segunda_fase() else theme.PULSO
    centro = c.ANCHO_VENTANA // 2
    texto = fuentes["pequena"].render(f"{jefe.NOMBRE} · {etiqueta}", True, theme.TEXTO)
    pantalla.blit(texto, texto.get_rect(midtop=(centro, 14)))
    barra = pygame.Rect(0, 0, 360, 14)
    barra.midtop = (centro, 44)
    pygame.draw.rect(pantalla, theme.CORAZON_VACIO, barra)
    pygame.draw.rect(pantalla, color, (barra.x, barra.y, int(barra.width * proporcion), barra.height))
    pygame.draw.rect(pantalla, theme.TEXTO, barra, 2)
    texto = fuentes["normal"].render(vida, True, theme.TEXTO)
    pantalla.blit(texto, texto.get_rect(midtop=(centro, 64)))


def dibujar_anuncio_fase(pantalla, fuentes, texto):
    superficie = fuentes["grande"].render(texto, True, theme.AVISO)
    pantalla.blit(superficie, superficie.get_rect(center=(c.ANCHO_VENTANA // 2, 180)))


def dibujar_apuntado(pantalla, robot, camara_x, pos_raton):
    """Línea corta con la dirección real (ya limitada) y una mira en el cursor."""
    boca_x, boca_y = robot.origen_disparo()
    dir_x, dir_y = robot.direccion_disparo
    inicio = (boca_x - camara_x, boca_y)
    fin = (boca_x - camara_x + dir_x * 45, boca_y + dir_y * 45)
    pygame.draw.line(pantalla, theme.AVISO, inicio, fin, 2)
    mx, my = pos_raton
    pygame.draw.circle(pantalla, theme.TEXTO, (mx, my), 10, 2)
    pygame.draw.line(pantalla, theme.TEXTO, (mx - 15, my), (mx - 5, my), 2)
    pygame.draw.line(pantalla, theme.TEXTO, (mx + 5, my), (mx + 15, my), 2)
    pygame.draw.line(pantalla, theme.TEXTO, (mx, my - 15), (mx, my - 5), 2)
    pygame.draw.line(pantalla, theme.TEXTO, (mx, my + 5), (mx, my + 15), 2)
