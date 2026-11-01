"""Coordina los estados del juego (menú, nivel, arena, pausa, victoria y derrota)
y contiene el bucle principal."""

import pygame

import config as c
from entities.boss import Jefe
from entities.robot import Robot
from systems import collisions
from ui import hud, menus
from world import level, theme


class Juego:
    """Guarda el estado de la partida (pantalla, escena, listas del mundo y cámara).

    Cada entidad guarda sus propios datos para no duplicarlos: el robot su salud,
    postura, energía y espera de disparo; el jefe su vida, fase y patrones.
    """

    def __init__(self):
        # Recursos que se crean una sola vez
        self.fuentes = theme.crear_fuentes()
        self.capa_oscura = theme.crear_capa_oscura()
        self.fondos = theme.crear_fondos()
        self.botones = menus.crear_botones()
        self.reiniciar()
        self.estado = c.INICIO  # al abrir el juego se ve la pantalla inicial

    # ----- Estados ----------------------------------------------------------
    def reiniciar(self):
        """Reinicia toda la aventura: nivel, robot, enemigos, jefe y proyectiles."""
        self.escena = c.NIVEL
        self.solidos = level.crear_solidos()
        self.portal = level.crear_portal()
        self.robot = Robot(*level.POSICION_INICIAL)
        self.posicion_segura = self.robot.rect.bottomleft  # pies en el último lugar seguro
        self.enemigos = level.crear_enemigos()
        self.baterias = level.crear_baterias()
        self.pulsos = []        # proyectiles de NEXO-7 (aliados)
        self.proyectiles = []   # proyectiles del jefe (hostiles)
        self.jefe = None
        self.contador = 0
        self.esperar_soltar_clic = False  # True: hay que soltar el clic antes de disparar
        self.estado = c.JUGANDO
        self.motivo_derrota = ""
        self.camara_x = 0

    def iniciar_partida(self):
        """Usado por "Iniciar", "Reiniciar" y "Volver a jugar"."""
        self.reiniciar()
        self.esperar_soltar_clic = True  # el clic del botón no debe disparar

    def entrar_arena(self):
        """Pasa a la arena del jefe. Solo ocurre una vez: la arena no tiene portal."""
        self.escena = c.ARENA
        self.solidos = level.crear_solidos_arena()
        self.enemigos = []
        self.pulsos = []
        self.proyectiles = []
        self.robot = Robot(*level.POSICION_INICIAL_ARENA)  # con los 3 corazones
        self.jefe = Jefe(level.ZONA_JEFE)
        self.camara_x = 0  # la arena es fija, sin cámara

    def ancho_mundo(self):
        return c.ANCHO_NIVEL if self.escena == c.NIVEL else c.ANCHO_VENTANA

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
        if boton.accion == c.INICIAR:
            self.iniciar_partida()
        elif boton.accion == c.PAUSAR:
            self.estado = c.PAUSA
        elif boton.accion == c.CONTINUAR:
            self.estado = c.JUGANDO
            self.esperar_soltar_clic = True
        return boton.accion  # SALIR lo atiende el bucle principal

    def puede_atacar(self):
        # En los menús, en pausa o al terminar la partida los ataques están bloqueados
        return self.estado == c.JUGANDO and self.robot.puede_disparar(len(self.pulsos))

    def lanzar_pulso(self):
        if self.puede_atacar():
            self.pulsos.append(self.robot.disparar())

    # ----- Actualización ----------------------------------------------------
    def actualizar(self, teclas, pos_raton=None, clic_presionado=False):
        """Avanza el juego un paso fijo de 1/60 s."""
        # En el menú, en pausa o con la partida terminada no se mueve nada
        # y tampoco corren los temporizadores
        if self.estado != c.JUGANDO:
            return

        self.robot.actualizar_temporizadores()
        if not clic_presionado:
            self.esperar_soltar_clic = False

        self.robot.actualizar(teclas, self.solidos, self.ancho_mundo())
        if self.escena == c.NIVEL:
            self.actualizar_nivel()
        else:
            self.actualizar_arena()
        if self.estado != c.JUGANDO:
            return

        # El cursor está en coordenadas de pantalla; sumando la cámara se obtiene
        # su posición en el mundo
        if pos_raton is not None:
            self.robot.apuntar(pos_raton[0] + self.camara_x, pos_raton[1])
        # Mantener el clic dispara de forma repetida, respetando la espera
        if clic_presionado and not self.esperar_soltar_clic:
            self.lanzar_pulso()

    def actualizar_pulsos(self):
        """Mueve los pulsos y elimina los que chocan o llegan a su límite."""
        for pulso in self.pulsos[:]:  # se recorre una copia porque se borran elementos
            pulso.actualizar()
            enemigo = next((e for e in self.enemigos if pulso.rect.colliderect(e.rect)), None)
            if enemigo:
                self.enemigos.remove(enemigo)  # cada pulso elimina a un solo enemigo
                self.pulsos.remove(pulso)
            elif self.jefe and self.jefe.puede_recibir_danio() and pulso.rect.colliderect(self.jefe.rect):
                # Cada impacto resta un punto (durante la transición los pulsos lo atraviesan)
                self.jefe.recibir_impacto(pulso.danio)
                self.pulsos.remove(pulso)
            elif pulso.debe_desaparecer(self.ancho_mundo()) or collisions.toca_alguno(pulso.rect, self.solidos):
                self.pulsos.remove(pulso)

    def actualizar_nivel(self):
        for enemigo in self.enemigos:
            enemigo.actualizar()
        self.actualizar_pulsos()

        for bateria in self.baterias:
            if not bateria.recogida and self.robot.rect.colliderect(bateria.rect):
                bateria.recogida = True
                self.contador += 1

        # Solo se guarda como segura una posición con margen hacia ambos bordes
        apoyo = self.robot.apoyo
        if (apoyo and self.robot.rect.left - apoyo.left >= c.MARGEN_SEGURO
                and apoyo.right - self.robot.rect.right >= c.MARGEN_SEGURO):
            self.posicion_segura = self.robot.rect.bottomleft

        # Tocar a un enemigo resta un corazón (el ataque no da invulnerabilidad)
        if collisions.toca_alguno(self.robot.rect, [e.rect for e in self.enemigos]):
            self.robot.recibir_danio()
        if self.robot.rect.top > c.ALTO_VENTANA:
            self.robot.caer_al_vacio(self.posicion_segura)

        if self.robot.vidas <= 0:
            self.estado = c.DERROTA
            self.motivo_derrota = f"{c.NOMBRE_ROBOT} se quedó sin corazones"
        elif self.robot.rect.colliderect(self.portal):
            self.entrar_arena()
        else:
            self.actualizar_camara()

    def actualizar_arena(self):
        self.jefe.actualizar(self.robot, self.proyectiles)
        self.actualizar_pulsos()
        # Durante la transición a la fase 2 no hay proyectiles hostiles ni daño
        if self.jefe.en_transicion():
            self.proyectiles.clear()

        for proyectil in self.proyectiles[:]:
            proyectil.actualizar()
            if proyectil.rect.colliderect(self.robot.rect):
                # Desaparece al impactar, así que solo puede causar daño una vez
                self.proyectiles.remove(proyectil)
                self.robot.recibir_danio()
            elif proyectil.debe_desaparecer(c.ANCHO_VENTANA):
                self.proyectiles.remove(proyectil)

        if self.jefe.puede_danar() and self.robot.rect.colliderect(self.jefe.rect):
            self.robot.recibir_danio()

        # Si los dos llegan a cero en la misma actualización, gana el jugador
        if self.jefe.derrotado():
            self.estado = c.VICTORIA
            self.proyectiles = []
            self.pulsos = []
        elif self.robot.vidas <= 0:
            self.estado = c.DERROTA
            self.motivo_derrota = f"El {c.NOMBRE_JEFE} venció a {c.NOMBRE_ROBOT}"

    def actualizar_camara(self):
        # Centra al robot, pero sin mostrar nada fuera del nivel
        objetivo = self.robot.rect.centerx - c.ANCHO_VENTANA // 2
        self.camara_x = max(0, min(objetivo, c.ANCHO_NIVEL - c.ANCHO_VENTANA))

    # ----- Dibujo -----------------------------------------------------------
    def dibujar(self, pantalla, pos_raton=(-1, -1)):
        if self.estado == c.INICIO:
            menus.dibujar_inicio(pantalla, self.fuentes, self.fondos)
        else:
            self.dibujar_partida(pantalla)
            if self.estado == c.PAUSA:
                menus.dibujar_mensaje(pantalla, self.fuentes, self.capa_oscura, "Pausa", "El juego está detenido")
            elif self.estado == c.VICTORIA:
                menus.dibujar_mensaje(pantalla, self.fuentes, self.capa_oscura, f"¡{c.NOMBRE_ROBOT} apagó al Centinela!",
                                      f"Baterías recogidas: {self.contador} de {len(self.baterias)}")
            elif self.estado == c.DERROTA:
                menus.dibujar_mensaje(pantalla, self.fuentes, self.capa_oscura, "Fin de la partida", self.motivo_derrota)
        menus.dibujar_botones(pantalla, self.fuentes, self.botones[self.estado], pos_raton)
        if self.estado == c.JUGANDO:
            hud.dibujar_apuntado(pantalla, self.robot, self.camara_x, pos_raton)

    def dibujar_partida(self, pantalla):
        if self.escena == c.NIVEL:
            theme.dibujar_fondo_nivel(pantalla, self.fondos, self.camara_x)
        else:
            theme.dibujar_fondo_arena(pantalla, self.fondos)
        for solido in self.solidos:
            theme.dibujar_solido(pantalla, solido.move(-self.camara_x, 0))
        if self.escena == c.NIVEL:
            theme.dibujar_portal(pantalla, self.portal.move(-self.camara_x, 0))
            for bateria in self.baterias:
                bateria.dibujar(pantalla, self.camara_x)
            for enemigo in self.enemigos:
                enemigo.dibujar(pantalla, self.camara_x)
        else:
            self.jefe.dibujar(pantalla)
            for proyectil in self.proyectiles:
                proyectil.dibujar(pantalla, 0)

        # Al terminar la partida el robot se ve siempre (no parpadea)
        if self.estado != c.JUGANDO or self.robot.visible():
            self.robot.dibujar(pantalla, self.camara_x)
        for pulso in self.pulsos:
            pulso.dibujar(pantalla, self.camara_x)
        hud.dibujar_hud(pantalla, self.fuentes, self.robot, self.contador, len(self.baterias), self.puede_atacar())
        if self.jefe:
            hud.dibujar_barra_jefe(pantalla, self.fuentes, self.jefe)
            # Anuncio de la transición (oculto bajo los menús)
            if self.jefe.en_transicion() and self.estado == c.JUGANDO:
                hud.dibujar_anuncio_fase(pantalla, self.fuentes, "Fase 2: Sobrecarga")


def ejecutar():
    """Bucle principal con paso fijo: el juego avanza igual a cualquier FPS."""
    pygame.init()
    pantalla = pygame.display.set_mode((c.ANCHO_VENTANA, c.ALTO_VENTANA))
    pygame.display.set_caption(f"RoboAventura: {c.NOMBRE_ROBOT}")
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

        # Durante la partida se dibuja una mira en lugar del cursor del sistema
        pygame.mouse.set_visible(juego.estado != c.JUGANDO)
        juego.dibujar(pantalla, pos_raton)
        pygame.display.flip()

    pygame.quit()
