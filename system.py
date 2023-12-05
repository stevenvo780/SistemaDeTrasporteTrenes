import pygame
import random
from lineaMetro import LineaMetro
from agente import Agente
from constantes import NUM_LINEAS_METRO, NUM_AGENTES, TAMANO_ESPACIO, CAPACIDAD_TREN
import time

class SimulacionMetro:
    def __init__(self):
        self.ventana, self.reloj = self.inicializar_pygame()
        self.lineas_metro = [LineaMetro(num_estaciones=5, num_trenes=3, capacidad_tren=CAPACIDAD_TREN, tamano_espacio=TAMANO_ESPACIO) for _ in range(NUM_LINEAS_METRO)]
        self.agentes = self.inicializar_agentes()
        self.ejecutando = True

    def inicializar_agentes(self):
        agentes = [Agente(self, id, [random.randint(0, TAMANO_ESPACIO), random.randint(0, TAMANO_ESPACIO)]) for id in range(NUM_AGENTES)]
        return agentes

    def inicializar_pygame(self):
        pygame.init()
        ventana = pygame.display.set_mode((TAMANO_ESPACIO, TAMANO_ESPACIO))
        pygame.display.set_caption("Simulación del Sistema de Metro")
        return ventana, pygame.time.Clock()

    def dibujar_simulacion(self):
        self.ventana.fill((255, 255, 255))
        for linea in self.lineas_metro:
            for i in range(len(linea.estaciones) - 1):
                pygame.draw.line(self.ventana, (0, 0, 255), linea.estaciones[i], linea.estaciones[i+1], 2)

            for tren in linea.trenes:
                # Usar directamente la posición actual del tren para dibujarlo
                estacion_con_tren = tren.posicion_tren
                pygame.draw.rect(self.ventana, (0, 255, 0), [estacion_con_tren[0] - 10, estacion_con_tren[1] - 10, 20, 20])

        for agente in self.agentes:
            color = (235, 0, 0) if not agente.en_metro else (0, 235, 0)
            pygame.draw.circle(self.ventana, color, agente.ubicacion, 5)


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