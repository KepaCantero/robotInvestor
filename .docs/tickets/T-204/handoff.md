# T-204 · Traspaso

Solo existe si el trabajo cambia de manos. Una sección por traspaso, la más reciente arriba.

## 2026-11-25 · de claude (implementador, cierre) a QA (ronda de cierre de la r03)

- **Hecho:**
  - H-13 corregido: etiquetas reales en INC-T204-03 y fila T-54 anotada sin borrar la cita.
  - La observación sobre `test_h02` (el cambio 17 solo en el §0).
  - El rebase sobre `origin/develop` (`d11662ff`). En `tools/cuotas.txt`, ruff queda en 1533 (la medida del gate sobre A y B) y mypy A en 67. En la deuda y las incidencias se conservan los dos lados.
- **Comprobado:** `r03_02` da 0. `r01_02`, `r01_05`, `r02_02` y `r02_03` en verde. `pruebas_scripts.sh` da 455. El gate de cierre está en `pruebas.md`.
- **Cuidado con:**
  - Los hashes de la rama cambiaron con el rebase (`80d152ec` es ahora `fad84daf`). `r03_02` sigue funcionando con el hash viejo porque el objeto existe.
  - `r03_01` sobre `253f33fd..HEAD` mezcla lo de develop. Hay que usar `2980b8c6` (la r02 rebasada) como base.
- **Commit:** «T-204 cierre: …», local, sin push.

## 2026-11-25 · de claude (implementador, r03) a QA (r03)

- **Fase en la que se entrega:** QA (r03), después del NO APTO de la r02. La r02b de la coordinación ya había aplicado la enmienda 6 y la limpieza.
- **Hecho:** H-09 a H-12 corregidos, cada uno con su prueba. Detalle en `analisis-tecnico.md` («Ronda r03»).
  - Los documentos vivos describen la Constitución V0.7 y la limpieza ya aplicadas.
  - `test_h02` comprueba invariantes del contenido.
  - Cuatro líneas de evidencia vuelven a su texto original y se corrige la concordancia de T-166.
  - `limpiar_docs.py` reconoce más evidencia.
  - refs-vivas ve `NOMBRE=ruta`.
- **Resultado:** `pruebas_scripts.sh` da 455. 38 mutantes propios y 10 del revisor, muertos. Scripts r01 y r02 del revisor en verde (ver `pruebas.md` para `r01_04` y `r02_01`). Marco 62/62.
- **Cuidado con:**
  - `r02_01` atribuye cada caso al fichero siguiente del diff. Los ficheros reales de H-11 son T-106 (dos líneas), T-187, T-199 y T-166.
  - Se cambió una cita de `qa.md` (docs/x.md, el fichero de juguete de `r02_03`), que hacía fallar refs-vivas.
  - develop está en `358576c3` (T-201) y esta rama no se rebasa.
- **Commits:** «T-204 r03: …», locales, encima de `129376f4`, sin push.

## 2026-11-25 · de claude (implementador, r02) a QA (r02)

- **Fase en la que se entrega:** QA (r02), después del NO APTO de la r01.
- **Hecho:** H-01 a H-08 corregidos, cada uno con la corrección del `qa.md` y su prueba. Detalle en `analisis-tecnico.md` («Ronda r02»).
  - Parche de la Constitución: es la «enmienda 6», con el choque de numeración declarado en INC-T204-01. Anota el cambio 17 y pone la fecha nueva.
  - `limpiar_docs.py` respeta la marca T-204, la evidencia de gates y suites, los encargos y las citas «…». Sus pruebas están en `pruebas_gate_bloques.py` y la propuesta está regenerada.
  - Skill con A ≥ 607 y B ≥ 174; 43 hallazgos y 10 gates.
  - Marca como palabra y «=» solo en opciones, con 3 casos.
  - Cuota de ruff igual a la medida.
  - INC-T204-04 completa.
- **Resultado:** los scripts del revisor en verde (Q1 de `r01_03` adaptado con `r02_mutantes_revisor.py`). 36 mutantes propios muertos. `pruebas_scripts.sh` da 449.
- **Sigue sin aplicar:** el parche de la Constitución y la limpieza de `.docs/`. Los aplica la coordinación cuando el operador lo confirme.
- **Cuidado con:**
  - develop ya está en `358576c3` (T-201: ruff 2797 y mypy A 67). Esta rama sigue sobre `d23afe0`, sin rebase. Al integrar, `test_h07` exige que la cuota de ruff sea la medida sobre A y B con el código integrado.
  - El nombre `enmienda4_constitucion.patch` es el de la r01: lo cita el script del revisor.
- **Commit:** «T-204 r02: …», local, encima de `123118ea`, sin push.

## 2026-11-25 · de claude (implementador) a QA (otro agente o un revisor nuevo)

- **Fase en la que se entrega:** QA (r01).
- **Hecho:**
  - `bloque_a_forex/` borrado, junto con su mypy, su pytest, sus cuotas, sus 180 huellas del corpus (re-congelado: 525) y su lugar en `preparar_entorno.sh` y `qa_rama.sh`.
  - El gate queda en 10 comprobaciones (7 con `--core`) y ruff baja a 1604.
  - `refs-vivas` trata `bloque_a_forex` como bloque retirado (INC-T204-02).
  - La prueba nueva `.docs/scripts/pruebas_gate_bloques.py` impide que el Forex vuelva al gate.
  - Menciones reescritas en `CLAUDE.md`, `prompts/`, `docs/`, la skill de pruebas y `sistema_global/` (sin la Constitución).
  - 29 mutantes, todos muertos.
- **Falta, y depende del operador:**
  - **La Constitución.** La enmienda 4 está en `enmienda4_constitucion.patch` (INC-T204-01).
  - **La limpieza de `.docs/`.** Se hace con `limpiar_docs.py --aplicar` (INC-T204-03).

  El sistema de permisos de la sesión bloqueó las dos escrituras aunque la orden ampliada las pedía. No se aplicaron.
- **Commit:** local, en `wip/t204`, encima de `d23afe0` (origin/develop), sin push.
- **Cuidado con:**
  - Las citas antiguas al Forex en tickets, diario, memoria y diseño siguen ahí a propósito. `refs-vivas` las exime por estar en esos registros.
  - En `CLAUDE.md`, `prompts/`, `docs/` y los índices de `.docs/`, una cita sin «T-204» en la línea hace fallar el gate.
  - `wip/t202` mide cuotas del Forex: se ajusta al integrar.
  - El operador limpiará `bloque_a_forex/` del historial después de integrar. Este ticket no toca el historial.
- **Scripts útiles:** `.docs/tickets/T-204/mutantes.py`, `.docs/scripts/pruebas_gate_bloques.py` y `.docs/tickets/T-204/limpiar_docs.py`. Este último, sin opciones, solo propone.
