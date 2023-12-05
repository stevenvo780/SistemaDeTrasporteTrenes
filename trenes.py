import time
import copy

class Tren:
    def __init__(self, estaciones, capacidad, velocidad):
        self.estaciones = estaciones
        self.capacidad = capacidad
        self.posicion_tren = copy.deepcopy(estaciones[0])
        self.siguiente_estacion = 1
        self.direccion = 1
        self.velocidad = velocidad * 5   # Velocidad de movimiento entre estaciones
        self.tiempo_parada = 5  # Tiempo de parada en cada estación en segundos
        self.ultimo_tiempo_parada = time.time()
        self.agentes = []

    def mover_tren(self):
        if time.time() - self.ultimo_tiempo_parada < self.tiempo_parada:
            # Si aún está en tiempo de parada, no mover el tren
            return

        destino = self.estaciones[self.siguiente_estacion]
        dx, dy = destino[0] - self.posicion_tren[0], destino[1] - self.posicion_tren[1]
        distancia = (dx**2 + dy**2)**0.5

        if distancia < self.velocidad:
            # Si el tren está muy cerca de la estación, considerarlo como llegada
            self.posicion_tren = [destino[0], destino[1]]  # Crea una nueva lista en lugar de referenciar la estación
            self.ultimo_tiempo_parada = time.time()
            self.siguiente_estacion += self.direccion

            # Cambiar la dirección si es necesario
            if self.siguiente_estacion >= len(self.estaciones) or self.siguiente_estacion < 0:
                self.direccion *= -1
                self.siguiente_estacion += self.direccion * 2
        else:
            # Mover el tren hacia la siguiente estación
            paso_x, paso_y = dx / distancia * self.velocidad, dy / distancia * self.velocidad
            self.posicion_tren[0] += paso_x
            self.posicion_tren[1] += paso_y
