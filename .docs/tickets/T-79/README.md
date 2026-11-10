# T-79 · Integración del kit 2 de GLM en el marco común de C (V0.67)

| Campo | Valor |
| --- | --- |
| Estado | CERRADO (QA r01 APTO, 10-11-2026) |
| Pieza | sistema_global/marco_comun_c |
| Planifica · implementa · QA | claude · GLM (V0.60 a V0.66) y claude (integración y correcciones) · un revisor nuevo sin contexto |
| Aprobación del operador | 2026-11-10: «tengo los marcos comunes de C desde el V 0.60 hasta el V 0.66 […] Te paso los resultados para que los revises y mejores» |
| Deuda técnica | T-79 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Objetivo

Llevar al repositorio las siete piezas del kit 2 de GLM como V0.67, después de revisarlas y corregirlas, y completar su pasada de coherencia con la Constitución V0.6.

## Alcance

- **Entra:**
  - comprobar que la V0.66 contiene las anteriores;
  - verificarla desde limpio;
  - hacer la QA de Claude, con atención a V0.63 y V0.64, que no tenían revisión;
  - corregir lo encontrado, con su prueba;
  - completar la pasada de coherencia contra la V0.6;
  - renumerar la deuda de GLM.
- **No entra:** implementar lo que la pasada marca como pendiente (de T-80 a T-84). Cada cosa irá en su versión.

## Diseño

Detalle en el Documento 0, `sistema_global/documentos_0/V0.67_Integracion_del_kit_2_de_GLM.md`.
- **Estado persistido:** no cambia.
- **Esquema del código:** pasa a V0.67, con la migración MIG-005, sin cambios en el estado. El motivo es un parámetro nuevo en `parametros.py`.
- **Números:** `n_lineas_diario_ambar` vale 1000 `[PROPUESTO]`. Ya era el valor por defecto de la V0.64; ahora vive en `parametros.py`.

## Criterios de aceptación

1. CA-1: la V0.66 contiene las seis versiones anteriores, sin pérdidas ni vueltas atrás.
2. CA-2: las 56 baterías pasan en el repositorio (`.docs/scripts/pruebas_marco.sh`) y el gate da 12/12.
3. CA-3: cada corrección tiene una prueba que falla con la V0.66.
4. CA-4: la deuda de GLM está en la deuda técnica con números que no chocan, y lo que la pasada contra la V0.6 marca como pendiente tiene su fila.

## Registro

- 2026-11-10 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-10 · EN QA · V0.67 integrada (G-01 a G-06 en el Documento 0); 56 baterías en verde
- 2026-11-10 · CERRADO · QA r01 APTO; H-01 a H-10 corregidos o en la deuda (T-72, T-85)
