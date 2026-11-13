# Mapa del Plan de pruebas V3.0 → pruebas automáticas del ejecutor

**Bloque A · Robot Investor · Ejecutor programático V1.1 · Versión óptima V5.0 · 02/11/2026 · actualizado V5.1 (03/11/2026, ejecutor V1.2)** · Subordinado al Documento 0 óptima V5.1.

> **Aviso (13-11-2026, T-116).** Este mapa es del 3-11-2026 y se conserva como estaba. El mapa vigente y verificado prueba a prueba es `tests/mapa_plan_pruebas.json`, con una regla más estricta (una fila solo es automática si sus pruebas comprueban todo el criterio del plan); el resultado de ejecutarlo está en `docs/evidencias_pruebas_bloque_a.md` (desde la raíz del repositorio), que genera `.docs/scripts/evidencias_plan_a.py --ejecutar`.

Cobertura de las 67 pruebas (PB-01 a PB-67) del `09_Pruebas/Plan de pruebas del Bloque A - V3.0.md` por la batería `pytest` de esta carpeta, ejecutada con `MockClient` (respuestas sintéticas deterministas). Resultado de la última ejecución en `RESULTADOS.txt`. Rehecho contra el plan V3.0 en T-65 (CS-19 de T-53); `test_t65_resto_t53.py::test_cs19_mapa_cubre_las_67_pruebas_del_plan` comprueba que están las 67 y que cada prueba citada existe.

Leyenda de la columna «Cobertura»: **Automática** (la prueba ejecuta el criterio de aprobación del plan con el cliente simulado), **Parcial** (se comprueba la mecánica determinista del ejecutor; el juicio del agente requiere un LLM real), **LLM real** (exige el modelo real, usuarios o el despliegue multiagente completo), **Fuera del ejecutor** (corresponde a otras piezas del paquete).

Importante (R22): «Automática» con `MockClient` valida la **tubería** (canales, archivos, puertas, herramientas, cálculos, exportación), no la calidad analítica de los agentes. Ningún componente pasa por ello a «validado».

| Prueba | Cobertura | Prueba automática | Resultado |
|---|---|---|---|
| PB-01 Ciclo periódico completo | Automática | `test_integracion::test_ciclo_semanal_completo_apto`, `test_canales_y_matriz_respetados` | Superada |
| PB-02 Top-3 con menos de tres | Parcial | `test_ciclo_semanal_completo_apto` (motivo R14 en cada clase con < 3); segunda pasada en banda marginal: HT-03 | Superada |
| PB-03 Clase sin opciones | Parcial | `test_presupuesto_agotado_parcial_declarado` (clase con 0 opciones y semáforo GRIS); caso PS3 sembrado no automatizado | Superada |
| PB-04 Misma tendencia, estrategias por clase | LLM real | — (las lentes por clase las aplica el modelo; el ejecutor registra perfiles y cálculos en RC) | — |
| PB-05 Marco de otra clase sin justificación | LLM real | — (lo detecta el Auditor) | — |
| PB-06 Consulta N0 sin escalado | Automática | `test_consulta_n0_sin_escalado` (ruta N0, referencias existentes, sin CT-05, ≤ 1 UC con caché caliente) | Superada |
| PB-07 Consulta que escala | Automática | `test_consulta_que_escala_y_pregunta_repetida` | Superada |
| PB-08 Ráfaga de peticiones | Parcial | Idempotencia y acuse: `test_contratos_canales_credenciales_e_idempotencia`; cola: HT-08 en `test_ht04_y_ht06_y_ht08` | Superada |
| PB-09 Cambio de periodicidad | Parcial | `test_peticion_ad_hoc_y_decisiones` (CFG- por AG-01, CT-22); la reprogramación real la hace el planificador externo | Superada |
| PB-10 Configuración no permitida | Automática | `test_peticion_ad_hoc_y_decisiones` (H1 de INM y umbral E rechazados; APLICADA_PARCIALMENTE) | Superada |
| PB-11 Decisión del Broker sin alterar el análisis | Automática | `test_peticion_ad_hoc_y_decisiones` (estado de F3 intacto, `decision_broker`, CT-22) | Superada |
| PB-12 Campos de decisión y paquete para B | Automática | `test_ciclo_semanal_completo_apto` (validación con el esquema JSON V5.0 del paquete; una entrada de B por opción) | Superada |
| PB-13 GC0 negativo con arrastre verificado | Automática | `test_gc0_negativo_arrastre_verificado` (N1, ≤ 5 UC del Anexo A V5.1, solo modo ligero, sin candidatas nuevas) | Superada |
| PB-14 Arrastre con invalidación activada | Automática | `test_autocritica::test_arrastre_con_invalidacion_activada` | Superada |
| PB-15 Reglas de parada | LLM real | — | — |
| PB-16 Presupuesto agotado | Automática | `test_presupuesto_agotado_parcial_declarado` (PARCIAL, limitación en ambos informes, G3 en F6 y F7) | Superada |
| PB-17 Ampliación de presupuesto | Parcial | Registro AUT- en HA dentro de la prueba de presupuesto (autorización determinista por regla) | Superada |
| PB-18 Cola saturada y apertura de instancia | Parcial | `test_ht04_y_ht06_y_ht08` (ORD- para agente sin estado) | Superada |
| PB-19 Agente de instancia única saturado | Parcial | `test_ht04_y_ht06_y_ht08` (sin ORD- para AG-02) | Superada |
| PB-20 Instrucción incrustada | Automática | `test_instruccion_incrustada_ignorada_y_registrada`, `test_saneamiento_r9` | Superada |
| PB-21 Credencial en un mensaje | Automática | `test_contratos_canales_credenciales_e_idempotencia` (rechazo íntegro, valor no registrado) | Superada |
| PB-22 Canal no previsto | Automática | `test_contratos_canales_credenciales_e_idempotencia` | Superada |
| PB-23 Escritura fuera de reserva | Automática | `test_almacen_reserva_integridad_y_as_of` (tres INC-, F4 intacto) | Superada |
| PB-24 Enlace roto y borrado | Fuera del ejecutor | HT-02 (pruebas de `10_Herramientas`); el ejecutor solo lo invoca (`bloque-a verificar-enlaces`) | — |
| PB-25 Contenido cambiado y retractación | Fuera del ejecutor | Ídem | — |
| PB-26 Clasificación temática y orden por calidad | Fuera del ejecutor | — | — |
| PB-27 Fondo metodológico | LLM real | — | — |
| PB-28 Alimentación continua y Novedades | LLM real | — | — |
| PB-29 Contar raíces | Parcial | Deduplicación por hash y raíces por fuente en `_registrar_evidencia_clase` (cubierta por el ciclo completo) | Superada |
| PB-30 Cifra sin artefacto bloqueada | Parcial | HT-09 C08 con `artefactos` del RC en cada ciclo; retirada de opciones con bloqueo implementada | Superada |
| PB-31 Horizonte no certificado sin probabilidad | Automática | `test_ciclo_semanal_completo_apto` (prob = null y etiqueta en todos los horizontes) | Superada |
| PB-32 Certificación de un horizonte | Automática | `test_certificado_emitido_con_muestra_suficiente`, `test_metricas_de_pronostico_con_pronosticadores_sinteticos` | Superada |
| PB-33 Revocación por deterioro | Parcial | `Evaluador.revisar_certificados`: `test_ece_cero_no_revoca_un_certificado`, `test_umbral_de_revocacion_ece_sale_de_la_configuracion` (T-53); el deterioro del BSS, sin prueba dedicada | Superada |
| PB-34 Fuga en evaluación | Automática | `test_pronosticos_resueltos_sin_look_ahead`, `test_guardia_de_fuga_del_proveedor`, `test_fecha_publicacion_filtra_revisiones`, rechazo FUGA del Motor | Superada |
| PB-35 Recalibración en sombra | Parcial | Implementada (`Evaluador.recalibrar`, comparación de sombra en F6); sin prueba dedicada (exige ≥ 30 resueltos publicados) | — |
| PB-36 Recalibración fuera de bandas | Parcial | Propuesta P3-EVAL- implementada; sin prueba dedicada | — |
| PB-37 Pronóstico congelado inmutable | Automática | `test_almacen_reserva_integridad_y_as_of` (cadena de hash detecta la modificación), PRG no anulados en `test_arrastre_con_invalidacion_activada` | Superada |
| PB-38 Objeción fuerte sin resolver | Automática | `test_autocritica::test_objecion_fuerte_sin_resolver_excluye_del_top3` | Superada |
| PB-39 Legibilidad < 70 bloqueada | Parcial | HT-07 ≥ 70 comprobado en el ciclo; bloqueo y reescritura implementados (C12) | Superada |
| PB-40 Comprensión por usuarios | LLM real | Requiere usuarios | — |
| PB-41 Coherencia entre entregables | Automática | Comprobación `coherencia()` en cada entrega (falla ⇒ BLOQUEADO), ciclo completo APTO | Superada |
| PB-42 Auditoría asíncrona sin bloqueo | Parcial | F9 tras la entrega (AUD-/HAL- en HA); hallazgos reales requieren LLM | — |
| PB-43 Pregunta repetida | Automática | `test_consulta_que_escala_y_pregunta_repetida` (CT-22 y LEC- de producto) | Superada |
| PB-44 Historial de aciertos honesto | Automática | `test_pronosticos_resueltos_sin_look_ahead` (n publicado ≤ resueltos conocidos en la fecha) | Superada |
| PB-45 Lección aplicada | Parcial | Lecciones ≤ 10 inyectadas en el contexto de cada encargo; el mock de Prospectiva reacciona a lecciones de calibración | — |
| PB-46 Fiabilidad de fuentes | LLM real | No implementado (FUE-) en V1.0 | — |
| PB-47 Estados de madurez | Parcial | Rechazo `METODO_NO_IMPLEMENTADO` en `test_servicio_del_motor_rc_cache_fuga_y_reejecucion`; las fichas «Documentado» con código no dan cifras: `test_cs08_fichas_documentadas_no_entregan_cifras` (T-65) | Superada |
| PB-48 Conflicto de normas | Parcial | La invalidación determinista prevalece sobre la recomendación del Analista (R23) | — |
| PB-49 Historial íntegro | Automática | `test_almacen_reserva_integridad_y_as_of`, `test_canales_y_matriz_respetados` (integridad de todos los archivos) | Superada |
| PB-50 Horizontes según la clase | Parcial | Filtro de la tabla 8.3 y F10 en cada opción; HT-09 C06 | Superada |
| PB-51 Conocimiento en los system prompts | Fuera del ejecutor | Revisión documental | — |
| PB-52 Modo degradado | Parcial | Clase sin datos ⇒ PARCIAL (PS2); salida no conforme ⇒ PARCIAL con INC (`test_busqueda_web_solo_en_vivo_y_reparacion_json`); símbolo sin datos o con datos inválidos ⇒ excluido y declarado (`test_un_simbolo_sin_historia_no_vacia_su_tipo`, `test_h15_simbolo_con_datos_invalidos_se_excluye_y_se_declara`) | Superada |
| PB-53 Frontera A/B: activo concreto | Parcial | `test_esquema_de_finalista_sin_vehiculos` (la ficha de finalista no admite vehículos); que el Analista no proponga un activo concreto lo juzga el Auditor (R21) | Superada |
| PB-54 Encargo completo para el Bloque B | Automática | `test_ciclo_semanal_completo_apto` (una entrada de `paquete_para_bloque_B` por opción, validada con el esquema) | Superada |
| PB-55 Cobertura de los doce tipos | Automática | `test_doce_tipos_agentes_y_canales`, `test_ciclo_semanal_completo_apto` (≤ 3 opciones por tipo) | Superada |
| PB-56 Oportunidad duplicada entre tipos | Automática | `test_sin_duplicados_entre_tipos` | Superada |
| PB-57 Estrategias de los tipos nuevos | LLM real | — (lo audita el Auditor: R21 en los tipos IDX, FON, DER, MON y TCV) | — |

Pruebas adicionales exigidas por el encargo del ejecutor: guardia de fuga del proveedor, backtest de 12 semanas sintéticas con CSV y métricas coherentes (`test_backtest_12_semanas_csv_y_metricas`), certificados no emitidos con n insuficiente (`test_certificados_no_emitidos_con_n_insuficiente`), reproducibilidad con `ReplayClient` y anonimización (`test_reproducibilidad_con_replay_y_anonimizacion`, `test_anonimizacion_oculta_simbolos`), cliente Anthropic (caché de prompts, herramienta de búsqueda web, `pause_turn`, contabilidad de caché) con SDK simulado (`test_cliente_anthropic_cache_herramienta_y_pause_turn`), búsqueda web desactivada en backtest, casos de control de las fichas del Motor (`test_casos_de_control_de_las_fichas`), SCORE-RK-001 idéntico a HT-03 (`test_score_rk_identico_a_ht03`) y copias de HT-02/03/07/09 sin divergencia (`test_herramientas_de_referencia_sin_divergencia`). También: CLI de backtest y estado (`test_cli_backtest_y_estado`), fechas de HT-05 (`test_ht05_fechas`), mock determinista y UC (`test_mock_determinista_y_uc`), referencias reales con cualquier versión (`test_referencias_reales_se_cargan_con_cualquier_version`) y proveedor sintético determinista (`test_sintetico_determinista`).

## Pruebas añadidas en la adaptación a la V5.0 (`tests/test_v5.py`)

| Aspecto de la V5.0 | Prueba automática | Resultado |
|---|---|---|
| Doce tipos de activo, Analistas AG-21..AG-25 y sus canales CT-06; tabla 8.3 | `test_doce_tipos_agentes_y_canales` | Superada |
| Presupuestos del Anexo A (N1 5, N2 18, N3 50, ciclo ≤ 240 UC), modelos AG-21..AG-25 y referencias de 8.4 | `test_configuracion_por_defecto_v5`, `test_referencias_de_comparacion` | Superada |
| Carga de prompts por nombre del agente con cualquier sufijo de versión, NFC/NFD, nombres anteriores y modo degradado con el marco común | `test_busqueda_de_archivos_versionados`, `test_prompts_de_los_analistas_nuevos_y_modo_degradado` | Superada |
| Universo de ámbitos con indicador de seguimiento; compatibilidad de `tipo_opcion` V4.x | `test_universo_de_ambitos_con_indicador` | Superada |
| Frontera con el Bloque B: ficha de finalista sin vehículos, con ámbito, indicador, invertibilidad y encargo | `test_esquema_de_finalista_sin_vehiculos`, `test_integracion::test_ciclo_semanal_completo_apto` | Superada |
| Regla 5 de 2.6: ninguna oportunidad en dos top-3 | `test_sin_duplicados_entre_tipos` (y C16 de HT-09 en `10_Herramientas`) | Superada |
| `senales.csv` con `tipo_activo`, `subtipo`, `ambito`, `indicador_seguimiento_simbolo` y alias `proxy_backtest` | `test_integracion::test_backtest_12_semanas_csv_y_metricas` | Superada |

## Pruebas añadidas en la actualización V5.1 (`tests/test_v51.py`)

| Prueba del plan / aspecto de la V5.1 | Cobertura | Prueba automática | Resultado |
|---|---|---|---|
| Tabla 8.3 con H5, naturalezas y rangos del horizonte principal | Automática | `test_tabla_y_naturalezas` | Superada |
| PB-65 Horizonte principal coherente con la naturaleza en cada opción | Automática | `test_horizonte_principal_y_naturaleza_en_cada_opcion`, `test_ht09_bloquea_h5_sin_hitos` (C17) | Superada |
| PB-63 H5 solo con banda y ≥ 3 hitos HIT- congelados en F4; JSON conforme al esquema V5.1 | Automática | `test_h5_con_hitos_y_sin_probabilidad`, `test_ht09_bloquea_h5_sin_hitos` (C18) | Superada |
| PB-64 Evaluación de H5 por hitos y degradación | Automática | `test_estado_h5_por_hitos`; degradación en F6 y F10 y efecto en el ciclo: `test_degradacion_h5_se_aplica_en_f6_y_f10`, `test_h05_degradacion_h5_cambia_la_tabla_del_ciclo_siguiente` (T-53), `test_h13_la_degradacion_registra_el_efecto_desde_el_mismo_ciclo` (T-65) | Superada |
| CT-23 a CT-25 en el catálogo de canales; solo el Coordinador habla con el Broker (R3) | Automática | `test_canales_v51` | Superada |
| F11: escritura reservada a AG-01 | Automática | `test_f11_reserva_de_escritura` | Superada |
| PB-66 Seguimiento encargado: alta, ciclo C6, informe validado (HT-09 y esquema), pausa, reanudación, cancelación inmediata, aviso al Evaluador | Automática | `test_seguimiento_alta_ciclo_y_cancelacion`, `test_seguimiento_frecuencia_corta_y_opp_inexistente` | Superada |
| PB-61 Consulta BLOQUEANTE: pausa del tipo afectado, vencimiento con supuesto declarado (C19), respuesta tardía | Automática | `test_consulta_bloqueante_pausa_y_vencimiento` | Superada |
| PB-62 Validación, agrupación (máx. 3 por RUN-), recurrencia y aportación espontánea | Automática | `test_consulta_validaciones_agrupacion_y_entrante` | Superada |
| PB-58, PB-59, PB-60 Credenciales: solicitud, rechazo del valor en un mensaje, depósito en la bóveda, denegación y recordatorio | Automática | `test_credenciales_boveda`, `test_cli_v51` | Superada |
| PB-67 Recomendación PROPONER_ENVIO_A_B | Parcial (perfil SEGUIMIENTO de HT-09) | `10_Herramientas/tests/test_ht09_validador_g3.py::TestV51::test_seguimiento_envio_a_b` | Superada |

## Pruebas de las revisiones T-53, T-66 y T-65

Regresiones de cada hallazgo corregido; el detalle, en el `pruebas.md` de cada ticket (`.docs/tickets/T-NN/`).

| Archivo | Qué cubre |
|---|---|
| `tests/test_t53_seleccion_y_entrega.py` | T-53: continuidad (CA-01), hitos H5 (CA-11), entrega bloqueada (CA-03), consultas bloqueantes (CA-04), PS1 (CA-05), símbolos sin historia (CA-06), PS2 en sesiones (CA-14), siguiente paso y semáforo (CS-17), horizonte del Analista (CS-01) y hallazgos H-01 a H-05 y H-12 de su QA |
| `tests/test_t53_evaluacion_y_almacen.py` | T-53: cierres inválidos (CA-02), Holm (CA-07), hitos fuera de H4 (CA-08), congelación de F4 (CA-09), bóveda (CA-10), ECE 0 (CA-13), monitor (CS-03), bandas (CS-05) y degradación de H5 (CS-12) |
| `tests/test_t66_propuestas.py`, `tests/test_t66_evaluacion.py` | T-66: propuestas PA-01, PA-03, PA-05, PA-09, PA-10, PA-14 y PA-21, H-06 de T-65 y hallazgos de su QA |
| `tests/test_t65_hallazgos.py` | T-65: hallazgos H-07 a H-21 de las QA de T-53 y T-66 |
| `tests/test_t65_resto_t53.py` | T-65: resto técnico de T-53 (CA-14, CA-15, CS-08, CS-10, CS-11, CS-18, CS-19 y CS-23) |
