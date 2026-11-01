# RoboAventura

Mini-juego de plataformas 2D hecho en Python con Pygame. Es una actividad de **vibecoding**: el juego se desarrolló con IA como copiloto, a partir de prompts progresivos.

Un robot recorre un nivel de plataformas recogiendo baterías y esquivando o eliminando enemigos con un pulso de energía. El portal del final lo lleva a una arena donde debe vencer al jefe **VOLTARÓN**. Tiene tres corazones. El juego se maneja con menús de botones: inicio, pausa y fin de partida.

## Cómo ejecutarlo

Requisitos: Python 3.10 o superior.

```bash
pip install -r requirements.txt
```

```bash
python main.py
```

> **Si la instalación falla con Python 3.14** (error `'SDL.h' file not found`): pygame 2.6.1 todavía no tiene versión lista para Python 3.14. Instala `pygame-ce`, que se usa igual con `import pygame`:
>
> ```bash
> pip install pygame-ce
> ```

## Controles

| Tecla | Acción |
|---|---|
| A / D o flechas ← → | Moverse |
| Espacio | Saltar |
| J (se puede mantener presionada) | Lanzar pulsos de energía (uno cada 0,3 s, máximo 2 en pantalla) |
| Clic izquierdo | Botones: Iniciar, Pausa, Continuar, Reiniciar, Volver a jugar y Salir |

Desde la versión 4, R y Escape ya no se usan. Para reiniciar o salir se usan los botones, y la ventana también se puede cerrar con su botón de cierre.

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

## Validación

### Pruebas realizadas por la IA (automáticas, sin ventana)

Se ejecutó un script con Pygame en modo sin pantalla que simula teclas y revisa el estado del juego.

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

1. **Instalación en macOS con Python 3.14:** `pip install -r requirements.txt` falló con `'SDL.h' file not found`, porque pygame 2.6.1 no tiene versión para Python 3.14 e intentó compilarse. **Ajuste:** se instaló `pygame-ce`, que es compatible y no requiere cambiar el código. Se agregó la nota en "Cómo ejecutarlo".
2. **El pulso pasaba 2 px de su alcance:** avanzaba de 8 en 8 y 350 no es múltiplo de 8, así que llegaba a 352 px. Lo detectó una prueba automática. **Ajuste:** el último paso se recorta a lo que falta.
3. **La regla de "máximo 2 pulsos" no tenía efecto:** con velocidad 10, el pulso desaparecía en 35 cuadros, antes de que terminara la espera de 36. **Ajuste:** se bajó la velocidad a 8 (el pulso dura unos 44 cuadros).
4. **El indicador decía "listo" después de perder,** aunque el ataque estaba bloqueado. Se vio en una captura. **Ajuste:** `puede_atacar()` también revisa que la partida siga en curso.
5. **(Versión 3) Reaparecer al filo del hueco:** al principio, la posición segura era el último lugar donde el robot estuvo apoyado, que muchas veces es el borde del hueco. Una prueba mostró que, con la tecla todavía presionada, el robot volvía a caer enseguida y perdía otro corazón. **Ajuste:** solo se guarda una posición con al menos 100 px de suelo a cada lado (`MARGEN_SEGURO`). Para eso el jugador ahora recuerda sobre qué sólido está parado (`apoyo`).
6. **(Versión 4) Textos encimados en la pausa:** en una captura, el anuncio "FASE 2" quedaba detrás del título "Pausa". **Ajuste:** el anuncio solo se dibuja mientras se juega. Como su tiempo no corre en pausa, sigue visible al continuar.

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
- **Pendiente:** jugar las versiones 2, 3 y 4 con ventana, teclado y ratón reales (pruebas manuales 10 a 45).

## Reflexión final

_Pendiente: la escribe el estudiante._
