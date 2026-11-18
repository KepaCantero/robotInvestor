# T-176 · Evaluador: recalibración del umbral E y P-05 fuera de banda a la cola de HA (PB-36) y sección Novedades de F6 (PB-33)

| Campo | Valor |
| --- | --- |
| Estado | CERRADO (17-11-2026, QA r02 APTO tras la ronda de cierre) |
| Pieza | Bloque A (Evaluador, AG-20; elevación por CT-19 en `orquestacion.py`) |
| Planifica · implementa · QA | claude · claude · astra (o un revisor nuevo de Claude que no implementó) |
| Aprobación del operador | no necesaria (pruebas y corrección de huecos del plan; las decisiones del diseño que faltan, `[PROPUESTO]` por la regla del 13-11-2026) |
| Deuda técnica | T-176 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Objetivo

Que PB-36 y PB-33 del Plan de pruebas V3.0 pasen de «Superada en parte» a «Superada»: el Evaluador recalibra también el umbral E (P-09) en la revisión trimestral y, fuera de banda o sin banda (P-05, PENDIENTE_OPERADOR), su P3-EVAL- llega por CT-19 al Orquestador y queda en la cola de tipo 3 de HA (PENDING_OPERATOR) con F10 intacto; y F6 publica su sección semanal «Novedades».

## Alcance

- Entra:
  - **PB-36.** Función general del Evaluador para proponer el ajuste de un parámetro CALIBRABLE de F10 (`proponer_ajuste`): dentro de banda, AJU- PROPUESTO (no toca F10); fuera de banda (`fuera de banda`) o con banda PENDIENTE_OPERADOR (`sin banda`), P3-EVAL- en F6 con evidencia, impacto, pruebas de regresión y plan de reversión (esquema F6 4.7). Bandas de P-09 del Anexo A (±5 por trimestre, ±10 en total) a la configuración; los calibrables sin banda en el Documento 0 (esquema F10 4.3, P-05 entre ellos) son PENDIENTE_OPERADOR: cualquier cambio es tipo 3 (regla 2 de F10, R23).
  - Revisión trimestral (`RTR-AAAA-Tn` en F6, el primer C5 de cada trimestre): evidencia del umbral E óptimo con los PRG resueltos admisibles que llevan la E de su opción (índice de Youden), y propuesta por `proponer_ajuste`. Los estimadores de la revisión están en una tabla (`ESTIMADORES_TRIMESTRALES`); hoy solo P-09 · E.
  - Elevación: cada P3-EVAL- de F6 sin `elevada_via` sale por CT-19 (AG-20 → AG-18), el Orquestador la registra en HA (`tipo_entrada` P3, `origen` EVAL, `estado` PENDING_OPERATOR) y la P3- de F6 anota `elevada_via` (msg_id). Idempotente. Vale también para las P3- ya existentes (P-11 fuera de banda, H5 «Limitado» → «No»).
  - **PB-33.** Sección «Novedades» de F6 (`NOV-AAAA-Www`, una por semana ISO): altas (CERT-), revocaciones (CERT_REVOCACION), ajustes (AJU- y P3-EVAL-) y lecciones nuevas (LEC-) por identificador, desde la anterior. Se publica al final de C5 si hay algo nuevo; un segundo C5 de la misma semana la rehace entera.
  - Pruebas del criterio completo de los dos casos, mapa del plan, evidencias regeneradas, incidencia INC-T176-01.
- No entra:
  - Aplicar un cambio de P-09 en producción ni su evaluación sombra en HT-03 (la sombra de HT-03 solo compara pesos de RK; dentro de banda el AJU- de P-09 queda PROPUESTO).
  - Estimador para P-05 (ni el Documento 0 ni el plan dicen cómo se mide un número óptimo de candidatas); la función acepta su evidencia.
  - Leer «Novedades» en el contexto de los agentes por HT-06 (las lecciones y los certificados ya llegan por su vía; cambiar el contexto mueve tokens de todos los agentes).
  - La decisión del operador sobre la P3- (APROBADA/RECHAZADA/APLICADA): sin lector en el ejecutor hoy.
  - Corpus congelado, esquemas de `06_Plantillas_entregables`, otros bloques.

## Diseño

- Contratos: CT-19 (AG-20 → AG-18 ya permitido en `contratos.py`; la mensajería no exige campos). Cuerpo: `tipo` PROPUESTA_TIPO_3 y `p3` con los campos de F6 4.7. Ningún golden cambia (no se toca la mensajería ni ningún esquema).
- Estado persistido: entradas nuevas en F6 (`RTR`, `NOV`) y en HA (`P3` de origen EVAL); campo nuevo `elevada_via` en P3- de F6 (ya en el esquema 4.7). Append-only; sin migración (los lectores ignoran tipos que no conocen).
- Números: bandas de P-09 (Anexo A: «±5/trimestre; ±10 total») → `evaluacion.bandas_f10.P-09`; P-05 → `evaluacion.bandas_f10.P-05: {estado: PENDIENTE_OPERADOR}` (esquema F10 4.3). Muestra mínima: `evaluacion.min_calibrar` (30). Valor vigente de P-05: F10 si está, si no `seleccion.max_candidatas`. Ningún número nuevo en código.
- Cómo falla cerrado: un parámetro CALIBRABLE sin banda en la configuración es PENDIENTE_OPERADOR (tipo 3); uno no CALIBRABLE se rechaza (ValueError). Sin muestra suficiente, la revisión no propone nada y lo dice en su RTR-. La elevación que falla no tumba C5 (incidencia) y se reintenta en el siguiente ciclo (la P3- sigue sin `elevada_via`).
- `[PROPUESTO]` (INC-T176-01): estimador de Youden para el umbral E; AJU- de P-09 dentro de banda como PROPUESTO, no EN_SOMBRA; Novedades solo si hay algo nuevo; periodicidad trimestral de la revisión de P-09 con registro RTR-; P3- de F6 sigue ENVIADA (estado de F6 4.7) mientras HA la lleva PENDING_OPERATOR.

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| La revisión trimestral escribe en F6 en todos los ciclos mock | Pruebas que cuentan entradas de F6 cambian | Suite completa de A; las entradas nuevas tienen tipos propios |
| `ajuste_en_sombra` cogería un AJU- de P-09 | HT-03 recibiría umbrales como pesos de RK | El AJU- de P-09 nunca es EN_SOMBRA; `ajuste_en_sombra` filtra P-11 |
| Choque con T-177/T-178 en ficheros compartidos | Conflictos al integrar | Cambios acotados al Evaluador, un método nuevo en `orquestacion.py` y filas propias del mapa |
| No romper PB-33 de T-173 | Regresión | Las tres pruebas `test_pb33_…` siguen en el mapa y pasan |

## Criterios de aceptación (binarios)

1. CA-1: con evidencia de que el umbral E óptimo es 48 (−12 frente a 60), la revisión trimestral deja una P3-EVAL- `fuera de banda` con evidencia, impacto, pruebas de regresión y plan de reversión, y ningún cambio en F10 (P-09 igual, sin CFG-).
2. CA-2: con P-05 (banda PENDIENTE_OPERADOR) cualquier propuesta sale P3-EVAL- `sin banda`; F10 intacto en P-05.
3. CA-3: tras el ciclo, cada P3-EVAL- tiene su CT-19 al Orquestador (AG-18), su `elevada_via` en F6 y su entrada P3 en HA PENDING_OPERATOR; un segundo ciclo no la duplica.
4. CA-4: dentro de banda (p. ej. E óptimo 57) sale un AJU- PROPUESTO de P-09 con sus bandas y sin tocar F10; un parámetro no CALIBRABLE se rechaza; un CALIBRABLE sin banda en la configuración es tipo 3.
5. CA-5: la revisión de P-09 es una por trimestre (RTR-); sin muestra suficiente no propone nada.
6. CA-6: tras la revocación de PB-33, F6 tiene la NOV- de la semana con la revocación y la lección de sobreconfianza por identificador; la de la semana siguiente solo lleva lo nuevo; las tres pruebas `test_pb33_…` de T-173 siguen pasando.
7. CA-7: PB-36 y PB-33 «Superada» en `docs/evidencias_pruebas_bloque_a.md`; suite de A ≥ línea base y sin fallos; ruff ≤ 2813, mypy A ≤ 102; mutantes propios muertos.

## Plan de pruebas

| Prueba | Tipo | Criterio |
| --- | --- | --- |
| `test_t176_pb36_pb33.py::test_pb36_umbral_e_y_p05_fuera_de_banda_a_la_cola_de_ha_con_f10_intacto` (ciclo mock) | integración | CA-1, CA-2, CA-3 |
| `test_t176_pb36_pb33.py::test_pb36_un_segundo_ciclo_no_duplica_la_elevacion_ni_la_revision` | regresión | CA-3, CA-5 |
| `test_t176_pb36_pb33.py::test_p3_de_p11_tambien_se_eleva` | regresión | CA-3 |
| `test_t176_pb36_pb33.py::test_proponer_ajuste_banda_trimestral_de_p09_en_el_limite` (55, 65, 54, 66) | límite | CA-4 |
| `test_t176_pb36_pb33.py::test_proponer_ajuste_dentro_de_banda_suma_lo_del_trimestre_y_el_total_frente_al_inicial` | nominal/límite | CA-4 |
| `test_t176_pb36_pb33.py::test_proponer_ajuste_rechaza_no_calibrable_y_sin_banda_es_tipo_3` | fallo cerrado | CA-2, CA-4 |
| `test_t176_pb36_pb33.py::test_evidencia_umbral_e_youden_y_muestra_insuficiente` | nominal/límite | CA-5 |
| `test_t176_pb36_pb33.py::test_evidencia_umbral_e_empate_elige_el_mas_cercano_al_vigente_y_j_nulo_no_propone` | límite | CA-5 |
| `test_t176_pb36_pb33.py::test_pb33_novedades_de_la_semana_con_la_revocacion_y_la_leccion` (ciclo mock) | integración | CA-6 |
| `test_t176_pb36_pb33.py::test_novedades_semana_siguiente_solo_lo_nuevo_y_misma_semana_rehace` | nominal | CA-6 |
| Mutantes propios (`.docs/tickets/T-176/mutantes.py`) | mutación | CA-7 |
| Suite de A completa, gates | regresión | CA-7 |

## Scripts

`.docs/scripts/evidencias_plan_a.py` (mapa y evidencias), `.docs/scripts/gate.sh`, `.docs/tickets/T-176/mutantes.py` (nuevo, del ticket).

## Registro

- 2026-11-17 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-17 · PLANIFICADO · claude · plan, criterios y pruebas
- 2026-11-17 · EN CURSO · claude · implementación (`evaluador.py`, `orquestacion.py`, `por_defecto.yaml`) y pruebas
- 2026-11-17 · EN QA (r01) · claude · pruebas, mutantes 28/28, evidencias y gate 12/12; pendiente QA de otro agente
- 2026-11-17 · QA r01 NO APTO · revisor · H-01 (media) y H-02 a H-06 (bajas), en `qa.md`
- 2026-11-17 · EN QA (r02: QA r01 NO APTO) · claude · H-01 a H-06 corregidos con su regresión; `revisores/r01_ataques.py` 17/17; mutantes 37/37
- 2026-11-18 · QA r02 · revisor · un hallazgo bajo, H-07 (`recalibrar` sin transacción)
- 2026-11-18 · EN QA (ronda de cierre de la QA r02) · claude · H-07 corregido con su regresión y M38; r01_ataques 17/17, r02_ataques 7/7
