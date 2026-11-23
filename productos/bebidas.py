from .producto import Producto


class Bebida(Producto):
    def __init__(self, nombre, precio, tipo_bebida="vaso"):
        super().__init__(nombre, precio)
        self._tipo_bebida = tipo_bebida

    def calcular_precio(self):
        return self._precio

    def esta_disponible(self, dia):
        return True

    def contar_platos(self):
        return 0