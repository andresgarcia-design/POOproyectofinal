from pedido import Pedido


class ParaLlevar(Pedido):
    def __init__(self, numero, cliente, costo_envase=3):
        super().__init__(numero, cliente)
        self._costo_envase = float(costo_envase)

    def calcular_cargo_bs(self):
        return self._costo_envase
