# T-141 · Pruebas

| Prueba u orden | Resultado |
| --- | --- |
| `tests/test_t141_datos_bce.py` | 4 passed (encontró que un tipo cero daba un cruce infinito; corregido) |
| `descargar_datos_bce.py <carpeta>` | 6 series, 3 039 cierres cada una, 2015-01-02 → 2026-11-13 |
| `comprobar_datos_a.py <carpeta> --clases DIV --as-of 2026-11-13` | 6 de 6 OK (también en H1 el 15-11) |
| `bloque-a --cliente mock --datos <carpeta> --as-of 2026-11-13 ciclo` | COMPLETO · ENTREGADA · G3 APTO |
