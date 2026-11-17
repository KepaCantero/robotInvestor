# T-174 · Traspaso

Solo existe si el trabajo cambia de manos. Una sección por traspaso, la más reciente arriba.

## 2026-11-17 · de claude (implementador, r03) al revisor (comprobación de H-07 y H-08)

- **Hecho:** H-07 (huérfanas: `proceso`, `huerfanas()`, aviso único, `huerfana: true`) y H-08 (intento al reclamar, sin repetir una ya entregada), con sus pruebas `test_r03_*`; A8 de la r01 corregido; mutantes M22 a M28.
- **Commit:** local, sin push («wip local: T-174 r03»).

## 2026-11-17 · de claude (implementador, r02) a un revisor nuevo (QA r02)

- **Fase:** QA r02, tras la QA r01 NO APTO.
- **Hecho:** H-01 a H-06 corregidos con sus pruebas (`test_r02_*`), mutantes M12 a M21, órdenes `consulta-broker revisiones` y `relanzar`, evidencias regeneradas.
- **Cuidado con:** A8 de `r01_01_ataques.py` falla a propósito (afirma FALLIDA; H-05 pide ENTREGADA). Las EN_CURSO solo se relanzan expresamente (ver `analisis-tecnico.md`, r02).
- **Commit:** local, sin push («wip local: T-174 r02»).

## 2026-11-17 · de claude (implementador) a un revisor nuevo sin contexto (QA r01)

- **Fase en la que se entrega:** QA.
- **Hecho:**
  - la revisión C2 por una respuesta CT-23 a un supuesto ya entregado (`interfaz_broker.py`, más dos líneas en `orquestacion.py` y una en `seguimiento.py`);
  - 8 pruebas en `tests/test_t174_pb61_revision_c2.py`;
  - PB-61 en el mapa como AUTOMATICA y las evidencias regeneradas;
  - INC-T174-01, y ruff bajado a 2808.
- **Falta:** la QA (`ri-qa`) y la integración en `develop`. El commit es local («wip local: T-174»), sin push. Lo integra la sesión coordinadora.
- **Commit:** ver `pruebas.md` (sección «Commit»).
- **Cuidado con:**
  - La regla de «invalida» es deliberadamente amplia: toda respuesta nueva cuenta como invalidación (INC-T174-01). No es un fallo, pero sí la decisión que más conviene discutir.
  - En el ejecutor por línea de órdenes solo está activo DIV. Una consulta con `clases: ["CRI"]` no abre revisión porque CRI no se analiza, y eso es lo correcto. Para verlo por la línea de órdenes, usa una consulta sin clases (ver `pruebas.md`).
  - Hay agentes en paralelo (T-173, T-175) tocando `orquestacion.py`. Los cambios de T-174 ahí son dos líneas aisladas.
- **Scripts útiles:**
  - `.docs/tickets/T-174/mutantes_t174.py <carpeta bloque_a> <copia>`: copia el `bloque_a` entero, porque copiar solo `11_Ejecutor` hace «morir» a todos los mutantes;
  - `.docs/scripts/evidencias_plan_a.py --pb PB-61`;
  - `bloque_a/11_Ejecutor/tests/goldens_ct.py`.
