import time
import copy

class Tren:
    def __init__(self, estaciones_ida, estaciones_vuelta, capacidad, velocidad):
        self.estaciones_ida = estaciones_ida
        self.estaciones_vuelta = estaciones_vuelta
        self.estaciones_actuales = self.estaciones_ida  # Comienza en el riel de ida
        self.capacidad = capacidad
        self.posicion_tren = copy.deepcopy(self.estaciones_actuales[0])
        self.siguiente_estacion = 1
        self.direccion = 1
        self.velocidad = velocidad
        self.tiempo_parada = 2  # Tiempo de parada en cada estación en segundos
        self.ultimo_tiempo_parada = time.time()
        self.agentes = []

    def cambiar_riel(self):
        # Cambiar entre estaciones de ida y vuelta
        if self.estaciones_actuales == self.estaciones_ida:
            self.estaciones_actuales = self.estaciones_vuelta
        else:
            self.estaciones_actuales = self.estaciones_ida
        self.siguiente_estacion = 1  # Reiniciar el índice de la siguiente estación

    def mover_tren(self):
        if time.time() - self.ultimo_tiempo_parada < self.tiempo_parada:
            return

        destino = self.estaciones_actuales[self.siguiente_estacion]
        dx, dy = destino[0] - self.posicion_tren[0], destino[1] - self.posicion_tren[1]
        distancia = (dx**2 + dy**2)**0.5

        if distancia < self.velocidad:
            self.posicion_tren = [destino[0], destino[1]]
            self.ultimo_tiempo_parada = time.time()
            self.siguiente_estacion += 1

            if self.siguiente_estacion >= len(self.estaciones_actuales):
                self.cambiar_riel()
        else:
            paso_x, paso_y = dx / distancia * self.velocidad, dy / distancia * self.velocidad
            self.posicion_tren[0] += paso_x
            self.posicion_tren[1] += paso_y
