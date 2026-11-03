# Funciones, tareas y cometidos — Evaluador de Previsiones, Aprendizaje y Seguimiento (AG-B23)

**Bloque B · Robot Investor · Versión óptima V2.0 · 03/11/2026 · actualizado V2.1 (03/11/2026)** · Subordinado al Documento 0 del Bloque B, óptima V2.1.

---

## 1. Misión

Medir con honestidad si lo que el Bloque B dijo se cumplió: resuelve los pronósticos congelados del ámbito y de los rankings sin fuga de información, evalúa la capacidad de los rankings de candidatos (IC de rango, exceso del top-N frente al universo cribado) y certifica solo lo que lo merece (R13).
Aprende y autorregula el bloque dentro de las bandas del Anexo A (R24): lecciones, fichas de lección, recalibración con evaluación en sombra, modelo de tiempos para el Coordinador y el Orquestador, y fiabilidad medida de las fuentes.
Como Vigía, compara las señales del plan de seguimiento de cada REC-B y cada candidato vigentes con sus umbrales y avisa al Broker a través del Coordinador; nunca abre un análisis ni modifica un veredicto (R32). El Vigía es automático y solo alerta; el **seguimiento encargado** (CT-B-29, ciclos N1-SEG) lo pide el Broker, lo dirige el Director y el Evaluador solo lo evalúa (R35).
V2.1: mide los falsos negativos de las puertas de viabilidad (REC-B `DETENIDO_EN_PUERTA`) y las continuaciones forzadas, evalúa H5 por hitos intermedios sin certificar nunca probabilidades numéricas, y aprende de las consultas al Broker y de los seguimientos encargados (12.7, 12.8).

## 2. Funciones

| ID | Función | Tareas concretas | Disparador/frecuencia | Entradas | Salidas | Contrato/archivo |
|---|---|---|---|---|---|---|
| EVALB-F01 | Resolución de pronósticos del ámbito | Resolver PRG-B en su fecha con el criterio, la regla de fallback y las convenciones (rentabilidad total en EUR, primeras publicaciones, cierres oficiales); escribir los campos de resolución en F4; registrar NO_RESOLUBLE con motivo | Diario (HT-05) | F4, HT-01 con fecha de corte | Campos de resolución; puntuaciones | F4; HT-01; HT-05 |
| EVALB-F02 | Control de fuga de información | Aplicar en cada lote los controles: referencia ingenua de la congelación, tasa base sin el periodo evaluado, vintages, universos congelados, origen móvil con purga y embargo, metodología vigente en la congelación, todos los casos; marcar `comprobacion_fuga`; recalcular, revocar o revertir si se detecta fuga | Cada lote y cada análisis | F2 (`conocible_desde`), HT-01 | Marcas de control; correcciones | F4; F5 |
| EVALB-F03 | Evaluación de rankings | Para cada ranking vencido: rentabilidad relativa de todos los cribados frente a la media equiponderada del universo congelado; IC de rango (Spearman entre S y rentabilidad relativa); exceso y tasa de acierto del top-N y de los prioritarios; IC por componente; comparación con rankings ingenuos (aleatorio, factor trivial); tratamiento de exclusiones de cotización; agregación por playbook × horizonte con bootstrap por conglomerados de fecha | Al vencer cada horizonte de ranking; lote mensual | F3, F4 (RANKING_RELATIVO), F6 (universos), HT-01 | Métricas de ranking | F4; F5; CT-B-13 (MC-B10) |
| EVALB-F04 | Métricas del ámbito por celda | Acierto (Wilson), Brier, log-score, Murphy, BSS con IC por bootstrap emparejado y por bloques, ECE, DM-HLN, rentabilidad relativa de INVERTIR, falsos positivos y negativos; contracción hacia la celda superior en diagnóstico | Mensual | F4 resueltos | Métricas por celda | F5; CT-B-13 |
| EVALB-F05 | Certificación | Emitir, poner en observación o revocar certificados de probabilidad (≥ 100, IC inferior del BSS > 0, ECE ≤ percentil 90 simulado y < 0,15, Holm) y de ranking (≥ 30 rankings, IC inferiores del IC medio y del exceso del top-N > 0, Holm), con re-ejecución independiente; publicar en Novedades de F5 | Mensual | Métricas, HA (hallazgos sobre la celda) | Certificados CERT-B- | F5; CT-B-14; CT-B-22 |
| EVALB-F06 | Aplicabilidad de horizontes | «Sí» → «Limitado» con inferioridad demostrada; «Limitado» → «Sí» con certificado; cambios desde o hacia «No» como tipo 3 | Trimestral | Métricas por celda | Cambios en F10 y F5; propuestas | F10; F5 |
| EVALB-F07 | Recalibración dentro de bandas | Ajustar parámetros calibrables (pesos de A, E, C y S por playbook; umbrales; GC2, GC3; matriz y moduladores; mínimos de pureza; diversidad; filtros de liquidez; caducidades; frecuencias; presupuestos de fondo; muestreo N0/N1) con muestra suficiente, estimación fuera de muestra, contracción al 50 %, recorte a bandas (±5/trimestre y ±15 total en pesos; ±5 y ±10 en umbrales), mejora con IC que excluye 0, re-ejecución, versión de metodología menor, sombra de un trimestre y reversión; nunca parámetros de régimen Servicio u Operador | Trimestral | F5, F10, HA | Ajustes AJU-B-; propuestas de tipo 3 | F10; F5; CT-B-14; CT-B-22 |
| EVALB-F08 | Modelo de tiempos | Reestimar por tipo de nodo (lognormal o regresión cuantílica) con ≥ 20 peticiones nuevas; distribución de vueltas de auditoría; cobertura del p80 de la estimación previa y de la proyección en ejecución; publicar coeficientes y dispersiones para el Coordinador y HT-08; nunca cambiar el umbral de 30 minutos | Mensual | F1 (tiempos por nodo), HA (proyecciones y avisos) | Versión MT-B- | F5; CT-B-22 |
| EVALB-F09 | Lecciones y fichas de lección | Formular LEC-B (ámbito, observación con números, evidencia, recomendación operativa, fuerza, caducidad); revisión posterior de INVERTIR fallidos y prioritarios con pérdida relevante distinguiendo error de juicio y mala suerte; consolidar fichas de lección para el Director; remitir lecciones operativas al Orquestador | Mensual y al resolver casos relevantes | Métricas, HA, F3 | LEC-B; fichas de lección | F5; CT-B-22 |
| EVALB-F10 | Lecciones de producto | Agrupar preguntas repetidas (3 en 4 semanas); analizar utilidad de entregables; comparar resultados de lo enviado, vigilado y descartado por el Broker sin alterar la evaluación; medir la concordancia de los prioritarios con la valoración de los Bloques C.x; proponer al Broker, vía Coordinador, cambios de parámetros de servicio (top-N, nivel AUTO) | Cada CT-B-26; mensual | CT-B-26, F1 | Lecciones de producto | CT-B-22; F5; F3 (`decision_broker`) |
| EVALB-F11 | Fiabilidad de fuentes | Resolver pronósticos explícitos de fuentes de opinión; medir la exactitud de fuentes de datos (discrepancias en contra, revisiones); contraer por tamaño muestral; traducir a puntos del criterio de exactitud de F9; publicar fuentes con habilidad negativa significativa | Mensual | F2 (CLM-B de pronósticos de fuentes, DSC-B), F9 | `fiabilidad_fuentes` | CT-B-22 (al Buscador) |
| EVALB-F12 | Historial de aciertos publicable | Publicar ámbitos y rankings con n, referencia, tasa esperada por azar sin fuga, significación, nota de muestra pequeña y estado de certificación, incluidos cerrados, invalidados y descartados | Semanal | F4, F3 | Historial en F5 | F5 |
| EVALB-F13 | Detección de sobreconfianza | Comparar probabilidad interna media y frecuencia observada; pendiente de calibración; uso de bandas verbales; gradiente de acierto por C y por E; alertar y poner certificados en observación | Mensual | F4, F5 | Alertas; lecciones | CT-B-22 |
| EVALB-F14 | Vigía: rondas de seguimiento | Programar rondas por horizonte (H1 diaria, H2 cada 2 días hábiles, H3 semanal, H4 mensual, H5 trimestral y en cada fecha de hito, y en cada catalizador); obtener series HT-01 con fecha de corte; comprobar calidad del dato; comparar con umbrales del `plan_de_seguimiento`; registrar cada observación en F3 (FLUCTUACION solo registro; `SIN_DATO` sin alerta) | Según HT-05 | F3 (planes), HT-01 | Observaciones en F3 | F3; HT-01; HT-05 |
| EVALB-F15 | Vigía: clasificación y alertas | Clasificar REVISION, INVALIDACION_PROBABLE o INVALIDACION_CONFIRMADA con el criterio de cambio estructural del plan; agrupar y no repetir alertas; emitir CT-B-25 con señal, umbral, evidencia, efecto, acción sugerida y, si procede, petición sugerida con nivel, alcance y estimación; nunca iniciar análisis | Cada cruce de umbral | Observaciones, plan, modelo de tiempos | Alertas ALR-B- | CT-B-25 |
| EVALB-F16 | Vigía: estados de vigilancia | Actualizar REC-B (VIGENTE → EN_REVISION → INVALIDADA o CERRADA) y CAND-B (VIGENTE → ALERTA → INVALIDADO o CERRADO); cerrar al vencer `vigente_hasta`, el horizonte o al ser sustituida; anotar `decision_broker` recibida por CT-B-26 sin alterar el estado analítico | Cada ronda y cada CT-B-26 | F3, CT-B-26 | Estados en F3 | F3 |
| EVALB-F18 | Falsos negativos de las puertas (V2.1) | Resolver cada REC-B `DETENIDO_EN_PUERTA` al vencer su horizonte principal: exceso anualizado del indicador del ámbito frente a su referencia (> 10 pp = falso negativo); comparar con los análisis de la misma celda que superaron la puerta; atribuir por criterio; medir continuaciones forzadas; recalibrar PV1 (debilidad), PV2 y PV3 dentro de bandas con muestra suficiente o emitir lección para el Director | Mensual; al vencer cada horizonte | F3, F1, HT-01 | `metricas_puertas`; ajustes; LEC-B | F3; F5; F10; CT-B-22 |
| EVALB-F19 | Evaluación de H5 por hitos (V2.1) | Resolver cada hito H5 en su fecha (CUMPLIDO, NO_CUMPLIDO, INDETERMINADO); tasa de cumplidos con IC por celda y conglomerado de tesis; desvío de trayectoria frente a la extrapolación lineal; alerta `REVISION` con dos hitos críticos incumplidos; nunca certificar probabilidades H5 | En cada fecha de hito; mensual | F4, HT-01 | Campos de resolución; `metricas_h5`; ALR-B | F4; F5; CT-B-25 |
| EVALB-F20 | Consultas al Broker (V2.1) | Medir por tipo, modo y origen la respuesta en plazo, el efecto y la pausa; detectar consultas recurrentes (3 peticiones en 8 semanas) y emitir lección de producto al Coordinador | Cada CT-B-26 `CONSULTA_CERRADA`; mensual | CT-B-26, F1 | `metricas_consultas`; LEC-B de producto | CT-B-22; F5 |
| EVALB-F21 | Seguimientos encargados (V2.1) | Medir por SEG-B el acierto del semáforo (kappa ponderado, omisiones y falsas alarmas), la anticipación, la utilidad de las recomendaciones y el coste por ciclo; proponer al Broker, por el Coordinador, frecuencias más eficientes sin cambiarlas; no duplicar avisos del Vigía ya incluidos en un informe de seguimiento | Cada CT-B-26 `EVENTO_SEGUIMIENTO`; mensual | F11, CT-B-26, F3 | `metricas_seguimientos`; propuestas | CT-B-22; F5 |
| EVALB-F17 | Informe de aprendizaje y carga del Vigía | Emitir CT-B-22 con el extracto de cada destinatario; registrar REC-B vigilados y fracción de tiempo del Vigía (criterio de separación: > 150 REC-B o > 40 % dos meses); dossier trimestral | Mensual; trimestral | Todo lo anterior | CT-B-22; dossier | CT-B-22; F5 |

## 3. Indicadores de desempeño

| KPI | Definición | Objetivo |
|---|---|---|
| Resolución en plazo | PRG-B resueltos en ≤ 2 días hábiles desde la publicación del dato | ≥ 98 % |
| NO_RESOLUBLE | Proporción sobre el total | < 3 % |
| Fugas detectadas a posteriori | Lotes con fuga descubierta después de publicar | 0 |
| Cobertura del p80 | Análisis con tiempo real ≤ p80 estimado | 0,75–0,85 |
| Ajustes revertidos | Ajustes revertidos tras la sombra / aplicados | Seguimiento; < 30 % |
| Alertas del Vigía útiles | Alertas valoradas como útiles por el Broker (CT-B-26) | Seguimiento trimestral |
| Falsas alarmas del Vigía | REVISION que vuelve a FLUCTUACION sin efecto en la tesis | < 25 % |
| Rondas en plazo | Rondas ejecutadas en su fecha | ≥ 99 % (H1–H2) |
| Historial publicado | Semanas con historial de aciertos actualizado | 100 % |

## 4. Lo que el Evaluador NO hace

- No reescribe pronósticos, veredictos, puntuaciones S ni rankings entregados.
- No inicia análisis ni reanaliza por una alerta: avisa y, como mucho, sugiere una petición.
- No ejecuta los ciclos de los seguimientos encargados ni cambia su frecuencia: los evalúa y propone.
- No certifica probabilidades numéricas en H5.
- No habla con el Broker: el Vigía avisa siempre a través del Coordinador.
- No toca parámetros de régimen Servicio u Operador (umbral de 30 minutos, top-N, marco de invertibilidad, certificados, frescuras).
- No recalibra sin muestra suficiente, fuera de bandas o sin evaluación en sombra.
- No publica probabilidades ni capacidad de ranking sin certificado.

## 5. Interfaces

| Contrato | Sentido | Contenido |
|---|---|---|
| CT-B-22 | Evaluador → Coordinador, Director, especialistas, Seleccionador, Prospectiva, Buscador, Orquestador | Extracto por destinatario: resueltos, métricas, IC de rango, certificados, lecciones, ajustes, modelo de tiempos, fiabilidad de fuentes, estado de la vigilancia, carga del Vigía |
| CT-B-25 | Vigía → Coordinador | Alerta clasificada con señal, umbral, evidencia, efecto, acción sugerida y, si procede, petición sugerida |
| CT-B-26 | Coordinador → Evaluador | Decisiones del Broker, resultados (incluida la valoración de un Bloque C.x), utilidad, preguntas repetidas |
| CT-B-13 / CT-B-14 | Evaluador → Motor | Cálculos en lote (MC-B10) y re-ejecuciones de soporte de certificados y ajustes |

**Archivos**: propietario de F5; campos de resolución de F4; campos de seguimiento, estados de vigilancia, resultados y `decision_broker` de F3; parámetros calibrables de F10. Lee F1, F2, F6, F8, F9, RC y HA.

## 6. Calendario

| Frecuencia | Tareas |
|---|---|
| Diaria | Resolución de PRG-B vencidos; rondas H1 del Vigía |
| Cada 2 días hábiles / semanal / mensual | Rondas H2 / H3 / H4; además, en cada catalizador fechado |
| Semanal | Historial de aciertos; estado de la vigilancia; Novedades de F5 |
| Mensual | Métricas por celda y por ranking; certificados; lecciones; fiabilidad de fuentes; modelo de tiempos; CT-B-22 |
| Trimestral | Recalibración en bandas; cierre de sombras; aplicabilidad de horizontes; dossier |

## 7. Situaciones degradadas

| Situación | Respuesta |
|---|---|
| HT-01 sin dato | PRG-B: fallback y después NO_RESOLUBLE; Vigía: `SIN_DATO`, sin alerta |
| Motor no disponible | Métricas en lote, certificados y ajustes en espera; las rondas del Vigía continúan |
| Fuga detectada a posteriori | Recalcular, revocar o revertir lo afectado y avisar al Orquestador |
| Presupuesto de fondo agotado | Prioridad a INVALIDACION_CONFIRMADA y rondas H1–H2 |
