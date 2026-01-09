from constants import PLAYER_COLOR, BSIZ, NO_PLAYER, ST_PLAYER

from collections import namedtuple

# Representación de las piedras en el tablero.
# Utilizamos de coordenadas x, y (fila y columna)
# Utilizamos el índice del jugador (0/1), que se usa con PLAYER_COLOR['color']

Stone = namedtuple('Stone', ('x', 'y', 'color'))


def set_board_up(stones_per_player = ST_PLAYER): 

    #Inicialización del tablero
    #Vamos a hacer una matriz donde NO_PLAYER = -1 significa casilla no jugada, 0 es cassilla
    #del jugador 0 y 1 es casilla del jugador 1

    i, j = 0,0                                       #contador filas y columnas
    board = []                                     #esto será la matriz

    while i < BSIZ:
        fila = []
        while j < BSIZ:
            fila.append(NO_PLAYER)                 #Añadimos NO_PLAYER en fila BSIZ veces
            j += 1

        board.append(fila)                         #Ponemos la fila de NO_PLAYER [-1, -1, -1] en el tablero, BSIZ veces
        i += 1
        j = 0                                      #reiniciamos el contador de columnas a cero



    # Ahora toca definir las distintas variables involucradas en el tablero

    # 1. Lista de piedras: cada elemento será Stone(x, y, color)
    stones_list = []

    # 2. Jugador actual: 0 o 1
    current_player = 0

    # 3. Fase del juego: Placing (se colocan las piedras) o Moving (todas colocadas, ahora se mueven)
    phase = 'placing'

    # 4. Número de piedras colocadas por cada jugador. El primer valor corresponde al jugador 0 y el segundo al 1
    stones_placed = [0,0]

    # 5. Índice de piedra seleccionado en la fase moving. Se refiere al índice de stones_list
    selected_index = None

    # 6. Orden de colocación por jugador (guardamos índices de stones_list)                                                     #modificación
    order = [[], []]




    #---------------------------------#
    #            FUNCIONES            #
    #---------------------------------#

    # Solo  nos dice que devuelve las piedras que hay
    def stones():
        return stones_list


    # Dibujar el tablero. Se puede hacer con dos while, yendo valor por valor comprobando si es igual a
    # -1, 0 o 1, y en función a eso imprimir ".". "X" o "O"
    def draw_txt(end = False):

        fila, col = 0, 0

        while fila < BSIZ:
            linea = ""                             # Se imprimirá más tarde. Se inicializa ahora porque se le añadirán cosas

            while col < BSIZ:
                posicion = board[fila][col]        #Recorremos toda la matriz
                
                if posicion == NO_PLAYER:          #Dependiendo del valor que hay en cada posición, ponemos X, O, ".
                    caracter = "."
                elif posicion == 0:
                    caracter = 'O'
                else:
                    caracter = 'X'

                linea = linea + caracter + ' '     # Linea pasa a ser cada caracter de la fila, con espacios ' ' para que se vea mejor
                col += 1
            
            print(linea)                           # Se imprime una fila y se pasa a la siguiente
            fila += 1
            col = 0

        if not end:                                                  # Si end es False, la partida continúa (y mostramos a quién le toca). Si es True se acaba.
            print("Turno del jugador:", current_player)              # El valor de end es recibido desde la función move_st(), del fichero main_txt.py
        else:
            print("Fin de la partida")


    # Devuelve True si el jugador 'player' ha hecho 3 en ralla. Le pasamos 'player' desde move_st
    def end(player):

        # Comprobar horizontal

        fila = 0
        while fila < BSIZ:
            if board[fila][0] == player and board [fila][1] == player and board[fila][2] == player:
                return True
            fila += 1
        
        # Comprobar vertical

        col = 0
        while col < BSIZ:
            if board[0][col] == player and board[1][col] == player and board[2][col] == player:
                return True
            col += 1

        # Comprobar las dos diagonales

        if board[0][0] == player and board[1][1] == player and board[2][2] == player:
            return True
        
        if board[0][2] == player and board[1][1] == player and board[2][0] == player:
            return True
        
        # Si no se cumplió nada de lo de arriba, devolvemos False
        return False
    


    def must_move():                    #modificación
    # Devuelve (x, y) de la piedra que DEBE moverse ahora, o None si no aplica
        if phase != 'moving':
            return None
        
        if selected_index is not None:
            return None
        
        if not order[current_player]:
            return None
        
        idx = order[current_player][0]
        s = stones_list[idx]
        return (s.x, s.y)


    # Selecciona la piedra en (i,j) si pertenece al jugador actual. Si la selección es válida devuelve True, sino False
    # Esta función se utiliza en move_st para que la funcion sepa qué piedra exacta modificar

    def select_st(i,j):
        
        nonlocal selected_index             # La variable se debe actualizar para todas las funciones internas

        if phase == 'placing':
            return True                  # Si estamos en fase de placing devolveremos True directamente ya que no tenemos que seleccionar piedras

        # Miramos si las coordenadas que ha puesto están dentro del tablero

        if i < 0 or i >= BSIZ or j < 0 or j >= BSIZ:
            return False
        
        # Asignamos a valor lo que hay en la posición del tablero para hacer las comparaciones
        valor = board[j][i]

        # Si no hay piedra
        if valor == NO_PLAYER:
            return False
        
        # Si hay piedra pero es del otro jugador
        if valor != current_player:
            return False
        

        k = 0                                           # Inicializamos el índice que recorre la lista de piedras
        encontrada = False
        dim = len(stones_list)

        while k < dim and encontrada == False:          # Mientras k sea menor a la dimensión de la lista y la piedra no se encuentre
            stone = stones_list[k]
            
            if stone.x == i and stone.y == j:           # Buscamos en qué índice de la lista está la piedra seleccionada
                encontrada = True
            else:
                k += 1

        if encontrada == False:
            return encontrada
        
        # Solo se puede mover la piedra más antigua del jugador actual                                                                        #modificación                                           
        if k != order[current_player][0]:
            return False

        selected_index = k
        return True
    
    
    def move_st(i,j):
        nonlocal current_player, phase, stones_placed, selected_index

        # Miramos si las coordenadas que ha puesto están dentro del tablero

        if i < 0 or i >= BSIZ or j < 0 or j >= BSIZ:
            return True, current_player, False

        # Fase de placing
        if phase == 'placing':

            # Si la casilla está ocupada, no se puede colocar la piedra
            if board[j][i] != NO_PLAYER:
                return True, current_player, False

            # Colocamos la piedra en el tablero
            board[j][i] = current_player

            # Añadimos la piedra a la lista de piedras
            owner = current_player
            nueva_piedra = Stone(i, j, PLAYER_COLOR[owner])
            stones_list.append(nueva_piedra)

            order[owner].append(len(stones_list) - 1)         # Guardamos el índice de la piedra recién añadida en el orden de colocación del jugador correspondiente    #modificación

            # Actualizamos el número de piedras colocadas por el jugador actual
            stones_placed[current_player] += 1

            # Comprobamos si se ha hecho 3 en raya
            if end(current_player):
                return False, current_player, True

            # Cambiamos de jugador
            current_player = 1 - current_player

            # Comprobamos si se ha terminado la fase de placing
            if stones_placed[0] == stones_per_player and stones_placed[1] == stones_per_player:
                phase = 'moving'
                return False, current_player, False
            if stones_placed[1] != stones_per_player:
                return True, current_player, False

        # Fase de moving
        else:

            # Si la casilla está ocupada, no se puede mover la piedra
            if board[j][i] != NO_PLAYER:
                return True, current_player, False

            # Movemos la piedra en el tablero
            piedra_seleccionada = stones_list[selected_index]
            board[piedra_seleccionada.y][piedra_seleccionada.x] = NO_PLAYER
            board[j][i] = current_player

            # Actualizamos la posición de la piedra en la lista de piedras
            stones_list[selected_index] = Stone(i, j, PLAYER_COLOR[current_player])
            # Rotamos el orden: la piedra movida pasa a ser la más nueva                                                        #modificación
            moved_idx = selected_index
            if order[current_player] and order[current_player][0] == moved_idx:
                order[current_player].pop(0)
                order[current_player].append(moved_idx)

            # Comprobamos si se ha hecho 3 en raya
            if end(current_player):
                return False, current_player, True

            # Cambiamos de jugador
            current_player = 1 - current_player

            # Desseleccionamos la piedra
            selected_index = None

            return False, current_player, False

    return stones, select_st, move_st, draw_txt,must_move