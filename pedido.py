from abc import ABC, abstractmethod
from metodo_pago import MetodoPago

from .detalle_pedido import DetallePedido


class Pedido(ABC):
    TRANSICIONES = {
        "registrado": ["cancelado"],
        "pagado": ["en preparación", "cancelado"],
        "en preparación": ["listo"],
        "listo": ["entregado"],
        "entregado": [],
        "cancelado": [],
    }

    def __init__(self, numero, cliente):
        self._numero = numero
        self._cliente = cliente
        self._productos_pedidos = []
        self._costo = 0.0
        self._estado = "registrado"
        self._metodo_pago: MetodoPago | None = None

    @abstractmethod
    def calcular_cargo_bs(self):
        pass

    def estados_siguientes(self):
        return self.TRANSICIONES[self._estado]

    def cambiar_estado(self, estado):
        if estado not in self.estados_siguientes():
            raise ValueError(f"No se puede pasar del estado '{self._estado}' a '{estado}'.")
        self._estado = estado

    def puede_modificarse(self):
        return self._estado == "registrado"

    def agregar_producto(self, producto):
        if not self.puede_modificarse():
            raise ValueError("Solo se pueden agregar productos a un pedido en estado 'registrado'.")
        for detalle in self._productos_pedidos:
            if detalle.producto is producto:
                detalle.aumentar_cantidad()
                return
        self._productos_pedidos.append(DetallePedido(producto))

    def quitar_producto(self, producto_a_quitar):
        if not self.puede_modificarse():
            raise ValueError("Solo se pueden quitar productos de un pedido en estado 'registrado'.")
        for detalle in self._productos_pedidos:
            if detalle.producto is producto_a_quitar:
                self._productos_pedidos.remove(detalle)
                return True
        return False

    def calcular_cargos(self):
        return self.calcular_cargo_bs()

    def pagar(self, metodo_pago: MetodoPago):
        if self._estado != "registrado":
            raise ValueError("Solo se pueden cobrar pedidos en estado 'registrado'.")
        if len(self._productos_pedidos) == 0:
            raise ValueError("El pedido no tiene productos.")
        resultado = metodo_pago.procesar_pago(self.calcular_total())
        self._metodo_pago = metodo_pago
        self._estado = "pagado"
        return resultado

    def fue_pagado(self):
        return self._estado in ["pagado", "en preparación", "listo", "entregado"]

    def calcular_total(self):
        subtotal = sum(detalle.calcular_subtotal() for detalle in self._productos_pedidos)
        self._costo = round(subtotal + self.calcular_cargo_bs(), 2)
        return self._costo

    def resumen(self):
        lineas = [f"Pedido #{self._numero}", f"Cliente: {self._cliente.nombre}", f"Estado: {self._estado}"]
        lineas.extend(f"- {detalle}" for detalle in self._productos_pedidos)
        lineas.append(f"Cargo: Bs {self.calcular_cargo_bs():.2f}")
        lineas.append(f"Total: Bs {self.calcular_total():.2f}")
        return "\n".join(lineas)

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
