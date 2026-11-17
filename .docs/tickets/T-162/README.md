# T-162 · Bloque A: respuesta final por CT-03 al terminar el análisis escalado de una consulta (PB-07)

| Campo | Valor |
| --- | --- |
| Estado | EN QA |
| Pieza | bloque_a (ejecutor: consulta C3, CT-03; módulo nuevo `bloque_a/respuesta_final.py`) |
| Planifica · implementa · QA | claude · claude · un revisor nuevo sin contexto (regla del 12-11-2026, `compartida/2026-11-12_claude-puede-hacer-qa`) |
| Aprobación del operador | no necesaria: completa una función del diseño (§7.6.3 del Documento 0, PB-07) con un mensaje CT-03 nuevo por un canal ya previsto (AG-01 → BROKER); no cambia la Constitución, los controles ni ningún mensaje que ya existía. Lo que el diseño no dice se decide por defecto (`compartida/2026-11-13_decide-el-agente-por-defecto`) y queda `[PROPUESTO]` en INC-T162-01 |
| Deuda técnica | T-162 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` (la fila la lleva la sesión coordinadora; este ticket no la toca) |

## Objetivo

Que una consulta CT-03 del Broker que escala a análisis (ruta ANALITICA) reciba, al terminar el RUN- ad hoc, una **respuesta
final por CT-03 con referencias**, como pide PB-07 («respuesta final por CT-03 con referencias») y §7.6.3 del Documento 0
(«entrega primero una respuesta provisional con lo que ya se sabe»). Hoy el ejecutor envía solo la provisional, con el RUN-
enlazado (INC-T116-03, fila PB-07 de `docs/evidencias_pruebas_bloque_a.md`).

## Kit de contexto leído

- Documento 0 V5.1: §6.1 (CT-03), §7.6 (consultas del Broker), F5 (QRY-), Anexo B (CT-03), vocabulario de confianza.
- Plan de pruebas V3.0: PB-07.
- `bloque_a/contratos.py` (CT-03, `CAMPOS_RETORNO`, `Mensajeria.crear`/`validar`, `ESQUEMAS["CONSULTA"]`),
  `bloque_a/orquestacion.py` (`Bloque.consulta`, `ciclo`, `_registrar_run`), `bloque_a/cli.py` (`consulta`, `--sin-escalado`),
  `tests/goldens_ct.py` (flujo `consulta_que_escala`).

## Alcance

- Entra:
  - `bloque_a/11_Ejecutor/bloque_a/respuesta_final.py` (nuevo): esquema JSON de la respuesta final, su construcción
    determinista desde F3, F4 y F5, la validación (esquema + mensajería) y el envío idempotente.
  - `bloque_a/11_Ejecutor/bloque_a/orquestacion.py`, solo `consulta`: el RUN- ad hoc se envuelve para que un fallo no se pierda
    (la provisional y la final dicen que falló) y, tras la provisional, se envía la final.
  - Pruebas nuevas en `bloque_a/11_Ejecutor/tests/test_t162_respuesta_final.py`.
  - `tests/mapa_plan_pruebas.json` (PB-07) y `docs/evidencias_pruebas_bloque_a.md` regenerado con
    `.docs/scripts/evidencias_plan_a.py --ejecutar` (`tests/MAPA_PLAN_DE_PRUEBAS.md` no: es el mapa histórico del 3-11,
    que se conserva como estaba).
  - `docs/incidencias.md` (INC-T162-01 y la nota «aplicada» de PB-07 en INC-T116-03),
    `sistema_global/seguimiento/Decisiones_del_operador_Bloque_A.md` (una fila en §6) y `bloque_a/11_Ejecutor/README.md`.
- No entra:
  - La forma de la respuesta provisional (no cambia ni un byte en los flujos que ya existían) ni el orden síncrono del
    ejecutor (la provisional se crea después del RUN-; ver Riesgos).
  - Los goldens: no se re-congelan. El flujo congelado `consulta_que_escala` cambia porque tiene un mensaje más; el diff exacto
    va en `analisis-tecnico.md` para que lo coordine la sesión coordinadora con el Documento 0 V5.2 (T-143).
  - El corpus, el Documento 0, `guias.py`, `evaluador.py`, `motor/`, `herramientas/verificador_ids.py`, `contratos.py`
    (no hace falta tocarlo: el canal y los campos mínimos de CT-03 ya admiten la final), otros bloques y el marco común de C.
  - El tiempo real de la provisional (< 2 minutos) y que un modelo real no responda con conocimiento propio: necesitan la API.

## Diseño

- **Contrato.** CT-03 RETORNO, AG-01 → BROKER (canal ya previsto). Cuerpo: los campos del Anexo B (`clase_consulta`, `ruta`
  ANALITICA, `respuesta`, `referencias`, `confianza`, `escalado` igual al de la provisional) y uno nuevo, `respuesta_final`
  (`provisional_msg_id`, `resultado_analisis`). Sobre: `query_id` de la consulta, `run_id` del RUN- (si lo hay),
  `estado` común (COMPLETO, PARCIAL o SIN_RESULTADO) y `limitaciones`. No cambia `VERSION_CONTRATO` ni ninguna tabla de
  `contratos.py`. El esquema vive en `respuesta_final.ESQUEMA` (la final la escribe el código, no un agente: no es de
  `contratos.ESQUEMAS`, cuyos goldens no cambian).
- **`resultado_analisis`** (de F5, fuente de verdad): ENTREGADO (RUN- COMPLETO y entregado), ENTREGADO_PARCIAL (PARCIAL y
  entregado), SIN_ENTREGA (G3 bloqueó, ningún tipo analizable o el RUN- no consta en F5), FALLIDO (el RUN- lanzó una
  excepción) y NO_EJECUTADO (`--sin-escalado`).
- **Referencias.** Solo identificadores que existen en F1–F6 o RC a la fecha de la consulta: el RUN-, y por cada opción del
  top-3 del RUN- (en su orden) su OPP-, sus TND-, sus CLM- (evidencias) y sus PRG- congelados por ese RUN- (F4). Sin entrega,
  solo el RUN- (si consta); fallido o no ejecutado, ninguna.
- **Confianza.** Con opciones entregadas, la más baja de las de esas opciones en F3 (orden: establecido > probable >
  especulativo > en disputa). Sin opciones o sin resultado, la más baja entre la provisional y «especulativo».
- **Texto.** Escrito por el código con lo que hay en F3 y F5 (sin llamar al modelo): resultado, nivel y tipos analizados, cada
  opción con su identificador, nombre y confianza, y la remisión a las limitaciones; sin resultado, lo dice y añade que la
  provisional no se confirma ni se amplía.
- **Estado persistido.** F5 (append-only, AG-01): una entrada más del mismo `QRY-` con `estado` `RESPONDIDA_FINAL` o
  `FINAL_SIN_RESULTADO` y `respuesta_final` (el mensaje enviado, sin el sobre). La lectura consolidada de F5 por `id` la une a la
  de la provisional. No lleva `tema_normalizado`: la cuenta de preguntas repetidas no cambia. No hay esquema de estado que
  migrar.
- **Idempotencia.** Bajo la transacción del almacén (también entre procesos): si F5 ya tiene la final de ese `QRY-`, se
  devuelve la guardada (`repetido: true`) sin crear mensaje. Orden: construir → validar contra el esquema → `Mensajeria.crear`
  (valida canal, R8 y campos mínimos) → F5. Si algo falla antes de F5, no queda nada escrito.
- **Fallo cerrado.** Excepción en el RUN-: incidencia HERRAMIENTA en HA con la clase del error (sin el texto), `estado_run`
  FALLIDO en el `escalado` y final SIN_RESULTADO. Cualquier referencia que no exista se descarta; la final nunca cita nada que
  no esté en la memoria del bloque.
- **Números.** Ninguno nuevo.
- **Decisiones `[PROPUESTO]`** (INC-T162-01 y §6 de las decisiones del Bloque A): el campo `respuesta_final`; los cinco
  resultados; qué referencias lleva; la regla de confianza; enviar la final también cuando el RUN- falla o no se lanza; no
  relanzar la excepción del RUN-.

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| La final cambia el flujo congelado `consulta_que_escala` | `test_fase3_goldens` falla hasta que se re-congele | No se re-congela aquí: diff exacto en `analisis-tecnico.md`; la coordinación la hace la sesión coordinadora junto con el Anexo B de la V5.2 |
| Capturar la excepción del RUN- oculta un fallo | Un error del ciclo deja de verse en la CLI | Incidencia en HA con la clase del error; la provisional y la final lo dicen; prueba que lo comprueba |
| Un segundo envío por reintento | El Broker recibe dos finales | F5 como registro de la final, comprobado bajo la transacción del almacén; prueba de idempotencia |
| Leer F5 «QRY» con dos entradas por consulta | Otro lector cuenta doble | El único lector (pregunta repetida) filtra por `tema_normalizado`, que la final no lleva; prueba de regresión |
| En el ejecutor síncrono la provisional se crea después del RUN- | El orden temporal de PB-07 no es el de un ejecutor asíncrono | Se mantiene (no cambiar la provisional); la final sale siempre después de la provisional y lo comprueba la prueba |

## Criterios de aceptación (binarios)

1. CA-1: una consulta que escala y cuyo RUN- termina recibe, después de la provisional, una segunda CT-03 RETORNO AG-01 → BROKER
   con el `query_id` de la consulta, el `run_id` del RUN-, `respuesta_final.provisional_msg_id` igual al `msg_id` de la
   provisional, y que cumple `respuesta_final.ESQUEMA` y la mensajería.
2. CA-2: sus referencias son el RUN- y las OPP- del top-3 del RUN- con sus TND-, CLM- y PRG-, y cada una existe en F1–F6/RC.
3. CA-3: si el RUN- falla (excepción), la final lleva `estado` SIN_RESULTADO, `resultado_analisis` FALLIDO, ninguna referencia,
   un texto que lo dice y una incidencia en HA; la provisional dice `estado_run` FALLIDO. Si el RUN- no entrega, SIN_ENTREGA; si
   no se lanza, NO_EJECUTADO.
4. CA-4: enviar la final dos veces para la misma consulta crea un solo mensaje y una sola entrada de F5; la segunda devuelve la
   misma con `repetido`.
5. CA-5: dos ejecuciones con las mismas entradas dan la misma final, byte a byte.
6. CA-6: la provisional no cambia (misma forma y valores que antes en la consulta que escala), la N0 no recibe final y la
   cuenta de preguntas repetidas no cambia.
7. CA-7: PB-07 de punta a punta con el simulado: la pregunta del plan → CONTRASTE, ANALITICA, provisional con nivel y plazo,
   RUN- de alcance mínimo enlazado a la QRY-, final con referencias; el mapa la da por AUTOMATICA y las evidencias, «Superada».
8. CA-8: cuotas ruff ≤ 2821 y mypy A ≤ 109; suite A ≥ 607; gates ligeros en verde.

## Plan de pruebas

| Prueba | Tipo | Criterio |
| --- | --- | --- |
| `test_ca1_la_final_sale_despues_de_la_provisional_enlazada_a_la_consulta_y_al_run` | nominal, contrato | CA-1 |
| `test_ca2_las_referencias_son_las_del_run_y_existen_en_la_memoria` | nominal | CA-2 |
| `test_ca3_si_el_run_falla_la_final_lo_dice_sin_referencias` | fallo cerrado | CA-3 |
| `test_ca3_un_run_sin_entrega_da_sin_entrega`, `test_ca3_un_run_bloqueado_o_sin_registro_da_sin_entrega`, `test_ca3_sin_escalado_la_final_dice_que_no_se_ejecuto` y `test_ca3_sin_escalado_por_la_cli` | fallo cerrado | CA-3 |
| `test_ca3_una_referencia_que_no_existe_no_se_cita` | fallo cerrado | CA-2, CA-3 |
| `test_ca1_una_final_que_no_cumple_el_esquema_no_sale_ni_se_registra` y `test_ca1_una_consulta_n0_o_inexistente_no_admite_final` | fallo cerrado | CA-1 |
| `test_ca4_enviar_dos_veces_no_duplica` y `test_ca4_dos_hilos_a_la_vez_envian_una_sola_final` | idempotencia | CA-4 |
| `test_ca5_dos_ejecuciones_dan_la_misma_final` | determinismo | CA-5 |
| `test_ca6_*` (provisional intacta, N0 sin final, pregunta repetida) | regresión | CA-6 |
| `test_pb07_de_punta_a_punta_con_el_simulado` | integración | CA-7 |
| Vecinas: `test_integracion.py`, `test_fase4_huecos.py`, `test_t65_qa_r01.py`, `test_t66_propuestas.py`, `test_t101_v6.py`; goldens `test_fase3_goldens.py`; gates ligeros; suite A completa | regresión | CA-6, CA-8 |

## Scripts

`.docs/scripts/nuevo_ticket.sh`, `.docs/scripts/evidencias_plan_a.py --ejecutar`, `bloque_a/11_Ejecutor/tests/goldens_ct.py`
(solo comprobación).

## Registro

- 2026-11-16 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-16 · PLANIFICADO · claude · plan y criterios
- 2026-11-16 · EN CURSO · claude · implementación y pruebas
- 2026-11-16 · EN QA · claude · pendiente de un revisor nuevo; goldens sin re-congelar (diff en `analisis-tecnico.md`); la sesión se cortó por el límite de uso y se retomó en la misma copia: las vecinas habían terminado y se relanzó una vez la suite completa
