WINDOW_SIZE = 760 # Ancho de la ventana por defecto

N_CELLS = 31 # Tamaño de la matriz por defecto

DARKRED = (139,0,0)
DORANGE = (255,140,0)
FGREEN = (34,139,34)
GWHITE = (248,248,255)
DLGREY = (17,49,49)
DARKCYAN = (0,139,139)
GOLD = (255,215,0)

# Colores de las celdas
COLORS = {
    0: DLGREY,      # Negro: Paredes
    1: GWHITE,      # Blanco: Pasillos
    2: DARKCYAN,    # Azul: Pasillos recorridos
    3: DARKRED      # Rojo: Pasillos analizados ### Linea agregada
}