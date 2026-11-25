from pedido import Pedido

class ParaLlevar(Pedido):
    def __init__(self, numero, cliente, costo_envase=2):
        super().__init__(numero, cliente)
        self._costo_envase = float(costo_envase)

    def calcular_cargo_bs(self):
        return self._costo_envase * self.contar_platos()

    def tipo(self):
        return "Para llevar"

    def descripcion_cargo(self):
        return f"Envases (Bs {self._costo_envase:.2f} x {self.contar_platos()} platos)"