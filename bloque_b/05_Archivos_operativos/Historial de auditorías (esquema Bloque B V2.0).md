# Esquema de archivo operativo — HA Historial de auditorías

**Bloque B · Robot Investor · Versión óptima V2.0 · 03/11/2026** · Subordinado al Documento 0 del Bloque B óptima V2.0 (ante discrepancia, manda el Documento 0).

---

## 1. Propósito

El Historial de auditorías (HA) es el registro único del **control de calidad, del control de tiempo y del gobierno operativo** del Bloque B (Documento 0, 5.1): validaciones deterministas G3 (HT-09) del paquete de síntesis y de la fidelidad de los entregables; ciclos de **auditoría experta previa a la salida** con sus vueltas de subsanación, hallazgos y severidades; **autorizaciones de contenido y de salida** (con reservas o bloqueos); **avisos de tiempo y puntos de control** emitidos al Coordinador (CT-B-27); guías de mejora; órdenes de escalado por instancias y métricas de carga; paquetes de mantenimiento del conocimiento; incidencias; conflictos de normas; propuestas de tipo 3; y revisiones trimestrales. Lo usa el Evaluador como materia prima del aprendizaje operativo y el operador como base de sus decisiones.

## 2. Propietario, lectores y contratos

| Aspecto | Contenido |
|---|---|
| Propietario de escritura | AG-B21 Orquestador técnico (único; los resultados automáticos de HT-09 y las métricas de HT-08 se registran bajo su propiedad) |
| Lectores | AG-B21, AG-B22 Auditor, AG-B23 Evaluador; AG-B02 Director (extractos: G3, hallazgos y guías de sus peticiones) |
| Contratos | CT-B-18 (validación G3), CT-B-19 (auditoría previa y calibración de severidades), CT-B-21 (guías y órdenes de instancias), CT-B-22 (lecciones y propuestas del Evaluador), CT-B-24 (mantenimiento del conocimiento), CT-B-27 (avisos de tiempo), CT-B-14 (re-ejecuciones pedidas por el Orquestador o el Auditor) |
| Herramientas | HT-09, HT-08, HT-07, HT-03 |

## 3. Reglas

1. **Append-only**: los cambios de estado de hallazgos, guías y propuestas son entradas nuevas; las correcciones del propio proceso referencian la entrada original (`COR-B`).
2. **Separación de funciones** (R19): HT-09 dictamina; el Auditor **hallazga y propone severidad, no edita ni bloquea**; el Orquestador decide la **autorización de contenido** (F8) y la **autorización de salida** (F9); el Director subsana. En N2 y N3 ninguna salida sin auditoría previa; en N1, según el muestreo del Anexo A.
3. **Bucle de subsanación** (7.4, F8; 11.3): cada vuelta registra hallazgo, corrección, evidencia y versión nueva del paquete; tras **tres vueltas** sin convergencia, el Orquestador decide autorizar con **reserva de auditoría** (solo si lo abierto es Material y no afecta a la tesis central, al veredicto ni a candidatos prioritarios) o **bloquear** (`BLOQUEADO_AUDITORIA`). El tiempo del bucle cuenta para la puerta de tiempo.
4. **Muestreo de N0** (Anexo A, 10 %): la revisión de una respuesta N0 seleccionada es **posterior** a su envío (el objetivo N0 es < 2 min); un hallazgo genera guía al Coordinador, nunca la retirada de la respuesta, y si afecta a una cifra se comunica una aclaración por CT-B-03 a iniciativa del Coordinador. (Anexo A.2 del Documento 0: la revisión por muestreo de N0 es posterior a la respuesta.)
5. **Sin credenciales ni datos personales**: en incidencias se registra el campo y el tipo, nunca el valor (R10, R11).
6. **Cola de tipo 3** recontada en cada informe al operador; nada se pierde entre periodos.
7. **Una auditoría sin hallazgos** es un resultado válido.
8. **Prefijos internos** del archivo: `G3V-B` validación, `AUD-B` ciclo de auditoría, `HAL-B` hallazgo, `AUTC-B` autorización de contenido, `AUTS-B` autorización de salida, `AVT-B` aviso de tiempo, `GUI-B` guía, `ORD-B` orden de instancias, `CAR-B` métricas de carga, `MAN-B` paquete de mantenimiento, `INC-B` incidencia, `CNF-B` conflicto de normas, `P3-B-<emisor>` propuesta de tipo 3 (emisor ORQ, AUD o EVAL; la del Evaluador conserva su identificador de F5), `TRI-B` revisión trimestral, `COR-B` corrección.

## 4. Formato de entrada

Cada entrada tiene los campos comunes `{id, tipo_entrada, fecha, autor AG-B21, refs}` y un bloque específico.

### 4.1 Validación G3 (G3V-B)

| Campo | Valores / formato |
|---|---|
| `g3v_id` | `G3V-B-AAAA-NNNN-ss` (ss = intento) |
| `pet_id` / `run_id` | — |
| `pasada` | PAQUETE_SINTESIS (F8) · FIDELIDAD_ENTREGABLES (F9) · EN_SECO (invocada por el Director) |
| `dictamen_ht09` | APTO · APTO_CON_ADVERTENCIAS · BLOQUEADO |
| `comprobaciones` | `{id G3B-xxx-nn (catálogo del Plan de pruebas del Bloque B, sección 3), resultado PASA·FALLA·NO_APLICA (motivo), clase B·W, objeto, detalle}` |
| `modo` | AUTOMATICO · MANUAL (herramienta caída, etiquetado; nunca APTO por defecto) |
| `tiempo_dictamen_min` | — |
| `relanzamientos` | `g3v_id` posteriores |

### 4.2 Ciclo de auditoría previa (AUD-B)

| Campo | Valores / formato |
|---|---|
| `aud_id` | `AUD-B-AAAA-NNNN` |
| `pet_id` / `run_id` / `query_id` | — |
| `motivo` | OBLIGATORIO (N2, N3, PERS > 10 min) · MUESTREO (N1, N0, PERS ≤ 10 min) con `semilla_hash` · SENAL_RIESGO |
| `focos_prioritarios` | Focos 1–10 de 11.2 ordenados por riesgo |
| `material_enviado` | `{msg_id_ct19, paquete_version, g3v_id}` |
| `vueltas` | `[{n, hallazgos HAL-B, recomendacion_auditor AUTORIZAR·SUBSANAR·RESERVA·BLOQUEAR, correcciones_director [{hal_id, agente_que_corrige, evidencia, version_nueva}], g3v_relanzamiento, minutos}]` |
| `desenlace` | AUTORIZADO · AUTORIZADO_CON_RESERVA · BLOQUEADO |
| `reservas` | `{hal_id, texto_para_entregables, motivo_no_central}` |
| `minutos_totales` | Cuenta para la puerta de tiempo |
| `calibracion_severidades` | `{discrepancias_auditor_orquestador, ajustes, precedente_aplicado}` |
| `puntos_ciegos_declarados` | Texto del Auditor |

### 4.3 Hallazgo (HAL-B)

`hal_id`, `aud_id`, `foco` (1–10 de 11.2), `objeto` (afirmación · cifra · dimensión · candidato · universo · veredicto · entregable), `agente_responsable`, `regla_o_punto` (R1–R32, PA/PC, G3B-xxx, foco), `descripcion` (esperado / encontrado / efecto), `evidencia`, `reproducibilidad` (re-ejecución CT-B-14 si procede), `origen` (G3 · AUDITOR · AUTOEVALUACION · VIGIA), `severidad_propuesta` (Auditor), `severidad` (decidida: Crítica · Material · Operativa · Menor), `justificacion`, `afecta_a` `{tesis_central, veredicto, candidatos_prioritarios, topN}`, `correccion_propuesta`, `tipo_propuesta` (1 · 2 · 3), `estado` (ABIERTO · EN_SUBSANACION · CORREGIDO · RESERVA · RECLASIFICADO · CERRADO_SIN_ACCION), `historial`.

### 4.4 Autorización de contenido (AUTC-B) o de salida (AUTS-B)

`autc_id` (`AUTC-B-AAAA-NNNN`, tipo CONTENIDO) o `auts_id` (`AUTS-B-AAAA-NNNN`, tipo SALIDA), `pet_id`, `run_id`, `tipo` (CONTENIDO · SALIDA), `base` (`{g3v_id, aud_id, desenlace}`), `condiciones` (sin Críticos ni Materiales abiertos; o reserva motivada), `reservas`, `decision` (AUTORIZADA · AUTORIZADA_CON_RESERVA · BLOQUEADA), `motivo`, `fecha`. Sin `AUTS-B` no hay publicación en ENT ni CT-B-02 (salvo el CT-B-02 de estado `BLOQUEADO_AUDITORIA` con opciones). La autorización de salida llega al Coordinador en el retorno del CT-B-08 del Director, que cita el identificador AUTS-B.

### 4.5 Aviso de tiempo y punto de control (AVT-B)

`avt_id`, `pet_id`, `run_id`, `msg_id_ct27`, `disparador` (PT30_EN_EJECUCION · PTA), `minutos_consumidos`, `proyeccion` `{p50, p80, modelo MOD-B}`, `umbral` (30 · autorizado + margen P-B-02), `nodos_pendientes`, `checkpoint_id` (CKP-) y `momento_detencion` (fin de fase · informe dimensional · informe de selección · vuelta de auditoría), `hecho_hasta_ahora`, `aut_id` resultante (F1), `nodos_en_curso_al_aviso` (deben completarse antes de detener: nunca a mitad de un cálculo o de una escritura).

### 4.6 Guía (GUI-B), orden de instancias (ORD-B) y carga (CAR-B)

- `GUI-B`: `guia_id` (`GUI-B-<agente>-NNNN`), `agente`, `version`, `sustituye`, `fecha_aplicacion`, `items` `{item_id, tipo 1·2, origen HAL-B·LEC-B·RND-B, que_cambia, donde_se_comprueba, como_se_sabe, caducidad}`, `acuse`, `estado` (EMITIDA · SUSTITUIDA · RETIRADA), `eficacia` `{tasa_antes, tasa_despues, peticiones, conclusion}`.
- `ORD-B`: `orden_id`, `agente`, `accion` (ABRIR · CERRAR), `instancias_antes`, `instancias_despues`, `metricas_disparo` `{cola, tiempo_respuesta, objetivo}` (umbral P-B-47), `restriccion` (agente con estado por petición o de instancia única: no se escala, se reordena la cola), `ejecutada_ht08`.
- `CAR-B`: instantánea por agente: `cola`, `t_respuesta_medio`, `t_respuesta_p90`, `instancias`, `encargos_completados`; para AG-B23, además `fraccion_tiempo_vigia` y `rec_vigentes_en_vigilancia` (criterio de separación P-B-43).

### 4.7 Mantenimiento del conocimiento (MAN-B)

`man_id`, `archivo` (F7 · F8 · F9 · FM), `emisor` (AG-B18 · AG-B19 · AG-B20), `periodo`, `altas`, `reparaciones`, `degradaciones`, `bajas` (con verificación muestral del «Registro de bajas»), `salud_enlaces` (% por estado HT-02), `cobertura_por_area` (≥ 20 verificadas por área), `distribucion_niveles`, `lagunas`, `avisos_curador` (`fuente_retirada`), `fuentes_que_requieren_clave`, `evaluacion` (SANA · CON_AVISOS · DEFICIENTE), `hallazgos`.

### 4.8 Incidencia (INC-B), conflicto (CNF-B), propuesta de tipo 3 (P3-B), revisión trimestral (TRI-B), corrección (COR-B)

- `INC-B`: `inc_id`, `tipo` (SEGURIDAD · CREDENCIAL_FUERA_DE_BOVEDA · DATOS_PERSONALES · MANIPULACION · CANAL_NO_PREVISTO · ACCESO_FUERA_DE_MATRIZ · HERRAMIENTA · ESCRITURA · ANALISIS_SIN_PETICION · OTRO), `severidad`, `origen` (F1 `MENSAJE_RECHAZADO`, F2 alerta de procedencia, HT-09, agente), `objeto`, `campo_afectado` (sin el valor), `tratamiento`, `escalado_operador`, `aviso_broker` (revocación de clave, 17.2).
- `CNF-B`: `cnf_id`, `normas_en_conflicto` (con su rango de 0.2), `regla_aplicada_provisional` (la más restrictiva, R27), `afectados`, `escalado`, `resolucion`.
- `P3-B`: `p3_id`, `emisor`, `objeto`, `evidencia`, `impacto`, `pruebas_regresion` (identificadores del Plan de pruebas), `plan_reversion`, `estado` (PENDIENTE_OPERADOR · APROBADA · RECHAZADA · APLICADA), `antiguedad_dias`, `decision_operador` `{fecha, texto, propagacion}`.
- `TRI-B`: `tri_id`, `trimestre`, `participantes` (Orquestador, Evaluador, operador), `dossier` (calibración y certificados, rendimiento de rankings, modelo de tiempos y uso de la puerta de tiempo, carga y cuellos, salud del conocimiento, criterio de separación del Vigía, cola de tipo 3), `decisiones`, `acciones` `{accion, dueño, fecha}`.
- `COR-B`: `cor_id`, `entrada_corregida`, `motivo`, `comunicado_a`.

## 5. Estados y transiciones

| Objeto | Transiciones |
|---|---|
| HAL-B | ABIERTO → EN_SUBSANACION → CORREGIDO · RESERVA · CERRADO_SIN_ACCION; ABIERTO → RECLASIFICADO (tipo 3) |
| AUD-B | ABIERTO → (vueltas 1–3) → AUTORIZADO · AUTORIZADO_CON_RESERVA · BLOQUEADO |
| AUTC-B · AUTS-B | Final al registrarse |
| GUI-B | EMITIDA → SUSTITUIDA · RETIRADA |
| P3-B | PENDIENTE_OPERADOR → APROBADA → APLICADA; PENDIENTE_OPERADOR → RECHAZADA |
| ORD-B | EMITIDA → EJECUTADA · FALLIDA |

## 6. Índices de consulta

| Índice | Clave | Uso |
|---|---|---|
| G3 por comprobación | `comprobaciones.id`, `resultado` | Fallos recurrentes; guías; tipo 3 |
| Auditorías por petición | `pet_id` | Informe técnico (estado de auditoría); N0 de estado |
| Hallazgos por agente, foco y severidad | `agente_responsable`, `foco`, `severidad` | Pareto; guías; lecciones operativas |
| Reservas y bloqueos | `desenlace` | Revisión trimestral; aprendizaje |
| Avisos de tiempo | `AVT-B` por petición | Uso de la puerta de tiempo; modelo de tiempos |
| Guías vigentes por agente | `estado` = EMITIDA | Lectura al inicio de cada encargo |
| Cola de tipo 3 | `estado` = PENDIENTE_OPERADOR | Informe al operador |
| Carga | `CAR-B` por agente y fecha | Cuellos de botella; separación del Vigía |
| Incidencias | `INC-B.tipo`, `severidad` | Seguridad; informe al operador |

## 7. Ejemplo ficticio

> **EJEMPLO FICTICIO — no es una entrada real.**

```json
{"aud_id":"AUD-B-2026-0005","pet_id":"PET-B-2026-0007","run_id":"RUN-B-2026-0007-01","motivo":"OBLIGATORIO","focos_prioritarios":[8,1,5],
 "material_enviado":{"msg_id_ct19":"MSG-B-2026-11-10-0410","paquete_version":"v1","g3v_id":"G3V-B-2026-0006-01"},
 "vueltas":[{"n":1,"hallazgos":["HAL-B-2026-0011"],"recomendacion_auditor":"SUBSANAR",
   "correcciones_director":[{"hal_id":"HAL-B-2026-0011","agente_que_corrige":"AG-B12","evidencia":"universo RF rehecho con 4 emisiones amortizadas en 2025 incluidas","version_nueva":"v2"}],
   "g3v_relanzamiento":"G3V-B-2026-0006-02","minutos":7}],
 "desenlace":"AUTORIZADO","reservas":[],"minutos_totales":11,
 "calibracion_severidades":{"discrepancias_auditor_orquestador":0,"ajustes":[],"precedente_aplicado":"universo con sesgo de supervivencia en un tipo con prioritarios = Material"},
 "puntos_ciegos_declarados":"No se re-ejecutó el DCF inverso del agregado (sin cambio desde la auditoría de PET-B-2026-0003)"}
```
