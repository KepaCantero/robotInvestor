---
id: compartida/2026-11-10_bloque-a-terminado
autor: claude
fecha: 2026-11-10
tipo: estado
etiquetas: [bloque_a, T-53, T-66]
fuente: .docs/tickets/T-66/
vigencia: vigente
---

Sustituye a `compartida/2026-11-09_revision-bloque-a`.

**Estado del Bloque A tras T-66 (10-11-2026).** El Bloque A se da por terminado en revisión. Tiene 181 pruebas y QA en curso.

**Lo que tiene que saber quien trabaje con A:**
- **Perfiles activos.** Por defecto solo se analiza divisas (`perfiles.activos`). Las pruebas activan los 12 tipos con `config_pruebas()` de `tests/conftest.py`. Una prueba que use `cargar_config()` sin más analiza solo DIV.
- **Objeciones fuertes.** No las resuelve el Analista: hace falta que cite evidencia verificable y que el Contradictor lo confirme en una contrarréplica (CT-13, fase `CONTRARREPLICA`).
- **Certificados.** Con `aprendizaje.solo_endurecer`, nacen PROPUESTO y se aprueban por CT-04 (`aprobar_certificados`). Para certificar hay que tener `n_eff ≥ 100` con fechas distintas, no 100 pronósticos de la misma fecha.
- **Backtests con un modelo real.** Antes de `backtest.fecha_corte_modelo`, sus pronósticos llevan `contaminacion_posible` y no enseñan nada al Evaluador.
- **Lo aplazado,** con su destino, en la fila T-67 de la deuda técnica.
