from simpleai.search import (
    SearchProblem,
    greedy, astar,
    )

from simpleai.search.viewers import (BaseViewer, WebViewer)

import itertools

INITIAL_STATE = (
        ("verde", "azul", "rojo", "naranja"),     # frasco 1, notar el orden de los colores
        ("azul", "rosa", "naranja"),              # frasco 2, notar que es de largo 3, queda un espacio vacío
        ("rosa", "celeste", "verde", "verde"),    # frasco 3, notar cómo "verde" se repite 2 veces por los 2 cuartos iguales
        ("rosa", "rojo", "celeste", "celeste"),   # frasco 4
        ("rojo", "azul", "lila"),                 # frasco 5
        ("verde", "naranja", "celeste", "rojo"),  # frasco 6
        ("azul", "naranja", "rosa"),              # frasco 7
        ("lila", "lila", "lila"),                 # frasco 8, notar la repetición de colores para cada cuarto
        ())

def esta_cerrado (frasco):
    un_color = set(frasco)
    return len(frasco) == 4 and len(un_color) == 1

def esta_vacio (frasco):
    return len(frasco) > 0

def color_superior(frasco):
    indice_color_superior = len(frasco) - 1
    color_superior = frasco[indice_color_superior]
    return color_superior

class SortEmAll(SearchProblem):

    def actions(self, state):
        frascos = state
        # Vamos a tener que ver el color del ultimo item y determinar a que frasco lo podemos a trasvasar
        actions = []
        # Recorro la lista de frascos, para ver desde que frasco puedo trasvasar
        for indice_origen, frasco_origen in enumerate(frascos):
            if not esta_vacio(frasco_origen) and not esta_cerrado(frasco_origen):
                # Recorro la lista de frascos para encontrar el destino
                for indice_destino, frasco_destino in enumerate(frascos):
                    # Ignoro el mismo frasco origen
                    if indice_destino != indice_origen:
                        # Ignoro los frascos llenos
                        if len(frasco_destino) < 4:
                            # Agrego los frascos vacios
                            if len(frasco_destino) == 0:
                                actions.append((indice_origen, indice_destino))
                            # Agrego los frascos que tienen el mismo color superior
                            elif color_superior(frasco_origen) == color_superior(frasco_destino): 
                                actions.append((indice_origen, indice_destino))

        return actions
    
    def result(self, state, action):
        origen,destino = action
        state = list(state)
        frasco_origen = list(state[origen])
        frasco_destino = list(state[destino])
        color_a_trasvasar = frasco_origen[len(frasco_origen)-1]
        cantidad_al_final = 0
        for color in frasco_origen:
            if color == color_a_trasvasar:
                cantidad_al_final += 1
            else:
                cantidad_al_final = 0
        #Hasta acá lo que hice fue ver cuantas unidades de ese color tengo al final, osea, cuantas puedo trasvasar.
        if (len(frasco_destino) == 0): ##Este es para trasvasar a uno vacio
             for _ in range(cantidad_al_final):
                color_sustraido = frasco_origen.pop()
                frasco_destino.append(color_sustraido)
        else: #Este es para cuando destino no esta vacio y tengo que contar cuantos puedo trasvasar
             faltante_destino = 4 - len(frasco_destino)
             if (faltante_destino >= cantidad_al_final):
                for _ in range(cantidad_al_final):
                    color_sustraido = frasco_origen.pop()
                    frasco_destino.append(color_sustraido)
             else:
                  while (len(frasco_destino) < 4):
                    color_sustraido = frasco_origen.pop()
                    frasco_destino.append(color_sustraido)                 
        frasco_origen = tuple(frasco_origen)
        frasco_destino = tuple(frasco_destino)
        state[origen] = frasco_origen
        state[destino] = frasco_destino
        return tuple(state)
    
    def cost(self, state, actions, state1): #Por lo que entiendo, lo que hay que minimizar son los movimientos, asi que cada accion vale 1
        return 1  
    
    def is_goal(self, state): # Esto no se si esta bien, es una idea
        for frasco in state:
            if len(frasco) > 0 and not esta_cerrado(frasco):
                return False
        return True
    
    def heuristic(self,state): #Solo voy a contar los frascos que no estan cerrados
        no_cerrados = 0
        for frasco in state:
            if len(frasco) >0 and not esta_cerrado(frasco):
                no_cerrados +=1
        return no_cerrados

my_problem = SortEmAll(INITIAL_STATE)

#v = BaseViewer()

v = WebViewer()

result = astar(my_problem, viewer=v)

if result is None:
    print("No solution")
else:
    for action, state in result.path():
        print("A:", action)
        print("S:")
        print(*state, sep="\n")
    print("Final cost:", result.cost)           







    


