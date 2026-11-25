from metodo_pago import MetodoPago


class PagoQR(MetodoPago):
    def __init__(self, codigo_transaccion):
        self._codigo_transaccion = codigo_transaccion

    def procesar_pago(self, total):
        if not self.validar_codigo():
            raise ValueError("El código QR debe tener exactamente 10 dígitos.")
        return total

    def validar_codigo(self):
        return self._codigo_transaccion.isdigit() and len(self._codigo_transaccion) == 10

    def nombre(self):
        return "QR"

    def lineas_comprobante(self, total, resultado):
        return [f"Código de transacción: {self._codigo_transaccion}", f"Total cobrado: Bs {resultado:.2f}"]

    def permitido_en_delivery(self):
        return True
