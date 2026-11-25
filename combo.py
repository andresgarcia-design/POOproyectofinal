from producto import Producto


class Combo(Producto):
    def __init__(self, nombre, descuento=15, minimo_productos=3):
        super().__init__(nombre, 0)
        self._productos = []
        self._descuento = float(descuento)
        self._minimo_productos = minimo_productos

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

    def aplica_descuento(self):
        return len(self._productos) >= self._minimo_productos

    def calcular_precio(self):
        precio_total = sum(producto.calcular_precio() for producto in self._productos)
        if self.aplica_descuento():
            return precio_total - (precio_total * self._descuento / 100)
        return precio_total

    def esta_disponible(self, dia):
        for producto in self._productos:
            if not producto.esta_disponible(dia):
                return False
        return True

    def contar_platos(self):
        return sum(producto.contar_platos() for producto in self._productos)

    def tipo(self):
        return "Combo"
