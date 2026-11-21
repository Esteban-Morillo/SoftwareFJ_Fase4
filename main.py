"""Aplicación interactiva de Software FJ.

Los registros se realizan a petición del usuario desde el menú.
No se ejecutan operaciones de demostración automáticamente.
"""

import logging
import os

from gestor import GestorSoftwareFJ
from servicios import ReservaSala, AlquilerEquipo, AsesoriaEspecializada
from excepciones import SoftwareFJError, ValidacionError

RUTA_LOGS = os.path.join(os.path.dirname(__file__), "logs")
os.makedirs(RUTA_LOGS, exist_ok=True)

logging.basicConfig(
    filename=os.path.join(RUTA_LOGS, "software_fj.log"),
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    encoding="utf-8",
)
logger = logging.getLogger("software_fj")


def leer_texto(mensaje):
    valor = input(mensaje).strip()
    if not valor:
        raise ValidacionError("Este campo no puede quedar vacío.")
    return valor


def leer_numero(mensaje, entero=False):
    texto = leer_texto(mensaje)
    try:
        numero = int(texto) if entero else float(texto)
    except ValueError as exc:
        raise ValidacionError("Debes ingresar un número válido.") from exc
    return numero


def pausar():
    input("\nPresiona ENTER para volver al menú...")


def registrar_cliente(sistema):
    print("\n--- REGISTRAR CLIENTE ---")
    nombre = leer_texto("Nombre completo: ")
    correo = leer_texto("Correo electrónico: ")
    telefono = leer_texto("Teléfono (7 a 15 dígitos, puede iniciar con +): ")
    cliente = sistema.registrar_cliente(nombre, correo, telefono)
    print("\nCliente registrado correctamente.")
    print(cliente.describir())


def listar_clientes(sistema):
    print("\n--- CLIENTES REGISTRADOS ---")
    if not sistema.clientes:
        print("Todavía no hay clientes registrados.")
        return
    for posicion, cliente in enumerate(sistema.clientes, start=1):
        print(f"{posicion}. {cliente.describir()} | ID: {cliente.id[:8]}")


def crear_servicio(sistema):
    print("\n--- CREAR SERVICIO ---")
    print("1. Reserva de sala")
    print("2. Alquiler de equipo")
    print("3. Asesoría especializada")
    tipo = leer_texto("Selecciona el tipo de servicio: ")

    nombre = leer_texto("Nombre del servicio: ")
    tarifa = leer_numero("Tarifa base en pesos colombianos: ")
    if tarifa <= 0:
        raise ValidacionError("La tarifa debe ser mayor que cero.")

    if tipo == "1":
        capacidad = leer_numero("Capacidad de la sala (personas): ", entero=True)
        servicio = ReservaSala(nombre, tarifa, capacidad)
    elif tipo == "2":
        unidades = leer_numero("Unidades disponibles: ", entero=True)
        servicio = AlquilerEquipo(nombre, tarifa, unidades)
    elif tipo == "3":
        especialidad = leer_texto("Especialidad de la asesoría: ")
        servicio = AsesoriaEspecializada(nombre, tarifa, especialidad)
    else:
        raise ValidacionError("Tipo de servicio no válido. Selecciona 1, 2 o 3.")

    sistema.agregar_servicio(servicio)
    print("\nServicio registrado correctamente.")
    print(servicio.describir())


def listar_servicios(sistema):
    print("\n--- SERVICIOS REGISTRADOS ---")
    if not sistema.servicios:
        print("Todavía no hay servicios registrados.")
        return
    for posicion, servicio in enumerate(sistema.servicios, start=1):
        estado = "Disponible" if servicio.disponible else "No disponible"
        print(f"{posicion}. {servicio.describir()} | {estado} | ID: {servicio.id[:8]}")


def seleccionar_servicio(sistema):
    listar_servicios(sistema)
    if not sistema.servicios:
        raise ValidacionError("Primero debes registrar al menos un servicio.")
    numero = leer_numero("Número del servicio que deseas seleccionar: ", entero=True)
    if numero < 1 or numero > len(sistema.servicios):
        raise ValidacionError("El número de servicio no existe.")
    return sistema.servicios[numero - 1]


def crear_reserva(sistema):
    print("\n--- CREAR RESERVA ---")
    if not sistema.clientes:
        raise ValidacionError("Primero debes registrar un cliente.")
    if not sistema.servicios:
        raise ValidacionError("Primero debes registrar un servicio.")

    listar_clientes(sistema)
    correo = leer_texto("\nEscribe el correo del cliente: ").lower()
    servicio = seleccionar_servicio(sistema)
    duracion = leer_numero("Duración (horas para salas/asesorías o días para equipos): ")
    reserva = sistema.crear_reserva(correo, servicio, duracion)
    print("\nReserva creada con estado PENDIENTE.")
    print(reserva.describir())


def listar_reservas(sistema):
    print("\n--- RESERVAS ---")
    if not sistema.reservas:
        print("Todavía no hay reservas registradas.")
        return
    for posicion, reserva in enumerate(sistema.reservas, start=1):
        print(f"{posicion}. {reserva.describir()}")


def seleccionar_reserva(sistema):
    listar_reservas(sistema)
    if not sistema.reservas:
        raise ValidacionError("No hay reservas para gestionar.")
    numero = leer_numero("Número de la reserva: ", entero=True)
    if numero < 1 or numero > len(sistema.reservas):
        raise ValidacionError("El número de reserva no existe.")
    return sistema.reservas[numero - 1]


def confirmar_reserva(sistema):
    print("\n--- CONFIRMAR RESERVA ---")
    reserva = seleccionar_reserva(sistema)
    impuesto = leer_numero("Impuesto (por ejemplo, 0.19 para 19 %; ENTER no aplica aquí): ")
    descuento = leer_numero("Descuento (por ejemplo, 0.10 para 10 %): ")
    if not 0 <= impuesto <= 1:
        raise ValidacionError("El impuesto debe estar entre 0 y 1.")
    if not 0 <= descuento <= 1:
        raise ValidacionError("El descuento debe estar entre 0 y 1.")
    costo = reserva.confirmar(impuesto, descuento)
    print(f"Reserva confirmada. Total: ${costo:,.2f} COP")


def cancelar_reserva(sistema):
    print("\n--- CANCELAR RESERVA ---")
    reserva = seleccionar_reserva(sistema)
    reserva.cancelar()
    print("Reserva cancelada correctamente.")


def procesar_reserva(sistema):
    print("\n--- PROCESAR RESERVA ---")
    reserva = seleccionar_reserva(sistema)
    reserva.procesar()
    print("Reserva procesada correctamente.")


def cambiar_disponibilidad(sistema):
    print("\n--- CAMBIAR DISPONIBILIDAD DE SERVICIO ---")
    servicio = seleccionar_servicio(sistema)
    print(f"Disponibilidad actual: {'Disponible' if servicio.disponible else 'No disponible'}")
    opcion = leer_texto("Escribe S para disponible o N para no disponible: ").upper()
    if opcion not in {"S", "N"}:
        raise ValidacionError("Opción inválida. Debes escribir S o N.")
    servicio.disponible = (opcion == "S")
    logger.info("Disponibilidad de %s cambiada a %s", servicio.nombre, servicio.disponible)
    print("Disponibilidad actualizada.")


def ejecutar_accion(accion):
    """Captura errores por operación y conserva activo el menú."""
    try:
        accion()
    except SoftwareFJError as error:
        logger.exception("Error controlado durante una operación del menú.")
        print(f"\nNo se pudo completar la operación: {error}")
    except (ValueError, TypeError) as error:
        logger.exception("Dato inválido ingresado por el usuario.")
        print(f"\nDato inválido: {error}")
    except Exception as error:
        logger.exception("Error inesperado; el programa continuará.")
        print(f"\nOcurrió un error inesperado. Se registró en el log: {error}")
    else:
        logger.info("Operación de menú completada.")
    finally:
        print("\nLa aplicación sigue activa.")


def mostrar_menu():
    print("\n" + "=" * 54)
    print("       SOFTWARE FJ - GESTIÓN INTEGRAL")
    print("=" * 54)
    print("1. Registrar cliente")
    print("2. Consultar clientes")
    print("3. Crear servicio")
    print("4. Consultar servicios")
    print("5. Crear reserva")
    print("6. Consultar reservas")
    print("7. Confirmar reserva")
    print("8. Cancelar reserva")
    print("9. Procesar reserva")
    print("10. Cambiar disponibilidad de un servicio")
    print("0. Salir")
    print("=" * 54)


def main():
    sistema = GestorSoftwareFJ()
    acciones = {
        "1": lambda: registrar_cliente(sistema),
        "2": lambda: listar_clientes(sistema),
        "3": lambda: crear_servicio(sistema),
        "4": lambda: listar_servicios(sistema),
        "5": lambda: crear_reserva(sistema),
        "6": lambda: listar_reservas(sistema),
        "7": lambda: confirmar_reserva(sistema),
        "8": lambda: cancelar_reserva(sistema),
        "9": lambda: procesar_reserva(sistema),
        "10": lambda: cambiar_disponibilidad(sistema),
    }

    logger.info("Aplicación Software FJ iniciada.")
    print("Bienvenido a Software FJ. Registra y administra los datos desde el menú.")

    while True:
        mostrar_menu()
        try:
            opcion = input("Selecciona una opción: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nSaliendo de Software FJ.")
            logger.info("Aplicación cerrada por interrupción de entrada.")
            break

        if opcion == "0":
            print("Gracias por utilizar Software FJ.")
            logger.info("Aplicación cerrada por el usuario.")
            break
        accion = acciones.get(opcion)
        if accion is None:
            ejecutar_accion(lambda: (_ for _ in ()).throw(
                ValidacionError("Opción de menú no válida.")
            ))
            continue
        ejecutar_accion(accion)


if __name__ == "__main__":
    try:
        main()
    except Exception:
        logger.exception("Error crítico fuera del ciclo principal.")
        print("Se detectó un error crítico. Consulta logs/software_fj.log.")
    finally:
        logging.shutdown()
