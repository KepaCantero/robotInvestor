# PROMPT — Fase 1 · Las 21 fichas nuevas del Catálogo (bloque_a)

> Sesión de implementación mecánica pero con especificación estricta. Modelo: Sonnet.
> Requisito: Fase 0 verificada (el informe del verificador de IDs existe y las
> decisiones del skew están documentadas en docs/incidencias.md).

---

FASE 1 — Implementar en el Motor del bloque_a las fichas del Catálogo V5.0 que hoy responden METODO_NO_IMPLEMENTADO, empezando por las 21 de las familias nuevas (IDX, FON, DER, MON, TCV) y siguiendo por lo que el verificador de la Fase 0 clasificó como SOLO_CATALOGO por prioridad P0.

Kit de contexto de ESTA fase:
- `bloque_a/04_Motor_conocimiento_y_catalogo/Catálogo de cálculos del Motor - V5.0.md` — cada ficha es un contrato de 14 campos: método, entradas mínimas, parámetros, salidas, supuestos, TOLERANCIAS Y SEMILLA, verificación, referencia ingenua, aclaración y rechazo.
- `bloque_a/11_Ejecutor/bloque_a/motor/operaciones.py` (patrón de las funciones existentes) y `servicio.py` (despacho CT-09/CT-10, ALTERNATIVAS, idempotencia).
- `bloque_a/11_Ejecutor/tests/test_unitarias.py` (patrón de casos de control).
- Las decisiones de la Fase 0 en `docs/incidencias.md` (el skew resuelto dice qué IDs mandan).

Reglas de la fase:
- CADA número, tolerancia y semilla sale de la ficha del Catálogo — nada inventado. Si una ficha es ambigua o contradice a otra, te paras, lo documentas en docs/incidencias.md y sigues con otra ficha.
- Cada ficha implementada: función en operaciones.py + registro en FICHAS_CATALOGO + caso de control en tests usando la «Verificación» y la «Referencia ingenua» de la propia ficha.
- Actualiza CATALOG_VERSION según la decisión documentada de la Fase 0.
- Si una ficha depende de una librería no instalada (como garch con arch), declárala en pyproject como extra y que el test se salte limpiamente si falta — el patrón ya existe.

Entregables: fichas implementadas con sus tests; `pytest -q bloque_a/11_Ejecutor` termina con MÁS de 58 pasando y CERO fallos; tabla en docs/AVANCE.md con ficha → estado.

Restricciones fijas: no modificas ningún .md del corpus; no tocas bloque_a_forex/ ni bloque_b/; nada en silencio; commits `fase1:`.

Criterio de éxito: lanzo `pytest -q bloque_a/11_Ejecutor` y el verificador de la Fase 0 ya no clasifica como SOLO_CATALOGO las fichas de esta fase.
