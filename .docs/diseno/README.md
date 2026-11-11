# Diseño de los bloques (propuestas para discutir)

El operador está decidiendo la arquitectura de cada bloque antes de construir nada más (11-11-2026). Aquí viven las propuestas de diseño y sus revisiones independientes. **Nada de esta carpeta se implementa** hasta que el operador cierre el diseño de ese bloque y se abra su ticket.

Cada bloque tiene su carpeta con:
- la propuesta de un agente (por ejemplo, `propuesta_claude.md`);
- el encargo de revisión al otro agente;
- la revisión del otro agente, cuando la entregue (fichero «revision_astra.md» o «revision_claude.md»).

| Bloque | Propuesta | Revisión | Estado |
| --- | --- | --- | --- |
| A (buscador de oportunidades) | `.docs/diseno/bloque_a/propuesta_claude.md` (rediseño: de 25 agentes a 6 papeles de IA) | Astra, encargo en `.docs/diseno/bloque_a/encargo_revision_astra.md` | En revisión |
| B (selección de activos) | `.docs/tickets/T-68/evaluacion_claude.md` (precisión frente a consumo) y `.docs/diseno/bloque_b/propuesta_rediseno_claude.md` (rediseño: de 24 agentes a 5 papeles de IA) | Astra, encargos en `.docs/tickets/T-68/encargo_revision_astra.md` y `.docs/diseno/bloque_b/encargo_revision_astra.md`, juntos | En revisión |
| C (análisis en profundidad) | — | — | Aplazado por el operador: es el más complejo |
| D (comparar opciones) | `.docs/diseno/bloque_d/propuesta_claude.md` | Astra, encargo en `.docs/diseno/bloque_d/encargo_revision_astra.md` | En revisión |
| E (dimensionar y construir carteras) | `.docs/diseno/bloque_e/propuesta_claude.md` | Astra, encargo en `.docs/diseno/bloque_e/encargo_revision_astra.md` | En revisión |
| F (control de riesgo) | `.docs/diseno/bloque_f/propuesta_claude.md` | Astra, encargo en `.docs/diseno/bloque_f/encargo_revision_astra.md` | En revisión |
| G (ejecución y conciliación) | `.docs/diseno/bloque_g/propuesta_claude.md` | Astra, encargo en `.docs/diseno/bloque_g/encargo_revision_astra.md` | En revisión |
| H (seguimiento de posiciones) | `.docs/diseno/bloque_h/propuesta_claude.md` | Astra, encargo en `.docs/diseno/bloque_h/encargo_revision_astra.md` | En revisión |
