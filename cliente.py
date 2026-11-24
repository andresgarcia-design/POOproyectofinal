class Cliente:
    def __init__(self, nombre, telefono):
        self._nombre = nombre
        self._telefono = telefono

    @property
    def nombre(self):
        return self._nombre

    def validar_telefono(self):
        return self._telefono.isdigit() and len(self._telefono) == 8
