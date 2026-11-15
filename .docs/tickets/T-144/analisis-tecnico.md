# T-144 · Análisis técnico

## Causa raíz

- **H-01.** `_etiquetas_series_copiadas` (T-135) solo comparaba rentabilidades fecha a fecha, cada serie entre sus propios precios consecutivos, con una tolerancia relativa del 1 % al mayor. Con una sesión ausente, la rentabilidad del día siguiente es de dos sesiones en una serie y de una en la otra; con 2 decimales, los días de rentabilidad pequeña rompen la tolerancia relativa (268 de 319 sesiones en el caso GBX→GBP del revisor). Así solo se agrupaban copias idénticas en coma flotante.
- **H-02.** T-135 ponía a ``None`` en la firma del aviso la total cuando era la circulante; en una copia con la circulante movida, la total dejaba de repetir y aparecían dos diferencias.
- **H-03.** El bucle sobre las T fechas con matrices n × n solo cortaba cuando todos los pares diferían; un par sin fechas comunes lo impedía.
- **H-04.** `_serie` y la vía `ent["series"]` aceptaban precios ≤ 0 (preexistente).

## Por qué esta regla y no el cociente ingenuo

El revisor midió que «copia si max |log(pᵢ/pₖ) − mediana| ≤ 1 %» agrupa los cuatro casos pero toma por copias el 6 % de los índices con ρ ≈ 0,995 y todos los fondos con error de seguimiento del 0,1 %/año. La regla de niveles usa como tolerancia el **error de redondeo de cada serie**, que sale de sus propios datos (su paso de precio), no un número fijo: con datos sin redondear la cota es del orden de 1e-10 y solo agrupa cocientes constantes de verdad; con 2 decimales a ~12 (la acción en libras), 4e-4; y nunca pasa de log(1,01) (la de los casi clones). Medido (`.docs/tickets/T-144/pruebas.md`):

| Pares (300 semillas, 320 sesiones) | sin redondear | 3 decimales | 2 decimales |
| --- | --- | --- | --- |
| índices con ρ ≈ 0,995, nivel 100 / 12 / 2 | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 |
| precio frente a rentabilidad total (2 %/año) | 0 / 0 / 0 | 0 / 0 / 0 | 0 / 0 / 0 |
| fondo frente a índice, TE 0,1 %/año | 0 / 0 / 0 | 0 / 0 / 9 | 0 / 55 / 300 |
| fondo frente a índice, TE 0,01 %/año | 0 / 0 / 0 | 0 / 57 / 300 | 101 / 300 / 300 |

Los fondos con datos redondeados gruesos frente a su precio no se distinguen de su índice a esa resolución: se toman por copias y la amplitud no se sirve (falla cerrado; límite declarado en INC-T128-01).

## Implementación

- `bloque_a/11_Ejecutor/bloque_a/motor/frontera_b.py`: `_paso_de_precio`, `_pares`, `ELEMENTOS_POR_TRAMO`, `_etiquetas_series_copiadas` reescrita (las dos reglas sobre pares candidatos en tramos; argumento opcional `tol_numerica`, por defecto `FRONTERA_B["tolerancia_numerica_copias"]`, así que la firma de cuatro argumentos del revisor sigue valiendo); `FRONTERA_B["tolerancia_numerica_copias"]`; `_aviso_casi_clones(…, repetidos=None)`.
- `motor/fichas_mon_idx.py`: IDX-CONC-001 rechaza precios no positivos o no finitos y pasa `tol_numerica` = la tolerancia de la ficha.
- `motor/fichas_p2.py`: CHR-TOKEN-001 lleva total y máxima en la firma del aviso y su marca `repetidos_aviso`.
- Pruebas cambiadas (comentadas «T-144»): `test_t135_motor.py::test_h05_etiquetas_de_series_copiadas` (los precios de la base eran enteros, paso 1, y la regla nueva tomaba por copia a «lejos», que a esa resolución lo es: se multiplican por un factor sin redondear y la prueba sigue fijando la regla de rentabilidades); `test_t127_hallazgos.py` y `test_t127_r02.py`, la igualdad exacta de `FRONTERA_B` gana la clave nueva (los tres números de antes no cambian). Ninguna se debilita.

**Decisiones `[PROPUESTO]` (INC-T128-01, «Ronda T-144»).** La regla de niveles y su cota; la tolerancia numérica; H-05 como coste declarado (contar cada grupo una vez cambiaría el caso a mano de la ficha: operador); sin *staking* ni concentración, una copia con solo el precio movido no da aviso (es la forma de dos tokens distintos de la misma oferta redonda, T-135 H-06).

**Límites.** No se detecta una copia desfasada una sesión, con un cambio de divisa variable o con rentabilidades perturbadas a propósito; los datos gruesos agrupan series casi iguales (arriba). Memoria: el índice de 2000 valores usa unos 590 MB el proceso entero (antes, 476 MB y 164 s).

## Comandos

```bash
cd bloque_a/11_Ejecutor; PY=/home/user/robotinvestor/.venv/bin/python
$PY -m pytest -q -p no:cacheprovider tests/test_t144.py tests/test_t135_motor.py tests/test_t127_hallazgos.py tests/test_t127_r02.py tests/test_t128_frontera.py tests/test_t128_r02.py
cd ../..
.venv/bin/python -I .docs/tickets/T-135/revisores/r01_01_copias_idx_conc.py bloque_a/11_Ejecutor
.venv/bin/python -I .docs/tickets/T-135/revisores/r01_02_aviso_firmas.py bloque_a/11_Ejecutor
.venv/bin/python .docs/tickets/T-147/mutantes.py <copia con «t147_mut»> --ticket T-144
```
