import pygame
import sys
import random as rd
from entities import MazeGenerator
from cons import *
    
clock = pygame.time.Clock()

# Ejemplo de uso
cell_size = WINDOW_SIZE//N_CELLS
cols = N_CELLS
rows = N_CELLS
widht = cols * cell_size
height = rows * cell_size
values = [0,1,2]
matrix = [[0 for _ in range(cols)] for _ in range(rows)]

agente = MazeGenerator()

# Inicialización de Pygame
pygame.init()

# Configuración de la ventana
screen = pygame.display.set_mode((widht, height))
pygame.display.set_caption("Dibujar Cuadrícula")

visited = []
long_way = 0

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Dibujar la cuadrícula
    for row in range(rows):
        for col in range(cols):
            if agente.position == [row,col]:
                color = agente.color
            elif agente.goal == [row,col]:
                color = (128,0,0)
            else:
                color = COLORS.get(matrix[row][col], DLGREY)  # DLGREY por defecto
            pygame.draw.rect(screen, color, (col * cell_size, row * cell_size, cell_size, cell_size))

    # Dibujar bordes
    # for row in range(rows):
    #     for col in range(cols):
    #         pygame.draw.rect(screen, (128, 128, 128), (col * cell_size, row * cell_size, cell_size, cell_size), 1)

    pos_available = agente.get_available(matrix)
    next_pos = agente.position

    if pos_available:
        next_pos = rd.choice(pos_available)
        visited.append(agente.position.copy())
    elif visited:
        if long_way < len(visited):
            long_way = len(visited)
            agente.goal = agente.position.copy()
        agente.change_to_visited(matrix)
        next_pos = visited.pop()

    agente.move(next_pos, matrix)

    pygame.display.flip()
    clock.tick(600)

pygame.quit()
sys.exit()

