# T-201 · Pruebas

| Suite | Antes | Después |
| --- | --- | --- |
| Bloque A (`tests/test_t201_cuotas.py`) | — | 38 superadas (35 en la r01) |
| Bloque A completa (gate) | 607 de línea base | r01: 8472 superadas; r02: 8475 superadas |
| B | sin tocar | sin tocar |

## Criterio de aceptación → prueba

| Criterio | Prueba | Resultado |
| --- | --- | --- |
| CA-1 | `.venv/bin/mypy --ignore-missing-imports --no-error-summary bloque_a/11_Ejecutor/bloque_a \| wc -l` (la orden del gate) | 102 → 67; ninguna línea nueva (salidas de antes y después comparadas sin números de línea). `tools/cuotas.txt`: `mypy_bloque_a=67`. De las 67, `… \| grep referencia/ \| grep -c "error:"` da 50 (HT-09 24, HT-02 13, HT-03 13) y `grep -c "note:"` da 11: 61 líneas de `referencia/`; las otras 6 son de `orquestacion.py`. Con la otra medida, `mypy bloque_a` desde `bloque_a/11_Ejecutor`, `referencia/` da 53 errores (HT-09 26, HT-02 14, HT-03 13): los 3 `import-not-found` que el gate no cuenta (r02, H-04) |
| CA-2 | `git diff --name-only origin/develop` frente a `git diff --name-only origin/develop...origin/astra/encargos-bloque-a-c38-c47` y `...wip/t196`; diff sin `type: ignore`, `noqa` nuevo, `cast(` ni `Any` nuevo; `tests/test_unitarias.py::test_herramientas_de_referencia_sin_divergencia` y el gate corpus-integridad | ninguna intersección; nada de eso en el diff (el `Any` de `ht09.py` ya estaba importado); `referencia/` y corpus sin tocar |
| CA-3 | `test_el_envoltorio_importa_en_ejecucion_el_mismo_modulo_que_antes` (4), `test_la_rama_de_mypy_apunta_al_mismo_fichero` (4), `test_el_envoltorio_reexporta_cada_nombre_publico_de_la_referencia` (4), `test_ht09_y_ht03_comparten_la_clase_de_error_de_la_referencia` | superadas |
| CA-4 | `test_ruta_sin_la_clave_…`, `test_ruta_con_la_clave_a_null_da_el_mensaje_nuevo`, `test_ruta_con_la_clave_vacia_devuelve_la_raiz_del_paquete_como_antes`, `test_ruta_con_la_clave_a_cero_da_el_error_de_path_como_antes` (r02, H-03), `test_ruta_con_la_clave_no_cambia`, `test_un_ct24_sin_seg_id_sigue_siendo_un_encargo_desconocido`, `test_b_agente_conserva_el_analista_por_defecto` (6 casos: None, «», clase desconocida), `test_estado_hito_da_lo_mismo_que_la_comprension_de_antes` (8 casos, frente a la expresión de antes copiada en la prueba), `test_estado_hito_lee_el_resultado_aunque_el_hito_siga_abierto` (fallo cerrado igual que antes), `test_la_revision_c6_lleva_el_estado_de_cada_hito`, `test_acierto_direccional_con_lista_y_con_array` (con el caso de flotantes `[1.7, 1.7, 0.2]` desde la r02, H-02), `test_diferencial_rentabilidades_con_historia_usa_el_diferencial_escalado`, `test_motor_sin_ficha_y_cache_hit_como_antes` | superadas |
| CA-5 | `.docs/tickets/T-201/equivalencia.sh .` (lanza también `sensibilidad.py`) | EQUIVALENTE y «puntos ciegos: ninguno» (ver abajo) |
| CA-6 | `./tools/check_all.sh` | ver «Gate» |

## Sin el cambio

Con `tests/test_t201_cuotas.py` sobre el paquete de `origin/develop` (copia con `git archive`), fallan 14 de 38 y pasan 24 (r02):
- **Fallan** las que exigen la estructura nueva: la rama de mypy en los 4 envoltorios, las dos del mensaje de `ruta` (clave ausente y a null) y los 8 casos de `_estado_hito`, que en `develop` no existe.
- **Pasan** las de equivalencia, que fijan lo que ya hacía `develop` (identidad del módulo, reexportación, `b_agente`, `_cambio`, la revisión C6 con hitos, `ruta` con `""` y con `0`, `acierto_direccional` con flotantes, el Motor y el CACHE_HIT): es lo esperado en un ticket que no cambia comportamiento.

## Prueba de equivalencia (en lugar de mutantes)

`equivalencia.sh` extrae el paquete del Bloque A de `origin/develop` con `git archive` en una carpeta temporal fuera del repositorio. Con ese paquete y con el de la copia ejecuta la misma secuencia con el cliente mock, y `comparar.py` compara todos los ficheros que salen (89 por lado). La secuencia:
1. el backtest del README (2024-01-05 → 2024-03-29);
2. un ciclo C1 (`--as-of 2026-06-05`);
3. una petición (`ejemplos/peticiones/peticion_ad_hoc.json`);
4. una consulta;
5. el alta de un seguimiento de una opción no VIGENTE;
6. su ciclo C6 (`seguimiento ejecutar`, 2026-06-12);
7. `evaluar`;
8. `estado`.

Antes de comparar, `comparar.py` normaliza solo esto (desde la r02, H-01 de la QA r01):
- las rutas de cada lado;
- las dos latencias, por su nombre exacto: `latencia_s` y `tiempo_respuesta_s` (su valor, no la clave), y la columna `latencia_s` de `consumo.csv`;
- los resúmenes encadenados (`_hash`, `_hash_prev` y los de `sellos_integridad.json`), que resumen entradas con rutas y con esas latencias.

Ningún instante ni ningún otro campo se enmascara. La r01 enmascaraba además cualquier fecha con hora y campos por prefijo (`duracion…`, `tiempo_…`, `t_…`, `W_…`, `ts`, `_ts`, `timestamp`, `creado`…), entre ellos datos de dominio (la dimensión T `duracion` de F3, `duracion_sesiones` del Motor, `fecha_congelacion` de F4): seis cambios de dominio daban EQUIVALENTE. Ninguno de esos valores difiere entre las dos ejecuciones, así que no hacía falta. Lo que lleva la fecha del reloj (`_ts` y `_fecha` de F10) coincide porque las dos ejecuciones corren a la vez; si una cruzara la medianoche, la comparación daría DISTINTO (falso positivo, nunca un punto ciego), y se repite. El número de entradas de cada sello sí se compara. `acuses.sqlite3` se compara por su volcado SQL.

- **Resultado (r02):** 62 ficheros idénticos sin normalizar y 0 distintos tras normalizar. Ninguno está solo en un lado. VEREDICTO: EQUIVALENTE.
- **Sensibilidad (r02):** `equivalencia.sh` lanza después `sensibilidad.py`. Cambia en el lado nuevo, de uno en uno, 9 valores que no son una ruta ni una latencia: los seis casos de dominio e instantes del revisor, la liquidez y el estado de una opción de F3 y la columna `reintentos` de `consumo.csv`. Cada uno tiene que dar DISTINTO. Cambia también las tres latencias, que tienen que dar EQUIVALENTE. Un patrón que no aparece cuenta como fallo. Resultado: «puntos ciegos: ninguno». El script del revisor, `revisores/r02_sensibilidad_equivalencia.py`, contra el `comparar.py` corregido: 7 de 7 DISTINTO, «puntos ciegos: ninguno».

**Cambios no mecánicos y su prueba:**

| Cambio | Prueba |
| --- | --- |
| Envoltorios con `TYPE_CHECKING` | las 13 de CA-3 y la equivalencia |
| `_cambio` con `seg_id` None | `test_un_ct24_sin_seg_id_sigue_siendo_un_encargo_desconocido` |
| `b_agente(None)` | `test_b_agente_conserva_el_analista_por_defecto` |
| `_estado_hito` | `test_estado_hito_…` (9 casos) y `test_la_revision_c6_lleva_el_estado_de_cada_hito` |
| `ALTERNATIVAS.get` con ficha None; `hit` en el CACHE_HIT | `test_motor_sin_ficha_y_cache_hit_como_antes` |
| `diferencial_rentabilidades` | `test_diferencial_rentabilidades_con_historia_usa_el_diferencial_escalado` |
| `acierto_direccional` | `test_acierto_direccional_con_lista_y_con_array`, con flotantes (mata M16) |
| `ruta` sin la clave o a null (cambia el mensaje) | `test_ruta_sin_la_clave_…`, `test_ruta_con_la_clave_a_null_…`, `test_ruta_con_la_clave_vacia_…` y `test_ruta_con_la_clave_a_cero_…` (matan M01) |

## Mutantes del revisor (r02)

`revisores/r04_mutantes.py <copia>/bloque_a <tmp>` (18 mutantes y el testigo M00), sobre la r02. El testigo pasa (145 pruebas). Mueren 16. Quedan vivos M10 y M11, que el revisor marca como equivalentes: F11 nunca tiene una clave falsa, y una ficha None se rechaza antes por la forma. **M01** (`if not valor:`) muere con `test_ruta_con_la_clave_vacia_devuelve_la_raiz_del_paquete_como_antes`. **M16** (`int(sum(o))`) muere con `test_acierto_direccional_con_lista_y_con_array`. «vivos no equivalentes: ninguno».

## Plan de pruebas y evidencias

T-201 no tiene caso del plan. `tests/mapa_plan_pruebas.json` lo cambia T-196 y aquí no se toca, así que el documento de evidencias no se regenera.

## Gate

`./tools/check_all.sh` completo en la copia (24-11-2026, lanzado con `setsid nohup`): **12 de 12 en verde**.
- corpus-integridad: 705 archivos coinciden con el manifiesto.
- nombres-nfc, yaml-configs, secrets y refs-vivas: OK.
- ruff: cuota 2797, actual 2797; antes 2806.
- mypy A: cuota 67, actual 67; antes 102. mypy A-Forex: 174 y mypy B: 159, sin tocar.
- pytest: A 8472 superadas (base 607), A-Forex 68 (base 68) y B 176 (base 174).

`handoff.md` se escribió con el gate en marcha. Después se volvieron a pasar refs-vivas, secrets y nombres-nfc, también en verde.

### Gate de la r02

`./tools/check_all.sh` completo de nuevo, con `setsid nohup` y log `scratchpad/gate_t201_r02b.log` (el primer intento de la r02 se cortó al reiniciarse el contenedor). Resultado, 25-11-2026: **12 de 12 en verde**.
- Cuotas: ruff 2797 de 2797, mypy A 67 de 67, A-Forex 174 de 174 y B 159 de 159.
- pytest: A 8475 superadas (las 3 pruebas nuevas de la r02), A-Forex 68 y B 176.
