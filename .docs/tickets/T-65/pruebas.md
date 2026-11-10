# T-65 · Pruebas

| Suite | Antes | Después |
| --- | --- | --- |
| `bloque_a/11_Ejecutor` (pytest) | 201 pasan (165 s) | **265 pasan** (176 s): +40 en `tests/test_t65_hallazgos.py` y +24 en `tests/test_t65_resto_t53.py`; dos pruebas de T-53 adaptadas (abajo) |
| `.docs/scripts/prueba_refs_vivas.py` | no existía (con el `tools/refs_vivas.py` anterior, 4/6) | 6/6 |
| `.docs/tickets/T-65/mutaciones.py` | — | 39/39 mutaciones detectadas |
| ruff (tres ejecutores) | 3102 (cuota 3109) | 3083 |
| mypy `bloque_a` | 123 (cuota 123) | 123 |
| `bloque_a_forex`, `bloque_b` | 68 y 174 | sin tocar (en el gate) |

## Criterio de aceptación → prueba

| Criterio | Prueba |
| --- | --- |
| CA-1 · cada corrección con una prueba que falla sin ella | Las 39 mutaciones de `mutaciones.py` (tabla de abajo) y `prueba_refs_vivas.py` contra el script anterior (falla en 2 de 6 casos) |
| CA-2 · los puntos ya hechos citan su prueba y pasa | H-06: `test_t66_propuestas.py::test_h06_todo_pausado_no_redacta_ni_falla_en_el_esquema`. H-12: `test_t53_seleccion_y_entrega.py::test_h12_dos_bloques_con_la_misma_configuracion_no_comparten_la_tabla_de_horizontes`. Las dos pasan en la suite de 265 |
| CA-3 · lo no hecho, con motivo y destino | Tabla del `README.md` (CS-10 P-07 → T-57; CS-11, 44 parámetros en F10 → T-83 y T-57; CS-18, ρ del prompt → revisión del corpus; CS-08, promoción → revisión del corpus) y límites de `analisis-tecnico.md` |
| CA-4 · ningún número nuevo en el código; los del operador `[PROPUESTO]` | `test_cs10_todas_las_claves_leidas_existen_en_por_defecto` (las 64 rutas leídas con `parametro()` existen en el YAML), `test_h08_*`, `test_h09_*` (7 incidencias marcadas junto a su clave) |
| CA-5 · suite en verde y por encima de 201; gate 12/12 | 265 pasan; gate abajo |
| CA-6 · sin tocar lo prohibido ni el corpus | `git status`: solo `bloque_a/11_Ejecutor/`, `.docs/tickets/T-65/`, `.docs/scripts/prueba_refs_vivas.py` y `tools/refs_vivas.py` (ver la nota de H-11). Gate `corpus-integridad` en verde |

## Regresiones

Las comprueba `python3 .docs/tickets/T-65/mutaciones.py`. El script quita cada corrección (sustituye el texto en el archivo), ejecuta su prueba y restaura el archivo comprobando su huella. Resultado: **39/39 FALLA** (todas detectadas).

| Punto | Mutación (se quita la corrección) | Prueba que falla |
| --- | --- | --- |
| H-07 | El Evaluador usa la tabla del módulo · la síntesis usa la función del módulo | `test_h07_dos_evaluadores_con_tablas_distintas_no_se_pisan`, `test_h07_la_sintesis_usa_la_tabla_de_su_bloque` |
| H-08 | Literal 65 en el siguiente paso · una clave nula se acepta | `test_h08_umbrales_de_presentacion_sin_respaldo_en_el_codigo`, `test_h08_un_parametro_que_falta_en_todas_partes_falla_cerrado` |
| H-09 | Sin `[PROPUESTO]` en INC-T53-03 | `test_h09_incidencias_marcadas_propuesto_junto_a_su_clave` |
| H-10 | `estado_g3` en memoria · carpeta antigua del C6 · `DatosInvalidos` como «sin datos» | `test_h10a_…`, `test_h10b_…`, `test_h10c_…` |
| H-13 | `efecto_desde` = as_of + 1 | `test_h13_la_degradacion_registra_el_efecto_desde_el_mismo_ciclo` |
| H-14 | El rechazo de la ficha no se anota | `test_h14_una_ficha_rechazada_por_el_motor_se_declara` |
| H-15 | Cierres ≤ 0 aceptados · duplicadas como `ValueError` · sin el `except` genérico · fechas ilegibles sin capturar | `test_h15_simbolo_con_datos_invalidos_se_excluye_y_se_declara`, `test_h15_cualquier_error_del_proveedor_para_un_simbolo_se_declara`, `test_h15_csv_con_fechas_ilegibles_se_excluye_y_se_declara` |
| H-16 | Todos los proxies a ML-CLUS-001 | `test_h16_un_finalista_con_poca_historia_no_desactiva_los_clusteres` |
| H-17 | Sin validación · sin lunes de Pascua | `test_h17_ps2_festivos_mal_formado_impide_crear_el_bloque`, `test_h17_lunes_de_pascua_configurable_y_propuesto_desactivado` |
| H-20 | Un contenedor que no es lista es «sin objeciones» | `test_h20_contenedor_mal_formado_cuenta_como_fuerte_abierta` |
| H-21 | Se sanea el texto propio · una incidencia por cita · sin `run_id` | `test_h21_texto_propio_del_analista_llega_intacto`, `test_h21_lo_externo_se_sanea_con_run_id_y_una_incidencia_por_fuente` |
| CA-14 | 21 sesiones por mes fijas · tasa base 0,5 · zona ±5 % · umbral C6 del 5 % | `test_ca14_*` (4) |
| CA-15 | Un solo contador de `msg_id` · `participantes` sin ordenar | `test_ca15_*` (2) |
| CS-08 | Sin fichas «Documentado» · alternativa no servible | `test_cs08_*` (2) |
| CS-10 | 200 réplicas · 2 celdas · falta `ps1` en el YAML | `test_cs10_*` (3) |
| CS-11 | Clave oculta `_parametros_ht03` · YAML distinto del corpus · regímenes incompletos · P-30 «4.0» | `test_cs11_*` (4) |
| CS-18 | Ventana de «2 años + 14 días» | `test_cs18_la_ventana_de_clusteres_sale_de_la_configuracion` |
| CS-19 | Sin la fila de PB-56 en el mapa | `test_cs19_mapa_cubre_las_67_pruebas_del_plan` |
| CS-23 | Cita de `test_herramientas.py` | `test_cs23_herramientas_cita_una_prueba_que_existe` |
| H-11 | `tools/refs_vivas.py` anterior (`git show HEAD:tools/refs_vivas.py`) | `prueba_refs_vivas.py`: fallan «revisores/ con una ruta rota falla» y «orden con argumentos viva» |

**Pruebas existentes adaptadas** (comprobaban el comportamiento que se corrige):

- `test_t53_evaluacion_y_almacen.py::test_bandas_desde_configuracion_y_validadas`. Esperaba que crear un `Evaluador` cambiara la tabla del módulo, que es justo el defecto H-07. Ahora comprueba la tabla de la instancia, que la del módulo no cambia y que una tabla inválida falla al validar y al crear el Evaluador.
- `test_t53_seleccion_y_entrega.py::test_h01_historia_corta_tambien_queda_declarada`. Esperaba «clústeres de exposición no calculados» para todos. Con H-16 se declara solo el proxy corto («sin medir para USDNEW=X»), y el run sigue PARCIAL.

## Gate

Comando: `.docs/scripts/gate.sh` con `--completo` (llama a `./tools/check_all.sh`).

**12/12 en verde** (2026-11-10, log `.docs/scripts/.logs/gate_20261110_133352.log`; la carpeta `.logs` no se sube):

| Gate | Resultado |
| --- | --- |
| corpus-integridad, nombres-nfc, yaml-configs, secrets | ✓ |
| refs-vivas | ✓ |
| ruff (hallazgos) | ✓ (3083 ≤ 3109) |
| mypy bloque_a · bloque_a_forex · bloque_b | ✓ (123 · 174 · 159) |
| pytest bloque_a | ✓ 265 passed |
| pytest bloque_a_forex | ✓ 68 passed |
| pytest bloque_b | ✓ 174 passed |

Una primera ejecución (`gate_20261110_132654.log`) dio 11/12. Falló `refs-vivas` por dos citas de este mismo ticket (una ruta de ejemplo y un comodín en `analisis-tecnico.md`, ya corregidas) y por una de `.docs/tickets/T-80/qa.md`, de otro agente, que ya no fallaba en la segunda ejecución.

Además: `python3 tools/refs_vivas.py` pasa, y ya no excluye las carpetas `revisores/`. Con el script anterior, el gate `refs-vivas` fallaba por una cita de otro ticket en curso (`.docs/scripts/gate.sh --completo` en `.docs/tickets/T-80/analisis-tecnico.md`); con el arreglo de H-11, esa cita cuenta como viva.

## Comandos usados

```bash
cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q -p no:cacheprovider      # 201 antes · 265 después
../../.venv/bin/python -m pytest -q -p no:cacheprovider tests/test_t65_hallazgos.py tests/test_t65_resto_t53.py
cd ../.. && python3 .docs/tickets/T-65/mutaciones.py                                     # 39/39
python3 .docs/scripts/prueba_refs_vivas.py                                               # 6/6
git show HEAD:tools/refs_vivas.py > /tmp/viejo.py && python3 .docs/scripts/prueba_refs_vivas.py /tmp/viejo.py   # 4/6
.venv/bin/ruff check --output-format=concise bloque_a/11_Ejecutor bloque_a_forex/11_Ejecutor bloque_b/11_Ejecutor | wc -l
.venv/bin/mypy --ignore-missing-imports --no-error-summary bloque_a/11_Ejecutor/bloque_a | wc -l
.docs/scripts/gate.sh --completo
```
