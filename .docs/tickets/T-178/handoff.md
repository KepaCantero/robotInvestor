# T-178 · Traspaso

Solo existe si el trabajo cambia de manos. Una sección por traspaso, la más reciente arriba.

## 2026-11-17 · de claude (implementador, r02) a QA (r02)

- **Fase en la que se entrega:** QA (r02), después del NO APTO de la r01.
- **Hecho:** los siete hallazgos están corregidos, cada uno con su prueba de regresión (tabla en `analisis-tecnico.md`, «Ronda r02»): H-01 (transacción), H-02 (`CERRADAS`), H-03 (fecha ISO), H-04 (tipos en lista cerrada), H-05, H-06 (`fin`) y H-07 (INC-T178-01). Hay 36 mutantes, todos muertos.
- **Cuidado con:**
  - H-05 se corrige de otra forma que la sugerida. La P3- cita solo los CAR- ya escritos, más `run_actual`, y no lleva una entrada de corrección. Con la sugerida, A5 del script de ataques falla al desempaquetar dos entradas P3-.
  - A3 del script no puede dar OK con la corrección de H-03: el rechazo sale fuera de su `try`. El script da 11 de 12 entradas; los rechazos de A3 y A3b los comprueba el `parametrize`.
- **Commit:** «wip local: T-178 r02», encima de `06bb04b`, sin push.

## 2026-11-17 · de claude (implementador) a QA (otro agente o un revisor nuevo)

- **Fase en la que se entrega:** QA (r01).
- **Hecho:**
  - PB-19: con un agente de instancia única saturado, HT-08 reordena su cola por prioridad (en el monitor y en el CAR-), el CAR- lleva el aviso de plazos al Coordinador si el agente está en el camino de la entrega (AG-01, AG-02, AG-18) y `carga.registrar_carga` eleva una P3- (PENDING_OPERATOR) si la saturación se repite en otro run, sin duplicarla mientras está abierta.
  - 17 pruebas nuevas en `tests/test_t178.py`; mapa y evidencias regenerados (PB-19 «Superada»). 27 mutantes propios, todos muertos (`mutantes.py`).
- **Falta:** la QA. Commit local, sin push.
- **Commit:** el «wip local: T-178» del worktree separado (ver `pruebas.md`).
- **Cuidado con:**
  - Las decisiones `[PROPUESTO]` de INC-T178-01: «si se repite» sin número (otro run, desde la última P3- de ese agente), qué agentes «afectan a plazos», la clave de orden y que el Coordinador lea de HA aunque la matriz no lo liste.
  - El ciclo no encola sus CT-05 en el monitor (no hay cola real de CT-05): la reordenación actúa sobre las órdenes registradas con `ordenes=`.
  - `orquestacion.py` solo cambia en un import y una línea (T-176 y T-177 trabajan en paralelo).
- **Scripts útiles:** `.docs/scripts/evidencias_plan_a.py --pb PB-19`; `.docs/tickets/T-178/mutantes.py`.
