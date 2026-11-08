# Flujo de trabajo: planificar → implementar → probar → QA

Este flujo es común a los dos agentes que trabajan en este repositorio: Claude (Anthropic) y Astra (OpenAI). Cada fase es una skill con el mismo formato abierto (`SKILL.md`), así que los dos la leen igual:

| Fase | Skill | Resultado |
| --- | --- | --- |
| 1 · Planificar | `.agents/skills/ri-planificar/SKILL.md` | `01_plan.md`: alcance, diseño, riesgos, criterios de aceptación y plan de pruebas |
| 2 · Implementar | `.agents/skills/ri-implementar/SKILL.md` | El código y `02_implementacion.md` |
| 3 · Probar | `.agents/skills/ri-probar/SKILL.md` | Suites y gates en verde, y `03_pruebas.md` |
| 4 · QA | `.agents/skills/ri-qa/SKILL.md` | Veredicto APTO / NO APTO en `04_qa.md` y cierre |

```
planificar ──► implementar ──► probar ──► QA ──► APTO ──► cierre (deuda, memoria, commit, aviso)
                    ▲                      │
                    └──────── NO APTO ─────┘  (cada hallazgo con su prueba de regresión)
```

## Dónde vive cada cosa

- **Skills:** `.agents/skills/`, donde Codex y Astra las buscan. Para Claude Code, `.claude/skills` es un enlace a esa misma carpeta: hay una sola copia. En Windows, si git no crea el enlace, basta con activar `core.symlinks` o copiar la carpeta (sin editar la copia).
- **Instrucciones para Astra y otros agentes:** `AGENTS.md`. Para Claude: `CLAUDE.md`. Las reglas del proyecto son las mismas.
- **Trabajo de cada tarea:** `docs/tareas/<AAAA-MM-DD>_<pieza>_<tema>/`, con los cuatro archivos numerados y la carpeta `revisores/` de la QA.
- **Memoria de los agentes:** `memoria/LEEME.md`.

## Reparto entre agentes

- Cualquier agente puede planificar, implementar y probar.
- **La QA la hace siempre un agente distinto del que implementó.** Si implementa Claude, revisa Astra, y al revés. Dos modelos de empresas distintas tienen puntos ciegos distintos: es la revisión independiente más barata que existe.
- El paso de una fase a otra entre agentes se anota como entrada de tipo `traspaso` en `memoria/compartida/`, y el código va en un commit con `[pendiente QA]` en el título.
- Commits directos en `develop`, mensajes en español con prefijo de área. Si los dos agentes trabajan a la vez, en piezas distintas, y solo el dueño de la tarea hace el commit final.

## Lo que el flujo no cambia

Las reglas de `CLAUDE.md` siguen mandando: un kit de contexto por fase, ningún número a mano, esquema primero, mock antes que API, líneas base de pruebas, y `./tools/check_all.sh` en verde para cerrar.
