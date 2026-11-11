# Encargo a Astra: revisión independiente de la propuesta de diseño del Bloque E

De: Claude, por indicación del operador (11-11-2026). Para: Astra.

## Qué se te pide

Revisar de forma independiente `.docs/diseno/bloque_e/propuesta_claude.md`, la propuesta de Claude para el Bloque E (construir carteras, dimensionar y supervisar en conjunto). **Es solo pensamiento de diseño: no escribas código ni documentos dentro de ningún bloque**, ni del marco común.

Va después de la revisión del Bloque D (`.docs/diseno/bloque_d/encargo_revision_astra.md`), porque D y E comparten la función objetivo; revisa las dos con eso en mente.

## Cómo hacerlo

1. **Forma tu opinión antes de leer la de Claude.** Lee primero:
   - la Constitución (`sistema_global/constitucion/Constitucion_Global.md`): §2 (filas de E, F, M y H), §4 (vía sistemática J → E → F → G), §7 (carteras, mandatos, rentabilidad mínima, plan de largo plazo y supervisión global) y §8 (controles de F);
   - el Documento 0 del E actual (`sistema_global/documentos_0/V0.10_E_dimensionado.md`) y su código (`sistema_global/marco_comun_c/validador/dimensionado.py`).
2. **Juzga cada decisión de la propuesta** con un veredicto (DE ACUERDO, DE ACUERDO CON CAMBIOS, EN DESACUERDO o NO CONCLUYENTE), el motivo y lo que cambiarías:
   - las tres capas (plan base, posiciones activas, vista global);
   - la regla de fondo: dimensionar con el riesgo y usar la rentabilidad estimada solo para inclinar;
   - Kelly fraccional sobre la estimación prudente de D, y la fracción de un cuarto como punto de partida;
   - la tabla por cartera (trading, táctica, largo plazo);
   - el ciclo de cinco pasos y sus cuatro entradas;
   - las fronteras con D, F, M, H y G;
   - consumo cero y validación con datos históricos.
3. **Busca en particular:**
   - errores en la tabla de Kelly o en sus supuestos (ventaja conocida, aproximación de media menos media varianza, apuestas repetidas);
   - qué pasa con varias posiciones correlacionadas a la vez (Kelly de cartera frente a Kelly por posición);
   - si el ajuste a la volatilidad o el freno por caída pueden empeorar el resultado y cuándo;
   - la regla fiscal española citada (FIFO, regla de los dos meses): si está bien descrita; no la resuelvas tú, márcala para el asesor (P-06);
   - conflictos con la Constitución que la propuesta no haya visto.
4. **Propón lo que falte**, con su efecto en precisión y en consumo.
5. **Responde a las siete preguntas** del §9 de la propuesta, en una o dos frases cada una, sin decidir por el operador.

## Entregable

Un fichero llamado «revision_astra.md», en esta misma carpeta, con un resumen de 5 líneas, la tabla de veredictos, tus mejoras y tus respuestas.

Después:
- añade una línea al diario (`.docs/scripts/diario.sh "Revisión de la propuesta del Bloque E" astra`);
- haz commit en develop con `.docs/scripts/commit.sh`, sin tocar ningún bloque ni el marco común;
- avisa al operador.

## Reglas

- No cambies nada de `bloque_a/`, `bloque_a_forex/`, `bloque_b/` ni `sistema_global/`.
- Si algo de la propuesta contradice la Constitución, dilo con la cita.
- Repositorio público: sin secretos ni datos personales.
