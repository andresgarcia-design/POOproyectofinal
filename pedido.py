from abc import ABC, abstractmethod
from proyectoPOOrestaurante.pagos.metodo_pago import MetodoPago

from .detalle_pedido import DetallePedido


class Pedido(ABC):
    def __init__(self, numero, cliente):
        self._numero = numero
        self._cliente = cliente
        self._productos_pedidos = []
        self._costo = 0.0
        self._estado = "pendiente"
        self._metodo_pago: MetodoPago|None = None

  

    @abstractmethod
    def calcular_cargo_bs(self):
        pass


    def cambiar_estado(self, estado):
        self._estado = estado

    def agregar_producto(self, producto):
        for detalle in self._productos_pedidos:
            if detalle.producto is producto:
                detalle.aumentar_cantidad()
                return
        self._productos_pedidos.append(DetallePedido(producto))

    def quitar_producto(self, producto_a_quitar):
        for detalle in self._productos_pedidos:
            if detalle.producto is producto_a_quitar:
                self._productos_pedidos.remove(detalle)
                return True
        return False
    
    def calcular_cargos(self):
        return self.calcular_cargo_bs()

    def pagar(self, metodo_pago: MetodoPago):
        self._metodo_pago = metodo_pago
        resultado = metodo_pago.procesar_pago(self.calcular_total())
        self._estado = "pagado"
        return resultado
    #extras
    def calcular_total(self):
            subtotal = sum(detalle.calcular_subtotal() for detalle in self._productos_pedidos)
            self._costo = subtotal + self.calcular_cargo_bs()
            return self._costo

    def resumen(self):
        lineas = [f"Pedido #{self._numero}", f"Cliente: {self._cliente.nombre}", f"Estado: {self._estado}"]
        lineas.extend(f"- {detalle}" for detalle in self._productos_pedidos)
        lineas.append(f"Cargo: Bs {self.calcular_cargo_bs():.2f}")
        lineas.append(f"Total: Bs {self.calcular_total():.2f}")
        return "\n".join(lineas)

    @property
    def productos_pedidos(self):
        return self._productos_pedidos

    @property
    def costo(self):
        return self._costo
