# RoboAventura

Mini-juego de plataformas 2D hecho en Python con Pygame. Es una actividad de **vibecoding**: el juego se desarrolló con IA como copiloto, a partir de prompts progresivos.

Un robot debe recoger baterías, esquivar a un enemigo y no caer en los huecos para llegar al portal de salida.

## Cómo ejecutarlo

Requisitos: Python 3.10 o superior.

```bash
pip install -r requirements.txt
```

```bash
python main.py
```

## Controles

| Tecla | Acción |
|---|---|
| A / D o flechas ← → | Moverse |
| Espacio | Saltar |
| R | Reiniciar (después de ganar o perder) |
| Escape | Salir |

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

### Prompt 2: _pendiente_

### Prompt 3: _pendiente_

---

## Cómo funciona (resumen técnico)

- **Movimiento:** cada cuadro se leen las teclas presionadas y el robot se desplaza 5 px a la izquierda o a la derecha.
- **Gravedad:** la velocidad vertical aumenta 1 px por cuadro, hasta un máximo de 15. Saltar la pone en −17, así que el robot sube unos 136 px y luego cae.
- **Colisiones:** primero se mueve en X y se corrige si choca con un sólido; después se mueve en Y. Si choca cayendo, aterriza (`en_suelo = True`). Si choca subiendo, se golpea la cabeza. Solo se puede saltar con `en_suelo = True`.
- **Cámara:** `camara_x` intenta centrar al robot, pero se limita entre 0 y 1920 (2880 − 960). Todo se dibuja restando `camara_x` a su posición.

## Validación

### Pruebas realizadas por la IA (automáticas, sin ventana)

Se ejecutó un script con Pygame en modo sin pantalla que simula teclas y revisa el estado del juego. Resultado: **14 de 14 correctas**.

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

También se generaron capturas de pantalla para revisar el dibujo del robot, el enemigo, las baterías, el portal y el mensaje de victoria.

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

### Limitaciones conocidas

- Las pruebas automáticas no reemplazan jugarlo: falta probarlo con ventana real y teclado.
- Un recorrido directo al portal toma unos 10–20 segundos (2880 px a 5 px por cuadro). Recoger las 6 baterías y esquivar al enemigo toma más, pero puede quedar por debajo del minuto pedido.
- La física avanza "por cuadro": si el equipo no alcanza 60 FPS, el juego se siente más lento.
- Debajo de la plataforma 5 el robot no puede saltar por encima del enemigo, porque se golpea la cabeza. Hay que esquivarlo antes o subir a la plataforma.

## Reflexión final

_Pendiente: la escribe el estudiante._
