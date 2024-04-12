import pygame
import random
from lineaMetro import LineaMetro
from agente import Agente
from constantes import NUM_LINEAS_METRO, NUM_AGENTES, TAMANO_ESPACIO, CAPACIDAD_TREN
import time

class SimulacionMetro:
    def __init__(self):
        self.ventana, self.reloj = self.inicializar_pygame()
        self.lineas_metro = [LineaMetro(num_estaciones=5, num_trenes=3, capacidad_tren=CAPACIDAD_TREN,
                                        tamano_espacio=TAMANO_ESPACIO) for _ in range(NUM_LINEAS_METRO)]
        self.agentes = self.inicializar_agentes()
        self.ejecutando = True

    def inicializar_agentes(self):
        agentes = [Agente(self, id, [random.randint(0, TAMANO_ESPACIO), random.randint(
            0, TAMANO_ESPACIO)]) for id in range(NUM_AGENTES)]
        return agentes

    def inicializar_pygame(self):
        pygame.init()
        ventana = pygame.display.set_mode((TAMANO_ESPACIO, TAMANO_ESPACIO))
        pygame.display.set_caption("Simulación del Sistema de Metro")
        return ventana, pygame.time.Clock()

    def dibujar_simulacion(self):
        self.ventana.fill((255, 255, 255))

        for linea in self.lineas_metro:
            # Dibujar ruta de ida
            for i in range(len(linea.estaciones_ida) - 1):
                pygame.draw.line(self.ventana, (0, 0, 255), linea.estaciones_ida[i], linea.estaciones_ida[i+1], 2)
                pygame.draw.circle(self.ventana, (0, 0, 255), linea.estaciones_ida[i], 5)  # Dibujar estaciones

            # Dibujar ruta de vuelta
            for i in range(len(linea.estaciones_vuelta) - 1):
                pygame.draw.line(self.ventana, (255, 0, 0), linea.estaciones_vuelta[i], linea.estaciones_vuelta[i+1], 2)
                pygame.draw.circle(self.ventana, (255, 0, 0), linea.estaciones_vuelta[i], 5)  # Dibujar estaciones

            # Dibujar trenes
            for tren in linea.trenes:
                color_tren = (0, 255, 0) if tren.estaciones_actuales == tren.estaciones_ida else (255, 255, 0)
                pygame.draw.rect(self.ventana, color_tren, [tren.posicion_tren[0] - 10, tren.posicion_tren[1] - 10, 20, 20])

        # Dibujar agentes
        for agente in self.agentes:
            color_agente = (235, 255, 0) if not agente.en_metro else (0, 235, 255)
            pygame.draw.circle(self.ventana, color_agente, agente.ubicacion, 5)

        pygame.display.flip()

    def ejecutar(self):
        while self.ejecutando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.ejecutando = False

            for linea in self.lineas_metro:
                linea.mover_trenes()

            for agente in self.agentes:
                agente.mover()

            self.dibujar_simulacion()
            pygame.display.flip()
            self.reloj.tick(60)

        pygame.quit()


# Ejecutar la simulación
simulacion = SimulacionMetro()
simulacion.ejecutar()
