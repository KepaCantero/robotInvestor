# Esquema de archivo operativo — F3 Registro de análisis, recomendaciones y candidatos

**Bloque B · Robot Investor · Versión óptima V2.0 · actualizado V2.1, 03/11/2026** · Subordinado al Documento 0 del Bloque B óptima V2.1 (ante discrepancia, manda el Documento 0).

---

## 1. Propósito

F3 es la **memoria analítica** del Bloque B (Documento 0, 5.1 y 15). Conserva, por petición: la oportunidad tal como se recibe y normaliza (OPP-B), el **plan de análisis** versionado (PLAN-B), las **hipótesis** (HIP-B), el **análisis entregado con su veredicto** (REC-B: ámbito, tipo de objeto, estrategia, tesis, puntuaciones A/E/C, puertas PA, veredicto, régimen, escenarios, invalidación, mapa de cobertura, plan de seguimiento y, desde la V2.1, capas y puertas de viabilidad, `mapa_cadena_valor` con sus eslabones ESL- y emergentes EMG-B, consultas y supuestos aplicados, lista de comprobación profesional y seguimientos encargados activos), los **candidatos** (CAND-B: tipo, identificadores, `eslabon_id`, S y desglose, IC, puertas PC, veredicto, encargo C.x), las **objeciones** de la refutación con su respuesta (OBJ-B) y las **señales** del plan de seguimiento (SIG-). Tras la entrega, el Evaluador (función de Vigía) añade los campos de seguimiento, los estados de vigilancia, la decisión del Broker y los resultados.

Es la base de: GC0 y la memoria de F0 (análisis previos del mismo ámbito o solapados); las respuestas N0; el Vigía (rondas sobre REC-B vigentes); la evaluación de veredictos y de rankings (sección 12); y el historial de aciertos que cada entrega publica.

**No es**: la evidencia (F2), los pronósticos (F4), la Biblioteca reutilizable (F6) ni los entregables (ENT). Los referencia por identificador.

## 2. Propietario, lectores y contratos

| Campos | Escritor | Momento |
|---|---|---|
| Altas y contenido analítico (OPP-B, PLAN-B, HIP-B, REC-B, CAND-B, OBJ-B, SIG-) y borradores en puntos de control | AG-B02 Director del Análisis de Mercado (una instancia por petición; escrituras serializadas por PET-B) | F0–F7 (borrador); F10 (alta definitiva tras la autorización de salida) |
| Campos de seguimiento: `seguimiento`, `estado_vigilancia`, `rondas`, `resultado`, `decision_broker` | AG-B23 Evaluador (función de Vigía y de evaluación) | F11–F12 y a la recepción de CT-B-26 |

**Lectores**: todos los agentes (matriz 5.1). **Contratos**: CT-B-08 (retorno del Director), CT-B-09, CT-B-10, CT-B-16, CT-B-17 (insumos que el Director consolida), CT-B-25 (alertas que nacen de F3), CT-B-26 (decisiones del Broker que el Evaluador anota). **Herramientas**: HT-03 (puntuaciones, puertas y veredictos), HT-06 (índice), HT-09 (G3 lee F3), HT-05 (programa las rondas del Vigía a partir de SIG-).

**Interpretación declarada**: el Documento 0 sitúa la decisión del Broker «en campo propio» de F3 sin nombrar su escritor; este esquema la asigna a AG-B23, que la recibe por CT-B-26 y es propietario de los campos de seguimiento (regla más restrictiva: no se abre un escritor nuevo).

## 3. Reglas

1. **Append-only** (5.2.1): un REC-B o un CAND-B entregado nunca se reescribe; las correcciones son versiones nuevas con `supersedes`; los estados de vigilancia cambian por entradas nuevas del `historial`. Nunca se borra un REC-B (9.10).
2. **Borradores aislados** (R6; 9.9): lo que el Director registra en un punto de control lleva `estado_registro = BORRADOR` y `pet_id`; ningún otro análisis puede leerlo como memoria. Solo un REC-B `ENTREGADO` es reutilizable (y la Biblioteca F6, que se actualiza con él).
3. **Veredictos congelados a la entrega**: el veredicto del ámbito y el de cada candidato quedan fijos; el Vigía nunca los modifica (R32), solo cambia el estado de vigilancia.
4. **Orden de cálculo del veredicto** (9.3): veredicto provisional del ámbito con A, E, C y PA1–PA8 → veredictos de los candidatos → veredicto final (si no hay ningún PRIORITARIO_PARA_C, el ámbito baja a VIGILAR con motivo «sin vehículo de captura adecuado»). Las tres etapas se registran.
5. **Puntuaciones reconstruibles**: todo total (A, E, C, S) lleva su desglose, los pesos vigentes de F10 y el `calc_id` o la ejecución de HT-03 que lo produjo (PA7, PC7).
6. **Menos es legítimo** (R21): un tipo de activo sin prioritarios lleva `menos_de_N_motivo` con cuántos se analizaron, por qué no llegaron y qué tendría que ocurrir.
7. **Universo completo trazable**: por cada tipo aplicable se conserva la referencia al artefacto del universo cribado (RC; hoja del anexo de datos) con todos sus miembros, sus métricas, su S provisional o completo y su motivo de exclusión. Es la base de la referencia del ranking (media equiponderada del universo cribado) y de la evaluación sin sesgo de supervivencia (12.6).
8. **Decisiones del Broker en campo propio** (`decision_broker`): no alteran el estado analítico ni la evaluación (7.8).
9. **Señales `FLUCTUACION`** solo se registran aquí (en `rondas`); no generan alerta (B.7).
10. **Sin datos personales** ni referencias a la cartera del usuario (R11).
11. **Paradas en puerta (V2.1, 7.11)**: un análisis detenido en PV1 o PV2 genera igualmente su REC-B con `resultado_del_analisis = DETENIDO_EN_PUERTA` y veredicto DESCARTAR (sugerencia descartar) o VIGILAR (sugerencia seguimiento), sin CAND-B, encargos C.x ni PRG-B; el Evaluador lo usa para medir los falsos negativos de las puertas (12.7).
12. **Eslabón en todo candidato (V2.1, 9.13)**: cada CAND-B lleva `eslabon_id` (ESL- del `mapa_cadena_valor` de su REC-B; `ESL-00` si el ámbito no tiene cadena desglosable) y `origen_seleccion` (TOP_N · MEJORES_POR_ESLABON · ALTERNATIVA). Las opciones por eslabón son adicionales al top-N y no lo duplican; tras PV3 no superada se registran como indicativas, sin PRIORITARIO_PARA_C.
13. **Identificadores ESL- y EMG-B**: ESL- es único dentro de su REC-B (Anexo C); EMG-B identifica un emergente del radar de AG-B24 y se reutiliza en F6.

## 4. Formato de entrada

### 4.1 Oportunidad recibida (OPP-B)

`opp_id` (`OPP-B-AAAA-NNNN`; el REC-B posterior conserva el mismo ordinal), `pet_id`, `origen` (BLOQUE_A · LIBRE), `opp_id_A`, `ambito_recibido` `{incluye, excluye, region}`, `tesis_recibida` y `mecanismo` (pistas, R31), `tipo_objeto_asignado` (seis tipos de 2.5) con `motivo` y `acentos_secundarios`, `correspondencia_A` (tabla E.2), `tipos_activo_aplicables` `{codigo, exposicion_material sí/no, motivo}` para los doce, `horizonte_dominante` y `solapamientos` con justificación, `preguntas_decisivas` (del Broker, `preguntas_para_B` y propias), `estado_registro` (BORRADOR · CERRADA_EN_REC).

### 4.2 Plan de análisis (PLAN-B, versionado)

| Campo | Tipo | Oblig. | Valores / formato |
|---|---|---|---|
| `plan_id` | Identificador | Sí | `PLAN-B-AAAA-NNNN-vN` |
| `pet_id` / `opp_id` | Identificadores | Sí | — |
| `version_motivo` | Texto | Si vN > 1 | Opción (b) o (c) de la puerta de tiempo, subsanación, desbloqueo |
| `estrategia` | Objeto | Sí | `{matriz_base (columna de 8.3.1), moduladores_horizonte, moduladores_activo, pesos_modulados D1…D12, desviaciones_director [{dim, delta (±5), justificacion}], pesos_efectivos, profundidad P0…P3 por dimensión, exclusiones [{dim, motivo_sustantivo, momento, condicion_reapertura}]}` |
| `especialistas` | Lista | Sí | `{agente AG-B03…B11, papel L·A·C, dimension, disparador (si C), instancias}` |
| `perfiles_motor` / `playbooks` | Listas | Sí | PERF-B-… / SEL-… por tipo aplicable |
| `playbook_horizonte` | Objeto | Sí | `{horizonte, familias_dominantes, excepciones_registradas}` (8.6) |
| `hipotesis` | Lista | Sí | HIP-B (tesis de partida y competidoras; 1 en N1, 2 de naturaleza distinta en N2, ≥ 2 en N3) |
| `despliegue_estructural_previsto` | Objeto | Sí | `{alcance N1 eslabón crítico·N2 relevantes·N3 completa, eslabones, eslabon_critico}` |
| `maquina_proyecciones` | Objeto | Sí | `{activada sí/no, motivo_exclusion}` (8.8) |
| `tipos_activo` / `top_n` | Lista / objeto | Sí | Por tipo: N, alternativas |
| `calculos_previstos` | Lista | Sí | `{metodo, perfil, plan MIN·STD·EXT, valor_informativo}` |
| `reutilizacion_F6` | Objeto | Sí | `{gc0 resultado, mkt_id, dimensiones_reutilizadas, dimensiones_caducadas, cambio_material}` |
| `grafo` | Objeto | Sí | `{nodos [{nodo_id, tipo OBLIGATORIO·CONDICIONAL·EXCLUIBLE, agente, dimension, depende_de[], paralelizable, disparador, motivo_exclusion, estimacion_min}], esperas, bloqueados [{nodo, dato_que_desbloquea}]}` |
| `criterios_parada_ampliacion` | Lista | Sí | 10.5 y particulares |
| `riesgos_encuadre` | Lista | Sí | Columna «riesgo de encuadre» de 2.5 y propios |

### 4.3 Hipótesis (HIP-B)

`hip_id` (`HIP-B-AAAA-NNNN-k`; k = 0 para la tesis de partida), `enunciado`, `naturaleza` (p. ej., cíclica, estructural, de valoración, de flujo), `discriminante`, `indicador_anticipado`, `invalidacion`, `busquedas_discriminacion` (msg_id de CT-B-11 con objetivo «refutar» o «confirmar»), `estado` (confirmada · debilitada · indeterminada · invalidada), `evidencia` (CLM-B), `cerrada_en` (F3 de la petición).

### 4.4 Análisis entregado (REC-B)

| Campo | Tipo | Oblig. | Valores / formato |
|---|---|---|---|
| `rec_id` | Identificador | Sí | `REC-B-AAAA-NNNN` (ordinal de su OPP-B) |
| `pet_id` / `run_ids` / `plan_id` | Identificadores | Sí | — |
| `estado_registro` | Enumerado | Sí | BORRADOR · ENTREGADO · SUSTITUIDO (por versión corregida) |
| `fecha_entrega` / `data_cutoff` / `methodology_version` | Fecha / fecha / texto | Sí | `data_cutoff` idéntico en los seis entregables (o en el informe de parada) |
| `ambito` | Objeto | Sí | `{nombre, nombre_llano, tipo_objeto, incluye, excluye, region, mkt_id}` |
| `estrategia` | Objeto | Sí | Resumen de PLAN-B efectivo (B.9 `estrategia`) |
| `regimen` | Identificador | Sí | RGM-B (F6) con `estado_confianza` |
| `tesis` | Objeto | Sí | `{enunciado, premisas [{premisa, evidencia CLM-B, comprobacion, horizonte, invalidacion, sensibilidad}], hipotesis (HIP-B y estado)}` o `sin_tesis_defendible` con motivo (R15) |
| `evaluaciones_separadas` | Objeto | Sí | `{mercado, calidad_ambito, atractivo_bursatil, accesibilidad}` |
| `puntuaciones` | Objeto | Sí | `{A, E, C, RF, RE, desglose {A, E, C}, pesos_F10 (cfg_ids), segunda_pasada [{puntuacion, componentes, valor_1, valor_2, usado}], tope_saturacion aplicado sí/no, tope_C_E10 aplicado sí/no, cambios_15_vs_previo [{puntuacion, de, a, justificacion}]}` |
| `puertas_ambito` | Objeto | Sí | PA1…PA8: `{resultado OK·BLOQUEA, motivo, veredicto_maximo}` |
| `veredicto` | Objeto | Sí | `{provisional, final, valor INVERTIR·INVERTIR_ESCALONADO·VIGILAR·DESCARTAR, horizonte, condiciones_entrada[], tramos[], disparadores[], motivo_descarte, resultado_del_analisis (V2.1: incluye DETENIDO_EN_PUERTA) CONCLUYENTE·PARCIAL·NO_CONCLUYENTE·BLOQUEADO, relevancia_decisional, reversibilidad, siguiente_paso_sugerido, que_cambiaria_la_conclusion[]}` |
| `escenarios` | Lista | Sí | `{nombre base·favorable·adverso, premisas, regimen, probabilidad (solo con base calibrable o certificado), banda, resultado_vs_referencia, calc_ids}` |
| `sensibilidades` / `robustez` | Objeto | Sí | `{tornado, sobol (EXT), RE, calc_ids}` |
| `pronosticos` | Lista | Sí | PRG-B (F4); con horizonte principal H5, al menos tres `HITO_H5` con fecha a 1–5 años |
| `capas` | Objeto | Sí (V2.1) | `{ejecutadas [0…4], puertas_viabilidad {PV1, PV2, PV3: SUPERADA·NO_SUPERADA·FORZADA·NO_EVALUADA}, continuacion_forzada {puerta, motivo, via} o null, por_capa_min}` (7.10) |
| `mapa_cadena_valor` | Objeto | Sí (V2.1) salvo parada | B.16 íntegro: eslabones ESL- (métricas, cuello con PCB, atractivo AE, opciones, emergentes EMG-B), omisiones, síntesis; ruta del entregable 6 |
| `consultas_broker` / `supuestos_aplicados` | Listas | Sí (V2.1) | CNS-B de la petición con su resolución; supuestos aplicados por falta de respuesta (7.12) |
| `lista_profesional` | Lista | Sí (V2.1) | 22 ítems de 8.10 con estado TRATADO (con referencia) · NO_APLICABLE (con motivo) · LAGUNA (declarada en limitaciones) |
| `horizontes_secundarios` | Lista | No (V2.1) | H1…H5 |
| `informe_parada` | Objeto | Si DETENIDO_EN_PUERTA | B.15 íntegro y rutas ENT |
| `seguimientos` | Lista | No (V2.1) | SEG-B activos del archivo F11 sobre este REC-B (anotados por el Coordinador; no cambian el estado analítico) |
| `riesgos` / `catalizadores` / `invalidacion` | Listas | Sí | Riesgos con mecanismo y señal temprana; catalizadores fechados |
| `riesgo_1a5` | Entero | Sí | Escala del Anexo A |
| `despliegue_estructural` | Objeto | Sí | Plantillas 4a–4e cumplimentadas (o referencia a su sección del informe técnico) |
| `proyecciones` | Objeto | Si máquina activada | Etapas 1–5 de 8.8 con premisas y CALC-B |
| `candidatos_por_tipo` | Objeto | Sí | Claves = los doce códigos: `{aplicable, motivo (si no aplica), universo {tamano, fuentes, fecha, universo_ref CALC-B}, excluidos_por_motivo, top_n [CAND-B], alternativas [CAND-B], sustituciones_diversidad, menos_de_N_motivo}` |
| `apuestas_independientes` | Entero | Sí | 9.7.5 |
| `contraste_adversarial` | Lista | N2/N3 | OBJ-B con su desenlace (aceptada · resuelta · mantenida como incertidumbre abierta) |
| `steelman_contrario` | Texto | Sí | 11.1 |
| `protocolo_antisesgo` | Objeto | Sí | Lista de verificación del Director (anclaje, confirmación, extrapolación, disponibilidad, exceso de confianza, narrativa, consenso) |
| `mapa_cobertura` | Objeto | Sí | `{directas, indirectas, perdedores_sistematicos, investigado, excluido_con_motivo, vigilancia_informativa, vigilancia_pre_salida [{actor, caducidad}]}` (8.7) |
| `plan_de_seguimiento` | Objeto | Sí | B.11 íntegro; las señales se dan de alta como SIG- (4.7) |
| `origen_contraste` | Objeto | Si BLOQUE_A | `{confirmado[], refutado[], sin_verificar[]}` (E.2) |
| `limitaciones` / `lagunas` / `reservas_auditoria` | Listas | Sí | — |
| `entregables` | Objeto | Sí | Rutas ENT |
| `supersedes` | Identificador | No | REC-B anterior del mismo ámbito o versión corregida |
| **Campos del Evaluador** | | | |
| `estado_vigilancia` | Enumerado | Sí tras entrega | Sección 5 |
| `rondas` | Lista append-only | — | `{fecha_corte, sig_id, valor, clasificacion FLUCTUACION·REVISION·INVALIDACION_PROBABLE·INVALIDACION_CONFIRMADA, alr_id o null, calc_id}` |
| `decision_broker` | Objeto | — | `{decision, fecha, ret_id}` (anotada a partir de CT-B-26) |
| `resultado` | Objeto | — | `{rentabilidad_relativa_vs_referencia, acierto_veredicto, prg_resueltos, calc_id, fecha}` |

### 4.5 Candidato (CAND-B)

| Campo | Tipo | Oblig. | Valores / formato |
|---|---|---|---|
| `cand_id` | Identificador | Sí | `CAND-B-AAAA-NNNN` |
| `pet_id` / `rec_id` | Identificadores | Sí | — |
| `tipo_activo` / `tipo_subyacente` | Enumerados | Sí / si FON | Doce códigos; regla de asignación de 2.6 aplicada (`regla_asignacion` 1–5) |
| `playbook` | Enumerado | Sí | SEL-RV … SEL-TCV |
| `instrumento` | Objeto | Sí | `{nombre, isin, ticker, mercado, divisa, tipo_instrumento, emisor_id}` |
| `fase_alcanzada` | Enumerado | Sí | UNIVERSO · CRIBADO · FINALISTA (GC3) · TOP_N · ALTERNATIVA |
| `puertas` | Objeto | Sí | PC1…PC8: `{resultado OK·FALLA·NO_EVALUADA (motivo), detalle}` |
| `pureza` | Objeto | Sí | `{metrica, valor, minimo_PC2, fuente DAT-B·CALC-B, metodo publicado·estimado}` |
| `alertas` | Lista | Sí | `{senal, valor, critica sí/no, verificar_en_C}` (PC4) |
| `eslabon_id` | Identificador | Sí (V2.1) | ESL- del `mapa_cadena_valor` (ESL-00 sin cadena desglosable) |
| `origen_seleccion` | Enumerado | Sí (V2.1) | TOP_N · MEJORES_POR_ESLABON · ALTERNATIVA |
| `opcion_eslabon` | Objeto | Si figura en una tabla por eslabón | `{rango, rol_en_eslabon, pureza_eslabon, en_top_n_tipo, indicativa (PV3 no superada) sí/no, motivo}` |
| `emg_id` | Identificador | Si procede de un emergente invertible | EMG-B (vía COTIZADA_DIRECTA · MATRIZ_COTIZADA · ETF_O_FONDO) |
| `S` | Objeto | Si FINALISTA o superior | `{provisional (MIN), final, desglose PE·QL·VA·MO·RI·LA·CO (NA·NE), pesos (cfg_id), ic90_S, rango, ic90_rango, frontera sí/no, segunda_pasada, calc_ids}` |
| `traduccion_rasgos` | Lista | Sí | `{rasgo_tesis, metrica, componente, cumple}` (9.5.6) |
| `diversidad` | Objeto | Sí | `{regla_aplicada 1–5, desplazado_por o desplaza (CAND-B), S_desplazado, exposicion_compartida (CAND-B de otro tipo)}` |
| `objeciones` | Lista | Si finalista N2/N3 | OBJ-B |
| `veredicto` | Objeto | Sí | `{valor PRIORITARIO_PARA_C·SECUNDARIO·EXCLUIDO, motivo_exclusion (D.5), rol_en_tesis, bloque_destino C.1…C.12}` |
| `encargo_C` | Objeto | Si PRIORITARIO o SECUNDARIO del top-N, o PRIORITARIO de una tabla por eslabón | `paquete_para_bloque_C` íntegro (B.10), con `eslabon_id`, `origen_seleccion` y `contexto_eslabon` |
| **Campos del Evaluador** | | | |
| `estado_vigilancia` | Enumerado | — | VIGENTE · ALERTA · INVALIDADO · CERRADO |
| `decision_broker` | Objeto | — | `{decision ENVIADO_A_C·EN_VIGILANCIA·DESCARTADO, bloque_c, fecha, ret_id}` |
| `valoracion_bloque_C` | Objeto | — | Lo que el Broker comunique (CT-B-04), sin reinterpretar |
| `resultado` | Objeto | — | `{rentabilidad_relativa_vs_universo, horizonte, calc_id}` |

### 4.6 Objeción (OBJ-B)

`obj_id` (`OBJ-B-AAAA-NNNN`), `objeto` (TESIS · CAND-B-…), `tipo` (explicación alternativa, evidencia contraria, sesgo, riesgo omitido, «qué tendría que ser cierto», trampa de valor, contabilidad agresiva, pureza sobreestimada, liquidez ilusoria, duplicación de exposición), `fuerza` (fuerte · moderada · debil), `argumento`, `evidencia`, `que_la_resolveria`, `respuesta` `{responde DIR·SEL, texto, evidencia, estado ACEPTADA·RESUELTA·SIN_RESOLVER}`, `efecto` (PA5 · PC5 · ninguno).

### 4.6 bis Emergente del radar (EMG-B, V2.1)

`emg_id` (`EMG-B-AAAA-NNNN`), `rec_id`, `eslabon_id`, `nombre`, `tipo` (STARTUP · SCALE_UP · SPIN_OFF_UNIVERSITARIO · SPIN_OFF_CORPORATIVO · SALIDA_A_BOLSA_RECIENTE), `financiacion_conocida` `{importe, divisa, ultima_ronda, fecha, fuente EVD-B}`, `tecnologia_o_ventaja`, `senales_traccion`, `via_exposicion` (COTIZADA_DIRECTA · MATRIZ_COTIZADA · ETF_O_FONDO · FUTURA_SALIDA_A_BOLSA · NO_INVERTIBLE_HOY), `instrumento_exposicion` `{nombre, isin, cand_id, fuera_de_filtros}`, `criterios` (seis criterios de PEM, propuestos por AG-B24), `PEM` (agregado por MC-B07 con la aritmética de HT-03 y confirmado por el Director), `calc_id`, `riesgos`, `etiqueta`, `vigilancia` (sí si no es invertible hoy: pasa al `mapa_cobertura`).

### 4.7 Señal del plan de seguimiento (SIG-)

`sig_id` (`SIG-AAAA-NNNN`), `rec_id`, `nombre`, `serie` (HT-01), `frecuencia` (Anexo A según horizonte), `umbral_fluctuacion` `{min, max}`, `umbral_revision`, `umbral_invalidacion`, `direccion`, `criterio_cambio_estructural`, `afecta_a` (AMBITO · CAND-B), `catalizador_asociado`, `vigente_hasta`, `programada_ht05` (sí/no).

## 5. Estados y transiciones

| Objeto | Transiciones (escritor) |
|---|---|
| REC-B (registro) | BORRADOR → ENTREGADO (Director, F10) → SUSTITUIDO (versión corregida); V2.1: BORRADOR → ENTREGADO con `resultado_del_analisis = DETENIDO_EN_PUERTA` (informe de parada) → SUSTITUIDO si el Broker fuerza la continuación y se entrega el análisis completo |
| REC-B (vigilancia) | VIGENTE → EN_REVISION (alerta de revisión o invalidación probable comunicada) → VIGENTE · INVALIDADA (condición confirmada) · CERRADA (horizonte vencido, sustituida por un análisis nuevo del mismo ámbito o retirada por el Broker) — Evaluador |
| CAND-B (veredicto) | Congelado a la entrega |
| CAND-B (vigilancia) | VIGENTE → ALERTA → VIGENTE · INVALIDADO; cualquiera → CERRADO — Evaluador |
| HIP-B | ABIERTA → confirmada · debilitada · indeterminada · invalidada (Director, F3) |
| OBJ-B | ABIERTA → ACEPTADA · RESUELTA · SIN_RESOLVER |
| PLAN-B | vN VIGENTE → vN+1 VIGENTE (vN queda SUSTITUIDA) |

## 6. Índices de consulta

| Índice | Clave | Uso |
|---|---|---|
| Por ámbito | `ambito.mkt_id`, `tipo_objeto`, `region` | F0 (memoria y GC0); N0 |
| Vigentes en vigilancia | `estado_vigilancia` = VIGENTE · EN_REVISION | Rondas del Vigía (HT-05); criterio de separación (> 150) |
| Candidatos por instrumento | `instrumento.isin`, `emisor_id` | Candidatos ya analizados o enviados a C; exposición compartida |
| Por veredicto y tipo | `veredicto.valor`, `tipo_activo`, `playbook` | Evaluación por celda; historial de aciertos |
| Universos | `universo_ref` | Referencia equiponderada del ranking; backtesting sin supervivencia |
| Objeciones sin resolver | `OBJ-B.respuesta.estado` = SIN_RESOLVER | PA5, PC5; G3 |
| Borradores | `estado_registro` = BORRADOR | Reanudación desde punto de control (solo la propia PET-B) |
| Por eslabón (V2.1) | `eslabon_id`, `mapa_cadena_valor.eslabones.eslabon_id` | Entregable 6, encargos por eslabón, ciclos de seguimiento |
| Detenidos en puerta (V2.1) | `resultado_del_analisis` = DETENIDO_EN_PUERTA, `capas.puertas_viabilidad` | Falsos negativos de las puertas (12.7) |
| Emergentes (V2.1) | `emg_id`, `via_exposicion` | Vigilancia pre-salida a bolsa; radar de la Biblioteca |

## 7. Ejemplo ficticio

> **EJEMPLO FICTICIO — no es una entrada real.** Nombres, ISIN y cifras inventados.

```json
{"cand_id":"CAND-B-2026-0044","pet_id":"PET-B-2026-0007","rec_id":"REC-B-2026-0007","tipo_activo":"RV","tipo_subyacente":null,"playbook":"SEL-RV",
 "instrumento":{"nombre":"Empresa Ficticia de Empaquetado SA","isin":"XX0000000001","ticker":"FICT","mercado":"Mercado regulado ficticio","divisa":"EUR","tipo_instrumento":"accion","emisor_id":"EMI-0001-FICTICIO"},
 "fase_alcanzada":"TOP_N","puertas":{"PC1":{"resultado":"OK"},"PC2":{"resultado":"OK"},"PC3":{"resultado":"OK"},"PC4":{"resultado":"OK"},"PC5":{"resultado":"OK"},"PC6":{"resultado":"OK"},"PC7":{"resultado":"OK"},"PC8":{"resultado":"OK"}},
 "pureza":{"metrica":"% ingresos","valor":0.58,"minimo_PC2":0.25,"fuente":"DAT-B-2026-0031","metodo":"publicado"},
 "alertas":[{"senal":"dilución > 10 %/año","valor":"11,2 %","critica":false,"verificar_en_C":true}],
 "S":{"provisional":74,"final":76,"desglose":{"PE":82,"QL":71,"VA":68,"MO":80,"RI":64,"LA":90,"CO":null},"ic90_S":[70,81],"rango":2,"ic90_rango":[1,4],"frontera":false,"segunda_pasada":false,"calc_ids":["CALC-B-2026-0140"]},
 "traduccion_rasgos":[{"rasgo_tesis":"capacidad instalada en Europa","metrica":"% capacidad en el EEE","componente":"PE","cumple":true}],
 "diversidad":{"regla_aplicada":null,"exposicion_compartida":"CAND-B-2026-0061"},
 "objeciones":["OBJ-B-2026-0012"],
 "veredicto":{"valor":"PRIORITARIO_PARA_C","motivo_exclusion":null,"rol_en_tesis":"eslabón cuello de botella; ganador si persiste la escasez","bloque_destino":"C.1"},
 "encargo_C":{"…":"paquete_para_bloque_C (B.10)"},"estado_vigilancia":"VIGENTE","decision_broker":null}
```
