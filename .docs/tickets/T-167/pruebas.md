# T-167 · Pruebas

| Orden | Resultado |
| --- | --- |
| `pytest -q tests/test_t167_version.py` | 2 passed |
| Las mismas pruebas con `version = "1.1.0"` en el pyproject | fallan (comprobado a mano antes del cambio: el pyproject decía 1.1.0 y el README V1.2) |
| `ruff check tests/test_t167_version.py` | sin avisos |
| Mutantes de la QA r01 (`revisores/r01_01_mutantes_version.py`) | 10/10 caen (pyproject o `__init__` a 1.1.0, los dos a 1.1.0, README V1.1/V1.3/sin versión, 1.2.1, "1.2", espacio final, 2.0.0); el control coherente (los tres a 1.3) pasa (CA-2) |
| Gates ligeros (corpus 696, NFC, secretos, refs vivas, YAML), ruff y mypy | en verde; ruff 2813 y mypy A 109, iguales a la cuota (CA-4; QA r01) |
