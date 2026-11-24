from metodo_pago import MetodoPago


class PagoTarjeta(MetodoPago):
    def __init__(self, comision=0.03):
        self._comision = float(comision)

    def procesar_pago(self, total):
        return total + self.calcular_comision(total)

    def calcular_comision(self, total):
        return total * self._comision
