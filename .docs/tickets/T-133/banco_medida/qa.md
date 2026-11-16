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

## Ronda r02

- **Revisor:** revisor nuevo sin contexto (Claude) · **Ronda:** r02 · **Fecha:** 2026-11-16 · **Commit revisado:** `e08081e` (origin/develop; banco `VERSION = "0.5.0"`, del commit `3736b10`)
- **Alcance:** `.docs/scripts/banco_medida.py` 0.5.0, las pruebas `test_t133_*` y `test_t133_r02_*` de `.docs/scripts/pruebas_banco_medida.py`, y las dos decisiones `[PROPUESTO]` de la fila T-133 de la deuda (datos cambiados como otra variante del mismo experimento; nivel mínimo de un veredicto 0,90).
- **Método:** opinión formada con el README, la r01 y el código (diff `bdeb3d8..3736b10` y el módulo entero). Los scripts r02 se escribieron antes de leer `analisis-tecnico.md`, `pruebas.md` y `mutantes.py`. Para ver lo que lee A se leyó su código (`bloque_a/11_Ejecutor/bloque_a/herramientas/ht01_datos.py`, `orquestacion.py`, `diseno_v6.py`) y se ejecutó A con el cliente simulado.

### Reproducción desde limpio

Cuatro worktrees nuevos desde `e08081e` en el scratchpad del revisor (`git worktree add --detach`), con `.venv` enlazado al del proyecto: «wt» (gate), «wt2» (pruebas y scripts), «wtm» y «wtm2» (solo mutantes). El árbol principal estaba en el mismo commit y sin cambios; «.docs/experimentos» no existe en él, ni antes ni después. Todos los temporales fueron al scratchpad.

| Comando (en el worktree) | Resultado |
| --- | --- |
| `.docs/scripts/pruebas_scripts.sh` | **231 passed** (43 s); línea base 231 (era 223) |
| `pytest --collect-only .docs/scripts/pruebas_banco_medida.py` | 106 pruebas (98 en la r01) |
| `ruff check` del banco y de sus pruebas | sin hallazgos |
| `tools/secrets_scan.py` (con los scripts r02 ya escritos) | sin hallazgos |
| `./tools/check_all.sh` (una sola vez, en «wt») | **12/12 en verde**, código 0, 38 min 36 s. Detalle en «Gate» |

### Scripts de la r01 (revisor), otra vez

Con `.venv/bin/python -B <script> <wt2>/.docs/scripts`; `r01_04` con «wtm».

| Script | Resultado | Juicio |
| --- | --- | --- |
| `r01_01_huella_y_fuente.py` | 1 fallo: «un CSV que no está en el universo no cambia la huella» | **cambio de firma, no defecto**: el script llama a `huella_datos(carpeta)` sin símbolos, y sin ellos se siguen resumiendo todos los CSV; `ejecutar_a` pasa los del universo (lo comprueba `r02_01`). Lo demás, en verde: universo con otro nombre, la misma huella; 40 tiradas iguales → 1 experimento, 0 adoptables; **300 tiradas con un CSV de relleno → 1 experimento, 1 dentro del máximo, 0 adoptables**; un cierre cambiado → el mismo experimento, fuera del máximo; pico de memoria de 2,0 MiB con un fichero de 16 MiB (era 16 MiB) |
| `r01_02_verificar_usos.py` | 1 fallo: «experimento.json con registro absoluto a otro» da código 0 con aviso | **cambio de diseño declarado** (H-02): el registro citado ya solo informa y se comprueba contra el del agente, que tiene el intento auténtico. La carpeta copiada a otra profundidad pasa, sin y con `--registro`; el registro de otro agente sin `--registro` no pasa; las otras cinco manipulaciones dan código 2 |
| `r01_03_nula_patron_a.py` | no se volvió a ejecutar | la ruta de `ejecutar_a` que mide no cambió en 0.5.0 (solo se añade la comprobación de las huellas) |
| `r01_04_mutantes.py` | 27 mutantes: 20 mueren y 7 **sin patrón** (F01 a F04, F06, F08 y V03: el código que mutaban ya no existe) | N19, P03, V01 y V02, que vivían, **mueren**. Los sin patrón se rehicieron en `r02_06` (R01 a R10, V11 a V14) |
| `r01_05_consumo_informe.py` | 0 fallos | H-06 en la línea del titular. Lo que no mira (la línea «Por selección resuelta»), en `r02_04` |
| `r01_06_muestra_en_el_informe.py` | 0 fallos, 1 nota | la nota de la H5 sin resolver sigue (resto de H-05) |

### Scripts de las QA de T-94, otra vez (CA-2)

Todos contra «wt2», sin tocarlos. `r03_04`, `r03_05` y `r03_10` se detienen al empezar: su titular falso devuelve datos de un temporal sin pasarlos con `--datos`, y 0.5.0 se detiene si el titular usa otros datos que los prerregistrados (cambio declarado en `analisis-tecnico.md`, fila H-01: «o el titular usa otros»). Se volvieron a ejecutar con `revisores/r02_00_r03_adaptados.py`, que solo hace que `rutas_por_defecto` apunte a los datos del titular falso (como el fixture `datos_falsos` de las pruebas) y pasa el nivel 0,80 de `r03_05` a 0,95.

| Script | Resultado | Juicio |
| --- | --- | --- |
| `r03_01` | 0 fallos | sin cambios |
| `r03_02` | en verde hasta el punto 6, que llama a `diferencia` con nivel 0,80 → `BancoError` | **cambio de diseño declarado** (H-08). La calibración con 0,90, en `r02_05` |
| `r03_03` | se detiene en `min_efectivas=5` | cambio de diseño declarado (H-27, de la r01) |
| `r03_04` (adaptado) | 0 fallos | correcto |
| `r03_05` (adaptado) | 1 fallo: «carpeta recién escrita: verificar no ve problemas (sin y con --registro)» | el mismo de la r01: cambio de diseño declarado (H-23). Lo demás, en verde |
| `r03_06` (integración con A, raíz de «wt2») | 0 fallos | correcto |
| `r03_07` (31 mutantes, desde el árbol principal sobre «wtm») | viven S06 y V03 (equivalentes, como en la r03 y la r01); N21 muere con la suite completa; N23, X03 y C02 sin patrón | N23 y X03 rehechos sobre el código nuevo (la búsqueda sin la fuente; la fuente sin el cliente): **los dos mueren**. C02 lo cubre K02 de `r01_04`, que muere |
| `r03_08` | 1 fallo y 3 notas: una fila sin `fecha_fin` cuenta como ventana de un día | lo mismo que en la r01: lo diseñado (README, H-25, y docstring de `fechas_sin_solape`), no un cambio. Sigue sin explicarse en `analisis-tecnico.md` (H-13) |
| `r03_09` con 1.000 mundos | S 11,9 % / 11,5 %; L 11,2 % / 10,4 %; R 12,4 % / 10,9 %; M 12,1 % / 13,7 %; «0 escenarios por encima del 15 %» | idéntico a la r01: calibrado. Con 200 mundos (lo que da sin argumentos) S sale 15,5 % frente a azar: es ruido de 200 mundos (los 1.000 dan 11,9 %). C se detiene en `min_efectivas=5` (H-27) |
| `r03_10` (adaptado) | 0 fallos | **el fallo de la r01 (H-01) ya no está**: la copia de los datos con el universo con otro nombre da el mismo experimento; 8 tiradas con un titular no determinista → 1 variante, 0 adoptables |
| `r03_11` | 6 «fallos» | todos son cambios declarados: consumo sin columnas de caché (cuenta 0, `columnas_ausentes` y «sin dato» en `informe.md`), vacío y celda vacía en una obligatoria → `BancoError` (H-06, H-26), `--nivel 0.80` y `diferencia` con 0,80 rechazados (H-08), `--min-efectivas 5` rechazado (H-27) |
| `.docs/tickets/T-94/nula_r03.py` (200 mundos) | sin tema 9,5 %; con tema 10,0 % | CA-3 se cumple |

### Scripts del revisor (r02)

Todo va al scratchpad. Se ejecutan con `.venv/bin/python -B <script> <carpeta de banco_medida.py>`; `r02_03` con la de un worktree, y `r02_06` y `r02_07` con un worktree.

| Script | Qué ataca | Resultado |
| --- | --- | --- |
| `revisores/r02_00_r03_adaptados.py` | adaptador de los `r03_*` (arriba) | — |
| `revisores/r02_01_huella_lo_que_lee_a.py` | si la huella es «solo de lo que lee A»: CSV fuera del universo, cierre cambiado, universo con otro nombre, en otro orden, con BOM o CRLF, un símbolo que cambia de clase, columnas del universo que A lee; datos con BOM o CRLF; y A de verdad (cliente simulado) | 0 fallos y 9 notas. Correcto: el CSV fuera del universo, el nombre, el orden, el BOM y el CRLF del universo no cambian la huella; el cierre y la clase, sí. **Notas (H-10):** `nombre`, `tipo_opcion` y `subyacente` del universo no entran en la huella, y A los lee; con A de verdad, **cambiar el nombre y el ámbito de las DIV da otras selecciones (otro `senales.csv`) con las mismas huellas**; un CSV que no es de un símbolo del universo (el `subyacente`, o un `indices_referencia` como ACWI si no está en el universo) tampoco entra, y A lo lee. Datos con CRLF: A entrega lo mismo y la huella cambia (otra variante, lado cerrado) |
| `revisores/r02_02_datos_durante_la_ejecucion.py` | la comprobación de que los datos no cambian durante la ejecución, con un titular falso que toca los ficheros | 1 fallo y 3 notas. Correcto: un cierre cambiado, una clase cambiada y otra carpeta con otro contenido detienen el banco; una copia con el mismo contenido pasa; el intento detenido queda «fallido» y la misma variante se reintenta. **Notas (H-10):** no se ven un cierre cambiado y restaurado antes de acabar, el `nombre` del universo ni un CSV de referencia fuera del universo. **Fallo (H-15):** un universo en el que todos los símbolos parecen números («0700», «7203») detiene el banco |
| `revisores/r02_03_verificar_avisos.py` | `verificar` con avisos, en «wt2» con `RI_AGENTE=qa-r02-t133` | 0 fallos. Copia a otra profundidad: código 0 y el aviso por stderr; con un problema a la vez, código 2 y los dos se ven; la API sin lista calla el aviso; la carpeta auténtica que cita un registro fabricado pasa contra el del agente con aviso. `experimento.json` sin la clave «registro» da un problema (lado cerrado) |
| `revisores/r02_04_informe_y_consumo.py` | la línea de la plantilla en `informe.md` y el consumo estricto | 1 fallo y 5 notas (H-12): «Por selección resuelta» dice **«0.0 leídos de caché, 0.0 uc»** sin esas columnas; una columna opcional presente con una celda vacía cuenta 0 sin decirlo; una fila con un campo de más se acepta. Correcto: la línea de la plantilla (también con 0), las tres obligatorias vacías → error, CRLF; BOM → error con motivo |
| `revisores/r02_05_nivel_y_minimo_de_a.py <wt2> 4000` | `_minimo_de_a` con la configuración de A rota o rara, y calibración de `diferencia` con nivel 0,90 y 10 fechas | 6 fallos y 4 notas. **H-11:** sin fichero, sin la clave, `true` o `10.5` → **`NameError: name 'BancoError' is not defined` al importar** (no `BancoError`); con `min_conglomerados_bootstrap: 3`, el banco admite veredictos con 3 fechas (25–27 % de rangos firmes sin habilidad). **H-14:** con nivel 0,90 y exactamente 10 fechas, **14,1 % (normal), 15,3 % (t de 3) y 15,8 % (lognormal)** de rangos firmes sin habilidad, nominal 10 % |
| `revisores/r02_06_mutantes.py <wtm>` | 24 mutantes de lo nuevo de 0.5.0 | 14 mueren y **10 viven** (H-16): R03 (huella del universo sin la clase), R05 (sin ordenar las filas), R07 (la comprobación durante la ejecución solo de los datos), R09 (símbolo sin CSV aceptado en la huella: acabaría en `FileNotFoundError`), V13 (los avisos no se imprimen), K17 («llamadas» vacía cuenta 0), Q19 (nivel mínimo 0,89), Q22 (el mínimo de A sin validar); Q21 (10 a mano) y H24 (leer entero) son equivalentes con la configuración actual. Mueren R01, R02, R04, R06, R08, R10, V11, V12, V14, I15, I16, K18, Q20 y Q23 |
| `revisores/r02_07_mutantes_del_implementador_en_worktree.py <wtm2>` | la lista de `mutantes.py` ejecutada en un worktree completo | **79 de 79 mueren** (la suite sin mutar pasa antes). Ver H-17: el propio `mutantes.py` no lo mide |

### Estado de H-01 a H-09 de la r01

| ID | Estado | Evidencia |
| --- | --- | --- |
| H-01 (media) | **corregido**, con lo que queda en H-10 | La fuente es `cliente <x>` y las huellas van en el prerregistro: unos datos cambiados son otra variante del mismo experimento, fuera del máximo (`r01_01`: 300 rellenos → 1 experimento, 1 dentro del máximo, 0 adoptables; cierre cambiado → mismo experimento, fuera del máximo; `r03_10` adaptado en verde). La huella ya no ve el nombre del universo ni los CSV fuera de él. Decisión `[PROPUESTO]` declarada en la fila T-133 de la deuda y en `analisis-tecnico.md`; falla del lado cerrado. Mutantes R01, R02 y R04 mueren. Pero la huella no es «solo lo que lee A» del todo: deja fuera columnas del universo y CSV de referencia que A sí lee (H-10) |
| H-02 (media) | **corregido** | `r01_02` punto 2 y `r02_03`: la carpeta copiada a otra profundidad da código 0 con aviso; V11 y V12 mueren |
| H-03 (media) | **corregido** | `test_t133_r02_h02_h03_verificar_con_el_registro_del_agente`; V01 y V02 de `r01_04` y V14 de `r02_06` mueren |
| H-04 (baja) | **corregido** | N19 muere (en `r01_04` y en `r03_07`), y P03 también; F03, F04 y F05 los cubre `test_t133_r02_h04_huella_sin_subcarpetas_ordenada_y_con_csv`. Quedan huecos nuevos (H-16) |
| H-05 (baja) | **corregido en parte** | `informe.md` dice el total de la plantilla y lo que entra (`r02_04`; I15 muere). La H5 sin resolver que deja la muestra en 1 fecha sigue sin motivo propio (nota de `r01_06`): la frase nueva es general. La columna «Fuera de muestra» sigue en 0 junto a la frase que dice cuántas quedan fuera |
| H-06 (baja) | **corregido en parte** | Obligatorias vacías o fila corta → error (K18 muere); «sin dato» en la línea del titular (I16 muere). Queda «Por selección resuelta» con 0.0 (H-12) |
| H-07 (baja) | **corregido en parte** | Fila del índice (`.docs/README.md`) y docstring de cabecera de la fuente, al día. Siguen: las líneas 14 a 19 del docstring sin las fechas sin solape; `analisis-tecnico.md` sin la fila sin `fecha_fin` (`r03_08`); y lo nuevo de H-13 |
| H-08 (baja) | **corregido en parte** | Nivel mínimo 0,90 `[PROPUESTO]` y mínimo leído de A (Q20 y Q23 mueren). Pero con 0,90 y 10 fechas el nivel declarado sigue sin cumplirse (14–16 % frente a 10 %, H-14), y la lectura de A falla con `NameError` y no tiene suelo propio (H-11) |
| H-09 (baja) | **corregido** | Lectura en trozos (pico 2,0 MiB con 16 MiB), nombres en NFC (R10 muere) y huellas otra vez al terminar A (R06 muere) |

### Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 | sí | 106 pruebas del banco en verde, con `test_t133_*` (una por hallazgo de T-94) y `test_t133_r02_*` (una por hallazgo de la r01); `pruebas_scripts.sh` 231 ≥ 231. Con huecos que dejan vivos 8 mutantes no equivalentes (H-16) |
| CA-2 | sí | Ningún script de las QA de T-94 da un defecto nuevo: lo que falla es un cambio de diseño explicado en `analisis-tecnico.md` (`r03_02` punto 6, `r03_03`, `r03_04`, `r03_05` y `r03_10` sin adaptar, `r03_09` C, `r03_11`) o lo que ya era así por diseño y está en el README y en el docstring (`r03_08`, sin explicar en el análisis: H-13). El defecto que hacía fallar CA-2 en la r01 (`r03_10` punto 2) está corregido |
| CA-3 | sí | `nula_r03.py`: 9,5 % y 10,0 %; `r03_09` con 1.000 mundos: entre el 10,4 % y el 13,7 % |
| CA-4 | sí | `./tools/check_all.sh` 12/12. El commit `3736b10` solo toca `.docs/` y la deuda; los cambios de `bloque_a` entre `bdeb3d8` y `e08081e` son de T-154 |

### Hallazgos nuevos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida |
| --- | --- | --- | --- | --- |
| H-10 | media | `revisores/r02_01_huella_lo_que_lee_a.py` (punto 3, con A de verdad) y `revisores/r02_02_datos_durante_la_ejecucion.py` (casos 2, 4 y 5) | **Esperado** (análisis, fila H-01): «la huella es solo de lo que A lee» y, si los datos cambian durante la ejecución, el banco se detiene. **Obtenido:** del universo solo entran (símbolo, clase), pero A lee y usa más columnas (`cargar_universo` exige `nombre`, `tipo_opcion`, `region`, `sector`, `divisa` y `notas`, y usa `ambito_*`, `indicador` y `subyacente`). Con el cliente simulado, **cambiar el nombre y el ámbito de las DIV cambia las selecciones de A y deja las dos huellas iguales**. A también lee el CSV del `subyacente` y el de `indices_referencia` (ACWI, AGG, DBC…) aunque no estén en el universo (`orquestacion.py`, `_referencia_invalida` y `gc0`), y la huella no los recoge. La comprobación de después tampoco ve esos cambios, ni un cierre cambiado y restaurado antes de acabar. Falla del lado cerrado en la adopción: con la misma ruta, el prerregistro es el mismo, la tirada es una repetición de la variante y por la regla de T-99 no cuenta. Pero el prerregistro dice que los datos eran otros que los que leyó A, y dos experimentos con entradas distintas pasan por idénticos. Por eso no es alta | Huella del universo con todas sus columnas normalizadas (o con las que lee `cargar_universo`), y de los datos con los CSV de los símbolos de `indices_referencia` y de la columna `subyacente` que existan en la carpeta. Mejor: que el proveedor CSV de A registre lo que abre y el banco resuma eso. Pruebas: cambiar `nombre` o `subyacente` del universo cambia la huella; cambiar el CSV de referencia, también. Declarar en el análisis que la comprobación es de antes y después |
| H-11 | baja | `revisores/r02_05_nivel_y_minimo_de_a.py` (punto 1) | **Esperado:** sin la configuración de A, o con un valor raro, `BancoError` con el motivo. **Obtenido:** `_minimo_de_a()` se llama en la línea 76, al importar, y `BancoError` se define en la 83: sin fichero, sin la clave, `true` o `10.5` dan **`NameError: name 'BancoError' is not defined`**, y el módulo no se importa (tampoco para `verificar`). Falla cerrado, pero sin motivo. Además, el suelo del banco sigue a A sin uno propio (solo `v >= 2`): si A baja `min_conglomerados_bootstrap` a 3 (su `por_defecto.yaml` no está en el corpus congelado), el banco admite veredictos con 3 fechas, con un 25–27 % de rangos firmes sin habilidad, y ninguna prueba lo ve (Q22 vive; la prueba solo compara con A). Un control del banco se relajaría por un cambio en A | Definir `BancoError` antes y leer el mínimo al usarlo, no al importar. Suelo propio `[PROPUESTO]` del banco (10) y `max(suelo, A)`, de modo que A solo pueda endurecerlo. Prueba con una configuración de A rara |
| H-12 | baja | `revisores/r02_04_informe_y_consumo.py` (2b, 3b y 4a) | **Esperado** (r01 H-06): «sin dato» también «fuera de `por_seleccion_resuelta`». **Obtenido:** sin las columnas de caché ni `uc`, `informe.md` dice «Por selección resuelta: … 0.0 leídos de caché, 0.0 uc». Una columna opcional presente con una celda vacía cuenta 0 y la suma sale como total completo. Una fila con un campo de más se acepta y el campo sobrante se pierde | «sin dato» en `por_seleccion_resuelta` para lo de `columnas_ausentes`; una celda vacía en una opcional presente, o error o «filas sin dato» como con el coste; fila larga → error |
| H-13 | baja | Lectura de `banco_medida.py` (líneas 14 a 19 y 682 a 684), `pruebas.md`, `analisis-tecnico.md`, la deuda y `.docs/README.md` | **Esperado:** documentación al día. **Obtenido:** (a) docstring de cabecera sin las fechas sin solape (resto de r01 H-07 a); (b) el docstring de `_experimento` sigue diciendo que el experimento es «una hipótesis con una fuente (cliente, datos y universo)», y la advertencia del informe dice «(otra fuente)» también cuando el otro experimento es de la misma fuente; (c) `pruebas.md` no tiene la ronda r02 (98 pruebas y «0 de 68 vivos»); (d) `analisis-tecnico.md` no explica la fila sin `fecha_fin` (`r03_08`) ni cómo se prerregistran «aparte» los datos de K (se puede con `registro_experimentos.py prerregistrar` y `--experimento`, pero no lo dice); (e) la fila T-94 de la deuda da a la vez «nivel entre 0,80 y 0,99» y «entre 0,90 y 0,99»; (f) la copia de los datos en otra ruta es el mismo experimento pero otra variante (la ruta entra en el prerregistro), y no se dice: `test_t133_r02_h01_…` lo tapa al cambiar `rutas_por_defecto` en lugar de pasar `--datos` | Corregir (a) a (f) |
| H-14 | baja | `revisores/r02_05_nivel_y_minimo_de_a.py <wt2> 4000` (punto 2) | **Esperado** (r01 H-08): con lo que el banco admite, el nivel declarado se cumple. **Obtenido:** con nivel 0,90 y 10 fechas por lado, 14,1 % (normal), 15,3 % (t de 3) y 15,8 % (lognormal) de rangos firmes sin habilidad, con un nominal del 10 %: el mismo exceso relativo (×1,4–1,6) que salía con 0,80. Subir el nivel no corrige el rango estrecho del remuestreo con pocas fechas. Lo atenúan el veredicto conjunto (hay que ganar a las dos referencias) y la nula realista (`r03_09`, 10–14 %). El nivel 0,90 es `[PROPUESTO]` y está declarado | Ensanchar el rango con pocas fechas (factor √(n/(n−1)) o cuantiles de t de Student) o subir el mínimo de fechas; volver a medir con `r02_05`. Que el análisis no diga que 0,90 resuelve el exceso |
| H-15 | baja | `revisores/r02_02_datos_durante_la_ejecucion.py` (caso 8b) | **Esperado:** el banco acepta los universos que acepta A (`cargar_universo` lee con `dtype=str`). **Obtenido:** con un universo en el que todos los símbolos parecen números («0700», «7203»…), la línea 835 (`pd.read_csv(tit["universo"], usecols=…)` sin `dtype=str`) los lee como 700 y 7203, y el banco se detiene con «no hay datos para 5». La huella de antes sí los lee como texto. Falla cerrado. Viene de antes de 0.5.0 | Leer el universo con `dtype=str, keep_default_na=False` en `ejecutar_a`, como en `_simbolos_del_universo`. Prueba con símbolos numéricos |
| H-16 | baja | `revisores/r02_06_mutantes.py <worktree>` | **Esperado:** las pruebas de la r02 protegen lo nuevo. **Obtenido:** viven R03 (la huella del universo sin la clase: un símbolo que cambia de clase daría la misma huella), R05, R07 (la comprobación de después sin el universo), R09, V13 (los avisos no se imprimen), K17 («llamadas» vacía cuenta 0), Q19 (nivel mínimo 0,89) y Q22. Además, `test_t133_r02_h08_…` llama a `bm.main(["a", …, "--salida", "x", "--nivel", "0.85"])` esperando `SystemExit`: con el mutante Q20 (nivel mínimo 0,85) **ejecutó A de verdad, escribió `x/` en la carpeta actual y anotó en el registro por defecto del agente** («wtm»/.docs/experimentos/registro_claude.jsonl). Ejecutada en el árbol principal, una regresión así escribiría en el registro real | Pruebas: universo con una clase cambiada → otra huella; filas en otro orden → la misma; universo cambiado durante la ejecución → se detiene; símbolo sin CSV → `BancoError`; stderr de `verificar` con el aviso; «llamadas» vacía → error; `--nivel 0.89` rechazado. La prueba de H-08 con `--salida` en `tmp_path` y `--sin-registro` |
| H-17 | baja | `cd <worktree> && .venv/bin/python -B .docs/tickets/T-133/banco_medida/mutantes.py`; contraste con `revisores/r02_07_mutantes_del_implementador_en_worktree.py <worktree>` | **Esperado:** `mutantes.py` mide si las pruebas matan cada mutante (el análisis cita «79 mutantes muertos» como evidencia). **Obtenido:** copia `.docs/scripts` a un temporal sin `bloque_a`; desde 0.5.0 el banco lee la configuración de A al importarse, y en esa copia la importación falla con `NameError` (H-11). Los 79 «mueren» en 61 s por un error de colección, sin ejecutar ninguna prueba: también moriría cualquier mutante que viva. Ejecutados en un worktree completo, los 79 mueren de verdad, así que la afirmación es cierta, pero la herramienta no la sostiene | Que `mutantes.py` trabaje en un worktree (o copie también `bloque_a/11_Ejecutor/config`) y que compruebe que la suite pasa sin mutar antes de empezar, como `r02_07` |

### Decisiones `[PROPUESTO]`

- **Datos cambiados = otra variante del mismo experimento.** Está implementada: la fuente es `cliente <x>` y el máximo de variantes se gasta. Está declarada en la fila T-133 de la deuda, en el código y en el análisis, y falla del lado cerrado. No bloquea. Dos consecuencias que conviene que el operador sepa al decidir:
  - la misma carpeta copiada a otra ruta, o el mismo universo con otro nombre, es otra variante, porque la ruta entra en el prerregistro (H-13 f);
  - con `max_variantes` 1, el primer intento con el cliente real gasta el experimento para siempre, y unos datos nuevos (los de K) solo se miden prerregistrando aparte y usando `--experimento`.
- **Nivel mínimo 0,90.** Implementado (en `diferencia`, en `ejecutar_a` y en la línea de órdenes) y declarado. No bloquea. Su motivo en el análisis («al 0,80 salía un 24,5 %») no queda resuelto: con 0,90 el exceso relativo sigue (H-14).

### Invariantes del sistema

- **Órdenes, F y G:** el banco no llega a ninguna orden ni toca F o G.
- **LLM:** no hay LLM en la huella, la comprobación, `verificar` ni la estadística.
- **Controles:** no se relajan solos dentro del banco. Pero el mínimo de fechas sigue a la configuración de A sin suelo propio: si A lo baja, el banco lo baja sin que nadie lo decida para el banco (H-11).
- **Falla cerrado:** sí en todo lo nuevo, con dos salvedades: la importación falla con `NameError`, no con `BancoError` (H-11); y la huella incompleta hace pasar por iguales entradas distintas (H-10), aunque eso no permite adoptar nada.
- **Números a mano:** el mínimo se lee de A; 0,90 y 0,99 están `[PROPUESTO]` en la deuda.
- **Decisiones del operador:** las dos de la r02 están `[PROPUESTO]` en la fila T-133.
- **Secretos y datos personales:** ninguno (`tools/secrets_scan.py` limpio con los scripts r02).
- **Documentación:** H-13.

### Lo que no se pudo comprobar

- El banco con el cliente real (regla 4; sin clave ni presupuesto) y con los datos de K (T-86 no ha llegado).
- Que A lea de verdad el CSV de un índice de referencia que no está en el universo: el cliente simulado solo analiza DIV (referencia CESTA). Con `--clases RV` no da selecciones, y un espía del proveedor CSV vio solo los 55 CSV del universo. La lectura sale del código de A (H-10). Lo de las columnas del universo sí se vio con A de verdad.
- `r01_03` no se volvió a ejecutar (su ruta no cambió).

### Veredicto

**APTO.** Se cumplen CA-1 a CA-4 y no queda ningún hallazgo crítico ni alto.

Los tres medios de la r01 están corregidos y probados (H-01, H-02 y H-03), y el defecto que hacía fallar CA-2 (`r03_10`) ya no está. Las dos decisiones nuevas están `[PROPUESTO]`, declaradas e implementadas del lado cerrado.

Quedan para la deuda, con su ID:
- el medio **H-10** (la huella no recoge todo lo que lee A; no permite adoptar, pero el prerregistro no identifica las entradas);
- los bajos **H-11** a **H-17**;
- los restos bajos de la r01: **H-05** (H5 sin motivo propio), **H-06** (sigue en H-12), **H-07** (sigue en H-13) y **H-08** (sigue en H-11 y H-14).

### Gate

`./tools/check_all.sh` una sola vez en el worktree «wt» limpio: **12/12 en verde**, código 0 (38 min 36 s).

| Gate | Resultado |
| --- | --- |
| Corpus, NFC, YAML, secretos, refs-vivas | en verde |
| ruff | 2831 de cuota 2831 |
| mypy | A 109/109, A-Forex 174/174, B 159/159 |
| pytest | A 6.624, A-Forex 68, B 176 |

El gate no ejecuta las pruebas de `.docs/scripts/`: se ejecutaron aparte, con 231 en verde.
