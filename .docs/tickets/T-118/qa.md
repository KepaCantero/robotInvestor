# T-118 · QA independiente

- **Revisor:** un revisor nuevo sin contexto de la implementación (subagente de Claude; no implementó T-118 ni hizo la QA de T-112) · **Ronda:** r01 · **Fecha:** 2026-11-14
- **Qué se revisa:** `git diff 94c6193 HEAD -- bloque_a/11_Ejecutor/bloque_a/motor` y sus pruebas, en una copia propia (`git worktree`, HEAD separado en `08862e8`). «Antes» es `94c6193`, extraído con `git archive` a una carpeta desechable.
- **Orden de lectura:** `README.md` del ticket y la ronda r02 de `.docs/tickets/T-112/qa.md` → el diff, `servicio.py` (`servir`, `reejecutar`) y `tests/test_t118_hallazgos.py` → mis ataques → solo al final `analisis-tecnico.md`, `pruebas.md` e INC-T118-01. No leí los cuatro módulos enteros: lo que sigue sale de ejecutar, salvo donde digo «leído».
- La numeración de los hallazgos de este fichero es propia de T-118 (H-01…); «H-09» a «H-15» son los de la QA r02 de T-112 que este ticket corrige.

## Reproducción desde limpio

Entorno: el `.venv` del repositorio (enlace en la raíz de la copia, borrado al acabar). Máquina de 4 núcleos compartida con otros trabajos (carga media entre 4 y 8 casi todo el tiempo): los tiempos son cotas superiores, salvo donde digo la carga.

| Qué | Orden | Resultado |
| --- | --- | --- |
| Suite del Bloque A, una vez | `cd bloque_a/11_Ejecutor && python -m pytest -q -p no:cacheprovider` | **3957 passed in 1672 s**; el árbol queda limpio. Incluye `test_t118_hallazgos.py` (93), `test_integracion.py` y `test_t112_motor.py` |
| Corpus, refs, secretos, NFC | `tools/corpus_integridad.py`, `refs_vivas.py`, `secrets_scan.py`, `nfc_check.py` | los cuatro en verde (695 archivos del corpus) |
| ruff y mypy de A, contados como el gate | `ruff check --output-format=concise` de los tres ejecutores `\| wc -l`; `mypy --ignore-missing-imports --no-error-summary bloque_a/11_Ejecutor/bloque_a \| wc -l` | **2902** (cuota 2902) y **109** (cuota 109) |

No ejecuté `tools/check_all.sh` completo (indicación del encargo). **Es condición de cierre.**

### Scripts de la QA r02 de T-112, vueltos a ejecutar sin tocar

Todos con `.venv/bin/python -I .docs/tickets/T-112/revisores/<script>` (con `ulimit -v 8000000`).

| Script | QA r02 de T-112 | Ahora | Nota |
| --- | --- | --- | --- |
| `r02_01_hostiles_anidados.py` (**completo**) | 706 `RecursionError` y 16 escapes en los campos | **15 986 llamadas en 2 201 s: 0 escapes**, una entrada en RC por llamada, nada no finito servido, ninguna llamada > 30 s. 6/7 | El implementador no lo terminó; yo sí. La comprobación que falla son los 40 «tipo raro servido donde había un número» de ACC-FACT-001 y FIR-SPREAD-001, que la r02 ya declaró que no son hallazgo |
| `r02_02_costes_y_tamanos.py` | C: BT-VAR-001 con 100 000 rendimientos no termina en 300 s; BT-PBO-001 con 3 000 configuraciones, 118 s | C: los dos **RECHAZADO en 0,3 s y 0,6 s**; ML-PRED-001 con 50 y 300 variables, RECHAZADO. 2/3 | La comprobación que falla es «ninguna llamada admitida > 60 s», y es de carga: REG-HMM-001 (156 s) y FX-REGIME-001 (180 s) del grupo S, fuera de este ticket, con la máquina a carga 7 (52 s y 76 s en la r02) |
| `r02_03_fecha_corte_y_cache.py` | 14/17, con ML-PRED-001 sirviendo datos posteriores al corte | 14/17: **ML-PRED-001 ya no figura** | Los tres que quedan son los de la r02: dos falsos positivos declarados (vencimientos; REI-FFO-001) y la observación de la caché |
| `r02_07_semillas_ct10_config.py` | 32/36 | **36/36** | H-11, H-12 (dos) y H-14 pasan; 136 casos de control de la Fase 2 y 6 de AUD-REX-001, superados |
| `r02_09_determinismo_y_minimos.py` | 42/42 | 42/42 | Los 136 casos en dos procesos |
| `r02_04`, `r02_08`, `r01_11_config.py` | 32/32, 11/11, 6/6 | 32/32, 11/11, 6/6 | |

No repetí `r02_05_oraculos.py` ni `r02_06_mutantes.py` (no tocan lo que cambia T-118; el implementador declara 84/84 del primero).

## Mis scripts (`revisores/`)

Todos con `.venv/bin/python -I .docs/tickets/T-118/revisores/<script>`; usan un Almacén temporal.

| Script | Qué ataca | Resultado |
| --- | --- | --- |
| `r01_01_h09_fecha_corte.py` | Borde del corte, 27 formatos de la fecha de corte y 8 tipos, fechas de los datos con hora y zona horaria, ML-CAL-001 con fechas que no son texto, y un barrido de las 56 fichas con caso de control (115 casos con fechas en sus valores) | **60/60.** El día del corte se sirve y la víspera se rechaza, también con hora (`…T23:59:59` del mismo día se sirve; `2020-08-11T00:00:00` se rechaza). Zonas horarias: mezclar fechas con y sin zona se rechaza (falla cerrado). Fechas enteras `AAAAMMDD` o epoch en ML-CAL-001: rechazadas. **Ninguna ficha del grupo R sirve un dato posterior al corte.** Fuera del grupo R, 14 fichas de la Fase 1 sí (H-04) |
| `r01_02_h10_cotas_y_costes.py` | A: cada lista y cada objeto de `valores` de los 36 casos de las nueve fichas del grupo R, agrandado (393 peticiones). B: tiempo hasta el rechazo. C: el servicio más caro que admiten las cotas (17 candidatos) | A: ningún dato **que la ficha use** se sirve por encima de su cota; las 105 servidas son objetos con claves de más que la ficha ignora (observación) o listas dentro de su cota. B: **8/8**, todos RECHAZADO por la cota entre 0,03 s y 6,7 s (100 000 rendimientos, 0,19 s; 1 001 configuraciones de 2 520, 4,3 s: se rechaza antes de calcular). C: todos terminan; el más caro, **BT-PBO-001 con S = 20 y 1 000 configuraciones × 2 520: 72,6 s** con la máquina casi libre y 96,6 s con carga 7 (el implementador midió 52 s) |
| `r01_03_h11_ct10_configuracion.py` | Qué guarda cada ficha y cuánto pesa; CT-10 de las 56 con la misma configuración y con todas las secciones leídas cambiadas; artefactos antiguos o raros (16 formas); error real más cambio de configuración; manipulación; determinismo y caché; ¿el registro de lecturas es completo? | **30/34.** Ver «H-11 en detalle». Fallan tres comprobaciones de H-01 y una observación sobre la caché |
| `r01_04_h12_configuracion.py` | Las 56 fichas con dos configuraciones; bordes por el Motor con H5 en 60 meses, ventana de señales de un año y 4 sesiones por semana; siete configuraciones mal formadas; literales en los cuatro módulos | **46/47.** FX-BRK, FX-STL, FX-COINT, ST-INF (1 260), FX-REGIME (252), RISK-VAR, BT-DSR, BT-VAR (1 260) y CHR-FLOW (32 sesiones) siguen a la configuración del Motor en su borde. Una configuración mal formada (H5 con texto, 0, negativo; 0 sesiones por semana) da RECHAZADO, sin excepción. Falla REG-HMM-001 (H-05) |
| `r01_05_h13_h14_fuzz.py` | 5 758 llamadas a `servir` (12 campos, 14 sitios dentro de `datos` y `parametros`, la petición entera y los tres argumentos, con 53 valores raros, en 4 fichas); anidamiento de 1 a 40, 500 y 3 000 niveles; 124 artefactos alterados por `reejecutar` | **4/8.** El borde del anidamiento es exacto (se rechaza desde 33 niveles de contenedor, en `valores`, en `parametros` y en un campo suelto); la petición legítima más profunda de los casos de control tiene 9 y lo que el ciclo pide al Motor, 4. El RC resultante (5 654 entradas) se reabre íntegro. Fallan: 104 escapes de `servir` (H-02) y 33 re-ejecuciones sin registro (H-03) |
| `r01_06_regresion_ciclo.py` | El backtest de `CLAUDE.md` con el árbol de `94c6193` y con el nuevo | **54 de 57 ficheros idénticos byte a byte.** Los otros tres: `consumo.csv` (solo latencias), el RC (129 y 129 entradas; **0 distintas** sin `configuracion_usada` ni la cadena de hash; +0,48 % de bytes) y `sellos_integridad.json` (solo el sello del RC) |
| `r01_07_mutantes.py` | 72 mutantes: cada corrección deshecha de una en una | **56 muertos, 16 vivos**; ver «Mutantes» y H-06 |

## Estado de los hallazgos de origen (QA r02 de T-112)

| ID | Gravedad | Estado | Evidencia |
| --- | --- | --- | --- |
| H-09 | media | **corregido** | `r02_03`: ML-PRED-001 rechaza. `r01_01`: 60/60; ML-PRED-001 comprueba `fechas` y `conocible_desde`, y ML-CAL-001 sus pares fechados; son las dos únicas fichas del grupo R con fechas (barrido). Mutantes M01 a M04 y M06 muertos |
| H-10 | media | **corregido** | Los dos casos del hallazgo, RECHAZADO en décimas de segundo con su entrada en RC. Inventario de 393 peticiones sin un dato usado fuera de cota. El más caro admitido, 73 s. 19 de 29 mutantes de cota muertos; los 10 vivos son cotas de datos alineados con otro que sí la tiene (H-06) |
| H-11 | media | **corregido en lo que decía**, con una clasificación discutible que queda (H-01) | DEC-VOI-001 servida con el umbral E en 60 y re-ejecutada con 68: SI. CT-10 de las 56 fichas con todas las secciones leídas cambiadas: SI en las 56 |
| H-12 | baja | **corregido en los números que señalaba**; queda uno del mismo tipo (H-05) | `r02_07` (las dos comprobaciones) y `r01_04` |
| H-13 | baja | **corregido en los casos del hallazgo**; quedan otros escapes (H-02) | `r02_01` completo: 0 escapes en 15 986 llamadas |
| H-14 | baja | **corregido en lo que decía** (el rechazo de la ficha); queda lo que el implementador declara como límite (H-03) | `r02_07` bloque 3; 39 de mis artefactos alterados acaban en NO / ERROR_REEJECUCION con su entrada |
| H-15 | baja | **corregido** | El código da S 36, R 36, V 38, P 26 = 136, y 6 de AUD-REX-001 (ejecutado); los tres documentos de T-112 dicen lo mismo, con la cifra vieja tachada (leído) |

### H-11 en detalle (el cambio más delicado)

- **Qué se guarda.** 15 de las 56 fichas leen la configuración: las de R y S con cota (`horizontes`, `calendario`), FX-REGIME-001 (`senales`), CHR-FLOW-001 (`calendario`), ML-CAL-001 y ML-PRED-001 (además `evaluacion`) y DEC-VOI-001 (`parametros_ht03`). Las otras 41 guardan `{}`.
- **¿Es completo el registro?** Sí hoy: con una configuración espía que apunta también iterar, copiar, `items`, `keys` y `len`, ninguna de las 56 fichas accede por una vía que `_ConfiguracionLeida` no registre.
- **Tamaño del RC.** Por entrada: +27 bytes en las que no leen la configuración, +307 en las de cota, +860 en ML-CAL y ML-PRED y **+1 175 en DEC-VOI-001** (un 37 % de una entrada de 3,2 kB; es la mayor). En el ciclo simulado, +0,48 % (535 766 → 538 358 bytes; las 96 entradas con el campo lo llevan vacío).
- **Artefactos anteriores o raros.** Sin el campo, con `None`, una lista o un texto, sin `artefacto`: se re-ejecutan con la configuración vigente (SI si no ha cambiado; NO / CONVENCION_DISTINTA si ha cambiado). Sección que no es objeto, sin `valor` o desconocida: SI. `valor` de tipo absurdo o umbral NaN: NO / ERROR_REEJECUCION. Ninguna de las 16 formas escapa como excepción y todas dejan su REEJECUCION.
- **Claves que la ficha no lee.** Otra sección (`uc`): SI y nada «distinto de la vigente». Otra clave de la misma sección (`horizontes.H1` en RISK-VAR-001): SI, y la entrada anota `horizontes` como distinta.
- **Manipulación.** Cambiar el umbral guardado en el fichero JSONL: el Almacén no abre («Fallo de integridad en RC, registro 1»). Una entrada nueva bien escrita con la configuración cambiada y el resultado original: `coincide` NO.
- **Determinismo y caché.** Dos Motores y dos órdenes de llamada dan el mismo `configuracion_usada`, el mismo resultado y la misma clave de idempotencia. La clave de la caché no cambia con T-118.
- **Esquema y goldens.** `artefacto.configuracion_usada` y `reejecucion.configuracion` no están en la tabla del esquema del Registro V2.0 (corpus congelado, un `.md`; no hay esquema JSON del RC en `06_Plantillas_entregables`). Está declarado en INC-T118-01, con la petición de añadirlos en una revisión del corpus. Los goldens de la Fase 3 (`test_fase3_goldens.py`) pasan en la suite y el ciclo V5 no cambia fuera del RC.
- **¿Puede un error real pasar por inocente?** Sí, y en más casos de los que declara INC-T118-01: H-01.

### Las tres pruebas de T-112 adaptadas (leídas y ejecutadas en la suite)

- `test_fase2_riesgo.py` (dos): la muestra pasa de 3 000 a 2 520 (`H5`) porque 3 000 queda fuera de la cota nueva. Mismas afirmaciones y tolerancias. Bien adaptadas.
- `test_t112_motor.py::test_r02_h04_h07_…`: `c is m.cfg` pasa a `c == m.cfg and c is not None`. Es lo que toca: la ficha recibe ahora una copia superficial que registra las lecturas. No esconde nada; que la ficha use la configuración del Motor lo siguen afirmando `r01_11_config.py` (6/6) y las pruebas de H-12.

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 (H-09) | sí | `r01_01` y `r02_03`. El día del corte se sirve. Solo ML-PRED-001 y ML-CAL-001 tienen datos fechados en el grupo R |
| CA-2 (H-10) | sí | `test_h10_*` en la suite (17 cotas en su borde); inventario `r01_02` A; rechazo antes de calcular (B); el más caro, 73 s con la máquina casi libre: «en torno a un minuto», algo por encima de los 52 s declarados |
| CA-3 (H-11) | sí | Los tres puntos, ejecutados (`r01_03`, bloques 1, 2 y 4) |
| CA-4 (H-12) | sí en los números que señalaba el hallazgo; con la salvedad de H-05 | `r01_04` y `r02_07`. La aclaración de H2 y H5 (rango del Documento 0 frente a duración nominal de la configuración) está en INC-T118-01 y es correcta para el grupo P |
| CA-5 (H-13) | sí («con los casos del hallazgo») | `r02_01` completo: 0 escapes y una entrada por llamada. Otros casos escapan: H-02 |
| CA-6 (H-14) | sí | `r02_07` bloque 3 y `r01_05` bloque 3 |
| CA-7 (H-15) | sí | 136 (36 + 36 + 38 + 26) y 6, contados al ejecutar |
| CA-8 | sí por partes; el gate entero, pendiente | Casos de control superados (`r02_07`, `r02_09`); suite 3957 en verde; ruff 2902 y mypy 109; cuatro gates de árbol en verde. «Cada corrección tiene un mutante que alguna prueba mata»: sí por hallazgo (H-09 5 de 6, H-10 19 de 29, H-11 12 de 14, H-12 7 de 9, H-13 9 de 10, H-14 4 de 4); no por cada línea (H-06) |

## Mutantes

`python .docs/tickets/T-118/revisores/r01_07_mutantes.py <copia desechable de 11_Ejecutor>`: 72 mutantes contra `tests/test_t118_hallazgos.py` filtrado por hallazgo; **56 muertos y 16 vivos**. Cuatro de los vivos (M05, M50, M68, M78) los enfrenté además a `test_t118_hallazgos.py` entero, `test_t112_motor.py` y `test_fase2_riesgo.py`, `_series.py` y `_reales.py` (1 642 pruebas): siguen vivos.

| Vivos | Qué son | Juicio |
| --- | --- | --- |
| M19, M20, M21, M25, M26, M27, M28, M30, M31 | La cota de un dato que debe alinear con otro que también la tiene (VaR previsto y resultados; referencia e intervalos con los pares; fechas, serie y `conocible_desde` de ML-PRED-001) | Equivalentes en el resultado (el rechazo llega por el dato hermano), no en el coste: sin su cota, una lista enorme se lee entera antes de rechazarse. Ninguna prueba agranda uno solo |
| M38 | La cota del vector se comprueba después de leer los elementos, no antes | Vivo: «antes de leer» no lo afirma ninguna prueba |
| M52, M67 | Guardar la referencia viva en vez de una copia; `OBS_MAXIMAS_SERIES = 2520` a mano | Equivalentes con la configuración por defecto |
| M05 | El corte se compara con hora y no por día | Vivo: ninguna prueba usa un dato con hora dentro del día del corte (yo sí: se sirve) |
| M50 | Una sección registrada sin `valor` no se quita de la configuración vigente al re-ejecutar | Vivo: no hay prueba con una configuración parcial |
| M68 | ST-INF-001 deja de seguir a la configuración | Vivo: la prueba se parametriza con el mismo conjunto `FICHAS_OBS_H5` que el mutante cambia |
| M78 | El tope de anidamiento baja de 32 a 8 | Vivo: ninguna prueba fija por abajo el tope (los casos de control llegan a 9 niveles contados como contenedores, pero la función cuenta desde 0 y no los rechaza con 8) |

## Invariantes del sistema

- Ningún camino nuevo llega a una orden; no hay LLM en la ruta de las fichas ni en sus controles (leído: los módulos importan numpy, scipy, pandas y la configuración).
- Los controles no se relajan solos: ninguna cota se cambia desde la petición (`test_h10_una_cota_no_se_cambia_desde_la_peticion`). Matiz: la categoría de una re-ejecución que no coincide sí se ablanda con un cambio de configuración (H-01).
- Falla cerrado y valida antes de mutar: sí en lo corregido; un rechazo deja una sola entrada RECHAZO. Excepciones que aún escapan: H-02 y H-03.
- Números: las cotas nuevas salen de la configuración, de una ficha o del Documento 0, o están como `[PROPUESTO]` en INC-T118-01 (1 000 configuraciones, 20 variables, 32 niveles). Quedan a mano los de H-05.
- Decisiones del operador: en INC-T118-01 como `[PROPUESTO]`; a la de la clasificación de CT-10 le falta decir todo su alcance (H-01).
- Secretos y datos personales: ninguno; gate de secretos en verde.
- Documentación: README, análisis, pruebas e incidencia al día. El `README.md` del ejecutor no se tocó (declarado).

### Observaciones sin hallazgo

- **La caché y un cambio en caliente de `m.cfg`.** Si la configuración de un Motor se cambia sobre el mismo objeto, la petición repetida sale de la caché con las cifras de antes (la clave no lleva la configuración). Es anterior a T-118 (desde H-04 de T-112) y no ocurre si cada configuración tiene su Motor.
- **Claves de más en los objetos de datos.** Un objeto de `valores` con 5 000 claves que la ficha no conoce (`varianza_sr_ensayos`, `dinamica`, `regimen`, `objetivo`…) se sirve y las claves se ignoran; los parámetros no declarados sí se rechazan (H-02 de T-112). El coste es el de copiar la petición.
- **`servicio.py` (ejecutor original).** `ventana_posicion` 756 (línea 86), las ventanas 5, 21, 63, 126 y 252 (línea 93) y las réplicas 2 000 de FC-EVAL-001 y FC-CAL-001 (líneas 168 y 177) son números del calendario y de `evaluacion` escritos a mano. No son de T-112 ni de T-118.
- **Entradas del RC sin artefacto.** Las 33 de RI-TB que escribe `evaluador.py` en el ciclo no llevan `artefacto` (ni, por tanto, `configuracion_usada`). Anterior a T-118.

## Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | media | `.venv/bin/python -I .docs/tickets/T-118/revisores/r01_03_h11_ct10_configuracion.py` (bloque 5) | **Un error real del original queda en CONVENCION_DISTINTA también en artefactos posteriores a T-118.** Artefacto de DEC-VOI-001 con el registro de configuración completo y una cifra alterada: con la misma configuración, NO / ERROR_ORIGINAL (bien). Si después cambia el umbral E (60 → 68), o **cualquier otra clave de la misma sección que la ficha no usa** (`parametros_ht03.cambio_material`), pasa a NO / CONVENCION_DISTINTA, aunque el artefacto bueno se reproduce SI con esa misma configuración vigente, es decir, aunque la re-ejecución ha usado la configuración del artefacto y sí ha reproducido las condiciones. Lo mismo en RISK-VAR-001 al cambiar `horizontes.H1`, que no lee. Y una configuración guardada manipulada (umbral E 1e308 en una entrada bien escrita) da CONVENCION_DISTINTA. Tras la sesión T-57, que cambiará los umbrales, ningún artefacto anterior de las 15 fichas que leen la configuración podrá ya dar ERROR_ORIGINAL. `coincide` sigue siendo NO y el diagnóstico nombra las secciones, por eso no es alta. INC-T118-01 solo declara el efecto en artefactos **anteriores** a T-118 y lo justifica con «no se culpa a un cálculo sin poder reproducir sus condiciones», que aquí no vale | Reservar CONVENCION_DISTINTA para cuando la re-ejecución no ha podido usar la configuración de entonces: `sin_registro` no vacío, o una sección guardada sin `valor` (o parcial) cuya huella de `por_defecto.yaml` ya no es la vigente. Con el registro completo, ERROR_ORIGINAL aunque la vigente haya cambiado. Si se mantiene la regla actual, decir todo su alcance en INC-T118-01 para T-57. Prueba: cifra alterada + cambio de la clave leída ⇒ ERROR_ORIGINAL | abierto |
| H-02 | baja | `.venv/bin/python -I .docs/tickets/T-118/revisores/r01_05_h13_h14_fuzz.py` (bloque 1; tarda unos 45 min con la máquina cargada). Caso mínimo: `m.servir({"operacion": "REI-CAP-001", "datos": […], "parametros": {}, "horizonte": "\ud800"}, "AG-18")` | **Siguen escapando excepciones de `Motor.servir`, sin RECHAZADO ni RC: 104 de 5 758 llamadas.** (a) `UnicodeEncodeError` (47) con un sustituto UTF-16 suelto (`"\ud800"`, que `json.loads` sí produce) en `operacion`, `ficha_id`, `horizonte`, `modo`, `plan`, `prioridad`, `fecha_corte` o en `serie`, `inicio`, `fin` y `rol` de un dato: sale al escribir en el Almacén. (b) `TypeError` (45) con un valor que no es JSON (un generador; un objeto con clave tupla) en `horizonte`, `modo`, `prioridad` o dentro de `parametros`. (c) 12 más en los argumentos `solicitante`, `run_id` y `msg_id` (anidamiento profundo o referencia circular), que no vienen de la petición. Los casos que citaba H-13 sí están corregidos. (a) llega en un mensaje JSON; (b) y (c), no | Validar en `_error_de_forma` que la petición entera se puede escribir (por ejemplo `json.dumps(peticion, default=str).encode("utf-8")` dentro del `try` que ya existe, ampliado a `UnicodeEncodeError`) y exigir texto a `horizonte`, `modo` y `prioridad`; o capturar en `_rechazo` el fallo de escritura y registrar un rechazo sin los campos ilegibles | abierto |
| H-03 | baja | El mismo script, bloque 3 | **`reejecutar` aún termina en excepción, sin entrada REEJECUCION, en 33 de 124 artefactos alterados** (23 con una excepción de clase no declarada y 10 con una de clase declarada pero por otro motivo), fuera de los cuatro casos «imposibles» documentados: (a) los datos ya no se pueden resolver: una serie de HT-01 que ya no está (`DatosNoDisponibles`), una `fecha_dato` posterior al `as_of` (`FugaDeInformacion`), un `as_of` ilegible (`DateParseError`); (b) un artefacto mal formado: `datos` o `operacion` o `resultado` nulos, `ficha_id` lista, sin `resultado` (`TypeError`, `KeyError`). (a) es el límite que declara `analisis-tecnico.md` («Errores de datos en `reejecutar`») y es el caso realista: un proveedor que recorta su historia deja el CT-10 sin registro. (b) exige un RC corrupto, que la cadena de hash detecta | Meter la resolución de datos y la lectura de `orig["resultado"]["payload"]` en el mismo `try` y registrar NO / ERROR_REEJECUCION (o una entrada «imposible») con el motivo | abierto |
| H-04 | media (fuera del alcance de T-118; nace de T-106) | `.venv/bin/python -I .docs/tickets/T-118/revisores/r01_01_h09_fecha_corte.py` (bloque 2) | **Catorce fichas de la Fase 1 sirven datos en línea fechados después de la fecha de corte**, sin limitación: FON-DISC-001 (`fechas`, `fecha_nav`), FON-FLOW-001, FON-LEV-001, IDX-CONC-001 (`composicion.fecha`), IDX-ERP-001 (`historia_multiplo`), IDX-REL-001 (historias de los dos índices), MON-FIX-001, MON-REAL-001 (vintages), MON-YLD-001, TCV-BEI-001 (encuestas), TCV-CDS-001, TCV-SLOPE-001 (curva y `conocible_desde`), TCV-TP-001 y TCV-VIXTS-001. Con el corte en la víspera de su última fecha, sus 40 casos de control se sirven igual. `fichas_mon_idx.py` y `fichas_tcv.py` no leen `ent["fecha_corte"]` (leído: cero apariciones); `fichas_fon_der.py` usa una fecha de corte propia de la ficha, no la de la petición. Es el mismo defecto que H-07 y H-09 de T-112, que quedó corregido en las 35 fichas de la Fase 2. No cuento CHR-FUND-001, FIR-PRICE-001, IDX-REB-001 ni MON-EXP-001: sus fechas posteriores son vencimientos o eventos futuros por naturaleza. CA-1 de T-118 solo pide el grupo R: no cuenta para este veredicto | Ticket nuevo: `_corte` y `_hasta_corte` en los tres módulos de la Fase 1 (están ya en R, S, V y P), con un caso por ficha; conviene antes de la Fase 5 (modo sombra) | abierto |
| H-05 | baja | `.venv/bin/python -I .docs/tickets/T-118/revisores/r01_04_h12_configuracion.py` (bloque 2, última comprobación de fichas, y bloque 3) | **Queda una cota de S derivada de la configuración y escrita a mano: las 520 observaciones de REG-HMM-001.** `fichas_series.py` la declara como «H5, 120 meses, en semanas: 10 años semanales»: 120 meses es `horizontes.H5` de la configuración, no el rango del Documento 0 (5 a 30 años). Con H5 en 60 meses, FX-BRK-001 baja a 1 260 y REG-HMM-001 sigue en 520. `analisis-tecnico.md` la da por «derivada de los rangos de H5», lo que vale para los 360 meses de TEM-DIFF-001 (30 años) pero no para esta; y `test_h12_las_cotas_de_s_y_p…` afirma que no cambia. La QA r02 de T-112 no la citó | Leer `horizontes.H5` en meses y convertir a semanas, o declarar en INC-T118-01 que la cota de REG-HMM-001 es un número propio `[PROPUESTO]` y quitar la mención a H5 | abierto |
| H-06 | baja | `python .docs/tickets/T-118/revisores/r01_07_mutantes.py <copia> --solo M05,M38,M50,M68,M78` (y `--todo`) | **Cinco correcciones sin una prueba que las sostenga** (mutantes vivos no equivalentes): comparar por día y no con hora (M05); comprobar la cota antes de leer los elementos (M38); quitar de la configuración vigente una sección registrada sin valor (M50); que ST-INF-001 siga a la configuración (M68: la prueba toma su lista del mismo conjunto que protege); y el tope de anidamiento, que puede bajar a 8 sin que nada falle (M78). Además, nueve cotas de datos alineados solo se prueban junto a la de su dato hermano. En todos los casos el código hace lo correcto (comprobado con mis scripts) | Una prueba por cada uno: dato con hora en el día del corte; un vector por encima de la cota con un elemento ilegible (debe decir «máximo», no el elemento); re-ejecución con una configuración parcial; la lista de fichas de H5 escrita en la prueba; y un caso de control servido con el anidamiento que tiene | abierto |

## Veredicto

**APTO.**

Los ocho criterios de aceptación se cumplen (CA-4 con la salvedad de H-05; CA-8 por partes, con el gate entero pendiente) y no queda ningún hallazgo crítico ni alto. Los siete hallazgos de la QA r02 de T-112 están corregidos en lo que decían, con evidencia mía: los scripts de aquella ronda pasan (el `r02_01` completo, que el implementador no terminó: 15 986 llamadas sin un escape), el ciclo V5 da lo mismo que antes salvo el campo nuevo del RC, y 56 de 72 mutantes mueren.

Quedan abiertos dos medios y cuatro bajos, que se corrigen o pasan a la deuda con su ID:
- **H-01** (media): la clasificación de CT-10 se ablanda más de lo que declara INC-T118-01. Recomiendo decidirlo antes de la sesión T-57, que es la que cambiará los umbrales.
- **H-04** (media, fuera del alcance): 14 fichas de la Fase 1 no aplican la fecha de corte a sus datos en línea. Pide ticket propio, antes del modo sombra.
- **H-02**, **H-03**, **H-05** y **H-06** (bajas).

**Condición de cierre:** `./tools/check_all.sh` 12/12 en el commit, que en esta ronda no he ejecutado entero.

Lo que no comprobé, para que conste: no leí los cuatro módulos enteros; `r02_05_oraculos.py`, `r02_06_mutantes.py` e `impl_mutantes.py` no los ejecuté; el ciclo comparado es el V5 del backtest de `CLAUDE.md` (el V6 lo comparé en la r02 de T-117); los tiempos están medidos en una máquina compartida; el fuzz de `servir` cubre 4 fichas, no las 56; no hay datos reales ni modelo real (fuera del alcance).

Este revisor no cierra el ticket ni toca la deuda, el diario o la memoria: lo hace quien encargó la QA.
