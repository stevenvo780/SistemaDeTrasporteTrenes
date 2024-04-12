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
        self.destino = self.encontrar_destino(self.ubicacion)  # Se pasa la ubicación como parámetro

    def mover(self):
        if self.en_metro:
            self.ubicacion = copy.deepcopy(self.tren_actual.posicion_tren)
            if self.esta_cerca(self.ubicacion, self.destino):
                self.bajarse_del_tren()
        else:
            if self.tiempo_llegada and time.time() - self.tiempo_llegada < 10:
                return
            estacion_cercana = self.encontrar_estacion_mas_cercana()
            self.mover_hacia_punto(estacion_cercana)
            if self.esta_en_estacion(estacion_cercana):
                self.subir_a_tren(estacion_cercana)

    def mover_hacia_punto(self, punto):
        dx, dy = punto[0] - self.ubicacion[0], punto[1] - self.ubicacion[1]
        distancia = (dx**2 + dy**2)**0.5
        if distancia > VELOCIDAD_AGENTES:
            dx, dy = dx / distancia * VELOCIDAD_AGENTES, dy / distancia * VELOCIDAD_AGENTES
        self.ubicacion[0] += dx
        self.ubicacion[1] += dy

    def esta_en_estacion(self, estacion):
        return self.esta_cerca(self.ubicacion, estacion)

    def encontrar_estacion_mas_cercana(self):
        min_distancia = float('inf')
        estacion_cercana = None
        for linea in self.simulacion.lineas_metro:
            for estacion in linea.estaciones_ida + linea.estaciones_vuelta:
                distancia = (
                    (self.ubicacion[0] - estacion[0])**2 + (self.ubicacion[1] - estacion[1])**2)**0.5
                if distancia < min_distancia:
                    min_distancia = distancia
                    estacion_cercana = estacion
        return estacion_cercana

    def esta_cerca(self, pos1, pos2, umbral=10):
        return abs(pos1[0] - pos2[0]) < umbral and abs(pos1[1] - pos2[1]) < umbral

    def subir_a_tren(self, estacion):
        tren_mas_cercano, direccion_correcta = self.encontrar_tren_mas_cercano_y_direccion()
        if tren_mas_cercano and self.esta_cerca(estacion, tren_mas_cercano.posicion_tren) and direccion_correcta:
            self.en_metro = True
            self.tren_actual = tren_mas_cercano
            tren_mas_cercano.agentes.append(self)

    def encontrar_tren_mas_cercano_y_direccion(self):
        min_distancia = float('inf')
        tren_cercano = None
        direccion_correcta = False
        for linea in self.simulacion.lineas_metro:
            for tren in linea.trenes:
                distancia = self.calcular_distancia(
                    tren.posicion_tren, self.ubicacion)
                if distancia < min_distancia:
                    tren_cercano = tren
                    min_distancia = distancia

        if tren_cercano:
            indice_estacion_actual = self.encontrar_indice_estacion_mas_cercana(
                tren_cercano)
            indice_destino = self.obtener_indice_destino(tren_cercano)
            direccion_correcta = (indice_destino > indice_estacion_actual and tren_cercano.direccion == 1) or \
                                 (indice_destino <
                                  indice_estacion_actual and tren_cercano.direccion == -1)

        return tren_cercano, direccion_correcta

    def obtener_indice_destino(self, tren):
        # Obtener el índice del destino en la ruta del tren
        try:
            return tren.estaciones_actuales.index(self.destino)
        except ValueError:
            return -1

    def es_direccion_correcta(self, tren):
        if self.destino not in tren.estaciones_actuales:
            return False
        indice_estacion_actual = self.encontrar_indice_estacion_mas_cercana(
            tren)
        indice_destino = tren.estaciones_actuales.index(self.destino)
        return (indice_destino > indice_estacion_actual and tren.direccion == 1) or \
               (indice_destino < indice_estacion_actual and tren.direccion == -1)

    def calcular_distancia(self, pos1, pos2):
        return ((pos1[0] - pos2[0])**2 + (pos1[1] - pos2[1])**2)**0.5

    def encontrar_indice_estacion_mas_cercana(self, tren):
        min_distancia = float('inf')
        indice_mas_cercano = -1
        for i, estacion in enumerate(tren.estaciones_actuales):
            distancia = ((tren.posicion_tren[0] - estacion[0]) **
                         2 + (tren.posicion_tren[1] - estacion[1])**2)**0.5
            if distancia < min_distancia:
                min_distancia = distancia
                indice_mas_cercano = i
        return indice_mas_cercano

    def encontrar_destino(self):
        # Elegir un destino que esté en la ruta del tren más cercano
        tren_cercano, direccion_correcta = self.encontrar_tren_mas_cercano_y_direccion()
        if tren_cercano and direccion_correcta:
            return random.choice(tren_cercano.estaciones_actuales)
        else:
            # Si no hay trenes cercanos o la dirección no es correcta, elegir cualquier estación
            linea = random.choice(self.simulacion.lineas_metro)
            return random.choice(linea.estaciones_ida + linea.estaciones_vuelta)

    def encontrar_tren_mas_cercano(self):
        min_distancia = float('inf')
        tren_cercano = None
        for linea in self.simulacion.lineas_metro:
            for tren in linea.trenes:
                distancia = ((tren.posicion_tren[0] - self.ubicacion[0])**2 + (
                    tren.posicion_tren[1] - self.ubicacion[1])**2)**0.5
                if distancia < min_distancia:
                    min_distancia = distancia
                    tren_cercano = tren
        return tren_cercano

    def bajarse_del_tren(self):
        self.tren_actual.agentes.remove(self)
        self.en_metro = False
        self.tren_actual = None
        self.tiempo_llegada = time.time()
        self.destino = self.encontrar_destino()
