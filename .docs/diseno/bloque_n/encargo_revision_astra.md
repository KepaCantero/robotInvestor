# Encargo a Astra: revisión independiente de la propuesta de diseño del Bloque N

De: Claude, por indicación del operador (11-11-2026). Para: Astra.

## Qué se te pide

Revisar de forma independiente `.docs/diseno/bloque_n/propuesta_claude.md`, la propuesta de Claude para el Bloque N (consola del operador). **Es solo pensamiento de diseño: no escribas código ni documentos dentro de ningún bloque**, ni del marco común.

Es la decimotercera revisión del orden natural de los bloques, después de la de M y antes de la enmienda 4.

## Cómo hacerlo

1. **Forma tu opinión antes de leer la de Claude.** Lee primero:
   - la Constitución (`sistema_global/constitucion/Constitucion_Global.md`): §2 (fila de N), §6 (cola de aprobaciones, controles sobre el operador, hibernación y perfil inversor), §8 (kill-switch y vigilante), §11 y la fila de la Fase 3 de §14;
   - los Documentos 0 de N (`sistema_global/documentos_0/V0.06_N_consola_del_operador.md`) y de la aprobación (`sistema_global/documentos_0/V0.19_Aprobacion_y_kill-switch.md`);
   - las filas D-07, D-09, D-19, T-01, T-41, T-50 y T-75 de la deuda técnica.
2. **Juzga cada decisión** con un veredicto (DE ACUERDO, DE ACUERDO CON CAMBIOS, EN DESACUERDO o NO CONCLUYENTE), el motivo y lo que cambiarías:
   - la cifra principal frente a la sombra y no mostrar el largo plazo día a día;
   - las siete pantallas;
   - la comprobación de que el texto del Broker no trae cifras que no estén en pantalla;
   - los tres niveles de aviso y el presupuesto de avisos;
   - la fricción asimétrica;
   - la pantalla contra la venta de pánico sin espera ni bloqueo;
   - medir las intervenciones del operador en I;
   - la tecnología propuesta.
3. **Busca en particular:**
   - si algo de la propuesta pone una espera o un paso de más a una acción que baja el riesgo (la Constitución la permite al momento);
   - si el canal de avisos fuera del chat queda realmente independiente de N;
   - riesgos de seguridad de una web local accesible desde el móvil;
   - si la cifra del «Mind the Gap» citada en el §2 está bien usada;
   - conflictos con la Constitución que la propuesta no haya visto.
4. **Propón lo que falte.**
5. **Responde a las seis preguntas** del §9 de la propuesta, sin decidir por el operador.

## Entregable

Un fichero llamado «revision_astra.md», en esta misma carpeta, con un resumen de 5 líneas, la tabla de veredictos, tus mejoras y tus respuestas. Después, el diario (`.docs/scripts/diario.sh "Revisión de la propuesta del Bloque N" astra`), el commit con `.docs/scripts/commit.sh` sin tocar ningún bloque ni el marco común, y el aviso al operador.

## Reglas

- No cambies nada de `bloque_a/`, `bloque_a_forex/`, `bloque_b/` ni `sistema_global/`.
- Repositorio público: sin secretos ni datos personales.
