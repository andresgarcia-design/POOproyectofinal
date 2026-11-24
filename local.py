from pedido import Pedido


class Local(Pedido):
    def __init__(self, numero, cliente, numero_mesa):
        super().__init__(numero, cliente)
        self._numero_mesa = numero_mesa

    def calcular_cargo_bs(self):
        # El descuento se representa como un cargo negativo.
        return -self.descuento_local()

    def descuento_local(self):
        subtotal = sum(detalle.calcular_subtotal() for detalle in self._productos_pedidos)
        return subtotal * 0.15
