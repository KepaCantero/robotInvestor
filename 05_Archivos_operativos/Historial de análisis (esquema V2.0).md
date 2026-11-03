# Esquema de archivo operativo — F5 Historial de análisis

**Bloque A · Robot Investor · Versión óptima V4.0 · 01/11/2026** · Subordinado al Documento 0 óptima V5.0.

---

## 1. Propósito

F5 es la **memoria episódica** del Bloque A (sección 15 del Documento 0, R24): registra cada ejecución de análisis (RUN-), cada consulta del Broker y su respuesta (QRY-) y cada comunicación de retroalimentación o configuración del Broker (RET-). Se consulta en F0 de cada ciclo (qué se propuso, qué cambió, qué decidió el Broker), sostiene la sección «cambios frente al ciclo anterior» de los informes, permite responder consultas N0 de estado e historial, y alimenta al Evaluador (consumo, utilidad, preguntas repetidas, decisiones) y al Orquestador (presupuestos, tiempos).

**No es**: un archivo de evidencia, de oportunidades ni de pronósticos (los referencia por identificador).

## 2. Propietario, lectores y contratos

| Aspecto | Contenido |
|---|---|
| Propietario de escritura | AG-01 Coordinador de Peticiones y Consultas (único) |
| Lectores | Todos los agentes |
| Contratos que lo alimentan | CT-01 (petición), CT-02 (entrega), CT-03 (consulta y respuesta), CT-04 (retroalimentación y configuración), CT-05 (orden y retorno del Analizador, con decisiones de puertas, consumo y participantes), CT-22 (avisos al Evaluador, registrados como referencia) |
| Herramientas | HT-05 (planificador), HT-06 (índice), HT-08 (consumo) |

## 3. Reglas

1. **Append-only en lo sustantivo** (R24). Correcciones como entradas nuevas referenciadas. Supresiones solo por la retención del Anexo A.
2. **Toda petición se registra**, también las encoladas, rechazadas por canal indebido o cerradas sin resultado (SIN_RESULTADO es legítimo con motivo).
3. **Decisiones de no continuar** (GC0–GC3) con su motivo: son resultados legítimos y deben constar.
4. **Sin datos personales del usuario ni credenciales**; el Broker se identifica por su rol.
5. **Preguntas repetidas**: el Coordinador marca la QRY- con `tema_normalizado`; al alcanzar el umbral de F10 (3 en 4 semanas) genera un aviso CT-22 al Evaluador y lo anota.
6. Los cambios de configuración del Broker se registran aquí (RET-) y se aplican en F10; F5 conserva la petición y F10 el valor vigente.

## 4. Formato de entrada

### 4.1 Ejecución (RUN-)

| Campo | Tipo | Oblig. | Valores / formato |
|---|---|---|---|
| `run_id` | Identificador | Sí | `RUN-AAAA-NNNN` |
| `tipo` | Enumerado | Sí | PERIODICO · AD_HOC · PROFUNDIZACION · CONSULTA_ANALITICA |
| `disparador` | Objeto | Sí | `{origen HT-05·CT-01·CT-03, msg_id, qry_id}` |
| `fecha_inicio` / `fecha_entrega` / `fecha_objetivo` | Fecha-hora | Sí | ISO 8601 con zona |
| `alcance` | Objeto | Sí | `{clases, regiones, tematicas, activos_concretos, pregunta}` |
| `horizontes` | Lista | Sí | H1–H4 |
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

## 5. Estados y transiciones

**RUN-**: `ENCOLADO` → `EN_CURSO` → `ENTREGADO` (COMPLETO o PARCIAL) | `CERRADO_SIN_RESULTADO` (con motivo) | `RECHAZADO` (canal o contenido indebido). Un RUN- `ENTREGADO` puede recibir una entrada `CORRECCION` referenciada si el operador decide emitir una corrección tras un hallazgo Crítico.

**QRY-**: `RECIBIDA` → `RESPONDIDA_N0` | `ESCALADA` → `RESPONDIDA_ANALITICA`.

**RET-**: `REGISTRADA` → `APLICADA` (configuración en F10) | `APLICADA_PARCIALMENTE` (con rechazos motivados).

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
