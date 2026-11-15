# T-133 · QA del banco de medida 0.4.0

## Ronda r01

- **Revisor:** revisor nuevo sin contexto (Claude) · **Ronda:** r01 · **Fecha:** 2026-11-15 · **Commit revisado:** `bdeb3d8` (origin/develop; `VERSION = "0.4.0"`)
- **Alcance:** `.docs/scripts/banco_medida.py`, las pruebas `test_t133_*` de `.docs/scripts/pruebas_banco_medida.py` y, solo en su interfaz con el banco, `.docs/scripts/registro_experimentos.py` (T-99, ya cerrado).
- **Método:** me formé la opinión con el plan (README, CA-1 a CA-4), los hallazgos de origen (`.docs/tickets/T-94/qa.md`, «Ronda r03») y el código. Los scripts r01 se escribieron y se ejecutaron antes de leer `analisis-tecnico.md`, `pruebas.md` y `mutantes.py`. `mutantes.py` no se ejecutó: los mutantes del revisor cubren lo mismo con otro diseño.

### Reproducción desde limpio

Hice tres worktrees nuevos desde `bdeb3d8` en el scratchpad del revisor (`git worktree add --detach`), los tres con `.venv` enlazado al del proyecto:
- «wt», para las pruebas y el gate;
- «wt2», para los scripts de T-94 y del revisor;
- «wtm», solo para los mutantes.

El árbol principal estaba en el mismo commit y sin cambios. Al terminar, `git status` de los tres solo mostraba el enlace `.venv`. «.docs/experimentos» no existe en el repositorio principal, ni antes ni después.

| Comando (en el worktree) | Resultado |
| --- | --- |
| `.docs/scripts/pruebas_scripts.sh` | **223 passed** (46 s); línea base 223 |
| `pytest --collect-only .docs/scripts/pruebas_banco_medida.py` | 98 pruebas (82 en la r03 de T-94) |
| `ruff check` del banco, de sus pruebas y del registro (desde la raíz) | sin hallazgos |
| `tools/secrets_scan.py` (con los scripts r01 ya escritos) | sin hallazgos |
| `./tools/check_all.sh` (una sola vez, en «wt») | **12/12 en verde**, código 0, 37 min. Detalle en «Gate» |

### Scripts de las QA de T-94, otra vez (CA-2)

Todos se ejecutaron contra el banco 0.4.0 de «wt2» con `.venv/bin/python -B <script> <wt2>/.docs/scripts`, y `r03_07` con el worktree «wtm». No se tocó ninguno.

| Script | Resultado | Juicio |
| --- | --- | --- |
| `r03_01`, `r03_02`, `r03_04` | 0 fallos | sin cambios. `r03_02`, punto 6: con el nivel 0,80 y 10 fechas, **24,5 %** de veredictos firmes sin habilidad (nominal 20 %): ver H-08 |
| `r03_03` | se detiene: `min_efectivas=5` → `BancoError` | **cambio de diseño declarado** (H-27, mínimo 10) |
| `r03_05` | 1 fallo: «carpeta recién escrita: verificar no ve problemas (sin y con --registro)». La carpeta se anotó en un registro temporal y `verificar` sin `--registro` usa el del agente | **cambio de diseño declarado** (H-23). El resto de `r03_05`, en verde |
| `r03_06` (integración con A) | 0 fallos. Byte a byte con `PYTHONHASHSEED` 1 y 987, `git status` sin cambios, caché y uc en el coste, aviso y fuga en el informe | correcto |
| `r03_07` (31 mutantes) | Viven N19, S06 y V03 (con la suite completa), y quedan sin patrón N23 y C02 | **N19 sigue vivo**: H-28 no está corregido para N19 (H-04). S06 y V03 son equivalentes, como en la r03. C02: el patrón aparece ahora dos veces, porque `leer_consumo` también comprueba columnas repetidas, y su lado del consumo lo cubre K02 de `r01_04` |
| `r03_08` | 1 fallo y 3 notas: una fila sin `fecha_fin` sigue contando como ventana de un día (30 fechas H3 → 30 efectivas y «mejor» por `construir_informe`); una H5 sin resolver deja la muestra en 1 fecha sin decir por qué | El fallo es **lo diseñado según el README** (H-25), pero `analisis-tecnico.md` no lo explica (H-07). Solo se llega por la API: `evaluar` siempre pone `fecha_fin`. La nota de H-24 (repetidas fuera de la muestra) ya no aplica en `ejecutar_a`: la prueba de `r03_08` usa `construir_informe` directamente |
| `r03_09` (nula propia de la r03, 1.000 mundos) | S 11,9 % / 11,5 %; L 11,2 % / 10,4 %; R 12,4 % / 10,9 %; M 12,1 % / 13,7 %. El escenario C se detiene (`min_efectivas=5`) | calibrado (techo 15 %). C: cambio de diseño declarado (H-27) |
| `r03_10` | 1 fallo: «copiar los mismos datos a otra carpeta no abre un experimento nuevo». La copia del universo se llama «universo_copia.csv» → otra huella → EXP-2026-0002, dentro del máximo | **defecto, no cambio de diseño**: H-22 sigue abierto en parte (H-01). El resto en verde: repetir la misma variante no la hace adoptable; con otros datos el prerregistro cambia; `verificar` ve el registro fabricado y el «dentro_del_maximo» cambiado |
| `r03_11` | 4 fallos. (1) `--min-efectivas 5` rechazado; (2) `consumo.csv` vacío → `BancoError`; (3) sin columnas de caché, cuentan 0; (4) una celda vacía cuenta 0 | (1) y (2): cambio de diseño correcto (el (2) falla cerrado). **(3) y (4): H-26 corregido solo en parte, y sin explicar** (H-06) |
| `.docs/tickets/T-94/nula_r03.py` (200 mundos) | sin tema 9,5 %; con tema 10,0 % | CA-3 se cumple |

### Scripts del revisor (r01)

Todo va a temporales. Se ejecutan con `.venv/bin/python -B <script> <carpeta de banco_medida.py>`; `r01_02`, con la de un worktree, y `r01_04`, con el worktree.

| Script | Qué ataca | Resultado |
| --- | --- | --- |
| `revisores/r01_01_huella_y_fuente.py` | Si `huella_datos` identifica lo que lee A. Casos: copia, universo con otro nombre, un CSV fuera del universo, ficheros que no son CSV, subcarpetas, orden de creación, `.CSV`, NFD, carpeta vacía o inexistente, enlace simbólico y fichero de 16 MiB. Después, volver a tirar con un titular no determinista y datos cambiados | **4 fallos y 2 notas** (H-01, H-09). Correcto: la copia en otra carpeta, los ficheros que no son CSV, las subcarpetas y el orden no cambian la huella; carpeta vacía o inexistente → `BancoError`; 40 tiradas con los mismos datos → 1 experimento y 0 adoptables (la regla de T-99). Mal: el universo con otro nombre, un CSV que A no lee y un cierre cambiado abren **otro experimento** con su variante libre. 300 tiradas, cada una con un CSV de relleno distinto → 300 experimentos, los 300 dentro del máximo, 24 con algún «mejor» y 0 adoptables (el veredicto conjunto exige ganar a las dos referencias); 299 de 300 informes traen la advertencia «hay N experimento(s) más… (otra fuente)» |
| `revisores/r01_02_verificar_usos.py` | `verificar` con el registro por defecto (RI_AGENTE propio, en el worktree): uso normal, carpeta copiada o movida, otro agente, rutas relativas, enlace simbólico y `experimento.json` manipulado de seis formas y como lista | **2 fallos** (H-02): una carpeta auténtica copiada a otra profundidad da código 2, sin `--registro` y con él, por «cita otro registro». Correcto: el uso normal, la carpeta movida a la misma profundidad, las rutas relativas y el enlace simbólico pasan; el registro de otro agente sin `--registro` no pasa, y con su `--registro` sí; las siete manipulaciones dan código 2 sin traza |
| `revisores/r01_03_nula_patron_a.py <wt2>/.docs/scripts 500` | Simulación nula **por `ejecutar_a`**, es decir, con la muestra elegida antes de evaluar: la ruta nueva de H-24, que no recorren `nula_r03.py` ni `r03_09`, porque llaman a `construir_informe`. Patrón de A: dos apuestas VIGENTES 26 semanas, H de 13 semanas, cortes semanales; deriva propia persistente de 0, 0,2 % y 0,4 % semanal | Firmes frente a azar: **P0 10,8 %, P1 10,6 %, P2 10,2 %** (39 fechas efectivas; 78 de 1.012 selecciones en la muestra). Calibrado: elegir la muestra antes de evaluar no introduce sesgo, ni siquiera con apuestas persistentes que cuentan en dos fechas de la muestra |
| `revisores/r01_04_mutantes.py <wtm>` | 27 mutantes de lo que cambió en 0.4.0: muestra previa (P), NEUTRAL (N01), huella y fuente (F), `verificar` (V), consumo (K), mínimo (Q) y los tres de H-28 | 19 mueren y **8 viven**: **V01** (sin `--registro` se usa el registro que cita la carpeta: vuelve H-23 y ninguna prueba lo ve), **V02**, **N19**, F08 (la fuente sin el universo), F03 (`rglob`), F04 (sin ordenar), F05 (carpeta sin CSV aceptada) y P03 (el filtro sin normalizar la fecha) (H-03, H-04). `git status` de «wtm» limpio al terminar |
| `revisores/r01_05_consumo_informe.py` | Qué llega a `informe.md` cuando falta un dato de consumo | **3 fallos** (H-06): sin columnas de caché ni uc, `informe.md` dice «0 escritos en caché y 0 leídos de caché; 0.0 uc», y el «sin dato» solo aparece en `columnas_ausentes` de `informe.json`. Una celda vacía o una fila corta en una columna obligatoria cuentan 0. `10.0` y `1e3` se aceptan como enteros exactos (correcto) |
| `revisores/r01_06_muestra_en_el_informe.py` | Lo que ve quien lee `informe.md` tras la muestra previa; una H5 sin resolver; fechas con hora | **1 fallo y 1 nota** (H-05). Con 300 selecciones del titular y 24 en la muestra, la fila del titular dice «24 \| 0 repetidas \| **0 fuera de muestra**», y el total solo está en `informe.json` (`plantilla`). Una H5 sin resolver en la primera fecha deja 1 fecha en la muestra y el motivo solo dice «pocas observaciones efectivas». Con hora en `fecha_asof`: la misma muestra (correcto) |

### Estado de los hallazgos H-21 a H-29 de T-94

| ID | Estado | Evidencia |
| --- | --- | --- |
| H-21 | **corregido en parte** | La repetición de la misma variante ya no se puede adoptar (`r01_01`: 40 tiradas, 0 adoptables; `r03_10` punto 3) y el prerregistro lleva `huella_datos` y `huella_universo` (F07 muere). Pero un cambio en los datos no es «otra variante», como dicen el README y `analisis-tecnico.md`: es **otro experimento**, con su variante libre, y lo abre cualquier cambio que A no lee (H-01) |
| H-22 | **corregido en parte** | La misma carpeta copiada da el mismo experimento (prueba H-21/H-22; F02 y F06 mueren). El universo con otro nombre de fichero da otro (`r03_10` punto 2 y `r01_01`) (H-01) |
| H-23 | corregido, sin prueba de lo central | `r03_10` puntos 4 y 5 y `r01_02`: sin `--registro`, el registro del agente; el «dentro_del_maximo» cambiado se ve. Pero V01 y V02 viven (H-03), y una carpeta copiada no se verifica (H-02) |
| H-24 | **corregido** | `test_t133_h24` (P01, P02 y P04 mueren); `r01_03`: calibrado por la ruta nueva (10,2–10,8 %); `r01_06`. Queda el informe (H-05) |
| H-25 | corregido lo pedido; el resto está declarado | NEUTRAL: `test_t133_h25` (N01 muere). Que una fila sin `fecha_fin` tenga un día de ventana y que la muestra salga del titular está declarado en el README; lo primero no lo explica `analisis-tecnico.md` (H-07). Una H5 sin resolver sigue sin motivo en el informe (H-05) |
| H-26 | **corregido en parte** | Decimales, columnas obligatorias que faltan y columnas repetidas → `BancoError` (K01, K02, K03 y K05 mueren). Celdas vacías y filas cortas cuentan 0, y lo ausente sale como 0 en `informe.md` (H-06) |
| H-27 | corregido lo de las 5 fechas | `MIN_EFECTIVAS_MIN = 10` (Q01 y Q02 mueren). El nivel 0,80 sigue dando 24,5 % de firmes con nominal 20 % (H-08) |
| H-28 | **corregido en parte** | S04 y C01 mueren; **N19 sigue vivo** (`r03_07` y `r01_04`): `test_t133_h28_la_muestra_se_aplica_a_todos_y_por_fecha` llama a `resumen` con los grupos ya hechos y no pasa por `construir_informe` (H-04) |
| H-29 | **corregido en parte** | `VERSION` 0.4.0 (prueba). El docstring (líneas 14 a 19) sigue diciendo «el número efectivo de observaciones es el de fechas distintas». La fila del índice no dice que `a` anota por defecto ni que `verificar` usa el registro del agente. La fila T-94 de la deuda sigue diciendo «al menos 5 fechas efectivas» (H-07) |

### Lo que se pidió mirar

- **¿Puede el titular elegir sus fechas para favorecerse?** No he encontrado cómo:
  - `fechas_sin_solape` solo mira la fecha de corte y `fecha_fin`, y `fecha_fin` sale del horizonte (`fecha_resolucion` de A) y no del resultado;
  - una fila sin precio final sigue gastando su ventana;
  - las NEUTRAL ya no la gastan;
  - las referencias se calculan en las mismas fechas, con el mismo número de selecciones, y azar y momento copian el horizonte.

  El titular decide la muestra con lo que sabe en cada corte, y la comparación es pareada en esas fechas, así que no hay sesgo de selección sin mirar el futuro. Mirar el futuro es la fuga, que ya quita los veredictos con un cliente real. Evidencia: `r01_03` (10,2–10,8 % de firmes por `ejecutar_a`, también con apuestas persistentes) y `r03_09` (11,2–13,7 %).
- **¿La huella identifica los datos?**
  - Orden: sí (se ordena por nombre).
  - Ficheros que no son CSV y subcarpetas: no cuentan, y está bien, porque A tampoco los lee.
  - Pero cuenta CSV que A no lee (los que no están en el universo) y el nombre del fichero del universo. Con eso, un cambio sin efecto abre otro experimento (H-01).
  - Los ficheros enormes se leen enteros en memoria, y un nombre en NFD da otra huella (H-09).
- **¿`verificar` contra el registro del agente rompe usos legítimos?**
  - Uso normal, carpeta movida a la misma profundidad, rutas relativas, enlace simbólico y otro agente con su `--registro`: funcionan.
  - Una carpeta auténtica copiada a otra profundidad (archivar la evidencia en un ticket) no se puede verificar de ninguna forma (H-02).
- **Mínimo de 10 fechas:** se aplica en la línea de órdenes, en `ejecutar_a` y en `diferencia` (`r03_11`, Q01, Q02). Es el mismo número que `evaluacion.min_conglomerados_bootstrap` de A (10), pero está escrito a mano en el banco y no se lee de esa configuración (H-08).

### Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 | sí | 98 pruebas del banco en verde, entre ellas `test_t133_*`, una por hallazgo (H-21 a H-29); `pruebas_scripts.sh` 223 ≥ 223 (línea base). Las pruebas de H-23 y H-28 no protegen lo central (H-03, H-04) |
| CA-2 | **no** | `r03_10` punto 2 sigue fallando por un **defecto** (H-22 a medias, H-01), no por un cambio de diseño. `r03_11` (celda vacía y columnas de caché ausentes que cuentan 0) y `r03_08` (fila sin `fecha_fin`) cambian o siguen igual sin que `analisis-tecnico.md` lo explique (H-06, H-07). Lo demás que falla es por diseño y está declarado (`r03_03`, `r03_05`, `r03_09` C y `r03_11` en `--min-efectivas 5` y en el fichero vacío) |
| CA-3 | sí | `nula_r03.py`: 9,5 % y 10,0 % (techo 15 %); además, `r03_09` (S, L, R y M entre el 10,4 % y el 13,7 %) y `r01_03` por la ruta nueva (10,2–10,8 %) |
| CA-4 | sí | `./tools/check_all.sh` 12/12 en verde. El commit no toca `bloque_a`, `bloque_a_forex`, `bloque_b`, `sistema_global/marco_comun_c` ni la Constitución |

### Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida |
| --- | --- | --- | --- | --- |
| H-01 | media | `revisores/r01_01_huella_y_fuente.py` y `.docs/tickets/T-94/revisores/r03_10_fuente_variantes_verificar.py` (punto 2) | **Esperado** (README y `analisis-tecnico.md`): «los mismos datos copiados en otra carpeta son el mismo experimento» y «unos datos cambiados son otra variante». **Obtenido:** `huella_datos` resume todos los `*.csv` de la carpeta y el nombre del fichero del universo, y la fuente lleva las dos huellas. Por eso abren **otro experimento**, con su máximo de variantes sin estrenar y el intento «dentro del máximo»: el mismo universo con otro nombre; un CSV que A no lee; un cierre cambiado. Con un titular no determinista se puede volver a tirar sin límite: 300 rellenos distintos dan 300 experimentos dentro del máximo. La regla de adopción de T-99 solo protege dentro de un experimento. Lo atenúan la advertencia «hay N experimento(s) más con esta misma hipótesis… (otra fuente)», en 299 de 300 informes, y el veredicto conjunto (0 adoptables en 300 tiradas sin habilidad); por eso no es alta | Huella solo de los ficheros que lee A (los `<símbolo>.csv` de los símbolos del universo) y del contenido del universo, sin su nombre (mejor: filas normalizadas y ordenadas). Decidir, y dejarlo `[PROPUESTO]`, si unos datos cambiados son otra variante del mismo experimento (como dice el ticket) o un experimento nuevo. Si es lo segundo, que `adoptable` o el informe cuenten los experimentos de la misma hipótesis y cliente. Pruebas: universo con otro nombre, CSV fuera del universo y datos cambiados |
| H-02 | media | `revisores/r01_02_verificar_usos.py` (punto 2) | **Esperado** (README y análisis: «avisa si la carpeta cita otro»): una carpeta auténtica copiada a otro sitio, por ejemplo la evidencia archivada en un ticket, se verifica. **Obtenido:** `experimento.json` guarda la ruta del registro relativa a la carpeta. Al copiarla a otra profundidad, `verificar` da **código 2**, sin `--registro` y con el `--registro` correcto, con «experimento.json cita otro registro que el indicado», aunque todo lo demás casa. No hay forma de verificarla sin editar `experimento.json`, que no lleva huella. Falla del lado cerrado, así que no da veredictos falsos | Que la ruta citada sea solo un aviso cuando el registro indicado contiene el intento con la variante y la huella del informe (o con `--registro` explícito). Separar avisos de problemas en la salida de `verificar`. O identificar el registro por algo que no dependa de la ruta (la huella de su primera anotación). Prueba con la carpeta copiada a otra profundidad |
| H-03 | media | `revisores/r01_04_mutantes.py <worktree>` (V01, V02) | **Esperado:** la prueba de H-23 protege lo que H-23 corrige. **Obtenido:** si `verificar`, sin `--registro`, vuelve a usar el registro que cita la carpeta (V01) o lo usa cuando no hay un RI_AGENTE válido (V02), las 98 pruebas siguen en verde. `test_t133_h23_verificar_no_se_fia_del_registro_que_cita_la_carpeta` siempre pasa `--registro`. Una regresión reabriría H-23 (verificar contra un registro fabricado) sin que nada lo vea | Prueba de `verificar(carpeta)` sin registro, con `REGISTRO_DEFECTO` sustituido por un temporal: una carpeta que apunta a un registro fabricado no pasa, la auténtica sí, y con `REGISTRO_DEFECTO = None` sale el problema «sin --registro y sin un RI_AGENTE válido» |
| H-04 | baja | `.docs/tickets/T-94/revisores/r03_07_mutantes.py <worktree>` y `revisores/r01_04_mutantes.py <worktree>` | **Esperado** (H-28): N19 muere. **Obtenido:** N19 vive (grupos por fecha y clase en `construir_informe`), porque la prueba nueva llama a `resumen` con grupos ya hechos. Viven también F08 (la fuente sin el universo), F03 (`rglob`), F04 (sin ordenar), F05 (carpeta sin CSV aceptada) y P03 (el filtro previo sin normalizar la fecha) | `construir_informe` con un titular de dos clases en la misma fecha (1 fecha efectiva); dos universos distintos → fuentes distintas; carpeta sin CSV → `BancoError`; `fecha_asof` con hora en `ejecutar_a` |
| H-05 | baja | `revisores/r01_06_muestra_en_el_informe.py` | **Esperado:** quien lee `informe.md` sabe cuántas selecciones quedaron fuera de la muestra. **Obtenido:** como `ejecutar_a` filtra antes, la fila del titular dice «24 selecciones, 0 repetidas, **0 fuera de muestra**» cuando el titular tenía 300. El total solo está en `informe.json` (`plantilla`), que `informe_md` no imprime. Una H5 sin resolver en la primera fecha deja 1 fecha en la muestra y el motivo solo dice «pocas observaciones efectivas» | Imprimir `plantilla` en `informe.md` (totales y en la muestra) y, cuando la muestra queda bajo el mínimo por una ventana larga, decirlo |
| H-06 | baja | `revisores/r01_05_consumo_informe.py`; `r03_11` | **Esperado** (H-26): «sin dato» si no hay dato y fallo cerrado. **Obtenido:** las columnas opcionales ausentes salen en `informe.md` como «0 escritos en caché y 0 leídos de caché; 0.0 uc», y el «sin dato» solo está en `columnas_ausentes` de `informe.json`. Una celda vacía o una fila corta en `tokens_entrada` o `tokens_salida` cuentan 0. No se explica en el análisis | Celda vacía o fila corta en una columna obligatoria → `BancoError`; en `informe.md`, «sin dato» para las columnas de `columnas_ausentes` (y fuera de `por_seleccion_resuelta`) |
| H-07 | baja | Lectura de `banco_medida.py`, de `.docs/README.md`, de la deuda y de `analisis-tecnico.md` | **Esperado:** documentación al día y cambios de diseño explicados en el análisis (CA-2). **Obtenido:** (a) el docstring del módulo (líneas 14 a 19) sigue sin las fechas sin solape (H-29); (b) la fila del índice no dice que `a` anota por defecto en el registro del agente ni contra qué registro comprueba `verificar`; (c) la fila T-94 de la deuda sigue dando «al menos 5 fechas efectivas» como cota `[PROPUESTO]`, y ahora es 10; (d) `analisis-tecnico.md` afirma «unos datos cambiados son otra variante» (falso, H-01) y «se avisa» (es un problema con código 2, H-02), y no explica la fila sin `fecha_fin` como ventana de un día (`r03_08`) ni que un `consumo.csv` vacío ahora detenga el banco (`r03_11`) | Corregir (a) a (d) |
| H-08 | baja | `.docs/tickets/T-94/revisores/r03_02_remuestreo_oraculo_adaptado.py` (punto 6) | **Esperado** (H-27): con lo que el banco admite, el nivel declarado se cumple. **Obtenido:** con nivel 0,80 y 10 fechas, 24,5 % de veredictos firmes sin habilidad (nominal 20 %). Ni se corrige ni se declara. Además, `MIN_EFECTIVAS = 10` copia a mano `evaluacion.min_conglomerados_bootstrap` de A en lugar de leerlo | Subir `NIVEL_MIN` (por ejemplo, 0,85) o ensanchar el rango con pocas fechas (√(n/(n−1)) o t de Student); leer el mínimo de la configuración de A, o dejarlo `[PROPUESTO]` en la deuda con el motivo |
| H-09 | baja | `revisores/r01_01_huella_y_fuente.py` (notas) | **Esperado:** la huella funciona con datos grandes y con nombres de macOS. **Obtenido:** `huella_datos` lee cada fichero entero (`read_bytes`; pico de 16 MiB con un fichero de 16 MiB), así que con datos de K de varios GiB puede quedarse sin memoria; el mismo nombre en NFD y en NFC da huellas distintas; y la huella se calcula antes de ejecutar A, no con lo que A lee | `hashlib.file_digest` o lectura por bloques; nombres en NFC; opcionalmente, volver a calcular la huella al terminar A y detenerse si cambió |

### Invariantes del sistema

- **Órdenes, F y G:** el banco no llega a ninguna orden ni toca F o G.
- **LLM:** no hay LLM en el evaluador, la muestra, la huella ni `verificar`.
- **Controles:** no se relajan solos. El mínimo sube a 10, y la fuga y el mínimo solo quitan veredictos.
- **Falla cerrado:** sí en lo nuevo de huella, `verificar` y consumo, salvo los restos bajos de H-06. La fila sin `fecha_fin` como ventana de un día es una decisión declarada solo en el README (H-07).
- **Números a mano:** el mínimo de 10 copia el de A sin leerlo, y la deuda sigue con la cota antigua de 5 (H-07, H-08).
- **Decisiones del operador:** que unos datos cambiados abran un experimento nuevo en lugar de una variante cambia la regla de adopción y no está `[PROPUESTO]` (H-01).
- **Secretos y datos personales:** ninguno (`tools/secrets_scan.py` limpio con los scripts r01).
- **Documentación:** H-07.

### Lo que no se pudo comprobar

- El banco con el cliente real (regla 4: sin clave ni presupuesto; la falta de determinismo se simuló con un titular falso).
- Con los datos de K (T-86 no ha llegado).
- `mutantes.py` del implementador no se ejecutó.
- Cómo importa `pytest` de los bloques, dentro del gate del worktree, los paquetes instalados en modo editable del `.venv` del proyecto. Los dos árboles estaban en el mismo commit, así que no cambia el resultado.

### Veredicto

**NO APTO.** No queda ningún hallazgo crítico ni alto, y CA-1, CA-3 y CA-4 se cumplen. Lo central de T-133 funciona:
- la muestra elegida antes de evaluar no introduce sesgo (calibrada por la ruta nueva de `ejecutar_a`);
- `verificar` ya no se fía del registro que cita la carpeta;
- repetir la misma variante no la hace adoptable;
- el mínimo de 10 fechas se aplica en todas partes.

Pero **CA-2 no se cumple**: `r03_10` sigue fallando por un defecto (la huella del universo depende del nombre del fichero y la de los datos, de CSV que A no lee: H-22 a medias), y `r03_08` y `r03_11` cambian o siguen igual sin explicarlo en `analisis-tecnico.md`.

Hay que corregir:
- los medios **H-01** (otro experimento por un cambio sin efecto; la documentación dice «otra variante»), **H-02** (`verificar` no acepta una carpeta auténtica copiada) y **H-03** (lo central de H-23 sin prueba);
- y, o bien corregir, o bien llevar a la deuda con su ID, los bajos **H-04** a **H-09**.

Después, volver a ejecutar `r01_01` a `r01_06` y los `r03_*` de T-94 en una ronda r02.

### Gate

`./tools/check_all.sh` una sola vez en el worktree «wt» limpio: **12/12 en verde**, código 0 (37 min).

| Gate | Resultado |
| --- | --- |
| Corpus, NFC, YAML, secretos, refs-vivas | en verde |
| ruff | 2831 de cuota 2831 |
| mypy | A 109/109, A-Forex 174/174, B 159/159 |
| pytest | A 6.557, A-Forex 68, B 176 |

El gate no ejecuta las pruebas de `.docs/scripts/`: se ejecutaron aparte, con 223 en verde.
