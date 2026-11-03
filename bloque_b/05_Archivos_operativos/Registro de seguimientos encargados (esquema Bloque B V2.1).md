# Esquema de archivo operativo — F11 Registro de seguimientos encargados

**Bloque B · Robot Investor · Versión óptima V2.1 · 03/11/2026** · Subordinado al Documento 0 del Bloque B óptima V2.1 (R5, R28, R32, R35, 4.3, 5.1, 7.13, 14.8, 15; Anexos A, B.13 y B.14). Ante discrepancia, manda el Documento 0.

> **Convención de citas (0.5).** «Archivo F11» designa este registro; «fase F11» designa la ronda del **Vigía**. Son cosas distintas: el Vigía es automático, compara señales con umbrales sobre las REC-B entregadas y solo emite alertas (R32); el seguimiento encargado lo pide el Broker por CT-B-29, ejecuta ciclos ligeros N1-SEG y entrega un informe de seguimiento con semáforo y recomendación.

---

## 1. Propósito

El archivo F11 es la **memoria de los seguimientos que el Broker encarga** (7.13): cada encargo SEG-B con su objeto, su frecuencia, su motivo, las señales que interesan al Broker, sus disparadores, su fecha de fin y su historial de altas, modificaciones, pausas, reanudaciones y cancelaciones; y cada **ciclo** CIC-B con su fecha de corte, su tiempo y su consumo, su semáforo, su recomendación, la ruta del informe de seguimiento y la decisión posterior del Broker.

Es la base de: (a) la programación de los ciclos en HT-05 (que solo programa lo que el Broker ha encargado, R5 y R35); (b) la orden `CICLO_SEGUIMIENTO` del Coordinador al Director (CT-B-08); (c) las respuestas N0 sobre «qué estáis siguiendo»; (d) la consulta del Director en F0 de una petición sobre el mismo ámbito (seguimientos activos y último semáforo); (e) las métricas del Evaluador sobre seguimientos (acierto del semáforo, utilidad de las recomendaciones, coste por ciclo, ciclos sin novedad; 12.7).

## 2. Propietario, lectores y contratos

| Aspecto | Contenido |
|---|---|
| Propietario de escritura | **AG-B01 Coordinador de Peticiones y Consultas** (único; escrituras serializadas) |
| Lectores | AG-B02 Director (encargo, último ciclo, último informe), AG-B23 Evaluador (métricas y lecciones), AG-B21 Orquestador (G3 perfil CIC, escalado), AG-B22 Auditor (muestreo 20 %), AG-B17 Redactor (extracto del encargo), HT-05 (programación), AG-B18, AG-B19 y AG-B20 (agenda de vigilancia) |
| Contratos | **CT-B-29** (encargo del Broker y acuse; entrega de cada informe de seguimiento), CT-B-08 (`CICLO_SEGUIMIENTO`, `APORTE_BROKER` con `seg_id`), CT-B-20 (`CICLO`), CT-B-26 (eventos de seguimiento al Evaluador), CT-B-28 (consulta del ciclo al Broker, máximo una por ciclo) |
| Registros relacionados | F1 (RUN-B del ciclo, consumo, CNS-B), F3 (REC-B: campo `seguimientos` con los SEG-B activos), F6 (versión de la ficha MKT-B actualizada por el ciclo), HA (G3V-B perfil CIC, AUD-B, AUTS-B), ENT (`Informes de seguimiento/`) |

## 3. Reglas

1. **Solo por encargo del Broker** (R5, R35). Ningún agente da de alta un seguimiento por iniciativa propia; el Director puede **sugerirlo** en un informe de parada (`PONER_EN_SEGUIMIENTO`) o en un veredicto VIGILAR, pero el alta exige un CT-B-29 del Broker.
2. **Append-only** (R28). Toda alta, modificación, pausa, reanudación, cancelación, ciclo, omisión y decisión es una entrada nueva; el estado vigente de un SEG-B es el de su última entrada.
3. **Cancelación inmediata.** El Broker cancela en cualquier momento; un ciclo en curso se cierra en su siguiente punto de control **sin informe**.
4. **Validación del encargo** (7.13): admisibilidad como en F0 (sin datos personales ni claves, R10 y R11; si llegan, el mensaje se rechaza íntegro); frecuencia ∈ {`DIARIA`, `SEMANAL`, `QUINCENAL`, `MENSUAL`, `TRIMESTRAL`, `PERSONALIZADA` con `cada_dias` ≥ 1}; una frecuencia mayor que la del Vigía para el horizonte principal se acepta **con advertencia**.
5. **Límites** (Anexo A): máximo **25** seguimientos activos; ciclo con objetivo **< 10 min** y PT30 aplicable (si la estimación supera 30 min se pide autorización por CT-B-05); presupuesto ≈ **5 UC** por ciclo; línea base de un ámbito nuevo ≤ 20 min; sin fecha de fin, recordatorio de revisión al Broker cada **6 meses**; un seguimiento pausado más de 6 meses recibe recordatorio trimestral; como máximo **una** consulta al Broker por ciclo.
6. **Sin solape.** Un ciclo que coincide con el anterior aún en curso se omite y se registra (`CICLO_OMITIDO_SOLAPE`).
7. **Ámbito nuevo.** Sin ficha F6, el primer ciclo es una **línea base** (capas 0 y 1 con las señales y disparadores que se vigilarán); un análisis completo exige una petición CT-B-01.
8. **Nunca inicia un análisis profundo.** La recomendación `REACTIVAR_ANALISIS_PROFUNDO` propone una petición (nivel, alcance, estimación); el Broker decide.
9. **Biblioteca.** Tras la entrega del ciclo, el Director actualiza F6 con lo verificado; el ciclo registra la versión resultante.
10. **Coordinación con el Vigía.** El ciclo incorpora las alertas ALR-B del periodo (`alertas_vigia_incluidas`); el Vigía no duplica avisos ya incluidos en un informe de seguimiento.
11. **Identificadores.** `SEG-B-AAAA-NNNN` (encargo) y `CIC-B-AAAA-NNNN-NN` (ciclo; los cuatro dígitos centrales son los del SEG-B y los dos finales, el número de ciclo). La ejecución del ciclo es un RUN-B en F1; el ejecutor de referencia usa `RUN-B-AAAA-NNNN-cNN`.
12. **Retención:** indefinida (Anexo A).

## 4. Formato de entrada

Cada línea es un objeto JSON con `tipo_entrada` ∈ {`SEG`, `CIC`, `DEC`} y los campos comunes `id`, `timestamp`, `agente` (AG-B01) y `fecha_corte`.

### 4.1 Encargo de seguimiento (SEG-B)

| Campo | Tipo | Contenido |
|---|---|---|
| `id` | texto | SEG-B-AAAA-NNNN |
| `accion` | enumerado | `ALTA` · `MODIFICACION` · `PAUSA` · `REANUDACION` · `CANCELACION` (B.13) |
| `estado` | enumerado | `ACTIVO` · `PAUSADO` · `CANCELADO` · `FINALIZADO` (o `RECHAZADO` en el acuse, sin alta) |
| `objeto` | objeto | `tipo` (`AMBITO_ANALIZADO` · `AMBITO_NUEVO`), `rec_id`, `mkt_id`, `ambito` {descripcion, incluye, excluye, region}, `tipo_objeto_sugerido` |
| `clave_universo` | texto | Clave del ámbito resuelta por el Coordinador |
| `frecuencia` | objeto | `tipo`, `cada_dias` (PERSONALIZADA), `dia_preferente` |
| `motivo` | texto | Por qué lo encarga el Broker |
| `senales_de_interes` | lista | Señales que interesan al Broker |
| `disparadores_broker` | lista | {descripcion, umbral} |
| `dimensiones_clave` | lista | D1…D12 (por defecto, las líderes de la matriz del ámbito) |
| `candidatos_a_vigilar` | lista | CAND-B entregados que el Broker quiere seguir |
| `horizonte_principal` | enumerado | H1…H5 |
| `fecha_fin` | fecha o nulo | Sin fecha: recordatorio de revisión cada 6 meses |
| `limite_ciclo` | objeto | {minutos (10), uc} |
| `proximo_ciclo` | fecha | Programado en HT-05 |
| `estimacion_ciclo` | objeto | {minutos_p50, minutos_p80, uc_p80} (modelo de tiempos de F5) |
| `linea_base` | objeto | {necesaria, minutos_p80} |
| `advertencias` | lista | p. ej., «frecuencia superior a la del Vigía para el horizonte principal» |
| `ciclos` | entero | Ciclos entregados hasta la fecha |
| `pausado_desde` | fecha | Solo en PAUSA |

### 4.2 Ciclo (CIC-B)

| Campo | Tipo | Contenido |
|---|---|---|
| `id` | texto | CIC-B-AAAA-NNNN-NN |
| `seg_id`, `run_id` | texto | Encargo y ejecución (F1) |
| `estado` | enumerado | `EN_CURSO` · `ENTREGADO` · `CICLO_OMITIDO_SOLAPE` · `CERRADO_SIN_INFORME` (cancelación) · `BLOQUEADO` (G3 o auditoría) |
| `linea_base` | booleano | Primer ciclo de un ámbito nuevo |
| `data_cutoff` | fecha | Fecha de corte del ciclo |
| `semaforo` | enumerado | `VERDE` · `AMBAR` · `ROJO` (con autorrefutación del cambio de color) |
| `recomendacion` | enumerado | `MANTENER_VIGILANCIA` · `REACTIVAR_ANALISIS_PROFUNDO` · `PROPONER_PASAR_A_C` · `CANCELAR_SEGUIMIENTO` |
| `motivo` | texto | De la recomendación |
| `peticion_sugerida` | objeto o nulo | {nivel, alcance, estimacion_min_p80} si se recomienda reactivar |
| `alertas_vigia_incluidas` | lista | ALR-B del periodo |
| `actualizacion_F6` | objeto | {mkt_id, version, dimensiones} |
| `consultas` | lista | CNS-B del ciclo (máximo una) |
| `tiempo_consumo` | objeto | {minutos, uc} |
| `g3`, `auditoria`, `auts_id` | objeto / texto | Dictamen G3 (perfil CIC), muestreo de auditoría y autorización de salida |
| `informe` | objeto | Rutas `markdown` y `json` del informe de seguimiento (`AAAA-MM-DD_informe-seguimiento_SEG-B-id_cNN`) |

### 4.3 Decisión posterior del Broker (DEC)

`seg_id`, `ciclo_id`, `decision` (`MANTENER` · `REACTIVAR_PETICION` con PET-B · `PASAR_A_C` con CAND-B · `CANCELAR` · `SIN_DECISION`), `motivo`, `timestamp`. Alimenta las métricas de utilidad de las recomendaciones (12.7).

### 4.4 Recordatorios

`RECORDATORIO_REVISION` (sin fecha de fin, cada 6 meses) y `RECORDATORIO_PAUSA` (pausado > 6 meses, trimestral). Se derivan del estado vigente (no cambian el estado del SEG-B); el Coordinador los transmite al Broker y registra el envío en F1. En el ejecutor de referencia aparecen en `bloque-b seguimiento listar` (campo `recordatorios`) y la decisión posterior se registra con `bloque-b decision` (`decision_seguimiento`).

## 5. Estados y transiciones

| De | A | Disparador |
|---|---|---|
| — | `ACTIVO` | ALTA válida (acuse CT-B-29 con `proximo_ciclo` y estimación) |
| — | `RECHAZADO` | Encargo inadmisible (datos sensibles, frecuencia inválida, límite de 25 activos) |
| `ACTIVO` | `PAUSADO` | PAUSA del Broker (no se programan ciclos) |
| `PAUSADO` | `ACTIVO` | REANUDACION (nuevo `proximo_ciclo`) |
| `ACTIVO` / `PAUSADO` | `CANCELADO` | CANCELACION (inmediata) o recomendación `CANCELAR_SEGUIMIENTO` aceptada por el Broker |
| `ACTIVO` | `FINALIZADO` | Llega `fecha_fin` |

Ciclo: `EN_CURSO` → `ENTREGADO` (o `BLOQUEADO`, `CERRADO_SIN_INFORME`); `CICLO_OMITIDO_SOLAPE` se registra sin ejecución.

## 6. Índices de consulta

| Índice | Uso |
|---|---|
| `seg_id` → última entrada | Estado vigente del encargo |
| `estado = ACTIVO` y `proximo_ciclo ≤ hoy` | Ciclos pendientes (HT-05; comando `seguimiento pendientes`) |
| `objeto.rec_id` / `clave_universo` | Seguimientos activos de un ámbito (F0 del Director; campo `seguimientos` de la REC-B) |
| `seg_id` → CIC-B ordenados | Último ciclo, delta frente al anterior, serie de semáforos |
| `recomendacion` × `decision` | Métricas del Evaluador (utilidad, ciclos sin novedad, coste por ciclo) |

## 7. Ejemplo ficticio

```json
{"tipo_entrada":"SEG","id":"SEG-B-2026-0001","timestamp":"2026-11-03T10:12:00+01:00","agente":"AG-B01","fecha_corte":"2026-11-03",
 "accion":"ALTA","estado":"ACTIVO","objeto":{"tipo":"AMBITO_ANALIZADO","rec_id":"REC-B-2026-0001","mkt_id":"MKT-B-2026-0001"},
 "clave_universo":"redes_electricas_europa","frecuencia":{"tipo":"MENSUAL"},
 "motivo":"Vigilar la cartera de pedidos y la valoración del ámbito (ejemplo ficticio)",
 "senales_de_interes":["book-to-bill de los fabricantes de cable","valoración relativa del ámbito"],
 "disparadores_broker":[{"descripcion":"book-to-bill inferior a 1 durante dos trimestres","umbral":"1,0"}],
 "dimensiones_clave":["D3","D9"],"candidatos_a_vigilar":[],"horizonte_principal":"H4","fecha_fin":"2027-11-03",
 "limite_ciclo":{"minutos":10},"proximo_ciclo":"2026-12-03","estimacion_ciclo":{"minutos_p50":6.0,"minutos_p80":9.0,"uc_p80":5.0},
 "linea_base":{"necesaria":false,"minutos_p80":null},"advertencias":[],"ciclos":0}
{"tipo_entrada":"CIC","id":"CIC-B-2026-0001-01","timestamp":"2026-12-03T09:40:00+01:00","agente":"AG-B01","fecha_corte":"2026-12-03",
 "seg_id":"SEG-B-2026-0001","run_id":"RUN-B-2026-0001-c01","estado":"ENTREGADO","linea_base":false,"data_cutoff":"2026-12-03",
 "semaforo":"VERDE","recomendacion":"MANTENER_VIGILANCIA","motivo":"Sin cambio material desde la entrega",
 "peticion_sugerida":null,"alertas_vigia_incluidas":[],"actualizacion_F6":{"mkt_id":"MKT-B-2026-0001","version":"c01","dimensiones":["D3","D9"]},
 "consultas":[],"tiempo_consumo":{"minutos":5.8,"uc":2.9},"g3":{"dictamen":"APTO","perfil":"CIC"},"auts_id":"AUTS-B-2026-0007",
 "informe":{"markdown":"ENT/Informes de seguimiento/2026-12-03_informe-seguimiento_SEG-B-2026-0001_c01.md",
            "json":"ENT/Informes de seguimiento/2026-12-03_informe-seguimiento_SEG-B-2026-0001_c01.json"}}
{"tipo_entrada":"DEC","id":"DEC-SEG-B-2026-0001-01","timestamp":"2026-12-04T08:00:00+01:00","agente":"AG-B01","fecha_corte":"2026-12-03",
 "seg_id":"SEG-B-2026-0001","ciclo_id":"CIC-B-2026-0001-01","decision":"MANTENER","motivo":"Ejemplo ficticio"}
```
