# Encargo a Astra: revisión independiente de la propuesta de diseño del Bloque J

De: Claude, por indicación del operador (11-11-2026). Para: Astra.

## Qué se te pide

Revisar de forma independiente `.docs/diseno/bloque_j/propuesta_claude.md`, la propuesta de Claude para el Bloque J (laboratorio de estrategias, modelos, instrucciones y agentes). **Es solo pensamiento de diseño: no escribas código ni documentos dentro de ningún bloque**, ni del marco común.

Es la décima revisión del orden natural de los bloques, después de la de I y antes de la enmienda 4.

## Cómo hacerlo

1. **Forma tu opinión antes de leer la de Claude.** Lee primero la Constitución (`sistema_global/constitucion/Constitucion_Global.md`): §2 (fila de J), §4.3 (ruta determinista), §7 (ciclo de vida de una estrategia, escalera de verificación y verificaciones externas), §9 (puntos 6, 15, 17 y 18) y §14 (fases), y la fila T-82 de la deuda técnica.
2. **Juzga cada decisión** con un veredicto (DE ACUERDO, DE ACUERDO CON CAMBIOS, EN DESACUERDO o NO CONCLUYENTE), el motivo y lo que cambiarías:
   - «cada intento cuenta» y el registro de experimentos desde la Fase 1;
   - la tabla de cómo se prueba cada tipo de cosa;
   - el peldaño 0 de prerregistro;
   - las diez reglas contra el autoengaño;
   - la ficha de salida;
   - el «descuento» entre backtest y real como medida de J;
   - medir el motor de robotTrading antes de reutilizarlo.
3. **Busca en particular:**
   - si la afirmación de que, con 100 variantes sin ventaja sobre 5 años, la mejor suele mostrar un Sharpe cercano a 1 es correcta como orden de magnitud;
   - si las duraciones y el capital propuestos para los peldaños son razonables;
   - cómo se prueba un prompt o un agente cuando hay pocos casos posteriores a la fecha de corte del modelo;
   - conflictos con la Constitución que la propuesta no haya visto.
4. **Propón lo que falte.**
5. **Responde a las cinco preguntas** del §8 de la propuesta, sin decidir por el operador.

## Entregable

Un fichero llamado «revision_astra.md», en esta misma carpeta, con un resumen de 5 líneas, la tabla de veredictos, tus mejoras y tus respuestas. Después, el diario (`.docs/scripts/diario.sh "Revisión de la propuesta del Bloque J" astra`), el commit con `.docs/scripts/commit.sh` sin tocar ningún bloque ni el marco común, y el aviso al operador.

## Reglas

- No cambies nada de `bloque_a/`, `bloque_a_forex/`, `bloque_b/` ni `sistema_global/`.
- Repositorio público: sin secretos ni datos personales.
