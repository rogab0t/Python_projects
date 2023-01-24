import pygame #se improta el modulo pygame

class Block(pygame.sprite.Sprite): #clase hija Block que hereda de la clase Padre Sprite del modulo sprite para crear un pequeño cuadro que en conjunto construiran la imagen del obstaculo
    def __init__(self, size, color, x, y): #metodo inicializador con los parametros para el tamaño de los cuadros, el color de los mismos y sus posiciones en el eje 'x' y en el eje 'y', los valores se asignaran al instanciar un objeto
        super().__init__() #metodo super para utilizar el metodo inicializador de la clase Sprite
        self.image = pygame.Surface((size, size)) #atrubuto para crear la imagen del cuadro, la cual sera un superifice con las dimenesiones de size siendo iguales para que sea un cuadro
        self.image.fill(color) #a la imagen se le da un color el cual será el que se coloque en el parametro
        self.rect = self.image.get_rect(topleft = (x, y)) #se obtiene un rectangulo a base de la superficie creada por image, el cual se empezara a colocara en la parte superior izquierda el cual tiene los valores (x, y) del parametro de __init__()


#array que sera la forma de los obstaculos donde cada 'x' sera una bloque/objeto/sprite 
shape = [ 
'  xxxxxxx',
' xxxxxxxxx',
'xxxxxxxxxxx',
'xxxxxxxxxxx',
'xxxxxxxxxxx',
'xxx     xxx',
'xx       xx']
