import pygame
import sys
import random as rd
from entities import AgentT1, AgentT2, AgentT3
from maze_generator import maze_generator
from cons import *
    
clock = pygame.time.Clock()

# Inicialización
n_cells = N_CELLS
cell_size = WINDOW_SIZE//N_CELLS
cols = n_cells
rows = n_cells

width = cols * cell_size
height = rows * cell_size

# Inicialización de Pygame
pygame.init()

# Configuración de la ventana
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Maze Game")

maze, goal = maze_generator(n_cells)

agent = AgentT3(DORANGE,goal)
# agent.get_best_path(maze)

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Dibujar el laberinto
    for row in range(rows):
        for col in range(cols):
            if agent.position == [row,col]:
                color = agent.color
            elif [row,col] == [0,0]:
                color = FGREEN
            elif goal == [row,col]:
                color = DARKRED
            else:
                color = COLORS.get(maze[row][col], DLGREY)  # DLGREY por defecto
            
            if agent.position == goal:
                if any([position == [row,col] for position in agent.tour]):
                    color = GOLD
            pygame.draw.rect(screen, color, (col * cell_size, row * cell_size, cell_size, cell_size))
    
    if not agent.position == goal:
        maze[agent.position[0]][agent.position[1]] = 2
        agent.move(maze,goal)           # Linea modificada

    pygame.display.flip()
    clock.tick(999)

pygame.quit()
sys.exit()

