from metodo_pago import MetodoPago


class PagoEfectivo(MetodoPago):
    def __init__(self, monto_recibido):
        self._monto_recibido = float(monto_recibido)

    def procesar_pago(self, total):
        if self._monto_recibido < total:
            raise ValueError("El monto recibido no alcanza para pagar el pedido.")
        return self.calcular_cambio(total)

    def calcular_cambio(self, total) -> float:
        return self._monto_recibido - total

    def redondear_total(self, total:float) -> float:
        return round(total, 2)
