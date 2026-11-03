# Esquema de archivo operativo — F1 Registro de peticiones y ejecuciones

**Bloque B · Robot Investor · Versión óptima V2.0 · actualizado V2.1, 03/11/2026** · Subordinado al Documento 0 del Bloque B óptima V2.1 (ante discrepancia, manda el Documento 0).

---

## 1. Propósito

F1 es la **memoria episódica del servicio** del Bloque B (Documento 0, secciones 5.1 y 15; R28). Registra cada petición del Broker (PET-B) desde su recepción hasta su entrega o cierre; cada ejecución (RUN-B) con sus tiempos y consumos por fase y sus puntos de control (CKP-); cada **autorización de la puerta de tiempo** (AUT-B), con su justificación aunque la autorización sea automática; cada **solicitud de credencial** (CRED-B), sin la clave; cada consulta y su respuesta (QRY-B); cada alerta del Vigía transmitida al Broker (ALR-B); desde la V2.1, cada **consulta del bloque al Broker** y cada aporte del Broker (CNS-B, CT-B-28), cada **puerta de viabilidad** PV1–PV3 evaluada, cada **parada en puerta** con su informe de parada y cada **continuación forzada**, y cada ejecución de un **ciclo de seguimiento encargado** (RUN-B del ciclo; el encargo y el ciclo viven en el archivo F11); y cada decisión, resultado, valoración o cambio de configuración comunicado por el Broker (RET-B).

Sirve para: (a) consultar en F0 los análisis previos del mismo ámbito y los candidatos ya enviados a los Bloques C.x; (b) responder consultas N0 de estado; (c) alimentar el **modelo de tiempos** del Evaluador (estimación frente a real por nodo y fase); (d) rendir cuentas del uso de la puerta de tiempo; (e) reconstruir cualquier petición sin preguntar a nadie.

**No es**: un registro de evidencia (F2), de conclusiones analíticas (F3), de pronósticos (F4) ni de control de calidad (HA). Los referencia por identificador. **Nunca contiene una clave API, un dato personal, la cartera ni el perfil del inversor** (R10, R11, 5.2.4).

## 2. Propietario, lectores y contratos

| Aspecto | Contenido |
|---|---|
| Propietario de escritura | AG-B01 Coordinador de Peticiones y Consultas (único; instancia única con cola, 4.5) |
| Lectores | Todos los agentes (matriz 5.1); el Orquestador lo recorre con HT-06 para registrar en HA las incidencias de entrada |
| Contratos que lo alimentan | CT-B-01 (petición y acuse), CT-B-02 (entrega), CT-B-03 (consulta y respuesta), CT-B-04 (decisiones, resultados, valoraciones y configuración), CT-B-05 (autorizaciones), CT-B-06 (credenciales), CT-B-07 (alertas transmitidas), CT-B-08 (orden de análisis, estados por fase y retorno), CT-B-25 (aviso del Vigía recibido), CT-B-26 (aviso al Evaluador, por referencia), CT-B-27 (aviso de tiempo recibido) |
| Herramientas | HT-05 (recordatorios de autorizaciones pendientes y de caducidad de credenciales), HT-06 (índice), HT-08 (tiempos, consumo y proyección), HT-01 (solo estado de credenciales en la bóveda) |

## 3. Reglas

1. **Append-only en lo sustantivo** (R28; 5.2.1). Los cambios de estado son entradas nuevas del `historial` de cada registro; una corrección referencia la entrada corregida (`supersedes`). Solo se suprime lo que indique la retención del Anexo A (F1: indefinida).
2. **Toda petición se registra**, también las rechazadas en la admisión, las vinculadas a otra idéntica en curso, las canceladas, las caducadas y las bloqueadas por auditoría. Un rechazo no es un fallo (7.4, F0.2).
3. **La justificación de la puerta de tiempo se registra siempre** (R20): con decisión del Broker, con política automática (`AUTORIZACION_AUTOMATICA_NOTIFICADA`) y en los N3 solicitados expresamente, cuya justificación se genera en F0.
4. **Sin claves** (R10; 5.2.4): de una credencial solo constan la solicitud, su estado, el alias `credencial_ref` y su caducidad. Si un mensaje entrante contiene una clave, un dato personal o la cartera del usuario, el mensaje se **rechaza íntegro**: F1 registra un `MENSAJE_RECHAZADO` con el campo afectado y el tipo de dato, **nunca el valor** (6.2.5; 17.2).
5. **Petición íntegra sin datos sensibles**: se conserva el CT-B-01 tal como llegó (con su `paquete_para_bloque_B`, tratado como contenido transportado, R12, R31) y su hash; la copia normalizada es la que circula por CT-B-08.
6. **Una petición, un análisis** (R5, R6): cada PET-B tiene su propio plan, sus propias ejecuciones y sus propias autorizaciones; la relación con otras peticiones solo puede ser `vinculada_a` (idempotencia, 6.2.2) o `referencia_previa` (análisis ya entregado).
7. **Tiempo y consumo por fase** (10.3): cada RUN-B registra minutos y UC por fase y por agente con HT-08; la entrega muestra estimación p80 frente a real.
8. **Preguntas repetidas** (7.7.4): cada QRY-B lleva `tema_normalizado`; al alcanzar el umbral del Anexo A (3 veces en 4 semanas) el Coordinador avisa al Evaluador (CT-B-26, `PREGUNTA_REPETIDA`) y lo anota.
9. **Configuración**: los cambios pedidos por CT-B-04 se registran aquí (RET-B) con lo aplicado y lo rechazado; el valor vigente vive en F10 (registro CFG-B). F1 conserva la petición del cambio; F10, el valor.
11. **Consultas al Broker (V2.1, 7.12; R34)**: solo el Coordinador envía (CT-B-28), tras el filtro del Director; cada CNS-B registra pregunta, origen, tipo, modo, plazo, supuesto declarado, respuesta o supuesto aplicado y efecto. Límites por petición (Anexo A): N1 1 · N2 3 · N3 6 · ciclo N1-SEG 1; BLOQUEANTES como máximo 1 (N3: 2). Plazos: BLOQUEANTE 4 h (recordatorio a las 2 h); NO_BLOQUEANTE hasta el inicio de F8 o 48 h. Las consultas que contendrían datos personales, cartera o perfil se descartan antes del envío (R11).
12. **Capas y puertas (V2.1, 7.10; R33)**: cada RUN-B registra tiempo y consumo **por capa** (0–4) además de por fase, y cada puerta PV1–PV3 evaluada (resultado, criterios, insumos); una parada registra el informe de parada y deja la petición `DETENIDA_EN_PUERTA` durante el plazo para forzar la continuación (7 días).
10. **Prefijos internos**: además de los del Anexo C (PET-B, RUN-B, QRY-B, AUT-B, CRED-B, CKP-, ALR-B, POL-), este archivo usa `RET-B-` para las comunicaciones del Broker por CT-B-04 (decisiones, resultados, valoraciones y configuración), prefijo interno del archivo.

## 4. Formato de entrada

Cada registro lleva los campos comunes `{tipo_registro, id, fecha_registro, autor AG-B01, msg_ids, historial[]}`. Fechas en ISO 8601 con zona horaria IANA del bloque.

### 4.1 Petición (PET-B)

| Campo | Tipo | Oblig. | Valores / formato | Descripción |
|---|---|---|---|---|
| `pet_id` | Identificador | Sí | `PET-B-AAAA-NNNN` | Clave |
| `pet_ref_broker` | Texto | Sí | Referencia del Broker | Correlación externa |
| `msg_id_ct01` | Texto | Sí | — | Mensaje CT-B-01 de origen |
| `fecha_recepcion` | Fecha-hora | Sí | ISO 8601 | — |
| `origen` | Enumerado | Sí | BLOQUE_A · LIBRE | — |
| `opp_id_A` | Texto | Si BLOQUE_A | `OPP-…` del Bloque A | Referencia de origen (Anexo C: nunca se reutiliza como identificador del Bloque B) |
| `peticion_original` | Objeto | Sí | CT-B-01 íntegro (B.1) | Conservado como contenido transportado |
| `hash_peticion` | Texto | Sí | SHA-256 | Idempotencia y detección de duplicados |
| `validacion_paquete_A` | Objeto | Si BLOQUE_A | `{esquema OK·INCOMPLETO·INVALIDO, campos_faltantes[], instrucciones_detectadas sí/no, tratamiento}` | Validación contra el Anexo B y E.2 del Documento 0 |
| `peticion_normalizada` | Objeto | Sí | `{objeto, tipo_objeto_sugerido, ambito {incluye, excluye, region}, tipos_activo_admitidos[], horizontes[], preguntas[], preguntas_para_B[], marco_invertibilidad, top_n, alto_impacto, prioridad, fecha_objetivo, idioma_usuario}` | Lo que viaja en CT-B-08 |
| `admision` | Objeto | Sí | `{resultado ADMITIDA·RECHAZADA, motivo (Anexo D.5), bloque_c_sugerido, reformulacion_propuesta, preguntas_aclaracion[], justificacion}` | 7.4, F0.2 |
| `vinculada_a` | Identificador | No | PET-B en curso idéntica | 6.2.2 |
| `solapadas_en_curso` | Lista | No | PET-B con ámbito solapado | Solo información; no se comparten conclusiones (R6) |
| `referencia_previa` | Identificador | No | REC-B · PET-B | Análisis entregado que se toma como memoria |
| `nivel` | Objeto | Sí | `{solicitado N1·N2·N3·PERS·AUTO, propuesto, criterio_auto (regla del Anexo A aplicada), final, limite {minutos, uc}}` | 7.2 |
| `estimacion_inicial` | Objeto | Sí si ADMITIDA | `{minutos_p50, minutos_p80, uc_p50, uc_p80, version_modelo_tiempos (MOD-B de F5), plan_ref PLAN-B, desglose_por_fase}` | 9.9; la puerta usa el p80 |
| `requiere_autorizacion` | Booleano | Sí | — | p80 > 30 min o > límite PERS |
| `aut_ids` | Lista | No | AUT-B | Autorizaciones de la petición |
| `minutos_autorizados_vigentes` | Número | Sí | — | Tiempo autorizado acumulado |
| `cred_ids` | Lista | No | CRED-B | Credenciales solicitadas por esta petición |
| `run_ids` | Lista | Sí | RUN-B | Ejecuciones encadenadas |
| `fases_division` | Lista | Si DIVIDIDA | `{fase_n, contenido, run_id, estado, entregable_intermedio}` | Opción (c) de 9.9 |
| `estado` | Enumerado | Sí | Sección 5.1 | Estado vigente |
| `entrega` | Objeto | Si ENTREGADA, DETENIDA_EN_PUERTA o BLOQUEADO_AUDITORIA | `{msg_id_ct02, fecha, rutas_ENT {informe_tecnico, informe_visual, paquete_json, memorando, anexo_datos, mapa_eslabones (md, docx, json)} o {informe_parada (md, json)}, puertas_viabilidad, supuestos_aplicados, por_capa_min, resumen (B.2), estado_g3, auditoria {realizada, reservas[]}, auts_id (AUTS-B de HA, citado por el Director en el retorno del CT-B-08)}` | CT-B-02 |
| `rec_id` | Identificador | Si ENTREGADA | REC-B | Alta del Director en F3 |
| `tiempo_total` | Objeto | Sí al cierre | `{estimado_p80_min, autorizado_min, real_min, desviacion_pct}` | Alimenta el modelo de tiempos |
| `consumo_total_uc` | Número | Sí al cierre | — | Sin techo, siempre registrado (7.2) |
| `limitaciones` / `incidencias` | Listas | Sí | Texto o identificadores INC-B de HA | Vacío declarado |

### 4.2 Ejecución (RUN-B)

| Campo | Tipo | Oblig. | Valores / formato | Descripción |
|---|---|---|---|---|
| `run_id` | Identificador | Sí | `RUN-B-AAAA-NNNN-rr` (rr = reanudación o fase) | Clave |
| `pet_id` | Identificador | Sí | PET-B | Petición |
| `tipo` | Enumerado | Sí | INICIAL · REANUDACION · FASE_DIVIDIDA | 2.4 |
| `msg_id_ct08` | Texto | Sí | — | Orden de análisis |
| `checkpoint_entrada` | Identificador | Si REANUDACION | CKP- | Punto desde el que se reanuda |
| `plan_ref` | Identificador | Sí | `PLAN-B-…-vN` | Versión del plan (F3) |
| `nivel` / `minutos_autorizados` / `uc_autorizadas` | Enumerado / números | Sí | — | Heredados por los encargos internos (6.2.4) |
| `methodology_version` | Texto | Sí | Vigente en F10 al inicio | Se conserva hasta el final de la ejecución |
| `fases` | Lista | Sí | `{fase F0…F10, capa 0…4, inicio, fin, minutos, uc, estado COMPLETA·PARCIAL·EN_PAUSA·NO_INICIADA, gc (GC0…GC3 con resultado y motivo)}` | Tiempo y consumo por fase |
| `por_capa` | Objeto | Sí (V2.1) | `{"0": {minutos, uc}, … "4": {…}}` frente a la estimación por capa | Recalibración del modelo de tiempos por capa (12.7) |
| `puertas_viabilidad` | Lista | Sí (V2.1) | Identificadores de las entradas PUERTA_VIABILIDAD (4.9) | 7.10 |
| `consumo_por_agente` | Lista | Sí | `{agente AG-B…, instancias, encargos, minutos, uc}` | 10.3 |
| `puntos_control` | Lista | Sí | `{checkpoint_id CKP-, fase, nodo, fecha, estado_registrado sí, reanudable sí, motivo FIN_FASE·INFORME_DIMENSIONAL·INFORME_SELECCION·VUELTA_AUDITORIA·PT30·PTA}` | 9.9 |
| `avisos_tiempo` | Lista | No | `{msg_id_ct27, fecha, minutos_consumidos, proyeccion_p50_p80, umbral 30·autorizado, nodos_pendientes}` | CT-B-27 recibidos |
| `g3` | Objeto | Sí si llegó a F8 | `{g3v_ids[], dictamen_final APTO·APTO_CON_ADVERTENCIAS·BLOQUEADO}` | Referencias a HA |
| `auditoria` | Objeto | Si aplica | `{aud_id, obligatoria sí/no (N2/N3) o muestreo, vueltas, reservas[], resultado}` | Referencias a HA |
| `autorizacion_contenido` / `autorizacion_salida` | Identificador | Si aplica | AUTC-B / AUTS-B (HA), citados por el Director en el retorno del CT-B-08 | F8 y F9 |
| `estado` | Enumerado | Sí | COMPLETO · PARCIAL · SIN_RESULTADO · RECHAZADO · EN_PAUSA | 6.2.6 |
| `limitaciones` / `incidencias` | Listas | Sí | — | Estados degradados declarados (17.6) |

### 4.3 Autorización de la puerta de tiempo (AUT-B)

Contiene íntegros los dos mensajes de B.5 (solicitud o notificación, y decisión) más los campos de gestión:

| Campo | Tipo | Oblig. | Valores / formato |
|---|---|---|---|
| `aut_id` | Identificador | Sí | `AUT-B-AAAA-NNNN` |
| `pet_id` / `run_id` | Identificadores | Sí | — |
| `tipo` | Enumerado | Sí | SOLICITUD · AUTORIZACION_AUTOMATICA_NOTIFICADA · JUSTIFICACION_N3_EXPRESO |
| `puerta` / `momento` | Enumerados | Sí | PT30 · PTA / PREVIO_F0 · EN_EJECUCION |
| `punto_control` | Objeto | Si EN_EJECUCION | `{checkpoint_id, fase, nodo}` |
| `hecho_hasta_ahora` | Objeto | Sí | `{fases_cerradas, conclusiones_provisionales, minutos_consumidos, uc_consumidas}` |
| `estimacion` | Objeto | Sí | `{minutos_p50, minutos_p80, uc_p50, uc_p80, desglose_por_fase, desglose_por_capa, minutos_p80_hasta_pv2}` |
| `justificacion` | Objeto | Sí | `{que_aporta, incertidumbres_que_reduce [{incertidumbre, efecto_posible}], que_se_perderia, relevancia_decisional}` — insumos del Director y del Orquestador (CT-B-27) |
| `opciones` | Lista | Sí | Las cinco de 9.9 con su contenido (CONTINUAR · VERSION_30_MIN · DIVIDIR · **HASTA_PV2** (V2.1: solo capas 0–2 y nueva decisión con el resultado de PV2) · CANCELAR); la (b) declara lo que se recorta y su efecto en E y en el veredicto máximo; nunca recorta controles (R23) |
| `recomendacion_bloque` | Objeto | Sí | `{opcion, motivo}` |
| `politica_aplicada` | Objeto | Sí | `{regla_id POL-, resultado AUTORIZA·NO_CUBRE·SUPERA_TOPE}` |
| `decision` | Objeto | Si decidida | `{opcion, minutos_autorizados, uc_autorizadas, decidido_por BROKER·USUARIO_VIA_BROKER·POLITICA_AUTOMATICA, motivo, timestamp}` |
| `recordatorio` | Fecha-hora | No | Enviado a las 24 h (HT-05) |
| `plan_modificado` | Identificador | Si opción b o c | `PLAN-B-…-vN` |
| `estado` | Enumerado | Sí | Sección 5.2 |

### 4.4 Solicitud de credencial (CRED-B)

| Campo | Tipo | Oblig. | Valores / formato |
|---|---|---|---|
| `cred_id` | Identificador | Sí | `CRED-B-AAAA-NNNN` |
| `pet_id` | Identificador | No | PET-B o null (necesidad recurrente) |
| `detectada_por` | Objeto | Sí | `{via F9_RESTRICCIONES·RETORNO_CT08·LAGUNA_DECLARADA, ref (MBF-/RF-…, PET-B), agente}` |
| `proveedor` / `servicio` | Texto | Sí | — |
| `tipo_acceso` | Enumerado | Sí | GRATUITO_CON_REGISTRO · DE_PAGO_FUTURO (este último solo con autorización previa del operador, 13.6) |
| `finalidad` | Objeto | Sí | `{dimensiones[], metricas[], decision_que_puede_cambiar, peticiones_que_la_usarian recurrente·solo esta}` |
| `alcance` | Objeto | Sí | `{permisos SOLO_LECTURA, puntos_de_acceso[], limite_llamadas_dia}` |
| `duracion` | Texto | Sí | hasta revocación · fecha |
| `alternativa_sin_clave` / `degradacion_sin_clave` | Texto | Sí | Lo que se hará y se declarará sin la clave |
| `urgencia` | Enumerado | Sí | BLOQUEA_PETICION · MEJORA_CALIDAD |
| `respuesta` | Objeto | Si respondida | `{estado PROVISTA_EN_BOVEDA·DENEGADA·APLAZADA, credencial_ref (alias), caducidad, restricciones, fecha}` |
| `comprobacion_boveda` | Objeto | Si PROVISTA | `{fecha, resultado ALIAS_ACTIVO·ALIAS_INEXISTENTE·CADUCADO}` (HT-01, solo estado) |
| `avisos_caducidad` | Lista | No | Fechas de aviso de HT-05 |
| `estado` | Enumerado | Sí | Sección 5.3 |

Ningún campo contiene ni puede contener la clave (B.6). Un valor con forma de clave en cualquier campo convierte el registro en `MENSAJE_RECHAZADO` (4.8) e incidencia Crítica.

### 4.5 Consulta (QRY-B)

| Campo | Tipo | Oblig. | Valores / formato |
|---|---|---|---|
| `query_id` | Identificador | Sí | `QRY-B-AAAA-NNNN` |
| `fecha_recepcion` / `fecha_respuesta` | Fecha-hora | Sí | — |
| `pregunta` | Texto | Sí | Literal, sin datos personales |
| `contexto` | Objeto | No | `{pet_id, rec_id, cand_id, alr_id}` |
| `urgencia` | Enumerado | Sí | INMEDIATA · NORMAL |
| `clase_consulta` | Enumerado | Sí | ACLARACION · DATO · METODO · ESTADO · CONTRASTE · PROFUNDIZACION |
| `ruta` | Enumerado | Sí | N0 · PROPUESTA_DE_PETICION |
| `respuesta` | Texto | Sí | Respuesta enviada |
| `referencias` | Lista | Sí en N0 | REC-B, CAND-B, CLM-B, PRG-B, CALC-B, MKT-B, PET-B, AUT-B, CRED-B, ALR-B |
| `caducidades_afectadas` | Lista | No | Dimensiones caducadas de la ficha MKT-B usada (7.7.2) |
| `confianza` | Enumerado | Sí | establecido · probable · especulativo · en disputa |
| `peticion_propuesta` | Objeto | Si PROPUESTA_DE_PETICION | `{nivel, alcance, estimacion_min_p80, adelanto (lo que ya se sabe, con referencias)}` |
| `tiempo_respuesta_s` / `consumo_uc` | Números | Sí | Objetivo N0 < 2 min, ≈ 1 UC |
| `tema_normalizado` / `repeticion` | Texto / objeto | Sí / No | `{veces_4_semanas, msg_id_ct26}` |
| `muestreo_auditoria` | Objeto | No | `{seleccionada sí/no, aud_id}` (muestreo del 10 % de N0; revisión posterior a la respuesta) |

### 4.6 Alerta transmitida (ALR-B)

`alr_id` (`ALR-B-AAAA-NNNN`, asignado por el Vigía en CT-B-25), `msg_id_ct25` (recibido), `msg_id_ct07` (enviado), `fecha_recepcion`, `fecha_transmision`, `rec_id`, `pet_id`, `cand_ids`, `clasificacion` (REVISION · INVALIDACION_PROBABLE · INVALIDACION_CONFIRMADA), `severidad`, `accion_sugerida` (NINGUNA · CONSULTA_N0 · NUEVA_PETICION_SUGERIDA), `peticion_sugerida`, `nota` («El bloque no ha iniciado ningún análisis.»), `respuesta_broker` (`{pet_id nueva o null, fecha}`). Las señales `FLUCTUACION` no llegan aquí: solo constan en F3 (B.7).

### 4.7 Comunicación del Broker (RET-B)

| Campo | Tipo | Oblig. | Valores / formato |
|---|---|---|---|
| `ret_id` | Identificador | Sí | `RET-B-AAAA-NNNN` |
| `msg_id_ct04` / `fecha` | Texto / fecha | Sí | — |
| `decision_ambito` | Objeto | No | `{rec_id, decision CANDIDATOS_ENVIADOS_A_C·EN_VIGILANCIA·DESCARTADO·APLAZADO, motivo}` |
| `decisiones_candidatos` | Lista | No | `{cand_id, decision ENVIADO_A_C·EN_VIGILANCIA·DESCARTADO, bloque_c, motivo}` |
| `resultado_comunicado` | Objeto | No | `{cand_id, valoracion_bloque_C, texto}` |
| `valoracion_entregables` | Objeto | No | `{pet_id, informe_tecnico, memorando, informe_visual, paquete_json, anexo_datos, mapa_eslabones (1–5), comentario}` |
| `forzar_continuacion` | Objeto | No (V2.1) | `{pet_id, puerta PV1·PV2, motivo}`; válido solo dentro del plazo (7 días) y nunca para PV3 |
| `configuracion` | Objeto | No | `{solicitado (B.4), aplicado [{param_id, cfg_id}], rechazado [{param, motivo REGIMEN_NO_SERVICIO·FUERA_DE_LIMITE·TOPE_480·NO_PERMITIDO}]}` |
| `estado` | Enumerado | Sí | APLICADA · APLICADA_PARCIALMENTE · RECHAZADA |
| `msg_id_ct26` | Texto | Sí | Aviso al Evaluador (decisiones, resultados y valoraciones) |

Las decisiones del Broker **no alteran la evaluación** (7.8): el Evaluador anota `decision_broker` en F3 sin cambiar el estado analítico.

### 4.8 Mensaje rechazado (tipo_registro `MENSAJE_RECHAZADO`)

`msg_id`, `contrato`, `emisor_declarado`, `fecha`, `motivo` (DATOS_SENSIBLES · CREDENCIAL_EN_MENSAJE · CANAL_NO_PREVISTO · ESQUEMA_INVALIDO · VERSION_CONTRATO · INSTRUCCION_INCRUSTADA), `campo_afectado` (ruta del campo, **sin el valor**), `tipo_dato` (clave API · IBAN · documento de identidad · correo · teléfono · cartera · otro), `respuesta_enviada` (motivo comunicado al Broker; en credenciales, aviso para que revoque la clave, 17.2), `inc_ref` (INC-B que el Orquestador abre en HA).

### 4.9 Puerta de viabilidad (tipo_registro `PUERTA_VIABILIDAD`, V2.1)

| Campo | Tipo | Oblig. | Valores / formato |
|---|---|---|---|
| `pet_id` / `run_id` | Identificadores | Sí | — |
| `puerta` / `capa` | Enumerado / entero | Sí | PV1 (capa 1) · PV2 (capa 2) · PV3 (capa 3) |
| `resultado` | Enumerado | Sí | SUPERADA · NO_SUPERADA · FORZADA |
| `criterios` | Lista | Sí | `{criterio, clase ELIMINATORIO·DEBILIDAD·UMBRAL, detalle}` (B.15) |
| `insumos` | Objeto | Sí | Valores evaluados por HT-03 (`evaluar_pv1`, `evaluar_pv2`, `evaluar_pv3`) |
| `fecha` | Fecha-hora | Sí | — |

### 4.10 Parada y continuación forzada (tipo_registro `PARADA_PUERTA` y `CONTINUACION_FORZADA`, V2.1)

`PARADA_PUERTA`: `pet_id`, `run_id`, `rec_id`, `puerta`, `sugerencia` (DESCARTAR · PONER_EN_SEGUIMIENTO), `rutas_ENT {informe_parada md, json}`, `g3` (perfil PAR), `auditoria` (muestreo 30 %), `autorizacion_salida` (AUTS-B), `posible_hasta` (fecha límite para forzar), `checkpoint_id`, `estimacion_resto_p80_min`.
`CONTINUACION_FORZADA`: `pet_id`, `puerta`, `motivo`, `via` (CT-B-04 · CT-B-28), `decidido_por` (BROKER · USUARIO_VIA_BROKER), `run_id` de reanudación, efecto declarado (tras PV2: F4 cualitativo y F5 indicativo salvo petición expresa).

### 4.11 Consulta al Broker y aporte (tipo_registro `CONSULTA_BROKER`, CNS-B, V2.1)

| Campo | Tipo | Oblig. | Valores / formato |
|---|---|---|---|
| `cns_id` | Identificador | Sí | `CNS-B-AAAA-NNNN` |
| `sentido` | Enumerado | Sí | SALIENTE · RESPUESTA · ENTRANTE |
| `pet_id` / `run_id` / `seg_id` | Identificadores | Según origen | — |
| `tipo` | Enumerado | Sí | ACLARACION_ALCANCE · DATO_O_DOCUMENTO · PREFERENCIA_O_CRITERIO · CONFIRMACION_SUPUESTO · OTRA · APORTE_BROKER (entrante) |
| `modo` | Enumerado | Si SALIENTE | BLOQUEANTE · NO_BLOQUEANTE |
| `preguntas` | Lista | Si SALIENTE | `{n, pregunta, origen_agente, por_que_importa, opciones, supuesto_si_no_hay_respuesta, efecto_si_supuesto_falso}` (B.12) |
| `plazo` / `punto_control` | Fecha-hora / objeto | Si SALIENTE | `{checkpoint_id, capa}` en las BLOQUEANTES |
| `respuestas` / `forzar_continuacion` | Lista / objeto | Si respondida | — |
| `naturaleza` / `contenido` | Enumerado / texto | Si ENTRANTE | ALCANCE · PREFERENCIA (vinculan) · DATO · DOCUMENTO (pista que se re-verifica, R31) |
| `resolucion` | Enumerado | Al cierre | RESPONDIDA · SUPUESTO_APLICADO · RESPUESTA_TARDIA |
| `efecto` | Enumerado | Al cierre | SIN_CAMBIO · SUPUESTO_CAMBIADO · CONCLUSION_CAMBIADA |
| `minutos_pausa` | Número | Si BLOQUEANTE | Tiempo en `EN_PAUSA_CONSULTA` |
| `recurrente` | Objeto | No | `{clase, peticiones (≥ 3 en 8 semanas), msg_id_ct26}` → lección de producto (12.7) |

### 4.12 Ejecución de un ciclo de seguimiento (RUN-B con `nivel` = N1-SEG, V2.1)

Como 4.2, con `seg_id` y `ciclo_id` (CIC-B del archivo F11) en lugar de `pet_id`; sin autorización salvo que el ciclo supere 30 min (CT-B-05). Tipo de registro `CICLO_SEGUIMIENTO` para la entrega del informe de seguimiento (ruta, semáforo, recomendación, G3 perfil CIC).

## 5. Estados y transiciones

### 5.1 Petición (PET-B; Documento 0, 7.5)

| Desde | Hacia | Condición |
|---|---|---|
| (alta) | RECIBIDA | CT-B-01 registrado |
| RECIBIDA | ADMITIDA · RECHAZADA | Admisibilidad (motivos de D.5) |
| ADMITIDA | PLANIFICADA | Plan PLAN-B y estimación del Coordinador |
| PLANIFICADA | EN_PAUSA_AUTORIZACION | p80 > 30 min o > límite PERS (PT30) |
| PLANIFICADA · EN_PAUSA_AUTORIZACION | EN_CURSO | p80 ≤ 30 min, autorización del Broker o de su política, o N3 expreso con justificación registrada |
| EN_CURSO | EN_PAUSA_PUNTO_CONTROL | Proyección de exceso (PT30 en ejecución o PTA) y punto de control seguro alcanzado |
| EN_PAUSA_PUNTO_CONTROL | EN_CURSO · DIVIDIDA · CANCELADA | Decisión (continuar o versión ≤ 30 min · dividir · cancelar) |
| EN_PAUSA_AUTORIZACION · EN_PAUSA_PUNTO_CONTROL | CADUCADA | 7 días sin respuesta (recordatorio a las 24 h) |
| EN_CURSO | EN_AUDITORIA | Paquete de síntesis en F8 |
| EN_AUDITORIA | AUTORIZADA · BLOQUEADO_AUDITORIA | Autorización de contenido y de salida, o bloqueo tras tres vueltas |
| AUTORIZADA | ENTREGADA | CT-B-02 enviado y publicado en ENT |
| EN_CURSO | EN_PAUSA_CONSULTA | Consulta BLOQUEANTE al Broker (CT-B-28) con punto de control (V2.1) |
| EN_PAUSA_CONSULTA | EN_CURSO | Respuesta del Broker o plazo vencido (se aplica el supuesto declarado) |
| EN_CURSO | DETENIDA_EN_PUERTA | PV1 o PV2 no superada sin continuación forzada; informe de parada entregado (V2.1) |
| DETENIDA_EN_PUERTA | EN_CURSO | Continuación forzada por el Broker dentro de plazo (CT-B-04 o CT-B-28) |
| DETENIDA_EN_PUERTA | ENTREGADA | Vence el plazo para forzar (7 días) |
| cualquiera no final | CANCELADA | Decisión del Broker |

Estados finales: RECHAZADA, ENTREGADA, CANCELADA, CADUCADA, BLOQUEADO_AUDITORIA (DETENIDA_EN_PUERTA es lateral y reanudable durante el plazo). Lo hecho en una petición CADUCADA o CANCELADA queda registrado y reutilizable, sin entregable salvo petición (9.9).

### 5.2 Autorización (AUT-B)

`PENDIENTE` → `DECIDIDA` (por el Broker) · `CADUCADA`; `AUTOMATICA_NOTIFICADA` (estado final al aplicar la política, con justificación registrada); `REGISTRADA_N3` (justificación de un N3 expreso).

### 5.3 Credencial (CRED-B)

`SOLICITADA` → `PROVISTA_EN_BOVEDA` · `DENEGADA` · `APLAZADA`; `PROVISTA_EN_BOVEDA` → `CADUCADA` · `REVOCADA`; `APLAZADA` → `SOLICITADA` (nueva solicitud referenciada).

## 6. Índices de consulta

| Índice | Clave | Uso |
|---|---|---|
| Por estado | `estado` | Colas, pausas y caducidades (HT-05) |
| Por ámbito | `peticion_normalizada.ambito`, `opp_id_A`, `rec_id` | F0: análisis previos; peticiones solapadas |
| Por hash | `hash_peticion` | Idempotencia (6.2.2) |
| Autorizaciones | `aut_id`, `tipo`, `decidido_por`, `politica_aplicada.regla_id` | Revisión trimestral del uso de la puerta de tiempo (18.2) |
| Estimación frente a real | `tiempo_total`, `fases` | Modelo de tiempos del Evaluador |
| Credenciales | `estado`, `caducidad`, `proveedor` | Avisos de caducidad; consultas de estado |
| Consultas | `clase_consulta`, `ruta`, `tema_normalizado` | Preguntas repetidas; N0 |
| Candidatos enviados a C | `decisiones_candidatos.decision` = ENVIADO_A_C | F0 de peticiones nuevas; aprendizaje (12.5) |
| Rechazos de mensajes | `tipo_registro` = MENSAJE_RECHAZADO | Incidencias de seguridad (HA) |
| Consultas al Broker (V2.1) | `cns_id`, `estado`, `plazo`, `tipo`, `pet_id` | Pausas, vencimientos (HT-05), consultas recurrentes, métricas del Evaluador |
| Puertas y paradas (V2.1) | `puerta`, `resultado`, `sugerencia` | Falsos negativos de las puertas (12.7); plazo para forzar |
| Ciclos de seguimiento (V2.1) | `seg_id`, `ciclo_id` | Consumo por ciclo; cruce con el archivo F11 |

## 7. Ejemplo ficticio

> **EJEMPLO FICTICIO — no es una entrada real.** Datos e identificadores inventados.

```json
{"tipo_registro":"AUT-B","aut_id":"AUT-B-2026-0004","pet_id":"PET-B-2026-0007","run_id":"RUN-B-2026-0007-01",
 "tipo":"AUTORIZACION_AUTOMATICA_NOTIFICADA","puerta":"PT30","momento":"PREVIO_F0","punto_control":null,
 "hecho_hasta_ahora":{"fases_cerradas":["F0"],"conclusiones_provisionales":[],"minutos_consumidos":3,"uc_consumidas":4},
 "estimacion":{"minutos_p50":48,"minutos_p80":62,"uc_p50":85,"uc_p80":104,"desglose_por_fase":{"F2":24,"F5":16,"F6":7,"F8":9,"F9":6}},
 "justificacion":{"que_aporta":"Tres tipos de activo aplicables (RV, FON, RF) y D4 en P3 con cinco eslabones",
   "incertidumbres_que_reduce":[{"incertidumbre":"persistencia del cuello en empaquetado avanzado","efecto_posible":"veredicto VIGILAR→INVERTIR_ESCALONADO"}],
   "que_se_perderia":"Selección RF y refutación de finalistas FON","relevancia_decisional":"ALTA"},
 "opciones":[{"opcion":"CONTINUAR","minutos_p80":62,"uc_p80":104},{"opcion":"VERSION_30_MIN","que_se_recorta":["RF omitido","top-N 3","D5 a P1"],"efecto_previsible":{"E_max":60,"veredicto_max":"VIGILAR"}},
   {"opcion":"DIVIDIR_EN_FASES","fases":[{"fase":1,"contenido":"ámbito y veredicto","minutos_p80":30},{"fase":2,"contenido":"selección","minutos_p80":35}]},{"opcion":"CANCELAR","se_entrega":"resumen N0"}],
 "recomendacion_bloque":{"opcion":"CONTINUAR","motivo":"El cuello decide el veredicto; recortarlo deja un VIGILAR no concluyente"},
 "politica_aplicada":{"regla_id":"POL-1","resultado":"AUTORIZA"},
 "decision":{"opcion":"CONTINUAR","minutos_autorizados":62,"uc_autorizadas":null,"decidido_por":"POLITICA_AUTOMATICA","motivo":"relevancia ALTA ≤ 90 min","timestamp":"2026-11-10T09:14:00+01:00"},
 "estado":"AUTOMATICA_NOTIFICADA"}
```
