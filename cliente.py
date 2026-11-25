class Cliente:
    def __init__(self, nombre, telefono):
        self._nombre = nombre
        self._telefono = telefono

    @property
    def nombre(self):
        return self._nombre

    def validar_telefono(self):
        if not self._telefono.isdigit() or len(self._telefono) != 8:
            return False
        return self._telefono[0] == "6" or self._telefono[0] == "7"
