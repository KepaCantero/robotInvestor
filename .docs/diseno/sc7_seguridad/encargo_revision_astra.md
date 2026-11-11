# Encargo a Astra: revisión independiente de la propuesta de diseño de SC-7 (seguridad y operación)

De: Claude, por indicación del operador (11-11-2026). Para: Astra.

## Qué se te pide

Revisar de forma independiente `.docs/diseno/sc7_seguridad/propuesta_claude.md`, la propuesta de Claude para el servicio común SC-7 (seguridad) y la operación del robot. **Es solo pensamiento de diseño: no escribas código ni documentos dentro de ningún bloque**, ni del marco común.

Va después de la revisión de SC-10 y antes de la enmienda 4: es la decimoctava de la lista.

## Cómo hacerlo

1. **Forma tu opinión antes de leer la de Claude.** Lee primero:
   - la Constitución (`sistema_global/constitucion/Constitucion_Global.md`): §12 entero, §8 (kill-switch y vigilante), §11 (fallos e incidentes) y el modo hibernación del §6;
   - los Documentos 0 de persistencia y firma (`sistema_global/documentos_0/V0.42_T-03_Persistencia_del_estado.md`, `sistema_global/documentos_0/V0.45_T-03_Firma_con_clave.md` y `sistema_global/documentos_0/V0.49_T-03_Rotacion_de_la_clave.md`);
   - las filas T-01 y T-30 de la deuda técnica.
2. **Juzga cada decisión** con un veredicto (DE ACUERDO, DE ACUERDO CON CAMBIOS, EN DESACUERDO o NO CONCLUYENTE), el motivo y lo que cambiarías:
   - las cuatro zonas de confianza;
   - dónde corre el robot y el vigilante en otra máquina;
   - la tabla de claves y la bóveda;
   - las copias, cuánto se puede perder y la prueba mensual;
   - la carta de instrucciones;
   - las actualizaciones y los simulacros.
3. **Busca en particular:**
   - amenazas que falten en la tabla del §2;
   - si el vigilante en otra máquina introduce un riesgo nuevo (sus propias credenciales, falsas alarmas);
   - si «perder como mucho un día» es coherente con lo que G necesita para conciliar;
   - conflictos con la Constitución que la propuesta no haya visto.
4. **Propón lo que falte.**
5. **Responde a las seis preguntas** del §10 de la propuesta, sin decidir por el operador.

## Entregable

Un fichero llamado «revision_astra.md», en esta misma carpeta, con un resumen de 5 líneas, la tabla de veredictos, tus mejoras y tus respuestas. Después, el diario (`.docs/scripts/diario.sh "Revisión de la propuesta de SC-7" astra`), el commit con `.docs/scripts/commit.sh` sin tocar ningún bloque ni el marco común, y el aviso al operador.

## Reglas

- No cambies nada de `bloque_a/`, `bloque_a_forex/`, `bloque_b/` ni `sistema_global/`.
- Repositorio público: sin secretos ni datos personales.
