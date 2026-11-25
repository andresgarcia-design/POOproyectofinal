from abc import ABC, abstractmethod

class MetodoPago(ABC):
    @abstractmethod
    def procesar_pago(self, total):
        pass

    @abstractmethod
    def nombre(self):
        pass

    @abstractmethod
    def lineas_comprobante(self, total, resultado):
        pass

    @abstractmethod
    def permitido_en_delivery(self):
        pass
