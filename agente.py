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
        self.tiempo_llegada = None  # Tiempo cuando el agente se baja del tren
        self.destino = self.encontrar_destino()

    def mover(self):
        if self.en_metro:
            # Actualizar ubicación del agente a la del tren directamente
            self.ubicacion = copy.deepcopy(self.tren_actual.posicion_tren)
            if self.esta_cerca(self.ubicacion, self.destino):
                self.bajarse_del_tren()
        else:
            if self.tiempo_llegada is not None and time.time() - self.tiempo_llegada < 10:
                # Esperar 10 segundos antes de buscar una nueva ubicación
                return

            estacion_cercana = self.encontrar_estacion_mas_cercana()
            self.mover_hacia_punto(estacion_cercana)

            if self.esta_en_estacion(estacion_cercana):
                self.subir_a_tren(estacion_cercana)

            # Una vez que comienza a moverse, resetear tiempo_llegada
            self.tiempo_llegada = None

    def mover_hacia_punto(self, punto):
        # Implementar lógica de movimiento hacia un punto
        dx, dy = punto[0] - self.ubicacion[0], punto[1] - self.ubicacion[1]
        distancia = (dx**2 + dy**2)**0.5
        if distancia > VELOCIDAD_AGENTES:
            dx, dy = dx / distancia * VELOCIDAD_AGENTES, dy / distancia * VELOCIDAD_AGENTES

        self.ubicacion[0] += dx
        self.ubicacion[1] += dy

    def esta_en_estacion(self, estacion):
        return self.esta_cerca(self.ubicacion, estacion)

    def encontrar_indice_estacion_mas_cercana(self, tren):
        # Encontrar la estación más cercana a la posición actual del tren
        min_distancia = float('inf')
        indice_mas_cercano = -1
        for i, estacion in enumerate(tren.estaciones_actuales):
            distancia = ((tren.posicion_tren[0] - estacion[0]) ** 2 + (tren.posicion_tren[1] - estacion[1]) ** 2) ** 0.5
            if distancia < min_distancia:
                min_distancia = distancia
                indice_mas_cercano = i
        return indice_mas_cercano

    def es_direccion_correcta(self, tren):
        # Determinar si el tren va en la dirección correcta
        indice_estacion_actual = self.encontrar_indice_estacion_mas_cercana(tren)
        indice_destino = tren.estaciones_actuales.index(self.destino)

        # Comprobar la dirección del tren en relación con la posición del destino
        return (indice_destino > indice_estacion_actual and tren.direccion == 1) or \
               (indice_destino < indice_estacion_actual and tren.direccion == -1)

    def subir_a_tren(self, estacion):
        for linea in self.simulacion.lineas_metro:
            for tren in linea.trenes:
                if self.esta_cerca(tren.posicion_tren, estacion) and \
                   len(tren.agentes) < tren.capacidad and \
                   self.es_direccion_correcta(tren):
                    self.en_metro = True
                    self.tren_actual = tren
                    tren.agentes.append(self)
                    return

    def bajarse_del_tren(self):
        self.tren_actual.agentes.remove(self)
        self.en_metro = False
        self.tren_actual = None
        self.tiempo_llegada = time.time()  # Registrar el momento de bajada
        self.destino = self.encontrar_destino()

    def esta_cerca(self, pos1, pos2, umbral=10):
        return abs(pos1[0] - pos2[0]) < umbral and abs(pos1[1] - pos2[1]) < umbral

    def encontrar_estacion_mas_cercana(self):
        # Lógica para encontrar la estación más cercana de todas las estaciones
        min_distancia = float('inf')
        estacion_cercana = None
        for linea in self.simulacion.lineas_metro:
            for estacion in linea.estaciones_ida + linea.estaciones_vuelta:
                distancia = ((self.ubicacion[0] - estacion[0])**2 + (self.ubicacion[1] - estacion[1])**2)**0.5
                if distancia < min_distancia:
                    min_distancia = distancia
                    estacion_cercana = estacion
        return estacion_cercana

    def encontrar_destino(self):
        # Elegir aleatoriamente entre estaciones de ida y vuelta
        linea = random.choice(self.simulacion.lineas_metro)
        if random.choice([True, False]):  # Elegir aleatoriamente entre ida y vuelta
            return random.choice(linea.estaciones_ida)
        else:
            return random.choice(linea.estaciones_vuelta)

