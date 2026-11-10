# T-90 · Pruebas

| Suite | Antes | Después |
| --- | --- | --- |
| `pytest -q bloque_b/11_Ejecutor` | 174 | 176 (`tests/test_t90_nota_fuera_de_corte.py`, dos pruebas) |

## Criterio de aceptación → prueba

| Criterio | Prueba |
| --- | --- |
| CA-1 | `test_nota_posterior_al_corte_se_excluye_y_se_declara`: la nota no está en F2 ni en el paquete y `estados_degradados` la declara con su recuento |
| CA-2 | Las dos pruebas fallan con el código anterior a T-90 (`estados_degradados` vacío); la QA r01 pasó la suite de B (175) y el gate 12/12 sobre una copia limpia |

## Regresiones

- **QA r01, H-01 y H-02:** `test_fechas_incompletas_no_se_rotulan_como_fuga_y_se_cuentan`. Dos notas del mismo especialista con fechas incompletas quedan como «2 nota(s) … fechas de fuente incompletas, ilegibles o incoherentes», sin la palabra fuga.

## Gate

Se pasa el gate completo (`.docs/scripts/gate.sh` con la opción `--completo`) antes del commit, a través de `.docs/scripts/commit.sh`.
