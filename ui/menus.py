"""Botones y pantallas de menú (inicio, pausa, victoria y derrota)."""

import pygame

import config as c
from world import theme


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
        color = theme.BOTON_ENCIMA if encima else theme.BOTON
        borde = theme.TEXTO if encima else theme.BORDE_BOTON
        pygame.draw.rect(pantalla, color, self.rect, border_radius=10)
        pygame.draw.rect(pantalla, borde, self.rect, 3, border_radius=10)
        texto = fuente.render(self.texto, True, theme.TEXTO)
        pantalla.blit(texto, texto.get_rect(center=self.rect.center))


def crear_botones():
    """Botones de cada pantalla. Ninguno coincide en posición con un botón de la
    pantalla que aparece después de pulsarlo, para evitar clics accidentales."""
    centro = c.ANCHO_VENTANA // 2
    return {
        c.INICIO: [Boton("Iniciar", c.INICIAR, (centro, 440)),
                   Boton("Salir", c.SALIR, (centro, 510))],
        c.JUGANDO: [Boton("Pausa", c.PAUSAR, (c.ANCHO_VENTANA - 80, 90), 120, 36)],
        c.PAUSA: [Boton("Continuar", c.CONTINUAR, (centro, 280)),
                  Boton("Reiniciar", c.INICIAR, (centro, 350)),
                  Boton("Salir", c.SALIR, (centro, 420))],
        c.VICTORIA: [Boton("Volver a jugar", c.INICIAR, (centro, 420)),
                     Boton("Salir", c.SALIR, (centro, 490))],
        c.DERROTA: [Boton("Volver a jugar", c.INICIAR, (centro, 420)),
                    Boton("Salir", c.SALIR, (centro, 490))],
    }


def boton_pulsado(botones, pos):
    """Devuelve el botón que contiene el punto (como máximo uno), o None."""
    for boton in botones:
        if boton.rect.collidepoint(pos):
            return boton
    return None


def dibujar_botones(pantalla, fuentes, botones, pos_raton):
    for boton in botones:
        boton.dibujar(pantalla, fuentes["normal"], pos_raton)


def dibujar_inicio(pantalla, fuentes, fondos):
    theme.dibujar_fondo_nivel(pantalla, fondos, 0)
    titulo = fuentes["titulo"].render("RoboAventura", True, theme.TEXTO)
    pantalla.blit(titulo, titulo.get_rect(center=(c.ANCHO_VENTANA // 2, 90)))
    subtitulo = fuentes["normal"].render(f"{c.NOMBRE_ROBOT} en la estación abandonada", True, theme.PULSO)
    pantalla.blit(subtitulo, subtitulo.get_rect(center=(c.ANCHO_VENTANA // 2, 150)))
    controles = [
        "A / D o flechas: moverse      Espacio: saltar",
        "S o flecha abajo: agacharse",
        "Shift en el aire: propulsor",
        "Ratón: apuntar (360° en el aire)      Clic izquierdo: disparar",
    ]
    for i, linea in enumerate(controles):
        texto = fuentes["normal"].render(linea, True, theme.TEXTO)
        pantalla.blit(texto, texto.get_rect(center=(c.ANCHO_VENTANA // 2, 215 + i * 40)))


def dibujar_mensaje(pantalla, fuentes, capa_oscura, titulo, detalle):
    """Capa semitransparente con un título y un detalle (pausa, victoria o derrota)."""
    pantalla.blit(capa_oscura, (0, 0))
    for fuente, texto, y in ((fuentes["grande"], titulo, 150), (fuentes["normal"], detalle, 210)):
        superficie = fuente.render(texto, True, theme.TEXTO)
        pantalla.blit(superficie, superficie.get_rect(center=(c.ANCHO_VENTANA // 2, y)))
