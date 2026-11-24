# T-194 · Traspaso

## 2026-11-24 · de claude (implementador, r02) a QA (r02, el mismo revisor)

- **Fase en la que se entrega:** QA r02, después del NO APTO de la r01.
- **Hecho:**
  - Los siete hallazgos están corregidos, cada uno con su prueba de regresión (tabla en `pruebas.md`): H-01 (`unset COLA_ASTRA_SCRIPT`), H-02 y H-03 (pruebas nuevas), H-04 (ruff a 0), H-05 (documentación), H-06 (cola propia en `pruebas_autor_generico.py`) y H-07 (`core.quotePath=false` en `cola_astra.py`).
  - 50 pruebas en `pruebas_cola_astra.py`, línea base 399.
  - 49 mutantes muertos, con R01, R02, R03, R04, R06 y R09 del revisor como M43 a M47 y M49, y M48 para H-07.
  - `revisores/` en verde.
- **Cuidado con:**
  - R03 no estaba en la lista de hallazgos. Su prueba está aquí para que `r01_mutantes_revisor.py` salga en verde.
  - `r01_aislamiento.sh` exige que `cola_astra.py` no tenga cambios sin commit (`git diff --quiet`): hay que ejecutarlo sobre el commit.
- **Commit:** «T-194 r02: …», en `wip/t194`, sin push.

## 2026-11-24 · de claude (implementador, r01b) a QA

- Corrige INC-T194-01 con `--untracked-files=all`, autorizado por el coordinador. La prueba deja de ser `xfail`, la línea base queda en 390 y M42 muere (42 de 42). Commit `4a3fd27`.

## 2026-11-24 · de claude (implementador) a QA (histórico, r01)

- **Fase en la que se entrega:** QA (r01).
- **Hecho:**
  - `pruebas_cola_astra.py` pasa a pytest, con un repositorio y una cola de prueba propios.
  - Tiene 41 pruebas: las 13 comprobaciones de antes, sus límites y cuatro del autor genérico en el script entero.
  - Línea base de 349 a 389. 41 mutantes, todos muertos.
- **Cuidado con:**
  - INC-T194-01: un entregable nuevo en una carpeta nueva sin añadir no avisa. `cola_astra.py` no se cambió (encargo). La prueba es `xfail(strict=True)`.
  - Las pruebas de EN CURSO dependen de `date.today()`.
- **Commit:** local, en la rama `wip/t194`, sin push.
- **Scripts útiles:** `.docs/scripts/pruebas_scripts.sh` y `.docs/tickets/T-194/mutantes.py`.
