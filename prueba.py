variables = [] 
dominio = []
def generar_variables(n):  
    lista_tuplas = []
    for x in range(1, n + 1):
        for y in range(1, 5):
            lista_tuplas.append((x, y))
    return lista_tuplas
colores = ['Celeste', 'Blanco', 'Rojo', 'Verde']
dominio = {(1, 1): 'Celeste', (1, 2): 'Celeste', (1, 3): 'Celeste', (1, 4): 'Blanco', (2, 1): 'Celeste', (2, 2): 'Blanco', (2, 3): 'Blanco', (2, 4): 'Rojo', (3, 1): 'Blanco', (3, 2): 'Rojo', (3, 3): 'Rojo', (3, 4): 'Verde', (4, 1): 'Rojo', (4, 2): 'Verde', (4, 3): 'Verde', (4, 4): 'Verde'}






def compartir_color(vars, vals, CANTIDAD_COLORES):  
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
keys = list(dominio.keys())
values = list(dominio.values())

resultado = compartir_color(keys, values, 4)
print(resultado)