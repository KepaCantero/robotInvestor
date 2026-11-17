# T-175 · QA independiente

- **Revisor:** claude (subagente revisor nuevo, sin el contexto de la implementación) · **Ronda:** r01 · 2026-11-17
- **Objeto:** `wip/t175` (`9761373`) sobre develop `80751da`, en una copia de trabajo aparte. La comparación se hizo contra otra copia de `80751da`.

## Reproducción desde limpio

Por orden del coordinador, no se repasaron la suite completa ni el gate: los pasó el implementador. Lo que sí se repasó:

| Comprobación | Resultado |
| --- | --- |
| `pytest -q tests/test_t175_alternativas.py` | 9 superadas |
| `.docs/tickets/T-175/mutantes.py` | 12/12 muertos |
| mypy A (`--ignore-missing-imports`, el comando del gate) | 109 en `80751da` → 102 en `9761373`. Las 7 que desaparecen son de `sintesis.py`: 6 `union-attr` (`_ambito`, `_indicador`, `_invertibilidad`) y 1 `index` (el `ok` de `construir`). |
| `revisores/r01_03_regresion.py`, ciclo mock de doce clases V5 y V6 en las dos copias | JSON y visual idénticos (V5 y V6). En el técnico V5 solo aparecen 4.1.4 y 2 filas de la sección 6 (10 líneas, lo que dice `diff_tecnico.py`). En el técnico V6 solo aparecen 4.2.4 y 4.4.4 y 4 filas de la sección 6. Las dos entregas son APTO. |
| `diff_tecnico.py comparar` (V5) | 10 líneas nuevas esperadas · 0 cambios fuera de lo esperado |
| Backtest mock del README (`2024-01-05`–`2024-03-29`) en las dos copias | `senales.csv`, `pronosticos.csv` y `metricas.json` idénticos byte a byte |

## Criterios de aceptación

| Criterio | Cumple | Evidencia |
| --- | --- | --- |
| CA-1 | sí | `test_pb38_…_alternativa_documentada_en_el_tecnico`. En el técnico de doce clases, la fila de `OPP-2026-0004` lleva G2, `OBJ-XLK-02` y lo que tendría que ocurrir. |
| CA-2 | sí | Sección 6: `` `OPP-2026-0004` (alternativa descartada) · fuerte · … · SIN_RESOLVER `` |
| CA-3 | sí | La OPP no aparece en el JSON, la coherencia sale vacía y el dictamen es APTO (`r01_03`; prueba del implementador) |
| CA-4 | sí | `diff_tecnico.py` y `r01_03` (V5 y V6): solo cambian 4.N.4 y las filas «(alternativa descartada)» |
| CA-5 | sí, con H-02 | `r01_01_casos_raros.py`: vigentes, de arrastre, elegibles, sin OPP, sin HT-03 y sin motivo no se listan. Hay dos estructuras mal formadas que sí rompen el informe (H-02). |
| CA-6 | **no, por diseño** | El criterio pide justo lo que H-01 señala como defecto. El ejecutor no escribe la raíz (cumple). Lo que no se sostiene es que el texto del modelo sobre una alternativa bloquee la entrega entera (H-01). |
| CA-7 | sí | PB-38 está «Superada» en el mapa y en las evidencias (33 · 25), y mypy A da 102. La suite y el gate los declara el implementador y no se repasaron. |

## Contraste del criterio de PB-38 con el corpus

- **Plan V3.0, PB-38.** El resultado esperado es: «la objeción figura en el técnico como sin resolver; la opción queda como alternativa documentada». Se cumple con 4.N.4 y con la fila de la sección 6.
- **Plantilla del técnico V5.0.**
  - 4.N.4 tiene las columnas Candidata · Puerta en la que quedó · Motivo · Qué tendría que ocurrir, con «máx. 5, las más cercanas al umbral». Las columnas y la posición coinciden: va tras las fichas y antes de la sección 5.
  - La sección 6 pide «todas las fuertes y moderadas», y así se hace.
- **Documento 0 V5.3, §14.1.** Pide «alternativas descartadas relevantes» por clase, y se cumple.
- **INC-T175-01.** La decisión es razonable y está documentada como `[PROPUESTO]`.
  - Lista solo las no elegibles y ordena por RK, porque no hay una medida común de «cercanía al umbral».
  - Observación para el operador: «las más cercanas al umbral» también se puede leer como las elegibles que se quedan fuera por RK, que INC-T175-01 deja fuera. Es una lectura defendible y está a la vista, así que no es un hallazgo.
  - El tope de 5 depende de `seleccion.max_finalistas` (5). Si el operador lo sube, 4.N.4 puede pasar de 5 filas. Conviene decirlo en la incidencia (ver H-03).
  - Excepto en el punto de G3-MET-13, que se discute en H-01.

## Las 7 correcciones de mypy

Las tres de `_ambito`, `_indicador` e `_invertibilidad` son equivalentes: leen una vez en lugar de dos el mismo `dict.get`.

La de `construir` cambia a `_objecion_respondida`, que difiere solo con datos mal formados:
- una `respuesta` que no es texto pero tiene longitud de 10 o más (antes RESPONDIDA, ahora SIN_RESOLVER);
- una objeción sin `fuerza` o sin `resuelta` (antes `KeyError`).

En el camino real, `respuesta` siempre es texto o `None`: solo se asigna tras `(x.get("respuesta") or "").strip()`. Las dos diferencias van hacia el lado prudente. El backtest y los ciclos V5 y V6 dan lo mismo, así que no hay cambio de comportamiento observable.

## Hallazgos

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección sugerida | Estado |
| --- | --- | --- | --- | --- | --- |
| H-01 | alta | `cd bloque_a/11_Ejecutor && ../../.venv/bin/python ../../.docs/tickets/T-175/revisores/r01_02_met13_alternativa.py alternativa "Falta el cálculo RISK-XYZ-999 de la cola." obedece` (un Contradictor que nombra una ficha que no existe en la objeción fuerte de la candidata que acaba como alternativa; el modelo obedece R22). Variante: `… alternativa` sin más argumentos (la raíz «valid-» persiste tras la reescritura, o la reescritura no cabe en la bolsa y no se pide). | **Esperado:** la misma proporción que con una opción del top-3. Con el mismo texto en una opción, F6 retira esa opción y entrega el resto (`… opcion "Falta el cálculo RISK-XYZ-999 de la cola." obedece`: ENTREGADA, top-3 sin XLU). En `80751da`, ese texto de una candidata no entregada es una ADVERTENCIA («no se presenta al Broker», docstring de `sintesis.g3_met13`). **Obtenido en `9761373`:** **toda la entrega BLOQUEADA** por G3-MET-13 en F7, con las doce clases si el ciclo es completo. En F6 queda una ADVERTENCIA; luego `g3_met13_tecnico` lee la fila de 4.N.4 o de la sección 6 como BLOQUEO y no hay retirada posible. El caso de la regla B (ficha desconocida, o VOL-GARCH-001 sin `arch`) **ni siquiera pasa por la reescritura R22**, que solo mira la raíz «valid-». Un solo texto del modelo sobre una candidata que no se entrega deja al Broker sin la entrega de la semana. | No presentar en el técnico un texto del modelo de una alternativa que G3-MET-13 rechazaría. Se sustituye por texto del ejecutor y se mantiene la fila, que es lo que pide PB-38. En `sintesis.alternativas_descartadas`, que pasa a recibir `bloque`: (1) por cada texto del modelo de la alternativa (`nombre`, y `resumen`, `respuesta` y `que_la_resolveria` de sus objeciones), si `ht09.tiene_raiz_valid(t)` o `_comprobar_met13(bloque, [("informe_tecnico", t, "BLOQUEO")])["incidencias"]` no está vacío, sustituirlo: el nombre por `f["proxy"]`, y el resumen o la respuesta por «Texto del modelo retirado por G3-MET-13 (R22); íntegro en F3». El `que_la_resolveria` se omite. (2) Dejar en HA una incidencia «G3-MET-13: texto de la alternativa `OPP-…` retirado del técnico», o reutilizar la ADVERTENCIA de F6, que ya existe. (3) Cambiar CA-6, `test_g3_met13_lee_las_filas_de_la_alternativa_y_bloquea`, el README del ejecutor y el último punto de INC-T175-01. La prueba nueva: con «validado» y con una ficha desconocida en la objeción de la alternativa, la entrega sale ENTREGADA, la fila de 4.N.4 está con el texto sustituido y hay una ADVERTENCIA de G3-MET-13. (4) Añadir un mutante que quite la sustitución. Lo que escribe el ejecutor sigue pasando por `g3_met13_tecnico`, así que el control no se relaja. | abierto |
| H-02 | baja | `../../.venv/bin/python ../../.docs/tickets/T-175/revisores/r01_01_casos_raros.py` (casos «motivos int», «_objeciones int» y «RK True/nan/inf») | **Esperado** (docstring y diseño: «una candidata mal formada no se lista ni rompe el informe»): no se lista. **Obtenido:** con `motivos_no_elegible` o `_objeciones` que no son lista, `TypeError: 'int' object is not iterable`, que rompería el técnico en F7. Un RK booleano sale como «(RK True)» y uno NaN desordena la lista. Hoy el ejecutor escribe esas estructuras (HT-03, `_objeciones_arrastre`), así que no se llega a esto en la práctica. | En `alternativas_descartadas`: `mot = ev.get("motivos_no_elegible"); motivos = [m for m in (mot if isinstance(mot, list) else []) if isinstance(m, dict) and m.get("codigo")]`. Además, `objs_crudas = f.get("_objeciones"); objs = [o for o in (objs_crudas if isinstance(objs_crudas, list) else []) if …]`, y `rk if isinstance(rk, (int, float)) and not isinstance(rk, bool) and math.isfinite(rk) else None`. Añadir los tres casos a `test_solo_se_listan_…`. | abierto |
| H-03 | baja | Lectura | El docstring de `test_pb38_tambien_en_el_diseno_v6` y `handoff.md` dicen «en el V6 el simulado resuelve la objeción fuerte». Solo es así en el ciclo de RV solo: en el ciclo V6 de doce clases salen 4.2.4 (`OBJ-EMB-02`) y 4.4.4 (`OBJ-DBC-02`) sin forzar nada (`r01_03`). CA-4 (`pruebas.md`) solo cita el diff V5. INC-T175-01 no dice que el tope de 5 depende de que `seleccion.max_finalistas` siga en 5. | En el docstring: «En el V6 de solo RV el simulado resuelve la objeción fuerte…». En `pruebas.md`, CA-4: añadir «V6 de doce clases: solo 4.2.4, 4.4.4 y 4 filas de la sección 6; JSON y visual idénticos». En INC-T175-01, tras «5 en `config/por_defecto.yaml`»: «si el operador sube `seleccion.max_finalistas`, 4.N.4 puede pasar de 5 filas». | abierto |

Observaciones (no son hallazgos):
- `_celda` no escapa las comillas invertidas: un nombre con una sola «`» descuadra el código en línea de la celda. Es cosmético y el top-3 tampoco las escapa.
- La cabecera de las evidencias cita `80751da`, el commit sobre el que se generaron antes del commit de trabajo. Es la costumbre del script.

## Invariantes

- No hay LLM en la ruta determinista: `alternativas_descartadas` es pura y lee `extras`.
- No hay números escritos a mano: el 10 de `_objecion_respondida` ya existía.
- Formatos congelados: JSON y esquema intactos.
- Sin secretos ni datos personales.
- Decisiones en INC-T175-01 `[PROPUESTO]`.
- G3-MET-13 sigue leyendo el técnico entero: el control no se relaja. H-01 no pide relajarlo, sino no presentar el texto rechazado.

## Veredicto

**NO APTO.** H-01 es alta: un texto del modelo sobre una candidata que no se entrega, como una ficha desconocida o la raíz «valid-» que persiste, bloquea la entrega entera de la semana. Con el mismo texto en una opción del top-3, solo se retira esa opción, y antes de T-175 era una advertencia. La parte de la regla B ni siquiera pasa por la reescritura R22.

PB-38 queda bien cubierto en lo demás:
- columnas, sección 6 y regla del estado;
- casos raros de nombres;
- sin alternativas;
- vigentes y arrastre;
- mypy sin cambio de comportamiento;
- ciclos V5 y V6 y backtest sin regresiones fuera de lo declarado.

H-02 y H-03 son bajos y se corrigen en el mismo ticket. En la r02, el revisor vuelve a ejecutar `revisores/r01_01`, `r01_02` (las dos variantes y el modo `opcion`) y `r01_03`.

## Ronda r02

- **Revisor:** claude (el mismo revisor de la r01, que no implementó) · 2026-11-17
- **Objeto:** `wip/t175` `55ad862` (r02), sobre `484d07d` (la r01 rebasada sobre develop `375d24b`), en una copia de trabajo nueva. Se comparó con otra copia de `375d24b`.
- Por orden del coordinador, no se repasaron la suite completa ni el gate.

### Scripts del revisor, otra vez

| Script | Resultado |
| --- | --- |
| `r01_01_casos_raros.py` | Todo OK. Las listas mal formadas ya no rompen nada (H-02). Un RK booleano, NaN, infinito o de texto se escribe como `None` y queda al final. |
| `r01_02 … alternativa` (la raíz «valid-» persiste) | **ENTREGADA**, sin bloqueos. G3V-F7 da APTO_CON_ADVERTENCIAS (G3-MET-13 con 5 advertencias). 4.N.4 está, y «validada» no aparece en el técnico. |
| `r01_02 … alternativa "Falta el cálculo RISK-XYZ-999 de la cola." obedece` (regla B) | **ENTREGADA**, sin bloqueos, con APTO_CON_ADVERTENCIAS y 4.N.4. |
| `r01_02 … opcion` con las dos variantes | Igual que en la r01: F6 retira la opción y el resto se entrega. |
| `r01_03_regresion.py` frente a `375d24b` | JSON y visual idénticos en V5 y V6. `diff_tecnico.py comparar`: V5 con 10 líneas esperadas y 0 fuera de lo esperado; V6 con 20 y 0. El técnico V5 de la r02 es idéntico al de la r01. |
| Backtest del README frente a `375d24b` | `senales.csv`, `pronosticos.csv` y `metricas.json` idénticos byte a byte |

También se pasaron, solo para este ticket:
- `pytest tests/test_t175_alternativas.py`: 11 superadas;
- `mutantes.py`: 22/22 muertos.

### H-01 a H-03 de la r01

| ID | Estado | Evidencia |
| --- | --- | --- |
| H-01 | corregido | Ver `r01_02` arriba. En el técnico se sustituye el nombre (por el símbolo), el resumen y la respuesta (por el aviso), y se omite «qué la resolvería». La fila se mantiene. Queda una ADVERTENCIA de G3-MET-13 en el G3V de F7. Lo que escribe el ejecutor sigue pasando por `g3_met13_tecnico`. |
| H-02 | corregido | `r01_01` |
| H-03 | corregido | Docstring de la prueba V6, `handoff.md`, `pruebas.md` (CA-4 con el V6 de doce clases) y INC-T175-01 (el tope depende de `seleccion.max_finalistas`) |

### 1. ¿Hay otros textos del modelo en 4.N.4 o en la sección 6 que se escapen de la sustitución?

**Qué hay en cada parte:**
- **4.N.4.**
  - Texto del modelo: el nombre y el «qué la resolvería» de las fuertes abiertas.
  - Texto del ejecutor: la `OPP-`, el RK, la puerta, el motivo y la condición. El motivo es el `detalle` de HT-03 y la condición, `_que_tendria_que_ocurrir`.
- **Sección 6.**
  - Texto del modelo: el resumen y la respuesta.
  - Texto del ejecutor: `objecion_id`, la fuerza (un valor de enum) y el estado.

Los cuatro campos del modelo pasan por `_texto_rechazado`.

**Prueba:** `revisores/r02_01_fugas_y_orden_ha.py` prueba 17 textos en cada uno de los cuatro campos:
- la raíz «valid-» con sus variantes («Revalidar», «convalidado», «VALIDACIÓN», «válido»);
- una ficha desconocida;
- una forma canónica falsa;
- un «[madurez: …]» suelto;
- «implementado»;
- un identificador partido por un salto de línea o por «|»;
- guiones que no son ASCII;
- VOL-GARCH-001 y AUD-REX-001.

**Método:** después de la sustitución, se lee con `_comprobar_met13` la parte del técnico que es de la alternativa, junto a una ficha IMPLEMENTADA.

**Resultado:** **0 fugas.**
- Lo que se retira es justo lo que bloquearía.
- Lo que no se retira tampoco bloquea en el técnico: «implementado» (no hay fichas por debajo de IMPLEMENTADO), «invalidación» (no es la raíz), el identificador partido o con barra (no se reconoce ni suelto ni en la tabla) y las fichas que el Motor sirve.

**Una vía teórica que no se cubre:** el `detalle` de ERROR_CALCULO de HT-03 puede llevar las claves de dimensión que escribe el modelo («dimensiones desconocidas [...]»). El esquema `DIMS` admite claves libres. Pero esa candidata no llega a GC3, porque la evaluación provisional da el mismo error y `_gc2` exige que no haya errores, así que no puede ser una alternativa. No es un hallazgo.

### 2. ¿Tapa algo poner delante la advertencia en HA?

Sí, en un caso.

**Por qué:**
- `advertir_alternativas_retiradas` inserta sus ADVERTENCIAS en la posición 0 de las incidencias de G3-MET-13.
- `g3_met13_tecnico` añade sus BLOQUEOS al final.
- El G3V de F7 guarda en HA solo los cinco primeros detalles (`redaccion.generar`, `[...][:5]`).

**Consecuencia:** si hay cinco o más alternativas con texto retirado y, a la vez, un BLOQUEO de G3-MET-13 en F7, el detalle del BLOQUEO no queda en HA. Pasa tanto si el BLOQUEO es anterior (del visual del Redactor) como si es del técnico.

**Reproducción:** `r02_01`, últimas dos líneas, con seis alternativas: «TAPA» en los dos casos.

**Lo que no cambia:**
- el dictamen (BLOQUEADO);
- la lista de bloqueos (`G3-MET-13`);
- el paso a la carpeta de bloqueados.

Solo se pierde el porqué en el registro de auditoría. Con advertencias de otras comprobaciones no pasa nada, porque cada comprobación tiene sus propios cinco detalles. Dentro de G3-MET-13, las advertencias de F6 de candidatas no entregadas quedan detrás, y son de la misma familia.

**Por qué es baja:** hace falta coincidir con cinco o más alternativas con texto retirado, y nada deja de bloquearse.

### 3. ¿Llama algún camino real a `tecnico()` sin las alternativas calculadas?

No.

- Solo hay dos llamadas a `Redaccion.tecnico`, `redaccion.py:429` y `:435`. Las dos están en `generar`, después de `extras["alternativas_descartadas"] = sint.alternativas_descartadas(paquete, extras, bloque)` (`:404`).
- `generar` vuelve a calcular la clave en cada llamada, así que la reescritura PB-39 (`orquestacion.py:1897` y `diseno_v6.py:940`) no hereda una versión vieja.
- Las otras llamadas a `tecnico()` están en las pruebas.
- Si alguien la llamara sin la clave, la vía de reserva calcula sin sustituir. Entonces G3-MET-13 bloquearía: falla cerrado, no abierto.

### Hallazgos r02

| ID | Gravedad | Cómo reproducirlo | Esperado / obtenido | Corrección exacta | Estado |
| --- | --- | --- | --- | --- | --- |
| H-04 | baja | `cd bloque_a/11_Ejecutor && ../../.venv/bin/python ../../.docs/tickets/T-175/revisores/r02_01_fugas_y_orden_ha.py` (últimas dos líneas) | **Esperado:** en el G3V de F7, en HA, el detalle de un BLOQUEO de G3-MET-13 está siempre entre los cinco que se guardan. **Obtenido:** con cinco o más alternativas con texto retirado, los cinco son esas ADVERTENCIAS y el BLOQUEO (del visual o del técnico) no aparece. | En `bloque_a/11_Ejecutor/bloque_a/redaccion.py`, en la escritura del G3V de F7 (`"comprobaciones": [...]`), cambiar `"detalle": [i["detalle"] for i in c["incidencias"]][:5]` por `"detalle": [i["detalle"] for i in sorted(c["incidencias"], key=lambda i: i.get("severidad") != "BLOQUEO")][:5]`. La ordenación es estable: primero los BLOQUEOS en su orden, luego las advertencias de las alternativas y después el resto. Corregir el comentario de `advertir_alternativas_retiradas` («delante de las demás advertencias; los BLOQUEOS, antes, al escribir el G3V»). Añadir a `test_t175_alternativas.py` una prueba con un `res` de G3-MET-13 con un BLOQUEO y seis alternativas retiradas, que compruebe que el BLOQUEO está entre los cinco detalles de la G3V-…-F7 (o, como unidad, la expresión de arriba), y un mutante que quite el `sorted`. | abierto |

### Veredicto r02

**APTO.** H-01 a H-03 están corregidos con sus pruebas. Los scripts de la r01 dan lo esperado y `r02_01` no encuentra fugas de texto del modelo en 4.N.4 ni en la sección 6. No hay regresiones: ciclos V5 y V6, backtest, JSON y visual idénticos frente a develop `375d24b`, y el técnico solo cambia en lo declarado.

Queda abierto H-04, que es bajo. Se corrige en este mismo ticket con la corrección exacta de arriba antes de cerrar; si no se corrige, pasa a la deuda técnica con su ID.

## Ronda de cierre

- **Revisor:** claude (el mismo revisor de la r01 y la r02, que no implementó) · 2026-11-17
- **Objeto:** `wip/t175` `0398a01` (ronda de cierre de H-04), sobre `55ad862`, en una copia de trabajo nueva.

### H-04

**Corregido.**
- `redaccion.detalles_g3v` ordena los detalles del G3V de F7, que va a HA, con los BLOQUEOS delante y en su orden (la ordenación es estable).
- `revisores/r03_01_cierre_orden.py` lo comprueba por el camino real de HA y sobre una lista **sin ordenar**, sin depender de `bloqueos_delante`: con seis ADVERTENCIAS seguidas de dos BLOQUEOS, los detalles salen `['B1', 'B2', 'a0', 'a1', 'a2']`.
- `r02_01` da 0 FUGA y 0 TAPA.

### El cambio extra en `g3_met13_tecnico` (T-165)

`sintesis.bloqueos_delante` solo reordena, en su sitio, las incidencias de la comprobación G3-MET-13 del `res` de F7.

**Qué no cambia:**
- **El dictamen, el motivo y el resumen.** `_recalcular` usa los `resultado` de las comprobaciones, no el orden de las incidencias.
- **La lista de bloqueos de `generar`.** Sale del orden de las comprobaciones, que no se toca.

**Quién no lee ese orden:**
- **F6.** `_validar_g3`, la retirada por OPP- y el G3V de F6 trabajan con otro `res`, el de `orquestacion._validar_g3`. Este cambio no lo toca.
- **El `res` de F7.** Se crea de nuevo en cada `generar` y, después de `g3_met13_tecnico`, solo lo lee el G3V de F7.

**Comprobaciones:**
- **`r03_01`.** Con tres situaciones previas (ninguna incidencia, una ADVERTENCIA de F6, un BLOQUEO del visual), `g3_met13_tecnico` da exactamente lo mismo con `bloqueos_delante` que con la función anulada: valor devuelto, dictamen, motivo, resumen, resultados de cada comprobación y multiconjunto de incidencias.
- **Pruebas:** `tests/test_t165_g3_met13.py` y `tests/test_t175_alternativas.py` dan **160 superadas**.
- **Mutantes:** `mutantes.py` da 25/25 muertos.

### Regresión

- `r01_02`:
  - con «valid-» que persiste en una alternativa: ENTREGADA;
  - con la regla B («RISK-XYZ-999») y modelo obediente: ENTREGADA;
  - en el modo `opcion`: se retira la opción y el resto se entrega.
- `r01_03` (V5 y V6 de doce clases): JSON, visual y técnico **idénticos** a los de `55ad862`, ENTREGADA APTO.

### Veredicto final

**APTO.**
- H-01 a H-04 están corregidos, cada uno con su prueba.
- Ningún hallazgo queda abierto ni pasa a la deuda técnica.
- PB-38 queda «Superada».
- INC-T175-01 sigue `[PROPUESTO]`, a la vista del operador.

T-175 pasa a CERRADO, en el README del ticket y en la deuda técnica.
