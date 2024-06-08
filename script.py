from entrega1 import jugar

pasos = jugar(
    frascos=(
        ("verde", "azul", "rojo", "naranja"),     # frasco 1, notar el orden de los colores
        ("azul", "rosa", "naranja"),              # frasco 2, notar que es de largo 3, queda un espacio vacío
        ("rosa", "celeste", "verde", "verde"),    # frasco 3, notar cómo "verde" se repite 2 veces por los 2 cuartos iguales
        ("rosa", "rojo", "celeste", "celeste"),   # frasco 4
        ("rojo", "azul", "lila"),                 # frasco 5
        ("verde", "naranja", "celeste", "rojo"),  # frasco 6
        ("azul", "naranja", "rosa"),              # frasco 7
        ("lila", "lila", "lila"),                 # frasco 8, notar la repetición de colores para cada cuarto
        (),                                       # frasco 9, notar que una tupla de largo 0 es un frasco vacío
    ),
    dificil=True,
)

print(pasos)