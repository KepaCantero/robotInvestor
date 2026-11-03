# Esquema de archivo operativo — F3 Registro de oportunidades

**Bloque A Forex · Robot Investor · Versión V1.0 · 02/11/2026** · Subordinado al Documento 0 del Bloque A Forex, versión óptima V1.0.

---

## 1. Propósito

F3 registra cada **oportunidad cambiaria** (OPP-FX-): un **ámbito cambiario delimitado** —un par, un cruce, una cesta, un bloque regional o temático, una estrategia, una opinión sobre volatilidad o un cambio de régimen— dentro de uno de los **seis segmentos** (Documento 0, 2.6), en el que se espera una evolución favorable en un horizonte determinado que todavía no está plenamente descontada por el forward, la curva de tipos ni el posicionamiento. Cada ficha recoge su segmento, tipo de opción, par o composición, dirección referida a la divisa base, divisa de financiación, tesis, valoración, **carry**, **convertibilidad**, puntuaciones A y RK, horizontes, puertas, objeciones, encargo para el Bloque B, relevancia decisional, estado analítico y decisión del Broker. Es la memoria de qué se propuso, por qué, qué pasó después y qué decidió el Broker; incluye **todas** las candidatas, finalistas no seleccionadas y descartadas, para que el Evaluador mida falsos positivos y negativos.

**No es**: una recomendación personalizada ni una orden; no es una selección de instrumentos (granularidad máxima: par, cruce, cesta o estrategia; el contado, el forward, el futuro, la opción, el ETF/ETC o el CFD, su proveedor, coste, apalancamiento, tamaño y nivel de entrada son del Bloque B); no es un registro de pronósticos (F4) ni de evidencia (F2).

## 2. Propietario, lectores y contratos

| Aspecto | Contenido |
|---|---|
| Propietario de escritura | AG-02 Analizador de Oportunidades en Divisas (único) |
| Lectores | Plano P2, AG-14, AG-15, AG-16, AG-01 Coordinador, AG-18 Orquestador, AG-19 Auditor, AG-20 Evaluador |
| Contratos | CT-06 (fichas de segmento), CT-06T (señales transversales que el Analizador incorpora a `valoracion`, `catalizadores` y `posicionamiento`), CT-12 (horizontes y PRG), CT-13 (objeciones), CT-15 (síntesis), CT-04 vía Coordinador (decisión del Broker, que el Analizador anota en `decision_broker`) |
| Herramientas | HT-03 (A y RK), HT-09 (G3), HT-06 |

## 3. Reglas

1. **Append-only**: cambios de estado, puntuaciones y decisiones son entradas nuevas; nada se borra.
2. **Estado analítico y decisión del Broker son independientes**: `decision_broker` nunca altera `estado`; el resultado se mide aunque el Broker la descarte.
3. **Puntuaciones** A y RK solo con HT-03 y pesos de F10 vigentes (A FX: asimetría 30 · valoración y desviación del equilibrio 20 · carry 15 · catalizadores 15 · momento y posicionamiento 10 · convertibilidad y profundidad 10); banda marginal (≤ 5 puntos de un umbral) con segunda pasada y menor valor; tope de 40 en valoración si la tendencia está saturada. Un carry negativo no impide la opción, pero puntúa bajo; un posicionamiento extremo a favor de la tesis puntúa bajo.
4. **Elegibilidad para el top-3** (9.2): E ≥ 60, A ≥ 55, T ≥ 50 (o T = NA con A ≥ 65, frecuente en oportunidades tácticas H1–H2), G1–G4 y PS1–PS8 superadas, sin objeción fuerte sin resolver (umbrales de F10).
5. **Horizontes** solo los aplicables según la matriz 8.3 vigente en F10; «limitado» exige liquidez suficiente y catalizador identificado; probabilidad numérica solo con certificado (R13).
6. **Notación y dirección** (2.4, R21): todo par se escribe en la convención de mercado `BASE/COTIZADA` (códigos ISO 4217; CNH admitido); la `direccion` se refiere siempre a la divisa base (`ALCISTA_BASE` o `BAJISTA_BASE`). Toda opción declara `composicion` (para un par, dos entradas: base y cotizada con lados opuestos); las cestas, bloques y estrategias declaran pesos por lado (cada lado suma 1) y `divisa_financiacion`. Un par fuera de convención o una dirección incoherente con la composición no supera G3 (G3-FX-01).
7. **Indicador de seguimiento**: toda opción FINALISTA declara la serie pública que mejor representa la evolución de su ámbito: el tipo de cambio del par con su fijación (BCE, Fed H.10 o WM/Reuters), un índice de la cesta, un tipo de cambio efectivo (BPI) o un índice de estrategia publicado. Con él se construyen los escenarios, se resuelven los pronósticos y el Evaluador mide el resultado frente al paseo aleatorio, al forward y a la referencia del segmento (8.4).
8. **Convertibilidad e invertibilidad (PS3)**: toda opción FINALISTA declara el bloque `convertibilidad`. PS3 no se supera si la divisa no es convertible para un inversor minorista europeo y no existe exposición alternativa (NDF, futuros o productos cotizados) en mercados accesibles, si hay controles que impiden la exposición o la repatriación, o si no hay indicador medible. La existencia de mercados se puede **citar** para justificar la invertibilidad, nunca para recomendar un producto o proveedor. Un tipo fijo con riesgo de ruptura o una divisa con controles parte, como mínimo, de riesgo 4 (Anexo A, nota 2).
9. **Granularidad y frontera con el Bloque B (R21)**: ninguna oportunidad puede ser un instrumento ni incluir proveedor, coste, apalancamiento, tamaño o nivel de entrada. Los niveles del par solo pueden aparecer como **condición de invalidación**. Toda opción PROPUESTA lleva su `encargo_bloque_B`.
10. **Asignación de segmento y duplicados** (2.6): el Analizador asigna `segmento` con las reglas 1–3 (divisa menos líquida; tres o más divisas o regla sistemática → ESTR; volatilidad de un par → segmento del par) y registra el motivo; una misma oportunidad (mismo ámbito, dirección y tesis) tiene una sola ficha y no puede estar en dos top-3.
11. **Diversidad y coherencia**: dentro de un segmento, no más de dos opciones del mismo clúster ni una misma divisa con la misma dirección en más de dos opciones; entre segmentos, toda contradicción de signo en una divisa se justifica con mecanismos distintos o se resuelve (9.6.3 y 9.6.6), y se registra en `coherencia_entre_segmentos`.
12. **Cierre**: motivo obligatorio (INVALIDACION · VENCIMIENTO_HORIZONTE · OBJETIVO_ALCANZADO · SUSTITUCION) y resultado observado (datos de HT-01 o del Evaluador) en precio de contado y en rentabilidad total.

## 4. Formato de entrada

| Campo | Tipo | Oblig. | Valores / formato | Descripción |
|---|---|---|---|---|
| `opp_id` | Identificador | Sí | `OPP-FX-AAAA-NNNN` | Clave |
| `version` | Entero | Sí | ≥ 1 | Correcciones |
| `nombre` / `nombre_llano` | Texto | Sí | `nombre`: «USD/JPY bajista (yen al alza)»; `nombre_llano` sin jerga, ≤ 12 palabras, que diga qué divisa gana valor y frente a cuál | Técnico y para el usuario |
| `segmento` | Enumerado | Sí | G10N · G10M · EMAS · EMLA · EMEA · ESTR | Asignado por el Analizador (2.6) |
| `segmentos_relacionados` / `motivo_asignacion_segmento` | Lista / Texto | No / Sí | Códigos de segmento / regla de 2.6 aplicada | Trazabilidad de la asignación |
| `perfiles_motor` | Lista | Sí | PERF-FX-G10 · PERF-FX-EM · PERF-FX-FACT | Combinados si procede |
| `tipo_opcion` | Enumerado | Sí | PAR · CRUCE · CESTA · BLOQUE · ESTRATEGIA · VOLATILIDAD · REGIMEN | 2.4 |
| `par` | Texto | Sí en PAR, CRUCE, VOLATILIDAD y REGIMEN sobre un par | `BASE/COTIZADA` en convención de mercado | Null en cestas, bloques y estrategias |
| `composicion` | Lista de objetos | Sí | `{divisa ISO 4217, peso, lado LARGO·CORTO}`; cada lado suma 1 | Exposición por divisa (base de la exposición agregada) |
| `direccion` | Enumerado | Sí si hay `par` | ALCISTA_BASE · BAJISTA_BASE | Referida a la divisa base |
| `divisa_financiacion` | ISO 4217 | Sí | — | Divisa que se vende o se toma prestada |
| `vista_volatilidad` | Objeto | Sí en VOLATILIDAD | `{objeto NIVEL·ESTRUCTURA_PLAZOS·SESGO, sentido AL_ALZA·A_LA_BAJA, plazo, medida IMPLICITA·REALIZADA·DIFERENCIAL}` | Opinión sobre la volatilidad, sin estructura de opciones |
| `regimen_cambiario` | Objeto | Sí en REGIMEN | `{clasificacion_de_facto TIPO_FIJO·CAJA_DE_CONVERSION·BANDA·DESLIZAMIENTO·FLOTACION_ADMINISTRADA·FLOTACION_LIBRE, ancla, controles, tesis_regimen RUPTURA·AJUSTE·MANTENIMIENTO·LIBERALIZACION, indicadores_sostenibilidad [{nombre, valor, calc_id}], devaluacion_implicita_forward, diferencial_onshore_offshore}` | Clasificación de Ilzetzki, Reinhart y Rogoff |
| `ambito` | Objeto | Sí | `{incluye, excluye}` | Universo que delimita la oportunidad (y que analizará el Bloque B) |
| `tnd_ids` | Lista | No (sí si no es táctica) | TND-FX- | Tendencias de origen |
| `tesis` | Texto + CLM- | Sí | Una frase refutable | — |
| `mecanismo` | Texto | Sí | Causal (diferencial de tipos, flujos, términos de intercambio, valoración, régimen…) | — |
| `por_que_ahora` | Texto | Sí | Qué no descuentan el forward, la curva o el posicionamiento | — |
| `valoracion` | Objeto | Sí desde FINALISTA | `{metodos [PPA·BEER·FEER·REER·MODELO_MATERIAS_PRIMAS·FORWARD_VS_CONTADO·VALOR_RELATIVO_ESTRATEGIA], desviacion_equilibrio_pct, que_descuenta_el_forward, que_descuenta_la_curva, calc_ids}` | — |
| `carry` | Objeto | Sí desde FINALISTA | `{anual_pct, signo A_FAVOR·EN_CONTRA·NEUTRO, ajustado_vol, fuente PUNTOS_FORWARD·DIFERENCIAL_TIPOS, plazo, calc_id}` | Respecto de la tesis |
| `posicionamiento` | Objeto | Sí desde FINALISTA | `{neto_cftc, percentil_historico, a_favor_de_la_tesis sí/no, crowding, fuente_pfv (msg_id CT-06T)}` | De AG-21 |
| `catalizadores` | Lista | Sí desde FINALISTA | `{evento, fecha, nivel S0–S3, fuente_bcm (msg_id CT-06T) si procede}` | Reuniones de bancos centrales, datos, elecciones, revisiones de índices de bonos |
| `riesgos` | Lista | Sí | Texto | Principales (intervención, sorpresa de banco central, aversión al riesgo, desplome del carry, ruptura de régimen…) |
| `riesgo_1a5` / `riesgo_cola` | Entero / objeto | Sí desde FINALISTA | 1–5 (RISK-DD-001; ≥ 4 en tipo fijo con riesgo de ruptura o con controles) / `{perdida_escenario_adverso, calc_id}` | — |
| `invalidacion` | Lista | Sí (≥ 1) | `{indicador, umbral, plazo}` | Observables; pueden incluir niveles del par, nunca como entrada |
| `que_no_sabemos` | Lista | Sí desde FINALISTA | Texto | R12 |
| `horizontes` | Objeto | Sí desde FINALISTA | `{H1..H4: {aplicable SI·LIMITADO·NO, vista ALCISTA_BASE·BAJISTA_BASE·RANGO·RELATIVA, tipo_rentabilidad PRECIO_CONTADO·RENTABILIDAD_TOTAL·NIVEL_VOLATILIDAD, banda, prob_publicada, certificado_ref, referencia PASEO_ALEATORIO·FORWARD·…, prg_ids}}` | — |
| `indicador_seguimiento` | Objeto | Sí desde FINALISTA | `{nombre, simbolo, serie_ht01, fuente, fijacion {fuente, hora, zona}, divisa_medicion}` | Base de medición |
| `convertibilidad` | Objeto | Sí desde FINALISTA | `{convertible, ndf, fijacion_ndf, controles_capitales, repatriacion_restringida, sanciones, profundidad MUY_ALTA·ALTA·MEDIA·BAJA, exposicion_alternativa_accesible, nota}` | PS3 (la `nota` puede citar la existencia de mercados, sin productos ni proveedores) |
| `liquidez` / `reversibilidad` | Enumerado | Sí desde FINALISTA | ALTA · MEDIA · BAJA | Del par o la cesta (no de un instrumento) |
| `encargo_bloque_B` | Objeto | Sí desde FINALISTA | `{carry_esperado {anual_pct, signo}, consideraciones_implementacion [liquidez, NDF, riesgo de evento, horario de liquidez, festivos de liquidación], metricas_clave, preguntas_para_B}` | Base del `paquete_para_bloque_B` (Anexo B); información, no recomendación de instrumento |
| `puntuaciones` | Objeto | Sí desde EN_INVESTIGACION | `{T, E, M, A, RK, desglose_ref, pasada, methodology_version, fecha}` | Con HT-03 |
| `puertas` | Objeto | Sí desde FINALISTA | `{GC1, GC2, GC3, G1, G2, G3, G4, PS1..PS8: {resultado SUPERADA·NO_SUPERADA·NO_APLICA, motivo, fecha}}` | — |
| `objeciones` | Lista | Sí en N2/N3 desde FINALISTA | `{obj_id, fuerza, resumen, respuesta, evidencia, estado RESPONDIDA·SIN_RESOLVER}` | CT-13 (incluidas forward, posicionamiento, intervención y fragilidad del carry) |
| `premortem` | Texto | Sí desde GC2 | Tres causas más probables de fallo | — |
| `cluster_id` / `factor_dominante` | Texto | Sí desde FINALISTA | p. ej. CL-USD, CL-JPY-REFUGIO, CL-CARRY-RIESGO, CL-MMPP, CL-<divisa> | Diversidad y apuestas independientes |
| `coherencia_entre_segmentos` | Objeto | Sí desde PROPUESTA | `{contradicciones [{divisa, opp_id_contraria, justificacion_contradiccion, resolucion MANTENIDA_JUSTIFICADA·REFORMULADA·RETIRADA}], exposiciones_comunes}` | 9.6.6 |
| `relevancia_decisional` | Enumerado | Sí desde PROPUESTA | ALTA · MEDIA · BAJA | Regla del Anexo A (ALTA si riesgo ≥ 4, reversibilidad baja, H4, E < 70 con A ≥ 75, tipo REGIMEN o divisa emergente de liquidez baja) |
| `siguiente_paso_sugerido` | Enumerado | Sí desde PROPUESTA | ENVIAR_A_BLOQUE_B · PROFUNDIZAR_EN_A · VIGILAR · DESCARTAR | — |
| `que_cambiaria_la_conclusion` | Lista | Sí desde PROPUESTA | Texto | — |
| `confianza` | Enumerado | Sí | establecido · probable · especulativo · en disputa | — |
| `estado` | Enumerado | Sí | Sección 5 | — |
| `rango_top3` | Entero | Si PROPUESTA/VIGENTE | 1–3 | Por RUN-FX- |
| `decision_broker` | Lista append-only | No | `{fecha, decision ENVIADA_A_BLOQUE_B·EN_SEGUIMIENTO·DESCARTADA·APLAZADA, motivo, ret_id}` | Desde CT-04 (F5) |
| `cierre` | Objeto | Sí si CERRADA | `{fecha, motivo, variacion_contado_pct, rentabilidad_total_pct, carry_realizado_pct, vs_paseo_aleatorio, vs_forward, vs_referencia_segmento, fuente, calc_id}` | Resultado frente a las referencias de 8.4 |
| `run_ids` | Lista | Sí | RUN-FX- | Ejecuciones |
| `historial` | Lista append-only | Sí | `{fecha, run_id, de, a, campo, justificacion}` | — |

## 5. Estados y transiciones

| Desde | Hacia | Condición |
|---|---|---|
| (alta) | CANDIDATA | Pasa GC1 en el cribado |
| CANDIDATA | EN_INVESTIGACION | Investigación dirigida iniciada |
| CANDIDATA | DESCARTADA | Señal no confirmada o PS7 (sanciones, datos no verificables, manipulación de la fijación, ruptura de régimen que invalida la tesis) |
| EN_INVESTIGACION | FINALISTA | GC2 y GC3 superadas (entre las 5 mejores de su segmento por RK provisional) |
| EN_INVESTIGACION | EN_OBSERVACION | No supera GC2 o GC3 (alternativa documentada) |
| EN_INVESTIGACION · FINALISTA | DESCARTADA | Tesis invalidada, PS7, objeción fuerte confirmada |
| FINALISTA | PROPUESTA | Seleccionada en el top-3 tras G3 |
| FINALISTA | EN_OBSERVACION | No seleccionada (conserva sus PRG con `en_informe: false`) |
| PROPUESTA | VIGENTE | Sigue en el top-3 en el ciclo siguiente |
| PROPUESTA · VIGENTE | CERRADA | Invalidación, vencimiento del horizonte, objetivo alcanzado o sustitución |
| EN_OBSERVACION | CANDIDATA | Nueva señal en un ciclo posterior |

## 6. Índices de consulta

| Índice | Clave | Uso |
|---|---|---|
| Vigentes por segmento | `estado` ∈ {PROPUESTA, VIGENTE}, `segmento` | F0 de cada ciclo; arrastre verificado |
| Top-3 por RUN- | `run_ids`, `rango_top3` | Historial e informes |
| Invalidaciones próximas | `invalidacion` a < 10 % del umbral | GC0 cambio material |
| Exposición por divisa | `composicion.divisa`, `lado`, `estado` | Exposición agregada, contradicciones entre segmentos y diversidad por divisa |
| Por par | `par`, `direccion` | Duplicados; consultas del Broker |
| Por decisión del Broker | `decision_broker.decision` | Lecciones de producto del Evaluador |
| Por clúster | `cluster_id`, `factor_dominante` | Apuestas independientes |
| Por tendencia | `tnd_ids` | Trazabilidad TND↔OPP |
| Duplicados entre segmentos | `par` o `composicion` normalizada + `direccion` + `tesis` | Regla 4 de 2.6 (una oportunidad, un solo top-3) |
| Por convertibilidad | `convertibilidad.controles_capitales`, `ndf` | PS3; relevancia ALTA |
| Por indicador de seguimiento | `indicador_seguimiento.serie_ht01` | Resolución de pronósticos y duplicados |
| Finalistas no seleccionadas | `estado` = EN_OBSERVACION con puertas de FINALISTA | Falsos negativos |
| Índice operativo | — | Recuentos por estado, segmento y tipo de opción |

## 7. Ejemplo ficticio

> **EJEMPLO FICTICIO — no es una entrada real.** Ningún dato describe una oportunidad existente; cifras e identificadores inventados.

```json
{"opp_id":"OPP-FX-2026-0007","version":1,"nombre":"USD/JPY bajista (yen al alza)","nombre_llano":"El yen japonés podría ganar valor frente al dólar",
 "segmento":"G10N","motivo_asignacion_segmento":"Par entre dos divisas de G10N (regla 1 de 2.6)","perfiles_motor":["PERF-FX-G10"],"tipo_opcion":"PAR",
 "par":"USD/JPY","composicion":[{"divisa":"JPY","peso":1.0,"lado":"LARGO"},{"divisa":"USD","peso":1.0,"lado":"CORTO"}],
 "direccion":"BAJISTA_BASE","divisa_financiacion":"USD",
 "ambito":{"incluye":"Exposición al tipo de cambio dólar–yen","excluye":"Cruces del yen con otras divisas y estrategias de carry multipar"},"tnd_ids":["TND-FX-2026-0001"],
 "tesis":{"texto":"El yen se apreciará frente al dólar en 3–6 meses al estrecharse el diferencial de tipos más de lo que descuenta el forward","clm_id":"CLM-FX-2026-0104"},
 "mecanismo":"Normalización del BoJ y recortes de la Fed; aumento de las coberturas cambiarias de inversores japoneses","por_que_ahora":"La curva OIS descuenta solo una subida del BoJ en 12 meses frente a las dos que sugiere la evidencia (informe BCM)",
 "valoracion":{"metodos":["PPA","REER","FORWARD_VS_CONTADO"],"desviacion_equilibrio_pct":-28,"que_descuenta_el_forward":"apreciación del yen del 1,5 % a 6 meses","que_descuenta_la_curva":"una subida del BoJ en 12 meses","calc_ids":["CALC-FX-2026-0201"]},
 "carry":{"anual_pct":-3.1,"signo":"EN_CONTRA","ajustado_vol":-0.35,"fuente":"PUNTOS_FORWARD","plazo":"3M","calc_id":"CALC-FX-2026-0202"},
 "posicionamiento":{"neto_cftc":-95000,"percentil_historico":12,"a_favor_de_la_tesis":"no","crowding":"cortos en yen extendidos: riesgo de cierre a favor de la tesis","fuente_pfv":"MSG-2026-11-07-0021"},
 "catalizadores":[{"evento":"Reunión del BoJ","fecha":"2026-12-18","nivel":"S2","fuente_bcm":"MSG-2026-11-07-0018"},{"evento":"Reunión del FOMC","fecha":"2026-12-09","nivel":"S2"}],
 "riesgos":["repunte de la inflación en EE. UU.","el BoJ aplaza la normalización"],"riesgo_1a5":3,"riesgo_cola":{"perdida_escenario_adverso":"-6,5 % en contado a 3 meses","calc_id":"CALC-FX-2026-0203"},
 "invalidacion":[{"indicador":"diferencial a 2 años EE. UU.–Japón","umbral":"se amplía > 50 pb","plazo":"2027-05-07"},{"indicador":"USD/JPY (fijación WM/Reuters 16:00 Londres)","umbral":"cierre semanal por encima de 158,00","plazo":"2027-05-07"}],
 "que_no_sabemos":["umbral de tolerancia del Ministerio de Finanzas a un yen fuerte"],
 "horizontes":{"H3":{"aplicable":"SI","vista":"BAJISTA_BASE","tipo_rentabilidad":"RENTABILIDAD_TOTAL","banda":"más probable que no","prob_publicada":null,"certificado_ref":null,"referencia":"PASEO_ALEATORIO y FORWARD","prg_ids":["PRG-FX-2026-0001"]}},
 "indicador_seguimiento":{"nombre":"USD/JPY, tipo de referencia","simbolo":"USDJPY","serie_ht01":"FICT-USDJPY-WMR16","fuente":"HT-01","fijacion":{"fuente":"WM_REUTERS","hora":"16:00","zona":"Europe/London"},"divisa_medicion":"JPY"},
 "convertibilidad":{"convertible":true,"ndf":false,"fijacion_ndf":null,"controles_capitales":false,"repatriacion_restringida":false,"sanciones":false,"profundidad":"MUY_ALTA","exposicion_alternativa_accesible":true,"nota":"Par muy líquido; existen futuros y opciones líquidos sobre el par en mercados regulados"},
 "liquidez":"ALTA","reversibilidad":"ALTA",
 "encargo_bloque_B":{"carry_esperado":{"anual_pct":-3.1,"signo":"EN_CONTRA"},
   "consideraciones_implementacion":["Par muy líquido; mercado 24 h; evitar los huecos de liquidez del fin de semana","Riesgo de evento: reuniones del BoJ y de la Fed","Posible intervención del Ministerio de Finanzas japonés"],
   "metricas_clave":["diferencial a 2 años EE. UU.–Japón","posicionamiento CFTC en JPY","risk reversal a 25 delta a 1 mes"],"preguntas_para_B":["¿Compensa el coste del carry en contra frente a capturar la exposición con otra estructura?"]},
 "puntuaciones":{"T":70,"E":75,"M":50,"A":70,"RK":72,"desglose_ref":"HT03-2026-0021","pasada":1,"methodology_version":"FX-1.0","fecha":"2026-11-07"},
 "cluster_id":"CL-JPY-REFUGIO","factor_dominante":"yen y refugio","coherencia_entre_segmentos":{"contradicciones":[],"exposiciones_comunes":["USD corto también en ESTR"]},
 "relevancia_decisional":"MEDIA","siguiente_paso_sugerido":"ENVIAR_A_BLOQUE_B","que_cambiaria_la_conclusion":["el BoJ descarta subidas","repunte del diferencial a 2 años"],
 "confianza":"probable","estado":"PROPUESTA","rango_top3":1,"decision_broker":[],"run_ids":["RUN-FX-2026-0001"]}
```
