# T-176 · Traspaso

Solo existe si el trabajo cambia de manos. Una sección por traspaso, la más reciente arriba.

## 2026-11-18 · de claude a la QA (cierre de la r02)

- **Hecho:** H-07: `recalibrar` en una transacción del almacén (`_recalibrar`), con su regresión y el mutante M38. r01_ataques 17/17, r02_ataques 7/7.
- **Falta:** el cierre de la QA r02.

## 2026-11-17 · de claude a la QA r02

- **Fase en la que se entrega:** QA (r02).
- **Hecho:** H-01 a H-06 de la QA r01 corregidos con la corrección exacta de `qa.md` y una regresión cada uno (`test_r02_…` y dos pruebas ampliadas); `revisores/r01_ataques.py` 17/17; mutantes M29–M37. Rebasado sobre `origin/develop`.
- **Falta:** la QA r02 (repetir `revisores/r01_ataques.py` y lo que el revisor quiera).
- **Cuidado con:** H-03 cambia la semántica: una P3- abierta bloquea también un AJU- dentro de banda del mismo parámetro y componente. Las transacciones de H-04 envuelven el cuerpo entero de los tres métodos (el almacén es reentrante).

## 2026-11-17 · de claude a la QA (astra o un revisor de Claude que no implementó)

- **Fase en la que se entrega:** QA (r01).
- **Hecho:** PB-36 (revisión trimestral del umbral E de P-09, `proponer_ajuste` para cualquier CALIBRABLE, P3-EVAL- elevada por CT-19 a la cola de tipo 3 de HA con F10 intacto) y PB-33 (sección `NOV-AAAA-Www` de F6). Pruebas, mutantes (28/28), mapa y evidencias regeneradas (PB-33 y PB-36 «Superada»). Decisiones en INC-T176-01.
- **Falta:** la QA. Commit local («wip local: T-176»), sin push: lo integra quien coordina.
- **Commit:** ver `git log` de la copia de trabajo del ticket; mensaje «wip local: T-176 …».
- **Cuidado con:**
  - El estimador de Youden solo puede proponer subir el umbral con datos reales del ejecutor (F4 no tiene opciones no elegibles). El caso del plan (48) es sintético.
  - P-05 no tiene estimador: la prueba siembra su evidencia en `ESTIMADORES_TRIMESTRALES` (la preparación del plan la da).
  - Dentro de banda el AJU- de P-09 queda PROPUESTO, no EN_SOMBRA; `ajuste_en_sombra` filtra P-11 para que HT-03 no reciba umbrales como pesos.
  - La elevación también recoge las P3- ya existentes (P-11 fuera de banda, H5 «Limitado» → «No»); la orden `evaluar` de la CLI no eleva (CT-19 exige `run_id`).
  - Las tres pruebas `test_pb33_…` de T-173 siguen en el mapa y pasan; `test_pb33_novedades…` reutiliza su preparación (`_pb33_revision_y_run`).
  - `tools/cuotas.txt` baja ruff a 2812 (T-177/T-178 pueden tocar la misma línea).
- **Scripts útiles:** `.docs/tickets/T-176/mutantes.py`, `.docs/scripts/evidencias_plan_a.py --pb PB-36` y `--pb PB-33`.
