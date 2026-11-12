# T-103 · Pruebas

| Suite | Antes | Después |
| --- | --- | --- |
| Bloque A (`pytest -q bloque_a/11_Ejecutor`) | 607 | 630 (23 nuevas en `tests/test_t103_r8_y_bajos.py`) |
| `test_t92_revision.py`, `test_t93_hallazgos.py` y `test_v51.py` | 120 en verde | 120 en verde |
| `r01_01_r8_escapes.py` (T-93) | 9 fallos | 0 fallos |
| `r01_02_almacen_legado.py` (T-93) | 2 fallos | 0 fallos |
| `r01_03_plazos_tipos.py` (T-93) | 1 fallo | 0 fallos |
| `r04_01_r8_regla_texto.py` (T-92) | 0 fallos | 0 fallos (formatos de proveedor al 100 %, 0 de 12 textos de H-33, corpus del bloque sin marcas, peor tiempo 0,92 s) |

`r01_01` caso 5 (INFO): las colas de 5×5, 4×6 y 4×8 cifras pasan a 2000/2000; las de 4×6 y 3×10 mayúsculas siguen en 0/2000 (declarado). Caso 4 (INFO): siguen 6 de 10 titulares con cifra y unidad (H-45, declarado).

## Criterio de aceptación → prueba

| Criterio | Prueba |
| --- | --- |
| CA-1 | `test_h40_*` (12 escapes y la clave de dict), `test_h44_*`; `r01_01` con 0 fallos |
| CA-2 | `test_h42_*` (legado y sellado), `test_h43_*`; `r01_02` y `r01_03` con 0 fallos |
| CA-3 | `r04_01` con 0 fallos; `test_h41_el_texto_con_fechas_sigue_sin_ser_clave` |
| CA-4 | Con el código de HEAD (`git stash`), 18 de las 23 nuevas fallan. Pasan 5: los 3 textos que no son clave (vigilan falsos positivos), el escape doble `\\/` (ya se veía) y la cola de 4×8 cifras (tramos de 8 cifras, que nunca fueron texto) |
| CA-5 | Gate de `commit_limpio.sh` |

## Regresiones

Sin la corrección fallan 11 de los 12 casos de escapes de H-40, la clave de dict, 2 de los 3 de colas de cifras (H-41), el de `frozenset` con «\n» (H-44), los dos del almacén (H-42) y el CNS sin plazo (H-43).

## Gate

`./tools/check_all.sh` completo desde `.docs/scripts/commit_limpio.sh` (solo hace el commit con 12/12); ruff de los archivos tocados sin errores nuevos (2 antes y 2 después).

## Ronda r02

| Suite | Antes | Después |
| --- | --- | --- |
| `tests/test_t103_r8_y_bajos.py` | 23 | 31 |
| `test_t92_revision.py`, `test_t93_hallazgos.py` | 107 | 107 |
| `revisores/r01_01_r8_escapes_y_falsos.py` | 0 fallos | 0 fallos (colas de tres grupos de 6, 7 u 8 cifras y de tres fechas, 500 de 500) |
| `revisores/r01_03_almacen_cortes.py` | 3 fallos (caso 7) | 0 fallos |
| `revisores/r01_02_r8_rendimiento.py` | 3 fallos (129 s y 592 s con 99.999 barras) | 0 fallos (0,013 s y 0,037 s) |
| `r04_01` de T-92 y `r01_01`/`r01_02` de T-93 | 0 fallos | 0 fallos |
