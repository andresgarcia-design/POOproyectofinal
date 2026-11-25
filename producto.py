from abc import ABC, abstractmethod


class Producto(ABC):
    def __init__(self, nombre, precio):
        self._nombre = nombre
        self._precio = float(precio)

    @property
    def nombre(self):
        return self._nombre

    @abstractmethod
    def calcular_precio(self):
        pass

    @abstractmethod
    def esta_disponible(self, dia):
        pass

    @abstractmethod
    def contar_platos(self):
        pass

    @abstractmethod
    def tipo(self):
        pass

    def __str__(self):
        return f"{self.nombre} - Bs {self.calcular_precio():.2f}"