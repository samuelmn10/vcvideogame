"""Información en pantalla: baterías, corazones, energía, ataque, jefe y mira."""

import pygame

import config as c
from world import theme


def dibujar_corazon(pantalla, x, y, lleno):
    """Corazón hecho con dos círculos y un triángulo."""
    color = theme.CORAZON if lleno else theme.CORAZON_VACIO
    pygame.draw.circle(pantalla, color, (x + 7, y + 7), 7)
    pygame.draw.circle(pantalla, color, (x + 19, y + 7), 7)
    pygame.draw.polygon(pantalla, color, [(x, y + 9), (x + 26, y + 9), (x + 13, y + 24)])


def dibujar_hud(pantalla, fuentes, robot, baterias_recogidas, total_baterias, puede_atacar):
    fuente = fuentes["normal"]
    texto = fuente.render(f"Baterías: {baterias_recogidas} / {total_baterias}", True, theme.TEXTO)
    pantalla.blit(texto, (20, 20))

    # Corazones: uno lleno por cada punto de vida
    for i in range(c.VIDAS_MAXIMAS):
        dibujar_corazon(pantalla, 20 + i * 34, 56, i < robot.vidas)

    # Energía del propulsor
    texto = fuente.render("Propulsor", True, theme.TEXTO)
    pantalla.blit(texto, (20, 90))
    barra = pygame.Rect(140, 96, 120, 12)
    llena = barra.width * robot.energia // c.ENERGIA_MAXIMA
    pygame.draw.rect(pantalla, theme.CORAZON_VACIO, barra)
    pygame.draw.rect(pantalla, theme.PULSO, (barra.x, barra.y, llena, barra.height))
    pygame.draw.rect(pantalla, theme.TEXTO, barra, 2)

    # Indicador del ataque: verde si está listo, gris mientras recarga
    if puede_atacar:
        color, estado = theme.LISTO, "listo"
    else:
        color, estado = theme.RECARGANDO, "recargando"
    texto = fuente.render(f"Clic: pulso ({estado})", True, color)
    pantalla.blit(texto, texto.get_rect(topright=(c.ANCHO_VENTANA - 20, 20)))
    progreso = 1 - robot.espera_disparo / c.ESPERA_PULSO
    barra = pygame.Rect(0, 0, 160, 8)
    barra.topright = (c.ANCHO_VENTANA - 20, 50)
    pygame.draw.rect(pantalla, theme.RECARGANDO, barra, 1)
    pygame.draw.rect(pantalla, color, (barra.x, barra.y, int(barra.width * progreso), barra.height))


def dibujar_barra_jefe(pantalla, fuentes, jefe):
    fase = " · FASE 2" if jefe.en_segunda_fase() else ""
    maximo = jefe.vida_maxima()
    texto = fuentes["normal"].render(f"{c.NOMBRE_JEFE}  {jefe.vida}/{maximo}{fase}", True, theme.TEXTO)
    pantalla.blit(texto, texto.get_rect(midtop=(c.ANCHO_VENTANA // 2, 14)))
    color = theme.JEFE_FASE_2 if jefe.en_segunda_fase() else theme.JEFE_FASE_1
    barra = pygame.Rect(0, 0, 360, 14)
    barra.midtop = (c.ANCHO_VENTANA // 2, 44)
    pygame.draw.rect(pantalla, theme.CORAZON_VACIO, barra)
    pygame.draw.rect(pantalla, color, (barra.x, barra.y, barra.width * jefe.vida // maximo, barra.height))
    pygame.draw.rect(pantalla, theme.TEXTO, barra, 2)


def dibujar_anuncio_fase(pantalla, fuentes, texto):
    superficie = fuentes["grande"].render(texto, True, theme.JEFE_FASE_2)
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
