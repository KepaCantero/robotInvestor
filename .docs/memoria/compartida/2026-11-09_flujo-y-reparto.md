---
id: compartida/2026-11-09_flujo-y-reparto
autor: claude
fecha: 2026-11-09
tipo: convencion
etiquetas: [flujo, skills, qa, astra, claude]
fuente: docs/flujo_de_trabajo.md; AGENTS.md
vigencia: sustituida por compartida/2026-11-09_espacio-docs
---

- El operador pidió el 9-11-2026 un flujo común para Claude y Astra: planificar → implementar → probar → QA, con una skill por fase en `.agents/skills/` (enlazada desde `.claude/skills`).
- **La QA la hace el agente que no implementó.** Es la forma de revisión independiente del proyecto entre agentes; dentro de un mismo agente sigue valiendo un revisor nuevo sin contexto.
- Cada tarea deja sus cuatro archivos en `docs/tareas/<AAAA-MM-DD>_<pieza>_<tema>/`. Lo pendiente de revisar va en un commit con `[pendiente QA]` en el título y una entrada `traspaso` aquí.
- Astra crea su carpeta `memoria/astra/` la primera vez que trabaje en el repo.
