# T-151 · QA independiente

- **Revisor:** Claude, subagente revisor nuevo sin el contexto de la implementación (no implementó T-151) · **Ronda:** r01 · 15-11-2026
- **Copia:** git worktree de la instantánea `1cd844e` con `.venv` enlazado. Sin red, sin la API, sin coste y sin clave real (el SDK `anthropic` 2.8 real sobre `httpx2.MockTransport`, o SDK dobles en Python). La instantánea lleva también el código de T-150 (`cadena_b.py`, `frontera_b.py`, `test_t14[49].py`, `test_t150.py`): para comparar «antes y después» solo de T-151 se usó una copia de la instantánea con `consumo.py`, `llm.py`, `orquestacion.py` y `config/por_defecto.yaml` de `6e076aa` («antes»).

## Reproducción desde limpio

Desde la raíz de la copia (`<tmp>` es una carpeta temporal fuera del repo; `<antes>` la copia «antes» descrita arriba):

| Orden | Resultado |
| --- | --- |
| `cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q -p no:cacheprovider` (una vez) | **6557 passed, 2 skipped**, exit 0, 28 min 28 s (6476 del implementador + las pruebas de T-150 que trae la instantánea) |
| `… -m pytest -q -p no:cacheprovider tests/test_fase3_goldens.py tests/test_t151_reintentos.py tests/test_t146_presupuesto.py tests/test_t148.py` | 192 passed |
| `cd bloque_a/11_Ejecutor && ../../.venv/bin/python tests/goldens_ct.py` | «goldens de contratos: coinciden» |
| `.venv/bin/python tools/refs_vivas.py`, `secrets_scan.py`, `nfc_check.py`, `corpus_integridad.py` | exit 0 los cuatro; corpus **695** archivos coinciden |
| `.venv/bin/ruff check --output-format=concise bloque_a/11_Ejecutor bloque_a_forex/11_Ejecutor bloque_b/11_Ejecutor \| wc -l` | **2831** (cuota `tools/cuotas.txt`: 2831) |
| `.venv/bin/mypy --ignore-missing-imports --no-error-summary bloque_a/11_Ejecutor/bloque_a \| wc -l` | **109** (cuota 109) |
| `.venv/bin/python -I .docs/tickets/T-146/revisores/r02_01_arreglos_r02.py bloque_a/11_Ejecutor <tmp>` | **28/28 OK** (R7: gastado 4,551 = en las bolsas de F5 4,551; R9: factor 0,00) |
| `… T-146/revisores/r01_01_reserva_unidad.py bloque_a/11_Ejecutor` | 10/12, como en la r02 (U2 hace a mano el orden viejo; U3 es la salvedad de la lectura a 0) |
| `… T-146/revisores/r01_02_ciclo_sdk_hostil.py bloque_a/11_Ejecutor <tmp>` (solo DIV) | DIV 25,355 / 25,355; suma = gastado 57,316; sin violaciones |
| `… r01_02 … --tipos <12> --hilos 6 --lectura 0 / 3000 / 6000` | AG-10: 18 / 18 / 15 (+1 AG-11); sin violaciones |
| `… r01_02 … --tipos <12> --hilos 6 --lectura 6000 --factor 1.6` | pasan DIV, IDX, MP, RV y TCV: la salvedad declarada del CA-1 de T-146, igual que en la r02 |
| `… r01_02 … --tipos RV,RF,DIV,MP --hilos 4 --cache --orden directo\|inverso --veces 2` | **IGUAL** en los dos órdenes y entre ellos, firma `fce20f7854fb` (la del implementador) |
| `… r01_02 … --tipos <12> --hilos 6 --cache --lectura 3000 --factor 1.6 --orden directo\|inverso --veces 2` | **IGUAL** (`815e51157c78`) en las cuatro ejecuciones |
| `… r01_02 … --tipos RV,RF,DIV,MP --hilos 4 --cache --v6 --orden directo\|inverso --veces 2` | **IGUAL** (`e910ef27284c`); sin violaciones |
| `… T-146/revisores/r01_03_c5_con_escala.py bloque_a/11_Ejecutor <tmp>` | OK: COMÚN 4,551 / 5,882 |
| `… T-146/revisores/r01_04_t88_h13_absoluto.py <19f3f3b>/bloque_a/11_Ejecutor bloque_a/11_Ejecutor` (y `--compartido`) | IGUAL (y DISTINTO a propósito), como en la r02; contra `<antes>`, IGUAL en los dos |
| `cd bloque_a/11_Ejecutor && PYTHONPATH=$PWD ../../.venv/bin/python ../../.docs/scripts/medir_consumo_a.py <tmp>/m_div 2024-03-29` y `… <tmp>/m_12 2024-03-29 --config <doce.yaml>` | 8 y 77 llamadas medidas |
| `.venv/bin/python .docs/scripts/estimar_coste_ciclo_a.py <tmp>/m_div` (por defecto, `--con-t146`, `--sin-t146`) y `… <tmp>/m_12 --config <doce.yaml>` (`--sin-t146`) | 28,04 USD (presupuesto 46,08; `--sin-t146` 69,62) y 46,08 (llamadas 268,48; `--sin-t146` 248,02); pesos 0,40 / 0,08 y 0,96 / 4,80: sin cambios |
| `PYTHONPATH=bloque_a/11_Ejecutor .venv/bin/python -I .docs/tickets/T-148/revisores/r01_01_tope_y_cota_con_t146.py <m_div> <m_12> <doce.yaml> <tmp>` | A 6 OK, B 4 OK, D 4 OK; C «HALLAZGO» como en la r02 (la salvedad declarada de la lectura) |
| `.venv/bin/python -I .docs/tickets/T-148/revisores/r02_01_peso_y_textos.py <m_div> <m_12> <doce.yaml> <tmp>` | **0 hallazgos** (15 OK) |
| `bash .docs/tickets/T-146/comparar_ciclos.sh <antes>/bloque_a/11_Ejecutor bloque_a/11_Ejecutor <tmp> .venv/bin/python` | solo difieren `bt/salida/consumo.csv` y `doce/estado/cache_resultados.jsonl` (cambian también entre dos pasadas iguales); F5 sin campos distintos en ningún RUN |
| Mutantes, cada uno en su copia desechable de `git archive HEAD bloque_a .docs tools` (borradas al acabar): `.docs/tickets/T-151/mutantes_t151.py <…/t151_mut>` | **18/18** muertos |
| `.docs/tickets/T-146/mutantes_t146.py <…/t146_mut>` | **35/35** muertos |
| `.docs/tickets/T-146/revisores/r01_05_mutantes_qa.py <…/qa19_mut>` | **12/12** muertos |
| `.docs/tickets/T-146/revisores/r02_02_mutantes_qa.py <…/qa21_t146_mut>` | **10/10** muertos (V01, V04 y V05 incluidos) |
| `.docs/tickets/T-148/revisores/r02_02_mutantes_qa.py <…/qa21_t148_mut>` | **5/5** muertos (W04 y W05; también W02, que la r02 daba por equivalente) |
| `.docs/tickets/T-147/mutantes.py <…/t147_mut> --ticket T-148` | **13/13** (M25–M37, «0 vivos») |

## Scripts del revisor (esta ronda)

| Orden (desde la raíz) | Qué ataca | Resultado |
| --- | --- | --- |
| `.venv/bin/python -I .docs/tickets/T-151/revisores/r01_01_reintentos_unidad.py bloque_a/11_Ejecutor` | H-09 y H-11 en unidad, con el SDK real sobre un transporte falso | **9/9 OK**, 3 OBS (X9, X10, X12) |
| `.venv/bin/python -I .docs/tickets/T-151/revisores/r01_02_ciclo_reintentos.py bloque_a/11_Ejecutor <tmp> [--tipos …] [--hilos N] [--cache] [--orden directo\|inverso] [--veces N] [--sin-tipos] [--fallo-escribe cobrables\|ninguno]` | ciclos completos con un SDK doble que falla (timeout, 503, 529, 500) según el contenido de cada petición | ver abajo |
| `.venv/bin/python .docs/tickets/T-151/revisores/r01_03_mutantes_qa.py <copia con «qa24_» y «_mut»>` | 16 mutantes propios (Q01–Q16) contra `test_t151_reintentos.py` y `test_t146_presupuesto.py` | **14/16** muertos; vivos Q09 y Q10 (H-04) |

`r01_01` (unidad):

- X1: con un SDK recibido con `max_retries=5`, 529 → 529 → 200 son exactamente 3 peticiones HTTP, 3 reservas, esperas [0,5; 1,0], lo consumido = lo real y nada reservado: el SDK no reintenta por su cuenta.
- X2: `AnthropicClient(api_key=…)` y `crear_cliente("anthropic")` crean el SDK con `max_retries=0`, el `timeout_s` de la configuración y la regla.
- X3/X8: timeout → 503 → 529 → 200: cuatro reservas; el timeout y el 503 quedan cargados por su peor caso (en `sin_respuesta`), el 529 suelto y el 200 por lo real; consumido 0,9664 = 0,1292 + 0,4186 + 0,4186, exacto: ni reserva colgada ni cobro doble.
- X4: 500 hasta agotar: 5 peticiones, 5 cargadas, `error_proveedor`, consumido = Σ reservas.
- X5: tras un timeout, el reintento que no cabe no sale (1 petición), `presupuesto_agotado`, motivo «… (reparación, continuación o reintento) …», lo del timeout cargado.
- X6: un 400 y un `TypeError` del SDK: una petición, sin reintento, reserva suelta.
- X7: `KeyboardInterrupt` en la espera tras un timeout, por la rama de `Bloque._invocar`: sube, lo del timeout queda cargado y nada reservado.
- X11 (H-11): búsqueda con `pause_turn` → timeout → continuación sin búsqueda: no observa (factor 0); la reparación siguiente sí (19,03 con la entrada inflada a propósito).
- X9, X10 y X12 (OBS): ver H-01 y las observaciones.

`r01_02` (ciclos; cada uno con su estado limpio):

| Orden (opciones) | Resultado |
| --- | --- |
| `--veces 2` (DIV) | 14 peticiones = 14 reservas; 6 fallos; 4 en F5 y 1 de AG-19 cargado pero no declarado (H-02); consumido 42,3304 = contabilidad 17,6533 + sin respuesta 24,6772; nada reservado; **IGUAL** |
| `--tipos RV,RF,DIV,MP --hilos 4` | 37 = 37; 14 fallos; consumido 99,8063 = 51,5926 + 48,2138; cierres con «reintento»; sin violaciones |
| `--tipos RV,RF,DIV,MP --hilos 4 --cache --orden directo\|inverso --veces 3` | sin violaciones de cotas ni reservas colgadas, pero **DISTINTO** (2 firmas, en los dos órdenes): solo cambia lo consumido de DIV, MP y RV en 0,5157 UC cada una (H-03) |
| `… lo mismo con --fallo-escribe ninguno` | **IGUAL** (`a9bad5135cf9`) en las seis ejecuciones |
| `--tipos <12> --hilos 6 --cache --orden directo\|inverso --veces 2` | sin violaciones; IGUAL en un orden y DISTINTO en el otro (H-03) |
| `--sin-tipos` (DIV activo, alcance RF; AG-20 con un timeout) | F5 lleva `presupuesto` (COMÚN 6,7019 = contabilidad 2,1509 + 4,5510 sin respuesta), `peticiones_sin_respuesta` con AG-20 y `resultado["presupuesto"]` igual (H-12 OK) |

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 (H-11) | sí | R9 y R3 de `T-146/revisores/r02_01` OK; `r01_01` X11 (también con un timeout en medio); mutantes N01, N02 y Q04 muertos |
| CA-2 (H-12) | sí | R7 de `r02_01` OK; `r01_02 --sin-tipos` (también con lo sin respuesta de AG-20); N03 y Q07 muertos |
| CA-3 (H-13) | sí | Lectura: CA-1 de `.docs/tickets/T-146/README.md` («Si con eso pasa también del límite máximo…») y «Límites declarados» de INC-T146-01 (el factor ya no se aprende de lo que leen las búsquedas ni en las continuaciones de una generación que buscó) dicen lo que hace el código; R8 de `r02_01` OK |
| CA-4 | sí | `r02_02` de T-146: 10/10; de T-148: 5/5 (W04 y W05 muertos; W02 también) |
| CA-5 (H-09) | sí | `r01_01` X1–X8; `r01_02` (cada petición del SDK con su reserva en todos los ciclos); `test_t151_reintentos.py` 23 passed; N04–N18 y Q01–Q03, Q05–Q08, Q11–Q16 muertos. INC-T146-01 lo declara `[PROPUESTO]`, con la caché a 1 h y su pregunta al operador. Con el matiz de H-01 (los 5xx fuera de la lista) |
| CA-6 | sí | `mutantes_t146.py` 35/35 · `r01_05` 12/12 · `T-147/mutantes.py --ticket T-148` 13/13 · `mutantes_t151.py` 18/18 |
| CA-7 | sí | Tabla de reproducción: scripts r01/r02, `comparar_ciclos.sh`, goldens, gates ligeros y suite completa en verde; ruff 2831 ≤ 2831 (la cuota ya bajó en `tools/cuotas.txt`; el CA-7 decía ≤ 2838) y mypy A 109 ≤ 109 |

Punto 6 del encargo (el motivo de los cierres «reparación, continuación o reintento»): ningún golden, esquema, ejemplo ni prueba cita el texto viejo (`grep` en el repo); los goldens coinciden y `comparar_ciclos.sh` no ve ningún campo de F5 distinto en los ciclos simulados (allí no se cierra ninguna fase por una petición negada); la firma de F5 del `r01_02` con caché cambia solo por ese texto (`fce20f7854fb`, la que da el implementador).

## Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | baja | `r01_01` X9 | Esperado (README del ejecutor: «la petición que pudo cobrarse sin respuesta (conexión, *timeout*, 5xx salvo 529) se carga»; INC-T146-01: «u otro 5xx»): todo 5xx que no sea 529 se carga por su peor caso. Obtenido: un 5xx fuera de `estados_reintentables` (501, 505, 520…) o un 500 con `x-should-retry: false` no se reintenta y se suelta como no cobrado (`clasificar_error` da cobro solo si se reintenta). El SDK 2.8 reintentaba todo ≥ 500. Falla abierto en la cuenta (una petición que el servidor pudo ejecutar no se carga), pero acotado a una petición por llamada y en estados que la API apenas da | En `clasificar_error`, cobro posible para todo estado ≥ 500 que no esté en `estados_sin_cobro`, se reintente o no (o reintentar también los ≥ 500 como el SDK); o, si se quiere así, decirlo en el README y en INC-T146-01. Prueba con 501 y con 500 + `x-should-retry: false` | abierto (ticket nuevo) |
| H-02 | baja | `r01_02 … --veces 2` (DIV): línea «OBS: 1 fallo(s) de AG-19» | Esperado (README e INC-T146-01: la petición sin respuesta «queda en `peticiones_sin_respuesta` del RUN en F5»). Obtenido: la auditoría (AG-19) corre después de `_registrar_run`; su timeout se carga en COMÚN (está en `resultado["presupuesto"]`: consumido 42,33 = contabilidad 17,65 + 24,68 sin respuesta), pero F5 solo declara 20,47. Lo mismo pasaba ya con los cierres, recortes y excesos de AG-19 (T-146) | Declarar lo de la auditoría después de ella (una entrada de F5 que complete el RUN, o en el AUD de HA), o decir en INC-T146-01 que lo de AG-19 queda solo en el resultado | abierto (ticket nuevo) |
| H-03 | baja | `r01_02 … --tipos RV,RF,DIV,MP --hilos 4 --cache --orden directo --veces 3` (DISTINTO) frente a `… --fallo-escribe ninguno` (IGUAL) | Esperado (T-88 y T-146 r02): F5 no depende del orden de los hilos. Obtenido: si la petición que falla sin respuesta (timeout o 5xx que el servidor completó) es la primera que escribe un prefijo compartido, ninguna respuesta trae esa escritura y `liquidar_primas` no reparte su prima: lo consumido de DIV, MP y RV cambia 0,5157 UC según qué hilo llegó antes. Siempre prudente (el peor caso cargado de la fallida ya cuenta toda su entrada como escritura) y sin pasar de ningún límite; solo con fallos. Antes de T-151 pasaba igual dentro de los reintentos del SDK | En `ReservaLlamada.fallida` con cobro posible, apuntar el prefijo de esa petición en el grupo de primas como escrito, o declarar en INC-T88-01 / INC-T146-01 que el determinismo de F5 con caché vale sin peticiones sin respuesta. Prueba con el SDK de `r01_02` | abierto (ticket nuevo) |
| H-04 | baja | `r01_03_mutantes_qa.py <copia «qa24_…_mut»>` | Mutantes vivos: Q09 (un `retry-after` infinito o NaN se acepta como espera; `time.sleep(inf)` lanzaría `OverflowError` dentro de `_crear`, fuera de su `try`) y Q10 (`x-should-retry` sensible a mayúsculas). Ninguna prueba los mira | Dos casos más en `test_la_espera_dobla_hasta_la_maxima_o_es_la_del_servidor` («inf», «nan») y en la clasificación («True») | abierto (ticket nuevo) |
| H-05 | baja (texto) | Lectura | (a) El CA-7 del README de T-151 dice ruff ≤ 2838 y `analisis-tecnico.md` y `pruebas.md` dicen que `tools/cuotas.txt` no se toca; en la instantánea ya está en 2831 (se cumple). (b) INC-T129-01 (límites del estimador y cota del ciclo) y el S5 que imprime `estimar_coste_ciclo_a.py` siguen diciendo «los reintentos del SDK»: ahora los hace el cliente y, con T-146, cada uno reserva (la cota por presupuesto los cubre; la cota por llamadas no los cuenta). (c) Fuera del alcance: A-Forex y B siguen creando el SDK con `max_retries` = `max_reintentos` (el riesgo de H-09 sigue allí para su modo sombra) | Poner al día esas líneas; para (c), un ticket por bloque antes de su modo sombra | abierto (ticket nuevo) |

Observaciones (sin hallazgo):

- `retry-after` sin tope (`r01_01` X10: 100 000 s de espera). Es lo que hace el SDK 2.8 (tope 4 294 967 s), así que no cambia nada respecto de antes; con `timeout_s` 600, quizá convenga un tope en la configuración (decisión del operador).
- La regla acepta estados raros (200, negativos, listas vacías) y esperas 0 (`r01_01` X12): inocuo, falla hacia no reintentar.
- `peticiones_sin_respuesta` se ordena por (clase, agente, petición): dos llamadas del mismo agente en la misma bolsa empatan; hoy van siempre en el mismo hilo (la bolsa de cada hilo es su tipo), así que el orden es determinista.

Invariantes del sistema: ningún camino nuevo llega a una orden sin F y G (T-151 solo toca presupuesto, cliente LLM y registro); no hay LLM en la ruta determinista ni en los controles; los controles no se relajan (el reintento que no cabe cierra la fase declarada); falla cerrado y valida antes de mutar (la regla inválida es `ValueError`/`KeyError` antes de crear el cliente; lo que pudo cobrarse se carga por su peor caso; salvo H-01); los números nuevos (`llm.reintentos.*`) están en `config/por_defecto.yaml` con su origen y `[PROPUESTO]`, sin ninguno escrito a mano en el código; las decisiones nuevas están en INC-T146-01 como `[PROPUESTO]` con su pregunta al operador (T-57); sin secretos ni datos personales (gate en verde; la clave de los scripts es «clave-falsa-qa»). Este ticket no toca la deuda técnica ni el briefing (no cambia la arquitectura).

No comprobado: el comportamiento real de la API (qué estados cobra, cuánto miden los bloques de búsqueda reenviados) sin red ni gasto; `./tools/check_all.sh` entero (A-Forex y B no se tocan: se pasaron los gates ligeros, las cuotas y la suite de A).

## Veredicto

**APTO** · Los siete criterios se cumplen con evidencia propia, y no hay ningún hallazgo crítico, alto ni medio. Los cinco bajos (H-01 a H-05) no rompen ningún criterio. Se apuntan para un ticket nuevo: H-01, el cobro de los 5xx que quedan fuera de la lista; H-02, lo de AG-19 en F5; H-03, el determinismo con caché cuando falla la petición que escribe el prefijo; H-04, dos pruebas; H-05, textos y los otros dos bloques. El revisor no cierra el ticket ni toca la deuda técnica (lo hace quien coordina).
