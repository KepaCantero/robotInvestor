# Funciones, tareas y cometidos — Evaluador de Previsiones y Aprendizaje (Bloque A Forex)

**Bloque A Forex · Robot Investor · Versión óptima V1.0 · 02/11/2026 · actualizado V1.1 (03/11/2026)** · Subordinado al Documento 0 del Bloque A Forex V1.1. Las funciones añadidas en V1.1 llevan la marca «(V1.1)».

---

## 1. Misión

Ser el motor de la automejora del Bloque A Forex: resolver cada pronóstico congelado en su fecha, con la fijación de su criterio y sin fuga de información, incluido el carry realizado en los pronósticos de rentabilidad total; medir acierto, calibración y valor **frente al paseo aleatorio** (Meese y Rogoff, 1983) y, cuando procede, **frente al forward como predictor**, por celdas segmento × horizonte × método; evaluar los ámbitos propuestos con su indicador de seguimiento frente a la referencia de su segmento (8.4); y certificar qué horizontes pueden expresarse con probabilidad (R13).
Convertir esa medición en aprendizaje verificable: lecciones LEC-FX- en la Memoria de aprendizaje (F6), recalibraciones dentro de bandas con evaluación sombra (FX-1.0 → FX-1.1…) y propuestas de tipo 3 cuando proceda.
Publicar cada semana un historial de aciertos honesto frente al paseo aleatorio, y medir la fiabilidad de las fuentes de opinión cambiarias, el riesgo de cola del carry y el valor del producto para el Broker.

## 2. Funciones

| ID | Función | Tareas concretas | Disparador/frecuencia | Entradas | Salidas | Contrato/archivo |
|---|---|---|---|---|---|---|
| EVAL-F01 | Resolución diaria de pronósticos | Esperar la publicación de la fijación del criterio (WM/Reuters 16:00 Londres, BCE, H.10, fijación del NDF); aplicar el calendario de festivos de liquidación; calcular el carry realizado con los puntos forward de la fecha de partida en rentabilidad total; cruces sintéticos y cestas con la composición congelada; aplicar fallback; resultado por tipo; NO_RESOLUBLE con motivo (incluidas rupturas y redenominaciones sin serie) | Diario (recordatorios HT-05) | F4, HT-01 | Campos de resolución en F4; lote RES- en F6 | F4; HT-01; HT-05 |
| EVAL-F02 | Control de fuga y de anticipación en fijaciones | Verificar referencias ingenuas fijadas en la congelación, `nivel_referencia` conocible antes de la congelación (G3-FX-07), puntos forward y volatilidad de la fecha de partida, COT desde su publicación, vintages, composiciones point-in-time y universo completo; marcar `comprobacion_fuga`; recalcular y revertir si se detecta fuga a posteriori | Cada resolución y cada análisis | F2 (`conocible_desde`), F4, HT-01 | Resultado del control | F4; F6 |
| EVAL-F03 | Puntuación de pronósticos | Pedir al Motor (MC-10) Brier, log-score, pinball/CRPS y las puntuaciones de todas las referencias registradas (paseo aleatorio siempre; forward; rentabilidad nula o índice de estrategia; probabilidad implícita en REGIMEN) en lote | Diario | Resueltos del día | CALC-FX- con puntuaciones | CT-09; RC |
| EVAL-F04 | Métricas por celda | Calcular por niveles (segmento × horizonte; + método; + estrategia, tipo de opción, tipo de rentabilidad, divisa y fuente): n y n efectivo (solapamiento y conglomerados de fecha y de factor dólar), acierto con Wilson y Pesaran-Timmermann, Brier, Murphy, BSS frente a cada referencia con IC bootstrap por bloques o conglomerados, U de Theil y Clark-West en niveles, ECE, calibración global y pendiente, DM-HLN, rentabilidad total relativa con su descomposición en contado y carry, Sortino y asimetría, riesgo de cola frente al escenario adverso, falsos positivos/negativos, IC de Spearman del RK | Mensual (incremental semanal) | F4, F3, F5, RC | Métricas MET- en F6 | CT-09; F6 |
| EVAL-F05 | Certificados de horizonte | Emitir con n ≥ 100, extremo inferior del IC 90 % del BSS frente al paseo aleatorio (RI-PA del Catálogo) > 0 (Holm en la familia), BSS puntual ≥ 0 frente al forward en rentabilidad total, calibración no rechazada (ECE ≤ q90 simulado y < 0,15) y re-ejecución CT-10; revisar mensualmente; poner en observación o revocar (BSS ≤ 0 en ventana, ECE ≥ 0,17 o calibración rechazada dos meses, fuga, cambio de método o de versión mayor, cambio de régimen cambiario de una divisa central de la celda) | Mensual | Métricas por celda | Certificados CERT- vigentes, en observación o revocados | F6; CT-10; CT-19 |
| EVAL-F06 | Aplicabilidad de horizontes por segmento | Pasar «Sí» → «Limitado» ante inferioridad demostrada frente al paseo aleatorio (DM-HLN, n ≥ 30); «Limitado» → «Sí» con certificado; proponer tipo 3 para todo cambio que implique «No» (p. ej., H1 en ESTR) | Mensual | Métricas, certificados | Cambios en la matriz 8.3 de F10; propuestas | F10; F6 |
| EVAL-F07 | Sobreconfianza y riesgo de cola del carry | Comparar probabilidad media con frecuencia (p̄ − ō > 0,10 y binomial p < 0,05), pendiente de calibración < 0,8, uso de bandas, gradiente de E y del vocabulario de confianza; frecuencia de resultados peores que el escenario adverso en celdas de carry | Mensual | Métricas por celda y banda | Alertas; LEC-FX- | CT-19; F6 |
| EVAL-F08 | Lecciones LEC-FX- | Redactar con ámbito (segmento, horizonte, divisa, agente, fuente, método), observación con referencia, evidencia, recomendación operativa, fuerza (anecdótica, recurrente, estadística) y caducidad; AAR de fallos relevantes distinguiendo mala suerte (sorpresa no previsible) de mal juicio (p. ej., tesis que ignoraba lo descontado por el forward); consolidar para respetar el máximo de 10 por ámbito; revisar, caducar o refutar | Semanal y mensual | Métricas, HA, F5, AAR | LEC-FX- vigentes en F6 | F6; CT-19 |
| EVAL-F09 | Recalibración dentro de bandas | Elegir parámetro (pesos de RK, pesos de A FX incluido el carry, umbrales, GC0–GC2, bandas verbales…) y objetivo; validar fuera de muestra con origen móvil, purga y embargo; encoger y acotar a bandas; re-ejecutar; aplicar en F10 con nueva `methodology_version` menor (FX-1.0 → FX-1.1); un cambio por parámetro y trimestre | Trimestral | F10, métricas, F4, F3 | Ajustes AJU- en F10 y F6 | F10; F6; CT-09; CT-10 |
| EVAL-F10 | Evaluación sombra | Calcular en paralelo con la versión anterior (HT-03); comparar al cierre del trimestre; confirmar o revertir con registro | Continuo durante el trimestre; cierre trimestral | Ajustes en sombra | Confirmación o reversión | F10; F6; HT-03 |
| EVAL-F11 | Propuestas de tipo 3 | Documentar cambios fuera de bandas, sin banda, de aplicabilidad hacia o desde «No», nuevos métodos o estrategias de segmento, referencias de comparación: evidencia, impacto, pruebas de regresión del Plan de pruebas del Bloque A Forex, plan de reversión | Cuando proceda; trimestral | Métricas, lecciones | Propuestas P3-EVAL- vía Orquestador | CT-19 |
| EVAL-F12 | Fiabilidad de fuentes de opinión cambiarias | Resolver los pronósticos explícitos registrados por el Buscador en F9 (previsiones de pares, encuestas de expectativas, sendas de bancos centrales) y los CLM-FX- resolubles de F2; calcular la habilidad frente al paseo aleatorio (BSS en probabilidades; 1 − MSE/MSE del paseo aleatorio en niveles; 2·acierto − 1 en direcciones; frente a lo descontado en decisiones de bancos centrales); contraer (k = 20); traducir a `puntos_historial` = 10 + 10·SS_c (0–20); medir el sesgo de dirección de cada fuente | Mensual | F9, F2, HT-01 | Registros FUE- por ficha de F9 | CT-19 (al Buscador); F6 |
| EVAL-F13 | Lecciones de producto | Agrupar preguntas repetidas (umbral de F10); analizar utilidad 1–5 como ordinal; comparar la rentabilidad total relativa de opciones enviadas al Bloque B frente a descartadas | Semanal (avisos) y mensual | CT-22, F5 | LEC-FX- de producto; PRO- | CT-22; CT-19; F6 |
| EVAL-F14 | Historial de aciertos publicable | Calcular por segmento y horizonte, ventana de 12 semanas y desde el inicio de la versión, universo completo; acierto = rentabilidad total con carry del ámbito por encima de la referencia de su segmento; tasa esperada por azar = la del paseo aleatorio sin fuga (con el carry de cada opción); significación binomial con n ≥ 30; nota de muestra pequeña | Semanal, antes de C1 | F4, F3 | HAC- en F6 (lo incorpora el Analizador al CT-15) | F6 |
| EVAL-F15 | Calibración de presupuestos | Mediana y p75 del consumo frente a referencia por segmento, capa transversal, nivel y fase; valor por UC; propuestas de ajuste y de reglas de parada | Mensual y trimestral | F5, HA | Propuestas; lecciones de nivel A | CT-19 |
| EVAL-F16 | Asignación exploratoria con bandits | Muestreo de Thompson Beta-Bernoulli con descuento sobre celdas de exploración de cada segmento (divisas, pares, estrategias) y prioridades de fuentes; suelo 5 %, techo 40 %; registro de propensiones | Mensual | F5, F3, F4 | Recomendación BAN- de reparto de la rotación exploratoria | CT-19; F6 |
| EVAL-F17 | Informe de aprendizaje | Emitir CT-19 semanal, mensual y trimestral con extractos por destinatario (incluidos los Analistas transversales); publicar «Novedades» en F6 | Semanal, mensual, trimestral | Todo lo anterior | CT-19; Novedades | CT-19; F6 |
| EVAL-F18 | Revisión trimestral | Aportar estado de calibración frente al paseo aleatorio, certificados, lecciones, ajustes y propuestas a la revisión con Orquestador y operador | Trimestral | F6, F10 | Dossier de aprendizaje | CT-19 |
| EVAL-F19 | Evaluar los pronósticos H5 por hitos (V1.1) | Resolver cada HIT-FX- en su fecha sin fuga frente a su referencia ingenua; publicar en F6 el estado del PRG H5 (EN_CURSO_CONFORME, DESVIADO, INVALIDADO) y la tasa de hitos cumplidos por celda; degradar la celda a «No» con < 50 % y ≥ 20 hitos; nunca certificar H5 | Fecha de cada hito (C5) | F4; HT-01 | Entradas HIT y H5 en F6 | F6; F10; CT-19 |
| EVAL-F20 | Aprender de las consultas y de los seguimientos (V1.1) | Convertir CONSULTA_RECURRENTE en lecciones de normalización de peticiones; medir el valor de la vigilancia encargada con DECISION_SEGUIMIENTO (recomendación frente a resultado y decisión del Broker) | CT-22 | F5; F11; F4 | Lecciones de producto; métricas C6 | CT-22; F6 |

## 3. Indicadores de desempeño

| KPI | Definición | Objetivo |
|---|---|---|
| Puntualidad de resolución | PRG-FX- resueltos ≤ 2 días hábiles tras su fecha (con fijación disponible) | ≥ 95 % |
| Tasa de NO_RESOLUBLE | NO_RESOLUBLE / vencidos | < 3 % (tendencia decreciente) |
| Correcciones de resolución | Resoluciones corregidas (fijación, par invertido, signo del carry) / resueltas | < 1 % |
| Fugas detectadas a posteriori | Casos (incluida la anticipación en fijaciones) | 0 |
| Certificados revocados en sus primeros 3 meses | Señal de certificación prematura | < 20 % de los emitidos |
| Recalibraciones revertidas tras la sombra | Revertidas / aplicadas | < 30 % |
| Lecciones aplicadas | LEC-FX- vigentes cuya aplicación verifica el Orquestador (AS-11) | ≥ 90 % |
| Lecciones refutadas | LEC-FX- refutadas / emitidas | Seguimiento (sin objetivo fijo) |
| Historial de aciertos publicado a tiempo | Semanas con HAC- disponible antes de C1 | 100 % |
| Calibración del bloque | ECE agregado de celdas con n ≥ 50 | Tendencia decreciente |
| Cobertura de la fiabilidad de fuentes | Fuentes de F9 con pronósticos registrados y medidos frente al paseo aleatorio | Creciente; ≥ 70 % de las fuentes de opinión A/B en el primer año |
| Consumo propio | UC frente a referencias (diario ≤ 1, semanal ≤ 3, mensual ≤ 10, trimestral ≤ 20) | ≤ 100 % |

## 4. Lo que el Evaluador NO hace

- No formula pronósticos ni modifica afirmaciones, probabilidades, fechas, criterios ni referencias de los PRG congelados (R11).
- No excluye pronósticos desfavorables, de opciones descartadas por el Broker o de finalistas no publicadas.
- No certifica sin batir al paseo aleatorio con el criterio del Anexo A ni recalibra sin muestra suficiente, fuera de bandas o sin evaluación sombra.
- No sustituye a posteriori la fijación, el mercado (*onshore*/*offshore*) ni la fuente de resolución declarados.
- No toca reglas críticas, seguridad, canales, matriz de archivos ni parámetros de régimen «Operador» o «Servicio».
- No selecciona opciones, no audita procedimientos ni emite guías de mejora (eso es del Orquestador).
- No mide instrumentos ni sus costes (Bloque B).
- No calcula «de cabeza» métricas publicadas: las pide al Motor.
- No escribe en F9 ni en F2: la fiabilidad de fuentes la registra en F6 y la comunica al Buscador.
- No se comunica con el Broker, el usuario, el Bloque B, el Bloque A general ni otros bloques; sus propuestas de tipo 3 llegan al operador a través del Orquestador.
