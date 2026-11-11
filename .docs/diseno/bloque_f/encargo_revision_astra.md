# Encargo a Astra: revisión independiente de la propuesta de diseño del Bloque F

De: Claude, por indicación del operador (11-11-2026). Para: Astra.

## Qué se te pide

Revisar de forma independiente `.docs/diseno/bloque_f/propuesta_claude.md`, la propuesta de Claude para el Bloque F (control determinista e independiente). **Es solo pensamiento de diseño: no escribas código ni documentos dentro de ningún bloque**, ni del marco común. T-74 (controles de F que faltan) sigue en espera.

Va después de las revisiones de D y E (`.docs/diseno/README.md`).

## Cómo hacerlo

1. **Forma tu opinión antes de leer la de Claude.** Lee primero:
   - la Constitución (`sistema_global/constitucion/Constitucion_Global.md`): P1, P2, P8, P15 y P20; §6 (autonomía y anulaciones); §7 (contrapesos de la abstención, rentabilidad mínima y supervisión global); §8 entero; §11 (desencadenantes del kill-switch);
   - el Documento 0 del F actual (`sistema_global/documentos_0/V0.07_F_control_de_riesgo.md`) y su código (`sistema_global/marco_comun_c/validador/control_f.py`, reglas F-01 a F-23 y CF-01 a CF-09);
   - la fila T-74 de la deuda técnica.
2. **Juzga cada decisión de la propuesta** con un veredicto (DE ACUERDO, DE ACUERDO CON CAMBIOS, EN DESACUERDO o NO CONCLUYENTE), el motivo y lo que cambiarías:
   - la asimetría por tipo de acción (abrir o aumentar, reequilibrar, reducir o cerrar, proteger);
   - la exención del reequilibrio al plan de los límites de pérdida y las ventanas de eventos;
   - una política por cartera y los tres niveles de límite;
   - el estado de cartera leído solo del libro conciliado de G;
   - la exposición compartida mirando dentro de los fondos, y la regla prudente sin composición;
   - reducir en lugar de vetar en táctica cuando el evento es el catalizador;
   - la cuenta de I (coste de los vetos, lo evitado, uso de los límites) y la batería permanente de ataque.
3. **Busca en particular:**
   - formas de abusar de la asimetría: por ejemplo, disfrazar un aumento de riesgo de «reequilibrio» o de «protección», o cerrar y reabrir para esquivar límites;
   - si alguna propuesta contradice la Constitución (por ejemplo, P20 o el kill-switch del §8) y con qué cita;
   - si la tabla de pérdidas y recuperación y el razonamiento de «cortar las colas» se sostienen;
   - controles que falten y que no estén en T-74.
4. **Propón lo que falte**, con su efecto en la protección y en los vetos de más.
5. **Responde a las seis preguntas** del §9 de la propuesta, en una o dos frases cada una, sin decidir por el operador.

## Entregable

Un fichero llamado «revision_astra.md», en esta misma carpeta, con un resumen de 5 líneas, la tabla de veredictos, tus mejoras y tus respuestas.

Después:
- añade una línea al diario (`.docs/scripts/diario.sh "Revisión de la propuesta del Bloque F" astra`);
- haz commit en develop con `.docs/scripts/commit.sh`, sin tocar ningún bloque ni el marco común;
- avisa al operador.

## Reglas

- No cambies nada de `bloque_a/`, `bloque_a_forex/`, `bloque_b/` ni `sistema_global/`.
- Repositorio público: sin secretos ni datos personales.
