from simpleai.search import (CspProblem, backtrack, min_conflicts,
                             MOST_CONSTRAINED_VARIABLE, LEAST_CONSTRAINING_VALUE)


def generar_variables(n):
    return [(frasco, posicion) for frasco in range(1, n + 1) for posicion in range(1, 5)]


def armar_nivel(colores, contenidos_parciales):
    num_frascos = len(colores)
    variables = generar_variables(num_frascos)

    # Crear el dominio de cada variable
    dominio = {var: list(colores) for var in variables}
    for frasco_idx, frasco in enumerate(contenidos_parciales):
        for pos_idx, color in enumerate(frasco):
            dominio[(frasco_idx + 1, pos_idx + 1)] = [color]

    # Definición de restricciones
    restricciones = []

    def solo_4(vars, vals):
        color_count = {}
        for val in vals:
            if val is not None:
                color_count[val] = color_count.get(val, 0) + 1
                if color_count[val] > 4:
                    return False
        return True

    def no_resuelto(vars, vals):
        frascos = [[] for _ in range(num_frascos)]
        for var, val in zip(vars, vals):
            if val is not None:
                frascos[var[0] - 1].append(val)
        for frasco in frascos:
            if len(frasco) == 4 and len(set(frasco)) == 1:
                return False
        return True

    def todos_al_fondo(vars, vals):
        color_fondo = [vals[i] for i in range(len(vars)) if vars[i][1] == 1 and vals[i] is not None]
        color_count = {color: color_fondo.count(color) for color in set(color_fondo)}
        return all(count < 4 for count in color_count.values())

    def compartir_color(vars, vals):
        frascos = [[] for _ in range(num_frascos)]
        for var, val in zip(vars, vals):
            if val is not None:
                frascos[var[0] - 1].append(val)
        for i in range(1, num_frascos):
            if not set(frascos[i - 1]).intersection(frascos[i]):
                return False
        return True

    def que_no_haya_6(vars, vals):
        frascos = [[] for _ in range(num_frascos)]
        for var, val in zip(vars, vals):
            if val is not None:
                frascos[var[0] - 1].append(val)
        for i in range(1, num_frascos):
            if len(set(frascos[i - 1] + frascos[i])) > 6:
                return False
        return True

    def todos_distintos(vars, vals):
        frascos = [[] for _ in range(num_frascos)]
        for var, val in zip(vars, vals):
            if val is not None:
                frascos[var[0] - 1].append(val)
        frascos_tuplas = [tuple(frasco) for frasco in frascos if len(frasco) == 4]
        return len(frascos_tuplas) == len(set(frascos_tuplas))

    restricciones.append((variables, solo_4))
    restricciones.append((variables, no_resuelto))
    restricciones.append((variables, todos_al_fondo))
    restricciones.append((variables, compartir_color))
    restricciones.append((variables, que_no_haya_6))
    restricciones.append((variables, todos_distintos))

    # Crear el problema CSP y resolverlo
    problema = CspProblem(variables, dominio, restricciones)
    #solucion = backtrack(problema, variable_heuristic=MOST_CONSTRAINED_VARIABLE, value_heuristic=LEAST_CONSTRAINING_VALUE)
    solucion = min_conflicts(problema, 40000)

    # Convertir la solución en el formato esperado
    frascos_armados = []
    for frasco in range(1, num_frascos + 1):
        frasco_values = [solucion[(frasco, pos)] for pos in range(1, 5)]
        frascos_armados.append(tuple(frasco_values))

    return frascos_armados
