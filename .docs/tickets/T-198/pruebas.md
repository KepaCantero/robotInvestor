# T-198 · Pruebas

| Suite | Antes | Después |
| --- | --- | --- |
| `tests/test_t198_buscador_ct19.py` (nueva) | — | 20 superadas |
| `test_t125_fiabilidad_fuentes.py`, `test_t125_r02.py`, `test_t125_r03.py` (vecinas: el CT-19 del ciclo) | 72 | 72 superadas, sin cambiarlas |
| Bloque A completo | ver «Gate» | ver «Gate» |

## Criterio de aceptación → prueba

| Criterio | Prueba (`tests/test_t198_buscador_ct19.py`) |
| --- | --- |
| CA-1 | `test_ca1_las_dos_fuentes_del_plan_quedan_en_f9_con_su_fiabilidad_medida` (el caso del plan; con un pronóstico más sin vencer: 26 registrados y 25 resueltos; la Q del corpus no cambia), `test_ca1_con_la_configuracion_por_defecto_tal_cual` (`cargar_config()` sin cambios), `test_ca1_en_un_ciclo_el_buscador_atiende_el_ct19` |
| CA-2 | `test_ca2_un_ct19_que_no_cuadra_no_escribe_nada_en_f9` (16 mensajes malos, la mayoría con la primera fuente buena, y una fuente que no es de F9), `test_ca2_un_ct19_sin_msg_id_no_se_atiende_aunque_f6_no_anote_ninguno`, `test_ca2_el_ct19_bueno_si_se_atiende`, `test_ca2_en_el_ciclo_queda_una_incidencia_y_se_reintenta_en_el_siguiente`, `test_ca2_un_error_del_almacen_no_se_traga` |
| CA-3 | `test_ca3_atender_dos_veces_no_duplica_y_el_ciclo_siguiente_no_reenvia`, `test_ca3_dos_instancias_a_la_vez_dejan_una_entrada_por_fuente` (cuatro `Almacen` sobre la misma carpeta, a la vez con una barrera) |
| CA-4 | `test_ca4_una_fue_comunicada_antes_de_t198_se_atiende_en_el_ciclo_siguiente`, `test_ca4_la_mas_reciente_de_una_fuente_queda_la_ultima` |
| CA-5 | `test_ca5_anotar_candidatas_solo_las_de_f9_con_fiabilidad_y_sin_fuga`, `test_ca5_en_un_ciclo_la_busqueda_del_buscador_lleva_la_fiabilidad_medida` |
| CA-6 | `test_ca6_solo_ag16_escribe_f9_y_solo_fiabilidad_medida`, `test_ca6_un_almacen_sellado_antes_de_t198_abre_y_sella_f9_vacio`, `test_ca6_f9_sin_sello_o_borrado_falla_cerrado` |
| CA-7 | `test_ca7_sin_fue_no_hay_ct19_ni_f9_ni_anotacion`, `test_ca7_el_ct19_al_buscador_conserva_sus_campos`, `test_ca7_ningun_texto_de_f9_dice_valid`; las 72 de T-125; ciclo mock y backtest; suite y gate (abajo) |

## Regresiones y mutantes

- **Sin el cambio fallan.** En una copia con `almacen.py` y `orquestacion.py` de `origin/develop` (y el resto de T-198), 18 de las 19 pruebas de la primera versión fallan; la que pasa es `test_ca7_el_ct19_al_buscador_conserva_sus_campos`, que comprueba que el cuerpo del CT-19 no cambia.
- **Mutantes** (`mutantes.py`, 34, sobre una copia del árbol): primera pasada, 32 muertos y 2 vivos, que no eran equivalentes:
  - M10 (mensaje sin msg_id admitido): con una FUE- recién escrita (`comunicado_ct19` None) un mensaje con `msg_id` None pasaría el cotejo con F6. Nueva prueba `test_ca2_un_ct19_sin_msg_id_…`.
  - M15 (`resueltos` = registrados): en el caso del plan los dos números eran 25. La prueba de CA-1 añade un pronóstico sin vencer (26 frente a 25).
  - Segunda pasada, con las dos pruebas reforzadas: **34 de 34 muertos**.

## Ciclo mock y backtest

`bloque-a --cliente mock --datos ejemplos/datos_sinteticos --universo config/universo_ejemplo.csv` con `--as-of 2026-06-05 ciclo` y con `backtest --desde 2024-01-05 --hasta 2024-03-29` (`python -m bloque_a.cli`), en develop (`git archive origin/develop`) y en T-198: rc 0 los cuatro. `senales.csv`, `pronosticos.csv` y `metricas.json` son idénticos byte a byte; `consumo.csv` es igual salvo la columna `latencia_s`; F5 y los informes técnicos difieren solo en la ruta de la carpeta temporal; `sellos_integridad.json` gana la clave `F9` (vacío). Ningún `F9_registro_fuentes.jsonl` en ninguno de los dos (no hay FUE-). Script: `scratchpad/comparar.sh` (no se sube; los comandos son los de arriba).

## Gate

`./tools/check_all.sh`: corpus-integridad, nombres-nfc, yaml-configs, secrets, refs-vivas, ruff y mypy ×3 en verde (9/12). Las tres pytest no terminaron en esta sesión: dos ejecuciones se cortaron desde fuera (exit 144, otra sesión compartía el log y mató procesos) y la tercera, con log propio (`scratchpad/gate_t198.log`), seguía corriendo al entregar. Antes de cortarse, el primer 34 % de la suite de A había pasado sin fallos; las 352 pruebas citadas por el mapa, todas superadas (`evidencias_plan_a.py --ejecutar`). **Pendiente: 12/12.**

- ruff (A + A-Forex + B, como el gate): 2807 (cuota 2807, sin subir; `fiabilidad_f9.py` y `test_t198_buscador_ct19.py` limpios).
- mypy de A: 102 (cuota 102, sin subir; ningún error en `fiabilidad_f9.py` ni nuevo en `almacen.py` u `orquestacion.py`).

## Comandos

Los de `analisis-tecnico.md`, más `.venv/bin/python .docs/scripts/evidencias_plan_a.py --ejecutar` y `./tools/check_all.sh`.

## Ronda r02 (QA r01 NO APTO)

| Suite o script | Resultado |
| --- | --- |
| `tests/test_t198_buscador_ct19.py` | 29 pruebas, 35 casos, superadas (eran 20); los `test_r02_…` y CA-1 reforzada, una por hallazgo (tabla en `analisis-tecnico.md`) |
| `revisores/r01_ataques.py` (sin cambiarlo) | 10 de 10 en verde (eran 2 en rojo: H-01 y H-03) |
| `revisores/r01_sello_generico.py` | rc 0: HA, F4 y F6 fallan cerrado (era rc 1) |
| `revisores/r01_mutantes.py` | 9 de 9 muertos (eran 3) |
| `mutantes.py` | 48 de 48 muertos: los 34 de la r01, R1–R6 del revisor y M35–M42 de las correcciones. En la primera pasada quedó vivo M41 (timestamp no ISO admitido): «ayer» lo rechazaba igual `fromisoformat`; se añadió el caso «2026-06-04 y algo más» y murió |
| Vecinas: T-125 (tres suites) y `test_t134_r03_t125.py` | 94 superadas |
| Evidencias (`evidencias_plan_a.py --ejecutar`) | 357 de 357 citadas superadas; PB-46 sigue «Superada en parte» |
| ruff · mypy A / FX / B | 2807 · 102 / 174 / 159 (cuotas iguales, no suben) |

**Gate r02** (`./tools/check_all.sh`, log propio `scratchpad/gate_t198_r02.log`, lanzado con `setsid nohup`): al entregar, 9 de 12 en verde (corpus, NFC, YAML, secretos, refs, ruff, mypy ×3) y pytest de A en curso. **El 12/12 queda por confirmar en ese log** (el proceso sigue vivo y escribe en él; nadie más lo usa).

## Ronda de cierre de la QA r02

| Suite o script | Resultado |
| --- | --- |
| `tests/test_t198_buscador_ct19.py` (30 pruebas, 36 casos) + `revisores/r01_ataques.py` + `revisores/r02_ataques.py` + vecinas (T-125 ×3, `test_t134_r03_t125.py`) | 143 superadas, rc 0 (`r02_ataques.py`: H-08 en verde) |
| `revisores/r01_sello_generico.py` | rc 0 |
| `revisores/r01_mutantes.py` | 9 de 9 muertos |
| `revisores/r02_m12_repetido.py <copia> 8` | M12 vivo en 0 de 8 pasadas (rc 0) |
| `revisores/r01_ciclo_mock.sh` (develop frente a T-198) | rc 0 los dos; paquete JSON e informe visual iguales; el técnico, solo la ruta temporal; sin `F9_registro_fuentes.jsonl` |
| `mutantes.py` (50: los 48 de la r02 más M43 y M44 de H-08), con otras tareas en marcha en la máquina | 50 de 50 muertos, M12 incluido |

Gate completo: no se repite en esta ronda por indicación del coordinador (cambian una condición y pruebas; el de la r02, `scratchpad/gate_t198_r02.log`, dio 12/12 según la QA r02). Lo vuelve a pasar la integración con `commit_limpio.sh`.
