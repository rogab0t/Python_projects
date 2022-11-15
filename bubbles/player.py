#importar la libreria pygame
import pygame #importar pygame con todos sus elementos

#importar los elementos del módulo settings
from settings import WIDTH #ancho de la ventana
from settings import HEIGHT #largo de la ventana
from settings import PURPLE #color violeta
from settings import WIDTH_PLAYER #ancho del circulo jugador/player
from settings import HEIGHT_PLAYER #alto del circulo jugador/player
from settings import UP, DOWN, RIGHT, LEFT #direccion de movimiento del jugador

#clase hija Player
class Player(pygame.sprite.Sprite): #clase hija heredando de la clase padre Sprite de sprite en pygame

    def __init__(self, posicion_x, posicion_y): #inicializar clase hija Player con los parametros para pintar el player en su posicion inicial
        pygame.sprite.Sprite.__init__(self) #inicializar clase padre Sprite 
        
        self.posicion_x = posicion_x #atributo de posicion en eje x con el valor del parámetro en __init__
        self.posicion_y = posicion_y #atributo de posicion en eje y con el valor del parámetro en __init__

        self.width = WIDTH_PLAYER #atrubuto que modificara el ancho del circulo player
        self.height = HEIGHT_PLAYER #atrubuto que modificara el alto del circulo player
        
        self.speed = 3 #atributo de velocidad de movimiento en 3
        self.direction = RIGHT # atributo de direccion inicial de movimiento del circulo player hacia la derecha
        self.colition = 0 #atriubuto para saber cantidad de colisiones del jugador con apple's

        self.make_image() #se ejecuta el método para colocar el circulo player
    
    def make_image(self):
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA, 32) #atributo para crear una superficie/image para pintar na rectangulo con las dimensiones (self.width y self.height), y una mascara de transparecia de 32
        self.rect = self.image.get_rect() #atributo para obtener un rectangulo a partir de la superficie/image
        
        pygame.draw.circle(self.image, PURPLE, self.rect.center, (self.width // 2) - 1) #metodo para pintar un circulo en la superficie/image self.image, de color PURPLE, en la coordenada del centro del rectangulo self.rect, y con un radio del atributo self.width entre 2, menos 1 pixel para seer un cierculo perfecto


    def draw(self, image): #metodo para pintar/colocar el circulo obtenido en make_image sobre la superfice/image obtenida en self.image
        self.move() #ejecuta metodo move antes de pintar al circulo jugador para mantener el movimiento

        self.rect.x = self.posicion_x #atributo de la posicion x del rectangulo pintado en la superficie/image obtenida en self.image
        self.rect.y = self.posicion_y #atributo de la posicion y del rectangulo pintado en la superficie/image obtenida en self.image
        
        image.blit(self.image, self.rect) #atributo para dibujar sobre la superficie/image obtenida en self.image, el rectangulo obtenido con el atributo self.rect


    def move(self): #metodo para mover al jugador dependiendo de la tecla presionada
        self.limit_move() #ejecuta metodo para limitar el movimiento 

        if self.direction == UP: #condicional valida el atributo direccion si es UP
            self.posicion_y -= self.speed #asignacion al atributo de posicion en eje y del valor del atributo speed en su valor menos 1 

        elif self.direction == DOWN: #condicional valida el atributo direccion si es DOWN
            self.posicion_y += self.speed #asignacion al atributo de posicion en eje y del valor del atributo speed en su valor mas 1

        elif self.direction == RIGHT: #condicional valida el atributo direccion si es RIGHT
            self.posicion_x += self.speed #asignacion al atributo de posicion en eje x del valor del atributo speed en su valor mas 1

        elif self.direction == LEFT: #condicional valida el atributo direccion si es LEFT
            self.posicion_x -= self.speed #asignacion al atributo de posicion en eje y del valor del atributo speed en su valor menos 1


    def limit_move(self): #metodo para limitar el movimiento del circulo player dentro de la ventana/superficie screen
        if self.posicion_x <= 0: #condicional para validar movimiento en eje x si es menor o igual a 0 
            self.posicion_x = 3 #el valor del atributo de posicion en eje x sera 3 para mantenerlo justo en el borde

        if self.posicion_x >= (WIDTH - self.width): #condicional para validar movimiento en eje x si es mayor o igual al ancho de la ventana menos el ancho del circulo del player el cual es el atributo self.width
            self.posicion_x = (WIDTH - self.width) - 3 #asignar al atributo de posicion en eje x el valor (del ancho de la ventana menos el ancho del circulo del player) menos 3 para mantenerlo justo en el borde

        if self.posicion_y <= 0: #condicional para movimiento en eje y si es menor o igual a 0
            self.posicion_y = 3 #el valor del atributo de posicion en eje y sera 3 para mantenerlo justo en el borde

        if self.posicion_y >= (HEIGHT - self.height): #condicional para validar movimiento en eje y si es mayor o igual al alto de la ventana menos el alto del circulo del player el cual es el atributo self.width
            self.posicion_y = (HEIGHT - self.height) - 3 #asignar al atributo de posicion en eje x el valor (del alto de la ventana menos el alto del circulo del player) menos 3 para mantenerlo justo en el borde


    def up(self): #metodo para mover al jugador hacia arriba
        self.direction = UP #cambio de valo del atributo direccion a UP


    def down(self): #metodo para mover al jugador hacia abajo
        self.direction = DOWN #cambio de valo del atributo direccion a DOWN


    def right(self): #metodo para mover al jugador hacia la derecha
        self.direction = RIGHT #cambio de valo del atributo direccion a RIGHT


    def left(self): #metodo para mover al jugador hacia la izquierda
        self.direction = LEFT #cambio de valo del atributo direccion a LEFT


    def colide(self): #metodo para tener un contador de colisiones y aumente el tamaño del circulo player
        self.colition += 1 #asignacion de su mismo valor mas 1 del atributo colition
        print(self.colition) #impresion del valor de colition

        self.width += 10 #el valor del atributo width aumenta su mismo valor en 10
        self.height += 10 #el valor del atributo height aumenta su mismo valor en 10

        self.make_image() #se ejecuta el método para pintar el circulo player con las nuevas dimensiones por cada colision
