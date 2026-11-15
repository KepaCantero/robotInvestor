# T-144 · Bloque A, Motor: copias de una serie con una sesión ausente o redondeada en IDX-CONC-001

| Campo | Valor |
| --- | --- |
| Estado | EN QA |
| Pieza | bloque_a (11_Ejecutor: `bloque_a/motor/frontera_b.py`, `motor/fichas_mon_idx.py`, `motor/fichas_p2.py`, `tests/test_t144.py`, `tests/test_t135_motor.py`, `tests/test_t127_hallazgos.py`, `tests/test_t127_r02.py`); `docs/incidencias.md` (INC-T128-01) |
| Planifica · implementa · QA | claude · claude · el otro agente o un revisor nuevo |
| Aprobación del operador | 2026-11-14: «quiero que por tu cuenta vayas completando los tickets que quedan abiertos»; las decisiones nuevas van como `[PROPUESTO]` |
| Deuda técnica | T-144 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` (esta copia no la toca) |

## Objetivo

Cerrar los hallazgos de la QA r01 de T-135 (`.docs/tickets/T-135/qa.md`) antes del modo sombra: que la amplitud de IDX-CONC-001 no sea la de un valor cuando la «otra» serie es la misma de otra fuente (una sesión ausente, redondeada, en otra unidad), sin tomar por copias series de verdad distintas y muy correladas.

## Alcance

- Entra: H-01 (media), H-02 a H-05 (bajas).
- No entra: cambiar el cálculo de la amplitud con copias (H-05 es decisión del operador: se documenta); el desfase de una sesión y los cambios de divisa variables (límites declarados); O-01 (`_params` sin claves declaradas, preexistente).

## Diseño

| Hallazgo | Corrección |
| --- | --- |
| H-01 (media): no se agrupa la misma serie con una sesión ausente o redondeada | Regla de **niveles** en `_etiquetas_series_copiadas`, además de la de rentabilidades: copias si, en las fechas comunes, log(pᵢ/pₖ) es una constante salvo el redondeo de cada serie. El paso de precio (`_paso_de_precio`: la mayor potencia de 10 de la que todos sus precios son múltiplos) da el error de redondeo de cada precio, qᵢ/2pᵢ; la cota del par es la suma de los dos más 2·`tolerancia_numerica_copias`, con tope log(1 + `tolerancia_clon`) |
| H-02 (baja): CHR-TOKEN sin aviso con la circulante movida | La firma del aviso vuelve a llevar total y máxima tal cual y una marca de lo que repite otro dato del mismo token (`repetidos`); lo repetido en los dos iguala y no informa |
| H-03 (baja): coste n²·T | Pares candidatos en tramos (`ELEMENTOS_POR_TRAMO`); un par sale cuando incumple las dos reglas |
| H-04 (baja): precios ≤ 0 aceptados | `ErrorFicha` con precios nulos, negativos o no finitos, por las dos vías |
| H-05 (baja): dos copias más otra serie | Coste declarado en INC-T128-01, sin cambiar el cálculo |

- Contratos y esquemas: no cambian (goldens de contratos coinciden).
- Números: `tolerancia_numerica_copias` = 1e-10 en `FRONTERA_B` (la de verificación de IDX-CONC-001, `FICHAS[…]["tol"]`; una prueba lo comprueba). `ELEMENTOS_POR_TRAMO` es de coste, no cambia el resultado (probado). Los cifras decimales que se prueban salen de `np.finfo(float).precision`.
- Falla cerrado: lo que no se distingue a la resolución de los datos se agrupa (la amplitud no se sirve); los precios inválidos se rechazan.

## Criterios de aceptación (binarios)

1. CA-1 (H-01): las vías de copia del revisor (una sesión ausente, GBX→GBP con 2 decimales, otra divisa a cambio fijo con 4, otro proveedor con 2 o 3 decimales) dan amplitud `null` sin identificadores; 0 copias en 100–300 semillas para índices con ρ ≈ 0,995 y precio frente a rentabilidad total (con y sin redondeo), y para fondos con error de seguimiento del 0,1 % y 0,01 %/año sin redondear.
2. CA-2 (H-02): CHR-TOKEN-001 con un token de oferta fija y una copia con la circulante −4 %, la total y la máxima +4 % o la máxima +4 % da el aviso, con y sin *staking*; dos tokens distintos de la misma oferta redonda, sin aviso.
3. CA-3 (H-03): el índice de 2000 valores con salida y exclusión sin fechas comunes en menos de 60 s; el tramo no cambia el resultado.
4. CA-4 (H-04): un precio 0, −1 o infinito se rechaza por `valores["precios"]` y por las series.
5. CA-5: `r01_01` y `r01_02` del revisor sin hallazgos; casos de control 67/67 sin aviso; mutantes del grupo T-144 de `.docs/tickets/T-147/mutantes.py` muertos; ruff ≤ 2838, mypy A ≤ 109.

## Plan de pruebas

| Prueba (`tests/test_t144.py`) | Tipo | Criterio |
| --- | --- | --- |
| `test_h01_la_misma_serie_de_otra_fuente_es_una_copia`, `test_h01_la_regla_de_niveles_a_mano`, `test_h01_paso_de_precio`, `test_h01_la_cota_no_es_mas_laxa…` | nominal, límite, regresión | CA-1 |
| `test_h01_series_distintas_muy_correladas_no_son_copias`, `…rentabilidades_sigue_viva`, `…desfase…` | falsos positivos, límite declarado | CA-1 |
| `test_h02_…` | regresión | CA-2 |
| `test_h03_…` | coste, determinismo | CA-3 |
| `test_h04_…` | fallo cerrado | CA-4 |
| `test_t135_motor.py::test_casos_de_control_no_cambian_ni_dan_aviso`, revisores, mutantes | regresión | CA-5 |

## Scripts

`.docs/tickets/T-135/revisores/r01_01_copias_idx_conc.py` y `r01_02_aviso_firmas.py` (del revisor); `.docs/tickets/T-147/mutantes.py --ticket T-144`.

## Registro

- 2026-11-15 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-15 · EN CURSO · claude · plan, implementación y pruebas en la copia `t147` (sin commit)
- 2026-11-15 · EN QA · claude · pendiente de QA por un agente que no implementó
