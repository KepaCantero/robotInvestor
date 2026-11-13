# Bloque B: decisión de Claude sobre la revisión C-02 de Astra y diseño V3

De: Claude, 13-11-2026. Responde a la revisión de Astra `.docs/tickets/T-68/revision_astra.md` (base `f2db7ad`, corpus B V2.1) y a la petición del operador del mismo día: «analiza la propuesta de revisión que ha generado Astra y, al igual que en el bloque A, considera qué propuestas adoptar y cuáles no. También puedes aportar más mejoras». Las propuestas revisadas son la evaluación de T-68 (`.docs/tickets/T-68/evaluacion_claude.md`) y el rediseño (`propuesta_rediseno_claude.md`, en esta carpeta).

Estado: **DISEÑO ESTABLECIDO**. Se implementa siguiendo `directrices_astra.md`, en esta carpeta, cuando el operador asigne la tarea y levante la congelación de `bloque_b/`.

## 1. Resumen

- **Se acepta la revisión casi entera.** De las nueve mejoras, las nueve se aceptan con los cambios de Astra. De las siete decisiones del rediseño, cinco se aceptan tal como las pide y dos con un matiz (§3).
- **Dos correcciones a mi propuesta, que Astra tenía razón en señalar:**
  - la auditoría previa al 100 % en N2 y N3 **se conserva**; no se cambia por muestreo;
  - las cifras de consumo de la propuesta (6 a 8 llamadas y 150.000 a 200.000 tokens por N2) **se retiran**. No están medidas: se medirán con los prompts construidos.
- **El rediseño se construye como diseño V3 seleccionable** (`diseno: v3`), como en A. La V2.1 sigue por defecto y es la referencia. Volver atrás es cambiar una línea de la configuración.
- **Nada sale de B** mientras I, H, K y el Orquestador del Broker no existan como código. Por configuración solo se apagan las llamadas de IA de las funciones que pasan a código.
- **Diez ideas nuevas** (§5). La mayoría vienen de lo aprendido al construir la V6 de A (T-101, T-102, T-88, T-91). Las más útiles son:
  - el plan por código con la matriz de activación del Documento 0, que ya existe;
  - el Sintetizador sin cifras libres;
  - la exploración medida de las dimensiones que el plan deja fuera.

## 2. Mejoras de T-68

| # | Mejora | Decisión | Cómo se aplica |
| --- | --- | --- | --- |
| 1 | Banco de medida | **Se acepta con los cambios de Astra** | Cuatro variantes con los mismos casos, fechas, universo y costes: azar, solo código, V2.1 y V3. Intervalos emparejados y una muestra final reservada que nadie mira hasta el final. Mide omisiones, errores graves y latencia, además de calidad y coste. El simulador solo valida la mecánica y el consumo; la aceptación posterior de C no es verdad de mercado. |
| 2 | Caché | **Se acepta con los cambios de Astra** | Por prefijo, no por agente (lección de T-88): el núcleo común va primero y es idéntico byte a byte. Se cachea según la reutilización observada, también entre peticiones. Hay desactivación explícita y se corrige el fallo que encontró Astra: hoy `ttl=""` sigue añadiendo `cache_control`. Se registra cada acierto y cada escritura. No se anuncia ningún ahorro sin medirlo. |
| 3 | Un playbook por instancia | **Se acepta con los cambios de Astra** | El kit del Seleccionador lleva el playbook de su tipo más el **cierre de sus dependencias**, que se calcula mecánicamente a partir de las referencias cruzadas (P.7.3 al subyacente, P.5.3 a RV…). Las reglas globales se conservan. Una prueba comprueba que ninguna referencia queda sin cargar. |
| 4 | Prefijo común | **Se acepta con los cambios de Astra** | Solo el texto literalmente idéntico entre los prompts forma el núcleo. Se extrae mecánicamente y se comprueba byte a byte. Lo marcado como común que lleva sustituciones propias del agente va al kit. |
| 5 | Director por fases | **Se acepta con los cambios de Astra** | Lo absorbe el Analista de ámbito (§3): invariantes siempre presentes y un módulo por fase. Una tabla de obligaciones dice dónde queda cada obligación del prompt del Director, y la comprueba una prueba. |
| 6 | Lotes | **Se acepta con los cambios de Astra** | Solo para lo que admite demora: evaluación, mantenimiento de F7 a F9 y backtests. El Vigía y los seguimientos encargados quedan fuera. Cada lote tiene caducidad y cancelación, y al consumir el resultado se comprueba que los datos siguen vigentes. |
| 7 | Precios y tope | **Se acepta con los cambios de Astra** | Antes de cada intento se reserva el presupuesto, incluida la salida máxima, los reintentos y las herramientas. Hay un límite global para las peticiones concurrentes. Al llegar al tope, el análisis para en un punto de control y es reanudable. El coste se da en la moneda declarada. Los precios siguen `null` hasta que el operador los rellene, y el tope por petición es `[PROPUESTO]` para T-57; el tope anual es el de E2. |
| 8 | Modelo por tarea | **Se acepta con los cambios de Astra** | El modelo se fija por papel, nivel y tarea en la configuración, con versión fijada. Sonnet es el aspirante por defecto y Opus queda para el Analista de ámbito en N3. Solo se promueve un modelo tras el banco, por coste por análisis válido, no por tarifa. |
| 9 | Reglas a código | **Se acepta con los cambios de Astra** | Pasa a código lo exacto: validación, identificadores, formatos, duplicados exactos y raíces por la fuente declarada. La credibilidad, la materialidad y las contradicciones no se convierten en deduplicación: las discrepancias que marca el código las resuelve el Analista de ámbito y las revisa el Auditor. |

## 3. Decisiones del rediseño

| Decisión | Astra | Claude | Motivo |
| --- | --- | --- | --- |
| Eliminar el Director | De acuerdo con cambios | **De acuerdo con sus cambios** | Una máquina de estados en código coordina, con las capas, PV1 a PV3, PT30 y PTA, pausas, cancelación y reanudación idempotente. El Analista de ámbito pone el juicio. La tabla de obligaciones (mejora 5) cubre las consultas filtradas (CT-B-28), la parada y la respuesta a objeciones. |
| Analista de dimensión y plan | De acuerdo con cambios | **De acuerdo, con un matiz** | El plan lo hace el código con la **matriz de activación y de pesos del Documento 0 (8.3.1 y 8.3.4)**, que ya distingue líder, activado y condicional. Así se respeta R17 («doce dimensiones o exclusión justificada») sin juicio nuevo: toda dimensión excluida queda en el mapa de cobertura con su motivo. Un papel puede tener varias instancias en paralelo, una por dimensión líder. El matiz: en N2, las dimensiones activadas que no son líderes se agrupan en lotes por tamaño (configuración), y el banco compara lotes y llamadas sueltas. El Analista de ámbito puede pedir una dimensión que el plan dejó fuera, con motivo registrado. |
| Seleccionador con kit y Sonnet | De acuerdo con cambios | **De acuerdo con sus cambios** | Kit con cierre de dependencias (mejora 3) y campos de incertidumbre. Sonnet es aspirante. |
| Contradictor y segundo analista | De acuerdo con cambios | **De acuerdo, con un matiz** | Las objeciones conservan su alcance (TESIS o CANDIDATO), el candidato, el eslabón, la fuente, la fecha y la resolución. Si cae un finalista, el sustituto pasa la misma crítica, como en A (A-01). Los dos papeles reciben la misma evidencia fechada y responden sin ver el razonamiento del otro. El matiz es la regla del desacuerdo en N3: manda el veredicto más prudente de los dos, el desacuerdo se declara en la entrega y baja la convicción con la regla de la configuración, sin números en el código. El cliente del segundo proveedor queda preparado; mientras no se contrate (decisión 2 de la tanda 1), se usa el mismo y se declara. |
| Código y funciones fuera | De acuerdo con cambios | **De acuerdo con sus cambios** | Se acepta el rechazo de Astra: la **auditoría previa se conserva al 100 % en N2 y N3** (arquitectura §8, CT-B-19), hecha por el Auditor como papel independiente del Orquestador. En N1 y N0 sigue el muestreo de la V2.1. Nada sale de B (§1). |
| Banco de cuatro variantes | De acuerdo con cambios | **De acuerdo con sus cambios** | Mismos casos y presupuesto de evaluación; calidad, cobertura, daño y coste total, con incertidumbre. Un empate por falta de potencia no da la razón a nadie: se dice «todavía no se sabe». |
| Migración por pasos | De acuerdo con cambios | **De acuerdo con sus cambios** | Contratos y criterios antes de mover responsabilidades. Cada pieza de la V3 se activa sola en la configuración. Primero se ejecuta en paralelo con la V2.1, en sombra, y siempre se puede volver atrás. Se retira «ningún riesgo» de los pasos 1 y 5 de la propuesta. |

**Respuestas a las preguntas de T-68 y del rediseño.** Se toman las de Astra. Cinco papeles era un objetivo, no una condición de éxito: el diseño V3 tiene los que necesitan las obligaciones (§4).

## 4. Diseño V3

### Papeles de IA

| Papel | Firma con | Qué hace | Cuándo | Modelo por defecto (`[PROPUESTO]`, lo decide el banco) |
| --- | --- | --- | --- | --- |
| **Analista de ámbito** | AG-B02 | Encuadre y tesis falsable con hipótesis competidoras (F3); veredicto (F7); filtro de las consultas al Broker (CT-B-28); resolución de las discrepancias que marca el código; respuesta a las objeciones de la tesis | Dos veces (tesis y veredicto), más subsanación | Sonnet en N1 y N2; Opus en N3 |
| **Analista de dimensión** | El ID del especialista del kit (AG-B03 a AG-B11, AG-B24) | Una dimensión, o un lote en N1 y en las no líderes, con núcleo común y kit | Una por dimensión líder; las demás en lotes | Haiku en N1; Sonnet en N2 y N3 |
| **Seleccionador** | AG-B12 | Universo, PC1 a PC8 con el Motor y HT-03, ranking con IC, diversidad, top-N, mejores por eslabón y encargos C.x, con el kit de su tipo | Una por tipo de activo aplicable | Sonnet |
| **Prospectiva** | AG-B13 | Escenarios, sensibilidades y pronósticos PRG-B que se congelan en F4 (R14) | Una en N2 y N3; en N1 va dentro del veredicto | Sonnet |
| **Contradictor** | AG-B14 | Refutación de la tesis y de los finalistas, y de cada sustituto | Una en N2 y N3, más una por ronda de sustitución | Otro proveedor cuando exista |
| **Lector de evidencia** | AG-B25 (nuevo) | Lee web y documentos aislado, sin herramientas de escritura; devuelve datos con fuente y fecha | Solo si hay fuentes externas | Haiku |
| **Auditor** | AG-B22 | Auditoría previa: 100 % en N2 y N3, muestreo en N1 y N0. Diez focos, con módulo por foco | Una por petición N2 y N3 | Opus |
| **Sintetizador** | AG-B17 | Textos llanos del informe visual y del memorando, con marcadores de texto y sin cifras libres (§5, idea 4); el informe técnico y el anexo salen por plantilla | Una por entrega | Sonnet |
| **Respondedor** | AG-B26 (nuevo) | Respuesta N0 a las consultas (CT-B-03), solo desde F1 a F6, RC y los entregables, citando identificadores | Por consulta | Haiku |

Ningún número del cuadro se escribe en el código: modelos, lotes, rondas y topes van en la configuración (regla 2 del proyecto).

### Pasa a código, conservando su identificador

Un papel que pasa a código sigue firmando con su identificador como servicio determinista, igual que en A. Así F1 a F11, RC y HA no cambian de propietario.

| Servicio | Firma | Qué hace |
| --- | --- | --- |
| Coordinador | AG-B01 | Admisión por reglas y por los campos de CT-B-01. Un ámbito dudoso (AMBITO_INDETERMINADO, ASESORAMIENTO_PERSONAL) lo decide el Analista de ámbito en F0. También estimación HT-08, PT30 y PTA, política automática, credenciales, entrega y registro |
| Director | AG-B02 | Máquina de estados: plan con la matriz, grafo, capas, puertas, pausas y reanudación. El juicio es del Analista de ámbito, que también firma como AG-B02 |
| Curador | AG-B15 | Normaliza, deduplica lo exacto, cuenta raíces por la fuente declarada y marca las discrepancias (registro: «independencia por fuente declarada, sin evaluación semántica») |
| Orquestador | AG-B21 | G3 con HT-09, tiempos, colas y autorizaciones de contenido y de salida |
| Evaluador y Vigía | AG-B23 | Resolución de F4, métricas, certificados y comparación de umbrales del Vigía, todo determinista; el informe de aprendizaje con IA, opcional por configuración |
| Documentadores | AG-B18 a AG-B20 | Mantenimiento de F7 a F9 fuera del ciclo, por lotes; la IA, opcional por configuración |

### Un N2 en la V3

1. Coordinador (código): admisión y estimación.
2. Analista de ámbito: encuadre y tesis provisional.
3. Plan por la matriz: dimensiones líderes en paralelo y lotes de las activadas; capas con PV1 a PV3.
4. Seleccionador, uno por tipo, con el Motor y HT-03; y Prospectiva.
5. Contradictor, y sus sustitutos si cae algún finalista.
6. Analista de ámbito: veredicto.
7. G3 y Auditor.
8. Sintetizador y plantillas.
9. Entrega CT-B-02.

El número de llamadas se medirá; según la cuenta de Astra, un N2 no bajará de unas diez.

### Contratos y propietarios

Ningún esquema de contrato cambia, y el corpus congelado no se toca.

| Contrato | Propietario en la V3 | Cambio |
| --- | --- | --- |
| CT-B-01 a CT-B-07, CT-B-26 a CT-B-29 | Coordinador (código); N0 de CT-B-03, el Respondedor | Solo cambia quién redacta la respuesta N0 |
| CT-B-08 | Coordinador → Director (código) | El Director ya no es una llamada de IA |
| CT-B-09 | Director (código) → Analista de dimensión | Cambia el prompt (núcleo y kit), no el contrato |
| CT-B-10 | Director (código) ↔ Seleccionador | Kit por tipo con dependencias |
| CT-B-11 y CT-B-12 | Lector de evidencia en el ciclo; Documentadores fuera del ciclo | — |
| CT-B-13 y CT-B-14 | Motor (código) | Sin cambio |
| CT-B-15 | Curador (código) | La IA, opcional para la ablación |
| CT-B-16 | Prospectiva | Sin cambio |
| CT-B-17 | Contradictor | También sobre cada sustituto |
| CT-B-18 y CT-B-21 | Orquestador (código) | Sin cambio |
| CT-B-19 | Orquestador ↔ Auditor | Sin cambio: 100 % en N2 y N3 |
| CT-B-20 | Director (código) ↔ Sintetizador y plantillas | El Redactor solo escribe textos llanos |
| CT-B-22 a CT-B-25 | Evaluador y Documentadores | El informe con IA, opcional |

## 5. Ideas nuevas

1. **Plan con la matriz del Documento 0.** La matriz de activación (líder, activado, condicional o no activado) y la de pesos y profundidad ya existen en 8.3.1 y 8.3.4. El código las aplica tal cual y registra la exclusión justificada de cada dimensión, así que R17 se cumple por construcción. Esto responde a la objeción de Astra de que el código «no conoce qué dimensión importa»: la conoce el Documento 0.
2. **Exploración medida de lo que el plan deja fuera.** Una rotación sembrada activa de vez en cuando una dimensión condicional no activada. Si cambia la tesis, el veredicto o el top-N, el plan tuvo un falso negativo, y queda contado (como GC1 en A).
3. **Registro de cobertura del embudo y seguimiento contrafactual.** En HA, una entrada por candidato y por dimensión: hasta dónde llegó (universo, PC1 a PC8, finalista, crítica, top-N) y por qué se quedó. Cada run marca una muestra sembrada de candidatos descartados. Cuando vence el horizonte, el Evaluador compara sin IA su rentabilidad con la de los elegidos del mismo tipo y fecha.
4. **Sintetizador sin cifras libres (lección de T-102).** El Sintetizador escribe con marcadores de texto (`{cand:…}`, `{tipo:…}`, `{eslabon:…}`) y nunca cuenta: las cuentas y las cifras las escribe el código en frases propias, con datos del paquete. Un filtro frase a frase quita lo que lleve una cifra, también en letra, o un código de un instrumento, y lo declara. El informe visual ya prohíbe las listas de valores para comprar, y así se garantiza por construcción. El filtro se mide con el banco ciego de un revisor, con los umbrales de INC-T102-01.
5. **Kits derivados mecánicamente de los prompts congelados (como A).** El núcleo y los kits se sacan de los prompts V2.0 al cargarlos, sin escribir contenido nuevo. Una prueba comprueba que núcleo más kit devuelven las mismas secciones que el prompt original. El kit tiene dos variantes, con la base de conocimientos y sin ella, y el banco las compara.
6. **Tabla de obligaciones.** Cada obligación de los prompts del Director, del Coordinador y del Curador (cada «debe», cada puerta, cada campo obligatorio) se lista con su nuevo dueño: código, papel o comprobación de G3. Una prueba falla si una obligación no tiene dueño. Es la respuesta concreta a «registrar qué obligaciones desaparecen del prompt y dónde se conservan».
7. **Consumo determinista con hilos (lección de T-88).** Las escrituras de caché de un prefijo compartido se reparten por grupo de prefijo. Las listas que dependen del orden de los hilos (cierres, limitaciones) se ordenan. Dos ejecuciones iguales deben dar el mismo registro de consumo.
8. **Coste completo y tope del prompt por papel.** Cada llamada registra sus intentos, sus reparaciones y su latencia. Cada papel tiene un tope de tokens de su prompt en la configuración, vigilado por una prueba, para que no vuelva a crecer sin que nadie lo vea.
9. **V2.1 intacta, comprobada.** Con `diseno: v2`, los runs, las llamadas y los paquetes de los ejemplos de redes, India y cobre son idénticos byte a byte antes y después del cambio. Una prueba lo fija, como en A con `r01_v5_sin_cambios`.
10. **Resolución de pronósticos con la regla de A (lección de T-91).** Se comprueba que la resolución de F4 en B usa la fecha común más reciente con frescura por horizonte y los festivos de mercado. Si no la usa, se alinea con INC-T91-01.

## 6. Qué no se hace

- No se cambia el corpus congelado: Documento 0 V2.1, prompts V2.0 ni esquemas de `06_Plantillas_entregables`. Los prompts nuevos de la V3 van en el ejecutor (`prompts_v3/`), fuera del corpus.
- No se mueve nada a I, H, K ni al Orquestador del Broker.
- No se afirma ninguna mejora de calidad. El simulador mide el flujo y el consumo; la calidad se mide en modo sombra con la API real (Fase 5 del plan).
- Si el banco con la API real da la razón a la V3, el Documento 0 V3.0 y su re-congelado son otro paso, con aprobación del operador.
