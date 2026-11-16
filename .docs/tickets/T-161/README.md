# T-161 · Guías CT-18: hallazgos de la QA r01 de T-158

| Campo | Valor |
| --- | --- |
| Estado | EN QA (r03: QA r02 NO APTO) |
| Pieza | bloque_a (ejecutor, `11_Ejecutor`) |
| Planifica · implementa · QA | claude · claude · un revisor nuevo sin contexto (regla del 12-11-2026, `compartida/2026-11-12_claude-puede-hacer-qa`) |
| Aprobación del operador | no necesaria: corrección de hallazgos de QA de una función ya cerrada (T-158); lo que el diseño no dice se decide por defecto (regla del 13-11-2026), se marca `[PROPUESTO]` y va a INC-T126-01 y al registro de decisiones |
| Deuda técnica | T-161 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` (la fila no se toca en este ticket) |

## Objetivo

Cerrar los hallazgos H-01 a H-07 de la QA r01 de T-158 (`.docs/tickets/T-158/qa.md`): que el control doble de las guías CT-18 no se salte con variantes triviales, sinónimos u otros idiomas; que revise todo lo que llega al modelo; que no lleguen guías a los agentes que son controles; que sea idempotente, que el emisor también filtre y que las pruebas fijen lo que el ticket promete.

## Kit de contexto leído (regla 1)

- `.docs/tickets/T-158/` (README, `analisis-tecnico.md`, `qa.md`) y los scripts del revisor `revisores/r01_0*.py`.
- Prompt del Orquestador V5.0 (dato en runtime, no se edita): solo 6.8 (tipos y reclasificación obligatoria) y 6.9 (guías).
- Código: `bloque_a/guias.py`, el enganche en `orquestacion.py` (F0 del ciclo y `_invocar`), `cli.py` (`guia`), `tests/test_t158_guias.py`, `ejemplos/guias/guia_pb48.json`.
- `docs/incidencias.md` (INC-T126-01) y `sistema_global/seguimiento/Decisiones_del_operador_Bloque_A.md` (fila de las guías).

## Alcance

- Entra: `bloque_a/guias.py` (normalización, detector, revisión de todos los campos de texto, agentes de control, idempotencia de COR- y P3-, control del emisor), `cli.py` (`guia emitir` falla cerrado con mensaje y opción de simulación para PB-48), pruebas nuevas en `tests/test_t161_guias.py`, ajuste de la preparación de las pruebas de PB-48 de `test_t158_guias.py` (la guía en conflicto ya no la deja emitir el emisor salvo en simulación), `ejemplos/guias/`, README del ejecutor, mapa del plan (texto de PB-48), INC-T126-01 y el registro de decisiones.
- No entra: los goldens, `contratos.py`, el Documento 0, `evaluador.py`, `motor/`, `herramientas/verificador_ids.py`, otros bloques, el corpus, la fila T-161 de la deuda. Ni que el Orquestador redacte guías con el modelo real (Fase 5).

## Diseño

- **Contratos y estado.** No cambian: el cuerpo CT-18 de tipo GUIA y su esquema siguen igual; HA gana, como en T-158, entradas GUI-, COR- y P3-. El COR- y el P3- de un rechazo en el F0 se reutilizan si ya existen para el mismo `(guia_id, item_id)`. No hay migración.
- **H-01 · Normalización.** NFKC; se quitan los caracteres de formato (Cf: espacio de ancho cero, guion blando…); guiones de cualquier tipo, signo menos y subrayado pasan a espacio; NFKD sin marcas combinantes (tildes); minúsculas; espacios unificados. **Escritura:** una letra que no es latina (cirílica, griega…) hace del ítem un conflicto (familia `ESCRITURA`).
- **H-01 · Criterio.** Se combina una lista de permitidos acotada con la de prohibidos ampliada, sobre `que_cambia`:
  - Se mantienen las tres familias de T-158 (tipo 3, relaja un control, prohibido) con más sinónimos (saltar en todas sus formas, aplazar, sustituir, copiar, ahorrar, dispensar, «no es preciso», «innecesaria»…).
  - **Nombra un control** (`NOMBRA_CONTROL`): si nombra un control o una regla (segunda pasada o cualquier pasada, reevaluación, dimensiones decisivas, puntuaciones, corroboración, una fuente, raíces, verificación, revisión, control doble, registro, historial, seguridad, refutación, «en contra», objeciones, auditoría, hallazgos, G3 o validación final, dictamen, bloqueos, avisos, excepciones, HT-03, HT-09, elegibilidad, puertas, PS1–PS8, una regla R, reglas de datos, prompts, contratos) es conflicto **salvo** que la acción sea claramente de reforzarlo: un verbo de refuerzo (haz, aplica, comprueba, verifica, añade, exige, registra, cita, repite, incluye, consulta, revisa, documenta, contrasta, confirma…) y ninguna marca de rebaja (negación, «solo», «sin», «salvo», «basta», «opcional», «en lugar de»…).
  - Rebajas implícitas que son conflicto por sí solas: «un único», «una sola», «una fuente», «por bueno», «como leves», «como avisos».
  - **Idioma:** palabras funcionales de inglés, catalán, francés, portugués, italiano y alemán que no existen en castellano → conflicto (familia `IDIOMA`). Las guías se redactan en castellano.
  - **H-06:** estados (todos, no solo los de madurez), prioridades (salvo las de la agenda de vigilancia, que 6.8 pone como tipo 2), reglas de datos (antigüedad, frescura, datos antiguos) y métricas (maximizar, minimizar).
- **H-02.** Se revisan todos los campos de texto del ítem que llegan al modelo (`que_cambia`, `donde_se_comprueba`, `como_se_sabe`) y además `origen`. Los dos descriptivos se revisan con el criterio de prohibidos (una acción que rebaja un control, rebajas implícitas, tipo 3 con un verbo de cambio, credenciales, datos protegidos, idioma, escritura), no con el de «nombra un control», porque su oficio es nombrar el campo o la comprobación (el ejemplo del prompt dice «HT-09 G3-DAT-02 sin fallos»).
- **H-04.** `[PROPUESTO]`: 6.8 y 6.9 no dicen a quién puede dirigir guías el Orquestador (6.8: «el agente afectado»; CT-18 es AG-18 → cualquier agente). Por defecto, ninguna guía a los agentes que son controles: AG-11 (refutación, R12), AG-18 (el propio Orquestador, que emite y dictamina) y AG-19 (Auditor). El emisor no la emite; si aparece en HA, el receptor deja COR- y P3- por cada ítem y la guía pasa a RETIRADA. Se corrige el límite declarado en INC-T126-01 («R23 por construcción» solo vale para los controles que son código).
- **H-03.** Idempotencia: antes de escribir COR- y P3-, `_retirar` busca un COR- del mismo `(guia_id, item_id)` y lo reutiliza (y escribe el P3- si faltaba).
- **H-05.** El emisor repite el detector y los agentes de control: un ítem en conflicto no se emite (`MensajeInvalido`, HA sin cambios); la CLI termina con el motivo. Para ejercer PB-48 («guía vigente que sugiere omitir la segunda pasada», es decir, el filtro del Orquestador falló), `emitir(…, simular_fallo_del_emisor=True)` y la CLI `--simular-fallo-del-emisor` lo admiten **solo con el cliente simulado**; la entrada GUI- lo anota (`control_emisor`).
- **H-07.** Pruebas: determinismo con ciclo e hilos y una guía en conflicto (G09); caso negativo con verbo de rebaja y sin control (G08); dos `cargar` del mismo día en runs distintos con una entrada de HA escrita entre medias (G22).
- **Números.** Ninguno nuevo. Los límites y la caducidad siguen en `guias_orquestador`.
- **Cómo falla cerrado.** Lo que el detector reconoce como dudoso es conflicto: no se aplica, se registra y se escala; lo que no reconoce se aplica como contexto del modelo del receptor (corregido en la r02, QA r01 H-04). Un falso positivo solo retira un ítem y pide decisión al operador.

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| Criterio estricto | Falsos positivos: ítems válidos retirados y escalados | Se miden con los ejemplos válidos (prompt 4.5, tipos de 6.8, `guia_pb48.json`, pruebas de T-158); el falso positivo es prudente |
| Seguir siendo una lista de palabras | Una paráfrasis nueva puede pasar | Lo que llega al modelo pasa por el detector en todos los campos; no llega a los agentes de control; HT-03, puertas y G3 siguen siendo código. Límite declarado |
| El emisor rechaza la guía de PB-48 | La prueba de PB-48 y la CLI ya no pueden preparar el caso | Simulación explícita, solo con el cliente simulado y anotada en HA |
| Los scripts del revisor dependen del comportamiento viejo | Algunos casos de r01_02 y r01_05 fallan | Se explican uno a uno en `pruebas.md` (miden hallazgos ya corregidos o emiten sin simulación) |

## Criterios de aceptación (binarios)

1. CA-1 (H-01): de los 50 ataques de `r01_01_detector.py`, quedan detectados todos salvo los explicados; las variantes tipográficas, los sinónimos, otros idiomas y otras escrituras se detectan.
2. CA-2 (H-01): falsos positivos medidos con los ejemplos válidos; ninguno en el ejemplo del prompt (4.5), en `guia_pb48.json` (ítem válido) ni en los casos válidos de `test_t158_guias.py`.
3. CA-3 (H-02): un ítem que rebaja un control en `donde_se_comprueba`, `como_se_sabe` u `origen` es conflicto y no llega a ningún agente.
4. CA-4 (H-04): no se emite ni se aplica una guía para AG-11, AG-18 o AG-19; si está en HA, COR- y P3- por ítem y RETIRADA; INC-T126-01 dice el límite real.
5. CA-5 (H-03): si la reemisión falla, el run siguiente no duplica COR- ni P3-.
6. CA-6 (H-05): `emitir` y la CLI rechazan un ítem en conflicto sin tocar HA; la simulación solo con el cliente simulado.
7. CA-7 (H-06, H-07): estados, prioridades, reglas de datos y métricas detectados; los mutantes G08, G09 y G22 mueren con las pruebas del ticket.
8. CA-8: PB-48 sigue «Superada»; los goldens coinciden; cuotas ruff ≤ 2825 y mypy de A ≤ 109; la suite de A no baja.

## Plan de pruebas

| Prueba | Tipo | Criterio |
| --- | --- | --- |
| `tests/test_t161_guias.py`: ataques de r01_01, normalización, idiomas, escrituras | Fallo cerrado, regresión | CA-1 |
| `tests/test_t161_guias.py`: ejemplos válidos | Nominal | CA-2 |
| `tests/test_t161_guias.py`: campos descriptivos y ciclo | Integración | CA-3 |
| `tests/test_t161_guias.py`: agentes de control | Fallo cerrado | CA-4 |
| `tests/test_t161_guias.py`: reemisión que falla | Regresión | CA-5 |
| `tests/test_t161_guias.py`: emisor y CLI | Fallo cerrado | CA-6 |
| `tests/test_t161_guias.py`: H-06, determinismo con hilos, caché por run, verbo sin control | Regresión, determinismo | CA-7 |
| `test_t158_guias.py`, `test_t126_pb26_pb48.py`, goldens, gates ligeros, suite completa de A, mutantes de r01_04 | Regresión, contrato | CA-8 |

## Scripts

- `.docs/scripts/nuevo_ticket.sh` (abre el ticket).
- `.docs/tickets/T-161/medir_detector.py` (nuevo): ataques de r01_01 y falsos positivos con los ejemplos válidos, en una tabla.
- `.docs/scripts/mutantes_revisor_ampliado.py` (mutantes de r01_04 con las pruebas nuevas).
- `.docs/scripts/evidencias_plan_a.py --pb PB-48`, `bloque_a/11_Ejecutor/tests/goldens_ct.py`.

## Ronda r02 (QA r01 de T-161: NO APTO)

Hallazgos de `.docs/tickets/T-161/qa.md` y cómo se cierran (detalle en `analisis-tecnico.md`, sección r02; pruebas en `pruebas.md`):

| Hallazgo | Corrección | Prueba |
| --- | --- | --- |
| H-01 (alta) | AG-20 en `AGENTES_DE_CONTROL`; `conflicto_de_leccion` en `_informe_aprendizaje` (`orquestacion.py`): una lección del modelo que rebaja un control no se escribe en F6. `evaluador.py` no se toca | `test_t161_r02.py::test_h01_*`; M24, M25 |
| H-02 (media) | Negaciones indirectas, condiciones y números con letras (también en los descriptivos); cifras como letras; R9 (`RE_INYECCION`); INSTRUCCION y MARCADO, que retiran la guía entera; lista de caracteres permitidos | `test_h02_*` (los 68 ataques); M15, M19–M23 |
| H-03 (media) | Enmascarado de sentidos financieros, IDIOMA sin siglas ni nombres propios, verbos de orden y formato, «una sola» acotada | `test_h03_*` (40 de la QA, 40 de dominio); M16–M18 |
| H-04 (baja) | Textos de INC-T126-01, del registro de decisiones, del mapa de PB-48, de `guias.py`, del README del ejecutor y de este ticket | lectura |
| H-05 (baja) | Pruebas para Q02, Q06 y Q12; `max_caracteres_por_texto: 600` en `guias_orquestador` | `test_h05_*`; M26 |

Criterios de aceptación de la r02:

- CA-9 (corregido en la r03): AG-20 no recibe guías; ningún agente de control recibe una lección redactada por un modelo (solo las del código del ejecutor, origen DETERMINISTA en F6); las lecciones de AG-20 que no cumplen F6 4.4 (`tipo`, `ambito`) o que el detector reconoce como conflicto no se escriben en F6 ni se dan al leerlas; lo que el detector no reconoce llega como contexto a los agentes que no son de control.
- CA-10: 0 de los 68 ataques nuevos pasan; los explicados, explicados.
- CA-11: falsos positivos medidos y declarados con cifras en INC-T126-01.
- CA-12: Q02, Q06 y Q12 mueren; los textos tienen longitud máxima de la configuración.

## Ronda r03 (QA r02 de T-161: NO APTO)

Hallazgos de la sección «Ronda r02» de `.docs/tickets/T-161/qa.md` (detalle en `analisis-tecnico.md`, sección r03; pruebas en `pruebas.md`):

| Hallazgo | Corrección | Prueba |
| --- | --- | --- |
| H-06 (alta) | Arreglo estructural: los agentes de control solo reciben lecciones del código (origen DETERMINISTA en F6); `tipo` y `ambito` validados contra F6 4.4 al escribir y al leer; detector al leer para los demás; revisión en el F0 con incidencia; falla cerrado. `orquestacion.py`: una línea en `_invocar` y la llamada de `_informe_aprendizaje`. `evaluador.py`: sin tocar (ya marcaba el origen) | `test_t161_r03.py::test_h06_*`; M27–M31, M37, M38 |
| H-07 (media) | Sin enmascarado si hay un verbo de cambio o de rebaja; verbos neutros solo fuera del núcleo; condiciones, verbos de omitir, otras lecturas del texto, base64, otra lengua en mayúsculas, redefiniciones | `test_h07_*` (los 52 ataques y los 48 válidos); M33–M36 |
| H-08 (media) | `ENDURECE`: lo que hace más prudente una lección no cuenta como rebaja | `test_h08_*` (20 prudentes, 8 ataques); M32 |
| H-09 (baja) | INC-T126-01, registro de decisiones, mapa de PB-48 y CA-9 | lectura |
| H-10 (baja) | Pruebas para S04, S07 y S09; el umbral de mayúsculas de `_sin_nombres` se quita (S06 ya no aplica) | `test_h10_*` |

## Registro

- 2026-11-16 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-16 · PLANIFICADO · claude · plan y criterios escritos
- 2026-11-16 · EN CURSO · claude · implementación
- 2026-11-16 · EN QA · claude · implementado y probado; QA con un revisor nuevo
- 2026-11-16 · EN CURSO · claude · r02: QA r01 NO APTO (H-01 alta); correcciones
- 2026-11-16 · EN QA · claude · r02 implementada y probada; QA r02 con un revisor nuevo
- 2026-11-16 · EN CURSO · claude · r03: QA r02 NO APTO (H-06 alta); correcciones
- 2026-11-16 · EN QA · claude · r03 implementada y probada; QA r03 con un revisor nuevo
