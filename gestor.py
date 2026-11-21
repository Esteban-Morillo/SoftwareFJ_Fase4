"""Gestor central: mantiene los objetos en listas, sin base de datos."""

import logging
from clientes import Cliente
from servicios import Servicio
from reservas import Reserva
from excepciones import ClienteNoEncontradoError, ValidacionError

logger = logging.getLogger("software_fj")


class GestorSoftwareFJ:
    def __init__(self):
        self._clientes = []
        self._servicios = []
        self._reservas = []

    @property
    def clientes(self):
        return tuple(self._clientes)

    @property
    def servicios(self):
        return tuple(self._servicios)

    @property
    def reservas(self):
        return tuple(self._reservas)

    def registrar_cliente(self, nombre, correo, telefono):
        cliente = Cliente(nombre, correo, telefono)
        if any(c.correo == cliente.correo for c in self._clientes):
            raise ValidacionError(f"Ya existe un cliente con el correo {cliente.correo}.")
        self._clientes.append(cliente)
        logger.info("Cliente registrado: %s", cliente.correo)
        return cliente

    def agregar_servicio(self, servicio):
        if not isinstance(servicio, Servicio):
            raise ValidacionError("Solo se pueden agregar objetos derivados de Servicio.")
        if any(s.nombre.lower() == servicio.nombre.lower() for s in self._servicios):
            raise ValidacionError(f"Ya existe un servicio llamado '{servicio.nombre}'.")
        self._servicios.append(servicio)
        logger.info("Servicio agregado: %s", servicio.nombre)
        return servicio

    def buscar_cliente(self, correo):
        for cliente in self._clientes:
            if cliente.correo == correo.strip().lower():
                return cliente
        raise ClienteNoEncontradoError(f"No se encontró el cliente con correo {correo!r}.")

    def crear_reserva(self, correo_cliente, servicio, duracion):
        cliente = self.buscar_cliente(correo_cliente)
        if servicio not in self._servicios:
            raise ValidacionError("El servicio debe estar registrado en el sistema.")
        reserva = Reserva(cliente, servicio, duracion)
        self._reservas.append(reserva)
        logger.info("Reserva creada: %s", reserva.id)
        return reserva
