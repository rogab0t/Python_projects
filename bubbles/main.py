#importar la libreria pygame
import pygame #importar pygame con todos sus elementos

import random #importar el modulo random

#imporados desde el modulo settings
from settings import SIZE #importar SIZE desde settings
from settings import WHITE #importar WHITE desde settings
from settings import WIDTH #importar WIDTH desde settings
from settings import HEIGHT #importar HEIGHT desde settings
from settings import WIDTH_APPLE #importar WIDTH_APPLE desde settings
from settings import HEIGHT_APPLE #importar HEIGHT_APPLE desde settings

#importado desde el modulo apple
from apple import Apple

#importado desde el modulo player
from player import Player

pygame.init() #inicializar pygame

#ventana
screen = pygame.display.set_mode(SIZE) #se crea la ventana con las dimesiones de la tupla SIZE para tener una superficie donde pintar
pygame.display.set_caption('Bubbles') #define el titulo de la ventana

clock = pygame.time.Clock() #reloj/contador para la ventana

window = True #controlar la ventana para que siempre este abierta/activa

player = Player(400, 300) #objeto creado/instanciado de la clase Player con los valores para colocarlo en la posicion 400 x, 600 y
apples = pygame.sprite.Group() #se llama la clase Group del modulo sprite de la libreria pygame para colocar apple's en el objeto/grupo apples

for _ in range(0, 10): #ciclo sin variable para crear un grupo de 10 apple's, un apple por cada iteracion
    posicion_x = random.randint(0, (WIDTH - WIDTH_APPLE) - 10) #posicion en el eje x de un valor aleatorio de entre 0 y el ancho del screen menos el ancho de apple menos 10, evitando salir del window
    posicion_y = random.randint(0, (HEIGHT - HEIGHT_APPLE) - 10) #posicion en el eje y de un valor aleatorio de entre 0 y el alto del screen menos el alto de apple menos 10, evitando salir del window

    apples.add(Apple(posicion_x, posicion_y)) #por cada iteracion se añade con el metodo add de la clase aples, al objeto/grupo apples un objeto de la clase Apple con una posicion aleatoria dentro del screen

#logica del juego
while window:#ciclo para mantener activa la ventana
    clock.tick(60) #el tiempo del reloj es de 60 fotogramas por segundo
    
    for event in pygame.event.get(): #ciclo para obtener la lista de eventos del modulo event
        
        if event.type == pygame.QUIT: #condicional para cerrar la ventana si el tipo de evento por cada iteracion es igual al evento QUIT
            window = False #cambio de valor de window de True a False
    
    screen.fill(WHITE) #cambio de color del fondo de la ventana a blanco importado desde el modulo settings
    
    key_pressed = pygame.key.get_pressed() #conocer que tecla fue presionada
    
    if key_pressed[pygame.K_UP]: #condicional para validar si la tecla fecha arriba fue presionada
        player.up() #se ejecuta el metodo up sobre el jugador  
    elif key_pressed[pygame.K_DOWN]: #condicional para validar si la tecla fecha abajo fue presionada
        player.down() #se ejecuta el metodo down sobre el jugador 
    elif key_pressed[pygame.K_RIGHT]: #condicional para validar si la tecla fecha derecha fue presionada
        player.right() #se ejecuta el metodo right sobre el jugador 
    elif key_pressed[pygame.K_LEFT]: #condicional para validar si la tecla fecha izquierda fue presionada
        player.left() #se ejecuta el metodo left sobre el jugador

    player.draw(screen) #se pinta el player en la superficie window despues de pintar dicha superficie de blanco y antes de actualizar la misma
    
    for apple in apples: #ciclo para iterar por cada apple en el  objeto/grupo apples
        if pygame.sprite.collide_mask(player, apple) and apple.visible: #condicional para validar una colision entre la mascara de player y las de apple con el atributo self.image y si el valor de visible es True por cada colision
            apple.visible = False #reasigancion del valor del atributo visible de True a False por cada colision
            player.colide() #ejecucion del metodo colide por cada colision entre jugador y apple
            apples.remove(apple) #se elimina con el metodo remove del objeto/grupo apples, la manzana que ha colisionado con el circulo jugador

        apple.draw(screen) #se pinta en el screen un apple por cada ietracion

    pygame.display.flip() #Actualizar la pantalla en todo momento
