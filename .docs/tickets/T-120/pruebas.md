# T-120 · Pruebas

| Suite | Antes | Después |
| --- | --- | --- |
| `tests/test_t120_r8_y_lecciones.py` | — | 16 superadas |

## Criterio de aceptación → prueba

| Criterio | Prueba |
| --- | --- |
| CA-1 | `test_el_iban_se_detecta_con_y_sin_separador_entre_grupos` (4) |
| CA-2 | `test_un_ct04_con_solo_un_iban_con_espacios_se_rechaza_y_no_queda_en_ningun_archivo` |
| CA-3 | `test_lo_que_no_es_un_iban_espanol_no_se_marca` (10) |
| CA-4 | `test_el_maximo_de_lecciones_sale_de_la_configuracion` |
| CA-5 | Suites de contratos, secretos y goldens; gate en el commit |

## Regresiones

`test_un_ct04_con_solo_un_iban_con_espacios…` falla sin la corrección: el mensaje se admite y el IBAN queda en F5.

## Gate

Lo pasa `commit_limpio.sh` al hacer el commit.
