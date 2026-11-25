from abc import ABC, abstractmethod

from detalle_pedido import DetallePedido


class Pedido(ABC):
    def __init__(self, numero, cliente):
        self._numero = numero
        self._cliente = cliente
        self._productos_pedidos = []
        self._costo = 0.0
        self._estado = "REGISTRADO"
        self._metodo_pago = None

    @abstractmethod
    def calcular_cargo_bs(self):
        pass

    @abstractmethod
    def tipo(self):
        pass

    @abstractmethod
    def descripcion_cargo(self):
        pass

    def numero_mesa(self):
        return None

    def acepta_metodo(self, metodo_pago):
        return True

    def esta_pagado(self):
        return self._metodo_pago is not None

    def esta_abierto(self):
        return self._estado != "ENTREGADO" and self._estado != "CANCELADO"

    def estados_siguientes(self):
        if self._estado == "REGISTRADO":
            if self.esta_pagado():
                return ["EN_PREPARACION"]
            return ["EN_PREPARACION", "CANCELADO"]
        if self._estado == "EN_PREPARACION":
            return ["LISTO"]
        if self._estado == "LISTO":
            return ["ENTREGADO"]
        return []

    def cambiar_estado(self, estado):
        if estado not in self.estados_siguientes():
            raise ValueError(f"No se puede pasar del estado {self._estado} a {estado}.")
        self._estado = estado

    def puede_modificarse(self):
        return self._estado == "REGISTRADO" and not self.esta_pagado()

    def agregar_producto(self, producto):
        if not self.puede_modificarse():
            raise ValueError("Solo se agregan productos a un pedido REGISTRADO y sin pagar.")
        for detalle in self._productos_pedidos:
            if detalle.producto is producto:
                detalle.aumentar_cantidad()
                return
        self._productos_pedidos.append(DetallePedido(producto))

    def quitar_producto(self, producto_a_quitar):
        if not self.puede_modificarse():
            raise ValueError("Solo se quitan productos de un pedido REGISTRADO y sin pagar.")
        for detalle in self._productos_pedidos:
            if detalle.producto is producto_a_quitar:
                self._productos_pedidos.remove(detalle)
                return True
        return False

    def calcular_subtotal(self):
        subtotal = 0.0
        for detalle in self._productos_pedidos:
            subtotal += detalle.calcular_subtotal()
        return subtotal

    def contar_platos(self):
        platos = 0
        for detalle in self._productos_pedidos:
            platos += detalle.contar_platos()
        return platos

    def calcular_cargos(self):
        return self.calcular_cargo_bs()

    def validar_pago(self):
        if self._estado == "CANCELADO":
            raise ValueError("No se puede cobrar un pedido CANCELADO.")
        if self.esta_pagado():
            raise ValueError("Este pedido ya fue pagado.")
        if len(self._productos_pedidos) == 0:
            raise ValueError("El pedido no tiene productos.")

    def pagar(self, metodo_pago):
        self.validar_pago()
        if not self.acepta_metodo(metodo_pago):
            raise ValueError(f"Un pedido {self.tipo()} no acepta pago con {metodo_pago.nombre()}.")
        resultado = metodo_pago.procesar_pago(self.calcular_total())
        self._metodo_pago = metodo_pago
        return resultado

    def calcular_total(self):
        self._costo = round(self.calcular_subtotal() + self.calcular_cargo_bs(), 2)
        return self._costo

    def resumen(self):
        texto = f"Pedido #{self._numero} - {self.tipo()}\n"
        texto += f"Cliente: {self._cliente.nombre}\n"
        if self.esta_pagado():
            texto += f"Estado: {self._estado} (pagado)\n"
        else:
            texto += f"Estado: {self._estado} (sin pagar)\n"
        for detalle in self._productos_pedidos:
            texto += f"  - {detalle}\n"
        texto += f"Subtotal: Bs {self.calcular_subtotal():.2f}\n"
        texto += f"{self.descripcion_cargo()}: Bs {self.calcular_cargo_bs():.2f}\n"
        texto += f"Total: Bs {self.calcular_total():.2f}"
        return texto

    @property
    def numero(self):
        return self._numero

    @property
    def cliente(self):
        return self._cliente

    @property
    def estado(self):
        return self._estado

    @property
    def productos_pedidos(self):
        return self._productos_pedidos

    @property
    def costo(self):
        return self._costo
