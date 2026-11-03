# Mapa del Plan de pruebas V2.0 → pruebas automáticas del ejecutor

**Bloque A · Robot Investor · Ejecutor programático V1.1 · Versión óptima V5.0 · 02/11/2026** · Subordinado al Documento 0 óptima V5.0.

Cobertura de las 52 pruebas del `09_Pruebas/Plan de pruebas del Bloque A - V3.0.md` por la batería `pytest` de esta carpeta, ejecutada con `MockClient` (respuestas sintéticas deterministas). Resultado de la última ejecución en `RESULTADOS.txt`.

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
| PB-12 Campos de decisión y paquete para B | Automática | `test_ciclo_semanal_completo_apto` (validación con el esquema JSON V4.0; una entrada de B por opción) | Superada |
| PB-13 GC0 negativo con arrastre verificado | Automática | `test_gc0_negativo_arrastre_verificado` (N1, ≤ 5 UC del Anexo A V5.0, solo modo ligero, sin candidatas nuevas) | Superada |
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
| PB-33 Revocación por deterioro | Parcial | Regla implementada en `Evaluador.revisar_certificados`; sin prueba dedicada | — |
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
| PB-47 Estados de madurez | Parcial | Rechazo `METODO_NO_IMPLEMENTADO` en `test_servicio_del_motor_rc_cache_fuga_y_reejecucion` | Superada |
| PB-48 Conflicto de normas | Parcial | La invalidación determinista prevalece sobre la recomendación del Analista (R23) | — |
| PB-49 Historial íntegro | Automática | `test_almacen_reserva_integridad_y_as_of`, `test_canales_y_matriz_respetados` (integridad de todos los archivos) | Superada |
| PB-50 Horizontes según la clase | Parcial | Filtro de la tabla 8.3 y F10 en cada opción; HT-09 C06 | Superada |
| PB-51 Conocimiento en los system prompts | Fuera del ejecutor | Revisión documental | — |
| PB-52 Modo degradado | Parcial | Clase sin datos ⇒ PARCIAL (PS2); salida no conforme ⇒ PARCIAL con INC (`test_busqueda_web_solo_en_vivo_y_reparacion_json`) | Superada |

Pruebas adicionales exigidas por el encargo del ejecutor: guardia de fuga del proveedor, backtest de 12 semanas sintéticas con CSV y métricas coherentes (`test_backtest_12_semanas_csv_y_metricas`), certificados no emitidos con n insuficiente (`test_certificados_no_emitidos_con_n_insuficiente`), reproducibilidad con `ReplayClient` y anonimización (`test_reproducibilidad_con_replay_y_anonimizacion`, `test_anonimizacion_oculta_simbolos`), cliente Anthropic (caché de prompts, herramienta de búsqueda web, `pause_turn`, contabilidad de caché) con SDK simulado (`test_cliente_anthropic_cache_herramienta_y_pause_turn`), búsqueda web desactivada en backtest, casos de control de las fichas del Motor, SCORE-RK-001 idéntico a HT-03 y copias de HT-02/03/07/09 sin divergencia.

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

