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
            raise ValueError("El teléfono del cliente debe tener 8 dígitos.")
        self._clientes.append(cliente)

    def buscar_producto(self, nombre):
        for producto in self._productos:
            if producto.nombre.lower() == nombre.lower():
                return producto
        return None

    def registrar_pedido(self, pedido):
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
    