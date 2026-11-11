# Encargo a Astra: revisión independiente de la propuesta de diseño del Bloque D

De: Claude, por indicación del operador (11-11-2026: «En esta parte quiero compartir tus propuestas de diseño de cada bloque con Astra»). Para: Astra.

## Qué se te pide

Revisar de forma independiente `.docs/diseno/bloque_d/propuesta_claude.md`, la propuesta de Claude para el Bloque D (comparar opciones ya analizadas para que el Broker decida). El operador quiere decidir la arquitectura con las dos opiniones delante. **Es solo pensamiento de diseño: no escribas código ni documentos dentro de ningún bloque**, ni del marco común.

Va después de la revisión del Bloque B (`.docs/tickets/T-68/encargo_revision_astra.md`) y antes de tus demás tareas.

El objetivo que fija el operador:
- maximizar la rentabilidad que consigue por cada euro invertido;
- también la máxima rentabilidad a corto plazo;
- que el comparador le sirva para todas las carteras (trading, táctica y largo plazo).

## Cómo hacerlo

1. **Forma tu opinión antes de leer la de Claude.** Lee primero:
   - la Constitución (`sistema_global/constitucion/Constitucion_Global.md`): §2 (fila de D y CT-G-05), §4.1, §5 (capas de CT-G-02 y regla 1), §7 (carteras, mandatos, freno a la rotación y rentabilidad mínima) y los principios P1, P3, P5, P17 y P19;
   - el comparador actual: `sistema_global/marco_comun_c/validador/comparador.py`.

   Anota cómo diseñarías D tú. Después, lee la propuesta.
2. **Juzga cada decisión de la propuesta.** Para cada una, da un veredicto (DE ACUERDO, DE ACUERDO CON CAMBIOS, EN DESACUERDO o NO CONCLUYENTE), el motivo y lo que cambiarías:
   - el objetivo: crecimiento compuesto neto por cartera y por periodo, frente al plan pasivo;
   - un solo comparador con un perfil por cartera, en lugar de tres;
   - las cuatro clases de opción (no hacer nada, candidato, reforzar, sustituir);
   - la estimación prudente encogida hacia la tasa base según el acierto medido por I;
   - la aportación marginal a la cartera al tamaño de referencia de E;
   - la misma ventana para todas las opciones, con el dinero liberado al benchmark;
   - la puerta del extremo bajo del rango y las tres salidas;
   - D y E separados con una función objetivo compartida (Kelly fraccional);
   - consumo cero de tokens en D y aprendizaje vía I.
3. **Busca en particular:**
   - supuestos sin respaldo o cifras que no se sostengan (por ejemplo, el ejemplo del 0,09 % o del 68 % anual);
   - dónde el diseño falla para el corto plazo (trading y táctica): costes, deslizamiento, capacidad, ventajas que se agotan, operaciones simultáneas correlacionadas;
   - qué datos necesita D que hoy no existen (calibración por autor en I, factores en el sobre, modelo de costes por cartera) y en qué orden habría que construirlos;
   - riesgos de que D se abstenga siempre o de que recomiende de más, y cómo detectarlos;
   - conflictos con la Constitución que la propuesta no haya visto.
4. **Propón lo que falte.** Alternativas de diseño que Claude no haya considerado, con su efecto en precisión y en consumo.
5. **Responde a las ocho preguntas** del §9 de la propuesta con tu opinión, en una o dos frases cada una, sin decidir por el operador.

## Entregable

Un fichero llamado «revision_astra.md», en esta misma carpeta, con:
- un resumen de 5 líneas;
- la tabla de veredictos por decisión;
- tus mejoras o alternativas;
- tus respuestas a las preguntas.

Después:
- añade una línea al diario (`.docs/scripts/diario.sh "Revisión de la propuesta del Bloque D" astra`);
- haz commit en develop con `.docs/scripts/commit.sh`, sin tocar ningún bloque ni el marco común;
- avisa al operador.

## Reglas

- No cambies nada de `bloque_a/`, `bloque_a_forex/`, `bloque_b/` ni `sistema_global/`.
- Si algo de la propuesta contradice la Constitución, dilo con la cita; no la reinterpretes.
- Repositorio público: sin secretos ni datos personales.
