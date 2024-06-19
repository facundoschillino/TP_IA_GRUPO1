from simpleai.search import (
    csp, 
    SearchProblem, 
    backtrack, 
    min_conflicts
)

variables = {} #Podriamos manejar las variables como un conjunto de tuplas, donde el primer valor equivale al frasco
#Fede: Las variables tienen que ser los cuartos de cada frasco

dominio= [] #En el dom vamos a poner los colores!!!
#Fede: traete los colores que pase a la funcion armar_nivel (bueno, es bastante obvio)
#Para las variables que ya tienen valores hay que fijarles el dominio aca

#Fede: esta variable la recibe de la funcion armar_nivel (una vez que ya este implementado el CSP y ande)
CANTIDAD_COLORES = 3

#Fede: Hay que generar los cuartos, no los frascos
#Fede: Podria armarse una tupla con 1A, 1B, 1C, y asi
def generar_variables(n): #Aca simplemente generamos la cantidad de frascos que necesitamos
    lista_tuplas = []
    for x in range(1, n+1):
        for y in range(1, 5):
            lista_tuplas.append((x, y))
    return lista_tuplas

#Una vez que este generado el csp, hacemos una funcion que nos retorne los frascos armados
restricciones = []

#Todos los frascos tienen capacidad de 4 segmentos. Esto lo satisfacemos definiendo las variables

#Todos los frascos deben llenarse hasta el tope. El problema tiene que ser completo, asi que esto se satisface en la definición

#No puede haber más de 4 segmentos de un mismo color, de lo contrario no se podría resolver el juego. Restriccion. No lo entiendo

#Ningún frasco debe comenzar resuelto. Es decir, ningún frasco debe tener 4 segmentos del mismo color. Resuelto

#Si dos frascos son adyacentes, deben compartir al menos un color. #Restriccion
#Si dos frascos son adyacentes, no pueden tener más de 6 colores diferentes entre ambos, para evitar situaciones demasiado complejas. #Restriccion
#No puede haber dos frascos exáctamente iguales. Restriccion.

def no_resuelto(vars, vals):
    for frasco in range(1, n+1):
        colores_frasco = []
        for posicion_frasco in range(1, 5):
            colores_frasco.append(variables[frasco,posicion_frasco])
        colores_frasco = set(colores_frasco)
        if len(colores_frasco) != 1:
            return False
            break
    return True

#Ningún color puede comenzar con todos sus segmentos en el fondo de frascos,
# porque se trataría de una situación excesivamente difícil de resolver. Restriccion
def todos_al_fondo(vars,vals): #No se me 
    colores_Fondo = [] #Lo que se me ocurre es agregar colores que estan en el fondo del frasco
    #Fede: es buena esa. Podes contar la cantidad de apariciones de cada color en el fondo. Si alguno tiene 4 apariciones, no se cumple la restriccion

#Comienzo a agregar las restricciones
#Para la restriccion no_resuelto tienen que agruparse las variables de un mismo frasco    