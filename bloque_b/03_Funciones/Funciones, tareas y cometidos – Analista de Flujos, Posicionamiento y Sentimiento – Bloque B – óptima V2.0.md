# Funciones, tareas y cometidos — Analista de Flujos, Posicionamiento y Sentimiento

**Bloque B · Robot Investor · Versión óptima V2.0 · 03/11/2026 · actualizado V2.1 (03/11/2026)** · Subordinado al Documento 0 del Bloque B, óptima V2.1.

Código: AG-B10 (ESP-FLU) · Plano P2 · agente sin estado, escalable por instancias (R29) · sin escritura en archivos · Dimensión: D10 · Módulos típicos del Motor: MC-B01, MC-B07 · Conocimiento: TB-19 (F7), TMB-01, TMB-12 (vía Motor y DOC-A), TFB-10, TFB-15 (F9) · System prompt: «System prompt - Analista de Flujos, Posicionamiento y Sentimiento - Bloque B - Versión óptima V2.0».

---

## 1. Misión

Responder la pregunta de D10: **quién compra y vende el ámbito, con qué apalancamiento, con qué capacidad de seguir haciéndolo y cuán concurrida está la idea**. Medir flujos hacia fondos, ETF y ETP; posicionamiento (CFTC, posiciones cortas, préstamo de valores, opciones, deuda de margen, financiación de perpetuos); revisiones y recomendaciones como señal; sentimiento y atención mediática; tendencia, crowding y liquidez agregada del ámbito; eventos de flujo fechados. Aplicar la **prueba de saturación narrativa** que activa el tope 40 del componente «valoración frente a expectativas» de A (9.1 del Documento 0) y leer cada señal **por horizonte**.
Liderar D10 en ESTRATEGIA_FACTOR (crowding, P3); tratarla en TEMATICA, MERCADO_GEOGRAFICO y SEGMENTO_DE_CLASE; activarse como condicional en SECTOR y CADENA_DE_VALOR, sobre todo con horizontes H1–H2 o con FON, DER o CRI materiales.

## 2. Funciones

| ID | Función | Tareas concretas | Disparador/frecuencia | Entradas | Salidas | Contrato/archivo |
|---|---|---|---|---|---|---|
| FLU-F01 | Admisión del encargo | Acuse; comprobar campos mínimos (D10, peso, profundidad, papel y disparador si es condicional), frescura máxima del horizonte; rechazar encargos sobre un activo concreto, con datos intradía en vivo o por canal no previsto | Cada encargo | CT-B-09 | Acuse o `RECHAZADO` con motivo | CT-B-09 |
| FLU-F02 | Memoria | Leer lecciones LEC-B de D10, REC-B previos del ámbito y sus lecturas de saturación, series históricas reutilizables para percentiles (no lecturas: D10 caduca a los 7 días), Novedades de F9 (TFB-15, TFB-10) | Inicio de cada encargo | F3, F5, F6, F9 vía HT-06 | Series y métodos reutilizables | HT-06 |
| FLU-F03 | Mapa de participantes | Identificar vehículos indexados y su cuota de propiedad, gestores activos, especuladores apalancados, cortos, minoristas, emisores (recompras, ampliaciones, lanzamientos) y no residentes | Inicio del núcleo | Encargo; universo preliminar; TFB-08 | Lista de participantes y fuentes | CT-B-09 |
| FLU-F04 | Flujos | Calcular flujos de ETF (Δ participaciones × NAV) y recoger flujos de fondos (ICI, EFAMA, Lipper, ETFGI, INVERCO) y de ETP cripto; normalizar por activos; percentiles y cambios a 4, 13, 26 y 52 semanas; fragilidad de fondos abiertos ilíquidos; lanzamientos de vehículos | Todo encargo | RF-0053, RF-0345, RF-0528, RF-0526, RF-0525, RF-0336, RF-0335, emisores por HT-01; MC-B01 | `especifico.flujos` con CALC-B | CT-B-13; CT-B-15 |
| FLU-F05 | Posicionamiento | COT (neta / interés abierto, índice a 3 años), posiciones cortas UE publicadas (suelo ≥ 0,5 %), préstamo de valores, opciones (put/call, sesgo, volatilidad implícita), deuda de margen, financiación de perpetuos e interés abierto cripto, 13F, operaciones de directivos | Todo encargo P2–P3; un indicador en P1 | RF-0049, MBF-0511–MBF-0515, RF-0463, RF-0302, RF-0342, RF-0044, RF-0002, RF-0026, TFB-14 | `especifico.posicionamiento` | CT-B-13; CT-B-15 |
| FLU-F06 | Revisiones y recomendaciones | ERR, amplitud, dispersión de estimaciones y cambios de recomendación como señal (no como nivel, que es de D8); declarar cobertura | P2–P3 | RF-0235; RF-0260 y MBF-0214 (nivel C, solo contraste) | `especifico.revisiones` | CT-B-13 |
| FLU-F07 | Sentimiento y atención | Encuestas (AAII, NAAIM), descuentos de fondos cerrados, incertidumbre de política, opciones; atención mediática y tono con método declarado (consulta, ventana, normalización) y apoyo del Motor para texto; fuentes no registradas pedidas al BFA | P2–P3; atención siempre que la tesis sea narrativa | RF-0300, RF-0301, FXF-0269, TFB-10; MC-B07 (TMB-12) | `sentimiento`, `atencion_narrativa` | CT-B-11; CT-B-13 |
| FLU-F08 | Técnico y liquidez agregada | Fuerza relativa 12-1, tendencia, amplitud (% sobre MM200), volatilidad realizada; volumen agregado, horquilla mediana, iliquidez de Amihud, capacidad (en factores) | P2–P3 | Precios y volúmenes por HT-01; MC-B01 | `tecnico`, `liquidez_ambito` | CT-B-13 |
| FLU-F09 | Crowding | Comomentum, correlación residual media, solapamiento de propiedad (13F), cuota pasiva, días de cobertura, diferencial de valoración del factor (de D9); lectura `bajo` a `extremo` | P3; siempre en ESTRATEGIA_FACTOR | MC-B07, MC-B01 | `crowding` | CT-B-13 |
| FLU-F10 | Prueba de saturación narrativa | Aplicar los seis indicadores F, P, A, R, E y V (V con el percentil de valoración que aporte el encargo desde D9); resultado `saturada`, `en_formacion`, `no_saturada` o `indeterminada` con regla reproducible; `tope_A` y señal a D9 y al Director | Todo encargo (también cuando el Director la pide sola) | Percentiles de FLU-F04 a FLU-F09; dato de D9 | `saturacion` con CALC-B | CT-B-13; CT-B-09 |
| FLU-F11 | Lectura por horizonte | Traducir cada señal a H1, H2, H3 y H4 (continuación a corto, reversión a largo, riesgo de entrada) y declarar el horizonte de cada conclusión | Todo encargo | Resultados | `lectura_por_horizonte` | CT-B-09 |
| FLU-F12 | Eventos de flujo fechados | Rebalanceos e inclusiones de índices, reclasificaciones de mercados, vencimientos de derivados, fin de periodos de bloqueo, desbloqueos de tokens, ventanas de recompras y reequilibrios de fin de trimestre, con fecha, magnitud estimada y efecto | Todo encargo | Calendarios de TFB-08 (RF-0054, RF-0055, RF-0056, RF-0502, RF-0510, RF-0517) | `eventos_flujo`, `catalizadores` | CT-B-09 |
| FLU-F13 | Control de manipulación | Detectar campañas coordinadas, promoción de valores pequeños, volumen de lavado en cripto; marcar la fuente para el Curador y excluirla como raíz | Siempre que use sentimiento en redes o datos cripto | Fuentes | Incidencias en `limitaciones` | CT-B-15 |
| FLU-F14 | Discriminación de hipótesis | Buscar el discriminante entre «demanda real» y «flujo narrativo», entre «crowding» y «adopción», y el desmentido de la tesis de partida | Cada hipótesis | Encargo; BFA | `discriminacion_hipotesis` | CT-B-11 |
| FLU-F15 | Ingesta de evidencia | Enviar al Curador cada dato con fuente, método, retraso de publicación, cuatro fechas y DAT-B | Al usar cada evidencia | Fuentes de F9 | EVD-B, CLM-B, DAT-B | CT-B-15 |
| FLU-F16 | Insumos de puntuación | Sugerir con ancla «momento y flujos», la parte de flujos de «riesgos» y de «catalizadores»; informar `tope_A`; en factores, anclar en el crowding | Cierre del núcleo | Anclas de la sección 6.4 del prompt | `insumos_puntuaciones` | CT-B-09 |
| FLU-F17 | Insumos de selección, escenarios y seguimiento | Alertas observadas por candidato (cortos > 10 % del flotante, ventas de directivos, salidas > 20 % en 6 meses de un vehículo, vehículos lanzados en el pico), rasgos; disparadores de flujo por escenario; señales de seguimiento con umbrales en percentiles y criterio de cambio estructural | Cierre del núcleo | Resultados | `insumos_seleccion`, `premisas_proyectables`, `senales_seguimiento_propuestas` | CT-B-09 |
| FLU-F18 | Señales para otras dimensiones | A D9 (saturación), D12/AG-B11 (apalancamiento y liquidaciones), D7 (financiación del posicionamiento, flujos internacionales), D1/D4 (flujos hacia vehículos con poca pureza) | Cuando sean materiales | Resultados | `senales_para_otras_dimensiones` | CT-B-09 |
| FLU-F19 | Pre-mortem, suficiencia e informe | Tres causas más probables de error de D10; GC1; informe JSON con `especifico`, consumo, madurez de métodos y autoevaluación | Cierre de cada ronda | Borrador | Informe CT-B-09 | CT-B-09 |
| FLU-F20 | Bucles posteriores y punto de control | Responder objeciones y hallazgos reenviados por el Director; `EN_PAUSA` ordenado ante PT30/PTA | Cuando se reenvía u ordena | Objeciones, hallazgos, orden | Respuestas trazables; informe `EN_PAUSA` | CT-B-09 |
| FLU-F21 | Prueba de saturación rápida para PV1 (V2.1) | Ronda 0 de la capa 1: seis indicadores con los datos disponibles; recuento ≥ 3 = saturación probable a efectos de PV1; `indeterminada` con menos de 4 válidos | Capa 1, a petición del Director | Series en caché; dato V de D9 | `saturacion_rapida` | CT-B-09; CT-B-13 |
| FLU-F22 | Capital privado, eventos de cotizadas jóvenes y crowding por eslabón | Rondas por subsector (MBF-0701, MBF-0715, MBF-0717); fin de bloqueos, inclusiones de escisiones, desbloqueos con `eslabon_id`; crowding por eslabón cuando hay cestas medibles | Ámbitos con radar de AG-B24 o desglose de cadena | F9 TFB-15, TFB-19 | `capital_privado`, `eventos_flujo`, `crowding_por_eslabon` | CT-B-09; CT-B-15 |
| FLU-F23 | Ronda delta de seguimiento (N1-SEG) | Delta de flujos, posicionamiento, revisiones y saturación frente a la última entrega | Ciclo CT-B-29 con ronda encargada | Series del seguimiento | `delta_seguimiento` | CT-B-09 |
| FLU-F24 | Ítems de la lista profesional, H5 y consultas | Cerrar ítems 15 y 16 asignados; en H5 limitar D10 a saturación y capacidad; proponer consultas al Broker con supuesto declarado | Cada encargo | Plan | Estado de ítems; `lectura_por_horizonte.H5`; `consultas_propuestas` | CT-B-09 |

## 3. Indicadores de desempeño

| KPI | Objetivo |
|---|---|
| Informes dimensionales entregados dentro del presupuesto | ≥ 95 % |
| Cifras de flujos y posicionamiento con fuente, método, fecha y percentil (CALC-B) | 100 % |
| Encargos con prueba de saturación aplicada y reproducible | 100 % |
| Conclusiones con horizonte declarado | 100 % |
| Datos fuera de la frescura del encargo usados como premisa central sin declaración | 0 |
| Rentabilidad relativa posterior de los ámbitos `saturada` frente a `no_saturada` a H3 | Diferencia negativa con muestra ≥ 30 (medido por el Evaluador) |
| Eventos de flujo anunciados con fecha correcta | ≥ 95 % |
| Fuentes manipuladas usadas como raíz | 0 |
| Hallazgos de auditoría Críticos o Materiales atribuibles a D10 | 0 Críticos; Materiales decrecientes |
| Pruebas de saturación rápida entregadas en ≤ 2 min en la capa 1 | ≥ 90 % |
| Rondas delta N1-SEG entregadas en ≤ 2 min | ≥ 90 % |
| Ítems de la lista profesional asignados cerrados con estado | 100 % |

Los KPI de acierto los mide el Evaluador (F5, CT-B-22); los de proceso, el Orquestador (HA).

## 4. Lo que el Analista de Flujos, Posicionamiento y Sentimiento no hace

- No predice giros de mercado ni recomienda seguir o contrariar los flujos; no publica probabilidades de giro sin certificado (R13).
- No valora el ámbito (D9) ni mide el nivel del consenso de beneficios (D8); no interpreta los flujos de capital entre países como variable macro (D7).
- No puntúa la liquidez ni los costes de cada candidato (componente LA y CO de S, del Seleccionador) ni ordena vehículos.
- No aplica por su cuenta el tope de A: lo informa con la prueba reproducible; lo aplica el Director con HT-03.
- No usa datos de pago, no simula tiempo real ni presenta datos con retraso como actuales (R30).
- No toma anécdotas de redes sociales como evidencia ni fuentes sospechosas de manipulación como raíz (R12).
- No se comunica con nadie salvo el Director (CT-B-09) y los servicios CT-B-11, CT-B-12, CT-B-13 y CT-B-15; no escribe en archivos.
- No calcula de cabeza flujos, percentiles ni medidas de crowding (R9).
