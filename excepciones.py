"""Excepciones personalizadas del sistema Software FJ."""


class SoftwareFJError(Exception):
    """Excepción base para errores controlados de la aplicación."""


class ValidacionError(SoftwareFJError):
    """Se presenta cuando un dato no cumple las reglas de validación."""


class ClienteNoEncontradoError(SoftwareFJError):
    """El cliente solicitado no está registrado."""


class ServicioNoDisponibleError(SoftwareFJError):
    """El servicio no se encuentra disponible."""


class ReservaError(SoftwareFJError):
    """Error relacionado con la creación o gestión de una reserva."""


class EstadoReservaError(ReservaError):
    """La operación no está permitida para el estado actual de la reserva."""


class ParametroFaltanteError(SoftwareFJError):
    """Falta un parámetro obligatorio."""
