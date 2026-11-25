# T-201 · Análisis técnico

## Causa raíz o motivo

La cuota de mypy de A (`tools/cuotas.txt`, `mypy_bloque_a=102`) cuenta las líneas que da `mypy --ignore-missing-imports --no-error-summary bloque_a/11_Ejecutor/bloque_a`, que es la orden del gate. En `origin/develop` (7f92064a) esas 102 líneas son:

- **61 de `herramientas/referencia/`**: 50 errores (HT-09 24, HT-02 13, HT-03 13) y 11 notas; con `mypy bloque_a`, sin `--ignore-missing-imports`, son 53 errores, por los 3 `import-not-found` de los imports entre copias (r02, H-04). Son copias literales del corpus congelado y no se tocan: decisión del operador del 16-11-2026 (`sistema_global/seguimiento/Decisiones_del_operador_Bloque_A.md`, §1, fila G3-MET-13). Quedan como deuda del corpus hasta que una entrega del corpus las corrija.
- **19 `attr-defined`** en los usos de los envoltorios: `ht09.validar`, `ht03.evaluar_opcion`, `ht02.leer_fichas`, `ht07.analizar`… en `orquestacion.py`, `sintesis.py`, `redaccion.py`, `referencias.py`, `cli.py` y `seguimiento.py`. Los envoltorios importan la copia por `sys.path` (`import ht09_validador_g3`), y mypy no la encuentra con ese nombre. Con `--ignore-missing-imports` el módulo pasa a `Any`, pero `from ht09_validador_g3 import *` no trae ningún nombre, así que cada atributo del envoltorio «no existe». Sin esa opción salen, además, 4 `import-not-found` (uno por envoltorio).
- **16 errores de tipos** en seis ficheros que no son de otras ramas, y **6 de `orquestacion.py`**, que está en la PR 3 de Astra y en T-196 y no se toca.

## Evidencia

- Antes: 102 líneas (orden del gate); `mypy bloque_a` desde `bloque_a/11_Ejecutor`: 147 errores en 42 ficheros.
- Después: 67 líneas (61 de `referencia/` y 6 de `orquestacion.py`); `mypy bloque_a`: 109 errores en 37 ficheros. De ellos, 49 son `import-untyped` (T-202), 53 están en `referencia/`, 6 en `orquestacion.py` y 1 es el `import-not-found` de `yfinance`.
- Ningún error nuevo en ningún fichero (comparadas las dos salidas línea a línea).

## Implementación

- **Archivos cambiados y por qué** (todos en `bloque_a/11_Ejecutor/`):
  - `bloque_a/herramientas/ht02.py`, `ht03.py`, `ht07.py` y `ht09.py`: `if TYPE_CHECKING:` importa la copia por su ruta de paquete (`from .referencia.<modulo> import *`, el mismo fichero); `else:` importa como antes, por `sys.path`. En ejecución `TYPE_CHECKING` es falso y nada cambia. Se quitan los `# noqa: E402` y `F401,F403`, que ruff ya marcaba como inútiles (RUF100), y el `# noqa: I001` de HT-09, cuyo motivo («DIR_REFERENCIA va antes que la referencia») desaparece porque el import de la copia ya no está en el bloque de imports. Corrige 23 errores de `mypy bloque_a` (4 `import-not-found` y 19 `attr-defined`), 21 de ellos en ficheros que no se tocan.
  - `bloque_a/seguimiento.py`: `-> tuple[str, str]` en lugar de `-> (str, str)` (error de sintaxis de la anotación y su nota); `_cambio` con `seg_id` None; `b_agente(clase: str | None)`; `_estado_hito` sacado de la comprensión de `_revision`.
  - `bloque_a/configuracion.py`: `ruta` sin la clave lanza el mismo `TypeError` que `Path(None)`, con un mensaje que nombra la clave.
  - `bloque_a/backtest.py`: `metricas: dict` (la estructura JSON del resultado; mypy la infería como `dict[str, object]` y no dejaba indexarla).
  - `bloque_a/motor/servicio.py`: `ent: dict[str, dict]`; `ALTERNATIVAS.get(ficha) if ficha is not None else None`; la entrada del CACHE_HIT se llama `hit` y no `e`, que ya era el nombre de una excepción en el mismo método.
  - `bloque_a/motor/operaciones.py`: `mapa: dict[int, int]`; `posicion_historica` admite `np.ndarray` (ya lo recibía de `servicio.py` y de `diferencial_rentabilidades`); en `diferencial_rentabilidades`, el diferencial escalado en una variable y `out: dict[str, float | str]`.
  - `bloque_a/motor/evaluacion.py`: en `acierto_direccional`, el array es `arr` y no reutiliza el parámetro `o: Sequence[int]`.
  - `tests/test_t201_cuotas.py` (nuevo, 35 pruebas).
  - `tools/cuotas.txt`: `ruff=2797` (antes 2806) y `mypy_bloque_a=67` (antes 102).
  - `docs/incidencias.md` (INC-T201-01), la deuda técnica (fila T-201) y este ticket.
- **Decisiones y desviaciones:**
  - El objetivo cambió: ver el README («Cambio de objetivo»).
  - Ninguna anotación usa `cast` ni un `Any` nuevo. Las de `metricas: dict` y `ent: dict[str, dict]` son el tipo que ya devuelven las funciones del paquete (`-> dict`) y no tapan ningún fallo: el error era de inferencia, no de datos.
  - Ningún error resultó ser un fallo real que se pudiera alcanzar:
    - el `None` de `_cambio` y el de `servicio.py` ya terminaban en un `KeyError` o en un rechazo; el de `servicio.py`, además, lo para antes la comprobación de forma;
    - el de `b_agente` termina en el AG-03 por defecto;
    - el de `ruta` terminaba en un `TypeError` críptico, y es el único caso en que cambia el mensaje.
  - El defecto silencioso de `b_agente` (una clase ausente o desconocida va al AG-03 sin aviso) se conserva y se anota en INC-T201-01 como observación. Cambiarlo cambiaría el comportamiento y queda fuera de un ticket de cuotas.
- **Límites conocidos:**
  - Los 3 `import-not-found` de dentro de las copias y sus 50 errores de tipos siguen ahí: son corpus.
  - Los envoltorios sí se pueden arreglar sin tocar `referencia/` ni la configuración, y se ha hecho. Lo que no se puede es que mypy siga, dentro de las copias, sus imports de primer nivel.
  - El `import-not-found` de `yfinance` no lo cuenta el gate; desaparecería instalando el extra `yahoo`, lo que cambia el entorno fijado y no le toca a este ticket.

## Cómo probarlo

Desde la raíz de la copia:

```bash
.venv/bin/mypy --ignore-missing-imports --no-error-summary bloque_a/11_Ejecutor/bloque_a | wc -l     # 67
(cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t201_cuotas.py)
.docs/tickets/T-201/equivalencia.sh .        # VEREDICTO: EQUIVALENTE (unos 75 s; carpeta temporal fuera del repo)
./tools/check_all.sh
```

## Ronda r02 (QA r01 NO APTO, H-01 a H-04)

| Hallazgo | Corrección | Prueba |
| --- | --- | --- |
| H-01 (media): `comparar.py` enmascaraba campos de dominio e instantes | `LATENCIAS` solo con `latencia_s` y `tiempo_respuesta_s`, por su nombre exacto; fuera `INSTANTE`. Se conservan rutas, `LATENCIA_CSV` y `RESUMEN`. No hizo falta normalizar ningún instante: con la comparación estricta la equivalencia sigue dando EQUIVALENTE (las dos ejecuciones corren a la vez). `equivalencia.sh` lanza después el testigo `sensibilidad.py` y termina con 1 si encuentra un punto ciego | `sensibilidad.py`: «puntos ciegos: ninguno» (9 cambios DISTINTO, 3 latencias EQUIVALENTE); `revisores/r02_sensibilidad_equivalencia.py`: «puntos ciegos: ninguno»; `equivalencia.sh`: EQUIVALENTE |
| H-02 (baja): M16 vivía | caso `acierto_direccional([1.7, 1.7, 0.2])` → `n` 3, `aciertos` 2 en `test_acierto_direccional_con_lista_y_con_array` | `revisores/r04_mutantes.py`: M16 muerto |
| H-03 (baja): M01 vivía; el mensaje decía «no está» con la clave a null | mensaje «rutas.<clave> no está en la configuración o es null»; tres pruebas: `""` → la raíz del paquete, `0` → el error de `Path` (sin el mensaje nuevo), `None` → el mensaje nuevo (texto completo) | `revisores/r04_mutantes.py`: M01 muerto con `tests/test_t201_cuotas.py` |
| H-04 (baja): cifras de `referencia/` con dos medidas mezcladas | README, INC-T201-01, fila de la deuda y este análisis: 61 líneas del gate, 50 errores (HT-09 24, HT-02 13, HT-03 13) y 11 notas; 53 con `mypy bloque_a` por los 3 `import-not-found` | las dos órdenes y su resultado en `pruebas.md` (CA-1) |

El defecto de `b_agente` no se toca: va a un ticket propio (orden del coordinador del 25-11-2026; propuesta en INC-T201-01 y en el `qa.md`).
