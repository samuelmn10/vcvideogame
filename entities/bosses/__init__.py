"""Lista de jefes en el orden de la campaña (dificultad creciente).

Para agregar un jefe: se crea su módulo en esta carpeta (heredando de JefeBase)
y se agrega aquí su clase.
"""

from entities.bosses.centinela import CentinelaEclipse
from entities.bosses.embestidor import EmbestidorFerreo
from entities.bosses.serafin import SerafinVoltaico

JEFES = [CentinelaEclipse, EmbestidorFerreo, SerafinVoltaico]
