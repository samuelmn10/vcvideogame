"""Coordina las pantallas (menú, selección, detalle, combate, pausa, victoria,
derrota y campaña completada) y contiene el bucle principal."""

import pygame

import config as c
from entities.bosses import JEFES
from entities.robot import Robot
from systems import collisions
from systems.progress import Progreso
from ui import hud, menus
from world import arena, theme


class Juego:
    """Guarda la pantalla actual, el combate en curso y el progreso.

    Cada entidad guarda sus propios datos para no duplicarlos: el robot su salud,
    postura, energía y espera de disparo; el jefe su vida, fase y patrones;
    Progreso los desbloqueos y las victorias.
    """

    def __init__(self, ruta_progreso=c.ARCHIVO_PROGRESO):
        # Recursos que se crean una sola vez
        self.fuentes = theme.crear_fuentes()
        self.capa_oscura = theme.crear_capa_oscura()
        self.fondos = theme.crear_fondos()
        self.botones = menus.crear_botones(JEFES)
        self.progreso = Progreso(ruta_progreso, len(JEFES))
        self.estado = c.MENU
        self.indice_jefe = 0     # jefe elegido (o en combate)
        self.limpiar_combate()

    # ----- Combate ----------------------------------------------------------
    def limpiar_combate(self):
        self.robot = None
        self.jefe = None
        self.solidos = []
        self.pulsos = []        # proyectiles de NEXO-7 (aliados)
        self.proyectiles = []   # proyectiles del jefe (hostiles)
        self.esperar_soltar_clic = False  # True: hay que soltar el clic antes de disparar

    def iniciar_combate(self, indice):
        """Usado por "Combatir" y "Reintentar": 4 corazones, energía llena y jefe nuevo."""
        self.indice_jefe = indice
        self.jefe = JEFES[indice]()
        self.solidos = arena.crear_solidos(self.jefe.PLATAFORMAS)
        self.robot = Robot(*arena.POSICION_INICIAL_ROBOT)
        self.pulsos = []
        self.proyectiles = []
        self.estado = c.JUGANDO
        self.esperar_soltar_clic = True  # el clic del botón no debe disparar

    # ----- Entrada ----------------------------------------------------------
    def manejar_tecla(self, tecla):
        # El teclado solo mueve al robot; se dispara y se usan los menús con el ratón
        if self.estado == c.JUGANDO and tecla == c.TECLA_SALTO:
            self.robot.saltar(self.solidos)

    def manejar_clic(self, pos):
        """Ejecuta la acción del botón pulsado (como máximo uno) y la devuelve."""
        boton = menus.boton_pulsado(self.botones[self.estado], pos)
        if boton is None:
            return None
        accion = boton.accion
        if accion == c.ELEGIR:
            if not self.progreso.desbloqueado(boton.indice):
                return None  # los bloqueados se ven, pero no se eligen
            self.indice_jefe = boton.indice
            self.estado = c.DETALLE
        elif accion == c.JUGAR:
            self.estado = c.SELECCION
        elif accion == c.VOLVER:
            self.estado = c.MENU if self.estado == c.SELECCION else c.SELECCION
        elif accion == c.COMBATIR or accion == c.REINTENTAR:
            self.iniciar_combate(self.indice_jefe)
        elif accion == c.PAUSAR:
            self.estado = c.PAUSA
        elif accion == c.CONTINUAR:
            self.estado = c.JUGANDO
            self.esperar_soltar_clic = True
        elif accion == c.IR_A_SELECCION:
            self.limpiar_combate()
            self.estado = c.SELECCION
        elif accion == c.SIGUIENTE:
            self.limpiar_combate()
            self.indice_jefe += 1
            self.estado = c.DETALLE
        return accion  # SALIR lo atiende el bucle principal

    def puede_atacar(self):
        # En los menús, en pausa o al terminar el combate los ataques están bloqueados
        pulsos_normales = sum(1 for p in self.pulsos if not p.superataque)
        return self.estado == c.JUGANDO and self.robot.puede_disparar(pulsos_normales)

    def puede_superataque(self):
        """Cargado, en combate, sin otra descarga en el aire y fuera de la transición
        (durante la transición el jefe no recibe daño y se desperdiciaría)."""
        return (self.estado == c.JUGANDO and self.robot.super_listo()
                and not self.jefe.en_transicion() and not any(p.superataque for p in self.pulsos))

    def manejar_clic_derecho(self):
        if self.puede_superataque():
            self.pulsos.append(self.robot.disparar_super())

    def lanzar_pulso(self):
        if self.puede_atacar():
            self.pulsos.append(self.robot.disparar())

    # ----- Actualización ----------------------------------------------------
    def actualizar(self, teclas, pos_raton=None, clic_presionado=False):
        """Avanza el combate un paso fijo de 1/60 s."""
        # Fuera del combate (menús, pausa, fin) no se mueve nada ni corren los temporizadores
        if self.estado != c.JUGANDO:
            return

        self.robot.actualizar_temporizadores()
        if not clic_presionado:
            self.esperar_soltar_clic = False

        self.robot.actualizar(teclas, self.solidos, c.ANCHO_VENTANA)
        self.jefe.actualizar(self.robot, self.proyectiles)
        self.actualizar_pulsos()
        # Durante la transición de fase no hay proyectiles hostiles ni daño
        if self.jefe.en_transicion():
            self.proyectiles.clear()
        self.actualizar_proyectiles()
        if self.jefe.puede_danar() and self.robot.rect.colliderect(self.jefe.rect):
            self.robot.recibir_danio()
        self.revisar_fin()
        if self.estado != c.JUGANDO:
            return

        # Apuntar (la arena no tiene cámara: pantalla y mundo coinciden)
        if pos_raton is not None:
            self.robot.apuntar(*pos_raton)
        # Mantener el clic dispara de forma repetida, respetando la espera
        if clic_presionado and not self.esperar_soltar_clic:
            self.lanzar_pulso()

    def actualizar_pulsos(self):
        """Mueve los pulsos y elimina los que chocan o llegan a su límite."""
        for pulso in self.pulsos[:]:  # se recorre una copia porque se borran elementos
            pulso.actualizar()
            if pulso.superataque:
                # La descarga de núcleo destruye los proyectiles hostiles que toca
                self.proyectiles = [p for p in self.proyectiles if not p.rect.colliderect(pulso.rect)]
            if self.jefe.puede_recibir_danio() and pulso.rect.colliderect(self.jefe.rect):
                # Un pulso resta 1 y carga el superataque; la descarga resta DANIO_SUPER
                # (durante la transición los pulsos lo atraviesan)
                self.jefe.recibir_impacto(pulso.danio)
                if not pulso.superataque:
                    self.robot.registrar_acierto()
                self.pulsos.remove(pulso)
            elif pulso.debe_desaparecer(c.ANCHO_VENTANA) or collisions.toca_alguno(pulso.rect, self.solidos):
                self.pulsos.remove(pulso)

    def actualizar_proyectiles(self):
        for proyectil in self.proyectiles[:]:
            proyectil.actualizar()
            if proyectil.rect.colliderect(self.robot.rect):
                # Desaparece al impactar, así que solo puede causar daño una vez
                self.proyectiles.remove(proyectil)
                self.robot.recibir_danio()
            elif proyectil.debe_desaparecer(c.ANCHO_VENTANA):
                self.proyectiles.remove(proyectil)

    def revisar_fin(self):
        # Si los dos llegan a cero en la misma actualización, gana el jugador
        if self.jefe.derrotado():
            self.proyectiles = []
            self.pulsos = []
            self.progreso.registrar_victoria(self.indice_jefe)
            ultimo = self.indice_jefe == len(JEFES) - 1
            self.estado = c.CAMPANA if ultimo else c.VICTORIA
        elif self.robot.vidas <= 0:
            self.estado = c.DERROTA

    # ----- Dibujo -----------------------------------------------------------
    def dibujar(self, pantalla, pos_raton=(-1, -1)):
        if self.estado == c.MENU:
            menus.dibujar_menu(pantalla, self.fuentes, self.fondos, self.capa_oscura, self.progreso.aviso)
        elif self.estado == c.SELECCION:
            menus.dibujar_seleccion(pantalla, self.fuentes, self.fondos, self.capa_oscura)
        elif self.estado == c.DETALLE:
            menus.dibujar_detalle(pantalla, self.fuentes, self.fondos, self.capa_oscura,
                                  JEFES[self.indice_jefe], self.indice_jefe)
        else:
            self.dibujar_combate(pantalla)
            nombre = self.jefe.NOMBRE
            if self.estado == c.PAUSA:
                menus.dibujar_mensaje(pantalla, self.fuentes, self.capa_oscura, "Pausa", "El combate está detenido")
            elif self.estado == c.VICTORIA:
                siguiente = JEFES[self.indice_jefe + 1].NOMBRE
                menus.dibujar_mensaje(pantalla, self.fuentes, self.capa_oscura, f"¡{nombre} derrotado!",
                                      f"Desbloqueaste: {siguiente}")
            elif self.estado == c.DERROTA:
                menus.dibujar_mensaje(pantalla, self.fuentes, self.capa_oscura, "Derrota",
                                      f"{nombre} venció a {c.NOMBRE_ROBOT}. Los desbloqueos se conservan.")
            elif self.estado == c.CAMPANA:
                menus.dibujar_mensaje(pantalla, self.fuentes, self.capa_oscura, "¡Campaña completada!",
                                      f"{c.NOMBRE_ROBOT} venció a los {len(JEFES)} jefes de la Arena Eclipse")
        menus.dibujar_botones(pantalla, self.fuentes, self.botones[self.estado], pos_raton, self)
        if self.estado == c.JUGANDO:
            hud.dibujar_apuntado(pantalla, self.robot, 0, pos_raton)

    def dibujar_combate(self, pantalla):
        theme.dibujar_fondo(pantalla, self.fondos, self.jefe.FONDO)
        for solido in self.solidos:
            theme.dibujar_solido(pantalla, solido)
        self.jefe.dibujar(pantalla)
        for proyectil in self.proyectiles:
            proyectil.dibujar(pantalla, 0)
        # Al terminar el combate el robot se ve siempre (no parpadea)
        if self.estado != c.JUGANDO or self.robot.visible():
            self.robot.dibujar(pantalla, 0)
        for pulso in self.pulsos:
            pulso.dibujar(pantalla, 0)
        hud.dibujar_hud(pantalla, self.fuentes, self.robot, self.puede_atacar())
        hud.dibujar_super(pantalla, self.fuentes, self.robot)
        hud.dibujar_barra_jefe(pantalla, self.fuentes, self.jefe)
        # Nombre de la nueva fase durante la transición (oculto bajo los menús)
        if self.jefe.en_transicion() and self.estado == c.JUGANDO:
            hud.dibujar_anuncio_fase(pantalla, self.fuentes, f"Fase 2: {self.jefe.NOMBRE_FASE_2}")


def ejecutar():
    """Bucle principal con paso fijo: el juego avanza igual a cualquier FPS."""
    pygame.init()
    pantalla = pygame.display.set_mode((c.ANCHO_VENTANA, c.ALTO_VENTANA))
    pygame.display.set_caption(c.TITULO)
    reloj = pygame.time.Clock()
    juego = Juego()

    ejecutando = True
    acumulado = 0.0  # tiempo real pendiente de simular
    while ejecutando:
        # Se simulan tantos pasos de 1/60 s como tiempo real haya pasado
        acumulado += min(reloj.tick(c.FPS) / 1000, 0.25)  # tope para no "saltar" tras un bloqueo
        clic_atendido = False  # como máximo un clic por cuadro: un clic = una acción
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                ejecutando = False  # botón de cierre de la ventana
            elif evento.type == pygame.KEYDOWN:
                juego.manejar_tecla(evento.key)
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == c.BOTON_SUPER:
                juego.manejar_clic_derecho()  # superataque (los botones usan solo el clic izquierdo)
            elif evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1 and not clic_atendido:
                clic_atendido = True
                if juego.manejar_clic(evento.pos) == c.SALIR:
                    ejecutando = False

        teclas = pygame.key.get_pressed()
        pos_raton = pygame.mouse.get_pos()
        clic_presionado = pygame.mouse.get_pressed()[c.BOTON_DISPARO]
        while acumulado >= c.PASO:
            juego.actualizar(teclas, pos_raton, clic_presionado)
            acumulado -= c.PASO

        # Durante el combate se dibuja una mira en lugar del cursor del sistema
        pygame.mouse.set_visible(juego.estado != c.JUGANDO)
        juego.dibujar(pantalla, pos_raton)
        pygame.display.flip()

    pygame.quit()
