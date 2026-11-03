# Esquema de archivo operativo — RC Registro de cálculos del Motor

**Bloque A · Robot Investor · Versión óptima V4.0 · 01/11/2026 · actualizado V5.1 (03/11/2026)** · Subordinado al Documento 0 óptima V5.1. Cambio V5.1: horizonte H5.

---

## 1. Propósito

El Registro de cálculos (RC) conserva cada servicio del Motor de Cálculo Avanzado: cálculos (CT-09), re-ejecuciones independientes (CT-10), rechazos y fallos, con su **artefacto reproducible** (método, versión, datos con fecha y vintage, parámetros, semilla, código y transformaciones). Es la fuente de toda cifra que el bloque entrega (R7), la base de la reutilización por idempotencia (10.2 del Documento 0) y el soporte de las comprobaciones G3-DAT-07 y G3-MET-13.

## 2. Propietario, lectores y contratos

| Aspecto | Contenido |
|---|---|
| Propietario de escritura | AG-13 Motor de Cálculo Avanzado (único; con varias instancias, escritura serializada por `calc_id`) |
| Lectores | AG-18 Orquestador, AG-19 Auditor, AG-20 Evaluador, AG-15 Documentador para el Motor, y cada solicitante sobre sus propios servicios |
| Contratos | CT-09 (Analizador, Analistas, Prospectiva, Evaluador, Orquestador, Auditor → Motor); CT-10 (Orquestador, Auditor, Evaluador → Motor); CT-20 (documentación metodológica, referenciada) |
| Herramientas | HT-01 (datos), HT-06 (caché) |

## 3. Reglas

1. **Todo servicio se registra**, sea cual sea su estado (servido, con limitaciones, aclaración pendiente, rechazado, fallido).
2. **Append-only**: un reintento o una corrección abre entrada nueva referenciada; la original conserva su estado.
3. **Idempotencia**: la misma `clave_idempotencia` devuelve el artefacto registrado (`cache_hit`) sin recalcular ni duplicar.
4. **Artefacto reproducible** suficiente para reconstruir el cálculo sin el Motor.
5. **Fechas**: todo dato de entrada con fecha de dato, fecha de recuperación y vintage; `fecha_limite_informacion` cuando el solicitante evalúa históricamente (el Motor no usa datos conocibles después de ella).
6. **Clase de cifra** (determinista o estadística) e **incertidumbre** obligatorias en resultados estadísticos.
7. **Referencia ingenua** en todo cálculo predictivo.
8. **Madurez** del método (documentado, implementado, validado; R22).
9. **Re-ejecuciones CT-10** en aislamiento, por MC-08, con comparación y tolerancia; las discrepancias no alteran la entrada original.
10. Retención de artefactos: 5 años (Anexo A).

## 4. Formato de entrada

| Campo | Tipo | Oblig. | Valores / formato |
|---|---|---|---|
| `calc_id` | Identificador | Sí | `CALC-AAAA-NNNN`; identifica también el artefacto (`artefacto_id` = `calc_id`) |
| `contrato` | Enumerado | Sí | CT-09 · CT-10 |
| `msg_id` / `run_id` · `query_id` | Texto | Sí | Trazabilidad con el solicitante |
| `solicitante` | Enumerado | Sí | AG-02 · AG-03…AG-09 · AG-10 · AG-18 · AG-19 · AG-20 (CT-09); AG-18 · AG-19 · AG-20 (CT-10) |
| `operacion` | Objeto | Sí | `{method_id, method_version, ficha_id, ficha_version, catalog_version, familia, op_sin_ficha}` |
| `perfil` | Lista | Sí | PERF-xx · TRANSVERSAL (combinados en híbridos) |
| `clase` / `horizonte` | Enumerado | Si aplica | RV…TCV (doce tipos) / H1–H5 |
| `modo` | Enumerado | Sí | SYNC_CALC · ASYNC_CALC |
| `plan` | Enumerado | Sí | PLAN_MIN · PLAN_STD · PLAN_EXT |
| `modulos` | Lista | Sí | MC-01 … MC-10 (efectivos, no previstos) |
| `prioridad` | Enumerado | Sí | INTEGRIDAD · MATERIAL · ORDEN_LLEGADA |
| `datos` | Lista | Sí | `{serie_ht01 o valor, unidad, divisa, fecha_dato, fecha_recuperacion, vintage, fuente}` |
| `fecha_limite_informacion` | Fecha-hora | Si evaluación histórica | Ningún dato posterior |
| `parametros` | Lista | Sí | `{nombre, valor, unidad}` |
| `semilla` | Entero o null | Sí | Con generador si no es null |
| `as_of` | Fecha | Sí | Corte temporal de los datos |
| `estado` | Enumerado | Sí | Sección 5 |
| `resultado` | Objeto | Si SERVED* | `{forma VALOR·TABLA·SERIE·DISTRIBUCION, payload, unidades}` |
| `clase_cifra` | Enumerado | Si SERVED* | DETERMINISTA · ESTADISTICA |
| `incertidumbre` | Objeto | Si ESTADISTICA | `{tipo IC·ERROR_ESTANDAR·CUANTILES·ESCENARIOS, valores, nivel}` |
| `referencia_ingenua` | Objeto | Si predictivo | `{tipo, valor, metrica_comparada}` |
| `artefacto` | Objeto | Sí | `{code_ref, inputs_effective, transformations, rounding_policy, data_quality_report}` |
| `verificacion_interna` | Objeto | Sí | `{identity_checks, second_path, integracion_plan}` |
| `madurez_metodo` | Enumerado | Sí | DOCUMENTADO · IMPLEMENTADO · VALIDADO |
| `clave_idempotencia` | Texto | Sí | Hash de (operación, versiones, datos, parámetros, semilla, perfil) |
| `cache_hit` | Booleano | Sí | Respuesta servida desde caché |
| `consumo_uc` | Número | Sí | — |
| `tiempos` | Objeto | Sí | `{recibido, iniciado, completado}` ISO 8601 |
| `limitaciones` / `incidencias` | Listas | Sí | «ninguna» solo con motivo |
| `motivo_rechazo` | Texto | Si REJECTED · CLARIFICATION_NEEDED · FAILED | — |
| `reejecucion` | Objeto | Si CT-10 | `{calc_original, motivo, aislamiento CONFIRMADO, tolerancia, coincide SI·NO·DENTRO_TOLERANCIA, diferencias, categoria DATOS_DISTINTOS·CONVENCION_DISTINTA·ERROR_ORIGINAL·ERROR_REEJECUCION·NO_DETERMINISMO, diagnostico, audit_ref}` |
| `consumido_por` | Lista | No | RUN-, OPP-, PRG-, CERT-, AJU-, HAL- (añadido por referencias posteriores) |

## 5. Estados y transiciones

`RECIBIDO` → `SERVED` · `SERVED_WITH_LIMITATIONS` · `CLARIFICATION_NEEDED` · `REJECTED` · `FAILED`. Los estados finales son cerrados: una aclaración respondida o un reintento abre una entrada nueva con `reintento_de`. G3 solo acepta cifras de entradas `SERVED` o `SERVED_WITH_LIMITATIONS` (con la limitación declarada en el entregable).

## 6. Índices de consulta

| Índice | Clave | Uso |
|---|---|---|
| Idempotencia | `clave_idempotencia` | Reutilización antes de calcular |
| Por ejecución | `run_id`, `query_id` | G3-DAT-07; auditoría |
| Por método | `method_id`, `method_version`, `madurez_metodo` | G3-MET-13; DOC-M |
| Por perfil y clase | `perfil`, `clase` | G3-MET-12 |
| Re-ejecuciones | `contrato` = CT-10, `reejecucion.coincide` | Orquestador, Auditor, Evaluador |
| Por consumidor | `consumido_por` | Propagación de correcciones |
| Rechazos y fallos | `estado` | Salud del Motor |

## 7. Ejemplo ficticio

> **EJEMPLO FICTICIO — no es una entrada real.**

```json
{"calc_id":"CALC-2026-0013","contrato":"CT-09","msg_id":"MSG-2026-11-07-0412","run_id":"RUN-2026-0001","solicitante":"AG-10",
 "operacion":{"method_id":"MET-TASA-BASE-REL","method_version":"1.0","ficha_id":"FX-MC10-003","ficha_version":"1.0","catalog_version":"4.0","familia":"evaluación predictiva","op_sin_ficha":false},
 "perfil":["PERF-ACC"],"clase":"RV","horizonte":"H3","modo":"SYNC_CALC","plan":"PLAN_MIN","modulos":["MC-10"],"prioridad":"MATERIAL",
 "datos":[{"serie_ht01":"IDX-FICT-001","unidad":"índice","divisa":"EUR","fecha_dato":"2026-11-06","fecha_recuperacion":"2026-11-07T07:50:00+01:00","vintage":"2026-11-06","fuente":"HT-01"}],
 "fecha_limite_informacion":"2026-11-06T23:59:59+01:00","parametros":[{"nombre":"ventana","valor":20,"unidad":"años"},{"nombre":"horizonte","valor":26,"unidad":"semanas"}],
 "semilla":null,"as_of":"2026-11-06","estado":"SERVED","resultado":{"forma":"VALOR","payload":{"tasa_base":0.47},"unidades":{"tasa_base":"proporción"}},
 "clase_cifra":"ESTADISTICA","incertidumbre":{"tipo":"IC","valores":[0.41,0.53],"nivel":0.90},"referencia_ingenua":null,
 "artefacto":{"code_ref":"ficticio","inputs_effective":"…","transformations":"rentabilidades totales solapadas a 26 semanas","rounding_policy":"2 decimales","data_quality_report":"sin huecos"},
 "verificacion_interna":{"identity_checks":["recuento de ventanas"],"second_path":"cálculo con ventanas no solapadas: 0,46"},"madurez_metodo":"IMPLEMENTADO",
 "clave_idempotencia":"9c1e…(ficticia)","cache_hit":false,"consumo_uc":0.3,"limitaciones":["ventanas solapadas: IC por bloques"],"incidencias":[]}
```
