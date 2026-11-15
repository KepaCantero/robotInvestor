# T-132 · Bloque A: bajar la cuota de ruff

| Campo | Valor |
| --- | --- |
| Estado | CERRADO |
| Pieza | bloque_a (11_Ejecutor: `sintesis.py`, `anonimizacion.py`, `herramientas/ht01_datos.py`, `ht01_boveda.py`, `ht04_graficos.py`, `ht05_planificador.py`, `ht06_indice.py`, `ht08_monitor.py`) y `tools/cuotas.txt` |
| Planifica · implementa · QA | claude · claude · un revisor nuevo sin contexto |
| Aprobación del operador | 2026-11-15: «me parece genial» (punto 5 de la lista de tareas de la noche) |
| Deuda técnica | T-132 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Qué se hace

Correcciones automáticas **seguras** de ruff (`ruff check --fix`, sin `--unsafe-fixes`) en ocho ficheros del ejecutor que ningún trabajo en curso toca: anotaciones de tipos al estilo actual (`dict`, `list`, `X | None`), importaciones sin usar u ordenadas y `dt.UTC`. La cuota pasa de 2902 a 2838 (política de cuotas: solo bajan).

No se tocan las cuatro herramientas de `herramientas/referencia/` (son copias idénticas de `bloque_a/10_Herramientas/`, que es corpus congelado) ni los ficheros con trabajo en curso (Motor, `orquestacion.py`, `evaluador.py`, `referencias.py`, `mock_respuestas.py`).

## Criterios de aceptación (binarios)

1. CA-1: ruff desde la raíz da 2838 o menos; `tools/cuotas.txt` dice 2838.
2. CA-2: mypy de A no sube (109); ningún cambio de comportamiento: el diff solo toca anotaciones, importaciones y `dt.timezone.utc` → `dt.UTC`.
3. CA-3: pruebas vecinas (`test_unitarias.py`, `test_integracion.py`, `test_fase3_goldens.py`) en verde; gate 12/12.

## Registro

- 2026-11-15 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-15 · EN QA · claude · 55 correcciones; 150 pruebas vecinas en verde; mypy A 109
- 2026-11-15 · CERRADO · QA r01 APTO (revisor nuevo sin contexto), sin hallazgos
