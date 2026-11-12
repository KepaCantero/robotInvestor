---
id: compartida/2026-11-12_claude-puede-hacer-qa
autor: claude
fecha: 2026-11-12
tipo: regla
etiquetas: [qa, operador, flujo]
fuente: el operador, en el chat del 12-11-2026
vigencia: vigente
---

El operador, el 12-11-2026, mientras Claude implementaba las rondas r03 de T-75 y T-76: «sí que puedes hacer las QAs de cualquier cosa».

- **Qué cambia:** Claude puede hacer la QA de cualquier ticket, también de los que ha implementado él. Hasta ese día la QA la hacía el agente que no implementó (`.docs/knowledge/02_flujo-de-trabajo.md`).
- **Cómo se aplica:** para conservar la independencia, la QA de algo que implementó Claude la hace **un revisor nuevo sin contexto**: un subagente al que se da solo el ticket y el código, nunca las conclusiones de quien implementó. Sigue la skill `ri-qa`: reproducir desde limpio, intentar romperlo y dar un veredicto binario en `qa.md`. Como hasta ahora, cada ronda la hace un revisor nuevo.
- **Lo que no cambia:** Astra solo hace las tareas que el operador le asigne (`compartida/2026-11-12_tareas-de-astra`).
- **Matiza** lo que dice `compartida/2026-11-12_tareas-de-astra` en «Consecuencia» («Claude no hace la QA de lo suyo»): eso ya no vale.
