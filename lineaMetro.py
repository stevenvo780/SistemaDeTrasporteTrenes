import random
import copy
from trenes import Tren
from constantes import VELOCIDAD_TREN

class LineaMetro:
    def __init__(self, num_estaciones, num_trenes, capacidad_tren, tamano_espacio):
        estaciones_ida, estaciones_vuelta = self.generar_estaciones(num_estaciones, tamano_espacio)
        self.estaciones_ida = estaciones_ida
        self.estaciones_vuelta = estaciones_vuelta
        self.trenes = [Tren(self.estaciones_ida, self.estaciones_vuelta, capacidad_tren, VELOCIDAD_TREN) for _ in range(num_trenes)]

    def generar_estaciones(self, num_estaciones, tamano_espacio):
        offset = 20  # Desplazamiento entre las líneas de ida y vuelta
        estaciones_ida = [[random.randint(0, tamano_espacio - offset), random.randint(0, tamano_espacio)] for _ in range(num_estaciones)]
        estaciones_vuelta = [[x + offset, y] for x, y in estaciones_ida]  # Desplazar las estaciones de vuelta

        return estaciones_ida, estaciones_vuelta

    def mover_trenes(self):
        for tren in self.trenes:
            tren.mover_tren()
