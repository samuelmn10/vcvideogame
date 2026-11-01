"""Cálculos de desplazamiento: dirección horizontal, gravedad, salto y propulsión."""

import config as c


def alguna_presionada(teclas, grupo):
    return any(teclas[tecla] for tecla in grupo)


def desplazamiento_horizontal(teclas, velocidad):
    """Píxeles a mover en X este paso según las teclas (izquierda y derecha se anulan)."""
    dx = 0
    if alguna_presionada(teclas, c.TECLAS_IZQUIERDA):
        dx -= velocidad
    if alguna_presionada(teclas, c.TECLAS_DERECHA):
        dx += velocidad
    return dx


def aplicar_gravedad(vel_y):
    return min(vel_y + c.GRAVEDAD, c.VELOCIDAD_CAIDA_MAX)


def aplicar_propulsor(vel_y):
    """La gravedad sigue actuando, pero el empuje la supera hasta una subida máxima."""
    return max(vel_y + c.GRAVEDAD - c.EMPUJE_PROPULSOR, -c.VELOCIDAD_SUBIDA_MAX)


def velocidad_de_salto():
    return c.VELOCIDAD_SALTO
