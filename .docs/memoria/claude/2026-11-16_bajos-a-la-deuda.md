---
id: claude/2026-11-16_bajos-a-la-deuda
autor: claude
fecha: 2026-11-16
tipo: leccion
etiquetas: [qa, deuda, tickets]
fuente: Decisiones_del_operador_Bloque_A.md §1 (16-11-2026)
vigencia: vigente
---

**La regla, desde el 16-11-2026, por decisión del operador.** Cuando una QA da APTO:
- Los hallazgos altos y medios abren un ticket que se lleva hasta APTO.
- Los bajos no abren ticket y **tampoco se aplazan**. Se subsanan en el mismo ticket antes de cerrarlo, en una ronda de cierre que comprueba el mismo revisor. En la deuda no se deja ningún bajo abierto.

**Corrección del mismo día.** Propuse que los bajos fueran a la deuda y el operador lo corrigió: «no quiero que los bajos vayan a la deuda; quiero que se subsanen». El nombre del fichero se queda como estaba para no romper el índice.

**Por qué.** Esa noche casi cada ticket APTO dejaba otro ticket de seguimiento, casi siempre de bajos, y la cola no se acababa. Con la ronda de cierre los bajos se arreglan igual, pero sin multiplicar tickets.

**Cómo aplicarlo.**
1. Una QA da APTO con bajos.
2. El implementador hace la ronda de cierre en su misma copia.
3. El revisor comprueba solo esos arreglos.
4. Se cierra el ticket.
