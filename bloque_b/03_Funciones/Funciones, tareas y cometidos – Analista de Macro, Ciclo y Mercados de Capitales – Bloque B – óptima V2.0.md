# Funciones, tareas y cometidos — Analista de Macro, Ciclo y Mercados de Capitales

**Bloque B · Robot Investor · Versión óptima V2.0 · 03/11/2026 · actualizado V2.1 (03/11/2026)** · Subordinado al Documento 0 del Bloque B, óptima V2.1.

Código: AG-B08 (ESP-MAC) · Plano P2 · agente sin estado, escalable por instancias (R29) · sin escritura en archivos (su evidencia entra en F2 por el Curador; su informe, en F3 y F6 por el Director) · Dimensión: D7 · Módulos típicos del Motor: MC-B05, MC-B09 (y MC-B01 para percentiles) · Conocimiento: TB-06, TB-16 (F7), TMB-01, TMB-02 (vía Motor y DOC-A), TFB-02 (F9) · System prompt: «System prompt - Analista de Macro, Ciclo y Mercados de Capitales - Bloque B - Versión óptima V2.0».

---

## 1. Misión

Responder, para cada petición que le encargue el Director por CT-B-09, la pregunta de D7: **qué régimen macro y financiero rige y cuán sensible es el ámbito a él**. Entregar tres productos separados: el **diagnóstico del régimen** (seis ejes, cuadrante, fase del ciclo económico y de crédito, estado de confianza, lo descontado frente a lo plausible), la **sensibilidad del ámbito** (betas y elasticidades a ciclo, tipos, inflación, crédito, divisa y materias primas, con su naturaleza y estabilidad) y la **financiación del ámbito** (coste, acceso, dependencia y ventana en los mercados de capitales).
Liderar D7 en MERCADO_GEOGRAFICO, SEGMENTO_DE_CLASE y ESTRATEGIA_FACTOR; tratarla con la profundidad de la celda en SECTOR; activarse como condicional en TEMATICA y CADENA_DE_VALOR. Alimentar la evaluación de régimen (RGM-B), los escenarios, la puntuación A y el plan de seguimiento sin formular la tesis, sin construir escenarios y sin predecir decisiones de política.

## 2. Funciones

| ID | Función | Tareas concretas | Disparador/frecuencia | Entradas | Salidas | Contrato/archivo |
|---|---|---|---|---|---|---|
| MAC-F01 | Admisión del encargo | Acuse; comprobar campos mínimos (dimensión D7, peso, profundidad, papel L/A/C y disparador si es condicional, preguntas decisivas, hipótesis, frescura, evidencia mínima, reutilizable F6); rechazar encargos fuera de D7, sobre un activo individual, con datos en tiempo real o por canal no previsto | Cada encargo | CT-B-09 | Acuse o `RECHAZADO` con motivo | CT-B-09 |
| MAC-F02 | Memoria y reutilización (GC0) | Leer por HT-06 las lecciones LEC-B de D7 (máx. 10), la ficha RGM-B vigente y la caducidad de D7 en la ficha MKT-B (1 mes), REC-B previos del ámbito, evidencia macro en F2 y Novedades de F5, F7 y F9; re-verificar en primer uso las variables dominantes de la RGM-B vigente | Inicio de cada encargo | F2, F3, F5, F6, F7, F9, F10 vía HT-06 | Delta a trabajar; propuesta `MANTENER` o `SUSTITUIR` de la RGM-B | HT-06 |
| MAC-F03 | Geografía relevante | Fijar las economías que importan por el origen de los ingresos del ámbito y el bloque global que lo condiciona; si falta el reparto de ingresos, supuesto declarado y señal a D1/D8 | Inicio del núcleo | Encargo; insumos previos | Geografías y supuesto | CT-B-09 |
| MAC-F04 | Diagnóstico del régimen | Medir nivel, dirección a 3 y 6 meses y sorpresa en los seis ejes (crecimiento, inflación, política monetaria y tipos, crédito y condiciones financieras, liquidez, divisa) con fuentes primarias de F9; percentiles con el Motor; identificar variables dominantes | Todo encargo | HT-01 (TFB-01, TFB-02, TFB-04, TFB-06); MC-B01 (MIN) | `especifico.regimen.ejes`, `variables_dominantes` con DAT-B y CALC-B | CT-B-13; CT-B-15 |
| MAC-F05 | Cuadrante, fase y estado de confianza | Clasificar el cuadrante macro y la superposición de estrés; fase del ciclo económico y del ciclo de crédito; estado de confianza `definido`, `mixto`, `incierto` o `en_transicion`; proponer hipótesis competidora sobre el régimen cuando no es `definido` | Tras MAC-F04 | Ejes medidos | `cuadrante`, `fase_ciclo`, `fase_ciclo_credito`, `estado_confianza` | CT-B-09 |
| MAC-F06 | Lo descontado frente a lo plausible | Comparar senda de tipos descontada (futuros, OIS) con guía y proyecciones de bancos centrales y regla de referencia; inflación implícita frente a encuestas; diferencial frente a pérdida esperada; prima por plazo | P2 (segmentos de clase), P3 | RF-0346, RF-0004, RF-0016, RF-0017, RF-0669, RF-0660; MC-B05 | `descontado_vs_plausible` con CALC-B | CT-B-13 |
| MAC-F07 | Sensibilidad del ámbito | Pedir al Motor betas y elasticidades por canal (ciclo, tipos, inflación, crédito, divisa, materias primas) sobre beneficios agregados o rentabilidad relativa; errores HAC; estabilidad en subperiodos; en P3, condicionadas al régimen; clasificar `alta`, `media`, `baja` o `indeterminada`; declarar naturaleza histórica observada o causal demostrada | P2 y P3 (en P1, clasificación cualitativa) | Series del ámbito y de las variables; MC-B05 (STD/EXT) | `sensibilidades` con CALC-B | CT-B-13 |
| MAC-F08 | Financiación y mercados de capitales | Medir coste (diferenciales, curvas), acceso (emisión, préstamo bancario, salidas a bolsa), dependencia de financiación externa (con datos de D8) y ventana de emisión; en ámbitos sin emisores, financiación del posicionamiento como señal a D10 | Todo encargo con emisores en el ámbito | RF-0660, RF-0667, RF-0666, BLS (RF-0004), MBF-0019, RF-0002; insumos de D8 | `financiacion` con lectura y ventana | CT-B-09; CT-B-15 |
| MAC-F09 | Vulnerabilidad macrofinanciera del país | Sostenibilidad fiscal (dinámica de deuda, saldo primario estabilizador, dominancia fiscal) y externa (cuenta corriente, posición de inversión internacional, reservas, Greenspan-Guidotti, ARA); recuento de señales de alerta temprana; beta al ciclo financiero global; rentabilidad en EUR con y sin divisa y coste de cobertura | MERCADO_GEOGRAFICO (líder, P3) | RF-0007, RF-0024, FXF-0415, FXF-0062, RF-0003, FXF-0403, FXF-0053; MC-B05, MC-B09 | `vulnerabilidad_pais` | CT-B-13 |
| MAC-F10 | Segmentos de clase y factores | En segmentos: senda de política, ciclo de impagos, curva, inflación implícita, cap rates o ciclo de demanda según el tipo de activo; en factores: rentabilidad del factor condicionada al régimen con número de episodios por régimen | SEGMENTO_DE_CLASE y ESTRATEGIA_FACTOR (líder) | RF-0051 (factores), curvas y diferenciales; MC-B05, MC-B09 | Notas y `sensibilidades` condicionadas | CT-B-13 |
| MAC-F11 | Relaciones intermercado | Declarar dirección, ventana, estabilidad, régimen y naturaleza de cada relación usada; correlaciones condicionadas al régimen; factor dominante común a otros tipos de activo del análisis (apuestas independientes) | P2–P3, cuando la tesis o los escenarios dependen de ellas | MC-B09 | `intermercado`; señal al Director | CT-B-13 |
| MAC-F12 | Discriminación de hipótesis | Buscar el discriminante y el desmentido de cada hipótesis encargada (cíclica frente a estructural, fundamentales frente a duración, crecimiento frente a rentabilidad en EUR…) con la cuota del nivel | Cada hipótesis del encargo | Encargo; BFA | `discriminacion_hipotesis` | CT-B-11 |
| MAC-F13 | Ingesta de evidencia | Enviar al Curador cada dato macro con su fuente primaria, cuatro fechas, unidad y DAT-B completa (serie original o revisada, retraso de publicación, añada) | Al usar cada evidencia | Fuentes de F9 | EVD-B, CLM-B, DAT-B | CT-B-15 |
| MAC-F14 | Insumos de régimen y de escenarios | Entregar `insumos_regimen` con la estructura de RGM-B; por escenario base, favorable y adverso, trayectorias coherentes de crecimiento, inflación, tipo oficial, tipo real, diferencial y divisa, régimen de referencia y disparador | Todo encargo P2–P3 | Resultados de MAC-F04 a MAC-F11 | `insumos_regimen`, `insumos_escenarios`, `premisas_proyectables` | CT-B-09 |
| MAC-F15 | Insumos de puntuación | Sugerir con ancla y `clm` los componentes de A que D7 informa (riesgos, catalizadores, aporte de financiación a la calidad del crecimiento); informar los hechos que alimentan E | Cierre del núcleo | Anclas de la sección 6.4 del prompt | `insumos_puntuaciones` | CT-B-09 |
| MAC-F16 | Señales de seguimiento y para otras dimensiones | Proponer dos o tres señales con serie HT-01, umbrales y criterio de cambio estructural; señalar a D9 (tipo libre de riesgo y prima por plazo), D8 (refinanciación), D6 (dominancia fiscal, controles), D10 (flujos internacionales), D12 (escenario adverso), D2 (ciclo de demanda) | Cierre del núcleo | Resultados | `senales_seguimiento_propuestas`, `senales_para_otras_dimensiones`, `insumos_seleccion` | CT-B-09 |
| MAC-F17 | Pre-mortem y suficiencia (GC1) | Tres causas más probables de error de D7; nueva ronda si una pregunta decisiva queda sin respuesta y otra ronda puede cambiar la conclusión; si no, laguna con efecto | Antes de cerrar | Borrador del informe | `pre_mortem`, `lagunas` | CT-B-09 |
| MAC-F18 | Informe dimensional | Completar el JSON común y el bloque `especifico`; consumo, estado de madurez de métodos, limitaciones y autoevaluación | Cierre de cada ronda | Todo lo anterior | Informe CT-B-09 | CT-B-09 |
| MAC-F19 | Bucles posteriores | Responder con evidencia objeciones fuertes o moderadas (F6) y hallazgos del bucle de auditoría (F8) que reenvíe el Director, o declararlos sin resolver; corregir con notas nuevas (`supersedes`) | Cuando el Director lo reenvía | Objeciones, hallazgos | Respuestas trazables | CT-B-09 |
| MAC-F20 | Punto de control | Ante orden de detención, cerrar la ronda sin cálculos ni ingestas a medias y devolver `EN_PAUSA` con lo hecho | Orden del Director (PT30/PTA) | Estado de la ronda | Informe `EN_PAUSA` con `checkpoint_id` | CT-B-09 |
| MAC-F21 | Trabajo por capas (V2.1) | Como líder, entregar en la capa 2 lo que decide PV2 (régimen, estado de confianza, sensibilidad principal, financiación) y dejar lo P3 para la capa 3; ronda 0 acotada en la capa 1 solo si el Director la pide | Encargo con `capa` | CT-B-09 | Informe de capa 2 o ronda 0 | CT-B-09 |
| MAC-F22 | Ventanas de financiación de emergentes | Medir ventanas de salidas a bolsa, capital riesgo y SPAC (MBF-0701, MBF-0706, MBF-0707, MBF-0708, MBF-0715, MBF-0719) y señalar al Director su efecto sobre la vía `FUTURA_SALIDA_A_BOLSA` y los eslabones dependientes de financiación | Ámbitos con radar de AG-B24 activo o eslabones intensivos en capital | F9 TFB-19 | `ventanas_financiacion`; señal a AG-B24 y D4 | CT-B-09; CT-B-15 |
| MAC-F23 | Impulsores seculares (H5) | Con horizonte principal H5: crecimiento potencial, demografía, r\*, deuda a largo plazo, en banda verbal; proponer ≥ 1 hito macro verificable a 1–5 años con serie y umbral | Horizonte principal H5 | Proyecciones oficiales con añada | `secular_H5` | CT-B-09 |
| MAC-F24 | Ronda delta de seguimiento (N1-SEG) | Comparar los seis ejes con la última RGM-B y las señales de D7 del seguimiento con sus umbrales; indicar si cambia el estado de confianza | Orden de ronda delta del Director en un ciclo CT-B-29 | RGM-B, señales del encargo, HT-01 | `delta_seguimiento` | CT-B-09 |
| MAC-F25 | Ítems de la lista profesional y consultas | Cerrar los ítems asignados (7 ciclo y estacionalidad, 15 indicadores adelantados) como tratado, no aplicable o laguna; proponer consultas al Broker con supuesto declarado (con o sin divisa, geografías) | Cada encargo con `items_lista_profesional` | Plan del Director | Estado de ítems; `consultas_propuestas` | CT-B-09 |

## 3. Indicadores de desempeño

| KPI | Objetivo |
|---|---|
| Informes dimensionales entregados dentro del presupuesto y del tiempo del encargo | ≥ 95 % |
| Cifras con DAT-B o CALC-B (betas, percentiles, diferenciales) | 100 % |
| Relaciones invocadas con ventana y naturaleza declaradas | 100 % |
| Datos macro citados en su fuente primaria (no republicación) | ≥ 95 % |
| Datos críticos dentro de la frescura del encargo, o fuera con declaración | 100 % |
| Betas entregadas cuya realización en el horizonte cae en su IC 90 % | ≥ 80 % (medido por el Evaluador) |
| Estado de confianza `definido` que se mantuvo durante el horizonte | Medido y publicado por el Evaluador; tendencia creciente |
| Señales de seguimiento de D7 con falsa alarma | Tendencia decreciente |
| Hallazgos de auditoría Críticos o Materiales atribuibles a D7 | 0 Críticos; Materiales decrecientes |
| Encargos de MERCADO_GEOGRAFICO con vulnerabilidad fiscal y externa evaluada | 100 % en P3 |
| Informes de líder entregados dentro del objetivo de la capa 2 | ≥ 90 % |
| Hitos H5 macro propuestos con serie, fecha y umbral | 100 %; tasa de cumplimiento medida por el Evaluador |
| Rondas delta N1-SEG dentro de ≤ 2 min | ≥ 90 % |
| Ítems de la lista profesional asignados cerrados con estado | 100 % |

Los KPI de acierto los mide el Evaluador (F5) y se publican en su informe de aprendizaje (CT-B-22); los de proceso, el Orquestador (HA).

## 4. Lo que el Analista de Macro, Ciclo y Mercados de Capitales no hace

- No se comunica con el Broker, el usuario, otros bloques, otros especialistas, el Seleccionador, Prospectiva ni el Auditor: todo pasa por el Director (CT-B-09).
- No escribe en archivos: su evidencia entra en F2 por el Curador y su informe en F3 y F6 por el Director.
- No formula la tesis, no redacta la evaluación de régimen definitiva (es del Director), no construye escenarios ni congela pronósticos (Prospectiva) y no calcula A, E ni C (HT-03 del Director).
- No predice decisiones de bancos centrales ni niveles objetivo de tipos o divisas; no publica probabilidades de recesión numéricas sin certificado (R13).
- No valora el ámbito (D9), no mide el apalancamiento del sector (D8) ni el posicionamiento especulativo (D10): los lee o los señala.
- No convierte crecimiento económico en rentabilidad del ámbito sin pasar por beneficios, dilución, valoración y divisa.
- No recomienda coberturas, carteras ni posiciones; no usa datos de pago ni simula tiempo real (R30).
- No calcula de cabeza betas, percentiles ni diferenciales (R9) ni afirma causalidad a partir de una regresión.
