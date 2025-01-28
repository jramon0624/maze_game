WINDOW_SIZE = 700 # Ancho de la ventana por defecto

N_CELLS = 51 # Tamaño de la matriz por defecto

# Colores en formato RGB
GWHITE = (248,248,255)
DARKCYAN = (0,139,139)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
LIGHT_GREEN = (144, 238, 144)
LIGHT_BLUE = (173, 216, 230)
DARKRED = (139, 0, 0)
GOLD = (255, 215, 0)
FGREEN = (34, 139, 34)  # Forest Green
DLGREY = (169, 169, 169)  # Dark Gray
DORANGE = (255, 140, 0)  # Dark Orange
SOFTBLUE = (204,139,139)

FONDO = (255, 255, 255)

# Colores de las celdas
COLORS = {
    0: BLACK,      # Negro: Paredes
    1: GWHITE,      # Blanco: Pasillos
    2: DARKCYAN,    # Azul: Pasillos recorridos
    3: SOFTBLUE     # Rojo: Pasillos analizados 
}