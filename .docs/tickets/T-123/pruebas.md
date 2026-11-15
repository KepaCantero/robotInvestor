# T-123 · Pruebas

## Suites

| Suite | Antes (r01) | Después (r02) |
| --- | --- | --- |
| `tests/test_t123_r8_iban_y_tarjetas.py` | 70 | 70 |
| `tests/test_t123_r02.py` | — | 22 |
| Vecinas de R8 (`test_t120_r8_y_lecciones.py`, `test_t122_hallazgos.py`) | en verde | en verde (una expectativa movida: tres separadores ahora se detectan) |

Las cuatro juntas, desde `bloque_a/11_Ejecutor`: `python -m pytest -q tests/test_t123_r02.py tests/test_t123_r8_iban_y_tarjetas.py tests/test_t120_r8_y_lecciones.py tests/test_t122_hallazgos.py` → 154 passed.

## Criterio → prueba

| Criterio | Prueba |
| --- | --- |
| CA-1 IBAN de ocho países | `test_t123_r8_iban_y_tarjetas.py` (IBAN por país y forma) y `test_t123_r02.py::test_h01_iban_*` |
| CA-2 tarjetas de cinco redes, enmascaradas | `test_t123_r8_iban_y_tarjetas.py` y `test_t123_r02.py::test_h01_tarjeta_*` |
| CA-3 sin falsos positivos | `test_t123_r8_iban_y_tarjetas.py` (series corrientes y 20 000 al azar) y `test_t123_r02.py::test_h02_*`, `test_h04_*`, `test_r02_decimales_*` |
| CA-4 CT-04 rechazado sin dejar el dato | `test_t123_r8_iban_y_tarjetas.py` (CT-04) y el script del revisor `r01_02_caminos_r8.py` (30/30) |
| CA-5 goldens, ciclo y gate | `tests/goldens_ct.py` «coinciden»; la suite completa y el gate 12/12, en el commit con `commit_limpio.sh` |

## Scripts del revisor (r01) contra la r02

- `r01_01_banco_iban_tarjetas.py`: 10/11. Lo que queda en rojo son 90 de 5 000 series de cuatro grupos de cuatro cifras al azar, que tienen la forma de una tarjeta: límite declarado en INC-T123-01. Diners y Maestro y el formato con puntos siguen sin detectarse, como en la r01 (no están entre las redes y formas declaradas).
- `r01_02_caminos_r8.py`: 30/30.
- `r01_03_efecto_en_ct04.py`: el bloque a pasa entero (caducidad, CVV e IBAN seguido de cifra, rechazados sin dejar el dato); el bloque b se para con `StopIteration` porque ya no encuentra, entre 100 000 huellas, ninguna que se marque como tarjeta, que es lo que pedía H-02.
