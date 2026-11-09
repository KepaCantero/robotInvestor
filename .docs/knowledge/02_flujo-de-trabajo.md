# 02 · Flujo de trabajo: planificar → implementar → probar → QA

Este flujo es común a los dos agentes que trabajan en el repositorio, Claude (Anthropic) y Astra (OpenAI), y a las personas del equipo. Cada fase es una skill en el formato abierto `SKILL.md`, de modo que los dos agentes la leen igual. Todo el trabajo de una tarea vive en su ticket, `.docs/tickets/T-NN/`, y el ID es el mismo que tiene en la deuda técnica.

| Fase | Skill | Qué deja en el ticket |
| --- | --- | --- |
| 1 · Planificar | `.agents/skills/ri-planificar/SKILL.md` | `README.md`: estado, alcance, diseño, riesgos, criterios de aceptación y plan de pruebas |
| 2 · Implementar | `.agents/skills/ri-implementar/SKILL.md` | El código y `analisis-tecnico.md` (causa raíz, evidencia e implementación) |
| 3 · Probar | `.agents/skills/ri-probar/SKILL.md` | Suites y gates en verde, y `pruebas.md` |
| 4 · QA | `.agents/skills/ri-qa/SKILL.md` | `qa.md` con el veredicto APTO / NO APTO, la carpeta `revisores/` y el cierre |

```
planificar ──► implementar ──► probar ──► QA ──► APTO ──► cierre (deuda, diario, memoria, commit, aviso)
                    ▲                      │
                    └──────── NO APTO ─────┘  (cada hallazgo con su prueba de regresión)
```

## Dónde vive cada cosa

- **Skills:** en `.agents/skills/`, que es donde las buscan Codex y Astra. Para Claude, `.claude/skills` es un enlace a esa misma carpeta, así que hay una sola copia. En Windows, si git no crea el enlace, activa `core.symlinks` o copia la carpeta, y no edites la copia.
- **Instrucciones:** `AGENTS.md` para Astra y otros agentes; `CLAUDE.md` para Claude. Las reglas del proyecto son las mismas.
- **Tickets, diario, scripts y memoria:** `.docs/README.md`.
- **Herramientas:** cada fase usa los scripts de `.docs/scripts/`. Por ejemplo, `nuevo_ticket.sh` para abrir un ticket, `gate.sh` y `pruebas_marco.sh` para probar, y `commit.sh` para cerrar.

## Reparto entre agentes

- Cualquier agente puede planificar, implementar y probar.
- **La QA la hace siempre un agente distinto del que implementó.** Si implementa Claude, revisa Astra, y al revés. Dos modelos de empresas distintas tienen puntos ciegos distintos, así que es la revisión independiente más barata que existe.
- **Cuando el trabajo cambia de manos**, se escribe `handoff.md` dentro del ticket y el código va en un commit con `[pendiente QA]` en el título.
- **Commits** directos en `develop`, con el mensaje en español y prefijo de área. Si los dos agentes trabajan a la vez, lo hacen en piezas distintas, y solo el dueño del ticket hace el commit final.

## Lo que el flujo no cambia

Las reglas de `CLAUDE.md` siguen mandando:
- un kit de contexto por fase;
- ningún número escrito a mano;
- el esquema primero;
- mock antes que API;
- las líneas base de pruebas;
- `./tools/check_all.sh` en verde para cerrar.
