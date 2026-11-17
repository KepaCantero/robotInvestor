# T-175 · Análisis técnico

## Causa raíz o motivo

`Redaccion.tecnico` (`bloque_a/11_Ejecutor/bloque_a/redaccion.py`) solo recorría `paquete["clases"][c]["opciones"]`, es decir, el top-3. La finalista que HT-03 declara no elegible por una objeción fuerte sin resolver (motivos `PUERTA_NO_SUPERADA` G2 y `OBJECION_FUERTE`) solo quedaba en F3 (`estado` `EN_OBSERVACION`, `elegible` falso, `objeciones_internas`). El técnico no tenía la subsección 4.N.4 «Alternativas descartadas relevantes» de la plantilla V5.0, que §14.1 del Documento 0 V5.3 también pide, y la sección 6 no llevaba esa objeción. Es el hueco que INC-T116-03 dejó en PB-38.

## Evidencia

- Plan V3.0, PB-38: «la objeción figura en el técnico como sin resolver; la opción queda como alternativa documentada».
- Ciclo mock (`AS_OF` 2026-06-05, doce clases): `OPP-2026-0004` (RV, «Sector tecnológico de EE. UU.», RK 64) tiene `OBJ-XLK-02` fuerte sin resolver y no aparecía en ninguna parte del técnico. Antes y después, en `.docs/tickets/T-175/diff_tecnico.py`.

## Implementación

- **Archivos cambiados:**
  - `bloque_a/11_Ejecutor/bloque_a/sintesis.py`:
    - `_objecion_respondida(o)`: la regla del estado (RESPONDIDA / SIN_RESOLVER), sacada de `construir` y compartida con las alternativas, con la misma semántica. Además, si la respuesta no es texto, cuenta como sin responder.
    - `alternativas_descartadas(paquete, extras)`: una función pura que lee `extras["seleccion"]`.
    - `from .herramientas import ht03`: para reutilizar `_que_tendria_que_ocurrir`, la frase de R14.
    - De paso, tres asignaciones de `_ambito`, `_indicador` y `_invertibilidad` se escriben en dos pasos para que mypy estreche el tipo. No cambia el comportamiento y quita 7 errores de mypy.
  - `bloque_a/11_Ejecutor/bloque_a/redaccion.py`:
    - en `tecnico`, la subsección `#### 4.{i}.4` después de la ficha de la última opción de cada clase y las filas «(alternativa descartada)» en la sección 6;
    - `_celda`, que escapa «|» y une las líneas en las celdas nuevas.
  - `bloque_a/11_Ejecutor/tests/test_t175_alternativas.py`: 9 pruebas nuevas.
  - `bloque_a/11_Ejecutor/tests/mapa_plan_pruebas.json`: PB-38 pasa a AUTOMATICA con 5 pruebas más.
  - `docs/evidencias_pruebas_bloque_a.md`: regenerado.
  - `bloque_a/11_Ejecutor/README.md`: una viñeta.
  - `docs/incidencias.md`: INC-T175-01 y la nota «Aplicada en T-175» en INC-T116-03.
  - Deuda técnica: fila T-175.
  - `tools/cuotas.txt`: mypy A, 109 → 102.
- **Decisiones (INC-T175-01 `[PROPUESTO]`):**
  - **Qué filas entran:** las finalistas no elegibles según HT-03 que no son opción, ni vigentes, ni de arrastre.
  - **Orden:** por RK descendente y, a igual RK, por `opp_id`.
  - **Tope:** no se escribe el «máx. 5». Lo da `seleccion.max_finalistas`.
  - **Sección 6:** van las objeciones fuertes y moderadas de las alternativas.
  - **Entregables:** solo cambia el técnico.
- **Fallo cerrado:**
  - No se lista una candidata sin `_ht03`, sin `opp_id` de texto, con `elegible` que no sea `False` o sin motivos.
  - Una objeción que no es un dict se ignora.
  - Un resumen o una respuesta que no es texto se escribe «—».
- **G3-MET-13:**
  - El texto que escribe el ejecutor no lleva la raíz «valid-». Lo comprueba una prueba.
  - El nombre, la objeción y «qué la resolvería» vienen del modelo y ya pasaron la reescritura R22 del camino de invocación.
  - Como el técnico entero se comprueba después (`g3_met13_tecnico`), una mención indebida en una alternativa bloquea la entrega. Antes, la de una candidata no entregada era una advertencia. Es deliberado, porque ahora se presenta al Broker. Lo prueba `test_g3_met13_lee_las_filas_de_la_alternativa_y_bloquea`.
- **Coherencia G3-ENT-07:** no cambia. Las alternativas no usan `##### N.` ni la celda `· \`OPP\` | RK |`.
- **Límites conocidos:**
  - En el diseño V6 el simulado resuelve la objeción fuerte. La prueba V6 hace que la contrarréplica no convenza (`resuelta` falso) para crear el caso.
  - Las subsecciones 4.N.1, 4.N.2 y 4.N.5 y los «veredictos globales» de la sección 6 siguen sin estar: no son de PB-38.
- **Comandos:**
  - `cd bloque_a/11_Ejecutor && ../../.venv/bin/python -m pytest -q tests/test_t175_alternativas.py tests/test_autocritica.py`
  - `.venv/bin/python .docs/tickets/T-175/mutantes.py` (desde la raíz; 12 mutantes)
  - `cd bloque_a/11_Ejecutor && ../../.venv/bin/python ../../.docs/tickets/T-175/diff_tecnico.py generar /tmp/despues.md`, y `comparar antes.md despues.md` (con el «antes» generado en una copia de origin/develop anterior)
  - `.venv/bin/python .docs/scripts/evidencias_plan_a.py --pb PB-38`

## Ronda r02 (QA r01 NO APTO)

- **H-01 (alta): un texto del modelo sobre una alternativa bloqueaba la entrega entera.**
  - **Qué cambia:**
    - `sintesis.alternativas_descartadas(paquete, extras, bloque=None)`. Con `bloque`, sustituye todo texto del modelo de la alternativa que G3-MET-13 rechazaría en el técnico: la raíz «valid-» (`ht09.tiene_raiz_valid`, sin mirar el ámbito, porque en el técnico la tabla entera es un párrafo) o una incidencia de las reglas A a C (`_comprobar_met13`).
    - **Qué se sustituye:**
      - el nombre, por el símbolo de seguimiento (`proxy`);
      - el resumen y la respuesta de una objeción, por `TEXTO_RETIRADO_MET13` («Texto del modelo retirado por G3-MET-13 (R22); íntegro en F3»);
      - el «qué la resolvería», que se omite.
    - La fila se mantiene, como pide PB-38, y `retirados` dice qué se quitó.
    - `redaccion.generar` la calcula una vez tras `ht09_validar`, con el bloque, y la deja en `extras["alternativas_descartadas"]`, que es lo que lee `tecnico`.
    - `sintesis.advertir_alternativas_retiradas` suma una ADVERTENCIA a G3-MET-13. La pone delante, porque el G3V de F7 en HA guarda los cinco primeros detalles. Nunca rebaja un BLOQUEO.
  - **Efectos:**
    - La entrega sale ENTREGADA con dictamen APTO_CON_ADVERTENCIAS.
    - Lo que escribe el ejecutor sigue pasando `g3_met13_tecnico`.
    - CA-6 se reformula.
  - **Pruebas y mutantes:**
    - `test_un_texto_del_modelo_que_g3_met13_rechaza_en_una_alternativa_se_retira_y_la_entrega_sale` sustituye a `test_g3_met13_lee_las_filas_de_la_alternativa_y_bloquea`. Tiene dos variantes: una ficha desconocida con un modelo que obedece, y «validada» que persiste tras la reescritura.
    - `test_la_sustitucion_cubre_nombre_resumen_respuesta_y_que_la_resolveria` cubre «validada» sin método en el texto, la regla de no rebajar un BLOQUEO y el caso sin retirados.
    - Hay seis mutantes nuevos.
- **H-02 (baja): datos mal formados.**
  - `motivos_no_elegible`, `_objeciones` y `candidatos` se comprueban como listas.
  - El RK solo se usa si es un número finito y no booleano (`_rk_valido`).
  - Hay cinco casos nuevos en la prueba de filtro y orden, y cuatro mutantes.
- **H-03 (baja): textos.**
  - El docstring de la prueba V6 dice ahora «V6 de solo RV».
  - En `pruebas.md`, CA-4 incluye el ciclo V6 de doce clases.
  - INC-T175-01 avisa de que con `seleccion.max_finalistas` mayor que 5, 4.N.4 puede pasar de 5 filas.
- **Rebase:** se rebasó sobre origin/develop (`375d24b`, T-171).
  - Solo hubo un conflicto, en la deuda técnica: se conservan las filas T-171, T-172 y T-175.
  - `sintesis.py` y `redaccion.py` no cambiaron arriba entre `80751da` y `375d24b`: T-165 ya estaba en la base.

## Ronda de cierre de la QA r02 (APTO con H-04, bajo)

- **H-04.** Con cinco o más alternativas con texto retirado, el BLOQUEO de G3-MET-13 quedaba fuera de los cinco detalles del G3V de F7.
- **Corrección:**
  - `redaccion.detalles_g3v`: el detalle del G3V ordena los BLOQUEOS delante (ordenación estable).
  - `sintesis.bloqueos_delante` deja los BLOQUEOS delante en las incidencias guardadas. Se aplica en `advertir_alternativas_retiradas` y en `g3_met13_tecnico`, tras añadir el bloqueo del técnico.
  - El comentario de `advertir_alternativas_retiradas` está corregido.
- **Desviación de la corrección propuesta:** además del `sorted` en redaccion, ahora también se ordenan las incidencias guardadas. El script del revisor `r02_01` reproduce la lista guardada (`[:5]` sin ordenar). Así, el criterio del revisor se cumple en las dos lecturas.
- **Pruebas:** dos nuevas, `test_un_bloqueo_de_g3_met13_no_queda_tapado_por_seis_alternativas_retiradas_en_el_g3v` y `test_el_bloqueo_que_anade_el_tecnico_va_delante_de_las_advertencias_de_las_alternativas`.
- **Mutantes:** tres nuevos. 25 de 25 muertos.
