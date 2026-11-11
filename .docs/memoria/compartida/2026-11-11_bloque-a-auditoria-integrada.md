---
id: compartida/2026-11-11_bloque-a-auditoria-integrada
autor: claude
fecha: 2026-11-11
tipo: decision
etiquetas: [bloque-a, auditoria, astra, t-92]
fuente: commit 6b26137; .docs/tickets/T-92/; rama astra/bloque-a-integridad-y-evidencia (76b90e6)
vigencia: vigente
---

<Contenido: el hecho, por qué importa y cómo aplicarlo.>

(Contenido completado el 11-11-2026: la entrada se creó con la plantilla vacía.)

- La auditoría de Astra al Bloque A, en la rama `astra/bloque-a-integridad-y-evidencia` y llamada T-87 en esa rama, está integrada en develop como **T-92**, tras cuatro rondas de QA: r01, r02 y r03 NO APTO, y r04 APTO. Incluye:
  - datos y evaluación: base congelada al emitir, CESTA con la composición de la emisión y certificados por método;
  - agentes: caché, filtro R8 de secretos, turnos incompletos, referencias en el corte y tope de ampliación;
  - contratos: CT-01 durable con reconciliación, CT-04, CT-23 y CT-25;
  - almacén: cerrojo entre procesos y sellos de final de cadena.
- A pasó de 326 a 439 pruebas (la línea base de `CLAUDE.md`); ruff bajó a 3072 y mypy de A a 115.
- **Choque de números:** el T-87 de la rama no es el T-87 de develop (SC-5). Al integrar trabajo de otro agente, renumerar siempre contra la deuda técnica.
- **La rama no se fusiona entera:** `preparar-encargo-b` se queda en ella para la Fase 6, y C6 ya estaba cubierto en develop.
- **Pendientes:** los hallazgos medios y bajos de la r04 (H-32 a H-39) en T-93; INC-T92-01 (tope de ampliación) y `senales.umbral_favorable` en T-57.
- **Lección del filtro R8:** detectar claves «sk-» por la forma de la clave daba falsos positivos y luego falsos negativos; funciona reconociendo la forma del texto.
