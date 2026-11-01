"""Progreso guardado en un archivo JSON local: jefes desbloqueados y victorias.

Formato del archivo:
    {"desbloqueados": 1, "victorias": [0, 0, 0]}
"desbloqueados" es cuántos jefes se pueden elegir (1 a N) y "victorias" cuenta
las veces que se venció a cada jefe. No se guarda nada más.
"""

import json
import os


class Progreso:
    def __init__(self, ruta, cantidad_jefes):
        self.ruta = ruta
        self.cantidad = cantidad_jefes
        self.aviso = ""  # mensaje para el menú si hubo que restablecer el progreso
        self.desbloqueados = 1
        self.victorias = [0] * cantidad_jefes
        self.cargar()

    # ----- Archivo ----------------------------------------------------------
    def cargar(self):
        if not os.path.exists(self.ruta):
            return  # primera vez: progresión nueva
        try:
            with open(self.ruta, encoding="utf-8") as archivo:
                datos = json.load(archivo)
            self.desbloqueados, self.victorias = self.validar(datos)
        except (OSError, ValueError, TypeError, KeyError):
            # Archivo dañado: no se cierra el juego; se empieza de nuevo y se avisa
            self.desbloqueados = 1
            self.victorias = [0] * self.cantidad
            self.aviso = "El archivo de progreso estaba dañado: se restableció el progreso."
            self.guardar()

    def validar(self, datos):
        """Revisa tipos y rangos; si algo no cuadra, lanza ValueError."""
        desbloqueados = datos["desbloqueados"]
        victorias = datos["victorias"]
        if type(desbloqueados) is not int or not 1 <= desbloqueados <= self.cantidad:
            raise ValueError("desbloqueados fuera de rango")
        if (not isinstance(victorias, list) or len(victorias) != self.cantidad
                or any(type(v) is not int or v < 0 for v in victorias)):
            raise ValueError("victorias inválidas")
        return desbloqueados, victorias

    def guardar(self):
        """Escribe primero un archivo temporal y después lo reemplaza: si el juego
        se cierra a la mitad, el archivo anterior queda entero."""
        datos = {"desbloqueados": self.desbloqueados, "victorias": self.victorias}
        temporal = self.ruta + ".tmp"
        try:
            with open(temporal, "w", encoding="utf-8") as archivo:
                json.dump(datos, archivo, indent=2)
            os.replace(temporal, self.ruta)
        except OSError:
            self.aviso = "No se pudo guardar el progreso en el disco."

    # ----- Consultas y cambios ----------------------------------------------
    def desbloqueado(self, indice):
        return indice < self.desbloqueados

    def derrotado(self, indice):
        return self.victorias[indice] > 0

    def registrar_victoria(self, indice):
        """Suma la victoria y desbloquea el siguiente jefe (perder no quita nada)."""
        self.victorias[indice] += 1
        self.desbloqueados = max(self.desbloqueados, min(indice + 2, self.cantidad))
        self.guardar()
