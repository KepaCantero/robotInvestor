# T-106 · Pruebas

| Suite | Antes | Después |
| --- | --- | --- |
| `test_fase1_mon_idx.py` | — | 118 |
| `test_fase1_fon_der.py` | — | 122 |
| `test_fase1_tcv.py` | — | 101 |
| `test_t106_motor.py` | — | 27 |
| Pruebas del Motor existentes (`test_unitarias`, `test_t65_resto_t53`, `test_t87_contratos`, `test_t92_revision`) | en verde | en verde (491 con las nuevas) |

Casos de control: 53 en 21 fichas, todos superados (`promover_fichas_catalogo.py`; salida en `analisis-tecnico.md`).

Cuotas: ruff 2938 → 2908 (correcciones seguras en `servicio.py`), mypy de A 109.

## Gate

`./tools/check_all.sh` completo con `commit_limpio.sh`, con el corpus re-congelado en el mismo commit.
