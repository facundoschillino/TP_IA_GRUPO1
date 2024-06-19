from simpleai.search import (
    CspProblem,
    csp, 
    SearchProblem, 
    backtrack, 
    min_conflicts
)
#Todos los frascos tienen capacidad de 4 segmentos. Esto lo satisfacemos definiendo las variables
#Todos los frascos deben llenarse hasta el tope. El problema tiene que ser completo, asi que esto se satisface en la definición
variables = {}  
dominio= ["Celeste", "Blanco", "Rojo", "Verde"] 
restricciones = []
#Fede: esta variable la recibe de la funcion armar_nivel (una vez que ya este implementado el CSP y ande)
CANTIDAD_COLORES = 4
#Fede: Hay que generar los cuartos, no los frascos
#Fede: Podria armarse una tupla con 1A, 1B, 1C, y asi
def generar_variables(n): #Aca simplemente generamos la cantidad de frascos que necesitamos
    lista_tuplas = []
    for x in range(1, n+1):
        for y in range(1, 5):
            lista_tuplas.append((x, y))
    return lista_tuplas
variables = generar_variables(CANTIDAD_COLORES)
#Una vez que este generado el csp, hacemos una funcion que nos retorne los frascos armados
#Restriccion que verifica que cada color solo aparezca 4 veces:
def solo_4(vars, vals):
    colores = {}
    for valor in vals:
        if valor in colores:
            colores[valor] += 1
        else:
            colores[valor] = 1
    for conteo in colores.values():
        if conteo > 4:
            return False
    return True
restricciones.append((variables, solo_4))
#Ningún frasco debe comenzar resuelto. Es decir, ningún frasco debe tener 4 segmentos del mismo color. Resuelto
def no_resuelto(vars, vals):
    for frasco in range(1, CANTIDAD_COLORES + 1):
        colores_frasco = []
        for posicion_frasco in range(1, 5):
            try:
                index = vars.index((frasco, posicion_frasco))
                colores_frasco.append(vals[index])
            except ValueError:
                continue
        if len(set(colores_frasco)) == 1:
            return False
    return True
restricciones.append((variables, no_resuelto))
#Ningún color puede comenzar con todos sus segmentos en el fondo de frascos, porque se trataría de una situación excesivamente difícil de resolver. Restriccion
def todos_al_fondo(vars,vals): 
    colores_Fondo = []
    for var, val in zip(vars, vals):
        frasco, cuarto = var
        if cuarto == 1: #Si es el primer cuarto del frasco (Osea digamos el que esta al fondo) lo agrego a la lista
            color_del_fondo = val #Me guardo el color del fondo
            colores_Fondo.append(val) # Lo aniado a la lista
    conteo = {} #Diccionario que voy a usar para llevar la cantidad de apariciones
    for color in colores_Fondo:
        if color in conteo:
            conteo[color] += 1
        else:
            conteo[color] = 1
    for color in conteo:
        if conteo[color] >= 4:
            return False
    return True
restricciones.append((variables, todos_al_fondo))
#Si dos frascos son adyacentes, deben compartir al menos un color. #Restriccion
def compartir_color(vars, vals):
    frascos = [[] for _ in range(CANTIDAD_COLORES)]  # Inicializa la lista de frascos
    # Llena los frascos con sus valores correspondientes
    for var, val in zip(vars, vals):
        frasco, cuarto = var
        frascos[frasco - 1].append(val)
    # Verifica que frascos adyacentes compartan al menos un color
    for indice, frasco in enumerate(frascos):
        interseccion1 = set()
        interseccion2 = set()
        frasco_anterior = []
        frasco_posterior = []
        if indice > 0:
            frasco_anterior = set(frascos[indice - 1])
            interseccion1 = set(frasco).intersection(frasco_anterior)
        if indice < CANTIDAD_COLORES - 1:
            frasco_posterior = set(frascos[indice + 1])
            interseccion2 = set(frasco).intersection(frasco_posterior)
        if not interseccion1 and not interseccion2:
            return False
    return True 
restricciones.append((variables, compartir_color))
#Si dos frascos son adyacentes, no pueden tener más de 6 colores diferentes entre ambos, para evitar situaciones demasiado complejas. #Restriccion

def que_no_haya_6(vars, vals): 
    frascos = [[] for _ in range(CANTIDAD_COLORES)]  # Inicializo la lista de frascos
    #Genero los frascos con sus colores
    for var, val in zip(vars, vals):
        frasco, cuarto = var
        frascos[frasco - 1].append(val)
    for indice, frasco in enumerate(frascos):
        frasco_anterior = []
        frasco_posterior = []
        if indice > 0:
            frasco_anterior = frascos[indice - 1]  
            frasco_anterior.extend(frasco)
        if indice < CANTIDAD_COLORES -1:
            frasco_posterior = frascos[indice + 1]       
            frasco_posterior.extend(frasco)
        if len(set(frasco_anterior)) > 6 or len(set(frasco_posterior)) > 6:
            return False
    return True
restricciones.append((variables, que_no_haya_6))

#No puede haber dos frascos exáctamente iguales. Restriccion.
def todos_distintos(vars, vals):
    frascos = [[] for _ in range(CANTIDAD_COLORES)]  # Inicializo la lista de frascos
    #Genero los frascos con sus colores
    for var, val in zip(vars, vals):
        frasco, cuarto = var
        frascos[frasco - 1].append(val)
restricciones.append((variables, todos_distintos))        

problema = CspProblem(variables, {var: dominio for var in variables}, restricciones)
solucion = min_conflicts(problema)
print (solucion)
    
    
    
    
    
    
    #Lo que se me ocurre es agregar colores que estan en el fondo del frasco
    #Fede: es buena esa. Podes contar la cantidad de apariciones de cada color en el fondo. Si alguno tiene 4 apariciones, no se cumple la restriccion

#Comienzo a agregar las restricciones
#Para la restriccion no_resuelto tienen que agruparse las variables de un mismo frasco    