# Encargo a Astra: revisión independiente del rediseño del Bloque A

De: Claude, por indicación del operador (11-11-2026: revisar «si en la construcción del bloque A también has sido conservador»). Para: Astra.

## Qué se te pide

Revisar de forma independiente `.docs/diseno/bloque_a/propuesta_claude.md`: de 25 agentes a 6 papeles de IA, con coordinación en código, puerta GC1 por código antes de la IA y prompts de núcleo común más kits. Retoma PA-06 y PA-07 de T-53, aplazadas en T-67. **Es solo pensamiento de diseño: no cambies prompts, papeles ni código de `bloque_a/` por este encargo.** Tus tareas de A del relevo (T-93, T-91 y T-88) siguen como están.

Es la primera revisión del orden natural de los bloques (A, B, C, D, E, F, G, H), que fijó el operador el 11-11-2026.

## Cómo hacerlo

1. **Forma tu opinión antes de leer la de Claude.** Lee primero:
   - `bloque_a/08_Arquitectura/Arquitectura del Bloque A - Descripción detallada para LLM - V4.0.md` (agentes y flujo);
   - `bloque_a/11_Ejecutor/config/por_defecto.yaml` (modelos y `perfiles.activos`);
   - `.docs/tickets/T-53/propuestas.md` (PA-04 a PA-07 y PA-14) y la fila T-67 de la deuda técnica;
   - la Constitución: P12, §3 (verificación diversa) y §10 (economía del análisis).
2. **Reproduce la medida.** Desde `bloque_a/11_Ejecutor`, ejecuta `.docs/scripts/medir_consumo_a.py` (uso en su cabecera) dos veces: con la configuración por defecto (solo divisas) y con un YAML que active los doce perfiles (`perfiles: {activos: [RV, RF, DIV, MP, IDX, FON, DER, INM, CRI, ALT, MON, TCV]}`) pasado con `--config`. Comprueba las 8 y las 77 llamadas, los 184.000 y 1.662.000 tokens de entrada y el reparto por agente.
3. **Juzga cada decisión** con un veredicto (DE ACUERDO, DE ACUERDO CON CAMBIOS, EN DESACUERDO o NO CONCLUYENTE), el motivo y lo que cambiarías:
   - un Analista de perfil con kits en lugar de doce analistas;
   - Prospectiva una vez por ciclo;
   - Contradictor solo para las finalistas que van a ser encargo, en una ronda;
   - Sintetizador (Analizador y Redactor juntos);
   - lo que pasa a código (GC1, G3, coordinación, curación, auditoría) y lo que sale de A;
   - el banco de medida y el camino por pasos.
4. **Busca en particular:** qué se pierde al quitar la refutación de las finalistas que no serán encargo; si una sola llamada de Prospectiva para todas las finalistas cabe en contexto y mantiene la calidad; conflictos con los contratos CT-01 a CT-25 o con la Constitución.
5. **Responde a las cuatro preguntas** del §6 de la propuesta, sin decidir por el operador.

## Entregable

Un fichero llamado «revision_astra.md», en esta misma carpeta, con un resumen de 5 líneas, la reproducción de la medida, la tabla de veredictos, tus mejoras y tus respuestas. Después, el diario (`.docs/scripts/diario.sh "Revisión del rediseño del Bloque A" astra`), el commit con `.docs/scripts/commit.sh` y el aviso al operador.

## Reglas

- No cambies nada de `bloque_a/`, `bloque_a_forex/`, `bloque_b/` ni `sistema_global/` por este encargo.
- Repositorio público: sin secretos ni datos personales.
