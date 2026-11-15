# T-134 · Bloque A: hallazgos de la QA r03 de T-125

| Campo | Valor |
| --- | --- |
| Estado | CERRADO |
| Pieza | bloque_a (11_Ejecutor: `bloque_a/evaluador.py`, `bloque_a/orquestacion.py`) |
| Planifica · implementa · QA | claude · claude · un revisor nuevo sin contexto |
| Aprobación del operador | 2026-11-14: «quiero que por tu cuenta vayas completando los tickets que quedan abiertos»; 2026-11-15: los tickets nuevos, con QA APTO |
| Deuda técnica | T-134 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Qué se corrige

| Hallazgo | Corrección |
| --- | --- |
| H-14 (media): un entero de 400 cifras en el umbral, el rango o la probabilidad tumbaba el ciclo con `OverflowError` | `_finito`: el desbordamiento cuenta como no finito; el bloque no se registra |
| H-15 (baja): el mismo número en un F2 manipulado hacía perder la FUE- de todas las fuentes | El Evaluador usa la misma comprobación y descarta solo ese pronóstico |
| H-16 (baja): cifras no ASCII y zona sin hora en las fechas | `RE_FECHA_ISO` solo con `[0-9]` y la zona solo detrás de una hora |
| H-17 (baja): `fiabilidad_fuentes.variables_nivel` sin validar | `variables_nivel(cfg)`: lista no vacía de textos; si no, `ValueError` al crear el Evaluador |
| H-18 (baja): dos conexiones del ciclo sin prueba (M12 y M14) | Pruebas de que el C5 pasa su `run_id` y de que el alta en F2 usa la lista de la configuración |

## Criterios de aceptación (binarios)

1. CA-1: `tests/test_t134_r03_t125.py` y las pruebas de T-125 en verde.
2. CA-2: los scripts del revisor de la r03 (`.docs/tickets/T-125/revisores/r03_02_fechas_variables_y_numeros.py`, `r03_03_ciclo_tras_desbordamiento.py`) ya no reproducen H-14 a H-17; con `r03_04_mutantes.py`, M12 y M14 mueren.
3. CA-3: gate 12/12.

## Registro

- 2026-11-15 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-15 · EN QA · claude · implementado y probado
- 2026-11-15 · CERRADO · QA r01 APTO (revisor nuevo sin contexto); H-19 (baja) en T-137
