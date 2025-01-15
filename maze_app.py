import pygame
import sys
from entities import AgentT1, AgentT2, AgentT3
from maze_generator import maze_generator
from cons import *

# Inicialización
pygame.init()
clock = pygame.time.Clock()

# Parámetros
n_cells = N_CELLS
cell_size = WINDOW_SIZE // N_CELLS
cols = n_cells
rows = n_cells
width = cols * cell_size
height = rows * cell_size

# Colores
GRAY = (169, 169, 169)
LIGHT_GREEN = (144, 238, 144)
LIGHT_BLUE = (173, 216, 230)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Configuración de la ventana
screen = pygame.display.set_mode((width, height + 100))
pygame.display.set_caption("Maze Game")

# Generar el laberinto y agente
maze, goal = maze_generator(n_cells)
current_agent = AgentT3(DORANGE, goal)

# Fuente
font = pygame.font.Font(None, 36)

# Botones
button_start = pygame.Rect(10, height + 40 + 20, 100, 40)
button_pause = pygame.Rect(120, height + 40 + 20, 100, 40)
button_mode = pygame.Rect(230, height + 40 + 20, 150, 40)
button_speed_up = pygame.Rect(400, height + 40 + 20, 50, 40)
button_speed_down = pygame.Rect(460, height + 40 + 20, 50, 40)
input_size = pygame.Rect(520, height + 40 + 20, 100, 40)


# Opciones de modo de búsqueda
modes = ["AgentT1", "AgentT2", "AgentT3"]
current_mode_index = 2

# Estado de botones
start_label = "Iniciar"
pause_label = "Pausar"
size_locked = False
started = False
paused = True

def draw_buttons():
    pygame.draw.rect(screen, GRAY, button_start)
    pygame.draw.rect(screen, LIGHT_GREEN, button_pause)
    pygame.draw.rect(screen, LIGHT_BLUE, button_mode)
    pygame.draw.rect(screen, GRAY, button_speed_up)
    pygame.draw.rect(screen, GRAY, button_speed_down)
    #pygame.draw.rect(screen, WHITE, input_size)

    text_start = font.render(start_label, True, BLACK)
    text_pause = font.render(pause_label, True, BLACK)
    text_mode = font.render(modes[current_mode_index], True, BLACK)
    text_speed_up = font.render("+", True, BLACK)
    text_speed_down = font.render("-", True, BLACK)
    text_size = font.render(str(n_cells), True, BLACK)

    screen.blit(text_start, (button_start.x + 10, button_start.y + 5))
    screen.blit(text_pause, (button_pause.x + 10, button_pause.y + 5))
    screen.blit(text_mode, (button_mode.x + 5, button_mode.y + 5))
    screen.blit(text_speed_up, (button_speed_up.x + 15, button_speed_up.y + 5))
    screen.blit(text_speed_down, (button_speed_down.x + 15, button_speed_down.y + 5))
    screen.blit(text_size, (input_size.x + 10, input_size.y + 5))

# Temporizador
def draw_timer(time_elapsed):
    timer_text = font.render(f"{time_elapsed // 60}:{time_elapsed % 60:02}", True, WHITE)
    pygame.draw.rect(screen, GRAY, (0, 0, width, 40))
    screen.blit(timer_text, (width // 2 - timer_text.get_width() // 2, 5))

# Variables de estado
running = True
start_time = pygame.time.get_ticks()
time_elapsed = 0
speed = 60

# Bucle principal
while running:
    screen.fill(BLACK)

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_start.collidepoint(event.pos):
                if start_label == "Iniciar":
                    paused = False
                    started = True
                    start_time = pygame.time.get_ticks() - time_elapsed * 1000
                    size_locked = True
                    start_label = "Reiniciar"
                    pause_label = "Pausar"
                else:
                    # Reiniciar el juego
                    maze, goal = maze_generator(n_cells)
                    current_agent = AgentT3(DORANGE, goal)
                    start_time = pygame.time.get_ticks()
                    time_elapsed = 0
                    paused = True
                    started = False
                    start_label = "Iniciar"
                    pause_label = "Pausar"
            elif button_pause.collidepoint(event.pos) and started:
                paused = not paused
                pause_label = "Continuar" if paused else "Pausar"
            elif button_mode.collidepoint(event.pos) and not started:
                current_mode_index = (current_mode_index + 1) % len(modes)
                if current_mode_index == 0:
                    current_agent = AgentT1(DORANGE, goal)
                elif current_mode_index == 1:
                    current_agent = AgentT2(DORANGE, goal)
                elif current_mode_index == 2:
                    current_agent = AgentT3(DORANGE, goal)
            elif button_speed_up.collidepoint(event.pos) and started:
                speed = min(speed + 10, 120)
            elif button_speed_down.collidepoint(event.pos) and started:
                speed = max(speed - 10, 10)
        elif event.type == pygame.KEYDOWN and not size_locked:
            if event.key == pygame.K_BACKSPACE:
                n_cells = int(str(n_cells)[:-1]) if len(str(n_cells)) > 1 else 1
            elif event.unicode.isdigit():
                n_cells = int(str(n_cells) + event.unicode)

    # Actualizar tiempo
    if not paused and started:
        time_elapsed = (pygame.time.get_ticks() - start_time) // 1000

    # Dibujar el laberinto (20 unidades por debajo del temporizador)
    for row in range(rows):
        for col in range(cols):
            if current_agent.position == [row, col]:
                color = current_agent.color
            elif [row, col] == [0, 0]:
                color = FGREEN
            elif goal == [row, col]:
                color = DARKRED
            else:
                color = COLORS.get(maze[row][col], DLGREY)

            if current_agent.position == goal:
                if any([position == [row, col] for position in current_agent.tour]):
                    color = GOLD

            pygame.draw.rect(screen, color, (col * cell_size, row * cell_size + 40, cell_size, cell_size))  # Desplazamiento en Y

    if not current_agent.position == goal and not paused and started:
        maze[current_agent.position[0]][current_agent.position[1]] = 2
        current_agent.move(maze, goal)

    # Dibujar botones y temporizador
    draw_buttons()
    draw_timer(time_elapsed)

    pygame.display.flip()
    clock.tick(speed)

pygame.quit()
sys.exit()
