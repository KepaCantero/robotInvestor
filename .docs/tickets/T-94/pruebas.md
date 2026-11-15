# T-94 · Pruebas

## Ronda r03 (15-11-2026)

| Suite | r02 | r03 |
| --- | --- | --- |
| `.docs/scripts/pruebas_banco_medida.py` | 51 | 82 en verde (unos 26 s) |
| `.docs/scripts/pruebas_registro_experimentos.py` | 20 | 20 |
| Mutantes `.docs/tickets/T-94/mutantes_r03.py` | 0 de 29 vivos | 0 de 57 vivos |
| Mutantes del revisor `revisores/r02_07_mutantes.py` | 8 de 34 vivos | ninguno vivo entre los que aún casan con el código; los 8 que ya no casan están rehechos en `mutantes_r03.py` (M09, M17, M18, M21, M40, M41, M47 y M49) |

Hallazgos de la QA r02 y sus pruebas:
- H-13: `test_h13_solo_fechas_sin_solape` y `test_h13_ventanas_solapadas_sobre_activos_distintos_no_suman_fechas`.
- H-14: `test_h04_otra_semilla_es_otra_variante_del_mismo_experimento` (también otro periodo) y `test_h14_simulado_y_real_son_experimentos_distintos`.
- H-15: `test_h15_verificar_sin_registro_md_y_experimento_danado`.
- H-16: `test_h16_csv_raros` (dd/mm, formatos mezclados, fecha repetida, columnas repetidas, sin filas, vacío).
- H-17: `test_h17_orden_canonico_fechas_normalizadas_horizonte_y_universo`.
- H-18: `test_h18_*`.
- H-19: `test_h19_*` y las cotas en `test_h02_pocas_observaciones_no_dan_veredicto`.
- H-20: `test_h20_*`.

Simulación nula con fechas suficientes (`.docs/tickets/T-94/nula_r03.py`): un 9,5 % y un 10,0 % de veredictos firmes sin habilidad, para un 10 % nominal.

Ejecución del README: 39 selecciones del titular, de las que 36 quedan fuera de la muestra (con H3, en tres meses cabe una sola fecha sin solape). Resultado: «todavía no se sabe», con 1 fecha de un mínimo de 10. `verificar` dice que las huellas casan.

## Ronda r02 (15-11-2026)

| Suite | Antes (r01) | Después (r02) |
| --- | --- | --- |
| `.docs/scripts/pruebas_banco_medida.py` | 12 de 12 | 51 de 51 en verde (unos 22 s) |
| `.docs/scripts/pruebas_registro_experimentos.py` | 20 de 20 | 20 de 20 |
| Mutantes `.docs/tickets/T-94/mutantes_r02.py` | 6 de 12 vivos (QA r01) | 0 de 29 vivos |
| Suites de los bloques y del marco | Sin cambios | Sin cambios: el banco no toca ningún bloque ni el marco (CA-8) |

Scripts del revisor de la r01, contra la versión 0.3.0:
- `r01_02`: los escenarios A, B y C, en el 3,0 %, el 0,0 % y el 0,0 %. El techo es el 16 %.
- `r01_05`: 0 fallos. Veinte semillas dan un experimento con 19 intentos fuera del máximo; el intento fallido queda anotado; `verificar` existe; el experimento ajeno se rechaza.
- `r01_04`: azar con más filas que miembros da `BancoError`; momento con un miembro sin historia suficiente da las mismas selecciones; el evaluador no mira datos fuera de la ventana.
- `r01_03` y `r01_08`: los cierres imposibles ya no entran. El banco se detiene con `BancoError` y el motivo, que es el comportamiento pedido; los scripts lo reciben como una excepción sin capturar.
- `r01_01`: la clave `rango90` pasa a ser `rango` con su `nivel`, porque el nivel es ahora un argumento. El oráculo equivalente está en `test_h11_borde_del_cero_y_nivel_frente_a_un_oraculo`.

## Criterio de aceptación → prueba

| Criterio | Prueba |
| --- | --- |
| CA-1 | `test_integracion_bloque_a`: deja `prerregistro.json`, `informe.json` e `informe.md` |
| CA-2 | `test_exceso_frente_a_la_cesta`: exceso exacto con precios a mano, en LARGO y en CORTO |
| CA-3 | `test_momento_sin_datos_futuros`: alterar precios posteriores al corte no cambia la selección |
| CA-4 | `test_informe_reproducible` y la doble ejecución de `test_integracion_bloque_a`: informes idénticos byte a byte |
| CA-5 | `test_veredictos` y `test_h11_borde_del_cero_y_nivel_frente_a_un_oraculo` (`[0, x]` y `[x, 0]` dan «todavía no se sabe») |
| CA-6 | `test_sin_precio_final_queda_sin_resolver`, `test_h03_cierres_imposibles_detienen`, `test_h03_series_imposibles_en_evaluar_y_momento` y `test_h03_columnas_y_fechas` |
| CA-7 | `test_integracion_bloque_a`, `test_informe_reproducible` y `test_h09_aviso_por_partes` |
| CA-8 | `test_integracion_bloque_a`: `git status` de `bloque_a`, `bloque_b` y el marco común igual antes y después |

## Hallazgo de la QA r01 → prueba de regresión

| Hallazgo | Pruebas |
| --- | --- |
| H-01 | `test_h01_apuesta_repetida_cuenta_una_vez`, `test_h01_remuestreo_por_fechas_y_efectivas` y `test_h01_simulacion_nula_no_afirma` (40 mundos nulos, ≤ 15 % de veredictos firmes) |
| H-02 | `test_h02_pocas_observaciones_no_dan_veredicto` (n = 1, 2 y 9; con 10 sí hay veredicto) |
| H-03 | `test_h03_*` (vacío, espacio, nan, inf, −inf, negativo, cero y texto; columnas; fechas; JSON estricto) |
| H-04 | `test_h04_otra_semilla_es_otra_variante_del_mismo_experimento`, `test_h04_experimento_ajeno_rechazado_sin_anotar` y `test_h04_verificar_detecta_reescrituras` |
| H-05 | `test_h05_fallo_despues_del_titular_queda_anotado` (BancoError en `evaluar` y una excepción cualquiera) |
| H-06 | `test_h06_referencias_iguales_al_titular_o_se_detienen` |
| H-07 | `test_h07_coste_con_cache_uc_y_coste_cero` |
| H-08 | `test_h08_fuga_sin_veredicto_y_advertencias` |
| H-09 | `test_h09_aviso_por_partes` |
| H-10 | `test_h10_clase_direccion_y_simbolo`, `test_h10_parametros_de_la_estadistica` y `test_h10_argumentos_de_la_linea_de_ordenes` |
| H-11 | `test_h11_*` y `mutantes_r02.py` |
| H-12 | `analisis-tecnico.md`, este fichero y la fila T-94 de la deuda |

## Ejecución de ejemplo (r02)

`.venv/bin/python .docs/scripts/banco_medida.py a --desde 2026-03-06 --hasta 2026-05-29 --salida <carpeta> --registro <carpeta>/r.jsonl`, con el cliente simulado y los datos sintéticos:

| Contendiente | Selecciones | Repetidas | Resueltas | Fechas efectivas | Exceso medio |
| --- | --- | --- | --- | --- | --- |
| titular (A) | 39 | 35 | 4 | 2 | +1,33 % |
| azar | 39 | 33 | 6 | 3 | −0,03 % |
| momento | 39 | 34 | 5 | 3 | −0,40 % |

Las dos comparaciones dan «todavía no se sabe», porque hay pocas observaciones efectivas (2 de un mínimo de 10 por lado). El informe copia la advertencia de fuga de A y el aviso de cliente simulado. `verificar` dice que las huellas casan.

**Esto no mide a A:** con el cliente simulado las señales salen de reglas sintéticas, y los precios son de ejemplo.

## Lint

`ruff check` sobre `banco_medida.py`, `pruebas_banco_medida.py`, `registro_experimentos.py` y `mutantes_r02.py`: sin hallazgos. En la r01 había dos en `registro_experimentos.py`, que ahora están corregidos. El gate del repositorio no cubre `.docs/scripts/`, porque sus cuotas son de los ejecutores.

## Gate

Se ejecuta en el commit con `.docs/scripts/commit_limpio.sh` (gate completo en una copia limpia).
