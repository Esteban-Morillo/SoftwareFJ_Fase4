"""Clase Reserva: integra cliente, servicio, duración, costo y estado."""

import logging
from entidades import Entidad
from excepciones import ValidacionError, ReservaError, EstadoReservaError, ParametroFaltanteError

logger = logging.getLogger("software_fj")


class Reserva(Entidad):
    ESTADOS_VALIDOS = {"PENDIENTE", "CONFIRMADA", "CANCELADA", "PROCESADA"}

    def __init__(self, cliente, servicio, duracion):
        super().__init__()
        if cliente is None:
            raise ParametroFaltanteError("La reserva requiere un cliente.")
        if servicio is None:
            raise ParametroFaltanteError("La reserva requiere un servicio.")
        if isinstance(duracion, bool) or not isinstance(duracion, (int, float)) or duracion <= 0:
            raise ValidacionError("La duración debe ser un número positivo.")
        self._cliente = cliente
        self._servicio = servicio
        self._duracion = duracion
        self._estado = "PENDIENTE"
        self._costo = None

    @property
    def cliente(self):
        return self._cliente

    @property
    def servicio(self):
        return self._servicio

    @property
    def duracion(self):
        return self._duracion

    @property
    def estado(self):
        return self._estado

    @property
    def costo(self):
        return self._costo

    def confirmar(self, impuesto=0.19, descuento=0):
        if self._estado != "PENDIENTE":
            raise EstadoReservaError(f"No se puede confirmar una reserva en estado {self._estado}.")
        try:
            self._costo = self._servicio.calcular_costo(self._duracion, impuesto, descuento)
        except Exception as exc:
            logger.exception("Error al calcular costo para la reserva %s", self.id)
            raise ReservaError("No fue posible confirmar la reserva por un error en el cálculo.") from exc
        else:
            self._estado = "CONFIRMADA"
            logger.info("Reserva %s confirmada. Costo: %.2f", self.id, self._costo)
            return self._costo

    def cancelar(self):
        if self._estado not in {"PENDIENTE", "CONFIRMADA"}:
            raise EstadoReservaError(f"No se puede cancelar una reserva en estado {self._estado}.")
        self._estado = "CANCELADA"
        logger.info("Reserva %s cancelada.", self.id)

    def procesar(self):
        if self._estado != "CONFIRMADA":
            raise EstadoReservaError("Solo se pueden procesar reservas confirmadas.")
        if self._costo is None or self._costo <= 0:
            raise ReservaError("El costo de la reserva es inconsistente.")
        self._estado = "PROCESADA"
        logger.info("Reserva %s procesada correctamente.", self.id)

    def describir(self):
        costo = f"${self._costo:,.2f}" if self._costo is not None else "Pendiente de cálculo"
        return (
            f"Reserva {self.id[:8]} | Cliente: {self.cliente.nombre} | "
            f"Servicio: {self.servicio.nombre} | Duración: {self.duracion} | "
            f"Estado: {self.estado} | Costo: {costo}"
        )

    def __str__(self):
        return self.describir()
