# Mapa de conocimientos — Motor de Cálculo Avanzado (AG-13)

**Bloque A · Robot Investor · Versión óptima V5.0 · 02/11/2026** · Subordinado al Documento 0 óptima V5.0.

Archivo CC (propietario: operador, tipo 3; el Motor propone). Lectores: AG-13 y sus módulos, AG-15 (Documentador para el Motor), Analistas de tipo de activo (AG-03 a AG-09 y AG-21 a AG-25), Orquestador técnico, Auditor, Evaluador. «Tipo de activo» y «clase de activo» son sinónimos (2.6 del Documento 0).

---

## 1. Propósito y uso

1.1. Este mapa enumera **todas** las áreas de conocimiento que el Motor debe dominar, con su nivel, su módulo responsable, su aplicación por tipo de activo (los doce tipos de 2.6 del Documento 0) y su prioridad. Es autosuficiente: no remite a versiones anteriores.

1.2. **Usos gobernados**: (a) **enrutado**: el Orquestador de Cálculo sitúa cada petición CT-09 en su área, su módulo y su perfil; (b) **selección de métodos**: a igual precisión exigida, se prefiere el área y el método de nivel más bajo (I antes que II, II antes que III); (c) **rechazo con orientación**: una petición fuera de cobertura se rechaza indicando el área más próxima; (d) **ampliación**: propuestas de fichas, perfiles y módulos (tipo 3); (e) **mantenimiento del conocimiento**: el Documentador para el Motor (AG-15) organiza F8 por las temáticas TM- y vigila la literatura de cada área (sección 5).

1.3. **Niveles de dominio**:

| Nivel | Significado | Activación |
|---|---|---|
| I · Fundamentación | Imprescindible; usado a diario por cualquier módulo | Siempre disponible |
| II · Especialización avanzada | Métodos especializados de uso frecuente en uno o varios tipos de activo | Bajo demanda, con ficha |
| III · Especialización condicionada | Métodos de uso ocasional, coste alto o riesgo de mal uso | Solo con petición explícita, ficha vigente y justificación en el plan |

1.4. **Prioridades de implantación**: **P0** núcleo transversal imprescindible (incluye lo que exigen R7, R13, G3 y la reproducibilidad); **P1** conocimiento propio de un tipo de activo con datos accesibles y uso frecuente; **P2** ampliación (datos especializados, uso ocasional o madurez metodológica baja).

1.5. **Cobertura no es obligación** (R15): ninguna investigación activa todas las áreas; el valor de la información decide. **Madurez** (R22): todas las áreas están **documentadas**; la implementación y validación de cada método constan en su ficha del Catálogo de cálculos (V5.0).

1.6. **Frontera con el Bloque B** (2.5 del Documento 0): las áreas se aplican a **ámbitos** (mercados, índices, sectores, segmentos, categorías, curvas, factores) y a sus indicadores de seguimiento. Ningún área habilita al Motor para comparar o seleccionar instrumentos concretos ni sus costes, comisiones o plataformas.

## 2. Bloques temáticos

| Bloque | Áreas | Módulos | Temáticas F8 | Prioridad dominante |
|---|---|---|---|---|
| I. Fundamentos matemáticos y estadísticos | 1–5 | MC-01 | TM-01 | P0 |
| II. Series temporales, tendencias, relaciones y dinámica | 6–10 | MC-02, MC-03, MC-04 | TM-02, TM-03, TM-04, TM-12 | P0 |
| III. Causalidad, sistemas, prospectiva y simulación | 11–15 | MC-03, MC-04, MC-05 | TM-04, TM-09, TM-12 | P0 |
| IV. Aprendizaje automático y modelización predictiva | 16–18 | MC-06, MC-03 | TM-07, TM-10 | P0/P1 |
| V. Economía, mercados y estructura de las tendencias | 19–23 | MC-03, MC-04, MC-01 | TM-04, TM-12 | P0/P1 |
| VI. Riesgo, optimización y decisión | 24–25 | MC-07 | TM-08 | P0 |
| VII. Datos, calidad y metodología científica | 26–29 | STC-1, MC-01, STC-3, MC-08 | TM-14 | P0 |
| VIII. Computación científica y reproducibilidad | 30–32 | STC-2, STC-4, MC-08, MC-10 | TM-09, TM-14 | P0 |
| IX. Conocimientos transversales de especialización | 33–37 | MC-01, MC-06, MC-07, STC-1 | TM-01, TM-14 | P0/P1/P2 |
| X. Gobierno del servicio, seguridad y límites | 38–43 | Orquestador de Cálculo, MC-08 | TM-14 | P0 |
| XI. Valoración y modelos de precios de activos | 44–50 | MC-09 | TM-05, TM-06, TM-07 | P1 |
| XII. Métricas y valoración específicas por tipo de activo | 51–57, 64–68 | MC-09, MC-01, MC-02, MC-03, MC-04 | TM-13, TM-05, TM-06 | P1/P2 |
| XIII. Evaluación predictiva y backtesting | 58–63 | MC-10 | TM-11 | P0 |

## 3. Inventario completo de áreas

Abreviaturas de tipo de activo (2.6 del Documento 0): RV, RF, DIV, MP, IDX, FON, DER, INM, CRI, ALT, MON, TCV; «Todas» = transversal. Las áreas 64–68 se numeran a continuación de la 63 para no alterar las referencias existentes, aunque pertenecen al bloque XII.

### Bloque I · Fundamentos matemáticos y estadísticos

| Área | Contenido operativo | Nivel | Módulo | Aplicación por tipo de activo | Prior. |
|---|---|---|---|---|---|
| 1. Matemáticas aplicadas y álgebra | Álgebra lineal (matrices, autovalores, descomposiciones de Cholesky y espectral, número de condición), cálculo, interpolación, raíces (Newton, Brent), optimización elemental | I | MC-01 | Todas (covarianzas, curvas, TIR) | P0 |
| 2. Cálculo financiero y crecimiento | Interés compuesto y continuo, valor actual y futuro, anualidades, TIR y TIR múltiples, CAGR, nominal/real, efecto base, rentabilidad aritmética frente a geométrica | I | MC-01 | Todas | P0 |
| 3. Probabilidad | Distribuciones (normal, t, lognormal, Pareto, binomial, Poisson, beta), momentos, colas, teoremas límite, probabilidad condicionada y Bayes, cópulas básicas | I | MC-01 | Todas; colas pesadas en CRI, MP, HY | P0 |
| 4. Estadística descriptiva y exploratoria | Localización, dispersión robusta, asimetría y curtosis, cuantiles (tipos de Hyndman-Fan), atípicos, visualización exploratoria | I | MC-01 | Todas | P0 |
| 5. Inferencia y diseño | Contrastes paramétricos y no paramétricos, IC, potencia y tamaño muestral, bootstrap, comparaciones múltiples (Holm, BH), errores HAC | I | MC-01 | Todas | P0 |

### Bloque II · Series temporales, tendencias, relaciones y dinámica

| Área | Contenido operativo | Nivel | Módulo | Aplicación por tipo de activo | Prior. |
|---|---|---|---|---|---|
| 6. Análisis de series temporales y volatilidad | Estacionariedad (ADF, KPSS), ARIMA, suavizado exponencial, espacio de estados y filtro de Kalman, STL, volatilidad realizada, EWMA, GARCH/GJR/EGARCH, volatilidad realizada de alta frecuencia | I–II | MC-02 | Todas; volatilidad central en DIV, MP, CRI; estacionalidad en MP, INM | P0 |
| 7. Detección y medición de tendencias | Mann-Kendall, Theil-Sen, filtros (Hodrick-Prescott con advertencias, Hamilton), medias móviles, momentum de series temporales, aceleración | I–II | MC-02 | Todas | P0 |
| 8. Econometría y relaciones económicas | MCO y diagnósticos, MCG, variables instrumentales, paneles (efectos fijos y aleatorios), cointegración (Engle-Granger, Johansen, DOLS), VAR y VECM, causalidad de Granger | II | MC-03 | Todas; paridades en DIV; equilibrio en DIV y MP | P0 |
| 9. Crecimiento, difusión y adopción | Logística, Gompertz, Bass, curvas de aprendizaje (ley de Wright), curvas S de tecnología, saturación | II | MC-04 | PERF-TEM sobre RV, MP, INM, CRI | P1 |
| 10. Regímenes, ciclos y rupturas | Markov switching, HMM multivariante, Bai-Perron, CUSUM, datación de ciclos (Bry-Boschan), análisis espectral básico | II–III | MC-02 | Todas (régimen del tipo de activo, paso 1 del marco común) | P0 |

### Bloque III · Causalidad, sistemas, prospectiva y simulación

| Área | Contenido operativo | Nivel | Módulo | Aplicación por tipo de activo | Prior. |
|---|---|---|---|---|---|
| 11. Inferencia causal | Grafos causales, diferencias en diferencias, control sintético, regresión discontinua, estudios de eventos (rentabilidades anormales acumuladas), identificación declarada | II–III | MC-03 | Todas; estudios de eventos en RV, RF, DIV | P1 |
| 12. Sistemas dinámicos y complejidad | Retroalimentación, dinámica de sistemas, modelos de stock y flujo, no linealidad, umbrales | II–III | MC-04 | MP (ciclos de inversión), INM (ciclo de construcción), CRI (adopción) | P2 |
| 13. Prospectiva cuantitativa y escenarios | Escenarios consistentes, árboles de escenarios, análisis morfológico cuantificado, señales tempranas, bloques de rentabilidad esperada a largo plazo | II | MC-04, MC-05 | Todas (servicio a Prospectiva, CT-12) | P0 |
| 14. Simulación y Monte Carlo | Generadores y semillas, reducción de varianza, bootstrap (iid, por bloques, estacionario, filtrado), cuasi-Monte Carlo, cópulas, error de Monte Carlo y convergencia | II | MC-05 | Todas | P0 |
| 15. Teoría de la información y señales | Entropía, información mutua, relación señal/ruido, filtrado, detección de cambios en flujos de datos | II–III | MC-05 | Todas (soporte) | P2 |

### Bloque IV · Aprendizaje automático y modelización predictiva

| Área | Contenido operativo | Nivel | Módulo | Aplicación por tipo de activo | Prior. |
|---|---|---|---|---|---|
| 16. Aprendizaje automático estadístico | Regularización (Ridge, Lasso, Elastic Net), logística, árboles y ensambles, k-vecinos, PCA, agrupación, anomalías, interpretabilidad (permutación, SHAP); redes profundas solo condicionadas | II (III las profundas) | MC-06 | Todas; clústeres de exposición para el Analizador | P1 |
| 17. Predicción, calibración e incertidumbre | Validación temporal (walk-forward, purga, embargo), calibración (Platt, isotónica), conformal, cuantiles, combinación de previsiones, deriva | II | MC-06 (con MC-10) | Todas | P0 |
| 18. Análisis multivariante y dependencia | Correlación (Pearson, Spearman, Kendall), correlación dinámica (DCC), dependencia de cola, matrices aleatorias (Marchenko-Pastur), encogimiento de covarianzas | II | MC-03 | Todas; apuestas independientes y coherencia entre tipos de activo | P0 |

### Bloque V · Economía, mercados y estructura de las tendencias

| Área | Contenido operativo | Nivel | Módulo | Aplicación por tipo de activo | Prior. |
|---|---|---|---|---|---|
| 19. Macroeconomía cuantitativa | Ciclo, brecha de producción, curva de Phillips, reglas de Taylor, condiciones financieras, sorpresas macro, expectativas de inflación, balanza de pagos | II | MC-03 | Todas (capa macro); RF y DIV en especial | P0 |
| 20. Economía industrial y cadenas de valor | Concentración (HHI), poder de mercado, márgenes por eslabón, capacidad, cuellos de botella | II–III | MC-04 | RV (sectores, temáticas), MP | P2 |
| 21. Innovación y tecnología | Patentes e I+D como indicadores, madurez tecnológica, costes unitarios, sustitución tecnológica | II–III | MC-04 | PERF-TEM | P2 |
| 22. Energía, recursos y materiales | Balances de oferta y demanda, curvas de costes, intensidades, transición energética | II–III | MC-04 | MP, INM (infraestructuras), RV (energía) | P1 |
| 23. Indicadores e índices compuestos | Construcción, normalización, ponderación, sensibilidad, números índice (Laspeyres, Paasche, Fisher), encadenamiento | I–II | MC-01 | Todas | P0 |

### Bloque VI · Riesgo, optimización y decisión

| Área | Contenido operativo | Nivel | Módulo | Aplicación por tipo de activo | Prior. |
|---|---|---|---|---|---|
| 24. Optimización y teoría de la decisión | Programación lineal, cuadrática, convexa, entera; KKT; métodos globales; robusta; multiobjetivo; utilidad esperada; valor de la información (EVPI, EVSI); decisión bajo incertidumbre profunda | II–III | MC-07 | Todas (cálculo de apoyo; nunca carteras del usuario) | P0 |
| 25. Riesgo y eventos extremos | Volatilidad, VaR, ES, EVT (POT, Hill, GEV), drawdown, liquidez (LVaR), estrés histórico, hipotético e inverso, contribución al riesgo, escala de riesgo 1–5 | II–III | MC-07 | Todas; colas extremas en CRI, MP, HY | P0 |

### Bloque VII · Datos, calidad y metodología científica

| Área | Contenido operativo | Nivel | Módulo | Aplicación por tipo de activo | Prior. |
|---|---|---|---|---|---|
| 26. Calidad y validación de datos | Esquemas, unidades, huecos, atípicos, alineación de calendarios y husos, ajustes corporativos, conocibilidad (`conocible_desde`), informe de calidad | I | STC-1 | Todas; UTC en CRI; valoraciones infrecuentes en ALT, INM | P0 |
| 27. Muestreo, sesgos y representatividad | Supervivencia, selección, relleno retrospectivo, sesgo de anticipación, representatividad de bases privadas | I–II | MC-01 | Todas; críticos en ALT y en backtests | P0 |
| 28. Bibliometría y métricas de fuentes | Volúmenes, crecimiento, concentración, duplicados, cobertura de corpus | II | MC-01 | Transversal (F7–F9 vía Orquestador técnico y Evaluador) | P1 |
| 29. Metodología científica | Formulación de hipótesis falsables, preregistro de criterios, replicación, sesgo de confirmación en el análisis cuantitativo | I | STC-3, MC-08 | Todas | P0 |

### Bloque VIII · Computación científica y reproducibilidad

| Área | Contenido operativo | Nivel | Módulo | Aplicación por tipo de activo | Prior. |
|---|---|---|---|---|---|
| 30. Computación numérica | Coma flotante, aritmética decimal, estabilidad, condicionamiento, convergencia, tolerancias, paralelismo y determinismo | I | STC-2 | Todas | P0 |
| 31. Validación matemática, computacional y estadística | Casos de control, identidades, segunda vía, pruebas de regresión, validación fuera de muestra | I–II | MC-08, MC-10 | Todas | P0 |
| 32. Reproducibilidad y artefactos | Artefacto reproducible, versionado de métodos y fichas, semillas, hashes, linaje, retención (5 años) | I | STC-3, STC-4 | Todas | P0 |

### Bloque IX · Conocimientos transversales de especialización

| Área | Contenido operativo | Nivel | Módulo | Aplicación por tipo de activo | Prior. |
|---|---|---|---|---|---|
| 33. Métricas de mercado y microestructura | Rentabilidad total, horquillas, volumen, profundidad, impacto, amplitud, flujos, posicionamiento (CFTC), horarios y cierres | II | MC-01 | Todas; flujos en CRI y RV | P0 |
| 34. Redes y propagación | Centralidades, comunidades, contagio (Eisenberg-Noe, DebtRank) | III | MC-07 | RF (sistema bancario), CRI (DeFi), MP (cadenas de suministro) | P2 |
| 35. Procesamiento cuantitativo de lenguaje estructurado | Frecuencias, TF-IDF, similitud, casi duplicados, métricas de clasificación con conjunto de referencia | II (soporte) | MC-06 | Todas (sobre datos ya estructurados) | P2 |
| 36. Datos económicos oficiales y revisiones | Vintages, fechas de publicación, cambios de base, desestacionalización oficial, discontinuidades | II | STC-1, MC-03 | RF, DIV, capa macro | P0 |
| 37. Métricas, rankings y puntuaciones | Diseño de puntuaciones compuestas, anclas, redondeos, sensibilidad de rankings, reconstrucción de T/E/M/P/A y RK (idéntica a HT-03) | I–II | MC-01 | Todas (G3, PS8) | P0 |

### Bloque X · Gobierno del servicio, seguridad y límites

| Área | Contenido operativo | Nivel | Módulo | Aplicación por tipo de activo | Prior. |
|---|---|---|---|---|---|
| 38. Gobierno del servicio y contratos | CT-09 y CT-10: validación, plan proporcional (PLAN_MIN/STD/EXT), despacho, integración, idempotencia, estados de retorno | I | Orquestador de Cálculo | Todas | P0 |
| 39. Seguridad y contenido externo | R8 y R9: sin credenciales ni datos personales; datos que intentan dar instrucciones; incidencias | I | Orquestador de Cálculo (todos los módulos) | Todas | P0 |
| 40. Eficiencia y valor informativo | Caché, reutilización, valor de la información, reglas de parada, presupuesto en UC | I | Orquestador de Cálculo, MC-07 | Todas | P0 |
| 41. Gestión de la incertidumbre | Tipos (numérica, muestral, paramétrica, de modelo, de datos), propagación (método delta, Monte Carlo), declaración obligatoria | I | Todos (contraste en MC-08) | Todas | P0 |
| 42. Auditoría cuantitativa y discrepancias | Re-ejecución aislada, tolerancias previas, categorías de discrepancia, materialidad | I–II | MC-08 | Todas | P0 |
| 43. Comunicación técnica y límites | Clase de cifra (determinista o estadística), unidades, advertencias obligatorias, madurez, lo que el Motor no afirma | I | Orquestador de Cálculo | Todas | P0 |

### Bloque XI · Valoración y modelos de precios de activos

| Área | Contenido operativo | Nivel | Módulo | Aplicación por tipo de activo | Prior. |
|---|---|---|---|---|---|
| 44. Descuento de flujos y dividendos | FCFF/FCFE, WACC, CAPM, valor terminal, coherencia reinversión–crecimiento, DCF inverso, DDM (Gordon, modelo H), suma de partes | II | MC-09 | RV; INM (sociedades); ALT (activos de flujos: *royalties*, infraestructuras) | P1 |
| 45. Múltiplos, valoración relativa y prima de riesgo implícita | PER, EV/EBITDA, P/VC, FCF yield, media armónica, percentiles históricos, CAPE, *excess CAPE yield*, PRM implícita (Damodaran) | II | MC-09 | RV; INM (P/FFO); CRI (P/comisiones) | P1 |
| 46. Renta fija: precio, rendimiento y sensibilidades | Precio limpio y sucio, convenciones, YTM/YTW, duraciones (Macaulay, modificada, efectiva), DV01, convexidad, ligados a inflación y breakevens | I–II | MC-09 | RF; TCV (breakevens); INM (deuda) | P1 |
| 47. Estructura temporal de tipos | *Bootstrapping*, *forwards*, Nelson-Siegel-Svensson, Diebold-Li, prima temporal (ACM, Kim-Wright), pendientes y recesiones, carry y rolldown | II | MC-09 | RF; TCV (pendiente, prima por plazo); MON (curva monetaria); DIV (diferenciales de curvas); INM (descuento) | P1 |
| 48. Riesgo de crédito y diferenciales | G/I/Z-spread, OAS, triángulo de crédito, tasas de impago y recuperación, Merton y distancia al impago, rompecabezas del diferencial | II–III | MC-09 | RF; TCV (índices CDS); ALT (deuda privada); RV (riesgo de quiebra sectorial) | P1 |
| 49. Derivados, opciones y volatilidad implícita | BSM, Black-76, binomial CRR, griegas, volatilidad implícita, sonrisa y sesgo, densidad neutral al riesgo, prima de riesgo de varianza, financiación y base de futuros | II | MC-09 | DER (PERF-DER); TCV (volatilidad como factor); lectura del subyacente en RV, IDX, RF, DIV, MP, CRI | P1 |
| 50. Modelos factoriales, primas de riesgo y momentum | CAPM, Fama-French, Carhart, calidad, baja volatilidad, Fama-MacBeth, Newey-West, zoológico de factores, momentum transversal y de series temporales, valor y momentum en todos los tipos de activo | II | MC-09 | RV; IDX (valor y momentum entre índices); ALT y FON (estrategias); DIV, RF, MP (TSMOM, carry, valor) | P1 |

### Bloque XII · Métricas y valoración específicas por tipo de activo

| Área | Contenido operativo | Nivel | Módulo | Aplicación por tipo de activo | Prior. |
|---|---|---|---|---|---|
| 51. Divisas: paridades, carry y equilibrio | Paridad cubierta y descubierta, rompecabezas de la prima a plazo, PPA y vida media, tipo real efectivo, BEER/FEER, carry/volatilidad, momentum cambiario, colapsos del carry | II | MC-03, MC-09 | DIV; RF (cobertura de divisa) | P1 |
| 52. Materias primas: curvas, almacenamiento e inventarios | Coste de acarreo, *convenience yield*, teoría del almacenamiento, contango y *backwardation*, roll yield, descomposición de rentabilidad de futuros, inventarios frente a estacional, precio real y coste marginal, superciclos | II | MC-09, MC-02 | MP | P1 |
| 53. Inmobiliario e infraestructuras | Cap rate y relación de Gordon, diferencial cap rate–bono, NAV (EPRA), prima/descuento, FFO/AFFO, LTV, ICR, refinanciación, tasaciones y su retraso | II | MC-09 | INM; ALT (infraestructuras privadas) | P1 |
| 54. Criptoactivos | Capitalización realizada, MVRV, NVT, comisiones y rendimiento real de *staking*, tokenómica y desbloqueos, financiación y base, flujos de ETF y stablecoins, riesgos de protocolo y desanclaje | II–III | MC-09, MC-02 | CRI | P1 (mercado) / P2 (en cadena) |
| 55. Mercados privados y alternativos | TIR, TVPI, DPI, PME (KS, alfa directo), curva J, cosechas, Takahashi-Alexander, desuavizado (Geltner, Getmansky-Lo-Makarov), factores de Fung-Hsieh, índices de transacciones (ventas repetidas, hedónicos), sesgos de bases de datos | II–III | MC-09 | ALT; INM (directo) | P2 (desuavizado P1) |
| 56. Vehículos de inversión colectiva: estructura | Prima/descuento sobre NAV, diferencia y error de seguimiento agregados por categoría, métodos de replicación, apalancados e inversos y erosión por volatilidad, contraparte en sintéticos, liquidez primaria y secundaria de la categoría (siempre como categoría, nunca como comparación de productos) | II | MC-01, MC-09 | FON (PERF-ETF); ALT y INM (vehículos cotizados del activo) | P1 |
| 57. Sostenibilidad y clima cuantitativos | Intensidad de carbono, alcances 1–3, escenarios de transición, precio del carbono, riesgo físico, calidad de datos ESG | II–III | MC-03, MC-04 | Todas (capa PERF-ESG); MP (carbono) | P2 |
| 64. Índices bursátiles: valoración, estructura y eventos | Rentabilidad esperada por bloques (Grinold-Kroner: rentabilidad por dividendo, recompras netas, crecimiento real, inflación, cambio de valoración), CAPE y prima por región, valor relativo entre índices con ajuste neutral sectorial, concentración (HHI, número efectivo, peso de los mayores), amplitud, efectos de rebalanceo e inclusión (estudios de eventos, demanda indexada) | II | MC-09, MC-01, MC-03 | IDX; RV (agregados sectoriales) | P1 |
| 65. Vehículos como fuente de oportunidad | Descuentos de fondos cerrados y su reversión (sentimiento, liquidez, comisiones), flujos por categoría y su persistencia, estrategias de gestión por régimen, estructuras nuevas (ELTIF, ETF activos, ETF con vencimiento), decaimiento de apalancados por régimen de volatilidad | II | MC-09, MC-02, MC-01 | FON; ALT (vehículos cotizados de privados) | P1 |
| 66. Derivados como fuente de oportunidad | Prima de varianza (réplica libre de modelo, HAR-RV), sesgo y mariposa, estructura de plazos y volatilidad *forward*, movimiento descontado de eventos, carry y roll de futuros financieros (base, dividendos y repo implícitos), primas de estrategias de opciones (venta cubierta, protección) | II–III | MC-09, MC-02 | DER; TCV (volatilidad); DIV (*risk reversals*) | P1 |
| 67. Mercado monetario y liquidez | Convenciones (descuento, rendimiento equivalente, *money market yield*, Act/360 y Act/365, TAE), segmentos monetarios y sus diferenciales, comparación cubierta entre divisas, curva OIS y expectativas implícitas por reunión, ajuste de convexidad de futuros a corto, tipo real a corto, valor de fijar plazo frente a renovar | I–II | MC-01, MC-09 | MON; DIV (tipos a corto); RF (tramo corto) | P1 |
| 68. Tipos, crédito y volatilidad como factores | Pendiente y su valor razonable, prima por plazo (ACM, Kim-Wright, encuestas), breakevens y 5y5y frente a inflación esperada y primas de liquidez, índices CDS frente a pérdidas esperadas y base CDS–contado, índices de volatilidad y estructura de plazos de sus futuros, exposiciones neutrales en duración | II–III | MC-09, MC-03, MC-02 | TCV; RF (contexto); MON (prima a corto) | P1 |

### Bloque XIII · Evaluación predictiva y backtesting

| Área | Contenido operativo | Nivel | Módulo | Aplicación por tipo de activo | Prior. |
|---|---|---|---|---|---|
| 58. Reglas de puntuación y verificación de pronósticos | Reglas propias, Brier y descomposición de Murphy, log-score, RPS, CRPS, pinball, puntuación de intervalos, BSS, acierto direccional (binomial, Pesaran-Timmermann) | I–II | MC-10 | Todas (servicio al Evaluador; R13) | P0 |
| 59. Calibración y fiabilidad | Curvas de fiabilidad con bandas de consistencia, ECE con su nulo, recalibración logística, PIT, cobertura, sobreconfianza | II | MC-10 | Todas | P0 |
| 60. Comparación predictiva y comparaciones múltiples | Diebold-Mariano con HLN, Clark-West, Giacomini-White, Reality Check, SPA, Model Confidence Set, Holm, BH | II | MC-10 | Todas (12.2: degradación de horizontes) | P0 |
| 61. Backtesting sin sesgos y sobreajuste | Datos a fecha, ejecución sin anticipación, costes, purga y embargo, Sharpe y su error, PSR, Deflated Sharpe, MinTRL, PBO/CSCV | II | MC-10 | Todas | P0 |
| 62. Backtesting de medidas de riesgo | Kupiec, Christoffersen, semáforo de Basilea, pruebas de ES | II | MC-10 | Todas | P1 |
| 63. Diseño muestral, potencia y resolución | n efectivo con solapamiento, efecto mínimo detectable, bootstrap estacionario por fechas, resolución de pronósticos con criterio congelado y sin anticipación, NO_RESOLUBLE, fiabilidad de fuentes con encogimiento | I–II | MC-10 | Todas (F4, F6; 12.5) | P0 |

## 4. Distribución por módulo

| Módulo | Áreas de competencia | Fichas principales (Catálogo de cálculos V5.0) |
|---|---|---|
| Orquestador de Cálculo | 38, 39, 40, 43 (y custodia de 41) | — (gobierno del servicio) |
| MC-01 Fundamentos cuantitativos | 1–5, 23, 27, 28, 33, 37, 56 (parte), 64 (concentración), 67 (convenciones y tipos reales) | ST-DESC-001, ST-INF-001, FIN-CAGR-001, BIB-MET-001, SCORE-RK-001, IDX-CONC-001, FON-TD-001, MON-YLD-001, MON-REAL-001 |
| MC-02 Series temporales, regímenes y volatilidad | 6, 7, 10, 52 (inventarios), 54 (flujos), 65 (flujos por categoría), 66 y 68 (volatilidad realizada, como módulo invitado) | FX-TREND-001, FX-BRK-001, FX-STL-001, FX-VOL-001, FX-REGIME-001, VOL-GARCH-001, REG-HMM-001, CMD-INV-001, CHR-FLOW-001, FON-FLOW-001 |
| MC-03 Econometría, causalidad y macro | 8, 11, 18, 19, 36, 51 (paridades), 57 (parte), 64 (eventos de índice), 68 (regresiones y VAR, como módulo invitado) | FX-PPA-001, FX-CARRY-001, FX-COINT-001, FX-CORR-001, FX-BEER-001, IDX-REB-001 |
| MC-04 Crecimiento, difusión y prospectiva | 9, 12, 13, 20, 21, 22, 57 (parte) | TEM-DIFF-001 |
| MC-05 Simulación y escenarios | 13 (con MC-04), 14, 15 | SIM-MC-001, SCN-H-001 (y simulación invitada en FON-LEV-001) |
| MC-06 Aprendizaje automático y predicción calibrada | 16, 17, 35 | ML-CAL-001, ML-PRED-001, ML-CLUS-001 |
| MC-07 Optimización, decisión y riesgo | 24, 25, 34, 40 (valor de la información) | RISK-VAR-001, RISK-DD-001, DEC-VOI-001 |
| MC-08 Auditoría cuantitativa independiente | 29, 31, 41 (contraste), 42 | AUD-REX-001 |
| MC-09 Valoración y modelos de precios | 44–50, 51 (carry y momentum), 52, 53, 54, 55, 56 (parte), 64–68 | DER-OPT-001, ACC-*, FIR-*, FX-MOM-001, CMD-CURVE-001, CMD-RETDEC-001, CMD-REAL-001, REI-*, CHR-ONCHAIN-001, CHR-FUND-001, CHR-TOKEN-001, PRV-*, ALT-DESMOOTH-001, ALT-HF-001, ALT-AUC-001, IDX-ERP-001, IDX-REL-001, FON-DISC-001, FON-LEV-001, DER-VRP-001, DER-SKEW-001, DER-TERM-001, DER-ROLL-001, MON-EXP-001, MON-FIX-001, TCV-* |
| MC-10 Evaluación predictiva y backtesting | 31 (validación predictiva), 58–63 | FC-EVAL-001, FC-CAL-001, BT-DSR-001, BT-PBO-001, BT-VAR-001 |
| STC-1 a STC-4 | 26, 30, 32, 36 (datos) | (servicios deterministas; sin fichas propias) |

Ningún módulo es «de un tipo de activo»: la aplicación por tipo la gobiernan los perfiles PERF-xx (documento «Perfiles de clase de activo del Motor», V5.0).

## 5. Aplicaciones por tipo de activo (vista inversa)

| Tipo | Perfil | Áreas núcleo del tipo | Áreas de apoyo frecuentes |
|---|---|---|---|
| RV | PERF-ACC | 44, 45, 50 | 6, 7, 10, 18, 25, 49, 64 |
| RF | PERF-FIR | 46, 47, 48 | 8, 10, 19, 36, 25, 68 |
| DIV | PERF-FX | 51, 50 (carry y momentum) | 6, 8, 10, 19, 49, 67 |
| MP | PERF-CMD | 52, 22 | 6 (estacionalidad), 7, 10, 25, 49 |
| IDX | PERF-IDX | 64, 45 | 7, 10, 11 (eventos), 23, 33, 50, 51 |
| FON | PERF-ETF | 65, 56 | 6, 14, 33, 50, 55 |
| DER | PERF-DER | 66, 49 | 6, 14, 25 (colas), 47 |
| INM | PERF-REI | 53 | 46, 47, 44, 50, 55 (desuavizado de referencia), 25 |
| CRI | PERF-CHR | 54 | 6, 10, 25 (colas extremas), 49, 33 |
| ALT | PERF-PRV, PERF-ALT | 55 | 50, 48, 53 (infraestructuras e inmobiliario privados), 25, 27 (sesgos), 44 |
| MON | PERF-MON | 67 | 2, 19, 36, 47, 51 |
| TCV | PERF-TCV | 68, 47, 48 | 46, 49, 66, 8, 19, 25 |
| Capas | PERF-TEM, PERF-ESG, PERF-MAC | 9 y 20–21 (TEM), 57 (ESG), 19 (macro) | 13, 18 |

## 6. Correspondencia con la taxonomía de F8 (TM-)

| Temática F8 | Áreas |
|---|---|
| TM-01 Estadística e inferencia | 1–5, 23, 27, 37 |
| TM-02 Series temporales y detección de tendencias | 6, 7 |
| TM-03 Volatilidad y regímenes | 6 (volatilidad), 10 |
| TM-04 Econometría y causalidad | 8, 11, 19 |
| TM-05 Valoración de activos y estructura temporal | 44–48, 67, 68 |
| TM-06 Derivados y volatilidad implícita | 49, 66 |
| TM-07 Modelos factoriales y carteras | 18, 50 |
| TM-08 Riesgo y valores extremos | 24, 25 |
| TM-09 Simulación y métodos numéricos | 14, 15, 30 |
| TM-10 Aprendizaje automático para finanzas | 16, 17, 35 |
| TM-11 Evaluación predictiva y backtesting | 31, 58–63 |
| TM-12 Crecimiento, difusión y prospectiva cuantitativa | 9, 12, 13, 20–22 |
| TM-13 Métricas específicas por tipo de activo | 51–57, 64, 65 |
| TM-14 Datos, calidad y reproducibilidad | 26, 28, 29, 32, 33, 36, 38–43 |

El Documentador para el Motor mantiene en F8, para cada temática, al menos las referencias canónicas citadas en las fichas del Catálogo y en los prompts de los módulos, ordenadas por calidad Q.

## 7. Prioridades de implantación

| Prioridad | Áreas | Criterio |
|---|---|---|
| **P0** | 1–8, 10, 13, 14, 17, 18, 19, 23–27, 29–33, 36–43, 58–61, 63 | Sin ellas el bloque no puede calcular con trazabilidad (R7), validar (G3), certificar horizontes (R13) ni aprender (sección 12 del Documento 0) |
| **P1** | 9, 11, 16, 22, 28, 44–53, 54 (mercado), 55 (desuavizado), 56, 62, 64–68 | Métodos propios de tipo de activo con datos accesibles; habilitan la dimensión «valoración del ámbito» de A en los doce tipos |
| **P2** | 12, 15, 20, 21, 34, 35, 54 (en cadena), 55 (resto), 57 | Datos especializados, uso ocasional o madurez metodológica baja |

Orden de implantación recomendado: P0 completo → fichas P1 de valoración de los doce tipos de activo (al menos una por tipo para que A no dependa solo del juicio: p. ej., IDX-ERP-001, FON-DISC-001, DER-VRP-001, MON-YLD-001, TCV-TP-001 en los tipos nuevos) → P2 bajo demanda acreditada por el Registro de cálculos.

## 8. Metaespecialización: cuándo no calcular

El Motor debe saber reconocer cuándo un cálculo no procede, y decirlo:

1. **El cálculo no puede cambiar la decisión** (DEC-VOI-001; R15): no se ejecuta.
2. **El horizonte es «No» para el tipo de activo** (8.3 del Documento 0; p. ej., FON en H1, DER y MON en H4): se rechaza la previsión.
3. **Datos por debajo del mínimo de la ficha o del perfil**: se rechaza o se sirve con limitación; nunca se rellena.
4. **El método pertenece a otro tipo** (R21): DCF de un criptoactivo sin flujos, PER de un índice de bonos, VaR normal sobre colas extremas.
5. **Series suavizadas sin desuavizar** comparadas con activos cotizados.
6. **Probabilidades neutrales al riesgo** pedidas como probabilidades reales.
7. **Muestra de evaluación insuficiente** (< 30 por celda): solo descriptivos.
8. **Incertidumbre profunda**: escenarios sin probabilidades.
9. **La petición pretende comparar o seleccionar instrumentos concretos** (frontera con el Bloque B): `FUERA_DE_CATALOGO` con la ficha de ámbito más próxima.

## 9. Pruebas de competencia del servicio

Batería en `09_Pruebas`, con al menos: una misma tendencia con implicaciones distintas para RV, RF, DIV, MP, CRI, IDX, MON y TCV; un activo híbrido con dos perfiles; datos insuficientes (criptoactivo con historia corta, cosecha privada sin flujos, categoría de fondos cerrados con menos de 5 vehículos); una petición de comparar instrumentos concretos rechazada; un cálculo sin valor informativo que el Motor no ejecuta; una tendencia real que no es oportunidad por valoración; una re-ejecución CT-10 con discrepancia de convención; una evaluación de celda con fuga detectada; una certificación con muestra en el límite (n = 50) en la que el Motor informa del ECE nulo. Ningún área ni ficha se declara validada sin evidencia registrada (R22).

## 10. Lo que el Motor no asume

La interpretación económica y la decisión son del solicitante; la selección y verificación de fuentes, de los agentes de conocimiento; la auditoría de agentes, del circuito Orquestador técnico–Auditor; la certificación de horizontes y la recalibración, del Evaluador; la selección de activos e instrumentos concretos dentro de cada ámbito, del Bloque B; la decisión de inversión, del Broker Personal. El Motor no gestiona carteras del usuario ni recomienda: entrega cálculos reproducibles con sus límites.
