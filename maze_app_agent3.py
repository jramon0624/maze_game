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

agents = [AgentT2(DORANGE)]
winner = AgentT2(DORANGE)


# Bucle principal
running = True
while running:
    new_agents_list = []

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Dibujar el laberinto
    for row in range(rows):
        for col in range(cols):
            if any([agent.position == [row,col] for agent in agents]):
                color = agents[0].color
            elif [row,col] == [0,0]:
                color = FGREEN
            elif goal == [row,col]:
                color = DARKRED
            else:
                color = COLORS.get(maze[row][col], DLGREY)  # DLGREY por defecto
            
            if winner.visited:
                if any([position == [row,col] for position in winner.visited]):
                    color = GOLD
            pygame.draw.rect(screen, color, (col * cell_size, row * cell_size, cell_size, cell_size))
    
    if not any([agent.position == goal for agent in agents]):
        agents_to_delete = []
        for agent in agents:
            maze[agent.position[0]][agent.position[1]] = 2
            agent.get_available(maze)

            new_agents = len(agent.pos_available) - 1

            agent.visited.append(agent.position)

            if new_agents == 0:
                agent.position = agent.pos_available[0]
            elif new_agents > 0:
                for position in agent.pos_available[1:]:
                    new_agent = AgentT2(DORANGE)
                    new_agent.position = position
                    new_agent.visited = agent.visited.copy()
                    new_agents_list.append(new_agent)
                
                agent.position = agent.pos_available[0]
            else:
                agents_to_delete.append(agent)
        
        for agent in agents_to_delete:
            agents.remove(agent)
        
        for agent in new_agents_list:
            agents.append(agent)
    else:
        for agent in agents:
            if agent.position == goal:
                winner = agent

    pygame.display.flip()
    clock.tick(999)

pygame.quit()
sys.exit()

