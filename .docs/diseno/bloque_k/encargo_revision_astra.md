# Encargo a Astra: revisión independiente de la propuesta de diseño del Bloque K

De: Claude, por indicación del operador (11-11-2026). Para: Astra.

## Qué se te pide

Revisar de forma independiente `.docs/diseno/bloque_k/propuesta_claude.md`, la propuesta de Claude para el Bloque K (datos y calidad de datos). **Es solo pensamiento de diseño: no escribas código ni documentos dentro de ningún bloque**, ni del marco común.

Es la undécima revisión del orden natural de los bloques, después de la de J y antes de la enmienda 4.

## Cómo hacerlo

1. **Forma tu opinión antes de leer la de Claude.** Lee primero:
   - la Constitución (`sistema_global/constitucion/Constitucion_Global.md`): §2 (fila de K y D-18), §3 (SC-2, SC-10, SC-11 y registros comunes) y §10 entero;
   - el Documento 0 de K (`sistema_global/documentos_0/V0.03_K_datos_de_corte_y_calendario.md`) y su código de calidad (`sistema_global/marco_comun_c/validador/k_calidad.py`);
   - las filas T-86 y D-29 de la deuda técnica.
2. **Juzga cada decisión** con un veredicto (DE ACUERDO, DE ACUERDO CON CAMBIOS, EN DESACUERDO o NO CONCLUYENTE), el motivo y lo que cambiarías:
   - las dos fechas por dato;
   - el catálogo de necesidades y sus fuentes candidatas;
   - las comprobaciones de calidad nuevas (di cuáles ya cubren Q-01 a Q-15);
   - la regla de degradación;
   - la política de fuentes, coste y licencias.
3. **Busca en particular:** fuentes candidatas mal elegidas o con licencias problemáticas; datos que necesite algún bloque y no estén en el catálogo; si la tolerancia propuesta para el contraste de tipos de cambio es razonable; conflictos con la Constitución.
4. **Propón lo que falte.**
5. **Responde a las cinco preguntas** del §9 de la propuesta, sin decidir por el operador.

## Entregable

Un fichero llamado «revision_astra.md», en esta misma carpeta, con un resumen de 5 líneas, la tabla de veredictos, tus mejoras y tus respuestas. Después, el diario (`.docs/scripts/diario.sh "Revisión de la propuesta del Bloque K" astra`), el commit con `.docs/scripts/commit.sh` sin tocar ningún bloque ni el marco común, y el aviso al operador.

## Reglas

- No cambies nada de `bloque_a/`, `bloque_a_forex/`, `bloque_b/` ni `sistema_global/`.
- Repositorio público: sin secretos ni datos personales.
