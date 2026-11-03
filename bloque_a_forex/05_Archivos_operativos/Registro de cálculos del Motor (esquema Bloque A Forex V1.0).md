# Esquema de archivo operativo — RC Registro de cálculos del Motor

**Bloque A Forex · Robot Investor · Versión V1.0 · 02/11/2026** · Subordinado al Documento 0 del Bloque A Forex, versión óptima V1.0.

---

## 1. Propósito

El Registro de cálculos (RC) conserva cada servicio del Motor de Cálculo Avanzado (Forex): cálculos (CT-09), re-ejecuciones independientes (CT-10), rechazos y fallos, con su **artefacto reproducible** (método, versión, datos con fecha, fijación y vintage, convenciones de cotización y de días, parámetros, semilla, código y transformaciones). Es la fuente de toda cifra que el bloque entrega (R7): carry y carry ajustado por volatilidad, forwards por paridad cubierta, base cruzada, desviaciones de PPA/BEER/REER, factores cambiarios, volatilidades y *risk reversals*, escenarios y saltos de régimen, puntuaciones predictivas frente al paseo aleatorio y al forward, y backtests de estrategias. Es también la base de la reutilización por idempotencia (10.2 del Documento 0) y el soporte de las comprobaciones G3-DAT-07, G3-MET-12, G3-MET-13 y G3-FX-05.

## 2. Propietario, lectores y contratos

| Aspecto | Contenido |
|---|---|
| Propietario de escritura | AG-13 Motor de Cálculo Avanzado (único; con varias instancias, escritura serializada por `calc_id`) |
| Lectores | AG-18 Orquestador, AG-19 Auditor, AG-20 Evaluador, AG-15 Documentador para el Motor, AG-01 Coordinador (para responder consultas de método), AG-11 Contrarias (para contrastar cálculos de las finalistas) y cada solicitante sobre sus propios servicios |
| Contratos | CT-09 (Analizador, Analistas de segmento y transversales, Prospectiva, Evaluador, Orquestador, Auditor, Documentadores y Buscador → Motor); CT-10 (Orquestador, Auditor, Evaluador → Motor); CT-20 (documentación metodológica, referenciada) |
| Herramientas | HT-01 (datos: contado con fijación, puntos forward, curvas OIS y de swaps, volatilidades implícitas, base cruzada, posicionamiento, reservas, macro), HT-06 (caché) |

## 3. Reglas

1. **Todo servicio se registra**, sea cual sea su estado (servido, con limitaciones, aclaración pendiente, rechazado, fallido). El Motor comunica incidencias, informes de calidad y propuestas en la sección «Incidencias y propuestas» de este registro, que el Orquestador revisa.
2. **Append-only**: un reintento o una corrección abre entrada nueva referenciada; la original conserva su estado.
3. **Idempotencia**: la misma `clave_idempotencia` devuelve el artefacto registrado (`cache_hit`) sin recalcular ni duplicar.
4. **Artefacto reproducible** suficiente para reconstruir el cálculo sin el Motor.
5. **Fechas y fijaciones**: todo dato de entrada con fecha de dato, fecha de recuperación, vintage y, en tipos de cambio, fijación (fuente, hora, zona); `fecha_limite_informacion` cuando el solicitante evalúa históricamente (el Motor no usa datos conocibles después de ella; el posicionamiento CFTC cuenta desde su publicación del viernes).
6. **Convenciones cambiarias declaradas**: par en convención de mercado `BASE/COTIZADA`; base de días de cada divisa (ACT/360 en USD, EUR, JPY, CHF y la mayoría; ACT/365 en GBP, AUD, NZD, CAD y otras); fecha de valor de contado (T+2 en general; T+1 en USD/CAD y en algunos pares emergentes); calendario de festivos de liquidación; tipo de rentabilidad (contado o total con carry).
7. **Clase de cifra** (determinista o estadística) e **incertidumbre** obligatorias en resultados estadísticos.
8. **Referencias ingenuas** en todo cálculo predictivo: paseo aleatorio siempre; forward como predictor en rentabilidad total; rentabilidad nula o índice de la estrategia en estrategias (MC-10).
9. **Backtests sin sesgos**: universo *point-in-time* (incluidas divisas desaparecidas o redenominadas), vintages, señal en t y medición desde la fijación de t+1, corrección por pruebas múltiples; los costes de instrumento no se modelan (son del Bloque B) y se declara su omisión.
10. **Madurez** del método (documentado, implementado, validado; R22).
11. **Re-ejecuciones CT-10** en aislamiento, por MC-08, con comparación y tolerancia; las discrepancias no alteran la entrada original.
12. Retención de artefactos: 5 años (Anexo A).

## 4. Formato de entrada

| Campo | Tipo | Oblig. | Valores / formato |
|---|---|---|---|
| `calc_id` | Identificador | Sí | `CALC-AAAA-NNNN`; identifica también el artefacto (`artefacto_id` = `calc_id`) |
| `contrato` | Enumerado | Sí | CT-09 · CT-10 |
| `msg_id` / `run_id` · `query_id` | Texto | Sí | Trazabilidad con el solicitante (`run_id` con forma RUN-FX-) |
| `solicitante` | Enumerado | Sí | AG-02 · AG-03…AG-09 · AG-21 · AG-10 · AG-14 · AG-15 · AG-16 · AG-18 · AG-19 · AG-20 (CT-09); AG-18 · AG-19 · AG-20 (CT-10) |
| `operacion` | Objeto | Sí | `{method_id, method_version, ficha_id, ficha_version, catalog_version, familia, op_sin_ficha}` |
| `perfil` | Lista | Sí | PERF-FX-G10 · PERF-FX-EM · PERF-FX-FACT · TRANSVERSAL (combinados si procede) |
| `segmento` / `horizonte` | Enumerado | Si aplica | G10N…ESTR / H1–H4 |
| `pares` / `composicion` | Lista | Si aplica | Pares en convención de mercado / `{divisa, peso, lado}` |
| `convenciones` | Objeto | Si hay tipos de cambio o tipos de interés | `{base_dias por divisa, fecha_valor_contado, calendario_festivos, tipo_rentabilidad PRECIO_CONTADO·RENTABILIDAD_TOTAL·NIVEL_VOLATILIDAD, divisa_medicion}` |
| `modo` | Enumerado | Sí | SYNC_CALC · ASYNC_CALC |
| `plan` | Enumerado | Sí | PLAN_MIN · PLAN_STD · PLAN_EXT |
| `modulos` | Lista | Sí | MC-01 … MC-10 (efectivos, no previstos) |
| `prioridad` | Enumerado | Sí | INTEGRIDAD · MATERIAL · ORDEN_LLEGADA |
| `datos` | Lista | Sí | `{serie_ht01 o valor, par, unidad, divisa, fijacion {fuente, hora, zona}, fecha_dato, fecha_recuperacion, conocible_desde, vintage, fuente}` |
| `fecha_limite_informacion` | Fecha-hora | Si evaluación histórica | Ningún dato conocible después |
| `parametros` | Lista | Sí | `{nombre, valor, unidad}` |
| `semilla` | Entero o null | Sí | Con generador si no es null |
| `as_of` | Fecha | Sí | Corte temporal de los datos |
| `estado` | Enumerado | Sí | Sección 5 |
| `resultado` | Objeto | Si SERVED* | `{forma VALOR·TABLA·SERIE·DISTRIBUCION, payload, unidades}` |
| `clase_cifra` | Enumerado | Si SERVED* | DETERMINISTA · ESTADISTICA |
| `incertidumbre` | Objeto | Si ESTADISTICA | `{tipo IC·ERROR_ESTANDAR·CUANTILES·ESCENARIOS, valores, nivel}` |
| `referencias_ingenuas` | Lista | Si predictivo | `{tipo PASEO_ALEATORIO·FORWARD·IMPLICITA_FORWARD·RENTABILIDAD_NULA·INDICE_ESTRATEGIA·CESTA_SEGMENTO·IMPLICITA_OPCIONES, valor, metrica_comparada, prueba DM_HLN·CLARK_WEST·PESARAN_TIMMERMANN, p_valor}` |
| `control_sesgos` | Objeto | Si backtest | `{universo_point_in_time, vintages, desfase_senal_medicion, pruebas_multiples DEFLATED_SHARPE·HOLM·OTRA, costes_instrumento NO_MODELADOS_DECLARADO}` |
| `artefacto` | Objeto | Sí | `{code_ref, inputs_effective, transformations, rounding_policy, data_quality_report}` |
| `verificacion_interna` | Objeto | Sí | `{identity_checks, second_path, integracion_plan}` (p. ej., forward por CIP frente a puntos de mercado; cruce sintético frente a cruce directo) |
| `madurez_metodo` | Enumerado | Sí | DOCUMENTADO · IMPLEMENTADO · VALIDADO |
| `clave_idempotencia` | Texto | Sí | Hash de (operación, versiones, datos, convenciones, parámetros, semilla, perfil) |
| `cache_hit` | Booleano | Sí | Respuesta servida desde caché |
| `consumo_uc` | Número | Sí | — |
| `tiempos` | Objeto | Sí | `{recibido, iniciado, completado}` ISO 8601 |
| `limitaciones` / `incidencias` | Listas | Sí | «ninguna» solo con motivo |
| `motivo_rechazo` | Texto | Si REJECTED · CLARIFICATION_NEEDED · FAILED | — |
| `reejecucion` | Objeto | Si CT-10 | `{calc_original, motivo, aislamiento CONFIRMADO, tolerancia, coincide SI·NO·DENTRO_TOLERANCIA, diferencias, categoria DATOS_DISTINTOS·CONVENCION_DISTINTA·ERROR_ORIGINAL·ERROR_REEJECUCION·NO_DETERMINISMO, diagnostico, audit_ref}` |
| `consumido_por` | Lista | No | RUN-FX-, OPP-FX-, PRG-FX-, CERT-, AJU-, HAL- (añadido por referencias posteriores) |

## 5. Estados y transiciones

`RECIBIDO` → `SERVED` · `SERVED_WITH_LIMITATIONS` · `CLARIFICATION_NEEDED` · `REJECTED` · `FAILED`. Los estados finales son cerrados: una aclaración respondida o un reintento abre una entrada nueva con `reintento_de`. G3 solo acepta cifras de entradas `SERVED` o `SERVED_WITH_LIMITATIONS` (con la limitación declarada en el entregable). Una petición que exija elegir un instrumento, su coste o su apalancamiento se rechaza (`REJECTED`, R21).

## 6. Índices de consulta

| Índice | Clave | Uso |
|---|---|---|
| Idempotencia | `clave_idempotencia` | Reutilización antes de calcular |
| Por ejecución | `run_id`, `query_id` | G3-DAT-07; auditoría |
| Por método | `method_id`, `method_version`, `madurez_metodo` | G3-MET-13; DOC-M |
| Por perfil y segmento | `perfil`, `segmento` | G3-MET-12 |
| Por par | `pares` | Reutilización de carry, forwards y volatilidades entre segmentos y capas transversales |
| Referencias ingenuas | `referencias_ingenuas.tipo` | Evaluador; G3-FX-06 |
| Re-ejecuciones | `contrato` = CT-10, `reejecucion.coincide` | Orquestador, Auditor, Evaluador |
| Por consumidor | `consumido_por` | Propagación de correcciones |
| Rechazos y fallos | `estado` | Salud del Motor |

## 7. Ejemplo ficticio

> **EJEMPLO FICTICIO — no es una entrada real.** Datos, series, fichas e identificadores inventados.

```json
{"calc_id":"CALC-FX-2026-0202","contrato":"CT-09","msg_id":"MSG-2026-11-07-0412","run_id":"RUN-FX-2026-0001","solicitante":"AG-03",
 "operacion":{"method_id":"MET-FX-CARRY-AJ-01","method_version":"1.0","ficha_id":"FICHA-FICT-CARRY-01","ficha_version":"1.0","catalog_version":"FX-1.0","familia":"carry y paridades","op_sin_ficha":false},
 "perfil":["PERF-FX-G10"],"segmento":"G10N","horizonte":"H3","pares":["USD/JPY"],
 "composicion":[{"divisa":"JPY","peso":1.0,"lado":"LARGO"},{"divisa":"USD","peso":1.0,"lado":"CORTO"}],
 "convenciones":{"base_dias":{"USD":"ACT/360","JPY":"ACT/360"},"fecha_valor_contado":"T+2","calendario_festivos":"Nueva York y Tokio","tipo_rentabilidad":"RENTABILIDAD_TOTAL","divisa_medicion":"JPY"},
 "modo":"SYNC_CALC","plan":"PLAN_MIN","modulos":["MC-01","MC-02"],"prioridad":"MATERIAL",
 "datos":[{"serie_ht01":"FICT-USDJPY-WMR16","par":"USD/JPY","unidad":"JPY por USD","divisa":"JPY","fijacion":{"fuente":"WM_REUTERS","hora":"16:00","zona":"Europe/London"},"fecha_dato":"2026-11-06","fecha_recuperacion":"2026-11-07T07:50:00+01:00","conocible_desde":"2026-11-06T16:05:00+00:00","vintage":"2026-11-06","fuente":"HT-01"},
   {"serie_ht01":"FICT-USDJPY-FWD3M","par":"USD/JPY","unidad":"puntos forward","divisa":"JPY","fijacion":{"fuente":"OTRA","hora":"16:00","zona":"Europe/London"},"fecha_dato":"2026-11-06","fecha_recuperacion":"2026-11-07T07:50:00+01:00","conocible_desde":"2026-11-06T16:05:00+00:00","vintage":"2026-11-06","fuente":"HT-01"},
   {"serie_ht01":"FICT-USDJPY-IV3M","par":"USD/JPY","unidad":"vol. implícita %","divisa":null,"fijacion":{"fuente":"OTRA","hora":"16:00","zona":"Europe/London"},"fecha_dato":"2026-11-06","fecha_recuperacion":"2026-11-07T07:50:00+01:00","conocible_desde":"2026-11-06T16:05:00+00:00","vintage":"2026-11-06","fuente":"HT-01"}],
 "fecha_limite_informacion":null,"parametros":[{"nombre":"plazo","valor":3,"unidad":"meses"}],
 "semilla":null,"as_of":"2026-11-06","estado":"SERVED",
 "resultado":{"forma":"TABLA","payload":{"carry_anual_pct":-3.1,"signo_respecto_tesis":"EN_CONTRA","vol_implicita_3m_pct":8.9,"carry_ajustado_vol":-0.35},"unidades":{"carry_anual_pct":"% anual","vol_implicita_3m_pct":"% anual","carry_ajustado_vol":"ratio"}},
 "clase_cifra":"DETERMINISTA","incertidumbre":null,"referencias_ingenuas":null,
 "artefacto":{"code_ref":"ficticio","inputs_effective":"…","transformations":"carry = (F/S − 1) × 360/días anualizado desde los puntos forward a 3 meses; ajustado = carry / vol. implícita a 3 meses","rounding_policy":"2 decimales","data_quality_report":"sin huecos"},
 "verificacion_interna":{"identity_checks":["F = S + puntos/100 (convención de pips en JPY)"],"second_path":"carry por diferencial OIS a 3 meses USD–JPY: −3,05 %; diferencia atribuida a la base cruzada"},"madurez_metodo":"IMPLEMENTADO",
 "clave_idempotencia":"4d7a…(ficticia)","cache_hit":false,"consumo_uc":0.2,"limitaciones":["base cruzada no descompuesta en este cálculo"],"incidencias":[]}
```
