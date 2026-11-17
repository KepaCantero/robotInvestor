# T-168 · Pruebas

Desde `bloque_a/11_Ejecutor`, sin red ni coste:

| Orden | Resultado |
| --- | --- |
| `pytest -q tests/test_t102_filtro.py -k tiempo_lineal --durations=4` | 4 passed; la más lenta, 0,97 s (carga ≈ 1) |
| `-k tiempo_lineal` con 8 quemadores extra (carga 10,6–13) | 4 passed; reloj de `r05_h37` 4,40 s, CPU < 1 s (CA-2; QA r01, `revisores/r01_01`) |
| Mutantes de retroceso Q1–Q4 de la QA r01 (`revisores/r01_02`) | Los cuatro caen; Q5–Q6 son el límite declarado de H-01 (CA-3) |
| ruff, desde la raíz | 2813 (cuota 2813) |
