# Encargo a Astra: revisión independiente del rediseño del Bloque B

De: Claude, por indicación del operador (11-11-2026: «modifica la propuesta del bloque B»). Para: Astra.

## Qué se te pide

Revisar de forma independiente `.docs/diseno/bloque_b/propuesta_rediseno_claude.md`, una alternativa más ambiciosa a la evaluación de `.docs/tickets/T-68/evaluacion_claude.md`: de 24 agentes a 5 papeles de IA, coordinación en código y prompts de núcleo común más módulos. **Es solo pensamiento de diseño: `bloque_b/` sigue congelado.**

Hazla **junto con la revisión de T-68** (`.docs/tickets/T-68/encargo_revision_astra.md`): las dos propuestas se discuten a la vez, y las nueve mejoras de T-68 son los primeros pasos del camino de migración del rediseño. Es la segunda revisión del orden natural de los bloques (A, B, C, D, E, F, G, H), después de la de A.

## Cómo hacerlo

1. **Forma tu opinión antes de leer la de Claude**, con las mismas lecturas que el encargo de T-68, más la Constitución: P12, §3 (verificación diversa y lectores aislados) y §10 (economía del análisis).
2. **Juzga cada decisión** con un veredicto (DE ACUERDO, DE ACUERDO CON CAMBIOS, EN DESACUERDO o NO CONCLUYENTE), el motivo y lo que cambiarías:
   - quitar el Director y repartir su trabajo entre el Orquestador (código) y el Analista de ámbito;
   - un Analista de dimensión con módulos en lugar de diez especialistas, y el plan por código de las dimensiones materiales;
   - un Seleccionador con el kit de cada tipo de activo, en Sonnet por defecto;
   - Contradictor de otro proveedor y, en N3, un segundo analista independiente;
   - lo que pasa a código y lo que sale de B;
   - el banco de medida con sus cuatro variantes;
   - el camino de migración por pasos.
3. **Busca en particular:**
   - si las estimaciones de consumo (150.000–200.000 tokens en un N2) se sostienen con los tamaños reales de los prompts del bloque;
   - qué precisión se puede perder al fusionar especialistas, y si la red de seguridad (pedir una dimensión que el plan dejó fuera) basta;
   - si el plan por código puede elegir bien las dimensiones materiales con lo que hay en el encargo;
   - conflictos con la Constitución o con contratos CT-B que la propuesta no haya visto.
4. **Propón lo que falte o un diseño intermedio** si crees que el salto es demasiado grande.
5. **Responde a las cinco preguntas** del §7 de la propuesta, sin decidir por el operador.

## Entregable

Una sección «Rediseño» dentro de tu fichero «revision_astra.md» de T-68 (`.docs/tickets/T-68/`), con un resumen de 5 líneas, la tabla de veredictos, tus mejoras y tus respuestas. Después, el diario, el commit con `.docs/scripts/commit.sh` sin tocar `bloque_b/`, y el aviso al operador, como en T-68.

## Reglas

- No cambies nada de `bloque_b/` ni de su configuración.
- Repositorio público: sin secretos ni datos personales.
