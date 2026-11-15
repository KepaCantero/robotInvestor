# T-149 · Traspaso

Solo existe si el trabajo cambia de manos. Una sección por traspaso, la más reciente arriba.

## 2026-11-15 · de claude a la QA (el otro agente o un revisor nuevo)

- **Fase en la que se entrega:** QA.
- **Hecho:** los cinco hallazgos de las QA r01 de T-144 y T-147 y la pregunta O-01 (README, `analisis-tecnico.md`, `pruebas.md`).
- **Falta:** la QA r01. La fila de T-149 en la deuda técnica la pone la sesión coordinadora.
- **Commit:** local, «wip local: T-149» en la copia `t149` (sin push).
- **Cuidado con:** los scripts de mutantes del revisor buscan textos exactos de `frontera_b.py`, `cadena_b.py`, `cadena_a_b.py` y `descargar_datos_bce.py`: se conservaron. Las pruebas que matan Q02–Q10 están en `test_t144.py` y `test_t147.py` (los ficheros que fija `r01_03_mutantes_qa.py`), no en `test_t149.py`. La ronda T-144 de la regla de copias está en INC-T127-01 (aunque su texto cite INC-T128-01); la T-149 va detrás. G3: no es `[PROPUESTO]`, sale del Documento 0 (7.3 y CT-02).
- **Scripts útiles:** `.docs/tickets/T-149/medir_copias.py` (falsos positivos con 300 semillas; `--modulo` para comparar con otra versión de `frontera_b.py`), los revisores de T-144 y T-147 y `.docs/tickets/T-147/mutantes.py`.
