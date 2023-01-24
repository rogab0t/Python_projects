from pathlib import Path #se importa desde el modulo pathlib que ya se encuentra el la libreria de python, la clase Path

#dimensiones
SCREEN_WIDTH = 700 #ancho de la ventana/superficie
SCREEN_HEIGTH = 600 #alto de la ventana/supericie
SCREEN_SIZE = (SCREEN_WIDTH, SCREEN_HEIGTH) #dimesiones de la ventana superficie a base de las dimensiones anteriores

#colores
BLACK = (0, 0, 0) #color negro en rgb
RED = (241, 79, 80) #color rojo en rgb
PURPLE = (122, 42, 126) #color morado en rgb

#rutas
CURRENT_PATH = Path.cwd() #constante que sera la ruta actual, se utiliza el metodo cdw de la clase Path y el retorno es convertido a string para poder concatenar
SCORE_PATH = CURRENT_PATH / 'score.txt' #constante para la ruta donde se encuentra el archivo score.txt, utilizando la ruta actual concatenando con un slash y el nombre de dicho archivo
