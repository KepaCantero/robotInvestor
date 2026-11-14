# T-118 · Traspaso

Solo existe si el trabajo cambia de manos. Una sección por traspaso, la más reciente arriba.

## 2026-11-13 · de claude (implementación) a quien haga la QA

- **Fase en la que se entrega:** implementar y probar, hechas. Falta la QA.
- **Hecho:** H-09 a H-15 de la QA r02 de T-112 corregidos, cada uno con su prueba de regresión (`tests/test_t118_hallazgos.py`, 93 pruebas) y su mutante (51, todos muertos). Decisiones en INC-T118-01 (`docs/incidencias.md`).
- **Falta:**
  - la QA independiente;
  - fusionar la rama local `t118-trabajo` en `develop` (no hay `git push`) y pasar el gate completo en el árbol fusionado;
  - la fila de T-118 en la deuda técnica, el diario y la memoria, que lleva quien encarga.
- **Commit:** los de la rama local `t118-trabajo`, salida de `ab95d41`.
- **Cuidado con:**
  - `fichas_riesgo.py`, `fichas_series.py`, `fichas_reales.py` y `servicio.py` los toca también el trabajo que añade las fichas P2. Los cambios de T-118 son localizados: las cotas de R van en un bloque aparte detrás de `UMBRALES`;
  - tres pruebas de T-112 se adaptaron (`pruebas.md`, «Pruebas de T-112 adaptadas»);
  - el artefacto del RC tiene un campo nuevo (`configuracion_usada`) y la re-ejecución otro (`configuracion`), que el esquema congelado del Registro V2.0 no lista (INC-T118-01);
  - `r02_01_hostiles_anidados.py` completo no llegó a terminar con la máquina cargada: se ejecutó entero en su modo `--rapido`. Conviene repetirlo completo en la QA;
  - no se ejecutó `./tools/check_all.sh` completo, solo sus partes (`pruebas.md`, «Gate»).
- **Scripts útiles:** `.docs/tickets/T-118/revisores/impl_mutantes.py` e `impl_costes_motor.py`; los `r02_*` de `.docs/tickets/T-112/revisores/`.
