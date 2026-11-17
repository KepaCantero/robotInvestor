# T-168 · QA independiente

- **Revisor:** claude, subagente revisor nuevo (no implementó; solo plan, código y pruebas) · **Ronda:** r01 · 16-11-2026

## Reproducción desde limpio

Copia propia: `git worktree add --detach <scratchpad>/qa168 HEAD` (HEAD = `a621e9c`, que ya contiene el commit de T-168
`5aa9681`; en el árbol principal no quedaban cambios de T-168 sin commit). Venv `/home/user/robotinvestor/.venv`. Por
indicación del coordinador (otros agentes trabajan a la vez, carga ≈ 9 en 4 núcleos) no se pasaron la suite completa de A
ni `./tools/check_all.sh`: solo el fichero afectado y los scripts del revisor.

| Orden (desde `bloque_a/11_Ejecutor` de la copia) | Resultado |
| --- | --- |
| `pytest -q tests/test_t102_filtro.py -k tiempo_lineal --durations=4` ×3, carga ≈ 9 | 4 passed las tres veces; la más lenta (`r05_h37`) 0,88–0,95 s de reloj |
| `pytest -q tests/test_t102_filtro.py` (fichero entero, 260 pruebas), carga ≈ 8,3 | 260 passed |
| `-k tiempo_lineal` con 8 quemadores de CPU extra (carga 10,6 → 13) | 4 passed; reloj `r05_h37` 4,40 s y `textos_largos` 4,00 s (con `perf_counter` habrían caído: tope 2 s) |
| `ruff check tests/test_t102_filtro.py`, antes (`5aa9681~1`) y después | 0 avisos en ambos: la cuota no se mueve |

Scripts del revisor (`revisores/`, ronda r01; ver nota al final):

- `r01_01_cpu_frente_a_reloj.py [n_quemadores]`: las cuatro cargas con reloj, CPU del proceso y CPU del hilo principal.
  Sin carga extra: reloj 0,50 / 0,15 / 0,90 / 0,11 s, CPU 0,39 / 0,13 / 0,73 / 0,10 s. Con 12 quemadores extra: reloj
  **4,08 / 1,79 / 5,66 / 0,23 s**, CPU **0,33 / 0,13 / 0,71 / 0,06 s**. CPU del proceso = CPU del hilo principal en las cuatro;
  0 hilos nuevos; 0,000 s de CPU de hijos.
- `r01_02_mutantes_cuadraticos.py`: inyecta seis mutantes en `bloque_a/diseno_v6.py` (en la copia; el original se restaura
  siempre) y pasa las cuatro pruebas. Original: 4 passed. Q1 (`[ \t]+$`, el tipo de H-26): caen `r04` y `r06`. Q2
  (`(?:[A-Z]\.)+[a-z]`, H-37): cae `r05`. Q3 (`(?:[A-Z][a-z]+ )+[a-z]`): cae `r05`. Q4 (`(?:\w+[ ,]+)+;` en
  `texto_prohibido`): cae `textos_largos`. **Q5** (`t[:i].rfind` por cada posición, cuadrático en C: 0,03 s por cadena a
  50 000, ×4,5 al doblar) y **Q6** (`t[i:].count(" ")` por cada posición: 0,52 s por cadena, 1,7 s en la prueba) **sobreviven**
  (H-01).
- `r01_03_hilos_en_la_medicion.py`: plugin de pytest; con el fichero entero, en las cuatro pruebas: hilos 1→1, CPU de hijos
  0,000 s; reloj 0,44 / 0,14 / 1,05 / 0,13 s frente a CPU 0,31 / 0,13 / 0,72 / 0,08 s.

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 · las cuatro miden `process_time` y conservan sus topes | sí | `git show 5aa9681`: solo cambian `perf_counter`→`process_time` en las ocho llamadas; topes 2, 2, 2.0 y 1.0 iguales. Ninguna otra prueba del fichero mide tiempo |
| CA-2 · pasan con la máquina cargada | sí | 4 passed con carga 8–13 sobre 4 núcleos (incluidos 8 quemadores extra), con relojes de 4,0–4,4 s que la versión anterior no habría aguantado; `r01_01` con 12 quemadores: CPU sin cambio (0,71 frente a 0,73 s) |
| CA-3 · un filtro que vuelva a coste cuadrático las hace fallar | sí, para el defecto vigilado (con H-01) | `r01_02`: los cuatro mutantes de retroceso de expresiones regulares (la clase de H-26, H-37 y H-45) caen, cada uno en la prueba de su carga. Un cuadrático cuyo coste a estos tamaños queda bajo el tope (Q5, Q6) no cae, igual que antes de T-168 sin carga: el cambio no debilita la detección, pero el criterio escrito promete más |

Comprobaciones pedidas:

- **`process_time` mide solo la CPU del proceso:** en Linux es `CLOCK_PROCESS_CPUTIME_ID` (usuario + sistema de todos los
  hilos del proceso, sin hijos ni tiempo dormido o en espera). Sin efecto en la ruta medida: las tres funciones
  (`texto_prohibido`, `limpiar`, `frase_prohibida` de `bloque_a/diseno_v6.py`) son Python puro con `re` y `unicodedata`, sin
  E/S, hilos ni procesos (los `ThreadPoolExecutor` del paquete están en `orquestacion.py` y `ht02_verificador_enlaces.py`, con
  `with`, fuera de esta ruta); la fixture `perm` se calcula fuera de la medición. Medido: CPU del proceso = CPU del hilo
  principal, 0 hilos nuevos, 0 s de hijos (`r01_01`, `r01_03`). Nada escapa a la medición.
- **Sentido del error:** un hilo ajeno vivo en el proceso solo podría sumar CPU (falso fallo, no falso pase); con el fichero
  entero hay un solo hilo.

Invariantes: el cambio solo toca pruebas; ni F/G, ni LLM, ni controles, ni estado. Ningún número nuevo (los topes son los de
antes). Sin secretos ni datos personales. Deuda técnica al día (línea T-168 en EN QA).

## Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | baja | `python .docs/tickets/T-168/revisores/r01_02_mutantes_cuadraticos.py` desde `bloque_a/11_Ejecutor` de una copia | CA-3 y «Margen» del README dicen que «un regreso a coste cuadrático sigue fallando»; Q5 y Q6, cuadráticos de constante baja (0,1 s y 1,7 s a estos tamaños), pasan. Las pruebas son de tope absoluto: cazan el retroceso de expresiones regulares (Q1–Q4), no cualquier cuadrático. No lo introduce T-168 (con `perf_counter` y sin carga pasaban igual) | En `README.md` del ticket, CA-3 → «3. Un filtro que vuelva al defecto vigilado (retroceso de expresiones regulares, H-26, H-37 y H-45 de T-102: segundos a estos tamaños) las hace fallar. Límite declarado: un cuadrático cuyo coste a estos tamaños quede bajo el tope (mutantes Q5 y Q6 de la QA r01) no las hace fallar, igual que antes de T-168.»; y en «Diseño · Margen», cambiar «así que un regreso a coste cuadrático sigue fallando» por «así que un regreso a ese defecto sigue fallando (un cuadrático de constante baja, no: ver CA-3)» | corregido (ronda de cierre) |
| H-02 | baja | `grep -rn "perf_counter" bloque_a/11_Ejecutor/tests/*.py` | README («No entra») y la línea T-168 de la deuda hablan de «otras diez pruebas que miden reloj con `time.perf_counter() - t0 <`»; hay once sitios: el patrón deja fuera `tests/test_t130_r8.py::test_h08_coste_lineal` (3 casos), que mide reloj en un auxiliar `tarda()` con tope de 3,0 s y razón 10× | En el README («No entra») y en la línea T-168 de `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md`, «otras diez pruebas» → «otras once pruebas que miden reloj (`test_t92_revision`, `test_t103_r8_y_bajos`, `test_t113_deuda` ×3, `test_t123_r8_iban_y_tarjetas`, `test_t130_r8::test_h08_coste_lineal`, `test_t144`, `test_fase2_series` ×2 y `test_fase2_riesgo`)» | corregido (ronda de cierre) |
| H-03 | baja | Leer `pruebas.md` | Solo registra la pasada con carga ≈ 1; no hay evidencia propia de CA-2 (con carga) ni de CA-3 (un cuadrático cae) | Añadir a la tabla de `pruebas.md` dos filas: «`-k tiempo_lineal` con 8 quemadores extra (carga 10,6–13): 4 passed; reloj de `r05_h37` 4,40 s, CPU < 1 s (CA-2; QA r01, `r01_01`)» y «Mutantes de retroceso Q1–Q4 de la QA r01 (`r01_02`): los cuatro caen; Q5–Q6 son el límite de H-01 (CA-3)» | corregido (ronda de cierre) |

Nota sobre los scripts: por la regla del coordinador de no tocar el árbol principal salvo este `qa.md`, los tres scripts
`r01_01_cpu_frente_a_reloj.py`, `r01_02_mutantes_cuadraticos.py` y `r01_03_hilos_en_la_medicion.py` están en la copia del
revisor (`<scratchpad>/qa168/.docs/tickets/T-168/revisores/`). En la ronda de cierre hay que copiarlos a
`.docs/tickets/T-168/revisores/` (sin cambiarlos) para que se puedan repetir.

## Veredicto

**APTO** · CA-1, CA-2 y CA-3 se cumplen (CA-3 para el defecto que vigilan las pruebas); `process_time` mide toda la ruta (un
hilo, sin hijos ni E/S) y las cuatro pasan con la máquina cargada al triple de su capacidad mientras siguen cazando los cuatro
mutantes de retroceso. Ningún hallazgo crítico, alto ni medio. Por la regla del operador, H-01, H-02 y H-03 (bajos) se
subsanan en este mismo ticket con una ronda de cierre (las correcciones de arriba, solo texto) y se copian los scripts a
`revisores/` antes de pasar T-168 a CERRADO.

## Ronda de cierre

Revisada en el árbol principal el 16-11-2026, sin cambios de código (solo texto del ticket y de la deuda).

| ID | Estado | Comprobación |
| --- | --- | --- |
| H-01 | corregido | `README.md`: CA-3 y «Diseño · Margen» llevan el texto pedido, literal (`git diff`) |
| H-02 | corregido | «otras once pruebas» con la lista de ficheros en `README.md` («No entra») y en la fila T-168 de la deuda; la lista coincide con `grep -rn perf_counter bloque_a/11_Ejecutor/tests/*.py` |
| H-03 | corregido | `pruebas.md`: las dos filas nuevas (CA-2 con 8 quemadores, `r01_01`; CA-3 con Q1–Q4, `r01_02`) |
| Scripts | copiados | `revisores/r01_01_cpu_frente_a_reloj.py`, `r01_02_mutantes_cuadraticos.py` y `r01_03_hilos_en_la_medicion.py`, idénticos byte a byte a los de la copia del revisor (`cmp`) |

**Veredicto final: APTO**, sin hallazgos abiertos. Fila T-168 de la deuda en CERRADO.
