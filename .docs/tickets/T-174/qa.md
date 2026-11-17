# T-174 · QA independiente

- **Revisor:** claude (subagente nuevo, sin el contexto de la implementación) · **Ronda:** r01 · 2026-11-17
- **Base:** `wip/t174` (`c5b8287`) sobre develop `80751da`, en un worktree aparte; venv del proyecto; el CLI se lanzó con
  `python -c 'from bloque_a.cli import main; main()'` desde la copia (el `bloque-a` instalado apunta al árbol principal).

## Reproducción desde limpio

Por instrucción de la sesión coordinadora no se pasó la suite completa ni `check_all.sh`. Sí se ejecutó:

| Qué | Resultado |
| --- | --- |
| `pytest tests/test_t174_pb61_revision_c2.py tests/test_v51.py tests/test_fase4_mapa.py` | 44 passed |
| `python tests/goldens_ct.py` | «goldens de contratos: coinciden» |
| ruff con el comando del gate (los tres ejecutores) | 2808 en la rama, 2813 en la base: baja como declara |
| Ciclo mock por CLI (pasos de `pruebas.md`: enviar BLOQUEANTE, `ciclo` 06-05, `ciclo` 06-12, `responder`) | `tardia: true`, `revision_c2` RUN-2026-0003 ENTREGADA, revisa RUN-2026-0002, clases DIV. Una segunda respuesta idéntica: `revision_c2: null` |
| Regresión de un ciclo normal (NO_BLOQUEANTE + dos `ciclo`), base contra rama, F5 y salidas | En F5 solo cambia `supuestos_cns` en los dos RUN; los entregables solo difieren en las rutas de la carpeta de salida |
| Ataques propios: `revisores/r01_01_ataques.py` (19 casos) | 15 pasan, 4 fallan (H-01, H-02, H-03, H-04); A8 y A10 se leen en la salida (H-05, coste) |

## Contraste con el plan y el Documento 0

- **PB-61** (plan de pruebas, §PB-61): «la respuesta tardía que invalida el supuesto abre una revisión C2»; criterio: CNS- en
  `supuestos_declarados` con C19 OK y ningún dato del Broker inventado. Lo cubre la prueba integrada nueva más las tres previas
  del mapa. «Ningún dato inventado» depende del modelo real: bien dejado en «No comprueba».
- **Documento 0 V5.3, §7.9.5:** la respuesta tardía que invalida un supuesto entregado «se trata como petición de revisión (C2)
  y se comunica al Broker»: AD_HOC + CT-02, cumplido. **§7.9.4:** la NO_BLOQUEANTE «lo revisa al llegar la respuesta»: cubierto
  (CA-7). **Tabla de ciclos (C2):** «sin límite de número», así que no hay cuota de ciclos que respetar; la config tampoco la tiene.
- **Decisión «toda respuesta con texto invalida»:** razonable. El ejecutor no puede juzgar el texto sin un modelo, y el Anexo B
  no trae marca de confirmación. Falla hacia el lado caro (una revisión de más), no hacia el silencioso. Está declarada como
  `[PROPUESTO]` en INC-T174-01, con la mejora futura (marca de confirmación), y la deuda la referencia. Correcta.
- **Coste:** la revisión es un AD_HOC N2 con el presupuesto por RUN del Anexo A (en el ataque A10: 6,28 UC frente a 12,31 del
  C1 de RV). Observación O-1, sin hallazgo: una consulta de k preguntas contestada de una en una abre k revisiones. El Documento 0
  lo permite; agruparlas sería una mejora de coste.

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 | sí | `test_pb61_respuesta_tardia_…`; CLI (RUN-2026-0003, disparador CT-23) |
| CA-2 | sí | misma prueba (JSON, informe técnico, C19 OK, CT-02 espiado); CLI |
| CA-3 | sí | misma prueba; salida del CLI (`revision_c2`, `accion`). Nota: en F5 la clave es `revisiones_c2` (lista), como dice INC-T174-01; el README dice `revision_c2` |
| CA-4 | sí | `test_pb61_sin_informe_…`, `test_pb61_un_run_bloqueado_…`; A4 y A5 (BLOQUEADA, sin campo, PENDIENTE, minúsculas) |
| CA-5 | **parcial** | en secuencia sí (prueba propia, A1, CLI); **con dos procesos a la vez, no** (H-01) |
| CA-6 | **parcial** | PENDIENTE y FALLIDA, sí; el error de control se relanza, pero deja la revisión debida sin rastro (H-02) |
| CA-7 | sí | `test_pb61_no_bloqueante_…`, `test_pb61_informe_de_seguimiento_c6_…` |
| CA-8 | sí (lo medido) | mapa en verde, goldens coinciden, ruff 2808; suite completa y mypy no re-ejecutados por instrucción |

## Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | **alta** | `r01_01_ataques.py::test_a2_concurrencia_dos_respuestas_iguales`: dos `Bloque` sobre la misma carpeta de estado (dos procesos del ejecutor) responden a la vez la misma respuesta; la prueba solo ensancha con una espera la ventana que ya existe | Esperado: una revisión. Obtenido: **dos** (RUN-2026-0002 y RUN-2026-0003), es decir, dos AD_HOC completos y dos CT-02 al Broker por la misma respuesta | En `responder`, hacer la comprobación y la reserva de una vez bajo `with self.b.almacen._transaccion():` (el patrón de T-169, `respuesta_final.enviar`): releer `self._todas().get(cns_id)`, calcular `previos`, `nuevos` y `entregados`, y escribir la entrada CNS con `indices_respondidos` **y** la revisión reservada en `revisiones_c2` (`estado: "EN_CURSO"`, con `msg_id`). Lanzar `self.b.ciclo` fuera del cerrojo y escribir después el estado final de esa revisión (por `msg_id`). Prueba de regresión: A2 (exactamente un RUN con `disparador.origen == "CT-23"`) | abierto |
| H-02 | media | `test_a3_error_de_control_no_pierde_la_revision`: `ciclo` lanza `PermissionError` (error de control) | Esperado: se relanza y queda rastro de la revisión debida, que se puede reintentar. Obtenido: se relanza, pero `indices_respondidos` ya está escrito, no hay `revisiones_c2` ni incidencia, y una nueva respuesta no la reabre: **la revisión se pierde en silencio** | La reserva `EN_CURSO` de H-01 deja el rastro. Además: (a) en la rama que relanza, si el almacén está íntegro, anotar `estado: "INTERRUMPIDA"` con la clase del error antes del `raise`; (b) que `responder` (o un `revisiones_pendientes()`) vuelva a lanzar las revisiones `EN_CURSO`, `INTERRUMPIDA` o `PENDIENTE` de esa CNS- aunque no haya índices nuevos. Prueba: A3 | abierto |
| H-03 | media | `test_a7_alcance_no_amplia_lo_entregado`: la CNS- declara `["CRI", "IDX"]` y lo entregado analizó CRI y RV | Esperado: revisar solo lo entregado afectado (CRI). Obtenido: `clases: ["CRI", "IDX"]`, un análisis nuevo de IDX que ningún informe entregado llevaba, con su coste | En `_revision_c2`, calcular siempre `vistas` y usar `clases = sorted(set(c["clases"]) & vistas) if c.get("clases") else sorted(vistas)`. Prueba: A7 | abierto |
| H-04 | baja | `test_a9_respuesta_con_fecha_anterior_a_la_entrega`: respuesta con `as_of` 2026-06-05 y RUN entregado el 2026-06-12 | Esperado: a esa fecha no hay nada entregado (backtest sin mirar al futuro). Obtenido: revisa RUN-2026-0001 y lanza un AD_HOC fechado antes del informe que revisa | `_entregados_con(cns_id, as_of)` con `self.b.almacen.estado("F5", as_of, clave="id")`. Prueba: A9 | abierto |
| H-05 | baja | `test_a8_fallo_tras_escribir_el_run`: `ciclo` entrega y luego lanza `RuntimeError` | Esperado: estado coherente con F5. Obtenido: el RUN de la revisión está `ENTREGADA` (su CT-02 salió), pero la revisión queda `FALLIDA` y la `accion` no dice que llegó al Broker. Sin fuga R8: el texto del error no aparece ni en HA ni en F5 | En el `except`, si se encuentra `run_id`, tomar `estado` de la `entrega` de ese RUN en F5 y guardar la clase del error en `fallo`. Prueba: A8 con `rev["estado"] == "ENTREGADA"` | abierto |
| H-06 | baja | lectura de código: nada consume `revisiones_c2` en estado `PENDIENTE` o `FALLIDA` (`grep -rn revisiones_c2 bloque_a/`) | Esperado: una revisión que no se hizo llega al operador o se reintenta. Obtenido: la incidencia es de HERRAMIENTA sin `escalado_operador`, y el CLI no tiene un camino para relanzarla | Incidencia con `escalado_operador=True` y `tratamiento` («relanzar la revisión C2 de CNS-…»), más el reintento de H-02 (b). Si no se corrige aquí, pasa a la deuda con su ID | abierto |

Comprobado sin hallazgo: la repetición secuencial es idempotente (A1); una CNS- entrante, ajena o desconocida no abre nada (A4);
un RUN no entregado no cuenta (A5); las `respuestas` raras (índice negativo, flotante, cadena o NaN; texto vacío o None; sin texto;
lista vacía) no abren revisión (A6); el texto del Broker pasa por la mensajería, que rechaza credenciales antes de escribir en F5;
no hay LLM en la decisión de abrir; no hay números nuevos escritos a mano. El ciclo normal solo cambia `supuestos_cns`.

## Veredicto

**NO APTO** · H-01 (alta): la misma respuesta, procesada a la vez por dos ejecutores, abre dos revisiones C2 (dos AD_HOC y dos
CT-02). Lo demás cumple. Vuelve a `ri-implementar` para H-01 a H-05, cada uno con su prueba (los casos A2, A3, A7, A9 y A8 de
`revisores/r01_01_ataques.py` sirven de regresión). H-06 se corrige o pasa a la deuda. En la r02, el revisor vuelve a pasar
`r01_01_ataques.py` (y los añadidos `r02_*`), no solo las pruebas del implementador.

## Ronda r02

- **Revisor:** claude (subagente revisor, el mismo de la r01; no implementó) · 2026-11-17
- **Base:** `wip/t174` (`6fd2e82`) rebasada sobre develop `375d24b`, en un worktree nuevo. El CLI se lanzó desde la copia, y los
  guiones auxiliares con `PYTHONPATH` en la copia: sin él, `import bloque_a` carga el paquete instalado del árbol principal.

### Reproducción

| Qué | Resultado |
| --- | --- |
| `pytest tests/test_t174_pb61_revision_c2.py tests/test_v51.py tests/test_fase4_mapa.py` | 54 passed |
| `goldens_ct.py` | coinciden |
| ruff con el comando del gate | 2808 (cuota 2808); mypy no re-medido |
| `revisores/r01_01_ataques.py` (mis 20 casos de la r01) | 19 pasan. A8 falla porque espera FALLIDA y ahora sale ENTREGADA, que es justo la corrección que propuse en H-05: el caso de la r01 estaba mal escrito, no es una regresión |
| `revisores/r02_01_ataques.py` (5 casos nuevos) | B1, B2, B3 y B5 pasan como se esperaba; B4 falla (H-07) |
| Regresión de un ciclo normal (NO_BLOQUEANTE + dos `ciclo`), base `375d24b` contra rama | En F5 solo cambia `supuestos_cns` en los dos RUN; los entregables solo difieren en las rutas |
| CLI `consulta-broker revisiones` y `relanzar` (PENDIENTE preparada por API; muerte simulada en `relanzar`) | `revisiones` lista la PENDIENTE; `relanzar --cns` con una CNS- ajena no hace nada; tras la muerte, `revisiones` la lista EN_CURSO y `relanzar` sin la opción no la toca; `relanzar --incluir-en-curso --cns …` la entrega (RUN-2026-0002); el segundo `relanzar --incluir-en-curso` no repite nada. En HA: 0 avisos de la EN_CURSO (H-07) |

### Hallazgos de la r01

| ID | Estado | Evidencia |
| --- | --- | --- |
| H-01 | corregido | A2 pasa. Además, B1 (`relanzar_revisiones` y una respuesta repetida a la vez sobre una PENDIENTE) y B2 (dos `relanzar` a la vez sobre una FALLIDA): una sola revisión. B3 (dos respuestas distintas a la vez, índices 0 y 1): no se pierde ninguna, salen 2 revisiones ENTREGADA, `indices_respondidos` = [0, 1] |
| H-02 | corregido | A3 pasa: queda INTERRUMPIDA con una incidencia escalada y se relanza |
| H-03 | corregido | A7 pasa (la intersección); SIN_ALCANCE va con su incidencia escalada |
| H-04 | corregido | A9 pasa |
| H-05 | corregido | ENTREGADA desde F5 (A8 invertido, ver arriba) |
| H-06 | corregido | incidencia con `escalado_operador` y `tratamiento`; órdenes `revisiones` y `relanzar` (por la CLI, arriba) |

### Las dos desviaciones

1. **A8 ENTREGADA en vez de FALLIDA: correcta.** Es lo que pedía H-05: el RUN llegó al Broker por CT-02, así que su estado es
   el de la entrega. La clase del error queda en `fallo` y no se abre incidencia de «no llegó».
2. **Las EN_CURSO no se relanzan solas: correcta.** Una EN_CURSO puede estar viva en otro proceso, y el ciclo corre fuera del
   cerrojo. B5 lo confirma: con la revisión viva, `relanzar_revisiones(estados=("EN_CURSO",))` saca un segundo RUN. Por eso solo
   puede ser una orden expresa del operador, y la ayuda del CLI lo advierte. El riesgo que queda es la huérfana (H-07).

### Hallazgos nuevos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-07 | media | `r02_01_ataques.py::test_b4_en_curso_huerfana_se_detecta_y_se_avisa`: el proceso muere en mitad del ciclo de la revisión (`KeyboardInterrupt`, como un Ctrl-C, un SIGTERM convertido o un corte); luego otra instancia recibe la respuesta repetida y corre el ciclo de la semana siguiente. Lo mismo por la CLI | Esperado: la huérfana se detecta y se avisa al operador. Obtenido: queda EN_CURSO para siempre, sin incidencia (0 en HA). Ni `responder` ni el ciclo periódico la señalan; solo la ve quien ejecute `consulta-broker revisiones`. La revisión que se debe al Broker (§7.9.5) no sale y nadie lo sabe. Falla cerrado (no entrega nada falso), pero en silencio | 1) En `_reserva` (y al reclamar en `relanzar_revisiones`), guardar `proceso: {"host": socket.gethostname(), "pid": os.getpid()}`. 2) Un `huerfanas()` en `ConsultasBroker`: EN_CURSO del mismo host cuyo pid ya no existe (`os.kill(pid, 0)` lanza `ProcessLookupError`), o del pid actual que no esté en un conjunto en memoria de revisiones en marcha. Llamarlo al empezar `Bloque.ciclo` y en `revisiones_pendientes`. Por cada huérfana, una incidencia HERRAMIENTA con `escalado_operador=True` y `tratamiento` «consulta-broker relanzar --incluir-en-curso --cns …», una sola vez (marca `aviso_huerfana` en la revisión), y `huerfana: true` en la salida de `revisiones`. No hace falta ningún umbral de tiempo, así que no hay número nuevo. Prueba: B4 con `avisos` no vacío y una sola incidencia tras dos ciclos | abierto |
| H-08 | baja | Lectura de código y CLI: muerte en `relanzar` y después `relanzar --incluir-en-curso`; queda `intentos: 1` aunque hubo dos intentos | Esperado: antes de relanzar una EN_CURSO se comprueba si su RUN ya llegó a F5, y cada intento tiene su número. Obtenido: el intento solo se anota al terminar, así que el muerto y el siguiente llevan el mismo `disparador.intento`. Si el proceso murió después de entregar (el CT-02 ya salió), `--incluir-en-curso` saca una segunda revisión al Broker, y la búsqueda de H-05 por `msg_id` + `intento` puede tomar el RUN del intento muerto | 1) Al reclamar (`_reserva` y la reclamación en `relanzar_revisiones`), incrementar `intentos` dentro del cerrojo y pasar ese número al `disparador`. 2) En `relanzar_revisiones`, antes de lanzar una EN_CURSO o INTERRUMPIDA, buscar en F5 un RUN con `disparador.msg_id` igual: si su `entrega` es ENTREGADA, anotar ENTREGADA con su `run_id` sin lanzar otro ciclo. Prueba: muerte tras `orig(*a, **k)` dentro del ciclo, después `relanzar --incluir-en-curso`, y un solo RUN CT-23 | abierto |

Comprobado sin hallazgo en la r02:
- La reserva y la respuesta van en una sola entrada bajo el cerrojo.
- La reclamación en `relanzar_revisiones` relee dentro del cerrojo; el cerrojo es reentrante (`RLock` más `flock`, también entre instancias del mismo proceso).
- `responder` no relanza FALLIDA ni EN_CURSO; solo relanza INTERRUMPIDA y PENDIENTE.
- La incidencia lleva solo la clase del error (R8).
- No hay números nuevos ni LLM en la decisión.
- INC-T174-01 recoge la ronda r02 y la regla de las EN_CURSO.

### Veredicto r02

**APTO.** Los seis hallazgos de la r01 están corregidos y probados con los casos del revisor. Las dos desviaciones son correctas. No
queda ningún hallazgo crítico ni alto abierto, y los criterios CA-1 a CA-8 se cumplen. H-07 (media) y H-08 (baja) pueden
corregirse antes de integrar. Si no, pasan a la deuda técnica con su ID (T-174-H07 y T-174-H08), junto a la línea de T-174, al
cerrar. El cierre (estado CERRADO, diario, memoria, commit en develop y push) queda para la sesión coordinadora, como se pidió:
este commit es local.

## Ronda r03

- **Revisor:** claude (subagente revisor de la r01 y la r02; no implementó) · 2026-11-17
- **Base:** `wip/t174` (`73a0542`) sobre `6fd2e82`, en un worktree nuevo. El CLI y los guiones se lanzaron desde la copia, con
  `PYTHONPATH` en ella.

### Reproducción

| Qué | Resultado |
| --- | --- |
| Mutantes enteros, M0 a M28: `mutantes_t174.py bloque_a <copia>` | M0 (sin mutar) vive y los 28 mutantes mueren (M1 a M28); `vivos: []` |
| `pytest` de T-174, `test_v51`, T-162 (`test_t162_respuesta_final.py`), T-169 (`test_t169_hallazgos_t162.py`, `test_t169_r02.py`), el mapa, y mis `r01_01` y `r02_01` | 146 passed (r01_01 20/20, r02_01 5/5) |
| `goldens_ct.py` · ruff con el comando del gate | coinciden · 2808 |
| Regresión de un ciclo mock normal (NO_BLOQUEANTE + dos `ciclo`), base `375d24b` contra la r03 | En F5 solo cambia `supuestos_cns` en los dos RUN; mismas líneas en HA (9) y F3 (7): `huerfanas()` no escribe nada en un ciclo sin revisiones |
| CLI con el ciclo de la revisión matado con `os._exit` **antes** de entregar | `revisiones` la lista EN_CURSO con `huerfana: true` y su aviso; tras `revisiones` y un `ciclo` hay 1 solo aviso en HA; `relanzar` sin opción no la toca; `relanzar --incluir-en-curso` la entrega (intento 2); un solo RUN CT-23 |
| CLI con `os._exit` **después** de entregar (el CT-02 ya salió) | Igual hasta el aviso; `relanzar --incluir-en-curso` la da por ENTREGADA con el RUN del intento 1, sin lanzar otro ciclo; un solo RUN CT-23 (H-08 corregido) |
| `revisores/r03_01_ataques.py` (3 casos nuevos) | C3 (fork) pasa; C1 y C2 fallan (H-09 y H-10) |

### H-07 y H-08

| ID | Estado | Evidencia |
| --- | --- | --- |
| H-07 | corregido | B4 de la r02 pasa, y también por la CLI con `os._exit`: un solo aviso escalado aunque se vea en `revisiones` y en el ciclo |
| H-08 | corregido | CLI con `os._exit` tras entregar: no sale una segunda revisión. Los intentos se numeran al reclamar (2 tras un intento muerto); M27 y M28 mueren |

### Las preguntas de la coordinadora

1. **Mutantes M1 a M28:** todos mueren (arriba).
2. **Conjunto en memoria con varios Bloque y con fork:**
   - **Fork:** correcto (C3). El hijo hereda el conjunto, pero tiene otro pid, así que con el pid del padre consulta `os.kill` y,
     como el padre vive, no marca nada. El padre detecta su propia huérfana y avisa una vez.
   - **Varios Bloque en el mismo proceso:** dos huecos, los dos bajos (H-09 y H-10). En la CLI hay un proceso por orden, con un
     hilo y una carpeta, así que no se dan.
3. **Otro host o sin `proceso`:**
   - Queda sin aviso para siempre: `revisiones` la lista EN_CURSO sin decir que no se puede juzgar.
   - Está declarado en INC-T174-01 (ronda r03, «no se puede juzgar y no se marca») y en el docstring de `_es_huerfana`.
   - Pero no lleva `[PROPUESTO]` ni está en la deuda (H-11). «Sin `proceso`» solo afecta a estados anteriores a la r03, que no
     llegaron a develop.
   - Tampoco está declarada la reutilización de pid: un pid muerto que reutiliza otro proceso da un falso vivo (va en H-11).
4. **Ciclo CLI con `os._exit`:** correcto en los dos momentos (arriba).
5. **Regresiones:** ninguna (arriba).

### Hallazgos nuevos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-09 | baja | `r03_01_ataques.py::test_c1_ventana_entre_reserva_y_en_marcha`: con dos `Bloque` sobre la misma carpeta y en el mismo proceso, uno reserva la revisión EN_CURSO (bajo el cerrojo) y el otro llama a `huerfanas()` antes de que el primero entre en `_ejecutar_revision`. La prueba solo ensancha esa ventana, que ya existe | Esperado: la revisión está viva y no se marca. Obtenido: **falso huérfano**. Sale un aviso escalado que manda `relanzar --incluir-en-curso`, y si el operador lo obedece, se duplica la revisión. La ventana es de microsegundos y solo la ve otro hilo del mismo pid | Dar de alta la clave en `_EN_MARCHA` dentro del cerrojo, **antes** de escribir EN_CURSO: en `responder` (si `rev and ejecutar_revision`) y en la reclamación de `relanzar_revisiones`. Quitarla en un `finally` que cubra desde la reserva hasta el final de `_ejecutar_revision`, incluido el retorno SIN_ALCANCE y una excepción al escribir la reserva. `_ejecutar_revision` ya no la da de alta. Prueba: C1 | abierto (a la deuda) |
| H-10 | baja | `r03_01_ataques.py::test_c2_dos_carpetas_con_los_mismos_ids`: dos carpetas de estado en el mismo proceso, con los mismos ids (CNS-2026-0001 / MSG-2026-000006). X tiene una huérfana mientras Y ejecuta la suya | Esperado: la huérfana de X se marca. Obtenido: **falso vivo** (0 huérfanas), porque la clave del conjunto no incluye la carpeta. Al revés también: cuando la de X termine, la de Y podría verse huérfana. Solo pasa con pruebas o backtests con varias carpetas en un proceso | Clave `(str(Path(self.b.almacen.carpeta).resolve()), cns_id, msg_id)` en `_EN_MARCHA` y en `_es_huerfana`. Prueba: C2 | abierto (a la deuda) |
| H-11 | baja | Lectura de código y de INC-T174-01 (ronda r03) | Esperado: lo que no se puede juzgar se ve y queda como decisión pendiente. Obtenido: una EN_CURSO de otro host, o con el pid reutilizado, queda sin aviso para siempre. `revisiones` no dice que no se puede juzgar, y la decisión no lleva `[PROPUESTO]` ni tiene línea en la deuda | En `revisiones_pendientes`, añadir `huerfana: None` («no se puede juzgar desde este host») a las EN_CURSO de otro host o sin `proceso`. Marcar el punto de INC-T174-01 como `[PROPUESTO]`, añadir la reutilización de pid, y abrir una línea en la deuda: un despliegue en varios hosts necesita un latido con plazo, y el plazo saldría del Anexo A (hoy no existe; no se inventa) | abierto (a la deuda) |

### Veredicto r03

**APTO.**
- H-07 y H-08 están corregidos, también por la CLI con `os._exit`.
- Los 28 mutantes mueren, y no hay regresiones en T-174, `test_v51`, T-162/T-169 ni en el ciclo mock.
- No queda ningún hallazgo crítico, alto ni medio abierto.

H-09, H-10 y H-11 son bajos y pasan a la deuda técnica con su ID (fila «T-174 · QA r03» del documento de deuda). Ticket
CERRADO. El diario, la memoria, el commit en develop y el push quedan para la sesión coordinadora; este commit es local.

## Ronda de cierre

- **Revisor:** claude (subagente revisor de las rondas r01 a r03; no implementó) · 2026-11-17
- **Base:** `wip/t174` (`3ed78aa`) sobre mi `16c6423`, en un worktree nuevo. El CLI y los guiones se lanzaron desde la copia, con
  `PYTHONPATH` en ella.
- **Regla del operador:** los bajos se subsanan en el mismo ticket, no en la deuda. Por eso se retiró la fila «T-174 · QA r03» que
  abrí en la r03.

### Reproducción

| Qué | Resultado |
| --- | --- |
| Mutantes enteros, M0 a M33 (`mutantes_t174.py bloque_a <copia>`) | M0 (sin mutar) vive y los 33 mutantes mueren, también M29 a M33 de esta ronda; `vivos: []` |
| `pytest` de T-174, `test_v51`, T-162, T-169 (las dos), el mapa y todos los de `revisores/` (r01_01, r02_01, r03_01) | 125 passed: C1, C2 y C3 de la r03 pasan |
| `goldens_ct.py` · ruff y mypy A con los comandos del gate | coinciden · 2808 (cuota 2808) · 109 (cuota 109) |
| CLI con el ciclo de la revisión matado con `os._exit` **antes** de entregar | `revisiones`: EN_CURSO, `huerfana: true`, con aviso; tras un `ciclo`, 1 solo aviso en HA; `relanzar` sin opción no la toca; `relanzar --incluir-en-curso` la entrega (intento 2); `revisiones` queda vacía; un solo RUN CT-23 |
| CLI con `os._exit` **después** de entregar | Igual hasta el aviso; `relanzar --incluir-en-curso` la da por ENTREGADA con el RUN del intento 1, sin lanzar otro ciclo; un solo RUN CT-23 |
| CLI con la EN_CURSO anotada como de otro host (`_anotar_revision`, almacén íntegro) | `revisiones`: `huerfana: null`, «no se puede juzgar desde este host»; tras un `ciclo`, 0 avisos |

### H-09 a H-11

| ID | Estado | Evidencia |
| --- | --- | --- |
| H-09 | corregido | El alta en `_EN_MARCHA` se hace bajo el cerrojo, antes de escribir la reserva (en `responder`) o la reclamación (en `relanzar_revisiones`). La baja va en un `finally` que cubre desde la reserva hasta el final, incluidos SIN_ALCANCE y un fallo al escribir. C1 pasa; M29 y M30 mueren |
| H-10 | corregido | La clave es `(carpeta resuelta, cns_id, msg_id)`, en el alta y en `_es_huerfana`. C2 pasa; M31 muere |
| H-11 | corregido | `_es_huerfana` devuelve True, False o None; None no abre aviso y sale en `revisiones` con su nota (comprobado por la CLI). INC-T174-01 lleva `[PROPUESTO]`, con la reutilización de pid y el límite de varios hosts declarados (el plazo del latido tendría que salir del Anexo A). M32 y M33 mueren |

Comprobado además sin hallazgo:
- `huerfanas()` vuelve a mirar dentro del cerrojo con el mismo juicio, así que no avisa de una que otro proceso acaba de reclamar.
- La revisión que se está ejecutando no se ve huérfana desde su propio ciclo AD_HOC.
- Sin revisiones, el ciclo normal no escribe nada nuevo.

### Veredicto final

**APTO.** Los hallazgos H-01 a H-11 de las rondas r01 a r03 están corregidos y probados con los casos del revisor. No queda
ninguno abierto, de ninguna gravedad. Los criterios CA-1 a CA-8 se cumplen, y las cuotas y los goldens no cambian. Ticket
CERRADO. El diario, la memoria, el commit en develop y el push quedan para la sesión coordinadora; este commit es local.
