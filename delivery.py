from pedido import Pedido


class Delivery(Pedido):
    def __init__(self, numero, cliente, zona, pedido_minimo=60):
        super().__init__(numero, cliente)
        self._zona = zona
        self._costo_zona = self.costo_por_zona(zona)
        self._pedido_minimo = float(pedido_minimo)

    def costo_por_zona(self, zona):
        if zona == "Cercado":
            return 8.0
        if zona == "Quillacollo":
            return 15.0
        if zona == "Sacaba":
            return 15.0
        if zona == "Vinto":
            return 20.0
        raise ValueError("Zona no válida. Zonas: Cercado, Quillacollo, Sacaba, Vinto.")

    def calcular_cargo_bs(self):
        return self._costo_zona

    def tipo(self):
        return "Delivery"

    def descripcion_cargo(self):
        return f"Envío a {self._zona}"

    def cumple_pedido_minimo(self):
        return self.calcular_subtotal() >= self._pedido_minimo

    def acepta_metodo(self, metodo_pago):
        return metodo_pago.permitido_en_delivery()

    def validar_pago(self):
        super().validar_pago()
        if not self.cumple_pedido_minimo():
            raise ValueError(f"El delivery necesita un subtotal mínimo de Bs {self._pedido_minimo:.2f}.")
