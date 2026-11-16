# T-168 · Pruebas

Desde `bloque_a/11_Ejecutor`, sin red ni coste:

| Orden | Resultado |
| --- | --- |
| `pytest -q tests/test_t102_filtro.py -k tiempo_lineal --durations=4` | 4 passed; la más lenta, 0,97 s (carga ≈ 1) |
| ruff, desde la raíz | 2813 (cuota 2813) |
