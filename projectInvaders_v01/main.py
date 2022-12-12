import pygame, sys #importar el modulo pygame y el modulo sys
import obstacle #se importa el modulo obstacle
from pathlib import Path #se importa desde el modulo pathlib que ya se encuentra el la libreria de python, la clase Path
from random import choice, randint #se importa la funicon choise y la funcion randint desde el modulo random
from settings import SCREEN_WIDTH #se importa al ancho de la ventana del modulo settings
from settings import SCREEN_HEIGTH #se importa la altura de la ventana del modulo settings
from settings import SCREEN_SIZE #se importa el tamaño de la ventana del modulo settings
from settings import BLACK #se importa el color negro del modulo settings
from settings import PURPLE #se importa el color morado del modulo settings
from settings import CURRENT_PATH #se importa la ruta actual desde el modulo settings
from settings import SCORE_PATH #se importa la ruta del archivo score.txt desde el modulo settings
from player import Player #importar la clase Player del modulo player
from enemy import Human, Extra #se importa la clase Human y la clase Extra del modulo enemy
from laser import LaserEnemy #se importa la clase LaserEnemy del modulo laser

class Game(): #clase padre Game
    def __init__(self): #metodo inicializador
        self.mainScreen = True #atributo que contrala la activacion de la ventana del menu principal, con el valor de True por ser la ventana incial
        self.startGame = False #atributo que contrala la activacion de la ventana del juego, con el valor de False para que despues cambie a True y sea activada
        self.over = False #atributo que contrala la activacion de la ventana del mensaje de derrota, con el valor de False para que despues cambie a True y sea activada
        self.scores = False #atributo que contrala la activacion de la ventana de los puntajes, con el valor de False para que despues cambie a True y sea activada

        #Player setup
        self.player_sprite = Player((SCREEN_WIDTH / 2, (SCREEN_HEIGTH) - 10), SCREEN_WIDTH, 5) #objeto instanciado de la clase Player en la posicion del acho de la superfice entre dos y a la altura de la misma menos 10 para subir en el eje 'y' siendo la parte inferior del medio, y con otro parametro de dimension para saber el ancho de la pantalla y limitar movimiento, el 5 es parametro para la velocidad
        self.player = pygame.sprite.GroupSingle(self.player_sprite) #atributo player el cual es un contenedor/grupo para un solo sprite que sera el objeto player_sprite

        #heald and score setup
        self.lives = 3 #atributo para las vidas del jugador las cuales inician con el valor de 3
        self.player_image_path = CURRENT_PATH / 'images' / 'ship.png' #se declara la ruta donde se encuentra la imagen de la nave del jugador
        self.lives_surface = pygame.image.load(self.player_image_path).convert_alpha() #atributo que sera la imagen del jugador para mostrar cuantas vidas se tienen, la cantidad de vidas sera la cantidad de imagenes, dicha imagen es obtenida desde su ruta y a la misma se le ha aplicado el metodo para convertirla en alfa/transparente
        self.lives_x_start = (SCREEN_WIDTH - 35) - (self.lives_surface.get_size()[0] * 2) #atributo que es la posicion inicial donde se colocaran las imagenes correspondientes a las vidas dentro de la ventana/screen(superior dercha) en el eje 'x', dicho valor se obtiene de restar al ancho de la ventana el cual ya se le resto 35, el valor del ancho de la imagen del jugador, para obtener dicho ancho se aplica el metodo get_size()[0] el cual retorna los valores de 'x' y 'y' con el valor de 0 dentro de los corchetes significando que se necesita el primer valor que es 'x' que es el ancho de la imagen, a ese valor se le multiplica por 2 para obtener el ancho de dos imagenes
        self.score = 0 #atributo para el puntaje el cual inicia con el valor 0
        self.font_path = CURRENT_PATH / 'fonts' / 'space_invaders.ttf' #se declara la ruta donde se encuentra la fuente de letra
        self.font_game = pygame.font.Font(self.font_path, 18) #atributo para la fuente de las letras para el juego, se utiliza la clase Font, del modulo font de la libreria de pygame, y se coloca la ruta del archivo de la fuente y el tamaño de fuente
        self.font_title = pygame.font.Font(self.font_path, 30) #atributo para la fuente de las letras para los titulos, se utiliza la clase Font, del modulo font de la libreria de pygame, y se coloca la ruta del archivo de la fuente y el tamaño de fuente

        #Obstacle setup
        self.shape = obstacle.shape #atributo para la forma del obstaculo, se obtiene el array shape del modulo obstacle
        self.block_size = 6 #atributo para el tamaño de cada cuadro que conforma al obstaculo
        self.blocks = pygame.sprite.Group() #grupo donde se agregaran cada uno de los cuadros creados desde el array shape
        self.obstacle_amount = 4 #atributo para la cantidad de obstaculos que se colocaran
        self.obstacle_x_position = [number * (SCREEN_WIDTH / self.obstacle_amount - 25) for number in range(0, self.obstacle_amount)]  #atributo que es un array, para colocar la eparacion entre cada obstaculo, para ello, number va a ser un numero del 0 al 3 por tener 4 obstaculos, dependiendo del valor de number, este valor sera multiplicado por el resultado de dividir al ancho de la pnatalla entre la cantidad de obstaculos mas 25, y se obendra uno por uno un numero en el rango de 0 a la catidad de obstaculos que es 4, asi se colocaran 4 obstaculos sobre la pantalla en el eje 'x' de la misma, dichos numeros se guardan en el array
        self.create_multiple_obstacles(*self.obstacle_x_position, x_start = SCREEN_WIDTH / 7, y_start = 490) #se llama a ejecutar el metodo para crear los obstaculos con los parametros donde se colocara sobre la ventana/superficicie, el primer parametro es el desempaquetado utilizando '*' de los valores obtenidos en dicho atributo que es un array y los siguientes son donde se colocara el primer obstaculo sobre el eje 'x', dicho valor es el ancho de la ventana entre 7.5 para colocar todos los obstaculos centrados en el ancho de la ventana y el eje 'y' sobre la ventana

        #Human setup
        self.humans = pygame.sprite.Group() #grupo de sprites donde estaran colocados todos los objetos human_sprite
        self.human_lasers = pygame.sprite.Group() #grupo donde se agregara el laser del enemigo
        self.human_setup(rows = 5, columns = 10) #se llama a ejecutar la funcion para crear a los enemigos en una posicion especifica, la cual sera una posicion horizontal de 8 enemigos y vertical de 6 filas de enemigos
        self.human_direction = 1 #atributo para mover al grupo de enemigos a la velociadad de 1 pixel en el eje 'x' de la ventana(derecha)

        #Extra setup
        self.extra = pygame.sprite.GroupSingle() #se crea un grupo individual para colocar al enemigo extra
        self.extra_spawn_time = randint(1000, 2000) #se obtiene un numero aleatorio de entre 1000 y 2000 milisegundos para un temporizador

        #Audio
        self.player_explotion_path = CURRENT_PATH / 'sounds' / 'shipexplosion.wav' #se declara la ruta donde se encuentra el sonido de la explosion de la nave del jugador
        self.player_explotion = pygame.mixer.Sound(self.player_explotion_path) #atributo para obtener el archivo del sonido del daño al jugador, se utiliza la funcion Sound() del modulo mixer de pygame, dentro de dicha funcion se coloca la ruta del archivo
        self.player_explotion.set_volume(0.5) #se utiliza la funcion set_volume() para configurar el volumen del sonido

        self.enemy_explotion_path = CURRENT_PATH / 'sounds' / 'invaderkilled.wav' #se declara la ruta donde se encuentra el sonido de un enemigo eliminado
        self.enemy_explotion = pygame.mixer.Sound(self.enemy_explotion_path) #atributo para obtener el archivo del sonido del laser, se utiliza la funcion Sound() del modulo mixer de pygame, dentro de dicha funcion se coloca la ruta del archivo
        self.enemy_explotion.set_volume(1) #se utiliza la funcion set_volume() para configurar el volumen del sonido

        self.laser_enemy_path = CURRENT_PATH / 'sounds' / 'laserenemy.wav' #se declara la ruta donde se encuentra el sonido del laser del enemigo
        self.laser_enemy = pygame.mixer.Sound(self.laser_enemy_path) #atributo para obtener el archivo del sonido del laser, se utiliza la funcion Sound() del modulo mixer de pygame, dentro de dicha funcion se coloca la ruta del archivo
        self.laser_enemy.set_volume(0.2) #se utiliza la funcion set_volume() para configurar el volumen del sonido

        self.extra_sound_path = CURRENT_PATH / 'sounds' / 'mysteryentered.wav' #se declara la ruta donde se encuentra el sonido de la aparicion del enemigo extra
        self.extra_sound = pygame.mixer.Sound(self.extra_sound_path) #atributo para obtener el archivo del sonido de la aparicion del enemigo extra, se utiliza la funcion Sound() del modulo mixer de pygame, dentro de dicha funcion se coloca la ruta del archivo
        self.extra_sound.set_volume(0.3) #se utiliza la funcion set_volume() para configurar el volumen del sonido

        self.extra_explotion_path = CURRENT_PATH / 'sounds' / 'mysterykilled.wav' #se declara la ruta donde se encuentra el sonido de la eliminacion del enemigo extra
        self.extra_explotion = pygame.mixer.Sound(self.extra_explotion_path) #atributo para obtener el archivo del sonido del daño al enemigo extra, se utiliza la funcion Sound() del modulo mixer de pygame, dentro de dicha funcion se coloca la ruta del archivo
        self.extra_explotion.set_volume(0.5) #se utiliza la funcion set_volume() para configurar el volumen del sonido


    def create_obstacle(self, x_start, y_start, offset_x): #metodo para crear un obstaculo con los parametros donde se colocaran en sus respectivos ejes, primero en donde se epezara a colocar en el eje 'x', despues en el eje 'y' y final la separacion entre ellos
        for row_index, row in enumerate(self.shape): #ciclo que itera/recorre por cada indice de las filas, en las filas del array shape, se obtiene un nuero entero con el metodo enumerate() el cual es el indice de las filas y dicho numero se asigna a row_index, lo cual sera la altura del obstaculo
            for col_index, col in enumerate(row): #ciclo que itera/recorre por cada indice de las columnas en las filas del array shape, se obtiene un nuero entero con el metodo enumerate() y dicho numero se asigna a col_index, asi se obtiene la posicion exacta de cada una de las x dentro del array shape
                if col == 'x': #condicional que valida si cada elemento de cada columna en las filas del array shape es igual a 'x'
                    x = x_start + col_index * self.block_size + offset_x #se declara la variable 'x' y se le asigna el valor del resultado de multiplicar el indice de la columna por el tamaño del cuadro, y sumando el espacio inical en el eje 'x' que es a la izquierda y sumando el espacio entre cada uno de los obstaculos, asi obtenido la posicion del primer bloque en el eje 'x'
                    y = y_start + row_index * self.block_size #se declara la variable 'y' y se le asigna el valor del resultado de multiplicar el indice obtenido de la fila por el tamaño del bloque mas la posicion inicial donde se colocara en el eje 'y', asi oteniendo la posicion en el eje 'y' donde se colocara sobre la superficie/ventana
                    block = obstacle.Block(self.block_size, PURPLE, x, y ) #se declara la variable block el cual sera un bloque que coformara al obstaculo, para ello se instancia un obejto desde el modulo obstacle utilizando la clase Block con los parametros empezando por el tamaño del bloque, el color usando es morado y la posicion en el eje 'x' y en el 'y'
                    self.blocks.add(block) #se agrega al grupo blocks cada uno de los bloques creados mediante los ciclos for


    def create_multiple_obstacles(self,*offset, x_start, y_start): #metodo para crear varios obstaculos, *offset es la separacion que tendran entre cada obstaculo cuyo valor ya es colocado en una tupla al utilizar '*' y al momento de colocar los valores al llamar a ejecutar el metodo estos seran leidos como su estuviran dentro de una tupla y con los parametros para saber desde que posicion se colocaran sobre la ventana sobre sus respectivos ejes
        for offset_x in offset: #ciclo que itera por cada valor de separacion en el eje 'x' sore los valores de *offset
            self.create_obstacle(x_start, y_start, offset_x) #se ejecuta la funcion create_obstacle() con los parametros de colocacion en los ejes 'x' y 'y', y el valor de separacion en el eje 'x'


    def human_setup(self, rows, columns, x_distance = 50, y_distance = 50, x_offset = 110, y_offset = 80): #metodo para crear los enemigos en en una posicion especifica, la cual tendra una cantidad de filas y columnas de enemigos, y la distancia de separacion entre cada enemigo en el eje 'x' y en el eje 'y' y la separacion del cojunto de los enemigos en el eje 'x' y 'y'
        for row_index, row in enumerate(range(rows)): #ciclo para recorrer cada fila del rango filas y obtener su indice en enumerate() y asignarlo a row_index
            for col_index, column in enumerate(range(columns)): #ciclo para recorrer cada columna del rango columnas y obtener su indice con enumerate() y asignarlo a col_index
                x = col_index * x_distance + x_offset#para la posicion en el eje 'x' se multiplicara el numero del indice de las columnas por la distancia de 'x' de cada enemigo y se suma la compensacion del eje 'x'
                y = row_index * y_distance + y_offset #para la posicion en el eje 'y' se multiplicara el numero del indice de las filas por la distancia de 'y' de cada enemigo y se suma la compensacion del eje 'y'

                if row_index == 0: #condicional que evalua si el indice de la fila es igual a 0
                    human_sprite = Human('purple', x, y) #se instancia/crea un objeto/sprite de la clase Human con los valores para los parametros empezando por el color, la posicion que tendra al colocarse en el eje 'x' y la posicion que tendra al colocarse en el eje 'y'
                elif 1 <= row_index <= 2: #condicional que evalua si no es la condicion anterior, si 1 es menor o igual al indice de la fila que a su vez es menor o igual a 2, para que se ejecute el codigo si las estan entre el indice 1 y 2
                    human_sprite = Human('blue', x, y) #se instancia/crea un objeto/sprite de la clase Human con los valores para los parametros empezando por el color, la posicion que tendra al colocarse en el eje 'x' y la posicion que tendra al colocarse en el eje 'y'
                else: #si no es ninguna de las condiciones anteriores lo cul seran las filas restantes que son las filas en los indices 3 y 4
                    human_sprite = Human('green', x, y) #se instancia/crea un objeto/sprite de la clase Human con los valores para los parametros empezando por el color, la posicion que tendra al colocarse en el eje 'x' y la posicion que tendra al colocarse en el eje 'y'

                self.humans.add(human_sprite) #se agregan al grupo humans cada uno de los objetos/sprites creados de la clase Human()


    def human_position_limit(self): #metodo para limitar el movimiento del grupo de enemigos y cambiar su dereccion de movimieto horzontal
        if len(self.humans) > 1: #condicional para validar si la longitud del grupo de stprites humans es mayor que 1
            all_humans = self.humans.sprites() #variable que contiene el grupo de enemigos al cual se le aplica el metodo sprites() para que cada enemigo dentro del grupo pueda interactuar
            for human in all_humans: #ciclo para iterar por cada enemigo dentro del grupo humans
                if human.rect.right >= SCREEN_WIDTH: #condicional para validar si la parte derecha de cada rectangulo el cual es el objeto sobre el que esta pintado la imagen del enemigo, se encuentra en un valor mayor o igual al ancho de la ventana/superficie/screen
                    self.human_direction = -1 #se reasigan el valor del atributo human_direction colocando el valor negativo del original, haciendo que el grupo de enemigos se muevan de manera negativa en el eje 'x'(izquierda) de la ventana a la velocidad de 1 pixel
                    self.human_move_dow(2) #se llama a ejecutar el metodo para mover hacia abajo el grupo de enemigos a una distancia de dos pixeles en el eje 'y'
                elif human.rect.left <= 0: #condicional para validar si la parte izquierda de cada rectangulo el cual es el objeto sobre el que esta pintado la imagen del enemigo, se encuentra en un valor menor o igual a 0 en el eje 'y'
                    self.human_direction = 1 #se reasigan el valor del atributo human_direction colocando el valor positivo de nuevo, haciendo que el grupo de enemigos se muevan de manera postiva en el eje 'x'(derecha) de la ventana a la velocidad de 1 pixel
                    self.human_move_dow(2) #se llama a ejecutar el metodo para mover hacia abajo el grupo de enemigos a una distancia de 2 pixeles en el eje 'y'
        elif len(self.humans) == 1: #para validar si la longitud del grupo de stprites humans es igual a 1
            all_humans = self.humans.sprites() #variable que contiene el grupo de enemigos al cual se le aplica el metodo sprites() para que cada enemigo dentro del grupo pueda interactuar
            for human in all_humans: #ciclo para iterar por cada enemigo dentro del grupo humans
                if human.rect.right >= SCREEN_WIDTH: #condicional para validar si la parte derecha de cada rectangulo el cual es el objeto sobre el que esta pintado la imagen del enemigo, se encuentra en un valor mayor o igual al ancho de la ventana/superficie/screen
                    self.human_direction = - 6 #se reasigan el valor del atributo human_direction colocando el valor negativo del original, haciendo que el grupo de enemigos se muevan de manera negativa en el eje 'x'(izquierda) de la ventana a la velocidad de 6 pixeles
                    self.human_move_dow(25) #se llama a ejecutar el metodo para mover hacia abajo el grupo de enemigos a una distancia de 15 pixeles en el eje 'y'
                elif human.rect.left <= 0: #condicional para validar si la parte izquierda de cada rectangulo el cual es el objeto sobre el que esta pintado la imagen del enemigo, se encuentra en un valor menor o igual a 0 en el eje 'y'
                    self.human_direction = 6 #se reasigan el valor del atributo human_direction colocando el valor positivo de nuevo, haciendo que el grupo de enemigos se muevan de manera postiva en el eje 'x'(derecha) de la ventana a la velocidad de 6 pixeles
                    self.human_move_dow(25) #se llama a ejecutar el metodo para mover hacia abajo el grupo de enemigos a una distancia de 15 pixeles en el eje 'y'


    def human_move_dow(self, distance): #metodo para mover al grupo de enemigos hacia abajo cada vez que el algun enemigo del grupo golpee la parte izquierda o derecha de la ventana
        if self.humans: #condicionar que valida si son enemigos dentro del grupo humans, solo asi se ejecutara el ciclo siguiente, para que al momento de que ya no haya enemigos se deje de ejecutar dicho ciclo
            for human in self.humans.sprites(): #ciclo para iterar por cada enemigo dentro del grupo humans al cual se le aplica el metodo sprites() para que cada enemigo dentro del grupo pueda interactuar
                human.rect.y += distance #al valor 'y' el cual es la posicion en el eje 'y' dentro de la ventana/screen, del rectangulo el cual es el objeto sobre el que esta pintado la imagen del enemigo, se le asigna su valor mas el de distance el cual es la distancia que se movera hacia abajo y sera asignado al momento de llamar a ejecutar el metodo


    def human_shoot(self): #metodo para que el enemigo dispare
        if len(self.humans) > 1: #condicional para validar si la longitud del grupo de stprites humans es mayor que 1
            random_human = choice(self.humans.sprites()) #se ejecuta la funcion choice para seleccionar un sprite/objeto aleatorio del grupo humans
            laser_sprite = LaserEnemy(random_human.rect.center, SCREEN_HEIGTH, 10) #objeto instanciado/creado de la clase LaserEnemy el cual tiene como parametros la posicion central del rectangulo obtenido a base de la imagen del laser del enemigo para colocarlo en medio de la imagen del enemigo, el parametro SCREEN_HEIGTH como limite de altura para que se destruya cuando el laser esté debajo de la altura de la parte inferior del jugador y 8 para la velocidad de movimiento del laser sobre la ventana
            self.human_lasers.add(laser_sprite) #al atributo human_lasers se le aplica el metodo add() para agregar el objeto laser_sprite insatanciado de la clase LaserEnemy dentro del grupo human_lasers
            self.laser_enemy.play() #se utiliza la funcion play() para reproducir el sonido cada vez que se ejecute la funcion
        elif len(self.humans) == 1: #para validar si la longitud del grupo de stprites humans es igual a 1
            random_human = choice(self.humans.sprites()) #se ejecuta la funcion choice para seleccionar un sprite/objeto aleatorio del grupo humans
            laser_sprite = LaserEnemy(random_human.rect.center, SCREEN_HEIGTH, 15) #objeto instanciado/creado de la clase LaserEnemy el cual tiene como parametros la posicion central del rectangulo obtenido a base de la imagen del laser del enemigo para colocarlo en medio de la imagen del enemigo, el parametro SCREEN_HEIGTH como limite de altura para que se destruya cuando el laser esté debajo de la altura de la parte inferior del jugador y 15 para la velocidad de movimiento del laser sobre la ventana
            self.human_lasers.add(laser_sprite) #al atributo human_lasers se le aplica el metodo add() para agregar el objeto laser_sprite insatanciado de la clase LaserEnemy dentro del grupo human_lasers
            self.laser_enemy.play() #se utiliza la funcion play() para reproducir el sonido cada vez que se ejecute la funcion



    def extra_human_timer(self): #metodo para ser un temporizador de aparicion del enemigo extra
        self.extra_spawn_time -= 1 #al atributo extra_spawn_time que ya sera un numero aleatorio de entre 1500 y 2000, se le restara 1 a su valor cada vez que se ejecute el metodo
        if self.extra_spawn_time <= 0: #condicional para saber si el valor del atributo extra_spawn_time ha llegado a 0
            self.extra.add(Extra(choice(['right','left']), SCREEN_WIDTH)) #al grupo individual 'extra' se le agrega el objeto instanciado de la clase Extra, con el parametro para saber el lado de aparicion el cual sera aleatorio de entre dos opciones dentro de una lista, y el otro parametro el lugar donde se movera dicho enemigo el cual sera el eje 'x' de la ventana(horizontal)
            self.extra_spawn_time = randint(1500, 1800) #se vuelve a obtener un nuevo numero aleatorio den entre 1500 y 1800 para que se repita el proceso de aparicion del enemigo
            self.extra_sound.play() ##se utiliza la funcion play() para reproducir el sonido cada vez que se cumpla la condicion del timer llegado a 0


    def collision_checks(self): #metodo para comprobar las diferentes colisiones entre los distintos sprites/objetos
        #Player lasers
        if self.player.sprite.lasers: #condicional para validar si hay/se disparo algun laser del jugador
            for laser in self.player.sprite.lasers: #ciclo para iterar por cada laser agregado/disparado dentro del grupo unico lasers
                #obstacle collision
                if pygame.sprite.spritecollide(laser, self.blocks, True): #condicional para validar si hubo una colision de sprites, el primer parametro es el sprite principal, el segundo es contra que sprite hubo colision y el tercero es el valor que tendra la funcion kill() para eliminar dicho esprite con el que se ha colisionado
                    laser.kill() #se aplica el metodo kill() al sprite laser disparado que se encuantre dentro del grupo lasers
                
                #human collision
                humans_hit = pygame.sprite.spritecollide(laser, self.humans, True) #si hubo una colision de sprites/con un objeto human, el primer parametro es el sprite principal/laser del jugador, el segundo es contra que sprite hubo colision y el tercero es el valor que tendra la funcion kill() para eliminar dicho esprite con el que se ha colisionado
                if humans_hit: #condicional para validar si hubo una colision lo cual es un valor aignado a human_hit
                    for human in humans_hit: #ciclo para iterar por cada human/sprite que se encuentre dentro de la variable humans_hit
                        self.score += human.value #el valor del atributo score se le agrega su mismo valor mas el valor del atributo value del human/sprite dentro de humans_hit, asi se agregara el valor correspondiente al human colisionado el sprite principal
                    laser.kill() #se aplica el metodo kill() al sprite laser disparado que se encuantre dentro del grupo lasers para eliminarlo al momento de la colision
                    self.enemy_explotion.play() #se utiliza la funcion play() para reproducir el sonido cada vez que se ejecute la funcion
                
                #laser enemy
                laser_hit = pygame.sprite.spritecollide(laser, self.human_lasers, True) #variable que tiene el valor asignado de una colisión de un sprite/laser del jugador con un laser del enemigo, el primer parámetro es el objeto/sprite principal, el segundo el el sprite con el que colisiona el principal y el tercero es el valor que tendra la funcion kill() para eliminar dicho esprite con el que se ha colisionado el sprite principal
                if laser_hit: #condicional para validar si hubo una colision lo cual es un valor asignado a laser_hit
                    for laser in laser_hit: #ciclo para iterar por cada laser/sprite que se encuentre dentro de la variable humans_hit
                        laser.kill() #se aplica el metodo kill() al sprite laser disparado que se encuantre dentro del grupo lasers para eliminarlo al momento de la colision

                #extra collision
                if pygame.sprite.spritecollide(laser, self.extra, True): #condicional para validar si hubo una colision de sprites, el primer parametro es el sprite principal, el segundo es contra que sprite hubo colision y el tercero es el valor que tendra la funcion kill() para eliminar dicho esprite con el que se ha colisionado
                    self.score += 500 #al atributo socre se le aumenta su mismo valo mas 500 que es el valor del enemigo extra
                    laser.kill() #se aplica el metodo kill() al sprite laser disparado que se encuantre dentro del grupo lasers
                    self.extra_explotion.play() #se utiliza la funcion play() para reproducir el sonido cada vez que se ejecute la funcion
                    
        #Enemy lasers
        if self.human_lasers: #condicional para validar si hay/se disparo algun laser del enemigo
            for laser in self.human_lasers: #ciclo para iterar por cada laser agregado/disparado dentro del grupo human_lasers
                #obstacle collision
                if pygame.sprite.spritecollide(laser, self.blocks, True): #condicional para validar si hubo una colision de sprites, el primer parametro es el sprite principal, el segundo es contra que sprite hubo colision y el tercero es el valor que tendra la funcion kill() para eliminar el sprite con el que ha colisionado el principal
                    laser.kill() #se aplica el metodo kill() al sprite laser disparado que se encuantre dentro del grupo human_lasers
                
                #player collision
                if pygame.sprite.spritecollide(laser, self.player, False): #condicional para validar si hubo una colision de sprites, el primer parametro es el sprite principal, el segundo es contra que sprite hubo colision y el tercero es el valor que tendra la funcion kill() para NO eliminar el sprite con el que ha colisionado el principal
                    laser.kill() #se aplica el metodo kill() al sprite laser disparado que se encuantre dentro del grupo human_lasers
                    self.player_explotion.play() #se utiliza la funcion play() para reproducir el sonido cada vez que se ejecute la funcion
                    self.lives -= 1 #al valor del atributo lives se le restara su mismo valor menos 1 cada vez que haya una colison del laser del enemigo con el jugador, asi se eliminara un vida y una imagen de vida

        #enemies
        if self.humans: #condicional para validar si hay enemigos dentro del grupo humans
            for human in self.humans: #ciclo que itera cada sprite human dentro del grupo humans
                #obstacle collision
                pygame.sprite.spritecollide(human, self.blocks, True) #se ejecuta la colision contra un bloque de los obstaculo, la cual tiene como parametros el primero es el sprite principal, el segundo es con que colisiona y el tercero es el valor de la funcion kill() para eliminar el sprite con el que ha colisionado el principal

                #player collision
                if pygame.sprite.spritecollide(human, self.player, False): #condicional para validar si hubo una colision de sprites, el primer parametro es el sprite principal, el segundo es contra que sprite hubo colision y el tercero es el valor que tendra la funcion kill() para NO eliminar el sprite con el que ha colisionado el principal
                    self.lives = 0 #al valor del atributo se le asigna el valor de 0 para ejecutar correctamente el metodo game_over()
                    self.game_over() #se llama a ejecutar el metodo game_over() para colocar el texto de derrota cuando se cumpla la condicion necesaria

                #screen Height
                if human.rect.y + 20 >= SCREEN_HEIGTH: #condicional para validar el el largo del sprite human mas 20 pixeles es mayor o igual al largo de la superficice/ventana
                    self.lives = 0 #al valor del atributo se le asigna el valor de 0 para ejecutar correctamente el metodo game_over()
                    self.game_over() #se llama a ejecutar el metodo game_over() para colocar el texto de derrota cuando se cumpla la condicion necesaria


    def main_menu(self): #metodo para crear el menu principal el cual será la ventana inicial
        image_background_path = CURRENT_PATH / 'images' / 'background.jpg' #se declara la ruta donde se encuentra la imagen del fondo
        image_background = pygame.image.load(image_background_path) #variable que obtendra la imagen del fondo desde su ruta
        enemy1_path = CURRENT_PATH / 'images' / 'green.png' #se declara la ruta donde se encuentra la imagen del enemigo verde
        enemy1 = pygame.image.load(enemy1_path) #variable que obtendra la imagen del enemigo verde desde su ruta
        enemy2_path = CURRENT_PATH / 'images' / 'blue.png' #se declara la ruta donde se encuentra la imagen del enemigo azul
        enemy2 = pygame.image.load(enemy2_path) #variable que obtendra la imagen del enemigo azul desde su ruta
        enemy3_path = CURRENT_PATH / 'images' / 'purple.png' #se declara la ruta donde se encuentra la imagen del enemigo rojo
        enemy3 = pygame.image.load(enemy3_path) #variable que obtendra la imagen del enemigo rojo desde su ruta
        enemy4_path = CURRENT_PATH / 'images' / 'extra.png' #se declara la ruta donde se encuentra la imagen del enemigo extra
        enemy4 = pygame.image.load(enemy4_path) #variable que obtendra la imagen del enemigo extra desde su ruta

        titleText_surfce = self.font_title.render(f"Human Invaders", False, 'white') #se crea una superficie para el texto del titulo, el cual sera un texto renderizado como imagen, el primer parametro es el texto, el segundo es el valor del antialiasing en Falsa para que se mantega pixelado y el tercero es el color del texto
        titleText_rect = titleText_surfce.get_rect(center = (SCREEN_WIDTH / 2, (SCREEN_HEIGTH / 2) - 120)) #se obtiene un rectangulo a partir de la superfiice anterior, el cual se colocara en el centro de la ventana, obteniendo la mitad del valor del ancho y alto del SCREEN/ventana y se le agrega un valor para separarlo verticalmanete

        titleText2_surface = self.font_game.render(f"START  -PRESS ENTER-", False, 'white') #se crea una superficie para el texto para pasar a la siguiente ventana, el cual sera un texto renderizado como imagen, el primer parametro es el texto, el segundo es el valor del antialiasing en Falsa para que se mantega pixelado y el tercero es el color del texto
        titleText2_rect = titleText2_surface.get_rect(center = (SCREEN_WIDTH / 2, (SCREEN_HEIGTH / 2) - 60)) #se obtiene un rectangulo a partir de la superfiice anterior, el cual se colocara en el centro de la ventana, obteniendo la mitad del valor del ancho y alto del SCREEN/ventana y se le agrega un valor para separarlo verticalmanete

        enemy1Text_surface = self.font_game.render(f"   =   100 pts", False, 'green') #se crea una superficie para el texto del valor del enemigo, el cual sera un texto renderizado como imagen, el primer parametro es el texto, el segundo es el valor del antialiasing en Falsa para que se mantega pixelado y el tercero es el color del texto
        enemy1Tex_rect = enemy1Text_surface.get_rect(center = ((SCREEN_WIDTH / 2) + 20, SCREEN_HEIGTH / 2)) #se obtiene un rectangulo a partir de la superfiice anterior, el cual se colocara en el centro de la ventana, obteniendo la mitad del valor del ancho y alto del SCREEN/ventana y se le agrega un valor para separarlo verticalmanete

        enemy2Text_surface = self.font_game.render(f"   =  200 pts", False, 'aqua') #se crea una superficie para el texto del valor del enemigo, el cual sera un texto renderizado como imagen, el primer parametro es el texto, el segundo es el valor del antialiasing en Falsa para que se mantega pixelado y el tercero es el color del texto
        enemy2Text_rect = enemy2Text_surface.get_rect(center = ((SCREEN_WIDTH / 2) + 20, (SCREEN_HEIGTH / 2) + 50)) #se obtiene un rectangulo a partir de la superfiice anterior, el cual se colocara en el centro de la ventana, obteniendo la mitad del valor del ancho y alto del SCREEN/ventana y se le agrega un valor para separarlo verticalmanete

        enemy3Text_surface = self.font_game.render(f"   =  300 pts", False, 'purple') #se crea una superficie para el texto del valor del enemigo, el cual sera un texto renderizado como imagen, el primer parametro es el texto, el segundo es el valor del antialiasing en Falsa para que se mantega pixelado y el tercero es el color del texto
        enemy3Text_rect = enemy3Text_surface.get_rect(center = ((SCREEN_WIDTH / 2) + 20, (SCREEN_HEIGTH / 2) + 100)) #se obtiene un rectangulo a partir de la superfiice anterior, el cual se colocara en el centro de la ventana, obteniendo la mitad del valor del ancho y alto del SCREEN/ventana y se le agrega un valor para separarlo verticalmanete

        enemy4Text_surface = self.font_game.render(f"   =  500 pts", False, 'red') #se crea una superficie para el texto del valor del enemigo, el cual sera un texto renderizado como imagen, el primer parametro es el texto, el segundo es el valor del antialiasing en Falsa para que se mantega pixelado y el tercero es el color del texto
        enemy4Text_rect = enemy4Text_surface.get_rect(center = ((SCREEN_WIDTH / 2) + 20, (SCREEN_HEIGTH / 2) + 150)) #se obtiene un rectangulo a partir de la superfiice anterior, el cual se colocara en el centro de la ventana, obteniendo la mitad del valor del ancho y alto del SCREEN/ventana y se le agrega un valor para separarlo verticalmanete

        SCREEN.blit(image_background, (0,0)) #se coloca/dibuja sobre la ventana/superficie mediante blit(), la imagen del fondo desde las posiciones (0, 0) en los ejes 'x' y 'y'
        SCREEN.blit(titleText_surfce, titleText_rect) #se coloca/dibuja sobre la ventana/superficie mediante blit(), la superficie y el rectangulo obtenido de dicha superficie
        SCREEN.blit(titleText2_surface, titleText2_rect)#se coloca/dibuja sobre la ventana/superficie mediante blit(), la superficie y el rectangulo obtenido de dicha superficie

        SCREEN.blit(enemy1Text_surface, enemy1Tex_rect)#se coloca/dibuja sobre la ventana/superficie mediante blit(), la superficie y el rectangulo obtenido de dicha superficie
        SCREEN.blit(enemy1, (((SCREEN_WIDTH / 2) - 80), ((SCREEN_HEIGTH / 2)) - 10)) #se coloca/dibuja sobre la ventana/superficie mediante blit(), la imagen obtenida mediante su ruta, a la altura del centro de la pantalla y un valor extra para separar la imagen de su texto correspondiente horizontalmente y de las demas imagenes verticalmente

        SCREEN.blit(enemy2Text_surface, enemy2Text_rect)#se coloca/dibuja sobre la ventana/superficie mediante blit(), la superficie y el rectangulo obtenido de dicha superficie
        SCREEN.blit(enemy2, (((SCREEN_WIDTH / 2) - 80), ((SCREEN_HEIGTH / 2)) + 40)) #se coloca/dibuja sobre la ventana/superficie mediante blit(), la imagen obtenida mediante su ruta, a la altura del centro de la pantalla y un valor extra para separar la imagen de su texto correspondiente horizontalmente y de las demas imagenes verticalmente

        SCREEN.blit(enemy3Text_surface, enemy3Text_rect)#se coloca/dibuja sobre la ventana/superficie mediante blit(), la superficie y el rectangulo obtenido de dicha superficie
        SCREEN.blit(enemy3, (((SCREEN_WIDTH / 2) - 80), ((SCREEN_HEIGTH / 2)) + 80)) #se coloca/dibuja sobre la ventana/superficie mediante blit(), la imagen obtenida mediante su ruta, a la altura del centro de la pantalla y un valor extra para separar la imagen de su texto correspondiente horizontalmente y de las demas imagenes verticalmente

        SCREEN.blit(enemy4Text_surface, enemy4Text_rect)#se coloca/dibuja sobre la ventana/superficie mediante blit(), la superficie y el rectangulo obtenido de dicha superficie
        SCREEN.blit(enemy4, (((SCREEN_WIDTH / 2) - 115), ((SCREEN_HEIGTH / 2)) + 130)) #se coloca/dibuja sobre la ventana/superficie mediante blit(), la imagen obtenida mediante su ruta, a la altura del centro de la pantalla y un valor extra para separar la imagen de su texto correspondiente horizontalmente y de las demas imagenes verticalmente


        self.laser_enemy.set_volume(0) #el volumen de los lasers del enemigo es 0 para que no se escuchen
        for laser in self.human_lasers: #ciclo para iterar dentro del grupo human_lasers
            pygame.sprite.Sprite.kill(laser) #se eliminan los todos los lasers del enemigo que se encuentren dentro del grupo

        keys = pygame.key.get_pressed() #variable que obtiene una lista de las teclas que se pueden presionar, dicho metodo pertenece al modulo keys y a su vez dicho modulo pertenece al modulo pygame
        if keys[pygame.K_RETURN]: #condicional para validar si la tecla presioanda es RETURN/ENTER
            self.mainScreen = False #el valor del atributo cambia a False para NO mostrar la ventana del menu principal
            self.startGame = True #el valor del atributo cambia a True para mostrar la ventana del juego y este inicie
            self.windows() #se llama a ejecutar el metodo windows() para colocar el texto de derrota cuando se cumpla la condicion necesaria dependiendo de los valores de los atributos


    def display_lives(self): #metodo para colocar lasimagenes de las vidas del jugador sobre la ventana/screen
        for live in range(self.lives - 1): #ciclo para iterar sobre el valor/vida del atributo self.lives el cual es 3 y a ese valor se le resta uno para que al momento de tener una sola vida ya no se muestre ninguna imagen y al tener 3 vidas solo se muestan 2 imagenes
            x = self.lives_x_start + (live * ((self.lives_surface.get_size()[0]) + 10)) #el valor donde se colocaran las imagenes de las vidas sobre la ventana en el eje 'x', el cual es el resultado de sumar la posicion inicial en el eje 'x' que es la parte derecha, el valor de multiplicar cada valor/vida dentro de la varible vidas(1 o 2) por el tamaño del ancho de la imagen para las vidas que tiene sumado 10 para separa cada imagn y a ese resulatdo se le resta 5 para moverlos un poco hacia la izquierda, asi se colocaran dos imagenes una a lado de la otra en la esquina superior derecha
            SCREEN.blit(self.lives_surface, (x, 8)) #se pintara sobre la ventana la imagen para las vidas en la posicion en sus respectivos ejes, en 'x' con el valor de la varible 'x', y en 'y' con el valor de 8 ya que asi se coloca cerca de la parte superior


    def extract_high_score(self): #metodo para obtener el mayor puntaje desde el archivo score.txt
        self.score_order = [] #atributo que es una lista vacia donde se colocaran los valores/puntajes del archivo score.txt
        with open(SCORE_PATH, 'r') as file: #se utiliza el contexto 'with' para crear la variable 'file' la cual tiene el valor asignado de abrir el documeto desde su ruta y con el tipo de gestion archivos de lectura para obtener los puntajes dentro del archivo correspondiete(score.txt)
            for line in file.readlines(): #ciclo para iterar por cada liena dentro del archivo 'score.txt' al cual se le aplica el metodo para leer linea por linea
                score = line.replace('\n', '') #variable a la cual se le asigna el valor de cada linea con el string '\n' remplazado por nada para tener solo un numero que sigue siendo un string
                self.score_order.append(int(score)) #a la lista se le van ingresando los valores de la variable score los cuales primero son convertidos a valores de numeros enteros
        self.score_order.sort(reverse=True) #al los valores dentro de la lista se le aplica el metodo sort() para ordenar dichos valores ya siendo numero enteros y en dicho metodo se le coloca el parametro reverse con el valor asignado de True para ordenarlo con el mayor valor en el primer indice
        self.high_score = max(self.score_order) #atributo el cual es una variable que tiene asignado el mayor valor de la lista self.score_order, utilizando la funcion max() con el nombre de la lista que contiene los scores ya ordenados


    def display_score(self): #metodo para colocar el texto y la puntuacion del jugador sobre la ventana/screen
        self.extract_high_score() #se llama a ejecutar el metodo extract_high_score() cada vez que se tenga que mostrar el score actual y el mas alto para colocar ambos scores

        score_surface = self.font_game.render(f"score: {self.score}", False, 'white') #variable que sera la superficie/imagen la cual sera un renderizado de un texto el cual es "score {}" y dentro de las llaves se colocara el valor del atributo score el cual sera convetido a texto, se coloca Fasle para el antialiasing, asi se las letras se mostraran mas pixeladas y se le coloca el color blanco
        score_rect = score_surface.get_rect(topleft = (20, 10)) #se crea un rectangulo a base de la superficie creada con el texto el cual se colocara a en parte superior izquierda con un desplazamiento positivo de 20 pixeles en el eje 'x' y 10 pixeles en el eje 'y'
        SCREEN.blit(score_surface, score_rect) #se coloca/pinta sobre la superficie/screen la imagen y el recatgulo para el score/puntaje

        high_score_surface = self.font_game.render(f"high score: {self.high_score}", False, 'white') #variable que sera la superficie/imagen la cual sera un renderizado de un texto el cual es "high score: {}"" y dentro de las llaves se colocara el valor del atributo score el cual sera convetido a texto, se coloca Fasle para el antialiasing, asi se las letras se mostraran pixeladas y se le coloca el color blanco
        high_score_rect = high_score_surface.get_rect(topleft = (180, 10)) #se crea un rectangulo a base de la superficie creada con el texto el cual se colocara a en parte superior izquierda con un desplazamiento positivo de 10 pixeles en el eje 'y'(vertical) y de 180 pixeles en el eje 'x'(horizontal), asi se colocara a un lado del score actual
        SCREEN.blit(high_score_surface, high_score_rect) #se coloca/pinta sobre la superficie/screen la imagen y el recatgulo para el hight score/puntaje mas alto

    
    def superate_high_score(self): #metodo para mostrar si se ha obtenido un puntaje mas alto
        if self.score > self.high_score: #condicional para validar si el valor del socre actual es mayor que el score mas alto
            new_score_surface = self.font_title.render(f"- NEW HIGH SCORE -", False, 'white') #variable que sera la superficie/imagen la cual sera un renderizado de un texto el cual es "- NEW HIGH SCORE -", se coloca Fasle para el antialiasing asi se las letras se mostraran mas pixeladas y se le coloca el color blanco
            new_score_rect = new_score_surface.get_rect(center = (SCREEN_WIDTH / 2, (SCREEN_HEIGTH / 2) - 120)) #variable donde se obtiene un rectangulo a base de la superficie obtenida de renderizar el texto como una imagen, dicho rectangulo con el texto se mostrara en el centro de la ventana, para ello se obtienen los valores del ancho y el alto de dicha ventana y esos valores de dividen entre dos para que asi dicho recangulo se coloque en el centro de la ventana y al alto se le resta un valor para colocarlo mas arriba
            SCREEN.blit(new_score_surface, new_score_rect) #se dibuja/coloca sobre la ventana/screen mediante la funcion blit() la superifie con el texto y el rectangulo para posicionar dicho texto


    def victory_message(self): #metodo para mostrar un mesaje de victoria
        if not self.humans.sprites(): #condiconal para validaar si ya no se encuentra ningun spritet/objeto human dentro del grupo humans
            victory_surface = self.font_title.render(f"YOU WON", False, 'white') #variable que sera la superficie/imagen la cual sera un renderizado de un texto el cual es "YOU WON", se coloca Fasle para el antialiasing asi se las letras se mostraran mas pixeladas y se le coloca el color blanco
            victory_rect = victory_surface.get_rect(center = (SCREEN_WIDTH / 2, (SCREEN_HEIGTH / 2) - 50)) #variable donde se obtiene un rectangulo a base de la superficie obtenida de renderizar el texto como una imagen, dicho rectangulo con el texto se mostrara en el centro de la ventana, para ello se obtienen los valores del ancho y el alto de dicha ventana y esos valores de dividen entre dos para que asi dicho recangulo se coloque en el centro de la ventana
            SCREEN.blit(victory_surface, victory_rect) #se dibuja/coloca sobre la ventana/screen mediante la funcion blit() la superifie con el texto de victoria y el rectangulo para posicionar dicho texto

            score_surface = self.font_game.render(f"YOU SCORE : " + f"{self.score}", False, 'white') #se crea una superficie/imagen la cual sera un texto renderizado a imagen, utilizando la fuente de letra, y se renderizara eltexto "YOU SCORE : ", concatenado con el valor renderizado a texto de "{self.score}", se coloca false para no colocar suavisado al texto y se coloca el color 'white'
            score_rect = score_surface.get_rect(center = ((SCREEN_WIDTH / 2), (SCREEN_HEIGTH / 2) + 50)) #se obtiene un rectangulo a base de la superficie obtenida de renderizar el texto como una imagen, dicho rectangulo con el texto se mostrara en el centro de la ventana con un desplazamiento hacia abajo, para ello se obtienen los valores del ancho y el alto de dicha ventana/SCREEN y esos valores de dividen entre dos para que asi dicho recangulo se coloque en el centro de la ventana, al valor del alto se le suma el desplazamiento
            SCREEN.blit(score_surface, score_rect) #se coloca/pinta sobre la superficie/screen la imagen y el recatgulo para el score/puntaje

            continue_surface = self.font_game.render(f"SCORES  -PRESS ENTER-", False, 'white') #variable que sera la superficie/imagen la cual sera un renderizado de un texto el cual es "SCORES -PRESS ENTER-", se coloca Fasle para el antialiasing asi se las letras se mostraran mas pixeladas y se le coloca el color blanco
            continue_rect = continue_surface.get_rect(center = (SCREEN_WIDTH / 2, (SCREEN_HEIGTH / 2) + 100)) #variable donde se obtiene un rectangulo a base de la superficie obtenida de renderizar el texto como una imagen, dicho rectangulo con el texto se mostrara en el centro de la ventana, para ello se obtienen los valores del ancho y el alto de dicha ventana y esos valores de dividen entre dos para que asi dicho recangulo se coloque en el centro de la ventana y se suma un valor para que se coloque por debajo del centro horizontalmente
            SCREEN.blit(continue_surface, continue_rect) #se dibuja/coloca sobre la ventana/screen mediante la funcion blit() la superifie con el texto y el rectangulo para posicionar dicho texto

            for player in self.player: #ciclo que itera cada elemento/sprite player dentro del grupo unico player
                player.speed = 0 #al atributo speed del sprite player se le reasigna el valo de 0 para evitar el movimiento
                player.ready = False #al atributo ready se le reasigna el valor de False para evitar que dispare
            for human in self.humans: #ciclo que itera cada elemento/sprite human dentro del grupo humans
                self.human_direction = 0 #al atributo human_direction de cada sprite human dentro del grupo, se le reasigna el valor de 0 para evitar el movimiento
            for extra in self.extra: #ciclo que itera cada elemento/sprite extra dentro del grupo unico extra
                pygame.sprite.Sprite.kill(extra) #se utiliza la funcion kill(extra) de la clase Sprite del modulo sprite de la libreria pygame, el eobjeto/sprite a eliminar es el extra dentro del grupo unico extra
                extra.speed = 0 #al atributo speed del sprite extra se le reasigna el valo de 0 para evitar el movimiento
            
            self.extra_sound.set_volume(0) #al atributo extra_sound del sprite extra se le aplica el metodo set_volume(0) para que no tenga volumen al momento de aparecer
            self.extra_spawn_time += 0 #al atributo extra_spawn_time se le reasigna su mismo valor mas 0 para que no vuelva a reaparecer

            for laser in self.human_lasers: #ciclo para iterar dentro del grupo human_lasers
                pygame.sprite.Sprite.kill(laser) #se ejecuta el metodo kill(laser) para eliminar cada laser dentro del grupo human_lasers

            self.superate_high_score() #se llama a ejecutar el metodo para mostrar cada vez que se supere el puntaje mas alto

            keys = pygame.key.get_pressed() #variable que obtiene una lista de las teclas que se pueden presionar, dicho metodo pertenece al modulo keys y a su vez dicho modulo pertenece al modulo pygame
            if keys[pygame.K_RETURN]: #condicional para validar si la tecla presioanda es RETURN/ENTER
                self.over = False #el valor del atributo cambia a False para NO mostrar la ventana de fin del juego
                self.startGame = False #el valor del atributo cambia a False para NO mostrar la ventana del juego
                self.mainScreen = False #el valor del atributo cambia a False para NO mostrar la ventana del menu principal
                self.scores = True #el valor del atributo cambia a True para mostrar la ventana de los puntakes
                self.obtain_score() #se ejecuta el metodo para guardar el puntaje en el archivo score.txt una sola vez solo cuando se presione el boton
                self.extract_high_score() #se llama a ejecutar el metodo para obtener el puntaje mas alto
                self.high_score_list() #se llama a ejecutar el metodo obtener la lista ordenada de los puntajes
                self.show_high_scores() #se ejecuta el metodo para mostrar todos los puntajes


    def game_over(self): #metodo para mostar un mensaje de fin de juego
        self.startGame = False #el valor del atributo se reasigna a False para que se oculte el juego al al momento de perder todas las vidas
        SCREEN.fill(BLACK) #se pintade negro todala superficice/screen/ventana
        defeat_surface = self.font_title.render(f"GAME OVER", False, 'white') #variable que sera la superficie/imagen la cual sera un renderizado de un texto el cual es "GAME OVER", se coloca Fasle para el antialiasing asi se las letras se mostraran mas pixeladas y se le coloca el color blanco
        defear_rect = defeat_surface.get_rect(center = (SCREEN_WIDTH / 2, (SCREEN_HEIGTH / 2) - 50)) #variable donde se obtiene un rectangulo a base de la superficie obtenida de renderizar el texto como una imagen, dicho rectangulo con el texto se mostrara en el centro de la ventana, para ello se obtienen los valores del ancho y el alto de dicha ventana y esos valores de dividen entre dos para que asi dicho recangulo se coloque en el centro de la ventana
        SCREEN.blit(defeat_surface, defear_rect) #se dibuja/coloca sobre la ventana/screen mediante la funcion blit() la superifie con el texto de victoria y el rectangulo para posicionar dicho texto

        score_surface = self.font_game.render(f"YOU SCORE : " + f"{self.score}", False, 'white') #se crea una superficie/imagen la cual sera un texto renderizado a imagen, utilizando la fuente de letra, y se renderizara eltexto "YOU SCORE : ", concatenado con el valor renderizado a texto de "{self.score}", se coloca false para no colocar suavisado al texto y se coloca el color 'white'
        score_rect = score_surface.get_rect(center = ((SCREEN_WIDTH / 2), (SCREEN_HEIGTH / 2) + 50)) #se obtiene un rectangulo a base de la superficie obtenida de renderizar el texto como una imagen, dicho rectangulo con el texto se mostrara en el centro de la ventana con un desplazamiento hacia abajo, para ello se obtienen los valores del ancho y el alto de dicha ventana/SCREEN y esos valores de dividen entre dos para que asi dicho recangulo se coloque en el centro de la ventana, al valor del alto se le suma el desplazamiento
        SCREEN.blit(score_surface, score_rect) #se coloca/pinta sobre la superficie/screen la imagen y el recatgulo para el score/puntaje

        continue_surface = self.font_game.render(f"SCORES  -PRESS ENTER-", False, 'white') #variable que sera la superficie/imagen la cual sera un renderizado de un texto el cual es "SCORES -PRESS ENTER-", se coloca Fasle para el antialiasing asi se las letras se mostraran mas pixeladas y se le coloca el color blanco
        continue_rect = continue_surface.get_rect(center = (SCREEN_WIDTH / 2, (SCREEN_HEIGTH / 2) + 100)) #variable donde se obtiene un rectangulo a base de la superficie obtenida de renderizar el texto como una imagen, dicho rectangulo con el texto se mostrara en el centro de la ventana, para ello se obtienen los valores del ancho y el alto de dicha ventana y esos valores de dividen entre dos para que asi dicho recangulo se coloque en el centro de la ventana y se suma un valor para que se coloque por debajo del centro horizontalmente
        SCREEN.blit(continue_surface, continue_rect) #se dibuja/coloca sobre la ventana/screen mediante la funcion blit() la superifie con el texto y el rectangulo para posicionar dicho texto

        for player in self.player: #ciclo que itera cada elemento/sprite player dentro del grupo unico player
            player.speed = 0 #al atributo speed del sprite player se le reasigna el valo de 0 para evitar el movimiento
            player.ready = False #al atributo ready se le reasigna el valor de False para evitar que dispare
        for human in self.humans: #ciclo que itera cada elemento/sprite human dentro del grupo humans
            self.human_direction = 0 #al atributo human_direction de cada sprite human dentro del grupo, se le reasigna el valor de 0 para evitar el movimiento
        for extra in self.extra: #ciclo que itera cada elemento/sprite extra dentro del grupo unico extra
            pygame.sprite.Sprite.kill(extra) #se utiliza la funcion reomve(extra) de la clase Sprite del modulo sprite de la libreria pygame, el eobjeto/sprite a eliminar es el extra dentro del grupo unico extra
            extra.speed = 0 #al atributo speed del sprite extra se le reasigna el valo de 0 para evitar el movimiento
            
        self.extra_sound.set_volume(0) #al atributo extra_sound del sprite extra se le aplica el metodo set_volume(0) para que no tenga volumen al momento de aparecer
        self.extra_spawn_time += 0 #al atributo extra_spawn_time se le reasigna su mismo valor mas 0 para que no vuelva a reaparecer
        pygame.time.set_timer(TIMER_ALIENLASER, -1) #al temporizador con el evento creado TIMER_ALIENLASER tiene el valor de -1 para evitar que disparen
        pygame.time.set_timer(TIMER_ALIENLASER_ALONE, -1)#al temporizador con el evento creado TIMER_ALIENLASER tiene el valor de -1 para evitar que disparen

        self.superate_high_score() #se llama a ejecutar el metodo para mostrar cada vez que se supere el puntaje mas alto

        keys = pygame.key.get_pressed() #variable que obtiene una lista de las teclas que se pueden presionar, dicho metodo pertenece al modulo keys y a su vez dicho modulo pertenece al modulo pygame
        if keys[pygame.K_RETURN]: #condicional para validar si la tecla presioanda es RETURN/ENTER
            self.over = False #el valor del atributo cambia a False para NO mostrar la ventana de fin del juego
            self.startGame = False #el valor del atributo cambia a False para NO mostrar la ventana del juego
            self.mainScreen = False #el valor del atributo cambia a False para NO mostrar la ventana del menu principal
            self.scores = True #el valor del atributo cambia a True para mostrar la ventana de los puntajes
            self.extract_high_score() #se llama a ejecutar el metodo para obtener el puntaje mas alto
            self.high_score_list() #se llama a ejecutar el metodo para obtener la lista ordenada de los puntajes
            self.show_high_scores() #se ejecuta el metodo para mostrar todos los puntajes

    def obtain_score(self): #metodo para obtener el score del jugador y escribirlo en el archivo correspondiente(score.txt)
         with open(SCORE_PATH, 'a') as file: #se utiliza el contexto 'with' para crear la variable 'file' la cual tiene el valor asignado de abrir el documeto desde su ruta y con el tipo de gestion archivos de escritura el final al final del archivo para escribir cada nuevo puntaje dentro del archivo correspondiete(score.txt)
            file.write("\n" + str(self.score)) #a la variable que es el archivo abierto, se le aplica el metodo write("" + ) para escribir sobre el archivo, un salto de linea concatenado con el valor del atributo score convertido a string


    def high_score_list(self): #metodo para obtener la lista ordenada de los puntajes
        self.score_order.sort(reverse=True) #al los valores dentro de la lista se le aplica el metodo sort() para ordenar dichos valores ya siendo numero enteros y en dicho metodo se le coloca el parametro reverse con el valor asignado de True para ordenarlo con el mayor valor en el primer indice
        self.score1 = self.score_order[0] #atributo que tiene asignado el valor del indice 0 de la lista score_order ya ordenada
        self.score2 = self.score_order[1] #atributo que tiene asignado el valor del indice 1 de la lista score_order ya ordenada
        self.score3 = self.score_order[2] #atributo que tiene asignado el valor del indice 2 de la lista score_order ya ordenada
        self.score4 = self.score_order[3] #atributo que tiene asignado el valor del indice 3 de la lista score_order ya ordenada
        self.score5 = self.score_order[4] #atributo que tiene asignado el valor del indice 4 de la lista score_order ya ordenada


    def show_high_scores(self): #metodo para mostrar los 5 puntajes mas altos
        SCREEN.fill(BLACK) #se coloca/dibuja sobre la ventana/superficie mediante blit(), la imagen del fondo desde las posiciones (0, 0) en los ejes 'x' y 'y'
        high_title_surface = self.font_title.render(f"- HIGH SCORES -", False, 'white') #se crea una superficie para colocar el titulo de la seccion para mostrar los puntajes, el cual es un renderizado de texto con la fuente de letra, sin suavisado y de color blanco
        high_title_rect = high_title_surface.get_rect(center = (SCREEN_WIDTH / 2, (SCREEN_HEIGTH / 2) - 210)) #se onbtiene un rectangulo a base de la superficie del titulo, el cual se colocara en el centro superior de la ventana, para ello se obtien la mitad del valor delalto y del ancho de la ventana y al alto se le resta un valor para desplazarlo hacia arriba
        SCREEN.blit(high_title_surface, high_title_rect) #se pinta/coloca sobre la ventana la superificie y el rectangulo

        score1_surface = self.font_game.render(f"1. SCORE : " + f"{self.score1}", False, 'white') #variable que sera la superficie/imagen la cual sera un renderizado de un texto el cual es "1. SCORE : " concatenado con el score del inidce correspondiente, se coloca Fale para el antialiasing asi se las letras se mostraran mas pixeladas y se le coloca el color blanco
        scores1_rect = score1_surface.get_rect(center = (SCREEN_WIDTH / 2, (SCREEN_HEIGTH / 2) - 60)) #variable donde se obtiene un rectangulo a base de la superficie obtenida de renderizar el texto como una imagen, dicho rectangulo con el texto se mostrara en el centro de la ventana, para ello se obtienen los valores del ancho y el alto de dicha ventana y esos valores de dividen entre dos para que asi dicho recangulo se coloque en el centro de la ventana
        SCREEN.blit(score1_surface, scores1_rect) #se pinta/coloca sobre la ventana/screen la superficie que muestra las puntuaciones y el rectangulo obtenido de dicha superficie

        score2_surface = self.font_game.render(f"2. SCORE : " + f"{self.score2}", False, 'white') #variable que sera la superficie/imagen la cual sera un renderizado de un texto el cual es "2. SCORE : " concatenado con el score del inidce correspondiente, se coloca Fasle para el antialiasing asi se las letras se mostraran mas pixeladas y se le coloca el color blanco
        scores2_rect = score2_surface.get_rect(center = (SCREEN_WIDTH / 2, (SCREEN_HEIGTH / 2) - 10)) #variable donde se obtiene un rectangulo a base de la superficie obtenida de renderizar el texto como una imagen, dicho rectangulo con el texto se mostrara en el centro de la ventana, para ello se obtienen los valores del ancho y el alto de dicha ventana y esos valores de dividen entre dos para que asi dicho recangulo se coloque en el centro de la ventana
        SCREEN.blit(score2_surface, scores2_rect) #se pinta/coloca sobre la ventana/screen la superficie que muestra las puntuaciones y el rectangulo obtenido de dicha superficie

        score3_surface = self.font_game.render(f"3. SCORE : " + f"{self.score3}", False, 'white') #variable que sera la superficie/imagen la cual sera un renderizado de un texto el cual es "1. SCORE : " concatenado con el score del inidce correspondiente, se coloca Fasle para el antialiasing asi se las letras se mostraran mas pixeladas y se le coloca el color blanco
        scores3_rect = score3_surface.get_rect(center = (SCREEN_WIDTH / 2, (SCREEN_HEIGTH / 2) + 40)) #variable donde se obtiene un rectangulo a base de la superficie obtenida de renderizar el texto como una imagen, dicho rectangulo con el texto se mostrara en el centro de la ventana, para ello se obtienen los valores del ancho y el alto de dicha ventana y esos valores de dividen entre dos para que asi dicho recangulo se coloque en el centro de la ventana
        SCREEN.blit(score3_surface, scores3_rect) #se pinta/coloca sobre la ventana/screen la superficie que muestra las puntuaciones y el rectangulo obtenido de dicha superficie

        score4_surface = self.font_game.render(f"4. SCORE : " + f"{self.score4}", False, 'white') #variable que sera la superficie/imagen la cual sera un renderizado de un texto el cual es "1. SCORE : " concatenado con el score del inidce correspondiente, se coloca Fasle para el antialiasing asi se las letras se mostraran mas pixeladas y se le coloca el color blanco
        scores4_rect = score4_surface.get_rect(center = (SCREEN_WIDTH / 2, (SCREEN_HEIGTH / 2) + 90)) #variable donde se obtiene un rectangulo a base de la superficie obtenida de renderizar el texto como una imagen, dicho rectangulo con el texto se mostrara en el centro de la ventana, para ello se obtienen los valores del ancho y el alto de dicha ventana y esos valores de dividen entre dos para que asi dicho recangulo se coloque en el centro de la ventana
        SCREEN.blit(score4_surface, scores4_rect) #se pinta/coloca sobre la ventana/screen la superficie que muestra las puntuaciones y el rectangulo obtenido de dicha superficie

        score5_surface = self.font_game.render(f"5. SCORE : " + f"{self.score5}", False, 'white') #variable que sera la superficie/imagen la cual sera un renderizado de un texto el cual es "1. SCORE : " concatenado con el score del inidce correspondiente, se coloca Fasle para el antialiasing asi se las letras se mostraran mas pixeladas y se le coloca el color blanco
        scores5_rect = score5_surface.get_rect(center = (SCREEN_WIDTH / 2, (SCREEN_HEIGTH / 2) + 140)) #variable donde se obtiene un rectangulo a base de la superficie obtenida de renderizar el texto como una imagen, dicho rectangulo con el texto se mostrara en el centro de la ventana, para ello se obtienen los valores del ancho y el alto de dicha ventana y esos valores de dividen entre dos para que asi dicho recangulo se coloque en el centro de la ventana
        SCREEN.blit(score5_surface, scores5_rect) #se pinta/coloca sobre la ventana/screen la superficie que muestra las puntuaciones y el rectangulo obtenido de dicha superficie


    def run(self): #metodo para ejecutar el juego
        self.mainScreen = False #el valor del atributo se reasigna a False para que se oculte el menu principal al momento de iniciar el juego
        image_background_path = CURRENT_PATH / 'images' / 'background.jpg'
        image_background = pygame.image.load(image_background_path) #variable que obtendra la imagen del fondo desde su ruta
        SCREEN.blit(image_background, (0,0)) #se coloca/dibuja sobre la ventana/superficie mediante blit(), la imagen del fondo desde las posiciones (0, 0) en los ejes 'x' y 'y'

        self.player.update() #al grupo Unico player que es el contenedor del objeto player_sprite se le aplica el metodo para actualizar la funcionalidad/movimiento del jugador
        self.human_lasers.update() #se llama a ejecuar el metodo update() de la clase LaserEnemy() para actualizar el funcionamiento/movimiento del laser  
        self.extra.update() #se llama a ejecutar el metodo update() de la clase Extra() para actualizar el funcionamiento/movimiento del enemigo extra

        self.humans.update(self.human_direction) #al grupo humans que es el contenedor de los objetos human_sprite se le aplica el metodo para actualizar la funcionalidad/movimiento del grupo de enemigos con el valor del atributo que sera la direccion de movimiento del grupo de enemigos
        self.human_position_limit() #se llama a ejecutar el metodo para limitar el movimiento del grupo de enemigos dentro de la ventana
        self.extra_human_timer() #se llama a ejecutar el metodo para que empieze el temporizador al iniciar el juego
        self.collision_checks() #se llama a ejecutar el metodo collision_checks() para validar las colisiones

        self.player.sprite.lasers.draw(SCREEN) #se hace uso del metodo draw(SCREEN) para dibujar sobre la superficie/ventana, el objeto creado por el metodo shoot_laser() que se encuentra dentro del grupo lasers el cual sera un sprite/interactua, el cual se encuentra detro del GroupSingle y es el objeto player_sprite instanciado de la clase Player. Es colocado aqui para que se dibuje despues de actualizar la funcionalidad del juagdor y antes de la imagen del jugador, quedando debajo del mismo
        self.player.draw(SCREEN) #se dibujará sobre la superfice/ventana el objeto player_sprite el cual ya esta detro del GroupSingle
        self.blocks.draw(SCREEN) #se dibujan sobre la venata/superficie el contenido del grupo blocks, los cuales son los obstaculos creados
        self.humans.draw(SCREEN) #se dibujan sobre la venata/superficie el contenido del grupo humans, los cuales son todos los enemigos creados
        self.human_lasers.draw(SCREEN) #se dibujan sobre la venata/superficie el contenido del grupo human_lasers, el cual es el sprite/objeto del laser del enemigo
        self.extra.draw(SCREEN)  #se dibujan sobre la venata/superficie el contenido del grupo extra, el cual es el sprite/objeto del enemigo extra
        self.display_lives() #se llama a ejecutar el metodo display_lives() para colocar la cantidad de imagenes de la vidas correspondientes
        self.display_score() #se llama a ejecutar el metodo display_score() para colocar el texto con el puntaje
        self.victory_message() #se llama a ejecutar el metodo victory_message() para colocar el texto de victoria cuando se cumpla la condicion necesaria

        self.laser_enemy.set_volume(0.2) #el volumen de laser del enemigo vuelve a ser 0.2

        if self.lives <= 0: #condcicional para validar si el valor del atributo lives que son las vidas del jugador, es menor o igual a 0
            self.startGame = False #el valor del atributo cambia a False para ocultar el juego
            self.over = True #el valor del atributo cambia a True para mostrar la ventana de fin del juego
            self.windows() #se llama a ejecutar el metodo windows() para colocar el texto de derrota cuando se cumpla la condicion necesaria dependiendo de los valores de los atributos
            self.obtain_score() #se ejecuta el metodo para guardar el puntaje en el archivo score.txt una sola vez al momento de que el jugador ya no tenga mas vidas


    def windows(self): #metodo para cambiar entre las diferentes visualizaciones de pantallas
        if self.startGame == False and self.mainScreen == True and game.over == False: #condicional para validar si el valor de las tres variable son las necesarias para ejecutar el menu principal
            self.main_menu() #se ejecuta el metodo para mostrar el menu principal
        elif self.startGame == True and self.mainScreen == False and game.over == False: #condicional para validar si el valor de las tres variable son las necesarias para ejecutar el juego
            self.run() #se ejecuta el metodo run() para iniciar el juego
        elif game.startGame == False and self.mainScreen == False and game.over == True: #condicional para validar si el valor de las tres variable son las necesarias para ejecutar la ventana de perdida
            self.game_over() #se ejecuta el metodo game_over() para mostrar la ventana de fin del juego al perder


if __name__ == '__main__': #condicional para validar que se ejecute el codigo solo si el nombre del archivo es main evitando que lo ejecute otro archivo
    pygame.init() #inicializar el modulo pygame con todo su contenido
    pygame.display.set_caption('Human-Invaders') #define el titulo de la ventana
    SCREEN = pygame.display.set_mode(SCREEN_SIZE) #constante con valor para crear la superficie/ventana con las dimensiones de SCREEN_SIZE
    window = True #valor True en la variable window para mantener activa/abirta la ventana mientras el valor siga siendo True
    clock = pygame.time.Clock() #se crear un reloj/contador
    game = Game() #objeto instanciado de la clase Game el cual podra hacer uso de todos los metodos y atributos de dicha clase

    TIMER_ALIENLASER = pygame.USEREVENT + 1 #se crea un nuevo evento de usuario para ser un temporizador del disparo del enemigo
    pygame.time.set_timer(TIMER_ALIENLASER, 500) #se crea el temporizador con el evento anterior el cual se ejecutara cada 550 milisegundos

    TIMER_ALIENLASER_ALONE = pygame.USEREVENT + 2 #se crea un nuevo evento de usuario para ser un temporizador del disparo del enemigo final
    pygame.time.set_timer(TIMER_ALIENLASER_ALONE, 150) #se crea el temporizador con el evento anterior el cual se ejecutara cada 150 milisegundos

    while window: #condicional para mantener activa la ventana/superficie mientras el valor de window sea True
        for event in pygame.event.get(): #ciclo for por cada evento en el modulo event de pygame se ejeucta la funcion get() para obetenr la lista de evetos de dicho modulo
            if event.type == pygame.QUIT: #condicional para cerrar la ventana si el tipo de evento por cada iteracion es igual al evento QUIT
                window = False #cambio de valor de window de True a False, terminando el ciclo While window/True cerrando la ventana
            if event.type == TIMER_ALIENLASER and len(game.humans) > 1: #condicional para ejecutar el metodo si el tipo de evento es igual a TIMER_ALIENLASER el cual es el nuevo evento que fue creado y si la longitud del grupo de sprites humans de la clase Game es mayor que 1
                game.human_shoot() #se ejecuta el metodo para que el enemigo dispare en un tiempo determinado
            if event.type == TIMER_ALIENLASER_ALONE and len(game.humans) == 1: #condicional para ejecutar el metodo si el tipo de evento es igual a TIMER_ALIENLASER_ALONE el cual es el nuevo evento que fue creado y si la longitud del grupo de sprites humans de la clase Game es igual que 1
                game.human_shoot()

        game.windows() #se ejecuta el metodo windows() para validar que ventana mostrar dependiendo de los valores de las variables
        pygame.display.flip() #Actualizar la pantalla en todo momento
        clock.tick(60) #el tiempo del reloj es de 60 fotogramas por segundo
