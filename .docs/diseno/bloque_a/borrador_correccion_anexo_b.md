# Borrador · corrección del Anexo B del Documento 0 del Bloque A

**Estado: borrador para la próxima entrega del Documento 0. No se aplica al corpus** (el Documento 0 es una entrega congelada). Generado por `.docs/scripts/borrador_anexo_b.py` a partir de `bloque_a/11_Ejecutor/tests/goldens/divergencias_anexo_b.json`; no se edita a mano: si cambian las diferencias, se vuelve a generar.

**Por qué.** El operador decidió el 13-11-2026 que, si el Documento 0 y el código difieren, manda el código, porque el Documento 0 se escribió antes de construir el bloque (INC-T114-01 en `docs/incidencias.md`). El Anexo B se corrige para que describa lo que hace el ejecutor.

## 1. Cambios generales

- **Lotes (CT-11, CT-12 y CT-13).** El Anexo B describe una pieza, un encargo o una petición por mensaje; el ejecutor los agrupa en una lista (`piezas`, `encargos`, `peticiones`) y rechaza el ejemplo tal cual. Propuesta: describir el mensaje como la lista, con los campos de hoy dentro de cada elemento, y cambiar el ejemplo.
- **Estado del objeto en los retornos de CT-23, CT-24 y CT-25.** El bloque JSON del Anexo B pone el estado del objeto en `estado`; el ejecutor lo lleva en `estado_consulta`, `estado_seguimiento` y `estado_credencial`, como pide el §6.2.6 del propio Documento 0, y deja `estado` para el estado común. Propuesta: usar esos nombres en el Anexo B.
- **Campo del tipo en CT-22.** El Anexo B nombra `tipo` («admite además CONSULTA_RECURRENTE y DECISION_SEGUIMIENTO»); el ejecutor emite esos dos en `tipo_aviso` y usa `tipo` para DECISIONES_BROKER y PREGUNTA_REPETIDA. Propuesta: un solo campo. Lo más barato es documentar los dos tal como están; lo más limpio, unificar en el código (cambio de formato, con re-congelado de los goldens). Se decide al preparar la entrega.
- **Retornos RECHAZADO o SIN_RESULTADO.** El Anexo B no dice qué campos llevan. Propuesta: «solo el estado común y el motivo (§6.2.6); los campos de resultado no se exigen», salvo CT-03, donde el ejecutor exige los campos de retorno también en un rechazo (decirlo).
- **Listas cerradas.** Fuera de CT-01 y CT-02 la mensajería no aplica las listas cerradas del Anexo B (18 casos en 10 contratos) ni la condición de `contenido` de CT-23 («solo en ENTRANTE»). Propuesta: decir en cada lista si la mensajería la valida o si la valida el agente que recibe; o validarlas en el código (cambio de formato).
- **CT-16 a CT-21.** El Anexo B no da sus campos (los remite a los prompts de sistema). Propuesta: dar al menos los campos de los que el ejecutor emite (CT-16, CT-17 y CT-19), que ya están congelados en `formas_flujos_mock.json`.
- **`fecha_corte` de CT-09.** El Anexo B la hace obligatoria solo en evaluaciones y backtesting; el ejecutor la exige siempre (es más estricto). Propuesta: obligatoria siempre.
- **Lo que el Anexo B deja abierto.** La codificación de `coincide` (CT-10) y de `independiente` (CT-11) y los nombres de las claves de `fechas` (CT-11). Propuesta: fijarlos con los valores que usa el ejecutor (los de `esquemas_respuestas.json`).
- **Retornos internos (CT-06 a CT-14).** No pasan por la mensajería: la respuesta de cada agente se valida con los esquemas de `ESQUEMAS` (congelados en `bloque_a/11_Ejecutor/tests/goldens/esquemas_respuestas.json`), que no llevan los mismos nombres que el Anexo B. Propuesta: describir en el Anexo B los campos de esos esquemas, no marcar opcionales los de hoy.
- **Campos mínimos que el ejecutor no exige.** Por la decisión del operador, la propuesta por defecto es marcarlos en el Anexo B como opcionales («si aplica»). Si alguno debe ser obligatorio de verdad, se cambia el código en su lugar y se re-congelan los goldens con su motivo. La lista, contrato a contrato, está abajo.

## 2. Contrato a contrato

| Contrato | Lo que difiere hoy | Cambio propuesto en el Anexo B |
| --- | --- | --- |
| CT-01.ENCARGO | el ejecutor admite que falte `fecha_objetivo`, `nivel_forzado`, `referencia_previa` | marcarlos «opcional» (o exigirlos en el código) |
| CT-03.ENCARGO | el ejecutor admite que falte `contexto`, `urgencia` | marcarlos «opcional» (o exigirlos en el código) |
| CT-03.ENCARGO | en los mensajes emitidos falta `contexto.opp_id`, `contexto.run_id`, `query_id` | marcarlos «si aplica» |
| CT-03.RETORNO | el ejecutor admite que falte `escalado` | marcarlos «opcional» (o exigirlos en el código) |
| CT-03.RETORNO | `escalado` llega con otro tipo (el Anexo B pide object; el ejecutor envía null cuando no aplica) | admitir null «si no aplica» |
| CT-04.ENCARGO | el ejecutor admite que falte `configuracion`, `decisiones`, `resultado_comunicado`, `valoracion_informe` | marcarlos «opcional» (o exigirlos en el código) |
| CT-04.ENCARGO | en los mensajes emitidos falta `configuracion.clases_activas`, `configuracion.dia_hora_entrega`, `configuracion.idioma_usuario`, `configuracion.periodicidad` | marcarlos «si aplica» |
| CT-04.ENCARGO | INC-T116-01 | El Broker pide horizontes con una lista global (`horizontes`), no por tipo de activo: se rechaza cada celda que la tabla 8.3 marca «No». Decir en el Anexo B que la lista es global y que el rechazo es por celda. |
| CT-06.ENCARGO | golden (fases) | El ciclo emite las fases `CRIBADO_E_INVESTIGACION` y `RESPUESTA_OBJECIONES`, que la lista cerrada del Anexo B (CRIBADO, INVESTIGACION, PROFUNDIZACION, SEGUIMIENTO) no tiene: añadirlas. |
| CT-06.RETORNO | el ejecutor admite que falte `cribado`, `descartadas_relevantes`, `finalistas`, `lagunas`, `regimen_clase`, `revision_vigentes`, `senales_para_otras_clases` | describir los campos del esquema de `ESQUEMAS` de ese agente (ver «Retornos internos» en el §1) |
| CT-07.RETORNO | el ejecutor admite que falte `contradicciones`, `evidencias_enviadas_a_curador`, `lagunas`, `referencias`, `sintesis` | describir los campos del esquema de `ESQUEMAS` de ese agente (ver «Retornos internos» en el §1) |
| CT-08.RETORNO | el ejecutor admite que falte `contradicciones`, `evidencias_enviadas_a_curador`, `lagunas`, `referencias`, `sintesis` | describir los campos del esquema de `ESQUEMAS` de ese agente (ver «Retornos internos» en el §1) |
| CT-09.RETORNO | el ejecutor admite que falte `artefacto_id`, `clase_cifra`, `incertidumbre`, `informe_calidad_datos`, `resultado` | describir los campos del esquema de `ESQUEMAS` de ese agente (ver «Retornos internos» en el §1) |
| CT-10.RETORNO | el ejecutor admite que falte `coincide`, `diagnostico`, `diferencias` | describir los campos del esquema de `ESQUEMAS` de ese agente (ver «Retornos internos» en el §1) |
| CT-11.ENCARGO | el ejecutor exige `piezas` y rechaza el ejemplo del Anexo B (MensajeInvalido: «CT-11: faltan campos mínimos ['piezas']») | el mensaje es una lista `piezas`; cada elemento es una pieza de evidencia con los campos de hoy (`afirmacion`, `direccion`, `extracto`, `fechas`, `fuente`, `unidad_divisa`); ejemplo nuevo |
| CT-11.RETORNO | el ejecutor admite que falte `clm_id`, `duplicado_de`, `evd_id`, `independiente`, `raiz_id` | describir los campos del esquema de `ESQUEMAS` de ese agente (ver «Retornos internos» en el §1) |
| CT-12.ENCARGO | el ejecutor exige `encargos` y rechaza el ejemplo del Anexo B (MensajeInvalido: «CT-12: faltan campos mínimos ['encargos']») | el mensaje es una lista `encargos`; cada elemento es un encargo de prospectiva con los campos de hoy (`catalizadores_conocidos`, `datos`, `horizontes`, `opp_id`, `tesis`); ejemplo nuevo |
| CT-12.RETORNO | el ejecutor admite que falte `escenarios`, `hitos`, `indicadores_adelantados`, `invalidacion`, `pronosticos` | describir los campos del esquema de `ESQUEMAS` de ese agente (ver «Retornos internos» en el §1) |
| CT-13.ENCARGO | el ejecutor exige `peticiones` y rechaza el ejemplo del Anexo B (MensajeInvalido: «CT-13: faltan campos mínimos ['peticiones']») | el mensaje es una lista `peticiones`; cada elemento es una petición de objeciones con los campos de hoy (`calculos`, `evidencias_clave`, `opp_id`, `prospectiva`, `tesis`); ejemplo nuevo |
| CT-13.RETORNO | el ejecutor admite que falte `objeciones`, `veredicto_global` | describir los campos del esquema de `ESQUEMAS` de ese agente (ver «Retornos internos» en el §1) |
| CT-14.RETORNO | el ejecutor admite que falte `comprobaciones`, `dictamen`, `motivo` | describir los campos del esquema de `ESQUEMAS` de ese agente (ver «Retornos internos» en el §1) |
| CT-22.ENCARGO | el ejecutor admite que falte `tipo` | marcarlos «opcional» (o exigirlos en el código) |
| CT-22.ENCARGO | el valor `CONSULTA_RECURRENTE` va en `tipo_aviso`, no en `tipo` | nombrar `tipo_aviso` |
| CT-22.ENCARGO | el valor `DECISION_SEGUIMIENTO` va en `tipo_aviso`, no en `tipo` | nombrar `tipo_aviso` |
| CT-23.ENCARGO | el ejecutor admite que falte `plazo_respuesta`, `preguntas`, `punto_control`, `seg_id` | marcarlos «opcional» (o exigirlos en el código) |
| CT-23.ENCARGO | en los mensajes emitidos falta `preguntas[].efecto_si_falso`, `preguntas[].opciones_sugeridas`, `preguntas[].origen`, `preguntas[].por_que_importa`, `run_id` | marcarlos «si aplica» |
| CT-23.RETORNO | el ejecutor admite que falte `respuestas`, `supuestos_aplicados` | marcarlos «opcional» (o exigirlos en el código) |
| CT-23.RETORNO | el valor `RESPONDIDA` va en `estado_consulta`, no en `estado` | nombrar `estado_consulta` |
| CT-23.RETORNO | en los mensajes emitidos falta `respuestas[].documentos` | marcarlos «si aplica» |
| CT-24.ENCARGO | el ejecutor admite que falte `calendario_personalizado`, `fecha_fin`, `frecuencia`, `motivo`, `opp_id`, `seg_id`, `senales_interes` | marcarlos «opcional» (o exigirlos en el código) |
| CT-24.RETORNO | el ejecutor admite que falte `proximo_ciclo` | marcarlos «opcional» (o exigirlos en el código) |
| CT-24.RETORNO | el valor `ACTIVO` va en `estado_seguimiento`, no en `estado` | nombrar `estado_seguimiento` |
| CT-24.RETORNO | el valor `CANCELADO` va en `estado_seguimiento`, no en `estado` | nombrar `estado_seguimiento` |
| CT-24.RETORNO | el valor `FINALIZADO` va en `estado_seguimiento`, no en `estado` | nombrar `estado_seguimiento` |
| CT-24.RETORNO | el valor `PAUSADO` va en `estado_seguimiento`, no en `estado` | nombrar `estado_seguimiento` |
| CT-24.RETORNO | INC-T114-02 | El ejemplo publicado del informe de seguimiento no cumple su propio esquema: corregir el ejemplo. |
| CT-25.ENCARGO | el ejecutor admite que falte `herramienta`, `urgencia` | marcarlos «opcional» (o exigirlos en el código) |
| CT-25.RETORNO | el ejecutor admite que falte `caducidad`, `credencial_ref` | marcarlos «opcional» (o exigirlos en el código) |
| CT-25.RETORNO | el valor `DENEGADA` va en `estado_credencial`, no en `estado` | nombrar `estado_credencial` |
| CT-25.RETORNO | el valor `PROVISTA` va en `estado_credencial`, no en `estado` | nombrar `estado_credencial` |

## 3. Contratos sin campos en el Anexo B

`CT-16`, `CT-17`, `CT-18`, `CT-19`, `CT-20`, `CT-21`: ver «CT-16 a CT-21» en el §1.

## 4. Cómo se aplica en la entrega

1. Se edita el Anexo B (y los §7.6 y §7.9 si se unifica el campo de CT-22) en la nueva versión del Documento 0.
2. Se re-congela el corpus con su motivo (`tools/corpus_integridad.py --update`) y los goldens que dependan del Anexo B (`anexo_b_esquemas.json`, `huellas.json`, `divergencias_anexo_b.json`) con `goldens_ct.py --update --motivo`.
3. `divergencias_anexo_b.json` debería quedar vacío, salvo lo que se decida dejar.
