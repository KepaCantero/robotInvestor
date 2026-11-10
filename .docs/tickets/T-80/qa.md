# T-80 · QA independiente

- **Revisor:** Claude, revisor nuevo sin el contexto de la implementación (subagente; solo plan, Documento 0, Constitución y código) · **Ronda:** r01 · 10-11-2026
- **Código revisado:** commit `9a5225d` en `develop` (V0.68, «T-80, pendiente de QA»). Empecé sobre el árbol de trabajo sin commit; durante la revisión otra sesión hizo ese commit con el mismo código, y de paso metió las primeras versiones de mis sondas `entrega_claude/V0.68/qa/r01_*.py` (las versiones buenas son las del árbol de trabajo). No he hecho commit ni push.
- **Sondas:** `sistema_global/marco_comun_c/entrega_claude/V0.68/qa/` (`r01_comun.py` y `r01_01` a `r01_09`). Se ejecutan con `.venv/bin/python -I -B <sonda>` desde esa carpeta.

## Veredicto

**NO APTO.** Hay un hallazgo alto (H-01) y tres medios (H-02, H-03 y H-04), todos confirmados y reproducibles.

H-01 es el grave: un expediente `DIRECTA` puede quedarse con el encargo de su origen aunque el sobre que reutiliza no respondiera a ese encargo. Por ese hueco:
- un análisis hecho para `EXPLORAR` (N1) llega a `PROPUESTA` y a `AUTORIZADA`, con lo que se salta T-26 / E-09;
- un análisis cuyo sello de K se anuló sigue compitiendo y se propone.

## Reproducción desde limpio

| Qué | Comando | Resultado |
| --- | --- | --- |
| Extracción limpia de `HEAD` (`git archive HEAD`) en la carpeta temporal, todas las baterías | `bash .docs/scripts/pruebas_marco.sh` | `Marco común de C: 57 pasan, 0 fallan` |
| Batería nueva | `python -I pruebas/pruebas_via_directa_t80.py` | `93 comprobaciones` · `TODAS LAS PRUEBAS PASAN` |
| Baterías sobre el repositorio | `.docs/scripts/pruebas_marco.sh` | 57 pasan, 0 fallan |
| LEEME contra disco | `.venv/bin/python -I .docs/scripts/leeme_marco.py sistema_global/marco_comun_c` | `57 órdenes; disco: 57 baterías` · `SIN DIFERENCIAS (0)` |
| PC3-01 | `python -I entrega_claude/V0.68/scripts/pc3_01_via_directa.py` | `CUMPLE` |
| Gate, extracción limpia de `HEAD` | `./tools/check_all.sh` (con `PYTHONPATH` a los ejecutores de la extracción) | Ver «Gate» |
| Sondas r01 contra la extracción limpia | `for f in r01_0*.py; do python -I -B $f; done` | 01, 04 y 07 sin fallos; 02, 03, 05, 06, 08 y 09 dan los hallazgos de abajo |

**Gate.** Ejecutado sobre el árbol de trabajo da 8/12, pero los cuatro fallos no son de T-80. Vienen de una tarea en curso de otra sesión (T-65), sin commit, en `bloque_a/` y la carpeta del ticket T-65:
- `refs-vivas`: rutas citadas en el README del ticket T-65;
- `ruff`: 3170, por encima de la cuota de 3109;
- `mypy bloque_a`: 174, por encima de la cuota de 123;
- `pytest bloque_a`: error de colección.

Por eso el gate bueno es el de la extracción limpia de `HEAD`; ver «Gate (extracción limpia de HEAD)».

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 | sí | Batería `C_*`, `D_*`, `E_*`. Además, `r01_01_ruta_completa.py`: por D y por E también llega hasta `EJECUTADA` por F y G, y lo invertido ya no se reutiliza |
| CA-2 | **no** | Los rechazos dan su código y no dejan estado (`r01_04`: 400+ entradas raras, None, NaN, inf, bytes, listas, borde de `valid_until`, reloj atrás). Pero por D sin análisis, el «nivel bajo» N1 no puede acabar en una decisión (H-04). Y la comprobación de los mínimos del análisis reutilizado tiene el hueco de H-01 |
| CA-3 | sí, con reservas | La consulta no mueve expedientes, comparaciones ni encargos, y una entrada tocada se detecta. Pero borrar el rastro o recortar su cola no se detecta (H-02), y `consultar()` lee el rastro antes de comprobarlo (H-05) |
| CA-4 | **no** | Vaciar o recortar `consultas` no sale en `integridad()` (H-02). Los campos nuevos en un expediente no `DIRECTA` tampoco (H-07, baja). Los campos de un `DIRECTA` sí se detectan (`r01_05`) |
| CA-5 | sí | `r01_07`: guardar y cargar, fichero tocado (PE-02, o O-13 con kill-switch si se recalcula la huella), estados V0.45, V0.50, V0.52 y V0.52 con LIBRE migrados (MIG-002 a MIG-006) íntegros y con el rastro vacío; el diario reproduce aceptadas y rechazadas. 57 baterías en verde. Gate: ver «Gate» |
| CA-6 | sí | `pc3_01_via_directa.py` da `CUMPLE`, también dentro de la batería |

## Hallazgos

### H-01 · alta · El `DIRECTA` hereda un encargo al que su sobre no respondió

**Qué pasa.** `_origen_reutilizable` y `abrir_directa` copian `origen["encargo_actual"]`. Ese es el último encargo del origen, que no tiene por qué ser el que respondió el sobre reutilizado.

**Cómo se llega.** El origen:
1. valida S1;
2. pasa a `EN_OBSERVACION` por el operador;
3. el operador lo reabre y se le encarga E2;
4. vuelve a `EN_OBSERVACION` por el operador.

El registro sigue dando S1 como reutilizable, y el `DIRECTA` nace `VALIDADA` con el sobre S1 y el encargo E2. Las comprobaciones que leen el encargo (decisión que informa, sello de K y mandato de SC-1) miran entonces E2, no lo que de verdad se analizó. `integridad()` lo da por bueno, porque la anotación de reutilización encadena justo ese encargo.

**Reproducir:** `python -I -B r01_02_encargo_cruzado.py` y `python -I -B r01_03_sello_cruzado.py`.

```
# r01_02: S1 con encargo N1 EXPLORAR; E2 N3 ABRIR_POSICION
origen: EN_OBSERVACION sobre EV-SOB-0001 nivel N1 encargo_actual EV-ENC-0001-B ABRIR_POSICION
abrir_directa: {'ok': True, ... 'nace_en': 'VALIDADA', 'reutiliza': 'EXP-0001'}
proponer: {'ok': True, 'codigo': 'OK', 'motivo': 'propuesta registrada'}
integridad(): []
autorizar (F y operador): True OK autorizada
OK    contraste_sin_reencargo_EXPLORAR_se_rechaza_O06      # sin el cruce, T-26 sí lo para
# r01_03: S1 con el sello K-20261105-001; E2 con K-20261106-001; K reemplaza (anula) K-20261105-001
K reemplaza K-20261105-001: True OK sello viejo: ANULADO
FALLA el_DIRECTA_con_el_analisis_de_un_sello_anulado_caduca VALIDADA
proponer: True OK propuesta registrada
OK    contraste_expediente_normal_caduca                   # un expediente normal con S1 sí caduca
```

**Esperado:** el análisis N1 de `EXPLORAR` no se propone (O-06, como sin el cruce), y el `DIRECTA` caduca cuando se anula el sello de su análisis.

**Obtenido:** se propone, se autoriza, y con datos anulados.

**Efectos de la misma raíz, sin sonda propia:**
- `_dif_cortes` usa los mercados del sello de E2;
- el mandato se comprueba con el de E2 (O-24);
- si el `DIRECTA` se vuelve a encargar desde `EN_OBSERVACION`, `_emitir` marca `ANULADO` el encargo de su origen si sigue `EN_CURSO` (`previo` es de otro expediente).

**Corrección sugerida.** El encargo de un análisis reutilizado tiene que ser el que respondió ese sobre. Por ejemplo:
- guardar en `e["sobre"]` la referencia del encargo al validarlo (con su huella);
- o, en `_origen_reutilizable`, rechazar (O-06) si el origen tiene un «encargo emitido» posterior a la validación de `sid` (`encargo_actual` distinto del encargo de esa validación);
- copiar y encadenar ese encargo, no `encargo_actual`.

**Regresiones:** las sondas 02 y 03, y que el `DIRECTA` no toque encargos de otro expediente al volver a encargarse.

### H-02 · media · El rastro SC-5 se puede vaciar o recortar sin que lo vea `integridad()`

**Qué pasa.** `consultas_ok()` da por íntegro el rastro vacío, y una cadena recortada por la cola sigue cuadrando. No se cruza con nada:
- un `DIRECTA` con `consulta_ref` puede apuntar a una consulta que ya no existe;
- su `APERTURA` puede desaparecer.

SC-3, el modelo que cita el Documento 0, sí cruza sus índices con la cadena y con lo que citan los sobres (R-M1). Con un fichero sin clave, reescrito con su huella recalculada, el estado vaciado carga `ok`.

**Reproducir:** `python -I -B r01_05_integridad.py` y `r01_07_persistencia_diario_migracion.py`.

```
FALLA SC5_recortar_la_cola_se_detecta_en_integridad integridad()=[]; cabezas SC5 cambia: bd186e49534c -> 2f6dd7ee915e
FALLA SC5_borrar_todo_el_rastro_se_detecta_en_integridad integridad()=[]; EXP-DD-01.consulta_ref=CON-0001 apunta a una consulta que ya no existe
fichero con el rastro SC-5 vaciado (huella recalculada): True OK estado cargado | EXP-DE-01.consulta_ref: CON-0001
```

**Esperado** (CA-3 y CA-4): «queda en un rastro encadenado cuya alteración se detecta».

**Obtenido:** borrar o recortar solo se ve si alguien compara `cabezas()` con un ancla externa.

**Corrección sugerida.** En `consultas_ok()`:
- cada `DIRECTA` con `consulta_ref` debe tener su `APERTURA` (`consulta_id`, `expediente_id`) y la `CONSULTA` que cita;
- cada `APERTURA` debe apuntar a un expediente que exista con esa `consulta_ref`.

Si se quiere, además, anotar la cabeza `SC5` en la anotación de nacimiento del `DIRECTA`, para que recortar la cola también se note.

### H-03 · media · La vía DIRECTA resucita una propuesta caducada sin análisis nuevo (§4.1, regla 4)

**Qué pasa.** `CADUCADA` está en `REUTILIZABLE_DESDE`. Un sello anulado o un sobre vencido ya los rechaza `_analisis_vigente`, así que en la práctica `CADUCADA` solo deja pasar un caso: el de la propuesta, o la autorización, cuya ventana de entrada venció con el sobre aún vigente.

La regla 4 dice que esa propuesta «vuelve a EN_ANÁLISIS o pasa a DESCARTADA». La tabla `T` lo cumple para el propio expediente (O-04). Pero `abrir_directa` lo saca otra vez a `VALIDADA` y se vuelve a proponer sin análisis nuevo.

**Reproducir:** `python -I -B r01_08_propuesta_caducada.py`.

```
barrer: True [('expediente', 'EXP-0001', 'CADUCADA')]
el propio expediente CADUCADA no se vuelve a proponer: False O-04
abrir_directa por D con el análisis de la propuesta caducada: True OK expediente abierto por D (vía DIRECTA): nace VALIDADA
proponer de nuevo el análisis de la propuesta caducada: True OK propuesta registrada
```

**Corrección sugerida:**
- quitar `CADUCADA` de `REUTILIZABLE_DESDE`;
- o admitirla solo si el operador lo ratifica, como T-36;
- o, si se quiere ese camino, llevarlo al operador como `[PROPUESTO]` en la deuda.

Documentar la decisión en el Documento 0, §3.

### H-04 · media · Por D, el análisis de «nivel bajo» (N1) no puede acabar nunca en una decisión

**Qué pasa.** `NIVEL_BAJO = NIVEL_MAX_POR_DECISION["EXPLORAR"]` (N1). Un encargo N1 solo vale para `EXPLORAR`, `DESCARTAR`, `MANTENER`, `REDUCIR` o `CERRAR`: E-09 exige N2 para `ABRIR_POSICION` y `AUMENTAR`. Y `proponer()` rechaza todo lo que no sea `ABRIR_POSICION` o `AUMENTAR` (T-26). Un N2 se rechaza al entrar por D (O-06).

Así que entrar por D sin análisis reutilizable produce un expediente que no puede llegar a `PROPUESTA`. Para invertir habría que observarlo y volver a encargarlo a N2.

El §2 presenta ese análisis de nivel bajo como lo que completa los mínimos de una entrada por D. Qué es «nivel bajo» (N1, o N2, el mínimo que admite una decisión) es una interpretación no ratificada: no figura como `[PROPUESTO]` en la deuda, y ni el Documento 0 ni el LEEME avisan de que ese camino no lleva a una orden.

**Reproducir:** `python -I -B r01_06_D_nivel_bajo_y_E_testigos.py`.

```
D + encargo N1 ABRIR_POSICION: False O-01 encargo no válido: E-09: ABRIR_POSICION exige al menos N2
D + encargo N2 ABRIR_POSICION: False O-06 lo que falta al entrar por D se encarga a C con un análisis de nivel bajo (N1 o menos)
proponer el DIRECTA por D con el análisis de nivel bajo: False O-06 el encargo informa la decisión 'EXPLORAR': no se propone una entrada con él
```

**Corrección sugerida:**
- o bien el nivel bajo para una decisión es el mínimo que la admite (`NIVEL_MIN_POR_DECISION`, N2);
- o bien se mantiene N1 y se dice en el Documento 0 y en la respuesta (que ese expediente no lleva a una orden). En ese caso, la interpretación va a la deuda como `[PROPUESTO]` para el operador.

Hace falta una prueba del recorrido completo en cualquiera de los dos casos.

### H-05 · baja · `consultar()` lee el rastro antes de comprobar su integridad

**Qué pasa.** Con una consulta tocada a mano, repetirla con el contenido tocado da O-02 «duplicado» (`ok`), sin O-13 ni kill-switch. Con una entrada ilegible sí da O-13.

**Reproducir:** `r01_05`.

```
FALLA consultar_con_rastro_tocado_da_O13_y_kill ({'ok': True, 'codigo': 'O-02', 'motivo': 'consulta ya registrada: se ignora', 'duplicado': True}, None)
```

**Corrección:** mover `_config_rota()` y `_rota()` antes de `_consulta()`, igual que en `abrir_directa`.

### H-06 · baja · `abrir_directa` ignora argumentos sin decirlo

**Qué pasa.**
- Por D, con un análisis reutilizable y además un encargo, el encargo se descarta en silencio.
- Con un análisis no reutilizable y un encargo, se encarga, y el análisis pedido se descarta sin devolver por qué (`analisis_ref` None, `reutiliza` None).

**Reproducir:** `r01_09_argumentos_ignorados.py`.

**Corrección:** rechazar la combinación (O-01), o devolver `motivo_no_reutiliza` y anotarlo.

### H-07 · baja · Los campos nuevos en un expediente no `DIRECTA` no se detectan

**Qué pasa.** Poner `bloque_entrada`, `analisis_ref` o `consulta_ref` en un expediente `DISCRECIONAL` deja `integridad()` vacía (`r01_05`). Hoy no tiene efecto práctico. Pero `_candidato_d` decide por `analisis_ref` si reescribe el `expediente_id` del sobre que recibe D, y eso es un campo fuera de la cadena para no `DIRECTA`.

**Corrección:**
- en `_identidad_ok`, exigir que un expediente no `DIRECTA` no lleve esos campos, o que valgan None;
- en `_candidato_d`, condicionar a `via_entrada == "DIRECTA"`, que sí está en la identidad.

### H-08 · baja · Documentación y proceso

- `.docs/tickets/T-80/pruebas.md` es la plantilla sin rellenar: no hay informe de la fase 3 ni resultado del gate.
- La fila de la tabla del LEEME de `pruebas_via_directa_t80.py` dice «entrada por C, D y E hasta EJECUTADA». La batería solo lleva D y E hasta `PROPUESTA` (el párrafo «Comprobado…» sí lo dice bien). Mi sonda 01 muestra que llegan a `EJECUTADA`: conviene añadirlo a la batería.
- `CLAUDE.md` (V0.67, 56 suites), `sistema_global/README.md` (V0.67, 56 suites) y `Briefing_de_arranque.md` (V0.67; T-80 como pendiente) no están al día. Toca hacerlo al cerrar.
- `MAX_ANALISIS_CONSULTA = 50` está escrito en el código. Es técnico, pero en la V0.67 un tope técnico parecido (`n_lineas_diario_ambar`) se llevó a `parametros.py`. Conviene decidir el criterio y aplicarlo igual.

## Qué comprobé y está bien

- **Bloques y estados:** solo el Broker entra; F, G, A, B, None, listas, bytes y cualquier otro bloque se rechazan sin estado (`r01_04`). C nace `EN_ANALISIS`, D `VALIDADA` y E `COMPARADA` (`VALIDADA` → `COMPARADA` en la misma llamada). Las transiciones hacia delante, hasta `EJECUTADA` con posición, valen para C, D y E (`r01_01`).
- **Atomicidad:** con `@_seguro`, cada rechazo deja el estado igual salvo el reloj y los avisos, también con tipos raros, NaN, inf, un `ahora` ilegible, el reloj hacia atrás (O-16) y repetir la apertura (O-03) (`r01_04`). Lo de C y D con encargo se valida en `_emitir` antes de guardar el expediente.
- **Reutilización:** no se reutiliza un análisis en juego, invertido, en reanálisis, apartado por el gestor sin ratificar (T-36), con exclusión dura (T-27), de otra cartera, caducado, con el sello anulado ni con otro mandato. El segundo `DIRECTA` con el mismo sobre se rechaza.
- **Comparación por E:** compara con todos (T-34). Con otro candidato `VALIDADA` o `COMPARADA` se devuelve a D sin dejar nada. Con un testigo que habría ganado, da O-30 sin ganador (`r01_06`).
- **`_candidato_d`:** no permite colar un sobre ajeno en una comparación. El sobre del `DIRECTA` es la copia encadenada en su historial, y `_sobre_ok` y `_hash(documento)` lo comprueban. La reescritura del `expediente_id` solo afecta a la copia que recibe D. El hueco real está aguas arriba: qué encargo acompaña al sobre (H-01).
- **Consulta:** no toca expedientes, comparaciones ni encargos. Una entrada tocada sale `CONSULTAS` en `integridad()`, y el siguiente punto de decisión da O-13 con kill-switch. Es idempotente, y un id repetido con otro contenido da O-03.
- **Persistencia:** ida y vuelta idéntica. Un fichero tocado da PE-02; con la huella recalculada, O-13 con kill-switch. Un fichero sin el atributo `consultas` no carga.
- **Migración y diario:** MIG-006 desde los cuatro estados guardados (V0.45 a V0.52), íntegros y con el rastro vacío. El diario reproduce también las rechazadas y una llamada con un argumento inexistente (O-00) (`r01_07`).
- **Invariantes:** ningún camino nuevo llega a una orden sin F y G. No hay LLM. No se relaja ningún control fuera de H-01 y H-03. No hay secretos (gate `secrets` en verde).

## Gate (extracción limpia de HEAD)

`git archive HEAD` (commit `9a5225d`) en la carpeta temporal y `./tools/check_all.sh` con `PYTHONPATH` a los ejecutores de la extracción, para no importar el `bloque_a` modificado del repositorio. Resultado: **12/12**, `TODOS LOS GATES PASARON`.

| Gate | Resultado |
| --- | --- |
| corpus-integridad, nombres-nfc, yaml-configs, secrets, refs-vivas | ✓ |
| ruff | ✓ |
| mypy (bloque_a, bloque_a_forex, bloque_b) | ✓ |
| pytest | ✓ A 201 · FX 68 · B 174 |

El gate no ejecuta las baterías del marco: esas son las 57 de arriba, también en verde.

---

# Ronda r02

- **Revisor:** Claude, revisor nuevo sin el contexto de la implementación (subagente; plan, Documento 0, Constitución, código y la r01) · **Ronda:** r02 · 10-11-2026
- **Código revisado:** commit `9a5225d` más las correcciones de la r01 sin commit en el árbol de trabajo (`git diff 9a5225d -- sistema_global .docs/tickets/T-80 CLAUDE.md`). Los cambios de `bloque_a/`, `tools/refs_vivas.py`, la prueba nueva de refs-vivas de T-65 y la carpeta del ticket T-65 son de la tarea T-65 y no se revisan. No he hecho commit ni push.
- **Sondas nuevas:** `r02_01` a `r02_05` en `sistema_global/marco_comun_c/entrega_claude/V0.68/qa/`, junto a las de la r01 (`r01_comun.py` es la base común). Se ejecutan con `.venv/bin/python -I -B <sonda>` desde esa carpeta.

## Veredicto r02

**NO APTO.** Las ocho correcciones de la r01 funcionan, pero la de H-03 tiene un rodeo de una sola llamada (H-09, media): basta con pasar a `DESCARTADA` la propuesta caducada para que la vía DIRECTA la vuelva a sacar a `VALIDADA` y se proponga otra vez sin análisis nuevo. Además hay tres hallazgos bajos (H-10 a H-12).

## Reproducción

| Qué | Comando | Resultado |
| --- | --- | --- |
| Todas las baterías, árbol de trabajo | `.docs/scripts/pruebas_marco.sh` | `Marco común de C: 57 pasan, 0 fallan` |
| Batería de T-80 | `python -I pruebas/pruebas_via_directa_t80.py` | `106 comprobaciones` · `TODAS LAS PRUEBAS PASAN` |
| La misma batería con el `orquestador.py` de `9a5225d` (copia en la carpeta temporal) | ídem | fallan las 13 regresiones que cita `pruebas.md` (H-01 a H-07), como dice el informe |
| LEEME contra disco | `.venv/bin/python -I .docs/scripts/leeme_marco.py sistema_global/marco_comun_c` | `SIN DIFERENCIAS (0)` |
| PC3-01 | `python -I entrega_claude/V0.68/scripts/pc3_01_via_directa.py` | `CUMPLE` |
| Sondas r01 | `r01_0*.py` | 01, 02, 04, 05, 07, 08 y 09 SIN FALLOS; 03 y 06, ver abajo |
| Sondas r02 | `r02_0*.py` | 02, 03 y 04 SIN FALLOS; 01 (H-09) y 05 (H-10) con fallos |
| Gate, copia limpia (`git archive HEAD` más los ficheros de T-80 del árbol de trabajo, sin los de T-65) | `./tools/check_all.sh` con `PYTHONPATH` a los ejecutores de la copia | **11/12**. Pasan corpus, NFC, YAML, secrets, ruff (3102 ≤ 3109), mypy ×3 y pytest (A 201 · FX 68 · B 174). Solo falla `refs-vivas`, por las dos citas a la carpeta del ticket T-65 de la sección r01 de este `qa.md` (H-11), que no existe en la copia sin T-65 |

## Los hallazgos de la r01

| Hallazgo | ¿Corregido de verdad? | Evidencia |
| --- | --- | --- |
| H-01 (alta) | **Sí** | `r01_02` SIN FALLOS (O-06 y el registro dice por qué). `r01_03` acaba ahora en `KeyError` porque `abrir_directa` ya rechaza (O-06) lo que la sonda esperaba que se abriera: es el comportamiento correcto. `r02_02`: un DIRECTA legítimo caduca al anularse el sello de su análisis; volver a encargar el DIRECTA no toca el encargo del origen; re-encargar el origen después de abrir el DIRECTA no rompe su integridad ni deja reutilizar S1 otra vez; un encargo nuevo del origen que caduca sin sobre (el origen vuelve a `EN_OBSERVACION` con S1) tampoco deja reutilizar S1, y el rechazo no deja estado |
| H-02 (media) | **Sí**, con el alcance que declara el Documento 0 | `r01_05` SIN FALLOS. `r02_03`: con la cadena SC-5 rehecha entera por un falsificador sin clave, se detectan la APERTURA a otro expediente, quitar el análisis de la consulta, una APERTURA a un expediente sin consulta y borrar el expediente DIRECTA (O-13 y kill-switch en el siguiente `consultar()`). Añadir lo que nadie cita (p. ej. una APERTURA repetida) no se ve: queda para el ancla externa de la cabeza `SC5` (T-02), como dice el §4 |
| H-03 (media) | **No del todo** | `r01_08` SIN FALLOS, pero ver H-09 |
| H-04 (media) | **Sí** | `NIVEL_BAJO` = N2 (`[PROPUESTO]`, en T-57). La batería lleva D con encargo N2 hasta `PROPUESTA`. `r01_06` acaba ahora en `AssertionError` porque la apertura con N2 ya se acepta (la sonda esperaba que no): es el comportamiento correcto |
| H-05 (baja) | **Sí** | `r01_05` y `r02_04`: una consulta tocada y repetida da O-13 con kill-switch antes de mirar si es duplicada |
| H-06 (baja) | **Sí** | `r01_09` SIN FALLOS; `r02_04`: análisis y encargo a la vez da O-01 sin estado |
| H-07 (baja) | **Sí** | `r01_05`; `r02_05`: también con los campos a `None`. `_candidato_d` no reescribe el sobre de un expediente que no es DIRECTA aunque lleve `analisis_ref` |
| H-08 (baja) | **Casi** | Batería, LEEME, `CLAUDE.md`, briefing, parámetro y `pruebas.md` al día; quedan restos (H-11) |

## Regresiones y agujeros nuevos: qué comprobé y está bien

- **Cruce SC-5 en los recorridos legítimos** (`r02_03`): D reutilizando con consulta hasta `EJECUTADA`, C con consulta hasta `PROPUESTA`, D con encargo N2 y consulta, E único con consulta (también observado, reabierto y vuelto a encargar) y E con un testigo (O-30). Ninguno da un `CONSULTAS` falso, que con el cruce haría saltar el kill-switch. Guardar y cargar sigue dando un estado íntegro.
- **Orden de la APERTURA y su retirada por E** (`r02_03`): por E con consulta, cuando se devuelve a D (O-22), no queda ni el expediente ni la APERTURA (el estado es idéntico). Después se entra por D con la misma consulta.
- **Formas raras de `consultas`:** un estado distinto con la cadena vacía, `None`, una lista o entradas sin historial salen como `CONSULTAS` y paran con O-13.
- **Estados guardados antiguos:** `r01_07` (V0.45 a V0.52, MIG-002 a MIG-006) sigue íntegro con el cruce. Un estado de la V0.67 no tiene expedientes DIRECTA, así que el cruce no le afecta.
- **Atomicidad** (`r02_04`): cada rechazo nuevo de `abrir_directa()` y `consultar()` deja el estado igual (salvo avisos y reloj) y sin APERTURA. Eso incluye análisis más encargo, N3, ocho niveles raros, siete `consulta_id` raros, C con encargo inválido y consulta, consulta de otra cartera, origen re-encargado (por D y por E), `CADUCADA` y seis rechazos de `consultar()`.
- **`o_max_analisis_consulta`:** 50 pasa la forma y 51 da O-01 con el número en el motivo. `PARAMETROS` es de solo lectura, y tocar `parametros._VALORES` en caliente no lo cambia (es una copia congelada). Entra en la huella de configuración y en el esquema. `PAR-0.5.0` está en la batería de T-17.
- **Esquema** (`r02_05`): `esquema_actual()` es `ESQUEMA_V0_68` y está registrado; el de la r01 (`124145…`) ya no lo está.
- **Invariantes:** ningún camino nuevo llega a una orden sin F y G. No hay LLM. Los controles no se relajan solos, salvo H-09. Los dos `[PROPUESTO]` (N2 y el 50) están en T-57.

## Hallazgos r02

### H-09 · media · La propuesta caducada vuelve por la vía DIRECTA si antes se descarta (rodeo de la corrección de H-03)

**Qué pasa.** La r01 quitó `CADUCADA` de `REUTILIZABLE_DESDE`. Pero `T` permite `CADUCADA` → `DESCARTADA` a todos los `DECISORES`, y `DESCARTADA` sí es reutilizable. Además, `_salida_no_operador` no cuenta la caducidad del Orquestador como un apartado («no es una salida decidida por nadie»), así que tampoco frena T-36. Con una llamada más (`descartar`), el análisis de la propuesta caducada vuelve a nacer `VALIDADA` en un DIRECTA, gana la comparación y se propone otra vez sin análisis nuevo. Pasa igual si quien descarta es el Broker, el gestor o el operador. También pasa con un DIRECTA cuya propuesta caduca y se descarta: un segundo DIRECTA reutiliza el mismo análisis.

**Reproducir:** `python -I -B r02_01_caducada_descartada.py`.

```
[BROKER] directa desde CADUCADA: False O-06
[BROKER] CADUCADA -> DESCARTADA: True OK
[BROKER] abrir_directa por D con el análisis de la propuesta caducada y descartada: True OK ... nace VALIDADA
[BROKER] proponer otra vez el mismo análisis: True OK propuesta registrada | integridad: []
(igual con GESTOR_TACTICA y OPERADOR; y un DIRECTA caducado y descartado deja su análisis reutilizable)
```

**Esperado** (§4.1, regla 4, y Documento 0, §3: «una propuesta caducada no vuelve sin análisis nuevo»): O-06.

**Obtenido:** se propone de nuevo con el mismo sobre.

**Corrección sugerida.** En `_origen_reutilizable`, para cada expediente que tenga el sobre, rechazar (O-06) si después de su última validación (`iv`, como en H-01 y en `_salida_no_operador`) hay una anotación hacia `CADUCADA`, esté ahora en `CADUCADA` o en `DESCARTADA`. Si se quiere dejar una salida al operador, que sea con su ratificación explícita, como T-36, y anotada. Hacen falta las regresiones de `r02_01` (los tres actores y el DIRECTA caducado).

### H-10 · baja · `orquestador.py` ya no se puede leer con Python 3.11 o anterior

**Qué pasa.** La corrección de H-08 escribe, en `orquestador.py:1914`, `f"... {PARAMETROS["o_max_analisis_consulta"]}"`: comillas dobles dentro de un f-string de comillas dobles. Eso solo vale desde Python 3.12 (PEP 701). Con 3.11 todo el módulo da `SyntaxError`, así que no carga el Orquestador ni pasa ninguna batería. El código de la r01 sí se leía con 3.11, y es el único fichero del validador que no se lee. El resto del fichero usa comillas simples en el mismo caso (`PARAMETROS['h_max_edad_dato_min']`, línea 3254). El venv del proyecto es 3.12, pero el marco se entrega como ZIP y el LEEME lo ejecuta con `python3`. El flujo de GitHub Actions (3.9 a 3.11, `flake8 --select=E9`) ya fallaba por tres `redaccion.py` de los bloques; este es uno más.

**Reproducir:** `python -I -B r02_05_esquema_identidad_y_portabilidad.py` (parte d), o `python3.11 -c "import ast; ast.parse(open('validador/orquestador.py').read())"`.

**Corrección:** `PARAMETROS['o_max_analisis_consulta']`.

### H-11 · baja · Restos de documentación y de proceso

- `sistema_global/README.md`, línea 20: sigue diciendo «Cada una de las 56 suites» (son 57; la línea 8 sí dice V0.68).
- `.docs/tickets/T-80/pruebas.md`, «Gate»: no da el resultado, solo dice que se ejecutará antes del commit. CA-5 pide «el gate da 12/12», y la r01 (H-08) ya lo echaba en falta.
- Documento 0, §5: «ningún estado se guardó con él» (el esquema `124145…` de la r01) es una afirmación sin comprobar, y el commit `9a5225d` está publicado en `origin/develop`. Un estado guardado con ese código falla cerrado (PE-08 al cargar, MG-01 al migrar: `r02_05`, parte b), pero queda varado sin camino. Conviene decirlo así («si alguien guardó un estado con el commit `9a5225d`, no se migra: se rehace») o añadir la migración.
- La sección r01 de este `qa.md` cita rutas de la carpeta del ticket T-65, que aún no está en git. En una copia limpia de T-80 sin T-65, el gate `refs-vivas` falla por esas dos citas. Si T-80 se cierra antes que T-65, hay que quitar la forma de ruta de esas citas, o hacer antes el commit de T-65.

### H-12 · baja · Motivo engañoso para un análisis de una propuesta caducada

Cuando algún expediente con el sobre está `CADUCADA`, `abrir_directa` y `analisis_vigentes()` dan «EXP-…, que tiene el análisis …, se está analizando de nuevo (CADUCADA)». No se está analizando: caducó. El Broker y el operador leen ese motivo en el registro. Corrección: un motivo propio para `CADUCADA` (y, con H-09, para «caducó después de validarse»).

## Criterios de aceptación (r02)

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 | sí | Batería; `r01_01`; `r02_03` (1a a 1e) |
| CA-2 | **no** | Los mínimos rechazan sin estado (`r02_04`), pero el análisis de una propuesta caducada vuelve a entrar por D descartándola antes (H-09) |
| CA-3 | sí | `r02_03` y `r02_04`; el alcance del cruce (lo citado) es el que declara el Documento 0 |
| CA-4 | sí | `r01_05`, `r02_03` y `r02_05` |
| CA-5 | sí | 57 baterías en verde; migraciones `r01_07`; gate: ver la tabla de reproducción |
| CA-6 | sí | `pc3_01_via_directa.py`: CUMPLE |


> Nota de Claude (implementador), al corregir la r02: las citas a la carpeta del ticket T-65 de la sección r01 se pasaron a texto sin forma de ruta (H-11), para que `refs-vivas` no dependa de que T-65 esté en git. No cambia nada más de este informe.

---

# Ronda r03

- **Revisor:** Claude, revisor nuevo sin el contexto de la implementación (subagente; plan, Documento 0, Constitución, código y las rondas r01 y r02) · **Ronda:** r03 · 10-11-2026
- **Código revisado:** commit `9a5225d` más las correcciones de la r01 y la r02 sin commit en el árbol de trabajo (`git diff 9a5225d -- sistema_global .docs/tickets/T-80 CLAUDE.md`). Los cambios de `bloque_a/`, `tools/`, `.docs/scripts/` y la carpeta del ticket T-65 son de la tarea T-65 y no se revisan. No he hecho commit ni push.
- **Sondas nuevas:** `r03_01_caducada_reanalizada.py` y `r03_02_atomicidad_y_diario.py` en `sistema_global/marco_comun_c/entrega_claude/V0.68/qa/`, junto a las de la r01 y la r02. Se ejecutan con `.venv/bin/python -I -B <sonda>` desde esa carpeta.

## Veredicto r03

**NO APTO.** Las doce correcciones anteriores siguen en pie, pero la corrección de H-09 (y la protección T-36 de la vía DIRECTA) solo mira los expedientes que tienen **ahora** el sobre. Un DIRECTA que se reanaliza deja de tenerlo, y el análisis de su propuesta caducada, o el que apartó el gestor, vuelve a nacer `VALIDADA` en otro DIRECTA y se propone sin análisis nuevo (H-13, media). Además hay dos hallazgos bajos (H-14 y H-15).

## Reproducción

| Qué | Comando | Resultado |
| --- | --- | --- |
| Todas las baterías, árbol de trabajo | `.docs/scripts/pruebas_marco.sh` | `Marco común de C: 57 pasan, 0 fallan` |
| Batería de T-80 | `python -I pruebas/pruebas_via_directa_t80.py` | `110 comprobaciones` · `TODAS LAS PRUEBAS PASAN` |
| LEEME contra disco | `.venv/bin/python -I .docs/scripts/leeme_marco.py sistema_global/marco_comun_c` | `SIN DIFERENCIAS (0)` |
| Python 3.11 (H-10) | `ast.parse` con `/usr/bin/python3.11` de todo `validador/` y `pruebas/` | se leen todos |
| Sondas r01 y r02 | `r01_0*.py`, `r02_0*.py` | todas SIN FALLOS, salvo `r01_03` (`KeyError`) y `r01_06` (`AssertionError`), que acaban así porque el código ya rechaza o acepta lo que la sonda de la r01 esperaba lo contrario, como explicó la r02 |
| Sondas r03 | `r03_01`, `r03_02` | con fallos: H-13 y H-14 |
| Copia limpia (`git archive HEAD` más los ficheros de T-80 del árbol de trabajo y las sondas, sin los de T-65), todas las baterías y el LEEME | `bash .docs/scripts/pruebas_marco.sh` y `leeme_marco.py` | 57 pasan, 0 fallan · `SIN DIFERENCIAS (0)` |
| Gate en esa copia (con `.venv` enlazado y `PYTHONPATH` a los ejecutores de la copia) | `./tools/check_all.sh` | **12/12**, `TODOS LOS GATES PASARON`: corpus, NFC, YAML, secrets, refs-vivas, ruff (3102 ≤ 3109), mypy ×3 (123, 174, 159) y pytest (A 201 · FX 68 · B 174) |

## Los hallazgos anteriores

| Hallazgo | ¿Sigue corregido? | Evidencia |
| --- | --- | --- |
| H-01 (alta) | Sí | `r01_02` y `r02_02` SIN FALLOS; un origen reencargado no se reutiliza (O-06) |
| H-02 (media) | Sí | `r01_05` y `r02_03` SIN FALLOS; `r03_02` d): por E devuelto a D con consulta no queda ni el expediente ni la APERTURA, e `integridad()` sigue vacía |
| H-03 (media) | Sí | `r01_08` SIN FALLOS |
| H-04 (media) | Sí | Batería (D con encargo N2 hasta `PROPUESTA`) |
| H-05 (baja) | Sí | `r01_05` y `r02_04` |
| H-06 (baja) | Sí | `r01_09` y `r02_04` |
| H-07 (baja) | Sí | `r01_05` y `r02_05` c) |
| H-08 (baja) | Sí | Documentación al día salvo lo de H-15 |
| H-09 (media) | **Solo en parte** | `r02_01` SIN FALLOS (los tres actores y el DIRECTA caducado y descartado). Pero ver H-13 |
| H-10 (baja) | Sí | `r02_05` d) y `ast.parse` con 3.11 de todo el marco |
| H-11 (baja) | Sí | `sistema_global/README.md` dice 57; `pruebas.md` da el gate; el Documento 0, §5, explica el esquema de `9a5225d`; las citas de la r01 ya no tienen forma de ruta (el gate de la copia limpia da 12/12) |
| H-12 (baja) | Sí | El motivo dice «caducó: una propuesta caducada vuelve con un análisis nuevo (§4.1, regla 4)» |

## Qué comprobé y está bien

- **Transiciones de `T` e internas** con un expediente que tiene el sobre: observar (operador o gestor), reabrir, descartar (Broker, gestor, operador), `CADUCADA` → `DESCARTADA`, `CADUCADA` → `EN_ANALISIS`, caducar en `barrer` (ventana de la propuesta, `valid_until`, sello reemplazado), exclusión T-27 en un reanálisis (el expediente se queda con el sobre viejo y la `exclusion`), objeción crítica retenida (el sobre retenido no entra en el registro; el origen reencargado da O-06) y `levantar_objecion`. Mientras el expediente conserva el sobre, todas dan O-06 cuando deben. `ratificar_apartado` no deja ratificar una caducidad (O-04), así que no abre la puerta.
- **Atomicidad** (`r03_02`): `abrir_directa()` y `consultar()` con listas y diccionarios en `cartera_destino`, `bloque`, `cartera`, `tipo` y `analisis`, `pregunta` `None` y `analisis` con NaN rechazan (O-01, O-15 u O-00) sin estado. `analisis_vigentes()` no muta nada, da `[]` con un `ahora` ilegible y no lanza con un estado roto.
- **Diario y persistencia** (`r03_02` d): un recorrido con la consulta, E devuelto a D, D con consulta, la propuesta, la caducidad, el reanálisis y la reapertura de H-13 se reproduce idéntico desde el diario, y guardar y cargar da un estado íntegro.
- **Invariantes:** ningún camino nuevo llega a una orden sin F y G (la propuesta de H-13 sigue necesitando F, la autorización y G). No hay LLM. Los dos `[PROPUESTO]` siguen en T-57. No hay secretos (gate `secrets` en verde).

## Hallazgos r03

### H-13 · media · El análisis de una propuesta caducada, o el que apartó el gestor, vuelve por otro DIRECTA cuando el primero se reanaliza

**Qué pasa.** `_origen_reutilizable` solo recorre los expedientes cuyo `sobre.event_id` es hoy el análisis pedido (`sid`). Un expediente DIRECTA que reutilizó `sid` y después:
- caducó (`CADUCADA` → `EN_ANALISIS` está en `T` para los emisores), o
- lo apartó el gestor (T-36) y se reabrió,

y al que C le entrega un sobre nuevo S2, ya no «tiene» `sid`. El origen sigue teniéndolo, en `EN_OBSERVACION` por el operador, y en su propio historial no hay caducidad ni apartado. Con eso, `sid` vuelve a salir reutilizable en `analisis_vigentes()`, nace `VALIDADA` en un DIRECTA nuevo, gana la comparación y se propone con el mismo sobre.

En la variante del gestor no hace falta ninguna acción del operador: la reapertura la da la condición `FECHA` cumplida y el reencargo lo pide el Broker. Por la misma raíz, una exclusión dura T-27 que aparezca en un reanálisis posterior del DIRECTA tampoco frena `sid` (parte d de la sonda: el DIRECTA se reanaliza a S2 y luego a S3 `BLOQUEADO`, queda `DESCARTADA` con la `exclusion` y el sobre S2, y `sid` nace otra vez `VALIDADA` en un DIRECTA nuevo).

En el flujo normal esto no pasa: el expediente que se reanaliza es el que tiene el sobre en el registro (`eventos[sid]`), y al reanalizarlo `sid` sale del registro. Es la vía DIRECTA la que deja una copia de `sid` en un expediente y el original en otro.

**Reproducir:** `python -I -B r03_01_caducada_reanalizada.py`.

```
a) la propuesta del DIRECTA caduca y el DIRECTA se reanaliza
   control: abrir_directa con S1 con el DIRECTA aún CADUCADA: False O-06
   sobre nuevo S2 para EXP-DD-01: True OK | estado VALIDADA | sobre EV-SOB-DD-01-B
   registro (a): [('EV-SOB-0001', True, '')]
   abrir_directa EXP-DD-02 con S1 (a): True OK expediente abierto por D (vía DIRECTA): nace VALIDADA
   proponer EXP-DD-02 (S1 otra vez): True OK propuesta registrada | integridad []
c) el gestor aparta el DIRECTA, se cumple su condición de reapertura y el Broker lo reanaliza
   actores en el historial de EXP-DD-01: ['BROKER', 'C', 'GESTOR_TACTICA', 'ORQUESTADOR']
   abrir_directa EXP-DD-02 con S1 (c): True OK expediente abierto por D (vía DIRECTA): nace VALIDADA
d) el DIRECTA se reanaliza dos veces y el segundo reanálisis sale BLOQUEADO
   S3 BLOQUEADO: True O-32 | estado DESCARTADA | sobre EV-SOB-DD-01-B | exclusion True
   abrir_directa EXP-DD-02 con S1 (d): True OK expediente abierto por D (vía DIRECTA): nace VALIDADA
```

**Esperado** (§4.1, regla 4; Documento 0, §3, «una propuesta caducada no vuelve sin análisis nuevo»; riesgo T-36 del README: «no se reutiliza si algún expediente que lo tiene fue apartado sin ratificar»): O-06, como cuando el DIRECTA aún conserva el sobre (el control de la sonda lo da).

**Obtenido:** se reutiliza y se propone otra vez el análisis de la propuesta caducada (o el que apartó el gestor).

**Corrección sugerida.** Que la comprobación mire también a los expedientes que **tuvieron** `sid`, no solo a los que lo tienen. Todo DIRECTA lleva `analisis_ref` en su identidad encadenada, así que se puede:
- recorrer también los expedientes con `via_entrada == "DIRECTA"` y `analisis_ref == sid`;
- en cada uno, mirar el tramo de historial en que tuvo `sid` (desde su nacimiento hasta su primer «encargo emitido»);
- rechazar (O-06) si en ese tramo hay una anotación hacia `CADUCADA`, una salida de un actor distinto del operador sin ratificar (la lógica de `_salida_no_operador` acotada a ese tramo) o una exclusión.

O, más simple y más cerrado: no reutilizar `sid` si algún DIRECTA con `analisis_ref == sid` se volvió a encargar. Hacen falta las regresiones de `r03_01` a), c) y d), y el Documento 0, §3, tiene que decir «ningún expediente que lo tenga o lo haya tenido».

### H-14 · baja · Un rechazo de `abrir_directa()` por C (o por D con encargo) puede caducar encargos de otros expedientes

**Qué pasa.** `_emitir()` llama a `_caducar_encargos()` antes de comprobar la cartera, el expediente, el emisor, el mandato y las reglas del encargo. Si hay un encargo `EN_CURSO` de otro expediente con el `valid_until` vencido, un `abrir_directa()` que se rechaza (O-12, O-24, O-01…) lo deja `CADUCADO`, con su aviso O-10.

No relaja ningún control: es lo mismo que haría el siguiente `barrer`, y el diario lo reproduce. `emitir_encargo()` ya lo hacía antes de T-80. Pero contradice lo que se afirma de la entrada nueva:
- el Documento 0, §2 (fila de C): «Si algo falla, el expediente no nace y nada cambia»;
- el README del ticket: «todo se valida antes de crear el expediente: un rechazo no deja nada».

**Reproducir:** `python -I -B r03_02_atomicidad_y_diario.py`, parte a).

```
a) C_cartera_del_encargo: False O-12 la cartera del encargo no es la del expediente | cambia: ['encargos'] | encargo de EXP-0001: CADUCADO
```

**Corrección sugerida:** o mover `_caducar_encargos()` detrás de las validaciones en `_emitir()` (con cuidado: la comprobación del reintento lee el estado del encargo previo), o matizar las dos frases («salvo la caducidad de encargos vencidos, que haría igual `barrer`»).

### H-15 · baja · Restos de documentación

- Deuda técnica, fila T-80: dice «QA r01 NO APTO, corregido» y no menciona la r02 ni la r03.
- LEEME, fila de `pruebas_via_directa_t80.py`: «y las regresiones de la QA r01», pero las 110 incluyen las cuatro de la r02 (`pruebas.md` sí lo dice bien).
- Cuando se corrija H-13, el §3 del Documento 0 y la frase del LEEME («si nadie lo tiene en juego, invertido, caducado…») tienen que decir «lo tiene o lo tuvo».

## Criterios de aceptación (r03)

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 | sí | Batería; `r01_01`; `r02_03` |
| CA-2 | **no** | El análisis de una propuesta caducada, o el apartado por el gestor, vuelve a entrar por D si antes se reanaliza el DIRECTA que lo tenía (H-13) |
| CA-3 | sí | `r02_03`, `r02_04` y `r03_02` |
| CA-4 | sí | `r01_05`, `r02_03` y `r02_05` |
| CA-5 | sí | 57 baterías en verde (árbol de trabajo y copia limpia); diario y persistencia (`r03_02` d); gate 12/12 en la copia limpia |
| CA-6 | sí | `pc3_01_via_directa.py`: CUMPLE (dentro de la batería) |
