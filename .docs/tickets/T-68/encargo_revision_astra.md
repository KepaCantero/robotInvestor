# Encargo a Astra: revisión independiente de la evaluación del Bloque B

De: Claude, por indicación del operador (11-11-2026: «Me gustaría que tus propuestas para el bloque B fuesen evaluadas por Astra»). Para: Astra.

## Qué se te pide

Revisar de forma independiente `.docs/tickets/T-68/evaluacion_claude.md`, que contiene la evaluación de Claude del Bloque B (precisión frente a consumo de tokens) y nueve mejoras propuestas. El operador quiere decidir la arquitectura de B y de los demás bloques con las dos opiniones delante. **No es una QA de código ni hay nada que implementar**: el Bloque B sigue congelado (relevo, §0 bis), y esta revisión es solo lectura, medición y opinión.

Tiene prioridad sobre las demás tareas de tu relevo.

## Cómo hacerlo

1. **Forma tu opinión antes de leer la de Claude.** Lee primero, en este orden:
   - `bloque_b/08_Arquitectura/Arquitectura del Bloque B - Descripción detallada para LLM - V2.0.md`;
   - `bloque_b/11_Ejecutor/config/por_defecto.yaml` (modelos, `max_tokens`, `llm.cache_ttl`);
   - `bloque_b/11_Ejecutor/bloque_b/prompts.py` (`Prompts.system`) y `bloque_b/11_Ejecutor/bloque_b/agentes.py`;
   - la Constitución, §2 (mapa de bloques).

   Anota qué mejoras propondrías tú. Después, lee la evaluación de Claude.
2. **Reproduce las cifras.** Desde `bloque_b/11_Ejecutor`, ejecuta `.docs/scripts/medir_consumo_b.py` sobre `ejemplos/peticiones/peticion_redes_bloque_a.json`, `peticion_india.json` y `peticion_cobre.json` (el uso exacto está en la cabecera del script). Comprueba:
   - las llamadas por análisis (27 a 29);
   - el 96 % de entrada en prompts de sistema;
   - el reparto por agente;
   - el 35 % de playbooks ajenos del Seleccionador;
   - el 24 % a 34 % del marco común en los especialistas;
   - el cálculo de costes de la tabla «Consumo medido».

   Usa los precios de la documentación oficial de Anthropic que cita la evaluación, no de memoria.
3. **Juzga cada mejora (1 a 9).** Para cada una, da:
   - un veredicto: DE ACUERDO, DE ACUERDO CON CAMBIOS, EN DESACUERDO o NO CONCLUYENTE;
   - el motivo;
   - lo que cambiarías;
   - si su efecto en tokens o en precisión está bien estimado.

   Busca en particular:
   - supuestos sin respaldo (por ejemplo, el «Director un 30 % más corto por fase» o que los prompts por módulos mejoran la precisión);
   - efectos que Claude no ha visto: el coste de la salida, las rondas reales de los especialistas o la latencia;
   - riesgos para la precisión de cada recorte.
4. **Propón lo que falte.** Mejoras que Claude no ha visto, o un orden distinto. Ten en cuenta que el objetivo del operador es «la mejor relación precisión/consumo de tokens».
5. **Responde a las nueve preguntas de arquitectura** con tu opinión, en una o dos frases cada una, sin decidir por el operador.

## Entregable

El fichero «revision_astra.md», dentro de esta misma carpeta del ticket, con:
- un resumen de 5 líneas;
- la reproducción de las cifras (lo que coincide y lo que no, con tus números);
- la tabla de veredictos por mejora;
- tus mejoras nuevas;
- tus respuestas a las preguntas.

Después:
- añade una línea al diario (`.docs/scripts/diario.sh "Revisión de la evaluación del Bloque B" astra`);
- haz commit en develop con `.docs/scripts/commit.sh`, sin tocar `bloque_b/`;
- avisa al operador.

## Reglas

- No cambies nada de `bloque_b/` ni de su configuración.
- Si las cifras no se reproducen, dilo con tus números; no ajustes las de Claude.
- Repositorio público: sin secretos ni datos personales.
