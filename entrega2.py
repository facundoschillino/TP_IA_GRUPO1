from simpleai.search import (
    CspProblem,
    backtrack,
    MOST_CONSTRAINED_VARIABLE,
    )

from itertools import combinations

def generar_variables(n):  
    tupla_tuplas = ()
    for x in range(1, n + 1):
        for y in range(1, 5):
            tupla_tuplas += ((x, y),)
    return tupla_tuplas

def generar_restricciones(variables, cantidad_colores):
    restricciones = []

    #SOLO_4
    #Genero todas las combinaciones de 5 cuartos
    combinaciones_de_cuartos = combinations(variables, 5)
    for combinacion in combinaciones_de_cuartos:
        restricciones.append((combinacion, solo_4))

    #NO_RESUELTO
    #Agrupamos los cuartos por frasco
    frascos = [[] for _ in range(cantidad_colores)]
    for cuarto in variables:
        frasco = cuarto[0]
        frascos[frasco - 1].append(cuarto)

    for frasco in frascos:
        restricciones.append((frasco, no_resuelto))

    #TODOS_AL_FONDO
    #Obtengo las variables que representan los fondos de los frascos
    fondos = []
    for cuarto in variables:
        if cuarto[1] == 1:
            fondos.append(cuarto)
    restricciones.append((fondos, todos_al_fondo))

    #COMPARTIR_COLOR
    #QUE_NO_HAYA_6
    #Dividimos las variables en frascos puntuales, para que las restricciones no sean completamente globales
    for index, frasco in enumerate(frascos):
        #No tenemos en cuenta el ultimo frasco porque no tiene adyacente a la derecha
        if index < cantidad_colores - 1:
            cuartos_adyacentes = frasco.copy()
            cuartos_adyacentes.extend(frascos[index + 1])
            cuartos_adyacentes = tuple(cuartos_adyacentes)
            restricciones.append((cuartos_adyacentes, compartir_color))
            restricciones.append((cuartos_adyacentes, que_no_haya_6))

    #TODOS_DIFERENTES
    #Genero todas las combinaciones de frascos
    combinaciones_de_frascos = combinations(frascos, 2)
    for combinacion in combinaciones_de_frascos:
        cuartos_de_combinacion = ()
        for frasco in combinacion:
            for cuarto in frasco:
                cuartos_de_combinacion += ((cuarto),)
        restricciones.append((cuartos_de_combinacion, todos_diferentes))

    return restricciones

#------------------RESTRICCIONES------------------
#Que no haya mas de 4 cuartos de cada color
def solo_4(vars, vals):
    colores = []
    for color in vals:
        if color not in colores:
            colores.append(color)
    
    return len(colores) > 1

#Verifica que un frasco no este resuelto (tenga los 4 colores iguales)
def no_resuelto(vars, vals):
    colores = vals
    return len(set(colores)) != 1

#Verifica que un color no tenga todos sus cuartos en el fondo
def todos_al_fondo(vars, vals):    
    #Contamos las apariciones de colores en el fondo
    conteo = {}
    for color in vals:
        if color in conteo:
            conteo[color] += 1
        else:
            conteo[color] = 1

    #Encuentro si hay algun color que aparezca 4 veces
    for cantidad_apariciones in conteo.values():
        if cantidad_apariciones == 4:
            return False
    return True

#Verifica que un frasco y su adyacente tengan al menos un color en comun
def compartir_color(vars, vals):
    # Dividir la lista en dos partes
    MITAD = 4
    colores_frasco_derecha = vals[:MITAD]
    colores_frasco_izquierda = vals[MITAD:]

    colores_frasco_derecha = set(colores_frasco_derecha)
    colores_frasco_izquierda= set(colores_frasco_izquierda)

    interseccion = colores_frasco_izquierda.intersection(colores_frasco_derecha)

    return len(interseccion) > 0

#Verifica que dos frascos adyacentes no sumen mas de 6 colores unicos
def que_no_haya_6(vars, vals): 
    colores_unicos = set(vals)
    return len(colores_unicos) <= 6

#Verifica que no haya dos frascos iguales
def todos_diferentes(vars, vals):
    # Obtenemos los colores de los dos frascos
    MITAD = 4
    colores_frasco_A = vals[:MITAD]
    colores_frasco_B = vals[MITAD:]

    return colores_frasco_A != colores_frasco_B

#-------------------------------------------------

def armar_nivel(colores, contenidos_parciales):
    #Actualizo la variable global CANTIDAD_COLORES
    cantidad_colores = len(colores)

    variables = generar_variables(cantidad_colores)

    #Obtengo el dominio de las variables
    dominio = {var: list(colores) for var in variables}
    
    for indice_frasco, frasco in enumerate(contenidos_parciales):
        for indice, color in enumerate(frasco):
            dominio[(indice_frasco + 1, indice + 1)] = [color]

    restricciones = generar_restricciones(variables, cantidad_colores)
    
    problema = CspProblem(variables, dominio, restricciones)
    
    solucion = backtrack(problema, variable_heuristic=MOST_CONSTRAINED_VARIABLE)

    frascos_armados = []
    
    for frasco in range(cantidad_colores):
        frasco_values = [solucion[(frasco + 1, pos)] for pos in range(1, 5)]
        frascos_armados.append(tuple(frasco_values))
    return frascos_armados
