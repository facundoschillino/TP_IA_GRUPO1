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
        (), )


def cerrado (jarro): #Funcion para verificar que un jarro no este cerrado
    un_color = set(jarro)
    if (len(jarro) == 4 and len(un_color)==1):
        return True
    return False

class SortEmAll(SearchProblem):

    def actions(self, state): #Vamos a tener que ver el color del ultimo item y determinar a que frasco lo vamos a trasvasar
        actions = []
        for origen,jarro_origen in enumerate(state): #recorro la lista de jarros
            ultimo_color_origen = jarro_origen[len(jarro_origen)-1] #Guardo el ulitmo color para ver a cual puedo trasvasar
            for destino,jarro_destino in enumerate(state):
                ultimo_color_destino = jarro_destino[len(jarro_destino)-1]
                if (jarro_origen != jarro_destino and ultimo_color_destino == ultimo_color_origen and len(jarro_destino < 4)):
                    actions.append(origen, destino)
        return actions





    


