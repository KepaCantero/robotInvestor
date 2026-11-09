# 01 · Qué es el Robot Investor y por dónde empezar

**Qué es.** Un sistema personal de inversión, por bloques, que investiga, analiza, compara, construye carteras, controla el riesgo, ejecuta con autorización y aprende. Cada usuario tiene su propia copia y su propio dinero (D-47). Hoy todo funciona en simulación.

**Orden de lectura para alguien nuevo (persona o agente):**

1. `AGENTS.md` (agentes en general) o `CLAUDE.md` (Claude): reglas del repositorio.
2. `.docs/README.md`: cómo se organiza el trabajo.
3. `.docs/memoria/LEEME.md` y los índices de `.docs/memoria/`: lo que conviene saber ya.
4. `sistema_global/seguimiento/Briefing_de_arranque.md`: el estado del proyecto en una lectura.
5. `sistema_global/constitucion/Constitucion_Global.md`: la fuente de verdad. Solo las secciones que toque la tarea.
6. `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md`: lo pendiente (cada `T-NN` es un ticket posible).

**Piezas del repositorio:**

| Carpeta | Qué hay |
| --- | --- |
| `bloque_a/`, `bloque_b/` | Bloques A y B entregados (anteriores a la Constitución global; se revisan con el operador antes de conectarlos) |
| `bloque_a_forex/` | Prueba antigua; fuera del Robot Investor |
| `sistema_global/` | Constitución, código de referencia de la Fase 1 (`sistema_global/marco_comun_c/`), Documentos 0 y seguimiento |
| `tools/` | Gates del repositorio (`./tools/check_all.sh`) |
| `.agents/skills/` | Skills del flujo de trabajo (también en `.claude/skills`) |
| `.docs/` | Tickets, diario, scripts, conocimiento y memoria |
