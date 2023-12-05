import random
from constantes import VELOCIDAD_AGENTES
import copy
import time


class Agente:
    def __init__(self, simulacion, id, ubicacion):
        self.simulacion = simulacion
        self.id = id
        self.ubicacion = ubicacion.copy()
        self.en_metro = False
        self.tren_actual = None
        self.tiempo_llegada = None
        self.destino = self.encontrar_destino()

    def mover(self):
        if not self.en_metro:
            estacion_cercana = self.encontrar_estacion_mas_cercana()
            self.mover_hacia_punto(estacion_cercana)

            if self.esta_en_estacion(estacion_cercana):
                self.subir_a_tren(estacion_cercana)

        elif self.en_metro:
            # Actualizar ubicación del agente a la del tren directamente
            self.ubicacion = copy.deepcopy(self.tren_actual.posicion_tren)
            if self.esta_cerca(self.ubicacion, self.destino):
                self.bajarse_del_tren()

    def mover_hacia_punto(self, punto):
        # Implementar lógica de movimiento hacia un punto
        dx, dy = punto[0] - self.ubicacion[0], punto[1] - self.ubicacion[1]
        distancia = (dx**2 + dy**2)**0.5
        if distancia > VELOCIDAD_AGENTES:
            dx, dy = dx / distancia * VELOCIDAD_AGENTES, dy / distancia * VELOCIDAD_AGENTES

        self.ubicacion[0] += dx
        self.ubicacion[1] += dy

    def esta_en_estacion(self, estacion):
        return self.ubicacion == estacion

    def subir_a_tren(self, estacion):
        for linea in self.simulacion.lineas_metro:
            for tren in linea.trenes:
                if self.esta_cerca(tren.posicion_tren, estacion) and len(tren.agentes) < tren.capacidad:
                    self.en_metro = True
                    self.tren_actual = tren
                    tren.agentes.append(self)
                    return

    def esta_cerca(self, pos1, pos2, umbral=10):
        return abs(pos1[0] - pos2[0]) < umbral and abs(pos1[1] - pos2[1]) < umbral

    def bajarse_del_tren(self):
        self.tren_actual.agentes.remove(self)
        self.en_metro = False
        self.tren_actual = None
        self.destino = self.encontrar_destino()

    def encontrar_estacion_mas_cercana(self):
        # Lógica para encontrar la estación más cercana
        min_distancia = float('inf')
        estacion_cercana = None
        for linea in self.simulacion.lineas_metro:
            for estacion in linea.estaciones:
                distancia = (
                    (self.ubicacion[0] - estacion[0])**2 + (self.ubicacion[1] - estacion[1])**2)**0.5
                if distancia < min_distancia:
                    min_distancia = distancia
                    estacion_cercana = estacion
        return estacion_cercana

    def encontrar_destino(self):
        # Lógica para determinar un destino aleatorio
        linea = random.choice(self.simulacion.lineas_metro)
        return random.choice(linea.estaciones)
