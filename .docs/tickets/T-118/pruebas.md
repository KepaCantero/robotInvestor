# T-118 · Pruebas

Todo se ejecutó el 13-11-2026 en la copia de trabajo de la rama local `t118-trabajo`, con el `.venv` del repo. La máquina estaba compartida con otros tres trabajos (carga media de 6 a 7 en 4 núcleos), así que los tiempos son cotas superiores.

| Suite | Antes | Después |
| --- | --- | --- |
| `tests/test_t118_hallazgos.py` | — | 93 |
| Suite completa de A (`pytest -q tests`) | 3707 (las 3800 de ahora menos las 93 nuevas; no se volvió a ejecutar el árbol de partida) | **3800** en verde, 9 min 44 s |
| A-Forex y B | 68 y 176 | no se tocan ni se ejecutaron |

## Criterio de aceptación → prueba

| Criterio | Prueba | Resultado |
| --- | --- | --- |
| CA-1 (H-09) | `test_h09_*` (5): ML-PRED-001 por el Motor con el corte en 2008-12-31 y en 2020-08-09 (RECHAZADO «no conocible», una entrada en RC); con el corte en la última fecha, posterior o sin corte, se sirve. `conocible_desde` posterior al corte. Fecha de uso posterior al corte con variables conocidas antes. ML-CAL-001 con pares fechados. Fecha de corte ilegible | Sí |
| CA-2 (H-10) | `test_h10_*` (21): `test_h10_cota_de_los_datos_del_grupo_r` (17 cotas: en la cota se sirve, con uno más se rechaza), la cota sigue a la configuración, no se cambia desde la petición, y los dos casos del revisor por el Motor. Coste: `impl_costes_motor.py` | Sí. El más caro, 52 s |
| CA-3 (H-11) | `test_h11_*` (9) | Sí |
| CA-4 (H-12) | `test_h12_*` (7); INC-T118-01 | Sí |
| CA-5 (H-13) | `test_h13_*` (49) | Sí |
| CA-6 (H-14) | `test_h14_*` (2) | Sí |
| CA-7 (H-15) | `r02_07_semillas_ct10_config.py`: «casos de control de la Fase 2: 136», y AUD-REX-001 con 6 | Sí |
| CA-8 | Suite completa, cuotas, gates de árbol y mutantes (abajo) | Sí |

## Coste del servicio más caro que admiten las cotas (H-10)

Medido por `Motor.servir`, con sus dos pasadas, con `.docs/tickets/T-118/revisores/impl_costes_motor.py`. Cada petición lleva sus datos y sus parámetros de tamaño en el máximo.

| Petición | Tiempo |
| --- | --- |
| BT-VAR-001 generado, 2 520 rendimientos, ventana 250, Cornish-Fisher | 52,1 s |
| BT-PBO-001, S = 20, 1 000 configuraciones × 2 520 | 52,0 s |
| BT-VAR-001 generado, 2 520 rendimientos, ventana 250, histórico filtrado (el caso del hallazgo) | 18,1 s |
| RISK-VAR-001, distribución de 1 000 000, histórico filtrado | 17,2 s |
| BT-VAR-001 generado, ventana 500, EVT-POT | 8,8 s |
| DEC-VOI-001, 1 000 000 muestras | 3,7 s |
| ML-PRED-001, 2 520 × 20 variables, 20 pliegues, rejilla de 20, 10 000 réplicas | 3,0 s |
| BT-VAR-001 generado, ventana 250, t | 2,5 s |
| ML-CAL-001, 5 horizontes × 2 520, 10 000 réplicas | 2,1 s |
| SCN-H-001, 1 000 000 trayectorias, 2 520 rendimientos | 1,5 s |
| SIM-MC-001, bootstrap filtrado 10 000 × 2 520 | 0,8 s |

En una sola pasada del manejador, BT-VAR-001 generado con la historia de 2 520 es más barato cuanto más larga la ventana (menos ventanas): con Cornish-Fisher, de 26,8 s con ventana 250 a 6,8 s con 2 000. Por eso no hace falta acotar la ventana.

## Scripts del revisor (sin tocar)

`.venv/bin/python -I .docs/tickets/T-112/revisores/<script>`, desde la raíz de la copia. Importan el ejecutor de la copia.

| Script | QA r02 | Ahora | Nota |
| --- | --- | --- | --- |
| `r02_07_semillas_ct10_config.py` | 32/36 | **36/36** | Pasan las cuatro que fallaban: CT-10 tras cambiar el umbral E (H-11: SI), las dos de S (H-12) y el artefacto con un parámetro fuera de cota (H-14: NO, ERROR_REEJECUCION) |
| `r02_03_fecha_corte_y_cache.py` | 14/17 | 14/17 | ML-PRED-001 ya no figura entre las que sirven datos posteriores al corte (H-09). Los tres fallos que quedan no son hallazgos: los dos falsos positivos que el revisor declara y la observación de la caché |
| `r02_02_costes_y_tamanos.py C` | BT-VAR-001 con 100 000 rendimientos no termina en 300 s; BT-PBO-001 con 3 000 configuraciones, 118 s | **3/3** | Los dos, RECHAZADO en 0,1 s y 0,3 s. ML-PRED-001 con 50 y 300 variables, RECHAZADO. Lo admitido tarda como mucho 17,9 s |
| `r02_01_hostiles_anidados.py --rapido` | 706 `RecursionError` y 16 escapes en los campos | 6/7: **0 escapes** en 4 761 llamadas y en los campos de la petición | El fallo que queda son los «tipos raros servidos» de ACC-FACT-001 y FIR-SPREAD-001, que la QA declaró que no son hallazgo |
| `r02_01_hostiles_anidados.py` (completo) | 15 986 llamadas en unos 15 min | Interrumpido a los 14 min con 9 fichas hechas (5 010 llamadas), sin ningún escape | Con la máquina cargada iba tres o cuatro veces más lento. Lo corté y lancé la versión `--rapido` del mismo script |
| `r02_04_ct10_r01_con_corte_vigente.py` | 32/32 | 32/32 | Un artefacto con un umbral fijo en sus parámetros: NO y ERROR_REEJECUCION |
| `r02_08_r01_06_bloques_6_y_7.py` | 11/11 | 11/11 | |
| `r02_09_determinismo_y_minimos.py` | 42/42 | 42/42 | Los 136 casos de control, en dos procesos |
| `r02_05_oraculos.py` | 84/84 | 84/84 | |
| `r02_06_mutantes.py` | 27 muertos | no ejecutado | Sus mutantes deshacen correcciones de la r01 de T-112, no de este ticket |

## Regresiones

Cada corrección se deshizo en una copia desechable del ejecutor (`.docs/tickets/T-118/revisores/impl_mutantes.py`, que la borra al acabar): 51 mutantes, **51 muertos**.

| Hallazgo | Mutantes | Mueren ante |
| --- | --- | --- |
| H-09 | 5 (sin el corte en `fechas`, en `conocible_desde` o en ML-CAL-001; el día del corte rechazado; `_corte` que no lee) | `test_h09_*` |
| H-10 | 20 (cada cota quitada, una a una, y la cota fija en vez de la de la configuración) | `test_h10_*` |
| H-11 | 10 (no se guarda, no se usa, cada rama de la clasificación, cada forma de lectura sin apuntar) | `test_h11_*` |
| H-12 | 7 (cota fija en S y en P, la envoltura que no pasa la configuración) | `test_h12_*` |
| H-13 | 7 (sin la profundidad, `!=` en las semillas, sin el tipo de `clase` o de `perfil`, sin la segunda barrera, borde de la profundidad) | `test_h13_*` |
| H-14 | 2 (`ErrorFicha` vuelve a escapar; categoría ERROR_ORIGINAL) | `test_h14_*` |

Dos mutantes sobrevivieron a la primera pasada y cada uno llevó a una prueba nueva:
- M09a (sin el corte en `fechas`): en los casos de control `conocible_desde` es la misma lista que `fechas`, así que lo cazaba la otra comprobación. Prueba nueva con variables conocidas cinco sesiones antes.
- M11g (el registro no apunta las lecturas con `[]`): `parametro` consulta antes con `in`. Prueba nueva del registro, forma por forma.

## Pruebas de T-112 adaptadas

- `test_fase2_riesgo.py`: dos pruebas usaban 3 000 observaciones (EVT-POT frente a la verosimilitud perfil, y el IC del bootstrap de ML-CAL-001). Con la cota nueva usan 2 520. Sus comprobaciones y tolerancias no cambian.
- `test_t112_motor.py::test_r02_h04_h07_…`: comparaba la configuración que recibe la ficha con `is`; ahora con `==`.

## Gate

No se lanzó `./tools/check_all.sh` completo (indicación de quien encarga: la máquina está compartida). Por partes, desde la raíz de la copia:

| Comprobación | Resultado |
| --- | --- |
| `ruff check --output-format=concise bloque_a/11_Ejecutor bloque_a_forex/11_Ejecutor bloque_b/11_Ejecutor \| wc -l` | **2902** (cuota 2902) |
| `mypy --ignore-missing-imports --no-error-summary bloque_a/11_Ejecutor/bloque_a \| wc -l` | **109** (cuota 109) |
| `tools/corpus_integridad.py` | 695 archivos coinciden |
| `tools/refs_vivas.py` | todas las rutas existen |
| `tools/secrets_scan.py` | sin hallazgos |
| `tools/nfc_check.py` | todos en forma canónica |
| Suite completa de A | 3800 passed (línea base 607) |

## Comandos

```bash
cd bloque_a/11_Ejecutor
../../.venv/bin/pytest -q tests/test_t118_hallazgos.py
../../.venv/bin/python -m pytest -q -p no:cacheprovider tests
../../.venv/bin/python ../../.docs/tickets/T-118/revisores/impl_costes_motor.py
cd ../..
.venv/bin/python -I .docs/tickets/T-112/revisores/r02_07_semillas_ct10_config.py
.venv/bin/python -I .docs/tickets/T-112/revisores/r02_03_fecha_corte_y_cache.py
(ulimit -v 8000000; .venv/bin/python -I .docs/tickets/T-112/revisores/r02_02_costes_y_tamanos.py C)
(ulimit -v 8000000; .venv/bin/python -I .docs/tickets/T-112/revisores/r02_01_hostiles_anidados.py --rapido)
.venv/bin/python .docs/tickets/T-118/revisores/impl_mutantes.py "$PWD" /tmp/t118_mut
.venv/bin/ruff check --output-format=concise bloque_a/11_Ejecutor bloque_a_forex/11_Ejecutor bloque_b/11_Ejecutor | wc -l
.venv/bin/mypy --ignore-missing-imports --no-error-summary bloque_a/11_Ejecutor/bloque_a | wc -l
for t in corpus_integridad refs_vivas secrets_scan nfc_check; do .venv/bin/python tools/$t.py; done
```
