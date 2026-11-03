# Archivo operativo F8 — Documentación para el Motor de Cálculo Avanzado (Forex)

**Bloque A Forex · Robot Investor · Versión óptima V1.0 · 02/11/2026** · Subordinado al Documento 0 del Bloque A Forex V1.0.

**Versión del archivo:** V1.0 (02/11/2026), alineada con el Documento 0 del Bloque A Forex V1.0 · **Código:** F8 · **Propietario:** AG-15 Documentador para el Motor de Cálculo Avanzado (DOC-M) · **Alcance:** ecosistémico (lo reutilizan los bloques posteriores)

## Cómo usar este archivo

**Propósito.** Archivo específico del mercado de divisas (taxonomía TMX del Anexo D del Documento 0 Forex); incluye referencias reutilizadas del Bloque A general (conservan su ID) y referencias nuevas (prefijo FXM-).  Fondo de referencias de métodos cuantitativos (estadística, series temporales, econometría, valoración, derivados, carteras, riesgo, simulación, aprendizaje automático, evaluación predictiva y métodos específicos de divisas) que respalda cada servicio del Motor (MC-01 a MC-10) y la evaluación de pronósticos.

**Propietario y acceso.** Escribe solo AG-15 (DOC-M). Leen: AG-13 Motor, AG-14, AG-12 Curador, Orquestador, Auditor y Evaluador. Cualquier otro acceso es una incidencia (Documento 0, 5.2).

**Reglas de uso.**

1. **Lectura.** Lea primero «Novedades»; después el índice de temáticas; dentro de la temática, las fichas aparecen **ordenadas por Q descendente** (a igualdad, la más reciente primero). Cite siempre el ID de la ficha. Para corroboración (PS1) solo cuentan fichas de nivel A o B con `Estado del enlace` distinto de `ROTO`; una ficha `PENDIENTE_VERIFICACION_ALTA` no sustenta evidencia hasta que su propietario la confirme.
2. **Calidad.** Q (0–100) con la rúbrica 13.3: Tipo y revisión 25 · Rigor y transparencia 20 · Autoridad 15 · Vigencia 10 · Impacto 10 · Independencia 10 · Accesibilidad y estabilidad 10. Niveles: A (Q ≥ 80), B (65–79), C (50–64), D (< 50: candidata a baja salvo que sea la única fuente de un dato necesario, declarado). En las semillas la Q es provisional hasta la verificación de alta.
3. **Estados del enlace** (HT-02, barrido semanal del domingo): `OK`, `REDIRIGIDO`, `ROTO` (4xx/5xx en dos intentos separados 24 h), `MURO_PAGO`, `CONTENIDO_CAMBIADO` (similitud < 0,8 frente a la copia archivada) y `PENDIENTE_BARRIDO` (estado inicial de esta versión: ningún enlace se ha comprobado aún con HT-02). `Última verificación` recoge la última comprobación documentada, no una del barrido.
4. **Acciones** (potestad plena del propietario, R19): `REPARAR` (DOI, nueva URL oficial o copia archivada; obligatoria cuando la ficha lleva «Alerta»); `DEGRADAR` (bajar Q o nivel, con motivo); `BORRAR` cuando haya enlace roto sin alternativa tras dos barridos, contenido retirado o retractado, falsedad o manipulación demostrada, redundancia total con una ficha de mayor Q, o Q < 50 sin uso en 180 días. Cada borrado añade una línea al «Registro de bajas»; si la ficha sustentaba EVD de F2 se avisa al Curador (CT-11, tipo `fuente_retirada`).
5. **Ciclo.** DOC-M alimenta el archivo por su agenda de vigilancia y por las peticiones del Motor (CT-20); antes de buscar aplica el Fondo metodológico (R20). El Motor cita el ID de la ficha en el artefacto de cada cálculo (RC). Mensualmente el propietario informa al Orquestador de altas, reparaciones, bajas, salud de enlaces y lagunas (CT-21). Los IDs son inmutables y no se reutilizan; en el «Registro de bajas», «REF-id» es el ID propio de la ficha.

**Semillas.** Las fichas con `Estado: PENDIENTE_VERIFICACION_ALTA` son obras canónicas añadidas en V3.0 para cubrir lagunas evidentes. Sus identificadores (DOI, ISBN, URL) proceden de conocimiento previo y llevan la marca «a verificar»: no están verificadas y no pueden citarse como respaldo de un cálculo hasta que DOC-M las confirme con HT-02.

## Índice de temáticas (Anexo D, TMX-)

| Código | Temática | Referencias | Verificadas | Pendientes de verificación | A | B | C | D | Q medio |
|---|---|---|---|---|---|---|---|---|---|
| TMX-01 | Series temporales de tipos de cambio: raíces unitarias, cointegración, no linealidad y cambios de régimen | 23 | 23 | 0 | 18 | 5 | 0 | 0 | 87,6 |
| TMX-02 | Volatilidad cambiaria: GARCH, volatilidad realizada y alta frecuencia | 23 | 23 | 0 | 20 | 3 | 0 | 0 | 90,4 |
| TMX-03 | Paridades y cálculo cambiario: CIP, puntos forward, base cruzada y convenciones | 25 | 25 | 0 | 20 | 5 | 0 | 0 | 84,8 |
| TMX-04 | Modelos cuantitativos de equilibrio y valoración | 24 | 24 | 0 | 12 | 12 | 0 | 0 | 82,3 |
| TMX-05 | Opciones de divisas: Garman-Kohlhagen, superficie de volatilidad, risk reversals y densidades implícitas | 27 | 27 | 0 | 21 | 5 | 1 | 0 | 82,5 |
| TMX-06 | Factores cambiarios y construcción de carteras | 28 | 28 | 0 | 26 | 2 | 0 | 0 | 90,2 |
| TMX-07 | Riesgo de cola, saltos y valores extremos en divisas | 29 | 29 | 0 | 28 | 1 | 0 | 0 | 89,9 |
| TMX-08 | Evaluación predictiva frente al paseo aleatorio y backtesting cambiario | 39 | 39 | 0 | 38 | 1 | 0 | 0 | 87,8 |
| TMX-09 | Aprendizaje automático y análisis de texto para divisas | 26 | 26 | 0 | 22 | 3 | 1 | 0 | 87,0 |
| **Total** | — | **244** | **244** | 0 | 205 | 37 | 2 | 0 | 87,0 |

«Verificadas»: enlace en estado OK, REDIRIGIDO, MURO_PAGO o VERIFICADO_BUSQUEDA (existencia y datos confirmados por búsqueda web el 02/11/2026), o verificación documental completa en una carga anterior (25–26/10/2026), pendiente solo del barrido automático HT-02. «Pendientes»: semillas aún en PENDIENTE_VERIFICACION_ALTA o fichas con alerta sin resolver.

## Novedades

- 02/11/2026: emisión inicial V1.0 del archivo específico de divisas.

## TMX-01 Series temporales de tipos de cambio: raíces unitarias, cointegración, no linealidad y cambios de régimen

#### DOC-MOT-0024 · Q 95 (A) — Estimating and Testing Linear Models with Multiple Structural Changes

- **Autores:** Jushan Bai; Pierre Perron
- **Año:** 1998
- **Publicación o institución:** Econometrica, 66(1), 47-78
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-01 Series temporales de tipos de cambio: raíces unitarias, cointegración, no linealidad y cambios de régimen (principal) · secundarias: TMX-04
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** https://ideas.repec.org/a/ecm/emetrp/v66y1998i1p47-78.html · registro de la Econometric Society: https://www.econometricsociety.org/publications/econometrica/1998/01/01/estimating-and-testing-linear-models-multiple-structural (DOI no visto)
- **Acceso y licencia:** Ficha RePEc abierta; texto en Econometrica/JSTOR por suscripción (versión de trabajo del Département de sciences économiques de Montréal listada en RePEc)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Bai Perron 1998 "Estimating and Testing Linear Models with Multiple Structural Changes" Econometrica 66»; WebFetch: sí)
- **Contenido:** Teoría asintótica para estimar por mínimos cuadrados múltiples rupturas en fechas desconocidas, con contrastes supF, doble máximo (UDmax, WDmax) y secuencial ℓ frente a ℓ+1 para determinar el número de rupturas.
- **Uso en el Motor:** MC-02: fechado de rupturas múltiples (Bai-Perron) en tipos de cambio y diferenciales, p. ej., cambios de régimen cambiario o de banco central; insumo para AS-EMLA/AS-EMEA y TR-BCM.
- **Limitaciones:** Requiere tamaño mínimo de segmento (trimming); potencia baja con rupturas pequeñas; valores críticos no válidos con regresores no estacionarios. El DOI de la semilla (10.2307/2998540) no se ha visto y se retira.
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02. Reutilizada en F8 Forex V1.0 (2026-11-02) desde F8 V3.2.

#### DOC-MOT-0253 · Q 95 (A) — Tests for Parameter Instability and Structural Change with Unknown Change Point

- **Autores:** Donald W. K. Andrews
- **Año:** 1993
- **Publicación o institución:** Econometrica, 61(4), 821-856 (corrigendum: Econometrica 71(1), 2003, 395-397)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-01 Series temporales de tipos de cambio: raíces unitarias, cointegración, no linealidad y cambios de régimen (principal) · secundarias: —
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.2307/2951764 · Verificada en página índice: https://en.wikipedia.org/wiki/Structural_break
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Structural break wikipedia Chow test Andrews 1993 Zivot Andrews Bai Perron references»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Structural_break)
- **Contenido:** Contrastes supremo (sup-Wald, sup-LM, sup-LR) de una ruptura en fecha desconocida, con valores críticos asintóticos según el recorte.
- **Uso en el Motor:** MC-02: contraste de ruptura con punto desconocido (Andrews) en relaciones cambiarias (PPA, BEER, betas al dólar).
- **Limitaciones:** Una sola ruptura; véase Bai-Perron para varias. Confirmada solo mediante página índice (bibliografía de Wikipedia «Structural break»); pendiente de lectura de la fuente primaria.
- **Origen:** Reutilizada en F8 Forex V1.0 (2026-11-02) desde F8 V3.2.

#### DOC-MOT-0040 · Q 95 (A) — Estimation and Hypothesis Testing of Cointegration Vectors in Gaussian Vector Autoregressive Models

- **Autores:** Søren Johansen
- **Año:** 1991
- **Publicación o institución:** Econometrica, 59(6), 1551-1580
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-01 Series temporales de tipos de cambio: raíces unitarias, cointegración, no linealidad y cambios de régimen (principal) · secundarias: TMX-04
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** https://ideas.repec.org/a/ecm/emetrp/v59y1991i6p1551-80.html
- **Acceso y licencia:** Ficha RePEc abierta; texto por suscripción (JSTOR)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Johansen 1991 "Estimation and Hypothesis Testing of Cointegration Vectors in Gaussian Vector Autoregressive Models" Econometrica 59»; WebFetch: sí)
- **Contenido:** Estimación por máxima verosimilitud de VAR con cointegración (rango reducido) y contrastes de traza y máximo autovalor para el número de relaciones de cointegración, con restricciones lineales sobre los vectores.
- **Uso en el Motor:** MC-03: cointegración multivariante de Johansen para sistemas tipo de cambio-precios-tipos de interés (PPA con UIP, BEER); TR-BCM y AS-G10N.
- **Limitaciones:** Sensible al orden del VAR y a la especificación determinista. DOI de la semilla no visto; se retira.
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02. Reutilizada en F8 Forex V1.0 (2026-11-02) desde F8 V3.2.

#### DOC-MOT-0035 · Q 95 (A) — A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle

- **Autores:** James D. Hamilton
- **Año:** 1989
- **Publicación o institución:** Econometrica, 57(2), 357-384
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-01 Series temporales de tipos de cambio: raíces unitarias, cointegración, no linealidad y cambios de régimen (principal) · secundarias: TMX-02
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** Verificada en página índice: https://econweb.ucsd.edu/~jhamilto/palgrav1.pdf
- **Acceso y licencia:** Revista por suscripción (Econometrica/JSTOR)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Markov switching model wikipedia Hamilton 1989 regime switching references»; WebFetch: sí, sobre la página índice https://econweb.ucsd.edu/~jhamilto/palgrav1.pdf)
- **Contenido:** Introduce el modelo autorregresivo con cambio de régimen markoviano y el filtro de Hamilton para obtener probabilidades filtradas y suavizadas de cada régimen; aplicación a recesiones de EE. UU.
- **Uso en el Motor:** MC-02: modelo de cambio de régimen markoviano (Hamilton) para tendencias y fases de dólar fuerte/débil; base del modelo de Engel y Hamilton (1990) para el dólar.
- **Limitaciones:** Número de regímenes fijado a priori; riesgo de sobreajuste. Confirmada solo mediante página índice (bibliografía de J. D. Hamilton, «Regime-Switching Models», 2005); pendiente de lectura de la fuente primaria. DOI de la semilla no visto; se retira.
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02. Reutilizada en F8 Forex V1.0 (2026-11-02) desde F8 V3.2.

#### DOC-MOT-0039 · Q 95 (A) — Co-Integration and Error Correction: Representation, Estimation, and Testing

- **Autores:** Robert F. Engle; Clive W. J. Granger
- **Año:** 1987
- **Publicación o institución:** Econometrica, 55(2), 251-276
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-01 Series temporales de tipos de cambio: raíces unitarias, cointegración, no linealidad y cambios de régimen (principal) · secundarias: TMX-04
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.2307/1913236 · Verificada en página índice: https://en.wikipedia.org/wiki/Cointegration
- **Acceso y licencia:** Revista por suscripción (JSTOR 1913236)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Cointegration wikipedia Engle-Granger Johansen test Phillips-Ouliaris references»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Cointegration)
- **Contenido:** Define la cointegración, el teorema de representación de Granger (equivalencia con modelos de corrección del error) y el método en dos etapas con contraste de raíz unitaria sobre los residuos.
- **Uso en el Motor:** MC-03: cointegración en dos etapas y modelo de corrección del error para tipos de cambio y fundamentos (PPA, BEER); base del perfil PERF-FX-FACT (valor).
- **Limitaciones:** Una sola relación de cointegración; sesgo en muestras cortas. Confirmada solo mediante página índice (bibliografía de Wikipedia «Cointegration»); pendiente de lectura de la fuente primaria.
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02 (DOI confirmado en índice). Reutilizada en F8 Forex V1.0 (2026-11-02) desde F8 V3.2.

#### DOC-MOT-0027 · Q 94 (A) — Testing the Null Hypothesis of Stationarity against the Alternative of a Unit Root

- **Autores:** Denis Kwiatkowski; Peter C. B. Phillips; Peter Schmidt; Yongcheol Shin
- **Año:** 1992
- **Publicación o institución:** Journal of Econometrics, 54(1-3), 159-178; versión de trabajo: Cowles Foundation Discussion Paper 979 (1991)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-01 Series temporales de tipos de cambio: raíces unitarias, cointegración, no linealidad y cambios de régimen (principal) · secundarias: —
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** https://econpapers.repec.org/RePEc:cwl:cwldpp:979 (DOI no visto)
- **Acceso y licencia:** Documento de trabajo de Cowles (Yale) de acceso libre; revista Elsevier por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Kwiatkowski Phillips Schmidt Shin 1992 "Testing the null hypothesis of stationarity against the alternative of a unit root" Journal of Econometrics 54»; WebFetch: sí)
- **Contenido:** Contraste LM (KPSS) con hipótesis nula de estacionariedad en nivel o alrededor de tendencia, basado en sumas parciales de residuos y varianza de largo plazo con núcleo de Bartlett.
- **Uso en el Motor:** MC-02: contraste KPSS (nula de estacionariedad) en confirmación cruzada con ADF para tipos de cambio reales; reduce el riesgo de aceptar una raíz unitaria por baja potencia.
- **Limitaciones:** Sensible a la elección del ancho de banda; distorsiones de tamaño con alta persistencia. La versión de trabajo de Cowles figura con tres autores; la publicada añade a Y. Shin. El DOI de la semilla no se ha visto y se retira.
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02. Reutilizada en F8 Forex V1.0 (2026-11-02) desde F8 V3.2.

#### DOC-MOT-0238 · Q 94 (A) — Asymptotic Properties of Residual Based Tests for Cointegration

- **Autores:** Peter C. B. Phillips; Sam Ouliaris
- **Año:** 1990
- **Publicación o institución:** Econometrica, 58(1), 165-193
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-01 Series temporales de tipos de cambio: raíces unitarias, cointegración, no linealidad y cambios de régimen (principal) · secundarias: —
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.2307/2938339 · Verificada en página índice: https://en.wikipedia.org/wiki/Cointegration
- **Acceso y licencia:** Revista por suscripción (JSTOR 2938339)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Cointegration wikipedia Engle-Granger Johansen test Phillips-Ouliaris references»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Cointegration)
- **Contenido:** Distribuciones asintóticas y valores críticos de contrastes de cointegración basados en residuos (ADF y Phillips sobre residuos, Pu y Pz).
- **Uso en el Motor:** MC-03: valores críticos y propiedades de los contrastes de cointegración basados en residuos (Phillips-Ouliaris) aplicados a pares de divisas y fundamentos.
- **Limitaciones:** Confirmada solo mediante página índice (bibliografía de Wikipedia «Cointegration»); pendiente de lectura de la fuente primaria.
- **Origen:** Reutilizada en F8 Forex V1.0 (2026-11-02) desde F8 V3.2.

#### FXM-0010 · Q 93 (A) — Nonlinear Mean-Reversion in Real Exchange Rates: Toward a Solution to the Purchasing Power Parity Puzzles

- **Autores:** Mark P. Taylor; David A. Peel; Lucio Sarno
- **Año:** 2001
- **Publicación o institución:** International Economic Review, vol. 42, n.º 4, págs. 1015-1042
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-01 Series temporales de tipos de cambio: raíces unitarias, cointegración, no linealidad y cambios de régimen (principal) · secundarias: TMX-04
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1111/1468-2354.00144 · https://profiles.wustl.edu/en/publications/nonlinear-mean-reversion-in-real-exchange-rates-toward-a-solution/
- **Acceso y licencia:** Versión de trabajo en abierto (CEPR DP 2658, repositorio de Warwick); versión publicada por suscripción (Wiley)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Taylor Peel Sarno 2001 nonlinear mean-reversion real exchange rates purchasing power parity puzzles»; WebFetch: sí, ficha de Washington University con DOI)
- **Contenido:** Modelos ESTAR de reversión no lineal de los tipos de cambio reales del dólar justificados por costes de transacción; vidas medias mucho menores para shocks grandes y baja potencia de los contrastes lineales de raíz unitaria.
- **Uso en el Motor:** MC-02 y MC-09: estimación ESTAR de la velocidad de reversión a la PPA según el tamaño de la desviación; señal de valor de AS-ESTR.
- **Limitaciones:** Identificación del umbral y del equilibrio sensible a la muestra y al índice de precios.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### DOC-MOT-0026 · Q 93 (A) — Distribution of the Estimators for Autoregressive Time Series with a Unit Root

- **Autores:** David A. Dickey; Wayne A. Fuller
- **Año:** 1979
- **Publicación o institución:** Journal of the American Statistical Association, 74(366), 427-431
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-01 Series temporales de tipos de cambio: raíces unitarias, cointegración, no linealidad y cambios de régimen (principal) · secundarias: —
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** https://bigenc.ru/b/distribution-of-the-estimators-for-autoregressive-024b8d (ficha bibliográfica; DOI no visto)
- **Acceso y licencia:** Revista (Taylor & Francis/JSTOR) por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Dickey Fuller 1979 "Distribution of the Estimators for Autoregressive Time Series with a Unit Root" JASA 74 366»; WebFetch: sí)
- **Contenido:** Obtiene la distribución límite no estándar del estimador MCO y del estadístico t en un AR(1) con raíz unitaria (con y sin constante y tendencia): base del contraste Dickey-Fuller.
- **Uso en el Motor:** MC-02 y MC-03 (perfiles PERF-FX-G10 y PERF-FX-EM): contraste ADF de raíz unitaria en tipos de cambio reales y nominales antes de estimar vidas medias de PPA o modelos de corrección del error; base para AS-ESTR (valor).
- **Limitaciones:** Baja potencia en muestras cortas y ante rupturas; combinar con KPSS. El DOI de la semilla no se ha visto y se retira; la URL es una ficha bibliográfica, no el texto.
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02. Reutilizada en F8 Forex V1.0 (2026-11-02) desde F8 V3.2.

#### FXM-0031 · Q 92 (A) — Long Swings in the Dollar: Are They in the Data and Do Markets Know It?

- **Autores:** Charles Engel; James D. Hamilton
- **Año:** 1990
- **Publicación o institución:** American Economic Review, vol. 80, n.º 4, págs. 689-713 (versión de trabajo NBER WP 3165)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-01 Series temporales de tipos de cambio: raíces unitarias, cointegración, no linealidad y cambios de régimen (principal) · secundarias: TMX-08
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** https://ideas.repec.org/a/aea/aecrev/v80y1990i4p689-713.html · https://www.nber.org/papers/w3165
- **Acceso y licencia:** Versión de trabajo en abierto (NBER); versión publicada por suscripción (AEA/JSTOR)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Engel Hamilton 1990 "Long swings in the dollar: are they in the data and do markets know it?" American Economic Review»; WebFetch: sí, ficha IDEAS)
- **Contenido:** Modela el tipo de cambio del dólar como tendencias segmentadas con cambio de régimen markoviano («long swings»); rechaza el paseo aleatorio, mejora sus previsiones y rechaza la paridad descubierta.
- **Uso en el Motor:** MC-02: modelo de dos regímenes de tendencia para el dólar y los pares principales (fases de apreciación/depreciación) en PERF-FX-G10 y AS-ESTR (dólar amplio).
- **Limitaciones:** La ventaja frente al paseo aleatorio no es robusta en muestras posteriores (véase «Long Swings in Exchange Rates: Are They Really in the Data?», JBES, vol. 23, 2005).
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0052 · Q 91 (A) — The Purchasing Power Parity Debate

- **Autores:** Alan M. Taylor; Mark P. Taylor
- **Año:** 2004
- **Publicación o institución:** Journal of Economic Perspectives, vol. 18, n.º 4
- **Tipo de documento:** Artículo de revisión revisado por pares
- **Temática:** TMX-01 Series temporales de tipos de cambio: raíces unitarias, cointegración, no linealidad y cambios de régimen (principal) · secundarias: TMX-04
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** Confirmada en la bibliografía de https://ideas.repec.org/p/ecb/ecbwps/20101151.html
- **Acceso y licencia:** Acceso abierto (AEA)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «ECB working paper "Methodological advances in the assessment of equilibrium exchange rates" Bussière Ca' Zorzi Chudik Dieppe»; WebFetch: sí, sobre la página índice https://ideas.repec.org/p/ecb/ecbwps/20101151.html, que reproduce la cita)
- **Contenido:** Revisión de la evidencia sobre la PPA: problemas de potencia de los contrastes de raíz unitaria, paneles, datos largos, no linealidad por costes de transacción y efecto Balassa-Samuelson.
- **Uso en el Motor:** MC-02: guía de los contrastes de reversión del tipo de cambio real y de su interpretación (vidas medias).
- **Limitaciones:** Revisión; no aporta estimaciones nuevas. Confirmada solo mediante página índice; pendiente de lectura de la fuente primaria.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### DOC-MOT-0038 · Q 90 (A) — Regime Changes and Financial Markets

- **Autores:** Andrew Ang; Allan Timmermann
- **Año:** 2012
- **Publicación o institución:** Annual Review of Financial Economics, 4(1), 313-337; versión de trabajo NBER WP 17182 (2011)
- **Tipo de documento:** Artículo de revisión revisado por pares
- **Temática:** TMX-01 Series temporales de tipos de cambio: raíces unitarias, cointegración, no linealidad y cambios de régimen (principal) · secundarias: TMX-06
- **Calidad Q:** 90 (A) — Tipo 22/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** DOI: 10.3386/w17182 (documento de trabajo) · https://www.nber.org/papers/w17182 · https://ideas.repec.org/p/nbr/nberwo/17182.html
- **Acceso y licencia:** Documento de trabajo NBER accesible; revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Ang Timmermann "Regime Changes and Financial Markets" Annual Review of Financial Economics 2012»; WebFetch: sí)
- **Contenido:** Revisión de modelos de cambio de régimen en finanzas: regímenes con medias, volatilidades, autocorrelaciones y covarianzas distintas explican colas gruesas, volatilidad cambiante y correlaciones variables; efectos en valoración y asignación de carteras.
- **Uso en el Motor:** MC-02 y MC-07: revisión de modelos de régimen en finanzas, aplicada a regímenes de riesgo global (risk-on/risk-off) y su efecto en carry y cestas de refugio (AS-ESTR).
- **Limitaciones:** Revisión, no método nuevo. DOI de revista no visto (se da el del documento NBER).
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02. Reutilizada en F8 Forex V1.0 (2026-11-02) desde F8 V3.2.

#### FXM-0080 · Q 90 (A) — Transactions Costs and Nonlinear Adjustment in Real Exchange Rates: An Empirical Investigation

- **Autores:** Panos Michael; A. Robert Nobay; David A. Peel
- **Año:** 1997
- **Publicación o institución:** Journal of Political Economy, vol. 105, n.º 4, págs. 862-879
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-01 Series temporales de tipos de cambio: raíces unitarias, cointegración, no linealidad y cambios de régimen (principal) · secundarias: —
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.1086/262096 · https://ideas.repec.org/a/ucp/jpolec/v105y1997i4p862-79.html
- **Acceso y licencia:** Revista por suscripción (University of Chicago Press)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Michael Nobay Peel 1997 "Transactions costs and nonlinear adjustment in real exchange rates" Journal of Political Economy»; WebFetch: sí, ficha IDEAS con DOI)
- **Contenido:** Con datos mensuales de entreguerras y anuales de larga duración rechaza el ajuste lineal a la PPA en favor de un ESTAR coherente con costes de transacción, con reversión a la media consistente.
- **Uso en el Motor:** MC-02: especificación ESTAR original para tipos de cambio reales; contraste de linealidad previo.
- **Limitaciones:** Muestras históricas.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### DOC-MOT-0242 · Q 90 (A) — Tests for Cointegration in Models with Regime and Trend Shifts

- **Autores:** Allan W. Gregory; Bruce E. Hansen
- **Año:** 1996
- **Publicación o institución:** Oxford Bulletin of Economics and Statistics, 58(3), 555-560
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-01 Series temporales de tipos de cambio: raíces unitarias, cointegración, no linealidad y cambios de régimen (principal) · secundarias: TMX-04
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1111/j.1468-0084.1996.mp58003008.x · Verificada en página índice: https://en.wikipedia.org/wiki/Structural_break
- **Acceso y licencia:** Revista Wiley por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Structural break wikipedia Chow test Andrews 1993 Zivot Andrews Bai Perron references»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Structural_break)
- **Contenido:** Extiende los contrastes residuales de cointegración a una ruptura de fecha desconocida en constante, tendencia o pendiente de la relación.
- **Uso en el Motor:** MC-03: cointegración con ruptura de régimen (Gregory-Hansen), útil cuando un par cambia de régimen cambiario (fin de un tipo fijo, banda o techo) y la relación de equilibrio se desplaza.
- **Limitaciones:** Una sola ruptura. Confirmada solo mediante página índice (bibliografía de Wikipedia «Structural break»); pendiente de lectura de la fuente primaria.
- **Origen:** Reutilizada en F8 Forex V1.0 (2026-11-02) desde F8 V3.2.

#### FXM-0054 · Q 87 (A) — The Purchasing Power Parity Puzzle

- **Autores:** Kenneth Rogoff
- **Año:** 1996
- **Publicación o institución:** Journal of Economic Literature, vol. 34, n.º 2
- **Tipo de documento:** Artículo de revisión revisado por pares
- **Temática:** TMX-01 Series temporales de tipos de cambio: raíces unitarias, cointegración, no linealidad y cambios de régimen (principal) · secundarias: TMX-04
- **Calidad Q:** 87 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 10/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** Confirmada en la bibliografía de https://ideas.repec.org/p/ecb/ecbwps/20101151.html
- **Acceso y licencia:** Revista por suscripción (AEA/JSTOR)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «ECB working paper "Methodological advances in the assessment of equilibrium exchange rates" Bussière Ca' Zorzi Chudik Dieppe»; WebFetch: sí, sobre la página índice https://ideas.repec.org/p/ecb/ecbwps/20101151.html, que reproduce la cita)
- **Contenido:** Formula el enigma de la PPA: vidas medias de 3 a 5 años de las desviaciones del tipo de cambio real, incompatibles con la alta volatilidad a corto plazo si esta procede de shocks nominales.
- **Uso en el Motor:** MC-02: valor de referencia de vidas medias de la PPA frente al que se comparan las estimaciones del Motor.
- **Limitaciones:** Consenso de vidas medias revisado por la literatura no lineal posterior. Confirmada solo mediante página índice; pendiente de lectura de la fuente primaria.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0069 · Q 85 (A) — Cointegration, Fractional Cointegration, and Exchange Rate Dynamics

- **Autores:** Richard T. Baillie; Tim Bollerslev
- **Año:** 1994
- **Publicación o institución:** The Journal of Finance, vol. 49, n.º 2, págs. 737-745
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-01 Series temporales de tipos de cambio: raíces unitarias, cointegración, no linealidad y cambios de régimen (principal) · secundarias: —
- **Calidad Q:** 85 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 8/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** Confirmada en la bibliografía de https://authors.repec.org/pro/pba423/
- **Acceso y licencia:** Revista por suscripción (Wiley/AFA)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Baillie Bollerslev 1989 "The message in daily exchange rates: a conditional-variance tale" Journal of Business & Economic Statistics»; WebFetch: sí, sobre la página índice https://authors.repec.org/pro/pba423/, que reproduce la cita)
- **Contenido:** Sostiene que un sistema de tipos de cambio presenta cointegración fraccional: el error de equilibrio entre divisas revierte muy lentamente (memoria larga).
- **Uso en el Motor:** MC-03: contrastes de cointegración fraccional entre pares de divisas (cestas, cruces) cuando la cointegración estándar se rechaza.
- **Limitaciones:** Resultado discutido en réplicas posteriores. Confirmada solo mediante página índice; pendiente de lectura de la fuente primaria.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0081 · Q 81 (A) — Real Exchange Rate Dynamics in Transition Economies: A Nonlinear Analysis

- **Autores:** Mark P. Taylor; Lucio Sarno
- **Año:** 2001
- **Publicación o institución:** Studies in Nonlinear Dynamics & Econometrics, vol. 5, n.º 3, págs. 1-26
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-01 Series temporales de tipos de cambio: raíces unitarias, cointegración, no linealidad y cambios de régimen (principal) · secundarias: TMX-04
- **Calidad Q:** 81 (A) — Tipo 22/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 5/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.2202/1558-3708.1077 · https://ideas.repec.org/a/bpj/sndecm/v5y2001i3n1.html
- **Acceso y licencia:** Revista por suscripción (De Gruyter)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Michael Nobay Peel 1997 "Transactions costs and nonlinear adjustment in real exchange rates" Journal of Political Economy»; WebFetch: sí, ficha IDEAS con DOI)
- **Contenido:** Modelo no lineal de tipos de cambio reales de nueve economías en transición con diferenciales de tipos reales y productividad, y descomposición de Beveridge-Nelson no lineal multivariante en componentes permanente y transitorio.
- **Uso en el Motor:** MC-02 y MC-09: separación de componente de equilibrio y transitorio en divisas de Europa central y del este (AS-EMEA).
- **Limitaciones:** Muestra de los noventa.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0056 · Q 80 (A) — Real Exchange Rate Forecasting and PPP: This Time the Random Walk Loses

- **Autores:** Michele Ca' Zorzi; Jakub Muck; Michał Rubaszek
- **Año:** 2016
- **Publicación o institución:** Open Economies Review, vol. 27, n.º 3 (versión previa: Federal Reserve Bank of Dallas WP 229)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-01 Series temporales de tipos de cambio: raíces unitarias, cointegración, no linealidad y cambios de régimen (principal) · secundarias: TMX-08
- **Calidad Q:** 80 (A) — Tipo 22/25 · Rigor 16/20 · Autoridad 13/15 · Vigencia 9/10 · Impacto 6/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** Confirmada en la bibliografía de https://authors.repec.org/pro/pca585/
- **Acceso y licencia:** Revista por suscripción (Springer); versiones de trabajo en abierto
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «ECB working paper "Methodological advances in the assessment of equilibrium exchange rates" Bussière Ca' Zorzi Chudik Dieppe»; WebFetch: sí, sobre la página índice https://authors.repec.org/pro/pca585/, que reproduce la cita)
- **Contenido:** Un AR calibrado con una vida media de PPA de consenso (sin estimar) bate al paseo aleatorio en la previsión de tipos de cambio reales a medio plazo.
- **Uso en el Motor:** MC-02: modelo de reversión calibrada (half-life PPP) como referencia sencilla de previsión del tipo de cambio real.
- **Limitaciones:** Ventaja en tipos reales, no necesariamente en nominales. Confirmada solo mediante página índice; pendiente de lectura de la fuente primaria.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0053 · Q 79 (B) — Threshold Adjustment of Deviations from the Law of One Price

- **Autores:** Luciana Juvenal; Mark P. Taylor
- **Año:** 2008
- **Publicación o institución:** Studies in Nonlinear Dynamics & Econometrics, vol. 12, n.º 3
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-01 Series temporales de tipos de cambio: raíces unitarias, cointegración, no linealidad y cambios de régimen (principal) · secundarias: —
- **Calidad Q:** 79 (B) — Tipo 22/25 · Rigor 16/20 · Autoridad 13/15 · Vigencia 8/10 · Impacto 6/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** Confirmada en la bibliografía de https://ideas.repec.org/p/ecb/ecbwps/20101151.html
- **Acceso y licencia:** Revista por suscripción (De Gruyter)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «ECB working paper "Methodological advances in the assessment of equilibrium exchange rates" Bussière Ca' Zorzi Chudik Dieppe»; WebFetch: sí, sobre la página índice https://ideas.repec.org/p/ecb/ecbwps/20101151.html, que reproduce la cita)
- **Contenido:** Modelos autorregresivos de umbral (TAR) para las desviaciones de la ley del precio único con datos desagregados: bandas de inacción por costes de transacción y reversión fuera de ellas.
- **Uso en el Motor:** MC-02: estimación TAR/SETAR de bandas de no reversión en tipos de cambio reales.
- **Limitaciones:** Datos desagregados europeos. Confirmada solo mediante página índice; pendiente de lectura de la fuente primaria.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0059 · Q 77 (B) — Nonlinear Adjustment, Purchasing Power Parity and the Role of Nominal Exchange Rates and Prices

- **Autores:** Joscha Beckmann
- **Año:** 2013
- **Publicación o institución:** The North American Journal of Economics and Finance, vol. 24, págs. 176-190 (versión de trabajo: Ruhr Economic Papers n.º 272, 2011)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-01 Series temporales de tipos de cambio: raíces unitarias, cointegración, no linealidad y cambios de régimen (principal) · secundarias: —
- **Calidad Q:** 77 (B) — Tipo 22/25 · Rigor 16/20 · Autoridad 11/15 · Vigencia 8/10 · Impacto 4/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** https://ideas.repec.org/p/zbw/rwirep/272.html
- **Acceso y licencia:** Versión de trabajo en abierto (RWI/EconStor); revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Mark P. Taylor IDEAS RePEc author page exchange rates purchasing power parity nonlinear»; WebFetch: sí, ficha IDEAS)
- **Contenido:** VAR cointegrado y modelos de corrección del error ESTR con datos mensuales 1973-2009 de cinco economías: el tipo de cambio nominal, no los precios, realiza la mayor parte del ajuste no lineal hacia la PPA, con vidas medias muy inferiores a 3-5 años.
- **Uso en el Motor:** MC-02 y MC-03: ECM no lineal para decidir si la corrección de la PPA vendrá por el tipo de cambio (señal cambiaria) o por los precios.
- **Limitaciones:** Cinco economías avanzadas.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0057 · Q 75 (B) — Spatial Considerations on the PPP Debate

- **Autores:** Michele Ca' Zorzi; Alexander Chudik
- **Año:** 2013
- **Publicación o institución:** European Central Bank, Working Paper Series n.º 1534 (también Federal Reserve Bank of Dallas WP 138)
- **Tipo de documento:** Documento de trabajo de institución reconocida
- **Temática:** TMX-01 Series temporales de tipos de cambio: raíces unitarias, cointegración, no linealidad y cambios de régimen (principal) · secundarias: —
- **Calidad Q:** 75 (B) — Tipo 20/25 · Rigor 16/20 · Autoridad 13/15 · Vigencia 8/10 · Impacto 4/10 · Independencia 9/10 · Acceso 5/10
- **DOI / ISBN / URL:** Confirmada en la bibliografía de https://authors.repec.org/pro/pca585/
- **Acceso y licencia:** Acceso abierto (BCE)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «ECB working paper "Methodological advances in the assessment of equilibrium exchange rates" Bussière Ca' Zorzi Chudik Dieppe»; WebFetch: sí, sobre la página índice https://authors.repec.org/pro/pca585/, que reproduce la cita)
- **Contenido:** Analiza la reversión a la PPA considerando la dependencia espacial (distancia geográfica, vecindad comercial) entre tipos de cambio reales.
- **Uso en el Motor:** MC-02: contrastes de panel de PPA con dependencia transversal en cestas regionales.
- **Limitaciones:** Documento de trabajo. Confirmada solo mediante página índice; pendiente de lectura de la fuente primaria.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0058 · Q 75 (B) — Is Reversion to PPP in Euro Exchange Rates Non-Linear?

- **Autores:** Bernd Schnatz
- **Año:** 2007
- **Publicación o institución:** International Economics and Economic Policy, vol. 4, n.º 3, págs. 281-297
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-01 Series temporales de tipos de cambio: raíces unitarias, cointegración, no linealidad y cambios de régimen (principal) · secundarias: —
- **Calidad Q:** 75 (B) — Tipo 20/25 · Rigor 14/20 · Autoridad 13/15 · Vigencia 8/10 · Impacto 4/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1007/s10368-007-0091-7 · https://ideas.repec.org/a/kap/iecepo/v4y2007i3p281-297.html
- **Acceso y licencia:** Revista por suscripción (Springer)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Mark P. Taylor IDEAS RePEc author page exchange rates purchasing power parity nonlinear»; WebFetch: sí, ficha IDEAS con DOI)
- **Contenido:** Contrasta con modelos STAR si la reversión de los tipos de cambio del euro hacia la PPA es no lineal.
- **Uso en el Motor:** MC-02: aplicación de ESTAR a tipos de cambio reales del EUR (AS-G10N).
- **Limitaciones:** Resumen no disponible en el índice; resultados no leídos.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0060 · Q 74 (B) — Searching for Nonlinearities in Real Exchange Rates

- **Autores:** Yamin Ahmad; Stuart Glosser
- **Año:** 2011
- **Publicación o institución:** Applied Economics, vol. 43, n.º 15, págs. 1829-1845 (versión de trabajo: UW-Whitewater WP 09-01)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-01 Series temporales de tipos de cambio: raíces unitarias, cointegración, no linealidad y cambios de régimen (principal) · secundarias: —
- **Calidad Q:** 74 (B) — Tipo 20/25 · Rigor 16/20 · Autoridad 10/15 · Vigencia 8/10 · Impacto 4/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** https://ideas.repec.org/p/uww/wpaper/09-01.html
- **Acceso y licencia:** Versión de trabajo en abierto; revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Mark P. Taylor IDEAS RePEc author page exchange rates purchasing power parity nonlinear»; WebFetch: sí, ficha IDEAS)
- **Contenido:** Muestra que los contrastes de linealidad de Teräsvirta tienen fuertes distorsiones de tamaño por observaciones influyentes y que pocas series señaladas como ESTAR lo son al estimarlas; algunos tipos reales encajan mejor como TAR.
- **Uso en el Motor:** MC-08: control de falsos positivos de no linealidad antes de usar ESTAR en el Motor.
- **Limitaciones:** Cinco tipos de cambio del G7.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

## TMX-02 Volatilidad cambiaria: GARCH, volatilidad realizada y alta frecuencia

#### DOC-MOT-0217 · Q 97 (A) — Power and Bipower Variation with Stochastic Volatility and Jumps

- **Autores:** Ole E. Barndorff-Nielsen; Neil Shephard
- **Año:** 2004
- **Publicación o institución:** Journal of Financial Econometrics, 2(1), 1-37
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-02 Volatilidad cambiaria: GARCH, volatilidad realizada y alta frecuencia (principal) · secundarias: TMX-07
- **Calidad Q:** 97 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** https://www.nuffield.ox.ac.uk/economics/papers/2003/w18/eric_may03.pdf (versión de trabajo, mayo de 2003) · cita publicada en https://en.wikipedia.org/wiki/Realized_variance
- **Acceso y licencia:** Versión de trabajo en Nuffield College (Oxford), acceso libre
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Realized variance wikipedia Andersen Bollerslev Barndorff-Nielsen Shephard bipower variation realized kernel»; WebFetch: sí)
- **Contenido:** Variación bipotencia realizada: estimador de la varianza integrada robusto a saltos; la diferencia con la varianza realizada estima la contribución de los saltos.
- **Uso en el Motor:** MC-02: variación bipotencia para separar saltos (anuncios macro, intervenciones) de la volatilidad continua en datos intradía de divisas.
- **Limitaciones:** El índice imprime un DOI con prefijo dudoso; se omite. La URL es la versión de trabajo previa a la publicación.
- **Origen:** Reutilizada en F8 Forex V1.0 (2026-11-02) desde F8 V3.2.

#### DOC-MOT-0037 · Q 95 (A) — Modeling and Forecasting Realized Volatility

- **Autores:** Torben G. Andersen; Tim Bollerslev; Francis X. Diebold; Paul Labys
- **Año:** 2003
- **Publicación o institución:** Econometrica, 71(2), 579-625
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-02 Volatilidad cambiaria: GARCH, volatilidad realizada y alta frecuencia (principal) · secundarias: TMX-08
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1111/1468-0262.00418 · Verificada en página índice: https://en.wikipedia.org/wiki/Realized_variance
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Realized variance wikipedia Andersen Bollerslev Barndorff-Nielsen Shephard bipower variation realized kernel»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Realized_variance)
- **Contenido:** Marco de volatilidad realizada con datos intradía: la varianza realizada como medida observable de la varianza integrada y su modelización con VAR fraccionalmente integrado para prever volatilidades y correlaciones.
- **Uso en el Motor:** MC-02: volatilidad realizada de DM/USD y JPY/USD y su previsión con VAR fraccionario; referencia directa para TR-PFV (volatilidad realizada frente a implícita) y el carry ajustado por volatilidad.
- **Limitaciones:** Ruido de microestructura con muestreo muy fino. Confirmada solo mediante página índice (bibliografía de Wikipedia «Realized variance»); pendiente de lectura de la fuente primaria.
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02 (DOI confirmado en índice). Reutilizada en F8 Forex V1.0 (2026-11-02) desde F8 V3.2.

#### DOC-MOT-0033 · Q 95 (A) — Generalized Autoregressive Conditional Heteroskedasticity

- **Autores:** Tim Bollerslev
- **Año:** 1986
- **Publicación o institución:** Journal of Econometrics, 31(3), 307-327
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-02 Volatilidad cambiaria: GARCH, volatilidad realizada y alta frecuencia (principal) · secundarias: —
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1016/0304-4076(86)90063-1 · Verificada en página índice: https://en.wikipedia.org/wiki/Autoregressive_conditional_heteroskedasticity
- **Acceso y licencia:** Revista Elsevier por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Autoregressive conditional heteroskedasticity wikipedia GARCH EGARCH GJR references»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Autoregressive_conditional_heteroskedasticity)
- **Contenido:** Generaliza ARCH a GARCH(p,q): la varianza condicional depende de los cuadrados de los errores pasados y de sus propias varianzas pasadas; GARCH(1,1) es el estándar práctico.
- **Uso en el Motor:** MC-02: GARCH(1,1) de referencia para la volatilidad condicional de los pares de divisas (PERF-FX-G10 y PERF-FX-EM); base del carry ajustado por volatilidad.
- **Limitaciones:** Respuesta simétrica a choques (usar GJR/EGARCH ante apalancamiento). Confirmada solo mediante página índice (bibliografía de Wikipedia «Autoregressive conditional heteroskedasticity»); pendiente de lectura de la fuente primaria.
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02 (DOI confirmado en índice). Reutilizada en F8 Forex V1.0 (2026-11-02) desde F8 V3.2.

#### DOC-MOT-0032 · Q 95 (A) — Autoregressive Conditional Heteroscedasticity with Estimates of the Variance of United Kingdom Inflation

- **Autores:** Robert F. Engle
- **Año:** 1982
- **Publicación o institución:** Econometrica, 50(4), 987-1007
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-02 Volatilidad cambiaria: GARCH, volatilidad realizada y alta frecuencia (principal) · secundarias: —
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.2307/1912773 · Verificada en página índice: https://en.wikipedia.org/wiki/Autoregressive_conditional_heteroskedasticity
- **Acceso y licencia:** Revista por suscripción (JSTOR 1912773)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Autoregressive conditional heteroskedasticity wikipedia GARCH EGARCH GJR references»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Autoregressive_conditional_heteroskedasticity)
- **Contenido:** Introduce el modelo ARCH (varianza condicional función de errores cuadráticos pasados), su estimación por máxima verosimilitud y el contraste LM de efectos ARCH.
- **Uso en el Motor:** MC-02: modelo ARCH original; contraste de efectos ARCH en rendimientos cambiarios antes de estimar GARCH.
- **Limitaciones:** Superado en la práctica por GARCH. Confirmada solo mediante página índice (bibliografía de Wikipedia «Autoregressive conditional heteroskedasticity»); pendiente de lectura de la fuente primaria.
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02 (DOI confirmado en índice). Reutilizada en F8 Forex V1.0 (2026-11-02) desde F8 V3.2.

#### DOC-MOT-0036 · Q 94 (A) — A Simple Approximate Long-Memory Model of Realized Volatility

- **Autores:** Fulvio Corsi
- **Año:** 2009
- **Publicación o institución:** Journal of Financial Econometrics, 7(2), 174-196
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-02 Volatilidad cambiaria: GARCH, volatilidad realizada y alta frecuencia (principal) · secundarias: —
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** Verificada en página índice: https://en.wikipedia.org/wiki/Realized_variance
- **Acceso y licencia:** Revista OUP por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Realized variance wikipedia Andersen Bollerslev Barndorff-Nielsen Shephard bipower variation realized kernel»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Realized_variance)
- **Contenido:** Modelo HAR-RV: la volatilidad realizada se proyecta sobre sus medias diaria, semanal y mensual, reproduciendo memoria larga aproximada con MCO.
- **Uso en el Motor:** MC-02: modelo HAR-RV para prever la volatilidad realizada de pares de divisas en horizontes diario, semanal y mensual (TR-PFV).
- **Limitaciones:** Requiere datos intradía. Confirmada solo mediante página índice (bibliografía de Wikipedia «Realized variance»); pendiente de lectura de la fuente primaria. El índice imprime el DOI con prefijo dudoso (jfinec/jjfinec); se omite hasta confirmarlo.
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02. Reutilizada en F8 Forex V1.0 (2026-11-02) desde F8 V3.2.

#### DOC-MOT-0214 · Q 94 (A) — Dynamic Conditional Correlation: A Simple Class of Multivariate Generalized Autoregressive Conditional Heteroskedasticity Models

- **Autores:** Robert F. Engle
- **Año:** 2002
- **Publicación o institución:** Journal of Business & Economic Statistics, 20(3), 339-350
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-02 Volatilidad cambiaria: GARCH, volatilidad realizada y alta frecuencia (principal) · secundarias: TMX-06
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** https://ideas.repec.org/a/bes/jnlbes/v20y2002i3p339-50.html · versión de trabajo NYU: https://archive.nyu.edu/handle/2451/26879
- **Acceso y licencia:** Ficha RePEc abierta; texto de revista por suscripción; versión de trabajo en el repositorio de NYU
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Engle 2002 Dynamic Conditional Correlation Journal of Business Economic Statistics multivariate GARCH»; WebFetch: sí)
- **Contenido:** Modelo DCC: GARCH univariantes para cada activo y una dinámica GARCH escalar para la matriz de correlaciones de los residuos estandarizados, estimable en dos etapas.
- **Uso en el Motor:** MC-02 y MC-07: correlaciones condicionales dinámicas (DCC) entre pares y con el dólar amplio para carteras de factores cambiarios (PERF-FX-FACT).
- **Limitaciones:** Dinámica común a todas las correlaciones; sesgo en dimensiones grandes.
- **Origen:** Reutilizada en F8 Forex V1.0 (2026-11-02) desde F8 V3.2.

#### FXM-0012 · Q 94 (A) — The Distribution of Realized Exchange Rate Volatility

- **Autores:** Torben G. Andersen; Tim Bollerslev; Francis X. Diebold; Paul Labys
- **Año:** 2001
- **Publicación o institución:** Journal of the American Statistical Association, vol. 96, n.º 453, págs. 42-55
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-02 Volatilidad cambiaria: GARCH, volatilidad realizada y alta frecuencia (principal) · secundarias: —
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1198/016214501750332965 · https://fds.duke.edu/db/aas/Economics/faculty/boller/publications/238039
- **Acceso y licencia:** Versión de trabajo en abierto (Universidad de Pensilvania, NBER WP 7488 con otro título); versión publicada por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Andersen Bollerslev Diebold Labys 2001 distribution of realized exchange rate volatility JASA»; WebFetch: sí, ficha de Duke con DOI)
- **Contenido:** Con rendimientos intradía DM/USD y JPY/USD muestra que las varianzas realizadas son aproximadamente lognormales, los rendimientos estandarizados por volatilidad realizada casi gaussianos y la volatilidad de larga memoria.
- **Uso en el Motor:** MC-02: distribución de la volatilidad realizada de pares del G10; estandarización de rendimientos y modelización log-RV para TR-PFV.
- **Limitaciones:** Dos pares y periodo de los noventa.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### DOC-MOT-0215 · Q 94 (A) — Answering the Skeptics: Yes, Standard Volatility Models Do Provide Accurate Forecasts

- **Autores:** Torben G. Andersen; Tim Bollerslev
- **Año:** 1998
- **Publicación o institución:** International Economic Review, 39(4), 885-905
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-02 Volatilidad cambiaria: GARCH, volatilidad realizada y alta frecuencia (principal) · secundarias: TMX-08
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.2307/2527343 · Verificada en página índice: https://en.wikipedia.org/wiki/Realized_variance
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Realized variance wikipedia Andersen Bollerslev Barndorff-Nielsen Shephard bipower variation realized kernel»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Realized_variance)
- **Contenido:** Demuestra que el bajo R² de las previsiones GARCH frente a rendimientos al cuadrado se debe al ruido del proxy; usando varianza realizada intradía las previsiones son precisas.
- **Uso en el Motor:** MC-02 y MC-10: demuestra con DM/USD y JPY/USD que GARCH prevé bien la volatilidad cuando se evalúa frente a volatilidad realizada intradía; criterio de evaluación de previsiones de volatilidad cambiaria.
- **Limitaciones:** Confirmada solo mediante página índice (bibliografía de Wikipedia «Realized variance»); pendiente de lectura de la fuente primaria.
- **Origen:** Reutilizada en F8 Forex V1.0 (2026-11-02) desde F8 V3.2.

#### DOC-MOT-0220 · Q 93 (A) — Does Anything Beat 5-Minute RV? A Comparison of Realized Measures Across Multiple Asset Classes

- **Autores:** Lily Y. Liu; Andrew J. Patton; Kevin Sheppard
- **Año:** 2015
- **Publicación o institución:** Journal of Econometrics, 187(1), 293-311
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-02 Volatilidad cambiaria: GARCH, volatilidad realizada y alta frecuencia (principal) · secundarias: —
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1016/j.jeconom.2015.02.008 · Verificada en página índice: https://en.wikipedia.org/wiki/Realized_variance
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Realized variance wikipedia Andersen Bollerslev Barndorff-Nielsen Shephard bipower variation realized kernel»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Realized_variance)
- **Contenido:** Compara más de 400 medidas realizadas en 31 activos de varias clases con el Model Confidence Set: la RV a 5 minutos es difícil de batir de forma significativa.
- **Uso en el Motor:** MC-02: elección de la frecuencia de muestreo y de la medida realizada (RV a 5 minutos) para tipos de cambio y otras clases de activo.
- **Limitaciones:** Confirmada solo mediante página índice (bibliografía de Wikipedia «Realized variance»); pendiente de lectura de la fuente primaria.
- **Origen:** Reutilizada en F8 Forex V1.0 (2026-11-02) desde F8 V3.2.

#### FXM-0079 · Q 93 (A) — Spot and Forward Volatility in Foreign Exchange

- **Autores:** Pasquale Della Corte; Lucio Sarno; Ilias Tsiakas
- **Año:** 2011
- **Publicación o institución:** Journal of Financial Economics, vol. 100, n.º 3, págs. 496-513
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-02 Volatilidad cambiaria: GARCH, volatilidad realizada y alta frecuencia (principal) · secundarias: TMX-05
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI: 10.1016/j.jfineco.2011.01.007 · https://openaccess.city.ac.uk/id/eprint/3303/
- **Acceso y licencia:** Versión aceptada en abierto (City Research Online); revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Della Corte Sarno Tsiakas "Spot and forward volatility in foreign exchange" Journal of Financial Economics»; WebFetch: sí, repositorio de City con DOI)
- **Contenido:** Con volatilidades implícitas OTC de divisas deriva la volatilidad implícita forward (acuerdos de volatilidad forward) y muestra que sobrestima sistemáticamente los movimientos futuros de la volatilidad spot: primas por plazo de volatilidad predecibles y explotables.
- **Uso en el Motor:** MC-02 y MC-09: estructura de plazos de la volatilidad implícita de divisas y señal de prima por plazo para estrategias de volatilidad (AS-ESTR, TR-PFV).
- **Limitaciones:** Muestra hasta 2009; costes de transacción de las FVA.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### DOC-MOT-0222 · Q 93 (A) — Roughing It Up: Including Jump Components in the Measurement, Modeling, and Forecasting of Return Volatility

- **Autores:** Torben G. Andersen; Tim Bollerslev; Francis X. Diebold
- **Año:** 2007
- **Publicación o institución:** The Review of Economics and Statistics, 89(4), 701-720
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-02 Volatilidad cambiaria: GARCH, volatilidad realizada y alta frecuencia (principal) · secundarias: TMX-07
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1162/rest.89.4.701 · Verificada en página índice: https://en.wikipedia.org/wiki/Realized_variance
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Realized variance wikipedia Andersen Bollerslev Barndorff-Nielsen Shephard bipower variation realized kernel»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Realized_variance)
- **Contenido:** Separa la componente de saltos con variación bipotencia y muestra que el modelo HAR-RV-CJ (continuo y saltos separados) mejora las previsiones; los saltos son poco persistentes.
- **Uso en el Motor:** MC-02: HAR-RV-CJ con componente de saltos, aplicado también a DM/USD; previsión de volatilidad cambiaria con saltos poco persistentes.
- **Limitaciones:** Confirmada solo mediante página índice (bibliografía de Wikipedia «Realized variance»); pendiente de lectura de la fuente primaria.
- **Origen:** Reutilizada en F8 Forex V1.0 (2026-11-02) desde F8 V3.2.

#### FXM-0063 · Q 93 (A) — Deutsche Mark-Dollar Volatility: Intraday Activity Patterns, Macroeconomic Announcements, and Longer Run Dependencies

- **Autores:** Torben G. Andersen; Tim Bollerslev
- **Año:** 1998
- **Publicación o institución:** The Journal of Finance, vol. 53, n.º 1, págs. 219-265
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-02 Volatilidad cambiaria: GARCH, volatilidad realizada y alta frecuencia (principal) · secundarias: —
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.1111/0022-1082.85732 · https://fds.duke.edu/db/aas/Economics/faculty/boller/publications/237975
- **Acceso y licencia:** Revista por suscripción (Wiley); versión de trabajo NBER WP 5783
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Andersen Bollerslev 1998 "Deutsche mark-dollar volatility: intraday activity patterns, macroeconomic announcements, and longer run dependencies"»; WebFetch: sí, ficha de Duke con DOI)
- **Contenido:** Con un año de rendimientos DM/USD a cinco minutos separa la volatilidad en patrón intradía, efectos de anuncios macroeconómicos y persistencia ARCH diaria, que juntos explican gran parte de la variabilidad.
- **Uso en el Motor:** MC-02: desestacionalización intradía y ventanas de anuncios para medir la volatilidad realizada de pares del G10 (TR-PFV, TR-BCM).
- **Limitaciones:** Un par y un año de datos.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### DOC-MOT-0225 · Q 93 (A) — Autoregressive Conditional Heteroskedasticity and Changes in Regime

- **Autores:** James D. Hamilton; Raul Susmel
- **Año:** 1994
- **Publicación o institución:** Journal of Econometrics, 64, 307-333
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-02 Volatilidad cambiaria: GARCH, volatilidad realizada y alta frecuencia (principal) · secundarias: TMX-01
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** Verificada en página índice: https://econweb.ucsd.edu/~jhamilto/palgrav1.pdf
- **Acceso y licencia:** Revista Elsevier por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Markov switching model wikipedia Hamilton 1989 regime switching references»; WebFetch: sí, sobre la página índice https://econweb.ucsd.edu/~jhamilto/palgrav1.pdf)
- **Contenido:** Modelo SWARCH: parámetros ARCH sujetos a cambios de régimen markovianos; reduce la persistencia espuria de la volatilidad que GARCH atribuye a la memoria.
- **Uso en el Motor:** MC-02: ARCH con cambio de régimen (SWARCH) para episodios de volatilidad cambiaria (crisis, fin de tipos fijos) sin persistencia espuria (AS-EMLA, AS-EMEA).
- **Limitaciones:** Confirmada solo mediante página índice (bibliografía de J. D. Hamilton, «Regime-Switching Models»); pendiente de lectura de la fuente primaria.
- **Origen:** Reutilizada en F8 Forex V1.0 (2026-11-02) desde F8 V3.2.

#### DOC-MOT-0226 · Q 91 (A) — A New Approach to Markov-Switching GARCH Models

- **Autores:** Markus Haas; Stefan Mittnik; Marc S. Paolella
- **Año:** 2004
- **Publicación o institución:** Journal of Financial Econometrics, 2, 493-530
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-02 Volatilidad cambiaria: GARCH, volatilidad realizada y alta frecuencia (principal) · secundarias: TMX-01
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** Verificada en página índice: https://econweb.ucsd.edu/~jhamilto/palgrav1.pdf
- **Acceso y licencia:** Revista OUP por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Markov switching model wikipedia Hamilton 1989 regime switching references»; WebFetch: sí, sobre la página índice https://econweb.ucsd.edu/~jhamilto/palgrav1.pdf)
- **Contenido:** MS-GARCH con procesos de varianza paralelos por régimen que evita la dependencia de la trayectoria y permite estimación por máxima verosimilitud.
- **Uso en el Motor:** MC-02: GARCH con cambio de régimen markoviano para pares emergentes con regímenes de volatilidad diferenciados.
- **Limitaciones:** Confirmada solo mediante página índice (bibliografía de J. D. Hamilton, «Regime-Switching Models»); pendiente de lectura de la fuente primaria.
- **Origen:** Reutilizada en F8 Forex V1.0 (2026-11-02) desde F8 V3.2.

#### FXM-0065 · Q 90 (A) — Fractionally Integrated Generalized Autoregressive Conditional Heteroskedasticity

- **Autores:** Richard T. Baillie; Tim Bollerslev; H. O. Mikkelsen
- **Año:** 1996
- **Publicación o institución:** Journal of Econometrics, vol. 74, n.º 1, págs. 3-30
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-02 Volatilidad cambiaria: GARCH, volatilidad realizada y alta frecuencia (principal) · secundarias: —
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 10/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** Confirmada en la bibliografía de https://authors.repec.org/pro/pba423/
- **Acceso y licencia:** Revista por suscripción (Elsevier)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Baillie Bollerslev 1989 "The message in daily exchange rates: a conditional-variance tale" Journal of Business & Economic Statistics»; WebFetch: sí, sobre la página índice https://authors.repec.org/pro/pba423/, que reproduce la cita)
- **Contenido:** Modelo FIGARCH de memoria larga en la volatilidad condicional, ilustrado con el tipo de cambio DM/USD.
- **Uso en el Motor:** MC-02: volatilidad cambiaria con decaimiento hiperbólico para horizontes largos de carry ajustado por volatilidad.
- **Limitaciones:** Estimación sensible al truncamiento. Confirmada solo mediante página índice; pendiente de lectura de la fuente primaria.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0064 · Q 90 (A) — Meteor Showers or Heat Waves? Heteroskedastic Intra-Daily Volatility in the Foreign Exchange Market

- **Autores:** Robert F. Engle; Takatoshi Ito; Wen-Ling Lin
- **Año:** 1990
- **Publicación o institución:** Econometrica, vol. 58, n.º 3, págs. 525-542
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-02 Volatilidad cambiaria: GARCH, volatilidad realizada y alta frecuencia (principal) · secundarias: —
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** https://ideas.repec.org/a/ecm/emetrp/v58y1990i3p525-42.html
- **Acceso y licencia:** Revista por suscripción (Econometric Society/JSTOR); versión NBER WP 2609
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Engle Ito Lin 1990 "Meteor showers or heat waves? Heteroskedastic intra-daily volatility in the foreign exchange market" Econometrica»; WebFetch: sí, ficha IDEAS)
- **Contenido:** Contrasta si la volatilidad cambiaria se transmite entre las sesiones de Tokio, Europa y Nueva York (lluvia de meteoros) o solo depende de la propia sesión (ola de calor); la evidencia rechaza la ola de calor.
- **Uso en el Motor:** MC-02: modelos de transmisión de volatilidad entre husos horarios para pares asiáticos y G10 (AS-EMAS, TR-PFV).
- **Limitaciones:** Datos de los ochenta (JPY/USD).
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0087 · Q 90 (A) — Modelling the Coherence in Short-Run Nominal Exchange Rates: A Multivariate Generalized ARCH Model

- **Autores:** Tim Bollerslev
- **Año:** 1990
- **Publicación o institución:** The Review of Economics and Statistics, vol. 72, n.º 3, págs. 498-505
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-02 Volatilidad cambiaria: GARCH, volatilidad realizada y alta frecuencia (principal) · secundarias: TMX-06
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 10/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** https://ideas.repec.org/a/tpr/restat/v72y1990i3p498-505.html
- **Acceso y licencia:** Revista por suscripción (MIT Press/JSTOR)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Bollerslev 1990 "Modelling the coherence in short-run nominal exchange rates: a multivariate generalized ARCH model" Review of Economics and Statistics»; WebFetch: sí, ficha IDEAS)
- **Contenido:** Modelo GARCH multivariante de correlación condicional constante (CCC) aplicado a cinco divisas europeas frente al dólar: los comovimientos aumentan con el Sistema Monetario Europeo.
- **Uso en el Motor:** MC-02 y MC-07: matriz de covarianzas condicionales de cestas de divisas (CCC como referencia de DCC) para PERF-FX-FACT.
- **Limitaciones:** Correlaciones constantes por construcción.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0088 · Q 89 (A) — Common Persistence in Conditional Variances

- **Autores:** Robert F. Engle; Tim Bollerslev (orden según la página leída)
- **Año:** 1993
- **Publicación o institución:** Econometrica, vol. 61, n.º 1, págs. 167-186
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-02 Volatilidad cambiaria: GARCH, volatilidad realizada y alta frecuencia (principal) · secundarias: —
- **Calidad Q:** 89 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 8/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** https://www.econometricsociety.org/publications/econometrica/1993/01/01/common-persistence-conditional-variances · https://www.jstor.org/stable/2951782
- **Acceso y licencia:** Revista por suscripción (Econometric Society/JSTOR)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Bollerslev 1990 "Modelling the coherence in short-run nominal exchange rates: a multivariate generalized ARCH model" Review of Economics and Statistics»; WebFetch: sí, página de la Econometric Society)
- **Contenido:** Define la co-persistencia: varias series con volatilidad casi integrada (IGARCH) pueden compartir un componente persistente común; ejemplo con DM/USD y GBP/USD.
- **Uso en el Motor:** MC-02 y MC-07: detectar factores comunes de volatilidad persistente entre pares europeos para coberturas cruzadas y carteras.
- **Limitaciones:** Orden de autores tal como lo dio la página; comprobar en la fuente primaria.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0062 · Q 89 (A) — The Message in Daily Exchange Rates: A Conditional-Variance Tale

- **Autores:** Richard T. Baillie; Tim Bollerslev
- **Año:** 1989 (reedición 2002)
- **Publicación o institución:** Journal of Business & Economic Statistics, vol. 7, n.º 3, págs. 297-305 (1989); reeditado en vol. 20, n.º 1, págs. 60-68 (2002)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-02 Volatilidad cambiaria: GARCH, volatilidad realizada y alta frecuencia (principal) · secundarias: —
- **Calidad Q:** 89 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 9/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** https://ideas.repec.org/a/bes/jnlbes/v20y2002i1p60-68.html
- **Acceso y licencia:** Revista por suscripción (ASA/Taylor & Francis)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Baillie Bollerslev 1989 "The message in daily exchange rates: a conditional-variance tale" Journal of Business & Economic Statistics»; WebFetch: sí, ficha IDEAS de la reedición de 2002 con referencia a la versión de 1989)
- **Contenido:** Con seis divisas frente al dólar muestra raíz unitaria en los niveles, rendimientos casi incorrelacionados, y un GARCH con dummies de día de la semana y errores t que capta colas gruesas y volatilidad variable; los efectos se debilitan con datos semanales o mensuales.
- **Uso en el Motor:** MC-02: especificación GARCH-t con estacionalidad diaria para rendimientos cambiarios diarios (PERF-FX-G10).
- **Limitaciones:** Datos de los ochenta.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0066 · Q 84 (A) — A Multivariate Generalized ARCH Approach to Modeling Risk Premia in Forward Foreign Exchange Rate Markets

- **Autores:** Richard T. Baillie; Tim Bollerslev
- **Año:** 1990
- **Publicación o institución:** Journal of International Money and Finance, vol. 9, n.º 3, págs. 309-324
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-02 Volatilidad cambiaria: GARCH, volatilidad realizada y alta frecuencia (principal) · secundarias: TMX-03
- **Calidad Q:** 84 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 7/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** Confirmada en la bibliografía de https://authors.repec.org/pro/pba423/
- **Acceso y licencia:** Revista por suscripción (Elsevier)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Baillie Bollerslev 1989 "The message in daily exchange rates: a conditional-variance tale" Journal of Business & Economic Statistics»; WebFetch: sí, sobre la página índice https://authors.repec.org/pro/pba423/, que reproduce la cita)
- **Contenido:** GARCH multivariante con media en varianza para modelar primas de riesgo variables en los mercados forward de divisas.
- **Uso en el Motor:** MC-02 y MC-03: prima de riesgo del forward ligada a la covarianza condicional (TR-PFV).
- **Limitaciones:** Evidencia débil de que la volatilidad explique la prima. Confirmada solo mediante página índice; pendiente de lectura de la fuente primaria.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0068 · Q 79 (B) — Bear Squeezes, Volatility Spillovers and Speculative Attacks in the Hyperinflation 1920s Foreign Exchange

- **Autores:** Richard T. Baillie; Tim Bollerslev; M. R. Redfearn
- **Año:** 1993
- **Publicación o institución:** Journal of International Money and Finance, vol. 12, n.º 5, págs. 511-521
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-02 Volatilidad cambiaria: GARCH, volatilidad realizada y alta frecuencia (principal) · secundarias: TMX-07
- **Calidad Q:** 79 (B) — Tipo 25/25 · Rigor 14/20 · Autoridad 15/15 · Vigencia 6/10 · Impacto 5/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** Confirmada en la bibliografía de https://authors.repec.org/pro/pba423/
- **Acceso y licencia:** Revista por suscripción (Elsevier)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Baillie Bollerslev 1989 "The message in daily exchange rates: a conditional-variance tale" Journal of Business & Economic Statistics»; WebFetch: sí, sobre la página índice https://authors.repec.org/pro/pba423/, que reproduce la cita)
- **Contenido:** Transmisión de volatilidad entre divisas y ataques especulativos en los mercados cambiarios de la hiperinflación de los años veinte.
- **Uso en el Motor:** MC-02: modelos de contagio de volatilidad en episodios de alta inflación (AS-EMLA: ARS, AS-EMEA: TRY).
- **Limitaciones:** Episodio histórico. Confirmada solo mediante página índice; pendiente de lectura de la fuente primaria.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0035 · Q 78 (B) — Exchange Rate Volatility and the Mixture of Distribution Hypothesis

- **Autores:** Luc Bauwens; Dagfinn Rime; Genaro Sucarrat
- **Año:** 2006
- **Publicación o institución:** Empirical Economics, vol. 30, n.º 4, págs. 889-911
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-02 Volatilidad cambiaria: GARCH, volatilidad realizada y alta frecuencia (principal) · secundarias: —
- **Calidad Q:** 78 (B) — Tipo 22/25 · Rigor 15/20 · Autoridad 13/15 · Vigencia 7/10 · Impacto 6/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** Confirmada en https://ideas.repec.org/e/pri21.html
- **Acceso y licencia:** Revista por suscripción (Springer)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Lucio Sarno IDEAS RePEc publications exchange rates Akram Rime Sarno…»; WebFetch: sí, sobre la página índice IDEAS de Dagfinn Rime)
- **Contenido:** Relaciona la volatilidad cambiaria con la actividad de negociación y la llegada de información (hipótesis de mezcla de distribuciones) en el mercado de divisas noruego.
- **Uso en el Motor:** MC-02: variables de actividad (número de operaciones, flujo) como regresores de la volatilidad de pares menos líquidos (NOK, SEK) en AS-G10M.
- **Limitaciones:** Mercado pequeño; pendiente de lectura de la fuente primaria.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0067 · Q 76 (B) — Measuring Non-Linearity, Long Memory and Self-Similarity in High-Frequency European Exchange Rates

- **Autores:** Richard T. Baillie; A. A. Cecen; C. Erkal; Y.-W. Han
- **Año:** 2004
- **Publicación o institución:** Journal of International Financial Markets, Institutions and Money, vol. 14, n.º 5, págs. 401-418
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-02 Volatilidad cambiaria: GARCH, volatilidad realizada y alta frecuencia (principal) · secundarias: —
- **Calidad Q:** 76 (B) — Tipo 22/25 · Rigor 15/20 · Autoridad 13/15 · Vigencia 7/10 · Impacto 5/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** Confirmada en la bibliografía de https://authors.repec.org/pro/pba423/
- **Acceso y licencia:** Revista por suscripción (Elsevier)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Baillie Bollerslev 1989 "The message in daily exchange rates: a conditional-variance tale" Journal of Business & Economic Statistics»; WebFetch: sí, sobre la página índice https://authors.repec.org/pro/pba423/, que reproduce la cita)
- **Contenido:** Mide no linealidad, memoria larga y autosemejanza en rendimientos de alta frecuencia de divisas europeas.
- **Uso en el Motor:** MC-02: diagnóstico de memoria larga y escalado en datos intradía de pares europeos.
- **Limitaciones:** Pocos pares europeos de alta frecuencia. Confirmada solo mediante página índice; pendiente de lectura de la fuente primaria.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

## TMX-03 Paridades y cálculo cambiario: CIP, puntos forward, base cruzada y convenciones

#### FXM-0001 · Q 95 (A) — Deviations from Covered Interest Rate Parity

- **Autores:** Wenxin Du; Alexander Tepper; Adrien Verdelhan
- **Año:** 2018
- **Publicación o institución:** The Journal of Finance, vol. 73, n.º 3, págs. 915-957 (versión de trabajo NBER WP 23170)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-03 Paridades y cálculo cambiario: CIP, puntos forward, base cruzada y convenciones (principal) · secundarias: TMX-06
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1111/jofi.12620 · https://dspace.mit.edu/handle/1721.1/128481
- **Acceso y licencia:** Manuscrito original en abierto en el repositorio del MIT (CC BY-NC-SA 4.0); versión publicada por suscripción (Wiley)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «covered interest parity deviations Du Tepper Verdelhan 2018 Journal of Finance»; WebFetch: sí, registro completo de DSpace@MIT con DOI)
- **Contenido:** Documenta desviaciones persistentes de la CIP en las divisas del G10 desde 2008, mide la base con tipos Libor y con tipos sin riesgo (repo, letras), muestra los picos de fin de trimestre y los vincula a costes de balance de los intermediarios y a diferenciales de tipos nominales.
- **Uso en el Motor:** MC-01 y MC-09: definición y cálculo de la base de la CIP (forward implícito frente a forward de mercado) por plazo y por tipo de interés de referencia; insumo de TR-PFV (base cruzada) y del carry cubierto.
- **Limitaciones:** Muestra centrada en el G10 hasta 2016; la medición depende del tipo de interés elegido (Libor ya retirado; sustituir por tipos RFR).
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0034 · Q 92 (A) — Covered Interest Parity Arbitrage

- **Autores:** Dagfinn Rime; Andreas Schrimpf; Olav Syrstad
- **Año:** 2022
- **Publicación o institución:** The Review of Financial Studies, vol. 35, n.º 11, págs. 5185-5227
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-03 Paridades y cálculo cambiario: CIP, puntos forward, base cruzada y convenciones (principal) · secundarias: —
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** Confirmada en https://ideas.repec.org/e/pri21.html
- **Acceso y licencia:** Revista por suscripción (OUP); versiones de trabajo en abierto (BPI, Norges Bank)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Lucio Sarno IDEAS RePEc publications exchange rates Akram Rime Sarno…»; WebFetch: sí, sobre la página índice IDEAS de Dagfinn Rime)
- **Contenido:** Muestra que la CIP se cumple para los tipos marginales de financiación de cada banco, que la rentabilidad del arbitraje depende del coste de financiación del arbitrajista (segmentación del mercado monetario en dólares) y que la base medida con Libor sobrestima las oportunidades reales.
- **Uso en el Motor:** MC-01 y MC-09: elección del tipo de interés relevante (financiación marginal, OIS, papel comercial) al medir la base.
- **Limitaciones:** Pendiente de lectura de la fuente primaria.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0074 · Q 92 (A) — Covered Interest Parity Deviations: Macrofinancial Determinants

- **Autores:** Eugenio M. Cerutti; Maurice Obstfeld; Haonan Zhou
- **Año:** 2021
- **Publicación o institución:** Journal of International Economics, vol. 130 (mayo de 2021), NBER International Seminar on Macroeconomics 2020 (versión de trabajo NBER WP 26129; IMF WP 2019)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-03 Paridades y cálculo cambiario: CIP, puntos forward, base cruzada y convenciones (principal) · secundarias: —
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1016/j.jinteco.2021.103447 · https://www.nber.org/books-and-chapters/nber-international-seminar-macroeconomics-2020/covered-interest-parity-deviations-macrofinancial-determinants
- **Acceso y licencia:** Versiones de trabajo en abierto (NBER, FMI, CEPR); revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Cerutti Obstfeld Zhou "Covered interest parity deviations: macrofinancial determinants" Journal of International Economics»; WebFetch: sí, página del NBER con DOI)
- **Contenido:** Para 2010-2018 relaciona la base cruzada con factores de riesgo (liquidez del mercado cambiario, capacidad de riesgo de los intermediarios, fortaleza del dólar ligada a divisas refugio) y de política (balances de bancos centrales, primas por plazo, regulación de G-SIB a fin de año).
- **Uso en el Motor:** MC-03 y MC-09: modelo de determinantes de la base por divisa y plazo para TR-PFV; efecto fin de año en la base a tres meses.
- **Limitaciones:** Asociaciones, no identificación causal.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0061 · Q 92 (A) — The Dollar, Bank Leverage, and Deviations from Covered Interest Parity

- **Autores:** Stefan Avdjiev; Wenxin Du; Cathérine Koch; Hyun Song Shin
- **Año:** 2019
- **Publicación o institución:** American Economic Review: Insights, vol. 1, n.º 2, págs. 193-208 (versión de trabajo: BIS WP 592)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-03 Paridades y cálculo cambiario: CIP, puntos forward, base cruzada y convenciones (principal) · secundarias: —
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.1257/aeri.20180322 · https://econpapers.repec.org/article/aeaaerins/v_3a1_3ay_3a2019_3ai_3a2_3ap_3a193-208.htm
- **Acceso y licencia:** Revista por suscripción (AEA); versión de trabajo en abierto (BPI)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Avdjiev Du Koch Shin "The dollar, bank leverage and deviations from covered interest parity" American Economic Review: Insights»; WebFetch: sí, ficha EconPapers con DOI)
- **Contenido:** Relación triangular dólar-desviaciones de la CIP-crédito bancario transfronterizo en dólares: un dólar más fuerte amplía la base y contrae el crédito; el dólar como barómetro de la capacidad de asumir riesgo.
- **Uso en el Motor:** MC-03 y MC-09: regresión de la base sobre el dólar amplio; escenarios de TR-PFV y AS-ESTR (dólar amplio).
- **Limitaciones:** Muestra posterior a 2008.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### DOC-MOT-0309 · Q 92 (A) — Interpolation Methods for Curve Construction

- **Autores:** Patrick S. Hagan; Graeme West
- **Año:** 2006
- **Publicación o institución:** Applied Mathematical Finance, vol. 13, n.º 2, págs. 89-129
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-03 Paridades y cálculo cambiario: CIP, puntos forward, base cruzada y convenciones (principal) · secundarias: —
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI: 10.1080/13504860500396032 · Copia: http://www.finmod.co.za/Hagan_West_curves_AMF.pdf
- **Acceso y licencia:** Copia gratuita (finmod.co.za); revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Vasicek model Cox–Ingersoll–Ross model Heath–Jarrow–Morton framework affine term structure model yield curve (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Yield curve»)
- **Contenido:** Compara métodos de interpolación para construir curvas (lineal en rendimientos, log-lineal en factores de descuento, splines, monotone convex) y sus propiedades de forwards.
- **Uso en el Motor:** MC-01: interpolación de curvas de descuento en cada divisa para calcular puntos forward y forwards a fechas rotas (broken dates) coherentes con la CIP.
- **Limitaciones:** Enfocado a curvas de swaps; no aborda multicurva.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02. Reutilizada en F8 Forex V1.0 (2026-11-02) desde F8 V3.2.

#### FXM-0002 · Q 90 (A) — Covered Interest Parity Lost: Understanding the Cross-Currency Basis

- **Autores:** Claudio Borio; Robert N. McCauley; Patrick McGuire; Vladyslav Sushko
- **Año:** 2016
- **Publicación o institución:** BIS Quarterly Review, septiembre de 2016 (Banco de Pagos Internacionales)
- **Tipo de documento:** Artículo de revista institucional (organismo oficial)
- **Temática:** TMX-03 Paridades y cálculo cambiario: CIP, puntos forward, base cruzada y convenciones (principal) · secundarias: —
- **Calidad Q:** 90 (A) — Tipo 22/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 9/10 · Acceso 9/10
- **DOI / ISBN / URL:** https://www.bis.org/publ/qtrpdf/r_qt1609e.htm
- **Acceso y licencia:** Acceso abierto (BPI)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Borio McCauley McGuire Sushko "Covered interest parity lost: understanding the cross-currency basis" BIS Quarterly Review September 2016»; WebFetch: sí)
- **Contenido:** Explica la base cruzada de divisas (cross-currency basis) frente al dólar como resultado de la demanda de cobertura cambiaria y de los límites al arbitraje por el coste del balance bancario; incluye evidencia por divisas y en el tiempo.
- **Uso en el Motor:** MC-01 y MC-09: lectura de la base cruzada (FX swap y cross-currency swap) para TR-PFV y para el coste de cobertura en el carry cubierto de AS-G10N y AS-EMAS.
- **Limitaciones:** Artículo descriptivo; la cuantificación econométrica está en el documento de trabajo del BPI n.º 590.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0007 · Q 90 (A) — Dollar Funding and the Lending Behavior of Global Banks

- **Autores:** Victoria Ivashina; David S. Scharfstein; Jeremy C. Stein
- **Año:** 2015
- **Publicación o institución:** The Quarterly Journal of Economics, vol. 130, n.º 3, págs. 1241-1281
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-03 Paridades y cálculo cambiario: CIP, puntos forward, base cruzada y convenciones (principal) · secundarias: —
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** Confirmada en la bibliografía de https://www.bis.org/publ/qtrpdf/r_qt1609e.htm
- **Acceso y licencia:** Revista por suscripción (OUP)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Borio McCauley McGuire Sushko "Covered interest parity lost…"»; WebFetch: sí, sobre la página índice del BIS Quarterly Review)
- **Contenido:** Modelo y evidencia de cómo los bancos europeos, ante la escasez de financiación en dólares, recurren a FX swaps (ampliando las desviaciones de la CIP) y recortan el crédito en dólares.
- **Uso en el Motor:** MC-03 y MC-09: mecanismo de transmisión financiación en dólares → base cruzada, usado en escenarios de TR-PFV y TR-BCM.
- **Limitaciones:** Enfoque bancario; pendiente de lectura de la fuente primaria.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0032 · Q 90 (A) — Arbitrage in the Foreign Exchange Market: Turning on the Microscope

- **Autores:** Q. Farooq Akram; Dagfinn Rime; Lucio Sarno
- **Año:** 2008
- **Publicación o institución:** Journal of International Economics, vol. 76, n.º 2, págs. 237-253 (versión de trabajo: Norges Bank WP 2005/12)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-03 Paridades y cálculo cambiario: CIP, puntos forward, base cruzada y convenciones (principal) · secundarias: —
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 14/15 · Vigencia 8/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** https://ideas.repec.org/p/bno/worpap/2005_12.html
- **Acceso y licencia:** Versión de trabajo en abierto (Norges Bank); versión publicada por suscripción (Elsevier)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Lucio Sarno IDEAS RePEc publications exchange rates Akram Rime Sarno arbitrage foreign exchange market microscope»; WebFetch: sí, ficha IDEAS con versión publicada)
- **Contenido:** Con datos de cotizaciones ejecutables tick a tick (Reuters) muestra numerosas oportunidades de arbitraje de la CIP (ida y vuelta y de un solo sentido) económicamente significativas pero de corta duración, invisibles a menor frecuencia.
- **Uso en el Motor:** MC-01: cálculo de la CIP con precios comprador/vendedor (bid/ask) y diferenciales de depósito; criterio de banda de no arbitraje para la base.
- **Limitaciones:** Siete meses de datos (2004); antes de la ampliación de la base posterior a 2008.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### DOC-MOT-0311 · Q 89 (A) — Zero-Coupon Yield Curves: Technical Documentation

- **Autores:** Bank for International Settlements (contribuciones de bancos centrales)
- **Año:** 2005
- **Publicación o institución:** BIS Papers n.º 25 (30 de octubre de 2005)
- **Tipo de documento:** Informe técnico con metodología (organismo oficial)
- **Temática:** TMX-03 Paridades y cálculo cambiario: CIP, puntos forward, base cruzada y convenciones (principal) · secundarias: —
- **Calidad Q:** 89 (A) — Tipo 20/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://www.bis.org/publ/bppdf/bispap25j.pdf
- **Acceso y licencia:** Acceso gratuito (BPI)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Banco de España documento de trabajo estimación estructura temporal de los tipos de interés Nelson Siegel Svensson»; WebFetch: sí, documento BIS Papers 25)
- **Contenido:** Recopila los métodos de estimación de curvas cupón cero de los bancos centrales del BPI; la mayoría usa Nelson-Siegel o la extensión de Svensson.
- **Uso en el Motor:** MC-01: métodos oficiales de curvas cupón cero de bancos centrales usados como tipos de descuento domésticos y extranjeros en el cálculo de forwards y de la desviación de la CIP.
- **Limitaciones:** Documento de 2005; prácticas posteriores no recogidas.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02. Reutilizada en F8 Forex V1.0 (2026-11-02) desde F8 V3.2.

#### FXM-0082 · Q 88 (A) — FX Swaps and Forwards: Missing Global Debt?

- **Autores:** Claudio Borio; Robert N. McCauley; Patrick McGuire
- **Año:** 2017
- **Publicación o institución:** BIS Quarterly Review, septiembre de 2017 (Banco de Pagos Internacionales)
- **Tipo de documento:** Artículo de revista institucional (organismo oficial)
- **Temática:** TMX-03 Paridades y cálculo cambiario: CIP, puntos forward, base cruzada y convenciones (principal) · secundarias: —
- **Calidad Q:** 88 (A) — Tipo 22/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 9/10 · Acceso 9/10
- **DOI / ISBN / URL:** https://bis.org/publ/qtrpdf/r_qt1709e.htm
- **Acceso y licencia:** Acceso abierto (BPI)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Borio McCauley McGuire "FX swaps and forwards: missing global debt?" BIS Quarterly Review September 2017»; WebFetch: sí)
- **Contenido:** Trata FX swaps, cross-currency swaps y forwards como endeudamiento colateralizado fuera de balance y estima que las obligaciones en dólares de no bancos por estos instrumentos igualan o superan la deuda en dólares en balance; la mayor parte cubre exposiciones, pero los descalces de plazo generan tensiones de financiación.
- **Uso en el Motor:** MC-01 y MC-09: lectura económica de un FX swap como préstamo garantizado (pata spot + pata forward) y dimensión de la demanda de cobertura que presiona la base (TR-PFV).
- **Limitaciones:** Estimaciones con supuestos sobre la distribución por sectores.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0004 · Q 88 (A) — From Turmoil to Crisis: Dislocations in the FX Swap Market Before and After the Failure of Lehman Brothers

- **Autores:** Naohiko Baba; Frank Packer
- **Año:** 2009
- **Publicación o institución:** Journal of International Money and Finance, vol. 28, n.º 8, págs. 1350-1374
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-03 Paridades y cálculo cambiario: CIP, puntos forward, base cruzada y convenciones (principal) · secundarias: TMX-07
- **Calidad Q:** 88 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 8/10 · Impacto 9/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** Confirmada en la bibliografía de https://www.bis.org/publ/qtrpdf/r_qt1609e.htm
- **Acceso y licencia:** Revista por suscripción (Elsevier)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Borio McCauley McGuire Sushko "Covered interest parity lost…"»; WebFetch: sí, sobre la página índice del BIS Quarterly Review, que reproduce la cita completa)
- **Contenido:** Analiza las desviaciones de la CIP en el mercado de FX swaps durante 2007-2009 y su relación con el riesgo de contraparte de los bancos no estadounidenses y con las líneas swap de la Fed.
- **Uso en el Motor:** MC-01 y MC-09: modelo de la base en tensión (riesgo de contraparte, escasez de dólares) para escenarios de estrés de TR-PFV y MC-05.
- **Limitaciones:** Episodio de crisis concreto; pendiente de lectura de la fuente primaria.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0003 · Q 86 (A) — The Failure of Covered Interest Parity: FX Hedging Demand and Costly Balance Sheets

- **Autores:** Claudio Borio; Mobeen Iqbal; Robert N. McCauley; Patrick McGuire; Vladyslav Sushko
- **Año:** 2016
- **Publicación o institución:** BIS Working Papers n.º 590 (27 de octubre de 2016)
- **Tipo de documento:** Documento de trabajo de institución reconocida
- **Temática:** TMX-03 Paridades y cálculo cambiario: CIP, puntos forward, base cruzada y convenciones (principal) · secundarias: —
- **Calidad Q:** 86 (A) — Tipo 20/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 8/10 · Acceso 9/10
- **DOI / ISBN / URL:** https://www.bis.org/publ/work590.pdf
- **Acceso y licencia:** Acceso abierto (BPI)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Borio McCauley McGuire Sushko "Covered interest parity lost…" BIS Quarterly Review September 2016», que devolvió el PDF; WebFetch: sí)
- **Contenido:** Atribuye las desviaciones de la CIP frente al dólar no explicadas por costes de transacción ni riesgo de crédito a la demanda de cobertura forward; añadir medidas de demanda de cobertura mejora el poder explicativo de las regresiones habituales de la base.
- **Uso en el Motor:** MC-03 y MC-09: especificación de regresiones de la base cruzada con variables de demanda de cobertura y coste de balance (TR-PFV).
- **Limitaciones:** Documento de trabajo; muestra hasta 2016.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0071 · Q 86 (A) — The Forward Premium Anomaly Is Not as Bad as You Think

- **Autores:** Richard T. Baillie; Tim Bollerslev
- **Año:** 2000
- **Publicación o institución:** Journal of International Money and Finance, vol. 19, n.º 4, págs. 471-488
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-03 Paridades y cálculo cambiario: CIP, puntos forward, base cruzada y convenciones (principal) · secundarias: TMX-01
- **Calidad Q:** 86 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 8/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** Confirmada en la bibliografía de https://authors.repec.org/pro/pba423/
- **Acceso y licencia:** Revista por suscripción (Elsevier)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Baillie Bollerslev 1989 "The message in daily exchange rates: a conditional-variance tale" Journal of Business & Economic Statistics»; WebFetch: sí, sobre la página índice https://authors.repec.org/pro/pba423/, que reproduce la cita)
- **Contenido:** Muestra que la persistencia de la prima forward distorsiona la distribución del coeficiente de la regresión de Fama, de modo que la anomalía de la UIP es en parte un artefacto estadístico.
- **Uso en el Motor:** MC-03: inferencia robusta en regresiones de paridad descubierta (forward como predictor).
- **Limitaciones:** Simulaciones dependientes del modelo supuesto. Confirmada solo mediante página índice; pendiente de lectura de la fuente primaria.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0033 · Q 85 (A) — Does the Law of One Price Hold in International Financial Markets? Evidence from Tick Data

- **Autores:** Q. Farooq Akram; Dagfinn Rime; Lucio Sarno
- **Año:** 2009
- **Publicación o institución:** Journal of Banking & Finance, vol. 33, n.º 10, págs. 1741-1754
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-03 Paridades y cálculo cambiario: CIP, puntos forward, base cruzada y convenciones (principal) · secundarias: —
- **Calidad Q:** 85 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 7/10 · Impacto 7/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** Confirmada en la lista de artículos de https://ideas.repec.org/e/pri21.html
- **Acceso y licencia:** Revista por suscripción (Elsevier)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Lucio Sarno IDEAS RePEc publications exchange rates Akram Rime Sarno…»; WebFetch: sí, sobre la página índice IDEAS de Dagfinn Rime)
- **Contenido:** Contrasta la ley del precio único (CIP y paridades triangulares) con datos tick y estima la velocidad de corrección de las desviaciones.
- **Uso en el Motor:** MC-01: control de coherencia de cruces sintéticos (arbitraje triangular) y de la CIP en datos de alta frecuencia.
- **Limitaciones:** Pendiente de lectura de la fuente primaria.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0070 · Q 83 (A) — The Long Memory of the Forward Premium

- **Autores:** Richard T. Baillie; Tim Bollerslev
- **Año:** 1994
- **Publicación o institución:** Journal of International Money and Finance, vol. 13, n.º 5, págs. 565-571
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-03 Paridades y cálculo cambiario: CIP, puntos forward, base cruzada y convenciones (principal) · secundarias: TMX-01
- **Calidad Q:** 83 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 7/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** Confirmada en la bibliografía de https://authors.repec.org/pro/pba423/
- **Acceso y licencia:** Revista por suscripción (Elsevier)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Baillie Bollerslev 1989 "The message in daily exchange rates: a conditional-variance tale" Journal of Business & Economic Statistics»; WebFetch: sí, sobre la página índice https://authors.repec.org/pro/pba423/, que reproduce la cita)
- **Contenido:** La prima forward (diferencia forward-contado) muestra memoria larga (integración fraccional), lo que afecta a los contrastes de regresión de la UIP.
- **Uso en el Motor:** MC-01 y MC-03: tratamiento estadístico de los puntos forward y de la prima forward como serie persistente.
- **Limitaciones:** Muestra de los ochenta. Confirmada solo mediante página índice; pendiente de lectura de la fuente primaria.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0083 · Q 82 (A) — The US Dollar Shortage in Global Banking

- **Autores:** Patrick McGuire; Goetz von Peter
- **Año:** 2009
- **Publicación o institución:** BIS Quarterly Review, marzo de 2009, págs. 47-63
- **Tipo de documento:** Artículo de revista institucional (organismo oficial)
- **Temática:** TMX-03 Paridades y cálculo cambiario: CIP, puntos forward, base cruzada y convenciones (principal) · secundarias: —
- **Calidad Q:** 82 (A) — Tipo 22/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 9/10 · Independencia 9/10 · Acceso 5/10
- **DOI / ISBN / URL:** Confirmada en la bibliografía de https://bis.org/publ/qtrpdf/r_qt1709e.htm
- **Acceso y licencia:** Acceso abierto (BPI)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Borio McCauley McGuire "FX swaps and forwards: missing global debt?" BIS Quarterly Review September 2017»; WebFetch: sí, sobre la página índice https://bis.org/publ/qtrpdf/r_qt1709e.htm, que reproduce la cita)
- **Contenido:** Mide con estadísticas bancarias del BPI la financiación en dólares de bancos no estadounidenses mediante FX swaps y la escasez de dólares que amplió la base en 2008.
- **Uso en el Motor:** MC-09: indicadores de necesidad de financiación en dólares por sistema bancario como explicativos de la base por divisa.
- **Limitaciones:** Episodio de crisis. Confirmada solo mediante página índice; pendiente de lectura de la fuente primaria.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0005 · Q 82 (A) — The Spillover of Money Market Turbulence to FX Swap and Cross-Currency Swap Markets

- **Autores:** Naohiko Baba; Frank Packer; Teppei Nagano
- **Año:** 2008
- **Publicación o institución:** BIS Quarterly Review, marzo de 2008, págs. 73-86
- **Tipo de documento:** Artículo de revista institucional (organismo oficial)
- **Temática:** TMX-03 Paridades y cálculo cambiario: CIP, puntos forward, base cruzada y convenciones (principal) · secundarias: —
- **Calidad Q:** 82 (A) — Tipo 22/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 8/10 · Independencia 9/10 · Acceso 6/10
- **DOI / ISBN / URL:** Confirmada en la bibliografía de https://www.bis.org/publ/qtrpdf/r_qt1609e.htm
- **Acceso y licencia:** Acceso abierto (BPI)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Borio McCauley McGuire Sushko "Covered interest parity lost…"»; WebFetch: sí, sobre la página índice del BIS Quarterly Review)
- **Contenido:** Describe la mecánica de los FX swaps y de los cross-currency swaps y cómo la tensión del mercado monetario en dólares se trasladó a sus primas implícitas en 2007-2008.
- **Uso en el Motor:** MC-01: diferencias de cálculo entre la base de FX swap (corto plazo) y la de cross-currency swap (largo plazo) para TR-PFV.
- **Limitaciones:** Descriptivo; pendiente de lectura de la fuente primaria.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0072 · Q 82 (A) — Do Asymmetric and Nonlinear Adjustments Explain the Forward Premium Anomaly?

- **Autores:** Richard T. Baillie; R. Kilic
- **Año:** 2006
- **Publicación o institución:** Journal of International Money and Finance, vol. 25, n.º 1, págs. 22-47
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-03 Paridades y cálculo cambiario: CIP, puntos forward, base cruzada y convenciones (principal) · secundarias: TMX-01
- **Calidad Q:** 82 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 13/15 · Vigencia 8/10 · Impacto 6/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** Confirmada en la bibliografía de https://authors.repec.org/pro/pba423/
- **Acceso y licencia:** Revista por suscripción (Elsevier)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Baillie Bollerslev 1989 "The message in daily exchange rates: a conditional-variance tale" Journal of Business & Economic Statistics»; WebFetch: sí, sobre la página índice https://authors.repec.org/pro/pba423/, que reproduce la cita)
- **Contenido:** Modelos de transición suave (LSTAR/ESTAR) para la regresión de la UIP: la paridad se cumple mejor cuando el diferencial o la volatilidad superan ciertos umbrales.
- **Uso en el Motor:** MC-03: regresión no lineal de la UIP condicionada al tamaño del diferencial de tipos (carry).
- **Limitaciones:** Ajuste no lineal sensible a la elección de la variable de transición. Confirmada solo mediante página índice; pendiente de lectura de la fuente primaria.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0086 · Q 81 (A) — Non-Deliverable Forwards: Impact of Currency Internationalisation and Derivatives Reform

- **Autores:** Robert N. McCauley; Chang Shu
- **Año:** 2016
- **Publicación o institución:** BIS Quarterly Review, diciembre de 2016, págs. 81-93
- **Tipo de documento:** Artículo de revista institucional (organismo oficial)
- **Temática:** TMX-03 Paridades y cálculo cambiario: CIP, puntos forward, base cruzada y convenciones (principal) · secundarias: —
- **Calidad Q:** 81 (A) — Tipo 22/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 6/10 · Independencia 9/10 · Acceso 5/10
- **DOI / ISBN / URL:** Confirmada en la bibliografía de https://bis.org/publ/qtrpdf/r_qt1709e.htm
- **Acceso y licencia:** Acceso abierto (BPI)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Borio McCauley McGuire "FX swaps and forwards: missing global debt?" BIS Quarterly Review September 2017»; WebFetch: sí, sobre la página índice https://bis.org/publ/qtrpdf/r_qt1709e.htm, que reproduce la cita)
- **Contenido:** Describe el mercado de forwards sin entrega (NDF) de divisas emergentes y cómo la internacionalización de la divisa y la reforma de derivados lo reducen o lo trasladan a forwards con entrega.
- **Uso en el Motor:** MC-01: cálculo con NDF (fijación, liquidación en dólares) y brecha entre forward onshore y NDF offshore en EMAS y EMLA (INR, KRW, TWD, BRL, CLP, COP).
- **Limitaciones:** Nombre de pila de la coautora de conocimiento previo; iniciales en el índice. Confirmada solo mediante página índice; pendiente de lectura de la fuente primaria.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0006 · Q 80 (A) — Capital Constraints, Counterparty Risk, and Deviations from Covered Interest Parity

- **Autores:** Niall Coffey; Warren B. Hrung; Asani Sarkar
- **Año:** 2009
- **Publicación o institución:** Federal Reserve Bank of New York, Staff Reports n.º 393
- **Tipo de documento:** Documento de trabajo de institución reconocida
- **Temática:** TMX-03 Paridades y cálculo cambiario: CIP, puntos forward, base cruzada y convenciones (principal) · secundarias: —
- **Calidad Q:** 80 (A) — Tipo 20/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 7/10 · Impacto 8/10 · Independencia 9/10 · Acceso 6/10
- **DOI / ISBN / URL:** Confirmada en la bibliografía de https://www.bis.org/publ/qtrpdf/r_qt1609e.htm
- **Acceso y licencia:** Acceso abierto (Fed de Nueva York)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Borio McCauley McGuire Sushko "Covered interest parity lost…"»; WebFetch: sí, sobre la página índice del BIS Quarterly Review)
- **Contenido:** Relaciona las desviaciones de la CIP durante la crisis con las restricciones de capital de los arbitrajistas y con el riesgo de contraparte, y evalúa el efecto de las facilidades de la Fed.
- **Uso en el Motor:** MC-03: variables explicativas (CDS bancarios, restricciones de capital) en modelos de la base de la CIP.
- **Limitaciones:** Documento de trabajo; pendiente de lectura de la fuente primaria.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0084 · Q 79 (B) — Do Firms Believe in Interest Rate Parity?

- **Autores:** M. McBrady; S. Mortal; M. Schill
- **Año:** 2010
- **Publicación o institución:** Review of Finance, vol. 14, n.º 4, págs. 695-726
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-03 Paridades y cálculo cambiario: CIP, puntos forward, base cruzada y convenciones (principal) · secundarias: —
- **Calidad Q:** 79 (B) — Tipo 25/25 · Rigor 15/20 · Autoridad 12/15 · Vigencia 7/10 · Impacto 6/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** Confirmada en la bibliografía de https://bis.org/publ/qtrpdf/r_qt1709e.htm
- **Acceso y licencia:** Revista por suscripción (OUP)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Borio McCauley McGuire "FX swaps and forwards: missing global debt?" BIS Quarterly Review September 2017»; WebFetch: sí, sobre la página índice https://bis.org/publ/qtrpdf/r_qt1709e.htm, que reproduce la cita)
- **Contenido:** Analiza la elección de divisa de emisión de deuda de las empresas y si aprovechan diferenciales de tipos cubiertos y descubiertos.
- **Uso en el Motor:** MC-03: emisión en divisa extranjera y swap de vuelta como fuente de demanda de cobertura que afecta a la base a largo plazo.
- **Limitaciones:** Nombres de pila no vistos en el índice. Confirmada solo mediante página índice; pendiente de lectura de la fuente primaria.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0073 · Q 75 (B) — Deviations from Daily Uncovered Interest Rate Parity and the Role of Intervention

- **Autores:** Richard T. Baillie; William P. Osterberg
- **Año:** 2000
- **Publicación o institución:** Journal of International Financial Markets, Institutions and Money, vol. 10, n.º 3-4, págs. 363-379
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-03 Paridades y cálculo cambiario: CIP, puntos forward, base cruzada y convenciones (principal) · secundarias: —
- **Calidad Q:** 75 (B) — Tipo 22/25 · Rigor 14/20 · Autoridad 13/15 · Vigencia 7/10 · Impacto 5/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** Confirmada en la bibliografía de https://authors.repec.org/pro/pba423/
- **Acceso y licencia:** Revista por suscripción (Elsevier)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Baillie Bollerslev 1989 "The message in daily exchange rates: a conditional-variance tale" Journal of Business & Economic Statistics»; WebFetch: sí, sobre la página índice https://authors.repec.org/pro/pba423/, que reproduce la cita)
- **Contenido:** Mide desviaciones diarias de la UIP y su relación con las intervenciones cambiarias de los bancos centrales.
- **Uso en el Motor:** MC-03: efecto de la intervención en las desviaciones de paridad (TR-BCM, AS-EMAS).
- **Limitaciones:** Datos de intervención de los ochenta y noventa. Confirmada solo mediante página índice; pendiente de lectura de la fuente primaria.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0009 · Q 74 (B) — An Upsurge in a CIP Deviation during the Non-Crisis Period and the Role of Divergence in Monetary Policy

- **Autores:** Tomoyuki Iida; Takeshi Kimura; Nao Sudo
- **Año:** 2016
- **Publicación o institución:** Bank of Japan Working Paper Series n.º 16-E-14 (agosto de 2016)
- **Tipo de documento:** Documento de trabajo de institución reconocida
- **Temática:** TMX-03 Paridades y cálculo cambiario: CIP, puntos forward, base cruzada y convenciones (principal) · secundarias: —
- **Calidad Q:** 74 (B) — Tipo 20/25 · Rigor 14/20 · Autoridad 13/15 · Vigencia 8/10 · Impacto 5/10 · Independencia 9/10 · Acceso 5/10
- **DOI / ISBN / URL:** Confirmada en la bibliografía de https://www.bis.org/publ/qtrpdf/r_qt1609e.htm
- **Acceso y licencia:** Acceso abierto (Banco de Japón)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Borio McCauley McGuire Sushko "Covered interest parity lost…"»; WebFetch: sí, sobre la página índice del BIS Quarterly Review)
- **Contenido:** Relaciona la ampliación de la base USD/JPY fuera de crisis con la divergencia de políticas monetarias y la regulación bancaria.
- **Uso en el Motor:** MC-03: efecto de los diferenciales de política monetaria sobre la base (TR-BCM y AS-G10N para USD/JPY).
- **Limitaciones:** Documento de trabajo; pendiente de lectura de la fuente primaria.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0085 · Q 74 (B) — Motivations for Swap-Covered Foreign Currency Borrowing

- **Autores:** A. Munro; P. Wooldridge
- **Año:** 2010
- **Publicación o institución:** BIS Papers n.º 52 (julio de 2010), págs. 145-185
- **Tipo de documento:** Documento de trabajo de institución reconocida
- **Temática:** TMX-03 Paridades y cálculo cambiario: CIP, puntos forward, base cruzada y convenciones (principal) · secundarias: —
- **Calidad Q:** 74 (B) — Tipo 20/25 · Rigor 14/20 · Autoridad 14/15 · Vigencia 7/10 · Impacto 5/10 · Independencia 9/10 · Acceso 5/10
- **DOI / ISBN / URL:** Confirmada en la bibliografía de https://bis.org/publ/qtrpdf/r_qt1709e.htm
- **Acceso y licencia:** Acceso abierto (BPI)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Borio McCauley McGuire "FX swaps and forwards: missing global debt?" BIS Quarterly Review September 2017»; WebFetch: sí, sobre la página índice https://bis.org/publ/qtrpdf/r_qt1709e.htm, que reproduce la cita)
- **Contenido:** Estudia por qué bancos y empresas se endeudan en divisa extranjera y la convierten mediante swaps a moneda local (coste, profundidad de mercado, diversificación de inversores).
- **Uso en el Motor:** MC-01: estructura de los flujos de cross-currency swap en divisas de G10M y emergentes (AUD, NZD, KRW).
- **Limitaciones:** Datos anteriores a 2010. Confirmada solo mediante página índice; pendiente de lectura de la fuente primaria.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0008 · Q 72 (B) — Limits to Arbitrage and Deviations from Covered Interest Rate Parity

- **Autores:** James Pinnington; Maral Shamloo
- **Año:** 2016
- **Publicación o institución:** Bank of Canada, Staff Discussion Papers 16-4
- **Tipo de documento:** Documento de trabajo de institución reconocida
- **Temática:** TMX-03 Paridades y cálculo cambiario: CIP, puntos forward, base cruzada y convenciones (principal) · secundarias: —
- **Calidad Q:** 72 (B) — Tipo 18/25 · Rigor 14/20 · Autoridad 13/15 · Vigencia 8/10 · Impacto 5/10 · Independencia 9/10 · Acceso 5/10
- **DOI / ISBN / URL:** Confirmada en la bibliografía de https://www.bis.org/publ/qtrpdf/r_qt1609e.htm
- **Acceso y licencia:** Acceso abierto (Banco de Canadá)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Borio McCauley McGuire Sushko "Covered interest parity lost…"»; WebFetch: sí, sobre la página índice del BIS Quarterly Review)
- **Contenido:** Revisión de los límites al arbitraje (regulación, coste de balance) que mantienen desviaciones de la CIP, con la perspectiva del dólar canadiense.
- **Uso en el Motor:** MC-09: lectura de la base CAD/USD para AS-G10M.
- **Limitaciones:** Nota de discusión; pendiente de lectura de la fuente primaria.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

## TMX-04 Modelos cuantitativos de equilibrio y valoración

#### DOC-MOT-0239 · Q 94 (A) — Bounds Testing Approaches to the Analysis of Level Relationships

- **Autores:** M. Hashem Pesaran; Yongcheol Shin; Richard J. Smith
- **Año:** 2001
- **Publicación o institución:** Journal of Applied Econometrics, 16(3), 289-326
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-04 Modelos cuantitativos de equilibrio y valoración (principal) · secundarias: TMX-01
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1002/jae.616 · Verificada en páginas índice: https://en.wikipedia.org/wiki/Cointegration · https://en.wikipedia.org/wiki/Structural_break
- **Acceso y licencia:** Revista Wiley por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Cointegration wikipedia Engle-Granger Johansen test Phillips-Ouliaris references»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Cointegration)
- **Contenido:** Contraste de cotas ARDL para relaciones de nivel válido con regresores I(0), I(1) o mezcla, con valores críticos inferior y superior.
- **Uso en el Motor:** MC-03 y MC-09: enfoque ARDL de cotas para estimar relaciones de nivel entre tipo de cambio real y fundamentos (BEER) con regresores I(0)/I(1) mezclados, frecuente en divisas emergentes.
- **Limitaciones:** Confirmada solo mediante página índice (bibliografía de Wikipedia «Cointegration» y «Structural break»); pendiente de lectura de la fuente primaria.
- **Origen:** Reutilizada en F8 Forex V1.0 (2026-11-02) desde F8 V3.2.

#### FXM-0027 · Q 93 (A) — The External Balance Assessment Methodology: 2018 Update

- **Autores:** Luis Cubeddu; Signe Krogstrup; Gustavo Adler; Pau Rabanal; Mai Chi Dao; Swarnali Ahmed Hannan; Luciana Juvenal; Carolina Osorio Buitron; Cyril Rebillard; Daniel Garcia-Macia; Callum Jones; Jair Rodriguez; Kyun Suk Chang; Deepali Gautam; Zijiao Wang
- **Año:** 2019
- **Publicación o institución:** IMF Working Paper WP/19/65 (marzo de 2019)
- **Tipo de documento:** Documento metodológico de organismo oficial
- **Temática:** TMX-04 Modelos cuantitativos de equilibrio y valoración (principal) · secundarias: —
- **Calidad Q:** 93 (A) — Tipo 22/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 9/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://imf.org/-/media/Files/Publications/WP/2019/WPIEA2019065.ashx · https://www.sipotra.it/wp-content/uploads/2019/03/The-External-Balance-Assessment-Methodology-2018-Update.pdf (copia leída)
- **Acceso y licencia:** Acceso abierto (FMI)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «External Balance Assessment (EBA) methodology IMF working paper Phillips Catão Ricci 2013 Cubeddu 2019 update»; WebFetch: sí, sobre la copia en PDF devuelta por la búsqueda; DOI no visto)
- **Contenido:** Actualización 2018 del EBA para 49 economías: modelos de cuenta corriente y de tipo de cambio real, derivación de normas y brechas, elasticidades CA-REER y nuevas herramientas para factores estructurales y sesgos de medición.
- **Uso en el Motor:** MC-09: cálculo de la brecha del REER y su traducción en sobre/infravaloración; base del perfil de valor PERF-FX-FACT.
- **Limitaciones:** Juicio normativo en las brechas de políticas; muestra limitada a 49 economías.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0026 · Q 92 (A) — The External Balance Assessment (EBA) Methodology

- **Autores:** Steven T. Phillips; Luis Catão; Luca A. Ricci; Rudolfs Bems; Mitali Das; Julian di Giovanni; D. Filiz Unsal; Marola Castillo; Jungjin Lee; Jair Rodriguez; Mauricio Vargas
- **Año:** 2013
- **Publicación o institución:** IMF Working Paper WP/13/272 (Fondo Monetario Internacional)
- **Tipo de documento:** Documento metodológico de organismo oficial
- **Temática:** TMX-04 Modelos cuantitativos de equilibrio y valoración (principal) · secundarias: —
- **Calidad Q:** 92 (A) — Tipo 22/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 10/10 · Independencia 9/10 · Acceso 10/10
- **DOI / ISBN / URL:** DOI: 10.5089/9781484346686.001 · https://www.imf.org/en/publications/wp/issues/2016/12/31/the-external-balance-assessment-eba-methodology-41200
- **Acceso y licencia:** Acceso abierto (FMI)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «External Balance Assessment (EBA) methodology IMF working paper Phillips Catão Ricci 2013 Cubeddu 2019 update»; WebFetch: sí)
- **Contenido:** Metodología EBA del FMI (sucesora de CGER): regresiones de panel de cuenta corriente y de tipo de cambio real (índice y nivel), separación entre factores fundamentales y brechas de políticas, normas y brechas multilateralmente coherentes.
- **Uso en el Motor:** MC-09: modelo de referencia para estimar la desalineación del tipo de cambio real (brecha REER) por país; insumo de AS-ESTR (valor) y de los Analistas emergentes.
- **Limitaciones:** Brechas con bandas de incertidumbre amplias; versión superada en parte por la actualización de 2018.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### DOC-MOT-0243 · Q 88 (A) — Likelihood-Based Inference in Cointegrated Vector Autoregressive Models

- **Autores:** Søren Johansen
- **Año:** 1995
- **Publicación o institución:** Oxford University Press
- **Tipo de documento:** Manual de referencia
- **Temática:** TMX-04 Modelos cuantitativos de equilibrio y valoración (principal) · secundarias: TMX-01
- **Calidad Q:** 88 (A) — Tipo 20/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** Verificada en página índice: https://encyclopediaofmath.org/wiki/Vector_autoregressive_models
- **Acceso y licencia:** Libro de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Vector autoregression wikipedia Sims 1980 Lütkepohl structural VAR impulse response references»; WebFetch: sí, sobre la página índice https://encyclopediaofmath.org/wiki/Vector_autoregressive_models)
- **Contenido:** Tratado del enfoque de Johansen: representación, estimación de rango reducido, contrastes de rango e hipótesis sobre vectores de cointegración y ajuste.
- **Uso en el Motor:** MC-03 y MC-09: inferencia en VAR cointegrados para estimar relaciones de equilibrio del tipo de cambio real (BEER/PEER) y separar componentes permanentes y transitorios.
- **Limitaciones:** Confirmada solo mediante página índice (bibliografía de Encyclopedia of Mathematics); pendiente de lectura de la fuente primaria.
- **Origen:** Reutilizada en F8 Forex V1.0 (2026-11-02) desde F8 V3.2.

#### FXM-0036 · Q 87 (A) — Methodological Advances in the Assessment of Equilibrium Exchange Rates

- **Autores:** Matthieu Bussière; Michele Ca' Zorzi; Alexander Chudik; Alistair Dieppe
- **Año:** 2010
- **Publicación o institución:** European Central Bank, Working Paper Series n.º 1151
- **Tipo de documento:** Documento de trabajo de institución reconocida
- **Temática:** TMX-04 Modelos cuantitativos de equilibrio y valoración (principal) · secundarias: —
- **Calidad Q:** 87 (A) — Tipo 20/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 8/10 · Independencia 9/10 · Acceso 9/10
- **DOI / ISBN / URL:** https://ideas.repec.org/p/ecb/ecbwps/20101151.html
- **Acceso y licencia:** Acceso abierto (BCE)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ECB working paper "Methodological advances in the assessment of equilibrium exchange rates" Bussière Ca' Zorzi Chudik Dieppe»; WebFetch: sí, ficha IDEAS con resumen y bibliografía)
- **Contenido:** Revisa los enfoques de balance macroeconómico, sostenibilidad externa y forma reducida (CGER) y propone mejoras econométricas: promediado bayesiano de modelos para normas de cuenta corriente, incertidumbre de elasticidades comerciales, estimación en panel y dependencia transversal.
- **Uso en el Motor:** MC-09 y MC-03: diseño de la estimación en panel del tipo de cambio real de equilibrio y de las normas de cuenta corriente con incertidumbre de modelo.
- **Limitaciones:** Aplicación centrada en economías avanzadas y del este de Europa.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0037 · Q 87 (A) — Equilibrium Exchange Rates: Assessment Methodologies

- **Autores:** Peter Isard
- **Año:** 2007
- **Publicación o institución:** IMF Working Paper WP/07/296 (diciembre de 2007)
- **Tipo de documento:** Documento de trabajo de institución reconocida
- **Temática:** TMX-04 Modelos cuantitativos de equilibrio y valoración (principal) · secundarias: —
- **Calidad Q:** 87 (A) — Tipo 20/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 9/10 · Independencia 9/10 · Acceso 10/10
- **DOI / ISBN / URL:** DOI: 10.5089/9781451868593.001 · https://www.imf.org/en/publications/wp/issues/2016/12/31/equilibrium-exchange-rates-assessment-methodologies-21517
- **Acceso y licencia:** Acceso abierto (FMI)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ECB working paper "Methodological advances in the assessment of equilibrium exchange rates" Bussière Ca' Zorzi Chudik Dieppe»; WebFetch: sí, página del FMI devuelta por la búsqueda)
- **Contenido:** Describe seis metodologías de tipo de cambio de equilibrio (PPA, balance macroeconómico, sostenibilidad externa, BEER, FEER, DSGE, entre otras), sus limitaciones, y muestra con datos de EE. UU. de 2006 que pueden dar diagnósticos muy distintos.
- **Uso en el Motor:** MC-09: catálogo de métodos de equilibrio y regla de triangulación de varios enfoques antes de emitir una señal de valor (AS-ESTR).
- **Limitaciones:** Número de WP inferido del nombre del archivo del FMI; aplicación a un solo país.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0044 · Q 87 (A) — Medium-Term Determinants of Current Accounts in Industrial and Developing Countries

- **Autores:** Menzie D. Chinn; Eswar S. Prasad
- **Año:** 2003
- **Publicación o institución:** Journal of International Economics, vol. 59, n.º 1
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-04 Modelos cuantitativos de equilibrio y valoración (principal) · secundarias: —
- **Calidad Q:** 87 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 9/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** Confirmada en la bibliografía de https://ideas.repec.org/p/ecb/ecbwps/20101151.html
- **Acceso y licencia:** Revista por suscripción (Elsevier); versión NBER
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «ECB working paper "Methodological advances in the assessment of equilibrium exchange rates" Bussière Ca' Zorzi Chudik Dieppe»; WebFetch: sí, sobre la página índice https://ideas.repec.org/p/ecb/ecbwps/20101151.html, que reproduce la cita)
- **Contenido:** Regresiones de panel de los determinantes de medio plazo de la cuenta corriente (saldo fiscal, activos exteriores netos, demografía, renta relativa, apertura); base de las normas de cuenta corriente del CGER y del EBA.
- **Uso en el Motor:** MC-09: especificación de normas de cuenta corriente en el enfoque de balance macroeconómico.
- **Limitaciones:** Título tal como figura en el índice. Confirmada solo mediante página índice; pendiente de lectura de la fuente primaria.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0014 · Q 87 (A) — Exchange Rates and Economic Fundamentals: A Methodological Comparison of BEERs and FEERs

- **Autores:** Peter B. Clark; Ronald MacDonald
- **Año:** 1998
- **Publicación o institución:** IMF Working Papers 1998/067 (Fondo Monetario Internacional)
- **Tipo de documento:** Documento de trabajo de institución reconocida
- **Temática:** TMX-04 Modelos cuantitativos de equilibrio y valoración (principal) · secundarias: TMX-01
- **Calidad Q:** 87 (A) — Tipo 20/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 10/10 · Independencia 9/10 · Acceso 9/10
- **DOI / ISBN / URL:** https://ideas.repec.org/p/imf/imfwpa/1998-067.html · https://www.imf.org/en/Publications/WP/Issues/2016/12/30/Exchange-Rates-and-Economic-Fundamentals-A-Methodological-Comparison-of-BEERs-and-FEERs-2592
- **Acceso y licencia:** Acceso abierto (FMI)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Clark MacDonald 1998 "Exchange rates and economic fundamentals: a methodological comparison of BEERs and FEERs" IMF working paper»; WebFetch: sí, ficha IDEAS)
- **Contenido:** Define el BEER (relación econométrica entre tipo de cambio real efectivo y fundamentos) frente al FEER (tipo de cambio que equilibra la cuenta corriente con pleno empleo) y los aplica a las divisas del G3.
- **Uso en el Motor:** MC-09: especificación del BEER (diferenciales de tipos reales, activos exteriores netos, términos de intercambio, productividad) y cálculo de la desviación actual frente al equilibrio para AS-ESTR (valor).
- **Limitaciones:** Resultados sensibles a la especificación y a la muestra.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0048 · Q 85 (A) — The Reliability of Equilibrium Exchange Rate Models: A Forecasting Perspective

- **Autores:** Michele Ca' Zorzi; Adam Cap; Andrej Mijakovic; Michał Rubaszek
- **Año:** 2022
- **Publicación o institución:** International Journal of Central Banking, 3.er trimestre de 2022 (versión de trabajo: BCE WP 2358, 2020)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-04 Modelos cuantitativos de equilibrio y valoración (principal) · secundarias: TMX-08
- **Calidad Q:** 85 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 5/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** Confirmada en la bibliografía de https://authors.repec.org/pro/pca585/
- **Acceso y licencia:** Acceso abierto (IJCB); versión de trabajo del BCE
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «ECB working paper "Methodological advances in the assessment of equilibrium exchange rates" Bussière Ca' Zorzi Chudik Dieppe»; WebFetch: sí, sobre la página índice https://authors.repec.org/pro/pca585/, que reproduce la cita)
- **Contenido:** Evalúa fuera de muestra los modelos PPA, BEER y balance macroeconómico como predictores del tipo de cambio real: los más simples (PPA con reversión calibrada) son los más fiables.
- **Uso en el Motor:** MC-09 y MC-10: elección del modelo de equilibrio con mejor historial predictivo para la señal de valor.
- **Limitaciones:** Horizonte de medio plazo; ventajas pequeñas a corto plazo. Confirmada solo mediante página índice; pendiente de lectura de la fuente primaria.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0045 · Q 85 (A) — Thousands of Models, One Story: Current Account Imbalances in the Global Economy

- **Autores:** Michele Ca' Zorzi; Alexander Chudik; Alistair Dieppe
- **Año:** 2012
- **Publicación o institución:** Journal of International Money and Finance, vol. 31, n.º 6, págs. 1319-1338
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-04 Modelos cuantitativos de equilibrio y valoración (principal) · secundarias: —
- **Calidad Q:** 85 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 8/10 · Impacto 7/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** Confirmada en la bibliografía de https://authors.repec.org/pro/pca585/
- **Acceso y licencia:** Revista por suscripción (Elsevier); versión de trabajo BCE WP 1441
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «ECB working paper "Methodological advances in the assessment of equilibrium exchange rates" Bussière Ca' Zorzi Chudik Dieppe»; WebFetch: sí, sobre la página índice https://authors.repec.org/pro/pca585/, que reproduce la cita)
- **Contenido:** Promediado bayesiano sobre miles de especificaciones de cuenta corriente para obtener normas robustas a la incertidumbre de modelo.
- **Uso en el Motor:** MC-09: normas de cuenta corriente con promediado de modelos para FEER/balance macroeconómico.
- **Limitaciones:** Normas con bandas amplias. Confirmada solo mediante página índice; pendiente de lectura de la fuente primaria.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0043 · Q 85 (A) — The Purchasing-Power Parity Doctrine: A Reappraisal

- **Autores:** Bela Balassa
- **Año:** 1964
- **Publicación o institución:** Journal of Political Economy, vol. 72, n.º 6
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-04 Modelos cuantitativos de equilibrio y valoración (principal) · secundarias: —
- **Calidad Q:** 85 (A) — Tipo 25/25 · Rigor 13/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 10/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** Confirmada en la bibliografía de https://ideas.repec.org/p/ecb/ecbwps/20101151.html
- **Acceso y licencia:** Revista por suscripción (University of Chicago Press/JSTOR)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «ECB working paper "Methodological advances in the assessment of equilibrium exchange rates" Bussière Ca' Zorzi Chudik Dieppe»; WebFetch: sí, sobre la página índice https://ideas.repec.org/p/ecb/ecbwps/20101151.html, que reproduce la cita)
- **Contenido:** Efecto Balassa-Samuelson: la productividad relativa del sector comerciable eleva el tipo de cambio real de equilibrio de las economías que convergen.
- **Uso en el Motor:** MC-09: variable de productividad relativa en BEER y corrección de la PPA en divisas emergentes.
- **Limitaciones:** Obra clásica; la evidencia empírica del efecto es mixta. Confirmada solo mediante página índice; pendiente de lectura de la fuente primaria.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0038 · Q 84 (A) — Methodologies for the Assessment of Real Effective Exchange Rates

- **Autores:** Leonor Coutinho; Nuria Mata Garcia; Alessandro Turrini; Goran Vukšić
- **Año:** 2021
- **Publicación o institución:** European Economy – Discussion Papers n.º 149, Dirección General de Asuntos Económicos y Financieros (DG ECFIN), Comisión Europea
- **Tipo de documento:** Documento metodológico de organismo oficial
- **Temática:** TMX-04 Modelos cuantitativos de equilibrio y valoración (principal) · secundarias: —
- **Calidad Q:** 84 (A) — Tipo 20/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 6/10 · Independencia 9/10 · Acceso 9/10
- **DOI / ISBN / URL:** https://ideas.repec.org/p/euf/dispap/149.html
- **Acceso y licencia:** Acceso abierto (Comisión Europea)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ECB working paper "Methodological advances in the assessment of equilibrium exchange rates" Bussière Ca' Zorzi Chudik Dieppe»; WebFetch: sí, ficha IDEAS)
- **Contenido:** Referencias de tipo de cambio real efectivo basadas en modelos BEER y niveles de REER comparables entre países construidos con PPA del Programa de Comparación Internacional del Banco Mundial (siguiendo a Cubeddu et al.), complementarias a las brechas de cuenta corriente del Procedimiento de Desequilibrios Macroeconómicos de la UE.
- **Uso en el Motor:** MC-09: BEER en índice y en nivel para divisas europeas (EUR, PLN, HUF, CZK, RON) en AS-G10N y AS-EMEA.
- **Limitaciones:** Enfoque de vigilancia de la UE; sin DOI visible.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0042 · Q 79 (B) — Towards the Estimation of Equilibrium Exchange Rates for Transition Economies

- **Autores:** Francisco Maeso-Fernandez; Chiara Osbat; Bernd Schnatz
- **Año:** 2006
- **Publicación o institución:** Journal of Comparative Economics, vol. 34, n.º 3
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-04 Modelos cuantitativos de equilibrio y valoración (principal) · secundarias: —
- **Calidad Q:** 79 (B) — Tipo 22/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 7/10 · Impacto 7/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** Confirmada en la bibliografía de https://ideas.repec.org/p/ecb/ecbwps/20101151.html
- **Acceso y licencia:** Revista por suscripción (Elsevier)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «ECB working paper "Methodological advances in the assessment of equilibrium exchange rates" Bussière Ca' Zorzi Chudik Dieppe»; WebFetch: sí, sobre la página índice https://ideas.repec.org/p/ecb/ecbwps/20101151.html, que reproduce la cita)
- **Contenido:** Propone estimar el equilibrio de economías en transición con coeficientes de panel de economías avanzadas (fuera de muestra), por la brevedad y los cambios estructurales de sus series.
- **Uso en el Motor:** MC-09: BEER para divisas emergentes con historia corta (EMEA: PLN, HUF, CZK, RON) mediante panel.
- **Limitaciones:** Título tal como figura en el índice (posible subtítulo no visto). Confirmada solo mediante página índice; pendiente de lectura de la fuente primaria.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0039 · Q 79 (B) — Concepts of Equilibrium Exchange Rates

- **Autores:** Rebecca L. Driver; Peter F. Westaway
- **Año:** 2005
- **Publicación o institución:** Bank of England, Staff Working Paper n.º 248
- **Tipo de documento:** Documento de trabajo de institución reconocida
- **Temática:** TMX-04 Modelos cuantitativos de equilibrio y valoración (principal) · secundarias: —
- **Calidad Q:** 79 (B) — Tipo 20/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 7/10 · Impacto 8/10 · Independencia 9/10 · Acceso 6/10
- **DOI / ISBN / URL:** Confirmada en la bibliografía de https://ideas.repec.org/p/ecb/ecbwps/20101151.html
- **Acceso y licencia:** Acceso abierto (Banco de Inglaterra)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «ECB working paper "Methodological advances in the assessment of equilibrium exchange rates" Bussière Ca' Zorzi Chudik Dieppe»; WebFetch: sí, sobre la página índice https://ideas.repec.org/p/ecb/ecbwps/20101151.html, que reproduce la cita)
- **Contenido:** Clasifica los conceptos de tipo de cambio de equilibrio por horizonte (corto, medio y largo plazo) y por enfoque (PPA, UIP, BEER, FEER, DEER, NATREX, PEER).
- **Uso en el Motor:** MC-09: taxonomía para elegir el concepto de equilibrio según el horizonte H1-H4 de la oportunidad.
- **Limitaciones:** Texto conceptual sin estimaciones actualizadas. Confirmada solo mediante página índice; pendiente de lectura de la fuente primaria.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0041 · Q 79 (B) — Determinants of the Euro Real Effective Exchange Rate: A BEER/PEER Approach

- **Autores:** Francisco Maeso-Fernandez; Chiara Osbat; Bernd Schnatz
- **Año:** 2002
- **Publicación o institución:** Australian Economic Papers, vol. 41, n.º 4
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-04 Modelos cuantitativos de equilibrio y valoración (principal) · secundarias: —
- **Calidad Q:** 79 (B) — Tipo 22/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 7/10 · Impacto 7/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** Confirmada en la bibliografía de https://ideas.repec.org/p/ecb/ecbwps/20101151.html
- **Acceso y licencia:** Revista por suscripción (Wiley); versión de trabajo del BCE
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «ECB working paper "Methodological advances in the assessment of equilibrium exchange rates" Bussière Ca' Zorzi Chudik Dieppe»; WebFetch: sí, sobre la página índice https://ideas.repec.org/p/ecb/ecbwps/20101151.html, que reproduce la cita)
- **Contenido:** Estima el BEER del euro sintético con productividad relativa, diferenciales de tipos reales, activos exteriores netos y precio del petróleo, y el PEER (componente permanente) por descomposición de Gonzalo-Granger.
- **Uso en el Motor:** MC-09: especificación BEER/PEER del EUR efectivo (AS-G10N).
- **Limitaciones:** Muestra anterior al euro en circulación. Confirmada solo mediante página índice; pendiente de lectura de la fuente primaria.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0028 · Q 78 (B) — 2009 Estimates of Fundamental Equilibrium Exchange Rates

- **Autores:** William R. Cline; John Williamson
- **Año:** 2009
- **Publicación o institución:** Peterson Institute for International Economics, Policy Brief PB09-10 (junio de 2009)
- **Tipo de documento:** Informe técnico con metodología
- **Temática:** TMX-04 Modelos cuantitativos de equilibrio y valoración (principal) · secundarias: —
- **Calidad Q:** 78 (B) — Tipo 15/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 7/10 · Impacto 9/10 · Independencia 9/10 · Acceso 9/10
- **DOI / ISBN / URL:** https://ideas.repec.org/p/iie/pbrief/pb09-10.html · https://piie.com/publications/policy-briefs/2009-estimates-fundamental-equilibrium-exchange-rates
- **Acceso y licencia:** Acceso abierto (PIIE)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Cline Williamson fundamental equilibrium exchange rates FEER estimates SMIC model Peterson Institute»; WebFetch: sí, ficha IDEAS)
- **Contenido:** Estima objetivos de cuenta corriente para 34 economías y los convierte en tipos FEER bilaterales frente al dólar con el método de inversión matricial simétrica (SMIM) de Cline; compara con las estimaciones del año anterior.
- **Uso en el Motor:** MC-09: procedimiento FEER (objetivo de cuenta corriente → tipo de cambio efectivo → bilaterales coherentes) para AS-ESTR y los Analistas de segmento.
- **Limitaciones:** Objetivos de cuenta corriente normativos; estimaciones fechadas (serie semestral discontinuada).
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0049 · Q 77 (B) — Boosting Carry with Equilibrium Exchange Rate Estimates

- **Autores:** Michał Rubaszek; Joscha Beckmann; Michele Ca' Zorzi; Marek Kwas
- **Año:** 2022
- **Publicación o institución:** European Central Bank, Working Paper Series n.º 2731
- **Tipo de documento:** Documento de trabajo de institución reconocida
- **Temática:** TMX-04 Modelos cuantitativos de equilibrio y valoración (principal) · secundarias: TMX-06
- **Calidad Q:** 77 (B) — Tipo 20/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 4/10 · Independencia 9/10 · Acceso 5/10
- **DOI / ISBN / URL:** Confirmada en la bibliografía de https://authors.repec.org/pro/pca585/
- **Acceso y licencia:** Acceso abierto (BCE)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «ECB working paper "Methodological advances in the assessment of equilibrium exchange rates" Bussière Ca' Zorzi Chudik Dieppe»; WebFetch: sí, sobre la página índice https://authors.repec.org/pro/pca585/, que reproduce la cita)
- **Contenido:** Combina la señal de carry con estimaciones de equilibrio (desalineación) para mejorar la rentabilidad ajustada al riesgo de las carteras de divisas.
- **Uso en el Motor:** MC-09 y MC-07: filtro de valor sobre carteras de carry en PERF-FX-FACT (AS-ESTR).
- **Limitaciones:** Documento de trabajo reciente. Confirmada solo mediante página índice; pendiente de lectura de la fuente primaria.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0046 · Q 77 (B) — Evaluating Historical CGER Assessments

- **Autores:** J. Lee; A. Abiad; P. Kannan
- **Año:** 2009
- **Publicación o institución:** IMF Working Paper WP/09/32
- **Tipo de documento:** Documento de trabajo de institución reconocida
- **Temática:** TMX-04 Modelos cuantitativos de equilibrio y valoración (principal) · secundarias: —
- **Calidad Q:** 77 (B) — Tipo 20/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 6/10 · Independencia 9/10 · Acceso 5/10
- **DOI / ISBN / URL:** Confirmada en la bibliografía de https://ideas.repec.org/p/ecb/ecbwps/20101151.html
- **Acceso y licencia:** Acceso abierto (FMI)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «ECB working paper "Methodological advances in the assessment of equilibrium exchange rates" Bussière Ca' Zorzi Chudik Dieppe»; WebFetch: sí, sobre la página índice https://ideas.repec.org/p/ecb/ecbwps/20101151.html, que reproduce la cita)
- **Contenido:** Evalúa si las desalineaciones estimadas por el CGER del FMI anticiparon los movimientos posteriores del tipo de cambio real.
- **Uso en el Motor:** MC-09 y MC-10: validación ex post de señales de equilibrio como predictoras de corrección.
- **Limitaciones:** Título tal como figura en el índice (posible subtítulo no visto). Confirmada solo mediante página índice; pendiente de lectura de la fuente primaria.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0051 · Q 77 (B) — Determinants of the Effective Real Exchange Rate of the Synthetic Euro

- **Autores:** C. Detken; A. Dieppe; J. Henry; F. Smets; C. Marin
- **Año:** 2002
- **Publicación o institución:** Australian Economic Papers, vol. 41, n.º 4
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-04 Modelos cuantitativos de equilibrio y valoración (principal) · secundarias: —
- **Calidad Q:** 77 (B) — Tipo 22/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 6/10 · Impacto 6/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** Confirmada en la bibliografía de https://ideas.repec.org/p/ecb/ecbwps/20101151.html
- **Acceso y licencia:** Revista por suscripción (Wiley)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «ECB working paper "Methodological advances in the assessment of equilibrium exchange rates" Bussière Ca' Zorzi Chudik Dieppe»; WebFetch: sí, sobre la página índice https://ideas.repec.org/p/ecb/ecbwps/20101151.html, que reproduce la cita)
- **Contenido:** Compara enfoques alternativos (BEER, NATREX, modelo estructural) para el tipo de cambio real efectivo del euro sintético.
- **Uso en el Motor:** MC-09: contraste de robustez de la valoración del EUR con varios métodos.
- **Limitaciones:** Título tal como figura en el índice (posible subtítulo no visto); muestra anterior a 2002. Confirmada solo mediante página índice; pendiente de lectura de la fuente primaria.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0040 · Q 77 (B) — Estimating Equilibrium Exchange Rates

- **Autores:** John Williamson (ed.)
- **Año:** 1994
- **Publicación o institución:** Peterson Institute for International Economics (Institute for International Economics), Washington
- **Tipo de documento:** Manual de referencia (libro colectivo)
- **Temática:** TMX-04 Modelos cuantitativos de equilibrio y valoración (principal) · secundarias: —
- **Calidad Q:** 77 (B) — Tipo 20/25 · Rigor 14/20 · Autoridad 15/15 · Vigencia 6/10 · Impacto 9/10 · Independencia 9/10 · Acceso 4/10
- **DOI / ISBN / URL:** Confirmada en la bibliografía de https://ideas.repec.org/p/ecb/ecbwps/20101151.html
- **Acceso y licencia:** Libro (PIIE)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «ECB working paper "Methodological advances in the assessment of equilibrium exchange rates" Bussière Ca' Zorzi Chudik Dieppe»; WebFetch: sí, sobre la página índice https://ideas.repec.org/p/ecb/ecbwps/20101151.html, que reproduce la cita)
- **Contenido:** Obra fundacional del enfoque FEER: tipo de cambio real compatible con equilibrio interno (pleno empleo) y externo (cuenta corriente sostenible) y estimaciones para las grandes economías.
- **Uso en el Motor:** MC-09: definición de referencia del FEER y del balance macroeconómico.
- **Limitaciones:** Estimaciones históricas; sensibilidad a los supuestos de elasticidades. Confirmada solo mediante página índice; pendiente de lectura de la fuente primaria.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0029 · Q 75 (B) — Estimates of Fundamental Equilibrium Exchange Rates, May 2012

- **Autores:** William R. Cline; John Williamson
- **Año:** 2012
- **Publicación o institución:** Peterson Institute for International Economics, Policy Brief PB12-14 (mayo de 2012)
- **Tipo de documento:** Informe técnico con metodología
- **Temática:** TMX-04 Modelos cuantitativos de equilibrio y valoración (principal) · secundarias: —
- **Calidad Q:** 75 (B) — Tipo 15/25 · Rigor 14/20 · Autoridad 14/15 · Vigencia 7/10 · Impacto 7/10 · Independencia 9/10 · Acceso 9/10
- **DOI / ISBN / URL:** https://econpapers.repec.org/paper/iiepbrief/pb12-14.htm
- **Acceso y licencia:** Acceso abierto (PIIE)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Cline Williamson fundamental equilibrium exchange rates FEER estimates SMIC model Peterson Institute»; WebFetch: sí, ficha EconPapers)
- **Contenido:** FEER con proyecciones del WEO de primavera de 2012: dólar sobrevalorado y renminbi infravalorado un 3-4 % en términos efectivos; medida agregada de desalineación ponderada por PIB y su evolución desde 2009.
- **Uso en el Motor:** MC-09: ejemplo de cálculo de la desalineación agregada y de su seguimiento temporal; contraste de coherencia con el EBA.
- **Limitaciones:** Estimaciones fechadas; dependientes de las proyecciones del FMI.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0047 · Q 75 (B) — Exchange Rate Misalignment: Concepts and Measurement for Developing Countries

- **Autores:** Lawrence E. Hinkle; Peter J. Montiel (eds.)
- **Año:** 1999
- **Publicación o institución:** Oxford University Press (para el Banco Mundial)
- **Tipo de documento:** Manual de referencia
- **Temática:** TMX-04 Modelos cuantitativos de equilibrio y valoración (principal) · secundarias: —
- **Calidad Q:** 75 (B) — Tipo 20/25 · Rigor 14/20 · Autoridad 14/15 · Vigencia 6/10 · Impacto 8/10 · Independencia 9/10 · Acceso 4/10
- **DOI / ISBN / URL:** Confirmada en la bibliografía de https://ideas.repec.org/p/ecb/ecbwps/20101151.html
- **Acceso y licencia:** Libro comercial
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «ECB working paper "Methodological advances in the assessment of equilibrium exchange rates" Bussière Ca' Zorzi Chudik Dieppe»; WebFetch: sí, sobre la página índice https://ideas.repec.org/p/ecb/ecbwps/20101151.html, que reproduce la cita)
- **Contenido:** Manual de medición de la desalineación del tipo de cambio real en países en desarrollo: índices de tipo de cambio real, PPA, modelos de equilibrio general y de forma reducida.
- **Uso en el Motor:** MC-09: medición de desalineaciones en divisas emergentes y frontera (AS-EMLA, AS-EMEA).
- **Limitaciones:** Datos y ejemplos de los noventa. Confirmada solo mediante página índice; pendiente de lectura de la fuente primaria.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0030 · Q 74 (B) — Estimating Consistent Fundamental Equilibrium Exchange Rates

- **Autores:** William R. Cline
- **Año:** 2008
- **Publicación o institución:** Peterson Institute for International Economics, Working Paper 08-6
- **Tipo de documento:** Documento de trabajo de institución reconocida
- **Temática:** TMX-04 Modelos cuantitativos de equilibrio y valoración (principal) · secundarias: —
- **Calidad Q:** 74 (B) — Tipo 18/25 · Rigor 14/20 · Autoridad 14/15 · Vigencia 7/10 · Impacto 7/10 · Independencia 9/10 · Acceso 5/10
- **DOI / ISBN / URL:** Citado como origen del método SMIM en https://ideas.repec.org/p/iie/pbrief/pb09-10.html
- **Acceso y licencia:** Acceso abierto (PIIE)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Cline Williamson fundamental equilibrium exchange rates FEER estimates SMIC model Peterson Institute»; WebFetch: sí, sobre la ficha IDEAS de PB09-10, que identifica el WP 08-6 como origen del método)
- **Contenido:** Presenta el método de inversión matricial simétrica (SMIM) para obtener tipos de cambio bilaterales coherentes entre sí a partir de objetivos de cuenta corriente de muchas economías.
- **Uso en el Motor:** MC-09: algoritmo para pasar de desalineaciones efectivas a bilaterales coherentes (evita que la suma de desalineaciones no cuadre).
- **Limitaciones:** Título confirmado solo por referencia indirecta (el índice cita «Working Paper 08-6» y el método); pendiente de lectura de la fuente primaria.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0050 · Q 74 (B) — In Search of Equilibrium: Estimating Equilibrium Real Exchange Rates in Sub-Saharan African Countries

- **Autores:** J. Mongardini; Alexander Chudik
- **Año:** 2007
- **Publicación o institución:** IMF Working Paper WP/07/90
- **Tipo de documento:** Documento de trabajo de institución reconocida
- **Temática:** TMX-04 Modelos cuantitativos de equilibrio y valoración (principal) · secundarias: —
- **Calidad Q:** 74 (B) — Tipo 20/25 · Rigor 14/20 · Autoridad 14/15 · Vigencia 7/10 · Impacto 5/10 · Independencia 9/10 · Acceso 5/10
- **DOI / ISBN / URL:** Confirmada en la bibliografía de https://ideas.repec.org/p/ecb/ecbwps/20101151.html
- **Acceso y licencia:** Acceso abierto (FMI)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «ECB working paper "Methodological advances in the assessment of equilibrium exchange rates" Bussière Ca' Zorzi Chudik Dieppe»; WebFetch: sí, sobre la página índice https://ideas.repec.org/p/ecb/ecbwps/20101151.html, que reproduce la cita)
- **Contenido:** Estimación de tipos de cambio reales de equilibrio en panel para economías africanas con series cortas.
- **Uso en el Motor:** MC-09: valoración de divisas africanas (ZAR, NGN, KES) en AS-EMEA.
- **Limitaciones:** Muestra y datos de baja calidad. Confirmada solo mediante página índice; pendiente de lectura de la fuente primaria.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

## TMX-05 Opciones de divisas: Garman-Kohlhagen, superficie de volatilidad, risk reversals y densidades implícitas

#### DOC-MOT-0324 · Q 95 (A) — Arbitrage-Free SVI Volatility Surfaces

- **Autores:** Jim Gatheral; Antoine Jacquier
- **Año:** 2014
- **Publicación o institución:** Quantitative Finance, vol. 14, págs. 59-71
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-05 Opciones de divisas: Garman-Kohlhagen, superficie de volatilidad, risk reversals y densidades implícitas (principal) · secundarias: —
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** DOI: 10.1080/14697688.2013.819986 · arXiv: https://arxiv.org/abs/1204.0646
- **Acceso y licencia:** Preprint gratuito en arXiv; revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «local volatility Dupire SABR volatility model volatility smile variance swap (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Stochastic volatility», que reproduce la cita completa)
- **Contenido:** Condiciones para parametrizaciones SVI libres de arbitraje estático (mariposa y calendario) y método de ajuste de superficies.
- **Uso en el Motor:** MC-09: parametrización SVI libre de arbitraje para construir la superficie de volatilidad de divisas a partir de las cotizaciones de ATM, risk reversals y butterflies.
- **Limitaciones:** Parametrización específica; requiere optimización cuidadosa.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02. Reutilizada en F8 Forex V1.0 (2026-11-02) desde F8 V3.2.

#### DOC-MOT-0004 · Q 94 (A) — A Closed-Form Solution for Options with Stochastic Volatility with Applications to Bond and Currency Options

- **Autores:** Steven L. Heston
- **Año:** 1993
- **Publicación o institución:** The Review of Financial Studies, vol. 6, n.º 2, págs. 327-343 (Oxford University Press)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-05 Opciones de divisas: Garman-Kohlhagen, superficie de volatilidad, risk reversals y densidades implícitas (principal) · secundarias: —
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1093/rfs/6.2.327 · https://doi.org/10.1093%2Frfs%2F6.2.327
- **Acceso y licencia:** Texto completo por suscripción en la editorial (OUP)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «VIX variance swap jump diffusion volatility risk premium implied volatility (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Stochastic volatility jump models», que reproduce la cita completa y «Stochastic volatility»)
- **Contenido:** Solución semicerrada mediante función característica para opciones europeas con volatilidad estocástica de reversión a la media correlacionada con el subyacente.
- **Uso en el Motor:** MC-09: modelo de Heston con aplicación explícita a opciones de divisas; base de la sonrisa y del skew en PERF-FX-G10 y de los modelos de volatilidad estocástica-local.
- **Limitaciones:** Integración numérica sensible a parámetros; calibración no tratada.
- **Origen:** Ficha de carga V2.3 re-verificada por DOC-M el 2026-11-02 (tanda 2); se normaliza al formato del encargo. Reutilizada en F8 Forex V1.0 (2026-11-02) desde F8 V3.2.

#### DOC-MOT-0325 · Q 93 (A) — Jumps and Stochastic Volatility: Exchange Rate Processes Implicit in Deutsche Mark Options

- **Autores:** David S. Bates
- **Año:** 1996
- **Publicación o institución:** The Review of Financial Studies, vol. 9, n.º 1, págs. 69-107
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-05 Opciones de divisas: Garman-Kohlhagen, superficie de volatilidad, risk reversals y densidades implícitas (principal) · secundarias: TMX-07
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1093/rfs/9.1.69 · https://doi.org/10.1093%2Frfs%2F9.1.69
- **Acceso y licencia:** Texto completo por suscripción en la editorial (OUP)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «VIX variance swap jump diffusion volatility risk premium implied volatility (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Stochastic volatility jump models», que reproduce la cita completa)
- **Contenido:** Combina volatilidad estocástica tipo Heston con saltos (modelo SVJ) y lo estima con opciones sobre el marco alemán.
- **Uso en el Motor:** MC-09: saltos y volatilidad estocástica implícitos en opciones sobre el marco alemán; referencia para extraer el riesgo de salto de la superficie de volatilidad de un par (TR-PFV).
- **Limitaciones:** Calibración con muchos parámetros.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02. Reutilizada en F8 Forex V1.0 (2026-11-02) desde F8 V3.2.

#### FXM-0013 · Q 92 (A) — Stochastic Skew in Currency Options

- **Autores:** Peter Carr; Liuren Wu
- **Año:** 2007
- **Publicación o institución:** Journal of Financial Economics, vol. 86, n.º 1, págs. 213-247
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-05 Opciones de divisas: Garman-Kohlhagen, superficie de volatilidad, risk reversals y densidades implícitas (principal) · secundarias: TMX-07
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** https://ideas.repec.org/a/eee/jfinec/v86y2007i1p213-247.html
- **Acceso y licencia:** Por suscripción (Elsevier); versión de trabajo en abierto (EconWPA)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Carr Wu 2007 "Stochastic skew in currency options" Journal of Financial Economics»; WebFetch: sí, ficha IDEAS/RePEc; DOI no visto)
- **Contenido:** Con opciones OTC de JPY/USD y GBP/USD muestra que la asimetría neutral al riesgo es nula en media pero muy variable y cambia de signo; propone modelos de salto y volatilidad estocástica con asimetría estocástica.
- **Uso en el Motor:** MC-09: modelización de risk reversals variables en el tiempo y de la asimetría de un par; TR-PFV.
- **Limitaciones:** Calibración compleja; dos pares.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### DOC-MOT-0056 · Q 90 (A) — Prices of State-Contingent Claims Implicit in Option Prices

- **Autores:** Douglas T. Breeden; Robert H. Litzenberger
- **Año:** 1978
- **Publicación o institución:** The Journal of Business, págs. 621-651
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-05 Opciones de divisas: Garman-Kohlhagen, superficie de volatilidad, risk reversals y densidades implícitas (principal) · secundarias: —
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** DOI no visto (se retira «10.1086/296025 a verificar») · Cita en https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_model
- **Acceso y licencia:** Texto completo por suscripción en la editorial (University of Chicago Press/JSTOR); sin copia abierta identificada
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Black–Scholes model Merton 1973 Heston model binomial options pricing (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Black–Scholes model», que reproduce la cita completa)
- **Contenido:** Muestra que la segunda derivada del precio de la opción respecto al precio de ejercicio da la densidad de precios de estado (densidad neutral al riesgo).
- **Uso en el Motor:** MC-09: densidad neutral al riesgo como segunda derivada del precio de la opción respecto al strike; base de las densidades implícitas de tipos de cambio.
- **Limitaciones:** Requiere interpolación suave de la curva de precios por strike. Alerta: REPARAR (localizar DOI/volumen en la editorial).
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (tanda 2). Reutilizada en F8 Forex V1.0 (2026-11-02) desde F8 V3.2.

#### FXM-0011 · Q 89 (A) — Foreign Currency Option Values

- **Autores:** Mark B. Garman; Steven W. Kohlhagen
- **Año:** 1983
- **Publicación o institución:** Journal of International Money and Finance, vol. 2, n.º 3, págs. 231-237
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-05 Opciones de divisas: Garman-Kohlhagen, superficie de volatilidad, risk reversals y densidades implícitas (principal) · secundarias: TMX-03
- **Calidad Q:** 89 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** https://macroption.com/foreign-currency-option-values-garman-kohlhagen (página que reproduce la cita y el modelo; registro también en EconBiz)
- **Acceso y licencia:** Artículo por suscripción (Elsevier); la página enlazada es divulgativa
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Garman Kohlhagen 1983 foreign currency option values Journal of International Money and Finance»; WebFetch: sí, sobre la página de Macroption con la cita completa; DOI no visto)
- **Contenido:** Fórmula cerrada de opciones europeas sobre divisas: Black-Scholes con el tipo de interés extranjero en el papel de rendimiento continuo.
- **Uso en el Motor:** MC-09: modelo base para precio, griegas, volatilidad implícita y conversión de deltas de las opciones de divisas (PERF-FX-G10 y PERF-FX-EM).
- **Limitaciones:** Volatilidad constante; no reproduce la sonrisa.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0075 · Q 86 (A) — Simple and Reliable Way to Compute Option-Based Risk-Neutral Distributions

- **Autores:** Allan M. Malz
- **Año:** 2014
- **Publicación o institución:** Federal Reserve Bank of New York, Staff Reports n.º 677
- **Tipo de documento:** Documento de trabajo de institución reconocida
- **Temática:** TMX-05 Opciones de divisas: Garman-Kohlhagen, superficie de volatilidad, risk reversals y densidades implícitas (principal) · secundarias: —
- **Calidad Q:** 86 (A) — Tipo 20/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 7/10 · Independencia 9/10 · Acceso 9/10
- **DOI / ISBN / URL:** https://ideas.repec.org/p/fip/fednsr/677.html
- **Acceso y licencia:** Acceso abierto (Fed de Nueva York)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Malz "A simple and reliable way to compute option-based risk-neutral distributions" Federal Reserve Bank of New York staff report»; WebFetch: sí, ficha IDEAS)
- **Contenido:** Procedimiento paso a paso para estimar densidades neutrales al riesgo a partir de la sonrisa de volatilidad implícita respetando las restricciones de no arbitraje (sin probabilidades negativas); ejemplos con acciones, divisas y tipos de interés.
- **Uso en el Motor:** MC-09: algoritmo de referencia para extraer la densidad implícita de un par a partir de ATM, risk reversals y butterflies (TR-PFV).
- **Limitaciones:** Extrapolación de colas basada en supuestos.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### DOC-MOT-0334 · Q 86 (A) — Summary Statistics of Option-Implied Probability Density Functions and Their Properties

- **Autores:** Damien Lynch; Nikolaos Panigirtzoglou
- **Año:** 2008
- **Publicación o institución:** Bank of England Working Paper n.º 345 (marzo de 2008)
- **Tipo de documento:** Documento de trabajo
- **Temática:** TMX-05 Opciones de divisas: Garman-Kohlhagen, superficie de volatilidad, risk reversals y densidades implícitas (principal) · secundarias: —
- **Calidad Q:** 86 (A) — Tipo 20/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 7/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://www.bankofengland.co.uk/-/media/boe/files/working-paper/2008/summary-statistics-of-option-implied-probability-density-functions.pdf
- **Acceso y licencia:** Acceso gratuito (Banco de Inglaterra)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Bank of England Quarterly Bulletin 2012 "Option-implied probability distributions for future inflation"»; WebFetch: sí, documento completo)
- **Contenido:** Estadísticos diarios de densidades implícitas (incertidumbre, asimetría, colas) para índices y tipos de EE. UU. y Reino Unido: persistentes, reaccionan a crisis pero no las anticipan.
- **Uso en el Motor:** MC-09: estadísticos resumen (incertidumbre, asimetría, colas) de densidades implícitas, aplicables a las densidades de pares de divisas que publica TR-PFV.
- **Limitaciones:** Muestra hasta 2006.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02. Reutilizada en F8 Forex V1.0 (2026-11-02) desde F8 V3.2.

#### DOC-MOT-0323 · Q 86 (A) — Managing Smile Risk

- **Autores:** Patrick S. Hagan; Deep Kumar; Andrew S. Lesniewski; Diana E. Woodward
- **Año:** 2002
- **Publicación o institución:** Wilmott Magazine, págs. 84-108
- **Tipo de documento:** Artículo en revista profesional
- **Temática:** TMX-05 Opciones de divisas: Garman-Kohlhagen, superficie de volatilidad, risk reversals y densidades implícitas (principal) · secundarias: —
- **Calidad Q:** 86 (A) — Tipo 15/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** Sin DOI · Copia de autor: http://lesniewski.us/papers/published/ManagingSmileRisk.pdf
- **Acceso y licencia:** Copia gratuita del autor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «local volatility Dupire SABR volatility model volatility smile variance swap (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «SABR volatility model», que reproduce la cita completa)
- **Contenido:** Introduce el modelo SABR y su aproximación asintótica de volatilidad implícita, con dinámica de sonrisa coherente.
- **Uso en el Motor:** MC-09: modelo SABR para interpolar la sonrisa de un par por plazo y gestionar el riesgo de sonrisa.
- **Limitaciones:** Aproximación inexacta en alas y con tipos bajos; ver versión sin arbitraje.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02. Reutilizada en F8 Forex V1.0 (2026-11-02) desde F8 V3.2.

#### FXM-0021 · Q 85 (A) — FX Options and Structured Products (2.ª ed.)

- **Autores:** Uwe Wystup
- **Año:** 2017 (1.ª ed. 2006)
- **Publicación o institución:** John Wiley & Sons (Wiley Finance)
- **Tipo de documento:** Manual de referencia
- **Temática:** TMX-05 Opciones de divisas: Garman-Kohlhagen, superficie de volatilidad, risk reversals y densidades implícitas (principal) · secundarias: —
- **Calidad Q:** 85 (A) — Tipo 20/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** Confirmada en la bibliografía de https://arxiv.org/pdf/2512.19621
- **Acceso y licencia:** Libro comercial
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Foreign exchange option Garman Kohlhagen vanna-volga Reiswich Wystup delta conventions wikipedia»; WebFetch: sí, sobre la página índice arXiv:2512.19621 y la nota de MathFinance que cita la 1.ª ed.)
- **Contenido:** Referencia de mercado sobre opciones de divisas vainilla, de primera y segunda generación y productos estructurados, con convenciones, griegas y métodos de valoración (incluido vanna-volga).
- **Uso en el Motor:** MC-09: fórmulas de exóticas (barreras, digitales) y convenciones para AS-ESTR (estrategias de volatilidad).
- **Limitaciones:** Orientación práctica; pendiente de lectura de la fuente primaria.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0017 · Q 85 (A) — Foreign Exchange Option Pricing: A Practitioner's Guide

- **Autores:** Iain J. Clark
- **Año:** 2011
- **Publicación o institución:** John Wiley & Sons
- **Tipo de documento:** Manual de referencia
- **Temática:** TMX-05 Opciones de divisas: Garman-Kohlhagen, superficie de volatilidad, risk reversals y densidades implícitas (principal) · secundarias: TMX-03
- **Calidad Q:** 85 (A) — Tipo 20/25 · Rigor 17/20 · Autoridad 13/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** Confirmada en la bibliografía de https://arxiv.org/pdf/2512.19621
- **Acceso y licencia:** Libro comercial
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Foreign exchange option Garman Kohlhagen vanna-volga Reiswich Wystup delta conventions wikipedia»; WebFetch: sí, sobre la página índice arXiv:2512.19621)
- **Contenido:** Guía práctica de valoración de opciones de divisas: convenciones de mercado (fechas de valor, deltas con o sin prima), superficie de volatilidad, volatilidad local y estocástica-local, barreras y exóticas.
- **Uso en el Motor:** MC-01 y MC-09: convenciones de fechas y deltas, y modelos de sonrisa para PERF-FX-G10 y PERF-FX-EM.
- **Limitaciones:** Pendiente de lectura de la fuente primaria.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### DOC-MOT-0059 · Q 84 (A) — Options, Futures, and Other Derivatives (11.ª ed.)

- **Autores:** John C. Hull
- **Año:** 2021
- **Publicación o institución:** Pearson
- **Tipo de documento:** Manual de referencia
- **Temática:** TMX-05 Opciones de divisas: Garman-Kohlhagen, superficie de volatilidad, risk reversals y densidades implícitas (principal) · secundarias: TMX-03
- **Calidad Q:** 84 (A) — Tipo 20/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 9/10 · Acceso 5/10
- **DOI / ISBN / URL:** ISBN no visto · Cita de la 11.ª ed. en https://en.wikipedia.org/wiki/Short-rate_model
- **Acceso y licencia:** De pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Vasicek model Cox–Ingersoll–Ross model Heath–Jarrow–Morton framework affine term structure model yield curve (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Short-rate model», que reproduce la cita completa)
- **Contenido:** Manual de referencia de derivados: futuros, swaps, opciones, griegas, árboles, volatilidad y modelos de tipos.
- **Uso en el Motor:** MC-01 y MC-09: manual de referencia de forwards, futuros y opciones sobre divisas (paridad, Garman-Kohlhagen como Black-Scholes con rendimiento extranjero).
- **Limitaciones:** Manual de máster, no de investigación; ediciones anteriores circulan con numeración distinta.
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (tanda 2). Reutilizada en F8 Forex V1.0 (2026-11-02) desde F8 V3.2.

#### DOC-MOT-0330 · Q 84 (A) — Let's Be Rational

- **Autores:** Peter Jäckel
- **Año:** 2015
- **Publicación o institución:** Wilmott Magazine, vol. 2015, n.º 75, págs. 40-53
- **Tipo de documento:** Artículo en revista profesional
- **Temática:** TMX-05 Opciones de divisas: Garman-Kohlhagen, superficie de volatilidad, risk reversals y densidades implícitas (principal) · secundarias: —
- **Calidad Q:** 84 (A) — Tipo 15/25 · Rigor 18/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI: 10.1002/wilm.10395 · Implementación de referencia del autor: http://www.jaeckel.org
- **Acceso y licencia:** Revista de pago; código de referencia gratuito del autor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «VIX variance swap jump diffusion volatility risk premium implied volatility (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Implied volatility», que reproduce la cita completa)
- **Contenido:** Algoritmo para invertir Black-Scholes y obtener la volatilidad implícita a precisión de máquina en dos iteraciones.
- **Uso en el Motor:** MC-09: inversión rápida y exacta del precio a volatilidad implícita, aplicable a Garman-Kohlhagen con precios forward.
- **Limitaciones:** Revista profesional.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02. Reutilizada en F8 Forex V1.0 (2026-11-02) desde F8 V3.2.

#### FXM-0016 · Q 84 (A) — FX Options and Smile Risk

- **Autores:** Antonio Castagna
- **Año:** 2010
- **Publicación o institución:** John Wiley & Sons (Wiley Finance)
- **Tipo de documento:** Manual de referencia
- **Temática:** TMX-05 Opciones de divisas: Garman-Kohlhagen, superficie de volatilidad, risk reversals y densidades implícitas (principal) · secundarias: —
- **Calidad Q:** 84 (A) — Tipo 20/25 · Rigor 17/20 · Autoridad 13/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** Confirmada en la bibliografía de https://arxiv.org/pdf/2512.19621
- **Acceso y licencia:** Libro comercial
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Foreign exchange option Garman Kohlhagen vanna-volga Reiswich Wystup delta conventions wikipedia»; WebFetch: sí, sobre la página índice arXiv:2512.19621, que reproduce la cita)
- **Contenido:** Manual de mercado de opciones de divisas: convenciones de cotización, construcción de la sonrisa (incluido vanna-volga), riesgo de sonrisa y cobertura de libros de opciones.
- **Uso en el Motor:** MC-09: construcción de la superficie por delta y plazo y cálculo de griegas de sonrisa (vanna, volga).
- **Limitaciones:** Orientación de mesa; pendiente de lectura de la fuente primaria.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0077 · Q 84 (A) — A Guide to FX Options Quoting Conventions

- **Autores:** Dimitri Reiswich; Uwe Wystup
- **Año:** 2010
- **Publicación o institución:** The Journal of Derivatives, vol. 18, n.º 2, págs. 58-68
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-05 Opciones de divisas: Garman-Kohlhagen, superficie de volatilidad, risk reversals y densidades implícitas (principal) · secundarias: TMX-03
- **Calidad Q:** 84 (A) — Tipo 22/25 · Rigor 15/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** https://repository.uantwerpen.be/link/irua/123455
- **Acceso y licencia:** Revista por suscripción; registro en el repositorio de la Universidad de Amberes
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Reiswich Wystup "A guide to FX options quoting conventions" Journal of Derivatives»; WebFetch: sí, registro del repositorio de Amberes)
- **Contenido:** Explica las convenciones de cotización del mercado de opciones de divisas: deltas spot y forward, con y sin prima incluida, varias definiciones de ATM (forward, delta neutral) y sus implicaciones para la construcción de la sonrisa.
- **Uso en el Motor:** MC-01 y MC-09: conversión correcta entre deltas y strikes según la convención de cada par (p. ej., USD/JPY con prima incluida) antes de calibrar la sonrisa.
- **Limitaciones:** El registro del repositorio no muestra los autores; la atribución procede de los resultados de la búsqueda y de la obra afín de los mismos autores (CPQF WP 20).
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0076 · Q 83 (A) — Implied Risk-Neutral Probability Density Functions from Option Prices: Theory and Application

- **Autores:** Bhupinder Bahra
- **Año:** 1997
- **Publicación o institución:** Bank of England, Working Paper (1997)
- **Tipo de documento:** Documento de trabajo de institución reconocida
- **Temática:** TMX-05 Opciones de divisas: Garman-Kohlhagen, superficie de volatilidad, risk reversals y densidades implícitas (principal) · secundarias: —
- **Calidad Q:** 83 (A) — Tipo 20/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 7/10 · Impacto 8/10 · Independencia 9/10 · Acceso 9/10
- **DOI / ISBN / URL:** https://www.bankofengland.co.uk/-/media/boe/files/working-paper/1997/implied-risk-neutral-probability-density-functions-from-option-prices.pdf
- **Acceso y licencia:** Acceso abierto (Banco de Inglaterra)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Malz "A simple and reliable way to compute option-based risk-neutral distributions" Federal Reserve Bank of New York staff report»; WebFetch: sí; número de serie no visto)
- **Contenido:** Compara técnicas de extracción de densidades implícitas y recomienda la mezcla de dos lognormales; describe su aplicación a opciones de divisas con Garman-Kohlhagen (incluidas opciones cruzadas DM/GBP) y su uso para política monetaria.
- **Uso en el Motor:** MC-09: mezcla de lognormales para densidades bimodales de un par (eventos binarios, regímenes cambiarios).
- **Limitaciones:** Los ejemplos aplicados son sobre todo de tipos de interés.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0020 · Q 82 (A) — FX Volatility Smile Construction

- **Autores:** Dimitri Reiswich; Uwe Wystup
- **Año:** 2012 (versión de trabajo 2009)
- **Publicación o institución:** Wilmott, vol. 2012, n.º 60, págs. 58-69; versión de trabajo: CPQF Working Paper Series n.º 20, Frankfurt School of Finance & Management (2009)
- **Tipo de documento:** Artículo técnico con metodología (y documento de trabajo)
- **Temática:** TMX-05 Opciones de divisas: Garman-Kohlhagen, superficie de volatilidad, risk reversals y densidades implícitas (principal) · secundarias: —
- **Calidad Q:** 82 (A) — Tipo 17/25 · Rigor 17/20 · Autoridad 13/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 9/10 · Acceso 9/10
- **DOI / ISBN / URL:** https://econpapers.repec.org/RePEc:zbw:cpqfwp:20
- **Acceso y licencia:** Versión de trabajo en abierto (EconStor)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Foreign exchange option Garman Kohlhagen vanna-volga Reiswich Wystup delta conventions wikipedia»; WebFetch: sí, ficha EconPapers; versión Wilmott confirmada en la bibliografía de arXiv:2512.19621)
- **Contenido:** Describe las convenciones de cotización de la volatilidad en divisas (delta spot/forward, con o sin prima, ATM delta neutral, strangle de mercado frente a butterfly) y propone una fórmula eficiente y robusta para construir la sonrisa.
- **Uso en el Motor:** MC-09: algoritmo de construcción de la sonrisa a partir de ATM, RR y BF con la convención correcta de cada par.
- **Limitaciones:** Enfoque por vencimiento (no superficie completa).
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0022 · Q 82 (A) — The Vanna-Volga Method for Implied Volatilities

- **Autores:** Antonio Castagna; Fabio Mercurio
- **Año:** 2007
- **Publicación o institución:** Risk, enero de 2007, págs. 106-111
- **Tipo de documento:** Artículo técnico de revista profesional
- **Temática:** TMX-05 Opciones de divisas: Garman-Kohlhagen, superficie de volatilidad, risk reversals y densidades implícitas (principal) · secundarias: —
- **Calidad Q:** 82 (A) — Tipo 17/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** Confirmada en la bibliografía de https://mathfinance.com/wp-content/uploads/2024/10/wystup_vannavolga_eqf.pdf
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Foreign exchange option Garman Kohlhagen vanna-volga Reiswich Wystup delta conventions wikipedia»; WebFetch: sí, sobre la nota de Wystup en MathFinance, que reproduce la cita)
- **Contenido:** Formaliza el método vanna-volga: la sonrisa de un vencimiento se obtiene replicando vega, vanna y volga con tres opciones (25 delta put, ATM, 25 delta call) y da fórmulas cerradas aproximadas de la volatilidad implícita.
- **Uso en el Motor:** MC-09: interpolación y extrapolación de la sonrisa de divisas desde tres cotizaciones.
- **Limitaciones:** Extrapolación poco fiable en las alas; pendiente de lectura de la fuente primaria.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### DOC-MOT-0320 · Q 82 (A) — Pricing with a Smile

- **Autores:** Bruno Dupire
- **Año:** 1994
- **Publicación o institución:** Risk, vol. 7, n.º 1 (enero de 1994), Incisive Media
- **Tipo de documento:** Artículo en revista profesional
- **Temática:** TMX-05 Opciones de divisas: Garman-Kohlhagen, superficie de volatilidad, risk reversals y densidades implícitas (principal) · secundarias: —
- **Calidad Q:** 82 (A) — Tipo 15/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** Sin DOI · Cita en https://en.wikipedia.org/wiki/Bruno_Dupire y https://en.wikipedia.org/wiki/Local_volatility
- **Acceso y licencia:** Revista profesional de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «local volatility Dupire SABR volatility model volatility smile variance swap (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Bruno Dupire», que reproduce la cita completa y «Local volatility»)
- **Contenido:** Deriva la volatilidad local única consistente con la superficie de precios de opciones europeas (fórmula de Dupire).
- **Uso en el Motor:** MC-09: volatilidad local de Dupire, base de los modelos de volatilidad local y estocástica-local usados para exóticas de divisas.
- **Limitaciones:** Inestable con datos ruidosos; dinámica de sonrisa poco realista.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02. Reutilizada en F8 Forex V1.0 (2026-11-02) desde F8 V3.2.

#### FXM-0015 · Q 80 (A) — Counterexamples for FX Options Interpolations — Part I

- **Autores:** Jherek Healy
- **Año:** 2025
- **Publicación o institución:** arXiv:2512.19621 (22 de diciembre de 2025)
- **Tipo de documento:** Preprint técnico con metodología
- **Temática:** TMX-05 Opciones de divisas: Garman-Kohlhagen, superficie de volatilidad, risk reversals y densidades implícitas (principal) · secundarias: —
- **Calidad Q:** 80 (A) — Tipo 15/25 · Rigor 17/20 · Autoridad 11/15 · Vigencia 10/10 · Impacto 7/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://arxiv.org/pdf/2512.19621
- **Acceso y licencia:** Acceso abierto (arXiv)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Foreign exchange option Garman Kohlhagen vanna-volga Reiswich Wystup delta conventions wikipedia»; WebFetch: sí)
- **Contenido:** Cataloga casos en que los métodos habituales de interpolación de la sonrisa de divisas (vanna-volga, SABR, SVI, polinomios en delta) generan arbitraje o precios absurdos; útil como batería de pruebas de una superficie de volatilidad cambiaria.
- **Uso en el Motor:** MC-09 y MC-08: pruebas de no arbitraje de la superficie construida a partir de ATM, risk reversals y butterflies antes de extraer densidades.
- **Limitaciones:** Preprint sin revisión por pares; existe una parte II (arXiv:2512.19625).
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### DOC-MOT-0011 · Q 80 (A) — The Volatility Surface: A Practitioner's Guide

- **Autores:** Jim Gatheral
- **Año:** 2006
- **Publicación o institución:** John Wiley & Sons (Wiley Finance)
- **Tipo de documento:** Libro académico-profesional
- **Temática:** TMX-05 Opciones de divisas: Garman-Kohlhagen, superficie de volatilidad, risk reversals y densidades implícitas (principal) · secundarias: —
- **Calidad Q:** 80 (A) — Tipo 18/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 9/10 · Acceso 5/10
- **DOI / ISBN / URL:** ISBN: 978-0-471-79251-2 · Cita en https://en.wikipedia.org/wiki/Local_volatility
- **Acceso y licencia:** De pago (Wiley)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «local volatility Dupire SABR volatility model volatility smile variance swap (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Local volatility», que reproduce la cita completa y «Stochastic volatility»)
- **Contenido:** Guía práctica de la superficie de volatilidad: volatilidad local y estocástica, saltos, asintóticas de la sonrisa y calibración.
- **Uso en el Motor:** MC-09: manual de superficie de volatilidad (volatilidad local, estocástica, saltos) aplicado a la superficie de un par de divisas.
- **Limitaciones:** Orientado a la práctica; revisar modelos posteriores (volatilidad rugosa, SVI sin arbitraje).
- **Origen:** Ficha de carga V2.3 re-verificada por DOC-M el 2026-11-02 (tanda 2); se normaliza al formato del encargo. Reutilizada en F8 Forex V1.0 (2026-11-02) desde F8 V3.2.

#### FXM-0078 · Q 79 (B) — Pricing Formulae for Foreign Exchange Options

- **Autores:** Andreas Weber; Uwe Wystup
- **Año:** 2010
- **Publicación o institución:** Encyclopedia of Quantitative Finance (Wiley, Chichester), págs. 1408-1418; ISBN 978-0-470-05756-8
- **Tipo de documento:** Capítulo de obra de referencia
- **Temática:** TMX-05 Opciones de divisas: Garman-Kohlhagen, superficie de volatilidad, risk reversals y densidades implícitas (principal) · secundarias: —
- **Calidad Q:** 79 (B) — Tipo 20/25 · Rigor 15/20 · Autoridad 13/15 · Vigencia 9/10 · Impacto 6/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** https://repository.uantwerpen.be/link/irua/123465
- **Acceso y licencia:** Obra de referencia comercial; registro en el repositorio de la Universidad de Amberes
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Reiswich Wystup "A guide to FX options quoting conventions" Journal of Derivatives»; WebFetch: sí, registro del repositorio de Amberes)
- **Contenido:** Recopila las fórmulas cerradas de valoración de opciones de divisas (vainilla, digitales, barreras, touch) en el marco de Garman-Kohlhagen.
- **Uso en el Motor:** MC-09: biblioteca de fórmulas cerradas para verificar implementaciones (MC-08).
- **Limitaciones:** Nombre de pila del primer autor abreviado en el registro («A. Weber»).
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0019 · Q 78 (B) — Option-Implied Probability Distributions and Currency Excess Returns

- **Autores:** Allan M. Malz
- **Año:** 1997
- **Publicación o institución:** Federal Reserve Bank of New York, Staff Reports n.º 32; disponible también en SSRN n.º 943500
- **Tipo de documento:** Documento de trabajo de institución reconocida
- **Temática:** TMX-05 Opciones de divisas: Garman-Kohlhagen, superficie de volatilidad, risk reversals y densidades implícitas (principal) · secundarias: TMX-06
- **Calidad Q:** 78 (B) — Tipo 18/25 · Rigor 15/20 · Autoridad 13/15 · Vigencia 7/10 · Impacto 8/10 · Independencia 9/10 · Acceso 8/10
- **DOI / ISBN / URL:** https://ideas.repec.org/p/fip/fednsr/32.html
- **Acceso y licencia:** Acceso abierto (Fed de Nueva York, SSRN)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Foreign exchange option Garman Kohlhagen vanna-volga Reiswich Wystup delta conventions wikipedia»; WebFetch: sí, sobre la página índice arXiv:2512.19621; después, búsqueda «Malz "A simple and reliable way to compute option-based risk-neutral distributions"…» y WebFetch de la ficha IDEAS del Staff Report 32)
- **Contenido:** Construye la sonrisa a partir de ATM, risk reversal y strangle de 25 delta y extrae distribuciones implícitas de divisas; relaciona sus momentos (asimetría, curtosis) con los rendimientos en exceso de las divisas.
- **Uso en el Motor:** MC-09: interpolación cuadrática en delta y densidades implícitas desde las tres cotizaciones estándar; señal de risk reversals para TR-PFV.
- **Limitaciones:** Interpolación sencilla que puede generar arbitraje en las colas.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0024 · Q 74 (B) — Vanna-Volga Methods Applied to FX Derivatives: From Theory to Market Practice

- **Autores:** Frédéric Bossens; Grégory Rayée; Nikos S. Skantzos; Griselda Deelstra
- **Año:** 2009
- **Publicación o institución:** arXiv:0904.1074
- **Tipo de documento:** Preprint técnico con metodología
- **Temática:** TMX-05 Opciones de divisas: Garman-Kohlhagen, superficie de volatilidad, risk reversals y densidades implícitas (principal) · secundarias: —
- **Calidad Q:** 74 (B) — Tipo 15/25 · Rigor 16/20 · Autoridad 11/15 · Vigencia 8/10 · Impacto 6/10 · Independencia 9/10 · Acceso 9/10
- **DOI / ISBN / URL:** https://arxiv.org/pdf/0904.1074v1 · https://ar5iv.arxiv.org/html/0904.1074
- **Acceso y licencia:** Acceso abierto (arXiv)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Foreign exchange option Garman Kohlhagen vanna-volga Reiswich Wystup delta conventions wikipedia»; WebFetch: sí, versión ar5iv)
- **Contenido:** Revisa las variantes de mercado del método vanna-volga para opciones exóticas de divisas, las compara con modelos de volatilidad estocástica y local y analiza su calibración y sus fallos.
- **Uso en el Motor:** MC-09 y MC-08: elección y control de la variante vanna-volga aplicada a barreras de divisas.
- **Limitaciones:** Preprint; año inferido del identificador arXiv.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0023 · Q 70 (B) — Vanna-Volga Pricing (nota técnica)

- **Autores:** Uwe Wystup
- **Año:** 2008
- **Publicación o institución:** MathFinance AG (Waldems, Alemania), 30 de junio de 2008
- **Tipo de documento:** Informe técnico con metodología
- **Temática:** TMX-05 Opciones de divisas: Garman-Kohlhagen, superficie de volatilidad, risk reversals y densidades implícitas (principal) · secundarias: —
- **Calidad Q:** 70 (B) — Tipo 15/25 · Rigor 13/20 · Autoridad 13/15 · Vigencia 8/10 · Impacto 5/10 · Independencia 7/10 · Acceso 9/10
- **DOI / ISBN / URL:** https://mathfinance.com/wp-content/uploads/2024/10/wystup_vannavolga_eqf.pdf
- **Acceso y licencia:** Acceso abierto (MathFinance)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Foreign exchange option Garman Kohlhagen vanna-volga Reiswich Wystup delta conventions wikipedia»; WebFetch: sí)
- **Contenido:** Explica la regla de mercado vanna-volga para exóticas de divisas (ajuste por el coste de cubrir vanna y volga con ATM, risk reversal y butterfly) y sus limitaciones, incluido el factor de ajuste por probabilidad de supervivencia en barreras.
- **Uso en el Motor:** MC-09: ajuste vanna-volga de precios de barreras y digitales de divisas.
- **Limitaciones:** Nota de empresa (MathFinance, consultora); el método carece de fundamento teórico pleno.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0018 · Q 66 (B) — Using FX Volatility Skew to Assess the Implied Probability of Hard Brexit

- **Autores:** Iain J. Clark; Saeed Amen
- **Año:** 2018
- **Publicación o institución:** Wilmott, vol. 2018, n.º 95, págs. 64-69
- **Tipo de documento:** Artículo técnico de revista profesional
- **Temática:** TMX-05 Opciones de divisas: Garman-Kohlhagen, superficie de volatilidad, risk reversals y densidades implícitas (principal) · secundarias: TMX-07
- **Calidad Q:** 66 (B) — Tipo 15/25 · Rigor 13/20 · Autoridad 11/15 · Vigencia 8/10 · Impacto 5/10 · Independencia 9/10 · Acceso 5/10
- **DOI / ISBN / URL:** Confirmada en la bibliografía de https://arxiv.org/pdf/2512.19621
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Foreign exchange option Garman Kohlhagen vanna-volga Reiswich Wystup delta conventions wikipedia»; WebFetch: sí, sobre la página índice arXiv:2512.19621)
- **Contenido:** Usa la asimetría de la volatilidad de GBP/USD para extraer la probabilidad implícita de un escenario binario (Brexit duro) mediante una mezcla de distribuciones.
- **Uso en el Motor:** MC-09 y MC-05: probabilidad implícita de eventos binarios (referendos, elecciones, ruptura de tipos fijos) a partir de la sonrisa de un par.
- **Limitaciones:** Aplicación a un evento; pendiente de lectura de la fuente primaria.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

#### FXM-0025 · Q 55 (C) — The Vanna-Volga Method for Derivatives Pricing

- **Autores:** Agnieszka Janek
- **Año:** 2011
- **Publicación o institución:** MPRA Paper n.º 36127 (tesis de máster), Biblioteca Universitaria de Múnich
- **Tipo de documento:** Tesis de máster
- **Temática:** TMX-05 Opciones de divisas: Garman-Kohlhagen, superficie de volatilidad, risk reversals y densidades implícitas (principal) · secundarias: —
- **Calidad Q:** 55 (C) — Tipo 8/25 · Rigor 13/20 · Autoridad 6/15 · Vigencia 8/10 · Impacto 3/10 · Independencia 9/10 · Acceso 8/10
- **DOI / ISBN / URL:** https://mpra.ub.uni-muenchen.de/36127
- **Acceso y licencia:** Acceso abierto (MPRA)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Foreign exchange option Garman Kohlhagen vanna-volga Reiswich Wystup delta conventions wikipedia»; WebFetch: sí)
- **Contenido:** Deriva las fórmulas exacta y simplificada del vanna-volga para opciones vainilla de divisas, construye la superficie de volatilidad y compara su ajuste con el modelo de Heston y en barreras.
- **Uso en el Motor:** MC-09: material didáctico y casos de prueba de implementación del vanna-volga.
- **Limitaciones:** Tesis de máster sin revisión por pares; uso solo de apoyo, no para PS1.
- **Origen:** Alta nueva F8 Forex V1.0 (FXM), 2026-11-02.

## TMX-06 Factores cambiarios y construcción de carteras

#### FXM-0206 · Q 96 (A) — Volatility Risk Premia and Exchange Rate Predictability

- **Autores:** P. Della Corte; T. Ramadorai; L. Sarno
- **Año:** 2016
- **Publicación o institución:** Journal of Financial Economics, vol. 120, n.º 1, págs. 21-40
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-06 Factores cambiarios y construcción de carteras (principal) · secundarias: TMX-05
- **Calidad Q:** 96 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** DOI: 10.1016/j.jfineco.2016.02.015 · https://openaccess.city.ac.uk/id/eprint/13156/
- **Acceso y licencia:** Revista por suscripción; versión aceptada en City Research Online
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Della Corte Ramadorai Sarno "Volatility risk premia and exchange rate predictability" Journal of Financial Economics 2016»; WebFetch: sí, repositorio City)
- **Contenido:** Define la prima de riesgo de volatilidad cambiaria (volatilidad realizada esperada menos implícita libre de modelo) y construye una cartera que compra divisas con protección barata y vende las de protección cara; el rendimiento procede sobre todo del tipo spot.
- **Uso en el Motor:** MC-09 (PERF-FX-FACT): factor de prima de volatilidad cambiaria a partir de la superficie de opciones (TMX-05); TR-PFV y AS-ESTR.
- **Limitaciones:** Requiere datos de opciones de divisas fiables; universo limitado a pares con mercado de opciones líquido.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### DOC-MOT-0065 · Q 95 (A) — Value and Momentum Everywhere

- **Autores:** Clifford S. Asness; Tobias J. Moskowitz; Lasse Heje Pedersen
- **Año:** 2013
- **Publicación o institución:** The Journal of Finance, vol. 68, n.º 3, págs. 929-985
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-06 Factores cambiarios y construcción de carteras (principal) · secundarias: —
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1111/jofi.12021 · https://onlinelibrary.wiley.com/doi/abs/10.1111/jofi.12021 · Repositorio: https://research.cbs.dk/en/publications/9cef71a9-adf5-4d83-925d-53c571dd0691
- **Acceso y licencia:** Texto completo por suscripción en la editorial (Wiley); registro en repositorio CBS
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «momentum investing Jegadeesh Titman time series momentum carry trade betting against beta low-volatility anomaly (dominio en.wikipedia.org)»; WebFetch: sí, páginas índice de Wikipedia «Factor investing» y «Momentum investing»)
- **Contenido:** Construye de forma homogénea factores valor y momentum en ocho mercados/clases de activo y documenta su correlación negativa y estructura factorial común.
- **Uso en el Motor:** MC-09, MC-07 (PERF-FX-FACT): construcción homogénea de factores valor y momentum en divisas y su correlación negativa; AS-ESTR para combinar estilos cambiarios.
- **Limitaciones:** Costes de transacción no modelados en detalle.
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (tanda 2). Reutilizada de F8 general V3.2 (TM-07, mismo ID) para el Bloque A Forex el 2026-11-02.

#### DOC-MOT-0070 · Q 95 (A) — Optimal Versus Naive Diversification: How Inefficient Is the 1/N Portfolio Strategy?

- **Autores:** Victor DeMiguel; Lorenzo Garlappi; Raman Uppal
- **Año:** 2009
- **Publicación o institución:** The Review of Financial Studies, vol. 22, n.º 5, págs. 1915-1953
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-06 Factores cambiarios y construcción de carteras (principal) · secundarias: TMX-08
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1093/rfs/hhm075 · https://doi.org/10.1093/rfs/hhm075
- **Acceso y licencia:** Texto completo por suscripción en la editorial (OUP)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «modern portfolio theory Black–Litterman model risk parity momentum investing hierarchical risk parity (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Hierarchical Risk Parity», que reproduce la cita completa)
- **Contenido:** Compara 14 modelos de optimización con la cartera 1/N fuera de muestra: ninguno la supera de forma consistente por el error de estimación.
- **Uso en el Motor:** MC-07: referencia 1/N frente a carteras optimizadas de divisas; obliga a comparar toda cesta cambiaria optimizada con la cesta equiponderada fuera de muestra.
- **Limitaciones:** Universos de pocos activos; horizonte de estimación determinante.
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (tanda 2). Reutilizada de F8 general V3.2 (TM-07, mismo ID) para el Bloque A Forex el 2026-11-02.

#### DOC-MOT-0068 · Q 95 (A) — A Well-Conditioned Estimator for Large-Dimensional Covariance Matrices

- **Autores:** Olivier Ledoit; Michael Wolf
- **Año:** 2004
- **Publicación o institución:** Journal of Multivariate Analysis, vol. 88, n.º 2, págs. 365-411
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-06 Factores cambiarios y construcción de carteras (principal) · secundarias: —
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI no visto (se retira «10.1016/S0047-259X(03)00096-4 a verificar») · Copia del autor: http://www.econ.uzh.ch/faculty/wolf/publications/wellCond.pdf (archivada en https://web.archive.org/web/20141205062201/http://www.econ.uzh.ch/faculty/wolf/publications/wellCond.pdf)
- **Acceso y licencia:** Copia de autor gratuita (Universidad de Zúrich, archivada); editorial por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Ledoit Wolf shrinkage estimation of covariance matrices stationary bootstrap Politis Romano Fama–MacBeth regression (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Estimation of covariance matrices», que reproduce la cita completa)
- **Contenido:** Estimador de contracción lineal óptimo hacia la identidad escalada, bien condicionado aun cuando el número de variables supera al de observaciones.
- **Uso en el Motor:** MC-07: contracción de la matriz de covarianzas de rendimientos cambiarios (muchas divisas, historiales cortos en emergentes) antes de optimizar cestas de AS-ESTR.
- **Limitaciones:** Contracción lineal; superado en algunos usos por la contracción no lineal.
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (tanda 2). Reutilizada de F8 general V3.2 (TM-07, mismo ID) para el Bloque A Forex el 2026-11-02.

#### DOC-MOT-0338 · Q 95 (A) — A Test of the Efficiency of a Given Portfolio

- **Autores:** Michael R. Gibbons; Stephen A. Ross; Jay Shanken
- **Año:** 1989
- **Publicación o institución:** Econometrica, vol. 57, n.º 5, págs. 1121-1152
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-06 Factores cambiarios y construcción de carteras (principal) · secundarias: TMX-08
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.2307/1913625 · JSTOR: https://www.jstor.org/stable/1913625 · CiteSeerX: https://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.557.1995
- **Acceso y licencia:** Texto completo por suscripción en la editorial (Econometric Society/JSTOR)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Fama–French three-factor model capital asset pricing model Black–Litterman arbitrage pricing theory (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Fama–French three-factor model», que reproduce la cita completa)
- **Contenido:** Contraste GRS de muestra finita de que las alfas de un conjunto de carteras son conjuntamente cero respecto a unos factores.
- **Uso en el Motor:** MC-09, MC-10: contraste GRS de alfas conjuntas nulas de carteras cambiarias frente a los factores dólar y carry.
- **Limitaciones:** Supone normalidad.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02. Reutilizada de F8 general V3.2 (TM-07, mismo ID) para el Bloque A Forex el 2026-11-02.

#### DOC-MOT-0063 · Q 95 (A) — Risk, Return, and Equilibrium: Empirical Tests

- **Autores:** Eugene F. Fama; James D. MacBeth
- **Año:** 1973
- **Publicación o institución:** Journal of Political Economy, vol. 81, n.º 3, págs. 607-636
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-06 Factores cambiarios y construcción de carteras (principal) · secundarias: —
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1086/260061 · JSTOR: https://www.jstor.org/stable/1831028 · CiteSeerX: https://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.632.511
- **Acceso y licencia:** Texto completo por suscripción en la editorial (University of Chicago Press)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Ledoit Wolf shrinkage estimation of covariance matrices stationary bootstrap Politis Romano Fama–MacBeth regression (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Fama–MacBeth regression», que reproduce la cita completa)
- **Contenido:** Procedimiento en dos etapas: regresiones de sección cruzada periodo a periodo y promedio temporal de coeficientes para estimar primas de riesgo.
- **Uso en el Motor:** MC-09: regresiones de sección cruzada (Fama-MacBeth) para estimar precios de riesgo de los factores dólar y HML_FX en carteras de divisas.
- **Limitaciones:** Errores estándar sesgados con correlación persistente (véase Petersen 2009).
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (tanda 2). Reutilizada de F8 general V3.2 (TM-07, mismo ID) para el Bloque A Forex el 2026-11-02.

#### DOC-MOT-0066 · Q 94 (A) — Carry

- **Autores:** Ralph S. J. Koijen; Tobias J. Moskowitz; Lasse Heje Pedersen; Evert B. Vrugt
- **Año:** 2018
- **Publicación o institución:** Journal of Financial Economics, vol. 127, n.º 2, págs. 197-225 (versión previa: NBER Working Paper 19325, 2013)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-06 Factores cambiarios y construcción de carteras (principal) · secundarias: TMX-03
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 9/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI del documento de trabajo: 10.3386/w19325 (el DOI de la revista no se ha visto; se retira «10.1016/j.jfineco.2017.11.002 a verificar») · https://ideas.repec.org/a/eee/jfinec/v127y2018i2p197-225.html · https://www.nber.org/papers/w19325
- **Acceso y licencia:** NBER WP de libre acceso; revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Koijen Moskowitz Pedersen Vrugt "Carry" Journal of Financial Economics 2018 127»; WebFetch: sí, ficha IDEAS de R. Koijen y página NBER w19325)
- **Contenido:** Define el carry de forma unificada para cualquier activo (rentabilidad esperada si el precio no cambia) y lo estudia en divisas, bonos, materias primas, índices y opciones.
- **Uso en el Motor:** MC-09 (PERF-FX-FACT): definición unificada del carry cambiario (diferencial de tipos implícito en el forward) y comparación con el carry de otras clases; AS-ESTR para cestas de carry G10 y emergentes.
- **Limitaciones:** Carry sufre en crisis; definiciones dependen de la curva de futuros.
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (tanda 2). Reutilizada de F8 general V3.2 (TM-07, mismo ID) para el Bloque A Forex el 2026-11-02.

#### FXM-0204 · Q 94 (A) — The Share of Systematic Variation in Bilateral Exchange Rates

- **Autores:** Adrien Verdelhan
- **Año:** 2018
- **Publicación o institución:** The Journal of Finance, vol. 73, n.º 1, págs. 375-418 (versión previa: SED 2012 Meeting Papers 763)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-06 Factores cambiarios y construcción de carteras (principal) · secundarias: —
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1111/jofi.12587 · https://ideas.repec.org/a/bla/jfinan/v73y2018i1p375-418.html · Repositorio: https://dspace.mit.edu/handle/1721.1/122354
- **Acceso y licencia:** Revista por suscripción; copia en MIT DSpace
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Adrien Verdelhan "The Share of Systematic Variation in Bilateral Exchange Rates" Journal of Finance 2018»; WebFetch: sí, ficha IDEAS)
- **Contenido:** Ordena divisas por su beta frente al dólar y obtiene un factor de pendiente (dollar carry) ortogonal a HML_FX; los dos factores explican entre el 18 % y el 80 % de los movimientos mensuales de los tipos bilaterales.
- **Uso en el Motor:** MC-09: regresiones de tipos bilaterales sobre los factores dólar y carry para separar el componente sistemático del idiosincrásico; TR-PFV y AS-G10N para atribuir movimientos del par al dólar global.
- **Limitaciones:** Factores definidos desde la perspectiva del inversor en dólares; betas variables en el tiempo.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### FXM-0201 · Q 94 (A) — Carry Trades and Global Foreign Exchange Volatility

- **Autores:** Lukas Menkhoff; Lucio Sarno; Maik Schmeling; Andreas Schrimpf
- **Año:** 2012
- **Publicación o institución:** The Journal of Finance, vol. 67, n.º 2, págs. 681-718 (versión previa: CEPR Discussion Paper 8291)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-06 Factores cambiarios y construcción de carteras (principal) · secundarias: TMX-07
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** https://authors.repec.org/pro/pme67 (índice) · https://repec.cepr.org/repec/cpr/ceprdp/DP8291.pdf
- **Acceso y licencia:** Revista por suscripción; documento de trabajo CEPR en abierto
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Lukas Menkhoff IDEAS RePEc "Carry trades and global foreign exchange volatility" "Currency momentum strategies" "Currency value"»; WebFetch: sí, índice: perfil RePEc de L. Menkhoff, https://authors.repec.org/pro/pme67)
- **Contenido:** Construye un factor de innovaciones de la volatilidad cambiaria global y muestra que explica la sección cruzada de rentabilidades de carteras de carry: las divisas de alto tipo pierden cuando sube la volatilidad global.
- **Uso en el Motor:** MC-09, MC-07: factor de volatilidad global (VOL_FX) como riesgo del carry; TR-PFV para vincular el régimen de volatilidad con la fragilidad del carry en AS-ESTR.
- **Limitaciones:** Factor estimado sobre un panel concreto de divisas; el precio del riesgo puede variar con el régimen.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### FXM-0202 · Q 94 (A) — Currency Momentum Strategies

- **Autores:** Lukas Menkhoff; Lucio Sarno; Maik Schmeling; Andreas Schrimpf
- **Año:** 2012
- **Publicación o institución:** Journal of Financial Economics, vol. 106, n.º 3, págs. 660-684
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-06 Factores cambiarios y construcción de carteras (principal) · secundarias: TMX-08
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1016/j.jfineco.2012.06.009 · https://econpapers.repec.org/article/eeejfinec/v_3a106_3ay_3a2012_3ai_3a3_3ap_3a660-684.htm · Versión abierta: https://faculty.washington.edu/ss1110/IF/Sarno%20Currency%20Momentum%20JFE%20%281%29.pdf
- **Acceso y licencia:** Revista por suscripción; copia de trabajo accesible
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Lukas Menkhoff IDEAS RePEc "Carry trades and global foreign exchange volatility" "Currency momentum strategies" "Currency value"»; WebFetch: sí, ficha EconPapers)
- **Contenido:** Documenta un diferencial de hasta un 10 % anual entre divisas ganadoras y perdedoras; el momentum cambiario es distinto del carry, poco correlacionado con reglas técnicas clásicas y limitado por costes y límites al arbitraje.
- **Uso en el Motor:** MC-09 (PERF-FX-FACT): construcción del factor momentum cambiario (periodos de formación y tenencia) y su tratamiento de costes; AS-ESTR.
- **Limitaciones:** Parte del rendimiento desaparece con costes de transacción y se concentra en divisas menos líquidas.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### DOC-MOT-0119 · Q 94 (A) — Common Risk Factors in Currency Markets

- **Autores:** Hanno Lustig; Nikolai Roussanov; Adrien Verdelhan
- **Año:** 2011
- **Publicación o institución:** The Review of Financial Studies, vol. 24, n.º 11, págs. 3731-3777 (versión previa: NBER Working Paper 14082, 2008)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-06 Factores cambiarios y construcción de carteras (principal) · secundarias: —
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1093/rfs/hhr068 · https://ideas.repec.org/a/oup/rfinst/v24yi11p3731-3777.html · Versión abierta: https://dspace.mit.edu/bitstream/1721.1/66103/1/Verdelhan_Common%20Risk.pdf · https://papers.ssrn.com/abstract=1159046
- **Acceso y licencia:** Revista por suscripción; versiones de trabajo abiertas (MIT DSpace, NBER, SSRN)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Lustig Roussanov Verdelhan "Common Risk Factors in Currency Markets" "Countercyclical Currency Risk Premia" ideas.repec.org»; WebFetch: sí, ficha IDEAS)
- **Contenido:** Ordena divisas en carteras por tipo de interés y extrae dos factores: el factor dólar (nivel, media de todas las carteras) y HML_FX (pendiente, carry); HML_FX explica la mayor parte de la sección cruzada de excesos de rentabilidad y se asocia a la volatilidad bursátil global.
- **Uso en el Motor:** MC-09 (PERF-FX-FACT): construcción estándar de carteras por forward discount y de los factores DOL y HML_FX; AS-ESTR y TR-PFV para descomponer cualquier cesta en exposición al dólar y al carry.
- **Limitaciones:** Muestra 1983-2009 y universo de divisas del estudio; carteras sensibles a la inclusión de emergentes y a costes de transacción. Corrige la semilla V3.0 (antes PENDIENTE_VERIFICACION_ALTA en TM-13).
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### FXM-0203 · Q 93 (A) — Currency Value

- **Autores:** Lukas Menkhoff; Lucio Sarno; Maik Schmeling; Andreas Schrimpf
- **Año:** 2017
- **Publicación o institución:** The Review of Financial Studies, vol. 30, n.º 2, págs. 416-441
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-06 Factores cambiarios y construcción de carteras (principal) · secundarias: TMX-04
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** https://authors.repec.org/pro/pme67 (índice)
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Lukas Menkhoff IDEAS RePEc "Carry trades and global foreign exchange volatility" "Currency momentum strategies" "Currency value"»; WebFetch: sí, índice: perfil RePEc de L. Menkhoff, https://authors.repec.org/pro/pme67)
- **Contenido:** Construye estrategias de valor cambiario basadas en el tipo de cambio real ajustado por fundamentos y muestra que su rendimiento refleja en parte primas de riesgo y no solo reversión a la PPA.
- **Uso en el Motor:** MC-09: señal de valor cambiario (desviación del tipo real respecto a fundamentos) como factor de cartera; enlaza con los modelos de equilibrio de TMX-04 (AS-ESTR).
- **Limitaciones:** Horizonte de reversión largo; señal sensible a la definición del tipo real y de los fundamentos.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### FXM-0208 · Q 92 (A) — International Diversification Benefits with Foreign Exchange Investment Styles

- **Autores:** T. A. Kröncke (Kroencke); F. Schindler; A. Schrimpf
- **Año:** 2014
- **Publicación o institución:** Review of Finance, vol. 18, n.º 5, págs. 1847-1883
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-06 Factores cambiarios y construcción de carteras (principal) · secundarias: —
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI: 10.1093/rof/rft047 · https://edoc.unibas.ch/50918
- **Acceso y licencia:** Revista por suscripción; registro institucional (Universidad de Basilea)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Kroencke Schindler Schrimpf "International Diversification Benefits with Foreign Exchange Investment Styles" Review of Finance 2014»; WebFetch: sí, edoc.unibas.ch)
- **Contenido:** Gestiona la parte cambiaria de carteras internacionales con estilos carry, momentum y valor; un compuesto de estilos eleva el Sharpe fuera de muestra de una cartera global de 0,64 a 1,05 tras costes.
- **Uso en el Motor:** MC-07: diversificación de carteras con estilos cambiarios y comparación con la cobertura pasiva; AS-ESTR.
- **Limitaciones:** Resultados dependientes del periodo y de los costes supuestos.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### DOC-MOT-0343 · Q 92 (A) — Honey, I Shrunk the Sample Covariance Matrix

- **Autores:** Olivier Ledoit; Michael Wolf
- **Año:** 2004
- **Publicación o institución:** The Journal of Portfolio Management, vol. 30, n.º 4, págs. 110-119
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-06 Factores cambiarios y construcción de carteras (principal) · secundarias: —
- **Calidad Q:** 92 (A) — Tipo 22/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** Sin DOI visto · Copia del autor archivada: https://web.archive.org/web/20141205061842/http://www.econ.uzh.ch/faculty/ledoit/publications/honey.pdf
- **Acceso y licencia:** Copia gratuita archivada; revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Ledoit Wolf shrinkage estimation of covariance matrices stationary bootstrap Politis Romano Fama–MacBeth regression (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Estimation of covariance matrices», que reproduce la cita completa)
- **Contenido:** Contracción hacia la matriz de correlación constante para carteras de acciones, con fórmula de intensidad óptima.
- **Uso en el Motor:** MC-07: versión aplicada de la contracción de covarianzas; estimador por defecto para carteras de factores cambiarios de PERF-FX-FACT.
- **Limitaciones:** Objetivo de contracción específico.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02. Reutilizada de F8 general V3.2 (TM-07, mismo ID) para el Bloque A Forex el 2026-11-02.

#### DOC-MOT-0003 · Q 92 (A) — Portfolio Selection

- **Autores:** Harry M. Markowitz
- **Año:** 1952
- **Publicación o institución:** The Journal of Finance, vol. 7, n.º 1, págs. 77-91
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-06 Factores cambiarios y construcción de carteras (principal) · secundarias: —
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1111/j.1540-6261.1952.tb01525.x · JSTOR: 2975974 · https://doi.org/10.1111%2Fj.1540-6261.1952.tb01525.x
- **Acceso y licencia:** Texto completo por suscripción en la editorial (Wiley/JSTOR)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Fama–French three-factor model capital asset pricing model Black–Litterman arbitrage pricing theory (dominio en.wikipedia.org)» y «modern portfolio theory Black–Litterman model risk parity momentum investing hierarchical risk parity (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Capital asset pricing model», que reproduce la cita completa y «Modern portfolio theory»)
- **Contenido:** Formula la selección de carteras media-varianza y la frontera eficiente.
- **Uso en el Motor:** MC-07: base media-varianza para cestas cambiarias de AS-ESTR (siempre con covarianzas contraídas y referencia 1/N).
- **Limitaciones:** Sensibilidad extrema a errores en medias y covarianzas.
- **Origen:** Ficha de carga V2.3 re-verificada por DOC-M el 2026-11-02 (tanda 2); se normaliza al formato del encargo. Reutilizada de F8 general V3.2 (TM-07, mismo ID) para el Bloque A Forex el 2026-11-02.

#### FXM-0207 · Q 91 (A) — Beyond the Carry Trade: Optimal Currency Portfolios

- **Autores:** Pedro Barroso; Pedro Santa-Clara
- **Año:** 2015
- **Publicación o institución:** Journal of Financial and Quantitative Analysis, vol. 50, n.º 5, págs. 1037-1056
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-06 Factores cambiarios y construcción de carteras (principal) · secundarias: TMX-08
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** https://ideas.repec.org/a/cup/jfinqa/v50y2015i05p1037-1056_00.html · Repositorio: https://ore.exeter.ac.uk/repository/handle/10871/14068
- **Acceso y licencia:** Revista por suscripción; registro en repositorio de Exeter
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Barroso Santa-Clara "Beyond the Carry Trade: Optimal Currency Portfolios" Journal of Financial and Quantitative Analysis»; WebFetch: sí, ficha IDEAS)
- **Contenido:** Optimiza carteras de divisas con política paramétrica sobre características (carry, momentum, reversión del valor, tipo real, balanza corriente); carry, momentum y reversión aportan, la cuenta corriente y el tipo real no; la cartera óptima eleva el Sharpe de carteras globales.
- **Uso en el Motor:** MC-07, MC-09: carteras paramétricas de divisas sobre características (PERF-FX-FACT); AS-ESTR para cestas multiseñal.
- **Limitaciones:** Riesgo de sobreajuste en la selección de características; DOI no visto en la verificación.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### FXM-0205 · Q 91 (A) — Countercyclical Currency Risk Premia

- **Autores:** Hanno Lustig; Nikolai Roussanov; Adrien Verdelhan
- **Año:** 2010
- **Publicación o institución:** NBER Working Paper 16427 (septiembre de 2010)
- **Tipo de documento:** Documento de trabajo
- **Temática:** TMX-06 Factores cambiarios y construcción de carteras (principal) · secundarias: TMX-08
- **Calidad Q:** 91 (A) — Tipo 20/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://www.nber.org/system/files/working_papers/w16427/revisions/w16427.rev0.pdf
- **Acceso y licencia:** Acceso abierto (NBER)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Lustig Roussanov Verdelhan "Common Risk Factors in Currency Markets" "Countercyclical Currency Risk Premia" ideas.repec.org»; WebFetch: sí, PDF NBER)
- **Contenido:** Muestra que el forward discount medio del dólar frente a divisas desarrolladas predice el exceso de rentabilidad de una cesta frente al dólar (estrategia dollar carry), con primas que suben en recesiones de EE. UU.
- **Uso en el Motor:** MC-09: señal de carry del dólar (forward discount medio) y su componente cíclico; AS-ESTR para cestas de dólar amplio.
- **Limitaciones:** Se cita la versión de trabajo; la versión publicada no se ha verificado en esta tanda.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### FXM-0219 · Q 89 (A) — Currency Premia and Global Imbalances

- **Autores:** P. Della Corte; S. J. Riddiough; L. Sarno
- **Año:** 2016
- **Publicación o institución:** The Review of Financial Studies, vol. 29, n.º 8, págs. 2161-2193
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-06 Factores cambiarios y construcción de carteras (principal) · secundarias: TMX-04
- **Calidad Q:** 89 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** https://ideas.repec.org/a/eee/jfinec/v114y2014i2p197-225.html (índice)
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Lettau Maggiori Weber "Conditional risk premia in currency markets and other asset classes" ideas.repec.org»; WebFetch: sí, índice: ficha IDEAS de Lettau, Maggiori y Weber 2014, lista «Most related items», https://ideas.repec.org/a/eee/jfinec/v114y2014i2p197-225.html)
- **Contenido:** Construye un factor de desequilibrios globales (posición exterior neta y proporción de pasivos en moneda extranjera) que explica la sección cruzada de rentabilidades cambiarias junto al carry.
- **Uso en el Motor:** MC-09 (PERF-FX-FACT): factor de desequilibrios externos (IMB) para carteras de divisas; enlaza TR-BCM (balanza de pagos) con AS-ESTR.
- **Limitaciones:** Confirmada solo por índice; DOI no visto. Datos de posición exterior con retraso y revisiones.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### FXM-0225 · Q 88 (A) — The Risk in Hedge Fund Strategies: Theory and Evidence from Trend Followers

- **Autores:** W. Fung; D. A. Hsieh
- **Año:** 2001
- **Publicación o institución:** The Review of Financial Studies, vol. 14, págs. 313-341
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-06 Factores cambiarios y construcción de carteras (principal) · secundarias: TMX-08
- **Calidad Q:** 88 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 10/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** https://people.duke.edu/~dah7/vitae.htm (índice)
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Hsieh 1988 "The statistical properties of daily foreign exchange rates: 1974-1983" Journal of International Economics»; WebFetch: sí, índice: currículum de D. A. Hsieh, https://people.duke.edu/~dah7/vitae.htm)
- **Contenido:** Modela las rentabilidades de los seguidores de tendencia (incluidas divisas) como carteras de opciones lookback straddle, base de los factores de tendencia en divisas, bonos y materias primas.
- **Uso en el Motor:** MC-09, MC-07: factor de tendencia cambiaria (lookback straddles sobre divisas) para atribuir rentabilidades de estrategias de momentum/tendencia; AS-ESTR.
- **Limitaciones:** Confirmada solo por índice; DOI no visto. Enfoque multiactivo, no solo divisas.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### DOC-MOT-0067 · Q 88 (A) — Global Portfolio Optimization

- **Autores:** Fischer Black; Robert Litterman
- **Año:** 1992
- **Publicación o institución:** Financial Analysts Journal, vol. 48, n.º 5, págs. 28-43
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-06 Factores cambiarios y construcción de carteras (principal) · secundarias: —
- **Calidad Q:** 88 (A) — Tipo 24/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 9/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.2469/faj.v48.n5.28 · https://www.tandfonline.com/doi/abs/10.2469/faj.v48.n5.28
- **Acceso y licencia:** Texto completo por suscripción en la editorial (Taylor & Francis)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «modern portfolio theory Black–Litterman model risk parity momentum investing hierarchical risk parity (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Black–Litterman model», que reproduce la cita completa)
- **Contenido:** Combina rentabilidades de equilibrio implícitas con opiniones del inversor ponderadas por su confianza, produciendo carteras estables.
- **Uso en el Motor:** MC-07: optimización global con expectativas sobre activos y divisas (Black-Litterman con cobertura cambiaria); combina opiniones de AS-G10N/AS-G10M con el equilibrio.
- **Limitaciones:** Elección subjetiva de τ y de la confianza en opiniones.
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (tanda 2). Reutilizada de F8 general V3.2 (TM-07, mismo ID) para el Bloque A Forex el 2026-11-02.

#### DOC-MOT-0341 · Q 88 (A) — Asset Allocation: Combining Investor Views with Market Equilibrium

- **Autores:** Fischer Black; Robert B. Litterman
- **Año:** 1991
- **Publicación o institución:** The Journal of Fixed Income, vol. 1, n.º 2, págs. 7-18
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-06 Factores cambiarios y construcción de carteras (principal) · secundarias: —
- **Calidad Q:** 88 (A) — Tipo 24/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 9/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.3905/JFI.1991.408013 · https://www.pm-research.com/content/iijfixinc/1/2/7
- **Acceso y licencia:** Texto completo por suscripción en la editorial (PM Research)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «modern portfolio theory Black–Litterman model risk parity momentum investing hierarchical risk parity (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Black–Litterman model», que reproduce la cita completa)
- **Contenido:** Primera exposición del modelo Black-Litterman aplicado a asignación global de bonos y divisas.
- **Uso en el Motor:** MC-07: marco de combinación de opiniones y equilibrio aplicable a cestas cambiarias de AS-ESTR.
- **Limitaciones:** Exposición original menos detallada que 1992.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02. Reutilizada de F8 general V3.2 (TM-07, mismo ID) para el Bloque A Forex el 2026-11-02.

#### FXM-0216 · Q 87 (A) — The Cross-Section of Currency Volatility Premia

- **Autores:** Pasquale Della Corte; Roman Kozhan; Anthony Neuberger
- **Año:** 2021
- **Publicación o institución:** Journal of Financial Economics, vol. 139, n.º 3
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-06 Factores cambiarios y construcción de carteras (principal) · secundarias: TMX-05
- **Calidad Q:** 87 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 7/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** https://ideas.repec.org/a/eee/jfinec/v113y2014i3p325-347.html (índice)
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Jurek "Crash-neutral currency carry trades" Journal of Financial Economics 2014»; WebFetch: sí, índice: ficha IDEAS de Jurek 2014, lista «Most related», https://ideas.repec.org/a/eee/jfinec/v113y2014i3p325-347.html)
- **Contenido:** Estudia la sección cruzada de las primas de volatilidad de las divisas (diferencia entre volatilidad implícita y realizada) y su comportamiento como estrategia de cartera.
- **Uso en el Motor:** MC-09: estrategias de volatilidad cambiaria sobre varias divisas (ESTR, regla 3 de 2.6); TR-PFV.
- **Limitaciones:** Confirmada solo por índice; páginas y DOI no vistos.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### FXM-0220 · Q 86 (A) — Good Carry, Bad Carry

- **Autores:** G. Bekaert; G. Panayotov
- **Año:** 2020
- **Publicación o institución:** Journal of Financial and Quantitative Analysis, vol. 55, n.º 4
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-06 Factores cambiarios y construcción de carteras (principal) · secundarias: TMX-07
- **Calidad Q:** 86 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 6/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** https://ideas.repec.org/p/cpr/ceprdp/15305.html (índice)
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Filippou Rapach Taylor Zhou "Exchange rate prediction with machine learning and a smart carry portfolio"»; WebFetch: sí, índice: ficha IDEAS de CEPR DP 15305 (Filippou et al.), lista «Most related items», https://ideas.repec.org/p/cpr/ceprdp/15305.html)
- **Contenido:** Distingue carteras de carry «buenas» (mejor relación rentabilidad/asimetría) de «malas» según la composición de divisas, mostrando que excluir ciertas divisas mejora el perfil de riesgo del carry.
- **Uso en el Motor:** MC-07, MC-09: selección de divisas dentro de la cesta de carry atendiendo a la asimetría; AS-ESTR.
- **Limitaciones:** Confirmada solo por índice; páginas y DOI no vistos.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### FXM-0217 · Q 86 (A) — Properties of Foreign Exchange Risk Premiums

- **Autores:** Lucio Sarno; Paul Schneider; Christian Wagner
- **Año:** 2012
- **Publicación o institución:** Journal of Financial Economics, vol. 105, n.º 2
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-06 Factores cambiarios y construcción de carteras (principal) · secundarias: TMX-03
- **Calidad Q:** 86 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 7/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** https://ideas.repec.org/a/eee/jfinec/v113y2014i3p325-347.html (índice)
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Jurek "Crash-neutral currency carry trades" Journal of Financial Economics 2014»; WebFetch: sí, índice: ficha IDEAS de Jurek 2014, lista «Most related», https://ideas.repec.org/a/eee/jfinec/v113y2014i3p325-347.html)
- **Contenido:** Estima con un modelo afín las primas de riesgo cambiarias y caracteriza sus propiedades (variación temporal, relación con la paridad descubierta) en un panel de divisas.
- **Uso en el Motor:** MC-09: estimación de primas de riesgo cambiarias con modelos de estructura temporal; AS-ESTR.
- **Limitaciones:** Confirmada solo por índice; páginas y DOI no vistos.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### FXM-0222 · Q 83 (A) — Forward-Looking Policy Rules and Currency Premia

- **Autores:** Ilias Filippou; Mark P. Taylor
- **Año:** 2023
- **Publicación o institución:** Journal of Financial and Quantitative Analysis, vol. 58, n.º 1
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-06 Factores cambiarios y construcción de carteras (principal) · secundarias: TMX-04
- **Calidad Q:** 83 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 5/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** https://ideas.repec.org/p/cpr/ceprdp/15305.html (índice)
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Filippou Rapach Taylor Zhou "Exchange rate prediction with machine learning and a smart carry portfolio"»; WebFetch: sí, índice: ficha IDEAS de CEPR DP 15305 (Filippou et al.), lista «Most related items», https://ideas.repec.org/p/cpr/ceprdp/15305.html)
- **Contenido:** Construye estrategias cambiarias a partir de reglas de política monetaria prospectivas (diferenciales de tipos implícitos en reglas de Taylor) y estudia su prima.
- **Uso en el Motor:** MC-09: factor de reglas de política monetaria para cestas de divisas; puente entre TR-BCM (sendas de tipos) y AS-ESTR.
- **Limitaciones:** Confirmada solo por índice; páginas y DOI no vistos.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### FXM-0221 · Q 83 (A) — Dissecting Currency Momentum

- **Autores:** Zhang (nombre completo no visto en el índice)
- **Año:** 2022
- **Publicación o institución:** Journal of Financial Economics, vol. 144, n.º 1
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-06 Factores cambiarios y construcción de carteras (principal) · secundarias: —
- **Calidad Q:** 83 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 5/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** https://ideas.repec.org/p/cpr/ceprdp/15305.html (índice)
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Filippou Rapach Taylor Zhou "Exchange rate prediction with machine learning and a smart carry portfolio"»; WebFetch: sí, índice: ficha IDEAS de CEPR DP 15305 (Filippou et al.), lista «Most related items», https://ideas.repec.org/p/cpr/ceprdp/15305.html)
- **Contenido:** Descompone el momentum cambiario en sus fuentes (componentes de la rentabilidad pasada) para identificar qué parte genera la persistencia.
- **Uso en el Motor:** MC-09: refinamiento de la señal de momentum cambiario de PERF-FX-FACT; AS-ESTR.
- **Limitaciones:** Confirmada solo por índice; autoría completa, páginas y DOI no vistos: completar en el próximo barrido.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### FXM-0223 · Q 79 (B) — Cross-Sectional Return Dispersion and Currency Momentum

- **Autores:** J. N. Eriksen
- **Año:** 2019
- **Publicación o institución:** Journal of Empirical Finance, vol. 53, págs. 91-108
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-06 Factores cambiarios y construcción de carteras (principal) · secundarias: —
- **Calidad Q:** 79 (B) — Tipo 25/25 · Rigor 14/20 · Autoridad 12/15 · Vigencia 10/10 · Impacto 4/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** https://ideas.repec.org/a/eee/jfinec/v114y2014i2p197-225.html (índice)
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Lettau Maggiori Weber "Conditional risk premia in currency markets and other asset classes" ideas.repec.org»; WebFetch: sí, índice: ficha IDEAS de Lettau, Maggiori y Weber 2014, lista «Most related items», https://ideas.repec.org/a/eee/jfinec/v114y2014i2p197-225.html)
- **Contenido:** Relaciona la dispersión transversal de rentabilidades cambiarias con el rendimiento posterior del momentum de divisas (variable de estado para su gestión).
- **Uso en el Motor:** MC-09, MC-07: modulación de la exposición a momentum cambiario según la dispersión transversal; AS-ESTR.
- **Limitaciones:** Confirmada solo por índice; nombre de pila y DOI no vistos.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### FXM-0224 · Q 78 (B) — Common Information in Carry Trade Risk Factors

- **Autores:** J. P. Byrne; B. M. Ibrahim; R. Sakemoto
- **Año:** 2018
- **Publicación o institución:** Journal of International Financial Markets, Institutions and Money, vol. 52, págs. 37-47
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-06 Factores cambiarios y construcción de carteras (principal) · secundarias: —
- **Calidad Q:** 78 (B) — Tipo 25/25 · Rigor 13/20 · Autoridad 12/15 · Vigencia 10/10 · Impacto 4/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** https://ideas.repec.org/a/eee/jfinec/v114y2014i2p197-225.html (índice)
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Lettau Maggiori Weber "Conditional risk premia in currency markets and other asset classes" ideas.repec.org»; WebFetch: sí, índice: ficha IDEAS de Lettau, Maggiori y Weber 2014, lista «Most related items», https://ideas.repec.org/a/eee/jfinec/v114y2014i2p197-225.html)
- **Contenido:** Extrae la información común de los numerosos factores de riesgo propuestos para el carry y evalúa cuántos factores distintos son realmente necesarios.
- **Uso en el Motor:** MC-09: reducción de dimensión del «zoológico» de factores cambiarios antes de modelizar el carry; AS-ESTR.
- **Limitaciones:** Confirmada solo por índice; nombres de pila y DOI no vistos.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

## TMX-07 Riesgo de cola, saltos y valores extremos en divisas

#### DOC-MOT-0350 · Q 97 (A) — On the Coherence of Expected Shortfall

- **Autores:** Carlo Acerbi; Dirk Tasche
- **Año:** 2002
- **Publicación o institución:** Journal of Banking & Finance, vol. 26, n.º 7, págs. 1487-1503
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-07 Riesgo de cola, saltos y valores extremos en divisas (principal) · secundarias: —
- **Calidad Q:** 97 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** DOI: 10.1016/S0378-4266(02)00283-2 · arXiv: https://arxiv.org/abs/cond-mat/0104295
- **Acceso y licencia:** Preprint gratuito en arXiv; revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «expected shortfall coherent risk measure value at risk backtesting extreme value theory (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Expected shortfall», que reproduce la cita completa)
- **Contenido:** Define el ES de forma que sea coherente para cualquier distribución (incluidas discretas) y lo relaciona con el CVaR.
- **Uso en el Motor:** MC-07: justifica el uso del déficit esperado (ES) como medida de cola para el carry y las cestas cambiarias de PERF-FX-FACT.
- **Limitaciones:** Teórico.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02. Reutilizada de F8 general V3.2 (TM-08, mismo ID) para el Bloque A Forex el 2026-11-02.

#### DOC-MOT-0074 · Q 96 (A) — Estimation of Tail-Related Risk Measures for Heteroscedastic Financial Time Series: An Extreme Value Approach

- **Autores:** Alexander J. McNeil; Rüdiger Frey
- **Año:** 2000
- **Publicación o institución:** Journal of Empirical Finance, vol. 7, n.º 3-4, págs. 271-300
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-07 Riesgo de cola, saltos y valores extremos en divisas (principal) · secundarias: TMX-02
- **Calidad Q:** 96 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI: 10.1016/S0927-5398(00)00012-8 · https://research.wu.ac.at/de/publications/estimation-of-tail-related-risk-measures-for-heteroscedastic-fina-3/ · PDF: https://www.wu.ac.at/fileadmin/wu/d/i/statmath/Publications/Publications_Frey/Journal_Papers/evt-garch.pdf
- **Acceso y licencia:** Copia institucional gratuita (WU Viena); revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «McNeil Frey 2000 "Estimation of tail-related risk measures for heteroscedastic financial time series" Journal of Empirical Finance»; WebFetch: sí, portal de investigación de la WU)
- **Contenido:** Método en dos etapas: GARCH por pseudo-máxima verosimilitud y teoría de valores extremos (GPD) sobre los residuos para VaR y ES condicionales.
- **Uso en el Motor:** MC-07: VaR/ES condicional GARCH-EVT para rendimientos cambiarios diarios (pares G10 y emergentes con colas gruesas).
- **Limitaciones:** Supone residuos i.i.d.; umbral de la GPD a elegir.
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (tanda 2). Reutilizada de F8 general V3.2 (TM-08, mismo ID) para el Bloque A Forex el 2026-11-02.

#### DOC-MOT-0075 · Q 96 (A) — Coherent Measures of Risk

- **Autores:** Philippe Artzner; Freddy Delbaen; Jean-Marc Eber; David Heath
- **Año:** 1999
- **Publicación o institución:** Mathematical Finance, vol. 9, n.º 3, págs. 203-228
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-07 Riesgo de cola, saltos y valores extremos en divisas (principal) · secundarias: —
- **Calidad Q:** 96 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI: 10.1111/1467-9965.00068 · https://onlinelibrary.wiley.com/doi/10.1111/1467-9965.00068 · Preprint: http://www.math.ethz.ch/~delbaen/ftp/preprints/CoherentMF.pdf
- **Acceso y licencia:** Preprint gratuito (ETH Zúrich); revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «expected shortfall coherent risk measure value at risk backtesting extreme value theory (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Expected shortfall», que reproduce la cita completa, «Value at risk» y «Coherent risk measure»)
- **Contenido:** Axiomas de coherencia (monotonía, subaditividad, homogeneidad, invariancia por traslación); el VaR no es subaditivo en general.
- **Uso en el Motor:** MC-07: axiomas de coherencia que debe cumplir la medida de riesgo de cola aplicada a carteras de divisas.
- **Limitaciones:** Teoría estática; no trata elicitabilidad ni dinámica.
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (tanda 2). Reutilizada de F8 general V3.2 (TM-08, mismo ID) para el Bloque A Forex el 2026-11-02.

#### FXM-0209 · Q 95 (A) — The Carry Trade: Risks and Drawdowns

- **Autores:** Kent Daniel; Robert J. Hodrick; Zhongjin Lu
- **Año:** 2017
- **Publicación o institución:** Critical Finance Review, vol. 6, n.º 2, págs. 211-262 (versión previa: NBER Working Paper 20433, 2014)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-07 Riesgo de cola, saltos y valores extremos en divisas (principal) · secundarias: TMX-06
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** DOI: 10.1561/104.00000051 · https://ideas.repec.org/a/now/jnlcfr/104.00000051.html · https://www.nber.org/papers/w20433 · PDF: https://business.columbia.edu/sites/default/files-efs/pubfiles/6378/Daniel.Hodrick.Lu.Carry%20Trade.Critical%20Finance%20Review.2017.pdf
- **Acceso y licencia:** Versiones abiertas (Columbia, NBER)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Daniel Hodrick Lu "The Carry Trade: Risks and Drawdowns" Critical Finance Review 2017»; WebFetch: sí, ficha IDEAS)
- **Contenido:** Compara el carry G10 neutral al dólar (asimetría negativa y riesgo bajista) con el dollar carry diversificado (sin asimetría ni riesgo bajista) y estima distribuciones de máxima pérdida y drawdown con datos diarios.
- **Uso en el Motor:** MC-07: drawdown máximo, asimetría y riesgo bajista de variantes de carry; AS-ESTR y CONTRA para la fragilidad del carry.
- **Limitaciones:** Universo G10; resultados sensibles a la construcción de la cartera.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### FXM-0230 · Q 95 (A) — Rare Disasters and Exchange Rates

- **Autores:** E. Farhi; X. Gabaix
- **Año:** 2016
- **Publicación o institución:** The Quarterly Journal of Economics, vol. 131, n.º 1, págs. 1-52 (NBER Working Paper 13805)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-07 Riesgo de cola, saltos y valores extremos en divisas (principal) · secundarias: TMX-06
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** https://xgabaix.scholars.harvard.edu/publications/rare-disasters-and-exchange-rates · https://ideas.repec.org/a/oup/qjecon/v131y2016i1p1-52..html · https://www.nber.org/papers/w13805
- **Acceso y licencia:** Revista por suscripción; versión del autor y NBER en abierto
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Farhi Gabaix "Rare Disasters and Exchange Rates" Quarterly Journal of Economics 2016»; WebFetch: sí, página del autor (Harvard))
- **Contenido:** Modelo de desastres raros con resiliencia variable por país que explica conjuntamente la prima forward, la asimetría de las opciones cambiarias y la relación con la bolsa.
- **Uso en el Motor:** MC-05, MC-07: marco teórico para simular desastres y su traslación a divisas de refugio y de alto rendimiento; AS-ESTR.
- **Limitaciones:** Modelo estilizado; calibración de la probabilidad de desastre difícil.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### FXM-0231 · Q 95 (A) — Conditional Risk Premia in Currency Markets and Other Asset Classes

- **Autores:** Martin Lettau; Matteo Maggiori; Michael Weber
- **Año:** 2014
- **Publicación o institución:** Journal of Financial Economics, vol. 114, n.º 2, págs. 197-225 (NBER Working Paper 18844)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-07 Riesgo de cola, saltos y valores extremos en divisas (principal) · secundarias: TMX-06
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI: 10.1016/j.jfineco.2014.07.001 · https://ideas.repec.org/a/eee/jfinec/v114y2014i2p197-225.html · https://nber.org/papers/18844
- **Acceso y licencia:** Revista por suscripción; NBER WP en abierto
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Lettau Maggiori Weber "Conditional risk premia in currency markets and other asset classes" ideas.repec.org»; WebFetch: sí, ficha IDEAS)
- **Contenido:** Propone el CAPM de riesgo bajista (DR-CAPM): la beta de mercado de las divisas de alto tipo aumenta en malos momentos bursátiles, lo que explica la sección cruzada del carry y de otras clases de activos.
- **Uso en el Motor:** MC-07, MC-09: beta bajista de carteras de divisas como medida de riesgo de cola del carry; AS-ESTR.
- **Limitaciones:** Resultados dependientes de la elección del umbral bajista.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### FXM-0229 · Q 95 (A) — Do Peso Problems Explain the Returns to the Carry Trade?

- **Autores:** C. Burnside; M. Eichenbaum; I. Kleshchelski; S. Rebelo
- **Año:** 2011
- **Publicación o institución:** The Review of Financial Studies, vol. 24, n.º 3, págs. 853-891 (NBER Working Paper 14054)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-07 Riesgo de cola, saltos y valores extremos en divisas (principal) · secundarias: TMX-06
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI: 10.1093/rfs/hhq138 · https://eprints.gla.ac.uk/59358 · https://dukespace.lib.duke.edu/items/245f5a49-ab66-45ab-8a6d-64b1c5054374
- **Acceso y licencia:** Revista por suscripción; registros en repositorios de Glasgow y Duke
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Burnside Eichenbaum Kleshchelski Rebelo "Do Peso Problems Explain the Returns to the Carry Trade?" Review of Financial Studies»; WebFetch: sí, eprints de Glasgow)
- **Contenido:** Usa carteras de carry cubiertas con opciones para mostrar que la rentabilidad del carry refleja un problema peso: un evento raro que se manifiesta como valores altos del factor de descuento estocástico más que como pérdidas enormes.
- **Uso en el Motor:** MC-07: interpretación y medición del problema peso en el carry; contraste con carry cubierto con opciones (AS-ESTR, CONTRA).
- **Limitaciones:** Conclusión sensible a la especificación del factor de descuento.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### FXM-0211 · Q 95 (A) — Carry Trades and Currency Crashes

- **Autores:** M. K. Brunnermeier; S. Nagel; L. H. Pedersen
- **Año:** 2008
- **Publicación o institución:** NBER Macroeconomics Annual, vol. 23, págs. 313-347 (NBER Working Paper 14473)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-07 Riesgo de cola, saltos y valores extremos en divisas (principal) · secundarias: TMX-06
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 10/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** DOI: 10.1086/593088 · https://collaborate.princeton.edu/en/publications/carry-trades-and-currency-crashes/ · https://www.nber.org/papers/w14473
- **Acceso y licencia:** Documento de trabajo NBER en abierto
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Brunnermeier Nagel Pedersen "Carry Trades and Currency Crashes" NBER Macroeconomics Annual 2008»; WebFetch: sí, portal Princeton)
- **Contenido:** Muestra que el carry tiene asimetría negativa (crash risk) por deshacimientos súbitos ligados a la liquidez de financiación y al apetito de riesgo; tras las pérdidas cae el riesgo de crash pero sube el precio de la protección (risk reversals).
- **Uso en el Motor:** MC-07: asimetría y risk reversals como medidas de riesgo de crash del carry; TR-PFV (posicionamiento y liquidez) y CONTRA.
- **Limitaciones:** Muestra anterior a la crisis de 2008; medidas de liquidez específicas de EE. UU.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### DOC-MOT-0358 · Q 95 (A) — Statistical Inference Using Extreme Order Statistics

- **Autores:** James Pickands III
- **Año:** 1975
- **Publicación o institución:** The Annals of Statistics, vol. 3, n.º 1, págs. 119-131
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-07 Riesgo de cola, saltos y valores extremos en divisas (principal) · secundarias: —
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** DOI: 10.1214/aos/1176343003 · https://projecteuclid.org/journals/annals-of-statistics/volume-3/issue-1/Statistical-Inference-Using-Extreme-Order-Statistics/10.1214/aos/1176343003.full
- **Acceso y licencia:** Acceso gratuito en Project Euclid
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «generalized Pareto distribution extreme value theory Hill estimator copula CoVaR systemic risk (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Pickands–Balkema–De Haan theorem», que reproduce la cita completa y «Extreme value theory»)
- **Contenido:** Establece que los excesos sobre umbrales altos siguen aproximadamente una distribución de Pareto generalizada y propone el estimador de Pickands.
- **Uso en el Motor:** MC-07: estimador de Hill del índice de cola de rendimientos cambiarios (comparación entre pares y regímenes).
- **Limitaciones:** Estimador de Pickands de alta varianza.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02. Reutilizada de F8 general V3.2 (TM-08, mismo ID) para el Bloque A Forex el 2026-11-02.

#### FXM-0212 · Q 94 (A) — Crash-Neutral Currency Carry Trades

- **Autores:** Jakub W. Jurek
- **Año:** 2014
- **Publicación o institución:** Journal of Financial Economics, vol. 113, n.º 3, págs. 325-347
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-07 Riesgo de cola, saltos y valores extremos en divisas (principal) · secundarias: TMX-05
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1016/j.jfineco.2014.05.004 · https://ideas.repec.org/a/eee/jfinec/v113y2014i3p325-347.html · Repositorio: https://repository.upenn.edu/handle/20.500.14332/34466
- **Acceso y licencia:** Revista por suscripción; copia en repositorio de la Universidad de Pensilvania
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Jurek "Crash-neutral currency carry trades" Journal of Financial Economics 2014»; WebFetch: sí, ficha IDEAS)
- **Contenido:** Construye carry G10 cubierto contra crashes con opciones fuera de dinero y concluye que las primas de crash explican como máximo un tercio del exceso de rentabilidad del carry (1990-2012); los resultados no se deben a problemas peso.
- **Uso en el Motor:** MC-07, MC-09: valoración de la cobertura de cola del carry con opciones y descomposición de la prima de crash; AS-ESTR.
- **Limitaciones:** Solo G10 con opciones líquidas; coste de cobertura sensible a la elección de strikes.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### DOC-MOT-0365 · Q 94 (A) — Asset Market Linkages in Crisis Periods

- **Autores:** Philipp Hartmann; Stefan Straetmans; Casper G. de Vries
- **Año:** 2004
- **Publicación o institución:** Review of Economics and Statistics, vol. 86, n.º 1, págs. 313-326
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-07 Riesgo de cola, saltos y valores extremos en divisas (principal) · secundarias: —
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI: 10.1162/003465304323023831 · Repositorio: http://repository.tue.nl/548705 · https://hdl.handle.net/10419%2F152505
- **Acceso y licencia:** Copias gratuitas (TU Eindhoven, EconStor); revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «generalized Pareto distribution extreme value theory Hill estimator copula CoVaR systemic risk (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Tail dependence», que reproduce la cita completa)
- **Contenido:** Mide la dependencia de colas entre acciones y bonos del G-5 con EVT multivariante: contagio y huida hacia la calidad.
- **Uso en el Motor:** MC-07: dependencia extrema entre mercados en crisis; base para medir el contagio en colas entre divisas emergentes (AS-EMLA, AS-EMEA, AS-EMAS).
- **Limitaciones:** Muestra hasta finales de los 90.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02. Reutilizada de F8 general V3.2 (TM-08, mismo ID) para el Bloque A Forex el 2026-11-02.

#### DOC-MOT-0073 · Q 94 (A) — Evaluating Interval Forecasts

- **Autores:** Peter F. Christoffersen
- **Año:** 1998
- **Publicación o institución:** International Economic Review, vol. 39, n.º 4, págs. 841-862
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-07 Riesgo de cola, saltos y valores extremos en divisas (principal) · secundarias: TMX-08
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.2307/2527341 · JSTOR: 2527341
- **Acceso y licencia:** Texto completo por suscripción en la editorial (Wiley/JSTOR)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «expected shortfall coherent risk measure value at risk backtesting extreme value theory (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Value at risk», que reproduce la cita completa)
- **Contenido:** Contrastes de razón de verosimilitud de cobertura incondicional, independencia y cobertura condicional de las excepciones de intervalos/VaR.
- **Uso en el Motor:** MC-07, MC-10: contraste de cobertura condicional de intervalos/VaR de rendimientos cambiarios.
- **Limitaciones:** Baja potencia con pocas excepciones.
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (tanda 2). Reutilizada de F8 general V3.2 (TM-08, mismo ID) para el Bloque A Forex el 2026-11-02.

#### DOC-MOT-0352 · Q 93 (A) — Backtesting Value-at-Risk: A Duration-Based Approach

- **Autores:** Peter Christoffersen; Denis Pelletier
- **Año:** 2004
- **Publicación o institución:** Journal of Financial Econometrics, vol. 2, págs. 84-108
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-07 Riesgo de cola, saltos y valores extremos en divisas (principal) · secundarias: TMX-08
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1093/jjfinec/nbh004
- **Acceso y licencia:** Texto completo por suscripción en la editorial (OUP)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «expected shortfall coherent risk measure value at risk backtesting extreme value theory (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Value at risk», que reproduce la cita completa)
- **Contenido:** Contrastes de independencia de excepciones basados en la duración entre violaciones del VaR, más potentes ante agrupamientos.
- **Uso en el Motor:** MC-07, MC-10: contraste de duración entre violaciones del VaR en series cambiarias con agrupamiento de volatilidad.
- **Limitaciones:** Potencia limitada en muestras cortas.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02. Reutilizada de F8 general V3.2 (TM-08, mismo ID) para el Bloque A Forex el 2026-11-02.

#### DOC-MOT-0363 · Q 93 (A) — Models for Exceedances over High Thresholds

- **Autores:** A. C. Davison; R. L. Smith
- **Año:** 1990
- **Publicación o institución:** Journal of the Royal Statistical Society, Series B, vol. 52, n.º 3, págs. 393-425
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-07 Riesgo de cola, saltos y valores extremos en divisas (principal) · secundarias: —
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1111/j.2517-6161.1990.tb01796.x · https://rss.onlinelibrary.wiley.com/doi/10.1111/j.2517-6161.1990.tb01796.x
- **Acceso y licencia:** Texto completo por suscripción en la editorial (Wiley/RSS)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «generalized Pareto distribution extreme value theory Hill estimator copula CoVaR systemic risk (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Extreme value theory», que reproduce la cita completa)
- **Contenido:** Desarrolla el método de picos sobre umbral (POT) con GPD, regresión y diagnósticos.
- **Uso en el Motor:** MC-07, MC-05: excesos sobre umbral (GPD) para modelar grandes depreciaciones y desplomes del carry.
- **Limitaciones:** Datos no financieros.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02. Reutilizada de F8 general V3.2 (TM-08, mismo ID) para el Bloque A Forex el 2026-11-02.

#### FXM-0227 · Q 92 (A) — Crash Risk in Currency Returns

- **Autores:** M. Chernov; J. Graveline; I. Zviadadze
- **Año:** 2018
- **Publicación o institución:** Journal of Financial and Quantitative Analysis, vol. 53, n.º 1, págs. 137-170
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-07 Riesgo de cola, saltos y valores extremos en divisas (principal) · secundarias: TMX-02
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 7/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** https://www.cambridge.org/core/product/9141836509BC03A5AEE293D19CAFD8AB · Versión de trabajo: https://repec.cepr.org/repec/cpr/ceprdp/DP8745.pdf
- **Acceso y licencia:** Revista por suscripción; versión de trabajo CEPR («Sources of Risk in Currency Returns»)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Chernov Graveline Zviadadze "Crash Risk in Currency Returns" Journal of Financial and Quantitative Analysis 2018 jumps»; WebFetch: sí, página de Cambridge Core)
- **Contenido:** Modelo empírico de tipos bilaterales con volatilidad estocástica y saltos en el tipo y en la varianza; la intensidad de los saltos depende de los tipos de interés, los saltos del tipo coinciden con anuncios programados y explican cerca de un cuarto del riesgo cambiario.
- **Uso en el Motor:** MC-05, MC-07: especificación de saltos dependientes del diferencial de tipos para simular colas del carry y de pares individuales; TR-BCM (anuncios).
- **Limitaciones:** Estimación compleja (filtrado de saltos); la página leída no listaba autores ni DOI (autores confirmados por la búsqueda).
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### FXM-0226 · Q 91 (A) — Crash Risk in Currency Markets

- **Autores:** Emmanuel Farhi; Samuel Paul Fraiberger; Xavier Gabaix; Romain Ranciere; Adrien Verdelhan
- **Año:** 2009
- **Publicación o institución:** NBER Working Paper 15062 (junio de 2009; revisado en mayo de 2013)
- **Tipo de documento:** Documento de trabajo
- **Temática:** TMX-07 Riesgo de cola, saltos y valores extremos en divisas (principal) · secundarias: TMX-05
- **Calidad Q:** 91 (A) — Tipo 20/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** DOI: 10.3386/w15062 · https://www.nber.org/papers/w15062
- **Acceso y licencia:** Acceso abierto (NBER)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Farhi Fraiberger Gabaix Ranciere Verdelhan "Crash Risk in Currency Markets" NBER»; WebFetch: sí, página NBER)
- **Contenido:** Modelo estructural con riesgo normal y de desastre estimable con opciones fuera de dinero, spot y forward (1996-2011); construye un índice en tiempo real de primas de desastre y atribuye a ese riesgo más de un tercio de las primas cambiarias en economías avanzadas.
- **Uso en el Motor:** MC-07, MC-05: extracción de la prima de desastre del carry desde la superficie de opciones (risk reversals); TR-PFV y CONTRA.
- **Limitaciones:** Documento de trabajo; depende de la calidad de los datos de opciones fuera de dinero.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### DOC-MOT-0360 · Q 91 (A) — A Simple General Approach to Inference about the Tail of a Distribution

- **Autores:** Bruce M. Hill
- **Año:** 1975
- **Publicación o institución:** The Annals of Statistics, vol. 3, págs. 1163-1174
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-07 Riesgo de cola, saltos y valores extremos en divisas (principal) · secundarias: —
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** DOI no visto · Cita en https://en.wikipedia.org/wiki/Heavy-tailed_distribution
- **Acceso y licencia:** No determinado (no se ha localizado copia ni página editorial en esta pasada)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «generalized Pareto distribution extreme value theory Hill estimator copula CoVaR systemic risk (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Heavy-tailed distribution», que reproduce la cita completa)
- **Contenido:** Estimador de Hill del índice de cola para distribuciones de tipo Pareto a partir de los estadísticos de orden superiores.
- **Uso en el Motor:** MC-07: inferencia sobre la cola (Pickands) como contraste de robustez del índice de cola cambiario.
- **Limitaciones:** Sensible al número de estadísticos de orden. Alerta: REPARAR (localizar DOI/URL).
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02. Reutilizada de F8 general V3.2 (TM-08, mismo ID) para el Bloque A Forex el 2026-11-02.

#### DOC-MOT-0077 · Q 89 (A) — Quantitative Risk Management: Concepts, Techniques and Tools (ed. revisada)

- **Autores:** Alexander J. McNeil; Rüdiger Frey; Paul Embrechts
- **Año:** 2015
- **Publicación o institución:** Princeton University Press (Princeton Series in Finance)
- **Tipo de documento:** Manual de referencia
- **Temática:** TMX-07 Riesgo de cola, saltos y valores extremos en divisas (principal) · secundarias: —
- **Calidad Q:** 89 (A) — Tipo 20/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** ISBN: 978-0-691-16627-8 · https://econpapers.repec.org/RePEc:pup:chapts:10496-1
- **Acceso y licencia:** De pago; capítulos introductorios con ficha en RePEc
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «McNeil Frey Embrechts "Quantitative Risk Management" revised edition 2015 Princeton University Press»; WebFetch: sí, ficha EconPapers del prefacio)
- **Contenido:** Manual integral de riesgo cuantitativo: medidas de riesgo, modelos de series, valores extremos, cópulas, riesgo de crédito y operacional, backtesting.
- **Uso en el Motor:** MC-07: manual de gestión cuantitativa del riesgo (VaR, ES, EVT, cópulas) aplicable a carteras cambiarias.
- **Limitaciones:** Extenso; requiere base de probabilidad.
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (tanda 2). Reutilizada de F8 general V3.2 (TM-08, mismo ID) para el Bloque A Forex el 2026-11-02.

#### DOC-MOT-0362 · Q 88 (A) — An Introduction to Statistical Modeling of Extreme Values

- **Autores:** Stuart Coles
- **Año:** 2001
- **Publicación o institución:** Springer (Springer Series in Statistics)
- **Tipo de documento:** Manual de referencia
- **Temática:** TMX-07 Riesgo de cola, saltos y valores extremos en divisas (principal) · secundarias: —
- **Calidad Q:** 88 (A) — Tipo 20/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.1007/978-1-4471-3675-0 · ISBN: 978-1-84996-874-4
- **Acceso y licencia:** De pago (Springer)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «generalized Pareto distribution extreme value theory Hill estimator copula CoVaR systemic risk (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Extreme value theory», que reproduce la cita completa)
- **Contenido:** Manual aplicado de valores extremos: GEV, GPD/POT, procesos puntuales, no estacionariedad y extremos multivariantes, con inferencia por verosimilitud.
- **Uso en el Motor:** MC-07: manual de referencia de valores extremos (bloques máximos, GPD, niveles de retorno) aplicado a movimientos cambiarios extremos.
- **Limitaciones:** Ejemplos ambientales más que financieros.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02. Reutilizada de F8 general V3.2 (TM-08, mismo ID) para el Bloque A Forex el 2026-11-02.

#### DOC-MOT-0078 · Q 87 (A) — Modelling Extremal Events for Insurance and Finance

- **Autores:** Paul Embrechts; Claudia Klüppelberg; Thomas Mikosch
- **Año:** 1997
- **Publicación o institución:** Springer (Stochastic Modelling and Applied Probability, vol. 33)
- **Tipo de documento:** Libro académico
- **Temática:** TMX-07 Riesgo de cola, saltos y valores extremos en divisas (principal) · secundarias: —
- **Calidad Q:** 87 (A) — Tipo 20/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.1007/978-3-642-33483-2 · ISBN: 978-3-642-08242-9 · Cita en https://en.wikipedia.org/wiki/Heavy-tailed_distribution
- **Acceso y licencia:** De pago (Springer)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «generalized Pareto distribution extreme value theory Hill estimator copula CoVaR systemic risk (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Heavy-tailed distribution», que reproduce la cita completa y «Extreme value theory»)
- **Contenido:** Tratado de valores extremos: GEV, GPD, estimadores de cola (Hill), distribuciones subexponenciales y aplicaciones actuariales y financieras.
- **Uso en el Motor:** MC-07: fundamentos teóricos de eventos extremales para colas de tipos de cambio y rupturas de tipos fijos.
- **Limitaciones:** Alto nivel matemático.
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (tanda 2). Reutilizada de F8 general V3.2 (TM-08, mismo ID) para el Bloque A Forex el 2026-11-02.

#### FXM-0215 · Q 86 (A) — Equity Tail Risk and Currency Risk Premiums

- **Autores:** Zhenzhen Fan; Juan M. Londono; Xiao Xiao
- **Año:** 2022
- **Publicación o institución:** Journal of Financial Economics, vol. 143, n.º 1, págs. 484-503
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-07 Riesgo de cola, saltos y valores extremos en divisas (principal) · secundarias: TMX-06
- **Calidad Q:** 86 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 6/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** https://ideas.repec.org/a/eee/jfinec/v113y2014i3p325-347.html (índice) · https://ideas.repec.org/a/eee/jfinec/v114y2014i2p197-225.html (índice)
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Jurek "Crash-neutral currency carry trades" Journal of Financial Economics 2014»; WebFetch: sí, índice: ficha IDEAS de Jurek 2014, lista «Most related», https://ideas.repec.org/a/eee/jfinec/v113y2014i3p325-347.html)
- **Contenido:** Relaciona el riesgo de cola de la renta variable con las primas de riesgo cambiarias: la exposición de las divisas a la cola bursátil ayuda a explicar sus excesos de rentabilidad.
- **Uso en el Motor:** MC-07, MC-09: beta de las divisas frente a la cola bursátil global como factor de riesgo; TR-PFV.
- **Limitaciones:** Confirmada solo por índices (IDEAS de Jurek 2014 y de Lettau, Maggiori y Weber 2014); DOI no visto.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### FXM-0213 · Q 86 (A) — Carry Trade and Systemic Risk: Why are FX Options so Cheap?

- **Autores:** Ricardo J. Caballero; Joseph B. Doyle
- **Año:** 2012
- **Publicación o institución:** NBER Working Paper 18644
- **Tipo de documento:** Documento de trabajo
- **Temática:** TMX-07 Riesgo de cola, saltos y valores extremos en divisas (principal) · secundarias: TMX-05
- **Calidad Q:** 86 (A) — Tipo 20/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 7/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://ideas.repec.org/p/nbr/nberwo/18644.html · http://www.nber.org/papers/w18644.pdf
- **Acceso y licencia:** Acceso abierto (NBER)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Jurek "Crash-neutral currency carry trades" Journal of Financial Economics 2014»; WebFetch: sí, ficha IDEAS)
- **Contenido:** Ajusta el carry por riesgo sistémico: sus rendimientos se parecen a una estrategia de rolldown del VIX, y las coberturas con opciones de divisas funcionan como un seguro barato contra shocks sistémicos.
- **Uso en el Motor:** MC-07: ajuste del carry por exposición sistémica y evaluación del coste de cobertura con opciones; CONTRA.
- **Limitaciones:** Documento de trabajo sin versión de revista verificada.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### FXM-0232 · Q 84 (A) — Downside Market Risk of Carry Trades

- **Autores:** V. Dobrynskaya
- **Año:** 2014
- **Publicación o institución:** Review of Finance, vol. 18, n.º 5, págs. 1885-1913
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-07 Riesgo de cola, saltos y valores extremos en divisas (principal) · secundarias: TMX-06
- **Calidad Q:** 84 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 7/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** https://ideas.repec.org/a/eee/jfinec/v114y2014i2p197-225.html (índice)
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Lettau Maggiori Weber "Conditional risk premia in currency markets and other asset classes" ideas.repec.org»; WebFetch: sí, índice: ficha IDEAS de Lettau, Maggiori y Weber 2014, lista «Most related items», https://ideas.repec.org/a/eee/jfinec/v114y2014i2p197-225.html)
- **Contenido:** Muestra que las carteras de carry tienen betas bajistas frente al mercado mundial mayores que las alcistas y que el riesgo de mercado bajista explica su rentabilidad.
- **Uso en el Motor:** MC-07: betas condicionales bajista/alcista del carry; CONTRA.
- **Limitaciones:** Confirmada solo por índice; DOI no visto.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### FXM-0228 · Q 84 (A) — The Statistical Properties of Daily Foreign Exchange Rates: 1974-1983

- **Autores:** D. A. Hsieh
- **Año:** 1988
- **Publicación o institución:** Journal of International Economics, vol. 24, págs. 129-145
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-07 Riesgo de cola, saltos y valores extremos en divisas (principal) · secundarias: TMX-02
- **Calidad Q:** 84 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 5/10 · Impacto 9/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** https://people.duke.edu/~dah7/vitae.htm (índice) · https://scholars.duke.edu/publication/777404
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Hsieh 1988 "The statistical properties of daily foreign exchange rates: 1974-1983" Journal of International Economics»; WebFetch: sí, índice: currículum de D. A. Hsieh, https://people.duke.edu/~dah7/vitae.htm)
- **Contenido:** Documenta que los rendimientos cambiarios diarios no son iid ni normales: colas gruesas (leptocurtosis) y heterocedasticidad condicional explican buena parte de la no normalidad.
- **Uso en el Motor:** MC-07: justificación de distribuciones de colas gruesas y modelos condicionales antes de medir VaR/ES cambiario; MC-02.
- **Limitaciones:** Muestra antigua; confirmada solo por índice.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### FXM-0214 · Q 82 (A) — Conditionally-Hedged Currency Carry Trades

- **Autores:** Jin Ho Choi; Sangwon Suh
- **Año:** 2022
- **Publicación o institución:** Journal of International Financial Markets, Institutions and Money, vol. 79
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-07 Riesgo de cola, saltos y valores extremos en divisas (principal) · secundarias: TMX-05
- **Calidad Q:** 82 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 11/15 · Vigencia 10/10 · Impacto 5/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1016/j.intfin.2022.101591 · https://ideas.repec.org/a/eee/intfin/v79y2022ics1042443122000737.html
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Jurek "Crash-neutral currency carry trades" Journal of Financial Economics 2014»; WebFetch: sí, ficha IDEAS)
- **Contenido:** Usa precios de opciones para predecir crashes del carry y cubre solo en los periodos de crash previsto, reduciendo la exposición a cola y mejorando el resultado frente al carry convencional.
- **Uso en el Motor:** MC-07: cobertura condicional del riesgo de cola del carry con señales de opciones; AS-ESTR.
- **Limitaciones:** Evidencia reciente y menos replicada.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### FXM-0210 · Q 82 (A) — When Carry Goes Bad: The Magnitude, Causes, and Duration of Currency Carry Unwinds

- **Autores:** Michael Melvin; Duncan Shand
- **Año:** 2017
- **Publicación o institución:** Financial Analysts Journal, vol. 73, n.º 1, págs. 121-144
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-07 Riesgo de cola, saltos y valores extremos en divisas (principal) · secundarias: TMX-06
- **Calidad Q:** 82 (A) — Tipo 23/25 · Rigor 16/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 7/10 · Independencia 9/10 · Acceso 4/10
- **DOI / ISBN / URL:** DOI: 10.2469/faj.v73.n1.4 · https://rpc.cfainstitute.org/en/research/financial-analysts-journal/2017/when-carry-goes-bad-the-magnitude-causes-and-duration-of-currency-carry-unwinds
- **Acceso y licencia:** Texto completo para miembros del CFA Institute
- **Estado:** Aprobada
- **Estado del enlace:** MURO_PAGO
- **Última verificación:** 2026-11-02 (búsqueda web: «Daniel Hodrick Lu "The Carry Trade: Risks and Drawdowns" Critical Finance Review 2017»; WebFetch: sí, página CFA Institute)
- **Contenido:** Analiza las mayores pérdidas del carry cambiario y modela la duración de los drawdowns con el carry esperado inicial, el estrés financiero y la distancia de la cartera de carry a una de valor; fuera de muestra limita pérdidas.
- **Uso en el Motor:** MC-07: modelo de duración de desplomes del carry; CONTRA y AS-ESTR para alertas de deshacimiento.
- **Limitaciones:** Artículo orientado a practicantes; acceso de pago.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### DOC-MOT-0079 · Q 80 (A) — Backtesting Expected Shortfall

- **Autores:** Carlo Acerbi; Balázs Székely
- **Año:** 2014
- **Publicación o institución:** MSCI Inc. (documento de investigación, diciembre de 2014; borrador de 27/10/2014)
- **Tipo de documento:** Informe técnico con metodología
- **Temática:** TMX-07 Riesgo de cola, saltos y valores extremos en divisas (principal) · secundarias: TMX-08
- **Calidad Q:** 80 (A) — Tipo 15/25 · Rigor 16/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 8/10 · Acceso 9/10
- **DOI / ISBN / URL:** Sin DOI · https://www.msci.com/documents/10199/22aa9922-f874-4060-b77a-0f0e267a489b
- **Acceso y licencia:** Acceso gratuito (MSCI)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Acerbi Szekely "Backtesting Expected Shortfall" 2014 Risk MSCI»; WebFetch: sí, documento MSCI)
- **Contenido:** Tres contrastes no paramétricos para backtesting del ES (magnitud de excepciones, contraste directo de cola y contraste por rangos).
- **Uso en el Motor:** MC-07, MC-10: backtesting del déficit esperado de carteras de carry y cestas de divisas.
- **Limitaciones:** Autores vinculados a proveedor comercial; la versión en la revista Risk no se ha confirmado.
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (tanda 2). Reutilizada de F8 general V3.2 (TM-08, mismo ID) para el Bloque A Forex el 2026-11-02.

#### FXM-0233 · Q 80 (A) — Currency Excess Returns and Global Downside Market Risk

- **Autores:** V. Atanasov; T. Nitschka
- **Año:** 2014
- **Publicación o institución:** Journal of International Money and Finance, vol. 47, págs. 268-285
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-07 Riesgo de cola, saltos y valores extremos en divisas (principal) · secundarias: TMX-06
- **Calidad Q:** 80 (A) — Tipo 25/25 · Rigor 14/20 · Autoridad 12/15 · Vigencia 10/10 · Impacto 5/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** https://ideas.repec.org/a/eee/jfinec/v114y2014i2p197-225.html (índice)
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Lettau Maggiori Weber "Conditional risk premia in currency markets and other asset classes" ideas.repec.org»; WebFetch: sí, índice: ficha IDEAS de Lettau, Maggiori y Weber 2014, lista «Most related items», https://ideas.repec.org/a/eee/jfinec/v114y2014i2p197-225.html)
- **Contenido:** Relaciona los excesos de rentabilidad cambiarios con el riesgo de mercado global bajista, complementando el DR-CAPM.
- **Uso en el Motor:** MC-07: contraste de robustez del riesgo bajista global en carteras de divisas.
- **Limitaciones:** Confirmada solo por índice; nombres de pila y DOI no vistos.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### FXM-0234 · Q 79 (B) — The Tail Risk Premia of the Carry Trades

- **Autores:** P. Dupuy
- **Año:** 2015
- **Publicación o institución:** Journal of International Money and Finance, vol. 59, págs. 123-145
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-07 Riesgo de cola, saltos y valores extremos en divisas (principal) · secundarias: TMX-05
- **Calidad Q:** 79 (B) — Tipo 25/25 · Rigor 14/20 · Autoridad 12/15 · Vigencia 10/10 · Impacto 4/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** https://ideas.repec.org/a/eee/jfinec/v114y2014i2p197-225.html (índice)
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Lettau Maggiori Weber "Conditional risk premia in currency markets and other asset classes" ideas.repec.org»; WebFetch: sí, índice: ficha IDEAS de Lettau, Maggiori y Weber 2014, lista «Most related items», https://ideas.repec.org/a/eee/jfinec/v114y2014i2p197-225.html)
- **Contenido:** Estima las primas de riesgo de cola incorporadas en el carry cambiario y su contribución al rendimiento.
- **Uso en el Motor:** MC-07: cuantificación de la prima de cola del carry; AS-ESTR.
- **Limitaciones:** Confirmada solo por índice; nombre de pila y DOI no vistos.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

## TMX-08 Evaluación predictiva frente al paseo aleatorio y backtesting cambiario

#### FXM-0236 · Q 97 (A) — Exchange Rate Predictability

- **Autores:** Barbara Rossi
- **Año:** 2013
- **Publicación o institución:** Journal of Economic Literature, vol. 51, n.º 4, págs. 1063-1119 (versiones previas: UPF WP 1369; CEPR DP 9575)
- **Tipo de documento:** Artículo de revisión revisado por pares
- **Temática:** TMX-08 Evaluación predictiva frente al paseo aleatorio y backtesting cambiario (principal) · secundarias: TMX-01
- **Calidad Q:** 97 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** https://ideas.repec.org/p/upf/upfgen/1369.html · Versión abierta: https://econ-papers.upf.edu/papers/1369.pdf
- **Acceso y licencia:** Revista por suscripción (AEA); documento de trabajo UPF en abierto
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Rossi 2013 "Exchange Rate Predictability" Journal of Economic Literature 51(4) ideas.repec.org»; WebFetch: sí, ficha IDEAS)
- **Contenido:** Revisión empírica de la predictibilidad cambiaria: depende del predictor, horizonte, muestra, modelo y método de evaluación; el paseo aleatorio sin deriva es el rival más duro y las reglas de Taylor y los activos exteriores netos son los predictores más prometedores.
- **Uso en el Motor:** MC-10: protocolo de evaluación frente al paseo aleatorio sin deriva (elección de ventana, contrastes, inestabilidad); PROS y EVAL.
- **Limitaciones:** Revisión de 2013; no cubre los métodos de aprendizaje automático posteriores.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### DOC-MOT-0103 · Q 95 (A) — … and the Cross-Section of Expected Returns

- **Autores:** Campbell R. Harvey; Yan Liu; Heqing Zhu
- **Año:** 2016
- **Publicación o institución:** The Review of Financial Studies, 29(1), 5-68
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-08 Evaluación predictiva frente al paseo aleatorio y backtesting cambiario (principal) · secundarias: TMX-06
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1093/rfs/hhv059 · https://academicnewsletter.sufe.edu.cn/info/353765
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Harvey Liu Zhu "and the Cross-Section of Expected Returns" probability of backtest overfitting»; WebFetch: sí)
- **Contenido:** Recopila más de 300 factores publicados y aplica correcciones por pruebas múltiples; propone exigir t > 3 a los nuevos factores.
- **Uso en el Motor:** MC-10: umbrales de t elevados ante pruebas múltiples al validar nuevos factores cambiarios.
- **Limitaciones:** Umbral orientativo, dependiente del supuesto de pruebas no publicadas. Volumen/fascículo tomados de la semilla (la página leída solo mostraba revista, año, DOI y página inicial 5).
- **Origen:** Reutilizada de F8 general V3.2 (TM-11, mismo ID) para el Bloque A Forex el 2026-11-02.

#### DOC-MOT-0094 · Q 95 (A) — Approximately Normal Tests for Equal Predictive Accuracy in Nested Models

- **Autores:** Todd E. Clark; Kenneth D. West
- **Año:** 2007
- **Publicación o institución:** Journal of Econometrics, 138(1), 291-311 (versión previa: NBER Technical Working Paper 326, 2006)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-08 Evaluación predictiva frente al paseo aleatorio y backtesting cambiario (principal) · secundarias: —
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI WP: 10.3386/t0326 · https://www.nber.org/papers/t0326
- **Acceso y licencia:** Documento de trabajo NBER de acceso abierto; artículo de revista de pago
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Clark West 2007 "Approximately normal tests for equal predictive accuracy in nested models" Journal of Econometrics»; WebFetch: sí)
- **Contenido:** Ajusta el diferencial de error cuadrático para comparar un modelo con su versión anidada (p. ej., señal frente a paseo aleatorio) con valores críticos aproximadamente normales.
- **Uso en el Motor:** MC-10: contraste Clark-West para modelos anidados; obligatorio cuando el modelo cambiario anida el paseo aleatorio sin deriva.
- **Limitaciones:** Específico de pérdida cuadrática. Cita de revista confirmada en la bibliografía del paquete R pretest; el DOI de revista de la semilla no se ha visto y se retira.
- **Origen:** Reutilizada de F8 general V3.2 (TM-11, mismo ID) para el Bloque A Forex el 2026-11-02.

#### DOC-MOT-0093 · Q 95 (A) — Tests of Conditional Predictive Ability

- **Autores:** Raffaella Giacomini; Halbert White
- **Año:** 2006
- **Publicación o institución:** Econometrica, 74(6), 1545-1578
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-08 Evaluación predictiva frente al paseo aleatorio y backtesting cambiario (principal) · secundarias: —
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1111/j.1468-0262.2006.00718.x · https://ideas.repec.org:443/a/ecm/emetrp/v74y2006i6p1545-1578.html
- **Acceso y licencia:** Artículo de pago en el editor; versiones de trabajo de 2003 en RePEc
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Giacomini White 2006 "Tests of Conditional Predictive Ability" Econometrica Clark West nested»; WebFetch: sí)
- **Contenido:** Contraste de capacidad predictiva condicional que compara métodos de pronóstico (modelo más ventana de estimación) y admite modelos anidados con ventanas móviles.
- **Uso en el Motor:** MC-10: capacidad predictiva condicional (Giacomini-White) con ventanas móviles en pronósticos de tipos de cambio.
- **Limitaciones:** Requiere ventana de estimación limitada.
- **Origen:** Reutilizada de F8 general V3.2 (TM-11, mismo ID) para el Bloque A Forex el 2026-11-02.

#### DOC-MOT-0099 · Q 95 (A) — A Reality Check for Data Snooping

- **Autores:** Halbert White
- **Año:** 2000
- **Publicación o institución:** Econometrica, 68(5), 1097-1126
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-08 Evaluación predictiva frente al paseo aleatorio y backtesting cambiario (principal) · secundarias: —
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1111/1468-0262.00152 · https://www.econometricsociety.org/publications/econometrica/2000/09/01/reality-check-data-snooping
- **Acceso y licencia:** Página de la Econometric Society (resumen abierto); texto completo para miembros o suscriptores
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «"Data dredging" wikipedia data snooping White reality check»; WebFetch: sí)
- **Contenido:** Contraste bootstrap de si el mejor de muchos modelos supera a una referencia, corrigiendo la búsqueda de especificaciones (data snooping).
- **Uso en el Motor:** MC-10: Reality Check de White frente al fisgoneo de datos en universos de reglas técnicas y estrategias cambiarias.
- **Limitaciones:** Conservador con modelos irrelevantes (véase Hansen 2005, DOC-MOT-0100).
- **Origen:** Reutilizada de F8 general V3.2 (TM-11, mismo ID) para el Bloque A Forex el 2026-11-02.

#### DOC-MOT-0091 · Q 95 (A) — Comparing Predictive Accuracy

- **Autores:** Francis X. Diebold; Roberto S. Mariano
- **Año:** 1995
- **Publicación o institución:** Journal of Business & Economic Statistics, 13(3), 253-263
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-08 Evaluación predictiva frente al paseo aleatorio y backtesting cambiario (principal) · secundarias: —
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1080/07350015.1995.10524599 · https://pkg.robjhyndman.com/forecast/reference/dm.test.html
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Diebold Mariano test wikipedia»; WebFetch: sí, sobre la página índice https://pkg.robjhyndman.com/forecast/reference/dm.test.html)
- **Contenido:** Propone el contraste DM de igualdad de precisión predictiva entre dos pronósticos con funciones de pérdida generales y errores autocorrelacionados.
- **Uso en el Motor:** MC-10: contraste Diebold-Mariano de igual precisión entre un modelo cambiario y el paseo aleatorio o el forward.
- **Limitaciones:** No válido para modelos anidados (usar Clark-West, DOC-MOT-0094). DOI confirmado en https://en.wikipedia.org/wiki/Mean_absolute_scaled_error.
- **Origen:** Reutilizada de F8 general V3.2 (TM-11, mismo ID) para el Bloque A Forex el 2026-11-02.

#### FXM-0247 · Q 94 (A) — The Adaptive Markets Hypothesis: Evidence from the Foreign Exchange Market

- **Autores:** Christopher J. Neely; Paul A. Weller; Joshua M. Ulrich
- **Año:** 2009
- **Publicación o institución:** Journal of Financial and Quantitative Analysis, vol. 44, n.º 2, págs. 467-488 (versión previa: Federal Reserve Bank of St. Louis WP 2006-046)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-08 Evaluación predictiva frente al paseo aleatorio y backtesting cambiario (principal) · secundarias: TMX-06
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 9/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** DOI: 10.1017/S0022109009090103 · https://ideas.repec.org/a/cup/jfinqa/v44y2009i02p467-488_09.html · https://files.stlouisfed.org/files/htdocs/wp/2006/2006-046.pdf
- **Acceso y licencia:** Revista por suscripción; documento de trabajo de la Fed de San Luis en abierto
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Neely Weller Ulrich "The Adaptive Markets Hypothesis: Evidence from the Foreign Exchange Market" Journal of Financial and Quantitative Analysis»; WebFetch: sí, ficha IDEAS y entrada de la GP Bibliography (DOI))
- **Contenido:** Pruebas verdaderamente fuera de muestra de reglas técnicas cambiarias publicadas: los beneficios de los años setenta y ochenta eran reales, pero desaparecieron a principios de los noventa para filtros y medias móviles, en línea con la hipótesis de mercados adaptativos.
- **Uso en el Motor:** MC-10: evaluación fuera de muestra real y decadencia de señales técnicas cambiarias; EVAL y AS-ESTR.
- **Limitaciones:** Alta volatilidad dificulta estimar rentabilidades medias con precisión.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### DOC-MOT-0080 · Q 94 (A) — The Stationary Bootstrap

- **Autores:** Dimitris N. Politis; Joseph P. Romano
- **Año:** 1994
- **Publicación o institución:** Journal of the American Statistical Association, vol. 89, n.º 428, págs. 1303-1313
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-08 Evaluación predictiva frente al paseo aleatorio y backtesting cambiario (principal) · secundarias: —
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1080/01621459.1994.10476870 · https://doi.org/10.1080/01621459.1994.10476870
- **Acceso y licencia:** Texto completo por suscripción en la editorial (Taylor & Francis)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Ledoit Wolf shrinkage estimation of covariance matrices stationary bootstrap Politis Romano Fama–MacBeth regression (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Bootstrapping (statistics)», que reproduce la cita completa)
- **Contenido:** Remuestreo por bloques de longitud aleatoria geométrica que preserva la estacionariedad de la serie remuestreada.
- **Uso en el Motor:** MC-10: bootstrap estacionario para intervalos de Sharpe y de pérdidas de pronóstico en series cambiarias dependientes.
- **Limitaciones:** Elección de la longitud media de bloque.
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (tanda 2). Reutilizada de F8 general V3.2 (TM-09, mismo ID) para el Bloque A Forex el 2026-11-02.

#### FXM-0249 · Q 93 (A) — Technical Trading: Is It Still Beating the Foreign Exchange Market?

- **Autores:** P.-H. Hsu; M. P. Taylor; Z. Wang
- **Año:** 2016
- **Publicación o institución:** Journal of International Economics, vol. 102, págs. 188-208
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-08 Evaluación predictiva frente al paseo aleatorio y backtesting cambiario (principal) · secundarias: TMX-06
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1016/j.jinteco.2016.03.012 · https://profiles.wustl.edu/en/publications/technical-trading-is-it-still-beating-the-foreign-exchange-market/
- **Acceso y licencia:** Revista por suscripción; ficha institucional (WUSTL)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «"Technical trading-rule profitability, data snooping, and reality check: evidence from the foreign exchange market" Qi Wu»; WebFetch: sí, ficha WUSTL)
- **Contenido:** Contrasta más de 21.000 reglas técnicas en 30 divisas desarrolladas y emergentes durante 45 años con un contraste por pasos frente al fisgoneo de datos; encuentra capacidad predictiva y rentabilidad anómala variable por subperiodos y grupos de países.
- **Uso en el Motor:** MC-10: contraste por pasos (stepwise SPA) sobre universos de reglas cambiarias; AS-ESTR y AS-EMAS/EMLA/EMEA (emergentes).
- **Limitaciones:** Resultados variables por periodo; costes de transacción en emergentes.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### DOC-MOT-0100 · Q 93 (A) — A Test for Superior Predictive Ability

- **Autores:** Peter Reinhard Hansen
- **Año:** 2005
- **Publicación o institución:** Journal of Business & Economic Statistics
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-08 Evaluación predictiva frente al paseo aleatorio y backtesting cambiario (principal) · secundarias: —
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** https://en.wikipedia.org/wiki/Peter_Reinhard_Hansen (lista de publicaciones)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Peter Reinhard Hansen IDEAS RePEc "A Test for Superior Predictive Ability"»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Peter_Reinhard_Hansen)
- **Contenido:** Contraste SPA: versión estudentizada y recentrada del Reality Check, más potente y menos sensible a modelos irrelevantes.
- **Uso en el Motor:** MC-10: contraste SPA de Hansen (más potente que el Reality Check) para la mejor estrategia cambiaria frente al paseo aleatorio.
- **Limitaciones:** Requiere bootstrap estacionario. Solo se han confirmado autor, año, título y revista; volumen, páginas y DOI de la semilla quedan sin confirmar y se retiran.
- **Origen:** Reutilizada de F8 general V3.2 (TM-11, mismo ID) para el Bloque A Forex el 2026-11-02.

#### DOC-MOT-0092 · Q 92 (A) — Testing the Equality of Prediction Mean Squared Errors

- **Autores:** David Harvey; Stephen Leybourne; Paul Newbold
- **Año:** 1997
- **Publicación o institución:** International Journal of Forecasting, 13(2), 281-291
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-08 Evaluación predictiva frente al paseo aleatorio y backtesting cambiario (principal) · secundarias: —
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** https://pkg.robjhyndman.com/forecast/reference/dm.test.html (bibliografía de la función dm.test)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Diebold Mariano test wikipedia»; WebFetch: sí, sobre la página índice https://pkg.robjhyndman.com/forecast/reference/dm.test.html)
- **Contenido:** Corrección de muestra pequeña del contraste DM y uso de la distribución t de Student.
- **Uso en el Motor:** MC-10: corrección de muestra pequeña del Diebold-Mariano en evaluaciones cambiarias con pocos pronósticos (horizontes H3-H4).
- **Limitaciones:** Mismas limitaciones que DM. El DOI de la semilla no se ha visto en la verificación y se retira.
- **Origen:** Reutilizada de F8 general V3.2 (TM-11, mismo ID) para el Bloque A Forex el 2026-11-02.

#### FXM-0218 · Q 90 (A) — The Obstinate Passion of Foreign Exchange Professionals: Technical Analysis

- **Autores:** Lukas Menkhoff; Mark P. Taylor
- **Año:** 2007
- **Publicación o institución:** Journal of Economic Literature, vol. 45, n.º 4, págs. 936-972
- **Tipo de documento:** Artículo de revisión revisado por pares
- **Temática:** TMX-08 Evaluación predictiva frente al paseo aleatorio y backtesting cambiario (principal) · secundarias: TMX-06
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** https://authors.repec.org/pro/pme67 (índice)
- **Acceso y licencia:** Revista por suscripción (AEA)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Lukas Menkhoff IDEAS RePEc "Carry trades and global foreign exchange volatility" "Currency momentum strategies" "Currency value"»; WebFetch: sí, índice: perfil RePEc de L. Menkhoff, https://authors.repec.org/pro/pme67)
- **Contenido:** Revisión de la evidencia sobre el uso y la rentabilidad del análisis técnico en divisas: rentabilidad decreciente en el tiempo, dependencia del periodo y explicaciones (intervención, sesgos, información).
- **Uso en el Motor:** MC-10: marco para evaluar reglas técnicas cambiarias y su decadencia; AS-ESTR y EVAL.
- **Limitaciones:** Revisión; no aporta contrastes nuevos.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### DOC-MOT-0102 · Q 88 (A) — The Probability of Backtest Overfitting

- **Autores:** David H. Bailey; Jonathan M. Borwein; Marcos López de Prado; Qiji Jim Zhu
- **Año:** 2015 (versión SSRN revisada; publicación en Journal of Computational Finance)
- **Publicación o institución:** Journal of Computational Finance (Risk Journals); SSRN 2326253
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-08 Evaluación predictiva frente al paseo aleatorio y backtesting cambiario (principal) · secundarias: —
- **Calidad Q:** 88 (A) — Tipo 22/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 9/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI SSRN: 10.2139/ssrn.2326253 · https://papers.ssrn.com/abstract=2326253
- **Acceso y licencia:** Documento SSRN gratuito; artículo de revista de pago
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Harvey Liu Zhu "and the Cross-Section of Expected Returns" probability of backtest overfitting»; WebFetch: sí)
- **Contenido:** Define la probabilidad de sobreajuste del backtest (PBO) y la estima con validación cruzada simétrica combinatoria (CSCV).
- **Uso en el Motor:** MC-10: probabilidad de sobreajuste del backtesting (CSCV) para las reglas de AS-ESTR.
- **Limitaciones:** Coste computacional. Volumen, páginas y DOI de revista de la semilla no confirmados (SSRN lo daba como «forthcoming»); se retiran.
- **Origen:** Reutilizada de F8 general V3.2 (TM-11, mismo ID) para el Bloque A Forex el 2026-11-02.

#### DOC-MOT-0423 · Q 88 (A) — Comparing Predictive Accuracy, Twenty Years Later: A Personal Perspective on the Use and Abuse of Diebold-Mariano Tests

- **Autores:** Francis X. Diebold
- **Año:** 2015
- **Publicación o institución:** Journal of Business & Economic Statistics, 33(1), 1
- **Tipo de documento:** Artículo revisado por pares (con discusión)
- **Temática:** TMX-08 Evaluación predictiva frente al paseo aleatorio y backtesting cambiario (principal) · secundarias: —
- **Calidad Q:** 88 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.1080/07350015.2014.983236 · https://en.wikipedia.org/wiki/Mean_absolute_scaled_error (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Mean absolute scaled error" en.wikipedia.org Hyndman Koehler»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Mean_absolute_scaled_error)
- **Contenido:** El propio autor delimita el uso correcto del contraste DM (comparar pronósticos, no modelos) y advierte contra su abuso en la selección de modelos.
- **Uso en el Motor:** MC-10: guía de uso correcto del Diebold-Mariano (comparación de pronósticos, no de modelos) en la evaluación frente al paseo aleatorio.
- **Limitaciones:** Ensayo de posición; las páginas finales no figuran en la fuente.
- **Origen:** Reutilizada de F8 general V3.2 (TM-11, mismo ID) para el Bloque A Forex el 2026-11-02.

#### FXM-0239 · Q 88 (A) — Out-of-Sample Forecast Tests Robust to the Choice of Window Size

- **Autores:** Barbara Rossi; A. Inoue
- **Año:** 2012
- **Publicación o institución:** Journal of Business & Economic Statistics, vol. 30, n.º 3, págs. 432-453
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-08 Evaluación predictiva frente al paseo aleatorio y backtesting cambiario (principal) · secundarias: —
- **Calidad Q:** 88 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 7/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** https://ideas.repec.org/p/upf/upfgen/1369.html (índice)
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Rossi 2013 "Exchange Rate Predictability" Journal of Economic Literature 51(4) ideas.repec.org»; WebFetch: sí, índice: ficha IDEAS de Rossi (2013), listas «Most related items» y referencias, https://ideas.repec.org/p/upf/upfgen/1369.html)
- **Contenido:** Propone contrastes de capacidad predictiva fuera de muestra robustos a la elección del tamaño de la ventana de estimación, evitando la búsqueda oportunista de ventanas.
- **Uso en el Motor:** MC-10: contrastes robustos a la ventana al comparar modelos cambiarios con el paseo aleatorio; EVAL.
- **Limitaciones:** Confirmada solo por índice; DOI no visto.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### FXM-0253 · Q 88 (A) — Out-of-Sample Exchange Rate Predictability with Taylor Rule Fundamentals

- **Autores:** T. Molodtsova; D. H. Papell
- **Año:** 2009
- **Publicación o institución:** Journal of International Economics, vol. 77, n.º 2
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-08 Evaluación predictiva frente al paseo aleatorio y backtesting cambiario (principal) · secundarias: TMX-04
- **Calidad Q:** 88 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 9/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** https://ideas.repec.org:443/a/eee/jimfin/v88y2018icp1-24.html (índice)
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Amat Michalski Stoltz "Fundamentals and exchange rate forecastability with simple machine learning methods" ideas.repec.org»; WebFetch: sí, índice: ficha IDEAS de Amat, Michalski y Stoltz (2018), listas de referencias, citas y «Most related items», https://ideas.repec.org:443/a/eee/jimfin/v88y2018icp1-24.html)
- **Contenido:** Muestra que fundamentos de regla de Taylor predicen tipos de cambio a un mes mejor que el paseo aleatorio (contraste Clark-West) en muchas divisas.
- **Uso en el Motor:** MC-10: modelo de referencia de reglas de Taylor en la evaluación de AS-G10N/AS-G10M; TR-BCM.
- **Limitaciones:** Confirmada solo por índice; DOI no visto.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### DOC-MOT-0104 · Q 88 (A) — The Statistics of Sharpe Ratios

- **Autores:** Andrew W. Lo
- **Año:** 2002
- **Publicación o institución:** Financial Analysts Journal, 58(4), 36-52
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-08 Evaluación predictiva frente al paseo aleatorio y backtesting cambiario (principal) · secundarias: —
- **Calidad Q:** 88 (A) — Tipo 22/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 9/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.2469/faj.v58.n4.2453 · https://en.wikipedia.org/wiki/Sharpe_ratio (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Sharpe ratio" en.wikipedia.org deflated Sharpe ratio»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Sharpe_ratio)
- **Contenido:** Deriva la distribución muestral del ratio de Sharpe con rentabilidades IID y autocorrelacionadas y muestra que la anualización por raíz del tiempo puede sesgarlo mucho.
- **Uso en el Motor:** MC-10: errores estándar del Sharpe de estrategias cambiarias con autocorrelación (carry, momentum).
- **Limitaciones:** Supuestos asintóticos.
- **Origen:** Reutilizada de F8 general V3.2 (TM-11, mismo ID) para el Bloque A Forex el 2026-11-02.

#### FXM-0250 · Q 88 (A) — The Significance of Technical Trading-Rule Profits in the Foreign Exchange Market: A Bootstrap Approach

- **Autores:** Richard M. Levich; Lee R. Thomas
- **Año:** 1993
- **Publicación o institución:** Journal of International Money and Finance, vol. 12, n.º 5, págs. 451-474 (NBER Working Paper 3818, 1991)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-08 Evaluación predictiva frente al paseo aleatorio y backtesting cambiario (principal) · secundarias: —
- **Calidad Q:** 88 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 5/10 · Impacto 9/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** DOI (WP): 10.3386/w3818 · https://nber.org/papers/w3818
- **Acceso y licencia:** Documento de trabajo NBER en abierto; revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «"Technical trading-rule profitability, data snooping, and reality check: evidence from the foreign exchange market" Qi Wu»; WebFetch: sí, página NBER)
- **Contenido:** Evalúa reglas técnicas sobre futuros de divisas (1976-1990) comparando sus beneficios con la distribución obtenida en miles de series remuestreadas.
- **Uso en el Motor:** MC-10: contraste por remuestreo de la significación de beneficios de reglas cambiarias; EVAL.
- **Limitaciones:** Muestra antigua; el remuestreo iid ignora la dependencia de la volatilidad.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### FXM-0255 · Q 87 (A) — Forecast Comparisons in Unstable Environments

- **Autores:** Raffaella Giacomini; Barbara Rossi
- **Año:** 2010
- **Publicación o institución:** Journal of Applied Econometrics, vol. 25, n.º 4
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-08 Evaluación predictiva frente al paseo aleatorio y backtesting cambiario (principal) · secundarias: —
- **Calidad Q:** 87 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 7/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** https://ideas.repec.org:443/a/eee/jimfin/v88y2018icp1-24.html (índice)
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Amat Michalski Stoltz "Fundamentals and exchange rate forecastability with simple machine learning methods" ideas.repec.org»; WebFetch: sí, índice: ficha IDEAS de Amat, Michalski y Stoltz (2018), listas de referencias, citas y «Most related items», https://ideas.repec.org:443/a/eee/jimfin/v88y2018icp1-24.html)
- **Contenido:** Contrastes de capacidad predictiva relativa que varía en el tiempo (fluctuation test), aplicados a modelos de tipo de cambio.
- **Uso en el Motor:** MC-10: detectar periodos en que un modelo cambiario supera o pierde frente al paseo aleatorio; EVAL.
- **Limitaciones:** Confirmada solo por índice; DOI no visto.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### FXM-0238 · Q 87 (A) — Exchange Rate Models Are Not as Bad as You Think

- **Autores:** Charles Engel; N. C. Mark; Kenneth D. West
- **Año:** 2008
- **Publicación o institución:** NBER Macroeconomics Annual 2007, vol. 22, págs. 381-441
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-08 Evaluación predictiva frente al paseo aleatorio y backtesting cambiario (principal) · secundarias: TMX-04
- **Calidad Q:** 87 (A) — Tipo 24/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 9/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** https://ideas.repec.org/p/upf/upfgen/1369.html (índice)
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Rossi 2013 "Exchange Rate Predictability" Journal of Economic Literature 51(4) ideas.repec.org»; WebFetch: sí, índice: ficha IDEAS de Rossi (2013), listas «Most related items» y referencias, https://ideas.repec.org/p/upf/upfgen/1369.html)
- **Contenido:** Defiende que superar al paseo aleatorio no es la prueba adecuada para modelos de fundamentos y muestra mejoras con datos de panel, horizontes largos y reglas de Taylor.
- **Uso en el Motor:** MC-10: criterios de evaluación de modelos de fundamentos con paneles y horizontes largos (H3-H4); PROS.
- **Limitaciones:** Confirmada solo por índice; DOI no visto.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### FXM-0251 · Q 87 (A) — Using Out-of-Sample Mean Squared Prediction Errors to Test the Martingale Difference Hypothesis

- **Autores:** Todd E. Clark; Kenneth D. West
- **Año:** 2006
- **Publicación o institución:** Journal of Econometrics, vol. 135
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-08 Evaluación predictiva frente al paseo aleatorio y backtesting cambiario (principal) · secundarias: —
- **Calidad Q:** 87 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 8/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** https://ideas.repec.org:443/a/eee/jimfin/v88y2018icp1-24.html (índice)
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Amat Michalski Stoltz "Fundamentals and exchange rate forecastability with simple machine learning methods" ideas.repec.org»; WebFetch: sí, índice: ficha IDEAS de Amat, Michalski y Stoltz (2018), listas de referencias, citas y «Most related items», https://ideas.repec.org:443/a/eee/jimfin/v88y2018icp1-24.html)
- **Contenido:** Contraste del paseo aleatorio (diferencia martingala) frente a modelos que lo anidan corrigiendo el ruido de estimación del modelo alternativo; aplicación a tipos de cambio.
- **Uso en el Motor:** MC-10: contraste específico de la hipótesis de paseo aleatorio cambiario; complementa a DOC-MOT-0094.
- **Limitaciones:** Confirmada solo por índice; DOI no visto.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### FXM-0252 · Q 87 (A) — Empirical Exchange Rate Models of the Nineties: Are Any Fit to Survive?

- **Autores:** Y.-W. Cheung; M. D. Chinn; A. Garcia Pascual
- **Año:** 2005
- **Publicación o institución:** Journal of International Money and Finance, vol. 24, n.º 7
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-08 Evaluación predictiva frente al paseo aleatorio y backtesting cambiario (principal) · secundarias: TMX-04
- **Calidad Q:** 87 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 9/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** https://ideas.repec.org:443/a/eee/jimfin/v88y2018icp1-24.html (índice)
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Amat Michalski Stoltz "Fundamentals and exchange rate forecastability with simple machine learning methods" ideas.repec.org»; WebFetch: sí, índice: ficha IDEAS de Amat, Michalski y Stoltz (2018), listas de referencias, citas y «Most related items», https://ideas.repec.org:443/a/eee/jimfin/v88y2018icp1-24.html)
- **Contenido:** Compara modelos estructurales de los noventa (paridad de intereses, productividad, BEER, monetario) frente al paseo aleatorio con varias métricas y horizontes; ningún modelo domina de forma consistente.
- **Uso en el Motor:** MC-10: batería de métricas (MSE, dirección, consistencia) para comparar modelos cambiarios; PROS.
- **Limitaciones:** Confirmada solo por índice; DOI no visto.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### FXM-0240 · Q 87 (A) — Why Is It So Difficult to Beat the Random Walk Forecast of Exchange Rates?

- **Autores:** L. Kilian; Mark P. Taylor
- **Año:** 2003
- **Publicación o institución:** Journal of International Economics, vol. 60, n.º 1, págs. 85-107
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-08 Evaluación predictiva frente al paseo aleatorio y backtesting cambiario (principal) · secundarias: TMX-01
- **Calidad Q:** 87 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 9/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** https://ideas.repec.org/p/upf/upfgen/1369.html (índice)
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Rossi 2013 "Exchange Rate Predictability" Journal of Economic Literature 51(4) ideas.repec.org»; WebFetch: sí, índice: ficha IDEAS de Rossi (2013), listas «Most related items» y referencias, https://ideas.repec.org/p/upf/upfgen/1369.html)
- **Contenido:** Atribuye la dificultad de batir al paseo aleatorio a la reversión no lineal a la PPA (bandas de inacción), que solo se manifiesta a horizontes largos.
- **Uso en el Motor:** MC-10, MC-02: expectativas realistas de mejora frente al paseo aleatorio por horizonte; PROS.
- **Limitaciones:** Confirmada solo por índice; DOI no visto.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### DOC-MOT-0415 · Q 86 (A) — Pseudo-Mathematics and Financial Charlatanism: The Effects of Backtest Overfitting on Out-of-Sample Performance

- **Autores:** David H. Bailey; Jonathan M. Borwein; Marcos López de Prado (autoría según la bibliografía consultada)
- **Año:** 2014
- **Publicación o institución:** Notices of the American Mathematical Society, 61(5), 458-471
- **Tipo de documento:** Artículo revisado por pares (divulgación técnica)
- **Temática:** TMX-08 Evaluación predictiva frente al paseo aleatorio y backtesting cambiario (principal) · secundarias: —
- **Calidad Q:** 86 (A) — Tipo 22/25 · Rigor 14/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 9/10 · Acceso 9/10
- **DOI / ISBN / URL:** https://en.wikipedia.org/wiki/Deflated_Sharpe_ratio (bibliografía)
- **Acceso y licencia:** Acceso abierto en la revista de la AMS
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Sharpe ratio" en.wikipedia.org deflated Sharpe ratio»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Deflated_Sharpe_ratio)
- **Contenido:** Muestra que, con pocas observaciones y muchas configuraciones probadas, es casi seguro encontrar un backtest con Sharpe alto sin capacidad predictiva, y propone la longitud mínima de backtest.
- **Uso en el Motor:** MC-10: advertencia y cuantificación del sobreajuste de backtests cambiarios con muchos parámetros.
- **Limitaciones:** Texto divulgativo; resultados bajo supuestos simplificados.
- **Origen:** Reutilizada de F8 general V3.2 (TM-11, mismo ID) para el Bloque A Forex el 2026-11-02.

#### FXM-0241 · Q 86 (A) — Exchange Rate Forecasting: The Errors We've Really Made

- **Autores:** Jon Faust; John H. Rogers; Jonathan H. Wright
- **Año:** 2003
- **Publicación o institución:** Journal of International Economics, vol. 60, n.º 1, págs. 35-59
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-08 Evaluación predictiva frente al paseo aleatorio y backtesting cambiario (principal) · secundarias: —
- **Calidad Q:** 86 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 8/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** https://ideas.repec.org/p/upf/upfgen/1369.html (índice)
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Rossi 2013 "Exchange Rate Predictability" Journal of Economic Literature 51(4) ideas.repec.org»; WebFetch: sí, índice: ficha IDEAS de Rossi (2013), listas «Most related items» y referencias, https://ideas.repec.org/p/upf/upfgen/1369.html)
- **Contenido:** Reevalúa los pronósticos cambiarios con datos en tiempo real (vintages) y muestra que los resultados dependen de las revisiones de los datos macro.
- **Uso en el Motor:** MC-10: obligación de evaluar con datos en tiempo real (vintages) los modelos de fundamentos; EVAL y CUR.
- **Limitaciones:** Confirmada solo por índice; DOI no visto.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### FXM-0237 · Q 86 (A) — Empirical Exchange Rate Models of the Seventies: Do They Fit Out of Sample?

- **Autores:** R. A. Meese; K. Rogoff
- **Año:** 1983
- **Publicación o institución:** Journal of International Economics, vol. 14, n.º 1-2, págs. 3-24
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-08 Evaluación predictiva frente al paseo aleatorio y backtesting cambiario (principal) · secundarias: TMX-04
- **Calidad Q:** 86 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 5/10 · Impacto 10/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** https://ideas.repec.org/p/upf/upfgen/1369.html (índice)
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Rossi 2013 "Exchange Rate Predictability" Journal of Economic Literature 51(4) ideas.repec.org»; WebFetch: sí, índice: ficha IDEAS de Rossi (2013), listas «Most related items» y referencias, https://ideas.repec.org/p/upf/upfgen/1369.html)
- **Contenido:** Trabajo fundacional que muestra que los modelos estructurales de tipo de cambio no superan al paseo aleatorio fuera de muestra a horizontes de 1 a 12 meses, incluso con fundamentos observados.
- **Uso en el Motor:** MC-10: origen del paseo aleatorio como referencia obligatoria (R13) en toda evaluación cambiaria; PROS y EVAL.
- **Limitaciones:** Confirmada solo por índice; DOI no visto.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### DOC-MOT-0101 · Q 85 (A) — The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting, and Non-Normality

- **Autores:** David H. Bailey; Marcos López de Prado
- **Año:** 2014
- **Publicación o institución:** The Journal of Portfolio Management, 40(5), 94-107
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-08 Evaluación predictiva frente al paseo aleatorio y backtesting cambiario (principal) · secundarias: TMX-06
- **Calidad Q:** 85 (A) — Tipo 22/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 8/10 · Acceso 5/10
- **DOI / ISBN / URL:** https://en.wikipedia.org/wiki/Deflated_Sharpe_ratio (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Sharpe ratio" en.wikipedia.org deflated Sharpe ratio»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Deflated_Sharpe_ratio)
- **Contenido:** Ajusta el Sharpe observado por el número de estrategias probadas, la asimetría y la curtosis para estimar la probabilidad de que el Sharpe verdadero sea positivo.
- **Uso en el Motor:** MC-10: Sharpe deflactado de estrategias de carry, momentum y valor cambiario según número de ensayos, asimetría y curtosis.
- **Limitaciones:** Requiere estimar el número efectivo de ensayos. El DOI de la semilla no se ha visto en la verificación y se retira.
- **Origen:** Reutilizada de F8 general V3.2 (TM-11, mismo ID) para el Bloque A Forex el 2026-11-02.

#### FXM-0256 · Q 85 (A) — Bayesian Model Averaging and Exchange Rate Forecasts

- **Autores:** Jonathan H. Wright
- **Año:** 2008
- **Publicación o institución:** Journal of Econometrics, vol. 146, n.º 2
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-08 Evaluación predictiva frente al paseo aleatorio y backtesting cambiario (principal) · secundarias: TMX-09
- **Calidad Q:** 85 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 7/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** https://ideas.repec.org:443/a/eee/jimfin/v88y2018icp1-24.html (índice)
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Amat Michalski Stoltz "Fundamentals and exchange rate forecastability with simple machine learning methods" ideas.repec.org»; WebFetch: sí, índice: ficha IDEAS de Amat, Michalski y Stoltz (2018), listas de referencias, citas y «Most related items», https://ideas.repec.org:443/a/eee/jimfin/v88y2018icp1-24.html)
- **Contenido:** Aplica promediado bayesiano de modelos a pronósticos cambiarios con muchos predictores, con ligeras mejoras frente al paseo aleatorio.
- **Uso en el Motor:** MC-10, MC-06: combinación de modelos cambiarios con incertidumbre de modelo; PROS.
- **Limitaciones:** Confirmada solo por índice; DOI no visto.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### FXM-0242 · Q 85 (A) — Exchange Rates and Fundamentals: Evidence on Long-Horizon Predictability

- **Autores:** N. C. Mark
- **Año:** 1995
- **Publicación o institución:** American Economic Review, vol. 85, n.º 1, págs. 201-218
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-08 Evaluación predictiva frente al paseo aleatorio y backtesting cambiario (principal) · secundarias: TMX-04
- **Calidad Q:** 85 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 5/10 · Impacto 10/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** https://ideas.repec.org/p/upf/upfgen/1369.html (índice)
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Rossi 2013 "Exchange Rate Predictability" Journal of Economic Literature 51(4) ideas.repec.org»; WebFetch: sí, índice: ficha IDEAS de Rossi (2013), listas «Most related items» y referencias, https://ideas.repec.org/p/upf/upfgen/1369.html)
- **Contenido:** Encuentra predictibilidad de los fundamentos monetarios a horizontes largos (16 trimestres) con inferencia por bootstrap.
- **Uso en el Motor:** MC-10: regresiones de horizonte largo y su inferencia por bootstrap en evaluaciones H3-H4.
- **Limitaciones:** Confirmada solo por índice; DOI no visto.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### FXM-0254 · Q 84 (A) — Predicting Exchange Rates Out of Sample: Can Economic Fundamentals Beat the Random Walk?

- **Autores:** J. Li; I. Tsiakas; W. Wang
- **Año:** 2015
- **Publicación o institución:** Journal of Financial Econometrics, vol. 13, n.º 2
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-08 Evaluación predictiva frente al paseo aleatorio y backtesting cambiario (principal) · secundarias: TMX-06
- **Calidad Q:** 84 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 6/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** https://ideas.repec.org:443/a/eee/jimfin/v88y2018icp1-24.html (índice)
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Amat Michalski Stoltz "Fundamentals and exchange rate forecastability with simple machine learning methods" ideas.repec.org»; WebFetch: sí, índice: ficha IDEAS de Amat, Michalski y Stoltz (2018), listas de referencias, citas y «Most related items», https://ideas.repec.org:443/a/eee/jimfin/v88y2018icp1-24.html)
- **Contenido:** Combina fundamentos con regresiones penalizadas y evalúa su valor estadístico y económico frente al paseo aleatorio.
- **Uso en el Motor:** MC-10: evaluación económica (utilidad del inversor) de pronósticos cambiarios basados en fundamentos.
- **Limitaciones:** Confirmada solo por índice; nombres de pila y DOI no vistos.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### FXM-0245 · Q 84 (A) — The Taylor Rule and Forecast Intervals for Exchange Rates

- **Autores:** J. Wang; J. J. Wu
- **Año:** 2012
- **Publicación o institución:** Journal of Money, Credit and Banking, vol. 44, n.º 1, págs. 103-144
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-08 Evaluación predictiva frente al paseo aleatorio y backtesting cambiario (principal) · secundarias: TMX-04
- **Calidad Q:** 84 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 6/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** https://ideas.repec.org/p/upf/upfgen/1369.html (índice)
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Rossi 2013 "Exchange Rate Predictability" Journal of Economic Literature 51(4) ideas.repec.org»; WebFetch: sí, índice: ficha IDEAS de Rossi (2013), listas «Most related items» y referencias, https://ideas.repec.org/p/upf/upfgen/1369.html)
- **Contenido:** Evalúa intervalos de pronóstico (no solo puntuales) de modelos de regla de Taylor frente al paseo aleatorio, con mejoras en la cobertura de intervalos.
- **Uso en el Motor:** MC-10: evaluación de intervalos y densidades de pronóstico cambiario frente al paseo aleatorio; PROS y EVAL.
- **Limitaciones:** Confirmada solo por índice; DOI no visto.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### FXM-0248 · Q 83 (A) — Lessons from the Evolution of Foreign Exchange Trading Strategies

- **Autores:** Christopher Neely; Paul A. Weller
- **Año:** 2011
- **Publicación o institución:** Federal Reserve Bank of St. Louis Working Paper 2011-021 (la ficha enlaza una versión de 2013 en Journal of Banking & Finance, vol. 37, n.º 10, págs. 3783-3798, deducida del enlace)
- **Tipo de documento:** Documento de trabajo
- **Temática:** TMX-08 Evaluación predictiva frente al paseo aleatorio y backtesting cambiario (principal) · secundarias: TMX-06
- **Calidad Q:** 83 (A) — Tipo 20/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 8/10 · Impacto 6/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** DOI: 10.20955/wp.2011.021 · https://econpapers.repec.org/paper/fipfedlwp/2011-021.htm
- **Acceso y licencia:** Acceso abierto (Fed de San Luis)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Neely Weller Ulrich "The Adaptive Markets Hypothesis: Evidence from the Foreign Exchange Market" Journal of Financial and Quantitative Analysis»; WebFetch: sí, ficha EconPapers)
- **Contenido:** Simula un inversor que selecciona en tiempo real entre reglas técnicas cambiarias, carry y renta variable: el backtesting no habría elegido el carry hasta los noventa y la rentabilidad cambiaria migra hacia emergentes.
- **Uso en el Motor:** MC-10: selección de estrategias en tiempo real (sin sesgo de retrospectiva) en backtests cambiarios; AS-ESTR.
- **Limitaciones:** Datos de la versión de revista no verificados directamente.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### FXM-0246 · Q 83 (A) — Forecasting Exchange Rates with a Large Bayesian VAR

- **Autores:** A. Carriero; G. Kapetanios; M. Marcellino
- **Año:** 2009
- **Publicación o institución:** International Journal of Forecasting, vol. 25, n.º 2, págs. 400-417
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-08 Evaluación predictiva frente al paseo aleatorio y backtesting cambiario (principal) · secundarias: TMX-09
- **Calidad Q:** 83 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 7/10 · Impacto 7/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** https://ideas.repec.org/p/upf/upfgen/1369.html (índice)
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Rossi 2013 "Exchange Rate Predictability" Journal of Economic Literature 51(4) ideas.repec.org»; WebFetch: sí, índice: ficha IDEAS de Rossi (2013), listas «Most related items» y referencias, https://ideas.repec.org/p/upf/upfgen/1369.html)
- **Contenido:** Pronostica conjuntamente un panel amplio de tipos de cambio con un VAR bayesiano grande y contracción, mejorando ligeramente al paseo aleatorio.
- **Uso en el Motor:** MC-10, MC-06: modelo multivariante con contracción para pronóstico conjunto de divisas; PROS.
- **Limitaciones:** Confirmada solo por índice; DOI no visto.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### FXM-0243 · Q 83 (A) — Testing Long-Horizon Predictive Ability with High Persistence, and the Meese-Rogoff Puzzle

- **Autores:** Barbara Rossi
- **Año:** 2005
- **Publicación o institución:** International Economic Review, vol. 46, n.º 1, págs. 61-92
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-08 Evaluación predictiva frente al paseo aleatorio y backtesting cambiario (principal) · secundarias: —
- **Calidad Q:** 83 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 7/10 · Impacto 6/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** https://ideas.repec.org/p/upf/upfgen/1369.html (índice)
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Rossi 2013 "Exchange Rate Predictability" Journal of Economic Literature 51(4) ideas.repec.org»; WebFetch: sí, índice: ficha IDEAS de Rossi (2013), listas «Most related items» y referencias, https://ideas.repec.org/p/upf/upfgen/1369.html)
- **Contenido:** Contrastes de capacidad predictiva a horizonte largo válidos con regresores muy persistentes, aplicados al enigma de Meese-Rogoff.
- **Uso en el Motor:** MC-10: inferencia con predictores persistentes (diferenciales de tipos, tipo real) a horizontes largos.
- **Limitaciones:** Confirmada solo por índice; DOI no visto.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### FXM-0259 · Q 82 (A) — Can Currency-Based Risk Factors Help Forecast Exchange Rates?

- **Autores:** S. Ahmed; X. Liu; G. Valente
- **Año:** 2016
- **Publicación o institución:** International Journal of Forecasting, vol. 32, n.º 1
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-08 Evaluación predictiva frente al paseo aleatorio y backtesting cambiario (principal) · secundarias: TMX-06
- **Calidad Q:** 82 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 13/15 · Vigencia 9/10 · Impacto 6/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** https://ideas.repec.org/p/cpr/ceprdp/15305.html (índice)
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Filippou Rapach Taylor Zhou "Exchange rate prediction with machine learning and a smart carry portfolio"»; WebFetch: sí, índice: ficha IDEAS de CEPR DP 15305, lista «Most related items», https://ideas.repec.org/p/cpr/ceprdp/15305.html)
- **Contenido:** Evalúa si los factores de riesgo cambiarios (dólar, carry, etc.) mejoran el pronóstico de tipos bilaterales frente al paseo aleatorio.
- **Uso en el Motor:** MC-10, MC-09: uso de factores cambiarios como predictores en la evaluación frente al paseo aleatorio.
- **Limitaciones:** Confirmada solo por índice; nombres completos y DOI no vistos.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### FXM-0244 · Q 82 (A) — The Continuing Puzzle of Short Horizon Exchange Rate Forecasting

- **Autores:** K. Rogoff; V. Stavrakeva
- **Año:** 2008
- **Publicación o institución:** NBER Working Paper 14071
- **Tipo de documento:** Documento de trabajo
- **Temática:** TMX-08 Evaluación predictiva frente al paseo aleatorio y backtesting cambiario (principal) · secundarias: —
- **Calidad Q:** 82 (A) — Tipo 20/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 7/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** https://ideas.repec.org/p/upf/upfgen/1369.html (índice)
- **Acceso y licencia:** Acceso abierto
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Rossi 2013 "Exchange Rate Predictability" Journal of Economic Literature 51(4) ideas.repec.org»; WebFetch: sí, índice: ficha IDEAS de Rossi (2013), listas «Most related items» y referencias, https://ideas.repec.org/p/upf/upfgen/1369.html)
- **Contenido:** Critica las pruebas de predictibilidad cambiaria a horizonte corto: los resultados positivos son frágiles a la ventana, la muestra y el contraste (Clark-West frente a DM).
- **Uso en el Motor:** MC-10: advertencias sobre el uso de Clark-West y la robustez temporal de las mejoras frente al paseo aleatorio; CONTRA.
- **Limitaciones:** Confirmada solo por índice; DOI no visto.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### FXM-0257 · Q 82 (A) — A Utility-Based Comparison of Some Models of Exchange Rate Volatility

- **Autores:** Kenneth D. West; H. J. Edison; D. Cho
- **Año:** 1993
- **Publicación o institución:** Journal of International Economics, vol. 35
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-08 Evaluación predictiva frente al paseo aleatorio y backtesting cambiario (principal) · secundarias: TMX-02
- **Calidad Q:** 82 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 5/10 · Impacto 7/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** https://ideas.repec.org:443/a/eee/jimfin/v88y2018icp1-24.html (índice)
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Amat Michalski Stoltz "Fundamentals and exchange rate forecastability with simple machine learning methods" ideas.repec.org»; WebFetch: sí, índice: ficha IDEAS de Amat, Michalski y Stoltz (2018), listas de referencias, citas y «Most related items», https://ideas.repec.org:443/a/eee/jimfin/v88y2018icp1-24.html)
- **Contenido:** Compara modelos de volatilidad cambiaria por la utilidad que generan a un inversor media-varianza, no solo por métricas estadísticas.
- **Uso en el Motor:** MC-10: evaluación económica de pronósticos de volatilidad cambiaria; TR-PFV.
- **Limitaciones:** Confirmada solo por índice; DOI no visto.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### FXM-0258 · Q 80 (A) — Evaluation of Exchange Rate Point and Density Forecasts: An Application to Brazil

- **Autores:** W. P. Gaglianone; J. T. M. Marins
- **Año:** 2017
- **Publicación o institución:** International Journal of Forecasting, vol. 33, n.º 3
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-08 Evaluación predictiva frente al paseo aleatorio y backtesting cambiario (principal) · secundarias: —
- **Calidad Q:** 80 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 12/15 · Vigencia 9/10 · Impacto 5/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** https://ideas.repec.org/a/gam/jjrfmx/v13y2020i3p48-d328353.html (índice)
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Amat Michalski Stoltz "Fundamentals and exchange rate forecastability with simple machine learning methods" ideas.repec.org»; WebFetch: sí, índice: ficha IDEAS de Zhang y Hamori (2020), lista «Most related items», https://ideas.repec.org/a/gam/jjrfmx/v13y2020i3p48-d328353.html)
- **Contenido:** Evalúa pronósticos puntuales y de densidad del real brasileño (BRL), con contrastes de calibración de densidades en una divisa emergente.
- **Uso en el Motor:** MC-10: evaluación de densidades de pronóstico en divisas emergentes; AS-EMLA.
- **Limitaciones:** Confirmada solo por índice; nombres completos y DOI no vistos.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### FXM-0235 · Q 77 (B) — The Profitability of Currency Speculation

- **Autores:** J. F. O. Bilson; D. A. Hsieh
- **Año:** 1987
- **Publicación o institución:** International Journal of Forecasting, vol. 3, págs. 115-130
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-08 Evaluación predictiva frente al paseo aleatorio y backtesting cambiario (principal) · secundarias: TMX-06
- **Calidad Q:** 77 (B) — Tipo 25/25 · Rigor 14/20 · Autoridad 13/15 · Vigencia 5/10 · Impacto 6/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** https://people.duke.edu/~dah7/vitae.htm (índice)
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Hsieh 1988 "The statistical properties of daily foreign exchange rates: 1974-1983" Journal of International Economics»; WebFetch: sí, índice: currículum de D. A. Hsieh, https://people.duke.edu/~dah7/vitae.htm)
- **Contenido:** Evalúa la rentabilidad de estrategias especulativas en divisas basadas en el diferencial forward, un antecedente de la evaluación económica de pronósticos cambiarios.
- **Uso en el Motor:** MC-10: evaluación económica (no solo estadística) de pronósticos cambiarios; AS-ESTR.
- **Limitaciones:** Confirmada solo por índice; DOI no visto.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

## TMX-09 Aprendizaje automático y análisis de texto para divisas

#### FXM-0271 · Q 97 (A) — Text as Data

- **Autores:** Matthew Gentzkow; Bryan Kelly; Matt Taddy
- **Año:** 2019
- **Publicación o institución:** Journal of Economic Literature, vol. 57, n.º 3, págs. 535-574 (NBER Working Paper 23276)
- **Tipo de documento:** Artículo de revisión revisado por pares
- **Temática:** TMX-09 Aprendizaje automático y análisis de texto para divisas (principal) · secundarias: —
- **Calidad Q:** 97 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** DOI: 10.1257/jel.20181020 · https://ideas.repec.org/a/aea/jeclit/v57y2019i3p535-74.html · Versión abierta: https://web.stanford.edu/%7Egentzkow/research/text-as-data.pdf
- **Acceso y licencia:** Revista por suscripción (AEA); versión de trabajo abierta
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Gentzkow Kelly Taddy "Text as Data" Journal of Economic Literature 2019»; WebFetch: sí, ficha IDEAS)
- **Contenido:** Guía de referencia del texto como dato en economía: representación (bolsas de palabras, embeddings), métodos estadísticos (diccionarios, regresión penalizada, modelos de temas) y aplicaciones.
- **Uso en el Motor:** MC-06: marco metodológico para convertir comunicados de bancos centrales y noticias en señales cambiarias (TR-BCM).
- **Limitaciones:** No específico de divisas.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### DOC-MOT-0086 · Q 95 (A) — Empirical Asset Pricing via Machine Learning

- **Autores:** Shihao Gu; Bryan Kelly; Dacheng Xiu
- **Año:** 2020
- **Publicación o institución:** The Review of Financial Studies, 33(5), 2223-2273 (versión previa: NBER Working Paper 25398, 2018, rev. 2019)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-09 Aprendizaje automático y análisis de texto para divisas (principal) · secundarias: TMX-06
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1093/rfs/hhaa009 · https://nber.org/papers/w25398
- **Acceso y licencia:** Artículo de revista de pago; documento de trabajo NBER de acceso abierto (DOI WP: 10.3386/w25398)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Gu Kelly Xiu 2020 "Empirical Asset Pricing via Machine Learning" Review of Financial Studies»; WebFetch: sí)
- **Contenido:** Compara regresiones penalizadas, componentes principales, árboles potenciados, bosques aleatorios y redes neuronales para predecir rentabilidades de acciones de EE. UU.; árboles y redes superan con claridad a los modelos lineales, con variables de momentum, liquidez y volatilidad como predictores dominantes.
- **Uso en el Motor:** MC-06: comparativa de métodos de aprendizaje automático para predicción de rentabilidades; plantilla para la predicción de rendimientos cambiarios con muchos predictores.
- **Limitaciones:** Universo estadounidense; costes de implementación y de rotación no centrales.
- **Origen:** Reutilizada de F8 general V3.2 (TM-10, mismo ID) para el Bloque A Forex el 2026-11-02.

#### FXM-0272 · Q 94 (A) — Shocking Language: Understanding the Macroeconomic Effects of Central Bank Communication

- **Autores:** Stephen Hansen; Michael McMahon
- **Año:** 2016
- **Publicación o institución:** Journal of International Economics, vol. 99, págs. S114-S133 (versión previa: CFM Discussion Paper 2015-37)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-09 Aprendizaje automático y análisis de texto para divisas (principal) · secundarias: —
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI: 10.1016/j.jinteco.2015.12.008 · https://wrap.warwick.ac.uk/85615/ · https://researchonline.lse.ac.uk/id/eprint/86247
- **Acceso y licencia:** Revista por suscripción; versiones en repositorios de Warwick y LSE
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Hansen McMahon "Shocking language: Understanding the macroeconomic effects of central bank communication" Journal of International Economics»; WebFetch: sí, WRAP (Warwick) y LSE Research Online)
- **Contenido:** Mide con lingüística computacional lo que el FOMC comunica sobre la situación actual y sobre la política futura, y estima con un FAVAR que la orientación prospectiva mueve más los mercados que la información sobre la coyuntura.
- **Uso en el Motor:** MC-06, MC-03: extracción de señales de orientación prospectiva de comunicados para TR-BCM y su traslación a diferenciales de tipos y divisas.
- **Limitaciones:** Centrado en la Fed; efectos reales débiles.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### DOC-MOT-0087 · Q 94 (A) — Random Forests

- **Autores:** Leo Breiman
- **Año:** 2001
- **Publicación o institución:** Machine Learning, 45(1), 5-32
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-09 Aprendizaje automático y análisis de texto para divisas (principal) · secundarias: —
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1023/A:1010933404324 · https://mlanthology.org/mlj/2001/breiman2001mlj-random
- **Acceso y licencia:** Artículo de pago en el editor (Springer); ficha bibliográfica abierta
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Breiman 2001 "Random Forests" Machine Learning 45 5-32»; WebFetch: sí)
- **Contenido:** Define los bosques aleatorios (agregación de árboles con remuestreo y selección aleatoria de variables), su error fuera de bolsa y la importancia de variables por permutación.
- **Uso en el Motor:** MC-06: bosques aleatorios para clasificar la dirección de pares y señales de régimen cambiario.
- **Limitaciones:** Importancia de variables sesgada con predictores correlacionados; el error fuera de bolsa no respeta la dependencia temporal.
- **Origen:** Reutilizada de F8 general V3.2 (TM-10, mismo ID) para el Bloque A Forex el 2026-11-02.

#### DOC-MOT-0400 · Q 94 (A) — Greedy Function Approximation: A Gradient Boosting Machine

- **Autores:** Jerome H. Friedman
- **Año:** 2001
- **Publicación o institución:** The Annals of Statistics, 29(5), 1189-1232
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-09 Aprendizaje automático y análisis de texto para divisas (principal) · secundarias: —
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.1214/aos/1013203451 · https://projecteuclid.org/euclid.aos/1013203451
- **Acceso y licencia:** Página del editor (Project Euclid) con resumen abierto; texto completo según suscripción
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Friedman 2001 "Greedy function approximation: A gradient boosting machine" Annals of Statistics»; WebFetch: sí)
- **Contenido:** Formula el boosting como descenso de gradiente en el espacio de funciones con pérdidas arbitrarias (cuadrática, absoluta, Huber, logística) y árboles de regresión como aprendices base; introduce la contracción (shrinkage) y los gráficos de dependencia parcial.
- **Uso en el Motor:** MC-06: boosting de gradiente para predicción de rendimientos cambiarios con predictores macro y de mercado.
- **Limitaciones:** Marco general; no aborda dependencia temporal ni no estacionariedad de datos financieros.
- **Origen:** Reutilizada de F8 general V3.2 (TM-10, mismo ID) para el Bloque A Forex el 2026-11-02.

#### DOC-MOT-0401 · Q 94 (A) — Regression Shrinkage and Selection via the Lasso

- **Autores:** Robert Tibshirani
- **Año:** 1996
- **Publicación o institución:** Journal of the Royal Statistical Society, Series B (Methodological), 58(1), 267-288
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-09 Aprendizaje automático y análisis de texto para divisas (principal) · secundarias: —
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1111/j.2517-6161.1996.tb02080.x · https://academicnewsletter.sufe.edu.cn/info/442374
- **Acceso y licencia:** Artículo de pago en el editor; copias docentes en abierto (p. ej., sites.stat.washington.edu)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Tibshirani 1996 "Regression shrinkage and selection via the lasso" Journal of the Royal Statistical Society Series B»; WebFetch: sí)
- **Contenido:** Propone el lasso: mínimos cuadrados con restricción en la norma L1 de los coeficientes, que contrae y anula coeficientes y realiza selección de variables continua.
- **Uso en el Motor:** MC-06: lasso para seleccionar fundamentos cambiarios (diferenciales de tipos, inflación, balanza) en predicción.
- **Limitaciones:** Selección inestable con predictores muy correlacionados (véase elastic net, DOC-MOT-0402); el número de volumen se toma de la cita estándar, la página leída solo mostraba páginas y DOI.
- **Origen:** Reutilizada de F8 general V3.2 (TM-10, mismo ID) para el Bloque A Forex el 2026-11-02.

#### DOC-MOT-0084 · Q 93 (A) — The Elements of Statistical Learning (2.ª ed.)

- **Autores:** Trevor Hastie; Robert Tibshirani; Jerome Friedman
- **Año:** 2009
- **Publicación o institución:** Springer (PDF gratuito de los autores en la Universidad de Stanford)
- **Tipo de documento:** Manual de referencia
- **Temática:** TMX-09 Aprendizaje automático y análisis de texto para divisas (principal) · secundarias: —
- **Calidad Q:** 93 (A) — Tipo 20/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://web.stanford.edu/~hastie/Papers/ESLII.pdf
- **Acceso y licencia:** PDF completo de acceso gratuito publicado por los autores; edición impresa de pago (Springer)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Hastie Tibshirani Friedman "The Elements of Statistical Learning" second edition pdf stanford»; WebFetch: no)
- **Contenido:** Manual de referencia del aprendizaje estadístico: regularización, árboles, boosting, métodos kernel, validación cruzada y descomposición sesgo-varianza.
- **Uso en el Motor:** MC-06: manual de referencia de aprendizaje estadístico (validación cruzada, regularización, árboles) aplicado a divisas.
- **Limitaciones:** Sin tratamiento específico de datos financieros dependientes ni de validación temporal. El DOI del libro que figuraba en la semilla no se ha visto en la verificación y se retira de la ficha.
- **Origen:** Reutilizada de F8 general V3.2 (TM-10, mismo ID) para el Bloque A Forex el 2026-11-02.

#### DOC-MOT-0402 · Q 93 (A) — Regularization and Variable Selection via the Elastic Net

- **Autores:** Hui Zou; Trevor Hastie
- **Año:** 2005
- **Publicación o institución:** Journal of the Royal Statistical Society, Series B (Statistical Methodology), 67(2), 301-320
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-09 Aprendizaje automático y análisis de texto para divisas (principal) · secundarias: —
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.1111/j.1467-9868.2005.00503.x · https://ideas.repec.org/a/bla/jorssb/v67y2005i2p301-320.html
- **Acceso y licencia:** Artículo de pago en el editor; ficha abierta en RePEc y copia docente en sites.stat.washington.edu
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Zou Hastie 2005 "Regularization and variable selection via the elastic net" JRSS B»; WebFetch: sí)
- **Contenido:** Combina penalizaciones L1 y L2 para seleccionar variables agrupando predictores correlacionados y funcionar cuando hay más variables que observaciones.
- **Uso en el Motor:** MC-06: red elástica con predictores cambiarios correlacionados (tipos y diferenciales a varios plazos).
- **Limitaciones:** Dos hiperparámetros a ajustar con validación respetuosa del orden temporal; existe una corrección publicada por los autores (web.stanford.edu).
- **Origen:** Reutilizada de F8 general V3.2 (TM-10, mismo ID) para el Bloque A Forex el 2026-11-02.

#### FXM-0261 · Q 92 (A) — Fundamentals and Exchange Rate Forecastability with Simple Machine Learning Methods

- **Autores:** Christophe Amat; Tomasz Michalski; Gilles Stoltz
- **Año:** 2018
- **Publicación o institución:** Journal of International Money and Finance, vol. 88, págs. 1-24 (versión previa: HAL halshs-01003914, 2014)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-09 Aprendizaje automático y análisis de texto para divisas (principal) · secundarias: TMX-08
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI: 10.1016/j.jimonfin.2018.06.003 · https://ideas.repec.org:443/a/eee/jimfin/v88y2018icp1-24.html · Versión abierta: https://halshs.archives-ouvertes.fr/halshs-01003914
- **Acceso y licencia:** Revista por suscripción; versión de trabajo en HAL
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Amat Michalski Stoltz "Fundamentals and exchange rate forecastability with simple machine learning methods" ideas.repec.org»; WebFetch: sí, ficha IDEAS)
- **Contenido:** Con regresión ridge secuencial y agregación con pesos exponenciales (con factores de descuento) sobre fundamentos de PPA, UIP y reglas de Taylor, supera al pronóstico sin cambio a un mes en divisas principales (1973-2014).
- **Uso en el Motor:** MC-06: aprendizaje secuencial en línea con fundamentos cambiarios; MC-10 para su evaluación frente al paseo aleatorio; AS-G10N.
- **Limitaciones:** Mejoras modestas; sensibles al factor de descuento.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### FXM-0262 · Q 91 (A) — Economic Fundamentals and Short-Run Exchange Rate Prediction: A Machine-Learning Perspective

- **Autores:** Ilias Filippou; David E. Rapach; Mark P. Taylor; Guofu Zhou
- **Año:** 2026
- **Publicación o institución:** Journal of Financial and Quantitative Analysis (publicado en la web de la revista en agosto de 2026); versión de trabajo relacionada: «Exchange Rate Prediction with Machine Learning and a Smart Carry Trade Portfolio», CEPR Discussion Paper 15305 (2020)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-09 Aprendizaje automático y análisis de texto para divisas (principal) · secundarias: TMX-06
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 5/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** https://jfqa.org/?p=10665 · https://ideas.repec.org/p/cpr/ceprdp/15305.html · https://repec.cepr.org/repec/cpr/ceprdp/DP15305.pdf
- **Acceso y licencia:** Versión de trabajo CEPR en abierto; PDF enlazado en la web de JFQA
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Filippou Rapach Taylor Zhou "Exchange rate prediction with machine learning and a smart carry portfolio"»; WebFetch: sí, web de JFQA y ficha IDEAS)
- **Contenido:** Usa unos 70 predictores (características por país, variables globales e interacciones) con red elástica y redes profundas: los fundamentos predicen a corto plazo cuando interactúan con la volatilidad cambiaria global y mejoran una cartera de carry («smart carry»).
- **Uso en el Motor:** MC-06: plantilla de predicción cambiaria de alta dimensión con interacciones de estado global; MC-09 para el carry condicionado; AS-ESTR y PROS.
- **Limitaciones:** Estado editorial exacto de la versión JFQA no confirmado (publicada en web, posible «forthcoming»); poca evidencia de no linealidad.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### DOC-MOT-0404 · Q 91 (A) — The Virtue of Complexity in Return Prediction

- **Autores:** Bryan T. Kelly; Semyon Malamud; Kangying Zhou
- **Año:** 2024
- **Publicación o institución:** The Journal of Finance, 79(1), 459-503
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-09 Aprendizaje automático y análisis de texto para divisas (principal) · secundarias: —
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 9/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1111/jofi.13298 · https://www.sfi.ch/en/publications/the-virtue-of-complexity-in-return-prediction
- **Acceso y licencia:** Artículo de pago; copia del artículo publicada en economics.yale.edu
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Kelly Malamud Zhou "The Virtue of Complexity in Return Prediction" Journal of Finance»; WebFetch: sí)
- **Contenido:** Demuestra teórica y empíricamente que modelos de predicción con más parámetros que observaciones (regresiones de características aleatorias con contracción) pueden mejorar el rendimiento fuera de muestra y el Sharpe de la estrategia de market timing.
- **Uso en el Motor:** MC-06: modelos de alta complejidad (características aleatorias) en predicción de rentabilidades, aplicables a carry y momentum cambiario.
- **Limitaciones:** Resultado debatido en la literatura posterior; sensible a la normalización y a la elección de la penalización; uno de los autores trabaja en la industria (AQR).
- **Origen:** Reutilizada de F8 general V3.2 (TM-10, mismo ID) para el Bloque A Forex el 2026-11-02.

#### FXM-0273 · Q 90 (A) — Measuring News Sentiment

- **Autores:** Adam Hale Shapiro; Moritz Sudhof; Daniel J. Wilson
- **Año:** 2017
- **Publicación o institución:** Federal Reserve Bank of San Francisco Working Paper 2017-01; versión de revista enlazada en ScienceDirect (pii S0304407620303535)
- **Tipo de documento:** Documento de trabajo (con versión de revista)
- **Temática:** TMX-09 Aprendizaje automático y análisis de texto para divisas (principal) · secundarias: —
- **Calidad Q:** 90 (A) — Tipo 22/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** https://www.frbsf.org/research-and-insights/publications/system-research-san-francisco-fed/2024/06/measuring-news-sentiment-eern · https://www.frbsf.org/wp-content/uploads/wp2017-01.pdf
- **Acceso y licencia:** Acceso abierto (Fed de San Francisco)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Shapiro Wilson "Taking the Fed at its Word" Review of Economic Studies; Shapiro Sudhof Wilson "Measuring news sentiment" Journal of Econometrics»; WebFetch: sí, página de la Fed de San Francisco)
- **Contenido:** Construye un índice diario de sentimiento económico a partir de noticias (1980-2015), compara modelos de análisis de sentimiento con valoraciones humanas y propone un léxico específico de noticias económicas.
- **Uso en el Motor:** MC-06: léxico y metodología de sentimiento de noticias para señales macro de TR-BCM y TR-PFV.
- **Limitaciones:** Noticias de EE. UU.; datos de la versión de revista (revista, volumen, páginas) no vistos.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### FXM-0269 · Q 90 (A) — Is Technical Analysis in the Foreign Exchange Market Profitable? A Genetic Programming Approach

- **Autores:** Christopher Neely; Paul Weller; Rob Dittmar
- **Año:** 1997
- **Publicación o institución:** Journal of Financial and Quantitative Analysis, vol. 32, n.º 4, págs. 405-426 (versiones previas: Fed de San Luis WP 1996-006; CEPR DP 1480)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-09 Aprendizaje automático y análisis de texto para divisas (principal) · secundarias: TMX-08
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 5/10 · Impacto 9/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** https://ideas.repec.org/a/cup/jfinqa/v32y1997i04p405-426_00.html · https://gpbib.cs.ucl.ac.uk/gp-html/neely_1997_JFQA.html · https://files.stlouisfed.org/files/htdocs/wp/1996/96-006.pdf
- **Acceso y licencia:** Revista por suscripción; documento de trabajo de la Fed de San Luis en abierto
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Neely Weller Dittmar 1997 "Is Technical Analysis in the Foreign Exchange Market Profitable? A Genetic Programming Approach"»; WebFetch: sí, ficha IDEAS y GP Bibliography)
- **Contenido:** Descubre reglas técnicas cambiarias mediante programación genética; obtiene excesos de rentabilidad fuera de muestra en seis tipos de cambio (1981-1995) no explicados por riesgo sistemático.
- **Uso en el Motor:** MC-06: búsqueda automática de reglas cambiarias con control fuera de muestra; MC-10 para su validación (Reality Check/SPA).
- **Limitaciones:** Muestra anterior a la decadencia documentada en FXM-0247.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### DOC-MOT-0090 · Q 89 (A) — On Calibration of Modern Neural Networks

- **Autores:** Chuan Guo; Geoff Pleiss; Yu Sun; Kilian Q. Weinberger
- **Año:** 2017
- **Publicación o institución:** Proceedings of the 34th International Conference on Machine Learning (ICML 2017), PMLR 70, 1321-1330
- **Tipo de documento:** Comunicación de congreso revisada por pares
- **Temática:** TMX-09 Aprendizaje automático y análisis de texto para divisas (principal) · secundarias: TMX-08
- **Calidad Q:** 89 (A) — Tipo 20/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** https://proceedings.mlr.press/v70/guo17a.html (preprint: arXiv 1706.04599)
- **Acceso y licencia:** Acceso abierto (PMLR y arXiv)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Guo Pleiss Sun Weinberger "On Calibration of Modern Neural Networks" ICML 2017 PMLR»; WebFetch: sí)
- **Contenido:** Muestra que las redes neuronales profundas están mal calibradas, define el error de calibración esperado (ECE) y propone el escalado de temperatura como corrección simple y eficaz.
- **Uso en el Motor:** MC-06: escalado de temperatura y diagnóstico de calibración en redes neuronales aplicadas a divisas.
- **Limitaciones:** Centrado en clasificación de imágenes y texto; no aborda el desplazamiento de distribución típico de los mercados.
- **Origen:** Reutilizada de F8 general V3.2 (TM-10, mismo ID) para el Bloque A Forex el 2026-11-02.

#### DOC-MOT-0406 · Q 88 (A) — A Unified Approach to Interpreting Model Predictions

- **Autores:** Scott M. Lundberg; Su-In Lee
- **Año:** 2017
- **Publicación o institución:** Advances in Neural Information Processing Systems 30 (NIPS 2017)
- **Tipo de documento:** Comunicación de congreso revisada por pares
- **Temática:** TMX-09 Aprendizaje automático y análisis de texto para divisas (principal) · secundarias: —
- **Calidad Q:** 88 (A) — Tipo 20/25 · Rigor 16/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 9/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://papers.nips.cc/paper/7062-a (preprint: arXiv 1705.07874)
- **Acceso y licencia:** Acceso abierto (actas NeurIPS y arXiv)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Lundberg Lee 2017 "A Unified Approach to Interpreting Model Predictions" NeurIPS»; WebFetch: sí)
- **Contenido:** Propone SHAP: atribución aditiva de la predicción a cada variable basada en valores de Shapley, con propiedades de unicidad y aproximaciones eficientes (Kernel SHAP).
- **Uso en el Motor:** MC-06: valores SHAP para explicar qué fundamentos o señales impulsan un pronóstico cambiario.
- **Limitaciones:** Atribuciones engañosas con variables correlacionadas; coste computacional; explica el modelo, no la causalidad.
- **Origen:** Reutilizada de F8 general V3.2 (TM-10, mismo ID) para el Bloque A Forex el 2026-11-02.

#### DOC-MOT-0088 · Q 88 (A) — XGBoost: A Scalable Tree Boosting System

- **Autores:** Tianqi Chen; Carlos Guestrin
- **Año:** 2016
- **Publicación o institución:** Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (KDD '16), ACM
- **Tipo de documento:** Comunicación de congreso revisada por pares
- **Temática:** TMX-09 Aprendizaje automático y análisis de texto para divisas (principal) · secundarias: —
- **Calidad Q:** 88 (A) — Tipo 20/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI: 10.1145/2939672.2939785 · https://arxiv.org/abs/1603.02754
- **Acceso y licencia:** Preprint de acceso abierto en arXiv; versión de actas en ACM
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Chen Guestrin "XGBoost: A Scalable Tree Boosting System" KDD 2016 arXiv»; WebFetch: sí)
- **Contenido:** Describe XGBoost: boosting de árboles con regularización explícita, algoritmo consciente de la dispersión, bosquejo de cuantiles ponderado y diseño de sistema escalable.
- **Uso en el Motor:** MC-06: implementación eficiente de boosting (XGBoost) para modelos cambiarios con datos de panel de divisas.
- **Limitaciones:** Riesgo de sobreajuste sin validación temporal; artículo de sistema, no de inferencia.
- **Origen:** Reutilizada de F8 general V3.2 (TM-10, mismo ID) para el Bloque A Forex el 2026-11-02.

#### DOC-MOT-0089 · Q 87 (A) — Predicting Good Probabilities with Supervised Learning

- **Autores:** Alexandru Niculescu-Mizil; Rich Caruana
- **Año:** 2005
- **Publicación o institución:** Proceedings of the 22nd International Conference on Machine Learning (ICML 2005), ACM, 625-632
- **Tipo de documento:** Comunicación de congreso revisada por pares
- **Temática:** TMX-09 Aprendizaje automático y análisis de texto para divisas (principal) · secundarias: TMX-08
- **Calidad Q:** 87 (A) — Tipo 20/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI: 10.1145/1102351.1102430 · https://mlanthology.org/icml/2005/niculescumizil2005icml-predicting
- **Acceso y licencia:** Ficha abierta en ML Anthology; texto en ACM Digital Library
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Niculescu-Mizil Caruana 2005 "Predicting good probabilities with supervised learning" ICML»; WebFetch: sí)
- **Contenido:** Evalúa la calibración de las probabilidades de diez clasificadores y muestra cómo corregirla con escalado de Platt y regresión isotónica.
- **Uso en el Motor:** MC-06: calibración de probabilidades de dirección cambiaria antes de congelar pronósticos PRG- en F4.
- **Limitaciones:** Datos no financieros; la isotónica sobreajusta con muestras pequeñas.
- **Origen:** Reutilizada de F8 general V3.2 (TM-10, mismo ID) para el Bloque A Forex el 2026-11-02.

#### FXM-0266 · Q 84 (A) — Statistical Learning and Exchange Rate Forecasting

- **Autores:** E. Colombo; M. Pelagatti
- **Año:** 2020
- **Publicación o institución:** International Journal of Forecasting, vol. 36, n.º 4, págs. 1260-1289
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-09 Aprendizaje automático y análisis de texto para divisas (principal) · secundarias: TMX-08
- **Calidad Q:** 84 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 5/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** https://ideas.repec.org:443/a/eee/jimfin/v88y2018icp1-24.html (índice)
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Amat Michalski Stoltz "Fundamentals and exchange rate forecastability with simple machine learning methods" ideas.repec.org»; WebFetch: sí, índice: ficha IDEAS de Amat, Michalski y Stoltz (2018), listas de referencias, citas y «Most related items», https://ideas.repec.org:443/a/eee/jimfin/v88y2018icp1-24.html)
- **Contenido:** Compara métodos de aprendizaje estadístico con fundamentos para pronosticar tipos de cambio frente al paseo aleatorio.
- **Uso en el Motor:** MC-06: comparativa de métodos de aprendizaje estadístico para divisas; MC-10.
- **Limitaciones:** Confirmada solo por índice; nombres completos y DOI no vistos.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### FXM-0274 · Q 83 (A) — Answering the Queen: Machine Learning and Financial Crises

- **Autores:** J. Fouliard; M. Howell; H. Rey; V. Stavrakeva
- **Año:** 2020
- **Publicación o institución:** NBER Working Paper 28302
- **Tipo de documento:** Documento de trabajo
- **Temática:** TMX-09 Aprendizaje automático y análisis de texto para divisas (principal) · secundarias: TMX-07
- **Calidad Q:** 83 (A) — Tipo 20/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 6/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** https://ideas.repec.org:443/a/eee/jimfin/v88y2018icp1-24.html (índice)
- **Acceso y licencia:** Acceso abierto
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Amat Michalski Stoltz "Fundamentals and exchange rate forecastability with simple machine learning methods" ideas.repec.org»; WebFetch: sí, índice: ficha IDEAS de Amat, Michalski y Stoltz (2018), listas de referencias, citas y «Most related items», https://ideas.repec.org:443/a/eee/jimfin/v88y2018icp1-24.html)
- **Contenido:** Aplica aprendizaje en línea con agregación de predictores para anticipar crisis financieras sistémicas en tiempo real.
- **Uso en el Motor:** MC-06, MC-07: sistemas de alerta temprana con aprendizaje en línea aplicables a crisis cambiarias de emergentes (AS-EMLA, AS-EMEA, AS-EMAS).
- **Limitaciones:** Confirmada solo por índice; crisis financieras en general, no solo cambiarias.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### DOC-MOT-0085 · Q 83 (A) — Advances in Financial Machine Learning

- **Autores:** Marcos López de Prado
- **Año:** 2018
- **Publicación o institución:** John Wiley & Sons
- **Tipo de documento:** Libro académico-profesional
- **Temática:** TMX-09 Aprendizaje automático y análisis de texto para divisas (principal) · secundarias: TMX-08
- **Calidad Q:** 83 (A) — Tipo 20/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 8/10 · Acceso 5/10
- **DOI / ISBN / URL:** ISBN: 978-1-119-48208-6 · https://www.wiley-vch.de/en/areas-interest/finance-economics-law/advances-in-financial-machine-learning-978-1-119-48208-6
- **Acceso y licencia:** Libro de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «López de Prado "Advances in Financial Machine Learning" Wiley 2018 ISBN 978-1-119-48208-6»; WebFetch: no)
- **Contenido:** Manual práctico de aprendizaje automático financiero: barras de información, etiquetado por triple barrera, metaetiquetado, diferenciación fraccional, validación cruzada purgada con embargo, importancia de variables y sobreajuste de backtest.
- **Uso en el Motor:** MC-06: etiquetado, validación cruzada purgada y ponderación por unicidad en series cambiarias de alta frecuencia.
- **Limitaciones:** Algunas propuestas con evidencia empírica limitada; autor vinculado a la industria.
- **Origen:** Reutilizada de F8 general V3.2 (TM-10, mismo ID) para el Bloque A Forex el 2026-11-02.

#### FXM-0264 · Q 80 (A) — The Predictability of the Exchange Rate When Combining Machine Learning and Fundamental Models

- **Autores:** Yuchen Zhang; Shigeyuki Hamori
- **Año:** 2020
- **Publicación o institución:** Journal of Risk and Financial Management (MDPI), vol. 13, n.º 3, art. 48
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-09 Aprendizaje automático y análisis de texto para divisas (principal) · secundarias: TMX-08
- **Calidad Q:** 80 (A) — Tipo 22/25 · Rigor 13/20 · Autoridad 10/15 · Vigencia 10/10 · Impacto 5/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://ideas.repec.org/a/gam/jjrfmx/v13y2020i3p48-d328353.html
- **Acceso y licencia:** Acceso abierto (MDPI)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Amat Michalski Stoltz "Fundamentals and exchange rate forecastability with simple machine learning methods" ideas.repec.org»; WebFetch: sí, ficha IDEAS)
- **Contenido:** Combina bosques aleatorios, máquinas de vectores soporte y redes neuronales con fundamentos de UIP, PPA, modelo monetario y reglas de Taylor; por RMSE superan al paseo aleatorio, con resultados mixtos en Diebold-Mariano.
- **Uso en el Motor:** MC-06: híbridos fundamentos + aprendizaje automático; MC-10 para su evaluación con DM.
- **Limitaciones:** Revista de menor impacto; robustez limitada.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### FXM-0267 · Q 80 (A) — Forecasting Daily and Monthly Exchange Rates with Machine Learning Techniques

- **Autores:** V. Plakandaras; T. Papadimitriou; P. Gogas
- **Año:** 2015
- **Publicación o institución:** Journal of Forecasting, vol. 34, n.º 7, págs. 560-573
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-09 Aprendizaje automático y análisis de texto para divisas (principal) · secundarias: TMX-08
- **Calidad Q:** 80 (A) — Tipo 25/25 · Rigor 14/20 · Autoridad 12/15 · Vigencia 9/10 · Impacto 6/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** https://ideas.repec.org:443/a/eee/jimfin/v88y2018icp1-24.html (índice)
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Amat Michalski Stoltz "Fundamentals and exchange rate forecastability with simple machine learning methods" ideas.repec.org»; WebFetch: sí, índice: ficha IDEAS de Amat, Michalski y Stoltz (2018), listas de referencias, citas y «Most related items», https://ideas.repec.org:443/a/eee/jimfin/v88y2018icp1-24.html)
- **Contenido:** Combina descomposición de señales con máquinas de vectores soporte y redes neuronales para pronosticar tipos de cambio diarios y mensuales.
- **Uso en el Motor:** MC-06: modelos híbridos de descomposición + aprendizaje automático para pares cambiarios.
- **Limitaciones:** Confirmada solo por índice; DOI no visto.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### FXM-0263 · Q 79 (B) — Information Spillover and Cross-Predictability of Currency Returns: An Analysis via Machine Learning

- **Autores:** Jia; Liu; Wu; Yan (nombres no vistos en el índice)
- **Año:** 2024
- **Publicación o institución:** Journal of Banking & Finance, vol. 169
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-09 Aprendizaje automático y análisis de texto para divisas (principal) · secundarias: TMX-06
- **Calidad Q:** 79 (B) — Tipo 25/25 · Rigor 14/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 3/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** https://ideas.repec.org/p/cpr/ceprdp/15305.html (índice)
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Filippou Rapach Taylor Zhou "Exchange rate prediction with machine learning and a smart carry portfolio"»; WebFetch: sí, índice: ficha IDEAS de CEPR DP 15305, lista «Most related items», https://ideas.repec.org/p/cpr/ceprdp/15305.html)
- **Contenido:** Aplica aprendizaje automático para explotar la predictibilidad cruzada entre rendimientos de distintas divisas (contagio informativo).
- **Uso en el Motor:** MC-06: predictores cruzados entre divisas en modelos de alta dimensión; AS-ESTR.
- **Limitaciones:** Confirmada solo por índice; autoría completa, páginas y DOI no vistos.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### FXM-0265 · Q 78 (B) — Exchange Rate Forecasting with Advanced Machine Learning Methods

- **Autores:** J. F. Pfahler
- **Año:** 2022
- **Publicación o institución:** Journal of Risk and Financial Management (MDPI), vol. 15, n.º 1, art. 2
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-09 Aprendizaje automático y análisis de texto para divisas (principal) · secundarias: TMX-08
- **Calidad Q:** 78 (B) — Tipo 22/25 · Rigor 14/20 · Autoridad 9/15 · Vigencia 10/10 · Impacto 3/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** DOI: 10.3390/jrfm15010002 · https://mdpi.com/1911-8074/15/1/2
- **Acceso y licencia:** Acceso abierto (MDPI, CC BY)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Amat Michalski Stoltz "Fundamentals and exchange rate forecastability with simple machine learning methods" ideas.repec.org»; WebFetch: sí, página MDPI)
- **Contenido:** Redes neuronales y XGBoost con fundamentos (PPA, UIP, monetario) en 10 pares OCDE frente al USD: no baten al paseo aleatorio en niveles, sí en dirección, pero la ventaja depende de variables temporales ficticias.
- **Uso en el Motor:** MC-06: advertencia sobre la fuente real de la mejora (efectos temporales) en clasificadores de dirección cambiaria; MC-10.
- **Limitaciones:** Autor único, revista de menor impacto.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### FXM-0268 · Q 76 (B) — Should Economic Theories Guide the Machine Learning Model in Forecasting Exchange Rates?

- **Autores:** Lin; Liu; Vincent (nombres no vistos en el índice)
- **Año:** 2025
- **Publicación o institución:** Economic Modelling, vol. 151
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TMX-09 Aprendizaje automático y análisis de texto para divisas (principal) · secundarias: —
- **Calidad Q:** 76 (B) — Tipo 25/25 · Rigor 13/20 · Autoridad 12/15 · Vigencia 10/10 · Impacto 2/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** https://ideas.repec.org:443/a/eee/jimfin/v88y2018icp1-24.html (índice)
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Amat Michalski Stoltz "Fundamentals and exchange rate forecastability with simple machine learning methods" ideas.repec.org»; WebFetch: sí, índice: ficha IDEAS de Amat, Michalski y Stoltz (2018), listas de referencias, citas y «Most related items», https://ideas.repec.org:443/a/eee/jimfin/v88y2018icp1-24.html)
- **Contenido:** Evalúa si imponer estructura de teoría económica (fundamentos) mejora los modelos de aprendizaje automático para tipos de cambio.
- **Uso en el Motor:** MC-06: diseño de modelos con restricciones teóricas frente a modelos libres; PROS.
- **Limitaciones:** Confirmada solo por índice; autoría completa, páginas y DOI no vistos.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

#### FXM-0270 · Q 58 (C) — Graph Learning for FX Rate Prediction and Statistical Arbitrage

- **Autores:** Hong; Klabjan (nombres no vistos en el índice)
- **Año:** 2025
- **Publicación o institución:** arXiv:2508.14784 (preprint)
- **Tipo de documento:** Preprint
- **Temática:** TMX-09 Aprendizaje automático y análisis de texto para divisas (principal) · secundarias: —
- **Calidad Q:** 58 (C) — Tipo 12/25 · Rigor 10/20 · Autoridad 8/15 · Vigencia 10/10 · Impacto 2/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** https://ideas.repec.org:443/a/eee/jimfin/v88y2018icp1-24.html (índice)
- **Acceso y licencia:** Acceso abierto
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Amat Michalski Stoltz "Fundamentals and exchange rate forecastability with simple machine learning methods" ideas.repec.org»; WebFetch: sí, índice: ficha IDEAS de Amat, Michalski y Stoltz (2018), listas de referencias, citas y «Most related items», https://ideas.repec.org:443/a/eee/jimfin/v88y2018icp1-24.html)
- **Contenido:** Aplica aprendizaje sobre grafos (relaciones entre divisas) a la predicción de tipos de cambio y al arbitraje estadístico.
- **Uso en el Motor:** MC-06: exploración de modelos de grafos para cestas de divisas; uso solo experimental.
- **Limitaciones:** Preprint sin revisión por pares; confirmado solo por índice.
- **Origen:** Alta nueva de DOC-M (Bloque A Forex) el 2026-11-02.

## Lagunas de cobertura

Áreas con menos de 20 referencias verificadas tras la emisión V1.0 del 02/11/2026 (objetivo del propietario: 20–50 por área):

| Código | Temática | Verificadas | Faltan para 20 |
|---|---|---|---|
| — | Ninguna | — | — |

## Registro de bajas

| REF-id | Título | Motivo | Fecha | Sustituta |
|---|---|---|---|---|

## Historial de versión

| Versión | Fecha | Cambio |
|---|---|---|
| V1.0 | 02/11/2026 | Emisión inicial del archivo específico de divisas del Bloque A Forex: 244 fichas (reutilizadas del Bloque A general V3.2 con su ID original, y nuevas verificadas por búsqueda web con prefijo FX); 0 bajas; orden por temática y Q; índice con recuento de verificadas. |

