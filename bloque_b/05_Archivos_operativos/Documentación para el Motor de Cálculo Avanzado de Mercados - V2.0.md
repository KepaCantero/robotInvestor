# Archivo operativo F8 — Documentación para el Motor de Cálculo Avanzado de Mercados

**Bloque B · Robot Investor · Versión óptima V2.0 · 02/11/2026** · Subordinado al Documento 0 del Bloque B V2.0.

**Versión del archivo:** V2.0 (02/11/2026), alineada con el Documento 0 del Bloque B V2.0 · **Código:** F8 · **Propietario:** AG-B19 Documentador para el Motor de Cálculo Avanzado de Mercados (DOC-M)

## Cómo usar este archivo

**Propósito.** Archivo del Bloque B (taxonomía TMB del Anexo D del Documento 0 del Bloque B); incluye referencias reutilizadas del Bloque A (conservan su ID) y referencias nuevas (prefijo MBM-).  Fondo de referencias de métodos cuantitativos (estadística, series temporales, econometría, valoración, derivados, carteras, riesgo, simulación, aprendizaje automático, evaluación predictiva y métricas por clase) que respalda cada servicio del Motor (MC-B01 a MC-B10) y la evaluación de pronósticos.

**Propietario y acceso.** Escribe solo AG-B19 (DOC-M). Leen: AG-B16 Motor, AG-B02 Director, especialistas AG-B03…AG-B11, AG-B12, AG-B13, AG-B18, AG-B15 Curador, Orquestador, Auditor y Evaluador. Cualquier otro acceso es una incidencia (Documento 0, 5.2).

**Reglas de uso.**

1. **Lectura.** Lea primero «Novedades»; después el índice de temáticas; dentro de la temática, las fichas aparecen **ordenadas por Q descendente** (a igualdad, la más reciente primero). Cite siempre el ID de la ficha. Para corroboración (PA1) solo cuentan fichas de nivel A o B con `Estado del enlace` distinto de `ROTO`; una ficha `PENDIENTE_VERIFICACION_ALTA` no sustenta evidencia hasta que su propietario la confirme.
2. **Calidad.** Q (0–100) con la rúbrica 13.3: Tipo y revisión 25 · Rigor y transparencia 20 · Autoridad 15 · Vigencia 10 · Impacto 10 · Independencia 10 · Accesibilidad y estabilidad 10. Niveles: A (Q ≥ 80), B (65–79), C (50–64), D (< 50: candidata a baja salvo que sea la única fuente de un dato necesario, declarado). En las semillas la Q es provisional hasta la verificación de alta.
3. **Estados del enlace** (HT-02, barrido semanal del domingo): `OK`, `REDIRIGIDO`, `ROTO` (4xx/5xx en dos intentos separados 24 h), `MURO_PAGO`, `CONTENIDO_CAMBIADO` (similitud < 0,8 frente a la copia archivada) y `PENDIENTE_BARRIDO` (estado inicial de esta versión: ningún enlace se ha comprobado aún con HT-02). `Última verificación` recoge la última comprobación documentada, no una del barrido.
4. **Acciones** (potestad plena del propietario, R25): `REPARAR` (DOI, nueva URL oficial o copia archivada; obligatoria cuando la ficha lleva «Alerta»); `DEGRADAR` (bajar Q o nivel, con motivo); `BORRAR` cuando haya enlace roto sin alternativa tras dos barridos, contenido retirado o retractado, falsedad o manipulación demostrada, redundancia total con una ficha de mayor Q, o Q < 50 sin uso en 180 días. Cada borrado añade una línea al «Registro de bajas»; si la ficha sustentaba EVD de F2 se avisa al Curador (CT-B-15, tipo `fuente_retirada`).
5. **Ciclo.** DOC-M alimenta el archivo por su agenda de vigilancia y por las peticiones del Motor (CT-B-23); antes de buscar aplica el Fondo metodológico (R25). El Motor cita el ID de la ficha en el artefacto de cada cálculo (RC). Mensualmente el propietario informa al Orquestador de altas, reparaciones, bajas, salud de enlaces y lagunas (CT-B-24). Los IDs son inmutables y no se reutilizan; en el «Registro de bajas», «REF-id» es el ID propio de la ficha.

**Semillas.** Las fichas con `Estado: PENDIENTE_VERIFICACION_ALTA` son obras canónicas añadidas en V3.0 para cubrir lagunas evidentes. Sus identificadores (DOI, ISBN, URL) proceden de conocimiento previo y llevan la marca «a verificar»: no están verificadas y no pueden citarse como respaldo de un cálculo hasta que DOC-M las confirme con HT-02.

## Índice de temáticas (Anexo D, TMB-)

| Código | Temática | Referencias | Verificadas | Pendientes de verificación | A | B | C | D | Q medio |
|---|---|---|---|---|---|---|---|---|---|
| TMB-01 | Estadística y series temporales aplicadas a sectores | 36 | 36 | 0 | 31 | 5 | 0 | 0 | 86,7 |
| TMB-02 | Econometría de la demanda, elasticidades y paneles sectoriales | 34 | 34 | 0 | 27 | 7 | 0 | 0 | 85,5 |
| TMB-03 | Modelos de difusión y curvas de adopción | 28 | 28 | 0 | 23 | 5 | 0 | 0 | 84,4 |
| TMB-04 | Concentración, poder de mercado y márgenes | 28 | 28 | 0 | 16 | 12 | 0 | 0 | 80,8 |
| TMB-05 | Curvas de costes, de aprendizaje y de capacidad | 28 | 28 | 0 | 13 | 11 | 4 | 0 | 78,0 |
| TMB-06 | Valoración: DCF, múltiplos, ROIC y coste de capital sectorial | 26 | 26 | 0 | 18 | 7 | 1 | 0 | 82,7 |
| TMB-07 | Modelos factoriales, cribado cuantitativo y rankings | 28 | 28 | 0 | 24 | 4 | 0 | 0 | 88,4 |
| TMB-08 | Simulación Monte Carlo, escenarios y sensibilidad | 32 | 32 | 0 | 29 | 3 | 0 | 0 | 87,3 |
| TMB-09 | Riesgo: volatilidad, correlaciones, colas y estrés sectorial | 28 | 28 | 0 | 28 | 0 | 0 | 0 | 91,7 |
| TMB-10 | Análisis input-output y redes de cadena de suministro | 25 | 25 | 0 | 21 | 4 | 0 | 0 | 85,4 |
| TMB-11 | Evaluación predictiva, calibración y backtesting de selección | 29 | 29 | 0 | 26 | 3 | 0 | 0 | 88,3 |
| TMB-12 | Aprendizaje automático y análisis de texto para mercados | 30 | 30 | 0 | 28 | 2 | 0 | 0 | 88,8 |
| TMB-13 | Decisión multicriterio y agregación de juicio experto | 28 | 28 | 0 | 22 | 6 | 0 | 0 | 83,9 |
| TMB-14 | Datos, calidad y reproducibilidad | 30 | 30 | 0 | 28 | 2 | 0 | 0 | 88,2 |
| **Total** | — | **410** | **410** | 0 | 334 | 71 | 5 | 0 | 85,8 |

«Verificadas»: enlace en estado OK, REDIRIGIDO, MURO_PAGO o VERIFICADO_BUSQUEDA (existencia y datos confirmados por búsqueda web el 02/11/2026), o verificación documental completa en una carga anterior (25–26/10/2026), pendiente solo del barrido automático HT-02. «Pendientes»: semillas aún en PENDIENTE_VERIFICACION_ALTA o fichas con alerta sin resolver.

## Novedades

- 02/11/2026: emisión V2.0 del archivo (primera con fichas verificadas).

## TMB-01 Estadística y series temporales aplicadas a sectores

#### DOC-MOT-0029 · Q 95 (A) — Why You Should Never Use the Hodrick-Prescott Filter

- **Autores:** James D. Hamilton
- **Año:** 2018
- **Publicación o institución:** The Review of Economics and Statistics, 100(5), 831-843 (MIT Press); versión de trabajo NBER WP 23429 (2017)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-01 Estadística y series temporales aplicadas a sectores (principal) · secundarias: TMB-02
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI: 10.1162/rest_a_00706 · https://www.nber.org/papers/w23429 · https://ideas.repec.org/a/tpr/restat/v100y2018i5p831-843.html
- **Acceso y licencia:** Documento de trabajo NBER (DOI 10.3386/w23429) y copia del autor (econweb.ucsd.edu) localizables; revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Hamilton 2018 "Why You Should Never Use the Hodrick-Prescott Filter" Review of Economics and Statistics»; WebFetch: sí)
- **Contenido:** Muestra que el filtro HP genera dinámicas espurias, valores de final de muestra distintos de los intermedios y un λ incoherente con los datos; propone como alternativa la regresión de y(t+h) sobre sus 4 últimos valores (h = 8 trimestres), cuyo residuo es el ciclo.
- **Uso en el Motor:** AG-B16, MC-B01: alternativa al filtro HP para separar tendencia y ciclo de series de producción o ventas sectoriales (AG-B08 Macro y Ciclo).
- **Limitaciones:** Propuesta discutida en la literatura posterior (véanse DOC-MOT-0204 y DOC-MOT-0205).
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02 (DOI confirmado).

#### DOC-MOT-0025 · Q 95 (A) — Computation and Analysis of Multiple Structural Change Models

- **Autores:** Jushan Bai; Pierre Perron
- **Año:** 2003
- **Publicación o institución:** Journal of Applied Econometrics, 18(1), 1-22
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-01 Estadística y series temporales aplicadas a sectores (principal) · secundarias: —
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1002/jae.659 · https://ideas.repec.org/a/jae/japmet/v18y2003i1p1-22.html
- **Acceso y licencia:** Ficha RePEc abierta; texto Wiley por suscripción; versión de trabajo (Montréal 9807) listada en RePEc
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Bai Perron 2003 "Computation and analysis of multiple structural change models" Journal of Applied Econometrics 10.1002/jae.659»; WebFetch: sí)
- **Contenido:** Algoritmo de programación dinámica para obtener las particiones de mínima suma de cuadrados con O(T²) operaciones, valores críticos ampliados, intervalos de confianza de las fechas y guía práctica de especificación.
- **Uso en el Motor:** AG-B16, MC-B01: datación de varias rupturas estructurales en series sectoriales (cambios de régimen de demanda, regulación o tecnología) para AG-B13 Prospectiva y AG-B07.
- **Limitaciones:** Coste computacional con muchas rupturas y regresores fijos entre regímenes (iterativo, sin óptimo garantizado).
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02 (DOI confirmado).

#### DOC-MOT-0024 · Q 95 (A) — Estimating and Testing Linear Models with Multiple Structural Changes

- **Autores:** Jushan Bai; Pierre Perron
- **Año:** 1998
- **Publicación o institución:** Econometrica, 66(1), 47-78
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-01 Estadística y series temporales aplicadas a sectores (principal) · secundarias: —
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** https://ideas.repec.org/a/ecm/emetrp/v66y1998i1p47-78.html · registro de la Econometric Society: https://www.econometricsociety.org/publications/econometrica/1998/01/01/estimating-and-testing-linear-models-multiple-structural (DOI no visto)
- **Acceso y licencia:** Ficha RePEc abierta; texto en Econometrica/JSTOR por suscripción (versión de trabajo del Département de sciences économiques de Montréal listada en RePEc)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Bai Perron 1998 "Estimating and Testing Linear Models with Multiple Structural Changes" Econometrica 66»; WebFetch: sí)
- **Contenido:** Teoría asintótica para estimar por mínimos cuadrados múltiples rupturas en fechas desconocidas, con contrastes supF, doble máximo (UDmax, WDmax) y secuencial ℓ frente a ℓ+1 para determinar el número de rupturas.
- **Uso en el Motor:** AG-B16, MC-B01: contraste y estimación de rupturas múltiples en la tendencia de un sector antes de extrapolarla.
- **Limitaciones:** Requiere tamaño mínimo de segmento (trimming); potencia baja con rupturas pequeñas; valores críticos no válidos con regresores no estacionarios. El DOI de la semilla (10.2307/2998540) no se ha visto y se retira.
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02.

#### DOC-MOT-0253 · Q 95 (A) — Tests for Parameter Instability and Structural Change with Unknown Change Point

- **Autores:** Donald W. K. Andrews
- **Año:** 1993
- **Publicación o institución:** Econometrica, 61(4), 821-856 (corrigendum: Econometrica 71(1), 2003, 395-397)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-01 Estadística y series temporales aplicadas a sectores (principal) · secundarias: —
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.2307/2951764 · Verificada en página índice: https://en.wikipedia.org/wiki/Structural_break
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Structural break wikipedia Chow test Andrews 1993 Zivot Andrews Bai Perron references»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Structural_break)
- **Contenido:** Contrastes supremo (sup-Wald, sup-LM, sup-LR) de una ruptura en fecha desconocida, con valores críticos asintóticos según el recorte.
- **Uso en el Motor:** AG-B16, MC-B01: contraste de inestabilidad de parámetros con fecha de ruptura desconocida en relaciones sector-ciclo (AG-B08).
- **Limitaciones:** Una sola ruptura; véase Bai-Perron para varias. Confirmada solo mediante página índice (bibliografía de Wikipedia «Structural break»); pendiente de lectura de la fuente primaria.

#### DOC-MOT-0027 · Q 94 (A) — Testing the Null Hypothesis of Stationarity against the Alternative of a Unit Root

- **Autores:** Denis Kwiatkowski; Peter C. B. Phillips; Peter Schmidt; Yongcheol Shin
- **Año:** 1992
- **Publicación o institución:** Journal of Econometrics, 54(1-3), 159-178; versión de trabajo: Cowles Foundation Discussion Paper 979 (1991)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-01 Estadística y series temporales aplicadas a sectores (principal) · secundarias: TMB-02
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** https://econpapers.repec.org/RePEc:cwl:cwldpp:979 (DOI no visto)
- **Acceso y licencia:** Documento de trabajo de Cowles (Yale) de acceso libre; revista Elsevier por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Kwiatkowski Phillips Schmidt Shin 1992 "Testing the null hypothesis of stationarity against the alternative of a unit root" Journal of Econometrics 54»; WebFetch: sí)
- **Contenido:** Contraste LM (KPSS) con hipótesis nula de estacionariedad en nivel o alrededor de tendencia, basado en sumas parciales de residuos y varianza de largo plazo con núcleo de Bartlett.
- **Uso en el Motor:** AG-B16, MC-B01: contraste KPSS de estacionariedad previo a modelizar series sectoriales en niveles o diferencias.
- **Limitaciones:** Sensible a la elección del ancho de banda; distorsiones de tamaño con alta persistencia. La versión de trabajo de Cowles figura con tres autores; la publicada añade a Y. Shin. El DOI de la semilla no se ha visto y se retira.
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02.

#### DOC-MOT-0026 · Q 93 (A) — Distribution of the Estimators for Autoregressive Time Series with a Unit Root

- **Autores:** David A. Dickey; Wayne A. Fuller
- **Año:** 1979
- **Publicación o institución:** Journal of the American Statistical Association, 74(366), 427-431
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-01 Estadística y series temporales aplicadas a sectores (principal) · secundarias: TMB-02
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** https://bigenc.ru/b/distribution-of-the-estimators-for-autoregressive-024b8d (ficha bibliográfica; DOI no visto)
- **Acceso y licencia:** Revista (Taylor & Francis/JSTOR) por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Dickey Fuller 1979 "Distribution of the Estimators for Autoregressive Time Series with a Unit Root" JASA 74 366»; WebFetch: sí)
- **Contenido:** Obtiene la distribución límite no estándar del estimador MCO y del estadístico t en un AR(1) con raíz unitaria (con y sin constante y tendencia): base del contraste Dickey-Fuller.
- **Uso en el Motor:** AG-B16, MC-B01: contraste Dickey-Fuller de raíz unitaria en series de ventas, precios o capacidad sectorial.
- **Limitaciones:** Baja potencia en muestras cortas y ante rupturas; combinar con KPSS. El DOI de la semilla no se ha visto y se retira; la URL es una ficha bibliográfica, no el texto.
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02.

#### DOC-MOT-0020 · Q 92 (A) — Forecasting: Principles and Practice (3.ª ed.)

- **Autores:** Rob J. Hyndman; George Athanasopoulos
- **Año:** 2021
- **Publicación o institución:** OTexts (libro en línea abierto, con edición impresa)
- **Tipo de documento:** Manual de referencia
- **Temática:** TMB-01 Estadística y series temporales aplicadas a sectores (principal) · secundarias: TMB-11
- **Calidad Q:** 92 (A) — Tipo 20/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** ISBN: 9780987507136 · https://ci.nii.ac.jp/ncid/BC10558540 · libro en línea enlazado desde el paquete CRAN fpp3: https://OTexts.com/fpp3/
- **Acceso y licencia:** Acceso abierto en línea (OTexts); paquete de datos fpp3 en CRAN
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «"Forecasting: Principles and Practice" 3rd edition Hyndman Athanasopoulos 2021»; WebFetch: sí (CiNii y página CRAN de fpp3; otexts.com no admitido por WebFetch))
- **Contenido:** Manual de previsión: descomposición STL, suavizado exponencial (ETS), ARIMA, regresión dinámica, previsión jerárquica, validación cruzada temporal y métricas de precisión, con código R (fable/tsibble).
- **Uso en el Motor:** AG-B16, MC-B01: descomposición, ETS, ARIMA y validación cruzada temporal de series sectoriales (ventas, producción, precios) que piden AG-B04 Demanda y Adopción y AG-B08 Macro y Ciclo.
- **Limitaciones:** Orientado a previsión univariante y de negocio; el texto en otexts.com no pudo leerse con WebFetch (dominio no admitido).
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02 (título, autores, edición, editorial, año e ISBN en CiNii).

#### DOC-MOT-0255 · Q 92 (A) — Trends and Random Walks in Macroeconomic Time Series: Some Evidence and Implications

- **Autores:** Charles R. Nelson; Charles I. Plosser
- **Año:** 1982
- **Publicación o institución:** Journal of Monetary Economics, 10(2), 139-162
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-01 Estadística y series temporales aplicadas a sectores (principal) · secundarias: —
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1016/0304-3932(82)90012-5 · Verificada en página índice: https://en.wikipedia.org/wiki/Cointegration
- **Acceso y licencia:** Revista Elsevier por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Cointegration wikipedia Engle-Granger Johansen test Phillips-Ouliaris references»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Cointegration)
- **Contenido:** Aplica contrastes Dickey-Fuller a 14 series macro de EE. UU. y no rechaza raíz unitaria en la mayoría: tendencias estocásticas frente a deterministas.
- **Uso en el Motor:** AG-B16, MC-B01: discriminar tendencia determinista y estocástica antes de proyectar el crecimiento de un mercado (AG-B04, AG-B13).
- **Limitaciones:** Conclusiones discutidas con rupturas (Perron 1989). Título completo en la publicación; el índice lo abrevia. Confirmada solo mediante página índice (bibliografía de Wikipedia «Cointegration»); pendiente de lectura de la fuente primaria.

#### DOC-MOT-0023 · Q 92 (A) — Estimates of the Regression Coefficient Based on Kendall's Tau

- **Autores:** Pranab Kumar Sen
- **Año:** 1968
- **Publicación o institución:** Journal of the American Statistical Association, 63(324), 1379-1389
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-01 Estadística y series temporales aplicadas a sectores (principal) · secundarias: —
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1080/01621459.1968.10480934 · https://mathworld.wolfram.com/Theil-SenEstimator.html (cita con DOI)
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Sen 1968 "Estimates of the Regression Coefficient Based on Kendall's Tau" Journal of the American Statistical Association 63»; WebFetch: sí)
- **Contenido:** Estimador de la pendiente como mediana de las pendientes entre todos los pares (Theil-Sen), con intervalo de confianza basado en la tau de Kendall; robusto a atípicos.
- **Uso en el Motor:** AG-B16, MC-B01: pendiente robusta de Theil-Sen para estimar el crecimiento tendencial de series sectoriales cortas o con atípicos.
- **Limitaciones:** Supone tendencia lineal; los intervalos suponen independencia.
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02 (DOI confirmado).

#### DOC-MOT-0021 · Q 92 (A) — Nonparametric Tests Against Trend

- **Autores:** Henry B. Mann
- **Año:** 1945
- **Publicación o institución:** Econometrica, 13(3), 245-259
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-01 Estadística y series temporales aplicadas a sectores (principal) · secundarias: —
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** https://intouch.econometricsociety.org/publications/econometrica/1945/07/01/nonparametric-tests-against-trend · JSTOR estable 1907187 (DOI no visto)
- **Acceso y licencia:** Registro abierto de la Econometric Society; texto vía JSTOR
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Mann 1945 "Nonparametric Tests Against Trend" Econometrica 13 245-259»; WebFetch: sí)
- **Contenido:** Propone el estadístico S (número de pares concordantes menos discordantes en el tiempo) como prueba no paramétrica de tendencia monótona: origen de la prueba de Mann-Kendall.
- **Uso en el Motor:** AG-B16, MC-B01: contraste no paramétrico de Mann-Kendall de tendencia monótona en indicadores sectoriales (adopción, cuotas, márgenes).
- **Limitaciones:** Sin control del error tipo I con autocorrelación (véase DOC-MOT-0202). El DOI de la semilla no se ha visto y se retira.
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02.

#### DOC-MOT-0257 · Q 91 (A) — On Adjusting the Hodrick-Prescott Filter for the Frequency of Observations

- **Autores:** Morten O. Ravn; Harald Uhlig
- **Año:** 2002
- **Publicación o institución:** The Review of Economics and Statistics, 84(2), 371-376
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-01 Estadística y series temporales aplicadas a sectores (principal) · secundarias: —
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** Verificada en página índice: https://cran.r-universe.dev/lpirfs/doc/manual.html
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Jordà 2005 "Estimation and Inference of Impulse Responses by Local Projections" American Economic Review 95»; WebFetch: sí, sobre la página índice https://cran.r-universe.dev/lpirfs/doc/manual.html)
- **Contenido:** Regla de ajuste de λ del filtro HP según la frecuencia (multiplicar por la cuarta potencia del cambio de frecuencia: λ≈6,25 anual, 129 600 mensual).
- **Uso en el Motor:** AG-B16, MC-B01: ajuste del parámetro del filtro HP a la frecuencia (mensual, trimestral, anual) de las series sectoriales.
- **Limitaciones:** Confirmada solo mediante página índice (bibliografía de manual de lpirfs); pendiente de lectura de la fuente primaria.

#### DOC-MOT-0031 · Q 91 (A) — Continuous Inspection Schemes

- **Autores:** E. S. Page
- **Año:** 1954
- **Publicación o institución:** Biometrika, 41(1-2), 100-115
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-01 Estadística y series temporales aplicadas a sectores (principal) · secundarias: TMB-11
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1093/biomet/41.1-2.100 · https://academic.oup.com/biomet/issue/41/1-2
- **Acceso y licencia:** Oxford Academic, suscripción
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Page 1954 "Continuous Inspection Schemes" Biometrika 41 100-115»; WebFetch: sí, índice del número)
- **Contenido:** Introduce el CUSUM: suma acumulada de desviaciones respecto a un valor de referencia con regla de alarma por umbral, para detectar de forma secuencial cambios en la media.
- **Uso en el Motor:** AG-B16, MC-B01: CUSUM para vigilar cambios de nivel en indicadores sectoriales seguidos por AG-B10 Flujos y Sentimiento y AG-B13.
- **Limitaciones:** Requiere fijar umbrales y tamaño de cambio de referencia; supuestos de independencia.
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02 (DOI confirmado).

#### MBM-0001 · Q 90 (A) — Automatic Time Series Forecasting: The forecast Package for R

- **Autores:** Rob J. Hyndman; Yeasmin Khandakar
- **Año:** 2008
- **Publicación o institución:** Journal of Statistical Software, 27(3), 1-22
- **Tipo de documento:** Artículo revisado por pares (software estadístico)
- **Temática:** TMB-01 Estadística y series temporales aplicadas a sectores (principal) · secundarias: TMB-14
- **Calidad Q:** 90 (A) — Tipo 22/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 8/10 · Impacto 10/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** DOI: 10.18637/jss.v027.i03 · https://www.jstatsoft.org/article/view/v027i03
- **Acceso y licencia:** Acceso abierto (JSS, CC BY)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Hyndman Khandakar 2008 "Automatic time series forecasting: the forecast package for R" Journal of Statistical Software»; WebFetch: sí)
- **Contenido:** Describe los algoritmos automáticos de selección de modelos ETS y ARIMA (auto.arima: contrastes de raíz unitaria, búsqueda escalonada por AICc) implementados en el paquete forecast.
- **Uso en el Motor:** AG-B16, MC-B01: previsión automática y reproducible de muchas series sectoriales a la vez (ventas, producción, precios) para AG-B04 Demanda y Adopción y AG-B08 Macro y Ciclo.
- **Limitaciones:** Univariante; la selección automática no sustituye el juicio sobre rupturas estructurales.

#### DOC-MOT-0254 · Q 90 (A) — The New Econometrics of Structural Change: Dating Breaks in U.S. Labor Productivity

- **Autores:** Bruce E. Hansen
- **Año:** 2001
- **Publicación o institución:** Journal of Economic Perspectives, 15(4), 117-128
- **Tipo de documento:** Artículo revisado por pares (divulgativo-técnico)
- **Temática:** TMB-01 Estadística y series temporales aplicadas a sectores (principal) · secundarias: —
- **Calidad Q:** 90 (A) — Tipo 23/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** DOI: 10.1257/jep.15.4.117 · Verificada en página índice: https://en.wikipedia.org/wiki/Structural_break · ficha IDEAS https://ideas.repec.org:443/a/aea/jecper/v15y2001i4p117-128.html
- **Acceso y licencia:** JEP de acceso abierto en la web de la AEA
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Structural break wikipedia Chow test Andrews 1993 Zivot Andrews Bai Perron references»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Structural_break)
- **Contenido:** Introducción aplicada a contrastes de ruptura (Chow, Andrews, Bai-Perron) e intervalos de fechas, con aplicación a la productividad de EE. UU.
- **Uso en el Motor:** AG-B16, MC-B01: aplicación de referencia de datación de rupturas a productividad, útil para series de productividad sectorial (AG-B05, AG-B06).
- **Limitaciones:** Confirmada solo mediante página índice (bibliografía de Wikipedia «Structural break»); pendiente de lectura de la fuente primaria.

#### DOC-MOT-0028 · Q 90 (A) — Postwar U.S. Business Cycles: An Empirical Investigation

- **Autores:** Robert J. Hodrick; Edward C. Prescott
- **Año:** 1997
- **Publicación o institución:** Journal of Money, Credit and Banking, 29(1), 1-16
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-01 Estadística y series temporales aplicadas a sectores (principal) · secundarias: TMB-02
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** https://ideas.repec.org/a/mcb/jmoncb/v29y1997i1p1-16.html (DOI no visto)
- **Acceso y licencia:** Ficha RePEc abierta; versión de trabajo (Northwestern CMS-EMS 451) listada en RePEc; revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Hodrick Prescott 1997 "Postwar U.S. Business Cycles: An Empirical Investigation" Journal of Money, Credit and Banking 29»; WebFetch: sí)
- **Contenido:** Formaliza el filtro HP: tendencia que minimiza la suma de cuadrados del ciclo más λ veces la suma de cuadrados de las segundas diferencias de la tendencia (λ = 1600 trimestral).
- **Uso en el Motor:** AG-B16, MC-B01: filtro HP clásico para el componente cíclico de la producción sectorial (AG-B08), con las cautelas de DOC-MOT-0029.
- **Limitaciones:** Efecto de final de muestra y ciclos espurios (DOC-MOT-0029); vigencia reducida para uso en tiempo real. El DOI de la semilla no se ha visto y se retira.
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02.

#### DOC-MOT-0256 · Q 88 (A) — bcp: An R Package for Performing a Bayesian Analysis of Change Point Problems

- **Autores:** Chandra Erdman; John W. Emerson
- **Año:** 2007
- **Publicación o institución:** Journal of Statistical Software, 23(3)
- **Tipo de documento:** Artículo revisado por pares (software)
- **Temática:** TMB-01 Estadística y series temporales aplicadas a sectores (principal) · secundarias: —
- **Calidad Q:** 88 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 12/15 · Vigencia 9/10 · Impacto 7/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** DOI: 10.18637/jss.v023.i03 · Verificada en página índice: https://en.wikipedia.org/wiki/Structural_break
- **Acceso y licencia:** Acceso abierto (JSS)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Structural break wikipedia Chow test Andrews 1993 Zivot Andrews Bai Perron references»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Structural_break)
- **Contenido:** Implementación del análisis bayesiano de puntos de cambio de Barry-Hartigan con probabilidades posteriores de cambio en cada instante.
- **Uso en el Motor:** AG-B16, MC-B01: análisis bayesiano de puntos de cambio en series sectoriales con probabilidad posterior de ruptura.
- **Limitaciones:** Confirmada solo mediante página índice (bibliografía de Wikipedia «Structural break»); pendiente de lectura de la fuente primaria.

#### MBM-0002 · Q 88 (A) — A State Space Framework for Automatic Forecasting Using Exponential Smoothing Methods

- **Autores:** Rob J. Hyndman; Anne B. Koehler; Ralph D. Snyder; Simone Grose
- **Año:** 2002
- **Publicación o institución:** International Journal of Forecasting, 18(3), 439-454
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-01 Estadística y series temporales aplicadas a sectores (principal) · secundarias: —
- **Calidad Q:** 88 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 7/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de Hyndman y Khandakar 2008): https://anorien.csc.warwick.ac.uk/CRAN/web/packages/forecast/vignettes/JSS2008.pdf
- **Acceso y licencia:** Artículo de pago (Elsevier)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Hyndman Khandakar 2008 "Automatic time series forecasting: the forecast package for R" Journal of Statistical Software»; WebFetch: sí, sobre la bibliografía del PDF índice)
- **Contenido:** Formula los métodos de suavizado exponencial como modelos de espacio de estados con error aditivo o multiplicativo, lo que permite verosimilitud, selección por criterio de información e intervalos de predicción.
- **Uso en el Motor:** AG-B16, MC-B01: base de los modelos ETS para proyectar series sectoriales con tendencia y estacionalidad e intervalos coherentes.
- **Limitaciones:** Confirmada solo por bibliografía; univariante.

#### DOC-MOT-0019 · Q 88 (A) — Time Series Analysis

- **Autores:** James D. Hamilton
- **Año:** 1994
- **Publicación o institución:** Princeton University Press
- **Tipo de documento:** Manual de referencia
- **Temática:** TMB-01 Estadística y series temporales aplicadas a sectores (principal) · secundarias: TMB-02
- **Calidad Q:** 88 (A) — Tipo 20/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** ISBN: 978-0-691-04289-3 · verificada en páginas índice: https://en.wikipedia.org/wiki/Newey%E2%80%93West_estimator · https://www.wiwiss.fu-berlin.de/fachbereich/vwl/luetkepohl/Lehrveranstaltungen/MTSA_SS2016.pdf
- **Acceso y licencia:** Libro de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Newey–West estimator wikipedia heteroskedasticity and autocorrelation consistent Andrews 1991 bandwidth»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Newey%E2%80%93West_estimator)
- **Contenido:** Manual de series temporales: ARMA, raíces unitarias, VAR, cointegración, GMM, filtro de Kalman, estimación HAC y cambio de régimen markoviano.
- **Uso en el Motor:** AG-B16, MC-B01: manual de base para ARMA, VAR, cointegración y filtros aplicados a series sectoriales.
- **Limitaciones:** No cubre desarrollos posteriores a 1994 (volatilidad realizada, proyecciones locales). Confirmada solo mediante página índice (bibliografía de Wikipedia «Newey–West estimator» y programa docente de H. Lütkepohl, FU Berlin); pendiente de lectura de la fuente primaria.
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02 (ISBN confirmado en índice).

#### MBM-0005 · Q 87 (A) — Optimal Forecast Reconciliation for Hierarchical and Grouped Time Series Through Trace Minimization

- **Autores:** Shanika L. Wickramasuriya; George Athanasopoulos; Rob J. Hyndman
- **Año:** 2019
- **Publicación o institución:** Journal of the American Statistical Association, 114(526), 804-819
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-01 Estadística y series temporales aplicadas a sectores (principal) · secundarias: TMB-11
- **Calidad Q:** 87 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 0/10
- **DOI / ISBN / URL:** DOI: 10.1080/01621459.2018.1448825 · https://research.monash.edu/en/publications/optimal-forecast-reconciliation-for-hierarchical-and-grouped-time/
- **Acceso y licencia:** Artículo de pago; documento de trabajo previo de Monash en abierto
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Wickramasuriya Athanasopoulos Hyndman 2019 "Optimal forecast reconciliation for hierarchical and grouped time series through trace minimization"»; WebFetch: sí)
- **Contenido:** Método MinT de conciliación de previsiones jerárquicas que usa la matriz de covarianzas completa de los errores y produce previsiones coherentes e insesgadas de varianza mínima.
- **Uso en el Motor:** AG-B16, MC-B01: hacer coherentes las previsiones de mercado total, subsectores, regiones y segmentos (la suma de partes cuadra con el total) en el dimensionado de AG-B04 y MC-B02.
- **Limitaciones:** Requiere estimar covarianzas con muchas series; el texto completo es de pago.

#### MBM-0003 · Q 86 (A) — Forecasting with Exponential Smoothing: The State Space Approach

- **Autores:** Rob J. Hyndman; Anne B. Koehler; J. Keith Ord; Ralph D. Snyder
- **Año:** 2008
- **Publicación o institución:** Springer-Verlag (Springer Series in Statistics)
- **Tipo de documento:** Monografía de referencia
- **Temática:** TMB-01 Estadística y series temporales aplicadas a sectores (principal) · secundarias: —
- **Calidad Q:** 86 (A) — Tipo 22/25 · Rigor 18/20 · Autoridad 14/15 · Vigencia 7/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de Hyndman y Khandakar 2008): https://anorien.csc.warwick.ac.uk/CRAN/web/packages/forecast/vignettes/JSS2008.pdf
- **Acceso y licencia:** Libro de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Hyndman Khandakar 2008 "Automatic time series forecasting: the forecast package for R" Journal of Statistical Software»; WebFetch: sí, sobre la bibliografía del PDF índice)
- **Contenido:** Tratamiento completo de la taxonomía ETS (error, tendencia, estacionalidad), estimación, selección de modelos e intervalos de predicción.
- **Uso en el Motor:** AG-B16, MC-B01: referencia teórica para elegir entre tendencia amortiguada, aditiva o multiplicativa al proyectar un mercado.
- **Limitaciones:** Técnico; sin covariables.

#### DOC-MOT-0030 · Q 86 (A) — STL: A Seasonal-Trend Decomposition Procedure Based on Loess

- **Autores:** Robert B. Cleveland; William S. Cleveland; Jean E. McRae; Irma Terpenning
- **Año:** 1990
- **Publicación o institución:** Journal of Official Statistics, 6(1), 3-73 (Statistics Sweden)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-01 Estadística y series temporales aplicadas a sectores (principal) · secundarias: —
- **Calidad Q:** 86 (A) — Tipo 22/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** Verificada en página índice: https://www.statsmodels.org/v0.14.4/generated/statsmodels.tsa.seasonal.STL.html (cita completa en la documentación de statsmodels STL)
- **Acceso y licencia:** Revista de acceso abierto (JOS); enlace directo al texto no obtenido en esta verificación
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Cleveland 1990 "STL: A Seasonal-Trend Decomposition Procedure Based on Loess" Journal of Official Statistics»; WebFetch: sí, sobre la página índice https://www.statsmodels.org/v0.14.4/generated/statsmodels.tsa.seasonal.STL.html)
- **Contenido:** Descomposición iterativa de una serie en estacionalidad, tendencia y resto mediante suavizados loess anidados, con versión robusta a atípicos.
- **Uso en el Motor:** AG-B16, MC-B01: descomposición STL estacional-tendencia de ventas y producción sectoriales mensuales.
- **Limitaciones:** No modela incertidumbre de la descomposición. Confirmada solo mediante página índice (bibliografía de statsmodels); pendiente de lectura de la fuente primaria.
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02.

#### MBM-0004 · Q 85 (A) — Time Series Analysis: Forecasting and Control (3.ª ed.)

- **Autores:** George E. P. Box; Gwilym M. Jenkins; Gregory C. Reinsel
- **Año:** 1994
- **Publicación o institución:** Prentice Hall (Englewood Cliffs, N.J.)
- **Tipo de documento:** Manual de referencia
- **Temática:** TMB-01 Estadística y series temporales aplicadas a sectores (principal) · secundarias: —
- **Calidad Q:** 85 (A) — Tipo 22/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 5/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** ISBN: 0130607746 · https://bemis2.marmot.org/Record/.b17751263
- **Acceso y licencia:** Libro de pago (existen ediciones posteriores en Wiley)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Box–Jenkins method Wikipedia "Time Series Analysis: Forecasting and Control"»; WebFetch: sí, registro de catálogo)
- **Contenido:** Obra fundacional de la metodología Box-Jenkins: identificación, estimación y diagnóstico de modelos ARIMA y ARIMA estacionales, función de transferencia y control.
- **Uso en el Motor:** AG-B16, MC-B01: identificación ARIMA/SARIMA de series sectoriales y modelos de función de transferencia (p. ej., respuesta de la demanda sectorial a un indicador adelantado).
- **Limitaciones:** Edición de 1994; el registro de catálogo muestra una discrepancia menor de edición en la descripción.

#### DOC-MOT-0202 · Q 84 (A) — Permutation Testing for Monotone Trend

- **Autores:** Joseph P. Romano; Marius A. Tirlea
- **Año:** 2024
- **Publicación o institución:** arXiv:2404.06239 [math.ST] (Stanford University)
- **Tipo de documento:** Documento de trabajo (preprint)
- **Temática:** TMB-01 Estadística y series temporales aplicadas a sectores (principal) · secundarias: —
- **Calidad Q:** 84 (A) — Tipo 18/25 · Rigor 18/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 4/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://arxiv.org/pdf/2404.06239
- **Acceso y licencia:** Acceso abierto (arXiv)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Mann 1945 "Nonparametric Tests Against Trend" Econometrica 13 245-259»; WebFetch: sí)
- **Contenido:** Demuestra que el Mann-Kendall clásico no controla el error tipo I con dependencia (sobrerrechaza con autocorrelación positiva) y propone pruebas de permutación con el estadístico studentizado (varianza HAC truncada), exactas con datos i.i.d. y asintóticamente válidas con dependencia; añade estadísticos «locales» de tendencia.
- **Uso en el Motor:** AG-B16, MC-B01: contraste por permutación de tendencia monótona con series sectoriales cortas.
- **Limitaciones:** Preprint sin publicación en revista constatada; supone estacionariedad con mezcla β.

#### DOC-MOT-0203 · Q 83 (A) — A Unified Approach to Nonparametric Trend Tests for Dependent and Independent Samples

- **Autores:** Arne C. Bathke
- **Año:** 2009
- **Publicación o institución:** Metrika, 69, 17-29 (Springer)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-01 Estadística y series temporales aplicadas a sectores (principal) · secundarias: —
- **Calidad Q:** 83 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 12/15 · Vigencia 9/10 · Impacto 5/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.1007/s00184-008-0171-x · https://link.springer.com/doi/10.1007/s00184-008-0171-x
- **Acceso y licencia:** Springer, suscripción (resumen abierto)
- **Estado:** Aprobada
- **Estado del enlace:** MURO_PAGO
- **Última verificación:** 2026-11-02 (búsqueda web: «Mann 1945 "Nonparametric Tests Against Trend" Econometrica 13 245-259»; WebFetch: sí)
- **Contenido:** Marco único de pruebas no paramétricas frente a alternativas ordenadas para muestras dependientes e independientes, aplicable a datos cuantitativos, ordinales y binarios, invariante a transformaciones monótonas.
- **Uso en el Motor:** AG-B16, MC-B01: contrastes de tendencia no paramétricos válidos con dependencia serial en series sectoriales.
- **Limitaciones:** Orientado a diseños factoriales más que a series temporales largas.

#### DOC-MOT-0204 · Q 82 (A) — Why You Should Never Use the Hodrick-Prescott Filter: Comment

- **Autores:** Alban Moura
- **Año:** 2022
- **Publicación o institución:** Banque centrale du Luxembourg, Cahier d'études n.º 162 (agosto de 2022)
- **Tipo de documento:** Documento de trabajo de banco central
- **Temática:** TMB-01 Estadística y series temporales aplicadas a sectores (principal) · secundarias: —
- **Calidad Q:** 82 (A) — Tipo 20/25 · Rigor 16/20 · Autoridad 12/15 · Vigencia 9/10 · Impacto 5/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://www.bcl.lu/en/publications/Working-papers/162/BCLWP162.pdf
- **Acceso y licencia:** Acceso abierto (Banque centrale du Luxembourg)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Hamilton 2018 "Why You Should Never Use the Hodrick-Prescott Filter" Review of Economics and Statistics»; WebFetch: sí)
- **Contenido:** Réplica a Hamilton (2018): el ciclo del filtro de Hamilton (error de previsión a varios pasos) muestra persistencia y predictibilidad análogas a las del ciclo HP y su tendencia va retrasada respecto a los datos por construcción.
- **Uso en el Motor:** AG-B16, MC-B01: réplica crítica a Hamilton para elegir filtro de ciclo sectorial con criterio (AG-B14 Contrarias).
- **Limitaciones:** Documento de trabajo; las opiniones no comprometen al BCL.

#### DOC-MOT-0205 · Q 82 (A) — Does Hamilton's OLS Regression Provide a "Better Alternative" to the Hodrick-Prescott Filter? A New Zealand Business Cycle Perspective

- **Autores:** Viv B. Hall; Peter Thomson
- **Año:** 2020
- **Publicación o institución:** CAMA Working Paper 71/2020, Crawford School of Public Policy, The Australian National University
- **Tipo de documento:** Documento de trabajo de institución académica
- **Temática:** TMB-01 Estadística y series temporales aplicadas a sectores (principal) · secundarias: —
- **Calidad Q:** 82 (A) — Tipo 20/25 · Rigor 16/20 · Autoridad 12/15 · Vigencia 9/10 · Impacto 5/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://crawford.anu.edu.au/sites/default/files/2025-01/71_2020_hall_thomson.pdf
- **Acceso y licencia:** Acceso abierto (ANU)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Hamilton 2018 "Why You Should Never Use the Hodrick-Prescott Filter" Review of Economics and Statistics»; WebFetch: sí)
- **Contenido:** Compara el filtro de Hamilton (H84) con HP1600 en el ciclo neozelandés: H84 exagera la volatilidad y da tendencias menos creíbles; los filtros HP extendidos con previsiones mejoran la estimación en los extremos de la muestra.
- **Uso en el Motor:** AG-B16, MC-B01: comparación HP frente a regresión de Hamilton para extraer el ciclo de un sector.
- **Limitaciones:** Evidencia de un solo país; documento de trabajo.

#### MBM-0013 · Q 82 (A) — Time Series Analysis by State Space Methods

- **Autores:** James Durbin; Siem Jan Koopman
- **Año:** 2001
- **Publicación o institución:** Oxford University Press (Oxford)
- **Tipo de documento:** Monografía de referencia
- **Temática:** TMB-01 Estadística y series temporales aplicadas a sectores (principal) · secundarias: —
- **Calidad Q:** 82 (A) — Tipo 22/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 5/10 · Impacto 10/10 · Independencia 10/10 · Acceso 1/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de Hyndman y Khandakar 2008): https://anorien.csc.warwick.ac.uk/CRAN/web/packages/forecast/vignettes/JSS2008.pdf
- **Acceso y licencia:** Libro de pago (hay 2.ª ed. de 2012)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Hyndman Khandakar 2008 "Automatic time series forecasting…"»; WebFetch: sí, sobre la bibliografía del PDF índice)
- **Contenido:** Modelos de componentes no observados y filtro de Kalman: tendencia local, estacionalidad, datos faltantes y suavizado.
- **Uso en el Motor:** AG-B16, MC-B01: modelos estructurales de series sectoriales con huecos o frecuencias mixtas y nowcasting de indicadores sectoriales.
- **Limitaciones:** Exigente técnicamente.

#### MBM-0010 · Q 82 (A) — Seasonal Integration and Cointegration

- **Autores:** Svend Hylleberg; Robert F. Engle; Clive W. J. Granger; Byung Sam Yoo
- **Año:** 1990
- **Publicación o institución:** Journal of Econometrics, 44, 215-238
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-01 Estadística y series temporales aplicadas a sectores (principal) · secundarias: TMB-02
- **Calidad Q:** 82 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 4/10 · Impacto 10/10 · Independencia 10/10 · Acceso 0/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de Hyndman y Khandakar 2008): https://anorien.csc.warwick.ac.uk/CRAN/web/packages/forecast/vignettes/JSS2008.pdf
- **Acceso y licencia:** Artículo de pago (Elsevier)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Hyndman Khandakar 2008 "Automatic time series forecasting…"»; WebFetch: sí, sobre la bibliografía del PDF índice)
- **Contenido:** Contraste HEGY de raíces unitarias estacionales y concepto de cointegración estacional.
- **Uso en el Motor:** AG-B16, MC-B01: decidir si la estacionalidad de una serie sectorial es estable o estocástica (diferencia estacional o no).
- **Limitaciones:** Confirmada solo por bibliografía.

#### DOC-MOT-0022 · Q 81 (A) — Rank Correlation Methods (4.ª ed.)

- **Autores:** Maurice G. Kendall
- **Año:** 1970 (4.ª ed.; a menudo citada por la reimpresión de 1975)
- **Publicación o institución:** Charles Griffin, Londres
- **Tipo de documento:** Libro académico
- **Temática:** TMB-01 Estadística y series temporales aplicadas a sectores (principal) · secundarias: —
- **Calidad Q:** 81 (A) — Tipo 20/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 9/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** ISBN: 0852641990 · https://ci.nii.ac.jp/ncid/BA00860250 · https://search.worldcat.org/oclc/136868
- **Acceso y licencia:** Libro descatalogado; acceso en bibliotecas
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Kendall "Rank Correlation Methods" 4th edition 1970 OR 1975 Griffin London»; WebFetch: sí)
- **Contenido:** Monografía sobre la tau de Kendall y la rho de Spearman: distribución exacta y asintótica, tratamiento de empates, concordancia y contrastes basados en rangos; base teórica de la prueba de Mann-Kendall.
- **Uso en el Motor:** AG-B16, MC-B01: base teórica de la correlación de rangos de Kendall para tendencias y para comparar rankings sectoriales.
- **Limitaciones:** Edición antigua de acceso limitado. Corrección: la 4.ª edición es de 1970 según CiNii y WorldCat (la semilla indicaba 1975, fecha de reimpresión habitual en las citas).
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02 (año corregido).

#### MBM-0006 · Q 80 (A) — Fast Computation of Reconciled Forecasts for Hierarchical and Grouped Time Series

- **Autores:** Rob J. Hyndman; Alan J. Lee; Earo Wang
- **Año:** 2016
- **Publicación o institución:** Computational Statistics and Data Analysis, 97, 16-32
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-01 Estadística y series temporales aplicadas a sectores (principal) · secundarias: TMB-14
- **Calidad Q:** 80 (A) — Tipo 23/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 7/10 · Independencia 10/10 · Acceso 1/10
- **DOI / ISBN / URL:** Verificada en página índice (referencias de la documentación de hts::MinT): https://search.r-project.org/CRAN/refmans/hts/html/MinT.html
- **Acceso y licencia:** Artículo de pago (Elsevier)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Wickramasuriya Athanasopoulos Hyndman 2019 "Optimal forecast reconciliation…"»; WebFetch: sí, sobre la página índice)
- **Contenido:** Algoritmos eficientes para conciliar previsiones de jerarquías y agrupaciones grandes de series temporales.
- **Uso en el Motor:** AG-B16, MC-B01: conciliación a escala de previsiones por país × subsector × producto.
- **Limitaciones:** Confirmada solo por referencia bibliográfica.

#### MBM-0007 · Q 80 (A) — Exponential Smoothing: The State of the Art

- **Autores:** Everette S. Gardner Jr.
- **Año:** 1985
- **Publicación o institución:** Journal of Forecasting, 4, 1-28
- **Tipo de documento:** Artículo de revisión revisado por pares
- **Temática:** TMB-01 Estadística y series temporales aplicadas a sectores (principal) · secundarias: —
- **Calidad Q:** 80 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 13/15 · Vigencia 4/10 · Impacto 10/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de Hyndman y Khandakar 2008): https://anorien.csc.warwick.ac.uk/CRAN/web/packages/forecast/vignettes/JSS2008.pdf
- **Acceso y licencia:** Artículo de pago (Wiley)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Hyndman Khandakar 2008 "Automatic time series forecasting…"»; WebFetch: sí, sobre la bibliografía del PDF índice)
- **Contenido:** Revisión clásica de los métodos de suavizado exponencial (simple, Holt, Holt-Winters) y de su evidencia empírica.
- **Uso en el Motor:** AG-B16, MC-B01: elección de métodos simples y robustos para previsiones sectoriales de corto plazo.
- **Limitaciones:** Antigua; superada en formalización por MBM-0002.

#### MBM-0008 · Q 79 (B) — Forecasting Trends in Time Series

- **Autores:** Everette S. Gardner Jr.; Ed McKenzie
- **Año:** 1985
- **Publicación o institución:** Management Science, 31(10), 1237-1246
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-01 Estadística y series temporales aplicadas a sectores (principal) · secundarias: TMB-03
- **Calidad Q:** 79 (B) — Tipo 25/25 · Rigor 15/20 · Autoridad 13/15 · Vigencia 4/10 · Impacto 9/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de Hyndman y Khandakar 2008): https://anorien.csc.warwick.ac.uk/CRAN/web/packages/forecast/vignettes/JSS2008.pdf
- **Acceso y licencia:** Artículo de pago (INFORMS)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Hyndman Khandakar 2008 "Automatic time series forecasting…"»; WebFetch: sí, sobre la bibliografía del PDF índice)
- **Contenido:** Introduce la tendencia amortiguada en el suavizado exponencial, que evita extrapolar indefinidamente el crecimiento reciente.
- **Uso en el Motor:** AG-B16, MC-B01: proyecciones prudentes de crecimiento sectorial que se aplanan con el horizonte (contrapeso a la extrapolación lineal en AG-B13).
- **Limitaciones:** Confirmada solo por bibliografía.

#### DOC-MOT-0258 · Q 79 (B) — statsmodels: STL — Season-Trend Decomposition Using LOESS (documentación, v0.14.4)

- **Autores:** Equipo de desarrollo de statsmodels
- **Año:** Versión 0.14.4
- **Publicación o institución:** statsmodels.org
- **Tipo de documento:** Documentación técnica de software
- **Temática:** TMB-01 Estadística y series temporales aplicadas a sectores (principal) · secundarias: TMB-14
- **Calidad Q:** 79 (B) — Tipo 15/25 · Rigor 14/20 · Autoridad 12/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** https://www.statsmodels.org/v0.14.4/generated/statsmodels.tsa.seasonal.STL.html
- **Acceso y licencia:** Abierto; software libre (BSD)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Cleveland 1990 "STL: A Seasonal-Trend Decomposition Procedure Based on Loess" Journal of Official Statistics»; WebFetch: sí)
- **Contenido:** Implementación Python de STL: periodo inferido o fijado, longitud del suavizador estacional (impar, ≥ 7) y ajuste robusto ponderado frente a atípicos.
- **Uso en el Motor:** AG-B16, MC-B01: implementación reproducible de STL en Python (statsmodels) para series sectoriales.
- **Limitaciones:** Documentación escueta sobre elección de parámetros.

#### MBM-0009 · Q 78 (B) — Programs TRAMO and SEATS: Instructions for the Users

- **Autores:** Víctor Gómez; Agustín Maravall
- **Año:** 1998
- **Publicación o institución:** Ministerio de Economía y Hacienda (España), documento de trabajo 97001
- **Tipo de documento:** Documento técnico de organismo público
- **Temática:** TMB-01 Estadística y series temporales aplicadas a sectores (principal) · secundarias: TMB-14
- **Calidad Q:** 78 (B) — Tipo 15/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 6/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de Hyndman y Khandakar 2008): https://anorien.csc.warwick.ac.uk/CRAN/web/packages/forecast/vignettes/JSS2008.pdf
- **Acceso y licencia:** Documento técnico público (versiones posteriores en el Banco de España)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Hyndman Khandakar 2008 "Automatic time series forecasting…"»; WebFetch: sí, sobre la bibliografía del PDF índice)
- **Contenido:** Manual de TRAMO (regresión ARIMA con atípicos, efectos calendario y datos faltantes) y SEATS (extracción de señal y desestacionalización basada en modelos), estándar del SEE y Eurostat.
- **Uso en el Motor:** AG-B16, MC-B01: desestacionalizar y corregir de calendario series sectoriales europeas (producción industrial, ventas, matriculaciones) antes de medir tendencias.
- **Limitaciones:** Versión de 1998; la herramienta actual de referencia es JDemetra+.

#### MBM-0011 · Q 78 (B) — Are Seasonal Patterns Constant Over Time? A Test for Seasonal Stability

- **Autores:** Fabio Canova; Bruce E. Hansen
- **Año:** 1995
- **Publicación o institución:** Journal of Business and Economic Statistics, 13, 237-252
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-01 Estadística y series temporales aplicadas a sectores (principal) · secundarias: —
- **Calidad Q:** 78 (B) — Tipo 25/25 · Rigor 17/20 · Autoridad 13/15 · Vigencia 4/10 · Impacto 9/10 · Independencia 10/10 · Acceso 0/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de Hyndman y Khandakar 2008): https://anorien.csc.warwick.ac.uk/CRAN/web/packages/forecast/vignettes/JSS2008.pdf
- **Acceso y licencia:** Artículo de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Hyndman Khandakar 2008 "Automatic time series forecasting…"»; WebFetch: sí, sobre la bibliografía del PDF índice)
- **Contenido:** Contraste de estabilidad de los patrones estacionales con la nula de estacionalidad determinista.
- **Uso en el Motor:** AG-B16, MC-B01: detectar cambios en el patrón estacional de un sector (p. ej., comercio electrónico, turismo) que invalidan factores estacionales históricos.
- **Limitaciones:** Confirmada solo por bibliografía.

#### MBM-0012 · Q 77 (B) — Forecasting and Stock Control for Intermittent Demands

- **Autores:** J. D. Croston
- **Año:** 1972
- **Publicación o institución:** Operational Research Quarterly, 23(3), 289-304
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-01 Estadística y series temporales aplicadas a sectores (principal) · secundarias: TMB-05
- **Calidad Q:** 77 (B) — Tipo 25/25 · Rigor 14/20 · Autoridad 12/15 · Vigencia 3/10 · Impacto 10/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de Hyndman y Khandakar 2008): https://anorien.csc.warwick.ac.uk/CRAN/web/packages/forecast/vignettes/JSS2008.pdf
- **Acceso y licencia:** Artículo de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Hyndman Khandakar 2008 "Automatic time series forecasting…"»; WebFetch: sí, sobre la bibliografía del PDF índice)
- **Contenido:** Método de Croston para series de demanda intermitente (muchos ceros): previsión separada del tamaño de la demanda y del intervalo entre demandas.
- **Uso en el Motor:** AG-B16, MC-B01: series sectoriales de pedidos irregulares (bienes de equipo, aeronaves, grandes contratos) que piden AG-B05 Oferta y AG-B04.
- **Limitaciones:** Sesgo conocido corregido en variantes posteriores.

## TMB-02 Econometría de la demanda, elasticidades y paneles sectoriales

#### DOC-MOT-0044 · Q 95 (A) — Estimation and Inference of Impulse Responses by Local Projections

- **Autores:** Òscar Jordà
- **Año:** 2005
- **Publicación o institución:** American Economic Review, 95(1), 161-182
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-02 Econometría de la demanda, elasticidades y paneles sectoriales (principal) · secundarias: TMB-01
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1257/0002828053828518 · https://www.citedrive.com/en/discovery/estimation-and-inference-of-impulse-responses-by-local-projections (DOI) · referencia completa en https://cran.r-universe.dev/lpirfs/doc/manual.html
- **Acceso y licencia:** Revista AEA por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Jordà 2005 "Estimation and Inference of Impulse Responses by Local Projections" American Economic Review 95»; WebFetch: sí)
- **Contenido:** Estima funciones impulso-respuesta mediante una regresión distinta para cada horizonte (proyecciones locales), robusta a errores de especificación del VAR y extensible a no linealidades.
- **Uso en el Motor:** AG-B16, MC-B05: respuestas dinámicas de ventas o márgenes sectoriales a shocks macro (tipos, energía) mediante proyecciones locales (AG-B08 Macro y Ciclo).
- **Limitaciones:** Mayor varianza que el VAR en muestras cortas.
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02 (DOI confirmado).

#### DOC-MOT-0040 · Q 95 (A) — Estimation and Hypothesis Testing of Cointegration Vectors in Gaussian Vector Autoregressive Models

- **Autores:** Søren Johansen
- **Año:** 1991
- **Publicación o institución:** Econometrica, 59(6), 1551-1580
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-02 Econometría de la demanda, elasticidades y paneles sectoriales (principal) · secundarias: TMB-01
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** https://ideas.repec.org/a/ecm/emetrp/v59y1991i6p1551-80.html
- **Acceso y licencia:** Ficha RePEc abierta; texto por suscripción (JSTOR)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Johansen 1991 "Estimation and Hypothesis Testing of Cointegration Vectors in Gaussian Vector Autoregressive Models" Econometrica 59»; WebFetch: sí)
- **Contenido:** Estimación por máxima verosimilitud de VAR con cointegración (rango reducido) y contrastes de traza y máximo autovalor para el número de relaciones de cointegración, con restricciones lineales sobre los vectores.
- **Uso en el Motor:** AG-B16, MC-B05: cointegración multivariante de Johansen entre demanda sectorial, precio y renta para elasticidades de equilibrio.
- **Limitaciones:** Sensible al orden del VAR y a la especificación determinista. DOI de la semilla no visto; se retira.
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02.

#### DOC-MOT-0232 · Q 95 (A) — Heteroskedasticity and Autocorrelation Consistent Covariance Matrix Estimation

- **Autores:** Donald W. K. Andrews
- **Año:** 1991
- **Publicación o institución:** Econometrica, 59(3), 817-858
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-02 Econometría de la demanda, elasticidades y paneles sectoriales (principal) · secundarias: —
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.2307/2938229 · Verificada en páginas índice: https://en.wikipedia.org/wiki/Newey%E2%80%93West_estimator · https://rdrr.io/pkg/sandwich/man/NeweyWest.html
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Newey–West estimator wikipedia heteroskedasticity and autocorrelation consistent Andrews 1991 bandwidth»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Newey%E2%80%93West_estimator)
- **Contenido:** Teoría de los estimadores HAC con núcleo: núcleo espectral cuadrático óptimo y selección automática del ancho de banda mediante aproximación AR(1)/VAR.
- **Uso en el Motor:** AG-B16, MC-B05: elección del ancho de banda HAC en regresiones sectoriales con autocorrelación.
- **Limitaciones:** Confirmada solo mediante página índice (bibliografía de Wikipedia «Newey–West estimator» y ayuda de sandwich); pendiente de lectura de la fuente primaria.

#### DOC-MOT-0039 · Q 95 (A) — Co-Integration and Error Correction: Representation, Estimation, and Testing

- **Autores:** Robert F. Engle; Clive W. J. Granger
- **Año:** 1987
- **Publicación o institución:** Econometrica, 55(2), 251-276
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-02 Econometría de la demanda, elasticidades y paneles sectoriales (principal) · secundarias: TMB-01
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.2307/1913236 · Verificada en página índice: https://en.wikipedia.org/wiki/Cointegration
- **Acceso y licencia:** Revista por suscripción (JSTOR 1913236)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Cointegration wikipedia Engle-Granger Johansen test Phillips-Ouliaris references»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Cointegration)
- **Contenido:** Define la cointegración, el teorema de representación de Granger (equivalencia con modelos de corrección del error) y el método en dos etapas con contraste de raíz unitaria sobre los residuos.
- **Uso en el Motor:** AG-B16, MC-B05: modelo de corrección del error para separar elasticidades de corto y largo plazo de la demanda sectorial.
- **Limitaciones:** Una sola relación de cointegración; sesgo en muestras cortas. Confirmada solo mediante página índice (bibliografía de Wikipedia «Cointegration»); pendiente de lectura de la fuente primaria.
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02 (DOI confirmado en índice).

#### DOC-MOT-0236 · Q 95 (A) — A Heteroskedasticity-Consistent Covariance Matrix Estimator and a Direct Test for Heteroskedasticity

- **Autores:** Halbert White
- **Año:** 1980
- **Publicación o institución:** Econometrica, 48(4), 817-838
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-02 Econometría de la demanda, elasticidades y paneles sectoriales (principal) · secundarias: TMB-01
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.2307/1912934 · Verificada en página índice: https://en.wikipedia.org/wiki/Heteroskedasticity-consistent_standard_errors
- **Acceso y licencia:** Revista por suscripción (JSTOR 1912934)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Heteroskedasticity-consistent standard errors wikipedia White 1980 MacKinnon White 1985»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Heteroskedasticity-consistent_standard_errors)
- **Contenido:** Estimador de covarianzas robusto a heterocedasticidad de forma desconocida (HC0) y contraste directo de heterocedasticidad.
- **Uso en el Motor:** AG-B16, MC-B05: errores estándar robustos a heterocedasticidad en regresiones de demanda y de sensibilidad sectorial (AG-B04, AG-B08).
- **Limitaciones:** Confirmada solo mediante página índice (bibliografía de Wikipedia «Heteroskedasticity-consistent standard errors»); pendiente de lectura de la fuente primaria.

#### DOC-MOT-0239 · Q 94 (A) — Bounds Testing Approaches to the Analysis of Level Relationships

- **Autores:** M. Hashem Pesaran; Yongcheol Shin; Richard J. Smith
- **Año:** 2001
- **Publicación o institución:** Journal of Applied Econometrics, 16(3), 289-326
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-02 Econometría de la demanda, elasticidades y paneles sectoriales (principal) · secundarias: TMB-01
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1002/jae.616 · Verificada en páginas índice: https://en.wikipedia.org/wiki/Cointegration · https://en.wikipedia.org/wiki/Structural_break
- **Acceso y licencia:** Revista Wiley por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Cointegration wikipedia Engle-Granger Johansen test Phillips-Ouliaris references»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Cointegration)
- **Contenido:** Contraste de cotas ARDL para relaciones de nivel válido con regresores I(0), I(1) o mezcla, con valores críticos inferior y superior.
- **Uso en el Motor:** AG-B16, MC-B05: elasticidades de largo plazo (renta, precio) con modelos ARDL y contraste de cotas, válido con regresores I(0) o I(1).
- **Limitaciones:** Confirmada solo mediante página índice (bibliografía de Wikipedia «Cointegration» y «Structural break»); pendiente de lectura de la fuente primaria.

#### DOC-MOT-0041 · Q 94 (A) — A Simple, Positive Semi-Definite, Heteroskedasticity and Autocorrelation Consistent Covariance Matrix

- **Autores:** Whitney K. Newey; Kenneth D. West
- **Año:** 1987
- **Publicación o institución:** Econometrica, 55(3), 703-708
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-02 Econometría de la demanda, elasticidades y paneles sectoriales (principal) · secundarias: TMB-01
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.2307/1913610 · Verificada en páginas índice: https://en.wikipedia.org/wiki/Newey%E2%80%93West_estimator · https://rdrr.io/pkg/sandwich/man/NeweyWest.html
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Newey–West estimator wikipedia heteroskedasticity and autocorrelation consistent Andrews 1991 bandwidth»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Newey%E2%80%93West_estimator)
- **Contenido:** Estimador de la matriz de covarianzas robusto a heterocedasticidad y autocorrelación con ponderaciones de Bartlett, que garantiza semidefinición positiva.
- **Uso en el Motor:** AG-B16, MC-B05: errores estándar HAC de Newey-West en regresiones temporales de elasticidades y betas sectoriales al ciclo.
- **Limitaciones:** Elección del retardo (véanse DOC-MOT-0232 y 0233); mal comportamiento en muestras pequeñas. Confirmada solo mediante página índice (bibliografía de Wikipedia «Newey–West estimator» y ayuda de sandwich); pendiente de lectura de la fuente primaria.
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02 (DOI confirmado en índice).

#### DOC-MOT-0240 · Q 93 (A) — Spurious Regressions in Econometrics

- **Autores:** Clive W. J. Granger; Paul Newbold
- **Año:** 1974
- **Publicación o institución:** Journal of Econometrics, 2(2), 111-120
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-02 Econometría de la demanda, elasticidades y paneles sectoriales (principal) · secundarias: TMB-01
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1016/0304-4076(74)90034-7 · Verificada en página índice: https://en.wikipedia.org/wiki/Cointegration
- **Acceso y licencia:** Revista Elsevier por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Cointegration wikipedia Engle-Granger Johansen test Phillips-Ouliaris references»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Cointegration)
- **Contenido:** Simulaciones que muestran R² y t elevados en regresiones entre paseos aleatorios independientes: la regresión espuria.
- **Uso en el Motor:** AG-B16, MC-B05: advertencia de regresión espuria al relacionar series sectoriales no estacionarias (control de AG-B14 Contrarias).
- **Limitaciones:** Confirmada solo mediante página índice (bibliografía de Wikipedia «Cointegration»); pendiente de lectura de la fuente primaria.

#### MBM-0014 · Q 91 (A) — An Almost Ideal Demand System

- **Autores:** Angus Deaton; John Muellbauer
- **Año:** 1980
- **Publicación o institución:** American Economic Review, 70(3), 312-326
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-02 Econometría de la demanda, elasticidades y paneles sectoriales (principal) · secundarias: TMB-04
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 6/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** https://deaton.scholar.princeton.edu/publications/almost-ideal-demand-system · índice: https://en.wikipedia.org/wiki/Almost_ideal_demand_system
- **Acceso y licencia:** Artículo de JSTOR/AEA; enlace a PDF desde la página del autor
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Almost Ideal Demand System Deaton Muellbauer 1980 American Economic Review Wikipedia»; WebFetch: sí (página del autor y Wikipedia))
- **Contenido:** Sistema de demanda AIDS: cuotas de gasto lineales en el logaritmo de precios y del gasto real, compatible con la agregación y que permite contrastar homogeneidad y simetría.
- **Uso en el Motor:** AG-B16, MC-B05: estimar elasticidades propias, cruzadas y de gasto entre categorías de un sector (sustitución entre bienes, canales o tecnologías) para AG-B04 Demanda y Adopción.
- **Limitaciones:** Requiere datos de gasto y precios por categoría; la versión lineal (LA-AIDS) depende del índice de precios usado.

#### MBM-0019 · Q 90 (A) — Automobile Prices in Market Equilibrium

- **Autores:** Steven Berry; James Levinsohn; Ariel Pakes
- **Año:** 1995
- **Publicación o institución:** Econometrica, 63(4), 841-890
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-02 Econometría de la demanda, elasticidades y paneles sectoriales (principal) · secundarias: TMB-04
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 10/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** JSTOR: https://www.jstor.org/stable/2171802 · https://www.econometricsociety.org/publications/econometrica/1995/07/01/automobile-prices-market-equilibrium
- **Acceso y licencia:** Artículo de pago (Econometric Society/JSTOR)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Berry Levinsohn Pakes 1995 "Automobile Prices in Market Equilibrium" Nevo "A Practitioner's Guide to Estimation of Random-Coefficients Logit Models of Demand"»; WebFetch: sí)
- **Contenido:** Modelo BLP de demanda de productos diferenciados con logit de coeficientes aleatorios, precios endógenos y oferta oligopolística, aplicado al automóvil en EE. UU.
- **Uso en el Motor:** AG-B16, MC-B05 y MC-B03: elasticidades propias y cruzadas a nivel de producto y márgenes implícitos en mercados diferenciados (AG-B03 Estructura y Competencia, AG-B04).
- **Limitaciones:** Exigente en datos (cuotas, características, instrumentos) y en cómputo.

#### MBM-0026 · Q 88 (A) — Initial Conditions and Moment Restrictions in Dynamic Panel Data Models

- **Autores:** Richard Blundell; Stephen Bond
- **Año:** 1998
- **Publicación o institución:** Journal of Econometrics, 87(1), 115-143
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-02 Econometría de la demanda, elasticidades y paneles sectoriales (principal) · secundarias: —
- **Calidad Q:** 88 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 6/10 · Impacto 10/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** DOI: 10.1016/S0304-4076(98)00009-8 · índice: https://en.wikipedia.org/wiki/Arellano%E2%80%93Bond_estimator
- **Acceso y licencia:** Artículo de pago (Elsevier); copia CiteSeerX
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Arellano–Bond estimator Wikipedia Blundell Bond 1998 system GMM Wooldridge Econometric Analysis of Cross Section and Panel Data»; WebFetch: sí, sobre la página índice de Wikipedia)
- **Contenido:** Estimador GMM de sistema que añade condiciones en niveles y corrige el sesgo por instrumentos débiles con series muy persistentes.
- **Uso en el Motor:** AG-B16, MC-B05: estimar persistencia de rentabilidades o márgenes sectoriales (ROIC, ventas) en paneles cortos de empresas.
- **Limitaciones:** Supuestos sobre condiciones iniciales; riesgo de proliferación de instrumentos.

#### MBM-0025 · Q 88 (A) — Some Tests of Specification for Panel Data: Monte Carlo Evidence and an Application to Employment Equations

- **Autores:** Manuel Arellano; Stephen Bond
- **Año:** 1991
- **Publicación o institución:** Review of Economic Studies, 58(2), 277-297
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-02 Econometría de la demanda, elasticidades y paneles sectoriales (principal) · secundarias: —
- **Calidad Q:** 88 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 6/10 · Impacto 10/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** DOI: 10.2307/2297968 · índice: https://en.wikipedia.org/wiki/Arellano%E2%80%93Bond_estimator
- **Acceso y licencia:** Artículo de pago (JSTOR)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Arellano–Bond estimator Wikipedia Blundell Bond 1998 system GMM Wooldridge Econometric Analysis of Cross Section and Panel Data»; WebFetch: sí, sobre la página índice de Wikipedia)
- **Contenido:** Estimador GMM en diferencias para paneles dinámicos con efectos fijos y contrastes de autocorrelación y de sobreidentificación.
- **Uso en el Motor:** AG-B16, MC-B05: paneles dinámicos de empresas o países por sector (persistencia de ventas, márgenes o inversión) para AG-B03 y AG-B09.
- **Limitaciones:** Instrumentos débiles con series persistentes (véase MBM-0026).

#### DOC-MOT-0046 · Q 87 (A) — Mostly Harmless Econometrics: An Empiricist's Companion

- **Autores:** Joshua D. Angrist; Jörn-Steffen Pischke
- **Año:** 2009
- **Publicación o institución:** Princeton University Press (edición electrónica en De Gruyter Brill)
- **Tipo de documento:** Manual de referencia
- **Temática:** TMB-02 Econometría de la demanda, elasticidades y paneles sectoriales (principal) · secundarias: TMB-11
- **Calidad Q:** 87 (A) — Tipo 20/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.1515/9781400829828 · https://www.degruyterbrill.com/document/doi/10.1515/9781400829828/html?lang=en
- **Acceso y licencia:** Libro de pago; preliminares abiertos
- **Estado:** Aprobada
- **Estado del enlace:** MURO_PAGO
- **Última verificación:** 2026-11-02 (búsqueda web: «Angrist Pischke "Mostly Harmless Econometrics: An Empiricist's Companion" Princeton University Press 2009»; WebFetch: sí)
- **Contenido:** Guía de identificación causal: regresión como aproximación a la esperanza condicional, variables instrumentales, diferencias en diferencias, regresión discontinua, datos de panel y errores estándar.
- **Uso en el Motor:** AG-B16, MC-B05: diseño de identificación (variables instrumentales, diferencias en diferencias, discontinuidad) para estimar efectos causales de precio, regulación o shocks en un sector (AG-B04, AG-B07).
- **Limitaciones:** Orientado a microeconometría; anterior a la nueva literatura de DiD escalonado.
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02 (DOI confirmado).

#### MBM-0027 · Q 87 (A) — How to Do xtabond2: An Introduction to Difference and System GMM in Stata

- **Autores:** David Roodman
- **Año:** 2009
- **Publicación o institución:** The Stata Journal, 9(1), 86-136
- **Tipo de documento:** Artículo revisado por pares (tutorial)
- **Temática:** TMB-02 Econometría de la demanda, elasticidades y paneles sectoriales (principal) · secundarias: TMB-14
- **Calidad Q:** 87 (A) — Tipo 22/25 · Rigor 16/20 · Autoridad 12/15 · Vigencia 7/10 · Impacto 10/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** DOI: 10.1177/1536867X0900900106 · https://ageconsearch.umn.edu/record/122704/files/sjart_st0159.pdf
- **Acceso y licencia:** Acceso abierto (AgEcon Search)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Arellano–Bond estimator Wikipedia Blundell Bond 1998 system GMM Wooldridge Econometric Analysis of Cross Section and Panel Data»; WebFetch: sí)
- **Contenido:** Tutorial de los estimadores GMM en diferencias y de sistema, sus contrastes y los riesgos de usar demasiados instrumentos.
- **Uso en el Motor:** AG-B16, MC-B05: guía práctica y lista de comprobación para paneles dinámicos sectoriales.
- **Limitaciones:** Centrado en Stata.

#### MBM-0033 · Q 86 (A) — A Meta-Analysis on the Price Elasticity of Energy Demand

- **Autores:** Xavier Labandeira; José M. Labeaga; Xiral López-Otero
- **Año:** 2017
- **Publicación o institución:** Energy Policy, 102, 549-568
- **Tipo de documento:** Artículo revisado por pares (metaanálisis)
- **Temática:** TMB-02 Econometría de la demanda, elasticidades y paneles sectoriales (principal) · secundarias: TMB-01
- **Calidad Q:** 86 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 13/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** DOI: 10.1016/j.enpol.2017.01.002 · https://ideas.repec.org/a/eee/enepol/v102y2017icp549-568.html · versión previa: https://cadmus.eui.eu/bitstream/handle/1814/40870/RSCAS_2016_25.pdf
- **Acceso y licencia:** Artículo de pago; documento de trabajo en abierto (EUI RSCAS 2016/25)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Labandeira Labeaga López-Otero 2017 "A meta-analysis on the price elasticity of energy demand" Energy Policy»; WebFetch: sí)
- **Contenido:** Metaanálisis de elasticidades-precio de corto y largo plazo de la demanda de energía (electricidad, gas natural, gasolina, gasóleo, gasóleo de calefacción) y de sus determinantes.
- **Uso en el Motor:** AG-B16, MC-B05: valores de referencia de elasticidades para sectores energéticos y para contrastar las estimadas (AG-B04, AG-B11 Sostenibilidad).
- **Limitaciones:** Resultados medios; los rangos por país y periodo son amplios.

#### MBM-0029 · Q 85 (A) — Panel Data Econometrics in R: The plm Package

- **Autores:** Yves Croissant; Giovanni Millo
- **Año:** 2008
- **Publicación o institución:** Journal of Statistical Software, 27(2), 1-43
- **Tipo de documento:** Artículo revisado por pares (software)
- **Temática:** TMB-02 Econometría de la demanda, elasticidades y paneles sectoriales (principal) · secundarias: TMB-14
- **Calidad Q:** 85 (A) — Tipo 22/25 · Rigor 16/20 · Autoridad 12/15 · Vigencia 6/10 · Impacto 9/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** DOI: 10.18637/jss.v027.i02 · índice: https://en.wikipedia.org/wiki/Arellano%E2%80%93Bond_estimator
- **Acceso y licencia:** Acceso abierto (JSS)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Arellano–Bond estimator Wikipedia Blundell Bond 1998 system GMM Wooldridge Econometric Analysis of Cross Section and Panel Data»; WebFetch: sí, sobre la página índice de Wikipedia)
- **Contenido:** Paquete R para efectos fijos y aleatorios, contraste de Hausman, GMM dinámico y errores robustos en paneles.
- **Uso en el Motor:** AG-B16, MC-B05: implementación reproducible de paneles sectoriales (empresas × años, países × sectores).
- **Limitaciones:** Versión de 2008; el paquete ha evolucionado.

#### MBM-0021 · Q 85 (A) — A Practitioner's Guide to Estimation of Random-Coefficients Logit Models of Demand

- **Autores:** Aviv Nevo
- **Año:** 2000
- **Publicación o institución:** Journal of Economics & Management Strategy, 9(4), 513-548
- **Tipo de documento:** Artículo revisado por pares (guía metodológica)
- **Temática:** TMB-02 Econometría de la demanda, elasticidades y paneles sectoriales (principal) · secundarias: —
- **Calidad Q:** 85 (A) — Tipo 23/25 · Rigor 17/20 · Autoridad 13/15 · Vigencia 6/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1111/j.1430-9134.2000.00513.x · https://ideas.repec.Org/a/bla/jemstr/v9y2000i4p513-548.html
- **Acceso y licencia:** Artículo de pago; registro abierto en IDEAS
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Berry Levinsohn Pakes 1995 "Automobile Prices in Market Equilibrium" Nevo "A Practitioner's Guide to Estimation of Random-Coefficients Logit Models of Demand"»; WebFetch: sí)
- **Contenido:** Guía práctica para estimar el modelo BLP: algoritmo de contracción, instrumentos, cálculo de elasticidades y márgenes, con ejemplo de cereales.
- **Uso en el Motor:** AG-B16, MC-B05: receta paso a paso para implementar demanda de coeficientes aleatorios en un sector concreto.
- **Limitaciones:** Problemas numéricos conocidos señalados en literatura posterior.

#### MBM-0016 · Q 85 (A) — Quadratic Engel Curves and Consumer Demand

- **Autores:** James Banks; Richard Blundell; Arthur Lewbel
- **Año:** 1997
- **Publicación o institución:** Review of Economics and Statistics, 79(4), 527-539
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-02 Econometría de la demanda, elasticidades y paneles sectoriales (principal) · secundarias: —
- **Calidad Q:** 85 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 6/10 · Impacto 9/10 · Independencia 10/10 · Acceso 2/10
- **DOI / ISBN / URL:** Verificada en página índice: https://en.wikipedia.org/wiki/Almost_ideal_demand_system
- **Acceso y licencia:** Artículo de pago (MIT Press)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Almost Ideal Demand System Deaton Muellbauer 1980 American Economic Review Wikipedia»; WebFetch: sí, sobre la página índice)
- **Contenido:** Extiende el AIDS con un término cuadrático en el gasto (QUAIDS): bienes que son de lujo a rentas bajas y necesarios a rentas altas.
- **Uso en el Motor:** AG-B16, MC-B05: elasticidades-renta que cambian con el nivel de renta, clave para proyectar la demanda sectorial en mercados emergentes (AG-B04, AG-B08).
- **Limitaciones:** Confirmada solo por página índice.

#### MBM-0020 · Q 85 (A) — Estimating Discrete-Choice Models of Product Differentiation

- **Autores:** Steven T. Berry
- **Año:** 1994
- **Publicación o institución:** RAND Journal of Economics, 25(2), 242-262
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-02 Econometría de la demanda, elasticidades y paneles sectoriales (principal) · secundarias: TMB-04
- **Calidad Q:** 85 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 6/10 · Impacto 10/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** Verificada en página índice (referencias de Nevo 2000 en IDEAS): https://ideas.repec.Org/a/bla/jemstr/v9y2000i4p513-548.html
- **Acceso y licencia:** Artículo de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Berry Levinsohn Pakes 1995 "Automobile Prices in Market Equilibrium" Nevo "A Practitioner's Guide to Estimation of Random-Coefficients Logit Models of Demand"»; WebFetch: sí, sobre la página índice)
- **Contenido:** Inversión de las cuotas de mercado para recuperar utilidades medias y estimar demandas logit y logit anidado con instrumentos a partir de datos agregados.
- **Uso en el Motor:** AG-B16, MC-B05: estimación de elasticidades con solo cuotas de mercado y precios por producto (logit / logit anidado) cuando no hay microdatos.
- **Limitaciones:** Confirmada solo por página índice.

#### MBM-0028 · Q 85 (A) — Estimation of Dynamic Models with Error Components

- **Autores:** T. W. Anderson; Cheng Hsiao
- **Año:** 1981
- **Publicación o institución:** Journal of the American Statistical Association, 76(375), 598-606
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-02 Econometría de la demanda, elasticidades y paneles sectoriales (principal) · secundarias: —
- **Calidad Q:** 85 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 4/10 · Impacto 9/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1080/01621459.1981.10477691 · índice: https://en.wikipedia.org/wiki/Arellano%E2%80%93Bond_estimator
- **Acceso y licencia:** Artículo de pago; PDF enlazado desde Wikipedia
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Arellano–Bond estimator Wikipedia Blundell Bond 1998 system GMM Wooldridge Econometric Analysis of Cross Section and Panel Data»; WebFetch: sí, sobre la página índice de Wikipedia)
- **Contenido:** Estimador de variables instrumentales en primeras diferencias para modelos de panel dinámico.
- **Uso en el Motor:** AG-B16, MC-B05: alternativa simple al GMM para paneles sectoriales pequeños.
- **Limitaciones:** Menos eficiente que el GMM.

#### MBM-0015 · Q 83 (A) — Economics and Consumer Behavior

- **Autores:** Angus Deaton; John Muellbauer
- **Año:** 1980
- **Publicación o institución:** Cambridge University Press (Cambridge)
- **Tipo de documento:** Manual de referencia
- **Temática:** TMB-02 Econometría de la demanda, elasticidades y paneles sectoriales (principal) · secundarias: —
- **Calidad Q:** 83 (A) — Tipo 22/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 5/10 · Impacto 10/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** Verificada en página índice (referencias del manual del paquete micEconAids): https://cran.r-universe.dev/micEconAids/doc/manual.html
- **Acceso y licencia:** Libro de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Almost Ideal Demand System Deaton Muellbauer 1980 American Economic Review Wikipedia»; WebFetch: sí, sobre la página índice)
- **Contenido:** Manual de teoría y econometría de la demanda del consumidor: separabilidad, agregación, sistemas de demanda, números índice y bienes duraderos.
- **Uso en el Motor:** AG-B16, MC-B05: marco teórico para restricciones (homogeneidad, simetría, separabilidad) al estimar demandas sectoriales.
- **Limitaciones:** Confirmada solo por referencia bibliográfica; anterior a los modelos de productos diferenciados.

#### MBM-0032 · Q 82 (A) — Analysis of Panel Data (3.ª ed.)

- **Autores:** Cheng Hsiao
- **Año:** 2014
- **Publicación o institución:** Cambridge University Press (Nueva York)
- **Tipo de documento:** Manual de referencia
- **Temática:** TMB-02 Econometría de la demanda, elasticidades y paneles sectoriales (principal) · secundarias: —
- **Calidad Q:** 82 (A) — Tipo 22/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 1/10
- **DOI / ISBN / URL:** ISBN: 978-1-107-65763-2 · índice: https://en.wikipedia.org/wiki/Arellano%E2%80%93Bond_estimator
- **Acceso y licencia:** Libro de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Arellano–Bond estimator Wikipedia Blundell Bond 1998 system GMM Wooldridge Econometric Analysis of Cross Section and Panel Data»; WebFetch: sí, sobre la página índice de Wikipedia)
- **Contenido:** Manual de paneles: modelos estáticos y dinámicos, ecuaciones simultáneas, coeficientes variables y paneles con dependencia transversal.
- **Uso en el Motor:** AG-B16, MC-B05: heterogeneidad de pendientes entre empresas o países de un sector.
- **Limitaciones:** Confirmada solo por página índice.

#### MBM-0022 · Q 82 (A) — Differentiated Products Demand Systems from a Combination of Micro and Macro Data: The New Car Market

- **Autores:** Steven Berry; James Levinsohn; Ariel Pakes
- **Año:** 2004
- **Publicación o institución:** Journal of Political Economy, 112(1), 68-105
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-02 Econometría de la demanda, elasticidades y paneles sectoriales (principal) · secundarias: —
- **Calidad Q:** 82 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 5/10 · Impacto 8/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** Verificada en página índice (referencias de Nevo 2000 en IDEAS): https://ideas.repec.Org/a/bla/jemstr/v9y2000i4p513-548.html
- **Acceso y licencia:** Artículo de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Berry Levinsohn Pakes 1995 "Automobile Prices in Market Equilibrium" Nevo "A Practitioner's Guide to Estimation of Random-Coefficients Logit Models of Demand"»; WebFetch: sí, sobre la página índice)
- **Contenido:** Combina microdatos de encuesta (segundas opciones de compra) con datos de mercado para identificar mejor los patrones de sustitución.
- **Uso en el Motor:** AG-B16, MC-B05: mejorar elasticidades cruzadas sectoriales cuando hay encuestas de consumidores.
- **Limitaciones:** Confirmada solo por página índice.

#### MBM-0024 · Q 82 (A) — Mixed MNL Models for Discrete Response

- **Autores:** Daniel McFadden; Kenneth Train
- **Año:** 2000
- **Publicación o institución:** Journal of Applied Econometrics, 15(5), 447-470
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-02 Econometría de la demanda, elasticidades y paneles sectoriales (principal) · secundarias: —
- **Calidad Q:** 82 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 6/10 · Impacto 9/10 · Independencia 10/10 · Acceso 2/10
- **DOI / ISBN / URL:** Verificada en página índice (referencias de Nevo 2000 en IDEAS): https://ideas.repec.Org/a/bla/jemstr/v9y2000i4p513-548.html
- **Acceso y licencia:** Artículo de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Berry Levinsohn Pakes 1995 "Automobile Prices in Market Equilibrium" Nevo "A Practitioner's Guide to Estimation of Random-Coefficients Logit Models of Demand"»; WebFetch: sí, sobre la página índice)
- **Contenido:** Demuestra que el logit mixto aproxima cualquier modelo de utilidad aleatoria y desarrolla su estimación por simulación.
- **Uso en el Motor:** AG-B16, MC-B05: modelos de elección del consumidor con heterogeneidad (adopción de tecnologías, elección de proveedor) con microdatos.
- **Limitaciones:** Confirmada solo por página índice.

#### MBM-0030 · Q 81 (A) — Econometric Analysis of Panel Data (4.ª ed.)

- **Autores:** Badi H. Baltagi
- **Año:** 2008
- **Publicación o institución:** John Wiley & Sons
- **Tipo de documento:** Manual de referencia
- **Temática:** TMB-02 Econometría de la demanda, elasticidades y paneles sectoriales (principal) · secundarias: —
- **Calidad Q:** 81 (A) — Tipo 22/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 7/10 · Impacto 10/10 · Independencia 10/10 · Acceso 1/10
- **DOI / ISBN / URL:** ISBN: 978-0-470-51886-1 · índice: https://en.wikipedia.org/wiki/Arellano%E2%80%93Bond_estimator
- **Acceso y licencia:** Libro de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Arellano–Bond estimator Wikipedia Blundell Bond 1998 system GMM Wooldridge Econometric Analysis of Cross Section and Panel Data»; WebFetch: sí, sobre la página índice de Wikipedia)
- **Contenido:** Manual de econometría de datos de panel: efectos fijos y aleatorios, paneles dinámicos, heterogeneidad y dependencia transversal.
- **Uso en el Motor:** AG-B16, MC-B05: referencia general para paneles de empresas por sector y paneles de países.
- **Limitaciones:** Hay ediciones posteriores.

#### MBM-0038 · Q 80 (A) — Long-Run Demand for Energy Services: Income and Price Elasticities over Two Hundred Years

- **Autores:** Roger Fouquet
- **Año:** 2014
- **Publicación o institución:** Review of Environmental Economics and Policy, 8(2), 186-207
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-02 Econometría de la demanda, elasticidades y paneles sectoriales (principal) · secundarias: TMB-03
- **Calidad Q:** 80 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 13/15 · Vigencia 8/10 · Impacto 7/10 · Independencia 10/10 · Acceso 2/10
- **DOI / ISBN / URL:** Verificada en página índice (referencias de Labandeira et al. 2017 en IDEAS): https://ideas.repec.org/a/eee/enepol/v102y2017icp549-568.html
- **Acceso y licencia:** Artículo de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Labandeira Labeaga López-Otero 2017 "A meta-analysis on the price elasticity of energy demand" Energy Policy»; WebFetch: sí, sobre la página índice)
- **Contenido:** Estima cómo cambian las elasticidades renta y precio de los servicios energéticos (luz, transporte, calor) a lo largo de dos siglos de desarrollo.
- **Uso en el Motor:** AG-B16, MC-B05: elasticidades que varían con la madurez del mercado, para proyecciones de largo plazo (AG-B13 Prospectiva).
- **Limitaciones:** Confirmada solo por página índice; datos británicos.

#### MBM-0031 · Q 80 (A) — Microeconometrics: Methods and Applications

- **Autores:** A. Colin Cameron; Pravin K. Trivedi
- **Año:** 2005
- **Publicación o institución:** Cambridge University Press (Nueva York)
- **Tipo de documento:** Manual de referencia
- **Temática:** TMB-02 Econometría de la demanda, elasticidades y paneles sectoriales (principal) · secundarias: —
- **Calidad Q:** 80 (A) — Tipo 22/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 6/10 · Impacto 10/10 · Independencia 10/10 · Acceso 1/10
- **DOI / ISBN / URL:** ISBN: 0-521-84805-9 · índice: https://en.wikipedia.org/wiki/Arellano%E2%80%93Bond_estimator
- **Acceso y licencia:** Libro de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Arellano–Bond estimator Wikipedia Blundell Bond 1998 system GMM Wooldridge Econometric Analysis of Cross Section and Panel Data»; WebFetch: sí, sobre la página índice de Wikipedia)
- **Contenido:** Manual de microeconometría: elección discreta, datos de recuento, duración, paneles, simulación y bootstrap.
- **Uso en el Motor:** AG-B16, MC-B05: modelos de elección discreta y de recuento para adopción y demanda con microdatos.
- **Limitaciones:** Confirmada solo por página índice.

#### MBM-0037 · Q 79 (B) — Meta-Regression Analysis: A Quantitative Method of Literature Surveys

- **Autores:** T. D. Stanley; Stephen B. Jarrell
- **Año:** 2005
- **Publicación o institución:** Journal of Economic Surveys, 19(3), 299-308
- **Tipo de documento:** Artículo revisado por pares (método)
- **Temática:** TMB-02 Econometría de la demanda, elasticidades y paneles sectoriales (principal) · secundarias: TMB-13
- **Calidad Q:** 79 (B) — Tipo 25/25 · Rigor 15/20 · Autoridad 12/15 · Vigencia 6/10 · Impacto 9/10 · Independencia 10/10 · Acceso 2/10
- **DOI / ISBN / URL:** Verificada en página índice (referencias de Labandeira et al. 2017 en IDEAS): https://ideas.repec.org/a/eee/enepol/v102y2017icp549-568.html
- **Acceso y licencia:** Artículo de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Labandeira Labeaga López-Otero 2017 "A meta-analysis on the price elasticity of energy demand" Energy Policy»; WebFetch: sí, sobre la página índice)
- **Contenido:** Presenta la metarregresión para sintetizar estimaciones empíricas y explicar su heterogeneidad.
- **Uso en el Motor:** AG-B16, MC-B05: combinar elasticidades publicadas de un sector en una estimación de consenso con su dispersión.
- **Limitaciones:** Confirmada solo por página índice.

#### MBM-0034 · Q 79 (B) — Gasoline Demand Revisited: An International Meta-Analysis of Elasticities

- **Autores:** Molly Espey
- **Año:** 1998
- **Publicación o institución:** Energy Economics, 20(3), 273-295
- **Tipo de documento:** Artículo revisado por pares (metaanálisis)
- **Temática:** TMB-02 Econometría de la demanda, elasticidades y paneles sectoriales (principal) · secundarias: —
- **Calidad Q:** 79 (B) — Tipo 25/25 · Rigor 16/20 · Autoridad 13/15 · Vigencia 4/10 · Impacto 9/10 · Independencia 10/10 · Acceso 2/10
- **DOI / ISBN / URL:** Verificada en página índice (referencias de Labandeira et al. 2017 en IDEAS): https://ideas.repec.org/a/eee/enepol/v102y2017icp549-568.html
- **Acceso y licencia:** Artículo de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Labandeira Labeaga López-Otero 2017 "A meta-analysis on the price elasticity of energy demand" Energy Policy»; WebFetch: sí, sobre la página índice)
- **Contenido:** Metaanálisis internacional de elasticidades-precio y renta de la demanda de gasolina y de cómo dependen del diseño del estudio.
- **Uso en el Motor:** AG-B16, MC-B05: rangos de elasticidades para combustibles de automoción (refino, distribución, vehículo eléctrico como sustituto).
- **Limitaciones:** Confirmada solo por página índice; datos antiguos.

#### MBM-0035 · Q 78 (B) — Demand for Gasoline Is More Price-Inelastic than Commonly Thought

- **Autores:** Tomas Havranek; Zuzana Irsova; Karel Janda
- **Año:** 2012
- **Publicación o institución:** Energy Economics, 34(1), 201-207
- **Tipo de documento:** Artículo revisado por pares (metaanálisis)
- **Temática:** TMB-02 Econometría de la demanda, elasticidades y paneles sectoriales (principal) · secundarias: —
- **Calidad Q:** 78 (B) — Tipo 25/25 · Rigor 15/20 · Autoridad 12/15 · Vigencia 7/10 · Impacto 7/10 · Independencia 10/10 · Acceso 2/10
- **DOI / ISBN / URL:** Verificada en página índice (referencias de Labandeira et al. 2017 en IDEAS): https://ideas.repec.org/a/eee/enepol/v102y2017icp549-568.html
- **Acceso y licencia:** Artículo de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Labandeira Labeaga López-Otero 2017 "A meta-analysis on the price elasticity of energy demand" Energy Policy»; WebFetch: sí, sobre la página índice)
- **Contenido:** Corrige el sesgo de publicación en las elasticidades de la gasolina y concluye que la demanda es menos elástica de lo que sugiere la literatura.
- **Uso en el Motor:** AG-B16, MC-B05: ajuste por sesgo de publicación al usar elasticidades de la literatura en un sector.
- **Limitaciones:** Confirmada solo por página índice.

#### MBM-0023 · Q 78 (B) — Valuation of New Goods under Perfect and Imperfect Competition

- **Autores:** Jerry A. Hausman
- **Año:** 1996
- **Publicación o institución:** NBER Chapters (NBER), 207-248
- **Tipo de documento:** Capítulo de libro académico
- **Temática:** TMB-02 Econometría de la demanda, elasticidades y paneles sectoriales (principal) · secundarias: TMB-03
- **Calidad Q:** 78 (B) — Tipo 20/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 5/10 · Impacto 8/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** Verificada en página índice (referencias de Nevo 2000 en IDEAS): https://ideas.repec.Org/a/bla/jemstr/v9y2000i4p513-548.html
- **Acceso y licencia:** Capítulo NBER
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Berry Levinsohn Pakes 1995 "Automobile Prices in Market Equilibrium" Nevo "A Practitioner's Guide to Estimation of Random-Coefficients Logit Models of Demand"»; WebFetch: sí, sobre la página índice)
- **Contenido:** Método para estimar el valor para el consumidor de un nuevo producto (precio virtual) a partir de una demanda estimada, con competencia perfecta e imperfecta.
- **Uso en el Motor:** AG-B16, MC-B05: valorar la demanda potencial de un producto o categoría nueva y su canibalización de las existentes (AG-B04, AG-B06).
- **Limitaciones:** Confirmada solo por página índice; especificación criticada en la literatura.

#### MBM-0017 · Q 76 (B) — Units of Measurement and the Stone Index in Demand System Estimation

- **Autores:** GianCarlo Moschini
- **Año:** 1995
- **Publicación o institución:** American Journal of Agricultural Economics, 77, 63-68
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-02 Econometría de la demanda, elasticidades y paneles sectoriales (principal) · secundarias: —
- **Calidad Q:** 76 (B) — Tipo 25/25 · Rigor 15/20 · Autoridad 12/15 · Vigencia 5/10 · Impacto 7/10 · Independencia 10/10 · Acceso 2/10
- **DOI / ISBN / URL:** Verificada en página índice (referencias del manual micEconAids): https://cran.r-universe.dev/micEconAids/doc/manual.html
- **Acceso y licencia:** Artículo de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Almost Ideal Demand System Deaton Muellbauer 1980 American Economic Review Wikipedia»; WebFetch: sí, sobre la página índice)
- **Contenido:** Muestra que el índice de Stone del LA-AIDS no es invariante a las unidades y propone índices alternativos.
- **Uso en el Motor:** AG-B16, MC-B05: control técnico al estimar LA-AIDS con datos sectoriales (elección del índice de precios).
- **Limitaciones:** Nota técnica breve; confirmada solo por referencia.

#### MBM-0036 · Q 75 (B) — Turning on the Lights: A Meta-Analysis of Residential Electricity Demand Elasticities

- **Autores:** James A. Espey; Molly Espey
- **Año:** 2004
- **Publicación o institución:** Journal of Agricultural and Applied Economics, 36(1), 65-81
- **Tipo de documento:** Artículo revisado por pares (metaanálisis)
- **Temática:** TMB-02 Econometría de la demanda, elasticidades y paneles sectoriales (principal) · secundarias: —
- **Calidad Q:** 75 (B) — Tipo 25/25 · Rigor 14/20 · Autoridad 12/15 · Vigencia 5/10 · Impacto 7/10 · Independencia 10/10 · Acceso 2/10
- **DOI / ISBN / URL:** Verificada en página índice (referencias de Labandeira et al. 2017 en IDEAS): https://ideas.repec.org/a/eee/enepol/v102y2017icp549-568.html
- **Acceso y licencia:** Artículo de revista
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Labandeira Labeaga López-Otero 2017 "A meta-analysis on the price elasticity of energy demand" Energy Policy»; WebFetch: sí, sobre la página índice)
- **Contenido:** Metaanálisis de elasticidades-precio y renta de la demanda eléctrica residencial.
- **Uso en el Motor:** AG-B16, MC-B05: referencia de elasticidades para utilities eléctricas y para escenarios de demanda.
- **Limitaciones:** Confirmada solo por página índice.

#### MBM-0018 · Q 73 (B) — micEconAids: Demand Analysis with the Almost Ideal Demand System (AIDS) — manual del paquete R

- **Autores:** Arne Henningsen (autor y mantenedor)
- **Año:** 2026 (versión consultada)
- **Publicación o institución:** CRAN / R-universe
- **Tipo de documento:** Documentación de software
- **Temática:** TMB-02 Econometría de la demanda, elasticidades y paneles sectoriales (principal) · secundarias: TMB-14
- **Calidad Q:** 73 (B) — Tipo 15/25 · Rigor 14/20 · Autoridad 10/15 · Vigencia 8/10 · Impacto 6/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://cran.r-universe.dev/micEconAids/doc/manual.html
- **Acceso y licencia:** Software libre (GPL)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Almost Ideal Demand System Deaton Muellbauer 1980 American Economic Review Wikipedia»; WebFetch: sí)
- **Contenido:** Paquete R que estima AIDS y LA-AIDS, calcula elasticidades (Marshall, Hicks, gasto) y contrasta restricciones, con datos de ejemplo.
- **Uso en el Motor:** AG-B16, MC-B05: implementación reproducible de sistemas de demanda sectoriales.
- **Limitaciones:** Documentación técnica, no revisada por pares.

## TMB-03 Modelos de difusión y curvas de adopción

#### DOC-MOT-0106 · Q 93 (A) — A New Product Growth for Model Consumer Durables

- **Autores:** Frank M. Bass
- **Año:** 1969
- **Publicación o institución:** Management Science, 15(5), 215-227
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-03 Modelos de difusión y curvas de adopción (principal) · secundarias: TMB-01
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1287/mnsc.15.5.215 · https://en.wikipedia.org/wiki/Bass_diffusion_model (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Bass diffusion model" en.wikipedia.org»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Bass_diffusion_model)
- **Contenido:** Modelo de difusión de Bass: la adopción combina innovación (coeficiente p) e imitación (q) y produce curvas S de ventas de bienes duraderos.
- **Uso en el Motor:** AG-B16, MC-B02: ajuste del modelo de Bass (innovación p, imitación q, mercado potencial m) para proyectar la adopción de un producto o tecnología y su pico de ventas (AG-B04 Demanda y Adopción, AG-B13 Prospectiva).
- **Limitaciones:** Mercado potencial fijo; pronósticos inestables con pocos datos iniciales.

#### DOC-MOT-0433 · Q 91 (A) — Why the Bass Model Fits without Decision Variables

- **Autores:** Frank M. Bass; Trichy V. Krishnan; Dipak C. Jain
- **Año:** 1994
- **Publicación o institución:** Marketing Science, 13(3), 203-223
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-03 Modelos de difusión y curvas de adopción (principal) · secundarias: TMB-02
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.1287/mksc.13.3.203 · https://en.wikipedia.org/wiki/Bass_diffusion_model (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Bass diffusion model" en.wikipedia.org»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Bass_diffusion_model)
- **Contenido:** Modelo de Bass generalizado con precio y publicidad; explica por qué el modelo simple ajusta bien cuando esas variables cambian de forma regular.
- **Uso en el Motor:** AG-B16, MC-B02: Bass generalizado con precio y publicidad para escenarios de adopción cuando cambian precios o incentivos (AG-B04, AG-B07).
- **Limitaciones:** Supone efectos porcentuales de las variables de decisión.

#### DOC-MOT-0435 · Q 90 (A) — A Diffusion Theory Model of Adoption and Substitution for Successive Generations of High-Technology Products

- **Autores:** John A. Norton; Frank M. Bass
- **Año:** 1987
- **Publicación o institución:** Management Science, 33(9), 1069-1086
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-03 Modelos de difusión y curvas de adopción (principal) · secundarias: TMB-05
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.1287/mnsc.33.9.1069 · https://en.wikipedia.org/wiki/Bass_diffusion_model (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Bass diffusion model" en.wikipedia.org»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Bass_diffusion_model)
- **Contenido:** Extiende el modelo de Bass a generaciones sucesivas de tecnología que se sustituyen entre sí (p. ej., memorias DRAM).
- **Uso en el Motor:** AG-B16, MC-B02: difusión y sustitución entre generaciones sucesivas de una tecnología (p. ej., chips, redes móviles, baterías) para AG-B06 Tecnología.
- **Limitaciones:** Mismos parámetros de difusión entre generaciones.

#### MBM-0040 · Q 89 (A) — An Exploration of Technology Diffusion

- **Autores:** Diego Comin; Bart Hobijn
- **Año:** 2010
- **Publicación o institución:** American Economic Review, 100(5), 2031-2059
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-03 Modelos de difusión y curvas de adopción (principal) · secundarias: TMB-06
- **Calidad Q:** 89 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 10/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** Verificada en página índice (referencias de «The CHAT Dataset» en IDEAS): https://ideas.repec.org/p/nbr/nberwo/15319.html
- **Acceso y licencia:** Artículo de pago (AEA)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Comin Hobijn 2010 "An Exploration of Technology Diffusion" American Economic Review CHAT dataset»; WebFetch: sí, sobre la página índice)
- **Contenido:** Estima los retardos de adopción de numerosas tecnologías en muchos países durante dos siglos, separando el momento de llegada de la tecnología de su intensidad de uso.
- **Uso en el Motor:** AG-B16, MC-B02: retardos de adopción entre países para proyectar la difusión de una tecnología en mercados geográficos rezagados (AG-B04, AG-B08).
- **Limitaciones:** Confirmada solo por página índice; macro por países, no por producto.

#### DOC-MOT-0112 · Q 89 (A) — Modelling and Forecasting the Diffusion of Innovation – A 25-Year Review

- **Autores:** Nigel Meade; Towhidul Islam
- **Año:** 2006
- **Publicación o institución:** International Journal of Forecasting, 22(3), 519-545
- **Tipo de documento:** Artículo de revisión revisado por pares
- **Temática:** TMB-03 Modelos de difusión y curvas de adopción (principal) · secundarias: TMB-11
- **Calidad Q:** 89 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** https://ideas.repec.org/a/eee/intfor/v22y2006i3p519-545.html
- **Acceso y licencia:** Artículo de pago en el editor (ScienceDirect); ficha abierta en RePEc
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Meade Islam 2006 "Modelling and forecasting the diffusion of innovation" 25-year review International Journal of Forecasting»; WebFetch: sí)
- **Contenido:** Revisa 25 años de modelos de difusión (Bass y extensiones, multigeneración, multinacionales, estimación) y su capacidad predictiva.
- **Uso en el Motor:** AG-B16, MC-B02: revisión de modelos de difusión y de su capacidad predictiva para elegir el modelo de adopción de un mercado.
- **Limitaciones:** Revisión anterior a 2006. El DOI de la semilla no aparecía en la página leída y se retira.

#### DOC-MOT-0440 · Q 89 (A) — Technical Change and the Rate of Imitation

- **Autores:** Edwin Mansfield
- **Año:** 1961
- **Publicación o institución:** Econometrica, 741-766
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-03 Modelos de difusión y curvas de adopción (principal) · secundarias: TMB-04
- **Calidad Q:** 89 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** https://arxiv.org/pdf/2602.19488 (bibliografía de DOC-MOT-0429)
- **Acceso y licencia:** Artículo de pago en el editor (JSTOR)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Meade Islam 2006 "Modelling and forecasting the diffusion of innovation" 25-year review International Journal of Forecasting»; WebFetch: sí, sobre la página índice https://arxiv.org/pdf/2602.19488)
- **Contenido:** Modelo logístico de imitación entre empresas: la velocidad de difusión aumenta con la rentabilidad de la innovación y disminuye con la inversión requerida.
- **Uso en el Motor:** AG-B16, MC-B02: difusión logística entre empresas de un sector según rentabilidad e inversión requerida de la innovación (AG-B06).
- **Limitaciones:** Datos industriales históricos de EE. UU.; volumen no indicado en la fuente.

#### DOC-MOT-0445 · Q 88 (A) — Bias and Systematic Change in the Parameter Estimates of Macro-Level Diffusion Models

- **Autores:** Christophe Van den Bulte; Gary L. Lilien
- **Año:** 1997
- **Publicación o institución:** Marketing Science, 16(4), 338-353
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-03 Modelos de difusión y curvas de adopción (principal) · secundarias: TMB-11
- **Calidad Q:** 88 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 7/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** https://ideas.repec.org/a/eee/intfor/v22y2006i3p519-545.html (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Meade Islam 2006 "Modelling and forecasting the diffusion of innovation" 25-year review International Journal of Forecasting»; WebFetch: sí, sobre la página índice https://ideas.repec.org/a/eee/intfor/v22y2006i3p519-545.html)
- **Contenido:** Documenta que los parámetros del modelo de Bass estimados con datos truncados están sesgados y derivan con el tamaño de la muestra.
- **Uso en el Motor:** AG-B16, MC-B02: aviso de sesgo de los parámetros de Bass estimados con datos truncados al inicio de la adopción (control de AG-B14 Contrarias).
- **Limitaciones:** Centrado en mínimos cuadrados no lineales.

#### DOC-MOT-0434 · Q 88 (A) — Diffusion of New Products: Empirical Generalizations and Managerial Uses

- **Autores:** Vijay Mahajan; Eitan Muller; Frank M. Bass
- **Año:** 1995
- **Publicación o institución:** Marketing Science, 14(3), G79-G88
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-03 Modelos de difusión y curvas de adopción (principal) · secundarias: —
- **Calidad Q:** 88 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.1287/mksc.14.3.G79 · https://en.wikipedia.org/wiki/Bass_diffusion_model (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Bass diffusion model" en.wikipedia.org»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Bass_diffusion_model)
- **Contenido:** Sintetiza regularidades empíricas de la difusión (valores típicos de p y q, momento del pico de ventas) y sus usos en decisiones.
- **Uso en el Motor:** AG-B16, MC-B02: generalizaciones empíricas (valores típicos de p y q) para fijar priors de adopción cuando hay pocos datos.
- **Limitaciones:** Muestras de bienes de consumo de EE. UU.

#### DOC-MOT-0438 · Q 88 (A) — New Product Diffusion Models in Marketing: A Review and Directions for Research

- **Autores:** Vijay Mahajan; Eitan Muller; Frank M. Bass
- **Año:** 1990
- **Publicación o institución:** Journal of Marketing, 54(1), 1-26
- **Tipo de documento:** Artículo de revisión revisado por pares
- **Temática:** TMB-03 Modelos de difusión y curvas de adopción (principal) · secundarias: —
- **Calidad Q:** 88 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** https://arxiv.org/pdf/2602.19488 (bibliografía de DOC-MOT-0429)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Meade Islam 2006 "Modelling and forecasting the diffusion of innovation" 25-year review International Journal of Forecasting»; WebFetch: sí, sobre la página índice https://arxiv.org/pdf/2602.19488)
- **Contenido:** Revisión de referencia de los modelos de difusión hasta 1990: estructura, estimación, extensiones y agenda de investigación.
- **Uso en el Motor:** AG-B16, MC-B02: revisión de extensiones de los modelos de difusión aplicables al dimensionado de mercados.
- **Limitaciones:** Revisión anterior a los modelos estocásticos y de agentes.

#### DOC-MOT-0439 · Q 87 (A) — Innovation Diffusion and New Product Growth Models: A Critical Review and Research Directions

- **Autores:** Renana Peres; Eitan Muller; Vijay Mahajan
- **Año:** 2010
- **Publicación o institución:** International Journal of Research in Marketing, 27(2), 91-106
- **Tipo de documento:** Artículo de revisión revisado por pares
- **Temática:** TMB-03 Modelos de difusión y curvas de adopción (principal) · secundarias: —
- **Calidad Q:** 87 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** https://arxiv.org/pdf/2602.19488 (bibliografía de DOC-MOT-0429)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Meade Islam 2006 "Modelling and forecasting the diffusion of innovation" 25-year review International Journal of Forecasting»; WebFetch: sí, sobre la página índice https://arxiv.org/pdf/2602.19488)
- **Contenido:** Actualiza la revisión de modelos de crecimiento de nuevos productos: redes sociales, efectos de red, difusión internacional y competencia.
- **Uso en el Motor:** AG-B16, MC-B02: revisión crítica de modelos de crecimiento de nuevos productos (redes sociales, efectos de red, internacional) para AG-B04.
- **Limitaciones:** Orientado a marketing de productos.

#### DOC-MOT-0444 · Q 87 (A) — On the Econometrics of the Bass Diffusion Model

- **Autores:** H. Peter Boswijk; Philip Hans Franses
- **Año:** 2005
- **Publicación o institución:** Journal of Business & Economic Statistics, 23, 255-268
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-03 Modelos de difusión y curvas de adopción (principal) · secundarias: TMB-02
- **Calidad Q:** 87 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 6/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** https://ideas.repec.org/a/eee/intfor/v22y2006i3p519-545.html (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Meade Islam 2006 "Modelling and forecasting the diffusion of innovation" 25-year review International Journal of Forecasting»; WebFetch: sí, sobre la página índice https://ideas.repec.org/a/eee/intfor/v22y2006i3p519-545.html)
- **Contenido:** Formula el modelo de Bass como ecuación diferencial estocástica y deriva su estimación e inferencia econométrica con errores heterocedásticos y autocorrelacionados.
- **Uso en el Motor:** AG-B16, MC-B02: estimación econométrica del modelo de Bass con inferencia válida (intervalos sobre m, p y q).
- **Limitaciones:** Requiere series de adopción largas.

#### DOC-MOT-0446 · Q 87 (A) — Models of Technology Diffusion

- **Autores:** Paul A. Geroski
- **Año:** 2000
- **Publicación o institución:** Research Policy, 29(4-5), 603-625
- **Tipo de documento:** Artículo de revisión revisado por pares
- **Temática:** TMB-03 Modelos de difusión y curvas de adopción (principal) · secundarias: —
- **Calidad Q:** 87 (A) — Tipo 25/25 · Rigor 14/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** https://ideas.repec.org/a/eee/intfor/v22y2006i3p519-545.html (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Meade Islam 2006 "Modelling and forecasting the diffusion of innovation" 25-year review International Journal of Forecasting»; WebFetch: sí, sobre la página índice https://ideas.repec.org/a/eee/intfor/v22y2006i3p519-545.html)
- **Contenido:** Revisa los modelos económicos de difusión (epidémico, probit o de heterogeneidad, legitimación y cascadas de información) y su relación con la curva S.
- **Uso en el Motor:** AG-B16, MC-B02: marco económico de la curva S (epidémico, probit, cascadas) para justificar el modelo de adopción elegido.
- **Limitaciones:** Revisión conceptual, sin estimaciones nuevas.

#### DOC-MOT-0442 · Q 87 (A) — Forecasting with Growth Curves: An Empirical Comparison

- **Autores:** Nigel Meade; Towhidul Islam
- **Año:** 1995
- **Publicación o institución:** International Journal of Forecasting, 11(2), 199-215
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-03 Modelos de difusión y curvas de adopción (principal) · secundarias: TMB-11
- **Calidad Q:** 87 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 7/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** https://ideas.repec.org/a/eee/intfor/v11y1995i2p199-215.html
- **Acceso y licencia:** Artículo de pago en el editor; ficha abierta en RePEc
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Meade Islam 2006 "Modelling and forecasting the diffusion of innovation" 25-year review International Journal of Forecasting»; WebFetch: sí, sobre la página índice https://ideas.repec.org/e/pis165.html)
- **Contenido:** Compara empíricamente diecisiete curvas de crecimiento (logística, Gompertz, etc.) en series de telecomunicaciones y su precisión fuera de muestra.
- **Uso en el Motor:** AG-B16, MC-B02: comparación empírica de curvas logística, Gompertz y otras para elegir la curva de crecimiento de un mercado.
- **Limitaciones:** Series de telecomunicaciones.

#### DOC-MOT-0436 · Q 87 (A) — A Meta-Analysis of Applications of Diffusion Models

- **Autores:** Fareena Sultan; John U. Farley; Donald R. Lehmann
- **Año:** 1990
- **Publicación o institución:** Journal of Marketing Research, 27(1), 70-77
- **Tipo de documento:** Artículo revisado por pares (metaanálisis)
- **Temática:** TMB-03 Modelos de difusión y curvas de adopción (principal) · secundarias: —
- **Calidad Q:** 87 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.1177/002224379002700107 · https://en.wikipedia.org/wiki/Bass_diffusion_model (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Bass diffusion model" en.wikipedia.org»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Bass_diffusion_model)
- **Contenido:** Metaanálisis de 213 aplicaciones del modelo de Bass: valores medios de p (≈0,03) y q (≈0,38) y factores que los explican.
- **Uso en el Motor:** AG-B16, MC-B02: metaanálisis de parámetros de difusión para priors por tipo de producto y región.
- **Limitaciones:** Aplicaciones anteriores a 1990.

#### DOC-MOT-0443 · Q 86 (A) — Technological Forecasting — Model Selection, Model Stability, and Combining Models

- **Autores:** Nigel Meade; Towhidul Islam
- **Año:** 1998
- **Publicación o institución:** Management Science, 44(8), 1115-1130
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-03 Modelos de difusión y curvas de adopción (principal) · secundarias: TMB-11
- **Calidad Q:** 86 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 7/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** https://ideas.repec.org/e/pis165.html (lista de publicaciones)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Meade Islam 2006 "Modelling and forecasting the diffusion of innovation" 25-year review International Journal of Forecasting»; WebFetch: sí, sobre la página índice https://ideas.repec.org/e/pis165.html)
- **Contenido:** Estudia la selección y estabilidad de modelos de difusión y muestra las ventajas de combinarlos para pronosticar.
- **Uso en el Motor:** AG-B16, MC-B02: combinación de modelos de difusión para pronósticos de adopción más estables.
- **Limitaciones:** Muestra de series tecnológicas limitada.

#### DOC-MOT-0107 · Q 85 (A) — Diffusion of Innovations (5.ª ed.)

- **Autores:** Everett M. Rogers
- **Año:** 2003
- **Publicación o institución:** Free Press (Simon & Schuster)
- **Tipo de documento:** Libro académico
- **Temática:** TMB-03 Modelos de difusión y curvas de adopción (principal) · secundarias: —
- **Calidad Q:** 85 (A) — Tipo 20/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** ISBN: 978-0-7432-5823-4 · https://en.wikipedia.org/wiki/Diffusion_of_innovations (bibliografía)
- **Acceso y licencia:** Libro de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Diffusion of innovations" en.wikipedia.org Rogers Griliches hybrid corn»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Diffusion_of_innovations)
- **Contenido:** Teoría clásica de la difusión: categorías de adoptantes, atributos de la innovación, canales y masa crítica.
- **Uso en el Motor:** AG-B16, MC-B02: categorías de adoptantes y factores cualitativos de la difusión que contextualizan el ajuste cuantitativo (AG-B04).
- **Limitaciones:** Teoría cualitativa; complementar con modelos cuantitativos.

#### DOC-MOT-0447 · Q 85 (A) — The Diffusion of Mobile Telecommunications Services in the European Union

- **Autores:** Harald Gruber; Frank Verboven
- **Año:** 2001
- **Publicación o institución:** European Economic Review, 45(3), 577-588
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-03 Modelos de difusión y curvas de adopción (principal) · secundarias: TMB-04
- **Calidad Q:** 85 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 7/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** https://ideas.repec.org/a/eee/intfor/v22y2006i3p519-545.html (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Meade Islam 2006 "Modelling and forecasting the diffusion of innovation" 25-year review International Journal of Forecasting»; WebFetch: sí, sobre la página índice https://ideas.repec.org/a/eee/intfor/v22y2006i3p519-545.html)
- **Contenido:** Estima la difusión de la telefonía móvil en los países de la UE y el efecto de la regulación, la competencia y el cambio tecnológico (analógico a digital).
- **Uso en el Motor:** AG-B16, MC-B02: ejemplo europeo de difusión con efecto de regulación y competencia (telefonía móvil) para AG-B07.
- **Limitaciones:** Periodo 1984-1997.

#### DOC-MOT-0437 · Q 85 (A) — Determination of Adopter Categories by Using Innovation Diffusion Models

- **Autores:** Vijay Mahajan; Eitan Muller; Rajendra K. Srivastava
- **Año:** 1990
- **Publicación o institución:** Journal of Marketing Research, 27(1), 37
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-03 Modelos de difusión y curvas de adopción (principal) · secundarias: —
- **Calidad Q:** 85 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 7/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.2307/3172549 · https://en.wikipedia.org/wiki/Bass_diffusion_model (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor (JSTOR 3172549)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Bass diffusion model" en.wikipedia.org»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Bass_diffusion_model)
- **Contenido:** Deriva las categorías de adoptantes de Rogers a partir de los puntos de inflexión del modelo de Bass.
- **Uso en el Motor:** AG-B16, MC-B02: localizar la fase de adopción de un mercado (innovadores, mayoría temprana, etc.) a partir del modelo de Bass ajustado.
- **Limitaciones:** Depende de la calidad del ajuste de Bass.

#### DOC-MOT-0432 · Q 82 (A) — Comments on «A New Product Growth for Model Consumer Durables»: The Bass Model

- **Autores:** Frank M. Bass
- **Año:** 2004
- **Publicación o institución:** Management Science, 50(12, suplemento), 1833-1840
- **Tipo de documento:** Artículo revisado por pares (comentario retrospectivo)
- **Temática:** TMB-03 Modelos de difusión y curvas de adopción (principal) · secundarias: —
- **Calidad Q:** 82 (A) — Tipo 22/25 · Rigor 12/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 7/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1287/mnsc.1040.0300 · https://en.wikipedia.org/wiki/Bass_diffusion_model (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Bass diffusion model" en.wikipedia.org»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Bass_diffusion_model)
- **Contenido:** Retrospectiva del autor sobre la génesis, extensiones y usos del modelo de Bass, incluido el pronóstico antes del lanzamiento por analogía.
- **Uso en el Motor:** AG-B16, MC-B02: comentario del propio Bass sobre el uso y los límites de su modelo.
- **Limitaciones:** Texto retrospectivo, no aporta nueva evidencia.

#### MBM-0042 · Q 81 (A) — Cross-Country Technology Adoption: Making the Theories Face the Facts

- **Autores:** Diego Comin; Bart Hobijn
- **Año:** 2004
- **Publicación o institución:** Journal of Monetary Economics, 51(1), 39-83
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-03 Modelos de difusión y curvas de adopción (principal) · secundarias: —
- **Calidad Q:** 81 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 5/10 · Impacto 8/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** Verificada en página índice (referencias de «The CHAT Dataset» en IDEAS): https://ideas.repec.org/p/nbr/nberwo/15319.html
- **Acceso y licencia:** Artículo de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Comin Hobijn 2010 "An Exploration of Technology Diffusion" American Economic Review CHAT dataset»; WebFetch: sí, sobre la página índice)
- **Contenido:** Documenta patrones de adopción de tecnologías entre países y sus determinantes (capital humano, apertura, instituciones).
- **Uso en el Motor:** AG-B16, MC-B02: variables explicativas de la velocidad de adopción por país para segmentar mercados geográficos.
- **Limitaciones:** Confirmada solo por página índice.

#### MBM-0044 · Q 81 (A) — Time Paths in the Diffusion of Product Innovations

- **Autores:** Michael Gort; Steven Klepper
- **Año:** 1982
- **Publicación o institución:** Economic Journal, 92(367), 630-653
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-03 Modelos de difusión y curvas de adopción (principal) · secundarias: TMB-04
- **Calidad Q:** 81 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 4/10 · Impacto 9/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** Verificada en página índice (referencias de «The CHAT Dataset» en IDEAS): https://ideas.repec.org/p/nbr/nberwo/15319.html
- **Acceso y licencia:** Artículo de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Comin Hobijn 2010 "An Exploration of Technology Diffusion" American Economic Review CHAT dataset»; WebFetch: sí, sobre la página índice)
- **Contenido:** Describe las fases de la difusión de innovaciones de producto según la evolución del número de productores: entrada neta, sacudida y estabilización.
- **Uso en el Motor:** AG-B16, MC-B02 y MC-B03: situar un mercado en su ciclo de vida (entrada, consolidación) y anticipar la evolución del número de competidores (AG-B03, AG-B13).
- **Limitaciones:** Confirmada solo por página índice; datos estadounidenses históricos.

#### MBM-0039 · Q 81 (A) — On the Nature of the Function Expressive of the Law of Human Mortality, and on a New Mode of Determining the Value of Life Contingencies

- **Autores:** Benjamin Gompertz
- **Año:** 1825
- **Publicación o institución:** Philosophical Transactions of the Royal Society of London, 115, 513-583
- **Tipo de documento:** Artículo científico histórico
- **Temática:** TMB-03 Modelos de difusión y curvas de adopción (principal) · secundarias: TMB-01
- **Calidad Q:** 81 (A) — Tipo 22/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 1/10 · Impacto 10/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** https://www.medicine.mcgill.ca/epidemiology/hanley/c609/material/Gompertz-1825.pdf
- **Acceso y licencia:** Dominio público (copia docente en McGill)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Gompertz function Wikipedia 1825 "On the Nature of the Function Expressive of the Law of Human Mortality" growth curve»; WebFetch: sí)
- **Contenido:** Artículo original de la función de Gompertz, curva sigmoidea asimétrica que hoy se usa para crecimiento y saturación de mercados.
- **Uso en el Motor:** AG-B16, MC-B02: curva de Gompertz como alternativa a la logística cuando la adopción se frena lentamente cerca de la saturación (AG-B04, AG-B13).
- **Limitaciones:** Formulado para mortalidad, no para mercados; la aplicación a adopción procede de la literatura posterior (DOC-MOT-0442).

#### DOC-MOT-0441 · Q 80 (A) — A Simple Substitution Model of Technological Change

- **Autores:** J. C. Fisher; R. H. Pry
- **Año:** 1971
- **Publicación o institución:** Technological Forecasting and Social Change, 3, 75-88
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-03 Modelos de difusión y curvas de adopción (principal) · secundarias: TMB-05
- **Calidad Q:** 80 (A) — Tipo 22/25 · Rigor 13/20 · Autoridad 13/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** https://arxiv.org/pdf/2602.19488 (bibliografía de DOC-MOT-0429)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Meade Islam 2006 "Modelling and forecasting the diffusion of innovation" 25-year review International Journal of Forecasting»; WebFetch: sí, sobre la página índice https://arxiv.org/pdf/2602.19488)
- **Contenido:** Modelo logístico de sustitución: la cuota de la tecnología nueva sigue una recta en escala logit.
- **Uso en el Motor:** AG-B16, MC-B02: sustitución logística de una tecnología por otra (cuota en escala logit), p. ej., vehículo eléctrico frente a combustión.
- **Limitaciones:** Supone sustitución completa y simétrica.

#### MBM-0043 · Q 79 (B) — Technology Usage Lags

- **Autores:** Diego Comin; Bart Hobijn; Emilie Rovito
- **Año:** 2008
- **Publicación o institución:** Journal of Economic Growth, 13(4), 237-256
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-03 Modelos de difusión y curvas de adopción (principal) · secundarias: —
- **Calidad Q:** 79 (B) — Tipo 25/25 · Rigor 15/20 · Autoridad 13/15 · Vigencia 6/10 · Impacto 7/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** Verificada en página índice (referencias de «The CHAT Dataset» en IDEAS): https://ideas.repec.org/p/nbr/nberwo/15319.html
- **Acceso y licencia:** Artículo de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Comin Hobijn 2010 "An Exploration of Technology Diffusion" American Economic Review CHAT dataset»; WebFetch: sí, sobre la página índice)
- **Contenido:** Mide los retardos de uso de tecnologías entre países y su relación con las diferencias de renta.
- **Uso en el Motor:** AG-B16, MC-B02: estimar cuántos años lleva un país al líder en la adopción de una tecnología.
- **Limitaciones:** Confirmada solo por página índice.

#### MBM-0041 · Q 78 (B) — The CHAT Dataset

- **Autores:** Diego A. Comin; Bart Hobijn
- **Año:** 2009
- **Publicación o institución:** NBER Working Paper 15319 (también HBS WP 10-035)
- **Tipo de documento:** Documento de trabajo con base de datos
- **Temática:** TMB-03 Modelos de difusión y curvas de adopción (principal) · secundarias: TMB-14
- **Calidad Q:** 78 (B) — Tipo 15/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 6/10 · Impacto 8/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://ideas.repec.org/p/nbr/nberwo/15319.html · datos: https://www.nber.org/research/data/cross-country-historical-adoption-technology
- **Acceso y licencia:** Acceso abierto (NBER)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Comin Hobijn 2010 "An Exploration of Technology Diffusion" American Economic Review CHAT dataset»; WebFetch: sí)
- **Contenido:** Describe la base CHAT: panel no equilibrado de adopción de más de 100 tecnologías en más de 150 países desde 1800, con alcance, limitaciones y usos.
- **Uso en el Motor:** AG-B16, MC-B02: datos históricos para calibrar curvas de adopción análogas (analogías de difusión) en el dimensionado de mercados.
- **Limitaciones:** Cobertura desigual por tecnología y país; datos hasta inicios del siglo XXI.

#### MBM-0045 · Q 75 (B) — Technology Adoption from Hybrid Corn to Beta-Blockers

- **Autores:** Jonathan Skinner; Douglas Staiger
- **Año:** 2007
- **Publicación o institución:** NBER, capítulo en «Hard-to-Measure Goods and Services», 545-570
- **Tipo de documento:** Capítulo de libro académico
- **Temática:** TMB-03 Modelos de difusión y curvas de adopción (principal) · secundarias: —
- **Calidad Q:** 75 (B) — Tipo 20/25 · Rigor 15/20 · Autoridad 13/15 · Vigencia 6/10 · Impacto 7/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** Verificada en página índice (referencias de «The CHAT Dataset» en IDEAS): https://ideas.repec.org/p/nbr/nberwo/15319.html
- **Acceso y licencia:** Capítulo NBER
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Comin Hobijn 2010 "An Exploration of Technology Diffusion" American Economic Review CHAT dataset»; WebFetch: sí, sobre la página índice)
- **Contenido:** Muestra que los estados de EE. UU. que adoptan pronto una tecnología tienden a adoptar pronto otras muy distintas (del maíz híbrido a tratamientos médicos).
- **Uso en el Motor:** AG-B16, MC-B02: persistencia regional de la adopción, útil para ordenar mercados geográficos por velocidad esperada.
- **Limitaciones:** Confirmada solo por página índice.

#### DOC-MOT-0429 · Q 72 (B) — The Dynamics of Innovation Diffusion: A Survey of Bass-Type Models

- **Autores:** Nicolas Langrené; Rui Liu; Xiangqin Wu; Tianhao Zhi
- **Año:** 2026
- **Publicación o institución:** arXiv 2602.19488 (Beijing Normal-Hong Kong Baptist University; Imperial College London; University of Southampton)
- **Tipo de documento:** Artículo de revisión (preprint)
- **Temática:** TMB-03 Modelos de difusión y curvas de adopción (principal) · secundarias: —
- **Calidad Q:** 72 (B) — Tipo 15/25 · Rigor 14/20 · Autoridad 10/15 · Vigencia 10/10 · Impacto 3/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://arxiv.org/pdf/2602.19488
- **Acceso y licencia:** Acceso abierto (arXiv)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Meade Islam 2006 "Modelling and forecasting the diffusion of innovation" 25-year review International Journal of Forecasting»; WebFetch: sí)
- **Contenido:** Revisión reciente de modelos tipo Bass: precios, multigeneración, multinacionales, versiones estocásticas, estimación frecuentista, bayesiana (filtro de Kalman) y metaheurística, y comparación con modelos de agentes.
- **Uso en el Motor:** AG-B16, MC-B02: revisión reciente de modelos tipo Bass y de métodos de estimación (bayesiana, filtro de Kalman).
- **Limitaciones:** Preprint sin revisión por pares constatada.

#### MBM-0046 · Q 72 (B) — Five Facts You Need to Know About Technology Diffusion

- **Autores:** Diego Comin; Bart Hobijn; Emilie Rovito
- **Año:** 2006
- **Publicación o institución:** NBER Working Paper 11928
- **Tipo de documento:** Documento de trabajo
- **Temática:** TMB-03 Modelos de difusión y curvas de adopción (principal) · secundarias: —
- **Calidad Q:** 72 (B) — Tipo 15/25 · Rigor 14/20 · Autoridad 13/15 · Vigencia 7/10 · Impacto 7/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** Verificada en página índice (referencias de «The CHAT Dataset» en IDEAS): https://ideas.repec.org/p/nbr/nberwo/15319.html
- **Acceso y licencia:** Documento de trabajo NBER
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Comin Hobijn 2010 "An Exploration of Technology Diffusion" American Economic Review CHAT dataset»; WebFetch: sí, sobre la página índice)
- **Contenido:** Resume hechos estilizados de la difusión de tecnologías entre países (dispersión de intensidad de uso, convergencia, papel de las nuevas tecnologías).
- **Uso en el Motor:** AG-B16, MC-B02: hechos estilizados para contrastar supuestos de adopción en escenarios.
- **Limitaciones:** Documento de trabajo; confirmada solo por página índice.

## TMB-04 Concentración, poder de mercado y márgenes

#### MBM-0069 · Q 95 (A) — The Rise of Market Power and the Macroeconomic Implications

- **Autores:** Jan De Loecker; Jan Eeckhout; Gabriel Unger
- **Año:** 2020
- **Publicación o institución:** The Quarterly Journal of Economics, 135(2), 561-644
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-04 Concentración, poder de mercado y márgenes (principal) · secundarias: TMB-06
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1093/qje/qjz041 · https://crei.cat/wp-content/uploads/2020/10/the-rise-1.pdf · https://ideas.repec.Org/p/nbr/nberwo/23687.html
- **Acceso y licencia:** Artículo de pago; copia del autor y NBER WP 23687 en abierto
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «De Loecker Eeckhout Unger 2020 "The Rise of Market Power and the Macroeconomic Implications" Quarterly Journal of Economics ideas.repec»; WebFetch: sí)
- **Contenido:** Estima márgenes precio-coste marginal a nivel de empresa con datos contables (enfoque de la función de producción) y documenta su fuerte aumento en EE. UU. desde 1980, concentrado en las empresas grandes.
- **Uso en el Motor:** AG-B16, MC-B03: estimar márgenes (markups) de las empresas de un sector a partir de estados financieros y seguir su evolución como indicador de poder de mercado (AG-B03, AG-B09).
- **Limitaciones:** Sensible a la elasticidad del input variable y al tratamiento de gastos generales (véase Basu 2019).

#### MBM-0073 · Q 90 (A) — The Fall of the Labor Share and the Rise of Superstar Firms

- **Autores:** David Autor; David Dorn; Lawrence F. Katz; Christina Patterson; John Van Reenen
- **Año:** 2020
- **Publicación o institución:** The Quarterly Journal of Economics, 135(2), 645-709
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-04 Concentración, poder de mercado y márgenes (principal) · secundarias: TMB-07
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** Verificada en página índice (referencias en IDEAS de NBER WP 23687): https://ideas.repec.Org/p/nbr/nberwo/23687.html
- **Acceso y licencia:** Artículo de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «De Loecker Eeckhout Unger 2020 "The Rise of Market Power and the Macroeconomic Implications" Quarterly Journal of Economics ideas.repec»; WebFetch: sí, sobre la página índice)
- **Contenido:** Relaciona el aumento de la concentración sectorial con empresas «superestrella» de alta productividad y con la caída de la participación del trabajo.
- **Uso en el Motor:** AG-B16, MC-B03: interpretar la concentración creciente como eficiencia de líderes o como poder de mercado al analizar un sector (AG-B03).
- **Limitaciones:** Confirmada solo por página índice.

#### MBM-0070 · Q 89 (A) — Markups and Firm-Level Export Status

- **Autores:** Jan De Loecker; Frederic Warzynski
- **Año:** 2012
- **Publicación o institución:** American Economic Review, 102(6), 2437-2471
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-04 Concentración, poder de mercado y márgenes (principal) · secundarias: —
- **Calidad Q:** 89 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 10/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** Verificada en página índice (referencias de De Loecker y Eeckhout, NBER WP 23687, en IDEAS): https://ideas.repec.Org/p/nbr/nberwo/23687.html
- **Acceso y licencia:** Artículo de pago (AEA)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «De Loecker Eeckhout Unger 2020 "The Rise of Market Power and the Macroeconomic Implications" Quarterly Journal of Economics ideas.repec»; WebFetch: sí, sobre la página índice)
- **Contenido:** Método para estimar márgenes empresa a empresa como cociente entre la elasticidad de producción de un input variable y su peso en los ingresos.
- **Uso en el Motor:** AG-B16, MC-B03: base metodológica del cálculo de márgenes por empresa en un sector.
- **Limitaciones:** Requiere estimar la función de producción; confirmada solo por página índice.

#### ANA-DOC-0454 · Q 89 (A) — Industry Concentration and Average Stock Returns

- **Autores:** Kewei Hou; David T. Robinson
- **Año:** 2006
- **Publicación o institución:** Journal of Finance, vol. 61, n.º 4, págs. 1927-1956
- **Tipo de documento:** Artículo revisado por pares (revista de primer nivel)
- **Temática:** TMB-04 Concentración, poder de mercado y márgenes (principal) · secundarias: TMB-07
- **Calidad Q:** 89 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 8/10 · Impacto 8/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1111/j.1540-6261.2006.00893.x · URL: https://ideas.repec.org/a/bla/jfinan/v61y2006i4p1927-1956.html
- **Acceso y licencia:** Peldaño 4 (versión editorial de pago, Wiley; ficha RePEc abierta)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Hou Robinson "Industry Concentration and Average Stock Returns" Journal of Finance 2006»; WebFetch: sí, ficha RePEc)
- **Contenido:** Las empresas de sectores muy concentrados obtienen menores rendimientos bursátiles medios tras controlar por tamaño, valor y momentum, por barreras de entrada que reducen el riesgo de distress o por menor innovación.
- **Uso en el Motor:** AG-B16, MC-B03 y MC-B07: traducir la concentración sectorial en expectativas de rentabilidad bursátil y usarla como variable de cribado (AG-B03, AG-B12 Seleccionador de Activos).
- **Limitaciones:** Medida de concentración basada en Compustat (solo cotizadas).

#### MBM-0072 · Q 88 (A) — Are Price-Cost Markups Rising in the United States? A Discussion of the Evidence

- **Autores:** Susanto Basu
- **Año:** 2019
- **Publicación o institución:** Journal of Economic Perspectives, 33(3), 3-22
- **Tipo de documento:** Artículo de revisión revisado por pares
- **Temática:** TMB-04 Concentración, poder de mercado y márgenes (principal) · secundarias: —
- **Calidad Q:** 88 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** Verificada en página índice (referencias en IDEAS de NBER WP 23687): https://ideas.repec.Org/p/nbr/nberwo/23687.html
- **Acceso y licencia:** Acceso abierto (AEA, JEP)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «De Loecker Eeckhout Unger 2020 "The Rise of Market Power and the Macroeconomic Implications" Quarterly Journal of Economics ideas.repec»; WebFetch: sí, sobre la página índice)
- **Contenido:** Revisa críticamente las distintas medidas de márgenes (función de producción, beneficios, demanda) y sus resultados divergentes.
- **Uso en el Motor:** AG-B16, MC-B03: contrastar márgenes estimados con varios métodos antes de concluir poder de mercado (AG-B14 Contrarias).
- **Limitaciones:** Revisión centrada en EE. UU.

#### MBM-0091 · Q 87 (A) — Herfindahl-Hirschman Index (y Merger Guidelines 2023, § 2.1)

- **Autores:** U.S. Department of Justice, Antitrust Division; Federal Trade Commission
- **Año:** 2024 (actualización del 17/01/2024)
- **Publicación o institución:** U.S. Department of Justice
- **Tipo de documento:** Documento oficial de autoridad de competencia
- **Temática:** TMB-04 Concentración, poder de mercado y márgenes (principal) · secundarias: TMB-13
- **Calidad Q:** 87 (A) — Tipo 18/25 · Rigor 14/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://www.justice.gov/atr/Herfindahl-hirschman-index
- **Acceso y licencia:** Acceso abierto (dominio público)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Herfindahl–Hirschman index Wikipedia Hirschman 1964 "The Paternity of an Index" American Economic Review»; WebFetch: sí)
- **Contenido:** Define el HHI y los umbrales vigentes de las Merger Guidelines de 2023: moderadamente concentrado 1.000-1.800, muy concentrado > 1.800, y presunción de daño si una operación sube el HHI más de 100 puntos en un mercado muy concentrado.
- **Uso en el Motor:** AG-B16, MC-B03: clasificar la concentración de un mercado y anticipar el riesgo regulatorio de fusiones (AG-B03, AG-B07 Regulación y Geopolítica).
- **Limitaciones:** Umbrales de EE. UU.; la UE usa otros (directrices de concentraciones horizontales).

#### MBM-0081 · Q 87 (A) — Identification Properties of Recent Production Function Estimators

- **Autores:** Daniel A. Ackerberg; Kevin Caves; Garth Frazer
- **Año:** 2015
- **Publicación o institución:** Econometrica, 83, 2411-2451
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-04 Concentración, poder de mercado y márgenes (principal) · secundarias: TMB-05
- **Calidad Q:** 87 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** Verificada en página índice (referencias en IDEAS de NBER WP 23687): https://ideas.repec.Org/p/nbr/nberwo/23687.html
- **Acceso y licencia:** Artículo de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «De Loecker Eeckhout Unger 2020 "The Rise of Market Power and the Macroeconomic Implications" Quarterly Journal of Economics ideas.repec»; WebFetch: sí, sobre la página índice)
- **Contenido:** Analiza la identificación de los estimadores de función de producción con variables proxy y propone un procedimiento alternativo (ACF).
- **Uso en el Motor:** AG-B16, MC-B03: estimar elasticidades de producción necesarias para calcular márgenes y productividad sectorial.
- **Limitaciones:** Confirmada solo por página índice.

#### MBM-0074 · Q 87 (A) — Measuring Market Power in the Ready-to-Eat Cereal Industry

- **Autores:** Aviv Nevo
- **Año:** 2001
- **Publicación o institución:** Econometrica, 69(2), 307-342
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-04 Concentración, poder de mercado y márgenes (principal) · secundarias: TMB-02
- **Calidad Q:** 87 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 6/10 · Impacto 10/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** Verificada en página índice (referencias en IDEAS de NBER WP 23687): https://ideas.repec.Org/p/nbr/nberwo/23687.html
- **Acceso y licencia:** Artículo de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «De Loecker Eeckhout Unger 2020 "The Rise of Market Power and the Macroeconomic Implications" Quarterly Journal of Economics ideas.repec»; WebFetch: sí, sobre la página índice)
- **Contenido:** Estima demanda de productos diferenciados y compara márgenes observados con los implícitos en distintas conductas (producto único, multiproducto, colusión).
- **Uso en el Motor:** AG-B16, MC-B03: atribuir los márgenes de un sector a diferenciación, carteras multiproducto o colusión.
- **Limitaciones:** Confirmada solo por página índice.

#### DOC-MOT-0515 · Q 86 (A) — The Herfindahl-Hirschman Index

- **Autores:** Stephen A. Rhoades
- **Año:** 1993
- **Publicación o institución:** Federal Reserve Bulletin (marzo de 1993), Board of Governors of the Federal Reserve System
- **Tipo de documento:** Artículo de publicación oficial de banco central
- **Temática:** TMB-04 Concentración, poder de mercado y márgenes (principal) · secundarias: TMB-01
- **Calidad Q:** 86 (A) — Tipo 20/25 · Rigor 14/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 9/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://fedinprint.org/item/fedgrb/15160
- **Acceso y licencia:** Acceso abierto (Fed in Print)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Rhoades 1993 "The Herfindahl-Hirschman Index" Federal Reserve Bulletin»; WebFetch: sí)
- **Contenido:** Explica la construcción del índice HHI (suma de cuadrados de las cuotas), su interpretación y los umbrales usados en defensa de la competencia.
- **Uso en el Motor:** AG-B16, MC-B03: cálculo e interpretación del HHI de un mercado y de su número equivalente de empresas (1/HHI) para AG-B03 Estructura y Competencia.
- **Limitaciones:** Pensado para concentración de mercado bancario, no de carteras; la ficha de Fed in Print no da páginas.

#### MBM-0082 · Q 85 (A) — The Dynamics of Productivity in the Telecommunications Equipment Industry

- **Autores:** G. Steven Olley; Ariel Pakes
- **Año:** 1996
- **Publicación o institución:** Econometrica, 64(6), 1263-1297
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-04 Concentración, poder de mercado y márgenes (principal) · secundarias: TMB-05
- **Calidad Q:** 85 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 5/10 · Impacto 10/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** Verificada en página índice (referencias en IDEAS de NBER WP 23687): https://ideas.repec.Org/p/nbr/nberwo/23687.html
- **Acceso y licencia:** Artículo de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «De Loecker Eeckhout Unger 2020 "The Rise of Market Power and the Macroeconomic Implications" Quarterly Journal of Economics ideas.repec»; WebFetch: sí, sobre la página índice)
- **Contenido:** Estimador de función de producción con selección y simultaneidad, y descomposición de la productividad agregada en media y reasignación de cuota.
- **Uso en el Motor:** AG-B16, MC-B03: medir si la productividad de un sector crece por mejora de las empresas o por reasignación de cuota hacia las mejores.
- **Limitaciones:** Confirmada solo por página índice.

#### MBM-0071 · Q 84 (A) — The Relation between Price and Marginal Cost in U.S. Industry

- **Autores:** Robert E. Hall
- **Año:** 1988
- **Publicación o institución:** Journal of Political Economy, 96(5), 921-947
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-04 Concentración, poder de mercado y márgenes (principal) · secundarias: TMB-05
- **Calidad Q:** 84 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 4/10 · Impacto 10/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** Verificada en página índice (referencias en IDEAS de NBER WP 23687): https://ideas.repec.Org/p/nbr/nberwo/23687.html
- **Acceso y licencia:** Artículo de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «De Loecker Eeckhout Unger 2020 "The Rise of Market Power and the Macroeconomic Implications" Quarterly Journal of Economics ideas.repec»; WebFetch: sí, sobre la página índice)
- **Contenido:** Estima márgenes sectoriales a partir de la relación entre crecimiento de la producción y de los inputs (residuo de Solow) y halla márgenes notables en muchas industrias.
- **Uso en el Motor:** AG-B16, MC-B03: estimación de márgenes con datos sectoriales agregados cuando no hay datos por empresa.
- **Limitaciones:** Supuestos de rendimientos constantes; confirmada solo por página índice.

#### MBM-0083 · Q 82 (A) — Market Structure and Productivity: A Concrete Example

- **Autores:** Chad Syverson
- **Año:** 2004
- **Publicación o institución:** Journal of Political Economy, 112(6), 1181-1222
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-04 Concentración, poder de mercado y márgenes (principal) · secundarias: TMB-05
- **Calidad Q:** 82 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 6/10 · Impacto 8/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** Verificada en página índice (referencias en IDEAS de NBER WP 23687): https://ideas.repec.Org/p/nbr/nberwo/23687.html
- **Acceso y licencia:** Artículo de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «De Loecker Eeckhout Unger 2020 "The Rise of Market Power and the Macroeconomic Implications" Quarterly Journal of Economics ideas.repec»; WebFetch: sí, sobre la página índice)
- **Contenido:** Muestra en el hormigón premezclado que mercados locales más densos (más competencia) tienen productividad media mayor y menos dispersa.
- **Uso en el Motor:** AG-B16, MC-B03: relación entre intensidad competitiva y dispersión de productividad o márgenes dentro de un sector.
- **Limitaciones:** Confirmada solo por página índice.

#### MBM-0084 · Q 81 (A) — Competition, Markups, and the Gains from International Trade

- **Autores:** Chris Edmond; Virgiliu Midrigan; Daniel Yi Xu
- **Año:** 2015
- **Publicación o institución:** American Economic Review, 105(10), 3183-3221
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-04 Concentración, poder de mercado y márgenes (principal) · secundarias: TMB-07
- **Calidad Q:** 81 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 13/15 · Vigencia 7/10 · Impacto 7/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** Verificada en página índice (referencias en IDEAS de NBER WP 23687): https://ideas.repec.Org/p/nbr/nberwo/23687.html
- **Acceso y licencia:** Artículo de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «De Loecker Eeckhout Unger 2020 "The Rise of Market Power and the Macroeconomic Implications" Quarterly Journal of Economics ideas.repec»; WebFetch: sí, sobre la página índice)
- **Contenido:** Modelo con márgenes variables según la cuota de la empresa: la apertura comercial reduce márgenes de las empresas grandes.
- **Uso en el Motor:** AG-B16, MC-B03: efecto de aranceles o apertura sobre márgenes del sector (AG-B07 Regulación y Geopolítica).
- **Limitaciones:** Calibrado con datos de Taiwán; confirmada solo por página índice.

#### MBM-0080 · Q 81 (A) — Econometric Tools for Analyzing Market Outcomes

- **Autores:** Daniel Ackerberg; C. Lanier Benkard; Steven Berry; Ariel Pakes
- **Año:** 2007
- **Publicación o institución:** Handbook of Econometrics, vol. 6, cap. 63, Elsevier
- **Tipo de documento:** Capítulo de manual (revisión)
- **Temática:** TMB-04 Concentración, poder de mercado y márgenes (principal) · secundarias: TMB-02
- **Calidad Q:** 81 (A) — Tipo 22/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 9/10 · Independencia 10/10 · Acceso 1/10
- **DOI / ISBN / URL:** Verificada en página índice (referencias en IDEAS de NBER WP 23687): https://ideas.repec.Org/p/nbr/nberwo/23687.html
- **Acceso y licencia:** Capítulo de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «De Loecker Eeckhout Unger 2020 "The Rise of Market Power and the Macroeconomic Implications" Quarterly Journal of Economics ideas.repec»; WebFetch: sí, sobre la página índice)
- **Contenido:** Revisión de la econometría de demanda de productos diferenciados, funciones de producción y dinámica industrial.
- **Uso en el Motor:** AG-B16, MC-B03 y MC-B05: manual de métodos de organización industrial empírica.
- **Limitaciones:** Confirmada solo por página índice.

#### MBM-0075 · Q 80 (A) — Empirical Studies of Industries with Market Power

- **Autores:** Timothy F. Bresnahan
- **Año:** 1989
- **Publicación o institución:** Handbook of Industrial Organization, vol. 2, cap. 17, 1011-1057, Elsevier
- **Tipo de documento:** Capítulo de manual (revisión)
- **Temática:** TMB-04 Concentración, poder de mercado y márgenes (principal) · secundarias: —
- **Calidad Q:** 80 (A) — Tipo 22/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 5/10 · Impacto 10/10 · Independencia 10/10 · Acceso 1/10
- **DOI / ISBN / URL:** Verificada en página índice (referencias en IDEAS de NBER WP 23687): https://ideas.repec.Org/p/nbr/nberwo/23687.html
- **Acceso y licencia:** Capítulo de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «De Loecker Eeckhout Unger 2020 "The Rise of Market Power and the Macroeconomic Implications" Quarterly Journal of Economics ideas.repec»; WebFetch: sí, sobre la página índice)
- **Contenido:** Revisión fundacional de la «nueva organización industrial empírica»: identificación de la conducta y del poder de mercado sin observar costes.
- **Uso en el Motor:** AG-B16, MC-B03: marco para estimar parámetros de conducta en un sector concreto.
- **Limitaciones:** Confirmada solo por página índice.

#### MBM-0085 · Q 80 (A) — The Concept of Monopoly and the Measurement of Monopoly Power

- **Autores:** Abba P. Lerner
- **Año:** 1934
- **Publicación o institución:** The Review of Economic Studies, 1(3), 157-175
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-04 Concentración, poder de mercado y márgenes (principal) · secundarias: —
- **Calidad Q:** 80 (A) — Tipo 25/25 · Rigor 14/20 · Autoridad 15/15 · Vigencia 3/10 · Impacto 10/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** DOI: 10.2307/2967480 · índice: https://en.wikipedia.org/wiki/Lerner_index
- **Acceso y licencia:** Artículo de pago (JSTOR)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Lerner index Wikipedia "The Concept of Monopoly and the Measurement of Monopoly Power" 1934 Review of Economic Studies»; WebFetch: sí, sobre la página índice)
- **Contenido:** Define el índice de Lerner, (P − CMg)/P, como medida del poder de monopolio, igual al inverso de la elasticidad de la demanda en el óptimo.
- **Uso en el Motor:** AG-B16, MC-B03: cálculo del índice de Lerner y su relación con la elasticidad de la demanda estimada en MC-B05.
- **Limitaciones:** Requiere coste marginal, rara vez observable.

#### MBM-0094 · Q 79 (B) — Economics of Regulation and Antitrust (5.ª ed.)

- **Autores:** W. Kip Viscusi; Joseph E. Harrington Jr.; David E. M. Sappington
- **Año:** 2018
- **Publicación o institución:** MIT Press
- **Tipo de documento:** Manual de referencia
- **Temática:** TMB-04 Concentración, poder de mercado y márgenes (principal) · secundarias: TMB-13
- **Calidad Q:** 79 (B) — Tipo 22/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 10/10 · Acceso 1/10
- **DOI / ISBN / URL:** ISBN: 978-0-262-03806-5 · índice: https://en.wikipedia.org/wiki/Herfindahl%E2%80%93Hirschman_index
- **Acceso y licencia:** Libro de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Herfindahl–Hirschman index Wikipedia Hirschman 1964 "The Paternity of an Index" American Economic Review»; WebFetch: sí, sobre la página índice)
- **Contenido:** Manual de defensa de la competencia y regulación: medidas de concentración, fusiones, colusión, monopolización y regulación de precios.
- **Uso en el Motor:** AG-B16, MC-B03: referencia de medidas de concentración y de análisis de fusiones para AG-B03 y AG-B07.
- **Limitaciones:** Enfoque estadounidense.

#### MBM-0078 · Q 79 (B) — Testing Static Oligopoly Models: Conduct and Cost in the Sugar Industry, 1890-1914

- **Autores:** David Genesove; Wallace P. Mullin
- **Año:** 1998
- **Publicación o institución:** RAND Journal of Economics, 29(2), 355-377
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-04 Concentración, poder de mercado y márgenes (principal) · secundarias: —
- **Calidad Q:** 79 (B) — Tipo 25/25 · Rigor 16/20 · Autoridad 13/15 · Vigencia 4/10 · Impacto 8/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** Verificada en página índice (referencias en IDEAS de NBER WP 23687): https://ideas.repec.Org/p/nbr/nberwo/23687.html
- **Acceso y licencia:** Artículo de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «De Loecker Eeckhout Unger 2020 "The Rise of Market Power and the Macroeconomic Implications" Quarterly Journal of Economics ideas.repec»; WebFetch: sí, sobre la página índice)
- **Contenido:** Contrasta los métodos de estimación de conducta frente a costes marginales observados en la industria del azúcar.
- **Uso en el Motor:** AG-B16, MC-B03: validación de cuánto fían los métodos de conducta para medir poder de mercado.
- **Limitaciones:** Caso histórico; confirmada solo por página índice.

#### MBM-0077 · Q 79 (B) — Departures from Marginal-Cost Pricing in the American Automobile Industry: Estimates for 1977-1978

- **Autores:** Timothy F. Bresnahan
- **Año:** 1981
- **Publicación o institución:** Journal of Econometrics, 17(2), 201-227
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-04 Concentración, poder de mercado y márgenes (principal) · secundarias: TMB-02
- **Calidad Q:** 79 (B) — Tipo 25/25 · Rigor 16/20 · Autoridad 13/15 · Vigencia 4/10 · Impacto 8/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** Verificada en página índice (referencias de Nevo 2000 en IDEAS): https://ideas.repec.Org/a/bla/jemstr/v9y2000i4p513-548.html
- **Acceso y licencia:** Artículo de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Berry Levinsohn Pakes 1995 "Automobile Prices in Market Equilibrium" Nevo "A Practitioner's Guide to Estimation of Random-Coefficients Logit Models of Demand"»; WebFetch: sí, sobre la página índice)
- **Contenido:** Estima márgenes sobre coste marginal por modelo de automóvil con un modelo de productos diferenciados verticalmente.
- **Uso en el Motor:** AG-B16, MC-B03: ejemplo aplicado de márgenes por producto en una industria oligopolística.
- **Limitaciones:** Confirmada solo por página índice.

#### MBM-0076 · Q 78 (B) — The Oligopoly Solution Concept Is Identified

- **Autores:** Timothy F. Bresnahan
- **Año:** 1982
- **Publicación o institución:** Economics Letters, 10(1-2), 87-92
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-04 Concentración, poder de mercado y márgenes (principal) · secundarias: —
- **Calidad Q:** 78 (B) — Tipo 25/25 · Rigor 15/20 · Autoridad 13/15 · Vigencia 4/10 · Impacto 8/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** Verificada en página índice (referencias en IDEAS de NBER WP 23687): https://ideas.repec.Org/p/nbr/nberwo/23687.html
- **Acceso y licencia:** Artículo de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «De Loecker Eeckhout Unger 2020 "The Rise of Market Power and the Macroeconomic Implications" Quarterly Journal of Economics ideas.repec»; WebFetch: sí, sobre la página índice)
- **Contenido:** Muestra que la conducta oligopolística es identificable con datos de mercado si la demanda rota con variables exógenas.
- **Uso en el Motor:** AG-B16, MC-B03: fundamento de la estimación del grado de competencia de un mercado.
- **Limitaciones:** Confirmada solo por página índice.

#### MBM-0079 · Q 75 (B) — Estimating Market Power: Evidence from the US Brewing Industry

- **Autores:** Jan De Loecker; Paul T. Scott
- **Año:** 2016
- **Publicación o institución:** NBER Working Paper 22957
- **Tipo de documento:** Documento de trabajo
- **Temática:** TMB-04 Concentración, poder de mercado y márgenes (principal) · secundarias: —
- **Calidad Q:** 75 (B) — Tipo 15/25 · Rigor 16/20 · Autoridad 13/15 · Vigencia 8/10 · Impacto 7/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** Verificada en página índice (referencias en IDEAS de NBER WP 23687): https://ideas.repec.Org/p/nbr/nberwo/23687.html
- **Acceso y licencia:** Documento de trabajo NBER
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «De Loecker Eeckhout Unger 2020 "The Rise of Market Power and the Macroeconomic Implications" Quarterly Journal of Economics ideas.repec»; WebFetch: sí, sobre la página índice)
- **Contenido:** Compara márgenes estimados por el enfoque de demanda (BLP) y por el de la función de producción en la cerveza de EE. UU.
- **Uso en el Motor:** AG-B16, MC-B03: contraste cruzado de los dos enfoques de márgenes en un sector concreto.
- **Limitaciones:** Documento de trabajo; confirmada solo por página índice.

#### MBM-0086 · Q 75 (B) — The Lerner Index of Monopoly Power: Origins and Uses

- **Autores:** Kenneth G. Elzinga; David E. Mills
- **Año:** 2011 (sesión AEA)
- **Publicación o institución:** American Economic Association, congreso anual 2011 (versión de prepublicación)
- **Tipo de documento:** Artículo académico (prepublicación)
- **Temática:** TMB-04 Concentración, poder de mercado y márgenes (principal) · secundarias: —
- **Calidad Q:** 75 (B) — Tipo 15/25 · Rigor 14/20 · Autoridad 13/15 · Vigencia 8/10 · Impacto 6/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** https://aeaweb.org/conference/2011/retrieve.php?pdfid=222
- **Acceso y licencia:** Acceso abierto (AEA)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Lerner index Wikipedia "The Concept of Monopoly and the Measurement of Monopoly Power" 1934 Review of Economic Studies»; WebFetch: sí)
- **Contenido:** Repasa el origen del índice de Lerner, sus usos en economía industrial y defensa de la competencia y sus limitaciones prácticas.
- **Uso en el Motor:** AG-B16, MC-B03: guía para interpretar el índice de Lerner y evitar errores al usarlo con datos contables.
- **Limitaciones:** Versión de prepublicación sin fecha visible.

#### MBM-0087 · Q 75 (B) — Market Power in Antitrust Cases

- **Autores:** William M. Landes; Richard A. Posner
- **Año:** 1981
- **Publicación o institución:** Harvard Law Review, 94, 937-996
- **Tipo de documento:** Artículo revisado (revista jurídica)
- **Temática:** TMB-04 Concentración, poder de mercado y márgenes (principal) · secundarias: —
- **Calidad Q:** 75 (B) — Tipo 22/25 · Rigor 13/20 · Autoridad 14/15 · Vigencia 4/10 · Impacto 9/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** Verificada en página índice (referencias de Elzinga y Mills): https://aeaweb.org/conference/2011/retrieve.php?pdfid=222
- **Acceso y licencia:** Artículo de revista jurídica
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Lerner index Wikipedia "The Concept of Monopoly and the Measurement of Monopoly Power" 1934 Review of Economic Studies»; WebFetch: sí, sobre la página índice)
- **Contenido:** Relaciona cuota de mercado, elasticidad de la demanda del mercado y oferta de los rivales con el índice de Lerner de la empresa.
- **Uso en el Motor:** AG-B16, MC-B03: inferir poder de mercado de una empresa a partir de su cuota y de elasticidades (AG-B03, AG-B07).
- **Limitaciones:** Confirmada solo por página índice.

#### MBM-0088 · Q 74 (B) — The Profit Rate as a Measure of Monopoly Power

- **Autores:** Joe S. Bain
- **Año:** 1941
- **Publicación o institución:** Quarterly Journal of Economics, 55, 271-293
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-04 Concentración, poder de mercado y márgenes (principal) · secundarias: TMB-06
- **Calidad Q:** 74 (B) — Tipo 25/25 · Rigor 12/20 · Autoridad 14/15 · Vigencia 2/10 · Impacto 8/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** Verificada en página índice (referencias de Elzinga y Mills): https://aeaweb.org/conference/2011/retrieve.php?pdfid=222
- **Acceso y licencia:** Artículo de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Lerner index Wikipedia "The Concept of Monopoly and the Measurement of Monopoly Power" 1934 Review of Economic Studies»; WebFetch: sí, sobre la página índice)
- **Contenido:** Analiza si la tasa de beneficio contable sirve como medida de poder de monopolio y sus problemas de medición.
- **Uso en el Motor:** AG-B16, MC-B03: cautelas al usar ROIC o márgenes contables como indicador de poder de mercado.
- **Limitaciones:** Antiguo; confirmada solo por página índice.

#### MBM-0093 · Q 70 (B) — Large Firm Dominance and Price-Cost Margins in Manufacturing Industries

- **Autores:** John E. Kwoka Jr.
- **Año:** 1977
- **Publicación o institución:** Southern Economic Journal, 44(1), 183-189
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-04 Concentración, poder de mercado y márgenes (principal) · secundarias: —
- **Calidad Q:** 70 (B) — Tipo 25/25 · Rigor 12/20 · Autoridad 11/15 · Vigencia 3/10 · Impacto 6/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** DOI: 10.2307/1057315 · índice: https://en.wikipedia.org/wiki/Herfindahl%E2%80%93Hirschman_index
- **Acceso y licencia:** Artículo de pago (JSTOR)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Herfindahl–Hirschman index Wikipedia Hirschman 1964 "The Paternity of an Index" American Economic Review»; WebFetch: sí, sobre la página índice)
- **Contenido:** Relaciona la cuota de las mayores empresas con los márgenes precio-coste en la industria manufacturera.
- **Uso en el Motor:** AG-B16, MC-B03: evidencia de que el tamaño relativo de los líderes (no solo el HHI) explica márgenes.
- **Limitaciones:** Antiguo; confirmada solo por página índice.

#### MBM-0092 · Q 70 (B) — Comment on the «H» Concentration Measure as a Numbers-Equivalent

- **Autores:** M. A. Adelman
- **Año:** 1969
- **Publicación o institución:** Review of Economics and Statistics, 51(1), 99-101
- **Tipo de documento:** Nota en revista revisada por pares
- **Temática:** TMB-04 Concentración, poder de mercado y márgenes (principal) · secundarias: —
- **Calidad Q:** 70 (B) — Tipo 25/25 · Rigor 11/20 · Autoridad 12/15 · Vigencia 2/10 · Impacto 7/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** DOI: 10.2307/1926955 · índice: https://en.wikipedia.org/wiki/Herfindahl%E2%80%93Hirschman_index
- **Acceso y licencia:** Artículo de pago (JSTOR)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Herfindahl–Hirschman index Wikipedia Hirschman 1964 "The Paternity of an Index" American Economic Review»; WebFetch: sí, sobre la página índice)
- **Contenido:** Interpreta el inverso del HHI como número equivalente de empresas de igual tamaño.
- **Uso en el Motor:** AG-B16, MC-B03: traducir el HHI a «número efectivo de competidores» en los informes de AG-B03.
- **Limitaciones:** Nota breve.

#### MBM-0089 · Q 69 (B) — The Paternity of an Index

- **Autores:** Albert O. Hirschman
- **Año:** 1964
- **Publicación o institución:** American Economic Review, 54(5), 761-762
- **Tipo de documento:** Nota en revista revisada por pares
- **Temática:** TMB-04 Concentración, poder de mercado y márgenes (principal) · secundarias: —
- **Calidad Q:** 69 (B) — Tipo 15/25 · Rigor 10/20 · Autoridad 13/15 · Vigencia 3/10 · Impacto 10/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** JSTOR 1818582 · índice: https://en.wikipedia.org/wiki/Herfindahl%E2%80%93Hirschman_index
- **Acceso y licencia:** Nota breve (JSTOR)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Herfindahl–Hirschman index Wikipedia Hirschman 1964 "The Paternity of an Index" American Economic Review»; WebFetch: sí, sobre la página índice)
- **Contenido:** Nota en la que Hirschman reclama la autoría del índice de concentración por suma de cuadrados de cuotas, propuesto por él en 1945 antes que Herfindahl.
- **Uso en el Motor:** AG-B16, MC-B03: cita de origen del índice HHI.
- **Limitaciones:** Nota histórica sin contenido metodológico nuevo.

#### MBM-0090 · Q 69 (B) — Concentration in the Steel Industry

- **Autores:** Orris C. Herfindahl
- **Año:** 1950
- **Publicación o institución:** Tesis doctoral; publicada en Archive.org en 2021 con permiso de los herederos
- **Tipo de documento:** Tesis doctoral
- **Temática:** TMB-04 Concentración, poder de mercado y márgenes (principal) · secundarias: —
- **Calidad Q:** 69 (B) — Tipo 15/25 · Rigor 13/20 · Autoridad 12/15 · Vigencia 2/10 · Impacto 9/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** https://archive.org/details/herfindahl-concentration-in-the-steel-industry-1950-publish/ · índice: https://en.wikipedia.org/wiki/Herfindahl%E2%80%93Hirschman_index
- **Acceso y licencia:** Acceso abierto (Archive.org)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Herfindahl–Hirschman index Wikipedia Hirschman 1964 "The Paternity of an Index" American Economic Review»; WebFetch: sí, sobre la página índice)
- **Contenido:** Tesis que aplica el índice de suma de cuadrados de cuotas a la concentración de la siderurgia estadounidense.
- **Uso en el Motor:** AG-B16, MC-B03: origen aplicado del HHI a un sector concreto.
- **Limitaciones:** Histórica; confirmada por página índice y enlace de Archive.org no leído.

## TMB-05 Curvas de costes, de aprendizaje y de capacidad

#### MBM-0047 · Q 96 (A) — Empirically Grounded Technology Forecasts and the Energy Transition

- **Autores:** Rupert Way; Matthew Ives; Penny Mealy; J. Doyne Farmer
- **Año:** 2022
- **Publicación o institución:** Joule, 6(9), 2057-2082
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-05 Curvas de costes, de aprendizaje y de capacidad (principal) · secundarias: TMB-03, TMB-08
- **Calidad Q:** 96 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** DOI: 10.1016/j.joule.2022.08.009 · https://ora.ox.ac.uk/objects/uuid:17256b64-f822-40ef-8770-5d0fa1ddc73e
- **Acceso y licencia:** Acceso abierto (CC BY 4.0)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Way Ives Mealy Farmer 2022 "Empirically grounded technology forecasts and the energy transition" Joule»; WebFetch: sí)
- **Contenido:** Aplica métodos de previsión de costes validados con backtesting en muchas tecnologías (ley de Wright estocástica) a solar, eólica, baterías y electrolizadores, y estima el coste de distintas trayectorias de transición energética.
- **Uso en el Motor:** AG-B16, MC-B04 y MC-B08: proyección probabilística de costes unitarios de tecnologías y escenarios de coste sectorial (AG-B05, AG-B06, AG-B11, AG-B13).
- **Limitaciones:** Supone continuidad de las tendencias de aprendizaje; no modela restricciones de materias primas.

#### DOC-MOT-0110 · Q 93 (A) — Statistical Basis for Predicting Technological Progress

- **Autores:** Béla Nagy; J. Doyne Farmer; Quan M. Bui; Jessika E. Trancik
- **Año:** 2013
- **Publicación o institución:** PLoS ONE, 8(2), e52669
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-05 Curvas de costes, de aprendizaje y de capacidad (principal) · secundarias: TMB-03
- **Calidad Q:** 93 (A) — Tipo 23/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** DOI: 10.1371/journal.pone.0052669 · https://en.wikipedia.org/wiki/Experience_curve_effect (bibliografía)
- **Acceso y licencia:** Acceso abierto (PLoS)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Experience curve effects" en.wikipedia.org Wright's law»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Experience_curve_effect)
- **Contenido:** Compara la capacidad predictiva de las leyes de Moore, Wright, Goddard y otras con datos de 62 tecnologías; Wright y Moore rinden de forma parecida.
- **Uso en el Motor:** AG-B16, MC-B04: comparar las leyes de Wright y Moore para proyectar costes unitarios de una tecnología (AG-B05 Oferta, AG-B06 Tecnología).
- **Limitaciones:** Base de datos histórica limitada.

#### DOC-MOT-0111 · Q 90 (A) — How Predictable Is Technological Progress?

- **Autores:** J. Doyne Farmer; François Lafond
- **Año:** 2016
- **Publicación o institución:** Research Policy, 45(3), 647-665
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-05 Curvas de costes, de aprendizaje y de capacidad (principal) · secundarias: TMB-11
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** https://arxiv.org/pdf/1703.05979 (bibliografía de Lafond et al., DOC-MOT-0428)
- **Acceso y licencia:** Artículo de pago en el editor; preprint en arXiv
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Experience curve effects" en.wikipedia.org Wright's law»; WebFetch: sí, sobre la página índice https://arxiv.org/pdf/1703.05979)
- **Contenido:** Modela el coste tecnológico como paseo aleatorio con deriva y autocorrelación y obtiene pronósticos probabilísticos validados fuera de muestra.
- **Uso en el Motor:** AG-B16, MC-B04: pronósticos distribucionales del coste de tecnologías con intervalos validados por backtesting.
- **Limitaciones:** Supone continuidad de la tendencia histórica. El DOI de la semilla no se ha visto y se retira.

#### DOC-MOT-0430 · Q 90 (A) — The Economic Implications of Learning by Doing

- **Autores:** Kenneth J. Arrow
- **Año:** 1962
- **Publicación o institución:** The Review of Economic Studies, 155-173
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-05 Curvas de costes, de aprendizaje y de capacidad (principal) · secundarias: —
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** https://arxiv.org/pdf/1703.05979 (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor (JSTOR/OUP)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Experience curve effects" en.wikipedia.org Wright's law»; WebFetch: sí, sobre la página índice https://arxiv.org/pdf/1703.05979)
- **Contenido:** Formaliza el aprendizaje por la práctica: la productividad crece con la experiencia acumulada (inversión acumulada), fundamento económico de las curvas de aprendizaje.
- **Uso en el Motor:** AG-B16, MC-B04: fundamento teórico del aprendizaje por la práctica (coste decreciente con la producción acumulada).
- **Limitaciones:** Modelo teórico agregado; volumen y DOI no figuran en la fuente consultada.

#### DOC-MOT-0428 · Q 87 (A) — How Well Do Experience Curves Predict Technological Progress? A Method for Making Distributional Forecasts

- **Autores:** François Lafond; Aimee Gotway Bailey; Jan David Bakker; Dylan Rebois; Rubina Zadourian; Patrick McSharry; J. Doyne Farmer
- **Año:** 2017
- **Publicación o institución:** arXiv 1703.05979 (versión de 18-09-2017)
- **Tipo de documento:** Documento de trabajo (preprint)
- **Temática:** TMB-05 Curvas de costes, de aprendizaje y de capacidad (principal) · secundarias: TMB-11
- **Calidad Q:** 87 (A) — Tipo 20/25 · Rigor 17/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 7/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://arxiv.org/pdf/1703.05979
- **Acceso y licencia:** Acceso abierto (arXiv)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «"Experience curve effects" en.wikipedia.org Wright's law»; WebFetch: sí)
- **Contenido:** Método de pronóstico distribucional con curvas de experiencia (primeras diferencias con ruido autocorrelacionado), validado con 51 tecnologías y aplicado a módulos fotovoltaicos.
- **Uso en el Motor:** AG-B16, MC-B04: método para pronósticos distribucionales con curvas de experiencia (Wright) y su incertidumbre.
- **Limitaciones:** Se cita la versión preprint; no se confirmó la revista de publicación.

#### DOC-MOT-0431 · Q 85 (A) — Learning Rates for Energy Technologies

- **Autores:** Alan McDonald; Leo Schrattenholzer
- **Año:** 2001
- **Publicación o institución:** Energy Policy, 29(4), 255-261
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-05 Curvas de costes, de aprendizaje y de capacidad (principal) · secundarias: TMB-03
- **Calidad Q:** 85 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 13/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** https://arxiv.org/pdf/1703.05979 (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Experience curve effects" en.wikipedia.org Wright's law»; WebFetch: sí, sobre la página índice https://arxiv.org/pdf/1703.05979)
- **Contenido:** Recopila tasas de aprendizaje de 26 tecnologías energéticas y muestra su dispersión y su descenso con la madurez.
- **Uso en el Motor:** AG-B16, MC-B04: tasas de aprendizaje de referencia de tecnologías energéticas para escenarios de coste (AG-B11 Sostenibilidad).
- **Limitaciones:** Datos anteriores a 2000; fuentes heterogéneas.

#### MBM-0050 · Q 85 (A) — Learning and Forgetting: The Dynamics of Aircraft Production

- **Autores:** C. Lanier Benkard
- **Año:** 2000
- **Publicación o institución:** American Economic Review, 90(4), 1034-1054
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-05 Curvas de costes, de aprendizaje y de capacidad (principal) · secundarias: TMB-04
- **Calidad Q:** 85 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 14/15 · Vigencia 6/10 · Impacto 9/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** Verificada en página índice (referencias de Levitt, List y Syverson, NBER WP 18017): https://www.nber.org/papers/w18017.pdf
- **Acceso y licencia:** Artículo de pago (AEA)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Levitt List Syverson "Toward an Understanding of Learning by Doing: Evidence from an Automobile Assembly Plant" Journal of Political Economy 2013»; WebFetch: sí, sobre la página índice)
- **Contenido:** Estima aprendizaje y olvido organizativo en la producción del Lockheed L-1011: la experiencia se deprecia y cae al cambiar de modelo.
- **Uso en el Motor:** AG-B16, MC-B04: incorporar depreciación de la experiencia al proyectar costes en sectores con producción discontinua (aeroespacial, naval).
- **Limitaciones:** Confirmada solo por página índice.

#### DOC-MOT-0109 · Q 85 (A) — Factors Affecting the Cost of Airplanes

- **Autores:** Theodore P. Wright
- **Año:** 1936
- **Publicación o institución:** Journal of the Aeronautical Sciences, 3(4), 122-128
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-05 Curvas de costes, de aprendizaje y de capacidad (principal) · secundarias: —
- **Calidad Q:** 85 (A) — Tipo 22/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.2514/8.155 · https://en.wikipedia.org/wiki/Experience_curve_effect (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Experience curve effects" en.wikipedia.org Wright's law»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Experience_curve_effect)
- **Contenido:** Formula la curva de aprendizaje (ley de Wright): el coste unitario cae un porcentaje fijo cada vez que se duplica la producción acumulada.
- **Uso en el Motor:** AG-B16, MC-B04: ley de Wright original (coste unitario frente a producción acumulada) para estimar la tasa de aprendizaje de un sector.
- **Limitaciones:** Tasa de aprendizaje no constante entre tecnologías.

#### MBM-0067 · Q 83 (A) — Industrial Production and Capacity Utilization (G.17): Capacity and Capacity Utilization — metodología

- **Autores:** Board of Governors of the Federal Reserve System
- **Año:** 2026 (página vigente)
- **Publicación o institución:** Federal Reserve Board
- **Tipo de documento:** Documentación metodológica oficial
- **Temática:** TMB-05 Curvas de costes, de aprendizaje y de capacidad (principal) · secundarias: TMB-14
- **Calidad Q:** 83 (A) — Tipo 15/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://www.federalreserve.gov/RELEASES/G17/Meth/MethCap.htm
- **Acceso y licencia:** Acceso abierto (dominio público)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Federal Reserve G.17 industrial production and capacity utilization explanatory notes methodology capacity estimates»; WebFetch: sí)
- **Contenido:** Define la capacidad como producción máxima sostenible, explica cómo se construyen los índices de capacidad de 89 industrias (encuesta de capacidad del Census, capital, edad del capital) y cómo se calcula la utilización.
- **Uso en el Motor:** AG-B16, MC-B04: interpretar y usar tasas de utilización sectoriales como indicador de tensión de oferta o exceso de capacidad (AG-B05, AG-B08).
- **Limitaciones:** Solo EE. UU.; capacidad interpolada entre estimaciones anuales.

#### MBM-0052 · Q 82 (A) — How Much Did the Liberty Shipbuilders Learn? New Evidence for an Old Case Study

- **Autores:** Peter Thompson
- **Año:** 2001
- **Publicación o institución:** Journal of Political Economy, 109(1), 103-137
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-05 Curvas de costes, de aprendizaje y de capacidad (principal) · secundarias: —
- **Calidad Q:** 82 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 5/10 · Impacto 8/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** Verificada en página índice (referencias de Levitt, List y Syverson, NBER WP 18017): https://www.nber.org/papers/w18017.pdf
- **Acceso y licencia:** Artículo de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Levitt List Syverson "Toward an Understanding of Learning by Doing: Evidence from an Automobile Assembly Plant" Journal of Political Economy 2013»; WebFetch: sí, sobre la página índice)
- **Contenido:** Reexamina el caso clásico de los astilleros Liberty y muestra que parte de la mejora atribuida al aprendizaje se debe a inversión de capital y cambios de calidad.
- **Uso en el Motor:** AG-B16, MC-B04: cautela al atribuir toda la caída de costes al aprendizaje (control de AG-B14 Contrarias).
- **Limitaciones:** Confirmada solo por página índice.

#### MBM-0049 · Q 82 (A) — Learning Curves in Manufacturing

- **Autores:** Linda Argote; Dennis Epple
- **Año:** 1990
- **Publicación o institución:** Science, 247(4945), 920-924
- **Tipo de documento:** Artículo revisado por pares (revisión)
- **Temática:** TMB-05 Curvas de costes, de aprendizaje y de capacidad (principal) · secundarias: —
- **Calidad Q:** 82 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 5/10 · Impacto 10/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** Verificada en página índice (referencias de Levitt, List y Syverson, NBER WP 18017): https://www.nber.org/papers/w18017.pdf
- **Acceso y licencia:** Artículo de pago (AAAS)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Levitt List Syverson "Toward an Understanding of Learning by Doing: Evidence from an Automobile Assembly Plant" Journal of Political Economy 2013»; WebFetch: sí, sobre la página índice)
- **Contenido:** Revisión de la evidencia de curvas de aprendizaje en fabricación: heterogeneidad de tasas, olvido organizativo y transferencia de conocimiento entre plantas.
- **Uso en el Motor:** AG-B16, MC-B04: rangos y causas de variación de las tasas de aprendizaje entre empresas de un sector.
- **Limitaciones:** Confirmada solo por página índice.

#### MBM-0051 · Q 81 (A) — Toward an Understanding of Learning by Doing: Evidence from an Automobile Assembly Plant

- **Autores:** Steven D. Levitt; John A. List; Chad Syverson
- **Año:** 2012
- **Publicación o institución:** NBER Working Paper 18017 (versión publicada en Journal of Political Economy, 2013)
- **Tipo de documento:** Documento de trabajo (publicado después en revista)
- **Temática:** TMB-05 Curvas de costes, de aprendizaje y de capacidad (principal) · secundarias: —
- **Calidad Q:** 81 (A) — Tipo 15/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 7/10 · Impacto 8/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://www.nber.org/papers/w18017.pdf · https://www.nber.org/papers/18017
- **Acceso y licencia:** Acceso abierto (NBER)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Levitt List Syverson "Toward an Understanding of Learning by Doing: Evidence from an Automobile Assembly Plant" Journal of Political Economy 2013»; WebFetch: sí)
- **Contenido:** Con datos detallados de producción de una planta de montaje de automóviles, documenta un aprendizaje rápido y analiza dónde se acumula y cómo se transmite el conocimiento en la organización.
- **Uso en el Motor:** AG-B16, MC-B04: micro-evidencia para justificar curvas de aprendizaje en el arranque de nuevas plantas o líneas (AG-B05).
- **Limitaciones:** Una sola planta; la referencia a JPE procede del resultado de búsqueda, sin volumen comprobado.

#### MBM-0058 · Q 81 (A) — Getting Big Too Fast

- **Autores:** John D. Sterman; Rebecca Henderson; Eric D. Beinhocker; Lee I. Newman
- **Año:** 2007
- **Publicación o institución:** Management Science, 53(4), 683-696
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-05 Curvas de costes, de aprendizaje y de capacidad (principal) · secundarias: TMB-08
- **Calidad Q:** 81 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 7/10 · Impacto 8/10 · Independencia 10/10 · Acceso 2/10
- **DOI / ISBN / URL:** DOI: 10.1287/mnsc.1060.0673 · índice: https://en.wikipedia.org/wiki/Experience_curve_effect
- **Acceso y licencia:** Artículo de pago (INFORMS)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Experience curve effects Wikipedia Henderson Boston Consulting Group Wright's law learning curve bibliography»; WebFetch: sí, sobre la página índice)
- **Contenido:** Simula que la estrategia agresiva de ganar cuota para bajar por la curva de experiencia puede fracasar con retardos de capacidad y previsión imperfecta de la demanda.
- **Uso en el Motor:** AG-B16, MC-B04 y MC-B08: escenarios de sobrecapacidad cuando todos los competidores persiguen la curva de experiencia (AG-B05, AG-B14).
- **Limitaciones:** Modelo de simulación; confirmada solo por página índice.

#### MBM-0054 · Q 79 (B) — Learning from Experience and Learning from Others: An Exploration of Learning and Spillovers in Wartime Shipbuilding

- **Autores:** Rebecca Achee Thornton; Peter Thompson
- **Año:** 2001
- **Publicación o institución:** American Economic Review, 91(5), 1350-1368
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-05 Curvas de costes, de aprendizaje y de capacidad (principal) · secundarias: TMB-04
- **Calidad Q:** 79 (B) — Tipo 25/25 · Rigor 15/20 · Autoridad 13/15 · Vigencia 5/10 · Impacto 8/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** Verificada en página índice (referencias de Levitt, List y Syverson, NBER WP 18017): https://www.nber.org/papers/w18017.pdf
- **Acceso y licencia:** Artículo de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Levitt List Syverson "Toward an Understanding of Learning by Doing: Evidence from an Automobile Assembly Plant" Journal of Political Economy 2013»; WebFetch: sí, sobre la página índice)
- **Contenido:** Mide el aprendizaje propio y los efectos derrame entre astilleros.
- **Uso en el Motor:** AG-B16, MC-B04: valorar si la experiencia es apropiable por la empresa líder o se difunde al sector (ventaja de costes sostenible o no).
- **Limitaciones:** Confirmada solo por página índice.

#### MBM-0053 · Q 77 (B) — Learning by Doing

- **Autores:** Peter Thompson
- **Año:** 2010
- **Publicación o institución:** Handbook of Economics of Technical Change (según la cita índice; B. H. Hall y N. Rosenberg, eds.), North-Holland/Elsevier
- **Tipo de documento:** Capítulo de manual (revisión)
- **Temática:** TMB-05 Curvas de costes, de aprendizaje y de capacidad (principal) · secundarias: —
- **Calidad Q:** 77 (B) — Tipo 20/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 7/10 · Impacto 8/10 · Independencia 10/10 · Acceso 2/10
- **DOI / ISBN / URL:** Verificada en página índice (referencias de Levitt, List y Syverson, NBER WP 18017): https://www.nber.org/papers/w18017.pdf
- **Acceso y licencia:** Capítulo de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Levitt List Syverson "Toward an Understanding of Learning by Doing: Evidence from an Automobile Assembly Plant" Journal of Political Economy 2013»; WebFetch: sí, sobre la página índice)
- **Contenido:** Revisión de la literatura económica sobre aprendizaje por la práctica: medición, sesgos de estimación, olvido y efectos derrame.
- **Uso en el Motor:** AG-B16, MC-B04: revisión de métodos para estimar tasas de aprendizaje sectoriales.
- **Limitaciones:** Confirmada solo por página índice.

#### MBM-0055 · Q 76 (B) — Treating Progress Functions as a Managerial Opportunity

- **Autores:** John M. Dutton; Annie Thomas
- **Año:** 1984
- **Publicación o institución:** Academy of Management Review, 9(2), 235-247
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-05 Curvas de costes, de aprendizaje y de capacidad (principal) · secundarias: —
- **Calidad Q:** 76 (B) — Tipo 25/25 · Rigor 13/20 · Autoridad 12/15 · Vigencia 4/10 · Impacto 9/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** Verificada en página índice (referencias de Levitt, List y Syverson, NBER WP 18017): https://www.nber.org/papers/w18017.pdf
- **Acceso y licencia:** Artículo de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Levitt List Syverson "Toward an Understanding of Learning by Doing: Evidence from an Automobile Assembly Plant" Journal of Political Economy 2013»; WebFetch: sí, sobre la página índice)
- **Contenido:** Recopila tasas de progreso empíricas, muestra su gran dispersión entre empresas y sectores y los factores de gestión que las afectan.
- **Uso en el Motor:** AG-B16, MC-B04: distribución de referencia de tasas de progreso para priors cuando un sector carece de datos.
- **Limitaciones:** Confirmada solo por página índice.

#### MBM-0059 · Q 76 (B) — Diagnosing the Experience Curve

- **Autores:** George S. Day; David B. Montgomery
- **Año:** 1983
- **Publicación o institución:** Journal of Marketing, 47, 44 y ss.
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-05 Curvas de costes, de aprendizaje y de capacidad (principal) · secundarias: —
- **Calidad Q:** 76 (B) — Tipo 25/25 · Rigor 13/20 · Autoridad 13/15 · Vigencia 4/10 · Impacto 8/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** DOI: 10.2307/1251492 · índice: https://en.wikipedia.org/wiki/Experience_curve_effect
- **Acceso y licencia:** Artículo de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Experience curve effects Wikipedia Henderson Boston Consulting Group Wright's law learning curve bibliography»; WebFetch: sí, sobre la página índice)
- **Contenido:** Analiza cuándo la curva de experiencia es válida para la estrategia y sus problemas de medición (definición de producto, experiencia compartida).
- **Uso en el Motor:** AG-B16, MC-B04: lista de comprobación antes de aplicar curvas de experiencia a un sector.
- **Limitaciones:** Confirmada solo por página índice (solo página inicial).

#### MBM-0065 · Q 75 (B) — Fifty Years of Moore's Law

- **Autores:** Chris A. Mack
- **Año:** 2011
- **Publicación o institución:** IEEE Transactions on Semiconductor Manufacturing, 24(2), 202-207
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-05 Curvas de costes, de aprendizaje y de capacidad (principal) · secundarias: TMB-03
- **Calidad Q:** 75 (B) — Tipo 22/25 · Rigor 13/20 · Autoridad 13/15 · Vigencia 7/10 · Impacto 8/10 · Independencia 10/10 · Acceso 2/10
- **DOI / ISBN / URL:** DOI: 10.1109/TSM.2010.2096437 · índice: https://en.wikipedia.org/wiki/Learning_curve
- **Acceso y licencia:** Artículo de pago (IEEE)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Experience curve effects Wikipedia Henderson Boston Consulting Group Wright's law learning curve bibliography»; WebFetch: sí, sobre la página índice)
- **Contenido:** Repasa medio siglo de la ley de Moore, su base económica y técnica y sus límites.
- **Uso en el Motor:** AG-B16, MC-B04: tendencia de coste por transistor para el análisis del sector de semiconductores (AG-B06).
- **Limitaciones:** Confirmada solo por página índice.

#### MBM-0063 · Q 74 (B) — Technological Learning in the Energy Sector

- **Autores:** Martin Junginger; Wilfried van Sark; André Faaij (eds.)
- **Año:** 2010
- **Publicación o institución:** Edward Elgar
- **Tipo de documento:** Libro colectivo académico
- **Temática:** TMB-05 Curvas de costes, de aprendizaje y de capacidad (principal) · secundarias: TMB-03
- **Calidad Q:** 74 (B) — Tipo 20/25 · Rigor 15/20 · Autoridad 13/15 · Vigencia 8/10 · Impacto 6/10 · Independencia 10/10 · Acceso 2/10
- **DOI / ISBN / URL:** ISBN: 978-1-84844-834-6 · índice: https://en.wikipedia.org/wiki/Experience_curve_effect
- **Acceso y licencia:** Libro de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Experience curve effects Wikipedia Henderson Boston Consulting Group Wright's law learning curve bibliography»; WebFetch: sí, sobre la página índice)
- **Contenido:** Compila curvas de experiencia de tecnologías energéticas (solar, eólica, biomasa, eficiencia) y discute su uso en modelos y políticas.
- **Uso en el Motor:** AG-B16, MC-B04: tasas de aprendizaje por tecnología energética para escenarios de coste (AG-B11).
- **Limitaciones:** Confirmada solo por página índice (título principal e ISBN).

#### MBM-0066 · Q 73 (B) — Learning Curve Models and Applications

- **Autores:** Michel Jose Anzanello; Flavio Sanson Fogliatto
- **Año:** 2011
- **Publicación o institución:** International Journal of Industrial Ergonomics, 41(5), 573-583
- **Tipo de documento:** Artículo de revisión revisado por pares
- **Temática:** TMB-05 Curvas de costes, de aprendizaje y de capacidad (principal) · secundarias: —
- **Calidad Q:** 73 (B) — Tipo 22/25 · Rigor 13/20 · Autoridad 12/15 · Vigencia 8/10 · Impacto 6/10 · Independencia 10/10 · Acceso 2/10
- **DOI / ISBN / URL:** DOI: 10.1016/j.ergon.2011.05.001 · índice: https://en.wikipedia.org/wiki/Learning_curve
- **Acceso y licencia:** Artículo de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Experience curve effects Wikipedia Henderson Boston Consulting Group Wright's law learning curve bibliography»; WebFetch: sí, sobre la página índice)
- **Contenido:** Revisión de modelos de curvas de aprendizaje (log-lineal, exponencial, hiperbólico) y de sus aplicaciones.
- **Uso en el Motor:** AG-B16, MC-B04: catálogo de formas funcionales alternativas a Wright.
- **Limitaciones:** Confirmada solo por página índice.

#### MBM-0068 · Q 73 (B) — Industrial Production and Capacity Utilization: Recent Developments and the 1999 Revision

- **Autores:** Charles Gilbert; Norman Morin; Richard Raddock
- **Año:** 2000
- **Publicación o institución:** Federal Reserve Bulletin, 86 (marzo de 2000), 194-197 (según la cita de la página metodológica)
- **Tipo de documento:** Artículo de publicación oficial de banco central
- **Temática:** TMB-05 Curvas de costes, de aprendizaje y de capacidad (principal) · secundarias: TMB-14
- **Calidad Q:** 73 (B) — Tipo 18/25 · Rigor 13/20 · Autoridad 15/15 · Vigencia 5/10 · Impacto 6/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** Verificada en página índice: https://www.federalreserve.gov/RELEASES/G17/Meth/MethCap.htm
- **Acceso y licencia:** Publicación oficial
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Federal Reserve G.17 industrial production and capacity utilization explanatory notes methodology capacity estimates»; WebFetch: sí, sobre la página índice)
- **Contenido:** Describe la revisión de 1999 de los índices de producción y capacidad y los cambios metodológicos asociados.
- **Uso en el Motor:** AG-B16, MC-B04: contexto metodológico de las series históricas de capacidad.
- **Limitaciones:** Confirmada solo por cita; páginas tal como aparecen en la página índice.

#### MBM-0056 · Q 73 (B) — The Learning Curve: Historical Review and Comprehensive Survey

- **Autores:** Louis E. Yelle
- **Año:** 1979
- **Publicación o institución:** Decision Sciences, 10(2), 302-328
- **Tipo de documento:** Artículo de revisión revisado por pares
- **Temática:** TMB-05 Curvas de costes, de aprendizaje y de capacidad (principal) · secundarias: —
- **Calidad Q:** 73 (B) — Tipo 22/25 · Rigor 13/20 · Autoridad 13/15 · Vigencia 3/10 · Impacto 9/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** DOI: 10.1111/j.1540-5915.1979.tb00026.x · índice: https://en.wikipedia.org/wiki/Learning_curve
- **Acceso y licencia:** Artículo de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Experience curve effects Wikipedia Henderson Boston Consulting Group Wright's law learning curve bibliography»; WebFetch: sí, sobre la página índice)
- **Contenido:** Revisión histórica de las formas funcionales de la curva de aprendizaje (log-lineal, plateau, Stanford-B, etc.).
- **Uso en el Motor:** AG-B16, MC-B04: elección de la forma funcional de la curva de costes.
- **Limitaciones:** Antigua; confirmada solo por página índice.

#### MBM-0057 · Q 71 (B) — Competitive Cost Dynamics: The Experience Curve

- **Autores:** Arnoldo C. Hax; Nicolas S. Majluf
- **Año:** 1982
- **Publicación o institución:** Interfaces, 12(5), 50-61
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-05 Curvas de costes, de aprendizaje y de capacidad (principal) · secundarias: TMB-04
- **Calidad Q:** 71 (B) — Tipo 22/25 · Rigor 12/20 · Autoridad 12/15 · Vigencia 4/10 · Impacto 8/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** DOI: 10.1287/inte.12.5.50 · índice: https://en.wikipedia.org/wiki/Experience_curve_effect
- **Acceso y licencia:** Artículo de pago (INFORMS)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Experience curve effects Wikipedia Henderson Boston Consulting Group Wright's law learning curve bibliography»; WebFetch: sí, sobre la página índice)
- **Contenido:** Explica el uso estratégico de la curva de experiencia: posición de costes relativa, precios y dinámica competitiva.
- **Uso en el Motor:** AG-B16, MC-B04: estimar ventaja de costes relativa entre competidores según su producción acumulada (AG-B03).
- **Limitaciones:** Confirmada solo por página índice.

#### MBM-0064 · Q 70 (B) — Costs, Learning Curves, and Scale Economies

- **Autores:** Ernst R. Berndt
- **Año:** 1991
- **Publicación o institución:** Capítulo de «The Practice of Econometrics», Addison-Wesley
- **Tipo de documento:** Capítulo de manual
- **Temática:** TMB-05 Curvas de costes, de aprendizaje y de capacidad (principal) · secundarias: TMB-02
- **Calidad Q:** 70 (B) — Tipo 20/25 · Rigor 14/20 · Autoridad 13/15 · Vigencia 4/10 · Impacto 7/10 · Independencia 10/10 · Acceso 2/10
- **DOI / ISBN / URL:** ISBN: 0-201-17628-9 · índice: https://en.wikipedia.org/wiki/Experience_curve_effect
- **Acceso y licencia:** Libro de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Experience curve effects Wikipedia Henderson Boston Consulting Group Wright's law learning curve bibliography»; WebFetch: sí, sobre la página índice)
- **Contenido:** Capítulo de manual que estima curvas de aprendizaje y economías de escala con datos reales, separando ambos efectos por regresión.
- **Uso en el Motor:** AG-B16, MC-B04: separar aprendizaje (producción acumulada) de escala (producción corriente) al estimar curvas de costes sectoriales.
- **Limitaciones:** Confirmada solo por página índice.

#### MBM-0060 · Q 64 (C) — Limits of the Learning Curve

- **Autores:** William J. Abernathy; Kenneth Wayne
- **Año:** 1974
- **Publicación o institución:** Harvard Business Review, 52(5), 109-119
- **Tipo de documento:** Artículo de revista profesional
- **Temática:** TMB-05 Curvas de costes, de aprendizaje y de capacidad (principal) · secundarias: TMB-06
- **Calidad Q:** 64 (C) — Tipo 15/25 · Rigor 11/20 · Autoridad 13/15 · Vigencia 3/10 · Impacto 9/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** Verificada en página índice: https://en.wikipedia.org/wiki/Learning_curve
- **Acceso y licencia:** Artículo de pago (HBR)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Experience curve effects Wikipedia Henderson Boston Consulting Group Wright's law learning curve bibliography»; WebFetch: sí, sobre la página índice)
- **Contenido:** Caso del Ford T: la búsqueda obsesiva de la curva de experiencia reduce la flexibilidad y la capacidad de innovar.
- **Uso en el Motor:** AG-B16, MC-B04: contrapeso cualitativo a la extrapolación de costes (AG-B14 Contrarias).
- **Limitaciones:** Revista profesional, sin revisión por pares.

#### MBM-0048 · Q 64 (C) — The Experience Curve, Reviewed (Part II): History

- **Autores:** Bruce D. Henderson
- **Año:** 1973
- **Publicación o institución:** Boston Consulting Group (serie Perspectives)
- **Tipo de documento:** Ensayo de consultora
- **Temática:** TMB-05 Curvas de costes, de aprendizaje y de capacidad (principal) · secundarias: TMB-04
- **Calidad Q:** 64 (C) — Tipo 12/25 · Rigor 10/20 · Autoridad 13/15 · Vigencia 3/10 · Impacto 10/10 · Independencia 6/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://www.bcg.com/ru-ru/publications/1973/corporate-finance-strategy-portfolio-management-experience-curve-reviewed-part-ii-the-history · índice: https://en.wikipedia.org/wiki/Experience_curve_effect
- **Acceso y licencia:** Acceso abierto (web de BCG)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Experience curve effects Wikipedia Henderson Boston Consulting Group Wright's law learning curve bibliography»; WebFetch: sí)
- **Contenido:** Presenta la curva de experiencia de BCG (el coste unitario cae un porcentaje constante cada vez que se duplica la producción acumulada) y la distingue de la curva de aprendizaje de mano de obra.
- **Uso en el Motor:** AG-B16, MC-B04: marco estratégico que liga cuota, producción acumulada y ventaja de costes, para AG-B03 Estructura y Competencia y AG-B05.
- **Limitaciones:** Texto divulgativo de consultora, sin evidencia econométrica.

#### MBM-0061 · Q 60 (C) — Building Strategy on the Experience Curve

- **Autores:** Pankaj Ghemawat
- **Año:** 1985
- **Publicación o institución:** Harvard Business Review
- **Tipo de documento:** Artículo de revista profesional
- **Temática:** TMB-05 Curvas de costes, de aprendizaje y de capacidad (principal) · secundarias: TMB-04
- **Calidad Q:** 60 (C) — Tipo 15/25 · Rigor 10/20 · Autoridad 12/15 · Vigencia 3/10 · Impacto 7/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** Verificada en página índice (lectura adicional): https://en.wikipedia.org/wiki/Experience_curve_effect
- **Acceso y licencia:** Artículo de pago (HBR)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Experience curve effects Wikipedia Henderson Boston Consulting Group Wright's law learning curve bibliography»; WebFetch: sí, sobre la página índice)
- **Contenido:** Cuándo la curva de experiencia justifica estrategias de liderazgo en costes y cuándo no (difusión de la experiencia, cambio tecnológico).
- **Uso en el Motor:** AG-B16, MC-B04: evaluar si la ventaja de costes del líder sectorial es defendible.
- **Limitaciones:** Revista profesional; datos bibliográficos parciales en la página índice.

#### MBM-0062 · Q 59 (C) — Profit from the Learning Curve

- **Autores:** Winfred B. Hirschmann
- **Año:** 1964
- **Publicación o institución:** Harvard Business Review (enero de 1964), ISSN 0017-8012
- **Tipo de documento:** Artículo de revista profesional
- **Temática:** TMB-05 Curvas de costes, de aprendizaje y de capacidad (principal) · secundarias: —
- **Calidad Q:** 59 (C) — Tipo 15/25 · Rigor 9/20 · Autoridad 11/15 · Vigencia 3/10 · Impacto 8/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** Verificada en página índice: https://en.wikipedia.org/wiki/Experience_curve_effect
- **Acceso y licencia:** Artículo de pago (HBR)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Experience curve effects Wikipedia Henderson Boston Consulting Group Wright's law learning curve bibliography»; WebFetch: sí, sobre la página índice)
- **Contenido:** Extiende la curva de aprendizaje de la aeronáutica a la industria de proceso (refino) y la propone como herramienta de gestión.
- **Uso en el Motor:** AG-B16, MC-B04: aplicación de curvas de aprendizaje a industrias de proceso (química, refino).
- **Limitaciones:** Antigua; revista profesional.

## TMB-06 Valoración: DCF, múltiplos, ROIC y coste de capital sectorial

#### DOC-MOT-0052 · Q 95 (A) — The Dividend-Price Ratio and Expectations of Future Dividends and Discount Factors

- **Autores:** John Y. Campbell; Robert J. Shiller
- **Año:** 1988
- **Publicación o institución:** The Review of Financial Studies, vol. 1, n.º 3, págs. 195-228 (circuló antes como NBER Working Paper 2100, diciembre de 1986)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-06 Valoración: DCF, múltiplos, ROIC y coste de capital sectorial (principal) · secundarias: TMB-01
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI del documento de trabajo: 10.3386/w2100 (el DOI de la versión de revista no se ha visto; se retira el «10.1093/rfs/1.3.195 a verificar») · https://www.nber.org/papers/w2100
- **Acceso y licencia:** Documento de trabajo NBER con PDF de libre descarga; versión de revista por suscripción (Oxford University Press)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Campbell Shiller 1988 "The Dividend-Price Ratio and Expectations of Future Dividends and Discount Factors" Review of Financial Studies»; WebFetch: sí)
- **Contenido:** Introduce la aproximación log-lineal del ratio dividendo-precio («identidad de Campbell-Shiller») que lo descompone en expectativas de crecimiento de dividendos y de tasas de descuento futuras, y la contrasta con un VAR.
- **Uso en el Motor:** AG-B16, MC-B06: descomposición del ratio dividendo-precio en crecimiento esperado y tasa de descuento, base de las expectativas implícitas en el precio de un sector.
- **Limitaciones:** Predictibilidad débil fuera de muestra (véase Goyal y Welch); el NBER WP es una versión previa que puede diferir del texto publicado.
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (metadatos de la versión publicada tomados de la página NBER).

#### DOC-MOT-0340 · Q 94 (A) — The Capital Asset Pricing Model: Theory and Evidence

- **Autores:** Eugene F. Fama; Kenneth R. French
- **Año:** 2004
- **Publicación o institución:** Journal of Economic Perspectives, vol. 18, n.º 3, págs. 25-46
- **Tipo de documento:** Artículo de revisión revisado por pares
- **Temática:** TMB-06 Valoración: DCF, múltiplos, ROIC y coste de capital sectorial (principal) · secundarias: TMB-07
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 9/10 · Acceso 10/10
- **DOI / ISBN / URL:** DOI: 10.1257/0895330042162430 · https://www.aeaweb.org/articles?id=10.1257/0895330042162430
- **Acceso y licencia:** Acceso gratuito (AEA)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Fama–French three-factor model capital asset pricing model Black–Litterman arbitrage pricing theory (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Capital asset pricing model», que reproduce la cita completa)
- **Contenido:** Revisión de la teoría y de la evidencia empírica del CAPM, concluyendo que sus fallos invalidan su uso aplicado.
- **Uso en el Motor:** AG-B16, MC-B06: límites empíricos del CAPM al estimar costes de capital sectoriales (control de AG-B14 Contrarias).
- **Limitaciones:** Revisión de autores con postura conocida.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0071 · Q 93 (A) — Capital Asset Prices: A Theory of Market Equilibrium under Conditions of Risk

- **Autores:** William F. Sharpe
- **Año:** 1964
- **Publicación o institución:** The Journal of Finance, vol. 19, n.º 3, págs. 425-442
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-06 Valoración: DCF, múltiplos, ROIC y coste de capital sectorial (principal) · secundarias: TMB-07
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1111/j.1540-6261.1964.tb02865.x · https://doi.org/10.1111%2Fj.1540-6261.1964.tb02865.x
- **Acceso y licencia:** Texto completo por suscripción en la editorial (Wiley)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Fama–French three-factor model capital asset pricing model Black–Litterman arbitrage pricing theory (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Capital asset pricing model», que reproduce la cita completa)
- **Contenido:** Formula el CAPM: en equilibrio la rentabilidad esperada es lineal en la beta respecto a la cartera de mercado.
- **Uso en el Motor:** AG-B16, MC-B06: CAPM como base del coste del capital propio sectorial (beta sectorial).
- **Limitaciones:** Evidencia empírica débil (Fama-French 1992, 2004).
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (tanda 2).

#### MBM-0096 · Q 92 (A) — Equity Valuation Using Multiples

- **Autores:** Jing Liu; Doron Nissim; Jacob Thomas
- **Año:** 2002
- **Publicación o institución:** Journal of Accounting Research, 40(1), 135-172
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-06 Valoración: DCF, múltiplos, ROIC y coste de capital sectorial (principal) · secundarias: TMB-07
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 14/15 · Vigencia 7/10 · Impacto 10/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI: 10.1111/1475-679X.00042 · https://ideas.repec.org/a/bla/joares/v40y2002i1p135-172.html · https://business.columbia.edu/sites/default/files-efs/pubfiles/318/Equity_Valuation_Using_Multiples.pdf
- **Acceso y licencia:** Artículo de pago; copia del autor en abierto
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Liu Nissim Thomas 2002 "Equity Valuation Using Multiples" Journal of Accounting Research»; WebFetch: sí)
- **Contenido:** Compara la precisión de múltiplos: los basados en beneficios previstos son los mejores, seguidos de beneficios históricos, flujos de caja y valor contable; las ventas, los peores; la ordenación se mantiene en casi todos los sectores.
- **Uso en el Motor:** AG-B16, MC-B06: elegir el múltiplo y el grupo de comparables al valorar candidatos por valoración relativa (AG-B09, AG-B12).
- **Limitaciones:** Muestra con previsiones de analistas y valores positivos; EE. UU.

#### DOC-MOT-0315 · Q 92 (A) — The Equity Premium: A Puzzle

- **Autores:** Rajnish Mehra; Edward C. Prescott
- **Año:** 1985
- **Publicación o institución:** Journal of Monetary Economics, vol. 15, n.º 2, págs. 145-161
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-06 Valoración: DCF, múltiplos, ROIC y coste de capital sectorial (principal) · secundarias: —
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1016/0304-3932(85)90061-3 · PDF: http://minneapolisfed.org/research/sr/sr81.pdf
- **Acceso y licencia:** Versión Fed de Minneapolis gratuita; revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «dividend discount model equity premium puzzle residual income valuation Gordon growth (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Equity premium puzzle»)
- **Contenido:** Muestra que la prima de riesgo histórica de la renta variable es demasiado alta para modelos de consumo con aversión al riesgo razonable.
- **Uso en el Motor:** AG-B16, MC-B06: contexto de la magnitud de la prima de riesgo usada en el coste de capital.
- **Limitaciones:** Calibración a EE. UU. 1889-1978.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0337 · Q 92 (A) — The Valuation of Risk Assets and the Selection of Risky Investments in Stock Portfolios and Capital Budgets

- **Autores:** John Lintner
- **Año:** 1965
- **Publicación o institución:** Review of Economics and Statistics, vol. 47, n.º 1, págs. 13-37
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-06 Valoración: DCF, múltiplos, ROIC y coste de capital sectorial (principal) · secundarias: TMB-07
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.2307/1924119 · JSTOR: https://www.jstor.org/stable/1924119
- **Acceso y licencia:** Texto completo por suscripción en la editorial (MIT Press/JSTOR)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Fama–French three-factor model capital asset pricing model Black–Litterman arbitrage pricing theory (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Capital asset pricing model», que reproduce la cita completa y «Modern portfolio theory»)
- **Contenido:** Derivación independiente del CAPM con préstamo y endeudamiento libre de riesgo y aplicación a la presupuestación de capital.
- **Uso en el Motor:** AG-B16, MC-B06: derivación alternativa del CAPM (Lintner) y relación con la selección de inversiones de capital.
- **Limitaciones:** Supuestos de equilibrio estático.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0316 · Q 90 (A) — The Worldwide Equity Premium: A Smaller Puzzle

- **Autores:** Elroy Dimson; Paul Marsh; Mike Staunton
- **Año:** 2008
- **Publicación o institución:** En R. Mehra (ed.), Handbook of the Equity Risk Premium, Elsevier (versión SSRN 891620)
- **Tipo de documento:** Capítulo de manual académico
- **Temática:** TMB-06 Valoración: DCF, múltiplos, ROIC y coste de capital sectorial (principal) · secundarias: —
- **Calidad Q:** 90 (A) — Tipo 20/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** ISBN: 978-0-08-055585-0 · SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=891620
- **Acceso y licencia:** Versión SSRN gratuita
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «dividend discount model equity premium puzzle residual income valuation Gordon growth (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Equity premium puzzle»)
- **Contenido:** Primas de riesgo históricas de 17 países desde 1900; la prima mundial es menor que la de EE. UU. por sesgo de supervivencia.
- **Uso en el Motor:** AG-B16, MC-B06: primas de riesgo históricas internacionales por país para calibrar el coste del capital propio por mercado.
- **Limitaciones:** Datos hasta 2005 en la versión citada.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0314 · Q 88 (A) — Dividends, Earnings, and Stock Prices

- **Autores:** Myron J. Gordon
- **Año:** 1959
- **Publicación o institución:** Review of Economics and Statistics, vol. 41, n.º 2, págs. 99-105
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-06 Valoración: DCF, múltiplos, ROIC y coste de capital sectorial (principal) · secundarias: —
- **Calidad Q:** 88 (A) — Tipo 25/25 · Rigor 14/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.2307/1927792 · JSTOR: https://www.jstor.org/stable/1927792
- **Acceso y licencia:** Texto completo por suscripción en la editorial (MIT Press/JSTOR)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «dividend discount model equity premium puzzle residual income valuation Gordon growth (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Dividend discount model», que reproduce la cita completa)
- **Contenido:** Fundamenta el modelo de descuento de dividendos con crecimiento constante (modelo de Gordon) y lo contrasta empíricamente.
- **Uso en el Motor:** AG-B16, MC-B06: modelo de crecimiento de Gordon (valor = flujo / (k − g)) para valor terminal y DCF inverso (crecimiento implícito en el precio).
- **Limitaciones:** Muy sensible a g y r; supone crecimiento perpetuo.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### MBM-0095 · Q 85 (A) — Valuation: Measuring and Managing the Value of Companies (7.ª ed.)

- **Autores:** Tim Koller; Marc Goedhart; David Wessels (McKinsey & Company)
- **Año:** 2020
- **Publicación o institución:** John Wiley & Sons (Nueva Jersey)
- **Tipo de documento:** Manual de referencia
- **Temática:** TMB-06 Valoración: DCF, múltiplos, ROIC y coste de capital sectorial (principal) · secundarias: TMB-07
- **Calidad Q:** 85 (A) — Tipo 22/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 9/10 · Acceso 4/10
- **DOI / ISBN / URL:** ISBN: 9781119610885 · https://pure.eur.nl/en/publications/valuation-measuring-and-managing-the-value-of-companies-7th-editi/
- **Acceso y licencia:** Libro de pago
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Koller Goedhart Wessels "Valuation: Measuring and Managing the Value of Companies" McKinsey 7th edition Wiley 2020 ISBN»; WebFetch: sí (registro de Erasmus University))
- **Contenido:** Manual profesional de valoración: ROIC, crecimiento y flujo de caja libre como impulsores del valor, DCF empresarial, coste de capital, múltiplos y análisis de rendimiento histórico por sector.
- **Uso en el Motor:** AG-B16, MC-B06: árbol de valor ROIC−WACC, DCF de candidatos y DCF inverso (crecimiento y ROIC implícitos en el precio) para AG-B09 y AG-B12.
- **Limitaciones:** Autores vinculados a McKinsey; hay 8.ª edición más reciente.

#### MBM-0097 · Q 85 (A) — Industry Costs of Equity

- **Autores:** Eugene F. Fama; Kenneth R. French
- **Año:** 1997
- **Publicación o institución:** Journal of Financial Economics, 43(2), 153-193
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-06 Valoración: DCF, múltiplos, ROIC y coste de capital sectorial (principal) · secundarias: TMB-07
- **Calidad Q:** 85 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 5/10 · Impacto 10/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** https://ideas.repec.org/a/eee/jfinec/v43y1997i2p153-193.html
- **Acceso y licencia:** Artículo de pago (Elsevier); ficha abierta en IDEAS
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Fama French 1997 "Industry costs of equity" Journal of Financial Economics 43»; WebFetch: sí)
- **Contenido:** Estima el coste del capital propio de sectores con el CAPM y el modelo de tres factores y muestra que las estimaciones son muy imprecisas por la incertidumbre de las primas y la variación temporal de las cargas.
- **Uso en el Motor:** AG-B16, MC-B06: coste del capital propio sectorial con intervalos de error y cautela sobre su precisión (AG-B09).
- **Limitaciones:** Datos hasta mediados de los noventa.

#### DOC-MOT-0054 · Q 84 (A) — Investment Valuation: Tools and Techniques for Determining the Value of Any Asset (3.ª ed.)

- **Autores:** Aswath Damodaran
- **Año:** 2012
- **Publicación o institución:** John Wiley & Sons (Wiley Finance)
- **Tipo de documento:** Manual de referencia
- **Temática:** TMB-06 Valoración: DCF, múltiplos, ROIC y coste de capital sectorial (principal) · secundarias: TMB-07
- **Calidad Q:** 84 (A) — Tipo 20/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 9/10 · Acceso 5/10
- **DOI / ISBN / URL:** ISBN: 978-1-118-01152-2 (tapa dura) · https://www.oreilly.com/library/view/investment-valuation-tools/9781118011522/03_copyright.html
- **Acceso y licencia:** De pago (Wiley); material complementario gratuito en la web del autor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Damodaran "Investment Valuation" third edition Wiley 2012 ISBN»; WebFetch: no)
- **Contenido:** Manual integral de valoración: descuento de flujos (FCFF/FCFE), coste de capital, múltiplos, valoración relativa y de activos difíciles (empresas jóvenes, en pérdidas, financieras).
- **Uso en el Motor:** AG-B16, MC-B06: manual de DCF (FCFF/FCFE), coste de capital, múltiplos y valoración relativa de candidatos y sectores (AG-B09 Finanzas y Valoración, AG-B12).
- **Limitaciones:** Manual profesional; casos y datos de 2010-2011.
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (ISBN visto en catálogos y en la página de copyright de O'Reilly).

#### MBM-0102 · Q 84 (A) — Toward an Implied Cost of Capital

- **Autores:** William R. Gebhardt; Charles M. C. Lee; Bhaskaran Swaminathan
- **Año:** 2001
- **Publicación o institución:** Journal of Accounting Research, 39, 135-176
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-06 Valoración: DCF, múltiplos, ROIC y coste de capital sectorial (principal) · secundarias: TMB-07
- **Calidad Q:** 84 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 6/10 · Impacto 9/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de Liu, Nissim y Thomas 2002, copia del autor en Columbia): https://business.columbia.edu/sites/default/files-efs/pubfiles/318/Equity_Valuation_Using_Multiples.pdf
- **Acceso y licencia:** Artículo de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Liu Nissim Thomas 2002 "Equity Valuation Using Multiples" Journal of Accounting Research»; WebFetch: sí, sobre la página índice)
- **Contenido:** Calcula el coste de capital implícito que iguala el precio con un modelo de beneficio residual y muestra que depende sistemáticamente del sector y de características de la empresa.
- **Uso en el Motor:** AG-B16, MC-B06: coste de capital implícito sectorial como alternativa al CAPM y para el DCF inverso.
- **Limitaciones:** Depende de previsiones de analistas; confirmada solo por página índice.

#### MBM-0098 · Q 83 (A) — Earnings, Book Values, and Dividends in Equity Valuation

- **Autores:** James A. Ohlson
- **Año:** 1995
- **Publicación o institución:** Contemporary Accounting Research (primavera de 1995), 661-687
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-06 Valoración: DCF, múltiplos, ROIC y coste de capital sectorial (principal) · secundarias: —
- **Calidad Q:** 83 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 6/10 · Impacto 9/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de Liu, Nissim y Thomas 2002, copia del autor en Columbia): https://business.columbia.edu/sites/default/files-efs/pubfiles/318/Equity_Valuation_Using_Multiples.pdf
- **Acceso y licencia:** Artículo de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Liu Nissim Thomas 2002 "Equity Valuation Using Multiples" Journal of Accounting Research»; WebFetch: sí, sobre la página índice)
- **Contenido:** Modelo de valoración por beneficio residual: el valor es el valor contable más el valor actual de los beneficios anormales, bajo contabilidad de excedente limpio.
- **Uso en el Motor:** AG-B16, MC-B06: valoración por beneficio residual (útil para bancos y aseguradoras, donde el DCF de flujos es poco práctico).
- **Limitaciones:** Confirmada solo por página índice.

#### MBM-0100 · Q 83 (A) — The Valuation of Cash Flow Forecasts: An Empirical Analysis

- **Autores:** Steven N. Kaplan; Richard S. Ruback
- **Año:** 1995
- **Publicación o institución:** The Journal of Finance, 50, 1059-1093
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-06 Valoración: DCF, múltiplos, ROIC y coste de capital sectorial (principal) · secundarias: —
- **Calidad Q:** 83 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 5/10 · Impacto 9/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de Liu, Nissim y Thomas 2002, copia del autor en Columbia): https://business.columbia.edu/sites/default/files-efs/pubfiles/318/Equity_Valuation_Using_Multiples.pdf
- **Acceso y licencia:** Artículo de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Liu Nissim Thomas 2002 "Equity Valuation Using Multiples" Journal of Accounting Research»; WebFetch: sí, sobre la página índice)
- **Contenido:** Con operaciones apalancadas, muestra que el DCF de previsiones de flujo de caja aproxima bien el valor de transacción, comparable o mejor que los múltiplos.
- **Uso en el Motor:** AG-B16, MC-B06: evidencia de precisión del DCF frente a múltiplos para combinar ambos métodos.
- **Limitaciones:** Confirmada solo por página índice.

#### DOC-MOT-0053 · Q 82 (A) — Equity Risk Premiums (ERP): Determinants, Estimation, and Implications — The 2026 Edition

- **Autores:** Aswath Damodaran
- **Año:** 2026 (actualización anual; serie iniciada en 2008)
- **Publicación o institución:** NYU Stern School of Business (Damodaran Online y SSRN)
- **Tipo de documento:** Documento de trabajo (actualización anual)
- **Temática:** TMB-06 Valoración: DCF, múltiplos, ROIC y coste de capital sectorial (principal) · secundarias: —
- **Calidad Q:** 82 (A) — Tipo 15/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 8/10 · Acceso 10/10
- **DOI / ISBN / URL:** Sin DOI visto · Anuncio de la edición 2026: https://www.bvresources.com/articles/bvwire/damodaran-unveils-his-annual-erp-update · Ediciones anteriores en el servidor del autor (p. ej., https://pages.stern.nyu.edu/~adamodar/pdfiles/papers/ERP2022Formatted.pdf)
- **Acceso y licencia:** Acceso gratuito (página del autor y SSRN)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Damodaran "Equity Risk Premiums (ERP): Determinants, Estimation, and Implications" 2025 Edition SSRN» y «… "The 2025 Edition" ssrn»; WebFetch: sí, del anuncio de BVResources, que identifica la edición 2026)
- **Contenido:** Revisión anual de los métodos de estimación de la prima de riesgo de la renta variable (histórica, de encuesta e implícita por descuento de flujos), con la prima implícita del S&P 500 y primas por país.
- **Uso en el Motor:** AG-B16, MC-B06: prima de riesgo de la renta variable (implícita e histórica) y primas país para el coste de capital sectorial por mercado geográfico (AG-B09).
- **Limitaciones:** Supuestos de crecimiento terminal; un solo autor sin revisión por pares. Alerta: REPARAR enlace (sustituir por la URL SSRN o del PDF de la edición 2026 en el próximo barrido). Corrección: la semilla indicaba 2025; la edición vigente es la de 2026.
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02.

#### MBM-0099 · Q 81 (A) — Valuation and Clean Surplus Accounting for Operating and Financial Activities

- **Autores:** Gerald A. Feltham; James A. Ohlson
- **Año:** 1995
- **Publicación o institución:** Contemporary Accounting Research (primavera de 1995), 689-731
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-06 Valoración: DCF, múltiplos, ROIC y coste de capital sectorial (principal) · secundarias: —
- **Calidad Q:** 81 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 13/15 · Vigencia 6/10 · Impacto 8/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de Liu, Nissim y Thomas 2002, copia del autor en Columbia): https://business.columbia.edu/sites/default/files-efs/pubfiles/318/Equity_Valuation_Using_Multiples.pdf
- **Acceso y licencia:** Artículo de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Liu Nissim Thomas 2002 "Equity Valuation Using Multiples" Journal of Accounting Research»; WebFetch: sí, sobre la página índice)
- **Contenido:** Separa actividades operativas y financieras en el modelo de beneficio residual y relaciona valor con activos operativos netos.
- **Uso en el Motor:** AG-B16, MC-B06: valoración por beneficio residual operativo coherente con ROIC.
- **Limitaciones:** Confirmada solo por página índice.

#### MBM-0103 · Q 80 (A) — Accounting Valuation, Market Expectation, and Cross-Sectional Stock Returns

- **Autores:** Richard Frankel; Charles M. C. Lee
- **Año:** 1998
- **Publicación o institución:** Journal of Accounting and Economics, 25, 283-319
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-06 Valoración: DCF, múltiplos, ROIC y coste de capital sectorial (principal) · secundarias: TMB-07
- **Calidad Q:** 80 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 13/15 · Vigencia 5/10 · Impacto 8/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de Liu, Nissim y Thomas 2002, copia del autor en Columbia): https://business.columbia.edu/sites/default/files-efs/pubfiles/318/Equity_Valuation_Using_Multiples.pdf
- **Acceso y licencia:** Artículo de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Liu Nissim Thomas 2002 "Equity Valuation Using Multiples" Journal of Accounting Research»; WebFetch: sí, sobre la página índice)
- **Contenido:** Estima el valor fundamental por beneficio residual con previsiones de analistas; el ratio valor/precio predice rentabilidades.
- **Uso en el Motor:** AG-B16, MC-B06 y MC-B07: ratio valor intrínseco/precio como variable de cribado de candidatos.
- **Limitaciones:** Confirmada solo por página índice.

#### MBM-0108 · Q 80 (A) — On Estimating the Expected Return on the Market: An Exploratory Investigation

- **Autores:** Robert C. Merton
- **Año:** 1980
- **Publicación o institución:** Journal of Financial Economics, 8(4), 323-361
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-06 Valoración: DCF, múltiplos, ROIC y coste de capital sectorial (principal) · secundarias: —
- **Calidad Q:** 80 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 4/10 · Impacto 9/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** Verificada en página índice (referencias de Fama y French 1997 en IDEAS): https://ideas.repec.org/a/eee/jfinec/v43y1997i2p153-193.html
- **Acceso y licencia:** Artículo de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Fama French 1997 "Industry costs of equity" Journal of Financial Economics 43»; WebFetch: sí, sobre la página índice)
- **Contenido:** Muestra que la rentabilidad esperada del mercado se estima con mucha imprecisión con datos históricos y propone usar la varianza.
- **Uso en el Motor:** AG-B16, MC-B06: cautela sobre la imprecisión de la prima de riesgo usada en el WACC sectorial.
- **Limitaciones:** Confirmada solo por página índice.

#### MBM-0105 · Q 79 (B) — Valuing IPOs

- **Autores:** Moonchul Kim; Jay R. Ritter
- **Año:** 1999
- **Publicación o institución:** Journal of Financial Economics, 53, 409-437
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-06 Valoración: DCF, múltiplos, ROIC y coste de capital sectorial (principal) · secundarias: —
- **Calidad Q:** 79 (B) — Tipo 25/25 · Rigor 15/20 · Autoridad 13/15 · Vigencia 5/10 · Impacto 8/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de Liu, Nissim y Thomas 2002, copia del autor en Columbia): https://business.columbia.edu/sites/default/files-efs/pubfiles/318/Equity_Valuation_Using_Multiples.pdf
- **Acceso y licencia:** Artículo de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Liu Nissim Thomas 2002 "Equity Valuation Using Multiples" Journal of Accounting Research»; WebFetch: sí, sobre la página índice)
- **Contenido:** Evalúa la valoración por múltiplos de comparables en salidas a bolsa y su escasa precisión salvo con beneficios previstos.
- **Uso en el Motor:** AG-B16, MC-B06: valoración de candidatos recién cotizados o sin historial.
- **Limitaciones:** Confirmada solo por página índice.

#### MBM-0101 · Q 79 (B) — The Effect of the Set of Comparable Firms on the Accuracy of the Price-Earnings Valuation Method

- **Autores:** Andrew W. Alford
- **Año:** 1992
- **Publicación o institución:** Journal of Accounting Research, 30, 94-108
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-06 Valoración: DCF, múltiplos, ROIC y coste de capital sectorial (principal) · secundarias: TMB-07
- **Calidad Q:** 79 (B) — Tipo 25/25 · Rigor 15/20 · Autoridad 13/15 · Vigencia 5/10 · Impacto 8/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de Liu, Nissim y Thomas 2002, copia del autor en Columbia): https://business.columbia.edu/sites/default/files-efs/pubfiles/318/Equity_Valuation_Using_Multiples.pdf
- **Acceso y licencia:** Artículo de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Liu Nissim Thomas 2002 "Equity Valuation Using Multiples" Journal of Accounting Research»; WebFetch: sí, sobre la página índice)
- **Contenido:** Compara criterios de selección de comparables (sector, riesgo, crecimiento) para el PER y halla que el sector a tres dígitos funciona bien.
- **Uso en el Motor:** AG-B16, MC-B06: criterio de selección del grupo de comparables por clasificación sectorial.
- **Limitaciones:** Confirmada solo por página índice.

#### MBM-0104 · Q 77 (B) — Financial Statement Analysis and Security Valuation

- **Autores:** Stephen H. Penman
- **Año:** 2001
- **Publicación o institución:** Irwin / McGraw-Hill
- **Tipo de documento:** Manual de referencia
- **Temática:** TMB-06 Valoración: DCF, múltiplos, ROIC y coste de capital sectorial (principal) · secundarias: —
- **Calidad Q:** 77 (B) — Tipo 22/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 6/10 · Impacto 9/10 · Independencia 10/10 · Acceso 1/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de Liu, Nissim y Thomas 2002, copia del autor en Columbia): https://business.columbia.edu/sites/default/files-efs/pubfiles/318/Equity_Valuation_Using_Multiples.pdf
- **Acceso y licencia:** Libro de pago (hay ediciones posteriores)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Liu Nissim Thomas 2002 "Equity Valuation Using Multiples" Journal of Accounting Research»; WebFetch: sí, sobre la página índice)
- **Contenido:** Manual de análisis de estados financieros orientado a la valoración: reformulación, análisis de rentabilidad (ROCE, RNOA), previsión y beneficio residual.
- **Uso en el Motor:** AG-B16, MC-B06: reformulación de estados financieros y descomposición de la rentabilidad de los candidatos.
- **Limitaciones:** Edición antigua; confirmada solo por página índice.

#### DOC-MOT-0509 · Q 76 (B) — The Equity Risk Premium (modelo Grinold-Kroner)

- **Autores:** Richard Grinold; Kenneth Kroner
- **Año:** 2002
- **Publicación o institución:** Investment Insights, Barclays Global Investors (julio de 2002)
- **Tipo de documento:** Informe técnico con metodología
- **Temática:** TMB-06 Valoración: DCF, múltiplos, ROIC y coste de capital sectorial (principal) · secundarias: TMB-07
- **Calidad Q:** 76 (B) — Tipo 15/25 · Rigor 15/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 7/10 · Acceso 6/10
- **DOI / ISBN / URL:** Verificada en página índice: https://en.wikipedia.org/wiki/Grinold_and_Kroner_Model
- **Acceso y licencia:** Publicación de gestora; sin copia oficial localizada en abierto
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Grinold Kroner "Investment Insights" Barclays Global Investors 2002 equity risk premium building blocks»; WebFetch: sí, sobre la página índice)
- **Contenido:** Descompone la rentabilidad esperada de la renta variable en rentabilidad por dividendo, inflación esperada, crecimiento real de beneficios, variación del número de acciones (recompras/emisiones) y variación del PER.
- **Uso en el Motor:** AG-B16, MC-B06: rentabilidad esperada por bloques (dividendo, crecimiento, recompras, cambio de múltiplo) aplicada a un índice sectorial.
- **Limitaciones:** Documento de gestora, no revisado por pares; supuestos de reversión del PER subjetivos; confirmada solo por página índice.

#### MBM-0109 · Q 74 (B) — Arbitrage Pricing Theory and Utility Stock Returns

- **Autores:** Dorothy H. Bower; Richard S. Bower; Dennis E. Logue
- **Año:** 1984
- **Publicación o institución:** Journal of Finance, 39(4), 1041-1054
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-06 Valoración: DCF, múltiplos, ROIC y coste de capital sectorial (principal) · secundarias: TMB-07
- **Calidad Q:** 74 (B) — Tipo 25/25 · Rigor 13/20 · Autoridad 12/15 · Vigencia 4/10 · Impacto 7/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** Verificada en página índice (referencias de Fama y French 1997 en IDEAS): https://ideas.repec.org/a/eee/jfinec/v43y1997i2p153-193.html
- **Acceso y licencia:** Artículo de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Fama French 1997 "Industry costs of equity" Journal of Financial Economics 43»; WebFetch: sí, sobre la página índice)
- **Contenido:** Aplica la teoría de valoración por arbitraje (APT) a las rentabilidades de las utilities y la compara con el CAPM para el coste de capital.
- **Uso en el Motor:** AG-B16, MC-B06: coste de capital de sectores regulados con modelos multifactoriales (AG-B07, AG-B09).
- **Limitaciones:** Confirmada solo por página índice.

#### MBM-0110 · Q 71 (B) — The Arbitrage Pricing Theory and Cost-of-Capital Estimation: The Case of Electric Utilities

- **Autores:** David H. Goldenberg; Ashok J. Robin
- **Año:** 1991
- **Publicación o institución:** Journal of Financial Research, 14(3), 181-196
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-06 Valoración: DCF, múltiplos, ROIC y coste de capital sectorial (principal) · secundarias: —
- **Calidad Q:** 71 (B) — Tipo 25/25 · Rigor 12/20 · Autoridad 11/15 · Vigencia 4/10 · Impacto 6/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** Verificada en página índice (referencias de Fama y French 1997 en IDEAS): https://ideas.repec.org/a/eee/jfinec/v43y1997i2p153-193.html
- **Acceso y licencia:** Artículo de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Fama French 1997 "Industry costs of equity" Journal of Financial Economics 43»; WebFetch: sí, sobre la página índice)
- **Contenido:** Estima el coste de capital de las eléctricas con la APT y discute su utilidad regulatoria.
- **Uso en el Motor:** AG-B16, MC-B06: coste de capital sectorial de utilities para valorar candidatos regulados.
- **Limitaciones:** Confirmada solo por página índice.

#### MBM-0107 · Q 66 (B) — Equity Premia as Low as Three Percent? Empirical Evidence from Analysts' Earnings Forecasts for Domestic and International Stock Markets

- **Autores:** James J. Claus; Jacob K. Thomas
- **Año:** 2000
- **Publicación o institución:** Documento de trabajo, Columbia University (Nueva York)
- **Tipo de documento:** Documento de trabajo
- **Temática:** TMB-06 Valoración: DCF, múltiplos, ROIC y coste de capital sectorial (principal) · secundarias: —
- **Calidad Q:** 66 (B) — Tipo 12/25 · Rigor 14/20 · Autoridad 13/15 · Vigencia 6/10 · Impacto 8/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de Liu, Nissim y Thomas 2002, copia del autor en Columbia): https://business.columbia.edu/sites/default/files-efs/pubfiles/318/Equity_Valuation_Using_Multiples.pdf
- **Acceso y licencia:** Documento de trabajo
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Liu Nissim Thomas 2002 "Equity Valuation Using Multiples" Journal of Accounting Research»; WebFetch: sí, sobre la página índice)
- **Contenido:** Estima primas de riesgo implícitas con modelos de beneficio residual y previsiones de analistas en varios mercados y obtiene primas bajas.
- **Uso en el Motor:** AG-B16, MC-B06: prima de riesgo implícita por mercado geográfico.
- **Limitaciones:** Se cita la versión de trabajo vista en la página índice; confirmada solo por página índice.

#### MBM-0106 · Q 64 (C) — Estimating Industry Multiples

- **Autores:** Malcolm Baker; Richard Ruback
- **Año:** 1999
- **Publicación o institución:** Documento de trabajo, Harvard University
- **Tipo de documento:** Documento de trabajo
- **Temática:** TMB-06 Valoración: DCF, múltiplos, ROIC y coste de capital sectorial (principal) · secundarias: TMB-04
- **Calidad Q:** 64 (C) — Tipo 12/25 · Rigor 14/20 · Autoridad 13/15 · Vigencia 5/10 · Impacto 7/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de Liu, Nissim y Thomas 2002, copia del autor en Columbia): https://business.columbia.edu/sites/default/files-efs/pubfiles/318/Equity_Valuation_Using_Multiples.pdf
- **Acceso y licencia:** Documento de trabajo
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Liu Nissim Thomas 2002 "Equity Valuation Using Multiples" Journal of Accounting Research»; WebFetch: sí, sobre la página índice)
- **Contenido:** Estima múltiplos sectoriales con métodos estadísticos (media armónica, mínimo error) y compara bases (EBITDA, EBIT, ventas).
- **Uso en el Motor:** AG-B16, MC-B06: cálculo del múltiplo sectorial representativo (media armónica) para valoración relativa.
- **Limitaciones:** Documento de trabajo; confirmada solo por página índice.

## TMB-07 Modelos factoriales, cribado cuantitativo y rankings

#### ANA-DOC-0279 · Q 96 (A) — Quality Minus Junk

- **Autores:** Clifford S. Asness; Andrea Frazzini; Lasse Heje Pedersen
- **Año:** 2019
- **Publicación o institución:** Review of Accounting Studies, vol. 24, n.º 1, págs. 34-112
- **Tipo de documento:** Artículo revisado por pares (acceso abierto)
- **Temática:** TMB-07 Modelos factoriales, cribado cuantitativo y rankings (principal) · secundarias: TMB-06
- **Calidad Q:** 96 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 9/10 · Acceso 10/10
- **DOI / ISBN / URL:** DOI: 10.1007/s11142-018-9470-2 · https://research-api.cbs.dk/ws/portalfiles/portal/60211462/lasse_heje_pedersen_et_al_quality_minus_junk_publishersversion.pdf
- **Acceso y licencia:** Acceso abierto, licencia CC BY (versión editorial en el repositorio de la Copenhagen Business School)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Frazzini Pedersen "Betting Against Beta" Asness "Quality Minus Junk" Review of Accounting Studies»; WebFetch: sí)
- **Contenido:** Define la calidad (rentabilidad, crecimiento, seguridad, remuneración) y muestra que las acciones de calidad tienen precios más altos pero no lo suficiente: el factor QMJ obtiene rentabilidades positivas.
- **Uso en el Motor:** AG-B16, MC-B07: definición operativa de calidad (rentabilidad, crecimiento, seguridad, remuneración) para puntuar candidatos (AG-B12).
- **Limitaciones:** Autores vinculados a AQR.

#### DOC-MOT-0061 · Q 95 (A) — A Five-Factor Asset Pricing Model

- **Autores:** Eugene F. Fama; Kenneth R. French
- **Año:** 2015
- **Publicación o institución:** Journal of Financial Economics, vol. 116, n.º 1, págs. 1-22
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-07 Modelos factoriales, cribado cuantitativo y rankings (principal) · secundarias: TMB-06
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1016/j.jfineco.2014.10.010 · https://doi.org/10.1016%2Fj.jfineco.2014.10.010 · CiteSeerX: https://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.645.3745
- **Acceso y licencia:** Texto completo por suscripción en la editorial (Elsevier)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Fama–French three-factor model capital asset pricing model Black–Litterman arbitrage pricing theory (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Fama–French three-factor model», que reproduce la cita completa)
- **Contenido:** Amplía el modelo de tres factores con rentabilidad (RMW) e inversión (CMA); el factor valor resulta redundante en EE. UU.
- **Uso en el Motor:** AG-B16, MC-B07: factores de rentabilidad e inversión (cinco factores) como señales de cribado y para controlar la exposición factorial de una lista de candidatos (AG-B12 Seleccionador de Activos).
- **Limitaciones:** No incorpora momentum; evidencia centrada en EE. UU.
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (tanda 2).

#### DOC-MOT-0344 · Q 95 (A) — Betting Against Beta

- **Autores:** Andrea Frazzini; Lasse Heje Pedersen
- **Año:** 2014
- **Publicación o institución:** Journal of Financial Economics, vol. 111, n.º 1, págs. 1-25
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-07 Modelos factoriales, cribado cuantitativo y rankings (principal) · secundarias: —
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 9/10 · Acceso 8/10
- **DOI / ISBN / URL:** Sin DOI visto · Copia del autor: http://pages.stern.nyu.edu/~lpederse/papers/BettingAgainstBeta.pdf
- **Acceso y licencia:** Copia gratuita del autor; revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «momentum investing Jegadeesh Titman time series momentum carry trade betting against beta low-volatility anomaly (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Low-volatility anomaly», que reproduce la cita completa)
- **Contenido:** Factor BAB (largo baja beta apalancada, corto alta beta) rentable en múltiples clases de activos, explicado por restricciones de financiación.
- **Uso en el Motor:** AG-B16, MC-B07: señal de baja beta y ajuste del apalancamiento en rankings de candidatos.
- **Limitaciones:** Autores vinculados a gestora (AQR).
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0065 · Q 95 (A) — Value and Momentum Everywhere

- **Autores:** Clifford S. Asness; Tobias J. Moskowitz; Lasse Heje Pedersen
- **Año:** 2013
- **Publicación o institución:** The Journal of Finance, vol. 68, n.º 3, págs. 929-985
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-07 Modelos factoriales, cribado cuantitativo y rankings (principal) · secundarias: —
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1111/jofi.12021 · https://onlinelibrary.wiley.com/doi/abs/10.1111/jofi.12021 · Repositorio: https://research.cbs.dk/en/publications/9cef71a9-adf5-4d83-925d-53c571dd0691
- **Acceso y licencia:** Texto completo por suscripción en la editorial (Wiley); registro en repositorio CBS
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «momentum investing Jegadeesh Titman time series momentum carry trade betting against beta low-volatility anomaly (dominio en.wikipedia.org)»; WebFetch: sí, páginas índice de Wikipedia «Factor investing» y «Momentum investing»)
- **Contenido:** Construye de forma homogénea factores valor y momentum en ocho mercados/clases de activo y documenta su correlación negativa y estructura factorial común.
- **Uso en el Motor:** AG-B16, MC-B07: combinación de valor y momentum en distintos mercados y clases de activo para rankings compuestos.
- **Limitaciones:** Costes de transacción no modelados en detalle.
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (tanda 2).

#### DOC-MOT-0345 · Q 95 (A) — The Cross-Section of Volatility and Expected Returns

- **Autores:** Andrew Ang; Robert J. Hodrick; Yuhang Xing; Xiaoyan Zhang
- **Año:** 2006
- **Publicación o institución:** The Journal of Finance, vol. 61, n.º 1, págs. 259-299
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-07 Modelos factoriales, cribado cuantitativo y rankings (principal) · secundarias: TMB-09
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI: 10.1111/j.1540-6261.2006.00836.x · NBER: http://www.nber.org/papers/w10852.pdf
- **Acceso y licencia:** NBER WP gratuito; revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «momentum investing Jegadeesh Titman time series momentum carry trade betting against beta low-volatility anomaly (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Low-volatility anomaly», que reproduce la cita completa)
- **Contenido:** La sensibilidad a la volatilidad agregada se remunera negativamente y las acciones con alta volatilidad idiosincrática rinden menos.
- **Uso en el Motor:** AG-B16, MC-B07: volatilidad idiosincrática como señal negativa en el cribado.
- **Limitaciones:** Robustez discutida en la literatura posterior.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0062 · Q 95 (A) — On Persistence in Mutual Fund Performance

- **Autores:** Mark M. Carhart
- **Año:** 1997
- **Publicación o institución:** The Journal of Finance, vol. 52, n.º 1, págs. 57-82
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-07 Modelos factoriales, cribado cuantitativo y rankings (principal) · secundarias: TMB-11
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1111/j.1540-6261.1997.tb03808.x · JSTOR: https://www.jstor.org/stable/2329556
- **Acceso y licencia:** Texto completo por suscripción en la editorial (Wiley/JSTOR)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Fama–French three-factor model capital asset pricing model Black–Litterman arbitrage pricing theory (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Fama–French three-factor model», que reproduce la cita completa y «Factor investing»)
- **Contenido:** Añade momentum al modelo de tres factores (modelo de cuatro factores) y muestra que la persistencia de fondos se explica por factores y costes.
- **Uso en el Motor:** AG-B16, MC-B07: modelo de cuatro factores (con momentum) para descontar exposiciones conocidas del rendimiento de una selección.
- **Limitaciones:** Muestra de fondos de EE. UU. 1962-1993.
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (tanda 2).

#### DOC-MOT-0060 · Q 95 (A) — Common Risk Factors in the Returns on Stocks and Bonds

- **Autores:** Eugene F. Fama; Kenneth R. French
- **Año:** 1993
- **Publicación o institución:** Journal of Financial Economics, vol. 33, n.º 1, págs. 3-56
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-07 Modelos factoriales, cribado cuantitativo y rankings (principal) · secundarias: TMB-06
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1016/0304-405X(93)90023-5 · https://doi.org/10.1016%2F0304-405X%2893%2990023-5 · CiteSeerX: https://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.139.5892
- **Acceso y licencia:** Texto completo por suscripción en la editorial (Elsevier); datos de factores en la biblioteca de K. French
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Fama–French three-factor model capital asset pricing model Black–Litterman arbitrage pricing theory (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Fama–French three-factor model», que reproduce la cita completa)
- **Contenido:** Modelo de tres factores (mercado, tamaño SMB, valor HML) y factores de plazo y crédito para bonos, estimados con regresiones de series temporales.
- **Uso en el Motor:** AG-B16, MC-B07: factores tamaño y valor para normalizar rankings y medir exposiciones de candidatos y sectores.
- **Limitaciones:** Anomalías no explicadas (momentum, rentabilidad).
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (tanda 2).

#### DOC-MOT-0064 · Q 95 (A) — Returns to Buying Winners and Selling Losers: Implications for Stock Market Efficiency

- **Autores:** Narasimhan Jegadeesh; Sheridan Titman
- **Año:** 1993
- **Publicación o institución:** The Journal of Finance, vol. 48, n.º 1, págs. 65-91
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-07 Modelos factoriales, cribado cuantitativo y rankings (principal) · secundarias: —
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1111/j.1540-6261.1993.tb04702.x · JSTOR: 2328882 · https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.1993.tb04702.x
- **Acceso y licencia:** Texto completo por suscripción en la editorial (Wiley)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «momentum investing Jegadeesh Titman time series momentum carry trade betting against beta low-volatility anomaly (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Momentum investing», que reproduce la cita completa)
- **Contenido:** Documenta el momentum de sección cruzada con carteras de formación/tenencia de 3-12 meses y sus reversiones posteriores.
- **Uso en el Motor:** AG-B16, MC-B07: señal de momentum (ganadores-perdedores) en el ranking de candidatos y de sectores.
- **Limitaciones:** Muestra 1965-1989; sensibilidad a costes.
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (tanda 2).

#### DOC-MOT-0338 · Q 95 (A) — A Test of the Efficiency of a Given Portfolio

- **Autores:** Michael R. Gibbons; Stephen A. Ross; Jay Shanken
- **Año:** 1989
- **Publicación o institución:** Econometrica, vol. 57, n.º 5, págs. 1121-1152
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-07 Modelos factoriales, cribado cuantitativo y rankings (principal) · secundarias: TMB-11
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.2307/1913625 · JSTOR: https://www.jstor.org/stable/1913625 · CiteSeerX: https://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.557.1995
- **Acceso y licencia:** Texto completo por suscripción en la editorial (Econometric Society/JSTOR)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Fama–French three-factor model capital asset pricing model Black–Litterman arbitrage pricing theory (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Fama–French three-factor model», que reproduce la cita completa)
- **Contenido:** Contraste GRS de muestra finita de que las alfas de un conjunto de carteras son conjuntamente cero respecto a unos factores.
- **Uso en el Motor:** AG-B16, MC-B07: contraste GRS de si un modelo de factores explica las rentabilidades de las carteras de cribado.
- **Limitaciones:** Supone normalidad.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0063 · Q 95 (A) — Risk, Return, and Equilibrium: Empirical Tests

- **Autores:** Eugene F. Fama; James D. MacBeth
- **Año:** 1973
- **Publicación o institución:** Journal of Political Economy, vol. 81, n.º 3, págs. 607-636
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-07 Modelos factoriales, cribado cuantitativo y rankings (principal) · secundarias: TMB-02
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1086/260061 · JSTOR: https://www.jstor.org/stable/1831028 · CiteSeerX: https://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.632.511
- **Acceso y licencia:** Texto completo por suscripción en la editorial (University of Chicago Press)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Ledoit Wolf shrinkage estimation of covariance matrices stationary bootstrap Politis Romano Fama–MacBeth regression (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Fama–MacBeth regression», que reproduce la cita completa)
- **Contenido:** Procedimiento en dos etapas: regresiones de sección cruzada periodo a periodo y promedio temporal de coeficientes para estimar primas de riesgo.
- **Uso en el Motor:** AG-B16, MC-B07: regresiones de sección cruzada de Fama-MacBeth para medir la prima asociada a una señal de cribado.
- **Limitaciones:** Errores estándar sesgados con correlación persistente (véase Petersen 2009).
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (tanda 2).

#### DOC-MOT-0347 · Q 94 (A) — Replicating Anomalies

- **Autores:** Kewei Hou; Chen Xue; Lu Zhang
- **Año:** 2020
- **Publicación o institución:** The Review of Financial Studies, vol. 33, n.º 5, págs. 2019-2133
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-07 Modelos factoriales, cribado cuantitativo y rankings (principal) · secundarias: TMB-11
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1093/rfs/hhy131 · JSTOR: https://www.jstor.org/stable/48574457
- **Acceso y licencia:** Texto completo por suscripción en la editorial (OUP/JSTOR)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «momentum investing Jegadeesh Titman time series momentum carry trade betting against beta low-volatility anomaly (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Factor investing», que reproduce la cita completa)
- **Contenido:** Replica 452 anomalías con controles de microcapitalizaciones: la mayoría no resulta significativa.
- **Uso en el Motor:** AG-B16, MC-B07: cautela sobre señales que no se replican al aplicar filtros de cribado (control de AG-B14 Contrarias).
- **Limitaciones:** Resultados dependientes del tratamiento de microcaps.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0346 · Q 94 (A) — The Other Side of Value: The Gross Profitability Premium

- **Autores:** Robert Novy-Marx
- **Año:** 2013
- **Publicación o institución:** Journal of Financial Economics, vol. 108, n.º 1, págs. 1-28
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-07 Modelos factoriales, cribado cuantitativo y rankings (principal) · secundarias: TMB-06
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1016/j.jfineco.2013.01.003 · https://www.sciencedirect.com/science/article/pii/S0304405X13000044
- **Acceso y licencia:** Texto completo por suscripción en la editorial (Elsevier)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «momentum investing Jegadeesh Titman time series momentum carry trade betting against beta low-volatility anomaly (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Factor investing», que reproduce la cita completa)
- **Contenido:** La rentabilidad bruta sobre activos predice rendimientos con fuerza similar al valor y complementa las estrategias de valor.
- **Uso en el Motor:** AG-B16, MC-B07: rentabilidad bruta sobre activos como señal de calidad en el cribado (AG-B09, AG-B12).
- **Limitaciones:** Medida contable; sensible a definiciones.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0336 · Q 94 (A) — The Cross-Section of Expected Stock Returns

- **Autores:** Eugene F. Fama; Kenneth R. French
- **Año:** 1992
- **Publicación o institución:** The Journal of Finance, vol. 47, n.º 2, págs. 427-465
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-07 Modelos factoriales, cribado cuantitativo y rankings (principal) · secundarias: —
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1111/j.1540-6261.1992.tb04398.x · JSTOR: https://www.jstor.org/stable/2329112
- **Acceso y licencia:** Texto completo por suscripción en la editorial (Wiley/JSTOR)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Fama–French three-factor model capital asset pricing model Black–Litterman arbitrage pricing theory (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Fama–French three-factor model», que reproduce la cita completa y «Capital asset pricing model»)
- **Contenido:** Muestra que tamaño y valor contable/mercado explican la sección cruzada de rentabilidades y la beta no.
- **Uso en el Motor:** AG-B16, MC-B07: evidencia de tamaño y valor contable/mercado como variables de cribado.
- **Limitaciones:** Acciones de EE. UU. 1963-1990.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0335 · Q 94 (A) — The Arbitrage Theory of Capital Asset Pricing

- **Autores:** Stephen A. Ross
- **Año:** 1976
- **Publicación o institución:** Journal of Economic Theory, vol. 13, n.º 3, págs. 341-360
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-07 Modelos factoriales, cribado cuantitativo y rankings (principal) · secundarias: TMB-06
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1016/0022-0531(76)90046-6 · https://doi.org/10.1016%2F0022-0531%2876%2990046-6
- **Acceso y licencia:** Texto completo por suscripción en la editorial (Elsevier)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Fama–French three-factor model capital asset pricing model Black–Litterman arbitrage pricing theory (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Arbitrage pricing theory», que reproduce la cita completa y «Factor investing»)
- **Contenido:** Teoría de valoración por arbitraje (APT): rentabilidades esperadas lineales en las exposiciones a factores comunes sin requerir la cartera de mercado.
- **Uso en el Motor:** AG-B16, MC-B07: base teórica de los modelos multifactoriales (APT) con que se miden exposiciones de candidatos.
- **Limitaciones:** No identifica los factores.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0348 · Q 92 (A) — Economic Forces and the Stock Market

- **Autores:** Nai-Fu Chen; Richard Roll; Stephen A. Ross
- **Año:** 1986
- **Publicación o institución:** The Journal of Business, vol. 59, n.º 3, págs. 383-403
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-07 Modelos factoriales, cribado cuantitativo y rankings (principal) · secundarias: TMB-06
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1086/296344 · JSTOR: https://www.jstor.org/stable/2352710
- **Acceso y licencia:** Texto completo por suscripción en la editorial (University of Chicago Press/JSTOR)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Fama–French three-factor model capital asset pricing model Black–Litterman arbitrage pricing theory (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Arbitrage pricing theory», que reproduce la cita completa)
- **Contenido:** Modelo de factores macroeconómicos (producción, inflación, diferenciales de crédito y de plazo) valorados en la sección cruzada.
- **Uso en el Motor:** AG-B16, MC-B07: factores macroeconómicos (producción, inflación, diferenciales) para medir la sensibilidad de sectores y candidatos al ciclo (AG-B08).
- **Limitaciones:** Estabilidad de primas discutida.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### MBM-0112 · Q 85 (A) — Evidence on the Characteristics of Cross Sectional Variation in Stock Returns

- **Autores:** Kent Daniel; Sheridan Titman
- **Año:** 1997
- **Publicación o institución:** The Journal of Finance, 52(1), 1-33
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-07 Modelos factoriales, cribado cuantitativo y rankings (principal) · secundarias: —
- **Calidad Q:** 85 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 5/10 · Impacto 10/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** Verificada en página índice (referencias de Harvey, Liu y Zhu, NBER WP 20592, en IDEAS): https://ideas.repec.org/p/nbr/nberwo/20592.html
- **Acceso y licencia:** Artículo de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Harvey Liu Zhu 2016 "… and the Cross-Section of Expected Returns" Review of Financial Studies ideas.repec»; WebFetch: sí, sobre la página índice)
- **Contenido:** Muestra que las características (tamaño, valor contable/mercado), más que las cargas factoriales, explican las rentabilidades medias.
- **Uso en el Motor:** AG-B16, MC-B07: justificar el cribado por características de la empresa frente a betas estimadas.
- **Limitaciones:** Confirmada solo por página índice.

#### MBM-0114 · Q 85 (A) — Multifactor Explanations of Asset Pricing Anomalies

- **Autores:** Eugene F. Fama; Kenneth R. French
- **Año:** 1996
- **Publicación o institución:** The Journal of Finance, 51(1), 55-84
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-07 Modelos factoriales, cribado cuantitativo y rankings (principal) · secundarias: TMB-06
- **Calidad Q:** 85 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 5/10 · Impacto 10/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** Verificada en página índice (referencias de Fama y French 1997 en IDEAS): https://ideas.repec.org/a/eee/jfinec/v43y1997i2p153-193.html
- **Acceso y licencia:** Artículo de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Fama French 1997 "Industry costs of equity" Journal of Financial Economics 43»; WebFetch: sí, sobre la página índice)
- **Contenido:** Contrasta si el modelo de tres factores explica anomalías (PER, flujo de caja/precio, crecimiento de ventas, reversión a largo plazo); no explica el momentum.
- **Uso en el Motor:** AG-B16, MC-B07: comprobar si una señal de cribado aporta algo más allá de tamaño y valor.
- **Limitaciones:** Confirmada solo por página índice.

#### MBM-0121 · Q 84 (A) — In Search of Distress Risk

- **Autores:** John Y. Campbell; Jens Hilscher; Jan Szilagyi
- **Año:** 2008
- **Publicación o institución:** The Journal of Finance, 63(6), 2899-2939
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-07 Modelos factoriales, cribado cuantitativo y rankings (principal) · secundarias: TMB-09
- **Calidad Q:** 84 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 7/10 · Impacto 9/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** Verificada en página índice (referencias de Harvey, Liu y Zhu, NBER WP 20592, en IDEAS): https://ideas.repec.org/p/nbr/nberwo/20592.html
- **Acceso y licencia:** Artículo de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Harvey Liu Zhu 2016 "… and the Cross-Section of Expected Returns" Review of Financial Studies ideas.repec»; WebFetch: sí, sobre la página índice)
- **Contenido:** Modelo logit de probabilidad de quiebra con variables contables y de mercado; las empresas en dificultades obtienen rentabilidades anómalamente bajas.
- **Uso en el Motor:** AG-B16, MC-B07: filtro de riesgo de insolvencia en el cribado de candidatos (AG-B09, AG-B11).
- **Limitaciones:** Confirmada solo por página índice.

#### MBM-0119 · Q 84 (A) — Illiquidity and Stock Returns: Cross-Section and Time-Series Effects

- **Autores:** Yakov Amihud
- **Año:** 2002
- **Publicación o institución:** Journal of Financial Markets, 5(1), 31-56
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-07 Modelos factoriales, cribado cuantitativo y rankings (principal) · secundarias: TMB-09
- **Calidad Q:** 84 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 6/10 · Impacto 10/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** Verificada en página índice (referencias de Harvey, Liu y Zhu, NBER WP 20592, en IDEAS): https://ideas.repec.org/p/nbr/nberwo/20592.html
- **Acceso y licencia:** Artículo de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Harvey Liu Zhu 2016 "… and the Cross-Section of Expected Returns" Review of Financial Studies ideas.repec»; WebFetch: sí, sobre la página índice)
- **Contenido:** Propone la medida de iliquidez de Amihud (rentabilidad absoluta por volumen negociado) y muestra que se remunera.
- **Uso en el Motor:** AG-B16, MC-B07: filtro de liquidez mínima de los candidatos y penalización en el ranking (AG-B10 Flujos, AG-B12).
- **Limitaciones:** Confirmada solo por página índice.

#### MBM-0113 · Q 83 (A) — Testing Factor-Model Explanations of Market Anomalies

- **Autores:** Kent Daniel; Sheridan Titman
- **Año:** 2012
- **Publicación o institución:** Critical Finance Review, 1(1), 103-139
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-07 Modelos factoriales, cribado cuantitativo y rankings (principal) · secundarias: TMB-11
- **Calidad Q:** 83 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 13/15 · Vigencia 8/10 · Impacto 8/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** Verificada en página índice (referencias de Harvey, Liu y Zhu, NBER WP 20592, en IDEAS): https://ideas.repec.org/p/nbr/nberwo/20592.html
- **Acceso y licencia:** Artículo de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Harvey Liu Zhu 2016 "… and the Cross-Section of Expected Returns" Review of Financial Studies ideas.repec»; WebFetch: sí, sobre la página índice)
- **Contenido:** Muestra que los contrastes de modelos factoriales con carteras ordenadas por características tienen poca potencia y propone carteras más exigentes.
- **Uso en el Motor:** AG-B16, MC-B07: diseño de contrastes de las carteras de cribado que no confundan factor y característica.
- **Limitaciones:** Confirmada solo por página índice.

#### MBM-0120 · Q 83 (A) — Asset Growth and the Cross-Section of Stock Returns

- **Autores:** Michael J. Cooper; Huseyin Gulen; Michael J. Schill
- **Año:** 2008
- **Publicación o institución:** The Journal of Finance, 63(4), 1609-1651
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-07 Modelos factoriales, cribado cuantitativo y rankings (principal) · secundarias: TMB-06
- **Calidad Q:** 83 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 7/10 · Impacto 9/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** Verificada en página índice (referencias de Harvey, Liu y Zhu, NBER WP 20592, en IDEAS): https://ideas.repec.org/p/nbr/nberwo/20592.html
- **Acceso y licencia:** Artículo de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Harvey Liu Zhu 2016 "… and the Cross-Section of Expected Returns" Review of Financial Studies ideas.repec»; WebFetch: sí, sobre la página índice)
- **Contenido:** Las empresas con fuerte crecimiento de activos obtienen después rentabilidades bajas.
- **Uso en el Motor:** AG-B16, MC-B07: señal de inversión agresiva como penalización en el ranking (sectores en expansión de capacidad, enlace con AG-B05).
- **Limitaciones:** Confirmada solo por página índice.

#### MBM-0115 · Q 82 (A) — Another Look at the Cross-Section of Expected Stock Returns

- **Autores:** S. P. Kothari; Jay Shanken; Richard G. Sloan
- **Año:** 1995
- **Publicación o institución:** The Journal of Finance, 50(1), 185-224
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-07 Modelos factoriales, cribado cuantitativo y rankings (principal) · secundarias: TMB-14
- **Calidad Q:** 82 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 5/10 · Impacto 9/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** Verificada en página índice (referencias de Fama y French 1997 en IDEAS): https://ideas.repec.org/a/eee/jfinec/v43y1997i2p153-193.html
- **Acceso y licencia:** Artículo de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Fama French 1997 "Industry costs of equity" Journal of Financial Economics 43»; WebFetch: sí, sobre la página índice)
- **Contenido:** Argumenta que el efecto valor está inflado por sesgo de supervivencia en Compustat y por la elección de intervalos de rentabilidad.
- **Uso en el Motor:** AG-B16, MC-B07: control del sesgo de supervivencia en el cribado histórico (enlace con MC-B10).
- **Limitaciones:** Confirmada solo por página índice.

#### MBM-0111 · Q 80 (A) — Active Portfolio Management: A Quantitative Approach for Providing Superior Returns and Controlling Risk (2.ª ed.)

- **Autores:** Richard C. Grinold; Ronald N. Kahn
- **Año:** 2000
- **Publicación o institución:** McGraw-Hill (Nueva York)
- **Tipo de documento:** Manual de referencia
- **Temática:** TMB-07 Modelos factoriales, cribado cuantitativo y rankings (principal) · secundarias: TMB-11
- **Calidad Q:** 80 (A) — Tipo 22/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 7/10 · Impacto 10/10 · Independencia 9/10 · Acceso 1/10
- **DOI / ISBN / URL:** https://find.library.upatras.gr/Record/9894?lng=en
- **Acceso y licencia:** Libro de pago
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Grinold Kahn "Active Portfolio Management" quantitative approach second edition McGraw-Hill 2000 Grinold 1989 "fundamental law of active management"»; WebFetch: sí (registro de catálogo))
- **Contenido:** Manual de gestión activa cuantitativa: previsión de alfas, coeficiente de información, ley fundamental de la gestión activa, modelos de riesgo multifactoriales y construcción de carteras.
- **Uso en el Motor:** AG-B16, MC-B07: convertir puntuaciones de cribado en alfas esperadas (z-score × IC × volatilidad) y medir la calidad de un ranking con el coeficiente de información (AG-B12).
- **Limitaciones:** Autores vinculados a BARRA/BGI; enfoque de gestión de carteras más que de selección sectorial.

#### MBM-0117 · Q 80 (A) — The Relationship between Return and Market Value of Common Stocks

- **Autores:** Rolf W. Banz
- **Año:** 1981
- **Publicación o institución:** Journal of Financial Economics, 9(1), 3-18
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-07 Modelos factoriales, cribado cuantitativo y rankings (principal) · secundarias: —
- **Calidad Q:** 80 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 3/10 · Impacto 10/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** Verificada en página índice (referencias de Harvey, Liu y Zhu, NBER WP 20592, en IDEAS): https://ideas.repec.org/p/nbr/nberwo/20592.html
- **Acceso y licencia:** Artículo de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Harvey Liu Zhu 2016 "… and the Cross-Section of Expected Returns" Review of Financial Studies ideas.repec»; WebFetch: sí, sobre la página índice)
- **Contenido:** Documenta el efecto tamaño: las empresas pequeñas obtienen rentabilidades ajustadas por riesgo superiores.
- **Uso en el Motor:** AG-B16, MC-B07: control del tamaño en rankings de candidatos de distinta capitalización.
- **Limitaciones:** Efecto debilitado tras su publicación; confirmada solo por página índice.

#### MBM-0116 · Q 79 (B) — Evaluating the Performance of Value Versus Glamour Stocks: The Impact of Selection Bias

- **Autores:** Louis K. C. Chan; Narasimhan Jegadeesh; Josef Lakonishok
- **Año:** 1995
- **Publicación o institución:** Journal of Financial Economics, 38(3), 269-296
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-07 Modelos factoriales, cribado cuantitativo y rankings (principal) · secundarias: TMB-14
- **Calidad Q:** 79 (B) — Tipo 25/25 · Rigor 15/20 · Autoridad 13/15 · Vigencia 5/10 · Impacto 8/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** Verificada en página índice (referencias de Fama y French 1997 en IDEAS): https://ideas.repec.org/a/eee/jfinec/v43y1997i2p153-193.html
- **Acceso y licencia:** Artículo de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Fama French 1997 "Industry costs of equity" Journal of Financial Economics 43»; WebFetch: sí, sobre la página índice)
- **Contenido:** Estudia si el sesgo de selección en las bases de datos explica la prima de valor y concluye que no la elimina.
- **Uso en el Motor:** AG-B16, MC-B07: comprobar la robustez de rankings de valor a sesgos de datos.
- **Limitaciones:** Confirmada solo por página índice.

#### MBM-0123 · Q 78 (B) — Mean-Variance Spanning

- **Autores:** Gur Huberman; Shmuel Kandel
- **Año:** 1987
- **Publicación o institución:** The Journal of Finance, 42(4), 873-888
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-07 Modelos factoriales, cribado cuantitativo y rankings (principal) · secundarias: TMB-11
- **Calidad Q:** 78 (B) — Tipo 25/25 · Rigor 15/20 · Autoridad 13/15 · Vigencia 4/10 · Impacto 8/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** Verificada en página índice (referencias de Fama y French 1997 en IDEAS): https://ideas.repec.org/a/eee/jfinec/v43y1997i2p153-193.html
- **Acceso y licencia:** Artículo de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Fama French 1997 "Industry costs of equity" Journal of Financial Economics 43»; WebFetch: sí, sobre la página índice)
- **Contenido:** Contraste de si añadir nuevos activos amplía la frontera media-varianza de un conjunto dado.
- **Uso en el Motor:** AG-B16, MC-B07: comprobar si una nueva cartera de cribado (sector, temática) aporta diversificación frente a factores existentes.
- **Limitaciones:** Confirmada solo por página índice.

#### MBM-0118 · Q 78 (B) — Investment Performance of Common Stocks in Relation to Their Price-Earnings Ratios: A Test of the Efficient Market Hypothesis

- **Autores:** Sanjoy Basu
- **Año:** 1977
- **Publicación o institución:** The Journal of Finance, 32(3), 663-682
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-07 Modelos factoriales, cribado cuantitativo y rankings (principal) · secundarias: TMB-06
- **Calidad Q:** 78 (B) — Tipo 25/25 · Rigor 14/20 · Autoridad 13/15 · Vigencia 3/10 · Impacto 10/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** Verificada en página índice (referencias de Harvey, Liu y Zhu, NBER WP 20592, en IDEAS): https://ideas.repec.org/p/nbr/nberwo/20592.html
- **Acceso y licencia:** Artículo de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Harvey Liu Zhu 2016 "… and the Cross-Section of Expected Returns" Review of Financial Studies ideas.repec»; WebFetch: sí, sobre la página índice)
- **Contenido:** Muestra que las carteras de PER bajo superan a las de PER alto en rentabilidad ajustada por riesgo.
- **Uso en el Motor:** AG-B16, MC-B07: base del cribado por múltiplo de beneficios (enlace con MC-B06).
- **Limitaciones:** Antiguo; confirmada solo por página índice.

#### MBM-0122 · Q 76 (B) — Detecting GAAP Violation: Implications for Assessing Earnings Management among Firms with Extreme Financial Performance

- **Autores:** Messod D. Beneish
- **Año:** 1997
- **Publicación o institución:** Journal of Accounting and Public Policy, 16(3), 271-309
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-07 Modelos factoriales, cribado cuantitativo y rankings (principal) · secundarias: TMB-14
- **Calidad Q:** 76 (B) — Tipo 25/25 · Rigor 14/20 · Autoridad 12/15 · Vigencia 4/10 · Impacto 8/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** Verificada en página índice (referencias de Harvey, Liu y Zhu, NBER WP 20592, en IDEAS): https://ideas.repec.org/p/nbr/nberwo/20592.html
- **Acceso y licencia:** Artículo de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Harvey Liu Zhu 2016 "… and the Cross-Section of Expected Returns" Review of Financial Studies ideas.repec»; WebFetch: sí, sobre la página índice)
- **Contenido:** Modelo con ratios contables para detectar manipulación de resultados entre empresas con resultados extremos (precursor del M-score).
- **Uso en el Motor:** AG-B16, MC-B07: bandera roja contable en el cribado de candidatos antes de pasarlos al Bloque C.
- **Limitaciones:** Confirmada solo por página índice.

## TMB-08 Simulación Monte Carlo, escenarios y sensibilidad

#### DOC-MOT-0369 · Q 97 (A) — Multilevel Monte Carlo Path Simulation

- **Autores:** Michael B. Giles
- **Año:** 2008
- **Publicación o institución:** Operations Research, vol. 56, n.º 3, págs. 607-617
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-08 Simulación Monte Carlo, escenarios y sensibilidad (principal) · secundarias: —
- **Calidad Q:** 97 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI: 10.1287/opre.1070.0496 · Copia abierta: https://ora.ox.ac.uk/objects/uuid:d9d28973-94aa-4179-962a-28bcfa8d8f00/datastreams/ATTACHMENT01
- **Acceso y licencia:** Copia gratuita en ORA (Oxford); revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Monte Carlo methods in finance Sobol sequence multilevel Monte Carlo Mersenne Twister Euler–Maruyama (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Multilevel Monte Carlo method», que reproduce la cita completa)
- **Contenido:** Monte Carlo multinivel: combina discretizaciones de distinta finura para reducir el coste de O(ε⁻³) a O(ε⁻² (log ε)²).
- **Uso en el Motor:** MC-B08: reducción del coste de simulaciones de trayectorias (precios de materias primas, demanda) cuando el Motor encadena muchos escenarios.
- **Limitaciones:** Requiere acoplamiento entre niveles.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02. Reutilizada en F8 del Bloque B V2.0 (TMB-08) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0370 · Q 96 (A) — Multilevel Monte Carlo Methods

- **Autores:** Michael B. Giles
- **Año:** 2015
- **Publicación o institución:** Acta Numerica, vol. 24, págs. 259-328
- **Tipo de documento:** Artículo de revisión revisado por pares
- **Temática:** TMB-08 Simulación Monte Carlo, escenarios y sensibilidad (principal) · secundarias: —
- **Calidad Q:** 96 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** DOI: 10.1017/s096249291500001x · arXiv: https://arxiv.org/abs/1304.5472
- **Acceso y licencia:** Preprint gratuito en arXiv
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Monte Carlo methods in finance Sobol sequence multilevel Monte Carlo Mersenne Twister Euler–Maruyama (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Multilevel Monte Carlo method», que reproduce la cita completa)
- **Contenido:** Revisión completa de MLMC: teoría de complejidad, aplicaciones en finanzas, EDP estocásticas y variantes.
- **Uso en el Motor:** MC-B08: marco general de Monte Carlo multinivel para acotar error y coste en simulaciones encadenadas de escenarios sectoriales.
- **Limitaciones:** Técnico.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02. Reutilizada en F8 del Bloque B V2.0 (TMB-08) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0372 · Q 96 (A) — Mersenne Twister: A 623-Dimensionally Equidistributed Uniform Pseudo-Random Number Generator

- **Autores:** Makoto Matsumoto; Takuji Nishimura
- **Año:** 1998
- **Publicación o institución:** ACM Transactions on Modeling and Computer Simulation, vol. 8, n.º 1, págs. 3-30
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-08 Simulación Monte Carlo, escenarios y sensibilidad (principal) · secundarias: TMB-14
- **Calidad Q:** 96 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** DOI: 10.1145/272991.272995 · PDF de los autores: http://www.math.sci.hiroshima-u.ac.jp/~m-mat/MT/ARTICLES/mt.pdf
- **Acceso y licencia:** Copia gratuita de los autores
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Monte Carlo methods in finance Sobol sequence multilevel Monte Carlo Mersenne Twister Euler–Maruyama (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Pseudorandom number generator», que reproduce la cita completa)
- **Contenido:** Generador MT19937 de periodo 2^19937−1 y equidistribución en 623 dimensiones; estándar en software científico.
- **Uso en el Motor:** MC-B08 y MC-B10: generador pseudoaleatorio estándar; fijar y registrar semilla y generador para reproducir cada simulación (TMB-14).
- **Limitaciones:** No apto para criptografía; falla algunas baterías (TestU01).
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02. Reutilizada en F8 del Bloque B V2.0 (TMB-08) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0374 · Q 94 (A) — Improved Long-Period Generators Based on Linear Recurrences Modulo 2

- **Autores:** François Panneton; Pierre L'Ecuyer; Makoto Matsumoto
- **Año:** 2006
- **Publicación o institución:** ACM Transactions on Mathematical Software, vol. 32, n.º 1, págs. 1-16
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-08 Simulación Monte Carlo, escenarios y sensibilidad (principal) · secundarias: TMB-14
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** DOI: 10.1145/1132973.1132974 · PDF: http://www.iro.umontreal.ca/~lecuyer/myftp/papers/wellrng.pdf
- **Acceso y licencia:** Copia gratuita del autor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Monte Carlo methods in finance Sobol sequence multilevel Monte Carlo Mersenne Twister Euler–Maruyama (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Pseudorandom number generator», que reproduce la cita completa)
- **Contenido:** Generadores WELL con mejor equidistribución y recuperación más rápida de estados con muchos ceros que el Mersenne Twister.
- **Uso en el Motor:** MC-B08: generadores WELL de periodo largo como alternativa al Mersenne Twister en simulaciones masivas reproducibles.
- **Limitaciones:** Menor adopción que MT.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02. Reutilizada en F8 del Bloque B V2.0 (TMB-08) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0375 · Q 94 (A) — An Algorithmic Introduction to Numerical Simulation of Stochastic Differential Equations

- **Autores:** Desmond J. Higham
- **Año:** 2001
- **Publicación o institución:** SIAM Review, vol. 43, n.º 3, págs. 525-546
- **Tipo de documento:** Artículo de revisión revisado por pares
- **Temática:** TMB-08 Simulación Monte Carlo, escenarios y sensibilidad (principal) · secundarias: —
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1137/S0036144500378302 · CiteSeerX: 10.1.1.137.6375
- **Acceso y licencia:** Copia en CiteSeerX; revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Euler–Maruyama method Milstein method Crank–Nicolson finite difference methods for option pricing antithetic variates (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Stochastic differential equation», que reproduce la cita completa)
- **Contenido:** Introducción práctica con código a Euler-Maruyama, Milstein, convergencia fuerte y débil y estabilidad.
- **Uso en el Motor:** MC-B08: esquemas de Euler-Maruyama y Milstein para simular trayectorias de precios, costes de insumos o demanda en escenarios estocásticos.
- **Limitaciones:** Introductorio.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02. Reutilizada en F8 del Bloque B V2.0 (TMB-08) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0080 · Q 94 (A) — The Stationary Bootstrap

- **Autores:** Dimitris N. Politis; Joseph P. Romano
- **Año:** 1994
- **Publicación o institución:** Journal of the American Statistical Association, vol. 89, n.º 428, págs. 1303-1313
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-08 Simulación Monte Carlo, escenarios y sensibilidad (principal) · secundarias: TMB-11
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1080/01621459.1994.10476870 · https://doi.org/10.1080/01621459.1994.10476870
- **Acceso y licencia:** Texto completo por suscripción en la editorial (Taylor & Francis)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Ledoit Wolf shrinkage estimation of covariance matrices stationary bootstrap Politis Romano Fama–MacBeth regression (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Bootstrapping (statistics)», que reproduce la cita completa)
- **Contenido:** Remuestreo por bloques de longitud aleatoria geométrica que preserva la estacionariedad de la serie remuestreada.
- **Uso en el Motor:** MC-B08 y MC-B10: remuestreo por bloques para generar escenarios que conservan la dependencia temporal de series sectoriales y para intervalos de confianza de rankings.
- **Limitaciones:** Elección de la longitud media de bloque.
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (tanda 2). Reutilizada en F8 del Bloque B V2.0 (TMB-08) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0368 · Q 92 (A) — Options: A Monte Carlo Approach

- **Autores:** Phelim P. Boyle
- **Año:** 1977
- **Publicación o institución:** Journal of Financial Economics, vol. 4, n.º 3, págs. 323-338
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-08 Simulación Monte Carlo, escenarios y sensibilidad (principal) · secundarias: TMB-06
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1016/0304-405X(77)90005-8 · https://ideas.repec.org/a/eee/jfinec/v4y1977i3p323-338.html
- **Acceso y licencia:** Texto completo por suscripción en la editorial; ficha en IDEAS
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Monte Carlo methods in finance Sobol sequence multilevel Monte Carlo Mersenne Twister Euler–Maruyama (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Monte Carlo methods in finance», que reproduce la cita completa)
- **Contenido:** Primera aplicación de Monte Carlo a la valoración de opciones, con variables antitéticas y de control.
- **Uso en el Motor:** MC-B08: fundamento de la valoración por simulación y de las técnicas antitéticas y de variables de control aplicadas a DCF estocásticos de candidatos (MC-B06).
- **Limitaciones:** Histórico; métodos superados.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02. Reutilizada en F8 del Bloque B V2.0 (TMB-08) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### MBM-0216 · Q 91 (A) — Sensitivity Analysis of Environmental Models: A Systematic Review with Practical Workflow

- **Autores:** Francesca Pianosi; Keith Beven; Jim Freer; Jim W. Hall; Jonathan Rougier; David B. Stephenson; Thorsten Wagener
- **Año:** 2016
- **Publicación o institución:** Environmental Modelling & Software, vol. 79
- **Tipo de documento:** Artículo de revisión revisado por pares
- **Temática:** TMB-08 Simulación Monte Carlo, escenarios y sensibilidad (principal) · secundarias: TMB-14
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 13/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI: 10.1016/j.envsoft.2016.02.008 · Página índice: https://pypi.org/project/SALib/
- **Acceso y licencia:** Acceso abierto (CC BY, según la editorial)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «SALib "An open-source Python library for Sensitivity Analysis" Herman Usher Journal of Open Source Software Morris elementary effects»; WebFetch: sí, página de SALib en PyPI (cita «Pianosi et al. 2016» con DOI; título según la obra citada))
- **Contenido:** Revisión sistemática de métodos de sensibilidad con un flujo de trabajo práctico: definir objetivo, muestreo, método, convergencia y visualización.
- **Uso en el Motor:** MC-B08: flujo de trabajo estándar para el análisis de sensibilidad del Motor y lista de control para el Auditor.
- **Limitaciones:** Aplicaciones ambientales; licencia no comprobada en esta carga.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### MBM-0209 · Q 90 (A) — A Comparison of Three Methods for Selecting Values of Input Variables in the Analysis of Output from a Computer Code

- **Autores:** M. D. McKay; R. J. Beckman; W. J. Conover
- **Año:** 1979 (reimpresión 2000)
- **Publicación o institución:** Technometrics; reimpreso en vol. 42, n.º 1 (número especial del 40.º aniversario), págs. 55-61, 2000
- **Tipo de documento:** Artículo revisado por pares (fundacional)
- **Temática:** TMB-08 Simulación Monte Carlo, escenarios y sensibilidad (principal) · secundarias: —
- **Calidad Q:** 90 (A) — Tipo 24/25 · Rigor 18/20 · Autoridad 14/15 · Vigencia 7/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** JSTOR: http://www.jstor.org/stable/1271432 · Copia abierta: https://www.asc.ohio-state.edu/statistics/comp_exp/jour.club/McKayConoverBeckman.pdf
- **Acceso y licencia:** Copia de lectura abierta (Ohio State); original de pago
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Iman Conover 1982 "distribution-free approach to inducing rank correlation among input variables" McKay Beckman Conover Latin hypercube»; WebFetch: sí, PDF de la reimpresión del año 2000)
- **Contenido:** Introduce el muestreo por hipercubo latino y lo compara con el aleatorio simple y el estratificado.
- **Uso en el Motor:** MC-B08: muestreo estratificado de supuestos para obtener distribuciones de valor estables con menos simulaciones.
- **Limitaciones:** La cita leída es la reimpresión de 2000; datos de la edición de 1979 no vistos.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### DOC-MOT-0371 · Q 90 (A) — Distribution of Points in a Cube and Approximate Evaluation of Integrals

- **Autores:** I. M. Sobol'
- **Año:** 1967
- **Publicación o institución:** Zh. Vych. Mat. Mat. Fiz., vol. 7, págs. 784-802 (traducción: U.S.S.R. Comput. Maths. Math. Phys., vol. 7, págs. 86-112)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-08 Simulación Monte Carlo, escenarios y sensibilidad (principal) · secundarias: TMB-07
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** Sin DOI · Cita en https://en.wikipedia.org/wiki/Sobol_sequence
- **Acceso y licencia:** Sin copia abierta identificada
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Monte Carlo methods in finance Sobol sequence multilevel Monte Carlo Mersenne Twister Euler–Maruyama (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Sobol sequence», que reproduce la cita completa)
- **Contenido:** Introduce las secuencias LPτ (Sobol') de baja discrepancia para integración cuasi-Monte Carlo.
- **Uso en el Motor:** MC-B08: secuencias de baja discrepancia de Sobol' para muestrear el espacio de supuestos (crecimiento, margen, WACC) con menos puntos.
- **Limitaciones:** Acceso difícil; usar implementaciones (Joe-Kuo, SciPy).
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02. Reutilizada en F8 del Bloque B V2.0 (TMB-08) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0373 · Q 89 (A) — Parallel Random Numbers: As Easy as 1, 2, 3

- **Autores:** John K. Salmon; Mark A. Moraes; Ron O. Dror; David E. Shaw
- **Año:** 2011
- **Publicación o institución:** Proceedings of the 2011 International Conference for High Performance Computing, Networking, Storage and Analysis (SC11), artículo 16
- **Tipo de documento:** Comunicación en congreso revisada por pares
- **Temática:** TMB-08 Simulación Monte Carlo, escenarios y sensibilidad (principal) · secundarias: TMB-14
- **Calidad Q:** 89 (A) — Tipo 22/25 · Rigor 18/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1145/2063384.2063405
- **Acceso y licencia:** Actas ACM (suscripción)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Monte Carlo methods in finance Sobol sequence multilevel Monte Carlo Mersenne Twister Euler–Maruyama (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Pseudorandom number generator», que reproduce la cita completa)
- **Contenido:** Generadores basados en contador (Philox, Threefry) para simulación paralela reproducible.
- **Uso en el Motor:** MC-B08: generadores basados en contador para simulación paralela reproducible de escenarios.
- **Limitaciones:** Comunicación de congreso.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02. Reutilizada en F8 del Bloque B V2.0 (TMB-08) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### MBM-0205 · Q 89 (A) — Variance Based Sensitivity Analysis of Model Output. Design and Estimator for the Total Sensitivity Index

- **Autores:** Andrea Saltelli; Paola Annoni; Ivano Azzini; Francesca Campolongo; Marco Ratto; Stefano Tarantola
- **Año:** 2010
- **Publicación o institución:** Computer Physics Communications, vol. 181, n.º 2, págs. 259-270
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-08 Simulación Monte Carlo, escenarios y sensibilidad (principal) · secundarias: —
- **Calidad Q:** 89 (A) — Tipo 24/25 · Rigor 19/20 · Autoridad 14/15 · Vigencia 8/10 · Impacto 10/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** Página índice: https://en.wikipedia.org/wiki/Variance-based_sensitivity_analysis · Listado del método en https://pypi.org/project/SALib/ (DOI no visto)
- **Acceso y licencia:** De pago (Elsevier)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «variance-based sensitivity analysis Sobol indices Saltelli Global Sensitivity Analysis The Primer wikipedia»; WebFetch: sí, páginas índice de Wikipedia y de SALib en PyPI)
- **Contenido:** Diseño muestral y estimadores recomendados para los índices de Sobol de primer orden y totales.
- **Uso en el Motor:** MC-B08: estimador estándar de los índices totales que implementa el Motor (vía SALib).
- **Limitaciones:** Requiere N·(k+2) evaluaciones del modelo.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### DOC-MOT-0006 · Q 89 (A) — Monte Carlo Methods in Financial Engineering

- **Autores:** Paul Glasserman
- **Año:** 2003
- **Publicación o institución:** Springer (Stochastic Modelling and Applied Probability, vol. 53)
- **Tipo de documento:** Libro académico
- **Temática:** TMB-08 Simulación Monte Carlo, escenarios y sensibilidad (principal) · secundarias: TMB-09
- **Calidad Q:** 89 (A) — Tipo 20/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** ISBN: 0-387-00451-3 (978-0-387-00451-8) · DOI del libro: 10.1007/978-0-387-21617-1 (verificado en V2.3) · Préstamo digital: https://archive.org/details/montecarlomethod53glas
- **Acceso y licencia:** De pago (Springer)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Monte Carlo methods in finance Sobol sequence multilevel Monte Carlo Mersenne Twister Euler–Maruyama (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Monte Carlo methods in finance», que reproduce la cita completa y «Quasi-Monte Carlo methods in finance»)
- **Contenido:** Monte Carlo en finanzas: generación de variables, discretización, reducción de varianza, cuasi-Monte Carlo, sensibilidades y opciones americanas.
- **Uso en el Motor:** MC-B08 (AG-B16): manual de referencia para simular escenarios de demanda, márgenes y valor de candidatos; reducción de varianza y control del error de simulación.
- **Limitaciones:** No cubre MLMC (posterior).
- **Origen:** Ficha de carga V2.3 re-verificada por DOC-M el 2026-11-02 (tanda 2); se normaliza al formato del encargo. Reutilizada en F8 del Bloque B V2.0 (TMB-08) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### MBM-0201 · Q 89 (A) — Global Sensitivity Indices for Nonlinear Mathematical Models and Their Monte Carlo Estimates

- **Autores:** Ilya M. Sobol'
- **Año:** 2001
- **Publicación o institución:** Mathematics and Computers in Simulation, vol. 55, n.º 1-3, págs. 271-280
- **Tipo de documento:** Artículo revisado por pares (fundacional)
- **Temática:** TMB-08 Simulación Monte Carlo, escenarios y sensibilidad (principal) · secundarias: TMB-07
- **Calidad Q:** 89 (A) — Tipo 24/25 · Rigor 19/20 · Autoridad 14/15 · Vigencia 8/10 · Impacto 10/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** DOI: 10.1016/S0378-4754(00)00270-6 · Página índice: https://en.wikipedia.org/wiki/Variance-based_sensitivity_analysis
- **Acceso y licencia:** De pago (Elsevier)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «variance-based sensitivity analysis Sobol indices Saltelli Global Sensitivity Analysis The Primer wikipedia»; WebFetch: sí, página índice de Wikipedia «Variance-based sensitivity analysis» (bibliografía con DOI))
- **Contenido:** Define los índices de sensibilidad global de primer orden y totales basados en la descomposición de la varianza y su estimación por Monte Carlo.
- **Uso en el Motor:** MC-B08 (AG-B16): calcular índices de Sobol de un DCF o de un modelo de dimensionado de mercado para saber qué supuestos (crecimiento, margen, WACC, adopción) explican la dispersión del resultado.
- **Limitaciones:** Supone entradas independientes; coste computacional alto con modelos lentos.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### DOC-MOT-0378 · Q 89 (A) — Quasi-Monte Carlo Methods in Numerical Finance

- **Autores:** Corwin Joy; Phelim P. Boyle; Ken Seng Tan
- **Año:** 1996
- **Publicación o institución:** Management Science, vol. 42, n.º 6, págs. 926-938
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-08 Simulación Monte Carlo, escenarios y sensibilidad (principal) · secundarias: —
- **Calidad Q:** 89 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** Sin DOI visto · Cita en https://en.wikipedia.org/wiki/Quasi-Monte_Carlo_methods_in_finance
- **Acceso y licencia:** Texto completo por suscripción en la editorial (INFORMS)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Monte Carlo methods in finance Sobol sequence multilevel Monte Carlo Mersenne Twister Euler–Maruyama (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Quasi-Monte Carlo methods in finance», que reproduce la cita completa)
- **Contenido:** Aplica secuencias de baja discrepancia a la valoración de derivados y muestra mejoras de convergencia frente a Monte Carlo.
- **Uso en el Motor:** MC-B08: cuasi-Monte Carlo para acelerar la propagación de incertidumbre en DCF y modelos de dimensionado de mercado.
- **Limitaciones:** Alerta: REPARAR (DOI/URL editorial no vistos). La página índice escribe el tercer autor como «Tang, K. S.».
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02. Reutilizada en F8 del Bloque B V2.0 (TMB-08) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### MBM-0202 · Q 87 (A) — Global Sensitivity Analysis: The Primer

- **Autores:** Andrea Saltelli; Marco Ratto; Terry Andres; Francesca Campolongo; Jessica Cariboni; Debora Gatelli; Michaela Saisana; Stefano Tarantola
- **Año:** 2008
- **Publicación o institución:** John Wiley & Sons (304 págs.; publicado en diciembre de 2007)
- **Tipo de documento:** Libro académico (manual)
- **Temática:** TMB-08 Simulación Monte Carlo, escenarios y sensibilidad (principal) · secundarias: TMB-07
- **Calidad Q:** 87 (A) — Tipo 21/25 · Rigor 19/20 · Autoridad 14/15 · Vigencia 8/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.1002/9780470725184 · ISBN: 978-0-470-05997-5 · https://en.wikipedia.org/wiki/Global_Sensitivity_Analysis._The_Primer
- **Acceso y licencia:** De pago (Wiley)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «variance-based sensitivity analysis Sobol indices Saltelli Global Sensitivity Analysis The Primer wikipedia»; WebFetch: sí, página de Wikipedia del libro (ISBN, DOI y reseñas))
- **Contenido:** Manual de referencia del análisis de sensibilidad global: diseño de experimentos, cribado de Morris, índices de Sobol, FAST y análisis de incertidumbre con ejemplos.
- **Uso en el Motor:** MC-B08: protocolo completo de sensibilidad (cribado + índices de varianza) para los modelos de valoración y de escenarios del Bloque B; base del diagrama tornado y de Sobol que reporta el Motor.
- **Limitaciones:** Ejemplos de ingeniería y medio ambiente; no trata casos financieros.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### MBM-0208 · Q 87 (A) — A Distribution-Free Approach to Inducing Rank Correlation Among Input Variables

- **Autores:** Ronald L. Iman; W. J. Conover
- **Año:** 1982
- **Publicación o institución:** Communications in Statistics: Simulation and Computation, vol. 11, n.º 3, págs. 311-334
- **Tipo de documento:** Artículo revisado por pares (fundacional)
- **Temática:** TMB-08 Simulación Monte Carlo, escenarios y sensibilidad (principal) · secundarias: TMB-09
- **Calidad Q:** 87 (A) — Tipo 24/25 · Rigor 18/20 · Autoridad 13/15 · Vigencia 8/10 · Impacto 10/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** DOI: 10.1080/03610918208812265 · https://ftp.math.utah.edu/pub/tex/bib/idx/communstatsimulcomput1980/11/3/311-334.html
- **Acceso y licencia:** De pago (Taylor & Francis)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Iman Conover 1982 "distribution-free approach to inducing rank correlation among input variables" McKay Beckman Conover Latin hypercube»; WebFetch: sí, ficha bibliográfica de la Universidad de Utah)
- **Contenido:** Método de reordenación que induce una correlación de rangos deseada entre entradas simuladas sin alterar sus distribuciones marginales.
- **Uso en el Motor:** MC-B08 y MC-B09: simular supuestos correlacionados (demanda y precio, coste de insumo y margen) respetando sus marginales empíricas.
- **Limitaciones:** Controla correlación de rangos, no la dependencia de cola.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### ANA-DOC-0531 · Q 86 (A) — NGFS Climate Scenarios Technical Documentation, V5.0 (Phase V)

- **Autores:** Network for Greening the Financial System (NGFS), Workstream on Scenario Design and Analysis; consorcio PIK, IIASA, Universidad de Maryland, Climate Analytics, ETH Zúrich y NIESR
- **Año:** 2024 (noviembre; documento publicado en enero de 2025)
- **Publicación o institución:** NGFS (red de bancos centrales y supervisores)
- **Tipo de documento:** Documentación técnica de escenarios oficiales
- **Temática:** TMB-08 Simulación Monte Carlo, escenarios y sensibilidad (principal) · secundarias: TMB-09
- **Calidad Q:** 86 (A) — Tipo 23/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 6/10 · Impacto 10/10 · Independencia 7/10 · Acceso 9/10
- **DOI / URL:** URL de acceso: https://www.ngfs.net/system/files/2025-01/NGFS%20Climate%20Scenarios%20Technical%20Documentation.pdf · Aviso a usuarios: https://www.ngfs.net/en/publications-and-statistics/publications/ngfs-climate-scenarios-central-banks-and-supervisors-phase-v
- **Acceso y licencia:** Peldaño 1 (descarga libre)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «NGFS long-term climate scenarios technical documentation 2024 phase V»; WebFetch: sí, PDF y página de aviso)
- **Contenido:** Siete escenarios (ordenados, desordenados, «hot house world», «too little, too late») con modelos REMIND-MAgPIE, MESSAGEix-GLOBIOM, GCAM, NiGEM y MAGICC; documenta supuestos, variables y función de daños.
- **Uso en el Motor:** MC-B08 y AG-B11: escenarios climáticos de referencia (variables macro, carbono, energía) para alimentar simulaciones sectoriales de transición; AG-B13 Prospectiva.
- **Limitaciones:** **Aviso NGFS**: el artículo de Kotz et al. (2024), base de la función de daños físicos, fue retractado por Nature; quedan afectadas las salidas «Integrated Physical Damages», las físicas y combinadas de NiGEM y las de PIB «Kotz-Wenz». Usar solo las variables de transición o con advertencia.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-08) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### MBM-0204 · Q 86 (A) — How to Avoid a Perfunctory Sensitivity Analysis

- **Autores:** Andrea Saltelli; Paola Annoni
- **Año:** 2010
- **Publicación o institución:** Environmental Modelling & Software, vol. 25, págs. 1508-1517
- **Tipo de documento:** Artículo revisado por pares (metodológico)
- **Temática:** TMB-08 Simulación Monte Carlo, escenarios y sensibilidad (principal) · secundarias: TMB-14
- **Calidad Q:** 86 (A) — Tipo 24/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 8/10 · Impacto 9/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** Página índice: https://en.wikipedia.org/wiki/Variance-based_sensitivity_analysis (DOI no visto)
- **Acceso y licencia:** De pago (Elsevier)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «variance-based sensitivity analysis Sobol indices Saltelli Global Sensitivity Analysis The Primer wikipedia»; WebFetch: sí, página índice de Wikipedia «Variance-based sensitivity analysis»)
- **Contenido:** Muestra que el análisis «uno a uno» (OAT) explora una fracción mínima del espacio de entradas y propone alternativas globales.
- **Uso en el Motor:** MC-B08 y Auditor: regla para no aceptar como análisis de sensibilidad un tornado OAT aislado; exigir complemento global cuando haya interacciones.
- **Limitaciones:** Ejemplos fuera de finanzas.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### MBM-0217 · Q 86 (A) — A New Uncertainty Importance Measure

- **Autores:** Emanuele Borgonovo
- **Año:** 2007
- **Publicación o institución:** Reliability Engineering & System Safety, vol. 92
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-08 Simulación Monte Carlo, escenarios y sensibilidad (principal) · secundarias: TMB-09
- **Calidad Q:** 86 (A) — Tipo 24/25 · Rigor 18/20 · Autoridad 13/15 · Vigencia 8/10 · Impacto 9/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** PII S0951832006000883 · Página índice: https://pypi.org/project/SALib/
- **Acceso y licencia:** De pago (Elsevier)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «SALib "An open-source Python library for Sensitivity Analysis" Herman Usher Journal of Open Source Software Morris elementary effects»; WebFetch: sí, página de SALib en PyPI (cita «Borgonovo 2007»; título según la obra citada))
- **Contenido:** Medida de importancia delta independiente de momentos: mide cuánto cambia toda la distribución de la salida al fijar una entrada.
- **Uso en el Motor:** MC-B08 y MC-B09: sensibilidad cuando importa la cola (pérdidas) y no solo la varianza del valor.
- **Limitaciones:** Estimación más costosa que Sobol.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### MBM-0207 · Q 85 (A) — An Annotated Timeline of Sensitivity Analysis

- **Autores:** Stefano Tarantola; Federico Ferretti; Samuele Lo Piano; Mariia Kozlova; Alessio Lachi; Rossana Rosati; Arnald Puy; Pamphile Roy; Giulia Vannucci; Marta Kuc-Czarnecka; Andrea Saltelli
- **Año:** 2024
- **Publicación o institución:** Environmental Modelling & Software, vol. 174, art. 105977
- **Tipo de documento:** Artículo de revisión revisado por pares
- **Temática:** TMB-08 Simulación Monte Carlo, escenarios y sensibilidad (principal) · secundarias: TMB-14
- **Calidad Q:** 85 (A) — Tipo 24/25 · Rigor 16/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 6/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1016/j.envsoft.2024.105977 · Página índice: https://en.wikipedia.org/wiki/Global_Sensitivity_Analysis._The_Primer
- **Acceso y licencia:** Revista Elsevier (acceso no comprobado)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «variance-based sensitivity analysis Sobol indices Saltelli Global Sensitivity Analysis The Primer wikipedia»; WebFetch: sí, página índice de Wikipedia «Global Sensitivity Analysis. The Primer»)
- **Contenido:** Cronología comentada de los métodos de análisis de sensibilidad, de los diseños factoriales a los índices de Sobol, Shapley y métodos sin momentos.
- **Uso en el Motor:** MC-B08 y DOC-M: mapa actualizado de métodos para elegir y justificar la técnica de sensibilidad.
- **Limitaciones:** Revisión histórica; no compara rendimiento de métodos.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### MBM-0206 · Q 85 (A) — Importance Measures in Global Sensitivity Analysis of Nonlinear Models

- **Autores:** Toshimitsu Homma; Andrea Saltelli
- **Año:** 1996
- **Publicación o institución:** Reliability Engineering and System Safety, vol. 52, págs. 1-17
- **Tipo de documento:** Artículo revisado por pares (fundacional)
- **Temática:** TMB-08 Simulación Monte Carlo, escenarios y sensibilidad (principal) · secundarias: —
- **Calidad Q:** 85 (A) — Tipo 24/25 · Rigor 18/20 · Autoridad 13/15 · Vigencia 7/10 · Impacto 9/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** Página índice: https://en.wikipedia.org/wiki/Variance-based_sensitivity_analysis (DOI no visto)
- **Acceso y licencia:** De pago (Elsevier)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «variance-based sensitivity analysis Sobol indices Saltelli Global Sensitivity Analysis The Primer wikipedia»; WebFetch: sí, página índice de Wikipedia «Variance-based sensitivity analysis»)
- **Contenido:** Introduce el índice de efecto total, que capta la contribución de una entrada incluidas sus interacciones.
- **Uso en el Motor:** MC-B08: distinguir supuestos con efecto propio de los que actúan por interacción (p. ej., precio × volumen).
- **Limitaciones:** Texto técnico; estimadores mejorados después (Saltelli et al., 2010).
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### MBM-0214 · Q 85 (A) — Factorial Sampling Plans for Preliminary Computational Experiments

- **Autores:** Max D. Morris
- **Año:** 1991
- **Publicación o institución:** Technometrics, vol. 33
- **Tipo de documento:** Artículo revisado por pares (fundacional)
- **Temática:** TMB-08 Simulación Monte Carlo, escenarios y sensibilidad (principal) · secundarias: —
- **Calidad Q:** 85 (A) — Tipo 24/25 · Rigor 17/20 · Autoridad 13/15 · Vigencia 7/10 · Impacto 10/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** DOI: 10.1080/00401706.1991.10484804 · Página índice: https://pypi.org/project/SALib/
- **Acceso y licencia:** De pago (Taylor & Francis)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «SALib "An open-source Python library for Sensitivity Analysis" Herman Usher Journal of Open Source Software Morris elementary effects»; WebFetch: sí, página de SALib en PyPI (cita «Morris 1991» con DOI; título según la obra citada))
- **Contenido:** Método de los efectos elementales para cribar qué entradas tienen efectos despreciables, lineales o no lineales/interactivos con pocas evaluaciones.
- **Uso en el Motor:** MC-B08: cribado inicial de decenas de supuestos de un modelo sectorial antes de calcular índices de Sobol.
- **Limitaciones:** Medida cualitativa; no cuantifica la varianza explicada.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### MBM-0213 · Q 84 (A) — Toward SALib 2.0: Advancing the Accessibility and Interpretability of Global Sensitivity Analyses

- **Autores:** Takuya Iwanaga; William Usher; Jonathan Herman
- **Año:** 2022
- **Publicación o institución:** Socio-Environmental Systems Modelling, vol. 4, art. 18155
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-08 Simulación Monte Carlo, escenarios y sensibilidad (principal) · secundarias: —
- **Calidad Q:** 84 (A) — Tipo 22/25 · Rigor 15/20 · Autoridad 11/15 · Vigencia 10/10 · Impacto 6/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** DOI: 10.18174/sesmo.18155 · Página índice: https://pypi.org/project/SALib/
- **Acceso y licencia:** Acceso abierto
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «SALib "An open-source Python library for Sensitivity Analysis" Herman Usher Journal of Open Source Software Morris elementary effects»; WebFetch: sí, página de SALib en PyPI (cita recomendada))
- **Contenido:** Describe la versión 2 de SALib, su interfaz simplificada y recomendaciones para interpretar resultados de sensibilidad global.
- **Uso en el Motor:** MC-B08: guía de uso actual de SALib e interpretación de índices para los informes del Motor.
- **Limitaciones:** Centrado en la herramienta.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### MBM-0212 · Q 84 (A) — SALib: An Open-Source Python Library for Sensitivity Analysis

- **Autores:** Jon Herman; Will Usher
- **Año:** 2017
- **Publicación o institución:** Journal of Open Source Software, vol. 2, n.º 9
- **Tipo de documento:** Artículo de software revisado por pares
- **Temática:** TMB-08 Simulación Monte Carlo, escenarios y sensibilidad (principal) · secundarias: TMB-14
- **Calidad Q:** 84 (A) — Tipo 20/25 · Rigor 16/20 · Autoridad 11/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** DOI: 10.21105/joss.00097 · https://joss.theoj.org/papers/10.21105/joss.00097 · https://pypi.org/project/SALib/
- **Acceso y licencia:** Acceso abierto; software libre
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «SALib "An open-source Python library for Sensitivity Analysis" Herman Usher Journal of Open Source Software Morris elementary effects»; WebFetch: sí, página de SALib en PyPI (versión 1.6.0 y citas de cada método))
- **Contenido:** Biblioteca Python que implementa Sobol, Morris, FAST, delta, DGSM, PAWN y otros métodos con citas a su fuente.
- **Uso en el Motor:** MC-B08: herramienta de implementación de los análisis de sensibilidad del Motor; registrar versión y método en el artefacto (TMB-14).
- **Limitaciones:** Documentación técnica; no valida los modelos del usuario.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### MBM-0215 · Q 84 (A) — An Effective Screening Design for Sensitivity Analysis of Large Models

- **Autores:** Francesca Campolongo; Jessica Cariboni; Andrea Saltelli
- **Año:** 2007
- **Publicación o institución:** Environmental Modelling & Software, vol. 22
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-08 Simulación Monte Carlo, escenarios y sensibilidad (principal) · secundarias: —
- **Calidad Q:** 84 (A) — Tipo 24/25 · Rigor 16/20 · Autoridad 13/15 · Vigencia 8/10 · Impacto 9/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** DOI: 10.1016/j.envsoft.2006.10.004 · Página índice: https://pypi.org/project/SALib/
- **Acceso y licencia:** De pago (Elsevier)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «SALib "An open-source Python library for Sensitivity Analysis" Herman Usher Journal of Open Source Software Morris elementary effects»; WebFetch: sí, página de SALib en PyPI (cita «Campolongo et al. 2007» con DOI; título según la obra citada))
- **Contenido:** Mejora el método de Morris con la medida μ* y una estrategia de trayectorias más eficiente.
- **Uso en el Motor:** MC-B08: versión recomendada del cribado de Morris en el Motor.
- **Limitaciones:** Mismos límites cualitativos que Morris.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### MBM-0203 · Q 82 (A) — Sensitivity Analysis in Practice: A Guide to Assessing Scientific Models

- **Autores:** Andrea Saltelli; Stefano Tarantola; Francesca Campolongo; Marco Ratto
- **Año:** 2004
- **Publicación o institución:** John Wiley & Sons
- **Tipo de documento:** Libro académico (guía práctica)
- **Temática:** TMB-08 Simulación Monte Carlo, escenarios y sensibilidad (principal) · secundarias: —
- **Calidad Q:** 82 (A) — Tipo 20/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 7/10 · Impacto 9/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.1002/0470870958 · ISBN: 0-470-87093-1 · Página índice: https://en.wikipedia.org/wiki/Global_Sensitivity_Analysis._The_Primer
- **Acceso y licencia:** De pago (Wiley)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «variance-based sensitivity analysis Sobol indices Saltelli Global Sensitivity Analysis The Primer wikipedia»; WebFetch: sí, página índice de Wikipedia «Global Sensitivity Analysis. The Primer» (cita con DOI e ISBN y reseñas en JASA y JRSS-A))
- **Contenido:** Guía aplicada para elegir y ejecutar métodos de sensibilidad (cribado, regresión, varianza) con el programa SIMLAB.
- **Uso en el Motor:** MC-B08: elegir el método de sensibilidad según el coste del modelo y el número de supuestos.
- **Limitaciones:** Software SIMLAB desfasado; superada en parte por el Primer de 2008.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### DOC-MOT-0383 · Q 81 (A) — Construction and Comparison of High-Dimensional Sobol' Generators

- **Autores:** Ilya Sobol'; Danil Asotsky; Alexander Kreinin; Sergei Kucherenko
- **Año:** 2011
- **Publicación o institución:** Wilmott Journal, n.º 56, págs. 64-79
- **Tipo de documento:** Artículo en revista profesional
- **Temática:** TMB-08 Simulación Monte Carlo, escenarios y sensibilidad (principal) · secundarias: —
- **Calidad Q:** 81 (A) — Tipo 15/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 8/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI: 10.1002/wilm.10056 · PDF: http://www.broda.co.uk/doc/HD_SobolGenerator.pdf
- **Acceso y licencia:** Copia gratuita (BRODA)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Monte Carlo methods in finance Sobol sequence multilevel Monte Carlo Mersenne Twister Euler–Maruyama (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Sobol sequence», que reproduce la cita completa)
- **Contenido:** Construcción y comparación de generadores Sobol' de alta dimensión (hasta decenas de miles de dimensiones) con propiedades A y A'.
- **Uso en el Motor:** MC-B08: generadores Sobol' de alta dimensión para diseños de escenarios con muchos supuestos y para estimar índices de Sobol.
- **Limitaciones:** Coautores vinculados a proveedor comercial (BRODA).
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02. Reutilizada en F8 del Bloque B V2.0 (TMB-08) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0382 · Q 81 (A) — Monte Carlo Methods in Finance

- **Autores:** Peter Jäckel
- **Año:** 2002
- **Publicación o institución:** John Wiley & Sons
- **Tipo de documento:** Libro académico-profesional
- **Temática:** TMB-08 Simulación Monte Carlo, escenarios y sensibilidad (principal) · secundarias: —
- **Calidad Q:** 81 (A) — Tipo 18/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** ISBN: 0-471-49741-X · Cita en https://en.wikipedia.org/wiki/Sobol_sequence
- **Acceso y licencia:** De pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Monte Carlo methods in finance Sobol sequence multilevel Monte Carlo Mersenne Twister Euler–Maruyama (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Sobol sequence», que reproduce la cita completa y «Quasi-Monte Carlo methods in finance»)
- **Contenido:** Monte Carlo práctico: generadores, Sobol' con inicialización, puentes brownianos, reducción de varianza y griegas.
- **Uso en el Motor:** MC-B08: implementación práctica de Monte Carlo en producción (generadores, Sobol', reducción de varianza) para las simulaciones del Motor de Mercados.
- **Limitaciones:** Orientado a practicantes.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02. Reutilizada en F8 del Bloque B V2.0 (TMB-08) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### ANA-DOC-0535 · Q 79 (B) — Guide to Climate Scenario Analysis for Central Banks and Supervisors (Update)

- **Autores:** Network for Greening the Financial System (NGFS)
- **Año:** 2025 (noviembre)
- **Publicación o institución:** NGFS
- **Tipo de documento:** Guía técnica institucional
- **Temática:** TMB-08 Simulación Monte Carlo, escenarios y sensibilidad (principal) · secundarias: TMB-09
- **Calidad Q:** 79 (B) — Tipo 15/25 · Rigor 14/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 8/10 · Acceso 9/10
- **DOI / URL:** URL de acceso: https://www.ngfs.net/system/files/2025-11/Guide%20to%20climate%20scenario%20analysis%20for%20central%20banks%20and%20supervisors%20%E2%80%93%20Update.pdf
- **Acceso y licencia:** Peldaño 1 (descarga libre)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «NGFS long-term climate scenarios technical documentation 2024 phase V»; WebFetch: sí)
- **Contenido:** Proceso en cuatro pasos para el análisis de escenarios climáticos (objetivos, elección de escenarios, impacto económico-financiero, comunicación) con los escenarios NGFS de corto y largo plazo; advierte de la crítica a las estimaciones de riesgo físico de la fase V.
- **Uso en el Motor:** MC-B08 y AG-B13: guía para diseñar análisis de escenarios (narrativa, horizonte, variables) y traducirlos a impactos sectoriales.
- **Limitaciones:** Orientada a supervisores; no aporta resultados cuantitativos propios.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-08) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### MBM-0210 · Q 77 (B) — Risk Aggregation with Empirical Margins: Latin Hypercubes, Empirical Copulas, and Convergence of Sum Distributions

- **Autores:** Georg Mainik
- **Año:** 2015
- **Publicación o institución:** arXiv:1508.02749 (RiskLab, ETH Zúrich)
- **Tipo de documento:** Documento de trabajo (preprint)
- **Temática:** TMB-08 Simulación Monte Carlo, escenarios y sensibilidad (principal) · secundarias: TMB-09
- **Calidad Q:** 77 (B) — Tipo 15/25 · Rigor 16/20 · Autoridad 12/15 · Vigencia 9/10 · Impacto 5/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://arxiv.org/pdf/1508.02749
- **Acceso y licencia:** Acceso abierto (arXiv)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Iman Conover 1982 "distribution-free approach to inducing rank correlation among input variables" McKay Beckman Conover Latin hypercube»; WebFetch: sí, PDF en arXiv)
- **Contenido:** Estudia la agregación de riesgos con marginales empíricas mediante hipercubos latinos con dependencia (reordenación tipo Iman-Conover) y cópulas empíricas, con resultados de convergencia.
- **Uso en el Motor:** MC-B08 y MC-B09: agregar pérdidas de varios sectores o insumos con dependencia empírica en simulaciones de estrés.
- **Limitaciones:** Preprint; venue de publicación no confirmado.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### MBM-0211 · Q 76 (B) — Scenario Planning: A Tool for Strategic Thinking

- **Autores:** Paul J. H. Schoemaker
- **Año:** 1995
- **Publicación o institución:** MIT Sloan Management Review (invierno de 1995)
- **Tipo de documento:** Artículo de revista de gestión (revisión editorial)
- **Temática:** TMB-08 Simulación Monte Carlo, escenarios y sensibilidad (principal) · secundarias: TMB-13
- **Calidad Q:** 76 (B) — Tipo 16/25 · Rigor 13/20 · Autoridad 14/15 · Vigencia 6/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** https://sloanreview.mit.edu/article/scenario-planning-a-tool-for-strategic-thinking/amp
- **Acceso y licencia:** Página del editor (texto completo con suscripción)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Schoemaker 1995 "Scenario Planning: A Tool for Strategic Thinking" Sloan Management Review Wack 1985 "Scenarios: Uncharted Waters Ahead"»; WebFetch: sí, página de MIT Sloan Management Review)
- **Contenido:** Método de planificación por escenarios: identificar fuerzas motrices e incertidumbres clave y construir varias narrativas plausibles para contrarrestar sesgos como el exceso de confianza.
- **Uso en el Motor:** AG-B13 Prospectiva y MC-B08: construir los escenarios narrativos (base, alcista, bajista, ruptura) que el Motor cuantifica.
- **Limitaciones:** Método cualitativo; la cuantificación la aporta MC-B08.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

## TMB-09 Riesgo: volatilidad, correlaciones, colas y estrés sectorial

#### DOC-MOT-0350 · Q 97 (A) — On the Coherence of Expected Shortfall

- **Autores:** Carlo Acerbi; Dirk Tasche
- **Año:** 2002
- **Publicación o institución:** Journal of Banking & Finance, vol. 26, n.º 7, págs. 1487-1503
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-09 Riesgo: volatilidad, correlaciones, colas y estrés sectorial (principal) · secundarias: —
- **Calidad Q:** 97 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** DOI: 10.1016/S0378-4266(02)00283-2 · arXiv: https://arxiv.org/abs/cond-mat/0104295
- **Acceso y licencia:** Preprint gratuito en arXiv; revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «expected shortfall coherent risk measure value at risk backtesting extreme value theory (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Expected shortfall», que reproduce la cita completa)
- **Contenido:** Define el ES de forma que sea coherente para cualquier distribución (incluidas discretas) y lo relaciona con el CVaR.
- **Uso en el Motor:** MC-B09: justifica el uso de Expected Shortfall como medida de cola en el estrés de sectores y cestas de candidatos.
- **Limitaciones:** Teórico.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02. Reutilizada en F8 del Bloque B V2.0 (TMB-09) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0074 · Q 96 (A) — Estimation of Tail-Related Risk Measures for Heteroscedastic Financial Time Series: An Extreme Value Approach

- **Autores:** Alexander J. McNeil; Rüdiger Frey
- **Año:** 2000
- **Publicación o institución:** Journal of Empirical Finance, vol. 7, n.º 3-4, págs. 271-300
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-09 Riesgo: volatilidad, correlaciones, colas y estrés sectorial (principal) · secundarias: TMB-01
- **Calidad Q:** 96 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI: 10.1016/S0927-5398(00)00012-8 · https://research.wu.ac.at/de/publications/estimation-of-tail-related-risk-measures-for-heteroscedastic-fina-3/ · PDF: https://www.wu.ac.at/fileadmin/wu/d/i/statmath/Publications/Publications_Frey/Journal_Papers/evt-garch.pdf
- **Acceso y licencia:** Copia institucional gratuita (WU Viena); revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «McNeil Frey 2000 "Estimation of tail-related risk measures for heteroscedastic financial time series" Journal of Empirical Finance»; WebFetch: sí, portal de investigación de la WU)
- **Contenido:** Método en dos etapas: GARCH por pseudo-máxima verosimilitud y teoría de valores extremos (GPD) sobre los residuos para VaR y ES condicionales.
- **Uso en el Motor:** MC-B09: VaR/ES condicional con GARCH+EVT para colas de índices sectoriales y de candidatos.
- **Limitaciones:** Supone residuos i.i.d.; umbral de la GPD a elegir.
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (tanda 2). Reutilizada en F8 del Bloque B V2.0 (TMB-09) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0075 · Q 96 (A) — Coherent Measures of Risk

- **Autores:** Philippe Artzner; Freddy Delbaen; Jean-Marc Eber; David Heath
- **Año:** 1999
- **Publicación o institución:** Mathematical Finance, vol. 9, n.º 3, págs. 203-228
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-09 Riesgo: volatilidad, correlaciones, colas y estrés sectorial (principal) · secundarias: —
- **Calidad Q:** 96 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI: 10.1111/1467-9965.00068 · https://onlinelibrary.wiley.com/doi/10.1111/1467-9965.00068 · Preprint: http://www.math.ethz.ch/~delbaen/ftp/preprints/CoherentMF.pdf
- **Acceso y licencia:** Preprint gratuito (ETH Zúrich); revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «expected shortfall coherent risk measure value at risk backtesting extreme value theory (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Expected shortfall», que reproduce la cita completa, «Value at risk» y «Coherent risk measure»)
- **Contenido:** Axiomas de coherencia (monotonía, subaditividad, homogeneidad, invariancia por traslación); el VaR no es subaditivo en general.
- **Uso en el Motor:** MC-B09: axiomas de medidas de riesgo coherentes; criterio para elegir la medida de riesgo sectorial que reporta el Motor.
- **Limitaciones:** Teoría estática; no trata elicitabilidad ni dinámica.
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (tanda 2). Reutilizada en F8 del Bloque B V2.0 (TMB-09) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0354 · Q 95 (A) — Explanatory Note on the Minimum Capital Requirements for Market Risk

- **Autores:** Basel Committee on Banking Supervision
- **Año:** 2019
- **Publicación o institución:** Bank for International Settlements (enero de 2019)
- **Tipo de documento:** Informe técnico con metodología (organismo oficial)
- **Temática:** TMB-09 Riesgo: volatilidad, correlaciones, colas y estrés sectorial (principal) · secundarias: —
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://www.bis.org/bcbs/publ/d457_note.pdf
- **Acceso y licencia:** Acceso gratuito (BPI)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «expected shortfall coherent risk measure value at risk backtesting extreme value theory (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Value at risk», que reproduce la cita completa)
- **Contenido:** Explica el marco revisado de riesgo de mercado (FRTB): sustitución del VaR por ES al 97,5 %, horizontes de liquidez y pruebas de backtesting y atribución de P&L.
- **Uso en el Motor:** MC-B09: referencia regulatoria de ES 97,5 % y horizontes de liquidez para calibrar el estrés de cestas sectoriales.
- **Limitaciones:** Marco regulatorio bancario; no es metodología estadística general.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02. Reutilizada en F8 del Bloque B V2.0 (TMB-09) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0364 · Q 95 (A) — Convex Measures of Risk and Trading Constraints

- **Autores:** Hans Föllmer; Alexander Schied
- **Año:** 2002
- **Publicación o institución:** Finance and Stochastics, vol. 6, n.º 4, págs. 429-447
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-09 Riesgo: volatilidad, correlaciones, colas y estrés sectorial (principal) · secundarias: —
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI: 10.1007/s007800200072 · Copia abierta: http://edoc.hu-berlin.de/18452/4274
- **Acceso y licencia:** Copia gratuita (HU Berlín); revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «expected shortfall coherent risk measure value at risk backtesting extreme value theory (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Coherent risk measure», que reproduce la cita completa)
- **Contenido:** Generaliza las medidas coherentes a medidas convexas de riesgo y su representación dual.
- **Uso en el Motor:** MC-B09: medidas de riesgo convexas como generalización cuando hay restricciones de liquidez o de posición en la selección.
- **Limitaciones:** Teórico.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02. Reutilizada en F8 del Bloque B V2.0 (TMB-09) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0210 · Q 95 (A) — Measuring and Testing the Impact of News on Volatility

- **Autores:** Robert F. Engle; Victor K. Ng
- **Año:** 1993
- **Publicación o institución:** The Journal of Finance, 48(5), 1749-1778
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-09 Riesgo: volatilidad, correlaciones, colas y estrés sectorial (principal) · secundarias: TMB-01
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1111/j.1540-6261.1993.tb05127.x · Verificada en página índice: https://en.wikipedia.org/wiki/Autoregressive_conditional_heteroskedasticity (SSRN 262096)
- **Acceso y licencia:** Revista por suscripción; versión en SSRN
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Autoregressive conditional heteroskedasticity wikipedia GARCH EGARCH GJR references»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Autoregressive_conditional_heteroskedasticity)
- **Contenido:** Introduce la curva de impacto de noticias y los contrastes de sesgo de signo y de tamaño para diagnosticar asimetrías no recogidas por un GARCH.
- **Uso en el Motor:** MC-B09: asimetría de la volatilidad ante noticias negativas (curva de impacto de noticias) en sectores cíclicos.
- **Limitaciones:** Confirmada solo mediante página índice (bibliografía de Wikipedia «Autoregressive conditional heteroskedasticity»); pendiente de lectura de la fuente primaria.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-09) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0033 · Q 95 (A) — Generalized Autoregressive Conditional Heteroskedasticity

- **Autores:** Tim Bollerslev
- **Año:** 1986
- **Publicación o institución:** Journal of Econometrics, 31(3), 307-327
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-09 Riesgo: volatilidad, correlaciones, colas y estrés sectorial (principal) · secundarias: TMB-01
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1016/0304-4076(86)90063-1 · Verificada en página índice: https://en.wikipedia.org/wiki/Autoregressive_conditional_heteroskedasticity
- **Acceso y licencia:** Revista Elsevier por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Autoregressive conditional heteroskedasticity wikipedia GARCH EGARCH GJR references»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Autoregressive_conditional_heteroskedasticity)
- **Contenido:** Generaliza ARCH a GARCH(p,q): la varianza condicional depende de los cuadrados de los errores pasados y de sus propias varianzas pasadas; GARCH(1,1) es el estándar práctico.
- **Uso en el Motor:** MC-B09 y MC-B01: modelo GARCH de referencia para la volatilidad condicional de índices sectoriales.
- **Limitaciones:** Respuesta simétrica a choques (usar GJR/EGARCH ante apalancamiento). Confirmada solo mediante página índice (bibliografía de Wikipedia «Autoregressive conditional heteroskedasticity»); pendiente de lectura de la fuente primaria.
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02 (DOI confirmado en índice). Reutilizada en F8 del Bloque B V2.0 (TMB-09) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0356 · Q 94 (A) — CoVaR

- **Autores:** Tobias Adrian; Markus K. Brunnermeier
- **Año:** 2016
- **Publicación o institución:** American Economic Review, vol. 106, n.º 7, págs. 1705-1741
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-09 Riesgo: volatilidad, correlaciones, colas y estrés sectorial (principal) · secundarias: TMB-10
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1257/aer.20120555 · https://doi.org/10.1257/aer.20120555
- **Acceso y licencia:** Texto completo por suscripción en la editorial (AEA)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «generalized Pareto distribution extreme value theory Hill estimator copula CoVaR systemic risk (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Markus Brunnermeier»)
- **Contenido:** Mide el riesgo sistémico como el VaR del sistema condicionado a que una institución esté en dificultades (ΔCoVaR), estimado por regresión cuantílica.
- **Uso en el Motor:** MC-B09: riesgo de contagio entre sectores y entidades (CoVaR) para medir cuánto añade un sector al riesgo del conjunto; AG-B11.
- **Limitaciones:** Requiere datos de mercado de las entidades.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02. Reutilizada en F8 del Bloque B V2.0 (TMB-09) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0365 · Q 94 (A) — Asset Market Linkages in Crisis Periods

- **Autores:** Philipp Hartmann; Stefan Straetmans; Casper G. de Vries
- **Año:** 2004
- **Publicación o institución:** Review of Economics and Statistics, vol. 86, n.º 1, págs. 313-326
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-09 Riesgo: volatilidad, correlaciones, colas y estrés sectorial (principal) · secundarias: TMB-10
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI: 10.1162/003465304323023831 · Repositorio: http://repository.tue.nl/548705 · https://hdl.handle.net/10419%2F152505
- **Acceso y licencia:** Copias gratuitas (TU Eindhoven, EconStor); revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «generalized Pareto distribution extreme value theory Hill estimator copula CoVaR systemic risk (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Tail dependence», que reproduce la cita completa)
- **Contenido:** Mide la dependencia de colas entre acciones y bonos del G-5 con EVT multivariante: contagio y huida hacia la calidad.
- **Uso en el Motor:** MC-B09: dependencia de cola entre mercados y sectores en crisis; diagnóstico de contagio para AG-B11 y AG-B14.
- **Limitaciones:** Muestra hasta finales de los 90.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02. Reutilizada en F8 del Bloque B V2.0 (TMB-09) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0214 · Q 94 (A) — Dynamic Conditional Correlation: A Simple Class of Multivariate Generalized Autoregressive Conditional Heteroskedasticity Models

- **Autores:** Robert F. Engle
- **Año:** 2002
- **Publicación o institución:** Journal of Business & Economic Statistics, 20(3), 339-350
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-09 Riesgo: volatilidad, correlaciones, colas y estrés sectorial (principal) · secundarias: TMB-01
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** https://ideas.repec.org/a/bes/jnlbes/v20y2002i3p339-50.html · versión de trabajo NYU: https://archive.nyu.edu/handle/2451/26879
- **Acceso y licencia:** Ficha RePEc abierta; texto de revista por suscripción; versión de trabajo en el repositorio de NYU
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Engle 2002 Dynamic Conditional Correlation Journal of Business Economic Statistics multivariate GARCH»; WebFetch: sí)
- **Contenido:** Modelo DCC: GARCH univariantes para cada activo y una dinámica GARCH escalar para la matriz de correlaciones de los residuos estandarizados, estimable en dos etapas.
- **Uso en el Motor:** MC-B09: correlaciones dinámicas (DCC) entre sectores y entre candidatos; detecta aumentos de correlación en estrés.
- **Limitaciones:** Dinámica común a todas las correlaciones; sesgo en dimensiones grandes.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-09) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0073 · Q 94 (A) — Evaluating Interval Forecasts

- **Autores:** Peter F. Christoffersen
- **Año:** 1998
- **Publicación o institución:** International Economic Review, vol. 39, n.º 4, págs. 841-862
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-09 Riesgo: volatilidad, correlaciones, colas y estrés sectorial (principal) · secundarias: TMB-11
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.2307/2527341 · JSTOR: 2527341
- **Acceso y licencia:** Texto completo por suscripción en la editorial (Wiley/JSTOR)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «expected shortfall coherent risk measure value at risk backtesting extreme value theory (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Value at risk», que reproduce la cita completa)
- **Contenido:** Contrastes de razón de verosimilitud de cobertura incondicional, independencia y cobertura condicional de las excepciones de intervalos/VaR.
- **Uso en el Motor:** MC-B09 y MC-B10: pruebas de cobertura y de independencia de los intervalos de riesgo que publica el Motor.
- **Limitaciones:** Baja potencia con pocas excepciones.
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (tanda 2). Reutilizada en F8 del Bloque B V2.0 (TMB-09) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### MBM-0218 · Q 93 (A) — On the Network Topology of Variance Decompositions: Measuring the Connectedness of Financial Firms

- **Autores:** Francis X. Diebold; Kamil Yılmaz
- **Año:** 2014
- **Publicación o institución:** Journal of Econometrics, vol. 182, n.º 1, págs. 119-134 (reimpreso en vol. 234, 2023, págs. 70-90)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-09 Riesgo: volatilidad, correlaciones, colas y estrés sectorial (principal) · secundarias: TMB-10
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1016/j.jeconom.2014.04.012 · https://research.hub.ku.edu.tr/entities/publication/b39c5142-032a-4ac0-aec8-d8b42bb7317e/full · NBER WP 17490: https://www.nber.org/papers/w17490
- **Acceso y licencia:** Revista de pago; documento de trabajo NBER
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Diebold Yilmaz "On the network topology of variance decompositions: Measuring the connectedness of financial firms" Journal of Econometrics 2014 "Better to give than to receive"»; WebFetch: sí, repositorio de la Universidad Koç (registro con DOI y registro de la reimpresión de 2023))
- **Contenido:** Mide la conectividad entre activos como red dirigida a partir de descomposiciones de varianza de un VAR (índices de conectividad total, emitida y recibida).
- **Uso en el Motor:** MC-B09: red de transmisión de volatilidad entre sectores o candidatos; identificar emisores y receptores netos de shocks en el estrés sectorial (AG-B11, AG-B14).
- **Limitaciones:** Depende de la especificación del VAR y de la ventana; aplicado a entidades financieras.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### DOC-MOT-0353 · Q 93 (A) — Value-at-Risk Prediction: A Comparison of Alternative Strategies

- **Autores:** Keith Kuester; Stefan Mittnik; Marc S. Paolella
- **Año:** 2006
- **Publicación o institución:** Journal of Financial Econometrics, vol. 4, págs. 53-89
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-09 Riesgo: volatilidad, correlaciones, colas y estrés sectorial (principal) · secundarias: —
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1093/jjfinec/nbj002 · https://doi.org/10.1093%2Fjjfinec%2Fnbj002
- **Acceso y licencia:** Texto completo por suscripción en la editorial (OUP)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «expected shortfall coherent risk measure value at risk backtesting extreme value theory (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Value at risk», que reproduce la cita completa)
- **Contenido:** Compara fuera de muestra métodos de VaR (histórico, GARCH con distintas colas, EVT, CAViaR): destacan los híbridos GARCH-EVT y de colas asimétricas.
- **Uso en el Motor:** MC-B09: comparación empírica de métodos de VaR (histórico, GARCH, EVT) para elegir el método por tipo de serie sectorial.
- **Limitaciones:** Un solo índice (Nasdaq).
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02. Reutilizada en F8 del Bloque B V2.0 (TMB-09) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0352 · Q 93 (A) — Backtesting Value-at-Risk: A Duration-Based Approach

- **Autores:** Peter Christoffersen; Denis Pelletier
- **Año:** 2004
- **Publicación o institución:** Journal of Financial Econometrics, vol. 2, págs. 84-108
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-09 Riesgo: volatilidad, correlaciones, colas y estrés sectorial (principal) · secundarias: TMB-11
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1093/jjfinec/nbh004
- **Acceso y licencia:** Texto completo por suscripción en la editorial (OUP)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «expected shortfall coherent risk measure value at risk backtesting extreme value theory (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Value at risk», que reproduce la cita completa)
- **Contenido:** Contrastes de independencia de excepciones basados en la duración entre violaciones del VaR, más potentes ante agrupamientos.
- **Uso en el Motor:** MC-B09 y MC-B10: backtesting de VaR por duraciones entre excesos; detecta agrupamiento de pérdidas en series sectoriales.
- **Limitaciones:** Potencia limitada en muestras cortas.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02. Reutilizada en F8 del Bloque B V2.0 (TMB-09) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0351 · Q 93 (A) — Expected Shortfall: A Natural Coherent Alternative to Value at Risk

- **Autores:** Carlo Acerbi; Dirk Tasche
- **Año:** 2002
- **Publicación o institución:** Economic Notes, vol. 31, n.º 2, págs. 379-388
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-09 Riesgo: volatilidad, correlaciones, colas y estrés sectorial (principal) · secundarias: —
- **Calidad Q:** 93 (A) — Tipo 24/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** DOI: 10.1111/1468-0300.00091 · Copia: http://www.bis.org/bcbs/ca/acertasc.pdf · arXiv: cond-mat/0105191
- **Acceso y licencia:** Copia gratuita en el BPI y arXiv
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «expected shortfall coherent risk measure value at risk backtesting extreme value theory (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Expected shortfall», que reproduce la cita completa)
- **Contenido:** Exposición divulgativa-técnica del ES como alternativa coherente al VaR y su estimador empírico.
- **Uso en el Motor:** MC-B09: ES como alternativa coherente al VaR en el estrés de candidatos.
- **Limitaciones:** Solapa parcialmente con DOC-MOT-0350.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02. Reutilizada en F8 del Bloque B V2.0 (TMB-09) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0076 · Q 93 (A) — Optimization of Conditional Value-at-Risk

- **Autores:** R. Tyrrell Rockafellar; Stanislav Uryasev
- **Año:** 2000
- **Publicación o institución:** Journal of Risk, vol. 2, n.º 3, págs. 21-41
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-09 Riesgo: volatilidad, correlaciones, colas y estrés sectorial (principal) · secundarias: —
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI: 10.21314/JOR.2000.038 · PDF de los autores: https://sites.math.washington.edu/~rtr/papers/rtr179-CVaR1.pdf
- **Acceso y licencia:** Copia gratuita de los autores; revista por suscripción (Risk.net)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «expected shortfall coherent risk measure value at risk backtesting extreme value theory (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Expected shortfall», que reproduce la cita completa)
- **Contenido:** Formulación del CVaR como problema de minimización auxiliar que con escenarios se resuelve por programación lineal, obteniendo a la vez VaR y CVaR.
- **Uso en el Motor:** MC-B09: optimización de CVaR para cestas de candidatos con límite de pérdida en cola (apoyo a AG-B12).
- **Limitaciones:** Supone distribuciones continuas (generalizado en 2002). Wikipedia indica págs. 21-42.
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (tanda 2). Reutilizada en F8 del Bloque B V2.0 (TMB-09) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0363 · Q 93 (A) — Models for Exceedances over High Thresholds

- **Autores:** A. C. Davison; R. L. Smith
- **Año:** 1990
- **Publicación o institución:** Journal of the Royal Statistical Society, Series B, vol. 52, n.º 3, págs. 393-425
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-09 Riesgo: volatilidad, correlaciones, colas y estrés sectorial (principal) · secundarias: —
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1111/j.2517-6161.1990.tb01796.x · https://rss.onlinelibrary.wiley.com/doi/10.1111/j.2517-6161.1990.tb01796.x
- **Acceso y licencia:** Texto completo por suscripción en la editorial (Wiley/RSS)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «generalized Pareto distribution extreme value theory Hill estimator copula CoVaR systemic risk (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Extreme value theory», que reproduce la cita completa)
- **Contenido:** Desarrolla el método de picos sobre umbral (POT) con GPD, regresión y diagnósticos.
- **Uso en el Motor:** MC-B09: picos sobre umbral (GPD) para estimar colas de rendimientos sectoriales y de precios de insumos.
- **Limitaciones:** Datos no financieros.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02. Reutilizada en F8 del Bloque B V2.0 (TMB-09) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0355 · Q 93 (A) — Basel Framework MAR32: Internal Models Approach — Backtesting and P&L Attribution Test Requirements

- **Autores:** Basel Committee on Banking Supervision / Bank for International Settlements
- **Año:** Publicación continua (consolidada)
- **Publicación o institución:** Bank for International Settlements, Basel Framework, capítulo MAR32
- **Tipo de documento:** Norma técnica de organismo oficial
- **Temática:** TMB-09 Riesgo: volatilidad, correlaciones, colas y estrés sectorial (principal) · secundarias: TMB-11
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 14/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://www.bis.org/basel_framework/chapter/MAR/32.htm
- **Acceso y licencia:** Acceso gratuito (BPI)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «expected shortfall coherent risk measure value at risk backtesting extreme value theory (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Value at risk», que reproduce la cita completa)
- **Contenido:** Requisitos regulatorios de backtesting del VaR (zonas de semáforo por número de excepciones) y test de atribución de P&L.
- **Uso en el Motor:** MC-B09 y MC-B10: estándar regulatorio de backtesting y semáforo de excepciones, adaptable a los modelos de riesgo del Motor.
- **Limitaciones:** Texto normativo vivo; citar la versión consultada.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02. Reutilizada en F8 del Bloque B V2.0 (TMB-09) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0367 · Q 91 (A) — Analytical Value-at-Risk with Jumps and Stochastic Volatility

- **Autores:** Darrell Duffie; Jun Pan
- **Año:** 2001
- **Publicación o institución:** Finance and Stochastics, vol. 5, n.º 2, págs. 155-180
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-09 Riesgo: volatilidad, correlaciones, colas y estrés sectorial (principal) · secundarias: —
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1007/PL00013592 · https://doi.org/10.1007%2FPL00013592
- **Acceso y licencia:** Texto completo por suscripción en la editorial (Springer)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «VIX variance swap jump diffusion volatility risk premium implied volatility (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Stochastic volatility jump models», que reproduce la cita completa)
- **Contenido:** VaR analítico de carteras con opciones bajo saltos y volatilidad estocástica mediante transformadas afines.
- **Uso en el Motor:** MC-B09: VaR analítico con saltos y volatilidad estocástica para sectores expuestos a eventos discretos (regulación, catástrofes).
- **Limitaciones:** Requiere modelo afín.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02. Reutilizada en F8 del Bloque B V2.0 (TMB-09) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0360 · Q 91 (A) — A Simple General Approach to Inference about the Tail of a Distribution

- **Autores:** Bruce M. Hill
- **Año:** 1975
- **Publicación o institución:** The Annals of Statistics, vol. 3, págs. 1163-1174
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-09 Riesgo: volatilidad, correlaciones, colas y estrés sectorial (principal) · secundarias: —
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** DOI no visto · Cita en https://en.wikipedia.org/wiki/Heavy-tailed_distribution
- **Acceso y licencia:** No determinado (no se ha localizado copia ni página editorial en esta pasada)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «generalized Pareto distribution extreme value theory Hill estimator copula CoVaR systemic risk (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Heavy-tailed distribution», que reproduce la cita completa)
- **Contenido:** Estimador de Hill del índice de cola para distribuciones de tipo Pareto a partir de los estadísticos de orden superiores.
- **Uso en el Motor:** MC-B09: estimador de Hill del índice de cola para clasificar sectores por grosor de cola.
- **Limitaciones:** Sensible al número de estadísticos de orden. Alerta: REPARAR (localizar DOI/URL).
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02. Reutilizada en F8 del Bloque B V2.0 (TMB-09) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0357 · Q 90 (A) — CISS – A Composite Indicator of Systemic Stress in the Financial System

- **Autores:** Dániel Holló; Manfred Kremer; Marco Lo Duca
- **Año:** 2012
- **Publicación o institución:** European Central Bank, Working Paper Series n.º 1426 (marzo de 2012)
- **Tipo de documento:** Documento de trabajo (banco central)
- **Temática:** TMB-09 Riesgo: volatilidad, correlaciones, colas y estrés sectorial (principal) · secundarias: TMB-01
- **Calidad Q:** 90 (A) — Tipo 20/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** https://ECB.eu/pub/pdf/scpwps/ecbwp1426.pdf (redirige a ecb.europa.eu) · Perfil BCE: https://www.ecb.europa.eu/pub/research/authors/profiles/daniel-hollo.en.html
- **Acceso y licencia:** Acceso gratuito (BCE)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Holló Kremer Lo Duca "CISS – a composite indicator of systemic stress in the financial system" ECB Working Paper 1426»; WebFetch: sí, perfil de autor del BCE (el PDF redirige al dominio del BCE))
- **Contenido:** Indicador compuesto de estrés sistémico que agrega subíndices de mercados con ponderación por correlaciones cambiantes (enfoque de cartera).
- **Uso en el Motor:** MC-B09 y AG-B08: indicador compuesto de estrés sistémico como variable de estado para condicionar el estrés sectorial.
- **Limitaciones:** Construcción específica de la zona del euro.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02. Reutilizada en F8 del Bloque B V2.0 (TMB-09) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0077 · Q 89 (A) — Quantitative Risk Management: Concepts, Techniques and Tools (ed. revisada)

- **Autores:** Alexander J. McNeil; Rüdiger Frey; Paul Embrechts
- **Año:** 2015
- **Publicación o institución:** Princeton University Press (Princeton Series in Finance)
- **Tipo de documento:** Manual de referencia
- **Temática:** TMB-09 Riesgo: volatilidad, correlaciones, colas y estrés sectorial (principal) · secundarias: TMB-08
- **Calidad Q:** 89 (A) — Tipo 20/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** ISBN: 978-0-691-16627-8 · https://econpapers.repec.org/RePEc:pup:chapts:10496-1
- **Acceso y licencia:** De pago; capítulos introductorios con ficha en RePEc
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «McNeil Frey Embrechts "Quantitative Risk Management" revised edition 2015 Princeton University Press»; WebFetch: sí, ficha EconPapers del prefacio)
- **Contenido:** Manual integral de riesgo cuantitativo: medidas de riesgo, modelos de series, valores extremos, cópulas, riesgo de crédito y operacional, backtesting.
- **Uso en el Motor:** MC-B09: manual de referencia (cópulas, EVT, agregación de riesgos, estrés) para todo el módulo de riesgo del Motor de Mercados.
- **Limitaciones:** Extenso; requiere base de probabilidad.
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (tanda 2). Reutilizada en F8 del Bloque B V2.0 (TMB-09) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0362 · Q 88 (A) — An Introduction to Statistical Modeling of Extreme Values

- **Autores:** Stuart Coles
- **Año:** 2001
- **Publicación o institución:** Springer (Springer Series in Statistics)
- **Tipo de documento:** Manual de referencia
- **Temática:** TMB-09 Riesgo: volatilidad, correlaciones, colas y estrés sectorial (principal) · secundarias: —
- **Calidad Q:** 88 (A) — Tipo 20/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.1007/978-1-4471-3675-0 · ISBN: 978-1-84996-874-4
- **Acceso y licencia:** De pago (Springer)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «generalized Pareto distribution extreme value theory Hill estimator copula CoVaR systemic risk (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Extreme value theory», que reproduce la cita completa)
- **Contenido:** Manual aplicado de valores extremos: GEV, GPD/POT, procesos puntuales, no estacionariedad y extremos multivariantes, con inferencia por verosimilitud.
- **Uso en el Motor:** MC-B09: introducción aplicada a valores extremos para dimensionar pérdidas sectoriales de baja frecuencia.
- **Limitaciones:** Ejemplos ambientales más que financieros.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02. Reutilizada en F8 del Bloque B V2.0 (TMB-09) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0072 · Q 88 (A) — Techniques for Verifying the Accuracy of Risk Measurement Models

- **Autores:** Paul H. Kupiec
- **Año:** 1995
- **Publicación o institución:** Board of Governors of the Federal Reserve System, Finance and Economics Discussion Series 95-24
- **Tipo de documento:** Documento de trabajo
- **Temática:** TMB-09 Riesgo: volatilidad, correlaciones, colas y estrés sectorial (principal) · secundarias: TMB-11
- **Calidad Q:** 88 (A) — Tipo 20/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** Sin DOI visto · https://ideas.repec.org/f/pku379.html (registro del autor; ítem 95-24)
- **Acceso y licencia:** Acceso gratuito (serie FEDS)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Kupiec 1995 "Techniques for verifying the accuracy of risk measurement models" Journal of Derivatives»; WebFetch: sí, página de autor en IDEAS/RePEc)
- **Contenido:** Contraste de proporción de fallos (POF) de cobertura incondicional del VaR y análisis de su baja potencia con muestras cortas.
- **Uso en el Motor:** MC-B09 y MC-B10: test de proporción de fallos de Kupiec para validar el VaR sectorial.
- **Limitaciones:** Corrección: se cita la versión FEDS confirmada; la versión en The Journal of Derivatives 3(2) de la semilla no se ha podido confirmar.
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (tanda 2). Reutilizada en F8 del Bloque B V2.0 (TMB-09) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0078 · Q 87 (A) — Modelling Extremal Events for Insurance and Finance

- **Autores:** Paul Embrechts; Claudia Klüppelberg; Thomas Mikosch
- **Año:** 1997
- **Publicación o institución:** Springer (Stochastic Modelling and Applied Probability, vol. 33)
- **Tipo de documento:** Libro académico
- **Temática:** TMB-09 Riesgo: volatilidad, correlaciones, colas y estrés sectorial (principal) · secundarias: —
- **Calidad Q:** 87 (A) — Tipo 20/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.1007/978-3-642-33483-2 · ISBN: 978-3-642-08242-9 · Cita en https://en.wikipedia.org/wiki/Heavy-tailed_distribution
- **Acceso y licencia:** De pago (Springer)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «generalized Pareto distribution extreme value theory Hill estimator copula CoVaR systemic risk (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Heavy-tailed distribution», que reproduce la cita completa y «Extreme value theory»)
- **Contenido:** Tratado de valores extremos: GEV, GPD, estimadores de cola (Hill), distribuciones subexponenciales y aplicaciones actuariales y financieras.
- **Uso en el Motor:** MC-B09: referencia teórica de eventos extremos y riesgo de cola en seguros y finanzas.
- **Limitaciones:** Alto nivel matemático.
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (tanda 2). Reutilizada en F8 del Bloque B V2.0 (TMB-09) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### ANA-DOC-0517 · Q 84 (A) — Climate Stress Testing

- **Autores:** Viral V. Acharya; Richard Berner; Robert Engle; Hyeyoon Jung; Johannes Stroebel; Xuran Zeng; Yihao Zhao
- **Año:** 2023
- **Publicación o institución:** Annual Review of Financial Economics, 15(1), 291–326
- **Tipo de documento:** Artículo de revisión revisado
- **Temática:** TMB-09 Riesgo: volatilidad, correlaciones, colas y estrés sectorial (principal) · secundarias: TMB-08
- **Calidad Q:** 84 (A) — Tipo 23/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 7/10 · Independencia 10/10 · Acceso 4/10
- **DOI / URL:** DOI: 10.1146/annurev-financial-110921-101555 · URL de acceso: https://ideas.repec.org/a/anr/refeco/v15y2023p291-326.html
- **Acceso y licencia:** Peldaño 3 (revista; versiones de trabajo en NBER)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Giglio Kelly Stroebel Climate Finance» → perfil IDEAS de Stroebel; WebFetch: sí)
- **Contenido:** Revisa los escenarios regulatorios de pruebas de resistencia climática y pide modelizar mejor el riesgo de transición por políticas, las retroalimentaciones clima-economía y los riesgos compuestos; valora pruebas basadas en datos de mercado.
- **Uso en el Motor:** MC-B09 y AG-B11: estrés climático de carteras y sectores (beta climática); traduce escenarios de transición en pérdidas sectoriales.
- **Limitaciones:** Orientación a supervisión bancaria; escasa cuantificación propia.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-09) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0366 · Q 83 (A) — Value at Risk: The New Benchmark for Managing Financial Risk (3.ª ed.)

- **Autores:** Philippe Jorion
- **Año:** 2006
- **Publicación o institución:** McGraw-Hill
- **Tipo de documento:** Manual de referencia
- **Temática:** TMB-09 Riesgo: volatilidad, correlaciones, colas y estrés sectorial (principal) · secundarias: —
- **Calidad Q:** 83 (A) — Tipo 20/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** ISBN: 978-0-07-146495-6 · Cita en https://en.wikipedia.org/wiki/Value_at_risk
- **Acceso y licencia:** De pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «expected shortfall coherent risk measure value at risk backtesting extreme value theory (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Value at risk», que reproduce la cita completa)
- **Contenido:** Manual profesional del VaR: métodos de cálculo, backtesting, pruebas de estrés y uso regulatorio.
- **Uso en el Motor:** MC-B09: manual práctico de VaR (métodos, mapeo de posiciones, estrés) para el riesgo de cestas sectoriales; AG-B09 y AG-B11.
- **Limitaciones:** Previo a FRTB y al ES regulatorio.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02. Reutilizada en F8 del Bloque B V2.0 (TMB-09) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0079 · Q 80 (A) — Backtesting Expected Shortfall

- **Autores:** Carlo Acerbi; Balázs Székely
- **Año:** 2014
- **Publicación o institución:** MSCI Inc. (documento de investigación, diciembre de 2014; borrador de 27/10/2014)
- **Tipo de documento:** Informe técnico con metodología
- **Temática:** TMB-09 Riesgo: volatilidad, correlaciones, colas y estrés sectorial (principal) · secundarias: TMB-11
- **Calidad Q:** 80 (A) — Tipo 15/25 · Rigor 16/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 8/10 · Acceso 9/10
- **DOI / ISBN / URL:** Sin DOI · https://www.msci.com/documents/10199/22aa9922-f874-4060-b77a-0f0e267a489b
- **Acceso y licencia:** Acceso gratuito (MSCI)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Acerbi Szekely "Backtesting Expected Shortfall" 2014 Risk MSCI»; WebFetch: sí, documento MSCI)
- **Contenido:** Tres contrastes no paramétricos para backtesting del ES (magnitud de excepciones, contraste directo de cola y contraste por rangos).
- **Uso en el Motor:** MC-B09 y MC-B10: backtesting de Expected Shortfall.
- **Limitaciones:** Autores vinculados a proveedor comercial; la versión en la revista Risk no se ha confirmado.
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (tanda 2). Reutilizada en F8 del Bloque B V2.0 (TMB-09) el 2026-11-02 con su ID original; Temática y Uso adaptados.

## TMB-10 Análisis input-output y redes de cadena de suministro

#### MBM-0226 · Q 94 (A) — Tracing Value-Added and Double Counting in Gross Exports

- **Autores:** Robert Koopman; Zhi Wang; Shang-Jin Wei
- **Año:** 2014
- **Publicación o institución:** American Economic Review, vol. 104, n.º 2 (NBER WP 18579, 2012)
- **Tipo de documento:** Artículo revisado por pares (revista de primer nivel)
- **Temática:** TMB-10 Análisis input-output y redes de cadena de suministro (principal) · secundarias: TMB-14
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI de la revista: 10.1257/aer.104.2.459 · DOI NBER: 10.3386/w18579 · https://www.nber.org/papers/w18579
- **Acceso y licencia:** Documento de trabajo NBER; revista de pago
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «"Tracing Value-Added and Double Counting in Gross Exports" Koopman Wang Wei 2014 "Measuring the Upstreamness of Production and Trade Flows" Antràs 2012 Timmer "An Illustrated User Guide to the World Input–Output Database"»; WebFetch: sí, página NBER)
- **Contenido:** Descompone las exportaciones brutas en valor añadido doméstico, extranjero y doble contabilización con tablas input-output multirregionales.
- **Uso en el Motor:** MC-B09 y AG-B05: medir el contenido importado y la exposición indirecta de un sector a países y a cuellos de botella (PERF-B-CADENA).
- **Limitaciones:** Requiere tablas input-output mundiales.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### ANA-DOC-0448 · Q 94 (A) — The Network Origins of Aggregate Fluctuations

- **Autores:** Daron Acemoglu; Vasco M. Carvalho; Asuman Ozdaglar; Alireza Tahbaz-Salehi
- **Año:** 2012
- **Publicación o institución:** Econometrica, vol. 80, n.º 5, págs. 1977-2016
- **Tipo de documento:** Artículo revisado por pares (revista de primer nivel)
- **Temática:** TMB-10 Análisis input-output y redes de cadena de suministro (principal) · secundarias: TMB-09
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / URL:** DOI: 10.3982/ECTA9623 · URL: https://www.econometricsociety.org/publications/econometrica/2012/09/01/network-origins-aggregate-fluctuations
- **Acceso y licencia:** Peldaño 2 (documento de trabajo abierto en UPF/BSE); versión editorial de pago (Econometric Society)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Vasco M. Carvalho IDEAS RePEc "The Network Origins of Aggregate Fluctuations" "Supply Chain Disruptions"»; WebFetch: sí)
- **Contenido:** Shocks sectoriales pequeños generan fluctuaciones agregadas cuando los sectores están conectados por redes input-output asimétricas (proveedores dominantes).
- **Uso en el Motor:** MC-B09 y AG-B05: identificar sectores nodo de la red input-output cuyos shocks se propagan al agregado; ponderar el riesgo de cadena en candidatos.
- **Limitaciones:** Resultado teórico; la evidencia cuantitativa está en trabajos posteriores.
- **Disciplinas y etiquetas:** Redes de producción; ciclo · cadenas-valor; redes; input-output
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-10) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### MBM-0225 · Q 93 (A) — Input Specificity and the Propagation of Idiosyncratic Shocks in Production Networks

- **Autores:** Jean-Noël Barrot; Julien Sauvagnat
- **Año:** 2016
- **Publicación o institución:** The Quarterly Journal of Economics, vol. 131, n.º 3, págs. 1543-1592
- **Tipo de documento:** Artículo revisado por pares (revista de primer nivel)
- **Temática:** TMB-10 Análisis input-output y redes de cadena de suministro (principal) · secundarias: TMB-09
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1093/qje/qjw018 · https://ideas.repec.org/a/oup/qjecon/v131y2016i3p1543-1592..html · Versión abierta: https://dspace.mit.edu/handle/1721.1/111134
- **Acceso y licencia:** Revista de pago; versión abierta en DSpace@MIT
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Barrot Sauvagnat 2016 "Input Specificity and the Propagation of Idiosyncratic Shocks in Production Networks" Quarterly Journal of Economics»; WebFetch: sí, ficha IDEAS/RePEc)
- **Contenido:** Con desastres naturales como shocks, muestra que los clientes de proveedores afectados pierden producción y valor de mercado, sobre todo si el input es específico.
- **Uso en el Motor:** MC-B09 y AG-B05: ponderar el riesgo de cadena de un candidato por la especificidad de sus inputs críticos y por la concentración de proveedores.
- **Limitaciones:** Datos de empresas estadounidenses.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### ANA-DOC-0449 · Q 91 (A) — Supply Chain Disruptions: Evidence from the Great East Japan Earthquake

- **Autores:** Vasco M. Carvalho; Makoto Nirei; Yukiko U. Saito; Alireza Tahbaz-Salehi
- **Año:** 2021
- **Publicación o institución:** Quarterly Journal of Economics, vol. 136, n.º 2, págs. 1255-1321
- **Tipo de documento:** Artículo revisado por pares (revista de primer nivel)
- **Temática:** TMB-10 Análisis input-output y redes de cadena de suministro (principal) · secundarias: TMB-09
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 6/10
- **DOI / URL:** Página índice: https://authors.repec.org/pro/pca56/ (DOI no visto)
- **Acceso y licencia:** Peldaño 4 (versión editorial de pago, OUP)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Vasco M. Carvalho IDEAS RePEc "The Network Origins of Aggregate Fluctuations" "Supply Chain Disruptions"»; WebFetch: sí, página índice del perfil RePEc; ficha individual no cargada)
- **Contenido:** Usa el terremoto de 2011 en Japón como experimento natural para cuantificar la propagación de shocks aguas arriba y aguas abajo por las redes de proveedores y clientes.
- **Uso en el Motor:** MC-B09 y AG-B05: evidencia cuantitativa de propagación de un shock de oferta por la red de proveedores; calibrar escenarios de disrupción.
- **Limitaciones:** Resumen no leído en esta carga; caso japonés.
- **Disciplinas y etiquetas:** Cadenas de suministro; propagación de shocks · cadenas-valor; disrupciones; japon
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-10) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### ANA-DOC-0451 · Q 90 (A) — Accounting for intermediates: Production sharing and trade in value added

- **Autores:** Robert C. Johnson; Guillermo Noguera
- **Año:** 2012
- **Publicación o institución:** Journal of International Economics, vol. 86, n.º 2, págs. 224-236
- **Tipo de documento:** Artículo revisado por pares (revista de primer nivel)
- **Temática:** TMB-10 Análisis input-output y redes de cadena de suministro (principal) · secundarias: TMB-14
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 8/10 · Impacto 9/10 · Independencia 10/10 · Acceso 7/10
- **DOI / URL:** DOI: 10.1016/j.jinteco.2011.10.003 · URL: https://ideas.repec.org/a/eee/inecon/v86y2012i2p224-236.html
- **Acceso y licencia:** Peldaño 4 (versión editorial de pago, Elsevier; ficha RePEc abierta)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Robert C. Johnson IDEAS RePEc "Accounting for intermediates" "Measuring Global Value Chains"»; WebFetch: sí, ficha RePEc)
- **Contenido:** Estima el valor añadido contenido en el comercio bilateral con tablas input-output y propone el ratio VAX (valor añadido/exportaciones brutas) como medida de producción compartida.
- **Uso en el Motor:** MC-B09 y AG-B05: comercio en valor añadido con tablas input-output; separa exposición directa e indirecta de un sector a un país.
- **Limitaciones:** Supuestos de proporcionalidad de las tablas input-output.
- **Disciplinas y etiquetas:** Comercio en valor añadido; cadenas globales de valor · cadenas-valor; vax; tiva
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-10) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### MBM-0231 · Q 90 (A) — Measuring the Upstreamness of Production and Trade Flows

- **Autores:** Pol Antràs; Davin Chor; Thibault Fally; Russell Hillberry
- **Año:** 2012
- **Publicación o institución:** American Economic Review: Papers & Proceedings, vol. 102, n.º 3, págs. 412-416
- **Tipo de documento:** Artículo revisado (actas)
- **Temática:** TMB-10 Análisis input-output y redes de cadena de suministro (principal) · secundarias: TMB-04
- **Calidad Q:** 90 (A) — Tipo 22/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 10/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI: 10.1257/aer.102.3.412 · https://antras.scholars.harvard.edu/publications/measuring-upstreamness-production-and-trade-flows · Versión final: https://faculty.tuck.dartmouth.edu/images/uploads/faculty/davin-chor/AntrasChorFallyHillberry_AER_PP_2012_Final_Version.pdf
- **Acceso y licencia:** Versión final abierta en la página del autor
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Antràs Chor Fally Hillberry "Measuring the Upstreamness of Production and Trade Flows" American Economic Review Papers and Proceedings 2012»; WebFetch: sí, página del autor y PDF de la versión final)
- **Contenido:** Mide la distancia de cada industria a la demanda final (upstreamness) con tablas input-output de 426 industrias y datos STAN.
- **Uso en el Motor:** MC-B09 y AG-B05: situar sectores y candidatos en la cadena (aguas arriba o abajo) y anticipar su sensibilidad al ciclo y a shocks de inventario.
- **Limitaciones:** Tablas de EE. UU. de 2002.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### ANA-DOC-0455 · Q 90 (A) — Economic Links and Predictable Returns

- **Autores:** Lauren Cohen; Andrea Frazzini
- **Año:** 2008
- **Publicación o institución:** Journal of Finance, vol. 63, n.º 4, págs. 1977-2011
- **Tipo de documento:** Artículo revisado por pares (revista de primer nivel)
- **Temática:** TMB-10 Análisis input-output y redes de cadena de suministro (principal) · secundarias: TMB-12
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 8/10 · Impacto 9/10 · Independencia 10/10 · Acceso 7/10
- **DOI / URL:** DOI: 10.1111/j.1540-6261.2008.01379.x · URL: https://ideas.repec.org/a/bla/jfinan/v63y2008i4p1977-2011.html
- **Acceso y licencia:** Peldaño 4 (versión editorial de pago, Wiley; ficha RePEc abierta)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Cohen Frazzini "Economic Links and Predictable Returns" Journal of Finance 2008»; WebFetch: sí, ficha RePEc)
- **Contenido:** Por atención limitada, los inversores reaccionan con retraso a noticias de clientes de una empresa; una estrategia long-short basada en vínculos cliente-proveedor obtiene alfas mensuales superiores a 150 pb.
- **Uso en el Motor:** MC-B09 y AG-B12: vínculos cliente-proveedor como señal de rentabilidad predecible; mapa de exposición de candidatos a sus clientes.
- **Limitaciones:** Muestra de EE. UU. hasta 2004; posible erosión tras su publicación.
- **Disciplinas y etiquetas:** Cadena de suministro; atención limitada; anomalías · cadenas-valor; cliente-proveedor; senales
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-10) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### ANA-DOC-0456 · Q 89 (A) — World Development Report 2020: Trading for Development in the Age of Global Value Chains

- **Autores:** Banco Mundial
- **Año:** 2020
- **Publicación o institución:** Banco Mundial (Open Knowledge Repository, handle 10986/32437)
- **Tipo de documento:** Informe institucional de referencia (flagship)
- **Temática:** TMB-10 Análisis input-output y redes de cadena de suministro (principal) · secundarias: TMB-14
- **Calidad Q:** 89 (A) — Tipo 22/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 9/10 · Acceso 10/10
- **DOI / URL:** URL: https://openknowledge.worldbank.org/handle/10986/32437 (DOI no confirmado en la página leída)
- **Acceso y licencia:** Peldaño 1 (Banco Mundial, licencia CC BY 3.0 IGO)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «World Development Report 2020 "Trading for Development in the Age of Global Value Chains" Open Knowledge Repository»; WebFetch: sí)
- **Contenido:** Las cadenas globales de valor explican casi la mitad del comercio y la convergencia de países pobres desde 1990; desde 2008 su expansión se estanca y la automatización y los conflictos geopolíticos amenazan con fragmentarlas.
- **Uso en el Motor:** AG-B05 y AG-B07: diagnóstico de cadenas globales de valor y su política; contexto para escenarios de relocalización (MC-B09).
- **Limitaciones:** Anterior a la pandemia y a la fragmentación geoeconómica reciente.
- **Disciplinas y etiquetas:** Cadenas globales de valor; desarrollo · cadenas-valor; banco-mundial; desglobalizacion
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-10) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### MBM-0219 · Q 89 (A) — Input-Output Analysis: Foundations and Extensions (2.ª ed.)

- **Autores:** Ronald E. Miller; Peter D. Blair
- **Año:** 2009
- **Publicación o institución:** Cambridge University Press
- **Tipo de documento:** Libro académico (manual de referencia)
- **Temática:** TMB-10 Análisis input-output y redes de cadena de suministro (principal) · secundarias: TMB-09
- **Calidad Q:** 89 (A) — Tipo 22/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI del capítulo 1: 10.1017/CBO9780511626982.002 · ISBN: 9780521739023 · https://www.cambridge.org/core/books/inputoutput-analysis/introduction-and-overview/8C224C3F59BA29EDDA14F65A7E4E4B63
- **Acceso y licencia:** De pago (Cambridge)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Input–output model Leontief 1936 "Quantitative Input and Output Relations in the Economic System of the United States" Miller Blair Input-Output Analysis Foundations and Extensions»; WebFetch: sí, página del capítulo «Introduction and Overview» en Cambridge Core)
- **Contenido:** Manual de referencia del análisis input-output: tablas, matriz inversa de Leontief, multiplicadores, modelos multirregionales, encadenamientos y extensiones.
- **Uso en el Motor:** MC-B09 y AG-B05: fórmulas de multiplicadores, encadenamientos hacia atrás y hacia delante y propagación de shocks de demanda u oferta entre sectores.
- **Limitaciones:** Edición de 2009 (existe una posterior no verificada aquí).
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### ANA-DOC-0447 · Q 87 (A) — Risks and Global Supply Chains: What We Know and What We Need to Know

- **Autores:** Richard Baldwin; Rebecca Freeman
- **Año:** 2022
- **Publicación o institución:** Annual Review of Economics, vol. 14 (NBER Working Paper 29444; Bank of England Staff WP 2021)
- **Tipo de documento:** Artículo de revisión (survey) revisado
- **Temática:** TMB-10 Análisis input-output y redes de cadena de suministro (principal) · secundarias: TMB-09
- **Calidad Q:** 87 (A) — Tipo 23/25 · Rigor 14/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 7/10 · Independencia 10/10 · Acceso 9/10
- **DOI / URL:** DOI: 10.1146/annurev-economics-051420-113737 · URL: https://www.nber.org/papers/w29444
- **Acceso y licencia:** Peldaño 2 (documento de trabajo NBER; versión del Banco de Inglaterra en abierto)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Baldwin Freeman "Risks and Global Supply Chains: What We Know and What We Need to Know" Annual Review of Economics»; WebFetch: sí, NBER)
- **Contenido:** Revisa riesgos para y desde las cadenas globales de suministro, cuestiona que la relocalización hubiera evitado la escasez y propone el marco riesgo-rentabilidad de carteras para evaluar políticas de resiliencia; la exposición a shocks externos supera lo que indican las medidas directas.
- **Uso en el Motor:** AG-B05 y MC-B09: marco de riesgos de cadenas globales (oferta, demanda, transmisión) para el estrés de cadena de suministro.
- **Limitaciones:** Página NBER sin números de página de la versión publicada.
- **Disciplinas y etiquetas:** Cadenas de suministro; resiliencia · cadenas-valor; reshoring; riesgo
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-10) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### ANA-DOC-0446 · Q 86 (A) — Conceptual Aspects of Global Value Chains

- **Autores:** Pol Antràs
- **Año:** 2020
- **Publicación o institución:** The World Bank Economic Review, vol. 34, n.º 3, págs. 551-574 (NBER WP 26539; World Bank Policy Research WP 9114)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-10 Análisis input-output y redes de cadena de suministro (principal) · secundarias: —
- **Calidad Q:** 86 (A) — Tipo 23/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 7/10 · Independencia 10/10 · Acceso 7/10
- **DOI / URL:** DOI: 10.1093/wber/lhaa006 · URL: https://ideas.repec.org/a/oup/wbecrv/v34yi3p551-574..html · Versión abierta: https://documents1.worldbank.org/curated/en/541931579622262085/pdf/Conceptual-Aspects-of-Global-Value-Chains.pdf
- **Acceso y licencia:** Peldaño 2 (documento de trabajo del Banco Mundial en abierto); versión editorial de acceso restringido
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Pol Antràs RePEc IDEAS "Conceptual Aspects of Global Value Chains"»; WebFetch: sí, ficha RePEc)
- **Contenido:** Revisa definiciones e interpretaciones del auge de las cadenas globales de valor y sus implicaciones de medición, los determinantes y consecuencias de la participación para países y empresas, y el efecto previsible de las nuevas tecnologías.
- **Uso en el Motor:** AG-B05 y MC-B09: aspectos conceptuales de las cadenas globales de valor (relaciones, gobernanza) que condicionan la propagación de shocks.
- **Limitaciones:** La ficha RePEc no muestra el año (2020 inferido del DOI y de las versiones de trabajo; confirmar en el barrido).
- **Disciplinas y etiquetas:** Cadenas globales de valor; teoría · cadenas-valor; gvc; antras
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-10) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### ANA-DOC-0452 · Q 86 (A) — Measuring Global Value Chains

- **Autores:** Robert C. Johnson
- **Año:** 2018
- **Publicación o institución:** Annual Review of Economics, vol. 10, págs. 207-236 (NBER Working Paper 24027)
- **Tipo de documento:** Artículo de revisión (survey) revisado
- **Temática:** TMB-10 Análisis input-output y redes de cadena de suministro (principal) · secundarias: —
- **Calidad Q:** 86 (A) — Tipo 23/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 7/10 · Independencia 10/10 · Acceso 8/10
- **DOI / URL:** DOI: 10.1146/annurev-economics-080217-053600 · URL: https://www.nber.org/papers/w24027
- **Acceso y licencia:** Peldaño 2 (documento de trabajo NBER); versión editorial en Annual Reviews
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Robert C. Johnson IDEAS RePEc "Accounting for intermediates" "Measuring Global Value Chains"»; WebFetch: sí, NBER y perfil RePEc)
- **Contenido:** Revisa la medición de cadenas globales de valor: enfoque macro (tablas input-output mundiales, comercio en valor añadido, longitud y posición) y enfoque micro (datos de empresa, multinacionales).
- **Uso en el Motor:** MC-B09 y AG-B05: métricas de cadenas globales de valor (participación, posición, valor añadido) aplicables al análisis PERF-B-CADENA.
- **Limitaciones:** Corte 2017.
- **Disciplinas y etiquetas:** Medición; cadenas globales de valor · cadenas-valor; medicion; input-output
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-10) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### MBM-0227 · Q 85 (A) — The Nature and Growth of Vertical Specialization in World Trade

- **Autores:** David Hummels; Jun Ishii; Kei-Mu Yi
- **Año:** 2001
- **Publicación o institución:** Journal of International Economics, vol. 54, págs. 75-96
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-10 Análisis input-output y redes de cadena de suministro (principal) · secundarias: —
- **Calidad Q:** 85 (A) — Tipo 24/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 6/10 · Impacto 10/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** Página índice: https://www.usitc.gov/research_and_analysis/documents/AER_KWW3-17-2013_0.pdf (bibliografía)
- **Acceso y licencia:** De pago (Elsevier)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Tracing Value-Added and Double Counting in Gross Exports" Koopman Wang Wei 2014 "Measuring the Upstreamness of Production and Trade Flows" Antràs 2012 Timmer "An Illustrated User Guide to the World Input–Output Database"»; WebFetch: sí, versión USITC de Koopman, Wang y Wei (bibliografía))
- **Contenido:** Define y mide la especialización vertical (contenido importado de las exportaciones) con tablas input-output.
- **Uso en el Motor:** MC-B09: indicador básico de integración en cadenas globales por sector y país.
- **Limitaciones:** Supuestos de proporcionalidad de importaciones.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### ANA-DOC-0450 · Q 84 (A) — Production Networks: A Primer

- **Autores:** Vasco M. Carvalho; Alireza Tahbaz-Salehi
- **Año:** 2019
- **Publicación o institución:** Annual Review of Economics, vol. 11, págs. 635-663
- **Tipo de documento:** Artículo de revisión (survey) revisado
- **Temática:** TMB-10 Análisis input-output y redes de cadena de suministro (principal) · secundarias: —
- **Calidad Q:** 84 (A) — Tipo 23/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 7/10 · Independencia 10/10 · Acceso 6/10
- **DOI / URL:** Página índice: https://authors.repec.org/pro/pca56/ (DOI no visto)
- **Acceso y licencia:** Peldaño 4 (Annual Reviews, acceso restringido)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Vasco M. Carvalho IDEAS RePEc "The Network Origins of Aggregate Fluctuations" "Supply Chain Disruptions"»; WebFetch: sí, página índice del perfil RePEc; ficha individual no cargada)
- **Contenido:** Introducción a los modelos de redes de producción y a la propagación de shocks microeconómicos a través de relaciones input-output.
- **Uso en el Motor:** MC-B09: manual de redes de producción (centralidad, multiplicadores, propagación) para el submódulo de contagio en la cadena.
- **Limitaciones:** Resumen no leído en esta carga.
- **Disciplinas y etiquetas:** Redes de producción; survey · cadenas-valor; redes
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-10) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### ANA-DOC-0457 · Q 84 (A) — From Micro to Macro via Production Networks

- **Autores:** Vasco M. Carvalho
- **Año:** 2014
- **Publicación o institución:** Journal of Economic Perspectives, vol. 28, n.º 4, págs. 23-48
- **Tipo de documento:** Artículo de revisión revisado (revista de la AEA)
- **Temática:** TMB-10 Análisis input-output y redes de cadena de suministro (principal) · secundarias: —
- **Calidad Q:** 84 (A) — Tipo 22/25 · Rigor 14/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 7/10 · Independencia 10/10 · Acceso 8/10
- **DOI / URL:** Página índice: https://authors.repec.org/pro/pca56/ (DOI no visto)
- **Acceso y licencia:** Peldaño 1 (JEP es de acceso abierto en la AEA)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Vasco M. Carvalho IDEAS RePEc "The Network Origins of Aggregate Fluctuations" "Supply Chain Disruptions"»; WebFetch: sí, página índice del perfil RePEc; ficha individual no cargada)
- **Contenido:** Exposición divulgativa de cómo las redes de producción convierten shocks de empresas o sectores en fluctuaciones agregadas.
- **Uso en el Motor:** MC-B09: síntesis de cómo shocks microeconómicos se agregan vía redes de producción; base de los multiplicadores sectoriales.
- **Limitaciones:** Resumen no leído en esta carga; nivel introductorio.
- **Disciplinas y etiquetas:** Redes de producción; divulgación académica · cadenas-valor; redes
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-10) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### MBM-0220 · Q 84 (A) — Quantitative Input and Output Relations in the Economic System of the United States

- **Autores:** Wassily W. Leontief
- **Año:** 1936
- **Publicación o institución:** Review of Economics and Statistics, vol. XVIII, n.º 3
- **Tipo de documento:** Artículo revisado por pares (fundacional)
- **Temática:** TMB-10 Análisis input-output y redes de cadena de suministro (principal) · secundarias: —
- **Calidad Q:** 84 (A) — Tipo 24/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 5/10 · Impacto 10/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** Página índice: https://economix.fr/uploads/source/doc/workshops/2012_pioneers/aroche-marquez.pdf (bibliografía); citado también en Miller y Blair (2009)
- **Acceso y licencia:** De pago (JSTOR)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Ghosh 1958 "Input-Output Approach in an Allocation System" Economica Leontief 1936 Review of Economic Statistics supply-driven model»; WebFetch: sí, documento de Aroche y Márquez (bibliografía) y capítulo 1 de Miller y Blair)
- **Contenido:** Primera tabla input-output de la economía de EE. UU. y fundamento del modelo de Leontief.
- **Uso en el Motor:** MC-B09: fundamento teórico del modelo de demanda que usa el submódulo input-output.
- **Limitaciones:** Valor histórico; datos de los años veinte.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### ANA-DOC-0453 · Q 83 (A) — Five Facts about Value-Added Exports and Implications for Macroeconomics and Trade Research

- **Autores:** Robert C. Johnson
- **Año:** 2014
- **Publicación o institución:** Journal of Economic Perspectives, vol. 28, n.º 2, págs. 119-142
- **Tipo de documento:** Artículo de revisión revisado (revista de la AEA)
- **Temática:** TMB-10 Análisis input-output y redes de cadena de suministro (principal) · secundarias: —
- **Calidad Q:** 83 (A) — Tipo 22/25 · Rigor 14/20 · Autoridad 14/15 · Vigencia 8/10 · Impacto 7/10 · Independencia 10/10 · Acceso 8/10
- **DOI / URL:** Página índice: https://ideas.repec.org/e/pjo146.html (ficha: ideas.repec.org/a/aea/jecper/v28y2014i2p119-42.html; DOI no visto)
- **Acceso y licencia:** Peldaño 1 (JEP es de acceso abierto en la AEA)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Robert C. Johnson IDEAS RePEc "Accounting for intermediates" "Measuring Global Value Chains"»; WebFetch: sí, página índice del perfil RePEc; ficha individual no cargada)
- **Contenido:** Cinco hechos estilizados sobre exportaciones en valor añadido frente a brutas y sus implicaciones para el análisis macro y comercial.
- **Uso en el Motor:** MC-B09: hechos estilizados del comercio en valor añadido para contrastar los resultados del módulo input-output.
- **Limitaciones:** Resumen no leído en esta carga.
- **Disciplinas y etiquetas:** Comercio en valor añadido · cadenas-valor; valor-anadido
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-10) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### MBM-0224 · Q 82 (A) — In Vindication of the Ghosh Model: A Reinterpretation as a Price Model

- **Autores:** Erik Dietzenbacher
- **Año:** 1997
- **Publicación o institución:** Journal of Regional Science, vol. 37, n.º 4, págs. 629-651
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-10 Análisis input-output y redes de cadena de suministro (principal) · secundarias: TMB-04
- **Calidad Q:** 82 (A) — Tipo 24/25 · Rigor 17/20 · Autoridad 13/15 · Vigencia 6/10 · Impacto 8/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** Página índice: https://economix.fr/uploads/source/doc/workshops/2012_pioneers/aroche-marquez.pdf (bibliografía)
- **Acceso y licencia:** De pago (Wiley)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Ghosh 1958 "Input-Output Approach in an Allocation System" Economica Leontief 1936 Review of Economic Statistics supply-driven model»; WebFetch: sí, documento de Aroche y Márquez (bibliografía; título según la obra citada))
- **Contenido:** Reinterpreta el modelo de Ghosh como modelo de precios (de costes): propagación aguas abajo de un aumento del precio de un input.
- **Uso en el Motor:** MC-B09 y MC-B04: trasladar subidas de coste de insumos (energía, materias primas) a los costes de los sectores clientes.
- **Limitaciones:** Supone traslación completa de costes.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### MBM-0229 · Q 81 (A) — The World Input-Output Database (WIOD): Contents, Sources and Methods

- **Autores:** Marcel P. Timmer (ed.)
- **Año:** 2012
- **Publicación o institución:** WIOD Working Paper n.º 10 (www.wiod.org)
- **Tipo de documento:** Documento técnico de base de datos
- **Temática:** TMB-10 Análisis input-output y redes de cadena de suministro (principal) · secundarias: TMB-14
- **Calidad Q:** 81 (A) — Tipo 17/25 · Rigor 17/20 · Autoridad 13/15 · Vigencia 7/10 · Impacto 9/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** Página índice: https://www.usitc.gov/research_and_analysis/documents/AER_KWW3-17-2013_0.pdf (bibliografía)
- **Acceso y licencia:** Acceso abierto (documentación de WIOD)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Tracing Value-Added and Double Counting in Gross Exports" Koopman Wang Wei 2014 "Measuring the Upstreamness of Production and Trade Flows" Antràs 2012 Timmer "An Illustrated User Guide to the World Input–Output Database"»; WebFetch: sí, versión USITC de Koopman, Wang y Wei (bibliografía))
- **Contenido:** Documentación de contenidos, fuentes y métodos de construcción de las tablas input-output mundiales WIOD.
- **Uso en el Motor:** MC-B09 y TMB-14: conocer cómo se construyen las tablas mundiales antes de usarlas en el submódulo input-output.
- **Limitaciones:** Versión de 2012; existen ediciones posteriores de WIOD.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### MBM-0228 · Q 81 (A) — Who Produces for Whom in the World Economy?

- **Autores:** Guillaume Daudin; Christine Rifflart; Danielle Schweisguth
- **Año:** 2011
- **Publicación o institución:** Canadian Journal of Economics, vol. 44, n.º 4
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-10 Análisis input-output y redes de cadena de suministro (principal) · secundarias: —
- **Calidad Q:** 81 (A) — Tipo 24/25 · Rigor 16/20 · Autoridad 12/15 · Vigencia 7/10 · Impacto 8/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** Página índice: https://www.usitc.gov/research_and_analysis/documents/AER_KWW3-17-2013_0.pdf (bibliografía)
- **Acceso y licencia:** De pago (Wiley)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Tracing Value-Added and Double Counting in Gross Exports" Koopman Wang Wei 2014 "Measuring the Upstreamness of Production and Trade Flows" Antràs 2012 Timmer "An Illustrated User Guide to the World Input–Output Database"»; WebFetch: sí, versión USITC de Koopman, Wang y Wei (bibliografía))
- **Contenido:** Reconstruye el comercio en valor añadido para identificar qué países producen para la demanda final de cuáles.
- **Uso en el Motor:** MC-B09 y AG-B07: exposición de sectores a la demanda final de países concretos (riesgo geopolítico y arancelario).
- **Limitaciones:** Datos GTAP de la década de 2000.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### MBM-0221 · Q 80 (A) — Input-Output Economics (2.ª ed.)

- **Autores:** Wassily W. Leontief
- **Año:** 1986
- **Publicación o institución:** Oxford University Press
- **Tipo de documento:** Libro académico (recopilación del autor)
- **Temática:** TMB-10 Análisis input-output y redes de cadena de suministro (principal) · secundarias: —
- **Calidad Q:** 80 (A) — Tipo 20/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 6/10 · Impacto 9/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** Página índice: https://economix.fr/uploads/source/doc/workshops/2012_pioneers/aroche-marquez.pdf (bibliografía)
- **Acceso y licencia:** De pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Ghosh 1958 "Input-Output Approach in an Allocation System" Economica Leontief 1936 Review of Economic Statistics supply-driven model»; WebFetch: sí, documento de Aroche y Márquez (bibliografía))
- **Contenido:** Recopilación de los trabajos de Leontief sobre el modelo input-output, sus aplicaciones y extensiones.
- **Uso en el Motor:** MC-B09: consulta de los supuestos y aplicaciones originales del modelo.
- **Limitaciones:** Edición antigua.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### MBM-0232 · Q 79 (B) — Concepts and Methods of the Input-Output Account

- **Autores:** Karen J. Horowitz; Mark A. Planting
- **Año:** 2009
- **Publicación o institución:** Bureau of Economic Analysis (documentación)
- **Tipo de documento:** Documento metodológico oficial
- **Temática:** TMB-10 Análisis input-output y redes de cadena de suministro (principal) · secundarias: TMB-14
- **Calidad Q:** 79 (B) — Tipo 18/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 7/10 · Impacto 6/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** Página índice: https://faculty.tuck.dartmouth.edu/images/uploads/faculty/davin-chor/AntrasChorFallyHillberry_AER_PP_2012_Final_Version.pdf (bibliografía)
- **Acceso y licencia:** Documentación oficial abierta
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Antràs Chor Fally Hillberry "Measuring the Upstreamness of Production and Trade Flows" American Economic Review Papers and Proceedings 2012»; WebFetch: sí, bibliografía de Antràs et al. (2012))
- **Contenido:** Documentación del BEA sobre conceptos, clasificaciones y métodos de las cuentas input-output de EE. UU.
- **Uso en el Motor:** MC-B09 y TMB-14: entender las tablas oficiales de EE. UU. (fuente gratuita) antes de calcular multiplicadores sectoriales.
- **Limitaciones:** Título según la cita de Antràs et al.; puede haber versiones posteriores.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### MBM-0223 · Q 79 (B) — On the Plausibility of the Supply-Driven Input-Output Model

- **Autores:** Jan Oosterhaven
- **Año:** 1988
- **Publicación o institución:** Journal of Regional Science, vol. 28, n.º 2, págs. 203-217
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-10 Análisis input-output y redes de cadena de suministro (principal) · secundarias: —
- **Calidad Q:** 79 (B) — Tipo 24/25 · Rigor 16/20 · Autoridad 12/15 · Vigencia 5/10 · Impacto 8/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** Página índice: https://economix.fr/uploads/source/doc/workshops/2012_pioneers/aroche-marquez.pdf (bibliografía)
- **Acceso y licencia:** De pago (Wiley)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Ghosh 1958 "Input-Output Approach in an Allocation System" Economica Leontief 1936 Review of Economic Statistics supply-driven model»; WebFetch: sí, documento de Aroche y Márquez (bibliografía))
- **Contenido:** Crítica del modelo de Ghosh como modelo de cantidades: implica sustitución perfecta poco realista entre inputs.
- **Uso en el Motor:** MC-B09 y Auditor: límite de uso del modelo de oferta; usarlo con cautela para shocks de suministro.
- **Limitaciones:** Debate teórico.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### MBM-0222 · Q 79 (B) — Input-Output Approach in an Allocation System

- **Autores:** Ambica Ghosh
- **Año:** 1958
- **Publicación o institución:** Economica, New Series, vol. 25, n.º 97, págs. 58-64
- **Tipo de documento:** Artículo revisado por pares (fundacional)
- **Temática:** TMB-10 Análisis input-output y redes de cadena de suministro (principal) · secundarias: —
- **Calidad Q:** 79 (B) — Tipo 24/25 · Rigor 15/20 · Autoridad 13/15 · Vigencia 5/10 · Impacto 8/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** Página índice: https://economix.fr/uploads/source/doc/workshops/2012_pioneers/aroche-marquez.pdf (bibliografía)
- **Acceso y licencia:** De pago (JSTOR/Wiley)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Ghosh 1958 "Input-Output Approach in an Allocation System" Economica Leontief 1936 Review of Economic Statistics supply-driven model»; WebFetch: sí, documento de Aroche y Márquez (bibliografía))
- **Contenido:** Modelo input-output impulsado por la oferta (coeficientes de asignación): cómo un cambio en inputs primarios se distribuye aguas abajo.
- **Uso en el Motor:** MC-B09 y AG-B05: estimar la exposición de sectores clientes a un corte de suministro (encadenamientos hacia delante).
- **Limitaciones:** Plausibilidad discutida (véase Oosterhaven, 1988, y Dietzenbacher, 1997).
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### MBM-0230 · Q 75 (B) — Value Added and Factors in Trade: A Comprehensive Approach

- **Autores:** Robert Stehrer; Neil Foster; Gaaitzen J. de Vries
- **Año:** 2012
- **Publicación o institución:** wiiw Working Paper n.º 80, Vienna Institute for International Economic Studies
- **Tipo de documento:** Documento de trabajo
- **Temática:** TMB-10 Análisis input-output y redes de cadena de suministro (principal) · secundarias: —
- **Calidad Q:** 75 (B) — Tipo 17/25 · Rigor 15/20 · Autoridad 12/15 · Vigencia 7/10 · Impacto 6/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** Página índice: https://www.usitc.gov/research_and_analysis/documents/AER_KWW3-17-2013_0.pdf (bibliografía)
- **Acceso y licencia:** Documento de trabajo abierto
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Tracing Value-Added and Double Counting in Gross Exports" Koopman Wang Wei 2014 "Measuring the Upstreamness of Production and Trade Flows" Antràs 2012 Timmer "An Illustrated User Guide to the World Input–Output Database"»; WebFetch: sí, versión USITC de Koopman, Wang y Wei (bibliografía))
- **Contenido:** Marco para medir el valor añadido y los factores (trabajo, capital) incorporados en el comercio con tablas input-output mundiales.
- **Uso en el Motor:** MC-B09: descomponer la exposición sectorial por factores y países.
- **Limitaciones:** Documento de trabajo.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

## TMB-11 Evaluación predictiva, calibración y backtesting de selección

#### DOC-MOT-0095 · Q 96 (A) — Strictly Proper Scoring Rules, Prediction, and Estimation

- **Autores:** Tilmann Gneiting; Adrian E. Raftery
- **Año:** 2007
- **Publicación o institución:** Journal of the American Statistical Association, 102, 359-378
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-11 Evaluación predictiva, calibración y backtesting de selección (principal) · secundarias: —
- **Calidad Q:** 96 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1198/016214506000001437 · https://en.wikipedia.org/wiki/Brier_score (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor; copia del autor en sites.stat.washington.edu
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Brier score" en.wikipedia.org»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Brier_score)
- **Contenido:** Teoría general de las reglas de puntuación estrictamente propias (Brier, logarítmica, CRPS, puntuaciones de energía e intervalos) y su uso para evaluar y estimar con pronósticos probabilísticos.
- **Uso en el Motor:** MC-B10: reglas de puntuación estrictamente propias para evaluar las probabilidades que emite el Bloque B (p. ej., que un candidato supere al índice sectorial).
- **Limitaciones:** Marco teórico; elegir la regla según el uso. El número de fascículo no se confirma (la fuente consultada lo transcribe de forma distinta a la semilla).
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-11) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0103 · Q 95 (A) — … and the Cross-Section of Expected Returns

- **Autores:** Campbell R. Harvey; Yan Liu; Heqing Zhu
- **Año:** 2016
- **Publicación o institución:** The Review of Financial Studies, 29(1), 5-68
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-11 Evaluación predictiva, calibración y backtesting de selección (principal) · secundarias: TMB-07
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1093/rfs/hhv059 · https://academicnewsletter.sufe.edu.cn/info/353765
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Harvey Liu Zhu "and the Cross-Section of Expected Returns" probability of backtest overfitting»; WebFetch: sí)
- **Contenido:** Recopila más de 300 factores publicados y aplica correcciones por pruebas múltiples; propone exigir t > 3 a los nuevos factores.
- **Uso en el Motor:** MC-B10 y MC-B07: umbrales de significación más exigentes (t > 3) al validar factores y criterios de cribado ante pruebas múltiples.
- **Limitaciones:** Umbral orientativo, dependiente del supuesto de pruebas no publicadas. Volumen/fascículo tomados de la semilla (la página leída solo mostraba revista, año, DOI y página inicial 5).
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-11) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0094 · Q 95 (A) — Approximately Normal Tests for Equal Predictive Accuracy in Nested Models

- **Autores:** Todd E. Clark; Kenneth D. West
- **Año:** 2007
- **Publicación o institución:** Journal of Econometrics, 138(1), 291-311 (versión previa: NBER Technical Working Paper 326, 2006)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-11 Evaluación predictiva, calibración y backtesting de selección (principal) · secundarias: —
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI WP: 10.3386/t0326 · https://www.nber.org/papers/t0326
- **Acceso y licencia:** Documento de trabajo NBER de acceso abierto; artículo de revista de pago
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Clark West 2007 "Approximately normal tests for equal predictive accuracy in nested models" Journal of Econometrics»; WebFetch: sí)
- **Contenido:** Ajusta el diferencial de error cuadrático para comparar un modelo con su versión anidada (p. ej., señal frente a paseo aleatorio) con valores críticos aproximadamente normales.
- **Uso en el Motor:** MC-B10: comparar un modelo de selección con otro que lo anida (p. ej., ranking con y sin una señal adicional).
- **Limitaciones:** Específico de pérdida cuadrática. Cita de revista confirmada en la bibliografía del paquete R pretest; el DOI de revista de la semilla no se ha visto y se retira.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-11) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0093 · Q 95 (A) — Tests of Conditional Predictive Ability

- **Autores:** Raffaella Giacomini; Halbert White
- **Año:** 2006
- **Publicación o institución:** Econometrica, 74(6), 1545-1578
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-11 Evaluación predictiva, calibración y backtesting de selección (principal) · secundarias: —
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1111/j.1468-0262.2006.00718.x · https://ideas.repec.org:443/a/ecm/emetrp/v74y2006i6p1545-1578.html
- **Acceso y licencia:** Artículo de pago en el editor; versiones de trabajo de 2003 en RePEc
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Giacomini White 2006 "Tests of Conditional Predictive Ability" Econometrica Clark West nested»; WebFetch: sí)
- **Contenido:** Contraste de capacidad predictiva condicional que compara métodos de pronóstico (modelo más ventana de estimación) y admite modelos anidados con ventanas móviles.
- **Uso en el Motor:** MC-B10: capacidad predictiva condicional; comparar métodos de pronóstico sectorial con ventanas móviles.
- **Limitaciones:** Requiere ventana de estimación limitada.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-11) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0099 · Q 95 (A) — A Reality Check for Data Snooping

- **Autores:** Halbert White
- **Año:** 2000
- **Publicación o institución:** Econometrica, 68(5), 1097-1126
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-11 Evaluación predictiva, calibración y backtesting de selección (principal) · secundarias: TMB-07
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1111/1468-0262.00152 · https://www.econometricsociety.org/publications/econometrica/2000/09/01/reality-check-data-snooping
- **Acceso y licencia:** Página de la Econometric Society (resumen abierto); texto completo para miembros o suscriptores
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «"Data dredging" wikipedia data snooping White reality check»; WebFetch: sí)
- **Contenido:** Contraste bootstrap de si el mejor de muchos modelos supera a una referencia, corrigiendo la búsqueda de especificaciones (data snooping).
- **Uso en el Motor:** MC-B10: corrección por fisgoneo de datos al elegir la mejor regla de cribado entre muchas probadas.
- **Limitaciones:** Conservador con modelos irrelevantes (véase Hansen 2005, DOC-MOT-0100).
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-11) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0091 · Q 95 (A) — Comparing Predictive Accuracy

- **Autores:** Francis X. Diebold; Roberto S. Mariano
- **Año:** 1995
- **Publicación o institución:** Journal of Business & Economic Statistics, 13(3), 253-263
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-11 Evaluación predictiva, calibración y backtesting de selección (principal) · secundarias: —
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1080/07350015.1995.10524599 · https://pkg.robjhyndman.com/forecast/reference/dm.test.html
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Diebold Mariano test wikipedia»; WebFetch: sí, sobre la página índice https://pkg.robjhyndman.com/forecast/reference/dm.test.html)
- **Contenido:** Propone el contraste DM de igualdad de precisión predictiva entre dos pronósticos con funciones de pérdida generales y errores autocorrelacionados.
- **Uso en el Motor:** MC-B10: test de Diebold-Mariano para comparar la precisión de dos pronósticos sectoriales (demanda, márgenes, rentabilidad relativa).
- **Limitaciones:** No válido para modelos anidados (usar Clark-West, DOC-MOT-0094). DOI confirmado en https://en.wikipedia.org/wiki/Mean_absolute_scaled_error.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-11) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0098 · Q 95 (A) — A New Vector Partition of the Probability Score

- **Autores:** Allan H. Murphy
- **Año:** 1973
- **Publicación o institución:** Journal of Applied Meteorology, 12(4), 595-600
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-11 Evaluación predictiva, calibración y backtesting de selección (principal) · secundarias: —
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI: 10.1175/1520-0450(1973)012<0595:ANVPOT>2.0.CO;2 · https://en.wikipedia.org/wiki/Brier_score (bibliografía)
- **Acceso y licencia:** Página del editor (AMS)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Brier score" en.wikipedia.org»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Brier_score)
- **Contenido:** Descompone la puntuación de Brier en fiabilidad (calibración), resolución e incertidumbre.
- **Uso en el Motor:** MC-B10: descomposición del Brier en fiabilidad, resolución e incertidumbre para diagnosticar las probabilidades del Bloque B.
- **Limitaciones:** Requiere agrupar probabilidades; sesgo en muestras pequeñas (véase DOC-MOT-0422).
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-11) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### MBM-0233 · Q 94 (A) — Probabilistic Forecasts, Calibration and Sharpness

- **Autores:** Tilmann Gneiting; Fadoua Balabdaoui; Adrian E. Raftery
- **Año:** 2007
- **Publicación o institución:** Journal of the Royal Statistical Society: Series B, vol. 69, n.º 2, págs. 243-268
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-11 Evaluación predictiva, calibración y backtesting de selección (principal) · secundarias: TMB-13
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1111/j.1467-9868.2007.00587.x · https://ideas.repec.org/a/bla/jorssb/v69y2007i2p243-268.html · Copia del autor: https://sites.stat.washington.edu/people/raftery/Research/PDF/Gneiting2007jrssb.pdf
- **Acceso y licencia:** Revista de pago; copia del autor abierta
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Gneiting Balabdaoui Raftery 2007 "Probabilistic forecasts, calibration and sharpness" Journal of the Royal Statistical Society Series B»; WebFetch: sí, ficha IDEAS/RePEc)
- **Contenido:** Paradigma de maximizar la nitidez sujeta a calibración; herramientas: histogramas PIT, gráficos de calibración marginal, diagramas de nitidez y reglas propias.
- **Uso en el Motor:** MC-B10: diagnóstico de las distribuciones de previsión del Bloque B (rangos de crecimiento, valor intrínseco) y elección de métrica.
- **Limitaciones:** Ejemplo en energía eólica.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### DOC-MOT-0097 · Q 94 (A) — Verification of Forecasts Expressed in Terms of Probability

- **Autores:** Glenn W. Brier
- **Año:** 1950
- **Publicación o institución:** Monthly Weather Review, 78(1), 1-3
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-11 Evaluación predictiva, calibración y backtesting de selección (principal) · secundarias: TMB-13
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI: 10.1175/1520-0493(1950)078<0001:VOFEIT>2.0.CO;2 · https://journals.ametsoc.org/view/journals/mwre/78/1/1520-0493_1950_078_0001_vofeit_2_0_co_2.xml
- **Acceso y licencia:** Página del editor (AMS); copia archivada de NOAA en web.archive.org
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Brier score" en.wikipedia.org»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Brier_score)
- **Contenido:** Define la puntuación de Brier (error cuadrático medio de las probabilidades) para verificar pronósticos probabilísticos de eventos categóricos.
- **Uso en el Motor:** MC-B10: puntuación de Brier para las previsiones probabilísticas del Bloque B y de los paneles de expertos (TMB-13).
- **Limitaciones:** Solo eventos binarios o categóricos.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-11) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0105 · Q 93 (A) — Another Look at Measures of Forecast Accuracy

- **Autores:** Rob J. Hyndman; Anne B. Koehler
- **Año:** 2006
- **Publicación o institución:** International Journal of Forecasting, 22(4), 679-688
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-11 Evaluación predictiva, calibración y backtesting de selección (principal) · secundarias: —
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1016/j.ijforecast.2006.03.001 · https://en.wikipedia.org/wiki/Mean_absolute_scaled_error (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Mean absolute scaled error" en.wikipedia.org Hyndman Koehler»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Mean_absolute_scaled_error)
- **Contenido:** Revisa las medidas de error de pronóstico, critica MAPE y medidas relativas, y propone el error absoluto medio escalado (MASE).
- **Uso en el Motor:** MC-B10: MASE y métricas escaladas para comparar errores de pronóstico entre sectores con escalas distintas.
- **Limitaciones:** Medidas puntuales, no probabilísticas.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-11) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0100 · Q 93 (A) — A Test for Superior Predictive Ability

- **Autores:** Peter Reinhard Hansen
- **Año:** 2005
- **Publicación o institución:** Journal of Business & Economic Statistics
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-11 Evaluación predictiva, calibración y backtesting de selección (principal) · secundarias: TMB-07
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** https://en.wikipedia.org/wiki/Peter_Reinhard_Hansen (lista de publicaciones)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Peter Reinhard Hansen IDEAS RePEc "A Test for Superior Predictive Ability"»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Peter_Reinhard_Hansen)
- **Contenido:** Contraste SPA: versión estudentizada y recentrada del Reality Check, más potente y menos sensible a modelos irrelevantes.
- **Uso en el Motor:** MC-B10: test SPA de Hansen para elegir entre muchas estrategias de selección sin sesgo de fisgoneo.
- **Limitaciones:** Requiere bootstrap estacionario. Solo se han confirmado autor, año, título y revista; volumen, páginas y DOI de la semilla quedan sin confirmar y se retiran.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-11) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0092 · Q 92 (A) — Testing the Equality of Prediction Mean Squared Errors

- **Autores:** David Harvey; Stephen Leybourne; Paul Newbold
- **Año:** 1997
- **Publicación o institución:** International Journal of Forecasting, 13(2), 281-291
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-11 Evaluación predictiva, calibración y backtesting de selección (principal) · secundarias: —
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** https://pkg.robjhyndman.com/forecast/reference/dm.test.html (bibliografía de la función dm.test)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Diebold Mariano test wikipedia»; WebFetch: sí, sobre la página índice https://pkg.robjhyndman.com/forecast/reference/dm.test.html)
- **Contenido:** Corrección de muestra pequeña del contraste DM y uso de la distribución t de Student.
- **Uso en el Motor:** MC-B10: corrección en muestras pequeñas del test de Diebold-Mariano.
- **Limitaciones:** Mismas limitaciones que DM. El DOI de la semilla no se ha visto en la verificación y se retira.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-11) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0426 · Q 89 (A) — Consistent Ranking of Volatility Models

- **Autores:** Peter Reinhard Hansen; Asger Lunde
- **Año:** 2006
- **Publicación o institución:** Journal of Econometrics, 131, 97-121
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-11 Evaluación predictiva, calibración y backtesting de selección (principal) · secundarias: TMB-09
- **Calidad Q:** 89 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** https://en.wikipedia.org/wiki/Peter_Reinhard_Hansen (lista de publicaciones)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Peter Reinhard Hansen IDEAS RePEc "A Test for Superior Predictive Ability"»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Peter_Reinhard_Hansen)
- **Contenido:** Muestra que, con proxies ruidosos de la volatilidad, algunas funciones de pérdida ordenan mal los modelos y caracteriza las que dan rankings consistentes.
- **Uso en el Motor:** MC-B10: funciones de pérdida robustas para clasificar modelos de volatilidad con proxies ruidosos.
- **Limitaciones:** Sin DOI en la fuente consultada.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-11) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0102 · Q 88 (A) — The Probability of Backtest Overfitting

- **Autores:** David H. Bailey; Jonathan M. Borwein; Marcos López de Prado; Qiji Jim Zhu
- **Año:** 2015 (versión SSRN revisada; publicación en Journal of Computational Finance)
- **Publicación o institución:** Journal of Computational Finance (Risk Journals); SSRN 2326253
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-11 Evaluación predictiva, calibración y backtesting de selección (principal) · secundarias: TMB-07
- **Calidad Q:** 88 (A) — Tipo 22/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 9/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI SSRN: 10.2139/ssrn.2326253 · https://papers.ssrn.com/abstract=2326253
- **Acceso y licencia:** Documento SSRN gratuito; artículo de revista de pago
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Harvey Liu Zhu "and the Cross-Section of Expected Returns" probability of backtest overfitting»; WebFetch: sí)
- **Contenido:** Define la probabilidad de sobreajuste del backtest (PBO) y la estima con validación cruzada simétrica combinatoria (CSCV).
- **Uso en el Motor:** MC-B10: probabilidad de sobreajuste del backtest (PBO, CSCV) en el ranking de candidatos y en las reglas de cribado.
- **Limitaciones:** Coste computacional. Volumen, páginas y DOI de revista de la semilla no confirmados (SSRN lo daba como «forthcoming»); se retiran.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-11) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0423 · Q 88 (A) — Comparing Predictive Accuracy, Twenty Years Later: A Personal Perspective on the Use and Abuse of Diebold-Mariano Tests

- **Autores:** Francis X. Diebold
- **Año:** 2015
- **Publicación o institución:** Journal of Business & Economic Statistics, 33(1), 1
- **Tipo de documento:** Artículo revisado por pares (con discusión)
- **Temática:** TMB-11 Evaluación predictiva, calibración y backtesting de selección (principal) · secundarias: —
- **Calidad Q:** 88 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.1080/07350015.2014.983236 · https://en.wikipedia.org/wiki/Mean_absolute_scaled_error (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Mean absolute scaled error" en.wikipedia.org Hyndman Koehler»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Mean_absolute_scaled_error)
- **Contenido:** El propio autor delimita el uso correcto del contraste DM (comparar pronósticos, no modelos) y advierte contra su abuso en la selección de modelos.
- **Uso en el Motor:** MC-B10: uso correcto y límites del test de Diebold-Mariano en comparaciones de modelos.
- **Limitaciones:** Ensayo de posición; las páginas finales no figuran en la fuente.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-11) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0104 · Q 88 (A) — The Statistics of Sharpe Ratios

- **Autores:** Andrew W. Lo
- **Año:** 2002
- **Publicación o institución:** Financial Analysts Journal, 58(4), 36-52
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-11 Evaluación predictiva, calibración y backtesting de selección (principal) · secundarias: —
- **Calidad Q:** 88 (A) — Tipo 22/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 9/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.2469/faj.v58.n4.2453 · https://en.wikipedia.org/wiki/Sharpe_ratio (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Sharpe ratio" en.wikipedia.org deflated Sharpe ratio»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Sharpe_ratio)
- **Contenido:** Deriva la distribución muestral del ratio de Sharpe con rentabilidades IID y autocorrelacionadas y muestra que la anualización por raíz del tiempo puede sesgarlo mucho.
- **Uso en el Motor:** MC-B10: error estándar del ratio de Sharpe con autocorrelación; intervalos para el Sharpe de una cesta de candidatos.
- **Limitaciones:** Supuestos asintóticos.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-11) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0416 · Q 88 (A) — Performance Hypothesis Testing with the Sharpe and Treynor Measures

- **Autores:** J. D. Jobson; Bob M. Korkie
- **Año:** 1981
- **Publicación o institución:** The Journal of Finance, 36(4), 888-908
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-11 Evaluación predictiva, calibración y backtesting de selección (principal) · secundarias: —
- **Calidad Q:** 88 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.1111/j.1540-6261.1981.tb04891.x · https://en.wikipedia.org/wiki/Sharpe_ratio (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Sharpe ratio" en.wikipedia.org deflated Sharpe ratio»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Sharpe_ratio)
- **Contenido:** Primer contraste formal de igualdad de ratios de Sharpe y Treynor entre dos carteras, con su distribución asintótica.
- **Uso en el Motor:** MC-B10: contraste de igualdad de ratios de Sharpe entre dos estrategias de selección.
- **Limitaciones:** Supone normalidad IID; véanse correcciones posteriores (Lo 2002, DOC-MOT-0104).
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-11) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0420 · Q 87 (A) — Sampling Distributions of the Brier Score and Brier Skill Score under Serial Dependence

- **Autores:** Daniel S. Wilks
- **Año:** 2010
- **Publicación o institución:** Quarterly Journal of the Royal Meteorological Society, 136, 2109-2118
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-11 Evaluación predictiva, calibración y backtesting de selección (principal) · secundarias: —
- **Calidad Q:** 87 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 7/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.1002/qj.709 · https://en.wikipedia.org/wiki/Brier_score (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Brier score" en.wikipedia.org»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Brier_score)
- **Contenido:** Deriva la varianza muestral del Brier y del Brier skill score cuando los pronósticos están autocorrelacionados, y muestra que ignorarlo exagera la significación.
- **Uso en el Motor:** MC-B10: distribución del Brier y del Brier Skill Score con dependencia serial; intervalos para la calibración del Bloque B.
- **Limitaciones:** Modelo de dependencia de primer orden.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-11) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0415 · Q 86 (A) — Pseudo-Mathematics and Financial Charlatanism: The Effects of Backtest Overfitting on Out-of-Sample Performance

- **Autores:** David H. Bailey; Jonathan M. Borwein; Marcos López de Prado (autoría según la bibliografía consultada)
- **Año:** 2014
- **Publicación o institución:** Notices of the American Mathematical Society, 61(5), 458-471
- **Tipo de documento:** Artículo revisado por pares (divulgación técnica)
- **Temática:** TMB-11 Evaluación predictiva, calibración y backtesting de selección (principal) · secundarias: TMB-14
- **Calidad Q:** 86 (A) — Tipo 22/25 · Rigor 14/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 9/10 · Acceso 9/10
- **DOI / ISBN / URL:** https://en.wikipedia.org/wiki/Deflated_Sharpe_ratio (bibliografía)
- **Acceso y licencia:** Acceso abierto en la revista de la AMS
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Sharpe ratio" en.wikipedia.org deflated Sharpe ratio»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Deflated_Sharpe_ratio)
- **Contenido:** Muestra que, con pocas observaciones y muchas configuraciones probadas, es casi seguro encontrar un backtest con Sharpe alto sin capacidad predictiva, y propone la longitud mínima de backtest.
- **Uso en el Motor:** MC-B10: efectos del sobreajuste del backtest sobre el rendimiento fuera de muestra; regla de número mínimo de datos.
- **Limitaciones:** Texto divulgativo; resultados bajo supuestos simplificados.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-11) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0427 · Q 85 (A) — A Novel Approach to Predictive Accuracy Testing in Nested Environments

- **Autores:** Jean-Yves Pitarakis
- **Año:** 2023
- **Publicación o institución:** Econometric Theory (Cambridge University Press), publicado en línea
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-11 Evaluación predictiva, calibración y backtesting de selección (principal) · secundarias: —
- **Calidad Q:** 85 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 4/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1017/S0266466623000154 · https://resolve.cambridge.org/core/services/aop-cambridge-core/content/view/0B4D706CDA6D4A2C883C3BDF397DCB18/S0266466623000154a.pdf/a-novel-approach-to-predictive-accuracy-testing-in-nested-environments.pdf
- **Acceso y licencia:** PDF en Cambridge Core (acceso según licencia); implementado en el paquete R pretest
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Clark West 2007 "Approximately normal tests for equal predictive accuracy in nested models" Journal of Econometrics»; WebFetch: sí, sobre la página índice https://cran.r-universe.dev/pretest/doc/manual.html)
- **Contenido:** Propone estadísticos de precisión predictiva para modelos anidados con distribución normal estándar que evitan la degeneración del contraste en el nulo.
- **Uso en el Motor:** MC-B10: alternativa para contrastes de precisión en modelos anidados.
- **Limitaciones:** Reciente, poca adopción; volumen y páginas no confirmados.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-11) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0101 · Q 85 (A) — The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting, and Non-Normality

- **Autores:** David H. Bailey; Marcos López de Prado
- **Año:** 2014
- **Publicación o institución:** The Journal of Portfolio Management, 40(5), 94-107
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-11 Evaluación predictiva, calibración y backtesting de selección (principal) · secundarias: TMB-07
- **Calidad Q:** 85 (A) — Tipo 22/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 8/10 · Acceso 5/10
- **DOI / ISBN / URL:** https://en.wikipedia.org/wiki/Deflated_Sharpe_ratio (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Sharpe ratio" en.wikipedia.org deflated Sharpe ratio»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Deflated_Sharpe_ratio)
- **Contenido:** Ajusta el Sharpe observado por el número de estrategias probadas, la asimetría y la curtosis para estimar la probabilidad de que el Sharpe verdadero sea positivo.
- **Uso en el Motor:** MC-B10: Sharpe deflactado para corregir por número de pruebas y no normalidad al validar la selección de candidatos.
- **Limitaciones:** Requiere estimar el número efectivo de ensayos. El DOI de la semilla no se ha visto en la verificación y se retira.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-11) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0421 · Q 85 (A) — Scoring Rules for Forecast Verification

- **Autores:** Riccardo Benedetti
- **Año:** 2010
- **Publicación o institución:** Monthly Weather Review, 138(1), 203-211
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-11 Evaluación predictiva, calibración y backtesting de selección (principal) · secundarias: —
- **Calidad Q:** 85 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 12/15 · Vigencia 10/10 · Impacto 6/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1175/2009MWR2945.1 · https://en.wikipedia.org/wiki/Brier_score (bibliografía)
- **Acceso y licencia:** Página del editor (AMS)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Brier score" en.wikipedia.org»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Brier_score)
- **Contenido:** Caracteriza axiomáticamente las reglas de puntuación aceptables para verificar pronósticos probabilísticos y defiende la puntuación logarítmica.
- **Uso en el Motor:** MC-B10: revisión de reglas de puntuación para elegir la métrica de evaluación según el tipo de pronóstico.
- **Limitaciones:** Enfoque axiomático; no trata pronósticos continuos.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-11) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0422 · Q 83 (A) — A Bias-Corrected Decomposition of the Brier Score

- **Autores:** Christopher A. T. Ferro; Thomas E. Fricker
- **Año:** 2012
- **Publicación o institución:** Quarterly Journal of the Royal Meteorological Society, 138(668), 1954-1960
- **Tipo de documento:** Artículo revisado por pares (nota)
- **Temática:** TMB-11 Evaluación predictiva, calibración y backtesting de selección (principal) · secundarias: —
- **Calidad Q:** 83 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 12/15 · Vigencia 10/10 · Impacto 6/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** https://en.wikipedia.org/wiki/Brier_score (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Brier score" en.wikipedia.org»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Brier_score)
- **Contenido:** Corrige el sesgo de muestra finita de la descomposición de Murphy en fiabilidad y resolución.
- **Uso en el Motor:** MC-B10: descomposición del Brier corregida por sesgo en muestras pequeñas de previsiones sectoriales.
- **Limitaciones:** Sin DOI en la fuente consultada.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-11) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0425 · Q 82 (A) — A Note on the Mean Absolute Scaled Error

- **Autores:** Philip Hans Franses
- **Año:** 2016
- **Publicación o institución:** International Journal of Forecasting, 32(1), 20-22
- **Tipo de documento:** Artículo revisado por pares (nota)
- **Temática:** TMB-11 Evaluación predictiva, calibración y backtesting de selección (principal) · secundarias: —
- **Calidad Q:** 82 (A) — Tipo 23/25 · Rigor 13/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 5/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI: 10.1016/j.ijforecast.2015.03.008 · https://en.wikipedia.org/wiki/Mean_absolute_scaled_error (bibliografía; handle 1765/78815)
- **Acceso y licencia:** Artículo de pago; copia en repositorio institucional (hdl 1765/78815)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Mean absolute scaled error" en.wikipedia.org Hyndman Koehler»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Mean_absolute_scaled_error)
- **Contenido:** Muestra que el MASE se puede interpretar como contraste frente al pronóstico ingenuo y comenta sus propiedades.
- **Uso en el Motor:** MC-B10: nota técnica sobre el MASE.
- **Limitaciones:** Nota breve.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-11) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0418 · Q 82 (A) — The Sharpe Ratio Efficient Frontier

- **Autores:** David H. Bailey; Marcos López de Prado
- **Año:** 2012
- **Publicación o institución:** Journal of Risk, 15(2) (SSRN 1821643)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-11 Evaluación predictiva, calibración y backtesting de selección (principal) · secundarias: —
- **Calidad Q:** 82 (A) — Tipo 22/25 · Rigor 15/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 7/10 · Independencia 8/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.21314/JOR.2012.255 · https://en.wikipedia.org/wiki/Deflated_Sharpe_ratio (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor; versión SSRN gratuita
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Sharpe ratio" en.wikipedia.org deflated Sharpe ratio»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Deflated_Sharpe_ratio)
- **Contenido:** Introduce el ratio de Sharpe probabilístico (PSR) y la longitud mínima de registro necesaria para confiar en un Sharpe dado con rentabilidades no normales.
- **Uso en el Motor:** MC-B10: frontera eficiente del Sharpe para valorar si el mejor resultado de varias pruebas es significativo.
- **Limitaciones:** Supuestos de estacionariedad e independencia aproximada.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-11) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0424 · Q 81 (A) — Accuracy Measures: Theoretical and Practical Concerns

- **Autores:** Spyros Makridakis
- **Año:** 1993
- **Publicación o institución:** International Journal of Forecasting, 9(4), 527-529
- **Tipo de documento:** Artículo revisado por pares (nota)
- **Temática:** TMB-11 Evaluación predictiva, calibración y backtesting de selección (principal) · secundarias: —
- **Calidad Q:** 81 (A) — Tipo 23/25 · Rigor 12/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.1016/0169-2070(93)90079-3 · https://en.wikipedia.org/wiki/Mean_absolute_scaled_error (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Mean absolute scaled error" en.wikipedia.org Hyndman Koehler»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Mean_absolute_scaled_error)
- **Contenido:** Discute las propiedades y sesgos de las medidas de precisión (MAPE simétrico, asimetrías) y su elección práctica.
- **Uso en el Motor:** MC-B10: problemas prácticos de las métricas de precisión al comparar pronósticos de demanda sectorial.
- **Limitaciones:** Nota breve, superada en parte por Hyndman-Koehler (DOC-MOT-0105).
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-11) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0419 · Q 78 (B) — Detection of False Investment Strategies Using Unsupervised Learning Methods

- **Autores:** Marcos López de Prado; Michael J. Lewis
- **Año:** 2019
- **Publicación o institución:** Quantitative Finance, 19(9), 1555-1565
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-11 Evaluación predictiva, calibración y backtesting de selección (principal) · secundarias: TMB-12
- **Calidad Q:** 78 (B) — Tipo 22/25 · Rigor 14/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 6/10 · Independencia 8/10 · Acceso 5/10
- **DOI / ISBN / URL:** https://en.wikipedia.org/wiki/Deflated_Sharpe_ratio (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Sharpe ratio" en.wikipedia.org deflated Sharpe ratio»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Deflated_Sharpe_ratio)
- **Contenido:** Estima el número efectivo de ensayos independientes agrupando estrategias probadas, para aplicar después el Sharpe deflactado.
- **Uso en el Motor:** MC-B10: detección de estrategias falsas mediante agrupamiento de pruebas (número efectivo de ensayos).
- **Limitaciones:** Depende del algoritmo de agrupamiento elegido.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-11) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### MBM-0234 · Q 78 (B) — Evaluating Density Forecasts: Forecast Combinations, Model Mixtures, Calibration and Sharpness

- **Autores:** James Mitchell; Kenneth F. Wallis
- **Año:** 2008
- **Publicación o institución:** NIESR Discussion Paper n.º 320
- **Tipo de documento:** Documento de trabajo
- **Temática:** TMB-11 Evaluación predictiva, calibración y backtesting de selección (principal) · secundarias: TMB-13
- **Calidad Q:** 78 (B) — Tipo 17/25 · Rigor 16/20 · Autoridad 13/15 · Vigencia 7/10 · Impacto 7/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** https://www.niesr.ac.uk/publications/evaluating-density-forecasts-forecast-combinations-model-mixtures-calibration-and-sharpness · https://econpapers.repec.org/paper/nsrniesrd/320.htm
- **Acceso y licencia:** Acceso abierto
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Gneiting Balabdaoui Raftery 2007 "Probabilistic forecasts, calibration and sharpness" Journal of the Royal Statistical Society Series B»; WebFetch: sí, página del NIESR)
- **Contenido:** Réplica a Gneiting et al. (2007): con ejemplos realistas de series temporales, los métodos de calibración existentes discriminan entre previsiones y no hace falta un criterio aparte de nitidez.
- **Uso en el Motor:** MC-B10: contrapunto metodológico al evaluar previsiones de densidad combinadas del Bloque B.
- **Limitaciones:** Documento de trabajo.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### DOC-MOT-0417 · Q 76 (B) — Being Honest in Backtest Reporting: A Template for Disclosing Multiple Tests

- **Autores:** Frank J. Fabozzi; Marcos López de Prado
- **Año:** 2018
- **Publicación o institución:** The Journal of Portfolio Management, 45(1), 141-147
- **Tipo de documento:** Artículo revisado por pares (profesional)
- **Temática:** TMB-11 Evaluación predictiva, calibración y backtesting de selección (principal) · secundarias: TMB-14
- **Calidad Q:** 76 (B) — Tipo 22/25 · Rigor 12/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 6/10 · Independencia 8/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.3905/jpm.2018.45.1.141 · https://en.wikipedia.org/wiki/Deflated_Sharpe_ratio (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Sharpe ratio" en.wikipedia.org deflated Sharpe ratio»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Deflated_Sharpe_ratio)
- **Contenido:** Propone una plantilla para declarar el número de pruebas, su correlación y el Sharpe deflactado al presentar un backtest.
- **Uso en el Motor:** MC-B10 y TMB-14: plantilla para declarar todas las pruebas realizadas en el backtest de selección.
- **Limitaciones:** Propuesta normativa sin validación empírica.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-11) el 2026-11-02 con su ID original; Temática y Uso adaptados.

## TMB-12 Aprendizaje automático y análisis de texto para mercados

#### FXM-0271 · Q 97 (A) — Text as Data

- **Autores:** Matthew Gentzkow; Bryan Kelly; Matt Taddy
- **Año:** 2019
- **Publicación o institución:** Journal of Economic Literature, vol. 57, n.º 3, págs. 535-574 (NBER Working Paper 23276)
- **Tipo de documento:** Artículo de revisión revisado por pares
- **Temática:** TMB-12 Aprendizaje automático y análisis de texto para mercados (principal) · secundarias: TMB-14
- **Calidad Q:** 97 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** DOI: 10.1257/jel.20181020 · https://ideas.repec.org/a/aea/jeclit/v57y2019i3p535-74.html · Versión abierta: https://web.stanford.edu/%7Egentzkow/research/text-as-data.pdf
- **Acceso y licencia:** Revista por suscripción (AEA); versión de trabajo abierta
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Gentzkow Kelly Taddy "Text as Data" Journal of Economic Literature 2019»; WebFetch: sí, ficha IDEAS)
- **Contenido:** Guía de referencia del texto como dato en economía: representación (bolsas de palabras, embeddings), métodos estadísticos (diccionarios, regresión penalizada, modelos de temas) y aplicaciones.
- **Uso en el Motor:** AG-B10 y MC-B07: marco para convertir texto (informes 10-K, noticias, transcripciones) en variables sectoriales y señales de candidatos.
- **Limitaciones:** No específico de divisas.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02. Reutilizada en F8 del Bloque B V2.0 (TMB-12) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0086 · Q 95 (A) — Empirical Asset Pricing via Machine Learning

- **Autores:** Shihao Gu; Bryan Kelly; Dacheng Xiu
- **Año:** 2020
- **Publicación o institución:** The Review of Financial Studies, 33(5), 2223-2273 (versión previa: NBER Working Paper 25398, 2018, rev. 2019)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-12 Aprendizaje automático y análisis de texto para mercados (principal) · secundarias: TMB-07
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1093/rfs/hhaa009 · https://nber.org/papers/w25398
- **Acceso y licencia:** Artículo de revista de pago; documento de trabajo NBER de acceso abierto (DOI WP: 10.3386/w25398)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Gu Kelly Xiu 2020 "Empirical Asset Pricing via Machine Learning" Review of Financial Studies»; WebFetch: sí)
- **Contenido:** Compara regresiones penalizadas, componentes principales, árboles potenciados, bosques aleatorios y redes neuronales para predecir rentabilidades de acciones de EE. UU.; árboles y redes superan con claridad a los modelos lineales, con variables de momentum, liquidez y volatilidad como predictores dominantes.
- **Uso en el Motor:** MC-B07 y AG-B12: aprendizaje automático para la sección cruzada de rendimientos; base para rankings no lineales de candidatos.
- **Limitaciones:** Universo estadounidense; costes de implementación y de rotación no centrales.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-12) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### MBM-0235 · Q 94 (A) — When Is a Liability Not a Liability? Textual Analysis, Dictionaries, and 10-Ks

- **Autores:** Tim Loughran; Bill McDonald
- **Año:** 2011
- **Publicación o institución:** Journal of Finance (versión SSRN de 2010, «forthcoming»)
- **Tipo de documento:** Artículo revisado por pares (revista de primer nivel)
- **Temática:** TMB-12 Aprendizaje automático y análisis de texto para mercados (principal) · secundarias: TMB-14
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** https://papers.ssrn.com/abstract=1331573
- **Acceso y licencia:** Versión de trabajo en SSRN; revista de pago
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Loughran McDonald "Textual Analysis in Accounting and Finance: A Survey" 2016 Journal of Accounting Research "When Is a Liability Not a Liability"»; WebFetch: sí, ficha SSRN)
- **Contenido:** Muestra que el diccionario Harvard clasifica mal el vocabulario financiero y construye listas específicas (negativas, positivas, incertidumbre, litigio…) para informes 10-K.
- **Uso en el Motor:** AG-B10 y MC-B07: diccionario de referencia para medir tono y riesgo en informes anuales, transcripciones y noticias de candidatos.
- **Limitaciones:** Calibrado en 10-K estadounidenses en inglés.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### DOC-MOT-0087 · Q 94 (A) — Random Forests

- **Autores:** Leo Breiman
- **Año:** 2001
- **Publicación o institución:** Machine Learning, 45(1), 5-32
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-12 Aprendizaje automático y análisis de texto para mercados (principal) · secundarias: —
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1023/A:1010933404324 · https://mlanthology.org/mlj/2001/breiman2001mlj-random
- **Acceso y licencia:** Artículo de pago en el editor (Springer); ficha bibliográfica abierta
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Breiman 2001 "Random Forests" Machine Learning 45 5-32»; WebFetch: sí)
- **Contenido:** Define los bosques aleatorios (agregación de árboles con remuestreo y selección aleatoria de variables), su error fuera de bolsa y la importancia de variables por permutación.
- **Uso en el Motor:** MC-B07: bosques aleatorios para clasificar candidatos y medir importancia de variables en el cribado.
- **Limitaciones:** Importancia de variables sesgada con predictores correlacionados; el error fuera de bolsa no respeta la dependencia temporal.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-12) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0400 · Q 94 (A) — Greedy Function Approximation: A Gradient Boosting Machine

- **Autores:** Jerome H. Friedman
- **Año:** 2001
- **Publicación o institución:** The Annals of Statistics, 29(5), 1189-1232
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-12 Aprendizaje automático y análisis de texto para mercados (principal) · secundarias: —
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.1214/aos/1013203451 · https://projecteuclid.org/euclid.aos/1013203451
- **Acceso y licencia:** Página del editor (Project Euclid) con resumen abierto; texto completo según suscripción
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Friedman 2001 "Greedy function approximation: A gradient boosting machine" Annals of Statistics»; WebFetch: sí)
- **Contenido:** Formula el boosting como descenso de gradiente en el espacio de funciones con pérdidas arbitrarias (cuadrática, absoluta, Huber, logística) y árboles de regresión como aprendices base; introduce la contracción (shrinkage) y los gráficos de dependencia parcial.
- **Uso en el Motor:** MC-B07: potenciación de gradiente para modelos de puntuación de candidatos.
- **Limitaciones:** Marco general; no aborda dependencia temporal ni no estacionariedad de datos financieros.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-12) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0401 · Q 94 (A) — Regression Shrinkage and Selection via the Lasso

- **Autores:** Robert Tibshirani
- **Año:** 1996
- **Publicación o institución:** Journal of the Royal Statistical Society, Series B (Methodological), 58(1), 267-288
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-12 Aprendizaje automático y análisis de texto para mercados (principal) · secundarias: TMB-07
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1111/j.2517-6161.1996.tb02080.x · https://academicnewsletter.sufe.edu.cn/info/442374
- **Acceso y licencia:** Artículo de pago en el editor; copias docentes en abierto (p. ej., sites.stat.washington.edu)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Tibshirani 1996 "Regression shrinkage and selection via the lasso" Journal of the Royal Statistical Society Series B»; WebFetch: sí)
- **Contenido:** Propone el lasso: mínimos cuadrados con restricción en la norma L1 de los coeficientes, que contrae y anula coeficientes y realiza selección de variables continua.
- **Uso en el Motor:** MC-B07 y MC-B05: lasso para seleccionar variables sectoriales y señales con muchas candidatas.
- **Limitaciones:** Selección inestable con predictores muy correlacionados (véase elastic net, DOC-MOT-0402); el número de volumen se toma de la cita estándar, la página leída solo mostraba páginas y DOI.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-12) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### MBM-0238 · Q 93 (A) — Text-Based Network Industries and Endogenous Product Differentiation

- **Autores:** Gerard Hoberg; Gordon Phillips
- **Año:** 2016
- **Publicación o institución:** Journal of Political Economy, vol. 124, n.º 5, págs. 1423-1465
- **Tipo de documento:** Artículo revisado por pares (revista de primer nivel)
- **Temática:** TMB-12 Aprendizaje automático y análisis de texto para mercados (principal) · secundarias: TMB-04
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1086/688176 · https://ideas.repec.org/a/ucp/jpolec/doi10.1086-688176.html · NBER WP 15991: https://www.nber.org/papers/w15991
- **Acceso y licencia:** Revista de pago; documento de trabajo NBER
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Hoberg Phillips "Text-Based Network Industries and Endogenous Product Differentiation" Journal of Political Economy 2016»; WebFetch: sí, ficha IDEAS/RePEc)
- **Contenido:** Usa la similitud textual de las descripciones de producto de los 10-K para crear clasificaciones sectoriales anuales en las que cada empresa tiene su propio conjunto de competidores (TNIC).
- **Uso en el Motor:** AG-B03 y MC-B07: definir el universo de comparables y competidores de un candidato y medir pureza de exposición temática con texto.
- **Limitaciones:** Limitado a empresas con 10-K.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### DOC-MOT-0413 · Q 93 (A) — Statistical Learning and Selective Inference

- **Autores:** Jonathan Taylor; Robert J. Tibshirani
- **Año:** 2015
- **Publicación o institución:** Proceedings of the National Academy of Sciences, 112(25), 7629-7634
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-12 Aprendizaje automático y análisis de texto para mercados (principal) · secundarias: TMB-11
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** DOI: 10.1073/pnas.1507583112 · https://en.wikipedia.org/wiki/Data_dredging (bibliografía)
- **Acceso y licencia:** Acceso abierto en PMC (PMC4485109)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Data dredging" wikipedia data snooping White reality check»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Data_dredging)
- **Contenido:** Presenta la inferencia selectiva: intervalos y p-valores válidos después de haber elegido el modelo con los mismos datos (p. ej., tras el lasso o la regresión por pasos).
- **Uso en el Motor:** MC-B10: inferencia tras selección de variables; evita sobrevalorar señales elegidas por los datos.
- **Limitaciones:** Supuestos gaussianos en la versión básica; implementación no trivial con datos dependientes.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-12) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0084 · Q 93 (A) — The Elements of Statistical Learning (2.ª ed.)

- **Autores:** Trevor Hastie; Robert Tibshirani; Jerome Friedman
- **Año:** 2009
- **Publicación o institución:** Springer (PDF gratuito de los autores en la Universidad de Stanford)
- **Tipo de documento:** Manual de referencia
- **Temática:** TMB-12 Aprendizaje automático y análisis de texto para mercados (principal) · secundarias: —
- **Calidad Q:** 93 (A) — Tipo 20/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://web.stanford.edu/~hastie/Papers/ESLII.pdf
- **Acceso y licencia:** PDF completo de acceso gratuito publicado por los autores; edición impresa de pago (Springer)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Hastie Tibshirani Friedman "The Elements of Statistical Learning" second edition pdf stanford»; WebFetch: no)
- **Contenido:** Manual de referencia del aprendizaje estadístico: regularización, árboles, boosting, métodos kernel, validación cruzada y descomposición sesgo-varianza.
- **Uso en el Motor:** MC-B07: manual de referencia de aprendizaje estadístico (regularización, árboles, validación cruzada).
- **Limitaciones:** Sin tratamiento específico de datos financieros dependientes ni de validación temporal. El DOI del libro que figuraba en la semilla no se ha visto en la verificación y se retira de la ficha.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-12) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0402 · Q 93 (A) — Regularization and Variable Selection via the Elastic Net

- **Autores:** Hui Zou; Trevor Hastie
- **Año:** 2005
- **Publicación o institución:** Journal of the Royal Statistical Society, Series B (Statistical Methodology), 67(2), 301-320
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-12 Aprendizaje automático y análisis de texto para mercados (principal) · secundarias: —
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.1111/j.1467-9868.2005.00503.x · https://ideas.repec.org/a/bla/jorssb/v67y2005i2p301-320.html
- **Acceso y licencia:** Artículo de pago en el editor; ficha abierta en RePEc y copia docente en sites.stat.washington.edu
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Zou Hastie 2005 "Regularization and variable selection via the elastic net" JRSS B»; WebFetch: sí)
- **Contenido:** Combina penalizaciones L1 y L2 para seleccionar variables agrupando predictores correlacionados y funcionar cuando hay más variables que observaciones.
- **Uso en el Motor:** MC-B07: red elástica para señales correlacionadas (p. ej., métricas de rentabilidad y calidad).
- **Limitaciones:** Dos hiperparámetros a ajustar con validación respetuosa del orden temporal; existe una corrección publicada por los autores (web.stanford.edu).
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-12) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0403 · Q 92 (A) — Characteristics Are Covariances: A Unified Model of Risk and Return

- **Autores:** Bryan T. Kelly; Seth Pruitt; Yinan Su
- **Año:** 2019
- **Publicación o institución:** Journal of Financial Economics, 134(3), 501-524 (versión previa: NBER Working Paper 24540)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-12 Aprendizaje automático y análisis de texto para mercados (principal) · secundarias: TMB-07
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1016/j.jfineco.2019.05.001 · https://ideas.repec.org/a/eee/jfinec/v134y2019i3p501-524.html
- **Acceso y licencia:** Artículo de pago; documento de trabajo NBER w24540 disponible
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Kelly Pruitt Su 2019 "Characteristics are covariances: A unified model of risk and return" Journal of Financial Economics»; WebFetch: sí)
- **Contenido:** Introduce el análisis de componentes principales instrumentado (IPCA): factores latentes con cargas variables en el tiempo que dependen de características observables; cinco factores IPCA explican mejor las rentabilidades medias que los modelos factoriales habituales.
- **Uso en el Motor:** MC-B07: modelo IPCA que liga características y covarianzas; factores latentes para clasificar candidatos.
- **Limitaciones:** Estimación por mínimos cuadrados alternos; universo de acciones de EE. UU.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-12) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### MBM-0239 · Q 92 (A) — Giving Content to Investor Sentiment: The Role of Media in the Stock Market

- **Autores:** Paul C. Tetlock
- **Año:** 2007
- **Publicación o institución:** Journal of Finance
- **Tipo de documento:** Artículo revisado por pares (revista de primer nivel)
- **Temática:** TMB-12 Aprendizaje automático y análisis de texto para mercados (principal) · secundarias: TMB-11
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** https://www.columbia.edu/~pt2238/papers/Tetlock_Media_Sentiment_JF.pdf · SSRN: https://papers.ssrn.com/abstract=685145
- **Acceso y licencia:** Copia del autor abierta; revista de pago
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Tetlock 2007 "Giving Content to Investor Sentiment: The Role of Media in the Stock Market" Journal of Finance ideas.repec»; WebFetch: sí, PDF del autor)
- **Contenido:** Con el General Inquirer aplicado a una columna del Wall Street Journal (1984-1999) muestra que el pesimismo mediático anticipa caídas de precios seguidas de reversión.
- **Uso en el Motor:** AG-B10: referencia para tratar el tono de prensa como sentimiento con efecto transitorio en sectores y candidatos.
- **Limitaciones:** Una sola columna y un diccionario general.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### DOC-MOT-0404 · Q 91 (A) — The Virtue of Complexity in Return Prediction

- **Autores:** Bryan T. Kelly; Semyon Malamud; Kangying Zhou
- **Año:** 2024
- **Publicación o institución:** The Journal of Finance, 79(1), 459-503
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-12 Aprendizaje automático y análisis de texto para mercados (principal) · secundarias: —
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 9/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1111/jofi.13298 · https://www.sfi.ch/en/publications/the-virtue-of-complexity-in-return-prediction
- **Acceso y licencia:** Artículo de pago; copia del artículo publicada en economics.yale.edu
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Kelly Malamud Zhou "The Virtue of Complexity in Return Prediction" Journal of Finance»; WebFetch: sí)
- **Contenido:** Demuestra teórica y empíricamente que modelos de predicción con más parámetros que observaciones (regresiones de características aleatorias con contracción) pueden mejorar el rendimiento fuera de muestra y el Sharpe de la estrategia de market timing.
- **Uso en el Motor:** MC-B07: argumento y límites de los modelos complejos en predicción de rendimientos.
- **Limitaciones:** Resultado debatido en la literatura posterior; sensible a la normalización y a la elección de la penalización; uno de los autores trabaja en la industria (AQR).
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-12) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0405 · Q 90 (A) — Financial Machine Learning

- **Autores:** Bryan T. Kelly; Dacheng Xiu
- **Año:** 2023
- **Publicación o institución:** Foundations and Trends in Finance, 13(3-4), 205-363 (también NBER Working Paper 31502)
- **Tipo de documento:** Artículo de revisión (monografía)
- **Temática:** TMB-12 Aprendizaje automático y análisis de texto para mercados (principal) · secundarias: —
- **Calidad Q:** 90 (A) — Tipo 22/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 9/10 · Acceso 9/10
- **DOI / ISBN / URL:** DOI: 10.3386/w31502 · https://www.nber.org/papers/w31502
- **Acceso y licencia:** Documento de trabajo NBER y versión SSRN de acceso abierto
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Kelly Xiu "Financial Machine Learning" Foundations and Trends in Finance 2023»; WebFetch: sí)
- **Contenido:** Revisión sistemática del aprendizaje automático en finanzas: predicción de rentabilidades, modelos factoriales con aprendizaje, optimización de carteras, texto y datos alternativos, con orientaciones de investigación.
- **Uso en el Motor:** MC-B07: panorama del aprendizaje automático financiero (texto, predicción, carteras) para el Motor de Mercados.
- **Limitaciones:** Sesgo hacia la investigación de los propios autores; aplicaciones centradas en renta variable estadounidense.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-12) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### FXM-0273 · Q 90 (A) — Measuring News Sentiment

- **Autores:** Adam Hale Shapiro; Moritz Sudhof; Daniel J. Wilson
- **Año:** 2017
- **Publicación o institución:** Federal Reserve Bank of San Francisco Working Paper 2017-01; versión de revista enlazada en ScienceDirect (pii S0304407620303535)
- **Tipo de documento:** Documento de trabajo (con versión de revista)
- **Temática:** TMB-12 Aprendizaje automático y análisis de texto para mercados (principal) · secundarias: —
- **Calidad Q:** 90 (A) — Tipo 22/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** https://www.frbsf.org/research-and-insights/publications/system-research-san-francisco-fed/2024/06/measuring-news-sentiment-eern · https://www.frbsf.org/wp-content/uploads/wp2017-01.pdf
- **Acceso y licencia:** Acceso abierto (Fed de San Francisco)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Shapiro Wilson "Taking the Fed at its Word" Review of Economic Studies; Shapiro Sudhof Wilson "Measuring news sentiment" Journal of Econometrics»; WebFetch: sí, página de la Fed de San Francisco)
- **Contenido:** Construye un índice diario de sentimiento económico a partir de noticias (1980-2015), compara modelos de análisis de sentimiento con valoraciones humanas y propone un léxico específico de noticias económicas.
- **Uso en el Motor:** AG-B10: índice de sentimiento de noticias económicas como variable de sentimiento sectorial y macro.
- **Limitaciones:** Noticias de EE. UU.; datos de la versión de revista (revista, volumen, páginas) no vistos.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02. Reutilizada en F8 del Bloque B V2.0 (TMB-12) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0412 · Q 90 (A) — A Unified View of Performance Metrics: Translating Threshold Choice into Expected Classification Loss

- **Autores:** José Hernández-Orallo; Peter A. Flach; César Ferri
- **Año:** 2012
- **Publicación o institución:** Journal of Machine Learning Research, 13, 2813-2869
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-12 Aprendizaje automático y análisis de texto para mercados (principal) · secundarias: TMB-11
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 6/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** http://jmlr.org/papers/volume13/hernandez-orallo12a/hernandez-orallo12a.pdf
- **Acceso y licencia:** Acceso abierto (JMLR)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Brier score" en.wikipedia.org»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Brier_score)
- **Contenido:** Demuestra que métricas como el Brier, el AUC o la exactitud son pérdidas de clasificación esperadas bajo distintas reglas de elección de umbral, lo que unifica la evaluación de clasificadores probabilísticos.
- **Uso en el Motor:** MC-B10: relación entre umbral de decisión y pérdida esperada en clasificadores de candidatos.
- **Limitaciones:** Marco teórico; requiere conocer la política de umbrales del usuario final.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-12) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### MBM-0237 · Q 89 (A) — Predicting Returns with Text Data

- **Autores:** Zheng Tracy Ke; Bryan Kelly; Dacheng Xiu
- **Año:** 2019 (rev. 2020)
- **Publicación o institución:** NBER Working Paper n.º 26186
- **Tipo de documento:** Documento de trabajo (NBER)
- **Temática:** TMB-12 Aprendizaje automático y análisis de texto para mercados (principal) · secundarias: TMB-07
- **Calidad Q:** 89 (A) — Tipo 19/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** https://www.nber.org/papers/w26186 · https://ideas.repec.org/p/nbr/nberwo/26186.html · PDF: https://www.nottingham.ac.uk/economics/documents/seminar-papers/senior/2020/xiu-18-11-20.pdf
- **Acceso y licencia:** Acceso abierto (versión de seminario); NBER
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Ke Kelly Xiu "Predicting Returns with Text Data" NBER working paper»; WebFetch: sí, PDF de la versión de octubre de 2020)
- **Contenido:** Método supervisado (SESTM) que aprende de los propios datos qué palabras predicen rendimientos y construye una puntuación de sentimiento de noticias.
- **Uso en el Motor:** AG-B10 y MC-B07: señal de sentimiento de noticias por candidato con vocabulario aprendido, alternativa a los diccionarios.
- **Limitaciones:** Requiere corpus grande de noticias con marca temporal precisa.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### DOC-MOT-0090 · Q 89 (A) — On Calibration of Modern Neural Networks

- **Autores:** Chuan Guo; Geoff Pleiss; Yu Sun; Kilian Q. Weinberger
- **Año:** 2017
- **Publicación o institución:** Proceedings of the 34th International Conference on Machine Learning (ICML 2017), PMLR 70, 1321-1330
- **Tipo de documento:** Comunicación de congreso revisada por pares
- **Temática:** TMB-12 Aprendizaje automático y análisis de texto para mercados (principal) · secundarias: TMB-11
- **Calidad Q:** 89 (A) — Tipo 20/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** https://proceedings.mlr.press/v70/guo17a.html (preprint: arXiv 1706.04599)
- **Acceso y licencia:** Acceso abierto (PMLR y arXiv)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Guo Pleiss Sun Weinberger "On Calibration of Modern Neural Networks" ICML 2017 PMLR»; WebFetch: sí)
- **Contenido:** Muestra que las redes neuronales profundas están mal calibradas, define el error de calibración esperado (ECE) y propone el escalado de temperatura como corrección simple y eficaz.
- **Uso en el Motor:** MC-B10: calibración de probabilidades de modelos de clasificación (escalado de temperatura).
- **Limitaciones:** Centrado en clasificación de imágenes y texto; no aborda el desplazamiento de distribución típico de los mercados.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-12) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### MBM-0236 · Q 89 (A) — Textual Analysis in Accounting and Finance: A Survey

- **Autores:** Tim Loughran; Bill McDonald
- **Año:** 2016
- **Publicación o institución:** Journal of Accounting Research
- **Tipo de documento:** Artículo de revisión revisado por pares
- **Temática:** TMB-12 Aprendizaje automático y análisis de texto para mercados (principal) · secundarias: —
- **Calidad Q:** 89 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.1111/1475-679x.12123 · https://www.citedrive.com/en/discovery/textual-analysis-in-accounting-and-finance-a-survey
- **Acceso y licencia:** De pago (Wiley)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Loughran McDonald "Textual Analysis in Accounting and Finance: A Survey" 2016 Journal of Accounting Research "When Is a Liability Not a Liability"»; WebFetch: sí, ficha bibliográfica CiteDrive)
- **Contenido:** Revisión de métodos de análisis textual en contabilidad y finanzas, sus matices y errores frecuentes, y de la literatura aplicada.
- **Uso en el Motor:** AG-B10 y MC-B07: lista de control de buenas prácticas antes de usar señales de texto en el cribado.
- **Limitaciones:** Anterior a los modelos de lenguaje de gran tamaño.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### DOC-MOT-0406 · Q 88 (A) — A Unified Approach to Interpreting Model Predictions

- **Autores:** Scott M. Lundberg; Su-In Lee
- **Año:** 2017
- **Publicación o institución:** Advances in Neural Information Processing Systems 30 (NIPS 2017)
- **Tipo de documento:** Comunicación de congreso revisada por pares
- **Temática:** TMB-12 Aprendizaje automático y análisis de texto para mercados (principal) · secundarias: —
- **Calidad Q:** 88 (A) — Tipo 20/25 · Rigor 16/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 9/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://papers.nips.cc/paper/7062-a (preprint: arXiv 1705.07874)
- **Acceso y licencia:** Acceso abierto (actas NeurIPS y arXiv)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Lundberg Lee 2017 "A Unified Approach to Interpreting Model Predictions" NeurIPS»; WebFetch: sí)
- **Contenido:** Propone SHAP: atribución aditiva de la predicción a cada variable basada en valores de Shapley, con propiedades de unicidad y aproximaciones eficientes (Kernel SHAP).
- **Uso en el Motor:** MC-B07: valores SHAP para explicar a AG-B12 y al Auditor por qué un candidato puntúa alto.
- **Limitaciones:** Atribuciones engañosas con variables correlacionadas; coste computacional; explica el modelo, no la causalidad.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-12) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0088 · Q 88 (A) — XGBoost: A Scalable Tree Boosting System

- **Autores:** Tianqi Chen; Carlos Guestrin
- **Año:** 2016
- **Publicación o institución:** Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (KDD '16), ACM
- **Tipo de documento:** Comunicación de congreso revisada por pares
- **Temática:** TMB-12 Aprendizaje automático y análisis de texto para mercados (principal) · secundarias: —
- **Calidad Q:** 88 (A) — Tipo 20/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI: 10.1145/2939672.2939785 · https://arxiv.org/abs/1603.02754
- **Acceso y licencia:** Preprint de acceso abierto en arXiv; versión de actas en ACM
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Chen Guestrin "XGBoost: A Scalable Tree Boosting System" KDD 2016 arXiv»; WebFetch: sí)
- **Contenido:** Describe XGBoost: boosting de árboles con regularización explícita, algoritmo consciente de la dispersión, bosquejo de cuantiles ponderado y diseño de sistema escalable.
- **Uso en el Motor:** MC-B07: implementación eficiente de árboles potenciados para el cribado.
- **Limitaciones:** Riesgo de sobreajuste sin validación temporal; artículo de sistema, no de inferencia.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-12) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0089 · Q 87 (A) — Predicting Good Probabilities with Supervised Learning

- **Autores:** Alexandru Niculescu-Mizil; Rich Caruana
- **Año:** 2005
- **Publicación o institución:** Proceedings of the 22nd International Conference on Machine Learning (ICML 2005), ACM, 625-632
- **Tipo de documento:** Comunicación de congreso revisada por pares
- **Temática:** TMB-12 Aprendizaje automático y análisis de texto para mercados (principal) · secundarias: TMB-11
- **Calidad Q:** 87 (A) — Tipo 20/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI: 10.1145/1102351.1102430 · https://mlanthology.org/icml/2005/niculescumizil2005icml-predicting
- **Acceso y licencia:** Ficha abierta en ML Anthology; texto en ACM Digital Library
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Niculescu-Mizil Caruana 2005 "Predicting good probabilities with supervised learning" ICML»; WebFetch: sí)
- **Contenido:** Evalúa la calibración de las probabilidades de diez clasificadores y muestra cómo corregirla con escalado de Platt y regresión isotónica.
- **Uso en el Motor:** MC-B10: calibración de probabilidades (Platt, isotónica) de clasificadores de candidatos.
- **Limitaciones:** Datos no financieros; la isotónica sobreajusta con muestras pequeñas.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-12) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0407 · Q 86 (A) — Deep Learning in Asset Pricing

- **Autores:** Luyang Chen; Markus Pelger; Jason Zhu
- **Año:** 2024
- **Publicación o institución:** Management Science (INFORMS); documento de trabajo SSRN 3350138 (2019, rev. 2021)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-12 Aprendizaje automático y análisis de texto para mercados (principal) · secundarias: —
- **Calidad Q:** 86 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 7/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** DOI: 10.1287/mnsc.2023.4695 · https://papers.ssrn.com/abstract=3350138
- **Acceso y licencia:** Documento de trabajo gratuito en SSRN y arXiv (1904.00745); versión de revista de pago
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Chen Pelger Zhu "Deep Learning in Asset Pricing" Management Science»; WebFetch: sí, sobre SSRN)
- **Contenido:** Estima el factor de descuento estocástico con redes neuronales (incluidas recurrentes para estados macro) bajo la condición de no arbitraje mediante un enfoque adversarial, logrando mayor Sharpe y menores errores de valoración que los modelos de referencia.
- **Uso en el Motor:** MC-B07: redes profundas en valoración de activos; referencia para modelos no lineales de factores.
- **Limitaciones:** Alta complejidad y sensibilidad a hiperparámetros; año de la revista inferido del DOI y de la página del editor (no se vio volumen/páginas).
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-12) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### MBM-0240 · Q 86 (A) — Is All That Talk Just Noise? The Information Content of Internet Stock Message Boards

- **Autores:** Werner Antweiler; Murray Z. Frank
- **Año:** 2004
- **Publicación o institución:** Journal of Finance, vol. 59, págs. 1259-1293
- **Tipo de documento:** Artículo revisado por pares (revista de primer nivel)
- **Temática:** TMB-12 Aprendizaje automático y análisis de texto para mercados (principal) · secundarias: —
- **Calidad Q:** 86 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 9/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** Página índice: https://www.columbia.edu/~pt2238/papers/Tetlock_Media_Sentiment_JF.pdf (bibliografía)
- **Acceso y licencia:** De pago (Wiley)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Tetlock 2007 "Giving Content to Investor Sentiment: The Role of Media in the Stock Market" Journal of Finance ideas.repec»; WebFetch: sí, bibliografía de Tetlock (2007))
- **Contenido:** Clasifica con Naive Bayes millones de mensajes de foros bursátiles y relaciona su volumen y tono con volatilidad y volumen negociado.
- **Uso en el Motor:** AG-B10: precedente de clasificación supervisada de texto de redes y foros para medir atención y desacuerdo sobre candidatos.
- **Limitaciones:** Foros de principios de los 2000.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### DOC-MOT-0408 · Q 84 (A) — An Empirical Comparison of Supervised Learning Algorithms

- **Autores:** Rich Caruana; Alexandru Niculescu-Mizil
- **Año:** 2006
- **Publicación o institución:** Proceedings of the 23rd International Conference on Machine Learning (ICML 2006), ACM International Conference Proceeding Series vol. 148, 161-168
- **Tipo de documento:** Comunicación de congreso revisada por pares
- **Temática:** TMB-12 Aprendizaje automático y análisis de texto para mercados (principal) · secundarias: —
- **Calidad Q:** 84 (A) — Tipo 20/25 · Rigor 16/20 · Autoridad 13/15 · Vigencia 8/10 · Impacto 9/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** https://cs.utexas.edu/~shivaram/readings/b2hd-CaruanaNiculescu-Mizil2006.html
- **Acceso y licencia:** Ficha bibliográfica abierta; texto en ACM Digital Library
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Niculescu-Mizil Caruana 2005 "Predicting good probabilities with supervised learning" ICML» —resultado relacionado—; WebFetch: sí)
- **Contenido:** Compara diez algoritmos supervisados en once problemas y ocho métricas (exactitud, AUC, error cuadrático, entropía cruzada…), antes y después de calibrar; árboles potenciados calibrados, bosques aleatorios y SVM encabezan el ranking.
- **Uso en el Motor:** MC-B07: comparación empírica de algoritmos supervisados para elegir un modelo base.
- **Limitaciones:** Conjuntos de datos no financieros y anteriores al aprendizaje profundo moderno.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-12) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0085 · Q 83 (A) — Advances in Financial Machine Learning

- **Autores:** Marcos López de Prado
- **Año:** 2018
- **Publicación o institución:** John Wiley & Sons
- **Tipo de documento:** Libro académico-profesional
- **Temática:** TMB-12 Aprendizaje automático y análisis de texto para mercados (principal) · secundarias: TMB-11
- **Calidad Q:** 83 (A) — Tipo 20/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 8/10 · Acceso 5/10
- **DOI / ISBN / URL:** ISBN: 978-1-119-48208-6 · https://www.wiley-vch.de/en/areas-interest/finance-economics-law/advances-in-financial-machine-learning-978-1-119-48208-6
- **Acceso y licencia:** Libro de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «López de Prado "Advances in Financial Machine Learning" Wiley 2018 ISBN 978-1-119-48208-6»; WebFetch: no)
- **Contenido:** Manual práctico de aprendizaje automático financiero: barras de información, etiquetado por triple barrera, metaetiquetado, diferenciación fraccional, validación cruzada purgada con embargo, importancia de variables y sobreajuste de backtest.
- **Uso en el Motor:** MC-B07 y MC-B10: etiquetado, validación cruzada purgada y embargo para modelos de selección sin fuga de información.
- **Limitaciones:** Algunas propuestas con evidencia empírica limitada; autor vinculado a la industria.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-12) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0409 · Q 83 (A) — Regression Shrinkage and Selection via the Lasso: A Retrospective

- **Autores:** Robert Tibshirani
- **Año:** 2011
- **Publicación o institución:** Journal of the Royal Statistical Society, Series B (Statistical Methodology), 73(3), 273-282
- **Tipo de documento:** Artículo revisado por pares (retrospectiva con discusión)
- **Temática:** TMB-12 Aprendizaje automático y análisis de texto para mercados (principal) · secundarias: —
- **Calidad Q:** 83 (A) — Tipo 22/25 · Rigor 14/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** DOI: 10.1111/j.1467-9868.2011.00771.x · https://academicnewsletter.sufe.edu.cn/info/442010
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Tibshirani 1996 "Regression shrinkage and selection via the lasso" Journal of the Royal Statistical Society Series B» —resultado relacionado—; WebFetch: sí)
- **Contenido:** Repasa quince años de desarrollo del lasso: algoritmos (LARS, descenso por coordenadas), extensiones (lasso agrupado, fusionado, elastic net) e inferencia tras la selección.
- **Uso en el Motor:** MC-B07: retrospectiva del lasso y sus extensiones.
- **Limitaciones:** Texto breve de posición; el número de volumen procede de la cita estándar (la página leída mostraba páginas y DOI).
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-12) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0411 · Q 80 (A) — Machine Learning for Asset Managers

- **Autores:** Marcos López de Prado
- **Año:** 2020
- **Publicación o institución:** Cambridge University Press, serie Elements in Quantitative Finance
- **Tipo de documento:** Libro académico-profesional (monografía breve)
- **Temática:** TMB-12 Aprendizaje automático y análisis de texto para mercados (principal) · secundarias: TMB-11
- **Calidad Q:** 80 (A) — Tipo 20/25 · Rigor 15/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 8/10 · Acceso 6/10
- **DOI / ISBN / URL:** ISBN: 978-1-108-79289-9 · https://en.wikipedia.org/wiki/Deflated_Sharpe_ratio (bibliografía)
- **Acceso y licencia:** Libro de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Sharpe ratio" en.wikipedia.org deflated Sharpe ratio»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Deflated_Sharpe_ratio)
- **Contenido:** Aplica aprendizaje no supervisado y supervisado a la gestión de carteras: limpieza de matrices de covarianza, métricas de distancia, agrupamiento, importancia de variables y control de pruebas múltiples.
- **Uso en el Motor:** MC-B07: agrupamiento, denoising de covarianzas e importancia de variables para el cribado.
- **Limitaciones:** Autor vinculado a la industria; algunas recetas con evidencia empírica limitada.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-12) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0414 · Q 76 (B) — The 10 Reasons Most Machine Learning Funds Fail

- **Autores:** Marcos López de Prado
- **Año:** 2018
- **Publicación o institución:** The Journal of Portfolio Management, 44(6), 120-133
- **Tipo de documento:** Artículo revisado por pares (profesional)
- **Temática:** TMB-12 Aprendizaje automático y análisis de texto para mercados (principal) · secundarias: TMB-14
- **Calidad Q:** 76 (B) — Tipo 22/25 · Rigor 12/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 7/10 · Independencia 7/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.3905/jpm.2018.44.6.120 · https://en.wikipedia.org/wiki/Deflated_Sharpe_ratio (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Sharpe ratio" en.wikipedia.org deflated Sharpe ratio»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Deflated_Sharpe_ratio)
- **Contenido:** Enumera los errores habituales al aplicar aprendizaje automático a la inversión (muestreo cronológico, diferenciación integral, etiquetado ingenuo, fuga en validación cruzada, backtests sobreajustados) y sus remedios.
- **Uso en el Motor:** MC-B10 y TMB-14: errores habituales al aplicar aprendizaje automático a la inversión; lista de control.
- **Limitaciones:** Texto de posición de un autor de la industria; poca evidencia empírica formal.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-12) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0410 · Q 70 (B) — Confronting Machine Learning With Financial Research

- **Autores:** Kristof Lommers; Ouns El Harzli; Jack Kim
- **Año:** 2021
- **Publicación o institución:** arXiv 2103.00366 (Universidad de Oxford, Oxford-Man Institute of Quantitative Finance; Data Capital Management)
- **Tipo de documento:** Documento de trabajo (preprint)
- **Temática:** TMB-12 Aprendizaje automático y análisis de texto para mercados (principal) · secundarias: —
- **Calidad Q:** 70 (B) — Tipo 15/25 · Rigor 12/20 · Autoridad 10/15 · Vigencia 10/10 · Impacto 5/10 · Independencia 8/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://arxiv.org/pdf/2103.00366
- **Acceso y licencia:** Acceso abierto (arXiv)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Kelly Xiu "Financial Machine Learning" Foundations and Trends in Finance 2023» —resultado relacionado—; WebFetch: sí)
- **Contenido:** Analiza por qué los datos financieros (baja relación señal-ruido, no estacionariedad, muestras cortas) y las normas de la investigación social exigen adaptar el aprendizaje automático, y lo sitúa como complemento del econometra en estimación, contraste, inferencia causal y predicción.
- **Uso en el Motor:** MC-B07: crítica y límites del aprendizaje automático en la investigación financiera.
- **Limitaciones:** Preprint sin revisión por pares constatada; año inferido del identificador arXiv (marzo de 2021); uno de los autores procede de la industria.

<!-- Segunda tanda (2026-11-02): cupo de 25 WebSearch agotado. Fichas con «VERIFICADO_BUSQUEDA» y WebFetch sobre «página índice»: metadatos (autores, año, título, revista, páginas y, cuando figura, DOI) confirmados en la bibliografía de una página índice leída (Wikipedia, IDEAS/RePEc, bibliografía de un artículo o manual de software); la página propia de la obra no se ha cargado. Los DOI solo se incluyen si aparecían en la página leída. -->
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-12) el 2026-11-02 con su ID original; Temática y Uso adaptados.

## TMB-13 Decisión multicriterio y agregación de juicio experto

#### MBM-0263 · Q 92 (A) — Psychological Strategies for Winning a Geopolitical Forecasting Tournament

- **Autores:** Barbara A. Mellers; Lyle Ungar; Jonathan Baron; Jaime Ramos; Burcu Gurcay; Katrina Fincher; et al.
- **Año:** 2014
- **Publicación o institución:** Psychological Science
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-13 Decisión multicriterio y agregación de juicio experto (principal) · secundarias: TMB-11
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1177/0956797614524255 · https://www.psychologicalscience.org/journals/psychological-science/0956797614524255/
- **Acceso y licencia:** De pago (SAGE)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Mellers Tetlock 2014 "Psychological Strategies for Winning a Geopolitical Forecasting Tournament" Satopää "Combining multiple probability predictions using a simple logit model"»; WebFetch: no; confirmado en la bibliografía de Tetlock et al. (2014), leída con WebFetch)
- **Contenido:** Muestra que el entrenamiento en razonamiento probabilístico, el trabajo en equipo y el seguimiento de los mejores mejoran la precisión de los pronósticos.
- **Uso en el Motor:** AG-B02 y MC-B10: prácticas para mejorar la calibración de los especialistas (formación, equipos, selección de los mejor calibrados).
- **Limitaciones:** Preguntas geopolíticas, no de mercado.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### MBM-0264 · Q 92 (A) — Combining Multiple Probability Predictions Using a Simple Logit Model

- **Autores:** Ville A. Satopää; Jonathan Baron; Dean P. Foster; Barbara A. Mellers; Philip E. Tetlock; Lyle H. Ungar
- **Año:** 2014
- **Publicación o institución:** International Journal of Forecasting, vol. 30, págs. 344-356
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-13 Decisión multicriterio y agregación de juicio experto (principal) · secundarias: TMB-11
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 9/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1016/j.ijforecast.2013.09.009 · https://www.academia.edu/13898151/Combining_multiple_probability_predictions_using_a_simple_logit_model
- **Acceso y licencia:** De pago; copia en Academia.edu
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Mellers Tetlock 2014 "Psychological Strategies for Winning a Geopolitical Forecasting Tournament" Satopää "Combining multiple probability predictions using a simple logit model"»; WebFetch: sí, ficha en Academia.edu)
- **Contenido:** Agrega probabilidades de muchos pronosticadores en escala logit con extremización, mejorando la media simple.
- **Uso en el Motor:** AG-B02 y MC-B10: regla de agregación extremizada de las probabilidades de los especialistas.
- **Limitaciones:** Extremizar empeora si los juicios no son independientes.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### MBM-0248 · Q 90 (A) — Combining Probability Distributions from Experts in Risk Analysis

- **Autores:** Robert T. Clemen; Robert L. Winkler
- **Año:** 1999
- **Publicación o institución:** Risk Analysis, vol. 19, n.º 2, págs. 187-203
- **Tipo de documento:** Artículo de revisión revisado por pares
- **Temática:** TMB-13 Decisión multicriterio y agregación de juicio experto (principal) · secundarias: TMB-11
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.1023/A:1006917509560 · https://fds.duke.edu/db/aas/stat/faculty/bob.winkler/publications/278482
- **Acceso y licencia:** De pago (Wiley)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Clemen Winkler 1999 "Combining Probability Distributions From Experts in Risk Analysis" Cooke 1991 "Experts in Uncertainty" classical model structured expert judgment»; WebFetch: sí, ficha de publicaciones de Duke)
- **Contenido:** Revisión de métodos para agregar distribuciones de probabilidad de expertos: agregación matemática (pools lineales y logarítmicos, bayesianos) y conductual.
- **Uso en el Motor:** AG-B02 y MC-B10: combinar las probabilidades de los especialistas AG-B03…AG-B11 en una distribución única con método explícito.
- **Limitaciones:** No trata la ponderación por desempeño en detalle (véase Cooke).
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### MBM-0251 · Q 89 (A) — TU Delft Expert Judgment Data Base

- **Autores:** Roger M. Cooke; Louis L. H. J. Goossens
- **Año:** 2008
- **Publicación o institución:** Reliability Engineering & System Safety (2008)
- **Tipo de documento:** Artículo revisado por pares (evidencia empírica)
- **Temática:** TMB-13 Decisión multicriterio y agregación de juicio experto (principal) · secundarias: TMB-11
- **Calidad Q:** 89 (A) — Tipo 24/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 7/10 · Impacto 9/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** https://filelist.tudelft.nl/EWI/Over%20de%20faculteit/Afdelingen/Applied%20Mathematics/Applied%20Probability/Risk/Download/RESS_Cooke_Goossens.pdf · https://rogermcooke.net/rogermcooke_files/RESS3860-TUDdatabase.pdf
- **Acceso y licencia:** Copia abierta en la TU Delft
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Clemen Winkler 1999 "Combining Probability Distributions From Experts in Risk Analysis" Cooke 1991 "Experts in Uncertainty" classical model structured expert judgment»; WebFetch: sí, PDF de la TU Delft (revista según los resultados de búsqueda; volumen y páginas no vistos))
- **Contenido:** Base de datos de estudios de juicio experto con el modelo clásico; compara la ponderación por desempeño con la ponderación igual.
- **Uso en el Motor:** MC-B10 y AG-B02: evidencia de que ponderar por desempeño mejora la calibración del panel.
- **Limitaciones:** Estudios de ingeniería y riesgo, no de mercados.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### MBM-0241 · Q 89 (A) — A Scaling Method for Priorities in Hierarchical Structures

- **Autores:** Thomas L. Saaty
- **Año:** 1977
- **Publicación o institución:** Journal of Mathematical Psychology, vol. 15, págs. 234-281
- **Tipo de documento:** Artículo revisado por pares (fundacional)
- **Temática:** TMB-13 Decisión multicriterio y agregación de juicio experto (principal) · secundarias: —
- **Calidad Q:** 89 (A) — Tipo 24/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 6/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** https://mail.superdecisions.com/sd_resources/Paper_ScalingMethod.pdf
- **Acceso y licencia:** Copia abierta (Super Decisions)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Analytic hierarchy process Saaty 1980 "A scaling method for priorities in hierarchical structures" wikipedia»; WebFetch: sí, PDF del artículo)
- **Contenido:** Fundamento del AHP: comparaciones por pares en escala 1-9, prioridades por el autovector principal e índice de consistencia.
- **Uso en el Motor:** AG-B02 Director y AG-B12: ponderar criterios del veredicto sectorial y de la selección de candidatos por comparaciones por pares con control de consistencia.
- **Limitaciones:** Problemas de inversión de rango (véase Dyer, 1990).
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### ANA-DOC-0236 · Q 88 (A) — Forecast Combinations

- **Autores:** Allan Timmermann
- **Año:** 2006
- **Publicación o institución:** Handbook of Economic Forecasting, vol. 1 (eds. G. Elliott, C. W. J. Granger y A. Timmermann), Elsevier / North-Holland
- **Tipo de documento:** Capítulo de manual de referencia (survey)
- **Temática:** TMB-13 Decisión multicriterio y agregación de juicio experto (principal) · secundarias: TMB-11
- **Calidad Q:** 88 (A) — Tipo 22/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** Confirmada vía página índice: https://econpapers.repec.org/bookchap/eeeecofor/1.htm (índice del Handbook en EconPapers/RePEc)
- **Acceso y licencia:** Texto editorial por suscripción; sin copia abierta verificada en esta carga · Licencia: copyright del editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Handbook of Economic Forecasting Volume 1 2006 Elliott Granger Timmermann chapters "Forecast Combinations" "Forecast Evaluation"»; WebFetch: sí, de la página índice; no de la obra)
- **Contenido:** Revisión de la combinación de pronósticos: por qué los promedios simples suelen ser difíciles de batir y cuándo conviene ponderar.
- **Uso en el Motor:** AG-B02 y MC-B10: combinar pronósticos de varios especialistas o modelos (pesos iguales frente a óptimos).
- **Limitaciones:** Estado del arte a 2006; el vol. 2 (2013) actualiza parte de los temas.
- **Disciplinas y etiquetas:** Econometría de la previsión · handbook; combinacion-de-pronosticos; promedios
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-13) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### MBM-0259 · Q 88 (A) — The Delphi Technique as a Forecasting Tool: Issues and Analysis

- **Autores:** Gene Rowe; George Wright
- **Año:** 1999
- **Publicación o institución:** International Journal of Forecasting, vol. 15, n.º 4, págs. 353-375
- **Tipo de documento:** Artículo de revisión revisado por pares
- **Temática:** TMB-13 Decisión multicriterio y agregación de juicio experto (principal) · secundarias: TMB-11
- **Calidad Q:** 88 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 10/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** https://ideas.repec.org/a/eee/intfor/v15y1999i4p353-375.html · ScienceDirect PII S0169-2070(99)00018-7
- **Acceso y licencia:** De pago (Elsevier)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Rowe Wright 1999 "The Delphi technique as a forecasting tool: issues and analysis" International Journal of Forecasting Dalkey Helmer 1963»; WebFetch: sí, ficha IDEAS/RePEc)
- **Contenido:** Revisión de la evidencia empírica sobre Delphi: cuándo mejora a los grupos interactuantes y a la media estadística, y qué rasgos de diseño importan.
- **Uso en el Motor:** AG-B02: diseño de rondas Delphi entre especialistas (anonimato, retroalimentación, iteración) para la prospectiva sectorial (AG-B13).
- **Limitaciones:** Evidencia mayoritariamente de laboratorio.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### MBM-0265 · Q 87 (A) — Forecasting Tournaments: Tools for Increasing Transparency and Improving the Quality of Debate

- **Autores:** Philip E. Tetlock; Barbara A. Mellers; Nick Rohrbaugh; Eva Chen
- **Año:** 2014
- **Publicación o institución:** Current Directions in Psychological Science, vol. 23, n.º 4, págs. 290-295
- **Tipo de documento:** Artículo de revisión breve revisado por pares
- **Temática:** TMB-13 Decisión multicriterio y agregación de juicio experto (principal) · secundarias: TMB-11
- **Calidad Q:** 87 (A) — Tipo 23/25 · Rigor 14/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 8/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** https://faculty.wharton.upenn.edu/wp-content/uploads/2015/07/2014---forecasting-tournaments-tools-for-increasing-transparency-and-improving-debate.pdf
- **Acceso y licencia:** Copia abierta (Wharton)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Mellers Tetlock 2014 "Psychological Strategies for Winning a Geopolitical Forecasting Tournament" Satopää "Combining multiple probability predictions using a simple logit model"»; WebFetch: sí, PDF de Wharton)
- **Contenido:** Defiende los torneos de pronóstico con preguntas verificables y puntuación de Brier para medir y mejorar el juicio experto.
- **Uso en el Motor:** AG-B02 y MC-B10: registrar pronósticos verificables de los especialistas y puntuarlos para ponderarlos después.
- **Limitaciones:** Texto breve.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### MBM-0253 · Q 87 (A) — Combining Probability Distributions: A Critique and an Annotated Bibliography

- **Autores:** Christian Genest; James V. Zidek
- **Año:** 1986
- **Publicación o institución:** Statistical Science, vol. 1, n.º 1
- **Tipo de documento:** Artículo de revisión revisado por pares
- **Temática:** TMB-13 Decisión multicriterio y agregación de juicio experto (principal) · secundarias: —
- **Calidad Q:** 87 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 5/10 · Impacto 9/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** Página índice: https://filelist.tudelft.nl/EWI/Over%20de%20faculteit/Afdelingen/Applied%20Mathematics/Applied%20Probability/Risk/Download/RESS_Cooke_Goossens.pdf (bibliografía)
- **Acceso y licencia:** Revista (Project Euclid; acceso no comprobado)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Clemen Winkler 1999 "Combining Probability Distributions From Experts in Risk Analysis" Cooke 1991 "Experts in Uncertainty" classical model structured expert judgment»; WebFetch: sí, artículo de Cooke y Goossens (bibliografía))
- **Contenido:** Revisión crítica de las reglas de combinación de distribuciones (pools lineales, logarítmicos) y sus propiedades axiomáticas.
- **Uso en el Motor:** AG-B02 y MC-B10: propiedades formales de cada regla de agregación antes de elegirla.
- **Limitaciones:** Antigua; no cubre extremización.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### MBM-0242 · Q 86 (A) — How to Make a Decision: The Analytic Hierarchy Process

- **Autores:** Thomas L. Saaty
- **Año:** 1990
- **Publicación o institución:** European Journal of Operational Research, vol. 48, págs. 9-26
- **Tipo de documento:** Artículo revisado por pares (tutorial)
- **Temática:** TMB-13 Decisión multicriterio y agregación de juicio experto (principal) · secundarias: —
- **Calidad Q:** 86 (A) — Tipo 23/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 6/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** https://vpp.sbuf.se/Public/Documents/ProjectDocuments/06F167EF-B243-48ED-8C45-F7466B3136EB/WebPublishings/How%20to%20make%20decision%20AHP.pdf
- **Acceso y licencia:** Copia abierta
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Analytic hierarchy process Saaty 1980 "A scaling method for priorities in hierarchical structures" wikipedia»; WebFetch: sí, PDF del artículo)
- **Contenido:** Exposición práctica del AHP: estructurar la jerarquía, construir matrices de comparación, sintetizar prioridades y comprobar la consistencia.
- **Uso en el Motor:** AG-B02 y AG-B12: guía operativa para montar la jerarquía de criterios del Bloque B.
- **Limitaciones:** Visión del autor del método.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### MBM-0258 · Q 85 (A) — Multiple Criteria Decision Analysis: State of the Art Surveys (2.ª ed.)

- **Autores:** Salvatore Greco; Matthias Ehrgott; José Rui Figueira (eds.)
- **Año:** 2016
- **Publicación o institución:** Springer
- **Tipo de documento:** Libro académico (compendio de revisiones)
- **Temática:** TMB-13 Decisión multicriterio y agregación de juicio experto (principal) · secundarias: TMB-07
- **Calidad Q:** 85 (A) — Tipo 22/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** ISBN: 9781493930937 · https://www.ebook.de/de/product/24385032/multiple_criteria_decision_analysis.html
- **Acceso y licencia:** De pago (Springer)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «multiple-criteria decision analysis Keeney Raiffa 1976 "Decisions with Multiple Objectives" TOPSIS Hwang Yoon 1981 PROMETHEE Brans Vincke 1985 ELECTRE Roy»; WebFetch: sí, ficha del libro en ebook.de)
- **Contenido:** Revisiones del estado del arte de los métodos multicriterio (MAUT, AHP, ELECTRE, PROMETHEE, métodos robustos, etc.).
- **Uso en el Motor:** AG-B02 y MC-B07: elegir el método multicriterio adecuado y conocer sus supuestos.
- **Limitaciones:** Obra extensa y de pago.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### MBM-0266 · Q 85 (A) — Expert Political Judgment: How Good Is It? How Can We Know?

- **Autores:** Philip E. Tetlock
- **Año:** 2005
- **Publicación o institución:** Princeton University Press
- **Tipo de documento:** Libro académico
- **Temática:** TMB-13 Decisión multicriterio y agregación de juicio experto (principal) · secundarias: TMB-11
- **Calidad Q:** 85 (A) — Tipo 21/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 10/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** Página índice: https://faculty.wharton.upenn.edu/wp-content/uploads/2015/07/2014---forecasting-tournaments-tools-for-increasing-transparency-and-improving-debate.pdf (bibliografía)
- **Acceso y licencia:** De pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Mellers Tetlock 2014 "Psychological Strategies for Winning a Geopolitical Forecasting Tournament" Satopää "Combining multiple probability predictions using a simple logit model"»; WebFetch: sí, bibliografía de Tetlock et al. (2014))
- **Contenido:** Estudio de dos décadas de pronósticos de expertos: baja precisión media y mejor desempeño de los «zorros» frente a los «erizos».
- **Uso en el Motor:** AG-B14 Contrarias y AG-B02: cautela con los juicios expertos no puntuados; incentivo a medir su calibración.
- **Limitaciones:** Dominio político.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### MBM-0243 · Q 84 (A) — The Analytic Hierarchy Process: An Exposition

- **Autores:** Ernest H. Forman; Saul I. Gass
- **Año:** 2001
- **Publicación o institución:** Operations Research, vol. 49, n.º 4, págs. 469-487
- **Tipo de documento:** Artículo revisado por pares (exposición)
- **Temática:** TMB-13 Decisión multicriterio y agregación de juicio experto (principal) · secundarias: —
- **Calidad Q:** 84 (A) — Tipo 24/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 7/10 · Impacto 9/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** DOI: 10.1287/opre.49.4.469.11231 · Página índice: https://en.wikipedia.org/wiki/Analytic_hierarchy_process
- **Acceso y licencia:** De pago (INFORMS)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Analytic hierarchy process Saaty 1980 "A scaling method for priorities in hierarchical structures" wikipedia»; WebFetch: sí, página índice de Wikipedia «Analytic hierarchy process»)
- **Contenido:** Exposición del AHP, sus axiomas, modos de síntesis (distributivo e ideal) y aplicaciones.
- **Uso en el Motor:** AG-B02: elegir el modo de síntesis adecuado y documentar el método en el informe.
- **Limitaciones:** Autores favorables al método.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### MBM-0250 · Q 84 (A) — Experts in Uncertainty: Opinion and Subjective Probability in Science

- **Autores:** Roger M. Cooke
- **Año:** 1991
- **Publicación o institución:** Oxford University Press
- **Tipo de documento:** Libro académico (fundacional)
- **Temática:** TMB-13 Decisión multicriterio y agregación de juicio experto (principal) · secundarias: TMB-11
- **Calidad Q:** 84 (A) — Tipo 21/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 6/10 · Impacto 10/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** Página índice: https://filelist.tudelft.nl/EWI/Over%20de%20faculteit/Afdelingen/Applied%20Mathematics/Applied%20Probability/Risk/Download/RESS_Cooke_Goossens.pdf (bibliografía)
- **Acceso y licencia:** De pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Clemen Winkler 1999 "Combining Probability Distributions From Experts in Risk Analysis" Cooke 1991 "Experts in Uncertainty" classical model structured expert judgment»; WebFetch: sí, artículo de Cooke y Goossens sobre la base de datos de la TU Delft (bibliografía; subtítulo según la obra))
- **Contenido:** Fundamenta el modelo clásico de juicio experto estructurado: pondera expertos por calibración e información medidas con preguntas semilla.
- **Uso en el Motor:** AG-B02 y MC-B10: ponderar a los especialistas por su historial de calibración en vez de a partes iguales.
- **Limitaciones:** Requiere preguntas semilla con respuesta conocida.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### MBM-0267 · Q 83 (A) — Two Reasons to Make Aggregated Probability Forecasts More Extreme

- **Autores:** Jonathan Baron; Lyle H. Ungar; Barbara A. Mellers; Philip E. Tetlock
- **Año:** 2014
- **Publicación o institución:** Decision Analysis
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-13 Decisión multicriterio y agregación de juicio experto (principal) · secundarias: TMB-11
- **Calidad Q:** 83 (A) — Tipo 24/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 8/10 · Impacto 7/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** DOI: 10.1287/deca.2014.0293 · Página índice: https://faculty.wharton.upenn.edu/wp-content/uploads/2015/07/2014---forecasting-tournaments-tools-for-increasing-transparency-and-improving-debate.pdf (bibliografía)
- **Acceso y licencia:** De pago (INFORMS)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Mellers Tetlock 2014 "Psychological Strategies for Winning a Geopolitical Forecasting Tournament" Satopää "Combining multiple probability predictions using a simple logit model"»; WebFetch: sí, bibliografía de Tetlock et al. (2014))
- **Contenido:** Justifica extremizar la media de probabilidades por información compartida parcialmente y por sesgo hacia 0,5.
- **Uso en el Motor:** MC-B10: fundamento de la extremización al agregar probabilidades del panel.
- **Limitaciones:** Volumen y páginas no vistos.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### MBM-0246 · Q 83 (A) — Relative Measurement and Its Generalization in Decision Making

- **Autores:** Thomas L. Saaty
- **Año:** 2008
- **Publicación o institución:** RACSAM — Revista de la Real Academia de Ciencias Exactas, Físicas y Naturales, Serie A: Matemáticas, vol. 102, n.º 2, págs. 251-318
- **Tipo de documento:** Artículo revisado por pares (síntesis)
- **Temática:** TMB-13 Decisión multicriterio y agregación de juicio experto (principal) · secundarias: —
- **Calidad Q:** 83 (A) — Tipo 23/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 8/10 · Impacto 7/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1007/bf03191825 · Página índice: https://en.wikipedia.org/wiki/Analytic_hierarchy_process
- **Acceso y licencia:** Revista (acceso no comprobado)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Analytic hierarchy process Saaty 1980 "A scaling method for priorities in hierarchical structures" wikipedia»; WebFetch: sí, página índice de Wikipedia «Analytic hierarchy process»)
- **Contenido:** Síntesis de la medición relativa (AHP y ANP), incluida la red de dependencias entre criterios.
- **Uso en el Motor:** AG-B02: extender a ANP cuando los criterios del veredicto no son independientes.
- **Limitaciones:** Texto largo y técnico.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### MBM-0249 · Q 83 (A) — Aggregating Probability Distributions

- **Autores:** Robert T. Clemen; Robert L. Winkler
- **Año:** 2007
- **Publicación o institución:** En W. Edwards, R. F. Miles y D. von Winterfeldt (eds.), Advances in Decision Analysis: From Foundations to Applications, Cambridge University Press, págs. 154-176
- **Tipo de documento:** Capítulo de libro académico
- **Temática:** TMB-13 Decisión multicriterio y agregación de juicio experto (principal) · secundarias: TMB-11
- **Calidad Q:** 83 (A) — Tipo 20/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 8/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.1017/CBO9780511611308.010 · https://fds.duke.edu/db/aas/stat/faculty/bob.winkler/publications/278404
- **Acceso y licencia:** De pago (Cambridge)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Clemen Winkler 1999 "Combining Probability Distributions From Experts in Risk Analysis" Cooke 1991 "Experts in Uncertainty" classical model structured expert judgment»; WebFetch: sí, ficha de publicaciones de Duke)
- **Contenido:** Actualización de la revisión de 1999 sobre agregación de distribuciones de expertos, con recomendaciones prácticas.
- **Uso en el Motor:** AG-B02: elegir regla de agregación (media lineal, ponderada, extremizada) para el panel del Bloque B.
- **Limitaciones:** Capítulo; editores citados según la obra (no vistos en la ficha).
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### MBM-0257 · Q 83 (A) — A Preference Ranking Organisation Method (The PROMETHEE Method for Multiple Criteria Decision-Making)

- **Autores:** J. P. Brans; Ph. Vincke
- **Año:** 1985
- **Publicación o institución:** Management Science, vol. 31, n.º 6, págs. 647 y ss.
- **Tipo de documento:** Artículo revisado por pares (fundacional)
- **Temática:** TMB-13 Decisión multicriterio y agregación de juicio experto (principal) · secundarias: TMB-07
- **Calidad Q:** 83 (A) — Tipo 24/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 6/10 · Impacto 9/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** DOI: 10.1287/mnsc.31.6.647 · https://pubsonline.informs.org/doi/fpi/10.1287/mnsc.31.6.647
- **Acceso y licencia:** De pago (INFORMS)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «multiple-criteria decision analysis Keeney Raiffa 1976 "Decisions with Multiple Objectives" TOPSIS Hwang Yoon 1981 PROMETHEE Brans Vincke 1985 ELECTRE Roy»; WebFetch: sí, primera página en INFORMS PubsOnline)
- **Contenido:** Método de sobreclasificación PROMETHEE: funciones de preferencia por criterio y flujos de preferencia para ordenar alternativas.
- **Uso en el Motor:** AG-B12 y MC-B07: ranking alternativo de candidatos que no compensa totalmente debilidades graves con fortalezas (contraste del ranking aditivo).
- **Limitaciones:** Requiere elegir funciones de preferencia y umbrales.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### MBM-0254 · Q 83 (A) — Decisions with Multiple Objectives: Preferences and Value Tradeoffs

- **Autores:** Ralph L. Keeney; Howard Raiffa
- **Año:** 1976
- **Publicación o institución:** John Wiley & Sons, Nueva York
- **Tipo de documento:** Libro académico (fundacional; Premio Lanchester 1976)
- **Temática:** TMB-13 Decisión multicriterio y agregación de juicio experto (principal) · secundarias: —
- **Calidad Q:** 83 (A) — Tipo 21/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 5/10 · Impacto 10/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** https://www.informs.org/Explore/History-of-O.R.-Excellence/Biographical-Profiles/Keeney-Ralph-L
- **Acceso y licencia:** De pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «multiple-criteria decision analysis Keeney Raiffa 1976 "Decisions with Multiple Objectives" TOPSIS Hwang Yoon 1981 PROMETHEE Brans Vincke 1985 ELECTRE Roy»; WebFetch: sí, perfil biográfico de Keeney en INFORMS)
- **Contenido:** Teoría de utilidad multiatributo: independencia de preferencias, funciones de valor aditivas y multiplicativas, y elicitación de pesos.
- **Uso en el Motor:** AG-B02 y AG-B12: fundamento teórico de la puntuación compuesta del veredicto sectorial y del ranking de candidatos.
- **Limitaciones:** Elicitación exigente.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### MBM-0244 · Q 82 (A) — Remarks on the Analytic Hierarchy Process

- **Autores:** James S. Dyer
- **Año:** 1990
- **Publicación o institución:** Management Science, vol. 36, n.º 3, págs. 249-258
- **Tipo de documento:** Artículo revisado por pares (crítica)
- **Temática:** TMB-13 Decisión multicriterio y agregación de juicio experto (principal) · secundarias: —
- **Calidad Q:** 82 (A) — Tipo 24/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 5/10 · Impacto 9/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** Página índice: https://en.wikipedia.org/wiki/Analytic_hierarchy_process
- **Acceso y licencia:** De pago (INFORMS)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Analytic hierarchy process Saaty 1980 "A scaling method for priorities in hierarchical structures" wikipedia»; WebFetch: sí, página índice de Wikipedia «Analytic hierarchy process»)
- **Contenido:** Crítica del AHP: inversión de rango arbitraria al añadir alternativas y propuesta de vincularlo a la teoría de utilidad multiatributo.
- **Uso en el Motor:** AG-B14 Contrarias y Auditor: límite del AHP; comprobar la estabilidad del ranking de candidatos al añadir o quitar alternativas.
- **Limitaciones:** Debate académico (réplica de Harker y Vargas).
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### MBM-0256 · Q 81 (A) — Decision Analysis: An Overview

- **Autores:** Ralph L. Keeney
- **Año:** 1982
- **Publicación o institución:** Operations Research, vol. 30, n.º 5, págs. 803-838
- **Tipo de documento:** Artículo de revisión revisado por pares
- **Temática:** TMB-13 Decisión multicriterio y agregación de juicio experto (principal) · secundarias: —
- **Calidad Q:** 81 (A) — Tipo 24/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 5/10 · Impacto 8/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** https://www.informs.org/Explore/History-of-O.R.-Excellence/Biographical-Profiles/Keeney-Ralph-L
- **Acceso y licencia:** De pago (INFORMS)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «multiple-criteria decision analysis Keeney Raiffa 1976 "Decisions with Multiple Objectives" TOPSIS Hwang Yoon 1981 PROMETHEE Brans Vincke 1985 ELECTRE Roy»; WebFetch: sí, perfil biográfico de Keeney en INFORMS)
- **Contenido:** Panorama del análisis de decisiones: estructuración, probabilidades subjetivas, utilidad y análisis de sensibilidad.
- **Uso en el Motor:** AG-B02 y Auditor: marco general para documentar decisiones bajo incertidumbre.
- **Limitaciones:** Antiguo.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### MBM-0260 · Q 81 (A) — An Experimental Application of the DELPHI Method to the Use of Experts

- **Autores:** Norman Dalkey; Olaf Helmer
- **Año:** 1963
- **Publicación o institución:** Management Science, vol. 9, n.º 3
- **Tipo de documento:** Artículo revisado por pares (fundacional)
- **Temática:** TMB-13 Decisión multicriterio y agregación de juicio experto (principal) · secundarias: —
- **Calidad Q:** 81 (A) — Tipo 24/25 · Rigor 14/20 · Autoridad 15/15 · Vigencia 4/10 · Impacto 10/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** Página índice: https://ideas.repec.org/a/eee/intfor/v15y1999i4p353-375.html (bibliografía de Rowe y Wright)
- **Acceso y licencia:** De pago (INFORMS)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Rowe Wright 1999 "The Delphi technique as a forecasting tool: issues and analysis" International Journal of Forecasting Dalkey Helmer 1963»; WebFetch: sí, ficha IDEAS/RePEc de Rowe y Wright (lista de referencias))
- **Contenido:** Primera descripción publicada del método Delphi desarrollado en RAND.
- **Uso en el Motor:** AG-B02 y AG-B13: origen y lógica del procedimiento Delphi.
- **Limitaciones:** Valor histórico.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### MBM-0262 · Q 78 (B) — People Consultation to Construct the Future: A Delphi Application

- **Autores:** Jon Landeta; Jon Barrutia
- **Año:** 2011
- **Publicación o institución:** International Journal of Forecasting
- **Tipo de documento:** Artículo revisado por pares (aplicación)
- **Temática:** TMB-13 Decisión multicriterio y agregación de juicio experto (principal) · secundarias: —
- **Calidad Q:** 78 (B) — Tipo 24/25 · Rigor 14/20 · Autoridad 12/15 · Vigencia 8/10 · Impacto 6/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** Página índice: https://ideas.repec.org/a/eee/intfor/v15y1999i4p353-375.html (artículos relacionados)
- **Acceso y licencia:** De pago (Elsevier)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Rowe Wright 1999 "The Delphi technique as a forecasting tool: issues and analysis" International Journal of Forecasting Dalkey Helmer 1963»; WebFetch: sí, ficha IDEAS/RePEc de Rowe y Wright (sección de artículos relacionados))
- **Contenido:** Aplicación de Delphi con participación amplia para construir visiones de futuro; autores de la Universidad del País Vasco.
- **Uso en el Motor:** AG-B13 Prospectiva: ejemplo europeo de Delphi para escenarios.
- **Limitaciones:** Volumen y páginas no vistos.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### MBM-0252 · Q 78 (B) — Procedures Guide for Structured Expert Judgment

- **Autores:** Roger M. Cooke; Louis L. H. J. Goossens
- **Año:** 2000
- **Publicación o institución:** Comisión Europea, EUR 18820EN (también Radiation Protection Dosimetry, vol. 90, n.º 3)
- **Tipo de documento:** Guía metodológica institucional
- **Temática:** TMB-13 Decisión multicriterio y agregación de juicio experto (principal) · secundarias: —
- **Calidad Q:** 78 (B) — Tipo 18/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 6/10 · Impacto 8/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** Página índice: https://filelist.tudelft.nl/EWI/Over%20de%20faculteit/Afdelingen/Applied%20Mathematics/Applied%20Probability/Risk/Download/RESS_Cooke_Goossens.pdf (bibliografía)
- **Acceso y licencia:** Documento institucional (acceso no comprobado)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Clemen Winkler 1999 "Combining Probability Distributions From Experts in Risk Analysis" Cooke 1991 "Experts in Uncertainty" classical model structured expert judgment»; WebFetch: sí, artículo de Cooke y Goossens (bibliografía))
- **Contenido:** Protocolo paso a paso para elicitar juicio experto: selección de expertos, preguntas, entrenamiento, elicitación, agregación y documentación.
- **Uso en el Motor:** AG-B02: protocolo para las rondas de elicitación con los especialistas y su registro.
- **Limitaciones:** Orientado a riesgo radiológico.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### MBM-0255 · Q 78 (B) — Value-Focused Thinking: A Path to Creative Decisionmaking

- **Autores:** Ralph L. Keeney
- **Año:** 1992
- **Publicación o institución:** Harvard University Press
- **Tipo de documento:** Libro académico
- **Temática:** TMB-13 Decisión multicriterio y agregación de juicio experto (principal) · secundarias: —
- **Calidad Q:** 78 (B) — Tipo 19/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 6/10 · Impacto 9/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** https://www.informs.org/Explore/History-of-O.R.-Excellence/Biographical-Profiles/Keeney-Ralph-L
- **Acceso y licencia:** De pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «multiple-criteria decision analysis Keeney Raiffa 1976 "Decisions with Multiple Objectives" TOPSIS Hwang Yoon 1981 PROMETHEE Brans Vincke 1985 ELECTRE Roy»; WebFetch: sí, perfil biográfico de Keeney en INFORMS)
- **Contenido:** Propone partir de los objetivos (valores) del decisor antes que de las alternativas para estructurar decisiones.
- **Uso en el Motor:** AG-B02: estructurar los criterios del análisis a partir de los objetivos del propietario antes de puntuar.
- **Limitaciones:** Enfoque cualitativo.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### MBM-0261 · Q 78 (B) — Combining the Judgments of Experts: How Many and Which Ones?

- **Autores:** Robert H. Ashton
- **Año:** 1986
- **Publicación o institución:** Organizational Behavior and Human Decision Processes, vol. 38, n.º 3
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-13 Decisión multicriterio y agregación de juicio experto (principal) · secundarias: TMB-11
- **Calidad Q:** 78 (B) — Tipo 24/25 · Rigor 15/20 · Autoridad 13/15 · Vigencia 5/10 · Impacto 7/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** Página índice: https://ideas.repec.org/a/eee/intfor/v15y1999i4p353-375.html (bibliografía de Rowe y Wright)
- **Acceso y licencia:** De pago (Elsevier)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Rowe Wright 1999 "The Delphi technique as a forecasting tool: issues and analysis" International Journal of Forecasting Dalkey Helmer 1963»; WebFetch: sí, ficha IDEAS/RePEc de Rowe y Wright (lista de referencias))
- **Contenido:** Analiza cómo mejora la precisión al promediar juicios de más expertos y cuáles conviene incluir.
- **Uso en el Motor:** AG-B02: dimensionar el panel de especialistas y su composición.
- **Limitaciones:** Contexto contable.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### MBM-0247 · Q 76 (B) — Models, Methods, Concepts & Applications of the Analytic Hierarchy Process

- **Autores:** Thomas L. Saaty; Luis G. Vargas
- **Año:** 2001
- **Publicación o institución:** Kluwer Academic Publishers
- **Tipo de documento:** Libro académico
- **Temática:** TMB-13 Decisión multicriterio y agregación de juicio experto (principal) · secundarias: —
- **Calidad Q:** 76 (B) — Tipo 19/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 6/10 · Impacto 8/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** ISBN: 0-7923-7267-0 · Página índice: https://en.wikipedia.org/wiki/Analytic_hierarchy_process
- **Acceso y licencia:** De pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Analytic hierarchy process Saaty 1980 "A scaling method for priorities in hierarchical structures" wikipedia»; WebFetch: sí, página índice de Wikipedia «Analytic hierarchy process»)
- **Contenido:** Compendio de modelos y aplicaciones del AHP, incluidas asignación de recursos y previsión.
- **Uso en el Motor:** AG-B02 y AG-B12: ejemplos de aplicación del AHP a la asignación y la priorización.
- **Limitaciones:** Edición de 2001.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### MBM-0245 · Q 75 (B) — Reply to «Remarks on the Analytic Hierarchy Process» by J. S. Dyer

- **Autores:** Patrick T. Harker; Luis G. Vargas
- **Año:** 1990
- **Publicación o institución:** Management Science, vol. 36, n.º 3, págs. 269-273
- **Tipo de documento:** Artículo revisado por pares (réplica)
- **Temática:** TMB-13 Decisión multicriterio y agregación de juicio experto (principal) · secundarias: —
- **Calidad Q:** 75 (B) — Tipo 22/25 · Rigor 14/20 · Autoridad 13/15 · Vigencia 5/10 · Impacto 7/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** Página índice: https://en.wikipedia.org/wiki/Analytic_hierarchy_process
- **Acceso y licencia:** De pago (INFORMS)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Analytic hierarchy process Saaty 1980 "A scaling method for priorities in hierarchical structures" wikipedia»; WebFetch: sí, página índice de Wikipedia «Analytic hierarchy process»)
- **Contenido:** Defensa del AHP frente a la crítica de Dyer sobre inversión de rango y fundamentos.
- **Uso en el Motor:** Auditor: completar el debate sobre la validez del AHP antes de adoptarlo.
- **Limitaciones:** Réplica breve.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

## TMB-14 Datos, calidad y reproducibilidad

#### ANA-DOC-0280 · Q 98 (A) — Is There a Replication Crisis in Finance?

- **Autores:** Theis Ingerslev Jensen; Bryan T. Kelly; Lasse Heje Pedersen
- **Año:** 2023
- **Publicación o institución:** The Journal of Finance, vol. 78, n.º 5, págs. 2465-2518 (versión de trabajo: NBER WP 28432)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-14 Datos, calidad y reproducibilidad (principal) · secundarias: TMB-11
- **Calidad Q:** 98 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 9/10 · Acceso 10/10
- **DOI / URL:** DOI: 10.1111/jofi.13249 · https://www.nber.org/papers/w28432 · versión editorial: https://research-api.cbs.dk/ws/portalfiles/portal/95651880/theis_ingerslev_jensen_et_al_is_there_a_replication_crisis_in_finance_publishersversion.pdf
- **Acceso y licencia:** Versión editorial en el repositorio de la CBS y versión NBER · Licencia: según el repositorio
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Jensen Kelly Pedersen "Is There a Replication Crisis in Finance?" Journal of Finance»; WebFetch: sí)
- **Contenido:** Con un modelo bayesiano y datos de 93 países concluye que la mayoría de los factores se replica, se agrupa en 13 temas y se mantiene fuera de muestra.
- **Uso en el Motor:** MC-B07 y MC-B10: evidencia de replicabilidad de factores con datos públicos y código abierto; referencia para replicar señales de cribado.
- **Limitaciones:** Conclusión sujeta al marco bayesiano y a la base de datos de los autores.
- **Disciplinas y etiquetas:** Factores · replicacion; zoo-de-factores; internacional
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-14) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### fondo_entry_215 · Q 95 (A) — A manifesto for reproducible science

- **Cita normalizada:** Munafò, M. R., Nosek, B. A., Bishop, D. V. M., Button, K. S., Chambers, C. D., Percie du Sert, N., Simonsohn, U., Wagenmakers, E.-J., Ware, J. J., y Ioannidis, J. P. A. (2017). A manifesto for reproducible science. Nature Human Behaviour, 1(1), 0021.
- **Tipo de documento:** Artículo revisado por pares (perspectiva de consenso)
- **Temática:** TMB-14 Datos, calidad y reproducibilidad (principal) · secundarias: TMB-11
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 10/10
- **DOI / URL:** DOI: 10.1038/s41562-016-0021 · https://orca.cardiff.ac.uk/id/eprint/97336/
- **Acceso y licencia:** Acceso abierto (Creative Commons Attribution); PDF en el repositorio ORCA de Cardiff
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Munafò 2017 "A manifesto for reproducible science" Nature Human Behaviour»; WebFetch: sí)
- **Contenido:** Propone medidas para mejorar la fiabilidad de la investigación en cinco frentes (métodos, reporte y difusión, reproducibilidad, evaluación e incentivos), entre ellas el registro previo, la transparencia de datos y código y la protección frente al sesgo cognitivo del investigador.
- **Uso en el Motor:** Auditor y MC-B10: medidas para la reproducibilidad (registro previo, transparencia, código) aplicadas a los análisis del Bloque B.
- **Limitaciones:** Orientado a ciencias biomédicas y del comportamiento; recomendaciones generales, no protocolos.
- **Origen:** Alta V4.0 (2026-11-02), segunda tanda de verificación. Reutilizada en F8 del Bloque B V2.0 (TMB-14) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### fondo_entry_211 · Q 93 (A) — Transparency, Reproducibility, and the Credibility of Economics Research

- **Cita normalizada:** Christensen, G., y Miguel, E. (2018). Transparency, Reproducibility, and the Credibility of Economics Research. Journal of Economic Literature (número de septiembre). Documento de trabajo previo: NBER Working Paper 22989 (diciembre de 2016).
- **Tipo de documento:** Artículo de revisión revisado por pares (survey)
- **Temática:** TMB-14 Datos, calidad y reproducibilidad (principal) · secundarias: —
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 9/10
- **DOI / URL:** DOI: 10.1257/jel.20171350 · NBER WP 22989: https://www.nber.org/papers/w22989.pdf · Reseña de la AEA: https://aeastaging.aeaweb.org/research/transparency-reproducibility-credibility-economics
- **Acceso y licencia:** Documento de trabajo NBER gratuito; versión JEL por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Christensen Miguel 2018 "Transparency, Reproducibility, and the Credibility of Economics Research" Journal of Economic Literature pdf»; WebFetch: sí (NBER y AEA))
- **Contenido:** Revisión de la evidencia sobre sesgo de publicación, búsqueda de especificaciones y falta de replicación en economía (Ioannidis 2005, Brodeur et al. 2016, proyecto JMCB de Dewald, Thursby y Anderson 1986, Franco et al. 2014) y de las soluciones: registro previo, planes de análisis previos, publicación de datos y código, y replicación.
- **Uso en el Motor:** Auditor: prácticas de transparencia y reproducibilidad en investigación económica aplicables a los artefactos del Motor.
- **Limitaciones:** Volumen y páginas de JEL no confirmados en las páginas leídas; centrado en economía académica.
- **Origen:** Alta V4.0 (2026-11-02), segunda tanda de verificación. Reutilizada en F8 del Bloque B V2.0 (TMB-14) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### fondo_entry_216 · Q 93 (A) — The FAIR Guiding Principles for scientific data management and stewardship

- **Cita normalizada:** Wilkinson, M. D., Dumontier, M., Aalbersberg, IJ. J., et al. (2016). The FAIR Guiding Principles for scientific data management and stewardship. Scientific Data, 3, 160018.
- **Tipo de documento:** Artículo revisado por pares (principios de consenso)
- **Temática:** TMB-14 Datos, calidad y reproducibilidad (principal) · secundarias: —
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 14/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 9/10
- **DOI / URL:** DOI: 10.1038/sdata.2016.18 · https://pure.eur.nl/en/publications/the-fair-guiding-principles-for-scientific-data-management-and-st/
- **Acceso y licencia:** Acceso abierto en la editorial (licencia no indicada en la página del repositorio leída)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Wilkinson 2016 "The FAIR Guiding Principles for scientific data management and stewardship" Scientific Data»; WebFetch: sí (repositorio de la Universidad Erasmus))
- **Contenido:** Principios FAIR: datos localizables (identificadores persistentes y metadatos ricos), accesibles (protocolos abiertos), interoperables (vocabularios normalizados) y reutilizables (licencia y procedencia claras). Proporciona la vara de medir la estabilidad y reutilización de una fuente de datos.
- **Uso en el Motor:** AG-B16 y Documentadores: principios FAIR para los conjuntos de datos y artefactos de cálculo del Motor (identificadores, metadatos, licencia, procedencia).
- **Limitaciones:** Principios, no métricas; su aplicación concreta requiere indicadores adicionales.
- **Origen:** Alta V4.0 (2026-11-02), segunda tanda de verificación. Reutilizada en F8 del Bloque B V2.0 (TMB-14) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0472 · Q 92 (A) — The Extent and Consequences of P-Hacking in Science

- **Autores:** Megan L. Head; Luke Holman; Rob Lanfear; Andrew T. Kahn; Michael D. Jennions
- **Año:** 2015
- **Publicación o institución:** PLOS Biology, 13(3), e1002106
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-14 Datos, calidad y reproducibilidad (principal) · secundarias: TMB-11
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** DOI: 10.1371/journal.pbio.1002106 · https://en.wikipedia.org/wiki/Data_dredging (bibliografía)
- **Acceso y licencia:** Acceso abierto (PLoS; PMC4359000)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Data dredging" wikipedia data snooping White reality check»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Data_dredging)
- **Contenido:** Con minería de textos de p-valores publicados, detecta p-hacking extendido aunque de efecto limitado en los metaanálisis.
- **Uso en el Motor:** MC-B10 y Auditor: alcance del p-hacking; justifica el registro previo de criterios de cribado.
- **Limitaciones:** Disciplinas biomédicas y biológicas.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-14) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0129 · Q 92 (A) — Why Most Published Research Findings Are False

- **Autores:** John P. A. Ioannidis
- **Año:** 2005
- **Publicación o institución:** PLoS Medicine, 2(8), e124
- **Tipo de documento:** Artículo revisado por pares (ensayo)
- **Temática:** TMB-14 Datos, calidad y reproducibilidad (principal) · secundarias: TMB-11
- **Calidad Q:** 92 (A) — Tipo 23/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** DOI: 10.1371/journal.pmed.0020124 · https://en.wikipedia.org/wiki/Data_dredging (bibliografía)
- **Acceso y licencia:** Acceso abierto (PLoS; PMC1182327)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Data dredging" wikipedia data snooping White reality check»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Data_dredging)
- **Contenido:** Muestra que la probabilidad de que un hallazgo publicado sea cierto baja con poca potencia, efectos pequeños, muchos contrastes, flexibilidad analítica y competencia entre equipos.
- **Uso en el Motor:** Auditor y MC-B10: por qué muchos hallazgos son falsos; probabilidad a priori de señales sectoriales.
- **Limitaciones:** Modelo conceptual.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-14) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0125 · Q 92 (A) — A Real-Time Data Set for Macroeconomists

- **Autores:** Dean Croushore; Tom Stark
- **Año:** 2001
- **Publicación o institución:** Journal of Econometrics, 105, 111-130
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-14 Datos, calidad y reproducibilidad (principal) · secundarias: TMB-11
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** https://facultystaff.richmond.edu/~dcrousho/docs/Croushore%20Real%20Time%20Frontiers%2009Dec.pdf (bibliografía); base de datos en la Reserva Federal de Filadelfia
- **Acceso y licencia:** Artículo de pago en el editor; versiones de trabajo en philadelphiafed.org
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Philadelphia Fed Real-Time Data Set for Macroeconomists Croushore Stark»; WebFetch: sí, sobre la página índice https://facultystaff.richmond.edu/~dcrousho/docs/Croushore%20Real%20Time%20Frontiers%2009Dec.pdf)
- **Contenido:** Presenta la base de datos de la Reserva Federal de Filadelfia con las «añadas» (vintages) de las series macro tal como se conocían en cada fecha.
- **Uso en el Motor:** MC-B01 y MC-B10: datos en tiempo real (vintages) para evitar sesgo de anticipación en pronósticos macro-sectoriales.
- **Limitaciones:** Datos estadounidenses. El DOI de la semilla no se ha visto y se retira.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-14) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0465 · Q 92 (A) — Monetary Policy Rules Based on Real-Time Data

- **Autores:** Athanasios Orphanides
- **Año:** 2001
- **Publicación o institución:** American Economic Review, 91, 964-985
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-14 Datos, calidad y reproducibilidad (principal) · secundarias: —
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** https://facultystaff.richmond.edu/~dcrousho/docs/Croushore%20Real%20Time%20Frontiers%2009Dec.pdf (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Philadelphia Fed Real-Time Data Set for Macroeconomists Croushore Stark»; WebFetch: sí, sobre la página índice https://facultystaff.richmond.edu/~dcrousho/docs/Croushore%20Real%20Time%20Frontiers%2009Dec.pdf)
- **Contenido:** Muestra que las reglas de Taylor estimadas con datos revisados describen mal la política real; con datos disponibles en su momento las conclusiones cambian.
- **Uso en el Motor:** MC-B10: ejemplo de cómo los datos revisados cambian las conclusiones; usar vintages en backtests.
- **Limitaciones:** Política de la Reserva Federal.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-14) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0124 · Q 92 (A) — Survivorship Bias in Performance Studies

- **Autores:** Stephen J. Brown; William N. Goetzmann; Roger G. Ibbotson; Stephen A. Ross
- **Año:** 1992
- **Publicación o institución:** The Review of Financial Studies, 5, 553-580
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-14 Datos, calidad y reproducibilidad (principal) · secundarias: TMB-11
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** https://archive.nyu.edu/bitstream/2451/27418/2/S-AM-00-08.pdf (bibliografía de Carhart et al., DOC-MOT-0469)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Survivorship bias" en.wikipedia.org mutual funds»; WebFetch: sí, sobre la página índice https://archive.nyu.edu/bitstream/2451/27418/2/S-AM-00-08.pdf)
- **Contenido:** Muestra que el sesgo de supervivencia puede generar una persistencia aparente de resultados en fondos aunque no exista.
- **Uso en el Motor:** MC-B10 y AG-B12: sesgo de supervivencia en bases de rentabilidad; exigir universos con empresas y fondos desaparecidos.
- **Limitaciones:** Contexto de fondos de inversión. El DOI de la semilla no se ha visto en la verificación y se retira.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-14) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### fondo_entry_210 · Q 91 (A) — Is Economics Research Replicable? Sixty Published Papers From Thirteen Journals Say «Often Not»

- **Cita normalizada:** Chang, A. C., y Li, P. (2022). Is Economics Research Replicable? Sixty Published Papers From Thirteen Journals Say «Often Not». Critical Finance Review, 11(1), 185-206. Versión previa: Finance and Economics Discussion Series 2015-083, Board of Governors of the Federal Reserve System («Usually Not»).
- **Tipo de documento:** Artículo revisado por pares (con documento de trabajo de banco central)
- **Temática:** TMB-14 Datos, calidad y reproducibilidad (principal) · secundarias: —
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 13/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 10/10 · Acceso 9/10
- **DOI / URL:** DOI: 10.1561/104.00000053 · https://nowpublishers.com/article/Details/CFR-0053 · FEDS 2015-083, DOI: 10.17016/FEDS.2015.083: https://www.federalreserve.gov/econres/feds/is-economics-research-replicable-sixty-published-papers-from-thirteen-journals-say-quotusually-notquot.htm
- **Acceso y licencia:** Documento de trabajo FEDS gratuito (con materiales de replicación); versión de revista en Now Publishers
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Chang Li "Is Economics Research Replicable? Sixty Published Papers from Thirteen Journals Say Often Not" Federal Reserve FEDS»; WebFetch: sí (Fed y Now Publishers))
- **Contenido:** Intenta reproducir 67 artículos de macroeconomía de 13 revistas con los datos y el código de los autores: sin ayuda de los autores reproduce el resultado cualitativo principal en 22 de 67 (33 %), y con su ayuda en 29 de 59 (49 %); las revistas que exigen ficheros de replicación los tienen en 29 de 35 casos frente a 11 de 26. Base empírica para exigir datos y código disponibles como señal de verificabilidad.
- **Uso en el Motor:** Auditor y MC-B10: evidencia de baja replicabilidad sin código y datos; exigir ambos en cada artefacto de cálculo.
- **Limitaciones:** Solo macroeconomía empírica; reproducción con los materiales originales, no replicación con datos nuevos.
- **Origen:** Alta V4.0 (2026-11-02), segunda tanda de verificación. Reutilizada en F8 del Bloque B V2.0 (TMB-14) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0471 · Q 91 (A) — The ASA Statement on p-Values: Context, Process, and Purpose

- **Autores:** Ronald L. Wasserstein; Nicole A. Lazar
- **Año:** 2016
- **Publicación o institución:** The American Statistician, 70(2), 129-133
- **Tipo de documento:** Declaración institucional revisada (American Statistical Association)
- **Temática:** TMB-14 Datos, calidad y reproducibilidad (principal) · secundarias: —
- **Calidad Q:** 91 (A) — Tipo 23/25 · Rigor 14/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** DOI: 10.1080/00031305.2016.1154108 · https://en.wikipedia.org/wiki/Data_dredging (bibliografía)
- **Acceso y licencia:** Acceso abierto (Taylor & Francis)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Data dredging" wikipedia data snooping White reality check»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Data_dredging)
- **Contenido:** Seis principios de la ASA sobre el uso e interpretación de los p-valores: no miden la probabilidad de la hipótesis ni el tamaño del efecto, y no deben usarse solos para decidir.
- **Uso en el Motor:** Auditor y MC-B10: uso correcto de p-valores en los informes del Motor.
- **Limitaciones:** Principios generales, no un procedimiento.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-14) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0468 · Q 91 (A) — Survivorship Bias and Mutual Fund Performance

- **Autores:** Edwin J. Elton; Martin J. Gruber; Christopher R. Blake
- **Año:** 1996
- **Publicación o institución:** The Review of Financial Studies, 9(4), 1097-1120
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-14 Datos, calidad y reproducibilidad (principal) · secundarias: TMB-11
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.1093/rfs/9.4.1097 · https://en.wikipedia.org/wiki/Survivorship_bias (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Survivorship bias" en.wikipedia.org mutual funds»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Survivorship_bias)
- **Contenido:** Cuantifica el sesgo de supervivencia en rentabilidades de fondos de inversión y su efecto sobre las medidas de rendimiento.
- **Uso en el Motor:** MC-B10: magnitud del sesgo de supervivencia en fondos; corrección para el cribado de ETF y fondos.
- **Limitaciones:** Fondos estadounidenses.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-14) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0473 · Q 89 (A) — P-Curve: A Key to the File-Drawer

- **Autores:** Uri Simonsohn; Leif D. Nelson; Joseph P. Simmons
- **Año:** 2014
- **Publicación o institución:** Journal of Experimental Psychology: General, 143(2), 534-547
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-14 Datos, calidad y reproducibilidad (principal) · secundarias: —
- **Calidad Q:** 89 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.1037/a0033242 · https://en.wikipedia.org/wiki/Data_dredging (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Data dredging" wikipedia data snooping White reality check»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Data_dredging)
- **Contenido:** Propone la curva p (distribución de p-valores significativos) para distinguir efectos reales de resultados seleccionados o manipulados.
- **Uso en el Motor:** Auditor: curva p para detectar selección de resultados en la literatura que respalda una tesis.
- **Limitaciones:** Requiere p-valores independientes y bien reportados.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-14) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0469 · Q 89 (A) — Mutual Fund Survivorship

- **Autores:** Mark M. Carhart; Jennifer N. Carpenter; Anthony W. Lynch; David K. Musto
- **Año:** 2000 (versión de 12-09-2000; primer borrador de 1994)
- **Publicación o institución:** NYU Stern (documento de trabajo; repositorio archive.nyu.edu)
- **Tipo de documento:** Documento de trabajo de institución reconocida
- **Temática:** TMB-14 Datos, calidad y reproducibilidad (principal) · secundarias: TMB-11
- **Calidad Q:** 89 (A) — Tipo 20/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** https://archive.nyu.edu/bitstream/2451/27418/2/S-AM-00-08.pdf
- **Acceso y licencia:** Acceso abierto (repositorio de NYU)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «"Survivorship bias" en.wikipedia.org mutual funds»; WebFetch: sí)
- **Contenido:** Los fondos con malos resultados desaparecen tras varios años, de modo que el sesgo de supervivencia crece con la longitud de la muestra y distorsiona la persistencia medida.
- **Uso en el Motor:** MC-B10: base y método para tratar fondos desaparecidos en estudios de rendimiento.
- **Limitaciones:** Versión de trabajo; no se confirmó la publicación en revista.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-14) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### MBM-0269 · Q 88 (A) — Ten Simple Rules for Reproducible Computational Research

- **Autores:** Geir Kjetil Sandve; Anton Nekrutenko; James Taylor; Eivind Hovig
- **Año:** 2013
- **Publicación o institución:** PLoS Computational Biology, vol. 9, n.º 10, e1003285
- **Tipo de documento:** Artículo revisado por pares (guía)
- **Temática:** TMB-14 Datos, calidad y reproducibilidad (principal) · secundarias: TMB-08
- **Calidad Q:** 88 (A) — Tipo 23/25 · Rigor 14/20 · Autoridad 13/15 · Vigencia 8/10 · Impacto 10/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** DOI: 10.1371/journal.pcbi.1003285 · https://pure.psu.edu/en/publications/ten-simple-rules-for-reproducible-computational-research/ · PDF: https://hpc.ilri.cgiar.org/beca/training/AdvancedBFX2014_2/course/Reproducible-Computational-Research.pdf
- **Acceso y licencia:** Acceso abierto (CC BY)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Peng 2011 "Reproducible Research in Computational Science" Science; Sandve 2013 "Ten Simple Rules for Reproducible Computational Research" PLOS Computational Biology»; WebFetch: sí, ficha del repositorio de Penn State y PDF)
- **Contenido:** Diez reglas: registrar cómo se produjo cada resultado, evitar pasos manuales, archivar versiones de programas, control de versiones, guardar intermedios, registrar semillas aleatorias, etc.
- **Uso en el Motor:** AG-B16 y MC-B08: lista de control del artefacto de cálculo (semillas, versiones, pasos automatizados, datos intermedios).
- **Limitaciones:** Orientado a bioinformática.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### MBM-0271 · Q 88 (A) — The Delisting Bias in CRSP Data

- **Autores:** Tyler Shumway
- **Año:** 1997
- **Publicación o institución:** Journal of Finance, vol. 52, n.º 1, págs. 327-340
- **Tipo de documento:** Artículo revisado por pares (revista de primer nivel)
- **Temática:** TMB-14 Datos, calidad y reproducibilidad (principal) · secundarias: TMB-11
- **Calidad Q:** 88 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 10/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** https://ideas.repec.org/a/bla/jfinan/v52y1997i1p327-40.html
- **Acceso y licencia:** De pago (Wiley)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Shumway 1997 "The Delisting Bias in CRSP Data" Journal of Finance; Ljungqvist Malloy Marston "Rewriting History" I/B/E/S»; WebFetch: sí, ficha IDEAS/RePEc)
- **Contenido:** Los rendimientos de exclusión de cotización por causas negativas faltan en CRSP y son muy negativos; omitirlos sesga al alza los resultados.
- **Uso en el Motor:** MC-B10 y AG-B12: imputar rendimientos de exclusión al backtestear criterios de cribado (sin sesgo de supervivencia).
- **Limitaciones:** Específico de CRSP; corregido parcialmente en versiones posteriores.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### DOC-MOT-0467 · Q 88 (A) — Forecasting Output with the Composite Leading Index: A Real-Time Analysis

- **Autores:** Francis X. Diebold; Glenn D. Rudebusch
- **Año:** 1991
- **Publicación o institución:** Journal of the American Statistical Association, 86, 603-610
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-14 Datos, calidad y reproducibilidad (principal) · secundarias: —
- **Calidad Q:** 88 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** https://facultystaff.richmond.edu/~dcrousho/docs/Croushore%20Real%20Time%20Frontiers%2009Dec.pdf (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Philadelphia Fed Real-Time Data Set for Macroeconomists Croushore Stark»; WebFetch: sí, sobre la página índice https://facultystaff.richmond.edu/~dcrousho/docs/Croushore%20Real%20Time%20Frontiers%2009Dec.pdf)
- **Contenido:** Con datos en tiempo real, el índice compuesto de indicadores adelantados pronostica la producción mucho peor que con datos revisados.
- **Uso en el Motor:** MC-B01: ejemplo de evaluación en tiempo real de un indicador adelantado.
- **Limitaciones:** Índice adelantado de EE. UU.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-14) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0476 · Q 87 (A) — Degrees of Freedom in Planning, Running, Analyzing, and Reporting Psychological Studies: A Checklist to Avoid p-Hacking

- **Autores:** Jelte M. Wicherts; Coosje L. S. Veldkamp; Hilde E. M. Augusteijn; Marjan Bakker; Robbie C. M. van Aert; Marcel A. L. M. van Assen
- **Año:** 2016
- **Publicación o institución:** Frontiers in Psychology, 7, 1832
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-14 Datos, calidad y reproducibilidad (principal) · secundarias: —
- **Calidad Q:** 87 (A) — Tipo 23/25 · Rigor 13/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** DOI: 10.3389/fpsyg.2016.01832 · https://en.wikipedia.org/wiki/Data_dredging (bibliografía)
- **Acceso y licencia:** Acceso abierto (Frontiers; PMC5122713)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Data dredging" wikipedia data snooping White reality check»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Data_dredging)
- **Contenido:** Lista de comprobación de 34 grados de libertad del investigador en diseño, análisis e informe que permiten el p-hacking.
- **Uso en el Motor:** Auditor: lista de control de grados de libertad del investigador aplicable a los análisis del Bloque B.
- **Limitaciones:** Pensada para psicología; requiere adaptación a finanzas.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-14) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0461 · Q 87 (A) — Frontiers of Real-Time Data Analysis

- **Autores:** Dean Croushore
- **Año:** 2009 (versión del autor, diciembre de 2009)
- **Publicación o institución:** University of Richmond / Federal Reserve Bank of Philadelphia (versión aceptada tras revisión; la revista no se identifica en el texto)
- **Tipo de documento:** Artículo de revisión
- **Temática:** TMB-14 Datos, calidad y reproducibilidad (principal) · secundarias: —
- **Calidad Q:** 87 (A) — Tipo 20/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** https://facultystaff.richmond.edu/~dcrousho/docs/Croushore%20Real%20Time%20Frontiers%2009Dec.pdf
- **Acceso y licencia:** PDF de acceso abierto en la web del autor
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Philadelphia Fed Real-Time Data Set for Macroeconomists Croushore Stark»; WebFetch: sí)
- **Contenido:** Revisa la investigación con datos en tiempo real: revisiones de datos, modelos estructurales, pronóstico, política monetaria, análisis de coyuntura y conjuntos de datos disponibles.
- **Uso en el Motor:** MC-B01 y MC-B10: panorama del análisis con datos en tiempo real y revisiones.
- **Limitaciones:** Revista de publicación no confirmada; foco en EE. UU.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-14) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0463 · Q 87 (A) — Data Revisions Are Not Well Behaved

- **Autores:** S. Borağan Aruoba
- **Año:** 2008
- **Publicación o institución:** Journal of Money, Credit and Banking, 40, 319-340
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-14 Datos, calidad y reproducibilidad (principal) · secundarias: —
- **Calidad Q:** 87 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** https://facultystaff.richmond.edu/~dcrousho/docs/Croushore%20Real%20Time%20Frontiers%2009Dec.pdf (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Philadelphia Fed Real-Time Data Set for Macroeconomists Croushore Stark»; WebFetch: sí, sobre la página índice https://facultystaff.richmond.edu/~dcrousho/docs/Croushore%20Real%20Time%20Frontiers%2009Dec.pdf)
- **Contenido:** Muestra que las revisiones de datos macro de EE. UU. tienen media distinta de cero, son predecibles y no son ruido puro.
- **Uso en el Motor:** MC-B01: propiedades de las revisiones de datos; ajustar la confianza en datos sectoriales preliminares.
- **Limitaciones:** Variables macro estadounidenses.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-14) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0464 · Q 87 (A) — The Use and Abuse of «Real-Time» Data in Economic Forecasting

- **Autores:** Evan F. Koenig; Sheila Dolmas; Jeremy Piger
- **Año:** 2003
- **Publicación o institución:** The Review of Economics and Statistics, 85, 618-628
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-14 Datos, calidad y reproducibilidad (principal) · secundarias: —
- **Calidad Q:** 87 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** https://facultystaff.richmond.edu/~dcrousho/docs/Croushore%20Real%20Time%20Frontiers%2009Dec.pdf (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Philadelphia Fed Real-Time Data Set for Macroeconomists Croushore Stark»; WebFetch: sí, sobre la página índice https://facultystaff.richmond.edu/~dcrousho/docs/Croushore%20Real%20Time%20Frontiers%2009Dec.pdf)
- **Contenido:** Muestra que estimar modelos de pronóstico con datos de la primera publicación (en lugar de la última añada) mejora la precisión en tiempo real.
- **Uso en el Motor:** MC-B10: errores al usar datos supuestamente en tiempo real en previsiones.
- **Limitaciones:** Aplicación al PIB de EE. UU.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-14) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0474 · Q 86 (A) — The Credibility Crisis in Research: Can Economics Tools Help?

- **Autores:** Thomas Gall; John P. A. Ioannidis; Zacharias Maniadis
- **Año:** 2017
- **Publicación o institución:** PLOS Biology, 15(4), e2001846
- **Tipo de documento:** Artículo revisado por pares (ensayo)
- **Temática:** TMB-14 Datos, calidad y reproducibilidad (principal) · secundarias: —
- **Calidad Q:** 86 (A) — Tipo 23/25 · Rigor 13/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 6/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** DOI: 10.1371/journal.pbio.2001846 · https://en.wikipedia.org/wiki/Data_dredging (bibliografía)
- **Acceso y licencia:** Acceso abierto (PLoS; PMC5405914)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Data dredging" wikipedia data snooping White reality check»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Data_dredging)
- **Contenido:** Analiza con herramientas económicas (incentivos, diseño de mecanismos) las causas de la crisis de credibilidad y propone reformas.
- **Uso en el Motor:** Auditor: herramientas económicas frente a la crisis de credibilidad (registro previo, incentivos).
- **Limitaciones:** Ensayo conceptual.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-14) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0466 · Q 86 (A) — News and Noise in G-7 GDP Announcements

- **Autores:** Jon Faust; John H. Rogers; Jonathan H. Wright
- **Año:** 2005
- **Publicación o institución:** Journal of Money, Credit and Banking, 37, 403-419
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-14 Datos, calidad y reproducibilidad (principal) · secundarias: —
- **Calidad Q:** 86 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 7/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** https://facultystaff.richmond.edu/~dcrousho/docs/Croushore%20Real%20Time%20Frontiers%2009Dec.pdf (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Philadelphia Fed Real-Time Data Set for Macroeconomists Croushore Stark»; WebFetch: sí, sobre la página índice https://facultystaff.richmond.edu/~dcrousho/docs/Croushore%20Real%20Time%20Frontiers%2009Dec.pdf)
- **Contenido:** Analiza las revisiones del PIB en los países del G-7 y si los anuncios iniciales son noticia o ruido; en varios países las revisiones son predecibles.
- **Uso en el Motor:** MC-B01: noticias frente a ruido en las revisiones del PIB; tratamiento de datos preliminares.
- **Limitaciones:** Periodo de los años 80-90.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-14) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### DOC-MOT-0475 · Q 85 (A) — The Power of Tests for Detecting p-Hacking

- **Autores:** Graham Elliott; Nikolay Kudrin; Kaspar Wüthrich
- **Año:** 2025
- **Publicación o institución:** The Review of Economics and Statistics
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-14 Datos, calidad y reproducibilidad (principal) · secundarias: —
- **Calidad Q:** 85 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 4/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.1162/REST.a.1688 · https://en.wikipedia.org/wiki/Data_dredging (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Data dredging" wikipedia data snooping White reality check»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Data_dredging)
- **Contenido:** Evalúa teóricamente y por simulación la potencia de los contrastes de p-hacking según la forma de manipulación y el sesgo de publicación.
- **Uso en el Motor:** Auditor: potencia de los tests de p-hacking.
- **Limitaciones:** Reciente; volumen y páginas no figuran en la fuente.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-14) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### MBM-0272 · Q 85 (A) — Rewriting History

- **Autores:** Alexander Ljungqvist; Christopher Malloy; Felicia Marston
- **Año:** 2008
- **Publicación o institución:** NYU Stern Finance Working Paper FIN-06-004
- **Tipo de documento:** Documento de trabajo
- **Temática:** TMB-14 Datos, calidad y reproducibilidad (principal) · secundarias: TMB-11
- **Calidad Q:** 85 (A) — Tipo 18/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 9/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** http://hdl.handle.net/2451/27384 · https://archive.nyu.edu/handle/2451/27384
- **Acceso y licencia:** Acceso abierto (repositorio NYU)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Shumway 1997 "The Delisting Bias in CRSP Data" Journal of Finance; Ljungqvist Malloy Marston "Rewriting History" I/B/E/S»; WebFetch: sí, registro completo en el repositorio de NYU)
- **Contenido:** Comparando siete descargas de I/B/E/S (2000-2007) halla que entre el 1,6 % y el 21,7 % de los registros cambiaron, de forma no aleatoria, alterando backtests de señales de analistas.
- **Uso en el Motor:** MC-B10 y TMB-14: usar instantáneas fechadas de las bases de datos y registrar la versión usada en cada backtest de selección.
- **Limitaciones:** Versión de trabajo; publicación posterior no comprobada.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### DOC-MOT-0470 · Q 84 (A) — The J-Shape of Performance Persistence Given Survivorship Bias

- **Autores:** Darryll Hendricks; Jayendu Patel; Richard Zeckhauser
- **Año:** 1996
- **Publicación o institución:** The Review of Economics and Statistics
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMB-14 Datos, calidad y reproducibilidad (principal) · secundarias: TMB-11
- **Calidad Q:** 84 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 7/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** https://archive.nyu.edu/bitstream/2451/27418/2/S-AM-00-08.pdf (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Survivorship bias" en.wikipedia.org mutual funds»; WebFetch: sí, sobre la página índice https://archive.nyu.edu/bitstream/2451/27418/2/S-AM-00-08.pdf)
- **Contenido:** Muestra que el sesgo de supervivencia puede producir una relación en forma de J entre rentabilidad pasada y futura, imitando persistencia.
- **Uso en el Motor:** MC-B10: sesgo de supervivencia que crea persistencia aparente en forma de J.
- **Limitaciones:** Volumen y páginas no figuran en la fuente consultada.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-14) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### MBM-0268 · Q 83 (A) — Reproducible Research in Computational Science

- **Autores:** Roger D. Peng
- **Año:** 2011
- **Publicación o institución:** Science, vol. 334, págs. 1226-1227
- **Tipo de documento:** Artículo de perspectiva revisado
- **Temática:** TMB-14 Datos, calidad y reproducibilidad (principal) · secundarias: TMB-11
- **Calidad Q:** 83 (A) — Tipo 21/25 · Rigor 14/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** Página índice: https://hpc.ilri.cgiar.org/beca/training/AdvancedBFX2014_2/course/Reproducible-Computational-Research.pdf (bibliografía de Sandve et al., 2013)
- **Acceso y licencia:** De pago (AAAS)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Peng 2011 "Reproducible Research in Computational Science" Science; Sandve 2013 "Ten Simple Rules for Reproducible Computational Research" PLOS Computational Biology»; WebFetch: sí, PDF de Sandve et al. (2013) con su bibliografía)
- **Contenido:** Propone un espectro de reproducibilidad (de solo publicación a código y datos enlazados y ejecutables) como estándar mínimo en ciencia computacional.
- **Uso en el Motor:** AG-B16 y Auditor: nivel mínimo exigido a cada artefacto de cálculo del Motor (código, datos y versión enlazados).
- **Limitaciones:** Texto breve de opinión.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### DOC-MOT-0462 · Q 80 (A) — A Funny Thing Happened on the Way to the Data Bank: A Real-Time Data Set for Macroeconomists

- **Autores:** Dean D. Croushore; Tom Stark
- **Año:** 2000
- **Publicación o institución:** Federal Reserve Bank of Philadelphia, Business Review, sept.-oct. 2000, 15-27
- **Tipo de documento:** Artículo divulgativo de banco central
- **Temática:** TMB-14 Datos, calidad y reproducibilidad (principal) · secundarias: —
- **Calidad Q:** 80 (A) — Tipo 15/25 · Rigor 14/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 7/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://scholarship.richmond.edu/economics-faculty-publications/8
- **Acceso y licencia:** Acceso abierto (repositorio de la Universidad de Richmond)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Philadelphia Fed Real-Time Data Set for Macroeconomists Croushore Stark»; WebFetch: sí)
- **Contenido:** Explica cómo se construyó la base de datos en tiempo real, cuánto se revisan los datos y cómo cambian los resultados de pronóstico e investigación con datos revisados.
- **Uso en el Motor:** MC-B01: base de datos en tiempo real del Fed de Filadelfia como fuente de vintages.
- **Limitaciones:** Texto divulgativo.
- **Origen:** Ficha verificada del archivo fuente, reutilizada en F8 del Bloque B V2.0 (TMB-14) el 2026-11-02 con su ID original; Temática y Uso adaptados.

#### MBM-0273 · Q 78 (B) — Rewriting CRSP's History: Impact of Altered Monthly Returns on Asset Pricing

- **Autores:** Patrick Schwarz; Dominik Walter; Patrick Weiss
- **Año:** 2026
- **Publicación o institución:** Manuscrito alojado en jfqa.org (versión del 24-02-2026)
- **Tipo de documento:** Documento de trabajo (manuscrito)
- **Temática:** TMB-14 Datos, calidad y reproducibilidad (principal) · secundarias: TMB-07
- **Calidad Q:** 78 (B) — Tipo 17/25 · Rigor 16/20 · Autoridad 12/15 · Vigencia 10/10 · Impacto 4/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** https://jfqa.org/wp-content/uploads/2026/02/26501_Rewriting_CRSP_History.pdf
- **Acceso y licencia:** Acceso abierto
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Shumway 1997 "The Delisting Bias in CRSP Data" Journal of Finance; Ljungqvist Malloy Marston "Rewriting History" I/B/E/S»; WebFetch: sí, PDF del manuscrito)
- **Contenido:** La nueva cinta de CRSP cambia en al menos 1 pb el 9,6 % de los rendimientos mensuales (reinversión de dividendos en fecha ex); las primas medias apenas varían, con excepciones.
- **Uso en el Motor:** MC-B10 y MC-B07: registrar la versión de la base de datos y comprobar la estabilidad de las señales de cribado entre versiones.
- **Limitaciones:** Manuscrito; estado de publicación no confirmado.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

#### MBM-0270 · Q 76 (B) — Accessible Reproducible Research

- **Autores:** Jill P. Mesirov
- **Año:** 2010
- **Publicación o institución:** Science, vol. 327, págs. 415-416
- **Tipo de documento:** Artículo de perspectiva revisado
- **Temática:** TMB-14 Datos, calidad y reproducibilidad (principal) · secundarias: —
- **Calidad Q:** 76 (B) — Tipo 20/25 · Rigor 13/20 · Autoridad 14/15 · Vigencia 7/10 · Impacto 8/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** Página índice: https://hpc.ilri.cgiar.org/beca/training/AdvancedBFX2014_2/course/Reproducible-Computational-Research.pdf (bibliografía de Sandve et al., 2013)
- **Acceso y licencia:** De pago (AAAS)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Peng 2011 "Reproducible Research in Computational Science" Science; Sandve 2013 "Ten Simple Rules for Reproducible Computational Research" PLOS Computational Biology»; WebFetch: sí, PDF de Sandve et al. (2013) con su bibliografía)
- **Contenido:** Propone sistemas que vinculen el documento con el entorno de cálculo que produjo cada resultado.
- **Uso en el Motor:** AG-B16: enlazar cada cifra del informe con el artefacto de cálculo que la generó.
- **Limitaciones:** Breve.
- **Origen:** Alta nueva de DOC-M (Bloque B V2.0, F8) el 2026-11-02.

## Lagunas de cobertura

Áreas con menos de 20 referencias verificadas tras la emisión V2.0 del 02/11/2026 (objetivo del propietario: 20–50 por área):

| Código | Temática | Verificadas | Faltan para 20 |
|---|---|---|---|
| — | Ninguna | — | — |

## Registro de bajas

| REF-id | Título | Motivo | Fecha | Sustituta |
|---|---|---|---|---|

## Historial de versión

| Versión | Fecha | Cambio |
|---|---|---|
| V1.2 | 31/10/2026 | Esquema sin fichas (paquete del propietario, conservado en 99_Historico_V1.3). |
| V2.0 | 02/11/2026 | Primera carga de fichas del Bloque B V2.0: 410 fichas (reutilizadas de los Bloques A con su ID original, y nuevas verificadas por búsqueda web con prefijo MB); 0 bajas; orden por temática y Q; índice con recuento de verificadas. |

