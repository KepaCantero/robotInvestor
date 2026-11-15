# T-146 · QA independiente

- **Revisor:** revisor nuevo sin contexto de la implementación (subagente de Claude; implementó Claude) · **Ronda:** r01 · 2026-11-15
- **Copia:** extracción git en el scratchpad (HEAD `cfd8f08`, «instantánea para QA de T-146»), intérprete `/home/user/robotinvestor/.venv/bin/python`. Sin red, sin la API y sin coste: el cliente real es `llm.AnthropicClient` sobre SDK falsos locales. No se lanzan `./tools/check_all.sh`, A-Forex ni B (fuera del encargo).

## Reproducción desde limpio

| Comprobación | Resultado |
| --- | --- |
| Suite completa de A, una vez (`cd bloque_a/11_Ejecutor && python -m pytest -q -p no:cacheprovider`) | **6183 passed** en 24 min 15 s (línea base de A ≥ 607); exit 0 |
| `python tests/goldens_ct.py` | «goldens de contratos: coinciden» |
| ruff desde la raíz, tres ejecutores (`… \| wc -l`) | 2838 (cuota 2838) |
| mypy de A como el gate (`--ignore-missing-imports --no-error-summary bloque_a \| wc -l`) | 109 (cuota 109) |
| `tools/secrets_scan.py`, `tools/refs_vivas.py`, `tools/nfc_check.py`, `tools/corpus_integridad.py` | sin hallazgos · rutas vivas · NFC · 695 archivos íntegros |
| `peor_caso_por_bolsa.py` y SDK de peor caso del implementador (`r01_02 … ` sin opciones, solo divisas) | DIV 25,355 / 25,355; COMÚN 31,96; suma = gastado = 57,316; sin excesos (reproduce el análisis) |
| `comparar_ciclos.sh` (antes = `19f3f3b`) | igual que lo declarado: entregables iguales salvo la línea de consumo del informe técnico de los 12 tipos (62,46 → 64,38 UC); 9 recortes del Analista en las semanas N1 (12 000 → 11 785–11 820); +9 AUT- DENEGADA en HA; COMÚN con AG-20 y AG-18; F3/F4/RC solo cambian en `_ts`, `_hash*` y `fecha_congelacion` (el tic del reloj) |
| `mutantes_t146.py` (copia desechable `…/qa19_mut_t146_mut`) | **26/26 muertos** (M25 incluido) |
| Mutantes propios `revisores/r01_05_mutantes_qa.py` (copia `…/qa19_mut_q`) | 9/12 muertos; vivos Q01 (`pagar_resto` no suelta lo que no salió: `cerrar` lo suelta después, más prudente), Q09 (el cliente real no paga cada petición: las reservas de peor caso siguen ocupadas hasta `pagar_resto`, más prudente) y Q12 (`_cargar` sin el prefijo de la primera petición: el cálculo de reserva por intentos da lo mismo en las pruebas). Ninguno abre un camino de gasto; ver H-10 |

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 (peor caso, divisas: ninguna bolsa pasa, todo en las bolsas, ninguna petición cuesta más de lo reservado) | **no** (en vivo con búsquedas) | Con el SDK del implementador, sí. Con búsquedas que traen lectura (la entrada que cobra la API en la misma petición) una petición cuesta más de lo reservado y la bolsa pasa de su límite (`r01_01` U3: 23,48 / 22,50); junto con un tokenizador peor que 1,35, seis bolsas de los 12 tipos pasan su límite hasta 1,47 UC (`r01_02 --lectura 6000 --factor 1.6`). Declarado como límite conocido (H-04), pero el criterio no se cumple en el modo para el que se hace. |
| CA-2 (12 tipos y 6 hilos; determinismo con 4 tipos y 4 hilos; V6) | **no** | Las cotas se cumplen con el SDK de peor caso (12 tipos, 6 hilos y V6). El determinismo **no**: con una caché de prompts como la de la API (quien llega antes escribe el prefijo compartido y los demás lo leen), dos ejecuciones iguales dan F5 distintos y el orden de los hilos cambia presupuesto, ampliaciones, cierres y llamadas (H-02). Antes de T-146 (`19f3f3b`) el mismo ataque da el mismo F5 en los dos órdenes. |
| CA-3 (AG-18/19/20 en COMÚN; sin sitio, AG-20 no sale; controles con ampliación) | sí, con matiz | Pruebas `test_ca3_*` en verde; `r01_02` (12 tipos) carga AG-19 en COMÚN y gastado = cargado. Matiz: con el reparto escalado, lo de AG-20 pasa el límite de COMÚN (H-03). |
| CA-4 (búsquedas en UC, reservadas al máximo) | sí | `test_ca4_*`; `r01_02`: 30 búsquedas cobradas; `busquedas_maximas` = `max_uses` (por petición según el SDK instalado). |
| CA-5 (reserva petición a petición) | sí, con matiz | `r01_01` U1 (32 hilos, nunca pasa), U6 (continuación que no cabe: no sale, `presupuesto_agotado`), U7 (reparación que no cabe: no sale; lo pagado = lo cargado; cierre declarado). Matiz: el «factor observado» mezcla la lectura de las búsquedas con el error del tokenizador (H-01). |
| CA-6 (liquidación ≤ retenido; suma de límites ≤ ciclo) | sí, con matiz | `r01_04`: la secuencia de `test_r04_h13` da los mismos totales por bolsa que antes de T-146; la suma de límites máximos = 360 con escala. Matiz: H-03 (lo absorbido de C5) y H-06 (F5 no muestra la escala). |
| CA-7 (simulado: N2 sin recortes; N1 recorta y sigue COMPLETO; comparación) | sí | `comparar_ciclos.sh` (arriba). |
| CA-8 (suites y goldens) | sí | Suite completa y `goldens_ct.py`. |
| CA-9 (mutantes muertos) | sí | `mutantes_t146.py`; los mutantes propios están aparte. |
| CA-10 (cuotas) | sí | 2838 y 109. |

## Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | **alta** | `python -I revisores/r01_01_reserva_unidad.py bloque_a/11_Ejecutor` (U4) y `python -I revisores/r01_02_ciclo_sdk_hostil.py bloque_a/11_Ejecutor <tmp> --tipos RV,RF,DIV,MP,IDX,FON,DER,INM,CRI,ALT,MON,TCV --hilos 6 --lectura 3000` (comparar con `--lectura 0`) | Esperado: el factor observado corrige el error del tokenizador. Obtenido: `ReservaLlamada.pagar` compara la entrada cobrada (que incluye lo que leen las búsquedas) con la entrada medida de la petición, así que la primera petición con búsqueda de una bolsa sube su factor a ≈ 2–5 (U4: 4,74 con 5 × 6 000 tokens) y, desde entonces, **todas** las peticiones de ese tipo, sin búsqueda, reservan varias veces su peor caso real (U4: 1,68 → 3,37 UC la misma petición). En el ciclo de los 12 tipos (modo vivo, búsqueda habilitada por defecto para AG-14/15/16), con 3 000 tokens por búsqueda la Prospectiva pasa de 18 a 14 llamadas (con 6 000, a 12): fases cerradas «por presupuesto» que su coste real no cierra. Falla cerrado, pero degrada justo el modo sombra que el ticket acota, y no está declarado (el análisis presenta el factor como corrección del tokenizador) | No observar el factor en las peticiones con `busquedas_web > 0` (probado en una copia: con ese cambio la Prospectiva vuelve a 18 llamadas con lectura y las cotas se siguen cumpliendo), o restar una estimación de lo leído; prueba de regresión con lectura de búsquedas en el SDK falso | abierto |
| H-02 | **alta** | `python -I revisores/r01_02_ciclo_sdk_hostil.py bloque_a/11_Ejecutor <tmp> --tipos RV,RF,DIV,MP --hilos 4 --cache --orden directo --veces 2` (y `--orden inverso`); contra `19f3f3b`, el mismo comando da «determinismo: IGUAL» y el mismo F5 en los dos órdenes | Esperado (T-88, CA-2 y el análisis: «las reservas, lo retenido y los recortes de una bolsa dependen solo de sus propias llamadas»): F5 igual en cada ejecución. Obtenido: «determinismo: DISTINTO» con el mismo orden y, entre órdenes, cambian consumido, ampliado, cierres, recortes y hasta las búsquedas hechas (25 frente a 15). Causa: `pagar` aparta el coste real de cada petición, que depende de si otro hilo escribió antes el prefijo compartido (AG-10, AG-11, AG-12, AG-14, AG-16); con eso se decide si caben la reparación y las continuaciones de la misma llamada. `test_ca2_determinista_con_hilos_cerca_del_limite` no lo ve porque su SDK escribe siempre toda la entrada (nunca hay lectura) | Apartar lo real con lo leído contado como escrito (independiente del orden; probado en una copia: «IGUAL» en los dos órdenes y en tres ejecuciones, sin violar cotas), y una prueba de determinismo con un SDK que simule la caché por prefijo y fuerce el orden de los hilos | abierto |
| H-03 | media | `python -I revisores/r01_03_c5_con_escala.py bloque_a/11_Ejecutor <tmp>` (12 tipos, `presupuesto_uc.N2: 100` por configuración) | Esperado: ninguna bolsa pasa de su límite. Obtenido: con escala 0,196, COMÚN tiene límite 5,88 (máximo 7,06) y AG-20 gasta 9,78 UC antes del reparto contra una bolsa C5 sin escalar (30 UC); COMÚN acaba en 9,78 y además se cierran el dictamen G3 de AG-18, la integración y la redacción. Está en «Límites conocidos» del análisis, pero no en INC-T146-01 ni probado | Crear la bolsa de C5 con la escala del ciclo (calcular el reparto, o al menos `tope_total`, antes de C5) o descontar lo de C5 del tope antes de escalar; prueba con un reparto por encima del ciclo | abierto |
| H-04 | media | `r01_01` U3; `r01_02 --tipos <12> --hilos 6 --lectura 6000 --factor 1.6` | Esperado (criterio del operador): ninguna petición sale si su peor caso no cabe. Obtenido: lo que leen las búsquedas no se reserva y el margen 1,35 es sobre una aproximación de 3,6 caracteres por token, no sobre una cota del tokenizador (JSON con cifras puede ir a ≈ 2 caracteres por token): una petición puede costar más de lo reservado y la bolsa pasa su límite (U3 +0,98 UC; seis bolsas hasta +1,47 UC). Declarado `[PROPUESTO]` en INC-T146-01 y anotado en `excesos_reserva`, pero el CA-1 se formula sin esa salvedad | Reservar una lectura por búsqueda configurable (`presupuesto_uc.reserva.tokens_por_busqueda`, `[PROPUESTO]`) y que el operador decida el margen del tokenizador; reformular CA-1 con la salvedad o medirla en el modo sombra | abierto |
| H-05 | baja | `r01_01` U9 | Una reparación que devuelve JSON muy anidado lanza `RecursionError` desde `extraer_json` (solo se capturan `JSONDecodeError`/`ValueError`): lo ya pagado (4,68 UC) está en la contabilidad pero no en la bolsa y el ciclo entero cae. El fallo es anterior a T-146; el hueco del presupuesto acaba con el ciclo | Capturar `RecursionError` en `extraer_json` (falla cerrado como JSON no válido) o cargar lo pagado en un `finally` de `_invocar` | abierto |
| H-06 | baja | `r01_03` | Con escala < 1, F5 y CT-05 siguen mostrando `asignado` sin escalar (COMÚN 24,0 con base efectiva 4,7): el registro no deja ver el límite que se aplicó | Añadir al RUN de F5 la escala o el límite efectivo por bolsa | abierto |
| H-07 | baja | lectura de las pruebas | `test_t145.py::test_h01_la_cota_cubre…` queda con `assert viejo > 0` (no comprueba nada útil; lo que importa, `usd <= nueva`, sigue). `_comprobar_cotas` de `test_t146_presupuesto.py` calcula los límites con el `asignado` sin escalar (no vería H-03). El SDK de las pruebas de CA-2 no simula lectura de caché (no ve H-02). Las otras tres pruebas cambiadas no se debilitan: `r01_04` da los mismos totales por bolsa que antes en la secuencia de `test_r04_h13`, `test_pb17` exige ahora lo ampliado = lo autorizado y el consumo dentro del límite, y `pasadas == 0` es más fuerte que `>= 1` | Quitar o sustituir la aserción vacía; usar `Presupuesto.limite` en `_comprobar_cotas`; SDK con caché en la prueba de determinismo | abierto |
| H-08 | baja (latente) | `r01_01` U2 | `Bloque._invocar` suelta la reserva (`cerrar`) antes de cargar lo real (`_cargar`): si dos hilos compartieran una bolsa, otro podría reservar en ese hueco (U2: 8,84 UC en un límite de 5). Hoy no ocurre (cada bolsa la usa un solo hilo), pero nada lo impide si cambia el reparto de hilos | Cargar lo real y soltar la reserva bajo el mismo cerrojo (o mantener lo apartado hasta después de `_cargar`) | abierto |
| H-09 | baja (observación, sin la API) | lectura de código y del SDK instalado | (a) El SDK reintenta los *timeouts* (`max_reintentos_api: 4`): si el servidor completó una petición que el cliente dejó de esperar, podría cobrarse sin reserva; no comprobable sin la API. (b) La escritura de caché a 1 h cuesta en USD el doble que la entrada y `uc_de` la cuenta como entrada (convención anterior a T-146); `uc_por_busqueda_web` sí se deriva de USD: las UC no acotan igual el gasto en USD de lo escrito en caché | Para la deuda: decidir con el operador si los reintentos de timeout se limitan y si la UC del gasto del modo sombra se contrasta en USD | abierto |
| H-10 | baja | `python revisores/r01_05_mutantes_qa.py <copia con «qa19_mut»>` | Tres mutantes propios sobreviven (Q01, Q09, Q12; detalle arriba). Son más prudentes o equivalentes en las pruebas, pero ninguna prueba comprueba que cada continuación se pague por separado (el exceso y el factor de cada petición) | Una prueba que mire `excesos_reserva` por petición en una llamada con continuaciones | abierto |

Invariantes del sistema comprobados: ningún camino nuevo llega a una orden sin F y G; no hay LLM en la ruta determinista (C6 no llama al modelo: `seguimiento.ciclo_c6` es determinista); los controles no se relajan (si AG-18 no cabe, G3 queda en la regla restrictiva, `r01_03`); falla cerrado (factor NaN → `ValueError`; factor 0 o negativo y salida mínima 0 no dejan salir peticiones en `r01_01` U8); números en la configuración con origen y `[PROPUESTO]`; sin secretos; la consulta N0 queda fuera de la reserva y declarada con su pregunta al operador. Las búsquedas desde código (filtrado dinámico) cuentan en `server_tool_use.web_search_requests` y `max_uses` es por petición según el SDK instalado; su coste de ejecución de código no se ha podido comprobar sin la API.

Scripts de esta ronda en `revisores/`: `r01_01_reserva_unidad.py`, `r01_02_ciclo_sdk_hostil.py`, `r01_03_c5_con_escala.py`, `r01_04_t88_h13_absoluto.py`, `r01_05_mutantes_qa.py`.

## Veredicto

**NO APTO** · dos hallazgos altos abiertos y dos criterios sin cumplir. H-02: el presupuesto deja de ser determinista con hilos en cuanto la caché de prompts se comparte como en la API (regresión frente a `19f3f3b`; CA-2). H-01: la lectura de las búsquedas se toma por error del tokenizador y multiplica las reservas del resto del tipo, que cierra fases en el modo sombra sin que su coste lo pida. Además, H-03 y H-04 (medios) dejan bolsas por encima de su límite en casos que el criterio del operador no admite (CA-1). La cota de gasto en sí se cumple en todo lo demás: ninguna petición sale sin reservar (primer intento, reparación, continuación, controles y C5), gastado = cargado en todos los ataques, la suma nunca pasa de 360 UC y los 26 mutantes del implementador mueren. Vuelve a `ri-implementar`: corregir H-01 y H-02 con su prueba de regresión (las dos correcciones sugeridas se probaron en una copia), decidir H-03 y H-04, y en la ronda r02 se vuelven a pasar los scripts `r01_*`.

## Ronda r02

- **Revisor:** revisor nuevo e independiente (subagente de Claude; no implementó T-146 ni hizo la QA r01) · **Ronda:** r02 · 2026-11-15
- **Copia:** git worktree en el scratchpad (`qa21`), HEAD `010108a` («T-146 r02 y T-148 r02 [pendiente QA]»), `.venv` enlazado. Sin red, sin la API y sin coste (el cliente real, sobre SDK falsos locales). Para comparar: `git archive` de `19f3f3b` (antes de T-146) y de `b0046a1` (r01). Opinión formada con el README, el diff de la r02 y el código antes de leer `analisis-tecnico.md`.

### Reproducción desde limpio

| Comprobación | Resultado |
| --- | --- |
| Suite completa de A, una vez (`cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q -p no:cacheprovider`) | **6354 passed**, 0 fallos, en 33 min 38 s (con carga: mutantes en paralelo); exit 0. El fallo de `test_t148.py::test_h04_r04_r05…` que dejó el implementador (suite lanzada con el fichero de la r01) no aparece |
| `tests/test_fase3_goldens.py` · `python tests/goldens_ct.py` | 102 passed · «goldens de contratos: coinciden» |
| ruff desde la raíz (tres ejecutores, `--output-format=concise … \| wc -l`) · mypy de A (`--ignore-missing-imports --no-error-summary bloque_a/11_Ejecutor/bloque_a \| wc -l`) | **2838** (cuota 2838) · **109** (cuota 109) |
| `tools/refs_vivas.py`, `secrets_scan.py`, `nfc_check.py`, `corpus_integridad.py` | exit 0 los cuatro; corpus **695** archivos íntegros |
| `mutantes_t146.py` (copia desechable `…/qa21_t146_mut`) | **35/35 muertos** (M01–M35) |
| `revisores/r01_05_mutantes_qa.py` (copia `…/qa21_qa19_mut`) | **12/12 muertos** (en la r01, 9/12: Q01, Q09 y Q12 mueren ahora) |
| `comparar_ciclos.sh <b0046a1> <r02> <tmp>` | mismos entregables y mismo F5 que la r01 en los tres escenarios (divisas, backtest de 13 semanas, 12 tipos); solo difieren F10 (la clave nueva), los sellos y `consumo.csv`/`cache_resultados.jsonl` (cambian también entre dos pasadas iguales) |

### Scripts de la r01, otra vez

| Orden (desde la raíz, `.venv/bin/python -I …`) | r01 | r02 |
| --- | --- | --- |
| `.docs/tickets/T-146/revisores/r01_01_reserva_unidad.py bloque_a/11_Ejecutor` | 8/12 | **10/12**: U4 OK (factor observado 0; la misma petición sin búsqueda reserva 1,676 UC, igual que en una bolsa limpia), U9 OK (sin excepción; gastado = cargado = 4,682). Siguen U2 (el script hace a mano `cerrar` → `cargar`, el orden de antes; por el camino real, `r02_01` R1 da OK) y U3 (lectura de búsquedas sin reservar con el valor por defecto 0: la salvedad declarada; con la clave a 6 000, `r02_01` R2 da OK) |
| `…/r01_02_ciclo_sdk_hostil.py bloque_a/11_Ejecutor <tmp>` (solo DIV) | DIV 25,355; suma = gastado 57,316 | igual; sin violaciones |
| `… --tipos <12> --hilos 6 --lectura 0 / 3000 / 6000` | AG-10: 18 / 14 / 12 | **AG-10: 18 / 18 / 15 (+1 AG-11)**; sin violaciones de cotas; los excesos llevan `busquedas_web: 5`. Con 6 000 baja algo porque esa lectura se gasta de verdad (no por un factor inflado) |
| `… --tipos <12> --hilos 6 --lectura 6000 --factor 1.6` | 6 bolsas pasan (hasta +1,47 UC) | 5 bolsas pasan (DIV, IDX, MP, RV, TCV; hasta +1,47 UC): tokenizador peor que 1,35, la salvedad de CA-1. Comprobado sobre su F5: en cada bolsa, lo que pasa del límite ≤ la suma de `real_uc − reservado_uc` de sus `excesos_reserva` |
| `… --tipos RV,RF,DIV,MP --hilos 4 --cache --orden directo --veces 2` y `--orden inverso` | **DISTINTO** | **IGUAL** en los dos órdenes y entre ellos (misma firma de F5, `20ad04339dc9`) |
| `r01_03_c5_con_escala.py bloque_a/11_Ejecutor <tmp>` | COMÚN 9,782 / límite 5,882 (VIOLA) | **OK**: COMÚN 4,551 / 5,882; se cierran declarados la reparación de AG-20, AG-18 (G3 queda en la regla restrictiva), la integración y la redacción |
| `r01_04_t88_h13_absoluto.py <19f3f3b> <r02>` (y `--compartido`) | IGUAL (y DISTINTO a propósito) | igual que en la r01 |

### Ataques nuevos (scripts de esta ronda)

- `python -I .docs/tickets/T-146/revisores/r02_01_arreglos_r02.py bloque_a/11_Ejecutor <tmp>` → **26/28 OK** (contra el código de la r01, `b0046a1`: VIOLA en R1, R2, R3 y R4, y R4/R6 ni existen). Casos:
  - **R1 (H-08 por `_invocar`):** dos llamadas de una bolsa en hilos; la primera se para justo después de `cerrar`: consumido 4,42 con límite 5, la segunda no sale, nada reservado (r01: 8,84 / 5).
  - **R2 (H-04):** con `tokens_lectura_por_busqueda: 6000` y búsquedas que leen 6 000, sin exceso y dentro del límite; con 1 000 reservados y 6 000 leídos, lo que pasa ≤ lo anotado y el exceso lleva `busquedas_web: 5`; negativo, NaN, texto y nulo fallan cerrado (`ValueError`/`KeyError`); ausente en la configuración recibida, el de `por_defecto.yaml` (0), como todo `parametro`.
  - **R3 (H-01):** con búsquedas no se observa el factor; con la herramienta y 0 búsquedas, o en la siguiente sin búsqueda, sí (1,80).
  - **R4 (H-02):** la misma petición con el prefijo leído o escrito deja lo apartado, lo disponible, el `max_tokens` de la reparación y los recortes iguales.
  - **R5 (H-05):** `KeyboardInterrupt` del SDK en la reparación: sube, lo pagado (3,655) en la bolsa, nada reservado; en la primera petición: nada cargado; un error al registrar el segundo intento: sube y la bolsa carga 7,315 frente a 3,655 de la contabilidad (lo que la API habría cobrado; prudente).
  - **R6 (H-03):** la bolsa de C5 nunca pasa de la base de COMÚN más baja de **todos** los repartos reales posibles (2^12 combinaciones N1/N2) en 9 escenarios: N2 = 100, N1 = 100 > N2, N3 forzado en el periódico, profundización, override de un tipo, override de COMÚN, alcance parcial, alcance con un tipo no activo y V6.
  - **R7:** ciclo sin ningún tipo que analizar (alcance con un tipo no activo): AG-20 gasta 4,551 UC (acotado por su bolsa de C5) y F5 no lo registra en ninguna bolsa → **H-12**.
  - **R8:** tras pasar del límite actual sin llegar al máximo, una fase con ampliación aún saca peticiones; por encima del límite máximo no sale ninguna → **H-13** (texto).
  - **R9:** la última continuación de `pause_turn` sin búsquedas nuevas que reenvía lo leído antes: si la medida no ve ese reenvío, el factor sube a 6,57 → **H-11**.
- Determinismo, más duro que en la r01: `r01_02 … --tipos <12> --hilos 6 --cache --lectura 3000 --factor 1.6 --orden directo|inverso --veces 2` y `r01_02 … --tipos RV,RF,DIV,MP --hilos 4 --cache --v6 --orden directo|inverso --veces 2` → **IGUAL** en las cuatro ejecuciones de cada uno y entre órdenes (12 tipos: 66 peticiones, 19 excesos, 12 recortes, firma `ed54a1f728fd`; V6: `d804ff99ede2`); sin violaciones de cotas en la V6; con factor 1,6 las bolsas que pasan son las de la salvedad.
- `python .docs/tickets/T-146/revisores/r02_02_mutantes_qa.py <copia con «qa21_» y «_mut»>` (pasa `test_t146_presupuesto.py`, `test_t88_consumo.py` y `test_fase4_huecos.py`) → **7/10 muertos**. Vivos: V01 (el exceso comparado con lo real con lectura: con caché compartida, `excesos_reserva` dependería del orden; ninguna prueba de determinismo tiene excesos y caché a la vez), V04 (`except Exception` en vez de `BaseException`: con `KeyboardInterrupt` el ciclo termina igual; equivalente en la práctica) y V05 (R8 con `RecursionError` deja pasar: rama casi inalcanzable, porque `jsonschema` cae antes por la profundidad y entonces `datos` es `None`; y si el esquema falla en la raíz, la llamada sigue sin ser COMPLETA). Ninguno abre un camino de gasto.

### Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 (con la salvedad de la r02) | sí | `r01_02` solo DIV y 12 tipos con lectura 0/3000/6000: sin violaciones; con factor 1,6 (fuera de la salvedad) lo que pasa ≤ lo anotado en `excesos_reserva`; `r02_01` R2 |
| CA-2 | sí | determinismo IGUAL con caché compartida y orden forzado en 4 tipos, 12 tipos (con lectura y factor 1,6) y V6; cotas con 12 tipos y 6 hilos |
| CA-3 | sí (salvo H-12, baja) | `r01_03` OK; `test_ca3_*`; R7: sin tipos que analizar, lo de AG-20 no queda en F5 |
| CA-4 | sí | `test_ca4_*`; búsquedas cobradas en `r01_02` |
| CA-5 | sí | `r01_01` U1, U4, U6–U9; `r02_01` R1–R4, R9 (con la observación H-11) |
| CA-6 | sí | `r01_04` igual; R6; la suma de límites máximos 360 con escala (`r01_03`) |
| CA-7 | sí | `comparar_ciclos.sh` r01 → r02 sin cambios en entregables ni F5 |
| CA-8 | sí | suite completa 6354 passed; goldens |
| CA-9 | sí | 35/35; propios de la r01 12/12 |
| CA-10 | sí | 2838 y 109 |

### Hallazgos de la r01

| ID | Estado en la r02 |
| --- | --- |
| H-01 (alta) | **corregido** (U4, R3, `r01_02 --lectura 3000`: AG-10 vuelve a 18). Queda un resto (H-11, baja) |
| H-02 (alta) | **corregido** (IGUAL en todos los órdenes y ejecuciones, también con 12 tipos, lectura, factor 1,6 y V6; R4) |
| H-03 (media) | **corregido** (`r01_03` OK; R6 en todos los repartos posibles) |
| H-04 (media) | **salvedad bien declarada**: en el CA-1, en INC-T146-01 y en §3 de las decisiones del operador, `[PROPUESTO]`, con la clave `presupuesto_uc.reserva.tokens_lectura_por_busqueda` (0, con su origen y la pregunta al operador) que funciona (R2) y falla cerrado. Imprecisión en el texto: H-13 |
| H-05 (baja) | corregido (U9, R5) |
| H-06 (baja) | corregido (`test_r02_h03_y_h06…`, `r01_03`; V08 muere) |
| H-07 (baja) | corregido (lectura de `test_t145.py` y `_comprobar_cotas`) |
| H-08 (baja) | corregido (R1 por el camino real; U2 sigue en VIOLA solo porque reproduce a mano el orden viejo) |
| H-09 (baja) | sin cambios, como dice el README (para la deuda; no comprobable sin la API) |
| H-10 (baja) | corregido (Q01, Q09 y Q12 mueren) |

### Hallazgos nuevos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-11 | baja (observación, sin la API) | `python -I .docs/tickets/T-146/revisores/r02_01_arreglos_r02.py bloque_a/11_Ejecutor <tmp>` (R9) | El arreglo de H-01 deja de observar el factor en las peticiones con búsquedas, pero no en la continuación de `pause_turn` que no busca y reenvía los resultados de las anteriores. Si la medida de 3,6 caracteres por token se queda corta con esos bloques (en la API llevan `encrypted_content`; no se sabe cuánto miden sin ella), el factor de la bolsa sube como en la r01 (6,57 en el peor caso) y cierra fases antes de tiempo. Falla cerrado (no se gasta de más) | No observar el factor en las peticiones de una generación que ya buscó (o restar lo leído); medir en el modo sombra `factor_observado` y los excesos de las continuaciones | abierto (ticket nuevo) |
| H-12 | baja | R7 de `r02_01` | Con un alcance sin ningún tipo que analizar (todos no activos o pausados), `ciclo` corre AG-20 contra su bolsa de C5 y sale por `_run_sin_analisis`, que no escribe `presupuesto` en el RUN de F5: lo gastado (4,551 UC en el ataque) está en la contabilidad y acotado por esa bolsa, pero no en ninguna bolsa del RUN (CA-3 «todo lo gastado está en las bolsas», en un caso de borde). Anterior a la r02 (también en la r01) | Escribir el resumen de `pres_c5` en el RUN sin análisis | abierto (ticket nuevo) |
| H-13 | baja (texto) | R8 de `r02_01` | La salvedad del CA-1 dice «después no sale ninguna más de esa bolsa». Solo es así respecto del límite máximo (base × 1,5): si el exceso deja la bolsa por encima del límite actual sin llegar al máximo, una fase que admite ampliación (prospectiva, refutación, respuesta, controles) aún puede sacar peticiones (R8: 22,54 sobre 22,50 y la siguiente sale con 1,55 UC ampliadas). La cota no cambia (por encima del máximo cruza como mucho una petición), pero el texto engaña. En INC-T146-01, «Límites declarados» sigue diciendo que tras una búsqueda que lee mucho la bolsa usa el factor observado (desde la r02, no) | Decir «después no sale ninguna más por encima del límite máximo» y poner al día esa línea de INC-T146-01 | abierto (ticket nuevo) |

Invariantes del sistema comprobados: ningún camino nuevo llega a una orden sin F y G (la r02 solo toca presupuesto, JSON y registro); no hay LLM en la ruta determinista; los controles no se relajan (si AG-18 no cabe, G3 queda en la regla restrictiva; R8 por lo anidado falla cerrado); todo falla cerrado (lo que no cabe no sale; la clave nueva negativa, NaN, texto o nula es error); el único número nuevo (`tokens_lectura_por_busqueda: 0`) está en la configuración con su origen, `[PROPUESTO]` y la pregunta al operador; sin secretos (gate en verde). La r02 toca la línea de T-146 y T-148 en la deuda técnica solo para el estado (no la cierra).

No comprobado: el gasto real con la API (sin red ni coste) y por tanto lo que miden de verdad los bloques de resultado de búsqueda (H-11) y los reintentos de *timeout* del SDK (H-09); `./tools/check_all.sh` entero; las suites de A-Forex y B (la r02 no las toca).

Scripts de esta ronda en `revisores/`: `r02_01_arreglos_r02.py` y `r02_02_mutantes_qa.py`.

### Veredicto r02

**APTO** · H-01 y H-02 (altos) están corregidos de verdad: el factor ya no se infla con lo que leen las búsquedas (AG-10 vuelve a 18 llamadas con lectura) y F5 es igual en cualquier orden de los hilos con la caché compartida, también con 12 tipos, lectura, tokenizador peor y V6. H-03 se corrige en todos los repartos posibles y la salvedad de H-04 está declarada `[PROPUESTO]` con su clave, que funciona y falla cerrado. Todos los criterios se cumplen; suite completa en verde (6354), 35/35 mutantes del implementador y 12/12 de la r01 muertos, cuotas y gates en su sitio. Quedan tres bajos (H-11 a H-13) y los mutantes vivos V01, V04 y V05 para un ticket nuevo; H-09 sigue para la deuda. No se cierra el ticket aquí (lo hace quien coordina).
