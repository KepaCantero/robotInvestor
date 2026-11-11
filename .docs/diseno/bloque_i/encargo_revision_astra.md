# Encargo a Astra: revisión independiente de la propuesta de diseño del Bloque I

De: Claude, por indicación del operador (11-11-2026). Para: Astra.

## Qué se te pide

Revisar de forma independiente `.docs/diseno/bloque_i/propuesta_claude.md`, la propuesta de Claude para el Bloque I (evaluación y atribución). **Es solo pensamiento de diseño: no escribas código ni documentos dentro de ningún bloque**, ni del marco común.

Es la novena revisión del orden natural de los bloques (A a I), después de la de H y antes de la enmienda 4.

## Cómo hacerlo

1. **Forma tu opinión antes de leer la de Claude.** Lee primero:
   - la Constitución (`sistema_global/constitucion/Constitucion_Global.md`): P8, P17 y P19; §2 (fila de I); §9 entero; §14 (cuándo se construye I);
   - el Documento 0 de la cartera sombra (`sistema_global/documentos_0/V0.71_Cartera_sombra_pasiva.md`) y su código (`sistema_global/marco_comun_c/validador/sombra.py`);
   - las filas T-81, T-82 y T-86 de la deuda técnica.
2. **Juzga cada decisión** con un veredicto (DE ACUERDO, DE ACUERDO CON CAMBIOS, EN DESACUERDO o NO CONCLUYENTE), el motivo y lo que cambiarías:
   - las cuatro preguntas como estructura;
   - la atribución por etapa de decisión con sus alternativas simples;
   - los informes con rangos y «todavía no se sabe»;
   - la referencia ingenua para medir a cada autor;
   - el Redactor de autopsias como única IA;
   - el orden de construcción.
3. **Busca en particular:**
   - errores en la tabla de años necesarios para probar una ventaja, o en sus supuestos;
   - si la atribución por etapa es calculable con los datos que habrá, y cómo tratar la interacción entre etapas;
   - si 200 preguntas de torneo al año y 30 pronósticos por autor son razonables;
   - conflictos con la Constitución que la propuesta no haya visto.
4. **Propón lo que falte**, con su efecto en la precisión y en el consumo.
5. **Responde a las cinco preguntas** del §8 de la propuesta, sin decidir por el operador.

## Entregable

Un fichero llamado «revision_astra.md», en esta misma carpeta, con un resumen de 5 líneas, la tabla de veredictos, tus mejoras y tus respuestas. Después, el diario (`.docs/scripts/diario.sh "Revisión de la propuesta del Bloque I" astra`), el commit con `.docs/scripts/commit.sh` sin tocar ningún bloque ni el marco común, y el aviso al operador.

## Reglas

- No cambies nada de `bloque_a/`, `bloque_a_forex/`, `bloque_b/` ni `sistema_global/`.
- Repositorio público: sin secretos ni datos personales.
