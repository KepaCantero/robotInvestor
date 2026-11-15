# T-124 · Pruebas

| Comprobación | Resultado |
| --- | --- |
| `r02_01_mutantes_mensajeria_nuevos.py --confirmar` (revisor de T-114) | 20 de 20 detectados, ninguno vivo (antes, siete vivos) |
| `r02_02_formas_y_flujos.py --copia` | K01, K02 y K03 detectados |
| `python tests/goldens_ct.py` | coinciden |
| `tests/test_fase3_goldens.py` | en verde |
| QA r01 (`r01_01_que_cambia_el_recongelado.py`) | el re-congelado solo cambia lo que dice su motivo |

Rellenado en T-130 (QA r01 de T-124, H-01).
