# T-169 · Análisis técnico

## Causa raíz o motivo

Hallazgos de la QA r01 de T-162 (`.docs/tickets/T-162/qa.md`, APTO con H-01 a H-04):

- **H-01.** El `except Exception` que T-162 puso alrededor del RUN- escalado de `Bloque.consulta` trataba igual un fallo del
  análisis que uno del almacén o de los controles. Con el sello de F2 manipulado, la base se paraba con «Fallo de integridad en el
  sello de F2»; con T-162 la consulta seguía, enviaba provisional y final FALLIDO y solo quedaba una incidencia HERRAMIENTA.
- **H-02.** El `msg_id` de la provisional solo vivía en memoria: si la final no salía (el proceso muere, la mensajería la rechaza),
  nada la reintentaba, y `enviar` aceptaba cualquier `provisional_msg_id`.
- **H-03.** `construir` citaba cualquier identificador existente que hubiera en `evidencias` (un RUN- ajeno), o fallaba entera
  con un HIT-; y no comprobaba que el RUN- del `escalado` lo hubiera lanzado esa consulta.
- **H-04.** Seis mutantes del revisor (M01, M02, M07, M11, M12 y M16) sobrevivían a las 22 pruebas de T-162.

## Evidencia

- H-01: sonda del bloque 4 de `r01_02_procesos_y_base.py`, reproducida con un bloque solo de divisas en 3 s (sello de F2 → la
  consulta escalada a DIV terminaba con `estado_run` FALLIDO). Ahora: `ValueError: Fallo de integridad en el sello de F2`, sin QRY
  ni CT-03 RETORNO ni HERRAMIENTA (`test_h01_un_fallo_de_integridad_para_la_consulta_como_en_la_base`).
- H-02 y H-03: con el código de T-162 (`3533cb7`), 21 de las 27 primeras pruebas nuevas fallan (todas las de H-01, H-02 y H-03); las 6 de
  H-04 pasan igual, porque solo matan mutantes.
- H-03: `r01_01_sondas.py::test_s02b_*` (xfail estrictos) pasan a XPASS(strict): su aserción ya se cumple.
- H-04: el ejecutor de mutantes del ticket (ver «Comandos») da los seis MUERTO con `tests/test_t169_hallazgos_t162.py`.

## Implementación

### Archivos cambiados y por qué

| Archivo | Cambio |
| --- | --- |
| `bloque_a/11_Ejecutor/bloque_a/respuesta_final.py` | `ERRORES_DE_CONTROL` y `para_la_consulta` (H-01); `registrar_provisional`, `enviar` que exige y compara la provisional de F5 y toma de ahí la clase del fallo, `pendientes` y `enviar_pendientes` con `RECHAZOS_SIN_EFECTO` (H-02); `_por_tipo` y la comprobación de `disparador.qry_id` en `construir` (H-03). Las firmas de `construir` y `enviar` no cambian (`provisional_msg_id` admite None: el de F5), así que los scripts del revisor siguen funcionando |
| `bloque_a/11_Ejecutor/bloque_a/orquestacion.py` | En `consulta`: `enviar_pendientes` al empezar; en el `except` del RUN-, `if respuesta_final.para_la_consulta(...): raise` antes de escribir nada; `registrar_provisional` tras la provisional. En `ciclo`: `enviar_pendientes` al empezar, antes de numerar el RUN-. Se quita el `noqa: BLE001`, que ya no hace falta (el `except` relanza) |
| `bloque_a/11_Ejecutor/tests/test_t169_hallazgos_t162.py` (nuevo) | 28 pruebas (ver `pruebas.md`) |
| `bloque_a/11_Ejecutor/tests/test_t162_respuesta_final.py` | Tres ajustes por el diseño nuevo, ninguno más débil: el RUN- simulado de `test_ca3_un_run_bloqueado_o_sin_registro_da_sin_entrega` lleva el `disparador` que lleva el de verdad; `test_ca2_la_final_queda_en_f5_en_la_misma_qry` y `test_ca6_la_pregunta_repetida_no_cuenta_la_final` esperan tres entradas de la QRY- en F5 (provisional, registro, final) y comprueban además el `provisional_msg_id` |
| `bloque_a/11_Ejecutor/tests/mapa_plan_pruebas.json` | PB-07: dos pruebas más (integridad y final pendiente) y el texto de lo que comprueba |
| `docs/evidencias_pruebas_bloque_a.md` | Regenerado con `.docs/scripts/evidencias_plan_a.py --ejecutar` |
| `docs/incidencias.md` | INC-T169-01; nota en INC-T162-01 («Si el RUN- falla», acotado) |
| `sistema_global/seguimiento/Decisiones_del_operador_Bloque_A.md` | Una fila en §6 |
| `bloque_a/11_Ejecutor/README.md` | El punto de T-162 en §9 bis, ampliado |

### Decisiones tomadas y desviaciones del plan

Las de INC-T169-01, `[PROPUESTO]`:

- **Qué para la consulta:** los errores de control y cualquier fallo con el almacén roto según `verificar_integridad()`.
  - Se usa `PermissionError` y no una lista de clases, para no dejar fuera un control nuevo del almacén o de la mensajería.
  - Se comprueba la integridad porque un fallo de integridad llega como `ValueError` corriente.
  - Se relanza antes de la incidencia HERRAMIENTA, para que todo quede igual que en la base.
- **Finales pendientes:**
  - Se envían al empezar `consulta` y `ciclo`, las dos vías que propuso la coordinación.
  - Van con la fecha de su consulta, para que sean idénticas a las que habrían salido. `test_h02_la_final_recuperada_es_la_que_habria_salido` lo comprueba con una semana de diferencia: solo cambia el `timestamp`.
  - Una pendiente que la validación o la mensajería rechazan sin escribir nada se aparta una vez, para no bloquear el bloque. Las demás excepciones se propagan.
- **No se toca `contratos.py`:** el `msg_id` de la provisional no se reserva antes de crearla, porque eso exigiría cambiar `Mensajeria.crear`. Se registra justo después.

### Goldens

`tests/goldens_ct.py` sigue dando una sola diferencia, `formas_flujos_mock.json`. El generado con T-169 es **byte a byte el
mismo** que con T-162 (huella `6b7339b2…6c24`; diff exacto en `.docs/tickets/T-162/analisis-tecnico.md`). T-169 no añade nada a
los goldens porque en los flujos congelados no hay finales pendientes ni RUN- ajenos. `enviar_pendientes` sin pendientes no crea
mensajes ni identificadores, y la entrada nueva de F5 no entra en ningún golden.

### Límites conocidos

- Si el proceso muere entre crear la provisional y registrarla en F5 (la ventana de una escritura), la final no se puede
  enlazar y `pendientes` no la ve. Ese hueco ya existía en T-162 entre la final y su registro en F5.
- Una final apartada (`final_no_enviable`) solo la reenvía el operador (`respuesta_final.enviar`); no hay orden de la CLI para
  eso.
- `r01_01_sondas.py::test_s08_r8_desde_la_consulta_entera` documentaba H-02: afirmaba que F5 no guarda el `msg_id` de la
  provisional y por eso ahora falla, como se espera. Las dos `test_s02b_*` dan XPASS(strict), es decir, H-03 queda corregido. El
  resto de las sondas pasa.

### Comandos exactos para probarlo

```bash
cd bloque_a/11_Ejecutor
../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t169_hallazgos_t162.py tests/test_t162_respuesta_final.py
../../.venv/bin/python -m pytest -q -p no:cacheprovider -rX ../../.docs/tickets/T-162/revisores/r01_01_sondas.py   # s02b XPASS, s08 falla
../../.venv/bin/python tests/goldens_ct.py            # 1 diferencia, la de T-162
cd ../..
# mutantes del revisor contra las pruebas de T-169 y de T-162, en una copia desechable cuya ruta contenga «t169_mut»
mkdir -p <tmp>/t169_mut && tar --exclude=__pycache__ -cf - bloque_a | tar -x -C <tmp>/t169_mut && ln -s "$PWD/.venv" <tmp>/t169_mut/.venv
.venv/bin/python .docs/tickets/T-169/scripts/mutantes_t169.py .docs/tickets/T-162/revisores/r01_03_mutantes.py <tmp>/t169_mut M01 M02 M07 M11 M12 M16
```

## Ronda r02 (hallazgos de la QA r01 de T-169)

| Hallazgo | Causa | Cambio |
| --- | --- | --- |
| H-01 (media) | `enviar_pendientes` solo apartaba los rechazos; cualquier otro error de una pendiente (un `KeyError` de `construir` con un `escalado` sin `clases`) se propagaba al empezar cada `ciclo` y cada `consulta`, sin incidencia | Un segundo `except Exception` que relanza solo si `para_la_consulta` (integridad o control) y si no aparta con la incidencia escalada (`_apartar`, compartido con los rechazos). El `except` de los rechazos no cambia: con el almacén íntegro se apartan aunque `DatosSensibles` sea de control |
| H-02 (baja) | `ReplayFaltante` (respuesta no grabada en `--cliente replay --replay-modo reproducir`) se absorbía como FALLIDO | `ReplayFaltante` en `ERRORES_DE_CONTROL` (importado de `llm.py`, sin tocarlo) |
| H-03 (baja) | El apartado se escribía fuera de la transacción de `enviar`: cada hilo o proceso que veía la pendiente rechazada la apartaba y escalaba otra vez (3 de 8 hilos, 4 de 4 procesos) | Cada pendiente se envía o se aparta dentro de `with almacen._transaccion():` y, dentro, se vuelve a leer F5: si ya está apartada, se salta (la final ya enviada la devuelve `enviar` como repetida) |
| H-04 (baja) | Q02, Q03 y Q10 vivos | `tests/test_t169_r02.py`: dos pendientes en orden en la misma llamada, un rechazo con el sello de F2 roto a mitad del envío y la fecha de corte |

Archivos de la r02: `bloque_a/11_Ejecutor/bloque_a/respuesta_final.py`; `tests/test_t169_r02.py` (nuevo, 8 pruebas);
`tests/test_t169_hallazgos_t162.py` (la prueba que esperaba que un `RuntimeError` de una pendiente parase la consulta pasa a
comprobarlo con un error de control, `EscrituraFueraDeReserva`, que es lo que ahora para; el caso corriente lo cubre
`test_r02_h01_un_error_corriente_en_una_pendiente_no_para_la_consulta`); `.docs/tickets/T-169/scripts/mutantes_t169.py` (incluye
las pruebas de la r02, acepta una lista de mutantes sin bucle propio, como la del revisor de T-169, y añade Q02b–Q05b, Q09b y
R01–R04); `docs/incidencias.md` (INC-T169-01, ronda r02) y la fila de §6 de las decisiones. `orquestacion.py` no cambia en la r02.

Goldens: `formas_flujos_mock.json` generado sigue siendo byte a byte el de T-162 (huella `6b7339b2…`); ningún otro cambia.

Límite (nota p08 del revisor, sin hallazgo): si se reescribe en F5 la `provisional_msg_id` con otro `msg_id`, la final se enlaza a
ese; no hay un registro persistente de mensajes con que compararlo.

## Ronda de cierre (hallazgos de la QA r02 de T-169)

| Hallazgo | Causa | Cambio |
| --- | --- | --- |
| H-01 (baja) | `_apartar` escribía la marca `final_no_enviable` en F5 antes de pedir el INC-. Si la incidencia fallaba (por ejemplo, con `contadores.json` ilegible), la pendiente quedaba marcada, fuera de la lista y sin aviso | Se invierte el orden: primero `almacen.incidencia(...)` y después `almacen.escribir("F5", …)`. El detalle añade «puede haberse creado el mensaje; revisar antes de reenviar», por la nota `a08`: un fallo de F5 tras crear la final también se aparta |
| H-02 (baja) | Ninguna prueba del ticket cubría un error corriente con el almacén roto (S01 vivo) | Prueba de la sonda `a01`, parametrizada, y S01 en `PROPIOS` |
| H-03 (baja) | `docs/incidencias.md` y el README del ejecutor seguían con el texto de la r01 | Los dos textos de la QA, tal cual |

Archivos: `bloque_a/11_Ejecutor/bloque_a/respuesta_final.py` (solo `_apartar`); `tests/test_t169_r02.py` (5 pruebas nuevas y los
auxiliares `_romper_f2` y `_construir_que_lanza` de las sondas); `.docs/tickets/T-169/scripts/mutantes_t169.py` (S01);
`docs/incidencias.md`; `bloque_a/11_Ejecutor/README.md`. Copiados sin cambios de la copia del revisor: `qa.md` y `revisores/`
(`r02_01_sondas.py`, `r02_02_mutantes.py` y `r02_03_sondas.py`, nuevos).

Límite: si la incidencia sale y falla la marca, en el reintento se repite la incidencia (dos avisos al operador para una sola
pendiente). Se acepta así porque es el caso que la QA prefiere al de un apartado silencioso. No hay números nuevos.
