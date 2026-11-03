# Esquema de archivo operativo — F11 Registro de seguimientos encargados

**Bloque A · Robot Investor · Esquema V1.0 · nuevo en V5.1 (03/11/2026)** · Subordinado al Documento 0 óptima V5.1 (secciones 5.1, 6.1 CT-24, 7.1 C6, 7.11, 14.4, 15, R5 y R27; Anexo A y Anexo B).

---

## 1. Propósito

F11 registra los **encargos de seguimiento de opción** que el Broker Personal hace por **CT-24** sobre una OPP- que decidió no enviar al Bloque B pero quiere vigilar, su historial de altas, modificaciones, pausas, reanudaciones y cancelaciones, y una línea por cada **ciclo de seguimiento encargado (C6)** con su semáforo, su recomendación, la ruta del informe de seguimiento de opción y la respuesta del Broker. Es la agenda de la que el Planificador (HT-05) toma la frecuencia de cada encargo activo.

**No es**: el seguimiento de las opciones vigentes del top-3 dentro del ciclo C1 (ese continúa como está, 9.6.4 y 14.1); ni un registro de oportunidades (la ficha de la OPP- sigue en F3, que solo anota `decision_broker = EN_SEGUIMIENTO` y el `seg_id`); ni un archivo de pronósticos (los PRG- abiertos y sus hitos siguen en F4). El bloque **nunca** abre un seguimiento por iniciativa propia (R27).

## 2. Propietario, lectores y contratos

| Aspecto | Contenido |
|---|---|
| Propietario de escritura | **AG-01 Coordinador de Peticiones y Consultas** (único) |
| Lectores | AG-02 Analizador, Analistas de tipo de activo (AG-03…AG-09, AG-21…AG-25), AG-17 Redactor, AG-18 Orquestador, AG-19 Auditor, AG-20 Evaluador; HT-05 (programación) |
| Contratos que lo alimentan | CT-24 (alta, modificación, pausa, reanudación, cancelación; acuse e informes de cada ciclo), CT-05 de tipo `SEGUIMIENTO` (orden y retorno de cada ciclo), CT-22 `DECISION_SEGUIMIENTO` (aviso al Evaluador) |
| Herramientas | HT-05 (programación de los ciclos C6 según la frecuencia), HT-09 (validación del informe de seguimiento de opción), HT-06 (índice) |

## 3. Reglas

1. **Append-only en lo sustantivo** (5.2): cada acción del Broker y cada ciclo es una entrada nueva; el estado vigente de un encargo es la consolidación de sus entradas. Nada se borra.
2. **Admisión** (7.11.2): se admite cualquier OPP- registrada en F3, haya estado o no en un top-3. Ningún encargo se rechaza por número (R5). Si la frecuencia es más corta que la orientativa para el horizonte principal de la opción (P-39 de F10: H1 diaria · H2 diaria o semanal · H3 semanal a mensual · H4 mensual o trimestral · H5 trimestral), se acepta y se avisa al Broker de que los ciclos sin cambio material serán «sin novedad».
3. **Cancelación inmediata** (R27): la cancelación surte efecto en el acto; se anulan los ciclos programados y un ciclo en curso se detiene en su siguiente punto de control.
4. **Prioridad**: los ciclos C6 se encolan con prioridad inferior a C1–C3 y nunca retrasan sus entregas; presupuesto por ciclo: 2 UC, hasta 5 UC si el delta es material, ≤ 0,5 UC si «sin novedad» (P-40 de F10).
5. **Absorción en C1** (7.11.5): mientras la OPP- sea `VIGENTE` en el top-3, los ciclos C6 coincidentes se omiten con una entrada `CICLO_OMITIDO` («cubierto en C1»).
6. **Fin**: al llegar `fecha_fin`, el encargo pasa a `FINALIZADO` y se avisa al Broker. Si la OPP- pasa a `CERRADA`, el Coordinador propone la cancelación.
7. **Una sola recomendación por ciclo** (7.11.4): `MANTENER_VIGILANCIA`, `PROPONER_ENVIO_A_B` (solo si la opción vuelve a ser elegible según 9.2 con las puntuaciones actualizadas y sin objeciones fuertes abiertas), `CERRAR` o `PROPONER_CANCELACION`. La decisión es siempre del Broker (R4).
8. **Sin datos personales ni credenciales.** Conservación indefinida (como F1–F6).

## 4. Formato de entrada

### 4.1 Encargo (entrada `ALTA`)

| Campo | Tipo | Oblig. | Valores / formato | Descripción |
|---|---|---|---|---|
| `seg_id` | Identificador | Sí | `SEG-AAAA-NNNN` | Clave |
| `opp_id` | Identificador | Sí | OPP- de F3 | Opción vigilada |
| `clase` | Enumerado | Sí | Uno de los doce tipos de activo | Tipo de la OPP- |
| `frecuencia` | Enumerado | Sí | DIARIA · SEMANAL (por defecto) · QUINCENAL · MENSUAL · TRIMESTRAL · PERSONALIZADA | A elección del Broker |
| `calendario_personalizado` | Objeto o null | Si PERSONALIZADA | `{cada_dias}` o expresión cron con zona IANA | — |
| `motivo` | Texto | Sí | — | Por qué el Broker quiere vigilarla |
| `senales_interes` | Lista | No | Textos | Señales que interesan al Broker |
| `fecha_fin` | Fecha o null | No | ISO 8601 | Fin opcional del encargo |
| `estado` | Enumerado | Sí | ACTIVO al alta | 5 |
| `fecha_alta` / `msg_id` | Fecha / texto | Sí | — | Trazabilidad del CT-24 |
| `proximo_ciclo` | Fecha o null | Sí | ISO 8601 | Programado en HT-05 |
| `aviso` | Texto o null | No | — | Aviso de frecuencia corta (regla 2) |

### 4.2 Acciones posteriores (`MODIFICACION`, `PAUSA`, `REANUDACION`, `CANCELACION`, `FIN`)

`seg_id`, `tipo_entrada`, campos modificados (en MODIFICACION: `frecuencia`, `calendario_personalizado`, `motivo`, `senales_interes`, `fecha_fin`), `estado` resultante, `proximo_ciclo`, `fecha_cancelacion` (en CANCELACION), `msg_id` del CT-24.

### 4.3 Ciclo C6 (entrada `CICLO` o `CICLO_OMITIDO`)

| Campo | Tipo | Oblig. | Valores / formato |
|---|---|---|---|
| `seg_id` | Identificador | Sí | SEG- |
| `ciclo` | Objeto | Sí | `{n, run_id, fecha, semaforo VERDE·AMBAR·ROJO, recomendacion, ruta, g3 APTO·APTO_CON_ADVERTENCIAS·BLOQUEADO, entregado}` |
| `ciclos` | Entero | Sí | Número de ciclos ejecutados |
| `ultimo_run_id` / `ultima_fecha` / `ultima_recomendacion` / `ultimo_semaforo` / `ultimo_RK` | Varios | Sí | Consolidación para el ciclo siguiente |
| `sin_novedad_consecutivos` | Entero | Sí | Base de `PROPONER_CANCELACION` |
| `proximo_ciclo` | Fecha | Sí | Recalculado con la frecuencia |
| `motivo` | Texto | En CICLO_OMITIDO | «cubierto en C1» |

### 4.4 Respuesta del Broker (entrada `RESPUESTA_BROKER`)

`seg_id`, `respuesta_broker` `{run_id, decision, fecha}`; genera un aviso CT-22 `DECISION_SEGUIMIENTO` al Evaluador (12.4: valor de la vigilancia encargada).

## 5. Estados y transiciones

| Desde | Hacia | Quién | Condición |
|---|---|---|---|
| (alta) | ACTIVO | Coordinador | CT-24 `ALTA` válido |
| ACTIVO | PAUSADO | Coordinador | CT-24 `PAUSA` |
| PAUSADO | ACTIVO | Coordinador | CT-24 `REANUDACION` (próximo ciclo desde la fecha de reanudación) |
| ACTIVO · PAUSADO | CANCELADO | Coordinador | CT-24 `CANCELACION` (inmediata) o aceptación de `PROPONER_CANCELACION` |
| ACTIVO | FINALIZADO | Coordinador | `fecha_fin` alcanzada |

CANCELADO y FINALIZADO son finales: un nuevo seguimiento de la misma OPP- es un encargo nuevo (`SEG-` nuevo).

## 6. Índices de consulta

| Índice | Clave | Uso |
|---|---|---|
| Agenda | `estado` = ACTIVO, `proximo_ciclo` | Programación de HT-05 |
| Por oportunidad | `opp_id` | Absorción en C1; consultas N0 de estado |
| Por recomendación | `ciclo.recomendacion`, `respuesta_broker.decision` | Valor de la vigilancia (Evaluador) |
| Por tipo de activo | `clase` | Carga por Analista |

## 7. Ejemplo ficticio

> **EJEMPLO FICTICIO — no es una entrada real.**

```json
{"tipo_entrada":"ALTA","seg_id":"SEG-2026-0007","opp_id":"OPP-2026-0108","clase":"FON","frecuencia":"SEMANAL","calendario_personalizado":null,
 "motivo":"No la envío a B todavía; quiero vigilar si baja el descuento","senales_interes":["descuento sobre NAV","tipos a 10 años"],
 "fecha_fin":"2027-03-31","estado":"ACTIVO","fecha_alta":"2026-11-12","proximo_ciclo":"2026-11-19","aviso":null,"msg_id":"BRK-2026-11-12-0041"}
{"tipo_entrada":"CICLO","seg_id":"SEG-2026-0007","ciclos":1,"ultimo_run_id":"RUN-2026-0162","ultima_fecha":"2026-11-19",
 "ultima_recomendacion":"MANTENER_VIGILANCIA","ultimo_semaforo":"AMBAR","ultimo_RK":61,"sin_novedad_consecutivos":1,
 "ciclo":{"n":1,"run_id":"RUN-2026-0162","fecha":"2026-11-19","semaforo":"AMBAR","recomendacion":"MANTENER_VIGILANCIA",
          "ruta":"Informes de seguimiento/2026-11-19_informe-seguimiento_RUN-2026-0162.md","g3":"APTO","entregado":true},
 "proximo_ciclo":"2026-11-26"}
{"tipo_entrada":"CANCELACION","seg_id":"SEG-2026-0007","estado":"CANCELADO","proximo_ciclo":null,"fecha_cancelacion":"2026-12-02"}
```

## 8. Implementación de referencia

El ejecutor (`11_Ejecutor`) persiste F11 como `F11_registro_seguimientos.jsonl` (propietario de escritura AG-01; cualquier otra escritura se rechaza y se registra en HA) y lo opera con el subcomando `seguimiento` (alta, modificar, pausar, reanudar, cancelar, ejecutar, responder, listar).
