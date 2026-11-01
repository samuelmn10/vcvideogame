"""Detección y resolución de colisiones compartidas por varias entidades."""


def resolver_horizontal(rect, dx, solidos):
    """Mueve el rectángulo en X y, si choca con un sólido, lo pega a su borde."""
    rect.x += dx
    for solido in solidos:
        if rect.colliderect(solido):
            if dx > 0:
                rect.right = solido.left
            elif dx < 0:
                rect.left = solido.right


def resolver_vertical(rect, vel_y, solidos):
    """Mueve el rectángulo en Y y resuelve choques con el suelo o con techos.

    Devuelve (nueva_vel_y, apoyo): apoyo es el sólido sobre el que aterrizó, o None.
    """
    rect.y += vel_y
    apoyo = None
    for solido in solidos:
        if rect.colliderect(solido):
            if vel_y > 0:
                # Venía cayendo: aterriza encima del sólido
                rect.bottom = solido.top
                apoyo = solido
            elif vel_y < 0:
                # Venía subiendo: se golpea la cabeza por debajo
                rect.top = solido.bottom
            vel_y = 0
    return vel_y, apoyo


def limitar_horizontal(rect, ancho_mundo):
    """No permite salir por los extremos izquierdo y derecho."""
    rect.left = max(rect.left, 0)
    rect.right = min(rect.right, ancho_mundo)


def toca_alguno(rect, rects):
    return rect.collidelist(rects) != -1


def hay_espacio(rect, solidos):
    """True si el rectángulo cabe sin tocar sólidos ni salir por arriba."""
    return rect.top >= 0 and not toca_alguno(rect, solidos)
