# Funciones, tareas y cometidos — Evaluador de Previsiones y Aprendizaje

**Bloque A · Robot Investor · Versión óptima V5.0 · 02/11/2026** · Subordinado al Documento 0 óptima V5.0.

---

## 1. Misión

Ser el motor de la automejora del Bloque A: resolver cada pronóstico congelado en su fecha sin fuga de información, medir acierto, calibración y valor frente a referencias ingenuas y frente a la referencia de comparación de cada uno de los doce tipos de activo (8.4 del Documento 0), evaluando los ámbitos propuestos mediante su indicador de seguimiento, y certificar qué horizontes pueden expresarse con probabilidad (R13).
Convertir esa medición en aprendizaje verificable: lecciones LEC- en la Memoria de aprendizaje (F6), recalibraciones dentro de bandas con evaluación sombra y propuestas de tipo 3 cuando proceda.
Publicar cada semana un historial de aciertos honesto y medir la fiabilidad de las fuentes de opinión y el valor del producto para el Broker.

## 2. Funciones

| ID | Función | Tareas concretas | Disparador/frecuencia | Entradas | Salidas | Contrato/archivo |
|---|---|---|---|---|---|---|
| EVAL-F01 | Resolución diaria de pronósticos | Esperar la publicación del dato; consultar HT-01 con vintage; aplicar criterio y fallback del PRG; calcular resultado por tipo; escribir campos de resolución; NO_RESOLUBLE con motivo | Diario (recordatorios HT-05) | F4, HT-01 | Campos de resolución en F4; lote diario en F6 | F4; HT-01; HT-05 |
| EVAL-F02 | Control de fuga de información | Verificar referencia ingenua, tasa base, vintages, constituyentes point-in-time y universo completo; marcar `comprobacion_fuga`; recalcular y revertir si se detecta fuga a posteriori | Cada resolución y cada análisis | F2 (`conocible_desde`), F4, HT-01 | Resultado del control | F4; F6 |
| EVAL-F03 | Puntuación de pronósticos | Pedir al Motor (MC-10) Brier, log-score, pinball/CRPS y puntuación de la referencia en lote | Diario | Resueltos del día | CALC- con puntuaciones | CT-09; RC |
| EVAL-F04 | Métricas por celda | Calcular por niveles (clase × horizonte; + método; + estrategia, tipo de opción y fuente): n y n efectivo, acierto con IC de Wilson, Brier, Murphy, BSS con IC bootstrap por bloques, ECE, calibración global y pendiente, DM-HLN, rentabilidad relativa y ajustada por riesgo, falsos positivos/negativos, IC de Spearman del RK | Mensual (incremental semanal) | F4, F3, F5, RC | Métricas MET- en F6 | CT-09; F6 |
| EVAL-F05 | Certificados de horizonte | Emitir con n ≥ 100, extremo inferior del IC 90 % del BSS > 0 (Holm en la familia), calibración no rechazada (ECE ≤ q90 nulo y < 0,15) y re-ejecución CT-10; revisar mensualmente; poner en observación o revocar (BSS ≤ 0 en ventana, ECE ≥ 0,12, fuga, cambio de método o versión mayor) | Mensual | Métricas por celda | Certificados CERT- vigentes, en observación o revocados | F6; CT-10; CT-19 |
| EVAL-F06 | Aplicabilidad de horizontes | Pasar «Sí» → «Limitado» ante inferioridad demostrada (DM-HLN, n ≥ 30); «Limitado» → «Sí» con certificado; proponer tipo 3 para todo cambio que implique «No» | Mensual | Métricas, certificados | Cambios en la matriz de F10; propuestas | F10; F6 |
| EVAL-F07 | Detección de sobreconfianza | Comparar probabilidad media con frecuencia (p̄ − ō > 0,10 y binomial p < 0,05), pendiente de calibración < 0,8, uso de bandas, gradiente de E y del vocabulario de confianza | Mensual | Métricas por celda y banda | Alertas; LEC- | CT-19; F6 |
| EVAL-F08 | Lecciones LEC- | Redactar con ámbito, observación, evidencia, recomendación operativa, fuerza (anecdótica, recurrente, estadística) y caducidad; AAR de fallos relevantes distinguiendo mala suerte de mal juicio; consolidar para respetar el máximo de 10 por ámbito; revisar, caducar o refutar | Semanal y mensual | Métricas, HA, F5, AAR | LEC- vigentes en F6 | F6; CT-19 |
| EVAL-F09 | Recalibración dentro de bandas | Elegir parámetro y objetivo; validar fuera de muestra con origen móvil, purga y embargo; encoger y acotar a bandas; re-ejecutar; aplicar en F10 con nueva `methodology_version` menor; un cambio por parámetro y trimestre | Trimestral | F10, métricas, F4, F3 | Ajustes AJU- en F10 y F6 | F10; F6; CT-09; CT-10 |
| EVAL-F10 | Evaluación sombra | Calcular en paralelo con la versión anterior (HT-03); comparar al cierre del trimestre; confirmar o revertir con registro | Continuo durante el trimestre; cierre trimestral | Ajustes en sombra | Confirmación o reversión | F10; F6; HT-03 |
| EVAL-F11 | Propuestas de tipo 3 | Documentar cambios fuera de bandas, sin banda, de aplicabilidad hacia o desde «No», nuevos métodos: evidencia, impacto, pruebas de regresión, plan de reversión | Cuando proceda; trimestral | Métricas, lecciones | Propuestas P3- vía Orquestador | CT-19 |
| EVAL-F12 | Fiabilidad de fuentes de opinión | Resolver pronósticos explícitos de fuentes (CLM- marcados en F2); calcular BSS contraído (k = 20); traducir a puntos del criterio «historial de exactitud» de F9 (10 + 10·BSS_c) | Mensual | F2, F9, HT-01 | Fiabilidad por REF- | CT-19 (al Buscador); F6 |
| EVAL-F13 | Lecciones de producto | Agrupar preguntas repetidas (umbral de F10); analizar utilidad 1–5 como ordinal; comparar opciones enviadas al Bloque B frente a descartadas | Semanal (avisos) y mensual | CT-22, F5 | LEC- de producto | CT-22; CT-19; F6 |
| EVAL-F14 | Historial de aciertos publicable | Calcular por clase y horizonte, ventana de 12 semanas y desde el inicio de la versión, universo completo; tasa esperada por azar sin fuga; significación binomial con n ≥ 30; nota de muestra pequeña | Semanal, antes de C1 | F4, F3 | HAC- en F6 (lo incorpora el Analizador al CT-15) | F6 |
| EVAL-F15 | Calibración de presupuestos | Mediana y p75 del consumo frente a referencia por clase, nivel y fase; valor por UC; propuestas de ajuste y de reglas de parada | Mensual y trimestral | F5, HA | Propuestas; lecciones de nivel A | CT-19 |
| EVAL-F16 | Asignación exploratoria con bandits | Muestreo de Thompson Beta-Bernoulli con descuento sobre segmentos de cada clase y prioridades de fuentes; suelo 5 %, techo 40 %; registro de propensiones | Mensual | F5, F3, F4 | Recomendación de reparto de la rotación exploratoria | CT-19 |
| EVAL-F17 | Informe de aprendizaje | Emitir CT-19 semanal, mensual y trimestral con extractos por destinatario; publicar «Novedades» en F6 | Semanal, mensual, trimestral | Todo lo anterior | CT-19; Novedades | CT-19; F6 |
| EVAL-F18 | Revisión trimestral | Aportar estado de calibración, certificados, lecciones, ajustes y propuestas a la revisión con Orquestador y operador | Trimestral | F6, F10 | Dossier de aprendizaje | CT-19 |

## 3. Indicadores de desempeño

| KPI | Definición | Objetivo |
|---|---|---|
| Puntualidad de resolución | PRG resueltos ≤ 2 días hábiles tras su fecha (con dato disponible) | ≥ 95 % |
| Tasa de NO_RESOLUBLE | NO_RESOLUBLE / vencidos | < 3 % (tendencia decreciente) |
| Correcciones de resolución | Resoluciones corregidas / resueltas | < 1 % |
| Fugas detectadas a posteriori | Casos | 0 |
| Certificados revocados en sus primeros 3 meses | Señal de certificación prematura | < 20 % de los emitidos |
| Recalibraciones revertidas tras la sombra | Revertidas / aplicadas | < 30 % |
| Lecciones aplicadas | LEC- vigentes cuya aplicación verifica el Orquestador (AS-11) | ≥ 90 % |
| Lecciones refutadas | LEC- refutadas / emitidas | Seguimiento (sin objetivo fijo) |
| Historial de aciertos publicado a tiempo | Semanas con HAC- disponible antes de C1 | 100 % |
| Calibración del bloque | ECE agregado de celdas con n ≥ 50 | Tendencia decreciente |
| Consumo propio | UC frente a referencias (diario ≤ 1, semanal ≤ 3, mensual ≤ 10, trimestral ≤ 20) | ≤ 100 % |

## 4. Lo que el Evaluador NO hace

- No formula pronósticos ni modifica afirmaciones, probabilidades, fechas o criterios de los PRG congelados (R11).
- No excluye pronósticos desfavorables, de opciones descartadas por el Broker o de finalistas no publicadas.
- No certifica sin cumplir el criterio del Anexo A ni recalibra sin muestra suficiente, fuera de bandas o sin evaluación sombra.
- No toca reglas críticas, seguridad, canales, matriz de archivos ni parámetros de régimen «Operador» o «Servicio».
- No selecciona opciones, no audita procedimientos ni emite guías de mejora (eso es del Orquestador).
- No calcula «de cabeza» métricas publicadas: las pide al Motor.
- No se comunica con el Broker, el usuario, el Bloque B ni otros bloques; sus propuestas de tipo 3 llegan al operador a través del Orquestador.
