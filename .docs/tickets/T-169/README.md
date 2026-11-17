# T-169 · Bloque A: hallazgos de la QA r01 de T-162 (respuesta final por CT-03, PB-07)

| Campo | Valor |
| --- | --- |
| Estado | CERRADO (17-11-2026, QA r02 APTO tras la ronda de cierre) |
| Pieza | bloque_a (ejecutor: consulta C3; `bloque_a/respuesta_final.py` y `Bloque.consulta`/`Bloque.ciclo`) |
| Planifica · implementa · QA | claude · claude · un revisor nuevo sin contexto (regla del 12-11-2026, `compartida/2026-11-12_claude-puede-hacer-qa`) |
| Aprobación del operador | no necesaria: corrige hallazgos de una QA (H-01 y H-02, medios; H-03 y H-04, bajos) de una función ya diseñada (T-162); solo endurece. Lo que el diseño no dice se decide por defecto (`compartida/2026-11-13_decide-el-agente-por-defecto`) y queda `[PROPUESTO]` en INC-T169-01 |
| Deuda técnica | T-169 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` (la fila la pone la sesión coordinadora; este ticket no la toca) |
| Base | commit `3533cb7` («wip local: T-162»), en la copia `t162`; la QA de T-162 está en `.docs/tickets/T-162/qa.md` y `.docs/tickets/T-162/revisores/` (no se tocan) |

## Objetivo

Que T-162 pueda integrarse en `develop` sin regresión: un fallo de integridad o de control del almacén vuelve a parar la
consulta como en la base (H-01); una final que no salió se puede enviar después, con su enlace a la provisional comprobado
contra F5 (H-02); la final no cita nada ajeno con estado manipulado (H-03); y las pruebas matan los seis mutantes que
sobrevivían (H-04).

## Alcance

- Entra:
  - `bloque_a/11_Ejecutor/bloque_a/respuesta_final.py`: `para_la_consulta` (qué fallos del RUN- se relanzan), `registrar_provisional`
    (el `msg_id` de la provisional y la clase del fallo en F5), `enviar` que lo exige y lo compara, `pendientes` y
    `enviar_pendientes` (camino determinista para las finales que no salieron), filtro por tipo de las referencias y
    comprobación de `disparador.qry_id` del RUN-.
  - `bloque_a/11_Ejecutor/bloque_a/orquestacion.py`, lo justo: en `consulta`, relanzar lo que diga `para_la_consulta`, registrar
    la provisional y enviar antes las pendientes; en `ciclo`, enviar las pendientes al empezar.
  - Pruebas nuevas en `bloque_a/11_Ejecutor/tests/test_t169_hallazgos_t162.py`; en `tests/test_t162_respuesta_final.py`, el RUN-
    simulado de `test_ca3_un_run_bloqueado_o_sin_registro_da_sin_entrega` lleva el `disparador` que lleva el de verdad (la regla de
    H-03 lo exige; no se debilita nada).
  - `docs/incidencias.md` (INC-T169-01 y una nota en INC-T162-01), una fila en §6 de
    `sistema_global/seguimiento/Decisiones_del_operador_Bloque_A.md`, `bloque_a/11_Ejecutor/README.md`, y el mapa del plan
    (`tests/mapa_plan_pruebas.json`, PB-07: una prueba más) con las evidencias regeneradas.
- No entra: el corpus, el Documento 0, `guias.py`, `evaluador.py`, `motor/`, `herramientas/`, `contratos.py`, los goldens (no se
  re-congelan), el `qa.md` y los scripts del revisor de T-162, otros bloques.

## Diseño

- **H-01.** En el `except` del RUN- escalado, antes de escribir nada: si el error es de control (`PermissionError`, que cubre
  `EscrituraFueraDeReserva`, `PronosticoCongelado`, `CanalNoPrevisto` y `DatosSensibles`; `MensajeInvalido`; `FugaDeInformacion`)
  o `almacen.verificar_integridad()` da algún fichero roto, se relanza: la consulta se para como en la base, sin QRY en F5, sin
  provisional ni final y sin la incidencia HERRAMIENTA. Solo los demás fallos (los del análisis, con el almacén íntegro) siguen
  dando la final FALLIDO.
- **H-02.** Tras crear la provisional, una entrada más de la QRY- en F5 guarda `provisional_msg_id` (y `fallo_analisis`, la clase
  del error, si el RUN- falló). `enviar` lo lee de F5: sin él no hay final (`RespuestaFinalInvalida`), y un `provisional_msg_id`
  dado que no coincide se rechaza (también si la final ya está). `pendientes(almacen, as_of)` lista, en el orden de F5, las QRY-
  ANALITICA con provisional registrada y sin final; `enviar_pendientes(bloque, as_of)` las envía con la fecha de la QRY- (la
  misma final que habría salido) al empezar cada `consulta` y cada `ciclo`. Una pendiente que la validación o la mensajería
  rechazan (nada escrito) se aparta una vez: entrada `final_no_enviable` en F5 con la clase del error e incidencia en HA con
  `escalado_operador`; no se reintenta sola y no para el resto. Un fallo de integridad o de control sí para (como en H-01).
- **H-03.** Cada campo se filtra por su tipo antes de mirar si existe: TND- de `tnd_ids`, CLM- de `evidencias`, PRG- de F4; lo de
  otro tipo va a `referencias_descartadas_final`. El RUN- solo cuenta si su `disparador.qry_id` es la consulta; si no, SIN_ENTREGA
  («el RUN- no lo lanzó esta consulta»), sin citarlo ni enlazarlo en el sobre.
- **H-04.** Pruebas para M01 (confianzas distintas), M02 (PRG- del RUN- anterior de la misma opción), M07 (RUN- registrado antes
  del fallo), M11 y M12 (RUN- PARCIAL) y M16 (confianza no válida).
- **Contrato y goldens.** El mensaje CT-03 final no cambia de forma. En los flujos congelados no hay finales pendientes ni RUN-
  ajenos, así que `formas_flujos_mock.json` no debe cambiar más allá de lo de T-162 (se comprueba).
- **Números.** Ninguno nuevo.

## Ronda r02 (QA r01 de T-169: NO APTO sin altos; `qa.md` y `revisores/r01_0*.py`)

- **H-01 (media):** `enviar_pendientes` ya no propaga cualquier error. Solo propaga lo que para una consulta (`para_la_consulta`: integridad o control); un rechazo sin efecto con el almacén íntegro se sigue apartando; cualquier otro error (un `KeyError` de un `escalado` incompleto) se aparta igual, con su incidencia escalada, y el `ciclo` y la `consulta` siguen.
- **H-02 (baja):** `ReplayFaltante` entra en `ERRORES_DE_CONTROL`: una respuesta no grabada en el modo «reproducir» para la consulta.
- **H-03 (baja):** el envío y el apartado de cada pendiente, bajo `almacen._transaccion()`, y dentro se vuelve a mirar si ya está apartada: una sola marca y una sola incidencia aunque la vean varios hilos o procesos.
- **H-04 (baja):** pruebas para Q02, Q03 y Q10 en `tests/test_t169_r02.py`.
- Criterios r02: las sondas p04, p05 y p06 de `revisores/r01_01_sondas.py` dan XPASS; `r01_02` sin fallos; Q02, Q03 y Q10 (y sus versiones sobre el texto nuevo) mueren; goldens como en T-162; cuotas; suite A.

## Ronda de cierre (QA r02 de T-169: NO APTO solo por tres bajos; `qa.md` y `revisores/r02_0*.py`)

- **H-01 (baja):** en `respuesta_final._apartar`, primero la incidencia y después la marca `final_no_enviable` en F5. Si falla la incidencia, la pendiente sigue y se reintenta; si falla la marca, como mucho se repite la incidencia. Nunca queda apartada sin escalar. El detalle añade «puede haberse creado el mensaje; revisar antes de reenviar» (nota `a08`). Las sondas `a07` y `b01` pasan a `tests/test_t169_r02.py` sin xfail.
- **H-02 (baja):** prueba de la sonda `a01` (`KeyError("clases")`, `RuntimeError` y `OSError` con el sello de F2 roto: para y no aparta). El mutante S01 entra en `PROPIOS` de `scripts/mutantes_t169.py`.
- **H-03 (baja):** `docs/incidencias.md` (INC-T169-01, apartado de H-02) y `bloque_a/11_Ejecutor/README.md`, con el texto exacto de la QA.
- Criterios de cierre: las pruebas del ticket pasan; `a07` y `b01` dan XPASS en las sondas del revisor; S01 muere; ruff y mypy de A sin hallazgos nuevos.

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| Relanzar demasiado | Un fallo corriente del análisis vuelve a tumbar la consulta | Solo control e integridad; prueba de que un `RuntimeError` o un `KeyError` tras registrar el RUN- siguen dando FALLIDO |
| Una pendiente que nunca se puede enviar | Bloquearía todas las consultas y ciclos | Se aparta una vez con incidencia escalada; prueba |
| Enviar pendientes dentro de `ciclo` | Cambiaría los flujos congelados | Sin pendientes no se crea nada (ni identificadores); goldens comprobados |
| La entrada nueva de F5 | Otro lector cuenta doble | No lleva `tema_normalizado`; prueba de la pregunta repetida |

## Criterios de aceptación (binarios)

1. CA-1 (H-01): con el sello de F2 manipulado con el bloque abierto, la consulta escalada lanza `ValueError` «Fallo de
   integridad en el sello de F2» y no deja QRY en F5, ni CT-03 RETORNO, ni incidencia HERRAMIENTA; un error de control del RUN-
   también se relanza; un error corriente sigue dando FALLIDO.
2. CA-2 (H-02): la provisional queda en F5; `enviar` rechaza un `provisional_msg_id` inventado o una QRY- sin provisional
   registrada, sin escribir nada; una final que no salió la envía la consulta siguiente, el ciclo siguiente o un bloque reabierto,
   una sola vez, enlazada a la provisional verdadera e igual a la que habría salido; una pendiente que la mensajería rechaza se
   aparta con incidencia escalada y no se reintenta.
3. CA-3 (H-03): un RUN- o un HIT- dentro de `evidencias` no se cita ni tumba la final; una QRY- que apunta a un RUN- que no lanzó
   da SIN_ENTREGA sin citarlo; las sondas `test_s02b_*` de `r01_01_sondas.py` dejan de fallar su aserción (XPASS).
4. CA-4 (H-04): los mutantes M01, M02, M07, M11, M12 y M16 mueren con las pruebas del ticket.
5. CA-5: las 22 de T-162 siguen pasando; goldens sin más cambio que el de T-162; ruff ≤ 2821, mypy A ≤ 109; suite A completa y
   gates ligeros.

## Plan de pruebas

| Prueba (en `tests/test_t169_hallazgos_t162.py`) | Tipo | Criterio |
| --- | --- | --- |
| `test_h01_un_fallo_de_integridad_para_la_consulta_como_en_la_base` | regresión, fallo cerrado | CA-1 |
| `test_h01_un_error_de_control_del_run_se_relanza` (4 clases) | fallo cerrado | CA-1 |
| `test_h01_un_error_corriente_tras_registrar_el_run_sigue_dando_fallido` | regresión | CA-1, CA-4 (M07) |
| `test_h02_la_provisional_queda_en_f5` | nominal | CA-2 |
| `test_h02_enviar_rechaza_una_provisional_inventada_o_sin_registrar` | fallo cerrado | CA-2 |
| `test_h02_la_siguiente_consulta_envia_la_final_pendiente`, `…_el_siguiente_ciclo_…`, `…_un_bloque_reabierto_…` | integración, idempotencia | CA-2 |
| `test_h02_la_final_recuperada_es_la_que_habria_salido` | determinismo | CA-2 |
| `test_h02_una_pendiente_que_la_mensajeria_rechaza_se_aparta_una_vez` | fallo cerrado | CA-2 |
| `test_h03_un_id_de_otro_tipo_en_las_evidencias_no_se_cita` (RUN-, HIT-) y `…_en_las_tendencias_…` | fallo cerrado | CA-3 |
| `test_h03_un_run_que_no_lanzo_la_consulta_no_se_cita` | fallo cerrado | CA-3 |
| `test_h04_*` (confianza más baja, confianza no válida, PRG- solo de su RUN-, RUN- PARCIAL) | regresión | CA-4 |
| `r01_03_mutantes.py` en una copia desechable, con las pruebas del ticket; `r01_01_sondas.py` | mutantes, sondas | CA-3, CA-4 |
| Las 22 de T-162, vecinas, goldens, gates ligeros, suite A completa | regresión | CA-5 |

## Scripts

`.docs/scripts/nuevo_ticket.sh`, `.docs/scripts/evidencias_plan_a.py --ejecutar`, `bloque_a/11_Ejecutor/tests/goldens_ct.py`
(solo comprobación); los del revisor de T-162 (`r01_01_sondas.py`, `r01_02_procesos_y_base.py`, `r01_03_mutantes.py`), sin cambiarlos.

## Registro

- 2026-11-16 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-16 · PLANIFICADO · claude · plan y criterios a partir de `.docs/tickets/T-162/qa.md`
- 2026-11-16 · EN CURSO · claude · implementación y pruebas
- 2026-11-16 · EN QA · claude · pendiente de un revisor nuevo
- 2026-11-16 · EN CURSO · claude · r02: hallazgos H-01 a H-04 de la QA r01 de T-169 (NO APTO sin altos)
- 2026-11-16 · EN QA · claude · r02 lista, pendiente de un revisor nuevo
- 2026-11-17 · EN CURSO · claude · ronda de cierre: H-01 a H-03 de la QA r02 de T-169 (tres bajos)
- 2026-11-17 · EN QA · claude · ronda de cierre lista (commit local), pendiente de revisor
- 2026-11-17 · CERRADO · claude (revisor) · ronda de cierre comprobada: H-01 a H-03 de la r02 corregidos; QA r02 APTO
