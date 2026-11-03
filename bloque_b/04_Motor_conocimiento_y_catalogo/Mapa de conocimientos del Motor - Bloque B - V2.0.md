# Mapa de conocimientos del Motor de Cálculo Avanzado de Mercados (AG-B16)

**Bloque B · Robot Investor · Versión V2.0 · 03/11/2026 · actualizado V2.1 (03/11/2026)** · Subordinado al Documento 0 del Bloque B, óptima V2.1. V2.1: áreas nuevas 76–81 (desglose jerárquico y AE, puntuación del cuello PCB, potencial de emergentes PEM, proyección estructural H5, evaluación por hitos, evaluación de puertas y seguimientos), con sus fichas del Catálogo V2.1.

Archivo **CC** (propietario: operador, tipo 3; el Motor propone). Lectores: AG-B16 y sus módulos, AG-B19 (Documentador para el Motor), AG-B12, AG-B13, AG-B21; también lo consultan el Auditor y el Evaluador a través de F8 y RC. Comparte numeración con el «Catálogo de cálculos del Motor - Bloque B - V2.0» (campo «Mapa: área») y con los «Perfiles de estrategia y de selección del Motor - Bloque B - V2.0».

---

## 1. Propósito y uso

1.1. Este mapa enumera **todas las áreas de conocimiento** que el Motor del Bloque B debe dominar para analizar sectores, subsectores, temáticas, mercados geográficos, segmentos, estrategias y cadenas de valor y para cribar y ordenar candidatos, con su nivel, su módulo responsable, las dimensiones (D1–D12) y la selección (F5) a las que sirve, su temática de F8 (TMB-01…TMB-14), sus fichas del Catálogo y su prioridad.

1.2. **Usos gobernados.** (a) **Enrutado**: el Orquestador de Cálculo sitúa cada petición CT-B-13 en su área, su módulo y su perfil. (b) **Selección de métodos**: a igual precisión exigida se prefiere el área y el método de nivel más bajo. (c) **Rechazo con orientación**: una petición fuera de cobertura se rechaza indicando el área y la ficha más próximas. (d) **Ampliación**: propuestas de fichas y perfiles (tipo 3) con evidencia de RC. (e) **Mantenimiento del conocimiento**: el Documentador para el Motor (AG-B19) organiza F8 por TMB- y vigila la literatura de cada área (sección 6), con el objetivo de ≥ 20 referencias verificadas por temática (13.3 del Documento 0).

1.3. **Niveles de dominio.**

| Nivel | Significado | Activación |
|---|---|---|
| I · Fundamentación | Imprescindible; usado en casi todas las peticiones | Siempre disponible |
| II · Especialización | Métodos propios de un tipo de objeto, de una dimensión o de la selección, de uso frecuente | Bajo demanda, con ficha |
| III · Especialización condicionada | Uso ocasional, coste alto, datos especializados o riesgo de mal uso | Solo con petición explícita, ficha vigente y justificación en el plan (normalmente EXT) |

1.4. **Prioridades**: **P0** sin ellas el bloque no puede puntuar ni seleccionar con trazabilidad (R9), validar (G3), refutar con cifras ni certificar (R13); **P1** propias de un tipo de objeto o de activo con datos gratuitos accesibles; **P2** ampliación.

1.5. **Cobertura no es obligación** (R22) y **madurez declarada** (R26): todas las áreas están **documentadas**; la madurez de cada método consta en su ficha.

1.6. **Frontera con los Bloques C.x** (R7): ninguna área habilita precios objetivo ni valoraciones individuales completas; las valoraciones de candidatos son **para ordenar**.

## 2. Bloques temáticos

| Bloque | Áreas | Módulos | TMB | Prioridad dominante |
|---|---|---|---|---|
| I. Fundamentos cuantitativos | 1–4 | MC-B01 | TMB-01, TMB-08, TMB-14 | P0 |
| II. Series, regímenes y flujos | 5–10 | MC-B01 | TMB-01, TMB-09, TMB-12 | P0/P1 |
| III. Dimensionado y difusión | 11–15, 79 | MC-B02 | TMB-02, TMB-03 | P0/P1 |
| IV. Organización industrial | 16–20, 76 | MC-B03 | TMB-04, TMB-10, TMB-13 | P0/P1 |
| V. Oferta, costes y tecnología | 21–26, 77 | MC-B04 | TMB-05, TMB-10 | P0/P1 |
| VI. Econometría y macro-sector | 27–32 | MC-B05 | TMB-02 | P0/P1 |
| VII. Valoración sectorial y de candidatos | 33–40 | MC-B06 | TMB-06, TMB-07 | P0/P1 |
| VIII. Cribado, ranking y factores | 41–48, 75, 78 | MC-B07 | TMB-07, TMB-12, TMB-13 | P0 |
| IX. Simulación, escenarios y sensibilidad | 49–55 | MC-B08 | TMB-08, TMB-13 | P0/P1 |
| X. Riesgo y redes | 56–62 | MC-B09 | TMB-09, TMB-10 | P0/P1 |
| XI. Evaluación predictiva y backtesting | 63–69, 80, 81 | MC-B10 | TMB-11, TMB-14 | P0/P1 |
| XII. Datos, reproducibilidad y gobierno del servicio | 70–74 | Orquestador de Cálculo, CTI-1…CTI-4, instancia aislada | TMB-14 | P0 |

## 3. Inventario completo de áreas

Abreviaturas: D1…D12 (8.2 del Documento 0); «Sel.» = selección de activos (F5, 9.4–9.7); «Punt.» = puntuaciones A, E, C y S.

### Bloque I · Fundamentos cuantitativos

| Área | Contenido operativo | Nivel | Módulo | Sirve a | TMB | Fichas | Prior. |
|---|---|---|---|---|---|---|---|
| 1. Cálculo financiero y crecimiento | Rentabilidades simples y logarítmicas, divisa base EUR, anualización, CAGR y efecto base, nominal/real, contribuciones | I | MC-B01 | Todas | TMB-01 | FIN-CAGR-001 | P0 |
| 2. Estadística descriptiva y robusta | Momentos, MAD, recortes, winsorización, atípicos marcados, cuantiles tipo 7, percentiles históricos | I | MC-B01 | Todas; Sel. | TMB-01, TMB-14 | ST-DESC-001 | P0 |
| 3. Inferencia y comparaciones múltiples | Contrastes paramétricos y no paramétricos, IC, potencia, Holm, BH, Bayes Beta-binomial, valores p | I | MC-B01 | Todas; MC-B10 | TMB-01, TMB-14 | ST-INF-001, ST-DESC-001 | P0 |
| 4. Remuestreo | Bootstrap iid, BCa, por bloques, estacionario; remuestreo común a universos | I | MC-B01 | Sel. (IC de rango); MC-B08, MC-B10 | TMB-08 | ST-BOOT-001 | P0 |

### Bloque II · Series, regímenes y flujos

| Área | Contenido operativo | Nivel | Módulo | Sirve a | TMB | Fichas | Prior. |
|---|---|---|---|---|---|---|---|
| 5. Estacionariedad y tendencia | ADF, KPSS, Zivot-Andrews; Mann-Kendall, Sen | I | MC-B01 | D2, D3, D7, D10 | TMB-01 | FX-TREND-001 | P0 |
| 6. Estacionalidad, filtros y conciliación | STL, X-13/TRAMO-SEATS, Hamilton frente a HP, ETS, conciliación jerárquica MinT | II | MC-B01 | D2, D3 | TMB-01 | FX-STL-001, SER-HIER-001 | P1 |
| 7. Rupturas estructurales | Chow, Quandt-Andrews, Bai-Perron, CUSUM de Page, bayesiano | I | MC-B01 | D7, D12; Vigía | TMB-01 | FX-BRK-001 | P0 |
| 8. Regímenes | Markov-switching, HMM, probabilidades filtradas, RCM | I | MC-B01 | D7; RGM-B; Vigía | TMB-01 | FX-REGIME-001 | P0 |
| 9. Volatilidad | Estimadores de rango, EWMA, GARCH y variantes, QLIKE | I | MC-B01 | Sel. (RI); D12 | TMB-09, TMB-01 | FX-VOL-001, VOL-GARCH-001 | P0 |
| 10. Flujos, posicionamiento y sentimiento | Flujos relativos, COT, posiciones cortas, revisiones, saturación narrativa, crowding | II | MC-B01, MC-B07 | D10; Sel. (MO en FON); tope de A | TMB-01, TMB-12 | SER-FLOW-001, FAC-CROWD-001 | P1 |

### Bloque III · Dimensionado y difusión

| Área | Contenido operativo | Nivel | Módulo | Sirve a | TMB | Fichas | Prior. |
|---|---|---|---|---|---|---|---|
| 11. Dimensionado TAM/SAM/SOM | Vías descendente y ascendente (demanda y oferta), consumo aparente, control de doble cómputo, seis atributos obligatorios | I | MC-B02 | D2; máquina (etapa 1) | TMB-02, TMB-03 | MKT-DIM-001, MKT-DIM-002 | P0 |
| 12. Triangulación | Ponderación por precisión en logaritmos, efectos aleatorios, heterogeneidad, discrepancia D, raíces comunes | I | MC-B02 | D2; DSC-B | TMB-02 | MKT-TRI-001 | P0 |
| 13. Descomposición del crecimiento | Segmentos, volumen y precio, contribuciones, *shift-share*, motor de ingresos | II | MC-B02 | D2; máquina (etapa 2) | TMB-02 | MKT-SEG-001 | P1 |
| 14. Difusión | Bass (NLS, sesgos), Bass generalizado, logística, Gompertz, Fisher-Pry, Norton-Bass | II | MC-B02 | D2, D5 | TMB-03 | DIF-BASS-001, DIF-LOG-001, DIF-GEN-001 | P1 |
| 15. Analogías y clase de referencia | A prioris de meta-análisis, base CHAT, retardos de adopción entre países | II | MC-B02 | D2, D5 | TMB-03 | DIF-ANLG-001 | P1 |
| 79. Proyección estructural H5 (V2.1) | Curvas S de largo plazo con techo fundamentado, Fisher-Pry y Norton-Bass, paridad de coste por curva de experiencia distributiva, bandas que se ensanchan, diseño de ≥ 3 hitos discriminantes frente a la extrapolación lineal; probabilidades solo cualitativas | II | MC-B02, MC-B04, MC-B08 | D2, D5, D9 en H5; F4 (hitos) | TMB-03, TMB-05, TMB-08 | DIF-H5-001 | P1 |

### Bloque IV · Organización industrial

| Área | Contenido operativo | Nivel | Módulo | Sirve a | TMB | Fichas | Prior. |
|---|---|---|---|---|---|---|---|
| 16. Concentración | HHI, CRn, N_eq, entropía, cotas con franja, ΔHHI, umbrales de referencia | I | MC-B03 | D1, D4 (4a); SEL-IDX | TMB-04 | IO-CONC-001 | P0 |
| 17. Poder de mercado y markups | Lerner, PCM contable, markup por enfoque de producción, conducta oligopolística | III | MC-B03 | D4, D8; A (ventaja) | TMB-04 | IO-LERN-001 | P1 |
| 18. Captura de valor por eslabón | *Profit pools*, cuota en beneficio frente a ingresos, ROIC por eslabón | I | MC-B03 | D4 (4a), D8; máquina (etapa 3) | TMB-04, TMB-10 | IO-MARG-001 | P0 |
| 19. Dinámica de cuotas y persistencia | Hymer-Pashigian, Spearman de rangos, persistencia de beneficios (Mueller), matrices de transición | II | MC-B03 | D4, D8; valor terminal; Sel. (QL) | TMB-04, TMB-02 | IO-SHARE-001, IO-PROF-001 | P1 |
| 20. Poder de negociación | Concentración de clientes y proveedores, dependencia mutua | III | MC-B03 | D4; Sel. (RI) | TMB-04 | IO-BARG-001 | P2 |
| 76. Desglose jerárquico y atractivo del eslabón (V2.1) | Árbol `ESL-` macro → sub → actividad → insumo; conciliación en valor añadido (sin doble cómputo), MinT; margen anómalo frente a adyacentes; AE con seis componentes y réplica de HT-03; sensibilidad de pesos | I | MC-B03, MC-B04, MC-B09 | D4 (4a–4d); PV3; entregable 6; Sel. (`eslabon_id`) | TMB-04, TMB-10, TMB-13 | VC-DESG-001 | P0 |

### Bloque V · Oferta, costes y tecnología

| Área | Contenido operativo | Nivel | Módulo | Sirve a | TMB | Fichas | Prior. |
|---|---|---|---|---|---|---|---|
| 21. Curvas de coste | Orden de mérito, *cash cost* y coste sostenido, percentiles, precio incentivo | II | MC-B04 | D3; SEL-MP (VA) | TMB-05 | SUP-COST-001 | P1 |
| 22. Capacidad y balances | Utilización efectiva, tubería por fases, balance oferta-demanda | II | MC-B04 | D3; máquina (etapa 2) | TMB-05 | SUP-UTIL-001 | P1 |
| 23. Cuellos de botella | Regla del mínimo, holgura, indicadores de tensión, persistencia | I | MC-B04, MC-B08 | D3, D4 (4d) | TMB-05, TMB-10 | SUP-BOTT-001, SIM-BOTT-001 | P0 |
| 24. Curvas de aprendizaje | Wright, uno y dos factores, IC de la tasa, confusiones (escala, insumos, márgenes) | II | MC-B04 | D3, D5 | TMB-05 | SUP-LRN-001 | P1 |
| 25. Previsión tecnológica probabilística | Moore frente a Wright (Sahal), Farmer-Lafond, Way et al., cobertura empírica | III | MC-B04 | D5 | TMB-05 | SUP-LRN-002 | P2 |
| 26. Inventarios | Desviación frente a la norma estacional, días de cobertura, teoría del almacenamiento | II | MC-B04 | D3; SEL-MP (VA) | TMB-05, TMB-01 | SUP-INV-001 | P1 |
| 77. Puntuación del cuello de botella (V2.1) | Nueve indicadores en semáforo con umbrales del Anexo A, severidad por recuento, persistencia por tiempo hasta cerrar el déficit, relevancia para el valor, PCB multiplicativo, materialidad, control de doble cómputo, señal de resolución | I | MC-B04, MC-B08 | D3, D4 (4d); PV3; AE; entregable 6 | TMB-05, TMB-10, TMB-13 | VC-BOT-001 (con SUP-BOTT-001, SIM-BOTT-001) | P0 |

### Bloque VI · Econometría y macro-sector

| Área | Contenido operativo | Nivel | Módulo | Sirve a | TMB | Fichas | Prior. |
|---|---|---|---|---|---|---|---|
| 27. Demanda y elasticidades | Log-log, VI, BLP, AIDS/QUAIDS, ARDL y largo plazo, meta-análisis | II | MC-B05 | D2; estrés de demanda | TMB-02 | ECO-ELAS-001 | P1 |
| 28. Paneles | Efectos fijos, errores agrupados, Driscoll-Kraay, GMM dinámico | II | MC-B05 | D7, D8 | TMB-02 | ECO-PANEL-001 | P1 |
| 29. Betas al ciclo y a tipos | Betas multifactoriales, rodantes y por régimen, beta de beneficios, apalancamiento operativo, duración de la renta variable | I | MC-B05 | D7, D8; Sel. (RI) | TMB-02 | ECO-CYC-001 | P0 |
| 30. Respuestas a impulsos | Proyecciones locales de Jordà, VAR | III | MC-B05 | D7; escenarios | TMB-02 | ECO-LP-001 | P2 |
| 31. Cointegración y causalidad | Engle-Granger, Johansen, MCE, regresión espuria, Granger con cautela | II | MC-B05 | D7, D9 (BEER) | TMB-02 | FX-COINT-001, ECO-GRANG-001 | P1 |
| 32. Exposición a factores | Beta del candidato al factor del ámbito, R² incremental, estabilidad, asincronía | I | MC-B05 | Sel. (pureza en DIV, MP, TCV; segunda vía en RV) | TMB-02, TMB-07 | ECO-EXPO-001 | P0 |

### Bloque VII · Valoración sectorial y de candidatos

| Área | Contenido operativo | Nivel | Módulo | Sirve a | TMB | Fichas | Prior. |
|---|---|---|---|---|---|---|---|
| 33. DCF | FCFF, fases, impulsores de valor, RONIC, beneficios normalizados; candidatos para ordenar | I | MC-B06 | D9; máquina (etapa 4); Sel. (VA) | TMB-06 | VAL-DCF-001 | P0 |
| 34. Expectativas implícitas | DCF inverso, brecha de expectativas, coste de capital implícito, beneficio residual | I | MC-B06 | D9; A (valoración frente a expectativas); máquina (etapa 5) | TMB-06 | VAL-REV-001 | P0 |
| 35. Múltiplos y comparables | Agregación armónica, percentiles históricos, múltiplos justificados, regresión de comparables | I | MC-B06 | D9; Sel. (VA) | TMB-06 | VAL-MULT-001 | P0 |
| 36. Rentabilidad del capital | ROIC con y sin fondo de comercio, beneficio económico, dispersión, capitalización de intangibles | I | MC-B06 | D8; A (calidad del crecimiento); Sel. (QL) | TMB-06 | VAL-ROIC-001 | P0 |
| 37. Coste de capital y primas | Beta ascendente de Damodaran, Hamada, CRP, calificación sintética, ERP implícita, Grinold-Kroner, CAPE | I | MC-B06 | D8, D9; PERF-B-GEO | TMB-06 | VAL-WACC-001, ACC-ERP-001, IDX-ERP-001 | P0 |
| 38. Máquina de proyecciones | Cinco etapas de 8.8, premisas falsables, propagación de la incertidumbre | I | MC-B06 (con MC-B02, MC-B04, MC-B08) | D2, D8, D9; F4 | TMB-06, TMB-08, TMB-03 | VAL-PROJ-001 | P0 |
| 39. Valoración específica por tipo de activo | Diferencial y pérdida esperada, carry y rolldown, PPA y BEER, curva de futuros, NAV y cap rate, descuento de cerrados, prima de varianza, métricas de red, rentabilidad monetaria, factores TCV, PME, desuavizado | II | MC-B06 | D9 de PERF-B-SEGM; Sel. (VA) en los doce SEL- | TMB-06, TMB-09 | VAL-RF-001, FIR-SPREAD-001, FX-CARRY-001, FX-PPA-001, FX-BEER-001, CMD-CURVE-001, REI-NAV-001, REI-CAP-001, FON-DISC-001, DER-VRP-001, CHR-ONCHAIN-001, MON-YLD-001, TCV-CARRY-001, PRV-PME-001, ALT-DESMOOTH-001 | P1 |
| 40. Calidad contable | Piotroski, Beneish, Altman, devengos, dilución, probabilidad de quiebra | I | MC-B06 | D8; Sel. (QL, alertas PC4) | TMB-07 | QLT-ACC-001 | P0 |

### Bloque VIII · Cribado, ranking y factores

| Área | Contenido operativo | Nivel | Módulo | Sirve a | TMB | Fichas | Prior. |
|---|---|---|---|---|---|---|---|
| 41. Normalización y neutralización | Winsorización 2,5/97,5, percentiles por rango medio, z robustos, neutralización por subgrupo | I | MC-B07 | Sel. (9.5.1) | TMB-07, TMB-13 | SCR-NORM-001 | P0 |
| 42. Pureza de exposición | Métricas por tipo de activo, intervalo, marca de frontera PC2 | I | MC-B07 | Sel. (PE, PC2); D1 en TEMATICA | TMB-07, TMB-12 | SCR-PUR-001, SCR-PUR-002 | P0 |
| 43. Puntuaciones y réplica de HT-03 | S, A, E, C; NA/NE; redondeos; topes; bandas marginales | I | MC-B07 | Punt.; G3; PA7, PC7 | TMB-13 | SCR-S-001, SCR-AEC-001 | P0 |
| 44. Robustez de rankings | Bootstrap de insumos y perturbación de pesos, IC de S y de rango, `P(top-N)`, FRONTERA, τ de Kendall | I | MC-B07 | Sel. (9.5.4; PC6) | TMB-07, TMB-08, TMB-13 | SCR-ROB-001 | P0 |
| 45. Duplicación y apuestas independientes | Solapamiento de carteras, correlación a 2 años, subclústeres, exposición compartida, N_ef | I | MC-B07 | Sel. (9.7; PC8); informe | TMB-07, TMB-09 | SCR-DUP-001, ML-CLUS-001 | P0 |
| 46. Liquidez y costes | ADV, Amihud, Roll, días de liquidación, coste total de mantener, capacidad | I | MC-B07 | Sel. (LA, CO); D2 de FACT | TMB-07 | SCR-LIQ-001 | P0 |
| 47. Factores y estilos | Momento, revisiones, primas larga-corta, Fama-MacBeth, GRS, diferencial de valoración, crowding, pruebas múltiples | II | MC-B07 | Sel. (MO); PERF-B-FACT | TMB-07, TMB-11 | ACC-MOM-001, FAC-PREM-001, FAC-SPREAD-001, FAC-CROWD-001 | P1 |
| 48. Decisión multicriterio | AHP, valor multiatributo, PROMETHEE, consistencia y sensibilidad | III | MC-B07 | Traducción de rasgos de la tesis (9.5.6) | TMB-13 | SCR-MCDA-001 | P2 |
| 75. Aprendizaje automático y texto | Similitud textual y diccionarios, calibración, validación cruzada temporal | III | MC-B07 (con MC-B05) | Pureza estimada; sentimiento | TMB-12 | SCR-PUR-002 | P2 |
| 78. Potencial de emergentes (V2.1) | PEM con seis criterios anclados y réplica de HT-03; estabilidad del orden; pureza de la vía de exposición (matriz cotizada, ETF o fondo) y exposición residual; tasas base de salidas a bolsa y SPAC como contexto | II | MC-B07, MC-B02 | Radar de AG-B24; subtabla del entregable 6; universo del Seleccionador | TMB-13, TMB-07, TMB-03 | EMG-PEM-001 | P1 |

### Bloque IX · Simulación, escenarios y sensibilidad

| Área | Contenido operativo | Nivel | Módulo | Sirve a | TMB | Fichas | Prior. |
|---|---|---|---|---|---|---|---|
| 49. Monte Carlo y QMC | Error de Monte Carlo, LHS, Sobol aleatorizado, reducción de varianza, generadores | I | MC-B08 | D12; F4; máquina | TMB-08 | SIM-MC-001, SIM-BOTT-001 | P0 |
| 50. Dependencia | Iman-Conover, cópulas gaussiana y t, reparación de Higham | I | MC-B08 | F4; estrés | TMB-08 | SIM-IC-001 | P0 |
| 51. Escenarios y RE | Escenarios coherentes, régimen de referencia, probabilidad frente a la referencia, RE, asimetría | I | MC-B08 | D12; A (asimetría); C (RE) | TMB-08 | SIM-SCN-001 | P0 |
| 52. Sensibilidad local y cribado | Tornado, Morris | I | MC-B08 | Protocolo cuantitativo (8.8) | TMB-08 | SIM-TOR-001 | P0 |
| 53. Sensibilidad global | Sobol (Saltelli, Jansen), Borgonovo, Shapley | II | MC-B08 | N3; banda marginal | TMB-08 | SIM-SOB-001 | P1 |
| 54. Juicio experto | Agregación lineal y logarítmica, modelo clásico de Cooke, extremización, Delphi | II | MC-B08 | Premisas sin datos; clase `juicio_experto` | TMB-13 | SIM-JUD-001 | P1 |
| 55. Valor de la información | VEIP, cruce de umbral, priorización de búsquedas | II | MC-B08 | R22; plan | TMB-13 | DEC-VOI-001 | P1 |

### Bloque X · Riesgo y redes

| Área | Contenido operativo | Nivel | Módulo | Sirve a | TMB | Fichas | Prior. |
|---|---|---|---|---|---|---|---|
| 56. Colas y trayectorias | VaR, ES, EVT, Cornish-Fisher, drawdown, escala 1–5, colapsos de factores | I | MC-B09 | D12; Sel. (RI); `riesgo_1a5` | TMB-09 | RISK-VAR-001, RISK-DD-001, RISK-CRASH-001 | P0 |
| 57. Estrés | Histórico, hipotético (demanda, márgenes, insumos, carbono, tipos), inverso | I | MC-B09 | D11, D12 | TMB-09, TMB-08 | RISK-STR-001 | P0 |
| 58. Correlación y contagio financiero | DCC, dependencia de cola, Forbes-Rigobon, Diebold-Yilmaz, CoVaR | II | MC-B09 | D7, D12; Sel. (duplicación) | TMB-09 | FX-CORR-001, RISK-RGC-001 | P0 |
| 59. Riesgo país y divisa | Estrés de divisa, dinámica de la deuda, sostenibilidad externa | II | MC-B09 | D6, D7 de GEO; SEL-DIV, SEL-RF | TMB-09 | RISK-GEO-001 | P1 |
| 60. Input-output | Leontief, Ghosh, Rasmussen, *upstreamness*, VA en el comercio, modelo de precios, extracción hipotética | II | MC-B09 | D4 (4a, 4e), D6 | TMB-10 | NET-IO-001 | P1 |
| 61. Propagación en redes | Choques de oferta con sustituibilidad, pesos de Domar, vínculos cliente-proveedor | II | MC-B09 | D4 (4d, 4e), D12 | TMB-10 | NET-SHOCK-001 | P1 |
| 62. Dependencias estratégicas | HHI por país del suministro, sanciones y controles, exposiciones comunes de candidatos | II | MC-B09 | D6; Sel. (apuestas) | TMB-10 | NET-EXPO-001 | P1 |

### Bloque XI · Evaluación predictiva y backtesting

| Área | Contenido operativo | Nivel | Módulo | Sirve a | TMB | Fichas | Prior. |
|---|---|---|---|---|---|---|---|
| 63. Puntuación y comparación de pronósticos | Brier y Murphy, log-score, CRPS, MASE, Diebold-Mariano (HLN), Giacomini-White, Clark-West | I | MC-B10 | F12; R13 | TMB-11 | FC-EVAL-001 | P0 |
| 64. Calibración | Fiabilidad, ECE con nulo simulado, recalibración logística, PIT | I | MC-B10 | F12; R13 | TMB-11 | FC-CAL-001 | P0 |
| 65. Insumos de certificación | Condiciones del Anexo A, Holm entre celdas, semáforos sin certificar | I | MC-B10 | R13; 12.3 | TMB-11 | FC-CERT-001, RK-CERT-001 | P0 |
| 66. Capacidad de rankings | IC de rango (Spearman), exceso del top-N frente a RI-EQ, tasa de acierto, contribución de componentes | I | MC-B10 | F12; recalibración de pesos de S | TMB-11, TMB-07 | RK-IC-001, RK-TOPN-001 | P0 |
| 67. Backtesting sin sesgos | Universos *point-in-time*, rentabilidades de exclusión, fechas de publicación, *vintages*, costes | I | MC-B10 | PERF-B-FACT; validación de playbooks (18.4) | TMB-11, TMB-14 | BT-SEL-001 | P0 |
| 68. Inferencia con selección | Sharpe probabilístico y deflactado, PBO (CSCV), *Reality Check*, SPA, `t > 3` | II | MC-B10 | PERF-B-FACT; BT-SEL-001 | TMB-11 | BT-DSR-001, BT-PBO-001 | P1 |
| 69. Modelo de tiempos | Regresión cuantílica p50/p80, cobertura empírica; por capa (V2.1) | II | MC-B10 | 9.9 (estimación de F0 por capa y acumulada) | TMB-14, TMB-02 | EVL-TIME-001 | P1 |
| 80. Evaluación por hitos H5 (V2.1) | Resolución de hitos, tasa de cumplidos con Wilson y Clopper-Pearson, conglomerado por tesis, desvío frente a la extrapolación lineal, señal de dos críticos incumplidos; sin certificación numérica | II | MC-B10 | F12; 12.8; Vigía | TMB-11 | FC-HITO-001 | P1 |
| 81. Evaluación de puertas y seguimientos (V2.1) | Falsos negativos de PV1–PV3 con grupo de comparación, atribución por criterio, función de coste; semáforo de N1-SEG con kappa ponderado, omisiones, falsas alarmas y antelación | II | MC-B10 | 12.7; recalibración de umbrales PV | TMB-11, TMB-14 | EVL-PV-001 | P1 |

### Bloque XII · Datos, reproducibilidad y gobierno del servicio

| Área | Contenido operativo | Nivel | Módulo | Sirve a | TMB | Fichas | Prior. |
|---|---|---|---|---|---|---|---|
| 70. Calidad de datos y DAT-B | Unidades, divisas, calendarios, faltantes, atípicos, duplicados, previsiones separadas de datos, informe de calidad | I | CTI-1 | Todas; PA2, PC3 | TMB-14 | (transversal a todas las fichas) | P0 |
| 71. Conocibilidad y tiempo real | «Conocible desde», *vintages*, retrasos de publicación, reexpresiones, fecha de corte | I | CTI-1, MC-B10 | Evaluación; Vigía; R30 | TMB-14 | (transversal) | P0 |
| 72. Supervivencia y universos *point-in-time* | Excluidos, fusionados, liquidados; rentabilidades de exclusión; reconstrucción histórica de universos | I | CTI-1, MC-B10 | Sel. histórica; 12.6 | TMB-14, TMB-11 | BT-SEL-001 | P0 |
| 73. Reproducibilidad y artefactos | Semillas, versiones, hash, linaje, caché idempotente, re-ejecución aislada | I | CTI-2, CTI-3, CTI-4; instancia aislada | R9; G3; CT-B-14 | TMB-14 | AUD-REX-001 | P0 |
| 74. Gobierno, seguridad y límites | Canales, datos sensibles, contenido externo como dato, frontera con C, madurez, propuestas de tipo 3 | I | Orquestador de Cálculo | R2, R7, R10–R12, R26 | TMB-14 | (reglas del prompt del Motor) | P0 |

## 4. Distribución por módulo

| Módulo | Áreas | Fichas | Perfiles principales |
|---|---|---|---|
| MC-B01 Estadística y series | 1–10 | 12 | Todos |
| MC-B02 Dimensionado de mercado y difusión | 11–15, 79 | 9 | PERF-B-TEMA, -SECT, -CADENA, -GEO (H5) |
| MC-B03 Organización industrial | 16–20, 76 | 7 | PERF-B-SECT, -CADENA, -TEMA |
| MC-B04 Oferta y costes | 21–26, 77 | 7 | PERF-B-CADENA, -SEGM, -TEMA, -SECT |
| MC-B05 Econometría y macro-sector | 27–32 | 7 | PERF-B-GEO, -SECT; SEL-DIV, -MP, -TCV |
| MC-B06 Valoración sectorial y de candidatos | 33–40 | 24 | PERF-B-SECT, -GEO, -SEGM; todos los SEL- |
| MC-B07 Cribado y ranking | 41–48, 75, 78 | 15 | Todos los SEL-; PERF-B-FACT; radar de emergentes |
| MC-B08 Simulación, escenarios y sensibilidad | 49–55 | 8 | Todos los PERF-B- |
| MC-B09 Riesgo y redes | 56–62 | 10 | PERF-B-CADENA, -GEO, -FACT |
| MC-B10 Evaluación predictiva y backtesting de selección | 63–69, 80, 81 | 12 | Todos |
| Orquestador de Cálculo, CTI-1…CTI-4, instancia aislada | 70–74 | 1 (AUD-REX-001) | Transversal |

## 5. Vista inversa: qué áreas usa cada tipo de objeto y cada tipo de activo

| Perfil | Áreas núcleo (STD) | Áreas de ampliación (EXT) |
|---|---|---|
| PERF-B-SECT | 16, 18, 29, 27, 33–37, 40, 49–52, 56, 57; 76, 77 si D4 ≥ P2; 78 (AG-B24) | 17, 19, 28, 53, 58; 79 (H5) |
| PERF-B-TEMA | 11–15, 42, 34, 38, 49–52, 10; 76, 77 si D4 ≥ P2; 78 | 24, 25, 60, 61, 75, 53, 6; 79 (H5) |
| PERF-B-GEO | 8, 29, 37, 35, 59, 51, 45 | 58, 30, 60 (sector ancla) |
| PERF-B-SEGM | 39, 8, 7, 10, 22, 26, 57 | 53, 58 |
| PERF-B-FACT | 47, 56, 67, 68, 46, 8 | 58, 51 |
| PERF-B-CADENA | 21–23, 60–62, 18, 51, 76, 77, 78 | 24, 49 (persistencia), 19, 79 (H5) |

| SEL- | Áreas |
|---|---|
| SEL-RV | 41–46, 32 (2.ª vía), 35, 34, 36, 40, 47, 9, 29, 20 |
| SEL-RF | 41–46, 39 (diferencial, pérdida esperada), 40, 56 |
| SEL-DIV | 41–46, 32, 39 (PPA, BEER, carry), 59, 47, 9 |
| SEL-MP | 41–46, 32, 39 (curva), 21, 26, 47 |
| SEL-IDX | 41–46, 16, 37, 35, 47, 56 |
| SEL-FON | 41–46, 39 (descuento), 35, 10, 47 |
| SEL-DER | 41–46, 39 (prima de varianza, curva), 56 |
| SEL-INM | 41–46, 39 (NAV, cap rate, desuavizado), 40, 56 |
| SEL-CRI | 41–46, 39 (métricas de red), 56 |
| SEL-ALT | 41–46, 39 (PME, descuento, desuavizado), 56 |
| SEL-MON | 41–46, 39 (rentabilidad monetaria) |
| SEL-TCV | 41–46, 32, 39 (factores TCV, prima de varianza), 56 |

Evaluación de todos: 63–68, 71, 72; V2.1: 80 (tesis H5) y 81 (puertas y seguimientos).

## 6. Correspondencia con F8 (TMB-01…TMB-14)

| TMB | Temática de F8 | Áreas | Fichas que respalda | Referencias ancla en F8 | Vigilancia prioritaria del Documentador para el Motor |
|---|---|---|---|---|---|
| TMB-01 | Estadística y series temporales aplicadas a sectores | 1–3, 5–9, 26 | ST-*, FIN-CAGR-001, FX-TREND/STL/BRK/REGIME/VOL-001, VOL-GARCH-001, SER-HIER-001 | DOC-MOT-0020, DOC-MOT-0021, DOC-MOT-0024, DOC-MOT-0028, DOC-MOT-0029, DOC-MOT-0030, MBM-0005 | Conciliación jerárquica; detección de rupturas en línea |
| TMB-02 | Econometría de la demanda, elasticidades y paneles sectoriales | 11–13, 19, 27–32, 69 | ECO-*, FX-COINT-001, MKT-TRI-001 | DOC-MOT-0039, DOC-MOT-0044, DOC-MOT-0232, DOC-MOT-0239, MBM-0014, MBM-0019, MBM-0026, MBM-0033, MBM-0037 | Meta-análisis de elasticidades por sector (más allá de energía) |
| TMB-03 | Modelos de difusión y curvas de adopción | 11, 14, 15, 38, 79 | DIF-* (incluida DIF-H5-001), MKT-DIM-001, EMG-PEM-001 (tracción) | DOC-MOT-0106, DOC-MOT-0112, DOC-MOT-0433, DOC-MOT-0435, DOC-MOT-0436, DOC-MOT-0445, MBM-0040, MBM-0041 | Difusión de tecnologías digitales y de IA; a prioris por categoría |
| TMB-04 | Concentración, poder de mercado y márgenes | 16–20 | IO-* | MBM-0069, MBM-0071, MBM-0073, MBM-0086, MBM-0091, DOC-MOT-0515 | Medición de markups con datos contables europeos |
| TMB-05 | Curvas de costes, de aprendizaje y de capacidad | 21–26, 77, 79 | SUP-*, SIM-BOTT-001, VC-BOT-001, DIF-H5-001 (paridad de coste) | DOC-MOT-0109, DOC-MOT-0110, DOC-MOT-0111, DOC-MOT-0428, DOC-MOT-0431, MBM-0047, MBM-0067 | Curvas de coste de materias primas críticas; métodos de identificación de cuellos (laguna: 4 referencias de nivel C) |
| TMB-06 | Valoración: DCF, múltiplos, ROIC y coste de capital sectorial | 33–39 | VAL-*, ACC-ERP-001, IDX-ERP-001, específicas por tipo | MBM-0095, MBM-0096, MBM-0097, MBM-0102, DOC-MOT-0053, DOC-MOT-0054, DOC-MOT-0509 | Valoración de REIT, ETC y tokens (cobertura por tipo de activo) |
| TMB-07 | Modelos factoriales, cribado cuantitativo y rankings | 32, 40–47 | SCR-*, QLT-ACC-001, ML-CLUS-001, ACC-MOM-001, FAC-* | DOC-MOT-0060, DOC-MOT-0061, DOC-MOT-0064, DOC-MOT-0347, ANA-DOC-0279, MBM-0111, MBM-0119, MBM-0122 | Robustez de rankings compuestos y medición de pureza (laguna: literatura específica de pureza temática) |
| TMB-08 | Simulación Monte Carlo, escenarios y sensibilidad | 4, 38, 44, 49–53 | SIM-*, ST-BOOT-001, SCR-ROB-001 | DOC-MOT-0006, DOC-MOT-0080, MBM-0201, MBM-0205, MBM-0208, MBM-0209, MBM-0217 | Sensibilidad con insumos correlacionados (Shapley) |
| TMB-09 | Riesgo: volatilidad, correlaciones, colas y estrés sectorial | 9, 45, 56–59 | RISK-*, FX-CORR-001, ALT-DESMOOTH-001 | DOC-MOT-0033, DOC-MOT-0074, DOC-MOT-0075, DOC-MOT-0214, DOC-MOT-0350, DOC-MOT-0365, MBM-0218 | Estrés sectorial de transición climática |
| TMB-10 | Análisis input-output y redes de cadena de suministro | 18, 23, 60–62, 76, 77 | NET-*, IO-MARG-001, SUP-BOTT-001, VC-DESG-001, VC-BOT-001 | MBM-0219, MBM-0225, MBM-0227, MBM-0229, MBM-0231, ANA-DOC-0448, ANA-DOC-0449 | Desagregación de eslabones dentro de sectores de las tablas |
| TMB-11 | Evaluación predictiva, calibración y backtesting de selección | 47, 63–68, 72, 80, 81 | FC-* (incluida FC-HITO-001), RK-*, BT-*, EVL-PV-001 | DOC-MOT-0091, DOC-MOT-0095, DOC-MOT-0098, DOC-MOT-0101, DOC-MOT-0102, DOC-MOT-0420, MBM-0233 | Inferencia sobre IC de rango con universos pequeños |
| TMB-12 | Aprendizaje automático y análisis de texto para mercados | 10, 42, 75 | SCR-PUR-002, SER-FLOW-001, FAC-CROWD-001 | FXM-0271, MBM-0235, MBM-0236, MBM-0238, DOC-MOT-0089 | Pureza por texto en informes europeos (ESEF) |
| TMB-13 | Decisión multicriterio y agregación de juicio experto | 41, 43, 44, 48, 54, 55, 76–78 | SCR-S-001, SCR-AEC-001, SCR-MCDA-001, SIM-JUD-001, DEC-VOI-001, VC-DESG-001 (AE), VC-BOT-001 (PCB), EMG-PEM-001 | MBM-0241, MBM-0248, MBM-0250, MBM-0254, MBM-0264, ANA-DOC-0236 | Análisis de incertidumbre de indicadores compuestos (Saisana, Saltelli y Tarantola; guía OCDE-JRC): alta propuesta |
| TMB-14 | Datos, calidad y reproducibilidad | 2, 3, 67, 69–74 | AUD-REX-001; transversal | DOC-MOT-0124, DOC-MOT-0125, DOC-MOT-0461, DOC-MOT-0463, MBM-0269, MBM-0271, MBM-0272 | Sesgo de supervivencia en universos de ETF europeos |

Regla para el Documentador para el Motor: mantener en F8, para cada temática, al menos las referencias citadas en las fichas del Catálogo y en los prompts de los módulos, ordenadas por Q, y avisar al Motor (CT-B-23, «Novedades») de refutaciones o mejoras que afecten a una ficha.

## 7. Prioridades de implantación

| Prioridad | Áreas | Criterio |
|---|---|---|
| **P0** | 1–5, 7–9, 11, 12, 16, 18, 23, 29, 32–38, 40–46, 49–52, 56–58, 63–67, 70–74, 76, 77 | Sin ellas el bloque no puede puntuar ni seleccionar con trazabilidad (R9), validar (G3), refutar con cifras, estimar el IC del rango (PC6) ni certificar (R13) |
| **P1** | 6, 10, 13–15, 19, 21, 22, 24, 26–28, 31, 39, 47, 53–55, 59–62, 68, 69, 78–81 | Métodos propios de tipo de objeto o de activo con datos gratuitos; habilitan VA en los doce SEL- y la profundidad P3 de D2–D4 |
| **P2** | 17, 20, 25, 30, 48, 75 | Datos especializados, coste alto o madurez metodológica baja |

Orden recomendado: reverificación de las fichas heredadas → canal de selección P0 (áreas 41–46, 32, 40) → tesis y máquina P0 (11, 12, 16, 18, 23, 29, 33–38, 49–52, 57) → evaluación P0 (63–67) → valoración específica por tipo (39, al menos una ficha por SEL-) → P2 bajo demanda acreditada por RC.

## 8. Metaespecialización: cuándo no calcular

1. **El cálculo no puede cambiar A, E, C, S, el top-N, una puerta ni un horizonte** (DEC-VOI-001; R22): no se ejecuta, salvo «contexto» declarado y barato.
2. **Horizonte «No» para el tipo de activo** (8.6): previsión rechazada (`HORIZONTE_NO_APLICABLE`).
3. **Datos por debajo del mínimo de la ficha o del perfil**: rechazo o limitación; nunca se rellena.
4. **Método de otro dominio**: DCF de un token sin flujos; PER de un banco con EV; Bass sin tramo de aceleración; HHI de una clasificación oficial tomada como mercado.
5. **Universo superviviente** en un backtest o un IC de rango (`UNIVERSO_SESGADO`).
6. **Probabilidades sin base calibrable**: bandas verbales; nunca cifras «a ojo».
7. **Series suavizadas sin desuavizar** comparadas con cotizados.
8. **Muestra de evaluación insuficiente** (< 30 pronósticos o < 15 rankings por celda): solo descriptivos.
9. **Petición de precio objetivo, tamaño de posición o idoneidad**: `PRECIO_OBJETIVO_FUERA_DE_ROL`.
10. **Incertidumbre profunda** (techo de mercado sin anclaje): escenarios de juicio declarados, sin probabilidades numéricas.
11. **H5** (V2.1): trayectorias y hitos sí; probabilidades numéricas nunca (`PROBABILIDAD_NO_CERTIFICABLE`, R13).
12. **Profundidad del desglose** (V2.1): se detiene donde un nivel más no cambia ni AE ni PCB del eslabón (8.7.1, 10.4 del Documento 0).

## 9. Pruebas de competencia del servicio

Batería en `09_Pruebas`, con al menos: un sector con concentración alta y ROIC por encima del WACC pero expectativas ya descontadas (brecha negativa); una temática con TAM de terceros inflado (D > 3) y pureza baja de los vehículos «temáticos»; un mercado geográfico con sector ancla; un segmento de crédito con diferencial en percentil extremo; un factor con prima significativa en muestra que no sobrevive al DSR; un eslabón con cuello identificado por la regla del mínimo y su persistencia simulada; un universo RV heterogéneo que exige neutralización; un candidato en `FRONTERA`; dos ETF del mismo índice (duplicado); un mismo emisor en RV y RF (exposición compartida); una réplica de S que difiere de HT-03 (debe bloquearse); una petición de precio objetivo rechazada; un backtest sin universo *point-in-time* rechazado; una re-ejecución CT-B-14 con discrepancia de universo; V2.1: un desglose de tres niveles con conciliación conocida, un eslabón con cuello material (PCB ≥ 30 y dos rojos) y otro con un solo rojo, un par de indicadores correlacionados (doble cómputo), AE y PEM contra HT-03, una tesis H5 con hitos no discriminantes y una petición de probabilidad H5 rechazada, y un lote de puertas sintéticas con grupo de comparación. Ningún área ni ficha se declara validada sin evidencia registrada (R26).

## 10. Lo que el Motor no asume

La interpretación económica, la tesis, las puertas, los veredictos y el top-N son del Director, los especialistas y el Seleccionador con HT-03; los universos, de HT-11; las fuentes, de los agentes de conocimiento y el Curador; la auditoría, del circuito Orquestador técnico–Auditor; la certificación y la recalibración, del Evaluador; la valoración individual completa de cada candidato, de los Bloques C.x; la decisión, del Broker Personal. El Motor entrega cálculos reproducibles con su incertidumbre y sus límites.
