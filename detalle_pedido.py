class DetallePedido:
    def __init__(self, producto, cantidad=1):
        self._producto = producto
        self._cantidad = cantidad

    @property
    def producto(self):
        return self._producto

    def aumentar_cantidad(self):
        self._cantidad += 1

    def calcular_subtotal(self):
        return self._producto.calcular_precio() * self._cantidad

    def contar_platos(self):
        return self._producto.contar_platos() * self._cantidad

    def __str__(self):
        return f"{self._cantidad} x {self._producto.nombre}: Bs {self.calcular_subtotal():.2f}"
