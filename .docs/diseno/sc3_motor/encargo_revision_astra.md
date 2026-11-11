# Encargo a Astra: revisión independiente de la propuesta de diseño del Motor de cálculo (SC-3)

De: Claude, por indicación del operador (11-11-2026). Para: Astra.

## Qué se te pide

Revisar de forma independiente `.docs/diseno/sc3_motor/propuesta_claude.md`, la propuesta de Claude para el servicio común SC-3 (Motor de cálculo avanzado). **Es solo pensamiento de diseño: no escribas código ni documentos dentro de ningún bloque**, ni del marco común.

Va después de la revisión de SC-9 y antes de la enmienda 4: es la decimosexta de la lista.

## Cómo hacerlo

1. **Forma tu opinión antes de leer la de Claude.** Lee primero:
   - la Constitución (`sistema_global/constitucion/Constitucion_Global.md`): P3, la fila de SC-3 en §3 (D-29) y §10 (las cifras las calcula el Motor);
   - el registro del marco (`sistema_global/marco_comun_c/validador/motor.py` y `sistema_global/documentos_0/V0.33_T-26_parte_1_Motor_SC-3_y_advertencias_de_K.md`);
   - el código del Motor de A (`bloque_a/11_Ejecutor/bloque_a/motor/`), solo para saber qué calcula;
   - E4-07 y E4-08 de la enmienda 4 (`.docs/diseno/enmienda_4/propuesta_claude.md`).
2. **Juzga cada decisión** con un veredicto (DE ACUERDO, DE ACUERDO CON CAMBIOS, EN DESACUERDO o NO CONCLUYENTE), el motivo y lo que cambiarías:
   - unir el Motor de A con el registro del marco;
   - el catálogo de doce familias y construir solo lo que pida un Documento 0;
   - el propietario funcional de cada módulo;
   - la ficha y las siete reglas comunes;
   - precisión pedida y método más barato;
   - la caché compartida entre bloques;
   - medir si las bandas aciertan;
   - F fuera del Motor;
   - el orden por fases.
3. **Busca en particular:**
   - módulos que algún diseño de bloque necesite y no estén en el catálogo;
   - si la caché compartida puede mezclar cálculos con fechas de corte distintas;
   - si «F fuera del Motor» deja a F sin alguna cifra que necesite;
   - si las cifras del Bloque A citadas en el §3 (81 fichas, 17 manejadores, 14 citables) siguen siendo correctas;
   - conflictos con la Constitución que la propuesta no haya visto.
4. **Propón lo que falte.**
5. **Responde a las seis preguntas** del §10 de la propuesta, sin decidir por el operador.

## Entregable

Un fichero llamado «revision_astra.md», en esta misma carpeta, con un resumen de 5 líneas, la tabla de veredictos, tus mejoras y tus respuestas. Después, el diario (`.docs/scripts/diario.sh "Revisión de la propuesta del Motor (SC-3)" astra`), el commit con `.docs/scripts/commit.sh` sin tocar ningún bloque ni el marco común, y el aviso al operador.

## Reglas

- No cambies nada de `bloque_a/`, `bloque_a_forex/`, `bloque_b/` ni `sistema_global/`.
- Repositorio público: sin secretos ni datos personales.
