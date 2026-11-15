# T-126 · Pruebas

| Suite | Resultado |
| --- | --- |
| `test_t126_pb26_pb48.py` | 13 superadas |
| ruff | 2902 |

Gate completo: lo pasa `commit_limpio.sh` al hacer el commit.

## Ronda r02 (15-11-2026)

| Suite | Antes | Después |
| --- | --- | --- |
| `test_t126_pb26_pb48.py` | 13 | 13 (sin cambios) |
| `test_t126_r02.py` (nueva) | — | 11 |
| Vecinas (con las de T-125 y T-116) | — | en verde (ver `T-125/pruebas.md`, ronda r02) |
| ruff · mypy A | 2902 · 109 | 2902 · 109 |

| Hallazgo | Pruebas (`test_t126_r02.py`) |
| --- | --- |
| H-01 | `test_h01_en_el_ciclo_una_opcion_en_banda_marginal_se_resuelve_con_su_segunda_pasada`, `test_h01_sin_la_segunda_pasada_esas_opciones_no_serian_elegibles` |
| H-02 | `test_h02_cada_referencia_esta_fisicamente_en_la_seccion_de_su_tematica` (F7, F8, F9), `test_h02_a_igualdad_de_q_va_primero_la_mas_reciente` (F7, F8, F9), `test_h02_el_caso_dudoso_es_un_documento_sin_anio` |
| H-03 | `test_h03_las_comprobaciones_detectan_fichas_estropeadas` |
| H-04 | `test_h04_la_leccion_que_relaja_el_control_llega_al_analista_en_su_ct06` |

### Script del revisor (`revisores/r01_01_mutantes_y_ataques.py`)

| Mutante | r01 (tal cual) | r02 tal cual (solo `test_t126_pb26_pb48.py`) | r02 con `test_t126_r02.py` |
| --- | --- | --- | --- |
| J1, J2, J3, J6 | MUERTO | MUERTO | MUERTO |
| J4 | VIVO | VIVO | **MUERTO** |
| J5 | VIVO | VIVO | **MUERTO** |

El ataque A1 del script mira el ciclo de `test_pb48_una_guia_…` (sin la segunda pasada completa del Analista) y da lo mismo que en la r01 (3 en banda marginal sin resolver); el ciclo de H-01 es el de `test_t126_r02.py`, con el Analista haciendo la segunda pasada.

Comandos: desde `bloque_a/11_Ejecutor`, `python -m pytest -q tests/test_t126_pb26_pb48.py tests/test_t126_r02.py`; desde la raíz, `python .docs/scripts/mutantes_revisor_ampliado.py .docs/tickets/T-126/revisores/r01_01_mutantes_y_ataques.py <copia con «_mut»>/bloque_a tests/test_t126_r02.py`. Gate completo y suite entera: no ejecutados (encargo).
