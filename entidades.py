"""Entidad abstracta general para los objetos principales del sistema."""

from abc import ABC, abstractmethod
from datetime import datetime
from uuid import uuid4


class Entidad(ABC):
    """Define los atributos y comportamientos comunes de una entidad."""

    def __init__(self, identificador=None):
        self._id = str(identificador or uuid4())
        self._fecha_creacion = datetime.now()

    @property
    def id(self):
        return self._id

    @property
    def fecha_creacion(self):
        return self._fecha_creacion

    @abstractmethod
    def describir(self):
        """Devuelve una descripción legible de la entidad."""
        raise NotImplementedError
