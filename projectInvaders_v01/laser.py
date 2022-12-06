import pygame #se improta el modulo pygame
from settings import CURRENT_PATH #se importa la ruta actual desde el modulo settings

class Laser(pygame.sprite.Sprite): #clase padre/hija Laser que hereda de la clase Sprite del modulo sprite para los objetos interactuantes
    def __init__(self, position, screen_height, speed): #metodo inicializador de la clase Laser contiene el parametro position para colocar en laser en la posicion del jugador dentro de la ventana/superficie, tambien se tiene el parametro screen_height para saber el alto de la ventana/superficie y el parametro speed para que tenga una velocidad de movimiento, su valores serán colocados al momento de instanciar un objeto 
        super().__init__() #se utiliza el metodo super para utilizar el metodo inicializador de la clase Sprite para hacer uso de sus atributos
        self.image_laser_path = CURRENT_PATH / 'images' / 'laser.png' #se declara la ruta donde se encuentra la imagen del laser
        self.image = pygame.image.load(self.image_laser_path).convert_alpha() #atributo image para obtener la imagen del laser del jugador desde su ruta y a esa imagen se le aplica el metodo para convertirla en alfa/trasnparente #pygame.Surface((4, 20))
        self.rect = self.image.get_rect(center = position) #atributo para crear un rectangulo a base de la imagen del atributo image a la cual se le aplica el metodo para obtener un rectangulo con la posicion en el centro el cual sera el valor del parametro position
        self.height_y_limit = screen_height #atributo para limitar la altura donde llegara el lase al ser disparado
        self.speed = speed #atributo speed que tiene asignado el valor del parametro speed para que se mueva sobre la ventana


    def destroy(self): #metodo para destruir el laser una vez que fue disparado
        if self.rect.y <= -50 or self.rect.y >= self.height_y_limit + 50: #condicional para validar si el valor del eje 'y' del rectangulo obtenido por image el cual es su posicion en la superficie es menor o igual que -50 o si el valor del eje 'y' del rectangulo obtenido por image es mayor o igual que la altura de la ventana/superficie +50 para que se salga un poco de la superficie 
            self.kill() #se ejecuta el metodo kill() para destruit el objeto/sprite laser disparado


    def update(self): #metodo para actualizar el funcionamiento/movimiento del laser herdado de la clase Sprite
        self.rect.y -= self.speed #el valor de la coordena y del atributo rect sera su valor menos el valor del atributo speed, asi la imagen del laser se movera hacia arriba en el eje y, ya que su movimieto debe ir en valor negativo del eje 'y' a la velocidad de speed
        self.destroy() #se llama a ejecutar el metodo destroy() para eliminar el laser


class LaserEnemy(pygame.sprite.Sprite): #clase padre/hija Laser que hereda de la clase Sprite del modulo sprite para los objetos interactuantes
    def __init__(self,position, screen_height, speed): #metodo inicializador de la clase LaserEnemy contiene el parametro position para colocar el laser en la posicion del enemigo dentro de la ventana/superficie, tambien se tiene el parametro screen_height para saber el alto de la ventana/superficie y el parametro speed para que tenga una velocidad de movimiento, su valores serán colocados al momento de instanciar un objeto 
        super().__init__() #se utiliza el metodo super para utilizar el metodo inicializador de la clase Sprite para hacer uso de sus atributos
        self.image_enemy_laser_path = CURRENT_PATH / 'images' / 'enemylaser.png'  #se declara la ruta donde se encuentra la imagen del laser del enemigo
        self.image = pygame.image.load(self.image_enemy_laser_path).convert_alpha() #atributo image para obtener la imagen del laser del jugador desde su ruta y a esa imagen se le aplica el metodo para convertirla en alfa/trasnparente
        self.rect = self.image.get_rect(center = position) #atributo para crear un rectangulo a base de la imagen del atributo image a la cual se le aplica el metodo para obtener un rectangulo con la posicion en el centro el cual sera el valor del parametro position
        self.height_y_limit = screen_height #atributo para limitar la altura donde llegara el lase al ser disparado
        self.speed = speed #atributo speed que tiene asignado el valor del parametro speed para que se mueva sobre la ventana


    def destroy(self): #metodo para destruir el laser una vez que fue disparado
        if self.rect.y <= - 50 or self.rect.y >= self.height_y_limit + 50: #condicional para validar si el valor del eje 'y' del rectangulo obtenido por image el cual es su posicion en la superficie es menor o igual que -50 o si el valor del eje 'y' del rectangulo obtenido por image es mayor o igual que la altura de la ventana/superficie +50 para que se salga un poco de la superficie 
            self.kill() #se ejecuta el metodo kill() para destruit el objeto/sprite laser disparado


    def update(self): #metodo para actualizar el funcionamiento/movimiento del laser herdado de la clase Sprite
        self.rect.y += self.speed #el valor de la coordena 'y' del atributo rect sera su valor mas el valor del atributo speed, asi la imagen del laser se movera hacia abajo en el eje 'y', ya que su movimieto debe ir en valor positivo del eje 'y' a la velocidad de speed
        self.destroy() #se llama a ejecutar el metodo destroy() para eliminar el laser
