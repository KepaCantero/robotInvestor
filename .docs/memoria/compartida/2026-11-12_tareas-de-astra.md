---
id: compartida/2026-11-12_tareas-de-astra
autor: claude
fecha: 2026-11-12
tipo: regla
etiquetas: [astra, cola, operador]
fuente: .docs/tickets/_relevo/cola_astra.md (operador, 12-11-2026)
vigencia: vigente
---

El operador, el 12-11-2026: «Ya no quiero que realice las QA de las T-XX que faltan ni sus implementaciones. También quiero que elimines las 2 últimas tareas que has creado. A partir de ahora yo te diré qué tareas quiero que realice Astra.»

- **Cómo se aplica:** solo el operador añade o retira tareas de Astra en `.docs/tickets/_relevo/cola_astra.md`. Claude no añade ninguna por su cuenta; si cree que conviene, se lo propone al operador.
- **Estado de la cola ese día:** quedan las 23 revisiones de diseño (C-01 a C-23). Las QA de T-83, T-84, T-93, T-94, T-95, T-96, T-97 y T-99, las implementaciones de T-75, T-76, T-91 y T-88, y las dos tareas que Claude había añadido (C-35, borradores de contratos, y C-36, QA de T-99) están en `RETIRADA`; no se borraron porque de `.docs/` no se borra nada.
- **Consecuencia:** esos tickets quedan EN QA con la QA «sin asignar»; quién la hace, si se hace, lo decide el operador. La regla de que la QA la haga el agente que no implementó sigue en pie: Claude no hace la QA de lo suyo. *(Matizado el mismo día: el operador autorizó a Claude a hacer la QA de cualquier cosa; ver `compartida/2026-11-12_claude-puede-hacer-qa`.)*
