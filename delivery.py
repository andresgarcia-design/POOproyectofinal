from .pedido import Pedido


class Delivery(Pedido):
    def __init__(self, numero, cliente, costo_zona, pedido_minimo=60):
        super().__init__(numero, cliente)
        self._costo_zona = float(costo_zona)
        self._pedido_minimo = float(pedido_minimo)

    def calcular_cargo_bs(self):
        return self._costo_zona
#extras
    def cumple_pedido_minimo(self):
        subtotal = sum(detalle.calcular_subtotal() for detalle in self._productos_pedidos)
        return subtotal >= self._pedido_minimo
