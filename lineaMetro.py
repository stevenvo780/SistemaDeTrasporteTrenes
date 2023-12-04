# Agente
from constantes import TAMANO_ESPACIO
import random
from trenes import Tren


class LineaMetro:
    def __init__(self, num_estaciones, num_trenes, capacidad_tren, tamano_espacio):
        self.estaciones = self.generar_estaciones(
            num_estaciones, tamano_espacio)
        self.trenes = [Tren(self.estaciones, capacidad_tren)
                       for _ in range(num_trenes)]

    def generar_estaciones(self, num_estaciones, tamano_espacio):
        return [[random.randint(0, tamano_espacio), random.randint(0, tamano_espacio)] for _ in range(num_estaciones)]

    def mover_trenes(self):
        for tren in self.trenes:
            tren.mover_tren()
