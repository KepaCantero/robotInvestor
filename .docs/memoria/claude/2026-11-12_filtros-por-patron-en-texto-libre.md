---
id: claude/2026-11-12_filtros-por-patron-en-texto-libre
autor: claude
fecha: 2026-11-12
tipo: leccion
etiquetas: [bloque_a, v6, r13, r21, qa]
fuente: .docs/tickets/T-101/qa.md (rondas r01 a r03), bloque_a/11_Ejecutor/bloque_a/diseno_v6.py
vigencia: vigente
---

En T-101, el filtro R13/R21 de los textos del Sintetizador se rehízo dos veces con expresiones regulares, y cada QA encontró casos nuevos.
- **r01:** no había filtro.
- **r02:** el filtro dejaba pasar el ejemplo de la QA y tiraba «vender USD».
- **r03:** tiraba frases normales («opciones», EURUSD, WTI) y dejaba pasar «vender las acciones de TSLA».

**Por qué importa.** Sobre texto libre, un patrón o se pasa o se queda corto. Además, como un solo fallo hace caer el bloque entero de textos, un falso positivo degrada todo el informe.

**Cómo aplicarlo.**
- Ante un control de forma sobre texto libre, decidir primero la unidad (la frase, no el bloque) y la fuente de las listas (códigos y nombres en K).
- Hacer la validación una vez y para todos los diseños, en HT-09.
- Medir el filtro con un conjunto fijo de frases legítimas y prohibidas desde la primera ronda, como el de `.docs/tickets/T-101/revisores/r03_ataques_v6.py`.
- Declarar lo que no detecta.
