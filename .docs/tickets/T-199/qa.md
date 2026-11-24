# T-199 · QA

## Ronda r01 · 2026-11-24 · revisor: claude (sesión independiente, no implementó)

**Veredicto: NO APTO** (un hallazgo medio, H-01; tres bajos, H-02 a H-04).

Código revisado: `wip/t199` (`d1d7ac4`) sobre `6045913`, en un worktree propio (`qa_t199`), más uno de `develop` (`qa_t199_dev`) y otro
para mutantes (`qa_t199_mut`), para no mutar ficheros mientras corrían otras pruebas. Scripts y salidas en `revisores/` (r01_01 a r01_07).
Máquina de 4 núcleos con otros gates corriendo (carga natural de 5 a 9 durante toda la revisión): no se añadió carga artificial para no
tumbar los gates ajenos; se usó la carga real y `estrangular.py` (que no añade CPU).

### Lo comprobado

| Qué | Cómo | Resultado |
| --- | --- | --- |
| Gate del implementador | `herr/gate.txt` | 12/12, `exit 0`; A 8 359, FX 68, B 176; ruff 2806 frente a cuota 2806 |
| Cuota de ruff bajada | `tools/cuotas.txt` en el diff; recuento propio de los tres ejecutores | `ruff=2807 → 2806`; recuento propio: 2806. Correcto |
| ruff y mypy de los ficheros tocados | `ruff check` de los 10 ficheros; `mypy tests/tiempo_cpu.py` | 0 hallazgos; mypy sin errores |
| Ficheros tocados, completos | `pytest` de los 9 ficheros de prueba tocados (`r01_08_ficheros_tocados.log`) | 1 381 pasadas, con carga natural |
| Producción y corpus intactos | `git diff --stat` | solo pruebas, documentos del ticket, `docs/incidencias.md`, deuda y cuotas |
| Ninguna prueba antigua debilitada (salvo T-165) | lectura del diff | mismos tamaños y topes; `_rapido` mide lo mismo (el `with` de `medir_cpu` envuelve al de `pytest.raises`) |
| `develop` cae con la máquina saturada | `r01_05_estrangulada_develop.txt` (estrangulada al 10 %) | 1 fallo de 7: `test_t123…::test_el_coste_es_lineal` (10,04 s de reloj > 10) |
| T-199 aguanta lo mismo | `r01_05_estrangulada_t199.txt` (las mismas, más T-92, T-113 ×2, SIM-MC, ST-INF y `r05_h37` de T-102; al 10 %, carga 9–13) | 13 de 13 pasan |
| Mutantes del implementador (muestra) | `r01_07_mutantes_muestra.txt`, carga natural 9,5–12,8: M03 y M11 (tope fijo), M04 y M08 (razón), M13 | M03 (13,2 s > 2), M04 (5,4 s > 3), M08 (×53 > 16) y M11 muertos; M13 vivo (H-02). M12 contra la prueba propuesta en H-02: muerto en segundos |
| Razón de T-165 con un montón grande | `razon_t165.py 1000`, carga natural 9,5–12,5 (`r01_06_razon_t165_1000.txt`) | peor: 8,31 con la mínima intercalada (9,37 con una medida); con el tope 12 propuesto en H-01, margen 1,44 |
| Inventario | búsqueda propia de `time.time`, `perf_counter`, `monotonic`, `process_time`, `timeout`, `sleep`, `time_ns`, `Barrier`, `join(`, `.wait(`, `Event`, `datetime.now` en las tres suites | A-Forex y B: nada. A: ningún `perf_counter` ni `time.time` que mida coste; faltan en la tabla cuatro esperas (H-03) |
| M13 | análisis del código y `r01_02` | no equivalente, se puede matar (H-02) |
| Cambio de T-165 | `r01_01` (mutante paramétrico) | debilita la prueba (H-01) |

### H-01 · media · El tope ×16 con ×8 de texto de T-165 deja vivos cuadráticos que la prueba de `develop` mataba (CA-4)

- **Reproducir:** `cd bloque_a/11_Ejecutor/tests && PYTHONPATH=. ../../../.venv/bin/python ../../../.docs/tickets/T-199/revisores/r01_01_umbral_t165.py 120000 160000`
  (salidas: `r01_01_salida_a.txt` y `r01_01_salida_b.txt`). Es el mutante M08 del implementador con el bloque de re-escaneo como parámetro, y
  la mínima de tres medidas intercaladas en los dos protocolos (para comparar los tamaños y el tope, no el ruido).
- **Esperado:** CA-4, «lo que protege cada prueba no se debilita», y el objetivo del encargo, «sin perder la capacidad de detectar un coste
  cuadrático».
- **Pasa:** con bloque 120 000, el protocolo de `develop` (2 000 → 8 000, tope 6) da 7,17 / 6,60 / 6,20 y muere; el de T-199
  (1 000 → 8 000, tope 16) da 7,17 / 13,61 / 12,09 y **vive**. Con bloque 160 000: `develop` 4,09 / 7,52 / 6,86 (muere), T-199
  4,09 / 15,22 / 13,98 (**vive**). Con bloques de 80 000 o menos mueren los dos.
- **Por qué:** «el mismo exponente» (INC-T199-01) solo vale para un coste que sea una potencia pura de n. El defecto real (y el de M08) es
  lineal + cuadrático, `b·n + a·n²`. Con ×4 y tope 6 la prueba muere cuando el término cuadrático, al tamaño largo, pasa de 0,8 veces el
  lineal; con ×8 y tope 16, cuando pasa de 1,33 veces: hace falta un cuadrático un 67 % más pesado. El margen sobre lo lineal pasa de ×1,5 a
  ×2, más del que hace falta (la peor razón medida con carga, 9,63, es ×1,20 del lineal).
- **Corrección:** tope **12** con 1 000 → 8 000 (×1,5 del lineal, el mismo margen relativo que `develop`): muere cuando el cuadrático pasa de
  0,62 veces el lineal (más estricta que `develop`), y deja 12 / 9,63 = 1,25 de margen sobre la peor medida con carga del implementador
  (la de `develop` con la mínima intercalada era 6 / 4,94 = 1,21). Con los datos de `r01_01`, los bloques 120 000 (13,61 > 12) y 160 000
  (15,22 > 12) mueren. Corregir el docstring de la prueba, INC-T199-01 (quitar «el mismo exponente» como argumento; dar los umbrales de
  cuota cuadrática) y `pruebas.md`. Si se prefiere no mover los tamaños: 2 000 → 8 000, tope 6, con la mínima intercalada (margen 1,21).
- **Prueba de regresión:** añadir a `mutantes.py` un M14 = `ht09_reescaneo(120_000)` contra T-165 (y, si cabe en tiempo, `160_000`), que
  tiene que morir; y repetir `razon_t165.py 1000` con la carga de `carga.sh` para dejar la peor razón con el tope nuevo en `pruebas.md`.

### H-02 · baja · M13 no es equivalente y se puede matar sin medir tiempo

- **Análisis:** M13 (búsqueda desde 2 en vez de desde la aproximación) da el mismo `n_minimo` (la potencia del t crece con n), pero cuesta
  hasta 2 520 evaluaciones de la potencia por contraste donde el original hace 0 (si la aproximación pasa de la cota) o unas 5 (si no):
  con los 1 000 contrastes por familia que admite la ficha (`contrastes_maximos`), unos 500 s por llamada. No es equivalente: es una
  regresión de coste que el tope de 2 s no puede ver (0,5 s por contraste). Es un límite anterior a T-199, declarado, pero vivo.
- **Se puede matar** contando evaluaciones, que aquí sí son llamadas de Python (`_potencia_t`), sin depender de la carga:
  `revisores/r01_02_test_st_inf_cuenta.py` (original: 1, 1 y 5 evaluaciones con d = 0,05, 1e-300 y 0,06; tope 50 que corta en seguida).
  Con `r01_03_mutantes_contra.py`: **M13 MUERTO** y **M12 MUERTO**, los dos en segundos (M12 tardaba ~17 min por tiempo).
- **Corrección:** añadir esa aserción por recuento a `test_st_inf_n_minimo_de_potencia_acotado` (o como prueba nueva en `test_fase2_series.py`),
  quitar en `mutantes.py` la excepción de M13 (`malos += ok and not nombre.startswith("M13")`) y corregir «vivo a propósito» en `pruebas.md`,
  `handoff.md` y la frase del README «Contar operaciones no sirve aquí», que no vale para esta prueba.
- **Prueba de regresión:** `mutantes.py M12 M13` con la prueba nueva: los dos mueren por la aserción de recuento.

### H-03 · baja · Al inventario le faltan cuatro esperas (CA-1)

- La orden de `pruebas.md` no busca `.wait(`, y la tabla no recoge: `test_t87_contratos::test_peticion_idempotente_concurrente_durable_y_con_huella`
  (`assert dentro.wait(10)` y `assert continuar.wait(10)`, las de menos holgura de la suite), `test_t146_presupuesto::_ciclo_en_orden`
  (`assert hechos[…].wait(600)`) y `test_t65_resto_t53` (`assert turnos[clase].wait(30)`; la tabla solo cita su `join(60)`).
- No caen con carga (lo que esperan tarda milisegundos; estrangulada al 10 %, 10 s de reloj son 1 s de CPU), pero CA-1 pide justificarlas
  una a una.
- **Corrección:** añadir `\.wait\(` y `Event` a la orden de `pruebas.md` y las cuatro filas a la tabla del README, con su justificación
  (esperas a otro hilo que solo cortan un cuelgue).
- **Prueba de regresión:** la orden corregida, con su salida en `pruebas.md`, sin ninguna línea fuera de la tabla.

### H-04 · baja · Las cuatro pruebas de tiempo de T-102 siguen con el recolector activo, y una tiene el menor margen de la suite

- `test_t102_filtro.py` (T-168) mide `process_time` sin `tiempo_cpu`: con el recolector activo, que es justo la causa que el ticket da para
  T-165. `revisores/r01_04_margen_t102.py`: `test_r05_h37_sufijo_en_tiempo_lineal` gasta 0,99–1,10 s de CPU con tope 2,0 (×1,8 de margen, el
  menor de todas las pruebas de tope fijo; las otras tres, ×4 a ×10). No entraba en la lista de T-168, pero el inventario de T-199 es de las
  tres suites y el objetivo es que el gate no caiga con carga.
- **Corrección:** pasar las cuatro a `medir_cpu` (mismos topes) y añadirlas a la tabla del README con su margen.
- **Prueba de regresión:** `r01_05` estrangulada con las cuatro (ya incluye `r05_h37`) y su mutante de T-168, si lo hay, muriendo.

### Observaciones (sin hallazgo)

- `tiempo_cpu.medir_cpu` anidado es correcto (el interior no reactiva el recolector) y lo restaura si la función lanza.
- T-178 (`Barrier(timeout=3)`) y T-174 (`sleep(0.3)`): de acuerdo con la justificación; la carga solo puede debilitarlas.
- `mapa_plan_pruebas.json` y las evidencias no citan ninguna prueba tocada; no hay caso del plan.

### Resumen de la ronda

| ID | Gravedad | Corrección en una línea |
| --- | --- | --- |
| H-01 | media | T-165: tope 12 (no 16) con 1 000 → 8 000; M14 = re-escaneo de bloque 120 000 que tiene que morir; corregir INC-T199-01 |
| H-02 | baja | ST-INF-001: aserción por recuento de `_potencia_t` (r01_02); M13 deja de ser «vivo a propósito» |
| H-03 | baja | inventario: `.wait(`/`Event` en la orden y las cuatro esperas de T-87 contratos, T-146 y T-65 en la tabla |
| H-04 | baja | T-102: las cuatro pruebas de tiempo a `medir_cpu`, con su margen en la tabla |

Para la ronda r02 el revisor volverá a ejecutar `r01_01` (bloques 120 000 y 160 000 muertos), `r01_02`/`r01_03` (M12 y M13 muertos),
`r01_05` estrangulada y `r01_06`, además de leer el gate nuevo.

## Ronda r02 · 2026-11-24 · revisor: claude (el mismo de la r01)

**Veredicto: APTO.** Los cuatro hallazgos de la r01 están corregidos y probados, y no hay ninguno nuevo. No queda ninguno abierto, así que no
hace falta ronda de cierre.

Código revisado: `wip/t199` en `ad36e2ab`, sobre `d1d7ac4`. Los mutantes se ejecutaron en un worktree aparte. Carga natural de 3,5 a 4,5
durante la ronda, sin carga artificial. Salidas en `revisores/r02_*`.

| Hallazgo r01 | Corrección | Comprobación del revisor | Estado |
| --- | --- | --- | --- |
| H-01 (media) | T-165: `largo < 12 * max(corto, 0.02)` con 1 000 → 8 000; docstring, INC-T199-01, README y `pruebas.md` corregidos; M14 y M15 nuevos | `r02_01_umbral_t165.txt`: con B = 120 000, 8,07 / 9,56 / **14,08** (muere: 14,08 > 12); con B = 160 000, 4,05 / **13,18** / **15,37** (muere). `r02_07_mutantes.txt`: M14 MUERTO (×16,0) y M15 MUERTO (×14,9). Sin mutar, la peor razón es 8,66 (`r02_01`); con 6 millones de objetos vivos, 9,98 con la mínima intercalada (`r02_06_razon_t165_1000.txt`) | cerrado |
| H-02 (baja) | prueba nueva `test_st_inf_la_busqueda_del_n_minimo_empieza_en_la_aproximacion` (recuento de `_potencia_t`, corta a las 50); M13 deja de ser «vivo a propósito» | `r02_03_mutantes_recuento.txt`: M12 y M13 MUERTOS en segundos con la prueba nueva y con mi `r01_02`; sin mutar, pasan las dos pruebas de ST-INF | cerrado |
| H-03 (baja) | `.wait(` y `Event` en la búsqueda; cuatro filas nuevas más los `Barrier` sin plazo y los `timeout` simulados | la tabla recoge todas las líneas que dio mi búsqueda de la r01 | cerrado |
| H-04 (baja) | las cuatro de T-102 pasan a `medir_cpu`, con los mismos topes; M16 a M19 nuevos (mutantes de retroceso de T-168) | `r02_07_mutantes.txt`: M16 (61,6 s > 2) y M18 (24,4 s > 2,0) MUERTOS; `r02_05_estrangulada.txt` (al 10 %, con las cuatro de T-102 y la prueba nueva): **17 de 17 pasan** | cerrado |

**Gate.** `gate_t199_r02.log`: 12/12 y `exit 0`. pytest A 8 360 (8 359 más la prueba nueva), A-Forex 68, B 176; ruff 2806 frente a la cuota
2806; mypy A 102. El log terminó a las 15:22:32 y el commit es de las 15:23:03, así que el gate corrió sobre el árbol justo antes del commit.
Recuento propio de ruff: 2806, y 0 en los tres ficheros tocados en la r02.

**El margen de M14 (12,14 frente al tope 12, según el implementador).** Basta. M14 está a propósito en el umbral: es un término cuadrático
de unas 0,6 veces el lineal, justo lo que el tope 12 tiene que empezar a ver (0,62). Por eso su razón oscila alrededor de 12 (en mis tres
medidas, la mayor de las tres unidades fue 13,61, 14,08 y ×16,0). Que alguna vez sobreviva no sería una regresión de la prueba, y
`pruebas.md` lo declara («B = 120 000 queda cerca del umbral»). Los mutantes que dicen si la prueba se debilita son M15 y M08, que mueren
con margen (×13–15 y ×53).

**Observación, sin hallazgo.** La peor razón sin mutar con el montón grande ha sido 9,98 en esta ronda (8,31 en la r01 y 8,94 según el
implementador): el margen real sobre el tope 12 es de 1,20, el mismo que tenía `develop` con la mínima intercalada (1,21) y muy lejos del
1,005 que hizo caer el gate el 18-11. Si algún día cae, el remedio es subir `REPETICIONES`, no el tope.
