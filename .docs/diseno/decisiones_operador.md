# Decisiones del operador sobre los diseños

Registro de lo que el operador decide sobre las propuestas de `.docs/diseno/`. Cada decisión dice de dónde sale y qué falta para que sea efectiva. Las que cambian la Constitución quedan **aceptadas como rumbo** y se incorporan formalmente en la enmienda 5, cuando Astra termine sus revisiones.

## Tanda 1: antes de construir la Fase 1 (11-11-2026)

El operador acepta los valores por defecto de la tanda 1 de la pasada de coherencia (`.docs/diseno/coherencia/propuesta_claude.md`, §8): «Acepto los valores por defecto de la tanda 1».

| # | Decisión | Valor aceptado | Sale de | Qué falta |
| --- | --- | --- | --- | --- |
| 1 | Cómo se rehacen A, B y C | Misma pauta para los tres: pocos papeles de IA, núcleo común con kits por tipo de activo y banco de medida antes de recortar; cada recorte, como aspirante frente al diseño actual | Propuestas de A, B y C; E4-13 | Construir el banco de medida |
| 2 | Contradictor de otro proveedor de IA | Sí, con su coste y su clave propios, para A, B y C | Propuestas de B y C; E4-13 | Contratar el segundo proveedor (clave en SC-7, puerto en SC-10) |
| 3 | Adelantar el largo plazo (E4-18) | Sí, en paralelo a la Fase 1; los perfiles de C que son casi todo código (C-IDX y C-FON) no cuentan para el tope de ocho bloques activos | Enmienda 4; coherencia §5 | Incorporarlo en la enmienda 5 (cambia §14 y D-19) |
| 4 | Asimetría del control F | Reducir, cerrar o proteger nunca se bloquea por pérdidas, frecuencia ni kill-switch, solo por errores de forma | Propuesta de F | Incorporarlo en la enmienda 5; cambia CT-G-08 |
| 5 | Registro de experimentos | Desde la Fase 1, con prerregistro sellado | Propuesta de J | — |
| 6 | Informes con rangos | Siempre con rango; «todavía no se sabe» si incluye el cero | Propuestas de I y N | — |
| 7 | Jurisdicción fiscal (P-06) | Territorio común | Propuesta de SC-9 | El operador designa al asesor fiscal que firmará las reglas (no hace falta en la Fase 1, que es simulada) |
| 8 | Intermediario | Dos entidades por defecto (una con acceso por programa para trading y táctica; una española con fondos traspasables para el largo plazo), con los criterios del §4 de SC-10 | Propuestas de G y SC-10 | El operador elige las entidades en la ficha de restricciones reales (antes del peldaño 2, la cuenta de demostración) |

**Borrador del texto:** `.docs/diseno/enmienda_5/propuesta_claude.md` (enmienda 5, parte 1, 11-11-2026) redacta las ocho decisiones en la Constitución, con lo que concreta marcado [PROPUESTO]; no es efectivo hasta que el operador lo ratifique.

**Si una revisión de Astra discrepa** de alguna de estas decisiones, lo señala en su revisión y Claude lo lleva al operador antes de incorporarlo a la enmienda 5.

## Tanda 2: parámetros de la Fase 1 y preguntas de la enmienda 5, parte 2 (11-11-2026)

El operador pidió a Claude que contestara el cuestionario (`.docs/diseno/coherencia/cuestionario_tanda_2.md`) y confirmó sus respuestas: «Confirmo todas».

- **Los parámetros (R1 a R3, F1 a F5, H1 a H5, M1 a M4, A1 a A3)** son su perfil de riesgo y sus límites: viven en su documento privado y, cuando exista, en su copia (SC-1), **no en el repositorio**. Hasta entonces, el sistema sigue con los valores por defecto [PROPUESTO] del marco, en simulado; cambiar los del marco es código y va en un ticket con autorización.
- **Las decisiones de arquitectura (E1 a E8)** quedan aceptadas como rumbo y entran en la enmienda 5, parte 2, que el operador ratificará punto por punto:

| # | Decisión | Valor aceptado | Cambio de la parte 2 |
| --- | --- | --- | --- |
| E1 | Brújula de P17 | Sí; retirada propuesta tras dos revisiones sin aportar; decide el operador | 56 |
| E2 | Tope anual de gasto en IA y datos | 0,5 % del capital gestionado; al llegar, modo sin IA | 76 |
| E3 | Cambios menores sin aprobación | No al principio: todos los aprueba el operador | 52 |
| E4 | Perfilador con las conversaciones | No: solo cuestionarios y comportamiento real | 74 |
| E5 | Estratega macro | Fase 2, solo informando | 71 |
| E6 | Papeles del Broker | Siete funciones y como mucho tres agentes de IA; perfilador y asesor como modos del conversacional (se aparta de la opción recomendada del cuestionario) | 73, redactado de nuevo |
| E7 | SC-12, biblioteca de conocimiento | Sí, mínima en la Fase 1 | 57 |
| E8 | Comparar entre clases de activo | Se decide antes de la Fase 2; hasta entonces, la regla de hoy | 79 |

Sobre E2, Claude avisó de que con el consumo medido hoy es probable que un uso semanal supere el tope con carteras pequeñas: obliga a los rediseños de A y B a recortar y, si el banco de medida demuestra que no cabe, la decisión será entre subir el tope o gestionar en pasivo.

Las tandas 3 a 5 siguen con sus valores por defecto [PROPUESTO], en simulado.

## Bloque B: diseño cerrado y construcción (13-11-2026)

- **Diseño:** el operador pidió a Claude que decidiera sobre la revisión C-02 de Astra «al igual que en el bloque A». Resultado: `.docs/diseno/bloque_b/decision_claude_c02.md` (diseño V3 seleccionable, con la V2.1 por defecto).
- **Construcción:** «Asigna la tarea en su cola y levanta la congelación del bloque B». Se añade C-37 a la cola de Astra, después de C-08, con las directrices `.docs/diseno/bloque_b/directrices_astra.md`. `bloque_b/` deja de estar congelado para esa tarea. El corpus congelado de B (Documento 0, prompts y esquemas) sigue sin tocarse, como dicen las directrices.
- **Qué falta:** los valores `[PROPUESTO]` del diseño (tope por petición, modelos por papel) van a T-57. La publicación del trabajo de Astra sigue la regla de su cola: en local hasta que el operador autorice subirlo.
