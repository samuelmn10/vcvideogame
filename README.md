# NEXO-7: Arena Eclipse

Juego de combates contra jefes en 2D, hecho en Python con Pygame. Es una actividad de **vibecoding**: el juego se desarrolló con IA como copiloto, a partir de prompts progresivos. Empezó como el plataformas "RoboAventura" (prompts 1 a 6) y en el prompt 7 se transformó en este juego.

**NEXO-7**, un robot explorador, enfrenta a los tres sistemas de defensa de una estación abandonada, en orden de dificultad: el **Centinela Eclipse**, el **Embestidor Férreo** y el **Serafín Voltaico**. Vencer a cada uno desbloquea al siguiente. NEXO-7 tiene cuatro corazones, apunta y dispara con el ratón, se agacha para esquivar, tiene un propulsor breve y un superataque que se carga acertando disparos.

## Instalación y ejecución

Requisitos: Python 3.10 o superior.

```bash
pip install -r requirements.txt
```

```bash
python main.py
```

> **Nota:** el proyecto usa **pygame-ce** (la edición comunitaria de Pygame), que tiene versiones listas para Python 3.10 a 3.14 y se usa igual, con `import pygame`. Se eligió porque pygame 2.6.1 no se pudo instalar en Python 3.14 (error `'SDL.h' file not found`). Si ya tenías instalado `pygame`, desinstálalo antes, porque los dos no pueden convivir:
>
> ```bash
> pip uninstall pygame
> ```

## Controles

| Control | Acción |
|---|---|
| A / D o flechas ← → | Moverse |
| Espacio | Saltar |
| S o flecha abajo (en el suelo) | Agacharse (mitad de altura, más lento) |
| Shift (en el aire) | Propulsor: hasta 0,8 s de uso; se recarga en 1,5 s apoyado en el suelo o una plataforma |
| Ratón | Apuntar: ±60° en el suelo, 360° en el aire |
| Clic izquierdo (se puede mantener) | Disparar pulsos (uno cada 0,3 s, alcance 350 px, máximo 2 en pantalla) |
| Clic derecho | Superataque (descarga de núcleo), disponible tras 10 pulsos acertados al jefe |
| Clic izquierdo en los menús | Botones; un clic en un botón nunca dispara |

## Progresión

1. **Menú principal:** Jugar o Salir.
2. **Selección de jefe:** se ven los tres jefes, con su dificultad y su estado:
   - **Bloqueado** (gris, con candado): se ve, pero no se puede elegir;
   - **Disponible**;
   - **Derrotado (n)**, con la cantidad de victorias.
3. **Detalle:** características del jefe (fases, vida y patrones) y el botón **Combatir**.
4. **Combate:** 4 corazones y energía llena. Cada impacto resta un corazón, con 1,2 s de invulnerabilidad. El botón **Pausa** ofrece Continuar, Reintentar, Selección de jefe y Salir.
5. **Final del combate:**
   - **Victoria:** "Siguiente jefe" (va al detalle del jefe recién desbloqueado) o "Selección de jefe".
   - **Derrota:** "Reintentar" o "Selección de jefe". **Perder no quita desbloqueos.**
   - Vencer al tercer jefe muestra la pantalla **¡Campaña completada!**.

Al principio solo está disponible el Jefe 1. Vencerlo desbloquea al 2, y vencer al 2 desbloquea al 3. Cualquier jefe desbloqueado se puede volver a combatir.

### Guardado local

El progreso se guarda en `progreso.json`, junto a `main.py`. El archivo no se sube al repositorio (está en `.gitignore`). Solo guarda esto:

```json
{"desbloqueados": 2, "victorias": [1, 0, 0]}
```

- **Si no existe:** empieza una progresión nueva (solo el Jefe 1).
- **Si está dañado** (no es JSON, faltan datos o los valores no tienen sentido): el juego no se cierra. Restablece el progreso y avisa en el menú: "El archivo de progreso estaba dañado: se restableció el progreso."
- **Al escribir:** primero escribe un archivo temporal y después reemplaza el real, para que un cierre a la mitad no lo dañe.
- **Para empezar de cero,** se borra `progreso.json`.

## Los tres jefes

| | Centinela Eclipse | Embestidor Férreo | Serafín Voltaico |
|---|---|---|---|
| Dificultad | Inicial | Intermedia | Avanzada |
| Vida (fase 1 + fase 2) | 24 + 32 | 36 + 48 | 48 + 64 |
| Movimiento | En el suelo, patrulla lenta (1,5 px/paso) | En el suelo, rápido (3 px/paso) y embestidas marcadas de 320 px (400 en la fase 2) | Vuela entre 3 posiciones altas y 2 bajas |
| Patrones de la fase 1 | Proyectiles bajos · ráfaga dirigida | Embestida anunciada · abanico dirigido de 5 | Abanico descendente de 5 · descarga aérea dirigida |
| Patrones de la fase 2 | Bajos más seguidos · ráfaga doble (6 disparos) | Embestida + aviso + ráfaga · doble abanico | Abanico + ráfaga · lluvia doble |
| Aviso / descanso | 0,8 s / 1,4 s | 0,67 s / 1 s | 0,6 s y 0,5 s / 0,8 s (abajo, ventana de ataque) |
| Qué enseña | Leer avisos y esquivar | Saltar, agacharse y moverse | Apuntar en varias direcciones y usar el propulsor |

### Superataque

Cada pulso que acierta al jefe llena un poco la barra **Súper** del HUD. Con **10 aciertos**, la barra brilla, el pecho de NEXO-7 se ilumina y aparece "¡Clic derecho!". Con clic derecho sale una **descarga de núcleo**:
- un orbe grande en la dirección del arma, a 10 px por paso y con 700 px de alcance;
- hace **5 de daño** (un pulso hace 1) y **destruye los proyectiles hostiles** que toca;
- vacía la carga, y no suma carga por sí misma;
- no cuenta para el máximo de 2 pulsos, y solo puede haber una descarga a la vez.

No se puede usar en menús, en pausa, al terminar el combate ni durante la transición de fase (el jefe no recibe daño ahí); la carga se conserva para después. Cada combate y cada reintento empiezan con la carga en 0.

Reglas comunes:
- En el descanso entre ataques, los jefes de suelo (Centinela y Embestidor) **no se acercan a NEXO-7 a menos de 160 px**, y si están más cerca se alejan. Así solo hacen daño con ataques avisados, o si NEXO-7 camina hacia ellos.
- Cada jefe tiene dos fases. Agotar la primera barra inicia una **transición única de 1,5 s**: se borran los proyectiles hostiles, nadie recibe daño y aparece "Fase 2: …" con el nombre de la nueva fase.
- La segunda barra se carga **una sola vez**, y agotarla da la victoria.
- Los disparos dirigidos no persiguen a NEXO-7.
- Nunca hay más de 12 proyectiles hostiles: si no hay lugar, la emisión espera.

## Estructura del proyecto

```
main.py                 Punto de entrada: solo llama a game.ejecutar()
config.py               Dimensiones, controles, física, robot, reglas comunes de los jefes y nombres de pantallas
game.py                 Clase Juego (pantallas, combate, victoria y derrota) y bucle principal de paso fijo
entities/
  robot.py              NEXO-7: salud, invulnerabilidad, postura, propulsor, apuntado y disparo
  projectiles.py        Proyectil: movimiento, alcance, daño y cuándo desaparece (aliado u hostil)
  bosses/
    __init__.py         Lista JEFES en el orden de la campaña
    base.py             JefeBase: dos fases, transición, estados aviso/ataque/descanso, límite de 12, utilidades
    centinela.py        Jefe 1 (sus parámetros están al principio del archivo)
    embestidor.py       Jefe 2
    serafin.py          Jefe 3
systems/
  movement.py           Desplazamiento horizontal, gravedad, salto y propulsión
  collisions.py         Choques horizontales y verticales, límites y espacio libre
  progress.py           Progreso en JSON: carga, validación, restablecimiento y guardado seguro
world/
  arena.py              Suelo continuo, plataformas de cada jefe y posición inicial de NEXO-7
  theme.py              Colores, fuentes y fondos de las tres arenas (núcleo, hangar y cúpula)
ui/
  menus.py              Botones, tarjetas de jefe y pantallas de menú, selección, detalle y mensajes
  hud.py                Corazones, energía, ataque, nombre, fase y vida del jefe, y mira
```

- **Retirados del flujo** (siguen en el historial de git): `world/level.py` (nivel, baterías y portal), `entities/enemies.py` (enemigos comunes) y `entities/boss.py` (el jefe único de la versión 6).
- **Dependencias sin ciclos:** `config` y `theme` no importan nada del juego, y solo `game.py` reúne todo.
- **Recursos que se crean una sola vez:** fuentes, capa oscura, botones y los tres fondos.
- **NPCs:** no hay. Irían en `entities/npcs.py`.

## Modelo de funcionamiento

```
MENÚ --Jugar--> SELECCIÓN --jefe disponible--> DETALLE --Combatir--> JUGANDO <--Pausa/Continuar--> PAUSA
                  ^   |                          |                     |                            |
                  |   +--Volver--> MENÚ          +--Volver--> SELECCIÓN  |              Reintentar / Selección / Salir
                  |                                                    |
                  +----Selección de jefe----- VICTORIA / DERROTA / CAMPAÑA COMPLETADA
VICTORIA --Siguiente jefe--> DETALLE del siguiente · DERROTA --Reintentar--> JUGANDO
```

| Dueño | Datos |
|---|---|
| `Juego` | pantalla actual, jefe elegido, robot, jefe, sólidos, pulsos (aliados), proyectiles (hostiles), "esperar a soltar el clic" |
| `Robot` | rectángulo, velocidad, apoyo, postura, energía, apuntado, vidas, invulnerabilidad, espera de disparo |
| `JefeBase` y cada jefe | posición, fase, vida y vida máxima, transición, estado, temporizador, patrón y datos propios de sus ataques |
| `Progreso` | jefes desbloqueados, victorias y aviso de restablecimiento |

**Cómo se agrega un jefe:** se crea `entities/bosses/nuevo.py` con una clase que hereda de `JefeBase`. Esa clase define sus datos (nombre, vidas, avisos, fondo, plataformas), `patrones()`, `duracion_aviso()`, `duracion_descanso()`, `mover_en_descanso()`, `iniciar_ataque()`, `paso_ataque()` y `dibujar()`. Después se agrega a la lista `JEFES`.

## Dónde modificar cada cosa

| Quiero cambiar… | Archivo |
|---|---|
| Velocidades, salto, propulsor, corazones, ataque, controles | `config.py` |
| Reglas comunes de los jefes (transición, límite de proyectiles) | `config.py` y `entities/bosses/base.py` |
| Vida, avisos, descansos, velocidades y patrones de un jefe | Su módulo en `entities/bosses/` (parámetros al principio) |
| Orden de la campaña | `entities/bosses/__init__.py` (lista `JEFES`) |
| Plataformas de una arena | Atributo `PLATAFORMAS` del jefe; el suelo, en `world/arena.py` |
| Colores y fondos | `world/theme.py` (más el `dibujar()` de cada jefe) |
| Pantallas y botones | `ui/menus.py` |
| Información en combate | `ui/hud.py` |
| Formato del guardado | `systems/progress.py` |

---

## Evidencia de vibecoding (prompts)

### Prompt 1: primera versión funcional

**Qué se pidió a la IA:** una primera versión jugable de "RoboAventura": un nivel con plataformas, seis baterías, un enemigo que patrulla, dos huecos y un portal. Incluye gravedad, colisiones, una cámara que sigue al jugador, un contador, pantallas de victoria y derrota, y reinicio con R.

**Por qué se escribió así:** el prompt usa una estructura de **rol, contexto, objetivo, requisitos, límites y formato de respuesta**. Los límites de alcance (sin doble salto, menú, sonidos ni más niveles) y las reglas concretas (tamaño de ventana, número de plataformas, la cámara no muestra fuera del nivel) evitan que la IA invente funciones de más. Así el resultado es pequeño, comprensible y fácil de verificar. Las mejoras se dejaron a propósito para los prompts siguientes.

<details>
<summary>Texto completo del prompt 1</summary>

```
ROL
Actúa como desarrollador de videojuegos en Python y tutor de un estudiante principiante. Prioriza un código claro que pueda comprender y explicar.
CONTEXTO
Estoy realizando una actividad individual de vibecoding. Necesito crear un mini-juego funcional, mejorarlo mediante prompts posteriores y documentar cómo lo probé.
OBJETIVO
Desarrolla "RoboAventura", un juego arcade de plataformas en 2D inspirado en los saltos y la exploración de Mario y Astro Bot, con un robot y un escenario originales.
El jugador debe recoger baterías, evitar peligros y llegar a un portal.
REQUISITOS FUNCIONALES
* Utiliza Python 3 y Pygame.
* Permite moverse con A/D o las flechas y saltar con espacio.
* Implementa gravedad y colisiones con suelo y plataformas.
* Incluye una cámara horizontal que siga al personaje.
* Muestra un contador de baterías recogidas.
* Al tocar al enemigo o caer en un hueco, termina la partida.
* Permite reiniciar con R después de perder o ganar.
* Al llegar al portal, muestra una pantalla de victoria y la cantidad de baterías recogidas.
* Permite cerrar el juego con Escape o con el botón de cierre de la ventana.
LÍMITES DE ALCANCE
* Desarrolla únicamente un juego en 2D para un jugador.
* Incluye un solo nivel, diseñado para completarse aproximadamente en uno a tres minutos.
* Incluye entre seis y diez plataformas, seis baterías, un enemigo que patrulle, dos huecos y un portal de salida.
* El personaje solamente puede caminar y realizar un salto simple.
* No agregues doble salto, combate, disparos, jefes, inventarios, tiendas, poderes ni niveles adicionales.
* No incluyas multijugador, conexión a internet, cuentas de usuario, bases de datos ni guardado de partidas.
* No agregues todavía menú inicial, pausa, sonidos ni animaciones complejas. Esas mejoras se solicitarán en otro prompt.
* No amplíes el alcance por iniciativa propia.
LÍMITES DEL ESCENARIO Y LAS REGLAS
* Utiliza una ventana de 960 × 600 píxeles y un escenario de 2880 píxeles de ancho.
* Impide que el personaje salga por los extremos izquierdo y derecho del escenario.
* Limita la cámara para que nunca muestre espacio fuera del nivel.
* Si el personaje cae por debajo del escenario, activa la derrota.
* No permitas saltar nuevamente mientras esté en el aire.
* Cada batería debe contarse una sola vez.
* El enemigo debe permanecer dentro de su zona de patrulla.
* Coloca las plataformas a distancias y alturas alcanzables con el salto implementado.
* Al terminar la partida, detén la interacción del juego hasta reiniciar o salir.
* Reiniciar debe restaurar la posición del jugador, el enemigo, las baterías y el contador.
LÍMITES TÉCNICOS Y VISUALES
* Usa únicamente Pygame y módulos de la biblioteca estándar de Python.
* Dibuja los elementos con figuras geométricas y colores. No utilices archivos externos de imágenes, fuentes, música o sonidos.
* No copies personajes, nombres, escenarios ni recursos de Mario o Astro Bot.
* Mantén el código del juego en un único archivo main.py y declara Pygame en requirements.txt.
* Utiliza funciones o clases pequeñas, nombres claros y comentarios útiles en español.
* Evita arquitecturas avanzadas y código innecesario para este alcance.
FORMATO DE RESPUESTA
1. Resume el funcionamiento y el alcance de esta primera versión.
2. Entrega main.py y requirements.txt completos, sin fragmentos pendientes.
3. Explica cómo instalar las dependencias y ejecutar el juego.
4. Explica brevemente el movimiento, la gravedad, las colisiones y la cámara.
5. Proporciona pruebas manuales para verificar las reglas y los límites.
6. Indica las limitaciones conocidas y distingue las pruebas realizadas de las pendientes.
Genera únicamente esta primera versión funcional. Espera un nuevo prompt antes de incorporar mejoras.
```

</details>

### Prompt 2: más dificultad y un ataque

**Qué se pidió a la IA:** que mejorara el nivel existente, sin rehacerlo. Pasar de uno a tres enemigos, repartidos y algo más rápidos; mover plataformas y baterías para exigir más precisión; y agregar un pulso de energía con la tecla J, con reglas exactas (espera de 0,6 s, máximo 2 pulsos activos, alcance de 350 px, desaparece al chocar).

**Por qué se refinó el prompt así:**
- Se pidió **revisar el código actual y conservar lo que ya funciona**, para que la IA no reescribiera todo y se pudiera ver qué cambió.
- Los números concretos del ataque (espera, cantidad y alcance) evitan que el ataque haga el juego demasiado fácil.
- Las reglas de equilibrio (sin invulnerabilidad, nada de saltos imposibles, ningún enemigo en la aparición, el portal sigue siendo la victoria) evitan que "más difícil" se convierta en "injusto".
- Se repitieron los límites de alcance (sin jefes, armas extra, menús ni sonidos) para mantener el proyecto pequeño.

<details>
<summary>Texto completo del prompt 2</summary>

```
ROL
Continúa como desarrollador de videojuegos en Python y tutor del proyecto RoboAventura.
CONTEXTO
Ya tengo una primera versión del juego. Ahora quiero aumentar su dificultad e incorporar una habilidad de ataque. Revisa el código actual antes de modificarlo y conserva las funciones que ya funcionan.
OBJETIVO
Mejora el nivel existente agregando más enemigos y un pulso de energía que permita al robot defenderse.
REQUISITOS DE DIFICULTAD
* Mantén un único nivel y las dimensiones actuales.
* Aumenta de uno a tres enemigos y distribúyelos a lo largo del recorrido.
* Haz que patrullen sin caer de las plataformas ni salir de su zona.
* Aumenta moderadamente la velocidad de los enemigos respecto a la versión anterior.
* Ajusta la ubicación de algunas plataformas y baterías para exigir mayor precisión, manteniendo todos los saltos alcanzables.
* Evita colocar enemigos o peligros sobre el punto de aparición del jugador.
HABILIDAD DE ATAQUE
* Permite lanzar un pulso de energía con J.
* El pulso debe viajar horizontalmente hacia el lado que el personaje esté mirando.
* Cada pulso elimina a un solo enemigo al impactarlo y desaparece.
* Establece un tiempo de espera de 0,6 segundos entre ataques.
* Permite un máximo de dos pulsos activos simultáneamente.
* Limita su alcance a 350 píxeles desde el punto de lanzamiento.
* Elimina el pulso al alcanzar su distancia máxima, golpear una plataforma sólida o salir del escenario.
* Representa el ataque mediante figuras y colores dibujados con Pygame.
REGLAS Y EQUILIBRIO
* Mantén la derrota inmediata al tocar un enemigo o caer en un hueco.
* El ataque no debe otorgar invulnerabilidad.
* Permite atacar tanto desde el suelo como durante un salto.
* Llegar al portal sigue siendo la condición de victoria; eliminar a todos los enemigos es opcional.
* Muestra en pantalla el control de ataque y una indicación sencilla de cuándo está disponible.
* Después de ganar o perder, bloquea los ataques.
* Al reiniciar, restaura los tres enemigos y elimina todos los pulsos y tiempos de espera de la partida anterior.
LÍMITES
* No agregues niveles, jefes, armas adicionales, mejoras de armas, inventario, doble salto ni multijugador.
* No incorpores todavía menús nuevos, pausa, sonidos ni recursos externos.
* Mantén Python, Pygame y los archivos existentes.
* Evita reorganizar todo el proyecto o añadir complejidad innecesaria.
* Si encuentras un error previo que impida implementar esta mejora, explica la corrección necesaria.
* No aumentes la dificultad mediante saltos imposibles o situaciones inevitables de derrota.
FORMATO DE RESPUESTA
1. Resume los cambios respecto a la primera versión.
2. Entrega los archivos modificados completos.
3. Explica cómo funcionan la dirección del ataque, el tiempo de espera, el alcance y las colisiones de los pulsos.
4. Proporciona pruebas manuales para comprobar:
   * Ataques hacia ambos lados y durante el salto.
   * Tiempo de espera y máximo de pulsos activos.
   * Impactos contra enemigos y plataformas.
   * Eliminación de pulsos al alcanzar su límite.
   * Reinicio completo después de ganar o perder.
   * Posibilidad de completar el nivel.
5. Distingue las pruebas ejecutadas de las pendientes y señala las limitaciones conocidas.
Realiza únicamente esta segunda iteración y espera nuevas instrucciones antes de añadir otras funciones.
```

</details>

**Cambios respecto a la versión 1:**

| Elemento | Versión 1 | Versión 2 |
|---|---|---|
| Enemigos | 1, en el suelo (1300–1650) | 3: suelo del tramo 1 (430–690), encima de la plataforma 5 (1380–1620) y suelo del tramo 3 (2050–2500) |
| Velocidad de los enemigos | 2 px/cuadro | 3 px/cuadro |
| Plataforma 2 | (520, 360), 120 de ancho | (520, 340), 110 de ancho |
| Plataforma 4 | (1150, 350), 140 de ancho | (1110, 330), 110 de ancho |
| Plataforma 5 | (1400, 430), 160 de ancho | (1380, 430), 240 de ancho, con enemigo encima |
| Plataforma 7 | (2200, 350), 140 de ancho | (2160, 330), 110 de ancho |
| Baterías | fáciles de alcanzar | una exige saltar encima de la plataforma 2, otra está junto a un enemigo y dos están sobre los huecos |
| Ataque | — | pulso con J: espera de 0,6 s, máximo 2 activos, alcance de 350 px |

### Prompt 3: arena y batalla contra un jefe

**Qué se pidió a la IA:**
- Un sistema de **tres corazones** con 1,2 s de invulnerabilidad y parpadeo. Las caídas restan un corazón y devuelven al robot a un lugar seguro.
- Que el portal lleve a una **arena** donde hay que vencer a un **jefe original con 12 de vida**. El jefe se mueve, avisa antes de atacar, alterna dos patrones (ráfaga apuntada y proyectiles bajos) y tiene una segunda fase.

**Por qué se refinó el prompt así:**
- Se dijo de forma explícita que **dos reglas anteriores se reemplazan** (tocar un enemigo ya no es derrota inmediata y el portal ya no es victoria). Así la IA no queda con instrucciones contradictorias de los prompts anteriores.
- Los **estados del jefe** (aviso, ataque y descanso), los tiempos mínimos (aviso de 0,6 s y descanso de 1 s) y el orden fijo de los patrones hacen que el combate sea difícil pero predecible y justo.
- Se pidieron reglas para casos límite: que un proyectil dañe una sola vez, un máximo de 12 proyectiles, prioridad de la victoria si ambos llegan a 0 a la vez, y un reinicio completo. Son los errores típicos de un combate con jefe.
- Se pidió inspirarse en los **patrones** de Cuphead, pero con diseño y recursos originales.

<details>
<summary>Texto completo del prompt 3</summary>

```
ROL
Continúa como desarrollador de videojuegos en Python y tutor del proyecto RoboAventura.
CONTEXTO
El juego ya tiene plataformas, enemigos y un ataque de energía. Quiero agregar una batalla contra un jefe inspirada en los patrones de ataque de Cuphead, con diseño y recursos originales.
Esta iteración reemplaza dos reglas anteriores: tocar un enemigo ya no provoca derrota inmediata y llegar al portal ya no significa ganar.
OBJETIVO
Al atravesar el portal, lleva al jugador a una arena donde deba vencer a un jefe que se mueva, alterne ataques y tenga una barra de vida. El personaje debe soportar tres impactos antes de perder.
VIDAS DEL PERSONAJE
* Representa la salud mediante tres corazones visibles. Cada corazón equivale a un punto de vida.
* Tocar un enemigo, al jefe o uno de sus proyectiles resta un corazón.
* Después de recibir daño, concede 1,2 segundos de invulnerabilidad y haz parpadear al personaje.
* Durante ese intervalo, ningún contacto adicional debe quitar vida.
* Caer en un hueco resta un corazón y devuelve al personaje a una posición segura, sin provocar daños repetidos por la misma caída.
* Al llegar a cero corazones, muestra la derrota.
* Al entrar por primera vez a la arena, recupera los tres corazones para comenzar el combate en condiciones justas.
TRANSICIÓN POR EL PORTAL
* Conserva el nivel de plataformas existente.
* Al tocar el portal, cambia a una arena fija del tamaño de la ventana, sin desplazamiento de cámara.
* Limpia los enemigos y proyectiles del escenario anterior.
* Coloca al jugador y al jefe en extremos separados.
* La arena debe tener suelo continuo, límites laterales y espacio suficiente para esquivar.
* El portal no debe permitir regresar ni recuperar vida repetidamente.
* La victoria se obtiene únicamente al derrotar al jefe.
COMPORTAMIENTO DEL JEFE
* Crea un robot jefe original con doce puntos de vida.
* Muestra una barra de vida con su nombre y el valor actual sobre el máximo.
* Cada pulso del jugador que impacte al jefe resta un punto y desaparece.
* El jefe debe desplazarse horizontalmente dentro de una zona delimitada.
* Organiza su comportamiento mediante estados claros: aviso, ataque y descanso.
* Antes de cada ataque, muestra una señal visual durante al menos 0,6 segundos.
* Alterna estos patrones en un orden predecible:
   1. Ráfaga: dispara tres proyectiles consecutivos hacia la posición que tenía el jugador al iniciar cada disparo. Los proyectiles no persiguen al jugador.
   2. Salto de proyectiles: lanza una secuencia de tres proyectiles bajos, separados lo suficiente para que el jugador pueda saltarlos.
* Incluye al menos un segundo de descanso entre patrones para permitir contraatacar.
* Al quedar con seis puntos de vida o menos, activa una segunda fase: cambia su color y reduce moderadamente el descanso, sin eliminar los avisos ni volver inevitables los ataques.
* Ajusta posiciones y distancias para que el ataque actual del jugador pueda alcanzar al jefe.
REGLAS DEL COMBATE
* Conserva J para atacar, el tiempo de espera de 0,6 segundos, el alcance de 350 píxeles y el máximo de dos pulsos activos.
* Los proyectiles del jefe desaparecen al impactar al jugador o salir de la arena.
* Un proyectil solo puede causar daño una vez.
* Limita a doce los proyectiles enemigos activos.
* Al morir el jefe, elimina sus proyectiles, detén el daño y muestra la victoria.
* Si jugador y jefe llegan a cero vida en la misma actualización, da prioridad a la victoria.
* R después de ganar o perder debe reiniciar toda la aventura, restaurando corazones, enemigos, jefe, temporizadores y proyectiles.
LÍMITES
* Agrega únicamente una arena y un jefe con dos patrones y dos fases.
* No incorpores armas nuevas, inventario, mejoras, niveles adicionales ni multijugador.
* Mantén Python y Pygame, sin nuevas dependencias ni recursos externos.
* Dibuja personajes, efectos y barras con figuras geométricas.
* Conserva los controles actuales y evita cambios ajenos a esta iteración.
* No copies personajes, música ni imágenes de Cuphead.
FORMATO DE RESPUESTA
1. Resume las reglas que cambian.
2. Entrega los archivos modificados completos.
3. Explica el sistema de corazones, la invulnerabilidad, los estados del jefe y sus patrones.
4. Incluye pruebas manuales de daño, caída, transición, ataques, segunda fase, victoria, derrota y reinicio.
5. Distingue las pruebas realizadas de las pendientes e identifica las limitaciones conocidas.
Implementa únicamente esta iteración y espera nuevas instrucciones antes de ampliar el juego.
```

</details>

**Reglas que cambian respecto a la versión 2:**

| Regla | Versión 2 | Versión 3 |
|---|---|---|
| Tocar un enemigo | Derrota inmediata | Resta 1 corazón y da 1,2 s de invulnerabilidad |
| Caer en un hueco | Derrota inmediata | Resta 1 corazón y regresa al último lugar seguro |
| Derrota | Un solo error | Quedarse sin los 3 corazones |
| Portal | Victoria | Lleva a la arena del jefe (una sola vez) y recupera los 3 corazones |
| Victoria | Llegar al portal | Vencer a VOLTARÓN (12 de vida) |
| R | Reinicia el nivel | Reinicia toda la aventura (nivel, corazones, enemigos, jefe, tiempos y proyectiles) |


### Prompt 4: menús con botones, pausa y ajustes del combate

**Qué se pidió a la IA:**
- Una interfaz con **botones y ratón**: pantalla inicial, botón Pausa (con Continuar, Reiniciar y Salir) y Volver a jugar / Salir al terminar.
- Una **pausa real**, que congela también la espera del ataque y la invulnerabilidad.
- Un **ataque más rápido**: 0,3 s de espera y J mantenida.
- **Ajustes del jefe:** descanso de 1,2 s en la fase 1; en la fase 2, +20 % de velocidad, descanso de 0,8 s y el anuncio "Fase 2".
- **Quitar R y Escape.**

**Por qué se refinó el prompt así:**
- **Se corrigió el CONTEXTO antes de enviarlo.** La primera redacción decía "Quiero incorporar una batalla contra un jefe… tres corazones", como si no existieran. La IA señaló que eso ya estaba hecho desde el Prompt 3 y que la redacción podía llevar a reescribir todo. Se cambió a "El juego ya tiene… corazones y un jefe de dos fases. Ahora quiero agregar menús… Revisa el código actual y conserva lo que ya funciona". Así quedó claro que era una iteración y no una versión nueva desde cero.
- Se repitieron a propósito las reglas ya existentes (corazones, portal y arena, jefe). Así funcionan como **lista de verificación**: la IA debe confirmar que siguen funcionando después de los cambios.
- Se pidieron detalles de interfaz que suelen fallar: que un clic haga una sola acción, que no se active un botón de la pantalla siguiente, y que la pausa no consuma tiempos.
- **Este prompt reemplaza una regla del Prompt 3:** el descanso de la fase 2 baja a 0,8 s, aunque antes se pedía "al menos un segundo". Se compensa manteniendo los avisos de 0,75 s.

<details>
<summary>Texto completo del prompt 4 (con el contexto ya corregido)</summary>

```
ROL
Continúa como desarrollador de videojuegos en Python y tutor del proyecto RoboAventura.
CONTEXTO
El juego ya tiene plataformas, enemigos, ataque de energía, corazones y un jefe de dos fases. Ahora quiero agregar menús con botones, una pausa real, un ataque más rápido y ajustar los tiempos de las fases. Revisa el código actual y conserva lo que ya funciona.
OBJETIVO
Completa esta versión con una interfaz controlada mediante clics, un combate contra un jefe de dos fases y un ataque del jugador más rápido.
BOTONES E INTERFAZ
* Al abrir el juego, muestra una pantalla inicial con el título y los botones "Iniciar" y "Salir".
* "Iniciar" comienza una partida nueva con tres corazones.
* Durante la partida, muestra un botón "Pausa".
* Al pausarla, detén movimientos, proyectiles, daño y temporizadores. Muestra los botones "Continuar", "Reiniciar" y "Salir".
* "Continuar" reanuda la partida sin consumir durante la pausa los tiempos de espera o de invulnerabilidad.
* Después de ganar o perder, muestra los botones "Volver a jugar" y "Salir".
* "Reiniciar" y "Volver a jugar" restauran toda la aventura.
* Todos los botones deben funcionar con el botón izquierdo del ratón, tener texto legible y cambiar de aspecto al pasar el cursor.
* Un clic debe provocar una sola acción y no activar accidentalmente botones de la pantalla siguiente.
* "Salir" debe cerrar correctamente el juego desde cualquier menú.
* Elimina la dependencia de R y Escape para reiniciar o salir.
* Conserva A/D o las flechas para moverse, espacio para saltar y J para atacar. Muestra estos controles en la pantalla inicial.
* Mantén operativo el botón de cierre de la ventana.
VIDAS DEL JUGADOR
* Muestra tres corazones. Cada impacto de un enemigo, del jefe o de un proyectil resta uno.
* Después de recibir daño, concede 1,2 segundos de invulnerabilidad y haz parpadear al personaje.
* Caer en un hueco resta un corazón y devuelve al jugador a una posición segura.
* Evita descontar varios corazones por un mismo impacto o caída.
* Al llegar a cero, muestra la derrota y sus botones.
ATAQUE DEL JUGADOR
* Reduce el tiempo mínimo entre ataques de 0,6 a 0,3 segundos.
* Permite mantener J presionada para atacar repetidamente, respetando ese intervalo.
* Conserva un máximo de dos pulsos activos y un alcance de 350 píxeles.
* Cada pulso viaja hacia el lado que mira el personaje, causa un punto de daño y desaparece al impactar.
* Los pulsos también desaparecen al golpear superficies sólidas o alcanzar su límite.
* Permite atacar desde el suelo y durante un salto.
* No permitas atacar desde los menús, durante la pausa o después de terminar la partida.
PORTAL Y ARENA
* Conserva el nivel de plataformas.
* Al atravesar el portal, elimina los enemigos y proyectiles anteriores y entra a una arena fija con suelo continuo.
* Recupera los tres corazones una sola vez al entrar.
* Separa las posiciones iniciales del jugador y del jefe.
* Impide regresar por el portal para recuperar vida.
* La victoria se obtiene al derrotar al jefe.
JEFE Y FASES
* Crea un robot jefe original con doce puntos de vida y una barra visible.
* Haz que se mueva horizontalmente dentro de límites definidos.
* Organiza su comportamiento en aviso, ataque y descanso.
* Antes de cada patrón, muestra un aviso visual de al menos 0,6 segundos.
Fase 1: de doce a siete puntos de vida.
* Alterna una ráfaga de tres proyectiles dirigidos hacia la posición del jugador al disparar y una secuencia de tres proyectiles bajos que puedan esquivarse saltando.
* Los proyectiles no deben perseguir al jugador.
* Incluye 1,2 segundos de descanso entre patrones.
Fase 2: de seis a un punto de vida.
* Anuncia "Fase 2" brevemente y cambia el color del jefe.
* Aumenta un 20 % su velocidad de movimiento.
* Reduce el descanso entre patrones a 0,8 segundos.
* Conserva los avisos y ambos patrones, manteniendo oportunidades reales para esquivar y contraatacar.
* Activa la transición una sola vez.
REGLAS Y LÍMITES
* Limita a doce los proyectiles enemigos activos.
* Elimina los proyectiles enemigos al impactar al jugador o salir de la arena.
* Al morir el jefe, elimina sus ataques y detén el daño. Si ambos personajes llegan a cero en la misma actualización, da prioridad a la victoria.
* Reiniciar debe restaurar corazones, enemigos, jefe, fase, proyectiles y temporizadores.
* Mantén un nivel, una arena y un jefe con dos fases.
* No agregues armas, inventario, niveles, multijugador ni funciones ajenas a lo solicitado.
* Usa Python y Pygame, sin nuevas dependencias ni recursos externos.
* Dibuja los elementos mediante figuras geométricas originales.
FORMATO DE RESPUESTA
1. Resume los cambios.
2. Entrega los archivos modificados completos.
3. Explica los botones, la pausa, el intervalo de ataque y las fases del jefe.
4. Incluye pruebas manuales para verificar botones, pausa, daño, frecuencia de ataque, transición de fase y reinicio completo.
5. Distingue las pruebas ejecutadas de las pendientes y señala las limitaciones conocidas.
```

</details>

**Cambios respecto a la versión 3:**

| Elemento | Versión 3 | Versión 4 |
|---|---|---|
| Al abrir | Empieza a jugar | Pantalla inicial con título, controles e Iniciar / Salir |
| Reiniciar / salir | Teclas R y Escape | Botones (Reiniciar, Volver a jugar, Salir) y la X de la ventana |
| Pausa | No había | Botón Pausa: congela todo, incluidos los tiempos |
| Espera del ataque | 0,6 s, una pulsación por pulso | 0,3 s, y se puede mantener J |
| Descanso del jefe, fase 1 | 1,5 s | 1,2 s |
| Descanso del jefe, fase 2 | 1,1 s | 0,8 s |
| Velocidad del jefe, fase 2 | igual que en la fase 1 (2 px/cuadro) | +20 % (2,4 px/cuadro) |
| Cambio de fase | Solo color y texto en la barra | Además, el anuncio "FASE 2" durante 1,5 s; ocurre una sola vez |


### Prompt 5: apuntado con el ratón, agacharse y propulsor

**Qué se pidió a la IA:**
- **Apuntar con el ratón** en un rango de ±60° hacia cada lado, con mira y una línea de dirección.
- **Disparar con clic** (manteniendo, cada 0,3 s), en lugar de J.
- **Agacharse** con S para esquivar.
- Un **propulsor** con Shift para vuelos cortos, con barra de energía.
- Que el movimiento sea **independiente de los FPS**.

**Por qué se refinó el prompt así:**
- Se describió el **problema de jugabilidad** que motivaba el cambio ("disparar con J y apuntar solo en horizontal dificulta combatir y esquivar"), no solo la solución. Así la IA puede revisar si las nuevas habilidades de verdad sirven contra el jefe.
- Se detallaron los casos difíciles del apuntado, que suelen salir mal:
  - pasar el cursor de pantalla a coordenadas del mundo cuando hay cámara;
  - normalizar el vector;
  - que el eje Y crece hacia abajo;
  - reflejar el ángulo hacia la izquierda;
  - el cursor justo encima del arma.
- Se pidió que un clic en "Iniciar" o "Continuar" **no dispare**. Es un error típico al mezclar disparo con clic y botones con clic.
- Se pidió **no reconstruir el proyecto**: modificar el código actual.

<details>
<summary>Texto completo del prompt 5</summary>

```
ROL
Actúa como desarrollador de videojuegos en Python y especialista en controles de juegos de plataformas 2D.
CONTEXTO
Estoy desarrollando RoboAventura con Pygame. La versión actual tiene plataformas, tres corazones, un jefe con dos fases y menús con botones.
La jugabilidad necesita mejorar: disparar con J y apuntar únicamente en horizontal dificulta combatir y esquivar.
OBJETIVO
Modifica la versión existente para apuntar con el mouse, disparar con clic izquierdo, agacharse y realizar un vuelo corto. Conserva los menús, vidas, nivel y comportamiento del jefe.
APUNTADO VECTORIAL CON EL MOUSE
* Calcula un vector de dirección desde el arma del robot hacia el cursor.
* Convierte correctamente las coordenadas del cursor de pantalla a coordenadas del mundo cuando exista desplazamiento de cámara.
* Normaliza el vector para que la velocidad del proyectil sea constante, independientemente de la distancia al cursor.
* Permite apuntar desde −60° hasta +60° respecto a la horizontal del lado hacia el que se apunta: 0° horizontal, ángulos positivos hacia arriba y negativos hacia abajo.
* Refleja este rango al apuntar hacia la izquierda. Debe poder dispararse hacia ambos lados.
* Ten en cuenta que el eje Y de pantalla aumenta hacia abajo.
* Si el cursor queda fuera del rango permitido, limita el disparo al ángulo válido más cercano.
* La orientación del arma debe seguir al cursor, independientemente del movimiento: el robot puede caminar hacia la izquierda mientras dispara hacia la derecha.
* Si el cursor coincide con el origen del disparo, conserva la última dirección válida para evitar errores.
* Muestra una mira y una línea corta o indicador que represente la dirección real del disparo limitado.
DISPARO CON CLIC
* Sustituye J por el botón izquierdo del mouse.
* Mantener presionado el botón debe disparar cada 0,3 segundos.
* Conserva el alcance de 350 píxeles, el máximo de dos pulsos activos y un punto de daño por impacto.
* Mide el alcance mediante la distancia recorrida, también en disparos diagonales.
* Permite disparar caminando, saltando, agachado y volando.
* Ajusta el origen del disparo a la posición del arma en cada postura.
* Impide disparar al interactuar con botones o menús.
* Un clic en "Iniciar" o "Continuar" no debe producir un disparo: exige soltar el botón antes de comenzar a disparar.
AGACHARSE PARA ESQUIVAR
* Usa S o flecha abajo mientras el personaje esté apoyado en el suelo.
* Reduce aproximadamente a la mitad su altura y su zona de colisión, manteniendo los pies en la misma posición.
* Reduce su velocidad horizontal mientras esté agachado.
* La reducción de altura debe permitir esquivar proyectiles que antes impactaban en la parte superior del cuerpo.
* Al soltar la tecla, recupera su altura solamente si hay espacio libre encima.
* Evita que ponerse de pie introduzca al personaje dentro de una plataforma.
* No actives la postura agachada en el aire.
VUELO CORTO
* Agrega un propulsor activado al mantener Shift mientras el robot está en el aire.
* Conserva espacio para el salto normal.
* Mientras haya energía, el propulsor debe contrarrestar la gravedad y permitir ascender con una velocidad máxima controlada.
* Limita la energía a dos segundos de uso continuo.
* Al soltar Shift o agotarse la energía, vuelve a actuar la gravedad normal.
* Recarga completamente la energía en 1,5 segundos mientras esté apoyado en el suelo o una plataforma.
* Muestra una barra de energía.
* Impide atravesar techos, plataformas y límites del escenario durante el vuelo.
EQUILIBRIO Y LÍMITES
* Conserva los tres corazones y la invulnerabilidad temporal después de recibir daño.
* Mantén las dos fases y los patrones del jefe.
* Revisa que sus ataques puedan esquivarse con las nuevas habilidades y que el jugador pueda alcanzarlo con sus disparos.
* Mantén alcanzable el recorrido original mediante saltos normales; el vuelo será una ayuda adicional.
* Pausar debe congelar también el vuelo, su energía y todos los tiempos de espera.
* Reiniciar debe restaurar postura, energía, vida, proyectiles y estados del combate.
* No agregues armas, niveles, enemigos ni dependencias.
* No reconstruyas el proyecto desde cero: modifica el código actual.
FORMATO DE RESPUESTA
1. Resume los cambios y presenta los controles actualizados.
2. Entrega los archivos modificados completos.
3. Explica brevemente el vector de apuntado, el límite angular, la postura agachada y el propulsor.
4. Incluye pruebas de apuntado hacia ambos lados, disparos diagonales, movimiento independiente del apuntado, agacharse bajo obstáculos, agotamiento y recarga de energía, pausa y reinicio.
5. Distingue los resultados comprobados de los pendientes y señala cualquier limitación.
Prioriza controles fluidos y predecibles, con movimiento independiente de la velocidad de fotogramas.
```

</details>

**Cambios respecto a la versión 4:**

| Elemento | Versión 4 | Versión 5 |
|---|---|---|
| Disparo | J, siempre horizontal hacia donde camina | Clic izquierdo, hacia el cursor (±60°), sin importar hacia dónde camina |
| Pulso | Se mueve solo en X | Se mueve con un vector unitario; el alcance se mide por distancia recorrida |
| Postura | Solo de pie | Agachado con S: 24 px de alto (antes 48), velocidad 3 (antes 5) |
| Vuelo | No había | Propulsor con Shift en el aire: 2 s de energía, recarga en 1,5 s |
| HUD | Corazones e indicador de J | Además, barra del propulsor, mira y línea de apuntado |
| Ráfaga del jefe | Apuntaba al centro del robot | Apunta al pecho (borde superior + 10 px), para que agacharse sirva para esquivarla |
| Bucle principal | Una actualización por cuadro | Paso fijo de 1/60 s: misma velocidad a cualquier FPS |


### Prompt 6: arquitectura modular, NEXO-7 y Centinela Eclipse

**Qué se pidió a la IA:**
- Pasar de un único `main.py` a **módulos con responsabilidades claras**, sin datos duplicados ni dependencias circulares.
- Cambiar la identidad a **NEXO-7** en una estación abandonada.
- Acortar el propulsor a **0,8 s**.
- Permitir apuntar en **360° en el aire**.
- Convertir al jefe en el **Centinela Eclipse**: fase 1 con 40 de vida, una transición única y fase 2 con 60 de vida y dos patrones nuevos.

**Por qué se refinó el prompt así:**
- Se dijo de forma explícita que esta solicitud **autoriza** reemplazar el archivo único y cambiar límites anteriores (propulsor, apuntado y vida del jefe). Así la IA no queda dividida entre reglas viejas y nuevas.
- Se pidió **primero reorganizar sin cambiar el comportamiento y después cambiar la jugabilidad**. Por eso hay dos commits: la reorganización se verificó con las 136 pruebas de la versión 5 antes de tocar el combate.
- Se pidió definir **quién guarda cada dato** y evitar crear recursos en cada cuadro. Son los errores típicos al separar un programa en archivos.
- Para el jefe se fijaron reglas para casos límite que suelen fallar:
  - la recarga de vida ocurre **una sola vez**;
  - durante la transición se suspende el daño de **ambos**;
  - cuando hay 12 proyectiles, la emisión **espera** en lugar de perderse.
- Se pidió **no inventar NPCs**, solo explicar dónde irían.

<details>
<summary>Texto completo del prompt 6</summary>

```
ROL
Actúa como desarrollador de videojuegos en Python y tutor. Ayúdame a mejorar la arquitectura y la jugabilidad del proyecto existente, manteniendo un código comprensible para un estudiante.
CONTEXTO
Estoy desarrollando RoboAventura con Pygame. Actualmente tiene plataformas, enemigos, botones de menú, tres corazones, apuntado con mouse, disparo con clic, postura agachada, propulsor y una batalla contra un jefe.
Quiero reorganizar el código en módulos y mejorar el combate. Esta solicitud autoriza reemplazar la estructura de un único archivo y modificar los límites anteriores del propulsor, el apuntado y la vida del jefe.
OBJETIVO
Transforma el proyecto en una versión modular protagonizada por NEXO-7, un robot explorador que recorre una estación tecnológica abandonada y se enfrenta al "Centinela Eclipse", su sistema de defensa.
1. ESTRUCTURA MODULAR
Utiliza esta organización como referencia:
main.py
config.py
game.py
entities/
robot.py
enemies.py
boss.py
projectiles.py
systems/
movement.py
collisions.py
world/
level.py
theme.py
ui/
menus.py
hud.py
requirements.txt
README.md
Responsabilidades:
* main.py: inicializar y ejecutar el juego. Debe ser un punto de entrada pequeño.
* config.py: controles, dimensiones y parámetros ajustables de dificultad.
* game.py: coordinar el bucle principal y los estados de menú, nivel, arena, pausa, victoria y derrota.
* robot.py: estado y acciones específicas de NEXO-7, como salud, postura, energía y ataque.
* enemies.py: comportamiento de los enemigos comunes. Separa sus tipos mediante funciones o clases sencillas cuando lo necesiten.
* boss.py: vida, movimiento, fases y patrones del jefe.
* projectiles.py: movimiento, alcance, daño y eliminación de proyectiles.
* movement.py: cálculos de desplazamiento, gravedad, salto y propulsión.
* collisions.py: detección y resolución de colisiones compartidas.
* level.py: distribución del escenario, plataformas, enemigos y portal.
* theme.py: colores, fondos y características visuales de la ambientación.
* menus.py: botones e interacción de los menús.
* hud.py: corazones, energía, fase y barra de vida del jefe.
Usa funciones, módulos y clases sencillas cuando ayuden. No impongas herencia compleja ni patrones avanzados.
Define con claridad quién guarda cada estado para evitar datos duplicados. Evita dependencias circulares y la creación repetida de recursos en cada fotograma.
Si ya existen NPCs, separa su comportamiento en entities/npcs.py. Si no existen, explica dónde se incorporarían posteriormente, sin inventar personajes, diálogos o misiones en esta iteración.
2. IDENTIDAD Y AMBIENTACIÓN
* Cambia el nombre del personaje a NEXO-7 en la interfaz y la documentación.
* Mantén una ambientación coherente de estación tecnológica abandonada, con plataformas metálicas, baterías y un núcleo de energía.
* Distingue visualmente al jugador, enemigos, proyectiles aliados y proyectiles hostiles.
* Utiliza figuras geométricas originales y recursos generados con Pygame.
* Centraliza las decisiones visuales para poder cambiar la ambientación sin modificar la lógica del combate.
3. PROPULSOR BREVE
* Reduce su capacidad de dos segundos a 0,8 segundos de uso continuo.
* Permite activarlo con Shift mientras el personaje esté en el aire.
* Conserva el salto normal.
* Al soltar Shift o agotarse la energía, aplica nuevamente la gravedad normal.
* Recarga completamente la energía en 1,5 segundos de contacto continuo con suelo o plataformas.
* No recargues energía en el aire.
* Conserva la barra de energía y las colisiones con techos y plataformas.
* Debe servir para corregir saltos y esquivar, sin permitir vuelo permanente.
4. APUNTADO Y DISPARO EN EL AIRE
* Conserva el apuntado vectorial con el mouse y el disparo con clic izquierdo.
* En el suelo, conserva el rango de ±60° respecto a la horizontal del lado al que se apunta.
* Mientras NEXO-7 esté en el aire, permite apuntar en 360°, incluso hacia abajo.
* Esta libertad debe mantenerse durante el salto, la caída y el uso del propulsor.
* Permite moverse y apuntar en direcciones independientes.
* Al aterrizar, vuelve a aplicar el límite angular del suelo.
* La mira debe mostrar la dirección real del disparo.
* Conserva el intervalo de 0,3 segundos, el alcance de 350 píxeles y el máximo de dos pulsos activos.
* Mantén una velocidad constante de los proyectiles en todas las direcciones.
* No permitas que los clics sobre botones produzcan disparos.
5. JEFE CON DOS FASES COMPLETAS
Primera fase:
* El Centinela Eclipse comienza con 40 puntos de vida.
* Alterna ráfagas dirigidas hacia posiciones concretas del jugador y proyectiles bajos que puedan saltarse.
* Incluye avisos visuales de al menos 0,6 segundos y descansos de 1,2 segundos entre patrones.
Transición:
* Al agotar los 40 puntos, inicia una transición única de 1,5 segundos.
* Limpia los proyectiles hostiles y muestra "Fase 2: Sobrecarga".
* Durante la transición, suspende los ataques y el daño de ambos personajes, pero permite que el jugador se reposicione.
* Cambia la apariencia del jefe y recarga su barra con un nuevo máximo de 60 puntos.
* Esta recarga ocurre una sola vez. No es regeneración continua ni debe repetirse al recibir daño.
Segunda fase:
* Aumenta un 25 % la velocidad de movimiento del jefe.
* Reduce los descansos entre patrones a 0,8 segundos.
* Alterna dos patrones diferentes de los anteriores:
a. Abanico de cinco proyectiles con separaciones que permitan esquivarlos.
b. Tres ráfagas cortas dirigidas hacia la posición del jugador al comenzar cada ráfaga.
* Los proyectiles dirigidos no deben perseguir al jugador después de lanzarse.
* Conserva avisos visuales de al menos 0,5 segundos.
* Ajusta los ataques para que puedan esquivarse tanto desde el suelo como utilizando el propulsor.
* Al agotar los 60 puntos de esta fase, termina el combate con victoria.
Muestra siempre la fase actual y la vida correspondiente. Cada impacto del jugador resta un punto. Mantén un máximo de doce proyectiles hostiles activos y retrasa nuevas emisiones si se alcanza ese límite.
6. REGLAS QUE DEBEN CONSERVARSE
* Tres corazones e invulnerabilidad de 1,2 segundos después de recibir daño.
* Agacharse con una zona de colisión reducida.
* Menús y botones para iniciar, pausar, continuar, reiniciar y salir.
* Portal que conduce a la arena y recupera los corazones una sola vez al entrar.
* Pausa que congela todos los movimientos y temporizadores.
* Reinicio completo del nivel, vida, energía, jefe, fases y proyectiles.
* Un nivel, una arena y un jefe. No agregues armas, inventarios, multijugador ni dependencias.
7. DOCUMENTACIÓN Y ENTREGA
Antes del código, presenta brevemente:
* El árbol definitivo de archivos y sus responsabilidades.
* El modelo de funcionamiento: estados del juego, datos de cada entidad y transiciones entre fases.
* Las especificaciones de ambientación y los parámetros de dificultad elegidos.
Después:
* Entrega todos los archivos necesarios completos, identificados por su ruta.
* Actualiza el README con instalación, ejecución, controles y explicación de la estructura.
* Indica dónde modificar posteriormente movilidad, enemigos, jefe y ambientación.
* Verifica que el proyecto se ejecute desde main.py sin errores de importación.
* Comprueba especialmente el reinicio de fases, la recarga única del jefe y el cambio de apuntado al despegar y aterrizar.
* Distingue las pruebas ejecutadas de las pendientes y documenta las limitaciones reales.
Realiza la reorganización conservando el comportamiento existente, y después incorpora los cambios de jugabilidad. Evita reescribir funciones que ya funcionan si no es necesario.
```

</details>

**Cambios respecto a la versión 5:**

| Elemento | Versión 5 | Versión 6 |
|---|---|---|
| Código | Un solo `main.py` (1109 líneas) | 13 módulos (ver "Estructura del proyecto") |
| Protagonista | "el robot" | NEXO-7 (nombre en el HUD, el título y los mensajes) |
| Ambientación | Ciudad nocturna | Estación abandonada y cámara del núcleo de energía |
| Propulsor | 2 s | 0,8 s (720 unidades: gasta 15 por paso y recarga 8) |
| Apuntado | ±60° siempre | ±60° en el suelo; 360° en el aire |
| Jefe | VOLTARÓN, 12 de vida; fase 2 con 6 o menos | Centinela Eclipse: fase 1 con 40, transición de 1,5 s, fase 2 con 60 |
| Patrones de la fase 2 | Los mismos de la fase 1 | Abanico de 5 y tres ráfagas cortas |
| Límite de 12 proyectiles | El disparo se perdía | La emisión espera hasta que haya lugar |
| Pulsos y disparos del jefe | Dos clases (`Pulso`, `Proyectil`) | Una sola clase `Proyectil` (aliado u hostil) |


### Prompt 7: cambio de concepto a "NEXO-7: Arena Eclipse"

**Qué se pidió a la IA:**
- Convertir el juego en **combates contra jefes**: quitar el nivel de plataformas, las baterías y el portal.
- Agregar una pantalla de **selección de jefe** con desbloqueos en orden, guardados en un **JSON local**.
- Darle a NEXO-7 **4 corazones**.
- Crear **tres jefes** distintos, cada uno en su propio módulo, con dificultad creciente.

**Por qué se refinó el prompt así:**
- Se dijo de forma explícita que el prompt **reemplaza** reglas anteriores (3 corazones, un solo jefe), igual que en los prompts 3 y 6, para evitar contradicciones.
- Cada jefe tiene un **propósito de diseño** ("enseñar a leer avisos", "combinar salto y agacharse", "apuntar en varias direcciones") y se pidió **no subir la dificultad solo con más vida**. Así la IA diseña patrones diferentes en lugar de copiar al mismo jefe con más vida.
- Se pidió qué hacer si el **archivo de guardado está dañado**. Si no se piensa, es un error que cierra el juego.
- "Prioriza primero un combate completo; después los otros dos" llevó a trabajar en **dos commits**:
  - **Etapa A:** el flujo completo con el Jefe 1, ya probado.
  - **Etapa B:** los jefes 2 y 3, con la misma estructura y las mismas pruebas genéricas.

<details>
<summary>Texto completo del prompt 7</summary>

```
ROL
Actúa como desarrollador de videojuegos en Python y tutor. Modifica el proyecto existente con una estructura modular y código comprensible.
CAMBIO DE CONCEPTO
Transforma RoboAventura en "NEXO-7: Arena Eclipse", un juego centrado exclusivamente en combates contra jefes.
Elimina del recorrido jugable la sección de plataformas, la recolección de baterías y el portal. Desde el menú, el jugador debe seleccionar un jefe desbloqueado y entrar directamente a su arena.
Esta solicitud reemplaza las reglas anteriores de tres corazones y un único jefe.
OBJETIVO
Implementa tres jefes originales con dificultad creciente, movimientos y patrones diferentes. El jugador debe vencerlos en orden para desbloquear el siguiente.
PROGRESIÓN Y DIFICULTAD
* Al comenzar por primera vez, solamente está disponible el primer jefe.
* Vencer al primero desbloquea al segundo.
* Vencer al segundo desbloquea al tercero.
* Vencer al tercero muestra una pantalla de campaña completada.
* Permite volver a combatir contra cualquier jefe desbloqueado.
* Perder no elimina los desbloqueos.
* La dificultad aumenta entre encuentros; no agregues todavía un selector adicional de modos fácil, normal y difícil.
* Guarda únicamente los desbloqueos y las victorias en un archivo JSON local.
* Si el archivo no existe, inicia una progresión nueva. Si está dañado, evita que el juego se cierre e informa que se ha restablecido el progreso.
* No utilices cuentas, internet ni bases de datos.
SALUD DEL JUGADOR
* NEXO-7 tiene cuatro corazones.
* Cada impacto resta un corazón.
* Conserva 1,2 segundos de invulnerabilidad después del daño.
* Comienza cada combate o reintento con cuatro corazones y energía completa.
* La transición de fase del jefe no recupera los corazones del jugador.
* Al perder, permite reintentar el jefe actual o regresar a la selección.
JEFE 1: CENTINELA ECLIPSE
Dificultad inicial. Su función es enseñar a reconocer avisos y esquivar.
* Permanece en el suelo y patrulla lentamente.
* Fase 1: 24 puntos de vida.
* Alterna proyectiles bajos que puedan saltarse y ráfagas dirigidas hacia la posición del jugador.
* Utiliza avisos de 0,8 segundos y descansos de 1,4 segundos.
* Fase 2: recarga una nueva barra de 32 puntos.
* Aumenta moderadamente la frecuencia de disparo e incorpora una ráfaga adicional, conservando oportunidades claras para contraatacar.
JEFE 2: EMBESTIDOR FÉRREO
Dificultad intermedia. Exige combinar desplazamiento, salto y postura agachada.
* Se desplaza más rápido que el primer jefe.
* Fase 1: 36 puntos de vida.
* Alterna embestidas horizontales anunciadas y abanicos de proyectiles con espacios seguros.
* Antes de embestir, señala su dirección y permite saltar por encima.
* Fase 2: recarga una nueva barra de 48 puntos.
* Combina una embestida con una ráfaga posterior, separadas por un aviso que permita reaccionar.
* Utiliza avisos de al menos 0,6 segundos y descansos de un segundo entre secuencias.
JEFE 3: SERAFÍN VOLTAICO
Dificultad avanzada. Exige apuntar en varias direcciones y aprovechar el propulsor.
* Vuela entre posiciones delimitadas de la arena.
* Fase 1: 48 puntos de vida.
* Alterna abanicos descendentes y ráfagas dirigidas hacia posiciones concretas del jugador.
* Fase 2: recarga una nueva barra de 64 puntos.
* Aumenta la velocidad de desplazamiento y combina sus patrones en secuencias más exigentes.
* Utiliza avisos de al menos 0,5 segundos y descansos de 0,8 segundos.
* No permanezcas fuera del alcance del jugador: incluye posiciones y ventanas de ataque alcanzables con el salto y el propulsor breve.
* Evita que el combate requiera vuelo continuo.
REGLAS COMUNES DE LOS JEFES
* Cada jefe tiene exactamente dos fases.
* Agotar la primera barra inicia una transición única de 1,5 segundos.
* Durante la transición, limpia los proyectiles hostiles, suspende el daño de ambos personajes y muestra el nombre de la nueva fase.
* La segunda barra se carga una sola vez. No debe regenerarse continuamente.
* Agotar la segunda barra produce la victoria.
* Cada pulso del jugador causa un punto de daño.
* Los proyectiles dirigidos no persiguen al jugador después de lanzarse.
* Limita a doce los proyectiles hostiles activos.
* Los patrones deben ser reconocibles, evitables y distintos entre jefes.
* No aumentes la dificultad solamente mediante más vida: utiliza movimientos, combinaciones y ritmos diferentes.
CONTROLES Y MOVILIDAD
Conserva:
* A/D o flechas para desplazarse.
* Espacio para saltar.
* S o flecha abajo para agacharse, reduciendo realmente la zona de colisión.
* Shift para activar el propulsor en el aire.
* Propulsor con 0,8 segundos de energía y recarga completa en 1,5 segundos de contacto con suelo o plataformas.
* Apuntado con mouse: ±60° respecto a la horizontal en el suelo y 360° en el aire.
* Disparo con clic izquierdo, intervalo de 0,3 segundos, alcance de 350 píxeles y máximo de dos pulsos activos.
INTERFAZ
* Menú principal con "Jugar" y "Salir".
* Pantalla de selección con los tres jefes, su dificultad y su estado: bloqueado, disponible o derrotado.
* Los jefes bloqueados deben verse, pero no poder seleccionarse.
* Antes de entrar, muestra sus características y un botón "Combatir".
* Durante el combate, muestra cuatro corazones, energía del propulsor, nombre del jefe, fase y barra de vida.
* Conserva el botón de pausa con "Continuar", "Reintentar", "Selección de jefe" y "Salir".
* Después de vencer, ofrece "Siguiente jefe" cuando corresponda y "Selección de jefe".
* Los clics sobre botones nunca deben generar disparos.
ESTRUCTURA MODULAR
* Mantén main.py como punto de entrada pequeño.
* Separa configuración, coordinación del juego, robot, movimiento, colisiones, proyectiles, arenas, menús, HUD y progreso.
* Coloca cada jefe en un módulo propio dentro de entities/bosses/.
* Comparte únicamente la lógica común necesaria.
* Retira del flujo activo los módulos de baterías, portal y recorrido anterior.
* No agregues NPCs, enemigos comunes, armas, inventarios ni funciones ajenas a estos combates.
ENTREGA
1. Presenta el árbol actualizado de archivos y sus responsabilidades.
2. Entrega los archivos modificados o nuevos completos.
3. Explica los desbloqueos, el guardado local y las diferencias entre jefes.
4. Actualiza el README con instalación, controles y progresión.
5. Verifica selección, bloqueos, victorias, reintentos, transiciones, pausa y restauración de estados.
6. Distingue las pruebas realizadas de las pendientes y documenta las limitaciones reales.
Prioriza primero un combate completo que funcione; después incorpora los otros dos mediante la misma estructura modular.
```

</details>

**Cambios respecto a la versión 6:**

| Elemento | Versión 6 | Versión 7 |
|---|---|---|
| Concepto | Plataformas + un jefe al final | Solo combates contra jefes, elegidos desde un menú |
| Nivel, baterías, portal y enemigos comunes | Sí | Retirados (`world/level.py` y `entities/enemies.py` borrados) |
| Jefes | Centinela Eclipse (40 + 60) | Centinela (24 + 32), Embestidor (36 + 48) y Serafín (48 + 64), cada uno en `entities/bosses/` |
| Vidas de NEXO-7 | 3 | 4, y la transición del jefe no las recupera |
| Progreso | No se guardaba | `progreso.json` con desbloqueos y victorias |
| Pantallas | Inicio, pausa, victoria, derrota | Menú, selección, detalle, combate, pausa, victoria, derrota y campaña completada |
| Lógica de jefe | Una clase con todo | `JefeBase` (común) + un módulo por jefe (lo propio) |


### Pedido 8: corrección del Embestidor y superataque (después de jugar)

Después de probar la versión 7 en su computadora, el estudiante escribió dos pedidos en lenguaje natural, sin la estructura de los prompts anteriores:

> "Hay un problema con la habilidad del segundo jefe que son imposibles prácticamente de evadir porque al momento de que salta salta demasiado, entonces sería de ajustar ese ataque para que sea posible evitarlo."

> "Sigue con el mismo problema. […] Además de eso, creo yo que debería de haber un superataque con el clic derecho que se cargue después de cierta cantidad de ataques acertados."

**Qué se pidió:** que el ataque del segundo jefe se pudiera esquivar, y un superataque con clic derecho que se cargue acertando ataques.

**Cómo se trabajó:** el pedido describía una sensación ("imposible de evadir"), no una causa, así que antes de cambiar nada se **midió**:
1. El margen para presionar Espacio era de 0,12 s saltando quieto, y de 0 saltando alejándose. Eso llevó al ajuste 17.
2. Como el problema siguió, se clasificó cada golpe según lo que hacía el jefe en ese momento. Así apareció la causa real: la patrulla del descanso, que atropellaba sin aviso (ajuste 18).

Para el superataque, se fijaron números concretos (10 aciertos, 5 de daño) y reglas para los casos límite (menús, pausa, transición, reintento).


---

## Cómo funciona (resumen técnico)

- **Movimiento:** cada cuadro se leen las teclas presionadas y el robot se desplaza 5 px a la izquierda o a la derecha.
- **Gravedad:** la velocidad vertical aumenta 1 px por cuadro, hasta un máximo de 15. Saltar la pone en −17, así que el robot sube unos 136 px y luego cae.
- **Colisiones:** primero se mueve en X y se corrige si choca con un sólido; después se mueve en Y. Si choca cayendo, aterriza (`en_suelo = True`). Si choca subiendo, se golpea la cabeza. Solo se puede saltar con `en_suelo = True`.
- **Cámara:** `camara_x` intenta centrar al robot, pero se limita entre 0 y 1920 (2880 − 960). Todo se dibuja restando `camara_x` a su posición.
- **Enemigos:** cada uno recibe `(límite_izq, límite_der, y_de_la_superficie)`. Avanza 3 px por cuadro y, al tocar un límite, se acomoda en el borde y da la vuelta. El de la plataforma 5 tiene como límites los bordes de la plataforma, así que no puede caerse.
- **Dirección del pulso:** al presionar J, el pulso toma `mirando_derecha` del robot (1 = derecha, −1 = izquierda). Nace pegado al frente del robot, a la altura de su centro, y avanza 8 px por cuadro en esa dirección. Funciona igual en el suelo y en el aire.
- **Tiempo de espera:** al lanzar, `espera_pulso` vale 36 cuadros (0,6 s × 60 FPS) y baja 1 por cuadro. Solo se puede atacar si la espera está en 0, hay menos de 2 pulsos activos y la partida sigue en curso.
- **Alcance:** cada pulso suma en `recorrido` lo que avanza. El último paso se recorta para no pasar de 350 px, y al llegar ahí se elimina.
- **Colisiones del pulso:** cada cuadro se revisa si toca a un enemigo; si toca a uno, se eliminan ese enemigo y el pulso (`break`, así que solo uno). Si no, se elimina cuando llega a su alcance, choca con un sólido (`collidelist`) o sale del escenario. En la arena también se revisa si toca al jefe: le quita 1 de vida y el pulso desaparece.

### Versión 3: corazones y jefe

- **Corazones:** `vidas` empieza en 3 y el HUD dibuja un corazón lleno por cada punto (dos círculos y un triángulo). Todo el daño pasa por `recibir_danio()`, que no hace nada si `invulnerable > 0`. Si no, resta 1 y pone `invulnerable = 72` (1,2 s).
- **Parpadeo:** mientras `invulnerable > 0`, el robot se dibuja 6 cuadros sí y 6 no (`(invulnerable // 6) % 2`).
- **Caídas:** `caer_al_vacio()` resta un corazón y devuelve al robot a `posicion_segura`. Esa posición solo se guarda cuando el robot está apoyado con al menos 100 px de suelo a cada lado (`MARGEN_SEGURO`). Como vuelve arriba en el mismo cuadro, una caída daña una sola vez.
- **Portal:** `entrar_arena()` cambia la escena a `arena`. Pone un suelo continuo de 960 px, borra enemigos, pulsos y proyectiles, recupera los 3 corazones, coloca al robot a la izquierda y al jefe a la derecha, y deja la cámara en 0. La arena no tiene portal, así que no se puede volver ni recuperar vida otra vez.
- **Estados del jefe:** un temporizador cuenta los cuadros que faltan en el estado actual.
  - **Descanso** (2 s al entrar; luego 1,5 s, y 1,1 s en la fase 2): se mueve de lado a lado entre x=560 y x=920.
  - **Aviso** (0,75 s): se queda quieto, su ojo se pone amarillo y aparece un triángulo con "!". Para la ráfaga, además, brilla el cañón; para los proyectiles bajos, aparece una franja amarilla en el suelo.
  - **Ataque:** dispara 3 veces y vuelve a descanso, cambiando al otro patrón.
- **Ráfaga:** 3 disparos cada 24 cuadros. Cada disparo calcula la dirección hacia el centro del jugador en ese momento (`dx / distancia`, `dy / distancia`). Después la velocidad no cambia, así que no persigue.
- **Proyectiles bajos:** 3 proyectiles que ruedan por el suelo hacia el lado del jugador, uno cada 45 cuadros, con ~225 px de separación para saltarlos de a uno.
- **Fase 2:** con 6 de vida o menos, el jefe se vuelve naranja, la barra dice "FASE 2" y el descanso baja de 1,5 s a 1,1 s. Los avisos duran lo mismo.
- **Fin del combate:** si el jefe llega a 0 se revisa primero que el jugador (prioridad a la victoria). Al ganar se borran todos los proyectiles y ya no se procesa daño.

### Versión 4: menús, pausa y ajustes

- **Pantallas:** el juego tiene un `estado`: `inicio`, `jugando`, `pausa`, `victoria` o `derrota`. Cada estado tiene su lista de botones (`self.botones[estado]`), y solo se dibujan y se pueden pulsar los de la pantalla actual.
- **Botones:** la clase `Boton` guarda su texto, su acción y un rectángulo. Al dibujarse revisa si el cursor está encima (`collidepoint`); si lo está, usa un color más claro y un borde blanco.
- **Clics:** en el bucle principal solo se atiende `MOUSEBUTTONDOWN` con el botón izquierdo (`button == 1`), y como máximo un clic por cuadro. `manejar_clic()` ejecuta la acción del primer botón que contiene el punto y termina. Además, ningún botón está en la misma posición que un botón de la pantalla que aparece al pulsarlo, así que un clic no puede activar dos cosas.
- **Salir:** `manejar_clic()` devuelve `SALIR` y el bucle principal termina. La X de la ventana (`pygame.QUIT`) sigue funcionando.
- **Pausa:** `actualizar()` sale de inmediato si el estado no es `jugando`. Por eso, en pausa no se mueven el robot, el jefe ni los proyectiles, no hay daño, y tampoco bajan `espera_pulso`, `invulnerable`, el temporizador del jefe ni el anuncio de fase. Al continuar, todo sigue desde el mismo valor.
- **Ataque:** `ESPERA_PULSO = 18` cuadros (0,3 s). En cada cuadro de juego, si J está presionada (`teclas[pygame.K_j]`), se intenta lanzar un pulso. `puede_atacar()` solo lo permite con la espera en 0, menos de 2 pulsos activos y la partida en curso. Por eso, manteniendo J sale un pulso cada 18 cuadros, sin pasar de 2 a la vez.
- **Fases:** el jefe guarda `fase` (1 o 2). `recibir_impacto()` resta 1 y, si estaba en la fase 1 y quedó con 6 o menos, pasa a la fase 2 y activa `anuncio_fase` (90 cuadros). Como solo cambia cuando `fase == 1`, la transición ocurre una sola vez. En la fase 2 se mueve a 2,4 px por cuadro, guardando su posición con decimales (`self.x`), y descansa 48 cuadros.

### Versión 5: apuntado, agacharse y propulsor

- **Vector de apuntado:** en cada paso, el cursor (en píxeles de pantalla) se pasa al mundo sumándole `camara_x`. `apuntar()` resta la posición del hombro del robot y obtiene `dx` y `dy`. Si el cursor está a menos de 1 px del hombro, se conserva la dirección anterior.
- **Límite angular:** el ángulo se calcula con `atan2(-dy, abs(dx))`.
  - El `-dy` es porque en pantalla la Y crece hacia abajo; así, los ángulos positivos son hacia arriba.
  - El `abs(dx)` mide siempre desde la horizontal del lado hacia el que se apunta, y así el mismo rango sirve reflejado hacia la izquierda.
  - El ángulo se limita a [−60°, 60°] y se convierte en el vector `(lado · cos, −sin)`, que siempre mide 1. Por eso el pulso avanza 8 px por paso en cualquier dirección, sin importar qué tan lejos esté el cursor.
  - El lado al que mira el robot lo decide el cursor, no el movimiento.
- **Disparo:** el pulso sale de la boca del arma (hombro + 20 px en la dirección). En cada paso suma a `recorrido` la distancia avanzada y desaparece a los 350 px.
  - Mantener el clic dispara cada 18 pasos (0,3 s), con un máximo de 2 pulsos.
  - Después de Iniciar, Reiniciar, Volver a jugar o Continuar, `esperar_soltar_clic` exige soltar el botón antes de disparar.
- **Agacharse:** con S o flecha abajo, y solo si está apoyado, la altura pasa de 48 a 24 px y los pies quedan en el mismo lugar. La velocidad baja a 3 y el hombro (origen del disparo) baja con él. Al soltar, `levantarse()` prueba el rectángulo de pie; si chocaría con un sólido, sigue agachado. Saltar estando agachado también exige poder levantarse.
- **Propulsor:** con Shift, en el aire y con energía, la velocidad vertical cambia `+1 (gravedad) − 2 (empuje)` = 1 px/paso² hacia arriba, hasta un máximo de 6 px/paso. Las colisiones son las mismas, así que choca con los techos, y además no puede pasar del borde superior de la pantalla.
  - La energía se guarda en unidades enteras para evitar errores de redondeo: 360 en total, gasta 3 por paso (2 s) y recarga 4 por paso en el suelo (1,5 s).
- **Independencia de los FPS (paso fijo):** el bucle mide el tiempo real con `reloj.tick()` y lo acumula. Ejecuta `actualizar()` una vez por cada 1/60 s acumulado. A 30 FPS hace 2 pasos por cuadro y a 144 FPS, a veces ninguno. Así el juego va a la misma velocidad en cualquier computadora. Hay un tope de 0,25 s para que, después de un bloqueo de la ventana, no "salte" hacia adelante.

### Versión 6: módulos, propulsor breve, 360° en el aire y Centinela Eclipse

- **Bucle y estados:** `game.ejecutar()` tiene el bucle de paso fijo. `Juego.actualizar()` llama a `actualizar_nivel()` o a `actualizar_arena()` según la escena.
- **Propulsor:** la energía máxima se calcula como el mínimo común múltiplo entre los pasos de uso (48) y los de recarga (90): 720 unidades. Gasta 15 por paso en el aire con Shift y recarga 8 por paso solo si está apoyado. Si despega a mitad de la recarga, la energía queda como estaba hasta volver a apoyarse.
- **Apuntado:** `apuntar()` revisa `en_suelo`. En el aire usa el vector normalizado `(dx, dy) / distancia`, sin límite. En el suelo aplica el límite de ±60° de antes. Como se llama en cada paso, al despegar el límite desaparece y al aterrizar vuelve en el mismo paso.
- **Fase 1:** ráfaga (3 disparos al pecho de NEXO-7 en el momento de cada disparo) y proyectiles bajos (3, uno cada 0,75 s). Aviso de 0,75 s y descanso de 1,2 s.
- **Transición:** al quedar en 0 en la fase 1, `recibir_impacto()` cambia la fase a `TRANSICION` (1,5 s). Mientras dura:
  - `Juego` borra los proyectiles hostiles en cada paso;
  - el jefe no ataca ni se mueve;
  - los pulsos lo atraviesan sin hacerle daño y el contacto no daña a NEXO-7;
  - NEXO-7 se puede mover.

  El HUD muestra "Fase 2: Sobrecarga" y la barra se va llenando. Al terminar, `terminar_transicion()` fija la fase 2 con 60 de vida.
- **Fase 2:** velocidad 2,5 y descanso de 0,8 s.
  - **Abanico:** 5 proyectiles a 0°, 15°, 30°, 45° y 60° sobre la horizontal. El de 0° pasa por encima de NEXO-7 agachado; con salto y propulsor se puede pasar entre los de 0° y 15°.
  - **Ráfagas cortas:** 3 ráfagas de 3 disparos. Al empezar cada ráfaga se fija el objetivo (el pecho de NEXO-7), y los 3 disparos van a ese punto.
  - Los dos patrones usan aviso de 0,6 s.
- **Límite de 12:** antes de cada emisión, el jefe revisa si caben sus proyectiles (5 para el abanico). Si no caben, no avanza y lo vuelve a intentar en el siguiente paso.

### Versión 7: selección de jefes, progreso y tres jefes

- **Pantallas:** `Juego.estado` toma uno de estos valores: menú, selección, detalle, jugando, pausa, victoria, derrota o campaña. `manejar_clic()` busca el botón pulsado (como máximo uno) y cambia de pantalla. Las tarjetas de jefes bloqueados devuelven `None` y no hacen nada.
- **Combate:** `iniciar_combate(indice)` crea un `Robot` nuevo (4 corazones, energía llena), el jefe de esa posición en `JEFES`, y los sólidos de su arena con las plataformas del jefe. Lo usan "Combatir" y "Reintentar"; por eso un reintento lo restaura todo.
- **Victoria:** `revisar_fin()` revisa primero si el jefe fue derrotado; así, si los dos llegan a 0 en el mismo paso, gana NEXO-7. Llama a `Progreso.registrar_victoria()`, que suma la victoria, desbloquea el siguiente jefe y guarda.
- **Máquina de estados común** (`JefeBase.actualizar`):
  - en la transición solo cuenta 90 pasos y después recarga la segunda barra;
  - en el descanso llama a `mover_en_descanso()`; si devuelve `True` (el jefe todavía se está acomodando), el descanso no corre;
  - en el aviso, lo mismo con `mover_en_aviso()`;
  - en el ataque llama a `paso_ataque()` hasta que devuelve `True`, y entonces pasa al siguiente patrón.
- **Centinela Eclipse:** patrulla entre x=420 y 920. Los proyectiles bajos salen cada 45 pasos (36 en la fase 2). La ráfaga es de 3 disparos cada 24 pasos (18 en la fase 2). La ráfaga doble son dos ráfagas de 3 separadas por 40 pasos.
- **Embestidor Férreo:**
  - Al empezar el aviso decide hacia dónde embestirá (hacia NEXO-7) y hasta dónde: 320 px (400 en la fase 2), sin salir de la arena. Pinta en el suelo una franja con esa zona exacta y una flecha hasta el final.
  - Embiste a 8 px/paso (9 en la fase 2) y se detiene donde marcó. Mide 56 × 84 px, así que el salto de 136 px lo supera con margen.
  - Se esquiva de varias formas, cada una con su margen para presionar la tecla (fase 1):

    | Forma | Margen |
    | --- | --- |
    | Saltar alejándose | 1,03 s |
    | Salir de la zona caminando durante el aviso | 0,88 s |
    | Saltar hacia el jefe | 0,48 s |
    | Saltar pegado a la pared | 0,37 s |
    | Saltar quieto | 0,22 s |
  - El abanico son 5 disparos a −24°, −12°, 0°, 12° y 24° alrededor de la dirección al pecho de NEXO-7. Si NEXO-7 se agacha cuando llegan, el central pasa por encima y los inferiores se pierden en el suelo.
  - En la fase 2: embestida, luego un aviso de 40 pasos y después una ráfaga de 3.
- **Serafín Voltaico:**
  - Vuela a 4 px/paso (5,5 en la fase 2) entre posiciones altas (y = 160–200) para atacar y posiciones bajas (centro en y = 400, borde inferior en 435) para descansar.
  - El descanso cuenta desde que llega abajo: son 0,8 s quieto, la ventana de ataque.
  - El abanico descendente son 5 disparos hacia abajo separados 16°, con huecos entre ellos al llegar al suelo.
  - Su arena tiene una plataforma central bajo la posición alta del medio.

## Validación

### Pruebas realizadas por la IA (automáticas, sin ventana)

Se ejecutó un script con Pygame en modo sin pantalla que simula teclas y revisa el estado del juego.

**Versión 7: 167 de 167 correctas**, con pygame 2.6.1 y con pygame-ce 2.5.8. Las pruebas recorren la lista `JEFES`, así que las reglas comunes se verificaron en los tres jefes:

| Grupo | Qué se comprobó | Resultado |
|---|---|---|
| NEXO-7 | 4 corazones; 72 pasos de invulnerabilidad; salto de 136 px; agachado de 24 px; propulsor de 48 pasos y recarga de 90; ±60° en el suelo y 360° en el aire; disparo cada 18 pasos, máximo 2, alcance de 350 px en diagonal | ✅ |
| Progreso | Sin archivo: solo el Jefe 1. Vencer al 1 desbloquea al 2 y al 2 el 3. Se guarda solo `desbloqueados` y `victorias`, y se recupera al volver a abrir. 7 tipos de archivo dañado (texto roto, rangos y tipos inválidos, campos faltantes, archivo vacío): no se cierra, restablece y avisa en el menú | ✅ |
| Menús | Jugar y Salir; 3 tarjetas; los bloqueados no se eligen; detalle con Combatir y Volver; botones de pausa, derrota y victoria; Salir desde el menú, la pausa y la campaña; cambio de color con el cursor | ✅ |
| Clics | Combatir, Continuar y Reintentar no disparan hasta soltar el clic; no se dispara en ninguna pantalla que no sea el combate | ✅ |
| Cada jefe | Empieza en la fase 1 con su vida. La transición de 90 pasos borra los proyectiles, no daña a nadie y no recupera corazones. La segunda barra se carga una sola vez y agotarla da la victoria. Alterna sus patrones con aviso. Avisos y descansos de al menos lo pedido. Nunca más de 12 proyectiles en 8000 pasos. Los proyectiles no cambian de dirección. La pausa congela todo. Reintentar restaura 4 corazones, energía y fase 1. Perder no quita desbloqueos. Empate = victoria. La victoria se guarda y desbloquea. "Siguiente jefe" abre el detalle del próximo | ✅ ×3 |
| Diferencias | Ningún patrón se repite entre jefes; el Embestidor es más rápido; avisos y descansos que se acortan de jefe en jefe (48/36/30 y 84/60/48 pasos); vidas pedidas | ✅ |
| Centinela | Siempre en el suelo, patrulla a ≤ 2 px por paso; en la fase 2 dispara más seguido y la ráfaga doble lanza 6 | ✅ |
| Embestidor | La embestida recorre 320 px y se detiene donde marcó el aviso; quieto en la zona recibe la embestida; salir de la zona caminando (0,88 s de margen), saltar alejándose (1,03 s), saltar quieto (0,22 s) y saltar pegado a la pared (0,37 s) evitan el daño, también en la fase 2; abanico: quieto de pie recibe daño, agachándose después del disparo no; fase 2: embestida → aviso de 40 pasos → ráfaga | ✅ |
| Serafín | Vuela entre posiciones altas y bajas sin salir de la arena; en cada descanso baja a 435 px; desde el suelo, sin saltar, le acierta en la ventana baja; en la posición alta central se le alcanza desde la plataforma con salto y propulsor; abanico descendente con daño en unos lugares y espacios seguros entre rayos | ✅ |
| Patrulla | Con el robot quieto en 5 posiciones, el Centinela y el Embestidor nunca lo atropellan en el descanso ni se le acercan a menos de 160 px | ✅ |
| Superataque | Empieza sin carga; sin carga el clic derecho no hace nada; 10 aciertos lo cargan; lanza una sola descarga y vacía la carga; no ocupa el lugar de los 2 pulsos; hace 5 de daño y no suma carga; destruye proyectiles hostiles; no se usa en menús, pausa, fin de combate ni en la transición (la carga se conserva); Reintentar la pone en 0; con 3 de vida en la fase 1 inicia la transición; en la fase 2 puede dar la victoria | ✅ |
| Combates completos | Un jugador automático, que en cada paso simula 7 acciones durante 30 pasos y elige la que no choca, vence al Centinela (19 s, terminó con 3 corazones), al Embestidor (31 s, con 4) y al Serafín (122 s, con 4). **Nunca usa el propulsor**: el combate no exige volar | ✅ |

También se ejecutó `main.py` con clics simulados (menú → selección → detalle → combate → pausa → Salir), sin errores.

**Versión 6: 176 de 176 correctas**, con pygame 2.6.1 y con pygame-ce 2.5.8.

Primero se comprobó que la **reorganización en módulos no cambió nada**: las 136 pruebas de la versión 5 pasaron sin cambios de lógica, solo adaptadas a los nuevos nombres (`j.robot` en lugar de `j.jugador`, la vida guardada en el robot, una sola clase `Proyectil`). Después se cambió la jugabilidad y se agregaron estas pruebas:

| Regla | Resultado |
|---|---|
| El propulsor dura exactamente 48 pasos (0,8 s) | ✅ |
| No recarga en el aire; recarga completa en 90 pasos (1,5 s) apoyado | ✅ |
| Si despega a mitad de la recarga, la energía queda como estaba | ✅ |
| Manteniendo Shift no se vuela para siempre: aterriza solo | ✅ |
| Shift en el suelo no despega; con propulsor se sube más que con el salto (136 px) | ✅ |
| En el aire se apunta en 360° (cada 5°) con vector de largo 1, incluso recto hacia abajo | ✅ |
| Cursor a −80°: en el suelo se limita a −60°; al despegar y volando se libera; al aterrizar vuelve a −60° | ✅ |
| Disparo hacia abajo en el aire: 8 px por paso y desaparece al tocar el suelo | ✅ |
| En el aire se mueve hacia un lado y dispara hacia el otro | ✅ |
| El jefe empieza en la fase 1 con 40; con 1 de vida sigue en la fase 1 | ✅ |
| Al llegar a 0: empieza la transición y se borran los proyectiles hostiles; no es victoria | ✅ |
| La transición dura 90 pasos (1,5 s), sin daño para nadie (contacto ni pulsos); NEXO-7 se puede mover | ✅ |
| Fase 2 con 60 / 60 | ✅ |
| En todo el combate la vida del jefe sube una sola vez, y termina derrotado en la fase 2 | ✅ |
| Con 0 en la fase 2: victoria; si ambos llegan a 0 a la vez, gana el jugador | ✅ |
| Fase 2: +25 % de velocidad (100 px contra 80 en 40 pasos), aviso de 36 pasos y descanso de 48 | ✅ |
| Fase 1: aviso de 45 pasos y descanso de 72 | ✅ |
| La fase 2 alterna abanico y ráfagas cortas, siempre con aviso | ✅ |
| Abanico: 5 proyectiles a 0°, 15°, 30°, 45° y 60°, con separación mínima de 80 px a 300 px de distancia | ✅ |
| Abanico: de pie recibe 1 impacto; agachado, 0; con salto y propulsor entre los rayos, 0 | ✅ |
| Ráfagas cortas: 3 de 3, cada una al punto donde estaba NEXO-7 al empezarla, sin perseguirlo | ✅ |
| Ráfagas cortas: de pie recibe daño; agachándose cuando se acercan los disparos, no | ✅ |
| Con 9 proyectiles, el abanico espera; cuando hay lugar, lanza sus 5 (12 en total) | ✅ |
| En las dos fases nunca hay más de 12 proyectiles hostiles | ✅ |
| Volver a jugar (tras ganar o perder) y Reiniciar en la transición: el jefe vuelve a la fase 1 con 40 y la energía se llena | ✅ |
| La pausa congela la transición | ✅ |
| El HUD dibuja la fase y la vida en la fase 1, en la transición y en la fase 2 | ✅ |
| Un jugador automático que esquiva y dispara completa nivel, fase 1 y fase 2 sin perder corazones en la arena (42 s) | ✅ |

También se comprobó que `python main.py` arranca y cierra sin errores de importación, y que el bucle de paso fijo da ~120 pasos cada 2 s a 30, 60 y 144 FPS.

**Versión 5: 136 de 136 correctas**, con pygame 2.6.1 y con pygame-ce 2.5.8. Repiten las de las versiones 3 y 4 adaptadas al disparo con clic, y agregan:

| Regla | Resultado |
|---|---|
| Cursor a la derecha: 0° y vector (1, 0); 45° arriba da `dy` negativo en pantalla | ✅ |
| 80° se limita a +60°; −85° se limita a −60° | ✅ |
| Hacia la izquierda el rango se refleja (30°, y −70° → −60°) | ✅ |
| Cursor justo encima: conserva el lado y limita a 60°; cursor sobre el arma: conserva la dirección | ✅ |
| Para todos los ángulos de −90° a 90°, ambos lados y distancias de 5 a 900 px: vector de largo 1 y ángulo dentro del rango | ✅ |
| Con la cámara desplazada, el cursor se convierte bien a coordenadas del mundo | ✅ |
| Camina a la izquierda mientras dispara a la derecha | ✅ |
| Diagonales a 45° (derecha) y 30° (izquierda): línea recta, 8 px por paso, 350 px de alcance | ✅ |
| Cursor cerca o lejos: el pulso avanza igual | ✅ |
| Mantener el clic: un pulso cada 0,3 s y nunca más de 2 | ✅ |
| Se dispara agachado, saltando y volando; el arma baja al agacharse | ✅ |
| El clic en Iniciar o Continuar no dispara: hay que soltar y volver a presionar | ✅ |
| No se dispara en inicio, pausa, victoria ni derrota | ✅ |
| S o flecha abajo: altura 24 con los pies en el mismo lugar; velocidad 3; no se agacha en el aire | ✅ |
| Bajo un obstáculo de 34 px: de pie choca; agachado pasa; al soltar S sigue agachado; no puede saltar; al salir se levanta sin meterse en la plataforma | ✅ |
| Un disparo de ráfaga que golpea al robot de pie no lo toca si se agacha | ✅ |
| Shift en el suelo no hace nada; con salto + Shift sube mucho más que los 136 px del salto | ✅ |
| Subida limitada a 6 px por paso; la energía dura exactamente 120 pasos (2 s) | ✅ |
| Al soltar Shift o sin energía vuelve la gravedad; la recarga tarda exactamente 90 pasos (1,5 s) | ✅ |
| Volando no atraviesa plataformas ni sale por arriba o por los costados | ✅ |
| La pausa congela el vuelo, la energía y los tiempos; Volver a jugar restaura postura, energía, vida y combate | ✅ |
| Los proyectiles bajos se esquivan saltando con propulsor; el jugador automático sigue ganando (13 s) | ✅ |

También se probó el **bucle principal real** con un reloj falso:
- a 30, 60 y 144 FPS se simulan ~120 pasos por cada 2 s reales, así que la velocidad del juego es la misma;
- mantener el clic de "Iniciar" durante 1 s no lanza ningún pulso, y al soltar y volver a presionar sí dispara.

**Versión 4: 91 de 91 correctas**, con pygame 2.6.1 y con pygame-ce 2.5.8. Repiten las de la versión 3, adaptadas a los nuevos tiempos y botones, y agregan:

| Regla | Resultado |
|---|---|
| Al abrir se ve la pantalla inicial; cada pantalla tiene los botones pedidos | ✅ |
| En el menú, J, espacio y las flechas no hacen nada | ✅ |
| Iniciar empieza con 3 corazones; un clic fuera de los botones no hace nada | ✅ |
| Salir funciona desde inicio, pausa, victoria y derrota | ✅ |
| R y Escape ya no reinician ni cierran | ✅ |
| Ningún botón se superpone con los de la pantalla siguiente; repetir el clic en el mismo punto no activa nada | ✅ |
| El botón cambia de color con el cursor encima | ✅ |
| 5 s de pausa: no cambia nada (posiciones, proyectiles, temporizador del jefe, espera, invulnerabilidad, vidas) | ✅ |
| Continuar reanuda con los mismos tiempos; Reiniciar desde la pausa restaura toda la aventura | ✅ |
| Mantener J: 12 pulsos en 4 s, intervalo mínimo de 18 cuadros (0,3 s), nunca más de 2 activos | ✅ |
| No se puede atacar en inicio, pausa, victoria ni derrota | ✅ |
| El jefe sigue en la fase 1 con 7 de vida y pasa a la fase 2 con 6, una sola vez, con anuncio de 1,5 s | ✅ |
| En 50 cuadros recorre 100 px en la fase 1 y 120 px en la fase 2 (+20 %) | ✅ |
| Descanso: 72 cuadros (1,2 s) en la fase 1 y 48 (0,8 s) en la fase 2 | ✅ |
| En la fase 2 siguen los dos patrones, siempre con aviso de 45 cuadros | ✅ |
| Volver a jugar (tras ganar o perder) restaura corazones, enemigos, jefe, fase, proyectiles y tiempos | ✅ |
| El jugador automático completa todo (14 s) | ✅ |

También se probó el **bucle principal real** (`main()`) con clics simulados:
- Iniciar → Pausa → Continuar → Pausa → Salir cierra el juego.
- Si llegan dos clics en el mismo cuadro, solo cuenta el primero.
- La X de la ventana cierra el juego.
- Escape ya no cierra.

**Versión 3: 53 de 53 correctas**, con pygame 2.6.1 y con pygame-ce 2.5.8.

| Regla | Resultado |
|---|---|
| Empieza con 3 corazones; tocar un enemigo resta 1 y no termina la partida | ✅ |
| Durante 1,2 s (72 cuadros) el contacto no quita más vida; después vuelve a dañar | ✅ |
| El robot parpadea mientras es invulnerable | ✅ |
| Con 0 corazones aparece la derrota | ✅ |
| Caer al hueco resta 1 corazón y regresa a un lugar a 100 px o más del borde; la misma caída no daña dos veces | ✅ |
| El portal lleva a la arena (no es victoria), recupera los 3 corazones y limpia enemigos, pulsos y proyectiles | ✅ |
| Arena fija (cámara en 0), suelo continuo, límites izquierdo y derecho; no se recupera vida otra vez | ✅ |
| El jefe tiene 12 de vida; cada pulso le resta 1 y desaparece | ✅ |
| El jefe se desplaza y nunca sale de su zona (6000 cuadros) | ✅ |
| Patrones en orden ráfaga → bajos → ráfaga → bajos; cada ataque va precedido de un aviso de 45 cuadros (≥ 36) | ✅ |
| Descanso de 90 cuadros en la fase 1 y de 66 en la fase 2 (≥ 60) | ✅ |
| Ráfaga: cada disparo va hacia donde estaba el jugador en ese momento, con velocidad constante | ✅ |
| Proyectiles bajos: 3, por el suelo, separados 225 px; un jugador que salta cada uno no recibe daño | ✅ |
| Fase 2 con 6 de vida: cambia de color y descansa menos | ✅ |
| Un proyectil que impacta resta 1 y desaparece; los que salen de la arena también desaparecen; nunca hay más de 12 | ✅ |
| Al morir el jefe: victoria, sin proyectiles, sin daño ni ataques; si ambos llegan a 0 a la vez, gana el jugador | ✅ |
| R tras ganar y tras perder reinicia toda la aventura | ✅ |
| Las 11 superficies del nivel siguen siendo alcanzables | ✅ |
| Un jugador automático completa el nivel y vence al jefe (18 s en total, sin perder corazones en la arena) | ✅ |
| Quedarse quieto en la arena sin esquivar lleva a la derrota en ~10 s (los ataques sí son peligrosos) | ✅ |

**Versión 2: 33 de 33 correctas**, con pygame 2.6.1 y con pygame-ce 2.5.8. Además de repetir las pruebas de la versión 1:

| Regla | Resultado |
|---|---|
| Hay 3 enemigos y su velocidad subió de 2 a 3 | ✅ |
| Ninguno sale de su zona ni de su superficie en 5000 cuadros (el de la plataforma no se cae) | ✅ |
| Ningún enemigo está a menos de 300 px de la aparición; quedarse quieto 2 s no hace perder | ✅ |
| Pulso hacia la derecha, hacia la izquierda y durante un salto | ✅ |
| Espera: no se lanza otro pulso durante 35 cuadros y sí a los 36 (0,6 s) | ✅ |
| Nunca hay más de 2 pulsos activos (600 cuadros presionando J) | ✅ |
| El pulso avanza 350 px y desaparece | ✅ |
| El pulso desaparece al chocar con una plataforma y al salir del escenario | ✅ |
| Un pulso elimina a un solo enemigo aunque haya dos juntos | ✅ |
| Después de ganar o de perder no se puede atacar | ✅ |
| R restaura los 3 enemigos y borra pulsos y espera (tras perder y tras ganar) | ✅ |
| Las 11 superficies y las 6 baterías siguen siendo alcanzables | ✅ |
| Un jugador automático que camina, dispara y salta los huecos gana la partida | ✅ |

**Versión 1: 14 de 14 correctas.**

| Regla | Resultado |
|---|---|
| Altura del salto = 136 px | ✅ |
| No se puede saltar en el aire | ✅ |
| Una batería se cuenta una sola vez | ✅ |
| El enemigo nunca sale de su zona (1300–1650) en 5000 cuadros | ✅ |
| Caer en un hueco provoca la derrota | ✅ |
| Después de perder, nada se mueve | ✅ |
| Tocar al enemigo provoca la derrota | ✅ |
| Tocar el portal muestra la victoria | ✅ |
| R restaura jugador, enemigo, baterías y contador | ✅ |
| El jugador no sale por los bordes y la cámara queda entre 0 y 1920 | ✅ |
| Las 11 superficies (3 tramos de suelo + 8 plataformas) son alcanzables saltando | ✅ |
| Las 6 baterías se pueden recoger | ✅ |

También se generaron capturas de pantalla para revisar el dibujo del robot, los enemigos, las baterías, el pulso, el indicador de ataque, el portal y los mensajes de victoria y derrota.

### Errores encontrados y ajustes

1. **Instalación en macOS con Python 3.14:** `pip install -r requirements.txt` falló con `'SDL.h' file not found`, porque pygame 2.6.1 no tiene versión para Python 3.14 e intentó compilarse. **Ajuste:** se instaló `pygame-ce`, que es compatible y no requiere cambiar el código. En la versión 7, `requirements.txt` pasó a pedir `pygame-ce` directamente.
2. **El pulso pasaba 2 px de su alcance:** avanzaba de 8 en 8 y 350 no es múltiplo de 8, así que llegaba a 352 px. Lo detectó una prueba automática. **Ajuste:** el último paso se recorta a lo que falta.
3. **La regla de "máximo 2 pulsos" no tenía efecto:** con velocidad 10, el pulso desaparecía en 35 cuadros, antes de que terminara la espera de 36. **Ajuste:** se bajó la velocidad a 8 (el pulso dura unos 44 cuadros).
4. **El indicador decía "listo" después de perder,** aunque el ataque estaba bloqueado. Se vio en una captura. **Ajuste:** `puede_atacar()` también revisa que la partida siga en curso.
5. **(Versión 3) Reaparecer al filo del hueco:** al principio, la posición segura era el último lugar donde el robot estuvo apoyado, que muchas veces es el borde del hueco. Una prueba mostró que, con la tecla todavía presionada, el robot volvía a caer enseguida y perdía otro corazón. **Ajuste:** solo se guarda una posición con al menos 100 px de suelo a cada lado (`MARGEN_SEGURO`). Para eso el jugador ahora recuerda sobre qué sólido está parado (`apoyo`).
6. **(Versión 4) Textos encimados en la pausa:** en una captura, el anuncio "FASE 2" quedaba detrás del título "Pausa". **Ajuste:** el anuncio solo se dibuja mientras se juega. Como su tiempo no corre en pausa, sigue visible al continuar.
7. **(Versión 5) Energía con errores de redondeo:** al principio, la energía se guardaba en segundos y se restaba 1/60 por paso. Las pruebas mostraron que duraba 121 pasos en vez de 120 y que recargaba en 91 en vez de 90, porque 2,0 − 120 × (1/60) no da exactamente 0 en decimales. **Ajuste:** se cuenta en unidades enteras (360; gasta 3 y recarga 4 por paso).
8. **(Versión 5) Agacharse no esquivaba la ráfaga:** la ráfaga apuntaba al centro del robot, y ese punto sigue dentro del cuerpo agachado. **Ajuste:** apunta al pecho (borde superior + 10 px). Un disparo hecho al robot de pie le pasa por encima si se agacha.
9. **(Versión 5) Posición segura con la altura variable:** como ahora la altura del robot cambia, la posición segura se guarda por los pies (`bottomleft`). Si se guardara la esquina superior, el robot podría reaparecer metido en el suelo.
10. **(Versión 6) Superposición en el HUD:** en una captura, "Centinela Eclipse · Fase 2 · 60/60" se encimaba con el indicador del pulso. **Ajuste:** el indicador se acortó ("Pulso: listo") y la vida del jefe pasó debajo de la barra.
11. **(Versión 6) Reorganizar sin romper:** antes de cambiar la jugabilidad, la versión modular se probó con las 136 pruebas de la versión 5. Pasaron todas, lo que confirma que el comportamiento se conservó. Para no perder datos entre módulos, la vida, la invulnerabilidad y la espera de disparo pasaron del `Juego` al `Robot`, que es su dueño.
12. **(Versión 7) Tarjetas superpuestas:** en la primera captura de la selección, las tres tarjetas de 270 px se encimaban (estaban separadas solo 240). **Ajuste:** tarjetas de 250 px separadas 270, y la dificultad con una fuente más pequeña.
13. **(Versión 7) Título del jefe sobre los corazones:** con 4 corazones, "Embestidor Férreo · Fase 2: Metal al rojo" chocaba con ellos. **Ajuste:** el título del jefe usa una fuente más pequeña.
14. **(Versión 7) Plataforma que tapaba la ventana de ataque:** la posición baja izquierda del Serafín quedaba encima de una plataforma. Los disparos desde el suelo chocaban con ella y el jefe incluso se metía 5 px en la plataforma. Una prueba lo detectó (0 impactos en 1 s). **Ajuste:** las posiciones bajas pasaron a x = 200 y 760, y la arena quedó con una sola plataforma central bajo la posición alta del medio.
15. **(Versión 7) Nombres de patrones repetidos:** el Centinela y el Serafín tenían ambos una "ráfaga dirigida", y el Embestidor y el Serafín un "doble abanico". Se comportan distinto, pero los nombres confundían. **Ajuste:** los del Serafín se llaman "descarga aérea" y "lluvia doble".
16. **(Versión 7) Lo que las pruebas enseñaron sobre los abanicos dirigidos:** el abanico del Embestidor apunta al pecho de NEXO-7 en el momento del disparo, así que agacharse antes no sirve. La forma correcta es estar de pie cuando dispara y agacharse cuando llega. Se documentó en el detalle del jefe ("abanico hacia ti con espacios").
17. **(Versión 7) Embestida prácticamente imposible de esquivar (encontrado al jugar):** al probar el juego en la Mac, el estudiante reportó que la embestida del Embestidor no se podía evitar. Al medirlo se confirmó: cruzaba la arena de pared a pared, saltando quieto había solo 0,12 s para acertar el salto, y saltar alejándose (lo instintivo) era imposible. **Ajuste:** la embestida recorre una distancia fija (320 px; 400 en la fase 2) que el aviso marca en el suelo, y el jefe es más bajo y angosto (56 × 84 px). Ahora se puede salir de la zona durante el aviso (0,88 s de margen) o saltar alejándose (1,03 s). El jugador automático pasó de terminar con 1 corazón a no perder ninguno.
18. **(Versión 7) El Embestidor seguía golpeando "sin aviso" (encontrado al jugar):** después del ajuste 17, el estudiante reportó que seguía igual. Se simuló a un jugador que solo sale de la franja y se agacha ante el abanico, y se clasificó cada golpe según lo que hacía el jefe en ese momento. La mayoría llegaba **en el descanso**: entre ataques, el jefe patrullaba toda la arena a 3 px por paso y pasaba por encima del robot sin ningún aviso. **Ajuste:** en el descanso, los jefes de suelo mantienen 160 px de distancia y se alejan si están más cerca. Con la misma estrategia simple, los golpes en 30 s bajaron de 8–15 a 0–3 (los restantes son del abanico muy cerca del jefe).

### Pruebas manuales (para hacer al jugar)

1. Moverse con A/D y con las flechas; saltar con espacio.
2. Mantener presionado espacio o presionarlo en el aire: no debe haber un segundo salto.
3. Recoger una batería: el contador sube 1 y la batería desaparece.
4. Dejarse tocar por el enemigo: aparece "Fin de la partida" y nada se mueve.
5. Caer en un hueco: derrota con el mensaje "Caíste al vacío".
6. Presionar R: el robot vuelve al inicio, las baterías reaparecen y el contador vuelve a 0.
7. Caminar contra el borde izquierdo y el derecho: el robot no sale y la cámara no muestra espacio vacío.
8. Llegar al portal: aparece la victoria con la cantidad de baterías recogidas.
9. Cerrar con Escape y con la X de la ventana.

**Pulso de energía (versión 2):**

10. Mirar a la derecha y presionar J; luego mirar a la izquierda y presionar J: el pulso sale hacia el lado correcto.
11. Saltar y presionar J en el aire: el pulso sale a la altura del robot.
12. Presionar J muy rápido: solo sale un pulso cada 0,6 s, el indicador pasa a gris ("recargando") y la barra se vuelve a llenar.
13. Presionar J apenas termine la espera: puede haber 2 pulsos en pantalla, pero nunca 3.
14. Disparar a un enemigo: desaparecen el enemigo y el pulso.
15. Disparar contra el costado de una plataforma (por ejemplo, saltando junto a la plataforma 2): el pulso desaparece al chocar.
16. Disparar al vacío: el pulso desaparece a unos 350 px (algo más de un tercio de la pantalla).
17. Tocar a un enemigo justo después de disparar: igual se pierde (no hay invulnerabilidad).
18. Perder o ganar y presionar J: no sale ningún pulso.
19. Presionar R después de perder y después de ganar: vuelven los 3 enemigos, no queda ningún pulso y el indicador dice "listo".
20. Completar el nivel dos veces: una eliminando a los enemigos y otra esquivándolos con saltos o pasando por las plataformas.

**Corazones, arena y jefe (versión 3):**

21. Tocar un enemigo: se pierde 1 corazón, el robot parpadea y la partida sigue.
22. Mientras parpadea, quedarse encima del enemigo: no se pierde otro corazón hasta que deja de parpadear.
23. Caer en un hueco: se pierde 1 corazón y el robot reaparece lejos del borde, sin perder otro por la misma caída.
24. Perder los 3 corazones en el nivel: aparece "Te quedaste sin corazones".
25. Llegar al portal con 1 o 2 corazones: aparece la arena, sin cámara, con los 3 corazones llenos, el robot a la izquierda y VOLTARÓN a la derecha.
26. Caminar hasta los dos bordes de la arena: el robot no sale de la pantalla.
27. Observar al jefe: se mueve en el descanso, se detiene y muestra el "!" antes de cada ataque, y alterna ráfaga y proyectiles bajos.
28. Ráfaga: moverse o saltar entre disparos; cada disparo va hacia donde estabas, no te sigue.
29. Proyectiles bajos: saltarlos de a uno.
30. Disparar al jefe: la barra baja de a 1 (12/12 → 11/12…).
31. Bajar al jefe a 6: se pone naranja, aparece "FASE 2" y descansa menos, pero sigue avisando.
32. Vencer al jefe: desaparecen sus proyectiles y aparece "¡Derrotaste a VOLTARÓN!".
33. Perder en la arena: aparece "VOLTARÓN te venció".
34. ~~Presionar R después de ganar y de perder~~ (reemplazada por la 43 en la versión 4).

**Botones, pausa y ataque (versión 4):**

35. Abrir el juego: aparece la pantalla inicial con el título, los controles e Iniciar / Salir. Pasar el cursor por cada botón: cambia de color.
36. Presionar J, espacio o las flechas en la pantalla inicial: no pasa nada.
37. Pulsar Iniciar: empieza la partida con 3 corazones y aparece el botón Pausa arriba a la derecha.
38. Pausar con un enemigo o un proyectil cerca: todo se congela, el robot no se mueve aunque presiones teclas y no recibe daño. Esperar unos segundos y pulsar Continuar: todo sigue desde el mismo punto.
39. Recibir un golpe, pausar mientras parpadea, esperar y continuar: el parpadeo dura lo que le faltaba, no se consumió en la pausa.
40. Mantener J presionada: sale un pulso cada 0,3 s y nunca hay más de 2 en pantalla. Probar también en el aire y hacia los dos lados.
41. Bajar al jefe de 7 a 6: aparece "FASE 2" por un momento, el jefe se vuelve naranja, se mueve un poco más rápido y descansa menos, pero sigue avisando antes de cada ataque.
42. Pulsar Reiniciar en la pausa: vuelve al inicio del nivel con todo restaurado.
43. Ganar y perder: aparecen "Volver a jugar" y "Salir". Volver a jugar restaura 3 corazones, 3 enemigos, baterías, jefe en la fase 1 y el ataque listo.
44. Pulsar Salir en el inicio, en la pausa y al terminar la partida: el juego se cierra. También cerrar con la X de la ventana.
45. Presionar R y Escape en cualquier momento: no hacen nada.

**Apuntado, agacharse y propulsor (versión 5):**

46. Mover el ratón alrededor del robot: el arma y la línea amarilla siguen al cursor. Arriba o abajo del robot, la línea se queda en 60°.
47. Disparar hacia la derecha y hacia la izquierda, recto y en diagonal: el pulso va hacia el cursor (o hacia el ángulo límite), siempre a la misma velocidad.
48. Caminar hacia un lado mientras se apunta y dispara hacia el otro.
49. Mantener el clic: sale un pulso cada 0,3 s y nunca hay más de 2.
50. Avanzar con la cámara desplazada (mitad del nivel) y apuntar: la mira y el disparo coinciden con el cursor.
51. Pulsar Iniciar o Continuar sin soltar el botón: no sale ningún disparo hasta soltar y volver a hacer clic.
52. Agacharse (S): el robot se hace más bajo y más lento. En el aire, S no hace nada.
53. Con el jefe: agacharse justo después de que dispare la ráfaga; el disparo pasa por encima.
54. Saltar y mantener Shift: el robot sube con llama y la barra baja. A los 2 s se acaba y vuelve a caer. Al aterrizar, la barra se llena en 1,5 s.
55. Volar debajo de una plataforma: choca y no la atraviesa. Volar hacia arriba en la arena: no sale de la pantalla.
56. Pausar mientras vuela: el robot queda quieto en el aire y la barra no cambia. Al continuar, sigue igual.
57. Perder agachado o con la energía a medias y pulsar Volver a jugar: de pie, con energía llena y 3 corazones.

**NEXO-7 y Centinela Eclipse (versión 6):**

58. La pantalla inicial dice "NEXO-7 en la estación abandonada", y el HUD muestra "NEXO-7" junto a los corazones.
59. Saltar y mantener Shift: el propulsor dura menos de un segundo. En el aire la barra no se recarga; al aterrizar se llena en 1,5 s.
60. En el aire, apuntar hacia abajo y hacia atrás: la línea amarilla sigue al cursor en cualquier dirección. Al aterrizar, vuelve a quedarse entre −60° y 60°.
61. Bajar al Centinela de 40 a 0: aparece "Fase 2: Sobrecarga", desaparecen sus disparos, parpadea entre índigo y rojo, y la barra se llena. Durante 1,5 s no hace daño ni lo recibe, y NEXO-7 se puede mover.
62. Fase 2: el jefe es rojo, se mueve más rápido y alterna abanico (5 líneas amarillas de aviso) y ráfagas cortas (3 puntos de aviso).
63. Abanico: esquivarlo agachado. En otra ronda, esquivarlo saltando con propulsor entre los dos rayos más bajos.
64. Ráfagas cortas: moverse o agacharse entre ráfagas; cada ráfaga va adonde estaba NEXO-7 cuando empezó.
65. Vencer la fase 2: victoria. Volver a jugar y llegar otra vez a la arena: el Centinela empieza en la fase 1 con 40.

**NEXO-7: Arena Eclipse (versión 7):**

66. Borrar `progreso.json` y abrir el juego: en la selección solo el Centinela está disponible; los otros dos se ven grises con candado y no responden al clic.
67. Escribir texto cualquiera en `progreso.json` y abrir el juego: no se cierra y el menú avisa que se restableció el progreso.
68. Vencer al Centinela: "Siguiente jefe" lleva al detalle del Embestidor. En la selección, el Centinela figura como "Derrotado (1)".
69. Cerrar y volver a abrir el juego: los desbloqueos siguen.
70. Perder contra el Embestidor: "Reintentar" empieza con 4 corazones y el jefe en la fase 1; "Selección de jefe" mantiene los desbloqueos.
71. En cada jefe, agotar la fase 1: aparece "Fase 2: …", desaparecen los proyectiles y no se recuperan corazones.
72. Embestidor: esquivar la embestida saliendo de la franja amarilla durante el aviso, y otras veces saltándola (alejándose, hacia él o pegado a la pared); en el abanico, agacharse cuando llegan los disparos.
73. Serafín: dispararle cuando baja a descansar; desde la plataforma central, alcanzarlo arriba con salto y propulsor; buscar los huecos del abanico descendente.
74. Vencer al Serafín: aparece "¡Campaña completada!".
75. Pausar en cada jefe: todo se congela. Probar Continuar, Reintentar, Selección de jefe y Salir.
76. Hacer clic en Combatir, Continuar o Reintentar y mantener el botón: no sale ningún disparo hasta soltar.
77. Embestidor: quedarse lejos de él entre ataques; ya no debería acercarse hasta tocarte sin una franja o un "!" antes.
78. Acertar 10 pulsos al jefe: la barra Súper se llena, brilla, y el pecho de NEXO-7 se pone amarillo.
79. Clic derecho: sale el orbe grande, borra los proyectiles que toca y le quita 5 al jefe; la barra vuelve a 0.
80. Clic derecho con la carga llena durante la transición o en pausa: no pasa nada y la carga se conserva.

### Limitaciones conocidas

- Las pruebas automáticas no reemplazan jugarlo: falta probarlo con ventana real y teclado.
- El jugador automático ganó en unos 9 segundos yendo directo al portal. Recoger las 6 baterías lleva más tiempo, pero la partida puede seguir siendo más corta que el minuto pedido en el prompt 1.
- La física y la espera del pulso se cuentan "por cuadro": si el equipo no alcanza 60 FPS, todo se siente más lento (incluida la espera de 0,6 s).
- Desde el suelo no se puede dar al enemigo de la plataforma 5, porque el pulso pasa por debajo. Hay que subir a la plataforma. Es una decisión de diseño: ese enemigo y su batería son opcionales.
- El enemigo de la plataforma 5 empieza en el borde izquierdo. Si el robot sube justo ahí al comenzar, puede chocar con él. Conviene mirar antes de subir.
- `requirements.txt` sigue pidiendo `pygame`. En Python 3.14 hay que instalar `pygame-ce` a mano (ver nota en "Cómo ejecutarlo").
- **(Versión 3)** Las caídas siempre restan un corazón, incluso durante la invulnerabilidad. Si no, se podría caer gratis mientras el robot parpadea. Es una decisión de diseño.
- **(Versión 3, más notorio en la 4)** El jefe muere rápido. Con la espera de 0,3 s, un jugador cerca del jefe puede hacerle los 12 impactos en pocos segundos, porque los pulsos llegan antes y se libera el límite de 2. Para una pelea más larga habría que subir su vida, lo que cambiaría las reglas pedidas.
- **(Versión 4)** El descanso de la fase 2 (0,8 s) es menor que el "al menos un segundo" del Prompt 3. Lo pidió el Prompt 4, y los avisos de 0,75 s se mantienen para que siga siendo esquivable.
- **(Versión 4)** El indicador del ataque dice "recargando" en la pausa y al terminar la partida. En realidad está bloqueado, no recargando.
- **(Versión 3)** Tocar un enemigo no empuja al robot hacia atrás. Si se queda encima del enemigo después de parpadear, pierde otro corazón.
- **(Versión 3)** Detrás del jefe hay un espacio de 40 px cuando está en su extremo derecho. Si el robot salta por encima y se queda ahí, el jefe se da vuelta y le dispara hacia ese lado.
- **(Versión 5)** Agacharse solo esquiva la ráfaga. Los proyectiles bajos van por el suelo y se esquivan saltando o con el propulsor.
- **(Versión 5)** El propulsor permite cruzar los huecos y saltarse partes del nivel. Es la "ayuda adicional" pedida. El recorrido sigue siendo posible solo con saltos normales (comprobado).
- **(Versión 5)** Si se mantiene S al bajar de una plataforma caminando, el robot sigue agachado en el aire (no se agacha en el aire, pero tampoco se levanta solo mientras la tecla siga presionada).
- **(Versión 5)** Con el paso fijo, si la computadora va a menos de ~4 FPS (más de 0,25 s por cuadro), el juego se ve más lento en vez de saltar hacia adelante. Es intencional.
- **(Versión 5)** Durante la partida se oculta el cursor del sistema y se dibuja la mira. En los menús vuelve el cursor normal.
- **(Versión 6)** El combate dura bastante más: son 100 impactos (40 + 60). El jugador automático tardó unos 30 s en la arena; una persona tardará más.
- **(Versión 6)** El abanico siempre sale desde la horizontal hacia arriba. Agacharse lo esquiva desde el suelo, pero si NEXO-7 vuela alto puede quedar en la trayectoria de los rayos superiores.
- **(Versión 6)** Durante la transición, los pulsos atraviesan al jefe sin hacerle daño y no desaparecen. Se puede seguir disparando, pero no sirve.
- **(Versión 6)** El propulsor recarga de forma proporcional al tiempo apoyado: desde vacío, 1,5 s de contacto lo llenan; si despega antes, conserva la parte recargada.
- **(Versión 6)** Los nombres de las versiones anteriores (VOLTARÓN, "el robot") quedaron en la historia de este README a propósito, como evidencia de cada iteración.
- **(Versión 7)** Las pruebas manuales 1 a 65 son de las versiones anteriores (plataformas, baterías, portal). Quedan como historia; para la versión actual valen la 35 a la 57 (menús, pausa, apuntado, agacharse, propulsor) y las 66 a 76.
- **(Versión 7)** La dificultad se comprobó con un jugador automático que ve todos los proyectiles y reacciona en cada paso; para una persona será más difícil. El Serafín le tomó 122 s, porque sus ventanas de ataque son cortas.
- **(Versión 7)** Contra el Embestidor, agacharse solo sirve si NEXO-7 estaba de pie cuando salió el abanico; muy cerca del jefe (a menos de ~220 px), el rayo inferior también alcanza al robot agachado.
- **(Versión 7)** El abanico descendente del Serafín tiene huecos de unos 35 px entre rayos al llegar al suelo. Alejarse a más de ~220 px de su vertical es más seguro que buscar el hueco.
- **(Versión 7)** El progreso se guarda junto al código (`progreso.json`). Si la carpeta es de solo lectura, el juego sigue funcionando, pero avisa que no pudo guardar.
- **(Versión 7)** `requirements.txt` pide `pygame-ce` (antes pedía `pygame`, que no se instalaba en Python 3.14). Todas las pruebas se ejecutaron también con pygame 2.6.1, así que el código funciona con los dos.
- **(Versión 7)** El superataque hace que cada 10 aciertos el daño total suba en 5 (un 50 % más). Los combates pueden sentirse más cortos que antes.
- **Comprobado por el estudiante:** en su Mac, con el ajuste final, la embestida del Embestidor ya se puede esquivar, y lo venció.
- **Pendiente:** el resto de las pruebas manuales 66 a 80, y comprobar que la curva de dificultad de los tres jefes sea justa para una persona.

## Reflexión final

*Escrita por el estudiante.*

**¿Qué aprendí usando IA para programar?**
Lo que yo aprendí es que es una herramienta que ayuda mucho a que uno pueda trabajar sus ideas y las pueda realizar, sin tener mayor conocimiento de la programación.

**¿Qué ventajas y límites le vi al vibecoding?**
La ventaja es que con lenguaje natural uno puede manejar un tipo de lenguaje muy técnico y específico. Los límites son que siempre hay detalles que están fuera del alcance de una persona natural y del mismo código. Por lo tanto, siempre es importante ir revisando el resultado para ir iterando hasta pulir esos detalles.

**¿Qué partes del código entiendo y cuáles necesito reforzar?**
Prácticamente logro comprender la mayoría del código. La estructura del proyecto es algo que yo mismo sugerí, para tener todo de una manera más organizada: las configuraciones, el manejo del propio juego, lo que coordina las pantallas, junto con las demás funciones que ya están establecidas, con tal de llevar todo de manera modular.

Logro comprender cómo se definen las variables, cómo se forman las funciones, cómo se llaman y cómo se importan módulos, como por ejemplo `pygame`, `sys` y `math`, que son importantes para poder crear el juego. Ya tengo una base de conocimiento de programación.

Lo que sí necesitaría reforzar son ciertas palabras reservadas que sirven para llamar funciones de algún tipo específico.
