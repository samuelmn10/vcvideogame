"""Botones y pantallas de menú: principal, selección de jefe, detalle, pausa y fin de combate."""

import pygame

import config as c
from world import theme


class Boton:
    """Botón rectangular que se activa con el clic izquierdo."""

    def __init__(self, texto, accion, centro, ancho=300, alto=54):
        self.texto = texto
        self.accion = accion
        self.rect = pygame.Rect(0, 0, ancho, alto)
        self.rect.center = centro

    def dibujar(self, pantalla, fuentes, pos_raton, juego=None):
        # Cambia de color y de borde cuando el cursor está encima
        encima = self.rect.collidepoint(pos_raton)
        color = theme.BOTON_ENCIMA if encima else theme.BOTON
        borde = theme.TEXTO if encima else theme.BORDE_BOTON
        pygame.draw.rect(pantalla, color, self.rect, border_radius=10)
        pygame.draw.rect(pantalla, borde, self.rect, 3, border_radius=10)
        texto = fuentes["normal"].render(self.texto, True, theme.TEXTO)
        pantalla.blit(texto, texto.get_rect(center=self.rect.center))


class TarjetaJefe:
    """Tarjeta de la pantalla de selección. Los jefes bloqueados se ven pero no se eligen."""

    accion = c.ELEGIR

    def __init__(self, indice, clase_jefe, centro):
        self.indice = indice
        self.clase = clase_jefe
        self.rect = pygame.Rect(0, 0, 250, 250)
        self.rect.center = centro

    def dibujar(self, pantalla, fuentes, pos_raton, juego):
        progreso = juego.progreso
        desbloqueado = progreso.desbloqueado(self.indice)
        encima = desbloqueado and self.rect.collidepoint(pos_raton)
        fondo = theme.BOTON_ENCIMA if encima else (theme.BOTON if desbloqueado else theme.BLOQUEADO)
        pygame.draw.rect(pantalla, fondo, self.rect, border_radius=14)
        pygame.draw.rect(pantalla, theme.TEXTO if encima else theme.BORDE_BOTON, self.rect, 3, border_radius=14)
        if not desbloqueado:
            estado, color = "Bloqueado", theme.RECARGANDO
        elif progreso.derrotado(self.indice):
            estado, color = f"Derrotado ({progreso.victorias[self.indice]})", theme.DERROTADO
        else:
            estado, color = "Disponible", theme.AVISO
        lineas = [
            (fuentes["normal"], f"Jefe {self.indice + 1}", theme.TEXTO),
            (fuentes["normal"], self.clase.NOMBRE, theme.TEXTO),
            (fuentes["pequena"], f"Dificultad: {self.clase.DIFICULTAD}", theme.TEXTO),
            (fuentes["normal"], estado, color),
        ]
        for i, (fuente, texto, col) in enumerate(lineas):
            superficie = fuente.render(texto, True, col)
            pantalla.blit(superficie, superficie.get_rect(center=(self.rect.centerx, self.rect.top + 40 + i * 50)))
        if not desbloqueado:
            # Candado: arco y cuerpo
            cx, y = self.rect.centerx, self.rect.bottom - 34
            pygame.draw.arc(pantalla, theme.TEXTO, (cx - 10, y - 18, 20, 24), 0, 3.15, 3)
            pygame.draw.rect(pantalla, theme.TEXTO, (cx - 14, y - 6, 28, 20), border_radius=4)


def crear_botones(jefes):
    """Botones de cada pantalla (se crean una sola vez)."""
    centro = c.ANCHO_VENTANA // 2
    # Tarjetas de 250 px separadas 270 px entre centros, centradas en la ventana
    primera = centro - 270 * (len(jefes) - 1) // 2
    tarjetas = [TarjetaJefe(i, clase, (primera + 270 * i, 290)) for i, clase in enumerate(jefes)]
    seleccion = Boton("Selección de jefe", c.IR_A_SELECCION, (centro, 450))
    return {
        c.MENU: [Boton("Jugar", c.JUGAR, (centro, 400)), Boton("Salir", c.SALIR, (centro, 470))],
        c.SELECCION: tarjetas + [Boton("Volver", c.VOLVER, (centro, 530), 200)],
        c.DETALLE: [Boton("Combatir", c.COMBATIR, (centro - 130, 520), 240),
                    Boton("Volver", c.VOLVER, (centro + 130, 520), 240)],
        c.JUGANDO: [Boton("Pausa", c.PAUSAR, (c.ANCHO_VENTANA - 80, 90), 120, 36)],
        c.PAUSA: [Boton("Continuar", c.CONTINUAR, (centro, 260)),
                  Boton("Reintentar", c.REINTENTAR, (centro, 330)),
                  Boton("Selección de jefe", c.IR_A_SELECCION, (centro, 400)),
                  Boton("Salir", c.SALIR, (centro, 470))],
        c.VICTORIA: [Boton("Siguiente jefe", c.SIGUIENTE, (centro, 380)), seleccion],
        c.DERROTA: [Boton("Reintentar", c.REINTENTAR, (centro, 380)), seleccion],
        c.CAMPANA: [Boton("Selección de jefe", c.IR_A_SELECCION, (centro, 400)),
                    Boton("Salir", c.SALIR, (centro, 470))],
    }


def boton_pulsado(botones, pos):
    """Devuelve el botón que contiene el punto (como máximo uno), o None."""
    for boton in botones:
        if boton.rect.collidepoint(pos):
            return boton
    return None


def dibujar_botones(pantalla, fuentes, botones, pos_raton, juego):
    for boton in botones:
        boton.dibujar(pantalla, fuentes, pos_raton, juego)


def texto_centrado(pantalla, fuente, texto, y, color=theme.TEXTO):
    superficie = fuente.render(texto, True, color)
    pantalla.blit(superficie, superficie.get_rect(center=(c.ANCHO_VENTANA // 2, y)))


def dibujar_menu(pantalla, fuentes, fondos, capa, aviso):
    theme.dibujar_fondo(pantalla, fondos, "nucleo")
    pantalla.blit(capa, (0, 0))
    texto_centrado(pantalla, fuentes["titulo"], c.NOMBRE_ROBOT, 90)
    texto_centrado(pantalla, fuentes["grande"], "Arena Eclipse", 160, theme.PULSO)
    controles = [
        "A / D o flechas: moverse      Espacio: saltar",
        "S o flecha abajo: agacharse      Shift en el aire: propulsor",
        "Ratón: apuntar (360° en el aire)      Clic izquierdo: disparar",
        "Clic derecho: superataque (se carga con 10 aciertos)",
    ]
    for i, linea in enumerate(controles):
        texto_centrado(pantalla, fuentes["normal"], linea, 225 + i * 36)
    if aviso:
        texto_centrado(pantalla, fuentes["normal"], aviso, 545, theme.AVISO)


def dibujar_seleccion(pantalla, fuentes, fondos, capa):
    theme.dibujar_fondo(pantalla, fondos, "nucleo")
    pantalla.blit(capa, (0, 0))
    texto_centrado(pantalla, fuentes["grande"], "Elige un jefe", 70)
    texto_centrado(pantalla, fuentes["normal"], "Vence a cada jefe para desbloquear el siguiente", 125, theme.PULSO)


def dibujar_detalle(pantalla, fuentes, fondos, capa, clase_jefe, indice):
    theme.dibujar_fondo(pantalla, fondos, clase_jefe.FONDO)
    pantalla.blit(capa, (0, 0))
    texto_centrado(pantalla, fuentes["grande"], clase_jefe.NOMBRE, 80)
    texto_centrado(pantalla, fuentes["normal"], f"Jefe {indice + 1} · Dificultad: {clase_jefe.DIFICULTAD}", 135, theme.AVISO)
    texto_centrado(pantalla, fuentes["normal"],
                   f"Fase 1 «{clase_jefe.NOMBRE_FASE_1}»: {clase_jefe.VIDA_FASE_1} de vida   ·   "
                   f"Fase 2 «{clase_jefe.NOMBRE_FASE_2}»: {clase_jefe.VIDA_FASE_2}", 185)
    for i, linea in enumerate(clase_jefe.DESCRIPCION):
        texto_centrado(pantalla, fuentes["normal"], linea, 260 + i * 42)


def dibujar_mensaje(pantalla, fuentes, capa_oscura, titulo, detalle):
    """Capa semitransparente con un título y un detalle (pausa, victoria, derrota o campaña)."""
    pantalla.blit(capa_oscura, (0, 0))
    texto_centrado(pantalla, fuentes["grande"], titulo, 150)
    texto_centrado(pantalla, fuentes["normal"], detalle, 215)
