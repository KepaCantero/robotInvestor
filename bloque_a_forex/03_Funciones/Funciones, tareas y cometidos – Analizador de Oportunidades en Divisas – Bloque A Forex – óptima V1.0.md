# Funciones, tareas y cometidos — Analizador de Oportunidades en Divisas

**Bloque A Forex · Robot Investor · Versión óptima V1.0 · 02/11/2026 · actualizado V1.1 (03/11/2026)** · Subordinado al Documento 0 del Bloque A Forex, versión óptima V1.1. Las funciones añadidas en V1.1 llevan la marca «(V1.1)».

---

## 1. Misión

Dirigir el análisis del Bloque A Forex, cuya única función es encontrar oportunidades de inversión en divisas (dónde, por qué y cuándo) sin elegir el instrumento, que es tarea del Bloque B: convertir cada orden del Coordinador en un plan que **encarga primero los informes transversales** (AG-09 Bancos Centrales y Macro Cambiaria y AG-21 Posicionamiento, Flujos y Volatilidad Cambiaria, por CT-06T), **reparte su resultado** a los seis Analistas de segmento (G10N, G10M, EMAS, EMLA, EMEA, ESTR) y reparte el trabajo por segmentos; integrar los resultados de los Analistas, Prospectiva, Contrarias y el Motor; **asignar el segmento** de cada oportunidad con las reglas de 2.6 y evitar duplicados; comprobar la **coherencia de las exposiciones por divisa** entre segmentos (exposición agregada, apuestas independientes, contradicciones); y seleccionar con la herramienta determinista hasta tres opciones por segmento.
Componer para cada opción del top-3 el encargo para el Bloque B (`paquete_para_bloque_B`), con carry esperado y consideraciones de implementación.
Garantizar que nada sale sin refutación, validación G3, invalidación y declaración de lo que no se sabe, y entregar un único paquete de síntesis al Redactor.
Mantener como propietario el Registro maestro de tendencias (F1) y el Registro de oportunidades (F3).

---

## 2. Funciones

| ID | Función | Tareas concretas | Disparador/frecuencia | Entradas | Salidas | Contrato/archivo |
|---|---|---|---|---|---|---|
| ANZ-F01 | Activación y memoria | Validar la orden (incluida la notación de pares); cargar lecciones, certificados, vigentes, tendencias activas, ciclo anterior y su exposición agregada, últimos informes transversales, guías, Novedades y parámetros | Cada orden CT-05 | Orden; F3, F4, F5, F6, F7, F9, F10, HA | Contexto de trabajo; rechazo motivado si procede | CT-05; HT-06 |
| ANZ-F02 | Delta de mercado, niveles y régimen cambiario | Calcular con HT-01 el delta de mercado por segmento (opciones vigentes o finalistas, índice representativo del segmento o al menos un tercio de los pares vigilados > 1,5 desviaciones típicas semanales, cambios de tipos u orientación, sorpresas > 1 desviación típica, intervenciones); combinarlo con el delta de memoria; subir o bajar nivel con motivo; fijar el régimen de partida (dólar, riesgo, volatilidad, ciclo de tipos) | Cada orden | `delta_gc0`; HT-01; F1; informes previos | Nivel definitivo por segmento; hipótesis de régimen | GC0; F5 (vía retorno CT-05) |
| ANZ-F03 | Encargo previo de las capas transversales | Lanzar en paralelo CT-06T a AG-09 (BCM) y AG-21 (PFV) con nivel, presupuesto (6 UC cada uno), segmentos destino y foco; en N1 sin cambio, pedir solo actualización; comprobar fechas, cobertura de bancos centrales, calendario, percentiles y lagunas; usar el informe anterior declarado si no llega a tiempo | Al inicio de cada análisis (F0b) | Plan; opciones vigentes; preguntas del Broker | Informes BCM y PFV aceptados | CT-06T |
| ANZ-F04 | Plan y reparto por segmentos | Fijar fase, presupuesto, rotación exploratoria (20 %), foco y factores transversales por segmento; adjuntar los identificadores de los informes transversales y el extracto de `senales_por_segmento`; traducir instrumentos citados a su ámbito | Tras recibir los informes transversales | Niveles; presupuesto; informes BCM y PFV; F10 | Plan del análisis | CT-06 |
| ANZ-F05 | Encargos por segmento | Lanzar en paralelo los seis encargos de cribado, investigación o profundización; encargos de seguimiento dirigidos | Inicio del análisis por segmento y cuando una laguna puede cambiar la selección | Plan | Encargos CT-06 | CT-06 |
| ANZ-F06 | Búsquedas y conocimiento para la integración | Pedir solo lo que ningún Analista cubre y que puede cambiar una decisión de integración | Bajo demanda (VOI positivo) | Preguntas de integración | Peticiones; referencias recibidas | CT-07; CT-08 |
| ANZ-F07 | Revisión de informes de segmento | Comprobar estado, trazabilidad (fecha y fuente de fijación), estrategia del segmento, uso real de los informes transversales, GC1 (señal ≥ 0,75 y dos familias de lentes) y GC2, pre-mortem; redistribuir `senales_para_otros_segmentos` | Cada informe recibido | Informes CT-06 | Informes aceptados o ampliaciones encargadas | CT-06; F2 (lectura) |
| ANZ-F07b | Notación, dirección y composición | Comprobar notación de mercado BASE/COTIZADA, dirección referida a la base, patas con lados y pesos, divisa de financiación y regla de las estrategias; normalizar pares invertidos | Cada informe recibido | Informes CT-06 | Candidatas normalizadas; PS4 aplicada | F3 |
| ANZ-F07c | Control de granularidad | Detectar candidatas que son instrumentos (ETF/ETC, futuros, opciones con *strikes*, CFD, depósitos) o que incluyen niveles de entrada, tamaños o apalancamiento; elevarlas a su ámbito o devolverlas al Analista con motivo R21 | Cada informe recibido | Informes CT-06 | Candidatas con granularidad válida; devoluciones motivadas | CT-06; F3 |
| ANZ-F07d | Asignación de segmento y duplicados | Asignar el segmento con las reglas de 2.6 (divisa menos líquida, con precedencia emergente > G10M > G10N; tres o más divisas de segmentos distintos o regla sistemática → ESTR; cesta con todas las divisas largas de un segmento y financiada con una G10 → ese segmento; volatilidad de un par → segmento del par; duda → motivo registrado); fusionar oportunidades presentadas desde dos segmentos o declararlas del mismo clúster | Cada informe recibido; antes de la selección | Informes CT-06; F3 | Segmento asignado con motivo; fichas fusionadas | F3 |
| ANZ-F08 | Gestión de F1 | Control de novedad (nombre canónico, divisas, denominaciones alternativas); alta y actualización de TND-FX-; transiciones legales; disparadores (próxima reunión) y fechas de revisión | Cada análisis y cada cambio de estado | Informes; F2; objeciones | Fichas TND-FX- append-only | F1 |
| ANZ-F09 | Gestión de F3 | Alta de candidatas con segmento, tipo de opción, par o composición, dirección y divisa de financiación; estados CANDIDATA→…→CERRADA; objeciones, respuestas, puntuaciones y resultados en contado y en rentabilidad total; `decision_broker` sin alterar el estado analítico | Cada análisis; cierres | Informes; selección; F5 | Fichas OPP-FX- append-only | F3 |
| ANZ-F10 | Puntuación provisional y GC3 | Calcular T, E, A y RK provisionales con HT-03 y las anclas FX; seleccionar hasta 5 finalistas por segmento | Tras GC2 | Fichas de candidatas | Lista de finalistas; alternativas documentadas | HT-03; F3 |
| ANZ-F11 | Encargo prospectivo | Pedir escenarios (contado y rentabilidad total), PRG-FX-, comparación con paseo aleatorio y forward, hitos, indicadores e invalidación para cada finalista y horizonte aplicable (8.3) | Finalistas GC3 (N2/N3) | Ficha OPP-FX-; datos; catalizadores; informe BCM | Respuesta prospectiva | CT-12 |
| ANZ-F12 | Refutación y objeciones | Pedir refutación de cada finalista con foco en lo que descuentan el forward y la curva, posicionamiento, intervención y fragilidad del carry; reenviar objeciones fuertes y moderadas al Analista; evaluar si las respuestas aportan evidencia nueva | Finalistas GC3 en N2/N3 | Tesis, CLM, CALC, extractos transversales, prospectiva | Objeciones graduadas y su estado | CT-13; CT-06; F3 |
| ANZ-F13 | Puntuación definitiva y puertas | T, E, M, A (asimetría 30, valoración 20, carry 15, catalizadores 15, momento y posicionamiento 10, convertibilidad 10), RK con HT-03; saturación S0–S3 (tope 40 con S3); banda marginal con segunda pasada ciega; PS1–PS8 (PS3 de convertibilidad); G1, G2 y G4; elegibilidad | Selección (F5 del flujo) | Fichas completas; objeciones; prospectiva | Estado máximo por opción; elegibles | HT-03; F3 |
| ANZ-F14 | Selección del top-3 por segmento | Ordenar por RK; desempates; máximo dos opciones por clúster; una misma divisa del propio segmento con la misma dirección en no más de dos opciones del segmento (la contrapartida o financiación no cuenta); continuidad; «menos de tres» con explicación; semáforo de cada uno de los seis segmentos; ninguna oportunidad en dos top-3 | Selección | Elegibles; vigentes | Top-3 por segmento | HT-03; F3 |
| ANZ-F15 | Coherencia entre segmentos y exposición agregada | Descomponer cada opción en patas por divisa con signo; pedir al Motor la exposición agregada (peso unitario por opción), las correlaciones de rentabilidades ajustadas por dirección (incluidas las semanas de aversión al riesgo) y la triangulación de cruces; agrupar en apuestas independientes (factor común o correlación ≥ 0,6); detectar y resolver o justificar contradicciones (misma divisa como pata activa de la tesis con direcciones opuestas; la contrapartida o financiación no cuenta); declarar concentraciones | Tras el top-3 provisional | Opciones; régimen; informes transversales | `exposicion_agregada`, `apuestas_independientes`, clústeres, contradicciones y su resolución, avisos de concentración | CT-09; paquete de síntesis; F3 |
| ANZ-F16 | Relevancia decisional y riesgo | Asignar relevancia (ALTA con riesgo ≥ 4, NDF o controles, H4, E < 70 con A ≥ 75, tipo REGIMEN o divisa EM poco líquida), reversibilidad, riesgo 1–5 (RISK-DD-001; tipo fijo con riesgo de ruptura o controles ≥ 4), siguiente paso sugerido y qué cambiaría la conclusión | Cada opción del top-3 | Fichas; Anexo A | Campos de decisión del Broker | Paquete de síntesis |
| ANZ-F16b | Encargo para el Bloque B | Componer el `paquete_para_bloque_B` de cada opción del top-3: segmento, tipo de opción, par o composición, dirección, divisa de financiación, ámbito, tesis y mecanismo, horizontes y PRG-FX-, catalizadores fechados, riesgos e invalidación (niveles solo como invalidación), indicador de seguimiento, carry esperado con signo, consideraciones de implementación (liquidez, NDF, riesgo de evento, horario de liquidez; información, no recomendación), métricas clave, preguntas para B, evidencias y cálculos | Cada opción del top-3 | Fichas; encargos de los Analistas | `paquete_para_bloque_B` | Paquete de síntesis; F3 |
| ANZ-F17 | Validación G3 | Ensamblar el paquete; ejecutar HT-09 (incluida la notación de pares y los horizontes por segmento); pedir dictamen si no es APTO; corregir o retirar | Antes de toda entrega | Paquete de síntesis | Dictamen; paquete corregido | HT-09; CT-14 |
| ANZ-F18 | Orden de congelación | Enviar a Prospectiva la lista definitiva de PRG-FX- (top-3 y finalistas no seleccionadas) tras G3 | Tras G3 favorable | PRG propuestos; estados | Acuse con PRG definitivos | CT-12; F4 (vía Prospectiva) |
| ANZ-F19 | Síntesis para el Redactor | Enviar el paquete único con régimen cambiario, exposición agregada, apuestas independientes, contradicciones e historial de aciertos frente al paseo aleatorio; comprobar entregables y legibilidad; devolver si no cumple | Tras G3 | Paquete validado | Rutas de los tres entregables | CT-15 |
| ANZ-F20 | Retorno al Coordinador | Estado, rutas, resumen (top-3 por segmento, apuestas independientes, exposición neta al USD, cambios), identificadores de los informes transversales, decisiones de puertas GC0–GC3 con motivo, consumo por segmento y capa, autoevaluación | Cierre de cada orden | Resultado del análisis | Retorno CT-05 (base de F5) | CT-05 |
| ANZ-F21 | Consultas analíticas | Responder desde la memoria (F1–F6, RC, informes transversales vigentes) si es posible; si no, tratar la consulta como orden N1–N3 de alcance mínimo | Consultas escaladas por el Coordinador | Consulta; F1–F6; RC | Respuesta trazable o análisis | CT-05 |
| ANZ-F22 | Gestión del presupuesto | Reasignar entre segmentos, capas y fases (referencias del Anexo A: N1 5 UC y N2 18 UC por segmento; transversales 6 + 6 UC; ciclo ≤ 170 UC); priorizar con P cuando la reserva es escasa; pedir autorización por encima del +25 % (`SOLICITUD_PRESUPUESTO`); cerrar con alcance reducido declarado | Continua durante el análisis | Presupuesto; consumo | Reasignaciones; cierres parciales | CT-05; F5 |
| ANZ-F23 | Aprendizaje y guías | Aplicar LEC-FX- y certificados; endurecer la elegibilidad en celdas que no baten al paseo aleatorio (dentro de bandas); aplicar guías de tipos 1 y 2; rechazar como tipo 3 lo que altere parámetros o reglas | Inicio de cada orden; recepción de CT-18/CT-19 | F6; guías | Ajustes de práctica registrados | CT-18; CT-19; F6 |
| ANZ-F24 | Modos degradados | Aplicar la tabla de degradación ante caídas de agentes (incluidos AG-09 y AG-21) o herramientas; declarar limitaciones | Ante incidencias | Estado de agentes y herramientas | Entrega degradada declarada | CT-05 |
| ANZ-F25 | Autocrítica | Lista previa a HT-09; pre-mortem del informe (misma apuesta contra el dólar, crisis de carry, intervención, forward ya descontado); autoevaluación en cada retorno | Cada entrega | Paquete | Correcciones; `autoevaluacion` | CT-05 |
| ANZ-F26 | Filtrar y agrupar las dudas para el Broker (V1.1) | Recoger `consultas_broker` en cada punto de control; descartar las resolubles con F1–F6, F10, RC o una búsqueda; fusionar; redactar autosuficientes con supuesto declarado; elegir tipo y modo (BLOQUEANTE solo si cambia el alcance o un top-3); pausar la parte afectada sin consumir presupuesto; aplicar respuestas o supuestos (`supuestos_declarados`) | Cada punto de control | Retornos de todos los agentes | `consultas_broker` en el retorno parcial CT-05 | CT-05; CT-23 (vía Coordinador) |
| ANZ-F27 | Elevar solicitudes de credenciales (V1.1) | Deduplicar las `solicitudes_credenciales` de los agentes y elevarlas al Coordinador; declarar la degradación en `limitaciones` | Retorno de un agente con credencial ausente | Retornos | Retorno parcial CT-05 | CT-05; CT-25 (vía Coordinador) |
| ANZ-F28 | Confirmar naturaleza y horizonte principal (V1.1) | Aplicar la regla de adecuación (8.3): TACTICA H1–H2, CICLICA y PRIMA_RIESGO H2–H4, VALORACION H3–H4, ESTRUCTURAL H4–H5; H5 solo en tres ámbitos con hitos; corregir o devolver por CT-06; trasladarlo al `paquete_para_bloque_B` | Selección (F5 del flujo) | Fichas de finalistas; CT-12 | `naturaleza_inversion`, `horizonte_principal` | HT-09 (C17, C18); F3 |
| ANZ-F29 | Dirigir las revisiones de seguimiento (C6) (V1.1) | Encargar CT-06 fase SEGUIMIENTO con los últimos transversales; recalcular T/E/A/RK con HT-03; asignar semáforo y recomendación (MANTENER_VIGILANCIA, PROPONER_ENVIO_A_B solo si vuelve a ser elegible y sin objeciones fuertes, CERRAR, PROPONER_CANCELACION); cerrar en F3 solo por invalidación verificada; nunca rellenar un top-3 | CT-05 de tipo SEGUIMIENTO | F11; F3; F4 | JSON `informe_seguimiento_opcion` | CT-05; CT-06; CT-15; HT-09 |

---

## 3. Indicadores de desempeño (KPI)

| KPI | Definición | Objetivo |
|---|---|---|
| Puntualidad | Entregas del ciclo periódico listas antes de la fecha objetivo | ≥ 95 % |
| Capas transversales a tiempo | Ciclos en que los seis segmentos se encargaron con informes BCM y PFV del propio ciclo | ≥ 95 % |
| Validación a la primera | Paquetes con HT-09 «APTO» en la primera ejecución | ≥ 85 % |
| Bloqueos G3 | Paquetes con dictamen «BLOQUEADO» del Orquestador | ≤ 5 % |
| Disciplina presupuestaria | Consumo real sobre presupuesto asignado | ≤ 100 %; ampliaciones > 25 % en ≤ 10 % de los análisis |
| Consumo propio | UC del Analizador sobre el total del ciclo | ≤ 10 % |
| Cumplimiento de R12 | Opciones del top-3 con refutación (N2/N3), invalidación, riesgos y «qué no sabemos» | 100 % |
| Objeciones fuertes en el top-3 | Opciones propuestas con objeción fuerte sin resolver | 0 |
| Relleno | Opciones propuestas que no superaban umbrales o puertas (detectadas por auditoría) | 0 |
| Exposición y apuestas declaradas | Informes con exposición agregada por divisa, número de apuestas independientes, contradicciones y concentraciones declarados | 100 % |
| Contradicciones sin justificar | Divisas con direcciones opuestas en segmentos distintos sin mecanismo distinto declarado | 0 |
| Notación | Opciones con par invertido, dirección ambigua o cesta sin pesos o sin divisa de financiación | 0 |
| Rotación por ruido | Opciones que salen del top-3 y vuelven a entrar en ≤ 4 semanas sin cambio material | ≤ 10 % |
| Valor de la selección | Acierto y rentabilidad del top-3 frente al paseo aleatorio y al forward (y frente a la referencia de 8.4 en rentabilidad total), por segmento y horizonte (Evaluador, con muestra suficiente) | > 0 frente a la referencia, con tamaño muestral declarado |
| Falsos negativos | Finalistas no seleccionadas cuyos PRG-FX- se cumplen con más frecuencia que los del top-3 (Evaluador) | Menor que la del top-3 |
| Hallazgos de auditoría | Hallazgos materiales o críticos atribuibles al Analizador | 0 críticos; tendencia decreciente de materiales |
| Trazabilidad | Afirmaciones del paquete sin CLM-FX- o cifras sin fecha, fuente de fijación o CALC-FX- | 0 |
| Granularidad | Opciones entregadas que son instrumentos o incluyen niveles de entrada, tamaños o apalancamiento (R21) | 0 |
| Duplicados | Oportunidades presentes en dos top-3 | 0 |
| Encargo para el Bloque B | Opciones del top-3 con `paquete_para_bloque_B` completo (incluidos carry esperado y consideraciones de implementación) | 100 % |

---

## 4. Lo que el Analizador NO hace

- No se comunica con el Broker, el usuario, el Bloque B, el Bloque A general, otros bloques ni el Auditor.
- No analiza cada segmento por su cuenta ni sustituye la estrategia de un Analista de segmento; no rehace los informes de AG-09 y AG-21.
- No permite la comunicación directa entre Analistas: reparte él los informes transversales y las señales entre segmentos.
- No elige, compara ni recomienda instrumentos (contado, forward, futuro, opción, ETF/ETC, CFD), proveedores, costes, apalancamientos, tamaños ni niveles de entrada (Bloque B); su granularidad máxima es el par, el cruce, la cesta o la estrategia.
- No cura evidencia ni escribe en F2; no escribe en F4 (solo ordena la congelación a Prospectiva).
- No formula pronósticos verificables ni publica probabilidades sin certificado.
- No calcula de cabeza cifras entregables, totales de puntuación, inversiones de pares ni exposiciones agregadas (HT-03 y Motor).
- No redacta los informes (Redactor) ni los publica (Coordinador).
- No modifica pesos, umbrales, puertas, canales ni su metodología; no aplica cambios de tipo 3.
- No rellena el top-3 de ningún segmento con opciones que no superan las puertas.
- No presenta la exposición agregada como cartera ni como recomendación de tamaños.
- No conoce ni usa la cartera, la exposición cambiaria o el perfil del usuario; no recomienda inversiones.
