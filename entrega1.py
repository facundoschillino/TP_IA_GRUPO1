from simpleai.search import (
    SearchProblem,
    greedy,
    astar,)
from simpleai.search.viewers import (BaseViewer, WebViewer)
import itertools

inicial_ejemplo = (
        ("verde", "azul", "rojo", "naranja"),     # frasco 1, notar el orden de los colores
        ("azul", "rosa", "naranja"),              # frasco 2, notar que es de largo 3, queda un espacio vacío
        ("rosa", "celeste", "verde", "verde"),    # frasco 3, notar cómo "verde" se repite 2 veces por los 2 cuartos iguales
        ("rosa", "rojo", "celeste", "celeste"),   # frasco 4
        ("rojo", "azul", "lila"),                 # frasco 5
        ("verde", "naranja", "celeste", "rojo"),  # frasco 6
        ("azul", "naranja", "rosa"),              # frasco 7
        ("lila", "lila", "lila"),                 # frasco 8, notar la repetición de colores para cada cuarto
        ())


def cerrado (jarro): #Funcion para verificar que un jarro no este cerrado
    un_color = set(jarro)
    if (len(jarro) == 4 and len(un_color)==1):
        return True
    return False
class SortEmAll(SearchProblem):
    def actions(self,state): #Vamos a tener que ver el color del ultimo item y determinar a que frasco lo vamos a trasvasar
        actions = []
        for origen,jarro_origen in enumerate(state):#recorro la lista de jarros, para ver desde que jarro voy a trasvasar
            if len(jarro_origen) > 0 and not cerrado(jarro_origen): # verifico que no este vacío o cerrado
                indice_ultimo_color_origen = len(jarro_origen)-1
                ultimo_color_origen = jarro_origen[indice_ultimo_color_origen] #Guardo el ulitmo color para ver a cual puedo trasvasar
                for destino,jarro_destino in enumerate(state): # #recorro la lista de jarros, para ver hacia que jarro voy a trasvasar
                    if jarro_origen != jarro_destino and len(jarro_destino) > 0: #Primero, voy a probar con los frascos que tienen el mismo color encima, descartando los frascos vacíos, ya que a esos siempre puedo trasvasar
                        indice_ultimo_color_destino = len(jarro_destino)-1
                        ultimo_color_destino = jarro_destino[indice_ultimo_color_destino]
                        if (ultimo_color_destino == ultimo_color_origen and len(jarro_destino)<4):
                            actions.append((origen, destino))
                    if len(jarro_destino) == 0:
                         actions.append((origen, destino))
        return actions
    def result(self, state,action):
        origen,destino = action
        state = list(state)
        jarro_origen = list(state[origen])
        jarro_destino = list(state[destino])
        color_a_trasvasar = jarro_origen[len(jarro_origen)-1]
        cantidad_al_final = 0
        for color in jarro_origen:
            if color == color_a_trasvasar:
                cantidad_al_final += 1
            else:
                cantidad_al_final = 0
        #Hasta acá lo que hice fue ver cuantas unidades de ese color tengo al final, osea, cuantas puedo trasvasar.
        if (len(jarro_destino) == 0): ##Este es para trasvasar a uno vacio
             for _ in range(cantidad_al_final):
                color_sustraido = jarro_origen.pop()
                jarro_destino.append(color_sustraido)
        else: #Este es para cuando destino no esta vacio y tengo que contar cuantos puedo trasvasar
             faltante_destino = 4 - len(jarro_destino)
             if (faltante_destino >= cantidad_al_final):
                for _ in range(cantidad_al_final):
                    color_sustraido = jarro_origen.pop()
                    jarro_destino.append(color_sustraido)
             else:
                  while (len(jarro_destino) < 4):
                    color_sustraido = jarro_origen.pop()
                    jarro_destino.append(color_sustraido)                 
        jarro_origen = tuple(jarro_origen)
        jarro_destino = tuple(jarro_destino)
        state[origen] = jarro_origen
        state[destino] = jarro_destino
        return tuple(state)
    def cost(self, state, actions, state1): #Por lo que entiendo, lo que hay que minimizar son los movimientos, asi que cada accion vale 1
        return 1  
    def is_goal(self, state): # Esto no se si esta bien, es una idea
        for jarro in state:
            if len(jarro) > 0 and not cerrado(jarro):
                return False
        return True
    def heuristic(self,state): #Solo voy a contar los jarros que no estan cerrados
        no_cerrados = 0
        for jarro in state:
            if len(jarro) >0 and not cerrado(jarro):
                no_cerrados +=1
        return no_cerrados

my_problem = SortEmAll(inicial_ejemplo)
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







    


