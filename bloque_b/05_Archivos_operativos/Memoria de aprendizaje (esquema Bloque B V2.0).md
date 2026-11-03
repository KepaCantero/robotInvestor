# Esquema de archivo operativo — F5 Memoria de aprendizaje

**Bloque B · Robot Investor · Versión óptima V2.0 · actualizado V2.1, 03/11/2026** · Subordinado al Documento 0 del Bloque B óptima V2.1 (ante discrepancia, manda el Documento 0).

---

## 1. Propósito

F5 es la memoria de lo que el Bloque B **ha aprendido de forma verificable** (sección 12 del Documento 0; R24): lotes de resolución de pronósticos, métricas de acierto, calibración e IC de rango por celda, **certificados** de probabilidad y de ranking (R13; 12.3), el **modelo de tiempos** calibrado con el historial de F1 (9.9), las lecciones LEC-B y las **fichas de lección**, el rendimiento por especialista, fuente, método y playbook, la fiabilidad medida de las fuentes de F9, los ajustes aplicados y en sombra, las propuestas de tipo 3, el historial de aciertos publicable y las lecciones de producto (Broker y Bloques C.x). Desde la V2.1 también mide las **puertas de viabilidad** (falsos negativos de PV1–PV3, con las paradas y las continuaciones forzadas), las **consultas al Broker** (tasa de respuesta en plazo, efecto, pausa de las bloqueantes, consultas recurrentes), los **seguimientos encargados** (acierto del semáforo, utilidad de las recomendaciones, coste por ciclo) y los **hitos H5**, y recalibra el modelo de tiempos **por capa** (12.7).

Cada agente lee al inicio de cada encargo el extracto de su ámbito (máximo diez lecciones vigentes, 10.7) y la sección «Novedades»; el Coordinador lee el modelo de tiempos para estimar; HT-09 lee los certificados; el Director consulta las fichas de lección en F0.

## 2. Propietario, lectores y contratos

| Aspecto | Contenido |
|---|---|
| Propietario de escritura | AG-B23 Evaluador de Previsiones, Aprendizaje y Seguimiento (único; instancia única con cola) |
| Lectores | Todos (extracto por ámbito vía HT-06) |
| Contratos | CT-B-22 (difusión: resultados, calibración, IC de rango, certificados, lecciones, ajustes, modelo de tiempos), CT-B-26 (entradas de producto: decisiones, resultados, valoraciones, preguntas repetidas), CT-B-13/CT-B-14 (cálculos y re-ejecuciones que sostienen métricas y decisiones) |
| Consumidores clave | AG-B01 (modelo de tiempos), AG-B02 (fichas de lección, historial de aciertos, certificados), AG-B12 (pesos de S, certificados de ranking), AG-B13 (calibración y certificados), AG-B20 (fiabilidad de fuentes), AG-B21 (lecciones operativas para guías), HT-09 (certificados) |

## 3. Reglas

1. **Append-only**: métricas, certificados, lecciones y ajustes son entradas nuevas; los estados cambian por entradas nuevas; nada se borra.
2. **Toda cifra publicada** procede de un CALC-B del Motor (MC-B10 para la evaluación) o de un recuento reproducible sobre F1, F3 y F4 (R9).
3. **Sin fuga y sin supervivencia** (12.6): cada métrica declara `comprobacion_fuga` y, en rankings, `comprobacion_supervivencia`. Una métrica FALLIDA no sostiene ningún ajuste ni certificado.
4. **Celdas** (12.1): nivel 1 = tipo de objeto × tipo de activo × horizonte; nivel 2 = + método (probabilidad) o + playbook (ranking), usado para certificar; nivel 3 = + especialista, fuente o perfil del Motor (diagnóstico, con contracción).
5. **Muestras** (Anexo A): ninguna recalibración con menos de 30 pronósticos o 15 rankings resueltos en la celda; ningún certificado de probabilidad con n < 100; ningún certificado de ranking con menos de 30 rankings resueltos.
6. **Bandas** (12.2): cada peso ±5 puntos por trimestre y ±15 en total; cada umbral ±5 por trimestre y ±10 en total; mínimos de pureza ±10 en total. Todo ajuste se evalúa **en sombra** durante un trimestre y es reversible. Fuera de bandas: propuesta de tipo 3 (R24).
7. **Intocables por ajuste automático** (12.6): reglas críticas, seguridad, canales, matriz de archivos y el **umbral de 30 minutos** de la puerta de tiempo. El modelo de tiempos se recalibra; el umbral, no.
8. **Lecciones**: máximo 10 vigentes por ámbito en el extracto; caducidad obligatoria; las metodológicas recurrentes se convierten en **fichas de lección** (`ficha = true`) que el Director consulta en F0 (12.4).
9. **Novedades**: sección semanal con certificados emitidos o revocados, ajustes, lecciones nuevas, versión vigente del modelo de tiempos.
10. **Prefijos internos** del archivo (complementarios al Anexo C, que fija LEC-B): `RES-B` lote de resolución, `MET-B` métricas, `CERT-B` certificado, `MOD-B` versión del modelo de tiempos, `RND-B` rendimiento operativo, `FUE-B` fiabilidad de fuente, `AJU-B` ajuste, `P3-B-EVAL` propuesta de tipo 3, `HAC-B` historial de aciertos, `PRO-B` lección de producto.

## 4. Formato de entrada

### 4.1 Lote de resolución (RES-B)

`res_id` (`RES-B-AAAA-MM-DD`), `fecha`, `fecha_corte`, `prg_resueltos`, `prg_no_resolubles` (con motivo), `rankings_resueltos` (PRG-B de familia RANKING), `rec_ids_afectadas` (campo `resultado` de F3 actualizado), `calc_ids`, `comprobacion_fuga`, `comprobacion_supervivencia`.

### 4.2 Métricas por celda (MET-B)

| Campo | Tipo | Valores / formato |
|---|---|---|
| `met_id` | Identificador | `MET-B-AAAA-MM-<celda>` |
| `celda` | Objeto | `{nivel 1·2·3, tipo_objeto, tipo_activo, horizonte, metodo, playbook, especialista, fuente, perfil_motor}` |
| `ventana` / `n` / `n_eff` | Texto / enteros | — |
| `ambito` | Objeto | `{acierto_direccional {tasa, ic90_wilson}, error_vs_ingenua, brier, log, bss {valor, ic90, referencia, bootstrap BLOQUES·CONGLOMERADOS, replicas}, ece, ece_p90_nulo, curva_fiabilidad (calc_id), rentabilidad_relativa_invertir {media, ic90}, falsos_positivos, falsos_negativos}` |
| `ranking` | Objeto | `{ic_rango_medio {valor, ic90}, exceso_topN_vs_universo {media, ic90}, tasa_acierto_topN, contribucion_componentes S {PE, QL, VA, MO, RI, LA, CO}, frente_ranking_aleatorio, frente_factor_trivial}` |
| `seleccion_vs_C` | Objeto | `{prioritarios_valorados_por_C, superaron_valoracion_C, tasa, n}` (12.5; solo con lo comunicado por el Broker) |
| `sobreconfianza` | Objeto | `{C_media_declarada, acierto_observado, brecha, alerta sí/no}` (11.1, mensual) |
| `puertas_viabilidad` | Objeto | V2.1: `{paradas_PV1, paradas_PV2, no_superadas_PV3, forzadas, falsos_negativos {n, tasa, ic90} (ámbitos parados cuyo indicador batió después a su referencia en el horizonte), resultado_tras_forzar}` (12.7) |
| `consultas_broker` | Objeto | V2.1: `{n, por_tipo, por_origen, tasa_respuesta_en_plazo, efecto {SIN_CAMBIO, SUPUESTO_CAMBIADO, CONCLUSION_CAMBIADA}, minutos_pausa_bloqueantes, recurrentes}` |
| `seguimientos` | Objeto | V2.1: `{seg_activos, ciclos, acierto_semaforo, utilidad_recomendaciones (reactivaciones y pasos a C con su resultado), coste_medio_ciclo {minutos, uc}, ciclos_sin_novedad}` |
| `hitos_h5` | Objeto | V2.1: `{resueltos, cumplidos, criticos_incumplidos, frente_RI_LIN}` (FC-HITO-001) |
| `calc_ids` / `comprobacion_fuga` / `comprobacion_supervivencia` | Lista / enumerados | SUPERADA · FALLIDA |
| `madurez` | Enumerado | documentado · implementado · validado (R26) |

### 4.3 Certificado (CERT-B)

| Campo | Valores / formato |
|---|---|
| `cert_id` | `CERT-B-AAAA-NNNN` |
| `clase_certificado` | PROBABILIDAD · RANKING |
| `celda` | Probabilidad: `{tipo_activo, horizonte, metodo}`; ranking: `{playbook, horizonte}` |
| `criterio` | Probabilidad: n ≥ 100, extremo inferior del IC 90 % del BSS > 0, ECE ≤ percentil 90 del ECE simulado bajo calibración perfecta y < 0,15, Holm si hay varias celdas; ranking: ≥ 30 rankings, extremo inferior del IC 90 % del IC de rango medio > 0 y del exceso del top-N frente al universo > 0 |
| `evidencia` | `{n, bss, bss_ic90, ece, ece_p90_nulo, holm_superado, ic_rango_ic90, exceso_ic90, met_id, calc_id, reejecucion (CALC-B de CT-B-14)}` |
| `methodology_version` / `emitido` / `revision` | — |
| `estado` / `motivo_cambio` | Sección 5 |

### 4.4 Modelo de tiempos (MOD-B)

| Campo | Valores / formato |
|---|---|
| `mod_id` | `MOD-B-AAAA-NN` (versión) |
| `especificacion` | Regresión por tipo de nodo: dimensión × profundidad; selección × tamaño del universo × tipo de activo; prospectiva; refutación; auditoría (vueltas esperadas); redacción; reutilización F6 como variable (Anexo A). V2.1: además desglose del cambio de cadena y radar de emergentes (AG-B24), estimación y ajuste **por capa** (0–4), tramo `HASTA_PV2`, informe de parada y ciclo N1-SEG |
| `coeficientes` | Por tipo de nodo, con su incertidumbre |
| `muestra` | `{peticiones, ventana, n_nuevas_desde_anterior (≥ 20 para reestimar)}` |
| `ajuste` | `{error_medio_abs_p50, cobertura_p80 (fracción de peticiones con real ≤ p80), sesgo, por_tipo_nodo, por_capa (V2.1)}` |
| `calc_id` / `fecha_efecto` / `estado` | VIGENTE · EN_SOMBRA · SUSTITUIDO |
| `nota` | El umbral de 30 minutos es OPERADOR: este modelo no lo cambia |

### 4.5 Lección (LEC-B)

| Campo | Valores / formato |
|---|---|
| `lec_id` | `LEC-B-AAAA-NNNN` |
| `ambito` | `{tipo_objeto, tipo_activo, horizonte, agente[], fuente, metodo, playbook}` |
| `nivel` | OPERATIVO · PREDICTIVO · METODOLOGICO (antecedente de tipo 3) |
| `tipo` | PREDICTIVA · RANKING · OPERATIVA · TIEMPO · PRODUCTO · FUENTE · CALIBRACION · PUERTA (V2.1: falso negativo de una puerta de viabilidad) · CONSULTA (V2.1: consulta recurrente al Broker, para mejorar la normalización de las peticiones) · SEGUIMIENTO (V2.1) |
| `observacion` / `evidencia` | Factual con cifras / CALC-B, MET-B, PRG-B, PET-B, QRY-B, HAL-B y, desde la V2.1, CNS-B, SEG-B, CIC-B |
| `recomendacion` | Qué hacer distinto y en qué fase |
| `fuerza` | anecdotica · recurrente · estadistica |
| `n` / `efecto` | Con IC |
| `ficha` | true si es ficha de lección (metodológica recurrente) |
| `caducidad` | 3, 6 o 12 meses según fuerza |
| `estado` / `sustituye` | Sección 5 |

### 4.6 Rendimiento operativo (RND-B)

`rnd_id`, `periodo`, `objeto` (especialista AG-B03…B11 · fuente · método · playbook · nodo del grafo), `aporte` (cambios de A, E, C, S o del top-N atribuibles), `minutos`, `uc`, `aporte_por_minuto`, `reutilizacion_F6` (dimensiones reutilizadas y si la reutilización resultó correcta), `atascos_grafo` (nodos que bloquearon a otros), `fuentes` (HT-08, F1, RC, HA).

### 4.7 Fiabilidad de fuente (FUE-B)

`fue_id`, `ref_id` (ficha de F9), `periodo`, `n` (pronósticos de la fuente resueltos), `aciertos`, `bss`, `bss_contraido`, `puntos_historial` (0–20; neutro 10 mientras no haya resolución), `calc_id`, `comunicado` (msg_id de CT-B-22 al Buscador).

### 4.8 Ajuste (AJU-B) y propuesta de tipo 3 (P3-B)

- `AJU-B`: `aju_id`, `parametro` (P-B-NN de F10), `de`, `a`, `banda` `{trimestral, total}`, `acumulado_vs_inicial`, `evidencia` `{objetivo, mejora_fuera_muestra, ic90, calc_id, reejecucion}`, `methodology_version` `{de, a}`, `efecto_desde`, `sombra_hasta`, `estado`, `resultado_sombra` `{metrica_nueva, metrica_anterior, veredictos_cambiados, topN_cambiados, decision CONFIRMADO·REVERTIDO}`, `cfg_id` (F10).
- `P3-B`: `p3_id` (`P3-B-EVAL-AAAA-NNNN`; el Orquestador la registra en la cola de tipo 3 de HA con el mismo identificador), `objeto`, `motivo` (fuera de banda · sin banda · cambio hacia o desde «No» en horizontes · componente o playbook nuevo · separación del Vigía · otro), `evidencia`, `impacto_esperado`, `pruebas_regresion` (identificadores del Plan de pruebas), `plan_reversion`, `elevada_via` (msg_id CT-B-22 al Orquestador, que la registra en la cola de tipo 3 de HA), `estado`.

### 4.9 Historial de aciertos publicable (HAC-B)

`hac_id`, `ventana`, `ambitos` `{n, aciertos, rentabilidad_relativa_media, ic90, por_veredicto, por_tipo_objeto}`, `rankings` `{n, exceso_medio, ic_rango_medio, por_playbook}`, `certificacion` (texto: «sin ventaja demostrada todavía» o certificados vigentes), `no_resolubles_excluidos`, `calc_id`, `publicado` (fecha). Es el que el Director incluye en el paquete de síntesis (14.1 punto 15) y el Redactor resume en «cómo nos fue».

### 4.10 Lección de producto (PRO-B)

`pro_id`, `tema` (`tema_normalizado` de QRY-B o, desde la V2.1, clase de duda de una consulta al Broker: tipo y tema, recurrente si aparece en 3 peticiones distintas en 8 semanas), `qry_ids`, `cns_ids` (V2.1), `veces_4_semanas`, `utilidad` `{por_entregable: mediana y distribución, tendencia}`, `decisiones_broker` `{enviados_vs_descartados: rentabilidad relativa de cada grupo, n}`, `valoraciones_C` (resumen de lo comunicado), `lec_id` generada, `propuesta_mejora` (sección por defecto en un entregable, regla de nivel AUTO…).

## 5. Estados y transiciones

| Objeto | Transiciones |
|---|---|
| CERT-B | VIGENTE → EN_OBSERVACION → VIGENTE · REVOCADO; VIGENTE → REVOCADO (BSS o exceso ≤ 0 en la ventana móvil, ECE ≥ 0,12, fuga detectada, cambio de método o de versión mayor de metodología) |
| LEC-B | VIGENTE → REVISADA (sustituida) · CADUCADA · REFUTADA |
| MOD-B | EN_SOMBRA → VIGENTE → SUSTITUIDO |
| AJU-B | PROPUESTO → EN_SOMBRA → CONFIRMADO · REVERTIDO |
| P3-B | ENVIADA → APROBADA → APLICADA · RECHAZADA (según comunique el Orquestador) |

## 6. Índices de consulta

| Índice | Clave | Uso |
|---|---|---|
| Lecciones por ámbito | `ambito.*`, `fuerza`, `estado` = VIGENTE | Lectura al inicio de cada encargo (máx. 10) |
| Fichas de lección | `ficha` = true | F0 del Director |
| Certificados vigentes | `clase_certificado`, `celda`, `estado` | Prospectiva, Seleccionador, Director, HT-09 |
| Modelo de tiempos vigente | `MOD-B.estado` = VIGENTE | Estimación del Coordinador (F0) y proyección de HT-08 |
| Métricas por celda | `celda`, `ventana` | CT-B-22; revisión trimestral |
| Historial de aciertos | último HAC-B | Paquete de síntesis |
| Fiabilidad por fuente | `ref_id` | Rúbrica de F9 (20 puntos de exactitud) |
| Ajustes en sombra | `estado` = EN_SOMBRA | Cierre trimestral |
| Puertas, consultas y seguimientos (V2.1) | `MET-B.puertas_viabilidad`, `MET-B.consultas_broker`, `MET-B.seguimientos`, `LEC-B.tipo` ∈ {PUERTA, CONSULTA, SEGUIMIENTO} | Revisión trimestral de umbrales PV (calibrables dentro de bandas); normalización de peticiones; utilidad de los seguimientos |

## 7. Ejemplo ficticio

> **EJEMPLO FICTICIO — no es una entrada real.**

```json
{"mod_id":"MOD-B-2027-03","especificacion":"regresión por tipo de nodo; variables: profundidad, tamaño del universo, n.º de tipos de activo, reutilización F6",
 "coeficientes":{"dimension_P3":{"min":6.1,"ic90":[4.9,7.4]},"dimension_P2":{"min":3.4,"ic90":[2.8,4.1]},"seleccion_por_100_activos":{"min":4.2,"ic90":[3.3,5.0]},"vuelta_auditoria":{"min":5.5,"ic90":[4.0,7.2]}},
 "muestra":{"peticiones":64,"ventana":"2026-11-10/2027-02-28","n_nuevas_desde_anterior":23},
 "ajuste":{"error_medio_abs_p50":4.8,"cobertura_p80":0.81,"sesgo":"+1,2 min (infraestima la refutación en N3)"},
 "calc_id":"CALC-B-2027-0410","fecha_efecto":"2027-03-03","estado":"VIGENTE","nota":"El umbral de 30 minutos no se modifica por este ajuste"}
```
