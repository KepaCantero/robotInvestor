# T-116 · Fase 4 del Bloque A: evidencias del plan de pruebas

| Campo | Valor |
| --- | --- |
| Estado | CERRADO |
| Pieza | bloque_a (pruebas y documentación) |
| Planifica · implementa · QA | claude · claude · un revisor nuevo sin contexto (o Astra, si el operador se lo asigna) |
| Aprobación del operador | aprobada el 2026-11-13: «empieza por la fase 4» |
| Deuda técnica | T-116 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Objetivo

Ejecutar el Plan de pruebas V3.0 del Bloque A (PB-01 a PB-67) con el cliente simulado y dejar, para cada prueba del plan, su resultado real y el comando que lo repite. Es la Fase 4 del plan de fases de `CLAUDE.md` y sigue el prompt `prompts/FASE4_PLAN_PRUEBAS.md`.

## Alcance

- Entra:
  - el mapa verificado `bloque_a/11_Ejecutor/tests/mapa_plan_pruebas.json`: por cada PB, su cobertura, las pruebas automáticas que la cubren (identificador completo), qué comprueban y qué no;
  - el script `.docs/scripts/evidencias_plan_a.py`, que comprueba el mapa, ejecuta las pruebas citadas y escribe el documento;
  - el documento generado `docs/evidencias_pruebas_bloque_a.md`;
  - la prueba `bloque_a/11_Ejecutor/tests/test_fase4_mapa.py`, que mantiene el mapa al día con el plan y con la suite;
  - la lista de huecos: cláusulas del plan que el ejecutor podría comprobar y ninguna prueba comprueba.
- No entra:
  - las pruebas que exigen la API real: quedan «Pendiente API» con su motivo (regla 4 y prompt de la fase);
  - corregir el ejecutor: un fallo del plan es una incidencia en `docs/incidencias.md`, no un arreglo en silencio;
  - el Bloque B (un bloque por sesión);
  - reescribir `tests/MAPA_PLAN_DE_PRUEBAS.md`, el mapa del 3-11-2026: se conserva y se le añade un aviso que remite al nuevo.

## Diseño

- **Dos pasos.** Primero el mapa verificado (lectura: cada prueba citada se lee y se contrasta con el criterio de aprobación del plan). Después la ejecución, que genera el documento. El segundo paso carga la máquina y no se hace en paralelo con una QA.
- **Cobertura, con regla estricta:**
  - `AUTOMATICA`: las pruebas comprueban todo el criterio, salvo lo que solo existe con tiempo real o con el modelo real, que se anota;
  - `PARCIAL`: queda alguna cláusula que el ejecutor podría comprobar y ninguna prueba comprueba;
  - `PENDIENTE_API`, `REQUIERE_USUARIOS`, `DOCUMENTAL`: no son pruebas del ejecutor con el cliente simulado;
  - `SIN_PRUEBA`: ninguna prueba cubre el caso.
- **Las herramientas cuentan.** Las pruebas de `bloque_a/10_Herramientas/tests` (HT-02, HT-03, HT-07, HT-09) se citan y se ejecutan desde su carpeta. No están en el gate del repositorio; el script las ejecuta aparte.
- **El documento no se edita a mano:** lo regenera el script, con la fecha y el commit.
- Contratos CT-G afectados y versión de esquema: ninguno.
- Estado persistido: no cambia.
- Números y su origen: ninguno nuevo.
- Cómo falla cerrado: el script termina con 1 si un PB del plan falta en el mapa o sobra, si una prueba citada no existe, si una fila parcial no dice qué le falta o si una prueba citada falla. Una prueba que no se ejecuta deja la fila como «No ejecutada», nunca como superada.
- Decisiones del operador usadas como `[PROPUESTO]`: ninguna. Queda una para el operador: qué huecos se cubren con pruebas nuevas (ver «Huecos»).

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| Marcar por parecido (una prueba con nombre afín que no comprueba el criterio) | Evidencia falsa | Cada prueba citada se ha leído; la regla estricta manda a `PARCIAL` cualquier cláusula sin afirmación; el revisor de QA lo contrasta por muestreo |
| El mapa envejece al cambiar la suite | Filas que citan pruebas que ya no existen | `test_fase4_mapa.py` falla si una prueba citada desaparece o si el plan y el mapa dejan de coincidir |
| Tomar «Superada» por calidad validada | Confianza indebida | El documento repite que el cliente simulado valida la tubería, no la calidad analítica (R22) |

## Criterios de aceptación (binarios)

1. CA-1: el mapa tiene las 67 pruebas del plan, ni una más ni una menos, y cada fila dice su cobertura, sus pruebas, qué comprueban y qué no.
2. CA-2: toda prueba citada existe en la suite del ejecutor o en la de las herramientas (`evidencias_plan_a.py` sin opciones termina con 0).
3. CA-3: `evidencias_plan_a.py --ejecutar` genera `docs/evidencias_pruebas_bloque_a.md` con las 67 filas y termina con 0: todas las pruebas citadas pasan.
4. CA-4: cada fila «Superada» o «Superada en parte» tiene en el documento un comando que, copiado tal cual desde la raíz, pasa.
5. CA-5: ninguna fila que dependa del modelo real, de usuarios o de una revisión documental figura como superada.
6. CA-6: citar en el mapa una prueba que no existe, quitar un PB o dejar una fila parcial sin su hueco hace fallar el script y `test_fase4_mapa.py`.
7. CA-7: los huecos están listados en este ticket y en la deuda técnica.
8. CA-8: `./tools/check_all.sh` 12/12; las cuotas no suben; las pruebas recogidas del Bloque A no bajan.

## Plan de pruebas

| Prueba | Tipo (nominal, límite, fallo cerrado, regresión, migración, integración) | Criterio |
| --- | --- | --- |
| El mapa coincide con el plan (67) y sus filas tienen la forma debida | nominal | CA-1 |
| Cada prueba citada existe como función de prueba en su fichero | nominal | CA-2 |
| Mapa con una prueba inventada, sin un PB o con una fila parcial sin hueco: `comprobar` lo dice | fallo cerrado | CA-6 |
| Una fila sin pruebas nunca resulta «Superada» | fallo cerrado | CA-5 |
| `--ejecutar` completo y un comando del documento copiado a mano | integración | CA-3, CA-4 |
| Gate completo | integración | CA-8 |

## Huecos (primera mitad)

Resultado del mapa verificado: 22 automáticas, 31 parciales, 7 pendientes de la API, 5 sin prueba, 1 con usuarios y 1 documental. El mapa del 3-11-2026 daba 34 automáticas. Con la regla estricta, 13 pasan a parciales (PB-10, PB-11, PB-13, PB-16, PB-20, PB-22, PB-31, PB-34, PB-41, PB-43, PB-44, PB-59, PB-62) y una que era parcial pasa a automática gracias a pruebas posteriores y de las herramientas (PB-53).

- Sin prueba: PB-17 (autorizaciones AUT- de ampliación de presupuesto), PB-26 (orden por calidad y temática de las referencias), PB-45 (máximo de 10 lecciones por encargo), PB-46 (fiabilidad de fuentes, FUE-, no implementada) y PB-48 (conflicto de normas).
- Parciales: la cláusula que falta en cada una está en la columna «No comprueba» del mapa y del documento.

### Huecos cubiertos (13-11-2026, por orden del operador: «Haz ambos puntos. Lo confirmo»)

Ocho pruebas nuevas en `bloque_a/11_Ejecutor/tests/test_fase4_huecos.py`. El mapa queda en 27 automáticas, 28 parciales, 7 pendientes de la API, 3 sin prueba, 1 con usuarios y 1 documental.

| PB | Qué se añade | Queda |
| --- | --- | --- |
| PB-10 | Qué cambia en F10 y que HA queda sin incidencia de escritura | Parcial: el ejecutor guarda también la lista global de horizontes (INC-T116-01) |
| PB-16 | G3 hace las mismas comprobaciones con el presupuesto agotado | Automática |
| PB-17 | AUT- autorizada y denegada, y cierre con alcance reducido en un ciclo | Parcial: la AUT- no lleva CPI ni EAC (INC-T116-02) |
| PB-22 | Los tres mensajes del plan, tres incidencias y ningún efecto en archivos | Automática |
| PB-33 | Estado, motivo y fecha de la revocación; pronósticos congelados intactos | Automática |
| PB-45 | Diez lecciones como máximo en el encargo, las de más fuerza | Automática (la aplicación de la lección es del modelo) |
| PB-59 | Incidencia SEGURIDAD en HA sin copiar el valor | Automática |

Siguen sin prueba PB-26, PB-46 (no implementada) y PB-48. Los demás parciales conservan su hueco en la columna «No comprueba».

Hallazgo al escribir PB-17, sin tocar: con el presupuesto de MP forzado, el ciclo simulado acaba COMPLETO con 6,75 y 7,0 UC y PARCIAL con 7,25 UC. No es un fallo del control (nunca se supera el margen), pero el resultado no crece con el presupuesto, porque la estimación previa de cada llamada depende del tamaño del mensaje. Apuntado en la deuda (T-116).

### Ronda r04 (14-11-2026): repaso cláusula a cláusula

Las filas que cambian, fila a fila, están en `analisis-tecnico.md` («Ronda r04»). Lo que el ejecutor no hace y el plan pide queda en INC-T116-03 (`docs/incidencias.md`): la re-ejecución CT-10 del certificado (PB-32), la sección «Novedades» de F6 (PB-33), la respuesta final por CT-03 de una consulta escalada (PB-07), la lección que compara enviadas y descartadas (PB-11), el tipo de dato en la incidencia de seguridad (PB-21), la objeción sin resolver en el técnico (PB-38), la revisión C2 de una respuesta tardía (PB-61), la LEC- de una consulta recurrente (PB-62), la publicación de los estados H5 (PB-64), la degradación de un horizonte distinto de H5 por DM-HLN (PB-50), la recalibración de umbrales y la P3- en HA (PB-36) y el aviso de plazos del monitor (PB-19).

## Scripts

- Crea `.docs/scripts/evidencias_plan_a.py` (apuntado en la tabla de `.docs/README.md`).

## Registro

- 2026-11-13 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-13 · EN CURSO · claude · plan escrito y primera mitad hecha en una copia aparte, mientras corre la QA r02 de T-112: mapa verificado, script y prueba del mapa. Falta ejecutar (`--ejecutar`), generar el documento y el gate
- 2026-11-13 · EN CURSO · claude · huecos cubiertos: ocho pruebas nuevas (PB-10, 16, 17, 22, 33, 45 y 59), INC-T116-01 y 02. Sigue pendiente ejecutar, generar el documento y el gate
- 2026-11-13 · EN QA · claude · evidencias generadas: 94 de 94 pruebas citadas superadas (27 filas superadas, 28 en parte); informe de pruebas escrito; pendiente la QA
- 2026-11-14 · NO APTO · QA r01 (revisor nuevo sin contexto, `2ff0630`): H-01 alto (PB-21, PB-23, PB-37 y PB-49 dadas por automáticas con una cláusula sin afirmar), H-02 y H-04 medios, H-03 y H-05 bajos. El script, el documento y las ocho pruebas de huecos, bien
- 2026-11-14 · EN QA · claude · ronda r02: siete pruebas nuevas (PB-21, 23, 37, 49, 54 y 64), PB-37 pasa a parcial, `--pb` y `--runxfail`, cabeceras del plan, documento comparado con el mapa, análisis técnico, deuda y avance. 26 superadas y 29 en parte; 101 de 101 pruebas citadas superadas
- 2026-11-14 · NO APTO · QA r02 (revisor nuevo sin contexto): los cinco hallazgos de la r01, corregidos; uno nuevo del mismo tipo, H-06 alto (PB-32 automática sin prueba de que una celda sin habilidad no se certifica)
- 2026-11-14 · EN QA · claude · ronda r03: dos pruebas de PB-32 (nueve casos), PB-32 y PB-49 a parcial; 24 superadas y 31 en parte
- 2026-11-14 · NO APTO · QA r03 (revisor nuevo sin contexto): H-06 corregido (P32a a P32d mueren); nuevos H-07 alto (PB-60, PB-33, PB-56 y PB-06 automáticas con una cláusula sin afirmar; en PB-60 el ejecutor no declara la degradación en los entregables), H-08 medio (hueco de PB-32 incompleto: Holm y certificado por método) y H-09 bajo. El revisor propone un repaso cláusula a cláusula de las 24 automáticas
- 2026-11-14 · EN QA · claude · ronda r04: repaso cláusula a cláusula de las 24 automáticas y de las 31 parciales (H-07 y H-08) y la cifra de la deuda (H-09). Dos correcciones del ejecutor con su prueba de regresión (los entregables declaran un servicio degradado por una credencial denegada o pendiente, PB-60 y PB-58; la incidencia de canal no previsto se escala, PB-22) y 25 pruebas nuevas (29 casos) en `test_fase4_huecos.py`; doce diferencias con el plan que no se arreglan, con su línea en INC-T116-03 `[PROPUESTO]`. Pasan a parcial PB-07, PB-21, PB-33, PB-38, PB-61 y PB-64; a automática, PB-31, PB-37, PB-43 y PB-49. Resultado: 22 superadas y 33 en parte (7 pendientes de la API, 3 sin prueba, 1 con usuarios, 1 documental); 132 de 132 pruebas citadas superadas. Mutantes de la r03, todos muertos; 20 de 20 de los propios (`r04_mutantes_implementador.py`)
- 2026-11-14 · EN QA · claude · integrada la r04 con T-125 y T-126: PB-26, PB-46 y PB-48 pasan de SIN_PRUEBA a PARCIAL. Totales del mapa: 22 automáticas, 36 parciales, 7 pendientes de la API, 1 documental, 1 que requiere usuarios, 0 sin prueba; 145 pruebas citadas, todas superadas
- 2026-11-15 · NO APTO · QA r04 (revisor nuevo sin contexto): H-10 alto (PB-31 y PB-37 con una cláusula sin afirmar, M31, M37a y M37b vivos; PB-58 con un paso del ejecutor que no existe), H-11 medio (huecos incompletos de PB-44, PB-46, PB-48 y PB-26), H-12 bajo (`escalado_operador` sin lector)
- 2026-11-15 · EN QA · ronda r05 · claude · PB-31 (la banda sigue a la probabilidad interna; 0,65 «más probable que no» en los tres entregables) y PB-37 (`Evaluador.resolver` en los dos vencimientos) con su prueba, siguen automáticas; PB-58 a parcial con su línea en INC-T116-03; huecos completos de PB-44, PB-46, PB-48 y PB-26 (estas tres citan las pruebas de la r02 de T-125 y T-126); `incidencias_escaladas` en el estado del operador (H-12). Mapa: 21 automáticas, 37 parciales, 7 pendientes de la API, 1 documental, 1 con usuarios; 162 pruebas citadas, todas superadas. `r04_01`: 9 de 9 mutantes muertos
- 2026-11-15 · CERRADO · QA r05 APTO (revisor nuevo sin contexto). Sus hallazgos se resuelven al cerrar: H-13 (hueco de PB-20 completo), H-14 (PB-46 cita las pruebas del `calc_id`, de una FUE- por fuente y mes y las de la r03 de T-125) y H-15 (huecos de PB-08 y PB-29 concretos); evidencias regeneradas, 171 de 171 pruebas citadas superadas
