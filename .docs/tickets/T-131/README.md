# T-131 · Bloque A: preparar las decisiones pendientes del operador

| Campo | Valor |
| --- | --- |
| Estado | EN QA |
| Pieza | `.docs/scripts/comprobar_datos_a.py`, `.docs/scripts/borrador_anexo_b.py`, `.docs/diseno/bloque_a/borrador_correccion_anexo_b.md`; pruebas en `bloque_a/11_Ejecutor/tests/test_t131_preparativos.py`. No cambia el ejecutor ni el corpus |
| Planifica · implementa · QA | claude · claude · un revisor nuevo sin contexto |
| Aprobación del operador | 2026-11-15: «me parece genial» (puntos 7 y 8 de la lista de tareas de la noche) |
| Deuda técnica | T-131 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Objetivo

Dejar listo lo que se pueda de dos decisiones del operador, sin tomarlas:

1. **Fuente de datos reales (sin decidir).** El ejecutor ya lee CSV genéricos (HT-01, `ProveedorCSV`). Falta poder saber, antes de un ciclo, si una carpeta sirve: `comprobar_datos_a.py` dice por símbolo del universo si está OK, falta, es inválido (con el motivo de HT-01) o está anticuado para el horizonte pedido (`ps2_antiguedad_maxima_dias`, Anexo A), con su rango de fechas y su mayor hueco.
2. **Nueva entrega del Documento 0.** El operador decidió que manda el código (INC-T114-01). `borrador_anexo_b.py` genera, desde las diferencias congeladas en los goldens, el borrador contrato a contrato de lo que el Anexo B debería decir. No se aplica al corpus.

## Criterios de aceptación (binarios)

1. CA-1: `comprobar_datos_a.py` con los datos de ejemplo da 57 de 57 OK; falta, inválido y anticuado se distinguen; el umbral cambia con el horizonte; admite columnas con alias (`Date`, `Close`).
2. CA-2: `borrador_anexo_b.py --comprobar` coincide; el borrador cubre los 23 contratos con diferencias y no tiene mensajes de jsonschema sin traducir.
3. CA-3: `tests/test_t131_preparativos.py` en verde; gate 12/12.

## Registro

- 2026-11-15 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-15 · EN QA · claude · implementado y probado
