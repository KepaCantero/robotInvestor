# Esquema de archivo operativo — RC Registro de cálculos del Motor

**Bloque B · Robot Investor · Versión óptima V2.0 · 03/11/2026** · Subordinado al Documento 0 del Bloque B óptima V2.0 (ante discrepancia, manda el Documento 0).

---

## 1. Propósito

El Registro de cálculos (RC) conserva cada servicio del **Motor de Cálculo Avanzado de Mercados** (AG-B16): cálculos (CT-B-13), re-ejecuciones independientes (CT-B-14), rechazos y fallos, cada uno con su **artefacto reproducible** (método, versión, perfil PERF-B- o SEL-, plan MIN/STD/EXT, módulos MC-B01…MC-B10 usados, datos con fecha y «conocible desde», parámetros, semilla, fecha de corte, transformaciones y código). Es la fuente de toda cifra que el Bloque B entrega (R9: «toda cifra entregada procede de un artefacto reproducible del Motor o de un dato con fuente y fecha»), la base de la reutilización por caché (10.2), de las puertas PA7 y PC7, de la reconstrucción de S y de los universos cribados que sirven de referencia a los rankings. Incluye la sección **«Incidencias y propuestas»** del Motor (5.1).

## 2. Propietario, lectores y contratos

| Aspecto | Contenido |
|---|---|
| Propietario de escritura | AG-B16 Motor (único; sin estado y con varias instancias, escritura serializada por `calc_id`) |
| Lectores | AG-B21 Orquestador, AG-B22 Auditor, AG-B23 Evaluador, AG-B19 Documentador para el Motor, AG-B01 (respuestas N0 de método y cifra) y cada solicitante sobre sus propios servicios (matriz 5.1) |
| Contratos | CT-B-13 (DIR, ESP, SEL, PROS, CONTRA, EVAL, ORQ, AUD, DOC, BFA → Motor); CT-B-14 (ORQ, AUD, EVAL → Motor); CT-B-23 (documentación metodológica, referenciada) |
| Herramientas | HT-01 (datos), HT-06 (caché), HT-03 (cuando el cálculo produce puntuaciones: S, A, E, C) |
| Archivo relacionado | CC (Catálogo, perfiles y mapa del Motor): fichas de método, perfiles PERF-B y SEL; el Motor solo propone cambios (tipo 3) |

## 3. Reglas

1. **Todo servicio se registra**, sea cual sea su estado.
2. **Append-only**: un reintento o una corrección abre entrada nueva con `reintento_de` o `supersedes`; la original conserva su estado.
3. **Caché por idempotencia** (10.2): mismo método, versión, insumos y fecha de corte → se devuelve el artefacto registrado (`cache_hit = true`) sin recalcular.
4. **Artefacto suficiente** para que un tercero reconstruya el cálculo sin el Motor (14.5: el anexo de datos indexa estos artefactos).
5. **Fecha de corte** (6.2.9): en evaluación, backtesting y vigilancia, ningún dato con `conocible_desde` posterior; el Motor rechaza (`FUGA_DE_INFORMACION`) cualquier insumo posterior.
6. **Clase de cifra** e **incertidumbre** obligatorias en los resultados estadísticos (8.8).
7. **Referencia ingenua** en todo cálculo predictivo y en todo ranking (9.11; MC-B10).
8. **Saneo de resultados** antes de servir (8.8.5): consistencia entre cálculos relacionados, extremos investigados, fuga comprobada; se anota en `verificacion_interna`.
9. **No interpreta**: el Motor calcula, declara supuestos e incertidumbre; nunca emite conclusiones de inversión ni precios objetivo (4.2; frontera con C).
10. **Madurez** del método declarada (documentado · implementado · validado, R26).
11. **Universos**: el cribado y el ranking (MC-B07) guardan el universo completo con todas sus métricas, componentes, S, IC, rango y motivo de exclusión (hoja de universo del anexo de datos).
12. **Re-ejecución CT-B-14** en aislamiento, con comparación y tolerancia; las discrepancias no alteran la entrada original.
13. Retención de artefactos: 5 años (Anexo A).
14. Sin claves: los conectores se citan por alias (`credencial_ref`), nunca la clave (R10).

## 4. Formato de entrada

| Campo | Tipo | Oblig. | Valores / formato |
|---|---|---|---|
| `calc_id` | Identificador | Sí | `CALC-B-AAAA-NNNN` (= identificador del artefacto) |
| `contrato` | Enumerado | Sí | CT-B-13 · CT-B-14 |
| `msg_id` / `pet_id` · `run_id` · `query_id` | Texto | Sí | Trazabilidad (tareas de fondo: `pet_id` = null y `tarea` = VIGIA·EVALUACION·CONOCIMIENTO) |
| `solicitante` | Enumerado | Sí | AG-B02…AG-B15, AG-B18, AG-B19, AG-B20, AG-B21, AG-B22, AG-B23 (según contrato) |
| `metodo` | Objeto | Sí | `{method_id, method_version, ficha_CC, catalog_version, op_sin_ficha}` |
| `perfil` | Lista | Sí | PERF-B-SECT · PERF-B-TEMA · PERF-B-GEO · PERF-B-SEGM · PERF-B-FACT · PERF-B-CADENA · SEL-RV … SEL-TCV · TRANSVERSAL |
| `modulos` | Lista | Sí | MC-B01 … MC-B10 efectivamente usados |
| `plan_calculo` | Enumerado | Sí | MIN · STD · EXT |
| `modo` | Enumerado | Sí | SINCRONO · ASINCRONO |
| `dimension` / `tipo_activo` / `horizonte` | Enumerados | Si aplica | D1…D12 · SELECCION / doce códigos / H1–H4 |
| `valor_informativo` | Texto | Sí | Qué conclusión puede cambiar (10.4) o «contexto» declarado |
| `datos` | Lista | Sí | `{serie_ht01 o dat_id, unidad, divisa, fecha_dato, fecha_recuperacion, conocible_desde, vintage, conector (alias)}` |
| `fecha_corte` | Fecha | Sí | Corte temporal de los datos |
| `parametros` | Lista | Sí | `{nombre, valor, unidad}` |
| `semilla` | Entero o null | Sí | Con generador si no es null |
| `estado` | Enumerado | Sí | Sección 5 |
| `resultado` | Objeto | Si SERVIDO | `{forma VALOR·TABLA·SERIE·DISTRIBUCION·RANKING·UNIVERSO, payload, unidades}` |
| `clase_cifra` | Enumerado | Si SERVIDO | determinista · estimacion_estadistica |
| `incertidumbre` | Objeto | Si estadística | `{tipo IC·ERROR_ESTANDAR·CUANTILES·ESCENARIOS·IC_RANGO, valores, nivel}` |
| `referencia_ingenua` | Objeto | Si predictivo o ranking | `{tipo, valor, metrica_comparada}` |
| `ranking` | Objeto | Si MC-B07 | `{universo_tamano, normalizacion (winsorización 2,5–97,5 y percentiles por subgrupo), pesos (cfg_id), S [{instrumento, S, desglose, ic90_S, rango, ic90_rango, frontera}], perturbacion_pesos ±5, replicas_bootstrap, duplicacion (correlación y solapamiento)}` |
| `artefacto` | Objeto | Sí | `{code_ref, inputs_effective, transformations, rounding_policy, data_quality_report}` |
| `verificacion_interna` | Objeto | Sí | `{identity_checks, second_path, saneo (consistencia, extremos, fuga)}` |
| `madurez_metodo` | Enumerado | Sí | DOCUMENTADO · IMPLEMENTADO · VALIDADO |
| `clave_cache` | Texto | Sí | Hash de (método, versiones, insumos, parámetros, semilla, perfil, fecha de corte) |
| `cache_hit` | Booleano | Sí | — |
| `consumo_uc` / `tiempos` | Número / objeto | Sí | `{recibido, iniciado, completado}` |
| `limitaciones` / `incidencias` | Listas | Sí | «ninguna» solo con motivo |
| `motivo_rechazo` | Texto | Si RECHAZADO · ACLARACION_NECESARIA · FALLIDO | METODO_NO_IMPLEMENTADO · DATOS_INSUFICIENTES · FUGA_DE_INFORMACION · PERFIL_INCOHERENTE · otro |
| `reejecucion` | Objeto | Si CT-B-14 | `{calc_original, motivo, aislamiento CONFIRMADO, tolerancia, coincide SI·NO·DENTRO_TOLERANCIA, diferencias, categoria DATOS_DISTINTOS·CONVENCION_DISTINTA·ERROR_ORIGINAL·ERROR_REEJECUCION·NO_DETERMINISMO, diagnostico}` |
| `consumido_por` | Lista | No | CLM-B, REC-B, CAND-B, PRG-B, CERT-B, AJU-B, HAL-B (añadido por referencias posteriores) |

**Sección «Incidencias y propuestas»**: `{fecha, tipo METODO_FALTANTE·FICHA_INCOMPLETA·DATO_INCONSISTENTE·PROPUESTA_CC, descripcion, calc_ids, propuesta (tipo 1, 2 o 3), estado}`; el Documentador para el Motor la lee (CT-B-23) y el Orquestador la recoge en HA.

## 5. Estados y transiciones

`RECIBIDO` → `SERVIDO` · `SERVIDO_CON_LIMITACIONES` · `ACLARACION_NECESARIA` · `RECHAZADO` · `FALLIDO`. Los estados finales son cerrados; una aclaración respondida o un reintento abre entrada nueva. G3 solo acepta cifras de entradas `SERVIDO` o `SERVIDO_CON_LIMITACIONES` (con la limitación declarada en el entregable).

## 6. Índices de consulta

| Índice | Clave | Uso |
|---|---|---|
| Caché | `clave_cache` | Reutilización antes de calcular |
| Por petición | `pet_id`, `run_id` | G3 (artefactos presentes); auditoría; anexo de datos |
| Por método y madurez | `method_id`, `madurez_metodo` | Estados de madurez (R26); Documentador para el Motor |
| Por perfil y tipo | `perfil`, `tipo_activo` | Coherencia perfil–objeto y playbook–tipo |
| Universos y rankings | `resultado.forma` = UNIVERSO · RANKING | Referencias de ranking; evaluación sin supervivencia |
| Re-ejecuciones | `contrato` = CT-B-14, `coincide` | Orquestador, Auditor, Evaluador |
| Por consumidor | `consumido_por` | Propagación de correcciones |
| Rechazos y fallos | `estado` | Salud del Motor; tipo 3 |

## 7. Ejemplo ficticio

> **EJEMPLO FICTICIO — no es una entrada real.**

```json
{"calc_id":"CALC-B-2026-0140","contrato":"CT-B-13","msg_id":"MSG-B-2026-11-10-0377","pet_id":"PET-B-2026-0007","run_id":"RUN-B-2026-0007-01","solicitante":"AG-B12",
 "metodo":{"method_id":"SEL-S-RANK","method_version":"2.0","ficha_CC":"FCC-MCB07-004","catalog_version":"2.0","op_sin_ficha":false},
 "perfil":["SEL-RV"],"modulos":["MC-B07","MC-B06"],"plan_calculo":"STD","modo":"SINCRONO","dimension":"SELECCION","tipo_activo":"RV","horizonte":"H3",
 "valor_informativo":"Fija el top-5 RV y los PRIORITARIO_PARA_C","datos":[{"dat_id":"DAT-B-2026-0031","fecha_corte":"2026-11-07"}],"fecha_corte":"2026-11-07",
 "parametros":[{"nombre":"winsorizacion","valor":"2,5–97,5","unidad":"percentil"},{"nombre":"replicas_bootstrap","valor":2000,"unidad":"n"}],"semilla":20261110,
 "estado":"SERVIDO","resultado":{"forma":"RANKING","payload":"…","unidades":{"S":"0–100"}},"clase_cifra":"estimacion_estadistica",
 "incertidumbre":{"tipo":"IC_RANGO","valores":"por candidato","nivel":0.90},"referencia_ingenua":{"tipo":"RANKING_ALEATORIO","valor":"IC de rango esperado 0","metrica_comparada":"Spearman"},
 "artefacto":{"code_ref":"ficticio","inputs_effective":"53 emisores tras PC1–PC4","transformations":"percentiles por subindustria","rounding_policy":"S entero","data_quality_report":"2 NE en MO"},
 "verificacion_interna":{"identity_checks":["suma de pesos = 100"],"second_path":"S recalculado con HT-03: idéntico","saneo":"sin extremos; fuga comprobada"},
 "madurez_metodo":"IMPLEMENTADO","clave_cache":"b7e2…(ficticia)","cache_hit":false,"consumo_uc":1.2,"limitaciones":["pureza estimada en 6 emisores sin segmentos publicados"],"incidencias":[]}
```
