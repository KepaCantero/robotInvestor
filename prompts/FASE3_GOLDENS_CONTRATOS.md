# PROMPT — Fase 3 · Goldens de contratos (ambos A)

> Sesión de precisión sobre formatos. Modelo: el más capaz. Requisito: Fases 0–1 verificadas.

---

FASE 3 — Congelar los contratos CT en goldens verificables para que ningún cambio futuro pueda romper un formato sin que salte una prueba. Empieza por bloque_a (CT-01..CT-25) y luego replica en bloque_a_forex con sus contratos.

Kit de contexto:
- `bloque_a/01_Gobernanza/Documento 0 - Protocolo maestro del Bloque A - Versión óptima V5.1.md` — Anexo B (campos mínimos de contratos y esquemas JSON) y §6 (catálogo de contratos).
- `bloque_a/06_Plantillas_entregables/Esquema JSON - Paquete de oportunidades - V5.0.json` + su ejemplo válido (y el de seguimiento V5.1): son la definición, no una inspiración.
- `bloque_a/11_Ejecutor/bloque_a/contratos.py` (ESQUEMAS existentes) y la lección de robotTrading: goldens congelados y comparados byte a byte en CI.

Entregables:
1. Por cada contrato con esquema en el código: validación jsonschema del ejemplo/fixture + golden congelado (fichero esperado) comparado exactamente.
2. Los contratos que solo existen en el Anexo B y no tienen esquema en código: esquema JSON nuevo derivado SOLO del Anexo B + ejemplo mínimo, marcado como «derivado del Anexo B» en el propio fichero.
3. Regla de re-congelado documentada en el README de los goldens: solo deliberado, un commit con golden+motivo (igual que el corpus de conformance de robotTrading).
4. `pytest` de los tres bloques sigue con cero fallos.

Restricciones fijas + commits `fase3:`.

Criterio de éxito: cambio a propósito un campo de un golden y la suite falla; lo revierto y vuelve a verde. Si eso no ocurre, el golden no protege nada.
