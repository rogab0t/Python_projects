import pygame, sys #importar el modulo pygame y el modulo sys
import obstacle #se importa el modulo obstacle
from random import choice, randint #se importa la funicon choise y la funcion randint desde el modulo random
from settings import SCREEN_WIDTH #se importa al ancho de la ventana del modulo settings
from settings import SCREEN_HEIGTH #se importa la altura de la ventana del modulo settings
from settings import SCREEN_SIZE #se importa el tamaño de la ventana del modulo settings
from settings import PURPLE #se importa el color morado del modulo settings
from player import Player #importar la clase Player del modulo player
from enemy import Alien, Extra #se importa la clase Alien y la clase Extra del modulo enemy
from laser import LaserEnemy #se importa la clase LaserEnemy del modulo laser

class Game(): #clase padre Game
    def __init__(self): #metodo inicializador
        #Player setup
        player_sprite = Player((SCREEN_WIDTH / 2, SCREEN_HEIGTH), SCREEN_WIDTH, 5) #objeto instanciado de la clase Player en la posicion del acho de la superfice entre dos y a la altura de la misma siendo la parte inferior del medio, y con otro parametro de dimension para saber el ancho de la pantalla y limitar movimiento, el 5 es parametro para la velocidad
        self.player = pygame.sprite.GroupSingle(player_sprite) #atributo player el cual es un contenedor/grupo para un solo sprite que sera el objeto player_sprite

        #heald and score setup
        self.lives = 3 #atributo para las vidas del jugador las cuales inician con el valor de 3
        self.lives_surface = pygame.image.load('../projectInvaders/images/ship.png').convert_alpha() #atributo que sera la imagen del jugador para mostrar cuantas vidas se tienen, la cantidad de imagenes sera la cantidad de vidas, dicha imagen es obtenida desde su ruta y a la misma se le ha aplicado el metodo para convertirla en alfa/transparente
        self.lives_x_start = SCREEN_WIDTH - (self.lives_surface.get_size()[0] * 2) #atributo que es la posicion inicial donde se colocaran las imagenes correspondientes a las vidas dentro de la ventana/screen(superior dercha) en el eje 'x', dicho valor se obtiene de restar al ancho de la ventana el valor del ancho de la imagen del jugador, para obtener dicho ancho se aplica el metodo get_size()[0] el cual retorna los valores de 'x' y 'y' con el valor de 0 dentro de los corchetes significando que se necesita el primer valor que es 'x' que es el ancho de la imagen, a ese valor se le multiplica por 2 para obtener el ancho de dos imagenes
        self.score = 0 #atributo para el puntaje el cual inicia con el valor 0
        self.font_game = pygame.font.Font('../projectInvaders/fonts/space_invaders.ttf', 20) #atributo para la fuente de las letras para el score, se utiliza la clase Font, del modulo font de la libreria de pygame, y se coloca la ruta del archivo de la fuente y el tamaño de fuente

        #Obstacle setup
        self.shape = obstacle.shape #atributo para la forma del obstaculo, se obtiene el array shape del modulo obstacle
        self.block_size = 6 #atributo para el tamaño de cada cuadro que conforma al obstaculo
        self.blocks = pygame.sprite.Group() #grupo donde se agregaran cada uno de los cuadros creados desde el array shape
        self.obstacle_amount = 4 #atributo para la cantidad de obstaculos que se colocaran
        self.obstacle_x_position = [number * (SCREEN_WIDTH / self.obstacle_amount - 25) for number in range(0, self.obstacle_amount)] #atributo que es un array, para colocar la eparacion entre cada obstaculo, para ello, number va a ser un numero del 0 al 3 por tener 4 obstaculos, dependiendo del valor de number, este valor sera multiplicado por el resultado de dividir al ancho de la pnatalla entre la cantidad de obstaculos mas 25, y se obendra uno por uno un numero en el rango de 0 a la catidad de obstaculos que es 4, asi se colocaran 4 obstaculos sobre la pantalla en el eje 'x' de la misma, dichos numeros se guardan en el array
        self.create_multiple_obstacles(*self.obstacle_x_position, x_start = SCREEN_WIDTH / 7, y_start = 490) #se llama a ejecutar el metodo para crear los obstaculos con los parametros donde se colocara sobre la ventana/superficicie, el primer parametro es el desempaquetado utilizando '*' de los valores obtenidos en dicho atributo que es un array y los siguientes son donde se colocara el primer obstaculo sobre el eje 'x', dicho valor es el ancho de la ventana entre 7.5 para colocar todos los obstaculos centrados en el ancho de la ventana y el eje 'y' sobre la ventana

        #Alien setup
        self.aliens = pygame.sprite.Group() #grupo de sprites donde estaran colocados todos los objetos alien_sprite
        self.alien_lasers = pygame.sprite.Group() #grupo donde se agregara el laser del enemigo
        self.alien_setup(rows = 5, columns = 10) #se llama a ejecutar la funcion para crear a los enemigos en una posicion especifica, la cual sera una posicion horizontal de 8 enemigos y vertical de 6 filas de enemigos
        self.alien_direction = 1 #atributo para mover al grupo de enemigos a la velociadad de 1 pixel en el eje 'x' de la ventana(derecha)

        #Extra setup
        self.extra = pygame.sprite.GroupSingle() #se crea un grupo individual para colocar al enemigo extra
        self.extra_spawn_time = randint(1000, 2000) #se obtiene un numero aleatorio de entre 1000 y 2000 milisegundos para un temporizador

        #Audio
        self.player_explotion = pygame.mixer.Sound('../projectInvaders/sounds/shipexplosion.wav') #atributo para obtener el archivo del sonido del daño al jugador, se utiliza la funcion Sound() del modulo mixer de pygame, dentro de dicha funcion se coloca la ruta del archivo
        self.player_explotion.set_volume(0.5) #se utiliza la funcion set_volume() para configurar el volumen del sonido

        self.enemy_explotion = pygame.mixer.Sound('../projectInvaders/sounds/invaderkilled.wav') #atributo para obtener el archivo del sonido del laser, se utiliza la funcion Sound() del modulo mixer de pygame, dentro de dicha funcion se coloca la ruta del archivo
        self.enemy_explotion.set_volume(1) #se utiliza la funcion set_volume() para configurar el volumen del sonido
        
        self.laser_enemy = pygame.mixer.Sound('../projectInvaders/sounds/laserenemy.wav') #atributo para obtener el archivo del sonido del laser, se utiliza la funcion Sound() del modulo mixer de pygame, dentro de dicha funcion se coloca la ruta del archivo
        self.laser_enemy.set_volume(0.2) #se utiliza la funcion set_volume() para configurar el volumen del sonido

        self.extra_sound = pygame.mixer.Sound('../projectInvaders/sounds/mysteryentered.wav') #atributo para obtener el archivo del sonido de la aparicion del enemigo extra, se utiliza la funcion Sound() del modulo mixer de pygame, dentro de dicha funcion se coloca la ruta del archivo
        self.extra_sound.set_volume(0.3) #se utiliza la funcion set_volume() para configurar el volumen del sonido

        self.extra_explotion = pygame.mixer.Sound('../projectInvaders/sounds/mysterykilled.wav') #atributo para obtener el archivo del sonido del daño al enemigo extra, se utiliza la funcion Sound() del modulo mixer de pygame, dentro de dicha funcion se coloca la ruta del archivo
        self.extra_explotion.set_volume(0.5) #se utiliza la funcion set_volume() para configurar el volumen del sonido


    def create_obstacle(self, x_start, y_start, offset_x): #metodo para crear un obstaculo con los parametros donde se colocaran en sus respectivos ejes, primero en donde se epezara a colocar en el eje 'x', despues en el eje 'y' y final la separacion entre ellos
        for row_index, row in enumerate(self.shape): #ciclo que itera/recorre por cada indice de las filas, en las filas del array shape, se obtiene un nuero entero con el metodo enumerate() el cual es el indice de las filas y dicho numero se asigna a row_index, lo cual sera la altura del obstaculo
            for col_index, col in enumerate(row): #ciclo que itera/recorre por cada indice de las columnas en las filas del array shape, se obtiene un nuero entero con el metodo enumerate() y dicho numero se asigna a col_index, asi se obtiene la posicion exacta de cada una de las x dentro del array shape
                if col == 'x': #condicional que valida si cada elemento de cada columna en las filas del array shape es igual a 'x'
                    x = x_start + col_index * self.block_size + offset_x #se declara la variable 'x' y se le asigna el valor del resultado de multiplicar el indice de la columna por el tamaño del cuadro, y sumando el espacio inical en el eje 'x' que es a la izquierda y sumando el espacio entre cada uno de los obstaculos, asi obtenido a posicion del obstaculo en el eje 'x'
                    y = y_start + row_index * self.block_size #se declara la variable 'y' y se le asigna el valor del resultado de multiplicar el indice obtenido de la fila por el tamaño del bloque mas la posicion inicial donde se colocara en el eje 'y', asi oteniendo la posicion en el eje 'y' donde se colocara sobre la superficie/ventana
                    block = obstacle.Block(self.block_size, PURPLE, x, y ) #se declara la variable block el cual sera un bloque que coformara al obstaculo, para ello se instancia un obejto desde el modulo obstacle utilizando la clase Block con los parametros empezando por el tamaño del bloque, el color usando es morado y la posicion en el eje 'x' y en el 'y'
                    self.blocks.add(block) #se agrega al grupo blocks cada uno de los bloques creados mediante los ciclos for

    def create_multiple_obstacles(self,*offset, x_start, y_start): #metodo para crear varios obstaculos, *offset es la separacion que tendran entre cada obstaculo cuyo valor ya es colocado en una tupla al utilizar '*' y al momento de colocar los valores al llamar a ejecutar el metodo estos seran leidos como su estuviran dentro de una tupla y con los parametros para saber desde que posicion se colocaran sobre la ventana sobre sus respectivos ejes
        for offset_x in offset: #ciclo que itera por cada valor de separacion en el eje 'x' sore los valores de *offset
            self.create_obstacle(x_start, y_start, offset_x) #se ejecuta la funcion create_obstacle() con los parametros de colocacion en los ejes 'x' y 'y', y el valor de separacion en el eje 'x'

    def alien_setup(self, rows, columns, x_distance = 50, y_distance = 50, x_offset = 110, y_offset = 80): #metodo para crear los enemigos en en una posicion especifica, la cual tendra una cantidad de filas y columnas de enemigos, y la distancia de separacion entre cada enemigo en el eje 'x' y en el eje 'y' y la separacion del cojunto de los enemigos en el eje 'x' y 'y'
        for row_index, row in enumerate(range(rows)): #ciclo para recorrer cada fila del rango filas y obtener su indice en enumerate() y asignarlo a row_index
            for col_index, column in enumerate(range(columns)): #ciclo para recorrer cada columna del rango columnas y obtener su indice con enumerate() y asignarlo a col_index
                x = col_index * x_distance + x_offset#para la posicion en el eje 'x' se multiplicara el numero del indice de las columnas por la distancia de 'x' de cada enemigo y se suma la compensacion del eje 'x'
                y = row_index * y_distance + y_offset #para la posicion en el eje 'y' se multiplicara el numero del indice de las filas por la distancia de 'y' de cada enemigo y se suma la compensacion del eje 'y'

                if row_index == 0: #condicional que evalua si el indice de la fila es igual a 0
                    alien_sprite = Alien('red', x, y) #se instancia/crea un objeto/sprite de la clase Alien con los valores para los parametros empezando por el color, la posicion que tendra al colocarse en el eje 'x' y la posicion que tendra al colocarse en el eje 'y'
                elif 1 <= row_index <= 2: #condicional que evalua si no es la condicion anterior, si 1 es menor o igual al indice de la fila que a su vez es menor o igual a 2, para que se ejecute el codigo si las estan entre el indice 1 y 2
                    alien_sprite = Alien('blue', x, y) #se instancia/crea un objeto/sprite de la clase Alien con los valores para los parametros empezando por el color, la posicion que tendra al colocarse en el eje 'x' y la posicion que tendra al colocarse en el eje 'y'
                else: #si no es ninguna de las condiciones anteriores lo cul seran las filas restantes que son las filas en los indices 3 y 4
                    alien_sprite = Alien('green', x, y) #se instancia/crea un objeto/sprite de la clase Alien con los valores para los parametros empezando por el color, la posicion que tendra al colocarse en el eje 'x' y la posicion que tendra al colocarse en el eje 'y'

                self.aliens.add(alien_sprite) #se agregan al grupo aliens cada uno de los objetos/sprites creados de la clase Alien()
    
    def alien_position_limit(self): #metodo para limitar el movimiento del grupo de enemigos y cambiar su dereccion de movimieto horzontal
        all_aliens = self.aliens.sprites() #variable que contiene el grupo de enemigos al cual se le aplica el metodo sprites() para que cada enemigo dentro del grupo pueda interactuar
        for alien in all_aliens: #ciclo para iterar por cada enemigo dentro del grupo aliens
            if alien.rect.right >= SCREEN_WIDTH: #condicional para validar si la parte derecha de cada rectangulo el cual es el objeto sobre el que esta pintado la imagen del enemigo, se encuentra en un valor mayor o igual al ancho de la ventana/superficie/screen
                self.alien_direction = -1 #se reasigan el valor del atributo alien_direction colocando el valor negativo del original, haciendo que el grupo de enemigos se muevan de manera negativa en el eje 'x'(izquierda) de la ventana a la velocidad de 1 pixel
                self.alien_move_dow(2) #se llama a ejecutar el metodo para mover hacia abajo el grupo de enemigos a una distancia de dos pixeles en el eje 'y'
            elif alien.rect.left <= 0: #condicional para validar si la parte izquierda de cada rectangulo el cual es el objeto sobre el que esta pintado la imagen del enemigo, se encuentra en un valor menor o igual a 0 en el eje 'y'
                self.alien_direction = 1 #se reasigan el valor del atributo alien_direction colocando el valor positivo de nuevo, haciendo que el grupo de enemigos se muevan de manera postiva en el eje 'x'(derecha) de la ventana a la velocidad de 1 pixel
                self.alien_move_dow(2) #se llama a ejecutar el metodo para mover hacia abajo el grupo de enemigos a una distancia de 2 pixeles en el eje 'y'

    def alien_move_dow(self, distance): #metodo para mover al grupo de enemigos hacia abajo cada vez que el algun enemigo del grupo golpee la parte izquierda o derecha de la ventana
        if self.aliens: #condicionar que valida si son enemigos dentro del grupo aliens, solo asi se ejecutara el ciclo siguiente, para que al momento de que ya no haya enemigos se deje de ejecutar dicho ciclo
            for alien in self.aliens.sprites(): #ciclo para iterar por cada enemigo dentro del grupo aliens al cual se le aplica el metodo sprites() para que cada enemigo dentro del grupo pueda interactuar
                alien.rect.y += distance #al valor 'y' el cual es la posicion en el eje 'y' dentro de la ventana/screen, del rectangulo el cual es el objeto sobre el que esta pintado la imagen del enemigo, se le asigna su valor mas el de distance el cual es la distancia que se movera hacia abajo y sera asignado al momento de llamar a ejecutar el metodo

    def alien_shoot(self):
        if self.aliens.sprites(): #validar si hay sprites/objetos dentro del grupo aliens
            random_alien = choice(self.aliens.sprites()) #se ejecuta la funcion choice para seleccionar un sprite/objeto aleatorio del grupo aliens
            laser_sprite = LaserEnemy(random_alien.rect.center, SCREEN_HEIGTH, 9) #objeto instanciado/creado de la clase LaserEnemy el cual tiene como parametros la posicion central del rectangulo obtenido a base de la imagen del laser del enemigo para colocarlo en medio de la imagen del enemigo, el parametro SCREEN_HEIGTH como limite de altura para que se destruya cuando el laser esté debajo de la altura de la parte inferior del jugador y 8 para la velocidad de movimiento del laser sobre la ventana
            self.alien_lasers.add(laser_sprite) #al atributo alien_lasers se le aplica el metodo add() para agregar el objeto laser_sprite insatanciado de la clase LaserEnemy dentro del grupo alien_lasers
            self.laser_enemy.play() #se utiliza la funcion play() para reproducir el sonido cada vez que se ejecute la funcion

    def extra_alien_timer(self): #metodo para ser un temporizador de aparicion del enemigo extra
        self.extra_spawn_time -= 1 #al atributo extra_spawn_time que ya sera un numero aleatorio de entre 1500 y 2000, se le restara 1 a su valor cada vez que se ejecute el metodo
        if self.extra_spawn_time <= 0: #condicional para saber si el valor del atributo extra_spawn_time ha llegado a 0
            self.extra.add(Extra(choice(['right','left']), SCREEN_WIDTH)) #al grupo individual 'extra' se le agrega el objeto instanciado de la clase Extra, con el parametro para saber el lado de aparicio el cual sera aleatorio de entre dos opciones dentro de una lista, y el otro parametro el lugar donde se movera dicho enemigo el cual sera el eje 'x' de la ventana(horizontal)
            self.extra_spawn_time = randint(1500, 1800) #se vuelve a obtener un nuevo numero aleatorio den entre 1500 y 1800 para que se repita el proceso de aparicion del enemigo
            self.extra_sound.play() ##se utiliza la funcion play() para reproducir el sonido cada vez que se cumpla la condicion del timer llegado a 0
    
    def collision_checks(self): #metodo para comprobar las diferentes colisiones entre los distintos sprites/objetos
        #Player lasers
        if self.player.sprite.lasers: #condicional para validar si hay/se disparo algun laser del jugador
            for laser in self.player.sprite.lasers: #ciclo para iterar por cada laser agregado/disparado dentro del grupo unico lasers
                #obstacle collision
                if pygame.sprite.spritecollide(laser, self.blocks, True): #condicional para validar si hubo una colision de sprites, el primer parametro es el sprite principal, el segundo es contra que sprite hubo colision y el tercero es el valor que tendra la funcion kill() para eliminar dicho esprite con el que se ha colisionado
                    laser.kill() #se aplica el metodo kill() al sprite laser disparado que se encuantre dentro del grupo lasers
                
                #alien collision
                aliens_hit = pygame.sprite.spritecollide(laser, self.aliens, True) #si hubo una colision de sprites/con un objeto alien, el primer parametro es el sprite principal/laser del jugador, el segundo es contra que sprite hubo colision y el tercero es el valor que tendra la funcion kill() para eliminar dicho esprite con el que se ha colisionado
                if aliens_hit: #condicional para validar si hubo una colision lo cual es un valor detro de alien_hit
                    for alien in aliens_hit: #ciclo para iterar por cada alien/sprite que se encuentre dentro de la variable aliens_hit
                        self.score += alien.value #el valor del atributo score se le agrega su mismo valor mas el valor del atributo value del alien/sprite dentro de aliens_hit, asi se agregara el valor correspondiente al alien colisionado
                    laser.kill() #se aplica el metodo kill() al sprite laser disparado que se encuantre dentro del grupo lasers para eliminarlo al momento de la colision
                    self.enemy_explotion.play() #se utiliza la funcion play() para reproducir el sonido cada vez que se ejecute la funcion
                
                #laser enemy
                laser_hit = pygame.sprite.spritecollide(laser, self.alien_lasers, True)
                if laser_hit:
                    for laser in laser_hit:
                        laser.kill()

                #extra collision
                if pygame.sprite.spritecollide(laser, self.extra, True): #condicional para validar si hubo una colision de sprites, el primer parametro es el sprite principal, el segundo es contra que sprite hubo colision y el tercero es el valor que tendra la funcion kill() para eliminar dicho esprite con el que se ha colisionado
                    self.score += 500 #al atributo socre se le aumenta su mismo valo mas 500 que es el valor del enemigo extra
                    laser.kill() #se aplica el metodo kill() al sprite laser disparado que se encuantre dentro del grupo lasers
                    self.extra_explotion.play() #se utiliza la funcion play() para reproducir el sonido cada vez que se ejecute la funcion
                    
        #Enemy lasers
        if self.alien_lasers: #condicional para validar si hay/se disparo algun laser del enemigo
            for laser in self.alien_lasers: #ciclo para iterar por cada laser agregado/disparado dentro del grupo alien_lasers
                #obstacle collision
                if pygame.sprite.spritecollide(laser, self.blocks, True): #condicional para validar si hubo una colision de sprites, el primer parametro es el sprite principal, el segundo es contra que sprite hubo colision y el tercero es el valor que tendra la funcion kill() para eliminar el sprite con el que ha colisionado el principal
                    laser.kill() #se aplica el metodo kill() al sprite laser disparado que se encuantre dentro del grupo alien_lasers
                
                #player collision
                if pygame.sprite.spritecollide(laser, self.player, False): #condicional para validar si hubo una colision de sprites, el primer parametro es el sprite principal, el segundo es contra que sprite hubo colision y el tercero es el valor que tendra la funcion kill() para NO eliminar el sprite con el que ha colisionado el principal
                    laser.kill() #se aplica el metodo kill() al sprite laser disparado que se encuantre dentro del grupo alien_lasers
                    self.player_explotion.play() #se utiliza la funcion play() para reproducir el sonido cada vez que se ejecute la funcion
                    self.lives -= 1 #al valor del atributo lives se le restara su mismo valor menos 1 cada vez que haya una colison del laser del enemigo con el jugador, asi se eliminara un vida y una imagen de vida
                    if self.lives <= 0: #condicional para validar si el valor del atributo lives es menor o igual a 0
                        pygame.quit() #se ejecuata la funcion para descativar la biblioteca pygame
                        sys.exit() #se ejecuata la funcion para cerrar la ventana del juego

        #aliens
        if self.aliens: #condicional para validar si hay enemigos dentro del grupo aliens
            for alien in self.aliens: #ciclo que itera cada sprite alien dentro del grupo aliens
                #obstacle collision
                pygame.sprite.spritecollide(alien, self.blocks, True) #se ejecuta la colision contra un bloque de los obstaculo, la cual tiene como parametros el primero es el sprite principal, el segundo es con que colisiona y el tercero es el valor de la funcion kill() para eliminar el sprite con el que ha colisionado el principal

                #player collision
                if pygame.sprite.spritecollide(alien, self.player, False): #condicional para validar si hubo una colision de sprites, el primer parametro es el sprite principal, el segundo es contra que sprite hubo colision y el tercero es el valor que tendra la funcion kill() para NO eliminar el sprite con el que ha colisionado el principal
                    pygame.quit() #se ejecuta la funcion quit() del modula pygame para cerrar la ventana/superficie
                    sys.exit() #se ejecuta la funcion exit() del modula sys para cerrar la ventana del juego
 
    def display_lives(self): #metodo para colocar las imagenes de las vidas del jugador sobre la ventana/screen
        for live in range(self.lives - 1): #ciclo para iterar sobre el valor/vida del atributo self.lives el cual es 3 y a ese valor se le resta uno para que al momento de tener una sola vida ya no se muestre ninguna imagen y al tener 3 vidas solo se muestan 2 imagenes
            x = self.lives_x_start + (live * (self.lives_surface.get_size()[0]) - 5) #el valor donde se colocaran las imagenes de las vidas sobre la ventana en el eje 'x', el cual es el resultado de sumar la posicion inicial en el eje 'x' que es la parte derecha, el valor de multiplicar cada valor/vida dentro de la varible vidas(1 o 2) por el tamaño del ancho de la imagen para las vidas y a ese resulatdo se le resta 5 para moverlos un poco hacia la izquierda, asi se colocaran dos imagenes una a lado de la otra en la esquina superior derecha
            SCREEN.blit(self.lives_surface, (x, 8)) #se pintara sobre la ventana la imagen para las vidas en la posicion en sus respectivos ejes, en 'x' con el valor de la varible 'x', y en 'y' con el valor de 8 ya que asi se coloca cerca de la parte superior
    
    def display_score(self): #metodo para colocar el texto y la puntuacion del jugador sobre la ventana/screen
        score_surface = self.font_game.render(f"score: {self.score}", False, 'white') #variable que sera la superficie/imagen la cual sera un renderizado de un texto el cual es "score {}" y dentro de las llaves se colocara el valor del atributo score el cual sera convetido a texto, se coloca Fasle para el antialiasing, asi se las letras se mostraran mas pixeladas y se le coloca el color blanco
        score_rect = score_surface.get_rect(topleft = (0, 10)) #se crea un rectangulo a base de la superficie creada con el texto el cual se colocara a en parte superior izquierda con un desplazamiento positivo de 10 pixeles en el eje 'y'
        SCREEN.blit(score_surface, score_rect) #se coloca/pinta sobre la superficie/screen la imagen y el recatgulo para el score/puntaje

    def victory_message(self):
        if not self.aliens.sprites(): #condiconal para validaar si ya no se encuentra ningun spritet/objeto alien dentro del grupo aliens
            victory_surface = self.font_game.render(f"You Won", False, 'white') #variable que sera la superficie/imagen la cual sera un renderizado de un texto el cual es "You Won", se coloca Fasle para el antialiasing, asi se las letras se mostraran mas pixeladas y se le coloca el color blanco
            victory_rect = victory_surface.get_rect(center = (SCREEN_WIDTH / 2, SCREEN_HEIGTH / 2)) #variable donde se obtiene un rectangulo a base de la superficie obtenida de renderizar el texto como una imagen, dicho rectangulo con el texto se mostrara en el centro de la ventana, para ello se obtienen los valores del ancho y el alto de dicha ventana y esos valores de dividen entre dos para que asi dicho recangulo se coloque en el centro de la ventana
            SCREEN.blit(victory_surface, victory_rect) #se dibuja/coloca sobre la ventana/screen mediante la funcion blit() la superifie con el texto de victoria y el rectangulo para posicionar dicho texto

    def run(self): #metodo para ejecutar el juego
        self.player.update() #al grupo Unico player que es el contenedor del objeto player_sprite se le aplica el metodo para actualizar la funcionalidad del jugador
        self.alien_lasers.update() #se llama a ejecuar el metodo update() de la clase LaserEnemy() para actualizar el funcionamiento/movimiento del laser  
        self.extra.update() #se llama a ejecutar el metodo update() de la clase Extra() para actualizar el funcionamiento/movimiento del enemigo extra

        self.aliens.update(self.alien_direction) #al grupo aliens que es el contenedor de los objetos alien_sprite se le aplica el metodo para actualizar la funcionalidad/movimiento del grupo de enemigos con el valor del atributo que sera la direccion de movimiento del grupo de enemigos
        self.alien_position_limit() #se llama a ejecutar el metodo para limitar el movimiento del grupo de enemigos dentro de la ventana
        self.extra_alien_timer() #se llama a ejecutar el metodo para que empieze el temporizador al iniciar el juego
        self.collision_checks() #se llama a ejecutar el metodo collision_checks() para validar las colisiones

        self.player.sprite.lasers.draw(SCREEN) #se hace uso del metodo draw(SCREEN) para dibujar sobre la superficie/ventana, el objeto creado por el metodo shoot_laser() que se encuentra dentro del grupo lasers el cual sera un sprite/interactua, el cual se encuentra detro del GroupSingle y es el objeto player_sprite instanciado de la clase Player. Es colocado aqui para que se dibuje despues de actualizar la funcionalidad del juagdor y antes de la imagen del jugador, quedando debajo del mismo
        self.player.draw(SCREEN) #se dibujará sobre la superfice/ventana el objeto player_sprite el cual ya esta detro del GroupSingle
        self.blocks.draw(SCREEN) #se dibujan sobre la venata/superficie el contenido del grupo blocks, los cuales son los obstaculos creados
        self.aliens.draw(SCREEN) #se dibujan sobre la venata/superficie el contenido del grupo aliens, los cuales son todos los enemigos creados
        self.alien_lasers.draw(SCREEN) #se dibujan sobre la venata/superficie el contenido del grupo alien_lasers, el cual es el sprite/objeto del laser del enemigo
        self.extra.draw(SCREEN)  #se dibujan sobre la venata/superficie el contenido del grupo extra, el cual es el sprite/objeto del enemigo extra
        self.display_lives() #se llama a ejecutar el metodo display_lives() para colocar la cantidad de imagenes de la vidas correspondientes
        self.display_score() #se llama a ejecutar el metodo display_score() para colocar el texto con el puntaje
        self.victory_message() #se llama a ejecutar el metodo victory_message() para colocar el texto de viactoria cuando se cumpla la condicion necesaria

if __name__ == '__main__': #condicional para validar que se ejecute el codigo solo si el nombre del archivo es main evitando que lo ejecute otro archivo
    pygame.init() #inicializar el modulo pygame con todo su contenido
    SCREEN = pygame.display.set_mode(SCREEN_SIZE) #constante con valor para crear la superficie/ventana con las dimensiones de SCREEN_SIZE
    window = True #valor True en la variable window para mantener activa/abirta la ventana mientras el valor siga siendo True
    clock = pygame.time.Clock() #se crear un reloj/contador
    game = Game() #objeto instanciado de la clase Game

    TIMER_ALIENLASER = pygame.USEREVENT + 1 #se crea un nuevo evento para ser un temporizador del disparo del enemigo
    pygame.time.set_timer(TIMER_ALIENLASER, 550) #se crea el temporizador con el evento anterior el cual se ejecutara cada 550 milisegundos

    while window: #condicional para mantener activa la ventana/superficie mientras el valor de window sea True
        for event in pygame.event.get(): #ciclo for por cada evento en el modulo event de pygame se ejeucta la funcion get() para pbetenr la lista de evetos de dicho modulo
            if event.type == pygame.QUIT: #condicional para cerrar la ventana si el tipo de evento por cada iteracion es igual al evento QUIT
                window = False #cambio de valor de window de True a False, terminando el ciclo While window/True cerrando la ventana
            if event.type == TIMER_ALIENLASER: #condicional para ejecutar el metodo si el tipo de evento es igual a TIMER_ALIENLASER el cual es el nuevo evento que se creo
                game.alien_shoot() #se ejecuta el metodo para que el enemigo dispare en un tiempo determinado
        
        image = pygame.image.load('../projectInvaders/images/background.jpg') #variable que obtendra la imagen del fondo desde su ruta
        SCREEN.blit(image,(0,0)) #se coloca/dibuja sobre la ventana/superficie mediante blit(), la imagen del fondo desde las posiciones (0, 0) en los ejes 'x' y 'y'

        #SCREEN.fill(BLACK) #se rellena la superficie/ventana con el valor del color BLACK del modulo settings
        game.run() #se ejecuta el metodo run() del objeto game para ejecutar el juego despues de rellenar le superficie 

        pygame.display.flip() #Actualizar la pantalla en todo momento
        clock.tick(60) #el tiempo del reloj es de 60 fotogramas por segundo
