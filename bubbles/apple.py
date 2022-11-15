#importar la libreria pygame
import pygame #importar pygame con todos sus elementos

#importar desde el modulo sprite de la libreria pygame
from pygame.sprite import Sprite #clase padre Sprite

#importar los elementos del módulo settings
from settings import RED #color rojo
from settings import SIZE_APPLE #dimensiones para pintar ciculo apple
from settings import WIDTH_APPLE #ancho del circulo apple

#clase hija Apple
class Apple(Sprite): #clase hija heredando de la clase padre Sprite

    def __init__(self, posicion_x, posicion_y): #inicializar clase hija Apple con los parametros para la manzana/apple en su posicion inicial
        Sprite.__init__(self) #inicializar clase padre Sprite 

        self.posicion_x = posicion_x #atributo de posicion en eje x con valor del parámetro en __init__
        self.posicion_y = posicion_y #atributo de posicion en eje y con valor del parámetro en __init__

        self.image = pygame.Surface(SIZE_APPLE, pygame.SRCALPHA, 32) #atributo para obtener una superficie/image con las dimensiones de SIZE_APPLE para pintar al apple y una mascara de transparecia de 32
        self.rect = self.image.get_rect() #atributo para obtener un rectangulo a partir de la superficie/image con las dimensiones SIZE_APPLE

        pygame.draw.circle(self.image, RED, (20, 20),  WIDTH_APPLE // 2) #metodo para pintar un circulo en la superficie/image con las dimensiones SIZE_APPLE, de color RED, en la posicion cardinal 20, 20 y con un radio de WIDTH_APPLE // 2

        self.visible = True #atributo para tener visible a apple
    
    def draw(self, image): #metodo para pintar/colocar sobre la superfice/image self.image
        self.rect.x = self.posicion_x #atributo de la posicion x del rectangulo pintado en la superficie/image con las dimensiones SIZE_APPLE
        self.rect.y = self.posicion_y #atributo de la posicion y del rectangulo pintado en la superficie/image con las dimensiones SIZE_APPLE

        image.blit(self.image, self.rect) #atributo para dibujar sobre la superficie/image con las dimensiones SIZE_APPLE el rectangulo obtenido con el atributo self.rect = self.image.get_rect()
