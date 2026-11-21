"""Servicios especializados y comportamiento polimórfico."""

from abc import abstractmethod
from entidades import Entidad
from excepciones import ValidacionError, ServicioNoDisponibleError


class Servicio(Entidad):
    def __init__(self, nombre, tarifa_base, disponible=True):
        super().__init__()
        if not isinstance(nombre, str) or not nombre.strip():
            raise ValidacionError("El nombre del servicio es obligatorio.")
        if isinstance(tarifa_base, bool) or not isinstance(tarifa_base, (int, float)) or tarifa_base <= 0:
            raise ValidacionError("La tarifa base debe ser un número positivo.")
        self._nombre = nombre.strip()
        self._tarifa_base = float(tarifa_base)
        self._disponible = bool(disponible)

    @property
    def nombre(self):
        return self._nombre

    @property
    def tarifa_base(self):
        return self._tarifa_base

    @property
    def disponible(self):
        return self._disponible

    @disponible.setter
    def disponible(self, valor):
        if not isinstance(valor, bool):
            raise ValidacionError("La disponibilidad debe ser True o False.")
        self._disponible = valor

    def validar_disponibilidad(self):
        if not self.disponible:
            raise ServicioNoDisponibleError(f"El servicio '{self.nombre}' no está disponible.")

    @abstractmethod
    def calcular_costo(self, duracion, impuesto=0.19, descuento=0):
        """Calcula el costo según el tipo de servicio."""
        raise NotImplementedError

    @abstractmethod
    def describir(self):
        raise NotImplementedError

    @abstractmethod
    def validar_parametros(self, duracion):
        raise NotImplementedError

    def __str__(self):
        return self.describir()


class ReservaSala(Servicio):
    def __init__(self, nombre, tarifa_base, capacidad, disponible=True):
        super().__init__(nombre, tarifa_base, disponible)
        if isinstance(capacidad, bool) or not isinstance(capacidad, int) or capacidad <= 0:
            raise ValidacionError("La capacidad de la sala debe ser un entero positivo.")
        self._capacidad = capacidad

    def validar_parametros(self, duracion):
        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)) or duracion <= 0:
            raise ValidacionError("La duración de la sala debe ser mayor que cero.")

    def calcular_costo(self, duracion, impuesto=0.19, descuento=0):
        self.validar_disponibilidad()
        self.validar_parametros(duracion)
        validar_impuesto_descuento(impuesto, descuento)
        subtotal = self.tarifa_base * duracion
        return round(subtotal * (1 - descuento) * (1 + impuesto), 2)

    def describir(self):
        return f"Sala '{self.nombre}' | Capacidad: {self._capacidad} personas | Tarifa/hora: ${self.tarifa_base:,.2f}"


class AlquilerEquipo(Servicio):
    def __init__(self, nombre, tarifa_base, unidades_disponibles, disponible=True):
        super().__init__(nombre, tarifa_base, disponible)
        if isinstance(unidades_disponibles, bool) or not isinstance(unidades_disponibles, int) or unidades_disponibles < 0:
            raise ValidacionError("Las unidades disponibles deben ser un entero no negativo.")
        self._unidades_disponibles = unidades_disponibles

    def validar_parametros(self, duracion):
        if isinstance(duracion, bool) or not isinstance(duracion, int) or duracion <= 0:
            raise ValidacionError("La duración del alquiler debe ser un número entero de días.")
        if self._unidades_disponibles < 1:
            raise ServicioNoDisponibleError(f"No hay unidades disponibles de '{self.nombre}'.")

    def calcular_costo(self, duracion, impuesto=0.19, descuento=0):
        self.validar_disponibilidad()
        self.validar_parametros(duracion)
        validar_impuesto_descuento(impuesto, descuento)
        subtotal = self.tarifa_base * duracion
        return round(subtotal * (1 - descuento) * (1 + impuesto), 2)

    def describir(self):
        return f"Equipo '{self.nombre}' | Unidades disponibles: {self._unidades_disponibles} | Tarifa/día: ${self.tarifa_base:,.2f}"


class AsesoriaEspecializada(Servicio):
    def __init__(self, nombre, tarifa_base, especialidad, disponible=True):
        super().__init__(nombre, tarifa_base, disponible)
        if not isinstance(especialidad, str) or not especialidad.strip():
            raise ValidacionError("La especialidad de la asesoría es obligatoria.")
        self._especialidad = especialidad.strip()

    def validar_parametros(self, duracion):
        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)) or duracion <= 0:
            raise ValidacionError("La duración de la asesoría debe ser mayor que cero.")

    def calcular_costo(self, duracion, impuesto=0.19, descuento=0):
        self.validar_disponibilidad()
        self.validar_parametros(duracion)
        validar_impuesto_descuento(impuesto, descuento)
        subtotal = self.tarifa_base * duracion
        return round(subtotal * (1 - descuento) * (1 + impuesto), 2)

    def describir(self):
        return f"Asesoría '{self.nombre}' | Especialidad: {self._especialidad} | Tarifa/hora: ${self.tarifa_base:,.2f}"


def validar_impuesto_descuento(impuesto, descuento):
    if isinstance(impuesto, bool) or not isinstance(impuesto, (int, float)) or not 0 <= impuesto <= 1:
        raise ValidacionError("El impuesto debe estar entre 0 y 1 (por ejemplo, 0.19).")
    if isinstance(descuento, bool) or not isinstance(descuento, (int, float)) or not 0 <= descuento <= 1:
        raise ValidacionError("El descuento debe estar entre 0 y 1.")
