# Esquema de archivo operativo — F5 Historial de análisis

**Bloque A Forex · Robot Investor · Versión V1.0 · 02/11/2026 · actualizado V1.1 (03/11/2026)** · Subordinado al Documento 0 del Bloque A Forex, versión óptima V1.1. Actualización V1.1: consultas del bloque al Broker (CNS-FX-), solicitudes de credenciales (CRD-FX-, sin valores), ciclos de seguimiento encargado (RUN-FX- de tipo SEGUIMIENTO) y supuestos declarados.

---

## 1. Propósito

F5 es la **memoria episódica** del Bloque A Forex (sección 15 del Documento 0, R24): registra cada ejecución de análisis (RUN-FX-), cada consulta del Broker y su respuesta (QRY-), cada comunicación de retroalimentación o configuración del Broker (RET-) y, dentro de cada ejecución, los **informes transversales** del ciclo (política monetaria y macro de AG-09; posicionamiento, flujos y volatilidad de AG-21). Se consulta en F0 de cada ciclo (qué se propuso, qué cambió, qué decidió el Broker, qué decían los informes transversales anteriores), sostiene la sección «cambios frente al ciclo anterior» de los informes, permite responder consultas N0 de estado, historial y contexto macro-cambiario (p. ej., «¿qué descontaba el mercado para el BCE la semana pasada?»), y alimenta al Evaluador (consumo, utilidad, preguntas repetidas, decisiones) y al Orquestador (presupuestos, tiempos).

**No es**: un archivo de evidencia, de oportunidades ni de pronósticos (los referencia por identificador). Los informes transversales se archivan aquí como **registro del ciclo**; las tendencias persistentes que se derivan de ellos viven en F1 y las cifras que contienen remiten a F2 (EVD-/CLM-) y al Registro de cálculos (CALC-).

## 2. Propietario, lectores y contratos

| Aspecto | Contenido |
|---|---|
| Propietario de escritura | AG-01 Coordinador de Peticiones y Consultas (único) |
| Lectores | Todos los agentes |
| Contratos que lo alimentan | CT-23 (consultas del bloque al Broker y aportaciones del Broker), CT-24 (acciones de los encargos de seguimiento; el detalle vive en F11), CT-25 (solicitudes de credenciales, sin valores), CT-01 (petición), CT-02 (entrega), CT-03 (consulta y respuesta), CT-04 (retroalimentación y configuración), CT-05 (orden y retorno del Analizador, con decisiones de puertas, consumo, participantes e informes transversales del ciclo, que el Analizador adjunta tal como los recibió por CT-06T), CT-22 (avisos al Evaluador, registrados como referencia) |
| Herramientas | HT-05 (planificador), HT-06 (índice), HT-08 (consumo) |

## 3. Reglas

1. **Append-only en lo sustantivo** (R24). Correcciones como entradas nuevas referenciadas. Supresiones solo por la retención del Anexo A.
2. **Toda petición se registra**, también las encoladas, rechazadas por canal indebido o cerradas sin resultado (SIN_RESULTADO es legítimo con motivo).
3. **Decisiones de no continuar** (GC0–GC3) con su motivo, por segmento: son resultados legítimos y deben constar.
4. **Informes transversales**: todo RUN-FX- registra, para cada capa (BCM y PFV), si el informe se encargó completo, se actualizó solo en parte o se **reutilizó** del ciclo anterior (N1 sin cambio material), con su `msg_id` y fecha, o si faltó (con motivo y efecto declarado). Su contenido se archiva íntegro en `informes_transversales.contenido`; ningún agente distinto de AG-09 y AG-21 lo redacta.
5. **Sin datos personales del usuario ni credenciales**; el Broker se identifica por su rol. La divisa base del usuario es un parámetro de servicio, no un dato personal.
6. **Preguntas repetidas**: el Coordinador marca la QRY- con `tema_normalizado`; al alcanzar el umbral de F10 (3 en 4 semanas) genera un aviso CT-22 al Evaluador y lo anota.
7. Los cambios de configuración del Broker se registran aquí (RET-) y se aplican en F10; F5 conserva la petición y F10 el valor vigente.
8. **Consultas al Broker (CT-23, V1.1)**: cada consulta saliente o aportación entrante es una CNS-FX- con su respuesta, su vencimiento y los supuestos aplicados; las recurrentes (mismo tipo y motivo 3 veces en 8 semanas) generan aviso CT-22 `CONSULTA_RECURRENTE`.
9. **Credenciales (CT-25, V1.1)**: cada solicitud es una CRD-FX- con servicio, solicitante, uso, impacto, fechas, recordatorios, estado y alias de la bóveda de HT-01; **nunca el valor**. Un mensaje con una clave se rechaza íntegro y se registra como incidencia sin copiar el dato.
10. **Seguimiento encargado (V1.1)**: cada ciclo C6 es un RUN-FX- de tipo `SEGUIMIENTO` (4.4) vinculado a su SEG-FX- de F11; las acciones del encargo se anotan aquí de forma resumida y en F11 con detalle.

## 4. Formato de entrada

### 4.1 Ejecución (RUN-FX-)

| Campo | Tipo | Oblig. | Valores / formato |
|---|---|---|---|
| `run_id` | Identificador | Sí | `RUN-FX-AAAA-NNNN` |
| `tipo` | Enumerado | Sí | PERIODICO · AD_HOC · PROFUNDIZACION · CONSULTA_ANALITICA · SEGUIMIENTO (V1.1; campos de 4.4) |
| `disparador` | Objeto | Sí | `{origen HT-05·CT-01·CT-03, msg_id, qry_id}` |
| `fecha_inicio` / `fecha_entrega` / `fecha_objetivo` | Fecha-hora | Sí | ISO 8601 con zona |
| `alcance` | Objeto | Sí | `{segmentos, divisas, pares, tematicas, pregunta}` |
| `horizontes` | Lista | Sí | H1–H5 (H5 «limitado») |
| `supuestos_declarados` | Lista | No (V1.1) | `{supuesto, cns_id, efecto_si_falso}` aplicados en el RUN (6.2.9) |
| `prioridad` | Enumerado | Sí | ALTA · NORMAL · BAJA |
| `divisa_base_usuario` | ISO 4217 | Sí | Vigente en F10 al inicio del RUN- |
| `nivel_por_segmento` | Objeto | Sí | `{G10N: N1·N2·N3, …}`; nivel forzado por el Broker, si lo hubo |
| `gc0_por_segmento` | Objeto | Sí en PERIODICO | `{segmento: {cambio_material sí/no, motivos [MOVIMIENTO_1_5_SIGMA·REUNION_BANCO_CENTRAL·SORPRESA_DATO·INTERVENCION·INVALIDACION_CERCANA·LECCION_NUEVA], arrastre_verificado sí/no}}` |
| `informes_transversales` | Objeto | Sí | `{BCM: {modo COMPLETO·ACTUALIZACION·REUTILIZADO·AUSENTE, msg_id, msg_id_reutilizado, fecha, estado COMPLETO·PARCIAL·SIN_RESULTADO·RECHAZADO, instancias, consumo_uc, lagunas, motivo_ausencia, efecto_declarado, contenido}, PFV: {…}}` |
| `decisiones_puertas` | Lista | Sí | `{segmento, objeto, puerta GC1·GC2·GC3, resultado, motivo}` (resumen; el detalle está en F3) |
| `presupuesto` | Objeto | Sí | UC por segmento, por capa transversal y por fase; ampliaciones `{uc, autorizado_por AG-01·AG-18, motivo}` |
| `consumo` | Objeto | Sí | UC reales por segmento, capa transversal, fase y agente |
| `participantes` | Lista | Sí | `{agente, instancias, encargos}` |
| `methodology_version` | Texto | Sí | Vigente en F10 (p. ej., "FX-1.0") |
| `top3_por_segmento` | Objeto | Sí | `{segmento: {opciones [OPP-FX- en orden], menos_de_tres_motivo, semaforo VERDE·AMBAR·GRIS}}` |
| `cambios_vs_anterior` | Objeto | Sí | `{entradas, salidas, mantenidas, motivo por cambio}` |
| `exposicion_agregada` | Objeto | Sí | `{divisa: {signo LARGA·CORTA·NEUTRA, magnitud ELEVADA·MODERADA·LIGERA, opp_ids}}` |
| `contradicciones_entre_segmentos` | Lista | Sí (vacía declarada) | `{divisa, opp_ids, resolucion MANTENIDA_JUSTIFICADA·REFORMULADA·RETIRADA, justificacion}` |
| `apuestas_independientes` | Entero | Sí | — |
| `prg_congelados` | Lista | Sí | PRG-FX- |
| `entregables` | Objeto | Sí | Rutas ENT `AAAA-MM-DD_tipo_RUN-id` |
| `g3` | Objeto | Sí | `{g3v_id, dictamen APTO·APTO_CON_ADVERTENCIAS, advertencias}` |
| `estado` | Enumerado | Sí | COMPLETO · PARCIAL · SIN_RESULTADO · RECHAZADO |
| `limitaciones` / `incidencias` | Listas | Sí | Texto (vacío declarado) |
| `audit_ref` | Identificador | No | AUD- (cuando el Orquestador lo audita) |

**Contenido de los informes transversales** (`informes_transversales.<capa>.contenido`), tal como define el Anexo B para el CT-06T:

- **BCM** (AG-09): `regimen_global`; `bancos_centrales` [{`banco`, `tipo_actual`, `senda_descontada`, `sesgo`, `proxima_reunion`, `sorpresa_reciente`}]; `diferenciales` (nominales y reales, 2 años); `calendario` (fechas); `riesgos_intervencion`; `senales_por_segmento`; `lagunas`.
- **PFV** (AG-21): `posicionamiento` [{`divisa`, `neto_cftc`, `percentil_historico`, `cambio_semanal`}]; `flujos`; `volatilidad` [{`par`, `iv_1m`, `rv_1m`, `rr_25d`, `percentil`}]; `crowding_estrategias`; `base_cruzada`; `senales_por_segmento`; `lagunas`.

Toda cifra del contenido conserva su referencia (CALC-, serie HT-01 con fecha y fijación, o EVD-).

### 4.2 Consulta (QRY-)

| Campo | Tipo | Oblig. | Valores / formato |
|---|---|---|---|
| `qry_id` | Identificador | Sí | `QRY-AAAA-NNNN` |
| `fecha_recepcion` / `fecha_respuesta` | Fecha-hora | Sí | ISO 8601 |
| `pregunta` | Texto | Sí | Literal (sin datos personales) |
| `contexto` | Objeto | No | `{run_id, opp_id, prg_id, par, divisa}` |
| `urgencia` | Enumerado | Sí | INMEDIATA · NORMAL |
| `clase_consulta` | Enumerado | Sí | ACLARACION · DATO · METODO · CONTRASTE · PROFUNDIZACION · ESTADO |
| `ruta` | Enumerado | Sí | N0 · ANALITICA |
| `respuesta` | Texto | Sí | Respuesta entregada (pares en convención de mercado; qué divisa sube y cuál baja) |
| `referencias` | Lista | Sí en N0 | OPP-FX-, TND-FX-, CLM-, PRG-FX-, CALC-, RUN-FX-, `msg_id` de informes transversales |
| `confianza` | Enumerado | Sí | establecido · probable · especulativo · en disputa |
| `escalado` | Objeto | Si ANALITICA | `{run_id, plazo_estimado, respuesta_provisional}` |
| `tiempo_respuesta_s` | Número | Sí | Segundos |
| `tema_normalizado` | Texto | Sí | Para detección de repetición |
| `repeticion` | Objeto | No | `{veces_4_semanas, aviso_ct22_msg_id}` |
| `consumo_uc` | Número | Sí | — |

### 4.3 Retroalimentación y configuración (RET-)

| Campo | Tipo | Oblig. | Valores / formato |
|---|---|---|---|
| `ret_id` | Identificador | Sí | `RET-AAAA-NNNN` |
| `fecha` / `msg_id` | Fecha-hora / texto | Sí | — |
| `decisiones` | Lista | No | `{opp_id, decision ENVIADA_A_BLOQUE_B·EN_SEGUIMIENTO·DESCARTADA·APLAZADA, motivo}` |
| `valoracion_informe` | Objeto | No | `{run_id, utilidad 1–5, comentario}` |
| `configuracion` | Objeto | No | `{periodicidad, dia_hora_entrega, segmentos_activos, divisa_base_usuario, horizontes, idioma_usuario, formato_informe}` |
| `resultado_comunicado` | Objeto | No | `{opp_id, texto}` |
| `aplicado_en_f10` | Objeto | Si hay configuración | `{parametros, fecha_efecto, rechazos (p. ej., horizonte «No» de 8.3, parámetro CALIBRABLE u OPERADOR)}` |
| `aviso_ct22` | Texto | Sí | `msg_id` del aviso al Evaluador |

### 4.4 Entradas V1.1: consultas (CNS-FX-), credenciales (CRD-FX-) y ciclos de seguimiento

| Entrada | Campos |
|---|---|
| CNS-FX- (`tipo_entrada: CNS`, `CNS_RESPUESTA`, `CNS_VENCIDA`, `CNS_AGRUPACION`) | `cns_id`, `msg_id`, `sentido` SALIENTE·ENTRANTE, `run_id` o `seg_id`, `segmento` (si pausa un segmento), `tipo` ACLARACION_ALCANCE·DATO_O_DOCUMENTO·PREFERENCIA_O_CRITERIO·CONFIRMACION_SUPUESTO·OTRA, `modo` BLOQUEANTE·NO_BLOQUEANTE, `preguntas` [{texto, origen, por_que_importa, supuesto_declarado, efecto_si_falso}], `plazo_respuesta`, `punto_control`, `estado` PENDIENTE·RESPONDIDA·PARCIAL·VENCIDA·RECIBIDA (entrante), `respuestas`, `supuestos_aplicados`, `tardia`, `revision_C2_sugerida`; en las entrantes, `contenido` saneado (R9) y `fuente_evidencia: BROKER` |
| CRD-FX- (`tipo_entrada: CRD`, `CRD_RESPUESTA`, `CRD_RECORDATORIO`, `CRD_INCIDENCIA`) | `crd_id`, `servicio`, `herramienta` HT-01, `uso_previsto`, `solicitante`, `impacto_si_falta`, `urgencia`, `estado` SOLICITADA·PROVISTA·DENEGADA·APLAZADA, `estado_boveda`, `credencial_ref` (alias), `caducidad`, `recordatorios`, `servicio_degradado`. **Nunca el valor** |
| RUN-FX- de seguimiento (`tipo_entrada: RUN_SEGUIMIENTO`) | `run_id`, `tipo: SEGUIMIENTO`, `seg_id`, `opp_id`, `fecha`, `nivel: N1`, `presupuesto_uc`, `consumo`, `semaforo`, `recomendacion`, `entregables` (informe y JSON), `g3` (`validar_seguimiento`), `entrega` |
| SEG (`tipo_entrada: SEG`) | Resumen de cada acción CT-24 (`seg_id`, `accion`, `fecha`) y de la respuesta del Broker a la recomendación |

## 5. Estados y transiciones

**RUN-FX-**: `ENCOLADO` → `EN_CURSO` → `ENTREGADO` (COMPLETO o PARCIAL) | `CERRADO_SIN_RESULTADO` (con motivo) | `RECHAZADO` (canal o contenido indebido). Un RUN- `ENTREGADO` puede recibir una entrada `CORRECCION` referenciada si el operador decide emitir una corrección tras un hallazgo Crítico.

**QRY-**: `RECIBIDA` → `RESPONDIDA_N0` | `ESCALADA` → `RESPONDIDA_ANALITICA`.

**RET-**: `REGISTRADA` → `APLICADA` (configuración en F10) | `APLICADA_PARCIALMENTE` (con rechazos motivados).

**CNS-FX-** (saliente): `PENDIENTE` → `RESPONDIDA` | `PARCIAL` | `VENCIDA` (sigue con el supuesto declarado) → `RESPONDIDA` (tardía; revisión C2 si afecta a un informe entregado). **CRD-FX-**: `SOLICITADA` → `PROVISTA` | `DENEGADA` (limitación en F10; no se repite) | `APLAZADA` (recordatorios cada 7 días, máx. 3).

## 6. Índices de consulta

| Índice | Clave | Uso |
|---|---|---|
| Último ciclo por segmento | `tipo` = PERIODICO, `fecha_entrega`, `nivel_por_segmento` | F0: memoria y delta |
| Últimos informes transversales | `informes_transversales.BCM/PFV.msg_id`, `fecha` | Reutilización en N1; consultas N0 de contexto; comparación semana a semana de sendas y posicionamiento |
| Top-3 histórico | `top3_por_segmento` | «Cambios frente al ciclo anterior»; consultas de estado |
| Exposición agregada histórica | `exposicion_agregada` | Concentración por divisa a lo largo del tiempo; lecciones del Evaluador |
| Por oportunidad | OPP-FX- en `top3_por_segmento` y `decisiones` | Historial de una opción |
| Consultas por tema | `tema_normalizado`, fecha | Preguntas repetidas |
| Utilidad | `valoracion_informe.utilidad` | Lecciones de producto |
| Consumo | `consumo` por segmento, capa transversal y fase | Calibración de presupuestos |
| Tiempos | `tiempo_respuesta_s`, fechas de RUN- | Objetivo N0 < 2 min; carga |
| Auditoría | `audit_ref` | Enlace con HA |

## 7. Ejemplo ficticio

> **EJEMPLO FICTICIO — no es una entrada real.**

```json
{"qry_id":"QRY-FX-2026-0001","fecha_recepcion":"2026-11-10T09:02:11+01:00","fecha_respuesta":"2026-11-10T09:03:05+01:00",
 "pregunta":"¿Por qué el peso mexicano no aparece esta semana?","contexto":{"run_id":"RUN-FX-2026-0001","opp_id":null,"prg_id":null,"par":"USD/MXN","divisa":"MXN"},
 "urgencia":"NORMAL","clase_consulta":"ACLARACION","ruta":"N0",
 "respuesta":"Se analizaron 6 candidatas en EMLA. «USD/MXN bajista (peso al alza)» no superó GC2 (E provisional 45) y el informe de posicionamiento de esta semana sitúa los largos especulativos en MXN en el percentil 94, lo que penaliza la dimensión de posicionamiento de A.",
 "referencias":["RUN-FX-2026-0001","OPP-FX-2026-0019","MSG-2026-11-07-0021"],"confianza":"establecido","escalado":null,"tiempo_respuesta_s":54,
 "tema_normalizado":"MXN ausente del top-3","repeticion":{"veces_4_semanas":1,"aviso_ct22_msg_id":null},"consumo_uc":0.4}
```

Fragmento ficticio de RUN-FX- (solo los campos propios de divisas):

```json
{"run_id":"RUN-FX-2026-0001","divisa_base_usuario":"EUR",
 "nivel_por_segmento":{"G10N":"N2","G10M":"N1","EMAS":"N1","EMLA":"N2","EMEA":"N1","ESTR":"N2"},
 "informes_transversales":{"BCM":{"modo":"COMPLETO","msg_id":"MSG-2026-11-07-0018","fecha":"2026-11-07","estado":"COMPLETO","instancias":1,"consumo_uc":5.6,"lagunas":["sin curva OIS fiable para EGP"]},
   "PFV":{"modo":"COMPLETO","msg_id":"MSG-2026-11-07-0021","fecha":"2026-11-07","estado":"COMPLETO","instancias":1,"consumo_uc":5.1,"lagunas":[]}},
 "exposicion_agregada":{"USD":{"signo":"CORTA","magnitud":"MODERADA","opp_ids":["OPP-FX-2026-0007","OPP-FX-2026-0012"]},"JPY":{"signo":"LARGA","magnitud":"MODERADA","opp_ids":["OPP-FX-2026-0007"]},"EUR":{"signo":"NEUTRA","magnitud":"LIGERA","opp_ids":[]}},
 "contradicciones_entre_segmentos":[],"apuestas_independientes":4}
```
