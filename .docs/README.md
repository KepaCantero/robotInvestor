# .docs · espacio de trabajo de los agentes

Todo lo que Claude, Astra y las personas del equipo necesitan para trabajar en el repositorio sin depender del historial de una conversación. Estructura propuesta por Kepa el 9-11-2026, adaptada al proyecto (en español y con commit, porque se comparte entre personas y agentes).

| Carpeta | Para qué sirve | Quién escribe |
| --- | --- | --- |
| `.docs/README.md` | Este índice y las reglas | Cualquiera, con cuidado |
| `.docs/tickets/` | Una carpeta por ticket (`T-NN`, el mismo ID que en la deuda técnica): `README.md` (estado, alcance, aceptación y plan), `analisis-tecnico.md` (causa raíz, evidencia e implementación), `pruebas.md`, `qa.md` y, solo si el trabajo cambia de manos, `handoff.md`. Plantillas en `.docs/tickets/_plantilla/` | El agente que lleva el ticket; la QA, el revisor |
| `.docs/diario/` | Diario por mes (`AAAA-MM.md`), la entrada más reciente arriba | Quien trabaja ese día |
| `.docs/scripts/` | Scripts de trabajo: todo lo que se hace más de una vez | Cualquiera |
| `.docs/knowledge/` | Documentos de incorporación, estáticos y numerados | Cualquiera, al cambiar el modo de trabajo |
| `.docs/memoria/` | Memoria indexada de los agentes: `compartida/` y una carpeta por agente | Cada agente en la suya y en `compartida/` |

## Reglas

1. **Nunca se borra nada de `.docs/`.** Lo viejo se marca (ticket `CERRADO`, entrada de memoria `sustituida`) y se conserva.
2. **Nunca se hace commit de secretos.** Los tokens viven en `.env`, en la raíz del repositorio (está en `.gitignore`), y solo los carga `.docs/scripts/common.sh`. Plantilla: `.docs/scripts/env.ejemplo`.
3. **Nada personal ni financiero de ningún usuario** (el repositorio es público y cada usuario tiene su propia copia, D-47).
4. **Lo repetible se automatiza.** Antes de hacer algo a mano, mira `.docs/scripts/`. Si vas a hacer algo que se repetirá (comprobar, probar, crear, publicar, migrar), escríbelo como script, guárdalo ahí y apúntalo en la tabla de scripts. La próxima vez se ejecuta el script y no se gastan otra vez los mismos tokens.
5. **Los traspasos van dentro del ticket** (`handoff.md`), no en la raíz ni en la memoria.
6. **Carpetas basura conocidas** (no se leen, no se citan, no se suben): `.venv/`, `__pycache__/`, `.pytest_cache/`, `.mypy_cache/`, `.ruff_cache/`, `.docs/scripts/.logs/`, `estado_bloque_a/`, `entregables/`.

## Scripts

| Script | Qué hace |
| --- | --- |
| `.docs/scripts/common.sh` | Base de todos: modo estricto, raíz del repo, carga de `.env`, `requiere_var`, `requiere_cmd`, Python del proyecto |
| `.docs/scripts/gate.sh` | Gate rápido (`--core`) o completo (`--completo`), con el log en `.docs/scripts/.logs/` |
| `.docs/scripts/pruebas_marco.sh` | Todas las suites del marco común de C, leídas del LEEME; avisa de las que falten en él |
| `.docs/scripts/nuevo_ticket.sh` | Crea `.docs/tickets/T-NN/` desde la plantilla |
| `.docs/scripts/diario.sh` | Añade la entrada de hoy al diario del mes, arriba |
| `.docs/scripts/memoria.sh` | Crea una entrada de memoria, la indexa y, con `--sustituye`, marca la anterior |
| `.docs/scripts/commit.sh` | Gate, commit (autor y líneas finales desde `.env`) y push a `develop` |
| `.docs/scripts/qa_rama.sh` | QA de una rama de otro agente: commits, archivos, si se fusiona por avance rápido, copia limpia y pruebas de cada pieza tocada contra el código de la rama |

## Diario: formato

```markdown
## AAAA-MM-DD — <título> (<autor>)

**Resultado.** Qué quedó hecho.
**Causas y hallazgos.** Qué se descubrió y por qué pasó lo que pasó.
**Correcciones.** Qué se arregló.
**Operaciones y siguiente.** Commits, despliegues, y lo próximo.
```

## Diario, memoria y tickets: qué va dónde

- **Ticket:** todo sobre una tarea concreta, de principio a fin.
- **Diario:** qué pasó cada día, en orden cronológico; enlaza a los tickets.
- **Memoria:** lo que conviene saber siempre (reglas, lecciones, estado), indexado para leer solo lo necesario.
- **Knowledge:** cómo se trabaja aquí, para quien llega nuevo.
