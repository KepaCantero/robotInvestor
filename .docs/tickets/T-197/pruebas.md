# T-197 · Pruebas

| Suite | Antes | Después |
| --- | --- | --- |
| Bloque A (`pytest -q bloque_a/11_Ejecutor`, recogidas) | 8361 | 8379 (+18 de `tests/test_t197_periodicidad.py`) |
| Bloque A, ejecución completa (en el gate, r01) | — | 8377 superadas y 2 omitidas de 8379 recogidas, sin fallos. Las 2 omitidas son `test_t149.py::test_h01_series_distintas_en_otras_rejillas_no_son_copias` (`pytest.skip`, límite declarado de T-149), las mismas que omite develop |
| A-Forex, B | sin tocar | sin tocar |

La línea base de A (607) se respeta con holgura. Todas las pruebas con la configuración por defecto (`config_pruebas()`, que solo activa los doce perfiles y baja el bootstrap); la de integración, solo con DIV para que el ciclo real sea corto.

## Criterio de aceptación → prueba (`tests/test_t197_periodicidad.py`)

| Criterio | Pruebas |
| --- | --- |
| CA-1 | `test_ca1_ct04_escribe_el_p01_completo_con_fecha_de_efecto` (RET- APLICADA, un CFG- de AG-01, fecha de efecto, CT-22), `test_ca1_cambios_parciales_conservan_la_otra_parte_y_recalculan_la_ejecucion` (redondeo, diaria, «MIÉ»), `test_ca1_lee_el_p01_de_dos_partes_anterior_a_t197`, `test_ca1_rechaza_lo_que_ht05_no_puede_programar_sin_tocar_f10` (franja, diaria del día anterior, PERSONALIZADA, formato), `test_ca1_p01_ilegible_exige_las_dos_partes`; y las de antes `test_t87_contratos.py::test_ct04_conserva_frecuencia_y_aplica_desde_fecha_efecto` (ahora con el P-01 de tres partes) y `test_integracion.py::test_peticion_ad_hoc_y_decisiones` |
| CA-2 | `test_ca2_proximo_c1_en_la_fecha_nueva` (06-06 antes del cambio; 08-06, 22-06 y 06-07 después), `test_ca2_calendarios_de_ht05` (diaria sin fin de semana, mensual, inicio, quincenal en el año de 53 semanas, entregas), `test_ca2_los_numeros_salen_de_la_configuracion` |
| CA-3 | `test_ca3_el_c1_se_dispara_en_la_fecha_nueva_y_no_en_la_antigua`, `test_ca3_ciclo_real_disparado_lleva_su_p01_en_el_run` (integración: ciclo real con cliente mock) |
| CA-4 | `test_ca4_ningun_otro_parametro_cambia` (toda la vista de F10 salvo P-01, P-30, un solo CFG-, el disparo no escribe en F10 ni toca la configuración) |
| CA-5 | `test_ca5_disparo_perdido_se_recupera_una_vez_o_queda_perdido`, `test_ca5_limite_de_24_horas` (24 h justas: RECUPERADO), `test_ca5_sin_ejecutar_no_escribe`, `test_ca5_ciclo_cortado_queda_fallido_y_no_se_repite`, `test_ca5_p01_ilegible_falla_cerrado_sin_escribir`, `test_ca5_instante_con_zona_y_dias_antes_del_inicio`, `test_ca5_dos_procesos_a_la_vez_disparan_un_solo_c1` (cuatro bloques sobre el mismo estado, con la ventana lectura-escritura abierta a propósito) |
| CA-6 | suite, gates, cuotas, mutantes, evidencias, ciclo mock y backtest (abajo) |

## Sin el cambio fallan

- Con el `orquestacion.py` de `origin/develop` (y HT-05 y el planificador nuevos) fallan 8 de las 17 pruebas de la primera versión: las cinco de CA-1, la de `proximo` y las dos de CA-3. Sin `planificacion_c1.py` (develop entero) el módulo no se recoge.
- Mutantes (`.docs/tickets/T-197/mutantes.py`, contra `test_t197_periodicidad.py` y la prueba de CT-04 de `test_t87_contratos.py`): 32. En la primera pasada quedaron 5 vivos (M4 redondeo, M10 periodicidad del P-01, M11 `componer_p01`, M16 inicio, M32 instante con zona): M4 mostró una línea redundante, que se quita (la hora se escribe con `hora // 60`; M4 y M5 pasan a mutar la escritura y la división), y para los otros cuatro hay comprobaciones nuevas (`leer_p01` con cuatro P-01 malos, `componer_p01` con una parte vacía y `test_ca5_instante_con_zona_y_dias_antes_del_inicio`, separada para que la excepción del P-01 ilegible no tape la de la zona). Segunda pasada, con los 32: **32 muertos, 0 vivos**.

## Ciclo mock y backtest frente a develop

`.docs/tickets/T-197/` no guarda las salidas; se repite con `python -m bloque_a.cli --cliente mock …` desde `bloque_a/11_Ejecutor` de cada árbol (develop extraído con `git archive`):
- **Backtest del README** (2024-01-05 a 2024-03-29): `senales.csv`, `pronosticos.csv` y `metricas.json` idénticos; informes, paquetes y F5 idénticos salvo las rutas de salida; `consumo.csv` solo difiere en `latencia_s` (tiempo real) y por eso los `_hash` de F5.
- **Ciclo** (`--as-of 2026-06-05 ciclo`): mismo resumen salvo las rutas; mismos entregables salvo las rutas.
- **CT-04 de ejemplo** (`decision --json ejemplos/peticiones/decision_ejemplo.json`): mismo acuse; el único cambio declarado es el P-01 de F10, «SEMANAL · LUN 07:00» → «SEMANAL · SAB 06:00 · entrega LUN 07:00».

## Fusión con la rama de Astra (T-189)

`git merge-tree` de esta copia con `origin/astra/encargos-bloque-a-c38-c47`: `orquestacion.py`, `cli.py`, `por_defecto.yaml` y `mapa_plan_pruebas.json` se fusionan sin conflicto. Chocan, además de los dos ficheros que ya chocan entre develop y esa rama (`cola_astra.md` y la deuda técnica), `docs/incidencias.md` (las dos ramas añaden al final: se resuelve con las dos entradas) y `docs/evidencias_pruebas_bloque_a.md` (generado: no se resuelve a mano, se regenera con `.docs/scripts/evidencias_plan_a.py --ejecutar` después de fusionar). Corregido en la r02 (H-05); la lista de la r01 olvidaba las evidencias.

## Evidencias

`.docs/scripts/evidencias_plan_a.py --pb PB-09` → «Superada»; `--ejecutar` → 362 de 362 pruebas citadas superadas; mapa: AUTOMATICA 41, PARCIAL 18, PENDIENTE_API 7, REQUIERE_USUARIOS 1.

## Gate y cuotas

`./tools/check_all.sh` completo en esta copia (log propio, `gate2.log` del scratchpad; la primera ejecución se cortó por el límite de tiempo de la tarea y se relanzó): **12/12**. corpus-integridad, nombres-nfc, yaml-configs, secrets y refs-vivas en verde; ruff 2807 (cuota 2807), mypy A 102 (102), A-Forex 174 (174), B 159 (159); pytest A 8377 superadas, A-Forex 68, B 176. Las cuotas no suben ni bajan: el único hallazgo nuevo de ruff (orden de imports de la prueba) se corrigió, y los dos de mypy del CT-04 se resolvieron con tipos.

## Ronda r02 (QA r01 NO APTO)

| Comprobación | Resultado |
| --- | --- |
| `test_t197_periodicidad.py` | 35 (18 + 17 de la r02: 4 de H-01, 2 de H-02, 1 de H-03, 10 de H-06; H-04 son tres casos más en la prueba de rechazos) |
| Pruebas que llaman al CT-04 o a HT-05 (`test_fase1_mon_idx`, `test_fase4_huecos`, `test_integracion`, `test_t120`, `test_t122`, `test_t123`, `test_t142`, `test_t159`, `test_t160`, `test_t66_propuestas`, `test_t87_contratos`, `test_unitarias`) | 553 superadas |
| Goldens de los contratos (`tests/goldens_ct.py`, `test_fase3_goldens.py`) | coinciden; 192 superadas |
| Ataques del revisor (`revisores/r01_01_ataques.py`) | **35 de 35** (A1, A2, A3 ×3 y A9 incluidos); A4, con cuatro procesos reales, cinco veces seguidas en verde |
| Mutantes del revisor (`revisores/r01_02_mutantes.py`, en una copia del árbol) | 16 muertos de 17; vivo solo R4, equivalente según la QA r01 (el adelanto es siempre mayor que 0) |
| `mutantes.py` (58: los 32 de la r01, los vivos del revisor salvo R4 y los de las correcciones, M33 a M58), en una copia del árbol | **58 muertos de 58** |
| Evidencias (`evidencias_plan_a.py --ejecutar`) | 379 de 379 citadas superadas; PB-09 «Superada» |
| ruff y mypy | ruff 2807 (cuota 2807), mypy A 102 (cuota 102) |
| Gate (`./tools/check_all.sh` completo, lanzado con `setsid nohup` y log propio `scratchpad/gate_t197_r02.log`) | **12/12**: corpus, NFC, YAML, secretos, refs vivas; ruff 2807, mypy A 102, A-Forex 174, B 159; pytest A 8394 superadas (y las 2 omitidas de `test_t149.py`), A-Forex 68, B 176 |

## Ronda de cierre de la QA r02

| Comprobación | Resultado |
| --- | --- |
| `test_t197_periodicidad.py` | 38 (+3 de H-07; H-08 cambia las aserciones de la prueba del proceso muerto) y la de CT-04 de `test_t87`: 39 superadas |
| Pruebas vecinas del CT-04 y de HT-05 (las doce de la r02, más `test_fase3_goldens.py` y `test_fase4_mapa.py`) | 768 superadas |
| `revisores/r02_01_ataques.py` | **12 de 12** (B2 de H-07 y B3 de H-08 incluidos) |
| `revisores/r01_01_ataques.py` | 34 de 35: A9 falla en su última aserción (`"estado_run" not in f5`), la que la QA r02 sustituye por B3 |
| `revisores/r01_02_mutantes.py` (copia del árbol) | 16 muertos de 17; vivo R4, equivalente |
| `mutantes.py` (65: M59 a M65 nuevos; M52 y M56 reescritos), en una copia del árbol | **65 muertos de 65** |
| Evidencias (`--ejecutar`) | 382 de 382 citadas superadas; PB-09 «Superada»; `test_fase4_mapa.py` 23 superadas |
| ruff y mypy | ruff 2807, mypy A 102 (en sus cuotas) |
| Gate completo | no se repite en esta ronda (lo pasa la integración, por indicación de la coordinación) |

## Segunda ronda de cierre de la QA r02

| Comprobación | Resultado |
| --- | --- |
| `test_t197_periodicidad.py` + la de CT-04 de `test_t87` | 42 superadas (+3: H-09 y H-10 ×2) |
| `revisores/r01_01_ataques.py` (A9 corregida por el revisor) + `revisores/r02_01_ataques.py` | **47 de 47** |
| `revisores/r02_02_mutantes_cierre.py`, en una copia del árbol | **4 muertos de 4** (C1 a C3, los de H-09 y H-10, y C4) |
| `revisores/r01_02_mutantes.py`, en la copia | 16 muertos de 17; vivo R4, equivalente |
| `mutantes.py` (68: M66 a M68 son C1 a C3), en la copia | **68 muertos de 68** |
| Pruebas vecinas del CT-04 y de HT-05 (las de la r02 y `test_fase3_goldens.py`) | 745 superadas |
| Evidencias (`--ejecutar`) | 385 de 385 citadas superadas; `test_fase4_mapa.py` 23 superadas |
| ruff | 2807 (cuota); el código del ejecutor no cambia en esta ronda, así que mypy sigue en 102 |
| Gate completo | no se repite (lo pasa la integración) |
