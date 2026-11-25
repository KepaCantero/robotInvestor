# T-199 · Bloque A: las pruebas de tiempo miden CPU, no reloj, y aguantan una máquina cargada

| Campo | Valor |
| --- | --- |
| Estado | CERRADO (24-11-2026, QA r02 APTO sin hallazgos abiertos) |
| Pieza | bloque_a (pruebas): `bloque_a/11_Ejecutor/tests/` (once ficheros de prueba y un módulo auxiliar nuevo, `tiempo_cpu.py`) |
| Planifica · implementa · QA | claude · claude · otro agente o un revisor nuevo |
| Aprobación del operador | no necesaria: calidad de la suite, sin caso del plan de pruebas ni decisión nueva |
| Deuda técnica | T-199 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` (sigue a T-168, que dejó apuntadas las once pruebas) |

## Objetivo

Que el gate deje de caer por la carga de la máquina. El 18-11-2026, `test_t165_g3_met13.py::test_coste_lineal_en_una_frase_larga_y_en_muchas_fichas_por_parrafo` falló en el gate de un commit (`commit_limpio_gate_20261118_122103.log`: 1 fallo de 8 266, a los 52 min de suite); sola pasa en 1,5 s. T-168 resolvió lo mismo en las cuatro pruebas de `test_t102_filtro.py` pasando a `time.process_time()` y dejó apuntadas otras once que miden reloj.

## Inventario (las tres suites)

Búsqueda de `time.time`, `perf_counter`, `monotonic`, `process_time`, `datetime.now`, `sleep`, `timeout`, `Barrier`, `join(`, `.wait(` y `Event` (r02, H-03) en `bloque_a/11_Ejecutor/tests` y `bloque_b/11_Ejecutor/tests`. B no tiene ninguna prueba de tiempo. En A:

| Prueba | Medía | Camino | Qué protege |
| --- | --- | --- | --- |
| `test_t123_r8_iban_y_tarjetas::test_el_coste_es_lineal` | reloj, < 10 s | CPU | R8 (IBAN y tarjetas) en 1,6 MB sin retroceso |
| `test_t92_revision::test_r02_h17_r8_sin_retroceso_cuadratico` | reloj, < 2 s ×4 | CPU | R8 de claves «sk-» sin retroceso |
| `test_t103_r8_y_bajos::test_r02_h47_r8_lineal_con_un_tramo_largo_de_barras` | reloj, < 2 s | CPU | R8 con 100 000 barras (antes 129 s y 114 s) |
| `test_t130_r8::test_h08_coste_lineal` ×3 | reloj, razón < 10 y < 3 s | CPU, mínima de 3 intercaladas | ×4 de texto, como mucho ×10 de tiempo |
| `test_t113_deuda::test_h56_contenido_sensible_lineal_con_mucho_anidamiento` | reloj, < 5 s | CPU | H-56: profundidad × tamaño |
| `test_t113_deuda::test_r02_h01_lineal_con_listas_de_diccionarios` | reloj, < 20 s | CPU | listas de 50 000 niveles |
| `test_t113_deuda::test_r02_h01_la_misma_lista_en_muchos_sitios_se_mira_una_vez` | reloj, < 5 s | CPU | 2²⁶ caminos, 27 listas |
| `test_t165_g3_met13::test_coste_lineal_en_una_frase_larga_y_en_muchas_fichas_por_parrafo` | CPU (ya), razón < 6 | CPU, mínima de 3 intercaladas, ×8 con tope 12 (r02, H-01) | G3-MET-13 lineal |
| `test_t144::test_h03_indice_grande_con_salida_y_exclusion_sin_fechas_comunes` | reloj, < 60 s | CPU | H-03: n²·T (164 s en T-135) |
| `test_fase2_riesgo::test_la_ficha_mas_cara_en_su_cota_cabe_en_tiempo` | reloj, < 30 s | CPU | SIM-MC-001 en su cota |
| `test_fase2_series::_rapido` (21 pruebas de cotas) | reloj, < 2 s | CPU | el rechazo por la cota llega antes de calcular |
| `test_fase2_series::test_st_inf_n_minimo_de_potencia_acotado` | reloj, < 2 s | CPU | la búsqueda del n mínimo no pasa de la cota |
| `test_fase2_series::test_st_inf_la_busqueda_del_n_minimo_empieza_en_la_aproximacion` (nueva, r02, H-02) | — | recuento de `_potencia_t` (≤ 1 y ≤ 20; corta a las 50) | la búsqueda empieza en la aproximación: una búsqueda desde 2 (2 520 evaluaciones, 0,5 s) cabe en el tope de tiempo, no en el recuento |
| `test_t102_filtro::test_textos_largos_en_tiempo_lineal` (T-168; r02, H-04) | CPU con recolector, < 2 s | CPU sin recolector (`medir_cpu`) | margen ×3,6 (0,48–0,56 s) |
| `test_t102_filtro::test_r04_muchos_espacios_en_tiempo_lineal` (ídem) | CPU con recolector, < 2 s | ídem | margen ×7,7 (0,19–0,26 s) |
| `test_t102_filtro::test_r05_h37_sufijo_en_tiempo_lineal` (ídem) | CPU con recolector, < 2,0 s | ídem | margen ×1,8 (0,98–1,11 s), el menor de la suite; el tope es el de T-168 y no se sube |
| `test_t102_filtro::test_r06_h45_marcador_y_muchos_espacios_en_tiempo_lineal` (ídem) | CPU con recolector, < 1,0 s | ídem | margen ×10 (0,09–0,10 s) |
| `test_t174_pb61_revision_c2` (`sleep(0.3)`, `barrera.wait(60)`, `join(900)`) | — | se queda | el `sleep` ensancha a propósito la ventana de la carrera entre dos hilos; no hay aserción de tiempo |
| `test_t178::test_r02_h01_dos_runs_concurrentes_no_duplican_la_p3` (`Barrier(timeout=3)`) | — | se queda | con el código bueno la barrera tiene que romperse (un hilo espera al otro, que tiene el bloqueo): mide de verdad tiempo de pared. La carga solo puede debilitarla (el mutante sin transacción podría no cruzarse), nunca hacerla fallar |
| `test_t177_c4_credenciales` (`barrera.wait(30)`, `join(60/120)`, `subprocess timeout=600`), `test_t87_controles` (`proc.wait(30)`), `test_t157_verificador_ids` y `test_v51` (`timeout=300/600`), `test_t65_resto_t53` (`join(60)`) | — | se quedan | esperas a otros hilos o subprocesos, con holgura: tiempo de pared real (un subproceso no cuenta en `process_time`) y solo cortan un cuelgue |
| `test_t106_motor` (`time.time_ns()`) | — | se queda | fija la fecha de modificación de un fichero; no mide nada |
| `test_t87_contratos::test_peticion_idempotente_concurrente_durable_y_con_huella` (`assert dentro.wait(10)`, `assert continuar.wait(10)`) (r02, H-03) | — | se queda | espera a que el otro hilo llegue a un punto (milisegundos); los 10 s solo cortan un cuelgue. Es la de menos holgura, pero estrangulada al 10 % siguen siendo 1 s de CPU del otro hilo |
| `test_t146_presupuesto::_ciclo_en_orden` (`assert hechos[…].wait(600)`) (r02, H-03) | — | se queda | cada hilo espera a que acabe el anterior para ejecutar en orden; solo corta un cuelgue |
| `test_t65_resto_t53` (`assert turnos[clase].wait(30)`) (r02, H-03) | — | se queda | turnos entre hilos, como la anterior; la tabla de la r01 solo citaba su `join(60)` |
| `test_t169_r02`, `test_t176_pb36_pb33`, `test_t177_c4_credenciales:326` (`Barrier(n)` sin `timeout`) (r02, H-03) | — | se quedan | arrancan varios hilos a la vez; sin plazo, no dependen del tiempo |
| `test_t147`, `test_t149`, `test_t150` (`falso(url, timeout=None)`), `test_t151_reintentos` y `test_t154` (`timeout` simulado) | — | se quedan | el `timeout` es un parámetro o una excepción simulada, no una espera |

Fuera de las suites del gate: `bloque_*/10_Herramientas/tests/test_ht02_verificador_enlaces.py` (`sleep(1.5)`) es corpus congelado y no lo ejecuta `check_all.sh`.

Contar operaciones sirve donde el coste son llamadas de Python. En ST-INF-001 se cuentan las evaluaciones de `_potencia_t` (r02, H-02). En las demás no sirve: lo que vigilan es el retroceso de expresiones regulares, bucles numpy o repasos de prefijos, y eso ocurre dentro de una sola llamada (un repaso cuadrático hace una llamada por bloque, cada una más cara). Ningún recuento necesitaba un contador en producción: `monkeypatch` sobre `_potencia_t` basta.

## Alcance

- **Entra:** las doce pruebas de la tabla marcadas «CPU» (más las 21 de cotas que usan `_rapido`), las cuatro de T-102 y una prueba nueva por recuento en ST-INF-001 (r02); `tests/tiempo_cpu.py` (nuevo); una corrección de ruff en `test_t92_revision.py` (orden de imports, ya estaba) y la cuota de ruff.
- **No entra:** código de producción (ningún contador hacía falta); las pruebas que se quedan, justificadas arriba; los ficheros del corpus congelado (ninguno de los tocados está en `tools/corpus_manifest.txt`).

## Diseño

- `tests/tiempo_cpu.py`: `medir_cpu()` (gestor de contexto) y `cpu(f)` miden `time.process_time()` con el recolector de basura parado; `minimos_intercalados(f, g)` repite cada medida tres veces alternando los tamaños y se queda la mínima de cada uno.
  - **CPU:** lo que hacen otros procesos no cuenta (T-168).
  - **Sin recolector:** su coste depende de lo que dejan vivo las 8 000 pruebas anteriores del mismo proceso, no de la función. Con 6 millones de objetos vivos, la razón de T-165 llegaba a 5,6 con la máquina libre.
  - **Mínima intercalada:** la carga que comparten los núcleos (caché, memoria, frecuencia) también sube el tiempo de CPU; la mínima de tres, alternando, evita que una ráfaga caiga solo sobre uno de los tamaños.
- Topes: los mismos en todas, salvo T-165 (INC-T199-01): con ×4 de texto y tope 6, la razón medida con carga llegó a 5,97 (y a 4,94 con la mínima intercalada), porque con la memoria disputada el texto largo sufre más. Pasa a ×8 de texto (1 000 → 8 000 unidades) con tope 12 (r02, QA r01 H-01: la r01 ponía 16): ×1,5 de lo lineal, el margen relativo de `develop`. Para un coste lineal + cuadrático (b·n + a·n²) falla en cuanto el término cuadrático, al tamaño largo, pasa de 0,62 veces el lineal (`develop`: 0,8; con tope 16: 1,33). Peor razón medida con carga: 9,63 en la r01 y 8,94 en la r02 (margen 1,25 o más).
- **Estado persistido:** no cambia. **Números de producción:** ninguno. **Corpus:** no se toca.

## Criterios de aceptación

1. CA-1: ninguna prueba de las tres suites mide reloj para afirmar un coste; las que esperan a otros hilos o procesos están justificadas una a una (tabla de inventario).
2. CA-2: las doce pruebas pasan con la máquina cargada (8 procesos de CPU y 4 de copia de memoria en 4 núcleos, carga de 13 a 20).
3. CA-3: cada prueba falla con su mutante de coste (cuadrático, o el defecto que vigila), también con la máquina cargada. Límite declarado: en las de tope absoluto, un cuadrático cuyo coste a ese tamaño quede por debajo del tope no las hace fallar (como en T-168). En las de razón (T-130, T-165), las hace fallar uno cuyo término cuadrático pase de una fracción fija del lineal (en T-165, 0,62). En ST-INF-001 (r02) el recuento caza también una búsqueda lineal. No queda ningún mutante vivo.
4. CA-4: lo que protege cada prueba no se debilita: los topes no cambian, salvo T-165, que con ×8 y tope 12 es más estricta que `develop` (INC-T199-01, corregida en la r02).
5. CA-5: las líneas base no bajan, ninguna cuota sube y `./tools/check_all.sh` queda en verde (12/12).

## Plan de pruebas

| Prueba | Tipo | Criterio |
| --- | --- | --- |
| Búsqueda en las tres suites (`pruebas.md`, orden exacta) | inventario | CA-1 |
| Las doce pruebas con carga artificial (`mutantes.py --originales`) | regresión, carga | CA-2 |
| Las de `develop` con la misma carga | regresión (sin el cambio) | CA-2 |
| `mutantes.py`: M01 a M19 con carga (M14–M15, H-01; M12–M13 por recuento, H-02; M16–M19, T-102, H-04) | mutantes | CA-3 |
| Scripts del revisor `r01_01`, `r01_02`/`r01_03`, la tanda estrangulada de `r01_05` y `razon_t165.py 1000` (`r01_06`) | regresión de la QA | CA-2, CA-3, CA-4 |
| Diferencia de las pruebas (`git diff`) | revisión | CA-4 |
| Suites de A y B, `check_all.sh` | regresión | CA-5 |

## Scripts

`.docs/tickets/T-199/mutantes.py` (`--originales` ejecuta también las doce sin mutar), `carga.sh` (carga artificial), `estrangular.py` (deja correr un proceso una fracción del tiempo) y `razon_t165.py` (la razón de T-165 con un montón grande), todos nuevos y en la carpeta del ticket.

## Registro

- 2026-11-24 · ABIERTO · claude · encargo del operador (gate caído el 18-11-2026 por la prueba de T-165)
- 2026-11-24 · PLANIFICADO · claude · inventario de las tres suites: doce pruebas a CPU, el resto justificadas
- 2026-11-24 · EN CURSO · claude · `tiempo_cpu.py`, diez ficheros de prueba, 13 mutantes
- 2026-11-24 · EN QA (r01) · claude · pruebas con carga y mutantes en `pruebas.md`; gate completo; commit local
- 2026-11-24 · EN CURSO (r02) · claude · QA r01 NO APTO (H-01 medio; H-02 a H-04 bajos): T-165 con tope 12, recuento en ST-INF-001, cuatro esperas más en el inventario y T-102 con `medir_cpu`
- 2026-11-24 · EN QA (r02: QA r01 NO APTO) · claude · 19 mutantes muertos, scripts del revisor repetidos, gate completo; commit local
- 2026-11-24 · QA r02 · APTO sin hallazgos nuevos: los cuatro de la r01 cerrados, cada uno con su prueba (`qa.md`).
- 2026-11-24 · CERRADO · claude: integrado en `develop` con `commit_limpio.sh`.
