from metodo_pago import MetodoPago


class PagoTarjeta(MetodoPago):
    def __init__(self, comision=0.03):
        self._comision = float(comision)

    def procesar_pago(self, total):
        return total + self.calcular_comision(total)

    def calcular_comision(self, total):
        return total * self._comision

    def nombre(self):
        return "Tarjeta"

    def lineas_comprobante(self, total, resultado):
        return [f"Comisión ({self._comision * 100:.0f}%): Bs {self.calcular_comision(total):.2f}", f"Total cobrado: Bs {resultado:.2f}"]

    def permitido_en_delivery(self):
        return False
