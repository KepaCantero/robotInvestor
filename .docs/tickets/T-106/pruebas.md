# T-106 · Pruebas

| Suite | Antes | Después |
| --- | --- | --- |
| `test_fase1_mon_idx.py` | — | 118 |
| `test_fase1_fon_der.py` | — | 122 |
| `test_fase1_tcv.py` | — | 101 |
| `test_t106_motor.py` | — | 27 |
| Pruebas del Motor existentes (`test_unitarias`, `test_t65_resto_t53`, `test_t87_contratos`, `test_t92_revision`) | en verde | en verde (491 con las nuevas) |

Casos de control: 66 en 21 fichas desde la r02 (en la r01 eran 50), todos superados (`promover_fichas_catalogo.py`; salida en `analisis-tecnico.md`).

Cuotas: ruff 2938 → 2908 (correcciones seguras en `servicio.py`), mypy de A 109.

## Gate

`./tools/check_all.sh` completo con `commit_limpio.sh`, con el corpus re-congelado en el mismo commit.

## Ronda r02

| Suite | r01 | r02 |
| --- | --- | --- |
| `test_fase1_mon_idx.py` | 118 | 199 |
| `test_fase1_fon_der.py` | 122 | 181 |
| `test_fase1_tcv.py` | 101 | 150 |
| `test_t106_motor.py` | 27 | 32 |
| Casos de control | 50 | 66, todos superados |

Scripts de la QA r01 en el árbol de la r02:
- `r01_01_ataques_datos.py <raíz> --max 60`: 129/129, sin excepciones ajenas a `ErrorFicha` ni cifras no finitas;
- `r01_06_ataques_dirigidos.py`: 5/5;
- `r01_04` (mutantes de las fichas afectadas): mueren ante los casos de control y las pruebas, según los agentes. M38 no se aplica porque cambió el texto de `_forward` (lo caza «5y5y coherente…»).
- `r01_02` ahora se corta con un `ErrorFicha` en la curva redondeada de MON-EXP: es el rechazo que se busca.

Cuotas: ruff 2908 y mypy de A 109, sin cambios.

## Ronda r03

| Suite | r02 | r03 |
| --- | --- | --- |
| `test_t106_r03.py` | — | 45 (H-14, H-15, H-16, H-18 y H-20) |
| Pruebas del Motor Fase 1 (`test_fase1_*`, `test_t106_*`) | 562 | 607 |

Scripts de la QA r02 en el árbol de la r03:
- `r02_03_ataques.py`: 27/29. Los dos «fallos» son el comportamiento que pide H-14: subir `nodos_min` de MON-EXP o `anios_min` de MON-REAL se rechaza porque son umbrales fijos de la ficha. Las ocho peticiones mal formadas de H-15 quedan RECHAZADO en RC, y el caso de H-16 sale SERVED_WITH_LIMITATIONS con «hasta 93,6 puntos»;
- `r02_04_mutantes.py`, con `tests/test_t106_r03.py` añadido a las pruebas de cada familia y del Motor (en una copia del script, fuera del repo, porque el script del revisor no se toca): 0 mutantes vivos frente a casos de control y pruebas a la vez (antes, 13).

Cuotas: ruff 2908 y mypy de A 109, sin cambios.
