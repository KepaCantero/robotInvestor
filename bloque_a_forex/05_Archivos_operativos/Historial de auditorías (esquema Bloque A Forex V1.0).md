# Esquema de archivo operativo — HA Historial de auditorías

**Bloque A Forex · Robot Investor · Versión V1.0 · 02/11/2026** · Subordinado al Documento 0 del Bloque A Forex, versión óptima V1.0.

---

## 1. Propósito

El Historial de auditorías (HA) es el registro único del **control de calidad y del gobierno operativo** del Bloque A Forex: validaciones G3 y dictámenes de excepción (incluidas las comprobaciones cambiarias de notación, convertibilidad, carry, anticipación en fijaciones, exposición agregada y contradicciones entre segmentos), ciclos de auditoría asíncrona, hallazgos y severidades, guías de mejora, órdenes de escalado por instancias (también de los Analistas transversales), autorizaciones de presupuesto, paquetes de mantenimiento de conocimiento (F7 TX-, F8 TMX-, F9 TFX-), propuestas de tipo 3, incidencias de seguridad, métricas de carga y revisiones trimestrales. Lo usa el Evaluador como materia prima del aprendizaje de nivel A y el operador como base de sus decisiones.

## 2. Propietario, lectores y contratos

| Aspecto | Contenido |
|---|---|
| Propietario de escritura | AG-18 Orquestador técnico (único; los resultados automáticos de HT-09 y las métricas de HT-08 se registran bajo su propiedad) |
| Lectores | AG-18, AG-19 Auditor, AG-20 Evaluador; AG-02 Analizador (extractos: sus G3, hallazgos y guías) |
| Contratos | CT-14, CT-16, CT-17, CT-18, CT-19 (lecciones y propuestas del Evaluador), CT-21, CT-09/CT-10 (verificaciones) |
| Herramientas | HT-09, HT-08, HT-07, HT-03 |

## 3. Reglas

1. **Append-only**: los cambios de estado de hallazgos, guías y propuestas son entradas nuevas; las correcciones del propio proceso referencian la entrada original.
2. **Tipo de control y clase de resultado** en toda validación: `SINCRONO_DETERMINISTA` (G3; puede ser BLOQUEANTE) o `ASINCRONO` (auditoría; nunca bloquea, R17).
3. **Estados separados** en cada ciclo: proceso, guía, entrega y informe al operador.
4. **Sin credenciales ni datos personales**: en incidencias se registra el campo y el tipo, nunca el valor.
5. **Cola de tipo 3** recontada en cada informe; nada se pierde entre ciclos.
6. **Un ciclo sin hallazgos** es un resultado válido.
7. **Canales**: todo mensaje recibido por un canal no previsto (incluido cualquier intento de comunicación con el Bloque A general, el Bloque B o el usuario, o un informe transversal que llega a un Analista de segmento sin pasar por el Analizador) se registra como `INC-` de tipo CANAL_NO_PREVISTO.

## 4. Formato de entrada

Cada entrada tiene campos comunes `{id, tipo_entrada, fecha, autor AG-18, refs}` y un bloque específico.

### 4.1 Validación G3 (G3V-)

| Campo | Valores / formato |
|---|---|
| `g3v_id` | `G3V-AAAA-NNNN-ss` (ss = intento) |
| `run_id` | RUN-FX- |
| `tipo_control` / `clase_resultado` | SINCRONO_DETERMINISTA / BLOQUEANTE · ADVERTENCIA · NINGUNA |
| `dictamen_ht09` | APTO · APTO_CON_ADVERTENCIAS · BLOQUEADO |
| `comprobaciones` | `{id G3-EST-nn·G3-DAT-nn·G3-MET-nn·G3-CON-nn·G3-ENT-nn·G3-FX-nn, resultado PASA·FALLA·NO_APLICA, clase B·W, objeto, segmento, detalle}` |
| `excepcion` | `{recibida, dictamen_orquestador, motivo, condiciones_para_apto, advertencias, tiempo_dictamen_min, manual sí/no, comprobaciones_manuales (G3-FX no implementadas en HT-09)}` |
| `relanzamientos` | Lista de `g3v_id` posteriores |

### 4.2 Ciclo de auditoría (AUD-)

| Campo | Valores / formato |
|---|---|
| `audit_id` | `AUD-AAAA-NNNN` |
| `objeto` | RUN-FX- · QRY- · CT-21 |
| `ct16_msg_id` | — |
| `validacion_paquete` | `{resultado SUPERADA·CON_AVISOS·NO_SUPERADA, comprobaciones 1–8}` |
| `muestreo` | `{motivo OBLIGATORIO·ALEATORIO·SENAL_RIESGO, semilla_hash, senales (p. ej., opción REGIMEN, divisa con controles, contradicción entre segmentos, informe transversal ausente), profundidad COMPLETA·LIGERA}` |
| `comprobaciones_asincronas` | `{id AS-nn, resultado, evidencia}` |
| `coordinacion_auditor` | `{material_enviado (orden verificado), review_id, hallazgos_recibidos, discrepancias, ajustes_severidad, puntos_ciegos_declarados, perfil_revisor}` |
| `hallazgos` | Lista de HAL- |
| `guias_emitidas` | Lista de GUI- |
| `propuestas` | Lista de P3- |
| `versiones` | `{methodology_version (FX-x.y), guias_vigentes_del_agente}` |
| `estados_finales` | `{proceso COMPLETED·COMPLETED_WITH_LIMITATIONS·FAILED, guia ISSUED·SUPERSEDED·NONE, entrega CONFIRMED·PENDING·FAILED, informe_operador SENT·PENDING·FAILED}` |
| `limitaciones` | Texto |

### 4.3 Hallazgo (HAL-)

`hal_id` (`HAL-AAAA-NNNN`), `audit_id`, `objeto`, `agente` (AG-01…AG-21), `segmento` (si aplica), `regla_o_punto` (R1–R25, PR-xx, G3-xxx, AS-xx), `descripcion` (esperado / encontrado / efecto), `evidencia`, `reproducibilidad`, `origen` (G3 · ASINCRONO · AUDITOR · AUTOEVALUACION), `severidad` (Crítica · Material · Operativa · Menor), `severidad_propuesta_auditor`, `justificacion`, `alcance` (AFIRMACION · OPCION · RUN · AGENTE · SISTEMICO), `tipo_propuesta` (1 · 2 · 3), `estado` (ABIERTO · TRANSMITIDO · CORREGIDO · RECLASIFICADO · CERRADO_SIN_ACCION), `historial`.

Precedentes de severidad propios de divisas (vara inicial, revisable en el circuito de calibración CT-17): proponer un instrumento, coste, apalancamiento o nivel de entrada como opción → **Material** (R21); aplicar a un segmento el marco de otro sin justificación → **Material** (R21); par en notación invertida que llega a un entregable con dirección incoherente → **Material**; contradicción de signo en una divisa entre segmentos sin justificación → **Material**; anticipación en una fijación o en el posicionamiento usada en un pronóstico entregado → **Crítica** (R11, R18); omisión de la comparación con el paseo aleatorio en una métrica publicada → **Material** (R13).

### 4.4 Guía (GUI-)

`guia_id` (`GUI-AGnn-NNNN`), `agente`, `version`, `sustituye`, `fecha_aplicacion`, `items` `{item_id, tipo 1·2, origen HAL-·LEC-, que_cambia, donde_se_comprueba, como_se_sabe, caducidad}`, `acuse` (fecha), `estado` (ISSUED · SUPERSEDED · RETIRADA), `eficacia` `{tasa_antes, tasa_despues, ciclos, conclusion}`.

### 4.5 Orden de instancias (ORD-) y métricas de carga (CAR-)

- `ORD-`: `orden_id`, `agente` (solo agentes sin estado: AG-03 a AG-09, AG-21, AG-12 a AG-17; AG-10 y AG-11 admiten varias instancias), `accion` (ABRIR · CERRAR), `instancias_antes`, `instancias_despues`, `metricas_disparo` `{cola, W, rho, lambda, mu}`, `calculo` (c = ⌈λ/(μ·0,75)⌉), `vigencia`, `ejecutada_ht08` (sí/no).
- `CAR-`: instantánea periódica por agente: `cola`, `W_medio`, `W_p90`, `rho`, `instancias`, `encargos_completados`; para AG-09 y AG-21, además, `tiempo_hasta_informe` respecto del inicio de F1.

### 4.6 Autorización de presupuesto (AUT-)

`aut_id`, `run_id`, `solicitante`, `segmento_o_capa`, `presupuesto_base`, `ampliacion_uc`, `cpi`, `eac`, `valor_informacion` (qué decisión puede cambiar), `decision` (AUTORIZADA · DENEGADA), `condiciones`, `motivo`.

### 4.7 Paquete de mantenimiento de conocimiento (MAN-)

`man_id`, `archivo` (F7 · F8 · F9), `emisor` (AG-14 · AG-15 · AG-16), `periodo`, `altas`, `reparaciones`, `degradaciones`, `bajas` (n y verificación muestral del Registro de bajas), `salud_enlaces` (% OK y por estado), `cobertura_tematica` (por área TX-01…TX-14, TMX-01…TMX-09 o TFX-01…TFX-10), `distribucion_niveles`, `lagunas`, `avisos_curador`, `comprobaciones_muestrales` `{bajas_con_linea, verificaciones_recientes, orden_por_Q}`, `evaluacion` (SANA · CON_AVISOS · DEFICIENTE), `hallazgos`.

### 4.8 Propuesta de tipo 3 (P3-), incidencia (INC-), revisión trimestral (TRI-), corrección (COR-)

- `P3-`: `p3_id`, `origen` (ORQ · AUD · EVAL · agente), `objeto`, `evidencia`, `impacto`, `pruebas_regresion` (IDs del Plan de pruebas del Bloque A Forex), `plan_reversion`, `npr` (FMEA), `estado` (PENDING_OPERATOR · APROBADA · RECHAZADA · APLICADA), `antiguedad_dias`, `decision_operador` `{fecha, texto, propagacion}`.
- `INC-`: `inc_id`, `tipo` (SEGURIDAD · MANIPULACION · CANAL_NO_PREVISTO · ACCESO_FUERA_DE_MATRIZ · HERRAMIENTA · ESCRITURA · OTRO), `severidad`, `objeto`, `campo_afectado` (sin el valor), `tratamiento`, `escalado_operador`.
- `TRI-`: `tri_id`, `trimestre`, `participantes`, `dossier` (referencias), `decisiones`, `acciones` `{accion, dueño, fecha}`.
- `COR-`: `cor_id`, `entrada_corregida`, `motivo`, `comunicado_a`.

## 5. Estados y transiciones

| Objeto | Transiciones |
|---|---|
| HAL- | ABIERTO → TRANSMITIDO → CORREGIDO · CERRADO_SIN_ACCION; ABIERTO → RECLASIFICADO (tipo 3) |
| GUI- | ISSUED → SUPERSEDED (nueva versión) · RETIRADA (caducidad o ineficacia) |
| P3- | PENDING_OPERATOR → APROBADA → APLICADA; PENDING_OPERATOR → RECHAZADA |
| ORD- | EMITIDA → EJECUTADA · FALLIDA |
| AUD- | ABIERTO → CERRADO (con estados finales separados) |

## 6. Índices de consulta

| Índice | Clave | Uso |
|---|---|---|
| G3 por comprobación | `comprobaciones.id`, resultado | Gráfico p de fallos; FMEA (incluidas las G3-FX) |
| G3 por segmento | `comprobaciones.segmento` | Segmentos con más fallos; guías a su Analista |
| Excepciones G3 | `excepcion.recibida` | Tiempos de dictamen |
| Hallazgos por agente, regla y severidad | `agente`, `regla_o_punto`, `severidad` | Pareto; guías; lecciones de nivel A |
| Precedentes de severidad | Tipo de defecto → severidad | Vara estable |
| Guías vigentes por agente | `estado` = ISSUED | Lectura en F0 de cada agente |
| Cola de tipo 3 | `estado` = PENDING_OPERATOR, antigüedad | Informe al operador |
| Carga | CAR- por agente y fecha | Cuellos de botella (incluida la puntualidad de las capas transversales) |
| Salud del conocimiento | MAN- por archivo y área | Revisión trimestral |

## 7. Ejemplo ficticio

> **EJEMPLO FICTICIO — no es una entrada real.**

```json
{"g3v_id":"G3V-2026-0001-01","run_id":"RUN-FX-2026-0001","tipo_control":"SINCRONO_DETERMINISTA","clase_resultado":"BLOQUEANTE","dictamen_ht09":"BLOQUEADO",
 "comprobaciones":[{"id":"G3-FX-01","resultado":"FALLA","clase":"B","objeto":"OPP-FX-2026-0011","segmento":"G10N","detalle":"par «JPY/USD» fuera de convención de mercado; `direccion` ALCISTA_BASE con la base (JPY) en lado CORTO de la composición"},
   {"id":"G3-CON-10","resultado":"PASA","clase":"B","objeto":"OPP-FX-2026-0007.horizontes.H3","segmento":"G10N","detalle":"sin probabilidad publicada; banda y etiqueta «sin ventaja demostrada frente al paseo aleatorio» presentes"}],
 "excepcion":{"recibida":"2026-11-07T18:20:00+01:00","dictamen_orquestador":"BLOQUEADO","motivo":"R21: notación y dirección incoherentes en una opción del top-3",
   "condiciones_para_apto":["Reescribir la opción como «USD/JPY bajista (BAJISTA_BASE)» con JPY LARGO / USD CORTO, recalcular las invalidaciones con el Motor y relanzar HT-09"],
   "advertencias":[],"tiempo_dictamen_min":4,"manual":false,"comprobaciones_manuales":[]},
 "relanzamientos":["G3V-2026-0001-02"]}
```
