class Restaurante:
    def __init__(self, nombre):
        self._nombre = nombre
        self._pedidos = []
        self._clientes = []
        self._productos = []

    def registrar_producto(self, producto):
        self._productos.append(producto)

    def registrar_cliente(self, cliente):
        if not cliente.validar_telefono():
            raise ValueError("El teléfono debe tener 8 dígitos y empezar en 6 o 7.")
        self._clientes.append(cliente)

    def buscar_producto(self, nombre):
        for producto in self._productos:
            if producto.nombre.lower() == nombre.lower():
                return producto
        return None

    def mesa_ocupada(self, numero_mesa):
        for pedido in self._pedidos:
            if pedido.esta_abierto() and pedido.numero_mesa() == numero_mesa:
                return True
        return False

    def registrar_pedido(self, pedido):
        if pedido.numero_mesa() is not None and self.mesa_ocupada(pedido.numero_mesa()):
            raise ValueError(f"La mesa {pedido.numero_mesa()} ya tiene un pedido abierto.")
        self._pedidos.append(pedido)

    def buscar_pedido(self, numero):
        for pedido in self._pedidos:
            if pedido.numero == numero:
                return pedido
        return None

    @property
    def nombre(self):
        return self._nombre

    @property
    def productos(self):
        return self._productos

    @property
    def clientes(self):
        return self._clientes

    @property
    def pedidos(self):
        return self._pedidos