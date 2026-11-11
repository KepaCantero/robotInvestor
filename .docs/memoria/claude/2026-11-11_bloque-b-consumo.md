---
id: claude/2026-11-11_bloque-b-consumo
autor: claude
fecha: 2026-11-11
tipo: contexto
etiquetas: [bloque-b, consumo, tokens, t-68]
fuente: .docs/tickets/T-68/evaluacion_claude.md; .docs/scripts/medir_consumo_b.py; commit cc5500f
vigencia: vigente
---

<Contenido: el hecho, por qué importa y cómo aplicarlo.>

(Contenido completado el 11-11-2026: la entrada se creó con la plantilla vacía.)

Medida con el cliente simulado, en tres análisis N2 de ejemplo (redes eléctricas, India y cobre), con `.docs/scripts/medir_consumo_b.py`:
- unos 990.000 tokens de entrada en 27 a 29 llamadas por análisis, de los que unos 950.000 son prompts de sistema (el 96 %);
- el Director (Opus, unos 45.000 tokens por llamada, siete llamadas) es entre el 47 % y el 53 % del coste de entrada;
- la caché de una hora para todos se paga sin leerse: entre 11 y 14 de los 16 o 17 agentes llaman una sola vez;
- el Seleccionador lleva sus doce playbooks y usa uno (sobra el 35 %); los especialistas repiten el marco común (entre el 24 % y el 34 % de su texto).

Por qué importa: el problema de B no es de calidad (176 pruebas en verde, Motor y G3 deterministas), sino de cómo reparte el contexto. Mejoras por orden: banco de medida antes de recortar, prompts por módulos, caché solo en lo que se repite. El rediseño propuesto (cinco papeles de IA, sin Director) está en `.docs/diseno/bloque_b/`; las dos cosas esperan la revisión de Astra.

Cómo aplicarlo: la entrada no depende del modelo, así que estas cifras valen para la API real; la salida y la precisión no se pueden medir en simulado.
