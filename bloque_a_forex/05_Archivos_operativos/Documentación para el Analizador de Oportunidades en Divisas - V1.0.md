# Archivo operativo F7 — Documentación para el Analizador de Oportunidades en Divisas

**Bloque A Forex · Robot Investor · Versión óptima V1.0 · 02/11/2026** · Subordinado al Documento 0 del Bloque A Forex V1.0.

**Versión del archivo:** V1.0 (02/11/2026), alineada con el Documento 0 del Bloque A Forex V1.0 · **Código:** F7 · **Propietario:** AG-14 Documentador para el Analizador (DOC-A)

## Cómo usar este archivo

**Propósito.** Archivo específico del mercado de divisas (taxonomía TX del Anexo D del Documento 0 Forex); incluye referencias reutilizadas del Bloque A general (conservan su ID) y referencias nuevas (prefijo FXA-).  Fondo de referencias académicas y técnicas que sustenta el conocimiento de dominio del análisis de oportunidades en el mercado de divisas (Documento 0, 5.1 y 13). No contiene datos de mercado ni opinión (van en F9) ni métodos cuantitativos de cálculo (van en F8).

**Propietario y acceso.** Escribe solo AG-14 (DOC-A). Leen: agentes del plano P2 (Analizador, Analistas de segmento y transversales, Prospectiva, Contrarias, Curador), AG-16, Orquestador y Auditor. Cualquier otro acceso es una incidencia (Documento 0, 5.2).

**Reglas de uso.**

1. **Lectura.** Lea primero «Novedades»; después el índice de temáticas; dentro de la temática, las fichas aparecen **ordenadas por Q descendente** (a igualdad, la más reciente primero). Cite siempre el ID de la ficha. Para corroboración (PS1) solo cuentan fichas de nivel A o B con `Estado del enlace` distinto de `ROTO`; una ficha `PENDIENTE_VERIFICACION_ALTA` no sustenta evidencia hasta que su propietario la confirme.
2. **Calidad.** Q (0–100) con la rúbrica 13.3: Tipo y revisión 25 · Rigor y transparencia 20 · Autoridad 15 · Vigencia 10 · Impacto 10 · Independencia 10 · Accesibilidad y estabilidad 10. El desglose figura en cada ficha. Niveles: A (Q ≥ 80), B (65–79), C (50–64), D (< 50: candidata a baja salvo que sea la única fuente de un dato necesario, declarado). En las semillas la Q es provisional hasta la verificación de alta.
3. **Estados del enlace** (HT-02, barrido semanal del domingo): `OK`, `REDIRIGIDO`, `ROTO` (4xx/5xx en dos intentos separados 24 h), `MURO_PAGO`, `CONTENIDO_CAMBIADO` (similitud < 0,8 frente a la copia archivada) y `PENDIENTE_BARRIDO` (estado inicial de esta versión: ningún enlace se ha comprobado aún con HT-02). `Última verificación` recoge la última comprobación documentada, no una del barrido.
4. **Acciones** (potestad plena del propietario, R19): `REPARAR` (DOI, nueva URL oficial o copia archivada; obligatoria cuando la ficha lleva «Alerta»); `DEGRADAR` (bajar Q o nivel, con motivo); `BORRAR` cuando haya enlace roto sin alternativa tras dos barridos, contenido retirado o retractado, falsedad o manipulación demostrada, redundancia total con una ficha de mayor Q, o Q < 50 sin uso en 180 días. Cada borrado añade una línea al «Registro de bajas»; si la ficha sustentaba EVD de F2 se avisa al Curador (CT-11, tipo `fuente_retirada`).
5. **Ciclo.** DOC-A alimenta el archivo por su agenda de vigilancia y por las peticiones de conocimiento (CT-08); antes de buscar aplica el Fondo metodológico (R20). Mensualmente el propietario informa al Orquestador de altas, reparaciones, bajas, salud de enlaces y lagunas (CT-21). Los IDs son inmutables y no se reutilizan; en el «Registro de bajas», «REF-id» es el ID propio de la ficha.

## Índice de temáticas (Anexo D, TX-)

| Código | Temática | Referencias | Verificadas | Pendientes de verificación | A | B | C | D | Q medio |
|---|---|---|---|---|---|---|---|---|---|
| TX-01 | Teoría del tipo de cambio y finanzas internacionales | 23 | 23 | 0 | 22 | 1 | 0 | 0 | 85,1 |
| TX-02 | Política monetaria, bancos centrales y tipo de cambio | 24 | 24 | 0 | 20 | 4 | 0 | 0 | 83,9 |
| TX-03 | Tipo de cambio de equilibrio y valoración (PPA, BEER, FEER, REER) | 29 | 29 | 0 | 24 | 5 | 0 | 0 | 83,3 |
| TX-04 | Carry, prima de riesgo cambiaria y paridad descubierta | 30 | 30 | 0 | 29 | 1 | 0 | 0 | 85,4 |
| TX-05 | Momentum, valor y factores cambiarios | 22 | 22 | 0 | 20 | 2 | 0 | 0 | 87,2 |
| TX-06 | Microestructura, flujo de órdenes y posicionamiento | 22 | 22 | 0 | 15 | 7 | 0 | 0 | 82,5 |
| TX-07 | Balanza de pagos, flujos de capital y ciclo financiero global | 24 | 24 | 0 | 20 | 4 | 0 | 0 | 84,2 |
| TX-08 | Regímenes cambiarios, intervención y controles de capitales | 22 | 22 | 0 | 17 | 5 | 0 | 0 | 83,0 |
| TX-09 | Crisis cambiarias, devaluaciones y riesgo de cola | 22 | 22 | 0 | 17 | 5 | 0 | 0 | 83,2 |
| TX-10 | Divisas emergentes | 22 | 22 | 0 | 13 | 9 | 0 | 0 | 80,4 |
| TX-11 | Divisas de materias primas y términos de intercambio | 24 | 24 | 0 | 18 | 5 | 1 | 0 | 82,7 |
| TX-12 | Divisas de refugio y sistema monetario internacional | 39 | 39 | 0 | 23 | 15 | 1 | 0 | 80,1 |
| TX-13 | Previsión de tipos de cambio y su evaluación | 26 | 26 | 0 | 22 | 4 | 0 | 0 | 86,3 |
| TX-14 | Geopolítica, sanciones, política y divisas | 29 | 29 | 0 | 18 | 10 | 1 | 0 | 81,0 |
| **Total** | — | **358** | **358** | 0 | 278 | 77 | 3 | 0 | 83,3 |

«Verificadas»: enlace en estado OK, REDIRIGIDO, MURO_PAGO o VERIFICADO_BUSQUEDA (existencia y datos confirmados por búsqueda web el 02/11/2026), o verificación documental completa en una carga anterior (25–26/10/2026), pendiente solo del barrido automático HT-02. «Pendientes»: semillas aún en PENDIENTE_VERIFICACION_ALTA o fichas con alerta sin resolver.

## Novedades

- 02/11/2026: emisión inicial V1.0 del archivo específico de divisas.

## TX-01 Teoría del tipo de cambio y finanzas internacionales

#### FXA-0083 · Q 93 (A) — Exchange Rate Disconnect in General Equilibrium

- **Autores:** Oleg Itskhoki; Dmitry Mukhin
- **Año:** 2021 (NBER WP 23401, 2017)
- **Publicación o institución:** Journal of Political Economy, vol. 129, n.º 8, págs. 2183-2232
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-01 Teoría del tipo de cambio y finanzas internacionales (principal) · secundarias: TX-04, TX-06
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 6/10
- **DOI / URL:** DOI 10.1086/714447 · DOI WP 10.3386/w23401 · https://nber.org/papers/w23401 · PDF del autor: https://itskhoki.com/papers/disconnect.pdf
- **Acceso y licencia:** Peldaño 2 (WP del NBER y PDF del autor; artículo de pago) · Licencia: Copyright University of Chicago Press
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Itskhoki Mukhin "Exchange Rate Disconnect in General Equilibrium" Journal of Political Economy 2021»; WebFetch: sí, página del NBER y página de la medalla John Bates Clark 2022 de la AEA)
- **Contenido:** Modelo de equilibrio general con mercados financieros segmentados, límites al arbitraje y operadores de ruido: un shock pequeño pero persistente a la demanda internacional de activos es el único que genera la desconexión del tipo de cambio y explica a la vez los enigmas de Meese-Rogoff, PPA, términos de intercambio, Backus-Smith y UIP; el ruido financiero, no los fundamentales, sería el principal motor del tipo de cambio.
- **Uso en el bloque:** AG-02 ANZ, TR-PFV y Analistas de segmento: fundamento teórico de por qué flujos y posicionamiento (y no solo fundamentales) mueven las divisas; marco unificador de las lentes del cribado.
- **Limitaciones:** Modelo teórico calibrado; el shock financiero es exógeno.

#### FXA-0022 · Q 92 (A) — Expectations and Exchange Rate Dynamics

- **Autores:** Rudiger Dornbusch
- **Año:** 1976
- **Publicación o institución:** The Journal of Political Economy, vol. 84, n.º 6, págs. 1161-1176 (University of Chicago Press)
- **Tipo de documento:** Artículo revisado por pares (canónico)
- **Temática:** TX-01 Teoría del tipo de cambio y finanzas internacionales (principal) · secundarias: TX-02
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 10/10 · Independencia 10/10 · Acceso 8/10
- **DOI / URL:** https://users.ssc.wisc.edu/~cengel/IMF/DornbuschJPE1976.pdf
- **Acceso y licencia:** Peldaño 1 (copia en PDF alojada por C. Engel, Universidad de Wisconsin) · Licencia: Copyright University of Chicago Press
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Dornbusch 1976 "Expectations and Exchange Rate Dynamics" overshooting model Eichenbaum Evans delayed overshooting»; WebFetch: sí, primera página del PDF)
- **Contenido:** Modelo de «sobrerreacción» (overshooting): con precios de bienes rígidos y mercados de activos que se ajustan al instante bajo paridad descubierta, una expansión monetaria deprecia el tipo de cambio por encima de su nivel de largo plazo y luego se aprecia gradualmente.
- **Uso en el bloque:** TR-BCM y Analistas G10: mecanismo de referencia de la reacción del tipo de cambio a sorpresas monetarias y a cambios del diferencial de tipos reales.
- **Limitaciones:** La evidencia empírica de sobrerreacción es mixta (sobrerreacción retardada, Eichenbaum y Evans 1995).

#### ANA-DOC-0302 · Q 91 (A) — Exchange Rate Predictability

- **Autores:** Barbara Rossi
- **Año:** 2013
- **Publicación o institución:** Journal of Economic Literature, vol. 51, n.º 4, págs. 1063-1119 (versión de trabajo: Universitat Pompeu Fabra, Economics Working Paper 1369)
- **Tipo de documento:** Artículo de revisión (survey) revisado por pares
- **Temática:** TX-01 Teoría del tipo de cambio y finanzas internacionales (principal) · secundarias: TX-13
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / URL:** https://econ-papers.upf.edu/en/onepaper.php?id=1369
- **Acceso y licencia:** Peldaño 2 (versión de trabajo abierta en UPF; artículo JEL para miembros AEA) · Licencia: Copyright de la autora/AEA
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Rossi 2013 "Exchange Rate Predictability" Journal of Economic Literature»; WebFetch: sí) · reutilizada del F7 V3.2 (TA-07)
- **Contenido:** Revisión exhaustiva de la predictibilidad de tipos de cambio por modelos teóricos (PPA, monetarios, reglas de Taylor, activos exteriores netos, UIP): el paseo aleatorio sin deriva sigue siendo el rival más difícil; los mejores resultados aparecen con reglas de Taylor y activos exteriores netos, modelos lineales parsimoniosos y horizontes cortos.
- **Uso en el bloque:** AG-02 ANZ y Analistas de segmento: qué fundamentales teóricos tienen algún poder predictivo y en qué horizonte; AG-10 PROS y AG-20 EVAL: listón del paseo aleatorio.
- **Limitaciones:** Literatura revisada hasta 2012.

#### ANA-DOC-0751 · Q 88 (A) — A Quantity-Driven Theory of Term Premia and Exchange Rates

- **Autores:** Robin Greenwood; Samuel G. Hanson; Jeremy C. Stein; Adi Sunderam
- **Año:** 2023
- **Publicación o institución:** The Quarterly Journal of Economics, vol. 138, n.º 4, págs. 2327-2389
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-01 Teoría del tipo de cambio y finanzas internacionales (principal) · secundarias: TX-02, TX-04
- **Calidad Q:** 88 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 7/10 · Independencia 10/10 · Acceso 4/10
- **DOI / URL:** https://stein.scholars.harvard.edu/publications
- **Acceso y licencia:** Peldaño 3 (artículo de pago; listado bibliográfico abierto en la web del autor) · Licencia: copyright Oxford University Press / autores
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «López-Salido Stein Zakrajšek "Credit-Market Sentiment and the Business Cycle" Quarterly Journal of Economics», que devolvió la web de publicaciones del autor; WebFetch: sí, página índice https://stein.scholars.harvard.edu/publications) · reutilizada del F7 V3.2 (TA-23)
- **Contenido:** Teoría en la que la oferta neta de duración (emisión pública, compras de bancos centrales) que deben absorber arbitrajistas con capital limitado mueve las primas por plazo y, a través de ellas, los tipos de cambio; enlaza QE/QT con movimientos cambiarios y con desviaciones de la paridad descubierta.
- **Uso en el bloque:** TR-BCM: canal de cantidades (QE/QT, emisión del Tesoro) hacia el tipo de cambio; AS-G10N: tesis sobre USD, EUR y JPY ligadas a balances de bancos centrales.
- **Limitaciones:** Confirmado solo por página índice; contenido según conocimiento general de la obra, a cotejar.

#### ANA-DOC-0368 · Q 88 (A) — International Financial Adjustment

- **Autores:** Pierre-Olivier Gourinchas; Hélène Rey
- **Año:** 2007
- **Publicación o institución:** Journal of Political Economy, vol. 115, n.º 4, págs. 665-703
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-01 Teoría del tipo de cambio y finanzas internacionales (principal) · secundarias: TX-07, TX-13
- **Calidad Q:** 88 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 9/10 · Independencia 10/10 · Acceso 3/10
- **DOI / URL:** https://ideas.repec.org/a/ucp/jpolec/v115y2007i4p665-703.html
- **Acceso y licencia:** Peldaño 3 (University of Chicago Press) · Licencia: Copyright UCP
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Hélène Rey IDEAS RePEc author page publications»; WebFetch: sí, sobre la página de autora de IDEAS que lista la obra) · reutilizada del F7 V3.2 (TA-07)
- **Contenido:** Muestra que el ajuste exterior de EE. UU. opera en buena parte por efectos de valoración de activos y pasivos exteriores, y que los desequilibrios externos (medida nxa) predicen rendimientos exteriores netos y la depreciación del dólar.
- **Uso en el bloque:** AS-G10N y AS-ESTR: desequilibrio exterior como predictor del dólar a medio plazo (H3–H4); TR-BCM: lectura de la balanza de pagos.
- **Limitaciones:** Resumen no leído en esta carga.

#### ANA-DOC-0301 · Q 88 (A) — Empirical exchange rate models of the seventies: Do they fit out of sample?

- **Autores:** Richard A. Meese; Kenneth Rogoff
- **Año:** 1983
- **Publicación o institución:** Journal of International Economics, vol. 14, págs. 3-24
- **Tipo de documento:** Artículo revisado por pares (canónico)
- **Temática:** TX-01 Teoría del tipo de cambio y finanzas internacionales (principal) · secundarias: TX-13
- **Calidad Q:** 88 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** DOI 10.1016/0022-1996(83)90017-X · https://rogoff.scholars.harvard.edu/publications/empirical-exchange-rate-models-seventies-do-they-fit-out-sample
- **Acceso y licencia:** Peldaño 3 (artículo Elsevier de pago; ficha en la web del autor) · Licencia: Copyright Elsevier
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Meese Rogoff 1983 "Empirical exchange rate models of the seventies: Do they fit out of sample?"»; WebFetch: sí) · reutilizada del F7 V3.2 (TA-07)
- **Contenido:** Resultado fundacional: los modelos estructurales de tipo de cambio de los setenta (monetarios de precios flexibles y rígidos, Hooper-Morton) no baten fuera de muestra al paseo aleatorio, ni siquiera usando valores realizados de los fundamentales.
- **Uso en el bloque:** AG-10 PROS y AG-20 EVAL: referencia ingenua obligada (paseo aleatorio) para certificar horizontes (Documento 0, 8.3); Analistas de segmento (AS-G10N, AS-G10M…): humildad predictiva en tesis basadas en fundamentales.
- **Limitaciones:** Muestra antigua; matizado por la literatura posterior (véanse ANA-DOC-0302 y FXA-0482).

#### ANA-DOC-0309 · Q 87 (A) — The Six Major Puzzles in International Macroeconomics: Is There a Common Cause?

- **Autores:** Maurice Obstfeld; Kenneth Rogoff
- **Año:** 2001 (NBER Macroeconomics Annual 2000, vol. 15; NBER WP 7777 de 2000)
- **Publicación o institución:** NBER Macroeconomics Annual 2000, vol. 15 (MIT Press), ed. Ben S. Bernanke y Kenneth Rogoff
- **Tipo de documento:** Capítulo revisado en anuario académico
- **Temática:** TX-01 Teoría del tipo de cambio y finanzas internacionales (principal) · secundarias: TX-03
- **Calidad Q:** 87 (A) — Tipo 22/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / URL:** https://www.nber.org/chapters/c11059
- **Acceso y licencia:** Peldaño 1 (PDF del capítulo en NBER) · Licencia: Copyright NBER
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Obstfeld Rogoff "The Six Major Puzzles in International Macroeconomics: Is There a Common Cause?" NBER Macroeconomics Annual 2000»; WebFetch: sí) · reutilizada del F7 V3.2 (TA-07)
- **Contenido:** Sintetiza seis enigmas (sesgo doméstico en comercio y cartera, Feldstein-Horioka, correlación de consumo, PPA y desconexión del tipo de cambio) y propone los costes de comercio como causa común.
- **Uso en el bloque:** AG-02 ANZ y Analistas de segmento: marco conceptual del «exchange rate disconnect» para no sobreinterpretar fundamentales en tesis cambiarias.
- **Limitaciones:** Marco de 2000; parte de los enigmas se han reinterpretado (véase FXA-0083, Itskhoki y Mukhin).

#### FXA-0024 · Q 87 (A) — Exchange Rate Dynamics Redux

- **Autores:** Maurice Obstfeld; Kenneth Rogoff
- **Año:** 1995
- **Publicación o institución:** Journal of Political Economy, vol. 103, págs. 624-660
- **Tipo de documento:** Artículo revisado por pares (canónico)
- **Temática:** TX-01 Teoría del tipo de cambio y finanzas internacionales (principal) · secundarias: TX-02
- **Calidad Q:** 87 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 10/10 · Independencia 10/10 · Acceso 3/10
- **DOI / URL:** https://ucema.edu.ar/~car/dornbusch25.pdf (página índice: bibliografía de Rogoff 2002)
- **Acceso y licencia:** Peldaño 3 (University of Chicago Press, de pago) · Licencia: Copyright UCP
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Dornbusch 1976 "Expectations and Exchange Rate Dynamics" overshooting…»; WebFetch: sí, bibliografía de https://ucema.edu.ar/~car/dornbusch25.pdf con autores, revista, volumen y páginas)
- **Contenido:** Modelo fundacional de la «nueva macroeconomía abierta»: dos países, competencia monopolística, precios rígidos y microfundamentos; analiza los efectos de los shocks monetarios y fiscales sobre el tipo de cambio, la cuenta corriente y el bienestar.
- **Uso en el bloque:** TR-BCM y AG-02 ANZ: base teórica de los modelos de bancos centrales que usan los informes de política monetaria (transmisión vía tipo de cambio).
- **Limitaciones:** Confirmado solo por bibliografía; supuestos de fijación de precios en moneda del productor revisados por la literatura posterior.

#### FXA-0025 · Q 86 (A) — Foundations of International Macroeconomics

- **Autores:** Maurice Obstfeld; Kenneth Rogoff
- **Año:** 1996
- **Publicación o institución:** MIT Press, Cambridge (MA)
- **Tipo de documento:** Manual de referencia
- **Temática:** TX-01 Teoría del tipo de cambio y finanzas internacionales (principal) · secundarias: TX-03, TX-08
- **Calidad Q:** 86 (A) — Tipo 20/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / URL:** https://ucema.edu.ar/~car/dornbusch25.pdf (página índice: bibliografía de Rogoff 2002)
- **Acceso y licencia:** Peldaño 3 (libro de pago) · Licencia: Copyright MIT Press
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Dornbusch 1976 "Expectations and Exchange Rate Dynamics" overshooting…»; WebFetch: sí, bibliografía de Rogoff 2002)
- **Contenido:** Manual de referencia de macroeconomía internacional: enfoque intertemporal de la cuenta corriente, PPA y tipo de cambio real, modelos monetarios, precios rígidos, regímenes cambiarios y crisis.
- **Uso en el bloque:** Todos los Analistas de segmento y AG-14 DOC-A: base conceptual común y vocabulario estándar de las tesis cambiarias.
- **Limitaciones:** No cubre la literatura de finanzas cambiarias posterior a 2000 (factores, CIP, moneda dominante).

#### FXA-0057 · Q 85 (A) — The Economics of Exchange Rates

- **Autores:** Lucio Sarno; Mark P. Taylor
- **Año:** 2003
- **Publicación o institución:** Cambridge University Press
- **Tipo de documento:** Manual de referencia
- **Temática:** TX-01 Teoría del tipo de cambio y finanzas internacionales (principal) · secundarias: TX-03, TX-04, TX-06
- **Calidad Q:** 85 (A) — Tipo 20/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 7/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / URL:** https://ideas.repec.org/a/aea/jecper/v18y2004i4p135-158.html (página índice: referencias citadas por Taylor y Taylor 2004; ISBN 9780521485845)
- **Acceso y licencia:** Peldaño 3 (libro de pago) · Licencia: Copyright Cambridge University Press
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Alan Taylor Mark Taylor 2004 "The Purchasing Power Parity Debate"…»; WebFetch: sí, lista de referencias de IDEAS con ISBN)
- **Contenido:** Manual de economía de los tipos de cambio: eficiencia del mercado de divisas y prima forward, PPA y tipo real, modelos monetarios y de equilibrio, microestructura, intervención y crisis.
- **Uso en el bloque:** Analistas de segmento y transversales: manual de consulta específico de divisas, complementario de Obstfeld y Rogoff (FXA-0025).
- **Limitaciones:** Edición de 2003; no cubre la literatura factorial posterior.

#### FXA-0026 · Q 85 (A) — On the Mark: A Theory of Floating Exchange Rates Based on Real Interest Differentials

- **Autores:** Jeffrey A. Frankel
- **Año:** 1979
- **Publicación o institución:** American Economic Review, vol. 69, págs. 610-622
- **Tipo de documento:** Artículo revisado por pares (canónico)
- **Temática:** TX-01 Teoría del tipo de cambio y finanzas internacionales (principal) · secundarias: TX-02
- **Calidad Q:** 85 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 9/10 · Independencia 10/10 · Acceso 4/10
- **DOI / URL:** https://ucema.edu.ar/~car/dornbusch25.pdf (página índice: bibliografía de Rogoff 2002)
- **Acceso y licencia:** Peldaño 3 (AEA/JSTOR) · Licencia: Copyright AEA
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Dornbusch 1976 "Expectations and Exchange Rate Dynamics" overshooting…»; WebFetch: sí, bibliografía de Rogoff 2002)
- **Contenido:** Modelo monetario de precios rígidos en el que el tipo de cambio depende del diferencial de tipos de interés reales (y no nominales); aplicado al marco alemán frente al dólar.
- **Uso en el bloque:** TR-BCM y AS-G10N: fundamento de la lente «diferencial de tipos reales» del cribado (Documento 0, 8.2).
- **Limitaciones:** Confirmado solo por bibliografía; poder predictivo fuera de muestra limitado (Meese-Rogoff).

#### FXA-0019 · Q 84 (A) — The scapegoat theory of exchange rates: the first tests

- **Autores:** Marcel Fratzscher; Dagfinn Rime; Lucio Sarno; Gabriele Zinna
- **Año:** 2015
- **Publicación o institución:** Journal of Monetary Economics, vol. 70, págs. 1-21
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-01 Teoría del tipo de cambio y finanzas internacionales (principal) · secundarias: TX-06, TX-13
- **Calidad Q:** 84 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 5/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** DOI 10.1016/j.jmoneco.2014.09.001 · https://openaccess.city.ac.uk/id/eprint/13155/
- **Acceso y licencia:** Peldaño 2 (versión de autor en City Research Online) · Licencia: Copyright Elsevier
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Menkhoff Sarno Schmeling Schrimpf "Currency Value" Review of Financial Studies 2017»; WebFetch: sí, página índice de City Research Online)
- **Contenido:** Primer contraste de la teoría del «chivo expiatorio» (Bacchetta y van Wincoop): con encuestas a operadores sobre la importancia de cada fundamental, muestra que el peso que el mercado da a un fundamental cambia en el tiempo y que incorporarlo mejora el ajuste de los modelos de tipo de cambio.
- **Uso en el bloque:** Analistas de segmento y AG-02 ANZ: identificar qué fundamental «manda» en cada régimen (tipos, crecimiento, riesgo) en lugar de usar pesos fijos.
- **Limitaciones:** Encuestas de un proveedor; muestra limitada a divisas principales.

#### FXA-0023 · Q 84 (A) — Dornbusch's Overshooting Model After Twenty-Five Years

- **Autores:** Kenneth Rogoff
- **Año:** 2002 (conferencia de 29/11/2001, revisada el 22/01/2002)
- **Publicación o institución:** Fondo Monetario Internacional — Mundell-Fleming Lecture, Second Annual Research Conference
- **Tipo de documento:** Conferencia institucional / artículo de revisión
- **Temática:** TX-01 Teoría del tipo de cambio y finanzas internacionales (principal) · secundarias: TX-02
- **Calidad Q:** 84 (A) — Tipo 18/25 · Rigor 14/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 9/10 · Independencia 10/10 · Acceso 10/10
- **DOI / URL:** https://ucema.edu.ar/~car/dornbusch25.pdf
- **Acceso y licencia:** Peldaño 1 (PDF abierto) · Licencia: Copyright del autor/FMI
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Dornbusch 1976 "Expectations and Exchange Rate Dynamics" overshooting…»; WebFetch: sí)
- **Contenido:** Revisión del modelo de Dornbusch a los 25 años: explica por qué sigue siendo el marco de referencia de la política monetaria en economía abierta, su relación con la nueva macroeconomía abierta y por qué los modelos de fundamentales fallan empíricamente a corto plazo.
- **Uso en el bloque:** TR-BCM y AG-02 ANZ: marco didáctico de política monetaria y tipo de cambio; conecta el modelo con Meese-Rogoff (ANA-DOC-0301).
- **Limitaciones:** Conferencia de 2001; no recoge la literatura posterior a 2002.

#### FXA-0118 · Q 84 (A) — The New Open Economy Macroeconomics: A Survey

- **Autores:** Philip R. Lane
- **Año:** 2001
- **Publicación o institución:** Journal of International Economics, vol. 54, n.º 2, págs. 235-266
- **Tipo de documento:** Artículo de revisión (survey) revisado por pares
- **Temática:** TX-01 Teoría del tipo de cambio y finanzas internacionales (principal) · secundarias: TX-02
- **Calidad Q:** 84 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 9/10 · Independencia 10/10 · Acceso 3/10
- **DOI / URL:** https://ideas.repec.org/p/cpr/ceprdp/3346.html (página índice: referencias citadas por Galí y Monacelli en IDEAS)
- **Acceso y licencia:** Peldaño 3 (Elsevier; versión de trabajo abierta) · Licencia: Copyright Elsevier
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Galí Monacelli…»; WebFetch: sí, lista de referencias de IDEAS)
- **Contenido:** Revisión de la «nueva macroeconomía abierta» surgida de Obstfeld-Rogoff (1995): precios rígidos, competencia imperfecta, fijación de precios en moneda local, mercados de activos y bienestar.
- **Uso en el bloque:** AG-14 DOC-A y TR-BCM: mapa de la literatura teórica que sustenta los modelos de bancos centrales en economía abierta.
- **Limitaciones:** Confirmado solo por índice; literatura hasta 2000.

#### FXA-0119 · Q 84 (A) — New Directions for Stochastic Open Economy Models

- **Autores:** Maurice Obstfeld; Kenneth Rogoff
- **Año:** 2000
- **Publicación o institución:** Journal of International Economics, vol. 50, n.º 1, págs. 117-153
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-01 Teoría del tipo de cambio y finanzas internacionales (principal) · secundarias: TX-04
- **Calidad Q:** 84 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 8/10 · Independencia 10/10 · Acceso 3/10
- **DOI / URL:** https://ideas.repec.org/p/cpr/ceprdp/3346.html (página índice: referencias citadas por Galí y Monacelli en IDEAS; citada también en la bibliografía de Rogoff 2002, https://ucema.edu.ar/~car/dornbusch25.pdf)
- **Acceso y licencia:** Peldaño 3 (Elsevier) · Licencia: Copyright Elsevier
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Galí Monacelli…»; WebFetch: sí, dos páginas índice con revista, volumen y páginas)
- **Contenido:** Extiende los modelos de economía abierta con precios rígidos a un entorno estocástico: el riesgo afecta a los niveles medios de precios, al tipo de cambio esperado y a la prima de riesgo cambiaria, y permite comparar regímenes en términos de bienestar.
- **Uso en el bloque:** AG-02 ANZ y AS-ESTR: puente teórico entre política monetaria, incertidumbre y prima de riesgo cambiaria.
- **Limitaciones:** Confirmado solo por índices.

#### FXA-0058 · Q 84 (A) — Empirical Research on Nominal Exchange Rates

- **Autores:** Jeffrey A. Frankel; Andrew K. Rose
- **Año:** 1995
- **Publicación o institución:** En G. M. Grossman y K. Rogoff (eds.), Handbook of International Economics, vol. 3, cap. 33, págs. 1689-1729 (Elsevier)
- **Tipo de documento:** Capítulo de manual de referencia
- **Temática:** TX-01 Teoría del tipo de cambio y finanzas internacionales (principal) · secundarias: TX-13
- **Calidad Q:** 84 (A) — Tipo 20/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 6/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / URL:** https://ideas.repec.org/a/aea/jecper/v18y2004i4p135-158.html (página índice: referencias citadas por Taylor y Taylor 2004)
- **Acceso y licencia:** Peldaño 3 (Elsevier; versión NBER de trabajo) · Licencia: Copyright Elsevier
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Alan Taylor Mark Taylor 2004 "The Purchasing Power Parity Debate"…»; WebFetch: sí, lista de referencias de IDEAS)
- **Contenido:** Revisión de la investigación empírica sobre tipos de cambio nominales: modelos monetarios, desconexión con los fundamentales, sesgo del forward, expectativas de encuestas y microestructura.
- **Uso en el bloque:** AG-14 DOC-A y Analistas: estado del arte a mediados de los noventa; puente entre Meese-Rogoff y la literatura posterior.
- **Limitaciones:** Literatura hasta 1994.

#### ANA-DOC-0312 · Q 82 (A) — Obstfeld and Rogoff's international macro puzzles: a quantitative assessment

- **Autores:** Jonathan Eaton; Samuel Kortum; Brent Neiman
- **Año:** 2016
- **Publicación o institución:** Journal of Economic Dynamics and Control, vol. 72, págs. 5-23
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-01 Teoría del tipo de cambio y finanzas internacionales (principal) · secundarias: TX-03
- **Calidad Q:** 82 (A) — Tipo 23/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 6/10 · Independencia 10/10 · Acceso 3/10
- **DOI / URL:** DOI 10.1016/j.jedc.2016.06.002 · https://ideas.repec.org/a/eee/dyncon/v72y2016icp5-23.html
- **Acceso y licencia:** Peldaño 3 (artículo Elsevier de pago; ficha abierta en RePEc) · Licencia: Copyright Elsevier
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Obstfeld Rogoff "The Six Major Puzzles in International Macroeconomics: Is There a Common Cause?" NBER Macroeconomics Annual 2000» —la obra aparece en los resultados—; WebFetch: sí) · reutilizada del F7 V3.2 (TA-07)
- **Contenido:** Contrasta cuantitativamente, con un modelo dinámico multipaís calibrado a 19 economías, la hipótesis de Obstfeld y Rogoff: eliminar las fricciones comerciales en manufacturas atenúa Feldstein-Horioka, la volatilidad del tipo de cambio real (PPA relativa) y la baja correlación internacional del consumo.
- **Uso en el bloque:** AG-02 ANZ y AS-G10N: evidencia de que los costes de comercio (aranceles, fragmentación) afectan a tipos de cambio reales; útil para tesis cambiarias de aranceles y desglobalización.
- **Limitaciones:** Resultados de modelo calibrado; complementa ANA-DOC-0309.

#### FXA-0020 · Q 82 (A) — Asset prices, exchange rates and the current account

- **Autores:** Marcel Fratzscher; Luciana Juvenal; Lucio Sarno
- **Año:** 2010
- **Publicación o institución:** European Economic Review, vol. 54, n.º 5, págs. 643-658
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-01 Teoría del tipo de cambio y finanzas internacionales (principal) · secundarias: TX-07
- **Calidad Q:** 82 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 7/10 · Impacto 5/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** DOI 10.1016/j.euroecorev.2009.12.005 · https://openaccess.city.ac.uk/id/eprint/3304/
- **Acceso y licencia:** Peldaño 2 (versión de autor en City Research Online) · Licencia: Copyright Elsevier
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Menkhoff Sarno Schmeling Schrimpf "Currency Value" Review of Financial Studies 2017»; WebFetch: sí, página índice de City Research Online)
- **Contenido:** Con un VAR identificado por signos para EE. UU., muestra que los shocks de precios de activos (acciones y vivienda) explican una parte mayor de la cuenta corriente y del tipo de cambio real que los shocks al propio tipo de cambio.
- **Uso en el bloque:** AS-G10N y TR-BCM: relación entre ciclo de activos, déficit exterior y dólar; contexto para tesis de dólar a medio plazo.
- **Limitaciones:** Identificación por signos; centrado en EE. UU.

#### FXA-0098 · Q 82 (A) — International Capital Markets and Foreign Exchange Risk

- **Autores:** Michael J. Brennan; Yihong Xia
- **Año:** 2006
- **Publicación o institución:** Review of Financial Studies, vol. 19, n.º 3, págs. 753-795
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-01 Teoría del tipo de cambio y finanzas internacionales (principal) · secundarias: TX-04
- **Calidad Q:** 82 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 7/10 · Impacto 6/10 · Independencia 10/10 · Acceso 3/10
- **DOI / URL:** https://www.nber.org/papers/w13812.pdf (página índice: bibliografía de Lustig y Verdelhan 2010)
- **Acceso y licencia:** Peldaño 3 (OUP) · Licencia: Copyright OUP
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Hanno Lustig Adrien Verdelhan "The Cross Section of Foreign Currency Risk Premia…"»; WebFetch: sí, bibliografía del PDF del NBER)
- **Contenido:** Modelo de mercados de capitales internacionales en el que los factores de descuento de cada país se identifican a partir de las curvas de tipos y los tipos de cambio, que reflejan su cociente; estima primas de riesgo cambiarias coherentes con la valoración de bonos.
- **Uso en el bloque:** AG-02 ANZ y AS-ESTR: relación formal entre curvas de tipos, primas por plazo y tipos de cambio (enlaza con ANA-DOC-0751).
- **Limitaciones:** Confirmado solo por bibliografía; contenido según el título, a cotejar.

#### FXA-0027 · Q 82 (A) — Exchange Rate Pass-through, Exchange Rate Volatility, and Exchange Rate Disconnect

- **Autores:** Michael B. Devereux; Charles Engel
- **Año:** 2002
- **Publicación o institución:** Journal of Monetary Economics, vol. 49, n.º 5, págs. 913-940 (Carnegie-Rochester Conference Series on Public Policy)
- **Tipo de documento:** Artículo revisado por pares (conferencia)
- **Temática:** TX-01 Teoría del tipo de cambio y finanzas internacionales (principal) · secundarias: TX-02
- **Calidad Q:** 82 (A) — Tipo 23/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 8/10 · Independencia 10/10 · Acceso 3/10
- **DOI / URL:** https://ideas.repec.org/p/cpr/ceprdp/3346.html (página índice: referencias de Galí y Monacelli en IDEAS) · https://ucema.edu.ar/~car/dornbusch25.pdf (bibliografía de Rogoff 2002)
- **Acceso y licencia:** Peldaño 3 (Elsevier) · Licencia: Copyright Elsevier
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsquedas web: «Dornbusch 1976 "Expectations and Exchange Rate Dynamics" overshooting…» y «Galí Monacelli "Monetary Policy and Exchange Rate Volatility in a Small Open Economy"…»; WebFetch: sí, dos páginas índice; IDEAS da vol. 49(5), págs. 913-940)
- **Contenido:** Explica la desconexión del tipo de cambio con un modelo de fijación de precios en moneda local, distribución de bienes y operadores con expectativas sesgadas: el traspaso bajo permite una volatilidad cambiaria alta sin efectos reales proporcionales.
- **Uso en el bloque:** AG-02 ANZ y TR-BCM: por qué grandes movimientos cambiarios pueden coexistir con poca inflación importada (G10) y por qué no ocurre igual en EM.
- **Limitaciones:** Confirmado solo por índices.

#### FXA-0021 · Q 81 (A) — What Do Stock Markets Tell Us about Exchange Rates?

- **Autores:** Gino Cenedese; Richard Payne; Lucio Sarno; Giorgio Valente
- **Año:** 2016
- **Publicación o institución:** Review of Finance, vol. 20, n.º 3, págs. 1045-1080
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-01 Teoría del tipo de cambio y finanzas internacionales (principal) · secundarias: TX-07, TX-05
- **Calidad Q:** 81 (A) — Tipo 24/25 · Rigor 16/20 · Autoridad 13/15 · Vigencia 9/10 · Impacto 4/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** DOI 10.1093/rof/rfv032 · https://openaccess.city.ac.uk/id/eprint/13158/
- **Acceso y licencia:** Peldaño 2 (versión de autor en City Research Online) · Licencia: Copyright OUP
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Menkhoff Sarno Schmeling Schrimpf "Currency Value" Review of Financial Studies 2017»; WebFetch: sí, página índice de City Research Online)
- **Contenido:** Contrasta la condición de paridad de rentabilidades bursátiles (Hau y Rey): los diferenciales de rentabilidad de la renta variable entre países se relacionan con movimientos cambiarios en la sección cruzada, con implicaciones para estrategias de divisas.
- **Uso en el bloque:** Analistas de segmento: relación bolsa–divisa como señal (reequilibrio de carteras cubiertas) en G10 y EM.
- **Limitaciones:** Contenido resumido a partir del título y la literatura conexa; resumen no leído en esta carga.

#### FXA-0028 · Q 80 (A) — Nominal Exchange Rate Regimes and the Behavior of Real Exchange Rates: Evidence and Implications

- **Autores:** Michael Mussa
- **Año:** 1986
- **Publicación o institución:** Carnegie-Rochester Conference Series on Public Policy, vol. 25, págs. 117-214
- **Tipo de documento:** Artículo revisado por pares (conferencia)
- **Temática:** TX-01 Teoría del tipo de cambio y finanzas internacionales (principal) · secundarias: TX-08, TX-03
- **Calidad Q:** 80 (A) — Tipo 23/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 6/10 · Impacto 9/10 · Independencia 10/10 · Acceso 3/10
- **DOI / URL:** https://ucema.edu.ar/~car/dornbusch25.pdf (página índice: bibliografía de Rogoff 2002)
- **Acceso y licencia:** Peldaño 3 (Elsevier) · Licencia: Copyright Elsevier
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Dornbusch 1976 "Expectations and Exchange Rate Dynamics" overshooting…»; WebFetch: sí, bibliografía de Rogoff 2002)
- **Contenido:** Documenta que la volatilidad del tipo de cambio real es mucho mayor bajo tipos flexibles que bajo tipos fijos, lo que indica que el régimen nominal importa para las variables reales (evidencia de rigideces de precios).
- **Uso en el bloque:** Analistas de segmento y AS-EMEA (tipos fijos del Golfo, HKD): efectos de cambiar de régimen sobre la volatilidad real y la valoración.
- **Limitaciones:** Confirmado solo por bibliografía; muestra de Bretton Woods y primeros años de flotación.

#### FXA-0002 · Q 78 (B) — Local-currency pricing and the choice of exchange-rate regime

- **Autores:** Charles Engel
- **Año:** 2000
- **Publicación o institución:** European Economic Review, vol. 44, n.º 8, págs. 1449-1472
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-01 Teoría del tipo de cambio y finanzas internacionales (principal) · secundarias: TX-08
- **Calidad Q:** 78 (B) — Tipo 25/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 6/10 · Impacto 6/10 · Independencia 10/10 · Acceso 1/10
- **DOI / URL:** https://ideas.repec.org/a/eee/eecrev/v44y2000i8p1449-1472.html
- **Acceso y licencia:** Peldaño 3 (Elsevier; ficha abierta en RePEc sin resumen) · Licencia: Copyright Elsevier
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Charles Engel IDEAS RePEc author page exchange rates»; WebFetch: sí)
- **Contenido:** Analiza cómo la fijación de precios en moneda local (LCP) frente a la moneda del productor altera el traspaso del tipo de cambio y, con ello, la conveniencia de flotar o fijar; pieza clave de la «nueva macroeconomía abierta».
- **Uso en el bloque:** AG-02 ANZ y TR-BCM: por qué el traspaso a precios importados es bajo en economías con LCP y qué implica para la reacción del banco central a la depreciación.
- **Limitaciones:** Ficha RePEc sin resumen; contenido según el título y la literatura conexa; marco teórico superado en parte por el paradigma de la moneda dominante.

## TX-02 Política monetaria, bancos centrales y tipo de cambio

#### FXA-0111 · Q 91 (A) — Monetary Policy and Exchange Rate Volatility in a Small Open Economy

- **Autores:** Jordi Galí; Tommaso Monacelli
- **Año:** 2005 (CEPR DP 3346, 2002; UPF WP 835, 2004)
- **Publicación o institución:** Review of Economic Studies, vol. 72, n.º 3, págs. 707-734
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-02 Política monetaria, bancos centrales y tipo de cambio (principal) · secundarias: TX-08
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 4/10
- **DOI / URL:** https://ideas.repec.org/p/cpr/ceprdp/3346.html · versión de trabajo abierta: https://econ-papers.upf.edu/en/onepaper.php?id=835
- **Acceso y licencia:** Peldaño 2 (versión de trabajo abierta en UPF; artículo de pago) · Licencia: Copyright OUP/REStud
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Galí Monacelli "Monetary Policy and Exchange Rate Volatility in a Small Open Economy" Review of Economic Studies 2005 ideas repec»; WebFetch: sí, fichas de IDEAS y UPF)
- **Contenido:** Modelo de pequeña economía abierta con precios rígidos (Calvo) que compara tres regímenes: objetivo de inflación doméstica, objetivo de IPC y tipo de cambio fijo; difieren sobre todo en la volatilidad cambiaria que generan, y en un caso de referencia el objetivo de inflación doméstica es óptimo.
- **Uso en el bloque:** TR-BCM y Analistas G10M/EM: cuánto debe reaccionar un banco central de pequeña economía abierta (RBNZ, Riksbank, Norges Bank, bancos EM) al tipo de cambio y qué volatilidad cambiaria cabe esperar según su régimen.
- **Limitaciones:** Modelo estilizado (sin fricciones financieras ni moneda dominante).

#### FXA-0035 · Q 90 (A) — Monetary Policy Rules in Practice: Some International Evidence

- **Autores:** Richard Clarida; Jordi Galí; Mark Gertler
- **Año:** 1998
- **Publicación o institución:** European Economic Review, vol. 42, págs. 1033-1067
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-02 Política monetaria, bancos centrales y tipo de cambio (principal) · secundarias: —
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** https://www.uh.edu/~dpapell/Taylor%20Rule%20Fundamentals.pdf (página índice: bibliografía de Molodtsova y Papell)
- **Acceso y licencia:** Peldaño 3 (Elsevier) · Licencia: Copyright Elsevier
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Taylor rule fundamentals exchange rate predictability Molodtsova Papell… Clarida»; WebFetch: sí, bibliografía del PDF de Molodtsova y Papell)
- **Contenido:** Estima reglas de política monetaria prospectivas para el Bundesbank, el Banco de Japón, la Fed y los bancos centrales del Reino Unido, Francia e Italia; documenta el peso de la inflación esperada y la influencia del Bundesbank (y del tipo de cambio) en las reglas de los socios del SME.
- **Uso en el bloque:** TR-BCM: especificación de las funciones de reacción de bancos centrales del G10 que alimentan los diferenciales de tipos esperados del cribado.
- **Limitaciones:** Confirmado solo por bibliografía; periodo anterior al euro y a la política no convencional.

#### FXA-0038 · Q 90 (A) — Some Empirical Evidence on the Effects of Shocks to Monetary Policy on Exchange Rates

- **Autores:** Martin Eichenbaum; Charles L. Evans
- **Año:** 1995
- **Publicación o institución:** The Quarterly Journal of Economics, vol. 110, págs. 975-1009
- **Tipo de documento:** Artículo revisado por pares (canónico)
- **Temática:** TX-02 Política monetaria, bancos centrales y tipo de cambio (principal) · secundarias: TX-04
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** https://www.uh.edu/~dpapell/Taylor%20Rule%20Fundamentals.pdf (página índice: bibliografía de Molodtsova y Papell)
- **Acceso y licencia:** Peldaño 3 (OUP) · Licencia: Copyright OUP
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Taylor rule fundamentals exchange rate predictability Molodtsova Papell…»; WebFetch: sí, bibliografía del PDF de Molodtsova y Papell; además la búsqueda «Dornbusch 1976… Eichenbaum Evans delayed overshooting» devolvió https://ideas.repec.org/p/cdl/ucsbec/qt78k0b5zw.html, que lo discute)
- **Contenido:** Con VAR identificados, una contracción monetaria de EE. UU. aprecia el dólar de forma persistente y con máximo retrasado (sobrerreacción retardada), acompañada de desviaciones grandes de la paridad descubierta a favor de los activos en dólares.
- **Uso en el bloque:** TR-BCM y AS-G10N: duración esperada del efecto cambiario de un ciclo de subidas o bajadas de la Fed (H2–H3); AG-11 CONTRA.
- **Limitaciones:** Interpretación de «sobrerreacción retardada» discutida (Pippenger 2009); identificación VAR de la época.

#### FXA-0101 · Q 89 (A) — The effects of conventional and unconventional monetary policy on exchange rates

- **Autores:** Atsushi Inoue; Barbara Rossi
- **Año:** 2019 (NBER WP 25021; UPF Economics Working Paper 1639)
- **Publicación o institución:** Journal of International Economics, vol. 118, págs. 419-447
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-02 Política monetaria, bancos centrales y tipo de cambio (principal) · secundarias: TX-01
- **Calidad Q:** 89 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 6/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** DOI 10.1016/j.jinteco.2019.01.015 · https://bse.eu/research/publications/effects-conventional-and-unconventional-monetary-policy-exchange-rates · WP: https://nber.org/papers/w25021 · https://econ-papers.upf.edu/en/onepaper.php?id=1639
- **Acceso y licencia:** Peldaño 2 (versiones de trabajo abiertas en UPF y NBER; artículo de pago) · Licencia: Copyright Elsevier
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Inoue Rossi "The effects of conventional and unconventional monetary policy on exchange rates" Journal of International Economics 2019»; WebFetch: sí, ficha de la Barcelona School of Economics)
- **Contenido:** Identifica los shocks de política monetaria de EE. UU. como desplazamientos de toda la curva de tipos y muestra que una relajación deprecia el dólar tanto en periodos convencionales como no convencionales, con efectos que varían en el tiempo según cómo cambian las expectativas; apoya la sobrerreacción de Dornbusch y el canal de tipos reales esperados.
- **Uso en el bloque:** TR-BCM y AS-G10N: traducir cambios en la curva del Tesoro (y no solo en el tipo oficial) en el efecto esperado sobre el dólar, incluso con QE o QT.
- **Limitaciones:** Centrado en la Fed.

#### FXA-0085 · Q 88 (A) — Currency Choice and Exchange Rate Pass-Through

- **Autores:** Gita Gopinath; Oleg Itskhoki; Roberto Rigobon
- **Año:** 2010
- **Publicación o institución:** American Economic Review (2010)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-02 Política monetaria, bancos centrales y tipo de cambio (principal) · secundarias: TX-01, TX-12
- **Calidad Q:** 88 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 2/10
- **DOI / URL:** https://aeastaging.aeaweb.org/about-aea/honors-awards/bates-clark/oleg-itskhoki (página índice de la AEA)
- **Acceso y licencia:** Peldaño 3 (AEA; versión de trabajo NBER) · Licencia: Copyright AEA
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Itskhoki Mukhin "Exchange Rate Disconnect in General Equilibrium" Journal of Political Economy 2021»; WebFetch: sí, página índice de la AEA que da coautores, revista y año; volumen y páginas no vistos)
- **Contenido:** Con precios de importación de EE. UU. muestra que el traspaso del tipo de cambio depende de la moneda de facturación (mucho menor en bienes facturados en dólares, incluso a largo plazo) y que las explicaciones simples de precios rígidos son insuficientes; propone un modelo con elección endógena de moneda, márgenes dependientes de la demanda e insumos importados.
- **Uso en el bloque:** TR-BCM: estimar el traspaso de una depreciación a la inflación (y la reacción esperada del banco central) según la moneda de facturación del comercio del país; AS-EMAS y AS-EMLA.
- **Limitaciones:** Confirmado solo por índice; volumen y páginas pendientes.

#### FXA-0112 · Q 87 (A) — A Simple Framework for International Monetary Policy Analysis

- **Autores:** Richard Clarida; Jordi Galí; Mark Gertler
- **Año:** 2002
- **Publicación o institución:** Journal of Monetary Economics, vol. 49, n.º 5, págs. 879-904
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-02 Política monetaria, bancos centrales y tipo de cambio (principal) · secundarias: —
- **Calidad Q:** 87 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 9/10 · Independencia 10/10 · Acceso 3/10
- **DOI / URL:** https://ideas.repec.org/p/cpr/ceprdp/3346.html (página índice: referencias citadas por Galí y Monacelli en IDEAS)
- **Acceso y licencia:** Peldaño 3 (Elsevier) · Licencia: Copyright Elsevier
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Galí Monacelli "Monetary Policy and Exchange Rate Volatility in a Small Open Economy"…»; WebFetch: sí, lista de referencias de IDEAS con revista, volumen y páginas)
- **Contenido:** Marco neokeynesiano de dos países para analizar la política monetaria óptima con interdependencia: las ganancias de la cooperación frente a la política nacional y cómo los efectos de traspaso entre países alteran la regla óptima.
- **Uso en el bloque:** TR-BCM: interdependencia de las políticas de la Fed y del BCE y su reflejo en el tipo de cambio.
- **Limitaciones:** Confirmado solo por índice.

#### FXA-0113 · Q 87 (A) — Open-Economy Inflation Targeting

- **Autores:** Lars E. O. Svensson
- **Año:** 2000
- **Publicación o institución:** Journal of International Economics, vol. 50, n.º 1, págs. 155-183
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-02 Política monetaria, bancos centrales y tipo de cambio (principal) · secundarias: —
- **Calidad Q:** 87 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 9/10 · Independencia 10/10 · Acceso 3/10
- **DOI / URL:** https://ideas.repec.org/p/cpr/ceprdp/3346.html (página índice: referencias citadas por Galí y Monacelli en IDEAS)
- **Acceso y licencia:** Peldaño 3 (Elsevier; versiones de trabajo abiertas) · Licencia: Copyright Elsevier
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Galí Monacelli…»; WebFetch: sí, lista de referencias de IDEAS)
- **Contenido:** Analiza el objetivo de inflación en una economía abierta: el tipo de cambio añade canales de transmisión directos (precios de importación) e indirectos, y la elección entre objetivo de inflación del IPC o doméstica, estricto o flexible, cambia la volatilidad del tipo de cambio y del producto.
- **Uso en el bloque:** TR-BCM: interpretar las funciones de reacción de bancos centrales con objetivo de inflación (Riksbank, RBNZ, BoC, Norges Bank, bancos EM) ante depreciaciones.
- **Limitaciones:** Confirmado solo por índice.

#### FXA-0099 · Q 86 (A) — Monetary policy's rising FX impact in the era of ultra-low rates

- **Autores:** Massimo Ferrari; Jonathan Kearns; Andreas Schrimpf
- **Año:** 2017 (11/04/2017; también CEPR DP 11918)
- **Publicación o institución:** Banco de Pagos Internacionales, BIS Working Papers n.º 626
- **Tipo de documento:** Documento de trabajo institucional
- **Temática:** TX-02 Política monetaria, bancos centrales y tipo de cambio (principal) · secundarias: TX-06
- **Calidad Q:** 86 (A) — Tipo 20/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 6/10 · Independencia 9/10 · Acceso 9/10
- **DOI / URL:** https://www.bis.org/publ/work626.pdf · https://bis.org/publ/work626.htm · https://econpapers.repec.org/RePEc:bis:biswps:626
- **Acceso y licencia:** Peldaño 1 (serie abierta del BPI) · Licencia: Copyright BPI
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Ferrari Kearns Schrimpf "Monetary policy's rising FX impact in the era of ultra-low rates" BIS working paper»; WebFetch: sí)
- **Contenido:** Estudio de eventos de alta frecuencia con las noticias de política monetaria de siete grandes bancos centrales (2004-2015): el impacto de la política monetaria sobre el tipo de cambio ha aumentado; las noticias sobre bonos de vencimiento corto (senda futura de tipos, comunicación) son las que más mueven las divisas, y el efecto es mayor cuanto más bajos son los tipos.
- **Uso en el bloque:** TR-BCM y Analistas G10 (horizonte H1): magnitud esperada de la reacción del par a sorpresas de bancos centrales y a la orientación futura; importancia del tramo corto de la curva.
- **Limitaciones:** Muestra hasta 2015, con tipos cerca de cero; la sensibilidad puede cambiar con tipos más altos.

#### FXA-0043 · Q 86 (A) — Monetary Policy, Inflation, and the Business Cycle

- **Autores:** Jordi Galí
- **Año:** 2008
- **Publicación o institución:** Princeton University Press
- **Tipo de documento:** Manual de referencia
- **Temática:** TX-02 Política monetaria, bancos centrales y tipo de cambio (principal) · secundarias: TX-01
- **Calidad Q:** 86 (A) — Tipo 20/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** https://www.uh.edu/~dpapell/Taylor%20Rule%20Fundamentals.pdf (página índice: bibliografía de Molodtsova y Papell)
- **Acceso y licencia:** Peldaño 3 (libro de pago; existe 2.ª ed. de 2015 no verificada en esta carga) · Licencia: Copyright Princeton University Press
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Taylor rule fundamentals exchange rate predictability Molodtsova Papell…»; WebFetch: sí, bibliografía del PDF de Molodtsova y Papell)
- **Contenido:** Manual neokeynesiano de política monetaria que incluye el modelo de pequeña economía abierta (Galí-Monacelli) y la comparación de reglas que responden a la inflación doméstica, al IPC o al tipo de cambio.
- **Uso en el bloque:** TR-BCM: marco formal para interpretar cómo un banco central de economía abierta (BNS, Riksbank, RBNZ, bancos EM) reacciona al tipo de cambio.
- **Limitaciones:** Manual técnico; capítulo de economía abierta concreto (no confirmado en esta carga).

#### FXA-0115 · Q 86 (A) — Monetary Policy in the Open Economy Revisited: Price Setting and Exchange-Rate Flexibility

- **Autores:** Michael B. Devereux; Charles Engel
- **Año:** 2003
- **Publicación o institución:** Review of Economic Studies, vol. 70, n.º 4, págs. 765-783
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-02 Política monetaria, bancos centrales y tipo de cambio (principal) · secundarias: TX-08
- **Calidad Q:** 86 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 8/10 · Independencia 10/10 · Acceso 3/10
- **DOI / URL:** https://ideas.repec.org/p/cpr/ceprdp/3346.html (página índice: referencias citadas por Galí y Monacelli en IDEAS)
- **Acceso y licencia:** Peldaño 3 (OUP) · Licencia: Copyright OUP/REStud
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Galí Monacelli…»; WebFetch: sí, lista de referencias de IDEAS)
- **Contenido:** Muestra que, si los precios se fijan en la moneda del consumidor (LCP), la política monetaria óptima tiende a estabilizar el tipo de cambio (fijo como óptimo), al contrario que con fijación en moneda del productor, donde la flexibilidad cambiaria es deseable.
- **Uso en el bloque:** TR-BCM y AS-EMAS/EMEA: por qué algunos bancos centrales gestionan activamente el tipo de cambio; enlace con el paradigma de la moneda dominante.
- **Limitaciones:** Confirmado solo por índice.

#### FXA-0055 · Q 86 (A) — Sources of Real Exchange Rate Fluctuations: How Important are Nominal Shocks?

- **Autores:** Richard Clarida; Jordi Galí
- **Año:** 1994
- **Publicación o institución:** Carnegie-Rochester Conference Series on Public Policy, vol. 41, n.º 1, págs. 1-56
- **Tipo de documento:** Artículo revisado por pares (conferencia)
- **Temática:** TX-02 Política monetaria, bancos centrales y tipo de cambio (principal) · secundarias: TX-03, TX-01
- **Calidad Q:** 86 (A) — Tipo 23/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 10/10 · Independencia 10/10 · Acceso 4/10
- **DOI / URL:** https://ideas.repec.org/a/aea/jecper/v18y2004i4p135-158.html (página índice: referencias citadas por Taylor y Taylor 2004)
- **Acceso y licencia:** Peldaño 3 (Elsevier; versión NBER de trabajo) · Licencia: Copyright Elsevier
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Alan Taylor Mark Taylor 2004 "The Purchasing Power Parity Debate"…»; WebFetch: sí, lista de referencias de IDEAS)
- **Contenido:** Con VAR estructurales identificados por restricciones de largo plazo, descompone los tipos de cambio reales en shocks de oferta, demanda y monetarios: los shocks de demanda dominan, pero los monetarios explican una parte relevante de las fluctuaciones en algunos pares.
- **Uso en el bloque:** TR-BCM y Analistas G10: cuánto del movimiento de un tipo real cabe atribuir a la política monetaria frente a shocks reales.
- **Limitaciones:** Confirmado solo por índice; identificación sujeta a supuestos de largo plazo.

#### ANA-DOC-0370 · Q 85 (A) — International Channels of Transmission of Monetary Policy and the Mundellian Trilemma

- **Autores:** Hélène Rey
- **Año:** 2016
- **Publicación o institución:** IMF Economic Review, vol. 64, n.º 1, págs. 6-35
- **Tipo de documento:** Artículo revisado por pares (Mundell-Fleming Lecture)
- **Temática:** TX-02 Política monetaria, bancos centrales y tipo de cambio (principal) · secundarias: TX-07
- **Calidad Q:** 85 (A) — Tipo 24/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 10/10 · Acceso 3/10
- **DOI / URL:** https://ideas.repec.org/a/pal/imfecr/v64y2016i1p6-35.html
- **Acceso y licencia:** Peldaño 3 (Palgrave/FMI) · Licencia: Copyright FMI
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Hélène Rey IDEAS RePEc author page publications»; WebFetch: sí, sobre la página de autora de IDEAS que lista la obra) · reutilizada del F7 V3.2 (TA-07)
- **Contenido:** Canales internacionales de transmisión de la política monetaria del centro (EE. UU.) incluso a países con tipo de cambio flexible (Reino Unido, Canadá, Nueva Zelanda, Suecia) y revisión del trilema de Mundell: el tipo flexible no aísla plenamente de la Fed.
- **Uso en el bloque:** TR-BCM: transmisión de las decisiones de la Fed a condiciones financieras y divisas de economías G10 con tipo flotante; AS-G10M: GBP, CAD, NZD, SEK frente a sorpresas de la Fed.
- **Limitaciones:** Solapa parcialmente con la literatura del ciclo financiero global (TX-07); se conserva como versión publicada revisada.

#### FXA-0116 · Q 85 (A) — International Dimensions of Optimal Monetary Policy

- **Autores:** Giancarlo Corsetti; Paolo Pesenti
- **Año:** 2005
- **Publicación o institución:** Journal of Monetary Economics, vol. 52, n.º 2, págs. 281-305
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-02 Política monetaria, bancos centrales y tipo de cambio (principal) · secundarias: —
- **Calidad Q:** 85 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 7/10 · Independencia 10/10 · Acceso 3/10
- **DOI / URL:** https://ideas.repec.org/p/cpr/ceprdp/3346.html (página índice: referencias citadas por Galí y Monacelli en IDEAS)
- **Acceso y licencia:** Peldaño 3 (Elsevier) · Licencia: Copyright Elsevier
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Galí Monacelli…»; WebFetch: sí, lista de referencias de IDEAS)
- **Contenido:** Caracteriza la política monetaria óptima en economía abierta con traspaso incompleto: el banco central debe atender a la volatilidad del tipo de cambio y al traspaso, no solo a la inflación doméstica.
- **Uso en el bloque:** TR-BCM: fundamento para esperar reacciones de bancos centrales a movimientos cambiarios grandes.
- **Limitaciones:** Confirmado solo por índice; contenido según el título y la literatura conexa.

#### FXA-0036 · Q 85 (A) — Discretion versus Policy Rules in Practice

- **Autores:** John B. Taylor
- **Año:** 1993
- **Publicación o institución:** Carnegie-Rochester Conference Series on Public Policy, vol. 39, págs. 195-214
- **Tipo de documento:** Artículo revisado por pares (canónico)
- **Temática:** TX-02 Política monetaria, bancos centrales y tipo de cambio (principal) · secundarias: —
- **Calidad Q:** 85 (A) — Tipo 23/25 · Rigor 14/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 4/10
- **DOI / URL:** https://www.uh.edu/~dpapell/Taylor%20Rule%20Fundamentals.pdf (página índice: bibliografía de Molodtsova y Papell)
- **Acceso y licencia:** Peldaño 3 (Elsevier) · Licencia: Copyright Elsevier
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Taylor rule fundamentals exchange rate predictability Molodtsova Papell…»; WebFetch: sí, bibliografía del PDF de Molodtsova y Papell)
- **Contenido:** Propone la «regla de Taylor»: el tipo de interés oficial responde a la desviación de la inflación respecto al objetivo y a la brecha de producción; describe bien la política de la Fed entre 1987 y 1992.
- **Uso en el bloque:** TR-BCM: referencia normativa para estimar la senda de tipos de cada banco central y sus diferenciales, insumo de las lentes de política monetaria y carry.
- **Limitaciones:** Obra de política monetaria general (no específica de divisas); confirmada solo por bibliografía.

#### FXA-0087 · Q 84 (A) — Exchange Rate Dynamics and Monetary Spillovers with Imperfect Financial Markets

- **Autores:** Ozge Akinci; Albert Queralto
- **Año:** 2019 (NY Fed Staff Report 849, mayo de 2018, rev. mayo de 2019; IFDP 1254, julio-agosto de 2019)
- **Publicación o institución:** Board of Governors of the Federal Reserve System, International Finance Discussion Papers n.º 1254 · Federal Reserve Bank of New York, Staff Reports n.º 849
- **Tipo de documento:** Documento de trabajo institucional
- **Temática:** TX-02 Política monetaria, bancos centrales y tipo de cambio (principal) · secundarias: TX-04, TX-10
- **Calidad Q:** 84 (A) — Tipo 20/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 5/10 · Independencia 9/10 · Acceso 9/10
- **DOI / URL:** DOI 10.17016/IFDP.2019.1254 · https://www.federalreserve.gov/econres/ifdp/exchange-rate-dynamics-and-monetary-spillovers-with-imperfect-financial-markets.htm · https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr849.pdf
- **Acceso y licencia:** Peldaño 1 (publicaciones abiertas de la Fed) · Licencia: dominio público / Fed
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Kalemli-Özcan 2019 "U.S. Monetary Policy and International Risk Spillovers"…»; WebFetch: sí, páginas de la Fed y del NY Fed)
- **Contenido:** Modelo neokeynesiano de dos países con fricciones financieras y deuda en dólares: los límites al arbitraje generan desvíos endógenos de la UIP que, junto con la facturación en dólares, amplifican los efectos de la Fed en el exterior; estabilizar el tipo de cambio puede reducir el bienestar y aumentar su volatilidad. Empíricamente, los desvíos de la UIP se asocian a fricciones de crédito.
- **Uso en el bloque:** TR-BCM y Analistas EM: canal de transmisión de la Fed a divisas emergentes con deuda en dólares; AG-11 CONTRA: riesgo de que la defensa del tipo de cambio fracase.
- **Limitaciones:** Resultados de modelo calibrado.

#### FXA-0030 · Q 84 (A) — Taylor Rule Exchange Rate Forecasting During the Financial Crisis

- **Autores:** Tanya Molodtsova; David H. Papell
- **Año:** 2012
- **Publicación o institución:** National Bureau of Economic Research (NBER Working Paper 18330)
- **Tipo de documento:** Documento de trabajo institucional
- **Temática:** TX-02 Política monetaria, bancos centrales y tipo de cambio (principal) · secundarias: TX-13
- **Calidad Q:** 84 (A) — Tipo 20/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 6/10 · Independencia 10/10 · Acceso 8/10
- **DOI / URL:** https://www.nber.org/papers/w18330.pdf
- **Acceso y licencia:** Peldaño 1 (PDF del NBER) · Licencia: Copyright de los autores
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Taylor rule fundamentals exchange rate predictability Molodtsova Papell…»; WebFetch: sí)
- **Contenido:** Con datos en tiempo real del euro/dólar antes, durante y después de la crisis de 2008-2009, solo el modelo de regla de Taylor con coeficientes estimados y brecha de desempleo bate de forma consistente al paseo aleatorio; añadir diferenciales de crédito o índices de condiciones financieras mejora varios modelos.
- **Uso en el bloque:** TR-BCM y AS-G10N (EUR/USD): ajustar las reglas de Taylor en periodos de crisis o tipos en el límite inferior; incorporar condiciones financieras.
- **Limitaciones:** Un solo par; muestra hasta 2012.

#### FXA-0117 · Q 83 (A) — Into the Mussa Puzzle: Monetary Policy Regimes and the Real Exchange Rate in a Small Open Economy

- **Autores:** Tommaso Monacelli
- **Año:** 2004
- **Publicación o institución:** Journal of International Economics, vol. 62, n.º 1, págs. 191-217
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-02 Política monetaria, bancos centrales y tipo de cambio (principal) · secundarias: TX-08, TX-03
- **Calidad Q:** 83 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 13/15 · Vigencia 7/10 · Impacto 8/10 · Independencia 10/10 · Acceso 3/10
- **DOI / URL:** https://ideas.repec.org/p/cpr/ceprdp/3346.html (página índice: referencias citadas por Galí y Monacelli en IDEAS)
- **Acceso y licencia:** Peldaño 3 (Elsevier) · Licencia: Copyright Elsevier
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Galí Monacelli…»; WebFetch: sí, lista de referencias de IDEAS)
- **Contenido:** Explica el enigma de Mussa (la volatilidad del tipo real aumenta al pasar de tipos fijos a flotantes) a partir del régimen de política monetaria en una pequeña economía abierta con precios rígidos.
- **Uso en el bloque:** TR-BCM y AS-EMEA (tipos fijos del Golfo, HKD): efecto esperado de un cambio de régimen monetario sobre la volatilidad del tipo real.
- **Limitaciones:** Confirmado solo por índice.

#### FXA-0114 · Q 82 (A) — Policy Rules for Open Economies

- **Autores:** Laurence M. Ball
- **Año:** 1999
- **Publicación o institución:** En J. B. Taylor (ed.), Monetary Policy Rules, NBER / University of Chicago Press, págs. 127-156
- **Tipo de documento:** Capítulo de libro (conferencia NBER)
- **Temática:** TX-02 Política monetaria, bancos centrales y tipo de cambio (principal) · secundarias: —
- **Calidad Q:** 82 (A) — Tipo 21/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 9/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** https://ideas.repec.org/p/cpr/ceprdp/3346.html (página índice: referencias citadas por Galí y Monacelli en IDEAS)
- **Acceso y licencia:** Peldaño 2 (capítulo NBER, generalmente de lectura libre en nber.org) · Licencia: Copyright NBER
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Galí Monacelli…»; WebFetch: sí, lista de referencias de IDEAS)
- **Contenido:** Extiende las reglas de política monetaria a economías abiertas: propone usar un índice de condiciones monetarias (tipo de interés y tipo de cambio) y apuntar a una inflación «de largo plazo» que filtre el efecto transitorio del tipo de cambio.
- **Uso en el bloque:** TR-BCM: origen de los índices de condiciones monetarias que usan bancos centrales de economías abiertas para leer el endurecimiento implícito de una apreciación.
- **Limitaciones:** Confirmado solo por índice.

#### FXA-0041 · Q 81 (A) — Taylor Rules with Real-Time Data: A Tale of Two Countries and One Exchange Rate

- **Autores:** Tanya Molodtsova; Alex Nikolsko-Rzhevskyy; David H. Papell
- **Año:** 2008
- **Publicación o institución:** Journal of Monetary Economics, vol. 55, págs. S63-S79
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-02 Política monetaria, bancos centrales y tipo de cambio (principal) · secundarias: TX-13
- **Calidad Q:** 81 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 13/15 · Vigencia 7/10 · Impacto 6/10 · Independencia 10/10 · Acceso 4/10
- **DOI / URL:** https://www.uh.edu/~dpapell/Taylor%20Rule%20Fundamentals.pdf (página índice: bibliografía de Molodtsova y Papell)
- **Acceso y licencia:** Peldaño 3 (Elsevier) · Licencia: Copyright Elsevier
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Taylor rule fundamentals exchange rate predictability Molodtsova Papell…»; WebFetch: sí, bibliografía del PDF de Molodtsova y Papell; la búsqueda devolvió además https://www.uh.edu/~dpapell/Taylor%20Real%20Time.pdf)
- **Contenido:** Estima reglas de Taylor con datos en tiempo real para EE. UU. y Alemania y muestra que las desviaciones implícitas de política relativa ayudan a explicar y predecir el tipo de cambio marco/dólar.
- **Uso en el bloque:** TR-BCM: necesidad de usar datos en tiempo real (no revisados) al construir señales de política monetaria; AG-20 EVAL: evitar sesgo de anticipación.
- **Limitaciones:** Confirmado solo por bibliografía; un solo par.

#### FXA-0034 · Q 80 (A) — Is Bad News About Inflation Good News for the Exchange Rate?

- **Autores:** Richard Clarida; Daniel Waldman
- **Año:** 2008
- **Publicación o institución:** En J. Y. Campbell (ed.), Asset Prices and Monetary Policy, University of Chicago Press (NBER)
- **Tipo de documento:** Capítulo de libro (conferencia NBER)
- **Temática:** TX-02 Política monetaria, bancos centrales y tipo de cambio (principal) · secundarias: TX-06
- **Calidad Q:** 80 (A) — Tipo 21/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 7/10 · Independencia 10/10 · Acceso 3/10
- **DOI / URL:** https://www.uh.edu/~dpapell/Taylor%20Rule%20Fundamentals.pdf (página índice: bibliografía de Molodtsova y Papell)
- **Acceso y licencia:** Peldaño 3 (libro de pago) · Licencia: Copyright NBER/UCP
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Taylor rule fundamentals exchange rate predictability Molodtsova Papell… Clarida Waldman»; WebFetch: sí, bibliografía del PDF de Molodtsova y Papell)
- **Contenido:** Con datos de alta frecuencia de anuncios de inflación, muestra que en países con objetivo de inflación una sorpresa al alza de la inflación aprecia la divisa, porque el mercado anticipa una respuesta más restrictiva del banco central (lógica de regla de Taylor).
- **Uso en el bloque:** TR-BCM y Analistas G10 (horizonte H1): signo esperado de la reacción del par a sorpresas de IPC según la credibilidad del banco central; comparación con EM de credibilidad baja.
- **Limitaciones:** Confirmado solo por bibliografía; páginas no vistas.

#### FXA-0003 · Q 77 (B) — Optimal Exchange Rate Policy: The Influence of Price Setting and Asset Markets

- **Autores:** Charles Engel
- **Año:** 2001
- **Publicación o institución:** Journal of Money, Credit and Banking, vol. 33, n.º 2, págs. 518-541
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-02 Política monetaria, bancos centrales y tipo de cambio (principal) · secundarias: TX-08
- **Calidad Q:** 77 (B) — Tipo 25/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 6/10 · Impacto 5/10 · Independencia 10/10 · Acceso 1/10
- **DOI / URL:** https://ideas.repec.org/a/mcb/jmoncb/v33y2001i2p518-41.html
- **Acceso y licencia:** Peldaño 3 (Blackwell/Ohio State University Press) · Licencia: Copyright del editor
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Charles Engel IDEAS RePEc author page exchange rates»; WebFetch: sí)
- **Contenido:** Con modelos de dos países, precios rígidos y agentes prospectivos, muestra que la política cambiaria óptima (fijar o flotar) depende de cómo se fijan los precios y de cuánto riesgo comparten los mercados de activos; la evidencia de precios mexicanos indica violaciones de la ley del precio único.
- **Uso en el bloque:** TR-BCM y AS-EMLA: marco para valorar cuánto debería reaccionar un banco central al tipo de cambio según el traspaso y la profundidad financiera.
- **Limitaciones:** Resultados de modelo; evidencia empírica limitada a México.

#### FXA-0060 · Q 75 (B) — Forward-Looking Policy Rules and Currency Premia

- **Autores:** Ilias Filippou; Mark P. Taylor
- **Año:** 2019
- **Publicación o institución:** Centre for Economic Policy Research (CEPR Discussion Paper 13835)
- **Tipo de documento:** Documento de trabajo institucional
- **Temática:** TX-02 Política monetaria, bancos centrales y tipo de cambio (principal) · secundarias: TX-05
- **Calidad Q:** 75 (B) — Tipo 20/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 3/10 · Independencia 10/10 · Acceso 4/10
- **DOI / URL:** https://causalclaims.trfetzer.com/author/MarkPTaylor.html (página índice de trabajos del autor; enlace DP13835)
- **Acceso y licencia:** Peldaño 3 (CEPR, acceso para miembros) · Licencia: Copyright de los autores/CEPR
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Alan Taylor Mark Taylor 2004 "The Purchasing Power Parity Debate"…»; WebFetch: sí, página índice https://causalclaims.trfetzer.com/author/MarkPTaylor.html)
- **Contenido:** Relaciona las primas cambiarias con reglas de política monetaria prospectivas: ordenar divisas por la desviación esperada de la política monetaria respecto a la regla genera diferencias de rentabilidad.
- **Uso en el bloque:** TR-BCM y AS-ESTR: señal transversal basada en la senda esperada de los bancos centrales.
- **Limitaciones:** Confirmado solo por índice; contenido inferido del título, a cotejar.

#### FXA-0100 · Q 74 (B) — Exchange Rate Policies at the Zero Lower Bound

- **Autores:** Manuel Amador; Javier Bianchi; Luigi Bocola; Fabrizio Perri
- **Año:** 2017 (documento de trabajo recogido en NEP nep-cba de 02/04/2017)
- **Publicación o institución:** Documento de trabajo (serie no visible en el índice consultado)
- **Tipo de documento:** Documento de trabajo académico
- **Temática:** TX-02 Política monetaria, bancos centrales y tipo de cambio (principal) · secundarias: TX-08, TX-04
- **Calidad Q:** 74 (B) — Tipo 18/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 8/10 · Impacto 6/10 · Independencia 10/10 · Acceso 1/10
- **DOI / URL:** https://nep.repec.org/nep-cba/2017-04-02 (página índice NEP)
- **Acceso y licencia:** Peldaño 3 (versión publicada no verificada) · Licencia: Copyright de los autores
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Ferrari Kearns Schrimpf "Monetary policy's rising FX impact in the era of ultra-low rates" BIS working paper»; WebFetch: sí, página índice https://nep.repec.org/nep-cba/2017-04-02 con título y autores)
- **Contenido:** Analiza la política cambiaria de un banco central que quiere evitar la apreciación cuando los tipos están en el límite inferior: para sostener un tipo de cambio por debajo del de libre mercado debe acumular reservas y admitir desvíos de la paridad cubierta/descubierta, con costes crecientes (caso del Banco Nacional Suizo).
- **Uso en el bloque:** TR-BCM y AS-G10N (CHF, EUR/CHF): límites y costes de defender un suelo cambiario con tipos en cero; señales de abandono del suelo.
- **Limitaciones:** Confirmado solo por índice (título y autores); contenido según conocimiento general de la obra, a cotejar; versión publicada pendiente de verificar.

#### FXA-0042 · Q 72 (B) — Real Exchange Rate Persistence and Systematic Monetary Policy Behaviour

- **Autores:** Jan J. J. Groen; Akito Matsumoto
- **Año:** 2004
- **Publicación o institución:** Bank of England, Working Paper n.º 231
- **Tipo de documento:** Documento de trabajo institucional
- **Temática:** TX-02 Política monetaria, bancos centrales y tipo de cambio (principal) · secundarias: TX-03
- **Calidad Q:** 72 (B) — Tipo 20/25 · Rigor 14/20 · Autoridad 13/15 · Vigencia 6/10 · Impacto 3/10 · Independencia 9/10 · Acceso 7/10
- **DOI / URL:** https://www.uh.edu/~dpapell/Taylor%20Rule%20Fundamentals.pdf (página índice: bibliografía de Molodtsova y Papell)
- **Acceso y licencia:** Peldaño 2 (serie abierta del Banco de Inglaterra) · Licencia: Copyright Bank of England
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Taylor rule fundamentals exchange rate predictability Molodtsova Papell…»; WebFetch: sí, bibliografía del PDF de Molodtsova y Papell)
- **Contenido:** Relaciona la persistencia del tipo de cambio real con el comportamiento sistemático de la política monetaria (grado de respuesta a la inflación y suavizado de tipos) en un modelo de economía abierta.
- **Uso en el bloque:** TR-BCM y Analistas de segmento: por qué las desviaciones del valor justo duran más bajo ciertas funciones de reacción; enlace entre TX-02 y TX-03.
- **Limitaciones:** Confirmado solo por bibliografía; contenido resumido del título, a cotejar.

## TX-03 Tipo de cambio de equilibrio y valoración (PPA, BEER, FEER, REER)

#### FXA-0074 · Q 90 (A) — The External Balance Assessment Methodology: 2018 Update

- **Autores:** Luis M. Cubeddu; Signe Krogstrup; Gustavo Adler; Pau Rabanal; Mai Chi Dao; Swarnali Ahmed Hannan; Luciana Juvenal; Carolina Osorio Buitron; Cyril Rebillard; Daniel Garcia-Macia; Callum Jones; Jair Rodriguez; Kyun Suk Chang; Deepali Gautam; Zijiao Wang (la ficha del catálogo del FMI añade a Nan Li)
- **Año:** 2019 (marzo)
- **Publicación o institución:** Fondo Monetario Internacional, IMF Working Paper WP/19/65 (Departamento de Estudios)
- **Tipo de documento:** Documento metodológico de organismo oficial
- **Temática:** TX-03 Tipo de cambio de equilibrio y valoración (PPA, BEER, FEER, REER) (principal) · secundarias: TX-07
- **Calidad Q:** 90 (A) — Tipo 23/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 8/10 · Acceso 9/10
- **DOI / URL:** https://www.imf.org/external/pubs/cat/longres.aspx?sk=46643.0 · PDF: https://imf.org/-/media/Files/Publications/WP/2019/WPIEA2019065.ashx · copia: https://www.sipotra.it/wp-content/uploads/2019/03/The-External-Balance-Assessment-Methodology-2018-Update.pdf
- **Acceso y licencia:** Peldaño 1 (publicación abierta del FMI) · Licencia: Copyright FMI
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «IMF External Balance Assessment EBA methodology 2019 update Cubeddu working paper real exchange rate model»; WebFetch: sí, ficha del FMI y PDF)
- **Contenido:** Metodología EBA del FMI (2012, revisada en 2015 y 2018) para evaluar de forma multilateralmente coherente la cuenta corriente y el tipo de cambio efectivo real de 49 economías: modelos de cuenta corriente, de nivel e índice del REER y de sostenibilidad externa, más herramientas sobre factores estructurales y sesgos de medición.
- **Uso en el bloque:** Analistas de segmento, AS-ESTR y TR-BCM: referencia oficial de «brecha del REER» (sobre o infravaloración) que publica el FMI en su Informe del Sector Externo; comparar con estimaciones propias del MOTOR.
- **Limitaciones:** Las brechas incluyen un componente normativo (brechas de política); actualizaciones posteriores pueden cambiar coeficientes.

#### FXA-0044 · Q 90 (A) — The Purchasing Power Parity Debate

- **Autores:** Alan M. Taylor; Mark P. Taylor
- **Año:** 2004 (CEPR DP 4495; NBER WP 10607)
- **Publicación o institución:** Journal of Economic Perspectives, vol. 18, n.º 4, págs. 135-158
- **Tipo de documento:** Artículo de revisión revisado por pares
- **Temática:** TX-03 Tipo de cambio de equilibrio y valoración (PPA, BEER, FEER, REER) (principal) · secundarias: TX-01
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / URL:** DOI 10.1257/0895330042632744 · https://ideas.repec.org/a/aea/jecper/v18y2004i4p135-158.html · https://wrap.warwick.ac.uk/id/eprint/7558
- **Acceso y licencia:** Peldaño 2 (JEP es de acceso libre en la AEA; registro en WRAP con texto restringido) · Licencia: Copyright AEA
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Alan Taylor Mark Taylor 2004 "The Purchasing Power Parity Debate" Journal of Economic Perspectives»; WebFetch: sí)
- **Contenido:** Historia y estado de la PPA desde la Escuela de Salamanca: tras décadas de rechazo, los datos largos y los métodos no lineales devuelven apoyo a la PPA de largo plazo, con reversión más rápida cuando las desviaciones son grandes.
- **Uso en el bloque:** AS-ESTR (valor) y Analistas de segmento: justificación de la PPA como ancla de largo plazo (H4) y de la reversión no lineal (desviaciones grandes revierten antes).
- **Limitaciones:** Revisión hasta 2004; no trata BEER/FEER en detalle.

#### FXA-0045 · Q 89 (A) — PPP Strikes Back: Aggregation and the Real Exchange Rate

- **Autores:** Jean Imbs; Haroon Mumtaz; Morten O. Ravn; Hélène Rey
- **Año:** 2005
- **Publicación o institución:** The Quarterly Journal of Economics, vol. 120, n.º 1, págs. 1-43
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-03 Tipo de cambio de equilibrio y valoración (PPA, BEER, FEER, REER) (principal) · secundarias: —
- **Calidad Q:** 89 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 9/10 · Independencia 10/10 · Acceso 4/10
- **DOI / URL:** https://ideas.repec.org/a/aea/jecper/v18y2004i4p135-158.html (página índice: referencias citadas por Taylor y Taylor 2004 en IDEAS)
- **Acceso y licencia:** Peldaño 3 (OUP) · Licencia: Copyright OUP
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Alan Taylor Mark Taylor 2004 "The Purchasing Power Parity Debate"…»; WebFetch: sí, lista de referencias de la ficha IDEAS con revista, volumen y páginas)
- **Contenido:** Muestra que el sesgo de agregación (sectores con velocidades de ajuste distintas) explica buena parte del enigma de la PPA: con datos sectoriales la vida media de las desviaciones cae muy por debajo de los 3-5 años de consenso.
- **Uso en el bloque:** AS-ESTR y AG-13 MOTOR (vía F8): advertencia sobre el uso de índices agregados al medir la convergencia a valor; horizontes de reversión más cortos con precios desagregados.
- **Limitaciones:** Confirmado solo por índice; resultados discutidos por Chen y Engel.

#### FXA-0004 · Q 88 (A) — Accounting for U.S. Real Exchange Rate Changes

- **Autores:** Charles Engel
- **Año:** 1999
- **Publicación o institución:** Journal of Political Economy, vol. 107, n.º 3, págs. 507-538
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-03 Tipo de cambio de equilibrio y valoración (PPA, BEER, FEER, REER) (principal) · secundarias: TX-01
- **Calidad Q:** 88 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 9/10 · Independencia 10/10 · Acceso 4/10
- **DOI / URL:** DOI 10.1086/250070 · https://en.wikipedia.org/wiki/Charles_Engel (página índice con enlace al PDF del autor)
- **Acceso y licencia:** Peldaño 2 (PDF del autor en ssc.wisc.edu; artículo de pago) · Licencia: Copyright University of Chicago Press
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Charles Engel IDEAS RePEc author page exchange rates»; WebFetch: sí, página índice https://en.wikipedia.org/wiki/Charles_Engel)
- **Contenido:** Descompone la variación del tipo de cambio real de EE. UU. y concluye que casi toda procede de desviaciones de la ley del precio único en bienes comerciables, no del precio relativo de los no comerciables (contra la intuición Balassa-Samuelson a horizontes cortos y medios).
- **Uso en el bloque:** Analistas de segmento y AG-13 MOTOR (por vía de F8): advertencia sobre qué índice de precios usar en REER/PPA y sobre el alcance de Balassa-Samuelson (relevante para EMAS).
- **Limitaciones:** Muestra de EE. UU. con sus socios; conclusiones matizadas en emergentes con fuerte crecimiento de productividad.

#### FXA-0062 · Q 88 (A) — Exchange Rates and Economic Fundamentals: A Methodological Comparison of BEERs and FEERs

- **Autores:** Peter B. Clark; Ronald MacDonald
- **Año:** 1998 (IMF WP 98/67; reimpreso en R. MacDonald y J. Stein (eds.), Equilibrium Exchange Rates, Kluwer, 1999)
- **Publicación o institución:** Fondo Monetario Internacional, IMF Working Paper n.º 1998/067
- **Tipo de documento:** Documento de trabajo institucional (metodología de referencia)
- **Temática:** TX-03 Tipo de cambio de equilibrio y valoración (PPA, BEER, FEER, REER) (principal) · secundarias: —
- **Calidad Q:** 88 (A) — Tipo 20/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 10/10 · Independencia 9/10 · Acceso 9/10
- **DOI / URL:** https://www.imf.org/en/Publications/WP/Issues/2016/12/30/Exchange-Rates-and-Economic-Fundamentals-A-Methodological-Comparison-of-BEERs-and-FEERs-2592 · https://ideas.repec.org/p/imf/imfwpa/1998-067.html
- **Acceso y licencia:** Peldaño 1 (publicación abierta del FMI) · Licencia: Copyright FMI
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Clark MacDonald "Exchange Rates and Economic Fundamentals: A Methodological Comparison of BEERs and FEERs" IMF Working Paper»; WebFetch: sí, ficha IDEAS)
- **Contenido:** Compara los dos enfoques de tipo de cambio de equilibrio: FEER (tipo real que equilibra la cuenta corriente con pleno empleo y flujos de capital sostenibles) y BEER (relación econométrica de comportamiento entre el tipo real y sus fundamentales), con una aplicación a las divisas del G-3. Más de 300 citas en RePEc.
- **Uso en el bloque:** Analistas de segmento, AS-ESTR y AG-13 MOTOR (perfil de valoración): definición de referencia de BEER y FEER para la lente «valor» (Documento 0, 8.1).
- **Limitaciones:** Aplicación limitada al G-3 de los noventa.

#### FXA-0046 · Q 88 (A) — Perspectives on PPP and Long-Run Real Exchange Rates

- **Autores:** Kenneth A. Froot; Kenneth Rogoff
- **Año:** 1995
- **Publicación o institución:** En G. M. Grossman y K. Rogoff (eds.), Handbook of International Economics, vol. 3, cap. 32, págs. 1647-1688 (Elsevier)
- **Tipo de documento:** Capítulo de manual de referencia
- **Temática:** TX-03 Tipo de cambio de equilibrio y valoración (PPA, BEER, FEER, REER) (principal) · secundarias: TX-01
- **Calidad Q:** 88 (A) — Tipo 20/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 10/10 · Independencia 10/10 · Acceso 8/10
- **DOI / URL:** https://ideas.repec.org/a/aea/jecper/v18y2004i4p135-158.html (página índice: referencias citadas por Taylor y Taylor 2004)
- **Acceso y licencia:** Peldaño 3 (Elsevier; versión NBER de trabajo) · Licencia: Copyright Elsevier
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Alan Taylor Mark Taylor 2004 "The Purchasing Power Parity Debate"…»; WebFetch: sí, lista de referencias de IDEAS)
- **Contenido:** Revisión de manual de las pruebas de la PPA (de paseo aleatorio a cointegración y paneles) y de los determinantes reales del tipo de cambio real de largo plazo (productividad, Balassa-Samuelson, gasto público).
- **Uso en el bloque:** Todos los Analistas de segmento: guía de referencia sobre qué se puede y qué no se puede inferir de una desviación de la PPA.
- **Limitaciones:** Literatura hasta 1994.

#### FXA-0047 · Q 87 (A) — Nonlinear Mean-Reversion in Real Exchange Rates: Toward a Solution to the Purchasing Power Parity Puzzles

- **Autores:** Mark P. Taylor; David A. Peel; Lucio Sarno
- **Año:** 2001 (CEPR DP 2658)
- **Publicación o institución:** International Economic Review, vol. 42, n.º 4, págs. 1015-1042
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-03 Tipo de cambio de equilibrio y valoración (PPA, BEER, FEER, REER) (principal) · secundarias: TX-05
- **Calidad Q:** 87 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 14/15 · Vigencia 8/10 · Impacto 9/10 · Independencia 10/10 · Acceso 3/10
- **DOI / URL:** https://ideas.repec.org/a/aea/jecper/v18y2004i4p135-158.html (página índice) · https://causalclaims.trfetzer.com/author/MarkPTaylor.html (índice de trabajos del autor)
- **Acceso y licencia:** Peldaño 3 (Wiley) · Licencia: Copyright Wiley
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Alan Taylor Mark Taylor 2004 "The Purchasing Power Parity Debate"…»; WebFetch: sí, dos páginas índice que dan autores, revista, volumen y páginas)
- **Contenido:** Con modelos ESTAR muestra que los tipos de cambio reales revierten a la PPA de forma no lineal: casi paseo aleatorio cerca del equilibrio y reversión rápida cuando la desviación es grande, lo que reconcilia vidas medias largas con PPA de largo plazo.
- **Uso en el bloque:** AS-ESTR y Analistas de segmento: la señal de valor gana fuerza solo con desviaciones grandes; umbrales para activar tesis de valor.
- **Limitaciones:** Confirmado solo por índices; la no linealidad depende de la especificación.

#### FXA-0018 · Q 86 (A) — The predictive information content of external imbalances for exchange rate returns: How much is it worth?

- **Autores:** Pasquale Della Corte; Lucio Sarno; Giulia Sestieri
- **Año:** 2012
- **Publicación o institución:** Review of Economics and Statistics, vol. 94, n.º 1, págs. 100-115
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-03 Tipo de cambio de equilibrio y valoración (PPA, BEER, FEER, REER) (principal) · secundarias: TX-07, TX-13
- **Calidad Q:** 86 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 8/10 · Impacto 7/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** DOI 10.1162/rest_a_00157 · https://openaccess.city.ac.uk/id/eprint/3302/
- **Acceso y licencia:** Peldaño 2 (versión de autor en City Research Online) · Licencia: Copyright MIT Press
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Menkhoff Sarno Schmeling Schrimpf "Currency Value" Review of Financial Studies 2017»; WebFetch: sí, página índice de City Research Online)
- **Contenido:** Evalúa en términos económicos (valor para un inversor con asignación dinámica) el poder predictivo de los desequilibrios externos (medida de Gourinchas y Rey) sobre los tipos de cambio del dólar, y halla valor económico sustancial a horizontes largos.
- **Uso en el bloque:** AS-G10N y AS-ESTR: desequilibrio exterior como ancla de valoración del dólar a medio plazo (H3–H4).
- **Limitaciones:** Centrado en el dólar; datos de posición exterior con revisiones.

#### ANA-DOC-0310 · Q 86 (A) — The Purchasing Power Parity Puzzle

- **Autores:** Kenneth Rogoff
- **Año:** 1996
- **Publicación o institución:** Journal of Economic Literature, vol. 34, n.º 2, págs. 647-668
- **Tipo de documento:** Artículo de revisión revisado por pares
- **Temática:** TX-03 Tipo de cambio de equilibrio y valoración (PPA, BEER, FEER, REER) (principal) · secundarias: TX-01
- **Calidad Q:** 86 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 10/10 · Independencia 10/10 · Acceso 4/10
- **DOI / URL:** https://ideas.repec.org/a/aea/jeclit/v34y1996i2p647-668.html
- **Acceso y licencia:** Peldaño 3 (texto completo para miembros AEA; ficha abierta en RePEc) · Licencia: Copyright AEA
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Rogoff 1996 "The Purchasing Power Parity Puzzle" Journal of Economic Literature»; WebFetch: sí) · reutilizada del F7 V3.2 (TA-07)
- **Contenido:** Formula el «enigma de la PPA»: los tipos de cambio reales revierten a la paridad con vidas medias de 3-5 años, demasiado lentas para explicarse por rigideces nominales dada su alta volatilidad a corto plazo.
- **Uso en el bloque:** Analistas de segmento y AS-ESTR (estrategia de valor): horizonte realista (H4) de convergencia a valor justo en tesis de valoración por PPA; AG-11 CONTRA: objeción a tesis de valor a corto plazo.
- **Limitaciones:** Estimaciones de vida media sensibles a la muestra y a sesgos de agregación.

#### FXA-0075 · Q 85 (A) — The Level REER Model in the External Balance Assessment (EBA) Methodology

- **Autores:** Rui Mano; Luca A. Ricci; Mauricio Vargas
- **Año:** 2019 (13/09/2019)
- **Publicación o institución:** Fondo Monetario Internacional, IMF Working Paper (WP/19/192 según el nombre del fichero; RePEc imf:imfwpa:2019/192)
- **Tipo de documento:** Documento metodológico de organismo oficial
- **Temática:** TX-03 Tipo de cambio de equilibrio y valoración (PPA, BEER, FEER, REER) (principal) · secundarias: —
- **Calidad Q:** 85 (A) — Tipo 22/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 5/10 · Independencia 8/10 · Acceso 9/10
- **DOI / URL:** DOI 10.5089/9781513511023.001 · https://www.imf.org/en/publications/wp/issues/2019/09/13/the-level-reer-model-in-the-external-balance-assessment-eba-methodology-48588 · https://econpapers.repec.org/RePEc:imf:imfwpa:2019/192
- **Acceso y licencia:** Peldaño 1 (publicación abierta del FMI) · Licencia: Copyright FMI
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «IMF External Balance Assessment EBA methodology 2019 update…»; WebFetch: sí)
- **Contenido:** Modelo de panel de los determinantes del nivel del REER (no solo de su variación) que pasa a formar parte de la metodología EBA; recoge la gran variación transversal de niveles y muestra que con deflactores del PIB explica mejor la variación temporal que con IPC.
- **Uso en el bloque:** AS-ESTR (valor) y Analistas EM: comparar niveles de REER entre países con ajuste por fundamentales (renta per cápita, demografía, términos de intercambio).
- **Limitaciones:** Los autores piden más análisis antes de generalizar el uso de REER con deflactor del PIB.

#### FXA-0066 · Q 85 (A) — The Transfer Problem Revisited: Net Foreign Assets and Real Exchange Rates

- **Autores:** Philip R. Lane; Gian Maria Milesi-Ferretti
- **Año:** 2004
- **Publicación o institución:** The Review of Economics and Statistics, vol. 86, n.º 4, págs. 841-857
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-03 Tipo de cambio de equilibrio y valoración (PPA, BEER, FEER, REER) (principal) · secundarias: TX-07
- **Calidad Q:** 85 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 8/10 · Independencia 10/10 · Acceso 3/10
- **DOI / URL:** https://www.piie.com/sites/default/files/publications/pb/pb07-4/benassy-by-schnatz.pdf (página índice: bibliografía de Schnatz 2007)
- **Acceso y licencia:** Peldaño 3 (MIT Press) · Licencia: Copyright MIT Press
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Clark MacDonald "Exchange Rates and Economic Fundamentals…" IMF Working Paper»; WebFetch: sí, bibliografía del PDF de Schnatz con revista, volumen y páginas)
- **Contenido:** Con un panel amplio muestra que los países con mayores pasivos exteriores netos tienen tipos de cambio reales más depreciados (el «problema de la transferencia»), y que el efecto depende del grado de apertura y de la composición de la producción.
- **Uso en el bloque:** Analistas de segmento y AS-ESTR: posición de inversión internacional neta como variable de los modelos BEER.
- **Limitaciones:** Confirmado solo por bibliografía.

#### FXA-0050 · Q 85 (A) — Long-Run PPP May Not Hold After All

- **Autores:** Charles Engel
- **Año:** 2000
- **Publicación o institución:** Journal of International Economics, vol. 51, n.º 2, págs. 243-273
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-03 Tipo de cambio de equilibrio y valoración (PPA, BEER, FEER, REER) (principal) · secundarias: —
- **Calidad Q:** 85 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 8/10 · Independencia 10/10 · Acceso 3/10
- **DOI / URL:** https://ideas.repec.org/a/aea/jecper/v18y2004i4p135-158.html (página índice: referencias citadas por Taylor y Taylor 2004)
- **Acceso y licencia:** Peldaño 3 (Elsevier) · Licencia: Copyright Elsevier
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Alan Taylor Mark Taylor 2004 "The Purchasing Power Parity Debate"…»; WebFetch: sí, lista de referencias de IDEAS)
- **Contenido:** Contrapunto: si el tipo de cambio real tiene un componente no estacionario pequeño (precios de no comerciables), los contrastes habituales tienden a aceptar falsamente la PPA de largo plazo por problemas de tamaño en muestras finitas.
- **Uso en el bloque:** AG-11 CONTRA: objeción a tesis de valor que asumen reversión segura a la PPA.
- **Limitaciones:** Confirmado solo por índice.

#### FXA-0049 · Q 85 (A) — Real Exchange Rate Behavior: The Recent Float from the Perspective of the Past Two Centuries

- **Autores:** James R. Lothian; Mark P. Taylor
- **Año:** 1996
- **Publicación o institución:** Journal of Political Economy, vol. 104, n.º 3, págs. 488-509
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-03 Tipo de cambio de equilibrio y valoración (PPA, BEER, FEER, REER) (principal) · secundarias: —
- **Calidad Q:** 85 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 7/10 · Impacto 9/10 · Independencia 10/10 · Acceso 4/10
- **DOI / URL:** https://ideas.repec.org/a/aea/jecper/v18y2004i4p135-158.html (página índice: referencias citadas por Taylor y Taylor 2004)
- **Acceso y licencia:** Peldaño 3 (UCP) · Licencia: Copyright UCP
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Alan Taylor Mark Taylor 2004 "The Purchasing Power Parity Debate"…»; WebFetch: sí, lista de referencias de IDEAS)
- **Contenido:** Con dos siglos de datos dólar-libra y franco-libra halla reversión significativa a la PPA y muestra que la aparente no estacionariedad del periodo flotante se debe a la baja potencia de las muestras cortas.
- **Uso en el bloque:** AS-G10N y AS-ESTR: horizonte largo de valoración; precaución ante muestras cortas.
- **Limitaciones:** Confirmado solo por índice; dos pares.

#### FXA-0051 · Q 84 (A) — External Wealth, the Trade Balance, and the Real Exchange Rate

- **Autores:** Philip R. Lane; Gian Maria Milesi-Ferretti
- **Año:** 2002
- **Publicación o institución:** European Economic Review, vol. 46, n.º 6, págs. 1049-1071
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-03 Tipo de cambio de equilibrio y valoración (PPA, BEER, FEER, REER) (principal) · secundarias: TX-07
- **Calidad Q:** 84 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 8/10 · Independencia 10/10 · Acceso 3/10
- **DOI / URL:** https://ideas.repec.org/a/aea/jecper/v18y2004i4p135-158.html (página índice: referencias citadas por Taylor y Taylor 2004)
- **Acceso y licencia:** Peldaño 3 (Elsevier; versión de trabajo FMI) · Licencia: Copyright Elsevier
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Alan Taylor Mark Taylor 2004 "The Purchasing Power Parity Debate"…»; WebFetch: sí, lista de referencias de IDEAS)
- **Contenido:** Vincula la posición de activos exteriores netos con la balanza comercial de largo plazo y esta con el tipo de cambio real: los países deudores necesitan superávits comerciales y, por ello, un tipo real más depreciado.
- **Uso en el bloque:** Analistas de segmento y AS-ESTR: base de los modelos de tipo de cambio de equilibrio con activos exteriores netos (BEER, EBA).
- **Limitaciones:** Confirmado solo por índice.

#### FXA-0005 · Q 84 (A) — How Wide Is the Border?

- **Autores:** Charles Engel; John H. Rogers
- **Año:** 1996
- **Publicación o institución:** American Economic Review, vol. 86, págs. 1112-1125
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-03 Tipo de cambio de equilibrio y valoración (PPA, BEER, FEER, REER) (principal) · secundarias: TX-01
- **Calidad Q:** 84 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 6/10 · Impacto 9/10 · Independencia 10/10 · Acceso 4/10
- **DOI / URL:** https://en.wikipedia.org/wiki/Charles_Engel (página índice con enlace al PDF del autor: ssc.wisc.edu/~cengel/PublishedPapers/HowWideIsBorder.pdf)
- **Acceso y licencia:** Peldaño 2 (PDF del autor) · Licencia: Copyright AEA
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Charles Engel IDEAS RePEc author page exchange rates»; WebFetch: sí, página índice https://en.wikipedia.org/wiki/Charles_Engel)
- **Contenido:** Con precios de ciudades de EE. UU. y Canadá muestra que cruzar la frontera añade a la dispersión de precios tanto como miles de kilómetros de distancia, y que la rigidez de precios nominales unida a la variabilidad del tipo de cambio explica gran parte del «efecto frontera».
- **Uso en el bloque:** Analistas de segmento (AS-G10M para CAD): por qué la PPA falla a corto plazo y por qué las desviaciones del tipo real son persistentes.
- **Limitaciones:** Datos de los años ochenta y noventa; magnitud del efecto frontera discutida (Gorodnichenko y Tesar 2009).

#### FXA-0048 · Q 84 (A) — The Purchasing-Power Parity Doctrine: A Reappraisal

- **Autores:** Bela Balassa
- **Año:** 1964
- **Publicación o institución:** Journal of Political Economy, vol. 72, n.º 6, pág. 584 y ss.
- **Tipo de documento:** Artículo revisado por pares (canónico)
- **Temática:** TX-03 Tipo de cambio de equilibrio y valoración (PPA, BEER, FEER, REER) (principal) · secundarias: TX-10
- **Calidad Q:** 84 (A) — Tipo 25/25 · Rigor 13/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 10/10 · Independencia 10/10 · Acceso 3/10
- **DOI / URL:** https://ideas.repec.org/a/aea/jecper/v18y2004i4p135-158.html (página índice: referencias citadas por Taylor y Taylor 2004)
- **Acceso y licencia:** Peldaño 3 (UCP/JSTOR) · Licencia: Copyright UCP
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Alan Taylor Mark Taylor 2004 "The Purchasing Power Parity Debate"…»; WebFetch: sí, lista de referencias de IDEAS)
- **Contenido:** Formula el efecto Balassa(-Samuelson): el mayor crecimiento de la productividad en bienes comerciables de los países ricos eleva su nivel de precios y aprecia su tipo de cambio real, por lo que la PPA absoluta no se cumple entre países de distinta renta.
- **Uso en el bloque:** Analistas EM (AS-EMAS, AS-EMEA): ajustar la PPA por productividad antes de declarar una divisa emergente «barata» (Documento 0, 8.2: PPA ajustada Balassa-Samuelson).
- **Limitaciones:** Confirmado solo por índice; páginas finales no vistas.

#### FXA-0052 · Q 83 (A) — Transactions Costs and Nonlinear Adjustment in Real Exchange Rates: An Empirical Investigation

- **Autores:** Panos Michael; A. Robert Nobay; David A. Peel
- **Año:** 1997
- **Publicación o institución:** Journal of Political Economy, vol. 105, n.º 4, págs. 862-879
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-03 Tipo de cambio de equilibrio y valoración (PPA, BEER, FEER, REER) (principal) · secundarias: —
- **Calidad Q:** 83 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 13/15 · Vigencia 7/10 · Impacto 8/10 · Independencia 10/10 · Acceso 4/10
- **DOI / URL:** https://ideas.repec.org/a/aea/jecper/v18y2004i4p135-158.html (página índice: referencias citadas por Taylor y Taylor 2004)
- **Acceso y licencia:** Peldaño 3 (UCP) · Licencia: Copyright UCP
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Alan Taylor Mark Taylor 2004 "The Purchasing Power Parity Debate"…»; WebFetch: sí, lista de referencias de IDEAS)
- **Contenido:** Los costes de transacción crean una banda de inacción en la que el tipo de cambio real no revierte; fuera de ella el ajuste a la PPA es más rápido (evidencia con modelos no lineales de transición suave).
- **Uso en el bloque:** AS-ESTR: diseño de umbrales en señales de valor.
- **Limitaciones:** Confirmado solo por índice.

#### FXA-0056 · Q 82 (A) — A Panel Project on Purchasing Power Parity: Mean Reversion within and between Countries

- **Autores:** Jeffrey A. Frankel; Andrew K. Rose
- **Año:** 1996
- **Publicación o institución:** Journal of International Economics, vol. 40, n.º 1-2, págs. 209-224
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-03 Tipo de cambio de equilibrio y valoración (PPA, BEER, FEER, REER) (principal) · secundarias: —
- **Calidad Q:** 82 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 6/10 · Impacto 8/10 · Independencia 10/10 · Acceso 3/10
- **DOI / URL:** https://ideas.repec.org/a/aea/jecper/v18y2004i4p135-158.html (página índice: referencias citadas por Taylor y Taylor 2004)
- **Acceso y licencia:** Peldaño 3 (Elsevier) · Licencia: Copyright Elsevier
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Alan Taylor Mark Taylor 2004 "The Purchasing Power Parity Debate"…»; WebFetch: sí, lista de referencias de IDEAS)
- **Contenido:** Con un panel de unos 150 países y datos anuales de posguerra, encuentra reversión a la PPA con vida media de unos cuatro años, tanto dentro de cada país como entre países.
- **Uso en el bloque:** Analistas EM y AS-ESTR: horizonte de reversión de referencia para paneles amplios de divisas.
- **Limitaciones:** Confirmado solo por índice.

#### FXA-0064 · Q 82 (A) — Estimating Equilibrium Exchange Rates

- **Autores:** John Williamson
- **Año:** 1983
- **Publicación o institución:** Institute for International Economics (hoy Peterson Institute), Washington DC
- **Tipo de documento:** Monografía institucional (canónica)
- **Temática:** TX-03 Tipo de cambio de equilibrio y valoración (PPA, BEER, FEER, REER) (principal) · secundarias: TX-07
- **Calidad Q:** 82 (A) — Tipo 18/25 · Rigor 14/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 10/10 · Independencia 9/10 · Acceso 9/10
- **DOI / URL:** https://www.piie.com/sites/default/files/publications/pb/pb07-4/macdonald.pdf (página índice: bibliografía de MacDonald y Dias 2007)
- **Acceso y licencia:** Peldaño 2 (publicaciones históricas de PIIE) · Licencia: Copyright PIIE
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Clark MacDonald "Exchange Rates and Economic Fundamentals…" IMF Working Paper»; WebFetch: sí, bibliografía del PDF de MacDonald y Dias, que la cita como Williamson (1983), «Estimating Equilibrium Exchange Rates», IIE, Washington, como origen del FEER)
- **Contenido:** Origen del concepto de tipo de cambio de equilibrio fundamental (FEER): el tipo real compatible simultáneamente con equilibrio interno (pleno empleo e inflación baja) y externo (cuenta corriente igual a flujos de capital sostenibles).
- **Uso en el bloque:** Analistas de segmento y AS-ESTR: fundamento normativo del FEER usado por bancos centrales y PIIE (estimaciones periódicas de Cline y Williamson).
- **Limitaciones:** Confirmado solo por bibliografía (que la fecha en 1983); conviene cotejar año y edición en la próxima revisión. El FEER depende de un objetivo normativo de cuenta corriente.

#### FXA-0071 · Q 80 (A) — Exchange Rate Economics: Theories and Evidence

- **Autores:** Ronald MacDonald
- **Año:** 2007 (2.ª ed. de «Floating Exchange Rates: Theories and Evidence»)
- **Publicación o institución:** Routledge
- **Tipo de documento:** Manual de referencia
- **Temática:** TX-03 Tipo de cambio de equilibrio y valoración (PPA, BEER, FEER, REER) (principal) · secundarias: TX-01
- **Calidad Q:** 80 (A) — Tipo 20/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 7/10 · Impacto 7/10 · Independencia 10/10 · Acceso 7/10
- **DOI / URL:** https://www.piie.com/sites/default/files/publications/pb/pb07-4/macdonald.pdf (página índice: bibliografía de MacDonald y Dias 2007)
- **Acceso y licencia:** Peldaño 3 (libro de pago) · Licencia: Copyright Routledge
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Clark MacDonald "Exchange Rates and Economic Fundamentals…" IMF Working Paper»; WebFetch: sí, bibliografía del PDF de MacDonald y Dias)
- **Contenido:** Manual de teorías y evidencia de tipos de cambio con tratamiento extenso de los tipos de equilibrio (PPA, BEER, FEER, NATREX) por uno de los autores del BEER.
- **Uso en el bloque:** Analistas de segmento y AG-13 MOTOR: consulta de métodos de valoración cambiaria.
- **Limitaciones:** Confirmado solo por bibliografía.

#### FXA-0067 · Q 80 (A) — Are Our FEERs Justified?

- **Autores:** Giacomo Barisone; Rebecca L. Driver; Simon Wren-Lewis
- **Año:** 2006
- **Publicación o institución:** Journal of International Money and Finance, vol. 25, págs. 741-759
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-03 Tipo de cambio de equilibrio y valoración (PPA, BEER, FEER, REER) (principal) · secundarias: TX-13
- **Calidad Q:** 80 (A) — Tipo 24/25 · Rigor 16/20 · Autoridad 13/15 · Vigencia 7/10 · Impacto 7/10 · Independencia 10/10 · Acceso 3/10
- **DOI / URL:** https://www.piie.com/sites/default/files/publications/pb/pb07-4/benassy-by-schnatz.pdf (página índice: bibliografía de Schnatz 2007)
- **Acceso y licencia:** Peldaño 3 (Elsevier) · Licencia: Copyright Elsevier
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Clark MacDonald "Exchange Rates and Economic Fundamentals…" IMF Working Paper»; WebFetch: sí, bibliografía del PDF de Schnatz)
- **Contenido:** Contrasta si las desviaciones del tipo de cambio respecto a su FEER ayudan a explicar los movimientos posteriores del tipo de cambio, es decir, si el FEER tiene contenido empírico de atracción.
- **Uso en el bloque:** AG-11 CONTRA y AS-ESTR: evidencia sobre si el FEER sirve como ancla de reversión.
- **Limitaciones:** Confirmado solo por bibliografía; contenido según el título y su discusión por Schnatz.

#### FXA-0068 · Q 80 (A) — Towards the Estimation of Equilibrium Exchange Rates for Transition Economies: Methodological Issues and a Panel Cointegration Perspective

- **Autores:** Francisco Maeso-Fernández; Chiara Osbat; Bernd Schnatz
- **Año:** 2006
- **Publicación o institución:** Journal of Comparative Economics, vol. 34, págs. 499-517
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-03 Tipo de cambio de equilibrio y valoración (PPA, BEER, FEER, REER) (principal) · secundarias: TX-10
- **Calidad Q:** 80 (A) — Tipo 24/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 6/10 · Impacto 7/10 · Independencia 10/10 · Acceso 3/10
- **DOI / URL:** https://www.piie.com/sites/default/files/publications/pb/pb07-4/benassy-by-schnatz.pdf (página índice: bibliografía de Schnatz 2007)
- **Acceso y licencia:** Peldaño 3 (Elsevier; versión de trabajo BCE) · Licencia: Copyright Elsevier
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Clark MacDonald "Exchange Rates and Economic Fundamentals…" IMF Working Paper»; WebFetch: sí, bibliografía del PDF de Schnatz)
- **Contenido:** Propone estimar los coeficientes del BEER en un panel de economías maduras y aplicarlos a economías en transición (método en dos pasos), porque sus series cortas y en convergencia no permiten estimaciones fiables propias.
- **Uso en el bloque:** AS-EMEA (PLN, HUF, CZK, RON): valoración de divisas en convergencia con la zona del euro.
- **Limitaciones:** Confirmado solo por bibliografía.

#### FXA-0069 · Q 80 (A) — Equilibrium Exchange Rates in Transition Economies: Taking Stock of the Issues

- **Autores:** Balázs Égert; László Halpern; Ronald MacDonald
- **Año:** 2006
- **Publicación o institución:** Journal of Economic Surveys
- **Tipo de documento:** Artículo de revisión (survey) revisado por pares
- **Temática:** TX-03 Tipo de cambio de equilibrio y valoración (PPA, BEER, FEER, REER) (principal) · secundarias: TX-10
- **Calidad Q:** 80 (A) — Tipo 24/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 6/10 · Impacto 8/10 · Independencia 10/10 · Acceso 3/10
- **DOI / URL:** https://www.piie.com/sites/default/files/publications/pb/pb07-4/macdonald.pdf (página índice: bibliografía de MacDonald y Dias 2007)
- **Acceso y licencia:** Peldaño 3 (Wiley) · Licencia: Copyright Wiley
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Clark MacDonald "Exchange Rates and Economic Fundamentals…" IMF Working Paper»; WebFetch: sí, bibliografía del PDF de MacDonald y Dias; volumen y páginas no vistos)
- **Contenido:** Revisión de los problemas de estimar tipos de equilibrio en economías en transición de Europa central y del este: Balassa-Samuelson, infravaloración inicial, cambios estructurales y elección entre BEER, FEER y PPA ajustada.
- **Uso en el bloque:** AS-EMEA: marco de valoración para divisas de Europa central y del este.
- **Limitaciones:** Volumen y páginas no confirmados.

#### FXA-0053 · Q 80 (A) — The Usual Suspects? Productivity and Demand Shocks and Asia-Pacific Real Exchange Rates

- **Autores:** Menzie D. Chinn
- **Año:** 2000
- **Publicación o institución:** Review of International Economics, vol. 8, n.º 1, págs. 20-43
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-03 Tipo de cambio de equilibrio y valoración (PPA, BEER, FEER, REER) (principal) · secundarias: TX-10
- **Calidad Q:** 80 (A) — Tipo 23/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 6/10 · Impacto 6/10 · Independencia 10/10 · Acceso 6/10
- **DOI / URL:** https://ideas.repec.org/a/aea/jecper/v18y2004i4p135-158.html (página índice: referencias citadas por Taylor y Taylor 2004)
- **Acceso y licencia:** Peldaño 3 (Wiley; versión de trabajo abierta) · Licencia: Copyright Wiley
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Alan Taylor Mark Taylor 2004 "The Purchasing Power Parity Debate"…»; WebFetch: sí, lista de referencias de IDEAS)
- **Contenido:** Estima para economías de Asia-Pacífico la relación de largo plazo entre tipo de cambio real, productividad relativa (Balassa-Samuelson) y shocks de demanda (gasto público).
- **Uso en el bloque:** AS-EMAS: anclas de valoración para KRW, TWD, SGD, THB, MYR, IDR y PHP con ajuste por productividad.
- **Limitaciones:** Confirmado solo por índice; muestra anterior a 2000.

#### FXA-0073 · Q 79 (B) — Long-Run Determinants of the Real Exchange Rate: A Stock-Flow Perspective

- **Autores:** Hamid Faruqee
- **Año:** 1995
- **Publicación o institución:** IMF Staff Papers, vol. 42, págs. 80-107
- **Tipo de documento:** Artículo revisado por pares (revista del FMI)
- **Temática:** TX-03 Tipo de cambio de equilibrio y valoración (PPA, BEER, FEER, REER) (principal) · secundarias: TX-07
- **Calidad Q:** 79 (B) — Tipo 23/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 6/10 · Impacto 7/10 · Independencia 9/10 · Acceso 5/10
- **DOI / URL:** https://www.piie.com/sites/default/files/publications/pb/pb07-4/macdonald.pdf (página índice: bibliografía de MacDonald y Dias 2007; también citada por Schnatz 2007)
- **Acceso y licencia:** Peldaño 3 (Palgrave/JSTOR) · Licencia: Copyright FMI
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Clark MacDonald "Exchange Rates and Economic Fundamentals…" IMF Working Paper»; WebFetch: sí, bibliografías de MacDonald y Dias y de Schnatz)
- **Contenido:** Modelo de stock-flujo del tipo de cambio real de largo plazo: la posición exterior neta (stock) y los determinantes de la balanza comercial (productividad, términos de intercambio) fijan el equilibrio; aplicación a EE. UU. y Japón.
- **Uso en el bloque:** AS-G10N (USD, JPY): fundamento de BEER con activos exteriores netos.
- **Limitaciones:** Confirmado solo por bibliografía.

#### FXA-0072 · Q 78 (B) — Global Equilibrium Exchange Rates: Euro, Dollar, «Ins», «Outs», and Other Major Currencies in a Panel Cointegration Framework

- **Autores:** Enrique Alberola; Susana G. Cervero; Humberto López; Ángel Ubide
- **Año:** 1999
- **Publicación o institución:** Fondo Monetario Internacional, IMF Working Paper 99/175
- **Tipo de documento:** Documento de trabajo institucional
- **Temática:** TX-03 Tipo de cambio de equilibrio y valoración (PPA, BEER, FEER, REER) (principal) · secundarias: —
- **Calidad Q:** 78 (B) — Tipo 20/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 5/10 · Impacto 7/10 · Independencia 9/10 · Acceso 7/10
- **DOI / URL:** https://www.piie.com/sites/default/files/publications/pb/pb07-4/benassy-by-schnatz.pdf (página índice: bibliografía de Schnatz 2007)
- **Acceso y licencia:** Peldaño 2 (serie abierta del FMI) · Licencia: Copyright FMI
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Clark MacDonald "Exchange Rates and Economic Fundamentals…" IMF Working Paper»; WebFetch: sí, bibliografía del PDF de Schnatz)
- **Contenido:** Estima tipos de equilibrio para el euro, el dólar y otras divisas principales con cointegración de panel, combinando activos exteriores netos y productividad relativa; marco de equilibrio global (consistencia multilateral) desarrollado con autores del Banco de España.
- **Uso en el bloque:** AS-G10N: valoración del EUR y del USD con un marco multilateral coherente.
- **Limitaciones:** Confirmado solo por bibliografía; muestra anterior al euro.

#### FXA-0070 · Q 77 (B) — Filtering the BEER: A Permanent and Transitory Decomposition

- **Autores:** Peter B. Clark; Ronald MacDonald
- **Año:** 2000
- **Publicación o institución:** Fondo Monetario Internacional, IMF Working Paper 00/144 (también en Global Finance Journal)
- **Tipo de documento:** Documento de trabajo institucional
- **Temática:** TX-03 Tipo de cambio de equilibrio y valoración (PPA, BEER, FEER, REER) (principal) · secundarias: —
- **Calidad Q:** 77 (B) — Tipo 20/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 6/10 · Impacto 6/10 · Independencia 9/10 · Acceso 6/10
- **DOI / URL:** https://www.piie.com/sites/default/files/publications/pb/pb07-4/macdonald.pdf (página índice: bibliografía de MacDonald y Dias 2007)
- **Acceso y licencia:** Peldaño 2 (serie abierta del FMI) · Licencia: Copyright FMI
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Clark MacDonald "Exchange Rates and Economic Fundamentals…" IMF Working Paper»; WebFetch: sí, bibliografía del PDF de MacDonald y Dias)
- **Contenido:** Descompone el BEER en componentes permanente y transitorio (equilibrio permanente o PEER), para distinguir desalineamientos persistentes de fluctuaciones pasajeras de los fundamentales.
- **Uso en el bloque:** AS-ESTR y Analistas G10: separar el valor de equilibrio estructural del ciclo en tesis de valor.
- **Limitaciones:** Confirmado solo por bibliografía.

#### FXA-0065 · Q 76 (B) — A Macroeconomic Balance Framework for Estimating Equilibrium Exchange Rates

- **Autores:** Hamid Faruqee; Peter Isard; Paul R. Masson
- **Año:** 1998 (en R. MacDonald y J. Stein (eds.), Equilibrium Exchange Rates, cap. 4)
- **Publicación o institución:** Kluwer Academic Publishers, Boston
- **Tipo de documento:** Capítulo de libro (metodología del FMI)
- **Temática:** TX-03 Tipo de cambio de equilibrio y valoración (PPA, BEER, FEER, REER) (principal) · secundarias: TX-07
- **Calidad Q:** 76 (B) — Tipo 18/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 6/10 · Impacto 9/10 · Independencia 9/10 · Acceso 3/10
- **DOI / URL:** https://www.piie.com/sites/default/files/publications/pb/pb07-4/macdonald.pdf (página índice: bibliografía de MacDonald y Dias 2007)
- **Acceso y licencia:** Peldaño 3 (libro de pago) · Licencia: Copyright Kluwer/Springer
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Clark MacDonald "Exchange Rates and Economic Fundamentals…" IMF Working Paper»; WebFetch: sí, bibliografía del PDF de MacDonald y Dias)
- **Contenido:** Enfoque de «balance macroeconómico» del FMI (antecesor de CGER y EBA): compara el saldo por cuenta corriente subyacente con una norma de ahorro-inversión y traduce la brecha en desalineamiento del tipo de cambio real mediante elasticidades comerciales.
- **Uso en el bloque:** Analistas de segmento: origen metodológico de las evaluaciones externas del FMI que se citan en los informes del Artículo IV.
- **Limitaciones:** Confirmado solo por bibliografía.

#### FXA-0063 · Q 75 (B) — Behavioural Equilibrium Exchange Rate Estimates and Implied Exchange Rate Adjustments for Ten Countries

- **Autores:** Ronald MacDonald; Preethike Dias
- **Año:** 2007
- **Publicación o institución:** Peterson Institute for International Economics — taller sobre desequilibrios globales (Washington DC, febrero de 2007)
- **Tipo de documento:** Ponencia técnica con metodología
- **Temática:** TX-03 Tipo de cambio de equilibrio y valoración (PPA, BEER, FEER, REER) (principal) · secundarias: TX-07, TX-10
- **Calidad Q:** 75 (B) — Tipo 15/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 6/10 · Impacto 5/10 · Independencia 9/10 · Acceso 10/10
- **DOI / URL:** https://www.piie.com/sites/default/files/publications/pb/pb07-4/macdonald.pdf
- **Acceso y licencia:** Peldaño 1 (PDF abierto en PIIE) · Licencia: Copyright PIIE/autores
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Clark MacDonald "Exchange Rates and Economic Fundamentals…" IMF Working Paper»; WebFetch: sí)
- **Contenido:** Estima BEER para los tipos efectivos de diez economías clave de los desequilibrios globales (1988-2006) con diferencial de tipos reales, términos de intercambio, PIB per cápita y exportaciones netas (Johansen y DOLS de panel), y deriva los ajustes cambiarios necesarios (27-47 % para el renminbi).
- **Uso en el bloque:** AS-EMAS (CNY) y AS-G10N: ejemplo aplicado de BEER con variables estándar y de traducción a «ajuste necesario».
- **Limitaciones:** Estimaciones de 2007, desfasadas; incertidumbre alta en economías en transición.

## TX-04 Carry, prima de riesgo cambiaria y paridad descubierta

#### ANA-DOC-0756 · Q 92 (A) — Carry

- **Autores:** Ralph S. J. Koijen; Tobias J. Moskowitz; Lasse Heje Pedersen; Evert B. Vrugt
- **Año:** 2018 (NBER WP 19325, 2013)
- **Publicación o institución:** Journal of Financial Economics, vol. 127, n.º 2, págs. 197-225 · NBER Working Paper 19325
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-04 Carry, prima de riesgo cambiaria y paridad descubierta (principal) · secundarias: TX-05
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 7/10 · Acceso 9/10
- **DOI / URL:** https://ideas.repec.org/e/pvr15.html · NBER: https://www.nber.org/papers/w19325
- **Acceso y licencia:** Peldaño 1 (documento de trabajo NBER) · Licencia: copyright Elsevier / autores
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Koijen Moskowitz Pedersen Vrugt "Carry" Journal of Financial Economics 2018»; WebFetch: sí, perfil RePEc de E. B. Vrugt) · reutilizada del F7 V3.2 (TA-23)
- **Contenido:** Define el «carry» de forma general (rentabilidad esperada si los precios no cambian; en divisas, el diferencial de tipos o puntos forward) y muestra que predice rentabilidades en divisas y en otras siete clases de activo; el carry cambiario es un caso particular de una prima transversal.
- **Uso en el bloque:** AS-ESTR y AG-13 MOTOR (perfil PERF-FX-FACT): definición operativa del carry cambiario y comparación con el carry de otros activos; diversificación de carteras carry.
- **Limitaciones:** Coautores vinculados a gestoras cuantitativas (AQR) que comercializan estrategias de carry (Independencia 7/10); riesgo de cola de las estrategias carry.

#### ANA-DOC-0305 · Q 92 (A) — Carry Trades and Global Foreign Exchange Volatility

- **Autores:** Lukas Menkhoff; Lucio Sarno; Maik Schmeling; Andreas Schrimpf
- **Año:** 2012
- **Publicación o institución:** The Journal of Finance, vol. 67, n.º 2, págs. 681-718
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-04 Carry, prima de riesgo cambiaria y paridad descubierta (principal) · secundarias: TX-05, TX-09
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 7/10
- **DOI / URL:** DOI 10.1111/j.1540-6261.2012.01728.x · https://openaccess.city.ac.uk/id/eprint/3391/
- **Acceso y licencia:** Peldaño 2 (versión aceptada en City Research Online) · Licencia: Copyright Wiley/AFA; versión de autor de lectura libre
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Menkhoff Sarno Schmeling Schrimpf "Carry Trades and Global Foreign Exchange Volatility" Journal of Finance 2012»; WebFetch: sí) · reutilizada del F7 V3.2 (TA-07)
- **Contenido:** Los rendimientos del carry trade son una compensación por el riesgo de volatilidad cambiaria global: las divisas de alto tipo rinden mal cuando la volatilidad FX sube inesperadamente; el factor de volatilidad explica más del 90 % de la variación transversal de las carteras carry.
- **Uso en el bloque:** AS-ESTR y TR-PFV: la volatilidad FX global como variable de estado del carry (desmontar posiciones cuando sube); AG-11 CONTRA: fragilidad del carry.
- **Limitaciones:** Muestra hasta 2009.

#### FXA-0088 · Q 92 (A) — The Cross Section of Foreign Currency Risk Premia and Consumption Growth Risk

- **Autores:** Hanno Lustig; Adrien Verdelhan
- **Año:** 2007 (NBER WP 11104, 2005, rev. 2006)
- **Publicación o institución:** American Economic Review, vol. 97, n.º 1, págs. 89-117
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-04 Carry, prima de riesgo cambiaria y paridad descubierta (principal) · secundarias: TX-05
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** DOI WP 10.3386/w11104 · https://nber.org/papers/w11104
- **Acceso y licencia:** Peldaño 2 (WP del NBER; artículo AEA) · Licencia: Copyright AEA
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Hanno Lustig Adrien Verdelhan "The Cross Section of Foreign Currency Risk Premia and Consumption Growth Risk" "Countercyclical Currency Risk Premia"»; WebFetch: sí, página del NBER con la versión publicada)
- **Contenido:** Introduce las carteras de divisas ordenadas por diferencial de tipos: las divisas de tipo bajo se aprecian cuando el consumo de EE. UU. crece poco (cobertura) y las de tipo alto se deprecian, por lo que el CAPM de consumo explica el exceso de rentabilidad del carry.
- **Uso en el bloque:** AS-ESTR y AG-13 MOTOR: metodología de carteras ordenadas por carry y explicación de riesgo de la prima; AG-11 CONTRA: el carry rinde mal en recesiones.
- **Limitaciones:** Resultados discutidos por Burnside (2007) y contestados por los autores (FXA-0089).

#### ANA-DOC-0307 · Q 90 (A) — Deviations from Covered Interest Rate Parity

- **Autores:** Wenxin Du; Alexander Tepper; Adrien Verdelhan
- **Año:** 2018
- **Publicación o institución:** The Journal of Finance, vol. 73, n.º 3, págs. 915-957
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-04 Carry, prima de riesgo cambiaria y paridad descubierta (principal) · secundarias: TX-06, TX-12
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 4/10
- **DOI / URL:** DOI 10.1111/jofi.12620 · https://dspace.mit.edu/handle/1721.1/128481 · versión de trabajo: https://www.nber.org/papers/w23170
- **Acceso y licencia:** Peldaño 2 (registro abierto en DSpace@MIT y NBER WP 23170) · Licencia: Copyright Wiley/AFA
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Du Tepper Verdelhan "Deviations from Covered Interest Rate Parity" Journal of Finance 2018»; WebFetch: sí) · reutilizada del F7 V3.2 (TA-07)
- **Contenido:** Documenta desviaciones persistentes de la paridad cubierta de intereses (base cruzada de divisas) en las divisas del G10 desde 2008, explicadas por restricciones de balance bancario (efectos de cierre trimestral) y desequilibrios de demanda de inversión internacional.
- **Uso en el bloque:** TR-PFV: interpretación de la base cruzada como indicador de tensión en la financiación en dólares y del coste de cobertura; AS-G10N: carry cubierto frente a descubierto (JPY, EUR, CHF).
- **Limitaciones:** Las magnitudes de la base han variado desde la publicación.

#### FXA-0007 · Q 90 (A) — Forward and spot exchange rates

- **Autores:** Eugene F. Fama
- **Año:** 1984
- **Publicación o institución:** Journal of Monetary Economics, vol. 14, n.º 3, págs. 319-338
- **Tipo de documento:** Artículo revisado por pares (canónico)
- **Temática:** TX-04 Carry, prima de riesgo cambiaria y paridad descubierta (principal) · secundarias: TX-13
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** DOI 10.1016/0304-3932(84)90046-1 · https://en.wikipedia.org/wiki/Forward_premium_anomaly (página índice)
- **Acceso y licencia:** Peldaño 3 (Elsevier, de pago) · Licencia: Copyright Elsevier
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Fama 1984 "Forward and spot exchange rates" Journal of Monetary Economics forward premium puzzle»; WebFetch: sí, página índice https://en.wikipedia.org/wiki/Forward_premium_anomaly con DOI)
- **Contenido:** Regresión canónica del cambio del contado sobre la prima forward: el coeficiente es negativo (no 1), por lo que el forward es un predictor sesgado; atribuye la anomalía a una prima de riesgo variable más volátil que la depreciación esperada («enigma de Fama»).
- **Uso en el bloque:** AS-ESTR y AG-10 PROS: fundamento del carry (la divisa de tipo alto no se deprecia lo que descuenta el forward) y de usar el forward como referencia de comparación (Documento 0, 8.4).
- **Limitaciones:** Muestra de los setenta y ochenta; el coeficiente ha cambiado de signo en periodos recientes (véase FXA-0008).

#### ANA-DOC-0364 · Q 89 (A) — Currency Premia and Global Imbalances

- **Autores:** Pasquale Della Corte; Steven J. Riddiough; Lucio Sarno
- **Año:** 2016
- **Publicación o institución:** Review of Financial Studies, vol. 29, n.º 8, págs. 2161-2193 (CEPR DP 11129)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-04 Carry, prima de riesgo cambiaria y paridad descubierta (principal) · secundarias: TX-05, TX-07
- **Calidad Q:** 89 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** https://econpapers.repec.org/RePEc:cpr:ceprdp:11129 · versión abierta: https://openaccess.city.ac.uk/id/eprint/13287/1/FX_NFA_full.pdf
- **Acceso y licencia:** Peldaño 2 (versión de autor en City Research Online) · Licencia: Copyright OUP
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Lucio Sarno IDEAS RePEc publications currency premia global imbalances»; WebFetch: sí) · reutilizada del F7 V3.2 (TA-07)
- **Contenido:** Factor de riesgo de «desequilibrios globales»: las divisas de deudores netos con pasivos en moneda extranjera pagan prima porque se deprecian en malos tiempos; el factor explica la sección cruzada de rentabilidades cambiarias, incluido el carry.
- **Uso en el bloque:** AS-ESTR y Analistas EM: posición exterior neta como determinante de la prima cambiaria y del riesgo del carry; AG-11 CONTRA.
- **Limitaciones:** Revista confirmada vía enlace RePEc de la versión publicada.

#### FXA-0009 · Q 89 (A) — Do Peso Problems Explain the Returns to the Carry Trade?

- **Autores:** Craig Burnside; Martin Eichenbaum; Isaac Kleshchelski; Sergio Rebelo
- **Año:** 2011 (NBER WP 14054 de 2008)
- **Publicación o institución:** Review of Financial Studies, vol. 24, págs. 853-891
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-04 Carry, prima de riesgo cambiaria y paridad descubierta (principal) · secundarias: TX-09
- **Calidad Q:** 89 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 3/10
- **DOI / URL:** https://img.nber.org/papers/w14054 (WP del NBER) · página índice: https://cefup-nipe-rank.eeg.uminho.pt/people/1535/articles
- **Acceso y licencia:** Peldaño 2 (WP del NBER; copia en DukeSpace) · Licencia: Copyright OUP/autores
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Burnside Eichenbaum Kleshchelski Rebelo "Do Peso Problems Explain the Returns to the Carry Trade?" Review of Financial Studies»; WebFetch: sí, página índice de CEF.UP con revista, volumen y páginas)
- **Contenido:** Usando carteras carry cubiertas con opciones, atribuye la rentabilidad del carry a un «problema del peso»: no a crashes observados, sino a la prima que exige el inversor por estados malos raros en los que el factor de descuento estocástico es muy alto.
- **Uso en el bloque:** AS-ESTR y AG-11 CONTRA: por qué el carry parece rentable en muestra y qué coste tiene cubrir su cola; base para comparar carry cubierto con opciones (risk reversals de TR-PFV).
- **Limitaciones:** Muestra hasta 2008; resultados sensibles al precio de las opciones utilizadas.

#### ANA-DOC-0306 · Q 89 (A) — Carry Trades and Currency Crashes

- **Autores:** Markus K. Brunnermeier; Stefan Nagel; Lasse H. Pedersen
- **Año:** 2009 (NBER Macroeconomics Annual 2008, vol. 23; NBER WP 14473 de 2008)
- **Publicación o institución:** NBER Macroeconomics Annual 2008, vol. 23 (University of Chicago Press / NBER)
- **Tipo de documento:** Capítulo revisado en anuario académico
- **Temática:** TX-04 Carry, prima de riesgo cambiaria y paridad descubierta (principal) · secundarias: TX-09
- **Calidad Q:** 89 (A) — Tipo 22/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 7/10
- **DOI / URL:** DOI 10.3386/w14473 · https://www.nber.org/papers/w14473
- **Acceso y licencia:** Peldaño 1-2 (WP del NBER; copia en Princeton) · Licencia: Copyright NBER/autores
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Brunnermeier Nagel Pedersen "Carry Trades and Currency Crashes" NBER Macroeconomics Annual 2008»; WebFetch: sí) · reutilizada del F7 V3.2 (TA-07)
- **Contenido:** El carry trade tiene riesgo de crash (asimetría negativa) por el deshacer súbito de posiciones cuando cae el apetito por el riesgo o se endurece la liquidez de financiación; el diferencial de tipos predice asimetría negativa y la liquidez de financiación predice movimientos cambiarios.
- **Uso en el bloque:** AS-ESTR, AS-G10M (AUD/JPY, NZD/JPY) y AG-11 CONTRA: señal de fragilidad cuando el posicionamiento carry (TR-PFV) y la volatilidad baja coinciden.
- **Limitaciones:** Datos hasta 2008.

#### FXA-0105 · Q 89 (A) — The Forward Discount Anomaly and the Risk Premium: A Survey of Recent Evidence

- **Autores:** Charles Engel
- **Año:** 1996
- **Publicación o institución:** Journal of Empirical Finance, vol. 3, n.º 2, págs. 123-192
- **Tipo de documento:** Artículo de revisión (survey) revisado por pares
- **Temática:** TX-04 Carry, prima de riesgo cambiaria y paridad descubierta (principal) · secundarias: —
- **Calidad Q:** 89 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** https://www.nber.org/papers/w16942.pdf (página índice: bibliografía de Burnside, Eichenbaum y Rebelo 2011)
- **Acceso y licencia:** Peldaño 3 (Elsevier; versión NBER de trabajo) · Licencia: Copyright Elsevier
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Burnside Eichenbaum Rebelo "Carry Trade and Momentum in Currency Markets"…»; WebFetch: sí, bibliografía del PDF del NBER con revista, volumen y páginas)
- **Contenido:** Revisión clásica de la anomalía del descuento forward: documenta su robustez y muestra que los modelos de prima de riesgo (CAPM, consumo, GARCH-M) no logran explicar su magnitud ni su volatilidad.
- **Uso en el bloque:** AS-ESTR y AG-14 DOC-A: referencia obligada sobre el rechazo de la UIP y las explicaciones de prima de riesgo.
- **Limitaciones:** Confirmado solo por bibliografía; literatura hasta 1995.

#### FXA-0078 · Q 87 (A) — Currency Risk Factors in a Recursive Multicountry Economy

- **Autores:** Ric Colacito; Mariano M. Croce; Federico Gavazzoni; Robert Ready
- **Año:** 2018
- **Publicación o institución:** The Journal of Finance, vol. 73, n.º 6, págs. 2719-2756
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-04 Carry, prima de riesgo cambiaria y paridad descubierta (principal) · secundarias: TX-05, TX-01
- **Calidad Q:** 87 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 6/10 · Independencia 10/10 · Acceso 4/10
- **DOI / URL:** DOI 10.1111/jofi.12720 · https://ideas.repec.org/a/bla/jfinan/v73y2018i6p2719-2756.html
- **Acceso y licencia:** Peldaño 3 (Wiley/AFA) · Licencia: Copyright Wiley/AFA
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Pasquale Della Corte IDEAS RePEc author currency factors dollar risk»; WebFetch: sí)
- **Contenido:** Las diez divisas más negociadas difieren en la sensibilidad de sus economías a noticias de crecimiento global de largo plazo; un modelo multipaís con preferencias recursivas y esas diferencias de exposición reproduce las estrategias carry HML-FX (Lustig et al.) y HML-NFA (Della Corte et al.).
- **Uso en el bloque:** AS-ESTR y AS-G10M: fundamento teórico de por qué las divisas cíclicas (AUD, NZD, NOK) pagan prima de carry frente a JPY y CHF.
- **Limitaciones:** Modelo sin fricciones; calibración a G10.

#### FXA-0015 · Q 87 (A) — Properties of foreign exchange risk premiums

- **Autores:** Lucio Sarno; Paul Schneider; Christian Wagner
- **Año:** 2012
- **Publicación o institución:** Journal of Financial Economics, vol. 105, n.º 2, págs. 279-310
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-04 Carry, prima de riesgo cambiaria y paridad descubierta (principal) · secundarias: TX-13
- **Calidad Q:** 87 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 14/15 · Vigencia 8/10 · Impacto 7/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** DOI 10.1016/j.jfineco.2012.01.005 · https://openaccess.city.ac.uk/id/eprint/3297/
- **Acceso y licencia:** Peldaño 2 (versión de autor en City Research Online) · Licencia: Copyright Elsevier
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Menkhoff Sarno Schmeling Schrimpf "Currency Value" Review of Financial Studies 2017»; WebFetch: sí, página índice https://openaccess.city.ac.uk/view/creators/Sarno=3AL=2E=3A=3A.html)
- **Contenido:** Estima con modelos afines de estructura temporal las primas de riesgo cambiarias implícitas en tipos y tipos de cambio: las primas son variables, a veces de signo cambiante, y su componente estimado explica la violación de la UIP aunque la mejora predictiva fuera de muestra es limitada.
- **Uso en el bloque:** AS-ESTR y AG-10 PROS: descomponer el forward en depreciación esperada y prima de riesgo; fundamento de la valoración «cuánto descuenta el forward» (Documento 0, 8.1 paso 5).
- **Limitaciones:** Modelos de alta exigencia técnica; resultados dependientes de la especificación.

#### FXA-0091 · Q 87 (A) — Forward Exchange Rates as Optimal Predictors of Future Spot Rates: An Econometric Analysis

- **Autores:** Lars Peter Hansen; Robert J. Hodrick
- **Año:** 1980
- **Publicación o institución:** Journal of Political Economy, vol. 88, págs. 829-853
- **Tipo de documento:** Artículo revisado por pares (canónico)
- **Temática:** TX-04 Carry, prima de riesgo cambiaria y paridad descubierta (principal) · secundarias: TX-13
- **Calidad Q:** 87 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 6/10 · Impacto 10/10 · Independencia 10/10 · Acceso 3/10
- **DOI / URL:** https://www.nber.org/papers/w13812.pdf (página índice: bibliografía de Lustig y Verdelhan 2010)
- **Acceso y licencia:** Peldaño 3 (UCP) · Licencia: Copyright UCP
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Hanno Lustig Adrien Verdelhan "The Cross Section of Foreign Currency Risk Premia…"»; WebFetch: sí, bibliografía del PDF del NBER)
- **Contenido:** Contrasta si el tipo forward es el predictor óptimo del contado futuro con una metodología econométrica para errores solapados (origen de los errores estándar de Hansen-Hodrick) y rechaza la hipótesis de eficiencia simple para varias divisas.
- **Uso en el bloque:** AG-10 PROS y AG-20 EVAL: fundamento de usar el forward como referencia y de corregir el solapamiento al evaluar pronósticos a varios horizontes.
- **Limitaciones:** Confirmado solo por bibliografía; muestra de los setenta.

#### FXA-0006 · Q 86 (A) — The Real Exchange Rate, Real Interest Rates, and the Risk Premium

- **Autores:** Charles Engel
- **Año:** 2011 (NBER WP 17116; IHS Economics Series 265; publicado después como «Exchange Rates, Interest Rates, and the Risk Premium», American Economic Review, 2016)
- **Publicación o institución:** Institute for Advanced Studies (IHS), Economics Series 265 · NBER Working Paper 17116 · HKIMR WP 27/2011
- **Tipo de documento:** Documento de trabajo institucional
- **Temática:** TX-04 Carry, prima de riesgo cambiaria y paridad descubierta (principal) · secundarias: TX-01, TX-03
- **Calidad Q:** 86 (A) — Tipo 20/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 10/10 · Acceso 6/10
- **DOI / URL:** https://ideas.repec.org:443/p/ihs/ihsesp/265.html · texto completo: https://irihs.ihs.ac.at/id/eprint/2050
- **Acceso y licencia:** Peldaño 1 (texto completo en el repositorio del IHS) · Licencia: Copyright del autor
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Charles Engel IDEAS RePEc author page exchange rates»; WebFetch: sí). La versión AER 2016 no se ha visto en esta carga.
- **Contenido:** Documenta dos hechos difíciles de conciliar: las divisas de tipo alto tienen mayor rentabilidad esperada a corto plazo (enigma UIP), pero los países con tipos reales altos tienen divisas fuertes, más de lo que implicaría la UIP; la prima de riesgo cambiaria cambia de signo con el horizonte y los modelos existentes no reproducen ambos hechos.
- **Uso en el bloque:** AS-ESTR y Analistas G10: separar la ganancia de carry a corto plazo de la reversión del nivel a largo plazo; AG-10 PROS: horizonte de las tesis de carry.
- **Limitaciones:** Versión de trabajo; consultar la versión publicada (AER 2016) para las cifras finales.

#### FXA-0037 · Q 86 (A) — Exchange Rate Puzzles and Distorted Beliefs

- **Autores:** Pierre-Olivier Gourinchas; Aaron Tornell
- **Año:** 2004
- **Publicación o institución:** Journal of International Economics, vol. 64, págs. 303-333
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-04 Carry, prima de riesgo cambiaria y paridad descubierta (principal) · secundarias: TX-02, TX-01
- **Calidad Q:** 86 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 8/10 · Independencia 10/10 · Acceso 4/10
- **DOI / URL:** https://www.uh.edu/~dpapell/Taylor%20Rule%20Fundamentals.pdf (página índice: bibliografía de Molodtsova y Papell)
- **Acceso y licencia:** Peldaño 3 (Elsevier) · Licencia: Copyright Elsevier
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Taylor rule fundamentals exchange rate predictability Molodtsova Papell…»; WebFetch: sí, bibliografía del PDF de Molodtsova y Papell)
- **Contenido:** Explica el enigma de la prima forward y la sobrerreacción retardada sin prima de riesgo: los inversores perciben mal la persistencia de los shocks de tipos de interés (creencias distorsionadas), lo que genera infrarreacción inicial y rentabilidades predecibles del carry.
- **Uso en el bloque:** AS-ESTR y TR-BCM: explicación conductual del carry tras cambios de ciclo monetario; ventana de oportunidad tras sorpresas persistentes de tipos.
- **Limitaciones:** Confirmado solo por bibliografía.

#### FXA-0090 · Q 86 (A) — Affine Models of Currency Pricing: Accounting for the Forward Premium Anomaly

- **Autores:** David Backus; Silverio Foresi; Chris Telmer
- **Año:** 2001
- **Publicación o institución:** Journal of Finance, vol. 56, págs. 279-304
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-04 Carry, prima de riesgo cambiaria y paridad descubierta (principal) · secundarias: —
- **Calidad Q:** 86 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 14/15 · Vigencia 7/10 · Impacto 9/10 · Independencia 10/10 · Acceso 3/10
- **DOI / URL:** https://www.nber.org/papers/w13812.pdf (página índice: bibliografía de Lustig y Verdelhan 2010)
- **Acceso y licencia:** Peldaño 3 (Wiley/AFA) · Licencia: Copyright Wiley/AFA
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Hanno Lustig Adrien Verdelhan "The Cross Section of Foreign Currency Risk Premia…"»; WebFetch: sí, bibliografía del PDF del NBER con revista, volumen y páginas)
- **Contenido:** Deriva las condiciones que deben cumplir los factores de descuento de dos países para generar la anomalía de la prima forward en modelos afines de estructura temporal, y muestra la dificultad de reproducirla con modelos estándar.
- **Uso en el bloque:** AS-ESTR y AG-13 MOTOR (vía F8): marco formal para relacionar curvas de tipos y prima de riesgo cambiaria.
- **Limitaciones:** Confirmado solo por bibliografía; técnico.

#### FXA-0008 · Q 85 (A) — The New Fama Puzzle

- **Autores:** Matthieu Bussière; Menzie D. Chinn; Laurent Ferrara; Jonas Heipertz
- **Año:** 2022 (NBER WP 24342, 2018, rev. 2022)
- **Publicación o institución:** IMF Economic Review, vol. 70, n.º 3, págs. 451-486 · NBER Working Paper 24342
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-04 Carry, prima de riesgo cambiaria y paridad descubierta (principal) · secundarias: TX-13
- **Calidad Q:** 85 (A) — Tipo 24/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 5/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** DOI 10.1057/s41308-022-00161-z · DOI WP 10.3386/w24342 · https://www.nber.org/papers/w24342
- **Acceso y licencia:** Peldaño 2 (WP del NBER; artículo de pago) · Licencia: Copyright FMI/Palgrave
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Fama 1984 "Forward and spot exchange rates" Journal of Monetary Economics forward premium puzzle»; WebFetch: sí)
- **Contenido:** Para ocho tipos de cambio frente al dólar, el rechazo de la UIP desaparece durante y después de la crisis financiera: el coeficiente de Fama se vuelve grande y positivo («nuevo enigma de Fama»); las expectativas de encuestas apoyan más la UIP y el cambio se debe a la covarianza entre errores de expectativa y diferenciales.
- **Uso en el bloque:** AS-ESTR y AG-11 CONTRA: la relación carry-depreciación no es estable entre regímenes; revisar el supuesto de prima de carry tras 2008.
- **Limitaciones:** Ocho divisas frente al USD; periodo poscrisis con tipos cerca de cero.

#### FXA-0093 · Q 85 (A) — Puzzles in International Financial Markets

- **Autores:** Karen K. Lewis
- **Año:** 1995
- **Publicación o institución:** En G. Grossman y K. Rogoff (eds.), Handbook of International Economics, vol. 3, págs. 1913-1971 (Elsevier)
- **Tipo de documento:** Capítulo de manual de referencia
- **Temática:** TX-04 Carry, prima de riesgo cambiaria y paridad descubierta (principal) · secundarias: TX-01
- **Calidad Q:** 85 (A) — Tipo 20/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / URL:** https://www.nber.org/papers/w13812.pdf (página índice: bibliografía de Lustig y Verdelhan 2010)
- **Acceso y licencia:** Peldaño 3 (Elsevier; versión NBER de trabajo) · Licencia: Copyright Elsevier
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Hanno Lustig Adrien Verdelhan "The Cross Section of Foreign Currency Risk Premia…"»; WebFetch: sí, bibliografía del PDF del NBER)
- **Contenido:** Revisión de manual de dos enigmas: la prima forward (prima de riesgo, aprendizaje, problemas del peso, sesgos de expectativas) y el sesgo doméstico en carteras.
- **Uso en el bloque:** AS-ESTR y AG-14 DOC-A: catálogo de explicaciones del rechazo de la UIP.
- **Limitaciones:** Literatura hasta 1994.

#### FXA-0080 · Q 84 (A) — A credit-based theory of the currency risk premium

- **Autores:** Pasquale Della Corte; Alexandre Jeanneret; Ella D. S. Patelli
- **Año:** 2023
- **Publicación o institución:** Journal of Financial Economics, vol. 149, n.º 3, págs. 473-496
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-04 Carry, prima de riesgo cambiaria y paridad descubierta (principal) · secundarias: TX-10, TX-09
- **Calidad Q:** 84 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 5/10 · Independencia 10/10 · Acceso 3/10
- **DOI / URL:** https://ideas.repec.org/f/c/pde393.html (página índice de citas del autor en IDEAS; ficha: ideas.repec.org/a/eee/jfinec/v149y2023i3p473-496.html)
- **Acceso y licencia:** Peldaño 3 (Elsevier) · Licencia: Copyright Elsevier
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Pasquale Della Corte IDEAS RePEc author currency factors dollar risk»; WebFetch: sí, página índice https://ideas.repec.org/f/c/pde393.html)
- **Contenido:** Teoría de la prima de riesgo cambiaria basada en el riesgo de crédito (soberano) del país: las divisas de países con mayor riesgo de impago exigen prima y se deprecian cuando aumenta el riesgo de crédito global.
- **Uso en el bloque:** Analistas EM (AS-EMLA, AS-EMEA): vincular CDS soberanos, carry y riesgo de depreciación en divisas de alto rendimiento.
- **Limitaciones:** Confirmado solo por índice; contenido inferido del título y de la línea de investigación del autor (véase FXA-0013), a cotejar.

#### FXA-0016 · Q 84 (A) — Foreign exchange risk and the predictability of carry trade returns

- **Autores:** Gino Cenedese; Lucio Sarno; Ilias Tsiakas
- **Año:** 2014
- **Publicación o institución:** Journal of Banking & Finance, vol. 42, n.º 1, págs. 302-313
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-04 Carry, prima de riesgo cambiaria y paridad descubierta (principal) · secundarias: TX-09
- **Calidad Q:** 84 (A) — Tipo 24/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 5/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** DOI 10.1016/j.jbankfin.2014.01.040 · https://openaccess.city.ac.uk/id/eprint/13159/
- **Acceso y licencia:** Peldaño 2 (versión de autor en City Research Online) · Licencia: Copyright Elsevier
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Menkhoff Sarno Schmeling Schrimpf "Currency Value" Review of Financial Studies 2017»; WebFetch: sí, página índice de City Research Online)
- **Contenido:** Muestra que aumentos de la varianza del mercado cambiario (y no de las correlaciones) predicen pérdidas futuras del carry trade; la descomposición del riesgo cambiario agregado ayuda a anticipar episodios de desmontaje.
- **Uso en el bloque:** AS-ESTR y TR-PFV: indicador de régimen (varianza FX agregada) para reducir el carry; AG-11 CONTRA.
- **Limitaciones:** Predicción en muestra más fuerte que fuera de muestra.

#### FXA-0096 · Q 84 (A) — Understanding the Forward Premium Puzzle: A Microstructure Approach

- **Autores:** Craig Burnside; Martin Eichenbaum; Sergio Rebelo
- **Año:** 2009
- **Publicación o institución:** American Economic Journal: Macroeconomics, vol. 1, n.º 2, págs. 127-154
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-04 Carry, prima de riesgo cambiaria y paridad descubierta (principal) · secundarias: TX-06
- **Calidad Q:** 84 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 8/10 · Independencia 10/10 · Acceso 3/10
- **DOI / URL:** https://www.nber.org/papers/w13812.pdf (página índice: bibliografía de Lustig y Verdelhan 2010)
- **Acceso y licencia:** Peldaño 3 (AEA) · Licencia: Copyright AEA
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Hanno Lustig Adrien Verdelhan "The Cross Section of Foreign Currency Risk Premia…"»; WebFetch: sí, bibliografía del PDF del NBER)
- **Contenido:** Explica el enigma de la prima forward con un modelo de microestructura con selección adversa entre creadores de mercado e inversores con información ruidosa, sin recurrir a primas de riesgo.
- **Uso en el bloque:** AS-ESTR y TR-PFV: explicación alternativa (informacional) del carry; puente con TX-06.
- **Limitaciones:** Confirmado solo por bibliografía.

#### FXA-0017 · Q 82 (A) — Global liquidity risk in the foreign exchange market

- **Autores:** Chiara Banti; Kate Phylaktis; Lucio Sarno
- **Año:** 2012
- **Publicación o institución:** Journal of International Money and Finance, vol. 31, n.º 2, págs. 267-291
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-04 Carry, prima de riesgo cambiaria y paridad descubierta (principal) · secundarias: TX-06
- **Calidad Q:** 82 (A) — Tipo 24/25 · Rigor 17/20 · Autoridad 13/15 · Vigencia 8/10 · Impacto 5/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** DOI 10.1016/j.jimonfin.2011.11.010 · https://openaccess.city.ac.uk/id/eprint/13160/
- **Acceso y licencia:** Peldaño 2 (versión de autor en City Research Online) · Licencia: Copyright Elsevier
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Menkhoff Sarno Schmeling Schrimpf "Currency Value" Review of Financial Studies 2017»; WebFetch: sí, página índice de City Research Online)
- **Contenido:** Construye una medida de liquidez global del mercado cambiario a partir del flujo de órdenes y muestra que el riesgo de liquidez está valorado: las divisas más expuestas a caídas de liquidez global pagan una prima.
- **Uso en el bloque:** TR-PFV y AS-ESTR: liquidez cambiaria como componente de la prima de riesgo (relevante para G10M —NOK, SEK— y EM).
- **Limitaciones:** Datos de flujo de órdenes de un proveedor concreto y periodo limitado.

#### FXA-0095 · Q 82 (A) — Carry Trade: The Gains of Diversification

- **Autores:** Craig Burnside; Martin Eichenbaum; Sergio Rebelo
- **Año:** 2008
- **Publicación o institución:** Journal of the European Economic Association, vol. 6, n.º 2, págs. 581-588
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-04 Carry, prima de riesgo cambiaria y paridad descubierta (principal) · secundarias: TX-05
- **Calidad Q:** 82 (A) — Tipo 24/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 8/10 · Independencia 10/10 · Acceso 3/10
- **DOI / URL:** https://www.nber.org/papers/w13812.pdf (página índice: bibliografía de Lustig y Verdelhan 2010)
- **Acceso y licencia:** Peldaño 3 (Wiley/EEA) · Licencia: Copyright EEA
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Hanno Lustig Adrien Verdelhan "The Cross Section of Foreign Currency Risk Premia…"»; WebFetch: sí, bibliografía del PDF del NBER)
- **Contenido:** Una cartera diversificada de posiciones carry en muchas divisas tiene un ratio de Sharpe muy superior al de los pares individuales, porque la diversificación elimina buena parte del riesgo idiosincrásico.
- **Uso en el bloque:** AS-ESTR: diseño de cestas carry (ESTR) frente a apuestas carry de un solo par.
- **Limitaciones:** Confirmado solo por bibliografía; la diversificación cae en crisis.

#### FXA-0094 · Q 82 (A) — The Returns to Currency Speculation in Emerging Markets

- **Autores:** Craig Burnside; Martin Eichenbaum; Sergio Rebelo
- **Año:** 2007
- **Publicación o institución:** American Economic Review Papers and Proceedings, vol. 97, n.º 2, págs. 333-338
- **Tipo de documento:** Artículo (actas revisadas)
- **Temática:** TX-04 Carry, prima de riesgo cambiaria y paridad descubierta (principal) · secundarias: TX-10
- **Calidad Q:** 82 (A) — Tipo 22/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 8/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** https://www.nber.org/papers/w13812.pdf (página índice: bibliografía de Lustig y Verdelhan 2010)
- **Acceso y licencia:** Peldaño 3 (AEA) · Licencia: Copyright AEA
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Hanno Lustig Adrien Verdelhan "The Cross Section of Foreign Currency Risk Premia…"»; WebFetch: sí, bibliografía del PDF del NBER)
- **Contenido:** Mide la rentabilidad del carry en divisas emergentes teniendo en cuenta diferenciales compra-venta: es comparable a la de las divisas avanzadas y poco correlacionada con ella, lo que aporta diversificación.
- **Uso en el bloque:** Analistas EM (AS-EMLA, AS-EMEA, AS-EMAS) y AS-ESTR: carry EM neto de costes y su aportación a cestas.
- **Limitaciones:** Confirmado solo por bibliografía; muestra anterior a 2007.

#### FXA-0040 · Q 82 (A) — The (Partial) Rehabilitation of Interest Rate Parity in the Floating Rate Era

- **Autores:** Menzie D. Chinn
- **Año:** 2006
- **Publicación o institución:** Journal of International Money and Finance, vol. 25, págs. 7-21
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-04 Carry, prima de riesgo cambiaria y paridad descubierta (principal) · secundarias: TX-10
- **Calidad Q:** 82 (A) — Tipo 24/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 8/10 · Impacto 7/10 · Independencia 10/10 · Acceso 4/10
- **DOI / URL:** https://www.uh.edu/~dpapell/Taylor%20Rule%20Fundamentals.pdf (página índice: bibliografía de Molodtsova y Papell)
- **Acceso y licencia:** Peldaño 3 (Elsevier) · Licencia: Copyright Elsevier
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Taylor rule fundamentals exchange rate predictability Molodtsova Papell…»; WebFetch: sí, bibliografía del PDF de Molodtsova y Papell)
- **Contenido:** Revisa la evidencia de paridad descubierta: el rechazo es sobre todo un fenómeno de corto plazo en divisas avanzadas; a horizontes largos (bonos a 5-10 años), con expectativas de encuestas y en emergentes, la UIP se cumple mejor.
- **Uso en el bloque:** AS-ESTR y Analistas EM: el carry a corto plazo y la convergencia a UIP a largo plazo; matiz de horizonte para tesis de carry.
- **Limitaciones:** Confirmado solo por bibliografía.

#### FXA-0092 · Q 82 (A) — Anomalies: Foreign Exchange

- **Autores:** Kenneth A. Froot; Richard H. Thaler
- **Año:** 1990
- **Publicación o institución:** Journal of Economic Perspectives, vol. 4, págs. 179-192
- **Tipo de documento:** Artículo de revisión revisado por pares
- **Temática:** TX-04 Carry, prima de riesgo cambiaria y paridad descubierta (principal) · secundarias: TX-06
- **Calidad Q:** 82 (A) — Tipo 24/25 · Rigor 13/20 · Autoridad 15/15 · Vigencia 6/10 · Impacto 9/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** https://www.nber.org/papers/w13812.pdf (página índice: bibliografía de Lustig y Verdelhan 2010)
- **Acceso y licencia:** Peldaño 2 (JEP de acceso libre en la AEA) · Licencia: Copyright AEA
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Hanno Lustig Adrien Verdelhan "The Cross Section of Foreign Currency Risk Premia…"»; WebFetch: sí, bibliografía del PDF del NBER)
- **Contenido:** Revisión divulgativa de la anomalía de la prima forward: las divisas de tipo alto tienden a apreciarse en lugar de depreciarse; discute explicaciones de riesgo, de expectativas y de ajuste lento de carteras.
- **Uso en el bloque:** Analistas de segmento y AG-14 DOC-A: introducción accesible al enigma que sustenta el carry.
- **Limitaciones:** Confirmado solo por bibliografía; literatura hasta 1990.

#### FXA-0108 · Q 80 (A) — Carry Trades and Risk

- **Autores:** Craig Burnside
- **Año:** 2011 (2012 en la edición del libro)
- **Publicación o institución:** En J. James, I. W. Marsh y L. Sarno (eds.), Handbook of Exchange Rates, Wiley
- **Tipo de documento:** Capítulo de manual de referencia
- **Temática:** TX-04 Carry, prima de riesgo cambiaria y paridad descubierta (principal) · secundarias: TX-05
- **Calidad Q:** 80 (A) — Tipo 20/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 6/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** https://www.nber.org/papers/w16942.pdf (página índice: bibliografía de Burnside, Eichenbaum y Rebelo 2011)
- **Acceso y licencia:** Peldaño 3 (libro de Wiley; versión de trabajo NBER) · Licencia: Copyright Wiley
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Burnside Eichenbaum Rebelo "Carry Trade and Momentum in Currency Markets"…»; WebFetch: sí, bibliografía del PDF del NBER)
- **Contenido:** Capítulo de manual que revisa si el carry compensa riesgo: factores de consumo, de mercado y cambiarios, riesgo de crash y problemas del peso.
- **Uso en el bloque:** AS-ESTR y AG-11 CONTRA: síntesis para valorar si una tesis de carry es prima de riesgo o anomalía.
- **Limitaciones:** Confirmado solo por bibliografía.

#### FXA-0089 · Q 80 (A) — The Cross-Section of Foreign Currency Risk Premia and Consumption Growth Risk: A Reply

- **Autores:** Hanno Lustig; Adrien Verdelhan
- **Año:** 2008 (febrero; revisado en noviembre de 2010)
- **Publicación o institución:** National Bureau of Economic Research (NBER Working Paper 13812)
- **Tipo de documento:** Documento de trabajo institucional
- **Temática:** TX-04 Carry, prima de riesgo cambiaria y paridad descubierta (principal) · secundarias: TX-09
- **Calidad Q:** 80 (A) — Tipo 20/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 4/10 · Independencia 10/10 · Acceso 7/10
- **DOI / URL:** https://www.nber.org/papers/w13812.pdf
- **Acceso y licencia:** Peldaño 1 (PDF del NBER) · Licencia: Copyright de los autores
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Hanno Lustig Adrien Verdelhan "The Cross Section of Foreign Currency Risk Premia…"»; WebFetch: sí)
- **Contenido:** Responde a la crítica de Burnside: la beta de consumo del carry es grande y significativa, el precio del riesgo de consumo sigue siendo distinto de cero y las betas del carry frente al consumo y al mercado aumentan en recesiones y crisis (la crisis de 2008 como ejemplo), por lo que las betas incondicionales infravaloran su riesgo.
- **Uso en el bloque:** AG-11 CONTRA y TR-PFV: el riesgo del carry es condicional y se concentra en crisis.
- **Limitaciones:** Documento de réplica; complementa FXA-0088.

#### FXA-0097 · Q 80 (A) — On Biases in the Measurement of Foreign Exchange Risk Premiums

- **Autores:** Geert Bekaert; Robert J. Hodrick
- **Año:** 1993
- **Publicación o institución:** Journal of International Money and Finance, vol. 12, págs. 115-138
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-04 Carry, prima de riesgo cambiaria y paridad descubierta (principal) · secundarias: TX-13
- **Calidad Q:** 80 (A) — Tipo 24/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 6/10 · Impacto 7/10 · Independencia 10/10 · Acceso 3/10
- **DOI / URL:** https://www.nber.org/papers/w13812.pdf (página índice: bibliografía de Lustig y Verdelhan 2010)
- **Acceso y licencia:** Peldaño 3 (Elsevier) · Licencia: Copyright Elsevier
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Hanno Lustig Adrien Verdelhan "The Cross Section of Foreign Currency Risk Premia…"»; WebFetch: sí, bibliografía del PDF del NBER)
- **Contenido:** Analiza los sesgos de muestra pequeña y de problemas del peso en la medición de primas de riesgo cambiarias a partir de regresiones de prima forward.
- **Uso en el bloque:** AG-20 EVAL y AS-ESTR: cautela al inferir primas de carry de muestras cortas.
- **Limitaciones:** Confirmado solo por bibliografía; contenido según el título, a cotejar.

#### FXA-0106 · Q 80 (A) — The «Speculative Efficiency» Hypothesis

- **Autores:** John F. O. Bilson
- **Año:** 1981
- **Publicación o institución:** Journal of Business, vol. 54, n.º 3, págs. 435-451
- **Tipo de documento:** Artículo revisado por pares (canónico)
- **Temática:** TX-04 Carry, prima de riesgo cambiaria y paridad descubierta (principal) · secundarias: —
- **Calidad Q:** 80 (A) — Tipo 24/25 · Rigor 14/20 · Autoridad 13/15 · Vigencia 6/10 · Impacto 10/10 · Independencia 10/10 · Acceso 3/10
- **DOI / URL:** https://www.nber.org/papers/w16942.pdf (página índice: bibliografía de Burnside, Eichenbaum y Rebelo 2011)
- **Acceso y licencia:** Peldaño 3 (University of Chicago Press/JSTOR) · Licencia: Copyright UCP
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Burnside Eichenbaum Rebelo "Carry Trade and Momentum in Currency Markets"…»; WebFetch: sí, bibliografía del PDF del NBER)
- **Contenido:** Uno de los primeros contrastes de la hipótesis de eficiencia especulativa (el forward como predictor insesgado): la rechaza y muestra que una estrategia que explota la prima forward es rentable, precedente del carry trade.
- **Uso en el bloque:** AS-ESTR: antecedente histórico del carry como estrategia sistemática.
- **Limitaciones:** Confirmado solo por bibliografía.

#### FXA-0110 · Q 79 (B) — Crash Risk in Currency Markets

- **Autores:** Emmanuel Farhi; Samuel P. Fraiberger; Xavier Gabaix; Romain Rancière; Adrien Verdelhan
- **Año:** 2009
- **Publicación o institución:** National Bureau of Economic Research (NBER Working Paper 15062)
- **Tipo de documento:** Documento de trabajo institucional
- **Temática:** TX-04 Carry, prima de riesgo cambiaria y paridad descubierta (principal) · secundarias: TX-09
- **Calidad Q:** 79 (B) — Tipo 20/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 7/10 · Independencia 10/10 · Acceso 2/10
- **DOI / URL:** https://www.nber.org/papers/w16942.pdf (página índice: bibliografía de Burnside, Eichenbaum y Rebelo 2011; citado también por Lustig y Verdelhan, NBER WP 13812)
- **Acceso y licencia:** Peldaño 2 (serie de trabajo del NBER) · Licencia: Copyright de los autores
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Burnside Eichenbaum Rebelo "Carry Trade and Momentum in Currency Markets"…»; WebFetch: sí, bibliografías de dos PDF del NBER)
- **Contenido:** Usa precios de opciones de divisas (risk reversals) para estimar la prima por riesgo de desastre en el carry trade: una parte sustancial de la rentabilidad del carry compensa el riesgo de crash global.
- **Uso en el bloque:** TR-PFV y AS-ESTR: risk reversals como medida del coste del seguro contra crash del carry.
- **Limitaciones:** Confirmado solo por bibliografía; versión publicada no verificada.

## TX-05 Momentum, valor y factores cambiarios

#### ANA-DOC-0003 · Q 96 (A) — Value and Momentum Everywhere

- **Autores:** Clifford S. Asness; Tobias J. Moskowitz; Lasse Heje Pedersen
- **Año:** 2013
- **Publicación o institución:** The Journal of Finance, vol. 68, n.º 3 (Wiley)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-05 Momentum, valor y factores cambiarios (principal) · secundarias: —
- **Calidad Q:** 96 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 9/10 · Acceso 9/10
- **DOI / URL:** DOI 10.1111/jofi.12021 · PDF del autor: https://pages.stern.nyu.edu/~lpederse/papers/ValMomEverywhere.pdf · SSRN: papers.ssrn.com/sol3/papers.cfm?abstract_id=2174501 · datos: https://www.aqr.com/Insights/Datasets?&page=2
- **Acceso y licencia:** Peldaño 2 (PDF de autor y postprint en la Copenhagen Business School) · Licencia: Copyright Wiley
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Asness Moskowitz Pedersen "Value and Momentum Everywhere" Journal of Finance 2013 currencies Moskowitz Ooi Pedersen "Time Series Momentum"», que devolvió el PDF del autor en NYU; WebFetch: sí, página de datos de AQR que lista «Value and Momentum Everywhere: Original Paper Data»; el PDF redirige a una dirección no accesible para la herramienta) · reutilizada del F7 V3.2 (TA-05; estaba en PENDIENTE_BARRIDO y se reverifica aquí)
- **Contenido:** Encuentra primas de valor y de momentum consistentes en ocho mercados y clases de activo, incluidas las divisas (valor medido como reversión de largo plazo del tipo real; momentum de 12 meses), con correlación negativa entre ambos estilos y factores comunes de liquidez entre clases de activo.
- **Uso en el bloque:** AS-ESTR y AG-13 MOTOR (PERF-FX-FACT): definición estándar de valor y momentum cambiarios y argumento para combinarlos; coherencia con factores de otras clases de activo.
- **Limitaciones:** Coautores vinculados a AQR (Independencia 9/10); universo de divisas G10.

#### ANA-DOC-0002 · Q 96 (A) — Time Series Momentum

- **Autores:** Tobias J. Moskowitz; Yao Hua Ooi; Lasse Heje Pedersen
- **Año:** 2012
- **Publicación o institución:** Journal of Financial Economics, vol. 104, n.º 2, págs. 228-250 (Elsevier)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-05 Momentum, valor y factores cambiarios (principal) · secundarias: TX-06
- **Calidad Q:** 96 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 9/10 · Acceso 9/10
- **DOI / URL:** DOI 10.1016/j.jfineco.2011.11.003 · PDF de autor: docs.lhpedersen.com/TimeSeriesMomentum.pdf · datos: https://www.aqr.com/Insights/Datasets?&page=2
- **Acceso y licencia:** Peldaño 3 (versión de autor en web académica personal, acceso gratuito) · Licencia: Copyright Elsevier
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Asness Moskowitz Pedersen "Value and Momentum Everywhere"… Moskowitz Ooi Pedersen "Time Series Momentum"»; WebFetch: sí, página de datos de AQR que lista «Time Series Momentum: Original Paper Data — Moskowitz, Ooi and Pedersen (2012)»; citada además en la bibliografía de Burnside, Eichenbaum y Rebelo, NBER WP 16942) · reutilizada del F7 V3.2 (TA-03; estaba en PENDIENTE_BARRIDO y se reverifica aquí)
- **Contenido:** Documenta momentum temporal (tendencia) significativo en 58 futuros y forwards líquidos, incluidos los de divisas: la rentabilidad propia de 12 meses predice positivamente la del año siguiente, con reversión parcial a más largo plazo; los especuladores (CFTC) siguen la tendencia a costa de los coberturistas.
- **Uso en el bloque:** AS-ESTR y Analistas de segmento: lente «momentum y tendencia» del cribado (Documento 0, 8.1) aplicada a pares concretos; TR-PFV: relación con el posicionamiento especulativo.
- **Limitaciones:** Coautores vinculados a AQR; sensibilidad a costes de transacción.

#### ANA-DOC-0300 · Q 95 (A) — Common Risk Factors in Currency Markets

- **Autores:** Hanno Lustig; Nikolai Roussanov; Adrien Verdelhan
- **Año:** 2011
- **Publicación o institución:** Review of Financial Studies, vol. 24, n.º 11, págs. 3731-3777
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-05 Momentum, valor y factores cambiarios (principal) · secundarias: TX-04
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / URL:** https://dspace.mit.edu/handle/1721.1/66103 · versión de trabajo: https://nber.org/papers/w14082
- **Acceso y licencia:** Peldaño 2 (versión aceptada en DSpace@MIT, acceso abierto) · Licencia: Copyright del editor; versión de autor de lectura libre
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Lustig Roussanov Verdelhan 2011 "Common Risk Factors in Currency Markets" Review of Financial Studies»; WebFetch: sí) · reutilizada del F7 V3.2 (TA-07)
- **Contenido:** Identifica un factor «slope» (HML de divisas, carry) y un factor «nivel» (dólar) que explican la mayor parte de la variación de los rendimientos de carteras de divisas ordenadas por tipo de interés; el factor carry se vincula a la volatilidad global de la renta variable.
- **Uso en el bloque:** AS-ESTR y AG-13 MOTOR (perfil PERF-FX-FACT): estructura factorial del mercado cambiario (dólar y carry) para descomponer la rentabilidad de cualquier par o cesta y evitar exposiciones duplicadas entre top-3.
- **Limitaciones:** Muestra hasta finales de los 2000; la prima carry cambió de comportamiento tras 2008.

#### ANA-DOC-0008 · Q 94 (A) — Currency Momentum Strategies

- **Autores:** Lukas Menkhoff; Lucio Sarno; Maik Schmeling; Andreas Schrimpf
- **Año:** 2012
- **Publicación o institución:** Journal of Financial Economics, vol. 106, n.º 3, págs. 660-684 (Elsevier)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-05 Momentum, valor y factores cambiarios (principal) · secundarias: TX-04
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 10/10 · Acceso 9/10
- **DOI / URL:** DOI 10.1016/j.jfineco.2012.06.009 · https://openaccess.city.ac.uk/id/eprint/3296/ · versión de trabajo: BIS Working Papers 366 (https://ideas.repec.org/p/bis/biswps/366.html)
- **Acceso y licencia:** Peldaño 2 (versión aceptada en repositorio institucional abierto) · Licencia: Copyright Elsevier; la versión aceptada se cita como acceso de lectura
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Menkhoff Sarno Schmeling Schrimpf "Currency Value" Review of Financial Studies 2017»; WebFetch: sí, páginas índice https://openaccess.city.ac.uk/view/creators/Sarno=3AL=2E=3A=3A.html y https://ideas.repec.org/e/psc117.html, que dan revista, volumen, páginas y DOI) · reutilizada del F7 V3.2 (TA-07; estaba en PENDIENTE_BARRIDO y se reverifica aquí)
- **Contenido:** Encuentra un diferencial de hasta un 10 % anual entre divisas ganadoras y perdedoras pasadas (momentum transversal), no explicado por factores de riesgo tradicionales ni por el carry; el beneficio se concentra en divisas con costes y riesgo país altos, lo que apunta a límites al arbitraje.
- **Uso en el bloque:** AS-ESTR y AG-13 MOTOR (PERF-FX-FACT): fundamento del momentum cambiario como estrategia sistemática y de su escasa correlación con el carry; AG-11 CONTRA: costes de transacción y reversiones.
- **Limitaciones:** Horizonte hasta 2010; sensibilidad a costes de transacción documentada por los propios autores.

#### FXA-0010 · Q 91 (A) — Currency Value

- **Autores:** Lukas Menkhoff; Lucio Sarno; Maik Schmeling; Andreas Schrimpf
- **Año:** 2017 (CEPR DP 11324 de 2016)
- **Publicación o institución:** The Review of Financial Studies, vol. 30, n.º 2, págs. 416-441
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-05 Momentum, valor y factores cambiarios (principal) · secundarias: TX-03
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 10/10 · Acceso 6/10
- **DOI / URL:** DOI 10.1093/rfs/hhw067 · https://openaccess.city.ac.uk/id/eprint/14851/ · WP: https://ideas.repec.org/p/cpr/ceprdp/11324.html
- **Acceso y licencia:** Peldaño 2 (versión de autor en City Research Online) · Licencia: Copyright OUP
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Menkhoff Sarno Schmeling Schrimpf "Currency Value" Review of Financial Studies 2017»; WebFetch: sí, páginas índice de City Research Online e IDEAS (psc117) con revista, volumen, páginas y DOI)
- **Contenido:** Construye una medida de valor de las divisas: el tipo de cambio real ajustado por fundamentales (productividad, calidad de las exportaciones, activos exteriores netos, cuota de importaciones) predice mejor la rentabilidad cambiaria que la PPA simple; la estrategia de valor así definida es distinta del carry y del momentum.
- **Uso en el bloque:** AS-ESTR (estrategia de valor) y Analistas de segmento: lente «valor» del cribado (Documento 0, 8.1) con REER ajustado por fundamentales en lugar de PPA bruta.
- **Limitaciones:** Señal lenta (horizonte H3–H4); depende de datos macro con retraso de publicación.

#### FXA-0121 · Q 91 (A) — Countercyclical Currency Risk Premia

- **Autores:** Hanno Lustig; Nikolai Roussanov; Adrien Verdelhan
- **Año:** 2014 (NBER WP 16427, 2010, rev. 2013; Premio AQR Insight 2012, mención de honor)
- **Publicación o institución:** Journal of Financial Economics, vol. 111, n.º 3, págs. 527-553
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-05 Momentum, valor y factores cambiarios (principal) · secundarias: TX-04, TX-12
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 10/10 · Acceso 6/10
- **DOI / URL:** https://dspace.mit.edu/handle/1721.1/114867 · PDF: https://dspace.mit.edu/bitstream/1721.1/114867/1/Verdelhan_Countercyclical.pdf · WP: https://www.nber.org/papers/w16427.pdf
- **Acceso y licencia:** Peldaño 2 (versión aceptada en DSpace@MIT) · Licencia: Copyright Elsevier
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Lustig Roussanov Verdelhan "Countercyclical Currency Risk Premia" Journal of Financial Economics 2014 dollar carry trade»; WebFetch: sí, DSpace@MIT y página del premio AQR)
- **Contenido:** Propone el «dollar carry trade» (largo en divisas extranjeras frente al dólar cuando el descuento forward medio es positivo y corto cuando es negativo), con rentabilidades altas y poco correlacionadas con el carry clásico; el descuento forward medio y el crecimiento de la producción industrial de EE. UU. predicen hasta un 25 % de la variación anual de la rentabilidad del dólar.
- **Uso en el bloque:** AS-ESTR (estrategia «dólar amplio») y AS-G10N: señal sistemática de dirección del dólar basada en el diferencial medio de tipos y el ciclo de EE. UU.
- **Limitaciones:** Muestra hasta 2010; predictibilidad de un año con incertidumbre de estimación.

#### FXA-0076 · Q 90 (A) — Currency Risk Premiums Redux

- **Autores:** Federico Nucera; Lucio Sarno; Gabriele Zinna
- **Año:** 2024 (CEPR DP 18012, 2023, como «Currency Risk Premia Redux»)
- **Publicación o institución:** The Review of Financial Studies, vol. 37, n.º 2, págs. 356-408
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-05 Momentum, valor y factores cambiarios (principal) · secundarias: TX-04
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 5/10 · Independencia 10/10 · Acceso 7/10
- **DOI / URL:** DOI 10.1093/rfs/hhad049 · https://ideas.repec.org/a/oup/rfinst/v37y2024i2p356-408..html · versión abierta: https://repec.cepr.org/repec/cpr/ceprdp/DP18012.pdf
- **Acceso y licencia:** Peldaño 2 (DP del CEPR en PDF abierto; artículo de pago) · Licencia: Copyright OUP
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Pasquale Della Corte IDEAS RePEc author currency factors dollar risk»; WebFetch: sí, ficha IDEAS y PDF del CEPR)
- **Contenido:** Con métodos que corrigen sesgos de variables omitidas y error de medida en una amplia sección cruzada de divisas, el núcleo de valoración tiene al menos tres factores latentes: un factor dólar fuerte y dos factores de pendiente tipo carry y momentum con ratios de Sharpe altos; la evidencia de un factor valor es débil y, de más de 100 factores candidatos no negociables, solo unos pocos (volatilidad, incertidumbre y liquidez) tienen prima significativa.
- **Uso en el bloque:** AS-ESTR y AG-13 MOTOR (PERF-FX-FACT): selección parsimoniosa de factores cambiarios (dólar, carry, momentum) y escepticismo ante factores macro; AG-11 CONTRA.
- **Limitaciones:** Resultados dependientes del universo de divisas y del periodo.

#### ANA-DOC-0362 · Q 90 (A) — The Share of Systematic Variation in Bilateral Exchange Rates

- **Autores:** Adrien Verdelhan
- **Año:** 2018
- **Publicación o institución:** The Journal of Finance, vol. 73, n.º 1, págs. 375-418
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-05 Momentum, valor y factores cambiarios (principal) · secundarias: TX-12
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 4/10
- **DOI / URL:** DOI 10.1111/jofi.12587 · https://ideas.repec.org/a/bla/jfinan/v73y2018i1p375-418.html · versión abierta: https://dspace.mit.edu/handle/1721.1/122354
- **Acceso y licencia:** Peldaño 2 (DSpace@MIT) · Licencia: Copyright Wiley/AFA
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Adrien Verdelhan IDEAS RePEc "The Share of Systematic Variation in Bilateral Exchange Rates"»; WebFetch: sí) · reutilizada del F7 V3.2 (TA-07)
- **Contenido:** Ordenando países por su beta frente al dólar surge un factor «dólar» independiente del carry; ambos factores explican entre el 18 % y el 80 % de la variación mensual de los tipos de cambio bilaterales.
- **Uso en el bloque:** AG-02 ANZ y AS-ESTR: separar movimientos sistemáticos (dólar, carry) de idiosincrásicos al asignar oportunidades a segmentos y al resolver exposiciones comunes al dólar entre top-3.
- **Limitaciones:** Complementa ANA-DOC-0300.

#### FXA-0077 · Q 89 (A) — Pricing Currency Risks

- **Autores:** Mikhail Chernov; Magnus Dahlquist; Lars Lochstoer
- **Año:** 2023
- **Publicación o institución:** The Journal of Finance, vol. 78, n.º 2, págs. 693-730
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-05 Momentum, valor y factores cambiarios (principal) · secundarias: TX-04
- **Calidad Q:** 89 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 5/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** DOI 10.1111/jofi.13190 · https://ideas.repec.Org/a/bla/jfinan/v78y2023i2p693-730.html
- **Acceso y licencia:** Peldaño 3 (Wiley/AFA; versiones de trabajo previas) · Licencia: Copyright Wiley/AFA
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Pasquale Della Corte IDEAS RePEc author currency factors dollar risk»; WebFetch: sí)
- **Contenido:** Tres señales bastan para explicar la rentabilidad de las divisas: diferencial de tipos (carry), tendencia de precios (momentum) y reversión a la media (valor); con ellas construye una cartera eficiente en tiempo real que abarca las estrategias cambiarias principales. Al menos el 85 % del riesgo de estas posiciones no está valorado.
- **Uso en el bloque:** AS-ESTR: combinación de carry, momentum y valor en una sola cartera eficiente; AG-11 CONTRA: no confundir volatilidad con riesgo compensado.
- **Limitaciones:** Construcción de carteras exigente en estimación de covarianzas.

#### FXA-0011 · Q 88 (A) — Business Cycles and Currency Returns

- **Autores:** Riccardo Colacito; Steven J. Riddiough; Lucio Sarno
- **Año:** 2020
- **Publicación o institución:** Journal of Financial Economics, vol. 137, n.º 3, págs. 659-678
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-05 Momentum, valor y factores cambiarios (principal) · secundarias: TX-02
- **Calidad Q:** 88 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 6/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** DOI 10.1016/j.jfineco.2020.04.005 · https://openaccess.city.ac.uk/id/eprint/22867/
- **Acceso y licencia:** Peldaño 2 (versión de autor en City Research Online) · Licencia: Copyright Elsevier
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Menkhoff Sarno Schmeling Schrimpf "Currency Value" Review of Financial Studies 2017»; WebFetch: sí, página índice https://openaccess.city.ac.uk/view/creators/Sarno=3AL=2E=3A=3A.html)
- **Contenido:** Las divisas de países con posición cíclica fuerte (brecha de producción alta) tienden a apreciarse frente a las de países con ciclo débil; una estrategia que ordena divisas por la brecha de producción genera rentabilidad no explicada por carry, momentum ni valor.
- **Uso en el bloque:** TR-BCM y Analistas G10: el diferencial cíclico (y su reflejo en la política monetaria esperada) como señal transversal; AS-ESTR: factor macro adicional.
- **Limitaciones:** Brechas de producción estimadas con incertidumbre en tiempo real.

#### FXA-0013 · Q 87 (A) — Exchange Rates and Sovereign Risk

- **Autores:** Pasquale Della Corte; Lucio Sarno; Maik Schmeling; Christian Wagner
- **Año:** 2022 (CEPR DP 16058 de 2021)
- **Publicación o institución:** Management Science, vol. 68, n.º 8, págs. 5591-5617
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-05 Momentum, valor y factores cambiarios (principal) · secundarias: TX-10, TX-09
- **Calidad Q:** 87 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 5/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** DOI 10.1287/mnsc.2021.4115 · https://openaccess.city.ac.uk/id/eprint/31277/ · https://ideas.repec.org/a/inm/ormnsc/v68y2022i8p5591-5617.html
- **Acceso y licencia:** Peldaño 2 (versión de autor en City Research Online) · Licencia: Copyright INFORMS
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Menkhoff Sarno Schmeling Schrimpf "Currency Value" Review of Financial Studies 2017»; WebFetch: sí, páginas índice de City Research Online e IDEAS (psc117))
- **Contenido:** Los aumentos del riesgo soberano (CDS) van acompañados de depreciación de la divisa y de mayor volatilidad cambiaria; la exposición de las divisas a un factor global de riesgo soberano explica parte de la sección cruzada de rentabilidades cambiarias.
- **Uso en el bloque:** Analistas EM (AS-EMLA, AS-EMEA) y AS-ESTR: CDS soberanos como indicador de cribado y factor de riesgo cambiario (Documento 0, 8.2).
- **Limitaciones:** Disponibilidad de CDS limitada para algunas divisas.

#### FXA-0014 · Q 87 (A) — Volatility Risk Premia and Exchange Rate Predictability

- **Autores:** Pasquale Della Corte; Tarun Ramadorai; Lucio Sarno
- **Año:** 2016
- **Publicación o institución:** Journal of Financial Economics, vol. 120, n.º 1, págs. 21-40
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-05 Momentum, valor y factores cambiarios (principal) · secundarias: TX-06, TX-13
- **Calidad Q:** 87 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 6/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** DOI 10.1016/j.jfineco.2016.02.015 · https://openaccess.city.ac.uk/id/eprint/13156/
- **Acceso y licencia:** Peldaño 2 (versión de autor en City Research Online) · Licencia: Copyright Elsevier
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Menkhoff Sarno Schmeling Schrimpf "Currency Value" Review of Financial Studies 2017»; WebFetch: sí, página índice de City Research Online)
- **Contenido:** La prima de riesgo de volatilidad cambiaria (diferencia entre volatilidad implícita y realizada) predice la rentabilidad del contado: comprar divisas con seguro de volatilidad barato y vender las de seguro caro genera rentabilidad no explicada por carry, momentum ni valor.
- **Uso en el bloque:** TR-PFV y AS-ESTR: uso de la volatilidad implícita no solo como riesgo sino como señal de cribado transversal.
- **Limitaciones:** Requiere datos de opciones fiables (limitados en algunas EM).

#### FXA-0102 · Q 87 (A) — Carry Trade and Momentum in Currency Markets

- **Autores:** Craig Burnside; Martin Eichenbaum; Sergio Rebelo
- **Año:** 2011 (NBER WP 16942, abril de 2011)
- **Publicación o institución:** Annual Review of Financial Economics, vol. 3, págs. 511-535
- **Tipo de documento:** Artículo de revisión revisado por pares
- **Temática:** TX-05 Momentum, valor y factores cambiarios (principal) · secundarias: TX-04
- **Calidad Q:** 87 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 8/10 · Independencia 10/10 · Acceso 4/10
- **DOI / URL:** https://www.nber.org/papers/w16942.pdf · https://ideas.repec.org:443/a/anr/refeco/v3y2011p511-535.html · datos actualizados: https://people.duke.edu/~acb8/Burnside/Currency_Speculation_Data.html
- **Acceso y licencia:** Peldaño 1 (WP del NBER en PDF y datos abiertos del autor) · Licencia: Copyright Annual Reviews/autores
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Burnside Eichenbaum Rebelo "Carry Trade and Momentum in Currency Markets" Annual Review of Financial Economics»; WebFetch: sí, PDF del NBER y página de datos de Duke)
- **Contenido:** Revisa la rentabilidad del carry y del momentum en 20 divisas (1976-2010) y tres explicaciones: los factores de riesgo convencionales no la explican (los factores cambiarios explican el carry pero no el momentum); la crisis de 2008 no es el «desastre» relevante (el momentum ganó); y la presión de precios permite pagos medios positivos aunque la operación marginal no lo sea.
- **Uso en el bloque:** AS-ESTR: síntesis de referencia del carry y el momentum como estrategias; datos actualizados de pagos para el MOTOR.
- **Limitaciones:** Muestra hasta 2010.

#### FXA-0120 · Q 86 (A) — Beyond the Carry Trade: Optimal Currency Portfolios

- **Autores:** Pedro Barroso; Pedro Santa-Clara
- **Año:** 2015
- **Publicación o institución:** Journal of Financial and Quantitative Analysis, vol. 50, n.º 5, págs. 1037-1056 (Cambridge University Press)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-05 Momentum, valor y factores cambiarios (principal) · secundarias: TX-04
- **Calidad Q:** 86 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 13/15 · Vigencia 9/10 · Impacto 7/10 · Independencia 10/10 · Acceso 4/10
- **DOI / URL:** https://ideas.repec.org/a/cup/jfinqa/v50y2015i05p1037-1056_00.html · versión de autor: https://ore.exeter.ac.uk/repository/handle/10871/14068 · https://run.unl.pt/handle/10362/14970
- **Acceso y licencia:** Peldaño 2 (versiones de autor en repositorios de Exeter y NOVA) · Licencia: Copyright Cambridge University Press
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Barroso Santa-Clara "Beyond the Carry Trade: Optimal Currency Portfolios" Journal of Financial and Quantitative Analysis»; WebFetch: sí, ficha IDEAS)
- **Contenido:** Contrasta qué señales técnicas y fundamentales mejoran una cartera de divisas: carry, momentum y reversión de valor aportan; el tipo de cambio real y la cuenta corriente no. La cartera óptima obtiene rentabilidades fuera de muestra no explicadas por factores de riesgo estándar y eleva en torno a 0,5 el ratio de Sharpe de carteras diversificadas, con menor riesgo de crash.
- **Uso en el bloque:** AS-ESTR y AG-13 MOTOR (PERF-FX-FACT): combinación óptima de señales cambiarias y su valor en una cartera multiactivo.
- **Limitaciones:** Optimización sensible a estimaciones; muestra hasta 2012 aprox.

#### FXA-0079 · Q 85 (A) — The cross-section of currency volatility premia

- **Autores:** Pasquale Della Corte; Roman Kozhan; Anthony Neuberger
- **Año:** 2021
- **Publicación o institución:** Journal of Financial Economics, vol. 139, n.º 3, págs. 950-970
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-05 Momentum, valor y factores cambiarios (principal) · secundarias: TX-06
- **Calidad Q:** 85 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 5/10 · Independencia 10/10 · Acceso 3/10
- **DOI / URL:** https://ideas.repec.org/f/c/pde393.html (página índice de citas del autor en IDEAS; ficha: ideas.repec.org/a/eee/jfinec/v139y2021i3p950-970.html)
- **Acceso y licencia:** Peldaño 3 (Elsevier) · Licencia: Copyright Elsevier
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Pasquale Della Corte IDEAS RePEc author currency factors dollar risk»; WebFetch: sí, página índice https://ideas.repec.org/f/c/pde393.html con revista, volumen y páginas)
- **Contenido:** Estudia la sección cruzada de primas de volatilidad cambiaria (diferencia entre volatilidad implícita y realizada) en muchos pares, y su relación con factores de riesgo comunes.
- **Uso en el bloque:** TR-PFV y AS-ESTR: estrategias de volatilidad cambiaria en cestas (ESTR, regla 3 de 2.6).
- **Limitaciones:** Confirmado solo por índice; resumen no leído en esta carga.

#### FXA-0012 · Q 85 (A) — Which Fundamentals Drive Exchange Rates? A Cross-Sectional Perspective

- **Autores:** Lucio Sarno; Maik Schmeling
- **Año:** 2014 (CEPR DP 9472 de 2013)
- **Publicación o institución:** Journal of Money, Credit and Banking, vol. 46, n.º 2-3, págs. 267-292
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-05 Momentum, valor y factores cambiarios (principal) · secundarias: TX-01
- **Calidad Q:** 85 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 8/10 · Impacto 6/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** DOI 10.1111/jmcb.12106 · https://openaccess.city.ac.uk/id/eprint/3406/ · https://ideas.repec.org/a/wly/jmoncb/v46y2014i2-3p267-292.html
- **Acceso y licencia:** Peldaño 2 (versión de autor en City Research Online) · Licencia: Copyright Wiley
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Menkhoff Sarno Schmeling Schrimpf "Currency Value" Review of Financial Studies 2017»; WebFetch: sí, páginas índice de City Research Online e IDEAS (psc117))
- **Contenido:** Ordena divisas en carteras por su tipo de cambio relativo a fundamentales (diferenciales de inflación, dinero, producción) y muestra que esas carteras predicen los fundamentales futuros: el tipo de cambio incorpora información sobre fundamentales en la sección cruzada aunque falle en series temporales.
- **Uso en el bloque:** Analistas de segmento y AS-ESTR: justificación de las lentes de fundamentales en comparación transversal (qué divisa está cara o barata respecto a las demás).
- **Limitaciones:** Resultado sobre predicción de fundamentales, no de rentabilidad directa.

#### FXA-0081 · Q 85 (A) — Spot and forward volatility in foreign exchange

- **Autores:** Pasquale Della Corte; Lucio Sarno; Ilias Tsiakas
- **Año:** 2011 (CEPR DP 7893 de 2010)
- **Publicación o institución:** Journal of Financial Economics, vol. 100, n.º 3, págs. 496-513
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-05 Momentum, valor y factores cambiarios (principal) · secundarias: TX-06
- **Calidad Q:** 85 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 14/15 · Vigencia 8/10 · Impacto 6/10 · Independencia 10/10 · Acceso 4/10
- **DOI / URL:** DOI 10.1016/j.jfineco.2011.01.007 · https://openaccess.city.ac.uk/id/eprint/3303/
- **Acceso y licencia:** Peldaño 2 (versión de autor en City Research Online) · Licencia: Copyright Elsevier
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Pasquale Della Corte IDEAS RePEc author currency factors dollar risk»; WebFetch: sí, páginas índice https://ideas.repec.org/f/c/pde393.html y https://openaccess.city.ac.uk/view/creators/Sarno=3AL=2E=3A=3A.html)
- **Contenido:** Analiza la relación entre la volatilidad del contado y la volatilidad forward (acuerdos de volatilidad a plazo) en divisas y evalúa el valor económico de estrategias que explotan la prima por plazo de la volatilidad cambiaria.
- **Uso en el bloque:** TR-PFV y AS-ESTR: estructura temporal de la volatilidad implícita como fuente de rentabilidad.
- **Limitaciones:** Confirmado por índices; resumen no leído en esta carga.

#### FXA-0082 · Q 83 (A) — Global Risks in the Currency Market

- **Autores:** George Panayotov
- **Año:** 2020
- **Publicación o institución:** Review of Finance, vol. 24, n.º 6, págs. 1237-1270
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-05 Momentum, valor y factores cambiarios (principal) · secundarias: TX-04
- **Calidad Q:** 83 (A) — Tipo 24/25 · Rigor 17/20 · Autoridad 13/15 · Vigencia 10/10 · Impacto 4/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** DOI 10.1093/rof/rfaa010 · https://ideas.repec.org/a/oup/revfin/v24y2020i6p1237-1270..html
- **Acceso y licencia:** Peldaño 3 (OUP, de pago) · Licencia: Copyright OUP
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Pasquale Della Corte IDEAS RePEc author currency factors dollar risk»; WebFetch: sí)
- **Contenido:** Propone un contraste de valoración basado en la exposición distintiva de EE. UU. al riesgo global y lo aplica a muchos factores de la literatura cambiaria: solo el riesgo del mercado de renta variable actúa como riesgo global en el mercado de divisas.
- **Uso en el bloque:** AS-ESTR y AG-02 ANZ: el riesgo de renta variable global como principal determinante común de las primas cambiarias; coherencia con exposiciones multiactivo.
- **Limitaciones:** Resultado frente a un conjunto concreto de factores candidatos.

#### FXA-0107 · Q 80 (A) — The Carry Trade and Fundamentals: Nothing to Fear but FEER Itself

- **Autores:** Òscar Jordà; Alan M. Taylor
- **Año:** 2009
- **Publicación o institución:** National Bureau of Economic Research (NBER Working Paper 15518)
- **Tipo de documento:** Documento de trabajo institucional
- **Temática:** TX-05 Momentum, valor y factores cambiarios (principal) · secundarias: TX-04, TX-03
- **Calidad Q:** 80 (A) — Tipo 20/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 7/10 · Independencia 10/10 · Acceso 3/10
- **DOI / URL:** https://www.nber.org/papers/w16942.pdf (página índice: bibliografía de Burnside, Eichenbaum y Rebelo 2011)
- **Acceso y licencia:** Peldaño 2 (serie de trabajo del NBER) · Licencia: Copyright de los autores
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Burnside Eichenbaum Rebelo "Carry Trade and Momentum in Currency Markets"…»; WebFetch: sí, bibliografía del PDF del NBER)
- **Contenido:** Combina la señal de carry con la desviación del tipo de cambio respecto a su equilibrio fundamental (FEER/PPA) y con el momentum: el carry «condicionado» por valor reduce mucho el riesgo de crash del carry ingenuo.
- **Uso en el bloque:** AS-ESTR: diseño de carry ajustado por valor (Documento 0, 2.6: carry ajustado y valor); AG-11 CONTRA: alerta cuando el carry coincide con sobrevaloración.
- **Limitaciones:** Confirmado solo por bibliografía; versión publicada (JIE 2012) no verificada en esta carga.

#### FXA-0103 · Q 80 (A) — Do Momentum-Based Strategies Still Work in Foreign Currency Markets?

- **Autores:** John Okunev; Derek White
- **Año:** 2003
- **Publicación o institución:** Journal of Financial and Quantitative Analysis, vol. 38, n.º 2, págs. 425-447
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-05 Momentum, valor y factores cambiarios (principal) · secundarias: —
- **Calidad Q:** 80 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 12/15 · Vigencia 7/10 · Impacto 8/10 · Independencia 10/10 · Acceso 3/10
- **DOI / URL:** https://www.nber.org/papers/w16942.pdf (página índice: bibliografía de Burnside, Eichenbaum y Rebelo 2011)
- **Acceso y licencia:** Peldaño 3 (Cambridge University Press) · Licencia: Copyright del editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Burnside Eichenbaum Rebelo "Carry Trade and Momentum in Currency Markets"…»; WebFetch: sí, bibliografía del PDF del NBER con revista, volumen y páginas)
- **Contenido:** Estrategias de momentum transversal (comprar las divisas que más se han apreciado y vender las que menos) en divisas G10 siguen siendo rentables en los noventa, frente a la idea de que las reglas técnicas habían dejado de funcionar.
- **Uso en el bloque:** AS-ESTR: evidencia temprana del momentum cambiario transversal, previa a ANA-DOC-0008.
- **Limitaciones:** Confirmado solo por bibliografía; muestra hasta 2000.

#### FXA-0061 · Q 78 (B) — Forty Years, Thirty Currencies and 21,000 Trading Rules: A Large-Scale Data-Snooping Robust Analysis of Technical Trading in the Foreign Exchange Market

- **Autores:** Pohsuan Hsu; Mark P. Taylor
- **Año:** 2014
- **Publicación o institución:** Centre for Economic Policy Research (CEPR Discussion Paper 10018)
- **Tipo de documento:** Documento de trabajo institucional
- **Temática:** TX-05 Momentum, valor y factores cambiarios (principal) · secundarias: TX-13
- **Calidad Q:** 78 (B) — Tipo 20/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 8/10 · Impacto 5/10 · Independencia 10/10 · Acceso 4/10
- **DOI / URL:** https://causalclaims.trfetzer.com/author/MarkPTaylor.html (página índice de trabajos del autor; enlace DP10018)
- **Acceso y licencia:** Peldaño 3 (CEPR) · Licencia: Copyright de los autores/CEPR
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Alan Taylor Mark Taylor 2004 "The Purchasing Power Parity Debate"…»; WebFetch: sí, página índice de causalclaims)
- **Contenido:** Evalúa unas 21.000 reglas de análisis técnico (tendencia/momentum) en 30 divisas durante 40 años con contrastes robustos al data snooping, para separar rentabilidades genuinas de las debidas a búsqueda múltiple.
- **Uso en el bloque:** AS-ESTR y AG-20 EVAL: disciplina frente a la minería de datos en señales de tendencia cambiaria.
- **Limitaciones:** Confirmado solo por índice; resultados concretos no leídos en esta carga.

#### FXA-0059 · Q 76 (B) — Common Macro Factors and Currency Premia

- **Autores:** Ilias Filippou; Mark P. Taylor
- **Año:** 2014
- **Publicación o institución:** Centre for Economic Policy Research (CEPR Discussion Paper 10016)
- **Tipo de documento:** Documento de trabajo institucional
- **Temática:** TX-05 Momentum, valor y factores cambiarios (principal) · secundarias: TX-04
- **Calidad Q:** 76 (B) — Tipo 20/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 8/10 · Impacto 5/10 · Independencia 10/10 · Acceso 4/10
- **DOI / URL:** https://causalclaims.trfetzer.com/author/MarkPTaylor.html (página índice de trabajos del autor; enlace DP10016)
- **Acceso y licencia:** Peldaño 3 (CEPR) · Licencia: Copyright de los autores/CEPR
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Alan Taylor Mark Taylor 2004 "The Purchasing Power Parity Debate"…»; WebFetch: sí, página índice de causalclaims)
- **Contenido:** Investiga si factores macroeconómicos comunes (extraídos de grandes paneles de variables) explican las primas de las estrategias cambiarias (carry, momentum).
- **Uso en el bloque:** AS-ESTR: vínculo entre factores cambiarios y el ciclo macro global.
- **Limitaciones:** Confirmado solo por índice; contenido inferido del título; versión publicada no verificada.

## TX-06 Microestructura, flujo de órdenes y posicionamiento

#### FXA-0201 · Q 95 (A) — Order Flow and Exchange Rate Dynamics

- **Autores:** Martin D. D. Evans; Richard K. Lyons
- **Año:** 2002
- **Publicación o institución:** Journal of Political Economy, vol. 110, n.º 1 (febrero), págs. 170-180 · versión de trabajo: NBER Working Paper 7317 (1999)
- **Tipo de documento:** Artículo revisado por pares (con documento de trabajo NBER)
- **Temática:** TX-06 Microestructura, flujo de órdenes y posicionamiento (principal) · secundarias: TX-13, TX-01
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 10/10 · Independencia 10/10 · Acceso 9/10
- **DOI / URL:** DOI (versión NBER): 10.3386/w7317 · https://www.nber.org/papers/w7317
- **Acceso y licencia:** Documento de trabajo NBER de lectura libre; versión JPE de pago (University of Chicago Press)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Evans Lyons 2002 "Order Flow and Exchange Rate Dynamics" Journal of Political Economy»; WebFetch: sí, NBER w7317)
- **Contenido:** Introduce el flujo de órdenes interbancario como variable explicativa del tipo de cambio: con datos diarios DM/USD y JPY/USD el modelo alcanza R² superiores al 50 % y bate al paseo aleatorio a corto plazo; 1.000 millones de compras netas de dólares elevan el DM/USD en torno a un pfennig.
- **Uso en el bloque:** TR-PFV (AG-21): fundamento del uso de flujos y posicionamiento como lente de cribado; AS-G10N: interpretación de movimientos diarios no explicados por fundamentos; PROS y EVAL: referencia de modelos «micro» frente al paseo aleatorio.
- **Limitaciones:** Muestra de cuatro meses de 1996 y flujo interbancario (no disponible públicamente); el poder explicativo contemporáneo no implica capacidad predictiva con datos públicos.

#### FXA-0216 · Q 93 (A) — Information Flows in Foreign Exchange Markets: Dissecting Customer Currency Trades

- **Autores:** Lukas Menkhoff; Lucio Sarno; Maik Schmeling; Andreas Schrimpf
- **Año:** 2016
- **Publicación o institución:** Journal of Finance, vol. 71, n.º 2 (abril), págs. 601-634 · versión de trabajo: BIS Working Papers n.º 405 (2013)
- **Tipo de documento:** Artículo revisado por pares (con documento de trabajo del BPI)
- **Temática:** TX-06 Microestructura, flujo de órdenes y posicionamiento (principal) · secundarias: TX-13
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 8/10 · Independencia 9/10 · Acceso 9/10
- **DOI / URL:** https://ideas.repec.org:443/a/bla/jfinan/v71y2016i2p601-634.html · versión de trabajo: https://www.bis.org/publ/work405.htm · versión aceptada: https://openaccess.city.ac.uk/id/eprint/13781/
- **Acceso y licencia:** Versión de trabajo BIS y versión aceptada en City Research Online de acceso libre; versión JF de pago
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Menkhoff Sarno Schmeling Schrimpf "Information Flows in Foreign Exchange Markets: Dissecting Customer Currency Trades" Journal of Finance»; WebFetch: sí, IDEAS)
- **Contenido:** Con flujos de clientes finales de un gran banco en muchas divisas y por tipo de cliente (fondos de activos reales, apalancados, corporativos, privados), muestra que el flujo predice con fuerza los tipos de cambio y tiene valor económico, y que los grupos difieren en capacidad predictiva, estilo y exposición al riesgo.
- **Uso en el bloque:** TR-PFV: base para dar más peso a los flujos de fondos apalancados y de dinero real que a los corporativos; PROS: señal de flujos en horizontes H1–H2.
- **Limitaciones:** Datos propietarios de un banco; los flujos públicos agregados (bancos que publican flujos) son más ruidosos.

#### FXA-0205 · Q 90 (A) — How Is Macro News Transmitted to Exchange Rates?

- **Autores:** Martin D. D. Evans; Richard K. Lyons
- **Año:** 2008
- **Publicación o institución:** Journal of Financial Economics, vol. 88, págs. 26-50
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-06 Microestructura, flujo de órdenes y posicionamiento (principal) · secundarias: TX-02
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / URL:** https://faculty.haas.berkeley.edu/lyons/pubabs.html (índice de publicaciones del autor)
- **Acceso y licencia:** Artículo de pago (Elsevier); resumen libre en la página del autor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Evans Lyons 2002 "Order Flow and Exchange Rate Dynamics" Journal of Political Economy»; WebFetch: sí, índice Lyons/Haas)
- **Contenido:** Muestra que las noticias macroeconómicas afectan al tipo de cambio no solo de forma directa sino a través del flujo de órdenes que inducen, con un efecto indirecto que persiste tras la publicación.
- **Uso en el bloque:** TR-BCM y TR-PFV: interpretar la reacción a datos y decisiones de bancos centrales en horizontes H1; AS-G10N: análisis de eventos.
- **Limitaciones:** Datos interbancarios DM/USD de los noventa.

#### FXA-0202 · Q 90 (A) — The Microstructure Approach to Exchange Rates

- **Autores:** Richard K. Lyons
- **Año:** 2001
- **Publicación o institución:** MIT Press (Cambridge, MA), 333 págs.
- **Tipo de documento:** Libro (monografía académica de referencia)
- **Temática:** TX-06 Microestructura, flujo de órdenes y posicionamiento (principal) · secundarias: TX-01
- **Calidad Q:** 90 (A) — Tipo 23/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 6/10 · Impacto 10/10 · Independencia 10/10 · Acceso 8/10
- **DOI / URL:** https://faculty.haas.berkeley.edu/lyons/pubabs.html (página de publicaciones del autor, índice)
- **Acceso y licencia:** Libro comercial (MIT Press); el índice del autor ofrece resúmenes
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Evans Lyons 2002 "Order Flow and Exchange Rate Dynamics" Journal of Political Economy»; WebFetch: sí, índice https://faculty.haas.berkeley.edu/lyons/pubabs.html)
- **Contenido:** Manual que formaliza el enfoque de microestructura del mercado de divisas: papel de los creadores de mercado, información privada, flujo de órdenes como canal de agregación de información dispersa y modelos de «patata caliente» del interbancario.
- **Uso en el bloque:** TR-PFV y Analistas de segmento: marco conceptual para leer flujos de clientes, liquidez y posicionamiento; DOC-A: obra de cabecera del área.
- **Limitaciones:** Describe el mercado previo a la electronificación masiva (algoritmos, plataformas multibanco); los capítulos empíricos se basan en datos de los años noventa.

#### FXA-0209 · Q 89 (A) — Meese-Rogoff Redux: Micro-Based Exchange Rate Forecasting

- **Autores:** Martin D. D. Evans; Richard K. Lyons
- **Año:** 2005
- **Publicación o institución:** American Economic Review, vol. 95, págs. 405-414
- **Tipo de documento:** Artículo revisado por pares (Papers & Proceedings)
- **Temática:** TX-06 Microestructura, flujo de órdenes y posicionamiento (principal) · secundarias: TX-13
- **Calidad Q:** 89 (A) — Tipo 24/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 6/10 · Impacto 9/10 · Independencia 10/10 · Acceso 8/10
- **DOI / URL:** https://faculty.haas.berkeley.edu/lyons/pubabs.html (índice de publicaciones del autor)
- **Acceso y licencia:** Artículo de AEA (acceso según suscripción); resumen libre en la página del autor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Evans Lyons 2002 "Order Flow and Exchange Rate Dynamics" Journal of Political Economy»; WebFetch: sí, índice Lyons/Haas)
- **Contenido:** Muestra que el flujo de órdenes de clientes de un gran banco predice fuera de muestra los tipos de cambio a horizontes de días a un mes mejor que el paseo aleatorio y que los modelos macro estándar.
- **Uso en el bloque:** PROS y EVAL: precedente de previsión que bate al paseo aleatorio con información de flujos; TR-PFV: valor de los flujos de clientes publicados por bancos.
- **Limitaciones:** Flujos propietarios de un solo banco; resultados sensibles al periodo.

#### FXA-0204 · Q 88 (A) — OTC foreign exchange turnover in April 2025 (Triennial Central Bank Survey 2025)

- **Autores:** Banco de Pagos Internacionales (BPI/BIS), Departamento Monetario y Económico
- **Año:** 2025 (30 de septiembre)
- **Publicación o institución:** Bank for International Settlements, Triennial Central Bank Survey of Foreign Exchange and OTC Derivatives Markets
- **Tipo de documento:** Estadística oficial e informe de resultados de organismo internacional
- **Temática:** TX-06 Microestructura, flujo de órdenes y posicionamiento (principal) · secundarias: TX-12
- **Calidad Q:** 88 (A) — Tipo 21/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 7/10 · Acceso 8/10
- **DOI / URL:** https://www.bis.org/statistics/rpfx25_fx.htm · página general: https://bis.org/statistics/rpfx25.htm
- **Acceso y licencia:** Acceso abierto (BIS)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «BIS Triennial Central Bank Survey 2025 foreign exchange turnover April 2025 results»; WebFetch: sí)
- **Contenido:** Volumen diario medio de 9,6 billones de USD en abril de 2025 (+28 % frente a 2022); swaps 42 %, contado 31 %, forwards 19 %, opciones ~7 %; el USD está en el 89,2 % de las operaciones; Reino Unido (~38 %) y EE. UU. (~19 %) dominan, con Singapur al alza.
- **Uso en el bloque:** TR-PFV y Analistas de segmento: medida oficial de la liquidez relativa de cada divisa y centro (invertibilidad, regla de la divisa menos líquida); AS-ESTR: peso del dólar y de los swaps en la estructura del mercado.
- **Limitaciones:** Foto trienal de un solo mes (abril); datos preliminares sujetos a revisión; no recoge flujos por tipo de inversor final con detalle.

#### FXA-0206 · Q 88 (A) — Is There Private Information in the FX Market? The Tokyo Experiment

- **Autores:** Takatoshi Ito; Richard K. Lyons; Michael T. Melvin
- **Año:** 1998
- **Publicación o institución:** Journal of Finance, junio de 1998, págs. 1111-1130
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-06 Microestructura, flujo de órdenes y posicionamiento (principal) · secundarias: —
- **Calidad Q:** 88 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 5/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / URL:** https://faculty.haas.berkeley.edu/lyons/pubabs.html (índice de publicaciones del autor)
- **Acceso y licencia:** Artículo de pago (Wiley); resumen libre en la página del autor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Evans Lyons 2002 "Order Flow and Exchange Rate Dynamics" Journal of Political Economy»; WebFetch: sí, índice Lyons/Haas)
- **Contenido:** Aprovecha la apertura de la negociación en Tokio a la hora del almuerzo como experimento natural para mostrar que la volatilidad se debe en parte a información privada revelada por la negociación, no solo a noticias públicas.
- **Uso en el bloque:** TR-PFV: justificar que los flujos contienen información; AS-EMAS: estacionalidad intradía en sesiones asiáticas.
- **Limitaciones:** Episodio institucional concreto de los noventa.

#### FXA-0203 · Q 86 (A) — Foreign Exchange Market Structure, Players and Evolution

- **Autores:** Michael R. King; Carol Osler; Dagfinn Rime
- **Año:** 2011 (documento de trabajo; publicado después como capítulo de libro, 2012)
- **Publicación o institución:** Norges Bank Working Papers 10/2011 (45 págs.)
- **Tipo de documento:** Documento de trabajo de banco central (survey)
- **Temática:** TX-06 Microestructura, flujo de órdenes y posicionamiento (principal) · secundarias: —
- **Calidad Q:** 86 (A) — Tipo 20/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 9/10 · Independencia 9/10 · Acceso 9/10
- **DOI / URL:** Handle: http://hdl.handle.net/11250/2496951 · https://norges-bank.brage.unit.no/norges-bank-xmlui/handle/11250/2496951 · índice IDEAS: https://ideas.repec.org/p/bno/worpap/2011_10.html
- **Acceso y licencia:** Acceso abierto (repositorio de Norges Bank)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «King Osler Rime 2012 "Foreign exchange market structure, players and evolution"»; WebFetch: sí, registro completo Brage)
- **Contenido:** Describe los participantes del mercado de divisas (bancos creadores de mercado, clientes financieros y corporativos, minoristas, operadores de alta frecuencia, creadores no bancarios) y cómo la negociación electrónica redujo costes, triplicó volúmenes y aumentó la concentración de los intermediarios.
- **Uso en el bloque:** TR-PFV: mapa de quién mueve los flujos y cómo se forma el precio; Analistas de segmento: valoración de la liquidez y de la profundidad al juzgar la invertibilidad.
- **Limitaciones:** Datos hasta 2010; el ecosistema de liquidez ha cambiado después (internalización, plataformas, fijaciones).

#### FXA-0207 · Q 86 (A) — Tests of Microstructural Hypotheses in the Foreign Exchange Market

- **Autores:** Richard K. Lyons
- **Año:** 1995
- **Publicación o institución:** Journal of Financial Economics, octubre de 1995, págs. 321-351
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-06 Microestructura, flujo de órdenes y posicionamiento (principal) · secundarias: —
- **Calidad Q:** 86 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 4/10 · Impacto 9/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** https://faculty.haas.berkeley.edu/lyons/pubabs.html (índice de publicaciones del autor)
- **Acceso y licencia:** Artículo de pago (Elsevier)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Evans Lyons 2002 "Order Flow and Exchange Rate Dynamics" Journal of Political Economy»; WebFetch: sí, índice Lyons/Haas)
- **Contenido:** Con datos de un operador interbancario, contrasta los canales de inventario e información en la fijación de precios del creador de mercado de divisas, documentando ambos efectos.
- **Uso en el bloque:** TR-PFV: base empírica del efecto precio del flujo de órdenes y de la gestión de inventarios de los intermediarios.
- **Limitaciones:** Un solo operador y una semana de datos; mercado anterior a la electronificación.

#### FXA-0208 · Q 85 (A) — A Simultaneous Trade Model of the Foreign Exchange Hot Potato

- **Autores:** Richard K. Lyons
- **Año:** 1997
- **Publicación o institución:** Journal of International Economics, mayo de 1997, págs. 275-298
- **Tipo de documento:** Artículo revisado por pares (teórico)
- **Temática:** TX-06 Microestructura, flujo de órdenes y posicionamiento (principal) · secundarias: —
- **Calidad Q:** 85 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 4/10 · Impacto 8/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** https://faculty.haas.berkeley.edu/lyons/pubabs.html (índice de publicaciones del autor)
- **Acceso y licencia:** Artículo de pago (Elsevier)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Evans Lyons 2002 "Order Flow and Exchange Rate Dynamics" Journal of Political Economy»; WebFetch: sí, índice Lyons/Haas)
- **Contenido:** Modela la «patata caliente» del interbancario: el reparto de inventarios entre creadores de mercado multiplica el volumen y reduce la información que transmite el volumen interbancario.
- **Uso en el bloque:** TR-PFV: cautela al interpretar volumen bruto como señal; distinguir flujo de clientes finales del interbancario.
- **Limitaciones:** Modelo teórico estilizado.

#### FXA-0217 · Q 84 (A) — Rise of the Machines: Algorithmic Trading in the Foreign Exchange Market

- **Autores:** Alain Chaboud; Benjamin Chiquoine; Erik Hjalmarsson; Clara Vega
- **Año:** 2009 (documento de trabajo; versión revisada publicada en revista en 2014)
- **Publicación o institución:** Board of Governors of the Federal Reserve System, International Finance Discussion Papers n.º 980 (octubre de 2009)
- **Tipo de documento:** Documento de trabajo de banco central
- **Temática:** TX-06 Microestructura, flujo de órdenes y posicionamiento (principal) · secundarias: —
- **Calidad Q:** 84 (A) — Tipo 19/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 6/10 · Impacto 9/10 · Independencia 8/10 · Acceso 9/10
- **DOI / URL:** https://federalreserve.gov/econres/ifdp/rise-of-the-machines-algorithmic-trading-in-the-foreign-exchange-market.htm · PDF: https://www.federalreserve.gov/PubS/ifdp/2009/980/ifdp980.pdf
- **Acceso y licencia:** Acceso abierto (Reserva Federal)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Chaboud Chiquoine Hjalmarsson Vega "Rise of the Machines: Algorithmic Trading in the Foreign Exchange Market"»; WebFetch: sí)
- **Contenido:** Con datos de EBS (2006-2007) en EUR/USD, USD/JPY y EUR/JPY, encuentra que las operaciones algorítmicas están correlacionadas pero no elevan la volatilidad, se retiran en el minuto posterior a los datos macro y aportan liquidez en la hora siguiente; el flujo no algorítmico explica más varianza de los rendimientos.
- **Uso en el bloque:** TR-PFV: liquidez en torno a publicaciones y riesgo de huecos de liquidez en H1; AS-G10N: análisis de eventos de datos.
- **Limitaciones:** Periodo previo a la expansión de la alta frecuencia; la página no recoge la referencia de la versión publicada.

#### FXA-0214 · Q 84 (A) — Time-Varying Liquidity in Foreign Exchange

- **Autores:** Martin D. D. Evans; Richard K. Lyons
- **Año:** 2002
- **Publicación o institución:** Journal of Monetary Economics, vol. 49, n.º 5, págs. 1025-1051
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-06 Microestructura, flujo de órdenes y posicionamiento (principal) · secundarias: —
- **Calidad Q:** 84 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 5/10 · Impacto 7/10 · Independencia 10/10 · Acceso 4/10
- **DOI / URL:** https://faculty.haas.berkeley.edu/lyons/pubabs.html (índice de publicaciones del autor)
- **Acceso y licencia:** Artículo de pago (Elsevier)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Evans Lyons 2002 "Order Flow and Exchange Rate Dynamics" Journal of Political Economy»; WebFetch: sí, índice Lyons/Haas)
- **Contenido:** Documenta que el impacto en precio del flujo de órdenes varía en el tiempo y aumenta con la llegada de noticias, de modo que la liquidez del mercado de divisas no es constante.
- **Uso en el bloque:** TR-PFV: ajustar la lectura de flujos según el régimen de liquidez y la agenda de datos.
- **Limitaciones:** Mercado y datos de los noventa.

#### FXA-0210 · Q 82 (A) — Order flows, news, and exchange rate volatility

- **Autores:** Michael Frömmel; Alexander Mende; Lukas Menkhoff
- **Año:** 2008
- **Publicación o institución:** Journal of International Money and Finance, vol. 27, n.º 6 (octubre), págs. 994-1012 (Elsevier)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-06 Microestructura, flujo de órdenes y posicionamiento (principal) · secundarias: —
- **Calidad Q:** 82 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 12/15 · Vigencia 6/10 · Impacto 7/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** https://ideas.repec.org/a/eee/jimfin/v27y2008i6p994-1012.html
- **Acceso y licencia:** Ficha y resumen libres en IDEAS; texto de pago (ScienceDirect)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Dagfinn Rime IDEAS RePEc author page foreign exchange order flow»; WebFetch: sí)
- **Contenido:** Con datos de alta frecuencia EUR/USD de un banco, solo las operaciones grandes de clientes financieros y bancos (informadas) explican la volatilidad; el flujo de clientes comerciales no, incluso controlando por noticias.
- **Uso en el bloque:** TR-PFV: distinguir flujos informados (dinero real, fondos) de flujos comerciales al interpretar volatilidad y posicionamiento.
- **Limitaciones:** Cuatro meses de datos de un solo banco.

#### FXA-0211 · Q 80 (A) — An investigation of customer order flow in the foreign exchange market

- **Autores:** Mario Cerrato; Nicholas Sarantis; Alex Saunders
- **Año:** 2011
- **Publicación o institución:** Journal of Banking & Finance, vol. 35, n.º 8, págs. 1892-1906 (Elsevier)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-06 Microestructura, flujo de órdenes y posicionamiento (principal) · secundarias: TX-13
- **Calidad Q:** 80 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 11/15 · Vigencia 7/10 · Impacto 6/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** https://ideas.repec.org/a/eee/jbfina/v35y2011i8p1892-1906.html
- **Acceso y licencia:** Ficha libre en IDEAS; texto de pago
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Dagfinn Rime IDEAS RePEc author page foreign exchange order flow»; WebFetch: sí)
- **Contenido:** Con flujo neto semanal por tipo de cliente en nueve pares líquidos, analiza si el flujo de clientes explica y predice el tipo de cambio más allá de las variables macro y si sus previsiones fuera de muestra son explotables.
- **Uso en el bloque:** TR-PFV y PROS: evidencia a horizonte semanal (H2) sobre el valor de los flujos segmentados por tipo de cliente.
- **Limitaciones:** Datos propietarios de un banco; resumen leído, no el texto completo.

#### FXA-0218 · Q 80 (A) — Currency orders and exchange-rate dynamics: explaining the success of technical analysis

- **Autores:** Carol Osler
- **Año:** 2001 (Staff Report; versión publicada en revista posteriormente)
- **Publicación o institución:** Federal Reserve Bank of New York, Staff Reports n.º 125
- **Tipo de documento:** Documento de trabajo de banco central
- **Temática:** TX-06 Microestructura, flujo de órdenes y posicionamiento (principal) · secundarias: TX-05
- **Calidad Q:** 80 (A) — Tipo 19/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 5/10 · Impacto 8/10 · Independencia 8/10 · Acceso 9/10
- **DOI / URL:** https://econpapers.repec.org/RePEc:fip:fednsr:125 · https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr125.html
- **Acceso y licencia:** Acceso abierto (Fed de Nueva York)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Osler "Currency Orders and Exchange Rate Dynamics" stop-loss take-profit Journal of Finance 2003»; WebFetch: sí, EconPapers)
- **Contenido:** Con órdenes stop-loss y take-profit de un gran banco, muestra que las take-profit frenan las tendencias y las stop-loss las aceleran, y que su concentración en números redondos explica por qué los soportes y resistencias funcionan.
- **Uso en el bloque:** TR-PFV y AS-ESTR: fundamento microestructural de niveles técnicos y de aceleraciones al romperlos; CONTRA: riesgo de cascadas.
- **Limitaciones:** Datos de órdenes de un solo banco (2000); estructura de órdenes actual distinta.

#### FXA-0219 · Q 78 (B) — Stop-loss orders and price cascades in currency markets

- **Autores:** Carol Osler
- **Año:** 2002 (Staff Report; artículo con el mismo título fechado en 2005)
- **Publicación o institución:** Federal Reserve Bank of New York, Staff Reports n.º 150
- **Tipo de documento:** Documento de trabajo de banco central
- **Temática:** TX-06 Microestructura, flujo de órdenes y posicionamiento (principal) · secundarias: TX-09
- **Calidad Q:** 78 (B) — Tipo 18/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 5/10 · Impacto 7/10 · Independencia 8/10 · Acceso 9/10
- **DOI / URL:** https://econpapers.repec.org/RePEc:fip:fednsr:150
- **Acceso y licencia:** Acceso abierto
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Osler "Currency Orders and Exchange Rate Dynamics" stop-loss take-profit Journal of Finance 2003»; WebFetch: sí)
- **Contenido:** Las órdenes stop-loss generan realimentación positiva y cascadas de precios: las tendencias son más rápidas cerca de los niveles donde se agrupan, con efectos significativos en horas; mecanismo candidato para las colas gruesas de los rendimientos cambiarios.
- **Uso en el bloque:** TR-PFV y CONTRA: riesgo de movimientos bruscos en H1 cerca de niveles con órdenes acumuladas.
- **Limitaciones:** Efectos de horas, no de días; la página no detalla la revista de la versión publicada.

#### FXA-0213 · Q 76 (B) — An Empirical Study of Liquidity and Information Effects of Order Flow on Exchange Rates

- **Autores:** Francis Breedon; Paolo Vitale
- **Año:** 2004
- **Publicación o institución:** CEPR Discussion Paper n.º 4586 · también ECB Working Paper Series n.º 424
- **Tipo de documento:** Documento de trabajo (CEPR/BCE)
- **Temática:** TX-06 Microestructura, flujo de órdenes y posicionamiento (principal) · secundarias: TX-08
- **Calidad Q:** 76 (B) — Tipo 18/25 · Rigor 17/20 · Autoridad 12/15 · Vigencia 5/10 · Impacto 7/10 · Independencia 9/10 · Acceso 8/10
- **DOI / URL:** https://ideas.repec.org:443/p/cpr/ceprdp/4586.html
- **Acceso y licencia:** Ficha libre en IDEAS; versión BCE de acceso abierto
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Dagfinn Rime IDEAS RePEc author page foreign exchange order flow»; WebFetch: sí)
- **Contenido:** Modelo estructural (a partir de Bacchetta-van Wincoop) que separa efectos de liquidez e información del flujo de órdenes; con todas las operaciones EUR/USD de EBS y Reuters (2000-2001) la correlación flujo-precio se debe sobre todo a liquidez, también en cuatro episodios de intervención.
- **Uso en el bloque:** TR-PFV: cautela al leer el flujo como información; TR-BCM: efecto de la intervención vía flujo.
- **Limitaciones:** Seis meses de datos de un solo par.

#### FXA-0220 · Q 76 (B) — Foreign Exchange: Macro Puzzles, Micro Tools

- **Autores:** Richard K. Lyons
- **Año:** 2002
- **Publicación o institución:** Economic Review, Federal Reserve Bank of San Francisco, págs. 51-69
- **Tipo de documento:** Artículo de revista de banco central (divulgación técnica / survey)
- **Temática:** TX-06 Microestructura, flujo de órdenes y posicionamiento (principal) · secundarias: TX-01
- **Calidad Q:** 76 (B) — Tipo 17/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 5/10 · Impacto 7/10 · Independencia 9/10 · Acceso 9/10
- **DOI / URL:** https://faculty.haas.berkeley.edu/lyons/pubabs.html (índice de publicaciones del autor)
- **Acceso y licencia:** Publicación de banco central de acceso libre
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Evans Lyons 2002 "Order Flow and Exchange Rate Dynamics" Journal of Political Economy»; WebFetch: sí, índice Lyons/Haas)
- **Contenido:** Síntesis accesible de cómo las herramientas de microestructura (flujo de órdenes) ayudan a resolver los enigmas macro del tipo de cambio (desconexión, fracaso predictivo).
- **Uso en el bloque:** DOC-A y Analistas de segmento: introducción rápida al enfoque de flujos antes de las obras técnicas.
- **Limitaciones:** Texto divulgativo; sin datos nuevos.

#### FXA-0221 · Q 74 (B) — New Perspective on FX Markets: Order-Flow Analysis

- **Autores:** Richard K. Lyons
- **Año:** 2001
- **Publicación o institución:** International Finance, verano de 2001, págs. 303-320
- **Tipo de documento:** Artículo revisado por pares (ensayo)
- **Temática:** TX-06 Microestructura, flujo de órdenes y posicionamiento (principal) · secundarias: —
- **Calidad Q:** 74 (B) — Tipo 22/25 · Rigor 13/20 · Autoridad 14/15 · Vigencia 4/10 · Impacto 7/10 · Independencia 10/10 · Acceso 4/10
- **DOI / URL:** https://faculty.haas.berkeley.edu/lyons/pubabs.html (índice de publicaciones del autor)
- **Acceso y licencia:** Artículo de pago (Wiley)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Evans Lyons 2002 "Order Flow and Exchange Rate Dynamics" Journal of Political Economy»; WebFetch: sí, índice Lyons/Haas)
- **Contenido:** Ensayo que presenta el análisis de flujo de órdenes como nueva perspectiva sobre los mercados de divisas y sus implicaciones para la determinación del tipo de cambio.
- **Uso en el bloque:** DOC-A: lectura introductoria complementaria a FXA-0202.
- **Limitaciones:** Solapa en parte con FXA-0202 y FXA-0220.

#### FXA-0222 · Q 72 (B) — The Future of the Foreign Exchange Market

- **Autores:** Richard K. Lyons
- **Año:** 2002
- **Publicación o institución:** En Robert Litan y Richard Herring (eds.), Brookings-Wharton Papers on Financial Services, Brookings Institution Press, págs. 253-280
- **Tipo de documento:** Capítulo de volumen académico
- **Temática:** TX-06 Microestructura, flujo de órdenes y posicionamiento (principal) · secundarias: —
- **Calidad Q:** 72 (B) — Tipo 19/25 · Rigor 13/20 · Autoridad 14/15 · Vigencia 4/10 · Impacto 6/10 · Independencia 10/10 · Acceso 6/10
- **DOI / URL:** https://faculty.haas.berkeley.edu/lyons/pubabs.html (índice de publicaciones del autor)
- **Acceso y licencia:** Volumen de Brookings; acceso variable
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Evans Lyons 2002 "Order Flow and Exchange Rate Dynamics" Journal of Political Economy»; WebFetch: sí, índice Lyons/Haas)
- **Contenido:** Analiza la evolución estructural del mercado de divisas (electronificación, intermediación, plataformas) y anticipa cambios en el papel de los creadores de mercado.
- **Uso en el bloque:** TR-PFV: contexto histórico de la estructura del mercado; complemento de FXA-0203 y FXA-0204.
- **Limitaciones:** Prospectiva de 2002, superada en parte por los hechos.

#### FXA-0212 · Q 70 (B) — Foreign exchange customers and dealers: Who's driving whom?

- **Autores:** Nikola Gradojevic
- **Año:** 2014
- **Publicación o institución:** Finance Research Letters, vol. 11, n.º 3, págs. 213-218 (Elsevier) · versión previa: IESEG WP 2013-FIN-03
- **Tipo de documento:** Artículo revisado por pares (nota breve)
- **Temática:** TX-06 Microestructura, flujo de órdenes y posicionamiento (principal) · secundarias: —
- **Calidad Q:** 70 (B) — Tipo 21/25 · Rigor 14/20 · Autoridad 9/15 · Vigencia 7/10 · Impacto 4/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** DOI: 10.1016/j.frl.2013.11.005 · https://ideas.repec.org/a/eee/finlet/v11y2014i3p213-218.html
- **Acceso y licencia:** Ficha libre en IDEAS; texto de pago; versión de trabajo listada en IDEAS
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Dagfinn Rime IDEAS RePEc author page foreign exchange order flow»; WebFetch: sí)
- **Contenido:** Análisis en el dominio de la frecuencia de la interacción entre operadores y clientes: el flujo de los intermediarios anticipa el de los clientes a frecuencias superiores a una semana y la interacción se concentra en episodios de inestabilidad.
- **Uso en el bloque:** TR-PFV: matiz sobre la causalidad entre flujos de intermediarios y de clientes.
- **Limitaciones:** Nota breve; evidencia de alcance limitado.

#### FXA-0215 · Q 70 (B) — Customer Trades and Extreme Events in Foreign Exchange

- **Autores:** Mintao Fan; Richard K. Lyons
- **Año:** 2003
- **Publicación o institución:** En Paul Mizen (ed.), Monetary History, Exchange Rates and Financial Markets: Essays in Honour of Charles Goodhart, Edward Elgar, págs. 160-179
- **Tipo de documento:** Capítulo de libro académico
- **Temática:** TX-06 Microestructura, flujo de órdenes y posicionamiento (principal) · secundarias: TX-09
- **Calidad Q:** 70 (B) — Tipo 18/25 · Rigor 15/20 · Autoridad 13/15 · Vigencia 4/10 · Impacto 6/10 · Independencia 10/10 · Acceso 4/10
- **DOI / URL:** https://ideas.repec.org/h/elg/eechap/2818_6.html · índice: https://faculty.haas.berkeley.edu/lyons/pubabs.html
- **Acceso y licencia:** Capítulo de pago (Edward Elgar)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Dagfinn Rime IDEAS RePEc author page foreign exchange order flow»; WebFetch: sí, índice Lyons/Haas)
- **Contenido:** Analiza los flujos de clientes de un gran banco por tipo de cliente en relación con episodios extremos del mercado de divisas, para ver qué tipos de cliente absorben o amplifican los movimientos (según título y contexto del volumen; texto no leído).
- **Uso en el bloque:** TR-PFV y CONTRA: conducta de los distintos tipos de cliente en episodios de cola y deshacer posiciones.
- **Limitaciones:** Capítulo de libro; datos de un banco.

## TX-07 Balanza de pagos, flujos de capital y ciclo financiero global

#### ANA-DOC-0361 · Q 92 (A) — U.S. Monetary Policy and the Global Financial Cycle

- **Autores:** Silvia Miranda-Agrippino; Hélène Rey
- **Año:** 2020
- **Publicación o institución:** The Review of Economic Studies, vol. 87, n.º 6, págs. 2754-2776
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-07 Balanza de pagos, flujos de capital y ciclo financiero global (principal) · secundarias: TX-02, TX-10
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 4/10
- **DOI / URL:** https://ideas.repec.org/a/oup/restud/v87y2020i6p2754-2776..html
- **Acceso y licencia:** Peldaño 3 (OUP; versiones de trabajo NBER/CEPR) · Licencia: Copyright OUP
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Hélène Rey IDEAS RePEc author page publications»; WebFetch: sí, sobre la página de autora de IDEAS que lista la obra; ficha individual no accesible para la herramienta)
- **Contenido:** Contraste empírico formal de que la política monetaria de EE. UU. mueve el ciclo financiero global (precios de activos de riesgo, apalancamiento bancario, crédito y flujos de capital) en todo el mundo.
- **Uso en el bloque:** TR-BCM: transmisión de la política de la Fed a flujos, crédito y precios de riesgo globales; Analistas de segmento emergentes: complemento empírico de ANA-DOC-0303 para anticipar presiones sobre las divisas ante sorpresas de la Fed.
- **Limitaciones:** Resumen no leído en esta carga.

#### ANA-DOC-0303 · Q 92 (A) — Dilemma not Trilemma: The Global Financial Cycle and Monetary Policy Independence

- **Autores:** Hélène Rey
- **Año:** 2013 (Jackson Hole); NBER Working Paper 21162 (2015, rev. 2018)
- **Publicación o institución:** National Bureau of Economic Research (NBER WP 21162); ponencia del Economic Policy Symposium de Jackson Hole
- **Tipo de documento:** Documento de trabajo institucional
- **Temática:** TX-07 Balanza de pagos, flujos de capital y ciclo financiero global (principal) · secundarias: TX-08, TX-02
- **Calidad Q:** 92 (A) — Tipo 20/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 10/10
- **DOI / URL:** DOI 10.3386/w21162 · https://www.nber.org/papers/w21162
- **Acceso y licencia:** Peldaño 1 (PDF del NBER y copia en LBS Research Online) · Licencia: Copyright de la autora; lectura libre
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Hélène Rey "Dilemma not Trilemma: The Global Financial Cycle and Monetary Policy Independence" NBER 21162»; WebFetch: sí)
- **Contenido:** Documenta un ciclo financiero global de flujos de capital, precios de activos y crédito, correlacionado con el VIX e impulsado en parte por la política monetaria del centro (EE. UU.); con libre movilidad de capital el trilema se convierte en dilema, con independencia del régimen cambiario.
- **Uso en el bloque:** TR-BCM (AG-09): marco del régimen global (Fed, VIX, flujos) que condiciona a todas las divisas; AS-EMLA, AS-EMAS y AS-EMEA: lectura del contagio del ciclo financiero global aunque haya flotación; CONTRA: objeción de «independencia monetaria» ilusoria en emergentes.
- **Limitaciones:** Evidencia VAR sujeta a identificación; la intensidad del ciclo global varía entre periodos.

#### FXA-0278 · Q 91 (A) — Capital flows and the risk-taking channel of monetary policy

- **Autores:** Valentina Bruno; Hyun Song Shin
- **Año:** 2015 (BIS WP 400 de 2012; NBER WP 18942 de 2013)
- **Publicación o institución:** Journal of Monetary Economics, vol. 71, págs. 119-132
- **Tipo de documento:** Artículo revisado por pares (con documentos de trabajo BIS y NBER)
- **Temática:** TX-07 Balanza de pagos, flujos de capital y ciclo financiero global (principal) · secundarias: TX-02, TX-10
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 10/10 · Independencia 9/10 · Acceso 6/10
- **DOI / URL:** DOI (WP NBER): 10.3386/w18942 · https://www.nber.org/papers/w18942.marc · versión BIS: https://econpapers.repec.org/RePEc:bis:biswps:400
- **Acceso y licencia:** Documentos de trabajo BIS y NBER de acceso libre; artículo de pago (Elsevier)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Bruno Shin "Capital flows and the risk-taking channel of monetary policy" "Cross-border banking and global liquidity"»; WebFetch: sí, registro NBER y EconPapers)
- **Contenido:** Canal internacional de toma de riesgos: tipos bajos en el centro abaratan la financiación de los bancos globales, aumentan su apalancamiento y los flujos bancarios transfronterizos hacia emergentes, y la apreciación resultante reduce el riesgo medido y realimenta el ciclo.
- **Uso en el bloque:** TR-BCM y TR-PFV: mecanismo por el que la Fed y el dólar mueven flujos y divisas emergentes; AS-ESTR: base del vínculo dólar débil-apetito por el riesgo.
- **Limitaciones:** VAR con datos agregados; canal bancario menos dominante tras 2010 (auge de bonos y fondos).

#### FXA-0279 · Q 90 (A) — Cross-Border Banking and Global Liquidity

- **Autores:** Valentina Bruno; Hyun Song Shin
- **Año:** 2015
- **Publicación o institución:** Review of Economic Studies, vol. 82, págs. 535-564
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-07 Balanza de pagos, flujos de capital y ciclo financiero global (principal) · secundarias: TX-12
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 10/10 · Independencia 10/10 · Acceso 4/10
- **DOI / URL:** índice: https://www.federalreserve.gov/econres/ifdp/files/ifdp1241.pdf (bibliografía)
- **Acceso y licencia:** Artículo de pago (OUP); versiones de trabajo del BPI y de Princeton
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Bruno Shin "Capital flows and the risk-taking channel of monetary policy" "Cross-border banking and global liquidity"»; WebFetch: sí, índice: bibliografía de Correa et al., IFDP 1241, https://www.federalreserve.gov/econres/ifdp/files/ifdp1241.pdf)
- **Contenido:** Modelo de liquidez global en dos niveles (bancos globales que prestan a bancos locales) en el que el apalancamiento de los bancos globales, ligado al VIX y al dólar, impulsa los flujos bancarios transfronterizos.
- **Uso en el bloque:** TR-PFV: liquidez global y flujos bancarios como determinante común de las divisas emergentes; TR-BCM: lectura del VIX y del dólar como variables de estado.
- **Limitaciones:** Verificada por bibliografía de un tercero; texto no leído.

#### ANA-DOC-0363 · Q 90 (A) — Capital Flow Waves: Surges, Stops, Flight, and Retrenchment

- **Autores:** Kristin J. Forbes; Francis E. Warnock
- **Año:** 2012 (NBER WP 17351 de 2011)
- **Publicación o institución:** Journal of International Economics, vol. 88, n.º 2, págs. 235-251
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-07 Balanza de pagos, flujos de capital y ciclo financiero global (principal) · secundarias: TX-09, TX-10
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 10/10 · Independencia 10/10 · Acceso 4/10
- **DOI / URL:** https://ideas.repec.org/p/nbr/nberwo/17351.html · versión de conferencia: https://www.newyorkfed.org/medialibrary/media/research/conference/2011/global_sys_risk/Capital_Flow_Waves_Surges_Stops_Flight_Retrenchment.pdf
- **Acceso y licencia:** Peldaño 2 (WP NBER y copia en el NY Fed) · Licencia: Copyright Elsevier/autores
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Kristin Forbes Warnock "Capital flow waves" IDEAS RePEc Journal of International Economics»; WebFetch: sí)
- **Contenido:** Con flujos brutos identifica episodios de «surges», «stops», «flight» y «retrenchment»; el riesgo global y el contagio explican los episodios extremos más que los fundamentales domésticos; los controles de capital apenas influyen.
- **Uso en el bloque:** TR-PFV y TR-BCM: tipología de episodios extremos de flujos brutos (surges, stops, flight, retrenchment) y su vínculo con el riesgo global; AS-EMLA, AS-EMAS, AS-EMEA: señales de parada súbita y su impacto en la divisa.
- **Limitaciones:** Actualizado en ANA-DOC-0366 (después de 2008 los episodios son menos globales).

#### FXA-0238 · Q 88 (A) — Does the Current Account Still Matter?

- **Autores:** Maurice Obstfeld
- **Año:** 2012
- **Publicación o institución:** American Economic Review, vol. 102, n.º 3, págs. 1-23 (Richard T. Ely Lecture)
- **Tipo de documento:** Artículo revisado (conferencia Ely de la AEA)
- **Temática:** TX-07 Balanza de pagos, flujos de capital y ciclo financiero global (principal) · secundarias: TX-09, TX-03
- **Calidad Q:** 88 (A) — Tipo 23/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 9/10 · Independencia 10/10 · Acceso 7/10
- **DOI / URL:** https://ideas.repec.org/a/aea/aecrev/v102y2012i3p1-23.html
- **Acceso y licencia:** Ficha libre en IDEAS; artículo AEA (versión NBER de libre acceso)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Maurice Obstfeld IDEAS RePEc author page»; WebFetch: sí, índice https://ideas.repec.org:443/e/pob13.html)
- **Contenido:** Defiende que, pese a la globalización financiera, los grandes déficits por cuenta corriente siguen siendo señales de riesgo y que los flujos y posiciones brutas (no solo netos) son claves para la estabilidad financiera y cambiaria.
- **Uso en el bloque:** TR-BCM y Analistas de segmento: justificar el uso conjunto de cuenta corriente, balanza básica y posiciones brutas en la lente de flujos.
- **Limitaciones:** Ensayo de síntesis; resumen no leído en esta carga.

#### FXA-0281 · Q 88 (A) — Capital flows, push versus pull factors and the global financial crisis

- **Autores:** Marcel Fratzscher
- **Año:** 2012
- **Publicación o institución:** Journal of International Economics, vol. 88, n.º 2, págs. 341-356
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-07 Balanza de pagos, flujos de capital y ciclo financiero global (principal) · secundarias: TX-10
- **Calidad Q:** 88 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 14/15 · Vigencia 8/10 · Impacto 9/10 · Independencia 10/10 · Acceso 4/10
- **DOI / URL:** índice: https://www.federalreserve.gov/econres/ifdp/files/ifdp1241.pdf (bibliografía)
- **Acceso y licencia:** Artículo de pago (Elsevier); versión de trabajo del BCE
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Bruno Shin "Capital flows and the risk-taking channel of monetary policy" "Cross-border banking and global liquidity"»; WebFetch: sí, índice: bibliografía de Correa et al., IFDP 1241, https://www.federalreserve.gov/econres/ifdp/files/ifdp1241.pdf)
- **Contenido:** Con flujos de fondos de cartera por país, muestra que los factores comunes (push: riesgo y liquidez globales) dominaron los flujos durante la crisis de 2008, mientras que los factores propios del país (pull: fundamentos, instituciones) explicaron más la recuperación posterior y su heterogeneidad.
- **Uso en el bloque:** TR-PFV y Analistas de segmento emergentes: ponderar push frente a pull según el régimen de riesgo global.
- **Limitaciones:** Verificada por bibliografía de un tercero; texto no leído.

#### ANA-DOC-0311 · Q 86 (A) — The External Wealth of Nations Revisited: International Financial Integration in the Aftermath of the Global Financial Crisis

- **Autores:** Philip R. Lane; Gian Maria Milesi-Ferretti
- **Año:** 2018
- **Publicación o institución:** IMF Economic Review, vol. 66, n.º 1, págs. 189-222 (versión de trabajo: IMF Working Paper 17/115)
- **Tipo de documento:** Artículo revisado por pares con base de datos asociada
- **Temática:** TX-07 Balanza de pagos, flujos de capital y ciclo financiero global (principal) · secundarias: TX-03, TX-12
- **Calidad Q:** 86 (A) — Tipo 24/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 9/10 · Independencia 9/10 · Acceso 4/10
- **DOI / URL:** DOI 10.1057/s41308-017-0048-y · https://econpapers.repec.org/article/palimfecr/v_3a66_3ay_3a2018_3ai_3a1_3ad_3a10.1057_5fs41308-017-0048-y.htm · versión de trabajo: https://imf.org/~/media/Files/Publications/WP/2017/wp17115.ashx
- **Acceso y licencia:** Peldaño 2 (WP del FMI abierto; artículo de pago) · Licencia: Copyright FMI/Palgrave
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Lane Milesi-Ferretti "The External Wealth of Nations Revisited…" IMF Economic Review 2018»; WebFetch: sí)
- **Contenido:** Actualiza la base de activos y pasivos exteriores (posiciones de inversión internacional) y describe la integración financiera tras la crisis de 2008: estancamiento de posiciones brutas, auge de centros financieros y cambio en la composición de pasivos.
- **Uso en el bloque:** TR-BCM y Analistas de segmento: posición de inversión internacional neta y composición de pasivos exteriores (deuda frente a acciones, divisa) como fundamental de vulnerabilidad cambiaria; AS-ESTR: base para cestas por posición exterior.
- **Limitaciones:** Datos actualizados en versiones posteriores de la base EWN.

#### FXA-0223 · Q 86 (A) — Capital Flow Bonanzas: An Encompassing View of the Past and Present

- **Autores:** Carmen M. Reinhart; Vincent R. Reinhart
- **Año:** 2009 (CEPR DP 6996 de 2008)
- **Publicación o institución:** NBER International Seminar on Macroeconomics, vol. 5, n.º 1, págs. 9-62 (University of Chicago Press)
- **Tipo de documento:** Artículo revisado (volumen de conferencia NBER)
- **Temática:** TX-07 Balanza de pagos, flujos de capital y ciclo financiero global (principal) · secundarias: TX-09, TX-10
- **Calidad Q:** 86 (A) — Tipo 23/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 9/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** https://ideas.repec.org/a/ucp/intsma/doi10.1086-595995.html · versión de trabajo: https://ideas.repec.org/p/cpr/ceprdp/6996.html
- **Acceso y licencia:** Ficha libre en IDEAS; texto de pago (UCP); versión CEPR para miembros
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Carmen Reinhart IDEAS RePEc profile research papers»; WebFetch: sí, índice https://ideas.repec.org/e/pre33.html)
- **Contenido:** Define y fecha «bonanzas» de entradas de capital (grandes déficits por cuenta corriente) en muchos países desde la posguerra y muestra que tienden a preceder crisis cambiarias, bancarias y de deuda, sobre todo en economías emergentes.
- **Uso en el bloque:** TR-PFV y Analistas de segmento emergentes: señal de alerta cuando una divisa se aprecia con entradas masivas; CONTRA: riesgo de giro tras la bonanza.
- **Limitaciones:** Fechado anual; la frontera entre bonanza y financiación sana es discutible.

#### ANA-DOC-0369 · Q 86 (A) — Exchange Rates, Equity Prices, and Capital Flows

- **Autores:** Harald Hau; Hélène Rey
- **Año:** 2006
- **Publicación o institución:** Review of Financial Studies, vol. 19, n.º 1, págs. 273-317
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-07 Balanza de pagos, flujos de capital y ciclo financiero global (principal) · secundarias: TX-06
- **Calidad Q:** 86 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 8/10 · Independencia 10/10 · Acceso 3/10
- **DOI / URL:** https://ideas.repec.org/a/oup/rfinst/v19y2006i1p273-317.html
- **Acceso y licencia:** Peldaño 3 (OUP) · Licencia: Copyright OUP
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Hélène Rey IDEAS RePEc author page publications»; WebFetch: sí, sobre la página de autora de IDEAS que lista la obra)
- **Contenido:** Modelo y evidencia de reequilibrio de carteras: cuando la bolsa local sube más que la extranjera, los inversores reducen exposición y la divisa local tiende a depreciarse.
- **Uso en el bloque:** TR-PFV: flujos de reequilibrio de carteras de renta variable como determinante del tipo de cambio (la divisa del mercado que más sube tiende a depreciarse); AS-G10N y AS-G10M: relación bolsa-divisa y coberturas.
- **Limitaciones:** Resumen no leído en esta carga.

#### FXA-0240 · Q 86 (A) — The Global Capital Market: Benefactor or Menace?

- **Autores:** Maurice Obstfeld
- **Año:** 1998
- **Publicación o institución:** Journal of Economic Perspectives, vol. 12, n.º 4, págs. 9-30
- **Tipo de documento:** Artículo revisado (survey)
- **Temática:** TX-07 Balanza de pagos, flujos de capital y ciclo financiero global (principal) · secundarias: TX-08, TX-09
- **Calidad Q:** 86 (A) — Tipo 22/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 5/10 · Impacto 10/10 · Independencia 10/10 · Acceso 9/10
- **DOI / URL:** https://ideas.repec.org/a/aea/jecper/v12y1998i4p9-30.html
- **Acceso y licencia:** JEP de acceso abierto (AEA)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Maurice Obstfeld IDEAS RePEc author page»; WebFetch: sí, índice https://ideas.repec.org:443/e/pob13.html)
- **Contenido:** Survey sobre los beneficios (diversificación, financiación) y riesgos (crisis, pérdida de autonomía monetaria) de la integración financiera internacional, escrito tras la crisis asiática; introduce la lógica del trilema para lectores no especialistas.
- **Uso en el bloque:** DOC-A y Analistas de segmento: introducción conceptual a los flujos de capital y su vínculo con el régimen cambiario.
- **Limitaciones:** Visión de finales de los noventa.

#### FXA-0280 · Q 86 (A) — Capital Flows to Developing Countries in the 1990s: Causes and Effects

- **Autores:** Guillermo Calvo; Leonardo Leiderman; Carmen M. Reinhart
- **Año:** 1996
- **Publicación o institución:** Journal of Economic Perspectives, vol. 10, págs. 123-139
- **Tipo de documento:** Artículo revisado (survey)
- **Temática:** TX-07 Balanza de pagos, flujos de capital y ciclo financiero global (principal) · secundarias: TX-10
- **Calidad Q:** 86 (A) — Tipo 22/25 · Rigor 14/20 · Autoridad 15/15 · Vigencia 5/10 · Impacto 10/10 · Independencia 10/10 · Acceso 10/10
- **DOI / URL:** índice: https://www.federalreserve.gov/econres/ifdp/files/ifdp1241.pdf (bibliografía)
- **Acceso y licencia:** JEP de acceso abierto (AEA)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Bruno Shin "Capital flows and the risk-taking channel of monetary policy" "Cross-border banking and global liquidity"»; WebFetch: sí, índice: bibliografía de Correa et al., IFDP 1241, https://www.federalreserve.gov/econres/ifdp/files/ifdp1241.pdf)
- **Contenido:** Survey clásico que atribuye buena parte de las entradas de capital en los emergentes de los noventa a factores externos («push»: tipos de interés bajos en EE. UU., recesión en el centro) y analiza sus efectos (apreciación real, reservas, auge de crédito).
- **Uso en el bloque:** TR-BCM y Analistas de segmento emergentes: marco push/pull para separar el componente global del idiosincrásico en los flujos hacia una divisa.
- **Limitaciones:** Contexto de los noventa; verificada por bibliografía de un tercero.

#### FXA-0241 · Q 85 (A) — International Monetary Relations: Taking Finance Seriously

- **Autores:** Maurice Obstfeld; Alan M. Taylor
- **Año:** 2017
- **Publicación o institución:** Journal of Economic Perspectives, vol. 31, n.º 3, págs. 3-28
- **Tipo de documento:** Artículo revisado (survey)
- **Temática:** TX-07 Balanza de pagos, flujos de capital y ciclo financiero global (principal) · secundarias: TX-08, TX-12
- **Calidad Q:** 85 (A) — Tipo 22/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 7/10 · Independencia 10/10 · Acceso 8/10
- **DOI / URL:** https://ideas.repec.org/a/aea/jecper/v31y2017i3p3-28.html
- **Acceso y licencia:** JEP de acceso abierto (AEA)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Maurice Obstfeld IDEAS RePEc author page»; WebFetch: sí, índice https://ideas.repec.org:443/e/pob13.html)
- **Contenido:** Recorrido histórico de las relaciones monetarias internacionales (patrón oro, Bretton Woods, flotación) que pone en el centro la estabilidad financiera y los flujos de capital, y no solo el tipo de cambio y el comercio.
- **Uso en el bloque:** TR-BCM y AS-ESTR: perspectiva histórica del sistema y de las restricciones que imponen los flujos financieros a los regímenes.
- **Limitaciones:** Ensayo histórico; resumen no leído en esta carga.

#### ANA-DOC-0366 · Q 84 (A) — Capital Flow Waves—or Ripples? Extreme Capital Flow Movements Since the Crisis

- **Autores:** Kristin J. Forbes; Francis E. Warnock
- **Año:** 2021 (NBER WP 26851 de 2020)
- **Publicación o institución:** Journal of International Money and Finance, vol. 116
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-07 Balanza de pagos, flujos de capital y ciclo financiero global (principal) · secundarias: TX-10
- **Calidad Q:** 84 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 5/10 · Independencia 10/10 · Acceso 2/10
- **DOI / URL:** https://ideas.repec.org/p/nbr/nberwo/26851.html
- **Acceso y licencia:** Peldaño 2 (WP NBER) · Licencia: Copyright Elsevier/autores
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Kristin Forbes Warnock "Capital flow waves" IDEAS RePEc…»; WebFetch: sí)
- **Contenido:** Tras la crisis de 2008 la frecuencia de episodios extremos de flujos no aumenta, pero se vuelven menos ligados al riesgo global y más idiosincrásicos («ondas» frente a «olas»).
- **Uso en el bloque:** TR-PFV: matiza el peso del riesgo global (VIX) como predictor de episodios extremos de flujos desde 2010; CONTRA: objeción a tesis que extrapolan el patrón anterior a 2008.
- **Limitaciones:** Muestra hasta finales de los 2010.

#### FXA-0224 · Q 84 (A) — Global Cycles: Capital Flows, Commodities, and Sovereign Defaults, 1815-2015

- **Autores:** Carmen M. Reinhart; Vincent Reinhart; Christoph Trebesch
- **Año:** 2016
- **Publicación o institución:** American Economic Review, vol. 106, n.º 5, págs. 574-580 (Papers & Proceedings)
- **Tipo de documento:** Artículo revisado por pares (Papers & Proceedings)
- **Temática:** TX-07 Balanza de pagos, flujos de capital y ciclo financiero global (principal) · secundarias: TX-11, TX-09
- **Calidad Q:** 84 (A) — Tipo 23/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 8/10 · Independencia 10/10 · Acceso 4/10
- **DOI / URL:** https://ideas.repec.org/a/aea/aecrev/v106y2016i5p574-80.html
- **Acceso y licencia:** Ficha libre en IDEAS; texto AEA (acceso según suscripción)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Carmen Reinhart IDEAS RePEc profile research papers»; WebFetch: sí, índice https://ideas.repec.org/e/pre33.html)
- **Contenido:** Con dos siglos de datos, documenta la sincronía entre ciclos de flujos de capital, precios de materias primas e impagos soberanos: los auges conjuntos de flujos y materias primas suelen ir seguidos de oleadas de impagos.
- **Uso en el bloque:** TR-BCM y AS-G10M/AS-EMLA: lectura conjunta del ciclo de materias primas y de flujos para divisas exportadoras; horizonte H4.
- **Limitaciones:** Nota breve de Papers & Proceedings; evidencia agregada.

#### FXA-0239 · Q 82 (A) — Financial flows, financial crises, and global imbalances

- **Autores:** Maurice Obstfeld
- **Año:** 2012
- **Publicación o institución:** Journal of International Money and Finance, vol. 31, n.º 3, págs. 469-480
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-07 Balanza de pagos, flujos de capital y ciclo financiero global (principal) · secundarias: TX-09
- **Calidad Q:** 82 (A) — Tipo 25/25 · Rigor 14/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 7/10 · Independencia 10/10 · Acceso 4/10
- **DOI / URL:** https://ideas.repec.org/a/eee/jimfin/v31y2012i3p469-480.html
- **Acceso y licencia:** Ficha libre en IDEAS; texto de pago (Elsevier)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Maurice Obstfeld IDEAS RePEc author page»; WebFetch: sí, índice https://ideas.repec.org:443/e/pob13.html)
- **Contenido:** Relaciona los flujos financieros brutos, los desequilibrios globales y las crisis, subrayando que los riesgos se acumulan en los balances brutos aunque los saldos netos sean modestos.
- **Uso en el bloque:** TR-PFV y TR-BCM: complemento de FXA-0238 para leer la vulnerabilidad externa por flujos brutos.
- **Limitaciones:** Resumen no leído en esta carga.

#### FXA-0226 · Q 80 (A) — Decrypting New Age International Capital Flows

- **Autores:** Clemens Graf von Luckner; Carmen M. Reinhart; Kenneth Rogoff
- **Año:** 2023
- **Publicación o institución:** Journal of Monetary Economics, vol. 138, págs. 104-122
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-07 Balanza de pagos, flujos de capital y ciclo financiero global (principal) · secundarias: TX-08, TX-14
- **Calidad Q:** 80 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 5/10 · Independencia 10/10 · Acceso 0/10
- **DOI / URL:** https://ideas.repec.org/a/eee/moneco/v138y2023icp104-122.html
- **Acceso y licencia:** Ficha libre en IDEAS; texto de pago (Elsevier)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Carmen Reinhart IDEAS RePEc profile research papers»; WebFetch: sí, índice https://ideas.repec.org/e/pre33.html)
- **Contenido:** Estudia los flujos internacionales canalizados por criptoactivos como vía de elusión de controles de capitales y de salida de capitales en economías con restricciones cambiarias (según título y línea de la autora; texto no leído).
- **Uso en el bloque:** AS-EMLA (ARS y regímenes con controles), AS-EMEA (TRY, NGN, EGP): canales informales de fuga de capital que debilitan los controles y presionan el tipo paralelo.
- **Limitaciones:** Resumen no leído en esta carga; ámbito muy reciente.

#### FXA-0282 · Q 80 (A) — Cross-Border Bank Flows and Monetary Policy

- **Autores:** Ricardo Correa; Teodora Paligorova; Horacio Sapriza; Andrei Zlate
- **Año:** 2018 (diciembre)
- **Publicación o institución:** Board of Governors of the Federal Reserve System, International Finance Discussion Papers n.º 1241
- **Tipo de documento:** Documento de trabajo de banco central
- **Temática:** TX-07 Balanza de pagos, flujos de capital y ciclo financiero global (principal) · secundarias: TX-02
- **Calidad Q:** 80 (A) — Tipo 18/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 5/10 · Independencia 8/10 · Acceso 9/10
- **DOI / URL:** https://www.federalreserve.gov/econres/ifdp/files/ifdp1241.pdf
- **Acceso y licencia:** Acceso abierto (Reserva Federal)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Bruno Shin "Capital flows and the risk-taking channel of monetary policy" "Cross-border banking and global liquidity"»; WebFetch: sí)
- **Contenido:** Con datos de bancos con actividad transfronteriza en EE. UU., estudia cómo la política monetaria del centro afecta a los flujos bancarios transfronterizos y su reparto entre países y prestatarios.
- **Uso en el bloque:** TR-BCM y TR-PFV: canal bancario de transmisión de la Fed a la financiación en dólares de otras economías.
- **Limitaciones:** Documento de trabajo; centrado en bancos con presencia en EE. UU.

#### FXA-0283 · Q 80 (A) — Global liquidity and cross-border bank flows

- **Autores:** Eugenio Cerutti; Stijn Claessens; Lev Ratnovski
- **Año:** 2017
- **Publicación o institución:** Economic Policy, vol. 32, n.º 89, págs. 81-125
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-07 Balanza de pagos, flujos de capital y ciclo financiero global (principal) · secundarias: TX-10
- **Calidad Q:** 80 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 8/10 · Impacto 7/10 · Independencia 9/10 · Acceso 1/10
- **DOI / URL:** índice: https://www.federalreserve.gov/econres/ifdp/files/ifdp1241.pdf (bibliografía)
- **Acceso y licencia:** Artículo de pago (OUP); versiones de trabajo del FMI
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Bruno Shin "Capital flows and the risk-taking channel of monetary policy" "Cross-border banking and global liquidity"»; WebFetch: sí, índice: bibliografía de Correa et al., IFDP 1241, https://www.federalreserve.gov/econres/ifdp/files/ifdp1241.pdf)
- **Contenido:** Identifica los impulsores globales de los flujos bancarios transfronterizos (VIX, condiciones monetarias de EE. UU. y del Reino Unido, situación de los bancos) y qué características de los países receptores amplifican la sensibilidad.
- **Uso en el bloque:** TR-PFV: variables globales a vigilar en la lente de flujos; Analistas de segmento: sensibilidad de cada país.
- **Limitaciones:** Verificada por bibliografía de un tercero; texto no leído.

#### FXA-0243 · Q 80 (A) — Global Imbalances and the Financial Crisis: Products of Common Causes

- **Autores:** Maurice Obstfeld; Kenneth Rogoff
- **Año:** 2009
- **Publicación o institución:** CEPR Discussion Paper n.º 7606
- **Tipo de documento:** Documento de trabajo
- **Temática:** TX-07 Balanza de pagos, flujos de capital y ciclo financiero global (principal) · secundarias: TX-09, TX-12
- **Calidad Q:** 80 (A) — Tipo 17/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 6/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / URL:** https://ideas.repec.org/p/cpr/ceprdp/7606.html
- **Acceso y licencia:** Ficha libre en IDEAS; texto CEPR
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Maurice Obstfeld IDEAS RePEc author page»; WebFetch: sí, índice https://ideas.repec.org:443/e/pob13.html)
- **Contenido:** Sostiene que los desequilibrios globales y la crisis de 2008 comparten causas comunes (política monetaria laxa, fallos regulatorios, política cambiaria de acumulación de reservas en emergentes) y analiza sus implicaciones para el dólar.
- **Uso en el bloque:** TR-BCM y AS-G10N: vínculo entre política cambiaria de los superavitarios, flujos y dólar.
- **Limitaciones:** Análisis de 2009; resumen no leído en esta carga.

#### FXA-0225 · Q 78 (B) — Capital Inflows, Exchange Rate Flexibility and Credit Booms

- **Autores:** Nicolás E. Magud; Carmen M. Reinhart; Esteban R. Vesperoni
- **Año:** 2014 (IMF WP 12/41 de 2012)
- **Publicación o institución:** Review of Development Economics, vol. 18, n.º 3, págs. 415-430
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-07 Balanza de pagos, flujos de capital y ciclo financiero global (principal) · secundarias: TX-08, TX-10
- **Calidad Q:** 78 (B) — Tipo 24/25 · Rigor 16/20 · Autoridad 13/15 · Vigencia 7/10 · Impacto 6/10 · Independencia 9/10 · Acceso 3/10
- **DOI / URL:** https://ideas.repec.org/a/bla/rdevec/v18y2014i3p415-430.html · versión de trabajo: https://ideas.repec.org/p/imf/imfwpa/2012-041.html
- **Acceso y licencia:** Ficha libre en IDEAS; WP del FMI de acceso abierto
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Carmen Reinhart IDEAS RePEc profile research papers»; WebFetch: sí, índice https://ideas.repec.org/e/pre33.html)
- **Contenido:** Las entradas de capital alimentan más los auges de crédito en economías con tipos de cambio menos flexibles; la flexibilidad cambiaria amortigua el efecto sobre el crédito bancario.
- **Uso en el bloque:** AS-EMAS, AS-EMLA, AS-EMEA: vincular régimen cambiario, entradas y fragilidad financiera al valorar divisas con apreciación gestionada.
- **Limitaciones:** Muestra de emergentes hasta finales de los 2000.

#### FXA-0242 · Q 76 (B) — Twenty Five Years of Global Imbalances

- **Autores:** Maurice Obstfeld
- **Año:** 2018
- **Publicación o institución:** CEPR Discussion Paper n.º 13066
- **Tipo de documento:** Documento de trabajo
- **Temática:** TX-07 Balanza de pagos, flujos de capital y ciclo financiero global (principal) · secundarias: —
- **Calidad Q:** 76 (B) — Tipo 17/25 · Rigor 14/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 5/10 · Independencia 10/10 · Acceso 7/10
- **DOI / URL:** https://ideas.repec.org/p/cpr/ceprdp/13066.html
- **Acceso y licencia:** Ficha libre en IDEAS; texto CEPR
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Maurice Obstfeld IDEAS RePEc author page»; WebFetch: sí, índice https://ideas.repec.org:443/e/pob13.html)
- **Contenido:** Repaso de la evolución de los desequilibrios por cuenta corriente globales en el último cuarto de siglo y de sus causas y riesgos.
- **Uso en el bloque:** TR-BCM: contexto de desequilibrios (superávits asiáticos y europeos, déficit de EE. UU.) para tesis H4 del dólar.
- **Limitaciones:** Documento de trabajo; resumen no leído.

#### FXA-0276 · Q 76 (B) — Are Capital Flows Fickle? Increasingly? And Does the Answer Still Depend on Type?

- **Autores:** Barry Eichengreen; Poonam Gupta
- **Año:** 2018
- **Publicación o institución:** Asian Economic Papers, vol. 17, n.º 1, págs. 22-41 (MIT Press)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-07 Balanza de pagos, flujos de capital y ciclo financiero global (principal) · secundarias: TX-10
- **Calidad Q:** 76 (B) — Tipo 23/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 8/10 · Impacto 4/10 · Independencia 10/10 · Acceso 2/10
- **DOI / URL:** https://ideas.repec.org/a/tpr/asiaec/v17y2018i1p22-41.html
- **Acceso y licencia:** Ficha libre en IDEAS; texto de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Barry Eichengreen IDEAS RePEc author page»; WebFetch: sí, índice https://ideas.repec.org/e/pei2.html)
- **Contenido:** Compara la volatilidad de los distintos tipos de flujos (IED, cartera, otros/bancarios) en emergentes y si se han vuelto más volátiles con el tiempo.
- **Uso en el bloque:** TR-PFV y Analistas de segmento emergentes: ponderar la calidad de la financiación exterior (balanza básica frente a flujos de cartera) en la lente de flujos.
- **Limitaciones:** Resumen no leído en esta carga.

#### FXA-0284 · Q 76 (B) — The shifting drivers of global liquidity

- **Autores:** Stefan Avdjiev; Leonardo Gambacorta; Linda S. Goldberg; Stefano Schiaffi
- **Año:** 2017
- **Publicación o institución:** Federal Reserve Bank of New York, Staff Reports n.º 819
- **Tipo de documento:** Documento de trabajo de banco central
- **Temática:** TX-07 Balanza de pagos, flujos de capital y ciclo financiero global (principal) · secundarias: —
- **Calidad Q:** 76 (B) — Tipo 18/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 5/10 · Independencia 8/10 · Acceso 6/10
- **DOI / URL:** índice: https://www.federalreserve.gov/econres/ifdp/files/ifdp1241.pdf (bibliografía)
- **Acceso y licencia:** Staff Report de la Fed de Nueva York (acceso abierto)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Bruno Shin "Capital flows and the risk-taking channel of monetary policy" "Cross-border banking and global liquidity"»; WebFetch: sí, índice: bibliografía de Correa et al., IFDP 1241, https://www.federalreserve.gov/econres/ifdp/files/ifdp1241.pdf)
- **Contenido:** Documenta que los impulsores de la liquidez global cambiaron tras la crisis: la sensibilidad de los préstamos bancarios transfronterizos al VIX disminuyó y aumentó la sensibilidad a la política monetaria de EE. UU. y a la de los bonos.
- **Uso en el bloque:** TR-PFV: actualizar las variables de liquidez global (menos VIX, más Fed) en la lente de flujos.
- **Limitaciones:** Verificada por bibliografía de un tercero; texto no leído.

## TX-08 Regímenes cambiarios, intervención y controles de capitales

#### FXA-0289 · Q 94 (A) — Fear of Floating

- **Autores:** Guillermo A. Calvo; Carmen M. Reinhart
- **Año:** 2002 (NBER WP 7993 de 2000)
- **Publicación o institución:** The Quarterly Journal of Economics, vol. 117, n.º 2, págs. 379-408
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-08 Regímenes cambiarios, intervención y controles de capitales (principal) · secundarias: TX-10
- **Calidad Q:** 94 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 6/10 · Impacto 10/10 · Independencia 10/10 · Acceso 10/10
- **DOI / URL:** DOI: 10.1162/003355302753650274 · https://ideas.repec.org/a/oup/qjecon/v117y2002i2p379-408..html · versión de trabajo: https://www.nber.org/papers/w7993
- **Acceso y licencia:** Ficha libre en IDEAS; WP NBER y versión MPRA de acceso libre
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Calvo Reinhart 2002 "Fear of Floating" Quarterly Journal of Economics»; WebFetch: sí, IDEAS)
- **Contenido:** Con tipos de cambio, reservas y tipos de interés de muchos países, muestra que la mayoría de los que dicen flotar no lo hacen: su tipo de cambio es poco volátil y la variabilidad se traslada a reservas y tipos de interés («miedo a flotar»), por descalces, traspaso a precios y falta de credibilidad.
- **Uso en el bloque:** Analizador, TR-BCM y Analistas de segmento emergentes: no fiarse del régimen declarado; medir de facto la flexibilidad y anticipar defensa de la divisa.
- **Limitaciones:** Datos hasta finales de los noventa; muchos emergentes flotan hoy más que entonces (véase FXA-0229).

#### FXA-0288 · Q 92 (A) — When is Foreign Exchange Intervention Effective? Evidence from 33 Countries

- **Autores:** Marcel Fratzscher; Oliver Gloede; Lukas Menkhoff; Lucio Sarno; Tobias Stöhr
- **Año:** 2019
- **Publicación o institución:** American Economic Journal: Macroeconomics, vol. 11, n.º 1, págs. 132-156
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-08 Regímenes cambiarios, intervención y controles de capitales (principal) · secundarias: TX-02, TX-10
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 8/10 · Independencia 9/10 · Acceso 8/10
- **DOI / URL:** DOI: 10.1257/mac.20150317 · https://www.aeaweb.org/doi/10.1257/mac.20150317 · versión aceptada: https://openaccess.city.ac.uk/id/eprint/19099/
- **Acceso y licencia:** Versión aceptada de acceso abierto (City Research Online); datos de replicación en openICPSR
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Fratzscher Gloede Menkhoff Sarno Stöhr "When Is Foreign Exchange Intervention Effective?" American Economic Journal Macroeconomics 2019»; WebFetch: sí, City Research Online)
- **Contenido:** Con datos diarios de intervención de 33 países (1995-2011), muestra que los bancos centrales intervienen a menudo y con éxito (más del 80 % según algunos criterios), sobre todo para suavizar movimientos y sostener bandas estrechas; mover el nivel en flotación es más difícil y requiere volúmenes grandes, intervención pública y comunicación.
- **Uso en el bloque:** TR-BCM y Analistas de segmento (JPY, CHF, emergentes con flotación gestionada): estimar la probabilidad de éxito de una intervención y su efecto según régimen; CONTRA: riesgo de intervención contra la tesis.
- **Limitaciones:** Muestra hasta 2011.

#### FXA-0290 · Q 92 (A) — Official Intervention in the Foreign Exchange Market: Is It Effective and, If So, How Does It Work?

- **Autores:** Lucio Sarno; Mark P. Taylor
- **Año:** 2001
- **Publicación o institución:** Journal of Economic Literature, vol. 39, n.º 3, págs. 839-868
- **Tipo de documento:** Artículo de revisión (survey) revisado por pares
- **Temática:** TX-08 Regímenes cambiarios, intervención y controles de capitales (principal) · secundarias: TX-02, TX-06
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 6/10 · Impacto 10/10 · Independencia 10/10 · Acceso 9/10
- **DOI / URL:** DOI: 10.1257/jel.39.3.839 · https://ideas.repec.org/a/aea/jeclit/v39y2001i3p839-868.html · versión de trabajo: CEPR DP 2690 (https://econpapers.repec.org/paper/cprceprdp/2690.htm)
- **Acceso y licencia:** Ficha libre en IDEAS; copias de trabajo en abierto (CEPR, Warwick)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Sarno Taylor 2001 "Official Intervention in the Foreign Exchange Market…" Journal of Economic Literature»; WebFetch: sí, IDEAS)
- **Contenido:** Survey de teoría y evidencia sobre la intervención esterilizada: puede ser eficaz, sobre todo cuando señala intenciones de política, es pública y concertada; propone un canal de coordinación de expectativas para explicar por qué funciona incluso en secreto.
- **Uso en el bloque:** TR-BCM: canales (cartera, señal, coordinación) para valorar episodios de intervención en G10 (JPY, CHF) y emergentes.
- **Limitaciones:** Evidencia mayoritariamente de G3 anterior a 2000; complementar con FXA-0288.

#### FXA-0244 · Q 91 (A) — The Trilemma in History: Tradeoffs Among Exchange Rates, Monetary Policies, and Capital Mobility

- **Autores:** Maurice Obstfeld; Jay C. Shambaugh; Alan M. Taylor
- **Año:** 2005
- **Publicación o institución:** Review of Economics and Statistics, vol. 87, n.º 3, págs. 423-438
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-08 Regímenes cambiarios, intervención y controles de capitales (principal) · secundarias: TX-02, TX-07
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / URL:** https://ideas.repec.org/a/tpr/restat/v87y2005i3p423-438.html
- **Acceso y licencia:** Ficha libre en IDEAS; texto de pago (MIT Press); versiones NBER
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Maurice Obstfeld IDEAS RePEc author page»; WebFetch: sí, índice https://ideas.repec.org:443/e/pob13.html)
- **Contenido:** Con más de un siglo de datos, contrasta el trilema: los países con tipo fijo y movilidad de capital ven sus tipos de interés seguir a los del país ancla, mientras que la flotación o los controles conceden autonomía monetaria.
- **Uso en el bloque:** TR-BCM y Analistas de segmento: fundamento para juzgar cuánta autonomía tiene un banco central con ancla (HKD, Golfo, DKK) y la transmisión de los tipos del ancla.
- **Limitaciones:** Resumen no leído; matizado por Rey (ANA-DOC-0303) en la era del ciclo financiero global.

#### ANA-DOC-0308 · Q 90 (A) — Exchange Arrangements Entering the Twenty-First Century: Which Anchor will Hold?

- **Autores:** Ethan Ilzetzki; Carmen M. Reinhart; Kenneth S. Rogoff
- **Año:** 2019 (NBER WP 23134 de 2017)
- **Publicación o institución:** The Quarterly Journal of Economics, vol. 134, n.º 2, págs. 599-646
- **Tipo de documento:** Artículo revisado por pares con base de datos asociada
- **Temática:** TX-08 Regímenes cambiarios, intervención y controles de capitales (principal) · secundarias: TX-12, TX-10
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 4/10
- **DOI / URL:** DOI de la versión de trabajo 10.3386/w23134 · https://www.nber.org/papers/w23134
- **Acceso y licencia:** Peldaño 2 (versión NBER; datos en carmenreinhart.com) · Licencia: Copyright OUP/autores
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Ilzetzki Reinhart Rogoff "Exchange Arrangements Entering the Twenty-First Century: Which Anchor will Hold?" Quarterly Journal of Economics»; WebFetch: sí)
- **Contenido:** Clasificación de facto de regímenes cambiarios y monedas ancla de 194 países (1946-2016): el dólar sigue siendo el ancla dominante, el papel global del euro se ha estancado y los regímenes de flexibilidad limitada predominan.
- **Uso en el bloque:** Analizador y Analistas de segmento: clasificación de facto del régimen de cada divisa (ancla, banda, flotación gestionada) para la regla de asignación y la invertibilidad; TR-BCM: peso del dólar como ancla dominante frente al euro.
- **Limitaciones:** Clasificación actualizada periódicamente; usar la versión de datos vigente.

#### FXA-0291 · Q 88 (A) — Toward an Integrated Policy Framework (IMF Policy Paper)

- **Autores:** Fondo Monetario Internacional (equipo interdepartamental dirigido por David Hofman, con Emine Boz, Marcos Chamon y Vladimir Klyuev; aprobado por Tobias Adrian, Gita Gopinath y Martin Mühleisen)
- **Año:** 2020 (2 de septiembre)
- **Publicación o institución:** IMF Policy Paper (ppea2020046)
- **Tipo de documento:** Documento de política de organismo internacional
- **Temática:** TX-08 Regímenes cambiarios, intervención y controles de capitales (principal) · secundarias: TX-10, TX-02
- **Calidad Q:** 88 (A) — Tipo 20/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 8/10 · Acceso 10/10
- **DOI / URL:** https://www.imf.org/-/media/files/publications/pp/2020/english/ppea2020046.pdf.md · portal: https://www.imf.org/en/Topics/IPF-Integrated-Policy-Framework
- **Acceso y licencia:** Acceso abierto (FMI)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «IMF Integrated Policy Framework foreign exchange intervention capital flow management Basu Boz Gopinath Roch Unsal 2020»; WebFetch: sí)
- **Contenido:** Marco del FMI que integra política monetaria, intervención cambiaria, medidas macroprudenciales y de gestión de flujos de capital: con mercados profundos la flexibilidad plena es óptima; con fricciones y descalces, la intervención y las medidas sobre flujos pueden mejorar los resultados, sin servir para sostener tipos desalineados.
- **Uso en el bloque:** TR-BCM y Analistas de segmento emergentes: anticipar cuándo un banco central usará intervención o controles según el tipo de choque y sus vulnerabilidades; marco de referencia del FMI para la lente de régimen.
- **Limitaciones:** Documento normativo; la vista institucional del FMI sobre flujos se revisó después.

#### FXA-0227 · Q 86 (A) — Rethinking Exchange Rate Regimes

- **Autores:** Ethan Ilzetzki; Carmen M. Reinhart; Kenneth S. Rogoff
- **Año:** 2021
- **Publicación o institución:** CEPR Discussion Paper n.º 16722
- **Tipo de documento:** Documento de trabajo (survey)
- **Temática:** TX-08 Regímenes cambiarios, intervención y controles de capitales (principal) · secundarias: TX-12
- **Calidad Q:** 86 (A) — Tipo 21/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 10/10 · Acceso 6/10
- **DOI / URL:** https://ideas.repec.org/p/cpr/ceprdp/16722.html
- **Acceso y licencia:** Ficha libre en IDEAS; texto CEPR (acceso para miembros / versión NBER)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Carmen Reinhart IDEAS RePEc profile research papers»; WebFetch: sí, índice https://ideas.repec.org/e/pre33.html)
- **Contenido:** Revisión de la literatura y de la evidencia sobre regímenes cambiarios de facto: clasificación, prevalencia de anclas y flotaciones gestionadas, costes y beneficios de cada régimen y papel del dólar como ancla.
- **Uso en el bloque:** Analizador y Analistas de segmento: marco de referencia para clasificar el régimen de cada divisa y anticipar defensa de anclas; TR-BCM: riesgo de intervención.
- **Limitaciones:** Documento de trabajo; resumen no leído en esta carga (verificada por el índice de la autora).

#### FXA-0292 · Q 84 (A) — Integrated Monetary and Financial Policies for Small Open Economies

- **Autores:** Suman S. Basu; Emine Boz; Gita Gopinath; Francisco Roch; Filiz D. Unsal
- **Año:** 2025 (versión previa: «A Conceptual Model for the Integrated Policy Framework», IMF Working Paper, 2020)
- **Publicación o institución:** Econometrica, vol. 93
- **Tipo de documento:** Artículo revisado por pares (teórico)
- **Temática:** TX-08 Regímenes cambiarios, intervención y controles de capitales (principal) · secundarias: TX-10
- **Calidad Q:** 84 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 5/10 · Independencia 8/10 · Acceso 3/10
- **DOI / URL:** índice: https://gopinath.scholars.harvard.edu/publications.md · versión de trabajo (CEPR): https://repec.cepr.org/repec/cpr/ceprdp/DP15065.pdf
- **Acceso y licencia:** Econometrica (acceso según suscripción); versiones de trabajo del FMI y del CEPR
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «IMF Integrated Policy Framework foreign exchange intervention capital flow management Basu Boz Gopinath Roch Unsal 2020»; WebFetch: sí, índice https://gopinath.scholars.harvard.edu/publications.md)
- **Contenido:** Marco de pequeña economía abierta que caracteriza el uso eficiente restringido del tipo oficial, la intervención cambiaria, las medidas macroprudenciales y los controles de capital ante fricciones (descalces, mercados poco profundos, precios en dólares).
- **Uso en el bloque:** TR-BCM: fundamento teórico del IPF para modelar la respuesta de política en emergentes.
- **Limitaciones:** Teórico; la correspondencia del DP 15065 del CEPR con este trabajo se infiere de la búsqueda.

#### FXA-0245 · Q 84 (A) — Financial Stability, the Trilemma, and International Reserves

- **Autores:** Maurice Obstfeld; Jay C. Shambaugh; Alan M. Taylor
- **Año:** 2010
- **Publicación o institución:** American Economic Journal: Macroeconomics, vol. 2, n.º 2, págs. 57-94
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-08 Regímenes cambiarios, intervención y controles de capitales (principal) · secundarias: TX-09, TX-10
- **Calidad Q:** 84 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 6/10 · Impacto 8/10 · Independencia 10/10 · Acceso 3/10
- **DOI / URL:** https://ideas.repec.org/a/aea/aejmac/v2y2010i2p57-94.html
- **Acceso y licencia:** Ficha libre en IDEAS; texto AEA
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Maurice Obstfeld IDEAS RePEc author page»; WebFetch: sí, índice https://ideas.repec.org:443/e/pob13.html)
- **Contenido:** Explica la acumulación de reservas en emergentes por la necesidad de proteger el sistema financiero doméstico (riesgo de fuga de depósitos hacia divisas) bajo apertura financiera y tipos gestionados, más que por motivos comerciales.
- **Uso en el bloque:** AS-EMAS, AS-EMEA y TR-BCM: métricas de adecuación de reservas (frente a M2) para valorar la capacidad de defensa de la divisa.
- **Limitaciones:** Resumen no leído en esta carga.

#### FXA-0230 · Q 82 (A) — Will the Secular Decline In Exchange Rate and Inflation Volatility Survive COVID-19?

- **Autores:** Ethan Ilzetzki; Carmen M. Reinhart; Kenneth S. Rogoff
- **Año:** 2020
- **Publicación o institución:** Brookings Papers on Economic Activity, vol. 51, n.º 3 (otoño), págs. 279-332
- **Tipo de documento:** Artículo con discusión (Brookings Papers)
- **Temática:** TX-08 Regímenes cambiarios, intervención y controles de capitales (principal) · secundarias: TX-09
- **Calidad Q:** 82 (A) — Tipo 23/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 6/10 · Independencia 10/10 · Acceso 3/10
- **DOI / URL:** https://ideas.repec.org/a/bin/bpeajo/v51y2020i2020-03p279-332.html
- **Acceso y licencia:** Ficha libre en IDEAS; Brookings publica habitualmente los BPEA en abierto
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Carmen Reinhart IDEAS RePEc profile research papers»; WebFetch: sí, índice https://ideas.repec.org/e/pre33.html)
- **Contenido:** Documenta la caída secular de la volatilidad cambiaria y de la inflación en las décadas previas a 2020 y discute si sobrevivirá a la pandemia y al nuevo entorno de política.
- **Uso en el bloque:** AS-ESTR y TR-PFV: contexto histórico del régimen de volatilidad cambiaria; CONTRA: riesgo de que la baja volatilidad no sea permanente.
- **Limitaciones:** Escrito en 2020, antes del episodio inflacionario de 2021-2023.

#### FXA-0251 · Q 82 (A) — Estimation of De Facto Exchange Rate Regimes: Synthesis of the Techniques for Inferring Flexibility and Basket Weights

- **Autores:** Jeffrey Frankel; Shang-Jin Wei
- **Año:** 2008
- **Publicación o institución:** IMF Staff Papers, vol. 55, n.º 3, págs. 384-416
- **Tipo de documento:** Artículo revisado por pares (metodológico)
- **Temática:** TX-08 Regímenes cambiarios, intervención y controles de capitales (principal) · secundarias: TX-10
- **Calidad Q:** 82 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 5/10 · Impacto 7/10 · Independencia 9/10 · Acceso 4/10
- **DOI / URL:** https://ideas.repec.org/a/pal/imfstp/v55y2008i3p384-416.html
- **Acceso y licencia:** Ficha libre en IDEAS
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Jeffrey Frankel IDEAS RePEc author page Harvard Kennedy»; WebFetch: sí, índice https://ideas.repec.org/e/pfr12.html)
- **Contenido:** Sintetiza la regresión Frankel-Wei para inferir de facto los pesos de una cesta implícita (USD, EUR, JPY…) y el grado de flexibilidad de un régimen a partir de los movimientos del tipo de cambio.
- **Uso en el bloque:** AS-EMAS (CNY, SGD, MYR) y MOTOR (vía TMX): identificar la cesta implícita y la flexibilidad efectiva de una divisa gestionada.
- **Limitaciones:** Sensible al periodo de estimación y a cambios de régimen; resumen no leído.

#### FXA-0235 · Q 82 (A) — Fixed versus Flexible: Lessons from EMS Order Flow

- **Autores:** William P. Killeen; Richard K. Lyons; Michael J. Moore
- **Año:** 2006
- **Publicación o institución:** Journal of International Money and Finance, vol. 25, págs. 551-579
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-08 Regímenes cambiarios, intervención y controles de capitales (principal) · secundarias: TX-06
- **Calidad Q:** 82 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 5/10 · Impacto 6/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** https://faculty.haas.berkeley.edu/lyons/pubabs.html (índice de publicaciones de R. K. Lyons)
- **Acceso y licencia:** Artículo de pago (Elsevier); resumen en la página del autor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Evans Lyons 2002 "Order Flow and Exchange Rate Dynamics" Journal of Political Economy»; WebFetch: sí, índice https://faculty.haas.berkeley.edu/lyons/pubabs.html)
- **Contenido:** Usa el flujo de órdenes FRF/DEM antes y después de la fijación irrevocable de paridades del SME (1998) para mostrar que, con un tipo creíblemente fijo, el flujo deja de mover el precio: el régimen cambia la elasticidad de la demanda de los intermediarios.
- **Uso en el bloque:** AS-EMAS y AS-EMEA (tipos fijos de HKD y del Golfo): por qué el flujo no mueve una paridad creíble y qué señales anuncian pérdida de credibilidad.
- **Limitaciones:** Caso específico de la convergencia al euro.

#### FXA-0248 · Q 82 (A) — No Single Currency Regime is Right for All Countries or At All Times

- **Autores:** Jeffrey A. Frankel
- **Año:** 1999
- **Publicación o institución:** NBER Working Papers n.º 7338
- **Tipo de documento:** Documento de trabajo (ensayo de política)
- **Temática:** TX-08 Regímenes cambiarios, intervención y controles de capitales (principal) · secundarias: TX-10
- **Calidad Q:** 82 (A) — Tipo 19/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 5/10 · Impacto 9/10 · Independencia 10/10 · Acceso 9/10
- **DOI / URL:** https://ideas.repec.org/p/nbr/nberwo/7338.html
- **Acceso y licencia:** Ficha libre en IDEAS; WP NBER
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Jeffrey Frankel IDEAS RePEc author page Harvard Kennedy»; WebFetch: sí, índice https://ideas.repec.org/e/pfr12.html)
- **Contenido:** Ensayo clásico que rechaza la tesis de las «esquinas» (solo fijo duro o flotación libre) y argumenta que el régimen óptimo depende de las características del país y del momento.
- **Uso en el bloque:** Analizador y Analistas de segmento: marco para evaluar regímenes intermedios (bandas, cestas, flotación gestionada) sin prejuzgar su insostenibilidad.
- **Limitaciones:** Ensayo de 1999; resumen no leído.

#### FXA-0228 · Q 80 (A) — Capital Controls: Myth and Reality — A Portfolio Balance Approach

- **Autores:** Nicolás E. Magud; Carmen M. Reinhart; Kenneth S. Rogoff
- **Año:** 2018 (NBER WP 16805 de 2011)
- **Publicación o institución:** Annals of Economics and Finance, vol. 19, n.º 1, págs. 1-47
- **Tipo de documento:** Artículo revisado por pares (con documento de trabajo NBER)
- **Temática:** TX-08 Regímenes cambiarios, intervención y controles de capitales (principal) · secundarias: TX-07, TX-10
- **Calidad Q:** 80 (A) — Tipo 22/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 8/10 · Independencia 10/10 · Acceso 2/10
- **DOI / URL:** https://ideas.repec.org/a/cuf/journl/y2018v19i1magudreinhartrogoff.html · versión de trabajo: https://ideas.repec.org/p/nbr/nberwo/16805.html
- **Acceso y licencia:** Ficha libre en IDEAS; WP NBER
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Carmen Reinhart IDEAS RePEc profile research papers»; WebFetch: sí, índice https://ideas.repec.org/e/pre33.html)
- **Contenido:** Revisa la evidencia sobre controles de capitales con un índice homogéneo y un marco de equilibrio de cartera: los controles a la entrada alargan los plazos de los flujos y dan algo de autonomía monetaria, pero apenas reducen el volumen ni la presión sobre el tipo de cambio real.
- **Uso en el bloque:** AS-EMLA, AS-EMAS, AS-EMEA y CONTRA: valorar la eficacia esperada de controles anunciados y su efecto sobre la divisa y la invertibilidad.
- **Limitaciones:** Resultados heterogéneos por país; texto completo no leído en esta carga.

#### FXA-0246 · Q 80 (A) — Monetary Sovereignty, Exchange Rates, and Capital Controls: The Trilemma in the Interwar Period

- **Autores:** Maurice Obstfeld; Jay C. Shambaugh; Alan M. Taylor
- **Año:** 2004
- **Publicación o institución:** IMF Staff Papers, vol. 51, n.º s1, págs. 75-108
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-08 Regímenes cambiarios, intervención y controles de capitales (principal) · secundarias: —
- **Calidad Q:** 80 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 4/10 · Impacto 6/10 · Independencia 9/10 · Acceso 4/10
- **DOI / URL:** https://ideas.repec.org/a/pal/imfstp/v51y2004is1p75-108.html
- **Acceso y licencia:** Ficha libre en IDEAS
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Maurice Obstfeld IDEAS RePEc author page»; WebFetch: sí, índice https://ideas.repec.org:443/e/pob13.html)
- **Contenido:** Contrasta el trilema en el periodo de entreguerras: los países que abandonaron el oro o impusieron controles ganaron autonomía monetaria frente a los que mantuvieron la paridad con libre movilidad.
- **Uso en el bloque:** TR-BCM: evidencia histórica sobre controles de capitales como vía de autonomía monetaria.
- **Limitaciones:** Periodo histórico; resumen no leído.

#### FXA-0252 · Q 80 (A) — Global transmission of interest rates: monetary independence and currency regime

- **Autores:** Jeffrey Frankel; Sergio Schmukler; Luis Servén
- **Año:** 2004
- **Publicación o institución:** Journal of International Money and Finance, vol. 23, n.º 5, págs. 701-733
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-08 Regímenes cambiarios, intervención y controles de capitales (principal) · secundarias: TX-02, TX-07
- **Calidad Q:** 80 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 5/10 · Impacto 7/10 · Independencia 10/10 · Acceso 2/10
- **DOI / URL:** https://ideas.repec.org/a/eee/jimfin/v23y2004i5p701-733.html
- **Acceso y licencia:** Ficha libre en IDEAS; texto de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Jeffrey Frankel IDEAS RePEc author page Harvard Kennedy»; WebFetch: sí, índice https://ideas.repec.org/e/pfr12.html)
- **Contenido:** Mide la transmisión de los tipos de interés internacionales a los domésticos según el régimen: los tipos fijos transmiten más y más rápido, pero incluso los flotantes muestran transmisión sustancial a largo plazo.
- **Uso en el bloque:** TR-BCM: cuánto margen real tiene cada banco central frente a la Fed según su régimen; complemento de FXA-0244.
- **Limitaciones:** Resumen no leído en esta carga.

#### FXA-0249 · Q 80 (A) — Verifying exchange rate regimes

- **Autores:** Jeffrey Frankel; Eduardo Fajnzylber; Sergio L. Schmukler; Luis Servén
- **Año:** 2001
- **Publicación o institución:** Journal of Development Economics, vol. 66, n.º 2, págs. 351-386
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-08 Regímenes cambiarios, intervención y controles de capitales (principal) · secundarias: TX-10
- **Calidad Q:** 80 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 4/10 · Impacto 7/10 · Independencia 10/10 · Acceso 3/10
- **DOI / URL:** https://ideas.repec.org/a/eee/deveco/v66y2001i2p351-386.html · versión previa: «Verifiability and the Vanishing Intermediate Exchange Rate Regime», NBER WP 7901 (https://ideas.repec.org/p/nbr/nberwo/7901.html)
- **Acceso y licencia:** Ficha libre en IDEAS; texto de pago; WP NBER
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Jeffrey Frankel IDEAS RePEc author page Harvard Kennedy»; WebFetch: sí, índice https://ideas.repec.org/e/pfr12.html)
- **Contenido:** Estudia cuánto tiempo necesita un observador para verificar estadísticamente que un país cumple el régimen anunciado (cesta, banda): los regímenes intermedios complejos son poco verificables y por tanto menos creíbles.
- **Uso en el bloque:** AS-EMAS (cestas como la del SGD o la gestión del CNY) y TR-BCM: evaluar la credibilidad de regímenes intermedios anunciados.
- **Limitaciones:** Resumen no leído en esta carga.

#### FXA-0247 · Q 78 (B) — Trilemmas and trade-offs: living with financial globalisation

- **Autores:** Maurice Obstfeld
- **Año:** 2015
- **Publicación o institución:** BIS Working Papers n.º 480 (Banco de Pagos Internacionales)
- **Tipo de documento:** Documento de trabajo de organismo internacional
- **Temática:** TX-08 Regímenes cambiarios, intervención y controles de capitales (principal) · secundarias: TX-07, TX-10
- **Calidad Q:** 78 (B) — Tipo 18/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 7/10 · Independencia 8/10 · Acceso 7/10
- **DOI / URL:** https://ideas.repec.org/p/bis/biswps/480.html
- **Acceso y licencia:** Acceso abierto (BIS)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Maurice Obstfeld IDEAS RePEc author page»; WebFetch: sí, índice https://ideas.repec.org:443/e/pob13.html)
- **Contenido:** Responde al «dilema» de Rey: la flotación sigue dando cierto margen frente a los tipos cortos externos, aunque la globalización financiera reduce la autonomía sobre condiciones financieras largas y exige herramientas adicionales (macroprudenciales, de flujos).
- **Uso en el bloque:** TR-BCM y CONTRA: contrapeso de ANA-DOC-0303 al valorar el margen de los bancos centrales emergentes con flotación.
- **Limitaciones:** Documento de trabajo; resumen no leído.

#### FXA-0250 · Q 76 (B) — Systematic Managed Floating

- **Autores:** Jeffrey Frankel
- **Año:** 2019
- **Publicación o institución:** Open Economies Review, vol. 30, n.º 2, págs. 255-295
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-08 Regímenes cambiarios, intervención y controles de capitales (principal) · secundarias: TX-10
- **Calidad Q:** 76 (B) — Tipo 24/25 · Rigor 14/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 4/10 · Independencia 10/10 · Acceso 0/10
- **DOI / URL:** https://ideas.repec.org/a/kap/openec/v30y2019i2d10.1007_s11079-019-09528-8.html
- **Acceso y licencia:** Ficha libre en IDEAS; texto de pago (Springer)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Jeffrey Frankel IDEAS RePEc author page Harvard Kennedy»; WebFetch: sí, índice https://ideas.repec.org/e/pfr12.html)
- **Contenido:** Propone y estima la «flotación gestionada sistemática»: los bancos centrales emergentes intervienen con una regla que reparte las presiones del mercado entre tipo de cambio y reservas, y estima ese reparto por país.
- **Uso en el bloque:** TR-BCM, AS-EMAS, AS-EMLA, AS-EMEA: anticipar cuánto de una presión de salida se absorberá con reservas y cuánto con depreciación.
- **Limitaciones:** Resumen no leído en esta carga.

#### FXA-0231 · Q 76 (B) — Does reserve accumulation crowd out investment?

- **Autores:** Carmen M. Reinhart; Vincent Reinhart; Takeshi Tashiro
- **Año:** 2016
- **Publicación o institución:** Journal of International Money and Finance, vol. 63, págs. 89-111
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-08 Regímenes cambiarios, intervención y controles de capitales (principal) · secundarias: TX-10
- **Calidad Q:** 76 (B) — Tipo 25/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 7/10 · Impacto 5/10 · Independencia 10/10 · Acceso 0/10
- **DOI / URL:** https://ideas.repec.org/a/eee/jimfin/v63y2016icp89-111.html
- **Acceso y licencia:** Ficha libre en IDEAS; texto de pago (Elsevier)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Carmen Reinhart IDEAS RePEc profile research papers»; WebFetch: sí, índice https://ideas.repec.org/e/pre33.html)
- **Contenido:** Examina si la acumulación de reservas internacionales (vía intervención y esterilización) desplaza la inversión doméstica, como coste macroeconómico de la gestión del tipo de cambio.
- **Uso en el bloque:** AS-EMAS y TR-BCM: costes y límites de las políticas de acumulación de reservas que frenan la apreciación.
- **Limitaciones:** Resumen no leído en esta carga.

#### FXA-0277 · Q 76 (B) — How Reliable Are De Facto Exchange Rate Regime Classifications?

- **Autores:** Barry Eichengreen; Raul Razo-Garcia
- **Año:** 2013
- **Publicación o institución:** International Journal of Finance & Economics, vol. 18, n.º 3, págs. 216-239
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-08 Regímenes cambiarios, intervención y controles de capitales (principal) · secundarias: —
- **Calidad Q:** 76 (B) — Tipo 25/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 6/10 · Impacto 5/10 · Independencia 10/10 · Acceso 1/10
- **DOI / URL:** https://ideas.repec.org/a/wly/ijfiec/v18y2013i3p216-239.html
- **Acceso y licencia:** Ficha libre en IDEAS; texto de pago (Wiley)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Barry Eichengreen IDEAS RePEc author page»; WebFetch: sí, índice https://ideas.repec.org/e/pei2.html)
- **Contenido:** Compara las principales clasificaciones de facto de regímenes cambiarios (FMI, Reinhart-Rogoff, Levy-Yeyati-Sturzenegger…) y documenta discrepancias notables, sobre todo en emergentes y regímenes intermedios.
- **Uso en el bloque:** Analizador y AS-EMAS/AS-EMEA: no depender de una sola clasificación al determinar el régimen de una divisa (contrastar con ANA-DOC-0308).
- **Limitaciones:** Resumen no leído en esta carga.

#### FXA-0229 · Q 70 (B) — Goodbye Inflation Targeting, Hello Fear of Floating? Latin America after the Global Financial Crisis

- **Autores:** Carmen M. Reinhart
- **Año:** 2013
- **Publicación o institución:** MPRA Paper n.º 51282 (Munich Personal RePEc Archive)
- **Tipo de documento:** Documento de trabajo
- **Temática:** TX-08 Regímenes cambiarios, intervención y controles de capitales (principal) · secundarias: TX-10, TX-02
- **Calidad Q:** 70 (B) — Tipo 15/25 · Rigor 13/20 · Autoridad 15/15 · Vigencia 6/10 · Impacto 5/10 · Independencia 10/10 · Acceso 6/10
- **DOI / URL:** https://ideas.repec.org/p/pra/mprapa/51282.html
- **Acceso y licencia:** Acceso abierto (MPRA)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Carmen Reinhart IDEAS RePEc profile research papers»; WebFetch: sí, índice https://ideas.repec.org/e/pre33.html)
- **Contenido:** Analiza el regreso del «miedo a flotar» en América Latina tras 2008: bancos centrales con metas de inflación que intervienen y acumulan reservas para frenar apreciaciones.
- **Uso en el bloque:** AS-EMLA y TR-BCM: probabilidad de intervención de BCB, Banxico, BCCh, BanRep y BCRP ante apreciaciones o depreciaciones bruscas.
- **Limitaciones:** Documento breve de opinión técnica; resumen no leído.

## TX-09 Crisis cambiarias, devaluaciones y riesgo de cola

#### FXA-0297 · Q 93 (A) — Rare Disasters and Exchange Rates

- **Autores:** Emmanuel Farhi; Xavier Gabaix
- **Año:** 2016 (NBER WP 13805 de 2008)
- **Publicación o institución:** The Quarterly Journal of Economics, vol. 131, n.º 1, págs. 1-52
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-09 Crisis cambiarias, devaluaciones y riesgo de cola (principal) · secundarias: TX-04, TX-12
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / URL:** DOI: 10.1093/qje/qjv040 · https://ideas.repec.org:443/a/oup/qjecon/v131y2016i1p1-52..html · versión de trabajo: https://www.nber.org/papers/w13805 · página del autor: https://xgabaix.scholars.harvard.edu/publications/rare-disasters-and-exchange-rates
- **Acceso y licencia:** Ficha libre en IDEAS; WP NBER y copia del autor de acceso libre; artículo de pago (OUP)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Farhi Gabaix "Rare Disasters and Exchange Rates" Quarterly Journal of Economics»; WebFetch: sí, IDEAS)
- **Contenido:** Modelo en el que la probabilidad variable de desastres globales poco frecuentes y la exposición de cada país a ellos generan primas de riesgo que explican la volatilidad excesiva, la desconexión, el enigma de la prima a plazo, la rentabilidad del carry y su comovimiento con la bolsa; sus predicciones sobre opciones de divisas se cumplen empíricamente.
- **Uso en el bloque:** AS-ESTR, TR-PFV y CONTRA: interpretar el carry como compensación por riesgo de cola y usar las opciones (risk reversals) como indicador de riesgo de desastre por divisa.
- **Limitaciones:** Modelo calibrado; la medición de la exposición a desastres es indirecta.

#### FXA-0261 · Q 92 (A) — A Model of Balance-of-Payments Crises

- **Autores:** Paul Krugman
- **Año:** 1979
- **Publicación o institución:** Journal of Money, Credit and Banking, vol. 11, n.º 3, págs. 311-325
- **Tipo de documento:** Artículo revisado por pares (teórico, fundacional)
- **Temática:** TX-09 Crisis cambiarias, devaluaciones y riesgo de cola (principal) · secundarias: TX-08
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 5/10 · Impacto 10/10 · Independencia 10/10 · Acceso 9/10
- **DOI / URL:** DOI: 10.2307/1991793 · índice: https://en.wikipedia.org/wiki/Currency_crisis
- **Acceso y licencia:** Artículo de pago (JSTOR)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «currency crisis first generation model Krugman 1979 Obstfeld 1986 self-fulfilling second generation wikipedia»; WebFetch: sí, índice https://en.wikipedia.org/wiki/Currency_crisis)
- **Contenido:** Modelo de crisis de «primera generación»: un tipo fijo incompatible con una monetización persistente del déficit agota las reservas y termina en un ataque especulativo súbito y predecible cuando el tipo «sombra» supera la paridad.
- **Uso en el bloque:** Analistas de segmento emergentes (tipos fijos del Golfo, EGP, NGN) y CONTRA: comparar reservas y financiación monetaria del déficit para fechar el riesgo de ruptura de una paridad.
- **Limitaciones:** Modelo determinista sin expectativas autocumplidas ni balances bancarios.

#### ANA-DOC-0563 · Q 90 (A) — The Twin Crises: The Causes of Banking and Balance-of-Payments Problems

- **Autores:** Graciela L. Kaminsky; Carmen M. Reinhart
- **Año:** 1999
- **Publicación o institución:** American Economic Review, 89(3), 473–500
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-09 Crisis cambiarias, devaluaciones y riesgo de cola (principal) · secundarias: TX-10, TX-07
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** URL de acceso: https://authors.repec.org/pro/pre33 (perfil RePEc de C. M. Reinhart)
- **Acceso y licencia:** Peldaño 3 (revista; versiones de trabajo de la Fed abiertas)
- **Versión:** Versión publicada identificada en el perfil de la autora
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Carmen Reinhart RePEc author profile This Time is Different The Twin Crises»; WebFetch: sí, perfil)
- **Contenido:** Estudia la conexión entre crisis bancarias y cambiarias: las crisis bancarias suelen preceder a las cambiarias, que a su vez agravan las primeras; ambas siguen a liberalización financiera y auges de crédito; introduce el enfoque de señales.
- **Uso en el bloque:** TR-BCM y Analistas de segmento emergentes: secuencia liberalización financiera → crisis bancaria → crisis de balanza de pagos (crisis gemelas) como mapa de vulnerabilidad cambiaria; CONTRA: escenarios de devaluación con fragilidad bancaria.
- **Estatus epistémico:** Trabajo fundacional muy citado
- **Limitaciones:** DOI no visto; muestra de 1970–1995.

#### FXA-0262 · Q 90 (A) — Rational and Self-Fulfilling Balance-of-Payments Crises

- **Autores:** Maurice Obstfeld
- **Año:** 1986
- **Publicación o institución:** American Economic Review, vol. 76, n.º 1, págs. 72-81 (JSTOR 1804128)
- **Tipo de documento:** Artículo revisado por pares (teórico, fundacional)
- **Temática:** TX-09 Crisis cambiarias, devaluaciones y riesgo de cola (principal) · secundarias: TX-08
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 5/10 · Impacto 10/10 · Independencia 10/10 · Acceso 7/10
- **DOI / URL:** JSTOR 1804128 · índice: https://en.wikipedia.org/wiki/Currency_crisis
- **Acceso y licencia:** Artículo de pago (JSTOR/AEA)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «currency crisis first generation model Krugman 1979 Obstfeld 1986 self-fulfilling second generation wikipedia»; WebFetch: sí, índice https://en.wikipedia.org/wiki/Currency_crisis)
- **Contenido:** Origen de los modelos de «segunda generación»: si el gobierno cambia de política tras un ataque, pueden coexistir equilibrios múltiples y una crisis puede ser autocumplida aunque los fundamentos permitan sostener la paridad.
- **Uso en el bloque:** CONTRA y TR-BCM: reconocer zonas de vulnerabilidad en las que el sentimiento puede precipitar la ruptura de un ancla (relevante para EMEA y Asia con tipos gestionados).
- **Limitaciones:** Teórico; no predice cuándo ocurre el salto entre equilibrios.

#### ANA-DOC-0564 · Q 89 (A) — From Financial Crash to Debt Crisis

- **Autores:** Carmen M. Reinhart; Kenneth S. Rogoff
- **Año:** 2011
- **Publicación o institución:** American Economic Review, 101(5), 1676–1706
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-09 Crisis cambiarias, devaluaciones y riesgo de cola (principal) · secundarias: TX-10
- **Calidad Q:** 89 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 4/10
- **DOI / URL:** DOI: 10.1257/aer.101.5.1676 · URL de acceso: https://ideas.repec.org/a/aea/aecrev/v101y2011i5p1676-1706.html
- **Acceso y licencia:** Peldaño 3 (revista; versión NBER abierta)
- **Versión:** Versión de registro identificada
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Carmen Reinhart RePEc author profile From Financial Crash to Debt Crisis»; WebFetch: sí)
- **Contenido:** Con series históricas de deuda pública y externa, muestra que los auges de deuda externa preceden a crisis bancarias y que éstas predicen crisis de deuda soberana; la deuda interna infravalorada explica el aumento de deuda antes de los impagos.
- **Uso en el bloque:** TR-BCM y AS-EMEA/AS-EMLA: secuencia crisis financiera → crisis de deuda soberana y su efecto sobre la divisa (inflación, devaluación, controles); CONTRA: riesgo de cola soberano-cambiario.
- **Estatus epistémico:** Evidencia histórica revisada por pares
- **Limitaciones:** Los mismos autores tienen otro trabajo (2010, «Growth in a Time of Debt») con errores de cálculo documentados; no confundir.

#### ANA-DOC-0565 · Q 88 (A) — This Time Is Different: Eight Centuries of Financial Folly

- **Autores:** Carmen M. Reinhart; Kenneth S. Rogoff
- **Año:** 2009
- **Publicación o institución:** Princeton University Press
- **Tipo de documento:** Monografía de referencia
- **Temática:** TX-09 Crisis cambiarias, devaluaciones y riesgo de cola (principal) · secundarias: TX-10, TX-12
- **Calidad Q:** 88 (A) — Tipo 20/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 8/10
- **DOI / URL:** URL de acceso: https://authors.repec.org/pro/pre33 (perfil RePEc de C. M. Reinhart) · Chartbook complementario: https://ideas.repec.org/p/nbr/nberwo/15815.html
- **Acceso y licencia:** Peldaño 3 (libro de pago; datos y chartbook abiertos)
- **Versión:** Primera edición
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Carmen Reinhart RePEc author profile This Time is Different»; WebFetch: sí, perfil)
- **Contenido:** Historia cuantitativa de ocho siglos de impagos soberanos, crisis bancarias, inflación y crisis cambiarias en 66 países; patrones recurrentes y el síndrome de «esta vez es diferente».
- **Uso en el bloque:** CONTRA y Analistas de segmento emergentes: base histórica de crisis cambiarias, inflacionarias, bancarias y de deuda (frecuencia, secuencia y coste); refuerza la regla de no extrapolar periodos de calma («esta vez es diferente»).
- **Estatus epistémico:** Obra de referencia mundial
- **Limitaciones:** Libro; datos anteriores a 2009.

#### FXA-0263 · Q 88 (A) — A Model of Currency Crises in Emerging Markets

- **Autores:** Roberto Chang; Andrés Velasco
- **Año:** 2001
- **Publicación o institución:** Quarterly Journal of Economics, vol. 116, n.º 2, págs. 489-517
- **Tipo de documento:** Artículo revisado por pares (teórico)
- **Temática:** TX-09 Crisis cambiarias, devaluaciones y riesgo de cola (principal) · secundarias: TX-10
- **Calidad Q:** 88 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 5/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / URL:** DOI: 10.1162/00335530151144087 · índice: https://en.wikipedia.org/wiki/Currency_crisis
- **Acceso y licencia:** Artículo de pago (OUP)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «currency crisis first generation model Krugman 1979 Obstfeld 1986 self-fulfilling second generation wikipedia»; WebFetch: sí, índice https://en.wikipedia.org/wiki/Currency_crisis)
- **Contenido:** Modelo de «tercera generación» en el que la iliquidez internacional del sistema bancario (pasivos a corto en divisas frente a activos ilíquidos) genera pánicos bancarios que desembocan en crisis cambiarias.
- **Uso en el bloque:** AS-EMAS, AS-EMLA, AS-EMEA: incluir la liquidez en divisas del sistema bancario en la lente de riesgo y régimen.
- **Limitaciones:** Teórico; calibración empírica limitada.

#### FXA-0253 · Q 88 (A) — Currency crashes in emerging markets: an empirical treatment

- **Autores:** Jeffrey A. Frankel; Andrew K. Rose
- **Año:** 1996
- **Publicación o institución:** Board of Governors of the Federal Reserve System, International Finance Discussion Papers n.º 534 (publicado después en revista)
- **Tipo de documento:** Documento de trabajo de banco central (versión publicada muy citada)
- **Temática:** TX-09 Crisis cambiarias, devaluaciones y riesgo de cola (principal) · secundarias: TX-10, TX-13
- **Calidad Q:** 88 (A) — Tipo 21/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 5/10 · Impacto 10/10 · Independencia 10/10 · Acceso 10/10
- **DOI / URL:** https://ideas.repec.org/p/fip/fedgif/534.html
- **Acceso y licencia:** Acceso abierto (Reserva Federal)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Jeffrey Frankel IDEAS RePEc author page Harvard Kennedy»; WebFetch: sí, índice https://ideas.repec.org/e/pfr12.html)
- **Contenido:** Define «crash» cambiario (depreciación nominal de al menos el 25 % que supone una aceleración de al menos 10 puntos) y, con un probit sobre unos cien países en desarrollo, encuentra que la probabilidad aumenta con baja IED, reservas escasas, crecimiento del crédito, subidas de tipos del Norte y sobrevaloración real.
- **Uso en el bloque:** Analistas de segmento emergentes y CONTRA: definición operativa de crisis cambiaria y lista de indicadores de vulnerabilidad para el cribado de riesgo y régimen.
- **Limitaciones:** Datos anuales 1971-1992; la página índice no completa la referencia de la versión publicada.

#### FXA-0255 · Q 87 (A) — Can leading indicators assess country vulnerability? Evidence from the 2008–09 global financial crisis

- **Autores:** Jeffrey Frankel; George Saravelos
- **Año:** 2012 (NBER WP 16047 de 2010)
- **Publicación o institución:** Journal of International Economics, vol. 87, n.º 2, págs. 216-231
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-09 Crisis cambiarias, devaluaciones y riesgo de cola (principal) · secundarias: TX-10, TX-13
- **Calidad Q:** 87 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 9/10 · Independencia 10/10 · Acceso 4/10
- **DOI / URL:** https://ideas.repec.org/a/eee/inecon/v87y2012i2p216-231.html · versión de trabajo: https://ideas.repec.org/p/nbr/nberwo/16047.html
- **Acceso y licencia:** Ficha libre en IDEAS; WP NBER
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Jeffrey Frankel IDEAS RePEc author page Harvard Kennedy»; WebFetch: sí, índice https://ideas.repec.org/e/pfr12.html)
- **Contenido:** Revisa la literatura de indicadores adelantados y contrasta cuáles anticiparon la incidencia de la crisis de 2008-09 por país: las reservas y la sobrevaloración real previa son los más robustos.
- **Uso en el bloque:** Analistas de segmento emergentes y EVAL: priorizar reservas y REER en el cribado de vulnerabilidad cambiaria.
- **Limitaciones:** Un solo episodio global; resumen no leído en esta carga.

#### ANA-DOC-0570 · Q 84 (A) — Leading Indicators of Currency Crises

- **Autores:** Graciela Kaminsky; Saul Lizondo; Carmen M. Reinhart
- **Año:** 1998
- **Publicación o institución:** IMF Staff Papers, 45(1), 1–48
- **Tipo de documento:** Artículo revisado (revista del FMI)
- **Temática:** TX-09 Crisis cambiarias, devaluaciones y riesgo de cola (principal) · secundarias: TX-10, TX-13
- **Calidad Q:** 84 (A) — Tipo 23/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 10/10 · Independencia 9/10 · Acceso 5/10
- **DOI / URL:** URL de acceso: https://authors.repec.org/pro/pre33 (perfil RePEc de C. M. Reinhart)
- **Acceso y licencia:** Peldaño 2 (FMI; versiones abiertas)
- **Versión:** Versión publicada identificada en el perfil de la autora
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Carmen Reinhart RePEc author profile»; WebFetch: sí, perfil)
- **Contenido:** Revisa la literatura empírica de crisis cambiarias y propone el sistema de alerta temprana por «señales» con umbrales por indicador (reservas, tipo de cambio real, crédito, M2/reservas, etc.).
- **Uso en el bloque:** TR-BCM, AS-EMLA, AS-EMAS y AS-EMEA: método de «señales» (sobrevaloración real, caída de reservas, exportaciones, M2/reservas) para cribar riesgo de crisis cambiaria; EVAL: referencia de sistemas de alerta temprana.
- **Estatus epistémico:** Trabajo fundacional de alerta temprana
- **Limitaciones:** DOI no visto; capacidad predictiva fuera de muestra limitada.

#### FXA-0254 · Q 82 (A) — Contractionary Currency Crashes in Developing Countries

- **Autores:** Jeffrey A. Frankel
- **Año:** 2005
- **Publicación o institución:** IMF Staff Papers, vol. 52, n.º 2, págs. 149-192 (Mundell-Fleming Lecture) · versión de trabajo: NBER Working Papers n.º 11508
- **Tipo de documento:** Artículo revisado (conferencia publicada; con documento de trabajo NBER)
- **Temática:** TX-09 Crisis cambiarias, devaluaciones y riesgo de cola (principal) · secundarias: TX-10
- **Calidad Q:** 82 (A) — Tipo 22/25 · Rigor 14/20 · Autoridad 15/15 · Vigencia 5/10 · Impacto 7/10 · Independencia 10/10 · Acceso 9/10
- **DOI / URL:** DOI: 10.2307/30035893 · https://ideas.repec.org/p/nbr/nberwo/11508.html
- **Acceso y licencia:** Ficha libre en IDEAS; WP NBER
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsquedas web: «Jeffrey Frankel IDEAS RePEc author page Harvard Kennedy» y «currency crisis first generation model Krugman 1979…»; WebFetch: sí, índices https://ideas.repec.org/e/pfr12.html y https://en.wikipedia.org/wiki/Currency_crisis)
- **Contenido:** Analiza por qué las grandes devaluaciones en países en desarrollo suelen ser contractivas (efecto balance por deuda en divisas, traspaso a precios), frente a la visión clásica expansiva.
- **Uso en el bloque:** AS-EMLA, AS-EMEA y CONTRA: efectos de segunda ronda de una devaluación sobre crecimiento, banca y soberano.
- **Limitaciones:** Documento de trabajo; resumen no leído en esta carga.

#### FXA-0265 · Q 82 (A) — Government guarantees and self-fulfilling speculative attacks

- **Autores:** Craig Burnside; Martin Eichenbaum; Sergio Rebelo
- **Año:** 2004
- **Publicación o institución:** Journal of Economic Theory, vol. 119, págs. 31-63
- **Tipo de documento:** Artículo revisado por pares (teórico)
- **Temática:** TX-09 Crisis cambiarias, devaluaciones y riesgo de cola (principal) · secundarias: —
- **Calidad Q:** 82 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 5/10 · Impacto 6/10 · Independencia 10/10 · Acceso 3/10
- **DOI / URL:** DOI: 10.1016/j.jet.2003.06.002 · índice: https://en.wikipedia.org/wiki/Currency_crisis
- **Acceso y licencia:** Artículo de pago (Elsevier)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «currency crisis first generation model Krugman 1979 Obstfeld 1986 self-fulfilling second generation wikipedia»; WebFetch: sí, índice https://en.wikipedia.org/wiki/Currency_crisis)
- **Contenido:** Muestra que las garantías públicas a bancos con pasivos en divisas pueden hacer posibles ataques especulativos autocumplidos, ligando política fiscal futura, banca y régimen cambiario.
- **Uso en el bloque:** TR-BCM y CONTRA: valorar pasivos contingentes del soberano en el riesgo de devaluación.
- **Limitaciones:** Teórico; solapa parcialmente con FXA-0264.

#### FXA-0264 · Q 82 (A) — Hedging and financial fragility in fixed exchange rate regimes

- **Autores:** Craig Burnside; Martin Eichenbaum; Sergio Rebelo
- **Año:** 2001
- **Publicación o institución:** European Economic Review, vol. 45, n.º 7, págs. 1151-1193
- **Tipo de documento:** Artículo revisado por pares (teórico)
- **Temática:** TX-09 Crisis cambiarias, devaluaciones y riesgo de cola (principal) · secundarias: TX-08
- **Calidad Q:** 82 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 5/10 · Impacto 7/10 · Independencia 10/10 · Acceso 3/10
- **DOI / URL:** DOI: 10.1016/s0014-2921(01)00090-3 · índice: https://en.wikipedia.org/wiki/Currency_crisis
- **Acceso y licencia:** Artículo de pago (Elsevier)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «currency crisis first generation model Krugman 1979 Obstfeld 1986 self-fulfilling second generation wikipedia»; WebFetch: sí, índice https://en.wikipedia.org/wiki/Currency_crisis)
- **Contenido:** Las garantías públicas implícitas a la banca en regímenes de tipo fijo eliminan los incentivos a cubrir el riesgo cambiario, de modo que el sistema queda expuesto a una devaluación que se vuelve autocumplida.
- **Uso en el bloque:** CONTRA y Analistas de segmento emergentes: el descalce cambiario no cubierto como amplificador de crisis en regímenes con ancla.
- **Limitaciones:** Teórico.

#### FXA-0270 · Q 80 (A) — Imported or home grown? The 1992–3 EMS crisis

- **Autores:** Barry Eichengreen; Alain Naef
- **Año:** 2022
- **Publicación o institución:** Journal of International Economics, vol. 138
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-09 Crisis cambiarias, devaluaciones y riesgo de cola (principal) · secundarias: TX-08
- **Calidad Q:** 80 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 4/10 · Independencia 10/10 · Acceso 1/10
- **DOI / URL:** https://ideas.repec.org/a/eee/inecon/v138y2022ics0022199622000861.html
- **Acceso y licencia:** Ficha libre en IDEAS; texto de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Barry Eichengreen IDEAS RePEc author page»; WebFetch: sí, índice https://ideas.repec.org/e/pei2.html)
- **Contenido:** Reexamina la crisis del SME de 1992-93 para separar factores importados (choque alemán, tipos del Bundesbank) de vulnerabilidades domésticas en las divisas atacadas (GBP, ITL, SEK…).
- **Uso en el bloque:** AS-G10N y AS-EMEA (PLN, HUF, CZK con anclas implícitas al euro): lecciones sobre la defensa de bandas frente a choques del país ancla.
- **Limitaciones:** Resumen no leído en esta carga.

#### FXA-0269 · Q 80 (A) — The mother of all sudden stops: capital flows and reversals in Europe, 1919–32

- **Autores:** Olivier Accominotti; Barry Eichengreen
- **Año:** 2016 (NBER WP 19580 de 2013)
- **Publicación o institución:** Economic History Review, vol. 69, n.º 2, págs. 469-492
- **Tipo de documento:** Artículo revisado por pares (historia económica)
- **Temática:** TX-09 Crisis cambiarias, devaluaciones y riesgo de cola (principal) · secundarias: TX-07
- **Calidad Q:** 80 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 6/10 · Impacto 6/10 · Independencia 10/10 · Acceso 2/10
- **DOI / URL:** https://ideas.repec.org/a/bla/ehsrev/v69y2016i2p469-492.html · versión de trabajo: https://ideas.repec.org/p/nbr/nberwo/19580.html
- **Acceso y licencia:** Ficha libre en IDEAS; WP NBER
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Barry Eichengreen IDEAS RePEc author page»; WebFetch: sí, índice https://ideas.repec.org/e/pei2.html)
- **Contenido:** Reconstruye los flujos de capital hacia Europa en entreguerras y su brusca reversión en 1929-32, mostrando el papel de los factores globales (push) en la mayor parada súbita de la historia moderna.
- **Uso en el bloque:** CONTRA y PROS: escenario extremo de parada súbita global para pruebas de estrés en H4.
- **Limitaciones:** Contexto histórico de patrón oro.

#### FXA-0266 · Q 80 (A) — Currency Regimes, Capital Flows, and Crises

- **Autores:** Paul Krugman
- **Año:** 2014
- **Publicación o institución:** IMF Economic Review, vol. 62, n.º 4, págs. 470-493 (26 de agosto de 2014)
- **Tipo de documento:** Artículo revisado
- **Temática:** TX-09 Crisis cambiarias, devaluaciones y riesgo de cola (principal) · secundarias: TX-08, TX-07
- **Calidad Q:** 80 (A) — Tipo 22/25 · Rigor 13/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 8/10 · Independencia 10/10 · Acceso 4/10
- **DOI / URL:** DOI: 10.1057/imfer.2014.9 · índice: https://en.wikipedia.org/wiki/Currency_crisis
- **Acceso y licencia:** Artículo de pago (Palgrave)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «currency crisis first generation model Krugman 1979 Obstfeld 1986 self-fulfilling second generation wikipedia»; WebFetch: sí, índice https://en.wikipedia.org/wiki/Currency_crisis)
- **Contenido:** Contrasta las paradas súbitas en países con divisa propia y flotación (donde la depreciación amortigua) frente a los de la zona del euro (sin tipo de cambio propio), revisando la teoría de crisis tras 2008.
- **Uso en el bloque:** TR-BCM y AS-G10N/AS-EMEA: por qué los países con divisa propia y deuda en su moneda resisten mejor las paradas súbitas.
- **Limitaciones:** Ensayo; texto no leído.

#### FXA-0256 · Q 80 (A) — Does openness to trade make countries more vulnerable to sudden stops, or less? Using gravity to establish causality

- **Autores:** Eduardo A. Cavallo; Jeffrey A. Frankel
- **Año:** 2008
- **Publicación o institución:** Journal of International Money and Finance, vol. 27, n.º 8, págs. 1430-1452
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-09 Crisis cambiarias, devaluaciones y riesgo de cola (principal) · secundarias: TX-07, TX-10
- **Calidad Q:** 80 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 5/10 · Impacto 7/10 · Independencia 10/10 · Acceso 2/10
- **DOI / URL:** https://ideas.repec.org/a/eee/jimfin/v27y2008i8p1430-1452.html
- **Acceso y licencia:** Ficha libre en IDEAS; texto de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Jeffrey Frankel IDEAS RePEc author page Harvard Kennedy»; WebFetch: sí, índice https://ideas.repec.org/e/pfr12.html)
- **Contenido:** Usando la apertura comercial predicha por un modelo de gravedad como instrumento, concluye que una mayor apertura reduce la vulnerabilidad a paradas súbitas y crisis cambiarias, porque el ajuste exige menos depreciación real.
- **Uso en el bloque:** Analistas de segmento emergentes: apertura comercial como mitigante en la lente de riesgo y régimen.
- **Limitaciones:** Resumen no leído en esta carga.

#### FXA-0267 · Q 78 (B) — Default, Currency Crises, and Sovereign Credit Ratings

- **Autores:** Carmen M. Reinhart
- **Año:** 2002
- **Publicación o institución:** World Bank Economic Review, vol. 16, n.º 2, págs. 151-170
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-09 Crisis cambiarias, devaluaciones y riesgo de cola (principal) · secundarias: TX-10, TX-14
- **Calidad Q:** 78 (B) — Tipo 25/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 5/10 · Impacto 7/10 · Independencia 9/10 · Acceso 2/10
- **DOI / URL:** DOI: 10.1093/wber/16.2.151 · índice: https://en.wikipedia.org/wiki/Currency_crisis
- **Acceso y licencia:** Artículo de pago (OUP); WBER con acceso variable
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «currency crisis first generation model Krugman 1979 Obstfeld 1986 self-fulfilling second generation wikipedia»; WebFetch: sí, índice https://en.wikipedia.org/wiki/Currency_crisis)
- **Contenido:** Documenta el vínculo entre impagos soberanos y crisis cambiarias en emergentes y que las calificaciones soberanas reaccionan tarde, sin anticipar las crisis cambiarias.
- **Uso en el bloque:** AS-EMLA, AS-EMEA y CONTRA: no fiarse de las calificaciones como alerta temprana; vínculo deuda-divisa.
- **Limitaciones:** Muestra de los noventa.

#### FXA-0271 · Q 76 (B) — Managing Sudden Stops

- **Autores:** Barry Eichengreen; Poonam Gupta
- **Año:** 2018 (World Bank Policy Research WP 7639 de 2016)
- **Publicación o institución:** En Monetary Policy and Global Spillovers (Banco Central de Chile, serie de libros), págs. 9-47
- **Tipo de documento:** Capítulo de libro de banco central
- **Temática:** TX-09 Crisis cambiarias, devaluaciones y riesgo de cola (principal) · secundarias: TX-07, TX-10
- **Calidad Q:** 76 (B) — Tipo 18/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 8/10 · Impacto 5/10 · Independencia 8/10 · Acceso 8/10
- **DOI / URL:** https://ideas.repec.org/h/chb/bcchsb/v25c02pp009-047.html · versión de trabajo: https://ideas.repec.org/p/wbk/wbrwps/7639.html
- **Acceso y licencia:** Acceso abierto (Banco Central de Chile y Banco Mundial)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Barry Eichengreen IDEAS RePEc author page»; WebFetch: sí, índice https://ideas.repec.org/e/pei2.html)
- **Contenido:** Identifica paradas súbitas en emergentes desde los noventa y evalúa qué respuestas de política (uso de reservas, depreciación, subidas de tipos, medidas macroprudenciales) moderan su impacto.
- **Uso en el bloque:** TR-BCM y Analistas de segmento emergentes: anticipar la reacción del banco central ante una parada súbita.
- **Limitaciones:** Resumen no leído en esta carga.

#### FXA-0232 · Q 76 (B) — A Series of Unfortunate Events: Common Sequencing Patterns in Financial Crises

- **Autores:** Carmen M. Reinhart
- **Año:** 2012 (CEPR DP 8742; versión en Rivista di Politica Economica, 2011, n.º 4, págs. 11-36)
- **Publicación o institución:** CEPR Discussion Paper n.º 8742 · Rivista di Politica Economica
- **Tipo de documento:** Documento de trabajo y artículo de revista
- **Temática:** TX-09 Crisis cambiarias, devaluaciones y riesgo de cola (principal) · secundarias: TX-07
- **Calidad Q:** 76 (B) — Tipo 19/25 · Rigor 14/20 · Autoridad 15/15 · Vigencia 6/10 · Impacto 6/10 · Independencia 10/10 · Acceso 6/10
- **DOI / URL:** https://ideas.repec.org/p/cpr/ceprdp/8742.html · https://ideas.repec.org/a/rpo/ripoec/y2011i4p11-36.html
- **Acceso y licencia:** Fichas libres en IDEAS
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Carmen Reinhart IDEAS RePEc profile research papers»; WebFetch: sí, índice https://ideas.repec.org/e/pre33.html)
- **Contenido:** Describe la secuencia típica de las crisis financieras (bonanza de entradas, auge de crédito, crisis bancaria, crisis cambiaria, crisis de deuda e inflación) a partir de la base histórica Reinhart-Rogoff.
- **Uso en el bloque:** CONTRA y Analistas de segmento emergentes: ubicar a cada país en la secuencia para fechar el riesgo de devaluación.
- **Limitaciones:** Patrón estilizado; no es un modelo predictivo calibrado.

#### FXA-0268 · Q 74 (B) — Currency crisis models (New Palgrave Dictionary of Economics, 2.ª ed.)

- **Autores:** Craig Burnside; Martin Eichenbaum; Sergio Rebelo
- **Año:** 2008
- **Publicación o institución:** The New Palgrave Dictionary of Economics, 2.ª edición (Palgrave Macmillan)
- **Tipo de documento:** Entrada de diccionario académico (survey)
- **Temática:** TX-09 Crisis cambiarias, devaluaciones y riesgo de cola (principal) · secundarias: —
- **Calidad Q:** 74 (B) — Tipo 18/25 · Rigor 13/20 · Autoridad 15/15 · Vigencia 5/10 · Impacto 6/10 · Independencia 10/10 · Acceso 7/10
- **DOI / URL:** índice: https://en.wikipedia.org/wiki/Currency_crisis · copia de autor devuelta por la búsqueda: https://www.kellogg.northwestern.edu/faculty/rebelo/htm/currency crisis models Ed.pdf
- **Acceso y licencia:** Copia de autor en la web de Kellogg (resultado de búsqueda)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «currency crisis first generation model Krugman 1979 Obstfeld 1986 self-fulfilling second generation wikipedia»; WebFetch: sí, índice https://en.wikipedia.org/wiki/Currency_crisis)
- **Contenido:** Síntesis de las tres generaciones de modelos de crisis cambiarias (déficit monetizado, equilibrios múltiples, balances bancarios y garantías) y de sus implicaciones.
- **Uso en el bloque:** DOC-A y Analistas de segmento: guía rápida para clasificar el tipo de vulnerabilidad de un país.
- **Limitaciones:** Entrada de diccionario; no aporta evidencia nueva.

#### FXA-0233 · Q 72 (B) — Financial crises: past and future

- **Autores:** Carmen M. Reinhart
- **Año:** 2019
- **Publicación o institución:** Business Economics, vol. 54, n.º 1, págs. 3-15 (Palgrave Macmillan)
- **Tipo de documento:** Artículo (conferencia publicada en revista de la NABE)
- **Temática:** TX-09 Crisis cambiarias, devaluaciones y riesgo de cola (principal) · secundarias: TX-10
- **Calidad Q:** 72 (B) — Tipo 18/25 · Rigor 12/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 5/10 · Independencia 10/10 · Acceso 4/10
- **DOI / URL:** DOI: 10.1057/s11369-018-00113-4 · https://ideas.repec.org/a/pal/buseco/v54y2019i1d10.1057_s11369-018-00113-4.html
- **Acceso y licencia:** Ficha libre en IDEAS; texto de pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Carmen Reinhart IDEAS RePEc profile research papers»; WebFetch: sí, índice https://ideas.repec.org/e/pre33.html)
- **Contenido:** Repaso de las regularidades históricas de las crisis financieras y de las vulnerabilidades emergentes de cara al futuro (deuda, emergentes, dólar).
- **Uso en el bloque:** CONTRA y PROS: lista de vulnerabilidades para escenarios de cola en H3–H4.
- **Limitaciones:** Texto divulgativo; resumen no leído.

## TX-10 Divisas emergentes

#### FXA-0295 · Q 88 (A) — Local Currency Sovereign Risk

- **Autores:** Wenxin Du; Jesse Schreger
- **Año:** 2013 (documento de trabajo; la versión publicada en revista no se ha consultado)
- **Publicación o institución:** Board of Governors of the Federal Reserve System, International Finance Discussion Papers n.º 1094 (diciembre de 2013)
- **Tipo de documento:** Documento de trabajo de banco central
- **Temática:** TX-10 Divisas emergentes (principal) · secundarias: TX-04, TX-09
- **Calidad Q:** 88 (A) — Tipo 21/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 9/10 · Independencia 8/10 · Acceso 9/10
- **DOI / URL:** https://www.federalreserve.gov/econres/ifdp/local-currency-sovereign-risk.htm · PDF: https://federalreserve.gov/PubS/ifdp/2013/1094/ifdp1094.pdf
- **Acceso y licencia:** Acceso abierto (Reserva Federal)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Du Schreger "Local Currency Sovereign Risk" Journal of Finance 2016»; WebFetch: sí, página IFDP)
- **Contenido:** Define el diferencial de crédito en moneda local (rendimiento del bono local frente a un tipo libre de riesgo sintético construido con swaps de divisas): es positivo y sustancial, menor y menos correlacionado entre países que el de la deuda en divisas, y más ligado a la aversión al riesgo y la liquidez globales que a los fundamentos.
- **Uso en el bloque:** AS-EMLA, AS-EMAS, AS-EMEA y MOTOR: separar en el carry de una divisa emergente la prima cambiaria de la prima de crédito soberano en moneda local.
- **Limitaciones:** Versión de trabajo de 2013; referencia de la versión publicada no verificada.

#### FXA-0272 · Q 86 (A) — Yet it Endures: The Persistence of Original Sin

- **Autores:** Barry Eichengreen; Ricardo Hausmann; Ugo Panizza
- **Año:** 2023 (CID Working Paper 420 de 2022)
- **Publicación o institución:** Open Economies Review, vol. 34, n.º 1, págs. 1-42
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-10 Divisas emergentes (principal) · secundarias: TX-09, TX-07
- **Calidad Q:** 86 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 7/10 · Independencia 10/10 · Acceso 3/10
- **DOI / URL:** https://ideas.repec.org/a/kap/openec/v34y2023i1d10.1007_s11079-022-09704-3.html · versión de trabajo: https://ideas.repec.org/p/cid/wpfacu/420.html
- **Acceso y licencia:** Ficha libre en IDEAS; WP de Harvard CID de acceso abierto
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Barry Eichengreen IDEAS RePEc author page»; WebFetch: sí, índice https://ideas.repec.org/e/pei2.html)
- **Contenido:** Revisa el «pecado original» (incapacidad de endeudarse en el exterior en moneda propia) dos décadas después: pese al desarrollo de mercados de deuda local, la mayoría de emergentes sigue sin poder hacerlo a escala y el descalce persiste en otras formas (inversores extranjeros en deuda local, sector corporativo).
- **Uso en el bloque:** AS-EMAS, AS-EMLA, AS-EMEA y CONTRA: descalce de monedas y dependencia de inversores extranjeros como amplificadores de ventas masivas de divisas emergentes.
- **Limitaciones:** Resumen no leído en esta carga.

#### FXA-0259 · Q 86 (A) — A Tie That Binds: Revisiting the Trilemma in Emerging Market Economies

- **Autores:** Maurice Obstfeld; Jonathan D. Ostry; Mahvash S. Qureshi
- **Año:** 2019
- **Publicación o institución:** Review of Economics and Statistics, vol. 101, n.º 2, págs. 279-293
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-10 Divisas emergentes (principal) · secundarias: TX-08, TX-07
- **Calidad Q:** 86 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 9/10 · Acceso 3/10
- **DOI / URL:** https://ideas.repec.org/a/tpr/restat/v101y2019i2p279-293.html
- **Acceso y licencia:** Ficha libre en IDEAS; texto de pago (MIT Press); versión de trabajo del FMI
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Maurice Obstfeld IDEAS RePEc author page»; WebFetch: sí, índice https://ideas.repec.org:443/e/pob13.html)
- **Contenido:** Con unos 40 emergentes, muestra que los shocks financieros globales (VIX) se transmiten con más fuerza al crédito, precios de activos y tipos domésticos en países con tipo de cambio fijo que en los de flotación: el régimen cambiario sigue importando.
- **Uso en el bloque:** AS-EMAS, AS-EMLA, AS-EMEA y TR-BCM: valorar el papel amortiguador de la flotación en episodios de aversión al riesgo.
- **Limitaciones:** Resumen no leído en esta carga.

#### FXA-0285 · Q 86 (A) — Bond risk premia and the exchange rate

- **Autores:** Boris Hofmann; Ilhyock Shim; Hyun Song Shin
- **Año:** 2019 (18 de marzo)
- **Publicación o institución:** BIS Working Papers n.º 775 (Banco de Pagos Internacionales)
- **Tipo de documento:** Documento de trabajo de organismo internacional
- **Temática:** TX-10 Divisas emergentes (principal) · secundarias: TX-07, TX-12
- **Calidad Q:** 86 (A) — Tipo 19/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 8/10 · Acceso 9/10
- **DOI / URL:** https://www.bis.org/publ/work775.htm
- **Acceso y licencia:** Acceso abierto (BIS)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Hofmann Shim Shin "Bond risk premia and the exchange rate" emerging market BIS working paper»; WebFetch: sí)
- **Contenido:** En emergentes, una divisa más fuerte frente al USD coincide con diferenciales soberanos más bajos, incluso en bonos en moneda local, por una menor prima de riesgo de crédito; lo relevante es el tipo bilateral frente al dólar, no el efectivo, porque los inversores globales miden su rentabilidad en dólares.
- **Uso en el bloque:** AS-EMLA, AS-EMAS, AS-EMEA: correlación divisa-diferencial y amplificación de ventas cuando se fortalece el dólar; TR-PFV: canal de inversores en deuda local.
- **Limitaciones:** Documento de trabajo; no consta versión publicada en la página.

#### FXA-0296 · Q 86 (A) — US Monetary Policy and International Risk Spillovers

- **Autores:** Sebnem Kalemli-Özcan
- **Año:** 2019 (octubre)
- **Publicación o institución:** CEPR Discussion Papers n.º 14053 · ponencia del simposio de Jackson Hole 2019 (Federal Reserve Bank of Kansas City)
- **Tipo de documento:** Documento de trabajo (ponencia de simposio de banco central)
- **Temática:** TX-10 Divisas emergentes (principal) · secundarias: TX-07, TX-02
- **Calidad Q:** 86 (A) — Tipo 19/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 9/10 · Acceso 8/10
- **DOI / URL:** https://econpapers.repec.org/paper/cprceprdp/14053.htm · versión CEPR: https://repec.cepr.org/repec/cpr/ceprdp/DP14053.pdf · discusión: https://www.kansascityfed.org/documents/6953/GD_US_MonetaryPolicyRiskSpillover_JH2019.pdf
- **Acceso y licencia:** Acceso libre (CEPR/Kansas City Fed)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Kalemli-Özcan 2019 "U.S. Monetary Policy and International Risk Spillovers" Jackson Hole emerging markets»; WebFetch: sí, EconPapers)
- **Contenido:** La política monetaria de EE. UU. tiene efectos de contagio mayores en emergentes que en avanzadas a través de las percepciones de riesgo de los inversores globales, que mueven flujos y diferenciales de crédito; el traspaso del tipo oficial a los tipos a corto es imperfecto y las políticas para limitar la volatilidad cambiaria pueden ser contraproducentes.
- **Uso en el bloque:** TR-BCM y Analistas de segmento emergentes: canal de prima de riesgo de la Fed hacia las divisas emergentes; CONTRA: objeción a defensas cambiarias rígidas.
- **Limitaciones:** Documento de trabajo.

#### FXA-0299 · Q 86 (A) — International financial spillovers to emerging market economies: How important are economic fundamentals?

- **Autores:** Shaghil Ahmed; Brahima Coulibaly; Andrei Zlate
- **Año:** 2017 (IFDP 1135 de 2015)
- **Publicación o institución:** Journal of International Money and Finance, vol. 76, págs. 133-152
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-10 Divisas emergentes (principal) · secundarias: TX-07, TX-09
- **Calidad Q:** 86 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 8/10 · Impacto 7/10 · Independencia 9/10 · Acceso 6/10
- **DOI / URL:** DOI: 10.1016/j.jimonfin.2017.05.001 · https://ideas.repec.org:443/a/eee/jimfin/v76y2017icp133-152.html · versión de trabajo: https://www.federalreserve.gov/econres/ifdp/international-financial-spillovers-to-emerging-market-economies-how-important-are-economic-fundamentals.htm
- **Acceso y licencia:** Versión de trabajo de la Reserva Federal de acceso abierto; artículo de pago
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Ahmed Coulibaly Zlate "International financial spillovers to emerging market economies: How important are economic fundamentals?"»; WebFetch: sí, IDEAS)
- **Contenido:** En el «taper tantrum» de 2013 los emergentes con mejores fundamentos sufrieron menos, y los que habían recibido más entradas y más apreciación previa sufrieron más; la diferenciación por fundamentos aparece también en 2008, 2011 y 2015, pero no en las crisis de los noventa.
- **Uso en el bloque:** Analistas de segmento emergentes y CONTRA: ordenar divisas por vulnerabilidad (fundamentos, entradas y apreciación previas) ante choques globales.
- **Limitaciones:** Regresiones de corte transversal por episodio.

#### FXA-0300 · Q 84 (A) — What Drives Capital Flows To Emerging Markets? A Survey Of The Empirical Literature

- **Autores:** Robin Koepke
- **Año:** 2019 (MPRA 62770 de 2015)
- **Publicación o institución:** Journal of Economic Surveys, vol. 33, n.º 2, págs. 516-540 (Wiley)
- **Tipo de documento:** Artículo de revisión (survey) revisado por pares
- **Temática:** TX-10 Divisas emergentes (principal) · secundarias: TX-07
- **Calidad Q:** 84 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 12/15 · Vigencia 8/10 · Impacto 8/10 · Independencia 9/10 · Acceso 6/10
- **DOI / URL:** DOI: 10.1111/joes.12273 · https://ideas.repec.org/a/bla/jecsur/v33y2019i2p516-540.html · versión de trabajo: https://ideas.repec.org/p/pra/mprapa/62770.html
- **Acceso y licencia:** Versión de trabajo en MPRA de acceso libre; artículo de pago
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Koepke "What Drives Capital Flows to Emerging Markets? A Survey of the Empirical Literature" Journal of Economic Surveys»; WebFetch: sí, IDEAS)
- **Contenido:** Survey de los determinantes de los flujos hacia emergentes en el marco push/pull: los factores externos (aversión global al riesgo, tipos exteriores) pesan más en los flujos de cartera de deuda y acciones; los internos (crecimiento, rentabilidades, riesgo país) afectan a todos y sobre todo a los bancarios.
- **Uso en el bloque:** TR-PFV y Analistas de segmento emergentes: qué variables vigilar según el tipo de flujo que financia a cada divisa.
- **Limitaciones:** Revisión de literatura hasta mediados de los 2010.

#### FXA-0273 · Q 84 (A) — Tapering talk: The impact of expectations of reduced Federal Reserve security purchases on emerging markets

- **Autores:** Barry Eichengreen; Poonam Gupta
- **Año:** 2015 (World Bank WP 6754 de 2014)
- **Publicación o institución:** Emerging Markets Review, vol. 25, págs. 1-15
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-10 Divisas emergentes (principal) · secundarias: TX-07, TX-02
- **Calidad Q:** 84 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 7/10 · Impacto 9/10 · Independencia 10/10 · Acceso 3/10
- **DOI / URL:** https://ideas.repec.org/a/eee/ememar/v25y2015icp1-15.html · versión de trabajo: https://ideas.repec.org/p/wbk/wbrwps/6754.html
- **Acceso y licencia:** Ficha libre en IDEAS; WP del Banco Mundial de acceso abierto
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Barry Eichengreen IDEAS RePEc author page»; WebFetch: sí, índice https://ideas.repec.org/e/pei2.html)
- **Contenido:** Analiza el «taper tantrum» de 2013: los emergentes con mercados financieros más grandes y líquidos y con mayor apreciación real y déficit previos sufrieron más depreciación, salidas y caídas bursátiles; los fundamentos macro pesaron menos de lo esperado.
- **Uso en el bloque:** Analistas de segmento emergentes y TR-PFV: qué divisas sufren más ante un endurecimiento esperado de la Fed (liquidez del mercado como canal de venta).
- **Limitaciones:** Un solo episodio; resumen no leído en esta carga.

#### FXA-0236 · Q 84 (A) — Managers, Investors, and Crises: Mutual Fund Strategies in Emerging Markets

- **Autores:** Graciela Kaminsky; Richard K. Lyons; Sergio Schmukler
- **Año:** 2004
- **Publicación o institución:** Journal of International Economics, vol. 64, págs. 113-134
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-10 Divisas emergentes (principal) · secundarias: TX-07, TX-09
- **Calidad Q:** 84 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 5/10 · Impacto 8/10 · Independencia 10/10 · Acceso 4/10
- **DOI / URL:** https://faculty.haas.berkeley.edu/lyons/pubabs.html (índice de publicaciones de R. K. Lyons)
- **Acceso y licencia:** Artículo de pago (Elsevier)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Evans Lyons 2002 "Order Flow and Exchange Rate Dynamics" Journal of Political Economy»; WebFetch: sí, índice https://faculty.haas.berkeley.edu/lyons/pubabs.html)
- **Contenido:** Con datos de carteras de fondos de inversión en emergentes, separa las decisiones de gestores y de partícipes (reembolsos) y muestra conductas de momentum y contagio en las crisis (venta de países no afectados).
- **Uso en el bloque:** TR-PFV y Analistas de segmento emergentes: canal de contagio vía fondos dedicados que afecta a divisas emergentes no relacionadas.
- **Limitaciones:** Datos de los noventa; estructura de inversores emergentes distinta hoy (ETF, índices).

#### FXA-0286 · Q 82 (A) — Risk capacity, portfolio choice and exchange rates

- **Autores:** Boris Hofmann; Ilhyock Shim; Hyun Song Shin
- **Año:** 2022 (julio)
- **Publicación o institución:** BIS Working Papers n.º 1031
- **Tipo de documento:** Documento de trabajo de organismo internacional
- **Temática:** TX-10 Divisas emergentes (principal) · secundarias: TX-07
- **Calidad Q:** 82 (A) — Tipo 19/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 5/10 · Independencia 8/10 · Acceso 8/10
- **DOI / URL:** https://www.bis.org/RePEc/bis/biswps/work1031.redif · PDF: https://www.bis.org/publ/work1031.pdf
- **Acceso y licencia:** Acceso abierto (BIS)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Hofmann Shim Shin "Bond risk premia and the exchange rate" emerging market BIS working paper»; WebFetch: sí, registro RePEc del BIS)
- **Contenido:** Con un modelo de elección de cartera con restricción de VaR, las oscilaciones cambiarias alteran la capacidad de riesgo de los inversores globales en bonos locales emergentes aunque no haya descalces; una apreciación frente al USD se asocia a entradas en fondos de bonos y menores diferenciales, con efecto mucho mayor si es generalizada (dólar amplio) que si es idiosincrásica.
- **Uso en el bloque:** AS-EMLA, AS-EMAS, AS-EMEA y AS-ESTR: el índice amplio del dólar como variable de estado para los flujos hacia deuda local emergente.
- **Limitaciones:** Documento de trabajo.

#### FXA-0298 · Q 82 (A) — Original Sin Redux: A Model-Based Evaluation

- **Autores:** Boris Hofmann; Nikhil Patel; Steve Pak Yeung Wu
- **Año:** 2022 (22 de febrero)
- **Publicación o institución:** BIS Working Papers n.º 1004 (Banco de Pagos Internacionales)
- **Tipo de documento:** Documento de trabajo de organismo internacional
- **Temática:** TX-10 Divisas emergentes (principal) · secundarias: TX-08, TX-07
- **Calidad Q:** 82 (A) — Tipo 19/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 5/10 · Independencia 8/10 · Acceso 8/10
- **DOI / URL:** https://www.bis.org/publ/work1004.pdf · resumen: https://mondovisione.com/media-and-resources/news/bis-original-sin-redux-a-model-based-evaluation-2022222/
- **Acceso y licencia:** Acceso abierto (BIS)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Carstens Shin "Emerging Markets Aren't Out of the Woods Yet" Foreign Affairs 2019 original sin redux»; WebFetch: sí, reseña de Mondo Visione con el resumen del BIS)
- **Contenido:** El «pecado original redux»: aunque los emergentes se endeuden en moneda propia, el endurecimiento monetario en avanzadas sigue transmitiéndose al restringir a los prestamistas extranjeros, y el descalce se traslada a sus balances; la intervención cambiaria y las medidas sobre flujos alivian a corto plazo y una base inversora local más profunda reduce la vulnerabilidad a largo.
- **Uso en el bloque:** AS-EMLA, AS-EMAS, AS-EMEA: vulnerabilidad de divisas con alta tenencia extranjera de deuda local; TR-BCM: respuesta esperada (intervención, medidas sobre flujos).
- **Limitaciones:** Documento de trabajo basado en modelo; resumen leído en una reseña de terceros, no en la web del BIS.

#### ANA-DOC-0050 · Q 82 (A) — Understanding Inflation in Emerging and Developing Economies

- **Autores:** Jongrim Ha; M. Ayhan Kose; Franziska L. Ohnsorge
- **Año:** 2019 (febrero)
- **Publicación o institución:** Banco Mundial (Policy Research Working Paper 8761)
- **Tipo de documento:** Documento de trabajo institucional
- **Temática:** TX-10 Divisas emergentes (principal) · secundarias: TX-02
- **Calidad Q:** 82 (A) — Tipo 20/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 6/10 · Independencia 9/10 · Acceso 9/10
- **DOI / URL:** DOI 10.1596/1813-9450-8761 · https://openknowledge.worldbank.org/entities/publication/3c7413ba-ecf0-54b0-b1ce-6a107842cdfa/full · Handle: https://hdl.handle.net/10986/31338
- **Acceso y licencia:** Peldaño 1 (repositorio abierto del Banco Mundial) · Licencia: Copyright Banco Mundial; acceso abierto
- **Versión:** Publicada (PRWP 8761, febrero de 2019); resumen técnico del libro ANA-DOC-0047
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Ha Kose Ohnsorge "Understanding Inflation in Emerging and Developing Economies" Policy Research Working Paper 8761»; WebFetch: sí)
- **Contenido:** Síntesis técnica (versión de trabajo) de la dinámica de la inflación en emergentes: determinantes globales, expectativas y régimen de política.
- **Uso en el bloque:** TR-BCM y Analistas de segmento emergentes (AS-EMAS, AS-EMLA, AS-EMEA): determinantes de la inflación en emergentes (incluido el traspaso del tipo de cambio) para valorar la credibilidad del banco central y la sostenibilidad del carry.
- **Estatus epistémico:** Documento de trabajo institucional; nivel alto (complemento del libro)
- **Limitaciones:** Véase el libro asociado para el tratamiento completo; redundancia parcial con ANA-DOC-0047
- **Disciplinas y etiquetas:** Inflación; economías emergentes · bloque-1; inflacion; emergentes; banco-mundial
- **Verificación V2.7:** Completa (lote del operador, 26/10/2026). REPARACIÓN 2026-11-02: el registro del OKR (leído con WebFetch) confirma título, autores, PRWP 8761, febrero de 2019, DOI 10.1596/1813-9450-8761 y handle propio 10986/31338; se retira el handle 10986/30657 (libro de ANA-DOC-0047). Nota cruzada: el handle 10986/31338 figuraba por error en ANA-DOC-0032. Acceso pasa de 6 a 9; nivel B → A. Alerta resuelta.

#### FXA-0257 · Q 82 (A) — Monetary Policy in Emerging Markets: A Survey

- **Autores:** Jeffrey A. Frankel
- **Año:** 2010
- **Publicación o institución:** NBER Working Papers n.º 16125
- **Tipo de documento:** Documento de trabajo (survey)
- **Temática:** TX-10 Divisas emergentes (principal) · secundarias: TX-02, TX-08
- **Calidad Q:** 82 (A) — Tipo 20/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 6/10 · Impacto 8/10 · Independencia 10/10 · Acceso 8/10
- **DOI / URL:** https://ideas.repec.org/p/nbr/nberwo/16125.html
- **Acceso y licencia:** Ficha libre en IDEAS; WP NBER
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Jeffrey Frankel IDEAS RePEc author page Harvard Kennedy»; WebFetch: sí, índice https://ideas.repec.org/e/pfr12.html)
- **Contenido:** Survey de las particularidades de la política monetaria en emergentes: shocks de oferta y de términos de intercambio, procíclicidad de los flujos, credibilidad, traspaso del tipo de cambio, «pecado original» y elección entre metas de inflación y anclas cambiarias.
- **Uso en el bloque:** TR-BCM y AS-EMAS/AS-EMLA/AS-EMEA: marco de referencia para interpretar la reacción de los bancos centrales emergentes a choques sobre la divisa.
- **Limitaciones:** Preparado como capítulo de manual en 2010; resumen no leído en esta carga.

#### FXA-0274 · Q 78 (B) — Exchange Rates and Insulation in Emerging Markets

- **Autores:** Barry Eichengreen; Donghyun Park; Arief Ramayandi; Kwanho Shin
- **Año:** 2020
- **Publicación o institución:** Open Economies Review, vol. 31, n.º 3, págs. 565-618
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-10 Divisas emergentes (principal) · secundarias: TX-08
- **Calidad Q:** 78 (B) — Tipo 25/25 · Rigor 15/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 4/10 · Independencia 9/10 · Acceso 2/10
- **DOI / URL:** https://ideas.repec.org/a/kap/openec/v31y2020i3d10.1007_s11079-020-09587-2.html
- **Acceso y licencia:** Ficha libre en IDEAS; texto de pago (Springer)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Barry Eichengreen IDEAS RePEc author page»; WebFetch: sí, índice https://ideas.repec.org/e/pei2.html)
- **Contenido:** Evalúa si la flexibilidad cambiaria aísla a las economías emergentes de los choques financieros globales y en qué condiciones.
- **Uso en el bloque:** AS-EMAS, AS-EMLA, AS-EMEA: complemento de FXA-0259 sobre el papel amortiguador de la flotación.
- **Limitaciones:** Resumen no leído en esta carga.

#### FXA-0260 · Q 78 (B) — Global Financial Cycles and the Exchange Rate Regime: A Perspective from Emerging Markets

- **Autores:** Maurice Obstfeld; Jonathan D. Ostry; Mahvash S. Qureshi
- **Año:** 2018
- **Publicación o institución:** AEA Papers and Proceedings, vol. 108, págs. 499-504
- **Tipo de documento:** Artículo (Papers & Proceedings)
- **Temática:** TX-10 Divisas emergentes (principal) · secundarias: TX-07, TX-08
- **Calidad Q:** 78 (B) — Tipo 21/25 · Rigor 13/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 5/10 · Independencia 9/10 · Acceso 6/10
- **DOI / URL:** https://ideas.repec.org/a/aea/apandp/v108y2018p499-504.html
- **Acceso y licencia:** Ficha libre en IDEAS; texto AEA
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Maurice Obstfeld IDEAS RePEc author page»; WebFetch: sí, índice https://ideas.repec.org:443/e/pob13.html)
- **Contenido:** Nota breve que resume cómo el régimen cambiario condiciona la transmisión del ciclo financiero global a los emergentes.
- **Uso en el bloque:** Analistas de segmento emergentes: síntesis rápida complementaria de FXA-0259.
- **Limitaciones:** Solapa con FXA-0259; nota breve.

#### FXA-0287 · Q 76 (B) — Non-financial corporations from emerging market economies and capital flows

- **Autores:** Stefan Avdjiev; Michael Chui; Hyun Song Shin
- **Año:** 2014 (diciembre)
- **Publicación o institución:** BIS Quarterly Review, diciembre de 2014
- **Tipo de documento:** Artículo de revista de organismo internacional
- **Temática:** TX-10 Divisas emergentes (principal) · secundarias: TX-07
- **Calidad Q:** 76 (B) — Tipo 17/25 · Rigor 14/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 7/10 · Independencia 8/10 · Acceso 8/10
- **DOI / URL:** índice: https://www.federalreserve.gov/econres/ifdp/files/ifdp1241.pdf (bibliografía)
- **Acceso y licencia:** BIS Quarterly Review de acceso abierto
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Bruno Shin "Capital flows and the risk-taking channel of monetary policy" "Cross-border banking and global liquidity"»; WebFetch: sí, índice: bibliografía de Correa et al., IFDP 1241, https://www.federalreserve.gov/econres/ifdp/files/ifdp1241.pdf)
- **Contenido:** Documenta el endeudamiento en divisas de las empresas no financieras emergentes a través de filiales en el exterior y cómo estos flujos quedan mal recogidos en la balanza de pagos por residencia, con riesgos de descalce ante un dólar fuerte.
- **Uso en el bloque:** AS-EMAS, AS-EMLA, AS-EMEA: deuda corporativa en dólares como vulnerabilidad oculta de la divisa.
- **Limitaciones:** Verificada por bibliografía de un tercero; texto no leído.

#### FXA-0294 · Q 74 (B) — Monetary Policy and the Short-Rate Disconnect in Emerging Economies

- **Autores:** Pierre De Leo; Gita Gopinath; Sebnem Kalemli-Özcan
- **Año:** 2024
- **Publicación o institución:** Documento de trabajo (listado en la página de publicaciones de G. Gopinath)
- **Tipo de documento:** Documento de trabajo
- **Temática:** TX-10 Divisas emergentes (principal) · secundarias: TX-02, TX-04
- **Calidad Q:** 74 (B) — Tipo 15/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 4/10 · Independencia 8/10 · Acceso 6/10
- **DOI / URL:** índice: https://gopinath.scholars.harvard.edu/publications.md
- **Acceso y licencia:** Documento de trabajo de acceso libre
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «IMF Integrated Policy Framework foreign exchange intervention capital flow management Basu Boz Gopinath Roch Unsal 2020»; WebFetch: sí, índice https://gopinath.scholars.harvard.edu/publications.md)
- **Contenido:** Según el resumen visible en el índice, los bancos centrales emergentes con tipo flotante siguen reglas tipo Taylor; el título apunta a una desconexión entre el tipo oficial y los tipos de mercado a corto plazo, relevante para medir el diferencial de carry y la transmisión (texto no leído).
- **Uso en el bloque:** TR-BCM y AS-EMLA/AS-EMEA: medir el carry con tipos de mercado y no solo con el oficial.
- **Limitaciones:** Documento de trabajo; solo verificado por índice; detalle del resultado no leído.

#### FXA-0293 · Q 74 (B) — Preemptive Policies and Risk-Off Shocks in Emerging Markets

- **Autores:** Mitali Das; Gita Gopinath; Sebnem Kalemli-Özcan
- **Año:** 2022
- **Publicación o institución:** Documento de trabajo (listado en la página de publicaciones de G. Gopinath)
- **Tipo de documento:** Documento de trabajo
- **Temática:** TX-10 Divisas emergentes (principal) · secundarias: TX-08, TX-07
- **Calidad Q:** 74 (B) — Tipo 15/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 5/10 · Independencia 8/10 · Acceso 6/10
- **DOI / URL:** índice: https://gopinath.scholars.harvard.edu/publications.md
- **Acceso y licencia:** Documento de trabajo de acceso libre
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «IMF Integrated Policy Framework foreign exchange intervention capital flow management Basu Boz Gopinath Roch Unsal 2020»; WebFetch: sí, índice https://gopinath.scholars.harvard.edu/publications.md)
- **Contenido:** Muestra que las medidas preventivas de gestión de flujos de capital adoptadas antes de un choque de aversión al riesgo reducen la sensibilidad de los emergentes (diferenciales, tipo de cambio) a esos choques.
- **Uso en el bloque:** AS-EMAS, AS-EMLA, AS-EMEA: valorar la resiliencia de una divisa según las medidas preventivas en vigor.
- **Limitaciones:** Documento de trabajo; solo verificado por índice.

#### FXA-0237 · Q 74 (B) — Order flow in the South: Anatomy of the Brazilian FX market

- **Autores:** Thomas Wu
- **Año:** 2012
- **Publicación o institución:** The North American Journal of Economics and Finance, vol. 23, n.º 3, págs. 310-324 (Elsevier)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-10 Divisas emergentes (principal) · secundarias: TX-06
- **Calidad Q:** 74 (B) — Tipo 25/25 · Rigor 15/20 · Autoridad 10/15 · Vigencia 6/10 · Impacto 4/10 · Independencia 10/10 · Acceso 4/10
- **DOI / URL:** DOI: 10.1016/j.najef.2012.03.004 · https://ideas.repec.org/a/eee/ecofin/v23y2012i3p310-324.html
- **Acceso y licencia:** Ficha libre en IDEAS; texto de pago
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Dagfinn Rime IDEAS RePEc author page foreign exchange order flow»; WebFetch: sí)
- **Contenido:** Modelo de microestructura para el mercado cambiario brasileño (flotación gestionada, paradas súbitas), con intermediarios que mantienen posiciones nocturnas y demanda de clientes ligada a fundamentos; lo contrasta con todas las operaciones cliente-intermediario del mercado oficial (1999-2003).
- **Uso en el bloque:** AS-EMLA: lectura del flujo de clientes en BRL y de la dinámica ante shocks de liquidez externa.
- **Limitaciones:** Periodo 1999-2003; mercado onshore muy regulado.

#### FXA-0258 · Q 74 (B) — The Renminbi's Dollar Peg at the Crossroads

- **Autores:** Maurice Obstfeld
- **Año:** 2007
- **Publicación o institución:** Monetary and Economic Studies (Banco de Japón, IMES), vol. 25, n.º S1, págs. 29-56
- **Tipo de documento:** Artículo de revista de banco central
- **Temática:** TX-10 Divisas emergentes (principal) · secundarias: TX-08, TX-12
- **Calidad Q:** 74 (B) — Tipo 19/25 · Rigor 13/20 · Autoridad 15/15 · Vigencia 4/10 · Impacto 5/10 · Independencia 9/10 · Acceso 9/10
- **DOI / URL:** https://ideas.repec.org/a/ime/imemes/v25y2007is1p29-56.html
- **Acceso y licencia:** Acceso abierto (IMES, Banco de Japón)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Maurice Obstfeld IDEAS RePEc author page»; WebFetch: sí, índice https://ideas.repec.org:443/e/pob13.html)
- **Contenido:** Analiza los costes de la vinculación del renminbi al dólar (esterilización, presión inflacionaria, desequilibrios) y las opciones de transición hacia una mayor flexibilidad.
- **Uso en el bloque:** AS-EMAS: antecedentes del régimen del CNY y de su gestión frente a cesta, útil para interpretar la fijación diaria.
- **Limitaciones:** Escrito antes de la reforma de 2015 y del CNH moderno.

#### FXA-0275 · Q 72 (B) — From Tapering to Tightening: The Impact of the Fed's Exit on India

- **Autores:** Kaushik Basu; Barry Eichengreen; Poonam Gupta
- **Año:** 2015
- **Publicación o institución:** India Policy Forum (NCAER), vol. 11, n.º 1, págs. 1-66
- **Tipo de documento:** Artículo con discusión (foro de política)
- **Temática:** TX-10 Divisas emergentes (principal) · secundarias: TX-07
- **Calidad Q:** 72 (B) — Tipo 19/25 · Rigor 14/20 · Autoridad 14/15 · Vigencia 6/10 · Impacto 4/10 · Independencia 8/10 · Acceso 7/10
- **DOI / URL:** https://ideas.repec.org/a/nca/ncaerj/v11y2015i2015-1p1-66.html
- **Acceso y licencia:** Ficha libre en IDEAS; NCAER publica el foro en abierto
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Barry Eichengreen IDEAS RePEc author page»; WebFetch: sí, índice https://ideas.repec.org/e/pei2.html)
- **Contenido:** Estudio del impacto del anuncio de retirada de estímulos de la Fed en 2013 sobre la rupia india y las respuestas de política (subidas de tipos, medidas sobre flujos, reservas).
- **Uso en el bloque:** AS-EMAS (INR): caso de referencia de defensa de la divisa ante choques de la Fed.
- **Limitaciones:** Caso de un país; resumen no leído.

#### FXA-0234 · Q 70 (B) — From Financial Repression to External Distress: The Case of Venezuela

- **Autores:** Carmen M. Reinhart; Miguel Angel Santos
- **Año:** 2016
- **Publicación o institución:** Emerging Markets Finance and Trade, vol. 52, n.º 2, págs. 255-284
- **Tipo de documento:** Artículo revisado por pares (estudio de caso)
- **Temática:** TX-10 Divisas emergentes (principal) · secundarias: TX-08, TX-09
- **Calidad Q:** 70 (B) — Tipo 23/25 · Rigor 13/20 · Autoridad 14/15 · Vigencia 6/10 · Impacto 4/10 · Independencia 10/10 · Acceso 0/10
- **DOI / URL:** https://ideas.repec.org/a/mes/emfitr/v52y2016i2p255-284.html
- **Acceso y licencia:** Ficha libre en IDEAS; texto de pago (Taylor & Francis)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Carmen Reinhart IDEAS RePEc profile research papers»; WebFetch: sí, índice https://ideas.repec.org/e/pre33.html)
- **Contenido:** Estudio del caso venezolano: cómo la represión financiera, los controles de cambio y la monetización desembocan en dificultades externas, tipos múltiples y colapso de la divisa.
- **Uso en el bloque:** AS-EMLA: plantilla para regímenes con controles y tipos paralelos (ARS y similares) como «ámbitos de régimen»; CONTRA: señales de deterioro.
- **Limitaciones:** Caso único; resumen no leído.

## TX-11 Divisas de materias primas y términos de intercambio

#### ANA-DOC-0313 · Q 95 (A) — Not All Oil Price Shocks Are Alike: Disentangling Demand and Supply Shocks in the Crude Oil Market

- **Autores:** Lutz Kilian
- **Año:** 2009
- **Publicación o institución:** American Economic Review, vol. 99, n.º 3, págs. 1053-1069
- **Tipo de documento:** Artículo revisado por pares (canónico)
- **Temática:** TX-11 Divisas de materias primas y términos de intercambio (principal) · secundarias: TX-14
- **Calidad Q:** 95 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / URL:** DOI 10.1257/aer.99.3.1053 · https://ideas.repec.org/a/aea/aecrev/v99y2009i3p1053-69.html · versión de trabajo: https://ideas.repec.org/p/cpr/ceprdp/5994.html
- **Acceso y licencia:** Peldaño 2 (artículo AEA; ficha abierta en RePEc y versión CEPR DP 5994) · Licencia: Copyright AEA
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Lutz Kilian IDEAS RePEc author page publications oil price shocks»; WebFetch: sí) · reutilizada del F7 V3.2 (TA-08)
- **Contenido:** Descompone el precio real del petróleo en shocks de oferta, de demanda agregada global de materias primas y de demanda específica del crudo (precautoria); cada uno tiene efectos macro distintos y el alza de 2003-2008 fue sobre todo de demanda global.
- **Uso en el bloque:** AS-G10M y AS-EMEA: distinguir choques de oferta y de demanda de petróleo antes de traducirlos en una tesis sobre NOK, CAD o divisas del Golfo (un choque de demanda global y uno de oferta no mueven igual a las divisas de exportadores).
- **Limitaciones:** Identificación recursiva discutida en la literatura posterior (Baumeister-Hamilton).

#### FXA-0411 · Q 93 (A) — Commodity Trade and the Carry Trade: A Tale of Two Countries

- **Autores:** Robert Ready; Nikolai Roussanov; Colin Ward
- **Año:** 2017
- **Publicación o institución:** The Journal of Finance, vol. 72, n.º 6, págs. 2629-2684
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-11 Divisas de materias primas y términos de intercambio (principal) · secundarias: TX-04, TX-05
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 6/10
- **DOI / URL:** DOI: 10.1111/jofi.12546 · https://www.nber.org/papers/w19371 (NBER WP 19371)
- **Acceso y licencia:** Artículo de pago (Wiley); versión de trabajo NBER · Licencia: copyright del editor
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Ready Roussanov Ward "Commodity Trade and the Carry Trade: A Tale of Two Countries" Journal of Finance»; WebFetch: sí, página NBER)
- **Contenido:** Las divisas de tipos altos tienden a ser de exportadores de materias primas y las de tipos bajos de exportadores de manufacturas; un modelo con especialización comercial y capacidad de transporte limitada explica el diferencial; una estrategia basada en materias primas recoge gran parte de la prima del carry y su predictibilidad procíclica con precios de materias primas y fletes.
- **Uso en el bloque:** AS-G10M y AS-ESTR: interpretar el carry AUD/JPY, NZD/JPY o CAD/JPY como exposición a materias primas; MOTOR: variable de fletes como predictor.
- **Limitaciones:** Modelo estilizado de dos países; muestra hasta 2012 aprox.

#### ANA-DOC-0329 · Q 93 (A) — Oil and the Macroeconomy since World War II

- **Autores:** James D. Hamilton
- **Año:** 1983
- **Publicación o institución:** Journal of Political Economy, vol. 91, n.º 2, págs. 228-248
- **Tipo de documento:** Artículo revisado por pares (canónico)
- **Temática:** TX-11 Divisas de materias primas y términos de intercambio (principal) · secundarias: TX-14
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 10/10 · Independencia 10/10 · Acceso 8/10
- **DOI / URL:** https://ideas.repec.org/a/ucp/jpolec/v91y1983i2p228-48.html
- **Acceso y licencia:** Peldaño 2-3 (JPE; ficha abierta en RePEc) · Licencia: Copyright University of Chicago Press
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «James D. Hamilton IDEAS RePEc "Oil and the Macroeconomy since World War II"…»; WebFetch: sí, sobre la página de autor de RePEc que lista la obra) · reutilizada del F7 V3.2 (TA-08)
- **Contenido:** Documenta que casi todas las recesiones de EE. UU. de posguerra fueron precedidas por subidas bruscas del petróleo; origen de la literatura sobre petróleo y ciclo.
- **Uso en el bloque:** TR-BCM y AS-G10M: marco histórico de los choques petroleros y su transmisión macro, contexto de las divisas de exportadores e importadores.
- **Limitaciones:** Relación lineal inestable tras 1985 (véanse ANA-DOC-0313 y ANA-DOC-0323).

#### FXA-0401 · Q 92 (A) — Commodity currencies

- **Autores:** Yu-chin Chen; Kenneth Rogoff
- **Año:** 2003
- **Publicación o institución:** Journal of International Economics, vol. 60, n.º 1, págs. 133-160
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-11 Divisas de materias primas y términos de intercambio (principal) · secundarias: TX-03
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** https://ideas.repec.org/f/pch880.html (página de autora en IDEAS que lista la obra) · versión de trabajo: https://ideas.repec.org/p/imf/imfwpa/2002-027.html (IMF WP 02/27, «Commodity Currencies and Empirical Exchange Rate Puzzles»)
- **Acceso y licencia:** Artículo Elsevier de pago; versión de trabajo del FMI de libre acceso · Licencia: copyright del editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Kenneth Rogoff IDEAS RePEc author page "commodity currencies" Chen Rossi»; WebFetch: sí, sobre la página de autora de IDEAS y la ficha del IMF WP 02/27)
- **Contenido:** Obra fundacional: para Australia y Nueva Zelanda (y en menor medida Canadá), el precio en dólares de las materias primas exportadas tiene un efecto fuerte y estable sobre el tipo de cambio real, de magnitud coherente con la teoría; aun así persiste un enigma PPA en los residuos.
- **Uso en el bloque:** AS-G10M (AG-04): fundamento del vínculo AUD/NZD/CAD–precios de materias primas; TR-BCM: lectura de los términos de intercambio como determinante del tipo real.
- **Limitaciones:** Relación contemporánea, no predictiva a corto plazo; muestra hasta 2001; el CAD muestra un vínculo más débil.

#### ANA-DOC-0317 · Q 90 (A) — Forty Years of Oil Price Fluctuations: Why the Price of Oil May Still Surprise Us

- **Autores:** Christiane Baumeister; Lutz Kilian
- **Año:** 2016
- **Publicación o institución:** Journal of Economic Perspectives, vol. 30, n.º 1, págs. 139-160
- **Tipo de documento:** Artículo de revisión revisado por pares
- **Temática:** TX-11 Divisas de materias primas y términos de intercambio (principal) · secundarias: —
- **Calidad Q:** 90 (A) — Tipo 24/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 10/10 · Acceso 8/10
- **DOI / URL:** DOI 10.1257/jep.30.1.139 · https://ideas.repec.org/a/aea/jecper/v30y2016i1p139-60.html
- **Acceso y licencia:** Peldaño 1 (JEP es de acceso abierto) · Licencia: Copyright AEA; lectura libre
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Lutz Kilian IDEAS RePEc author page publications oil price shocks»; WebFetch: sí) · reutilizada del F7 V3.2 (TA-08)
- **Contenido:** Repasa los grandes episodios del petróleo 1973-2014 y sus causas, y explica por qué el precio sigue siendo difícil de prever y por qué una «sorpresa» depende de las expectativas de cada grupo.
- **Uso en el bloque:** AS-G10M y PROS: entender por qué el precio del petróleo (motor de los términos de intercambio de CAD/NOK) sorprende; cautela con escenarios de materias primas.
- **Limitaciones:** Termina en 2014.

#### FXA-0402 · Q 90 (A) — Can Exchange Rates Forecast Commodity Prices?

- **Autores:** Yu-chin Chen; Kenneth Rogoff; Barbara Rossi
- **Año:** 2010
- **Publicación o institución:** Quarterly Journal of Economics, vol. 125, n.º 3, págs. 1145-1194
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-11 Divisas de materias primas y términos de intercambio (principal) · secundarias: TX-13
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 4/10
- **DOI / URL:** DOI: 10.1162/qjec.2010.125.3.1145 · https://ideas.repec.org/f/pch880.html (lista la obra y la versión NBER WP 13901) · https://ideas.repec.org/p/hrv/faseco/29412033.html (copia de Harvard)
- **Acceso y licencia:** Artículo de pago (Oxford University Press); versiones de trabajo NBER y Harvard de libre acceso · Licencia: copyright del editor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Kenneth Rogoff IDEAS RePEc author page "commodity currencies" Chen Rossi»; WebFetch: sí, sobre la página de autora de IDEAS; DOI visto en https://en.wikipedia.org/wiki/Commodity_currency)
- **Contenido:** Muestra que los tipos de cambio de las economías exportadoras de materias primas (Australia, Canadá, Nueva Zelanda, Sudáfrica, Chile) predicen fuera de muestra los precios de sus materias primas, mientras que la causalidad inversa es mucho más débil: el tipo de cambio incorpora expectativas sobre los términos de intercambio futuros.
- **Uso en el bloque:** AS-G10M y AS-EMLA (CLP): el tipo de cambio como indicador adelantado de los términos de intercambio; PROS: prueba de dirección de causalidad antes de usar materias primas como predictor de divisas.
- **Limitaciones:** Resultados sensibles a la agregación temporal (véase Bork, Rovira Kaltwasser y Sercu 2022); horizonte trimestral.

#### FXA-0410 · Q 87 (A) — Can Oil Prices Forecast Exchange Rates? An Empirical Analysis of the Relationship between Commodity Prices and Exchange Rates

- **Autores:** Domenico Ferraro; Kenneth Rogoff; Barbara Rossi
- **Año:** 2015
- **Publicación o institución:** Journal of International Money and Finance, vol. 54 (junio), págs. 116-141
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-11 Divisas de materias primas y términos de intercambio (principal) · secundarias: TX-13
- **Calidad Q:** 87 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 6/10 · Independencia 10/10 · Acceso 4/10
- **DOI / URL:** DOI: 10.1016/j.jimonfin.2015.03.001 · https://rogoff.scholars.harvard.edu/publications/can-oil-prices-forecast-exchange-rates · versión de trabajo: https://www.nber.org/papers/w17998.pdf (NBER WP 17998)
- **Acceso y licencia:** Artículo de pago (Elsevier); versión de trabajo NBER y copia en crei.cat · Licencia: copyright del editor
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Ferraro Rogoff Rossi 2015 "Can oil prices forecast exchange rates?" Journal of International Money and Finance»; WebFetch: sí, página del autor en Harvard)
- **Contenido:** Con CAD/USD, encuentra poca relación sistemática fuera de muestra entre petróleo y tipo de cambio a frecuencia mensual o trimestral, pero una relación diaria bastante robusta (con precios contemporáneos y, de forma fugaz, retardados) una vez tenidas en cuenta las inestabilidades.
- **Uso en el bloque:** AS-G10M (CAD, NOK): la señal del petróleo es de muy corto plazo; PROS y EVAL: fijar el horizonte H1 para este tipo de predictor.
- **Limitaciones:** Centrado sobre todo en Canadá; el poder predictivo con retardos es efímero.

#### FXA-0412 · Q 85 (A) — When the Walk Is Not Random: Commodity Prices and Exchange Rates

- **Autores:** Emanuel Kohlscheen; Fernando Avalos; Andreas Schrimpf
- **Año:** 2017
- **Publicación o institución:** International Journal of Central Banking, vol. 13, n.º 2 (junio) · versión de trabajo: BIS Working Papers n.º 551
- **Tipo de documento:** Artículo revisado por pares (revista de bancos centrales)
- **Temática:** TX-11 Divisas de materias primas y términos de intercambio (principal) · secundarias: TX-13, TX-10
- **Calidad Q:** 85 (A) — Tipo 23/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 5/10 · Independencia 9/10 · Acceso 8/10
- **DOI / URL:** https://www.ijcb.org/journal/v13n2/when-walk-not-random-commodity-prices-and-exchange-rates · https://bis.org/publ/work551.htm
- **Acceso y licencia:** Acceso abierto (IJCB y BPI)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Kohlscheen Avalos Schrimpf "When the walk is not random: commodity prices and exchange rates" BIS working paper»; WebFetch: sí, página de IJCB)
- **Contenido:** En un panel de once exportadores de materias primas, los índices de precios específicos de cada país ayudan a predecir el tipo de cambio hasta unos dos meses y baten al paseo aleatorio fuera de muestra en la mayoría de ellos, incluso controlando por apetito global de riesgo y carry.
- **Uso en el bloque:** AS-G10M, AS-EMLA y AS-EMEA: índice de términos de intercambio por país como señal táctica; PROS: referencia de un predictor que sí bate al paseo aleatorio.
- **Limitaciones:** Pseudo fuera de muestra (precios de materias primas contemporáneos/realizados); horizonte corto.

#### ANA-DOC-0335 · Q 84 (A) — Commodity Markets Outlook, October 2025

- **Autores:** Banco Mundial (autor institucional)
- **Año:** 2025 (29 de octubre)
- **Publicación o institución:** World Bank Group, Prospects Group
- **Tipo de documento:** Informe institucional periódico con datos y previsiones (serie semestral)
- **Temática:** TX-11 Divisas de materias primas y términos de intercambio (principal) · secundarias: TX-10
- **Calidad Q:** 84 (A) — Tipo 22/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 6/10 · Independencia 8/10 · Acceso 8/10
- **DOI / URL:** Handle http://hdl.handle.net/10986/43864 · https://openknowledge.worldbank.org/entities/publication/d08d3ee8-e38a-4f02-8ade-95b9c6075c0b
- **Acceso y licencia:** Peldaño 1 (Open Knowledge Repository) · Licencia: CC BY 3.0 IGO
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «World Bank Commodity Markets Outlook October 2025»; WebFetch: sí) · reutilizada del F7 V3.2 (TA-08)
- **Contenido:** Prevé caídas de ≈7 % de los precios de materias primas en 2025 y 2026 (cuarto año de descenso) por crecimiento débil y exceso de oferta de crudo; metales preciosos +5 % en 2026 tras un alza de ≈40 % en 2025; riesgos sesgados a la baja.
- **Uso en el bloque:** AS-G10M, AS-EMLA y AS-EMEA: previsiones oficiales de precios de materias primas como insumo de los términos de intercambio de AUD, CAD, NOK, CLP, PEN, ZAR.
- **Limitaciones:** Previsiones con historial de error amplio; caduca con la edición siguiente (abril 2026).

#### FXA-0419 · Q 84 (A) — Terms of Trade and Exchange Rate Regimes in Developing Countries

- **Autores:** Christian Broda
- **Año:** 2004
- **Publicación o institución:** Journal of International Economics, vol. 63, págs. 31-58
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-11 Divisas de materias primas y términos de intercambio (principal) · secundarias: TX-08, TX-10
- **Calidad Q:** 84 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 13/15 · Vigencia 8/10 · Impacto 9/10 · Independencia 10/10 · Acceso 2/10
- **DOI / URL:** Confirmada vía página índice: https://nber.org/system/files/working_papers/w21253/w21253.pdf (bibliografía de Schmitt-Grohé y Uribe)
- **Acceso y licencia:** De pago (Elsevier)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Schmitt-Grohé Uribe "How Important Are Terms-of-Trade Shocks?" International Economic Review real exchange rate»; WebFetch: sí, de la página índice; no de la obra)
- **Contenido:** Muestra que la respuesta de los países en desarrollo a los choques de términos de intercambio depende del régimen cambiario: con tipo fijo, caídas de producto mayores y ajuste lento del tipo real; con flotación, depreciación nominal rápida y menor coste real.
- **Uso en el bloque:** AS-EMLA/AS-EMEA (divisas del Golfo, regímenes fijos frente a flotantes): anticipar si el ajuste a un choque de materias primas llegará vía tipo de cambio o vía precios y actividad.
- **Limitaciones:** Contenido descrito según conocimiento de la obra; muestra hasta finales de los noventa.

#### FXA-0404 · Q 84 (A) — Keynes, Cocoa, and Copper: In Search of Commodity Currencies

- **Autores:** Paul Cashin; Luis Felipe Céspedes; Ratna Sahay
- **Año:** 2002
- **Publicación o institución:** Fondo Monetario Internacional, IMF Working Paper WP/02/223
- **Tipo de documento:** Documento de trabajo
- **Temática:** TX-11 Divisas de materias primas y términos de intercambio (principal) · secundarias: TX-10, TX-03
- **Calidad Q:** 84 (A) — Tipo 20/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 8/10 · Impacto 9/10 · Independencia 9/10 · Acceso 7/10
- **DOI / URL:** https://www.imf.org/en/publications/wp/issues/2016/12/30/keynes-cocoa-and-copper-in-search-of-commodity-currencies-16194 · versión del Banco Central de Chile (DT n.º 236, Cashin y Céspedes): https://www.bcentral.cl/contenido/-/detalle/documento-de-trabajo-n-236
- **Acceso y licencia:** Acceso abierto (FMI) · Licencia: términos de uso del FMI
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Cashin Céspedes Sahay 2004 "Commodity currencies and the real exchange rate" Journal of Development Economics»; WebFetch: sí)
- **Contenido:** Construye índices mensuales de precios de exportación de materias primas para 58 países (44 materias primas, 1980-2002) y halla relación de largo plazo entre precios reales de materias primas y tipo de cambio real en unas dos quintas partes de ellos; la semivida del ajuste hacia la PPA aumentada por materias primas es de unos 8 meses, independiente del régimen.
- **Uso en el bloque:** AS-EMLA y AS-EMEA (CLP, PEN, ZAR, divisas africanas): identificar qué divisas emergentes son «de materias primas»; MOTOR: plantilla de índice de términos de intercambio por país.
- **Limitaciones:** Versión de trabajo; la versión publicada en revista (2004) no se ha verificado en esta carga; datos hasta 2002.

#### FXA-0418 · Q 84 (A) — The Terms of Trade, the Real Exchange Rate, and Economic Fluctuations

- **Autores:** Enrique G. Mendoza
- **Año:** 1995
- **Publicación o institución:** International Economic Review, vol. 36, n.º 1, págs. 101-137
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-11 Divisas de materias primas y términos de intercambio (principal) · secundarias: TX-01
- **Calidad Q:** 84 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 7/10 · Impacto 10/10 · Independencia 10/10 · Acceso 1/10
- **DOI / URL:** Confirmada vía página índice: https://nber.org/system/files/working_papers/w21253/w21253.pdf (bibliografía de Schmitt-Grohé y Uribe)
- **Acceso y licencia:** De pago (Wiley/JSTOR)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Schmitt-Grohé Uribe "How Important Are Terms-of-Trade Shocks?" International Economic Review real exchange rate»; WebFetch: sí, de la página índice; no de la obra)
- **Contenido:** Modelo de ciclo real de economía abierta con bienes comerciables y no comerciables en el que los choques de términos de intercambio explican una parte importante de las fluctuaciones del producto y del tipo de cambio real (obra canónica del canal términos de intercambio → tipo real).
- **Uso en el bloque:** AS-G10M, AS-EMLA y TR-BCM: fundamento teórico del vínculo términos de intercambio–tipo de cambio real.
- **Limitaciones:** Contenido descrito según conocimiento de la obra; su conclusión cuantitativa es discutida por Schmitt-Grohé y Uribe (FXA-0417).

#### ANA-DOC-0326 · Q 82 (A) — Oil prices, exchange rates and interest rates

- **Autores:** Lutz Kilian; Xiaoqing Zhou
- **Año:** 2022
- **Publicación o institución:** Journal of International Money and Finance, vol. 126
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-11 Divisas de materias primas y términos de intercambio (principal) · secundarias: TX-12, TX-02
- **Calidad Q:** 82 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 3/10 · Independencia 10/10 · Acceso 4/10
- **DOI / URL:** https://ideas.repec.org/a/eee/jimfin/v126y2022ics0261560622000821.html
- **Acceso y licencia:** Peldaño 3 (Elsevier) · Licencia: Copyright Elsevier
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Lutz Kilian IDEAS RePEc author page publications oil price shocks»; WebFetch: sí, sobre la página de autor de IDEAS que lista la obra) · reutilizada del F7 V3.2 (TA-08)
- **Contenido:** Relación entre precio del petróleo, dólar y tipos de interés; enlaza energía con divisas y renta fija.
- **Uso en el bloque:** AS-G10M (CAD, NOK) y TR-BCM: correlaciones cruzadas petróleo–dólar–tipos de interés para separar el canal de materias primas del de política monetaria.
- **Limitaciones:** Resumen no leído en esta carga; contenido descrito por el título.

#### FXA-0413 · Q 82 (A) — The relationship between oil prices and exchange rates: Revisiting theory and evidence

- **Autores:** Joscha Beckmann; Robert L. Czudaj; Vipin Arora
- **Año:** 2020
- **Publicación o institución:** Energy Economics, vol. 88, art. 104772 · versión previa: EIA Working Paper Series (junio de 2017)
- **Tipo de documento:** Artículo de revisión (survey) revisado por pares
- **Temática:** TX-11 Divisas de materias primas y términos de intercambio (principal) · secundarias: TX-01
- **Calidad Q:** 82 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 12/15 · Vigencia 10/10 · Impacto 6/10 · Independencia 9/10 · Acceso 5/10
- **DOI / URL:** DOI: 10.1016/j.eneco.2020.104772 · https://ideas.repec.org/a/eee/eneeco/v88y2020ics0140988320301122.html · versión abierta: https://www.eia.gov/workingpapers/pdf/oil_exchangerates_61317.pdf
- **Acceso y licencia:** Artículo de pago; versión de trabajo de la EIA de libre acceso
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Beckmann Czudaj Arora "The relationship between oil prices and exchange rates: Revisiting theory and evidence" Energy Economics»; WebFetch: sí, IDEAS y EIA)
- **Contenido:** Revisión de canales teóricos (términos de intercambio, riqueza, cartera, facturación en dólares) con causalidad bidireccional y de la evidencia empírica: vínculo de largo plazo frecuente y predictibilidad de corto plazo en ambas direcciones, pero inestable en el tiempo.
- **Uso en el bloque:** TR-BCM y AS-G10M: mapa de canales petróleo–dólar y petróleo–divisas de exportadores; DOC-A: puerta de entrada a la literatura.
- **Limitaciones:** Resultados empíricos heterogéneos por muestra y método.

#### FXA-0417 · Q 82 (A) — How Important Are Terms of Trade Shocks?

- **Autores:** Stephanie Schmitt-Grohé; Martín Uribe
- **Año:** 2015 (rev. noviembre de 2016)
- **Publicación o institución:** NBER Working Paper 21253 (versión publicada en revista no verificada en esta carga)
- **Tipo de documento:** Documento de trabajo
- **Temática:** TX-11 Divisas de materias primas y términos de intercambio (principal) · secundarias: TX-10
- **Calidad Q:** 82 (A) — Tipo 20/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 10/10 · Acceso 2/10
- **DOI / URL:** https://nber.org/system/files/working_papers/w21253/w21253.pdf
- **Acceso y licencia:** NBER (acceso según suscripción)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Schmitt-Grohé Uribe "How Important Are Terms-of-Trade Shocks?" International Economic Review real exchange rate»; WebFetch: sí)
- **Contenido:** Con SVAR por país para 38 economías, los choques de términos de intercambio explican menos del 10 % de las fluctuaciones de la actividad, frente al peso mucho mayor que les atribuyen los modelos calibrados (incluido el canal del tipo de cambio real); señala una desconexión entre evidencia y teoría.
- **Uso en el bloque:** AS-EMLA/AS-EMEA y CONTRA: no sobrestimar el peso de las materias primas en el ciclo (y en la divisa) de un emergente; contraste con FXA-0404.
- **Limitaciones:** Documento de trabajo; los términos de intercambio medidos con índices de precios pueden infraestimar el efecto en exportadores concentrados.

#### FXA-0415 · Q 82 (A) — Oil prices, exchange rates and asset prices

- **Autores:** Marcel Fratzscher; Daniel Schneider; Ine Van Robays
- **Año:** 2014
- **Publicación o institución:** Banco Central Europeo, ECB Working Paper Series n.º 1689 (también CESifo WP 4264 y DIW DP 1302, 2013)
- **Tipo de documento:** Documento de trabajo
- **Temática:** TX-11 Divisas de materias primas y términos de intercambio (principal) · secundarias: TX-12
- **Calidad Q:** 82 (A) — Tipo 20/25 · Rigor 18/20 · Autoridad 14/15 · Vigencia 8/10 · Impacto 6/10 · Independencia 8/10 · Acceso 8/10
- **DOI / URL:** https://ideas.repec.org/p/ecb/ecbwps/20141689.html · https://www.cesifo.org/DocDL/cesifo1_wp4264.pdf
- **Acceso y licencia:** Acceso abierto (BCE, CESifo)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Fratzscher Schneider Van Robays "Oil prices, exchange rates and asset prices" ECB working paper»; WebFetch: sí, IDEAS)
- **Contenido:** Con identificación por heterocedasticidad en un modelo multifactorial, halla causalidad bidireccional dólar–petróleo desde principios de los 2000 y fuerte influencia de la renta variable y del riesgo; la correlación negativa creciente petróleo–dólar se explica sobre todo por choques de riesgo y por la financiarización del petróleo.
- **Uso en el bloque:** TR-BCM y AS-ESTR (dólar amplio): no tratar la correlación petróleo–dólar como constante; AS-G10M: separar el componente de riesgo global del de materias primas.
- **Limitaciones:** Documento de trabajo; muestra hasta 2012 aprox.

#### FXA-0407 · Q 81 (A) — Aggregation bias in tests of the commodity currency hypothesis

- **Autores:** Lasse Bork; Pablo Rovira Kaltwasser; Piet Sercu
- **Año:** 2022
- **Publicación o institución:** Journal of Banking & Finance, vol. 135, art. 106392
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-11 Divisas de materias primas y términos de intercambio (principal) · secundarias: TX-13
- **Calidad Q:** 81 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 11/15 · Vigencia 10/10 · Impacto 3/10 · Independencia 10/10 · Acceso 4/10
- **DOI / URL:** DOI: 10.1016/j.jbankfin.2021.106392 · https://ideas.repec.org/a/eee/jbfina/v135y2022ics0378426621003435.html
- **Acceso y licencia:** De pago (Elsevier) · Licencia: copyright del editor
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Kenneth Rogoff IDEAS RePEc author page "commodity currencies" Chen Rossi»; WebFetch: sí)
- **Contenido:** Muestra que promediar precios diarios en datos mensuales crea predictibilidad espuria en las pruebas de la hipótesis de divisas de materias primas (el tipo de cambio predice los precios); con datos de final de periodo, el apoyo a la hipótesis es, como mucho, débil.
- **Uso en el bloque:** EVAL y CONTRA: advertencia metodológica sobre datos promediados al contrastar señales divisa–materias primas; PROS: usar datos de cierre.
- **Limitaciones:** Centrado en la dirección tipo de cambio → precios; poco citado aún.

#### FXA-0403 · Q 80 (A) — Are The Commodity Currencies An Exception To The Rule?

- **Autores:** Yu-chin Chen; Kenneth Rogoff
- **Año:** 2012
- **Publicación o institución:** Global Journal of Economics, vol. 1, n.º 1, págs. 1-28 (World Scientific)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-11 Divisas de materias primas y términos de intercambio (principal) · secundarias: TX-13
- **Calidad Q:** 80 (A) — Tipo 22/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 3/10 · Independencia 10/10 · Acceso 4/10
- **DOI / URL:** DOI: 10.1142/S2251361212500048 · https://ideas.repec.org/a/wsi/gjexxx/v01y2012i01ns2251361212500048.html
- **Acceso y licencia:** De pago (World Scientific) · Licencia: copyright del editor
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Kenneth Rogoff IDEAS RePEc author page "commodity currencies" Chen Rossi»; WebFetch: sí)
- **Contenido:** Los precios mundiales de las materias primas exportadas son un determinante robusto del tipo de cambio real de los exportadores con tipo flexible, pero dicen poco del movimiento del trimestre siguiente; con promediado bayesiano de modelos, ninguna especificación gana de forma estable entre países y periodos.
- **Uso en el bloque:** AS-G10M: evita sobrevender el precio de las materias primas como señal de corto plazo; CONTRA: argumento de inestabilidad de los modelos.
- **Limitaciones:** Revista de menor difusión; muestra de pocos países.

#### FXA-0416 · Q 79 (B) — Cross-country differences in the effects of oil shocks

- **Autores:** Gert Peersman; Ine Van Robays
- **Año:** 2012
- **Publicación o institución:** Energy Economics, vol. 34, n.º 5, págs. 1532-1547
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-11 Divisas de materias primas y términos de intercambio (principal) · secundarias: TX-02
- **Calidad Q:** 79 (B) — Tipo 25/25 · Rigor 16/20 · Autoridad 12/15 · Vigencia 8/10 · Impacto 6/10 · Independencia 10/10 · Acceso 2/10
- **DOI / URL:** https://ideas.repec.org/f/pva502.html (página de autora en IDEAS que lista la obra; versión de trabajo CESifo WP 3306)
- **Acceso y licencia:** De pago (Elsevier); versión de trabajo CESifo
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Fratzscher Schneider Van Robays "Oil prices, exchange rates and asset prices" ECB working paper»; WebFetch: sí, sobre la página de autora de IDEAS)
- **Contenido:** Compara los efectos macroeconómicos de choques de oferta y demanda de petróleo entre economías industrializadas, distinguiendo exportadoras netas de energía (con apreciación cambiaria) de importadoras.
- **Uso en el bloque:** AS-G10M (NOK, CAD, AUD) frente a AS-G10N (EUR, JPY): asimetrías de la respuesta del tipo de cambio según la posición energética.
- **Limitaciones:** Resumen no leído en esta carga; muestra hasta 2010 aprox.

#### FXA-0406 · Q 78 (B) — Commodity Currencies Revisited

- **Autores:** Evgenia Passari
- **Año:** 2015
- **Publicación o institución:** Université Paris-Dauphine (HAL Post-Print hal-01453266)
- **Tipo de documento:** Documento de trabajo / artículo depositado
- **Temática:** TX-11 Divisas de materias primas y términos de intercambio (principal) · secundarias: TX-05
- **Calidad Q:** 78 (B) — Tipo 18/25 · Rigor 16/20 · Autoridad 11/15 · Vigencia 9/10 · Impacto 5/10 · Independencia 10/10 · Acceso 9/10
- **DOI / URL:** https://ideas.repec.org/p/hal/journl/hal-01453266.html
- **Acceso y licencia:** Acceso abierto (HAL)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Kenneth Rogoff IDEAS RePEc author page "commodity currencies" Chen Rossi»; WebFetch: sí)
- **Contenido:** Propone una «estrategia de materias primas» que negocia divisas según los cambios diarios de un índice global de materias primas; los precios predicen fuera de muestra el tipo de cambio de exportadores e importadores a frecuencia diaria; diferencial largo-corto ≈ 6 % anual, poco correlacionado con carry y momentum, aunque los costes de transacción absorben parte.
- **Uso en el bloque:** AS-ESTR: diseño de una cesta temática de materias primas como factor distinto del carry; MOTOR: control de costes de transacción.
- **Limitaciones:** Versión publicada en revista no verificada; rentabilidad sensible a costes en emergentes.

#### FXA-0414 · Q 76 (B) — Is there a Homogeneous Causality Pattern between Oil Prices and Currencies of Oil Importers and Exporters?

- **Autores:** Joscha Beckmann; Robert Czudaj
- **Año:** 2013
- **Publicación o institución:** Energy Economics, vol. 40, págs. 665-678
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-11 Divisas de materias primas y términos de intercambio (principal) · secundarias: TX-10
- **Calidad Q:** 76 (B) — Tipo 25/25 · Rigor 15/20 · Autoridad 11/15 · Vigencia 8/10 · Impacto 5/10 · Independencia 10/10 · Acceso 2/10
- **DOI / URL:** DOI: 10.1016/j.eneco.2013.08.007 · https://oek.wiwi.uni-due.de/en/research/publications/is-there-a-homogeneous-causality-pattern-between-oil-prices-and-currencies-of-oil-importers-and-exporters-10337
- **Acceso y licencia:** De pago (Elsevier); ficha bibliográfica en la Universidad de Duisburg-Essen
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Beckmann Czudaj Arora "The relationship between oil prices and exchange rates: Revisiting theory and evidence" Energy Economics»; WebFetch: sí, solo ficha bibliográfica)
- **Contenido:** Contrasta si la dirección de causalidad entre petróleo y tipo de cambio es la misma para importadores y exportadores de crudo (por el título y la ficha; resumen no leído).
- **Uso en el bloque:** AS-EMAS (INR, KRW importadores) frente a AS-G10M/AS-EMEA (NOK, CAD, divisas del Golfo): no asumir una relación homogénea.
- **Limitaciones:** Resumen no leído en esta carga; contenido descrito por el título.

#### FXA-0408 · Q 74 (B) — Commodity Currencies and Causality: Some High-Frequency Evidence

- **Autores:** Rashad Ahmed
- **Año:** 2020
- **Publicación o institución:** Economics Letters, vol. 189 (versión de trabajo MPRA Paper 98319, 2019)
- **Tipo de documento:** Artículo revisado por pares (versión de trabajo en MPRA)
- **Temática:** TX-11 Divisas de materias primas y términos de intercambio (principal) · secundarias: TX-14, TX-04
- **Calidad Q:** 74 (B) — Tipo 22/25 · Rigor 16/20 · Autoridad 9/15 · Vigencia 9/10 · Impacto 3/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** https://ideas.repec.org/p/pra/mprapa/98319.html
- **Acceso y licencia:** Versión de trabajo de libre acceso (MPRA); artículo de pago
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Kenneth Rogoff IDEAS RePEc author page "commodity currencies" Chen Rossi»; WebFetch: sí)
- **Contenido:** Usa el ataque con drones a refinerías saudíes (septiembre de 2019) como experimento natural: con datos de alta frecuencia de 30 divisas, la intensidad exportadora (importadora) de crudo se asocia a apreciación (depreciación); las divisas con tipos altos y posición financiera débil se depreciaron más y las de refugio se apreciaron.
- **Uso en el bloque:** AS-G10M (NOK, CAD) y AS-EMEA: reacción esperada de las divisas a un choque de oferta de petróleo de origen geopolítico; TR-PFV: interacción con el desmontaje del carry.
- **Limitaciones:** Un solo evento; la identificación de la versión publicada procede de la ficha RePEc.

#### FXA-0405 · Q 66 (B) — Commodity Currencies

- **Autores:** Paul Cashin; Luis Céspedes; Ratna Sahay
- **Año:** 2003
- **Publicación o institución:** Finance & Development, vol. 40, n.º 1 (marzo), Fondo Monetario Internacional
- **Tipo de documento:** Artículo divulgativo especializado
- **Temática:** TX-11 Divisas de materias primas y términos de intercambio (principal) · secundarias: TX-08
- **Calidad Q:** 66 (B) — Tipo 8/25 · Rigor 12/20 · Autoridad 14/15 · Vigencia 8/10 · Impacto 6/10 · Independencia 9/10 · Acceso 9/10
- **DOI / URL:** https://www.imf.org/external/pubs/ft/fandd/2003/03/cash.htm
- **Acceso y licencia:** Acceso abierto (FMI)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Cashin Céspedes Sahay 2004 "Commodity currencies and the real exchange rate" Journal of Development Economics»; WebFetch: sí)
- **Contenido:** Resumen divulgativo: en 22 de 58 países exportadores los precios reales de materias primas explican más del 80 % de la variación del tipo de cambio real; elasticidad mediana 0,38 (una caída del 10 % en precios reales ≈ depreciación real del 3,8 %); la volatilidad real es similar con tipo fijo o flexible, pero con tipo fijo el ajuste llega vía precios (deflación).
- **Uso en el bloque:** AS-EMEA/AS-EMLA y RED: cifra de referencia de elasticidad para explicar al usuario la sensibilidad de una divisa a sus materias primas.
- **Limitaciones:** Divulgación; cifras de 2002; no sustituye a la versión técnica (FXA-0404).

#### FXA-0409 · Q 62 (C) — Commodity currencies and the real exchange rate

- **Autores:** Stephen Tokarick
- **Año:** 2008
- **Publicación o institución:** Economics Letters, vol. 101, n.º 1, págs. 60-62
- **Tipo de documento:** Artículo revisado por pares (nota teórica)
- **Temática:** TX-11 Divisas de materias primas y términos de intercambio (principal) · secundarias: TX-03
- **Calidad Q:** 62 (C) — Tipo 20/25 · Rigor 12/20 · Autoridad 10/15 · Vigencia 8/10 · Impacto 2/10 · Independencia 8/10 · Acceso 2/10
- **DOI / URL:** https://ideas.repec.org:443/a/eee/ecolet/v101y2008i1p60-62.html
- **Acceso y licencia:** De pago (Elsevier)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Cashin Céspedes Sahay 2004 "Commodity currencies and the real exchange rate" Journal of Development Economics»; WebFetch: sí)
- **Contenido:** Nota teórica: una mejora de los términos de intercambio de un exportador de materias primas puede subir o bajar el precio relativo de los no comerciables según dominen los efectos renta o sustitución; el signo de la respuesta del tipo real no está garantizado.
- **Uso en el bloque:** CONTRA: contraargumento teórico cuando una tesis da por hecho que un auge de materias primas aprecia el tipo real.
- **Limitaciones:** Nota breve, sin evidencia empírica; impacto bajo.

## TX-12 Divisas de refugio y sistema monetario internacional

#### ANA-DOC-0304 · Q 93 (A) — Dominant Currency Paradigm

- **Autores:** Gita Gopinath; Emine Boz; Camila Casas; Federico J. Díez; Pierre-Olivier Gourinchas; Mikkel Plagborg-Møller
- **Año:** 2020
- **Publicación o institución:** American Economic Review, vol. 110, n.º 3, págs. 677-719
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-12 Divisas de refugio y sistema monetario internacional (principal) · secundarias: TX-01
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** DOI 10.1257/aer.20171201 · https://ideas.repec.org/a/aea/aecrev/v110y2020i3p677-719.html · versión de trabajo: https://www.nber.org/papers/w22943
- **Acceso y licencia:** Peldaño 2 (artículo AEA de pago; versión de trabajo NBER y datos en openICPSR) · Licencia: Copyright AEA
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Gopinath Boz Casas Díez Gourinchas Plagborg-Møller "Dominant Currency Paradigm" American Economic Review 2020»; WebFetch: sí) · reutilizada del F7 V3.2 (TA-07)
- **Contenido:** Muestra que la mayor parte del comercio se factura en dólares y que, por ello, el tipo de cambio frente al dólar (no el bilateral) determina el traspaso a precios y volúmenes; la apreciación del dólar predice caídas del comercio mundial.
- **Uso en el bloque:** AS-ESTR (dólar amplio) y AS-EMAS/AS-EMLA/AS-EMEA: transmisión de un dólar fuerte a precios, comercio y divisas emergentes por la facturación en dólares.
- **Limitaciones:** Muestra centrada en Colombia y panel internacional de precios; el peso del euro como moneda de facturación es relevante para Europa.

#### FXA-0436 · Q 93 (A) — A Model of the International Monetary System

- **Autores:** Emmanuel Farhi; Matteo Maggiori
- **Año:** 2018
- **Publicación o institución:** The Quarterly Journal of Economics, vol. 133, n.º 1, págs. 295-355 (versión de trabajo NBER WP 22295, 2016)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-12 Divisas de refugio y sistema monetario internacional (principal) · secundarias: TX-01
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 9/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** https://ideas.repec.org/p/nbr/nberwo/22295.html
- **Acceso y licencia:** Artículo de pago (Oxford University Press); versión NBER
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Matteo Maggiori IDEAS RePEc "A Model of the International Monetary System" Farhi "International Currencies and Capital Allocation"»; WebFetch: sí)
- **Contenido:** Modelo de la oferta y demanda mundiales de activos de reserva en distintas monedas: hegemonía frente a multipolaridad, reservas abundantes frente a escasas, patrón oro frente a flotación; formaliza el dilema de Triffin, la advertencia de Nurkse sobre la inestabilidad multipolar y la recesión por escasez de reservas.
- **Uso en el bloque:** AS-ESTR y TR-BCM: marco teórico para tesis sobre la transición hacia un sistema multipolar y el riesgo de «confianza» en la moneda hegemónica.
- **Limitaciones:** Modelo teórico; no proporciona señales cuantitativas directas.

#### FXA-0420 · Q 92 (A) — Safe Haven Currencies

- **Autores:** Angelo Ranaldo; Paul Söderlind
- **Año:** 2010
- **Publicación o institución:** Review of Finance, vol. 14, n.º 3, págs. 385-407
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-12 Divisas de refugio y sistema monetario internacional (principal) · secundarias: TX-09
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / URL:** https://www.alexandria.unisg.ch/id/eprint/57677 (repositorio de la Universidad de St. Gallen) · https://ideas.repec.org/e/c/pra161.html
- **Acceso y licencia:** Artículo de pago (Oxford University Press); ficha y versión en el repositorio de St. Gallen
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Ranaldo Söderlind "Safe Haven Currencies" Review of Finance 2010»; WebFetch: sí)
- **Contenido:** Con datos de alta frecuencia (1993-2008) y un modelo factorial, muestra que el franco suizo y el yen se aprecian frente al dólar cuando caen las bolsas de EE. UU. y suben los bonos y la volatilidad cambiaria; el efecto refugio se observa de horas a días, es no lineal en la volatilidad y más fuerte en crisis.
- **Uso en el bloque:** AS-G10N y AS-ESTR (cesta de refugio JPY/CHF): definición operativa de divisa refugio y de su beta frente al riesgo; TR-PFV: respuesta esperada ante picos de volatilidad.
- **Limitaciones:** Muestra hasta 2008; la condición de refugio puede variar con la política monetaria (p. ej., suelo del CHF 2011-2015, tipos del BoJ).

#### FXA-0443 · Q 91 (A) — The stealth erosion of dollar dominance and the rise of nontraditional reserve currencies

- **Autores:** Serkan Arslanalp; Barry Eichengreen; Chima Simpson-Bell
- **Año:** 2022
- **Publicación o institución:** Journal of International Economics, vol. 138, art. 103656 (versión de trabajo: IMF WP 2022/058)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-12 Divisas de refugio y sistema monetario internacional (principal) · secundarias: TX-14, TX-10
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 9/10 · Acceso 6/10
- **DOI / URL:** DOI: 10.1016/j.jinteco.2022.103656 · https://ideas.repec.org/a/eee/inecon/v138y2022ics0022199622000885.html · versión abierta: https://www.imf.org/en/publications/wp/issues/2022/03/24/the-stealth-erosion-of-dollar-dominance-active-diversifiers-and-the-rise-of-nontraditional-515150
- **Acceso y licencia:** Artículo de pago; versión de trabajo del FMI en acceso abierto
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Arslanalp Eichengreen Simpson-Bell "The Stealth Erosion of Dollar Dominance" IMF working paper COFER»; WebFetch: sí, IDEAS)
- **Contenido:** Con datos COFER, la cuota del dólar en las reservas cae desde 1999 por diversificación activa de los gestores de reservas, no por efectos de valoración; el euro, el yen y la libra no ganan cuota: un cuarto va al renminbi y tres cuartos a divisas «no tradicionales» de países pequeños (AUD, CAD, KRW, SGD, divisas nórdicas).
- **Uso en el bloque:** AS-ESTR, AS-G10M y AS-EMAS: demanda estructural de reservas como apoyo a AUD, CAD, SGD, KRW o CNY; TR-BCM: lectura de COFER.
- **Limitaciones:** Datos hasta 2021; COFER no identifica tenedores por país.

#### FXA-0421 · Q 90 (A) — Getting Beyond Carry Trade: What Makes a Safe Haven Currency?

- **Autores:** Michael M. Habib; Livio Stracca
- **Año:** 2012
- **Publicación o institución:** Journal of International Economics, vol. 87, págs. 50-64
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-12 Divisas de refugio y sistema monetario internacional (principal) · secundarias: TX-04
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** Confirmada vía página índice: https://www.dallasfed.org/en/institute/~/media/documents/institute/wpapers/2014/0199.pdf (bibliografía de Fatum y Yamamoto, Dallas Fed GMPI WP 199)
- **Acceso y licencia:** Artículo de pago (Elsevier); existe versión de trabajo del BCE (no verificada en esta carga)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Ranaldo Söderlind "Safe Haven Currencies" Review of Finance 2010»; WebFetch: sí, de la página índice; no de la obra)
- **Contenido:** Busca los fundamentos que hacen de una divisa un refugio en un panel amplio de países: la posición de inversión internacional neta (y, en economías avanzadas, el tamaño del mercado de renta variable) predice el comportamiento refugio más allá del diferencial de tipos (carry).
- **Uso en el bloque:** AS-ESTR y AS-G10N: criterio estructural (PII neta) para evaluar si una divisa mantiene o pierde su condición de refugio; CONTRA: refutación de tesis «refugio» sin respaldo de balance externo.
- **Limitaciones:** Contenido descrito según conocimiento de la obra y la cita; resumen no leído en esta carga.

#### ANA-DOC-0365 · Q 88 (A) — The International Monetary and Financial System

- **Autores:** Pierre-Olivier Gourinchas; Hélène Rey; Maxime Sauzet
- **Año:** 2019
- **Publicación o institución:** Annual Review of Economics, vol. 11, págs. 859-893
- **Tipo de documento:** Artículo de revisión (survey) revisado por pares
- **Temática:** TX-12 Divisas de refugio y sistema monetario internacional (principal) · secundarias: TX-14
- **Calidad Q:** 88 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 7/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** https://ideas.repec.org/a/anr/reveco/v11y2019p859-893.html
- **Acceso y licencia:** Peldaño 2-3 (Annual Reviews; versión de trabajo NBER) · Licencia: Copyright Annual Reviews
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Hélène Rey IDEAS RePEc author page publications»; WebFetch: sí, sobre la página de autora de IDEAS que lista la obra) · reutilizada del F7 V3.2 (TA-07)
- **Contenido:** Revisión del sistema monetario y financiero internacional: papel del dólar, privilegio exorbitante, activos seguros y ciclo financiero global.
- **Uso en el bloque:** TR-BCM y AS-ESTR: marco de referencia del sistema monetario internacional (dólar, privilegio exorbitante, activos seguros) para tesis sobre hegemonía y fragmentación.
- **Limitaciones:** Resumen no leído en esta carga.

#### FXA-0428 · Q 88 (A) — Exorbitant Privilege: The Rise and Fall of the Dollar and the Future of the International Monetary System

- **Autores:** Barry Eichengreen
- **Año:** 2011
- **Publicación o institución:** Oxford University Press (ISBN 978-0-19-959671-3)
- **Tipo de documento:** Libro (monografía de referencia)
- **Temática:** TX-12 Divisas de refugio y sistema monetario internacional (principal) · secundarias: TX-14
- **Calidad Q:** 88 (A) — Tipo 20/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 10/10 · Independencia 10/10 · Acceso 9/10
- **DOI / URL:** Confirmada vía página índice: https://en.wikipedia.org/wiki/Exorbitant_privilege (referencias del artículo)
- **Acceso y licencia:** Libro comercial (Oxford University Press)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Exorbitant privilege Wikipedia Eichengreen 2011 Gourinchas Rey Govillot»; WebFetch: sí, de la página índice; no de la obra)
- **Contenido:** Historia del ascenso del dólar como moneda internacional desde 1914, de las fuentes de su «privilegio exorbitante» y de los escenarios para un sistema multipolar (euro, renminbi), con la tesis de que la primacía del dólar no es inamovible.
- **Uso en el bloque:** TR-BCM y AS-ESTR (dólar amplio): marco histórico e institucional para tesis de largo plazo sobre la hegemonía del dólar; RED: explicación al usuario.
- **Limitaciones:** Anterior a la experiencia post-2014 (sanciones, renminbi en el DEG); tono ensayístico.

#### FXA-0437 · Q 87 (A) — Financial Intermediation, International Risk Sharing, and Reserve Currencies

- **Autores:** Matteo Maggiori
- **Año:** 2017
- **Publicación o institución:** American Economic Review, vol. 107, n.º 10, págs. 3038-3071
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-12 Divisas de refugio y sistema monetario internacional (principal) · secundarias: TX-09
- **Calidad Q:** 87 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 7/10 · Independencia 10/10 · Acceso 3/10
- **DOI / URL:** Confirmada vía página índice: https://authors.repec.org/pro/pma2176 (perfil RePEc del autor)
- **Acceso y licencia:** De pago (AEA)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Matteo Maggiori IDEAS RePEc "A Model of the International Monetary System" Farhi "International Currencies and Capital Allocation"»; WebFetch: sí, de la página índice; no de la obra)
- **Contenido:** Explica la moneda de reserva por el mayor desarrollo financiero del país emisor, que asume más riesgo en tiempos normales y sufre pérdidas en crisis (seguro al resto del mundo); da fundamento a la apreciación del dólar en crisis.
- **Uso en el bloque:** AS-ESTR y AS-G10N: fundamento de la condición de refugio del USD frente al riesgo global.
- **Limitaciones:** Contenido descrito según conocimiento de la obra; resumen no leído en esta carga.

#### FXA-0438 · Q 86 (A) — International Currencies and Capital Allocation

- **Autores:** Matteo Maggiori; Brent Neiman; Jesse Schreger
- **Año:** 2020
- **Publicación o institución:** Journal of Political Economy (DOI 10.1086/705688)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-12 Divisas de refugio y sistema monetario internacional (principal) · secundarias: TX-07
- **Calidad Q:** 86 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 7/10 · Independencia 10/10 · Acceso 1/10
- **DOI / URL:** DOI: 10.1086/705688 · confirmada vía página índice: https://authors.repec.org/pro/pma2176
- **Acceso y licencia:** De pago (University of Chicago Press)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Matteo Maggiori IDEAS RePEc "A Model of the International Monetary System" Farhi "International Currencies and Capital Allocation"»; WebFetch: sí, de la página índice; no de la obra; el año no figura en el índice y se toma de la versión de trabajo)
- **Contenido:** Con datos de carteras de fondos a nivel de valor, documenta un fuerte sesgo hacia la moneda propia en las tenencias de bonos, salvo hacia el dólar: los inversores extranjeros prestan a empresas no estadounidenses sobre todo cuando emiten en dólares.
- **Uso en el bloque:** AS-EMAS/AS-EMLA/AS-EMEA y AS-ESTR: por qué la emisión en dólares atrae financiación y amplifica el «descalce» cambiario de los emergentes.
- **Limitaciones:** Año y páginas no confirmados en esta carga; contenido descrito según conocimiento de la obra.

#### ANA-DOC-0334 · Q 85 (A) — The Golden Dilemma

- **Autores:** Claude B. Erb; Campbell R. Harvey
- **Año:** 2013
- **Publicación o institución:** Financial Analysts Journal, vol. 69, n.º 4, págs. 10-42 (NBER WP 18706)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-12 Divisas de refugio y sistema monetario internacional (principal) · secundarias: TX-11
- **Calidad Q:** 85 (A) — Tipo 24/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 7/10 · Independencia 8/10 · Acceso 8/10
- **DOI / URL:** DOI 10.3386/w18706 · https://www.nber.org/papers/w18706 · copia del autor: https://people.duke.edu/~charvey/Research/Published_Papers/P113_The_golden_dilemma.pdf
- **Acceso y licencia:** Peldaño 1 (copia abierta en la web del autor y NBER) · Licencia: Copyright CFA Institute/autores
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Erb Harvey "The Golden Dilemma" Financial Analysts Journal 2013 gold»; WebFetch: sí) · reutilizada del F7 V3.2 (TA-08)
- **Contenido:** El oro preserva poder adquisitivo en horizontes seculares pero es mala cobertura de inflación a horizontes de inversión; precios reales altos han precedido rentabilidades reales bajas; la demanda de bancos centrales emergentes puede sostenerlo.
- **Uso en el bloque:** AS-ESTR: el oro como referencia de la cesta de refugio y como activo de reserva alternativo al dólar.
- **Limitaciones:** Independencia 8 por vinculación profesional de un autor con gestión de activos.

#### FXA-0430 · Q 85 (A) — From World Banker to World Venture Capitalist: US External Adjustment and the Exorbitant Privilege

- **Autores:** Pierre-Olivier Gourinchas; Hélène Rey
- **Año:** 2007 (versión NBER WP 11563, 2005)
- **Publicación o institución:** En R. Clarida (ed.), G7 Current Account Imbalances: Sustainability and Adjustment, University of Chicago Press, págs. 11-55 · NBER Working Paper 11563
- **Tipo de documento:** Capítulo de libro de conferencia NBER (revisado) / documento de trabajo
- **Temática:** TX-12 Divisas de refugio y sistema monetario internacional (principal) · secundarias: TX-07
- **Calidad Q:** 85 (A) — Tipo 20/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** https://www.nber.org/papers/w11563.pdf · capítulo confirmado en https://en.wikipedia.org/wiki/Exorbitant_privilege
- **Acceso y licencia:** Versión NBER de acceso según suscripción/abierto; capítulo de pago
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Exorbitant privilege Wikipedia Eichengreen 2011 Gourinchas Rey Govillot»; WebFetch: sí, PDF NBER)
- **Contenido:** Con activos y pasivos exteriores de EE. UU. a valor de mercado desde 1952, muestra que los activos rinden sustancialmente más que los pasivos (privilegio exorbitante), brecha ampliada tras Bretton Woods; EE. UU. pasa de «banquero mundial» a «capitalista riesgo mundial»; estima la depreciación necesaria para el ajuste externo.
- **Uso en el bloque:** TR-BCM y AS-ESTR: canal de valoración del ajuste externo de EE. UU. y su relación con la senda del dólar a largo plazo.
- **Limitaciones:** Datos hasta 2004; medición del diferencial discutida por Curcuru, Dvorak y Warnock (2008).

#### FXA-0444 · Q 84 (A) — Gold as international reserves: A barbarous relic no more?

- **Autores:** Serkan Arslanalp; Barry Eichengreen; Chima Simpson-Bell
- **Año:** 2023
- **Publicación o institución:** Journal of International Economics, vol. 145 (versión de trabajo: IMF WP 2023/014)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-12 Divisas de refugio y sistema monetario internacional (principal) · secundarias: TX-14, TX-11
- **Calidad Q:** 84 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 5/10 · Independencia 9/10 · Acceso 4/10
- **DOI / URL:** Confirmada vía página índice: https://ideas.repec.org/e/pei2.html (página de autor de Eichengreen en IDEAS)
- **Acceso y licencia:** Artículo de pago; versión de trabajo del FMI en acceso abierto (URL no verificada en esta carga)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Arslanalp Eichengreen Simpson-Bell "The Stealth Erosion of Dollar Dominance" IMF working paper COFER»; WebFetch: sí, de la página índice; no de la obra)
- **Contenido:** Analiza el regreso del oro como activo de reserva de los bancos centrales y sus determinantes, incluidos los riesgos de sanciones y la geopolítica (según el título y su contexto).
- **Uso en el bloque:** AS-ESTR (oro como referencia de la cesta de refugio) y TR-BCM: compras de oro de bancos centrales como señal de diversificación fuera del dólar.
- **Limitaciones:** Resumen no leído en esta carga.

#### FXA-0439 · Q 84 (A) — The Rise of the Dollar and Fall of the Euro as International Currencies

- **Autores:** Matteo Maggiori; Brent Neiman; Jesse Schreger
- **Año:** 2019
- **Publicación o institución:** AEA Papers and Proceedings, vol. 109, págs. 521-526 (NBER WP 25410; CEPR DP 13410)
- **Tipo de documento:** Artículo (actas revisadas)
- **Temática:** TX-12 Divisas de refugio y sistema monetario internacional (principal) · secundarias: —
- **Calidad Q:** 84 (A) — Tipo 22/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 7/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** DOI: 10.1257/pandp.20191007 · https://ideas.repec.org/a/aea/apandp/v109y2019p521-26.html
- **Acceso y licencia:** De pago (AEA); versiones NBER y CEPR
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Matteo Maggiori IDEAS RePEc "A Model of the International Monetary System" Farhi "International Currencies and Capital Allocation"»; WebFetch: sí)
- **Contenido:** Documenta que, tras la crisis financiera global, el uso del dólar ha aumentado y el del euro ha caído de forma paralela en reservas, emisión de bonos corporativos y soberanos, préstamos bancarios y facturación comercial.
- **Uso en el bloque:** AS-G10N (EUR/USD) y AS-ESTR: evidencia de largo plazo sobre la demanda estructural de dólares frente a euros.
- **Limitaciones:** Texto breve; datos hasta 2017-2018.

#### FXA-0429 · Q 84 (A) — How Global Currencies Work: Past, Present, and Future

- **Autores:** Barry Eichengreen; Arnaud Mehl; Livia Chiţu
- **Año:** 2018
- **Publicación o institución:** Princeton University Press (xv + 250 págs.; ISBN 9780691177007)
- **Tipo de documento:** Libro (monografía académica)
- **Temática:** TX-12 Divisas de refugio y sistema monetario internacional (principal) · secundarias: TX-14
- **Calidad Q:** 84 (A) — Tipo 20/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 7/10 · Independencia 9/10 · Acceso 7/10
- **DOI / URL:** Confirmada vía resultados de búsqueda: reseña en Business History Review (Cambridge University Press) https://www.cambridge.org/core/journals/business-history-review/article/how-global-currencies-work-past-present-and-future-bybarry-eichengreen-arnaud-mehl-andlivia-chitu-princeton-princeton-university-press-2018-xv-250-pp-figures-tables-notes-references-index-cloth-3950-isbn-9780691177007/F40546A4914941DA131C39202FE8E2F3
- **Acceso y licencia:** Libro comercial
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Eichengreen Mehl Chiţu "How Global Currencies Work: Past, Present, and Future" Princeton University Press»; WebFetch: no)
- **Contenido:** Con datos históricos nuevos (reservas, facturación, emisión de deuda), defiende frente a la visión de «moneda dominante única con fuertes externalidades de red» la de un sistema en el que pueden coexistir varias monedas internacionales; base para analizar la multipolaridad dólar–euro–renminbi.
- **Uso en el bloque:** AS-ESTR, TR-BCM y AS-EMAS: plausibilidad de escenarios de cuota creciente del euro o del renminbi en reservas y facturación.
- **Limitaciones:** Datos hasta 2016-2017; contenido descrito según conocimiento de la obra, sin lectura en esta carga.

#### FXA-0431 · Q 84 (A) — Exorbitant Privilege and Exorbitant Duty

- **Autores:** Pierre-Olivier Gourinchas; Hélène Rey; Nicolas Govillot
- **Año:** 2010
- **Publicación o institución:** Bank of Japan, IMES Discussion Paper 2010-E-20 (presentado también en conferencia del Tesoro de EE. UU., 2012)
- **Tipo de documento:** Documento de trabajo
- **Temática:** TX-12 Divisas de refugio y sistema monetario internacional (principal) · secundarias: TX-09
- **Calidad Q:** 84 (A) — Tipo 20/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** https://home.treasury.gov/system/files/276/2012-session-1-gourinchas-rey-govillot.pdf · serie IMES confirmada en https://en.wikipedia.org/wiki/Exorbitant_privilege
- **Acceso y licencia:** Acceso abierto (versión preliminar alojada por el Tesoro de EE. UU.)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Exorbitant privilege Wikipedia Eichengreen 2011 Gourinchas Rey Govillot»; WebFetch: sí)
- **Contenido:** Amplía los datos de posición exterior de EE. UU. hasta la crisis: el exceso de rentabilidad de los activos (privilegio) tiene como contrapartida un seguro al resto del mundo en tensiones globales (deber exorbitante): en 2007-2009 los pagos netos de EE. UU. al exterior rondaron el 19 % del PIB; modelo con menor aversión al riesgo en EE. UU.
- **Uso en el bloque:** AS-ESTR y PROS: por qué el dólar se aprecia en crisis globales pese a que EE. UU. pierde riqueza externa; escenarios de cola.
- **Limitaciones:** Versión preliminar («Please do not cite»); la versión definitiva no se ha verificado en esta carga.

#### FXA-0432 · Q 82 (A) — Exorbitant Privilege Gained and Lost: Fiscal Implications

- **Autores:** Zefeng Chen; Zhengyang Jiang; Hanno Lustig; Stijn Van Nieuwerburgh; Mindy Z. Xiaolan
- **Año:** 2025
- **Publicación o institución:** Journal of Political Economy (DOI 10.1086/738149)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-12 Divisas de refugio y sistema monetario internacional (principal) · secundarias: TX-14
- **Calidad Q:** 82 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 3/10 · Independencia 10/10 · Acceso 2/10
- **DOI / URL:** DOI: 10.1086/738149 · confirmada vía página índice: https://en.wikipedia.org/wiki/Exorbitant_privilege
- **Acceso y licencia:** De pago (University of Chicago Press)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Exorbitant privilege Wikipedia Eichengreen 2011 Gourinchas Rey Govillot»; WebFetch: sí, de la página índice; no de la obra)
- **Contenido:** Analiza las implicaciones fiscales para EE. UU. de ganar y perder el privilegio exorbitante (según el título: el valor de conveniencia de la deuda del Tesoro y su posible pérdida).
- **Uso en el bloque:** TR-BCM y CONTRA: escenarios de pérdida de estatus del dólar y su efecto en primas de la deuda y el tipo de cambio.
- **Limitaciones:** Resumen no leído en esta carga; obra muy reciente.

#### ANA-DOC-0557 · Q 82 (A) — The International Monetary Fund: 70 Years of Reinvention

- **Autores:** Carmen M. Reinhart; Christoph Trebesch
- **Año:** 2016
- **Publicación o institución:** Journal of Economic Perspectives, 30(1), 3–28
- **Tipo de documento:** Artículo revisado (acceso abierto)
- **Temática:** TX-12 Divisas de refugio y sistema monetario internacional (principal) · secundarias: TX-14
- **Calidad Q:** 82 (A) — Tipo 23/25 · Rigor 13/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 7/10 · Independencia 10/10 · Acceso 6/10
- **DOI / URL:** URL de acceso: https://authors.repec.org/pro/pre33 (perfil RePEc de C. M. Reinhart)
- **Acceso y licencia:** Peldaño 1 (JEP en acceso abierto)
- **Versión:** Versión publicada identificada en los perfiles de Reinhart y Trebesch
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Carmen Reinhart RePEc author profile»; WebFetch: sí, perfiles) · reutilizada del F7 V3.2 (TA-15)
- **Contenido:** Historia del FMI y de su transformación desde el sistema de Bretton Woods hasta prestamista de crisis de deuda, incluida su actuación en Europa.
- **Uso en el bloque:** TR-BCM: papel del FMI en el sistema monetario internacional (DEG, red de seguridad financiera, programas) como contexto de las divisas emergentes en tensión.
- **Estatus epistémico:** Ensayo histórico revisado
- **Limitaciones:** DOI no visto; carácter narrativo.

#### FXA-0449 · Q 82 (A) — When did the dollar overtake sterling as the leading international currency? Evidence from the bond markets

- **Autores:** Livia Chițu; Barry Eichengreen; Arnaud Mehl
- **Año:** 2014
- **Publicación o institución:** Journal of Development Economics, vol. 111, págs. 225-245
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-12 Divisas de refugio y sistema monetario internacional (principal) · secundarias: —
- **Calidad Q:** 82 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 6/10 · Independencia 9/10 · Acceso 2/10
- **DOI / URL:** Confirmada vía página índice: https://ideas.repec.org/e/pei2.html
- **Acceso y licencia:** De pago (Elsevier)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Arslanalp Eichengreen Simpson-Bell "The Stealth Erosion of Dollar Dominance" IMF working paper COFER»; WebFetch: sí, de la página índice; no de la obra)
- **Contenido:** Con datos de emisión de bonos internacionales, fecha el adelantamiento del dólar a la libra como moneda internacional líder (según el título), precedente histórico de relevo de moneda dominante.
- **Uso en el bloque:** PROS y CONTRA: precedente histórico para calibrar la velocidad de un posible relevo del dólar.
- **Limitaciones:** Resumen no leído en esta carga; evidencia histórica.

#### FXA-0434 · Q 82 (A) — Cross-Border Returns Differentials

- **Autores:** Stephanie Curcuru; Tomas Dvorak; Francis Warnock
- **Año:** 2008
- **Publicación o institución:** The Quarterly Journal of Economics, vol. 123, n.º 4, págs. 1495-1530
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-12 Divisas de refugio y sistema monetario internacional (principal) · secundarias: TX-07
- **Calidad Q:** 82 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 13/15 · Vigencia 7/10 · Impacto 8/10 · Independencia 10/10 · Acceso 2/10
- **DOI / URL:** DOI: 10.1162/qjec.2008.123.4.1495 · confirmada vía página índice: https://en.wikipedia.org/wiki/Exorbitant_privilege
- **Acceso y licencia:** De pago
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Exorbitant privilege Wikipedia Eichengreen 2011 Gourinchas Rey Govillot»; WebFetch: sí, de la página índice; no de la obra)
- **Contenido:** Contrapunto a la tesis del privilegio exorbitante: cuestiona la magnitud del diferencial de rentabilidad entre activos y pasivos exteriores de EE. UU. con datos de flujos y posiciones (según el título y su papel en el debate).
- **Uso en el bloque:** CONTRA: objeción a tesis que descansen en un diferencial de rentabilidad grande y estable a favor de EE. UU.
- **Limitaciones:** Resumen no leído en esta carga.

#### FXA-0452 · Q 80 (A) — The international role of the euro (edición de junio de 2026)

- **Autores:** Banco Central Europeo
- **Año:** 2026 (publicación anual)
- **Publicación o institución:** Banco Central Europeo (informe anual; nota de prensa del 2 de junio de 2026 «International role of the euro increased moderately in 2025»)
- **Tipo de documento:** Informe de organismo oficial con datos primarios
- **Temática:** TX-12 Divisas de refugio y sistema monetario internacional (principal) · secundarias: TX-14
- **Calidad Q:** 80 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 6/10 · Independencia 5/10 · Acceso 4/10
- **DOI / URL:** https://www.ecb.europa.eu/press/pr/date/2026/html/ecb.pr260602~f941e87516.en.html
- **Acceso y licencia:** Acceso abierto (BCE)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ECB "The international role of the euro" June 2025 report»; WebFetch: sí, nota de prensa; el informe completo no se pudo abrir)
- **Contenido:** Seguimiento anual del uso internacional del euro: en 2025 su cuota en un índice amplio de indicadores subió a ≈20 % (segunda moneda mundial), récord de emisión internacional de deuda en euros (+30 %), liderazgo en bonos verdes internacionales, entradas de cartera cerca de máximos y compras continuadas de oro por bancos centrales ante la fragmentación geopolítica.
- **Uso en el bloque:** AS-G10N (EUR) y TR-BCM: dato oficial anual de la cuota internacional del euro; AS-ESTR: indicadores de desdolarización y oro.
- **Limitaciones:** El emisor tiene interés institucional en la internacionalización del euro (independencia limitada); el informe completo no se leyó.

#### FXA-0440 · Q 80 (A) — Internationalizing Like China

- **Autores:** Christopher Clayton; Amanda Dos Santos; Matteo Maggiori; Jesse Schreger
- **Año:** 2025
- **Publicación o institución:** American Economic Review, vol. 115, n.º 3, págs. 864-902
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-12 Divisas de refugio y sistema monetario internacional (principal) · secundarias: TX-10, TX-08
- **Calidad Q:** 80 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 3/10 · Independencia 10/10 · Acceso 1/10
- **DOI / URL:** Confirmada vía página índice: https://authors.repec.org/pro/pma2176
- **Acceso y licencia:** De pago (AEA)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Matteo Maggiori IDEAS RePEc "A Model of the International Monetary System" Farhi "International Currencies and Capital Allocation"»; WebFetch: sí, de la página índice; no de la obra)
- **Contenido:** Estudia la estrategia china de internacionalización del renminbi con controles de capital (según el título): uso internacional de la moneda sin plena apertura de la cuenta financiera.
- **Uso en el bloque:** AS-EMAS (CNY/CNH) y AS-ESTR: evaluar tesis sobre el avance del renminbi como moneda internacional.
- **Limitaciones:** Resumen no leído en esta carga.

#### FXA-0450 · Q 80 (A) — Currency internationalization with Chinese characteristics: Is capital-account convertibility required for the renminbi to acquire reserve-currency status?

- **Autores:** Barry Eichengreen; Camille Macaire; Arnaud Mehl; Eric Monnet; Alain Naef
- **Año:** 2024
- **Publicación o institución:** International Finance, vol. 27, n.º 2, págs. 102-128 (versiones previas: Banque de France WP 892; CEPR DP 17498, 2022)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-12 Divisas de refugio y sistema monetario internacional (principal) · secundarias: TX-08, TX-10
- **Calidad Q:** 80 (A) — Tipo 24/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 3/10 · Independencia 9/10 · Acceso 3/10
- **DOI / URL:** Confirmada vía página índice: https://ideas.repec.org/e/pei2.html
- **Acceso y licencia:** De pago (Wiley); versión de trabajo de la Banque de France en abierto (URL no verificada)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Arslanalp Eichengreen Simpson-Bell "The Stealth Erosion of Dollar Dominance" IMF working paper COFER»; WebFetch: sí, de la página índice; no de la obra)
- **Contenido:** Pregunta si la convertibilidad de la cuenta de capital es necesaria para que el renminbi alcance estatus de moneda de reserva (según el título), con base en la experiencia china y en precedentes históricos.
- **Uso en el bloque:** AS-EMAS (CNY/CNH): límites del avance del renminbi como reserva con controles de capital.
- **Limitaciones:** Resumen no leído en esta carga.

#### FXA-0422 · Q 80 (A) — Intra-Safe Haven Currency Behavior During the Global Financial Crisis

- **Autores:** Rasmus Fatum; Yohei Yamamoto
- **Año:** 2014
- **Publicación o institución:** Federal Reserve Bank of Dallas, Globalization and Monetary Policy Institute, Working Paper n.º 199
- **Tipo de documento:** Documento de trabajo
- **Temática:** TX-12 Divisas de refugio y sistema monetario internacional (principal) · secundarias: TX-09
- **Calidad Q:** 80 (A) — Tipo 20/25 · Rigor 17/20 · Autoridad 12/15 · Vigencia 8/10 · Impacto 5/10 · Independencia 9/10 · Acceso 9/10
- **DOI / URL:** https://www.dallasfed.org/en/institute/~/media/documents/institute/wpapers/2014/0199.pdf
- **Acceso y licencia:** Acceso abierto (Reserva Federal de Dallas)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Ranaldo Söderlind "Safe Haven Currencies" Review of Finance 2010»; WebFetch: sí)
- **Contenido:** Analiza siete divisas (USD, JPY, CHF, EUR, GBP, SEK, CAD) entre sí frente al VIX con contrastes de umbral (Hansen 2000): el yen es el refugio «más seguro» y se aprecia con la incertidumbre a cualquier nivel; las demás muestran efectos umbral y el dólar no es el más seguro en ningún subperiodo (1999-2012).
- **Uso en el bloque:** AS-G10N y AS-ESTR: jerarquía de refugios y umbrales de VIX para activar la cesta de refugio; PROS: escenarios de aversión al riesgo.
- **Limitaciones:** Documento de trabajo; datos hasta 2012.

#### FXA-0453 · Q 78 (B) — Gaining Currency: The Rise of the Renminbi

- **Autores:** Eswar S. Prasad
- **Año:** 2016
- **Publicación o institución:** Oxford University Press (344 págs.)
- **Tipo de documento:** Libro (monografía de referencia)
- **Temática:** TX-12 Divisas de refugio y sistema monetario internacional (principal) · secundarias: TX-08, TX-10
- **Calidad Q:** 78 (B) — Tipo 20/25 · Rigor 13/20 · Autoridad 14/15 · Vigencia 7/10 · Impacto 7/10 · Independencia 9/10 · Acceso 8/10
- **DOI / URL:** Reseña en Finance & Development (FMI, dic. 2016, vol. 53, n.º 4): https://www.imf.org/external/pubs/ft/fandd/2016/12/book2.htm
- **Acceso y licencia:** Libro comercial; reseña en acceso abierto
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Eswar Prasad "Gaining Currency: The Rise of the Renminbi" Oxford University Press 2016»; WebFetch: sí, de la reseña del FMI; no de la obra)
- **Contenido:** Explica cómo China ha internacionalizado el renminbi sin abrir del todo la cuenta de capital (flujos controlados, inclusión en el DEG, AIIB, swaps), distingue moneda de reserva, internacionalización y apertura financiera, y sostiene que el renminbi ganará peso pero no desplazará al dólar como refugio sin reformas institucionales.
- **Uso en el bloque:** AS-EMAS (CNY/CNH) y AS-ESTR: marco conceptual para evaluar tesis sobre el ascenso del renminbi; RED: explicación al usuario.
- **Limitaciones:** Datos hasta 2016; el reseñista critica la rotundidad de las interpretaciones sobre motivaciones políticas internas.

#### FXA-0448 · Q 78 (B) — Stability or upheaval? The currency composition of international reserves in the long run

- **Autores:** Arnaud Mehl; Barry Eichengreen; Livia Chițu
- **Año:** 2014
- **Publicación o institución:** Banco Central Europeo, ECB Working Paper Series n.º 1715
- **Tipo de documento:** Documento de trabajo
- **Temática:** TX-12 Divisas de refugio y sistema monetario internacional (principal) · secundarias: —
- **Calidad Q:** 78 (B) — Tipo 20/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 5/10 · Independencia 8/10 · Acceso 6/10
- **DOI / URL:** Confirmada vía página índice: https://ideas.repec.org/e/pei2.html
- **Acceso y licencia:** Acceso abierto (BCE); URL propia no verificada en esta carga
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Arslanalp Eichengreen Simpson-Bell "The Stealth Erosion of Dollar Dominance" IMF working paper COFER»; WebFetch: sí, de la página índice; no de la obra)
- **Contenido:** Estudia la composición por monedas de las reservas internacionales a largo plazo (con datos históricos desde el siglo XIX) para valorar si es estable o propensa a cambios bruscos (según el título).
- **Uso en el bloque:** AS-ESTR y PROS: ritmo plausible de cambio en la composición de reservas para escenarios H4.
- **Limitaciones:** Resumen no leído en esta carga.

#### FXA-0445 · Q 76 (B) — Our Underappreciated International Reserve System

- **Autores:** Serkan Arslanalp; Barry Eichengreen; Chima Simpson-Bell
- **Año:** 2025
- **Publicación o institución:** NBER Working Paper 34478
- **Tipo de documento:** Documento de trabajo
- **Temática:** TX-12 Divisas de refugio y sistema monetario internacional (principal) · secundarias: —
- **Calidad Q:** 76 (B) — Tipo 20/25 · Rigor 14/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 2/10 · Independencia 9/10 · Acceso 6/10
- **DOI / URL:** Confirmada vía página índice: https://ideas.repec.org/e/pei2.html
- **Acceso y licencia:** NBER (acceso según suscripción)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Arslanalp Eichengreen Simpson-Bell "The Stealth Erosion of Dollar Dominance" IMF working paper COFER»; WebFetch: sí, de la página índice; no de la obra)
- **Contenido:** Valoración actualizada del sistema internacional de reservas por los mismos autores de la «erosión silenciosa» (según el título).
- **Uso en el bloque:** TR-BCM y AS-ESTR: actualización de la composición de reservas tras 2022.
- **Limitaciones:** Resumen no leído en esta carga; documento de trabajo reciente.

#### FXA-0451 · Q 76 (B) — RMBI or RMBR? Is the Renminbi Destined to Become a Global or Regional Currency?

- **Autores:** Barry Eichengreen; Domenico Lombardi
- **Año:** 2017
- **Publicación o institución:** Asian Economic Papers, vol. 16, n.º 1, págs. 35-59
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-12 Divisas de refugio y sistema monetario internacional (principal) · secundarias: TX-10
- **Calidad Q:** 76 (B) — Tipo 22/25 · Rigor 13/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 5/10 · Independencia 10/10 · Acceso 3/10
- **DOI / URL:** Confirmada vía página índice: https://ideas.repec.org/e/pei2.html
- **Acceso y licencia:** De pago (MIT Press)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Arslanalp Eichengreen Simpson-Bell "The Stealth Erosion of Dollar Dominance" IMF working paper COFER»; WebFetch: sí, de la página índice; no de la obra)
- **Contenido:** Discute si el renminbi está llamado a ser una moneda global o regional (asiática) (según el título).
- **Uso en el bloque:** AS-EMAS: papel del renminbi como ancla regional de las divisas asiáticas.
- **Limitaciones:** Resumen no leído en esta carga.

#### FXA-0423 · Q 74 (B) — The Curious Case of the Yen as a Safe Haven Currency: A Forensic Analysis

- **Autores:** Dennis Botman; Irineu de Carvalho Filho; W. Raphael Lam
- **Año:** 2013
- **Publicación o institución:** Fondo Monetario Internacional, IMF Working Paper 13/228
- **Tipo de documento:** Documento de trabajo
- **Temática:** TX-12 Divisas de refugio y sistema monetario internacional (principal) · secundarias: TX-06
- **Calidad Q:** 74 (B) — Tipo 20/25 · Rigor 15/20 · Autoridad 13/15 · Vigencia 7/10 · Impacto 5/10 · Independencia 9/10 · Acceso 5/10
- **DOI / URL:** Confirmada vía página índice: https://www.dallasfed.org/en/institute/~/media/documents/institute/wpapers/2014/0199.pdf (bibliografía de Fatum y Yamamoto 2014)
- **Acceso y licencia:** Acceso abierto (FMI); URL propia no verificada en esta carga
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Ranaldo Söderlind "Safe Haven Currencies" Review of Finance 2010»; WebFetch: sí, de la página índice; no de la obra)
- **Contenido:** Análisis «forense» de por qué el yen se aprecia en episodios de aversión al riesgo (según el título y su cita en la literatura de refugio).
- **Uso en el bloque:** AS-G10N (USD/JPY, cruces de JPY): mecanismos del comportamiento refugio del yen.
- **Limitaciones:** Resumen no leído en esta carga; contenido descrito por el título.

#### FXA-0427 · Q 74 (B) — Exchange Rates During Financial Crises

- **Autores:** Marion Kohler
- **Año:** 2010
- **Publicación o institución:** BIS Quarterly Review, marzo de 2010, págs. 39-50
- **Tipo de documento:** Informe técnico de organismo oficial
- **Temática:** TX-12 Divisas de refugio y sistema monetario internacional (principal) · secundarias: TX-09
- **Calidad Q:** 74 (B) — Tipo 15/25 · Rigor 14/20 · Autoridad 14/15 · Vigencia 7/10 · Impacto 6/10 · Independencia 9/10 · Acceso 9/10
- **DOI / URL:** Confirmada vía página índice: https://www.dallasfed.org/en/institute/~/media/documents/institute/wpapers/2014/0199.pdf (bibliografía de Fatum y Yamamoto 2014)
- **Acceso y licencia:** Acceso abierto (BPI); URL propia no verificada en esta carga
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Ranaldo Söderlind "Safe Haven Currencies" Review of Finance 2010»; WebFetch: sí, de la página índice; no de la obra)
- **Contenido:** Analiza los movimientos de los tipos de cambio en crisis financieras (incluida la de 2008), con atención a qué divisas se aprecian y cuáles se deprecian (según el título y su uso en la literatura de refugio).
- **Uso en el bloque:** AS-ESTR y CONTRA: comparación de patrones de crisis (2008 frente a crisis anteriores) para escenarios de cola.
- **Limitaciones:** Resumen no leído en esta carga.

#### FXA-0435 · Q 74 (B) — Excess Returns on Net Foreign Assets – The Exorbitant Privilege from a Global Perspective

- **Autores:** Maurizio Michael Habib
- **Año:** 2010
- **Publicación o institución:** Banco Central Europeo, ECB Working Paper Series n.º 1158
- **Tipo de documento:** Documento de trabajo
- **Temática:** TX-12 Divisas de refugio y sistema monetario internacional (principal) · secundarias: TX-07
- **Calidad Q:** 74 (B) — Tipo 20/25 · Rigor 15/20 · Autoridad 13/15 · Vigencia 7/10 · Impacto 5/10 · Independencia 9/10 · Acceso 5/10
- **DOI / URL:** Confirmada vía página índice: https://en.wikipedia.org/wiki/Exorbitant_privilege
- **Acceso y licencia:** Acceso abierto (BCE); URL propia no verificada en esta carga
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Exorbitant privilege Wikipedia Eichengreen 2011 Gourinchas Rey Govillot»; WebFetch: sí, de la página índice; no de la obra)
- **Contenido:** Mide el exceso de rentabilidad de los activos exteriores netos para un amplio grupo de países, situando el privilegio de EE. UU. en perspectiva global (según el título).
- **Uso en el bloque:** AS-ESTR y TR-BCM: comparar el privilegio del dólar con el de otras monedas de reserva (euro, yen, franco).
- **Limitaciones:** Resumen no leído en esta carga.

#### FXA-0446 · Q 72 (B) — From Dollar Dominance to Dollar Discontent

- **Autores:** Barry Eichengreen
- **Año:** 2026
- **Publicación o institución:** CEPR Discussion Paper 21372
- **Tipo de documento:** Documento de trabajo
- **Temática:** TX-12 Divisas de refugio y sistema monetario internacional (principal) · secundarias: TX-14
- **Calidad Q:** 72 (B) — Tipo 20/25 · Rigor 12/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 1/10 · Independencia 9/10 · Acceso 5/10
- **DOI / URL:** Confirmada vía página índice: https://ideas.repec.org/e/pei2.html
- **Acceso y licencia:** CEPR (acceso según suscripción)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Arslanalp Eichengreen Simpson-Bell "The Stealth Erosion of Dollar Dominance" IMF working paper COFER»; WebFetch: sí, de la página índice; no de la obra)
- **Contenido:** Análisis reciente del paso de la dominancia del dólar al «descontento» con el dólar en un contexto de tensiones geopolíticas y política estadounidense (según el título).
- **Uso en el bloque:** TR-BCM, AS-ESTR y CONTRA: vigilancia de la narrativa de desdolarización y de su evidencia.
- **Limitaciones:** Resumen no leído; documento muy reciente.

#### FXA-0447 · Q 72 (B) — An Opening for the Euro

- **Autores:** Barry Eichengreen; Arnaud Mehl; Isabel Vansteenkiste
- **Año:** 2026
- **Publicación o institución:** CEPR Discussion Paper 21265
- **Tipo de documento:** Documento de trabajo
- **Temática:** TX-12 Divisas de refugio y sistema monetario internacional (principal) · secundarias: —
- **Calidad Q:** 72 (B) — Tipo 20/25 · Rigor 12/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 1/10 · Independencia 9/10 · Acceso 5/10
- **DOI / URL:** Confirmada vía página índice: https://ideas.repec.org/e/pei2.html
- **Acceso y licencia:** CEPR (acceso según suscripción)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Arslanalp Eichengreen Simpson-Bell "The Stealth Erosion of Dollar Dominance" IMF working paper COFER»; WebFetch: sí, de la página índice; no de la obra)
- **Contenido:** Examina la oportunidad del euro para ganar peso internacional ante el «descontento» con el dólar (según el título).
- **Uso en el bloque:** AS-G10N (EUR/USD) y AS-ESTR: tesis estructurales de demanda de euros.
- **Limitaciones:** Resumen no leído; documento muy reciente; dos autores vinculados al BCE.

#### FXA-0454 · Q 72 (B) — Dollar Dominance in the International Reserve System: An Update

- **Autores:** Serkan Arslanalp; Barry Eichengreen; Chima Simpson-Bell
- **Año:** 2024 (11 de junio)
- **Publicación o institución:** Fondo Monetario Internacional, IMF Blog
- **Tipo de documento:** Divulgación especializada de organismo oficial con datos primarios (COFER)
- **Temática:** TX-12 Divisas de refugio y sistema monetario internacional (principal) · secundarias: TX-14
- **Calidad Q:** 72 (B) — Tipo 8/25 · Rigor 14/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 6/10 · Independencia 9/10 · Acceso 10/10
- **DOI / URL:** https://www.imf.org/en/blogs/articles/2024/06/11/dollar-dominance-in-the-international-reserve-system-an-update/index.md
- **Acceso y licencia:** Acceso abierto (FMI)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «IMF working paper geoeconomic fragmentation sanctions central bank reserves currency composition gold de-dollarization»; WebFetch: sí)
- **Contenido:** Actualiza con COFER (149 economías declarantes, ≈93 % de las reservas) la pérdida gradual de cuota del dólar a favor de divisas no tradicionales (AUD, CAD, CNY, KRW, SGD, nórdicas); el renminbi compensa un cuarto de la caída pero su cuota ajustada por tipo de cambio baja desde 2022; las sanciones empujan a algunos bancos centrales, modestamente, hacia el oro.
- **Uso en el bloque:** TR-BCM y AS-ESTR: lectura trimestral de COFER y su interpretación; AS-G10M: demanda de reservas en AUD/CAD.
- **Limitaciones:** Formato de blog; datos hasta 2023.

#### FXA-0441 · Q 72 (B) — China versus the United States: IMS Meets IPS

- **Autores:** Emmanuel Farhi; Matteo Maggiori
- **Año:** 2019
- **Publicación o institución:** AEA Papers and Proceedings, vol. 109, págs. 476-481
- **Tipo de documento:** Artículo (actas revisadas)
- **Temática:** TX-12 Divisas de refugio y sistema monetario internacional (principal) · secundarias: TX-14
- **Calidad Q:** 72 (B) — Tipo 22/25 · Rigor 12/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 4/10 · Independencia 10/10 · Acceso 0/10
- **DOI / URL:** Confirmada vía página índice: https://authors.repec.org/pro/pma2176
- **Acceso y licencia:** De pago (AEA)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Matteo Maggiori IDEAS RePEc "A Model of the International Monetary System" Farhi "International Currencies and Capital Allocation"»; WebFetch: sí, de la página índice; no de la obra)
- **Contenido:** Conecta el sistema monetario internacional (IMS) con el sistema político internacional (IPS) en la rivalidad China–EE. UU. (según el título).
- **Uso en el bloque:** TR-BCM y AS-EMAS: dimensión geopolítica de la competencia dólar–renminbi.
- **Limitaciones:** Resumen no leído en esta carga; texto breve.

#### FXA-0424 · Q 72 (B) — On Financial Risk and the Safe Haven Characteristics of Swiss Franc Exchange Rates

- **Autores:** Christian Grisse; Thomas Nitschka
- **Año:** 2013
- **Publicación o institución:** Banco Nacional Suizo, SNB Working Paper 2013-4
- **Tipo de documento:** Documento de trabajo
- **Temática:** TX-12 Divisas de refugio y sistema monetario internacional (principal) · secundarias: TX-08
- **Calidad Q:** 72 (B) — Tipo 20/25 · Rigor 15/20 · Autoridad 13/15 · Vigencia 7/10 · Impacto 4/10 · Independencia 8/10 · Acceso 5/10
- **DOI / URL:** Confirmada vía página índice: https://www.dallasfed.org/en/institute/~/media/documents/institute/wpapers/2014/0199.pdf (bibliografía de Fatum y Yamamoto 2014)
- **Acceso y licencia:** Acceso abierto (BNS); URL propia no verificada en esta carga
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Ranaldo Söderlind "Safe Haven Currencies" Review of Finance 2010»; WebFetch: sí, de la página índice; no de la obra)
- **Contenido:** Estudia la relación entre riesgo financiero global y los tipos de cambio del franco suizo para caracterizar su condición de refugio (según el título).
- **Uso en el bloque:** AS-G10N (EUR/CHF, USD/CHF): evidencia del propio banco central emisor sobre el franco como refugio.
- **Limitaciones:** Resumen no leído; posible sesgo institucional del emisor.

#### FXA-0426 · Q 72 (B) — Y2K Fears and Safe Haven Trading of the U.S. Dollar

- **Autores:** Aditya Kaul; Stephen Sapp
- **Año:** 2006
- **Publicación o institución:** Journal of International Money and Finance, vol. 25, págs. 760-779
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-12 Divisas de refugio y sistema monetario internacional (principal) · secundarias: TX-14
- **Calidad Q:** 72 (B) — Tipo 25/25 · Rigor 14/20 · Autoridad 10/15 · Vigencia 6/10 · Impacto 5/10 · Independencia 10/10 · Acceso 2/10
- **DOI / URL:** Confirmada vía página índice: https://www.dallasfed.org/en/institute/~/media/documents/institute/wpapers/2014/0199.pdf (bibliografía de Fatum y Yamamoto 2014)
- **Acceso y licencia:** De pago (Elsevier)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Ranaldo Söderlind "Safe Haven Currencies" Review of Finance 2010»; WebFetch: sí, de la página índice; no de la obra)
- **Contenido:** Estudio de evento sobre la demanda de dólares como refugio ante los temores del efecto 2000 (Y2K) (según el título).
- **Uso en el bloque:** AS-G10N y PROS: precedente de demanda de refugio en dólares ante un riesgo de evento anunciado.
- **Limitaciones:** Resumen no leído; episodio único y antiguo.

#### FXA-0433 · Q 70 (B) — Our Dollar, Your Problem

- **Autores:** Kenneth Rogoff
- **Año:** 2025
- **Publicación o institución:** Yale University Press (ISBN 978-0-300-28371-6)
- **Tipo de documento:** Libro (ensayo de autor de referencia)
- **Temática:** TX-12 Divisas de refugio y sistema monetario internacional (principal) · secundarias: TX-14
- **Calidad Q:** 70 (B) — Tipo 12/25 · Rigor 12/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 5/10 · Independencia 9/10 · Acceso 7/10
- **DOI / URL:** DOI: 10.2307/jj.27401515 · confirmada vía página índice: https://en.wikipedia.org/wiki/Exorbitant_privilege
- **Acceso y licencia:** Libro comercial
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Exorbitant privilege Wikipedia Eichengreen 2011 Gourinchas Rey Govillot»; WebFetch: sí, de la página índice; no de la obra)
- **Contenido:** Ensayo sobre el papel global del dólar, sus costes para el resto del mundo y los riesgos para su primacía (según el título, eco de la frase de Connally).
- **Uso en el bloque:** TR-BCM y RED: visión actual de un autor clave sobre la sostenibilidad de la dominancia del dólar.
- **Limitaciones:** Ensayo divulgativo; no leído en esta carga.

#### FXA-0425 · Q 70 (B) — Looking at the Other Side of Carry Trades: Are there any Safe Haven Currencies?

- **Autores:** Virginie Coudert; Cyriac Guillaumin; Hélène Raymond
- **Año:** 2014
- **Publicación o institución:** CEPII Working Paper 2014-03
- **Tipo de documento:** Documento de trabajo
- **Temática:** TX-12 Divisas de refugio y sistema monetario internacional (principal) · secundarias: TX-04
- **Calidad Q:** 70 (B) — Tipo 20/25 · Rigor 14/20 · Autoridad 11/15 · Vigencia 7/10 · Impacto 4/10 · Independencia 9/10 · Acceso 5/10
- **DOI / URL:** Confirmada vía página índice: https://www.dallasfed.org/en/institute/~/media/documents/institute/wpapers/2014/0199.pdf (bibliografía de Fatum y Yamamoto 2014)
- **Acceso y licencia:** Acceso abierto (CEPII); URL propia no verificada en esta carga
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Ranaldo Söderlind "Safe Haven Currencies" Review of Finance 2010»; WebFetch: sí, de la página índice; no de la obra)
- **Contenido:** Examina las divisas de financiación del carry para determinar si se comportan como refugios en episodios de tensión (según el título).
- **Uso en el bloque:** AS-ESTR: relación entre divisas de financiación del carry y cesta de refugio; CONTRA: riesgo de desmontaje.
- **Limitaciones:** Resumen no leído en esta carga; contenido descrito por el título.

#### FXA-0442 · Q 58 (C) — Hegemony or Harmony? A Unified Framework for the International Monetary System

- **Autores:** Tao Liu; Dong Lu; Liang Wang
- **Año:** 2023 (revisión de 2025: WP 202504)
- **Publicación o institución:** University of Hawaii at Manoa, Department of Economics, Working Paper 202305
- **Tipo de documento:** Documento de trabajo
- **Temática:** TX-12 Divisas de refugio y sistema monetario internacional (principal) · secundarias: TX-14
- **Calidad Q:** 58 (C) — Tipo 15/25 · Rigor 13/20 · Autoridad 7/15 · Vigencia 9/10 · Impacto 1/10 · Independencia 9/10 · Acceso 4/10
- **DOI / URL:** https://ideas.repec.org/p/hai/wpaper/202305.html
- **Acceso y licencia:** Acceso abierto
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Matteo Maggiori IDEAS RePEc "A Model of the International Monetary System" Farhi "International Currencies and Capital Allocation"»; WebFetch: sí)
- **Contenido:** Modelo monetario microfundamentado que reconcilia el sistema unipolar y el multipolar según si los papeles de medio de cambio y depósito de valor se refuerzan o compiten por la oferta de activos seguros; analiza el efecto de sanciones financieras sobre la moneda dominante.
- **Uso en el bloque:** AS-ESTR y CONTRA: condiciones teóricas bajo las que las sanciones o la escasez de activos seguros favorecen la diversificación fuera del dólar.
- **Limitaciones:** Documento de trabajo no publicado; autores con menor trayectoria en el campo.

## TX-13 Previsión de tipos de cambio y su evaluación

#### ANA-DOC-0246 · Q 92 (A) — Strictly Proper Scoring Rules, Prediction, and Estimation

- **Autores:** Tilmann Gneiting; Adrian E. Raftery
- **Año:** 2007
- **Publicación o institución:** Journal of the American Statistical Association, vol. 102 (copia de informe técnico en DTIC, ADA459827)
- **Tipo de documento:** Artículo revisado por pares (método)
- **Temática:** TX-13 Previsión de tipos de cambio y su evaluación (principal) · secundarias: —
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** DOI: 10.1198/016214506000001437 · Confirmada vía página índice: https://colab.ws/articles/10.1198%2F016214506000001437 (registro bibliográfico devuelto por la búsqueda, con DOI)
- **Acceso y licencia:** Copia de informe técnico de libre distribución en DTIC (apps.dtic.mil, ADA459827) · Licencia: copyright ASA para la versión publicada
- **Versión:** Publicada (metadatos según la página índice)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Gneiting Raftery 2007 "Strictly Proper Scoring Rules, Prediction, and Estimation" JASA»; WebFetch: sí, de la página índice; no de la obra) · reutilizada del F7 V3.2 (TA-04)
- **Contenido:** Teoría de las reglas de puntuación estrictamente propias (logarítmica, Brier, CRPS) para evaluar pronósticos probabilísticos y su uso en estimación.
- **Uso en el bloque:** EVAL: reglas de puntuación propias para calificar pronósticos probabilísticos de divisas (probabilidad de superar un nivel).
- **Estatus epistémico:** Método estadístico revisado por pares, de referencia; nivel alto.
- **Limitaciones:** Metadatos de volumen y páginas no confirmados en esta carga; técnico.
- **Disciplinas y etiquetas:** Estadística · reglas-de-puntuacion; pronostico-probabilistico; crps

#### ANA-DOC-0225 · Q 92 (A) — Comparing Predictive Accuracy

- **Autores:** Francis X. Diebold; Roberto S. Mariano
- **Año:** 1995
- **Publicación o institución:** Journal of Business and Economic Statistics, vol. 13, págs. 253-263
- **Tipo de documento:** Artículo revisado por pares (método)
- **Temática:** TX-13 Previsión de tipos de cambio y su evaluación (principal) · secundarias: —
- **Calidad Q:** 92 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** Confirmada vía página índice: https://www.nber.org/papers/w18391.pdf (bibliografía de Diebold, NBER WP 18391)
- **Acceso y licencia:** Texto editorial por suscripción; sin copia abierta verificada en esta carga · Licencia: copyright del editor
- **Versión:** Publicada (metadatos según la página índice)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Diebold Mariano 1995 "Comparing Predictive Accuracy" Journal of Business & Economic Statistics»; WebFetch: sí, de la página índice; no de la obra) · reutilizada del F7 V3.2 (TA-04)
- **Contenido:** Propone la prueba de Diebold-Mariano para comparar la precisión de dos pronósticos bajo funciones de pérdida generales, sin requerir modelos anidados.
- **Uso en el bloque:** EVAL y PROS: prueba estándar para comparar la precisión de un pronóstico cambiario frente al paseo aleatorio o el forward (modelos no anidados).
- **Estatus epistémico:** Método revisado por pares, estándar del campo; nivel alto.
- **Limitaciones:** Diseñada para comparar pronósticos, no modelos; problemas con modelos anidados (véase Clark-McCracken).
- **Disciplinas y etiquetas:** Econometría de la previsión · diebold-mariano; precision-predictiva; contraste

#### ANA-DOC-0229 · Q 91 (A) — The Model Confidence Set

- **Autores:** Peter R. Hansen; Asger Lunde; James M. Nason
- **Año:** 2011
- **Publicación o institución:** Econometrica, vol. 79, págs. 453-497
- **Tipo de documento:** Artículo revisado por pares (método)
- **Temática:** TX-13 Previsión de tipos de cambio y su evaluación (principal) · secundarias: —
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** Confirmada vía página índice: https://www.nber.org/papers/w18391.pdf (bibliografía de Diebold, NBER WP 18391)
- **Acceso y licencia:** Texto editorial por suscripción; sin copia abierta verificada en esta carga · Licencia: copyright del editor
- **Versión:** Publicada (metadatos según la página índice)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Diebold Mariano 1995 "Comparing Predictive Accuracy" Journal of Business & Economic Statistics»; WebFetch: sí, de la página índice; no de la obra) · reutilizada del F7 V3.2 (TA-04)
- **Contenido:** Construye un conjunto de modelos que contiene el mejor con una confianza dada, evitando elegir un único ganador cuando los datos no discriminan.
- **Uso en el bloque:** EVAL: selección del conjunto de modelos cambiarios estadísticamente indistinguibles del mejor.
- **Estatus epistémico:** Método revisado por pares; nivel alto.
- **Limitaciones:** Depende de la función de pérdida y del bootstrap elegido.
- **Disciplinas y etiquetas:** Econometría de la previsión · model-confidence-set; seleccion-de-modelos

#### ANA-DOC-0228 · Q 91 (A) — Tests of Conditional Predictive Ability

- **Autores:** Raffaella Giacomini; Halbert White
- **Año:** 2006
- **Publicación o institución:** Econometrica, vol. 74, págs. 1545-1578
- **Tipo de documento:** Artículo revisado por pares (método)
- **Temática:** TX-13 Previsión de tipos de cambio y su evaluación (principal) · secundarias: —
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** Confirmada vía página índice: https://www.nber.org/papers/w18391.pdf (bibliografía de Diebold, NBER WP 18391)
- **Acceso y licencia:** Texto editorial por suscripción; sin copia abierta verificada en esta carga · Licencia: copyright del editor
- **Versión:** Publicada (metadatos según la página índice)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Diebold Mariano 1995 "Comparing Predictive Accuracy" Journal of Business & Economic Statistics»; WebFetch: sí, de la página índice; no de la obra) · reutilizada del F7 V3.2 (TA-04)
- **Contenido:** Propone pruebas de capacidad predictiva condicional que evalúan métodos de pronóstico (modelo más ventana de estimación) y admiten modelos anidados y entornos cambiantes.
- **Uso en el bloque:** EVAL y PROS: contraste condicional de capacidad predictiva (en qué estados del mercado una señal cambiaria funciona).
- **Estatus epistémico:** Método revisado por pares; nivel alto.
- **Limitaciones:** Requiere ventanas de estimación rodantes o fijas; técnico.
- **Disciplinas y etiquetas:** Econometría de la previsión · capacidad-predictiva-condicional; giacomini-white

#### FXA-0480 · Q 91 (A) — Empirical exchange rate models of the nineties: Are any fit to survive?

- **Autores:** Yin-Wong Cheung; Menzie D. Chinn; Antonio Garcia Pascual
- **Año:** 2005
- **Publicación o institución:** Journal of International Money and Finance, vol. 24, págs. 1150-1175 (NBER WP 9393, 2002; IMF WP 04/73)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-13 Previsión de tipos de cambio y su evaluación (principal) · secundarias: TX-03
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 14/15 · Vigencia 8/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / URL:** DOI: 10.1016/j.jimonfin.2005.08.002 · versión del autor: https://users.ssc.wisc.edu/~mchinn/CCG-P_JIMF.pdf · https://nber.org/papers/w9393
- **Acceso y licencia:** Versión del autor de libre acceso; artículo de pago (Elsevier)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Cheung Chinn Garcia Pascual "Empirical exchange rate models of the nineties: Are any fit to survive?" "Exchange rate prediction redux"»; WebFetch: sí)
- **Contenido:** Evalúa modelos de los noventa (paridad de intereses, productividad, BEER compuesto) frente a PPA, monetario de precios rígidos y paseo aleatorio para CAD, GBP, DEM y JPY a 1, 4 y 20 trimestres con ECM, dirección del cambio y «consistencia»: ninguna combinación funciona bien en todos los periodos y criterios; los modelos estructurales rara vez baten al paseo aleatorio en ECM, pero sí a veces en dirección.
- **Uso en el bloque:** PROS y EVAL: protocolo de evaluación (ECM, dirección, consistencia) y expectativa realista del acierto de los modelos fundamentales.
- **Limitaciones:** Muestra hasta 2000; cuatro divisas principales.

#### ANA-DOC-0230 · Q 91 (A) — A Reality Check for Data Snooping

- **Autores:** Halbert White
- **Año:** 2000
- **Publicación o institución:** Econometrica, vol. 68, págs. 1097-1126
- **Tipo de documento:** Artículo revisado por pares (método)
- **Temática:** TX-13 Previsión de tipos de cambio y su evaluación (principal) · secundarias: —
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** Confirmada vía página índice: https://www.nber.org/papers/w18391.pdf (bibliografía de Diebold, NBER WP 18391)
- **Acceso y licencia:** Texto editorial por suscripción; sin copia abierta verificada en esta carga · Licencia: copyright del editor
- **Versión:** Publicada (metadatos según la página índice)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Diebold Mariano 1995 "Comparing Predictive Accuracy" Journal of Business & Economic Statistics»; WebFetch: sí, de la página índice; no de la obra) · reutilizada del F7 V3.2 (TA-04)
- **Contenido:** Propone el «Reality Check» bootstrap para contrastar si el mejor de muchos modelos supera a una referencia teniendo en cuenta la búsqueda de especificaciones.
- **Uso en el bloque:** EVAL y CONTRA: corrección por búsqueda de especificaciones al evaluar muchas reglas o modelos cambiarios (base de la crítica de Blomberg y Mountford, FXA-0474).
- **Estatus epistémico:** Método revisado por pares; nivel alto.
- **Limitaciones:** Conservador cuando se incluyen muchos modelos irrelevantes (véase la prueba SPA de Hansen).
- **Disciplinas y etiquetas:** Econometría de la previsión · data-snooping; reality-check; bootstrap

#### FXA-0481 · Q 90 (A) — Exchange rate prediction redux: New models, new data, new currencies

- **Autores:** Yin-Wong Cheung; Menzie D. Chinn; Antonio Garcia Pascual; Yi Zhang
- **Año:** 2019
- **Publicación o institución:** Journal of International Money and Finance, vol. 95, págs. 332-362 (NBER WP 23267; ECB WP 2018, 2017)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-13 Previsión de tipos de cambio y su evaluación (principal) · secundarias: TX-02, TX-03
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** DOI: 10.1016/j.jimonfin.2018.03.010 · https://ideas.repec.org/a/eee/jimfin/v95y2019icp332-362.html · versión de trabajo: https://www.nber.org/papers/w23267.pdf
- **Acceso y licencia:** Artículo de pago; versiones NBER y BCE
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «"Exchange rate prediction redux: New models, new data, new currencies" Cheung Chinn Garcia Pascual Zhang 2019»; WebFetch: sí)
- **Contenido:** Extiende el estudio de 2005 con reglas de Taylor, factores de la curva, tipos sombra y proxies de riesgo y liquidez: ningún modelo bate de forma consistente al paseo aleatorio en ECM, aunque la PPA se comporta relativamente bien; algunos modelos estructurales aciertan la dirección; la mejor combinación modelo-especificación-divisa cambia de un periodo a otro.
- **Uso en el bloque:** PROS, EVAL y CONTRA: referencia actualizada de la dificultad de batir al paseo aleatorio; justificación de usar la PPA como ancla de medio plazo.
- **Limitaciones:** Frecuencia trimestral; resultados agregados por divisa.

#### ANA-DOC-0226 · Q 90 (A) — Comparing Predictive Accuracy, Twenty Years Later: A Personal Perspective on the Use and Abuse of Diebold-Mariano Tests

- **Autores:** Francis X. Diebold
- **Año:** 2015 (NBER WP 18391, 2012)
- **Publicación o institución:** Journal of Business and Economic Statistics, vol. 33, n.º 1 · NBER Working Paper 18391 (septiembre de 2012)
- **Tipo de documento:** Artículo revisado por pares (ensayo metodológico)
- **Temática:** TX-13 Previsión de tipos de cambio y su evaluación (principal) · secundarias: —
- **Calidad Q:** 90 (A) — Tipo 22/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 10/10 · Acceso 10/10
- **DOI / URL:** https://www.nber.org/papers/w18391.pdf · RePEc: https://ideas.repec.org/a/taf/jnlbes/v33y2015i1p1-1.html
- **Acceso y licencia:** Versión de trabajo abierta en NBER · Licencia: copyright del autor / ASA
- **Versión:** Publicada; coexiste la versión NBER 2012
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Diebold Mariano 1995 "Comparing Predictive Accuracy" Journal of Business & Economic Statistics»; WebFetch: sí) · reutilizada del F7 V3.2 (TA-04)
- **Contenido:** Revisión crítica del uso de la prueba DM: sirve para comparar pronósticos, no para seleccionar modelos; discute la división de muestra y el abuso de comparaciones fuera de muestra.
- **Uso en el bloque:** EVAL: uso correcto (y abusos) de la prueba Diebold-Mariano al evaluar pronósticos cambiarios.
- **Estatus epistémico:** Ensayo metodológico del autor del método; nivel alto.
- **Limitaciones:** Perspectiva personal; no aporta evidencia empírica nueva.
- **Disciplinas y etiquetas:** Econometría de la previsión · evaluacion-fuera-de-muestra; buenas-practicas

#### FXA-0489 · Q 90 (A) — Out-of-Sample Exchange Rate Predictability with Taylor Rule Fundamentals

- **Autores:** Tanya Molodtsova; David H. Papell
- **Año:** 2009 (versión del autor del 25 de noviembre de 2008)
- **Publicación o institución:** Journal of International Economics (versión publicada: datos de volumen no verificados en esta carga)
- **Tipo de documento:** Artículo revisado por pares (versión del autor)
- **Temática:** TX-13 Previsión de tipos de cambio y su evaluación (principal) · secundarias: TX-02
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 13/15 · Vigencia 8/10 · Impacto 10/10 · Independencia 10/10 · Acceso 6/10
- **DOI / URL:** https://www.uh.edu/~dpapell/Taylor%20Rule%20Fundamentals.pdf
- **Acceso y licencia:** Versión del autor de libre acceso (Universidad de Houston)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Molodtsova Papell 2009 "Out-of-sample exchange rate predictability with Taylor rule fundamentals" Journal of International Economics»; WebFetch: sí)
- **Contenido:** Con fundamentos de regla de Taylor (inflación, brecha de producción, suavizado de tipos, coeficientes heterogéneos), encuentra predictibilidad a corto plazo fuera de muestra para 11 de 12 divisas frente al dólar en el periodo de flotación, muy superior a los modelos de paridad de intereses, PPA o monetarios.
- **Uso en el bloque:** TR-BCM y PROS: base para señales de divisas derivadas de la senda esperada de los bancos centrales; EVAL: uso de Clark-West frente al paseo aleatorio.
- **Limitaciones:** El rendimiento empeoró durante la crisis de 2007-2009 una vez corregida la inestabilidad (comentario de Rossi en el NBER Macroeconomics Annual 2013).

#### ANA-DOC-0227 · Q 90 (A) — Asymptotic Inference About Predictive Ability

- **Autores:** Kenneth D. West
- **Año:** 1996
- **Publicación o institución:** Econometrica, vol. 64, págs. 1067-1084
- **Tipo de documento:** Artículo revisado por pares (método)
- **Temática:** TX-13 Previsión de tipos de cambio y su evaluación (principal) · secundarias: —
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 9/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** Confirmada vía página índice: https://www.nber.org/papers/w18391.pdf (bibliografía de Diebold, NBER WP 18391)
- **Acceso y licencia:** Texto editorial por suscripción; sin copia abierta verificada en esta carga · Licencia: copyright del editor
- **Versión:** Publicada (metadatos según la página índice)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Diebold Mariano 1995 "Comparing Predictive Accuracy" Journal of Business & Economic Statistics»; WebFetch: sí, de la página índice; no de la obra) · reutilizada del F7 V3.2 (TA-04)
- **Contenido:** Desarrolla la inferencia asintótica sobre la capacidad predictiva teniendo en cuenta la incertidumbre por la estimación de parámetros.
- **Uso en el bloque:** EVAL: inferencia con incertidumbre de estimación en la comparación fuera de muestra de modelos cambiarios.
- **Estatus epistémico:** Método econométrico revisado por pares; nivel alto.
- **Limitaciones:** Técnico; supuestos de regularidad sobre los modelos comparados.
- **Disciplinas y etiquetas:** Econometría de la previsión · inferencia; incertidumbre-de-parametros

#### ANA-DOC-0232 · Q 88 (A) — Forecast Comparisons in Unstable Environments

- **Autores:** Raffaella Giacomini; Barbara Rossi
- **Año:** 2010
- **Publicación o institución:** Journal of Applied Econometrics, vol. 25, págs. 595-620
- **Tipo de documento:** Artículo revisado por pares (método)
- **Temática:** TX-13 Previsión de tipos de cambio y su evaluación (principal) · secundarias: —
- **Calidad Q:** 88 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** Confirmada vía página índice: https://www.nber.org/papers/w18391.pdf (bibliografía de Diebold, NBER WP 18391)
- **Acceso y licencia:** Texto editorial por suscripción; sin copia abierta verificada en esta carga · Licencia: copyright del editor
- **Versión:** Publicada (metadatos según la página índice)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Diebold Mariano 1995 "Comparing Predictive Accuracy" Journal of Business & Economic Statistics»; WebFetch: sí, de la página índice; no de la obra) · reutilizada del F7 V3.2 (TA-04)
- **Contenido:** Propone pruebas de precisión relativa que detectan cambios en el tiempo del rendimiento de los pronósticos (inestabilidad).
- **Uso en el bloque:** EVAL y PROS: evaluación con inestabilidad (prueba de fluctuación), clave en divisas, donde la capacidad predictiva cambia en el tiempo.
- **Estatus epistémico:** Método revisado por pares; nivel alto.
- **Limitaciones:** Técnico; requiere series de pérdidas suficientemente largas.
- **Disciplinas y etiquetas:** Econometría de la previsión · inestabilidad; fluctuation-test

#### FXA-0490 · Q 88 (A) — Exchange Rate Models Are Not as Bad as You Think

- **Autores:** Charles Engel; Nelson C. Mark; Kenneth D. West
- **Año:** 2007
- **Publicación o institución:** En D. Acemoglu, K. Rogoff y M. Woodford (eds.), NBER Macroeconomics Annual 2007, University of Chicago Press, págs. 381-441
- **Tipo de documento:** Artículo revisado (volumen anual NBER)
- **Temática:** TX-13 Previsión de tipos de cambio y su evaluación (principal) · secundarias: TX-01, TX-03
- **Calidad Q:** 88 (A) — Tipo 22/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 4/10
- **DOI / URL:** Confirmada vía página índice: https://www.uh.edu/~dpapell/Taylor%20Rule%20Fundamentals.pdf (bibliografía de Molodtsova y Papell)
- **Acceso y licencia:** Volumen NBER (versión de trabajo NBER disponible; URL no verificada)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Molodtsova Papell 2009 "Out-of-sample exchange rate predictability with Taylor rule fundamentals" Journal of International Economics»; WebFetch: sí, de la página índice; no de la obra)
- **Contenido:** Defiende que batir al paseo aleatorio no es el criterio adecuado para juzgar los modelos; con datos de panel y horizontes largos, los modelos monetarios, de PPA y de reglas de Taylor tienen cierto poder predictivo, y los tipos de cambio incorporan expectativas sobre los fundamentos.
- **Uso en el bloque:** PROS y EVAL: marco para combinar fundamentos de panel a horizontes H3-H4; matizar el «Meese-Rogoff» en informes.
- **Limitaciones:** Contenido descrito según conocimiento de la obra; resumen no leído.

#### ANA-DOC-0236 · Q 88 (A) — Forecast Combinations

- **Autores:** Allan Timmermann
- **Año:** 2006
- **Publicación o institución:** Handbook of Economic Forecasting, vol. 1 (eds. G. Elliott, C. W. J. Granger y A. Timmermann), Elsevier / North-Holland
- **Tipo de documento:** Capítulo de manual de referencia (survey)
- **Temática:** TX-13 Previsión de tipos de cambio y su evaluación (principal) · secundarias: —
- **Calidad Q:** 88 (A) — Tipo 22/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 10/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** Confirmada vía página índice: https://econpapers.repec.org/bookchap/eeeecofor/1.htm (índice del Handbook en EconPapers/RePEc)
- **Acceso y licencia:** Texto editorial por suscripción; sin copia abierta verificada en esta carga · Licencia: copyright del editor
- **Versión:** Publicada (metadatos según la página índice)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Handbook of Economic Forecasting Volume 1 2006 Elliott Granger Timmermann chapters "Forecast Combinations" "Forecast Evaluation"»; WebFetch: sí, de la página índice; no de la obra) · reutilizada del F7 V3.2 (TA-04)
- **Contenido:** Revisión de la combinación de pronósticos: por qué los promedios simples suelen ser difíciles de batir y cuándo conviene ponderar.
- **Uso en el bloque:** PROS: combinación de pronósticos cambiarios (modelos fundamentales, forward, encuestas) frente a apostar por uno.
- **Estatus epistémico:** Capítulo de manual de referencia del campo; nivel alto.
- **Limitaciones:** Estado del arte a 2006; el vol. 2 (2013) actualiza parte de los temas.
- **Disciplinas y etiquetas:** Econometría de la previsión · handbook; combinacion-de-pronosticos; promedios

#### FXA-0482 · Q 88 (A) — Exchange Rates and Fundamentals

- **Autores:** Charles Engel; Kenneth D. West
- **Año:** 2005
- **Publicación o institución:** Journal of Political Economy, vol. 113, págs. 485-517
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-13 Previsión de tipos de cambio y su evaluación (principal) · secundarias: TX-01
- **Calidad Q:** 88 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 1/10
- **DOI / URL:** Confirmada vía página índice: https://users.ssc.wisc.edu/~mchinn/CCG-P_JIMF.pdf (bibliografía de Cheung, Chinn y Garcia Pascual 2005)
- **Acceso y licencia:** De pago (University of Chicago Press)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Cheung Chinn Garcia Pascual "Empirical exchange rate models of the nineties: Are any fit to survive?" "Exchange rate prediction redux"»; WebFetch: sí, de la página índice; no de la obra)
- **Contenido:** Muestra que, en modelos de valor presente, si los fundamentos son I(1) y el factor de descuento es cercano a uno, el tipo de cambio se comporta casi como un paseo aleatorio aunque esté determinado por fundamentos; los tipos de cambio ayudan a predecir los fundamentos y no al revés.
- **Uso en el bloque:** PROS y CONTRA: explicación teórica de por qué batir al paseo aleatorio es difícil sin negar el papel de los fundamentos.
- **Limitaciones:** Contenido descrito según conocimiento de la obra; resumen no leído en esta carga.

#### ANA-DOC-0231 · Q 87 (A) — Tests of Equal Forecast Accuracy and Encompassing for Nested Models

- **Autores:** Todd E. Clark; Michael W. McCracken
- **Año:** 2001
- **Publicación o institución:** Journal of Econometrics, vol. 105, págs. 85-110
- **Tipo de documento:** Artículo revisado por pares (método)
- **Temática:** TX-13 Previsión de tipos de cambio y su evaluación (principal) · secundarias: —
- **Calidad Q:** 87 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 8/10 · Impacto 8/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** Confirmada vía página índice: https://www.nber.org/papers/w18391.pdf (bibliografía de Diebold, NBER WP 18391)
- **Acceso y licencia:** Texto editorial por suscripción; sin copia abierta verificada en esta carga · Licencia: copyright del editor
- **Versión:** Publicada (metadatos según la página índice)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Diebold Mariano 1995 "Comparing Predictive Accuracy" Journal of Business & Economic Statistics»; WebFetch: sí, de la página índice; no de la obra) · reutilizada del F7 V3.2 (TA-04)
- **Contenido:** Deriva la distribución de las pruebas de igual precisión y de inclusión (encompassing) cuando los modelos comparados están anidados.
- **Uso en el bloque:** EVAL: contraste de modelos anidados (señal frente a paseo aleatorio, que es su caso particular).
- **Estatus epistémico:** Método revisado por pares; nivel alto.
- **Limitaciones:** Valores críticos no estándar; técnico.
- **Disciplinas y etiquetas:** Econometría de la previsión · modelos-anidados; encompassing

#### ANA-DOC-0237 · Q 86 (A) — Forecast Evaluation

- **Autores:** Kenneth D. West
- **Año:** 2006
- **Publicación o institución:** Handbook of Economic Forecasting, vol. 1 (eds. G. Elliott, C. W. J. Granger y A. Timmermann), Elsevier / North-Holland
- **Tipo de documento:** Capítulo de manual de referencia (survey)
- **Temática:** TX-13 Previsión de tipos de cambio y su evaluación (principal) · secundarias: —
- **Calidad Q:** 86 (A) — Tipo 22/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 8/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** Confirmada vía página índice: https://econpapers.repec.org/bookchap/eeeecofor/1.htm (índice del Handbook en EconPapers/RePEc)
- **Acceso y licencia:** Texto editorial por suscripción; sin copia abierta verificada en esta carga · Licencia: copyright del editor
- **Versión:** Publicada (metadatos según la página índice)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Handbook of Economic Forecasting Volume 1 2006 Elliott Granger Timmermann chapters "Forecast Combinations" "Forecast Evaluation"»; WebFetch: sí, de la página índice; no de la obra) · reutilizada del F7 V3.2 (TA-04)
- **Contenido:** Revisión de los métodos de evaluación de pronósticos: funciones de pérdida, pruebas de precisión e inferencia con parámetros estimados.
- **Uso en el bloque:** EVAL: panorama de métodos de evaluación aplicables a F4 (puntuales, de intervalo y de densidad).
- **Estatus epistémico:** Capítulo de manual de referencia del campo; nivel alto.
- **Limitaciones:** Estado del arte a 2006; el vol. 2 (2013) actualiza parte de los temas.
- **Disciplinas y etiquetas:** Econometría de la previsión · handbook; evaluacion; funciones-de-perdida

#### FXA-0483 · Q 86 (A) — Exchange rates and fundamentals: evidence on long horizon predictability

- **Autores:** Nelson C. Mark
- **Año:** 1995
- **Publicación o institución:** American Economic Review, vol. 85, págs. 201-218
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-13 Previsión de tipos de cambio y su evaluación (principal) · secundarias: TX-03
- **Calidad Q:** 86 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 7/10 · Impacto 10/10 · Independencia 10/10 · Acceso 4/10
- **DOI / URL:** Confirmada vía página índice: https://users.ssc.wisc.edu/~mchinn/CCG-P_JIMF.pdf (bibliografía de Cheung, Chinn y Garcia Pascual 2005)
- **Acceso y licencia:** De pago (AEA/JSTOR)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Cheung Chinn Garcia Pascual "Empirical exchange rate models of the nineties: Are any fit to survive?" "Exchange rate prediction redux"»; WebFetch: sí, de la página índice; no de la obra)
- **Contenido:** Encuentra que la desviación del tipo de cambio respecto a fundamentos monetarios predice su variación a horizontes largos (hasta 16 trimestres), con predictibilidad creciente con el horizonte.
- **Uso en el bloque:** PROS (horizontes H3-H4): base de la predictibilidad de largo plazo por fundamentos; EVAL: cautela con la inferencia en regresiones de horizonte largo.
- **Limitaciones:** Resultados discutidos por Kilian (1999) y otros por problemas de inferencia con horizontes solapados; contenido descrito según conocimiento de la obra.

#### FXA-0484 · Q 85 (A) — Why is it so difficult to beat the random walk forecast of exchange rates?

- **Autores:** Lutz Kilian; Mark P. Taylor
- **Año:** 2003
- **Publicación o institución:** Journal of International Economics, vol. 60, n.º 1, págs. 85-107
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-13 Previsión de tipos de cambio y su evaluación (principal) · secundarias: TX-03
- **Calidad Q:** 85 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 8/10 · Impacto 9/10 · Independencia 10/10 · Acceso 2/10
- **DOI / URL:** Confirmada vía páginas índice: https://www.nber.org/papers/w23267.pdf y https://users.ssc.wisc.edu/~mchinn/CCG-P_JIMF.pdf (bibliografías)
- **Acceso y licencia:** De pago (Elsevier)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Exchange rate prediction redux: New models, new data, new currencies" Cheung Chinn Garcia Pascual Zhang 2019»; WebFetch: sí, de la página índice; no de la obra)
- **Contenido:** Atribuye la dificultad de batir al paseo aleatorio a la reversión no lineal (ESTAR) hacia los fundamentos: cerca del equilibrio el tipo de cambio parece un paseo aleatorio y solo con grandes desalineamientos y horizontes de 2-3 años aparece predictibilidad.
- **Uso en el bloque:** PROS y AS-ESTR (valor): justificar que las señales de valoración solo funcionan con desalineamientos grandes y horizontes largos.
- **Limitaciones:** Contenido descrito según conocimiento de la obra; resumen no leído.

#### ANA-DOC-0240 · Q 84 (A) — Survey Expectations

- **Autores:** M. Hashem Pesaran; Martin Weale
- **Año:** 2006
- **Publicación o institución:** Handbook of Economic Forecasting, vol. 1 (eds. G. Elliott, C. W. J. Granger y A. Timmermann), Elsevier / North-Holland
- **Tipo de documento:** Capítulo de manual de referencia (survey)
- **Temática:** TX-13 Previsión de tipos de cambio y su evaluación (principal) · secundarias: —
- **Calidad Q:** 84 (A) — Tipo 22/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 7/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** Confirmada vía página índice: https://econpapers.repec.org/bookchap/eeeecofor/1.htm (índice del Handbook en EconPapers/RePEc)
- **Acceso y licencia:** Texto editorial por suscripción; sin copia abierta verificada en esta carga · Licencia: copyright del editor
- **Versión:** Publicada (metadatos según la página índice)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Handbook of Economic Forecasting Volume 1 2006 Elliott Granger Timmermann chapters "Forecast Combinations" "Forecast Evaluation"»; WebFetch: sí, de la página índice; no de la obra) · reutilizada del F7 V3.2 (TA-04)
- **Contenido:** Revisión del uso de encuestas de expectativas en economía: medición, formación de expectativas y valor predictivo.
- **Uso en el bloque:** PROS y TR-PFV: uso de encuestas de expectativas cambiarias (consenso de analistas) como referencia y sus sesgos.
- **Estatus epistémico:** Capítulo de manual de referencia del campo; nivel alto.
- **Limitaciones:** Estado del arte a 2006; el vol. 2 (2013) actualiza parte de los temas.
- **Disciplinas y etiquetas:** Econometría de la previsión · handbook; encuestas; expectativas

#### FXA-0486 · Q 84 (A) — Using Out-of-sample Mean Squared Prediction Errors to Test the Martingale Difference Hypothesis

- **Autores:** Todd E. Clark; Kenneth D. West
- **Año:** 2006
- **Publicación o institución:** Journal of Econometrics, vol. 135, n.º 1-2, págs. 155-186
- **Tipo de documento:** Artículo revisado por pares (método)
- **Temática:** TX-13 Previsión de tipos de cambio y su evaluación (principal) · secundarias: —
- **Calidad Q:** 84 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 8/10 · Independencia 10/10 · Acceso 0/10
- **DOI / URL:** Confirmada vía página índice: https://www.nber.org/papers/w23267.pdf (bibliografía de Cheung, Chinn, Garcia Pascual y Zhang)
- **Acceso y licencia:** De pago (Elsevier)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Exchange rate prediction redux: New models, new data, new currencies" Cheung Chinn Garcia Pascual Zhang 2019»; WebFetch: sí, de la página índice; no de la obra)
- **Contenido:** Propone ajustar el ECM del modelo alternativo por el ruido de estimación al compararlo con la martingala (paseo aleatorio), corrigiendo el sesgo contra el modelo anidado; aplicado a tipos de cambio, es la prueba estándar en la literatura posterior (p. ej., Molodtsova y Papell).
- **Uso en el bloque:** EVAL y PROS: contraste correcto de una señal cambiaria frente al paseo aleatorio (modelos anidados). En F8 figura además la versión de 2007 para modelos anidados generales.
- **Limitaciones:** Contenido descrito según conocimiento de la obra; resumen no leído.

#### FXA-0485 · Q 82 (A) — Exchange rate forecasting: the errors we've really made

- **Autores:** Jon Faust; John H. Rogers; Jonathan H. Wright
- **Año:** 2003
- **Publicación o institución:** Journal of International Economics, vol. 60, págs. 35-60
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-13 Previsión de tipos de cambio y su evaluación (principal) · secundarias: —
- **Calidad Q:** 82 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 14/15 · Vigencia 8/10 · Impacto 6/10 · Independencia 10/10 · Acceso 2/10
- **DOI / URL:** Confirmada vía página índice: https://users.ssc.wisc.edu/~mchinn/CCG-P_JIMF.pdf (bibliografía de Cheung, Chinn y Garcia Pascual 2005)
- **Acceso y licencia:** De pago (Elsevier)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Cheung Chinn Garcia Pascual "Empirical exchange rate models of the nineties: Are any fit to survive?" "Exchange rate prediction redux"»; WebFetch: sí, de la página índice; no de la obra)
- **Contenido:** Repite ejercicios de previsión cambiaria con datos macroeconómicos en tiempo real (las vintages disponibles en cada momento) y muestra que los resultados cambian respecto a usar datos revisados.
- **Uso en el bloque:** EVAL y MOTOR: exigir datos en tiempo real para evaluar señales fundamentales y evitar sesgo de anticipación.
- **Limitaciones:** Contenido descrito según conocimiento de la obra; resumen no leído en esta carga.

#### FXA-0492 · Q 80 (A) — Taylor Rules and the Deutschmark–Dollar Real Exchange Rates

- **Autores:** Charles Engel; Kenneth D. West
- **Año:** 2006
- **Publicación o institución:** Journal of Money, Credit and Banking, vol. 38, págs. 1175-1194
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-13 Previsión de tipos de cambio y su evaluación (principal) · secundarias: TX-02
- **Calidad Q:** 80 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 7/10 · Impacto 6/10 · Independencia 10/10 · Acceso 1/10
- **DOI / URL:** Confirmada vía página índice: https://www.uh.edu/~dpapell/Taylor%20Rule%20Fundamentals.pdf (bibliografía de Molodtsova y Papell)
- **Acceso y licencia:** De pago (Wiley)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Molodtsova Papell 2009 "Out-of-sample exchange rate predictability with Taylor rule fundamentals" Journal of International Economics»; WebFetch: sí, de la página índice; no de la obra)
- **Contenido:** Construye un tipo de cambio real «modelo» como valor presente de diferenciales de tipos implícitos en reglas de Taylor y lo compara con el tipo real DEM/USD (según el título y su papel en la literatura).
- **Uso en el bloque:** TR-BCM: traducir sendas de política monetaria esperadas en un tipo de cambio real teórico.
- **Limitaciones:** Un solo par; resumen no leído.

#### FXA-0491 · Q 78 (B) — The Continuing Puzzle of Short Horizon Exchange Rate Forecasting

- **Autores:** Kenneth Rogoff; Vania Stavrakeva
- **Año:** 2008
- **Publicación o institución:** NBER Working Paper 14071
- **Tipo de documento:** Documento de trabajo
- **Temática:** TX-13 Previsión de tipos de cambio y su evaluación (principal) · secundarias: —
- **Calidad Q:** 78 (B) — Tipo 20/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 7/10 · Independencia 10/10 · Acceso 2/10
- **DOI / URL:** Confirmada vía página índice: https://www.uh.edu/~dpapell/Taylor%20Rule%20Fundamentals.pdf (bibliografía de Molodtsova y Papell)
- **Acceso y licencia:** NBER (acceso según suscripción)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Molodtsova Papell 2009 "Out-of-sample exchange rate predictability with Taylor rule fundamentals" Journal of International Economics»; WebFetch: sí, de la página índice; no de la obra)
- **Contenido:** Revisión crítica de los éxitos predictivos recientes (reglas de Taylor, factores, panel): muestra que muchos no son robustos a periodos de evaluación alternativos y que el uso de la prueba de Clark-West puede sobrestimar la mejora práctica sobre el paseo aleatorio.
- **Uso en el bloque:** CONTRA y EVAL: control de robustez temporal de cualquier señal cambiaria antes de certificar un horizonte.
- **Limitaciones:** Contenido descrito según conocimiento de la obra; resumen no leído.

#### FXA-0493 · Q 78 (B) — Testing Long-Horizon Predictive Ability with High Persistence, and the Meese-Rogoff Puzzle

- **Autores:** Barbara Rossi
- **Año:** 2005
- **Publicación o institución:** International Economic Review, vol. 46, págs. 61-92
- **Tipo de documento:** Artículo revisado por pares (método)
- **Temática:** TX-13 Previsión de tipos de cambio y su evaluación (principal) · secundarias: —
- **Calidad Q:** 78 (B) — Tipo 25/25 · Rigor 17/20 · Autoridad 13/15 · Vigencia 7/10 · Impacto 5/10 · Independencia 10/10 · Acceso 1/10
- **DOI / URL:** Confirmada vía página índice: https://www.uh.edu/~dpapell/Taylor%20Rule%20Fundamentals.pdf (bibliografía de Molodtsova y Papell)
- **Acceso y licencia:** De pago (Wiley)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Molodtsova Papell 2009 "Out-of-sample exchange rate predictability with Taylor rule fundamentals" Journal of International Economics»; WebFetch: sí, de la página índice; no de la obra)
- **Contenido:** Propone contrastes de capacidad predictiva a horizonte largo válidos con regresores muy persistentes y los aplica al enigma de Meese-Rogoff (según el título).
- **Uso en el bloque:** EVAL: inferencia correcta en pronósticos cambiarios a horizontes H3-H4 con fundamentos persistentes.
- **Limitaciones:** Resumen no leído en esta carga.

#### FXA-0488 · Q 78 (B) — The Out-of-Sample Failure of Exchange Rate Models: Sampling Error or Misspecification?

- **Autores:** Richard Meese; Kenneth Rogoff
- **Año:** 1983
- **Publicación o institución:** En J. Frankel (ed.), Exchange Rates and International Macroeconomics, University of Chicago Press (NBER), págs. 67-105
- **Tipo de documento:** Capítulo de libro de conferencia NBER
- **Temática:** TX-13 Previsión de tipos de cambio y su evaluación (principal) · secundarias: —
- **Calidad Q:** 78 (B) — Tipo 20/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 6/10 · Impacto 8/10 · Independencia 10/10 · Acceso 4/10
- **DOI / URL:** Confirmada vía página índice: https://www.nber.org/papers/w23267.pdf (bibliografía de Cheung, Chinn, Garcia Pascual y Zhang)
- **Acceso y licencia:** Capítulo NBER (acceso según disponibilidad)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"Exchange rate prediction redux: New models, new data, new currencies" Cheung Chinn Garcia Pascual Zhang 2019»; WebFetch: sí, de la página índice; no de la obra)
- **Contenido:** Complemento del artículo de 1983 en el JIE: examina si el fracaso fuera de muestra de los modelos estructurales se debe a error muestral en la estimación de parámetros o a mala especificación (según el título).
- **Uso en el bloque:** PROS y CONTRA: diagnóstico de las causas del fracaso predictivo antes de descartar un modelo.
- **Limitaciones:** Resumen no leído; complementario de la obra principal de Meese y Rogoff.

#### FXA-0494 · Q 76 (B) — The Taylor Rule and Interval Forecast for Exchange Rates

- **Autores:** Jian Wang; Jason J. Wu
- **Año:** 2009
- **Publicación o institución:** Board of Governors of the Federal Reserve System, International Finance Discussion Papers n.º 963
- **Tipo de documento:** Documento de trabajo
- **Temática:** TX-13 Previsión de tipos de cambio y su evaluación (principal) · secundarias: TX-02
- **Calidad Q:** 76 (B) — Tipo 20/25 · Rigor 16/20 · Autoridad 12/15 · Vigencia 8/10 · Impacto 4/10 · Independencia 9/10 · Acceso 7/10
- **DOI / URL:** https://www.federalreserve.gov/pubs/ifdp/2009/963/ifdp963.htm
- **Acceso y licencia:** Acceso abierto (Reserva Federal)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Molodtsova Papell 2009 "Out-of-sample exchange rate predictability with Taylor rule fundamentals" Journal of International Economics»; WebFetch: sí)
- **Contenido:** Evalúa previsiones por intervalos (semiparamétricas robustas) de modelos de regla de Taylor para 12 divisas OCDE frente al USD: con la misma cobertura que el paseo aleatorio, producen intervalos más estrechos, sobre todo a horizontes largos; los fundamentos ayudan a prever la distribución del tipo de cambio.
- **Uso en el bloque:** PROS y EVAL: evaluar pronósticos de intervalo (no solo puntuales) en F4; criterio de cobertura y amplitud.
- **Limitaciones:** Documento de trabajo; muestra hasta 2007 aprox.

## TX-14 Geopolítica, sanciones, política y divisas

#### ANA-DOC-0247 · Q 96 (A) — Measuring Economic Policy Uncertainty

- **Autores:** Scott R. Baker; Nicholas Bloom; Steven J. Davis
- **Año:** 2016 (NBER WP 21633, 2015)
- **Publicación o institución:** Quarterly Journal of Economics, vol. 131, n.º 4, págs. 1593-1636 · NBER Working Paper 21633
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-14 Geopolítica, sanciones, política y divisas (principal) · secundarias: TX-13
- **Calidad Q:** 96 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 9/10
- **DOI / URL:** DOI (NBER): 10.3386/w21633 · https://nber.org/papers/w21633
- **Acceso y licencia:** Versión de trabajo en NBER; índices públicos en policyuncertainty.com · Licencia: copyright de los autores / OUP
- **Versión:** Publicada; coexiste la versión NBER
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Baker Bloom Davis "Measuring Economic Policy Uncertainty" Quarterly Journal of Economics 2016»; WebFetch: sí) · reutilizada del F7 V3.2 (TA-04)
- **Contenido:** Construye el índice de incertidumbre de política económica (EPU) a partir de la cobertura de prensa y muestra su asociación con mayor volatilidad y menor inversión y empleo.
- **Uso en el bloque:** TR-BCM y TR-PFV: índice EPU como medida de incertidumbre de política económica por país, insumo para primas de riesgo cambiarias.
- **Estatus epistémico:** Evidencia empírica revisada por pares, muy citada; nivel alto.
- **Limitaciones:** Medida basada en texto de prensa; sensibilidad a la selección de periódicos.
- **Disciplinas y etiquetas:** Incertidumbre · epu; indice-de-prensa; incertidumbre-politica

#### ANA-DOC-0547 · Q 93 (A) — Measuring Geopolitical Risk

- **Autores:** Dario Caldara; Matteo Iacoviello
- **Año:** 2022 (Fed IFDP 1222, 2018, rev. 2022)
- **Publicación o institución:** American Economic Review, 112(4), 1194–1225
- **Tipo de documento:** Artículo revisado por pares con índice de datos público
- **Temática:** TX-14 Geopolítica, sanciones, política y divisas (principal) · secundarias: TX-12
- **Calidad Q:** 93 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 10/10 · Independencia 9/10 · Acceso 6/10
- **DOI / URL:** DOI: 10.1257/aer.20191823 · URL de acceso: https://matteoiacoviello.com/gpr.htm
- **Acceso y licencia:** Peldaño 1 (artículo, apéndice y datos del índice GPR en la web del autor; licencia CC BY para los materiales de la página)
- **Versión:** Versión publicada; índice mensual y diario actualizado (última actualización vista: 26/10/2026)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Caldara Iacoviello Measuring Geopolitical Risk American Economic Review 2022»; WebFetch: sí) · reutilizada del F7 V3.2 (TA-15)
- **Contenido:** Índice de riesgo geopolítico (GPR) basado en la proporción de artículos de prensa sobre tensiones adversas (desde 1900 y desde 1985; 44 países; subíndices de amenazas y actos); un GPR alto se asocia con menor inversión, bolsa y empleo y mayor probabilidad de desastres.
- **Uso en el bloque:** TR-BCM, TR-PFV y AS-EMEA: índice GPR como variable de riesgo geopolítico para divisas refugio y emergentes (véanse FXA-0470 a FXA-0472).
- **Estatus epistémico:** Medida de referencia revisada por pares, con datos abiertos
- **Limitaciones:** Basado en prensa anglosajona; mide atención mediática, no el riesgo objetivo.

#### FXA-0465 · Q 91 (A) — Sanctions and the Exchange Rate

- **Autores:** Oleg Itskhoki; Dmitry Mukhin
- **Año:** 2025
- **Publicación o institución:** The Review of Economic Studies (publicado en línea el 14 de septiembre de 2025) · versión de trabajo: NBER WP 30009 (2022)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-14 Geopolítica, sanciones, política y divisas (principal) · secundarias: TX-08, TX-10
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 19/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 6/10 · Independencia 10/10 · Acceso 6/10
- **DOI / URL:** DOI: 10.1093/restud/rdaf085 · https://www.restud.com/sanctions-and-the-exchange-rate/ · versión del autor: https://itskhoki.com/papers/sanctionsER.pdf
- **Acceso y licencia:** Artículo de pago (Oxford University Press); versión de autor y NBER
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Itskhoki Mukhin "Sanctions and the Exchange Rate" ruble NBER»; WebFetch: sí, página de la revista)
- **Contenido:** Las sanciones que restringen las exportaciones o congelan activos exteriores deprecian la divisa del país sancionado, mientras que las restricciones a las importaciones la aprecian, aunque tengan efectos reales equivalentes; el ahorro precautorio en divisas presiona a la baja salvo que se compense con ventas de reservas o controles; el modelo replica la trayectoria del rublo tras febrero de 2022.
- **Uso en el bloque:** AS-EMEA y CONTRA: interpretar correctamente la apreciación de una divisa sancionada (no implica que las sanciones fallen); PROS: escenarios por tipo de sanción.
- **Limitaciones:** Calibrado al caso ruso; el tipo de cambio observado con controles de capital no es libremente negociable.

#### ANA-DOC-0548 · Q 91 (A) — Uncertainty about Government Policy and Stock Prices

- **Autores:** Ľuboš Pástor; Pietro Veronesi
- **Año:** 2012
- **Publicación o institución:** The Journal of Finance, 67(4), 1219–1264
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-14 Geopolítica, sanciones, política y divisas (principal) · secundarias: —
- **Calidad Q:** 91 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 4/10
- **DOI / URL:** URL de acceso: https://econpapers.repec.org/RAS/ppa276.htm (perfil EconPapers de Ľ. Pástor)
- **Acceso y licencia:** Peldaño 3 (revista; versión NBER abierta)
- **Versión:** Versión publicada identificada en el perfil del autor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Lubos Pastor RePEc author profile Political uncertainty»; WebFetch: sí, perfiles) · reutilizada del F7 V3.2 (TA-15)
- **Contenido:** Modelo de equilibrio general: las acciones caen al anunciarse cambios de política (más si la incertidumbre es alta) y la volatilidad y correlaciones aumentan tras ellos.
- **Uso en el bloque:** TR-BCM: canal de la incertidumbre sobre política gubernamental a primas de riesgo, extrapolable a divisas.
- **Estatus epistémico:** Teoría de referencia muy citada
- **Limitaciones:** DOI no visto; modelo estilizado.

#### ANA-DOC-0549 · Q 90 (A) — Populist Leaders and the Economy

- **Autores:** Manuel Funke; Moritz Schularick; Christoph Trebesch
- **Año:** 2023
- **Publicación o institución:** American Economic Review, 113(12), 3249–3288
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-14 Geopolítica, sanciones, política y divisas (principal) · secundarias: TX-10
- **Calidad Q:** 90 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** DOI: 10.1257/aer.20202045 · URL de acceso: https://www.scripts-berlin.eu/publications/Publications/Trebesch-et-al_American-Economic-Review_Populst-Leaders-and-Economy/index.html
- **Acceso y licencia:** Peldaño 2 (ficha del clúster SCRIPTS; versiones de trabajo abiertas en Kiel/CEPR)
- **Versión:** Versión publicada identificada
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Christoph Trebesch Populist Leaders and the Economy China's Overseas Lending»; WebFetch: sí) · reutilizada del F7 V3.2 (TA-15)
- **Contenido:** Base de 51 líderes populistas (1900–2020): el PIB per cápita es ≈10 % menor a 15 años frente al contrafactual; más desintegración económica, inestabilidad macro y deterioro institucional.
- **Uso en el bloque:** AS-EMLA y AS-EMEA: coste económico del populismo como factor de riesgo de largo plazo de una divisa.
- **Estatus epistémico:** Evidencia histórica revisada por pares
- **Limitaciones:** Clasificación de populismo discutible; contrafactual sintético.

#### ANA-DOC-0550 · Q 89 (A) — The Price of Political Uncertainty: Theory and Evidence from the Option Market

- **Autores:** Bryan Kelly; Ľuboš Pástor; Pietro Veronesi
- **Año:** 2016
- **Publicación o institución:** The Journal of Finance, 71(5), 2417–2480
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-14 Geopolítica, sanciones, política y divisas (principal) · secundarias: —
- **Calidad Q:** 89 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 3/10
- **DOI / URL:** URL de acceso: https://econpapers.repec.org/RAS/ppa276.htm (perfil EconPapers de Ľ. Pástor)
- **Acceso y licencia:** Peldaño 3 (revista; versión NBER abierta)
- **Versión:** Versión publicada identificada en el perfil del autor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Lubos Pastor RePEc author profile Political uncertainty»; WebFetch: sí, perfiles) · reutilizada del F7 V3.2 (TA-15)
- **Contenido:** Las opciones cuyo vencimiento abarca elecciones nacionales y cumbres internacionales son más caras, lo que revela que la incertidumbre política se valora en el mercado, más en economías débiles.
- **Uso en el bloque:** TR-PFV: la incertidumbre política se descuenta en las opciones; analogía para la volatilidad implícita cambiaria en elecciones.
- **Estatus epistémico:** Evidencia empírica y teórica revisada por pares
- **Limitaciones:** DOI no visto.

#### ANA-DOC-0551 · Q 88 (A) — China's overseas lending

- **Autores:** Sebastian Horn; Carmen M. Reinhart; Christoph Trebesch
- **Año:** 2021
- **Publicación o institución:** Journal of International Economics, 133, 103539
- **Tipo de documento:** Artículo revisado por pares con base de datos
- **Temática:** TX-14 Geopolítica, sanciones, política y divisas (principal) · secundarias: TX-12
- **Calidad Q:** 88 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 9/10 · Independencia 10/10 · Acceso 3/10
- **DOI / URL:** DOI: 10.1016/j.jinteco.2021.103539 · URL de acceso: https://www.scripts-berlin.eu/publications/Publications/Trebesch-et-al_Journal-of-International-Economics_China_s-Overseas-Lending/index.html
- **Acceso y licencia:** Peldaño 2 (ficha SCRIPTS; documento de trabajo abierto)
- **Versión:** Versión publicada identificada
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Christoph Trebesch China's Overseas Lending»; WebFetch: sí) · reutilizada del F7 V3.2 (TA-15)
- **Contenido:** Base de ≈4.900 préstamos y donaciones oficiales chinas a 146 países (1949–2017): China supera al Banco Mundial y al FMI como prestamista oficial y en torno a la mitad de su crédito no figura en las estadísticas de deuda.
- **Uso en el bloque:** AS-EMAS y AS-EMEA: préstamos exteriores de China como canal de influencia y de riesgo para divisas de países deudores.
- **Estatus epistémico:** Evidencia empírica revisada por pares; nivel alto
- **Limitaciones:** Datos hasta 2017; actualización en JEP 2025 (Horn, Reinhart y Trebesch).

#### FXA-0460 · Q 86 (A) — Mars or Mercury? The geopolitics of international currency choice

- **Autores:** Barry Eichengreen; Arnaud Mehl; Livia Chițu
- **Año:** 2019
- **Publicación o institución:** Economic Policy, vol. 34, n.º 98, págs. 315-363 (versión de trabajo NBER WP 24145, 2017)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-14 Geopolítica, sanciones, política y divisas (principal) · secundarias: TX-12
- **Calidad Q:** 86 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 7/10 · Independencia 9/10 · Acceso 4/10
- **DOI / URL:** Confirmada vía página índice: https://ideas.repec.org/e/pei2.html (página de autor de Eichengreen en IDEAS)
- **Acceso y licencia:** Artículo de pago (Oxford University Press); versión de trabajo NBER
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Arslanalp Eichengreen Simpson-Bell "The Stealth Erosion of Dollar Dominance" IMF working paper COFER»; WebFetch: sí, de la página índice; no de la obra)
- **Contenido:** Contrasta la visión «Marte» (alianzas militares y seguridad determinan la moneda de reserva) frente a la «Mercurio» (comercio y finanzas): con datos históricos de reservas, las alianzas aumentan significativamente la cuota de la moneda del aliado; estima la caída de la cuota del dólar si EE. UU. se retirara de sus alianzas.
- **Uso en el bloque:** TR-BCM y AS-ESTR: canal geopolítico de la demanda de dólares y euros; PROS: escenarios de ruptura de alianzas.
- **Limitaciones:** Contenido descrito según conocimiento de la obra; datos históricos con muestras parciales.

#### ANA-DOC-0552 · Q 86 (A) — Going to extremes: Politics after financial crises, 1870–2014

- **Autores:** Manuel Funke; Moritz Schularick; Christoph Trebesch
- **Año:** 2016
- **Publicación o institución:** European Economic Review, 88, 227–260
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-14 Geopolítica, sanciones, política y divisas (principal) · secundarias: TX-09
- **Calidad Q:** 86 (A) — Tipo 24/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 10/10 · Independencia 10/10 · Acceso 3/10
- **DOI / URL:** URL de acceso: https://authors.repec.org/pro/psc129 (perfil RePEc de M. Schularick)
- **Acceso y licencia:** Peldaño 3 (revista; versiones de trabajo abiertas)
- **Versión:** Versión publicada identificada en los perfiles de Schularick y Trebesch
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Moritz Schularick IDEAS RePEc author profile» y «Christoph Trebesch RePEc author profile»; WebFetch: sí, perfiles) · reutilizada del F7 V3.2 (TA-15)
- **Contenido:** Tras las crisis financieras sistémicas aumenta el voto a la extrema derecha, se fragmentan los parlamentos y se debilitan los gobiernos (20 democracias, 1870–2014).
- **Uso en el bloque:** AS-EMLA/AS-EMEA y PROS: la polarización política tras crisis financieras como riesgo para la divisa.
- **Estatus epistémico:** Evidencia histórica revisada por pares
- **Limitaciones:** DOI no visto; muestra de democracias avanzadas.

#### FXA-0461 · Q 85 (A) — Sanctions and the exchange rate in time

- **Autores:** Barry Eichengreen; Massimo Ferrari Minesso; Arnaud Mehl; Isabel Vansteenkiste; Roland Vicquéry
- **Año:** 2024
- **Publicación o institución:** Economic Policy, vol. 39, n.º 118, págs. 323-354 (versión de trabajo CEPR DP 17641, 2022)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-14 Geopolítica, sanciones, política y divisas (principal) · secundarias: TX-09
- **Calidad Q:** 85 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 5/10 · Independencia 9/10 · Acceso 4/10
- **DOI / URL:** Confirmada vía página índice: https://ideas.repec.org/e/pei2.html
- **Acceso y licencia:** Artículo de pago; versión CEPR
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Arslanalp Eichengreen Simpson-Bell "The Stealth Erosion of Dollar Dominance" IMF working paper COFER»; WebFetch: sí, de la página índice; no de la obra)
- **Contenido:** Estudia el efecto de las sanciones sobre el tipo de cambio del país sancionado a lo largo del tiempo, con evidencia histórica de largo plazo (según el título y la serie).
- **Uso en el bloque:** AS-EMEA (RUB, TRY, divisas de Oriente Medio) y CONTRA: trayectoria típica de una divisa tras sanciones; riesgo de evento.
- **Limitaciones:** Resumen no leído en esta carga.

#### ANA-DOC-0554 · Q 85 (A) — Political Uncertainty and Risk Premia

- **Autores:** Ľuboš Pástor; Pietro Veronesi
- **Año:** 2013
- **Publicación o institución:** Journal of Financial Economics, 110(3), 520–545
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-14 Geopolítica, sanciones, política y divisas (principal) · secundarias: —
- **Calidad Q:** 85 (A) — Tipo 25/25 · Rigor 17/20 · Autoridad 15/15 · Vigencia 8/10 · Impacto 9/10 · Independencia 10/10 · Acceso 1/10
- **DOI / URL:** URL de acceso: https://econpapers.repec.org/RAS/ppa276.htm (perfil EconPapers de Ľ. Pástor)
- **Acceso y licencia:** Peldaño 3 (revista)
- **Versión:** Versión publicada identificada en el perfil del autor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Lubos Pastor RePEc author profile Political uncertainty»; WebFetch: sí, perfiles) · reutilizada del F7 V3.2 (TA-15)
- **Contenido:** La incertidumbre política exige una prima de riesgo, mayor cuando la economía es débil, y eleva volatilidad y correlaciones de las acciones.
- **Uso en el bloque:** TR-BCM y CONTRA: prima de riesgo por incertidumbre política, aplicable a divisas en periodos electorales.
- **Estatus epistémico:** Teoría con contraste empírico revisada por pares
- **Limitaciones:** DOI no visto; complementa ANA-DOC-0548.

#### FXA-0462 · Q 84 (A) — A Framework for Geoeconomics

- **Autores:** Christopher Clayton; Matteo Maggiori; Jesse Schreger
- **Año:** 2026
- **Publicación o institución:** Econometrica, vol. 94, n.º 1, págs. 105-136
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-14 Geopolítica, sanciones, política y divisas (principal) · secundarias: TX-12
- **Calidad Q:** 84 (A) — Tipo 25/25 · Rigor 18/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 2/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** Confirmada vía página índice: https://authors.repec.org/pro/pma2176 (perfil RePEc de Maggiori)
- **Acceso y licencia:** De pago (Econometric Society); versiones de trabajo previas
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Matteo Maggiori IDEAS RePEc "A Model of the International Monetary System" Farhi "International Currencies and Capital Allocation"»; WebFetch: sí, de la página índice; no de la obra)
- **Contenido:** Marco teórico del poder geoeconómico: cómo un hegemón usa amenazas sobre relaciones financieras y comerciales (incluida la provisión de su moneda y su sistema financiero) para influir en otros países (según el título y la línea de investigación de los autores).
- **Uso en el bloque:** TR-BCM, AS-ESTR y CONTRA: marco para evaluar el riesgo de uso coercitivo del dólar y sus efectos en la demanda de divisas.
- **Limitaciones:** Resumen no leído; teórico.

#### ANA-DOC-0556 · Q 84 (A) — The Costs of Economic Nationalism: Evidence from the Brexit Experiment

- **Autores:** Benjamin Born; Gernot J. Müller; Moritz Schularick; Petr Sedláček
- **Año:** 2019
- **Publicación o institución:** The Economic Journal, 129(623), 2722–2744
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-14 Geopolítica, sanciones, política y divisas (principal) · secundarias: TX-12
- **Calidad Q:** 84 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 7/10 · Independencia 10/10 · Acceso 3/10
- **DOI / URL:** URL de acceso: https://authors.repec.org/pro/psc129 (perfil RePEc de M. Schularick)
- **Acceso y licencia:** Peldaño 3 (revista; versiones de trabajo abiertas)
- **Versión:** Versión publicada identificada en el perfil del autor
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Moritz Schularick IDEAS RePEc author profile»; WebFetch: sí, perfil) · reutilizada del F7 V3.2 (TA-15)
- **Contenido:** Con un control sintético, estima la pérdida de producción del Reino Unido atribuible al voto del Brexit (en torno al 2 % del PIB a finales de 2018).
- **Uso en el bloque:** AS-G10N (GBP): caso de estudio del coste económico de una ruptura política (Brexit) con impacto cambiario duradero.
- **Estatus epistémico:** Evidencia cuasi-experimental revisada por pares
- **Limitaciones:** DOI no visto; cifra de impacto según conocimiento de la obra (comprobar); horizonte corto.

#### FXA-0473 · Q 84 (A) — Politics and Exchange Rate Forecasts

- **Autores:** S. Brock Blomberg; Gregory D. Hess
- **Año:** 1997
- **Publicación o institución:** Journal of International Economics, vol. 43, n.º 1-2, págs. 189-205
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-14 Geopolítica, sanciones, política y divisas (principal) · secundarias: TX-13
- **Calidad Q:** 84 (A) — Tipo 25/25 · Rigor 15/20 · Autoridad 12/15 · Vigencia 7/10 · Impacto 7/10 · Independencia 10/10 · Acceso 8/10
- **DOI / URL:** DOI: 10.1016/S0022-1996(96)01466-3 · https://scholarship.claremont.edu/cmc_fac_pub/181
- **Acceso y licencia:** Repositorio institucional de Claremont (acceso a la ficha y texto según disponibilidad)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Blomberg Hess "Politics and exchange rate forecasts" Journal of International Economics elections currency»; WebFetch: sí)
- **Contenido:** Añade a los modelos cambiarios variables políticas (partido en el poder, elecciones, características de los candidatos) y obtiene previsiones que baten al paseo aleatorio a 1-12 meses para GBP/USD, DEM/USD, GBP/DEM y tipos efectivos.
- **Uso en el bloque:** TR-BCM y PROS: calendario electoral y variables partidistas como información para escenarios cambiarios; base para hipótesis contrastables en F4.
- **Limitaciones:** Resultado no robusto a la corrección por búsqueda de especificaciones (véase FXA-0474).

#### FXA-0467 · Q 83 (A) — International Sanctions and Dollar Dominance

- **Autores:** Javier Bianchi; César Sosa-Padilla
- **Año:** 2025
- **Publicación o institución:** The Economic Journal, vol. 135, n.º 672, págs. 2567-2577 (NBER WP 31024, 2023, rev. 2025)
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-14 Geopolítica, sanciones, política y divisas (principal) · secundarias: TX-12
- **Calidad Q:** 83 (A) — Tipo 25/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 3/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** DOI: 10.1093/ej/ueaf052 · https://nber.org/papers/w31024
- **Acceso y licencia:** Artículo de pago; versión NBER
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Mohammed sanctions currency dollar de-dollarization working paper financial sanctions exchange rate reserves»; WebFetch: sí, página NBER)
- **Contenido:** Modelo monetario simple: la anticipación de sanciones financieras internacionales reduce el rendimiento de conveniencia del dólar y las tenencias de activos en dólares; los efectos de bienestar son en general negativos para todos los países.
- **Uso en el bloque:** AS-ESTR y TR-BCM: canal por el que el uso de sanciones puede erosionar la prima de conveniencia del dólar; CONTRA.
- **Limitaciones:** Modelo estilizado, sin estimación empírica.

#### FXA-0477 · Q 80 (A) — Geopolitical fragmentation risks and international currencies

- **Autores:** Tamar den Besten; Paola Di Casola; Maurizio Michael Habib
- **Año:** 2023 (21 de junio)
- **Publicación o institución:** Banco Central Europeo, artículo especial en «The international role of the euro», junio de 2023
- **Tipo de documento:** Informe técnico de organismo oficial con datos primarios
- **Temática:** TX-14 Geopolítica, sanciones, política y divisas (principal) · secundarias: TX-12
- **Calidad Q:** 80 (A) — Tipo 18/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 9/10 · Impacto 5/10 · Independencia 8/10 · Acceso 10/10
- **DOI / URL:** https://www.ecb.europa.eu/pub/ire/article/html/ecb.ireart202306_01~11d437be4d.en.html
- **Acceso y licencia:** Acceso abierto (BCE)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «IMF working paper geoeconomic fragmentation sanctions central bank reserves currency composition gold de-dollarization»; WebFetch: sí)
- **Contenido:** Tras la invasión de Ucrania, la fragmentación del sistema monetario se limita sobre todo a anuncios y casos concretos (Rusia: renminbi ≈16 % de su facturación en diciembre de 2022); con un índice de alineamiento geopolítico (sanciones, armas, Franja y Ruta, votos en la ONU) no hay vínculo claro con la diversificación de reservas, salvo en las compras de oro; el oro alcanzó ≈13 % de las reservas en 2022.
- **Uso en el bloque:** TR-BCM, AS-EMEA y CONTRA: medir la desdolarización efectiva frente a la anunciada; el oro como principal canal de respuesta a las sanciones.
- **Limitaciones:** Datos hasta 2022; emisor con interés en el papel del euro.

#### FXA-0479 · Q 80 (A) — Geoeconomic Fragmentation and the Future of Multilateralism

- **Autores:** Shekhar Aiyar et al.
- **Año:** 2023
- **Publicación o institución:** Fondo Monetario Internacional, IMF Staff Discussion Note SDN/2023/01
- **Tipo de documento:** Informe técnico de organismo oficial
- **Temática:** TX-14 Geopolítica, sanciones, política y divisas (principal) · secundarias: TX-12, TX-07
- **Calidad Q:** 80 (A) — Tipo 15/25 · Rigor 15/20 · Autoridad 15/15 · Vigencia 10/10 · Impacto 8/10 · Independencia 8/10 · Acceso 9/10
- **DOI / URL:** Confirmada vía página índice: https://cepr.org/voxeu/columns/geo-economic-fragmentation-implications-international-monetary-system (columna de VoxEU que la cita)
- **Acceso y licencia:** Acceso abierto (FMI); URL propia no verificada en esta carga
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «IMF working paper geoeconomic fragmentation sanctions central bank reserves currency composition gold de-dollarization»; WebFetch: sí, de la página índice; no de la obra)
- **Contenido:** Nota del FMI sobre la fragmentación geoeconómica y sus canales (comercio, flujos de capital, sistema de pagos, monedas de reserva, red de seguridad financiera); la columna asociada subraya sistemas de pago paralelos, erosión lenta del dólar, desplazamiento hacia el oro por riesgo de sanciones y fragmentación de las líneas swap.
- **Uso en el bloque:** TR-BCM y PROS: marco de escenarios de fragmentación para horizontes H4.
- **Limitaciones:** Lista completa de autores no verificada; contenido tomado de la columna que la cita.

#### FXA-0466 · Q 80 (A) — A Minimalist Model for the Ruble During the Russian Invasion of Ukraine

- **Autores:** Guido Lorenzoni; Iván Werning
- **Año:** 2022
- **Publicación o institución:** NBER Working Paper 29929
- **Tipo de documento:** Documento de trabajo
- **Temática:** TX-14 Geopolítica, sanciones, política y divisas (principal) · secundarias: TX-08
- **Calidad Q:** 80 (A) — Tipo 20/25 · Rigor 16/20 · Autoridad 15/15 · Vigencia 9/10 · Impacto 5/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** Confirmada vía página índice: https://cepr.org/voxeu/columns/sanctions-and-exchange-rate (referencias de la columna de VoxEU sobre sanciones y tipo de cambio)
- **Acceso y licencia:** NBER (acceso según suscripción)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Itskhoki Mukhin "Sanctions and the Exchange Rate" ruble NBER»; WebFetch: sí, de la página índice; no de la obra)
- **Contenido:** Modelo mínimo para explicar la depreciación y posterior recuperación del rublo durante la invasión de Ucrania, con sanciones, controles y caída de importaciones (según el título).
- **Uso en el bloque:** AS-EMEA: plantilla analítica para divisas bajo sanciones y controles de capital.
- **Limitaciones:** Resumen no leído en esta carga.

#### FXA-0470 · Q 77 (B) — Geopolitical Risk, Capital Flow Volatility, and Asset Market Spillovers

- **Autores:** John Beirne; Nuobu Renzhi
- **Año:** 2025
- **Publicación o institución:** Asian Development Bank, ADB Economics Working Paper Series n.º 820 (noviembre de 2025)
- **Tipo de documento:** Documento de trabajo
- **Temática:** TX-14 Geopolítica, sanciones, política y divisas (principal) · secundarias: TX-07, TX-10
- **Calidad Q:** 77 (B) — Tipo 20/25 · Rigor 15/20 · Autoridad 12/15 · Vigencia 10/10 · Impacto 2/10 · Independencia 8/10 · Acceso 10/10
- **DOI / URL:** https://www.adb.org/sites/default/files/publication/1099706/ewp-820-geopolitical-risk-capital-flow-volatility.pdf
- **Acceso y licencia:** Acceso abierto (BAsD)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «geopolitical risk GPR index exchange rates currencies emerging markets paper Journal of International Money and Finance»; WebFetch: sí)
- **Contenido:** El riesgo geopolítico deprecia las divisas, con efecto mayor y más persistente en emergentes (≈0,4 % tras un choque de una desviación típica en las respuestas a impulso); en avanzadas el impacto recae sobre todo en la bolsa; desarrollo financiero, independencia del banco central y menor deuda pública amortiguan el efecto.
- **Uso en el bloque:** AS-EMAS/AS-EMLA/AS-EMEA y TR-PFV: magnitud esperada y factores de vulnerabilidad de las divisas emergentes ante choques geopolíticos.
- **Limitaciones:** En la regresión base de muestra completa el coeficiente cambiario no es significativo; documento de trabajo reciente.

#### FXA-0478 · Q 76 (B) — US Monetary Spillovers, Foreign Exchange, and Gold Reserves at Times of Geopolitical Fragmentation

- **Autores:** Joshua Aizenman; Jamel Saadaoui; Gazi Salah Uddin; Naoki Yago
- **Año:** 2026 (junio; rev. julio)
- **Publicación o institución:** NBER Working Paper 35337
- **Tipo de documento:** Documento de trabajo
- **Temática:** TX-14 Geopolítica, sanciones, política y divisas (principal) · secundarias: TX-08, TX-02
- **Calidad Q:** 76 (B) — Tipo 20/25 · Rigor 16/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 1/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** https://www.nber.org/papers/w35337
- **Acceso y licencia:** NBER (acceso según suscripción)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «IMF working paper geoeconomic fragmentation sanctions central bank reserves currency composition gold de-dollarization»; WebFetch: sí)
- **Contenido:** Con sorpresas de política del FOMC de alta frecuencia y datos cambiarios por minuto para 18 países, mayores reservas en dólares (y en oro) se asocian a menores depreciaciones tras endurecimientos de la Fed; las reservas en otras monedas no; el efecto se concentra en países sin líneas swap/repo y con más pasivos externos en dólares.
- **Uso en el bloque:** AS-EMAS/AS-EMLA/AS-EMEA y TR-BCM: la composición de reservas y el acceso a líneas swap como amortiguadores ante la Fed en un mundo fragmentado.
- **Limitaciones:** Documento de trabajo muy reciente; 18 países.

#### FXA-0464 · Q 76 (B) — Putting Economics Back into Geoeconomics

- **Autores:** Christopher Clayton; Matteo Maggiori; Jesse Schreger
- **Año:** 2025 (NBER Macroeconomics Annual)
- **Publicación o institución:** NBER Macroeconomics Annual (University of Chicago Press; DOI 10.1086/738941)
- **Tipo de documento:** Artículo revisado (volumen anual NBER)
- **Temática:** TX-14 Geopolítica, sanciones, política y divisas (principal) · secundarias: TX-12
- **Calidad Q:** 76 (B) — Tipo 22/25 · Rigor 14/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 2/10 · Independencia 10/10 · Acceso 4/10
- **DOI / URL:** DOI: 10.1086/738941 · confirmada vía página índice: https://authors.repec.org/pro/pma2176
- **Acceso y licencia:** De pago (University of Chicago Press)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Matteo Maggiori IDEAS RePEc "A Model of the International Monetary System" Farhi "International Currencies and Capital Allocation"»; WebFetch: sí, de la página índice; no de la obra; año y volumen no figuran en el índice)
- **Contenido:** Revisión y agenda sobre la economía de la geoeconomía (coerción económica, fragmentación, sanciones financieras) para la macroeconomía (según el título y la serie).
- **Uso en el bloque:** DOC-A y TR-BCM: puerta de entrada a la literatura de geoeconomía aplicable a divisas.
- **Limitaciones:** Año y volumen no confirmados en el índice; resumen no leído.

#### FXA-0468 · Q 76 (B) — Bucking the Buck: US Financial Sanctions and the International Backlash against the Dollar

- **Autores:** Daniel McDowell
- **Año:** 2023
- **Publicación o institución:** Oxford University Press
- **Tipo de documento:** Libro (monografía académica de economía política)
- **Temática:** TX-14 Geopolítica, sanciones, política y divisas (principal) · secundarias: TX-12
- **Calidad Q:** 76 (B) — Tipo 20/25 · Rigor 13/20 · Autoridad 12/15 · Vigencia 10/10 · Impacto 5/10 · Independencia 10/10 · Acceso 6/10
- **DOI / URL:** DOI: 10.1093/oso/9780197679876.001.0001 · https://academic.oup.com/book/45697
- **Acceso y licencia:** De pago (Oxford Academic); copia de trabajo en carlanorrlof.com devuelta por la búsqueda
- **Estado:** Aprobada
- **Estado del enlace:** MURO_PAGO
- **Última verificación:** 2026-11-02 (búsqueda web: «Mohammed sanctions currency dollar de-dollarization working paper financial sanctions exchange rate reserves»; WebFetch: sí)
- **Contenido:** Analiza cómo el poder sancionador que da a EE. UU. la condición del dólar como «moneda indispensable» provoca una reacción internacional (sistemas de pago alternativos, diversificación de reservas, uso de otras monedas).
- **Uso en el bloque:** TR-BCM y AS-EMAS/AS-EMEA: indicadores de la reacción antidólar (CIPS, acuerdos bilaterales en moneda local) y su alcance real.
- **Limitaciones:** Enfoque de ciencia política; resumen leído solo parcialmente.

#### FXA-0471 · Q 76 (B) — Geopolitical risks and historical exchange rate volatility of the BRICS

- **Autores:** Afees A. Salisu; Juncal Cunado; Rangan Gupta
- **Año:** 2022
- **Publicación o institución:** International Review of Economics & Finance, vol. 77, págs. 179-190
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-14 Geopolítica, sanciones, política y divisas (principal) · secundarias: TX-13, TX-10
- **Calidad Q:** 76 (B) — Tipo 25/25 · Rigor 15/20 · Autoridad 10/15 · Vigencia 10/10 · Impacto 4/10 · Independencia 10/10 · Acceso 2/10
- **DOI / URL:** DOI: 10.1016/j.iref.2021.09.017 · https://repository.up.ac.za/handle/2263/86788
- **Acceso y licencia:** De pago (Elsevier); ficha en repositorio de la Universidad de Pretoria
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «geopolitical risk GPR index exchange rates currencies emerging markets paper Journal of International Money and Finance»; WebFetch: sí)
- **Contenido:** Con GARCH-MIDAS-X, el índice GPR (sobre todo el global frente al específico de país) ayuda a predecir la volatilidad cambiaria de Brasil, Rusia, India, China y Sudáfrica, con algunas ganancias económicas fuera de muestra en carteras de divisas.
- **Uso en el bloque:** TR-PFV y AS-EMLA/AS-EMEA/AS-EMAS: GPR global como variable explicativa de la volatilidad de BRL, ZAR, INR, CNY.
- **Limitaciones:** Predice volatilidad, no dirección; autores muy prolíficos en este tipo de ejercicios.

#### FXA-0475 · Q 76 (B) — Elections and exchange rate policy cycles

- **Autores:** Marco Antônio Cesar Bonomo; Maria Cristina T. Terra
- **Año:** 2005 (versión de trabajo 2001)
- **Publicación o institución:** Economics and Politics, vol. 17, n.º 2, págs. 151-176 · versión de trabajo: FGV EPGE Working Paper 435
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-14 Geopolítica, sanciones, política y divisas (principal) · secundarias: TX-08, TX-10
- **Calidad Q:** 76 (B) — Tipo 24/25 · Rigor 14/20 · Autoridad 11/15 · Vigencia 8/10 · Impacto 4/10 · Independencia 10/10 · Acceso 5/10
- **DOI / URL:** https://ideas.repec.org/p/fgv/epgewp/435.html
- **Acceso y licencia:** Versión de trabajo en abierto (FGV); artículo de pago (Wiley)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Blomberg Hess "Politics and exchange rate forecasts" Journal of International Economics elections currency»; WebFetch: sí)
- **Contenido:** Modelo en que el tipo de cambio real redistribuye renta (exportadores frente a consumidores) y genera ciclos electorales: tipo real más apreciado antes de las elecciones y depreciación después, patrón asociado a América Latina; la intensidad depende del peso electoral del sector no comerciable frente al lobby del comerciable.
- **Uso en el bloque:** AS-EMLA (BRL, MXN, COP, ARS): riesgo de depreciación poselectoral en regímenes gestionados; PROS: escenarios en torno a elecciones.
- **Limitaciones:** Modelo teórico con evidencia ilustrativa; menos aplicable a divisas de libre flotación con bancos centrales independientes.

#### FXA-0463 · Q 74 (B) — The Political Economy of Geoeconomic Power

- **Autores:** Christopher Clayton; Matteo Maggiori; Jesse Schreger
- **Año:** 2025
- **Publicación o institución:** AEA Papers and Proceedings, vol. 115, págs. 588-592
- **Tipo de documento:** Artículo (actas revisadas)
- **Temática:** TX-14 Geopolítica, sanciones, política y divisas (principal) · secundarias: —
- **Calidad Q:** 74 (B) — Tipo 22/25 · Rigor 12/20 · Autoridad 14/15 · Vigencia 10/10 · Impacto 2/10 · Independencia 10/10 · Acceso 4/10
- **DOI / URL:** Confirmada vía página índice: https://authors.repec.org/pro/pma2176
- **Acceso y licencia:** De pago (AEA)
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Matteo Maggiori IDEAS RePEc "A Model of the International Monetary System" Farhi "International Currencies and Capital Allocation"»; WebFetch: sí, de la página índice; no de la obra)
- **Contenido:** Economía política del poder geoeconómico: incentivos internos del hegemón al ejercerlo (según el título).
- **Uso en el bloque:** TR-BCM: lectura de decisiones de política estadounidense (aranceles, sanciones) con impacto cambiario.
- **Limitaciones:** Texto breve; resumen no leído.

#### FXA-0474 · Q 70 (B) — Can Political Variables Really Predict Exchange Rate Movements?

- **Autores:** S. Brock Blomberg; Andrew Mountford
- **Año:** 2000 (rev.; versión de 1999 como Wellesley College WP 99-10)
- **Publicación o institución:** Royal Holloway, University of London, Discussion Papers in Economics 99/11
- **Tipo de documento:** Documento de trabajo
- **Temática:** TX-14 Geopolítica, sanciones, política y divisas (principal) · secundarias: TX-13
- **Calidad Q:** 70 (B) — Tipo 18/25 · Rigor 15/20 · Autoridad 10/15 · Vigencia 7/10 · Impacto 2/10 · Independencia 10/10 · Acceso 8/10
- **DOI / URL:** https://ideas.repec.org/p/hol/holodi/9911.html
- **Acceso y licencia:** Acceso abierto (Royal Holloway)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Blomberg Hess "Politics and exchange rate forecasts" Journal of International Economics elections currency»; WebFetch: sí)
- **Contenido:** Aplicando el «Reality Check» de White para corregir la búsqueda de especificaciones entre muchos modelos, concluye que las variables políticas dejan de ser predictores significativos del tipo de cambio frente al paseo aleatorio.
- **Uso en el bloque:** CONTRA y EVAL: advertencia sobre el sobreajuste de señales políticas; ejemplo de aplicación del Reality Check a divisas.
- **Limitaciones:** No publicado en revista según el índice; muestra antigua.

#### FXA-0476 · Q 70 (B) — Democracy and Markets: The Case of Exchange Rates

- **Autores:** John R. Freeman; Jude C. Hays; Helmut Stix
- **Año:** 1999
- **Publicación o institución:** Oesterreichische Nationalbank, Working Papers n.º 39
- **Tipo de documento:** Documento de trabajo
- **Temática:** TX-14 Geopolítica, sanciones, política y divisas (principal) · secundarias: TX-06
- **Calidad Q:** 70 (B) — Tipo 18/25 · Rigor 14/20 · Autoridad 11/15 · Vigencia 6/10 · Impacto 4/10 · Independencia 9/10 · Acceso 8/10
- **DOI / URL:** https://ideas.repec.org/p/onb/oenbwp/39.html
- **Acceso y licencia:** Acceso abierto (OeNB)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Blomberg Hess "Politics and exchange rate forecasts" Journal of International Economics elections currency»; WebFetch: sí)
- **Contenido:** Las expectativas e incertidumbre sobre resultados electorales y supervivencia del gobierno, y las encuestas de aprobación del jefe del ejecutivo, alteran la probabilidad de cambio de equilibrio en el mercado de divisas; el efecto es menor en sistemas proporcionales que en mayoritarios.
- **Uso en el bloque:** TR-BCM y AS-G10N (GBP, divisas con sistemas mayoritarios): encuestas y estabilidad de gobierno como señales de riesgo político cambiario.
- **Limitaciones:** Documento de trabajo antiguo; versión publicada no verificada.

#### FXA-0472 · Q 68 (B) — The long-run effects of geopolitical risk on foreign exchange markets: evidence from some ASEAN countries

- **Autores:** Hon Chung Hui
- **Año:** 2022
- **Publicación o institución:** International Journal of Emerging Markets, vol. 17, n.º 6, págs. 1543-1564
- **Tipo de documento:** Artículo revisado por pares
- **Temática:** TX-14 Geopolítica, sanciones, política y divisas (principal) · secundarias: TX-10
- **Calidad Q:** 68 (B) — Tipo 22/25 · Rigor 13/20 · Autoridad 8/15 · Vigencia 9/10 · Impacto 3/10 · Independencia 10/10 · Acceso 3/10
- **DOI / URL:** DOI: 10.1108/IJOEM-08-2020-1001 · https://researchportal.hw.ac.uk/en/publications/the-long-run-effects-of-geopolitical-risk-on-foreign-exchange-mar/
- **Acceso y licencia:** De pago (Emerald); ficha en Heriot-Watt
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «geopolitical risk GPR index exchange rates currencies emerging markets paper Journal of International Money and Finance»; WebFetch: sí)
- **Contenido:** Con modelos ARDL que añaden el índice GPR de Caldara e Iacoviello a modelos monetarios, halla cointegración para MYR, IDR, THB y PHP frente al USD: un mayor riesgo geopolítico deprecia la divisa local a largo plazo en los cuatro casos.
- **Uso en el bloque:** AS-EMAS: GPR como determinante de largo plazo de las divisas del sudeste asiático.
- **Limitaciones:** Revista de impacto medio; método de cointegración sensible a la especificación.

#### FXA-0469 · Q 55 (C) — Far-Reaching Consequences of U.S. Financial Sanctions: The Dollar Shortage and the "Triffin Moment"

- **Autores:** Miriam L. Campanella
- **Año:** 2019
- **Publicación o institución:** Robert Triffin International, RTI Paper n.º 10 (con la Université catholique de Louvain y Compagnia di San Paolo)
- **Tipo de documento:** Informe / ensayo de think tank
- **Temática:** TX-14 Geopolítica, sanciones, política y divisas (principal) · secundarias: TX-12
- **Calidad Q:** 55 (C) — Tipo 8/25 · Rigor 9/20 · Autoridad 9/15 · Vigencia 8/10 · Impacto 2/10 · Independencia 9/10 · Acceso 10/10
- **DOI / URL:** https://www.triffininternational.eu/images/RTI/articles_papers/RTI-CSF_Consequences-of-US-Financial-Sanctions_June2019.pdf
- **Acceso y licencia:** Acceso abierto
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Mohammed sanctions currency dollar de-dollarization working paper financial sanctions exchange rate reserves»; WebFetch: sí)
- **Contenido:** Sostiene que las sanciones financieras de EE. UU. apalancan la infraestructura del dólar, pueden generar escasez de dólares (un «momento Triffin») y empujar hacia euro, renminbi (CIPS, swaps) y DEG; advierte de mayor volatilidad en una transición multipolar.
- **Uso en el bloque:** CONTRA y TR-BCM: visión europea del riesgo sistémico del uso de sanciones; contraste con trabajos empíricos (FXA-0443).
- **Limitaciones:** Ensayo con escaso análisis cuantitativo; orientación normativa.

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
| V1.0 | 02/11/2026 | Emisión inicial del archivo específico de divisas del Bloque A Forex: 358 fichas (reutilizadas del Bloque A general V3.2 con su ID original, y nuevas verificadas por búsqueda web con prefijo FX); 0 bajas; orden por temática y Q; índice con recuento de verificadas. |

