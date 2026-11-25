from pedido import Pedido


class Local(Pedido):
    def __init__(self, numero, cliente, numero_mesa, porcentaje_descuento=5, platos_minimos=6):
        if numero_mesa < 1 or numero_mesa > 15:
            raise ValueError("La mesa debe estar entre 1 y 15.")
        super().__init__(numero, cliente)
        self._numero_mesa = numero_mesa
        self._porcentaje_descuento = float(porcentaje_descuento)
        self._platos_minimos = platos_minimos

    def numero_mesa(self):
        return self._numero_mesa

    def aplica_descuento(self):
        return self.contar_platos() >= self._platos_minimos

    def descuento_local(self):
        if self.aplica_descuento():
            return self.calcular_subtotal() * self._porcentaje_descuento / 100
        return 0.0

    def calcular_cargo_bs(self):
        return 0.0 - self.descuento_local()

    def tipo(self):
        return "Local"

    def descripcion_cargo(self):
        if self.aplica_descuento():
            return f"Descuento local {self._porcentaje_descuento:.0f}% (mesa {self._numero_mesa})"
        return f"Descuento local (no aplica, menos de {self._platos_minimos} platos)"

