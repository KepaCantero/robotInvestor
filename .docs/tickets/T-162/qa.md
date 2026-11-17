# T-162 · QA independiente

- **Revisor:** Claude, subagente revisor nuevo sin el contexto de la implementación (regla del 12-11-2026) · **Ronda:** r01 · 16-11-2026
- **Copia:** worktree desechable en `3533cb7` («wip local: T-162»), `.venv` enlazado. Sin red ni gasto (todo con `MockClient`).

## Reproducción desde limpio

| Comprobación | Resultado |
| --- | --- |
| `tests/test_t162_respuesta_final.py` | 22/22 pasan (37 s) |
| Suite completa de A (`cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q -p no:cacheprovider`, máquina con carga ≈ 15) | 6919 recogidas: 6902 pasan, 2 omitidas y 15 fallan (1 h 24 min). Las 14 de `test_fase3_goldens.py` son las previstas (todas por `formas_flujos_mock.json`; con el golden generado, 102/102 en la copia desechable) y `test_t102_filtro.py::test_r05_h37_sufijo_en_tiempo_lineal` era de carga: repetida sola, con `test_textos_largos_en_tiempo_lineal`, 2/2. Sin esas 14, la suite queda muy por encima de la línea base (607) |
| Goldens: `tests/goldens_ct.py` en la copia | 1 diferencia, `formas_flujos_mock.json` (la prevista) |
| Goldens re-generados en una copia desechable (`git archive HEAD bloque_a docs sistema_global/seguimiento`, `goldens_ct.py --update`) | Solo cambia `formas_flujos_mock.json` (además de `REGISTRO.md`); el diff es **exactamente** el de `analisis-tecnico.md` (mismos cuatro hunks, solo añadidos) y las huellas coinciden: congelado `693eda19…7482`, generado `6b7339b2…6c24`. `divergencias_anexo_b.json` y los otros cinco generados no cambian. En esa copia, `test_fase3_goldens.py` 102/102 |
| Anexo B | El esquema `CT-03.RETORNO` de `anexo_b_esquemas.json` no fija `additionalProperties`: los campos de más de la final (`respuesta_final`, `run_id`, `limitaciones`) están admitidos (§6.2.3); la final nominal lo cumple (`test_ca1_…`) |
| Cuotas | ruff 2821 (≤ 2821); mypy de A 109 (≤ 109); ruff limpio en los dos ficheros nuevos y mypy sin errores en `respuesta_final.py` |
| Gates ligeros | `refs_vivas`, `secrets_scan`, `nfc_check` y `corpus_integridad` (695) en verde |

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 | sí | `test_ca1_*`; `r01_01` s01 (orden y enlace) |
| CA-2 | sí | `test_ca2_*`; `r01_01` s01: las OPP- son exactamente el top-3 del RUN- que salió por CT-02; los PRG- son exactamente los de ese RUN- y de esas opciones (no los del RUN- anterior de la misma opción, que existen); las TND- y CLM- son exactamente las de esas opciones; en el texto solo aparecen ese RUN- y esas OPP- |
| CA-3 | sí | `test_ca3_*`; `r01_01` s03 (G3 bloquea en la primera y en la segunda pasada, con un RUN- real: SIN_ENTREGA, solo el RUN-, sin CT-02), s04 (falla la auditoría tras registrar y entregar: FALLIDO, solo el RUN-) |
| CA-4 | sí | `test_ca4_*`; `r01_01` s09 (8 hilos con barrera: una nueva, 7 repetidas, iguales); `r01_02` (4 procesos a la vez: una nueva y tres repetidas con el mismo `msg_id`, una sola entrada en F5; tras reiniciar, `repetido`; almacén íntegro) |
| CA-5 | sí | `test_ca5_*`; `r01_02`: dos procesos aislados (`-I`, semilla de hash aleatoria) con la final ENTREGADO de 25 referencias, CT-03 y F5 iguales byte a byte (salvo `_ts`/`_hash`, que dependen del reloj de pared) |
| CA-6 | sí | `r01_02` contra la base `f2b3ad4`: con escalado (PB-07) y con `ejecutar_escalado=False`, el encargo y la provisional CT-03 son iguales byte a byte, la primera entrada QRY de F5 es igual (salvo la hora) y lo que devuelve `consulta` solo añade `respuesta_final` |
| CA-7 | sí | `test_pb07_de_punta_a_punta_con_el_simulado`; mapa en AUTOMATICA y evidencias «Superada» |
| CA-8 | sí | cuotas y gates arriba; suite: ver «Reproducción» |

**Lo que se pidió comprobar, además:**
- *Verdad.* Opciones inventadas en el top-3, CLM-/TND- inventadas: no se citan y quedan en `referencias_descartadas_final` (s02a). Confianza: la más baja de las citadas (s01); «en disputa» gana, y un valor no válido o ausente cuenta como «especulativo» (s05). Un RUN- PARCIAL sale ENTREGADO_PARCIAL con estado PARCIAL y «con alcance parcial» (s06). Solo con estado manipulado se consigue que cite algo ajeno (H-03).
- *R8.* El texto del error (un IBAN y un correo en un `KeyError` lanzado tras registrar el RUN-) no llega a la incidencia, a ningún mensaje ni a F5 (s04). Un correo en el `nombre` de una opción de F3 o un IBAN en las `limitaciones` del RUN-: la mensajería rechaza la final (`DatosSensibles`), no sale mensaje, no se escribe F5 y la incidencia SEGURIDAD no copia el dato (s07). En el flujo real ese dato tumbaría antes el CT-02 del RUN- (el nombre también va en él) y la final saldría FALLIDO sin opciones.
- *Idempotencia y reinicio.* Hilos y procesos, bien. Un reinicio a mitad (el proceso muere tras crear la provisional): el almacén queda íntegro y la QRY sin final, pero la final ya no se puede enviar bien (H-02). Dos consultas con el mismo RUN- (solo con F5 manipulado): cada una tiene su final y la segunda cita el RUN- de la primera (H-03).
- *El try/except.* Con `--sin-escalado` todo es como antes salvo la final (CA-6). `KeyboardInterrupt`/`SystemExit` no se capturan. Pero un fallo de integridad del almacén a mitad del RUN- se queda en una incidencia HERRAMIENTA (H-01).
- *Decisiones `[PROPUESTO]`.* INC-T162-01 y la fila del §6 recogen las seis (esquema propio, cinco resultados, referencias, confianza, final también sin análisis, sin `tema_normalizado`) y son prudentes. Matiz para H-01: «no relanzar la excepción del RUN-» está apuntado en general, sin decir que incluye los fallos de integridad. La fila de la deuda técnica sigue «EN CURSO»; la lleva la sesión coordinadora.

## Mutantes propios (`r01_03_mutantes.py`)

25 mutantes de `respuesta_final.py` y del cambio de `consulta`: 23 muertos y 2 vivos esperados (M15, quitar las reglas `allOf` del esquema, que `construir` nunca viola; M18, el RUN- candidato aunque no conste, que filtra `existentes`). **Seis solo los matan las sondas del revisor, no las 22 pruebas de T-162** (H-04): M01 (confianza más alta en vez de más baja), M02 (PRG- de cualquier RUN- de la opción), M07 (tras el fallo no se busca el RUN- registrado), M11 y M12 (un RUN- PARCIAL se da por COMPLETO) y M16 (confianza no válida → «establecido»).

## Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | media | `r01_02`, bloque 4: bloque abierto, sello de F2 manipulado en `sellos_integridad.json` (la consulta lee F1–F6 sin notarlo; falla el primer `escribir` de F2 dentro del RUN-), `consulta(PB-07)` | Esperado: que un fallo de integridad pare, como en la base (`ValueError: Fallo de integridad en el sello de F2`). Obtenido: la consulta termina sin error (la CLI saldría con 0), escribe la QRY en F5, envía la provisional y la final FALLIDO, y en HA solo queda `HERRAMIENTA · «El análisis escalado de QRY-… falló (ValueError)»`, sin `escalado_operador` y sin decir que es integridad. La final no miente ni cita nada, y el siguiente ciclo volvería a fallar cerrado, pero el `except Exception` trata igual un fallo de herramienta que uno del almacén o de los controles (`EscrituraFueraDeReserva`, `PronosticoCongelado`, `DatosSensibles`; estos al menos dejan su propia incidencia) | Relanzar (después de dejar la incidencia) los fallos de integridad del almacén y las excepciones de control, o comprobar `almacen.verificar_integridad()` en el `except` y relanzar si algo falla; como mínimo, incidencia con tipo propio y `escalado_operador`. Apuntar el alcance exacto en INC-T162-01. Prueba de regresión con este escenario | abierto |
| H-02 | media | `r01_02`, bloque 2 (el proceso muere justo después de la provisional y se reabre) y `r01_01` s08 (la final la rechaza la mensajería dentro de `consulta`) | Esperado: que una final pendiente se pueda enviar después con su enlace correcto. Obtenido: F5 no guarda el `msg_id` de la provisional, nada reintenta las finales pendientes y `enviar` acepta cualquier `provisional_msg_id` (`MSG-2026-999999` → final SIN_ENTREGA enlazada a un mensaje que no existe); si `enviar` lanza dentro de `consulta`, la consulta se cae después de la provisional y el `msg_id` solo queda en memoria. La ventana del corte es pequeña en el ejecutor síncrono; el fallo de `enviar` (R8, esquema, integridad) es la vía realista | Guardar el `msg_id` de la provisional en F5 (p. ej. una entrada más de la QRY- tras crearla, o reservar el `msg_id` antes de escribir) y que `enviar` lo lea de ahí en vez de recibirlo (o lo compare); una función que envíe las finales pendientes (QRY ANALITICA sin final) al reabrir | abierto |
| H-03 | baja | `r01_01` s02b (xfail estricto) y s10 | Con estado manipulado: un identificador existente de otro tipo en `evidencias` de una opción (un RUN- ajeno) se cita, y un HIT- hace fallar toda la final por el patrón del esquema; una QRY- cuyo `escalado` apunta al RUN- de otra consulta recibe una final con las opciones de ese RUN-. Esperado: descartar lo que no es del tipo del campo, y no citar un RUN- cuyo `disparador.qry_id` no es la consulta | Filtrar cada campo por su prefijo (TND- en `tnd_ids`, CLM- en `evidencias`) antes de `existentes`, y comprobar `run["disparador"]["qry_id"] == qry_id` (si no, SIN_ENTREGA) | abierto |
| H-04 | baja | `r01_03_mutantes.py` | Seis mutantes (M01, M02, M07, M11, M12, M16) sobreviven a las 22 pruebas de T-162: en el escenario nominal las tres opciones tienen la misma confianza, el RUN- anterior no deja PRG- que se puedan colar, ninguna prueba registra el RUN- antes de fallar y ninguna ejercita un RUN- PARCIAL ni una confianza no válida | Añadir a la suite del ticket esos casos (las sondas s01, s04, s05 y s06 sirven de modelo) | abierto |

## Veredicto

**APTO** · los ocho criterios se cumplen y no hay hallazgos críticos ni altos. La final dice la verdad: solo cita el RUN- y, de su top-3, las OPP- con sus TND-, CLM- y PRG- de ese RUN-; sin entrega, fallo o sin lanzar, no cita ninguna opción; la confianza es la más baja de las citadas; no copia el texto del error ni datos protegidos (la mensajería rechaza la final entera). Es idempotente entre hilos, procesos y reinicios y es determinista entre procesos; la provisional y `--sin-escalado` quedan como en la base salvo la final, y el diff de los goldens es exactamente el declarado. H-01 y H-02 (medias) y H-03 y H-04 (bajas) no bloquean: pasan a la deuda técnica con su ID. Lo hace la sesión coordinadora, igual que el re-congelado de `formas_flujos_mock.json`. Esta QA no cierra el ticket ni toca la deuda.

## Scripts del revisor (orden)

Desde la raíz de la copia de trabajo:

1. `cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q -p no:cacheprovider ../../.docs/tickets/T-162/revisores/r01_01_sondas.py` (11 pasan y 2 xfail estrictos de H-03; ≈ 75 s).
2. `git archive f2b3ad4 bloque_a | tar -x -C <base>` y `.venv/bin/python .docs/tickets/T-162/revisores/r01_02_procesos_y_base.py <trabajo> <base>/bloque_a` (0 fallos; anota H-01 y H-02; ≈ 15 min con carga).
3. Copia desechable `<…t162_mut>` con `git archive HEAD bloque_a`, `.venv` enlazado y `r01_01_sondas.py` en `.docs/tickets/T-162/revisores/`; `.venv/bin/python .docs/tickets/T-162/revisores/r01_03_mutantes.py <…t162_mut>` (23 muertos, 2 vivos esperados; ≈ 40 min).
