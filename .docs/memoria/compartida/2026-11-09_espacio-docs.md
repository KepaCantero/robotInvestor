---
id: compartida/2026-11-09_espacio-docs
autor: claude
fecha: 2026-11-09
tipo: convencion
etiquetas: [flujo, docs, tickets, diario, scripts, qa, astra, claude]
fuente: .docs/README.md; .docs/knowledge/02_flujo-de-trabajo.md; ticket .docs/tickets/T-60/
vigencia: vigente
---

Sustituye a `compartida/2026-11-09_flujo-y-reparto`.

- **Todo el trabajo de los agentes vive en `.docs/`**, según la propuesta de Kepa del 9-11-2026. El índice y las reglas están en `.docs/README.md`.
- **Tickets:** cada tarea tiene su carpeta `.docs/tickets/T-NN/`, con el mismo ID que en la deuda técnica. Contiene `README.md` (plan), `analisis-tecnico.md`, `pruebas.md`, `qa.md` con la carpeta `revisores/`, y `handoff.md` si el trabajo cambia de manos. Los traspasos ya no van en la memoria.
- **QA cruzada:** la hace siempre el agente que no implementó. Lo pendiente de revisar se sube en un commit con `[pendiente QA]` en el título.
- **Diario:** `.docs/diario/AAAA-MM.md`, con la entrada más reciente arriba. Se escribe al cerrar el trabajo del día.
- **Scripts:** antes de hacer algo a mano, se mira `.docs/scripts/`. Lo que se vaya a repetir se guarda ahí como script (sobre `common.sh`, con los secretos solo en `.env`) para no gastar otra vez los mismos tokens. Ya existen `gate.sh`, `pruebas_marco.sh`, `nuevo_ticket.sh`, `diario.sh`, `memoria.sh` y `commit.sh`.
- **Diferencias con la propuesta de Kepa:** todo en español (él propone el conocimiento en inglés) y con commit, porque se comparte entre personas y agentes.
