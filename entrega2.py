from simpleai.search import (CspProblem, backtrack, min_conflicts,
                             MOST_CONSTRAINED_VARIABLE,
                             LEAST_CONSTRAINING_VALUE)
variables = [] 
dominio = {}
def generar_variables(n):  
    lista_tuplas = []
    for x in range(1, n + 1):
        for y in range(1, 5):
            lista_tuplas.append((x, y))
    return lista_tuplas
def armar_nivel(colores, contenido_seleccionado):
    variables = generar_variables(len(colores))
    dominio = {var: colores for var in variables}
    for indice_frasco, frasco in enumerate(contenido_seleccionado):
        for indice, color in enumerate(frasco):
            dominio[(indice_frasco + 1, indice + 1)] = color
    cantidad_colores = len(colores)


    restricciones.append((variables, solo_4))
    restricciones.append((variables, no_resuelto))
    restricciones.append((variables, todos_al_fondo))
    restricciones.append((variables, compartir_color))
    restricciones.append((variables, que_no_haya_6))
    restricciones.append((variables, todos_distintos))
    problema = CspProblem(variables, dominio, restricciones)
    solucion = backtrack(problema, variable_heuristic=MOST_CONSTRAINED_VARIABLE, value_heuristic=LEAST_CONSTRAINING_VALUE)


    frascos = [[] for _ in range(cantidad_colores)]
    for posicion in solucion:
        frasco, cuarto = posicion
        frascos[frasco -1].append(solucion[posicion])
    return frascos

restricciones = []
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
def no_resuelto(vars, vals):
    CANTIDAD_COLORES = len(set(vals))  
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
def todos_al_fondo(vars, vals):  
    colores_fondo = [val for var, val in zip(vars, vals) if var[1] == 1]
    conteo = {color: colores_fondo.count(color) for color in colores_fondo}
    return all(c < 4 for c in conteo.values())

def compartir_color(vars, vals):
    CANTIDAD_COLORES = len(set(vals))  
    frascos = [[] for _ in range(CANTIDAD_COLORES)]
    for var, val in zip(vars, vals):
        frasco, cuarto = var
        frascos[frasco - 1].append(val)
    for indice, frasco in enumerate(frascos):
        if indice > 0 and not set(frasco).intersection(frascos[indice - 1]):
            return False
        if indice < CANTIDAD_COLORES - 1 and not set(frasco).intersection(frascos[indice + 1]):
            return False
    return True
def que_no_haya_6(vars, vals):
    CANTIDAD_COLORES = len(set(vals)) 
    frascos = [[] for _ in range(1,CANTIDAD_COLORES+1)]
    for var, val in zip(vars, vals):
        frasco, cuarto = var
        frascos[frasco - 1].append(val)
    for indice, frasco in enumerate(frascos):
        if indice > 0 and len(set(frasco + frascos[indice - 1])) > 6:
            return False
        if indice < CANTIDAD_COLORES - 1 and len(set(frasco + frascos[indice + 1])) > 6:
            return False
    return True
def todos_distintos(vars, vals):
    CANTIDAD_COLORES = len(set(vals))   
    frascos = [[] for _ in range(CANTIDAD_COLORES)]
    for var, val in zip(vars, vals):
        frasco, cuarto = var
        frascos[frasco - 1].append(val)
    return len(set(tuple(frasco) for frasco in frascos)) == CANTIDAD_COLORES

frascos = armar_nivel(colores=["rojo", "verde", "azul", "amarillo"],  # 4 colores, por lo que deberemos armar 4 frascos
    contenido_seleccionado=[
        ("verde", "azul", "rojo", "rojo"),    
        ("verde", "rojo"),                     
    ],
)

print(frascos)