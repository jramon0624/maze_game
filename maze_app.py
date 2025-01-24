import pygame
import sys
from entities import AgentT1, AgentT2, AgentT3
from maze_generator import maze_generator
from cons import *

# Inicialización
pygame.init()
clock = pygame.time.Clock()

# Obtén el tamaño de la pantalla disponible
display_info = pygame.display.Info()
screen_width, screen_height = display_info.current_w, display_info.current_h

# Tamaño de la ventana
window_margin = 0.2  # Reducir margen para que la ventana use más espacio
window_width = int(screen_width * (1 - window_margin))
window_height = int(screen_height * (1 - window_margin))

# Parámetros
n_cells = N_CELLS
cell_size = min(window_width, window_height - 120) // N_CELLS
cols = n_cells
rows = n_cells
width = cols * cell_size
height = rows * cell_size

# Configuración de la ventana adaptable
screen = pygame.display.set_mode((width + 300, height + 40), pygame.RESIZABLE | pygame.SCALED)
pygame.display.set_caption("Simulador de laberinto")

# Generar el laberinto y agente
maze, goal = maze_generator(n_cells)
current_agent = AgentT1(DORANGE, goal)

# Fuente
font = pygame.font.Font(None, int(36 * (screen_width / 1920)))  # Ajusta el tamaño de la fuente dinámicamente
title_font = pygame.font.Font(None, int(48 * (screen_width / 1920)))

# Botones - dinámicos
button_width, button_height = 200, 40

button_start = pygame.Rect(width + 50, 80, button_width, button_height)
button_pause = pygame.Rect(width + 50, 140, button_width, button_height)
button_mode = pygame.Rect(width + 50, 200, button_width, button_height)
button_speed_up = pygame.Rect(width + 200, 260, 50, button_height)
button_speed_down = pygame.Rect(width + 50, 260, 50, button_height)


# Opciones de modo de búsqueda
modes = ["Aleatorio", "Profundad", "Anchura"]
current_mode_index = 1

# Estado de botones
start_label = "Iniciar"
pause_label = "Pausar"
size_locked = False
started = False
paused = True

def draw_buttons():
    # Botón de iniciar
    pygame.draw.rect(screen, WHITE, button_start, border_radius=5)
    pygame.draw.rect(screen, BLACK, button_start, width=2, border_radius=5)
    text_start = font.render(start_label, True, BLACK)
    screen.blit(text_start, (button_start.x + (button_start.width - text_start.get_width()) // 2, button_start.y + 5))

    # Botón de pausar
    pygame.draw.rect(screen, WHITE, button_pause, border_radius=5)
    pygame.draw.rect(screen, BLACK, button_pause, width=2, border_radius=5)
    text_pause = font.render(pause_label, True, BLACK)
    screen.blit(text_pause, (button_pause.x + (button_pause.width - text_pause.get_width()) // 2, button_pause.y + 5))

    # Botón de modo
    pygame.draw.rect(screen, WHITE, button_mode, border_radius=5)
    pygame.draw.rect(screen, BLACK, button_mode, width=2, border_radius=5)
    text_mode = font.render(modes[current_mode_index], True, BLACK)
    screen.blit(text_mode, (button_mode.x + (button_mode.width - text_mode.get_width()) // 2, button_mode.y + 5))

    # Botones de velocidad
    pygame.draw.rect(screen, WHITE, button_speed_up, border_radius=5)
    pygame.draw.rect(screen, BLACK, button_speed_up, width=2, border_radius=5)
    text_speed_up = font.render("+", True, BLACK)
    screen.blit(text_speed_up, (button_speed_up.x + (button_speed_up.width - text_speed_up.get_width()) // 2, button_speed_up.y + 5))

    pygame.draw.rect(screen, WHITE, button_speed_down, border_radius=5)
    pygame.draw.rect(screen, BLACK, button_speed_down, width=2, border_radius=5)
    text_speed_down = font.render("-", True, BLACK)
    screen.blit(text_speed_down, (button_speed_down.x + (button_speed_down.width - text_speed_down.get_width()) // 2, button_speed_down.y + 5))

    # Texto de velocidad
    text_speed = font.render("SPEED", True, BLACK)
    screen.blit(text_speed, (button_speed_down.x + 60, button_speed_down.y + 5))

    # Valor numérico de velocidad
    speed_percentage = int((speed - 10) / 1.1)  # Escala de velocidad del 1 al 100
    text_speed_value = font.render(str(speed_percentage), True, BLACK)
    screen.blit(text_speed_value, (button_speed_down.x + 87, button_speed_down.y + 45))




def draw_timer(time_elapsed):
    timer_text = title_font.render(f"{time_elapsed // 60}:{time_elapsed % 60:02}", True, BLACK)
    pygame.draw.rect(screen, WHITE, (0, 0, width + 300, 40))
    pygame.draw.rect(screen, BLACK, (0, 0, width + 300, 40), width=2)
    screen.blit(timer_text, ((width + 300) // 2 - timer_text.get_width() // 2, 5))

# Variables de estado
running = True
start_time = pygame.time.get_ticks()
time_elapsed = 0
speed = 60

reached_goal = False

def draw_goal_message():
    # Fondo semitransparente
    overlay = pygame.Surface((width, height))
    overlay.set_alpha(180)  # Opacidad del fondo
    overlay.fill((0, 0, 0))  # Color negro
    screen.blit(overlay, (0, 40))  # Ajusta para respetar el encabezado

    # Mensaje
    message_text = title_font.render("¡Llegó a la meta!", True, WHITE)
    screen.blit(
        message_text,
        (width // 2 - message_text.get_width() // 2, height // 2 - message_text.get_height() // 2 + 40)
    )

# Bucle principal
while running:
    screen.fill(FONDO)  # Fondo negro

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if button_start.collidepoint(event.pos):
                if start_label == "Iniciar":
                    paused = False
                    started = True
                    reached_goal = False  # Reinicia el estado de meta
                    start_time = pygame.time.get_ticks() - time_elapsed * 1000
                    size_locked = True
                    start_label = "Reiniciar"
                    pause_label = "Pausar"
                else:
                    maze, goal = maze_generator(n_cells)
                    current_agent = AgentT3(DORANGE, goal)
                    start_time = pygame.time.get_ticks()
                    time_elapsed = 0
                    paused = True
                    started = False
                    reached_goal = False
                    start_label = "Iniciar"
                    pause_label = "Pausar"
            elif button_pause.collidepoint(event.pos) and started and not reached_goal:
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
            elif button_speed_up.collidepoint(event.pos) and started and not reached_goal:
                speed = min(speed + 10, 120)
            elif button_speed_down.collidepoint(event.pos) and started and not reached_goal:
                speed = max(speed - 10, 10)

    # Actualiza el tiempo solo si no se ha llegado a la meta
    if not paused and started and not reached_goal:
        time_elapsed = (pygame.time.get_ticks() - start_time) // 1000

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

            pygame.draw.rect(screen, color, (col * cell_size, row * cell_size + 40, cell_size, cell_size))

    # Comprueba si el agente llegó a la meta
    if current_agent.position == goal and not reached_goal:
        reached_goal = True
        paused = True  # Pausa la simulación al alcanzar la meta

    # Movimiento del agente solo si no se llegó a la meta
    if not current_agent.position == goal and not paused and started:
        maze[current_agent.position[0]][current_agent.position[1]] = 2
        current_agent.move(maze, goal)

    draw_buttons()
    draw_timer(time_elapsed)

    # Muestra el mensaje si se llegó a la meta
    if reached_goal:
        draw_goal_message()

    pygame.display.flip()
    clock.tick(speed)

pygame.quit()
sys.exit()