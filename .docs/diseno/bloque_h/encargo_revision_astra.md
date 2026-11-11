# Encargo a Astra: revisión independiente de la propuesta de diseño del Bloque H

De: Claude, por indicación del operador (11-11-2026). Para: Astra.

## Qué se te pide

Revisar de forma independiente `.docs/diseno/bloque_h/propuesta_claude.md`, la propuesta de Claude para el Bloque H (seguimiento de posiciones y condiciones de salida). **Es solo pensamiento de diseño: no escribas código ni documentos dentro de ningún bloque**, ni del marco común.

Es la octava y última revisión del orden natural de los bloques (A, B, C, D, E, F, G, H): va después de la de G (`.docs/diseno/README.md`).

## Cómo hacerlo

1. **Forma tu opinión antes de leer la de Claude.** Lee primero:
   - la Constitución (`sistema_global/constitucion/Constitucion_Global.md`): P6, P18 y P19; §2 (fila de H); §4.2 (estados de la posición y salidas automáticas); §7 (ciclo de vida y deriva de estrategias); §9 (sub-pronósticos, seguimiento de lo descartado);
   - los Documentos 0 de H: `sistema_global/documentos_0/V0.09_H_vigilancia_de_posiciones.md`, `sistema_global/documentos_0/V0.25_T-46_Reapertura_vigilada.md` y `sistema_global/documentos_0/V0.30_T-49_Vigilancia_de_senales_de_H.md`, y el código `sistema_global/marco_comun_c/validador/vigilancia.py`.
2. **Juzga cada decisión de la propuesta** con un veredicto (DE ACUERDO, DE ACUERDO CON CAMBIOS, EN DESACUERDO o NO CONCLUYENTE), el motivo y lo que cambiarías:
   - la pérdida medida en veces la oscilación normal;
   - vigilar el tiempo y el dinero parado, y enviarlo a D;
   - vigilar la deriva de estrategias y la calidad de los fondos;
   - la prioridad de cada revisión (dinero en juego y P18);
   - la tabla por cartera y el ciclo de seis pasos;
   - la frontera entre H (tesis) y E (conjunto).
3. **Busca en particular:**
   - si la pausa anticipada de estrategias (caída peor que la peor del backtest) es razonable o pausaría demasiado;
   - qué prueba estadística usarías para la deriva con pocas operaciones;
   - si alguna propuesta da a H un poder de venta que la Constitución no le da (§4.2);
   - conflictos con la Constitución que la propuesta no haya visto.
4. **Propón lo que falte**, con su efecto en la rentabilidad, en las falsas alarmas y en el consumo de los bloques que reciben las revisiones.
5. **Responde a las cinco preguntas** del §9 de la propuesta, en una o dos frases cada una, sin decidir por el operador.

## Entregable

Un fichero llamado «revision_astra.md», en esta misma carpeta, con un resumen de 5 líneas, la tabla de veredictos, tus mejoras y tus respuestas.

Después:
- añade una línea al diario (`.docs/scripts/diario.sh "Revisión de la propuesta del Bloque H" astra`);
- haz commit en develop con `.docs/scripts/commit.sh`, sin tocar ningún bloque ni el marco común;
- avisa al operador.

## Reglas

- No cambies nada de `bloque_a/`, `bloque_a_forex/`, `bloque_b/` ni `sistema_global/`.
- Repositorio público: sin secretos ni datos personales.
