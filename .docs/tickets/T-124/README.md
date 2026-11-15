# T-124 · Bloque A: hallazgos abiertos de la QA r02 de T-114 (goldens de contratos)

| Campo | Valor |
| --- | --- |
| Estado | CERRADO |
| Pieza | bloque_a (11_Ejecutor: `tests/goldens_ct.py` y `tests/goldens/`; no cambia código de producción) |
| Planifica · implementa · QA | claude · claude · un revisor nuevo sin contexto |
| Aprobación del operador | 2026-11-14: «quiero que por tu cuenta vayas completando los tickets que quedan abiertos» |
| Deuda técnica | T-124 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Qué se corrige

| Hallazgo | Corrección |
| --- | --- |
| H-07 (media): 38 mensajes de los flujos de petición ad hoc, consulta que escala e informe de aprendizaje se descartaban del golden de formas | Esos tres flujos se guardan enteros (`FLUJOS`): ya se ven el CT-05 AD_HOC con su pregunta, el `foco` de CT-06 y `historial_aciertos.por_horizonte` de CT-15 |
| H-08 (baja): una ruta genérica («<clase>») contaba una vez por clave real y salía «a veces» | Cuenta una vez por objeto (`rutas`) |
| H-09 (baja): siete mutantes de la mensajería vivos | Ocho casos nuevos en `bateria_mensajes.json`: dato protegido en `limitaciones`, `autoevaluacion`, `presupuesto` y `consumo`; `run_id` vacío; `horizontes` como texto vacío; `resumen` como lista; estado común contradictorio con el propio |
| H-10 (baja): INC-T114-01 no recogía que la mensajería no aplica las listas cerradas del Anexo B ni la condición de `contenido` de CT-23 | Añadido a INC-T114-01 |
| H-11 (baja): CA-1 y CA-2 de T-114 con cifras viejas | Nota en el registro de T-114 |

Re-congelado con su motivo: `aceptaciones_rechazos.json`, `formas_flujos_mock.json` y `huellas.json` (línea en `tests/goldens/REGISTRO.md`).

## Criterios de aceptación (binarios)

1. CA-1: `r02_01_mutantes_mensajeria_nuevos.py --confirmar` del revisor: ningún mutante vivo (antes, siete).
2. CA-2: `r02_02_formas_y_flujos.py --copia`: K01, K02 y K03 detectados.
3. CA-3: `python tests/goldens_ct.py` coincide; `test_fase3_goldens.py` en verde; no cambia código de producción.

## Registro

- 2026-11-14 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-14 · EN QA · claude · `r02_01 --confirmar`: los 20 mutantes de la mensajería detectados, vivos ninguno
- 2026-11-14 · EN QA · claude · `r02_02_formas_y_flujos.py --copia`: K01, K02 y K03 detectados (CA-2); goldens coinciden con T-125 integrado (CA-3)
- 2026-11-15 · CERRADO · QA r01 APTO (revisor nuevo sin contexto); hallazgos bajos (H-01 a H-03) resueltos en T-130
