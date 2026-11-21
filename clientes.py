"""Clase Cliente con encapsulación y validaciones robustas."""

import re
from entidades import Entidad
from excepciones import ValidacionError


class Cliente(Entidad):
    def __init__(self, nombre, correo, telefono):
        super().__init__()
        self.nombre = nombre
        self.correo = correo
        self.telefono = telefono

    @property
    def nombre(self):
        return self._nombre

    @nombre.setter
    def nombre(self, valor):
        if not isinstance(valor, str) or len(valor.strip()) < 2:
            raise ValidacionError("El nombre debe contener al menos 2 caracteres.")
        self._nombre = valor.strip()

    @property
    def correo(self):
        return self._correo

    @correo.setter
    def correo(self, valor):
        if not isinstance(valor, str) or not re.fullmatch(
            r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}", valor.strip()
        ):
            raise ValidacionError(f"Correo electrónico inválido: {valor!r}")
        self._correo = valor.strip().lower()

    @property
    def telefono(self):
        return self._telefono

    @telefono.setter
    def telefono(self, valor):
        if not isinstance(valor, str) or not re.fullmatch(r"\+?\d{7,15}", valor.strip()):
            raise ValidacionError("El teléfono debe contener entre 7 y 15 dígitos; puede iniciar con +.")
        self._telefono = valor.strip()

    def describir(self):
        return f"Cliente: {self.nombre} | Correo: {self.correo} | Teléfono: {self.telefono}"

    def __str__(self):
        return self.describir()
