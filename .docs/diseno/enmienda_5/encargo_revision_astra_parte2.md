# Encargo a Astra: revisión independiente del borrador de la enmienda 5, parte 2

De: Claude, por indicación del operador (11-11-2026). Para: Astra.

## Qué se te pide

Revisar de forma independiente `.docs/diseno/enmienda_5/propuesta_parte2_claude.md`: el texto con que entraría en la Constitución todo lo que queda de los diseños del 11-11-2026. Son 28 cambios (52 a 79) y 28 decisiones nuevas (D-57 a D-84), todo `[PROPUESTO]`:
- los dieciocho puntos de la enmienda 4 que no entraron en la parte 1;
- los hallazgos de la pasada de coherencia que tocan la Constitución;
- el reequilibrio hacia el plan en F;
- la regla 1 del §5, como variante de la tanda 3.

**Es solo un borrador: no cambies la Constitución ni ningún bloque.**

Se preparó **antes** de tus revisiones de diseño. Por eso cada cambio tiene una casilla «Revisión de Astra» vacía, y el §10 del borrador dice qué cambios puede tocar cada una de tus revisiones. Va **al final de tu lista**, después de la parte 1 (relevo, §0 bis).

## Cómo hacerlo

1. **Forma tu opinión antes de leer la de Claude.** Con la enmienda 4 (`.docs/diseno/enmienda_4/propuesta_claude.md`), la pasada de coherencia (`.docs/diseno/coherencia/propuesta_claude.md`, §3 y §6) y las secciones de la Constitución que tocan, escribe en dos líneas cómo redactarías tú cada punto.
2. **Juzga cada cambio (52 a 79)** con un veredicto (DE ACUERDO, DE ACUERDO CON CAMBIOS, EN DESACUERDO o NO CONCLUYENTE), el motivo y el texto que cambiarías.
3. **Comprueba en particular:**
   - que cada «Antes» cita bien el texto vigente de la V0.6;
   - que el texto recoge lo que dicen tus revisiones de diseño, y que no contradice ninguna decisión ya aceptada en la tanda 1 ni el texto de la parte 1;
   - contradicciones con el resto de la Constitución, sobre todo:
     - el Broker en siete papeles (cambio 73) frente a D-11 y D-21;
     - SC-12 (cambio 57) frente al tope de bloques y frente a K;
     - el canal de avisos (cambio 61) frente a la independencia de F (§8);
     - el reequilibrio (cambio 78) frente a la asimetría del cambio 47 y al kill-switch;
   - que la numeración de contratos CT-G-18 a CT-G-29 no choca con nada que ya uses.
4. **Responde a los trece puntos** del §9 del borrador, en el apartado «Para Astra», sin decidir por el operador.
5. **Revisa el §10:** ¿falta algún cambio de la Constitución que salga de tus revisiones? Si lo hay, propónlo como cambio 80 en adelante.

## Entregable

Un fichero llamado «revision_astra_parte2.md», en esta misma carpeta, con:
- un resumen de 5 líneas;
- la tabla de veredictos;
- el texto que propones donde cambies algo;
- tus respuestas.

Después:
- el diario (`.docs/scripts/diario.sh "Revisión de la enmienda 5, parte 2" astra`);
- el commit con `.docs/scripts/commit.sh`, sin tocar la Constitución ni ningún bloque;
- el aviso al operador.

## Reglas

- No cambies `sistema_global/constitucion/` ni ningún bloque.
- Repositorio público: sin secretos ni datos personales.
