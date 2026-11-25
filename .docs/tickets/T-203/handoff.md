# T-203 · Traspaso

Solo existe si el trabajo cambia de manos. Una sección por traspaso, la más reciente arriba.

## 2026-11-25 · de claude (implementador, ronda de cierre) al revisor de la r01

- **Fase en la que se entrega:** ronda de cierre de la QA r01 (APTO pendiente de H-01 y H-02).
- **Hecho:**
  - Rebasado sobre develop con T-201 (358576c3), como decidió el coordinador. Envoltorios HT-02/03/07: los de T-201, sin cambios (H-02 se cierra solo). `operaciones.py`: `def posicion_historica(valor: float, historia: Sequence[float] | np.ndarray) -> dict:`. `tools/cuotas.txt`: `ruff=2735` (el gate, desde 2797) y `mypy_bloque_a=67`.
  - `test_reexportacion_de_referencia_sin_cambios` espera también `TYPE_CHECKING`.
  - H-01: el solape real con T-201 (`ht02.py`, `ht03.py`, `ht07.py` y `operaciones.py` antes del rebase; tras él, `operaciones.py`, `tools/cuotas.txt` y la deuda técnica) está escrito en los seis sitios; CA-2 rehecho con `ca2_solapes.sh`.
  - `cierre_r01_04.sh` (tu `r01_04` adaptado a T-201 integrado), la equivalencia contra el develop nuevo y el gate completo, cada uno con su log (rutas en `pruebas.md`).
- **Falta:** comprobar la ronda de cierre. Commit local «T-203 cierre: …» en `wip/t203`, sin push.
- **Cuidado con:** T-204 (retira el Bloque A Forex) comparte `tools/cuotas.txt` y la deuda técnica; si entra antes, la cuota de ruff se recalcula con el gate al integrar.

## 2026-11-24 · de claude (implementador) a QA (otro agente o un revisor nuevo)

- **Fase en la que se entrega:** QA (r01).
- **Hecho:** ruff 2806 → 2735 (−71) con UP006, UP045, UP035, I001, F401 y RUF100 en cinco módulos del paquete (`motor/operaciones.py`, `mock_respuestas.py`, `herramientas/ht02.py`, `ht03.py`, `ht07.py`) y diez ficheros de pruebas; `tools/cuotas.txt` en `ruff=2735`; mypy sin cambios (A 102, los mismos avisos; A-Forex 174; B 159). Salidas del ejecutor idénticas a develop (`equivalencia.py`: IGUALES). Cinco pruebas nuevas en `tests/test_t203_cuotas.py`.
- **Falta:** la QA. Commit local en `wip/t203`, sin push.
- **Cuidado con:**
  - Medir con la orden del gate (configuración por defecto de ruff, sin `--select`) y filtrar por código. Con `--select`, RUF100 da por sin uso los `# noqa: BLE001`, que con el gate sí se usan.
  - El único cambio que no es una sustitución literal es el orden de imports de HT-02, HT-03 y HT-07 (ver `analisis-tecnico.md`).
  - `herramientas/referencia/ht07_legibilidad.py` se dejó fuera aposta: es copia literal del corpus y una prueba lo exige igual byte a byte. Lo mismo pasa con las otras tres copias de `referencia/`. (Corrección de la ronda de cierre, H-01: T-201 no era esas tres copias sino `ht02.py`, `ht03.py`, `ht07.py` y `operaciones.py`, que T-203 también cambiaba.)
  - La lista de exclusión se sacó de `git diff --name-only` contra `origin/astra/encargos-bloque-a-c38-c47` y `wip/t196` el 24-11-2026; si esas ramas cambian antes de integrar, conviene repetirla.
- **Scripts útiles:** `.docs/tickets/T-203/equivalencia.py <copia de develop> <copia del ticket> <carpeta de trabajo>` (unos 3 minutos).
