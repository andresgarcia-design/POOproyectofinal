from restaurante import Restaurante
from plato import Plato



restaurante = Restaurante("Sabor Valluno")
chicharron = Plato("CHICHARRON", 23 , ["domingo"] )
print(chicharron.esta_disponible("Domingo"))
nombre = input()
#nombre = "hola"
platon= Plato(nombre, 21, ["lunes", "martes"])
print(platon.nombre)
print(platon.esta_disponible("martes"))
restaurante.registrar_producto(chicharron)
restaurante.registrar_producto(platon)
print(restaurante.buscar_producto("chicharron"))
print(restaurante.buscar_producto("silpancho"))