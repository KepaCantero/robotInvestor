# Encargo a Astra: revisión independiente de la pasada de coherencia

De: Claude, por indicación del operador (11-11-2026). Para: Astra.

## Qué se te pide

Revisar de forma independiente `.docs/diseno/coherencia/propuesta_claude.md`, la pasada de coherencia de Claude sobre las veinte propuestas de diseño. **Es solo pensamiento de diseño: no escribas código ni documentos dentro de ningún bloque**, ni del marco común.

**Va la última de las revisiones de diseño, después de la enmienda 4,** porque resume todas las anteriores. Después solo queda el borrador de la enmienda 5, parte 1, que redacta en la Constitución lo ya decidido. Hazla cuando hayas revisado las demás: tus propias revisiones son la mejor prueba de si esta pasada se dejó algo.

## Cómo hacerlo

1. **Usa lo que ya sabes de tus revisiones anteriores** y la Constitución (`sistema_global/constitucion/Constitucion_Global.md`), sobre todo §2, §3, §5 y §14.
2. **Juzga cada hallazgo y cada propuesta** con un veredicto (DE ACUERDO, DE ACUERDO CON CAMBIOS, EN DESACUERDO o NO CONCLUYENTE), el motivo y lo que cambiarías:
   - los doce hallazgos del §3;
   - las fichas de los servicios pequeños del §4;
   - el orden por fases y la propuesta sobre el tope de bloques del §5;
   - la lista de dieciséis contratos del §6;
   - las tandas de decisiones del §8.
3. **Busca en particular:**
   - incoherencias que la pasada no vio, sobre todo las que hayan salido en tus revisiones;
   - contratos que falten;
   - preguntas repetidas que no se fusionaron;
   - si la tanda 1 contiene de verdad solo lo que bloquea la Fase 1.
4. **Propón lo que falte** y qué debería entrar en la enmienda 5.

## Entregable

Un fichero llamado «revision_astra.md», en esta misma carpeta, con un resumen de 5 líneas, la tabla de veredictos y tus mejoras. Después, el diario (`.docs/scripts/diario.sh "Revisión de la pasada de coherencia" astra`), el commit con `.docs/scripts/commit.sh` sin tocar ningún bloque ni el marco común, y el aviso al operador.

## Reglas

- No cambies nada de `bloque_a/`, `bloque_a_forex/`, `bloque_b/` ni `sistema_global/`.
- Repositorio público: sin secretos ni datos personales.
