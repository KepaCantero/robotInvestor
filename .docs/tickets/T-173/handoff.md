# T-173 · Traspaso

Solo existe si el trabajo cambia de manos. Una sección por traspaso, la más reciente arriba.

## 2026-11-17 · de claude (implementador) a QA (otro agente o un revisor nuevo)

- **Fase en la que se entrega:** QA (r01).
- **Hecho:**
  - PB-50: degradación automática de H1–H4 de «Sí» a «Limitado» por DM-HLN en el C5 (`Evaluador.degradacion_dm` y `aplicar_degradacion_dm`).
  - PB-64: publicación de los estados H5 en F6 (`EH5-`), en el paquete (`x_estados_h5` y el `estado` de cada hito) y en el informe técnico.
  - 16 pruebas nuevas en `tests/test_t173.py`; el mapa y las evidencias están regenerados. 14 mutantes propios, todos muertos (`mutantes.py`).
- **Falta:** la QA. Commit local, sin push.
- **Commit:** el «wip local: T-173» de la rama separada del worktree (ver `pruebas.md`).
- **Cuidado con:**
  - Los números de 12.2 que el Anexo A no fija (α, n mínima, pérdida, h): son `[PROPUESTO]` en INC-T173-01, sin número nuevo.
  - `test_pb33_…` de `test_fase4_huecos.py` cambió: su celda también pierde con significación y ahora se degrada (`analisis-tecnico.md`).
  - T-174 y T-175 trabajan en paralelo. Aquí `orquestacion.py` no se ha tocado y `redaccion.py` solo en dos puntos del informe técnico.
- **Scripts útiles:** `.docs/scripts/evidencias_plan_a.py --pb PB-50` y `--pb PB-64`; `.docs/tickets/T-173/mutantes.py`.

## 2026-11-17 · de claude (implementador, r02) a QA (r02)

- **Fase en la que se entrega:** QA (r02).
- **Hecho:**
  - Rebase sobre `origin/develop` (`375d24b`).
  - H-01 a H-04 corregidos (`analisis-tecnico.md`, «Ronda r02»).
  - 8 pruebas nuevas en `test_t173.py` y una en `test_fase4_huecos.py`.
  - 24 mutantes (10 nuevos para H-01, H-02 y H-03), todos muertos. Los ataques del revisor y las tasas están en `pruebas.md`.
- **Falta:** la QA r02 y el gate 12/12.
- **Commit:** el «wip local: T-173 r02» de la rama separada del worktree.
- **Cuidado con:**
  - `revisores/r01_ataques.py` §1–§3 y §5–§10 siembran todos sus PRG con una sola fecha de resolución. Con la r02 eso es un solo conglomerado, no hay DM y §1 falla al leer `dm_hln`.
  - `r02_ejecutar_ataques_r01.py` lo ejecuta sección a sección y, con `--fechas-distintas`, da a cada PRG su propia fecha, para que esas secciones ejerzan la regla.
- **Scripts útiles:** `r02_ejecutar_ataques_r01.py`, `r02_tasa_falsa.py`, `mutantes.py` y `revisores/r01_*`.

## 2026-11-17 · de claude (implementador, cierre de la QA r02) a QA

- **Fase en la que se entrega:** ronda de cierre de la QA r02 (APTO con H-05 y H-06 bajos).
- **Hecho:**
  - H-05 y H-06 corregidos (`analisis-tecnico.md`, «Ronda de cierre…»).
  - 25 pruebas en `test_t173.py`.
  - 26 mutantes, todos muertos.
  - `r01_regresion.sh`: salidas idénticas.
  - Tasas y potencia en INC-T173-01. Evidencias regeneradas.
- **Falta:** revisar el cierre y el gate 12/12.
- **Cuidado con:** `test_pb33_…` vuelve a su criterio original, porque RV × H3 ya no se degrada con la familia fija.
