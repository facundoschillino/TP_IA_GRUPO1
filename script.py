from entrega2 import armar_nivel

# frascos = armar_nivel(colores=["rojo", "verde", "azul","amarillo"], 
#     contenidos_parciales=[
#         ("verde", "azul", "rojo", "rojo"),    
#         ("verde", "rojo"),                     
#     ],
# )

frascos = armar_nivel(colores=['rojo', 'verde', 'azul', 'celeste', 'lila', 'naranja', 'amarillo', 'verde_oscuro'], 
    contenidos_parciales=[
        ('rojo', 'verde_oscuro', 'verde_oscuro', 'verde_oscuro'),
        ('celeste', 'azul', 'azul'),
        ('naranja', 'verde_oscuro', 'verde', 'azul'),
        ('amarillo', 'amarillo'),
        ('celeste',)                     
    ],
)

print(frascos)