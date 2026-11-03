# Esquema de archivo operativo — F11 Registro de seguimientos encargados

**Bloque A Forex · Robot Investor · Versión V1.1 · 03/11/2026** · Subordinado al Documento 0 del Bloque A Forex, versión óptima V1.1 (secciones 5.1, 6.1 CT-24, 7.1 C6, 7.11, 14.4 y Anexos A y B). Archivo nuevo en V1.1.

---

## 1. Propósito

F11 registra los **encargos de seguimiento de opción** que el Broker hace por **CT-24** y cada uno de sus **ciclos C6**. Un encargo es la vigilancia periódica de una OPP-FX- que el Broker decidió no enviar al Bloque B pero quiere seguir (R27): el bloque **no abre seguimientos por iniciativa propia**, y el Broker puede **dar de alta, modificar, pausar, reanudar o cancelar** cada encargo **en cualquier momento** (la cancelación surte efecto inmediato).

F11 es la fuente de verdad de: qué se vigila, con qué frecuencia, con qué señales de interés y hasta cuándo; en qué estado está cada encargo; qué produjo cada ciclo (semáforo, recomendación, informe) y qué respondió el Broker. HT-05 programa los ciclos a partir de F11.

**No es**: el seguimiento de las opciones vigentes del top-3, que sigue dentro del ciclo C1 (Documento 0, 9.6.4 y 14.1); ni un registro de oportunidades (F3) o de pronósticos (F4), que solo se referencian.

## 2. Propietario, lectores y contratos

| Aspecto | Contenido |
|---|---|
| Propietario de escritura | AG-01 Coordinador de Peticiones y Consultas (único) |
| Lectores | AG-02 Analizador; Analistas de segmento (AG-03 a AG-08); AG-17 Redactor; AG-18 Orquestador; AG-19 Auditor; AG-20 Evaluador; HT-05 (programación) |
| Contratos que lo alimentan | CT-24 (alta, modificación, pausa, reanudación, cancelación y retorno con el informe de cada ciclo); CT-05 de tipo `SEGUIMIENTO` (orden del ciclo C6 y retorno del Analizador); CT-22 `DECISION_SEGUIMIENTO` (aviso al Evaluador de la respuesta del Broker) |
| Herramientas | HT-05 (próximo ciclo según la frecuencia), HT-06 (índice), HT-09 (`validar_seguimiento` del informe) |
| Relación con otros archivos | F3: `decision_broker = EN_SEGUIMIENTO` y `seg_id` (los anota el Analizador, propietario de F3). F5: cada ciclo es un RUN-FX- de tipo `SEGUIMIENTO`. F6: resultados de los hitos H5 citados en el informe. ENT: `Informes de seguimiento/` |

## 3. Reglas

1. **Append-only** (R24, 5.2.1): cada acción (alta, modificación, pausa, reanudación, cancelación, finalización, ciclo, ciclo omitido, respuesta del Broker) es una entrada nueva con fecha y `msg_id`; el estado vigente es la consolidación de las entradas por `seg_id`.
2. **Admisión**: cualquier OPP-FX- registrada en F3, haya estado o no en un top-3. Sin límite de encargos (R5): se encolan con prioridad inferior a C1–C3.
3. **Frecuencia**: `DIARIA`, `SEMANAL` (por defecto), `QUINCENAL`, `MENSUAL`, `TRIMESTRAL` o `PERSONALIZADA` (lista de fechas o cada *n* días), a elección del Broker. Si es más corta que la orientativa para el horizonte principal de la opción (Anexo A: H1 diaria · H2 diaria o semanal · H3 semanal a mensual · H4 mensual o trimestral · H5 trimestral), se **acepta** y se registra el `aviso` (nunca es un veto).
4. **Cancelación inmediata**: estado `CANCELADO`, `proximo_ciclo = null`; el ciclo en curso se detiene en su siguiente punto de control y no produce informe.
5. **Pausa**: `PAUSADO`, sin ciclos hasta la reanudación (que recalcula el próximo ciclo desde la fecha de reanudación).
6. **Fin**: al pasar la `fecha_fin`, el encargo pasa a `FINALIZADO` y se avisa al Broker.
7. **Ciclos omitidos**: si la opción vuelve a ser `VIGENTE` en el top-3 de un C1, su seguimiento se cubre allí y el C6 coincidente se anota como `CICLO_OMITIDO`. Si un C6 no encuentra hueco antes del siguiente de su encargo, ambos se fusionan en un informe (anotado).
8. **Presupuesto por ciclo** (Anexo A): 2 UC; hasta 5 UC si el delta es material; ≤ 0,5 UC si es «sin novedad». Se registra el consumo de cada ciclo.
9. **Sin credenciales ni datos personales** (R8). Las señales de interés describen el mercado (niveles del indicador, reuniones, datos), nunca la posición del usuario.

## 4. Formato de entrada

### 4.1 Alta (`tipo_entrada: ALTA`)

| Campo | Tipo | Oblig. | Valores / formato |
|---|---|---|---|
| `seg_id` | Identificador | Sí | `SEG-FX-AAAA-NNNN` |
| `opp_id` | Identificador | Sí | OPP-FX- existente en F3 |
| `segmento` | Enumerado | Sí | G10N · G10M · EMAS · EMLA · EMEA · ESTR |
| `motivo` | Texto | Sí | Por qué el Broker quiere vigilarla |
| `frecuencia` | Enumerado | Sí | DIARIA · SEMANAL · QUINCENAL · MENSUAL · TRIMESTRAL · PERSONALIZADA |
| `calendario_personalizado` | Lista de fechas u objeto | Si PERSONALIZADA | `["AAAA-MM-DD", …]` o `{"dias": n}` |
| `senales_interes` | Lista de textos | No | P. ej., «USD/JPY por debajo de 140», «reunión del BoJ de diciembre» |
| `fecha_fin` | Fecha | No | `AAAA-MM-DD` |
| `horizonte_principal` | Enumerado | Sí | H1–H5 (el de la opción en F3) |
| `aviso` | Texto | No | Aviso de frecuencia (regla 3) |
| `estado` | Enumerado | Sí | ACTIVO |
| `fecha_alta`, `proximo_ciclo` | Fecha | Sí | `proximo_ciclo` calculado por HT-05 |
| `msg_id` | Identificador | Sí | Mensaje CT-24 del Broker |

### 4.2 Acciones posteriores

| `tipo_entrada` | Campos |
|---|---|
| `MODIFICACION` | Los campos cambiados (`frecuencia`, `calendario_personalizado`, `senales_interes`, `fecha_fin`, `motivo`), `proximo_ciclo` recalculado, `aviso` |
| `PAUSA` | `estado: PAUSADO`, `proximo_ciclo: null` |
| `REANUDACION` | `estado: ACTIVO`, `proximo_ciclo` |
| `CANCELACION` | `estado: CANCELADO`, `proximo_ciclo: null`, `motivo_cancelacion` |
| `FINALIZACION` | `estado: FINALIZADO` (por `fecha_fin`) |
| `CICLO_OMITIDO` | `motivo` (cubierto por C1 o fusionado), `proximo_ciclo` |
| `RESPUESTA_BROKER` | `run_id_respuesta`, `respuesta_broker` (p. ej., `MANTENER_VIGILANCIA`, `ENVIAR_A_BLOQUE_B`, `CANCELAR`), `comentario` |

### 4.3 Ciclo (`tipo_entrada: CICLO`)

| Campo | Tipo | Oblig. | Valores / formato |
|---|---|---|---|
| `run_id` | Identificador | Sí | `RUN-FX-AAAA-NNNN` de tipo `SEGUIMIENTO` (también en F5) |
| `fecha`, `ciclo_n` | Fecha, entero | Sí | Número de ciclo del encargo |
| `semaforo` | Enumerado | Sí | VERDE · AMBAR · ROJO |
| `recomendacion` | Enumerado | Sí | MANTENER_VIGILANCIA · PROPONER_ENVIO_A_B · CERRAR · PROPONER_CANCELACION |
| `ruta_informe`, `ruta_json` | Ruta | Sí | `Informes de seguimiento/AAAA-MM-DD_informe-seguimiento_RUN-FX-id.md` y `.json` |
| `dictamen_ht09` | Enumerado | Sí | APTO · APTO_CON_ADVERTENCIAS · BLOQUEADO (`validar_seguimiento`) |
| `entrega` | Enumerado | Sí | ENTREGADA · BLOQUEADA |
| `consumo_uc` | Número | Sí | Regla 8 |
| `ciclos_sin_novedad_seguidos` | Entero | Sí | Base de `PROPONER_CANCELACION` |
| `ultimo_nivel`, `ultimo_RK` | Número | No | Referencias para el delta del ciclo siguiente |
| `proximo_ciclo` | Fecha | Sí | HT-05 |
| `respuesta_broker` | Texto | No | Se completa con una entrada `RESPUESTA_BROKER` |

## 5. Estados y transiciones

```
ALTA → ACTIVO ──PAUSA──> PAUSADO ──REANUDACION──> ACTIVO
   ACTIVO / PAUSADO ──CANCELACION (inmediata)──> CANCELADO (final)
   ACTIVO ──fecha_fin superada──> FINALIZADO (final)
```

Una recomendación `PROPONER_CANCELACION` **no** cancela nada: la cancelación solo la decide el Broker (R4). Una recomendación `CERRAR` por invalidación verificada cierra la OPP-FX- en F3 (único cambio de estado analítico que puede producir un seguimiento); el encargo sigue activo hasta que el Broker lo cancele o venza.

## 6. Índices de consulta

| Consulta típica | Clave |
|---|---|
| Encargos activos y próximos ciclos (HT-05) | `estado = ACTIVO`, `proximo_ciclo` |
| Historial de una opción vigilada | `opp_id` |
| Informes de un encargo | `seg_id` → entradas `CICLO` |
| Valor de la vigilancia (Evaluador) | `recomendacion` y `respuesta_broker` frente a la resolución de los PRG de la opción |

## 7. Ejemplo ficticio

```json
{"tipo_entrada":"ALTA","seg_id":"SEG-FX-2026-0003","opp_id":"OPP-FX-2026-0106","segmento":"G10N","motivo":"No la envío a B por ahora; quiero vigilarla hasta la reunión del BoJ",
 "frecuencia":"SEMANAL","calendario_personalizado":null,"senales_interes":["USD/JPY por debajo de 140","reunión del BoJ de diciembre"],
 "fecha_fin":"2027-01-31","horizonte_principal":"H3","aviso":null,"estado":"ACTIVO","fecha_alta":"2026-11-17","proximo_ciclo":"2026-11-24","msg_id":"BRK-2026-11-17-0002"}
{"tipo_entrada":"CICLO","seg_id":"SEG-FX-2026-0003","run_id":"RUN-FX-2026-0071","fecha":"2026-11-24","ciclo_n":1,"semaforo":"AMBAR",
 "recomendacion":"MANTENER_VIGILANCIA","ruta_informe":"Informes de seguimiento/2026-11-24_informe-seguimiento_RUN-FX-2026-0071.md",
 "ruta_json":"Informes de seguimiento/2026-11-24_informe-seguimiento_RUN-FX-2026-0071.json","dictamen_ht09":"APTO","entrega":"ENTREGADA",
 "consumo_uc":0.5,"ciclos_sin_novedad_seguidos":1,"ultimo_nivel":151.2,"ultimo_RK":62,"proximo_ciclo":"2026-12-01","respuesta_broker":null}
{"tipo_entrada":"CANCELACION","seg_id":"SEG-FX-2026-0003","estado":"CANCELADO","proximo_ciclo":null,"motivo_cancelacion":"Ya no interesa","fecha":"2026-12-05"}
```

Implementación de referencia: `11_Ejecutor/bloque_a_forex/seguimiento.py` (archivo `F11_registro_seguimientos.jsonl`; estado «implementado» con pruebas, R22).
