# T-151 · Bloque A: hallazgos bajos de las QA r02 de T-146 y T-148 (factor en continuaciones, AG-20 sin tipos, textos, mutantes, reintentos del SDK)

| Campo | Valor |
| --- | --- |
| Estado | CERRADO (QA r01 APTO) |
| Pieza | Bloque A (`bloque_a/11_Ejecutor`: `bloque_a/consumo.py`, `llm.py`, `orquestacion.py`, `config/por_defecto.yaml`, `README.md`; `tests/test_t146_presupuesto.py`, `tests/test_t148.py`); `docs/incidencias.md` (INC-T146-01); el README de T-146 (texto del CA-1) |
| Planifica · implementa · QA | claude · claude · el otro agente o un revisor nuevo |
| Aprobación del operador | no necesaria (correcciones y pruebas de dos tickets cerrados; lo nuevo, `[PROPUESTO]` en INC-T146-01) |
| Deuda técnica | T-151 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` (este ticket no toca la fila) |

## Objetivo

Cerrar los hallazgos bajos que dejaron APTO las QA r02 de T-146 (H-11, H-12, H-13 y los mutantes V01, V04 y V05) y de T-148 (H-04: mutantes W04 y W05), y el H-09 de la r01 de T-146 (reintentos del SDK fuera de la reserva y la escritura de caché a 1 h), antes del modo sombra.

## Alcance

- Entra:
  - **H-11 (T-146 r02).** `ReservaLlamada.pagar` no observa el factor del tokenizador en una petición de una generación que ya buscó (las continuaciones de `pause_turn` reenvían lo leído, que la medida no ve entero).
  - **H-12 (T-146 r02).** El RUN sin ningún tipo que analizar (`_run_sin_analisis`) escribe en F5 el presupuesto de la bolsa con la que corrió AG-20 (COMÚN de C5), con sus cierres, recortes, excesos y peticiones sin respuesta, como el RUN normal.
  - **H-13 (T-146 r02).** Texto del CA-1 del README de T-146 («no sale ninguna más» solo respecto del límite máximo) y la línea «Límites declarados» de INC-T146-01 (el factor observado ya no se aprende de lo que leen las búsquedas).
  - **Mutantes V01, V04 y V05 (T-146 r02).** Pruebas que los maten.
  - **H-09 (T-146 r01).** El SDK reintentaba solo (`max_retries` = `llm.max_reintentos_api`, 4) sin pasar por la reserva: un *timeout* que el servidor completó podía cobrarse sin reserva. Ahora el SDK sale sin reintentos y reintenta el ejecutor, cada intento con su reserva; lo que pudo cobrarse sin respuesta se carga en la bolsa por su peor caso reservado. La escritura de caché a 1 h, declarada.
  - **H-04 (T-148 r02).** Pruebas de la salida de `.docs/scripts/estimar_coste_ciclo_a.py` con `presupuesto_uc.reserva.tokens_lectura_por_busqueda` > 0 y del peso con `--sin-t146` (mutantes W04 y W05).
- No entra: la fila de la deuda técnica; `bloque_a/cadena_b.py`, `motor/frontera_b.py`, `.docs/scripts/cadena_a_b.py`, `.docs/scripts/descargar_datos_bce.py`, `tests/test_t14[479].py` (otra tarea); otros bloques, `sistema_global/marco_comun_c/`, la Constitución y el corpus; medir con la API (sin red ni coste); cambiar la UC de la escritura de caché (decisión del operador, solo se declara).

## Diseño

| Hallazgo | Cambio |
| --- | --- |
| H-11 | En `pagar`, `ya_busco = self._pagado.busquedas_web > 0` antes de sumar la petición: si una petición anterior de la misma generación (las continuaciones de `pause_turn`) buscó, no se observa el factor. La reparación empieza una generación nueva (`pagar_resto` pone `_pagado` a cero) y no reenvía los bloques de búsqueda (solo el texto), así que sí observa |
| H-12 | `_run_sin_analisis` recibe `pres_c5` y escribe en el RUN de F5 `presupuesto` (su resumen: COMÚN), `cierres_parciales` y, si los hay, `recortes_salida`, `excesos_reserva` y `peticiones_sin_respuesta`; también `resultado["presupuesto"]` |
| H-13 | Solo texto (README de T-146, INC-T146-01) |
| V01 | Prueba: la misma petición con el prefijo leído o escrito deja el mismo `excesos_reserva` (el exceso se compara con lo real contado como escrito) |
| V04 | Prueba: un `KeyboardInterrupt` del SDK tras una petición pagada deja lo pagado en la bolsa y nada reservado, y sube |
| V05 | Prueba: si la comprobación de R8 no se puede hacer por lo anidado (`RecursionError`), la respuesta se bloquea (no queda COMPLETA) |
| H-09 | `AnthropicClient`: el SDK se crea con `max_retries=0` (y uno recibido con `with_options` se pasa a 0); el cliente reintenta hasta `llm.max_reintentos_api` veces los errores reintentables (conexión y *timeout*, y los estados de `llm.reintentos.estados_reintentables`), con espera determinista (`llm.reintentos.espera_inicial_s` doblando hasta `espera_max_s`, o el `retry-after` del servidor). Cada reintento reserva su petición antes de salir; si no cabe, `presupuesto_agotado`. La petición que falló suelta su reserva si el servidor la rechazó sin ejecutarla (`llm.reintentos.estados_sin_cobro`: 429 y 529); si no (conexión, *timeout*, otro 5xx), se carga en la bolsa por su peor caso reservado (`ReservaLlamada.fallida`) y queda en `peticiones_sin_respuesta` del RUN en F5 |
| H-04 (T-148) | Pruebas en `tests/test_t148.py` |

- Contratos y esquemas: no cambian (goldens).
- Estado persistido: sin versión nueva; el RUN de F5 sin análisis añade `presupuesto` y `cierres_parciales` (y las listas de T-146 si las hay); cualquier RUN puede añadir `peticiones_sin_respuesta` (solo si la hay).
- Números nuevos, en `config/por_defecto.yaml` con su origen, `[PROPUESTO]`: `llm.reintentos.espera_inicial_s` 0,5 y `espera_max_s` 8 (los del SDK 2.8 que dejan de usarse, `INITIAL_RETRY_DELAY` y `MAX_RETRY_DELAY`, sin la variación aleatoria); `estados_reintentables` (408, 409, 429, 500, 502, 503, 504, 529: los que reintenta el SDK, `_should_retry`); `estados_sin_cobro` (429, 529: el servidor rechaza la petición sin ejecutarla).
- Cómo falla cerrado: un reintento que no cabe no sale; lo que pudo cobrarse sin respuesta se carga por su peor caso (cota superior, no un valor inventado); una clave de reintentos ausente es `KeyError` (`parametro`), y una espera negativa o un estado que no es entero, `ValueError`.
- Decisiones `[PROPUESTO]` (INC-T146-01, ronda T-151): la regla de H-11; los reintentos en el ejecutor y su clasificación; la carga por el peor caso de lo que no respondió; lo de la caché a 1 h (declarado, para el operador).

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| Los reintentos del ejecutor se comportan distinto de los del SDK con la API real | Más o menos esperas, otro número de intentos | Mismos estados y mismas esperas base que el SDK, sin la variación aleatoria; se mide en el modo sombra; probado con el SDK real sobre un transporte falso (sin red) |
| Un *timeout* que no se cobró se carga por su peor caso | La bolsa se gasta antes (cierra fases antes) | Prudente y declarado: no se sabe si se cobró; queda en `peticiones_sin_respuesta` para medirlo |
| Cambiar líneas que citan los mutantes de T-146 y T-148 | Sus scripts darían «NO APLICA» | Se conservan las líneas citadas; se pasan los tres scripts de mutantes |

## Criterios de aceptación (binarios)

1. CA-1 (H-11): una continuación sin búsquedas de una generación que buscó no sube el factor (el R9 del revisor da OK); una petición sin búsquedas de otra llamada, o una reparación, sí lo aprende (R3 sigue OK).
2. CA-2 (H-12): en un ciclo sin tipos que analizar, lo que gasta AG-20 está en la bolsa COMÚN del RUN de F5 (el R7 del revisor da OK) y los cierres de C5 quedan en el RUN.
3. CA-3 (H-13): el CA-1 de T-146 y la línea de INC-T146-01 dicen lo que hace el código.
4. CA-4: `r02_02_mutantes_qa.py` de T-146: V01, V04 y V05 muertos (10/10); el de T-148: W04 y W05 muertos (W02, equivalente, declarado por la QA).
5. CA-5 (H-09): con `crear_cliente("anthropic")` el SDK sale con `max_retries=0`; un error reintentable se reintenta hasta `max_reintentos_api` veces con su reserva cada vez y las esperas de la configuración; un 429/529 suelta la reserva; un *timeout* la carga en la bolsa y queda en `peticiones_sin_respuesta`; un reintento que no cabe no sale; un error no reintentable no se reintenta. INC-T146-01 lo declara `[PROPUESTO]`, con la caché a 1 h.
6. CA-6: `mutantes_t146.py` 35/35, `r01_05` 12/12, `T-147/mutantes.py --ticket T-148` 13/13, y los mutantes propios de T-151 (`mutantes_t151.py`) muertos.
7. CA-7: las suites citadas, los scripts r01/r02 de T-146 y T-148, `comparar_ciclos.sh`, los goldens, los gates ligeros y la suite completa de A en verde; cuotas ruff ≤ 2831 y mypy A ≤ 109 (T-154, H-05 de la QA r01: decía ≤ 2838, la cuota de antes; el commit de T-151, `1ccffd5`, la bajó a 2831 en `tools/cuotas.txt`).

## Plan de pruebas

| Prueba | Tipo | Criterio |
| --- | --- | --- |
| `test_t151_h11_la_continuacion_de_una_generacion_que_busco_no_observa` | regresión | CA-1 |
| `test_t151_h11_la_reparacion_tras_buscar_si_observa` | límite | CA-1 |
| `test_t151_h12_sin_tipos_lo_de_ag20_esta_en_f5` | regresión, integración | CA-2 |
| `test_t151_v01_el_exceso_no_depende_de_si_el_prefijo_se_leyo` | regresión (mutante) | CA-4 |
| `test_t151_v04_keyboardinterrupt_deja_lo_pagado` | fallo cerrado (mutante) | CA-4 |
| `test_t151_v05_r8_sin_comprobar_bloquea` | fallo cerrado (mutante) | CA-4 |
| `test_t151_h09_*` (SDK sin reintentos, reintento con reserva, 429 suelta, *timeout* carga, no cabe, no reintentable, espera y `retry-after`, configuración inválida, SDK real con transporte falso) | nominal, límite, fallo cerrado | CA-5 |
| `test_t151_h04_w04_la_salida_dice_lo_reservado_por_busqueda`, `test_t151_h04_w05_el_peso_sin_t146` (en `test_t148.py`) | regresión (mutante) | CA-4 |
| Scripts del revisor, mutantes, `comparar_ciclos.sh`, goldens, gates, suite completa | regresión | CA-6, CA-7 |

## Scripts

Usa `.docs/tickets/T-146/mutantes_t146.py`, `revisores/r0*_*.py` de T-146 y T-148, `.docs/tickets/T-147/mutantes.py`, `.docs/tickets/T-146/comparar_ciclos.sh`, `.docs/scripts/medir_consumo_a.py` y `estimar_coste_ciclo_a.py`. Crea `.docs/tickets/T-151/mutantes_t151.py` (mutantes de lo que cambia T-151).

## Registro

- 2026-11-15 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-15 · PLANIFICADO · claude · plan y criterios
- 2026-11-15 · EN QA · claude · implementado y probado (ver `analisis-tecnico.md` y `pruebas.md`)
