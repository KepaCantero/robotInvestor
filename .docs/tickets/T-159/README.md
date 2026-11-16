# T-159 · Bloque A, Fase 4: pruebas de los casos «Superada en parte» que solo necesitan una prueba

| Campo | Valor |
| --- | --- |
| Estado | CERRADO (QA r02 APTO) |
| Pieza | bloque_a (solo pruebas: `bloque_a/11_Ejecutor/tests/` y el mapa del plan de pruebas) |
| Planifica · implementa · QA | claude · claude · otro agente o un revisor nuevo sin contexto |
| Aprobación del operador | no necesaria: pruebas y documentación, sin cambio de código del ejecutor, de contrato, de corpus ni de controles (tipo «corrección, pruebas, documentación» de `ri-planificar`) |
| Deuda técnica | T-159 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` (la fila la lleva la sesión coordinadora; este ticket no la toca) |

## Objetivo

Recorrer los 37 casos «Superada en parte» de `docs/evidencias_pruebas_bloque_a.md`, clasificar cada uno (A: el ejecutor ya cumple
la cláusula y solo falta la prueba; B: falta una función del ejecutor; C: necesita el modelo real o tiempo real) y escribir la
prueba de extremo a extremo de cada (A), para que su fila pase a «Superada». Es el punto 16 del plan de la noche
(`.docs/tickets/_relevo/plan_noche_bloque_a_2026-11-15.md`, apartado 3).

## Alcance

- Entra:
  - `bloque_a/11_Ejecutor/tests/test_t159_extremo_a_extremo.py` (nuevo): una prueba por caso (A), que cita su PB-xx, con el
    cliente simulado y los pasos del plan; más la parte de PB-52 que el ejecutor sí cumple.
  - `bloque_a/11_Ejecutor/tests/mapa_plan_pruebas.json`: las pruebas nuevas, las filas (A) en AUTOMATICA y el motivo de los (B).
  - `bloque_a/11_Ejecutor/tests/test_fase4_mapa.py`: un caso parametrizado usaba PB-02 como ejemplo de fila PARCIAL; pasa a PB-08,
    que sigue PARCIAL (la comprobación es la misma).
  - `docs/evidencias_pruebas_bloque_a.md`: regenerado con `.docs/scripts/evidencias_plan_a.py --ejecutar` (no se edita a mano).
  - `docs/incidencias.md`: INC-T159-01 con los (B) nuevos, para un ticket nuevo.
  - Este ticket: `README.md`, `analisis-tecnico.md` (tabla de los 37) y `pruebas.md`.
- No entra: código del ejecutor (si una prueba lo necesitara, el caso es B); PB-48 (T-158); los casos de la lista de funciones del
  plan de la noche (apartado 2), que son B por definición; el Documento 0, los goldens, `tests/test_fase3_goldens.py`, el corpus
  congelado, otros bloques y la fila T-159 de la deuda.

## Diseño

- Contratos y estado persistido: no cambian (solo pruebas).
- La siembra de cada prueba cambia solo lo que el plan prepara: lo que devuelve un agente simulado (`mock_respuestas`), la serie
  de un proveedor de pruebas, la madurez de una ficha del Catálogo leída por el Motor o la función que construye el paquete de
  síntesis (para sembrar la cifra sin artefacto de PB-30). Los umbrales se leen de la configuración (`config_pruebas`, F10).
- Sin red, sin clave y con la hora fija (`AS_OF` y fechas derivadas).

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| Una siembra que fuerce el resultado | La prueba no comprueba el ejecutor | Solo se siembra la preparación del plan; las afirmaciones son sobre F3, F4, HA, RC y los entregables que escribe el ejecutor |
| Datos sintéticos que cambien | Una prueba deja de encontrar su caso | Cada prueba comprueba primero que la siembra ocurrió (p. ej., que hubo candidatas de cada papel, que salió la recomendación) |
| Una prueba que descubra que el código no cumple | Tentación de debilitarla | No se debilita: el caso pasa a B (PB-52) |

## Criterios de aceptación (binarios)

1. CA-1: los 37 casos clasificados en A, B o C con su motivo en `analisis-tecnico.md`.
2. CA-2: cada caso (A) tiene al menos una prueba nueva en `tests/test_t159_*.py` que cita su PB-xx y pasa.
3. CA-3: el mapa cita las pruebas nuevas, las filas (A) están en AUTOMATICA y `evidencias_plan_a.py` no da problemas.
4. CA-4: `docs/evidencias_pruebas_bloque_a.md` regenerado con `--ejecutar`, con todas las pruebas citadas superadas.
5. CA-5: los (B) nuevos están en `docs/incidencias.md` (INC-T159-01) para un ticket nuevo.
6. CA-6: suite de A sin bajar de 607, gates ligeros en verde, ruff ≤ 2831 y mypy de A ≤ 109.

## Plan de pruebas

| Prueba | Tipo | Criterio |
| --- | --- | --- |
| `tests/test_t159_extremo_a_extremo.py` (10 pruebas) | integración (extremo a extremo con el cliente simulado) y fallo cerrado (PB-52) | CA-2 |
| `tests/test_fase4_mapa.py` | contrato del mapa | CA-3 |
| `.docs/scripts/evidencias_plan_a.py` y `--ejecutar` | evidencias | CA-3, CA-4 |
| `.docs/scripts/pruebas_scripts.sh` | scripts | CA-3 |
| Suite completa de A, `refs_vivas.py`, `secrets_scan.py`, `nfc_check.py`, `corpus_integridad.py`, ruff y mypy | regresión | CA-6 |

## Scripts

`.docs/scripts/nuevo_ticket.sh` (este ticket) y `.docs/scripts/evidencias_plan_a.py` (comprobación y `--ejecutar`). No se crea
ninguno nuevo: la actualización del mapa fue una edición única.

## Registro

- 2026-11-16 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-16 · PLANIFICADO · claude · plan y criterios
- 2026-11-16 · EN CURSO · claude · clasificación y pruebas
- 2026-11-16 · EN QA · claude · 8 casos (A) pasan a «Superada»; 27 (B) y 2 (C) siguen «en parte» con su motivo
- 2026-11-16 · EN QA r02 · claude (coordinadora) · QA r01 NO APTO; PB-47 vuelve a «en parte» (falta G3-MET-13) y PB-25 y PB-46 pasan a B: 7 casos (A) a «Superada», 30 (B)
- 2026-11-16 · CERRADO · QA r02 APTO; R02-H-06 y R02-H-07 (bajos, de texto) resueltos al cerrar
