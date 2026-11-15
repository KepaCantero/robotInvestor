# T-150 · Traspaso

Solo existe si el trabajo cambia de manos. Una sección por traspaso, la más reciente arriba.

## 2026-11-15 · de claude a la QA (el otro agente o un revisor nuevo)

- **Fase en la que se entrega:** QA.
- **Hecho:** H-01 a H-06 y las observaciones O-01, O-04, O-05 y O-06 de la QA r01 de T-149 (README, `analisis-tecnico.md`, `pruebas.md`).
- **Falta:** la QA r01. La fila de T-150 en la deuda técnica la lleva la sesión coordinadora.
- **Commit:** local, «wip local: T-150» en la copia `t150` (sin push).
- **Cuidado con:** H-05 se corrigió, no se declaró: la regla de niveles prueba cada serie redondeada y truncada (cuatro combinaciones por par, `_pares_por_hipotesis`); el desplazamiento es por precio y solo donde q/p ≤ `tolerancia_clon` (por serie, o en todos los precios, se pierden copias o se gana un falso positivo: hay una prueba de cada). La prueba de borde de T-149 en `test_t144.py` toma ahora el menor hueco de las cuatro combinaciones (con la hipótesis truncada, el par «justo fuera» caía dentro por un 0,6 %): sigue matando Q08 y Q09. Las pruebas de N21 y N27 están en `test_t149.py` (el fichero que fija el script de mutantes del revisor). Las líneas que mutan los scripts de T-147 y T-149 se conservaron. En R1 del revisor queda el OBS de O-03 (límite del detector).
- **Scripts útiles:** `.docs/tickets/T-150/medir_truncado.py` y `.docs/tickets/T-149/medir_copias.py` (con `--modulo` para comparar con `git show HEAD:bloque_a/11_Ejecutor/bloque_a/motor/frontera_b.py`), `.docs/tickets/T-150/mutantes.py`, los revisores de T-149 y `.docs/tickets/T-147/mutantes.py`.
