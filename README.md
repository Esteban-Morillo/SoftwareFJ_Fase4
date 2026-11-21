# Software FJ — Sistema Integral de Gestión

## Requisitos
- Python 3.10 o superior.
- No requiere paquetes externos ni base de datos.

## Ejecución
Abre una terminal en esta carpeta y ejecuta:

```bash
python main.py
```

El programa **no registra datos automáticamente**. Presenta un menú interactivo y espera que el usuario seleccione las operaciones.

## Opciones del menú
1. Registrar cliente.
2. Consultar clientes.
3. Crear servicio (sala, alquiler de equipo o asesoría).
4. Consultar servicios.
5. Crear reserva para un cliente y un servicio registrados.
6. Consultar reservas.
7. Confirmar una reserva y calcular su costo.
8. Cancelar una reserva.
9. Procesar una reserva confirmada.
10. Cambiar la disponibilidad de un servicio.
0. Salir.

Los datos se conservan en listas mientras la aplicación permanece abierta. Al cerrar el programa, los objetos en memoria se pierden; los eventos y errores quedan registrados en `logs/software_fj.log`.

## Arquitectura
- `Entidad`: clase abstracta base.
- `Cliente`: valida y encapsula nombre, correo y teléfono.
- `Servicio`: clase abstracta con cálculo polimórfico de costos.
- `ReservaSala`, `AlquilerEquipo` y `AsesoriaEspecializada`: servicios derivados.
- `Reserva`: administra estados pendiente, confirmada, cancelada y procesada.
- `GestorSoftwareFJ`: almacena objetos en listas.
- `excepciones.py`: excepciones personalizadas.
- `main.py`: menú interactivo.

## Principios de POO
- **Abstracción:** `Entidad` y `Servicio` son clases abstractas.
- **Herencia:** clientes y servicios especializados derivan de sus clases base.
- **Polimorfismo:** los servicios sobrescriben `calcular_costo`, `describir` y `validar_parametros`.
- **Encapsulación:** atributos internos y propiedades validadas.
- **Variantes de cálculo:** `calcular_costo(duracion, impuesto=0.19, descuento=0)` acepta parámetros opcionales. Python no implementa sobrecarga tradicional por firma como Java; esta solución ofrece variantes de llamada mediante argumentos opcionales.

## Manejo de errores
Se implementan excepciones personalizadas, bloques `try/except/else/finally` y encadenamiento con `raise ... from exc`. Los errores de una operación se registran y el menú continúa activo.

## Almacenamiento
No se utiliza base de datos. Clientes, servicios y reservas permanecen en memoria durante la ejecución. El archivo de logs guarda eventos y errores.
