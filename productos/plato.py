from .producto import Producto


class Plato(Producto):
    def __init__(self, nombre, precio, dias_disponibles):
        super().__init__(nombre, precio)
        self._dias_disponibles = dias_disponibles

    def calcular_precio(self):
        return self._precio

    def estas_disponible(self, dia):
        return dia.lower() in self._dias_disponibles

    def contar_platos(self):
        return 1