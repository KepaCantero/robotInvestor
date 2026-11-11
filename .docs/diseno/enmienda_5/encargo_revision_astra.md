# Encargo a Astra: revisión independiente del borrador de la enmienda 5, parte 1

De: Claude, por indicación del operador (11-11-2026). Para: Astra.

## Qué se te pide

Revisar de forma independiente `.docs/diseno/enmienda_5/propuesta_claude.md`: el texto con que entrarían en la Constitución las ocho decisiones de la tanda 1, que el operador aceptó como rumbo el 11-11-2026 (`.docs/diseno/decisiones_operador.md`). Son nueve cambios (43 a 51) y nueve decisiones nuevas (D-48 a D-56). **Es solo un borrador: no cambies la Constitución ni ningún bloque.**

Es la **última** revisión de tu lista, después de la pasada de coherencia (relevo, §0 bis), porque redacta lo que salga de todas. Si alguna de tus revisiones anteriores discrepa de una decisión de la tanda 1, este es el sitio para recordarlo.

## Cómo hacerlo

1. **Forma tu opinión antes de leer la de Claude.** Con la tabla de la tanda 1 de `decisiones_operador.md` y las secciones de la Constitución que tocan (§2, §3, §5, §8, §9, §10, §14 y §15), escribe en dos líneas cómo redactarías tú cada decisión.
2. **Juzga cada cambio (43 a 51)** con un veredicto (DE ACUERDO, DE ACUERDO CON CAMBIOS, EN DESACUERDO o NO CONCLUYENTE), el motivo y el texto que cambiarías.
3. **Comprueba en particular:**
   - que cada «Antes» cita bien el texto vigente de la V0.6;
   - que ningún «Después» decide algo que el operador no decidió, salvo lo marcado `[PROPUESTO]`;
   - contradicciones con el resto de la Constitución, sobre todo la asimetría de F (cambio 47) frente a la matriz del §6, el kill-switch del §8 y el §11, y la rebanada de largo plazo (cambio 45) frente a D-09, D-19 y las compuertas;
   - los riesgos de seguridad de la asimetría (punto 3 del §6 del borrador);
   - que las decisiones de la tanda 1 que no cambian la Constitución no se hayan quedado fuera.
4. **Responde a los once puntos** del §6 del borrador, sin decidir por el operador.
5. **Revisa la lista de la parte 2** (§7): ¿falta algo que ya sepas por tus revisiones?

## Entregable

Un fichero llamado «revision_astra.md», en esta misma carpeta, con un resumen de 5 líneas, la tabla de veredictos, el texto que propones donde cambies algo y tus respuestas. Después, el diario (`.docs/scripts/diario.sh "Revisión de la enmienda 5, parte 1" astra`), el commit con `.docs/scripts/commit.sh` sin tocar la Constitución ni ningún bloque, y el aviso al operador.

## Reglas

- No cambies `sistema_global/constitucion/` ni ningún bloque.
- Repositorio público: sin secretos ni datos personales.
