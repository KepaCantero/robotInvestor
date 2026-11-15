# T-144 · QA independiente

- **Revisor:** revisor nuevo sin contexto de la implementación (subagente de Claude; implementó Claude) · **Ronda:** r01 · 2026-11-15
- **Copia:** git worktree en el scratchpad con HEAD `f197bc5` y `.venv` enlazado. Sin red ni coste. Opinión formada con el README, el diff de HEAD (`frontera_b.py`, `fichas_mon_idx.py`, `fichas_p2.py`) y el código antes de leer `analisis-tecnico.md`.

## Reproducción desde limpio

| Comprobación | Resultado |
| --- | --- |
| Suite completa de A, una vez (`cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q -p no:cacheprovider`) | **6338 passed** en 24 min 8 s; exit 0 (incluye `test_t135_motor.py::test_casos_de_control_no_cambian_ni_dan_aviso`, `test_t127_*`) |
| `pytest -q tests/test_t144.py …` (con los de T-147 y T-148) | 218 passed en 29 s (la de n = 2000 incluida) |
| `goldens_ct.py` · `test_fase3_goldens.py` | coinciden · 102 passed |
| ruff · mypy de A | 2838 (cuota 2838) · 109 (cuota 109) |
| gates ligeros (`refs_vivas`, `secrets_scan`, `nfc_check`, `corpus_integridad`) | en verde |
| `python -I .docs/tickets/T-135/revisores/r01_01_copias_idx_conc.py bloque_a/11_Ejecutor` | **39 ok · 0 hallazgos**; n = 1000, 10 años, con salida y exclusión: 1,0 s |
| `python -I .docs/tickets/T-135/revisores/r01_02_aviso_firmas.py bloque_a/11_Ejecutor` | **24 ok · 0 hallazgos** |
| `.docs/tickets/T-147/mutantes.py <copia «t147_mut»>` | grupo T-144: **8 de 8 muertos** (M17–M24) |

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 | sí | `test_h01_*` en verde (las siete vías y 100 semillas de series distintas); `T-135/r01_01` sin hallazgos; `r01_01` (este) B: 0 de 100 pares de índices con ρ ≈ 0,995 redondeados a una rejilla de 0,05 se agrupan. Fuera de las vías del criterio quedan copias que no se agrupan (H-01) |
| CA-2 | sí | `test_h02_*`; `T-135/r01_02` 24 ok |
| CA-3 | sí | `test_h03_*` (n = 2000) dentro de la suite; `T-135/r01_01`: n = 1000 en 1,0 s |
| CA-4 | sí | `test_h04_*`; `r01_01` C: 0, −1, +∞ y −∞ rechazados con `ErrorFicha` |
| CA-5 | sí | revisores de T-135 sin hallazgos; casos de control en la suite completa; M17–M24 muertos; cuotas |

## Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | media | `.venv/bin/python -I .docs/tickets/T-144/revisores/r01_01_copias_otras_rejillas.py` (casos A) | Esperado (objetivo del ticket): la misma serie «de otra fuente… redondeada» se agrupa y la amplitud no se sirve. Obtenido: una copia redondeada a una rejilla que no es una potencia de 10 (pasos de 0,05 o 0,25, octavos, treintaidosavos) **no** se agrupa y IDX-CONC-001 sirve la amplitud de un solo valor; tampoco una copia a 2 decimales con un solo precio sin redondear. Causa: `_paso_de_precio` toma la mayor potencia de 10 de la que son múltiplos **todos** los precios; los múltiplos de 0,05 lo son de 0,01, así que el error de redondeo supuesto (0,005) es la quinta parte del real (0,025), y un único precio sin redondear lleva el paso al de la coma flotante. Las siete vías del CA-1 sí se agrupan | Admitir rejillas k·10⁻ᵈ con k ∈ {1, 2, 5, 25, 1/8…} (o estimar el paso por el máximo común divisor aproximado de las diferencias de precio) y calcularlo de forma robusta (que una minoría de precios fuera de la rejilla no lo hunda); pruebas con 0,05, 1/8 y un precio suelto; declararlo en INC-T128-01 si no se corrige | abierto |
| H-02 | baja | `.venv/bin/python .docs/tickets/T-147/revisores/r01_03_mutantes_qa.py <copia «t147_mut»> --ticket T-144` | Mutantes propios: Q11 (precio 0 aceptado) muere; viven Q08 (cota de redondeo sin `tolerancia_numerica_copias`), Q09 (error de redondeo q/p en vez de q/2p: la cota del doble de laxa) y Q10 (`lo > hi` → `lo >= hi`). Las pruebas no fijan la anchura de la cota de la regla de niveles: una cota el doble de laxa (más falsos «copias», falla cerrado pero sin amplitud en índices de verdad) pasa toda la batería | Una prueba que fije la cota a mano en el borde (un par justo dentro y otro justo fuera de bᵢ + bₖ + 2·tol) | abierto |

Invariantes comprobados: sin LLM en la ruta (código determinista del Motor); los números nuevos salen de `FRONTERA_B` (`tolerancia_numerica_copias` = la `tol` de la ficha, con prueba) y `ELEMENTOS_POR_TRAMO` solo cambia el coste; lo que no se distingue se agrupa (falla cerrado); el orden de las series no cambia el resultado (`r01_01` C).

Scripts de esta ronda: `revisores/r01_01_copias_otras_rejillas.py` y, para los mutantes, `.docs/tickets/T-147/revisores/r01_03_mutantes_qa.py`.

## Veredicto

**APTO** · los cinco criterios se cumplen con evidencia y no hay hallazgos altos. H-01 (media) no rompe el CA-1, que enumera las vías y todas se agrupan, pero deja otra vía de la misma revelación que el objetivo quería cerrar: ticket nuevo. H-02 (baja), al mismo ticket.
