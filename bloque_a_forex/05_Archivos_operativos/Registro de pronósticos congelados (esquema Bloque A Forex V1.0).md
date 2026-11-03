# Esquema de archivo operativo — F4 Registro de pronósticos congelados

**Bloque A Forex · Robot Investor · Versión V1.0 · 02/11/2026 · actualizado V1.1 (03/11/2026)** · Subordinado al Documento 0 del Bloque A Forex, versión óptima V1.1. Actualización V1.1: horizonte H5 «limitado» con hitos HIT-FX-, campo `es_principal` y evaluación de H5 por hitos.

---

## 1. Propósito

F4 conserva cada **pronóstico verificable** (PRG-FX-) que el Bloque A Forex emite, congelado en su fecha con su horizonte (H1–H5; H5 «limitado»), su afirmación sobre el indicador de seguimiento (dirección, rango, umbral, evento o rentabilidad total), su probabilidad interna y su banda, su **tipo de rentabilidad** (precio de contado o rentabilidad total con carry), su criterio, fijación y fecha de resolución y sus **referencias ingenuas obligatorias**: el **paseo aleatorio** (Meese y Rogoff, 1983) y, cuando procede, el **forward como predictor**; y, cuando vence, su **resolución** y puntuación. Es la base de la evaluación sin fuga de información, de los certificados de horizonte (R13), del historial de aciertos y de la recalibración (sección 12 del Documento 0).

**No es editable hacia atrás** (R11): nadie retoca un pronóstico congelado. Incluye los pronósticos de finalistas no seleccionadas (`en_informe: false`) para medir falsos negativos.

## 2. Propietario, lectores y contratos

| Aspecto | Contenido |
|---|---|
| Escritura de altas | AG-10 Analista de Prospectiva y Horizontes (único autor de altas, tras la orden de congelación del Analizador, posterior a G3) |
| Escritura de resolución | AG-20 Evaluador, **exclusivamente** en el bloque `resolucion` y en `estado` (ABIERTO → RESUELTO/NO_RESOLUBLE) |
| Lectores | Todos los agentes |
| Contratos | CT-12 (propuesta y orden de congelación), CT-19 (resultados), CT-09 (referencias ingenuas y puntuaciones del Motor, MC-10) |
| Herramientas | HT-01 (fijaciones, puntos forward, vintages), HT-05 (recordatorios de resolución y calendario de festivos de liquidación), HT-09 (G3-CON-13, G3-FX-06, G3-FX-07, G3-FX-11) |

## 3. Reglas

1. **Congelación**: la entrada de alta no se modifica jamás. Una corrección es un PRG nuevo con `version_de` = PRG anterior; **el original sigue evaluándose** en su fecha (impide «corregir» los pronósticos que van mal) y la versión nueva se evalúa desde su propia congelación.
2. **Separación de escritura**: los campos de alta los escribe solo Prospectiva; los de resolución solo el Evaluador. Cualquier otra escritura es incidencia Material.
3. **Probabilidad**: `prob_interna` se registra siempre (en rejilla de 5 puntos, 5–95 %; 15–85 % sin certificado); `prob_publicada` solo con certificado vigente (`certificado_ref`) para la celda segmento × horizonte × método.
4. **Notación**: la variable se expresa sobre el par en convención de mercado `BASE/COTIZADA`; las afirmaciones direccionales se refieren a la divisa base (p. ej., «USD/JPY cerrará por debajo de su nivel de referencia» = yen al alza).
5. **Tipo de rentabilidad**: todo PRG declara `PRECIO_CONTADO`, `RENTABILIDAD_TOTAL` o `NIVEL_VOLATILIDAD` (opciones VOLATILIDAD) (variación del tipo de cambio más el carry del periodo) y la divisa de medición.
6. **Referencias ingenuas obligatorias** (Anexo A, calculadas por el Motor sin fuga): paseo aleatorio (sin cambio) siempre; forward como predictor en todo PRG de rentabilidad total y en los direccionales cuando exista forward; en estrategias, rentabilidad nula o índice de la estrategia; en opciones `REGIMEN`, además, la probabilidad implícita en los puntos forward. Ejemplo de referencia probabilística: bajo el forward como predictor, P(S_T < S_0) ≈ Φ(ln(S_0/F)/(σ√T)), con σ la volatilidad implícita del plazo.
7. **Sin fuga ni anticipación en fijaciones**: nada en el alta puede ser posterior a `fecha_congelacion`. El `nivel_referencia` es la **última fijación conocible** en ese momento (p. ej., para una congelación el lunes 06:30 CET, la fijación del viernes); los datos de posicionamiento cuentan desde su publicación, no desde su fecha de referencia; el nivel de referencia respeta la antigüedad máxima de PS2 (H1 1 día · H2 2 · H3 5 · H4 30 · H5 90).
8. **Universo completo**: todos los PRG se resuelven, incluidos los de opciones cerradas, invalidadas o descartadas por el Broker. La invalidación de una opción no anula sus PRG.
9. **NO_RESOLUBLE** solo con motivo (fijación inexistente tras fallback, afirmación ambigua, divisa redenominada o discontinuada); se cuenta y se publica.
10. Conservación indefinida.
11. **H5 (V1.1, 8.3 y Anexo A)**: solo para opciones de naturaleza `ESTRUCTURAL` en uno de los tres ámbitos (`ambito_h5`: EQUILIBRIO_LARGO_PLAZO, REGIMEN_CAMBIARIO, SISTEMA_MONETARIO_INTERNACIONAL); `prob_interna` y `prob_publicada` **nulas** (solo `banda_verbal`; nunca certificable); `hitos` obligatorios (≥ 3 HIT-FX-, el primero a ≤ 12 meses, ≤ 24 meses entre hitos), cada uno con `hit_id`, `fecha`, `indicador`, `criterio` y `referencia_ingenua`. El PRG H5 no se puntúa con Brier ni log-score antes de su vencimiento: el Evaluador resuelve cada hito en su fecha y publica el resultado y el estado del PRG (EN_CURSO_CONFORME · DESVIADO · INVALIDADO) en **F6** (entradas `HIT` y `H5`), sin tocar el alta. En el ejecutor, `fecha_resolucion` = alta + 10 años.
12. **Horizonte principal**: el PRG del `horizonte_principal` de la opción lleva `es_principal = true` (uno por opción y congelación).

## 4. Formato de entrada

### 4.1 Campos de alta (Prospectiva)

| Campo | Tipo | Oblig. | Valores / formato | Descripción |
|---|---|---|---|---|
| `prg_id` | Identificador | Sí | `PRG-FX-AAAA-NNNN` | Clave |
| `version_de` | Identificador | No | PRG-FX- anterior | Corrección |
| `opp_id` / `tnd_ids` | Identificadores | Sí / No | OPP-FX- / TND-FX- | Vínculos |
| `run_id` | Identificador | Sí | RUN-FX- | Ejecución |
| `segmento` | Enumerado | Sí | G10N · G10M · EMAS · EMLA · EMEA · ESTR | Celda |
| `horizonte` | Enumerado | Sí | H1 · H2 · H3 · H4 · H5 | Celda (aplicable según 8.3 vigente; H5 «limitado») |
| `es_principal` | Booleano | Sí (V1.1) | — | PRG del horizonte principal de la opción |
| `ambito_h5` | Enumerado | Si H5 | EQUILIBRIO_LARGO_PLAZO · REGIMEN_CAMBIARIO · SISTEMA_MONETARIO_INTERNACIONAL | Regla 11 |
| `hitos` | Lista de objetos | Si H5 (≥ 3) | `{hit_id HIT-FX-AAAA-NNNN, fecha, indicador, criterio, referencia_ingenua, estado ABIERTO}` | Regla 11; resultados en F6 |
| `estrategia` | Texto codificado | Sí | Lente del segmento (p. ej., G10N-DIFERENCIAL-2A, G10M-TERMINOS-INTERCAMBIO, EMAS-FIJACION-CNY, EMLA-CARRY-AJUSTADO, EMEA-CONVERGENCIA-EUR, ESTR-CARRY, ESTR-VALOR, ESTR-MOMENTUM, ESTR-DOLAR-AMPLIO) | Celda de diagnóstico |
| `tipo_opcion` | Enumerado | Sí | PAR · CRUCE · CESTA · BLOQUE · ESTRATEGIA · VOLATILIDAD · REGIMEN | Celda de diagnóstico |
| `tipo_pronostico` | Enumerado | Sí | DIRECCIONAL · RELATIVO · RANGO · UMBRAL · EVENTO · CUANTIL | Forma |
| `afirmacion` | Texto | Sí | Inequívoca, con el par en convención de mercado | Lo que se pronostica |
| `variable` | Objeto | Sí | `{serie_ht01, par o composicion, descripcion, tipo_rentabilidad PRECIO_CONTADO·RENTABILIDAD_TOTAL·NIVEL_VOLATILIDAD, divisa_medicion}` | Qué se mide |
| `nivel_referencia` | Objeto | Sí | `{valor, fijacion {fuente, hora, zona}, fecha_hora, conocible_desde, fuente}` | Punto de partida (última fijación conocible) |
| `umbral` / `rango` / `cuantiles` | Número / par / lista | Según tipo | — | Condición |
| `fecha_congelacion` | Fecha-hora | Sí | ISO 8601 con zona | Momento de congelación |
| `fecha_resolucion` | Fecha | Sí | ISO 8601 | Cuándo se resuelve |
| `criterio_resolucion` | Texto | Sí | Convención exacta: fijación (BCE, WM/Reuters 16:00 Londres, Fed H.10, fijación de liquidación del NDF), día hábil, primera publicación | Cómo se resuelve |
| `fuente_resolucion` | Texto | Sí | Serie HT-01 o fuente oficial | — |
| `regla_fallback` | Texto | Sí | Fijación alternativa, festivos de liquidación, día hábil anterior, revisiones | — |
| `banda_verbal` | Enumerado | Sí | MUY_PROBABLE · MAS_PROBABLE_QUE_NO · INCIERTO · POCO_PROBABLE · MUY_POCO_PROBABLE | Correspondencia vigente en F10 (P-33; inicial: 80–95 %, 60–75 %, 45–55 %, 25–40 %, 5–20 %) |
| `prob_interna` | Número | Sí | 0,05–0,95 (rejilla 0,05) | Siempre registrada |
| `prob_publicada` | Número o null | Sí | null salvo certificado | R13 |
| `certificado_ref` | Identificador | Si `prob_publicada` | CERT- | — |
| `metodo` | Texto | Sí | Método o combinación (method_id del Catálogo) | Celda de certificación |
| `fuentes_clave` | Lista | No | REF- | Celda de diagnóstico por fuente |
| `referencias_ingenuas` | Lista de objetos | Sí (≥ 1; siempre PASEO_ALEATORIO) | `{tipo PASEO_ALEATORIO·FORWARD·IMPLICITA_FORWARD·RENTABILIDAD_NULA·INDICE_ESTRATEGIA·CESTA_SEGMENTO·IMPLICITA_OPCIONES·TASA_BASE·MEDIA_HISTORICA, valor_o_prob, calc_id}` | Calculadas sin fuga (MC-10) |
| `informes_transversales` | Lista | No | `{capa BCM·PFV, msg_id}` | Contexto usado al formularlo |
| `escenario_asociado` | Texto | Sí | BASE · FAVORABLE · ADVERSO | — |
| `en_informe` | Booleano | Sí | — | Publicado o no |
| `estado` | Enumerado | Sí | ABIERTO al alta | — |

### 4.2 Campos de resolución (exclusivos del Evaluador)

| Campo | Tipo | Oblig. al resolver | Descripción |
|---|---|---|---|
| `resolucion.fecha_resuelto` | Fecha | Sí | — |
| `resolucion.valor_observado` | Número / texto | Sí (salvo NO_RESOLUBLE) | Con unidad y fijación |
| `resolucion.carry_realizado` | Número | Si RENTABILIDAD_TOTAL | Carry del periodo (puntos forward o diferencial de tipos), con CALC- |
| `resolucion.fuente_usada` / `vintage` | Texto | Sí | Serie, fijación y versión |
| `resolucion.fallback_aplicado` | Booleano | Sí | — |
| `resolucion.resultado` | Enumerado | Sí | OCURRIDO · NO_OCURRIDO · VALOR (cuantiles) |
| `resolucion.resultado_binario` | 0/1 | Si binario | — |
| `resolucion.puntuaciones` | Objeto | Sí | `{brier, log, pinball, brier_paseo_aleatorio, brier_forward, log_paseo_aleatorio, error_vs_paseo_aleatorio, error_vs_forward}` |
| `resolucion.calc_id` | Identificador | Sí | CALC- del Motor (MC-10) |
| `resolucion.comprobacion_fuga` | Enumerado | Sí | SUPERADA · FALLIDA |
| `resolucion.motivo_no_resoluble` | Texto | Si NO_RESOLUBLE | — |
| `resolucion.corrige_a` | Identificador | Si es corrección | Resolución anterior corregida |

## 5. Estados y transiciones

| Desde | Hacia | Quién | Condición |
|---|---|---|---|
| (alta) | ABIERTO | Prospectiva | Orden de congelación tras G3 |
| ABIERTO | RESUELTO | Evaluador | Fijación disponible y resultado calculado |
| ABIERTO | NO_RESOLUBLE | Evaluador | Motivo documentado tras fallback (o 10 días hábiles sin dato) |
| RESUELTO | RESUELTO (corrección) | Evaluador | Nueva entrada de resolución con `corrige_a`; la anterior se conserva |

No existen estados «anulado» ni «invalidado»: la invalidación de una opción no detiene la resolución. Un PRG H5 permanece ABIERTO hasta su vencimiento; su estado intermedio (EN_CURSO_CONFORME, DESVIADO, INVALIDADO) se publica en F6 a partir de sus hitos.

## 6. Índices de consulta

| Índice | Clave | Uso |
|---|---|---|
| Vencimientos | `fecha_resolucion`, `estado` = ABIERTO | Resolución diaria (HT-05), con calendario de festivos |
| Celda de decisión | `segmento` × `horizonte` | Métricas, recalibración, aplicabilidad |
| Celda de certificación | `segmento` × `horizonte` × `metodo` (× `tipo_pronostico`) | Certificados |
| Diagnóstico | `estrategia`, `tipo_opcion`, `tipo_rentabilidad`, `fuentes_clave` | Lecciones de nivel A |
| Por par y divisa | `variable.par`, `composicion` | Historial por divisa; consultas del Broker |
| Por oportunidad | `opp_id` | Seguimiento de vigentes; historial de aciertos |
| Publicados / no publicados | `en_informe` | Falsos negativos; sesgo de selección |
| Por banda | `banda_verbal` | Sobreconfianza por banda |
| Versiones | `version_de` | Trazabilidad de correcciones |

## 7. Ejemplo ficticio

> **EJEMPLO FICTICIO — no es una entrada real.** Datos, series e identificadores inventados.

```json
{"prg_id":"PRG-FX-2026-0001","version_de":null,"opp_id":"OPP-FX-2026-0007","tnd_ids":["TND-FX-2026-0001"],"run_id":"RUN-FX-2026-0001",
 "segmento":"G10N","horizonte":"H3","estrategia":"G10N-DIFERENCIAL-2A","tipo_opcion":"PAR","tipo_pronostico":"DIRECCIONAL",
 "afirmacion":"La rentabilidad total de una posición larga en JPY y corta en USD será positiva entre el 2026-11-06 y el 2027-05-07 (USD/JPY, fijación WM/Reuters 16:00 Londres, carry incluido)",
 "variable":{"serie_ht01":"FICT-USDJPY-WMR16","par":"USD/JPY","descripcion":"rentabilidad total de JPY frente a USD","tipo_rentabilidad":"RENTABILIDAD_TOTAL","divisa_medicion":"JPY"},
 "nivel_referencia":{"valor":149.20,"fijacion":{"fuente":"WM_REUTERS","hora":"16:00","zona":"Europe/London"},"fecha_hora":"2026-11-06T16:00:00+00:00","conocible_desde":"2026-11-06T16:05:00+00:00","fuente":"HT-01"},
 "fecha_congelacion":"2026-11-09T06:30:00+01:00","fecha_resolucion":"2027-05-07",
 "criterio_resolucion":"Fijación WM/Reuters 16:00 Londres del 2027-05-07 (o día hábil anterior) más el carry del periodo implícito en los puntos forward a 6 meses del 2026-11-06","fuente_resolucion":"HT-01",
 "regla_fallback":"Tipo de referencia del BCE cruzado EUR/JPY ÷ EUR/USD del mismo día; si ninguno, NO_RESOLUBLE","banda_verbal":"MAS_PROBABLE_QUE_NO","prob_interna":0.60,"prob_publicada":null,"certificado_ref":null,
 "metodo":"MET-FX-DIF2A-01",
 "referencias_ingenuas":[{"tipo":"PASEO_ALEATORIO","valor_o_prob":0.41,"calc_id":"CALC-FX-2026-0204"},{"tipo":"FORWARD","valor_o_prob":0.50,"calc_id":"CALC-FX-2026-0204"}],
 "informes_transversales":[{"capa":"BCM","msg_id":"MSG-2026-11-07-0018"},{"capa":"PFV","msg_id":"MSG-2026-11-07-0021"}],
 "escenario_asociado":"BASE","en_informe":true,"estado":"ABIERTO","resolucion":null}
```

Nota al ejemplo: con el carry en contra (≈ −1,55 % en seis meses) y una volatilidad implícita del 10 % anual (σ√T ≈ 7,1 %), el paseo aleatorio (contado sin cambio) asigna a una rentabilidad total positiva una probabilidad ≈ Φ(−0,0155/0,071) ≈ 0,41; el forward como predictor implica una rentabilidad total esperada nula (la paridad cubierta compensa el carry con la apreciación implícita), por lo que su probabilidad de referencia es ≈ 0,50. La ventaja del pronóstico solo se demuestra si, con muestra suficiente, su Brier es menor que el de ambas referencias.
