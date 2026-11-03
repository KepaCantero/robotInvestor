# Mapa del Plan de pruebas del Bloque A Forex → pruebas automáticas del ejecutor

**Bloque A Forex · Robot Investor · Ejecutor `bloque_a_forex` V1.0 · 02/11/2026 · actualizado V1.1 (03/11/2026)** · Subordinado al Documento 0 del Bloque A Forex V1.1.

Cobertura de las 77 pruebas de `09_Pruebas/Plan de pruebas del Bloque A Forex - V1.0.md` por la batería `pytest` de esta carpeta, ejecutada con `MockClient` (respuestas sintéticas deterministas). Resultado de la última ejecución en `RESULTADOS.txt`. Las comprobaciones G3-FX-01…11 del Anexo 1 del Plan están implementadas en HT-09 y probadas en `10_Herramientas/tests/test_ht09_validador_g3.py`; el ejecutor usa una copia literal de HT-09 en cada ciclo.

Leyenda de la columna «Cobertura»: **Automática** (la prueba ejecuta el criterio de aprobación del plan con el cliente simulado), **Parcial** (se comprueba la mecánica determinista del ejecutor; el juicio del agente requiere un LLM real), **LLM real** (exige el modelo real, usuarios o el despliegue multiagente completo), **Fuera del ejecutor** (corresponde a otras piezas del paquete).

Importante (R22): «Automática» con `MockClient` valida la **tubería** (canales, archivos, puertas, herramientas, cálculos, exportación), no la calidad analítica de los agentes. Ningún componente pasa por ello a «validado».

| Prueba | Cobertura | Prueba automática | Resultado |
|---|---|---|---|
| PB-01 Ciclo periódico completo | Automática | `test_integracion::test_ciclo_semanal_completo_apto`, `test_canales_y_matriz_respetados` | Superada |
| PB-02 Top-3 con menos de tres | Parcial | `test_ciclo_semanal_completo_apto` (motivo R14 en cada segmento con < 3); segunda pasada en banda marginal: HT-03 | Superada |
| PB-03 Segmento sin opciones | Parcial | `test_presupuesto_agotado_parcial_declarado` (segmento con 0 opciones y semáforo GRIS) | Superada |
| PB-04 Misma tendencia, estrategias por segmento | LLM real | — (las lentes por segmento las aplica el modelo; el ejecutor registra perfiles y cálculos en RC) | — |
| PB-05 Marco de otro segmento sin justificación | LLM real | — (lo detecta el Auditor) | — |
| PB-06 Consulta N0 sin escalado | Automática | `test_consulta_n0_sin_escalado` (ruta N0, referencias con prefijo FX, sin CT-05, ≤ 1 UC con caché caliente) | Superada |
| PB-07 Consulta que escala | Automática | `test_consulta_que_escala_y_pregunta_repetida` (peso mexicano frente al real ⇒ C2 sobre EMLA) | Superada |
| PB-08 Ráfaga de peticiones | Parcial | Idempotencia y acuse: `test_contratos_canales_credenciales_e_idempotencia`; cola: HT-08 en `test_ht04_y_ht06_y_ht08` | Superada |
| PB-09 Cambio de periodicidad | Parcial | `test_peticion_ad_hoc_y_decisiones` (CFG- por AG-01, CT-22); la reprogramación real la hace el planificador externo | Superada |
| PB-10 Configuración no permitida | Automática | `test_peticion_ad_hoc_y_decisiones` (H1 de ESTR y umbral E rechazados; APLICADA_PARCIALMENTE) | Superada |
| PB-11 Decisión del Broker sin alterar el análisis | Automática | `test_peticion_ad_hoc_y_decisiones` (estado de F3 intacto, `decision_broker`, CT-22) | Superada |
| PB-12 Campos de decisión y paquete para B | Automática | `test_ciclo_semanal_completo_apto` (esquema JSON del Bloque A Forex; una entrada de B por opción) | Superada |
| PB-13 GC0 negativo con arrastre verificado | Automática | `test_gc0_negativo_arrastre_verificado` (N1, ≤ 5 UC, solo modo ligero, sin candidatas nuevas), `test_gc0_tercio_de_pares_e_indice_representativo` | Superada |
| PB-14 Arrastre con invalidación activada | Automática | `test_autocritica::test_arrastre_con_invalidacion_activada` | Superada |
| PB-15 Reglas de parada | LLM real | — | — |
| PB-16 Presupuesto agotado | Automática | `test_presupuesto_agotado_parcial_declarado` (PARCIAL, limitación en ambos informes, G3 en F6 y F7) | Superada |
| PB-17 Ampliación de presupuesto | Parcial | Registro AUT- en HA dentro de la prueba de presupuesto (autorización determinista por regla) | Superada |
| PB-18 Cola saturada y apertura de instancia | Parcial | `test_ht04_y_ht06_y_ht08` (ORD- para agente sin estado) | Superada |
| PB-19 Agente de instancia única saturado | Parcial | `test_ht04_y_ht06_y_ht08` (sin ORD- para AG-02) | Superada |
| PB-20 Instrucción incrustada | Automática | `test_instruccion_incrustada_ignorada_y_registrada` (notas de EUR/JPY), `test_saneamiento_r9` | Superada |
| PB-21 Credencial en un mensaje | Automática | `test_contratos_canales_credenciales_e_idempotencia` | Superada |
| PB-22 Canal no previsto | Automática | `test_contratos_canales_credenciales_e_idempotencia`; CT-06T solo entre AG-02 y AG-09/AG-21 (`test_seis_segmentos_veintiun_agentes_y_canales`) | Superada |
| PB-23 Escritura fuera de reserva | Automática | `test_almacen_reserva_integridad_y_as_of` | Superada |
| PB-24 Enlace roto y borrado | Fuera del ejecutor | HT-02 (pruebas de `10_Herramientas`); el ejecutor solo lo invoca (`bloque-a-forex verificar-enlaces`) | — |
| PB-25 Contenido cambiado y retractación | Fuera del ejecutor | Ídem | — |
| PB-26 Clasificación temática y orden por calidad | Fuera del ejecutor | Áreas TX/TMX/TFX/MB leídas por `referencias.py` (`test_archivos_de_referencia_reales_se_localizan_y_se_leen`) | — |
| PB-27 Fondo metodológico | LLM real | — | — |
| PB-28 Alimentación continua y Novedades | LLM real | — | — |
| PB-29 Contar raíces | Parcial | Deduplicación por hash y raíces por fuente en `_registrar_evidencia_segmento` (cubierta por el ciclo completo) | Superada |
| PB-30 Cifra sin artefacto bloqueada | Parcial | HT-09 C08 con `artefactos` del RC en cada ciclo; retirada de opciones con bloqueo implementada | Superada |
| PB-31 Horizonte no certificado sin probabilidad | Automática | `test_ciclo_semanal_completo_apto` (prob = null y etiqueta «sin ventaja demostrada frente al paseo aleatorio») | Superada |
| PB-32 Certificación de un horizonte | Automática | `test_certificado_emitido_con_muestra_suficiente`, `test_metricas_de_pronostico_con_pronosticadores_sinteticos` | Superada |
| PB-33 Revocación por deterioro | Parcial | Regla implementada en `Evaluador.revisar_certificados`; sin prueba dedicada | — |
| PB-34 Fuga en evaluación | Automática | `test_pronosticos_resueltos_sin_look_ahead`, `test_guardia_de_fuga_del_proveedor`, `test_fecha_publicacion_filtra_revisiones`, rechazo FUGA del Motor | Superada |
| PB-35 Recalibración en sombra | Parcial | Implementada (`Evaluador.recalibrar`); sin prueba dedicada (exige ≥ 30 resueltos publicados) | — |
| PB-36 Recalibración fuera de bandas | Parcial | Propuesta P3-EVAL- implementada; sin prueba dedicada | — |
| PB-37 Pronóstico congelado inmutable | Automática | `test_almacen_reserva_integridad_y_as_of`, PRG no anulados en `test_arrastre_con_invalidacion_activada` | Superada |
| PB-38 Objeción fuerte sin resolver | Automática | `test_autocritica::test_objecion_fuerte_sin_resolver_excluye_del_top3` | Superada |
| PB-39 Legibilidad < 70 bloqueada | Parcial | HT-07 ≥ 70 comprobado en el ciclo; bloqueo y reescritura implementados (C12) | Superada |
| PB-40 Comprensión por usuarios | LLM real | Requiere usuarios | — |
| PB-41 Coherencia entre entregables y entre segmentos | Automática | `coherencia()` en cada entrega (falla ⇒ BLOQUEADO); contradicciones entre segmentos en `test_contradicciones_entre_segmentos` | Superada |
| PB-42 Auditoría asíncrona sin bloqueo | Parcial | F9 tras la entrega (AUD-/HAL- en HA); hallazgos reales requieren LLM | — |
| PB-43 Pregunta repetida | Automática | `test_consulta_que_escala_y_pregunta_repetida` (CT-22 y LEC-FX- de producto) | Superada |
| PB-44 Historial de aciertos honesto | Automática | `test_pronosticos_resueltos_sin_look_ahead` (n publicado ≤ resueltos conocidos en la fecha) | Superada |
| PB-45 Lección aplicada | Parcial | Lecciones ≤ 10 inyectadas en el contexto de cada encargo; el mock de Prospectiva reacciona a lecciones de calibración | — |
| PB-46 Fiabilidad de fuentes | LLM real | No implementado (FUE-) | — |
| PB-47 Estados de madurez | Automática | `test_servicio_del_motor_rc_cache_fuga_y_reejecucion` (METODO_NO_IMPLEMENTADO con alternativa; FUERA_DE_CATALOGO para fichas retiradas) | Superada |
| PB-48 Conflicto de normas | Parcial | La invalidación determinista prevalece sobre la recomendación del Analista (R23) | — |
| PB-49 Historial íntegro | Automática | `test_almacen_reserva_integridad_y_as_of`, `test_canales_y_matriz_respetados` | Superada |
| PB-50 Horizontes según el segmento | Parcial | Tabla 8.3 (ESTR sin H1; H1 y H4 «limitados» en emergentes con catalizador y liquidez) y F10 en cada opción; HT-09 C06 | Superada |
| PB-51 Conocimiento en los system prompts | Fuera del ejecutor | Revisión documental; `test_prompts_reales_y_modo_degradado` comprueba que los 21 prompts Forex se localizan | — |
| PB-52 Modo degradado | Parcial | Segmento sin datos ⇒ PARCIAL (PS2); salida no conforme ⇒ PARCIAL con INC (`test_busqueda_web_solo_en_vivo_y_reparacion_json`); prompt sin versión Forex ⇒ incidencia (`test_prompts_reales_y_modo_degradado`) | Superada |
| PB-53 Frontera A/B: instrumento propuesto | Parcial | Ficha de finalista con `not` sobre instrumento, apalancamiento, nivel de entrada (`test_esquema_de_finalista_cambiaria`); consideraciones de implementación filtradas; HT-09 C15 en `10_Herramientas` | Superada |
| PB-54 Encargo completo para el Bloque B | Automática | `test_ciclo_semanal_completo_apto` (consideraciones, carry esperado, niveles con hora de fijación, métricas, preguntas, pronósticos) | Superada |
| PB-55 Cobertura de los seis segmentos | Automática | `test_ciclo_semanal_completo_apto` (seis segmentos en el paquete y en el semáforo), `test_seis_segmentos_veintiun_agentes_y_canales` | Superada |
| PB-56 Oportunidad duplicada entre segmentos | Automática | `test_sin_duplicados_entre_segmentos` (DUPLICADA_EN_OTRO_SEGMENTO por exposición) y C16 de HT-09 | Superada |
| PB-57 Estrategias de emergentes y de estrategias | LLM real | — | — |
| PB-58 Notación invertida | Parcial | El par se toma siempre del universo (`test_normalizacion_fx_de_las_finalistas`); G3-FX-01 en `10_Herramientas` | Superada |
| PB-59 Divisa con controles y PS3 | Automática | `test_normalizacion_fx_de_las_finalistas` (USD/INR no convertible con NDF supera PS3); riesgo ≥ 4 y relevancia ALTA en `test_ciclo_semanal_completo_apto` | Superada |
| PB-60 Tipo fijo y opción REGIMEN | Automática | USD/HKD con caja de conversión (`test_normalizacion_fx_de_las_finalistas`), suelo 4 de RISK-DD-001 v2.0 (`test_risk_dd_v2_umbrales_cambiarios_y_suelo`) | Superada |
| PB-61 Contradicción de USD entre segmentos | Automática | `test_contradicciones_entre_segmentos` (pata activa: JPY largo en G10N y corto en G10M se resuelve o se justifica; USD o EUR como contrapartida no cuentan), `test_patas_activas` en `10_Herramientas` | Superada |
| PB-62 Exposición agregada y apuestas independientes | Automática | `test_utilidades_fx_notacion_exposicion_y_textos`, `test_ciclo_semanal_completo_apto` (exposición agregada validada por G3-FX-08) | Superada |
| PB-63 Informe transversal ausente | Automática | `test_informe_transversal_ausente_declarado` (nota de ausencia, régimen cambiario determinista, entrega no bloqueada) | Superada |
| PB-64 Capas transversales en un ciclo sin cambios | Parcial | Reutilización de los TRV-FX- del ciclo anterior implementada en `_capas_transversales` (solo si ningún segmento tiene cambio material) | — |
| PB-65 Backtest frente al paseo aleatorio y al forward | Automática | `test_backtest_12_semanas_csv_y_metricas` (prob. del paseo aleatorio 0,5, Brier del forward), `test_referencia_ingenua_paseo_aleatorio_y_forward`, `test_carry_forward_ppa_y_paseo_aleatorio` | Superada |
| PB-66 Sin anticipación en las fijaciones | Automática | `test_ciclo_semanal_completo_apto` (niveles con hora de fijación y fecha ≤ fecha de datos), G3-FX-07 | Superada |
| PB-67 Cruces sin USD en el segmento correcto | Parcial | `motivo_asignacion_segmento` cuando el universo difiere de las reglas de 2.6; G3-FX-03 en `10_Herramientas` | Superada |
| PB-68 Carry: signo, ajuste y tipo de rentabilidad | Automática | `test_carry_forward_ppa_y_paseo_aleatorio`, `test_servicio_del_motor_rc_cache_fuga_y_reejecucion` (FX-CARRY-001 v2.0 con dirección), `test_ciclo_semanal_completo_apto` (carry con CALC-FX-, tipo de rentabilidad y divisa) | Superada |
| PB-69 Saturación narrativa cambiaria | Parcial | Tope de valoración en HT-03 (`10_Herramientas`); la marca la pone el Analista | — |
| PB-70 Diversidad por divisa | Parcial | HT-03 (≤ 2 opciones con la misma divisa y dirección por segmento) y G3-FX-09, probados en `10_Herramientas` | Superada |
| PB-71 Cambio de la divisa base | Automática | `test_peticion_ad_hoc_y_decisiones` (P-04 = CHF aplicado; «euro» rechazado por no ser ISO 4217) | Superada |
| PB-72 Intervención cambiaria como cambio material | Parcial | GC0 del Anexo A (`test_gc0_tercio_de_pares_e_indice_representativo`: un tercio de los pares, índice representativo, opción vigente) y eventos de calendario; la detección de la intervención requiere LLM o declaración | Superada |
| PB-73 Sanciones (PS7) | LLM real | — | — |
| PB-74 Identificadores Forex y versión de metodología | Automática | `test_ciclo_semanal_completo_apto` (RUN-FX-, OPP-FX-, PRG-FX-, CALC-FX-, TRV-FX-; FX-1.0), `test_servicio_del_motor_rc_cache_fuga_y_reejecucion` | Superada |
| PB-75 Paridad cubierta y convenciones en el Motor | Automática | `test_carry_forward_ppa_y_paseo_aleatorio` (FX-FWD-001: tipos iguales ⇒ puntos nulos, signo, rendimiento implícito) | Superada |
| PB-76 Informe visual cambiario | Automática | `test_ciclo_semanal_completo_apto` (lista de monedas, termómetro del euro, semáforo de seis, sube y baja, frase fija del Bloque B, HT-07 ≥ 70) | Superada |
| PB-77 Opción de volatilidad sin instrumento | Parcial | `test_normalizacion_fx_de_las_finalistas` (vista de volatilidad, sin dirección ni composición) | Superada |

Pruebas adicionales del encargo del ejecutor: guardia de fuga del proveedor, backtest de 12 semanas sintéticas con CSV y métricas coherentes, certificados no emitidos con n insuficiente, reproducibilidad con `ReplayClient` y anonimización, cliente Anthropic (caché de prompts, búsqueda web, `pause_turn`) con SDK simulado, búsqueda web desactivada en backtest, casos de control de las fichas del Motor (incluidos RISK-DD-001 v2.0, FX-CARRY-001 v2.0, FX-FWD-001, FX-PPP-001 y FX-RW-001), SCORE-RK-001 idéntico a HT-03 con los pesos de A Forex, copias de HT-02/03/07/09 sin divergencia, búsqueda de archivos por prefijo con preferencia por los del Bloque A Forex y lectura de los archivos de referencia reales (`tests/test_forex.py`).

## Actualización V1.1 (03/11/2026)

| Prueba | Cobertura | Prueba automática | Resultado |
|---|---|---|---|
| PB-78 Horizonte principal coherente con la naturaleza | Automática | `test_v11::test_ciclo_declara_naturaleza_y_horizonte_principal`, `test_v11::test_regla_de_adecuacion_y_hitos`; HT-09: `TestV11HorizontePrincipalYH5` | Superada |
| PB-79 H5 limitado con hitos | Automática | `test_v11::test_h5_estructural_con_hitos`, `test_h5_se_evalua_por_hitos_no_por_precio`, `test_ht09_bloquea_h5_tactico` | Superada |
| PB-80 Consulta no bloqueante con supuesto | Automática | `test_v11::test_consultas_broker` (supuestos del RUN, vencimiento, respuesta tardía) | Superada |
| PB-81 Consulta bloqueante: pausa en punto de control | Parcial | `test_v11::test_consultas_broker` (`segmentos_pausados`); la exclusión del segmento en `ciclo` se verificó en la prueba de humo | Superada |
| PB-82 Consultas recurrentes y aportaciones del Broker | Automática | `test_v11::test_consulta_recurrente_avisa_al_evaluador`, `test_consultas_broker` (entrante con R9 y R8) | Superada |
| PB-83 Credenciales por CT-25 y bóveda | Automática | `test_v11::test_credenciales_y_boveda`, `test_boveda_caducidad`, `test_cli_v11` | Superada |
| PB-84 Encargo de seguimiento: ciclo de vida | Automática | `test_v11::test_seguimiento_encargado` | Superada |
| PB-85 Ciclo C6 con informe de seguimiento | Automática | `test_v11::test_seguimiento_encargado`; HT-09: `TestV11Seguimiento` | Superada |
| PB-86 Seguimiento cubierto por C1 y fin del encargo | Automática | `test_v11::test_seguimiento_vigente_se_omite_y_fecha_fin` | Superada |
