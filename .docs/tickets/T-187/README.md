# T-187 · Bloque A, PB-51: conocimiento específico en los system prompts

| Campo | Valor |
| --- | --- |
| Estado | CERRADO (18-11-2026, QA r02 APTO) |
| Pieza | bloque_a (solo lectura de `02_System_prompts`, del Documento 0 y de la configuración; no se toca el corpus ni el código del ejecutor: solo una prueba nueva y el mapa del plan) |
| Planifica · implementa · QA | claude · claude · revisores independientes (paso 3) y el otro agente (QA) |
| Aprobación del operador | no necesaria (pruebas y documentación); las orientaciones de tamaño quedan para T-57 |
| Deuda técnica | T-187 en `sistema_global/seguimiento/Deuda_tecnica_y_pendientes_del_operador.md` |

## Objetivo

Ejecutar PB-51 del plan de pruebas del Bloque A (`bloque_a/09_Pruebas/Plan de pruebas del Bloque A - V3.0.md`): estructura del Anexo G (paso 1), recuento de la sección 10 por área (paso 2) y muestra de 10 afirmaciones por prompt contrastada por revisores independientes (paso 3), con un script sin red y determinista.

## Alcance

- Entra: el script `.docs/scripts/revision_prompts_pb51.py`, sus pruebas (`.docs/scripts/pruebas_revision_prompts_pb51.py`) y mutantes (`.docs/scripts/mutantes_revision_prompts_pb51.py`), con su fila en `.docs/README.md` y la línea base de `.docs/scripts/linea_base_pruebas.txt` (desde la r02, QA r01 H-06; antes estaban en el ticket); en el ticket, el informe `informe_pb51.md` y la muestra `muestra_afirmaciones.json` que genera; el contraste del paso 3 (lectura y validación de los veredictos de `veredictos/`, recuentos y sección del informe); las incidencias INC-T187-01, INC-T187-02 (denominador) e INC-T187-03 (erratas) en `docs/incidencias.md`; la prueba `bloque_a/11_Ejecutor/tests/test_t187_pb51.py` y la fila PB-51 del mapa del plan (`tests/mapa_plan_pruebas.json`) con las evidencias regeneradas; la fila T-187 de la deuda técnica.
- No entra: juzgar las afirmaciones (lo hicieron cuatro revisores independientes); corregir los prompts (corpus congelado: INC-T187-03, para la próxima entrega); fijar topes de tamaño (operador, T-57); comprobar con red que los DOI existen.

## Diseño

- Contratos y estado persistido: no cambian.
- Entradas: los 36 `.md` de `bloque_a/02_System_prompts` (35 prompts y 1 plantilla), el Anexo G del Documento 0 vigente (se lee del archivo, no se copia), `v6.tope_tokens_system` de la configuración y, del ejecutor, `NOMBRES_ALTERNATIVOS`, `ANALISTAS_TIPO` y `_tokens_aprox` (se importan, no se copian).
- Números y su origen: 10 afirmaciones por prompt (PB-51, paso 3); topes de tamaño (configuración, `[PROPUESTO]` de T-101); la semilla es un texto («T-187 · PB-51»), no un número. Único parámetro técnico: comparar títulos por las 6 primeras letras de cada palabra (declarado en el script).
- Cómo falla cerrado: sale con 2 si no hay exactamente un Documento 0, si no hay prompts, si falta la configuración o su clave de topes; lanza si el Anexo G no es una lista numerada 1..n o si una frase de la muestra no es copia exacta del prompt. Paso 3: sale con 2 si falta o sobra un id respecto a la muestra, si un id se repite (en un lote o entre lotes), si hay un veredicto desconocido, una nota sin letras ni cifras o de más de 40 palabras, un revisor en blanco, un lote o el comentario que no se puede leer (JSON, UTF-8 o una carpeta), si no hay lotes o si el comentario no casa con los veredictos (erratas = ERRONEA; dudosas = las CORRECTA con matiz en la nota; discutibles solo si su nota lo dice; cada `cita_nota` es un fragmento literal de la nota; sensibilidad ⊆ ERRONEA); no escribe nada, sin traza.
- Decisiones `[PROPUESTO]`: los criterios de INC-T187-01 (estructura completa, plantilla fuera del denominador, orientación de tamaño, referencias estrictas y amplias) y el denominador del 95 % de INC-T187-02 (las verificables).

## Riesgos

| Riesgo | Consecuencia | Mitigación |
| --- | --- | --- |
| Los recuentos son heurísticos (expresiones regulares) | Cifras con falsos positivos o negativos | Criterios explícitos en `analisis-tecnico.md`, casos sintéticos por criterio y 41 mutantes muertos; las cifras se presentan como recuento mecánico, no como juicio |
| Frases mal cortadas en la muestra | Afirmaciones ininteligibles para el revisor | Abreviaturas, iniciales, código, comillas y paréntesis abiertos no cortan; cada frase lleva la línea y el texto exacto, y el revisor puede marcarla NO_VERIFICABLE |
| Sin orientación de tamaño para 21 papeles | El criterio «tamaños dentro de las orientaciones» no se puede cerrar | INC-T187-01; se informa la medida y se espera a T-57 |

## Criterios de aceptación (binarios)

1. CA-1: el script comprueba en cada prompt las secciones del Anexo G (presentes, únicas, en orden) y la coherencia de sus títulos, y el informe lo tabula por prompt y por sección.
2. CA-2: el informe cuenta, por subárea 10.x de cada prompt, definiciones, fórmulas, umbrales, trampas y referencias con los criterios documentados.
3. CA-3: detecta las entradas de referencias canónicas sin autor, año o título y valida la estructura de los DOI (y el dígito de control de ISBN e ISSN), declarando que la existencia no se comprueba.
4. CA-4: mide palabras, líneas, caracteres y tokens aproximados de cada prompt y los compara con la orientación propuesta donde la hay.
5. CA-5: la muestra tiene 10 afirmaciones por prompt (o todas las candidatas si hay menos), reproducible con la semilla, con texto exacto, prompt, sección, línea y referencia citada, y sin veredicto.
6. CA-6: sin red y determinista (dos ejecuciones dan los mismos archivos; `--comprobar` lo verifica).
7. CA-7: pruebas sintéticas en verde y todos los mutantes muertos.
8. CA-8: INC-T187-01 registrada con el criterio propuesto.
9. CA-9: el paso 3 lee los cuatro lotes, falla cerrado (2) con ids que faltan, sobran o se repiten, veredictos desconocidos o notas de más de 40 palabras, y da los recuentos por lote, por prompt y totales con los dos denominadores; INC-T187-02 (denominador) e INC-T187-03 (las 9 erratas, para la próxima entrega del corpus) registradas; el informe da los verificables por prompt y los que no llegan a 10, y los veredictos por fuente declarada; PB-51 sale «Superada en parte» en las evidencias, con el resultado esperado incumplido (9 ERRONEA) y los 21 papeles sin orientación en «No comprueba».

## Plan de pruebas

| Prueba | Tipo | Criterio |
| --- | --- | --- |
| Anexo G, secciones, títulos, faltan/sobran/repetidas/orden, código | nominal, límite, fallo cerrado | CA-1 |
| Subáreas, elementos, definiciones, fórmulas, umbrales, trampas, inventario excluido | nominal, límite | CA-2 |
| Citas (formas A, B, C, partículas, falsos autores), entradas de lista, estricto y amplio, DOI, ISBN, ISSN | nominal, límite | CA-3 |
| Tamaño con tope propio, de analista y sin tope | nominal | CA-4 |
| Frases, marcas, candidatas, muestra determinista | nominal, regresión | CA-5 |
| De punta a punta en un repositorio sintético, `--comprobar`, dos ejecuciones iguales, sin Documento 0, con dos, sin topes | integración, fallo cerrado | CA-6 |
| Corpus real: lo guardado coincide con lo generado | regresión | CA-6 |
| `.docs/scripts/mutantes_revision_prompts_pb51.py` | mutación | CA-7, CA-9 |
| Contraste: recuentos, límite del 95 %, sensibilidad, verificables por prompt y cortos, veredictos por fuente, ids que faltan/sobran/repetidos, veredicto desconocido, nota de 40/41 palabras, vacía o sin letras, comentario que no casa (cita que no está en la nota, dudosos fuera del criterio, discutible sin apoyo), lotes sin formato, UTF-8 inválido o carpeta, de punta a punta con veredictos | nominal, límite, fallo cerrado, integración | CA-9 |
| Corpus real: los veredictos guardados dan 260/9/81 y superan | regresión | CA-9 |
| `bloque_a/11_Ejecutor/tests/test_t187_pb51.py` (PB-51 en el mapa, «Superada en parte») | regresión | CA-9 |

## Resultados (pasos 1 y 2)

- **Paso 1:** 35 de 35 prompts con las 12 secciones, únicas y en orden (100 %). 12 títulos de la §6 («Estrategia de análisis…», los Analistas de tipo de activo) no comparten palabra con «Metodología y criterios de decisión propios»: variantes por diseño, no suspenden. La plantilla tiene 10 secciones (faltan la 6 y la 10, por diseño).
- **Paso 2:** las 35 secciones 10 están partidas en subáreas (623 en total). Recuento mecánico (sin el inventario de competencias): 3 810 elementos, 1 717 definiciones, 1 704 fórmulas, 355 umbrales, 483 trampas y 2 172 referencias. Por prompt y subárea en `informe_pb51.md`.
- **Referencias:** 8 prompts no tienen subárea de referencias canónicas (Auditor, Buscador, Coordinador, Curador, Documentador del Motor, Evaluador, Orquestador y Redactor; citan en el texto). De las 674 entradas de las listas, 656 llevan autor y año (97,3 %; las 18 restantes son manuales citados sin año, como «Hull (‹Options, Futures…›)»), 448 llevan título en la entrada (66,5 %) y 465 con el criterio amplio (69,0 %). Ningún prompt escribe un DOI, ISBN o ISSN concretos.
- **Tamaños:** los 14 papeles con tope en la configuración (12 Analistas de tipo de activo, AG-10 y AG-11) quedan dentro; los otros 21 no tienen orientación escrita (INC-T187-01).
- **Paso 3 (preparado):** 350 afirmaciones, 10 por cada uno de los 35 prompts (candidatas por prompt: de 33 a 203); 297 de la §10 y 53 de la §6; 72 citan una referencia en la propia frase y 23 más en su elemento.
- **Paso 3 (contraste):** cuatro revisores independientes, un lote cada uno (lote 1: 66/2/22; lote 2: 58/5/27; lote 3: 74/2/14; lote 4: 62/0/18, CORRECTA/ERRONEA/NO_VERIFICABLE; recuentos comprobados por el script). Total: 260 CORRECTA, 9 ERRONEA y 81 NO_VERIFICABLE: **96,7 %** sobre las 269 verificables (criterio de INC-T187-02) y 74,3 % sobre las 350. El paso 3 pasa el umbral (≥ 95 %). Sensibilidad con AF-AG-22-03 y AF-AG-24-05 (las elige quien escribe el comentario; ningún revisor las llama discutibles): contadas como correctas, 97,4 %; quitadas, 97,4 %: el veredicto no cambia. 28 de 35 prompts tienen menos de 10 verificables (mínimo 2, el Coordinador). Por la fuente que declaran las notas, 249 de las 260 CORRECTA se juzgaron de memoria, 3 con búsqueda web y 8 con un cálculo a mano. El lote 2 queda en 92,1 % por sí solo, y AG-25 (71,4 %) y AG-19 (80,0 %) son los prompts más bajos. Las 9 erratas, en INC-T187-03 para la próxima entrega del corpus; la tabla por prompt, la tabla por fuente, las erratas y los cinco casos dudosos (AF-MC-02-04, AF-MC-06-02, AF-MC-07-10, AF-AG-13-09 y AF-AG-17-04: las CORRECTA con matiz en la nota), en `informe_pb51.md`.
- **Plan de pruebas:** PB-51 pasa de «Revisión documental» a **«Superada en parte»** (`tests/test_t187_pb51.py` ata el informe, la muestra y los veredictos al corpus actual). En «No comprueba», primero el resultado esperado que no se cumple (9 ERRONEA, INC-T187-03, pendientes de la entrega del corpus) y los 21 papeles sin orientación de tamaño (INC-T187-01, T-57); después, los verificables por prompt, la fuente de los veredictos y los criterios `[PROPUESTO]`.

## Scripts

- `.docs/scripts/revision_prompts_pb51.py` (genera el informe y la muestra en este ticket; `--comprobar`).
- `.docs/scripts/pruebas_revision_prompts_pb51.py` (las recoge `.docs/scripts/pruebas_scripts.sh`) y `.docs/scripts/mutantes_revision_prompts_pb51.py`.
- `.docs/tickets/T-187/veredictos/` (entradas del paso 3: `lote_1.json` a `lote_4.json` de los revisores y `comentario.json` con las erratas, los casos dudosos, las discutibles y la sensibilidad, cada caso con su cita literal de la nota).

## Registro

- 2026-11-18 · ABIERTO · creado con nuevo_ticket.sh
- 2026-11-18 · EN CURSO · claude · pasos 1 y 2 hechos y paso 3 preparado (350 afirmaciones); falta el contraste del paso 3 por revisores independientes y la QA
- 2026-11-18 · EN QA (r01) · claude · paso 3 contrastado (cuatro revisores: 260/9/81, 96,7 % sobre las verificables, pasa); INC-T187-02 e INC-T187-03; PB-51 «Superada»; a la QA del otro agente
- 2026-11-18 · EN QA (r02: QA r01 NO APTO) · claude · H-01 a H-07 corregidos: PB-51 «Superada en parte»; verificables por prompt y fuente de los veredictos en el informe e INC-T187-02; comentario con citas literales y criterio de dudosos; fallo cerrado sin traza; script movido a `.docs/scripts/`; título del paso 3
- 2026-11-18 · EN QA (ronda de cierre de la QA r02) · claude · QA r02 APTO con H-08 y H-09 (bajos): rutas viejas fuera de la allowlist y marcadas en el diario; cita de la nota de al menos 3 palabras (`MIN_PALABRAS_CITA` `[PROPUESTO]`) y columna «Cita de la nota» en el informe
- 2026-11-18 · CERRADO · claude (QA) · ronda de cierre de la QA r02 APTO: H-08 y H-09 corregidos (H-01 a H-07 de la r01, en la r02); PB-51 «Superada en parte»; ningún hallazgo abierto
