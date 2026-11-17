# T-175 · Traspaso

Solo existe si el trabajo cambia de manos. Una sección por traspaso, la más reciente arriba.

## 2026-11-17 · r02 · de claude al revisor de la QA r02

- **Fase en la que se entrega:** QA (r02, tras la QA r01 NO APTO).
- **Hecho:**
  - **H-01:** un texto del modelo que G3-MET-13 rechazaría se sustituye en el técnico. Queda íntegro en F3, se deja una ADVERTENCIA en el G3V de F7 y la entrega sale.
  - **H-02:** listas y RK finito.
  - **H-03:** textos corregidos.
  - Rebasado sobre origin/develop (`375d24b`).
  - 22/22 mutantes muertos.
  - Las pruebas del revisor (`r01_01`, `r01_02` en sus cuatro modos y `r01_03`) se volvieron a ejecutar.
  - Evidencias regeneradas: 217/217.
- **Commit:** local, «wip local: T-175 r02» (sin push).
- **Cuidado con:**
  - Con un texto retirado, el dictamen efectivo es APTO_CON_ADVERTENCIAS, no APTO.
  - La ADVERTENCIA va delante en G3-MET-13, porque HA guarda cinco detalles.
  - `tecnico()` sin `extras["alternativas_descartadas"]`, como en las pruebas unitarias, no sustituye nada: no tiene `bloque`.

## 2026-11-17 · de claude a astra (o un revisor que no implementó)

- **Fase en la que se entrega:** QA (r01).
- **Hecho:**
  - El informe técnico tiene ahora la subsección 4.N.4 «Alternativas descartadas relevantes», con las finalistas no elegibles según HT-03: no son opción, ni vigentes, ni de arrastre.
  - La sección 6 lleva las objeciones fuertes y moderadas de esas alternativas, marcadas «(alternativa descartada)».
  - Hay 9 pruebas nuevas y 12 mutantes propios, todos muertos.
  - PB-38 pasa a «Superada»: mapa y evidencias regenerados.
  - INC-T175-01 `[PROPUESTO]`.
  - Cuota de mypy A: 109 → 102.
- **Falta:** la QA independiente.
- **Commit:** local, «wip local: T-175» (sin push).
- **Cuidado con:**
  - Las pruebas de T-175 no dan por buena la elección de filas de INC-T175-01: qué entra en 4.N.4 y que no se ordene por cercanía al umbral.
  - (r01, superado en la r02 por H-01) Una mención «valid-» en el texto del modelo de una alternativa bloqueaba toda la entrega.
  - En el V6 de solo RV el simulado resuelve la objeción fuerte; la prueba V6 fuerza la contrarréplica (en el de doce clases salen 4.2.4 y 4.4.4 sin forzar).
  - Puede haber conflicto con T-173 y T-174 en `mapa_plan_pruebas.json`, `docs/evidencias_pruebas_bloque_a.md`, `docs/incidencias.md`, la deuda técnica y `tools/cuotas.txt`. Aquí solo cambian la fila PB-38, una línea de INC-T116-03, la incidencia nueva al final, la fila T-175 y la línea de mypy A.
- **Scripts útiles:**
  - `.docs/tickets/T-175/mutantes.py`
  - `.docs/tickets/T-175/diff_tecnico.py`
  - `.docs/scripts/evidencias_plan_a.py --pb PB-38`
