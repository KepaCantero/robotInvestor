# Esquema de archivo operativo — F3 Registro de oportunidades

**Bloque A · Robot Investor · Versión óptima V5.0 · 02/11/2026 · actualizado V5.1 (03/11/2026)** · Subordinado al Documento 0 óptima V5.1. Cambios V5.1: `naturaleza_inversion`, `horizonte_principal` y `justificacion_horizonte` (8.3); H5 con hitos; `seg_id` del seguimiento encargado (CT-24); cierre verificado en un ciclo C6.

---

## 1. Propósito

F3 registra cada **oportunidad** (OPP-): un **ámbito de inversión delimitado** (mercado, región, sector, subsector, temática, segmento, factor o estrategia) dentro de uno de los **doce tipos de activo** (Documento 0, 2.6), en el que por una tendencia o una ineficiencia se espera una evolución favorable no plenamente descontada, con su tipo de activo y subtipo, tipo de opción, ámbito, indicador de seguimiento, invertibilidad, tesis, valoración, puntuaciones A y RK, horizontes, puertas, objeciones, encargo para el Bloque B, relevancia decisional, estado analítico y decisión del Broker. Es la memoria de qué se propuso, por qué, qué pasó después y qué decidió el Broker; incluye **todas** las candidatas, finalistas no seleccionadas y descartadas, para que el Evaluador mida falsos positivos y negativos.

**No es**: una recomendación personalizada ni una orden; no es una selección de activos concretos (granularidad máxima: segmento; la selección de activos dentro del ámbito es del Bloque B y los nombres concretos solo figuran en `ejemplos_ilustrativos`); no es un registro de pronósticos (F4) ni de evidencia (F2).

## 2. Propietario, lectores y contratos

| Aspecto | Contenido |
|---|---|
| Propietario de escritura | AG-02 Analizador (único) |
| Lectores | Plano P2, AG-01 Coordinador, AG-18 Orquestador, AG-19 Auditor, AG-20 Evaluador |
| Contratos | CT-06 (fichas de clase), CT-12 (horizontes y PRG), CT-13 (objeciones), CT-15 (síntesis), CT-04 vía Coordinador (decisión del Broker, que el Analizador anota en `decision_broker`) |
| Herramientas | HT-03 (A y RK), HT-09 (G3), HT-06 |

## 3. Reglas

1. **Append-only**: cambios de estado, puntuaciones y decisiones son entradas nuevas; nada se borra.
2. **Estado analítico y decisión del Broker son independientes**: `decision_broker` nunca altera `estado`; el resultado se mide aunque el Broker la descarte. Una opción con seguimiento encargado (CT-24, V5.1) conserva su estado analítico y lleva su `seg_id`; solo pasa a `CERRADA` por invalidación, vencimiento, objetivo o sustitución, verificados en un ciclo C6 o C1.
3. **Puntuaciones** A y RK solo con HT-03 y pesos de F10 vigentes; banda marginal (≤ 5 puntos de un umbral) con segunda pasada y menor valor; tope de 40 en valoración si la tendencia está saturada.
4. **Elegibilidad para el top-3** (9.2): E ≥ 60, A ≥ 55, T ≥ 50 (o T = NA con A ≥ 65), G1–G4 y PS1–PS8 superadas, sin objeción fuerte sin resolver (umbrales de F10).
5. **Horizontes** solo los aplicables según la matriz 8.3 vigente en F10; probabilidad numérica solo con certificado (R13).
6. **Indicador de seguimiento**: toda opción FINALISTA declara el índice, serie o cesta pública (HT-01) que mejor representa la evolución de su ámbito; con él se construyen los escenarios, se resuelven los pronósticos y el Evaluador mide el resultado frente a la referencia de su tipo (8.4). No es una recomendación de compra.
6 bis. **Granularidad y frontera con el Bloque B (R21)**: ninguna oportunidad puede ser un activo concreto (valor, emisión, fondo, contrato o token); los nombres concretos solo en `ejemplos_ilustrativos`. Toda opción PROPUESTA lleva su `encargo_bloque_B`.
6 ter. **Asignación de tipo y duplicados**: el Analizador asigna `tipo_activo` con las reglas de 2.6 y registra el motivo; una misma oportunidad (mismo ámbito y tesis) tiene una sola ficha y no puede estar en dos top-3.
7. **Cierre**: motivo obligatorio (INVALIDACION · VENCIMIENTO_HORIZONTE · OBJETIVO_ALCANZADO · SUSTITUCION) y resultado observado (datos de HT-01 o del Evaluador).

## 4. Formato de entrada

| Campo | Tipo | Oblig. | Valores / formato | Descripción |
|---|---|---|---|---|
| `opp_id` | Identificador | Sí | `OPP-AAAA-NNNN` | Clave |
| `version` | Entero | Sí | ≥ 1 | Correcciones |
| `nombre` / `nombre_llano` | Texto | Sí | `nombre_llano` sin jerga, ≤ 8 palabras | Técnico y para el usuario |
| `tipo_activo` | Enumerado | Sí | RV · RF · DIV · MP · IDX · FON · DER · INM · CRI · ALT · MON · TCV | Tipo de activo asignado por el Analizador (2.6); sustituye al campo heredado `clase`, que se admite como alias de lectura |
| `subtipo` | Texto | Sí | Subtipo de 2.6 (p. ej., «Sector», «Deuda pública», «Volatilidad implícita») | Orienta la búsqueda |
| `tipos_secundarios` / `motivo_asignacion_tipo` | Lista / Texto | No / Sí | Códigos de tipo / regla de 2.6 aplicada | Ante duda de asignación |
| `perfiles_motor` | Lista | Sí | PERF-xx (combinados en híbridos) | — |
| `tipo_opcion` | Enumerado | Sí | MERCADO · SECTOR · SUBSECTOR · TEMATICA · SEGMENTO · FACTOR · ESTILO · ESTRATEGIA | Granularidad máxima: segmento |
| `ambito` | Objeto | Sí | `{incluye, excluye, region}` | Universo que delimita la oportunidad (y que analizará el Bloque B) |
| `regiones` / `divisa_exposicion` | Lista / ISO 4217 | Sí | Códigos de región; EUR, USD… | — |
| `tnd_ids` | Lista | No (sí si no es táctica) | TND- | Tendencias de origen |
| `tesis` | Texto + CLM- | Sí | Una frase refutable | — |
| `mecanismo` | Texto | Sí | Causal | — |
| `por_que_ahora` | Texto | Sí | Qué no descuenta el mercado | — |
| `valoracion` | Objeto | Sí desde FINALISTA | `{metodo, resultado, calc_ids, que_descuenta_el_precio}` | — |
| `catalizadores` | Lista | Sí desde FINALISTA | `{evento, fecha, nivel S0–S3}` | Fechados |
| `riesgos` | Lista | Sí | Texto | Principales |
| `riesgo_1a5` / `riesgo_cola` | Entero / objeto | Sí desde FINALISTA | 1–5 / `{perdida_escenario_adverso, calc_id}` | — |
| `invalidacion` | Lista | Sí (≥ 1) | `{indicador, umbral, plazo}` | Observables |
| `que_no_sabemos` | Lista | Sí desde FINALISTA | Texto | R12 |
| `horizontes` | Objeto | Sí desde FINALISTA | `{H1..H5: {aplicable SI·LIMITADO·NO, vista ALCISTA·BAJISTA·NEUTRAL·RELATIVA, banda, prob_publicada, certificado_ref, prg_ids}}`; en H5, `prob_publicada` siempre null y `hit_ids` | — |
| `naturaleza_inversion` | Enumerado | Sí desde FINALISTA (V5.1) | TACTICA · LIQUIDEZ · CICLICA · PRIMA_RIESGO · VALORACION · ESTRUCTURAL | Fija el rango del horizonte principal (8.3) |
| `horizonte_principal` | Enumerado | Sí desde FINALISTA (V5.1) | H1–H5 | Horizonte de la tesis central, de la asimetría de A y del pronóstico principal |
| `justificacion_horizonte` | Texto o null | Si el principal queda fuera del rango de su naturaleza | — | HT-09 C17 |
| `indicador_seguimiento` | Objeto | Sí desde FINALISTA | `{nombre, simbolo, serie_ht01, fuente, divisa}` | Base de medición de la tendencia y de los pronósticos |
| `liquidez` / `reversibilidad` | Enumerado | Sí desde FINALISTA | ALTA · MEDIA · BAJA | Del ámbito (no de un instrumento) |
| `invertibilidad` | Objeto | Sí desde FINALISTA | `{universo_suficiente: true·false, nota}` | PS3: existe un universo de activos negociables suficiente y accesible para un minorista europeo, sin seleccionar ninguno |
| `encargo_bloque_B` | Objeto | Sí desde FINALISTA | `{criterios_seleccion_sugeridos, metricas_clave, preguntas_para_B}` | Base del `paquete_para_bloque_B` (Anexo B) |
| `ejemplos_ilustrativos` | Lista | No | Nombres concretos marcados como ilustración | Nunca propuesta de inversión |
| `puntuaciones` | Objeto | Sí desde EN_INVESTIGACION | `{T, E, M, A, RK, desglose_ref, pasada, methodology_version, fecha}` | Con HT-03 |
| `puertas` | Objeto | Sí desde FINALISTA | `{GC1, GC2, GC3, G1, G2, G3, G4, PS1..PS8: {resultado SUPERADA·NO_SUPERADA·NO_APLICA, motivo, fecha}}` | — |
| `objeciones` | Lista | Sí en N2/N3 desde FINALISTA | `{obj_id, fuerza, resumen, respuesta, evidencia, estado RESPONDIDA·SIN_RESOLVER}` | CT-13 |
| `premortem` | Texto | Sí desde GC2 | Tres causas más probables de fallo | — |
| `cluster_id` / `factor_dominante` | Texto | Sí desde FINALISTA | p. ej. CL-TIPOS-EUR | Diversidad y apuestas independientes |
| `relevancia_decisional` | Enumerado | Sí desde PROPUESTA | ALTA · MEDIA · BAJA | Regla del Anexo A |
| `siguiente_paso_sugerido` | Enumerado | Sí desde PROPUESTA | ENVIAR_A_BLOQUE_B · PROFUNDIZAR_EN_A · VIGILAR · DESCARTAR | — |
| `que_cambiaria_la_conclusion` | Lista | Sí desde PROPUESTA | Texto | — |
| `confianza` | Enumerado | Sí | establecido · probable · especulativo · en disputa | — |
| `estado` | Enumerado | Sí | Sección 5 | — |
| `rango_top3` | Entero | Si PROPUESTA/VIGENTE | 1–3 | Por RUN- |
| `decision_broker` | Lista append-only | No | `{fecha, decision ENVIADA_A_BLOQUE_B·EN_SEGUIMIENTO·DESCARTADA·APLAZADA, motivo, ret_id}` | Desde CT-04 (F5); `EN_SEGUIMIENTO` es solo una anotación salvo que exista un encargo CT-24 |
| `seg_id` | Identificador | Si hay seguimiento encargado (V5.1) | SEG- de F11 | Lo anota el Analizador a petición del Coordinador; no altera el estado analítico |
| `cierre` | Objeto | Sí si CERRADA | `{fecha, motivo, resultado_relativo, referencia_indice, fuente}` | Resultado del indicador de seguimiento frente a la referencia del tipo (8.4) |
| `run_ids` | Lista | Sí | RUN- | Ejecuciones |
| `historial` | Lista append-only | Sí | `{fecha, run_id, de, a, campo, justificacion}` | — |

## 5. Estados y transiciones

| Desde | Hacia | Condición |
|---|---|---|
| (alta) | CANDIDATA | Pasa GC1 en el cribado |
| CANDIDATA | EN_INVESTIGACION | Investigación dirigida iniciada |
| CANDIDATA | DESCARTADA | Señal no confirmada o PS7 |
| EN_INVESTIGACION | FINALISTA | GC2 y GC3 superadas (entre las 5 mejores de su tipo por RK provisional) |
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
| Vigentes por tipo de activo | `estado` ∈ {PROPUESTA, VIGENTE}, `tipo_activo` | F0 de cada ciclo; arrastre verificado |
| Top-3 por RUN- | `run_ids`, `rango_top3` | Historial e informes |
| Invalidaciones próximas | `invalidacion` a < 10 % del umbral | GC0 cambio material |
| Por decisión del Broker | `decision_broker.decision` | Lecciones de producto del Evaluador |
| Por clúster | `cluster_id`, `factor_dominante` | Apuestas independientes |
| Por tendencia | `tnd_ids` | Trazabilidad TND↔OPP |
| Duplicados entre tipos | `ambito` normalizado + `tesis` | Control de la regla 5 de 2.6 (una oportunidad, un solo top-3) |
| Por indicador de seguimiento | `indicador_seguimiento.serie_ht01` | Resolución de pronósticos y duplicados |
| Finalistas no seleccionadas | `estado` = EN_OBSERVACION con puertas de FINALISTA | Falsos negativos |
| Índice operativo | — | Recuentos por estado, tipo de activo y tipo de opción |

## 7. Ejemplo ficticio

> **EJEMPLO FICTICIO — no es una entrada real.** Ningún dato describe una oportunidad existente.

```json
{"opp_id":"OPP-2026-0001","version":1,"nombre":"Renta variable europea de equipos de recarga (exposición temática)","nombre_llano":"Empresas europeas de cargadores eléctricos",
 "tipo_activo":"RV","subtipo":"Temática","motivo_asignacion_tipo":"Gana por la evolución de un grupo de empresas (regla 1 de 2.6)","perfiles_motor":["PERF-ACC","PERF-TEM"],"tipo_opcion":"TEMATICA",
 "ambito":{"incluye":"Fabricantes y operadores europeos de recarga eléctrica comercial","excluye":"Fabricantes de automóviles y eléctricas integradas","region":"Europa"},"regiones":["EUR"],"divisa_exposicion":"EUR","tnd_ids":["TND-2026-0001"],
 "tesis":{"texto":"Los fabricantes de recarga comercial crecerán por encima de lo que descuentan sus múltiplos","clm_id":"CLM-2026-0004"},
 "mecanismo":"Despliegue de flotas eléctricas urbanas","por_que_ahora":"Revisiones de beneficios al alza no reflejadas en el PER relativo",
 "valoracion":{"metodo":"PER relativo frente a historia","resultado":"descuento del 12 % frente a su media de 5 años","calc_ids":["CALC-2026-0011"],"que_descuenta_el_precio":"crecimiento de beneficios del 6 % anual"},
 "catalizadores":[{"evento":"resultados anuales del sector","fecha":"2027-02-20","nivel":"S2"}],"riesgos":["retraso de subvenciones","competencia asiática"],
 "riesgo_1a5":4,"riesgo_cola":{"perdida_escenario_adverso":"-28 %","calc_id":"CALC-2026-0012"},
 "invalidacion":[{"indicador":"revisiones de BPA del sector","umbral":"< 0 % en 3 meses","plazo":"2027-03-31"}],"que_no_sabemos":["ritmo real de pedidos públicos"],
 "horizontes":{"H3":{"aplicable":"SI","vista":"RELATIVA","banda":"más probable que no","prob_publicada":null,"certificado_ref":null,"prg_ids":["PRG-2026-0001"]}},
 "indicador_seguimiento":{"nombre":"índice temático europeo de electrificación (ficticio)","simbolo":"IDX-FICT-001","serie_ht01":"IDX-FICT-001","fuente":"HT-01","divisa":"EUR"},
 "liquidez":"MEDIA","reversibilidad":"MEDIA","invertibilidad":{"universo_suficiente":true,"nota":"Más de 15 compañías cotizadas en mercados regulados europeos (ficticio)"},
 "encargo_bloque_B":{"criterios_seleccion_sugeridos":["Más del 50 % de ingresos en recarga comercial","Cartera de pedidos creciente","Balance sin necesidad de ampliación"],
   "metricas_clave":["Cartera de pedidos","Margen bruto","Puntos de recarga instalados"],"preguntas_para_B":["¿Qué compañías capturan margen y cuáles solo volumen?"]},
 "ejemplos_ilustrativos":["(ilustración ficticia del ámbito: fabricantes europeos de cargadores de alta potencia)"],
 "puntuaciones":{"T":70,"E":65,"M":50,"A":65,"RK":66,"desglose_ref":"HT03-2026-0011","pasada":1,"methodology_version":"4.0","fecha":"2026-11-07"},
 "cluster_id":"CL-ELEC-EUR","factor_dominante":"inversión en electrificación europea","relevancia_decisional":"ALTA","siguiente_paso_sugerido":"PROFUNDIZAR_EN_A",
 "que_cambiaria_la_conclusion":["revisiones de BPA negativas"],"confianza":"probable","estado":"PROPUESTA","rango_top3":2,"decision_broker":[],"run_ids":["RUN-2026-0001"]}
```
