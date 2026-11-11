# Diseño de los bloques (propuestas para discutir)

El operador está decidiendo la arquitectura de cada bloque antes de construir nada más (11-11-2026). Aquí viven las propuestas de diseño y sus revisiones independientes. **Nada de esta carpeta se implementa** hasta que el operador cierre el diseño de ese bloque y se abra su ticket.

Cada bloque tiene su carpeta con:
- la propuesta de un agente (por ejemplo, `propuesta_claude.md`);
- el encargo de revisión al otro agente;
- la revisión del otro agente, cuando la entregue (fichero «revision_astra.md» o «revision_claude.md»).

| Bloque | Propuesta | Revisión | Estado |
| --- | --- | --- | --- |
| B (selección de activos) | `.docs/tickets/T-68/evaluacion_claude.md` (precisión frente a consumo) | Astra, encargo en `.docs/tickets/T-68/encargo_revision_astra.md` | En revisión |
| C (análisis en profundidad) | — | — | Aplazado por el operador: es el más complejo |
| D (comparar opciones) | `.docs/diseno/bloque_d/propuesta_claude.md` | Astra, encargo en `.docs/diseno/bloque_d/encargo_revision_astra.md` | En revisión |
