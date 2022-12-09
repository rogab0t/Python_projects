import pygame, sys #importar el modulo pygame y el modulo sys
from laser import Laser #se importa la clase Laser modulo laser
from settings import CURRENT_PATH #se importa la ruta actual desde el modulo settings

class Player(pygame.sprite.Sprite): #clase padre/hija Player que hereda de la clase Sprite del modulo sprite para los objetos interactuantes
    def __init__(self, position, limit, speed): #metodo inicializador de la clase Player, contiene el parametro position para colocar la posicion del jugador dentro de la ventana/superficie, el cual se colocará al instanciar un objeto, el parametro limit para limiar su movimiento dentro de la ventana y el parametro speed para que tenga una velocidad de movimiento, su valores serán colocados al momento de instanciar un objeto.
        super().__init__() #se utiliza el metodo super para utilizar el metodo inicializador de la clase Sprite para hacer uso de sus atributos
        self.image_ship_path = CURRENT_PATH / 'images' / 'ship.png'  #se declara la ruta donde se encuentra la imagen de la nave del jugador
        self.image = pygame.image.load(self.image_ship_path).convert_alpha() #atributo image para obtener la imagen del jugador desde su ruta y a esa imagen se le aplica el metodo para convertirla en alfa/trasnparente 
        self.rect = self.image.get_rect(midbottom = position) #atributo para crear un rectangulo a base de la imagen del atributo image a la cual se le aplica el metodo para obtener un rectangulo con la posicion en la parte inferior media el cual sera el valor del parametro position
        self.limit_x = limit #atributo para limitar el movimieto horizontal que es el eje x
        self.speed = speed #atributo para la velocidad que será asignado al instanciar/crear un objeto
        self.ready = True #atributo para disparar el laser del jugador, con valor true para poder empezar disparando
        self.shoot_time = 0 #atributo para saber cuando se ha disparado el laser, con valor 0 como inicio por no haber disparado
        self.shoot_cooldown = 500 #atributo para poder dispararel laser cada 550 milisegundos

        self.lasers = pygame.sprite.Group() #se crear un grupo de sprites para los lasers

        #sounds
        self.laser_sound_path = CURRENT_PATH / 'sounds' / 'laser.wav'  #se declara la ruta donde se encuentra el sonido del laser del jugador
        self.laser_sound = pygame.mixer.Sound(self.laser_sound_path) #atributo para obtener el archivo del sonido del laser, se utiliza la funcion Sound() del modulo mixer de pygame, dentro de dicha funcion se coloca la ruta del archivo
        self.laser_sound.set_volume(0.2) #se utiliza la funcion set_volume() para configurar el volumen del sonido


    def get_keys(self): #metodo para saber que tecla fue presionada 
        keys = pygame.key.get_pressed() #variable que obtendra las teclas presiondas

        if keys[pygame.K_RIGHT]: #condicional, si la tecla presionada es la tecla derecha dentro el array key de pygame
            self.rect.x += self.speed #el valor de la coordena x del atributo rect sera su valor mas el valor del atributo speed, asi la imagen del jugador se moverá hacia la derecha de la parte inferior en el eje x, su movimieto debe ir en valor negativo del eje x a la velocidad de speed
        elif keys[pygame.K_LEFT]: #condicional, si la tecla presionada es la tecla izquierda dentro el array key de pygame
            self.rect.x -= self.speed #el valor de la coordena x del atributo rect sera su valor mas el valor del atributo speed, asi la imagen del jugador se moverá hacia la izquierda de la parte inferior en el eje x, su movimieto debe ir en valor negativo del eje x a la velocidad de speed
        
        if keys[pygame.K_SPACE] and self.ready: #condicional, si la tecla presionada es la tecla espacio dentro el array key de pygame y el valor del atributo ready sea True
            self.shoot_laser() #se ejecuta el metodo para disparar el laser del juagador
            self.ready = False #al atributo ready se le cambia el valor a False por cada disparo del laser del jugador
            self.shoot_time = pygame.time.get_ticks() #al atributo shoot_time se le reasigna el obtener los milisegundos desde que se inicio el juego, se utiliza una solsa vez que es al presionar espacio, obteniendo un solo momento


    def recharge(self): #metodo para recargar el laser del jugador
        if not self.ready: #condicional que valida si el valor del atributo self.ready es False
            current_time = pygame.time.get_ticks() #se declara la variable y se le asigna el obtener los milisegundos desde que se inicio el juego, ejecutandose continuamente mientras se cumpla la condicion anterior, obteniendo varios momentos de tiempo
            if current_time - self.shoot_time >= self.shoot_cooldown: #condicional que valida si el tiempo actual menos el tiempo del disparo del laser del jugador es mayor o igual al valor del atributo shoot_cooldown que es 600 milisegundos
                self.ready = True #al atributo ready se le reasigna el valor True para que ejecute el metodo shoot_laser() en el condicional if keys[pygame.K_SPACE] and self.ready: y asi poder volver a disparar


    def limit(self): #metodo para limitar el movimiento horizontal del jugador
        if self.rect.left <= 0: #condicional si el valor left que es donde se coloca/pinta el objeto sobre la superficice/ventana, de rect que es la imagen del jugador, es menor o igual que cero(sale de la izquierda de la superficie)
            self.rect.left = 0 #al valor left de rect se le asigna el valor de 0 para colocarlo en la coordena 0 del eje x
        if self.rect.right >= self.limit_x: #condicional si el valor right que es donde se coloca/pinta el objeto sobre la superficice/ventana, de rect que es la imagen del jugador, es mayor o igual que el valor de limit que será el ancho de la superficie (sale de la derecha de la superficie)
            self.rect.right = self.limit_x #al valor rigth de rect se le asigna el valor de limit para colocarlo en la coordena del maximo del ancho de la superficice(ventana) del eje x


    def shoot_laser(self): #metodo para disparar el laser del jugador
        self.lasers.add(Laser(self.rect.center, self.rect.bottom, 14)) #al atributo lasers se le aplica el metodo add() para agregar el objeto laser insatanciado de la clase Laser dentro del grupo lasers, el cual tiene como parametros la posicion central del rectangulo obtenido a base de la imagen del laser para colocarlo en medio del jugador, el parametro self.rect.bottom como limite de altura para que se destruya cuando el laser esté debajo de la altura de la parte inferior del jugador y 14 para la velocidad de movimiento del laser
        self.laser_sound.play() #se utiliza la funcion play() para reproducir el sonido cada vez que se ejecute la funcion


    def update(self): #metodo para actualizar el funcionamiento/movimiento del jugador, herdado de la clase Sprite
        self.get_keys() #se llama a ejecutar el metodo get_keys() para ejecutar el movimiento del jugador
        self.recharge() #se llama a ejecutar el metodo recharge() para recargar el laser del jugador
        self.limit() #se llama a ejecutar el metodo limit() para limitar el movimiento del jugador cada vez que se actualice la imagen sobre la superificie
        self.lasers.update() #se ejecuta el metodo update() al grupo de sprites con el objeto laser ya agregado, para que se actualice su movimiento
