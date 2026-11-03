# Esquema de archivo operativo — F5 Historial de análisis

**Bloque A · Robot Investor · Versión óptima V4.0 · 01/11/2026 · actualizado V5.1 (03/11/2026)** · Subordinado al Documento 0 óptima V5.1. Cambios V5.1: consultas del bloque al Broker (CNS-, CT-23), solicitudes de credenciales (CRD-, CT-25, sin valores), acciones de los encargos de seguimiento (CT-24) y ciclos C6 (RUN- de tipo SEGUIMIENTO vinculados a su SEG- de F11); horizontes H1–H5.

---

## 1. Propósito

F5 es la **memoria episódica** del Bloque A (sección 15 del Documento 0, R24): registra cada ejecución de análisis (RUN-), cada consulta del Broker y su respuesta (QRY-) y cada comunicación de retroalimentación o configuración del Broker (RET-); desde V5.1, además, cada consulta del bloque al Broker y su respuesta o vencimiento (CNS-), cada solicitud de credencial (CRD-, sin valores), cada acción sobre un encargo de seguimiento (CT-24) y cada ciclo de seguimiento encargado (RUN- de tipo SEGUIMIENTO). Se consulta en F0 de cada ciclo (qué se propuso, qué cambió, qué decidió el Broker), sostiene la sección «cambios frente al ciclo anterior» de los informes, permite responder consultas N0 de estado e historial, y alimenta al Evaluador (consumo, utilidad, preguntas repetidas, decisiones) y al Orquestador (presupuestos, tiempos).

**No es**: un archivo de evidencia, de oportunidades ni de pronósticos (los referencia por identificador).

## 2. Propietario, lectores y contratos

| Aspecto | Contenido |
|---|---|
| Propietario de escritura | AG-01 Coordinador de Peticiones y Consultas (único) |
| Lectores | Todos los agentes |
| Contratos que lo alimentan | CT-01 (petición), CT-02 (entrega), CT-03 (consulta y respuesta), CT-04 (retroalimentación y configuración), CT-05 (orden y retorno del Analizador, con decisiones de puertas, consumo y participantes), CT-22 (avisos al Evaluador, registrados como referencia; V5.1: también `CONSULTA_RECURRENTE` y `DECISION_SEGUIMIENTO`), CT-23 (consultas al Broker), CT-24 (encargos de seguimiento; el detalle vive en F11), CT-25 (credenciales) |
| Herramientas | HT-05 (planificador), HT-06 (índice), HT-08 (consumo) |

## 3. Reglas

1. **Append-only en lo sustantivo** (R24). Correcciones como entradas nuevas referenciadas. Supresiones solo por la retención del Anexo A.
2. **Toda petición se registra**, también las encoladas, rechazadas por canal indebido o cerradas sin resultado (SIN_RESULTADO es legítimo con motivo).
3. **Decisiones de no continuar** (GC0–GC3) con su motivo: son resultados legítimos y deben constar.
4. **Sin datos personales del usuario ni credenciales**; el Broker se identifica por su rol. Una CRD- registra servicio, solicitante, fechas, estado y alias de la bóveda de HT-01, **nunca el valor**; un mensaje que lo contenga se rechaza sin copiarlo (6.2.5).
4 bis. **Consultas recurrentes del bloque** (V5.1): el mismo tipo y motivo de CNS- 3 veces en 8 semanas genera un aviso CT-22 `CONSULTA_RECURRENTE` al Evaluador, que se anota.
5. **Preguntas repetidas**: el Coordinador marca la QRY- con `tema_normalizado`; al alcanzar el umbral de F10 (3 en 4 semanas) genera un aviso CT-22 al Evaluador y lo anota.
6. Los cambios de configuración del Broker se registran aquí (RET-) y se aplican en F10; F5 conserva la petición y F10 el valor vigente.

## 4. Formato de entrada

### 4.1 Ejecución (RUN-)

| Campo | Tipo | Oblig. | Valores / formato |
|---|---|---|---|
| `run_id` | Identificador | Sí | `RUN-AAAA-NNNN` |
| `tipo` | Enumerado | Sí | PERIODICO · AD_HOC · PROFUNDIZACION · CONSULTA_ANALITICA · SEGUIMIENTO (V5.1: ciclo C6, con `seg_id` y `opp_id`; solo campos aplicables) |
| `disparador` | Objeto | Sí | `{origen HT-05·CT-01·CT-03, msg_id, qry_id}` |
| `fecha_inicio` / `fecha_entrega` / `fecha_objetivo` | Fecha-hora | Sí | ISO 8601 con zona |
| `alcance` | Objeto | Sí | `{clases, regiones, tematicas, activos_concretos, pregunta}` |
| `horizontes` | Lista | Sí | H1–H5 |
| `prioridad` | Enumerado | Sí | ALTA · NORMAL · BAJA |
| `nivel_por_clase` | Objeto | Sí | `{RV: N1·N2·N3, …}`; nivel forzado por el Broker, si lo hubo |
| `gc0_por_clase` | Objeto | Sí en PERIODICO | `{clase: {cambio_material sí/no, motivos, arrastre_verificado sí/no}}` |
| `decisiones_puertas` | Lista | Sí | `{clase, objeto, puerta GC1·GC2·GC3, resultado, motivo}` (resumen; el detalle está en F3) |
| `presupuesto` | Objeto | Sí | UC por clase y fase; ampliaciones `{uc, autorizado_por AG-01·AG-18, motivo}` |
| `consumo` | Objeto | Sí | UC reales por clase, fase y agente |
| `participantes` | Lista | Sí | `{agente, instancias, encargos}` |
| `methodology_version` | Texto | Sí | Vigente en F10 |
| `top3_por_clase` | Objeto | Sí | `{clase: [OPP- en orden], menos_de_tres_motivo}` |
| `cambios_vs_anterior` | Objeto | Sí | `{entradas, salidas, mantenidas, motivo por cambio}` |
| `apuestas_independientes` | Entero | Sí | — |
| `prg_congelados` | Lista | Sí | PRG- |
| `entregables` | Objeto | Sí | Rutas ENT `AAAA-MM-DD_tipo_RUN-id` |
| `g3` | Objeto | Sí | `{g3v_id, dictamen APTO·APTO_CON_ADVERTENCIAS, advertencias}` |
| `estado` | Enumerado | Sí | COMPLETO · PARCIAL · SIN_RESULTADO · RECHAZADO |
| `limitaciones` / `incidencias` | Listas | Sí | Texto (vacío declarado) |
| `audit_ref` | Identificador | No | AUD- (cuando el Orquestador lo audita) |
| `supuestos_declarados` | Lista | Si los hay (V5.1) | `{supuesto, cns_id, efecto_si_falso}` de consultas CT-23 sin respuesta |
| `seg_id` / `recomendacion` | Identificador / enumerado | Sí en SEGUIMIENTO | SEG- · MANTENER_VIGILANCIA · PROPONER_ENVIO_A_B · CERRAR · PROPONER_CANCELACION |

### 4.2 Consulta (QRY-)

| Campo | Tipo | Oblig. | Valores / formato |
|---|---|---|---|
| `qry_id` | Identificador | Sí | `QRY-AAAA-NNNN` |
| `fecha_recepcion` / `fecha_respuesta` | Fecha-hora | Sí | ISO 8601 |
| `pregunta` | Texto | Sí | Literal (sin datos personales) |
| `contexto` | Objeto | No | `{run_id, opp_id, prg_id}` |
| `urgencia` | Enumerado | Sí | INMEDIATA · NORMAL |
| `clase_consulta` | Enumerado | Sí | ACLARACION · DATO · METODO · CONTRASTE · PROFUNDIZACION · ESTADO |
| `ruta` | Enumerado | Sí | N0 · ANALITICA |
| `respuesta` | Texto | Sí | Respuesta entregada |
| `referencias` | Lista | Sí en N0 | OPP-, TND-, CLM-, PRG-, CALC-, RUN- |
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
| `configuracion` | Objeto | No | `{periodicidad, dia_hora_entrega, clases_activas, horizontes, idioma_usuario}` |
| `resultado_comunicado` | Objeto | No | `{opp_id, texto}` |
| `aplicado_en_f10` | Objeto | Si hay configuración | `{parametros, fecha_efecto, rechazos (p. ej., horizonte «No» de 8.3)}` |
| `aviso_ct22` | Texto | Sí | `msg_id` del aviso al Evaluador |

### 4.4 Consulta del bloque al Broker (CNS-, CT-23; V5.1)

| Campo | Tipo | Oblig. | Valores / formato |
|---|---|---|---|
| `cns_id` | Identificador | Sí | `CNS-AAAA-NNNN` |
| `sentido` | Enumerado | Sí | SALIENTE (pregunta del bloque) · ENTRANTE (aportación espontánea del Broker) |
| `run_id` / `seg_id` | Identificadores | No | Análisis o encargo al que se refiere |
| `tipo` | Enumerado | Sí | ACLARACION_ALCANCE · DATO_O_DOCUMENTO · PREFERENCIA_O_CRITERIO · CONFIRMACION_SUPUESTO · OTRA |
| `modo` | Enumerado | Sí | BLOQUEANTE · NO_BLOQUEANTE |
| `preguntas` | Lista | Sí en SALIENTE | `{texto, origen AG-xx, por_que_importa, supuesto_declarado, efecto_si_falso, opciones_sugeridas}` |
| `clases` | Lista | No | Tipos de activo afectados (los que pausa una BLOQUEANTE) |
| `plazo_respuesta` / `punto_control` | Fecha-hora / texto | Sí en SALIENTE | Anexo A (P-34 de F10) |
| `contenido` / `referencia` | Texto / objeto | Sí en ENTRANTE | Aportación del Broker y RUN-, OPP- o SEG- asociado |
| `estado` | Enumerado | Sí | ENVIADA · RESPONDIDA · PARCIAL · VENCIDA · RECIBIDA |
| `respuestas` / `supuestos_aplicados` | Listas | Al responder o vencer | — |
| `tardia` | Booleano | Al responder | Respuesta posterior al vencimiento (posible revisión C2) |

### 4.5 Solicitud de credencial (CRD-, CT-25; V5.1)

| Campo | Tipo | Oblig. | Valores / formato |
|---|---|---|---|
| `crd_id` | Identificador | Sí | `CRD-AAAA-NNNN` |
| `servicio` / `herramienta` | Texto | Sí | Servicio externo; HT-01 |
| `solicitante` / `uso_previsto` / `impacto_si_falta` / `urgencia` | Texto | Sí | — |
| `estado` | Enumerado | Sí | SOLICITADA · PROVISTA · DENEGADA · APLAZADA |
| `credencial_ref` / `caducidad` | Alias / fecha | Si PROVISTA | Alias en la bóveda de HT-01; **nunca el valor** |
| `recordatorios` | Entero | Sí | 0–3 (cada 7 días mientras siga degradado) |

### 4.6 Acción sobre un encargo de seguimiento (CT-24; V5.1)

`seg_id`, `accion` (ALTA · MODIFICACION · PAUSA · REANUDACION · CANCELACION), `msg_id`, acuse (estado, próximo ciclo, aviso de frecuencia corta). El encargo completo y su historial viven en F11.

## 5. Estados y transiciones

**RUN-**: `ENCOLADO` → `EN_CURSO` → `ENTREGADO` (COMPLETO o PARCIAL) | `CERRADO_SIN_RESULTADO` (con motivo) | `RECHAZADO` (canal o contenido indebido). Un RUN- `ENTREGADO` puede recibir una entrada `CORRECCION` referenciada si el operador decide emitir una corrección tras un hallazgo Crítico.

**QRY-**: `RECIBIDA` → `RESPONDIDA_N0` | `ESCALADA` → `RESPONDIDA_ANALITICA`.

**RET-**: `REGISTRADA` → `APLICADA` (configuración en F10) | `APLICADA_PARCIALMENTE` (con rechazos motivados).

**CNS-** (V5.1): `ENVIADA` → `RESPONDIDA` | `PARCIAL` | `VENCIDA` (se aplica el supuesto declarado) → `RESPONDIDA` (tardía). `RECIBIDA` para las entrantes.

**CRD-** (V5.1): `SOLICITADA` → `PROVISTA` | `DENEGADA` (limitación de servicio en F10) | `APLAZADA` → `SOLICITADA` (recordatorio).

## 6. Índices de consulta

| Índice | Clave | Uso |
|---|---|---|
| Último ciclo por clase | `tipo` = PERIODICO, `fecha_entrega` | F0: memoria y delta |
| Top-3 histórico | `top3_por_clase` | «Cambios frente al ciclo anterior»; consultas de estado |
| Por oportunidad | OPP- en `top3_por_clase` y `decisiones` | Historial de una opción |
| Consultas por tema | `tema_normalizado`, fecha | Preguntas repetidas |
| Utilidad | `valoracion_informe.utilidad` | Lecciones de producto |
| Consumo | `consumo` por clase y fase | Calibración de presupuestos |
| Tiempos | `tiempo_respuesta_s`, fechas de RUN- | Objetivo N0 < 2 min; carga |
| Auditoría | `audit_ref` | Enlace con HA |
| Consultas al Broker (V5.1) | `cns_id`, `estado`, `plazo_respuesta` | Vencimientos (HT-05), supuestos declarados, consultas recurrentes |
| Credenciales (V5.1) | `crd_id`, `servicio`, `estado` | Recordatorios y servicios degradados |
| Ciclos C6 (V5.1) | `tipo` = SEGUIMIENTO, `seg_id` | Historial de un encargo; valor de la vigilancia (Evaluador) |

## 7. Ejemplo ficticio

> **EJEMPLO FICTICIO — no es una entrada real.**

```json
{"qry_id":"QRY-2026-0001","fecha_recepcion":"2026-11-10T09:02:11+01:00","fecha_respuesta":"2026-11-10T09:03:05+01:00",
 "pregunta":"¿Por qué la renta fija emergente no aparece esta semana?","contexto":{"run_id":"RUN-2026-0001","opp_id":null,"prg_id":null},
 "urgencia":"NORMAL","clase_consulta":"ACLARACION","ruta":"N0",
 "respuesta":"Se analizaron 6 candidatas en RF; la de deuda emergente en moneda local no superó PS2 (dato de curva con 9 días) ni GC2 (E provisional 45).",
 "referencias":["RUN-2026-0001","OPP-2026-0009"],"confianza":"establecido","escalado":null,"tiempo_respuesta_s":54,
 "tema_normalizado":"RF emergente ausente del top-3","repeticion":{"veces_4_semanas":1,"aviso_ct22_msg_id":null},"consumo_uc":0.4}
```
