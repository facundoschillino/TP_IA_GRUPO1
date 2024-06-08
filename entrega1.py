from simpleai.search import (
    SearchProblem,
    greedy, astar,
    )

from simpleai.search.viewers import (WebViewer)

def jugar(frascos, dificil):
    problem = SortEmAll(frascos)
    if dificil == True:
        #Utilizo busqueda avara
        result = greedy(problem, graph_search=True)
    else:
        #Utilizo a estrella
        result = astar(problem, graph_search=True)
    pasos = []
    for paso, _ in result.path():
        if paso:
            pasos.append(paso)
    return pasos

def esta_cerrado (frasco):
    un_color = set(frasco)
    return esta_lleno(frasco) and len(un_color) == 1

def esta_vacio (frasco):
    return len(frasco) == 0

def esta_lleno (frasco):
    return len(frasco) == 4

def color_superior(frasco):
    indice_color_superior = len(frasco) - 1
    color_superior = frasco[indice_color_superior]
    return color_superior

class SortEmAll(SearchProblem):
    def actions(self, state):
        frascos = state
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
                                actions.append((indice_origen + 1, indice_destino + 1))
                            # Agrego los frascos que tienen el mismo color superior
                            elif color_superior(frasco_origen) == color_superior(frasco_destino): 
                                actions.append((indice_origen + 1, indice_destino + 1))

        return actions
    
    def result(self, state, action):
        origen, destino = action
        origen -= 1
        destino -= 1

        frascos = [list(frasco) for frasco in state]

        frasco_origen = frascos[origen]
        frasco_destino = frascos[destino]

        color_a_trasvasar = color_superior(frasco_origen)

        # Obtengo los cuartos en origen que puedo trasvasar
        cuartos_en_origen = 0
        for color in frasco_origen:
            if color == color_a_trasvasar:
                cuartos_en_origen += 1
            else:
                cuartos_en_origen = 0
        
        # Trasvaso hasta agotar los cuartos o llenar el destino
        for _ in range(cuartos_en_origen):
            color_sustraido = frasco_origen.pop()
            frasco_destino.append(color_sustraido)
            if esta_lleno(frasco_destino):
                break

        frascos = tuple(tuple(frasco) for frasco in frascos)
        return frascos
    
    #Por lo que entiendo, lo que hay que minimizar son los movimientos, asi que cada accion vale 1
    def cost(self, state, action, state2):
        return 1  
    
    def is_goal(self, state):
        frascos = state
        for frasco in frascos:
            if not esta_vacio(frasco) and not esta_cerrado(frasco):
                return False
        return True
    
    def heuristic(self, state):
        # Busca la cantidad de colores diferentes en los frascos no llenos ni vacios
        frascos = state
        costo_total = 0
        for frasco in frascos:
            if not esta_vacio(frasco) and not esta_cerrado(frasco):
                # Cuento la cantidad de colores distintos
                colores = []
                for color in frasco:
                    if color not in colores:
                        colores.append(color)
                # Resto uno para que no sobreestime
                cantidad_colores_distintos = len(colores) - 1
                costo_total += cantidad_colores_distintos
        return costo_total