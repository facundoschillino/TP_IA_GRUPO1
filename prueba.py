from simpleai.search import CspProblem, backtrack

# Cantidad de frascos/colores
CANTIDAD_COLORES = 4

# Generar variables para cada segmento de cada frasco
variables = [(frasco, segmento) for frasco in range(1, CANTIDAD_COLORES + 1) for segmento in range(1, 5)]

# Dominio de colores
dominio = ["Celeste", "Blanco", "Rojo", "Verde"]

# Inicializar restricciones
restricciones = []

# Restricción: No puede haber más de 4 segmentos de un mismo color en total
def restriccion_solo_4(variables, valores):
    conteo_colores = {color: 0 for color in dominio}
    for valor in valores:
        conteo_colores[valor] += 1
    return all(conteo <= 4 for conteo in conteo_colores.values())

restricciones.append((variables, restriccion_solo_4))

# Restricción: Ningún frasco debe comenzar resuelto (no 4 segmentos del mismo color en un frasco)
def restriccion_no_resuelto(frasco):
    def restriccion(frasco_vars, frasco_vals):
        return len(set(frasco_vals)) > 1
    frasco_vars = [(frasco, segmento) for segmento in range(1, 5)]
    restricciones.append((frasco_vars, restriccion))

for frasco in range(1, CANTIDAD_COLORES + 1):
    restriccion_no_resuelto(frasco)

# Restricción: Ningún color puede comenzar con todos sus segmentos en el fondo de frascos
def restriccion_todos_al_fondo(variables, valores):
    fondo_colores = [valores[i] for i in range(0, len(valores), 4)]
    conteo_colores = {color: fondo_colores.count(color) for color in dominio}
    return all(conteo < 4 for conteo in conteo_colores.values())

restricciones.append((variables, restriccion_todos_al_fondo))

# Restricción: Si dos frascos son adyacentes, deben compartir al menos un color
def restriccion_compartir_color(frasco1, frasco2):
    def restriccion(vars, vals):
        colores_frasco1 = set(vals[:4])
        colores_frasco2 = set(vals[4:])
        return len(colores_frasco1 & colores_frasco2) > 0
    frasco1_vars = [(frasco1, segmento) for segmento in range(1, 5)]
    frasco2_vars = [(frasco2, segmento) for segmento in range(1, 5)]
    restricciones.append((frasco1_vars + frasco2_vars, restriccion))

for frasco in range(1, CANTIDAD_COLORES):
    restriccion_compartir_color(frasco, frasco + 1)

# Restricción: Si dos frascos son adyacentes, no pueden tener más de 6 colores diferentes entre ambos
def restriccion_no_seis_colores(variables, valores):
    for i in range(CANTIDAD_COLORES - 1):
        frasco1_valores = valores[i*4:(i+1)*4]
        frasco2_valores = valores[(i+1)*4:(i+2)*4]
        if len(set(frasco1_valores + frasco2_valores)) > 6:
            return False
    return True

restricciones.append((variables, restriccion_no_seis_colores))

# Restricción: No puede haber dos frascos exactamente iguales
def restriccion_frascos_distintos(frasco1, frasco2):
    def restriccion(vars, vals):
        return vals[:4] != vals[4:]
    frasco1_vars = [(frasco1, segmento) for segmento in range(1, 5)]
    frasco2_vars = [(frasco2, segmento) for segmento in range(1, 5)]
    restricciones.append((frasco1_vars + frasco2_vars, restriccion))

for frasco1 in range(1, CANTIDAD_COLORES + 1):
    for frasco2 in range(frasco1 + 1, CANTIDAD_COLORES + 1):
        restriccion_frascos_distintos(frasco1, frasco2)

# Definir el problema CSP
problema = CspProblem(variables, {var: dominio for var in variables}, restricciones)

# Resolver el problema
solucion = backtrack(problema)

# Mostrar la solución
print("Solución encontrada:")
for frasco in range(1, CANTIDAD_COLORES + 1):
    print(f"Frasco {frasco}:")
    for segmento in range(1, 5):
        print(f"  Segmento {segmento}: {solucion[(frasco, segmento)]}")
