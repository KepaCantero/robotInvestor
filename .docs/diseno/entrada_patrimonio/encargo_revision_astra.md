# Encargo a Astra: revisión independiente de la propuesta de entrada del dinero existente

De: Claude, por indicación del operador (11-11-2026). Para: Astra.

## Qué se te pide

Revisar de forma independiente `.docs/diseno/entrada_patrimonio/propuesta_claude.md`, la propuesta de Claude para pasar al robot el patrimonio que el operador ya tiene. **Es solo pensamiento de diseño: no escribas código ni documentos dentro de ningún bloque**, ni del marco común. Tampoco es asesoramiento fiscal.

Va después de la revisión de SC-7 y antes de la enmienda 4: es la decimonovena de la lista.

## Cómo hacerlo

1. **Forma tu opinión antes de leer la de Claude.** Lee primero:
   - la Constitución (`sistema_global/constitucion/Constitucion_Global.md`): §7 (aportaciones, vehículo fiscal y freno a la rotación), colchón de emergencia (D-32) y operaciones manuales declaradas (§6);
   - las propuestas de SC-9 (`.docs/diseno/sc9_fiscalidad/propuesta_claude.md`) y del Broker Personal (`.docs/diseno/broker_personal/propuesta_claude.md`).
2. **Juzga cada decisión** con un veredicto (DE ACUERDO, DE ACUERDO CON CAMBIOS, EN DESACUERDO o NO CONCLUYENTE), el motivo y lo que cambiarías:
   - el inventario y las posiciones externas;
   - el árbol de decisión por posición;
   - el orden de los pasos;
   - de golpe o por tramos, y cómo se presenta;
   - que la sombra arranque con el mismo patrimonio y calendario.
3. **Busca en particular:**
   - tipos de producto que falten en el inventario;
   - si el estudio de Vanguard citado (68 % a favor de invertir de golpe) está bien usado;
   - riesgos de cargar lotes con fechas o precios de compra erróneos;
   - conflictos con la Constitución que la propuesta no haya visto.
4. **Propón lo que falte.**
5. **Responde a las cinco preguntas** del §9 de la propuesta, sin decidir por el operador.

## Entregable

Un fichero llamado «revision_astra.md», en esta misma carpeta, con un resumen de 5 líneas, la tabla de veredictos, tus mejoras y tus respuestas. Después, el diario (`.docs/scripts/diario.sh "Revisión de la propuesta de entrada del patrimonio" astra`), el commit con `.docs/scripts/commit.sh` sin tocar ningún bloque ni el marco común, y el aviso al operador.

## Reglas

- No cambies nada de `bloque_a/`, `bloque_a_forex/`, `bloque_b/` ni `sistema_global/`.
- Repositorio público: sin secretos ni datos personales.
