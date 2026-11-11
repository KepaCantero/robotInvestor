# Encargo a Astra: revisión independiente de la propuesta de diseño de SC-10 (intermediario y adaptadores)

De: Claude, por indicación del operador (11-11-2026). Para: Astra.

## Qué se te pide

Revisar de forma independiente `.docs/diseno/sc10_intermediario/propuesta_claude.md`, la propuesta de Claude para el servicio común SC-10 (adaptadores, simulador y elección del intermediario). **Es solo pensamiento de diseño: no escribas código ni documentos dentro de ningún bloque**, ni del marco común. Los ejemplos de entidades no son una recomendación.

Va después de la revisión del Motor (SC-3) y antes de la enmienda 4: es la decimoséptima de la lista.

## Cómo hacerlo

1. **Forma tu opinión antes de leer la de Claude.** Lee primero:
   - la Constitución (`sistema_global/constitucion/Constitucion_Global.md`): fila de SC-10 en §3, D-08 y D-41 (adaptadores), §8 (órdenes de protección y kill-switch), §11 (permisos y claves) y la fila de la Fase 3 de §14;
   - la propuesta de G (`.docs/diseno/bloque_g/propuesta_claude.md`), sobre todo sus preguntas sobre el intermediario;
   - las filas T-14, T-01, T-30 y P-05 de la deuda técnica.
2. **Juzga cada decisión** con un veredicto (DE ACUERDO, DE ACUERDO CON CAMBIOS, EN DESACUERDO o NO CONCLUYENTE), el motivo y lo que cambiarías:
   - los criterios y sus pesos por cartera;
   - dos intermediarios como opción por defecto;
   - el largo plazo en L1 manual con importación de extractos;
   - los siete puertos y sus reglas;
   - la escalera de cinco peldaños;
   - qué hacer si el intermediario cae.
3. **Busca en particular:**
   - datos de las entidades de ejemplo (§6) que estén mal o desactualizados;
   - si la regla de «estado desconocido» basta para evitar órdenes duplicadas;
   - riesgos de tener dos entidades (conciliación, fiscalidad, el mismo valor en dos sitios);
   - conflictos con la Constitución que la propuesta no haya visto.
4. **Propón lo que falte.**
5. **Responde a las seis preguntas** del §10 de la propuesta, sin decidir por el operador.

## Entregable

Un fichero llamado «revision_astra.md», en esta misma carpeta, con un resumen de 5 líneas, la tabla de veredictos, tus mejoras y tus respuestas. Después, el diario (`.docs/scripts/diario.sh "Revisión de la propuesta de SC-10" astra`), el commit con `.docs/scripts/commit.sh` sin tocar ningún bloque ni el marco común, y el aviso al operador.

## Reglas

- No cambies nada de `bloque_a/`, `bloque_a_forex/`, `bloque_b/` ni `sistema_global/`.
- Repositorio público: sin secretos ni datos personales.
