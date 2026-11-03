# Archivo operativo F8 — Documentación para el Motor de Cálculo Avanzado

**Bloque A · Robot Investor · Versión óptima V4.0 · 01/11/2026** · Subordinado al Documento 0 óptima V5.0.

**Versión del archivo:** V3.2 (01/11/2026), alineada con el Documento 0 óptima V5.0 · **Código:** F8 · **Propietario:** AG-15 Documentador para el Motor de Cálculo Avanzado (DOC-M) · **Alcance:** ecosistémico (lo reutilizan los bloques posteriores)

## Cómo usar este archivo

**Propósito.** Fondo de referencias de métodos cuantitativos (estadística, series temporales, econometría, valoración, derivados, carteras, riesgo, simulación, aprendizaje automático, evaluación predictiva y métricas por clase) que respalda cada servicio del Motor (MC-01 a MC-10) y la evaluación de pronósticos.

**Propietario y acceso.** Escribe solo AG-15 (DOC-M). Leen: AG-13 Motor, AG-14, Orquestador, Auditor y Evaluador. Cualquier otro acceso es una incidencia (Documento 0, 5.2).

**Reglas de uso.**

1. **Lectura.** Lea primero «Novedades»; después el índice de temáticas; dentro de la temática, las fichas aparecen **ordenadas por Q descendente** (a igualdad, la más reciente primero). Cite siempre el ID de la ficha. Para corroboración (PS1) solo cuentan fichas de nivel A o B con `Estado del enlace` distinto de `ROTO`; una ficha `PENDIENTE_VERIFICACION_ALTA` no sustenta evidencia hasta que su propietario la confirme.
2. **Calidad.** Q (0–100) con la rúbrica 13.3: Tipo y revisión 25 · Rigor y transparencia 20 · Autoridad 15 · Vigencia 10 · Impacto 10 · Independencia 10 · Accesibilidad y estabilidad 10. Niveles: A (Q ≥ 80), B (65–79), C (50–64), D (< 50: candidata a baja salvo que sea la única fuente de un dato necesario, declarado). En las semillas la Q es provisional hasta la verificación de alta.
3. **Estados del enlace** (HT-02, barrido semanal del domingo): `OK`, `REDIRIGIDO`, `ROTO` (4xx/5xx en dos intentos separados 24 h), `MURO_PAGO`, `CONTENIDO_CAMBIADO` (similitud < 0,8 frente a la copia archivada) y `PENDIENTE_BARRIDO` (estado inicial de esta versión: ningún enlace se ha comprobado aún con HT-02). `Última verificación` recoge la última comprobación documentada, no una del barrido.
4. **Acciones** (potestad plena del propietario, R19): `REPARAR` (DOI, nueva URL oficial o copia archivada; obligatoria cuando la ficha lleva «Alerta»); `DEGRADAR` (bajar Q o nivel, con motivo); `BORRAR` cuando haya enlace roto sin alternativa tras dos barridos, contenido retirado o retractado, falsedad o manipulación demostrada, redundancia total con una ficha de mayor Q, o Q < 50 sin uso en 180 días. Cada borrado añade una línea al «Registro de bajas»; si la ficha sustentaba EVD de F2 se avisa al Curador (CT-11, tipo `fuente_retirada`).
5. **Ciclo.** DOC-M alimenta el archivo por su agenda de vigilancia y por las peticiones del Motor (CT-20); antes de buscar aplica el Fondo metodológico (R20). El Motor cita el ID de la ficha en el artefacto de cada cálculo (RC). Mensualmente el propietario informa al Orquestador de altas, reparaciones, bajas, salud de enlaces y lagunas (CT-21). Los IDs son inmutables y no se reutilizan; en el «Registro de bajas», «REF-id» es el ID propio de la ficha.

**Semillas.** Las fichas con `Estado: PENDIENTE_VERIFICACION_ALTA` son obras canónicas añadidas en V3.0 para cubrir lagunas evidentes. Sus identificadores (DOI, ISBN, URL) proceden de conocimiento previo y llevan la marca «a verificar»: no están verificadas y no pueden citarse como respaldo de un cálculo hasta que DOC-M las confirme con HT-02.

## Índice de temáticas (Anexo D, TM-)

| Código | Temática | Referencias | Verificadas | Pendientes de verificación | A | B | C | D | Q medio |
|---|---|---|---|---|---|---|---|---|---|
| TM-01 | Estadística e inferencia | 22 | 22 | 0 | 21 | 1 | 0 | 0 | 91,2 |
| TM-02 | Series temporales y detección de tendencias | 26 | 26 | 0 | 22 | 4 | 0 | 0 | 87,6 |
| TM-03 | Volatilidad y regímenes | 30 | 30 | 0 | 29 | 1 | 0 | 0 | 91,0 |
| TM-04 | Econometría y causalidad | 29 | 29 | 0 | 28 | 1 | 0 | 0 | 90,7 |
| TM-05 | Valoración de activos y estructura temporal | 26 | 26 | 0 | 25 | 1 | 0 | 0 | 89,8 |
| TM-06 | Derivados y volatilidad implícita | 27 | 27 | 0 | 25 | 2 | 0 | 0 | 89,3 |
| TM-07 | Modelos factoriales y carteras | 28 | 28 | 0 | 28 | 0 | 0 | 0 | 92,9 |
| TM-08 | Riesgo y valores extremos | 26 | 26 | 0 | 26 | 0 | 0 | 0 | 91,8 |
| TM-09 | Simulación y métodos numéricos | 26 | 26 | 0 | 26 | 0 | 0 | 0 | 90,7 |
| TM-10 | Aprendizaje automático para finanzas | 22 | 22 | 0 | 20 | 2 | 0 | 0 | 87,9 |
| TM-11 | Evaluación predictiva y backtesting | 28 | 27 | 1 | 26 | 2 | 0 | 0 | 88,7 |
| TM-12 | Crecimiento, difusión y prospectiva cuantitativa | 27 | 26 | 1 | 26 | 1 | 0 | 0 | 87,0 |
| TM-13 | Métricas específicas por clase (cripto en cadena, inmobiliario, privados) | 24 | 20 | 4 | 21 | 3 | 0 | 0 | 86,7 |
| TM-14 | Datos, calidad y reproducibilidad | 23 | 20 | 3 | 23 | 0 | 0 | 0 | 88,4 |
| TM-15 | Índices: construcción, rebalanceo y rentabilidad esperada | 24 | 24 | 0 | 22 | 2 | 0 | 0 | 87,5 |
| TM-16 | Vehículos: descuentos, réplica y ETF apalancados | 26 | 26 | 0 | 21 | 5 | 0 | 0 | 85,8 |
| TM-17 | Mercado monetario: rentabilidades equivalentes y expectativas implícitas | 23 | 23 | 0 | 22 | 1 | 0 | 0 | 86,2 |
| TM-18 | Crédito, inflación implícita y volatilidad como factores | 27 | 27 | 0 | 26 | 1 | 0 | 0 | 89,0 |
| **Total** | — | **464** | **455** | 9 | 437 | 27 | 0 | 0 | 89,1 |

«Verificadas»: enlace en estado OK, REDIRIGIDO, MURO_PAGO o VERIFICADO_BUSQUEDA (existencia y datos confirmados por búsqueda web el 02/11/2026), o verificación documental completa en una carga anterior (25–26/10/2026), pendiente solo del barrido automático HT-02. «Pendientes»: semillas aún en PENDIENTE_VERIFICACION_ALTA o fichas con alerta sin resolver.

## Novedades

Sección de difusión semanal (Documento 0, 6.1): el propietario anota aquí las altas, reparaciones, degradaciones y bajas de la semana; los agentes lectores la consultan al inicio de cada encargo mediante HT-06. Se conservan las cuatro últimas semanas; lo anterior queda en el historial del archivo.

| Semana (lunes) | Tipo | ID | Temática | Resumen (una línea) |
|---|---|---|---|---|

Tipos admitidos: `ALTA`, `REPARACION`, `DEGRADACION`, `RECALIFICACION`, `BAJA`, `VERIFICACION_ALTA` (semilla confirmada o rechazada).

## TM-01 Estadística e inferencia

#### DOC-MOT-0261 · Q 96 (A) — Statistical Significance for Genomewide Studies

- **Autores:** John D. Storey; Robert Tibshirani
- **Año:** 2003
- **Publicación o institución:** Proceedings of the National Academy of Sciences, 100(16), 9440-9445
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-01 Estadística e inferencia (principal) · secundarias: —
- **Calidad Q:** 96 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** DOI: 10.1073/pnas.1530509100 · Verificada en página índice: https://en.wikipedia.org/wiki/Q-value_(statistics) (PMC170937)
- **Acceso y licencia:** Acceso abierto (PubMed Central)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «False discovery rate wikipedia Benjamini Yekutieli 2001 Storey 2002 q-value Holm»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Q-value_(statistics))
- **Contenido:** Procedimiento práctico de q-valores con estimación de π0 por suavizado, ilustrado con miles de contrastes simultáneos.
- **Uso en el Motor:** MC-01: receta operativa de q-valores aplicable a cribas masivas de señales.
- **Limitaciones:** Ejemplos genómicos, no financieros. Confirmada solo mediante página índice (bibliografía de Wikipedia «Q-value (statistics)»); pendiente de lectura de la fuente primaria.

#### DOC-MOT-0259 · Q 96 (A) — A Direct Approach to False Discovery Rates

- **Autores:** John D. Storey
- **Año:** 2002
- **Publicación o institución:** Journal of the Royal Statistical Society, Series B, 64(3), 479-498
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-01 Estadística e inferencia (principal) · secundarias: TM-11
- **Calidad Q:** 96 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI: 10.1111/1467-9868.00346 · https://www.stat.cmu.edu/~ryantibs/journalclub/storey_2002.pdf
- **Acceso y licencia:** Copia docente (Carnegie Mellon) de lectura; revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «False discovery rate wikipedia Benjamini Yekutieli 2001 Storey 2002 q-value Holm»; WebFetch: sí)
- **Contenido:** Fija la región de rechazo y estima la FDR resultante; introduce la pFDR, el q-valor y la estimación de la proporción de nulas verdaderas (π0) para ganar potencia frente a Benjamini-Hochberg.
- **Uso en el Motor:** MC-01, MC-10: q-valores al cribar muchas señales o estrategias.
- **Limitaciones:** Estimación de π0 sensible al parámetro de ajuste; supuestos de independencia débil. DOI tomado de la página índice https://en.wikipedia.org/wiki/Q-value_(statistics).

#### DOC-MOT-0016 · Q 96 (A) — The Jackknife and the Bootstrap for General Stationary Observations

- **Autores:** Hans R. Künsch
- **Año:** 1989
- **Publicación o institución:** The Annals of Statistics, 17(3), 1217-1241 (Institute of Mathematical Statistics)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-01 Estadística e inferencia (principal) · secundarias: TM-02, TM-09
- **Calidad Q:** 96 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** DOI: 10.1214/aos/1176347265 · https://projecteuclid.org/journals/annals-of-statistics/volume-17/issue-3/The-Jackknife-and-the-Bootstrap-for-General-Stationary-Observations/10.1214/aos/1176347265.full
- **Acceso y licencia:** Acceso abierto en Project Euclid (marcado «Open Access»); copyright IMS
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Künsch 1989 "The Jackknife and the Bootstrap for General Stationary Observations" Annals of Statistics»; WebFetch: sí)
- **Contenido:** Introduce el bootstrap y el jackknife por bloques móviles para observaciones estacionarias dependientes y demuestra su consistencia para la media y funcionales suaves de la distribución empírica m-dimensional.
- **Uso en el Motor:** MC-01, MC-10: bootstrap por bloques móviles para series dependientes (intervalos de Sharpe, métricas de backtesting).
- **Limitaciones:** Elección de longitud de bloque; bloques fijos generan no estacionariedad de la serie remuestreada (véase bootstrap estacionario, DOC-MOT-0080).
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02 (metadatos y DOI coincidentes).

#### DOC-MOT-0260 · Q 95 (A) — The Positive False Discovery Rate: A Bayesian Interpretation and the q-Value

- **Autores:** John D. Storey
- **Año:** 2003
- **Publicación o institución:** The Annals of Statistics, 31(6), 2013-2035
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-01 Estadística e inferencia (principal) · secundarias: TM-11
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI: 10.1214/aos/1074290335 · Verificada en página índice: https://en.wikipedia.org/wiki/Q-value_(statistics)
- **Acceso y licencia:** Project Euclid (IMS)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «False discovery rate wikipedia Benjamini Yekutieli 2001 Storey 2002 q-value Holm»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Q-value_(statistics))
- **Contenido:** Interpreta la pFDR como probabilidad posterior de nula verdadera dada la región de rechazo y fundamenta el q-valor como análogo bayesiano del p-valor.
- **Uso en el Motor:** MC-01: lectura probabilística de los q-valores en informes.
- **Limitaciones:** Confirmada solo mediante página índice (bibliografía de Wikipedia «Q-value (statistics)»); pendiente de lectura de la fuente primaria.

#### DOC-MOT-0017 · Q 95 (A) — Controlling the False Discovery Rate: A Practical and Powerful Approach to Multiple Testing

- **Autores:** Yoav Benjamini; Yosef Hochberg
- **Año:** 1995
- **Publicación o institución:** Journal of the Royal Statistical Society, Series B (Methodological), 57(1), 289-300
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-01 Estadística e inferencia (principal) · secundarias: TM-11
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1111/j.2517-6161.1995.tb02031.x · https://cris.tau.ac.il/en/publications/controlling-the-false-discovery-rate-a-practical-and-powerful-app-2/
- **Acceso y licencia:** Ficha institucional (Universidad de Tel Aviv) con metadatos; texto en la editorial (Oxford Academic/Wiley, suscripción)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Benjamini Hochberg 1995 Controlling the False Discovery Rate practical powerful approach multiple testing JRSS B»; WebFetch: sí)
- **Contenido:** Define la tasa de falsos descubrimientos (FDR) y el procedimiento escalonado de Benjamini-Hochberg (ordenar p-valores y rechazar hasta el mayor k con p(k) ≤ kq/m), que controla la FDR con contrastes independientes y es más potente que los métodos FWER.
- **Uso en el Motor:** MC-01, MC-10: corrección por contraste múltiple al cribar muchas señales o estrategias.
- **Limitaciones:** Garantía bajo independencia o dependencia positiva (PRDS); con dependencia arbitraria usar la variante de Benjamini-Yekutieli.
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02 (metadatos y DOI coincidentes).

#### DOC-MOT-0015 · Q 95 (A) — Bootstrap Methods: Another Look at the Jackknife

- **Autores:** Bradley Efron
- **Año:** 1979
- **Publicación o institución:** The Annals of Statistics, 7(1), 1-26 (Rietz Lecture 1977)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-01 Estadística e inferencia (principal) · secundarias: TM-09
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** https://sites.stat.washington.edu/courses/stat527/s13/readings/ann_stat1979.pdf · Project Euclid: https://projecteuclid.org:443/euclid.aos/1176344552 (DOI no visto en la verificación)
- **Acceso y licencia:** Copia en página docente de la Universidad de Washington (lectura); registro en Project Euclid; copyright IMS
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Efron 1979 "Bootstrap Methods: Another Look at the Jackknife" Annals of Statistics projecteuclid»; WebFetch: sí, sobre la copia de washington.edu)
- **Contenido:** Artículo fundacional del bootstrap: estimación de la distribución muestral de un estadístico remuestreando con reemplazo la distribución empírica, y su relación con el jackknife.
- **Uso en el Motor:** MC-01: fundamento del remuestreo (errores estándar e intervalos de estadísticos no estándar).
- **Limitaciones:** Supuesto i.i.d.; para series dependientes usar variantes por bloques (DOC-MOT-0016, DOC-MOT-0080).
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02; el DOI provisional de la semilla no se ha visto y se retira hasta confirmarlo.

#### DOC-MOT-0272 · Q 94 (A) — Estimating the Dimension of a Model

- **Autores:** Gideon Schwarz
- **Año:** 1978
- **Publicación o institución:** The Annals of Statistics, 6(2), 461-464
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-01 Estadística e inferencia (principal) · secundarias: TM-02, TM-04
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** Verificada en página índice: https://cran.r-universe.dev/lpirfs/doc/manual.html
- **Acceso y licencia:** Project Euclid (IMS)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Jordà 2005 "Estimation and Inference of Impulse Responses by Local Projections" American Economic Review 95»; WebFetch: sí, sobre la página índice https://cran.r-universe.dev/lpirfs/doc/manual.html)
- **Contenido:** Criterio bayesiano de información (BIC/SIC), consistente para el orden verdadero del modelo.
- **Uso en el Motor:** MC-01, MC-02: selección de orden y de número de rupturas (BIC en Bai-Perron).
- **Limitaciones:** Confirmada solo mediante página índice (bibliografía de manual de lpirfs); pendiente de lectura de la fuente primaria.

#### DOC-MOT-0262 · Q 93 (A) — A Note on the Stationary Bootstrap's Variance

- **Autores:** Daniel J. Nordman
- **Año:** 2009
- **Publicación o institución:** The Annals of Statistics, 37(1), 359-370
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-01 Estadística e inferencia (principal) · secundarias: TM-09
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 7/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** DOI: 10.1214/07-AOS567 · https://web3.arxiv.org/pdf/0903.0474
- **Acceso y licencia:** Acceso abierto (arXiv:0903.0474)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Bootstrapping (statistics) wikipedia block bootstrap Politis Romano Davison Hinkley BCa references»; WebFetch: sí)
- **Contenido:** Demuestra que la varianza asintótica del bootstrap estacionario coincide con la del bootstrap de bloques fijos no solapados, corrigiendo la creencia de que era la mayor.
- **Uso en el Motor:** MC-01, MC-10: justificación de elegir entre bootstrap estacionario y por bloques.
- **Limitaciones:** Resultado de primer orden; no cubre el sesgo.

#### DOC-MOT-0264 · Q 93 (A) — Some Asymptotic Theory for the Bootstrap

- **Autores:** Peter J. Bickel; David A. Freedman
- **Año:** 1981
- **Publicación o institución:** The Annals of Statistics, 9, 1196-1217
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-01 Estadística e inferencia (principal) · secundarias: TM-09
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** Verificada en página índice: https://arxiv.org/pdf/1809.04016
- **Acceso y licencia:** Project Euclid (IMS)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Bootstrapping (statistics) wikipedia block bootstrap Politis Romano Davison Hinkley BCa references»; WebFetch: sí, sobre la página índice https://arxiv.org/pdf/1809.04016)
- **Contenido:** Condiciones de validez asintótica del bootstrap para medias, U-estadísticos, cuantiles y funcionales de von Mises.
- **Uso en el Motor:** MC-01: fundamento de la consistencia del bootstrap.
- **Limitaciones:** Confirmada solo mediante página índice (bibliografía de J. L. Horowitz, «Bootstrap Methods in Econometrics»); pendiente de lectura de la fuente primaria.

#### DOC-MOT-0271 · Q 93 (A) — A New Look at the Statistical Model Identification

- **Autores:** Hirotugu Akaike
- **Año:** 1974
- **Publicación o institución:** IEEE Transactions on Automatic Control, 19(6), 716-723
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-01 Estadística e inferencia (principal) · secundarias: TM-02, TM-04
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** Verificada en página índice: https://cran.r-universe.dev/lpirfs/doc/manual.html
- **Acceso y licencia:** Revista IEEE por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Jordà 2005 "Estimation and Inference of Impulse Responses by Local Projections" American Economic Review 95»; WebFetch: sí, sobre la página índice https://cran.r-universe.dev/lpirfs/doc/manual.html)
- **Contenido:** Propone el criterio de información de Akaike (AIC) para seleccionar modelos minimizando la pérdida de información esperada.
- **Uso en el Motor:** MC-01, MC-02: selección de orden (ARMA, VAR, retardos).
- **Limitaciones:** Tiende a sobreparametrizar en muestras grandes. Confirmada solo mediante página índice (bibliografía de manual de lpirfs); pendiente de lectura de la fuente primaria.

#### DOC-MOT-0267 · Q 92 (A) — Resampling Fewer than n Observations: Gains, Losses, and Remedies for Losses

- **Autores:** Peter J. Bickel; Friedrich Götze; Willem R. van Zwet
- **Año:** 1997
- **Publicación o institución:** Statistica Sinica, 7, 1-32
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-01 Estadística e inferencia (principal) · secundarias: —
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** Verificada en página índice: https://arxiv.org/pdf/1809.04016
- **Acceso y licencia:** Statistica Sinica (acceso libre en la web de la revista)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Bootstrapping (statistics) wikipedia block bootstrap Politis Romano Davison Hinkley BCa references»; WebFetch: sí, sobre la página índice https://arxiv.org/pdf/1809.04016)
- **Contenido:** Bootstrap «m de n»: consistente en casos donde falla el bootstrap estándar, con análisis de pérdidas de eficiencia y remedios.
- **Uso en el Motor:** MC-01: alternativa al bootstrap en casos no regulares.
- **Limitaciones:** Elección de m. Confirmada solo mediante página índice (bibliografía de J. L. Horowitz); pendiente de lectura de la fuente primaria.

#### DOC-MOT-0269 · Q 91 (A) — How Robust Standard Errors Expose Methodological Problems They Do Not Fix, and What to Do About It

- **Autores:** Gary King; Margaret E. Roberts
- **Año:** 2015
- **Publicación o institución:** Political Analysis, 23(2), 159-179
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-01 Estadística e inferencia (principal) · secundarias: TM-04
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1093/pan/mpu015 · Verificada en página índice: https://en.wikipedia.org/wiki/Heteroskedasticity-consistent_standard_errors
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Heteroskedasticity-consistent standard errors wikipedia White 1980 MacKinnon White 1985»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Heteroskedasticity-consistent_standard_errors)
- **Contenido:** Propone usar la discrepancia entre errores clásicos y robustos como diagnóstico de mala especificación, con un contraste formal y pasos de reespecificación.
- **Uso en el Motor:** MC-01, MC-03: diagnóstico de especificación en regresiones del Motor.
- **Limitaciones:** Confirmada solo mediante página índice (bibliografía de Wikipedia «Heteroskedasticity-consistent standard errors»); pendiente de lectura de la fuente primaria.

#### DOC-MOT-0265 · Q 91 (A) — The Block-Block Bootstrap: Improved Asymptotic Refinements

- **Autores:** Donald W. K. Andrews
- **Año:** 2004
- **Publicación o institución:** Econometrica, 72, 673-700
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-01 Estadística e inferencia (principal) · secundarias: TM-02
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 7/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** Verificada en página índice: https://arxiv.org/pdf/1809.04016
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Bootstrapping (statistics) wikipedia block bootstrap Politis Romano Davison Hinkley BCa references»; WebFetch: sí, sobre la página índice https://arxiv.org/pdf/1809.04016)
- **Contenido:** Bootstrap de bloques de bloques con refinamientos asintóticos superiores para estadísticos de series temporales.
- **Uso en el Motor:** MC-01: inferencia por bloques con mejor precisión de orden superior.
- **Limitaciones:** Confirmada solo mediante página índice (bibliografía de J. L. Horowitz); pendiente de lectura de la fuente primaria.

#### DOC-MOT-0266 · Q 91 (A) — Inconsistency of the Bootstrap when a Parameter Is on the Boundary of the Parameter Space

- **Autores:** Donald W. K. Andrews
- **Año:** 2000
- **Publicación o institución:** Econometrica, 68, 399-405
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-01 Estadística e inferencia (principal) · secundarias: —
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** Verificada en página índice: https://arxiv.org/pdf/1809.04016
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Bootstrapping (statistics) wikipedia block bootstrap Politis Romano Davison Hinkley BCa references»; WebFetch: sí, sobre la página índice https://arxiv.org/pdf/1809.04016)
- **Contenido:** Muestra que el bootstrap es inconsistente cuando el parámetro está en la frontera (p. ej., varianzas o coeficientes GARCH en cero) y propone alternativas (submuestreo, m de n).
- **Uso en el Motor:** MC-01, MC-02: advertencia al hacer bootstrap de parámetros restringidos.
- **Limitaciones:** Confirmada solo mediante página índice (bibliografía de J. L. Horowitz); pendiente de lectura de la fuente primaria.

#### DOC-MOT-0273 · Q 91 (A) — Regression and Time Series Model Selection in Small Samples

- **Autores:** Clifford M. Hurvich; Chih-Ling Tsai
- **Año:** 1989
- **Publicación o institución:** Biometrika, 76(2), 297-307
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-01 Estadística e inferencia (principal) · secundarias: TM-02
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** Verificada en página índice: https://cran.r-universe.dev/lpirfs/doc/manual.html
- **Acceso y licencia:** Revista OUP por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Jordà 2005 "Estimation and Inference of Impulse Responses by Local Projections" American Economic Review 95»; WebFetch: sí, sobre la página índice https://cran.r-universe.dev/lpirfs/doc/manual.html)
- **Contenido:** Criterio AICc: corrección del AIC para muestras pequeñas en regresión y modelos de series temporales.
- **Uso en el Motor:** MC-01, MC-02: selección de modelos con historiales cortos.
- **Limitaciones:** Confirmada solo mediante página índice (bibliografía de manual de lpirfs); pendiente de lectura de la fuente primaria.

#### DOC-MOT-0200 · Q 90 (A) — Stationary Jackknife

- **Autores:** Weilian Zhou; Soumendra N. Lahiri
- **Año:** 2024 (en línea 25/08/2023)
- **Publicación o institución:** Journal of Time Series Analysis, 45, 333-360 (Wiley)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-01 Estadística e inferencia (principal) · secundarias: TM-02, TM-09
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 5/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** DOI: 10.1111/jtsa.12714 · https://par.nsf.gov//servlets/purl/10542182
- **Acceso y licencia:** Manuscrito aceptado en el repositorio público de la NSF (PAR), lectura libre; versión editorial de Wiley por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Künsch 1989 "The Jackknife and the Bootstrap for General Stationary Observations" Annals of Statistics»; WebFetch: sí)
- **Contenido:** Propone un jackknife para series estacionarias que elimina bloques de longitud aleatoria (geométrica truncada); prueba su consistencia para la varianza de la media y de estadísticos no lineales y muestra menor sensibilidad a la longitud de bloque que el jackknife de bloques móviles.
- **Uso en el Motor:** MC-01, MC-10: estimación robusta de la varianza de estadísticos (medias, ratios) calculados sobre rendimientos autocorrelados.
- **Limitaciones:** Método reciente, poco adoptado aún; sin implementación estándar en bibliotecas generalistas.

#### DOC-MOT-0268 · Q 89 (A) — On the So-Called 'Huber Sandwich Estimator' and 'Robust Standard Errors'

- **Autores:** David A. Freedman
- **Año:** 2006
- **Publicación o institución:** The American Statistician, 60(4), 299-302
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-01 Estadística e inferencia (principal) · secundarias: TM-04
- **Calidad Q:** 89 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1198/000313006X152207 · Verificada en página índice: https://en.wikipedia.org/wiki/Heteroskedasticity-consistent_standard_errors
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Heteroskedasticity-consistent standard errors wikipedia White 1980 MacKinnon White 1985»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Heteroskedasticity-consistent_standard_errors)
- **Contenido:** Advierte que los errores sándwich no salvan un modelo mal especificado: si el modelo es erróneo, el parámetro estimado puede carecer de sentido aunque su error estándar sea «robusto».
- **Uso en el Motor:** MC-01, MC-03: cautela al presentar errores robustos como garantía.
- **Limitaciones:** Nota breve. Confirmada solo mediante página índice (bibliografía de Wikipedia «Heteroskedasticity-consistent standard errors»); pendiente de lectura de la fuente primaria.

#### DOC-MOT-0270 · Q 89 (A) — Using Heteroscedasticity Consistent Standard Errors in the Linear Regression Model

- **Autores:** J. Scott Long; Laurie H. Ervin
- **Año:** 2000
- **Publicación o institución:** The American Statistician, 54(3), 217-224
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-01 Estadística e inferencia (principal) · secundarias: TM-04
- **Calidad Q:** 89 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.2307/2685594 · Verificada en página índice: https://en.wikipedia.org/wiki/Heteroskedasticity-consistent_standard_errors
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Heteroskedasticity-consistent standard errors wikipedia White 1980 MacKinnon White 1985»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Heteroskedasticity-consistent_standard_errors)
- **Contenido:** Simulaciones que recomiendan HC3 en muestras de menos de 250 observaciones frente a HC0-HC2.
- **Uso en el Motor:** MC-01: regla práctica de elección de estimador HC.
- **Limitaciones:** Confirmada solo mediante página índice (bibliografía de Wikipedia «Heteroskedasticity-consistent standard errors»); pendiente de lectura de la fuente primaria.

#### DOC-MOT-0014 · Q 88 (A) — An Introduction to the Bootstrap

- **Autores:** Bradley Efron; Robert J. Tibshirani
- **Año:** 1993 (la ficha de la editorial consigna 1994 como fecha de catálogo)
- **Publicación o institución:** Chapman & Hall/CRC (Monographs on Statistics and Applied Probability 57), hoy en Routledge/CRC Press
- **Tipo de documento:** Libro académico
- **Temática:** TM-01 Estadística e inferencia (principal) · secundarias: TM-09
- **Calidad Q:** 88 (A) — Tipo 20/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** ISBN: 9780412042317 · https://www.routledge.com/An-Introduction-to-the-Bootstrap/Efron-Tibshirani/p/book/9780412042317
- **Acceso y licencia:** Libro de pago (Routledge/CRC Press)
- **Estado:** Aprobada
- **Estado del enlace:** MURO_PAGO
- **Última verificación:** 2026-11-02 (búsqueda web: «Efron Tibshirani "An Introduction to the Bootstrap" 1993 Chapman Hall 10.1201/9780429246593»; WebFetch: sí)
- **Contenido:** Manual de referencia del bootstrap: errores estándar, intervalos (percentil, BCa, bootstrap-t), contrastes por remuestreo, validación cruzada y estimación de sesgo, con ejemplos.
- **Uso en el Motor:** MC-01, MC-05: intervalos de confianza por remuestreo, error estándar de estadísticos no estándar.
- **Limitaciones:** Bootstrap i.i.d.: no válido con dependencia serial sin variantes por bloques. El DOI de la semilla (10.1201/9780429246593) no se ha visto y se retira.
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02 (título, autores, serie y editorial coincidentes; año matizado).

#### DOC-MOT-0263 · Q 86 (A) — Bootstrap Methods in Econometrics

- **Autores:** Joel L. Horowitz
- **Año:** 2018 (arXiv)
- **Publicación o institución:** arXiv:1809.04016 (Northwestern University)
- **Tipo de documento:** Artículo de revisión (preprint)
- **Temática:** TM-01 Estadística e inferencia (principal) · secundarias: TM-04
- **Calidad Q:** 86 (A) — Tipo 18/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 7/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://arxiv.org/pdf/1809.04016
- **Acceso y licencia:** Acceso abierto (arXiv)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Bootstrapping (statistics) wikipedia block bootstrap Politis Romano Davison Hinkley BCa references»; WebFetch: sí)
- **Contenido:** Panorama expositivo del bootstrap en econometría: cuándo mejora la inferencia asintótica de primer orden y cuándo falla o requiere modificaciones (parámetros en la frontera, máximos, estimadores no suaves).
- **Uso en el Motor:** MC-01: criterios para decidir si el bootstrap es válido en un cálculo concreto.
- **Limitaciones:** Versión publicada no confirmada en esta verificación.

#### DOC-MOT-0018 · Q 86 (A) — Statistical Inference (2.ª ed.)

- **Autores:** George Casella; Roger L. Berger
- **Año:** 2002 (Duxbury/Cengage; reimpresión de Chapman & Hall/CRC en 2024)
- **Publicación o institución:** Duxbury / Cengage Learning; reimpresión Chapman & Hall (Routledge/CRC Press), 2024
- **Tipo de documento:** Manual de referencia
- **Temática:** TM-01 Estadística e inferencia (principal)
- **Calidad Q:** 86 (A) — Tipo 20/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** ISBN (reimpresión 2024): 9781032593036 · https://www.routledge.com/product/isbn/9781040024027
- **Acceso y licencia:** Libro de pago
- **Estado:** Aprobada
- **Estado del enlace:** MURO_PAGO
- **Última verificación:** 2026-11-02 (búsqueda web: «Casella Berger Statistical Inference second edition 2002 Duxbury ISBN»; WebFetch: sí)
- **Contenido:** Manual de inferencia estadística: distribuciones, suficiencia, estimación puntual (máxima verosimilitud, insesgadez, Cramér-Rao), contrastes (Neyman-Pearson, razón de verosimilitudes), intervalos y asintótica.
- **Uso en el Motor:** MC-01: estimación, contrastes, intervalos, suficiencia, máxima verosimilitud.
- **Limitaciones:** Manual general, no específico de finanzas ni de datos dependientes. La editorial indica que la 2.ª ed. original es de Cengage (2001/2002).
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02.

#### DOC-MOT-0201 · Q 76 (B) — tseries: tsbootstrap — Bootstrap for General Stationary Data (documentación de función R)

- **Autores:** Adrian Trapletti (autor de la función; paquete tseries, CRAN)
- **Año:** Documentación vigente consultada en 2026
- **Publicación o institución:** Paquete R «tseries» (CRAN), página de ayuda en rdrr.io
- **Tipo de documento:** Documentación técnica de software
- **Temática:** TM-01 Estadística e inferencia (principal) · secundarias: TM-09, TM-14
- **Calidad Q:** 76 (B) — Tipo 15/25 · Rigor 14/20 · Autoridad 11/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** https://rdrr.io/cran/tseries/man/tsbootstrap.html
- **Acceso y licencia:** Abierto; software libre (CRAN)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Künsch 1989 "The Jackknife and the Bootstrap for General Stationary Observations" Annals of Statistics»; WebFetch: sí)
- **Contenido:** Implementa bootstrap estacionario (Politis-Romano 1994, longitud media de bloque b), bootstrap por bloques (Künsch 1989) y bloques de bloques; estima sesgo y error estándar de un estadístico; longitud por defecto proporcional a n^(1/3).
- **Uso en el Motor:** MC-01, MC-10: implementación de referencia para replicar intervalos por bloques y contrastar resultados de código propio.
- **Limitaciones:** No selecciona automáticamente la longitud de bloque óptima; documentación escueta.

## TM-02 Series temporales y detección de tendencias

#### DOC-MOT-0029 · Q 95 (A) — Why You Should Never Use the Hodrick-Prescott Filter

- **Autores:** James D. Hamilton
- **Año:** 2018
- **Publicación o institución:** The Review of Economics and Statistics, 100(5), 831-843 (MIT Press); versión de trabajo NBER WP 23429 (2017)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-02 Series temporales y detección de tendencias (principal) · secundarias: TM-04
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI: 10.1162/rest_a_00706 · https://www.nber.org/papers/w23429 · https://ideas.repec.org/a/tpr/restat/v100y2018i5p831-843.html
- **Acceso y licencia:** Documento de trabajo NBER (DOI 10.3386/w23429) y copia del autor (econweb.ucsd.edu) localizables; revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Hamilton 2018 "Why You Should Never Use the Hodrick-Prescott Filter" Review of Economics and Statistics»; WebFetch: sí)
- **Contenido:** Muestra que el filtro HP genera dinámicas espurias, valores de final de muestra distintos de los intermedios y un λ incoherente con los datos; propone como alternativa la regresión de y(t+h) sobre sus 4 últimos valores (h = 8 trimestres), cuyo residuo es el ciclo.
- **Uso en el Motor:** MC-02: alternativa de regresión al filtro HP; cuándo NO usar HP.
- **Limitaciones:** Propuesta discutida en la literatura posterior (véanse DOC-MOT-0204 y DOC-MOT-0205).
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02 (DOI confirmado).

#### DOC-MOT-0025 · Q 95 (A) — Computation and Analysis of Multiple Structural Change Models

- **Autores:** Jushan Bai; Pierre Perron
- **Año:** 2003
- **Publicación o institución:** Journal of Applied Econometrics, 18(1), 1-22
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-02 Series temporales y detección de tendencias (principal) · secundarias: TM-03
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1002/jae.659 · https://ideas.repec.org/a/jae/japmet/v18y2003i1p1-22.html
- **Acceso y licencia:** Ficha RePEc abierta; texto Wiley por suscripción; versión de trabajo (Montréal 9807) listada en RePEc
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Bai Perron 2003 "Computation and analysis of multiple structural change models" Journal of Applied Econometrics 10.1002/jae.659»; WebFetch: sí)
- **Contenido:** Algoritmo de programación dinámica para obtener las particiones de mínima suma de cuadrados con O(T²) operaciones, valores críticos ampliados, intervalos de confianza de las fechas y guía práctica de especificación.
- **Uso en el Motor:** MC-02: algoritmo de programación dinámica y valores críticos para Bai-Perron.
- **Limitaciones:** Coste computacional con muchas rupturas y regresores fijos entre regímenes (iterativo, sin óptimo garantizado).
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02 (DOI confirmado).

#### DOC-MOT-0024 · Q 95 (A) — Estimating and Testing Linear Models with Multiple Structural Changes

- **Autores:** Jushan Bai; Pierre Perron
- **Año:** 1998
- **Publicación o institución:** Econometrica, 66(1), 47-78
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-02 Series temporales y detección de tendencias (principal) · secundarias: TM-03
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** https://ideas.repec.org/a/ecm/emetrp/v66y1998i1p47-78.html · registro de la Econometric Society: https://www.econometricsociety.org/publications/econometrica/1998/01/01/estimating-and-testing-linear-models-multiple-structural (DOI no visto)
- **Acceso y licencia:** Ficha RePEc abierta; texto en Econometrica/JSTOR por suscripción (versión de trabajo del Département de sciences économiques de Montréal listada en RePEc)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Bai Perron 1998 "Estimating and Testing Linear Models with Multiple Structural Changes" Econometrica 66»; WebFetch: sí)
- **Contenido:** Teoría asintótica para estimar por mínimos cuadrados múltiples rupturas en fechas desconocidas, con contrastes supF, doble máximo (UDmax, WDmax) y secuencial ℓ frente a ℓ+1 para determinar el número de rupturas.
- **Uso en el Motor:** MC-02: detección y datación de múltiples rupturas estructurales.
- **Limitaciones:** Requiere tamaño mínimo de segmento (trimming); potencia baja con rupturas pequeñas; valores críticos no válidos con regresores no estacionarios. El DOI de la semilla (10.2307/2998540) no se ha visto y se retira.
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02.

#### DOC-MOT-0253 · Q 95 (A) — Tests for Parameter Instability and Structural Change with Unknown Change Point

- **Autores:** Donald W. K. Andrews
- **Año:** 1993
- **Publicación o institución:** Econometrica, 61(4), 821-856 (corrigendum: Econometrica 71(1), 2003, 395-397)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-02 Series temporales y detección de tendencias (principal) · secundarias: TM-04
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.2307/2951764 · Verificada en página índice: https://en.wikipedia.org/wiki/Structural_break
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Structural break wikipedia Chow test Andrews 1993 Zivot Andrews Bai Perron references»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Structural_break)
- **Contenido:** Contrastes supremo (sup-Wald, sup-LM, sup-LR) de una ruptura en fecha desconocida, con valores críticos asintóticos según el recorte.
- **Uso en el Motor:** MC-02: contraste de una ruptura de fecha desconocida.
- **Limitaciones:** Una sola ruptura; véase Bai-Perron para varias. Confirmada solo mediante página índice (bibliografía de Wikipedia «Structural break»); pendiente de lectura de la fuente primaria.

#### DOC-MOT-0027 · Q 94 (A) — Testing the Null Hypothesis of Stationarity against the Alternative of a Unit Root

- **Autores:** Denis Kwiatkowski; Peter C. B. Phillips; Peter Schmidt; Yongcheol Shin
- **Año:** 1992
- **Publicación o institución:** Journal of Econometrics, 54(1-3), 159-178; versión de trabajo: Cowles Foundation Discussion Paper 979 (1991)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-02 Series temporales y detección de tendencias (principal) · secundarias: TM-04
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** https://econpapers.repec.org/RePEc:cwl:cwldpp:979 (DOI no visto)
- **Acceso y licencia:** Documento de trabajo de Cowles (Yale) de acceso libre; revista Elsevier por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Kwiatkowski Phillips Schmidt Shin 1992 "Testing the null hypothesis of stationarity against the alternative of a unit root" Journal of Econometrics 54»; WebFetch: sí)
- **Contenido:** Contraste LM (KPSS) con hipótesis nula de estacionariedad en nivel o alrededor de tendencia, basado en sumas parciales de residuos y varianza de largo plazo con núcleo de Bartlett.
- **Uso en el Motor:** MC-02: contraste KPSS (nula de estacionariedad), en combinación con ADF.
- **Limitaciones:** Sensible a la elección del ancho de banda; distorsiones de tamaño con alta persistencia. La versión de trabajo de Cowles figura con tres autores; la publicada añade a Y. Shin. El DOI de la semilla no se ha visto y se retira.
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02.

#### DOC-MOT-0026 · Q 93 (A) — Distribution of the Estimators for Autoregressive Time Series with a Unit Root

- **Autores:** David A. Dickey; Wayne A. Fuller
- **Año:** 1979
- **Publicación o institución:** Journal of the American Statistical Association, 74(366), 427-431
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-02 Series temporales y detección de tendencias (principal) · secundarias: TM-04
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** https://bigenc.ru/b/distribution-of-the-estimators-for-autoregressive-024b8d (ficha bibliográfica; DOI no visto)
- **Acceso y licencia:** Revista (Taylor & Francis/JSTOR) por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Dickey Fuller 1979 "Distribution of the Estimators for Autoregressive Time Series with a Unit Root" JASA 74 366»; WebFetch: sí)
- **Contenido:** Obtiene la distribución límite no estándar del estimador MCO y del estadístico t en un AR(1) con raíz unitaria (con y sin constante y tendencia): base del contraste Dickey-Fuller.
- **Uso en el Motor:** MC-02: contraste DF/ADF de raíz unitaria (tendencia estocástica frente a determinista).
- **Limitaciones:** Baja potencia en muestras cortas y ante rupturas; combinar con KPSS. El DOI de la semilla no se ha visto y se retira; la URL es una ficha bibliográfica, no el texto.
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02.

#### DOC-MOT-0020 · Q 92 (A) — Forecasting: Principles and Practice (3.ª ed.)

- **Autores:** Rob J. Hyndman; George Athanasopoulos
- **Año:** 2021
- **Publicación o institución:** OTexts (libro en línea abierto, con edición impresa)
- **Tipo de documento:** Manual de referencia
- **Temática:** TM-02 Series temporales y detección de tendencias (principal) · secundarias: TM-11
- **Calidad Q:** 92 (A) — Tipo 20/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** ISBN: 9780987507136 · https://ci.nii.ac.jp/ncid/BC10558540 · libro en línea enlazado desde el paquete CRAN fpp3: https://OTexts.com/fpp3/
- **Acceso y licencia:** Acceso abierto en línea (OTexts); paquete de datos fpp3 en CRAN
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «"Forecasting: Principles and Practice" 3rd edition Hyndman Athanasopoulos 2021»; WebFetch: sí (CiNii y página CRAN de fpp3; otexts.com no admitido por WebFetch))
- **Contenido:** Manual de previsión: descomposición STL, suavizado exponencial (ETS), ARIMA, regresión dinámica, previsión jerárquica, validación cruzada temporal y métricas de precisión, con código R (fable/tsibble).
- **Uso en el Motor:** MC-02, MC-10: descomposición, ETS, ARIMA, validación cruzada temporal, métricas de precisión.
- **Limitaciones:** Orientado a previsión univariante y de negocio; el texto en otexts.com no pudo leerse con WebFetch (dominio no admitido).
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02 (título, autores, edición, editorial, año e ISBN en CiNii).

#### DOC-MOT-0255 · Q 92 (A) — Trends and Random Walks in Macroeconomic Time Series: Some Evidence and Implications

- **Autores:** Charles R. Nelson; Charles I. Plosser
- **Año:** 1982
- **Publicación o institución:** Journal of Monetary Economics, 10(2), 139-162
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-02 Series temporales y detección de tendencias (principal) · secundarias: TM-04
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1016/0304-3932(82)90012-5 · Verificada en página índice: https://en.wikipedia.org/wiki/Cointegration
- **Acceso y licencia:** Revista Elsevier por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Cointegration wikipedia Engle-Granger Johansen test Phillips-Ouliaris references»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Cointegration)
- **Contenido:** Aplica contrastes Dickey-Fuller a 14 series macro de EE. UU. y no rechaza raíz unitaria en la mayoría: tendencias estocásticas frente a deterministas.
- **Uso en el Motor:** MC-02: precedente empírico para tratar tendencias como estocásticas.
- **Limitaciones:** Conclusiones discutidas con rupturas (Perron 1989). Título completo en la publicación; el índice lo abrevia. Confirmada solo mediante página índice (bibliografía de Wikipedia «Cointegration»); pendiente de lectura de la fuente primaria.

#### DOC-MOT-0023 · Q 92 (A) — Estimates of the Regression Coefficient Based on Kendall's Tau

- **Autores:** Pranab Kumar Sen
- **Año:** 1968
- **Publicación o institución:** Journal of the American Statistical Association, 63(324), 1379-1389
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-02 Series temporales y detección de tendencias (principal)
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1080/01621459.1968.10480934 · https://mathworld.wolfram.com/Theil-SenEstimator.html (cita con DOI)
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Sen 1968 "Estimates of the Regression Coefficient Based on Kendall's Tau" Journal of the American Statistical Association 63»; WebFetch: sí)
- **Contenido:** Estimador de la pendiente como mediana de las pendientes entre todos los pares (Theil-Sen), con intervalo de confianza basado en la tau de Kendall; robusto a atípicos.
- **Uso en el Motor:** MC-02: pendiente de Theil-Sen para cuantificar la intensidad de una tendencia.
- **Limitaciones:** Supone tendencia lineal; los intervalos suponen independencia.
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02 (DOI confirmado).

#### DOC-MOT-0021 · Q 92 (A) — Nonparametric Tests Against Trend

- **Autores:** Henry B. Mann
- **Año:** 1945
- **Publicación o institución:** Econometrica, 13(3), 245-259
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-02 Series temporales y detección de tendencias (principal)
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** https://intouch.econometricsociety.org/publications/econometrica/1945/07/01/nonparametric-tests-against-trend · JSTOR estable 1907187 (DOI no visto)
- **Acceso y licencia:** Registro abierto de la Econometric Society; texto vía JSTOR
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Mann 1945 "Nonparametric Tests Against Trend" Econometrica 13 245-259»; WebFetch: sí)
- **Contenido:** Propone el estadístico S (número de pares concordantes menos discordantes en el tiempo) como prueba no paramétrica de tendencia monótona: origen de la prueba de Mann-Kendall.
- **Uso en el Motor:** MC-02: prueba de Mann-Kendall de tendencia monótona.
- **Limitaciones:** Sin control del error tipo I con autocorrelación (véase DOC-MOT-0202). El DOI de la semilla no se ha visto y se retira.
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02.

#### DOC-MOT-0257 · Q 91 (A) — On Adjusting the Hodrick-Prescott Filter for the Frequency of Observations

- **Autores:** Morten O. Ravn; Harald Uhlig
- **Año:** 2002
- **Publicación o institución:** The Review of Economics and Statistics, 84(2), 371-376
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-02 Series temporales y detección de tendencias (principal) · secundarias: —
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** Verificada en página índice: https://cran.r-universe.dev/lpirfs/doc/manual.html
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Jordà 2005 "Estimation and Inference of Impulse Responses by Local Projections" American Economic Review 95»; WebFetch: sí, sobre la página índice https://cran.r-universe.dev/lpirfs/doc/manual.html)
- **Contenido:** Regla de ajuste de λ del filtro HP según la frecuencia (multiplicar por la cuarta potencia del cambio de frecuencia: λ≈6,25 anual, 129 600 mensual).
- **Uso en el Motor:** MC-02: λ coherente cuando se aplica HP a datos no trimestrales.
- **Limitaciones:** Confirmada solo mediante página índice (bibliografía de manual de lpirfs); pendiente de lectura de la fuente primaria.

#### DOC-MOT-0031 · Q 91 (A) — Continuous Inspection Schemes

- **Autores:** E. S. Page
- **Año:** 1954
- **Publicación o institución:** Biometrika, 41(1-2), 100-115
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-02 Series temporales y detección de tendencias (principal) · secundarias: TM-03
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1093/biomet/41.1-2.100 · https://academic.oup.com/biomet/issue/41/1-2
- **Acceso y licencia:** Oxford Academic, suscripción
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Page 1954 "Continuous Inspection Schemes" Biometrika 41 100-115»; WebFetch: sí, índice del número)
- **Contenido:** Introduce el CUSUM: suma acumulada de desviaciones respecto a un valor de referencia con regla de alarma por umbral, para detectar de forma secuencial cambios en la media.
- **Uso en el Motor:** MC-02: CUSUM para detección secuencial de cambios.
- **Limitaciones:** Requiere fijar umbrales y tamaño de cambio de referencia; supuestos de independencia.
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02 (DOI confirmado).

#### DOC-MOT-0254 · Q 90 (A) — The New Econometrics of Structural Change: Dating Breaks in U.S. Labor Productivity

- **Autores:** Bruce E. Hansen
- **Año:** 2001
- **Publicación o institución:** Journal of Economic Perspectives, 15(4), 117-128
- **Tipo de documento:** Artículo revisado por pares (divulgativo-técnico)
- **Temática:** TM-02 Series temporales y detección de tendencias (principal) · secundarias: —
- **Calidad Q:** 90 (A) — Tipo 23/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** DOI: 10.1257/jep.15.4.117 · Verificada en página índice: https://en.wikipedia.org/wiki/Structural_break · ficha IDEAS https://ideas.repec.org:443/a/aea/jecper/v15y2001i4p117-128.html
- **Acceso y licencia:** JEP de acceso abierto en la web de la AEA
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Structural break wikipedia Chow test Andrews 1993 Zivot Andrews Bai Perron references»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Structural_break)
- **Contenido:** Introducción aplicada a contrastes de ruptura (Chow, Andrews, Bai-Perron) e intervalos de fechas, con aplicación a la productividad de EE. UU.
- **Uso en el Motor:** MC-02: guía didáctica para justificar la datación de rupturas.
- **Limitaciones:** Confirmada solo mediante página índice (bibliografía de Wikipedia «Structural break»); pendiente de lectura de la fuente primaria.

#### DOC-MOT-0028 · Q 90 (A) — Postwar U.S. Business Cycles: An Empirical Investigation

- **Autores:** Robert J. Hodrick; Edward C. Prescott
- **Año:** 1997
- **Publicación o institución:** Journal of Money, Credit and Banking, 29(1), 1-16
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-02 Series temporales y detección de tendencias (principal)
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** https://ideas.repec.org/a/mcb/jmoncb/v29y1997i1p1-16.html (DOI no visto)
- **Acceso y licencia:** Ficha RePEc abierta; versión de trabajo (Northwestern CMS-EMS 451) listada en RePEc; revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Hodrick Prescott 1997 "Postwar U.S. Business Cycles: An Empirical Investigation" Journal of Money, Credit and Banking 29»; WebFetch: sí)
- **Contenido:** Formaliza el filtro HP: tendencia que minimiza la suma de cuadrados del ciclo más λ veces la suma de cuadrados de las segundas diferencias de la tendencia (λ = 1600 trimestral).
- **Uso en el Motor:** MC-02: filtro HP para separar tendencia y ciclo (con cautelas).
- **Limitaciones:** Efecto de final de muestra y ciclos espurios (DOC-MOT-0029); vigencia reducida para uso en tiempo real. El DOI de la semilla no se ha visto y se retira.
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02.

#### DOC-MOT-0256 · Q 88 (A) — bcp: An R Package for Performing a Bayesian Analysis of Change Point Problems

- **Autores:** Chandra Erdman; John W. Emerson
- **Año:** 2007
- **Publicación o institución:** Journal of Statistical Software, 23(3)
- **Tipo de documento:** Artículo revisado por pares (software)
- **Temática:** TM-02 Series temporales y detección de tendencias (principal) · secundarias: TM-14
- **Calidad Q:** 88 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 12/15 · Vigencia 9/10 · Impacto 7/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** DOI: 10.18637/jss.v023.i03 · Verificada en página índice: https://en.wikipedia.org/wiki/Structural_break
- **Acceso y licencia:** Acceso abierto (JSS)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Structural break wikipedia Chow test Andrews 1993 Zivot Andrews Bai Perron references»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Structural_break)
- **Contenido:** Implementación del análisis bayesiano de puntos de cambio de Barry-Hartigan con probabilidades posteriores de cambio en cada instante.
- **Uso en el Motor:** MC-02: probabilidad posterior de ruptura como medida de incertidumbre.
- **Limitaciones:** Confirmada solo mediante página índice (bibliografía de Wikipedia «Structural break»); pendiente de lectura de la fuente primaria.

#### DOC-MOT-0019 · Q 88 (A) — Time Series Analysis

- **Autores:** James D. Hamilton
- **Año:** 1994
- **Publicación o institución:** Princeton University Press
- **Tipo de documento:** Manual de referencia
- **Temática:** TM-02 Series temporales y detección de tendencias (principal) · secundarias: TM-04
- **Calidad Q:** 88 (A) — Tipo 20/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** ISBN: 978-0-691-04289-3 · verificada en páginas índice: https://en.wikipedia.org/wiki/Newey%E2%80%93West_estimator · https://www.wiwiss.fu-berlin.de/fachbereich/vwl/luetkepohl/Lehrveranstaltungen/MTSA_SS2016.pdf
- **Acceso y licencia:** Libro de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Newey–West estimator wikipedia heteroskedasticity and autocorrelation consistent Andrews 1991 bandwidth»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Newey%E2%80%93West_estimator)
- **Contenido:** Manual de series temporales: ARMA, raíces unitarias, VAR, cointegración, GMM, filtro de Kalman, estimación HAC y cambio de régimen markoviano.
- **Uso en el Motor:** MC-02, MC-03: ARMA, raíces unitarias, VAR, cointegración, filtro de Kalman, cambio de régimen.
- **Limitaciones:** No cubre desarrollos posteriores a 1994 (volatilidad realizada, proyecciones locales). Confirmada solo mediante página índice (bibliografía de Wikipedia «Newey–West estimator» y programa docente de H. Lütkepohl, FU Berlin); pendiente de lectura de la fuente primaria.
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02 (ISBN confirmado en índice).

#### DOC-MOT-0030 · Q 86 (A) — STL: A Seasonal-Trend Decomposition Procedure Based on Loess

- **Autores:** Robert B. Cleveland; William S. Cleveland; Jean E. McRae; Irma Terpenning
- **Año:** 1990
- **Publicación o institución:** Journal of Official Statistics, 6(1), 3-73 (Statistics Sweden)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-02 Series temporales y detección de tendencias (principal) · secundarias: —
- **Calidad Q:** 86 (A) — Tipo 22/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** Verificada en página índice: https://www.statsmodels.org/v0.14.4/generated/statsmodels.tsa.seasonal.STL.html (cita completa en la documentación de statsmodels STL)
- **Acceso y licencia:** Revista de acceso abierto (JOS); enlace directo al texto no obtenido en esta verificación
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Cleveland 1990 "STL: A Seasonal-Trend Decomposition Procedure Based on Loess" Journal of Official Statistics»; WebFetch: sí, sobre la página índice https://www.statsmodels.org/v0.14.4/generated/statsmodels.tsa.seasonal.STL.html)
- **Contenido:** Descomposición iterativa de una serie en estacionalidad, tendencia y resto mediante suavizados loess anidados, con versión robusta a atípicos.
- **Uso en el Motor:** MC-02: descomposición estacional y de tendencia robusta.
- **Limitaciones:** No modela incertidumbre de la descomposición. Confirmada solo mediante página índice (bibliografía de statsmodels); pendiente de lectura de la fuente primaria.
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02.

#### DOC-MOT-0202 · Q 84 (A) — Permutation Testing for Monotone Trend

- **Autores:** Joseph P. Romano; Marius A. Tirlea
- **Año:** 2024
- **Publicación o institución:** arXiv:2404.06239 [math.ST] (Stanford University)
- **Tipo de documento:** Documento de trabajo (preprint)
- **Temática:** TM-02 Series temporales y detección de tendencias (principal) · secundarias: TM-01
- **Calidad Q:** 84 (A) — Tipo 18/25 · Rigor 18/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 4/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://arxiv.org/pdf/2404.06239
- **Acceso y licencia:** Acceso abierto (arXiv)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Mann 1945 "Nonparametric Tests Against Trend" Econometrica 13 245-259»; WebFetch: sí)
- **Contenido:** Demuestra que el Mann-Kendall clásico no controla el error tipo I con dependencia (sobrerrechaza con autocorrelación positiva) y propone pruebas de permutación con el estadístico studentizado (varianza HAC truncada), exactas con datos i.i.d. y asintóticamente válidas con dependencia; añade estadísticos «locales» de tendencia.
- **Uso en el Motor:** MC-02: prueba de tendencia monótona válida para series financieras autocorreladas.
- **Limitaciones:** Preprint sin publicación en revista constatada; supone estacionariedad con mezcla β.

#### DOC-MOT-0203 · Q 83 (A) — A Unified Approach to Nonparametric Trend Tests for Dependent and Independent Samples

- **Autores:** Arne C. Bathke
- **Año:** 2009
- **Publicación o institución:** Metrika, 69, 17-29 (Springer)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-02 Series temporales y detección de tendencias (principal) · secundarias: TM-01
- **Calidad Q:** 83 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 12/15 · Vigencia 9/10 · Impacto 5/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.1007/s00184-008-0171-x · https://link.springer.com/doi/10.1007/s00184-008-0171-x
- **Acceso y licencia:** Springer, suscripción (resumen abierto)
- **Estado:** Aprobada
- **Estado del enlace:** MURO_PAGO
- **Última verificación:** 2026-11-02 (búsqueda web: «Mann 1945 "Nonparametric Tests Against Trend" Econometrica 13 245-259»; WebFetch: sí)
- **Contenido:** Marco único de pruebas no paramétricas frente a alternativas ordenadas para muestras dependientes e independientes, aplicable a datos cuantitativos, ordinales y binarios, invariante a transformaciones monótonas.
- **Uso en el Motor:** MC-02: contraste de tendencia ordenada entre grupos o periodos (p. ej., indicadores ordinales de sentimiento).
- **Limitaciones:** Orientado a diseños factoriales más que a series temporales largas.

#### DOC-MOT-0204 · Q 82 (A) — Why You Should Never Use the Hodrick-Prescott Filter: Comment

- **Autores:** Alban Moura
- **Año:** 2022
- **Publicación o institución:** Banque centrale du Luxembourg, Cahier d'études n.º 162 (agosto de 2022)
- **Tipo de documento:** Documento de trabajo de banco central
- **Temática:** TM-02 Series temporales y detección de tendencias (principal) · secundarias: TM-04
- **Calidad Q:** 82 (A) — Tipo 20/25 · Rigor 16/20 · Autoridad 12/15 · Vigencia 9/10 · Impacto 5/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://www.bcl.lu/en/publications/Working-papers/162/BCLWP162.pdf
- **Acceso y licencia:** Acceso abierto (Banque centrale du Luxembourg)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Hamilton 2018 "Why You Should Never Use the Hodrick-Prescott Filter" Review of Economics and Statistics»; WebFetch: sí)
- **Contenido:** Réplica a Hamilton (2018): el ciclo del filtro de Hamilton (error de previsión a varios pasos) muestra persistencia y predictibilidad análogas a las del ciclo HP y su tendencia va retrasada respecto a los datos por construcción.
- **Uso en el Motor:** MC-02: contrapeso metodológico al elegir entre filtro HP y filtro de Hamilton para extraer tendencia.
- **Limitaciones:** Documento de trabajo; las opiniones no comprometen al BCL.

#### DOC-MOT-0205 · Q 82 (A) — Does Hamilton's OLS Regression Provide a "Better Alternative" to the Hodrick-Prescott Filter? A New Zealand Business Cycle Perspective

- **Autores:** Viv B. Hall; Peter Thomson
- **Año:** 2020
- **Publicación o institución:** CAMA Working Paper 71/2020, Crawford School of Public Policy, The Australian National University
- **Tipo de documento:** Documento de trabajo de institución académica
- **Temática:** TM-02 Series temporales y detección de tendencias (principal)
- **Calidad Q:** 82 (A) — Tipo 20/25 · Rigor 16/20 · Autoridad 12/15 · Vigencia 9/10 · Impacto 5/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://crawford.anu.edu.au/sites/default/files/2025-01/71_2020_hall_thomson.pdf
- **Acceso y licencia:** Acceso abierto (ANU)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Hamilton 2018 "Why You Should Never Use the Hodrick-Prescott Filter" Review of Economics and Statistics»; WebFetch: sí)
- **Contenido:** Compara el filtro de Hamilton (H84) con HP1600 en el ciclo neozelandés: H84 exagera la volatilidad y da tendencias menos creíbles; los filtros HP extendidos con previsiones mejoran la estimación en los extremos de la muestra.
- **Uso en el Motor:** MC-02: tratamiento del problema de final de muestra en filtros de tendencia (extensión con previsiones).
- **Limitaciones:** Evidencia de un solo país; documento de trabajo.

#### DOC-MOT-0022 · Q 81 (A) — Rank Correlation Methods (4.ª ed.)

- **Autores:** Maurice G. Kendall
- **Año:** 1970 (4.ª ed.; a menudo citada por la reimpresión de 1975)
- **Publicación o institución:** Charles Griffin, Londres
- **Tipo de documento:** Libro académico
- **Temática:** TM-02 Series temporales y detección de tendencias (principal) · secundarias: TM-01
- **Calidad Q:** 81 (A) — Tipo 20/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 9/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** ISBN: 0852641990 · https://ci.nii.ac.jp/ncid/BA00860250 · https://search.worldcat.org/oclc/136868
- **Acceso y licencia:** Libro descatalogado; acceso en bibliotecas
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Kendall "Rank Correlation Methods" 4th edition 1970 OR 1975 Griffin London»; WebFetch: sí)
- **Contenido:** Monografía sobre la tau de Kendall y la rho de Spearman: distribución exacta y asintótica, tratamiento de empates, concordancia y contrastes basados en rangos; base teórica de la prueba de Mann-Kendall.
- **Uso en el Motor:** MC-02: estadístico tau de Kendall y su distribución, base de Mann-Kendall.
- **Limitaciones:** Edición antigua de acceso limitado. Corrección: la 4.ª edición es de 1970 según CiNii y WorldCat (la semilla indicaba 1975, fecha de reimpresión habitual en las citas).
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02 (año corregido).

#### DOC-MOT-0258 · Q 79 (B) — statsmodels: STL — Season-Trend Decomposition Using LOESS (documentación, v0.14.4)

- **Autores:** Equipo de desarrollo de statsmodels
- **Año:** Versión 0.14.4
- **Publicación o institución:** statsmodels.org
- **Tipo de documento:** Documentación técnica de software
- **Temática:** TM-02 Series temporales y detección de tendencias (principal) · secundarias: TM-14
- **Calidad Q:** 79 (B) — Tipo 15/25 · Rigor 14/20 · Autoridad 12/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** https://www.statsmodels.org/v0.14.4/generated/statsmodels.tsa.seasonal.STL.html
- **Acceso y licencia:** Abierto; software libre (BSD)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Cleveland 1990 "STL: A Seasonal-Trend Decomposition Procedure Based on Loess" Journal of Official Statistics»; WebFetch: sí)
- **Contenido:** Implementación Python de STL: periodo inferido o fijado, longitud del suavizador estacional (impar, ≥ 7) y ajuste robusto ponderado frente a atípicos.
- **Uso en el Motor:** MC-02: implementación de referencia de STL.
- **Limitaciones:** Documentación escueta sobre elección de parámetros.

#### DOC-MOT-0206 · Q 78 (B) — urca: ur.kpss — Kwiatkowski et al. Unit Root Test (documentación de función R)

- **Autores:** Bernhard Pfaff (autor y mantenedor); contribuciones de Eric Zivot y Matthieu Stigler
- **Año:** 2016 (versión 1.3-0 del paquete)
- **Publicación o institución:** Paquete R «urca» (CRAN), página de ayuda en quantargo.com
- **Tipo de documento:** Documentación técnica de software
- **Temática:** TM-02 Series temporales y detección de tendencias (principal) · secundarias: TM-04, TM-14
- **Calidad Q:** 78 (B) — Tipo 15/25 · Rigor 14/20 · Autoridad 12/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** https://www.quantargo.com/help/r/latest/packages/urca/1.3-0/ur.kpss.html
- **Acceso y licencia:** Abierto; software GPL (≥ 2)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Kwiatkowski Phillips Schmidt Shin 1992 "Testing the null hypothesis of stationarity against the alternative of a unit root" Journal of Econometrics 54»; WebFetch: sí)
- **Contenido:** Implementa KPSS con componente determinista «mu» o «tau» y reglas de retardos «short» (⁴√(4·n/100)) y «long» (⁴√(12·n/100)) o fijas; el paquete incluye además ADF, PP, ERS, Zivot-Andrews y Johansen.
- **Uso en el Motor:** MC-02, MC-03: implementación de referencia para validar contrastes de raíz unitaria y cointegración.
- **Limitaciones:** Página espejo (quantargo) en lugar de CRAN; versión documentada 1.3-0.

#### DOC-MOT-0207 · Q 77 (B) — EnvStats: kendallTrendTest — Kendall's Nonparametric Test for Monotonic Trend (documentación de función R)

- **Autores:** Steven P. Millard
- **Año:** Documentación vigente consultada en 2026
- **Publicación o institución:** Paquete R «EnvStats» (CRAN), página de ayuda en rdrr.io
- **Tipo de documento:** Documentación técnica de software
- **Temática:** TM-02 Series temporales y detección de tendencias (principal) · secundarias: TM-14
- **Calidad Q:** 77 (B) — Tipo 15/25 · Rigor 15/20 · Autoridad 11/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** https://rdrr.io/pkg/EnvStats/man/kendallTrendTest.html
- **Acceso y licencia:** Abierto; software libre (CRAN)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Mann 1945 "Nonparametric Tests Against Trend" Econometrica 13 245-259»; WebFetch: sí)
- **Contenido:** Implementa la prueba de Kendall/Mann de tendencia monótona (estadístico S, aproximación normal con corrección por empates y continuidad), pendiente de Theil-Sen, intercepto de Conover e intervalo de la pendiente de Gilbert; remite a la variante estacional de Hirsch et al. (1982).
- **Uso en el Motor:** MC-02: implementación de referencia de Mann-Kendall y Theil-Sen para validar código propio.
- **Limitaciones:** Supone independencia (no corrige autocorrelación); orientado a datos ambientales.

#### DOC-MOT-0208 · Q 73 (B) — RATS: @BAIPERRON Procedure (documentación técnica)

- **Autores:** Estima (RATS 11.1)
- **Año:** Documentación vigente consultada en 2026
- **Publicación o institución:** Estima — ayuda en línea de RATS
- **Tipo de documento:** Documentación técnica de software comercial
- **Temática:** TM-02 Series temporales y detección de tendencias (principal) · secundarias: TM-03
- **Calidad Q:** 73 (B) — Tipo 15/25 · Rigor 15/20 · Autoridad 11/15 · Vigencia 9/10 · Impacto 7/10 · Independencia 8/10 · Acceso 8/10
- **DOI / ISBN / URL:** https://estima.com/webhelp/topics/baiperronprocedure.html
- **Acceso y licencia:** Documentación abierta; software de pago
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Bai Perron 2003 "Computation and analysis of multiple structural change models" Journal of Applied Econometrics 10.1002/jae.659»; WebFetch: sí)
- **Contenido:** Implementación del algoritmo de Bai-Perron (2003) con opciones de separación mínima, número máximo de rupturas y regresores fijos; tabla BIC/LWZ/F para elegir el número de rupturas, intervalos de fechas y réplica del ejemplo británico de inflación.
- **Uso en el Motor:** MC-02: guía práctica de parametrización (trimming, criterios de selección) y advertencias (valores críticos no válidos con datos no estacionarios; tendencia segmentada continua no soportada).
- **Limitaciones:** Proveedor comercial (independencia menor); específico de RATS.

## TM-03 Volatilidad y regímenes

#### DOC-MOT-0218 · Q 97 (A) — Designing Realized Kernels to Measure the Ex Post Variation of Equity Prices in the Presence of Noise

- **Autores:** Ole E. Barndorff-Nielsen; Peter Reinhard Hansen; Asger Lunde; Neil Shephard
- **Año:** 2008
- **Publicación o institución:** Econometrica, 76(6), 1481-1536
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-03 Volatilidad y regímenes (principal) · secundarias: —
- **Calidad Q:** 97 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI: 10.3982/ECTA6495 · https://scholar.harvard.edu/sites/scholar.harvard.edu/files/ecta08.pdf
- **Acceso y licencia:** Copia del autor (Harvard) de acceso libre
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Realized variance wikipedia Andersen Bollerslev Barndorff-Nielsen Shephard bipower variation realized kernel»; WebFetch: sí)
- **Contenido:** Núcleos realizados: suma ponderada de autocovarianzas realizadas con pesos flat-top que corrige el sesgo del ruido de microestructura y alcanza la tasa de convergencia óptima.
- **Uso en el Motor:** MC-02: medición de volatilidad con datos tick a tick ruidosos.
- **Limitaciones:** Elección del ancho de banda; implementación más compleja que la RV a 5 minutos. DOI tomado de la página índice https://en.wikipedia.org/wiki/Realized_variance.

#### DOC-MOT-0217 · Q 97 (A) — Power and Bipower Variation with Stochastic Volatility and Jumps

- **Autores:** Ole E. Barndorff-Nielsen; Neil Shephard
- **Año:** 2004
- **Publicación o institución:** Journal of Financial Econometrics, 2(1), 1-37
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-03 Volatilidad y regímenes (principal) · secundarias: TM-08
- **Calidad Q:** 97 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** https://www.nuffield.ox.ac.uk/economics/papers/2003/w18/eric_may03.pdf (versión de trabajo, mayo de 2003) · cita publicada en https://en.wikipedia.org/wiki/Realized_variance
- **Acceso y licencia:** Versión de trabajo en Nuffield College (Oxford), acceso libre
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Realized variance wikipedia Andersen Bollerslev Barndorff-Nielsen Shephard bipower variation realized kernel»; WebFetch: sí)
- **Contenido:** Variación bipotencia realizada: estimador de la varianza integrada robusto a saltos; la diferencia con la varianza realizada estima la contribución de los saltos.
- **Uso en el Motor:** MC-02, MC-07: separación de componente continuo y saltos en volatilidad.
- **Limitaciones:** El índice imprime un DOI con prefijo dudoso; se omite. La URL es la versión de trabajo previa a la publicación.

#### DOC-MOT-0034 · Q 96 (A) — On the Relation between the Expected Value and the Volatility of the Nominal Excess Return on Stocks

- **Autores:** Lawrence R. Glosten; Ravi Jagannathan; David E. Runkle
- **Año:** 1993
- **Publicación o institución:** The Journal of Finance, 48(5), 1779-1801 (diciembre de 1993)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-03 Volatilidad y regímenes (principal) · secundarias: TM-08
- **Calidad Q:** 96 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** https://faculty.washington.edu/ezivot/econ589/GJRJOF1993.pdf · versión de trabajo: Federal Reserve Bank of Minneapolis (econpapers RePEc:fip:fedmsr:157)
- **Acceso y licencia:** Copia docente (Univ. de Washington) y versión de trabajo de la Fed de Minneapolis de acceso libre
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Glosten Jagannathan Runkle "On the Relation between the Expected Value and the Volatility of the Nominal Excess Return on Stocks" Journal of Finance 1993 48(5)»; WebFetch: sí)
- **Contenido:** Modelo GARCH asimétrico (GJR/TARCH) con término adicional para choques negativos; encuentra relación negativa entre rendimiento esperado y varianza condicional al controlar estacionalidad y tipos de interés.
- **Uso en el Motor:** MC-02: GARCH asimétrico (GJR) para el efecto apalancamiento.
- **Limitaciones:** Especificación paramétrica. Algunas fuentes secundarias lo citan erróneamente como 1992 / vol. 46; la portada impresa confirma 1993, vol. 48(5). DOI de la semilla no visto; se retira.
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02.

#### DOC-MOT-0037 · Q 95 (A) — Modeling and Forecasting Realized Volatility

- **Autores:** Torben G. Andersen; Tim Bollerslev; Francis X. Diebold; Paul Labys
- **Año:** 2003
- **Publicación o institución:** Econometrica, 71(2), 579-625
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-03 Volatilidad y regímenes (principal) · secundarias: TM-11
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1111/1468-0262.00418 · Verificada en página índice: https://en.wikipedia.org/wiki/Realized_variance
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Realized variance wikipedia Andersen Bollerslev Barndorff-Nielsen Shephard bipower variation realized kernel»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Realized_variance)
- **Contenido:** Marco de volatilidad realizada con datos intradía: la varianza realizada como medida observable de la varianza integrada y su modelización con VAR fraccionalmente integrado para prever volatilidades y correlaciones.
- **Uso en el Motor:** MC-02: volatilidad realizada como medida observable y su previsión.
- **Limitaciones:** Ruido de microestructura con muestreo muy fino. Confirmada solo mediante página índice (bibliografía de Wikipedia «Realized variance»); pendiente de lectura de la fuente primaria.
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02 (DOI confirmado en índice).

#### DOC-MOT-0210 · Q 95 (A) — Measuring and Testing the Impact of News on Volatility

- **Autores:** Robert F. Engle; Victor K. Ng
- **Año:** 1993
- **Publicación o institución:** The Journal of Finance, 48(5), 1749-1778
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-03 Volatilidad y regímenes (principal) · secundarias: —
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1111/j.1540-6261.1993.tb05127.x · Verificada en página índice: https://en.wikipedia.org/wiki/Autoregressive_conditional_heteroskedasticity (SSRN 262096)
- **Acceso y licencia:** Revista por suscripción; versión en SSRN
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Autoregressive conditional heteroskedasticity wikipedia GARCH EGARCH GJR references»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Autoregressive_conditional_heteroskedasticity)
- **Contenido:** Introduce la curva de impacto de noticias y los contrastes de sesgo de signo y de tamaño para diagnosticar asimetrías no recogidas por un GARCH.
- **Uso en el Motor:** MC-02: diagnóstico de asimetría antes de elegir GARCH, GJR o EGARCH.
- **Limitaciones:** Confirmada solo mediante página índice (bibliografía de Wikipedia «Autoregressive conditional heteroskedasticity»); pendiente de lectura de la fuente primaria.

#### DOC-MOT-0209 · Q 95 (A) — Conditional Heteroskedasticity in Asset Returns: A New Approach

- **Autores:** Daniel B. Nelson
- **Año:** 1991
- **Publicación o institución:** Econometrica, 59(2), 347-370
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-03 Volatilidad y regímenes (principal) · secundarias: TM-08
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.2307/2938260 · Verificada en página índice: https://en.wikipedia.org/wiki/Autoregressive_conditional_heteroskedasticity
- **Acceso y licencia:** Revista por suscripción (JSTOR 2938260)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Autoregressive conditional heteroskedasticity wikipedia GARCH EGARCH GJR references»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Autoregressive_conditional_heteroskedasticity)
- **Contenido:** Modelo EGARCH: el logaritmo de la varianza condicional responde asimétricamente al signo y al tamaño de los choques, sin restricciones de positividad.
- **Uso en el Motor:** MC-02: volatilidad asimétrica (EGARCH) en renta variable.
- **Limitaciones:** Confirmada solo mediante página índice (bibliografía de Wikipedia «Autoregressive conditional heteroskedasticity»); pendiente de lectura de la fuente primaria. Véase DOC-MOT-0228 sobre la interpretación de la asimetría.

#### DOC-MOT-0035 · Q 95 (A) — A New Approach to the Economic Analysis of Nonstationary Time Series and the Business Cycle

- **Autores:** James D. Hamilton
- **Año:** 1989
- **Publicación o institución:** Econometrica, 57(2), 357-384
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-03 Volatilidad y regímenes (principal) · secundarias: TM-04
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** Verificada en página índice: https://econweb.ucsd.edu/~jhamilto/palgrav1.pdf
- **Acceso y licencia:** Revista por suscripción (Econometrica/JSTOR)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Markov switching model wikipedia Hamilton 1989 regime switching references»; WebFetch: sí, sobre la página índice https://econweb.ucsd.edu/~jhamilto/palgrav1.pdf)
- **Contenido:** Introduce el modelo autorregresivo con cambio de régimen markoviano y el filtro de Hamilton para obtener probabilidades filtradas y suavizadas de cada régimen; aplicación a recesiones de EE. UU.
- **Uso en el Motor:** MC-02: cambio de régimen markoviano (probabilidades de régimen).
- **Limitaciones:** Número de regímenes fijado a priori; riesgo de sobreajuste. Confirmada solo mediante página índice (bibliografía de J. D. Hamilton, «Regime-Switching Models», 2005); pendiente de lectura de la fuente primaria. DOI de la semilla no visto; se retira.
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02.

#### DOC-MOT-0033 · Q 95 (A) — Generalized Autoregressive Conditional Heteroskedasticity

- **Autores:** Tim Bollerslev
- **Año:** 1986
- **Publicación o institución:** Journal of Econometrics, 31(3), 307-327
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-03 Volatilidad y regímenes (principal) · secundarias: TM-08
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1016/0304-4076(86)90063-1 · Verificada en página índice: https://en.wikipedia.org/wiki/Autoregressive_conditional_heteroskedasticity
- **Acceso y licencia:** Revista Elsevier por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Autoregressive conditional heteroskedasticity wikipedia GARCH EGARCH GJR references»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Autoregressive_conditional_heteroskedasticity)
- **Contenido:** Generaliza ARCH a GARCH(p,q): la varianza condicional depende de los cuadrados de los errores pasados y de sus propias varianzas pasadas; GARCH(1,1) es el estándar práctico.
- **Uso en el Motor:** MC-02, MC-07: GARCH(1,1) para volatilidad condicional y VaR.
- **Limitaciones:** Respuesta simétrica a choques (usar GJR/EGARCH ante apalancamiento). Confirmada solo mediante página índice (bibliografía de Wikipedia «Autoregressive conditional heteroskedasticity»); pendiente de lectura de la fuente primaria.
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02 (DOI confirmado en índice).

#### DOC-MOT-0032 · Q 95 (A) — Autoregressive Conditional Heteroscedasticity with Estimates of the Variance of United Kingdom Inflation

- **Autores:** Robert F. Engle
- **Año:** 1982
- **Publicación o institución:** Econometrica, 50(4), 987-1007
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-03 Volatilidad y regímenes (principal) · secundarias: —
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.2307/1912773 · Verificada en página índice: https://en.wikipedia.org/wiki/Autoregressive_conditional_heteroskedasticity
- **Acceso y licencia:** Revista por suscripción (JSTOR 1912773)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Autoregressive conditional heteroskedasticity wikipedia GARCH EGARCH GJR references»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Autoregressive_conditional_heteroskedasticity)
- **Contenido:** Introduce el modelo ARCH (varianza condicional función de errores cuadráticos pasados), su estimación por máxima verosimilitud y el contraste LM de efectos ARCH.
- **Uso en el Motor:** MC-02: modelo ARCH y contraste de heterocedasticidad condicional.
- **Limitaciones:** Superado en la práctica por GARCH. Confirmada solo mediante página índice (bibliografía de Wikipedia «Autoregressive conditional heteroskedasticity»); pendiente de lectura de la fuente primaria.
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02 (DOI confirmado en índice).

#### DOC-MOT-0036 · Q 94 (A) — A Simple Approximate Long-Memory Model of Realized Volatility

- **Autores:** Fulvio Corsi
- **Año:** 2009
- **Publicación o institución:** Journal of Financial Econometrics, 7(2), 174-196
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-03 Volatilidad y regímenes (principal) · secundarias: —
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** Verificada en página índice: https://en.wikipedia.org/wiki/Realized_variance
- **Acceso y licencia:** Revista OUP por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Realized variance wikipedia Andersen Bollerslev Barndorff-Nielsen Shephard bipower variation realized kernel»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Realized_variance)
- **Contenido:** Modelo HAR-RV: la volatilidad realizada se proyecta sobre sus medias diaria, semanal y mensual, reproduciendo memoria larga aproximada con MCO.
- **Uso en el Motor:** MC-02: HAR-RV para previsión de volatilidad realizada (horizontes H1-H2).
- **Limitaciones:** Requiere datos intradía. Confirmada solo mediante página índice (bibliografía de Wikipedia «Realized variance»); pendiente de lectura de la fuente primaria. El índice imprime el DOI con prefijo dudoso (jfinec/jjfinec); se omite hasta confirmarlo.
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02.

#### DOC-MOT-0219 · Q 94 (A) — A Tale of Two Time Scales: Determining Integrated Volatility with Noisy High-Frequency Data

- **Autores:** Lan Zhang; Per A. Mykland; Yacine Aït-Sahalia
- **Año:** 2005
- **Publicación o institución:** Journal of the American Statistical Association, 100(472), 1394-1411
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-03 Volatilidad y regímenes (principal) · secundarias: —
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1198/016214505000000169 · Verificada en página índice: https://en.wikipedia.org/wiki/Realized_variance
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Realized variance wikipedia Andersen Bollerslev Barndorff-Nielsen Shephard bipower variation realized kernel»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Realized_variance)
- **Contenido:** Estimador de dos escalas temporales (TSRV): combina varianzas realizadas submuestreadas y a máxima frecuencia para eliminar el sesgo del ruido, primer estimador consistente en ese marco.
- **Uso en el Motor:** MC-02: alternativa a núcleos realizados para volatilidad con ruido.
- **Limitaciones:** Confirmada solo mediante página índice (bibliografía de Wikipedia «Realized variance»); pendiente de lectura de la fuente primaria.

#### DOC-MOT-0214 · Q 94 (A) — Dynamic Conditional Correlation: A Simple Class of Multivariate Generalized Autoregressive Conditional Heteroskedasticity Models

- **Autores:** Robert F. Engle
- **Año:** 2002
- **Publicación o institución:** Journal of Business & Economic Statistics, 20(3), 339-350
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-03 Volatilidad y regímenes (principal) · secundarias: TM-07
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** https://ideas.repec.org/a/bes/jnlbes/v20y2002i3p339-50.html · versión de trabajo NYU: https://archive.nyu.edu/handle/2451/26879
- **Acceso y licencia:** Ficha RePEc abierta; texto de revista por suscripción; versión de trabajo en el repositorio de NYU
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Engle 2002 Dynamic Conditional Correlation Journal of Business Economic Statistics multivariate GARCH»; WebFetch: sí)
- **Contenido:** Modelo DCC: GARCH univariantes para cada activo y una dinámica GARCH escalar para la matriz de correlaciones de los residuos estandarizados, estimable en dos etapas.
- **Uso en el Motor:** MC-02, MC-07: correlaciones condicionales variables para carteras y cobertura.
- **Limitaciones:** Dinámica común a todas las correlaciones; sesgo en dimensiones grandes.

#### DOC-MOT-0216 · Q 94 (A) — Econometric Analysis of Realised Volatility and Its Use in Estimating Stochastic Volatility Models

- **Autores:** Ole E. Barndorff-Nielsen; Neil Shephard
- **Año:** 2002
- **Publicación o institución:** Journal of the Royal Statistical Society, Series B, 64(2), 253-280
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-03 Volatilidad y regímenes (principal) · secundarias: —
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1111/1467-9868.00336 · Verificada en página índice: https://en.wikipedia.org/wiki/Realized_variance
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Realized variance wikipedia Andersen Bollerslev Barndorff-Nielsen Shephard bipower variation realized kernel»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Realized_variance)
- **Contenido:** Teoría asintótica de la varianza realizada como estimador de la varianza integrada (distribución mixta normal y cuarticidad) y su uso para estimar modelos de volatilidad estocástica.
- **Uso en el Motor:** MC-02: intervalos de confianza para la volatilidad realizada.
- **Limitaciones:** Supone ausencia de ruido de microestructura y de saltos. Confirmada solo mediante página índice (bibliografía de Wikipedia «Realized variance»); pendiente de lectura de la fuente primaria.

#### DOC-MOT-0215 · Q 94 (A) — Answering the Skeptics: Yes, Standard Volatility Models Do Provide Accurate Forecasts

- **Autores:** Torben G. Andersen; Tim Bollerslev
- **Año:** 1998
- **Publicación o institución:** International Economic Review, 39(4), 885-905
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-03 Volatilidad y regímenes (principal) · secundarias: TM-11
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.2307/2527343 · Verificada en página índice: https://en.wikipedia.org/wiki/Realized_variance
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Realized variance wikipedia Andersen Bollerslev Barndorff-Nielsen Shephard bipower variation realized kernel»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Realized_variance)
- **Contenido:** Demuestra que el bajo R² de las previsiones GARCH frente a rendimientos al cuadrado se debe al ruido del proxy; usando varianza realizada intradía las previsiones son precisas.
- **Uso en el Motor:** MC-02, MC-10: elección del proxy de volatilidad al evaluar previsiones.
- **Limitaciones:** Confirmada solo mediante página índice (bibliografía de Wikipedia «Realized variance»); pendiente de lectura de la fuente primaria.

#### DOC-MOT-0220 · Q 93 (A) — Does Anything Beat 5-Minute RV? A Comparison of Realized Measures Across Multiple Asset Classes

- **Autores:** Lily Y. Liu; Andrew J. Patton; Kevin Sheppard
- **Año:** 2015
- **Publicación o institución:** Journal of Econometrics, 187(1), 293-311
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-03 Volatilidad y regímenes (principal) · secundarias: TM-11
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1016/j.jeconom.2015.02.008 · Verificada en página índice: https://en.wikipedia.org/wiki/Realized_variance
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Realized variance wikipedia Andersen Bollerslev Barndorff-Nielsen Shephard bipower variation realized kernel»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Realized_variance)
- **Contenido:** Compara más de 400 medidas realizadas en 31 activos de varias clases con el Model Confidence Set: la RV a 5 minutos es difícil de batir de forma significativa.
- **Uso en el Motor:** MC-02: elección por defecto de la medida realizada (RV 5 min) y justificación documentada.
- **Limitaciones:** Confirmada solo mediante página índice (bibliografía de Wikipedia «Realized variance»); pendiente de lectura de la fuente primaria.

#### DOC-MOT-0221 · Q 93 (A) — Good Volatility, Bad Volatility: Signed Jumps and the Persistence of Volatility

- **Autores:** Andrew J. Patton; Kevin Sheppard
- **Año:** 2015
- **Publicación o institución:** The Review of Economics and Statistics, 97(3), 683-697
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-03 Volatilidad y regímenes (principal) · secundarias: TM-08
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1162/REST_a_00503 · Verificada en página índice: https://en.wikipedia.org/wiki/Realized_variance
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Realized variance wikipedia Andersen Bollerslev Barndorff-Nielsen Shephard bipower variation realized kernel»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Realized_variance)
- **Contenido:** Descompone la volatilidad realizada en semivarianzas positiva y negativa y saltos con signo; la volatilidad «mala» (negativa) predice mejor la volatilidad futura (HAR extendido).
- **Uso en el Motor:** MC-02: previsión de volatilidad con semivarianzas; señales de riesgo bajista.
- **Limitaciones:** Confirmada solo mediante página índice (bibliografía de Wikipedia «Realized variance»); pendiente de lectura de la fuente primaria.

#### DOC-MOT-0222 · Q 93 (A) — Roughing It Up: Including Jump Components in the Measurement, Modeling, and Forecasting of Return Volatility

- **Autores:** Torben G. Andersen; Tim Bollerslev; Francis X. Diebold
- **Año:** 2007
- **Publicación o institución:** The Review of Economics and Statistics, 89(4), 701-720
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-03 Volatilidad y regímenes (principal) · secundarias: TM-08
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1162/rest.89.4.701 · Verificada en página índice: https://en.wikipedia.org/wiki/Realized_variance
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Realized variance wikipedia Andersen Bollerslev Barndorff-Nielsen Shephard bipower variation realized kernel»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Realized_variance)
- **Contenido:** Separa la componente de saltos con variación bipotencia y muestra que el modelo HAR-RV-CJ (continuo y saltos separados) mejora las previsiones; los saltos son poco persistentes.
- **Uso en el Motor:** MC-02: HAR con saltos para previsión de volatilidad.
- **Limitaciones:** Confirmada solo mediante página índice (bibliografía de Wikipedia «Realized variance»); pendiente de lectura de la fuente primaria.

#### DOC-MOT-0225 · Q 93 (A) — Autoregressive Conditional Heteroskedasticity and Changes in Regime

- **Autores:** James D. Hamilton; Raul Susmel
- **Año:** 1994
- **Publicación o institución:** Journal of Econometrics, 64, 307-333
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-03 Volatilidad y regímenes (principal) · secundarias: —
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** Verificada en página índice: https://econweb.ucsd.edu/~jhamilto/palgrav1.pdf
- **Acceso y licencia:** Revista Elsevier por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Markov switching model wikipedia Hamilton 1989 regime switching references»; WebFetch: sí, sobre la página índice https://econweb.ucsd.edu/~jhamilto/palgrav1.pdf)
- **Contenido:** Modelo SWARCH: parámetros ARCH sujetos a cambios de régimen markovianos; reduce la persistencia espuria de la volatilidad que GARCH atribuye a la memoria.
- **Uso en el Motor:** MC-02: volatilidad con regímenes (alta/baja) para detección de cambios de régimen.
- **Limitaciones:** Confirmada solo mediante página índice (bibliografía de J. D. Hamilton, «Regime-Switching Models»); pendiente de lectura de la fuente primaria.

#### DOC-MOT-0226 · Q 91 (A) — A New Approach to Markov-Switching GARCH Models

- **Autores:** Markus Haas; Stefan Mittnik; Marc S. Paolella
- **Año:** 2004
- **Publicación o institución:** Journal of Financial Econometrics, 2, 493-530
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-03 Volatilidad y regímenes (principal) · secundarias: —
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** Verificada en página índice: https://econweb.ucsd.edu/~jhamilto/palgrav1.pdf
- **Acceso y licencia:** Revista OUP por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Markov switching model wikipedia Hamilton 1989 regime switching references»; WebFetch: sí, sobre la página índice https://econweb.ucsd.edu/~jhamilto/palgrav1.pdf)
- **Contenido:** MS-GARCH con procesos de varianza paralelos por régimen que evita la dependencia de la trayectoria y permite estimación por máxima verosimilitud.
- **Uso en el Motor:** MC-02: GARCH con regímenes estimable de forma tratable.
- **Limitaciones:** Confirmada solo mediante página índice (bibliografía de J. D. Hamilton, «Regime-Switching Models»); pendiente de lectura de la fuente primaria.

#### DOC-MOT-0038 · Q 90 (A) — Regime Changes and Financial Markets

- **Autores:** Andrew Ang; Allan Timmermann
- **Año:** 2012
- **Publicación o institución:** Annual Review of Financial Economics, 4(1), 313-337; versión de trabajo NBER WP 17182 (2011)
- **Tipo de documento:** Artículo de revisión revisado por pares
- **Temática:** TM-03 Volatilidad y regímenes (principal) · secundarias: TM-07
- **Calidad Q:** 90 (A) — Tipo 22/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** DOI: 10.3386/w17182 (documento de trabajo) · https://www.nber.org/papers/w17182 · https://ideas.repec.org/p/nbr/nberwo/17182.html
- **Acceso y licencia:** Documento de trabajo NBER accesible; revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Ang Timmermann "Regime Changes and Financial Markets" Annual Review of Financial Economics 2012»; WebFetch: sí)
- **Contenido:** Revisión de modelos de cambio de régimen en finanzas: regímenes con medias, volatilidades, autocorrelaciones y covarianzas distintas explican colas gruesas, volatilidad cambiante y correlaciones variables; efectos en valoración y asignación de carteras.
- **Uso en el Motor:** MC-02, MC-07: revisión de modelos de régimen y su uso en asignación de activos.
- **Limitaciones:** Revisión, no método nuevo. DOI de revista no visto (se da el del documento NBER).
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02.

#### DOC-MOT-0211 · Q 90 (A) — GARCH 101: The Use of ARCH/GARCH Models in Applied Econometrics

- **Autores:** Robert F. Engle
- **Año:** 2001
- **Publicación o institución:** Journal of Economic Perspectives, 15(4), 157-168
- **Tipo de documento:** Artículo revisado por pares (divulgativo-técnico)
- **Temática:** TM-03 Volatilidad y regímenes (principal) · secundarias: TM-08
- **Calidad Q:** 90 (A) — Tipo 23/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI: 10.1257/jep.15.4.157 · Verificada en página índice: https://en.wikipedia.org/wiki/Autoregressive_conditional_heteroskedasticity
- **Acceso y licencia:** JEP es de acceso abierto en la web de la AEA
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Autoregressive conditional heteroskedasticity wikipedia GARCH EGARCH GJR references»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Autoregressive_conditional_heteroskedasticity)
- **Contenido:** Introducción aplicada a ARCH/GARCH: especificación, estimación, previsión de varianza a varios horizontes y uso en VaR, con ejemplo de cartera.
- **Uso en el Motor:** MC-02, MC-07: guía operativa para documentar el uso de GARCH en el Motor.
- **Limitaciones:** Texto introductorio; no cubre modelos multivariantes ni realizados. Confirmada solo mediante página índice (bibliografía de Wikipedia «Autoregressive conditional heteroskedasticity»); pendiente de lectura de la fuente primaria.

#### DOC-MOT-0213 · Q 89 (A) — Modelling Volatility Cycles: The MF2-GARCH Model

- **Autores:** Christian M. Conrad; Robert F. Engle
- **Año:** 2025
- **Publicación o institución:** Journal of Applied Econometrics, 40, 438-454
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-03 Volatilidad y regímenes (principal) · secundarias: TM-02
- **Calidad Q:** 89 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 4/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI: 10.1002/jae.3118 · Verificada en página índice: https://en.wikipedia.org/wiki/Autoregressive_conditional_heteroskedasticity (hdl:10419/323894, EconStor)
- **Acceso y licencia:** Copia en EconStor (acceso abierto) según el índice
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Autoregressive conditional heteroskedasticity wikipedia GARCH EGARCH GJR references»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Autoregressive_conditional_heteroskedasticity)
- **Contenido:** GARCH multiplicativo de dos componentes (corto y largo plazo) que capta ciclos de volatilidad de baja frecuencia y mejora la previsión a horizontes largos.
- **Uso en el Motor:** MC-02: previsión de volatilidad a horizontes H2-H3 con componente de largo plazo.
- **Limitaciones:** Muy reciente; escasa evidencia independiente. Confirmada solo mediante página índice (bibliografía de Wikipedia «Autoregressive conditional heteroskedasticity»); pendiente de lectura de la fuente primaria.

#### DOC-MOT-0224 · Q 89 (A) — Regime-Switching Models

- **Autores:** James D. Hamilton
- **Año:** 2005
- **Publicación o institución:** Preparado para The New Palgrave Dictionary of Economics (versión de 18/05/2005, UC San Diego)
- **Tipo de documento:** Artículo de referencia (entrada de diccionario académico)
- **Temática:** TM-03 Volatilidad y regímenes (principal) · secundarias: TM-04
- **Calidad Q:** 89 (A) — Tipo 20/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://econweb.ucsd.edu/~jhamilto/palgrav1.pdf
- **Acceso y licencia:** Copia del autor de acceso libre
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Markov switching model wikipedia Hamilton 1989 regime switching references»; WebFetch: sí)
- **Contenido:** Síntesis del autor del método: modelo de Markov con regímenes, filtro y suavizado, estimación por EM, contrastes de especificación, probabilidades de transición variables y aplicaciones, con amplia bibliografía.
- **Uso en el Motor:** MC-02: referencia compacta para implementar y documentar modelos de régimen.
- **Limitaciones:** Versión previa a la publicación; bibliografía hasta 2005.

#### DOC-MOT-0228 · Q 88 (A) — Asymmetry and Leverage in Conditional Volatility Models

- **Autores:** Michael McAleer
- **Año:** 2014
- **Publicación o institución:** Econometrics (MDPI), 2(3), 145-150
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-03 Volatilidad y regímenes (principal) · secundarias: TM-01
- **Calidad Q:** 88 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 5/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** DOI: 10.3390/econometrics2030145 · https://www.kier.kyoto-u.ac.jp/wp/wp-content/uploads/2021/07/Asymmetry-and-Leverage-in-Conditional-Volatility-Models.pdf
- **Acceso y licencia:** Acceso abierto (CC BY)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Autoregressive conditional heteroskedasticity wikipedia GARCH EGARCH GJR references»; WebFetch: sí)
- **Contenido:** Deriva GJR desde un proceso autorregresivo de coeficientes aleatorios y muestra que ni GJR ni EGARCH capturan apalancamiento en sentido estricto, solo asimetría; interpretación unificada de parámetros.
- **Uso en el Motor:** MC-02: interpretación correcta de parámetros asimétricos en informes del Motor.
- **Limitaciones:** Nota breve; cita GJR con año y volumen erróneos (1992, vol. 46).

#### DOC-MOT-0227 · Q 86 (A) — State-Space Models with Regime Switching: Classical and Gibbs-Sampling Approaches with Applications

- **Autores:** Chang-Jin Kim; Charles R. Nelson
- **Año:** 1999
- **Publicación o institución:** MIT Press
- **Tipo de documento:** Manual de referencia
- **Temática:** TM-03 Volatilidad y regímenes (principal) · secundarias: TM-02, TM-04
- **Calidad Q:** 86 (A) — Tipo 20/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** Verificada en páginas índice: https://econweb.ucsd.edu/~jhamilto/palgrav1.pdf · https://www.statsmodels.org/v0.14.4/generated/statsmodels.tsa.regime_switching.markov_regression.MarkovRegression.html
- **Acceso y licencia:** Libro de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Markov switching model wikipedia Hamilton 1989 regime switching references»; WebFetch: sí, sobre la página índice https://econweb.ucsd.edu/~jhamilto/palgrav1.pdf)
- **Contenido:** Manual de modelos de espacio de estados con regímenes: filtro de Kim, estimación clásica y bayesiana (Gibbs), con código y aplicaciones a ciclo y finanzas.
- **Uso en el Motor:** MC-02: base metodológica de MarkovRegression de statsmodels (suavizador de Kim).
- **Limitaciones:** Edición de 1999. Confirmada solo mediante página índice (bibliografía de J. D. Hamilton y documentación de statsmodels); pendiente de lectura de la fuente primaria.

#### DOC-MOT-0212 · Q 83 (A) — Chapter 8: Glossary to ARCH (GARCH)

- **Autores:** Tim Bollerslev
- **Año:** 2010
- **Publicación o institución:** En T. Bollerslev, J. Russell y M. Watson (eds.), Volatility and Time Series Econometrics: Essays in Honor of Robert Engle, Oxford University Press, 137-163
- **Tipo de documento:** Capítulo de libro académico
- **Temática:** TM-03 Volatilidad y regímenes (principal) · secundarias: —
- **Calidad Q:** 83 (A) — Tipo 20/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** ISBN: 9780199549498 · verificada en página índice: https://en.wikipedia.org/wiki/Autoregressive_conditional_heteroskedasticity
- **Acceso y licencia:** Libro de pago (OUP)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Autoregressive conditional heteroskedasticity wikipedia GARCH EGARCH GJR references»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Autoregressive_conditional_heteroskedasticity)
- **Contenido:** Glosario de más de un centenar de variantes de la familia ARCH con su definición formal y referencia original.
- **Uso en el Motor:** MC-02: tabla de equivalencias y nomenclatura de modelos de volatilidad.
- **Limitaciones:** Catálogo, no evaluación comparada. El índice lo atribuye a Bollerslev, Russell y Watson; los tres son los editores del volumen y el capítulo es de T. Bollerslev. Confirmada solo mediante página índice (bibliografía de Wikipedia «Autoregressive conditional heteroskedasticity»); pendiente de lectura de la fuente primaria.

#### DOC-MOT-0230 · Q 82 (A) — arch: Autoregressive Conditional Heteroskedasticity (ARCH) and Other Tools for Financial Econometrics in Python

- **Autores:** Kevin Sheppard (cuenta bashtage) y colaboradores
- **Año:** Versión vigente consultada en 2026
- **Publicación o institución:** Repositorio GitHub bashtage/arch; documentación en arch.readthedocs.org
- **Tipo de documento:** Documentación técnica de software
- **Temática:** TM-03 Volatilidad y regímenes (principal) · secundarias: TM-01, TM-02, TM-04
- **Calidad Q:** 82 (A) — Tipo 15/25 · Rigor 15/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** DOI: 10.5281/zenodo.593254 · https://github.com/bashtage/arch
- **Acceso y licencia:** Software libre (licencia en LICENSE.md)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «arch python package Kevin Sheppard documentation volatility models bibliography»; WebFetch: sí)
- **Contenido:** Biblioteca Python: GARCH, TARCH, EGARCH, EWMA con medias HAR/AR y errores normales, t o GED; contrastes de raíz unitaria (ADF, DF-GLS, PP, KPSS, Zivot-Andrews, ratio de varianzas), cointegración (Engle-Granger, Phillips-Ouliaris, DOLS, FMOLS), bootstraps i.i.d., estacionario y por bloques, SPA/StepM/MCS y varianza de largo plazo con ancho automático.
- **Uso en el Motor:** MC-02, MC-03, MC-10: implementación de referencia en Python para volatilidad, raíces unitarias, bootstrap y comparación múltiple.
- **Limitaciones:** La documentación en readthedocs no pudo leerse con WebFetch (dominio no admitido); la licencia no figura en la página leída.

#### DOC-MOT-0223 · Q 81 (A) — Advances in Forecasting Realized Volatility: A Review of Methodologies

- **Autores:** R. M. Leushuis; N. Petkov
- **Año:** 2026
- **Publicación o institución:** Financial Innovation, 12, 14 (Springer, acceso abierto)
- **Tipo de documento:** Artículo de revisión revisado por pares
- **Temática:** TM-03 Volatilidad y regímenes (principal) · secundarias: TM-10
- **Calidad Q:** 81 (A) — Tipo 23/25 · Rigor 15/20 · Autoridad 11/15 · Vigencia 10/10 · Impacto 3/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** DOI: 10.1186/s40854-025-00809-5 · Verificada en página índice: https://en.wikipedia.org/wiki/Realized_variance
- **Acceso y licencia:** Revista de acceso abierto (SpringerOpen)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Realized variance wikipedia Andersen Bollerslev Barndorff-Nielsen Shephard bipower variation realized kernel»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Realized_variance)
- **Contenido:** Revisión reciente de métodos de previsión de volatilidad realizada: familia HAR, modelos con saltos y semivarianzas, componentes de largo plazo y aprendizaje automático.
- **Uso en el Motor:** MC-02, MC-10: mapa actualizado de alternativas al HAR-RV.
- **Limitaciones:** Muy reciente; impacto aún no medible. Confirmada solo mediante página índice (bibliografía de Wikipedia «Realized variance»); pendiente de lectura de la fuente primaria.

#### DOC-MOT-0229 · Q 81 (A) — The Correct Regularity Condition and Interpretation of Asymmetry in EGARCH

- **Autores:** Chia-Lin Chang; Michael McAleer
- **Año:** 2017
- **Publicación o institución:** Documento de Trabajo n.º 1717, Instituto Complutense de Análisis Económico (ICAE), Universidad Complutense de Madrid; también Econometric Institute Report EI2017-17 (Erasmus)
- **Tipo de documento:** Documento de trabajo de institución académica
- **Temática:** TM-03 Volatilidad y regímenes (principal) · secundarias: TM-01
- **Calidad Q:** 81 (A) — Tipo 20/25 · Rigor 15/20 · Autoridad 12/15 · Vigencia 10/10 · Impacto 4/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://docta.ucm.es/bitstreams/cbbf4fa5-86b7-462f-a963-8af52140ee47/download · https://repub.eur.nl/pub/100416/EI2017-17-Report.pdf
- **Acceso y licencia:** Acceso abierto (repositorios UCM y Erasmus)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Autoregressive conditional heteroskedasticity wikipedia GARCH EGARCH GJR references»; WebFetch: sí)
- **Contenido:** Deriva la condición de regularidad de la asimetría en EGARCH: la simetría exige α = 0 (no γ = 0); como α suele ser significativo, EGARCH muestra asimetría pero no apalancamiento.
- **Uso en el Motor:** MC-02: contraste correcto de asimetría al estimar EGARCH.
- **Limitaciones:** Documento de trabajo; postura de un grupo de autores.

#### DOC-MOT-0231 · Q 79 (B) — statsmodels: MarkovRegression (documentación, v0.14.4)

- **Autores:** Equipo de desarrollo de statsmodels
- **Año:** Versión 0.14.4
- **Publicación o institución:** statsmodels.org
- **Tipo de documento:** Documentación técnica de software
- **Temática:** TM-03 Volatilidad y regímenes (principal) · secundarias: TM-02
- **Calidad Q:** 79 (B) — Tipo 15/25 · Rigor 14/20 · Autoridad 12/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** https://www.statsmodels.org/v0.14.4/generated/statsmodels.tsa.regime_switching.markov_regression.MarkovRegression.html
- **Acceso y licencia:** Abierto; software libre (BSD)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «statsmodels time series analysis tsa documentation references Markov switching regression»; WebFetch: sí)
- **Contenido:** Regresión con cambio de régimen markoviano de k regímenes: coeficientes y varianza conmutables, probabilidades de transición variables, estimación por máxima verosimilitud con filtro de Hamilton y suavizado de Kim.
- **Uso en el Motor:** MC-02: implementación de referencia en Python de modelos de régimen.
- **Limitaciones:** API declarada no estable; documentación escueta.

## TM-04 Econometría y causalidad

#### DOC-MOT-0246 · Q 96 (A) — Macroeconomic Forecasting Using Diffusion Indexes

- **Autores:** James H. Stock; Mark W. Watson
- **Año:** 2002
- **Publicación o institución:** Journal of Business & Economic Statistics, 20(2), 147-162
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-04 Econometría y causalidad (principal) · secundarias: TM-10
- **Calidad Q:** 96 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** https://scholar.harvard.edu/sites/scholar.harvard.edu/files/stock/files/macroeconomic_forecasting_using_diffusion_indexes.pdf
- **Acceso y licencia:** Copia del autor (Harvard) de acceso libre
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Stock Watson 2002 "Forecasting Using Principal Components From a Large Number of Predictors" JASA 97»; WebFetch: sí)
- **Contenido:** Aplicación empírica de índices de difusión: con 215 predictores mensuales, los factores por componentes principales baten a AR, VAR pequeños e indicadores adelantados (1970-1998).
- **Uso en el Motor:** MC-03, MC-06: evidencia y procedimiento para nowcasting con factores.
- **Limitaciones:** Datos de EE. UU. hasta 1998.

#### DOC-MOT-0044 · Q 95 (A) — Estimation and Inference of Impulse Responses by Local Projections

- **Autores:** Òscar Jordà
- **Año:** 2005
- **Publicación o institución:** American Economic Review, 95(1), 161-182
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-04 Econometría y causalidad (principal) · secundarias: TM-02
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1257/0002828053828518 · https://www.citedrive.com/en/discovery/estimation-and-inference-of-impulse-responses-by-local-projections (DOI) · referencia completa en https://cran.r-universe.dev/lpirfs/doc/manual.html
- **Acceso y licencia:** Revista AEA por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Jordà 2005 "Estimation and Inference of Impulse Responses by Local Projections" American Economic Review 95»; WebFetch: sí)
- **Contenido:** Estima funciones impulso-respuesta mediante una regresión distinta para cada horizonte (proyecciones locales), robusta a errores de especificación del VAR y extensible a no linealidades.
- **Uso en el Motor:** MC-03: impulso-respuesta por proyecciones locales.
- **Limitaciones:** Mayor varianza que el VAR en muestras cortas.
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02 (DOI confirmado).

#### DOC-MOT-0045 · Q 95 (A) — Forecasting Using Principal Components from a Large Number of Predictors

- **Autores:** James H. Stock; Mark W. Watson
- **Año:** 2002
- **Publicación o institución:** Journal of the American Statistical Association, 97(460), 1167-1179
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-04 Econometría y causalidad (principal) · secundarias: TM-10
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** https://stock.scholars.harvard.edu/publications/forecasting-using-principal-components-large-number-predictors
- **Acceso y licencia:** Ficha del autor (Harvard); revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Stock Watson 2002 "Forecasting Using Principal Components From a Large Number of Predictors" JASA 97»; WebFetch: sí)
- **Contenido:** Muestra que los componentes principales de un panel grande de predictores estiman de forma consistente los factores de un modelo de factores aproximado y producen previsiones eficientes (índices de difusión).
- **Uso en el Motor:** MC-03, MC-06: índices de difusión y modelos de factores para nowcasting con muchos predictores.
- **Limitaciones:** Factores sin interpretación económica directa. DOI de la semilla no visto; se retira.
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02.

#### DOC-MOT-0040 · Q 95 (A) — Estimation and Hypothesis Testing of Cointegration Vectors in Gaussian Vector Autoregressive Models

- **Autores:** Søren Johansen
- **Año:** 1991
- **Publicación o institución:** Econometrica, 59(6), 1551-1580
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-04 Econometría y causalidad (principal) · secundarias: TM-02
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** https://ideas.repec.org/a/ecm/emetrp/v59y1991i6p1551-80.html
- **Acceso y licencia:** Ficha RePEc abierta; texto por suscripción (JSTOR)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Johansen 1991 "Estimation and Hypothesis Testing of Cointegration Vectors in Gaussian Vector Autoregressive Models" Econometrica 59»; WebFetch: sí)
- **Contenido:** Estimación por máxima verosimilitud de VAR con cointegración (rango reducido) y contrastes de traza y máximo autovalor para el número de relaciones de cointegración, con restricciones lineales sobre los vectores.
- **Uso en el Motor:** MC-03: contraste de rango de cointegración en VAR (traza y máximo autovalor).
- **Limitaciones:** Sensible al orden del VAR y a la especificación determinista. DOI de la semilla no visto; se retira.
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02.

#### DOC-MOT-0232 · Q 95 (A) — Heteroskedasticity and Autocorrelation Consistent Covariance Matrix Estimation

- **Autores:** Donald W. K. Andrews
- **Año:** 1991
- **Publicación o institución:** Econometrica, 59(3), 817-858
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-04 Econometría y causalidad (principal) · secundarias: TM-01
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.2307/2938229 · Verificada en páginas índice: https://en.wikipedia.org/wiki/Newey%E2%80%93West_estimator · https://rdrr.io/pkg/sandwich/man/NeweyWest.html
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Newey–West estimator wikipedia heteroskedasticity and autocorrelation consistent Andrews 1991 bandwidth»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Newey%E2%80%93West_estimator)
- **Contenido:** Teoría de los estimadores HAC con núcleo: núcleo espectral cuadrático óptimo y selección automática del ancho de banda mediante aproximación AR(1)/VAR.
- **Uso en el Motor:** MC-01, MC-03: elección de núcleo y ancho de banda de errores HAC.
- **Limitaciones:** Confirmada solo mediante página índice (bibliografía de Wikipedia «Newey–West estimator» y ayuda de sandwich); pendiente de lectura de la fuente primaria.

#### DOC-MOT-0039 · Q 95 (A) — Co-Integration and Error Correction: Representation, Estimation, and Testing

- **Autores:** Robert F. Engle; Clive W. J. Granger
- **Año:** 1987
- **Publicación o institución:** Econometrica, 55(2), 251-276
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-04 Econometría y causalidad (principal) · secundarias: TM-02
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.2307/1913236 · Verificada en página índice: https://en.wikipedia.org/wiki/Cointegration
- **Acceso y licencia:** Revista por suscripción (JSTOR 1913236)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Cointegration wikipedia Engle-Granger Johansen test Phillips-Ouliaris references»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Cointegration)
- **Contenido:** Define la cointegración, el teorema de representación de Granger (equivalencia con modelos de corrección del error) y el método en dos etapas con contraste de raíz unitaria sobre los residuos.
- **Uso en el Motor:** MC-03: cointegración en dos etapas y modelos de corrección del error (pares de activos, relaciones de largo plazo).
- **Limitaciones:** Una sola relación de cointegración; sesgo en muestras cortas. Confirmada solo mediante página índice (bibliografía de Wikipedia «Cointegration»); pendiente de lectura de la fuente primaria.
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02 (DOI confirmado en índice).

#### DOC-MOT-0236 · Q 95 (A) — A Heteroskedasticity-Consistent Covariance Matrix Estimator and a Direct Test for Heteroskedasticity

- **Autores:** Halbert White
- **Año:** 1980
- **Publicación o institución:** Econometrica, 48(4), 817-838
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-04 Econometría y causalidad (principal) · secundarias: TM-01
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.2307/1912934 · Verificada en página índice: https://en.wikipedia.org/wiki/Heteroskedasticity-consistent_standard_errors
- **Acceso y licencia:** Revista por suscripción (JSTOR 1912934)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Heteroskedasticity-consistent standard errors wikipedia White 1980 MacKinnon White 1985»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Heteroskedasticity-consistent_standard_errors)
- **Contenido:** Estimador de covarianzas robusto a heterocedasticidad de forma desconocida (HC0) y contraste directo de heterocedasticidad.
- **Uso en el Motor:** MC-01, MC-03: errores estándar robustos en regresiones transversales y de series.
- **Limitaciones:** Confirmada solo mediante página índice (bibliografía de Wikipedia «Heteroskedasticity-consistent standard errors»); pendiente de lectura de la fuente primaria.

#### DOC-MOT-0234 · Q 94 (A) — Econometric Computing with HC and HAC Covariance Matrix Estimators

- **Autores:** Achim Zeileis
- **Año:** 2004
- **Publicación o institución:** Journal of Statistical Software, 11(10), 1-17
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-04 Econometría y causalidad (principal) · secundarias: TM-01, TM-14
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** DOI: 10.18637/jss.v011.i10 · Verificada en páginas índice: https://en.wikipedia.org/wiki/Newey%E2%80%93West_estimator · https://rdrr.io/pkg/sandwich/man/NeweyWest.html
- **Acceso y licencia:** Acceso abierto (JSS)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Newey–West estimator wikipedia heteroskedasticity and autocorrelation consistent Andrews 1991 bandwidth»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Newey%E2%80%93West_estimator)
- **Contenido:** Marco computacional modular para estimadores HC y HAC (núcleos, anchos, preblanqueo) implementado en el paquete R sandwich.
- **Uso en el Motor:** MC-01, MC-03: implementación y verificación de errores robustos.
- **Limitaciones:** Confirmada solo mediante página índice (bibliografía de Wikipedia «Newey–West estimator» y ayuda de sandwich); pendiente de lectura de la fuente primaria.

#### DOC-MOT-0239 · Q 94 (A) — Bounds Testing Approaches to the Analysis of Level Relationships

- **Autores:** M. Hashem Pesaran; Yongcheol Shin; Richard J. Smith
- **Año:** 2001
- **Publicación o institución:** Journal of Applied Econometrics, 16(3), 289-326
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-04 Econometría y causalidad (principal) · secundarias: TM-02
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1002/jae.616 · Verificada en páginas índice: https://en.wikipedia.org/wiki/Cointegration · https://en.wikipedia.org/wiki/Structural_break
- **Acceso y licencia:** Revista Wiley por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Cointegration wikipedia Engle-Granger Johansen test Phillips-Ouliaris references»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Cointegration)
- **Contenido:** Contraste de cotas ARDL para relaciones de nivel válido con regresores I(0), I(1) o mezcla, con valores críticos inferior y superior.
- **Uso en el Motor:** MC-03: relación de largo plazo sin precontraste de orden de integración.
- **Limitaciones:** Confirmada solo mediante página índice (bibliografía de Wikipedia «Cointegration» y «Structural break»); pendiente de lectura de la fuente primaria.

#### DOC-MOT-0238 · Q 94 (A) — Asymptotic Properties of Residual Based Tests for Cointegration

- **Autores:** Peter C. B. Phillips; Sam Ouliaris
- **Año:** 1990
- **Publicación o institución:** Econometrica, 58(1), 165-193
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-04 Econometría y causalidad (principal) · secundarias: TM-02
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.2307/2938339 · Verificada en página índice: https://en.wikipedia.org/wiki/Cointegration
- **Acceso y licencia:** Revista por suscripción (JSTOR 2938339)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Cointegration wikipedia Engle-Granger Johansen test Phillips-Ouliaris references»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Cointegration)
- **Contenido:** Distribuciones asintóticas y valores críticos de contrastes de cointegración basados en residuos (ADF y Phillips sobre residuos, Pu y Pz).
- **Uso en el Motor:** MC-03: contraste de cointegración residual (pares de activos).
- **Limitaciones:** Confirmada solo mediante página índice (bibliografía de Wikipedia «Cointegration»); pendiente de lectura de la fuente primaria.

#### DOC-MOT-0041 · Q 94 (A) — A Simple, Positive Semi-Definite, Heteroskedasticity and Autocorrelation Consistent Covariance Matrix

- **Autores:** Whitney K. Newey; Kenneth D. West
- **Año:** 1987
- **Publicación o institución:** Econometrica, 55(3), 703-708
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-04 Econometría y causalidad (principal) · secundarias: TM-01
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.2307/1913610 · Verificada en páginas índice: https://en.wikipedia.org/wiki/Newey%E2%80%93West_estimator · https://rdrr.io/pkg/sandwich/man/NeweyWest.html
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Newey–West estimator wikipedia heteroskedasticity and autocorrelation consistent Andrews 1991 bandwidth»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Newey%E2%80%93West_estimator)
- **Contenido:** Estimador de la matriz de covarianzas robusto a heterocedasticidad y autocorrelación con ponderaciones de Bartlett, que garantiza semidefinición positiva.
- **Uso en el Motor:** MC-01, MC-03: errores estándar HAC en regresiones con datos solapados o autocorrelados.
- **Limitaciones:** Elección del retardo (véanse DOC-MOT-0232 y 0233); mal comportamiento en muestras pequeñas. Confirmada solo mediante página índice (bibliografía de Wikipedia «Newey–West estimator» y ayuda de sandwich); pendiente de lectura de la fuente primaria.
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02 (DOI confirmado en índice).

#### DOC-MOT-0237 · Q 94 (A) — Some Heteroskedasticity-Consistent Covariance Matrix Estimators with Improved Finite Sample Properties

- **Autores:** James G. MacKinnon; Halbert White
- **Año:** 1985
- **Publicación o institución:** Journal of Econometrics, 29(3), 305-325
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-04 Econometría y causalidad (principal) · secundarias: TM-01
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1016/0304-4076(85)90158-7 · Verificada en página índice: https://en.wikipedia.org/wiki/Heteroskedasticity-consistent_standard_errors (hdl:10419/189084, EconStor)
- **Acceso y licencia:** Copia en EconStor según el índice
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Heteroskedasticity-consistent standard errors wikipedia White 1980 MacKinnon White 1985»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Heteroskedasticity-consistent_standard_errors)
- **Contenido:** Propone las variantes HC1-HC3 del estimador de White con mejores propiedades en muestras pequeñas (HC3 tipo jackknife).
- **Uso en el Motor:** MC-01, MC-03: elección HC3 en muestras cortas.
- **Limitaciones:** Confirmada solo mediante página índice (bibliografía de Wikipedia «Heteroskedasticity-consistent standard errors»); pendiente de lectura de la fuente primaria.

#### DOC-MOT-0043 · Q 94 (A) — Macroeconomics and Reality

- **Autores:** Christopher A. Sims
- **Año:** 1980
- **Publicación o institución:** Econometrica, 48(1), 1-48
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-04 Econometría y causalidad (principal) · secundarias: —
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** Verificada en página índice: https://encyclopediaofmath.org/wiki/Vector_autoregressive_models
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Vector autoregression wikipedia Sims 1980 Lütkepohl structural VAR impulse response references»; WebFetch: sí, sobre la página índice https://encyclopediaofmath.org/wiki/Vector_autoregressive_models)
- **Contenido:** Critica las restricciones de identificación «increíbles» de los modelos macro estructurales y propone los VAR no restringidos con funciones impulso-respuesta y descomposición de varianza.
- **Uso en el Motor:** MC-03: VAR y funciones impulso-respuesta.
- **Limitaciones:** Identificación recursiva discutible. Confirmada solo mediante página índice (bibliografía de H. Lütkepohl, «Vector autoregressive models», Encyclopedia of Mathematics); pendiente de lectura de la fuente primaria. DOI de la semilla no visto; se retira.
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02.

#### DOC-MOT-0042 · Q 94 (A) — Investigating Causal Relations by Econometric Models and Cross-spectral Methods

- **Autores:** Clive W. J. Granger
- **Año:** 1969
- **Publicación o institución:** Econometrica, 37(3), 424-438
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-04 Econometría y causalidad (principal) · secundarias: —
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** Verificada en página índice: https://encyclopediaofmath.org/wiki/Vector_autoregressive_models
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Vector autoregression wikipedia Sims 1980 Lütkepohl structural VAR impulse response references»; WebFetch: sí, sobre la página índice https://encyclopediaofmath.org/wiki/Vector_autoregressive_models)
- **Contenido:** Define la causalidad en el sentido de Granger (precedencia predictiva) y su contraste en modelos dinámicos y en el dominio de la frecuencia.
- **Uso en el Motor:** MC-03: causalidad de Granger (precedencia predictiva, no causalidad estructural).
- **Limitaciones:** No identifica causalidad estructural. Confirmada solo mediante página índice (bibliografía de Encyclopedia of Mathematics); pendiente de lectura de la fuente primaria. DOI de la semilla no visto; se retira.
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02.

#### DOC-MOT-0248 · Q 93 (A) — What Are the Effects of Monetary Policy on Output? Results from an Agnostic Identification Procedure

- **Autores:** Harald Uhlig
- **Año:** 2005
- **Publicación o institución:** Journal of Monetary Economics, 52, 381-419
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-04 Econometría y causalidad (principal) · secundarias: —
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** Verificada en página índice: https://www.wiwiss.fu-berlin.de/fachbereich/vwl/luetkepohl/Lehrveranstaltungen/MTSA_SS2016.pdf
- **Acceso y licencia:** Revista Elsevier por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Vector autoregression wikipedia Sims 1980 Lütkepohl structural VAR impulse response references»; WebFetch: sí, sobre la página índice https://www.wiwiss.fu-berlin.de/fachbereich/vwl/luetkepohl/Lehrveranstaltungen/MTSA_SS2016.pdf)
- **Contenido:** Identificación de SVAR por restricciones de signo sobre las respuestas al impulso, sin restricciones de exclusión.
- **Uso en el Motor:** MC-03: identificación por signos.
- **Limitaciones:** Identificación de conjunto (no puntual). Confirmada solo mediante página índice (bibliografía de programa docente FU Berlin); pendiente de lectura de la fuente primaria.

#### DOC-MOT-0233 · Q 93 (A) — Automatic Lag Selection in Covariance Matrix Estimation

- **Autores:** Whitney K. Newey; Kenneth D. West
- **Año:** 1994
- **Publicación o institución:** The Review of Economic Studies, 61(4), 631-654
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-04 Econometría y causalidad (principal) · secundarias: TM-01
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.2307/2297912 · Verificada en páginas índice: https://en.wikipedia.org/wiki/Newey%E2%80%93West_estimator · https://rdrr.io/pkg/sandwich/man/NeweyWest.html
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Newey–West estimator wikipedia heteroskedasticity and autocorrelation consistent Andrews 1991 bandwidth»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Newey%E2%80%93West_estimator)
- **Contenido:** Procedimiento no paramétrico de selección automática del retardo para estimadores HAC (Bartlett, Parzen), por defecto en paquetes como sandwich.
- **Uso en el Motor:** MC-01, MC-03: regla documentada de retardo HAC.
- **Limitaciones:** Confirmada solo mediante página índice (bibliografía de Wikipedia «Newey–West estimator»); pendiente de lectura de la fuente primaria.

#### DOC-MOT-0240 · Q 93 (A) — Spurious Regressions in Econometrics

- **Autores:** Clive W. J. Granger; Paul Newbold
- **Año:** 1974
- **Publicación o institución:** Journal of Econometrics, 2(2), 111-120
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-04 Econometría y causalidad (principal) · secundarias: TM-02
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1016/0304-4076(74)90034-7 · Verificada en página índice: https://en.wikipedia.org/wiki/Cointegration
- **Acceso y licencia:** Revista Elsevier por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Cointegration wikipedia Engle-Granger Johansen test Phillips-Ouliaris references»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Cointegration)
- **Contenido:** Simulaciones que muestran R² y t elevados en regresiones entre paseos aleatorios independientes: la regresión espuria.
- **Uso en el Motor:** MC-03: salvaguarda contra regresar niveles no estacionarios sin cointegración.
- **Limitaciones:** Confirmada solo mediante página índice (bibliografía de Wikipedia «Cointegration»); pendiente de lectura de la fuente primaria.

#### DOC-MOT-0247 · Q 92 (A) — The Dynamic Effects of Aggregate Demand and Supply Disturbances

- **Autores:** Olivier J. Blanchard; Danny Quah
- **Año:** 1989
- **Publicación o institución:** American Economic Review, 79, 655-673
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-04 Econometría y causalidad (principal) · secundarias: —
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** Verificada en página índice: https://www.wiwiss.fu-berlin.de/fachbereich/vwl/luetkepohl/Lehrveranstaltungen/MTSA_SS2016.pdf
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Vector autoregression wikipedia Sims 1980 Lütkepohl structural VAR impulse response references»; WebFetch: sí, sobre la página índice https://www.wiwiss.fu-berlin.de/fachbereich/vwl/luetkepohl/Lehrveranstaltungen/MTSA_SS2016.pdf)
- **Contenido:** Identificación de SVAR mediante restricciones de largo plazo (shocks sin efecto permanente sobre el nivel de una variable).
- **Uso en el Motor:** MC-03: identificación de largo plazo en SVAR.
- **Limitaciones:** Confirmada solo mediante página índice (bibliografía de programa docente de H. Lütkepohl, FU Berlin); pendiente de lectura de la fuente primaria.

#### DOC-MOT-0241 · Q 90 (A) — Critical Values for Cointegration Tests

- **Autores:** James G. MacKinnon
- **Año:** 2010
- **Publicación o institución:** Queen's Economics Department Working Paper n.º 1227 (EconStor hdl:10419/67744)
- **Tipo de documento:** Documento de trabajo de institución académica
- **Temática:** TM-04 Econometría y causalidad (principal) · secundarias: TM-02
- **Calidad Q:** 90 (A) — Tipo 20/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** Verificada en página índice: https://en.wikipedia.org/wiki/Cointegration
- **Acceso y licencia:** Acceso abierto (EconStor)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Cointegration wikipedia Engle-Granger Johansen test Phillips-Ouliaris references»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Cointegration)
- **Contenido:** Superficies de respuesta para valores críticos de contrastes de raíz unitaria y de cointegración de Engle-Granger con cualquier tamaño muestral y número de variables.
- **Uso en el Motor:** MC-02, MC-03: valores críticos y p-valores en ADF y Engle-Granger.
- **Limitaciones:** Confirmada solo mediante página índice (bibliografía de Wikipedia «Cointegration»); pendiente de lectura de la fuente primaria.

#### DOC-MOT-0242 · Q 90 (A) — Tests for Cointegration in Models with Regime and Trend Shifts

- **Autores:** Allan W. Gregory; Bruce E. Hansen
- **Año:** 1996
- **Publicación o institución:** Oxford Bulletin of Economics and Statistics, 58(3), 555-560
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-04 Econometría y causalidad (principal) · secundarias: TM-02
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1111/j.1468-0084.1996.mp58003008.x · Verificada en página índice: https://en.wikipedia.org/wiki/Structural_break
- **Acceso y licencia:** Revista Wiley por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Structural break wikipedia Chow test Andrews 1993 Zivot Andrews Bai Perron references»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Structural_break)
- **Contenido:** Extiende los contrastes residuales de cointegración a una ruptura de fecha desconocida en constante, tendencia o pendiente de la relación.
- **Uso en el Motor:** MC-03: cointegración con ruptura estructural.
- **Limitaciones:** Una sola ruptura. Confirmada solo mediante página índice (bibliografía de Wikipedia «Structural break»); pendiente de lectura de la fuente primaria.

#### DOC-MOT-0249 · Q 89 (A) — Sign Restrictions in Structural Vector Autoregressions: A Critical Review

- **Autores:** Renée Fry; Adrian Pagan
- **Año:** 2011
- **Publicación o institución:** Journal of Economic Literature, 49, 938-960
- **Tipo de documento:** Artículo de revisión revisado por pares
- **Temática:** TM-04 Econometría y causalidad (principal) · secundarias: —
- **Calidad Q:** 89 (A) — Tipo 23/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** Verificada en página índice: https://www.wiwiss.fu-berlin.de/fachbereich/vwl/luetkepohl/Lehrveranstaltungen/MTSA_SS2016.pdf
- **Acceso y licencia:** Revista AEA por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Vector autoregression wikipedia Sims 1980 Lütkepohl structural VAR impulse response references»; WebFetch: sí, sobre la página índice https://www.wiwiss.fu-berlin.de/fachbereich/vwl/luetkepohl/Lehrveranstaltungen/MTSA_SS2016.pdf)
- **Contenido:** Revisión crítica de la identificación por signos: problema de modelos múltiples, uso de la mediana y alternativas.
- **Uso en el Motor:** MC-03: cautelas al informar impulso-respuestas por signos.
- **Limitaciones:** Confirmada solo mediante página índice (bibliografía de programa docente FU Berlin); pendiente de lectura de la fuente primaria.

#### DOC-MOT-0244 · Q 89 (A) — New Introduction to Multiple Time Series Analysis

- **Autores:** Helmut Lütkepohl
- **Año:** 2005
- **Publicación o institución:** Springer-Verlag, Berlín
- **Tipo de documento:** Manual de referencia
- **Temática:** TM-04 Econometría y causalidad (principal) · secundarias: TM-02
- **Calidad Q:** 89 (A) — Tipo 20/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** Verificada en páginas índice: https://encyclopediaofmath.org/wiki/Vector_autoregressive_models · https://www.wiwiss.fu-berlin.de/fachbereich/vwl/luetkepohl/Lehrveranstaltungen/MTSA_SS2016.pdf
- **Acceso y licencia:** Libro de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Vector autoregression wikipedia Sims 1980 Lütkepohl structural VAR impulse response references»; WebFetch: sí, sobre la página índice https://encyclopediaofmath.org/wiki/Vector_autoregressive_models)
- **Contenido:** Manual de series multivariantes: VAR estables, selección de orden, causalidad de Granger, impulso-respuesta, VECM y cointegración, VAR estructurales y modelos de espacio de estados.
- **Uso en el Motor:** MC-03: referencia de implementación de VAR/VECM/SVAR.
- **Limitaciones:** Confirmada solo mediante página índice (bibliografía de Encyclopedia of Mathematics y programa docente FU Berlin); pendiente de lectura de la fuente primaria.

#### DOC-MOT-0243 · Q 88 (A) — Likelihood-Based Inference in Cointegrated Vector Autoregressive Models

- **Autores:** Søren Johansen
- **Año:** 1995
- **Publicación o institución:** Oxford University Press
- **Tipo de documento:** Manual de referencia
- **Temática:** TM-04 Econometría y causalidad (principal) · secundarias: TM-02
- **Calidad Q:** 88 (A) — Tipo 20/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** Verificada en página índice: https://encyclopediaofmath.org/wiki/Vector_autoregressive_models
- **Acceso y licencia:** Libro de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Vector autoregression wikipedia Sims 1980 Lütkepohl structural VAR impulse response references»; WebFetch: sí, sobre la página índice https://encyclopediaofmath.org/wiki/Vector_autoregressive_models)
- **Contenido:** Tratado del enfoque de Johansen: representación, estimación de rango reducido, contrastes de rango e hipótesis sobre vectores de cointegración y ajuste.
- **Uso en el Motor:** MC-03: base teórica de VECM.
- **Limitaciones:** Confirmada solo mediante página índice (bibliografía de Encyclopedia of Mathematics); pendiente de lectura de la fuente primaria.

#### DOC-MOT-0046 · Q 87 (A) — Mostly Harmless Econometrics: An Empiricist's Companion

- **Autores:** Joshua D. Angrist; Jörn-Steffen Pischke
- **Año:** 2009
- **Publicación o institución:** Princeton University Press (edición electrónica en De Gruyter Brill)
- **Tipo de documento:** Manual de referencia
- **Temática:** TM-04 Econometría y causalidad (principal) · secundarias: TM-01
- **Calidad Q:** 87 (A) — Tipo 20/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.1515/9781400829828 · https://www.degruyterbrill.com/document/doi/10.1515/9781400829828/html?lang=en
- **Acceso y licencia:** Libro de pago; preliminares abiertos
- **Estado:** Aprobada
- **Estado del enlace:** MURO_PAGO
- **Última verificación:** 2026-11-02 (búsqueda web: «Angrist Pischke "Mostly Harmless Econometrics: An Empiricist's Companion" Princeton University Press 2009»; WebFetch: sí)
- **Contenido:** Guía de identificación causal: regresión como aproximación a la esperanza condicional, variables instrumentales, diferencias en diferencias, regresión discontinua, datos de panel y errores estándar.
- **Uso en el Motor:** MC-03: identificación causal (IV, DiD, RD).
- **Limitaciones:** Orientado a microeconometría; anterior a la nueva literatura de DiD escalonado.
- **Origen:** Semilla V3.0 confirmada en verificación de alta 2026-11-02 (DOI confirmado).

#### DOC-MOT-0251 · Q 85 (A) — Tests for Causality between Integrated Variables Using Asymptotic and Bootstrap Distributions: Theory and Application

- **Autores:** R. Scott Hacker; Abdulnasser Hatemi-J
- **Año:** 2006
- **Publicación o institución:** Applied Economics, 38(15), 1489-1500
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-04 Econometría y causalidad (principal) · secundarias: TM-02
- **Calidad Q:** 85 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 12/15 · Vigencia 10/10 · Impacto 7/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1080/00036840500405763 · Verificada en página índice: https://en.wikipedia.org/wiki/Structural_break
- **Acceso y licencia:** Revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Structural break wikipedia Chow test Andrews 1993 Zivot Andrews Bai Perron references»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Structural_break)
- **Contenido:** Contraste de causalidad de Granger tipo Toda-Yamamoto (VAR aumentado) con valores críticos por bootstrap para corregir distorsiones de tamaño con variables integradas.
- **Uso en el Motor:** MC-03: causalidad de Granger con series I(1).
- **Limitaciones:** El enfoque Toda-Yamamoto tiene baja potencia si la causalidad actúa vía la relación de cointegración (advertencia documentada por Estima). Confirmada solo mediante página índice (bibliografía de Wikipedia «Structural break»); pendiente de lectura de la fuente primaria.

#### DOC-MOT-0245 · Q 81 (A) — Vector Autoregressive Models

- **Autores:** Helmut Lütkepohl
- **Año:** s. f. (entrada adaptada de StatProb)
- **Publicación o institución:** Encyclopedia of Mathematics (Springer / EMS)
- **Tipo de documento:** Artículo de referencia (enciclopedia académica)
- **Temática:** TM-04 Econometría y causalidad (principal) · secundarias: TM-02
- **Calidad Q:** 81 (A) — Tipo 15/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 6/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://encyclopediaofmath.org/wiki/Vector_autoregressive_models
- **Acceso y licencia:** Acceso abierto
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Vector autoregression wikipedia Sims 1980 Lütkepohl structural VAR impulse response references»; WebFetch: sí)
- **Contenido:** Síntesis de VAR: forma reducida y estructural, estimación, selección de orden (AIC), causalidad de Granger, impulso-respuesta y cointegración, con bibliografía esencial.
- **Uso en el Motor:** MC-03: glosario breve de VAR para documentar cálculos.
- **Limitaciones:** Texto breve sin fecha explícita.

#### DOC-MOT-0235 · Q 80 (A) — sandwich: NeweyWest — Newey-West HAC Covariance Matrix Estimation (documentación de función R)

- **Autores:** Autores del paquete sandwich (CRAN); función basada en Zeileis (2004)
- **Año:** Documentación vigente consultada en 2026
- **Publicación o institución:** Paquete R «sandwich» (CRAN), ayuda en rdrr.io
- **Tipo de documento:** Documentación técnica de software
- **Temática:** TM-04 Econometría y causalidad (principal) · secundarias: TM-01, TM-14
- **Calidad Q:** 80 (A) — Tipo 15/25 · Rigor 15/20 · Autoridad 12/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** https://rdrr.io/pkg/sandwich/man/NeweyWest.html
- **Acceso y licencia:** Abierto; software libre (CRAN)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Newey–West estimator wikipedia heteroskedasticity and autocorrelation consistent Andrews 1991 bandwidth»; WebFetch: sí)
- **Contenido:** Estimador Newey-West con pesos de Bartlett, retardo automático (Newey-West 1994), preblanqueo VAR(1) por defecto y corrección n/(n−k) opcional.
- **Uso en el Motor:** MC-01, MC-03: implementación de referencia; advierte que el valor por defecto no es el estimador de 1987.
- **Limitaciones:** Los valores por defecto (preblanqueo) difieren de otras bibliotecas; documentarlos al comparar resultados.

#### DOC-MOT-0252 · Q 80 (A) — statsmodels: Time Series Analysis (tsa) — índice de la API

- **Autores:** Equipo de desarrollo de statsmodels
- **Año:** Rama de desarrollo consultada en 2026
- **Publicación o institución:** statsmodels.org
- **Tipo de documento:** Documentación técnica de software
- **Temática:** TM-04 Econometría y causalidad (principal) · secundarias: TM-02, TM-14
- **Calidad Q:** 80 (A) — Tipo 15/25 · Rigor 14/20 · Autoridad 12/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** https://www.statsmodels.org/devel/_sources/tsa.rst.txt
- **Acceso y licencia:** Abierto; software libre (BSD)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «statsmodels time series analysis tsa documentation references Markov switching regression»; WebFetch: sí)
- **Contenido:** Índice del módulo tsa: ARIMA, ETS, STL/MSTL, filtros HP/BK/CF, VAR/VECM, MarkovRegression y contrastes adfuller, kpss, zivot_andrews, grangercausalitytests y coint.
- **Uso en el Motor:** MC-02, MC-03: mapa de funciones Python equivalentes a los métodos de este archivo.
- **Limitaciones:** Página de índice sin referencias bibliográficas; rama de desarrollo cambiante.

#### DOC-MOT-0250 · Q 77 (B) — lpirfs: Local Projections Impulse Response Functions (manual del paquete R, v0.2.5)

- **Autores:** Philipp Adämmer (autor y mantenedor); contribuciones de J. P. LeSage, M. Balcilar y J. Danielsson
- **Año:** Versión 0.2.5 (manual compilado en 2026)
- **Publicación o institución:** CRAN / R-universe
- **Tipo de documento:** Documentación técnica de software
- **Temática:** TM-04 Econometría y causalidad (principal) · secundarias: TM-14
- **Calidad Q:** 77 (B) — Tipo 15/25 · Rigor 15/20 · Autoridad 11/15 · Vigencia 10/10 · Impacto 7/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** https://cran.r-universe.dev/lpirfs/doc/manual.html
- **Acceso y licencia:** Abierto; software GPL (≥ 2)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Jordà 2005 "Estimation and Inference of Impulse Responses by Local Projections" American Economic Review 95»; WebFetch: sí (lectura parcial: primeros 100 000 caracteres))
- **Contenido:** Proyecciones locales lineales, con shocks identificados, 2SLS, panel (efectos fijos, GMM, errores robustos) y no lineales por estados (transición suave o variable ficticia); remite a Adämmer (2019, R Journal, DOI 10.32614/RJ-2019-052).
- **Uso en el Motor:** MC-03: implementación de referencia de proyecciones locales.
- **Limitaciones:** Paquete de un autor principal; solo R.

## TM-05 Valoración de activos y estructura temporal

#### DOC-MOT-0052 · Q 95 (A) — The Dividend-Price Ratio and Expectations of Future Dividends and Discount Factors

- **Autores:** John Y. Campbell; Robert J. Shiller
- **Año:** 1988
- **Publicación o institución:** The Review of Financial Studies, vol. 1, n.º 3, págs. 195-228 (circuló antes como NBER Working Paper 2100, diciembre de 1986)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-05 Valoración de activos y estructura temporal (principal) · secundarias: TM-02
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI del documento de trabajo: 10.3386/w2100 (el DOI de la versión de revista no se ha visto; se retira el «10.1093/rfs/1.3.195 a verificar») · https://www.nber.org/papers/w2100
- **Acceso y licencia:** Documento de trabajo NBER con PDF de libre descarga; versión de revista por suscripción (Oxford University Press)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Campbell Shiller 1988 "The Dividend-Price Ratio and Expectations of Future Dividends and Discount Factors" Review of Financial Studies»; WebFetch: sí)
- **Contenido:** Introduce la aproximación log-lineal del ratio dividendo-precio («identidad de Campbell-Shiller») que lo descompone en expectativas de crecimiento de dividendos y de tasas de descuento futuras, y la contrasta con un VAR.
- **Uso en el Motor:** MC-09: descomposición log-lineal del ratio dividendo-precio; base de la predicción de rentabilidades a H4.
- **Limitaciones:** Predictibilidad débil fuera de muestra (véase Goyal y Welch); el NBER WP es una versión previa que puede diferir del texto publicado.
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (metadatos de la versión publicada tomados de la página NBER).

#### DOC-MOT-0051 · Q 94 (A) — Pricing the Term Structure with Linear Regressions

- **Autores:** Tobias Adrian; Richard K. Crump; Emanuel Moench
- **Año:** 2013
- **Publicación o institución:** Journal of Financial Economics, vol. 110, n.º 1, págs. 110-138 (versión previa: Federal Reserve Bank of New York Staff Report 340, 2008, rev. abril de 2013)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-05 Valoración de activos y estructura temporal (principal)
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 9/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI: 10.1016/j.jfineco.2013.04.009 (visto en IDEAS/RePEc) · https://ideas.repec.org/a/eee/jfinec/v110y2013i1p110-138.html · Versión de acceso gratuito: https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr340.html
- **Acceso y licencia:** Staff Report del NY Fed de libre acceso; versión de revista por suscripción (Elsevier)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Adrian Crump Moench "Pricing the Term Structure with Linear Regressions" Journal of Financial Economics 2013» y «"Pricing the term structure with linear regressions" Journal of Financial Economics 110 doi …»; WebFetch: sí, IDEAS y NY Fed)
- **Contenido:** Estima modelos afines de la estructura temporal sin arbitraje mediante tres pasos de regresiones lineales (modelo ACM), lo que permite obtener primas por plazo de forma rápida y estable; el NY Fed publica las series resultantes.
- **Uso en el Motor:** MC-09: estimación de la prima por plazo (modelo ACM).
- **Limitaciones:** Dependiente de la especificación de factores (componentes principales de rendimientos).
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02.

#### DOC-MOT-0049 · Q 94 (A) — Forecasting the Term Structure of Government Bond Yields

- **Autores:** Francis X. Diebold; Canlin Li
- **Año:** 2006
- **Publicación o institución:** Journal of Econometrics, vol. 130, n.º 2, págs. 337-364 (versión previa: NBER Working Paper 10048, octubre de 2003)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-05 Valoración de activos y estructura temporal (principal) · secundarias: TM-02
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI del documento de trabajo: 10.3386/w10048 (el DOI de la revista no se ha visto; se retira «10.1016/j.jeconom.2005.03.005 a verificar») · https://www.nber.org/papers/w10048
- **Acceso y licencia:** NBER WP de libre descarga (también copia en economics.sas.upenn.edu); versión de revista por suscripción (Elsevier)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Diebold Li "Forecasting the term structure of government bond yields" Journal of Econometrics 2006»; WebFetch: sí)
- **Contenido:** Reinterpreta Nelson-Siegel como modelo dinámico de tres factores latentes (nivel, pendiente, curvatura) con dinámica autorregresiva y muestra su capacidad de previsión de la curva a horizontes de 6-12 meses.
- **Uso en el Motor:** MC-09, MC-02: Nelson-Siegel dinámico para prever la curva.
- **Limitaciones:** Sin restricción de no arbitraje; λ fijo.
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02.

#### DOC-MOT-0313 · Q 94 (A) — Predicting U.S. Recessions: Financial Variables as Leading Indicators

- **Autores:** Arturo Estrella; Frederic S. Mishkin
- **Año:** 1998
- **Publicación o institución:** Review of Economics and Statistics, vol. 80, págs. 45-61 (versión previa: NBER WP 5379)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-05 Valoración de activos y estructura temporal (principal) · secundarias: TM-02
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI: 10.1162/003465398557320 · NBER: http://www.nber.org/papers/w5379.pdf
- **Acceso y licencia:** NBER WP gratuito; revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Vasicek model Cox–Ingersoll–Ross model Heath–Jarrow–Morton framework affine term structure model yield curve (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Yield curve»)
- **Contenido:** Probit de recesiones: la pendiente de la curva es el mejor predictor financiero a 2-6 trimestres.
- **Uso en el Motor:** MC-09, MC-02: probabilidad de recesión a partir de la pendiente.
- **Limitaciones:** Relación inestable tras 2008 y con QE.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0047 · Q 94 (A) — Parsimonious Modeling of Yield Curves

- **Autores:** Charles R. Nelson; Andrew F. Siegel
- **Año:** 1987
- **Publicación o institución:** The Journal of Business, vol. 60, págs. 473-489 (octubre de 1987); versión previa: NBER Working Paper 1594 (1985), «Parsimoneous Modeling of Yield Curves for U.S. Treasury Bills»
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-05 Valoración de activos y estructura temporal (principal)
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI del documento de trabajo: 10.3386/w1594 (el DOI de la revista no se ha visto; se retira «10.1086/296409 a verificar») · https://www.nber.org/papers/w1594
- **Acceso y licencia:** NBER WP de libre descarga; versión de revista por suscripción (University of Chicago Press/JSTOR)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Nelson Siegel 1987 "Parsimonious Modeling of Yield Curves" Journal of Business»; WebFetch: sí)
- **Contenido:** Propone la forma funcional de tres componentes (nivel, pendiente, curvatura con decaimiento exponencial) para ajustar la curva de tipos con pocos parámetros.
- **Uso en el Motor:** MC-09: ajuste paramétrico de la curva de tipos (nivel, pendiente, curvatura).
- **Limitaciones:** Curvatura única; puede no ajustar tramos largos. Discrepancia de metadatos: la página NBER indica n.º 3 y la semilla n.º 4; se omite el número hasta comprobarlo en la editorial.
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02.

#### DOC-MOT-0303 · Q 93 (A) — The Affine Arbitrage-Free Class of Nelson–Siegel Term Structure Models

- **Autores:** Jens H. E. Christensen; Francis X. Diebold; Glenn D. Rudebusch
- **Año:** 2011
- **Publicación o institución:** Journal of Econometrics, vol. 164, n.º 1, págs. 4-20
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-05 Valoración de activos y estructura temporal (principal) · secundarias: TM-02
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1016/j.jeconom.2011.02.011 · http://www.sciencedirect.com/science/article/pii/S0304407611000388
- **Acceso y licencia:** Texto completo por suscripción en la editorial (Elsevier)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Vasicek model Cox–Ingersoll–Ross model Heath–Jarrow–Morton framework affine term structure model yield curve (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Affine term structure model», que reproduce la cita completa)
- **Contenido:** Modelo AFNS: impone no arbitraje a Nelson-Siegel dinámico manteniendo su parsimonia, con mejora de previsiones.
- **Uso en el Motor:** MC-09, MC-02: curva dinámica sin arbitraje.
- **Limitaciones:** Supuestos gaussianos.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0302 · Q 93 (A) — A Yield-Factor Model of Interest Rates

- **Autores:** Darrell Duffie; Rui Kan
- **Año:** 1996
- **Publicación o institución:** Mathematical Finance, vol. 6, n.º 4, págs. 379-406
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-05 Valoración de activos y estructura temporal (principal) · secundarias: —
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1111/j.1467-9965.1996.tb00123.x · https://doi.org/10.1111%2Fj.1467-9965.1996.tb00123.x
- **Acceso y licencia:** Texto completo por suscripción en la editorial (Wiley)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Vasicek model Cox–Ingersoll–Ross model Heath–Jarrow–Morton framework affine term structure model yield curve (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Affine term structure model», que reproduce la cita completa)
- **Contenido:** Caracteriza la clase de modelos afines de estructura temporal: rendimientos lineales en factores de estado con ecuaciones de Riccati.
- **Uso en el Motor:** MC-09: marco afín para modelos de curva sin arbitraje.
- **Limitaciones:** Técnico; identificación de factores compleja.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0301 · Q 93 (A) — A Theory of the Term Structure of Interest Rates

- **Autores:** John C. Cox; Jonathan E. Ingersoll; Stephen A. Ross
- **Año:** 1985
- **Publicación o institución:** Econometrica, vol. 53, n.º 2, págs. 385-407
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-05 Valoración de activos y estructura temporal (principal) · secundarias: TM-06
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.2307/1911242 · JSTOR: 1911242
- **Acceso y licencia:** Texto completo por suscripción en la editorial (Econometric Society/JSTOR)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Vasicek model Cox–Ingersoll–Ross model Heath–Jarrow–Morton framework affine term structure model yield curve (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Cox–Ingersoll–Ross model», que reproduce la cita completa y «Short-rate model»)
- **Contenido:** Modelo de equilibrio general con difusión de raíz cuadrada para el tipo corto, que garantiza tipos no negativos y precios cerrados de bonos.
- **Uso en el Motor:** MC-09: dinámica de tipos y de intensidades (CIR) en simulación.
- **Limitaciones:** Un factor; ajuste deficiente a curvas complejas.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0309 · Q 92 (A) — Interpolation Methods for Curve Construction

- **Autores:** Patrick S. Hagan; Graeme West
- **Año:** 2006
- **Publicación o institución:** Applied Mathematical Finance, vol. 13, n.º 2, págs. 89-129
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-05 Valoración de activos y estructura temporal (principal) · secundarias: TM-09
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI: 10.1080/13504860500396032 · Copia: http://www.finmod.co.za/Hagan_West_curves_AMF.pdf
- **Acceso y licencia:** Copia gratuita (finmod.co.za); revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Vasicek model Cox–Ingersoll–Ross model Heath–Jarrow–Morton framework affine term structure model yield curve (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Yield curve»)
- **Contenido:** Compara métodos de interpolación para construir curvas (lineal en rendimientos, log-lineal en factores de descuento, splines, monotone convex) y sus propiedades de forwards.
- **Uso en el Motor:** MC-09: construcción de curvas de descuento y forwards.
- **Limitaciones:** Enfocado a curvas de swaps; no aborda multicurva.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0315 · Q 92 (A) — The Equity Premium: A Puzzle

- **Autores:** Rajnish Mehra; Edward C. Prescott
- **Año:** 1985
- **Publicación o institución:** Journal of Monetary Economics, vol. 15, n.º 2, págs. 145-161
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-05 Valoración de activos y estructura temporal (principal) · secundarias: TM-07
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1016/0304-3932(85)90061-3 · PDF: http://minneapolisfed.org/research/sr/sr81.pdf
- **Acceso y licencia:** Versión Fed de Minneapolis gratuita; revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «dividend discount model equity premium puzzle residual income valuation Gordon growth (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Equity premium puzzle»)
- **Contenido:** Muestra que la prima de riesgo histórica de la renta variable es demasiado alta para modelos de consumo con aversión al riesgo razonable.
- **Uso en el Motor:** MC-09: contexto teórico de la prima de riesgo.
- **Limitaciones:** Calibración a EE. UU. 1889-1978.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0300 · Q 92 (A) — An Equilibrium Characterization of the Term Structure

- **Autores:** Oldřich Vašíček
- **Año:** 1977
- **Publicación o institución:** Journal of Financial Economics, vol. 5, n.º 2, págs. 177-188
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-05 Valoración de activos y estructura temporal (principal) · secundarias: TM-06
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1016/0304-405X(77)90016-2 · https://doi.org/10.1016%2F0304-405X%2877%2990016-2 · CiteSeerX: https://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.456.1407
- **Acceso y licencia:** Texto completo por suscripción en la editorial (Elsevier)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Vasicek model Cox–Ingersoll–Ross model Heath–Jarrow–Morton framework affine term structure model yield curve (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Vasicek model», que reproduce la cita completa y «Short-rate model»)
- **Contenido:** Modelo de tipo corto con reversión a la media gaussiana y precios de bonos cerrados; base de los modelos afines.
- **Uso en el Motor:** MC-09: modelo de referencia de tipo corto y escenarios de tipos.
- **Limitaciones:** Admite tipos negativos; un solo factor.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0306 · Q 91 (A) — An Empirical Comparison of Alternative Models of the Short-Term Interest Rate

- **Autores:** K. C. Chan; G. Andrew Karolyi; Francis A. Longstaff; Anthony B. Sanders
- **Año:** 1992
- **Publicación o institución:** The Journal of Finance, vol. 47, n.º 3 (julio de 1992)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-05 Valoración de activos y estructura temporal (principal) · secundarias: TM-02
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** Sin DOI visto · Copia del autor: http://personal.anderson.ucla.edu/francis.longstaff/empiricalcomparison.pdf
- **Acceso y licencia:** Copia gratuita del autor (UCLA); revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Vasicek model Cox–Ingersoll–Ross model Heath–Jarrow–Morton framework affine term structure model yield curve (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Short-rate model», que reproduce la cita completa)
- **Contenido:** Contrasta por GMM una familia anidada de modelos de tipo corto (CKLS) y muestra la importancia de la elasticidad de la volatilidad al nivel.
- **Uso en el Motor:** MC-09: selección y calibración de dinámicas de tipo corto.
- **Limitaciones:** Datos de EE. UU. 1964-1989; un factor.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0304 · Q 91 (A) — Pricing Interest-Rate-Derivative Securities

- **Autores:** John Hull; Alan White
- **Año:** 1990
- **Publicación o institución:** The Review of Financial Studies, vol. 3, n.º 4, págs. 573-592
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-05 Valoración de activos y estructura temporal (principal) · secundarias: TM-06
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.1093/rfs/3.4.573
- **Acceso y licencia:** Texto completo por suscripción en la editorial (OUP)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Vasicek model Cox–Ingersoll–Ross model Heath–Jarrow–Morton framework affine term structure model yield curve (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Short-rate model», que reproduce la cita completa)
- **Contenido:** Extiende Vasicek y CIR con parámetros dependientes del tiempo para ajustar exactamente la curva inicial (modelo Hull-White).
- **Uso en el Motor:** MC-09: valoración de derivados de tipos calibrada a la curva.
- **Limitaciones:** Un factor; tipos negativos en la versión gaussiana.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0312 · Q 90 (A) — Euro Area Yield Curves (estadísticas y notas técnicas del BCE)

- **Autores:** Banco Central Europeo
- **Año:** Publicación continua (consulta 2026)
- **Publicación o institución:** European Central Bank, Statistical Data Warehouse/portal estadístico
- **Tipo de documento:** Fuente oficial de datos con metodología
- **Temática:** TM-05 Valoración de activos y estructura temporal (principal) · secundarias: TM-14
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 13/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 9/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://www.ecb.europa.eu/stats/financial_markets_and_interest_rates/euro_area_yield_curves/html/index.en.html
- **Acceso y licencia:** Acceso gratuito oficial
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Vasicek model Cox–Ingersoll–Ross model Heath–Jarrow–Morton framework affine term structure model yield curve (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Yield curve» (enlace al portal del BCE))
- **Contenido:** Portal oficial del BCE con las curvas de rendimientos de la zona del euro y su documentación metodológica; fuente primaria europea para la curva de referencia.
- **Uso en el Motor:** MC-09: curva de referencia euro para contrastar las estimaciones propias.
- **Limitaciones:** Página de portal (no documento fijo); comprobar en el barrido la nota técnica vigente y el método de estimación declarado.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0310 · Q 90 (A) — The Term Structure of Interest Rates

- **Autores:** Robert A. Jarrow
- **Año:** 2009
- **Publicación o institución:** Annual Review of Financial Economics, vol. 1, n.º 1, págs. 69-96
- **Tipo de documento:** Artículo de revisión revisado por pares
- **Temática:** TM-05 Valoración de activos y estructura temporal (principal) · secundarias: TM-06
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1146/annurev.financial.050808.114513 · http://econpapers.repec.org/article/anrrefeco/v_3a1_3ay_3a2009_3ap_3a69-96.htm
- **Acceso y licencia:** Texto completo por suscripción en la editorial (Annual Reviews)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Vasicek model Cox–Ingersoll–Ross model Heath–Jarrow–Morton framework affine term structure model yield curve (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Short-rate model», que reproduce la cita completa)
- **Contenido:** Panorámica de la modelización de la estructura temporal: tipo corto, HJM, modelos de mercado y contraste empírico.
- **Uso en el Motor:** MC-09: mapa de modelos de curva para elegir especificación.
- **Limitaciones:** Revisión conceptual sin implementación.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0316 · Q 90 (A) — The Worldwide Equity Premium: A Smaller Puzzle

- **Autores:** Elroy Dimson; Paul Marsh; Mike Staunton
- **Año:** 2008
- **Publicación o institución:** En R. Mehra (ed.), Handbook of the Equity Risk Premium, Elsevier (versión SSRN 891620)
- **Tipo de documento:** Capítulo de manual académico
- **Temática:** TM-05 Valoración de activos y estructura temporal (principal) · secundarias: TM-07
- **Calidad Q:** 90 (A) — Tipo 20/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** ISBN: 978-0-08-055585-0 · SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=891620
- **Acceso y licencia:** Versión SSRN gratuita
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «dividend discount model equity premium puzzle residual income valuation Gordon growth (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Equity premium puzzle»)
- **Contenido:** Primas de riesgo históricas de 17 países desde 1900; la prima mundial es menor que la de EE. UU. por sesgo de supervivencia.
- **Uso en el Motor:** MC-09: primas históricas internacionales como contraste de la prima implícita.
- **Limitaciones:** Datos hasta 2005 en la versión citada.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0311 · Q 89 (A) — Zero-Coupon Yield Curves: Technical Documentation

- **Autores:** Bank for International Settlements (contribuciones de bancos centrales)
- **Año:** 2005
- **Publicación o institución:** BIS Papers n.º 25 (30 de octubre de 2005)
- **Tipo de documento:** Informe técnico con metodología (organismo oficial)
- **Temática:** TM-05 Valoración de activos y estructura temporal (principal) · secundarias: —
- **Calidad Q:** 89 (A) — Tipo 20/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://www.bis.org/publ/bppdf/bispap25j.pdf
- **Acceso y licencia:** Acceso gratuito (BPI)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Banco de España documento de trabajo estimación estructura temporal de los tipos de interés Nelson Siegel Svensson»; WebFetch: sí, documento BIS Papers 25)
- **Contenido:** Recopila los métodos de estimación de curvas cupón cero de los bancos centrales del BPI; la mayoría usa Nelson-Siegel o la extensión de Svensson.
- **Uso en el Motor:** MC-09: estándar oficial de estimación de curvas (contraste de la implementación).
- **Limitaciones:** Documento de 2005; prácticas posteriores no recogidas.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0048 · Q 89 (A) — Estimating and Interpreting Forward Interest Rates: Sweden 1992-1994

- **Autores:** Lars E. O. Svensson
- **Año:** 1994
- **Publicación o institución:** NBER Working Paper 4871 (septiembre de 1994); también IMF Working Paper 94/114; versión resumida publicada como «Estimating Forward Interest Rates with the Extended Nelson and Siegel Method», Sveriges Riksbank Quarterly Review 1995:3, págs. 13-26
- **Tipo de documento:** Documento de trabajo
- **Temática:** TM-05 Valoración de activos y estructura temporal (principal)
- **Calidad Q:** 89 (A) — Tipo 20/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 9/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI: 10.3386/w4871 · https://www.nber.org/papers/w4871 · Copia del autor: https://larseosvensson.se/files/papers/estimating-and-interpreting-forward-rates-sweden-1992-1994-IMFwp94-114.pdf
- **Acceso y licencia:** Acceso gratuito (NBER, FMI y página del autor)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Svensson "Estimating and Interpreting Forward Interest Rates: Sweden 1992-1994" NBER working paper 4871»; WebFetch: sí)
- **Contenido:** Extiende Nelson-Siegel con un segundo término de curvatura (método Svensson) para estimar curvas de tipos a plazo e interpretarlas como expectativas de política monetaria; método adoptado por numerosos bancos centrales.
- **Uso en el Motor:** MC-09: extensión de Nelson-Siegel con segunda curvatura.
- **Limitaciones:** Inestabilidad numérica de parámetros; aplicación empírica a Suecia.
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02.

#### DOC-MOT-0308 · Q 88 (A) — Interest Rate Models: Theory and Practice (2.ª ed.)

- **Autores:** Damiano Brigo; Fabio Mercurio
- **Año:** 2006
- **Publicación o institución:** Springer (Springer Finance)
- **Tipo de documento:** Manual de referencia
- **Temática:** TM-05 Valoración de activos y estructura temporal (principal) · secundarias: TM-06
- **Calidad Q:** 88 (A) — Tipo 20/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.1007/978-3-540-34604-3 · ISBN: 978-3-540-22149-4 · Cita en https://en.wikipedia.org/wiki/Short-rate_model
- **Acceso y licencia:** De pago (Springer)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Vasicek model Cox–Ingersoll–Ross model Heath–Jarrow–Morton framework affine term structure model yield curve (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Short-rate model», que reproduce la cita completa)
- **Contenido:** Referencia de modelos de tipos: tipo corto, extensiones por desplazamiento determinista (CIR++), HJM, modelo de mercado LIBOR, sonrisa, inflación y crédito.
- **Uso en el Motor:** MC-09: modelos de tipos calibrados.
- **Limitaciones:** Extenso; orientado a derivados de tipos.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0314 · Q 88 (A) — Dividends, Earnings, and Stock Prices

- **Autores:** Myron J. Gordon
- **Año:** 1959
- **Publicación o institución:** Review of Economics and Statistics, vol. 41, n.º 2, págs. 99-105
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-05 Valoración de activos y estructura temporal (principal) · secundarias: —
- **Calidad Q:** 88 (A) — Tipo 25/25 · Rigor 14/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.2307/1927792 · JSTOR: https://www.jstor.org/stable/1927792
- **Acceso y licencia:** Texto completo por suscripción en la editorial (MIT Press/JSTOR)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «dividend discount model equity premium puzzle residual income valuation Gordon growth (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Dividend discount model», que reproduce la cita completa)
- **Contenido:** Fundamenta el modelo de descuento de dividendos con crecimiento constante (modelo de Gordon) y lo contrasta empíricamente.
- **Uso en el Motor:** MC-09: valor terminal y rentabilidad implícita.
- **Limitaciones:** Muy sensible a g y r; supone crecimiento perpetuo.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0305 · Q 87 (A) — Term Structure Movements and Pricing Interest Rate Contingent Claims

- **Autores:** Thomas S. Y. Ho; Sang-Bin Lee
- **Año:** 1986
- **Publicación o institución:** The Journal of Finance, vol. 41, n.º 5, págs. 1011-1029
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-05 Valoración de activos y estructura temporal (principal) · secundarias: TM-06
- **Calidad Q:** 87 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 8/10 · Impacto 9/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.2307/2328161 · JSTOR: 2328161
- **Acceso y licencia:** Texto completo por suscripción en la editorial (Wiley/JSTOR)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Vasicek model Cox–Ingersoll–Ross model Heath–Jarrow–Morton framework affine term structure model yield curve (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Short-rate model», que reproduce la cita completa)
- **Contenido:** Primer modelo de no arbitraje calibrado a la curva observada mediante un árbol binomial de curvas.
- **Uso en el Motor:** MC-09: árboles de tipos sin arbitraje.
- **Limitaciones:** Sin reversión a la media.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0050 · Q 86 (A) — Common Factors Affecting Bond Returns

- **Autores:** Robert Litterman; José Scheinkman
- **Año:** 1991
- **Publicación o institución:** The Journal of Fixed Income, vol. 1, n.º 1, págs. 54-61
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-05 Valoración de activos y estructura temporal (principal)
- **Calidad Q:** 86 (A) — Tipo 22/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 4/10 (rebajada de 89: sin página editorial ni copia abierta localizadas)
- **DOI / ISBN / URL:** DOI no visto (se retira «10.3905/jfi.1991.692347 a verificar») · Cita confirmada en fuente secundaria: https://r-bloggers.com/2022/05/understanding-pca-3-factors-of-the-yield-curve-using-r-code
- **Acceso y licencia:** Revista por suscripción (PM Research); sin copia gratuita identificada
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Litterman Scheinkman (1991) Journal of Fixed Income 1(1) 54-61 level slope curvature principal components»; WebFetch: sí, solo de la fuente secundaria que reproduce la cita completa)
- **Contenido:** Muestra con componentes principales que tres factores (nivel, pendiente y curvatura) explican en torno al 99 % de la variación de las rentabilidades de bonos del Tesoro y propone coberturas basadas en ellos.
- **Uso en el Motor:** MC-09: componentes principales de la curva para riesgo de tipos.
- **Limitaciones:** Muestra histórica estadounidense. Alerta: REPARAR enlace (localizar página editorial/DOI en el próximo barrido).
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (metadatos bibliográficos coincidentes en fuente secundaria).

#### DOC-MOT-0307 · Q 85 (A) — Bond and Option Pricing when Short Rates are Lognormal

- **Autores:** Fischer Black; Piotr Karasinski
- **Año:** 1991
- **Publicación o institución:** Financial Analysts Journal, vol. 47, n.º 4, págs. 52-59
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-05 Valoración de activos y estructura temporal (principal) · secundarias: TM-06
- **Calidad Q:** 85 (A) — Tipo 24/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 9/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.2469/faj.v47.n4.52
- **Acceso y licencia:** Texto completo por suscripción en la editorial (Taylor & Francis)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Vasicek model Cox–Ingersoll–Ross model Heath–Jarrow–Morton framework affine term structure model yield curve (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Short-rate model», que reproduce la cita completa)
- **Contenido:** Modelo de tipo corto lognormal con reversión a la media, implementado en árbol y calibrado a curva y volatilidades.
- **Uso en el Motor:** MC-09: tipos estrictamente positivos en valoración.
- **Limitaciones:** Sin solución cerrada para bonos; inviable con tipos negativos.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0054 · Q 84 (A) — Investment Valuation: Tools and Techniques for Determining the Value of Any Asset (3.ª ed.)

- **Autores:** Aswath Damodaran
- **Año:** 2012
- **Publicación o institución:** John Wiley & Sons (Wiley Finance)
- **Tipo de documento:** Manual de referencia
- **Temática:** TM-05 Valoración de activos y estructura temporal (principal) · secundarias: TM-07
- **Calidad Q:** 84 (A) — Tipo 20/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 9/10 · Acceso 5/10
- **DOI / ISBN / URL:** ISBN: 978-1-118-01152-2 (tapa dura) · https://www.oreilly.com/library/view/investment-valuation-tools/9781118011522/03_copyright.html
- **Acceso y licencia:** De pago (Wiley); material complementario gratuito en la web del autor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Damodaran "Investment Valuation" third edition Wiley 2012 ISBN»; WebFetch: no)
- **Contenido:** Manual integral de valoración: descuento de flujos (FCFF/FCFE), coste de capital, múltiplos, valoración relativa y de activos difíciles (empresas jóvenes, en pérdidas, financieras).
- **Uso en el Motor:** MC-09: descuento de flujos, múltiplos, valoración relativa.
- **Limitaciones:** Manual profesional; casos y datos de 2010-2011.
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (ISBN visto en catálogos y en la página de copyright de O'Reilly).

#### DOC-MOT-0053 · Q 82 (A) — Equity Risk Premiums (ERP): Determinants, Estimation, and Implications — The 2026 Edition

- **Autores:** Aswath Damodaran
- **Año:** 2026 (actualización anual; serie iniciada en 2008)
- **Publicación o institución:** NYU Stern School of Business (Damodaran Online y SSRN)
- **Tipo de documento:** Documento de trabajo (actualización anual)
- **Temática:** TM-05 Valoración de activos y estructura temporal (principal)
- **Calidad Q:** 82 (A) — Tipo 15/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 8/10 · Acceso 10/10
- **DOI / ISBN / URL:** Sin DOI visto · Anuncio de la edición 2026: https://www.bvresources.com/articles/bvwire/damodaran-unveils-his-annual-erp-update · Ediciones anteriores en el servidor del autor (p. ej., https://pages.stern.nyu.edu/~adamodar/pdfiles/papers/ERP2022Formatted.pdf)
- **Acceso y licencia:** Acceso gratuito (página del autor y SSRN)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Damodaran "Equity Risk Premiums (ERP): Determinants, Estimation, and Implications" 2025 Edition SSRN» y «… "The 2025 Edition" ssrn»; WebFetch: sí, del anuncio de BVResources, que identifica la edición 2026)
- **Contenido:** Revisión anual de los métodos de estimación de la prima de riesgo de la renta variable (histórica, de encuesta e implícita por descuento de flujos), con la prima implícita del S&P 500 y primas por país.
- **Uso en el Motor:** MC-09: prima de riesgo implícita y comparación con primas históricas y de encuesta.
- **Limitaciones:** Supuestos de crecimiento terminal; un solo autor sin revisión por pares. Alerta: REPARAR enlace (sustituir por la URL SSRN o del PDF de la edición 2026 en el próximo barrido). Corrección: la semilla indicaba 2025; la edición vigente es la de 2026.
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02.

#### DOC-MOT-0317 · Q 78 (B) — Estrategias de inmunización ante posibles desplazamientos en la estructura temporal

- **Autores:** Inmaculada Gómez; Alfonso Novales
- **Año:** 1997
- **Publicación o institución:** Instituto Complutense de Análisis Económico (ICAE), Universidad Complutense de Madrid, Documento de trabajo 9707
- **Tipo de documento:** Documento de trabajo
- **Temática:** TM-05 Valoración de activos y estructura temporal (principal) · secundarias: TM-08
- **Calidad Q:** 78 (B) — Tipo 20/25 · Rigor 14/20 · Autoridad 12/15 · Vigencia 7/10 · Impacto 6/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** https://eprints.ucm.es/28077/1/9707.pdf
- **Acceso y licencia:** Acceso gratuito (repositorio UCM)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Banco de España documento de trabajo estimación estructura temporal de los tipos de interés Nelson Siegel Svensson»; WebFetch: sí, documento completo en E-Prints UCM)
- **Contenido:** Estima Nelson-Siegel sobre deuda pública española 1992-1996 y muestra que los cambios de curva rara vez son paralelos, lo que exige inmunización multivariante.
- **Uso en el Motor:** MC-09: evidencia española de factores de curva y cobertura.
- **Limitaciones:** Muestra antigua anterior al euro.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

## TM-06 Derivados y volatilidad implícita

#### DOC-MOT-0002 · Q 97 (A) — Option Pricing: A Simplified Approach

- **Autores:** John C. Cox; Stephen A. Ross; Mark Rubinstein
- **Año:** 1979
- **Publicación o institución:** Journal of Financial Economics, vol. 7, n.º 3, págs. 229-263
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-06 Derivados y volatilidad implícita (principal) · secundarias: TM-09
- **Calidad Q:** 97 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** DOI: 10.1016/0304-405X(79)90015-1 · https://doi.org/10.1016%2F0304-405X%2879%2990015-1 · CiteSeerX: https://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.379.7582
- **Acceso y licencia:** Editorial por suscripción (Elsevier); copias de lectura en CiteSeerX y página universitaria (V2.3)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Black–Scholes model Merton 1973 Heston model binomial options pricing (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Binomial options pricing model», que reproduce la cita completa)
- **Contenido:** Modelo binomial CRR: árbol recombinante con probabilidades neutrales al riesgo, convergencia a Black-Scholes y valoración americana por retro-inducción.
- **Uso en el Motor:** MC-09: valoración binomial y americana discreta; contraste de convergencia de métodos discretos.
- **Limitaciones:** Discretización; oscilación de la convergencia con pocos pasos.
- **Origen:** Ficha de carga V2.3 re-verificada por DOC-M el 2026-11-02 (tanda 2); se normaliza al formato del encargo.

#### DOC-MOT-0319 · Q 97 (A) — Option Pricing When Underlying Stock Returns Are Discontinuous

- **Autores:** Robert C. Merton
- **Año:** 1976
- **Publicación o institución:** Journal of Financial Economics, vol. 3, n.º 1-2, págs. 125-144
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-06 Derivados y volatilidad implícita (principal) · secundarias: TM-08
- **Calidad Q:** 97 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** DOI: 10.1016/0304-405X(76)90022-2 · Copia abierta: https://hdl.handle.net/1721.1/1899 (MIT)
- **Acceso y licencia:** Copia gratuita en MIT DSpace; revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «VIX variance swap jump diffusion volatility risk premium implied volatility (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Stochastic volatility jump models», que reproduce la cita completa y «Hierarchical Risk Parity»)
- **Contenido:** Modelo de difusión con saltos de Poisson lognormales y fórmula de valoración como mezcla de precios Black-Scholes.
- **Uso en el Motor:** MC-09, MC-05: saltos en precios y colas de la sonrisa.
- **Limitaciones:** Riesgo de salto diversificable por supuesto.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0055 · Q 96 (A) — Theory of Rational Option Pricing

- **Autores:** Robert C. Merton
- **Año:** 1973
- **Publicación o institución:** The Bell Journal of Economics and Management Science, vol. 4, n.º 1, págs. 141-183
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-06 Derivados y volatilidad implícita (principal) · secundarias: TM-05
- **Calidad Q:** 96 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** DOI: 10.2307/3003143 · JSTOR: https://www.jstor.org/stable/3003143 · Copias abiertas: https://hdl.handle.net/1721.1/49331 (MIT) y https://hdl.handle.net/10338.dmlcz%2F135817
- **Acceso y licencia:** Acceso gratuito en repositorios (MIT DSpace, DML-CZ); editorial por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Black–Scholes model Merton 1973 Heston model binomial options pricing (dominio en.wikipedia.org)» y «Vasicek model Cox–Ingersoll–Ross model Heath–Jarrow–Morton framework affine term structure model yield curve (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Black–Scholes model», que reproduce la cita completa y «Short-rate model»)
- **Contenido:** Establece cotas de no arbitraje para opciones, extiende Black-Scholes a dividendos continuos y tipos estocásticos y formaliza la valoración racional de opciones.
- **Uso en el Motor:** MC-09: cotas de no arbitraje y extensiones de Black-Scholes (dividendos continuos).
- **Limitaciones:** Mercado sin fricciones.
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (tanda 2).

#### DOC-MOT-0324 · Q 95 (A) — Arbitrage-Free SVI Volatility Surfaces

- **Autores:** Jim Gatheral; Antoine Jacquier
- **Año:** 2014
- **Publicación o institución:** Quantitative Finance, vol. 14, págs. 59-71
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-06 Derivados y volatilidad implícita (principal) · secundarias: TM-09
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** DOI: 10.1080/14697688.2013.819986 · arXiv: https://arxiv.org/abs/1204.0646
- **Acceso y licencia:** Preprint gratuito en arXiv; revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «local volatility Dupire SABR volatility model volatility smile variance swap (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Stochastic volatility», que reproduce la cita completa)
- **Contenido:** Condiciones para parametrizaciones SVI libres de arbitraje estático (mariposa y calendario) y método de ajuste de superficies.
- **Uso en el Motor:** MC-09: ajuste de superficies de volatilidad sin arbitraje.
- **Limitaciones:** Parametrización específica; requiere optimización cuidadosa.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0326 · Q 95 (A) — Transform Analysis and Asset Pricing for Affine Jump-Diffusions

- **Autores:** Darrell Duffie; Jun Pan; Kenneth J. Singleton
- **Año:** 2000
- **Publicación o institución:** Econometrica, vol. 68, n.º 6, págs. 1343-1376
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-06 Derivados y volatilidad implícita (principal) · secundarias: TM-05
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1111/1468-0262.00164 · https://doi.org/10.1111%2F1468-0262.00164
- **Acceso y licencia:** Texto completo por suscripción en la editorial (Econometric Society/Wiley)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «VIX variance swap jump diffusion volatility risk premium implied volatility (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Stochastic volatility jump models», que reproduce la cita completa)
- **Contenido:** Transformadas analíticas para difusiones afines con saltos que dan precios de opciones y bonos en forma semicerrada.
- **Uso en el Motor:** MC-09: valoración por transformadas en modelos afines.
- **Limitaciones:** Muy técnico.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0322 · Q 95 (A) — Implied Volatility Functions: Empirical Tests

- **Autores:** Bernard Dumas; Jeff Fleming; Robert E. Whaley
- **Año:** 1998
- **Publicación o institución:** The Journal of Finance, vol. 53, n.º 6, págs. 2059-2106
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-06 Derivados y volatilidad implícita (principal) · secundarias: TM-11
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI: 10.1111/0022-1082.00083 · NBER: http://www.nber.org/papers/w5500.pdf
- **Acceso y licencia:** NBER WP gratuito; revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «local volatility Dupire SABR volatility model volatility smile variance swap (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Local volatility», que reproduce la cita completa)
- **Contenido:** Contrasta fuera de muestra las funciones deterministas de volatilidad: no mejoran a un Black-Scholes ad hoc en valoración y cobertura.
- **Uso en el Motor:** MC-09, MC-10: validación de modelos de sonrisa.
- **Limitaciones:** Opciones del S&P 500 1988-1993.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0001 · Q 95 (A) — The Pricing of Options and Corporate Liabilities

- **Autores:** Fischer Black; Myron Scholes
- **Año:** 1973
- **Publicación o institución:** Journal of Political Economy, vol. 81, n.º 3, págs. 637-654 (University of Chicago Press)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-06 Derivados y volatilidad implícita (principal) · secundarias: TM-05
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1086/260062 · JSTOR: https://www.jstor.org/stable/1831029
- **Acceso y licencia:** Texto completo por suscripción en la editorial (University of Chicago Press/JSTOR)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Black–Scholes model Merton 1973 Heston model binomial options pricing (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Black–Scholes model», que reproduce la cita completa)
- **Contenido:** Deriva la ecuación de valoración de opciones europeas por réplica sin arbitraje y la fórmula cerrada bajo volatilidad y tipos constantes.
- **Uso en el Motor:** MC-09: valoración cerrada de opciones europeas e inversión para volatilidad implícita.
- **Limitaciones:** Supuestos estrictos (volatilidad constante, sin fricciones); no cubre ejercicio americano.
- **Origen:** Ficha de carga V2.3 re-verificada por DOC-M el 2026-11-02 (tanda 2); se normaliza al formato del encargo.

#### DOC-MOT-0057 · Q 94 (A) — Variance Risk Premiums

- **Autores:** Peter Carr; Liuren Wu
- **Año:** 2009
- **Publicación o institución:** The Review of Financial Studies, vol. 22, n.º 3, págs. 1311-1341 (versión previa: SSRN 577222, «Variance Risk Premia»)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-06 Derivados y volatilidad implícita (principal) · secundarias: TM-03
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1093/rfs/hhn038 · https://ideas.repec.org/a/oup/rfinst/v22y2009i3p1311-1341..html · Versión SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=577222
- **Acceso y licencia:** Texto completo por suscripción en la editorial (OUP); versión de trabajo en SSRN
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Carr Wu "Variance Risk Premiums" Review of Financial Studies 2009 22(3) 1311»; WebFetch: sí, ficha IDEAS/RePEc (metadatos completos) y página Wikipedia «Variance swap» (versión SSRN))
- **Contenido:** Mide la prima de riesgo de varianza como diferencia entre varianza realizada y tasa de swap de varianza sintetizada con opciones, para índices y acciones.
- **Uso en el Motor:** MC-09: prima de riesgo de varianza (implícita frente a realizada).
- **Limitaciones:** Requiere cadenas de opciones completas y de calidad.
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (tanda 2).

#### DOC-MOT-0004 · Q 94 (A) — A Closed-Form Solution for Options with Stochastic Volatility with Applications to Bond and Currency Options

- **Autores:** Steven L. Heston
- **Año:** 1993
- **Publicación o institución:** The Review of Financial Studies, vol. 6, n.º 2, págs. 327-343 (Oxford University Press)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-06 Derivados y volatilidad implícita (principal) · secundarias: TM-03
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1093/rfs/6.2.327 · https://doi.org/10.1093%2Frfs%2F6.2.327
- **Acceso y licencia:** Texto completo por suscripción en la editorial (OUP)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «VIX variance swap jump diffusion volatility risk premium implied volatility (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Stochastic volatility jump models», que reproduce la cita completa y «Stochastic volatility»)
- **Contenido:** Solución semicerrada mediante función característica para opciones europeas con volatilidad estocástica de reversión a la media correlacionada con el subyacente.
- **Uso en el Motor:** MC-09: valoración con volatilidad estocástica y calibración de superficies.
- **Limitaciones:** Integración numérica sensible a parámetros; calibración no tratada.
- **Origen:** Ficha de carga V2.3 re-verificada por DOC-M el 2026-11-02 (tanda 2); se normaliza al formato del encargo.

#### DOC-MOT-0331 · Q 93 (A) — The Impact of Jumps in Volatility and Returns

- **Autores:** Bjørn Eraker; Michael Johannes; Nicholas Polson
- **Año:** 2003
- **Publicación o institución:** The Journal of Finance, vol. 58, n.º 3, págs. 1269-1300
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-06 Derivados y volatilidad implícita (principal) · secundarias: TM-03
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1111/1540-6261.00566 · https://doi.org/10.1111%2F1540-6261.00566
- **Acceso y licencia:** Texto completo por suscripción en la editorial (Wiley)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «VIX variance swap jump diffusion volatility risk premium implied volatility (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Stochastic volatility jump models», que reproduce la cita completa)
- **Contenido:** Estima por MCMC modelos con saltos en rendimientos y en volatilidad sobre el S&P 500 y el Nasdaq: los saltos en volatilidad son relevantes.
- **Uso en el Motor:** MC-09, MC-05: especificación de saltos en volatilidad.
- **Limitaciones:** Estimación bayesiana costosa.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0327 · Q 93 (A) — Option Valuation Using the Fast Fourier Transform

- **Autores:** Peter Carr; Dilip B. Madan
- **Año:** 1999
- **Publicación o institución:** Journal of Computational Finance, vol. 2, n.º 4, págs. 61-73
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-06 Derivados y volatilidad implícita (principal) · secundarias: TM-09
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.21314/JCF.1999.043 · https://doi.org/10.21314%2FJCF.1999.043
- **Acceso y licencia:** Texto completo por suscripción en la editorial (Risk.net)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «VIX variance swap jump diffusion volatility risk premium implied volatility (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Stochastic volatility jump models», que reproduce la cita completa)
- **Contenido:** Valora opciones con la FFT a partir de la función característica, obteniendo de una vez precios para toda una malla de strikes.
- **Uso en el Motor:** MC-09: valoración rápida en modelos con función característica.
- **Limitaciones:** Elección del parámetro de amortiguación y de la malla.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0325 · Q 93 (A) — Jumps and Stochastic Volatility: Exchange Rate Processes Implicit in Deutsche Mark Options

- **Autores:** David S. Bates
- **Año:** 1996
- **Publicación o institución:** The Review of Financial Studies, vol. 9, n.º 1, págs. 69-107
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-06 Derivados y volatilidad implícita (principal) · secundarias: TM-03
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1093/rfs/9.1.69 · https://doi.org/10.1093%2Frfs%2F9.1.69
- **Acceso y licencia:** Texto completo por suscripción en la editorial (OUP)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «VIX variance swap jump diffusion volatility risk premium implied volatility (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Stochastic volatility jump models», que reproduce la cita completa)
- **Contenido:** Combina volatilidad estocástica tipo Heston con saltos (modelo SVJ) y lo estima con opciones sobre el marco alemán.
- **Uso en el Motor:** MC-09: modelos SVJ para sonrisas de corto plazo.
- **Limitaciones:** Calibración con muchos parámetros.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0318 · Q 93 (A) — The Pricing of Commodity Contracts

- **Autores:** Fischer Black
- **Año:** 1976
- **Publicación o institución:** Journal of Financial Economics, vol. 3, n.º 1-2, págs. 167-179
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-06 Derivados y volatilidad implícita (principal) · secundarias: TM-05
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1016/0304-405X(76)90024-6 · https://doi.org/10.1016/0304-405X(76)90024-6
- **Acceso y licencia:** Texto completo por suscripción en la editorial (Elsevier)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «local volatility Dupire SABR volatility model volatility smile variance swap (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Black model», que reproduce la cita completa)
- **Contenido:** Modelo Black-76 para opciones sobre futuros y forwards, estándar para caps, floors y swaptions.
- **Uso en el Motor:** MC-09: opciones sobre futuros y derivados de tipos.
- **Limitaciones:** Lognormalidad; inadecuado con tipos negativos (usar Bachelier).
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0332 · Q 92 (A) — The Jump-Risk Premia Implicit in Options: Evidence from an Integrated Time-Series Study

- **Autores:** Jun Pan
- **Año:** 2002
- **Publicación o institución:** Journal of Financial Economics, vol. 63, n.º 1, págs. 3-50
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-06 Derivados y volatilidad implícita (principal) · secundarias: TM-08
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.1016/S0304-405X(01)00092-2 (marcado como inactivo en Wikipedia a 14/08/2025)
- **Acceso y licencia:** Texto completo por suscripción en la editorial (Elsevier)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «VIX variance swap jump diffusion volatility risk premium implied volatility (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Stochastic volatility jump models», que reproduce la cita completa)
- **Contenido:** Estimación conjunta con precios spot y de opciones de la prima por riesgo de salto, que explica buena parte de la sonrisa.
- **Uso en el Motor:** MC-09: primas de riesgo de salto.
- **Limitaciones:** Alerta: REPARAR (DOI marcado inactivo; buscar URL editorial).
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0329 · Q 91 (A) — Efficient Analytic Approximation of American Option Values

- **Autores:** Giovanni Barone-Adesi; Robert E. Whaley
- **Año:** 1987
- **Publicación o institución:** The Journal of Finance, vol. 42, n.º 2, págs. 301-320
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-06 Derivados y volatilidad implícita (principal) · secundarias: TM-09
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI: 10.2307/2328254 · https://ideas.repec.org/a/bla/jfinan/v42y1987i2p301-20.html
- **Acceso y licencia:** Texto completo por suscripción en la editorial; ficha en IDEAS
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Black–Scholes model Merton 1973 Heston model binomial options pricing (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Black–Scholes model», que reproduce la cita completa)
- **Contenido:** Aproximación cuadrática analítica para opciones americanas sobre activos con dividendo continuo o futuros.
- **Uso en el Motor:** MC-09: valoración americana rápida.
- **Limitaciones:** Error apreciable a vencimientos largos.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0056 · Q 90 (A) — Prices of State-Contingent Claims Implicit in Option Prices

- **Autores:** Douglas T. Breeden; Robert H. Litzenberger
- **Año:** 1978
- **Publicación o institución:** The Journal of Business, págs. 621-651
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-06 Derivados y volatilidad implícita (principal) · secundarias: —
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** DOI no visto (se retira «10.1086/296025 a verificar») · Cita en https://en.wikipedia.org/wiki/Black%E2%80%93Scholes_model
- **Acceso y licencia:** Texto completo por suscripción en la editorial (University of Chicago Press/JSTOR); sin copia abierta identificada
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Black–Scholes model Merton 1973 Heston model binomial options pricing (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Black–Scholes model», que reproduce la cita completa)
- **Contenido:** Muestra que la segunda derivada del precio de la opción respecto al precio de ejercicio da la densidad de precios de estado (densidad neutral al riesgo).
- **Uso en el Motor:** MC-09: densidad neutral al riesgo a partir de precios de opciones.
- **Limitaciones:** Requiere interpolación suave de la curva de precios por strike. Alerta: REPARAR (localizar DOI/volumen en la editorial).
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (tanda 2).

#### DOC-MOT-0334 · Q 86 (A) — Summary Statistics of Option-Implied Probability Density Functions and Their Properties

- **Autores:** Damien Lynch; Nikolaos Panigirtzoglou
- **Año:** 2008
- **Publicación o institución:** Bank of England Working Paper n.º 345 (marzo de 2008)
- **Tipo de documento:** Documento de trabajo
- **Temática:** TM-06 Derivados y volatilidad implícita (principal) · secundarias: TM-11
- **Calidad Q:** 86 (A) — Tipo 20/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 7/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://www.bankofengland.co.uk/-/media/boe/files/working-paper/2008/summary-statistics-of-option-implied-probability-density-functions.pdf
- **Acceso y licencia:** Acceso gratuito (Banco de Inglaterra)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Bank of England Quarterly Bulletin 2012 "Option-implied probability distributions for future inflation"»; WebFetch: sí, documento completo)
- **Contenido:** Estadísticos diarios de densidades implícitas (incertidumbre, asimetría, colas) para índices y tipos de EE. UU. y Reino Unido: persistentes, reaccionan a crisis pero no las anticipan.
- **Uso en el Motor:** MC-09, MC-10: uso y límites de momentos implícitos como señales.
- **Limitaciones:** Muestra hasta 2006.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0010 · Q 86 (A) — Financial Modelling with Jump Processes

- **Autores:** Rama Cont; Peter Tankov
- **Año:** 2004
- **Publicación o institución:** Chapman & Hall/CRC Press (Financial Mathematics Series)
- **Tipo de documento:** Libro académico
- **Temática:** TM-06 Derivados y volatilidad implícita (principal) · secundarias: TM-08, TM-09
- **Calidad Q:** 86 (A) — Tipo 20/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** ISBN: 978-1-58488-413-2 · https://www.eyrolles.com/Sciences/Livre/financial-modelling-with-jump-processes-9781584884132
- **Acceso y licencia:** De pago; sin texto completo gratuito legal identificado
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Cont Tankov "Financial Modelling with Jump Processes" Chapman Hall CRC 2004»; WebFetch: no (confirmado en catálogos de bibliotecas y librería))
- **Contenido:** Procesos de Lévy y modelos con saltos: construcción, cambios de medida, simulación y valoración de opciones, con métodos numéricos asociados.
- **Uso en el Motor:** MC-09, MC-05: modelos con saltos y simulación de trayectorias discontinuas.
- **Limitaciones:** Exige base sólida en procesos estocásticos; calibración práctica limitada.
- **Origen:** Ficha de carga V2.3 re-verificada por DOC-M el 2026-11-02 (tanda 2); se normaliza al formato del encargo.

#### DOC-MOT-0323 · Q 86 (A) — Managing Smile Risk

- **Autores:** Patrick S. Hagan; Deep Kumar; Andrew S. Lesniewski; Diana E. Woodward
- **Año:** 2002
- **Publicación o institución:** Wilmott Magazine, págs. 84-108
- **Tipo de documento:** Artículo en revista profesional
- **Temática:** TM-06 Derivados y volatilidad implícita (principal) · secundarias: TM-05
- **Calidad Q:** 86 (A) — Tipo 15/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** Sin DOI · Copia de autor: http://lesniewski.us/papers/published/ManagingSmileRisk.pdf
- **Acceso y licencia:** Copia gratuita del autor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «local volatility Dupire SABR volatility model volatility smile variance swap (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «SABR volatility model», que reproduce la cita completa)
- **Contenido:** Introduce el modelo SABR y su aproximación asintótica de volatilidad implícita, con dinámica de sonrisa coherente.
- **Uso en el Motor:** MC-09: interpolación y cobertura de sonrisas de tipos.
- **Limitaciones:** Aproximación inexacta en alas y con tipos bajos; ver versión sin arbitraje.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0059 · Q 84 (A) — Options, Futures, and Other Derivatives (11.ª ed.)

- **Autores:** John C. Hull
- **Año:** 2021
- **Publicación o institución:** Pearson
- **Tipo de documento:** Manual de referencia
- **Temática:** TM-06 Derivados y volatilidad implícita (principal) · secundarias: TM-05
- **Calidad Q:** 84 (A) — Tipo 20/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 9/10 · Acceso 5/10
- **DOI / ISBN / URL:** ISBN no visto · Cita de la 11.ª ed. en https://en.wikipedia.org/wiki/Short-rate_model
- **Acceso y licencia:** De pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Vasicek model Cox–Ingersoll–Ross model Heath–Jarrow–Morton framework affine term structure model yield curve (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Short-rate model», que reproduce la cita completa)
- **Contenido:** Manual de referencia de derivados: futuros, swaps, opciones, griegas, árboles, volatilidad y modelos de tipos.
- **Uso en el Motor:** MC-09: referencia operativa de derivados.
- **Limitaciones:** Manual de máster, no de investigación; ediciones anteriores circulan con numeración distinta.
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (tanda 2).

#### DOC-MOT-0330 · Q 84 (A) — Let's Be Rational

- **Autores:** Peter Jäckel
- **Año:** 2015
- **Publicación o institución:** Wilmott Magazine, vol. 2015, n.º 75, págs. 40-53
- **Tipo de documento:** Artículo en revista profesional
- **Temática:** TM-06 Derivados y volatilidad implícita (principal) · secundarias: TM-09
- **Calidad Q:** 84 (A) — Tipo 15/25 · Rigor 18/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI: 10.1002/wilm.10395 · Implementación de referencia del autor: http://www.jaeckel.org
- **Acceso y licencia:** Revista de pago; código de referencia gratuito del autor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «VIX variance swap jump diffusion volatility risk premium implied volatility (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Implied volatility», que reproduce la cita completa)
- **Contenido:** Algoritmo para invertir Black-Scholes y obtener la volatilidad implícita a precisión de máquina en dos iteraciones.
- **Uso en el Motor:** MC-09: cálculo robusto de volatilidad implícita.
- **Limitaciones:** Revista profesional.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0333 · Q 84 (A) — Option-Implied Probability Distributions for Future Inflation

- **Autores:** Tom Smith
- **Año:** 2012
- **Publicación o institución:** Bank of England Quarterly Bulletin, vol. 52, n.º 3, págs. 224-234
- **Tipo de documento:** Artículo de banco central
- **Temática:** TM-06 Derivados y volatilidad implícita (principal) · secundarias: TM-05
- **Calidad Q:** 84 (A) — Tipo 20/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 7/10 · Independencia 9/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://ideas.repec.org/a/boe/qbullt/0083.html · https://www.bankofengland.co.uk/quarterly-bulletin/2012/q3/option-implied-probability-distributions-for-future-inflation
- **Acceso y licencia:** Acceso gratuito (Banco de Inglaterra)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Bank of England Quarterly Bulletin 2012 "Option-implied probability distributions for future inflation"»; WebFetch: sí, ficha IDEAS)
- **Contenido:** Extrae distribuciones de probabilidad neutrales al riesgo de la inflación futura a partir de opciones de inflación (caps/floors) en el Reino Unido.
- **Uso en el Motor:** MC-09: densidades implícitas en opciones de inflación.
- **Limitaciones:** Densidades neutrales al riesgo, no probabilidades reales.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0320 · Q 82 (A) — Pricing with a Smile

- **Autores:** Bruno Dupire
- **Año:** 1994
- **Publicación o institución:** Risk, vol. 7, n.º 1 (enero de 1994), Incisive Media
- **Tipo de documento:** Artículo en revista profesional
- **Temática:** TM-06 Derivados y volatilidad implícita (principal) · secundarias: —
- **Calidad Q:** 82 (A) — Tipo 15/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** Sin DOI · Cita en https://en.wikipedia.org/wiki/Bruno_Dupire y https://en.wikipedia.org/wiki/Local_volatility
- **Acceso y licencia:** Revista profesional de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «local volatility Dupire SABR volatility model volatility smile variance swap (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Bruno Dupire», que reproduce la cita completa y «Local volatility»)
- **Contenido:** Deriva la volatilidad local única consistente con la superficie de precios de opciones europeas (fórmula de Dupire).
- **Uso en el Motor:** MC-09: calibración de volatilidad local.
- **Limitaciones:** Inestable con datos ruidosos; dinámica de sonrisa poco realista.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0011 · Q 80 (A) — The Volatility Surface: A Practitioner's Guide

- **Autores:** Jim Gatheral
- **Año:** 2006
- **Publicación o institución:** John Wiley & Sons (Wiley Finance)
- **Tipo de documento:** Libro académico-profesional
- **Temática:** TM-06 Derivados y volatilidad implícita (principal) · secundarias: TM-03
- **Calidad Q:** 80 (A) — Tipo 18/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 9/10 · Acceso 5/10
- **DOI / ISBN / URL:** ISBN: 978-0-471-79251-2 · Cita en https://en.wikipedia.org/wiki/Local_volatility
- **Acceso y licencia:** De pago (Wiley)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «local volatility Dupire SABR volatility model volatility smile variance swap (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Local volatility», que reproduce la cita completa y «Stochastic volatility»)
- **Contenido:** Guía práctica de la superficie de volatilidad: volatilidad local y estocástica, saltos, asintóticas de la sonrisa y calibración.
- **Uso en el Motor:** MC-09: superficies de volatilidad y criterios de calibración.
- **Limitaciones:** Orientado a la práctica; revisar modelos posteriores (volatilidad rugosa, SVI sin arbitraje).
- **Origen:** Ficha de carga V2.3 re-verificada por DOC-M el 2026-11-02 (tanda 2); se normaliza al formato del encargo.

#### DOC-MOT-0328 · Q 80 (A) — More Than You Ever Wanted to Know About Volatility Swaps

- **Autores:** Kresimir Demeterfi; Emanuel Derman; Michael Kamal; Joseph Zou
- **Año:** 1999
- **Publicación o institución:** Goldman Sachs Quantitative Strategies Research Notes
- **Tipo de documento:** Informe técnico con metodología
- **Temática:** TM-06 Derivados y volatilidad implícita (principal) · secundarias: TM-03
- **Calidad Q:** 80 (A) — Tipo 15/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 7/10 · Acceso 7/10
- **DOI / ISBN / URL:** Sin DOI · Copia archivada: https://web.archive.org/web/20150906000344/http://elis.sigmath.es.osaka-u.ac.jp/research/gs-volatility_swaps.pdf
- **Acceso y licencia:** Copia gratuita archivada
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «VIX variance swap jump diffusion volatility risk premium implied volatility (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Variance swap», que reproduce la cita completa)
- **Contenido:** Réplica de swaps de varianza con una cartera de opciones ponderadas por 1/K² y contrato logarítmico; base del VIX moderno.
- **Uso en el Motor:** MC-09: varianza implícita sin modelo.
- **Limitaciones:** Nota de banco; supuestos de difusión continua.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0321 · Q 79 (B) — Riding on a Smile

- **Autores:** Emanuel Derman; Iraj Kani
- **Año:** 1994
- **Publicación o institución:** Risk, vol. 7, n.º 2 (febrero de 1994)
- **Tipo de documento:** Artículo en revista profesional
- **Temática:** TM-06 Derivados y volatilidad implícita (principal) · secundarias: TM-09
- **Calidad Q:** 79 (B) — Tipo 15/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 9/10 · Acceso 7/10
- **DOI / ISBN / URL:** Sin DOI · Copia de autor archivada: https://web.archive.org/web/20110710170610/http://www.ederman.com/new/docs/gs-volatility_smile.pdf
- **Acceso y licencia:** Copia gratuita archivada
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «local volatility Dupire SABR volatility model volatility smile variance swap (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Local volatility», que reproduce la cita completa)
- **Contenido:** Árbol binomial implícito calibrado a la sonrisa observada: versión discreta de la volatilidad local.
- **Uso en el Motor:** MC-09: árboles implícitos para exóticas.
- **Limitaciones:** Probabilidades negativas posibles en el árbol.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0058 · Q 76 (B) — Cboe Volatility Index (VIX) White Paper

- **Autores:** Cboe Global Markets (sin autor individual)
- **Año:** 2019
- **Publicación o institución:** Cboe (documento metodológico)
- **Tipo de documento:** Informe técnico con metodología
- **Temática:** TM-06 Derivados y volatilidad implícita (principal) · secundarias: —
- **Calidad Q:** 76 (B) — Tipo 15/25 · Rigor 14/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 7/10 · Acceso 9/10
- **DOI / ISBN / URL:** https://cdn.cboe.com/resources/vix/vixwhite.pdf
- **Acceso y licencia:** Acceso gratuito
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «VIX variance swap jump diffusion volatility risk premium implied volatility (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «VIX», que reproduce la cita completa)
- **Contenido:** Metodología oficial del VIX: varianza esperada a 30 días sin modelo a partir de una cartera ponderada de opciones fuera de dinero del S&P 500.
- **Uso en el Motor:** MC-09: cálculo de índices de volatilidad implícita sin modelo.
- **Limitaciones:** Documento del propio proveedor del índice.
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (tanda 2).

## TM-07 Modelos factoriales y carteras

#### DOC-MOT-0061 · Q 95 (A) — A Five-Factor Asset Pricing Model

- **Autores:** Eugene F. Fama; Kenneth R. French
- **Año:** 2015
- **Publicación o institución:** Journal of Financial Economics, vol. 116, n.º 1, págs. 1-22
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-07 Modelos factoriales y carteras (principal) · secundarias: —
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1016/j.jfineco.2014.10.010 · https://doi.org/10.1016%2Fj.jfineco.2014.10.010 · CiteSeerX: https://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.645.3745
- **Acceso y licencia:** Texto completo por suscripción en la editorial (Elsevier)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Fama–French three-factor model capital asset pricing model Black–Litterman arbitrage pricing theory (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Fama–French three-factor model», que reproduce la cita completa)
- **Contenido:** Amplía el modelo de tres factores con rentabilidad (RMW) e inversión (CMA); el factor valor resulta redundante en EE. UU.
- **Uso en el Motor:** MC-09: atribución de rentabilidades con cinco factores.
- **Limitaciones:** No incorpora momentum; evidencia centrada en EE. UU.
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (tanda 2).

#### DOC-MOT-0344 · Q 95 (A) — Betting Against Beta

- **Autores:** Andrea Frazzini; Lasse Heje Pedersen
- **Año:** 2014
- **Publicación o institución:** Journal of Financial Economics, vol. 111, n.º 1, págs. 1-25
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-07 Modelos factoriales y carteras (principal) · secundarias: TM-13
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 9/10 · Acceso 8/10
- **DOI / ISBN / URL:** Sin DOI visto · Copia del autor: http://pages.stern.nyu.edu/~lpederse/papers/BettingAgainstBeta.pdf
- **Acceso y licencia:** Copia gratuita del autor; revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «momentum investing Jegadeesh Titman time series momentum carry trade betting against beta low-volatility anomaly (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Low-volatility anomaly», que reproduce la cita completa)
- **Contenido:** Factor BAB (largo baja beta apalancada, corto alta beta) rentable en múltiples clases de activos, explicado por restricciones de financiación.
- **Uso en el Motor:** MC-09: factor baja beta.
- **Limitaciones:** Autores vinculados a gestora (AQR).
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0065 · Q 95 (A) — Value and Momentum Everywhere

- **Autores:** Clifford S. Asness; Tobias J. Moskowitz; Lasse Heje Pedersen
- **Año:** 2013
- **Publicación o institución:** The Journal of Finance, vol. 68, n.º 3, págs. 929-985
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-07 Modelos factoriales y carteras (principal) · secundarias: TM-13
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1111/jofi.12021 · https://onlinelibrary.wiley.com/doi/abs/10.1111/jofi.12021 · Repositorio: https://research.cbs.dk/en/publications/9cef71a9-adf5-4d83-925d-53c571dd0691
- **Acceso y licencia:** Texto completo por suscripción en la editorial (Wiley); registro en repositorio CBS
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «momentum investing Jegadeesh Titman time series momentum carry trade betting against beta low-volatility anomaly (dominio en.wikipedia.org)»; WebFetch: sí, páginas índice de Wikipedia «Factor investing» y «Momentum investing»)
- **Contenido:** Construye de forma homogénea factores valor y momentum en ocho mercados/clases de activo y documenta su correlación negativa y estructura factorial común.
- **Uso en el Motor:** MC-07, MC-09: factores valor y momentum multiactivo. Ficha de dominio en F7 (ANA-DOC-0003).
- **Limitaciones:** Costes de transacción no modelados en detalle.
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (tanda 2).

#### DOC-MOT-0070 · Q 95 (A) — Optimal Versus Naive Diversification: How Inefficient Is the 1/N Portfolio Strategy?

- **Autores:** Victor DeMiguel; Lorenzo Garlappi; Raman Uppal
- **Año:** 2009
- **Publicación o institución:** The Review of Financial Studies, vol. 22, n.º 5, págs. 1915-1953
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-07 Modelos factoriales y carteras (principal) · secundarias: —
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1093/rfs/hhm075 · https://doi.org/10.1093/rfs/hhm075
- **Acceso y licencia:** Texto completo por suscripción en la editorial (OUP)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «modern portfolio theory Black–Litterman model risk parity momentum investing hierarchical risk parity (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Hierarchical Risk Parity», que reproduce la cita completa)
- **Contenido:** Compara 14 modelos de optimización con la cartera 1/N fuera de muestra: ninguno la supera de forma consistente por el error de estimación.
- **Uso en el Motor:** MC-07: referencia ingenua 1/N y control del error de estimación.
- **Limitaciones:** Universos de pocos activos; horizonte de estimación determinante.
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (tanda 2).

#### DOC-MOT-0345 · Q 95 (A) — The Cross-Section of Volatility and Expected Returns

- **Autores:** Andrew Ang; Robert J. Hodrick; Yuhang Xing; Xiaoyan Zhang
- **Año:** 2006
- **Publicación o institución:** The Journal of Finance, vol. 61, n.º 1, págs. 259-299
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-07 Modelos factoriales y carteras (principal) · secundarias: TM-03
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI: 10.1111/j.1540-6261.2006.00836.x · NBER: http://www.nber.org/papers/w10852.pdf
- **Acceso y licencia:** NBER WP gratuito; revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «momentum investing Jegadeesh Titman time series momentum carry trade betting against beta low-volatility anomaly (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Low-volatility anomaly», que reproduce la cita completa)
- **Contenido:** La sensibilidad a la volatilidad agregada se remunera negativamente y las acciones con alta volatilidad idiosincrática rinden menos.
- **Uso en el Motor:** MC-09: factores de volatilidad.
- **Limitaciones:** Robustez discutida en la literatura posterior.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0068 · Q 95 (A) — A Well-Conditioned Estimator for Large-Dimensional Covariance Matrices

- **Autores:** Olivier Ledoit; Michael Wolf
- **Año:** 2004
- **Publicación o institución:** Journal of Multivariate Analysis, vol. 88, n.º 2, págs. 365-411
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-07 Modelos factoriales y carteras (principal) · secundarias: TM-01
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI no visto (se retira «10.1016/S0047-259X(03)00096-4 a verificar») · Copia del autor: http://www.econ.uzh.ch/faculty/wolf/publications/wellCond.pdf (archivada en https://web.archive.org/web/20141205062201/http://www.econ.uzh.ch/faculty/wolf/publications/wellCond.pdf)
- **Acceso y licencia:** Copia de autor gratuita (Universidad de Zúrich, archivada); editorial por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Ledoit Wolf shrinkage estimation of covariance matrices stationary bootstrap Politis Romano Fama–MacBeth regression (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Estimation of covariance matrices», que reproduce la cita completa)
- **Contenido:** Estimador de contracción lineal óptimo hacia la identidad escalada, bien condicionado aun cuando el número de variables supera al de observaciones.
- **Uso en el Motor:** MC-07: covarianzas estables para optimización.
- **Limitaciones:** Contracción lineal; superado en algunos usos por la contracción no lineal.
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (tanda 2).

#### DOC-MOT-0062 · Q 95 (A) — On Persistence in Mutual Fund Performance

- **Autores:** Mark M. Carhart
- **Año:** 1997
- **Publicación o institución:** The Journal of Finance, vol. 52, n.º 1, págs. 57-82
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-07 Modelos factoriales y carteras (principal) · secundarias: —
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1111/j.1540-6261.1997.tb03808.x · JSTOR: https://www.jstor.org/stable/2329556
- **Acceso y licencia:** Texto completo por suscripción en la editorial (Wiley/JSTOR)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Fama–French three-factor model capital asset pricing model Black–Litterman arbitrage pricing theory (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Fama–French three-factor model», que reproduce la cita completa y «Factor investing»)
- **Contenido:** Añade momentum al modelo de tres factores (modelo de cuatro factores) y muestra que la persistencia de fondos se explica por factores y costes.
- **Uso en el Motor:** MC-09: atribución con cuatro factores.
- **Limitaciones:** Muestra de fondos de EE. UU. 1962-1993.
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (tanda 2).

#### DOC-MOT-0060 · Q 95 (A) — Common Risk Factors in the Returns on Stocks and Bonds

- **Autores:** Eugene F. Fama; Kenneth R. French
- **Año:** 1993
- **Publicación o institución:** Journal of Financial Economics, vol. 33, n.º 1, págs. 3-56
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-07 Modelos factoriales y carteras (principal) · secundarias: —
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1016/0304-405X(93)90023-5 · https://doi.org/10.1016%2F0304-405X%2893%2990023-5 · CiteSeerX: https://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.139.5892
- **Acceso y licencia:** Texto completo por suscripción en la editorial (Elsevier); datos de factores en la biblioteca de K. French
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Fama–French three-factor model capital asset pricing model Black–Litterman arbitrage pricing theory (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Fama–French three-factor model», que reproduce la cita completa)
- **Contenido:** Modelo de tres factores (mercado, tamaño SMB, valor HML) y factores de plazo y crédito para bonos, estimados con regresiones de series temporales.
- **Uso en el Motor:** MC-09: modelo de tres factores para rentabilidad exigida y atribución.
- **Limitaciones:** Anomalías no explicadas (momentum, rentabilidad).
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (tanda 2).

#### DOC-MOT-0064 · Q 95 (A) — Returns to Buying Winners and Selling Losers: Implications for Stock Market Efficiency

- **Autores:** Narasimhan Jegadeesh; Sheridan Titman
- **Año:** 1993
- **Publicación o institución:** The Journal of Finance, vol. 48, n.º 1, págs. 65-91
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-07 Modelos factoriales y carteras (principal) · secundarias: —
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1111/j.1540-6261.1993.tb04702.x · JSTOR: 2328882 · https://onlinelibrary.wiley.com/doi/abs/10.1111/j.1540-6261.1993.tb04702.x
- **Acceso y licencia:** Texto completo por suscripción en la editorial (Wiley)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «momentum investing Jegadeesh Titman time series momentum carry trade betting against beta low-volatility anomaly (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Momentum investing», que reproduce la cita completa)
- **Contenido:** Documenta el momentum de sección cruzada con carteras de formación/tenencia de 3-12 meses y sus reversiones posteriores.
- **Uso en el Motor:** MC-07: metodología de carteras por ordenación. Ficha de dominio en F7 (ANA-DOC-0001).
- **Limitaciones:** Muestra 1965-1989; sensibilidad a costes.
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (tanda 2).

#### DOC-MOT-0338 · Q 95 (A) — A Test of the Efficiency of a Given Portfolio

- **Autores:** Michael R. Gibbons; Stephen A. Ross; Jay Shanken
- **Año:** 1989
- **Publicación o institución:** Econometrica, vol. 57, n.º 5, págs. 1121-1152
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-07 Modelos factoriales y carteras (principal) · secundarias: TM-04
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.2307/1913625 · JSTOR: https://www.jstor.org/stable/1913625 · CiteSeerX: https://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.557.1995
- **Acceso y licencia:** Texto completo por suscripción en la editorial (Econometric Society/JSTOR)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Fama–French three-factor model capital asset pricing model Black–Litterman arbitrage pricing theory (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Fama–French three-factor model», que reproduce la cita completa)
- **Contenido:** Contraste GRS de muestra finita de que las alfas de un conjunto de carteras son conjuntamente cero respecto a unos factores.
- **Uso en el Motor:** MC-09, MC-10: validación de modelos factoriales.
- **Limitaciones:** Supone normalidad.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0063 · Q 95 (A) — Risk, Return, and Equilibrium: Empirical Tests

- **Autores:** Eugene F. Fama; James D. MacBeth
- **Año:** 1973
- **Publicación o institución:** Journal of Political Economy, vol. 81, n.º 3, págs. 607-636
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-07 Modelos factoriales y carteras (principal) · secundarias: TM-04
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1086/260061 · JSTOR: https://www.jstor.org/stable/1831028 · CiteSeerX: https://citeseerx.ist.psu.edu/viewdoc/summary?doi=10.1.1.632.511
- **Acceso y licencia:** Texto completo por suscripción en la editorial (University of Chicago Press)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Ledoit Wolf shrinkage estimation of covariance matrices stationary bootstrap Politis Romano Fama–MacBeth regression (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Fama–MacBeth regression», que reproduce la cita completa)
- **Contenido:** Procedimiento en dos etapas: regresiones de sección cruzada periodo a periodo y promedio temporal de coeficientes para estimar primas de riesgo.
- **Uso en el Motor:** MC-09: primas de riesgo por sección cruzada.
- **Limitaciones:** Errores estándar sesgados con correlación persistente (véase Petersen 2009).
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (tanda 2).

#### DOC-MOT-0349 · Q 95 (A) — An Analytic Derivation of the Efficient Portfolio Frontier

- **Autores:** Robert C. Merton
- **Año:** 1972
- **Publicación o institución:** Journal of Financial and Quantitative Analysis, vol. 7, n.º 4, págs. 1851-1872
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-07 Modelos factoriales y carteras (principal) · secundarias: TM-09
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI: 10.2307/2329621 · JSTOR: 2329621 · Copia abierta: https://hdl.handle.net/1721.1%2F46832 (MIT)
- **Acceso y licencia:** Copia gratuita en MIT DSpace; revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «modern portfolio theory Black–Litterman model risk parity momentum investing hierarchical risk parity (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Modern portfolio theory», que reproduce la cita completa)
- **Contenido:** Derivación analítica cerrada de la frontera eficiente media-varianza y de sus propiedades.
- **Uso en el Motor:** MC-07: fórmulas cerradas de la frontera eficiente.
- **Limitaciones:** Sin restricciones de signo.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0347 · Q 94 (A) — Replicating Anomalies

- **Autores:** Kewei Hou; Chen Xue; Lu Zhang
- **Año:** 2020
- **Publicación o institución:** The Review of Financial Studies, vol. 33, n.º 5, págs. 2019-2133
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-07 Modelos factoriales y carteras (principal) · secundarias: TM-11
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1093/rfs/hhy131 · JSTOR: https://www.jstor.org/stable/48574457
- **Acceso y licencia:** Texto completo por suscripción en la editorial (OUP/JSTOR)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «momentum investing Jegadeesh Titman time series momentum carry trade betting against beta low-volatility anomaly (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Factor investing», que reproduce la cita completa)
- **Contenido:** Replica 452 anomalías con controles de microcapitalizaciones: la mayoría no resulta significativa.
- **Uso en el Motor:** MC-09, MC-10: selección de factores robustos.
- **Limitaciones:** Resultados dependientes del tratamiento de microcaps.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0066 · Q 94 (A) — Carry

- **Autores:** Ralph S. J. Koijen; Tobias J. Moskowitz; Lasse Heje Pedersen; Evert B. Vrugt
- **Año:** 2018
- **Publicación o institución:** Journal of Financial Economics, vol. 127, n.º 2, págs. 197-225 (versión previa: NBER Working Paper 19325, 2013)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-07 Modelos factoriales y carteras (principal) · secundarias: TM-13
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 9/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI del documento de trabajo: 10.3386/w19325 (el DOI de la revista no se ha visto; se retira «10.1016/j.jfineco.2017.11.002 a verificar») · https://ideas.repec.org/a/eee/jfinec/v127y2018i2p197-225.html · https://www.nber.org/papers/w19325
- **Acceso y licencia:** NBER WP de libre acceso; revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Koijen Moskowitz Pedersen Vrugt "Carry" Journal of Financial Economics 2018 127»; WebFetch: sí, ficha IDEAS de R. Koijen y página NBER w19325)
- **Contenido:** Define el carry de forma unificada para cualquier activo (rentabilidad esperada si el precio no cambia) y lo estudia en divisas, bonos, materias primas, índices y opciones.
- **Uso en el Motor:** MC-09: carry por clase de activo.
- **Limitaciones:** Carry sufre en crisis; definiciones dependen de la curva de futuros.
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (tanda 2).

#### DOC-MOT-0346 · Q 94 (A) — The Other Side of Value: The Gross Profitability Premium

- **Autores:** Robert Novy-Marx
- **Año:** 2013
- **Publicación o institución:** Journal of Financial Economics, vol. 108, n.º 1, págs. 1-28
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-07 Modelos factoriales y carteras (principal) · secundarias: —
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1016/j.jfineco.2013.01.003 · https://www.sciencedirect.com/science/article/pii/S0304405X13000044
- **Acceso y licencia:** Texto completo por suscripción en la editorial (Elsevier)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «momentum investing Jegadeesh Titman time series momentum carry trade betting against beta low-volatility anomaly (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Factor investing», que reproduce la cita completa)
- **Contenido:** La rentabilidad bruta sobre activos predice rendimientos con fuerza similar al valor y complementa las estrategias de valor.
- **Uso en el Motor:** MC-09: factor rentabilidad.
- **Limitaciones:** Medida contable; sensible a definiciones.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0340 · Q 94 (A) — The Capital Asset Pricing Model: Theory and Evidence

- **Autores:** Eugene F. Fama; Kenneth R. French
- **Año:** 2004
- **Publicación o institución:** Journal of Economic Perspectives, vol. 18, n.º 3, págs. 25-46
- **Tipo de documento:** Artículo de revisión revisado por pares
- **Temática:** TM-07 Modelos factoriales y carteras (principal) · secundarias: —
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 9/10 · Acceso 10/10
- **DOI / ISBN / URL:** DOI: 10.1257/0895330042162430 · https://www.aeaweb.org/articles?id=10.1257/0895330042162430
- **Acceso y licencia:** Acceso gratuito (AEA)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Fama–French three-factor model capital asset pricing model Black–Litterman arbitrage pricing theory (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Capital asset pricing model», que reproduce la cita completa)
- **Contenido:** Revisión de la teoría y de la evidencia empírica del CAPM, concluyendo que sus fallos invalidan su uso aplicado.
- **Uso en el Motor:** MC-09: justificación de modelos multifactoriales frente al CAPM.
- **Limitaciones:** Revisión de autores con postura conocida.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0336 · Q 94 (A) — The Cross-Section of Expected Stock Returns

- **Autores:** Eugene F. Fama; Kenneth R. French
- **Año:** 1992
- **Publicación o institución:** The Journal of Finance, vol. 47, n.º 2, págs. 427-465
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-07 Modelos factoriales y carteras (principal) · secundarias: —
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1111/j.1540-6261.1992.tb04398.x · JSTOR: https://www.jstor.org/stable/2329112
- **Acceso y licencia:** Texto completo por suscripción en la editorial (Wiley/JSTOR)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Fama–French three-factor model capital asset pricing model Black–Litterman arbitrage pricing theory (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Fama–French three-factor model», que reproduce la cita completa y «Capital asset pricing model»)
- **Contenido:** Muestra que tamaño y valor contable/mercado explican la sección cruzada de rentabilidades y la beta no.
- **Uso en el Motor:** MC-09: evidencia base de los factores tamaño y valor.
- **Limitaciones:** Acciones de EE. UU. 1963-1990.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0335 · Q 94 (A) — The Arbitrage Theory of Capital Asset Pricing

- **Autores:** Stephen A. Ross
- **Año:** 1976
- **Publicación o institución:** Journal of Economic Theory, vol. 13, n.º 3, págs. 341-360
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-07 Modelos factoriales y carteras (principal) · secundarias: —
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1016/0022-0531(76)90046-6 · https://doi.org/10.1016%2F0022-0531%2876%2990046-6
- **Acceso y licencia:** Texto completo por suscripción en la editorial (Elsevier)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Fama–French three-factor model capital asset pricing model Black–Litterman arbitrage pricing theory (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Arbitrage pricing theory», que reproduce la cita completa y «Factor investing»)
- **Contenido:** Teoría de valoración por arbitraje (APT): rentabilidades esperadas lineales en las exposiciones a factores comunes sin requerir la cartera de mercado.
- **Uso en el Motor:** MC-09: fundamento de los modelos multifactoriales.
- **Limitaciones:** No identifica los factores.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0071 · Q 93 (A) — Capital Asset Prices: A Theory of Market Equilibrium under Conditions of Risk

- **Autores:** William F. Sharpe
- **Año:** 1964
- **Publicación o institución:** The Journal of Finance, vol. 19, n.º 3, págs. 425-442
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-07 Modelos factoriales y carteras (principal) · secundarias: —
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1111/j.1540-6261.1964.tb02865.x · https://doi.org/10.1111%2Fj.1540-6261.1964.tb02865.x
- **Acceso y licencia:** Texto completo por suscripción en la editorial (Wiley)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Fama–French three-factor model capital asset pricing model Black–Litterman arbitrage pricing theory (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Capital asset pricing model», que reproduce la cita completa)
- **Contenido:** Formula el CAPM: en equilibrio la rentabilidad esperada es lineal en la beta respecto a la cartera de mercado.
- **Uso en el Motor:** MC-09: CAPM y beta como referencia de rentabilidad exigida.
- **Limitaciones:** Evidencia empírica débil (Fama-French 1992, 2004).
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (tanda 2).

#### DOC-MOT-0343 · Q 92 (A) — Honey, I Shrunk the Sample Covariance Matrix

- **Autores:** Olivier Ledoit; Michael Wolf
- **Año:** 2004
- **Publicación o institución:** The Journal of Portfolio Management, vol. 30, n.º 4, págs. 110-119
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-07 Modelos factoriales y carteras (principal) · secundarias: TM-01
- **Calidad Q:** 92 (A) — Tipo 22/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** Sin DOI visto · Copia del autor archivada: https://web.archive.org/web/20141205061842/http://www.econ.uzh.ch/faculty/ledoit/publications/honey.pdf
- **Acceso y licencia:** Copia gratuita archivada; revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Ledoit Wolf shrinkage estimation of covariance matrices stationary bootstrap Politis Romano Fama–MacBeth regression (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Estimation of covariance matrices», que reproduce la cita completa)
- **Contenido:** Contracción hacia la matriz de correlación constante para carteras de acciones, con fórmula de intensidad óptima.
- **Uso en el Motor:** MC-07: covarianzas para optimización de carteras.
- **Limitaciones:** Objetivo de contracción específico.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0348 · Q 92 (A) — Economic Forces and the Stock Market

- **Autores:** Nai-Fu Chen; Richard Roll; Stephen A. Ross
- **Año:** 1986
- **Publicación o institución:** The Journal of Business, vol. 59, n.º 3, págs. 383-403
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-07 Modelos factoriales y carteras (principal) · secundarias: TM-05
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1086/296344 · JSTOR: https://www.jstor.org/stable/2352710
- **Acceso y licencia:** Texto completo por suscripción en la editorial (University of Chicago Press/JSTOR)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Fama–French three-factor model capital asset pricing model Black–Litterman arbitrage pricing theory (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Arbitrage pricing theory», que reproduce la cita completa)
- **Contenido:** Modelo de factores macroeconómicos (producción, inflación, diferenciales de crédito y de plazo) valorados en la sección cruzada.
- **Uso en el Motor:** MC-09: factores macroeconómicos.
- **Limitaciones:** Estabilidad de primas discutida.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0337 · Q 92 (A) — The Valuation of Risk Assets and the Selection of Risky Investments in Stock Portfolios and Capital Budgets

- **Autores:** John Lintner
- **Año:** 1965
- **Publicación o institución:** Review of Economics and Statistics, vol. 47, n.º 1, págs. 13-37
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-07 Modelos factoriales y carteras (principal) · secundarias: TM-05
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.2307/1924119 · JSTOR: https://www.jstor.org/stable/1924119
- **Acceso y licencia:** Texto completo por suscripción en la editorial (MIT Press/JSTOR)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Fama–French three-factor model capital asset pricing model Black–Litterman arbitrage pricing theory (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Capital asset pricing model», que reproduce la cita completa y «Modern portfolio theory»)
- **Contenido:** Derivación independiente del CAPM con préstamo y endeudamiento libre de riesgo y aplicación a la presupuestación de capital.
- **Uso en el Motor:** MC-09: CAPM (formulación Sharpe-Lintner).
- **Limitaciones:** Supuestos de equilibrio estático.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0003 · Q 92 (A) — Portfolio Selection

- **Autores:** Harry M. Markowitz
- **Año:** 1952
- **Publicación o institución:** The Journal of Finance, vol. 7, n.º 1, págs. 77-91
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-07 Modelos factoriales y carteras (principal) · secundarias: —
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1111/j.1540-6261.1952.tb01525.x · JSTOR: 2975974 · https://doi.org/10.1111%2Fj.1540-6261.1952.tb01525.x
- **Acceso y licencia:** Texto completo por suscripción en la editorial (Wiley/JSTOR)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Fama–French three-factor model capital asset pricing model Black–Litterman arbitrage pricing theory (dominio en.wikipedia.org)» y «modern portfolio theory Black–Litterman model risk parity momentum investing hierarchical risk parity (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Capital asset pricing model», que reproduce la cita completa y «Modern portfolio theory»)
- **Contenido:** Formula la selección de carteras media-varianza y la frontera eficiente.
- **Uso en el Motor:** MC-07: optimización media-varianza.
- **Limitaciones:** Sensibilidad extrema a errores en medias y covarianzas.
- **Origen:** Ficha de carga V2.3 re-verificada por DOC-M el 2026-11-02 (tanda 2); se normaliza al formato del encargo.

#### DOC-MOT-0339 · Q 91 (A) — Capital Market Equilibrium with Restricted Borrowing

- **Autores:** Fischer Black
- **Año:** 1972
- **Publicación o institución:** The Journal of Business, vol. 45, n.º 3, págs. 444-455
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-07 Modelos factoriales y carteras (principal) · secundarias: —
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1086/295472 · https://doi.org/10.1086%2F295472
- **Acceso y licencia:** Texto completo por suscripción en la editorial (University of Chicago Press)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Fama–French three-factor model capital asset pricing model Black–Litterman arbitrage pricing theory (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Capital asset pricing model», que reproduce la cita completa y «Low-volatility anomaly»)
- **Contenido:** CAPM de beta cero: sin activo libre de riesgo la línea del mercado es más plana, anticipando la anomalía de baja beta.
- **Uso en el Motor:** MC-09: CAPM con restricciones de endeudamiento.
- **Limitaciones:** Modelo teórico.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0067 · Q 88 (A) — Global Portfolio Optimization

- **Autores:** Fischer Black; Robert Litterman
- **Año:** 1992
- **Publicación o institución:** Financial Analysts Journal, vol. 48, n.º 5, págs. 28-43
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-07 Modelos factoriales y carteras (principal) · secundarias: —
- **Calidad Q:** 88 (A) — Tipo 24/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 9/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.2469/faj.v48.n5.28 · https://www.tandfonline.com/doi/abs/10.2469/faj.v48.n5.28
- **Acceso y licencia:** Texto completo por suscripción en la editorial (Taylor & Francis)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «modern portfolio theory Black–Litterman model risk parity momentum investing hierarchical risk parity (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Black–Litterman model», que reproduce la cita completa)
- **Contenido:** Combina rentabilidades de equilibrio implícitas con opiniones del inversor ponderadas por su confianza, produciendo carteras estables.
- **Uso en el Motor:** MC-07: modelo Black-Litterman.
- **Limitaciones:** Elección subjetiva de τ y de la confianza en opiniones.
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (tanda 2).

#### DOC-MOT-0341 · Q 88 (A) — Asset Allocation: Combining Investor Views with Market Equilibrium

- **Autores:** Fischer Black; Robert B. Litterman
- **Año:** 1991
- **Publicación o institución:** The Journal of Fixed Income, vol. 1, n.º 2, págs. 7-18
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-07 Modelos factoriales y carteras (principal) · secundarias: —
- **Calidad Q:** 88 (A) — Tipo 24/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 9/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.3905/JFI.1991.408013 · https://www.pm-research.com/content/iijfixinc/1/2/7
- **Acceso y licencia:** Texto completo por suscripción en la editorial (PM Research)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «modern portfolio theory Black–Litterman model risk parity momentum investing hierarchical risk parity (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Black–Litterman model», que reproduce la cita completa)
- **Contenido:** Primera exposición del modelo Black-Litterman aplicado a asignación global de bonos y divisas.
- **Uso en el Motor:** MC-07: base del modelo Black-Litterman.
- **Limitaciones:** Exposición original menos detallada que 1992.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0342 · Q 85 (A) — The Intuition Behind Black-Litterman Model Portfolios

- **Autores:** Guangliang He; Robert Litterman
- **Año:** 2002
- **Publicación o institución:** SSRN Working Paper 334304 (Goldman Sachs)
- **Tipo de documento:** Documento de trabajo
- **Temática:** TM-07 Modelos factoriales y carteras (principal) · secundarias: —
- **Calidad Q:** 85 (A) — Tipo 20/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 7/10 · Acceso 9/10
- **DOI / ISBN / URL:** DOI: 10.2139/ssrn.334304 · https://papers.ssrn.com/sol3/papers.cfm?abstract_id=334304
- **Acceso y licencia:** Acceso gratuito (SSRN)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «modern portfolio theory Black–Litterman model risk parity momentum investing hierarchical risk parity (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Black–Litterman model», que reproduce la cita completa)
- **Contenido:** Desarrollo detallado e intuición de las carteras Black-Litterman: cómo las opiniones desplazan los pesos respecto al equilibrio.
- **Uso en el Motor:** MC-07: implementación de Black-Litterman.
- **Limitaciones:** Documento de practicantes de un banco.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0069 · Q 84 (A) — Building Diversified Portfolios that Outperform Out of Sample

- **Autores:** Marcos López de Prado
- **Año:** 2016
- **Publicación o institución:** The Journal of Portfolio Management, vol. 42, n.º 4, págs. 59-69
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-07 Modelos factoriales y carteras (principal) · secundarias: TM-10
- **Calidad Q:** 84 (A) — Tipo 22/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 9/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.3905/jpm.2016.42.4.059 · https://www.pm-research.com/content/iijpormgmt/42/4/59
- **Acceso y licencia:** Texto completo por suscripción en la editorial (PM Research)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «modern portfolio theory Black–Litterman model risk parity momentum investing hierarchical risk parity (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Hierarchical Risk Parity», que reproduce la cita completa)
- **Contenido:** Propone la paridad de riesgo jerárquica (HRP): agrupamiento jerárquico, cuasi-diagonalización y bisección recursiva sin invertir la covarianza.
- **Uso en el Motor:** MC-07: asignación HRP.
- **Limitaciones:** Evidencia principalmente por simulación; revista profesional.
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (tanda 2).

## TM-08 Riesgo y valores extremos

#### DOC-MOT-0350 · Q 97 (A) — On the Coherence of Expected Shortfall

- **Autores:** Carlo Acerbi; Dirk Tasche
- **Año:** 2002
- **Publicación o institución:** Journal of Banking & Finance, vol. 26, n.º 7, págs. 1487-1503
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-08 Riesgo y valores extremos (principal) · secundarias: —
- **Calidad Q:** 97 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** DOI: 10.1016/S0378-4266(02)00283-2 · arXiv: https://arxiv.org/abs/cond-mat/0104295
- **Acceso y licencia:** Preprint gratuito en arXiv; revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «expected shortfall coherent risk measure value at risk backtesting extreme value theory (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Expected shortfall», que reproduce la cita completa)
- **Contenido:** Define el ES de forma que sea coherente para cualquier distribución (incluidas discretas) y lo relaciona con el CVaR.
- **Uso en el Motor:** MC-07: definición correcta del ES.
- **Limitaciones:** Teórico.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0074 · Q 96 (A) — Estimation of Tail-Related Risk Measures for Heteroscedastic Financial Time Series: An Extreme Value Approach

- **Autores:** Alexander J. McNeil; Rüdiger Frey
- **Año:** 2000
- **Publicación o institución:** Journal of Empirical Finance, vol. 7, n.º 3-4, págs. 271-300
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-08 Riesgo y valores extremos (principal) · secundarias: TM-03
- **Calidad Q:** 96 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI: 10.1016/S0927-5398(00)00012-8 · https://research.wu.ac.at/de/publications/estimation-of-tail-related-risk-measures-for-heteroscedastic-fina-3/ · PDF: https://www.wu.ac.at/fileadmin/wu/d/i/statmath/Publications/Publications_Frey/Journal_Papers/evt-garch.pdf
- **Acceso y licencia:** Copia institucional gratuita (WU Viena); revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «McNeil Frey 2000 "Estimation of tail-related risk measures for heteroscedastic financial time series" Journal of Empirical Finance»; WebFetch: sí, portal de investigación de la WU)
- **Contenido:** Método en dos etapas: GARCH por pseudo-máxima verosimilitud y teoría de valores extremos (GPD) sobre los residuos para VaR y ES condicionales.
- **Uso en el Motor:** MC-07: VaR/ES condicional GARCH-EVT.
- **Limitaciones:** Supone residuos i.i.d.; umbral de la GPD a elegir.
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (tanda 2).

#### DOC-MOT-0075 · Q 96 (A) — Coherent Measures of Risk

- **Autores:** Philippe Artzner; Freddy Delbaen; Jean-Marc Eber; David Heath
- **Año:** 1999
- **Publicación o institución:** Mathematical Finance, vol. 9, n.º 3, págs. 203-228
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-08 Riesgo y valores extremos (principal) · secundarias: —
- **Calidad Q:** 96 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI: 10.1111/1467-9965.00068 · https://onlinelibrary.wiley.com/doi/10.1111/1467-9965.00068 · Preprint: http://www.math.ethz.ch/~delbaen/ftp/preprints/CoherentMF.pdf
- **Acceso y licencia:** Preprint gratuito (ETH Zúrich); revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «expected shortfall coherent risk measure value at risk backtesting extreme value theory (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Expected shortfall», que reproduce la cita completa, «Value at risk» y «Coherent risk measure»)
- **Contenido:** Axiomas de coherencia (monotonía, subaditividad, homogeneidad, invariancia por traslación); el VaR no es subaditivo en general.
- **Uso en el Motor:** MC-07: fundamento de la elección del ES frente al VaR.
- **Limitaciones:** Teoría estática; no trata elicitabilidad ni dinámica.
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (tanda 2).

#### DOC-MOT-0354 · Q 95 (A) — Explanatory Note on the Minimum Capital Requirements for Market Risk

- **Autores:** Basel Committee on Banking Supervision
- **Año:** 2019
- **Publicación o institución:** Bank for International Settlements (enero de 2019)
- **Tipo de documento:** Informe técnico con metodología (organismo oficial)
- **Temática:** TM-08 Riesgo y valores extremos (principal) · secundarias: TM-11
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://www.bis.org/bcbs/publ/d457_note.pdf
- **Acceso y licencia:** Acceso gratuito (BPI)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «expected shortfall coherent risk measure value at risk backtesting extreme value theory (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Value at risk», que reproduce la cita completa)
- **Contenido:** Explica el marco revisado de riesgo de mercado (FRTB): sustitución del VaR por ES al 97,5 %, horizontes de liquidez y pruebas de backtesting y atribución de P&L.
- **Uso en el Motor:** MC-07, MC-10: estándar regulatorio de ES y backtesting.
- **Limitaciones:** Marco regulatorio bancario; no es metodología estadística general.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0364 · Q 95 (A) — Convex Measures of Risk and Trading Constraints

- **Autores:** Hans Föllmer; Alexander Schied
- **Año:** 2002
- **Publicación o institución:** Finance and Stochastics, vol. 6, n.º 4, págs. 429-447
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-08 Riesgo y valores extremos (principal) · secundarias: —
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI: 10.1007/s007800200072 · Copia abierta: http://edoc.hu-berlin.de/18452/4274
- **Acceso y licencia:** Copia gratuita (HU Berlín); revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «expected shortfall coherent risk measure value at risk backtesting extreme value theory (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Coherent risk measure», que reproduce la cita completa)
- **Contenido:** Generaliza las medidas coherentes a medidas convexas de riesgo y su representación dual.
- **Uso en el Motor:** MC-07: medidas de riesgo con liquidez/restricciones.
- **Limitaciones:** Teórico.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0358 · Q 95 (A) — Statistical Inference Using Extreme Order Statistics

- **Autores:** James Pickands III
- **Año:** 1975
- **Publicación o institución:** The Annals of Statistics, vol. 3, n.º 1, págs. 119-131
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-08 Riesgo y valores extremos (principal) · secundarias: TM-01
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** DOI: 10.1214/aos/1176343003 · https://projecteuclid.org/journals/annals-of-statistics/volume-3/issue-1/Statistical-Inference-Using-Extreme-Order-Statistics/10.1214/aos/1176343003.full
- **Acceso y licencia:** Acceso gratuito en Project Euclid
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «generalized Pareto distribution extreme value theory Hill estimator copula CoVaR systemic risk (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Pickands–Balkema–De Haan theorem», que reproduce la cita completa y «Extreme value theory»)
- **Contenido:** Establece que los excesos sobre umbrales altos siguen aproximadamente una distribución de Pareto generalizada y propone el estimador de Pickands.
- **Uso en el Motor:** MC-07: fundamento del método POT.
- **Limitaciones:** Estimador de Pickands de alta varianza.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0359 · Q 95 (A) — Residual Life Time at Great Age

- **Autores:** A. A. Balkema; L. de Haan
- **Año:** 1974
- **Publicación o institución:** The Annals of Probability, vol. 2, n.º 5, págs. 792-804
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-08 Riesgo y valores extremos (principal) · secundarias: TM-01
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** DOI: 10.1214/aop/1176996548 · https://projecteuclid.org/journals/annals-of-probability/volume-2/issue-5/Residual-Life-Time-at-Great-Age/10.1214/aop/1176996548.full
- **Acceso y licencia:** Acceso gratuito en Project Euclid
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «generalized Pareto distribution extreme value theory Hill estimator copula CoVaR systemic risk (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Pickands–Balkema–De Haan theorem», que reproduce la cita completa)
- **Contenido:** Resultado límite para la distribución de excesos sobre umbral (teorema de Pickands-Balkema-de Haan).
- **Uso en el Motor:** MC-07: base teórica de la GPD.
- **Limitaciones:** Teórico.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0356 · Q 94 (A) — CoVaR

- **Autores:** Tobias Adrian; Markus K. Brunnermeier
- **Año:** 2016
- **Publicación o institución:** American Economic Review, vol. 106, n.º 7, págs. 1705-1741
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-08 Riesgo y valores extremos (principal) · secundarias: TM-04
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1257/aer.20120555 · https://doi.org/10.1257/aer.20120555
- **Acceso y licencia:** Texto completo por suscripción en la editorial (AEA)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «generalized Pareto distribution extreme value theory Hill estimator copula CoVaR systemic risk (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Markus Brunnermeier»)
- **Contenido:** Mide el riesgo sistémico como el VaR del sistema condicionado a que una institución esté en dificultades (ΔCoVaR), estimado por regresión cuantílica.
- **Uso en el Motor:** MC-07: contagio y riesgo sistémico.
- **Limitaciones:** Requiere datos de mercado de las entidades.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0365 · Q 94 (A) — Asset Market Linkages in Crisis Periods

- **Autores:** Philipp Hartmann; Stefan Straetmans; Casper G. de Vries
- **Año:** 2004
- **Publicación o institución:** Review of Economics and Statistics, vol. 86, n.º 1, págs. 313-326
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-08 Riesgo y valores extremos (principal) · secundarias: TM-07
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI: 10.1162/003465304323023831 · Repositorio: http://repository.tue.nl/548705 · https://hdl.handle.net/10419%2F152505
- **Acceso y licencia:** Copias gratuitas (TU Eindhoven, EconStor); revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «generalized Pareto distribution extreme value theory Hill estimator copula CoVaR systemic risk (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Tail dependence», que reproduce la cita completa)
- **Contenido:** Mide la dependencia de colas entre acciones y bonos del G-5 con EVT multivariante: contagio y huida hacia la calidad.
- **Uso en el Motor:** MC-07: dependencia extrema entre clases de activos.
- **Limitaciones:** Muestra hasta finales de los 90.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0073 · Q 94 (A) — Evaluating Interval Forecasts

- **Autores:** Peter F. Christoffersen
- **Año:** 1998
- **Publicación o institución:** International Economic Review, vol. 39, n.º 4, págs. 841-862
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-08 Riesgo y valores extremos (principal) · secundarias: TM-11
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.2307/2527341 · JSTOR: 2527341
- **Acceso y licencia:** Texto completo por suscripción en la editorial (Wiley/JSTOR)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «expected shortfall coherent risk measure value at risk backtesting extreme value theory (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Value at risk», que reproduce la cita completa)
- **Contenido:** Contrastes de razón de verosimilitud de cobertura incondicional, independencia y cobertura condicional de las excepciones de intervalos/VaR.
- **Uso en el Motor:** MC-07, MC-10: backtesting de VaR.
- **Limitaciones:** Baja potencia con pocas excepciones.
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (tanda 2).

#### DOC-MOT-0353 · Q 93 (A) — Value-at-Risk Prediction: A Comparison of Alternative Strategies

- **Autores:** Keith Kuester; Stefan Mittnik; Marc S. Paolella
- **Año:** 2006
- **Publicación o institución:** Journal of Financial Econometrics, vol. 4, págs. 53-89
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-08 Riesgo y valores extremos (principal) · secundarias: TM-11
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1093/jjfinec/nbj002 · https://doi.org/10.1093%2Fjjfinec%2Fnbj002
- **Acceso y licencia:** Texto completo por suscripción en la editorial (OUP)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «expected shortfall coherent risk measure value at risk backtesting extreme value theory (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Value at risk», que reproduce la cita completa)
- **Contenido:** Compara fuera de muestra métodos de VaR (histórico, GARCH con distintas colas, EVT, CAViaR): destacan los híbridos GARCH-EVT y de colas asimétricas.
- **Uso en el Motor:** MC-07: elección del método de VaR.
- **Limitaciones:** Un solo índice (Nasdaq).
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0352 · Q 93 (A) — Backtesting Value-at-Risk: A Duration-Based Approach

- **Autores:** Peter Christoffersen; Denis Pelletier
- **Año:** 2004
- **Publicación o institución:** Journal of Financial Econometrics, vol. 2, págs. 84-108
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-08 Riesgo y valores extremos (principal) · secundarias: TM-11
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1093/jjfinec/nbh004
- **Acceso y licencia:** Texto completo por suscripción en la editorial (OUP)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «expected shortfall coherent risk measure value at risk backtesting extreme value theory (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Value at risk», que reproduce la cita completa)
- **Contenido:** Contrastes de independencia de excepciones basados en la duración entre violaciones del VaR, más potentes ante agrupamientos.
- **Uso en el Motor:** MC-07, MC-10: backtesting de VaR por duraciones.
- **Limitaciones:** Potencia limitada en muestras cortas.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0351 · Q 93 (A) — Expected Shortfall: A Natural Coherent Alternative to Value at Risk

- **Autores:** Carlo Acerbi; Dirk Tasche
- **Año:** 2002
- **Publicación o institución:** Economic Notes, vol. 31, n.º 2, págs. 379-388
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-08 Riesgo y valores extremos (principal) · secundarias: —
- **Calidad Q:** 93 (A) — Tipo 24/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** DOI: 10.1111/1468-0300.00091 · Copia: http://www.bis.org/bcbs/ca/acertasc.pdf · arXiv: cond-mat/0105191
- **Acceso y licencia:** Copia gratuita en el BPI y arXiv
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «expected shortfall coherent risk measure value at risk backtesting extreme value theory (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Expected shortfall», que reproduce la cita completa)
- **Contenido:** Exposición divulgativa-técnica del ES como alternativa coherente al VaR y su estimador empírico.
- **Uso en el Motor:** MC-07: justificación operativa del ES.
- **Limitaciones:** Solapa parcialmente con DOC-MOT-0350.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0076 · Q 93 (A) — Optimization of Conditional Value-at-Risk

- **Autores:** R. Tyrrell Rockafellar; Stanislav Uryasev
- **Año:** 2000
- **Publicación o institución:** Journal of Risk, vol. 2, n.º 3, págs. 21-41
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-08 Riesgo y valores extremos (principal) · secundarias: TM-07
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI: 10.21314/JOR.2000.038 · PDF de los autores: https://sites.math.washington.edu/~rtr/papers/rtr179-CVaR1.pdf
- **Acceso y licencia:** Copia gratuita de los autores; revista por suscripción (Risk.net)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «expected shortfall coherent risk measure value at risk backtesting extreme value theory (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Expected shortfall», que reproduce la cita completa)
- **Contenido:** Formulación del CVaR como problema de minimización auxiliar que con escenarios se resuelve por programación lineal, obteniendo a la vez VaR y CVaR.
- **Uso en el Motor:** MC-07: optimización de carteras por CVaR.
- **Limitaciones:** Supone distribuciones continuas (generalizado en 2002). Wikipedia indica págs. 21-42.
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (tanda 2).

#### DOC-MOT-0363 · Q 93 (A) — Models for Exceedances over High Thresholds

- **Autores:** A. C. Davison; R. L. Smith
- **Año:** 1990
- **Publicación o institución:** Journal of the Royal Statistical Society, Series B, vol. 52, n.º 3, págs. 393-425
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-08 Riesgo y valores extremos (principal) · secundarias: TM-01
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1111/j.2517-6161.1990.tb01796.x · https://rss.onlinelibrary.wiley.com/doi/10.1111/j.2517-6161.1990.tb01796.x
- **Acceso y licencia:** Texto completo por suscripción en la editorial (Wiley/RSS)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «generalized Pareto distribution extreme value theory Hill estimator copula CoVaR systemic risk (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Extreme value theory», que reproduce la cita completa)
- **Contenido:** Desarrolla el método de picos sobre umbral (POT) con GPD, regresión y diagnósticos.
- **Uso en el Motor:** MC-07: ajuste GPD y diagnóstico de umbral.
- **Limitaciones:** Datos no financieros.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0355 · Q 93 (A) — Basel Framework MAR32: Internal Models Approach — Backtesting and P&L Attribution Test Requirements

- **Autores:** Basel Committee on Banking Supervision / Bank for International Settlements
- **Año:** Publicación continua (consolidada)
- **Publicación o institución:** Bank for International Settlements, Basel Framework, capítulo MAR32
- **Tipo de documento:** Norma técnica de organismo oficial
- **Temática:** TM-08 Riesgo y valores extremos (principal) · secundarias: TM-11
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 14/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://www.bis.org/basel_framework/chapter/MAR/32.htm
- **Acceso y licencia:** Acceso gratuito (BPI)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «expected shortfall coherent risk measure value at risk backtesting extreme value theory (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Value at risk», que reproduce la cita completa)
- **Contenido:** Requisitos regulatorios de backtesting del VaR (zonas de semáforo por número de excepciones) y test de atribución de P&L.
- **Uso en el Motor:** MC-10: umbrales de excepciones de referencia.
- **Limitaciones:** Texto normativo vivo; citar la versión consultada.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0367 · Q 91 (A) — Analytical Value-at-Risk with Jumps and Stochastic Volatility

- **Autores:** Darrell Duffie; Jun Pan
- **Año:** 2001
- **Publicación o institución:** Finance and Stochastics, vol. 5, n.º 2, págs. 155-180
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-08 Riesgo y valores extremos (principal) · secundarias: TM-06
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1007/PL00013592 · https://doi.org/10.1007%2FPL00013592
- **Acceso y licencia:** Texto completo por suscripción en la editorial (Springer)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «VIX variance swap jump diffusion volatility risk premium implied volatility (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Stochastic volatility jump models», que reproduce la cita completa)
- **Contenido:** VaR analítico de carteras con opciones bajo saltos y volatilidad estocástica mediante transformadas afines.
- **Uso en el Motor:** MC-07: VaR de carteras no lineales.
- **Limitaciones:** Requiere modelo afín.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0360 · Q 91 (A) — A Simple General Approach to Inference about the Tail of a Distribution

- **Autores:** Bruce M. Hill
- **Año:** 1975
- **Publicación o institución:** The Annals of Statistics, vol. 3, págs. 1163-1174
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-08 Riesgo y valores extremos (principal) · secundarias: TM-01
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** DOI no visto · Cita en https://en.wikipedia.org/wiki/Heavy-tailed_distribution
- **Acceso y licencia:** No determinado (no se ha localizado copia ni página editorial en esta pasada)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «generalized Pareto distribution extreme value theory Hill estimator copula CoVaR systemic risk (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Heavy-tailed distribution», que reproduce la cita completa)
- **Contenido:** Estimador de Hill del índice de cola para distribuciones de tipo Pareto a partir de los estadísticos de orden superiores.
- **Uso en el Motor:** MC-07: índice de cola de rendimientos.
- **Limitaciones:** Sensible al número de estadísticos de orden. Alerta: REPARAR (localizar DOI/URL).
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0361 · Q 91 (A) — Limiting Forms of the Frequency Distribution of the Largest or Smallest Member of a Sample

- **Autores:** R. A. Fisher; L. H. C. Tippett
- **Año:** 1928
- **Publicación o institución:** Proceedings of the Cambridge Philosophical Society, vol. 24, n.º 2, págs. 180-190
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-08 Riesgo y valores extremos (principal) · secundarias: TM-01
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1017/s0305004100015681 · https://doi.org/10.1017%2Fs0305004100015681
- **Acceso y licencia:** Texto completo por suscripción en la editorial (Cambridge University Press)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «generalized Pareto distribution extreme value theory Hill estimator copula CoVaR systemic risk (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Extreme value theory», que reproduce la cita completa)
- **Contenido:** Identifica las tres formas límite de la distribución del máximo (Gumbel, Fréchet, Weibull), origen de la GEV.
- **Uso en el Motor:** MC-07: fundamento de máximos por bloques.
- **Limitaciones:** Histórico.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0357 · Q 90 (A) — CISS – A Composite Indicator of Systemic Stress in the Financial System

- **Autores:** Dániel Holló; Manfred Kremer; Marco Lo Duca
- **Año:** 2012
- **Publicación o institución:** European Central Bank, Working Paper Series n.º 1426 (marzo de 2012)
- **Tipo de documento:** Documento de trabajo (banco central)
- **Temática:** TM-08 Riesgo y valores extremos (principal) · secundarias: TM-03
- **Calidad Q:** 90 (A) — Tipo 20/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** https://ECB.eu/pub/pdf/scpwps/ecbwp1426.pdf (redirige a ecb.europa.eu) · Perfil BCE: https://www.ecb.europa.eu/pub/research/authors/profiles/daniel-hollo.en.html
- **Acceso y licencia:** Acceso gratuito (BCE)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Holló Kremer Lo Duca "CISS – a composite indicator of systemic stress in the financial system" ECB Working Paper 1426»; WebFetch: sí, perfil de autor del BCE (el PDF redirige al dominio del BCE))
- **Contenido:** Indicador compuesto de estrés sistémico que agrega subíndices de mercados con ponderación por correlaciones cambiantes (enfoque de cartera).
- **Uso en el Motor:** MC-07: indicador europeo de estrés para escenarios de riesgo.
- **Limitaciones:** Construcción específica de la zona del euro.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0077 · Q 89 (A) — Quantitative Risk Management: Concepts, Techniques and Tools (ed. revisada)

- **Autores:** Alexander J. McNeil; Rüdiger Frey; Paul Embrechts
- **Año:** 2015
- **Publicación o institución:** Princeton University Press (Princeton Series in Finance)
- **Tipo de documento:** Manual de referencia
- **Temática:** TM-08 Riesgo y valores extremos (principal) · secundarias: TM-03
- **Calidad Q:** 89 (A) — Tipo 20/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** ISBN: 978-0-691-16627-8 · https://econpapers.repec.org/RePEc:pup:chapts:10496-1
- **Acceso y licencia:** De pago; capítulos introductorios con ficha en RePEc
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «McNeil Frey Embrechts "Quantitative Risk Management" revised edition 2015 Princeton University Press»; WebFetch: sí, ficha EconPapers del prefacio)
- **Contenido:** Manual integral de riesgo cuantitativo: medidas de riesgo, modelos de series, valores extremos, cópulas, riesgo de crédito y operacional, backtesting.
- **Uso en el Motor:** MC-07: referencia integral de riesgo.
- **Limitaciones:** Extenso; requiere base de probabilidad.
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (tanda 2).

#### DOC-MOT-0362 · Q 88 (A) — An Introduction to Statistical Modeling of Extreme Values

- **Autores:** Stuart Coles
- **Año:** 2001
- **Publicación o institución:** Springer (Springer Series in Statistics)
- **Tipo de documento:** Manual de referencia
- **Temática:** TM-08 Riesgo y valores extremos (principal) · secundarias: TM-01
- **Calidad Q:** 88 (A) — Tipo 20/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.1007/978-1-4471-3675-0 · ISBN: 978-1-84996-874-4
- **Acceso y licencia:** De pago (Springer)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «generalized Pareto distribution extreme value theory Hill estimator copula CoVaR systemic risk (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Extreme value theory», que reproduce la cita completa)
- **Contenido:** Manual aplicado de valores extremos: GEV, GPD/POT, procesos puntuales, no estacionariedad y extremos multivariantes, con inferencia por verosimilitud.
- **Uso en el Motor:** MC-07: implementación de modelos EVT.
- **Limitaciones:** Ejemplos ambientales más que financieros.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0072 · Q 88 (A) — Techniques for Verifying the Accuracy of Risk Measurement Models

- **Autores:** Paul H. Kupiec
- **Año:** 1995
- **Publicación o institución:** Board of Governors of the Federal Reserve System, Finance and Economics Discussion Series 95-24
- **Tipo de documento:** Documento de trabajo
- **Temática:** TM-08 Riesgo y valores extremos (principal) · secundarias: TM-11
- **Calidad Q:** 88 (A) — Tipo 20/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** Sin DOI visto · https://ideas.repec.org/f/pku379.html (registro del autor; ítem 95-24)
- **Acceso y licencia:** Acceso gratuito (serie FEDS)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Kupiec 1995 "Techniques for verifying the accuracy of risk measurement models" Journal of Derivatives»; WebFetch: sí, página de autor en IDEAS/RePEc)
- **Contenido:** Contraste de proporción de fallos (POF) de cobertura incondicional del VaR y análisis de su baja potencia con muestras cortas.
- **Uso en el Motor:** MC-07, MC-10: contraste de Kupiec.
- **Limitaciones:** Corrección: se cita la versión FEDS confirmada; la versión en The Journal of Derivatives 3(2) de la semilla no se ha podido confirmar.
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (tanda 2).

#### DOC-MOT-0078 · Q 87 (A) — Modelling Extremal Events for Insurance and Finance

- **Autores:** Paul Embrechts; Claudia Klüppelberg; Thomas Mikosch
- **Año:** 1997
- **Publicación o institución:** Springer (Stochastic Modelling and Applied Probability, vol. 33)
- **Tipo de documento:** Libro académico
- **Temática:** TM-08 Riesgo y valores extremos (principal) · secundarias: —
- **Calidad Q:** 87 (A) — Tipo 20/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.1007/978-3-642-33483-2 · ISBN: 978-3-642-08242-9 · Cita en https://en.wikipedia.org/wiki/Heavy-tailed_distribution
- **Acceso y licencia:** De pago (Springer)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «generalized Pareto distribution extreme value theory Hill estimator copula CoVaR systemic risk (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Heavy-tailed distribution», que reproduce la cita completa y «Extreme value theory»)
- **Contenido:** Tratado de valores extremos: GEV, GPD, estimadores de cola (Hill), distribuciones subexponenciales y aplicaciones actuariales y financieras.
- **Uso en el Motor:** MC-07: teoría de valores extremos.
- **Limitaciones:** Alto nivel matemático.
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (tanda 2).

#### DOC-MOT-0366 · Q 83 (A) — Value at Risk: The New Benchmark for Managing Financial Risk (3.ª ed.)

- **Autores:** Philippe Jorion
- **Año:** 2006
- **Publicación o institución:** McGraw-Hill
- **Tipo de documento:** Manual de referencia
- **Temática:** TM-08 Riesgo y valores extremos (principal) · secundarias: TM-11
- **Calidad Q:** 83 (A) — Tipo 20/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** ISBN: 978-0-07-146495-6 · Cita en https://en.wikipedia.org/wiki/Value_at_risk
- **Acceso y licencia:** De pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «expected shortfall coherent risk measure value at risk backtesting extreme value theory (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Value at risk», que reproduce la cita completa)
- **Contenido:** Manual profesional del VaR: métodos de cálculo, backtesting, pruebas de estrés y uso regulatorio.
- **Uso en el Motor:** MC-07: referencia operativa del VaR.
- **Limitaciones:** Previo a FRTB y al ES regulatorio.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0079 · Q 80 (A) — Backtesting Expected Shortfall

- **Autores:** Carlo Acerbi; Balázs Székely
- **Año:** 2014
- **Publicación o institución:** MSCI Inc. (documento de investigación, diciembre de 2014; borrador de 27/10/2014)
- **Tipo de documento:** Informe técnico con metodología
- **Temática:** TM-08 Riesgo y valores extremos (principal) · secundarias: TM-11
- **Calidad Q:** 80 (A) — Tipo 15/25 · Rigor 16/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 8/10 · Acceso 9/10
- **DOI / ISBN / URL:** Sin DOI · https://www.msci.com/documents/10199/22aa9922-f874-4060-b77a-0f0e267a489b
- **Acceso y licencia:** Acceso gratuito (MSCI)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Acerbi Szekely "Backtesting Expected Shortfall" 2014 Risk MSCI»; WebFetch: sí, documento MSCI)
- **Contenido:** Tres contrastes no paramétricos para backtesting del ES (magnitud de excepciones, contraste directo de cola y contraste por rangos).
- **Uso en el Motor:** MC-10: backtesting del ES.
- **Limitaciones:** Autores vinculados a proveedor comercial; la versión en la revista Risk no se ha confirmado.
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (tanda 2).

## TM-09 Simulación y métodos numéricos

#### DOC-MOT-0013 · Q 98 (A) — NIST Digital Library of Mathematical Functions (edición electrónica del NIST Handbook of Mathematical Functions)

- **Autores:** Frank W. J. Olver; Daniel W. Lozier; Ronald F. Boisvert; Charles W. Clark (eds.)
- **Año:** 2010 (lanzamiento; edición en línea continua)
- **Publicación o institución:** National Institute of Standards and Technology (NIST); edición impresa: Cambridge University Press
- **Tipo de documento:** Manual de referencia (organismo oficial)
- **Temática:** TM-09 Simulación y métodos numéricos (principal) · secundarias: TM-01
- **Calidad Q:** 98 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** ISBN impreso: 978-0-521-19225-5 · Portal: http://dlmf.nist.gov/ · Nota NIST: https://www.nist.gov/node/406446
- **Acceso y licencia:** Acceso gratuito oficial
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «NIST Digital Library of Mathematical Functions dlmf.nist.gov Olver Lozier Boisvert Clark»; WebFetch: sí, nota oficial del NIST (mayo de 2010))
- **Contenido:** Definiciones, propiedades y aproximaciones de funciones especiales (gamma, error, Bessel, hipergeométricas…), sucesora del Abramowitz-Stegun.
- **Uso en el Motor:** MC-01, MC-09: definiciones exactas de funciones especiales en fórmulas cerradas.
- **Limitaciones:** Citar versión y fecha consultadas.
- **Origen:** Ficha de carga V2.3 re-verificada por DOC-M el 2026-11-02 (tanda 2); se normaliza al formato del encargo.

#### DOC-MOT-0369 · Q 97 (A) — Multilevel Monte Carlo Path Simulation

- **Autores:** Michael B. Giles
- **Año:** 2008
- **Publicación o institución:** Operations Research, vol. 56, n.º 3, págs. 607-617
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-09 Simulación y métodos numéricos (principal) · secundarias: TM-06
- **Calidad Q:** 97 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI: 10.1287/opre.1070.0496 · Copia abierta: https://ora.ox.ac.uk/objects/uuid:d9d28973-94aa-4179-962a-28bcfa8d8f00/datastreams/ATTACHMENT01
- **Acceso y licencia:** Copia gratuita en ORA (Oxford); revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Monte Carlo methods in finance Sobol sequence multilevel Monte Carlo Mersenne Twister Euler–Maruyama (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Multilevel Monte Carlo method», que reproduce la cita completa)
- **Contenido:** Monte Carlo multinivel: combina discretizaciones de distinta finura para reducir el coste de O(ε⁻³) a O(ε⁻² (log ε)²).
- **Uso en el Motor:** MC-05: simulación eficiente de EDE.
- **Limitaciones:** Requiere acoplamiento entre niveles.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0005 · Q 97 (A) — Valuing American Options by Simulation: A Simple Least-Squares Approach

- **Autores:** Francis A. Longstaff; Eduardo S. Schwartz
- **Año:** 2001
- **Publicación o institución:** The Review of Financial Studies, vol. 14, n.º 1, págs. 113-147
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-09 Simulación y métodos numéricos (principal) · secundarias: TM-06
- **Calidad Q:** 97 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** DOI: 10.1093/rfs/14.1.113 (V2.3) · Copia de trabajo citada: http://repositories.cdlib.org/anderson/fin/1-01/ (eScholarship, UCLA)
- **Acceso y licencia:** Copia gratuita en eScholarship; revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Monte Carlo methods in finance Sobol sequence multilevel Monte Carlo Mersenne Twister Euler–Maruyama (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Monte Carlo methods in finance», que reproduce la cita completa)
- **Contenido:** Método LSM: estima el valor de continuación por regresión por mínimos cuadrados sobre trayectorias simuladas para valorar opciones americanas.
- **Uso en el Motor:** MC-05, MC-09: valoración americana por simulación.
- **Limitaciones:** Sesgo dependiente de la base de regresión.
- **Origen:** Ficha de carga V2.3 re-verificada por DOC-M el 2026-11-02 (tanda 2); se normaliza al formato del encargo.

#### DOC-MOT-0370 · Q 96 (A) — Multilevel Monte Carlo Methods

- **Autores:** Michael B. Giles
- **Año:** 2015
- **Publicación o institución:** Acta Numerica, vol. 24, págs. 259-328
- **Tipo de documento:** Artículo de revisión revisado por pares
- **Temática:** TM-09 Simulación y métodos numéricos (principal) · secundarias: —
- **Calidad Q:** 96 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** DOI: 10.1017/s096249291500001x · arXiv: https://arxiv.org/abs/1304.5472
- **Acceso y licencia:** Preprint gratuito en arXiv
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Monte Carlo methods in finance Sobol sequence multilevel Monte Carlo Mersenne Twister Euler–Maruyama (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Multilevel Monte Carlo method», que reproduce la cita completa)
- **Contenido:** Revisión completa de MLMC: teoría de complejidad, aplicaciones en finanzas, EDP estocásticas y variantes.
- **Uso en el Motor:** MC-05: diseño de simulaciones multinivel.
- **Limitaciones:** Técnico.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0372 · Q 96 (A) — Mersenne Twister: A 623-Dimensionally Equidistributed Uniform Pseudo-Random Number Generator

- **Autores:** Makoto Matsumoto; Takuji Nishimura
- **Año:** 1998
- **Publicación o institución:** ACM Transactions on Modeling and Computer Simulation, vol. 8, n.º 1, págs. 3-30
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-09 Simulación y métodos numéricos (principal) · secundarias: TM-14
- **Calidad Q:** 96 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** DOI: 10.1145/272991.272995 · PDF de los autores: http://www.math.sci.hiroshima-u.ac.jp/~m-mat/MT/ARTICLES/mt.pdf
- **Acceso y licencia:** Copia gratuita de los autores
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Monte Carlo methods in finance Sobol sequence multilevel Monte Carlo Mersenne Twister Euler–Maruyama (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Pseudorandom number generator», que reproduce la cita completa)
- **Contenido:** Generador MT19937 de periodo 2^19937−1 y equidistribución en 623 dimensiones; estándar en software científico.
- **Uso en el Motor:** MC-05: generador pseudoaleatorio y reproducibilidad de semillas.
- **Limitaciones:** No apto para criptografía; falla algunas baterías (TestU01).
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0374 · Q 94 (A) — Improved Long-Period Generators Based on Linear Recurrences Modulo 2

- **Autores:** François Panneton; Pierre L'Ecuyer; Makoto Matsumoto
- **Año:** 2006
- **Publicación o institución:** ACM Transactions on Mathematical Software, vol. 32, n.º 1, págs. 1-16
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-09 Simulación y métodos numéricos (principal) · secundarias: —
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** DOI: 10.1145/1132973.1132974 · PDF: http://www.iro.umontreal.ca/~lecuyer/myftp/papers/wellrng.pdf
- **Acceso y licencia:** Copia gratuita del autor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Monte Carlo methods in finance Sobol sequence multilevel Monte Carlo Mersenne Twister Euler–Maruyama (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Pseudorandom number generator», que reproduce la cita completa)
- **Contenido:** Generadores WELL con mejor equidistribución y recuperación más rápida de estados con muchos ceros que el Mersenne Twister.
- **Uso en el Motor:** MC-05: alternativa de generador pseudoaleatorio.
- **Limitaciones:** Menor adopción que MT.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0082 · Q 94 (A) — Convex Optimization

- **Autores:** Stephen Boyd; Lieven Vandenberghe
- **Año:** 2004
- **Publicación o institución:** Cambridge University Press (PDF gratuito de los autores)
- **Tipo de documento:** Manual de referencia
- **Temática:** TM-09 Simulación y métodos numéricos (principal) · secundarias: TM-07
- **Calidad Q:** 94 (A) — Tipo 20/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** DOI no visto (se retira «10.1017/CBO9780511804441») · https://web.stanford.edu/~boyd/cvxbook/
- **Acceso y licencia:** PDF completo gratuito de los autores
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Matrix Computations Golub Van Loan; Numerical Recipes; Convex Optimization Boyd Vandenberghe; Nocedal Wright Numerical Optimization; Higham Accuracy and Stability of Numerical Algorithms (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Stephen P. Boyd»)
- **Contenido:** Teoría y algoritmos de optimización convexa: dualidad, programación cónica, métodos de punto interior y aplicaciones.
- **Uso en el Motor:** MC-07: carteras con restricciones y regularización.
- **Limitaciones:** No cubre problemas no convexos.
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (tanda 2).

#### DOC-MOT-0375 · Q 94 (A) — An Algorithmic Introduction to Numerical Simulation of Stochastic Differential Equations

- **Autores:** Desmond J. Higham
- **Año:** 2001
- **Publicación o institución:** SIAM Review, vol. 43, n.º 3, págs. 525-546
- **Tipo de documento:** Artículo de revisión revisado por pares
- **Temática:** TM-09 Simulación y métodos numéricos (principal) · secundarias: —
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1137/S0036144500378302 · CiteSeerX: 10.1.1.137.6375
- **Acceso y licencia:** Copia en CiteSeerX; revista por suscripción
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Euler–Maruyama method Milstein method Crank–Nicolson finite difference methods for option pricing antithetic variates (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Stochastic differential equation», que reproduce la cita completa)
- **Contenido:** Introducción práctica con código a Euler-Maruyama, Milstein, convergencia fuerte y débil y estabilidad.
- **Uso en el Motor:** MC-05: implementación y prueba de esquemas de EDE.
- **Limitaciones:** Introductorio.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0080 · Q 94 (A) — The Stationary Bootstrap

- **Autores:** Dimitris N. Politis; Joseph P. Romano
- **Año:** 1994
- **Publicación o institución:** Journal of the American Statistical Association, vol. 89, n.º 428, págs. 1303-1313
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-09 Simulación y métodos numéricos (principal) · secundarias: TM-01
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1080/01621459.1994.10476870 · https://doi.org/10.1080/01621459.1994.10476870
- **Acceso y licencia:** Texto completo por suscripción en la editorial (Taylor & Francis)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Ledoit Wolf shrinkage estimation of covariance matrices stationary bootstrap Politis Romano Fama–MacBeth regression (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Bootstrapping (statistics)», que reproduce la cita completa)
- **Contenido:** Remuestreo por bloques de longitud aleatoria geométrica que preserva la estacionariedad de la serie remuestreada.
- **Uso en el Motor:** MC-05, MC-10: simulación de trayectorias dependientes.
- **Limitaciones:** Elección de la longitud media de bloque.
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (tanda 2).

#### DOC-MOT-0380 · Q 93 (A) — A Novel Pricing Method for European Options Based on Fourier-Cosine Series Expansions

- **Autores:** Fang Fang; Cornelis W. Oosterlee
- **Año:** 2008
- **Publicación o institución:** SIAM Journal on Scientific Computing, vol. 31, n.º 2, págs. 826-848
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-09 Simulación y métodos numéricos (principal) · secundarias: TM-06
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1137/080718061 · https://doi.org/10.1137%2F080718061
- **Acceso y licencia:** Texto completo por suscripción en la editorial (SIAM)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «VIX variance swap jump diffusion volatility risk premium implied volatility (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Stochastic volatility jump models», que reproduce la cita completa)
- **Contenido:** Método COS: valoración con desarrollo en serie de cosenos de la densidad a partir de la función característica, con convergencia exponencial.
- **Uso en el Motor:** MC-09: valoración rápida por transformadas.
- **Limitaciones:** Elección del intervalo de truncamiento.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0376 · Q 93 (A) — A Practical Method for Numerical Evaluation of Solutions of Partial Differential Equations of the Heat-Conduction Type

- **Autores:** J. Crank; P. Nicolson
- **Año:** 1947
- **Publicación o institución:** Mathematical Proceedings of the Cambridge Philosophical Society, vol. 43, n.º 1, págs. 50-67
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-09 Simulación y métodos numéricos (principal) · secundarias: TM-06
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1017/S0305004100023197 · https://doi.org/10.1017%2FS0305004100023197
- **Acceso y licencia:** Texto completo por suscripción en la editorial (Cambridge University Press)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Euler–Maruyama method Milstein method Crank–Nicolson finite difference methods for option pricing antithetic variates (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Crank–Nicolson method», que reproduce la cita completa)
- **Contenido:** Esquema implícito de segundo orden en tiempo e incondicionalmente estable para ecuaciones parabólicas; estándar en EDP de valoración.
- **Uso en el Motor:** MC-09: diferencias finitas para Black-Scholes y similares.
- **Limitaciones:** Oscilaciones con condiciones no suaves (usar pasos de Rannacher).
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0368 · Q 92 (A) — Options: A Monte Carlo Approach

- **Autores:** Phelim P. Boyle
- **Año:** 1977
- **Publicación o institución:** Journal of Financial Economics, vol. 4, n.º 3, págs. 323-338
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-09 Simulación y métodos numéricos (principal) · secundarias: TM-06
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1016/0304-405X(77)90005-8 · https://ideas.repec.org/a/eee/jfinec/v4y1977i3p323-338.html
- **Acceso y licencia:** Texto completo por suscripción en la editorial; ficha en IDEAS
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Monte Carlo methods in finance Sobol sequence multilevel Monte Carlo Mersenne Twister Euler–Maruyama (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Monte Carlo methods in finance», que reproduce la cita completa)
- **Contenido:** Primera aplicación de Monte Carlo a la valoración de opciones, con variables antitéticas y de control.
- **Uso en el Motor:** MC-05: fundamento de la valoración por simulación.
- **Limitaciones:** Histórico; métodos superados.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0007 · Q 90 (A) — Matrix Computations

- **Autores:** Gene H. Golub; Charles F. Van Loan
- **Año:** 2013 (4.ª ed.; 3.ª ed. de 1996)
- **Publicación o institución:** Johns Hopkins University Press
- **Tipo de documento:** Manual de referencia
- **Temática:** TM-09 Simulación y métodos numéricos (principal) · secundarias: TM-01
- **Calidad Q:** 90 (A) — Tipo 20/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** ISBN 4.ª ed.: 978-1-4214-0794-4 (verificado en V2.3) · ISBN 3.ª ed.: 978-0-8018-5413-2 · Cita en https://en.wikipedia.org/wiki/Numerical_linear_algebra
- **Acceso y licencia:** De pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Matrix Computations Golub Van Loan; Numerical Recipes; Convex Optimization Boyd Vandenberghe; Nocedal Wright Numerical Optimization; Higham Accuracy and Stability of Numerical Algorithms (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Numerical linear algebra», que reproduce la cita completa (3.ª ed.))
- **Contenido:** Referencia de álgebra lineal numérica: LU, Cholesky, QR, SVD, mínimos cuadrados y valores propios.
- **Uso en el Motor:** MC-05, MC-07: descomposiciones y mínimos cuadrados.
- **Limitaciones:** Hoy solo se ha visto la 3.ª ed.; la 4.ª se apoya en la verificación V2.3.
- **Origen:** Ficha de carga V2.3 re-verificada por DOC-M el 2026-11-02 (tanda 2); se normaliza al formato del encargo.

#### DOC-MOT-0008 · Q 90 (A) — Accuracy and Stability of Numerical Algorithms

- **Autores:** Nicholas J. Higham
- **Año:** 2002 (2.ª ed.; 1.ª ed. 1996)
- **Publicación o institución:** Society for Industrial and Applied Mathematics (SIAM)
- **Tipo de documento:** Manual de referencia
- **Temática:** TM-09 Simulación y métodos numéricos (principal) · secundarias: TM-14
- **Calidad Q:** 90 (A) — Tipo 20/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** ISBN 2.ª ed.: 978-0-89871-521-7 y DOI del libro 10.1137/1.9780898718027 (verificados en V2.3) · ISBN 1.ª ed.: 0-89871-355-2 · Copia de préstamo: https://archive.org/details/accuracystabilit0000high
- **Acceso y licencia:** De pago (SIAM); préstamo digital de la 1.ª ed. en Internet Archive
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Matrix Computations Golub Van Loan; Numerical Recipes; Convex Optimization Boyd Vandenberghe; Nocedal Wright Numerical Optimization; Higham Accuracy and Stability of Numerical Algorithms (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Numerical stability», que reproduce la cita completa y «Numerical linear algebra»)
- **Contenido:** Análisis de error de redondeo y estabilidad de algoritmos (sumas, sistemas lineales, factorizaciones).
- **Uso en el Motor:** MC-01…MC-10: análisis de error de los servicios de cálculo.
- **Limitaciones:** Técnico.
- **Origen:** Ficha de carga V2.3 re-verificada por DOC-M el 2026-11-02 (tanda 2); se normaliza al formato del encargo.

#### DOC-MOT-0379 · Q 90 (A) — Faster Valuation of Financial Derivatives

- **Autores:** Spassimir H. Paskov; Joseph F. Traub
- **Año:** 1995
- **Publicación o institución:** The Journal of Portfolio Management, vol. 22, n.º 1, págs. 113-120
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-09 Simulación y métodos numéricos (principal) · secundarias: TM-06
- **Calidad Q:** 90 (A) — Tipo 22/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** Copia de archivo (CMU, fondo Traub): https://iiif.library.cmu.edu/file/Traub_box00030_fld00007_bdl0001_doc0001/Traub_box00030_fld00007_bdl0001_doc0001.pdf
- **Acceso y licencia:** Copia gratuita en el archivo de Carnegie Mellon
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Monte Carlo methods in finance Sobol sequence multilevel Monte Carlo Mersenne Twister Euler–Maruyama (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Quasi-Monte Carlo methods in finance», que reproduce la cita completa)
- **Contenido:** Valoración de un CMO de 360 dimensiones con secuencias de Sobol' y Halton: cuasi-Monte Carlo supera claramente a Monte Carlo.
- **Uso en el Motor:** MC-05: evidencia de QMC en alta dimensión.
- **Limitaciones:** Caso único.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0371 · Q 90 (A) — Distribution of Points in a Cube and Approximate Evaluation of Integrals

- **Autores:** I. M. Sobol'
- **Año:** 1967
- **Publicación o institución:** Zh. Vych. Mat. Mat. Fiz., vol. 7, págs. 784-802 (traducción: U.S.S.R. Comput. Maths. Math. Phys., vol. 7, págs. 86-112)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-09 Simulación y métodos numéricos (principal) · secundarias: —
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 3/10
- **DOI / ISBN / URL:** Sin DOI · Cita en https://en.wikipedia.org/wiki/Sobol_sequence
- **Acceso y licencia:** Sin copia abierta identificada
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Monte Carlo methods in finance Sobol sequence multilevel Monte Carlo Mersenne Twister Euler–Maruyama (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Sobol sequence», que reproduce la cita completa)
- **Contenido:** Introduce las secuencias LPτ (Sobol') de baja discrepancia para integración cuasi-Monte Carlo.
- **Uso en el Motor:** MC-05: secuencias de baja discrepancia.
- **Limitaciones:** Acceso difícil; usar implementaciones (Joe-Kuo, SciPy).
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0373 · Q 89 (A) — Parallel Random Numbers: As Easy as 1, 2, 3

- **Autores:** John K. Salmon; Mark A. Moraes; Ron O. Dror; David E. Shaw
- **Año:** 2011
- **Publicación o institución:** Proceedings of the 2011 International Conference for High Performance Computing, Networking, Storage and Analysis (SC11), artículo 16
- **Tipo de documento:** Comunicación en congreso revisada por pares
- **Temática:** TM-09 Simulación y métodos numéricos (principal) · secundarias: TM-14
- **Calidad Q:** 89 (A) — Tipo 22/25 · Rigor 18/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1145/2063384.2063405
- **Acceso y licencia:** Actas ACM (suscripción)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Monte Carlo methods in finance Sobol sequence multilevel Monte Carlo Mersenne Twister Euler–Maruyama (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Pseudorandom number generator», que reproduce la cita completa)
- **Contenido:** Generadores basados en contador (Philox, Threefry) para simulación paralela reproducible.
- **Uso en el Motor:** MC-05: simulación paralela reproducible.
- **Limitaciones:** Comunicación de congreso.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0006 · Q 89 (A) — Monte Carlo Methods in Financial Engineering

- **Autores:** Paul Glasserman
- **Año:** 2003
- **Publicación o institución:** Springer (Stochastic Modelling and Applied Probability, vol. 53)
- **Tipo de documento:** Libro académico
- **Temática:** TM-09 Simulación y métodos numéricos (principal) · secundarias: TM-06
- **Calidad Q:** 89 (A) — Tipo 20/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** ISBN: 0-387-00451-3 (978-0-387-00451-8) · DOI del libro: 10.1007/978-0-387-21617-1 (verificado en V2.3) · Préstamo digital: https://archive.org/details/montecarlomethod53glas
- **Acceso y licencia:** De pago (Springer)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Monte Carlo methods in finance Sobol sequence multilevel Monte Carlo Mersenne Twister Euler–Maruyama (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Monte Carlo methods in finance», que reproduce la cita completa y «Quasi-Monte Carlo methods in finance»)
- **Contenido:** Monte Carlo en finanzas: generación de variables, discretización, reducción de varianza, cuasi-Monte Carlo, sensibilidades y opciones americanas.
- **Uso en el Motor:** MC-05: simulación y control de error.
- **Limitaciones:** No cubre MLMC (posterior).
- **Origen:** Ficha de carga V2.3 re-verificada por DOC-M el 2026-11-02 (tanda 2); se normaliza al formato del encargo.

#### DOC-MOT-0378 · Q 89 (A) — Quasi-Monte Carlo Methods in Numerical Finance

- **Autores:** Corwin Joy; Phelim P. Boyle; Ken Seng Tan
- **Año:** 1996
- **Publicación o institución:** Management Science, vol. 42, n.º 6, págs. 926-938
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-09 Simulación y métodos numéricos (principal) · secundarias: TM-06
- **Calidad Q:** 89 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** Sin DOI visto · Cita en https://en.wikipedia.org/wiki/Quasi-Monte_Carlo_methods_in_finance
- **Acceso y licencia:** Texto completo por suscripción en la editorial (INFORMS)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Monte Carlo methods in finance Sobol sequence multilevel Monte Carlo Mersenne Twister Euler–Maruyama (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Quasi-Monte Carlo methods in finance», que reproduce la cita completa)
- **Contenido:** Aplica secuencias de baja discrepancia a la valoración de derivados y muestra mejoras de convergencia frente a Monte Carlo.
- **Uso en el Motor:** MC-05: cuasi-Monte Carlo en valoración.
- **Limitaciones:** Alerta: REPARAR (DOI/URL editorial no vistos). La página índice escribe el tercer autor como «Tang, K. S.».
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0081 · Q 89 (A) — Numerical Solution of Stochastic Differential Equations

- **Autores:** Peter E. Kloeden; Eckhard Platen
- **Año:** 1992
- **Publicación o institución:** Springer
- **Tipo de documento:** Libro académico
- **Temática:** TM-09 Simulación y métodos numéricos (principal) · secundarias: —
- **Calidad Q:** 89 (A) — Tipo 20/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.1007/978-3-662-12616-5 · https://doi.org/10.1007/978-3-662-12616-5
- **Acceso y licencia:** De pago (Springer)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Euler–Maruyama method Milstein method Crank–Nicolson finite difference methods for option pricing antithetic variates (dominio en.wikipedia.org)» y «Monte Carlo methods in finance Sobol sequence multilevel Monte Carlo Mersenne Twister Euler–Maruyama (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Stochastic differential equation», que reproduce la cita completa y «Monte Carlo methods in finance»)
- **Contenido:** Esquemas de Euler-Maruyama, Milstein y de orden superior, con órdenes de convergencia fuerte y débil.
- **Uso en el Motor:** MC-05: discretización de EDE.
- **Limitaciones:** Notación densa.
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (tanda 2).

#### DOC-MOT-0377 · Q 89 (A) — Finite Difference Methods and Jump Processes Arising in the Pricing of Contingent Claims: A Synthesis

- **Autores:** Michael Brennan; Eduardo Schwartz
- **Año:** 1978
- **Publicación o institución:** Journal of Financial and Quantitative Analysis, vol. 13, n.º 3, págs. 461-474
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-09 Simulación y métodos numéricos (principal) · secundarias: TM-06
- **Calidad Q:** 89 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.2307/2330152 · JSTOR: 2330152
- **Acceso y licencia:** Texto completo por suscripción en la editorial (Cambridge University Press/JSTOR)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Euler–Maruyama method Milstein method Crank–Nicolson finite difference methods for option pricing antithetic variates (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Finite difference methods for option pricing», que reproduce la cita completa)
- **Contenido:** Relaciona los esquemas explícitos de diferencias finitas con procesos de salto y árboles, sintetizando su uso en valoración.
- **Uso en el Motor:** MC-09: fundamentos de diferencias finitas en finanzas.
- **Limitaciones:** Histórico.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0083 · Q 87 (A) — Numerical Optimization

- **Autores:** Jorge Nocedal; Stephen J. Wright
- **Año:** 1999 (1.ª ed.; la semilla citaba la 2.ª ed. de 2006, no verificada en esta pasada)
- **Publicación o institución:** Springer
- **Tipo de documento:** Manual de referencia
- **Temática:** TM-09 Simulación y métodos numéricos (principal) · secundarias: TM-07
- **Calidad Q:** 87 (A) — Tipo 20/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** ISBN 1.ª ed.: 0-387-98793-2 (se retira el DOI de la 2.ª ed. «10.1007/978-0-387-40065-5», no visto) · Cita en https://en.wikipedia.org/wiki/Nonlinear_programming
- **Acceso y licencia:** De pago (Springer)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Matrix Computations Golub Van Loan; Numerical Recipes; Convex Optimization Boyd Vandenberghe; Nocedal Wright Numerical Optimization; Higham Accuracy and Stability of Numerical Algorithms (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Nonlinear programming», que reproduce la cita completa)
- **Contenido:** Algoritmos de optimización continua: búsqueda lineal, regiones de confianza, cuasi-Newton, mínimos cuadrados no lineales y restricciones.
- **Uso en el Motor:** MC-07: optimización no lineal y calibración.
- **Limitaciones:** Comprobar la 2.ª ed. en el próximo barrido.
- **Origen:** Semilla V3.0 confirmada por DOC-M el 2026-11-02 (tanda 2).

#### DOC-MOT-0381 · Q 85 (A) — The Mathematics of Financial Derivatives: A Student Introduction

- **Autores:** Paul Wilmott; Sam Howison; Jeff Dewynne
- **Año:** 1995
- **Publicación o institución:** Cambridge University Press
- **Tipo de documento:** Manual de referencia
- **Temática:** TM-09 Simulación y métodos numéricos (principal) · secundarias: TM-06
- **Calidad Q:** 85 (A) — Tipo 20/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** ISBN: 978-0-521-49789-3 · Préstamo digital: https://archive.org/details/mathematicsoffin00wilm
- **Acceso y licencia:** De pago; préstamo digital en Internet Archive
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Euler–Maruyama method Milstein method Crank–Nicolson finite difference methods for option pricing antithetic variates (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Finite difference methods for option pricing», que reproduce la cita completa y «Crank–Nicolson method»)
- **Contenido:** Introducción a la valoración por EDP: Black-Scholes, problemas de frontera libre y diferencias finitas.
- **Uso en el Motor:** MC-09: formulación y resolución por EDP.
- **Limitaciones:** Introductorio.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0009 · Q 82 (A) — Numerical Recipes: The Art of Scientific Computing (3.ª ed.)

- **Autores:** William H. Press; Saul A. Teukolsky; William T. Vetterling; Brian P. Flannery
- **Año:** 2007
- **Publicación o institución:** Cambridge University Press
- **Tipo de documento:** Manual de referencia
- **Temática:** TM-09 Simulación y métodos numéricos (principal) · secundarias: —
- **Calidad Q:** 82 (A) — Tipo 20/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 9/10 · Acceso 5/10
- **DOI / ISBN / URL:** ISBN: 978-0-521-88068-8 (verificado en V2.3) · Cita en https://en.wikipedia.org/wiki/Pseudorandom_number_generator
- **Acceso y licencia:** De pago; código histórico en nr.com
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Monte Carlo methods in finance Sobol sequence multilevel Monte Carlo Mersenne Twister Euler–Maruyama (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Pseudorandom number generator», que reproduce la cita completa)
- **Contenido:** Recetario de métodos numéricos con código: interpolación, integración, raíces, optimización, generadores aleatorios.
- **Uso en el Motor:** MC-01…MC-10: selección de rutinas numéricas estándar.
- **Limitaciones:** Licencia de código restrictiva; algunos métodos superados.
- **Origen:** Ficha de carga V2.3 re-verificada por DOC-M el 2026-11-02 (tanda 2); se normaliza al formato del encargo.

#### DOC-MOT-0383 · Q 81 (A) — Construction and Comparison of High-Dimensional Sobol' Generators

- **Autores:** Ilya Sobol'; Danil Asotsky; Alexander Kreinin; Sergei Kucherenko
- **Año:** 2011
- **Publicación o institución:** Wilmott Journal, n.º 56, págs. 64-79
- **Tipo de documento:** Artículo en revista profesional
- **Temática:** TM-09 Simulación y métodos numéricos (principal) · secundarias: —
- **Calidad Q:** 81 (A) — Tipo 15/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 8/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI: 10.1002/wilm.10056 · PDF: http://www.broda.co.uk/doc/HD_SobolGenerator.pdf
- **Acceso y licencia:** Copia gratuita (BRODA)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Monte Carlo methods in finance Sobol sequence multilevel Monte Carlo Mersenne Twister Euler–Maruyama (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Sobol sequence», que reproduce la cita completa)
- **Contenido:** Construcción y comparación de generadores Sobol' de alta dimensión (hasta decenas de miles de dimensiones) con propiedades A y A'.
- **Uso en el Motor:** MC-05: elección de números de dirección para QMC.
- **Limitaciones:** Coautores vinculados a proveedor comercial (BRODA).
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

#### DOC-MOT-0382 · Q 81 (A) — Monte Carlo Methods in Finance

- **Autores:** Peter Jäckel
- **Año:** 2002
- **Publicación o institución:** John Wiley & Sons
- **Tipo de documento:** Libro académico-profesional
- **Temática:** TM-09 Simulación y métodos numéricos (principal) · secundarias: TM-06
- **Calidad Q:** 81 (A) — Tipo 18/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** ISBN: 0-471-49741-X · Cita en https://en.wikipedia.org/wiki/Sobol_sequence
- **Acceso y licencia:** De pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Monte Carlo methods in finance Sobol sequence multilevel Monte Carlo Mersenne Twister Euler–Maruyama (dominio en.wikipedia.org)»; WebFetch: sí, página índice de Wikipedia «Sobol sequence», que reproduce la cita completa y «Quasi-Monte Carlo methods in finance»)
- **Contenido:** Monte Carlo práctico: generadores, Sobol' con inicialización, puentes brownianos, reducción de varianza y griegas.
- **Uso en el Motor:** MC-05: implementación de simulación en producción.
- **Limitaciones:** Orientado a practicantes.
- **Origen:** Alta nueva F8_M2 (tanda 2), 2026-11-02.

## TM-10 Aprendizaje automático para finanzas

#### DOC-MOT-0086 · Q 95 (A) — Empirical Asset Pricing via Machine Learning

- **Autores:** Shihao Gu; Bryan Kelly; Dacheng Xiu
- **Año:** 2020
- **Publicación o institución:** The Review of Financial Studies, 33(5), 2223-2273 (versión previa: NBER Working Paper 25398, 2018, rev. 2019)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-10 Aprendizaje automático para finanzas (principal) · secundarias: TM-07
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1093/rfs/hhaa009 · https://nber.org/papers/w25398
- **Acceso y licencia:** Artículo de revista de pago; documento de trabajo NBER de acceso abierto (DOI WP: 10.3386/w25398)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Gu Kelly Xiu 2020 "Empirical Asset Pricing via Machine Learning" Review of Financial Studies»; WebFetch: sí)
- **Contenido:** Compara regresiones penalizadas, componentes principales, árboles potenciados, bosques aleatorios y redes neuronales para predecir rentabilidades de acciones de EE. UU.; árboles y redes superan con claridad a los modelos lineales, con variables de momentum, liquidez y volatilidad como predictores dominantes.
- **Uso en el Motor:** MC-06: referencia de comparación de métodos de aprendizaje automático para la predicción de rentabilidades y la medición del R² fuera de muestra.
- **Limitaciones:** Universo estadounidense; costes de implementación y de rotación no centrales.

#### DOC-MOT-0087 · Q 94 (A) — Random Forests

- **Autores:** Leo Breiman
- **Año:** 2001
- **Publicación o institución:** Machine Learning, 45(1), 5-32
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-10 Aprendizaje automático para finanzas (principal)
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1023/A:1010933404324 · https://mlanthology.org/mlj/2001/breiman2001mlj-random
- **Acceso y licencia:** Artículo de pago en el editor (Springer); ficha bibliográfica abierta
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Breiman 2001 "Random Forests" Machine Learning 45 5-32»; WebFetch: sí)
- **Contenido:** Define los bosques aleatorios (agregación de árboles con remuestreo y selección aleatoria de variables), su error fuera de bolsa y la importancia de variables por permutación.
- **Uso en el Motor:** MC-06: bosques aleatorios para clasificación y regresión; error fuera de bolsa como estimación interna.
- **Limitaciones:** Importancia de variables sesgada con predictores correlacionados; el error fuera de bolsa no respeta la dependencia temporal.

#### DOC-MOT-0400 · Q 94 (A) — Greedy Function Approximation: A Gradient Boosting Machine

- **Autores:** Jerome H. Friedman
- **Año:** 2001
- **Publicación o institución:** The Annals of Statistics, 29(5), 1189-1232
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-10 Aprendizaje automático para finanzas (principal) · secundarias: TM-01
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.1214/aos/1013203451 · https://projecteuclid.org/euclid.aos/1013203451
- **Acceso y licencia:** Página del editor (Project Euclid) con resumen abierto; texto completo según suscripción
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Friedman 2001 "Greedy function approximation: A gradient boosting machine" Annals of Statistics»; WebFetch: sí)
- **Contenido:** Formula el boosting como descenso de gradiente en el espacio de funciones con pérdidas arbitrarias (cuadrática, absoluta, Huber, logística) y árboles de regresión como aprendices base; introduce la contracción (shrinkage) y los gráficos de dependencia parcial.
- **Uso en el Motor:** MC-06: fundamento de los modelos de boosting de gradiente (XGBoost, LightGBM) y de la interpretación por dependencia parcial.
- **Limitaciones:** Marco general; no aborda dependencia temporal ni no estacionariedad de datos financieros.

#### DOC-MOT-0401 · Q 94 (A) — Regression Shrinkage and Selection via the Lasso

- **Autores:** Robert Tibshirani
- **Año:** 1996
- **Publicación o institución:** Journal of the Royal Statistical Society, Series B (Methodological), 58(1), 267-288
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-10 Aprendizaje automático para finanzas (principal) · secundarias: TM-01, TM-04
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1111/j.2517-6161.1996.tb02080.x · https://academicnewsletter.sufe.edu.cn/info/442374
- **Acceso y licencia:** Artículo de pago en el editor; copias docentes en abierto (p. ej., sites.stat.washington.edu)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Tibshirani 1996 "Regression shrinkage and selection via the lasso" Journal of the Royal Statistical Society Series B»; WebFetch: sí)
- **Contenido:** Propone el lasso: mínimos cuadrados con restricción en la norma L1 de los coeficientes, que contrae y anula coeficientes y realiza selección de variables continua.
- **Uso en el Motor:** MC-06: selección de predictores en regresiones de rentabilidad con muchos candidatos; línea base penalizada frente a métodos no lineales.
- **Limitaciones:** Selección inestable con predictores muy correlacionados (véase elastic net, DOC-MOT-0402); el número de volumen se toma de la cita estándar, la página leída solo mostraba páginas y DOI.

#### DOC-MOT-0413 · Q 93 (A) — Statistical Learning and Selective Inference

- **Autores:** Jonathan Taylor; Robert J. Tibshirani
- **Año:** 2015
- **Publicación o institución:** Proceedings of the National Academy of Sciences, 112(25), 7629-7634
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-10 Aprendizaje automático para finanzas (principal) · secundarias: TM-01, TM-11
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** DOI: 10.1073/pnas.1507583112 · https://en.wikipedia.org/wiki/Data_dredging (bibliografía)
- **Acceso y licencia:** Acceso abierto en PMC (PMC4485109)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Data dredging" wikipedia data snooping White reality check»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Data_dredging)
- **Contenido:** Presenta la inferencia selectiva: intervalos y p-valores válidos después de haber elegido el modelo con los mismos datos (p. ej., tras el lasso o la regresión por pasos).
- **Uso en el Motor:** MC-06, MC-10: inferencia honesta sobre predictores seleccionados por algoritmos de regularización.
- **Limitaciones:** Supuestos gaussianos en la versión básica; implementación no trivial con datos dependientes.

#### DOC-MOT-0084 · Q 93 (A) — The Elements of Statistical Learning (2.ª ed.)

- **Autores:** Trevor Hastie; Robert Tibshirani; Jerome Friedman
- **Año:** 2009
- **Publicación o institución:** Springer (PDF gratuito de los autores en la Universidad de Stanford)
- **Tipo de documento:** Manual de referencia
- **Temática:** TM-10 Aprendizaje automático para finanzas (principal) · secundarias: TM-01
- **Calidad Q:** 93 (A) — Tipo 20/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://web.stanford.edu/~hastie/Papers/ESLII.pdf
- **Acceso y licencia:** PDF completo de acceso gratuito publicado por los autores; edición impresa de pago (Springer)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Hastie Tibshirani Friedman "The Elements of Statistical Learning" second edition pdf stanford»; WebFetch: no)
- **Contenido:** Manual de referencia del aprendizaje estadístico: regularización, árboles, boosting, métodos kernel, validación cruzada y descomposición sesgo-varianza.
- **Uso en el Motor:** MC-06: base teórica de regularización, árboles, boosting y selección de modelos.
- **Limitaciones:** Sin tratamiento específico de datos financieros dependientes ni de validación temporal. El DOI del libro que figuraba en la semilla no se ha visto en la verificación y se retira de la ficha.

#### DOC-MOT-0402 · Q 93 (A) — Regularization and Variable Selection via the Elastic Net

- **Autores:** Hui Zou; Trevor Hastie
- **Año:** 2005
- **Publicación o institución:** Journal of the Royal Statistical Society, Series B (Statistical Methodology), 67(2), 301-320
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-10 Aprendizaje automático para finanzas (principal) · secundarias: TM-01
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.1111/j.1467-9868.2005.00503.x · https://ideas.repec.org/a/bla/jorssb/v67y2005i2p301-320.html
- **Acceso y licencia:** Artículo de pago en el editor; ficha abierta en RePEc y copia docente en sites.stat.washington.edu
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Zou Hastie 2005 "Regularization and variable selection via the elastic net" JRSS B»; WebFetch: sí)
- **Contenido:** Combina penalizaciones L1 y L2 para seleccionar variables agrupando predictores correlacionados y funcionar cuando hay más variables que observaciones.
- **Uso en el Motor:** MC-06: regresión penalizada por defecto con predictores financieros colineales (ratios de valoración, diferenciales).
- **Limitaciones:** Dos hiperparámetros a ajustar con validación respetuosa del orden temporal; existe una corrección publicada por los autores (web.stanford.edu).

#### DOC-MOT-0403 · Q 92 (A) — Characteristics Are Covariances: A Unified Model of Risk and Return

- **Autores:** Bryan T. Kelly; Seth Pruitt; Yinan Su
- **Año:** 2019
- **Publicación o institución:** Journal of Financial Economics, 134(3), 501-524 (versión previa: NBER Working Paper 24540)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-10 Aprendizaje automático para finanzas (principal) · secundarias: TM-07
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1016/j.jfineco.2019.05.001 · https://ideas.repec.org/a/eee/jfinec/v134y2019i3p501-524.html
- **Acceso y licencia:** Artículo de pago; documento de trabajo NBER w24540 disponible
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Kelly Pruitt Su 2019 "Characteristics are covariances: A unified model of risk and return" Journal of Financial Economics»; WebFetch: sí)
- **Contenido:** Introduce el análisis de componentes principales instrumentado (IPCA): factores latentes con cargas variables en el tiempo que dependen de características observables; cinco factores IPCA explican mejor las rentabilidades medias que los modelos factoriales habituales.
- **Uso en el Motor:** MC-06, MC-05: reducción de dimensión con cargas condicionales para modelos factoriales y atribución de rentabilidad.
- **Limitaciones:** Estimación por mínimos cuadrados alternos; universo de acciones de EE. UU.

#### DOC-MOT-0404 · Q 91 (A) — The Virtue of Complexity in Return Prediction

- **Autores:** Bryan T. Kelly; Semyon Malamud; Kangying Zhou
- **Año:** 2024
- **Publicación o institución:** The Journal of Finance, 79(1), 459-503
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-10 Aprendizaje automático para finanzas (principal) · secundarias: TM-11
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 9/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1111/jofi.13298 · https://www.sfi.ch/en/publications/the-virtue-of-complexity-in-return-prediction
- **Acceso y licencia:** Artículo de pago; copia del artículo publicada en economics.yale.edu
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Kelly Malamud Zhou "The Virtue of Complexity in Return Prediction" Journal of Finance»; WebFetch: sí)
- **Contenido:** Demuestra teórica y empíricamente que modelos de predicción con más parámetros que observaciones (regresiones de características aleatorias con contracción) pueden mejorar el rendimiento fuera de muestra y el Sharpe de la estrategia de market timing.
- **Uso en el Motor:** MC-06: justificación y límites de modelos sobreparametrizados con regularización para predecir rentabilidades.
- **Limitaciones:** Resultado debatido en la literatura posterior; sensible a la normalización y a la elección de la penalización; uno de los autores trabaja en la industria (AQR).

#### DOC-MOT-0405 · Q 90 (A) — Financial Machine Learning

- **Autores:** Bryan T. Kelly; Dacheng Xiu
- **Año:** 2023
- **Publicación o institución:** Foundations and Trends in Finance, 13(3-4), 205-363 (también NBER Working Paper 31502)
- **Tipo de documento:** Artículo de revisión (monografía)
- **Temática:** TM-10 Aprendizaje automático para finanzas (principal) · secundarias: TM-07, TM-11
- **Calidad Q:** 90 (A) — Tipo 22/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 9/10 · Acceso 9/10
- **DOI / ISBN / URL:** DOI: 10.3386/w31502 · https://www.nber.org/papers/w31502
- **Acceso y licencia:** Documento de trabajo NBER y versión SSRN de acceso abierto
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Kelly Xiu "Financial Machine Learning" Foundations and Trends in Finance 2023»; WebFetch: sí)
- **Contenido:** Revisión sistemática del aprendizaje automático en finanzas: predicción de rentabilidades, modelos factoriales con aprendizaje, optimización de carteras, texto y datos alternativos, con orientaciones de investigación.
- **Uso en el Motor:** MC-06: mapa de métodos y buenas prácticas para elegir el algoritmo según el problema financiero.
- **Limitaciones:** Sesgo hacia la investigación de los propios autores; aplicaciones centradas en renta variable estadounidense.

#### DOC-MOT-0412 · Q 90 (A) — A Unified View of Performance Metrics: Translating Threshold Choice into Expected Classification Loss

- **Autores:** José Hernández-Orallo; Peter A. Flach; César Ferri
- **Año:** 2012
- **Publicación o institución:** Journal of Machine Learning Research, 13, 2813-2869
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-10 Aprendizaje automático para finanzas (principal) · secundarias: TM-11
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 6/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** http://jmlr.org/papers/volume13/hernandez-orallo12a/hernandez-orallo12a.pdf
- **Acceso y licencia:** Acceso abierto (JMLR)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Brier score" en.wikipedia.org»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Brier_score)
- **Contenido:** Demuestra que métricas como el Brier, el AUC o la exactitud son pérdidas de clasificación esperadas bajo distintas reglas de elección de umbral, lo que unifica la evaluación de clasificadores probabilísticos.
- **Uso en el Motor:** MC-06, MC-10: elegir la métrica de evaluación de clasificadores coherente con cómo se fijará el umbral de decisión.
- **Limitaciones:** Marco teórico; requiere conocer la política de umbrales del usuario final.

#### DOC-MOT-0090 · Q 89 (A) — On Calibration of Modern Neural Networks

- **Autores:** Chuan Guo; Geoff Pleiss; Yu Sun; Kilian Q. Weinberger
- **Año:** 2017
- **Publicación o institución:** Proceedings of the 34th International Conference on Machine Learning (ICML 2017), PMLR 70, 1321-1330
- **Tipo de documento:** Comunicación de congreso revisada por pares
- **Temática:** TM-10 Aprendizaje automático para finanzas (principal) · secundarias: TM-11
- **Calidad Q:** 89 (A) — Tipo 20/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** https://proceedings.mlr.press/v70/guo17a.html (preprint: arXiv 1706.04599)
- **Acceso y licencia:** Acceso abierto (PMLR y arXiv)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Guo Pleiss Sun Weinberger "On Calibration of Modern Neural Networks" ICML 2017 PMLR»; WebFetch: sí)
- **Contenido:** Muestra que las redes neuronales profundas están mal calibradas, define el error de calibración esperado (ECE) y propone el escalado de temperatura como corrección simple y eficaz.
- **Uso en el Motor:** MC-06, MC-10: medición del ECE y recalibración de probabilidades de modelos neuronales.
- **Limitaciones:** Centrado en clasificación de imágenes y texto; no aborda el desplazamiento de distribución típico de los mercados.

#### DOC-MOT-0406 · Q 88 (A) — A Unified Approach to Interpreting Model Predictions

- **Autores:** Scott M. Lundberg; Su-In Lee
- **Año:** 2017
- **Publicación o institución:** Advances in Neural Information Processing Systems 30 (NIPS 2017)
- **Tipo de documento:** Comunicación de congreso revisada por pares
- **Temática:** TM-10 Aprendizaje automático para finanzas (principal) · secundarias: TM-14
- **Calidad Q:** 88 (A) — Tipo 20/25 · Rigor 16/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 9/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://papers.nips.cc/paper/7062-a (preprint: arXiv 1705.07874)
- **Acceso y licencia:** Acceso abierto (actas NeurIPS y arXiv)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Lundberg Lee 2017 "A Unified Approach to Interpreting Model Predictions" NeurIPS»; WebFetch: sí)
- **Contenido:** Propone SHAP: atribución aditiva de la predicción a cada variable basada en valores de Shapley, con propiedades de unicidad y aproximaciones eficientes (Kernel SHAP).
- **Uso en el Motor:** MC-06: explicación de predicciones de modelos no lineales en los artefactos del Motor (contribución de cada señal).
- **Limitaciones:** Atribuciones engañosas con variables correlacionadas; coste computacional; explica el modelo, no la causalidad.

#### DOC-MOT-0088 · Q 88 (A) — XGBoost: A Scalable Tree Boosting System

- **Autores:** Tianqi Chen; Carlos Guestrin
- **Año:** 2016
- **Publicación o institución:** Proceedings of the 22nd ACM SIGKDD International Conference on Knowledge Discovery and Data Mining (KDD '16), ACM
- **Tipo de documento:** Comunicación de congreso revisada por pares
- **Temática:** TM-10 Aprendizaje automático para finanzas (principal)
- **Calidad Q:** 88 (A) — Tipo 20/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI: 10.1145/2939672.2939785 · https://arxiv.org/abs/1603.02754
- **Acceso y licencia:** Preprint de acceso abierto en arXiv; versión de actas en ACM
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Chen Guestrin "XGBoost: A Scalable Tree Boosting System" KDD 2016 arXiv»; WebFetch: sí)
- **Contenido:** Describe XGBoost: boosting de árboles con regularización explícita, algoritmo consciente de la dispersión, bosquejo de cuantiles ponderado y diseño de sistema escalable.
- **Uso en el Motor:** MC-06: implementación de referencia de boosting de gradiente regularizado.
- **Limitaciones:** Riesgo de sobreajuste sin validación temporal; artículo de sistema, no de inferencia.

#### DOC-MOT-0089 · Q 87 (A) — Predicting Good Probabilities with Supervised Learning

- **Autores:** Alexandru Niculescu-Mizil; Rich Caruana
- **Año:** 2005
- **Publicación o institución:** Proceedings of the 22nd International Conference on Machine Learning (ICML 2005), ACM, 625-632
- **Tipo de documento:** Comunicación de congreso revisada por pares
- **Temática:** TM-10 Aprendizaje automático para finanzas (principal) · secundarias: TM-11
- **Calidad Q:** 87 (A) — Tipo 20/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI: 10.1145/1102351.1102430 · https://mlanthology.org/icml/2005/niculescumizil2005icml-predicting
- **Acceso y licencia:** Ficha abierta en ML Anthology; texto en ACM Digital Library
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Niculescu-Mizil Caruana 2005 "Predicting good probabilities with supervised learning" ICML»; WebFetch: sí)
- **Contenido:** Evalúa la calibración de las probabilidades de diez clasificadores y muestra cómo corregirla con escalado de Platt y regresión isotónica.
- **Uso en el Motor:** MC-06, MC-10: calibración de probabilidades de clasificadores (Platt, isotónica) antes de emitir probabilidades de escenarios.
- **Limitaciones:** Datos no financieros; la isotónica sobreajusta con muestras pequeñas.

#### DOC-MOT-0407 · Q 86 (A) — Deep Learning in Asset Pricing

- **Autores:** Luyang Chen; Markus Pelger; Jason Zhu
- **Año:** 2024
- **Publicación o institución:** Management Science (INFORMS); documento de trabajo SSRN 3350138 (2019, rev. 2021)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-10 Aprendizaje automático para finanzas (principal) · secundarias: TM-07
- **Calidad Q:** 86 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 7/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** DOI: 10.1287/mnsc.2023.4695 · https://papers.ssrn.com/abstract=3350138
- **Acceso y licencia:** Documento de trabajo gratuito en SSRN y arXiv (1904.00745); versión de revista de pago
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Chen Pelger Zhu "Deep Learning in Asset Pricing" Management Science»; WebFetch: sí, sobre SSRN)
- **Contenido:** Estima el factor de descuento estocástico con redes neuronales (incluidas recurrentes para estados macro) bajo la condición de no arbitraje mediante un enfoque adversarial, logrando mayor Sharpe y menores errores de valoración que los modelos de referencia.
- **Uso en el Motor:** MC-06: referencia para imponer restricciones económicas (no arbitraje) a modelos de aprendizaje profundo.
- **Limitaciones:** Alta complejidad y sensibilidad a hiperparámetros; año de la revista inferido del DOI y de la página del editor (no se vio volumen/páginas).

#### DOC-MOT-0408 · Q 84 (A) — An Empirical Comparison of Supervised Learning Algorithms

- **Autores:** Rich Caruana; Alexandru Niculescu-Mizil
- **Año:** 2006
- **Publicación o institución:** Proceedings of the 23rd International Conference on Machine Learning (ICML 2006), ACM International Conference Proceeding Series vol. 148, 161-168
- **Tipo de documento:** Comunicación de congreso revisada por pares
- **Temática:** TM-10 Aprendizaje automático para finanzas (principal) · secundarias: TM-11
- **Calidad Q:** 84 (A) — Tipo 20/25 · Rigor 16/20 · Autoridad 13/15 · Vigencia 8/10 · Impacto 9/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** https://cs.utexas.edu/~shivaram/readings/b2hd-CaruanaNiculescu-Mizil2006.html
- **Acceso y licencia:** Ficha bibliográfica abierta; texto en ACM Digital Library
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Niculescu-Mizil Caruana 2005 "Predicting good probabilities with supervised learning" ICML» —resultado relacionado—; WebFetch: sí)
- **Contenido:** Compara diez algoritmos supervisados en once problemas y ocho métricas (exactitud, AUC, error cuadrático, entropía cruzada…), antes y después de calibrar; árboles potenciados calibrados, bosques aleatorios y SVM encabezan el ranking.
- **Uso en el Motor:** MC-06: criterio para escoger familias de modelos y para evaluar con varias métricas, no solo exactitud.
- **Limitaciones:** Conjuntos de datos no financieros y anteriores al aprendizaje profundo moderno.

#### DOC-MOT-0085 · Q 83 (A) — Advances in Financial Machine Learning

- **Autores:** Marcos López de Prado
- **Año:** 2018
- **Publicación o institución:** John Wiley & Sons
- **Tipo de documento:** Libro académico-profesional
- **Temática:** TM-10 Aprendizaje automático para finanzas (principal) · secundarias: TM-11
- **Calidad Q:** 83 (A) — Tipo 20/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 8/10 · Acceso 5/10
- **DOI / ISBN / URL:** ISBN: 978-1-119-48208-6 · https://www.wiley-vch.de/en/areas-interest/finance-economics-law/advances-in-financial-machine-learning-978-1-119-48208-6
- **Acceso y licencia:** Libro de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «López de Prado "Advances in Financial Machine Learning" Wiley 2018 ISBN 978-1-119-48208-6»; WebFetch: no)
- **Contenido:** Manual práctico de aprendizaje automático financiero: barras de información, etiquetado por triple barrera, metaetiquetado, diferenciación fraccional, validación cruzada purgada con embargo, importancia de variables y sobreajuste de backtest.
- **Uso en el Motor:** MC-06, MC-10: etiquetado por triple barrera, validación cruzada purgada con embargo, importancia de variables y control del sobreajuste.
- **Limitaciones:** Algunas propuestas con evidencia empírica limitada; autor vinculado a la industria.

#### DOC-MOT-0409 · Q 83 (A) — Regression Shrinkage and Selection via the Lasso: A Retrospective

- **Autores:** Robert Tibshirani
- **Año:** 2011
- **Publicación o institución:** Journal of the Royal Statistical Society, Series B (Statistical Methodology), 73(3), 273-282
- **Tipo de documento:** Artículo revisado por pares (retrospectiva con discusión)
- **Temática:** TM-10 Aprendizaje automático para finanzas (principal) · secundarias: TM-01
- **Calidad Q:** 83 (A) — Tipo 22/25 · Rigor 14/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** DOI: 10.1111/j.1467-9868.2011.00771.x · https://academicnewsletter.sufe.edu.cn/info/442010
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Tibshirani 1996 "Regression shrinkage and selection via the lasso" Journal of the Royal Statistical Society Series B» —resultado relacionado—; WebFetch: sí)
- **Contenido:** Repasa quince años de desarrollo del lasso: algoritmos (LARS, descenso por coordenadas), extensiones (lasso agrupado, fusionado, elastic net) e inferencia tras la selección.
- **Uso en el Motor:** MC-06: guía para elegir la variante de penalización adecuada (grupos de señales, series suavizadas).
- **Limitaciones:** Texto breve de posición; el número de volumen procede de la cita estándar (la página leída mostraba páginas y DOI).

#### DOC-MOT-0411 · Q 80 (A) — Machine Learning for Asset Managers

- **Autores:** Marcos López de Prado
- **Año:** 2020
- **Publicación o institución:** Cambridge University Press, serie Elements in Quantitative Finance
- **Tipo de documento:** Libro académico-profesional (monografía breve)
- **Temática:** TM-10 Aprendizaje automático para finanzas (principal) · secundarias: TM-07, TM-11
- **Calidad Q:** 80 (A) — Tipo 20/25 · Rigor 15/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 8/10 · Acceso 6/10
- **DOI / ISBN / URL:** ISBN: 978-1-108-79289-9 · https://en.wikipedia.org/wiki/Deflated_Sharpe_ratio (bibliografía)
- **Acceso y licencia:** Libro de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Sharpe ratio" en.wikipedia.org deflated Sharpe ratio»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Deflated_Sharpe_ratio)
- **Contenido:** Aplica aprendizaje no supervisado y supervisado a la gestión de carteras: limpieza de matrices de covarianza, métricas de distancia, agrupamiento, importancia de variables y control de pruebas múltiples.
- **Uso en el Motor:** MC-06, MC-05: limpieza de covarianzas y agrupamiento de estrategias antes de optimizar carteras.
- **Limitaciones:** Autor vinculado a la industria; algunas recetas con evidencia empírica limitada.

#### DOC-MOT-0414 · Q 76 (B) — The 10 Reasons Most Machine Learning Funds Fail

- **Autores:** Marcos López de Prado
- **Año:** 2018
- **Publicación o institución:** The Journal of Portfolio Management, 44(6), 120-133
- **Tipo de documento:** Artículo revisado por pares (profesional)
- **Temática:** TM-10 Aprendizaje automático para finanzas (principal) · secundarias: TM-11, TM-14
- **Calidad Q:** 76 (B) — Tipo 22/25 · Rigor 12/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 7/10 · Independencia 7/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.3905/jpm.2018.44.6.120 · https://en.wikipedia.org/wiki/Deflated_Sharpe_ratio (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Sharpe ratio" en.wikipedia.org deflated Sharpe ratio»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Deflated_Sharpe_ratio)
- **Contenido:** Enumera los errores habituales al aplicar aprendizaje automático a la inversión (muestreo cronológico, diferenciación integral, etiquetado ingenuo, fuga en validación cruzada, backtests sobreajustados) y sus remedios.
- **Uso en el Motor:** MC-06, MC-10: lista de comprobación de errores metodológicos antes de aceptar un modelo predictivo.
- **Limitaciones:** Texto de posición de un autor de la industria; poca evidencia empírica formal.

#### DOC-MOT-0410 · Q 70 (B) — Confronting Machine Learning With Financial Research

- **Autores:** Kristof Lommers; Ouns El Harzli; Jack Kim
- **Año:** 2021
- **Publicación o institución:** arXiv 2103.00366 (Universidad de Oxford, Oxford-Man Institute of Quantitative Finance; Data Capital Management)
- **Tipo de documento:** Documento de trabajo (preprint)
- **Temática:** TM-10 Aprendizaje automático para finanzas (principal) · secundarias: TM-04, TM-14
- **Calidad Q:** 70 (B) — Tipo 15/25 · Rigor 12/20 · Autoridad 10/15 · Vigencia 10/10 · Impacto 5/10 · Independencia 8/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://arxiv.org/pdf/2103.00366
- **Acceso y licencia:** Acceso abierto (arXiv)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Kelly Xiu "Financial Machine Learning" Foundations and Trends in Finance 2023» —resultado relacionado—; WebFetch: sí)
- **Contenido:** Analiza por qué los datos financieros (baja relación señal-ruido, no estacionariedad, muestras cortas) y las normas de la investigación social exigen adaptar el aprendizaje automático, y lo sitúa como complemento del econometra en estimación, contraste, inferencia causal y predicción.
- **Uso en el Motor:** MC-06: lista de comprobación conceptual de los riesgos de aplicar aprendizaje automático genérico a datos de mercado.
- **Limitaciones:** Preprint sin revisión por pares constatada; año inferido del identificador arXiv (marzo de 2021); uno de los autores procede de la industria.

<!-- Segunda tanda (2026-11-02): cupo de 25 WebSearch agotado. Fichas con «VERIFICADO_BUSQUEDA» y WebFetch sobre «página índice»: metadatos (autores, año, título, revista, páginas y, cuando figura, DOI) confirmados en la bibliografía de una página índice leída (Wikipedia, IDEAS/RePEc, bibliografía de un artículo o manual de software); la página propia de la obra no se ha cargado. Los DOI solo se incluyen si aparecían en la página leída. -->

## TM-11 Evaluación predictiva y backtesting

#### DOC-MOT-0095 · Q 96 (A) — Strictly Proper Scoring Rules, Prediction, and Estimation

- **Autores:** Tilmann Gneiting; Adrian E. Raftery
- **Año:** 2007
- **Publicación o institución:** Journal of the American Statistical Association, 102, 359-378
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-11 Evaluación predictiva y backtesting (principal) · secundarias: —
- **Calidad Q:** 96 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1198/016214506000001437 · https://en.wikipedia.org/wiki/Brier_score (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor; copia del autor en sites.stat.washington.edu
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Brier score" en.wikipedia.org»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Brier_score)
- **Contenido:** Teoría general de las reglas de puntuación estrictamente propias (Brier, logarítmica, CRPS, puntuaciones de energía e intervalos) y su uso para evaluar y estimar con pronósticos probabilísticos.
- **Uso en el Motor:** MC-10: reglas de puntuación propias (Brier, logarítmica, CRPS) para pronósticos probabilísticos.
- **Limitaciones:** Marco teórico; elegir la regla según el uso. El número de fascículo no se confirma (la fuente consultada lo transcribe de forma distinta a la semilla).

#### DOC-MOT-0103 · Q 95 (A) — … and the Cross-Section of Expected Returns

- **Autores:** Campbell R. Harvey; Yan Liu; Heqing Zhu
- **Año:** 2016
- **Publicación o institución:** The Review of Financial Studies, 29(1), 5-68
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-11 Evaluación predictiva y backtesting (principal) · secundarias: TM-07
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1093/rfs/hhv059 · https://academicnewsletter.sufe.edu.cn/info/353765
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Harvey Liu Zhu "and the Cross-Section of Expected Returns" probability of backtest overfitting»; WebFetch: sí)
- **Contenido:** Recopila más de 300 factores publicados y aplica correcciones por pruebas múltiples; propone exigir t > 3 a los nuevos factores.
- **Uso en el Motor:** MC-10: umbral t > 3 para nuevos factores por contraste múltiple.
- **Limitaciones:** Umbral orientativo, dependiente del supuesto de pruebas no publicadas. Volumen/fascículo tomados de la semilla (la página leída solo mostraba revista, año, DOI y página inicial 5).

#### DOC-MOT-0094 · Q 95 (A) — Approximately Normal Tests for Equal Predictive Accuracy in Nested Models

- **Autores:** Todd E. Clark; Kenneth D. West
- **Año:** 2007
- **Publicación o institución:** Journal of Econometrics, 138(1), 291-311 (versión previa: NBER Technical Working Paper 326, 2006)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-11 Evaluación predictiva y backtesting (principal) · secundarias: —
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI WP: 10.3386/t0326 · https://www.nber.org/papers/t0326
- **Acceso y licencia:** Documento de trabajo NBER de acceso abierto; artículo de revista de pago
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Clark West 2007 "Approximately normal tests for equal predictive accuracy in nested models" Journal of Econometrics»; WebFetch: sí)
- **Contenido:** Ajusta el diferencial de error cuadrático para comparar un modelo con su versión anidada (p. ej., señal frente a paseo aleatorio) con valores críticos aproximadamente normales.
- **Uso en el Motor:** MC-10: comparación de modelos anidados (señal frente a paseo aleatorio).
- **Limitaciones:** Específico de pérdida cuadrática. Cita de revista confirmada en la bibliografía del paquete R pretest; el DOI de revista de la semilla no se ha visto y se retira.

#### DOC-MOT-0093 · Q 95 (A) — Tests of Conditional Predictive Ability

- **Autores:** Raffaella Giacomini; Halbert White
- **Año:** 2006
- **Publicación o institución:** Econometrica, 74(6), 1545-1578
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-11 Evaluación predictiva y backtesting (principal) · secundarias: —
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1111/j.1468-0262.2006.00718.x · https://ideas.repec.org:443/a/ecm/emetrp/v74y2006i6p1545-1578.html
- **Acceso y licencia:** Artículo de pago en el editor; versiones de trabajo de 2003 en RePEc
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Giacomini White 2006 "Tests of Conditional Predictive Ability" Econometrica Clark West nested»; WebFetch: sí)
- **Contenido:** Contraste de capacidad predictiva condicional que compara métodos de pronóstico (modelo más ventana de estimación) y admite modelos anidados con ventanas móviles.
- **Uso en el Motor:** MC-10: contraste de capacidad predictiva condicional con ventanas móviles.
- **Limitaciones:** Requiere ventana de estimación limitada.

#### DOC-MOT-0099 · Q 95 (A) — A Reality Check for Data Snooping

- **Autores:** Halbert White
- **Año:** 2000
- **Publicación o institución:** Econometrica, 68(5), 1097-1126
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-11 Evaluación predictiva y backtesting (principal) · secundarias: TM-01
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1111/1468-0262.00152 · https://www.econometricsociety.org/publications/econometrica/2000/09/01/reality-check-data-snooping
- **Acceso y licencia:** Página de la Econometric Society (resumen abierto); texto completo para miembros o suscriptores
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «"Data dredging" wikipedia data snooping White reality check»; WebFetch: sí)
- **Contenido:** Contraste bootstrap de si el mejor de muchos modelos supera a una referencia, corrigiendo la búsqueda de especificaciones (data snooping).
- **Uso en el Motor:** MC-10: contraste del mejor modelo frente a referencia corrigiendo la búsqueda de especificaciones.
- **Limitaciones:** Conservador con modelos irrelevantes (véase Hansen 2005, DOC-MOT-0100).

#### DOC-MOT-0091 · Q 95 (A) — Comparing Predictive Accuracy

- **Autores:** Francis X. Diebold; Roberto S. Mariano
- **Año:** 1995
- **Publicación o institución:** Journal of Business & Economic Statistics, 13(3), 253-263
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-11 Evaluación predictiva y backtesting (principal) · secundarias: —
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1080/07350015.1995.10524599 · https://pkg.robjhyndman.com/forecast/reference/dm.test.html
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Diebold Mariano test wikipedia»; WebFetch: sí, sobre la página índice https://pkg.robjhyndman.com/forecast/reference/dm.test.html)
- **Contenido:** Propone el contraste DM de igualdad de precisión predictiva entre dos pronósticos con funciones de pérdida generales y errores autocorrelacionados.
- **Uso en el Motor:** MC-10: contraste DM de igualdad de precisión predictiva.
- **Limitaciones:** No válido para modelos anidados (usar Clark-West, DOC-MOT-0094). DOI confirmado en https://en.wikipedia.org/wiki/Mean_absolute_scaled_error.

#### DOC-MOT-0098 · Q 95 (A) — A New Vector Partition of the Probability Score

- **Autores:** Allan H. Murphy
- **Año:** 1973
- **Publicación o institución:** Journal of Applied Meteorology, 12(4), 595-600
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-11 Evaluación predictiva y backtesting (principal) · secundarias: —
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI: 10.1175/1520-0450(1973)012<0595:ANVPOT>2.0.CO;2 · https://en.wikipedia.org/wiki/Brier_score (bibliografía)
- **Acceso y licencia:** Página del editor (AMS)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Brier score" en.wikipedia.org»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Brier_score)
- **Contenido:** Descompone la puntuación de Brier en fiabilidad (calibración), resolución e incertidumbre.
- **Uso en el Motor:** MC-10: descomposición de Brier en fiabilidad, resolución e incertidumbre.
- **Limitaciones:** Requiere agrupar probabilidades; sesgo en muestras pequeñas (véase DOC-MOT-0422).

#### DOC-MOT-0096 · Q 94 (A) — Probabilistic Forecasts, Calibration and Sharpness

- **Autores:** Tilmann Gneiting; Fadoua Balabdaoui; Adrian E. Raftery
- **Año:** 2007
- **Publicación o institución:** Journal of the Royal Statistical Society, Series B, 69(2), 243-268
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-11 Evaluación predictiva y backtesting (principal) · secundarias: TM-01
- **Calidad Q (provisional):** 94 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1111/j.1467-9868.2007.00587.x (DOI a verificar)
- **Estado:** PENDIENTE_VERIFICACION_ALTA
- **Estado del enlace:** PENDIENTE_BARRIDO
- **Última verificación:** — (sin verificar)
- **Uso en el Motor:** MC-10: paradigma «maximizar la nitidez sujeta a calibración»; histogramas PIT.
- **Limitaciones:** Requiere muestras amplias.
- **Origen:** Semilla V3.0 (2026-11-01) para cubrir lagunas; DOC-M la verifica en su primer barrido (HT-02: DOI, metadatos, acceso, retractaciones) y la confirma, repara o da de baja.

#### DOC-MOT-0097 · Q 94 (A) — Verification of Forecasts Expressed in Terms of Probability

- **Autores:** Glenn W. Brier
- **Año:** 1950
- **Publicación o institución:** Monthly Weather Review, 78(1), 1-3
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-11 Evaluación predictiva y backtesting (principal) · secundarias: —
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI: 10.1175/1520-0493(1950)078<0001:VOFEIT>2.0.CO;2 · https://journals.ametsoc.org/view/journals/mwre/78/1/1520-0493_1950_078_0001_vofeit_2_0_co_2.xml
- **Acceso y licencia:** Página del editor (AMS); copia archivada de NOAA en web.archive.org
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Brier score" en.wikipedia.org»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Brier_score)
- **Contenido:** Define la puntuación de Brier (error cuadrático medio de las probabilidades) para verificar pronósticos probabilísticos de eventos categóricos.
- **Uso en el Motor:** MC-10: puntuación de Brier, base del certificado de horizonte (R13).
- **Limitaciones:** Solo eventos binarios o categóricos.

#### DOC-MOT-0105 · Q 93 (A) — Another Look at Measures of Forecast Accuracy

- **Autores:** Rob J. Hyndman; Anne B. Koehler
- **Año:** 2006
- **Publicación o institución:** International Journal of Forecasting, 22(4), 679-688
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-11 Evaluación predictiva y backtesting (principal) · secundarias: —
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1016/j.ijforecast.2006.03.001 · https://en.wikipedia.org/wiki/Mean_absolute_scaled_error (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Mean absolute scaled error" en.wikipedia.org Hyndman Koehler»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Mean_absolute_scaled_error)
- **Contenido:** Revisa las medidas de error de pronóstico, critica MAPE y medidas relativas, y propone el error absoluto medio escalado (MASE).
- **Uso en el Motor:** MC-10: MASE y crítica de MAPE para comparar errores entre series.
- **Limitaciones:** Medidas puntuales, no probabilísticas.

#### DOC-MOT-0100 · Q 93 (A) — A Test for Superior Predictive Ability

- **Autores:** Peter Reinhard Hansen
- **Año:** 2005
- **Publicación o institución:** Journal of Business & Economic Statistics
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-11 Evaluación predictiva y backtesting (principal) · secundarias: TM-01
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** https://en.wikipedia.org/wiki/Peter_Reinhard_Hansen (lista de publicaciones)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Peter Reinhard Hansen IDEAS RePEc "A Test for Superior Predictive Ability"»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Peter_Reinhard_Hansen)
- **Contenido:** Contraste SPA: versión estudentizada y recentrada del Reality Check, más potente y menos sensible a modelos irrelevantes.
- **Uso en el Motor:** MC-10: contraste SPA, más potente que el Reality Check.
- **Limitaciones:** Requiere bootstrap estacionario. Solo se han confirmado autor, año, título y revista; volumen, páginas y DOI de la semilla quedan sin confirmar y se retiran.

#### DOC-MOT-0092 · Q 92 (A) — Testing the Equality of Prediction Mean Squared Errors

- **Autores:** David Harvey; Stephen Leybourne; Paul Newbold
- **Año:** 1997
- **Publicación o institución:** International Journal of Forecasting, 13(2), 281-291
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-11 Evaluación predictiva y backtesting (principal) · secundarias: —
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** https://pkg.robjhyndman.com/forecast/reference/dm.test.html (bibliografía de la función dm.test)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Diebold Mariano test wikipedia»; WebFetch: sí, sobre la página índice https://pkg.robjhyndman.com/forecast/reference/dm.test.html)
- **Contenido:** Corrección de muestra pequeña del contraste DM y uso de la distribución t de Student.
- **Uso en el Motor:** MC-10: corrección de muestra pequeña del contraste DM.
- **Limitaciones:** Mismas limitaciones que DM. El DOI de la semilla no se ha visto en la verificación y se retira.

#### DOC-MOT-0426 · Q 89 (A) — Consistent Ranking of Volatility Models

- **Autores:** Peter Reinhard Hansen; Asger Lunde
- **Año:** 2006
- **Publicación o institución:** Journal of Econometrics, 131, 97-121
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-11 Evaluación predictiva y backtesting (principal) · secundarias: TM-03
- **Calidad Q:** 89 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** https://en.wikipedia.org/wiki/Peter_Reinhard_Hansen (lista de publicaciones)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Peter Reinhard Hansen IDEAS RePEc "A Test for Superior Predictive Ability"»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Peter_Reinhard_Hansen)
- **Contenido:** Muestra que, con proxies ruidosos de la volatilidad, algunas funciones de pérdida ordenan mal los modelos y caracteriza las que dan rankings consistentes.
- **Uso en el Motor:** MC-10, MC-03: elección de pérdida (p. ej., QLIKE, MSE) al comparar pronósticos de volatilidad.
- **Limitaciones:** Sin DOI en la fuente consultada.

#### DOC-MOT-0102 · Q 88 (A) — The Probability of Backtest Overfitting

- **Autores:** David H. Bailey; Jonathan M. Borwein; Marcos López de Prado; Qiji Jim Zhu
- **Año:** 2015 (versión SSRN revisada; publicación en Journal of Computational Finance)
- **Publicación o institución:** Journal of Computational Finance (Risk Journals); SSRN 2326253
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-11 Evaluación predictiva y backtesting (principal) · secundarias: —
- **Calidad Q:** 88 (A) — Tipo 22/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 9/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI SSRN: 10.2139/ssrn.2326253 · https://papers.ssrn.com/abstract=2326253
- **Acceso y licencia:** Documento SSRN gratuito; artículo de revista de pago
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Harvey Liu Zhu "and the Cross-Section of Expected Returns" probability of backtest overfitting»; WebFetch: sí)
- **Contenido:** Define la probabilidad de sobreajuste del backtest (PBO) y la estima con validación cruzada simétrica combinatoria (CSCV).
- **Uso en el Motor:** MC-10: probabilidad de sobreajuste (PBO) mediante validación cruzada simétrica combinatoria.
- **Limitaciones:** Coste computacional. Volumen, páginas y DOI de revista de la semilla no confirmados (SSRN lo daba como «forthcoming»); se retiran.

#### DOC-MOT-0423 · Q 88 (A) — Comparing Predictive Accuracy, Twenty Years Later: A Personal Perspective on the Use and Abuse of Diebold-Mariano Tests

- **Autores:** Francis X. Diebold
- **Año:** 2015
- **Publicación o institución:** Journal of Business & Economic Statistics, 33(1), 1
- **Tipo de documento:** Artículo revisado por pares (con discusión)
- **Temática:** TM-11 Evaluación predictiva y backtesting (principal) · secundarias: —
- **Calidad Q:** 88 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.1080/07350015.2014.983236 · https://en.wikipedia.org/wiki/Mean_absolute_scaled_error (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Mean absolute scaled error" en.wikipedia.org Hyndman Koehler»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Mean_absolute_scaled_error)
- **Contenido:** El propio autor delimita el uso correcto del contraste DM (comparar pronósticos, no modelos) y advierte contra su abuso en la selección de modelos.
- **Uso en el Motor:** MC-10: criterios para decidir cuándo aplicar DM y cuándo contrastes de modelos.
- **Limitaciones:** Ensayo de posición; las páginas finales no figuran en la fuente.

#### DOC-MOT-0104 · Q 88 (A) — The Statistics of Sharpe Ratios

- **Autores:** Andrew W. Lo
- **Año:** 2002
- **Publicación o institución:** Financial Analysts Journal, 58(4), 36-52
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-11 Evaluación predictiva y backtesting (principal) · secundarias: TM-07
- **Calidad Q:** 88 (A) — Tipo 22/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 9/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.2469/faj.v58.n4.2453 · https://en.wikipedia.org/wiki/Sharpe_ratio (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Sharpe ratio" en.wikipedia.org deflated Sharpe ratio»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Sharpe_ratio)
- **Contenido:** Deriva la distribución muestral del ratio de Sharpe con rentabilidades IID y autocorrelacionadas y muestra que la anualización por raíz del tiempo puede sesgarlo mucho.
- **Uso en el Motor:** MC-10: error estándar del Sharpe y anualización con autocorrelación.
- **Limitaciones:** Supuestos asintóticos.

#### DOC-MOT-0416 · Q 88 (A) — Performance Hypothesis Testing with the Sharpe and Treynor Measures

- **Autores:** J. D. Jobson; Bob M. Korkie
- **Año:** 1981
- **Publicación o institución:** The Journal of Finance, 36(4), 888-908
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-11 Evaluación predictiva y backtesting (principal) · secundarias: TM-07
- **Calidad Q:** 88 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.1111/j.1540-6261.1981.tb04891.x · https://en.wikipedia.org/wiki/Sharpe_ratio (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Sharpe ratio" en.wikipedia.org deflated Sharpe ratio»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Sharpe_ratio)
- **Contenido:** Primer contraste formal de igualdad de ratios de Sharpe y Treynor entre dos carteras, con su distribución asintótica.
- **Uso en el Motor:** MC-10: contraste de diferencias de Sharpe entre estrategias.
- **Limitaciones:** Supone normalidad IID; véanse correcciones posteriores (Lo 2002, DOC-MOT-0104).

#### DOC-MOT-0420 · Q 87 (A) — Sampling Distributions of the Brier Score and Brier Skill Score under Serial Dependence

- **Autores:** Daniel S. Wilks
- **Año:** 2010
- **Publicación o institución:** Quarterly Journal of the Royal Meteorological Society, 136, 2109-2118
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-11 Evaluación predictiva y backtesting (principal) · secundarias: —
- **Calidad Q:** 87 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 7/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.1002/qj.709 · https://en.wikipedia.org/wiki/Brier_score (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Brier score" en.wikipedia.org»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Brier_score)
- **Contenido:** Deriva la varianza muestral del Brier y del Brier skill score cuando los pronósticos están autocorrelacionados, y muestra que ignorarlo exagera la significación.
- **Uso en el Motor:** MC-10: intervalos de confianza del Brier con pronósticos solapados o persistentes.
- **Limitaciones:** Modelo de dependencia de primer orden.

#### DOC-MOT-0415 · Q 86 (A) — Pseudo-Mathematics and Financial Charlatanism: The Effects of Backtest Overfitting on Out-of-Sample Performance

- **Autores:** David H. Bailey; Jonathan M. Borwein; Marcos López de Prado (autoría según la bibliografía consultada)
- **Año:** 2014
- **Publicación o institución:** Notices of the American Mathematical Society, 61(5), 458-471
- **Tipo de documento:** Artículo revisado por pares (divulgación técnica)
- **Temática:** TM-11 Evaluación predictiva y backtesting (principal) · secundarias: —
- **Calidad Q:** 86 (A) — Tipo 22/25 · Rigor 14/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 9/10 · Acceso 9/10
- **DOI / ISBN / URL:** https://en.wikipedia.org/wiki/Deflated_Sharpe_ratio (bibliografía)
- **Acceso y licencia:** Acceso abierto en la revista de la AMS
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Sharpe ratio" en.wikipedia.org deflated Sharpe ratio»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Deflated_Sharpe_ratio)
- **Contenido:** Muestra que, con pocas observaciones y muchas configuraciones probadas, es casi seguro encontrar un backtest con Sharpe alto sin capacidad predictiva, y propone la longitud mínima de backtest.
- **Uso en el Motor:** MC-10: longitud mínima de backtest y advertencia sobre el número de configuraciones probadas.
- **Limitaciones:** Texto divulgativo; resultados bajo supuestos simplificados.

#### DOC-MOT-0427 · Q 85 (A) — A Novel Approach to Predictive Accuracy Testing in Nested Environments

- **Autores:** Jean-Yves Pitarakis
- **Año:** 2023
- **Publicación o institución:** Econometric Theory (Cambridge University Press), publicado en línea
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-11 Evaluación predictiva y backtesting (principal) · secundarias: —
- **Calidad Q:** 85 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 4/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1017/S0266466623000154 · https://resolve.cambridge.org/core/services/aop-cambridge-core/content/view/0B4D706CDA6D4A2C883C3BDF397DCB18/S0266466623000154a.pdf/a-novel-approach-to-predictive-accuracy-testing-in-nested-environments.pdf
- **Acceso y licencia:** PDF en Cambridge Core (acceso según licencia); implementado en el paquete R pretest
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Clark West 2007 "Approximately normal tests for equal predictive accuracy in nested models" Journal of Econometrics»; WebFetch: sí, sobre la página índice https://cran.r-universe.dev/pretest/doc/manual.html)
- **Contenido:** Propone estadísticos de precisión predictiva para modelos anidados con distribución normal estándar que evitan la degeneración del contraste en el nulo.
- **Uso en el Motor:** MC-10: alternativa moderna a Clark-West para señal frente a referencia anidada.
- **Limitaciones:** Reciente, poca adopción; volumen y páginas no confirmados.

#### DOC-MOT-0101 · Q 85 (A) — The Deflated Sharpe Ratio: Correcting for Selection Bias, Backtest Overfitting, and Non-Normality

- **Autores:** David H. Bailey; Marcos López de Prado
- **Año:** 2014
- **Publicación o institución:** The Journal of Portfolio Management, 40(5), 94-107
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-11 Evaluación predictiva y backtesting (principal) · secundarias: TM-07
- **Calidad Q:** 85 (A) — Tipo 22/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 8/10 · Acceso 5/10
- **DOI / ISBN / URL:** https://en.wikipedia.org/wiki/Deflated_Sharpe_ratio (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Sharpe ratio" en.wikipedia.org deflated Sharpe ratio»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Deflated_Sharpe_ratio)
- **Contenido:** Ajusta el Sharpe observado por el número de estrategias probadas, la asimetría y la curtosis para estimar la probabilidad de que el Sharpe verdadero sea positivo.
- **Uso en el Motor:** MC-10: Sharpe deflactado por número de ensayos, asimetría y curtosis.
- **Limitaciones:** Requiere estimar el número efectivo de ensayos. El DOI de la semilla no se ha visto en la verificación y se retira.

#### DOC-MOT-0421 · Q 85 (A) — Scoring Rules for Forecast Verification

- **Autores:** Riccardo Benedetti
- **Año:** 2010
- **Publicación o institución:** Monthly Weather Review, 138(1), 203-211
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-11 Evaluación predictiva y backtesting (principal) · secundarias: —
- **Calidad Q:** 85 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 12/15 · Vigencia 10/10 · Impacto 6/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1175/2009MWR2945.1 · https://en.wikipedia.org/wiki/Brier_score (bibliografía)
- **Acceso y licencia:** Página del editor (AMS)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Brier score" en.wikipedia.org»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Brier_score)
- **Contenido:** Caracteriza axiomáticamente las reglas de puntuación aceptables para verificar pronósticos probabilísticos y defiende la puntuación logarítmica.
- **Uso en el Motor:** MC-10: justificación de la elección entre puntuación logarítmica y Brier.
- **Limitaciones:** Enfoque axiomático; no trata pronósticos continuos.

#### DOC-MOT-0422 · Q 83 (A) — A Bias-Corrected Decomposition of the Brier Score

- **Autores:** Christopher A. T. Ferro; Thomas E. Fricker
- **Año:** 2012
- **Publicación o institución:** Quarterly Journal of the Royal Meteorological Society, 138(668), 1954-1960
- **Tipo de documento:** Artículo revisado por pares (nota)
- **Temática:** TM-11 Evaluación predictiva y backtesting (principal) · secundarias: —
- **Calidad Q:** 83 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 12/15 · Vigencia 10/10 · Impacto 6/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** https://en.wikipedia.org/wiki/Brier_score (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Brier score" en.wikipedia.org»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Brier_score)
- **Contenido:** Corrige el sesgo de muestra finita de la descomposición de Murphy en fiabilidad y resolución.
- **Uso en el Motor:** MC-10: descomposición de Brier con pocas observaciones por intervalo de probabilidad.
- **Limitaciones:** Sin DOI en la fuente consultada.

#### DOC-MOT-0425 · Q 82 (A) — A Note on the Mean Absolute Scaled Error

- **Autores:** Philip Hans Franses
- **Año:** 2016
- **Publicación o institución:** International Journal of Forecasting, 32(1), 20-22
- **Tipo de documento:** Artículo revisado por pares (nota)
- **Temática:** TM-11 Evaluación predictiva y backtesting (principal) · secundarias: —
- **Calidad Q:** 82 (A) — Tipo 23/25 · Rigor 13/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 5/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI: 10.1016/j.ijforecast.2015.03.008 · https://en.wikipedia.org/wiki/Mean_absolute_scaled_error (bibliografía; handle 1765/78815)
- **Acceso y licencia:** Artículo de pago; copia en repositorio institucional (hdl 1765/78815)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Mean absolute scaled error" en.wikipedia.org Hyndman Koehler»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Mean_absolute_scaled_error)
- **Contenido:** Muestra que el MASE se puede interpretar como contraste frente al pronóstico ingenuo y comenta sus propiedades.
- **Uso en el Motor:** MC-10: interpretación del MASE como mejora sobre el paseo aleatorio.
- **Limitaciones:** Nota breve.

#### DOC-MOT-0418 · Q 82 (A) — The Sharpe Ratio Efficient Frontier

- **Autores:** David H. Bailey; Marcos López de Prado
- **Año:** 2012
- **Publicación o institución:** Journal of Risk, 15(2) (SSRN 1821643)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-11 Evaluación predictiva y backtesting (principal) · secundarias: TM-07
- **Calidad Q:** 82 (A) — Tipo 22/25 · Rigor 15/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 7/10 · Independencia 8/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.21314/JOR.2012.255 · https://en.wikipedia.org/wiki/Deflated_Sharpe_ratio (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor; versión SSRN gratuita
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Sharpe ratio" en.wikipedia.org deflated Sharpe ratio»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Deflated_Sharpe_ratio)
- **Contenido:** Introduce el ratio de Sharpe probabilístico (PSR) y la longitud mínima de registro necesaria para confiar en un Sharpe dado con rentabilidades no normales.
- **Uso en el Motor:** MC-10: PSR y longitud mínima del historial antes de aceptar una estrategia.
- **Limitaciones:** Supuestos de estacionariedad e independencia aproximada.

#### DOC-MOT-0424 · Q 81 (A) — Accuracy Measures: Theoretical and Practical Concerns

- **Autores:** Spyros Makridakis
- **Año:** 1993
- **Publicación o institución:** International Journal of Forecasting, 9(4), 527-529
- **Tipo de documento:** Artículo revisado por pares (nota)
- **Temática:** TM-11 Evaluación predictiva y backtesting (principal) · secundarias: —
- **Calidad Q:** 81 (A) — Tipo 23/25 · Rigor 12/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.1016/0169-2070(93)90079-3 · https://en.wikipedia.org/wiki/Mean_absolute_scaled_error (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Mean absolute scaled error" en.wikipedia.org Hyndman Koehler»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Mean_absolute_scaled_error)
- **Contenido:** Discute las propiedades y sesgos de las medidas de precisión (MAPE simétrico, asimetrías) y su elección práctica.
- **Uso en el Motor:** MC-10: criterios de elección de medida de error puntual.
- **Limitaciones:** Nota breve, superada en parte por Hyndman-Koehler (DOC-MOT-0105).

#### DOC-MOT-0419 · Q 78 (B) — Detection of False Investment Strategies Using Unsupervised Learning Methods

- **Autores:** Marcos López de Prado; Michael J. Lewis
- **Año:** 2019
- **Publicación o institución:** Quantitative Finance, 19(9), 1555-1565
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-11 Evaluación predictiva y backtesting (principal) · secundarias: TM-10
- **Calidad Q:** 78 (B) — Tipo 22/25 · Rigor 14/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 6/10 · Independencia 8/10 · Acceso 5/10
- **DOI / ISBN / URL:** https://en.wikipedia.org/wiki/Deflated_Sharpe_ratio (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Sharpe ratio" en.wikipedia.org deflated Sharpe ratio»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Deflated_Sharpe_ratio)
- **Contenido:** Estima el número efectivo de ensayos independientes agrupando estrategias probadas, para aplicar después el Sharpe deflactado.
- **Uso en el Motor:** MC-10: estimar el número efectivo de ensayos que exige DOC-MOT-0101.
- **Limitaciones:** Depende del algoritmo de agrupamiento elegido.

#### DOC-MOT-0417 · Q 76 (B) — Being Honest in Backtest Reporting: A Template for Disclosing Multiple Tests

- **Autores:** Frank J. Fabozzi; Marcos López de Prado
- **Año:** 2018
- **Publicación o institución:** The Journal of Portfolio Management, 45(1), 141-147
- **Tipo de documento:** Artículo revisado por pares (profesional)
- **Temática:** TM-11 Evaluación predictiva y backtesting (principal) · secundarias: TM-14
- **Calidad Q:** 76 (B) — Tipo 22/25 · Rigor 12/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 6/10 · Independencia 8/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.3905/jpm.2018.45.1.141 · https://en.wikipedia.org/wiki/Deflated_Sharpe_ratio (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Sharpe ratio" en.wikipedia.org deflated Sharpe ratio»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Deflated_Sharpe_ratio)
- **Contenido:** Propone una plantilla para declarar el número de pruebas, su correlación y el Sharpe deflactado al presentar un backtest.
- **Uso en el Motor:** MC-10, MC-08: plantilla de información obligatoria en los artefactos de backtest del Motor.
- **Limitaciones:** Propuesta normativa sin validación empírica.

## TM-12 Crecimiento, difusión y prospectiva cuantitativa

#### DOC-MOT-0110 · Q 93 (A) — Statistical Basis for Predicting Technological Progress

- **Autores:** Béla Nagy; J. Doyne Farmer; Quan M. Bui; Jessika E. Trancik
- **Año:** 2013
- **Publicación o institución:** PLoS ONE, 8(2), e52669
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-12 Crecimiento, difusión y prospectiva cuantitativa (principal) · secundarias: TM-11
- **Calidad Q:** 93 (A) — Tipo 23/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** DOI: 10.1371/journal.pone.0052669 · https://en.wikipedia.org/wiki/Experience_curve_effect (bibliografía)
- **Acceso y licencia:** Acceso abierto (PLoS)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Experience curve effects" en.wikipedia.org Wright's law»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Experience_curve_effect)
- **Contenido:** Compara la capacidad predictiva de las leyes de Moore, Wright, Goddard y otras con datos de 62 tecnologías; Wright y Moore rinden de forma parecida.
- **Uso en el Motor:** MC-04: comparación de leyes de Moore y Wright con 62 tecnologías.
- **Limitaciones:** Base de datos histórica limitada.

#### DOC-MOT-0106 · Q 93 (A) — A New Product Growth for Model Consumer Durables

- **Autores:** Frank M. Bass
- **Año:** 1969
- **Publicación o institución:** Management Science, 15(5), 215-227
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-12 Crecimiento, difusión y prospectiva cuantitativa (principal) · secundarias: —
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1287/mnsc.15.5.215 · https://en.wikipedia.org/wiki/Bass_diffusion_model (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Bass diffusion model" en.wikipedia.org»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Bass_diffusion_model)
- **Contenido:** Modelo de difusión de Bass: la adopción combina innovación (coeficiente p) e imitación (q) y produce curvas S de ventas de bienes duraderos.
- **Uso en el Motor:** MC-04: modelo de difusión de Bass (innovación e imitación) para curvas S de adopción.
- **Limitaciones:** Mercado potencial fijo; pronósticos inestables con pocos datos iniciales.

#### DOC-MOT-0108 · Q 92 (A) — Hybrid Corn: An Exploration in the Economics of Technological Change

- **Autores:** Zvi Griliches
- **Año:** 1957
- **Publicación o institución:** Econometrica, 25(4), 501-522
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-12 Crecimiento, difusión y prospectiva cuantitativa (principal)
- **Calidad Q (provisional):** 92 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.2307/1905380 (DOI a verificar)
- **Estado:** PENDIENTE_VERIFICACION_ALTA
- **Estado del enlace:** PENDIENTE_BARRIDO
- **Última verificación:** — (sin verificar)
- **Uso en el Motor:** MC-04: ajuste logístico de la difusión y sus determinantes económicos.
- **Limitaciones:** Caso agrícola histórico.
- **Origen:** Semilla V3.0 (2026-11-01) para cubrir lagunas; DOC-M la verifica en su primer barrido (HT-02: DOI, metadatos, acceso, retractaciones) y la confirma, repara o da de baja.

#### DOC-MOT-0433 · Q 91 (A) — Why the Bass Model Fits without Decision Variables

- **Autores:** Frank M. Bass; Trichy V. Krishnan; Dipak C. Jain
- **Año:** 1994
- **Publicación o institución:** Marketing Science, 13(3), 203-223
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-12 Crecimiento, difusión y prospectiva cuantitativa (principal) · secundarias: —
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.1287/mksc.13.3.203 · https://en.wikipedia.org/wiki/Bass_diffusion_model (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Bass diffusion model" en.wikipedia.org»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Bass_diffusion_model)
- **Contenido:** Modelo de Bass generalizado con precio y publicidad; explica por qué el modelo simple ajusta bien cuando esas variables cambian de forma regular.
- **Uso en el Motor:** MC-04: incorporar precio o inversión en la curva de adopción.
- **Limitaciones:** Supone efectos porcentuales de las variables de decisión.

#### DOC-MOT-0111 · Q 90 (A) — How Predictable Is Technological Progress?

- **Autores:** J. Doyne Farmer; François Lafond
- **Año:** 2016
- **Publicación o institución:** Research Policy, 45(3), 647-665
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-12 Crecimiento, difusión y prospectiva cuantitativa (principal) · secundarias: —
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** https://arxiv.org/pdf/1703.05979 (bibliografía de Lafond et al., DOC-MOT-0428)
- **Acceso y licencia:** Artículo de pago en el editor; preprint en arXiv
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Experience curve effects" en.wikipedia.org Wright's law»; WebFetch: sí, sobre la página índice https://arxiv.org/pdf/1703.05979)
- **Contenido:** Modela el coste tecnológico como paseo aleatorio con deriva y autocorrelación y obtiene pronósticos probabilísticos validados fuera de muestra.
- **Uso en el Motor:** MC-04: pronósticos probabilísticos de costes tecnológicos con su incertidumbre.
- **Limitaciones:** Supone continuidad de la tendencia histórica. El DOI de la semilla no se ha visto y se retira.

#### DOC-MOT-0435 · Q 90 (A) — A Diffusion Theory Model of Adoption and Substitution for Successive Generations of High-Technology Products

- **Autores:** John A. Norton; Frank M. Bass
- **Año:** 1987
- **Publicación o institución:** Management Science, 33(9), 1069-1086
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-12 Crecimiento, difusión y prospectiva cuantitativa (principal) · secundarias: —
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.1287/mnsc.33.9.1069 · https://en.wikipedia.org/wiki/Bass_diffusion_model (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Bass diffusion model" en.wikipedia.org»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Bass_diffusion_model)
- **Contenido:** Extiende el modelo de Bass a generaciones sucesivas de tecnología que se sustituyen entre sí (p. ej., memorias DRAM).
- **Uso en el Motor:** MC-04: adopción por generaciones (sustitución tecnológica).
- **Limitaciones:** Mismos parámetros de difusión entre generaciones.

#### DOC-MOT-0430 · Q 90 (A) — The Economic Implications of Learning by Doing

- **Autores:** Kenneth J. Arrow
- **Año:** 1962
- **Publicación o institución:** The Review of Economic Studies, 155-173
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-12 Crecimiento, difusión y prospectiva cuantitativa (principal) · secundarias: —
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** https://arxiv.org/pdf/1703.05979 (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor (JSTOR/OUP)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Experience curve effects" en.wikipedia.org Wright's law»; WebFetch: sí, sobre la página índice https://arxiv.org/pdf/1703.05979)
- **Contenido:** Formaliza el aprendizaje por la práctica: la productividad crece con la experiencia acumulada (inversión acumulada), fundamento económico de las curvas de aprendizaje.
- **Uso en el Motor:** MC-04: base teórica de la relación coste-experiencia acumulada.
- **Limitaciones:** Modelo teórico agregado; volumen y DOI no figuran en la fuente consultada.

#### DOC-MOT-0112 · Q 89 (A) — Modelling and Forecasting the Diffusion of Innovation – A 25-Year Review

- **Autores:** Nigel Meade; Towhidul Islam
- **Año:** 2006
- **Publicación o institución:** International Journal of Forecasting, 22(3), 519-545
- **Tipo de documento:** Artículo de revisión revisado por pares
- **Temática:** TM-12 Crecimiento, difusión y prospectiva cuantitativa (principal) · secundarias: TM-11
- **Calidad Q:** 89 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** https://ideas.repec.org/a/eee/intfor/v22y2006i3p519-545.html
- **Acceso y licencia:** Artículo de pago en el editor (ScienceDirect); ficha abierta en RePEc
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Meade Islam 2006 "Modelling and forecasting the diffusion of innovation" 25-year review International Journal of Forecasting»; WebFetch: sí)
- **Contenido:** Revisa 25 años de modelos de difusión (Bass y extensiones, multigeneración, multinacionales, estimación) y su capacidad predictiva.
- **Uso en el Motor:** MC-04: revisión de modelos de difusión y su capacidad predictiva.
- **Limitaciones:** Revisión anterior a 2006. El DOI de la semilla no aparecía en la página leída y se retira.

#### DOC-MOT-0440 · Q 89 (A) — Technical Change and the Rate of Imitation

- **Autores:** Edwin Mansfield
- **Año:** 1961
- **Publicación o institución:** Econometrica, 741-766
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-12 Crecimiento, difusión y prospectiva cuantitativa (principal) · secundarias: —
- **Calidad Q:** 89 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** https://arxiv.org/pdf/2602.19488 (bibliografía de DOC-MOT-0429)
- **Acceso y licencia:** Artículo de pago en el editor (JSTOR)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Meade Islam 2006 "Modelling and forecasting the diffusion of innovation" 25-year review International Journal of Forecasting»; WebFetch: sí, sobre la página índice https://arxiv.org/pdf/2602.19488)
- **Contenido:** Modelo logístico de imitación entre empresas: la velocidad de difusión aumenta con la rentabilidad de la innovación y disminuye con la inversión requerida.
- **Uso en el Motor:** MC-04: determinantes económicos de la velocidad de adopción empresarial.
- **Limitaciones:** Datos industriales históricos de EE. UU.; volumen no indicado en la fuente.

#### DOC-MOT-0445 · Q 88 (A) — Bias and Systematic Change in the Parameter Estimates of Macro-Level Diffusion Models

- **Autores:** Christophe Van den Bulte; Gary L. Lilien
- **Año:** 1997
- **Publicación o institución:** Marketing Science, 16(4), 338-353
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-12 Crecimiento, difusión y prospectiva cuantitativa (principal) · secundarias: TM-11
- **Calidad Q:** 88 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 7/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** https://ideas.repec.org/a/eee/intfor/v22y2006i3p519-545.html (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Meade Islam 2006 "Modelling and forecasting the diffusion of innovation" 25-year review International Journal of Forecasting»; WebFetch: sí, sobre la página índice https://ideas.repec.org/a/eee/intfor/v22y2006i3p519-545.html)
- **Contenido:** Documenta que los parámetros del modelo de Bass estimados con datos truncados están sesgados y derivan con el tamaño de la muestra.
- **Uso en el Motor:** MC-04: advertencia sobre pronósticos tempranos de mercado potencial.
- **Limitaciones:** Centrado en mínimos cuadrados no lineales.

#### DOC-MOT-0434 · Q 88 (A) — Diffusion of New Products: Empirical Generalizations and Managerial Uses

- **Autores:** Vijay Mahajan; Eitan Muller; Frank M. Bass
- **Año:** 1995
- **Publicación o institución:** Marketing Science, 14(3), G79-G88
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-12 Crecimiento, difusión y prospectiva cuantitativa (principal) · secundarias: —
- **Calidad Q:** 88 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.1287/mksc.14.3.G79 · https://en.wikipedia.org/wiki/Bass_diffusion_model (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Bass diffusion model" en.wikipedia.org»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Bass_diffusion_model)
- **Contenido:** Sintetiza regularidades empíricas de la difusión (valores típicos de p y q, momento del pico de ventas) y sus usos en decisiones.
- **Uso en el Motor:** MC-04: valores de referencia de p y q como priors.
- **Limitaciones:** Muestras de bienes de consumo de EE. UU.

#### DOC-MOT-0438 · Q 88 (A) — New Product Diffusion Models in Marketing: A Review and Directions for Research

- **Autores:** Vijay Mahajan; Eitan Muller; Frank M. Bass
- **Año:** 1990
- **Publicación o institución:** Journal of Marketing, 54(1), 1-26
- **Tipo de documento:** Artículo de revisión revisado por pares
- **Temática:** TM-12 Crecimiento, difusión y prospectiva cuantitativa (principal) · secundarias: —
- **Calidad Q:** 88 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** https://arxiv.org/pdf/2602.19488 (bibliografía de DOC-MOT-0429)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Meade Islam 2006 "Modelling and forecasting the diffusion of innovation" 25-year review International Journal of Forecasting»; WebFetch: sí, sobre la página índice https://arxiv.org/pdf/2602.19488)
- **Contenido:** Revisión de referencia de los modelos de difusión hasta 1990: estructura, estimación, extensiones y agenda de investigación.
- **Uso en el Motor:** MC-04: marco conceptual de las extensiones del modelo de Bass.
- **Limitaciones:** Revisión anterior a los modelos estocásticos y de agentes.

#### DOC-MOT-0428 · Q 87 (A) — How Well Do Experience Curves Predict Technological Progress? A Method for Making Distributional Forecasts

- **Autores:** François Lafond; Aimee Gotway Bailey; Jan David Bakker; Dylan Rebois; Rubina Zadourian; Patrick McSharry; J. Doyne Farmer
- **Año:** 2017
- **Publicación o institución:** arXiv 1703.05979 (versión de 18-09-2017)
- **Tipo de documento:** Documento de trabajo (preprint)
- **Temática:** TM-12 Crecimiento, difusión y prospectiva cuantitativa (principal) · secundarias: TM-11
- **Calidad Q:** 87 (A) — Tipo 20/25 · Rigor 17/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 7/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://arxiv.org/pdf/1703.05979
- **Acceso y licencia:** Acceso abierto (arXiv)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «"Experience curve effects" en.wikipedia.org Wright's law»; WebFetch: sí)
- **Contenido:** Método de pronóstico distribucional con curvas de experiencia (primeras diferencias con ruido autocorrelacionado), validado con 51 tecnologías y aplicado a módulos fotovoltaicos.
- **Uso en el Motor:** MC-04: intervalos de pronóstico de costes con la ley de Wright.
- **Limitaciones:** Se cita la versión preprint; no se confirmó la revista de publicación.

#### DOC-MOT-0439 · Q 87 (A) — Innovation Diffusion and New Product Growth Models: A Critical Review and Research Directions

- **Autores:** Renana Peres; Eitan Muller; Vijay Mahajan
- **Año:** 2010
- **Publicación o institución:** International Journal of Research in Marketing, 27(2), 91-106
- **Tipo de documento:** Artículo de revisión revisado por pares
- **Temática:** TM-12 Crecimiento, difusión y prospectiva cuantitativa (principal) · secundarias: —
- **Calidad Q:** 87 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** https://arxiv.org/pdf/2602.19488 (bibliografía de DOC-MOT-0429)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Meade Islam 2006 "Modelling and forecasting the diffusion of innovation" 25-year review International Journal of Forecasting»; WebFetch: sí, sobre la página índice https://arxiv.org/pdf/2602.19488)
- **Contenido:** Actualiza la revisión de modelos de crecimiento de nuevos productos: redes sociales, efectos de red, difusión internacional y competencia.
- **Uso en el Motor:** MC-04: extensiones con efectos de red y difusión entre países.
- **Limitaciones:** Orientado a marketing de productos.

#### DOC-MOT-0444 · Q 87 (A) — On the Econometrics of the Bass Diffusion Model

- **Autores:** H. Peter Boswijk; Philip Hans Franses
- **Año:** 2005
- **Publicación o institución:** Journal of Business & Economic Statistics, 23, 255-268
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-12 Crecimiento, difusión y prospectiva cuantitativa (principal) · secundarias: TM-04
- **Calidad Q:** 87 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 6/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** https://ideas.repec.org/a/eee/intfor/v22y2006i3p519-545.html (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Meade Islam 2006 "Modelling and forecasting the diffusion of innovation" 25-year review International Journal of Forecasting»; WebFetch: sí, sobre la página índice https://ideas.repec.org/a/eee/intfor/v22y2006i3p519-545.html)
- **Contenido:** Formula el modelo de Bass como ecuación diferencial estocástica y deriva su estimación e inferencia econométrica con errores heterocedásticos y autocorrelacionados.
- **Uso en el Motor:** MC-04: estimación con errores estándar correctos de los parámetros de difusión.
- **Limitaciones:** Requiere series de adopción largas.

#### DOC-MOT-0446 · Q 87 (A) — Models of Technology Diffusion

- **Autores:** Paul A. Geroski
- **Año:** 2000
- **Publicación o institución:** Research Policy, 29(4-5), 603-625
- **Tipo de documento:** Artículo de revisión revisado por pares
- **Temática:** TM-12 Crecimiento, difusión y prospectiva cuantitativa (principal) · secundarias: —
- **Calidad Q:** 87 (A) — Tipo 25/25 · Rigor 14/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** https://ideas.repec.org/a/eee/intfor/v22y2006i3p519-545.html (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Meade Islam 2006 "Modelling and forecasting the diffusion of innovation" 25-year review International Journal of Forecasting»; WebFetch: sí, sobre la página índice https://ideas.repec.org/a/eee/intfor/v22y2006i3p519-545.html)
- **Contenido:** Revisa los modelos económicos de difusión (epidémico, probit o de heterogeneidad, legitimación y cascadas de información) y su relación con la curva S.
- **Uso en el Motor:** MC-04: elegir el mecanismo de difusión que justifica la curva usada.
- **Limitaciones:** Revisión conceptual, sin estimaciones nuevas.

#### DOC-MOT-0442 · Q 87 (A) — Forecasting with Growth Curves: An Empirical Comparison

- **Autores:** Nigel Meade; Towhidul Islam
- **Año:** 1995
- **Publicación o institución:** International Journal of Forecasting, 11(2), 199-215
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-12 Crecimiento, difusión y prospectiva cuantitativa (principal) · secundarias: TM-11
- **Calidad Q:** 87 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 7/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** https://ideas.repec.org/a/eee/intfor/v11y1995i2p199-215.html
- **Acceso y licencia:** Artículo de pago en el editor; ficha abierta en RePEc
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Meade Islam 2006 "Modelling and forecasting the diffusion of innovation" 25-year review International Journal of Forecasting»; WebFetch: sí, sobre la página índice https://ideas.repec.org/e/pis165.html)
- **Contenido:** Compara empíricamente diecisiete curvas de crecimiento (logística, Gompertz, etc.) en series de telecomunicaciones y su precisión fuera de muestra.
- **Uso en el Motor:** MC-04: elegir la forma funcional de la curva S según capacidad predictiva.
- **Limitaciones:** Series de telecomunicaciones.

#### DOC-MOT-0436 · Q 87 (A) — A Meta-Analysis of Applications of Diffusion Models

- **Autores:** Fareena Sultan; John U. Farley; Donald R. Lehmann
- **Año:** 1990
- **Publicación o institución:** Journal of Marketing Research, 27(1), 70-77
- **Tipo de documento:** Artículo revisado por pares (metaanálisis)
- **Temática:** TM-12 Crecimiento, difusión y prospectiva cuantitativa (principal) · secundarias: —
- **Calidad Q:** 87 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.1177/002224379002700107 · https://en.wikipedia.org/wiki/Bass_diffusion_model (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Bass diffusion model" en.wikipedia.org»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Bass_diffusion_model)
- **Contenido:** Metaanálisis de 213 aplicaciones del modelo de Bass: valores medios de p (≈0,03) y q (≈0,38) y factores que los explican.
- **Uso en el Motor:** MC-04: priors empíricos de p y q para pronóstico temprano.
- **Limitaciones:** Aplicaciones anteriores a 1990.

#### DOC-MOT-0443 · Q 86 (A) — Technological Forecasting — Model Selection, Model Stability, and Combining Models

- **Autores:** Nigel Meade; Towhidul Islam
- **Año:** 1998
- **Publicación o institución:** Management Science, 44(8), 1115-1130
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-12 Crecimiento, difusión y prospectiva cuantitativa (principal) · secundarias: TM-11
- **Calidad Q:** 86 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 7/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** https://ideas.repec.org/e/pis165.html (lista de publicaciones)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Meade Islam 2006 "Modelling and forecasting the diffusion of innovation" 25-year review International Journal of Forecasting»; WebFetch: sí, sobre la página índice https://ideas.repec.org/e/pis165.html)
- **Contenido:** Estudia la selección y estabilidad de modelos de difusión y muestra las ventajas de combinarlos para pronosticar.
- **Uso en el Motor:** MC-04: combinación de curvas de difusión para robustecer el pronóstico.
- **Limitaciones:** Muestra de series tecnológicas limitada.

#### DOC-MOT-0107 · Q 85 (A) — Diffusion of Innovations (5.ª ed.)

- **Autores:** Everett M. Rogers
- **Año:** 2003
- **Publicación o institución:** Free Press (Simon & Schuster)
- **Tipo de documento:** Libro académico
- **Temática:** TM-12 Crecimiento, difusión y prospectiva cuantitativa (principal) · secundarias: —
- **Calidad Q:** 85 (A) — Tipo 20/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** ISBN: 978-0-7432-5823-4 · https://en.wikipedia.org/wiki/Diffusion_of_innovations (bibliografía)
- **Acceso y licencia:** Libro de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Diffusion of innovations" en.wikipedia.org Rogers Griliches hybrid corn»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Diffusion_of_innovations)
- **Contenido:** Teoría clásica de la difusión: categorías de adoptantes, atributos de la innovación, canales y masa crítica.
- **Uso en el Motor:** MC-04: categorías de adoptantes y atributos de la innovación.
- **Limitaciones:** Teoría cualitativa; complementar con modelos cuantitativos.

#### DOC-MOT-0431 · Q 85 (A) — Learning Rates for Energy Technologies

- **Autores:** Alan McDonald; Leo Schrattenholzer
- **Año:** 2001
- **Publicación o institución:** Energy Policy, 29(4), 255-261
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-12 Crecimiento, difusión y prospectiva cuantitativa (principal) · secundarias: —
- **Calidad Q:** 85 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 13/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** https://arxiv.org/pdf/1703.05979 (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Experience curve effects" en.wikipedia.org Wright's law»; WebFetch: sí, sobre la página índice https://arxiv.org/pdf/1703.05979)
- **Contenido:** Recopila tasas de aprendizaje de 26 tecnologías energéticas y muestra su dispersión y su descenso con la madurez.
- **Uso en el Motor:** MC-04: rangos de referencia de tasas de aprendizaje en energía.
- **Limitaciones:** Datos anteriores a 2000; fuentes heterogéneas.

#### DOC-MOT-0447 · Q 85 (A) — The Diffusion of Mobile Telecommunications Services in the European Union

- **Autores:** Harald Gruber; Frank Verboven
- **Año:** 2001
- **Publicación o institución:** European Economic Review, 45(3), 577-588
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-12 Crecimiento, difusión y prospectiva cuantitativa (principal) · secundarias: —
- **Calidad Q:** 85 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 7/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** https://ideas.repec.org/a/eee/intfor/v22y2006i3p519-545.html (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Meade Islam 2006 "Modelling and forecasting the diffusion of innovation" 25-year review International Journal of Forecasting»; WebFetch: sí, sobre la página índice https://ideas.repec.org/a/eee/intfor/v22y2006i3p519-545.html)
- **Contenido:** Estima la difusión de la telefonía móvil en los países de la UE y el efecto de la regulación, la competencia y el cambio tecnológico (analógico a digital).
- **Uso en el Motor:** MC-04: difusión con datos europeos y efecto de la política pública.
- **Limitaciones:** Periodo 1984-1997.

#### DOC-MOT-0437 · Q 85 (A) — Determination of Adopter Categories by Using Innovation Diffusion Models

- **Autores:** Vijay Mahajan; Eitan Muller; Rajendra K. Srivastava
- **Año:** 1990
- **Publicación o institución:** Journal of Marketing Research, 27(1), 37
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-12 Crecimiento, difusión y prospectiva cuantitativa (principal) · secundarias: —
- **Calidad Q:** 85 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 7/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.2307/3172549 · https://en.wikipedia.org/wiki/Bass_diffusion_model (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor (JSTOR 3172549)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Bass diffusion model" en.wikipedia.org»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Bass_diffusion_model)
- **Contenido:** Deriva las categorías de adoptantes de Rogers a partir de los puntos de inflexión del modelo de Bass.
- **Uso en el Motor:** MC-04: ubicar una tecnología en su fase de adopción (innovadores, mayoría temprana…).
- **Limitaciones:** Depende de la calidad del ajuste de Bass.

#### DOC-MOT-0109 · Q 85 (A) — Factors Affecting the Cost of Airplanes

- **Autores:** Theodore P. Wright
- **Año:** 1936
- **Publicación o institución:** Journal of the Aeronautical Sciences, 3(4), 122-128
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-12 Crecimiento, difusión y prospectiva cuantitativa (principal) · secundarias: —
- **Calidad Q:** 85 (A) — Tipo 22/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.2514/8.155 · https://en.wikipedia.org/wiki/Experience_curve_effect (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Experience curve effects" en.wikipedia.org Wright's law»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Experience_curve_effect)
- **Contenido:** Formula la curva de aprendizaje (ley de Wright): el coste unitario cae un porcentaje fijo cada vez que se duplica la producción acumulada.
- **Uso en el Motor:** MC-04: curva de aprendizaje (coste unitario frente a producción acumulada).
- **Limitaciones:** Tasa de aprendizaje no constante entre tecnologías.

#### DOC-MOT-0432 · Q 82 (A) — Comments on «A New Product Growth for Model Consumer Durables»: The Bass Model

- **Autores:** Frank M. Bass
- **Año:** 2004
- **Publicación o institución:** Management Science, 50(12, suplemento), 1833-1840
- **Tipo de documento:** Artículo revisado por pares (comentario retrospectivo)
- **Temática:** TM-12 Crecimiento, difusión y prospectiva cuantitativa (principal) · secundarias: —
- **Calidad Q:** 82 (A) — Tipo 22/25 · Rigor 12/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 7/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1287/mnsc.1040.0300 · https://en.wikipedia.org/wiki/Bass_diffusion_model (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Bass diffusion model" en.wikipedia.org»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Bass_diffusion_model)
- **Contenido:** Retrospectiva del autor sobre la génesis, extensiones y usos del modelo de Bass, incluido el pronóstico antes del lanzamiento por analogía.
- **Uso en el Motor:** MC-04: guía de uso del modelo de Bass y de parámetros por analogía.
- **Limitaciones:** Texto retrospectivo, no aporta nueva evidencia.

#### DOC-MOT-0441 · Q 80 (A) — A Simple Substitution Model of Technological Change

- **Autores:** J. C. Fisher; R. H. Pry
- **Año:** 1971
- **Publicación o institución:** Technological Forecasting and Social Change, 3, 75-88
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-12 Crecimiento, difusión y prospectiva cuantitativa (principal) · secundarias: —
- **Calidad Q:** 80 (A) — Tipo 22/25 · Rigor 13/20 · Autoridad 13/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** https://arxiv.org/pdf/2602.19488 (bibliografía de DOC-MOT-0429)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Meade Islam 2006 "Modelling and forecasting the diffusion of innovation" 25-year review International Journal of Forecasting»; WebFetch: sí, sobre la página índice https://arxiv.org/pdf/2602.19488)
- **Contenido:** Modelo logístico de sustitución: la cuota de la tecnología nueva sigue una recta en escala logit.
- **Uso en el Motor:** MC-04: pronóstico de cuota de una tecnología sustituta (p. ej., vehículos eléctricos frente a combustión).
- **Limitaciones:** Supone sustitución completa y simétrica.

#### DOC-MOT-0429 · Q 72 (B) — The Dynamics of Innovation Diffusion: A Survey of Bass-Type Models

- **Autores:** Nicolas Langrené; Rui Liu; Xiangqin Wu; Tianhao Zhi
- **Año:** 2026
- **Publicación o institución:** arXiv 2602.19488 (Beijing Normal-Hong Kong Baptist University; Imperial College London; University of Southampton)
- **Tipo de documento:** Artículo de revisión (preprint)
- **Temática:** TM-12 Crecimiento, difusión y prospectiva cuantitativa (principal) · secundarias: —
- **Calidad Q:** 72 (B) — Tipo 15/25 · Rigor 14/20 · Autoridad 10/15 · Vigencia 10/10 · Impacto 3/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://arxiv.org/pdf/2602.19488
- **Acceso y licencia:** Acceso abierto (arXiv)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Meade Islam 2006 "Modelling and forecasting the diffusion of innovation" 25-year review International Journal of Forecasting»; WebFetch: sí)
- **Contenido:** Revisión reciente de modelos tipo Bass: precios, multigeneración, multinacionales, versiones estocásticas, estimación frecuentista, bayesiana (filtro de Kalman) y metaheurística, y comparación con modelos de agentes.
- **Uso en el Motor:** MC-04: mapa actualizado de variantes del modelo de Bass y de sus métodos de estimación.
- **Limitaciones:** Preprint sin revisión por pares constatada.

## TM-13 Métricas específicas por clase (cripto en cadena, inmobiliario, privados)

#### DOC-MOT-0116 · Q 94 (A) — Private Equity Performance: What Do We Know?

- **Autores:** Robert S. Harris; Tim Jenkinson; Steven N. Kaplan
- **Año:** 2014
- **Publicación o institución:** The Journal of Finance, 69(5), 1851-1882
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-13 Métricas específicas por clase (cripto en cadena, inmobiliario, privados) (principal) · secundarias: —
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1111/jofi.12154 · https://ideas.repec.org/a/bla/jfinan/v69y2014i5p1851-1882.html
- **Acceso y licencia:** Artículo de pago en el editor; documento de trabajo NBER w17874
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Harris Jenkinson Kaplan "Private Equity Performance: What Do We Know?" Journal of Finance»; WebFetch: sí)
- **Contenido:** Con flujos de casi 1.400 fondos (Burgiss), el capital riesgo de compra supera al S&P 500 en más de un 3 % anual; el venture capital supera en los noventa y queda por detrás en los dos mil.
- **Uso en el Motor:** MC-09: TIR, múltiplos y PME con datos de flujos (Burgiss).
- **Limitaciones:** Periodo hasta ~2010.

#### DOC-MOT-0119 · Q 94 (A) — Common Risk Factors in Currency Markets

- **Autores:** Hanno Lustig; Nikolai Roussanov; Adrien Verdelhan
- **Año:** 2011
- **Publicación o institución:** The Review of Financial Studies, 24(11), 3731-3777
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-13 Métricas específicas por clase (cripto en cadena, inmobiliario, privados) (principal)
- **Calidad Q (provisional):** 94 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1093/rfs/hhr068 (DOI a verificar)
- **Estado:** PENDIENTE_VERIFICACION_ALTA
- **Estado del enlace:** PENDIENTE_BARRIDO
- **Última verificación:** — (sin verificar)
- **Uso en el Motor:** MC-09: factores de carry y dólar en divisas.
- **Limitaciones:** Universo de divisas del estudio.
- **Origen:** Semilla V3.0 (2026-11-01) para cubrir lagunas; DOC-M la verifica en su primer barrido (HT-02: DOI, metadatos, acceso, retractaciones) y la confirma, repara o da de baja.

#### DOC-MOT-0113 · Q 94 (A) — An Econometric Model of Serial Correlation and Illiquidity in Hedge Fund Returns

- **Autores:** Mila Getmansky; Andrew W. Lo; Igor Makarov
- **Año:** 2004
- **Publicación o institución:** Journal of Financial Economics, 74(3), 529-609 (versión previa: NBER Working Paper 9571, 2003)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-13 Métricas específicas por clase (cripto en cadena, inmobiliario, privados) (principal) · secundarias: TM-11
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 9/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI WP: 10.3386/w9571 · https://www.nber.org/papers/w9571
- **Acceso y licencia:** Documento de trabajo NBER; artículo de revista de pago
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Getmansky Lo Makarov "serial correlation and illiquidity in hedge fund returns" Geltner appraisal smoothing»; WebFetch: sí)
- **Contenido:** Modela la autocorrelación de las rentabilidades de hedge funds como suavizado por iliquidez y gestión de valoraciones, y propone cómo desuavizarlas.
- **Uso en el Motor:** MC-09: desuavizado de rentabilidades de activos ilíquidos (hedge funds, privados).
- **Limitaciones:** Modelo de suavizado lineal. El DOI de revista de la semilla no aparecía en la página y se retira.

#### DOC-MOT-0115 · Q 93 (A) — Private Equity Performance: Returns, Persistence, and Capital Flows

- **Autores:** Steven N. Kaplan; Antoinette Schoar
- **Año:** 2005
- **Publicación o institución:** The Journal of Finance, 60(4), 1791-1823 (versión de trabajo: University of Chicago GSB)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-13 Métricas específicas por clase (cripto en cadena, inmobiliario, privados) (principal) · secundarias: —
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** http://faculty.chicagobooth.edu/steven.kaplan/research/pereturns.pdf (enlace citado en https://en.wikipedia.org/wiki/Public_Market_Equivalent)
- **Acceso y licencia:** Versión de trabajo en la web del autor; artículo de revista de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Public market equivalent" en.wikipedia.org private equity»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Public_Market_Equivalent)
- **Contenido:** Introduce el PME de Kaplan-Schoar y documenta persistencia de resultados entre fondos sucesivos de una misma gestora.
- **Uso en el Motor:** MC-09: equivalente de mercado público (PME) para comparar capital privado con cotizados.
- **Limitaciones:** Datos de fondos con sesgo de selección. Datos de revista (volumen, páginas, DOI) tomados de la semilla y no confirmados en esta verificación; DOI retirado.

#### DOC-MOT-0121 · Q 92 (A) — Trading and Arbitrage in Cryptocurrency Markets

- **Autores:** Igor Makarov; Antoinette Schoar
- **Año:** 2020
- **Publicación o institución:** Journal of Financial Economics, 293-319 (versión previa: LSE Financial Markets Group DP 782, 2018)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-13 Métricas específicas por clase (cripto en cadena, inmobiliario, privados) (principal) · secundarias: —
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1016/j.jfineco.2019.07.001 · https://academicnewsletter.sufe.edu.cn/info/355765
- **Acceso y licencia:** Artículo de pago en el editor; versión de trabajo en researchonline.lse.ac.uk
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Liu Tsyvinski "Risks and Returns of Cryptocurrency" Makarov Schoar "Trading and arbitrage in cryptocurrency markets"»; WebFetch: sí)
- **Contenido:** Documenta grandes y persistentes desviaciones de precio de las criptomonedas entre plataformas y países, más fuertes entre países que dentro de ellos, ligadas a controles de capital.
- **Uso en el Motor:** MC-09: segmentación y primas de precio entre plataformas cripto.
- **Limitaciones:** Periodo 2017-2018. Volumen y fascículo de la semilla no aparecían en la página.

#### DOC-MOT-0123 · Q 92 (A) — The Price of Wine

- **Autores:** Elroy Dimson; Peter L. Rousseau; Christophe Spaenjers
- **Año:** 2015
- **Publicación o institución:** Journal of Financial Economics, 118(2), 431-449
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-13 Métricas específicas por clase (cripto en cadena, inmobiliario, privados) (principal)
- **Calidad Q (provisional):** 92 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1016/j.jfineco.2015.04.001 (a verificar)
- **Estado:** PENDIENTE_VERIFICACION_ALTA
- **Estado del enlace:** PENDIENTE_BARRIDO
- **Última verificación:** — (sin verificar)
- **Uso en el Motor:** MC-09: rentabilidad a largo plazo del vino de inversión y efecto envejecimiento.
- **Limitaciones:** Costes de almacenamiento y transacción elevados.
- **Origen:** Semilla V3.0 (2026-11-01) para cubrir lagunas; DOC-M la verifica en su primer barrido (HT-02: DOI, metadatos, acceso, retractaciones) y la confirma, repara o da de baja.

#### DOC-MOT-0122 · Q 91 (A) — Art as an Investment and the Underperformance of Masterpieces

- **Autores:** Jianping Mei; Michael Moses
- **Año:** 2002
- **Publicación o institución:** American Economic Review, 92(5), 1656-1668
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-13 Métricas específicas por clase (cripto en cadena, inmobiliario, privados) (principal)
- **Calidad Q (provisional):** 91 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1257/000282802762024683 (DOI a verificar)
- **Estado:** PENDIENTE_VERIFICACION_ALTA
- **Estado del enlace:** PENDIENTE_BARRIDO
- **Última verificación:** — (sin verificar)
- **Uso en el Motor:** MC-09: índice de ventas repetidas para arte.
- **Limitaciones:** Sesgo de selección de obras subastadas.
- **Origen:** Semilla V3.0 (2026-11-01) para cubrir lagunas; DOC-M la verifica en su primer barrido (HT-02: DOI, metadatos, acceso, retractaciones) y la confirma, repara o da de baja.

#### DOC-MOT-0120 · Q 90 (A) — Risks and Returns of Cryptocurrency

- **Autores:** Yukun Liu; Aleh Tsyvinski
- **Año:** 2018 (documento de trabajo; NBER w24877, SSRN 3226806)
- **Publicación o institución:** NBER Working Paper 24877 / SSRN 3226806; versión de revista indicada en la semilla (The Review of Financial Studies, 2021) no confirmada en esta verificación
- **Tipo de documento:** Documento de trabajo de institución reconocida
- **Temática:** TM-13 Métricas específicas por clase (cripto en cadena, inmobiliario, privados) (principal) · secundarias: —
- **Calidad Q:** 90 (A) — Tipo 20/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** https://papers.ssrn.com/abstract=3226806
- **Acceso y licencia:** SSRN y NBER (acceso gratuito a la versión de trabajo)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Liu Tsyvinski "Risks and Returns of Cryptocurrency" Makarov Schoar "Trading and arbitrage in cryptocurrency markets"»; WebFetch: sí)
- **Contenido:** Las rentabilidades de las criptomonedas no se explican por factores bursátiles, de divisas o de materias primas, sino por momentum y atención de los inversores propios del mercado cripto.
- **Uso en el Motor:** MC-09: factores de momentum y atención inversora en criptoactivos; exposición nula a factores tradicionales.
- **Limitaciones:** Historia corta y cambiante del mercado. El DOI de revista de la semilla no se ha visto y se retira.

#### DOC-MOT-0451 · Q 90 (A) — Risks and Portfolio Decisions Involving Hedge Funds

- **Autores:** Vikas Agarwal; Narayan Y. Naik
- **Año:** 2004
- **Publicación o institución:** The Review of Financial Studies, 17(1), 63-98
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-13 Métricas específicas por clase (cripto en cadena, inmobiliario, privados) (principal) · secundarias: TM-08
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.1093/rfs/hhg044 · https://en.wikipedia.org/wiki/Sharpe_ratio (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Sharpe ratio" en.wikipedia.org deflated Sharpe ratio»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Sharpe_ratio)
- **Contenido:** Muestra que muchas estrategias de hedge funds tienen pagos no lineales tipo opción (venta de puts) y que la media-varianza subestima sus pérdidas de cola.
- **Uso en el Motor:** MC-09, MC-07: factores de opciones y medidas de cola para hedge funds.
- **Limitaciones:** Datos de hedge funds con sesgos de declaración.

#### DOC-MOT-0118 · Q 89 (A) — The Tactical and Strategic Value of Commodity Futures

- **Autores:** Claude B. Erb; Campbell R. Harvey
- **Año:** 2005 (NBER Working Paper 11222)
- **Publicación o institución:** NBER Working Paper 11222; versión de revista indicada en la semilla (Financial Analysts Journal, 62(2), 2006) no confirmada en esta verificación
- **Tipo de documento:** Documento de trabajo de institución reconocida
- **Temática:** TM-13 Métricas específicas por clase (cripto en cadena, inmobiliario, privados) (principal) · secundarias: —
- **Calidad Q:** 89 (A) — Tipo 20/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** DOI WP: 10.3386/w11222 · https://www.nber.org/papers/w11222
- **Acceso y licencia:** Documento de trabajo NBER; copia en people.duke.edu
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Gorton Rouwenhorst "Facts and Fantasies about Commodity Futures" Erb Harvey "Strategic and Tactical Value of Commodity Futures"»; WebFetch: sí)
- **Contenido:** Descompone la rentabilidad de los futuros de materias primas (spot, roll, colateral) y muestra que el rendimiento de roll explica gran parte de las diferencias entre materias primas.
- **Uso en el Motor:** MC-09: descomposición de rentabilidad de futuros (spot, roll, colateral).
- **Limitaciones:** Periodo previo a la financiarización. Título invertido en la versión NBER («Tactical and Strategic»); la semilla usaba el de la versión de revista. DOI de revista retirado.

#### DOC-MOT-0117 · Q 89 (A) — Facts and Fantasies about Commodity Futures

- **Autores:** Gary B. Gorton; K. Geert Rouwenhorst
- **Año:** 2004 (documento de trabajo Yale ICF 04-20; SSRN 560042, rev. 2005)
- **Publicación o institución:** Yale ICF Working Paper 04-20 / SSRN 560042; versión de revista indicada en la semilla (Financial Analysts Journal, 62(2), 2006) no confirmada en esta verificación
- **Tipo de documento:** Documento de trabajo de institución reconocida
- **Temática:** TM-13 Métricas específicas por clase (cripto en cadena, inmobiliario, privados) (principal) · secundarias: —
- **Calidad Q:** 89 (A) — Tipo 20/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 9/10 · Acceso 9/10
- **DOI / ISBN / URL:** https://papers.ssrn.com/abstract=560042
- **Acceso y licencia:** Versión de trabajo gratuita (SSRN; copia en kellogg.northwestern.edu)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Gorton Rouwenhorst "Facts and Fantasies about Commodity Futures" Erb Harvey "Strategic and Tactical Value of Commodity Futures"»; WebFetch: sí)
- **Contenido:** Con un índice equiponderado de futuros de materias primas 1959-2004, la prima de riesgo (~5 % anual) es comparable a la de la renta variable, con correlación negativa con acciones y bonos y positiva con la inflación.
- **Uso en el Motor:** MC-09: rentabilidad de futuros de materias primas, rendimiento de roll y correlaciones.
- **Limitaciones:** Índice equiponderado histórico. El DOI de revista de la semilla no se ha visto y se retira.

#### DOC-MOT-0453 · Q 89 (A) — The Efficiency of the Market for Single-Family Homes

- **Autores:** Karl E. Case; Robert J. Shiller
- **Año:** 1989
- **Publicación o institución:** American Economic Review, 79, 125-137
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-13 Métricas específicas por clase (cripto en cadena, inmobiliario, privados) (principal) · secundarias: —
- **Calidad Q:** 89 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** https://realestate.wharton.upenn.edu/wp-content/uploads/2017/03/765.pdf (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor (JSTOR)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Repeat sales" index en.wikipedia.org Case Shiller Bailey Muth Nourse»; WebFetch: sí, sobre la página índice https://realestate.wharton.upenn.edu/wp-content/uploads/2017/03/765.pdf)
- **Contenido:** Con índices de ventas repetidas, muestra inercia (autocorrelación positiva) en los precios de la vivienda, señal de ineficiencia del mercado.
- **Uso en el Motor:** MC-09: momentum de precios inmobiliarios y su uso en pronóstico.
- **Limitaciones:** Mercados de EE. UU. de los años 70-80.

#### DOC-MOT-0452 · Q 89 (A) — Prices of Single Family Homes Since 1970: New Indexes for Four Cities

- **Autores:** Karl E. Case; Robert J. Shiller
- **Año:** 1987
- **Publicación o institución:** NBER Working Paper 2393 (publicado también en New England Economic Review, sept.-oct. 1987, 45-56)
- **Tipo de documento:** Documento de trabajo de institución reconocida
- **Temática:** TM-13 Métricas específicas por clase (cripto en cadena, inmobiliario, privados) (principal) · secundarias: —
- **Calidad Q:** 89 (A) — Tipo 20/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** https://www.nber.org/papers/w2393.pdf
- **Acceso y licencia:** Documento de trabajo NBER de acceso abierto
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «"Repeat sales" index en.wikipedia.org Case Shiller Bailey Muth Nourse»; WebFetch: sí)
- **Contenido:** Construye índices trimestrales de precios de vivienda para cuatro ciudades con el método de ventas repetidas ponderadas, origen del índice Case-Shiller.
- **Uso en el Motor:** MC-09: método de ventas repetidas ponderadas para índices inmobiliarios.
- **Limitaciones:** Solo viviendas unifamiliares con dos ventas; cuatro ciudades de EE. UU.

#### DOC-MOT-0448 · Q 88 (A) — The Public Market Equivalent and Private Equity Performance

- **Autores:** Morten Sorensen; Ravi Jagannathan
- **Año:** 2015
- **Publicación o institución:** Financial Analysts Journal, 71(4), 43-50
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-13 Métricas específicas por clase (cripto en cadena, inmobiliario, privados) (principal) · secundarias: —
- **Calidad Q:** 88 (A) — Tipo 22/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.2469/faj.v71.n4.4 · https://rpc.cfainstitute.org/en/research/financial-analysts-journal/2015/the-public-market-equivalent-and-private-equity-performance
- **Acceso y licencia:** Página del CFA Institute; versión de trabajo en SSRN 2347972
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «"Public market equivalent" en.wikipedia.org private equity»; WebFetch: sí)
- **Contenido:** Demuestra que el PME equivale a valorar el capital privado con un factor de descuento estocástico (CAPM dinámico de Rubinstein), sin necesidad de estimar betas.
- **Uso en el Motor:** MC-09: fundamento teórico del PME y elección del índice de referencia.
- **Limitaciones:** El índice debe representar la cartera total del inversor; supuesto de utilidad logarítmica.

#### DOC-MOT-0454 · Q 86 (A) — A Regression Method for Real Estate Price Index Construction

- **Autores:** Martin J. Bailey; Richard F. Muth; Hugh O. Nourse
- **Año:** 1963
- **Publicación o institución:** Journal of the American Statistical Association, 58, 933-942
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-13 Métricas específicas por clase (cripto en cadena, inmobiliario, privados) (principal) · secundarias: —
- **Calidad Q:** 86 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** https://realestate.wharton.upenn.edu/wp-content/uploads/2017/03/765.pdf (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor (JSTOR)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Repeat sales" index en.wikipedia.org Case Shiller Bailey Muth Nourse»; WebFetch: sí, sobre la página índice https://realestate.wharton.upenn.edu/wp-content/uploads/2017/03/765.pdf)
- **Contenido:** Método original de ventas repetidas (BMN): regresión de diferencias de log-precio de un mismo inmueble sobre variables de periodo.
- **Uso en el Motor:** MC-09: índice de ventas repetidas básico.
- **Limitaciones:** Ignora heterocedasticidad por intervalo entre ventas (corregida por Case-Shiller).

#### DOC-MOT-0455 · Q 85 (A) — Repeat Sales House Price Index Methodology

- **Autores:** Chaitra H. Nagaraja; Lawrence D. Brown; Susan M. Wachter
- **Año:** 2014
- **Publicación o institución:** Journal of Real Estate Literature, 22(1), 23-46
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-13 Métricas específicas por clase (cripto en cadena, inmobiliario, privados) (principal) · secundarias: TM-11
- **Calidad Q:** 85 (A) — Tipo 22/25 · Rigor 16/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 5/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** https://realestate.wharton.upenn.edu/wp-content/uploads/2017/03/765.pdf
- **Acceso y licencia:** Copia de acceso abierto en Wharton
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «"Repeat sales" index en.wikipedia.org Case Shiller Bailey Muth Nourse»; WebFetch: sí)
- **Contenido:** Compara índices BMN, Case-Shiller, FHFA, S&P/Case-Shiller, mediana y un índice autorregresivo con ventas únicas y efecto código postal; el autorregresivo predice mejor en 20 áreas metropolitanas.
- **Uso en el Motor:** MC-09: elección de metodología de índice inmobiliario y su error de predicción.
- **Limitaciones:** Solo viviendas con hipoteca convencional; 1985-2004.

#### DOC-MOT-0114 · Q 85 (A) — Estimating Market Values from Appraised Values without Assuming an Efficient Market

- **Autores:** David Geltner
- **Año:** 1993
- **Publicación o institución:** Journal of Real Estate Research, 8(3), 325-345
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-13 Métricas específicas por clase (cripto en cadena, inmobiliario, privados) (principal)
- **Calidad Q (provisional):** 85 (A) — Tipo 22/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI a verificar
- **Estado:** PENDIENTE_VERIFICACION_ALTA
- **Estado del enlace:** PENDIENTE_BARRIDO
- **Última verificación:** — (sin verificar)
- **Uso en el Motor:** MC-09: desuavizado de índices inmobiliarios de tasación.
- **Limitaciones:** Parámetro de suavizado a estimar.
- **Origen:** Semilla V3.0 (2026-11-01) para cubrir lagunas; DOC-M la verifica en su primer barrido (HT-02: DOI, metadatos, acceso, retractaciones) y la confirma, repara o da de baja.

#### DOC-MOT-0460 · Q 83 (A) — Valuing Private Equity

- **Autores:** Morten Sorensen; Neng Wang; Jinqiang Yang
- **Año:** 2011 (versión de trabajo de 13-12-2011)
- **Publicación o institución:** Columbia Business School (documento de trabajo)
- **Tipo de documento:** Documento de trabajo de institución reconocida
- **Temática:** TM-13 Métricas específicas por clase (cripto en cadena, inmobiliario, privados) (principal) · secundarias: —
- **Calidad Q:** 83 (A) — Tipo 20/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 7/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** http://www0.gsb.columbia.edu/faculty/nwang/papers/swy44.pdf (citado en https://en.wikipedia.org/wiki/Public_Market_Equivalent)
- **Acceso y licencia:** PDF en la web de los autores (disponibilidad no comprobada)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Public market equivalent" en.wikipedia.org private equity»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Public_Market_Equivalent)
- **Contenido:** Modelo de ciclo de vida para el inversor (LP) en capital privado con iliquidez, apalancamiento y comisiones; calcula el alfa que el gestor debe generar para compensarlas.
- **Uso en el Motor:** MC-09: coste de iliquidez y comisiones en la valoración de capital privado.
- **Limitaciones:** Versión de trabajo; no se confirmó la publicación en revista.

#### DOC-MOT-0456 · Q 82 (A) — Estimating Price Indices for Residential Property: A Comparison of Repeat Sales and Assessed Value Methods

- **Autores:** John M. Clapp; Carmelo Giaccotto
- **Año:** 1992
- **Publicación o institución:** Journal of the American Statistical Association, 87, 300-306
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-13 Métricas específicas por clase (cripto en cadena, inmobiliario, privados) (principal) · secundarias: —
- **Calidad Q:** 82 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 13/15 · Vigencia 9/10 · Impacto 6/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** https://realestate.wharton.upenn.edu/wp-content/uploads/2017/03/765.pdf (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Repeat sales" index en.wikipedia.org Case Shiller Bailey Muth Nourse»; WebFetch: sí, sobre la página índice https://realestate.wharton.upenn.edu/wp-content/uploads/2017/03/765.pdf)
- **Contenido:** Propone índices basados en la relación precio de venta/valor catastral y los compara con ventas repetidas.
- **Uso en el Motor:** MC-09: índices con valores catastrales cuando hay pocas ventas repetidas.
- **Limitaciones:** Depende de la calidad de la tasación administrativa.

#### DOC-MOT-0449 · Q 81 (A) — Benchmarking Private Equity: The Direct Alpha Method

- **Autores:** Oleg Gredil; Barry Griffiths; Rüdiger Stucke
- **Año:** 2014
- **Publicación o institución:** SSRN 2403521
- **Tipo de documento:** Documento de trabajo
- **Temática:** TM-13 Métricas específicas por clase (cripto en cadena, inmobiliario, privados) (principal) · secundarias: —
- **Calidad Q:** 81 (A) — Tipo 20/25 · Rigor 15/20 · Autoridad 12/15 · Vigencia 10/10 · Impacto 7/10 · Independencia 9/10 · Acceso 8/10
- **DOI / ISBN / URL:** https://papers.ssrn.com/sol3/papers.cfm?abstract_id=2403521 (citado en https://en.wikipedia.org/wiki/Public_Market_Equivalent)
- **Acceso y licencia:** SSRN (gratuito)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Public market equivalent" en.wikipedia.org private equity»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Public_Market_Equivalent)
- **Contenido:** Propone el «direct alpha»: TIR de los flujos del fondo capitalizados con el índice público, interpretable como alfa anualizado en tiempo continuo.
- **Uso en el Motor:** MC-09: métrica de exceso de rentabilidad de fondos privados frente al índice.
- **Limitaciones:** Documento de trabajo; año y autoría tomados del texto de la página índice.

#### DOC-MOT-0459 · Q 81 (A) — The Accuracy of Real Estate Indices: Repeat Sales Estimators

- **Autores:** William N. Goetzmann
- **Año:** 1992
- **Publicación o institución:** Journal of Real Estate Finance and Economics, 5, 5-53
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-13 Métricas específicas por clase (cripto en cadena, inmobiliario, privados) (principal) · secundarias: TM-14
- **Calidad Q:** 81 (A) — Tipo 22/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 7/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** https://realestate.wharton.upenn.edu/wp-content/uploads/2017/03/765.pdf (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Repeat sales" index en.wikipedia.org Case Shiller Bailey Muth Nourse»; WebFetch: sí, sobre la página índice https://realestate.wharton.upenn.edu/wp-content/uploads/2017/03/765.pdf)
- **Contenido:** Analiza el sesgo y la precisión de los estimadores de ventas repetidas y propone correcciones (incluido el sesgo al pasar de log-precios a precios).
- **Uso en el Motor:** MC-09: corrección del sesgo y del error de los índices de ventas repetidas.
- **Limitaciones:** Simulaciones con supuestos simplificados.

#### DOC-MOT-0457 · Q 79 (B) — Price Indices Based on the Hedonic Repeat-Sales Method: Application to the Housing Market

- **Autores:** John M. Clapp; Carmelo Giaccotto
- **Año:** 1998
- **Publicación o institución:** Journal of Real Estate Finance and Economics, 16, 5-26
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-13 Métricas específicas por clase (cripto en cadena, inmobiliario, privados) (principal) · secundarias: —
- **Calidad Q:** 79 (B) — Tipo 22/25 · Rigor 15/20 · Autoridad 13/15 · Vigencia 9/10 · Impacto 6/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** https://realestate.wharton.upenn.edu/wp-content/uploads/2017/03/765.pdf (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Repeat sales" index en.wikipedia.org Case Shiller Bailey Muth Nourse»; WebFetch: sí, sobre la página índice https://realestate.wharton.upenn.edu/wp-content/uploads/2017/03/765.pdf)
- **Contenido:** Combina ventas repetidas con variables hedónicas para controlar cambios de calidad del inmueble entre ventas.
- **Uso en el Motor:** MC-09: índices híbridos hedónicos-ventas repetidas.
- **Limitaciones:** Requiere características detalladas de los inmuebles.

#### DOC-MOT-0458 · Q 78 (B) — Residential Hedonic Models: A Rational Expectations Approach to Age Effects

- **Autores:** John M. Clapp; Carmelo Giaccotto
- **Año:** 1998
- **Publicación o institución:** Journal of Urban Economics, 44, 415-437
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-13 Métricas específicas por clase (cripto en cadena, inmobiliario, privados) (principal) · secundarias: —
- **Calidad Q:** 78 (B) — Tipo 22/25 · Rigor 15/20 · Autoridad 13/15 · Vigencia 9/10 · Impacto 5/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** https://realestate.wharton.upenn.edu/wp-content/uploads/2017/03/765.pdf (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Repeat sales" index en.wikipedia.org Case Shiller Bailey Muth Nourse»; WebFetch: sí, sobre la página índice https://realestate.wharton.upenn.edu/wp-content/uploads/2017/03/765.pdf)
- **Contenido:** Muestra que el efecto de la antigüedad en modelos hedónicos varía con el tiempo y lo modela con expectativas racionales, evitando sesgos en los índices.
- **Uso en el Motor:** MC-09: tratamiento de la depreciación por antigüedad en índices hedónicos.
- **Limitaciones:** Aplicación a un mercado local de EE. UU.

#### DOC-MOT-0450 · Q 66 (B) — A Private Investment Benchmark

- **Autores:** Austin M. Long; Craig J. Nickels
- **Año:** 1996
- **Publicación o institución:** Alignment Capital (presentado en la conferencia AIMR)
- **Tipo de documento:** Informe técnico con metodología
- **Temática:** TM-13 Métricas específicas por clase (cripto en cadena, inmobiliario, privados) (principal) · secundarias: —
- **Calidad Q:** 66 (B) — Tipo 15/25 · Rigor 12/20 · Autoridad 11/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 7/10 · Acceso 4/10
- **DOI / ISBN / URL:** http://alignmentcapital.com/pdfs/research/icm_aimr_benchmark_1996.pdf (citado en https://en.wikipedia.org/wiki/Public_Market_Equivalent)
- **Acceso y licencia:** PDF del emisor (disponibilidad no comprobada)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Public market equivalent" en.wikipedia.org private equity»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Public_Market_Equivalent)
- **Contenido:** Propone el método de comparación de índices (ICM o LN-PME): replicar los flujos del fondo en el índice público y comparar TIR.
- **Uso en el Motor:** MC-09: PME de Long-Nickels como alternativa al de Kaplan-Schoar.
- **Limitaciones:** Informe de una gestora; el enlace puede estar caído; el método puede dar valores negativos con fondos muy rentables.

## TM-14 Datos, calidad y reproducibilidad

#### DOC-MOT-0126 · Q 92 (A) — The FAIR Guiding Principles for Scientific Data Management and Stewardship

- **Autores:** Mark D. Wilkinson et al.
- **Año:** 2016
- **Publicación o institución:** Scientific Data, 3, 160018
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-14 Datos, calidad y reproducibilidad (principal)
- **Calidad Q (provisional):** 92 (A) — Tipo 23/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** DOI: 10.1038/sdata.2016.18 (DOI a verificar)
- **Estado:** PENDIENTE_VERIFICACION_ALTA
- **Estado del enlace:** PENDIENTE_BARRIDO
- **Última verificación:** — (sin verificar)
- **Uso en el Motor:** MC-01: principios de datos localizables, accesibles, interoperables y reutilizables para artefactos del Motor.
- **Limitaciones:** Principios, no implementación.
- **Origen:** Semilla V3.0 (2026-11-01) para cubrir lagunas; DOC-M la verifica en su primer barrido (HT-02: DOI, metadatos, acceso, retractaciones) y la confirma, repara o da de baja.

#### DOC-MOT-0472 · Q 92 (A) — The Extent and Consequences of P-Hacking in Science

- **Autores:** Megan L. Head; Luke Holman; Rob Lanfear; Andrew T. Kahn; Michael D. Jennions
- **Año:** 2015
- **Publicación o institución:** PLOS Biology, 13(3), e1002106
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-14 Datos, calidad y reproducibilidad (principal) · secundarias: TM-11
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** DOI: 10.1371/journal.pbio.1002106 · https://en.wikipedia.org/wiki/Data_dredging (bibliografía)
- **Acceso y licencia:** Acceso abierto (PLoS; PMC4359000)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Data dredging" wikipedia data snooping White reality check»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Data_dredging)
- **Contenido:** Con minería de textos de p-valores publicados, detecta p-hacking extendido aunque de efecto limitado en los metaanálisis.
- **Uso en el Motor:** MC-10: método de diagnóstico de p-hacking por la distribución de p-valores.
- **Limitaciones:** Disciplinas biomédicas y biológicas.

#### DOC-MOT-0129 · Q 92 (A) — Why Most Published Research Findings Are False

- **Autores:** John P. A. Ioannidis
- **Año:** 2005
- **Publicación o institución:** PLoS Medicine, 2(8), e124
- **Tipo de documento:** Artículo revisado por pares (ensayo)
- **Temática:** TM-14 Datos, calidad y reproducibilidad (principal) · secundarias: TM-11
- **Calidad Q:** 92 (A) — Tipo 23/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** DOI: 10.1371/journal.pmed.0020124 · https://en.wikipedia.org/wiki/Data_dredging (bibliografía)
- **Acceso y licencia:** Acceso abierto (PLoS; PMC1182327)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Data dredging" wikipedia data snooping White reality check»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Data_dredging)
- **Contenido:** Muestra que la probabilidad de que un hallazgo publicado sea cierto baja con poca potencia, efectos pequeños, muchos contrastes, flexibilidad analítica y competencia entre equipos.
- **Uso en el Motor:** MC-10: probabilidad de falso positivo según potencia, sesgo y número de equipos; aplicable a anomalías financieras.
- **Limitaciones:** Modelo conceptual.

#### DOC-MOT-0125 · Q 92 (A) — A Real-Time Data Set for Macroeconomists

- **Autores:** Dean Croushore; Tom Stark
- **Año:** 2001
- **Publicación o institución:** Journal of Econometrics, 105, 111-130
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-14 Datos, calidad y reproducibilidad (principal) · secundarias: TM-11
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** https://facultystaff.richmond.edu/~dcrousho/docs/Croushore%20Real%20Time%20Frontiers%2009Dec.pdf (bibliografía); base de datos en la Reserva Federal de Filadelfia
- **Acceso y licencia:** Artículo de pago en el editor; versiones de trabajo en philadelphiafed.org
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Philadelphia Fed Real-Time Data Set for Macroeconomists Croushore Stark»; WebFetch: sí, sobre la página índice https://facultystaff.richmond.edu/~dcrousho/docs/Croushore%20Real%20Time%20Frontiers%2009Dec.pdf)
- **Contenido:** Presenta la base de datos de la Reserva Federal de Filadelfia con las «añadas» (vintages) de las series macro tal como se conocían en cada fecha.
- **Uso en el Motor:** MC-03, MC-10: datos en tiempo real (vintages) para evitar sesgo de anticipación en backtests macro.
- **Limitaciones:** Datos estadounidenses. El DOI de la semilla no se ha visto y se retira.

#### DOC-MOT-0465 · Q 92 (A) — Monetary Policy Rules Based on Real-Time Data

- **Autores:** Athanasios Orphanides
- **Año:** 2001
- **Publicación o institución:** American Economic Review, 91, 964-985
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-14 Datos, calidad y reproducibilidad (principal) · secundarias: —
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** https://facultystaff.richmond.edu/~dcrousho/docs/Croushore%20Real%20Time%20Frontiers%2009Dec.pdf (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Philadelphia Fed Real-Time Data Set for Macroeconomists Croushore Stark»; WebFetch: sí, sobre la página índice https://facultystaff.richmond.edu/~dcrousho/docs/Croushore%20Real%20Time%20Frontiers%2009Dec.pdf)
- **Contenido:** Muestra que las reglas de Taylor estimadas con datos revisados describen mal la política real; con datos disponibles en su momento las conclusiones cambian.
- **Uso en el Motor:** MC-03, MC-10: evaluar señales de política monetaria con la información disponible en cada fecha.
- **Limitaciones:** Política de la Reserva Federal.

#### DOC-MOT-0124 · Q 92 (A) — Survivorship Bias in Performance Studies

- **Autores:** Stephen J. Brown; William N. Goetzmann; Roger G. Ibbotson; Stephen A. Ross
- **Año:** 1992
- **Publicación o institución:** The Review of Financial Studies, 5, 553-580
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-14 Datos, calidad y reproducibilidad (principal) · secundarias: TM-11
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** https://archive.nyu.edu/bitstream/2451/27418/2/S-AM-00-08.pdf (bibliografía de Carhart et al., DOC-MOT-0469)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Survivorship bias" en.wikipedia.org mutual funds»; WebFetch: sí, sobre la página índice https://archive.nyu.edu/bitstream/2451/27418/2/S-AM-00-08.pdf)
- **Contenido:** Muestra que el sesgo de supervivencia puede generar una persistencia aparente de resultados en fondos aunque no exista.
- **Uso en el Motor:** MC-10, MC-01: sesgo de supervivencia en bases de datos de rentabilidad.
- **Limitaciones:** Contexto de fondos de inversión. El DOI de la semilla no se ha visto en la verificación y se retira.

#### DOC-MOT-0471 · Q 91 (A) — The ASA Statement on p-Values: Context, Process, and Purpose

- **Autores:** Ronald L. Wasserstein; Nicole A. Lazar
- **Año:** 2016
- **Publicación o institución:** The American Statistician, 70(2), 129-133
- **Tipo de documento:** Declaración institucional revisada (American Statistical Association)
- **Temática:** TM-14 Datos, calidad y reproducibilidad (principal) · secundarias: TM-01, TM-11
- **Calidad Q:** 91 (A) — Tipo 23/25 · Rigor 14/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** DOI: 10.1080/00031305.2016.1154108 · https://en.wikipedia.org/wiki/Data_dredging (bibliografía)
- **Acceso y licencia:** Acceso abierto (Taylor & Francis)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Data dredging" wikipedia data snooping White reality check»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Data_dredging)
- **Contenido:** Seis principios de la ASA sobre el uso e interpretación de los p-valores: no miden la probabilidad de la hipótesis ni el tamaño del efecto, y no deben usarse solos para decidir.
- **Uso en el Motor:** MC-10, MC-08: regla de comunicación de significación en los artefactos del Motor.
- **Limitaciones:** Principios generales, no un procedimiento.

#### DOC-MOT-0468 · Q 91 (A) — Survivorship Bias and Mutual Fund Performance

- **Autores:** Edwin J. Elton; Martin J. Gruber; Christopher R. Blake
- **Año:** 1996
- **Publicación o institución:** The Review of Financial Studies, 9(4), 1097-1120
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-14 Datos, calidad y reproducibilidad (principal) · secundarias: TM-07
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.1093/rfs/9.4.1097 · https://en.wikipedia.org/wiki/Survivorship_bias (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Survivorship bias" en.wikipedia.org mutual funds»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Survivorship_bias)
- **Contenido:** Cuantifica el sesgo de supervivencia en rentabilidades de fondos de inversión y su efecto sobre las medidas de rendimiento.
- **Uso en el Motor:** MC-01, MC-10: corrección del sesgo de supervivencia en bases de fondos.
- **Limitaciones:** Fondos estadounidenses.

#### DOC-MOT-0128 · Q 89 (A) — Tidy Data

- **Autores:** Hadley Wickham
- **Año:** 2014
- **Publicación o institución:** Journal of Statistical Software, 59(10)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-14 Datos, calidad y reproducibilidad (principal)
- **Calidad Q (provisional):** 89 (A) — Tipo 22/25 · Rigor 15/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** DOI: 10.18637/jss.v059.i10 (DOI a verificar)
- **Estado:** PENDIENTE_VERIFICACION_ALTA
- **Estado del enlace:** PENDIENTE_BARRIDO
- **Última verificación:** — (sin verificar)
- **Uso en el Motor:** MC-01: estructura ordenada de datos para cálculos reproducibles.
- **Limitaciones:** Orientado a R.
- **Origen:** Semilla V3.0 (2026-11-01) para cubrir lagunas; DOC-M la verifica en su primer barrido (HT-02: DOI, metadatos, acceso, retractaciones) y la confirma, repara o da de baja.

#### DOC-MOT-0473 · Q 89 (A) — P-Curve: A Key to the File-Drawer

- **Autores:** Uri Simonsohn; Leif D. Nelson; Joseph P. Simmons
- **Año:** 2014
- **Publicación o institución:** Journal of Experimental Psychology: General, 143(2), 534-547
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-14 Datos, calidad y reproducibilidad (principal) · secundarias: TM-11
- **Calidad Q:** 89 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.1037/a0033242 · https://en.wikipedia.org/wiki/Data_dredging (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Data dredging" wikipedia data snooping White reality check»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Data_dredging)
- **Contenido:** Propone la curva p (distribución de p-valores significativos) para distinguir efectos reales de resultados seleccionados o manipulados.
- **Uso en el Motor:** MC-10: contrastar si un conjunto de anomalías publicadas refleja efectos reales.
- **Limitaciones:** Requiere p-valores independientes y bien reportados.

#### DOC-MOT-0469 · Q 89 (A) — Mutual Fund Survivorship

- **Autores:** Mark M. Carhart; Jennifer N. Carpenter; Anthony W. Lynch; David K. Musto
- **Año:** 2000 (versión de 12-09-2000; primer borrador de 1994)
- **Publicación o institución:** NYU Stern (documento de trabajo; repositorio archive.nyu.edu)
- **Tipo de documento:** Documento de trabajo de institución reconocida
- **Temática:** TM-14 Datos, calidad y reproducibilidad (principal) · secundarias: TM-07
- **Calidad Q:** 89 (A) — Tipo 20/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** https://archive.nyu.edu/bitstream/2451/27418/2/S-AM-00-08.pdf
- **Acceso y licencia:** Acceso abierto (repositorio de NYU)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «"Survivorship bias" en.wikipedia.org mutual funds»; WebFetch: sí)
- **Contenido:** Los fondos con malos resultados desaparecen tras varios años, de modo que el sesgo de supervivencia crece con la longitud de la muestra y distorsiona la persistencia medida.
- **Uso en el Motor:** MC-01, MC-10: diseño de muestras libres de supervivencia y magnitud esperada del sesgo.
- **Limitaciones:** Versión de trabajo; no se confirmó la publicación en revista.

#### DOC-MOT-0012 · Q 88 (A) — Ten Simple Rules for Reproducible Computational Research

- **Autores:** Geir Kjetil Sandve; Anton Nekrutenko; James Taylor; Eivind Hovig
- **Año:** 2013
- **Publicación o institución:** PLoS Computational Biology, vol. 9, n.º 10, e1003285 (Public Library of Science)
- **Tipo de documento:** Artículo revisado por pares (guía)
- **Temática:** TM-14 Datos, calidad y reproducibilidad (principal)
- **Calidad Q:** 88 (A) — Tipo 22/25 · Rigor 14/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** DOI: 10.1371/journal.pcbi.1003285 · Acceso abierto en la editorial (journals.plos.org) · Identificadores verificados (anexo 8.1 V2.3): DOI: doi.org/10.1371/journal.pcbi.1003285 · Acceso abierto en la editorial (journals.plos.org, ficha)
- **Acceso y licencia:** Peldaño 1 (acceso abierto en la editorial) · Licencia: Creative Commons (acceso abierto PLoS); verificar la variante CC exacta de la pieza
- **Versión:** Publicada (v1 en PLoS)
- **Estado:** Aprobada
- **Estado del enlace:** PENDIENTE_BARRIDO
- **Última verificación:** 2026-10-25 (verificación documentada en V2.3)
- **Contenido:** Diez reglas operativas de reproducibilidad computacional: versionar todo, anotar el entorno, no sobrescribir resultados, externalizar datos y scripts. Son las reglas que sustentan la exigencia del Motor de devolver resultado, artefacto y limitaciones reproducibles en cada servicio CT-11.
- **Uso en el Motor:** Reproducibilidad de los servicios (calculation_log, artefactos); base de la re-ejecución independiente (CT-10)
- **Estatus epistémico:** Guía revisada por pares; nivel alto para el propósito de trazabilidad
- **Limitaciones:** Reglas generales de reproducibilidad, no específicas de finanzas
- **Área y etiquetas:** Reproducibilidad computacional · reproducibilidad; trazabilidad; ct-12
- **Verificación V2.3:** Completa (carga de arranque): cita, DOI y acceso abierto verificados el 25/10/2026; comprobaciones omitidas: lectura del texto completo por el Documentador, pendiente de la primera revisión

#### DOC-MOT-0127 · Q 88 (A) — Reproducible Research in Computational Science

- **Autores:** Roger D. Peng
- **Año:** 2011
- **Publicación o institución:** Science, 334(6060), 1226-1227
- **Tipo de documento:** Artículo revisado por pares (perspectiva)
- **Temática:** TM-14 Datos, calidad y reproducibilidad (principal)
- **Calidad Q (provisional):** 88 (A) — Tipo 23/25 · Rigor 14/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI: 10.1126/science.1213847 (DOI a verificar)
- **Estado:** PENDIENTE_VERIFICACION_ALTA
- **Estado del enlace:** PENDIENTE_BARRIDO
- **Última verificación:** — (sin verificar)
- **Uso en el Motor:** MC-08: espectro de reproducibilidad (código, datos, entorno).
- **Limitaciones:** Texto breve de posición.
- **Origen:** Semilla V3.0 (2026-11-01) para cubrir lagunas; DOC-M la verifica en su primer barrido (HT-02: DOI, metadatos, acceso, retractaciones) y la confirma, repara o da de baja.

#### DOC-MOT-0467 · Q 88 (A) — Forecasting Output with the Composite Leading Index: A Real-Time Analysis

- **Autores:** Francis X. Diebold; Glenn D. Rudebusch
- **Año:** 1991
- **Publicación o institución:** Journal of the American Statistical Association, 86, 603-610
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-14 Datos, calidad y reproducibilidad (principal) · secundarias: TM-11
- **Calidad Q:** 88 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** https://facultystaff.richmond.edu/~dcrousho/docs/Croushore%20Real%20Time%20Frontiers%2009Dec.pdf (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Philadelphia Fed Real-Time Data Set for Macroeconomists Croushore Stark»; WebFetch: sí, sobre la página índice https://facultystaff.richmond.edu/~dcrousho/docs/Croushore%20Real%20Time%20Frontiers%2009Dec.pdf)
- **Contenido:** Con datos en tiempo real, el índice compuesto de indicadores adelantados pronostica la producción mucho peor que con datos revisados.
- **Uso en el Motor:** MC-10: ejemplo canónico de sobreestimación de capacidad predictiva por usar datos revisados.
- **Limitaciones:** Índice adelantado de EE. UU.

#### DOC-MOT-0476 · Q 87 (A) — Degrees of Freedom in Planning, Running, Analyzing, and Reporting Psychological Studies: A Checklist to Avoid p-Hacking

- **Autores:** Jelte M. Wicherts; Coosje L. S. Veldkamp; Hilde E. M. Augusteijn; Marjan Bakker; Robbie C. M. van Aert; Marcel A. L. M. van Assen
- **Año:** 2016
- **Publicación o institución:** Frontiers in Psychology, 7, 1832
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-14 Datos, calidad y reproducibilidad (principal) · secundarias: TM-11
- **Calidad Q:** 87 (A) — Tipo 23/25 · Rigor 13/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** DOI: 10.3389/fpsyg.2016.01832 · https://en.wikipedia.org/wiki/Data_dredging (bibliografía)
- **Acceso y licencia:** Acceso abierto (Frontiers; PMC5122713)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Data dredging" wikipedia data snooping White reality check»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Data_dredging)
- **Contenido:** Lista de comprobación de 34 grados de libertad del investigador en diseño, análisis e informe que permiten el p-hacking.
- **Uso en el Motor:** MC-08, MC-10: lista de comprobación de decisiones a registrar antes de un backtest (preregistro interno).
- **Limitaciones:** Pensada para psicología; requiere adaptación a finanzas.

#### DOC-MOT-0461 · Q 87 (A) — Frontiers of Real-Time Data Analysis

- **Autores:** Dean Croushore
- **Año:** 2009 (versión del autor, diciembre de 2009)
- **Publicación o institución:** University of Richmond / Federal Reserve Bank of Philadelphia (versión aceptada tras revisión; la revista no se identifica en el texto)
- **Tipo de documento:** Artículo de revisión
- **Temática:** TM-14 Datos, calidad y reproducibilidad (principal) · secundarias: TM-11
- **Calidad Q:** 87 (A) — Tipo 20/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** https://facultystaff.richmond.edu/~dcrousho/docs/Croushore%20Real%20Time%20Frontiers%2009Dec.pdf
- **Acceso y licencia:** PDF de acceso abierto en la web del autor
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Philadelphia Fed Real-Time Data Set for Macroeconomists Croushore Stark»; WebFetch: sí)
- **Contenido:** Revisa la investigación con datos en tiempo real: revisiones de datos, modelos estructurales, pronóstico, política monetaria, análisis de coyuntura y conjuntos de datos disponibles.
- **Uso en el Motor:** MC-01, MC-10: guía para usar añadas de datos y evitar el sesgo de datos revisados en evaluaciones.
- **Limitaciones:** Revista de publicación no confirmada; foco en EE. UU.

#### DOC-MOT-0463 · Q 87 (A) — Data Revisions Are Not Well Behaved

- **Autores:** S. Borağan Aruoba
- **Año:** 2008
- **Publicación o institución:** Journal of Money, Credit and Banking, 40, 319-340
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-14 Datos, calidad y reproducibilidad (principal) · secundarias: —
- **Calidad Q:** 87 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** https://facultystaff.richmond.edu/~dcrousho/docs/Croushore%20Real%20Time%20Frontiers%2009Dec.pdf (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Philadelphia Fed Real-Time Data Set for Macroeconomists Croushore Stark»; WebFetch: sí, sobre la página índice https://facultystaff.richmond.edu/~dcrousho/docs/Croushore%20Real%20Time%20Frontiers%2009Dec.pdf)
- **Contenido:** Muestra que las revisiones de datos macro de EE. UU. tienen media distinta de cero, son predecibles y no son ruido puro.
- **Uso en el Motor:** MC-01, MC-03: tratar el dato preliminar como estimación sesgada, no como valor final.
- **Limitaciones:** Variables macro estadounidenses.

#### DOC-MOT-0464 · Q 87 (A) — The Use and Abuse of «Real-Time» Data in Economic Forecasting

- **Autores:** Evan F. Koenig; Sheila Dolmas; Jeremy Piger
- **Año:** 2003
- **Publicación o institución:** The Review of Economics and Statistics, 85, 618-628
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-14 Datos, calidad y reproducibilidad (principal) · secundarias: TM-11
- **Calidad Q:** 87 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** https://facultystaff.richmond.edu/~dcrousho/docs/Croushore%20Real%20Time%20Frontiers%2009Dec.pdf (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Philadelphia Fed Real-Time Data Set for Macroeconomists Croushore Stark»; WebFetch: sí, sobre la página índice https://facultystaff.richmond.edu/~dcrousho/docs/Croushore%20Real%20Time%20Frontiers%2009Dec.pdf)
- **Contenido:** Muestra que estimar modelos de pronóstico con datos de la primera publicación (en lugar de la última añada) mejora la precisión en tiempo real.
- **Uso en el Motor:** MC-10: diseño de backtests macro con la añada correcta.
- **Limitaciones:** Aplicación al PIB de EE. UU.

#### DOC-MOT-0474 · Q 86 (A) — The Credibility Crisis in Research: Can Economics Tools Help?

- **Autores:** Thomas Gall; John P. A. Ioannidis; Zacharias Maniadis
- **Año:** 2017
- **Publicación o institución:** PLOS Biology, 15(4), e2001846
- **Tipo de documento:** Artículo revisado por pares (ensayo)
- **Temática:** TM-14 Datos, calidad y reproducibilidad (principal) · secundarias: —
- **Calidad Q:** 86 (A) — Tipo 23/25 · Rigor 13/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 6/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** DOI: 10.1371/journal.pbio.2001846 · https://en.wikipedia.org/wiki/Data_dredging (bibliografía)
- **Acceso y licencia:** Acceso abierto (PLoS; PMC5405914)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Data dredging" wikipedia data snooping White reality check»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Data_dredging)
- **Contenido:** Analiza con herramientas económicas (incentivos, diseño de mecanismos) las causas de la crisis de credibilidad y propone reformas.
- **Uso en el Motor:** MC-10: marco de incentivos para valorar la fiabilidad de fuentes de investigación.
- **Limitaciones:** Ensayo conceptual.

#### DOC-MOT-0466 · Q 86 (A) — News and Noise in G-7 GDP Announcements

- **Autores:** Jon Faust; John H. Rogers; Jonathan H. Wright
- **Año:** 2005
- **Publicación o institución:** Journal of Money, Credit and Banking, 37, 403-419
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-14 Datos, calidad y reproducibilidad (principal) · secundarias: —
- **Calidad Q:** 86 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 7/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** https://facultystaff.richmond.edu/~dcrousho/docs/Croushore%20Real%20Time%20Frontiers%2009Dec.pdf (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Philadelphia Fed Real-Time Data Set for Macroeconomists Croushore Stark»; WebFetch: sí, sobre la página índice https://facultystaff.richmond.edu/~dcrousho/docs/Croushore%20Real%20Time%20Frontiers%2009Dec.pdf)
- **Contenido:** Analiza las revisiones del PIB en los países del G-7 y si los anuncios iniciales son noticia o ruido; en varios países las revisiones son predecibles.
- **Uso en el Motor:** MC-01: calidad del dato preliminar de PIB en economías europeas y del G-7.
- **Limitaciones:** Periodo de los años 80-90.

#### DOC-MOT-0475 · Q 85 (A) — The Power of Tests for Detecting p-Hacking

- **Autores:** Graham Elliott; Nikolay Kudrin; Kaspar Wüthrich
- **Año:** 2025
- **Publicación o institución:** The Review of Economics and Statistics
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-14 Datos, calidad y reproducibilidad (principal) · secundarias: TM-11
- **Calidad Q:** 85 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 4/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** DOI: 10.1162/REST.a.1688 · https://en.wikipedia.org/wiki/Data_dredging (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Data dredging" wikipedia data snooping White reality check»; WebFetch: sí, sobre la página índice https://en.wikipedia.org/wiki/Data_dredging)
- **Contenido:** Evalúa teóricamente y por simulación la potencia de los contrastes de p-hacking según la forma de manipulación y el sesgo de publicación.
- **Uso en el Motor:** MC-10: elegir el contraste de p-hacking más potente al auditar evidencia.
- **Limitaciones:** Reciente; volumen y páginas no figuran en la fuente.

#### DOC-MOT-0470 · Q 84 (A) — The J-Shape of Performance Persistence Given Survivorship Bias

- **Autores:** Darryll Hendricks; Jayendu Patel; Richard Zeckhauser
- **Año:** 1996
- **Publicación o institución:** The Review of Economics and Statistics
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-14 Datos, calidad y reproducibilidad (principal) · secundarias: —
- **Calidad Q:** 84 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 7/10 · Independencia 10/10 · Acceso 4/10
- **DOI / ISBN / URL:** https://archive.nyu.edu/bitstream/2451/27418/2/S-AM-00-08.pdf (bibliografía)
- **Acceso y licencia:** Artículo de pago en el editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Survivorship bias" en.wikipedia.org mutual funds»; WebFetch: sí, sobre la página índice https://archive.nyu.edu/bitstream/2451/27418/2/S-AM-00-08.pdf)
- **Contenido:** Muestra que el sesgo de supervivencia puede producir una relación en forma de J entre rentabilidad pasada y futura, imitando persistencia.
- **Uso en el Motor:** MC-10: interpretación de la persistencia aparente en estudios de fondos.
- **Limitaciones:** Volumen y páginas no figuran en la fuente consultada.

#### DOC-MOT-0462 · Q 80 (A) — A Funny Thing Happened on the Way to the Data Bank: A Real-Time Data Set for Macroeconomists

- **Autores:** Dean D. Croushore; Tom Stark
- **Año:** 2000
- **Publicación o institución:** Federal Reserve Bank of Philadelphia, Business Review, sept.-oct. 2000, 15-27
- **Tipo de documento:** Artículo divulgativo de banco central
- **Temática:** TM-14 Datos, calidad y reproducibilidad (principal) · secundarias: —
- **Calidad Q:** 80 (A) — Tipo 15/25 · Rigor 14/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 7/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://scholarship.richmond.edu/economics-faculty-publications/8
- **Acceso y licencia:** Acceso abierto (repositorio de la Universidad de Richmond)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Philadelphia Fed Real-Time Data Set for Macroeconomists Croushore Stark»; WebFetch: sí)
- **Contenido:** Explica cómo se construyó la base de datos en tiempo real, cuánto se revisan los datos y cómo cambian los resultados de pronóstico e investigación con datos revisados.
- **Uso en el Motor:** MC-01: justificación divulgativa del uso de añadas en el Motor.
- **Limitaciones:** Texto divulgativo.

## TM-15 Índices: construcción, rebalanceo y rentabilidad esperada

#### DOC-MOT-0510 · Q 94 (A) — The Equity Premium

- **Autores:** Eugene F. Fama; Kenneth R. French
- **Año:** 2002
- **Publicación o institución:** The Journal of Finance, pp. 637-659
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-15 Índices: construcción, rebalanceo y rentabilidad esperada (principal) · secundarias: TM-05
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1111/1540-6261.00437 · https://academicnewsletter.sufe.edu.cn/info/361437
- **Acceso y licencia:** Artículo de revista de pago; resumen público (resumen CFA Digest, DOI 10.2469/dig.v32.n4.1174)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Fama French 2002 "The Equity Premium" Journal of Finance dividend growth model»; WebFetch: sí)
- **Contenido:** Estima la prima de renta variable de EE. UU. con modelos de crecimiento de dividendos y de beneficios (1872-2000): para 1951-2000 obtiene 2,55 % y 4,32 %, muy por debajo del 7,43 % realizado, y atribuye la diferencia a una caída de la tasa de descuento (revalorización inesperada).
- **Uso en el Motor:** MC-09: rentabilidad esperada de un índice por «bloques» (rentabilidad por dividendo + crecimiento) frente a la media histórica; separación del componente de revalorización. Al servicio de AC-IDX.
- **Limitaciones:** Solo EE. UU.; sensible a la elección de dividendos frente a beneficios y a las recompras.

#### DOC-MOT-0502 · Q 93 (A) — The Price Response to S&P 500 Index Additions and Deletions: Evidence of Asymmetry and a New Explanation

- **Autores:** Honghui Chen; Gregory Noronha; Vijay Singal
- **Año:** 2004
- **Publicación o institución:** The Journal of Finance, pp. 1901-1929
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-15 Índices: construcción, rebalanceo y rentabilidad esperada (principal) · secundarias: —
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1111/j.1540-6261.2004.00683.x · https://academicnewsletter.sufe.edu.cn/info/361234
- **Acceso y licencia:** Artículo de revista de pago; resumen público
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Chen Noronha Singal 2004 "The Price Response to S&P 500 Index Additions and Deletions: Evidence of Asymmetry and a New Explanation"»; WebFetch: sí)
- **Contenido:** Documenta la asimetría del efecto índice: las altas en el S&P 500 obtienen una subida permanente y las bajas no sufren caída permanente; lo explica por cambios en el reconocimiento de los inversores (investor awareness).
- **Uso en el Motor:** MC-01, MC-09: diseño de estudios de evento separados para altas y bajas en reconstituciones de índices (AC-IDX).
- **Limitaciones:** Muestra anterior a 2003; el efecto ha menguado después (véase DOC-MOT-0507).

#### DOC-MOT-0500 · Q 93 (A) — Do Demand Curves for Stocks Slope Down?

- **Autores:** Andrei Shleifer
- **Año:** 1986
- **Publicación o institución:** The Journal of Finance, 41(3), 579-590
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-15 Índices: construcción, rebalanceo y rentabilidad esperada (principal) · secundarias: —
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de Greenwood y Sammon, NBER WP 30748): https://www.nber.org/system/files/working_papers/w30748/w30748.pdf
- **Acceso y licencia:** Artículo de revista de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «S&P 500 index effect literature Shleifer 1986 Harris Gurel 1986 Chen Noronha Singal 2004 Petajisto index premium»; WebFetch: sí, sobre la página índice)
- **Contenido:** Estudio fundacional del efecto índice: las acciones incorporadas al S&P 500 obtienen rentabilidades anormales positivas al anuncio, evidencia de curvas de demanda con pendiente negativa.
- **Uso en el Motor:** MC-01: referencia de origen para medir el efecto de inclusión en índices.
- **Limitaciones:** Datos 1966-1983; confirmada solo por bibliografía; DOI no visto.

#### DOC-MOT-0507 · Q 92 (A) — The Disappearing Index Effect

- **Autores:** Robin Greenwood; Marco Sammon
- **Año:** 2025
- **Publicación o institución:** The Journal of Finance, 80(2), 657-698 (versión previa: NBER Working Paper 30748)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-15 Índices: construcción, rebalanceo y rentabilidad esperada (principal) · secundarias: —
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 7/10 · Independencia 10/10 · Acceso 8/10
- **DOI / ISBN / URL:** DOI: 10.1111/jofi.13410 · https://ideas.repec.org/a/bla/jfinan/v80y2025i2p657-698.html
- **Acceso y licencia:** Revista de pago; documento de trabajo NBER y SSRN (abstract=4294297) de acceso abierto
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Greenwood Sammon "The Disappearing Index Effect" Journal of Finance»; WebFetch: sí)
- **Contenido:** La rentabilidad anormal de las altas en el S&P 500 cae de un 7,4 % en los noventa a menos de un 1 % en la última década (y las bajas, a un -0,1 % en 2010-2020) pese al auge de la gestión indexada; examina las causas y halla caídas similares en otras familias de índices.
- **Uso en el Motor:** MC-09, MC-10: calibración actual del efecto índice y advertencia contra extrapolar estimaciones históricas en estrategias de rebalanceo (AC-IDX).
- **Limitaciones:** Centrado en EE. UU.

#### DOC-MOT-0501 · Q 92 (A) — Price and Volume Effects Associated with Changes in the S&P 500 List: New Evidence for the Existence of Price Pressures

- **Autores:** Lawrence Harris; Eitan Gurel
- **Año:** 1986
- **Publicación o institución:** The Journal of Finance, 41(4), 815-829
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-15 Índices: construcción, rebalanceo y rentabilidad esperada (principal) · secundarias: —
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de NBER WP 30748): https://www.nber.org/system/files/working_papers/w30748/w30748.pdf
- **Acceso y licencia:** Artículo de revista de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «S&P 500 index effect literature Shleifer 1986 Harris Gurel 1986 Chen Noronha Singal 2004 Petajisto index premium»; WebFetch: sí, sobre la página índice)
- **Contenido:** Muestra subidas de precio y volumen tras la inclusión en el S&P 500 que se revierten parcialmente, interpretadas como presión de precios temporal.
- **Uso en el Motor:** MC-01: hipótesis de presión de precios frente a curvas de demanda en el análisis de rebalanceos.
- **Limitaciones:** Muestra antigua; confirmada solo por bibliografía.

#### DOC-MOT-0517 · Q 91 (A) — Do Stocks Outperform Treasury Bills?

- **Autores:** Hendrik Bessembinder
- **Año:** 2018
- **Publicación o institución:** Journal of Financial Economics, pp. 440-457
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-15 Índices: construcción, rebalanceo y rentabilidad esperada (principal) · secundarias: TM-07
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / ISBN / URL:** DOI: 10.1016/j.jfineco.2018.06.004 · https://academicnewsletter.sufe.edu.cn/info/356102
- **Acceso y licencia:** Artículo de revista de pago; resumen público (página de la W. P. Carey School con resumen)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Bessembinder 2018 "Do stocks outperform Treasury bills?" Journal of Financial Economics»; WebFetch: sí)
- **Contenido:** La mayoría de las acciones de CRSP desde 1926 rinden menos que las letras a un mes; el 4 % mejor explica toda la creación neta de riqueza del mercado, por la asimetría positiva de las rentabilidades individuales.
- **Uso en el Motor:** MC-07, MC-09: fundamento de la concentración de la rentabilidad en índices y del coste de la diversificación insuficiente.
- **Limitaciones:** EE. UU.; volumen y número no figuran en la página leída.

#### DOC-MOT-0504 · Q 91 (A) — Short- and Long-Term Demand Curves for Stocks: Theory and Evidence on the Dynamics of Arbitrage

- **Autores:** Robin Greenwood
- **Año:** 2005
- **Publicación o institución:** Journal of Financial Economics, 75(3), 607-649
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-15 Índices: construcción, rebalanceo y rentabilidad esperada (principal) · secundarias: —
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de NBER WP 30748): https://www.nber.org/system/files/working_papers/w30748/w30748.pdf
- **Acceso y licencia:** Artículo de revista de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «S&P 500 index effect literature Shleifer 1986 Harris Gurel 1986 Chen Noronha Singal 2004 Petajisto index premium»; WebFetch: sí, sobre la página índice)
- **Contenido:** Usa la redefinición del índice Nikkei 225 en 2000 para estimar curvas de demanda a corto y largo plazo y la dinámica del arbitraje ante choques de oferta inducidos por índices.
- **Uso en el Motor:** MC-01, MC-09: estimación de elasticidades de demanda ante cambios de composición en mercados no estadounidenses.
- **Limitaciones:** Un único evento (Japón); confirmada solo por bibliografía.

#### DOC-MOT-0511 · Q 91 (A) — Fundamental Indexation

- **Autores:** Robert D. Arnott; Jason Hsu; Philip Moore
- **Año:** 2005
- **Publicación o institución:** Financial Analysts Journal, 61(2), 83-99
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-15 Índices: construcción, rebalanceo y rentabilidad esperada (principal) · secundarias: TM-07
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 8/10 · Acceso 9/10
- **DOI / ISBN / URL:** DOI: 10.2469/faj.v61.n2.2718 · https://rpc.cfainstitute.org/research/financial-analysts-journal/2005/fundamental-indexation
- **Acceso y licencia:** Página del editor con resumen; texto completo con suscripción CFA
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Arnott Hsu Moore 2005 "Fundamental Indexation" Financial Analysts Journal»; WebFetch: sí)
- **Contenido:** Compara índices ponderados por medidas fundamentales de tamaño (ventas, valor contable, dividendos, empleo) con índices ponderados por capitalización y halla mayor eficiencia media-varianza en los primeros.
- **Uso en el Motor:** MC-07, MC-09: comparación de esquemas de ponderación alternativos y su sesgo implícito hacia valor (AC-IDX).
- **Limitaciones:** Autores vinculados a un proveedor de índices fundamentales (conflicto de interés); parte del exceso se explica por exposición a factores.

#### DOC-MOT-0505 · Q 90 (A) — Regression Discontinuity and the Price Effects of Stock Market Indexing

- **Autores:** Yen-Cheng Chang; Harrison Hong; Inessa Liskovich
- **Año:** 2015
- **Publicación o institución:** The Review of Financial Studies, 28(1), 212-246
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-15 Índices: construcción, rebalanceo y rentabilidad esperada (principal) · secundarias: TM-04
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 7/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de NBER WP 30748): https://www.nber.org/system/files/working_papers/w30748/w30748.pdf
- **Acceso y licencia:** Artículo de revista de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «S&P 500 index effect literature Shleifer 1986 Harris Gurel 1986 Chen Noronha Singal 2004 Petajisto index premium»; WebFetch: sí, sobre la página índice)
- **Contenido:** Aplica regresión en discontinuidad en el umbral de capitalización Russell 1000/2000 para identificar el efecto precio de la inclusión en índices, separándolo de la selección.
- **Uso en el Motor:** MC-03: diseño de identificación causal del efecto de reconstitución en índices con reglas mecánicas.
- **Limitaciones:** Específico de la regla de Russell; confirmada solo por bibliografía.

#### DOC-MOT-0508 · Q 90 (A) — The Index Premium and Its Hidden Cost for Index Funds

- **Autores:** Antti Petajisto
- **Año:** 2011
- **Publicación o institución:** Journal of Empirical Finance, 18, 271-288
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-15 Índices: construcción, rebalanceo y rentabilidad esperada (principal) · secundarias: TM-16
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 12/15 · Vigencia 9/10 · Impacto 7/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** DOI: 10.1016/j.jempfin.2010.10.002 · https://ww.petajisto.net/papers/petajisto 2011 jef - hidden cost for index funds.pdf
- **Acceso y licencia:** Versión del autor en acceso abierto
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «S&P 500 index effect literature Shleifer 1986 Harris Gurel 1986 Chen Noronha Singal 2004 Petajisto index premium»; WebFetch: sí)
- **Contenido:** Estima la prima de índice en S&P 500 y Russell 2000 (1990-2005: +8,8 % y +4,7 % en altas; -15,1 % y -4,6 % en bajas) e introduce el «coste de rotación del índice» que soportan los fondos indexados (21-28 pb/año en el S&P 500 y 38-77 pb en el Russell 2000).
- **Uso en el Motor:** MC-09: cuantificación del coste oculto de replicar índices con reconstituciones previsibles (AC-IDX, AC-FON).
- **Limitaciones:** Muestra hasta 2005.

#### DOC-MOT-0506 · Q 90 (A) — Demand Curves for Stocks Do Slope Down

- **Autores:** Aditya Kaul; Vikas Mehrotra; Randall Morck
- **Año:** 2000
- **Publicación o institución:** The Journal of Finance, 55(2), 893-912
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-15 Índices: construcción, rebalanceo y rentabilidad esperada (principal) · secundarias: —
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de NBER WP 30748): https://www.nber.org/system/files/working_papers/w30748/w30748.pdf
- **Acceso y licencia:** Artículo de revista de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «S&P 500 index effect literature Shleifer 1986 Harris Gurel 1986 Chen Noronha Singal 2004 Petajisto index premium»; WebFetch: sí, sobre la página índice)
- **Contenido:** Aprovecha un cambio de ponderaciones del índice TSE 300 de Toronto por ajuste de capital flotante (sin contenido informativo) para mostrar efectos de precio permanentes, evidencia limpia de demanda con pendiente negativa.
- **Uso en el Motor:** MC-01, MC-09: estimación del impacto de cambios de ponderación por flotante en índices fuera de EE. UU.
- **Limitaciones:** Evento único canadiense; título tal como figura en la bibliografía índice (el artículo publicado lleva subtítulo sobre el ajuste de ponderaciones, no confirmado en esta verificación).

#### DOC-MOT-0503 · Q 89 (A) — Does Arbitrage Flatten Demand Curves for Stocks?

- **Autores:** Jeffrey Wurgler; Ekaterina Zhuravskaya
- **Año:** 2002
- **Publicación o institución:** The Journal of Business, 75(4), 583-608
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-15 Índices: construcción, rebalanceo y rentabilidad esperada (principal) · secundarias: —
- **Calidad Q:** 89 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de NBER WP 30748): https://www.nber.org/system/files/working_papers/w30748/w30748.pdf
- **Acceso y licencia:** Artículo de revista de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «S&P 500 index effect literature Shleifer 1986 Harris Gurel 1986 Chen Noronha Singal 2004 Petajisto index premium»; WebFetch: sí, sobre la página índice)
- **Contenido:** Relaciona la magnitud del efecto de inclusión en el S&P 500 con el riesgo de arbitraje (falta de sustitutivos cercanos): cuanto peor el sustitutivo, mayor el salto de precio.
- **Uso en el Motor:** MC-09: variable explicativa (riesgo idiosincrático/arbitraje) para graduar el efecto esperado de un cambio de composición.
- **Limitaciones:** Confirmada solo por bibliografía.

#### DOC-MOT-0513 · Q 88 (A) — The Properties of Equally Weighted Risk Contribution Portfolios

- **Autores:** Sébastien Maillard; Thierry Roncalli; Jérôme Teiletche
- **Año:** 2010
- **Publicación o institución:** The Journal of Portfolio Management, 36(4), 60-70
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-15 Índices: construcción, rebalanceo y rentabilidad esperada (principal) · secundarias: TM-07
- **Calidad Q:** 88 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 13/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 7/10 · Acceso 7/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de MSCI Product Insight, Sun 2011): https://www.msci.com/documents/10199/36c8ed57-cfad-4d77-8d40-6cbcc107a778
- **Acceso y licencia:** Artículo de revista de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Maillard Roncalli Teiletche "The Properties of Equally Weighted Risk Contribution Portfolios"»; WebFetch: sí, sobre la página índice)
- **Contenido:** Define la cartera de contribuciones al riesgo iguales (paridad de riesgo) y demuestra que su volatilidad queda entre la de mínima varianza y la equiponderada.
- **Uso en el Motor:** MC-07: construcción y diagnóstico de índices de paridad de riesgo y de contribuciones al riesgo.
- **Limitaciones:** Confirmada solo por bibliografía; autores de la industria.

#### DOC-MOT-0514 · Q 88 (A) — Minimum-Variance Portfolios in the U.S. Equity Market

- **Autores:** Roger Clarke; Harindra de Silva; Steven Thorley
- **Año:** 2006
- **Publicación o institución:** The Journal of Portfolio Management, 33(1), 10-24
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-15 Índices: construcción, rebalanceo y rentabilidad esperada (principal) · secundarias: TM-07
- **Calidad Q:** 88 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 13/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 8/10 · Acceso 7/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de MSCI Product Insight, Sun 2011): https://www.msci.com/documents/10199/36c8ed57-cfad-4d77-8d40-6cbcc107a778
- **Acceso y licencia:** Artículo de revista de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Maillard Roncalli Teiletche "The Properties of Equally Weighted Risk Contribution Portfolios"»; WebFetch: sí, sobre la página índice)
- **Contenido:** Construye carteras de mínima varianza con las 1.000 mayores acciones de EE. UU. y muestra menor volatilidad con rentabilidad comparable a la del índice ponderado por capitalización.
- **Uso en el Motor:** MC-07: referencia de los índices de mínima volatilidad como alternativa de ponderación.
- **Limitaciones:** Confirmada solo por bibliografía; concentración en sectores defensivos.

#### DOC-MOT-0522 · Q 88 (A) — Long-Run Stock Returns: Participating in the Real Economy

- **Autores:** Roger G. Ibbotson; Peng Chen
- **Año:** 2003
- **Publicación o institución:** Financial Analysts Journal, 59(1), 88-98
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-15 Índices: construcción, rebalanceo y rentabilidad esperada (principal) · secundarias: TM-05
- **Calidad Q:** 88 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 7/10 · Acceso 9/10
- **DOI / ISBN / URL:** DOI: 10.2469/faj.v59.n1.2505 · https://rpc.cfainstitute.org/research/financial-analysts-journal/2003/long-run-stock-returns-participating-in-the-real-economy
- **Acceso y licencia:** Página del editor con resumen; documento de trabajo en RePEc (ysm354)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Ibbotson Chen 2003 "Long-Run Stock Returns: Participating in the Real Economy" Financial Analysts Journal»; WebFetch: sí)
- **Contenido:** Descompone la rentabilidad histórica de la renta variable de EE. UU. (1926-2000) en inflación, crecimiento de beneficios, dividendos y variación del PER, y estima una prima de lado de oferta de unos 6 puntos (aritmética) y 4 (geométrica) sobre bonos a largo.
- **Uso en el Motor:** MC-09: contraste del modelo de bloques (DOC-MOT-0509, DOC-MOT-0510) con un enfoque de oferta ligado al crecimiento económico.
- **Limitaciones:** Autores vinculados a una firma de análisis de inversión; EE. UU.

#### DOC-MOT-0520 · Q 88 (A) — New Evidence on Stock Price Effects Associated with Changes in the S&P 500 Index

- **Autores:** Anthony W. Lynch; Richard R. Mendenhall
- **Año:** 1997
- **Publicación o institución:** The Journal of Business, 70(3), 351-383
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-15 Índices: construcción, rebalanceo y rentabilidad esperada (principal) · secundarias: —
- **Calidad Q:** 88 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 13/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de NBER WP 30748): https://www.nber.org/system/files/working_papers/w30748/w30748.pdf
- **Acceso y licencia:** Artículo de revista de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «S&P 500 index effect literature Shleifer 1986 Harris Gurel 1986 Chen Noronha Singal 2004 Petajisto index premium»; WebFetch: sí, sobre la página índice)
- **Contenido:** Explota el intervalo entre anuncio y fecha efectiva de los cambios del S&P 500 (desde 1989) para separar efectos de anuncio y de ejecución, con reversión parcial tras la fecha efectiva.
- **Uso en el Motor:** MC-01: ventana de evento (anuncio frente a fecha efectiva) en estudios de rebalanceo de índices.
- **Limitaciones:** Confirmada solo por bibliografía.

#### DOC-MOT-0515 · Q 86 (A) — The Herfindahl-Hirschman Index

- **Autores:** Stephen A. Rhoades
- **Año:** 1993
- **Publicación o institución:** Federal Reserve Bulletin (marzo de 1993), Board of Governors of the Federal Reserve System
- **Tipo de documento:** Artículo de publicación oficial de banco central
- **Temática:** TM-15 Índices: construcción, rebalanceo y rentabilidad esperada (principal) · secundarias: TM-01
- **Calidad Q:** 86 (A) — Tipo 20/25 · Rigor 14/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 9/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://fedinprint.org/item/fedgrb/15160
- **Acceso y licencia:** Acceso abierto (Fed in Print)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Rhoades 1993 "The Herfindahl-Hirschman Index" Federal Reserve Bulletin»; WebFetch: sí)
- **Contenido:** Explica la construcción del índice HHI (suma de cuadrados de las cuotas), su interpretación y los umbrales usados en defensa de la competencia.
- **Uso en el Motor:** MC-01: cálculo del HHI de ponderaciones de un índice y de su inverso (número efectivo de componentes, 1/HHI) como medida de concentración (AC-IDX).
- **Limitaciones:** Pensado para concentración de mercado bancario, no de carteras; la ficha de Fed in Print no da páginas.

#### DOC-MOT-0523 · Q 84 (A) — Index Construction Objectives, Guiding Principles and Methodology for the MSCI Global Investable Market Indexes

- **Autores:** MSCI Inc.
- **Año:** 2020 (versión de enero de 2020; actualizada periódicamente)
- **Publicación o institución:** MSCI Inc.
- **Tipo de documento:** Metodología oficial de proveedor de índices
- **Temática:** TM-15 Índices: construcción, rebalanceo y rentabilidad esperada (principal) · secundarias: TM-14
- **Calidad Q:** 84 (A) — Tipo 18/25 · Rigor 18/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 5/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://www.msci.com/eqb/methodology/meth_docs/MSCI_GIMIMethodology_Jan 2020.pdf
- **Acceso y licencia:** Acceso abierto (web de MSCI)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «MSCI Global Investable Market Indexes Methodology index review free float size segment»; WebFetch: sí)
- **Contenido:** Reglas de segmentación por tamaño (cobertura del 70/85/99 %), ajuste por capital flotante, requisitos mínimos de flotante, revisiones semestrales (mayo/noviembre) y trimestrales, y zonas de amortiguación (buffers) entre segmentos.
- **Uso en el Motor:** MC-01, MC-09: calendario y reglas mecánicas de rebalanceo para anticipar cambios de composición y su rotación (AC-IDX).
- **Limitaciones:** Versión de 2020: comprobar la vigente en la página de metodologías de MSCI antes de un cálculo; documento del propio proveedor.

#### DOC-MOT-0521 · Q 84 (A) — Risk Contribution Is Exposure Times Volatility Times Correlation: Decomposing Risk Using the X-Sigma-Rho Formula

- **Autores:** Jose Menchero; Ben Davis
- **Año:** 2011
- **Publicación o institución:** The Journal of Portfolio Management, 37(2), 97-106
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-15 Índices: construcción, rebalanceo y rentabilidad esperada (principal) · secundarias: TM-07, TM-08
- **Calidad Q:** 84 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 12/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 7/10 · Acceso 7/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de MSCI Product Insight, Sun 2011): https://www.msci.com/documents/10199/36c8ed57-cfad-4d77-8d40-6cbcc107a778
- **Acceso y licencia:** Artículo de revista de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Maillard Roncalli Teiletche "The Properties of Equally Weighted Risk Contribution Portfolios"»; WebFetch: sí, sobre la página índice)
- **Contenido:** Descompone la contribución de cada componente al riesgo de una cartera en exposición × volatilidad × correlación con la cartera.
- **Uso en el Motor:** MC-07: atribución de la concentración de riesgo de un índice por componente o sector, más allá de la concentración de pesos.
- **Limitaciones:** Autores de un proveedor de índices y modelos de riesgo; confirmada solo por bibliografía.

#### DOC-MOT-0512 · Q 84 (A) — Toward Maximum Diversification

- **Autores:** Yves Choueifaty; Yves Coignard
- **Año:** 2008
- **Publicación o institución:** The Journal of Portfolio Management, 35(1), 40-51 (la página índice de R lo cita como vol. 34, n.º 4)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-15 Índices: construcción, rebalanceo y rentabilidad esperada (principal) · secundarias: TM-07
- **Calidad Q:** 84 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 12/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 7/10 · Acceso 7/10
- **DOI / ISBN / URL:** Verificada en página índice (documentación de FRAPO::DivRatios): https://search.r-project.org/CRAN/refmans/FRAPO/html/DivRatios.html · ficha relacionada en risk.net
- **Acceso y licencia:** Artículo de revista de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Choueifaty Coignard 2008 "Toward Maximum Diversification" Journal of Portfolio Management diversification ratio»; WebFetch: sí, sobre la página índice y sobre la ficha de risk.net de Choueifaty, Froidure y Reynier)
- **Contenido:** Define el ratio de diversificación (media ponderada de volatilidades entre volatilidad de la cartera) y la cartera de máxima diversificación como alternativa a la ponderación por capitalización.
- **Uso en el Motor:** MC-01, MC-07: medida de diversificación de un índice complementaria al HHI (DOC-MOT-0515).
- **Limitaciones:** Autores de una gestora que comercializa la estrategia; discrepancia de volumen entre fuentes (35(1) en risk.net, 34(4) en la documentación de R).

#### DOC-MOT-0518 · Q 82 (A) — Index Mathematics Methodology

- **Autores:** S&P Dow Jones Indices (S&P Global)
- **Año:** 2026 (versión publicada el 25/09/2026; actualizada periódicamente)
- **Publicación o institución:** S&P Dow Jones Indices
- **Tipo de documento:** Metodología oficial de proveedor de índices
- **Temática:** TM-15 Índices: construcción, rebalanceo y rentabilidad esperada (principal) · secundarias: TM-14
- **Calidad Q:** 82 (A) — Tipo 18/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 5/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://www.spglobal.com/spdji/en/methodology/article/index-mathematics-methodology
- **Acceso y licencia:** Acceso abierto (web de S&P DJI)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «S&P Dow Jones Indices "Index Mathematics Methodology" divisor float adjustment»; WebFetch: sí)
- **Contenido:** Fórmulas del divisor y su ajuste por eventos corporativos y rebalanceos, índices de precio y de rentabilidad total, índices con límites de peso (capping) y esquemas de ponderación por capitalización, precio, equiponderación y factores.
- **Uso en el Motor:** MC-01: recálculo reproducible de niveles de índice, rentabilidad total y efecto de los límites de peso.
- **Limitaciones:** Documento del proveedor; los detalles cambian entre versiones.

#### DOC-MOT-0519 · Q 80 (A) — Why Does an Equal-Weighted Portfolio Outperform Value- and Price-Weighted Portfolios?

- **Autores:** Yuliya Plyakha; Raman Uppal; Grigory Vilkov
- **Año:** 2012
- **Publicación o institución:** EDHEC (documento de trabajo, marzo de 2012)
- **Tipo de documento:** Documento de trabajo
- **Temática:** TM-15 Índices: construcción, rebalanceo y rentabilidad esperada (principal) · secundarias: TM-07
- **Calidad Q:** 80 (A) — Tipo 17/25 · Rigor 16/20 · Autoridad 13/15 · Vigencia 9/10 · Impacto 7/10 · Independencia 9/10 · Acceso 9/10
- **DOI / ISBN / URL:** https://climateinstitute.edhec.edu/publications/why-does-equal-weighted-portfolio-outperform-value-and-price-weighted-portfolios
- **Acceso y licencia:** Acceso abierto (EDHEC)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Plyakha Uppal Vilkov "Equal or Value Weighting? Implications for Asset-Pricing Tests" rebalancing»; WebFetch: sí)
- **Contenido:** Con rebalanceo mensual, la cartera equiponderada de grandes índices de EE. UU. supera a la ponderada por valor y por precio en rentabilidad, alfa de cuatro factores y Sharpe, pese a su mayor riesgo; atribuye la ventaja a factores y al propio rebalanceo contrario.
- **Uso en el Motor:** MC-07, MC-09: separación del efecto «rebalanceo» del efecto «exposición a factores» en índices equiponderados.
- **Limitaciones:** Documento de trabajo (versión de 2012).

#### DOC-MOT-0516 · Q 76 (B) — Risk Budgeting and Diversification Based on Optimized Uncorrelated Factors

- **Autores:** Attilio Meucci; Alberto Santangelo; Romain Deguest
- **Año:** 2015 (revisión SSRN del 10/11/2015)
- **Publicación o institución:** SSRN (abstract=2276632)
- **Tipo de documento:** Documento de trabajo
- **Temática:** TM-15 Índices: construcción, rebalanceo y rentabilidad esperada (principal) · secundarias: TM-07
- **Calidad Q:** 76 (B) — Tipo 15/25 · Rigor 16/20 · Autoridad 12/15 · Vigencia 9/10 · Impacto 6/10 · Independencia 9/10 · Acceso 9/10
- **DOI / ISBN / URL:** DOI: 10.2139/ssrn.2276632 · verificada en página índice (README del paquete R uncorbets): https://archive.linux.duke.edu/cran/web/packages/uncorbets/readme/README.html
- **Acceso y licencia:** Acceso abierto (SSRN)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Meucci 2009 "Managing Diversification" Risk effective number of bets SSRN»; WebFetch: sí, sobre la página índice)
- **Contenido:** Propone factores no correlacionados óptimos (torsión mínima) y el «número efectivo de apuestas» (exponencial de la entropía de las contribuciones al riesgo) como medida de diversificación.
- **Uso en el Motor:** MC-07: número efectivo de apuestas de un índice como complemento al número efectivo de componentes (1/HHI).
- **Limitaciones:** Documento de trabajo; implementación numérica no trivial.

#### DOC-MOT-0509 · Q 76 (B) — The Equity Risk Premium (modelo Grinold-Kroner)

- **Autores:** Richard Grinold; Kenneth Kroner
- **Año:** 2002
- **Publicación o institución:** Investment Insights, Barclays Global Investors (julio de 2002)
- **Tipo de documento:** Informe técnico con metodología
- **Temática:** TM-15 Índices: construcción, rebalanceo y rentabilidad esperada (principal) · secundarias: TM-05
- **Calidad Q:** 76 (B) — Tipo 15/25 · Rigor 15/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 7/10 · Acceso 6/10
- **DOI / ISBN / URL:** Verificada en página índice: https://en.wikipedia.org/wiki/Grinold_and_Kroner_Model
- **Acceso y licencia:** Publicación de gestora; sin copia oficial localizada en abierto
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Grinold Kroner "Investment Insights" Barclays Global Investors 2002 equity risk premium building blocks»; WebFetch: sí, sobre la página índice)
- **Contenido:** Descompone la rentabilidad esperada de la renta variable en rentabilidad por dividendo, inflación esperada, crecimiento real de beneficios, variación del número de acciones (recompras/emisiones) y variación del PER.
- **Uso en el Motor:** MC-09: fórmula estándar de rentabilidad esperada a largo plazo de un índice por bloques (AC-IDX), con supuestos explícitos por componente.
- **Limitaciones:** Documento de gestora, no revisado por pares; supuestos de reversión del PER subjetivos; confirmada solo por página índice.

## TM-16 Vehículos: descuentos, réplica y ETF apalancados

#### DOC-MOT-0555 · Q 97 (A) — False Discoveries in Mutual Fund Performance: Measuring Luck in Estimated Alphas

- **Autores:** Laurent Barras; Olivier Scaillet; Russ Wermers
- **Año:** 2010
- **Publicación o institución:** The Journal of Finance, 65(1), 179 y ss.
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-16 Vehículos: descuentos, réplica y ETF apalancados (principal) · secundarias: TM-01, TM-11
- **Calidad Q:** 97 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 9/10
- **DOI / ISBN / URL:** https://terpconnect.umd.edu/~wermers/FDR_published.pdf
- **Acceso y licencia:** Versión publicada en la página del autor
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Barras Scaillet Wermers "False Discoveries in Mutual Fund Performance: Measuring Luck in Estimated Alphas" pdf»; WebFetch: sí)
- **Contenido:** Aplica la tasa de falsos descubrimientos a los alfas de fondos: ~75 % de los fondos tienen alfa cero neto de gastos; los fondos con habilidad casi desaparecen hacia 2006; mejora la detección de persistencia.
- **Uso en el Motor:** MC-10: medición de persistencia y habilidad en categorías de fondos controlando la suerte (AC-FON).
- **Limitaciones:** Fondos de renta variable de EE. UU.

#### DOC-MOT-0540 · Q 95 (A) — Path-Dependence of Leveraged ETF Returns

- **Autores:** Marco Avellaneda; Stanley Zhang
- **Año:** 2010
- **Publicación o institución:** SIAM Journal on Financial Mathematics, 1, 586-603
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-16 Vehículos: descuentos, réplica y ETF apalancados (principal) · secundarias: TM-06, TM-03
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** DOI: 10.1137/090760805 · https://math.nyu.edu/%7Eavellane/SIAMLETFS.pdf.pdf
- **Acceso y licencia:** Versión del autor en abierto (NYU)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Avellaneda Zhang 2010 "Path-dependence of leveraged ETF returns" SIAM Journal on Financial Mathematics»; WebFetch: sí)
- **Contenido:** Fórmula cerrada que liga el valor de un ETF apalancado (factor β) al del subyacente: (S_t/S_0)^β por un término de financiación y otro de varianza realizada con coeficiente (β−β²)/2; contrastada con datos de ETF apalancados.
- **Uso en el Motor:** MC-02, MC-09: cálculo del decaimiento por volatilidad esperado de ETF apalancados e inversos en función de la varianza realizada prevista (AC-FON, AC-DER).
- **Limitaciones:** Supone rebalanceo diario continuo; costes de préstamo simplificados.

#### DOC-MOT-0556 · Q 95 (A) — Luck versus Skill in the Cross-Section of Mutual Fund Returns

- **Autores:** Eugene F. Fama; Kenneth R. French
- **Año:** 2010
- **Publicación o institución:** The Journal of Finance, 65(5), 1915-1947
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-16 Vehículos: descuentos, réplica y ETF apalancados (principal) · secundarias: TM-11
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1111/j.1540-6261.2010.01598.x · https://ideas.repec.org/a/bla/jfinan/v65y2010i5p1915-1947.html
- **Acceso y licencia:** Artículo de revista de pago; ficha pública
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Fama French 2010 "Luck versus Skill in the Cross-Section of Mutual Fund Returns" Journal of Finance»; WebFetch: sí)
- **Contenido:** Mediante simulaciones bootstrap muestra que pocos fondos activos generan alfa suficiente para cubrir costes; antes de gastos hay evidencia de rendimiento superior e inferior en las colas.
- **Uso en el Motor:** MC-10: método bootstrap de referencia para separar suerte y habilidad al medir la persistencia de categorías de gestión activa.
- **Limitaciones:** EE. UU.; no identifica fondos individuales con fiabilidad.

#### DOC-MOT-0530 · Q 94 (A) — Investor Sentiment and the Closed-End Fund Puzzle

- **Autores:** Charles M. C. Lee; Andrei Shleifer; Richard H. Thaler
- **Año:** 1991
- **Publicación o institución:** The Journal of Finance, 46(1), 75-109 (versión previa: NBER WP 3465, 1990)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-16 Vehículos: descuentos, réplica y ETF apalancados (principal) · secundarias: —
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** https://ideas.repec.org/a/bla/jfinan/v46y1991i1p75-109.html · NBER: https://www.nber.org/papers/w3465
- **Acceso y licencia:** Revista de pago (JSTOR); documento de trabajo NBER y SSRN (abstract=987263) en abierto
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «closed-end fund puzzle Lee Shleifer Thaler 1991 "Investor Sentiment and the Closed-End Fund Puzzle"»; WebFetch: sí)
- **Contenido:** Explica las variaciones del descuento de los fondos cerrados por el sentimiento de los inversores minoristas: los descuentos covarían entre fondos, las emisiones se concentran cuando hay primas y los descuentos se estrechan cuando suben las acciones pequeñas.
- **Uso en el Motor:** MC-02, MC-09: descuento medio de fondos cerrados como indicador de sentimiento y factor común (AC-FON).
- **Limitaciones:** DOI no mostrado en la página leída; interpretación disputada (véanse DOC-MOT-0535 y DOC-MOT-0531).

#### DOC-MOT-0550 · Q 93 (A) — Exchange-Traded Funds 101 for Economists

- **Autores:** Martin Lettau; Ananth Madhavan
- **Año:** 2018
- **Publicación o institución:** Journal of Economic Perspectives, 32(1), 135-154 (versión previa: NBER WP 24250)
- **Tipo de documento:** Artículo de revisión revisado por pares
- **Temática:** TM-16 Vehículos: descuentos, réplica y ETF apalancados (principal) · secundarias: TM-15
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** DOI: 10.1257/jep.32.1.135 · https://ideas.repec.org/a/aea/jecper/v32y2018i1p135-54.html
- **Acceso y licencia:** Acceso abierto (AEA y NBER)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Lettau Madhavan 2018 "Exchange-Traded Funds 101 for Economists" Journal of Economic Perspectives»; WebFetch: sí)
- **Contenido:** Explica la estructura de los ETF (creación/reembolso, arbitraje, primas sobre valor liquidativo), sus diferencias con los fondos de inversión y los riesgos sistémicos alegados.
- **Uso en el Motor:** MC-09: marco conceptual de primas/descuentos y mecanismo de arbitraje de ETF (AC-FON).
- **Limitaciones:** Divulgativo; uno de los autores trabaja en una gestora de ETF.

#### DOC-MOT-0531 · Q 93 (A) — A Liquidity-Based Theory of Closed-End Funds

- **Autores:** Martin Cherkes; Jacob Sagi; Richard Stanton
- **Año:** 2009
- **Publicación o institución:** The Review of Financial Studies, 22(1), 257-297
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-16 Vehículos: descuentos, réplica y ETF apalancados (principal) · secundarias: —
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1093/rfs/hhn028 · https://ideas.repec.org/a/oup/rfinst/v22y2009i1p257-297.html
- **Acceso y licencia:** Artículo de revista de pago; ficha pública
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «closed-end fund discount review Pontiff 1996 "Costly Arbitrage" Berk Stanton 2007 Cherkes Sagi Stanton 2009 liquidity-based theory»; WebFetch: sí)
- **Contenido:** Modelo racional en el que el fondo cerrado ofrece acceso a activos ilíquidos sin costes de negociación; el equilibrio entre beneficio de liquidez y comisiones explica emisiones a prima, descuentos posteriores y oleadas sectoriales de emisiones.
- **Uso en el Motor:** MC-09: modelo de descuento «justo» en función de la iliquidez de la cartera y de las comisiones (AC-FON).
- **Limitaciones:** Contraste empírico limitado a EE. UU.

#### DOC-MOT-0543 · Q 92 (A) — Solving the Return Deviation Conundrum of Leveraged Exchange-Traded Funds

- **Autores:** Hongfei Tang; Xiaoqing Eleanor Xu
- **Año:** 2013
- **Publicación o institución:** Journal of Financial and Quantitative Analysis, 48, 309-342
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-16 Vehículos: descuentos, réplica y ETF apalancados (principal) · secundarias: —
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1017/S0022109012000622 · verificada en página índice: https://www.businessperspectives.org/index.php/journals/investment-management-and-financial-innovations/issue-281/assessing-the-performance-of-american-and-european-leveraged-exchange-traded-funds
- **Acceso y licencia:** Artículo de revista de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Cheng Madhavan 2009 "The Dynamics of Leveraged and Inverse Exchange-Traded Funds" Journal of Investment Management»; WebFetch: sí, sobre la página índice)
- **Contenido:** Descompone la desviación de rentabilidad de los ETF apalancados en efecto de capitalización compuesta (volatilidad), error de seguimiento diario y comisiones.
- **Uso en el Motor:** MC-09: descomposición de la desviación total en componentes atribuibles.
- **Limitaciones:** Confirmada solo por bibliografía.

#### DOC-MOT-0532 · Q 92 (A) — Managerial Ability, Compensation, and the Closed-End Fund Discount

- **Autores:** Jonathan B. Berk; Richard Stanton
- **Año:** 2007
- **Publicación o institución:** The Journal of Finance, 62(2), 529-556
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-16 Vehículos: descuentos, réplica y ETF apalancados (principal) · secundarias: —
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de Bleaney y Smith, Univ. de Nottingham DP 11-05): https://nottingham.ac.uk/economics/documents/discussion-papers/11-05.pdf
- **Acceso y licencia:** Artículo de revista de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «closed-end fund discount review Pontiff 1996 "Costly Arbitrage" Berk Stanton 2007 Cherkes Sagi Stanton 2009 liquidity-based theory»; WebFetch: sí, sobre la página índice)
- **Contenido:** Explica el ciclo de primas y descuentos por el trade-off entre la capacidad del gestor y su remuneración fija a largo plazo, sin recurrir a sentimiento.
- **Uso en el Motor:** MC-09: descuento esperado en función de comisiones y de la capacidad estimada del gestor.
- **Limitaciones:** Confirmada solo por bibliografía; DOI no visto.

#### DOC-MOT-0542 · Q 89 (A) — The Pricing and Performance of Leveraged Exchange-Traded Funds

- **Autores:** Narat Charupat; Peter Miu
- **Año:** 2011
- **Publicación o institución:** Journal of Banking & Finance, 35, 966-977
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-16 Vehículos: descuentos, réplica y ETF apalancados (principal) · secundarias: —
- **Calidad Q:** 89 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1016/j.jbankfin.2010.09.012 · verificada en página índice: https://www.businessperspectives.org/index.php/journals/investment-management-and-financial-innovations/issue-281/assessing-the-performance-of-american-and-european-leveraged-exchange-traded-funds
- **Acceso y licencia:** Artículo de revista de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Cheng Madhavan 2009 "The Dynamics of Leveraged and Inverse Exchange-Traded Funds" Journal of Investment Management»; WebFetch: sí, sobre la página índice)
- **Contenido:** Analiza primas/descuentos sobre valor liquidativo y la desviación de rentabilidad de ETF apalancados canadienses a distintos horizontes.
- **Uso en el Motor:** MC-09: medida de primas/descuentos y de desviación frente al múltiplo en ETF apalancados.
- **Limitaciones:** Mercado canadiense; la bibliografía índice da 2010 (en línea) y vol. 35 (2011).

#### DOC-MOT-0533 · Q 89 (A) — Excess Volatility and Closed-End Funds

- **Autores:** Jeffrey Pontiff
- **Año:** 1997
- **Publicación o institución:** American Economic Review, 87(1), 155-169
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-16 Vehículos: descuentos, réplica y ETF apalancados (principal) · secundarias: TM-03
- **Calidad Q:** 89 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 7/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de Nottingham DP 11-05): https://nottingham.ac.uk/economics/documents/discussion-papers/11-05.pdf
- **Acceso y licencia:** Artículo de revista de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «closed-end fund discount review Pontiff 1996 "Costly Arbitrage" Berk Stanton 2007 Cherkes Sagi Stanton 2009 liquidity-based theory»; WebFetch: sí, sobre la página índice)
- **Contenido:** Muestra que la rentabilidad de las participaciones de fondos cerrados es más volátil que la de su cartera subyacente (exceso de volatilidad), atribuible a variaciones del descuento.
- **Uso en el Motor:** MC-02: descomposición de la volatilidad del fondo cerrado en volatilidad del valor liquidativo y del descuento.
- **Limitaciones:** Confirmada solo por bibliografía.

#### DOC-MOT-0544 · Q 88 (A) — Do Leveraged Exchange-Traded Products Deliver Their Stated Multiples?

- **Autores:** Anthony Loviscek; Hongfei Tang; Xiaoqing Eleanor Xu
- **Año:** 2014
- **Publicación o institución:** Journal of Banking & Finance, 43, 29-47
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-16 Vehículos: descuentos, réplica y ETF apalancados (principal) · secundarias: —
- **Calidad Q:** 88 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 7/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** Verificada en página índice: https://www.businessperspectives.org/index.php/journals/investment-management-and-financial-innovations/issue-281/assessing-the-performance-of-american-and-european-leveraged-exchange-traded-funds (el DOI que da esa bibliografía parece erróneo y se omite)
- **Acceso y licencia:** Artículo de revista de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Cheng Madhavan 2009 "The Dynamics of Leveraged and Inverse Exchange-Traded Funds" Journal of Investment Management»; WebFetch: sí, sobre la página índice)
- **Contenido:** Evalúa si los productos cotizados apalancados entregan el múltiplo prometido a distintos horizontes y en distintos subyacentes.
- **Uso en el Motor:** MC-10: contraste empírico del múltiplo efectivo frente al nominal.
- **Limitaciones:** DOI no confirmado; confirmada solo por bibliografía.

#### DOC-MOT-0541 · Q 88 (A) — The Dynamics of Leveraged and Inverse Exchange-Traded Funds

- **Autores:** Minder Cheng; Ananth Madhavan
- **Año:** 2009
- **Publicación o institución:** Journal of Investment Management, 7(4), 43-62
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-16 Vehículos: descuentos, réplica y ETF apalancados (principal) · secundarias: TM-06
- **Calidad Q:** 88 (A) — Tipo 22/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 8/10 · Acceso 7/10
- **DOI / ISBN / URL:** https://www.joim.com/the-dynamics-of-leveraged-and-inverse-exchange-traded-funds/ · SSRN abstract_id=1539120 (según bibliografía índice)
- **Acceso y licencia:** Revista de pago (registro de invitado); versión SSRN
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Cheng Madhavan 2009 "The Dynamics of Leveraged and Inverse Exchange-Traded Funds" Journal of Investment Management»; WebFetch: sí)
- **Contenido:** Modela el rebalanceo diario de ETF apalancados e inversos: la exposición gamma neta genera flujos de cobertura en el sentido del mercado al cierre y la rentabilidad a horizontes largos diverge del múltiplo por la volatilidad.
- **Uso en el Motor:** MC-09: flujos de rebalanceo previsibles al cierre y divergencia multi-periodo frente al múltiplo nominal.
- **Limitaciones:** Autores de la industria (Barclays Global Investors); páginas tomadas de la bibliografía índice.

#### DOC-MOT-0545 · Q 87 (A) — Intraday Share Price Volatility and Leveraged ETF Rebalancing

- **Autores:** Paul Shum; Walid Hejazi; Edgar Haryanto; Arthur Rodier
- **Año:** 2016
- **Publicación o institución:** Review of Finance, 20, 2379-2409
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-16 Vehículos: descuentos, réplica y ETF apalancados (principal) · secundarias: TM-03
- **Calidad Q:** 87 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 6/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1093/rof/rfv061 · verificada en página índice: https://www.businessperspectives.org/index.php/journals/investment-management-and-financial-innovations/issue-281/assessing-the-performance-of-american-and-european-leveraged-exchange-traded-funds
- **Acceso y licencia:** Artículo de revista de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Cheng Madhavan 2009 "The Dynamics of Leveraged and Inverse Exchange-Traded Funds" Journal of Investment Management»; WebFetch: sí, sobre la página índice)
- **Contenido:** Relaciona el rebalanceo de fin de día de los ETF apalancados con el aumento de la volatilidad intradía al cierre de los componentes.
- **Uso en el Motor:** MC-02: efecto de los flujos de rebalanceo de ETF apalancados en la volatilidad del mercado subyacente.
- **Limitaciones:** Año: la bibliografía índice lo fecha en 2015 (publicación en línea); confirmada solo por bibliografía.

#### DOC-MOT-0534 · Q 86 (A) — Are Discounts on Closed-End Funds a Sentiment Index?

- **Autores:** Nai-Fu Chen; Raymond Kan; Merton H. Miller
- **Año:** 1993
- **Publicación o institución:** The Journal of Finance, 48, 795-800
- **Tipo de documento:** Artículo revisado por pares (comentario)
- **Temática:** TM-16 Vehículos: descuentos, réplica y ETF apalancados (principal) · secundarias: —
- **Calidad Q:** 86 (A) — Tipo 25/25 · Rigor 13/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de Nottingham DP 11-05): https://nottingham.ac.uk/economics/documents/discussion-papers/11-05.pdf
- **Acceso y licencia:** Artículo de revista de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «closed-end fund discount review Pontiff 1996 "Costly Arbitrage" Berk Stanton 2007 Cherkes Sagi Stanton 2009 liquidity-based theory»; WebFetch: sí, sobre la página índice)
- **Contenido:** Réplica crítica a Lee, Shleifer y Thaler: cuestiona la evidencia de que los descuentos sean un índice de sentimiento ligado a las acciones pequeñas.
- **Uso en el Motor:** MC-10: contrapunto metodológico antes de usar descuentos como señal de sentimiento.
- **Limitaciones:** Comentario breve; confirmada solo por bibliografía.

#### DOC-MOT-0551 · Q 84 (A) — Exchange-Traded Funds

- **Autores:** Itzhak Ben-David; Francesco Franzoni; Rabih Moussawi
- **Año:** 2017
- **Publicación o institución:** Annual Review of Financial Economics, 9, 169-189
- **Tipo de documento:** Artículo de revisión (survey)
- **Temática:** TM-16 Vehículos: descuentos, réplica y ETF apalancados (principal) · secundarias: TM-15
- **Calidad Q:** 84 (A) — Tipo 20/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de NBER WP 24250): https://nber.org/system/files/working_papers/w24250/w24250.pdf
- **Acceso y licencia:** Artículo de revista de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Lettau Madhavan 2018 "Exchange-Traded Funds 101 for Economists" Journal of Economic Perspectives»; WebFetch: sí, sobre la página índice)
- **Contenido:** Revisión de la literatura sobre ETF: arbitraje, liquidez, efectos sobre volatilidad y comovimiento de los componentes, y descubrimiento de precios.
- **Uso en el Motor:** MC-09: mapa de efectos de los ETF sobre los mercados subyacentes.
- **Limitaciones:** Confirmada solo por bibliografía.

#### DOC-MOT-0546 · Q 83 (A) — Understanding Bull and Bear ETFs

- **Autores:** Ruben Haga; Snorre Lindset
- **Año:** 2012
- **Publicación o institución:** The European Journal of Finance, 18, 149-165
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-16 Vehículos: descuentos, réplica y ETF apalancados (principal) · secundarias: —
- **Calidad Q:** 83 (A) — Tipo 25/25 · Rigor 14/20 · Autoridad 12/15 · Vigencia 9/10 · Impacto 6/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1080/1351847X.2011.574980 · verificada en página índice: https://www.businessperspectives.org/index.php/journals/investment-management-and-financial-innovations/issue-281/assessing-the-performance-of-american-and-european-leveraged-exchange-traded-funds
- **Acceso y licencia:** Artículo de revista de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Cheng Madhavan 2009 "The Dynamics of Leveraged and Inverse Exchange-Traded Funds" Journal of Investment Management»; WebFetch: sí, sobre la página índice)
- **Contenido:** Deriva la distribución de rentabilidades de ETF apalancados alcistas y bajistas y su dependencia de la volatilidad y del horizonte.
- **Uso en el Motor:** MC-05: simulación de rentabilidades de ETF apalancados a varios horizontes.
- **Limitaciones:** Confirmada solo por bibliografía.

#### DOC-MOT-0554 · Q 83 (A) — ESMA's Guidelines on ETFs and Other UCITS Issues (documento de consulta ESMA/2012/44)

- **Autores:** Autoridad Europea de Valores y Mercados (ESMA)
- **Año:** 2012
- **Publicación o institución:** ESMA, 30/01/2012
- **Tipo de documento:** Documento regulatorio (consulta)
- **Temática:** TM-16 Vehículos: descuentos, réplica y ETF apalancados (principal) · secundarias: TM-14
- **Calidad Q:** 83 (A) — Tipo 18/25 · Rigor 14/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 7/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://www.esma.europa.eu/sites/default/files/library/2015/11/2012-44_0.pdf
- **Acceso y licencia:** Acceso abierto (ESMA)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ESMA guidelines on ETFs and other UCITS issues tracking error tracking difference definition»; WebFetch: sí)
- **Contenido:** Define el error de seguimiento de los UCITS indexados como volatilidad de la diferencia de rentabilidades frente al índice y propone su divulgación (objetivo ex ante y realizado), base de las directrices europeas.
- **Uso en el Motor:** MC-01: definición regulatoria europea de error de seguimiento para el cálculo homogéneo en vehículos UCITS (AC-FON).
- **Limitaciones:** Es la consulta, no las directrices finales; no define la «diferencia de seguimiento».

#### DOC-MOT-0537 · Q 82 (A) — The Impact of Corporate Governance on Closed-end Funds

- **Autores:** Gordon Gemmill; Dylan Thomas
- **Año:** 2006
- **Publicación o institución:** European Financial Management, 12(5), 725-746
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-16 Vehículos: descuentos, réplica y ETF apalancados (principal) · secundarias: —
- **Calidad Q:** 82 (A) — Tipo 25/25 · Rigor 13/20 · Autoridad 12/15 · Vigencia 9/10 · Impacto 6/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de Nottingham DP 11-05): https://nottingham.ac.uk/economics/documents/discussion-papers/11-05.pdf
- **Acceso y licencia:** Artículo de revista de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «closed-end fund discount review Pontiff 1996 "Costly Arbitrage" Berk Stanton 2007 Cherkes Sagi Stanton 2009 liquidity-based theory»; WebFetch: sí, sobre la página índice)
- **Contenido:** Relaciona el descuento de los fondos cerrados británicos con su gobierno corporativo (independencia del consejo, mecanismos de control de descuentos).
- **Uso en el Motor:** MC-09: variables de gobierno como determinantes del descuento en vehículos cotizados europeos.
- **Limitaciones:** Reino Unido; confirmada solo por bibliografía.

#### DOC-MOT-0549 · Q 81 (A) — Assessing the Performance of American and European Leveraged Exchange Traded Funds

- **Autores:** George Tsalikis; Simeon Papadopoulos
- **Año:** 2018
- **Publicación o institución:** Investment Management and Financial Innovations, 15(2), 165-182
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-16 Vehículos: descuentos, réplica y ETF apalancados (principal) · secundarias: —
- **Calidad Q:** 81 (A) — Tipo 25/25 · Rigor 12/20 · Autoridad 10/15 · Vigencia 10/10 · Impacto 4/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** DOI: 10.21511/imfi.15(2).2018.15 · https://www.businessperspectives.org/index.php/journals/investment-management-and-financial-innovations/issue-281/assessing-the-performance-of-american-and-european-leveraged-exchange-traded-funds
- **Acceso y licencia:** Acceso abierto (CC BY 4.0)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Cheng Madhavan 2009 "The Dynamics of Leveraged and Inverse Exchange-Traded Funds" Journal of Investment Management»; WebFetch: sí)
- **Contenido:** Compara ETF apalancados de EE. UU. y Europa desde su lanzamiento: cumplen el múltiplo a un día y hasta una semana, con desviaciones crecientes a un mes, mayores en los bajistas.
- **Uso en el Motor:** MC-10: evidencia europea sobre horizonte de validez del múltiplo; su bibliografía sirve de índice del área.
- **Limitaciones:** Revista de impacto modesto.

#### DOC-MOT-0547 · Q 81 (A) — Long Term Performance of Leveraged ETFs

- **Autores:** Lei Lu; Jun Wang; Ge Zhang
- **Año:** 2012
- **Publicación o institución:** Financial Services Review, 21, 63-80
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-16 Vehículos: descuentos, réplica y ETF apalancados (principal) · secundarias: —
- **Calidad Q:** 81 (A) — Tipo 25/25 · Rigor 13/20 · Autoridad 11/15 · Vigencia 9/10 · Impacto 6/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.2139/ssrn.1344133 (versión SSRN) · verificada en página índice: https://www.businessperspectives.org/index.php/journals/investment-management-and-financial-innovations/issue-281/assessing-the-performance-of-american-and-european-leveraged-exchange-traded-funds
- **Acceso y licencia:** Versión SSRN en abierto
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Cheng Madhavan 2009 "The Dynamics of Leveraged and Inverse Exchange-Traded Funds" Journal of Investment Management»; WebFetch: sí, sobre la página índice)
- **Contenido:** Mide la desviación de ETF apalancados ultra frente al múltiplo a horizontes de semanas a un año.
- **Uso en el Motor:** MC-10: umbrales de horizonte a partir de los cuales el múltiplo deja de cumplirse.
- **Limitaciones:** Confirmada solo por bibliografía.

#### DOC-MOT-0536 · Q 80 (A) — Closed-End Funds: A Survey

- **Autores:** Elroy Dimson; Carolina Minio-Kozerski
- **Año:** 1999
- **Publicación o institución:** Financial Markets, Institutions and Instruments, 8, 1-41
- **Tipo de documento:** Artículo de revisión (survey)
- **Temática:** TM-16 Vehículos: descuentos, réplica y ETF apalancados (principal) · secundarias: —
- **Calidad Q:** 80 (A) — Tipo 20/25 · Rigor 14/20 · Autoridad 14/15 · Vigencia 8/10 · Impacto 7/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de Nottingham DP 11-05): https://nottingham.ac.uk/economics/documents/discussion-papers/11-05.pdf
- **Acceso y licencia:** Artículo de revista de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «closed-end fund discount review Pontiff 1996 "Costly Arbitrage" Berk Stanton 2007 Cherkes Sagi Stanton 2009 liquidity-based theory»; WebFetch: sí, sobre la página índice)
- **Contenido:** Revisión de las teorías y la evidencia sobre descuentos de fondos cerrados (comisiones, fiscalidad, iliquidez, sentimiento) con atención al mercado británico de investment trusts.
- **Uso en el Motor:** MC-09: mapa de factores explicativos del descuento para fondos cerrados europeos.
- **Limitaciones:** Anterior a la literatura de liquidez de 2007-2009; confirmada solo por bibliografía.

#### DOC-MOT-0548 · Q 79 (B) — A Tracking Error Approach to Leveraged ETFs: Are They Really That Bad?

- **Autores:** Vipul Bansal; Jeffrey Marshall
- **Año:** 2015
- **Publicación o institución:** Global Finance Journal, 26, 47-63
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-16 Vehículos: descuentos, réplica y ETF apalancados (principal) · secundarias: —
- **Calidad Q:** 79 (B) — Tipo 25/25 · Rigor 12/20 · Autoridad 11/15 · Vigencia 9/10 · Impacto 5/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1016/j.gfj.2015.01.004 · verificada en página índice: https://www.businessperspectives.org/index.php/journals/investment-management-and-financial-innovations/issue-281/assessing-the-performance-of-american-and-european-leveraged-exchange-traded-funds
- **Acceso y licencia:** Artículo de revista de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Cheng Madhavan 2009 "The Dynamics of Leveraged and Inverse Exchange-Traded Funds" Journal of Investment Management»; WebFetch: sí, sobre la página índice)
- **Contenido:** Mide el error de seguimiento de ETF apalancados frente al objetivo diario y frente a una cartera apalancada equivalente.
- **Uso en el Motor:** MC-09: definición de error de seguimiento adaptada a productos con objetivo diario.
- **Limitaciones:** Confirmada solo por bibliografía.

#### DOC-MOT-0553 · Q 78 (B) — A Comprehensive Guide to Exchange-Traded Funds (ETFs)

- **Autores:** Joanne M. Hill; Dave Nadig; Matt Hougan; Deborah Fuhr
- **Año:** 2015
- **Publicación o institución:** CFA Institute Research Foundation
- **Tipo de documento:** Monografía de fundación profesional
- **Temática:** TM-16 Vehículos: descuentos, réplica y ETF apalancados (principal) · secundarias: —
- **Calidad Q:** 78 (B) — Tipo 15/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 6/10 · Independencia 8/10 · Acceso 10/10
- **DOI / ISBN / URL:** SSRN abstract_id=2616223 (según bibliografía índice) · verificada en página índice: https://www.businessperspectives.org/index.php/journals/investment-management-and-financial-innovations/issue-281/assessing-the-performance-of-american-and-european-leveraged-exchange-traded-funds
- **Acceso y licencia:** Acceso abierto (CFA Institute Research Foundation)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Cheng Madhavan 2009 "The Dynamics of Leveraged and Inverse Exchange-Traded Funds" Journal of Investment Management»; WebFetch: sí, sobre la página índice)
- **Contenido:** Guía completa de ETF: estructuras, creación/reembolso, costes totales de tenencia, error y diferencia de seguimiento, ETF apalancados e inversos.
- **Uso en el Motor:** MC-09: definiciones operativas de coste total, diferencia de seguimiento y primas/descuentos.
- **Limitaciones:** Autores de la industria; confirmada solo por bibliografía.

#### DOC-MOT-0535 · Q 78 (B) — Neoclassical Finance, Alternative Finance and the Closed-End Fund Puzzle

- **Autores:** Stephen A. Ross
- **Año:** 2002
- **Publicación o institución:** European Financial Management, 8(2), 129-137
- **Tipo de documento:** Artículo revisado por pares (ensayo)
- **Temática:** TM-16 Vehículos: descuentos, réplica y ETF apalancados (principal) · secundarias: —
- **Calidad Q:** 78 (B) — Tipo 17/25 · Rigor 13/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 7/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de Nottingham DP 11-05): https://nottingham.ac.uk/economics/documents/discussion-papers/11-05.pdf
- **Acceso y licencia:** Artículo de revista de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «closed-end fund discount review Pontiff 1996 "Costly Arbitrage" Berk Stanton 2007 Cherkes Sagi Stanton 2009 liquidity-based theory»; WebFetch: sí, sobre la página índice)
- **Contenido:** Muestra que comisiones y distribuciones bastan, en un marco neoclásico, para generar descuentos del orden observado, sin sentimiento.
- **Uso en el Motor:** MC-09: descuento de equilibrio como valor presente de las comisiones frente al rendimiento distribuido.
- **Limitaciones:** Ensayo teórico; confirmada solo por bibliografía.

#### DOC-MOT-0552 · Q 75 (B) — Exchange-Traded Funds and the New Dynamics of Investing

- **Autores:** Ananth Madhavan
- **Año:** 2016
- **Publicación o institución:** Oxford University Press, Nueva York
- **Tipo de documento:** Libro de referencia
- **Temática:** TM-16 Vehículos: descuentos, réplica y ETF apalancados (principal) · secundarias: TM-15
- **Calidad Q:** 75 (B) — Tipo 17/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 7/10 · Independencia 7/10 · Acceso 5/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de NBER WP 24250): https://nber.org/system/files/working_papers/w24250/w24250.pdf
- **Acceso y licencia:** Libro comercial
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Lettau Madhavan 2018 "Exchange-Traded Funds 101 for Economists" Journal of Economic Perspectives»; WebFetch: sí, sobre la página índice)
- **Contenido:** Monografía sobre estructura, valoración, liquidez y efectos de mercado de los ETF, incluidos los apalancados y los de factores.
- **Uso en el Motor:** MC-09: manual de consulta sobre mecánica de ETF.
- **Limitaciones:** Autor de la industria; ISBN no visto.

#### DOC-MOT-0557 · Q 69 (B) — Price Dynamics and Liquidity of Exchange-Traded Funds

- **Autores:** Ananth Madhavan; Aleksander Sobczyk
- **Año:** 2016
- **Publicación o institución:** Journal of Investment Management (en prensa en 2016, según bibliografía índice)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-16 Vehículos: descuentos, réplica y ETF apalancados (principal) · secundarias: —
- **Calidad Q:** 69 (B) — Tipo 15/25 · Rigor 13/20 · Autoridad 12/15 · Vigencia 9/10 · Impacto 5/10 · Independencia 8/10 · Acceso 7/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de NBER WP 24250, que escribe «Sobcyzk»): https://nber.org/system/files/working_papers/w24250/w24250.pdf
- **Acceso y licencia:** Artículo de revista de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Lettau Madhavan 2018 "Exchange-Traded Funds 101 for Economists" Journal of Economic Perspectives»; WebFetch: sí, sobre la página índice)
- **Contenido:** Modelo de la dinámica de la prima/descuento de los ETF sobre su valor liquidativo y de su reversión por arbitraje, con implicaciones para la liquidez.
- **Uso en el Motor:** MC-02: modelización de la reversión de primas/descuentos de ETF.
- **Limitaciones:** Volumen y páginas no confirmados; autores de la industria.

## TM-17 Mercado monetario: rentabilidades equivalentes y expectativas implícitas

#### DOC-MOT-0560 · Q 97 (A) — Market-Based Measures of Monetary Policy Expectations

- **Autores:** Refet S. Gürkaynak; Brian P. Sack; Eric T. Swanson
- **Año:** 2007
- **Publicación o institución:** Journal of Business & Economic Statistics, 25(2), 201-212 (versiones previas: FEDS 2002-40; FRBSF WP 2006-04)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-17 Mercado monetario: rentabilidades equivalentes y expectativas implícitas (principal) · secundarias: TM-05
- **Calidad Q:** 97 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** DOI: 10.1198/073500106000000387 · https://sites.socsci.uci.edu/~swanson2/papers/mbmmpe.pdf
- **Acceso y licencia:** Versión del autor en abierto
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Gürkaynak Sack Swanson "Market-Based Measures of Monetary Policy Expectations" federal funds futures Eurodollar»; WebFetch: sí)
- **Contenido:** Compara la capacidad de futuros sobre fondos federales, depósitos y futuros de eurodólar, letras y papel comercial para predecir el tipo oficial: los futuros sobre fondos federales dominan a 1-6 meses y varios instrumentos empatan a 3-4 trimestres; todos superan a un VAR bayesiano.
- **Uso en el Motor:** MC-03, MC-09: elección del instrumento para extraer la senda esperada del tipo oficial por horizonte y medida de sorpresas de política (AC-MON).
- **Limitaciones:** EE. UU. y era pre-SOFR (los eurodólares han desaparecido); no ajusta primas de plazo variables.

#### DOC-MOT-0567 · Q 93 (A) — Reforming LIBOR and Other Financial Market Benchmarks

- **Autores:** Darrell Duffie; Jeremy C. Stein
- **Año:** 2015
- **Publicación o institución:** Journal of Economic Perspectives, 29(2), 191-212
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-17 Mercado monetario: rentabilidades equivalentes y expectativas implícitas (principal) · secundarias: TM-14
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de Schrimpf y Sushko 2019, BIS): https://bis.org/publ/qtrpdf/r_qt1903e.htm
- **Acceso y licencia:** Acceso abierto (AEA)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Schrimpf Sushko 2019 "Beyond LIBOR: a primer on the new reference rates" BIS Quarterly Review»; WebFetch: sí, sobre la página índice)
- **Contenido:** Analiza los fallos de diseño del LIBOR y propone principios para índices de referencia robustos basados en transacciones.
- **Uso en el Motor:** MC-01: criterios para elegir el tipo de referencia en cálculos de rentabilidad monetaria.
- **Limitaciones:** Confirmada solo por bibliografía, que lo titula «Reforming LIBOR and other financial benchmarks».

#### DOC-MOT-0572 · Q 93 (A) — What Explains the Stock Market's Reaction to Federal Reserve Policy?

- **Autores:** Ben S. Bernanke; Kenneth N. Kuttner
- **Año:** 2005
- **Publicación o institución:** The Journal of Finance, 60, 1221-1259
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-17 Mercado monetario: rentabilidades equivalentes y expectativas implícitas (principal) · secundarias: TM-04
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de Gürkaynak, Sack y Swanson 2007): https://sites.socsci.uci.edu/~swanson2/papers/mbmmpe.pdf
- **Acceso y licencia:** Artículo de revista de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Gürkaynak Sack Swanson "Market-Based Measures of Monetary Policy Expectations" federal funds futures Eurodollar»; WebFetch: sí, sobre la página índice)
- **Contenido:** Usa sorpresas de futuros sobre fondos federales para estimar la reacción de la bolsa a la política monetaria y descompone el efecto en dividendos, tipos reales y prima de riesgo.
- **Uso en el Motor:** MC-03: traslado de las sorpresas monetarias a otros activos.
- **Limitaciones:** Confirmada solo por bibliografía.

#### DOC-MOT-0562 · Q 93 (A) — Monetary Policy Surprises and Interest Rates: Evidence from the Fed Funds Futures Market

- **Autores:** Kenneth N. Kuttner
- **Año:** 2001
- **Publicación o institución:** Journal of Monetary Economics, 47, 523-544
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-17 Mercado monetario: rentabilidades equivalentes y expectativas implícitas (principal) · secundarias: TM-04
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de Gürkaynak, Sack y Swanson 2007): https://sites.socsci.uci.edu/~swanson2/papers/mbmmpe.pdf
- **Acceso y licencia:** Artículo de revista de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Gürkaynak Sack Swanson "Market-Based Measures of Monetary Policy Expectations" federal funds futures Eurodollar»; WebFetch: sí, sobre la página índice)
- **Contenido:** Separa los cambios del tipo oficial en esperados e inesperados con futuros sobre fondos federales y muestra que solo la sorpresa mueve los tipos de mercado.
- **Uso en el Motor:** MC-03: cálculo de la sorpresa de política a partir del futuro del mes corriente (con ajuste por días restantes).
- **Limitaciones:** Confirmada solo por bibliografía (título resumido en ella).

#### DOC-MOT-0563 · Q 92 (A) — Measuring Euro Area Monetary Policy

- **Autores:** Carlo Altavilla; Luca Brugnolini; Refet S. Gürkaynak; Roberto Motto; Giuseppe Ragusa
- **Año:** 2019
- **Publicación o institución:** Journal of Monetary Economics, 108, 162-179
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-17 Mercado monetario: rentabilidades equivalentes y expectativas implícitas (principal) · secundarias: TM-04
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1016/j.jmoneco.2019.08.016 · https://ideas.repec.org/a/eee/moneco/v108y2019icp162-179.html
- **Acceso y licencia:** Revista de pago; base de datos EA-MPD pública
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Altavilla Brugnolini Gürkaynak Motto Ragusa 2019 "Measuring euro area monetary policy" Journal of Monetary Economics»; WebFetch: sí)
- **Contenido:** Crea la base de datos pública EA-MPD de variaciones intradía en torno a las decisiones del BCE e identifica tres factores (tipo objetivo, orientación futura y QE) que explican casi toda la variación de la curva.
- **Uso en el Motor:** MC-03: sorpresas de política del BCE por tramo de curva monetaria; insumo europeo para AC-MON.
- **Limitaciones:** Requiere datos intradía para replicar.

#### DOC-MOT-0570 · Q 92 (A) — Futures Prices as Risk-Adjusted Forecasts of Monetary Policy

- **Autores:** Monika Piazzesi; Eric T. Swanson
- **Año:** 2008
- **Publicación o institución:** Journal of Monetary Economics, pp. 677-691 (versiones previas: NBER WP 10547, 2004; FRBSF WP 2006-23)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-17 Mercado monetario: rentabilidades equivalentes y expectativas implícitas (principal) · secundarias: TM-05
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1016/j.jmoneco.2008.04.003 · https://academicnewsletter.sufe.edu.cn/info/278524 · versión del autor: https://web.stanford.edu/~piazzesi/fff.pdf
- **Acceso y licencia:** Revista de pago; versiones de trabajo en abierto (NBER, FRBSF, páginas de los autores)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Piazzesi Swanson 2008 "Futures prices as risk-adjusted forecasts of monetary policy" Journal of Monetary Economics»; WebFetch: sí)
- **Contenido:** Los excesos de rentabilidad de los futuros sobre fondos federales (y de eurodólar) son en media positivos y contracíclicos, predecibles con el crecimiento del empleo, la pendiente de la curva y los diferenciales corporativos; ignorar esta prima sesga la senda implícita del tipo oficial.
- **Uso en el Motor:** MC-09: corrección de la prima de plazo a corto antes de leer expectativas de tipos en futuros y OIS (AC-MON, AC-TCV).
- **Limitaciones:** EE. UU.; volumen no mostrado en la página leída.

#### DOC-MOT-0561 · Q 89 (A) — Estimating Nominal Interest Rate Expectations: Overnight Indexed Swaps and the Term Structure

- **Autores:** Simon P. Lloyd
- **Año:** 2020
- **Publicación o institución:** Journal of Banking & Finance, 119 (artículo 105915) (versiones previas: Cambridge WP 1734; Bank of England Staff WP 763)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-17 Mercado monetario: rentabilidades equivalentes y expectativas implícitas (principal) · secundarias: TM-05
- **Calidad Q:** 89 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 6/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1016/j.jbankfin.2020.105915 · https://ideas.repec.org/a/eee/jbfina/v119y2020ics0378426620301771.html · documento de trabajo: https://www.bankofengland.co.uk/working-paper/2018/estimating-nominal-interest-rate-expectations-overnight-indexed-swaps-and-the-term-structure
- **Acceso y licencia:** Revista de pago; documento de trabajo del Banco de Inglaterra en abierto
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Lloyd "Estimating nominal interest rate expectations: Overnight indexed swaps and the term structure" Journal of Banking and Finance»; WebFetch: sí)
- **Contenido:** Añade tipos OIS de 3 a 24 meses a un modelo afín gaussiano de la curva para separar diariamente expectativas de tipos y primas de plazo; las expectativas resultantes siguen a las encuestas hasta 10 años.
- **Uso en el Motor:** MC-09: extracción de expectativas de tipo oficial a partir de la curva OIS con corrección por prima de plazo (AC-MON, AC-TCV).
- **Limitaciones:** Aplicación principal a EE. UU.

#### DOC-MOT-0564 · Q 89 (A) — The Term Structure of Very Short-Term Rates: New Evidence for the Expectations Hypothesis

- **Autores:** Francis A. Longstaff
- **Año:** 2000
- **Publicación o institución:** Journal of Financial Economics, 58(3), 397-415
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-17 Mercado monetario: rentabilidades equivalentes y expectativas implícitas (principal) · secundarias: TM-05
- **Calidad Q:** 89 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** https://ideas.repec.org/a/eee/jfinec/v58y2000i3p397-415.html
- **Acceso y licencia:** Artículo de revista de pago; ficha pública
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Longstaff 2000 "The term structure of very short-term rates: New evidence for the expectations hypothesis" Journal of Financial Economics»; WebFetch: sí)
- **Contenido:** Con tipos repo de un día a tres meses no rechaza la hipótesis de expectativas en el tramo muy corto, a diferencia de la evidencia en plazos largos.
- **Uso en el Motor:** MC-09: justificación de leer tipos repo/OIS cortos como expectativas casi sin prima.
- **Limitaciones:** DOI no mostrado en la página leída; ver la réplica de DOC-MOT-0565.

#### DOC-MOT-0566 · Q 88 (A) — Beyond LIBOR: A Primer on the New Benchmark Rates

- **Autores:** Andreas Schrimpf; Vladyslav Sushko
- **Año:** 2019
- **Publicación o institución:** BIS Quarterly Review, marzo de 2019 (artículo especial), Banco de Pagos Internacionales
- **Tipo de documento:** Artículo de publicación de organismo internacional
- **Temática:** TM-17 Mercado monetario: rentabilidades equivalentes y expectativas implícitas (principal) · secundarias: TM-14
- **Calidad Q:** 88 (A) — Tipo 20/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 7/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://bis.org/publ/qtrpdf/r_qt1903e.htm
- **Acceso y licencia:** Acceso abierto (BPI)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Schrimpf Sushko 2019 "Beyond LIBOR: a primer on the new reference rates" BIS Quarterly Review»; WebFetch: sí)
- **Contenido:** Explica la sustitución de los IBOR por tipos libres de riesgo a un día (SOFR, SONIA, SARON, €STR), los tipos a plazo retrospectivos (compuestos) y prospectivos (de OIS/futuros) y las diferencias entre tipos garantizados y no garantizados.
- **Uso en el Motor:** MC-01: convenciones de capitalización en retrospectiva y construcción de tipos a plazo a partir de tipos a un día (AC-MON).
- **Limitaciones:** Situación de 2019; el €STR ya sustituyó al EONIA.

#### DOC-MOT-0565 · Q 88 (A) — The Expectation Hypothesis of the Term Structure of Very Short-Term Rates: Statistical Tests and Economic Value

- **Autores:** Pasquale Della Corte; Lucio Sarno; Daniel L. Thornton
- **Año:** 2008
- **Publicación o institución:** Journal of Financial Economics, 89(1), 158-174
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-17 Mercado monetario: rentabilidades equivalentes y expectativas implícitas (principal) · secundarias: TM-05, TM-11
- **Calidad Q:** 88 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 6/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1016/j.jfineco.2007.08.002 · https://academicnewsletter.sufe.edu.cn/info/357315
- **Acceso y licencia:** Revista de pago; versión de trabajo en City Research Online
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Longstaff 2000 "The term structure of very short-term rates: New evidence for the expectations hypothesis" Journal of Financial Economics»; WebFetch: sí)
- **Contenido:** Con contrastes más potentes rechaza estadísticamente la hipótesis de expectativas en repos de un día a tres meses, pero una estrategia de negociación muestra que las desviaciones carecen de valor económico.
- **Uso en el Motor:** MC-10: distinción entre significación estadística y económica de las primas de plazo a corto.
- **Limitaciones:** Volumen y número tomados del identificador RePEc (econpapers) de la búsqueda.

#### DOC-MOT-0575 · Q 87 (A) — Price, Yield and Rate Calculations for a Treasury Bill

- **Autores:** Departamento del Tesoro de EE. UU. (TreasuryDirect)
- **Año:** 2004 (ejemplo de letra emitida el 22/01/2004)
- **Publicación o institución:** U.S. Department of the Treasury, Bureau of the Public Debt
- **Tipo de documento:** Documento técnico oficial
- **Temática:** TM-17 Mercado monetario: rentabilidades equivalentes y expectativas implícitas (principal) · secundarias: TM-01
- **Calidad Q:** 87 (A) — Tipo 20/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 6/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://www.treasurydirect.gov/instit/annceresult/press/preanre/2004/ofcalc6decbill.pdf
- **Acceso y licencia:** Acceso abierto (dominio público)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «TreasuryDirect Treasury bills discount rate investment rate coupon equivalent yield formula»; WebFetch: sí)
- **Contenido:** Fórmulas oficiales de precio a partir del tipo de descuento (base 360), tipo de descuento a partir del precio y rentabilidad equivalente de cupón (base 365/366), incluida la solución cuadrática para letras a más de medio año.
- **Uso en el Motor:** MC-01: conversión exacta entre tipo de descuento, rentabilidad de inversión y rentabilidad equivalente anual para comparar liquidez entre instrumentos (AC-MON).
- **Limitaciones:** Convención estadounidense; otros mercados usan otras bases (Act/360 en la zona del euro).

#### DOC-MOT-0568 · Q 87 (A) — The Fed Funds Futures Rate as a Predictor of Federal Reserve Policy

- **Autores:** Joel T. Krueger; Kenneth N. Kuttner
- **Año:** 1996
- **Publicación o institución:** Journal of Futures Markets, 16, 865-879
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-17 Mercado monetario: rentabilidades equivalentes y expectativas implícitas (principal) · secundarias: —
- **Calidad Q:** 87 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 7/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de Gürkaynak, Sack y Swanson 2007): https://sites.socsci.uci.edu/~swanson2/papers/mbmmpe.pdf
- **Acceso y licencia:** Artículo de revista de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Gürkaynak Sack Swanson "Market-Based Measures of Monetary Policy Expectations" federal funds futures Eurodollar»; WebFetch: sí, sobre la página índice)
- **Contenido:** Muestra que el tipo de los futuros sobre fondos federales es un predictor eficiente (casi insesgado) del tipo oficial a corto plazo.
- **Uso en el Motor:** MC-09: base para leer la probabilidad implícita de cambio de tipos en la siguiente reunión.
- **Limitaciones:** Confirmada solo por bibliografía (título resumido en ella).

#### DOC-MOT-0571 · Q 86 (A) — Anticipations of Monetary Policy in Financial Markets

- **Autores:** Joe Lange; Brian Sack; William Whitesell
- **Año:** 2003
- **Publicación o institución:** Journal of Money, Credit, and Banking, 35, 889-909
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-17 Mercado monetario: rentabilidades equivalentes y expectativas implícitas (principal) · secundarias: —
- **Calidad Q:** 86 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 6/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de Gürkaynak, Sack y Swanson 2007): https://sites.socsci.uci.edu/~swanson2/papers/mbmmpe.pdf
- **Acceso y licencia:** Artículo de revista de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Gürkaynak Sack Swanson "Market-Based Measures of Monetary Policy Expectations" federal funds futures Eurodollar»; WebFetch: sí, sobre la página índice)
- **Contenido:** Mide con qué antelación los mercados monetarios anticipan los cambios del tipo oficial y cómo ha mejorado esa anticipación.
- **Uso en el Motor:** MC-03: horizonte de anticipación de las decisiones en la curva monetaria.
- **Limitaciones:** Confirmada solo por bibliografía; títulos resumidos en ella.

#### DOC-MOT-0569 · Q 85 (A) — Predicting Monetary Policy with Federal Funds Futures Prices

- **Autores:** Ulf Söderström
- **Año:** 2001
- **Publicación o institución:** Journal of Futures Markets, 21, 377-391
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-17 Mercado monetario: rentabilidades equivalentes y expectativas implícitas (principal) · secundarias: —
- **Calidad Q:** 85 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 12/15 · Vigencia 10/10 · Impacto 6/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de Gürkaynak, Sack y Swanson 2007): https://sites.socsci.uci.edu/~swanson2/papers/mbmmpe.pdf
- **Acceso y licencia:** Artículo de revista de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Gürkaynak Sack Swanson "Market-Based Measures of Monetary Policy Expectations" federal funds futures Eurodollar»; WebFetch: sí, sobre la página índice)
- **Contenido:** Evalúa la capacidad predictiva de los futuros sobre fondos federales para las decisiones del FOMC y sus sesgos.
- **Uso en el Motor:** MC-10: validación del poder predictivo de futuros de tipos.
- **Limitaciones:** Confirmada solo por bibliografía.

#### DOC-MOT-0576 · Q 84 (A) — The Euro Short-Term Rate (€STR) Methodology and Policies

- **Autores:** Banco Central Europeo
- **Año:** Versión vigente en la web del BCE (fecha de versión no confirmada)
- **Publicación o institución:** Banco Central Europeo
- **Tipo de documento:** Metodología oficial de índice de referencia
- **Temática:** TM-17 Mercado monetario: rentabilidades equivalentes y expectativas implícitas (principal) · secundarias: TM-14
- **Calidad Q:** 84 (A) — Tipo 18/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 5/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://www.ecb.europa.eu/stats/euro-short-term-rates/interest_rate_benchmarks/shared/pdf/ecb.ESTER_methodology_and_policies.cs.pdf (resultado de búsqueda; versión inglesa en el mismo directorio)
- **Acceso y licencia:** Acceso abierto (BCE)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «ECB euro short-term rate €STR methodology and policies calculation volume-weighted trimmed mean»; WebFetch: no (la versión inglesa no estaba permitida para lectura))
- **Contenido:** Documento oficial que define las operaciones admisibles, el recorte de colas, la media ponderada por volumen y las políticas de contingencia del €STR.
- **Uso en el Motor:** MC-01: base del tipo a un día del euro para capitalizar rendimientos monetarios y construir tipos compuestos (AC-MON).
- **Limitaciones:** No leído en esta verificación; fecha de versión pendiente.

#### DOC-MOT-0580 · Q 83 (A) — Report by the Working Group on Euro Risk-Free Rates on the Transition from EONIA to ESTER

- **Autores:** Banco Central Europeo (grupo de trabajo sobre tipos libres de riesgo del euro)
- **Año:** 2018
- **Publicación o institución:** BCE, diciembre de 2018
- **Tipo de documento:** Informe oficial de grupo de trabajo de banco central
- **Temática:** TM-17 Mercado monetario: rentabilidades equivalentes y expectativas implícitas (principal) · secundarias: TM-14
- **Calidad Q:** 83 (A) — Tipo 17/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 7/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de Schrimpf y Sushko 2019, BIS): https://bis.org/publ/qtrpdf/r_qt1903e.htm
- **Acceso y licencia:** Acceso abierto (BCE)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Schrimpf Sushko 2019 "Beyond LIBOR: a primer on the new reference rates" BIS Quarterly Review»; WebFetch: sí, sobre la página índice)
- **Contenido:** Recomendaciones para la transición del EONIA al €STR, incluida la relación fija EONIA = €STR + diferencial y sus implicaciones para curvas OIS y contratos.
- **Uso en el Motor:** MC-01: empalme de series históricas EONIA/€STR en cálculos de curvas OIS del euro (AC-MON).
- **Limitaciones:** Confirmada solo por bibliografía; título tal como lo da la fuente índice.

#### DOC-MOT-0581 · Q 82 (A) — Second Report of the Alternative Reference Rates Committee

- **Autores:** Federal Reserve Bank of New York — Alternative Reference Rates Committee (ARRC)
- **Año:** 2018
- **Publicación o institución:** FRBNY, marzo de 2018
- **Tipo de documento:** Informe oficial de comité de mercado auspiciado por banco central
- **Temática:** TM-17 Mercado monetario: rentabilidades equivalentes y expectativas implícitas (principal) · secundarias: TM-14
- **Calidad Q:** 82 (A) — Tipo 17/25 · Rigor 14/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 7/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de Schrimpf y Sushko 2019, BIS): https://bis.org/publ/qtrpdf/r_qt1903e.htm
- **Acceso y licencia:** Acceso abierto (Reserva Federal de Nueva York)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Schrimpf Sushko 2019 "Beyond LIBOR: a primer on the new reference rates" BIS Quarterly Review»; WebFetch: sí, sobre la página índice)
- **Contenido:** Hoja de ruta de la transición del LIBOR en dólares al SOFR y desarrollo de mercados de futuros y OIS sobre SOFR.
- **Uso en el Motor:** MC-01: convenciones del SOFR y construcción de su curva a plazo (AC-MON).
- **Limitaciones:** Confirmada solo por bibliografía.

#### DOC-MOT-0582 · Q 82 (A) — SONIA: Key Features and Policies

- **Autores:** Bank of England
- **Año:** 2018
- **Publicación o institución:** Bank of England, noviembre de 2018
- **Tipo de documento:** Metodología oficial de índice de referencia
- **Temática:** TM-17 Mercado monetario: rentabilidades equivalentes y expectativas implícitas (principal) · secundarias: TM-14
- **Calidad Q:** 82 (A) — Tipo 18/25 · Rigor 14/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 6/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de Schrimpf y Sushko 2019, BIS): https://bis.org/publ/qtrpdf/r_qt1903e.htm
- **Acceso y licencia:** Acceso abierto (Banco de Inglaterra)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Schrimpf Sushko 2019 "Beyond LIBOR: a primer on the new reference rates" BIS Quarterly Review»; WebFetch: sí, sobre la página índice)
- **Contenido:** Definición, fuentes de datos (operaciones a un día no garantizadas), cálculo por media recortada ponderada por volumen y políticas del tipo SONIA reformado.
- **Uso en el Motor:** MC-01: cálculo y capitalización del tipo a un día de la libra (AC-MON).
- **Limitaciones:** Confirmada solo por bibliografía; puede haber versiones posteriores.

#### DOC-MOT-0578 · Q 81 (A) — Repo Market Functioning

- **Autores:** Committee on the Global Financial System (CGFS)
- **Año:** 2017
- **Publicación o institución:** CGFS Papers n.º 59 (abril de 2017), Banco de Pagos Internacionales
- **Tipo de documento:** Informe de comité de bancos centrales
- **Temática:** TM-17 Mercado monetario: rentabilidades equivalentes y expectativas implícitas (principal) · secundarias: —
- **Calidad Q:** 81 (A) — Tipo 17/25 · Rigor 14/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 6/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de Schrimpf y Sushko 2019, BIS): https://bis.org/publ/qtrpdf/r_qt1903e.htm
- **Acceso y licencia:** Acceso abierto (BPI)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Schrimpf Sushko 2019 "Beyond LIBOR: a primer on the new reference rates" BIS Quarterly Review»; WebFetch: sí, sobre la página índice)
- **Contenido:** Analiza el funcionamiento de los mercados de repos tras la regulación poscrisis, sus primas de fin de trimestre y su papel en la transmisión monetaria.
- **Uso en el Motor:** MC-02: explicación de saltos estacionales de tipos repo garantizados (fin de trimestre/año).
- **Limitaciones:** Confirmada solo por bibliografía.

#### DOC-MOT-0573 · Q 81 (A) — The Term Structure of Commercial Paper Rates

- **Autores:** Chris Downing; Stephen Oliner
- **Año:** 2004
- **Publicación o institución:** Federal Reserve Board, FEDS Working Paper 2004-18
- **Tipo de documento:** Documento de trabajo de banco central
- **Temática:** TM-17 Mercado monetario: rentabilidades equivalentes y expectativas implícitas (principal) · secundarias: —
- **Calidad Q:** 81 (A) — Tipo 17/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 5/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de Gürkaynak, Sack y Swanson 2007): https://sites.socsci.uci.edu/~swanson2/papers/mbmmpe.pdf
- **Acceso y licencia:** Acceso abierto (Reserva Federal)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Gürkaynak Sack Swanson "Market-Based Measures of Monetary Policy Expectations" federal funds futures Eurodollar»; WebFetch: sí, sobre la página índice)
- **Contenido:** Estudia la estructura de plazos del papel comercial y su contenido de expectativas y primas.
- **Uso en el Motor:** MC-09: diferenciales de papel comercial frente a tipos sin riesgo en la curva monetaria.
- **Limitaciones:** Confirmada solo por bibliografía; título resumido en ella.

#### DOC-MOT-0577 · Q 81 (A) — Gauging the Market's Expectations about Monetary Policy

- **Autores:** Simon Kwan
- **Año:** 2004
- **Publicación o institución:** FRBSF Economic Letter 2004-28 (08/10/2004), Federal Reserve Bank of San Francisco
- **Tipo de documento:** Nota divulgativa de banco central
- **Temática:** TM-17 Mercado monetario: rentabilidades equivalentes y expectativas implícitas (principal) · secundarias: —
- **Calidad Q:** 81 (A) — Tipo 17/25 · Rigor 13/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 7/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://www.frbsf.org/research-and-insights/publications/economic-letter/2004/10/gauging-market-expectations-about-monetary-policy
- **Acceso y licencia:** Acceso abierto (Fed de San Francisco)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Gürkaynak Sack Swanson "Market-Based Measures of Monetary Policy Expectations" federal funds futures Eurodollar»; WebFetch: sí)
- **Contenido:** Explica cómo extraer la senda esperada del tipo oficial de seis instrumentos monetarios y advierte de las primas de riesgo variables a horizontes largos.
- **Uso en el Motor:** MC-09: guía didáctica del cálculo de expectativas implícitas.
- **Limitaciones:** Divulgativo; instrumentos de la era LIBOR.

#### DOC-MOT-0579 · Q 80 (A) — What Drives Interbank Rates? Evidence from the Libor Panel

- **Autores:** François-Louis Michaud; Christian Upper
- **Año:** 2008
- **Publicación o institución:** BIS Quarterly Review, marzo de 2008, 47-58
- **Tipo de documento:** Artículo de publicación de organismo internacional
- **Temática:** TM-17 Mercado monetario: rentabilidades equivalentes y expectativas implícitas (principal) · secundarias: TM-18
- **Calidad Q:** 80 (A) — Tipo 17/25 · Rigor 14/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 6/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de Schrimpf y Sushko 2019, BIS): https://bis.org/publ/qtrpdf/r_qt1903e.htm
- **Acceso y licencia:** Acceso abierto (BPI)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Schrimpf Sushko 2019 "Beyond LIBOR: a primer on the new reference rates" BIS Quarterly Review»; WebFetch: sí, sobre la página índice)
- **Contenido:** Descompone los diferenciales interbancarios a plazo (LIBOR-OIS) en componentes de crédito y de liquidez durante la crisis de 2007-2008.
- **Uso en el Motor:** MC-09: lectura del diferencial entre tipos no garantizados y OIS como prima de crédito/liquidez a corto.
- **Limitaciones:** Confirmada solo por bibliografía; contexto 2007-2008.

#### DOC-MOT-0574 · Q 70 (B) — The Money Market

- **Autores:** Marcia Stigum
- **Año:** 1990
- **Publicación o institución:** McGraw-Hill (libro; ediciones posteriores con Anthony Crescenzi)
- **Tipo de documento:** Libro de referencia
- **Temática:** TM-17 Mercado monetario: rentabilidades equivalentes y expectativas implícitas (principal) · secundarias: —
- **Calidad Q:** 70 (B) — Tipo 15/25 · Rigor 14/20 · Autoridad 13/15 · Vigencia 7/10 · Impacto 8/10 · Independencia 8/10 · Acceso 5/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de Gürkaynak, Sack y Swanson 2007): https://sites.socsci.uci.edu/~swanson2/papers/mbmmpe.pdf
- **Acceso y licencia:** Libro comercial
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Gürkaynak Sack Swanson "Market-Based Measures of Monetary Policy Expectations" federal funds futures Eurodollar»; WebFetch: sí, sobre la página índice)
- **Contenido:** Manual clásico de instrumentos y convenciones del mercado monetario (letras, papel comercial, repos, depósitos, certificados) y de su cálculo de rentabilidades.
- **Uso en el Motor:** MC-01: consulta de convenciones de cotización y cálculo por instrumento.
- **Limitaciones:** Edición de 1990 citada en el índice; ISBN no visto.

## TM-18 Crédito, inflación implícita y volatilidad como factores

#### DOC-MOT-0595 · Q 97 (A) — The TIPS Yield Curve and Inflation Compensation

- **Autores:** Refet S. Gürkaynak; Brian Sack; Jonathan H. Wright
- **Año:** 2010
- **Publicación o institución:** American Economic Journal: Macroeconomics, 2(1), 70-92 (versión previa: FEDS 2008-05)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-18 Crédito, inflación implícita y volatilidad como factores (principal) · secundarias: TM-05
- **Calidad Q:** 97 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** DOI: 10.1257/mac.2.1.70 · https://www.aeaweb.org/articles/pdf/doi/10.1257/mac.2.1.70 · FEDS: https://www.federalreserve.gov/pubs/feds/2008/200805/200805abs.html
- **Acceso y licencia:** Revista con acceso AEA; versión FEDS en abierto
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Gürkaynak Sack Wright "The TIPS Yield Curve and Inflation Compensation" American Economic Journal Macroeconomics»; WebFetch: sí)
- **Contenido:** Estima curvas cupón cero diarias de TIPS y la compensación por inflación (breakeven) a plazo y forward, y discute las primas de riesgo de inflación y de liquidez que la contaminan.
- **Uso en el Motor:** MC-09: cálculo de breakevens al contado y forward (p. ej., 5a5a) a partir de curvas real y nominal (AC-TCV).
- **Limitaciones:** EE. UU.; breakeven ≠ expectativa pura.

#### DOC-MOT-0583 · Q 96 (A) — Modeling Term Structures of Defaultable Bonds

- **Autores:** Darrell Duffie; Kenneth J. Singleton
- **Año:** 1999
- **Publicación o institución:** The Review of Financial Studies, 12(4), 687-720
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-18 Crédito, inflación implícita y volatilidad como factores (principal) · secundarias: TM-05
- **Calidad Q:** 96 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** https://ideas.repec.org/a/oup/rfinst/v12y1999i4p687-720.html
- **Acceso y licencia:** Artículo de revista de pago; ficha pública
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Jarrow–Turnbull model reduced-form credit risk Duffie Singleton 1999 "Modeling Term Structures of Defaultable Bonds"»; WebFetch: sí)
- **Contenido:** Modelos de forma reducida en los que el bono con riesgo se descuenta a un tipo ajustado por impago (r + λ·L), con aplicaciones a curvas corporativas y soberanas y a opciones sobre diferenciales.
- **Uso en el Motor:** MC-09: descomposición del diferencial en intensidad de impago y pérdida en caso de impago; base de curvas de crédito (AC-TCV).
- **Limitaciones:** DOI no mostrado en la página leída; recuperación de valor de mercado como supuesto clave.

#### DOC-MOT-0584 · Q 95 (A) — Pricing Derivatives on Financial Securities Subject to Credit Risk

- **Autores:** Robert A. Jarrow; Stuart M. Turnbull
- **Año:** 1995
- **Publicación o institución:** The Journal of Finance, 50, 53-85
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-18 Crédito, inflación implícita y volatilidad como factores (principal) · secundarias: TM-06
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de Longstaff, Mithal y Neis, NBER WP 10418): https://www.nber.org/papers/w10418.pdf
- **Acceso y licencia:** Artículo de revista de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Longstaff Mithal Neis "Corporate Yield Spreads: Default Risk or Liquidity? New Evidence from the Credit Default Swap Market" pdf»; WebFetch: sí, sobre la página índice)
- **Contenido:** Modelo fundacional de intensidad: el impago llega como un proceso de Poisson exógeno y la recuperación es una fracción fija, lo que permite valorar derivados con riesgo de crédito sin modelar el balance.
- **Uso en el Motor:** MC-09: marco de intensidad para extraer probabilidades de impago neutrales al riesgo de bonos y CDS.
- **Limitaciones:** Confirmada solo por bibliografía.

#### DOC-MOT-0529 · Q 94 (A) — Option Prices, Implied Price Processes, and Stochastic Volatility

- **Autores:** Mark Britten-Jones; Anthony Neuberger
- **Año:** 2000
- **Publicación o institución:** The Journal of Finance, 55(2), 839-866
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-18 Crédito, inflación implícita y volatilidad como factores (principal) · secundarias: TM-06
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de Carr y Lee, «Robust Replication of Volatility Derivatives», 2009): https://www.ma.imperial.ac.uk/~ajacquie/IC_AMDP/IC_AMDP_Docs/Literature/Projects/CarrLee.pdf
- **Acceso y licencia:** Artículo de revista de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Carr Lee 2009 "Volatility Derivatives" Annual Review of Financial Economics variance swaps realized variance»; WebFetch: sí, sobre la página índice)
- **Contenido:** Deriva la varianza integrada esperada neutral al riesgo a partir de un continuo de precios de opciones, base de la volatilidad implícita «independiente de modelo».
- **Uso en el Motor:** MC-09: cálculo de la varianza implícita sin modelo (fundamento del VIX y de los swaps de varianza).
- **Limitaciones:** Confirmada solo por bibliografía.

#### DOC-MOT-0585 · Q 94 (A) — Valuing Credit Default Swaps I: No Counterparty Default Risk

- **Autores:** John Hull; Alan White
- **Año:** 2000
- **Publicación o institución:** The Journal of Derivatives, 8(1), 29-40
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-18 Crédito, inflación implícita y volatilidad como factores (principal) · secundarias: TM-06
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de Longstaff, Mithal y Neis, NBER WP 10418): https://www.nber.org/papers/w10418.pdf · versión de trabajo en NYU (FIN-00-022): https://archive.nyu.edu/handle/2451/26688
- **Acceso y licencia:** Revista de pago; versión de trabajo en repositorio de NYU
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «John Hull Alan White "Valuing Credit Default Swaps I: No Counterparty Default Risk" Journal of Derivatives 2000»; WebFetch: sí, sobre la página índice)
- **Contenido:** Procedimiento para valorar CDS: extracción de la densidad de probabilidad de impago a partir de precios de bonos y cálculo de la prima que iguala los valores presentes de las patas de pago y de protección.
- **Uso en el Motor:** MC-09: cálculo de la prima de CDS teórica y de probabilidades de impago implícitas por plazo (AC-TCV).
- **Limitaciones:** Sin riesgo de contraparte (tratado en la parte II); confirmada solo por bibliografía.

#### DOC-MOT-0587 · Q 93 (A) — The Determinants of Credit Spread Changes

- **Autores:** Pierre Collin-Dufresne; Robert S. Goldstein; J. Spencer Martin
- **Año:** 2001
- **Publicación o institución:** The Journal of Finance, 56, 2177-2207
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-18 Crédito, inflación implícita y volatilidad como factores (principal) · secundarias: TM-04
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de Longstaff, Mithal y Neis, NBER WP 10418): https://www.nber.org/papers/w10418.pdf
- **Acceso y licencia:** Artículo de revista de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Longstaff Mithal Neis "Corporate Yield Spreads: Default Risk or Liquidity? New Evidence from the Credit Default Swap Market" pdf»; WebFetch: sí, sobre la página índice)
- **Contenido:** Las variables de los modelos estructurales explican poco de las variaciones de los diferenciales; un factor común no identificado domina los residuos.
- **Uso en el Motor:** MC-03: regresiones de variaciones de diferenciales y su factor común (AC-TCV).
- **Limitaciones:** Confirmada solo por bibliografía.

#### DOC-MOT-0588 · Q 93 (A) — Explaining the Rate Spread on Corporate Bonds

- **Autores:** Edwin J. Elton; Martin J. Gruber; Deepak Agrawal; Christopher Mann
- **Año:** 2001
- **Publicación o institución:** The Journal of Finance, 56, 247-277
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-18 Crédito, inflación implícita y volatilidad como factores (principal) · secundarias: TM-05
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de Longstaff, Mithal y Neis, NBER WP 10418): https://www.nber.org/papers/w10418.pdf
- **Acceso y licencia:** Artículo de revista de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Longstaff Mithal Neis "Corporate Yield Spreads: Default Risk or Liquidity? New Evidence from the Credit Default Swap Market" pdf»; WebFetch: sí, sobre la página índice)
- **Contenido:** Descompone el diferencial corporativo en pérdida esperada por impago, efecto fiscal y prima de riesgo sistemático; la pérdida esperada explica una parte pequeña.
- **Uso en el Motor:** MC-09: descomposición del diferencial en pérdida esperada y primas (AC-TCV).
- **Limitaciones:** Confirmada solo por bibliografía.

#### DOC-MOT-0526 · Q 92 (A) — Explaining the Negative Returns to Volatility Claims: An Equilibrium Approach

- **Autores:** Bjørn Eraker; Yue Wu
- **Año:** 2017
- **Publicación o institución:** Journal of Financial Economics, 125(1), 72-98
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-18 Crédito, inflación implícita y volatilidad como factores (principal) · secundarias: TM-06
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1016/j.jfineco.2017.04.007 · https://ideas.repec.org/a/eee/jfinec/v125y2017i1p72-98.html
- **Acceso y licencia:** Artículo de revista de pago; ficha pública
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Eraker Wu 2017 "Explaining the negative returns to volatility claims: An equilibrium approach" VIX futures term structure»; WebFetch: sí)
- **Contenido:** Documenta primas fuertemente negativas en futuros de VIX, ETN de VIX y swaps de varianza (≈ -30 % anual en la cartera de futuros a 1 mes de vencimiento constante, 2006-2013) y las explica con un modelo de equilibrio con la estructura de plazos de los futuros.
- **Uso en el Motor:** MC-09: rentabilidad esperada del roll en la curva de futuros de VIX (contango) y de posiciones largas de volatilidad (AC-TCV, AC-DER).
- **Limitaciones:** Muestra 2006-2013.

#### DOC-MOT-0589 · Q 92 (A) — Credit Spreads and Business Cycle Fluctuations

- **Autores:** Simon Gilchrist; Egon Zakrajšek
- **Año:** 2012
- **Publicación o institución:** American Economic Review, 102(4), 1692-1720 (versión previa: NBER WP 17021)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-18 Crédito, inflación implícita y volatilidad como factores (principal) · secundarias: TM-12
- **Calidad Q:** 92 (A) — Tipo 20/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://www.nber.org/papers/w17021
- **Acceso y licencia:** Acceso abierto (NBER, versión de trabajo)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Gilchrist Zakrajšek 2012 "Credit Spreads and Business Cycle Fluctuations" American Economic Review excess bond premium»; WebFetch: sí)
- **Contenido:** Construye un índice de diferenciales a partir de bonos individuales y lo separa en componente de impago esperado y «prima de exceso de bonos» (EBP); la EBP concentra el poder predictivo sobre la actividad.
- **Uso en el Motor:** MC-02, MC-09: prima de exceso de bonos como factor de crédito y de ciclo (AC-TCV).
- **Limitaciones:** EE. UU.; la EBP se publica en la web de la Reserva Federal con revisiones.

#### DOC-MOT-0597 · Q 92 (A) — Inflation Expectations, Real Rates, and Risk Premia: Evidence from Inflation Swaps

- **Autores:** Joseph Haubrich; George Pennacchi; Peter Ritchken
- **Año:** 2012
- **Publicación o institución:** The Review of Financial Studies, p. 1588 y ss. (versión previa: Federal Reserve Bank of Cleveland WP 11-07)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-18 Crédito, inflación implícita y volatilidad como factores (principal) · secundarias: TM-05
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** DOI: 10.1093/rfs/hhs003 · https://academicnewsletter.sufe.edu.cn/info/354527 · WP: https://www.clevelandfed.org/publications/working-paper/2011/wp-1107-inflation-expectations-real-rates-and-risk-premia-evidence-from-inflation-swaps
- **Acceso y licencia:** Revista de pago; documento de trabajo en abierto
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Haubrich Pennacchi Ritchken "Inflation Expectations, Real Rates, and Risk Premia: Evidence from Inflation Swaps" Review of Financial Studies»; WebFetch: sí)
- **Contenido:** Modelo de curvas nominal y real con volatilidad estocástica estimado con Tesoro, encuestas y swaps de inflación; separa inflación esperada, tipos reales y primas de riesgo de inflación (base del modelo de la Fed de Cleveland).
- **Uso en el Motor:** MC-09: descomposición del breakeven/swap de inflación en expectativa y prima (AC-TCV).
- **Limitaciones:** Volumen no mostrado en la página leída.

#### DOC-MOT-0538 · Q 92 (A) — The Model-Free Implied Volatility and Its Information Content

- **Autores:** George J. Jiang; Yisong S. Tian
- **Año:** 2005
- **Publicación o institución:** The Review of Financial Studies, 18, 1305-1342
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-18 Crédito, inflación implícita y volatilidad como factores (principal) · secundarias: TM-06, TM-11
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de Carr y Lee, «Robust Replication of Volatility Derivatives», 2009): https://www.ma.imperial.ac.uk/~ajacquie/IC_AMDP/IC_AMDP_Docs/Literature/Projects/CarrLee.pdf
- **Acceso y licencia:** Artículo de revista de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Carr Lee 2009 "Volatility Derivatives" Annual Review of Financial Economics variance swaps realized variance»; WebFetch: sí, sobre la página índice)
- **Contenido:** Implementa la volatilidad implícita sin modelo y muestra que contiene toda la información de la volatilidad implícita de Black-Scholes y de la volatilidad histórica para predecir la volatilidad realizada.
- **Uso en el Motor:** MC-02, MC-10: comparación predictiva de volatilidad implícita sin modelo frente a realizada (prima de varianza).
- **Limitaciones:** Confirmada solo por bibliografía.

#### DOC-MOT-0591 · Q 91 (A) — Estimating the Price of Default Risk

- **Autores:** Gregory R. Duffee
- **Año:** 1999
- **Publicación o institución:** The Review of Financial Studies, 12, 197-226
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-18 Crédito, inflación implícita y volatilidad como factores (principal) · secundarias: —
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de Longstaff, Mithal y Neis, NBER WP 10418): https://www.nber.org/papers/w10418.pdf
- **Acceso y licencia:** Artículo de revista de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Longstaff Mithal Neis "Corporate Yield Spreads: Default Risk or Liquidity? New Evidence from the Credit Default Swap Market" pdf»; WebFetch: sí, sobre la página índice)
- **Contenido:** Estima con filtro de Kalman un modelo de intensidad de impago para bonos corporativos y su relación con los tipos sin riesgo.
- **Uso en el Motor:** MC-09: estimación econométrica de intensidades de impago a partir de paneles de bonos.
- **Limitaciones:** Confirmada solo por bibliografía.

#### DOC-MOT-0586 · Q 90 (A) — Corporate Yield Spreads: Default Risk or Liquidity? New Evidence from the Credit-Default Swap Market

- **Autores:** Francis A. Longstaff; Sanjay Mithal; Eric Neis
- **Año:** 2004
- **Publicación o institución:** NBER Working Paper 10418 (abril de 2004)
- **Tipo de documento:** Documento de trabajo
- **Temática:** TM-18 Crédito, inflación implícita y volatilidad como factores (principal) · secundarias: TM-05
- **Calidad Q:** 90 (A) — Tipo 17/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://www.nber.org/papers/w10418.pdf · ficha: https://ideas.repec.org/p/nbr/nberwo/10418.html
- **Acceso y licencia:** Acceso abierto (NBER)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Longstaff Mithal Neis "Corporate Yield Spreads: Default Risk or Liquidity? New Evidence from the Credit Default Swap Market" pdf»; WebFetch: sí)
- **Contenido:** Usa las primas de CDS como medida directa del componente de impago del diferencial corporativo: el impago explica la mayor parte del diferencial y el resto (componente no impago) se relaciona con la liquidez.
- **Uso en el Motor:** MC-09: descomposición del diferencial bono-CDS en crédito y liquidez (base CDS-bono) (AC-TCV).
- **Limitaciones:** Se cita la versión de trabajo (la publicada en revista no se confirmó en esta verificación).

#### DOC-MOT-0590 · Q 90 (A) — Credit Swap Valuation

- **Autores:** Darrell Duffie
- **Año:** 1999
- **Publicación o institución:** Financial Analysts Journal, 55, 73-87
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-18 Crédito, inflación implícita y volatilidad como factores (principal) · secundarias: TM-06
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de Longstaff, Mithal y Neis, NBER WP 10418): https://www.nber.org/papers/w10418.pdf
- **Acceso y licencia:** Artículo de revista de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Longstaff Mithal Neis "Corporate Yield Spreads: Default Risk or Liquidity? New Evidence from the Credit Default Swap Market" pdf»; WebFetch: sí, sobre la página índice)
- **Contenido:** Explica la valoración de permutas de impago por arbitraje frente a bonos a tipo flotante y con modelos de intensidad, y las fuentes de base.
- **Uso en el Motor:** MC-09: aproximación de la prima de CDS al diferencial de un flotante a la par.
- **Limitaciones:** Confirmada solo por bibliografía.

#### DOC-MOT-0592 · Q 90 (A) — On Cox Processes and Credit Risky Securities

- **Autores:** David Lando
- **Año:** 1998
- **Publicación o institución:** Review of Derivatives Research, 2, 99-120
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-18 Crédito, inflación implícita y volatilidad como factores (principal) · secundarias: TM-09
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de Longstaff, Mithal y Neis, NBER WP 10418): https://www.nber.org/papers/w10418.pdf
- **Acceso y licencia:** Artículo de revista de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Longstaff Mithal Neis "Corporate Yield Spreads: Default Risk or Liquidity? New Evidence from the Credit Default Swap Market" pdf»; WebFetch: sí, sobre la página índice)
- **Contenido:** Introduce intensidades de impago estocásticas (procesos de Cox) dependientes de variables de estado, generalizando el modelo de intensidad constante.
- **Uso en el Motor:** MC-05: simulación de impagos con intensidad estocástica.
- **Limitaciones:** Confirmada solo por bibliografía.

#### DOC-MOT-0593 · Q 90 (A) — An Econometric Model of the Term Structure of Interest-Rate Swap Yields

- **Autores:** Darrell Duffie; Kenneth J. Singleton
- **Año:** 1997
- **Publicación o institución:** The Journal of Finance, 52, 1287-1321
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-18 Crédito, inflación implícita y volatilidad como factores (principal) · secundarias: TM-05
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de Longstaff, Mithal y Neis, NBER WP 10418): https://www.nber.org/papers/w10418.pdf
- **Acceso y licencia:** Artículo de revista de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Longstaff Mithal Neis "Corporate Yield Spreads: Default Risk or Liquidity? New Evidence from the Credit Default Swap Market" pdf»; WebFetch: sí, sobre la página índice)
- **Contenido:** Modela los diferenciales swap-Tesoro con factores de crédito y liquidez en un marco afín.
- **Uso en el Motor:** MC-09: descomposición de los diferenciales de swaps en crédito y liquidez.
- **Limitaciones:** Confirmada solo por bibliografía.

#### DOC-MOT-0527 · Q 88 (A) — Volatility Derivatives

- **Autores:** Peter Carr; Roger Lee
- **Año:** 2009
- **Publicación o institución:** Annual Review of Financial Economics, 1, 319-339
- **Tipo de documento:** Artículo de revisión (survey)
- **Temática:** TM-18 Crédito, inflación implícita y volatilidad como factores (principal) · secundarias: TM-06
- **Calidad Q:** 88 (A) — Tipo 20/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** https://ideas.repec.org/a/anr/refeco/v1y2009p319-339.html
- **Acceso y licencia:** Revista de pago; versión SSRN (abstract=1599422)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Carr Lee 2009 "Volatility Derivatives" Annual Review of Financial Economics variance swaps realized variance»; WebFetch: sí)
- **Contenido:** Revisión del mercado y la teoría de derivados de volatilidad (swaps de varianza y de volatilidad, futuros y opciones sobre VIX) con demostraciones sencillas de los resultados de replicación.
- **Uso en el Motor:** MC-09: marco de valoración del tipo de swap de varianza y de su relación con el VIX.
- **Limitaciones:** DOI no mostrado explícitamente en la página leída.

#### DOC-MOT-0596 · Q 87 (A) — TIPS Yield Curve and Inflation Compensation (datos)

- **Autores:** Board of Governors of the Federal Reserve System
- **Año:** Serie desde 1999 (página actualizada el 29/07/2022; publicación semanal)
- **Publicación o institución:** Federal Reserve Board — Yield Curve Models and Data
- **Tipo de documento:** Conjunto de datos de investigación de banco central
- **Temática:** TM-18 Crédito, inflación implícita y volatilidad como factores (principal) · secundarias: TM-14
- **Calidad Q:** 87 (A) — Tipo 18/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://www.federalreserve.gov/data/tips-yield-curve-and-inflation-compensation.htm
- **Acceso y licencia:** Acceso abierto (CSV/HTML)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Gürkaynak Sack Wright "The TIPS Yield Curve and Inflation Compensation" American Economic Journal Macroeconomics»; WebFetch: sí)
- **Contenido:** Parámetros diarios de la curva real, rendimientos ajustados de TIPS hipotéticos y compensación por inflación implícita, con la metodología de DOC-MOT-0595.
- **Uso en el Motor:** MC-01, MC-09: serie de breakevens lista para uso en el Motor (AC-TCV).
- **Limitaciones:** Producto de personal investigador, no estadística oficial; implementación revisada en 2022.

#### DOC-MOT-0558 · Q 87 (A) — The Log Contract

- **Autores:** Anthony Neuberger
- **Año:** 1994
- **Publicación o institución:** The Journal of Portfolio Management, 20(2), 74-80
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-18 Crédito, inflación implícita y volatilidad como factores (principal) · secundarias: TM-06
- **Calidad Q:** 87 (A) — Tipo 25/25 · Rigor 14/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de Carr y Lee, «Robust Replication of Volatility Derivatives», 2009): https://www.ma.imperial.ac.uk/~ajacquie/IC_AMDP/IC_AMDP_Docs/Literature/Projects/CarrLee.pdf
- **Acceso y licencia:** Artículo de revista de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Carr Lee 2009 "Volatility Derivatives" Annual Review of Financial Economics variance swaps realized variance»; WebFetch: sí, sobre la página índice)
- **Contenido:** Propone el contrato logarítmico, cuyo valor es proporcional a la varianza esperada, como instrumento para negociar volatilidad.
- **Uso en el Motor:** MC-09: equivalencia entre contrato logarítmico y swap de varianza.
- **Limitaciones:** Confirmada solo por bibliografía.

#### DOC-MOT-0559 · Q 85 (A) — Valuation of Volatility Derivatives as an Inverse Problem

- **Autores:** Peter Friz; Jim Gatheral
- **Año:** 2005
- **Publicación o institución:** Quantitative Finance, 5(6), 531-542
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-18 Crédito, inflación implícita y volatilidad como factores (principal) · secundarias: TM-06, TM-09
- **Calidad Q:** 85 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 13/15 · Vigencia 9/10 · Impacto 6/10 · Independencia 10/10 · Acceso 7/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de Carr y Lee, «Robust Replication of Volatility Derivatives», 2009): https://www.ma.imperial.ac.uk/~ajacquie/IC_AMDP/IC_AMDP_Docs/Literature/Projects/CarrLee.pdf
- **Acceso y licencia:** Artículo de revista de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Carr Lee 2009 "Volatility Derivatives" Annual Review of Financial Economics variance swaps realized variance»; WebFetch: sí, sobre la página índice)
- **Contenido:** Trata la valoración de derivados de volatilidad (p. ej., swaps de volatilidad) como problema inverso a partir de la sonrisa de volatilidad observada.
- **Uso en el Motor:** MC-09: ajuste de convexidad entre swap de volatilidad y de varianza.
- **Limitaciones:** Confirmada solo por bibliografía; título resumido en la fuente índice.

#### DOC-MOT-0525 · Q 84 (A) — Understanding the VIX

- **Autores:** Robert E. Whaley
- **Año:** 2009
- **Publicación o institución:** The Journal of Portfolio Management, 35(3) (DOI indicado por la página: JPM.2009.35.3.098)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TM-18 Crédito, inflación implícita y volatilidad como factores (principal) · secundarias: TM-06, TM-03
- **Calidad Q:** 84 (A) — Tipo 22/25 · Rigor 13/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 9/10 · Acceso 7/10
- **DOI / ISBN / URL:** https://news.vanderbilt.edu/2010/01/14/article-explaining-popular-fear-index-receives-top-honors-from-journal-104130 · resumen del borrador SSRN (2008): https://www.cxoadvisory.com/volatility-effects/history-and-meaning-of-vix/
- **Acceso y licencia:** Revista de pago; borrador en SSRN
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Whaley "The Investor Fear Gauge" 2000 "Understanding the VIX" 2009 Journal of Portfolio Management»; WebFetch: sí, sobre la nota de Vanderbilt y el resumen de CXO)
- **Contenido:** Explica la construcción y la interpretación del VIX como precio del seguro de cartera a 30 días: buen predictor de la volatilidad futura, reversión a la media y respuesta asimétrica a caídas.
- **Uso en el Motor:** MC-02: interpretación del nivel del VIX y de su reversión a la media; complementa el white paper (DOC-MOT-0058).
- **Limitaciones:** Divulgativo; premio de la revista al mejor artículo de 2009.

#### DOC-MOT-0528 · Q 84 (A) — Robust Replication of Volatility Derivatives

- **Autores:** Peter Carr; Roger Lee
- **Año:** 2009
- **Publicación o institución:** Documento de trabajo (versión del 31/05/2009)
- **Tipo de documento:** Documento de trabajo
- **Temática:** TM-18 Crédito, inflación implícita y volatilidad como factores (principal) · secundarias: TM-06
- **Calidad Q:** 84 (A) — Tipo 15/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 6/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://www.ma.imperial.ac.uk/~ajacquie/IC_AMDP/IC_AMDP_Docs/Literature/Projects/CarrLee.pdf
- **Acceso y licencia:** Acceso abierto (copia académica)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Carr Lee 2009 "Volatility Derivatives" Annual Review of Financial Economics variance swaps realized variance»; WebFetch: sí)
- **Contenido:** Estrategias no paramétricas de réplica de derivados sobre varianza realizada con el subyacente y opciones vainilla, y fórmulas independientes de modelo para swaps de volatilidad y opciones sobre varianza.
- **Uso en el Motor:** MC-09: réplica independiente de modelo de swaps de varianza/volatilidad.
- **Limitaciones:** Copia alojada en una página docente, no oficial.

#### DOC-MOT-0524 · Q 83 (A) — The Inflation Risk Premium in the Post-Lehman Period

- **Autores:** Gonzalo Camba-Méndez; Thomas Werner
- **Año:** 2017
- **Publicación o institución:** ECB Working Paper Series n.º 2033
- **Tipo de documento:** Documento de trabajo de banco central
- **Temática:** TM-18 Crédito, inflación implícita y volatilidad como factores (principal) · secundarias: TM-05
- **Calidad Q:** 83 (A) — Tipo 17/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 5/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** Ficha del autor en el BCE: https://ecb.europa.eu/pub/research/authors/profiles/thomas-werner.en.html
- **Acceso y licencia:** Acceso abierto (BCE)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Ejsing Garcia Werner "The term structure of euro area break-even inflation rates" ECB working paper»; WebFetch: sí, sobre la ficha del autor en el BCE)
- **Contenido:** Estima la prima de riesgo de inflación de la zona del euro tras 2008, cuando los breakevens cayeron por debajo de las expectativas de las encuestas (prima negativa).
- **Uso en el Motor:** MC-09: interpretación de breakevens bajos con primas negativas en el euro.
- **Limitaciones:** Confirmada solo por la ficha del autor (URL del PDF no vista).

#### DOC-MOT-0599 · Q 83 (A) — Inflation Risks and Inflation Risk Premia

- **Autores:** Juan Angel García; Thomas Werner
- **Año:** 2010
- **Publicación o institución:** ECB Working Paper Series n.º 1162
- **Tipo de documento:** Documento de trabajo de banco central
- **Temática:** TM-18 Crédito, inflación implícita y volatilidad como factores (principal) · secundarias: TM-05
- **Calidad Q:** 83 (A) — Tipo 17/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 6/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://ECB.eu/pub/pdf/scpwps/ecbwp1162.pdf · ficha del autor: https://ecb.europa.eu/pub/research/authors/profiles/thomas-werner.en.html
- **Acceso y licencia:** Acceso abierto (BCE)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Ejsing Garcia Werner "The term structure of euro area break-even inflation rates" ECB working paper»; WebFetch: sí, sobre la ficha del autor en el BCE)
- **Contenido:** Estima primas de riesgo de inflación en la zona del euro con un modelo de curva que combina bonos nominales, ligados a la inflación y encuestas, y las relaciona con la percepción de riesgos de inflación.
- **Uso en el Motor:** MC-09: descomposición europea de la compensación por inflación (AC-TCV).
- **Limitaciones:** Documento de trabajo.

#### DOC-MOT-0598 · Q 83 (A) — The Term Structure of Euro Area Break-Even Inflation Rates: The Impact of Seasonality

- **Autores:** Jacob Ejsing; Juan Angel García; Thomas Werner
- **Año:** 2007
- **Publicación o institución:** ECB Working Paper Series n.º 830
- **Tipo de documento:** Documento de trabajo de banco central
- **Temática:** TM-18 Crédito, inflación implícita y volatilidad como factores (principal) · secundarias: TM-02
- **Calidad Q:** 83 (A) — Tipo 17/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 6/10 · Independencia 10/10 · Acceso 10/10
- **DOI / ISBN / URL:** https://ECB.eu/pub/pdf/scpwps/ecbwp830.pdf · ficha del autor: https://ecb.europa.eu/pub/research/authors/profiles/thomas-werner.en.html
- **Acceso y licencia:** Acceso abierto (BCE)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Ejsing Garcia Werner "The term structure of euro area break-even inflation rates" ECB working paper»; WebFetch: sí, sobre la ficha del autor en el BCE)
- **Contenido:** Construye la curva de inflación implícita del euro a partir de bonos ligados a la inflación y corrige la estacionalidad del IPCA que distorsiona los breakevens a corto.
- **Uso en el Motor:** MC-02, MC-09: ajuste estacional de breakevens del euro antes de compararlos entre plazos (AC-TCV).
- **Limitaciones:** Documento de trabajo; datos hasta 2007.

#### DOC-MOT-0594 · Q 82 (A) — Credit Risk

- **Autores:** Darrell Duffie; Kenneth J. Singleton
- **Año:** 2003
- **Publicación o institución:** Princeton University Press
- **Tipo de documento:** Libro de referencia
- **Temática:** TM-18 Crédito, inflación implícita y volatilidad como factores (principal) · secundarias: TM-08
- **Calidad Q:** 82 (A) — Tipo 17/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** https://www.gsb.stanford.edu/index%2ephp/faculty-research/books/credit-risk
- **Acceso y licencia:** Libro comercial
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Jarrow–Turnbull model reduced-form credit risk Duffie Singleton 1999 "Modeling Term Structures of Defaultable Bonds"»; WebFetch: sí)
- **Contenido:** Tratado integrado de modelos estructurales y de forma reducida, contrastados con datos de impago, recuperación, migraciones y diferenciales; cubre CDS, CDO y opciones sobre diferenciales.
- **Uso en el Motor:** MC-09: manual de referencia para la modelización del factor crédito.
- **Limitaciones:** ISBN no visto; la página leída muestra solo el título «Credit Risk» (el subtítulo de la edición no se confirmó).

#### DOC-MOT-0539 · Q 77 (B) — Towards a Theory of Volatility Trading

- **Autores:** Peter Carr; Dilip Madan
- **Año:** 1998
- **Publicación o institución:** En R. Jarrow (ed.), Volatility, Risk Publications, pp. 417-427
- **Tipo de documento:** Capítulo de libro
- **Temática:** TM-18 Crédito, inflación implícita y volatilidad como factores (principal) · secundarias: TM-06
- **Calidad Q:** 77 (B) — Tipo 15/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 5/10
- **DOI / ISBN / URL:** Verificada en página índice (bibliografía de Carr y Lee, «Robust Replication of Volatility Derivatives», 2009): https://www.ma.imperial.ac.uk/~ajacquie/IC_AMDP/IC_AMDP_Docs/Literature/Projects/CarrLee.pdf
- **Acceso y licencia:** Libro comercial
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Carr Lee 2009 "Volatility Derivatives" Annual Review of Financial Economics variance swaps realized variance»; WebFetch: sí, sobre la página índice)
- **Contenido:** Muestra cómo replicar exposición a la varianza con una cartera estática de opciones ponderada por 1/K² y negociación dinámica del subyacente.
- **Uso en el Motor:** MC-09: fundamento de la ponderación por 1/K² en el cálculo de varianza implícita.
- **Limitaciones:** Confirmada solo por bibliografía; capítulo difícil de obtener.

## Lagunas de cobertura

Áreas con menos de 20 referencias verificadas tras la carga del 02/11/2026 (V3.2) (objetivo del propietario: 20–50 por área):

| Código | Temática | Verificadas | Faltan para 20 |
|---|---|---|---|
| — | Ninguna | — | — |

## Registro de bajas

Sin bajas en la emisión V3.0 (no hay duplicados exactos). Las semillas que DOC-M no logre verificar se registran aquí como baja con motivo «semilla no verificable».

| REF-id | Título | Motivo | Fecha | Sustituta |
|---|---|---|---|---|

## Historial de versión

- V2.3 (25-26/10/2026): 13 fichas de la carga de arranque del operador.
- V3.0 (01/11/2026): reorganización por temáticas TM- del Anexo D, Q con desglose y orden por calidad, identificadores del anexo 8.1 volcados a las fichas, 116 referencias semilla pendientes de verificación, Novedades, lagunas y registro de bajas.
| V3.1 | 02/11/2026 | Carga verificada por búsqueda web: 235 referencias nuevas, 119 fichas existentes reverificadas o reparadas, 0 bajas; reordenación por temática y Q; índice con recuento de verificadas. |
| V3.2 | 02/11/2026 | Áreas nuevas para los tipos de activo de la V5.0 (índices, fondos y vehículos, derivados, monetario, tipos/crédito/volatilidad): 100 referencias nuevas verificadas por búsqueda web, 0 fichas existentes reverificadas o reparadas, 0 bajas; reordenación por temática y Q; índice con recuento de verificadas. |

