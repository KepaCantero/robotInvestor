---
id: claude/2026-11-14_dos-agentes-a-la-vez
autor: claude
fecha: 2026-11-14
tipo: regla
etiquetas: [agentes, limite, operador]
fuente: orden del operador en la sesión del 14-11-2026
vigencia: vigente
---


## Regla

El operador, el 14-11-2026: «Llévalo en dos en dos». Antes había dicho «puedes ir lo rápido que quieras».

## Por qué

Con cuatro agentes a la vez (QA e implementación) más el gate, el límite de uso de cinco horas se agotó dos veces en unos 30 a 40 minutos, y todo quedó parado hasta que el operador lo restableció.

## Cómo se aplica

- Como mucho dos subagentes trabajando a la vez. El gate de un commit puede correr mientras tanto.
- Se da prioridad a lo que desbloquea más: primero las correcciones y la QA del código que ya está en `develop`.
- Cada agente escribe su `qa.md` o hace commits locales según avanza: un corte no pierde trabajo y se reanuda con un mensaje al mismo agente.
- Antes de reanudar, guardar el trabajo sin commit de cada copia en un commit local.
