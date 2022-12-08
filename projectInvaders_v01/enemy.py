import pygame #se improta el modulo pygame
from settings import CURRENT_PATH #se importa la ruta actual desde el modulo settings

class Human(pygame.sprite.Sprite): #clase hija Human que hereda de la clase Padre Sprite del modulo sprite para crear a los enemigos
    def __init__(self, color, x ,y): #metodo inicializador de la clase Human con el paramaetro para el colo del human y la posicion donde sera pintado sobre la ventana/superificie
        super().__init__() #metodo super para utilizar el metodo inicializador de la clase Sprite
        human_path = CURRENT_PATH  / 'images' / (color + '.png') #variable que sera la ruta de las imagenes de los humans, primero se coloca la ruta actual, concatenacion con slash, el directorio 'images', concatenacion con slash y el valor del color del enemigo el cual sera ingresado al momento de ejecutar el metodo nicializador, concatenado utilizando '+' con la extension '.png'
        self.image = pygame.image.load(human_path).convert_alpha() #atributo image para obtener la imagen del human desde su ruta la cual es el valor de la varible human_path y a esa imagen se le aplica el metodo para convertirla en alfa/transparente
        self.rect = self.image.get_rect(topleft = (x, y)) #atributo para crear un rectangulo a base de la imagen del atributo image a la cual se le aplica el metodo para obtener un rectangulo en la posicion izquierda superior el cual sera el valor de los parametros 'x, y' del metodo __init__

        if color == 'green': #condicional para validar si el color del objeto/sprite/human es verde
            self.value = 100 #se asigna el valor de 100 al atributo del valor que tiene el enemigo de su color correspondiente
        elif color == 'blue': #condicional para validar si el color del objeto/sprite/human es amarillo
            self.value = 200 #se asigna el valor de 100 al atributo del valor que tiene el enemigo de su color correspondiente
        else: #condicional para validar si el color del no es ni verde o amarillo
            self.value = 300 #se asigna el valor de 100 al atributo del valor que tiene el enemigo de su color correspondiente


    def update(self, direction): #metodo para actualizar el funcionamiento/movimiento del jugador, herdado de la clase Sprite, con el atributo direction al cual se le dara su valor al momento de llamar a ejecutar el metodo, funcionanado como velocidada de movimiento hacia una direccion 
        self.rect.x += direction #atributo que es la direccion en el eje 'x' donde se posiciona el grupo de enemigos, al cual se le asigna su valor mas el valor del parametro direction la cual sera la direccion de moviemiento de los enemigos sobre la ventana/superficie en el eje 'x' de la ventana(horizontal)


class Extra(pygame.sprite.Sprite): #clase hija Extra que hereda de la clase Padre Sprite del modulo sprite para crear al enemigo extra
    def __init__(self, side, screen_width): #metodo inicializador de la clase Extra con el atributo side para saber el lado por el cual aparecera y con el atributo para saber el ancho de la ventana
        super().__init__() #metodo super para utilizar el metodo inicializador de la clase Sprite
        self.image_extra_path = CURRENT_PATH / 'images' / 'extra.png' #se declara la ruta donde se encuentra la imagen del enemigo extra
        self.image = pygame.image.load(self.image_extra_path).convert_alpha() #atributo image para obtener la imagen del jugador desde su ruta y a esa imagen se le aplica el metodo para convertirla en alfa/transparente

        if side == 'right': #condicional para saber si el lado es derecha
            x = screen_width + 150 #el valor de la varible x es el ancho de la ventana mas 150 para que aparezca en el eje 'x' de la ventana mas 50 pixeles para que aparezca desde fuera de la ventana del lado derecho
            self.speed = -3 #el valor de la velocidad en negativa a tres pixeles para que se mueva al lado izquierdo del eje 'x'
        else: #condicional para saber si el lado es izquierda ya que solo hay dos opciones y 'derecha' ya fue validado
            x = -150  #el valor de la varible x es menos 150 para que aparezca en el eje 'x' de la ventana menos 50 pixeles para que aparezca desde fuera de la ventana del lado izquierdo
            self.speed = 3 #el valor de la velocidad en positiva a tres pixeles para que se mueva al lado derecho del eje 'x'

        self.rect = self.image.get_rect(topleft = (x, 60)) #se obtiene un rectangulo a base de la imagen obtenida en image, el cual se colocara inicialmente en la parte superior izquierda cuyo valor es el valor de x el cual es el  eje 'x' de la ventana y en el eje 'y' en la posicion 60


    def update(self): #metodo para actualizar el movimiento/funcionalidad del objeto
        self.rect.x += self.speed #el valor de la coordena 'x' del atributo rect sera su valor mas el valor del atributo speed, asi la imagen del enemigo extra se movera horizontalmente en el eje 'x', ya que su movimieto debe ir en valor positivo o negativo del eje 'x' a la velocidad de speed
