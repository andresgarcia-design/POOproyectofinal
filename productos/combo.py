from .producto import Producto
from .plato import Plato


class Combo(Producto):
    def __init__(self, nombre, descuento=0):
        super().__init__(nombre, 0)
        self._productos = []
        self._descuento = float(descuento)

    def agregar_producto(self, producto):
        if producto is self:
            raise ValueError("Un combo no puede contenerse a sí mismo.")
        self._productos.append(producto)

    def quitar_producto(self, producto_a_quitar):
        for producto in self._productos:
            if producto is producto_a_quitar:
                self._productos.remove(producto)
                return True
        return False

    def calcular_precio(self):
        precio_total = sum(producto.calcular_precio() for producto in self._productos)
        return precio_total - (precio_total * self._descuento / 100)

    def esta_disponible(self, dia):
        for producto in self._productos:
            if not producto.esta_disponible(dia):
                return False
        return True

    def contar_platos(self):
        return sum(producto.contar_platos() for producto in self._productos)
