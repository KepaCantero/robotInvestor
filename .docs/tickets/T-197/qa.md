# T-197 · QA

## Ronda r01 · 2026-11-24 · revisor: claude (subagente sin el contexto de la implementación)

**Veredicto: NO APTO** (3 medios y 3 bajos; ningún alto ni crítico).

Copia revisada: `wip/t197` (47a4316) sobre `origin/develop` 6045913, en un worktree propio (sin tocar la copia del
implementador). Plan: PB-09 del Plan de pruebas V3.0; especificación de HT-05 (`bloque_a/10_Herramientas/ht05_planificador_ejemplo.md`).

### Qué se reprodujo

| Comprobación | Resultado |
| --- | --- |
| `test_t197_periodicidad.py` + `test_t87_contratos.py` + `test_integracion.py` | 43 superadas |
| Sin el cambio (el `orquestacion.py` de 6045913, HT-05 y planificador nuevos) | 9 fallan: las 5 de CA-1, `proximo`, las 2 de CA-3 y la de `test_t87`; sin `planificacion_c1.py` el módulo no se recoge |
| `mutantes.py` del ticket | 32 muertos de 32 |
| Mutantes del revisor (`revisores/r01_02_mutantes.py`) | 4 muertos de 17; 12 vivos no equivalentes (H-03, H-06) y 1 equivalente (R4: el adelanto es siempre mayor que 0, así que la entrega nunca cae en el instante de la ejecución) |
| Ataques del revisor (`revisores/r01_01_ataques.py`, 35 casos) | 28 superados; fallan A1, A2 (H-01), A3 ×3 (H-04) y A9 (H-02) |
| Cuatro **procesos** de verdad (`spawn`) sobre el mismo estado (A4) | un solo EMITIDO y tres DESCARTADO_DUPLICADO; un solo C1. La prueba del ticket usa hilos con cuatro `Bloque`; el `flock` también cubre procesos |
| CLI de punta a punta con el cliente simulado (A5) | `planificar` sin `--ejecutar` no escribe; con `--ejecutar` dispara un RUN- real; la segunda vez, duplicado. Funciona, pero no hay prueba del ticket que lo ate (H-03) |
| Calendarios en los bordes (A6): quincenal dos años seguidos, con la semana 53 de 2026; coherencia de `siguiente`/`ultima` en cuatro periodicidades; ninguna ejecución entre las 02:00 y las 03:00 para todas las entregas posibles | superados |
| Valores hostiles (A8): P-01 no texto, partes de más, minúsculas, sin espacios, 24:00, salto de línea; CT-04 con `None`, lista, número, minúsculas | fallan cerrado sin tocar F10 |
| Fusión con `origin/astra/encargos-bloque-a-c38-c47` (T-189, PR 3), árbol de `git merge-tree` | el código (`orquestacion.py`, `cli.py`, `por_defecto.yaml`, `mapa_plan_pruebas.json`) se fusiona sin conflicto y sin choque de lógica: T-189 añade sus `continue` en la rama `horizontes` y T-197 solo toca la rama P-01 y la línea del valor. En el árbol fusionado, `test_t197`, `test_t189_controles`, `test_t87` y `test_fase4_huecos`: 85 superadas. Chocan `cola_astra.md`, la deuda, `docs/incidencias.md` **y también `docs/evidencias_pruebas_bloque_a.md`** (H-05) |
| ruff y mypy de los ficheros tocados | ningún hallazgo nuevo de ruff (el de `fechas_ciclo` ya estaba en develop); gate: ruff 2807 y mypy A 102, en sus cuotas |
| Gate del implementador (`gate2.log`) | 12/12. «8377 superadas de 8379 recogidas»: las 2 que faltan son **2 omitidas**, `test_t149.py::test_h01_series_distintas_en_otras_rejillas_no_son_copias` (`pytest.skip` «paso del orden del 1 % del precio: límite declarado», con paso 1/8 y 1/4 a nivel 12). Las mismas 2 que develop omite desde T-149; ningún fallo oculto. `pruebas.md` no lo dice (H-05) |

### Los puntos que pidió la coordinación

1. **Formato del P-01.** No rompe a ningún lector. En el paquete solo leen P-01 el CT-04 (`decision`) y el planificador nuevo; nada del Broker (bloque B), de los prompts ni de los esquemas JSON lo lee. El esquema de F10 (Markdown, V3.0, tabla 4.3) da el valor en texto libre («Semanal; ejecución el sábado, entrega el lunes 07:00»), así que admite el nuevo. El cambio **unifica** el formato: en develop el F10 inicial ya era de tres partes y el CT-04 escribía dos. El cambio de `test_t87` es legítimo y no debilita la prueba: sigue comparando la cadena exacta, antes y después de la fecha de efecto, y con los rechazos; y la nueva cadena comprueba además la ejecución deducida (MAR 12:00 − 49 h = DOM 11:00).
2. **Los números.** 49 h (§4, «la ejecución se adelanta automáticamente 49 horas»), 02:00–03:00 (§2) y 24 h (§5.2) salen de la especificación de HT-05. Las 2 h de la diaria no las dice el texto; se deducen de la fila de §4 (05:00 → 07:00). Están en INC-T197-01 [PROPUESTO], igual que el adelanto de la quincenal y la mensual y el redondeo hacia abajo. Ninguno está en el Anexo A ni escrito en el código: todos salen de `planificador` en `por_defecto.yaml`. Matiz: el comentario del YAML solo marca como [PROPUESTO] la quincenal y la mensual. Se corrige en H-05.
3. **«Superada».** Es honesto, una vez se corrijan H-01 a H-03. El criterio dice «Siguiente C1 disparado en la nueva fecha; ningún otro parámetro modificado». HT-05 es, según su propia especificación (§3), un juego de expresiones cron con `CRON_TZ`. Que lo lance el cron del sistema cada hora es una forma legítima de implementarlo, y quién lo despierta es tiempo real (cláusula motivada). La decisión del disparo, la fecha nueva, la idempotencia y la recuperación están implementadas y probadas. C1-ENTREGA no forma parte del criterio de PB-09 (ni de su «Resultado esperado»), y el `no_comprueba` lo declara. Pero la evidencia afirma que «`bloque-a planificar --ejecutar` lo dispara» sin ninguna prueba que pase por esa orden (H-03).
4. **Fechas y relojes.** La quincenal no usa la paridad ISO, que se rompe en 2026, un año de 53 semanas, sino semanas contadas desde el ancla: comprobado durante dos años, siempre cada 14 días. El cambio de hora no afecta, porque ninguna ejecución puede caer en la franja de 02:00 a 03:00 y la CLI calcula «ahora» en `zona_horaria` (Europe/Madrid) y quita la zona, sea cual sea la del servidor o la del cron. Dos huecos: la entrega sí puede caer en la franja (H-04), y el margen de 24 h es de reloj de pared (23 o 25 h reales el día del cambio, sin efecto práctico; se deja como observación).
5. **Cuatro bloques a la vez.** Solo dispara uno, también con procesos reales (A4). Pero si el proceso que disparó muere dentro del ciclo, el disparo queda huérfano para siempre y nadie lo sabe (H-02).
6. **Astra (T-189).** Sin choque de código ni de lógica, y las pruebas de las dos ramas pasan en el árbol fusionado. La lista de ficheros en conflicto de `pruebas.md` está incompleta (H-05).

### Hallazgos

**H-01 · media · La quincena se reinicia con cualquier CFG- de P-01: un cambio de hora o un CT-04 repetido dan dos C1 en 7 días.**
- Cómo reproducirlo: `revisores/r01_01_ataques.py::test_a1…` y `::test_a2…`. Con QUINCENAL desde el 03-06, el C1 sale el 08-06. El martes 09-06 el Broker retrasa la entrega a MIE 09:00, o repite el mismo CT-04 sin cambiar nada. Siguiente C1 esperado: 22-06 (14 días). Obtenido: 15-06 (7 días).
- Causa: `_p01_en` toma `inicio` = `fecha_efecto` del último CFG- y `_ancla` vuelve a anclar en la primera ejecución desde esa fecha. Además, el CT-04 escribe un CFG- aunque el valor no cambie. La especificación guarda el ancla como dato propio del planificador (`semana_ancla_quincenal`, §4 y §6): no lo mueve cualquier cambio de la hora.
- Corrección: (a) el CT-04 no escribe un CFG- de P-01 cuando el valor compuesto es igual al vigente: lo anota en el RET- como «sin cambio» y no lo cuenta como aplicado. (b) Si la periodicidad nueva y la vigente son QUINCENAL, el ancla se conserva: el CFG- lleva `semana_ancla_quincenal`, el lunes de la semana ancla, copiado del vigente, y `_p01_en` y `es_dia_de_ejecucion` anclan en ese lunes. Solo al pasar de otra periodicidad a la quincenal se ancla en la primera ejecución. Hay que declararlo en INC-T197-01.
- Prueba de regresión: A1 y A2 en `test_t197_periodicidad.py`, más un cambio de día de la entrega (MIE → JUE: el siguiente C1 es el martes 23-06, de la misma quincena).

**H-02 · media · Disparo huérfano: si el proceso muere dentro del ciclo, el C1 se pierde en silencio y la salida es la de un duplicado normal.**
- Cómo reproducirlo: `revisores/r01_01_ataques.py::test_a9…`. Un proceso real cuyo ciclo hace `os._exit(9)` (OOM, `kill -9`, reinicio). En F5 queda `C1-EJEC-2026-05-30T06:00` EMITIDO, sin `run_id` ni `estado_run`. El `finally` no corre, y cada sondeo siguiente responde `DESCARTADO_DUPLICADO` con `registrado: EMITIDO`, igual que cuando todo fue bien. Ni HA ni la salida dicen que el C1 de esa semana no se hizo (C1-CONTROL no existe). CA-5 dice «un ciclo cortado queda FALLIDO», y eso no se cumple para el corte más habitual.
- Corrección: la reserva DISPARO guarda `pid` (como las C4- de T-177). En `disparar`, un previo sin `estado_run` cuyo `interfaz_broker._pid_vivo(pid)` es False se cierra una sola vez con `estado_run: FALLIDO` y el motivo «proceso terminado», y deja una incidencia Operativa en HA. La salida es `estado: FALLIDO` (o `HUERFANO`), no DESCARTADO_DUPLICADO. El C1 no se repite solo (lo lanza el operador con `ciclo`, como ya dice INC-T197-01). Si el pid está vivo, la salida es `EN_CURSO`.
- Prueba de regresión: A9, con un proceso real que muere; y otra con el pid vivo (el propio proceso de la prueba), que devuelve EN_CURSO sin escribir nada.

**H-03 · media · La orden `bloque-a planificar [--ejecutar]` no tiene ninguna prueba, y la evidencia la cita como lo que dispara el C1.**
- Cómo reproducirlo: `revisores/r01_02_mutantes.py R1 R2`. Con `ejecutar=True` fijo, el modo «solo informa» dispara ciclos reales; con `ejecutar=False` fijo, el cron nunca dispara. Los dos mutantes quedan vivos con todas las pruebas de PB-09. El `mapa_plan_pruebas.json` y las evidencias afirman que «`bloque-a planificar --ejecutar` lo dispara».
- Corrección: añadir a `test_t197_periodicidad.py` una prueba que llame a `bloque_a.cli.main([...,"--as-of","2026-05-30T06:10","planificar"])` con `orquestacion.Reloj` sustituido. Tiene que comprobar que esa llamada da PENDIENTE sin ninguna entrada DISPARO, que con `--ejecutar` da EMITIDO con un RUN-, y que la segunda llamada da DESCARTADO_DUPLICADO (en `revisores/r01_01_ataques.py::test_a5…` está hecha como subproceso). Hay que citarla en el mapa de PB-09.
- Prueba de regresión: esa misma; R1 y R2 tienen que morir.

**H-04 · baja · La entrega puede caer en la franja sin disparos.**
- Cómo reproducirlo: `revisores/r01_01_ataques.py::test_a3…`. «DOM 02:30», «LUN 02:00» y «MIE 02:59» se aplican: «SEMANAL · VIE 01:00 · entrega DOM 02:30». El §2 dice «Ningún disparo se programa entre las 02:00 y las 03:00» y C1-ENTREGA es un disparo de §3. El último domingo de marzo, esa entrega no existe.
- Corrección: `ejecucion_para_entrega` también rechaza (`P01Invalido`) una entrega cuya hora cae en `franja_sin_disparos_h`, y el CT-04 la rechaza con su motivo sin tocar F10.
- Prueba de regresión: los tres casos de A3 en `test_ca1_rechaza_lo_que_ht05_no_puede_programar_sin_tocar_f10`.

**H-05 · baja · Documentación del ticket.**
- `pruebas.md` dice que, además de `cola_astra.md` y la deuda, en la fusión con la rama de Astra solo choca `docs/incidencias.md`. También choca `docs/evidencias_pruebas_bloque_a.md` (`git merge-tree --write-tree wip/t197 origin/astra/encargos-bloque-a-c38-c47`). Hay que corregirlo y decir cómo se resuelve: se regenera con `evidencias_plan_a.py --ejecutar` después de fusionar, no a mano.
- `pruebas.md` dice «8377 superadas de 8379 recogidas» y no aclara que las 2 son las omitidas de `test_t149.py:126`, el límite declarado de T-149, las mismas que en develop.
- El comentario de `planificador` en `por_defecto.yaml` marca como [PROPUESTO] solo la quincenal y la mensual. Las 2 h de la diaria y el redondeo hacia abajo también lo son (INC-T197-01).
- Prueba de regresión: no hace falta (documentación); en la ronda de cierre se comprueba con `git merge-tree`.

**H-06 · baja · Mutantes vivos, no equivalentes, de cláusulas sin prueba que las ate** (`revisores/r01_02_mutantes.py`). El código hoy es correcto en todos estos casos; falta la prueba. Una prueba por mutante:
- R3 (`dia < f < c.date()`): un CT-04 el viernes 05-06 con efecto el sábado 06-06, el día del C1 semanal antiguo. `proximo` del viernes tiene que dar la ejecución nueva, no «2026-06-06T06:00».
- R6 (`t > entrega`): disparo justo a la hora de la entrega → RECUPERADO. Hay que fijar el borde declarado en INC-T197-01.
- R7 (`dia.day < 7`): una mensual cuyo sábado es el día 7 (sábado 07-11-2026) se ejecuta ese día.
- R8 (`< hasta`): `disparar` a la hora exacta, a las 06:00 (el cron con `0 * * * *`), tiene que dar EMITIDO y no SIN_DISPARO o el C1 anterior.
- R9 (entrega diaria con día de la semana): una ejecución DIARIA del martes con P-01 «DIARIA · LUN 05:00 · entrega LUN 07:00» entrega el martes a las 07:00, no el lunes siguiente.
- R10 (F10 leído sin `as_of`): en una simulación, un CT-04 escrito después de `ahora` no cambia el C1 que se calcula en `ahora`.
- R11 (sin segundos a cero): con «entrega + 24 h + 30 s» el disparo es RECUPERADO; los segundos no cuentan.
- R14 (`<= 0`): diaria con entrega a las 02:00 → ejecución a las 00:00 admitida. Cuidado con H-04: usar otra franja en la configuración de la prueba.
- R15 (el planificador con un P-01 de dos partes): con «QUINCENAL · MIE 08:00» en F10, escrito por un CT-04 anterior a T-197, el C1 sale el lunes 07:00, no el sábado 06:00.
- R16 (sin `fijar_fecha`): la entrada DISPARO de F5 lleva como `_fecha` el día del disparo.
- Prueba de regresión: las diez anteriores. Los mutantes R3, R6 a R11 y R14 a R16 tienen que morir.

### Observaciones (no son hallazgos)

- Los DESCARTADO_DUPLICADO no se escriben en F5, en contra de la letra de §5.4. Está declarado en INC-T197-01 y es razonable: con el sondeo horario, cada sondeo sería una línea.
- Margen de 24 h de reloj de pared el día del cambio de hora (23 o 25 h reales): sin efecto práctico.
- `bloque-a --as-of …+02:00 planificar` termina con una traza (`ValueError` «sin zona»). Falla cerrado, sin escribir nada.

### Invariantes

Números solo de la configuración, con [PROPUESTO] en INC-T197-01 (salvo el matiz del comentario, H-05). Corpus y esquemas congelados intactos (gate corpus-integridad en verde; el diff no toca el corpus). R8: los DISPARO solo llevan identificadores, el P-01 y fechas. No hay LLM en la ruta del planificador. Falla cerrado ante un P-01 ilegible, un instante con zona o un ciclo que se corta (salvo la muerte del proceso, H-02). Ninguna prueba antigua debilitada. El ciclo mock y el backtest no cambian por construcción: el diff de `orquestacion.py` solo cambia el CT-04 y pone la constante del P-01 inicial, con la misma cadena. Cuotas: ruff 2807, mypy A 102.

### Ronda de cierre

Volveré a ejecutar `revisores/r01_01_ataques.py` (los 35 casos tienen que pasar) y `revisores/r01_02_mutantes.py` (todos muertos salvo R4, equivalente), además de `mutantes.py`. Repetiré la fusión con la rama de Astra y leeré el log del gate.

## Ronda r02 · 2026-11-24 · revisor: claude (el mismo de la r01)

**Veredicto: APTO pendiente de ronda de cierre.** Quedan 2 hallazgos bajos nuevos, H-07 y H-08; ninguno medio ni alto. Los seis de la r01 están corregidos. La ronda de cierre la verifico yo.

Copia revisada: `wip/t197` 2512a133 (encima de 47a4316), en mi worktree. Mi `qa.md` y mis `revisores/` de la r01 llegan intactos en el commit, idénticos a los míos. Script nuevo de esta ronda: `revisores/r02_01_ataques.py`. Los de la r01 no se tocan.

### Reproducción

| Comprobación | Resultado |
| --- | --- |
| `test_t197_periodicidad.py` (35) + `test_t87_contratos.py` + `test_integracion.py` | 60 superadas |
| `revisores/r01_01_ataques.py` | 35 de 35 |
| `revisores/r01_02_mutantes.py`, en una copia de 2512a133 | 16 muertos de 17; vivo solo R4, equivalente |
| `mutantes.py` del ticket (58), en la misma copia | 58 muertos de 58 |
| `revisores/r02_01_ataques.py` (12) | 10 superados; fallan B2 (H-07) y B3 (H-08) |
| Fusión con `origin/astra/encargos-bloque-a-c38-c47` (sin cambios desde la r01, 2d99af6). Árbol de `git merge-tree`: 052539258f | el código se fusiona sin conflicto; chocan `cola_astra.md`, la deuda, `incidencias.md` y `evidencias_pruebas_bloque_a.md`, como ya dice `pruebas.md`. En el árbol fusionado, `test_t197`, `test_t189_controles`, `test_t87` y `test_fase4_huecos`: 102 superadas |
| Fusión con `origin/develop`, que avanzó a b9ce786 (T-194) | solo choca `docs/incidencias.md`: las dos ramas añaden al final y se resuelve conservando las dos entradas. Hay que tenerlo en cuenta al llevarlo a develop |
| Gate del implementador (`gate_t197_r02.log`) | 12/12. pytest A da 8394 superadas y las mismas 2 omitidas de `test_t149.py`. Ruff 2807 y mypy A 102, en sus cuotas |

### Las correcciones, una a una

- **H-01 · corregido.** Un CT-04 con el P-01 compuesto igual al vigente no escribe CFG- y lo anota en `aplicado_en_f10.sin_cambio`. Todo CFG- de P-01 lleva `semana_ancla_quincenal`, que se copia de QUINCENAL a QUINCENAL. A1 y A2 pasan. B4 pasa: con un CT-04 que cambia P-02 y repite P-01, se aplica P-02 y P-01 queda como sin cambio, con un solo CFG-. B5 pasa: una quincenal escrita antes de la r02, sin el campo, conserva la quincena de su primera ejecución. Que un cambio del día de la entrega dé un intervalo distinto de 14 días (LUN → MAR: 15 días) es inherente a mantener la paridad de la semana, igual que la guarda ISO de §4. No es hallazgo.
- **H-02 · corregido, con una desviación que no acepto tal cual (H-08) y un caso que queda sin cubrir (H-07).** Sobre la desviación del cierre en `cierre_huerfano.estado_run`: se debe a una aserción mía de la r01. A9 leía F5 después del sondeo y pedía que no hubiera `estado_run`. Era una descripción del fallo, no una especificación, y el error es mío. El cierre del huérfano tiene que leerse igual que el del ciclo cortado (H-08). La aserción `"estado_run" not in f5` de `r01_01_ataques.py::test_a9` queda sustituida por `r02_01_ataques.py::test_b3`. Sobre el cambio de la prueba de concurrencia: es legítimo y no la debilita. Ahora espera a que los otros tres sondeen con el C1 todavía abierto (antes era cuestión de tiempos), comprueba que dan EN_CURSO y, después, DESCARTADO_DUPLICADO; sigue exigiendo un solo C1 y una sola reserva.
- **A4 según el orden de llegada (lo que pidió la coordinación).** Con cuatro procesos reales, cuatro rondas con un C1 instantáneo y cuatro con uno de 3 s (B1, 8 casos): siempre un EMITIDO y un solo C1. Los demás procesos dan EN_CURSO si llegan con el C1 abierto (los 3 con el C1 lento) o DESCARTADO_DUPLICADO si llegan con él cerrado. Nunca un FALLIDO ni una incidencia de huérfano falsa, y F5 termina con `estado_run` COMPLETO. La etiqueta depende del orden, como debe ser; el resultado, no. A4 de la r01 pasa porque, con su C1 instantáneo, los otros llegan cuando ya está cerrado.
- **H-03 · corregido.** `test_r02_h03_orden_planificar_de_la_cli` pasa por `cli.main`, y R1 y R2 mueren.
- **H-04 · corregido.** La entrega entre las 02:00 y las 03:00 se rechaza (tres casos en la prueba de rechazos); A3 pasa.
- **H-05 · corregido.** `pruebas.md` cita las cuatro fuentes de conflicto con la rama de Astra y explica que las 2 que faltan son omitidas; el YAML marca como [PROPUESTO] las 2 h, el redondeo y el borde de las 24 h, igual que INC-T197-01.
- **H-06 · corregido.** Hay una prueba por cada mutante vivo de la r01; todos mueren salvo R4, que es equivalente.
- **Invariantes.** No hay números nuevos: el `pid` no es un parámetro. No cambian esquemas ni corpus (los goldens de los contratos coinciden, según `pruebas.md`; el gate da el corpus en verde). La salida del CT-04 gana `sin_cambio`, que no está en ningún esquema congelado. Ninguna prueba antigua debilitada.

### Hallazgos nuevos

**H-07 · baja · Si otro proceso reutiliza el pid de la reserva, el disparo huérfano se queda EN_CURSO.**
- Cómo reproducirlo: `revisores/r02_01_ataques.py::test_b2…`. Una reserva abierta que dejó otro arranque con el mismo pid que el proceso que sondea (tras reiniciar un contenedor los pid vuelven a empezar), o con el pid de un proceso cualquiera que ahora vive, da EN_CURSO. Mientras dure ese proceso no hay FALLIDO ni incidencia en HA, y si el pid es el de un servicio que no termina, no los hay nunca: vuelve el C1 perdido en silencio de H-02. Es baja porque el pid tiene que coincidir. Es la misma limitación que se aceptó en T-177, pero allí no se pierde un C1.
- Corrección: la reserva guarda, además del `pid`, la identidad del arranque del proceso: `boot_id` de `/proc/sys/kernel/random/boot_id` y la hora de arranque del proceso (campo 22 de `/proc/<pid>/stat`). Está vivo solo si las dos coinciden. Si no se pueden leer (fuera de Linux), el resultado es None, como ahora. Además, una reserva con el pid propio que este proceso no abrió (un conjunto de los `disparo_id` abiertos en el módulo) cuenta como muerta. Hay que declararlo en INC-T197-01.
- Prueba de regresión: B2, y otra con el pid de un proceso vivo ajeno con otra hora de arranque, que también da FALLIDO.

**H-08 · baja · El huérfano cerrado no se lee igual que el ciclo cortado.**
- Cómo reproducirlo: `revisores/r02_01_ataques.py::test_b3…`. Tras el cierre, F5 tiene `cierre_huerfano.estado_run = FALLIDO`, pero el `estado_run` de la entrada queda en None. Un ciclo cortado deja `estado_run` FALLIDO arriba. Quien lea F5 (el operador, una futura C1-CONTROL) tiene que mirar dos sitios distintos para saber lo mismo.
- Corrección: el cierre escribe `estado_run: "FALLIDO"` y `motivo_cierre: "proceso terminado"` en el nivel de arriba (`cierre_huerfano` puede quedar como detalle). `_previo` deja de comprobar `cierre_huerfano` para decidir si está abierto, y `test_r02_h02_proceso_muerto…` comprueba `f5["estado_run"] == "FALLIDO"`.
- Prueba de regresión: B3.

### Ronda de cierre

Volveré a ejecutar `r01_01_ataques.py` (salvo la aserción de A9 sustituida por B3), `r01_02_mutantes.py`, `r02_01_ataques.py` (12 de 12) y `mutantes.py`, repetiré la fusión con la rama de Astra y con develop, y leeré el log del gate.

## Ronda de cierre de la r02 · 2026-11-24 · revisor: claude

**Veredicto: APTO pendiente de una segunda ronda de cierre. Sigue habiendo algo abierto.** H-07 y H-08 están corregidos y no hay regresiones. Pero mis mutantes de la corrección de H-07 descubren dos huecos de prueba nuevos, los dos bajos (H-09 y H-10). El código es correcto en los dos casos; lo que falta es la prueba que los ate.

Copia revisada: `wip/t197` 1cd14ec4 (encima de 2512a133). Mi `qa.md` y mis `revisores/` llegan intactos en el commit. Scripts nuevos o tocados en esta ronda:
- `revisores/r02_02_mutantes_cierre.py`, nuevo.
- `revisores/r01_01_ataques.py`: se cambia solo la aserción de A9 que la r02 ya había sustituido por B3. Ahora pide `estado_run` FALLIDO tras el sondeo, con un comentario que lo explica.

### Reproducción

| Comprobación | Resultado |
| --- | --- |
| `test_t197_periodicidad.py` + `test_t87_contratos.py` | 48 superadas |
| `revisores/r01_01_ataques.py` (con A9 corregida) + `revisores/r02_01_ataques.py` | 47 de 47 (35 + 12). B1 (cuatro procesos, cualquier orden, C1 instantáneo o lento) sigue con un solo C1 y sin ningún huérfano falso; B2 y B3 pasan |
| `mutantes.py` del ticket (65), en una copia de 1cd14ec4 | 65 muertos de 65 |
| `revisores/r01_02_mutantes.py` | 16 muertos de 17; vivo solo R4 (equivalente) |
| `revisores/r02_02_mutantes_cierre.py` (4) | 1 muerto (C4: el pid propio sin tratamiento aparte); **3 vivos**: C1, C2 y C3 (H-09, H-10) |
| Fusión con `origin/astra/…` (sin cambios, 2d99af6) | el código se fusiona sin conflicto; chocan los mismos 4 documentos de siempre |
| Fusión con `origin/develop`, que avanzó a e91307b (T-198, que toca `orquestacion.py` y `almacen.py`) | el código se fusiona sin conflicto; chocan `evidencias_pruebas_bloque_a.md`, `incidencias.md` y la deuda (todo documentación: se regenera y se conservan las dos entradas). En el árbol fusionado, `test_t197`, `test_t198_buscador_ct19` y `test_t87`: 84 superadas |
| ruff en los ficheros tocados | sin hallazgos. mypy y el gate completo los repite la integración, como dice el implementador; no los he lanzado (máquina compartida) |

### Las correcciones

- **H-07 · corregido.** La reserva guarda `pid`, `boot_id` y `arranque_proceso`; lo he comprobado leyendo `/proc/<pid>/stat`: el campo 22, índice 19 después del «)», es el correcto. Un pid vivo cuenta como el mismo proceso solo si coinciden los dos. Un pid propio cuenta como vivo solo si este proceso abrió ese disparo (`_ABIERTOS`). B2 pasa, y también las tres pruebas nuevas: pid propio ajeno, pid vivo con otra hora de arranque, y mismo arranque (EN_CURSO, sin escribir) frente a otro `boot_id` (FALLIDO).
- **H-08 · corregido.** El cierre escribe arriba `estado_run` FALLIDO y `motivo_cierre`, y `_previo` decide solo con `estado_run`. B3 pasa y la desviación de la r02 queda deshecha.
- **¿Falla cerrado si no se puede leer la identidad (fuera de Linux, o una reserva sin ella)?** Sí. Responder DESCARTADO_DUPLICADO no repite nunca el C1 ni cierra como huérfano un C1 que puede seguir corriendo; con lo que el planificador sabe, es la única opción que no arriesga ni un C1 doble ni un FALLIDO falso. El precio es el silencio de H-02, pero solo fuera de Linux, donde `_pid_vivo` ya daba None. Está declarado en INC-T197-01 y lo acepto. Falta, eso sí, la prueba de esa rama (H-10).

### Hallazgos nuevos

**H-09 · baja · Ninguna prueba ata que `arranque_proceso` sea de verdad la hora de arranque del proceso.**
- Cómo reproducirlo: `revisores/r02_02_mutantes_cierre.py C1`. Leer el campo 23 (`vsize`) en vez del 22 deja vivas todas las pruebas, porque el `sleep` de las pruebas no cambia de tamaño. En producción, el tamaño de un proceso de Python cambia mientras corre el ciclo, así que con un campo así el C1 en curso se cerraría como huérfano falso, con su incidencia.
- Corrección: una prueba que lance `sleep` y compruebe que `btime` (de `/proc/stat`) + `arranque_proceso / os.sysconf("SC_CLK_TCK")` queda a menos de 2 s del `time.time()` anterior al `Popen`. Si se quiere además, otra que llame dos veces a `identidad_proceso(os.getpid())` con una reserva de memoria grande en medio y compruebe que da lo mismo.
- Prueba de regresión: esa misma; C1 tiene que morir.

**H-10 · baja · La rama «no se puede saber» (identidad ilegible o reserva sin ella) no tiene prueba.**
- Cómo reproducirlo: `revisores/r02_02_mutantes_cierre.py C2 C3`. Si esa rama devuelve False (cierra como huérfano) o True (EN_CURSO para siempre) en lugar de None, las pruebas siguen pasando. Es el comportamiento declarado en INC-T197-01 para fuera de Linux.
- Corrección: una prueba con la reserva de un pid vivo ajeno (un `sleep`) y `plan.RUTA_BOOT_ID` apuntando a un fichero inexistente (`monkeypatch`), y otra con una reserva sin `boot_id` ni `arranque_proceso`. En las dos, la respuesta es DESCARTADO_DUPLICADO, F5 y HA no cambian y no hay C1.
- Prueba de regresión: esas dos; C2 y C3 tienen que morir.

### Observaciones (no son hallazgos)

- `_ABIERTOS` es del módulo y solo guarda el `disparo_id`. Dos `Bloque` con estados distintos en un mismo proceso comparten el conjunto, y en la ventana en que uno tiene abierto un disparo con el mismo identificador, la reserva huérfana de otro estado con el pid propio daría EN_CURSO. Solo pasa en pruebas: `planificar` es un proceso por estado. Si se quiere cerrar del todo, la clave sería `(carpeta del almacén, disparo_id)`.
- Un estado compartido entre máquinas o contenedores distintos (otro espacio de pid) cerraría como huérfano un C1 que sigue corriendo en otra parte. El almacén ya supone una sola máquina, porque el `flock` es local. Queda igual que en la r02.

### Ronda de cierre siguiente

Volveré a ejecutar `r02_02_mutantes_cierre.py` (C1 a C4 muertos), `r01_01_ataques.py` + `r02_01_ataques.py` (47 de 47) y `mutantes.py`, y leeré el log del gate de la integración.

## Segunda ronda de cierre de la r02 · 2026-11-24 · revisor: claude

**Veredicto final: APTO, sin ningún hallazgo abierto.** H-01 a H-10 están corregidos y verificados con mis scripts.

Copia revisada: `wip/t197` f8d911ae (encima de 1cd14ec4). Mis `qa.md` y `revisores/` llegan intactos en el commit. Entre 1cd14ec4 y f8d911ae no cambia ni una línea de `bloque_a/11_Ejecutor/bloque_a` ni de `config`: solo pruebas, `mutantes.py`, el mapa, las evidencias y la documentación del ticket.

| Comprobación | Resultado |
| --- | --- |
| `test_t197_periodicidad.py` + `test_t87_contratos.py` | 51 superadas |
| `revisores/r01_01_ataques.py` + `revisores/r02_01_ataques.py` | 47 de 47 |
| `revisores/r02_02_mutantes_cierre.py`, en una copia de f8d911ae | 4 muertos de 4 (C1 a C3, vivos en la ronda anterior, mueren) |
| `mutantes.py` del ticket (68, con C1 a C3 como M66 a M68) | 68 muertos de 68 |

- **H-09 · corregido.** `test_cierre2_h09_…` comprueba que `btime` + `arranque_proceso / SC_CLK_TCK` de un `sleep` recién lanzado queda a menos de 2 s del momento del `Popen`. Comprueba también que, después de reservar 64 MB, la identidad del proceso no cambia, así que leer el campo 23 (`vsize`) ya no pasa. C1 muere.
- **H-10 · corregido.** Dos pruebas con la reserva de un proceso vivo ajeno: una con el `boot_id` ilegible (`RUTA_BOOT_ID` inexistente) y otra con una reserva sin identidad. Las dos dan DESCARTADO_DUPLICADO, sin escribir en F5 ni en HA y sin C1. C2 y C3 mueren.
- **Sin regresiones.** El código no cambia desde la ronda anterior, cuya fusión con la rama de Astra y con develop (e91307b) se fusionaba sin conflictos de código y pasaba las pruebas (84 en el árbol con develop). Al integrarlo, hay que resolver como documentación `evidencias_pruebas_bloque_a.md` (se regenera), `incidencias.md` y la deuda (se conservan las dos entradas). El gate completo lo pasa la integración. Las dos observaciones de la ronda anterior (`_ABIERTOS` del módulo, estado compartido entre máquinas) siguen siendo observaciones, no hallazgos.
