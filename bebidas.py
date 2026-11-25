from producto import Producto


class Bebida(Producto):
    def __init__(self, nombre, precio, tipo_bebida="vaso"):
        if float(precio) <= 0:
            raise ValueError("El precio debe ser mayor que cero.")
        if tipo_bebida != "vaso" and tipo_bebida != "jarra":
            raise ValueError("El tipo de bebida debe ser 'vaso' o 'jarra'.")
        super().__init__(nombre, precio)
        self._tipo_bebida = tipo_bebida

    def calcular_precio(self):
        if self._tipo_bebida == "jarra":
            return self._precio * 3
        return self._precio

    def esta_disponible(self, dia):
        return True

    def contar_platos(self):
        return 0

    def tipo(self):
        return "Bebida"