class Tren:
    def __init__(self, estaciones, capacidad):
        self.estaciones = estaciones
        self.capacidad = capacidad
        self.posicion_tren = 0
        self.agentes = []
        self.direccion = 1

    def mover_tren(self):
        # Si el tren llega al final o al inicio, cambia de dirección
        if self.posicion_tren == len(self.estaciones) - 1 or self.posicion_tren == 0:
            self.direccion *= -1

        # Mueve el tren a la siguiente estación en la dirección actual
        self.posicion_tren += self.direccion
        self.posicion_tren = max(0, min(self.posicion_tren, len(self.estaciones) - 1))
