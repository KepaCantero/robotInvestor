# Encargo a Astra: revisión independiente de la propuesta de diseño del Broker Personal

De: Claude, por indicación del operador (11-11-2026). Para: Astra.

## Qué se te pide

Revisar de forma independiente `.docs/diseno/broker_personal/propuesta_claude.md`, la propuesta de Claude para el Broker Personal (conversacional, Orquestador, gestores de cartera y las funciones que propone la enmienda 4). **Es solo pensamiento de diseño: no escribas código ni documentos dentro de ningún bloque**, ni del marco común.

Va después de la revisión de N y antes de la enmienda 4: es la decimocuarta de la lista.

## Cómo hacerlo

1. **Forma tu opinión antes de leer la de Claude.** Lee primero:
   - la Constitución (`sistema_global/constitucion/Constitucion_Global.md`): §2 (el Broker Personal en tres papeles, lo que hace con el operador e intercambio entre bloques, D-21 y D-23), §6 (perfil, controles sobre el operador, hibernación), §7 (aportaciones), §10 (asesor de configuración y cuestionario) y §11 (presupuesto duro);
   - el Documento 0 del Orquestador (`sistema_global/documentos_0/V0.04_Orquestador.md`);
   - los puntos E4-14 a E4-17 de `.docs/diseno/enmienda_4/propuesta_claude.md`;
   - las filas D-05, T-07 y P-07 de la deuda técnica.
2. **Juzga cada decisión** con un veredicto (DE ACUERDO, DE ACUERDO CON CAMBIOS, EN DESACUERDO o NO CONCLUYENTE), el motivo y lo que cambiarías:
   - siete funciones y como mucho tres agentes de IA (perfilador y asesor como modos del conversacional);
   - gestores de cartera en código con IA solo en excepciones;
   - el planificador patrimonial;
   - el orden fijo de prioridades y la puntuación de encargos;
   - el reparto del presupuesto entre carteras;
   - la reutilización de análisis vigentes entre carteras;
   - la resolución de conflictos entre carteras;
   - la memoria sin historial libre y el diario de decisiones;
   - el tope del 10 % del presupuesto de IA para el Broker.
3. **Busca en particular:**
   - si convertir papeles en modos del conversacional contradice D-21 o la enmienda 4;
   - si la afirmación sobre el traspaso de fondos sin tributar en España y la exclusión de la mayoría de ETF es correcta (debe validarla un asesor fiscal, P-06);
   - si reutilizar un análisis de otra cartera puede saltarse un mandato distinto;
   - riesgos de manipulación del conversacional que la propuesta no cubra;
   - conflictos con la Constitución que la propuesta no haya visto.
4. **Propón lo que falte.**
5. **Responde a las seis preguntas** del §11 de la propuesta, sin decidir por el operador.

## Entregable

Un fichero llamado «revision_astra.md», en esta misma carpeta, con un resumen de 5 líneas, la tabla de veredictos, tus mejoras y tus respuestas. Después, el diario (`.docs/scripts/diario.sh "Revisión de la propuesta del Broker Personal" astra`), el commit con `.docs/scripts/commit.sh` sin tocar ningún bloque ni el marco común, y el aviso al operador.

## Reglas

- No cambies nada de `bloque_a/`, `bloque_a_forex/`, `bloque_b/` ni `sistema_global/`.
- Repositorio público: sin secretos ni datos personales.
