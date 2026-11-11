# Encargo a Astra: revisión independiente de la propuesta de diseño del Bloque M

De: Claude, por indicación del operador (11-11-2026). Para: Astra.

## Qué se te pide

Revisar de forma independiente `.docs/diseno/bloque_m/propuesta_claude.md`, la propuesta de Claude para el Bloque M (riesgo de cartera). **Es solo pensamiento de diseño: no escribas código ni documentos dentro de ningún bloque**, ni del marco común.

Es la duodécima revisión del orden natural de los bloques, después de la de K y antes de la enmienda 4.

## Cómo hacerlo

1. **Forma tu opinión antes de leer la de Claude.** Lee primero la Constitución (`sistema_global/constitucion/Constitucion_Global.md`): §2 (fila de M, D-18), la regla de concentración mínima antes de M (D-25), la tabla de comparativas de D (estrés histórico), D-16, D-32, D-34 y la fila de la Fase 3 de §14. Después, las propuestas de E y F (`.docs/diseno/bloque_e/propuesta_claude.md` y `.docs/diseno/bloque_f/propuesta_claude.md`).
2. **Juzga cada decisión** con un veredicto (DE ACUERDO, DE ACUERDO CON CAMBIOS, EN DESACUERDO o NO CONCLUYENTE), el motivo y lo que cambiarías:
   - la regla de entrada (M solo si el banco demuestra que la comprobación de E se queda corta);
   - las cuatro vistas;
   - la pregunta previa para E;
   - los escenarios hipotéticos y quién los propone y aprueba;
   - la cifra de caída tipo 2008 en la política de inversión personal;
   - la comprobación de excepciones y el aspirante frente al titular en los modelos de riesgo;
   - el aviso cuando M y F discrepan.
3. **Busca en particular:**
   - si el aviso de discrepancia entre M y F rompe de algún modo la independencia de F (P2, P15);
   - si el número de episodios históricos y la cantidad de excepciones esperables bastan para juzgar un modelo de riesgo con los datos de un particular;
   - riesgos de cartera que no cubra ninguna de las cuatro vistas;
   - conflictos con la Constitución que la propuesta no haya visto.
4. **Propón lo que falte.**
5. **Responde a las seis preguntas** del §9 de la propuesta, sin decidir por el operador.

## Entregable

Un fichero llamado «revision_astra.md», en esta misma carpeta, con un resumen de 5 líneas, la tabla de veredictos, tus mejoras y tus respuestas. Después, el diario (`.docs/scripts/diario.sh "Revisión de la propuesta del Bloque M" astra`), el commit con `.docs/scripts/commit.sh` sin tocar ningún bloque ni el marco común, y el aviso al operador.

## Reglas

- No cambies nada de `bloque_a/`, `bloque_a_forex/`, `bloque_b/` ni `sistema_global/`.
- Repositorio público: sin secretos ni datos personales.
