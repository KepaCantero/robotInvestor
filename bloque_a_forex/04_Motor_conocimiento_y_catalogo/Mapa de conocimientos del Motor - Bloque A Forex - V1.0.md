# Mapa de conocimientos — Motor de Cálculo Avanzado (Forex) (AG-13)

**Bloque A Forex · Robot Investor · Versión óptima V1.0 · 02/11/2026** · Subordinado al Documento 0 del Bloque A Forex V1.0.

Archivo CC (propietario: operador, tipo 3; el Motor propone). Lectores: AG-13 y sus módulos, AG-15 (Documentador para el Motor), Analistas de segmento (AG-03 a AG-08), Analistas transversales (AG-09, AG-21), Orquestador técnico, Auditor, Evaluador. Sustituye, para este bloque, al «Mapa de conocimientos del Motor» V4.0 del Bloque A general; la numeración de áreas es propia de este bloque.

---

## 1. Propósito y uso

1.1. Este mapa enumera **todas** las áreas de conocimiento que el Motor debe dominar para calcular sobre divisas, con su nivel, su módulo responsable, su aplicación por segmento (G10N, G10M, EMAS, EMLA, EMEA, ESTR; 2.6 del Documento 0), su temática de F8 (TMX-01 a TMX-09, Anexo D) y su prioridad. Es autosuficiente: no remite a versiones anteriores.

1.2. **Usos gobernados**: (a) **enrutado**: el Orquestador de Cálculo sitúa cada petición CT-09 en su área, su módulo y su perfil; (b) **selección de métodos**: a igual precisión exigida, se prefiere el área y el método de nivel más bajo (I antes que II, II antes que III); (c) **rechazo con orientación**: una petición fuera de cobertura se rechaza indicando el área más próxima; (d) **ampliación**: propuestas de fichas, perfiles y módulos (tipo 3); (e) **mantenimiento del conocimiento**: el Documentador para el Motor (AG-15) organiza F8 por las temáticas TMX- y vigila la literatura de cada área (sección 6).

1.3. **Niveles de dominio**:

| Nivel | Significado | Activación |
|---|---|---|
| I · Fundamentación | Imprescindible; usado a diario por cualquier módulo | Siempre disponible |
| II · Especialización avanzada | Métodos especializados de uso frecuente en uno o varios segmentos | Bajo demanda, con ficha |
| III · Especialización condicionada | Métodos de uso ocasional, coste alto o riesgo de mal uso | Solo con petición explícita, ficha vigente y justificación en el plan |

1.4. **Prioridades de implantación**: **P0** núcleo imprescindible (incluye lo que exigen R7, R13, G3, la convención cambiaria, la comparación con el paseo aleatorio y la reproducibilidad); **P1** conocimiento cambiario con datos accesibles y uso frecuente; **P2** ampliación (datos especializados, uso ocasional o madurez metodológica baja).

1.5. **Cobertura no es obligación** (R15): ninguna investigación activa todas las áreas; el valor de la información decide. **Madurez** (R22): todas las áreas están **documentadas**; la implementación y validación de cada método constan en su ficha del Catálogo de cálculos del bloque (V1.0).

1.6. **Frontera con el Bloque B** (2.5 del Documento 0): las áreas se aplican a **ámbitos cambiarios** (par, cruce, cesta, bloque, estrategia, régimen) y a sus indicadores de seguimiento. Ningún área habilita al Motor para elegir o comparar instrumentos (contado, forward, futuro, opción, ETF/ETC, CFD), proveedores, costes de ejecución, apalancamiento, tamaño ni niveles de entrada. Las áreas de opciones (30–33) sirven para **leer** lo que el mercado descuenta, no para proponer contratos.

## 2. Bloques temáticos

| Bloque | Áreas | Módulos | Temáticas F8 | Prioridad dominante |
|---|---|---|---|---|
| I. Fundamentos y cálculo cambiario | 1–6 | MC-01 | TMX-03, TMX-08 | P0 |
| II. Series temporales, regímenes y volatilidad cambiaria | 7–10 | MC-02 | TMX-01, TMX-02 | P0 |
| III. Paridades, equilibrio y macro cambiaria | 11–17 | MC-03, MC-01 | TMX-01, TMX-03, TMX-04, TMX-06 | P0/P1 |
| IV. Prospectiva, simulación y regímenes cambiarios | 18–21 | MC-04, MC-05 | TMX-04, TMX-07 | P0/P1 |
| V. Aprendizaje automático | 22–24 | MC-06 | TMX-09 | P0/P1 |
| VI. Riesgo, carteras de factores y decisión | 25–28 | MC-07 | TMX-06, TMX-07 | P0/P1 |
| VII. Valoración cambiaria, factores y opciones | 29–35 | MC-09, MC-01 | TMX-03, TMX-05, TMX-06 | P1 |
| VIII. Evaluación predictiva frente al paseo aleatorio y backtesting | 36–41 | MC-10 | TMX-08 | P0 |
| IX. Datos, metodología y reproducibilidad | 42–50 | STC-1 a STC-4, MC-01, MC-08 | TMX-08 (respaldo transversal) | P0 |
| X. Gobierno del servicio, seguridad y límites | 51–56 | Orquestador de Cálculo, MC-08 | TMX-08 (respaldo transversal) | P0 |

## 3. Inventario completo de áreas

Abreviaturas de segmento (2.6 del Documento 0): G10N, G10M, EMAS, EMLA, EMEA, ESTR; «Todos» = transversal.

### Bloque I · Fundamentos y cálculo cambiario

| Área | Contenido operativo | Nivel | Módulo | Aplicación por segmento | TMX | Prior. |
|---|---|---|---|---|---|---|
| 1. Matemáticas aplicadas y álgebra | Álgebra lineal (matrices, autovalores, Cholesky, espectral, número de condición), cálculo, interpolación, raíces (Newton, Brent), optimización elemental | I | MC-01 | Todos (covarianzas, volatilidad implícita, curvas de puntos) | TMX-08 | P0 |
| 2. Cálculo financiero cambiario | Convención BASE/COTIZADA y prioridad de la base, pips, inversión, cruces sintéticos con horquilla, variaciones de base y cotizada, rentabilidad total (contado + carry + cruzado), exceso por forwards, conversión a la divisa base del usuario, interés compuesto y continuo, CAGR, nominal/real | I | MC-01 | Todos | TMX-03 | P0 |
| 3. Probabilidad | Distribuciones (normal, t, lognormal, Pareto, binomial, Poisson, beta), colas pesadas, saltos, Bayes, cópulas básicas | I | MC-01 | Todos; saltos en EMLA, EMEA y regímenes | TMX-07 | P0 |
| 4. Estadística descriptiva y robusta | Localización, dispersión robusta, asimetría y curtosis, cuantiles, atípicos, percentiles y z-scores frente a historia | I | MC-01 | Todos (cribado de los seis segmentos) | TMX-08 | P0 |
| 5. Inferencia y diseño | Contrastes, IC, potencia, bootstrap, comparaciones múltiples (Holm, BH), HAC, error estándar del Sharpe | I | MC-01 | Todos | TMX-08 | P0 |
| 6. Convenciones monetarias, liquidación y fechas valor | Bases de días (Act/360, Act/365, Bus/252), tipos a un día (SOFR, €STR, TONA, SONIA, SARON, CORRA, AONIA…), contado T+2 y T+1, festivos de dos plazas y de EE. UU., día hábil siguiente modificado, regla de fin de mes, ON/TN/SN, fechas de vencimiento y entrega de opciones, cortes horarios y fijaciones (NY 17:00, WM/Reuters 16:00, BCE, Fed H.10, PBoC) | I | MC-01 | Todos; Bus/252 en EMLA (BRL); T+1 en G10M (CAD), EMEA (TRY), EMAS (PHP) | TMX-03 | P0 |

### Bloque II · Series temporales, regímenes y volatilidad cambiaria

| Área | Contenido operativo | Nivel | Módulo | Aplicación por segmento | TMX | Prior. |
|---|---|---|---|---|---|---|
| 7. Series temporales de tipos de cambio | Raíces unitarias (ADF, PP, KPSS, Zivot-Andrews), persistencia de tipos reales y sesgo de muestra pequeña, paneles de raíz unitaria, ARIMA y ETS como referencia, STL (flujos de fin de mes y de año), filtros (Hamilton; HP con advertencias) | I–II | MC-02 | Todos | TMX-01 | P0 |
| 8. Tendencias y momentum de series | Mann-Kendall con Hamed-Rao, Theil-Sen, aceleración, señal de serie temporal escalada por volatilidad | I–II | MC-02 | Todos; ESTR (momentum) | TMX-01 | P0 |
| 9. Rupturas, regímenes y no linealidad | CUSUM, Bai-Perron, Markov-switching, HMM de régimen cambiario y de riesgo, *dollar smile*, ESTAR/TAR, rupturas por cambio de régimen cambiario, intervención o redenominación | II–III | MC-02 | Todos; regímenes gestionados en EMAS y EMEA | TMX-01 | P0 |
| 10. Volatilidad cambiaria | Cierre a cierre con corte declarado, rango (Parkinson, Garman-Klass, Yang-Zhang), realizada intradía de 5 minutos y bipotencia, estacionalidad intradía y de anuncios, EWMA, GARCH/GJR/EGARCH con asimetría direccional, HAR-RV, QLIKE | I–II | MC-02 | Todos; asimetría direccional en EMLA y cruces con JPY | TMX-02 | P0 |

### Bloque III · Paridades, equilibrio y macro cambiaria

| Área | Contenido operativo | Nivel | Módulo | Aplicación por segmento | TMX | Prior. |
|---|---|---|---|---|---|---|
| 11. Econometría | MCO con HAC y Hodrick, regresiones predictivas y sesgo de Stambaugh, regresión espuria, cointegración (Engle-Granger, Johansen, DOLS), VECM, VAR e IRF, Granger | II | MC-03 | Todos | TMX-01 | P0 |
| 12. Paridades de intereses | CIP con bases de días, puntos forward, rendimientos implícitos, base cruzada (Du-Tepper-Verdelhan), efectos de fin de trimestre, UIP y regresión de Fama, enigma de la prima forward, carry y carry ajustado | I–II | MC-03, MC-01 | Todos; base en G10N (EUR, JPY, CHF) | TMX-03 | P0 |
| 13. Equilibrio y valoración | PPA absoluta y relativa, vida media (estimador insesgado en mediana), Balassa-Samuelson, BEER (DOLS, panel), FEER y balanza macro (EBA), NATREX (III), valor como factor | II–III | MC-03 | Todos; Balassa-Samuelson en EMAS y EMEA | TMX-04 | P1 |
| 14. Índices efectivos y cestas | NEER y REER (BPI, pesos de doble ponderación), DXY, índice amplio de la Fed, cestas con pesos y financiación, índices geométricos y aritméticos, referencia de comparación de emergentes | I–II | MC-01 | Todos; ESTR (cestas y dólar amplio) | TMX-04, TMX-06 | P1 |
| 15. Política monetaria cuantitativa | Expectativas implícitas por reunión (OIS, futuros), divergencia de sendas, reglas de Taylor y `r*`, sorpresas macro y monetarias estandarizadas, estudios de eventos intradía, diferencial a 2 años y sensibilidad del par | II | MC-03, MC-09 | G10N, G10M; EMEA y EMLA con curva líquida; transversal AG-09 | TMX-04 | P0 |
| 16. Balanza de pagos, reservas y términos de intercambio | Balanza básica, cuenta corriente ajustada, posición de inversión internacional, métrica ARA del FMI, Guidotti-Greenspan, índices de términos de intercambio de materias primas y sensibilidad | II | MC-03 | G10M, EMLA, EMEA, EMAS | TMX-04 | P1 |
| 17. Dependencia multivariante | Correlación con cortes sincronizados, DCC, dependencia de cola, PCA y factor dólar, betas a dólar, riesgo y materias primas | II | MC-03 | Todos; coherencia entre segmentos y apuestas independientes | TMX-06 | P0 |

### Bloque IV · Prospectiva, simulación y regímenes cambiarios

| Área | Contenido operativo | Nivel | Módulo | Aplicación por segmento | TMX | Prior. |
|---|---|---|---|---|---|---|
| 18. Prospectiva cuantitativa | Escenarios de política monetaria frente a lo descontado y su traslación al tipo de cambio, tornado y sensibilidad global, umbrales de invalidación, tasas base de episodios comparables, bloques de rentabilidad a largo plazo (carry + reversión) | II | MC-04, MC-05 | Todos (servicio a Prospectiva, CT-12) | TMX-04 | P0 |
| 19. Simulación y Monte Carlo | Generadores y semillas, paseo aleatorio lognormal, GARCH-t, saltos, cambio de régimen, Ornstein-Uhlenbeck del tipo real, bootstrap por bloques y filtrado, cuasi-Monte Carlo, cópulas, error de Monte Carlo | II | MC-05 | Todos | TMX-07 | P0 |
| 20. Tipos fijos, bandas y rupturas | Clasificación de facto (Ilzetzki-Reinhart-Rogoff), zonas objetivo (Krugman), ajuste por deriva (Svensson), probabilidad neutral al riesgo de ruptura por salto, simulación «se mantiene / se rompe», intervención | II–III | MC-05, MC-09 | EMAS (HKD, CNY), EMEA (Golfo, EGP, NGN), EMLA (ARS); G10N histórico (EUR/CHF) | TMX-07 | P1 |
| 21. Teoría de la información y señales | Entropía, relación señal-ruido, detección secuencial de cambios de distribución | II–III | MC-05 | Todos (soporte) | TMX-01 | P2 |

### Bloque V · Aprendizaje automático

| Área | Contenido operativo | Nivel | Módulo | Aplicación por segmento | TMX | Prior. |
|---|---|---|---|---|---|---|
| 22. Aprendizaje automático estadístico | Regularización, logística, árboles y ensambles, agrupación (clústeres de exposición), anomalías, interpretabilidad; redes profundas solo condicionadas | II (III las profundas) | MC-06 | Todos; clústeres para el Analizador | TMX-09 | P1 |
| 23. Predicción calibrada y validación temporal | Walk-forward, CV purgada con embargo, calibración (Platt, isotónica), conformal, combinación de previsiones, deriva | II | MC-06 (con MC-10) | Todos | TMX-09 | P0 |
| 24. Texto estructurado de bancos centrales | Tono y sorpresa de orientación sobre texto ya estructurado, similitud entre comunicados, métricas con conjunto de referencia | II (soporte) | MC-06 | G10N, G10M; transversal AG-09 | TMX-09 | P2 |

### Bloque VI · Riesgo, carteras de factores y decisión

| Área | Contenido operativo | Nivel | Módulo | Aplicación por segmento | TMX | Prior. |
|---|---|---|---|---|---|---|
| 25. Riesgo y eventos extremos | VaR, ES, EVT (POT, Hill), drawdown sobre rentabilidad total, liquidez, estrés histórico cambiario e inverso, escala de riesgo 1–5 con suelo de régimen | II–III | MC-07 | Todos | TMX-07 | P0 |
| 26. Riesgo de cola del carry | Asimetría negativa, colapsos (2008, 2015, 2024), *crash risk* y desastres raros, *peso problem*, carry neto de cobertura de cola, fragilidad por posicionamiento | II–III | MC-07 | ESTR, EMLA, EMEA, G10M | TMX-07 | P1 |
| 27. Carteras de factores, apuestas independientes y exposición agregada | Mínima varianza, Ledoit-Wolf, paridad de riesgo, HRP, `1/N`, número efectivo de apuestas, clústeres por factor dominante, exposición agregada por divisa y contradicciones entre segmentos | II | MC-07, MC-06 | ESTR; Analizador (9.6) | TMX-06 | P0 |
| 28. Optimización y decisión | Programación convexa, robusta, utilidad esperada, valor de la información (EVPI, EVSI), decisión bajo incertidumbre profunda | II–III | MC-07 | Todos (cálculo de apoyo; nunca carteras del usuario) | TMX-06 | P1 |

### Bloque VII · Valoración cambiaria, factores y opciones

| Área | Contenido operativo | Nivel | Módulo | Aplicación por segmento | TMX | Prior. |
|---|---|---|---|---|---|---|
| 29. Factores cambiarios | Carteras por prima forward, DOL y HML_FX (Lustig-Roussanov-Verdelhan), *dollar carry*, volatilidad global (Menkhoff et al.), momentum transversal y de serie temporal, valor, desequilibrios globales, *crowding* | II | MC-09 | ESTR; exposición de pares en todos | TMX-06 | P1 |
| 30. Opciones de divisas | Garman-Kohlhagen, griegas, volatilidad implícita, delta de contado y forward, ajuste por prima, ATM DNS/forward/contado, conversión delta–precio de ejercicio, tiempo y fechas de entrega | II | MC-09 | Todos con mercado de opciones; `VOLATILIDAD` | TMX-05 | P1 |
| 31. Sonrisa y superficie | RR y BF a 25 y 10 delta, *strangle* de mercado frente a sonrisa, Malz, Vanna-Volga, SABR, SVI, no arbitraje, estructura de plazos, volatilidad forward y de evento | II–III | MC-09 | Todos con mercado de opciones; transversal AG-21 | TMX-05 | P1 |
| 32. Densidades implícitas | Breeden-Litzenberger, momentos implícitos, probabilidades de umbral neutrales al riesgo frente a reales | II–III | MC-09 | G10N, G10M; EM con opciones líquidas | TMX-05 | P2 |
| 33. Prima de volatilidad cambiaria | Varianza implícita frente a realizada prevista y posterior, réplica de varianza, sección cruzada | II–III | MC-09, MC-02 | Todos; ESTR (volatilidad) | TMX-05, TMX-02 | P2 |
| 34. Mercados no entregables y controles | NDF y fijaciones, rendimientos implícitos *offshore*, brecha *onshore*–*offshore* (CNH–CNY), tipos oficiales frente a paralelos, convertibilidad para PS3 | II | MC-01, MC-09 | EMAS, EMLA, EMEA | TMX-03 | P1 |
| 35. Posicionamiento, flujos y microestructura | CFTC (TFF y heredado), normalización por interés abierto, percentiles, flujos de cartera y de cobertura, flujo de órdenes, fijaciones y su hora, liquidez horaria | II | MC-01 | Todos; transversal AG-21 | TMX-06 | P1 |

### Bloque VIII · Evaluación predictiva frente al paseo aleatorio y backtesting

| Área | Contenido operativo | Nivel | Módulo | Aplicación por segmento | TMX | Prior. |
|---|---|---|---|---|---|---|
| 36. Reglas de puntuación y verificación | Brier y Murphy, log-score, CRPS, pinball, puntuación de intervalo, BSS frente al paseo aleatorio y al forward, acierto direccional (Pesaran-Timmermann) | I–II | MC-10 | Todos (servicio al Evaluador; R13) | TMX-08 | P0 |
| 37. Calibración | Curvas de fiabilidad con bandas, ECE con su nulo, recalibración, PIT, cobertura, sobreconfianza | II | MC-10 | Todos | TMX-08 | P0 |
| 38. Comparación predictiva frente al paseo aleatorio y el forward | Meese-Rogoff y literatura posterior, U de Theil, Clark-West (anidados), Diebold-Mariano con HLN, Giacomini-White, prueba de fluctuación de Giacomini-Rossi, Model Confidence Set, Holm entre celdas | II | MC-10 | Todos (certificados y degradación, 12.2) | TMX-08 | P0 |
| 39. Backtesting cambiario sin sesgos | Datos *point-in-time* del mismo corte, desfase de ejecución, universo fechado y exclusiones de la CIP, costes de horquilla, subperiodos y regímenes, PSR, Deflated Sharpe, MinTRL, PBO, Reality Check, SPA | II | MC-10 | ESTR; reglas de todos los segmentos | TMX-08 | P0 |
| 40. Backtesting de medidas de riesgo | Kupiec, Christoffersen, semáforo de Basilea, pruebas de ES | II | MC-10 | Todos | TMX-08, TMX-07 | P1 |
| 41. Diseño muestral y resolución | n efectivo con solapamiento, efecto mínimo detectable, bootstrap estacionario por fechas, resolución con criterio congelado y misma fuente y corte, NO_RESOLUBLE, fiabilidad de fuentes con encogimiento | I–II | MC-10 | Todos (F4, F6; 12.5) | TMX-08 | P0 |

### Bloque IX · Datos, metodología y reproducibilidad

| Área | Contenido operativo | Nivel | Módulo | Aplicación por segmento | TMX | Prior. |
|---|---|---|---|---|---|---|
| 42. Calidad y validación de datos cambiarios | Sentido del par y escala del pip, fuente y corte horario, sincronización, festivos, *onshore*/*offshore*, oficial/paralelo, redenominaciones y devaluaciones, flash crashes frente a dedos gordos, conocibilidad, informe de calidad | I | STC-1 | Todos; críticos en EMAS, EMLA, EMEA | TMX-08 | P0 |
| 43. Datos oficiales, vintages y revisiones | Vintages de IPC, PIB, balanza de pagos y reservas; revisiones de pesos del BPI; desfases de publicación; CFTC fechado al martes y publicado el viernes | II | STC-1, MC-03 | Todos; transversal AG-09 | TMX-08 | P0 |
| 44. Muestreo y sesgos | Supervivencia de divisas (legadas del euro, pasos a tipo fijo, controles), selección de universo, anticipación, fisgoneo | I–II | MC-01 | ESTR; backtests de todos | TMX-08 | P0 |
| 45. Bibliometría y métricas de fuentes | Volúmenes, crecimiento, concentración, duplicados, cobertura de corpus | II | MC-01 | Transversal (F7–F9 vía Orquestador técnico, Evaluador y agentes de conocimiento) | TMX-08 | P1 |
| 46. Metodología científica | Hipótesis falsables, preregistro de criterios, replicación, sesgo de confirmación | I | STC-3, MC-08 | Todos | TMX-08 | P0 |
| 47. Computación numérica | Coma flotante, aritmética decimal, cancelación en puntos forward pequeños, condicionamiento, convergencia, determinismo | I | STC-2 | Todos | TMX-08 | P0 |
| 48. Validación matemática y computacional | Casos de control cambiarios (triangulación, CIP, Garman-Kohlhagen), identidades, segunda vía, regresión del catálogo | I–II | MC-08, MC-10 | Todos | TMX-08 | P0 |
| 49. Reproducibilidad y artefactos | Artefacto con convenciones, versionado de métodos y fichas, semillas, hashes, linaje, retención de 5 años | I | STC-3, STC-4 | Todos | TMX-08 | P0 |
| 50. Métricas, rankings y puntuaciones | Puntuaciones compuestas con anclas, redondeos, sensibilidad, reconstrucción de T/E/M/P/A con pesos FX y RK (idéntica a HT-03) | I–II | MC-01 | Todos (G3, PS8) | TMX-08 | P0 |

### Bloque X · Gobierno del servicio, seguridad y límites

| Área | Contenido operativo | Nivel | Módulo | Aplicación por segmento | TMX | Prior. |
|---|---|---|---|---|---|---|
| 51. Gobierno del servicio y contratos | CT-09 y CT-10: validación, convención (M17), plan proporcional, despacho, integración, idempotencia, estados de retorno | I | Orquestador de Cálculo | Todos | TMX-08 | P0 |
| 52. Seguridad y contenido externo | R8 y R9; datos que intentan dar instrucciones; indicios de manipulación de fijaciones como dato para PS7 | I | Orquestador de Cálculo (todos los módulos) | Todos | TMX-08 | P0 |
| 53. Eficiencia y valor informativo | Caché, reutilización de informes transversales, lotes por segmento, valor de la información, reglas de parada, presupuesto en UC | I | Orquestador de Cálculo, MC-07 | Todos | TMX-08 | P0 |
| 54. Gestión de la incertidumbre | Tipos (numérica, muestral, paramétrica, de modelo, de datos, de convención), propagación, declaración obligatoria | I | Todos (contraste en MC-08) | Todos | TMX-08 | P0 |
| 55. Auditoría cuantitativa y discrepancias | Re-ejecución aislada, tolerancias previas, categorías de discrepancia (con `CONVENCION_DISTINTA`), materialidad | I–II | MC-08 | Todos | TMX-08 | P0 |
| 56. Comunicación técnica y límites | Clase de cifra, unidades y convenciones, contado frente a total, advertencias obligatorias, probabilidades neutrales al riesgo, madurez, lo que el Motor no afirma | I | Orquestador de Cálculo | Todos | TMX-08 | P0 |

## 4. Distribución por módulo

| Módulo | Áreas de competencia | Fichas principales (Catálogo de cálculos del bloque, V1.0) |
|---|---|---|
| Orquestador de Cálculo | 51, 52, 53, 56 (y custodia de 54) | — (gobierno del servicio) |
| MC-01 Fundamentos cuantitativos y estadística | 1–6, 14, 34 (aritmética de NDF), 35, 44, 45, 50 | FX-CONV-001, FX-SETL-001, FX-FWD-001, FX-TR-001, FX-BASKET-001, FX-REER-001, FX-NDF-001, FX-POS-001, ST-DESC-001, ST-INF-001, FIN-CAGR-001, BIB-MET-001, SCORE-RK-001 |
| MC-02 Series temporales, tendencias, regímenes y volatilidad | 7–10, 33 (realizada, invitado) | FX-TREND-001, FX-BRK-001, FX-STL-001, FX-VOL-001, FX-REGIME-001, VOL-GARCH-001, REG-HMM-001 |
| MC-03 Econometría, causalidad y macroeconomía cuantitativa | 11–13, 15–17, 43 (vintages) | FX-CARRY-001, FX-CIP-001, FX-UIP-001, FX-PPP-001, FX-PPA-001 (deprecada), FX-BEER-001, FX-FEER-001, FX-RDIFF-001, FX-TOT-001, FX-TAYLOR-001, FX-SURP-001, FX-COINT-001, FX-CORR-001 |
| MC-04 Crecimiento, difusión y prospectiva cuantitativa | 18 | FX-PASS-001 |
| MC-05 Simulación estocástica y escenarios | 18 (con MC-04), 19, 20, 21 | SIM-MC-001, SCN-H-001, FX-PEG-001 |
| MC-06 Aprendizaje automático y predicción calibrada | 22, 23, 24, 27 (clústeres) | ML-CAL-001, ML-PRED-001, ML-CLUS-001 |
| MC-07 Optimización, decisión y riesgo | 25–28 | RISK-VAR-001, RISK-DD-001, FX-TAIL-001, DEC-VOI-001 |
| MC-08 Auditoría cuantitativa independiente | 46, 48, 54 (contraste), 55 | AUD-REX-001 |
| MC-09 Valoración y modelos de precios de activos | 15 (expectativas implícitas), 20 (opciones en regímenes), 29–34 | FX-FACT-001, FX-MOM-001, MON-EXP-001, FX-GK-001, FX-RR-001, FX-TERM-001, FX-VRP-001, FX-RND-001 |
| MC-10 Evaluación predictiva y backtesting | 36–41, 48 (validación predictiva) | FX-RW-001, FC-EVAL-001, FC-CAL-001, FX-BT-001, BT-DSR-001, BT-PBO-001, BT-VAR-001 |
| STC-1 a STC-4 | 42, 43, 47, 49 | (servicios deterministas; sin fichas propias) |

Ningún módulo es «de un segmento»: la aplicación por segmento la gobiernan los perfiles PERF-FX-G10, PERF-FX-EM y PERF-FX-FACT.

## 5. Aplicaciones por segmento (vista inversa)

| Segmento | Perfil | Áreas núcleo | Áreas de apoyo frecuentes |
|---|---|---|---|
| G10N | PERF-FX-G10 | 12, 15, 13 | 2, 6, 10, 14, 17, 30, 31, 35, 38 |
| G10M | PERF-FX-G10 | 16 (términos de intercambio), 12, 15 | 10, 13, 17, 26, 29, 35 |
| EMAS | PERF-FX-EM | 34, 13 (Balassa-Samuelson), 20 | 9, 12, 14, 16, 42 |
| EMLA | PERF-FX-EM | 12 (carry), 26, 34, 16 | 10 (asimetría), 13, 15, 25, 42 |
| EMEA | PERF-FX-EM | 13, 20, 15, 16 | 9, 12, 14, 25, 34, 42 |
| ESTR | PERF-FX-FACT | 29, 26, 39 | 8, 9, 14, 17, 27, 33, 44 |
| Transversales AG-09 / AG-21 | Del segmento; PERF-FX-FACT global | AG-09: 15, 11, 9; AG-21: 35, 10, 31, 33, 12 (base) | 4, 17 |

## 6. Correspondencia con la taxonomía de F8 (TMX-01 a TMX-09)

| Temática F8 (Anexo D) | Áreas | Fichas cuyo respaldo mantiene |
|---|---|---|
| TMX-01 Series temporales de tipos de cambio: raíces unitarias, cointegración, no linealidad y cambios de régimen | 7, 8, 9, 11, 21 | FX-TREND-001, FX-BRK-001, FX-STL-001, FX-REGIME-001, REG-HMM-001, FX-COINT-001, FX-RDIFF-001, FX-SURP-001 |
| TMX-02 Volatilidad cambiaria: GARCH, volatilidad realizada y alta frecuencia | 10, 33 | FX-VOL-001, VOL-GARCH-001, FX-VRP-001 |
| TMX-03 Paridades y cálculo cambiario: CIP, puntos forward, base cruzada y convenciones | 2, 6, 12, 34 | FX-CONV-001, FX-SETL-001, FX-FWD-001, FX-TR-001, FX-CARRY-001, FX-CIP-001, FX-UIP-001, FX-NDF-001, FX-BASKET-001, MON-EXP-001, FIN-CAGR-001 |
| TMX-04 Modelos cuantitativos de equilibrio y valoración | 13, 14, 15, 16, 18 | FX-PPP-001, FX-PPA-001, FX-BEER-001, FX-FEER-001, FX-REER-001, FX-TOT-001, FX-TAYLOR-001, FX-PASS-001, SCN-H-001 |
| TMX-05 Opciones de divisas: Garman-Kohlhagen, superficie de volatilidad, *risk reversals* y densidades implícitas | 30, 31, 32, 33 | FX-GK-001, FX-RR-001, FX-TERM-001, FX-RND-001, FX-VRP-001 |
| TMX-06 Factores cambiarios y construcción de carteras | 14, 17, 27, 28, 29, 35 | FX-FACT-001, FX-MOM-001, FX-POS-001, FX-CORR-001, ML-CLUS-001, FX-BT-001 |
| TMX-07 Riesgo de cola, saltos y valores extremos en divisas | 3, 19, 20, 25, 26 | FX-TAIL-001, FX-PEG-001, RISK-VAR-001, RISK-DD-001, SIM-MC-001, BT-VAR-001 |
| TMX-08 Evaluación predictiva frente al paseo aleatorio y backtesting cambiario | 36–41; por convención, respaldo transversal de 1, 4, 5, 42–56 | FX-RW-001, FC-EVAL-001, FC-CAL-001, BT-DSR-001, BT-PBO-001, FX-BT-001, ML-CAL-001; ST-DESC-001, ST-INF-001, SCORE-RK-001, AUD-REX-001, BIB-MET-001, DEC-VOI-001 |
| TMX-09 Aprendizaje automático y análisis de texto para divisas | 22, 23, 24 | ML-PRED-001, ML-CAL-001, ML-CLUS-001 |

**Laguna de taxonomía.** El Anexo D del Documento 0 no prevé una temática TMX para estadística general, calidad de datos, computación numérica y reproducibilidad (áreas 1, 4, 5, 42–56). Por convención de este mapa, su respaldo bibliográfico se aloja en TMX-08 como «respaldo transversal». Una temática propia exigiría un cambio de tipo 3 del Anexo D; el Motor la propondrá si el volumen de referencias transversales en TMX-08 dificulta su mantenimiento.

El Documentador para el Motor mantiene en F8, para cada temática, al menos las referencias canónicas citadas en las fichas del Catálogo y en los prompts de los módulos, ordenadas por calidad Q.

## 7. Prioridades de implantación

| Prioridad | Áreas | Criterio |
|---|---|---|
| **P0** | 1–12, 15, 17–19, 23, 25, 27, 36–39, 41–44, 46–56 | Sin ellas el bloque no puede calcular con convención explícita y trazabilidad (R7), validar (G3), compararse con el paseo aleatorio y certificar horizontes (R13) ni aprender (sección 12 del Documento 0) |
| **P1** | 13, 14, 16, 20, 22, 26, 28–31, 34, 35, 40, 45 | Métodos cambiarios con datos accesibles; habilitan las dimensiones de A (valoración y desviación del equilibrio, carry, momento y posicionamiento, convertibilidad) |
| **P2** | 21, 24, 32, 33 | Datos especializados, uso ocasional o madurez metodológica baja |

Orden de implantación recomendado: P0 completo, empezando por las fichas de convención y rentabilidad total (FX-CONV-001, FX-SETL-001, FX-FWD-001, FX-TR-001) y por FX-RW-001 → fichas P1 que alimentan las dimensiones de A en los seis segmentos (FX-CARRY-001 v2.0, FX-PPP-001, FX-REER-001, FX-POS-001, FX-MOM-001, FX-NDF-001, FX-FACT-001, FX-RR-001) → P2 bajo demanda acreditada por el Registro de cálculos.

## 8. Metaespecialización: cuándo no calcular

El Motor debe saber reconocer cuándo un cálculo no procede, y decirlo:

1. **El cálculo no puede cambiar la decisión** (DEC-VOI-001; R15): no se ejecuta.
2. **El horizonte es «No» para el segmento** (8.3 del Documento 0: ESTR en H1) o «Limitado» sin liquidez ni catalizador declarados: se rechaza la previsión.
3. **Datos por debajo del mínimo de la ficha o del perfil**: se rechaza o se sirve con limitación; nunca se rellena.
4. **El método pertenece a otro régimen o perfil** (R21): BEER o PPA de flotación aplicados a un tipo fijo; GARCH como medida de riesgo de un régimen gestionado; carry *onshore* de una divisa no convertible.
5. **Convención ambigua**: par invertido, medida (contado o total) no declarada, cesta sin pesos o sin divisa de financiación, cortes horarios mezclados.
6. **Probabilidades neutrales al riesgo** (densidades implícitas, ruptura de tipos fijos) pedidas como probabilidades reales.
7. **La UIP o el forward pedidos como pronóstico del bloque**: son referencias ingenuas, no previsiones.
8. **Muestra de evaluación insuficiente** (< 30 por celda): solo descriptivos; certificado solo con ≥ 100.
9. **Incertidumbre profunda**: escenarios sin probabilidades.
10. **La petición pretende elegir o comparar instrumentos**, proveedores, costes de ejecución o niveles de entrada (frontera con el Bloque B): `FUERA_DE_CATALOGO` con la ficha de ámbito más próxima.

## 9. Pruebas de competencia del servicio

Batería en `09_Pruebas`, con al menos: una misma noticia (p. ej., una subida de la Fed) con implicaciones distintas para G10N, G10M, EMAS, EMLA, EMEA y ESTR; un par que cruza segmentos con su asignación; un cruce sintético con patas de cortes distintos rechazado; fechas valor de USD/CAD y de un par con festivo local; carry por puntos frente a carry por OIS con la base declarada; una PPA con dos bases y su banda; un régimen gestionado tratado con métodos de flotación detectado; una petición de comparar instrumentos rechazada; un cálculo sin valor informativo que el Motor no ejecuta; una re-ejecución CT-10 con discrepancia de convención (base de días); una evaluación con fuga detectada (CFTC usado antes del viernes); una certificación en el límite (n = 100) en la que el Motor informa del BSS frente al paseo aleatorio con su IC y del ECE nulo. Ningún área ni ficha se declara validada sin evidencia registrada (R22).

## 10. Lo que el Motor no asume

La interpretación económica y la decisión son del solicitante; la selección y verificación de fuentes, de los agentes de conocimiento; la auditoría de agentes, del circuito Orquestador técnico–Auditor; la certificación de horizontes y la recalibración, del Evaluador; la elección del instrumento, del proveedor, del coste, del apalancamiento, del tamaño y del nivel de entrada, del Bloque B; la decisión de inversión, del Broker Personal. El Motor no gestiona carteras del usuario ni recomienda: entrega cálculos reproducibles, con su convención y sus límites, comparados con el paseo aleatorio.
