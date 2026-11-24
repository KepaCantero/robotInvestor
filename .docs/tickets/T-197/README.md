# T-197 · Bloque A: PB-09, cambio de periodicidad por el Broker (P-01 completo y disparo del C1 por HT-05)

| Campo | Valor |
| --- | --- |
| Estado | CERRADO (24-11-2026, QA r02 APTO y dos rondas de cierre verificadas, sin hallazgos abiertos) |
| Pieza | bloque_a (ejecutor): `bloque_a/11_Ejecutor/bloque_a/herramientas/ht05_planificador.py`, `bloque_a/planificacion_c1.py` (nuevo), la parte P-01 del CT-04 en `orquestacion.py`, la orden `planificar` de `cli.py` |
| Planifica · implementa · QA | claude · claude · otro agente |
| Aprobación del operador | Encargo de la sesión coordinadora (24-11-2026); decisiones por defecto del agente (`compartida/2026-11-13_decide-el-agente-por-defecto`) |
| Deuda técnica | T-197 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Objetivo

Cerrar el hueco de PB-09 «Superada en parte» (INC-T159-01): el P-01 que escribe el CT-04 guarda la hora de entrega y pierde la de la ejecución, y nada llama a HT-05 con el P-01 de F10, así que el siguiente C1 no se dispara en la fecha nueva. Además, probar que ningún otro parámetro cambia.

## Fuentes

- Plan de pruebas V3.0, PB-09: CT-04 con periodicidad QUINCENAL y entrega MIE 08:00; RET- `APLICADA`, CFG- de P-01 escrito por AG-01 con fecha de efecto, HT-05 reprograma, `methodology_version` sin cambio, el ciclo en curso termina con su configuración, aviso CT-22. **Criterio:** «Siguiente C1 disparado en la nueva fecha; ningún otro parámetro modificado».
- Documento 0 V5.3: 7.1 (C1 por HT-05 según F10, periodicidades del CT-04), 7.4 (CT-04: F5, F10 en lo que es servicio, CT-22), R6 (F10 y F5 de AG-01).
- Esquema de F10 V3.0: P-01 (régimen SERVICIO, valor inicial «semanal; ejecución el sábado, entrega el lunes 07:00»), reglas 4 y 5 (los cambios de SERVICIO no cambian la versión; `fecha_efecto`; los análisis en curso terminan con sus valores).
- Especificación de HT-05 (`bloque_a/10_Herramientas/ht05_planificador_ejemplo.md`): §2 franja sin disparos, §4 periodicidades y adelanto de 49 h, §5 idempotencia, disparos perdidos y cambios.

## Alcance

- **Entra:**
  - CT-04: el P-01 pasa a `PERIODICIDAD · ejecución · entrega …`; la ejecución la deduce HT-05 de la entrega (adelanto de la configuración, redondeo a la hora en punto); se rechaza con motivo lo que HT-05 no puede programar (franja 02:00-03:00, diaria que caería el día anterior). Lee también el P-01 de dos partes anterior. **Solo** la parte P-01 del CT-04: la de horizontes (P-03) la toca T-189 (Astra) y no se cambia.
  - HT-05: lectura y composición del P-01, días de ejecución por periodicidad (quincenal anclada en su primera ejecución), siguiente y última ejecución, entrega de cada ejecución.
  - `planificacion_c1.py`: siguiente C1 con los cambios de P-01 ya conocidos y su fecha de efecto; disparo del C1 vencido una sola vez (reserva en F5 en una transacción), disparos perdidos y fallo cerrado. Orden `bloque-a planificar [--ejecutar]`.
  - Configuración `planificador` (números de la especificación de HT-05).
- **No entra:** el disparo C1-ENTREGA (la entrega sale al terminar el ciclo, como antes), C1-CONTROL, C4, C5 y el personalizado; un demonio que llame a `planificar` (se deja a cron o similar); los horizontes del CT-04 (T-189).

## Diseño

- **Contratos y esquemas:** ninguno cambia. El CT-04 no gana campos; F5 (esquema en Markdown) gana entradas `DISPARO` y el `disparador` del RUN- lleva `disparo_id`, `programado`, `p01` y `cfg_id` además de `origen` HT-05.
- **Números:** `planificador.adelanto_ejecucion_h` (49 h; 2 h la diaria), `franja_sin_disparos_h` (2 a 3) y `recuperacion_disparo_perdido_h` (24), todos de la especificación de HT-05; `[PROPUESTO]` el adelanto de la quincenal y la mensual (INC-T197-01).
- **Cómo falla cerrado:** P-01 ilegible → `P01Invalido` antes de escribir nada; el CT-04 rechaza con motivo y no toca F10; el disparo se reserva en F5 dentro de `almacen._transaccion()` antes del ciclo y un corte del ciclo lo deja FALLIDO sin repetirlo; un instante con zona se rechaza.
- **Decisiones `[PROPUESTO]`:** INC-T197-01.

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| T-189 (Astra) toca el CT-04 en `origin/astra/encargos-bloque-a-c38-c47` | Conflicto de fusión | Solo se cambian el bloque P-01 y la línea del valor; `git merge-tree` con esa rama sin conflictos (ver `pruebas.md`) |
| El formato del P-01 cambia | Una prueba antigua esperaba el de dos partes | Se actualiza (`test_t87_contratos.py`) y el de dos partes se sigue leyendo |
| F10 inicial con la fecha real del sistema | Simulaciones con `--as-of` anterior a la instalación no tienen P-01 | Falla cerrado («F10 no tiene P-01»); las pruebas fijan la fecha de instalación |

## Criterios de aceptación (binarios)

1. CA-1: un CT-04 con QUINCENAL y entrega MIE 08:00 deja RET- `APLICADA`, un solo CFG- de P-01 escrito por AG-01 con `fecha_efecto` el día siguiente y valor «QUINCENAL · LUN 07:00 · entrega MIE 08:00», y avisa al Evaluador por CT-22; los cambios parciales conservan la otra parte; lo que HT-05 no puede programar se rechaza sin tocar F10.
2. CA-2: HT-05 calcula el siguiente C1 con el P-01 de F10 y su fecha de efecto (antes del cambio, el sábado 06-06; después, el lunes 08-06 y luego cada 14 días), con los números de la configuración.
3. CA-3: el siguiente C1 se dispara en la fecha nueva (lunes 08-06 07:00) y no en la antigua (sábado 06-06), y su RUN- lleva el P-01 y el CFG- con que empezó.
4. CA-4: ningún otro parámetro de F10 cambia (`methodology_version` incluida), ni con el CT-04 ni con el disparo.
5. CA-5: cada C1 se dispara una sola vez, también con varios procesos a la vez; un disparo perdido se recupera una vez si su entrega no venció en más de 24 h y si no queda PERDIDO; un ciclo cortado queda FALLIDO y no se repite; un P-01 ilegible no dispara ni escribe nada.
6. CA-6: suite de A ≥ 607 y sin fallos; cuotas sin subir (ruff 2807, mypy A 102); mutantes muertos; mapa y evidencias de PB-09 regenerados; ciclo mock y backtest como en develop; `./tools/check_all.sh` 12/12.

## Plan de pruebas

| Prueba | Tipo | Criterio |
| --- | --- | --- |
| `test_t197_periodicidad.py::test_ca1_*` (5) | nominal, límite, fallo cerrado, regresión del formato | CA-1 |
| `test_t197_periodicidad.py::test_ca2_*` (3) | nominal, límite (año de 53 semanas), configuración | CA-2 |
| `test_t197_periodicidad.py::test_ca3_*` (2) | nominal e integración con un ciclo real (cliente mock) | CA-3 |
| `test_t197_periodicidad.py::test_ca4_*` (1) | regresión | CA-4 |
| `test_t197_periodicidad.py::test_ca5_*` (7) | límite, fallo cerrado, concurrencia | CA-5 |
| `test_t87_contratos.py::test_ct04_conserva_frecuencia_y_aplica_desde_fecha_efecto`, `test_integracion.py::test_peticion_ad_hoc_y_decisiones` | regresión | CA-1 |
| `.docs/tickets/T-197/mutantes.py` | robustez de las pruebas | todos |
| Suite de A, gates, ciclo mock y backtest | regresión | CA-6 |

## Scripts

`.docs/scripts/evidencias_plan_a.py --pb PB-09` y `--ejecutar`; `.docs/tickets/T-197/mutantes.py` (nuevo).

## Registro

- 2026-11-24 · ABIERTO · claude · encargo de la sesión coordinadora (PB-09, «No comprueba» de las evidencias)
- 2026-11-24 · PLANIFICADO · claude · plan con el Plan de pruebas V3.0, el Documento 0 V5.3 (7.1, 7.4), el esquema de F10 y la especificación de HT-05
- 2026-11-24 · EN CURSO · claude · implementación (HT-05, `planificacion_c1.py`, P-01 del CT-04, `planificar`)
- 2026-11-24 · EN QA (r01) · claude · 18 pruebas nuevas, 32 mutantes muertos, evidencias regeneradas (PB-09 Superada), gate 12/12; commit local
- 2026-11-24 · EN CURSO (r02) · claude · QA r01 NO APTO (3 medios, 3 bajos): correcciones de H-01 a H-06 (`qa.md`), cada una con su prueba
- 2026-11-24 · EN QA (r02: QA r01 NO APTO) · claude · 35 pruebas en `test_t197_periodicidad.py` (+17), ataques del revisor 35/35, mutantes propios y del revisor muertos (R4 equivalente), evidencias regeneradas, gate 12/12; commit local «T-197 r02»
- 2026-11-24 · EN QA (ronda de cierre de la QA r02) · claude · QA r02 APTO pendiente de dos bajos: H-07 (identidad del proceso en la reserva) y H-08 (cierre del huérfano en `estado_run`), con sus pruebas y mutantes; commit local «T-197 cierre»
- 2026-11-24 · EN QA (segunda ronda de cierre de la QA r02) · claude · H-09 y H-10 (solo pruebas: el código no cambia), con los mutantes C1 a C3 del revisor muertos y pasados a `mutantes.py`; commit local «T-197 cierre 2»
- 2026-11-24 · segunda ronda de cierre verificada · APTO sin nada abierto (`qa.md`).
- 2026-11-24 · CERRADO · claude: integrado en `develop` con `commit_limpio.sh`.
