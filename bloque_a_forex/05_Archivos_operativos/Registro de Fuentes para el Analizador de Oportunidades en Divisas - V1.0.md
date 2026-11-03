# Archivo operativo F9 — Registro de Fuentes para el Analizador de Oportunidades en Divisas

**Bloque A Forex · Robot Investor · Versión óptima V1.0 · 02/11/2026** · Subordinado al Documento 0 del Bloque A Forex V1.0.

**Versión del archivo:** V1.0 (02/11/2026), alineada con el Documento 0 del Bloque A Forex V1.0 · **Código:** F9 · **Propietario:** AG-16 Buscador de Fuentes Avanzadas (BFA)

## Cómo usar este archivo

**Propósito.** Archivo específico del mercado de divisas (taxonomía TFX del Anexo D del Documento 0 Forex); incluye referencias reutilizadas del Bloque A general (conservan su ID) y referencias nuevas (prefijo FXF-).  Registro de fuentes de opinión, actualidad, datos de mercado, posicionamiento, grandes inversores, regulación y redes con filtro de calidad (Documento 0, 5.1 y 13.1). No contiene literatura académica de dominio (F7) ni métodos de cálculo (F8).

**Propietario y acceso.** Escribe solo AG-16 (BFA). Leen: agentes del plano P2, AG-14, Orquestador, Auditor y Evaluador (este último mide el historial de exactitud de cada fuente). Cualquier otro acceso es una incidencia (Documento 0, 5.2).

**Reglas de uso.**

1. **Lectura.** Lea primero «Novedades»; después el índice de temáticas; dentro de la temática, las fichas aparecen **ordenadas por Q descendente** (a igualdad, la más reciente primero). Cite siempre el ID de la ficha. Para corroboración (PS1) solo cuentan fichas de nivel A o B con `Estado del enlace` distinto de `ROTO`; una ficha `PENDIENTE_VERIFICACION_ALTA` no sustenta evidencia hasta que su propietario la confirme.
2. **Calidad.** Q (0–100) con la rúbrica de fuentes de opinión y actualidad (13.3): Primariedad 20 · Historial de exactitud medido por el Evaluador 20 (neutro 10 mientras no haya pronósticos resueltos) · Transparencia de método y conflictos 15 · Autoridad 15 · Independencia 10 · Actualidad 10 · Accesibilidad 10. Niveles: A (Q ≥ 80), B (65–79), C (50–64), D (< 50: candidata a baja salvo que sea la única fuente de un dato necesario, declarado). En las semillas la Q es provisional hasta la verificación de alta.
3. **Estados del enlace** (HT-02, barrido semanal del domingo): `OK`, `REDIRIGIDO`, `ROTO` (4xx/5xx en dos intentos separados 24 h), `MURO_PAGO`, `CONTENIDO_CAMBIADO` (similitud < 0,8 frente a la copia archivada) y `PENDIENTE_BARRIDO` (estado inicial de esta versión: ningún enlace se ha comprobado aún con HT-02). `Última verificación` recoge la última comprobación documentada, no una del barrido.
4. **Acciones** (potestad plena del propietario, R19): `REPARAR` (DOI, nueva URL oficial o copia archivada; obligatoria cuando la ficha lleva «Alerta»); `DEGRADAR` (bajar Q o nivel, con motivo); `BORRAR` cuando haya enlace roto sin alternativa tras dos barridos, contenido retirado o retractado, falsedad o manipulación demostrada, redundancia total con una ficha de mayor Q, o Q < 50 sin uso en 180 días. Cada borrado añade una línea al «Registro de bajas»; si la ficha sustentaba EVD de F2 se avisa al Curador (CT-11, tipo `fuente_retirada`).
5. **Ciclo.** BFA alimenta el registro por su agenda de vigilancia y por las peticiones de búsqueda (CT-07); antes de buscar aplica el Fondo metodológico (R20), en especial los criterios de credibilidad (lectura lateral). Mensualmente el propietario informa al Orquestador de altas, reparaciones, bajas, salud de enlaces y lagunas (CT-21). Los IDs son inmutables y no se reutilizan; en el «Registro de bajas», «REF-id» es el ID propio de la ficha.

**Reglas propias de F9.** (a) Una fuente de opinión nunca prueba un hecho: los hechos se citan en su fuente primaria. (b) Las copias sindicadas enlazan a su raíz y no cuentan como fuentes independientes. (c) Las fuentes de acceso restringido solo se usan por sus contenidos públicos citables; las credenciales viven en HT-01, nunca en este archivo. (d) Las «piezas» (series, informes o artículos concretos) se registran bajo su fuente y heredan su temática y calidad salvo anotación. (e) Las semillas (`PENDIENTE_VERIFICACION_ALTA`) no sustentan evidencia hasta su confirmación.

## Índice de temáticas (Anexo D, TFX-)

| Código | Temática | Referencias | Verificadas | Pendientes de verificación | A | B | C | D | Q medio |
|---|---|---|---|---|---|---|---|---|---|
| TFX-01 | Bancos centrales del G10 | 20 | 20 | 0 | 19 | 1 | 0 | 0 | 84,3 |
| TFX-02 | Bancos centrales y autoridades monetarias emergentes | 26 | 26 | 0 | 20 | 6 | 0 | 0 | 82,4 |
| TFX-03 | Organismos internacionales y estadísticas cambiarias | 23 | 23 | 0 | 19 | 4 | 0 | 0 | 83,3 |
| TFX-04 | Balanza de pagos, flujos de capital y reservas | 24 | 24 | 0 | 21 | 3 | 0 | 0 | 83,3 |
| TFX-05 | Datos de mercado, tipos de referencia y posicionamiento | 20 | 20 | 0 | 15 | 5 | 0 | 0 | 83,2 |
| TFX-06 | Volatilidad y opciones de divisas: mercados y datos | 20 | 20 | 0 | 8 | 10 | 2 | 0 | 76,0 |
| TFX-07 | Prensa y agencias especializadas en divisas | 20 | 20 | 0 | 0 | 13 | 7 | 0 | 65,6 |
| TFX-08 | Análisis de divisas de bancos, gestoras y casas de análisis | 21 | 21 | 0 | 0 | 18 | 3 | 0 | 68,7 |
| TFX-09 | Calendario, política y riesgo soberano | 20 | 20 | 0 | 5 | 9 | 6 | 0 | 71,0 |
| TFX-10 | Repositorios académicos, think tanks y blogs especializados en divisas | 20 | 20 | 0 | 8 | 12 | 0 | 0 | 77,5 |
| **Total** | — | **214** | **214** | 0 | 115 | 81 | 18 | 0 | 77,8 |

«Verificadas»: enlace en estado OK, REDIRIGIDO, MURO_PAGO o VERIFICADO_BUSQUEDA (existencia y datos confirmados por búsqueda web el 02/11/2026), o verificación documental completa en una carga anterior (25–26/10/2026), pendiente solo del barrido automático HT-02. «Pendientes»: semillas aún en PENDIENTE_VERIFICACION_ALTA o fichas con alerta sin resolver.

## Novedades

- 02/11/2026: emisión inicial V1.0 del archivo específico de divisas.

## TFX-01 Bancos centrales del G10

#### RF-0016 · Q 88 (A) — Federal Reserve Board (comunicados, actas del FOMC, discursos, proyecciones SEP)

- **Canal oficial (URL raíz):** https://www.federalreserve.gov/ (calendario, comunicados y actas del FOMC: https://federalreserve.gov/monetarypolicy/fomccalendars.htm)
- **Emisor:** Board of Governors of the Federal Reserve System
- **Temática:** TFX-01 Bancos centrales del G10 (principal) · secundarias: TFX-09
- **Calidad Q:** 88 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Política monetaria de EE. UU.: calendario del FOMC, comunicados, actas, conferencias de prensa, Summary of Economic Projections (marzo, junio, septiembre, diciembre)
- **Motivo de inclusión y uso:** Fuente original de las decisiones de tipos y de las proyecciones del FOMC (próxima reunión con SEP: 8–9/12/2026). Uso: TR-BCM (AG-09) para la senda de tipos del dólar, sorpresas y cambios de tono; AS-G10N (AG-03) y AS-ESTR (AG-08, dólar amplio) para los diferenciales de tipos frente al USD.
- **Sesgos y cautelas:** Comunicación con orientación de política (no neutral sobre su propia actuación); las actas se publican tres semanas después.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Federal Reserve Board FOMC meeting calendars statements minutes»; WebFetch: sí)
- **Origen:** Reutilizada de F9 V3.2 (TF-01) en el Bloque A Forex V1.0 (2026-11-02).

#### RF-0017 · Q 88 (A) — Banco Central Europeo (decisiones, cuentas de política monetaria, discursos, proyecciones)

- **Canal oficial (URL raíz):** https://www.ecb.europa.eu/ (decisiones del Consejo de Gobierno: https://www.ecb.europa.eu/press/govcdec)
- **Emisor:** Banco Central Europeo
- **Temática:** TFX-01 Bancos centrales del G10 (principal) · secundarias: TFX-09
- **Calidad Q:** 88 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Política monetaria de la eurozona: decisiones de tipos (14:15 CET), declaración y preguntas de la conferencia de prensa, cuentas de la reunión (4 semanas después), otras decisiones (supervisión, estabilidad financiera, estadísticas)
- **Motivo de inclusión y uso:** Fuente original de las decisiones del BCE (última conferencia registrada: 29/10/2026). Uso: TR-BCM (AG-09) para la senda del €STR y el tono del Consejo de Gobierno; AS-G10N (EUR/USD, EUR/JPY, EUR/CHF, EUR/GBP) y AS-EMEA (cruces EUR/PLN, EUR/HUF, EUR/CZK).
- **Sesgos y cautelas:** Comunicación con orientación de política; los metadatos de algunas páginas no reflejan la fecha real del contenido.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «European Central Bank monetary policy decisions accounts ecb.europa.eu»; WebFetch: sí)
- **Origen:** Reutilizada de F9 V3.2 (TF-01) en el Bloque A Forex V1.0 (2026-11-02).

#### RF-0019 · Q 87 (A) — Bank of England (Monetary Policy Report, actas del MPC)

- **Canal oficial (URL raíz):** https://www.bankofengland.co.uk/ (índice del Monetary Policy Report: https://www.bankofengland.co.uk/sitemap/monetary-policy-report · ejemplo: https://www.bankofengland.co.uk/monetary-policy-report/2026/july-2026)
- **Emisor:** Bank of England
- **Temática:** TFX-01 Bancos centrales del G10 (principal) · secundarias: TFX-09
- **Calidad Q:** 87 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Política monetaria del Reino Unido: Monetary Policy Report trimestral, Monetary Policy Summary y actas del MPC con votaciones individuales, calendario de reuniones 2026–2027
- **Motivo de inclusión y uso:** Fuente original de las decisiones y proyecciones del MPC (p. ej., MPR de julio de 2026: Bank Rate al 3,75 % con votación 6–3). Uso: TR-BCM (AG-09) y AS-G10N (GBP/USD, EUR/GBP, GBP/JPY); el reparto de votos del MPC como señal adelantada de la senda de la libra.
- **Sesgos y cautelas:** Comunicación con orientación de política; documentos extensos (leer resumen y actas).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «bankofengland.co.uk monetary-policy-report 2026»; WebFetch: sí)
- **Origen:** Reutilizada de F9 V3.2 (TF-01) en el Bloque A Forex V1.0 (2026-11-02).

#### RF-0200 · Q 87 (A) — BIS — Central bankers' speeches (discursos de banqueros centrales)

- **Canal oficial (URL raíz):** https://www.bis.org/ (ejemplo de la colección: https://www.bis.org/speeches/20251010-japans-economy-and-monetary-policy · archivo histórico: https://www.bis.org/review/)
- **Emisor:** Bank for International Settlements
- **Temática:** TFX-01 Bancos centrales del G10 (principal) · secundarias: TFX-02
- **Calidad Q:** 87 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria (textos de los propios banqueros centrales)
- **Acceso:** Abierto
- **Ámbitos:** Discursos de gobernadores y miembros de consejos de bancos centrales de todo el mundo, en un único repositorio
- **Motivo de inclusión y uso:** Agrega en un solo canal los discursos de banqueros centrales (p. ej., Kazuo Ueda, BoJ, 10/10/2025; Norges Bank Watch, 2026). Uso: TR-BCM (AG-09) para detectar cambios de tono y de orientación futura de los bancos centrales del G10 y emergentes sin canal propio en este archivo; AS-EMAS, AS-EMLA y AS-EMEA para discursos de autoridades emergentes sobre intervención y régimen cambiario.
- **Sesgos y cautelas:** Es un agregador oficial: citar el discurso con su banco central emisor; los textos reflejan la visión de cada orador.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Bank of Japan Outlook for Economic Activity and Prices statements on monetary policy boj.or.jp»; WebFetch: sí)
- **Origen:** Reutilizada de F9 V3.2 (TF-01) en el Bloque A Forex V1.0 (2026-11-02).

#### FXF-0001 · Q 86 (A) — Banco Nacional Suizo (BNS/SNB) — evaluación de política monetaria y resumen de las deliberaciones

- **Canal oficial (URL raíz):** https://www.snb.ch/en/ (resumen de las deliberaciones de septiembre de 2026: https://www.snb.ch/en/publications/communication/summaries/zus_20261022)
- **Emisor:** Swiss National Bank (Schweizerische Nationalbank)
- **Documentación y notas:** El SNB publica la decisión en cada evaluación trimestral de política monetaria y, unas cuatro semanas después, un «Summary of discussion» del Consejo de Gobierno (p. ej., 22/10/2026 sobre la reunión del 22–23/09/2026: tipo oficial al 0 %, franco depreciado ~3 % en términos ponderados por comercio desde junio y señalado como «funding currency» de carry; disposición a intervenir en el mercado de divisas «según sea necesario», retirando la mayor disposición a intervenir señalada antes).
- **Temática:** TFX-01 Bancos centrales del G10 (principal) · secundarias: TFX-04
- **Calidad Q:** 86 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto (inglés, alemán, francés e italiano)
- **Ámbitos:** Tipo oficial del SNB, previsión condicional de inflación, lenguaje sobre intervención en divisas, valoración del franco y condiciones monetarias
- **Motivo de inclusión y uso:** Fuente original del único banco central del G10 que usa la intervención cambiaria como instrumento declarado de política. Uso: TR-BCM (AG-09) para la función de reacción del SNB; AS-G10N (USD/CHF, EUR/CHF) y AS-ESTR (CHF como refugio y como divisa de financiación del carry).
- **Restricciones de uso:** Uso libre con atribución; citar fecha de la evaluación y del resumen.
- **Sesgos posibles:** Comunicación con orientación de política; el lenguaje sobre intervención es deliberadamente condicional.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Publicación del resumen de deliberaciones introducida recientemente; vigilar cambios de calendario.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Swiss National Bank monetary policy assessment 2026»; WebFetch: sí, resumen del 22/10/2026)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-01).

#### FXF-0002 · Q 86 (A) — Bank of Canada — anuncios del tipo oficial y calendario de publicaciones

- **Canal oficial (URL raíz):** https://www.bankofcanada.ca/ (calendario 2026: https://www.bankofcanada.ca/2025/08/bank-canada-publishes-2026-schedule-policy-interest-rate-announcements-other-major-publications/)
- **Emisor:** Bank of Canada
- **Documentación y notas:** Ocho anuncios al año a las 9:45 ET (2026: 28/01, 18/03, 29/04, 10/06, 15/07, 02/09, 28/10, 09/12); «Summary of deliberations» del Consejo de Gobierno tras cada decisión; Business Outlook Survey y Canadian Survey of Consumer Expectations trimestrales. El 28/10/2026 el tipo oficial se elevó al 2,5 %.
- **Temática:** TFX-01 Bancos centrales del G10 (principal) · secundarias: TFX-09
- **Calidad Q:** 86 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (inglés y francés)
- **Ámbitos:** Tipo oficial de Canadá, comunicados, resumen de deliberaciones, encuestas de expectativas, calendario anual
- **Motivo de inclusión y uso:** Fuente original de la política monetaria canadiense. Uso: TR-BCM (AG-09) para la senda del tipo y el calendario; AS-G10M (AG-04: USD/CAD, CAD/JPY) para el diferencial de tipos frente a la Fed.
- **Restricciones de uso:** Uso libre con atribución.
- **Sesgos posibles:** Comunicación con orientación de política.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Bank of Canada Monetary Policy Report interest rate announcement October 2026»; WebFetch: sí, calendario 2026)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-01).

#### FXF-0003 · Q 85 (A) — Reserve Bank of Australia — decisiones y actas del Monetary Policy Board

- **Canal oficial (URL raíz):** https://www.rba.gov.au/ (actas 2026: https://www.rba.gov.au/monetary-policy/rba-board-minutes/2026/)
- **Emisor:** Reserve Bank of Australia
- **Documentación y notas:** El Monetary Policy Board (creado el 01/03/2025, sustituye al Reserve Bank Board) se reúne ocho veces al año tras la publicación de los datos clave de inflación y actividad; las actas se publican dos semanas después de cada reunión (2026: 03/02, 17/03, 05/05, 16/06, 11/08, 29/09…). Histórico de decisiones de tipos desde 1990 en el mismo sitio.
- **Temática:** TFX-01 Bancos centrales del G10 (principal) · secundarias: TFX-09
- **Calidad Q:** 85 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Tipo oficial (cash rate) de Australia, comunicados, actas, marco de política monetaria
- **Motivo de inclusión y uso:** Fuente original de la política monetaria australiana. Uso: TR-BCM (AG-09); AS-G10M (AG-04: AUD/USD, AUD/NZD, AUD/JPY) para diferenciales de tipos y tono.
- **Restricciones de uso:** Uso libre con atribución (licencia del RBA).
- **Sesgos posibles:** Comunicación con orientación de política; el cambio de órgano en 2025 rompe la comparabilidad de las actas anteriores.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Nuevo órgano de decisión desde el 01/03/2025.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Reserve Bank of Australia monetary policy decision minutes Statement on Monetary Policy 2026»; WebFetch: sí, página de actas 2026)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-01).

#### FXF-0004 · Q 85 (A) — Reserve Bank of Australia — Statement on Monetary Policy (previsiones trimestrales)

- **Canal oficial (URL raíz):** https://www.rba.gov.au/publications/smp/ (edición de agosto de 2026: https://www.rba.gov.au/publications/smp/2026/aug/contents.html)
- **Emisor:** Reserve Bank of Australia
- **Documentación y notas:** Informe trimestral con capítulos de condiciones financieras (incluido un apartado de mercados de divisas), condiciones económicas y perspectivas con «detailed forecast information»; edición de agosto de 2026 publicada el 11/08/2026 con datos hasta el 05/08/2026.
- **Temática:** TFX-01 Bancos centrales del G10 (principal) · secundarias: TFX-09
- **Calidad Q:** 85 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 8/10 · Acceso 8/10
- **Tipología:** primaria (previsiones propias del banco central)
- **Acceso:** Abierto (HTML y PDF)
- **Ámbitos:** Previsiones de inflación, actividad y supuestos de tipos y tipo de cambio ponderado (TWI) del RBA
- **Motivo de inclusión y uso:** Previsiones oficiales y lectura del RBA sobre el mercado de divisas. Uso: TR-BCM (AG-09) y AS-G10M (AG-04: AUD) para contrastar la senda descontada con las previsiones oficiales.
- **Restricciones de uso:** Uso libre con atribución.
- **Sesgos posibles:** Previsiones condicionadas a supuestos (no son hechos); el supuesto de tipo de cambio no es previsión.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Reserve Bank of Australia monetary policy decision minutes Statement on Monetary Policy 2026»; WebFetch: sí, SMP de agosto de 2026)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-01).

#### FXF-0005 · Q 85 (A) — Norges Bank — decisiones de tipo oficial (calendario)

- **Canal oficial (URL raíz):** https://www.norges-bank.no/en/ (calendario de decisiones: https://www.norges-bank.no/en/news-events/calendar/policy-rate-decisions/)
- **Emisor:** Norges Bank
- **Documentación y notas:** Decisiones a las 10:00 (hora de Oslo); en la consulta figuraban el 05/11/2026 (sin informe) y el 17/12/2026 (con Monetary Policy Report). Páginas por decisión (p. ej., 26-03-26, 26-06-18, 26-08-13, 26-09-24).
- **Temática:** TFX-01 Bancos centrales del G10 (principal) · secundarias: TFX-09
- **Calidad Q:** 85 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Tipo oficial de Noruega, comunicados y calendario de decisiones
- **Motivo de inclusión y uso:** Fuente original de la política monetaria noruega. Uso: TR-BCM (AG-09); AS-G10M (AG-04: EUR/NOK, USD/NOK) para la senda del tipo y su relación con la corona.
- **Restricciones de uso:** Uso libre con atribución.
- **Sesgos posibles:** Comunicación con orientación de política.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Norges Bank Monetary Policy Report policy rate decision 2026»; WebFetch: sí, calendario de decisiones)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-01).

#### FXF-0006 · Q 85 (A) — Norges Bank — Monetary Policy Report (senda del tipo oficial)

- **Canal oficial (URL raíz):** https://www.norges-bank.no/en/news-events/publications/Monetary-Policy-Report/ (MPR 2/2026: https://www.norges-bank.no/en/news-events/publications/Monetary-Policy-Report/2026/mpr-22026/)
- **Emisor:** Norges Bank
- **Documentación y notas:** Informe trimestral con la evaluación de la senda del tipo oficial, proyecciones de los principales agregados (descargables) y recuadros (MPR 2/2026, 18/06/2026: petróleo y socios comerciales, fijación de precios, tipo real neutral, efecto de la política monetaria en la inflación).
- **Temática:** TFX-01 Bancos centrales del G10 (principal) · secundarias: TFX-09
- **Calidad Q:** 85 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 8/10 · Acceso 8/10
- **Tipología:** primaria (previsiones propias del banco central)
- **Acceso:** Abierto (web, PDF y datos)
- **Ámbitos:** Senda publicada del tipo oficial, supuestos de la corona (importante ponderado), precio del petróleo
- **Motivo de inclusión y uso:** Uno de los pocos bancos centrales del G10 que publica su propia senda de tipos. Uso: TR-BCM (AG-09) para medir la sorpresa frente a la senda descontada; AS-G10M (NOK como divisa de materias primas).
- **Restricciones de uso:** Uso libre con atribución.
- **Sesgos posibles:** Senda condicional, no compromiso.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Norges Bank Monetary Policy Report policy rate decision 2026»; WebFetch: sí, MPR 2/2026)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-01).

#### RF-0020 · Q 85 (A) — Bank of Japan (declaraciones de política, Outlook Report)

- **Canal oficial (URL raíz):** https://www.boj.or.jp/en/ (Outlook for Economic Activity and Prices: https://www.boj.or.jp/en/mopo/outlook/index.htm)
- **Emisor:** Bank of Japan
- **Temática:** TFX-01 Bancos centrales del G10 (principal) · secundarias: TFX-09
- **Calidad Q:** 85 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (versión inglesa con cierto desfase respecto a la japonesa)
- **Ámbitos:** Política monetaria de Japón; Outlook Report trimestral (último: «The Bank's View», 30/10/2026); declaraciones de política
- **Motivo de inclusión y uso:** Fuente original de decisiones y previsiones del BoJ, clave para el yen y el carry trade financiado en yenes. Uso: TR-BCM (AG-09) para la normalización monetaria japonesa; AS-G10N (USD/JPY, EUR/JPY, GBP/JPY) y AS-ESTR (JPY como refugio y divisa de financiación).
- **Sesgos y cautelas:** El texto completo del Outlook se publica días después de «The Bank's View»; traducciones al inglés con retraso.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Bank of Japan Outlook for Economic Activity and Prices statements on monetary policy boj.or.jp»; WebFetch: sí)
- **Origen:** Reutilizada de F9 V3.2 (TF-01) en el Bloque A Forex V1.0 (2026-11-02).

#### FXF-0007 · Q 84 (A) — Sveriges Riksbank — decisiones de política monetaria y Monetary Policy Report (calendario)

- **Canal oficial (URL raíz):** https://www.riksbank.se/en-gb/ (calendario: https://www.riksbank.se/en/press-and-published/calendar/ · documentos de decisión 2026, p. ej.: https://www.riksbank.se/en-gb/press-and-published/calendar/calendar-2026/2026-09-24//Download)
- **Emisor:** Sveriges Riksbank
- **Documentación y notas:** La búsqueda devolvió los documentos de las decisiones de 2026 (19/03, 17/06, 24/09, 16/12) en el calendario oficial; el Riksbank publica decisión de tipo, Monetary Policy Report con senda propia del tipo oficial y actas.
- **Temática:** TFX-01 Bancos centrales del G10 (principal) · secundarias: TFX-09
- **Calidad Q:** 84 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 7/10
- **Tipología:** primaria
- **Acceso:** Abierto (sueco e inglés)
- **Ámbitos:** Tipo oficial de Suecia, senda de tipos publicada, actas, calendario
- **Motivo de inclusión y uso:** Fuente original de la política monetaria sueca. Uso: TR-BCM (AG-09); AS-G10M (AG-04: EUR/SEK, USD/SEK).
- **Restricciones de uso:** Uso libre con atribución.
- **Sesgos posibles:** Comunicación con orientación de política.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Riksbank Monetary Policy Report policy rate decision 2026»; WebFetch: sí, página de calendario —el contenido de 2026 se confirmó por los resultados de búsqueda—)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-01).

#### FXF-0008 · Q 84 (A) — Reserve Bank of New Zealand — decisiones del OCR y Monetary Policy Statement

- **Canal oficial (URL raíz):** https://rbnz.govt.nz/
- **Emisor:** Reserve Bank of New Zealand – Te Pūtea Matua
- **Documentación y notas:** La portada muestra el OCR vigente y su fecha (2,5 % tras la subida del 08/07/2026, con comunicado y «record of meeting»), la próxima revisión del OCR, el calendario de Monetary Policy Statements e informes de estabilidad financiera hasta marzo de 2027 y tipos de cambio del NZD frente a USD, GBP, AUD, EUR, CAD y JPY.
- **Temática:** TFX-01 Bancos centrales del G10 (principal) · secundarias: TFX-09
- **Calidad Q:** 84 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 7/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** OCR, Monetary Policy Statement trimestral con senda del OCR, actas («record of meeting»), tipos de cambio del NZD
- **Motivo de inclusión y uso:** Fuente original de la política monetaria neozelandesa, que publica senda propia del OCR. Uso: TR-BCM (AG-09); AS-G10M (AG-04: NZD/USD, AUD/NZD).
- **Restricciones de uso:** Uso libre con atribución.
- **Sesgos posibles:** Comunicación con orientación de política.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Reserve Bank of New Zealand Monetary Policy Statement OCR decision 2026»; WebFetch: sí, portada)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-01).

#### RF-0025 · Q 83 (A) — Liberty Street Economics (blog del Federal Reserve Bank of New York)

- **Canal oficial (URL raíz):** https://libertystreeteconomics.newyorkfed.org/
- **Emisor:** Federal Reserve Bank of New York (economistas del Research and Statistics Group)
- **Temática:** TFX-01 Bancos centrales del G10 (principal) · secundarias: TFX-10, TFX-04
- **Calidad Q:** 83 (A) — Primariedad 16/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 14/15 · Independencia 9/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** secundaria cualificada (análisis de economistas de banco central)
- **Acceso:** Abierto
- **Ámbitos:** Mercados financieros, crédito de hogares, mercados monetarios, inflación, estabilidad financiera
- **Motivo de inclusión y uso:** Blog del NY Fed (desde 2011) con análisis basados en datos propios, incluidos mercados monetarios, financiación en dólares y mercados internacionales. Uso: TR-BCM (AG-09) para interpretar la transmisión de la política de la Fed y la escasez de dólares; TR-PFV (AG-21) para la financiación en dólares y la base cruzada.
- **Sesgos y cautelas:** Aviso expreso: las opiniones son de los autores, no posición oficial del NY Fed ni del Sistema.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Liberty Street Economics Federal Reserve Bank of New York blog»; WebFetch: sí)
- **Origen:** Reutilizada de F9 V3.2 (TF-01) en el Bloque A Forex V1.0 (2026-11-02).

#### RF-0604 · Q 83 (A) — Federal Reserve Bank of New York — Survey of Market Expectations (SME)

- **Canal oficial (URL raíz):** https://www.newyorkfed.org/markets/market-intelligence/survey-of-market-expectations
- **Emisor:** Federal Reserve Bank of New York, Open Market Trading Desk
- **Temática:** TFX-01 Bancos centrales del G10 (principal) · secundarias: TFX-05
- **Calidad Q:** 83 (A) — Primariedad 17/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** primaria (encuesta oficial; las respuestas son opiniones de participantes)
- **Acceso:** Abierto (cuestionarios, resultados y datos en Excel)
- **Ámbitos:** Expectativas sobre la senda del tipo de los fondos federales, el tamaño del balance de la Fed y la economía; antes de cada reunión del FOMC; fusiona desde 2025 la Survey of Primary Dealers (2002–2024) y la Survey of Market Participants (2014–2024)
- **Motivo de inclusión y uso:** Contraste de la senda implícita en futuros (RF-0346) con las expectativas declaradas (distribuciones de probabilidad). Uso: TR-BCM (AG-09) para la senda esperada del dólar y la asimetría de riesgos; AS-ESTR (AG-08) para el dólar amplio.
- **Sesgos y cautelas:** Opinión agregada, no hechos; resultados publicados unas tres semanas después de la reunión (tras las actas). Una fuente de opinión no prueba hechos (regla F9-a).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «New York Fed reference rates SOFR EFFR OBFR TGCR BGCR» → enlace de la página de tipos de referencia; WebFetch: sí)
- **Origen:** Reutilizada de F9 V3.2 (TF-18) en el Bloque A Forex V1.0 (2026-11-02).

#### FXF-0009 · Q 82 (A) — Banco Nacional Suizo — Quarterly Bulletin (evaluación de política monetaria y previsión condicional)

- **Canal oficial (URL raíz):** https://www.snb.ch/en/publications/quarterly-bulletin/ (n.º 3/2026: https://www.snb.ch/en/publications/quarterly-bulletin/2026/quartbul_2026_3_komplett)
- **Emisor:** Swiss National Bank
- **Documentación y notas:** Boletín trimestral que recoge el informe de política monetaria de cada evaluación (incluida la previsión condicional de inflación) y las señales económicas de los delegados regionales; ediciones 1/2026, 2/2026 y 3/2026 devueltas por la búsqueda.
- **Temática:** TFX-01 Bancos centrales del G10 (principal) · secundarias: —
- **Calidad Q:** 82 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 7/10 · Acceso 7/10
- **Tipología:** primaria (análisis y previsiones propias)
- **Acceso:** Abierto (PDF)
- **Ámbitos:** Condiciones monetarias en Suiza, franco ponderado por comercio, previsión de inflación, encuestas regionales
- **Motivo de inclusión y uso:** Complemento analítico de FXF-0001. Uso: TR-BCM (AG-09) y AS-G10N (CHF).
- **Restricciones de uso:** Uso libre con atribución.
- **Sesgos posibles:** Visión institucional.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Swiss National Bank monetary policy assessment 2026»; WebFetch: no)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-01).

#### FXF-0010 · Q 82 (A) — Bank of Canada — Monetary Policy Report (trimestral)

- **Canal oficial (URL raíz):** https://www.bankofcanada.ca/ (calendario con las fechas del MPR: https://www.bankofcanada.ca/2025/08/bank-canada-publishes-2026-schedule-policy-interest-rate-announcements-other-major-publications/ · publicaciones de octubre de 2026: https://www.bankofcanada.ca/2026/10/)
- **Emisor:** Bank of Canada
- **Documentación y notas:** El MPR acompaña a los anuncios de enero, abril, julio y octubre (MPR de octubre de 2026 publicado el 28/10/2026); proyección económica de base y riesgos.
- **Temática:** TFX-01 Bancos centrales del G10 (principal) · secundarias: TFX-09
- **Calidad Q:** 82 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 7/10 · Acceso 7/10
- **Tipología:** primaria (previsiones propias)
- **Acceso:** Abierto
- **Ámbitos:** Proyecciones de inflación y PIB de Canadá, supuestos de precio del petróleo y del tipo de cambio
- **Motivo de inclusión y uso:** Uso: TR-BCM (AG-09) y AS-G10M (CAD como divisa de materias primas).
- **Restricciones de uso:** Uso libre con atribución.
- **Sesgos posibles:** Previsiones condicionadas a supuestos.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Bank of Canada Monetary Policy Report interest rate announcement October 2026»; WebFetch: sí, calendario 2026 que enlaza el MPR de octubre)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-01).

#### RF-0618 · Q 82 (A) — Bank of Japan — TONA (Tokyo Overnight Average Rate) y estadísticas del mercado monetario

- **Canal oficial (URL raíz):** https://www3.boj.or.jp/market/en/menu_m.htm (TONA diario) · https://www.stat-search.boj.or.jp/ssi/mtshtml/fm02_m_1_en.html (TONA mensual, estadísticas principales del BoJ)
- **Emisor:** Bank of Japan
- **Temática:** TFX-01 Bancos centrales del G10 (principal) · secundarias: TFX-05
- **Calidad Q:** 82 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 6/10
- **Tipología:** primaria (tipo oficial de referencia sobre transacciones)
- **Acceso:** Abierto (páginas en inglés con navegación poco amigable)
- **Ámbitos:** Tipo a un día no garantizado del mercado interbancario de call en yenes («mutan rate»), tipo libre de riesgo recomendado del yen desde el 28/12/2016 y objetivo operativo de la política monetaria tras el cambio de marco de marzo de 2024; medias y el índice TONA los publica QUICK Corp.
- **Motivo de inclusión y uso:** Objetivo operativo de la política monetaria del BoJ desde marzo de 2024 y tipo libre de riesgo del yen. Uso: TR-BCM (AG-09) para seguir la normalización monetaria japonesa; AS-G10N y AS-ESTR (AG-08) para el coste de financiación del carry en yenes y los puntos forward de USD/JPY. La ficha general del BoJ es RF-0020.
- **Sesgos y cautelas:** Las URL oficiales se tomaron de la ficha de Wikipedia (lectura lateral) y no se cargaron; los promedios compuestos no los publica el BoJ.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Bank of Japan TONA uncollateralized overnight call rate data» → Wikipedia «TONAR»; WebFetch: sí, sobre Wikipedia)
- **Origen:** Reutilizada de F9 V3.2 (TF-18) en el Bloque A Forex V1.0 (2026-11-02).

#### RF-0346 · Q 81 (A) — CME Group — FedWatch Tool

- **Canal oficial (URL raíz):** https://www.cmegroup.com/markets/interest-rates/cme-fedwatch-tool.html
- **Emisor:** CME Group
- **Documentación y notas:** Probabilidades de decisiones del FOMC implícitas en futuros de fondos federales a 30 días; metodología publicada (cmegroup.com/articles/2023/understanding-the-cme-group-fedwatch-tool-methodology.html): árbol de probabilidades por reunión, movimientos de 25 pb, tipo efectivo no negativo.
- **Temática:** TFX-01 Bancos centrales del G10 (principal) · secundarias: TFX-05
- **Calidad Q:** 81 (A) — Primariedad 17/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 14/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Expectativas de mercado sobre el tipo de los fondos federales
- **Motivo de inclusión y uso:** Senda de la Fed descontada por el mercado: base para medir sorpresas de política (TR-BCM, AG-09) y el diferencial de tipos esperado del dólar frente al resto del G10 (AS-G10N, AS-ESTR).
- **Restricciones de uso:** Condiciones de CME; citar fecha y hora.
- **Sesgos y cautelas:** Probabilidades de mercado (no previsión de la Fed); supuestos simplificadores.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «CME FedWatch Tool fed funds target rate probabilities»; WebFetch: sí, página de metodología)
- **Origen:** Reutilizada de F9 V3.2 (TF-06) en el Bloque A Forex V1.0 (2026-11-02).

#### RF-0616 · Q 79 (B) — BCE — Survey of Monetary Analysts (SMA)

- **Canal oficial (URL raíz):** https://www.ecb.europa.eu/stats/ecb_surveys/sma/shared/pdf/ecb.smar260323_march.en.pdf (resultados agregados de marzo de 2026; serie en la sección de encuestas del BCE)
- **Emisor:** Banco Central Europeo
- **Temática:** TFX-01 Bancos centrales del G10 (principal) · secundarias: TFX-05
- **Calidad Q:** 79 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 7/10 · Acceso 9/10
- **Tipología:** primaria (encuesta oficial; las respuestas son previsiones de analistas)
- **Acceso:** Abierto (resultados agregados antes/después de cada reunión de política monetaria)
- **Ámbitos:** Sendas esperadas de la facilidad de depósito, MRO, €STR y Euribor a 3 meses; probabilidades de cambios en las dos próximas reuniones; OIS y bonos a 10 años de Alemania, Francia, Italia y España; carteras APP/PEPP; probabilidad de activación del TPI; macro (PIB, paro, HICP). Marzo de 2026: 70 participantes
- **Motivo de inclusión y uso:** Expectativas de política monetaria del euro declaradas por analistas, para contrastar con la senda descontada en la curva OIS. Uso: TR-BCM (AG-09) para la senda esperada del BCE y su asimetría; AS-G10N (EUR) y AS-EMEA (cruces en euros).
- **Sesgos y cautelas:** Opinión de analistas (regla F9-a), no hechos; panel de entidades financieras; preguntas con menos de seis respuestas no se publican.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ECB Survey of Monetary Analysts SMA results and Survey of Professional Forecasters inflation expectations»; WebFetch: sí, PDF de marzo de 2026)
- **Origen:** Reutilizada de F9 V3.2 (TF-18) en el Bloque A Forex V1.0 (2026-11-02).

## TFX-02 Bancos centrales y autoridades monetarias emergentes

#### FXF-0020 · Q 86 (A) — Monetary Authority of Singapore (MAS) — Monetary Policy Statement (banda del S$NEER)

- **Canal oficial (URL raíz):** https://www.mas.gov.sg/ (MPS de octubre de 2026: https://www.mas.gov.sg/news/monetary-policy-statements/2026/mas-monetary-policy-statement-14oct26 · historial de decisiones: https://www.mas.gov.sg/monetary-policy/past-monetary-policy-decisions)
- **Emisor:** Monetary Authority of Singapore
- **Documentación y notas:** La MAS aplica la política monetaria mediante el tipo de cambio: una banda de política del S$NEER (tipo de cambio efectivo nominal del dólar de Singapur) definida por pendiente, anchura y centro. MPS del 14/10/2026: pendiente, anchura y centro sin cambios (tras un ligero aumento de la pendiente en julio de 2026); inflación subyacente MAS prevista en 1,5–2,0 % en 2026 y 1,5–2,5 % en 2027.
- **Temática:** TFX-02 Bancos centrales y autoridades monetarias emergentes (principal) · secundarias: TFX-01
- **Calidad Q:** 86 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Banda del S$NEER, previsiones de inflación y crecimiento de Singapur, Macroeconomic Review semestral
- **Motivo de inclusión y uso:** Único gran banco central que usa el tipo de cambio como instrumento principal: sus decisiones mueven directamente el SGD. Uso: AS-EMAS (AG-05) para el SGD y como ancla de las cestas asiáticas; TR-BCM (AG-09) para el calendario (enero, abril, julio y octubre).
- **Restricciones de uso:** Uso con atribución.
- **Sesgos posibles:** La MAS no publica la banda numérica: su nivel lo estiman los analistas.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «MAS Monetary Policy Statement S$NEER policy band October 2026»; WebFetch: sí, MPS del 14/10/2026)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-02).

#### FXF-0025 · Q 85 (A) — Czech National Bank — decisiones del Consejo, Monetary Policy Report y tipos de cambio diarios

- **Canal oficial (URL raíz):** https://www.cnb.cz/en/index.html
- **Emisor:** Česká národní banka
- **Documentación y notas:** URL oficial tomada del directorio de bancos centrales miembros del BPI (https://bis.org/about/member_cb.htm); los canales concretos (comunicados, actas, informes, estadísticas) se navegan desde la portada.
- **Temática:** TFX-02 Bancos centrales y autoridades monetarias emergentes (principal) · secundarias: TFX-04
- **Calidad Q:** 85 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (portal oficial; versión inglesa disponible)
- **Ámbitos:** Tipo repo a dos semanas; comunicados y actas del Consejo; previsión trimestral con supuesto de tipo de cambio de la corona; tipos de cambio oficiales diarios del CNB
- **Motivo de inclusión y uso:** Fuente original de la política monetaria checa y de su previsión con senda de tipos y de la corona (CZK) frente al euro. Uso: AS-EMEA (AG-07) (segmento EMEA) y TR-BCM (AG-09) para la senda de tipos, el diferencial frente al dólar y el riesgo de intervención.
- **Restricciones de uso:** Uso con atribución según las condiciones del sitio; citar comunicado o serie y fecha.
- **Sesgos posibles:** Comunicación con orientación de política.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos en la fecha de alta; vigilar cambios de régimen cambiario y de marco de política.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «BIS central bank websites directory list of central banks» → página índice https://bis.org/about/member_cb.htm (WebFetch: sí, índice de los 63 bancos centrales miembros con sus URL); sitio del banco central: WebFetch: no)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-02).

#### FXF-0021 · Q 84 (A) — Banco Central do Brasil (BCB) — decisiones y actas del Copom, intervención cambiaria y estadísticas

- **Canal oficial (URL raíz):** https://www.bcb.gov.br/?english
- **Emisor:** Banco Central do Brasil
- **Documentación y notas:** URL oficial tomada del directorio de bancos centrales miembros del BPI (https://bis.org/about/member_cb.htm); los canales concretos (comunicados, actas, informes, estadísticas) se navegan desde la portada.
- **Temática:** TFX-02 Bancos centrales y autoridades monetarias emergentes (principal) · secundarias: TFX-04
- **Calidad Q:** 84 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (portal oficial; versión inglesa disponible)
- **Ámbitos:** Tipo Selic y comunicados y actas del Copom; informe de política monetaria; operaciones cambiarias (subastas de swaps cambiarios y de dólares al contado); reservas internacionales; series del SGS
- **Motivo de inclusión y uso:** Fuente original de la política monetaria brasileña y de las intervenciones en el mercado del real (BRL): senda de la Selic, diferencial de carry frente al dólar y anuncios de subastas de swaps cambiarios. Uso: AS-EMLA (AG-06) (segmento EMLA) y TR-BCM (AG-09) para la senda de tipos, el diferencial frente al dólar y el riesgo de intervención.
- **Restricciones de uso:** Uso con atribución según las condiciones del sitio; citar comunicado o serie y fecha.
- **Sesgos posibles:** Comunicación con orientación de política; muchas series solo en portugués.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos en la fecha de alta; vigilar cambios de régimen cambiario y de marco de política.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «BIS central bank websites directory list of central banks» → página índice https://bis.org/about/member_cb.htm (WebFetch: sí, índice de los 63 bancos centrales miembros con sus URL); sitio del banco central: WebFetch: no)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-02).

#### FXF-0022 · Q 84 (A) — Banco de México (Banxico) — anuncios de política monetaria, minutas e información del mercado cambiario

- **Canal oficial (URL raíz):** https://www.banxico.org.mx/indexEn.html
- **Emisor:** Banco de México
- **Documentación y notas:** URL oficial tomada del directorio de bancos centrales miembros del BPI (https://bis.org/about/member_cb.htm); los canales concretos (comunicados, actas, informes, estadísticas) se navegan desde la portada.
- **Temática:** TFX-02 Bancos centrales y autoridades monetarias emergentes (principal) · secundarias: TFX-04
- **Calidad Q:** 84 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (portal oficial; versión inglesa disponible)
- **Ámbitos:** Tasa objetivo y anuncios de la Junta de Gobierno; minutas; informe trimestral; Comisión de Cambios (coberturas cambiarias, reservas); SIE (Sistema de Información Económica)
- **Motivo de inclusión y uso:** Fuente original de la política monetaria mexicana y de las medidas de la Comisión de Cambios que afectan al peso (MXN), la divisa emergente más líquida de Latinoamérica. Uso: AS-EMLA (AG-06) (segmento EMLA) y TR-BCM (AG-09) para la senda de tipos, el diferencial frente al dólar y el riesgo de intervención.
- **Restricciones de uso:** Uso con atribución según las condiciones del sitio; citar comunicado o serie y fecha.
- **Sesgos posibles:** Comunicación con orientación de política; la Comisión de Cambios incluye a la Secretaría de Hacienda.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos en la fecha de alta; vigilar cambios de régimen cambiario y de marco de política.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «BIS central bank websites directory list of central banks» → página índice https://bis.org/about/member_cb.htm (WebFetch: sí, índice de los 63 bancos centrales miembros con sus URL); sitio del banco central: WebFetch: no)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-02).

#### FXF-0023 · Q 84 (A) — Bank of Korea — decisiones del tipo base, actas del Monetary Policy Board y estadísticas (ECOS)

- **Canal oficial (URL raíz):** https://www.bok.or.kr/eng/main/main.do
- **Emisor:** Bank of Korea
- **Documentación y notas:** URL oficial tomada del directorio de bancos centrales miembros del BPI (https://bis.org/about/member_cb.htm); los canales concretos (comunicados, actas, informes, estadísticas) se navegan desde la portada.
- **Temática:** TFX-02 Bancos centrales y autoridades monetarias emergentes (principal) · secundarias: TFX-04
- **Calidad Q:** 84 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (portal oficial; versión inglesa disponible)
- **Ámbitos:** Tipo base y comunicados del Monetary Policy Board; actas; Monetary Policy Report; reservas de divisas mensuales; base de datos estadística ECOS
- **Motivo de inclusión y uso:** Fuente original de la política monetaria coreana y de los datos de reservas, clave para el won (KRW) y su sensibilidad al ciclo tecnológico global. Uso: AS-EMAS (AG-05) (segmento EMAS) y TR-BCM (AG-09) para la senda de tipos, el diferencial frente al dólar y el riesgo de intervención.
- **Restricciones de uso:** Uso con atribución según las condiciones del sitio; citar comunicado o serie y fecha.
- **Sesgos posibles:** Comunicación con orientación de política; las intervenciones se divulgan con desfase y en términos netos.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos en la fecha de alta; vigilar cambios de régimen cambiario y de marco de política.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «BIS central bank websites directory list of central banks» → página índice https://bis.org/about/member_cb.htm (WebFetch: sí, índice de los 63 bancos centrales miembros con sus URL); sitio del banco central: WebFetch: no)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-02).

#### FXF-0024 · Q 84 (A) — Reserve Bank of India — decisiones del MPC, estadísticas de reservas y del mercado de divisas

- **Canal oficial (URL raíz):** https://www.rbi.org.in/home.aspx
- **Emisor:** Reserve Bank of India
- **Documentación y notas:** URL oficial tomada del directorio de bancos centrales miembros del BPI (https://bis.org/about/member_cb.htm); los canales concretos (comunicados, actas, informes, estadísticas) se navegan desde la portada.
- **Temática:** TFX-02 Bancos centrales y autoridades monetarias emergentes (principal) · secundarias: TFX-04
- **Calidad Q:** 84 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (portal oficial; versión inglesa disponible)
- **Ámbitos:** Tipo repo y resoluciones del Monetary Policy Committee; actas; Weekly Statistical Supplement (reservas de divisas); boletín mensual con compras y ventas netas de divisas; regulación cambiaria (FEMA)
- **Motivo de inclusión y uso:** Fuente original de la política monetaria india y de los datos de intervención del RBI en la rupia (INR), divisa con gestión activa del tipo de cambio. Uso: AS-EMAS (AG-05) (segmento EMAS) y TR-BCM (AG-09) para la senda de tipos, el diferencial frente al dólar y el riesgo de intervención.
- **Restricciones de uso:** Uso con atribución según las condiciones del sitio; citar comunicado o serie y fecha.
- **Sesgos posibles:** Datos de intervención publicados con desfase; regulación cambiaria compleja.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos en la fecha de alta; vigilar cambios de régimen cambiario y de marco de política.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «BIS central bank websites directory list of central banks» → página índice https://bis.org/about/member_cb.htm (WebFetch: sí, índice de los 63 bancos centrales miembros con sus URL); sitio del banco central: WebFetch: no)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-02).

#### FXF-0026 · Q 84 (A) — Narodowy Bank Polski (NBP) — decisiones del Consejo de Política Monetaria y tipos de cambio medios

- **Canal oficial (URL raíz):** https://www.nbp.pl/homen.aspx?f=%2Fsrodeken.htm
- **Emisor:** Narodowy Bank Polski
- **Documentación y notas:** URL oficial tomada del directorio de bancos centrales miembros del BPI (https://bis.org/about/member_cb.htm); los canales concretos (comunicados, actas, informes, estadísticas) se navegan desde la portada.
- **Temática:** TFX-02 Bancos centrales y autoridades monetarias emergentes (principal) · secundarias: TFX-04
- **Calidad Q:** 84 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (portal oficial; versión inglesa disponible)
- **Ámbitos:** Tipo de referencia y comunicados del Consejo de Política Monetaria (RPP); informe de inflación; tipos de cambio medios oficiales diarios del NBP; reservas
- **Motivo de inclusión y uso:** Fuente original de la política monetaria polaca y de los tipos de cambio oficiales del zloty (PLN). Uso: AS-EMEA (AG-07) (segmento EMEA) y TR-BCM (AG-09) para la senda de tipos, el diferencial frente al dólar y el riesgo de intervención.
- **Restricciones de uso:** Uso con atribución según las condiciones del sitio; citar comunicado o serie y fecha.
- **Sesgos posibles:** Conferencias del gobernador con fuerte componente personal; parte de la documentación solo en polaco.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos en la fecha de alta; vigilar cambios de régimen cambiario y de marco de política.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «BIS central bank websites directory list of central banks» → página índice https://bis.org/about/member_cb.htm (WebFetch: sí, índice de los 63 bancos centrales miembros con sus URL); sitio del banco central: WebFetch: no)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-02).

#### FXF-0027 · Q 84 (A) — South African Reserve Bank (SARB) — decisiones y declaraciones del MPC, reservas y estadísticas

- **Canal oficial (URL raíz):** https://www.resbank.co.za/pages/default.aspx
- **Emisor:** South African Reserve Bank
- **Documentación y notas:** URL oficial tomada del directorio de bancos centrales miembros del BPI (https://bis.org/about/member_cb.htm); los canales concretos (comunicados, actas, informes, estadísticas) se navegan desde la portada.
- **Temática:** TFX-02 Bancos centrales y autoridades monetarias emergentes (principal) · secundarias: TFX-04
- **Calidad Q:** 84 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (portal oficial; versión inglesa disponible)
- **Ámbitos:** Tipo repo y declaración del Monetary Policy Committee; Monetary Policy Review; Quarterly Bulletin (balanza de pagos); reservas oficiales mensuales
- **Motivo de inclusión y uso:** Fuente original de la política monetaria sudafricana; el rand (ZAR) es la divisa africana más negociada y un termómetro del apetito por riesgo emergente. Uso: AS-EMEA (AG-07) (segmento EMEA) y TR-BCM (AG-09) para la senda de tipos, el diferencial frente al dólar y el riesgo de intervención.
- **Restricciones de uso:** Uso con atribución según las condiciones del sitio; citar comunicado o serie y fecha.
- **Sesgos posibles:** Comunicación con orientación de política.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos en la fecha de alta; vigilar cambios de régimen cambiario y de marco de política.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «BIS central bank websites directory list of central banks» → página índice https://bis.org/about/member_cb.htm (WebFetch: sí, índice de los 63 bancos centrales miembros con sus URL); sitio del banco central: WebFetch: no)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-02).

#### FXF-0028 · Q 84 (A) — Hong Kong Monetary Authority (HKMA) — sistema de tipo de cambio vinculado y estadísticas monetarias

- **Canal oficial (URL raíz):** https://www.hkma.gov.hk/eng/index.shtml
- **Emisor:** Hong Kong Monetary Authority
- **Documentación y notas:** URL oficial tomada del directorio de bancos centrales miembros del BPI (https://bis.org/about/member_cb.htm); los canales concretos (comunicados, actas, informes, estadísticas) se navegan desde la portada.
- **Temática:** TFX-02 Bancos centrales y autoridades monetarias emergentes (principal) · secundarias: TFX-04
- **Calidad Q:** 84 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (portal oficial; versión inglesa disponible)
- **Ámbitos:** Linked Exchange Rate System (convertibilidad del HKD frente al USD en una banda), operaciones de defensa del vínculo, saldo agregado del sistema bancario, tipo base, estadísticas monetarias
- **Motivo de inclusión y uso:** Fuente original del régimen del dólar de Hong Kong (HKD) y de las operaciones que lo defienden; también referencia para el mercado del renminbi offshore (CNH). Uso: AS-EMAS (AG-05) (segmento EMAS) y TR-BCM (AG-09) para la senda de tipos, el diferencial frente al dólar y el riesgo de intervención.
- **Restricciones de uso:** Uso con atribución según las condiciones del sitio; citar comunicado o serie y fecha.
- **Sesgos posibles:** Autoridad que defiende su propio régimen: leer como fuente del hecho, no como valoración de su sostenibilidad.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos en la fecha de alta; vigilar cambios de régimen cambiario y de marco de política.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «BIS central bank websites directory list of central banks» → página índice https://bis.org/about/member_cb.htm (WebFetch: sí, índice de los 63 bancos centrales miembros con sus URL); sitio del banco central: WebFetch: no)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-02).

#### FXF-0029 · Q 84 (A) — Bank of Israel — decisiones del Comité de Política Monetaria y operaciones en divisas

- **Canal oficial (URL raíz):** https://www.boi.org.il/en/
- **Emisor:** Bank of Israel
- **Documentación y notas:** URL oficial tomada del directorio de bancos centrales miembros del BPI (https://bis.org/about/member_cb.htm); los canales concretos (comunicados, actas, informes, estadísticas) se navegan desde la portada.
- **Temática:** TFX-02 Bancos centrales y autoridades monetarias emergentes (principal) · secundarias: TFX-04
- **Calidad Q:** 84 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (portal oficial; versión inglesa disponible)
- **Ámbitos:** Tipo oficial, comunicados y actas del Comité de Política Monetaria; previsiones del Departamento de Investigación; datos de compras de divisas y reservas
- **Motivo de inclusión y uso:** Fuente original de la política monetaria israelí y de las intervenciones en el séquel (ILS). Uso: AS-EMEA (AG-07) (segmento EMEA) y TR-BCM (AG-09) para la senda de tipos, el diferencial frente al dólar y el riesgo de intervención.
- **Restricciones de uso:** Uso con atribución según las condiciones del sitio; citar comunicado o serie y fecha.
- **Sesgos posibles:** Comunicación con orientación de política; sensibilidad geopolítica alta.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos en la fecha de alta; vigilar cambios de régimen cambiario y de marco de política.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «BIS central bank websites directory list of central banks» → página índice https://bis.org/about/member_cb.htm (WebFetch: sí, índice de los 63 bancos centrales miembros con sus URL); sitio del banco central: WebFetch: no)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-02).

#### FXF-0030 · Q 84 (A) — Banco Central de Chile — Reunión de Política Monetaria, IPoM y estadísticas cambiarias

- **Canal oficial (URL raíz):** https://www.bcentral.cl/en/inicio
- **Emisor:** Banco Central de Chile
- **Documentación y notas:** URL oficial tomada del directorio de bancos centrales miembros del BPI (https://bis.org/about/member_cb.htm); los canales concretos (comunicados, actas, informes, estadísticas) se navegan desde la portada.
- **Temática:** TFX-02 Bancos centrales y autoridades monetarias emergentes (principal) · secundarias: TFX-04
- **Calidad Q:** 84 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (portal oficial; versión inglesa disponible)
- **Ámbitos:** Tasa de política monetaria, comunicados y minutas de las RPM; Informe de Política Monetaria (IPoM); dólar observado; base de datos estadísticos; programas de intervención cambiaria cuando se anuncian
- **Motivo de inclusión y uso:** Fuente original de la política monetaria chilena y del tipo de cambio de referencia (dólar observado) del peso (CLP), muy ligado al cobre. Uso: AS-EMLA (AG-06) (segmento EMLA) y TR-BCM (AG-09) para la senda de tipos, el diferencial frente al dólar y el riesgo de intervención.
- **Restricciones de uso:** Uso con atribución según las condiciones del sitio; citar comunicado o serie y fecha.
- **Sesgos posibles:** Comunicación con orientación de política.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos en la fecha de alta; vigilar cambios de régimen cambiario y de marco de política.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «BIS central bank websites directory list of central banks» → página índice https://bis.org/about/member_cb.htm (WebFetch: sí, índice de los 63 bancos centrales miembros con sus URL); sitio del banco central: WebFetch: no)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-02).

#### FXF-0032 · Q 84 (A) — Banco Central de Reserva del Perú (BCRP) — programa monetario, intervención cambiaria y estadísticas

- **Canal oficial (URL raíz):** https://www.bcrp.gob.pe/en
- **Emisor:** Banco Central de Reserva del Perú
- **Documentación y notas:** URL oficial tomada del directorio de bancos centrales miembros del BPI (https://bis.org/about/member_cb.htm); los canales concretos (comunicados, actas, informes, estadísticas) se navegan desde la portada.
- **Temática:** TFX-02 Bancos centrales y autoridades monetarias emergentes (principal) · secundarias: TFX-04
- **Calidad Q:** 84 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (portal oficial; versión inglesa disponible)
- **Ámbitos:** Tasa de referencia y programa monetario mensual; Reporte de Inflación; operaciones cambiarias diarias (compras y ventas, swaps cambiarios, certificados indexados); base de datos de series
- **Motivo de inclusión y uso:** Fuente original de la política monetaria peruana y de una de las intervenciones cambiarias más activas de la región sobre el sol (PEN). Uso: AS-EMLA (AG-06) (segmento EMLA) y TR-BCM (AG-09) para la senda de tipos, el diferencial frente al dólar y el riesgo de intervención.
- **Restricciones de uso:** Uso con atribución según las condiciones del sitio; citar comunicado o serie y fecha.
- **Sesgos posibles:** Comunicación con orientación de política.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos en la fecha de alta; vigilar cambios de régimen cambiario y de marco de política.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «BIS central bank websites directory list of central banks» → página índice https://bis.org/about/member_cb.htm (WebFetch: sí, índice de los 63 bancos centrales miembros con sus URL); sitio del banco central: WebFetch: no)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-02).

#### FXF-0033 · Q 84 (A) — Banco de la República (Colombia) — decisiones de la Junta Directiva y estadísticas cambiarias

- **Canal oficial (URL raíz):** https://www.banrep.gov.co/en
- **Emisor:** Banco de la República
- **Documentación y notas:** URL oficial tomada del directorio de bancos centrales miembros del BPI (https://bis.org/about/member_cb.htm); los canales concretos (comunicados, actas, informes, estadísticas) se navegan desde la portada.
- **Temática:** TFX-02 Bancos centrales y autoridades monetarias emergentes (principal) · secundarias: TFX-04
- **Calidad Q:** 84 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (portal oficial; versión inglesa disponible)
- **Ámbitos:** Tasa de política, comunicados y minutas de la Junta Directiva; Informe de Política Monetaria; reservas internacionales; series de la TRM (tasa representativa del mercado)
- **Motivo de inclusión y uso:** Fuente original de la política monetaria colombiana y de los datos del peso (COP). Uso: AS-EMLA (AG-06) (segmento EMLA) y TR-BCM (AG-09) para la senda de tipos, el diferencial frente al dólar y el riesgo de intervención.
- **Restricciones de uso:** Uso con atribución según las condiciones del sitio; citar comunicado o serie y fecha.
- **Sesgos posibles:** Comunicación con orientación de política; Junta con participación del Ministerio de Hacienda.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos en la fecha de alta; vigilar cambios de régimen cambiario y de marco de política.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «BIS central bank websites directory list of central banks» → página índice https://bis.org/about/member_cb.htm (WebFetch: sí, índice de los 63 bancos centrales miembros con sus URL); sitio del banco central: WebFetch: no)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-02).

#### FXF-0031 · Q 83 (A) — Magyar Nemzeti Bank (MNB) — decisiones del Consejo Monetario y estadísticas

- **Canal oficial (URL raíz):** https://english.mnb.hu/
- **Emisor:** Magyar Nemzeti Bank
- **Documentación y notas:** URL oficial tomada del directorio de bancos centrales miembros del BPI (https://bis.org/about/member_cb.htm); los canales concretos (comunicados, actas, informes, estadísticas) se navegan desde la portada.
- **Temática:** TFX-02 Bancos centrales y autoridades monetarias emergentes (principal) · secundarias: TFX-04
- **Calidad Q:** 83 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (portal oficial; versión inglesa disponible)
- **Ámbitos:** Tipo base y comunicados del Consejo Monetario; informe de inflación; tipos de cambio oficiales; estadísticas de balanza de pagos y reservas
- **Motivo de inclusión y uso:** Fuente original de la política monetaria húngara y del forinto (HUF), una de las divisas de carry de Europa central. Uso: AS-EMEA (AG-07) (segmento EMEA) y TR-BCM (AG-09) para la senda de tipos, el diferencial frente al dólar y el riesgo de intervención.
- **Restricciones de uso:** Uso con atribución según las condiciones del sitio; citar comunicado o serie y fecha.
- **Sesgos posibles:** Comunicación con orientación de política; historial de cambios de marco operativo.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos en la fecha de alta; vigilar cambios de régimen cambiario y de marco de política.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «BIS central bank websites directory list of central banks» → página índice https://bis.org/about/member_cb.htm (WebFetch: sí, índice de los 63 bancos centrales miembros con sus URL); sitio del banco central: WebFetch: no)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-02).

#### FXF-0034 · Q 83 (A) — Bank Indonesia — decisiones del BI-Rate y estabilización de la rupia

- **Canal oficial (URL raíz):** https://www.bi.go.id/en/Default.aspx
- **Emisor:** Bank Indonesia
- **Documentación y notas:** URL oficial tomada del directorio de bancos centrales miembros del BPI (https://bis.org/about/member_cb.htm); los canales concretos (comunicados, actas, informes, estadísticas) se navegan desde la portada.
- **Temática:** TFX-02 Bancos centrales y autoridades monetarias emergentes (principal) · secundarias: TFX-04
- **Calidad Q:** 83 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (portal oficial; versión inglesa disponible)
- **Ámbitos:** BI-Rate y comunicados de la reunión del Consejo de Gobernadores; intervención «triple» (contado, DNDF y bonos); reservas; tipo de referencia JISDOR
- **Motivo de inclusión y uso:** Fuente original de la política monetaria indonesia y de la estabilización de la rupia (IDR). Uso: AS-EMAS (AG-05) (segmento EMAS) y TR-BCM (AG-09) para la senda de tipos, el diferencial frente al dólar y el riesgo de intervención.
- **Restricciones de uso:** Uso con atribución según las condiciones del sitio; citar comunicado o serie y fecha.
- **Sesgos posibles:** Comunicación con orientación de política; mandato explícito de estabilidad cambiaria.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos en la fecha de alta; vigilar cambios de régimen cambiario y de marco de política.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «BIS central bank websites directory list of central banks» → página índice https://bis.org/about/member_cb.htm (WebFetch: sí, índice de los 63 bancos centrales miembros con sus URL); sitio del banco central: WebFetch: no)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-02).

#### FXF-0035 · Q 83 (A) — Bank Negara Malaysia — decisiones del MPC y estadísticas

- **Canal oficial (URL raíz):** https://www.bnm.gov.my/
- **Emisor:** Bank Negara Malaysia
- **Documentación y notas:** URL oficial tomada del directorio de bancos centrales miembros del BPI (https://bis.org/about/member_cb.htm); los canales concretos (comunicados, actas, informes, estadísticas) se navegan desde la portada.
- **Temática:** TFX-02 Bancos centrales y autoridades monetarias emergentes (principal) · secundarias: TFX-04
- **Calidad Q:** 83 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (portal oficial; versión inglesa disponible)
- **Ámbitos:** Overnight Policy Rate y declaración del Monetary Policy Committee; reservas quincenales; normas cambiarias (Foreign Exchange Policy)
- **Motivo de inclusión y uso:** Fuente original de la política monetaria malasia y de las normas cambiarias del ringgit (MYR). Uso: AS-EMAS (AG-05) (segmento EMAS) y TR-BCM (AG-09) para la senda de tipos, el diferencial frente al dólar y el riesgo de intervención.
- **Restricciones de uso:** Uso con atribución según las condiciones del sitio; citar comunicado o serie y fecha.
- **Sesgos posibles:** Comunicación con orientación de política; mercado del MYR con restricciones offshore.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos en la fecha de alta; vigilar cambios de régimen cambiario y de marco de política.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «BIS central bank websites directory list of central banks» → página índice https://bis.org/about/member_cb.htm (WebFetch: sí, índice de los 63 bancos centrales miembros con sus URL); sitio del banco central: WebFetch: no)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-02).

#### FXF-0036 · Q 83 (A) — Bank of Thailand — decisiones del MPC y estadísticas

- **Canal oficial (URL raíz):** https://www.bot.or.th/en/home.html
- **Emisor:** Bank of Thailand
- **Documentación y notas:** URL oficial tomada del directorio de bancos centrales miembros del BPI (https://bis.org/about/member_cb.htm); los canales concretos (comunicados, actas, informes, estadísticas) se navegan desde la portada.
- **Temática:** TFX-02 Bancos centrales y autoridades monetarias emergentes (principal) · secundarias: TFX-04
- **Calidad Q:** 83 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (portal oficial; versión inglesa disponible)
- **Ámbitos:** Tipo oficial y comunicados del Monetary Policy Committee; Monetary Policy Report; reservas; medidas sobre el mercado del baht
- **Motivo de inclusión y uso:** Fuente original de la política monetaria tailandesa y de las medidas sobre el baht (THB). Uso: AS-EMAS (AG-05) (segmento EMAS) y TR-BCM (AG-09) para la senda de tipos, el diferencial frente al dólar y el riesgo de intervención.
- **Restricciones de uso:** Uso con atribución según las condiciones del sitio; citar comunicado o serie y fecha.
- **Sesgos posibles:** Comunicación con orientación de política.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos en la fecha de alta; vigilar cambios de régimen cambiario y de marco de política.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «BIS central bank websites directory list of central banks» → página índice https://bis.org/about/member_cb.htm (WebFetch: sí, índice de los 63 bancos centrales miembros con sus URL); sitio del banco central: WebFetch: no)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-02).

#### FXF-0037 · Q 83 (A) — Bangko Sentral ng Pilipinas — decisiones de la Monetary Board y estadísticas

- **Canal oficial (URL raíz):** https://www.bsp.gov.ph/
- **Emisor:** Bangko Sentral ng Pilipinas
- **Documentación y notas:** URL oficial tomada del directorio de bancos centrales miembros del BPI (https://bis.org/about/member_cb.htm); los canales concretos (comunicados, actas, informes, estadísticas) se navegan desde la portada.
- **Temática:** TFX-02 Bancos centrales y autoridades monetarias emergentes (principal) · secundarias: TFX-04
- **Calidad Q:** 83 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (portal oficial; versión inglesa disponible)
- **Ámbitos:** Tipo oficial (RRP) y comunicados de la Monetary Board; Monetary Policy Report; reservas internacionales brutas; remesas
- **Motivo de inclusión y uso:** Fuente original de la política monetaria filipina y de los datos de reservas y remesas que sostienen el peso (PHP). Uso: AS-EMAS (AG-05) (segmento EMAS) y TR-BCM (AG-09) para la senda de tipos, el diferencial frente al dólar y el riesgo de intervención.
- **Restricciones de uso:** Uso con atribución según las condiciones del sitio; citar comunicado o serie y fecha.
- **Sesgos posibles:** Comunicación con orientación de política.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos en la fecha de alta; vigilar cambios de régimen cambiario y de marco de política.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «BIS central bank websites directory list of central banks» → página índice https://bis.org/about/member_cb.htm (WebFetch: sí, índice de los 63 bancos centrales miembros con sus URL); sitio del banco central: WebFetch: no)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-02).

#### FXF-0039 · Q 83 (A) — Banca Națională a României (BNR) — decisiones de política monetaria y tipos de referencia

- **Canal oficial (URL raíz):** https://www.bnro.ro/Home.aspx
- **Emisor:** Banca Națională a României
- **Documentación y notas:** URL oficial tomada del directorio de bancos centrales miembros del BPI (https://bis.org/about/member_cb.htm); los canales concretos (comunicados, actas, informes, estadísticas) se navegan desde la portada.
- **Temática:** TFX-02 Bancos centrales y autoridades monetarias emergentes (principal) · secundarias: TFX-04
- **Calidad Q:** 83 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (portal oficial; versión inglesa disponible)
- **Ámbitos:** Tipo oficial, comunicados y actas del Consejo; informe de inflación; tipo de cambio de referencia diario del leu (RON); reservas
- **Motivo de inclusión y uso:** Fuente original de la política monetaria rumana y del tipo de referencia del leu, divisa con flotación muy gestionada frente al euro. Uso: AS-EMEA (AG-07) (segmento EMEA) y TR-BCM (AG-09) para la senda de tipos, el diferencial frente al dólar y el riesgo de intervención.
- **Restricciones de uso:** Uso con atribución según las condiciones del sitio; citar comunicado o serie y fecha.
- **Sesgos posibles:** Flotación gestionada con baja transparencia sobre intervención.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos en la fecha de alta; vigilar cambios de régimen cambiario y de marco de política.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «BIS central bank websites directory list of central banks» → página índice https://bis.org/about/member_cb.htm (WebFetch: sí, índice de los 63 bancos centrales miembros con sus URL); sitio del banco central: WebFetch: no)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-02).

#### FXF-0038 · Q 82 (A) — Central Bank of the Republic of Türkiye (CBRT) — decisiones del Comité de Política Monetaria y reservas

- **Canal oficial (URL raíz):** https://www.tcmb.gov.tr/wps/wcm/connect/en/tcmb+en
- **Emisor:** Türkiye Cumhuriyet Merkez Bankası
- **Documentación y notas:** URL oficial tomada del directorio de bancos centrales miembros del BPI (https://bis.org/about/member_cb.htm); los canales concretos (comunicados, actas, informes, estadísticas) se navegan desde la portada.
- **Temática:** TFX-02 Bancos centrales y autoridades monetarias emergentes (principal) · secundarias: TFX-04
- **Calidad Q:** 82 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 15/15 · Independencia 8/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (portal oficial; versión inglesa disponible)
- **Ámbitos:** Tipo de las repo a una semana y comunicados del Comité de Política Monetaria; informe de inflación; reservas internacionales semanales; balanza de pagos
- **Motivo de inclusión y uso:** Fuente original de la política monetaria turca y de los datos de reservas, imprescindibles para evaluar el carry en liras (TRY) y su riesgo de cola. Uso: AS-EMEA (AG-07) (segmento EMEA) y TR-BCM (AG-09) para la senda de tipos, el diferencial frente al dólar y el riesgo de intervención.
- **Restricciones de uso:** Uso con atribución según las condiciones del sitio; citar comunicado o serie y fecha.
- **Sesgos posibles:** Historial de cambios bruscos de marco y de dirección; reservas netas a reconstruir con swaps.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos en la fecha de alta; vigilar cambios de régimen cambiario y de marco de política.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «BIS central bank websites directory list of central banks» → página índice https://bis.org/about/member_cb.htm (WebFetch: sí, índice de los 63 bancos centrales miembros con sus URL); sitio del banco central: WebFetch: no)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-02).

#### FXF-0041 · Q 79 (B) — Saudi Central Bank (SAMA) — régimen de tipo fijo del riyal y estadísticas

- **Canal oficial (URL raíz):** https://www.sama.gov.sa/en-us/pages/default.aspx
- **Emisor:** Saudi Central Bank
- **Documentación y notas:** URL oficial tomada del directorio de bancos centrales miembros del BPI (https://bis.org/about/member_cb.htm); los canales concretos (comunicados, actas, informes, estadísticas) se navegan desde la portada.
- **Temática:** TFX-02 Bancos centrales y autoridades monetarias emergentes (principal) · secundarias: TFX-04
- **Calidad Q:** 79 (B) — Primariedad 20/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 15/15 · Independencia 8/10 · Actualidad 8/10 · Acceso 7/10
- **Tipología:** primaria
- **Acceso:** Abierto (portal oficial; versión inglesa disponible)
- **Ámbitos:** Tipo de cambio fijo del riyal (SAR) frente al dólar; tipos oficiales (que siguen a los de la Fed); boletines estadísticos mensuales; activos de reserva
- **Motivo de inclusión y uso:** Fuente original del régimen del riyal y de sus reservas; útil para la vigilancia de los tipos fijos del Golfo. Uso: AS-EMEA (AG-07) (segmento EMEA) y TR-BCM (AG-09) para la senda de tipos, el diferencial frente al dólar y el riesgo de intervención.
- **Restricciones de uso:** Uso con atribución según las condiciones del sitio; citar comunicado o serie y fecha.
- **Sesgos posibles:** Fuente del propio régimen: no valora su sostenibilidad; datos con desfase.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos en la fecha de alta; vigilar cambios de régimen cambiario y de marco de política.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «BIS central bank websites directory list of central banks» → página índice https://bis.org/about/member_cb.htm (WebFetch: sí, índice de los 63 bancos centrales miembros con sus URL); sitio del banco central: WebFetch: no)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-02).

#### FXF-0042 · Q 79 (B) — Central Bank of the UAE — régimen de tipo fijo del dírham y estadísticas

- **Canal oficial (URL raíz):** https://www.centralbank.ae/en/
- **Emisor:** Central Bank of the United Arab Emirates
- **Documentación y notas:** URL oficial tomada del directorio de bancos centrales miembros del BPI (https://bis.org/about/member_cb.htm); los canales concretos (comunicados, actas, informes, estadísticas) se navegan desde la portada.
- **Temática:** TFX-02 Bancos centrales y autoridades monetarias emergentes (principal) · secundarias: TFX-04
- **Calidad Q:** 79 (B) — Primariedad 20/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 15/15 · Independencia 8/10 · Actualidad 8/10 · Acceso 7/10
- **Tipología:** primaria
- **Acceso:** Abierto (portal oficial; versión inglesa disponible)
- **Ámbitos:** Tipo de cambio fijo del dírham (AED) frente al dólar; tipo base; estadísticas monetarias y de reservas
- **Motivo de inclusión y uso:** Fuente original del régimen del dírham y de las condiciones monetarias de los EAU. Uso: AS-EMEA (AG-07) (segmento EMEA) y TR-BCM (AG-09) para la senda de tipos, el diferencial frente al dólar y el riesgo de intervención.
- **Restricciones de uso:** Uso con atribución según las condiciones del sitio; citar comunicado o serie y fecha.
- **Sesgos posibles:** Fuente del propio régimen; datos con desfase.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos en la fecha de alta; vigilar cambios de régimen cambiario y de marco de política.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «BIS central bank websites directory list of central banks» → página índice https://bis.org/about/member_cb.htm (WebFetch: sí, índice de los 63 bancos centrales miembros con sus URL); sitio del banco central: WebFetch: no)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-02).

#### FXF-0043 · Q 79 (B) — Bank Al-Maghrib — régimen cambiario del dírham marroquí y política monetaria

- **Canal oficial (URL raíz):** https://www.bkam.ma/en
- **Emisor:** Bank Al-Maghrib
- **Documentación y notas:** URL oficial tomada del directorio de bancos centrales miembros del BPI (https://bis.org/about/member_cb.htm); los canales concretos (comunicados, actas, informes, estadísticas) se navegan desde la portada.
- **Temática:** TFX-02 Bancos centrales y autoridades monetarias emergentes (principal) · secundarias: TFX-04
- **Calidad Q:** 79 (B) — Primariedad 20/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 15/15 · Independencia 8/10 · Actualidad 8/10 · Acceso 7/10
- **Tipología:** primaria
- **Acceso:** Abierto (portal oficial; versión inglesa disponible)
- **Ámbitos:** Tipo director y comunicados del Consejo; régimen de cesta (euro y dólar) con banda de fluctuación del dírham (MAD); reservas; estadísticas
- **Motivo de inclusión y uso:** Fuente original del régimen cambiario de Marruecos, caso de flexibilización gradual de un tipo anclado a una cesta. Uso: AS-EMEA (AG-07) (segmento EMEA) y TR-BCM (AG-09) para la senda de tipos, el diferencial frente al dólar y el riesgo de intervención.
- **Restricciones de uso:** Uso con atribución según las condiciones del sitio; citar comunicado o serie y fecha.
- **Sesgos posibles:** Mercado poco líquido; documentación parcialmente solo en francés.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos en la fecha de alta; vigilar cambios de régimen cambiario y de marco de política.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «BIS central bank websites directory list of central banks» → página índice https://bis.org/about/member_cb.htm (WebFetch: sí, índice de los 63 bancos centrales miembros con sus URL); sitio del banco central: WebFetch: no)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-02).

#### FXF-0040 · Q 78 (B) — People's Bank of China (PBoC) — política monetaria, comunicados y estadísticas

- **Canal oficial (URL raíz):** https://www.pbc.gov.cn/en/3688006/index.html
- **Emisor:** People's Bank of China
- **Documentación y notas:** URL oficial tomada del directorio de bancos centrales miembros del BPI (https://bis.org/about/member_cb.htm); los canales concretos (comunicados, actas, informes, estadísticas) se navegan desde la portada.
- **Temática:** TFX-02 Bancos centrales y autoridades monetarias emergentes (principal) · secundarias: TFX-04
- **Calidad Q:** 78 (B) — Primariedad 20/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 15/15 · Independencia 7/10 · Actualidad 9/10 · Acceso 7/10
- **Tipología:** primaria
- **Acceso:** Abierto (portal oficial; versión inglesa disponible)
- **Ámbitos:** Tipos de las operaciones de mercado abierto y de la facilidad a medio plazo; Loan Prime Rate; informes de ejecución de la política monetaria; estadísticas monetarias y de reservas; regulación del renminbi
- **Motivo de inclusión y uso:** Fuente original de la política monetaria china y de la orientación sobre el renminbi (CNY/CNH); complementa la fijación diaria de CFETS (ficha en TFX-05). Uso: AS-EMAS (AG-05) (segmento EMAS) y TR-BCM (AG-09) para la senda de tipos, el diferencial frente al dólar y el riesgo de intervención.
- **Restricciones de uso:** Uso con atribución según las condiciones del sitio; citar comunicado o serie y fecha.
- **Sesgos posibles:** Baja transparencia sobre la función de reacción cambiaria (señalada por el Tesoro de EE. UU.); versión inglesa con retraso.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos en la fecha de alta; vigilar cambios de régimen cambiario y de marco de política.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «BIS central bank websites directory list of central banks» → página índice https://bis.org/about/member_cb.htm (WebFetch: sí, índice de los 63 bancos centrales miembros con sus URL); sitio del banco central: WebFetch: no)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-02).

#### FXF-0045 · Q 78 (B) — Banco Central de la República Argentina (BCRA) — régimen cambiario, comunicaciones y estadísticas

- **Canal oficial (URL raíz):** https://www.bcra.gob.ar/en/
- **Emisor:** Banco Central de la República Argentina
- **Documentación y notas:** URL oficial tomada del directorio de bancos centrales miembros del BPI (https://bis.org/about/member_cb.htm); los canales concretos (comunicados, actas, informes, estadísticas) se navegan desde la portada.
- **Temática:** TFX-02 Bancos centrales y autoridades monetarias emergentes (principal) · secundarias: TFX-04
- **Calidad Q:** 78 (B) — Primariedad 20/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 15/15 · Independencia 6/10 · Actualidad 9/10 · Acceso 7/10
- **Tipología:** primaria
- **Acceso:** Abierto (portal oficial; versión inglesa disponible)
- **Ámbitos:** Régimen cambiario y sus normas (comunicaciones «A»), tipo de cambio de referencia mayorista, reservas internacionales diarias, política monetaria
- **Motivo de inclusión y uso:** Fuente original de las normas cambiarias y de las reservas de Argentina; el ARS se analiza como ámbito de régimen (controles, bandas, brecha). Uso: AS-EMLA (AG-06) (segmento EMLA) y TR-BCM (AG-09) para la senda de tipos, el diferencial frente al dólar y el riesgo de intervención.
- **Restricciones de uso:** Uso con atribución según las condiciones del sitio; citar comunicado o serie y fecha.
- **Sesgos posibles:** Normas cambiarias sujetas a cambios frecuentes; credibilidad institucional históricamente baja (regla de prudencia en PS1).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos en la fecha de alta; vigilar cambios de régimen cambiario y de marco de política.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «BIS central bank websites directory list of central banks» → página índice https://bis.org/about/member_cb.htm (WebFetch: sí, índice de los 63 bancos centrales miembros con sus URL); sitio del banco central: WebFetch: no)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-02).

#### FXF-0044 · Q 75 (B) — State Bank of Vietnam — tipo central diario del dong y política monetaria

- **Canal oficial (URL raíz):** https://www.sbv.gov.vn/webcenter/portal/en/home/sbv
- **Emisor:** State Bank of Vietnam
- **Documentación y notas:** URL oficial tomada del directorio de bancos centrales miembros del BPI (https://bis.org/about/member_cb.htm); los canales concretos (comunicados, actas, informes, estadísticas) se navegan desde la portada.
- **Temática:** TFX-02 Bancos centrales y autoridades monetarias emergentes (principal) · secundarias: TFX-04
- **Calidad Q:** 75 (B) — Primariedad 20/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 15/15 · Independencia 7/10 · Actualidad 8/10 · Acceso 6/10
- **Tipología:** primaria
- **Acceso:** Abierto (portal oficial; versión inglesa disponible)
- **Ámbitos:** Tipo central diario del dong (VND) frente al dólar y banda de negociación; tipos oficiales; normativa cambiaria
- **Motivo de inclusión y uso:** Fuente original del tipo central del dong y de los cambios de banda, base de cualquier análisis del VND. Uso: AS-EMAS (AG-05) (segmento EMAS) y TR-BCM (AG-09) para la senda de tipos, el diferencial frente al dólar y el riesgo de intervención.
- **Restricciones de uso:** Uso con atribución según las condiciones del sitio; citar comunicado o serie y fecha.
- **Sesgos posibles:** Transparencia limitada; versión inglesa incompleta.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos en la fecha de alta; vigilar cambios de régimen cambiario y de marco de política.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «BIS central bank websites directory list of central banks» → página índice https://bis.org/about/member_cb.htm (WebFetch: sí, índice de los 63 bancos centrales miembros con sus URL); sitio del banco central: WebFetch: no)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-02).

## TFX-03 Organismos internacionales y estadísticas cambiarias

#### FXF-0051 · Q 89 (A) — FMI — COFER (composición por divisas de las reservas oficiales de divisas)

- **Canal oficial (URL raíz):** https://data.imf.org/cofer (nota de datos del 30/09/2026: https://data.imf.org/en/news/imf%20data%20brief%20september%2030)
- **Emisor:** Fondo Monetario Internacional (Departamento de Estadística)
- **Documentación y notas:** Encuesta trimestral (trimestral desde 1999T1) con 147 informantes; divisas: USD, EUR, CNY, JPY, GBP, AUD, CAD, CHF y «otras»; datos por país estrictamente confidenciales; desde 2025T3 se eliminó el residuo «no asignado» (revisado hasta 2000T1) y se publica la parte imputada. Dato de 2026T2 (30/09/2026): dólar 56,70 % (57,18 % en T1), euro 20,60 % (20,04 %), «otras» por encima del 6 %.
- **Temática:** TFX-03 Organismos internacionales y estadísticas cambiarias (principal) · secundarias: TFX-04
- **Calidad Q:** 89 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Papel internacional de las divisas como reserva; diversificación de reservas; dólar dominante
- **Motivo de inclusión y uso:** Dato oficial de la demanda de reservas por divisa. Uso: AS-ESTR (AG-08) y TR-BCM (AG-09) para el tema estructural del dólar, el euro y el renminbi (TX-12); AS-G10M para AUD y CAD como divisas de reserva.
- **Restricciones de uso:** Uso con atribución; citar trimestre y fecha de publicación.
- **Sesgos posibles:** Los cambios de participación mezclan efectos de valoración (tipo de cambio) y compras activas: separar ambos antes de interpretar.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Cambio metodológico de 2025T3 (eliminación del residuo no asignado).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «IMF COFER currency composition of official foreign exchange reserves 2026»; WebFetch: sí, página COFER y nota del 30/09/2026)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-03).

#### RF-0003 · Q 89 (A) — BIS (Bank for International Settlements), sección de estadísticas

- **Canal oficial:** bis.org/statistics/
- **Documentación y notas:** Portal de datos vigente: data.bis.org · Serie de crédito total de la pieza 4.3: bis.org/statistics/totcredit.htm
- **Temática:** TFX-03 Organismos internacionales y estadísticas cambiarias (principal) · secundarias: TFX-05
- **Calidad Q:** 89 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 10/10
- **Nivel de fiabilidad en V2.4:** A
- **Tipología:** primaria
- **Motivo de inclusión:** Estadísticas internacionales de referencia en banca central con módulos cambiarios propios: tipos de cambio bilaterales y efectivos (nominales y reales), encuesta trienal de divisas y derivados OTC, estadísticas bancarias internacionales y crédito global en dólares. Uso: MOTOR (AG-13, REER y valoración), AS-ESTR (AG-08, valor) y TR-PFV (AG-21, volúmenes y crédito en dólares).
- **Ámbitos:** Crédito global; banca central; deuda; derivados de OTC; mercados de divisas
- **Restricciones de uso:** Uso libre con atribución; citar la base estadística concreta y la fecha de extracción
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Sesgos posibles:** Ninguno editorial conocido; cobertura centrada en bancos centrales miembros
- **Cambios de propiedad o de metodología:** Sin cambios conocidos; el BIS revisa metodologías de sus bases periódicamente (vigilar notas de las series)
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «BIS effective exchange rate indices triennial survey 2025 foreign exchange turnover» → páginas de bis.org/statistics/; WebFetch: sí, https://www.bis.org/statistics/rpfx25_fx.htm)
- **Origen:** Reutilizada de F9 V3.2 (TF-01) en el Bloque A Forex V1.0 (2026-11-02).

#### RF-0004 · Q 89 (A) — BCE Data Portal (Banco Central Europeo)

- **Canal oficial:** https://data.ecb.europa.eu (balanza de pagos y otras estadísticas exteriores, p. ej.: https://data.ecb.europa.eu/publications/balance-payments-and-other-external-statistics/3032577 · política del BCE/Eurosistema y tipos de cambio: https://data.ecb.europa.eu/publications/ecbeurosystem-policy-and-exchange-rates)
- **Documentación y notas:** Descargas, metadatos SDMX y documentación desde el propio portal · Citar la serie con su clave SDMX y la fecha de consulta. Menús de publicación verificados: balanza de pagos (cuenta corriente, inversión directa, de cartera y otra inversión), reservas internacionales, deuda externa, posición de inversión internacional, tipos de cambio e indicadores de competitividad.
- **Temática:** TFX-03 Organismos internacionales y estadísticas cambiarias (principal) · secundarias: TFX-04
- **Calidad Q:** 89 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 10/10 · Acceso 10/10
- **Nivel de fiabilidad en V2.4:** A
- **Tipología:** primaria
- **Motivo de inclusión:** Fuente oficial de datos de la eurozona con módulos cambiarios: tipos de referencia del euro, indicadores de competitividad (tipos de cambio efectivos nominales y reales del BCE), balanza de pagos, posición de inversión internacional y reservas, con API SDMX pública. Uso en el Bloque A Forex: MOTOR (AG-13) para REER del euro y descarga de series; AS-G10N (EUR) para flujos de cartera de la zona del euro; AS-EMEA para tipos de referencia de PLN, HUF, CZK y RON frente al euro.
- **Ámbitos:** Eurozona; tipos de cambio; competitividad; balanza de pagos; posición de inversión internacional; reservas; inflación HICP
- **Restricciones de uso:** Datos públicos con atribución; citar la serie (clave SDMX) y su fecha
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Sesgos posibles:** Ninguno; cobertura eurozona
- **Cambios de propiedad o de metodología:** Portal nuevo (sucesor del SDW clásico): vigilar reorganizaciones de series; adopción futura del MBP7 en las estadísticas exteriores
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ECB Data Portal data.ecb.europa.eu exchange rates balance of payments»; WebFetch: sí, subpágina de balanza de pagos con menús de reservas, deuda externa, IIP y tipos de cambio)
- **Origen:** Reutilizada de F9 V3.2 (TF-01; estaba PENDIENTE_BARRIDO) en el Bloque A Forex V1.0 (2026-11-02).

#### RF-0021 · Q 88 (A) — Eurostat

- **Canal oficial (URL raíz):** https://ec.europa.eu/eurostat (guía del sitio: https://ec.europa.eu/eurostat/en/help/website-guide)
- **Emisor:** Comisión Europea — Oficina Estadística de la Unión Europea
- **Temática:** TFX-03 Organismos internacionales y estadísticas cambiarias (principal) · secundarias: —
- **Calidad Q:** 88 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto (acceso gratuito a todas sus bases de datos)
- **Ámbitos:** IPCA (HICP), PIB, empleo, comercio, finanzas públicas de la UE; calendario de publicaciones y «euro indicators»
- **Motivo de inclusión y uso:** Estadística oficial armonizada de la UE: IPCA (HICP) para deflactar tipos de cambio reales, balanza de pagos y comercio de la UE, y paridades de poder adquisitivo del programa Eurostat-OCDE. Uso: MOTOR (AG-13, REER y PPA); AS-G10N (EUR) y AS-EMEA (PLN, HUF, CZK, RON).
- **Sesgos y cautelas:** Datos agregados a partir de institutos nacionales; revisiones y desfases según país.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Eurostat official website European statistics database»; WebFetch: sí)
- **Origen:** Reutilizada de F9 V3.2 (TF-01) en el Bloque A Forex V1.0 (2026-11-02).

#### FXF-0401 · Q 87 (A) — FMI — Balance of Payments and International Investment Position Manual, 7.ª edición (MBP7/BPM7)

- **Canal oficial (URL raíz):** https://www.imf.org/en/News/Articles/2025/03/20/pr25072-imf-and-statistical-community-release-new-global-standards-for-macroeconomic-stats (capítulos: https://www.imf.org/en/data/statistics/bpm/bpm7-chapters · documento de política: https://www.imf.org/-/media/files/publications/pp/2025/english/ppea2025023.pdf)
- **Emisor:** Fondo Monetario Internacional (Departamento de Estadística), con el Comité de Estadísticas de Balanza de Pagos (BOPCOM)
- **Documentación y notas:** Publicado el 20/03/2025 junto con el SCN 2025 (adoptado por la Comisión de Estadística de la ONU el 05/03/2025); actualiza el MBP6 de 2009 para recoger interconexión, digitalización e innovación financiera. Implantación recomendada a los países en 2029–2030; versión «white cover» en inglés y traducciones (incluido el español) tras la versión final.
- **Temática:** TFX-03 Organismos internacionales y estadísticas cambiarias (principal) · secundarias: TFX-04
- **Calidad Q:** 87 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 7/10 · Acceso 10/10
- **Tipología:** primaria (norma estadística internacional)
- **Acceso:** Abierto
- **Ámbitos:** Definiciones y clasificaciones de la balanza de pagos y la posición de inversión internacional; activos de reserva; inversión directa y de cartera; transición MBP6 → MBP7
- **Motivo de inclusión y uso:** Norma que define todas las partidas que el bloque lee en TFX-04 (cuenta corriente, cuenta financiera, reservas). Uso: MOTOR (AG-13) y AS-ESTR (AG-08) para interpretar correctamente saldos y rupturas de serie; BFA para anotar cambios metodológicos en las fichas de balanza de pagos.
- **Restricciones de uso:** Uso con atribución; citar edición y capítulo.
- **Sesgos posibles:** Documento normativo: la adopción por países será escalonada, con rupturas de serie hasta 2030.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sustituye al MBP6 (2009); el FMI armonizará después el GFSM 2014 y el MFSMCG 2016.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «IMF BPM7 Balance of Payments and International Investment Position Manual seventh edition»; WebFetch: sí, comunicado PR 25/072)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-03).

#### RF-0005 · Q 87 (A) — World Bank Open Data (Banco Mundial)

- **Canal oficial:** https://data.worldbank.org (indicador cambiario de referencia: https://data.worldbank.org/indicator/PA.NUS.FCRF?lang=en-gb · API: https://api.worldbank.org/v2/country/CMR/indicator/PA.NUS.FCRF)
- **Documentación y notas:** Indicador PA.NUS.FCRF «Official exchange rate (LCU per US$, period average)», con fuente declarada en International Financial Statistics del FMI; licencia CC BY 4.0; último año mostrado: 2025. Útil también para PIB (NY.GDP.MKTP.CD), factores de conversión PPA del ICP e indicadores de deuda externa.
- **Temática:** TFX-03 Organismos internacionales y estadísticas cambiarias (principal) · secundarias: TFX-04
- **Calidad Q:** 87 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 8/10 · Acceso 10/10
- **Nivel de fiabilidad en V2.4:** A
- **Tipología:** primaria
- **Motivo de inclusión:** Series anuales comparables de tipos de cambio oficiales medios, PIB y PPA para casi todos los países, incluidas divisas frontera y exóticas sin cobertura de mercado. Uso en el Bloque A Forex: MOTOR (AG-13) para normalizar magnitudes a dólares y calcular desviaciones frente a PPA; AS-EMLA y AS-EMEA para contexto de largo plazo de divisas emergentes y frontera.
- **Ámbitos:** Tipos de cambio oficiales anuales; PIB; PPA; indicadores de desarrollo por país
- **Restricciones de uso:** CC BY 4.0 en general; citar indicador (código), país y año
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Sesgos posibles:** Media anual del tipo oficial: no refleja tipos paralelos ni regímenes múltiples (contrastar con AREAER, FXF-0052); desfase de publicación y revisiones retrospectivas
- **Cambios de propiedad o de metodología:** Sin cambios conocidos; las series se revisan con las actualizaciones del World Development Indicators
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «World Bank Open Data official exchange rate LCU per US$ period average PA.NUS.FCRF»; WebFetch: sí, página del indicador (variante ?lang=en-gb; la URL sin parámetro dio error de servidor puntual))
- **Origen:** Reutilizada de F9 V3.2 (TF-01; estaba PENDIENTE_BARRIDO) en el Bloque A Forex V1.0 (2026-11-02).

#### FXF-0050 · Q 86 (A) — BPI — Encuesta Trienal de Bancos Centrales sobre divisas y derivados OTC (2025)

- **Canal oficial (URL raíz):** https://bis.org/statistics/rpfx25.htm (resultados de divisas: https://www.bis.org/statistics/rpfx25_fx.htm · publicación: https://www.bis.org/publications/triennial-central-bank-survey-foreign-exchange-and-over-the-counter-otc-derivatives-markets-2025)
- **Emisor:** Bank for International Settlements, con la participación de los bancos centrales y autoridades de más de 50 jurisdicciones
- **Documentación y notas:** Resultados preliminares publicados el 30/09/2025 (datos de abril de 2025; los definitivos, en el BIS Quarterly Review de diciembre de 2025; complementa a RF-0540 de TFX-06, centrada en derivados OTC: esta ficha cubre el volumen del mercado de divisas): negociación OTC de divisas de 9,6 billones de dólares diarios (neto-neto), +28 % frente a 2022; contado 31 %, *forwards* 19 %, *FX swaps* 42 %, opciones 7 %; el dólar en un lado del 89,2 % de las operaciones; euro 28,9 %, yen 16,8 %, libra 10,2 %, renminbi 8,5 %, franco 6,4 %.
- **Temática:** TFX-03 Organismos internacionales y estadísticas cambiarias (principal) · secundarias: TFX-05, TFX-06
- **Calidad Q:** 86 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 6/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto (tablas, notas y conjuntos de datos)
- **Ámbitos:** Volumen del mercado mundial de divisas por instrumento, divisa, par, contraparte y plaza; derivados OTC de tipos de interés
- **Motivo de inclusión y uso:** Fuente de referencia sobre el tamaño y la estructura del mercado de divisas (liquidez relativa de cada par y de cada divisa emergente), base de la regla de asignación por liquidez de los segmentos. Uso: AS-ESTR y Analistas de segmento (liquidez y costes), TR-PFV (AG-21) y MOTOR (AG-13, ponderaciones).
- **Restricciones de uso:** Uso libre con atribución; citar edición (abril de 2025) y tabla.
- **Sesgos posibles:** Fotografía de un solo mes cada tres años; cambios en el número de bancos informantes entre ediciones.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Revisión de los datos preliminares en la publicación definitiva.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «BIS effective exchange rate indices triennial survey 2025 foreign exchange turnover»; WebFetch: sí, rpfx25_fx.htm)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-03).

#### FXF-0402 · Q 86 (A) — BCE — The international role of the euro (informe anual, junio de 2026)

- **Canal oficial (URL raíz):** https://ecb.europa.eu/press/other-publications/ire/html/index.en.html (edición de junio de 2026: https://www.ecb.europa.eu/press/other-publications/ire/html/ecb.ire202606.es.html)
- **Emisor:** Banco Central Europeo
- **Documentación y notas:** 25.ª edición, 02/06/2026. Índice compuesto del papel internacional del euro +0,2 pp a tipos constantes en 2025; el euro sigue segunda divisa (~20 %); cuota en reservas 20,2 % en 2025T4 (dólar ~57 %); emisión internacional de deuda en euros +30 % (> 1,1 billones de USD); entradas de cartera en la zona del euro > 850.000 M€ en 2025; comportamiento de refugio en episodios de aversión al riesgo; cuota del euro en la negociación de divisas a la baja (BPI ~29 % en abril de 2025; CLS 32,2 %).
- **Temática:** TFX-03 Organismos internacionales y estadísticas cambiarias (principal) · secundarias: TFX-04
- **Calidad Q:** 86 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria (informe institucional con datos propios y de terceros)
- **Acceso:** Abierto
- **Ámbitos:** Papel internacional del euro (reservas, deuda, facturación, pagos, negociación de divisas); desdolarización; liquidez en euros a bancos centrales extranjeros (EUREP)
- **Motivo de inclusión y uso:** Síntesis anual oficial del uso internacional del euro. Uso: AS-ESTR (AG-08) y TR-BCM (AG-09) para el tema estructural EUR frente a USD (TX-12); AS-G10N (EUR/USD) para el contexto de flujos de cartera hacia la zona del euro.
- **Restricciones de uso:** Uso con atribución.
- **Sesgos posibles:** El emisor tiene interés institucional en el fortalecimiento del euro: separar datos de recomendaciones de política.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos; el índice compuesto se publica a tipos constantes y corrientes.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ECB report "international role of the euro" 2026»; WebFetch: sí, edición de junio de 2026)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-03).

#### FXF-0052 · Q 85 (A) — FMI — Annual Report on Exchange Arrangements and Exchange Restrictions (AREAER)

- **Canal oficial (URL raíz):** https://www.imf.org/en/publications/annual-report-on-exchange-arrangements-and-exchange-restrictions/issues/2024/12/19/annual-report-on-exchange-arrangements-and-exchange-restrictions-2023-541890
- **Emisor:** Fondo Monetario Internacional
- **Documentación y notas:** Informe anual sobre todos los miembros del FMI: clasificación de los regímenes cambiarios, operaciones en el mercado de divisas, restricciones a pagos corrientes y prácticas de tipos múltiples (artículo VIII), controles de capital y medidas macroprudenciales con efecto sobre los flujos. Edición 2023 publicada el 19/12/2024 (DOI: 10.5089/9798400260391.012); descripciones por país en AREAER Online.
- **Temática:** TFX-03 Organismos internacionales y estadísticas cambiarias (principal) · secundarias: TFX-02, TFX-09
- **Calidad Q:** 85 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 6/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Informe abierto; base AREAER Online con suscripción o acceso institucional
- **Ámbitos:** Regímenes cambiarios de facto, controles de capital, restricciones cambiarias
- **Motivo de inclusión y uso:** Referencia oficial para clasificar el régimen de cada divisa (flotación, banda, tipo fijo, caja de conversión) y sus controles. Uso: AS-EMAS, AS-EMLA y AS-EMEA para tratar divisas con controles (ARS, VND, EGP, NGN…) como ámbitos de régimen; CONTRA (AG-11) para el riesgo de convertibilidad.
- **Restricciones de uso:** Condiciones del FMI; citar edición.
- **Sesgos posibles:** Desfase de casi un año entre fecha de corte y publicación.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Revisiones periódicas de la metodología de clasificación.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «IMF Annual Report on Exchange Arrangements and Exchange Restrictions AREAER External Sector Report»; WebFetch: sí, edición 2023)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-03).

#### FXF-0054 · Q 85 (A) — Bank of England — resultados del Reino Unido en la Encuesta Trienal del BPI (2025)

- **Canal oficial (URL raíz):** https://www.bankofengland.co.uk/statistics/bis-survey/2025 (resumen: https://www.bankofengland.co.uk/-/media/boe/files/statistics/bis-survey/2025/summary-of-uk-survey-results-2025.pdf)
- **Emisor:** Bank of England
- **Documentación y notas:** Publicado el 30/09/2025: negociación media diaria en el Reino Unido de 4.745.000 millones de dólares en abril de 2025 (3.735.000 millones en 2022), 37,8 % del total mundial; primera plaza mundial; tablas resumen en XLSX.
- **Temática:** TFX-03 Organismos internacionales y estadísticas cambiarias (principal) · secundarias: TFX-05
- **Calidad Q:** 85 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 5/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Volumen del mercado de divisas de Londres por instrumento, divisa y contraparte
- **Motivo de inclusión y uso:** Detalle de la principal plaza del mercado de divisas. Uso: TR-PFV (AG-21) y AS-G10N para la liquidez y la concentración de la negociación.
- **Restricciones de uso:** Uso libre con atribución.
- **Sesgos posibles:** Mide por ubicación de la mesa, no por residencia del cliente.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «BIS effective exchange rate indices triennial survey 2025 foreign exchange turnover»; WebFetch: sí, página y resumen PDF)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-03).

#### FXF-0403 · Q 85 (A) — BPI — Global liquidity indicators (GLI): crédito en dólares, euros y yenes a no residentes

- **Canal oficial (URL raíz):** https://bis.org/statistics/about_banking_stats.htm (calendario y portal: https://www.bis.org/statistics/dataportal/banking.htm)
- **Emisor:** Banco de Pagos Internacionales (BPI)
- **Documentación y notas:** Indicadores del crédito a prestatarios no bancarios que combinan préstamos bancarios y emisión de valores de deuda internacionales, con foco en el crédito en moneda extranjera a no residentes en dólares, euros y yenes; documento metodológico enlazado. Publicación trimestral conjunta con las estadísticas bancarias de localización (29/10/2026: datos de fin de junio de 2026; 31/07/2026: fin de marzo).
- **Temática:** TFX-03 Organismos internacionales y estadísticas cambiarias (principal) · secundarias: TFX-04
- **Calidad Q:** 85 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 7/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Crédito global en dólares fuera de EE. UU.; financiación en divisas de emergentes; ciclo financiero global
- **Motivo de inclusión y uso:** Mide el «dólar global» del lado de la financiación, determinante del canal de riesgo del dólar. Uso: AS-ESTR (AG-08) y TR-BCM (AG-09) para el ciclo de liquidez en dólares; AS-EMLA y AS-EMEA para vulnerabilidad de divisas emergentes con alta deuda en dólares. Complementa la ficha general RF-0003.
- **Restricciones de uso:** Uso con atribución; citar trimestre de referencia y fecha de publicación.
- **Sesgos posibles:** Desfase de unos cuatro meses; no capta la deuda implícita en dólares de swaps y forwards de divisas.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «BIS locational banking statistics global liquidity indicators»; WebFetch: sí, páginas about_banking_stats y dataportal/banking)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-03).

#### RF-0007 · Q 85 (A) — IMF Data (Fondo Monetario Internacional)

- **Canal oficial:** data.imf.org
- **Documentación y notas:** Nota de verificación: el punto de acceso SDMX histórico (dataservices.imf.org) quedó retirado en 2025; el acceso vigente es el portal data.imf.org, comprobado vivo el 02/11/2026 (páginas de COFER e IRFCL).
- **Temática:** TFX-03 Organismos internacionales y estadísticas cambiarias (principal) · secundarias: TFX-04
- **Calidad Q:** 85 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 7/10
- **Nivel de fiabilidad en V2.4:** A
- **Tipología:** primaria
- **Motivo de inclusión:** Portal de datos del FMI que aloja las bases cambiarias y externas de referencia: COFER (composición por divisas de las reservas), IRFCL (reservas y liquidez en divisas), balanza de pagos y posición de inversión internacional, y estadísticas financieras internacionales (tipos de cambio oficiales). Uso: TR-BCM (AG-09) y Analistas de segmento para datos externos comparables; MOTOR (AG-13) para series de valoración.
- **Ámbitos:** Macroeconomía global; balanza de pagos; reservas; estabilidad financiera
- **Restricciones de uso:** Condiciones del portal del FMI; citar base, serie y edición (los datos de proyección cambian por edición)
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Sesgos posibles:** Las proyecciones WEO son estimaciones del FMI, no hechos: tratarlas como previsión
- **Cambios de propiedad o de metodología:** Ediciones WEO semestrales: anotar siempre la edición usada
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «IMF COFER currency composition of official foreign exchange reserves 2026» → data.imf.org; WebFetch: sí, https://data.imf.org/cofer y https://data.imf.org/en/Datasets/IRFCL)
- **Origen:** Reutilizada de F9 V3.2 (TF-01) en el Bloque A Forex V1.0 (2026-11-02).

#### FXF-0053 · Q 84 (A) — FMI — External Sector Report (evaluación de desequilibrios y tipos de cambio)

- **Canal oficial (URL raíz):** https://www.imf.org/en/publications/esr/issues/2026/07/30/external-sector-report-2026 (serie: https://www.imf.org/en/Publications/SPROLLs/external-sector-reports)
- **Emisor:** Fondo Monetario Internacional
- **Documentación y notas:** «2026 External Sector Report: Amid Rising Imbalances, the Case for Rebalancing» (30/07/2026): los saldos por cuenta corriente mundiales se ampliaron de nuevo en 2025, con China y EE. UU. como principales contribuyentes a los saldos excesivos; evaluación de 30 grandes economías con datos de 2025 y la metodología EBA (External Balance Assessment) revisada; anexos en línea por país.
- **Temática:** TFX-03 Organismos internacionales y estadísticas cambiarias (principal) · secundarias: TFX-04
- **Calidad Q:** 84 (A) — Primariedad 17/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** primaria (evaluación oficial con modelos propios)
- **Acceso:** Abierto (informe, capítulos y anexos en PDF)
- **Ámbitos:** Saldos exteriores, brechas de cuenta corriente y de tipo de cambio real (EBA), posición de inversión internacional
- **Motivo de inclusión y uso:** Estimación oficial de la desalineación del tipo de cambio real de las grandes divisas. Uso: AS-ESTR (AG-08, estrategia de valor) y MOTOR (AG-13, contraste de BEER/FEER propios); Analistas de segmento como opinión oficial de valoración.
- **Restricciones de uso:** Condiciones del FMI; citar edición.
- **Sesgos posibles:** Evaluación con juicio del personal del FMI y presiones diplomáticas; no es previsión de tipo de cambio.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Metodología EBA «refinada» en la edición de 2026.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «IMF External Sector Report 2026 external balance assessment»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-03).

#### FXF-0055 · Q 84 (A) — BPI — directorio de bancos centrales miembros

- **Canal oficial (URL raíz):** https://bis.org/about/member_cb.htm
- **Emisor:** Bank for International Settlements
- **Documentación y notas:** Lista de los 63 bancos centrales miembros del BPI con el enlace a su sitio oficial (consultada el 02/11/2026). Es la página índice que sustenta las URL oficiales de las fichas de TFX-02.
- **Temática:** TFX-03 Organismos internacionales y estadísticas cambiarias (principal) · secundarias: TFX-01, TFX-02
- **Calidad Q:** 84 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** primaria (directorio oficial)
- **Acceso:** Abierto
- **Ámbitos:** Localización de los canales oficiales de los bancos centrales del mundo
- **Motivo de inclusión y uso:** Punto de partida verificable para localizar el sitio oficial de cualquier banco central (lectura lateral frente a copias o sitios suplantados). Uso: BFA (AG-16) en el alta y el barrido de fichas de bancos centrales; TR-BCM (AG-09).
- **Restricciones de uso:** Uso libre con atribución.
- **Sesgos posibles:** Solo incluye a los miembros del BPI (no a todos los bancos centrales).
- **Historial de exactitud:** No aplicable (directorio).
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «BIS central bank websites directory list of central banks»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-03).

#### FXF-0056 · Q 83 (A) — Bank of Japan — resultados de Japón en la encuesta de bancos centrales sobre divisas y derivados

- **Canal oficial (URL raíz):** https://www.boj.or.jp/en/statistics/bis/deri/index.htm
- **Emisor:** Bank of Japan
- **Documentación y notas:** Contribución japonesa a la encuesta trienal del BPI (desde 1998): volumen (abril de 2025, publicado el 06/10/2025) e importes vivos (fin de junio de 2025, publicado el 10/09/2025), con avisos de cambios y correcciones.
- **Temática:** TFX-03 Organismos internacionales y estadísticas cambiarias (principal) · secundarias: TFX-05
- **Calidad Q:** 83 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 5/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Volumen del mercado de divisas en Japón por instrumento y divisa
- **Motivo de inclusión y uso:** Estructura del mercado del yen en su plaza local. Uso: AS-G10N (JPY) y TR-PFV (AG-21).
- **Restricciones de uso:** Uso libre con atribución.
- **Sesgos posibles:** Solo datos a nivel de país; frecuencia trienal.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «BIS effective exchange rate indices triennial survey 2025 foreign exchange turnover»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-03).

#### FXF-0057 · Q 83 (A) — Reserve Bank of Australia — resultados de Australia en la Encuesta Trienal del BPI (2025)

- **Canal oficial (URL raíz):** https://www.rba.gov.au/media-releases/2025/mr-25-28-tables.html
- **Emisor:** Reserve Bank of Australia
- **Documentación y notas:** Negociación de divisas en Australia de 201.000 millones de dólares diarios en abril de 2025 (150.000 millones en 2022; +34 %, máximo histórico); operaciones contra el dólar australiano ≈ 47 % del total; AUD/USD, 41 % (par más negociado de la plaza).
- **Temática:** TFX-03 Organismos internacionales y estadísticas cambiarias (principal) · secundarias: TFX-05
- **Calidad Q:** 83 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 5/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Volumen del mercado de divisas en Australia; liquidez del AUD
- **Motivo de inclusión y uso:** Liquidez de la principal divisa de materias primas en su plaza local. Uso: AS-G10M (AG-04) y TR-PFV (AG-21).
- **Restricciones de uso:** Uso libre con atribución.
- **Sesgos posibles:** Fotografía trienal.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «BIS effective exchange rate indices triennial survey 2025 foreign exchange turnover»; WebFetch: sí, tablas del comunicado)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-03).

#### RF-0024 · Q 83 (A) — FMI — World Economic Outlook y blog del FMI

- **Canal oficial (URL raíz):** https://www.imf.org/en/publications/weo (edición vigente: https://www.imf.org/en/publications/weo/issues/2026/10/13/world-economic-outlook-october-2026)
- **Emisor:** Fondo Monetario Internacional
- **Temática:** TFX-03 Organismos internacionales y estadísticas cambiarias (principal) · secundarias: TFX-09
- **Calidad Q:** 83 (A) — Primariedad 16/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria (previsiones propias del organismo)
- **Acceso:** Abierto
- **Ámbitos:** Previsiones macro mundiales y por país (abril y octubre, con actualizaciones en enero y julio); base de datos del WEO
- **Motivo de inclusión y uso:** Escenario central de referencia del sector oficial (WEO de octubre de 2026, «Resilience Under Strain, Urgent Choices»: crecimiento mundial 3,1 % en 2026 y 3,4 % en 2027); la base de datos del WEO publica además saldos por cuenta corriente, inflación y PIB en PPA por país. Uso: TR-BCM (AG-09) para el régimen macro global; AS-ESTR (AG-08) y MOTOR (AG-13) para insumos de modelos de valoración (BEER, FEER).
- **Sesgos y cautelas:** Previsiones, no hechos; sesgo histórico hacia la continuidad; el blog del FMI expresa opiniones del personal.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «IMF World Economic Outlook October 2026»; WebFetch: sí)
- **Origen:** Reutilizada de F9 V3.2 (TF-01) en el Bloque A Forex V1.0 (2026-11-02).

#### FXF-0058 · Q 82 (A) — Banco Mundial — International Comparison Program (ICP) y fuentes de paridades de poder adquisitivo

- **Canal oficial (URL raíz):** https://www.worldbank.org/en/programs/icp/brief/Sources_of_PPPs
- **Emisor:** Banco Mundial (coordinador mundial del ICP bajo la Comisión de Estadística de la ONU)
- **Documentación y notas:** Nota que compara las fuentes de PPA: ICP (única que recopila precios nacionales; 44 categorías de gasto en los años de referencia), programa anual Eurostat-OCDE, WEO del FMI (extrapola las PPA del ICP con deflactores y publica previsiones), Penn World Table (Groningen y UC Davis; series desde 1950) y CIA World Factbook. En la fecha de la nota (09/2023) la última referencia publicada era 2017 y la de 2021 se esperaba para 2024.
- **Temática:** TFX-03 Organismos internacionales y estadísticas cambiarias (principal) · secundarias: —
- **Calidad Q:** 82 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 4/10 · Acceso 10/10
- **Tipología:** primaria (organismo que coordina la estadística)
- **Acceso:** Abierto
- **Ámbitos:** Paridades de poder adquisitivo y niveles de precios comparados
- **Motivo de inclusión y uso:** Guía oficial para elegir la serie de PPA adecuada y no mezclar fuentes. Uso: MOTOR (AG-13, valoración PPA) y AS-ESTR (AG-08, estrategia de valor).
- **Restricciones de uso:** Licencia del Banco Mundial (por lo general CC BY 4.0).
- **Sesgos posibles:** Las PPA de referencia se revisan en cada ronda; la nota es de 2023 (comprobar la ronda vigente).
- **Historial de exactitud:** No aplicable.
- **Cambios de propiedad o de metodología:** Nueva ronda ICP 2021 posterior a la nota.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «OECD purchasing power parities data World Bank International Comparison Program Penn World Table»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-03).

#### RF-0201 · Q 82 (A) — FRASER (Federal Reserve Archival System for Economic Research)

- **Canal oficial (URL raíz):** https://fraser.stlouisfed.org/
- **Emisor:** Federal Reserve Bank of St. Louis
- **Temática:** TFX-03 Organismos internacionales y estadísticas cambiarias (principal) · secundarias: TFX-10
- **Calidad Q:** 82 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 14/15 · Independencia 10/10 · Actualidad 6/10 · Acceso 10/10
- **Tipología:** primaria (documentos históricos digitalizados)
- **Acceso:** Abierto (búsqueda a texto completo, API REST y OAI-PMH)
- **Ámbitos:** Historia financiera, económica y bancaria de EE. UU.: publicaciones estadísticas históricas, documentos de la Fed, colecciones de archivo
- **Motivo de inclusión y uso:** Archivo digital de documentos y estadísticas históricas de la Reserva Federal (p. ej., ediciones antiguas de boletines con series de tipos de cambio y documentos del sistema de Bretton Woods). Uso: MOTOR (AG-13) y AS-ESTR (AG-08) para reconstruir series largas y analogías de regímenes cambiarios y crisis.
- **Sesgos y cautelas:** Cobertura centrada en EE. UU.; fondos históricos, no datos de actualidad.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ALFRED Archival Federal Reserve Economic Data vintage St. Louis Fed»; WebFetch: sí)
- **Origen:** Reutilizada de F9 V3.2 (TF-01) en el Bloque A Forex V1.0 (2026-11-02).

#### FXF-0059 · Q 78 (B) — HKMA / Gobierno de Hong Kong — resultados de Hong Kong en la Encuesta Trienal del BPI (2025)

- **Canal oficial (URL raíz):** https://www.info.gov.hk/gia/general/202509/30/P2025093000530.htm
- **Emisor:** Hong Kong Monetary Authority (comunicado del Gobierno de la RAE de Hong Kong)
- **Documentación y notas:** Comunicado del 30/09/2025 «Results of 2025 BIS Triennial Survey of Foreign Exchange and OTC Derivatives Markets Turnover» (versión p: https://www.info.gov.hk/gia/general/202509/30/P2025093000530p.htm). La carga directa de la página devolvió un control antibots; contenido confirmado por título en los resultados.
- **Temática:** TFX-03 Organismos internacionales y estadísticas cambiarias (principal) · secundarias: TFX-05
- **Calidad Q:** 78 (B) — Primariedad 20/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 14/15 · Independencia 9/10 · Actualidad 5/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Volumen del mercado de divisas en Hong Kong (HKD y renminbi offshore)
- **Motivo de inclusión y uso:** Plaza clave del renminbi offshore (CNH) y del HKD. Uso: AS-EMAS (AG-05) y TR-PFV (AG-21).
- **Restricciones de uso:** Uso con atribución.
- **Sesgos posibles:** Fotografía trienal.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «BIS effective exchange rate indices triennial survey 2025 foreign exchange turnover»; WebFetch: intentado, bloqueado por control antibots)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-03).

#### FXF-0060 · Q 76 (B) — Banco Central de Chile — resultados de Chile en la Encuesta Trienal del BPI (2025)

- **Canal oficial (URL raíz):** https://www.bcentral.cl/en/content/-/details/prensa/nota-de-prensa/resultados-encuesta-global-bis
- **Emisor:** Banco Central de Chile
- **Documentación y notas:** Nota de prensa «BIS publishes results of global survey on FX and interest rate derivatives markets», con la participación chilena en la encuesta de 2025.
- **Temática:** TFX-03 Organismos internacionales y estadísticas cambiarias (principal) · secundarias: TFX-02
- **Calidad Q:** 76 (B) — Primariedad 19/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 14/15 · Independencia 9/10 · Actualidad 5/10 · Acceso 7/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Volumen del mercado cambiario chileno (CLP)
- **Motivo de inclusión y uso:** Profundidad del mercado del peso chileno frente a otras divisas latinoamericanas. Uso: AS-EMLA (AG-06).
- **Restricciones de uso:** Uso con atribución.
- **Sesgos posibles:** Fotografía trienal.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «BIS effective exchange rate indices triennial survey 2025 foreign exchange turnover»; WebFetch: no)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-03).

#### FXF-0061 · Q 71 (B) — Banco Mundial — Data Blog: «Purchasing power parities (PPPs): new overview of available datasets and their differences»

- **Canal oficial (URL raíz):** https://blogs.worldbank.org/en/opendata/purchasing-power-parities-ppps-new-overview-available-datasets-and-their-differences
- **Emisor:** Banco Mundial (equipo de datos abiertos)
- **Documentación y notas:** Entrada divulgativa que presenta la comparación de conjuntos de datos de PPA (complemento de FXF-0058).
- **Temática:** TFX-03 Organismos internacionales y estadísticas cambiarias (principal) · secundarias: TFX-10
- **Calidad Q:** 71 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 14/15 · Independencia 9/10 · Actualidad 4/10 · Acceso 9/10
- **Tipología:** secundaria cualificada (divulgación de organismo oficial)
- **Acceso:** Abierto
- **Ámbitos:** Paridades de poder adquisitivo
- **Motivo de inclusión y uso:** Explicación accesible de las diferencias entre fuentes de PPA. Uso: MOTOR (AG-13) y AS-ESTR (AG-08) como apoyo metodológico.
- **Restricciones de uso:** Uso con atribución.
- **Sesgos posibles:** Divulgativo; no sustituye a la serie primaria.
- **Historial de exactitud:** No aplicable.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «OECD purchasing power parities data World Bank International Comparison Program Penn World Table»; WebFetch: no)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-03).

#### FXF-0062 · Q 70 (B) — DBnomics — redistribución abierta de bases del FMI, BPI y bancos centrales (COFER, IRFCL…)

- **Canal oficial (URL raíz):** https://db.nomics.world/IMF/COFER (también: https://db.nomics.world/IMF/IRFCL)
- **Emisor:** DBnomics (plataforma de datos abiertos de CEPREMAP)
- **Documentación y notas:** Agregador que redistribuye con API unificada bases oficiales (p. ej., COFER e IRFCL del FMI).
- **Temática:** TFX-03 Organismos internacionales y estadísticas cambiarias (principal) · secundarias: TFX-04
- **Calidad Q:** 70 (B) — Primariedad 8/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 11/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** secundaria (redistribución de datos oficiales)
- **Acceso:** Abierto (web y API)
- **Ámbitos:** Acceso programático a series oficiales de reservas, balanza de pagos y tipos de cambio
- **Motivo de inclusión y uso:** Herramienta de descarga reproducible para el MOTOR (AG-13) cuando la API del emisor original no basta. Regla F9-b: citar siempre la fuente original (FXF-0051, FXF-0072).
- **Restricciones de uso:** Licencias de los emisores originales.
- **Sesgos posibles:** Posible desfase frente a la fuente original.
- **Historial de exactitud:** No aplicable.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsquedas web: «IMF COFER currency composition of official foreign exchange reserves 2026» e «IMF International Reserves and Foreign Currency Liquidity data template»; WebFetch: no)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-03).

## TFX-04 Balanza de pagos, flujos de capital y reservas

#### RF-0023 · Q 89 (A) — U.S. Bureau of Economic Analysis (BEA)

- **Canal oficial (URL raíz):** https://www.bea.gov/ (renta y ahorro: https://www.bea.gov/taxonomy/term/1071)
- **Emisor:** U.S. Department of Commerce
- **Temática:** TFX-04 Balanza de pagos, flujos de capital y reservas (principal) · secundarias: TFX-03
- **Calidad Q:** 89 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** PIB, renta y gasto personal (PCE), tasa de ahorro, balanza de pagos, renta estatal de EE. UU.
- **Motivo de inclusión y uso:** Compilador oficial de las transacciones internacionales de EE. UU. (balanza por cuenta corriente y financiera) y de la posición de inversión internacional, además de las cuentas nacionales. Uso: TR-BCM (AG-09) y AS-ESTR (AG-08) para el déficit exterior y la financiación del dólar; MOTOR (AG-13) para insumos de modelos de equilibrio (FEER/BEER).
- **Sesgos y cautelas:** Revisiones sustanciales del PIB entre estimaciones; calendario reprogramado en 2025–2026 (verificar fecha en el aviso de la BEA).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «U.S. Bureau of Economic Analysis GDP personal income outlays bea.gov»; WebFetch: sí)
- **Origen:** Reutilizada de F9 V3.2 (TF-01) en el Bloque A Forex V1.0 (2026-11-02).

#### FXF-0071 · Q 88 (A) — Ministerio de Hacienda de Japón — operaciones de intervención en divisas

- **Canal oficial (URL raíz):** https://www.mof.go.jp/english/policy/international_policy/reference/feio/ (detalle trimestral de abril–junio de 2026: https://www.mof.go.jp/english/policy/international_policy/reference/feio/quarter/2026_2Qe.html · total mensual, p. ej.: https://www.mof.go.jp/english/policy/international_policy/reference/feio/monthly/20260130e.html)
- **Emisor:** Ministry of Finance Japan (autoridad responsable de la intervención; el BoJ ejecuta como agente)
- **Documentación y notas:** El MOF publica a fin de mes el total del periodo y, trimestralmente, el detalle diario (fecha, importe y par). Abril–junio de 2026: 11.734.900 millones de yenes en tres días (30/04: 6.278.700 M; 04/05: 780.200 M; 06/05: 4.675.900 M), todas ventas de dólares contra yenes.
- **Temática:** TFX-04 Balanza de pagos, flujos de capital y reservas (principal) · secundarias: TFX-01
- **Calidad Q:** 88 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Intervención oficial en USD/JPY (fechas, importes, sentido)
- **Motivo de inclusión y uso:** Dato oficial e inequívoco de intervención en la segunda divisa más negociada. Uso: AS-G10N (AG-03, USD/JPY), CONTRA (AG-11) para el riesgo de intervención en opciones contra el yen, TR-BCM (AG-09) y EVAL (AG-20) para estudiar episodios.
- **Restricciones de uso:** Uso libre con atribución.
- **Sesgos posibles:** El total mensual se conoce a fin de mes; el detalle diario, con hasta tres meses de desfase.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Japan Ministry of Finance foreign exchange intervention operations results»; WebFetch: sí, página trimestral 2026 T2)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-04).

#### FXF-0074 · Q 87 (A) — BCE — balanza de pagos mensual de la zona del euro (comunicado)

- **Canal oficial (URL raíz):** https://www.ecb.europa.eu/press/stats/bop/2026/html/ecb.bp260417~8cf2910734.es.html (comunicado de febrero de 2026, publicado el 17/04/2026)
- **Emisor:** Banco Central Europeo
- **Documentación y notas:** Comunicado mensual (cuenta corriente, cuenta financiera, inversión de cartera de residentes y no residentes). Febrero de 2026: superávit corriente de 25.000 M€ (289.000 M€ en doce meses, 1,8 % del PIB); compras netas de valores de la zona del euro por no residentes de 1,013 billones de € en doce meses (deuda 549.000 M€; acciones 464.000 M€).
- **Temática:** TFX-04 Balanza de pagos, flujos de capital y reservas (principal) · secundarias: TFX-01
- **Calidad Q:** 87 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto (comunicado en varias lenguas; series en el portal de datos del BCE)
- **Ámbitos:** Cuenta corriente y flujos de cartera de la zona del euro
- **Motivo de inclusión y uso:** Dato primario de los flujos que sostienen o presionan al euro. Uso: TR-BCM (AG-09) y TR-PFV (AG-21) para los flujos de cartera hacia la zona del euro; AS-G10N (EUR/USD).
- **Restricciones de uso:** Uso libre con atribución.
- **Sesgos posibles:** Desfase de unas siete semanas; revisiones posteriores.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ECB euro area monthly balance of payments press release portfolio investment»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-04).

#### RF-0018 · Q 87 (A) — Banco de España (informes, boletín económico, estadísticas)

- **Canal oficial (URL raíz):** https://www.bde.es/ (Boletín Económico: https://www.bde.es/bde/es/secciones/informes/analisis-economico-e-investigacion/boletin-economico/ · Boletín Estadístico: https://www.bde.es/wbe/es/publicaciones/informacion-estadistica/boletin-estadistico/)
- **Emisor:** Banco de España
- **Temática:** TFX-04 Balanza de pagos, flujos de capital y reservas (principal) · secundarias: TFX-01
- **Calidad Q:** 87 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Economía española; proyecciones macroeconómicas; Informe Anual; estabilidad financiera; Boletín Estadístico; repositorio institucional (repositorio.bde.es)
- **Motivo de inclusión y uso:** Compilador oficial de la balanza de pagos y la posición de inversión internacional de España y banco central del Eurosistema (Boletín Estadístico, Boletín Económico). Uso: TR-BCM (AG-09) para la contribución española a la balanza del área del euro y fuente europea de contraste; AS-G10N (EUR).
- **Sesgos y cautelas:** Perspectiva institucional del Eurosistema; algunos enlaces internos del portal (p. ej., «Notas Económicas») apuntaban a anclas rotas en la fecha de consulta.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Banco de España Boletín Económico informes estadísticas bde.es»; WebFetch: sí)
- **Origen:** Reutilizada de F9 V3.2 (TF-01) en el Bloque A Forex V1.0 (2026-11-02).

#### FXF-0070 · Q 86 (A) — Tesoro de EE. UU. — informe semestral «Macroeconomic and Foreign Exchange Policies of Major Trading Partners of the United States»

- **Canal oficial (URL raíz):** https://home.treasury.gov/policy-issues/international/macroeconomic-and-foreign-exchange-policies-of-major-trading-partners-of-the-united-states (informe de julio de 2026: https://home.treasury.gov/system/files/206/July-2026-FX-Report.pdf · enero de 2026: https://home.treasury.gov/system/files/136/January-2026-FX-Report.pdf)
- **Emisor:** U.S. Department of the Treasury
- **Documentación y notas:** Informe semestral al Congreso (leyes de 1988 y 2015). Criterios de 2015: superávit bilateral ≥ 15.000 M$, superávit corriente ≥ 3 % del PIB, compras netas de divisas en ≥ 8 de 12 meses por ≥ 2 % del PIB. Julio de 2026: ningún manipulador ni análisis reforzado; lista de seguimiento de diez economías (China, Japón, Corea, Taiwán, Tailandia, Singapur, Vietnam, Alemania, Irlanda y Suiza); señala la falta de transparencia cambiaria de China.
- **Temática:** TFX-04 Balanza de pagos, flujos de capital y reservas (principal) · secundarias: TFX-09, TFX-02
- **Calidad Q:** 86 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria (evaluación oficial con estimaciones de intervención)
- **Acceso:** Abierto (PDF)
- **Ámbitos:** Intervención cambiaria estimada, saldos exteriores y riesgo de designación como manipulador
- **Motivo de inclusión y uso:** Fuente oficial del riesgo político estadounidense sobre las divisas de sus socios (presión para apreciar). Uso: AS-EMAS (AG-05: CNY, KRW, TWD, SGD, THB, VND), AS-G10N (JPY, CHF), CONTRA (AG-11) y TR-BCM (AG-09).
- **Restricciones de uso:** Uso libre (documento público federal).
- **Sesgos posibles:** Documento con dimensión política y comercial; las estimaciones de intervención son del Tesoro.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Umbrales revisables por el Tesoro.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Treasury report Macroeconomic and Foreign Exchange Policies of Major Trading Partners of the United States 2026»; WebFetch: sí, página índice y PDF de julio de 2026)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-04).

#### FXF-0072 · Q 86 (A) — FMI — International Reserves and Foreign Currency Liquidity (IRFCL)

- **Canal oficial (URL raíz):** https://data.imf.org/en/Datasets/IRFCL (plantilla de declaración: https://data.imf.org/Datasets/IRFCL/Reporting-Template)
- **Emisor:** Fondo Monetario Internacional (redifusión de datos de los países miembros)
- **Documentación y notas:** Plantilla común en dólares de reservas oficiales, otros activos en divisas de las autoridades y obligaciones a corto plazo en divisas que pueden drenarlas; los suscriptores de las NEDD (SDDS) la difunden mensualmente con un desfase máximo de un mes desde 2000. El FMI advierte que redifundir no avala la calidad de los datos.
- **Temática:** TFX-04 Balanza de pagos, flujos de capital y reservas (principal) · secundarias: TFX-03
- **Calidad Q:** 86 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** primaria (datos oficiales en formato común)
- **Acceso:** Abierto
- **Ámbitos:** Reservas brutas, posiciones a plazo en divisas (*forwards* y *swaps* del banco central), drenajes previstos y contingentes
- **Motivo de inclusión y uso:** Permite estimar las reservas netas y la «posición corta a plazo» de los bancos centrales que intervienen con derivados (p. ej., Turquía, India). Uso: AS-EMAS, AS-EMLA y AS-EMEA; CONTRA (AG-11) para la capacidad de defensa de una divisa.
- **Restricciones de uso:** Condiciones del FMI; citar país y mes.
- **Sesgos posibles:** Calidad desigual por país; participación voluntaria.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Historia de la plantilla documentada en el portal.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «IMF International Reserves and Foreign Currency Liquidity data template»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-04).

#### FXF-0410 · Q 86 (A) — FMI — Portfolio Investment Positions by Counterpart Economy (PIP, antes CPIS)

- **Canal oficial (URL raíz):** https://data.imf.org/en/datasets/IMF.STA:PIP (descripción del antiguo CPIS: https://datahelp.imf.org/knowledgebase/articles/505725-what-is-the-coordinated-portfolio-investment-surve)
- **Emisor:** Fondo Monetario Internacional (Departamento de Estadística)
- **Documentación y notas:** Ejercicio voluntario bajo los auspicios del FMI: las economías participantes declaran sus tenencias de valores de inversión de cartera (participaciones de capital y en fondos, deuda a largo y a corto plazo) por economía emisora. Disponibilidad a 07/10/2026 con datos de referencia de diciembre de 2025; panel «Foreign Portfolio Investments Breakdown» y nota «Valuation Effects Drive the Increase in Cross-Border Portfolio Investment Assets».
- **Temática:** TFX-04 Balanza de pagos, flujos de capital y reservas (principal) · secundarias: TFX-03
- **Calidad Q:** 86 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 7/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Matriz bilateral de tenencias de cartera; exposición de inversores a activos de cada país; sesgo doméstico; flujos de cartera de largo plazo
- **Motivo de inclusión y uso:** Base de quién tiene los activos de cartera de quién: identifica divisas con base inversora extranjera concentrada y riesgo de repatriación. Uso: AS-ESTR (AG-08) para posicionamiento estructural; AS-G10N (JPY, CHF, EUR) para el riesgo de repatriación; AS-EMLA y AS-EMEA para dependencia de inversores no residentes.
- **Restricciones de uso:** Uso con atribución; citar fecha de referencia.
- **Sesgos posibles:** Participación voluntaria; posiciones a valor de mercado (efectos de valoración); asignación por residencia del emisor (centros financieros distorsionan).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Rebautizado de CPIS a PIP en el portal de datos del FMI.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «IMF Coordinated Portfolio Investment Survey CPIS data»; WebFetch: sí, página del conjunto PIP)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-04).

#### FXF-0412 · Q 86 (A) — BPI — Estadísticas bancarias de localización (LBS) por divisa

- **Canal oficial (URL raíz):** https://bis.org/statistics/about_banking_stats.htm (portal y calendario: https://www.bis.org/statistics/dataportal/banking.htm)
- **Emisor:** Banco de Pagos Internacionales (BPI)
- **Documentación y notas:** Activos y pasivos de los bancos según su localización geográfica y por divisa, incluidas las operaciones intragrupo; documentos de cobertura y de población informante enlazados. Publicación trimestral (29/10/2026: fin de junio de 2026). Complemento: estadísticas bancarias consolidadas (CBS) de exposición por país.
- **Temática:** TFX-04 Balanza de pagos, flujos de capital y reservas (principal) · secundarias: TFX-03
- **Calidad Q:** 86 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 7/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Flujos bancarios transfronterizos por divisa y contraparte; financiación en dólares, euros y yenes; centros financieros
- **Motivo de inclusión y uso:** Fuente de referencia de los flujos de capital bancarios, el componente más volátil de la cuenta financiera. Uso: AS-ESTR (AG-08) para retiradas de crédito transfronterizo; AS-EMLA y AS-EMEA para paradas súbitas; TR-PFV (AG-21) para financiación en divisas. Complementa la ficha general RF-0003.
- **Restricciones de uso:** Uso con atribución; citar trimestre de referencia.
- **Sesgos posibles:** Desfase de unos cuatro meses; variaciones de posiciones afectadas por tipo de cambio (usar los flujos ajustados por el BPI).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «BIS locational banking statistics global liquidity indicators»; WebFetch: sí, páginas about_banking_stats y dataportal/banking)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-04).

#### FXF-0417 · Q 86 (A) — Ministerio de Hacienda de Japón — International Reserves/Foreign Currency Liquidity (mensual)

- **Canal oficial (URL raíz):** https://www.mof.go.jp/english/policy/international_policy/reference/official_reserve_assets/e0803.html (fin de marzo de 2026, publicado el 07/04/2026)
- **Emisor:** Ministry of Finance Japan
- **Documentación y notas:** Plantilla IRFCL completa del FMI. Fin de marzo de 2026: activos de reserva 1.374.734 M USD (−35.965 M frente a febrero); reservas en divisas 1.161.819 M (valores 1.000.090 M; depósitos 161.729 M, casi todos en bancos centrales extranjeros y el BPI); posición en el FMI 11.137 M; DEG 60.447 M; oro 125.343 M; posiciones largas a plazo contra yenes por 20.000 M (drenajes predeterminados).
- **Temática:** TFX-04 Balanza de pagos, flujos de capital y reservas (principal) · secundarias: TFX-01
- **Calidad Q:** 86 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 8/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Reservas de Japón (segundo mayor tenedor); capacidad de intervención; composición por instrumento y divisas de la cesta DEG
- **Motivo de inclusión y uso:** Mide la munición disponible para intervenir en USD/JPY y los efectos de valoración y ventas de bonos del Tesoro. Uso: AS-G10N (USD/JPY) y TR-BCM (AG-09) junto con la ficha de intervenciones FXF-0071; CONTRA (AG-11) para el riesgo de intervención.
- **Restricciones de uso:** Uso libre con atribución.
- **Sesgos posibles:** Las variaciones mezclan intervención, valoración e intereses: cruzar con FXF-0071.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Japan Ministry of Finance international reserves monthly foreign reserves»; WebFetch: sí, página del 07/04/2026)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-04).

#### RF-0344 · Q 86 (A) — Tesoro de EE. UU. — Treasury International Capital (TIC)

- **Canal oficial (URL raíz):** https://home.treasury.gov/archives-of-tic-monthly-data-releases
- **Emisor:** U.S. Department of the Treasury
- **Documentación y notas:** Notas mensuales de flujos de capital transfronterizos (p. ej., nota de 16/09/2026 sobre julio de 2026: entrada neta de 83.700 M$, 73.500 M$ privados y 10.200 M$ oficiales; siguiente 16/10/2026); archivo histórico de publicaciones.
- **Temática:** TFX-04 Balanza de pagos, flujos de capital y reservas (principal) · secundarias: TFX-05
- **Calidad Q:** 86 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 7/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Compras extranjeras de valores de EE. UU.; tenencias de Treasuries por país
- **Motivo de inclusión y uso:** Flujos de capital extranjero hacia y desde activos estadounidenses, con desglose privado/oficial y tenencias de Treasuries por país. Uso: TR-PFV (AG-21) para la demanda extranjera de activos en dólares y los flujos oficiales (gestión de reservas, posible intervención); AS-EMAS y AS-G10N para tenencias de Japón y China.
- **Restricciones de uso:** Uso libre; citar mes de referencia.
- **Sesgos y cautelas:** Desfase de unos dos meses y medio; atribución por país de custodia.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Treasury International Capital TIC system monthly data»; WebFetch: sí, nota de septiembre de 2026)
- **Origen:** Reutilizada de F9 V3.2 (TF-06) en el Bloque A Forex V1.0 (2026-11-02).

#### RF-0612 · Q 86 (A) — Federal Reserve Board — H.4.1 Factors Affecting Reserve Balances (balance de la Fed)

- **Canal oficial (URL raíz):** https://www.federalreserve.gov/releases/h41/
- **Emisor:** Board of Governors of the Federal Reserve System
- **Temática:** TFX-04 Balanza de pagos, flujos de capital y reservas (principal) · secundarias: TFX-01
- **Calidad Q:** 86 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria (estado contable semanal oficial)
- **Acceso:** Abierto (cada jueves, hacia las 16:30 ET)
- **Ámbitos:** Factores que aportan y absorben reservas: valores en cartera, préstamos y facilidades, reverse repos (incluido el ON RRP), cuenta general del Tesoro (TGA), billetes; saldo de reservas bancarias. Última actualización vista: 29/10/2026
- **Motivo de inclusión y uso:** Medida semanal de la liquidez en dólares y, en sus partidas de memoria, de los valores custodiados por la Fed de Nueva York para cuentas oficiales extranjeras e internacionales, indicador semanal de la gestión de reservas en dólares por bancos centrales extranjeros. Uso: TR-PFV (AG-21) y TR-BCM (AG-09) para detectar ventas oficiales de Treasuries (posible defensa de divisas) y condiciones de liquidez en dólares.
- **Sesgos y cautelas:** Datos de miércoles y medias semanales: la volatilidad intrasemanal (TGA, fechas fiscales) no se ve; la página índice no describe las tablas (consultar la publicación).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «federalreserve.gov releases H.15 selected interest rates commercial paper rates» → enlace desde la página H.15; WebFetch: sí)
- **Origen:** Reutilizada de F9 V3.2 (TF-18) en el Bloque A Forex V1.0 (2026-11-02).

#### FXF-0416 · Q 85 (A) — Office for National Statistics (ONS) — Balance of payments, UK (trimestral)

- **Canal oficial (URL raíz):** https://www.ons.gov.uk/economy/nationalaccounts/balanceofpayments/datasets/balanceofpayments (publicación de abril–junio de 2026: https://www.ons.gov.uk/releases/balanceofpaymentsukapriltojune2026timeseries)
- **Emisor:** Office for National Statistics (Reino Unido)
- **Documentación y notas:** Serie PNBP: cuenta corriente, transferencias de capital, transacciones y saldos de activos y pasivos exteriores del Reino Unido (CSV, XLSX). Última publicación 30/09/2026 (2026T2); próxima 22/12/2026.
- **Temática:** TFX-04 Balanza de pagos, flujos de capital y reservas (principal) · secundarias: —
- **Calidad Q:** 85 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 6/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Cuenta corriente del Reino Unido; financiación exterior; posición de inversión internacional
- **Motivo de inclusión y uso:** Dato oficial del déficit exterior británico, argumento recurrente de la libra («dependencia de la amabilidad de extraños»). Uso: AS-G10N (GBP) y AS-ESTR (AG-08) para la financiación de la cuenta corriente; MOTOR (AG-13) para modelos de balance externo.
- **Restricciones de uso:** Open Government Licence; citar publicación y fecha.
- **Sesgos posibles:** Revisiones importantes de trimestres anteriores; desfase de unos tres meses.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ONS UK balance of payments quarterly current account»; WebFetch: sí, página del conjunto PNBP y de la publicación de 2026T2)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-04).

#### FXF-0411 · Q 84 (A) — FMI — Direct Investment Positions by Counterpart Economy (DIP, antes CDIS)

- **Canal oficial (URL raíz):** https://data.imf.org/en/datasets/IMF.STA%3ADIP (acceso corto: https://data.imf.org/cdis)
- **Emisor:** Fondo Monetario Internacional (Departamento de Estadística)
- **Documentación y notas:** Posiciones de inversión extranjera directa entrantes (por instrumento y economía del inversor inmediato) y salientes (por economía de destino inmediata), con capital y deuda netos por separado y datos espejo para economías no participantes. Tablas de disponibilidad del 10/12/2025; panel DIP.
- **Temática:** TFX-04 Balanza de pagos, flujos de capital y reservas (principal) · secundarias: TFX-03
- **Calidad Q:** 84 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 5/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Stock bilateral de IED; financiación estable de la cuenta corriente; dependencia de inversores directos
- **Motivo de inclusión y uso:** Permite valorar la calidad de la financiación exterior (IED frente a cartera) de cada divisa. Uso: AS-EMLA y AS-EMEA para resiliencia de divisas con déficit por cuenta corriente; MOTOR (AG-13) como insumo de vulnerabilidad externa.
- **Restricciones de uso:** Uso con atribución.
- **Sesgos posibles:** Contraparte inmediata, no última (Países Bajos, Luxemburgo, Irlanda inflan posiciones); periodicidad anual con desfase.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Rebautizado de CDIS a DIP en el portal de datos del FMI.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «IMF Coordinated Direct Investment Survey CDIS direct investment positions by counterpart economy»; WebFetch: sí, página del conjunto DIP)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-04).

#### RF-0613 · Q 84 (A) — Federal Reserve Bank of New York — Central Bank Liquidity Swap Operations (líneas swap en dólares)

- **Canal oficial (URL raíz):** https://www.newyorkfed.org/markets/desk-operations/central-bank-liquidity-swap-operations
- **Emisor:** Federal Reserve Bank of New York, Open Market Trading Desk
- **Temática:** TFX-04 Balanza de pagos, flujos de capital y reservas (principal) · secundarias: TFX-01
- **Calidad Q:** 84 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 8/10
- **Tipología:** primaria (resultados de operaciones oficiales)
- **Acceso:** Abierto (resultados semanales cuando hay operaciones; API de datos de mercados)
- **Ámbitos:** Uso de las líneas swap de liquidez en dólares por bancos centrales extranjeros (enlaces a resultados del BoE, BoJ, BCE y BNS), incluidas operaciones de prueba de pequeño importe
- **Motivo de inclusión y uso:** Indicador de escasez de dólares fuera de EE. UU.: la demanda en las subastas de dólares de otros bancos centrales sube en episodios de tensión (2008, 2020). Uso: TR-PFV (AG-21) junto con la base cruzada de divisas; TR-BCM (AG-09) para el riesgo de financiación en dólares; AS-ESTR (AG-08) para el dólar como refugio.
- **Sesgos y cautelas:** La página no muestra saldos: hay que ir a los resultados de cada banco central o a la API; las operaciones de prueba no reflejan demanda real.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «New York Fed reference rates SOFR EFFR OBFR TGCR BGCR» → enlace desde la página de tipos de referencia; WebFetch: sí)
- **Origen:** Reutilizada de F9 V3.2 (TF-18) en el Bloque A Forex V1.0 (2026-11-02).

#### FXF-0075 · Q 83 (A) — Tesoro de EE. UU. — U.S. International Reserve Position (semanal)

- **Canal oficial (URL raíz):** https://home.treasury.gov/data/us-international-reserve-position
- **Emisor:** U.S. Department of the Treasury
- **Documentación y notas:** Publicación semanal de los activos de reserva de EE. UU.: divisas (repartidas entre el Exchange Stabilization Fund y la cartera SOMA de la Fed), DEG, posición de reserva en el FMI y oro. Releases desde 2017 (último listado: 23/10/2026).
- **Temática:** TFX-04 Balanza de pagos, flujos de capital y reservas (principal) · secundarias: TFX-01
- **Calidad Q:** 83 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 7/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Reservas oficiales de EE. UU.; recursos del ESF para intervención
- **Motivo de inclusión y uso:** Detectar intervención estadounidense (rara) y la capacidad del ESF. Uso: TR-BCM (AG-09) y AS-ESTR (AG-08, dólar amplio).
- **Restricciones de uso:** Uso libre.
- **Sesgos posibles:** Cambios semanales dominados por valoración.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «SAFE State Administration of Foreign Exchange official reserve assets monthly data»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-04).

#### FXF-0415 · Q 83 (A) — Banco Mundial — International Debt Statistics (IDS)

- **Canal oficial (URL raíz):** https://datacatalog.worldbank.org/search/dataset/0038015/international-debt-statistics (productos del International Debt Report: https://www.worldbank.org/en/programs/debt-statistics/idr/products · guía metodológica IDS 2025: https://thedocs.worldbank.org/en/doc/6e72b0ded996306fa01f5db7a0c38b19-0050052021/related/IDS-2025-User-Guide-and-Methodology.pdf)
- **Emisor:** Banco Mundial (Debtor Reporting System, DRS, creado en 1951)
- **Documentación y notas:** Deuda externa de países de renta baja y media, anual, 1970–2032 (incluye proyecciones de servicio de la deuda); sucesora de Global Development Finance y World Debt Tables; licencia CC BY 4.0; metadatos actualizados el 14/05/2026 (versión 14).
- **Temática:** TFX-04 Balanza de pagos, flujos de capital y reservas (principal) · secundarias: TFX-09
- **Calidad Q:** 83 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 5/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Deuda externa por acreedor, moneda y plazo; calendario de amortizaciones; flujos netos de deuda a emergentes y frontera
- **Motivo de inclusión y uso:** Base oficial de la deuda externa y su servicio, clave para el riesgo de crisis cambiaria en emergentes. Uso: AS-EMLA y AS-EMEA para necesidades de financiación exterior y concentración de vencimientos; CONTRA (AG-11) para escenarios de crisis.
- **Restricciones de uso:** CC BY 4.0; citar indicador, país y edición.
- **Sesgos posibles:** Anual con más de un año de desfase; depende de la declaración de los deudores; no cubre economías avanzadas.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «World Bank International Debt Statistics IDS 2025 external debt low middle income countries»; WebFetch: sí, ficha del catálogo de datos)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-04).

#### FXF-0418 · Q 83 (A) — Deutsche Bundesbank — saldos TARGET

- **Canal oficial (URL raíz):** https://www.bundesbank.de/en/tasks/payment-systems/t2/target-balances-920752 (anuncio de medias mensuales: https://www.bundesbank.de/en/press/press-releases/bundesbank-to-publish-monthly-averages-for-target2-balance-873408)
- **Emisor:** Deutsche Bundesbank
- **Documentación y notas:** Saldos de fin de día de cada banco central del Eurosistema frente al BCE derivados de pagos transfronterizos en T2. Bundesbank a 30/09/2026: 1.004.295,6 millones de euros; media de septiembre de 2026: 1.047.504,6 millones; serie de medias mensuales enlazada. Lectura analítica: documento de trabajo del BPI n.º 393 «Interpreting TARGET2 balances» (https://www.bis.org/publ/work393.htm).
- **Temática:** TFX-04 Balanza de pagos, flujos de capital y reservas (principal) · secundarias: TFX-09
- **Calidad Q:** 83 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 8/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Flujos de capital intraeuropeos; fragmentación de la zona del euro; fuga hacia la calidad (Alemania frente a periferia)
- **Motivo de inclusión y uso:** Termómetro de la fragmentación y de la fuga de capitales dentro de la zona del euro, relevante para la prima de riesgo del euro. Uso: AS-G10N (EUR) y TR-BCM (AG-09) en episodios de tensión soberana; CONTRA (AG-11) para escenarios de ruptura. Complementar con los saldos del Banco de España (RF-0018).
- **Restricciones de uso:** Uso con atribución.
- **Sesgos posibles:** Saldos afectados por compras de activos del Eurosistema y por la ubicación de la liquidez, no solo por fuga de capitales.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Migración de TARGET2 a T2 (2023); la página pasó a «T2/TARGET balances».
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Bundesbank TARGET2 balances statistics»; WebFetch: sí, página de saldos TARGET)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-04).

#### FXF-0073 · Q 81 (A) — FMI — International Reserves: plantilla de datos y guías (portal con enlaces por país)

- **Canal oficial (URL raíz):** https://www.imf.org/external/np/sta/ir/index.htm (guías: https://www.imf.org/external/np/sta/ir/irprocessweb/dataguide.htm)
- **Emisor:** Fondo Monetario Internacional
- **Documentación y notas:** Portal de la plantilla de reservas y liquidez en divisas: plantilla común, guías («Guidelines for a Data Template»), mapa para acceder a los datos de cada país (HTML actual; históricos en PDF y CSV) y enlaces a balanza de pagos y NEDD.
- **Temática:** TFX-04 Balanza de pagos, flujos de capital y reservas (principal) · secundarias: TFX-03
- **Calidad Q:** 81 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 6/10 · Acceso 7/10
- **Tipología:** primaria (metodología y redifusión oficial)
- **Acceso:** Abierto
- **Ámbitos:** Definiciones de reservas, drenajes y posiciones en derivados del sector oficial
- **Motivo de inclusión y uso:** Guía para interpretar correctamente las cifras de reservas (brutas frente a netas). Uso: MOTOR (AG-13) y Analistas de segmento emergente.
- **Restricciones de uso:** Condiciones del FMI.
- **Sesgos posibles:** Portal antiguo (la línea «Last Updated» falló en la consulta).
- **Historial de exactitud:** No aplicable.
- **Cambios de propiedad o de metodología:** Migración progresiva a data.imf.org (FXF-0072).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «IMF International Reserves and Foreign Currency Liquidity data template»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-04).

#### FXF-0078 · Q 80 (A) — Sveriges Riksbank — activos oficiales de reserva (informe semanal)

- **Canal oficial (URL raíz):** https://www.riksbank.se/en-gb/statistics/riksbanks-balance-sheet/official-reserve-assets-weekly-report/
- **Emisor:** Sveriges Riksbank
- **Documentación y notas:** Informe semanal de las reservas de divisas del Riksbank por partidas (oro, activos en divisas, DEG y otros).
- **Temática:** TFX-04 Balanza de pagos, flujos de capital y reservas (principal) · secundarias: TFX-01
- **Calidad Q:** 80 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 8/10 · Acceso 6/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Reservas oficiales de Suecia
- **Motivo de inclusión y uso:** Seguimiento de la gestión de reservas del Riksbank (incluidas coberturas o ventas de reservas que afectan a la corona). Uso: AS-G10M (AG-04: SEK).
- **Restricciones de uso:** Uso con atribución.
- **Sesgos posibles:** Variaciones dominadas por valoración.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «SAFE State Administration of Foreign Exchange official reserve assets monthly data»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-04).

#### FXF-0079 · Q 80 (A) — Department of Finance Canada — Monthly Official International Reserves

- **Canal oficial (URL raíz):** https://www.canada.ca/en/department-finance/services/publications/monthly-official-international-reserves.html
- **Emisor:** Department of Finance Canada
- **Documentación y notas:** Actualizaciones mensuales del valor total de las reservas, de los factores de su variación y del desglose por activos; publicaciones desde 2011 y archivo 1999–2009.
- **Temática:** TFX-04 Balanza de pagos, flujos de capital y reservas (principal) · secundarias: TFX-01
- **Calidad Q:** 80 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 7/10 · Acceso 6/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Reservas oficiales de Canadá
- **Motivo de inclusión y uso:** Reservas canadienses (gestionadas por el Gobierno, no por el banco central). Uso: AS-G10M (AG-04: CAD).
- **Restricciones de uso:** Licencia de gobierno abierto de Canadá.
- **Sesgos posibles:** La página índice no muestra el último mes: ir a «Publications and reports».
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «SAFE State Administration of Foreign Exchange official reserve assets monthly data»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-04).

#### FXF-0413 · Q 80 (A) — Lane y Milesi-Ferretti — External Wealth of Nations (EWN) database (Brookings, Hutchins Center)

- **Canal oficial (URL raíz):** https://www.brookings.edu/articles/the-external-wealth-of-nations-database/ (antecedente metodológico: https://www.imf.org/en/Publications/WP/Issues/2016/12/31/The-External-Wealth-of-Nations-Mark-II-Revised-and-Extended-Estimates-of-Foreign-Assets-and-18942)
- **Emisor:** Gian Maria Milesi-Ferretti (Brookings) y Philip R. Lane (BCE); alojada por el Hutchins Center on Fiscal and Monetary Policy
- **Documentación y notas:** Activos y pasivos exteriores de más de 200 países desde 1970 (IED, cartera, otra inversión, derivados, reservas), posición de inversión internacional neta y neta sin oro; datos hasta fin de 2024 con revisiones de principios de 2026; fuentes: estadísticas de balanza de pagos y PII del FMI, completadas con CPIS/CDIS, deuda externa y UNCTAD. Cita sugerida: Lane y Milesi-Ferretti (2018), IMF Economic Review 66.
- **Temática:** TFX-04 Balanza de pagos, flujos de capital y reservas (principal) · secundarias: TFX-10
- **Calidad Q:** 80 (A) — Primariedad 15/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 14/15 · Independencia 10/10 · Actualidad 6/10 · Acceso 10/10
- **Tipología:** secundaria (base de datos académica construida con fuentes oficiales)
- **Acceso:** Abierto (Excel descargable)
- **Ámbitos:** Posición de inversión internacional neta; composición de activos y pasivos exteriores; series largas comparables
- **Motivo de inclusión y uso:** Serie larga y homogénea de la PII neta, variable clave de los modelos de valoración de largo plazo (balance externo). Uso: MOTOR (AG-13) para modelos de tipo de cambio de equilibrio; AS-ESTR (AG-08) para divisas acreedoras frente a deudoras (JPY, CHF frente a USD, AUD, NZD).
- **Restricciones de uso:** Uso con atribución y cita del artículo.
- **Sesgos posibles:** Estimaciones propias para rellenar huecos; frecuencia anual con un año de desfase.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Pasó de alojarse en el FMI a Brookings; actualizaciones periódicas anunciadas.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Lane Milesi-Ferretti External Wealth of Nations database IMF»; WebFetch: sí, página de Brookings)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-04).

#### FXF-0076 · Q 78 (B) — State Administration of Foreign Exchange (SAFE, China) — reservas de divisas mensuales

- **Canal oficial (URL raíz):** https://www.safe.gov.cn/en/ (tabla anual de ejemplo: https://www.safe.gov.cn/en/2011/0920/574.html)
- **Emisor:** State Administration of Foreign Exchange (República Popular China)
- **Documentación y notas:** Tablas de reservas de divisas a fin de mes en miles de millones de dólares (sección «Data and Statistics» › «Forex Reserves»); difusión mensual a principios de mes (p. ej., 3,2407 billones de dólares a fin de marzo de 2025, difundido el 07/04/2025 en english.www.gov.cn). El SAFE publica además la balanza de pagos y la posición de inversión internacional de China.
- **Temática:** TFX-04 Balanza de pagos, flujos de capital y reservas (principal) · secundarias: TFX-02
- **Calidad Q:** 78 (B) — Primariedad 20/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 15/15 · Independencia 7/10 · Actualidad 9/10 · Acceso 7/10
- **Tipología:** primaria
- **Acceso:** Abierto (versión inglesa con tablas históricas por año)
- **Ámbitos:** Reservas oficiales de China, balanza de pagos china
- **Motivo de inclusión y uso:** Mayor tenedor de reservas del mundo; los cambios se usan como indicio de intervención (con cautela por valoración). Uso: AS-EMAS (AG-05: CNY/CNH) y TR-BCM (AG-09).
- **Restricciones de uso:** Uso con atribución.
- **Sesgos posibles:** Transparencia limitada: la intervención puede realizarse a través de bancos estatales y no reflejarse en las reservas (señalado por el Tesoro de EE. UU., FXF-0070).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «SAFE State Administration of Foreign Exchange official reserve assets monthly data»; WebFetch: sí, tablas 2006, 2007 y 2010 y nota de gov.cn de abril de 2025)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-04).

#### FXF-0414 · Q 76 (B) — SWIFT — Global Currency Tracker (antes RMB Tracker)

- **Canal oficial (URL raíz):** https://www.swift.com/sites/default/files/files/global-currency-tracker_september-2026.pdf (edición de marzo de 2026: https://www.swift.com/sites/default/files/files/global-currency-tracker_march-2026_final_v3.pdf · RMB Tracker anterior: https://www.swift.com/sites/default/files/files/rmb-tracker_february-2025.pdf)
- **Emisor:** S.W.I.F.T. SC
- **Documentación y notas:** Informe mensual renombrado en febrero de 2026 (antes RMB Tracker). Edición de septiembre de 2026 (datos de agosto): cuotas en pagos internacionales sin la zona del euro USD 52,09 %, EUR 21,37 %, GBP 6,37 %, JPY 3,52 %, CNY 3,26 %; en pagos globales USD 59,87 %, EUR 13,25 %, JPY 4,93 %, GBP 4,83 %, CNY 2,38 %. Basado en el valor de mensajes MT 103/202, pacs.008/009 (pagos), MT 300 (divisas) y MT 400/700 (financiación comercial).
- **Temática:** TFX-04 Balanza de pagos, flujos de capital y reservas (principal) · secundarias: TFX-03
- **Calidad Q:** 76 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 12/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** primaria (datos propios de la red de mensajería)
- **Acceso:** Abierto (PDF mensual)
- **Ámbitos:** Uso de divisas en pagos internacionales; internacionalización del renminbi; RMB offshore; financiación comercial
- **Motivo de inclusión y uso:** Indicador mensual y rápido del uso transaccional de cada divisa, complementario de COFER (reservas) y del informe del BCE (FXF-0402). Uso: AS-ESTR (AG-08) y TR-BCM (AG-09) para desdolarización y renminbi (TX-12); AS-EMLA/Asia para CNH.
- **Restricciones de uso:** Datos «tal cual»; citar edición y mes de datos.
- **Sesgos posibles:** No es estadística completa del mercado (existen canales fuera de SWIFT, p. ej., CIPS); cambios de cuota por cambios en tipos de mensaje o uso de la red, no solo por demanda.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Cambio de nombre y ampliación de alcance en febrero de 2026; SWIFT puede corregir datos pasados.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «SWIFT RMB Tracker share of global payments renminbi 2026»; WebFetch: sí, PDF de septiembre de 2026)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-04).

#### FXF-0077 · Q 70 (B) — Institute of International Finance (IIF) — Capital Flows Tracker

- **Canal oficial (URL raíz):** https://www.iif.com/Products/Capital-Flows-Tracker/lapg-7321/22 (lanzamiento: https://www.iif.com/About-Us/Press/View/ID/1152/IIFs-New-Capital-Flows-Tracker-Sees-Pick-up-in-Portfolio-Flows-to-Emerging-Markets)
- **Emisor:** Institute of International Finance (asociación de entidades financieras)
- **Documentación y notas:** Estimaciones mensuales de flujos de cartera (deuda y renta variable) hacia mercados emergentes, publicadas la última semana de cada mes desde el 26/03/2014; usan datos diarios de las economías que los publican. Los informes completos son para miembros; los titulares se difunden en notas de prensa.
- **Temática:** TFX-04 Balanza de pagos, flujos de capital y reservas (principal) · secundarias: TFX-08
- **Calidad Q:** 70 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 13/15 · Independencia 6/10 · Actualidad 10/10 · Acceso 7/10
- **Tipología:** secundaria cualificada (estimaciones propias a partir de datos oficiales)
- **Acceso:** Restringido a miembros (titulares públicos)
- **Ámbitos:** Flujos de cartera de no residentes hacia emergentes, por país y clase de activo
- **Motivo de inclusión y uso:** Indicador de alta frecuencia de entradas y salidas de capital en emergentes, adelantado a la balanza de pagos oficial. Uso: TR-PFV (AG-21) y Analistas de segmento emergente.
- **Restricciones de uso:** Solo contenidos públicos citables (regla F9-c).
- **Sesgos posibles:** Asociación de la industria financiera; estimaciones que se revisan con los datos oficiales.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Rebautizado de «Portfolio Flows Tracker» a «Capital Flows Tracker».
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «IIF Capital Flows Tracker emerging markets portfolio flows»; WebFetch: sí, nota de prensa de lanzamiento)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-04).

## TFX-05 Datos de mercado, tipos de referencia y posicionamiento

#### RF-0600 · Q 90 (A) — BCE — €STR (euro short-term rate) y €STR compuesto

- **Canal oficial (URL raíz):** https://www.ecb.europa.eu/stats/financial_markets_and_interest_rates/euro_short-term_rate/html/eurostr_overview.en.html (series: https://data.ecb.europa.eu/data/data-categories/financial-markets-and-interest-rates/euro-money-market/euro-short-term-rate-data)
- **Emisor:** Banco Central Europeo (administrador del índice), con datos recogidos por Bundesbank, Banco de España, Banque de France y Banca d'Italia
- **Temática:** TFX-05 Datos de mercado, tipos de referencia y posicionamiento (principal) · secundarias: TFX-01
- **Calidad Q:** 90 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria (índice de referencia oficial calculado sobre transacciones)
- **Acceso:** Abierto y gratuito (sin licencia de uso)
- **Ámbitos:** Tipo de interés a un día no garantizado de los bancos de la eurozona; publicación a las 08:00 CET de cada día TARGET2; tipos compuestos a 1 semana y 1, 3, 6 y 12 meses e índice compuesto (09:15 CET); pre-€STR hasta 30/09/2019; revisión metodológica anual (última vista: 09/12/2025)
- **Motivo de inclusión y uso:** Tipo libre de riesgo de referencia del euro y ancla de la curva OIS en euros. Uso: MOTOR (AG-13) y TR-PFV (AG-21) como pata en euros de los puntos forward, del carry y de la base cruzada EUR/USD; TR-BCM (AG-09) para el diferencial €STR–facilidad de depósito.
- **Sesgos y cautelas:** Solo mide préstamos no garantizados captados por bancos (incluye depósitos de entidades no bancarias, por eso cotiza por debajo de la facilidad de depósito); procedimiento de contingencia si informan menos de 20 bancos.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ECB euro short-term rate €STR money market statistical reporting»; WebFetch: sí)
- **Origen:** Reutilizada de F9 V3.2 (TF-18) en el Bloque A Forex V1.0 (2026-11-02).

#### RF-0602 · Q 90 (A) — Federal Reserve Bank of New York — Reference Rates (SOFR, EFFR, OBFR, TGCR, BGCR)

- **Canal oficial (URL raíz):** https://www.newyorkfed.org/markets/reference-rates (SOFR: https://www.newyorkfed.org/markets/reference-rates/sofr · medias e índice: https://www.newyorkfed.org/markets/reference-rates/sofr-averages-and-index)
- **Emisor:** Federal Reserve Bank of New York (administrador; en cooperación con la OFR para los tipos repo)
- **Temática:** TFX-05 Datos de mercado, tipos de referencia y posicionamiento (principal) · secundarias: TFX-01
- **Calidad Q:** 90 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria (índices de referencia oficiales sobre transacciones; declaración de cumplimiento IOSCO)
- **Acceso:** Abierto (API de datos de mercados)
- **Ámbitos:** EFFR y OBFR (mediana ponderada por volumen de fondos federales y eurodólares; ~9:00 ET); TGCR, BGCR y SOFR (repo a un día con colateral del Tesoro; SOFR excluye el 20 % de menor tipo del DVP); medias SOFR a 30, 90 y 180 días e índice SOFR (8:00 ET)
- **Motivo de inclusión y uso:** Fuente primaria de los tipos a un día del dólar (SOFR, EFFR). Uso: MOTOR (AG-13, MC de paridad cubierta) y TR-PFV (AG-21) como pata en dólares de los puntos forward, del carry y de la base cruzada; TR-BCM (AG-09) para la posición del EFFR en la banda objetivo.
- **Sesgos y cautelas:** Revisiones del mismo día (~14:30 ET) posibles; el SOFR se publica con un día de retraso respecto a la fecha valor. RF-0343 (OFR) redistribuye estas series: citar aquí la fuente primaria.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «New York Fed reference rates SOFR EFFR OBFR TGCR BGCR»; WebFetch: sí, página «additional information about reference rates»)
- **Origen:** Reutilizada de F9 V3.2 (TF-18) en el Bloque A Forex V1.0 (2026-11-02).

#### FXF-0090 · Q 89 (A) — BCE — tipos de cambio de referencia del euro

- **Canal oficial (URL raíz):** https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html (acceso corto: https://www.ecb.europa.eu/stats/eurofxref)
- **Emisor:** Banco Central Europeo
- **Documentación y notas:** 29 divisas frente al euro (tipo del rublo suspendido desde el 01/03/2022), publicadas hacia las 16:00 CET cada día hábil salvo cierres de TARGET; resultan de una concertación diaria entre bancos centrales europeos hacia las 14:10 CET. «Solo a efectos informativos»: el BCE desaconseja su uso para transacciones. Descargas en PDF, CSV, XML, RSS y SDMX-ML (series históricas). Último dato visto: 30/10/2026.
- **Temática:** TFX-05 Datos de mercado, tipos de referencia y posicionamiento (principal) · secundarias: TFX-03
- **Calidad Q:** 89 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria (tipo oficial de referencia)
- **Acceso:** Abierto y gratuito
- **Ámbitos:** Tipos de referencia diarios del euro desde 1999 (incluidas divisas emergentes europeas y asiáticas)
- **Motivo de inclusión y uso:** Serie oficial homogénea y gratuita para valoraciones, contabilidad y análisis históricos. Uso: MOTOR (AG-13), CUR (AG-12) para normalizar fechas y convenciones, AS-G10N y AS-EMEA.
- **Restricciones de uso:** Uso libre con atribución; no apta para liquidar transacciones.
- **Sesgos posibles:** Fotografía de una hora concreta (no cierre de Nueva York); no recoge todas las divisas.
- **Historial de exactitud:** No aplicable (dato).
- **Cambios de propiedad o de metodología:** Reforma de 2015 tras las recomendaciones del FSB sobre referencias cambiarias; suspensión del RUB en 2022.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ECB euro foreign exchange reference rates daily 16:00 CET»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-05).

#### FXF-0091 · Q 89 (A) — Federal Reserve Board — H.10/G.5 Foreign Exchange Rates

- **Canal oficial (URL raíz):** https://www.federalreserve.gov/RELEASES/h10/about.htm
- **Emisor:** Board of Governors of the Federal Reserve System (tipos certificados por la Fed de Nueva York)
- **Documentación y notas:** H.10 semanal con tipos diarios («noon buying rates in New York for cable transfers», certificados a efectos aduaneros) e índices nominales del dólar (Broad, AFE —economías avanzadas— y EME —emergentes—); G.5 mensual y G.5A anual; índices reales solo mensuales. Publicaciones anteriores no se revisan; la serie histórica por país se actualiza cada lunes a las 16:15. Cambio de indexación de los índices diarios desde el 24/06/2019.
- **Temática:** TFX-05 Datos de mercado, tipos de referencia y posicionamiento (principal) · secundarias: TFX-03
- **Calidad Q:** 89 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto (también vía FRED, RF-0001)
- **Ámbitos:** Tipos bilaterales frente al dólar e índices del dólar
- **Motivo de inclusión y uso:** Serie oficial de referencia del dólar en EE. UU. Uso: MOTOR (AG-13), AS-ESTR (AG-08, dólar amplio), Analistas de segmento.
- **Restricciones de uso:** Uso libre con atribución.
- **Sesgos posibles:** Tipo de mediodía de Nueva York (no cierre); cobertura limitada de divisas.
- **Historial de exactitud:** No aplicable (dato).
- **Cambios de propiedad o de metodología:** Cambio de 2019 en los índices diarios.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Federal Reserve H.10 foreign exchange rates nominal broad dollar index»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-05).

#### RF-0605 · Q 89 (A) — Bank of England — SONIA (Sterling Overnight Index Average) y SONIA Compounded Index

- **Canal oficial (URL raíz):** https://www.bankofengland.co.uk/markets/sonia-benchmark
- **Emisor:** Bank of England (administrador del índice desde 2016)
- **Temática:** TFX-05 Datos de mercado, tipos de referencia y posicionamiento (principal) · secundarias: TFX-01
- **Calidad Q:** 89 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** primaria (índice de referencia oficial sobre transacciones)
- **Acceso:** Abierto (serie IUDSOIA en la base de datos estadística interactiva del BoE)
- **Ámbitos:** Tipo medio a un día no garantizado en libras; publicación cada día hábil de Londres; índice compuesto desde 03/08/2020; documento de características y políticas; actas del grupo asesor
- **Motivo de inclusión y uso:** Tipo libre de riesgo de la libra y ancla de la curva OIS en libras. Uso: MOTOR (AG-13) y TR-PFV (AG-21) como pata en libras de los puntos forward y del carry de GBP; TR-BCM (AG-09) para el diferencial SONIA–Bank Rate.
- **Sesgos y cautelas:** Refleja préstamos a bancos (incluye depósitos de no bancarias); la ficha general del BoE es RF-0019.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Bank of England SONIA interest rate benchmark»; WebFetch: sí)
- **Origen:** Reutilizada de F9 V3.2 (TF-18) en el Bloque A Forex V1.0 (2026-11-02).

#### RF-0001 · Q 88 (A) — FRED (Federal Reserve Economic Data, Banco de la Reserva Federal de San Luis)

- **Canal oficial:** fred.stlouisfed.org
- **Documentación y notas:** Documentación de la API: fred.stlouisfed.org/docs/api/fred/ · Cada serie declara su fuente original y metodología en sus metadatos (p. ej. la serie CPIAUCSL de la pieza 4.3: fred.stlouisfed.org/series/CPIAUCSL)
- **Temática:** TFX-05 Datos de mercado, tipos de referencia y posicionamiento (principal) · secundarias: TFX-03
- **Calidad Q:** 88 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 10/10
- **Nivel de fiabilidad en V2.4:** A
- **Tipología:** primaria (hospeda series de los emisores oficiales)
- **Motivo de inclusión:** Portal que redistribuye, con metadatos de fuente, las series oficiales de tipos de cambio de la Reserva Federal (H.10: bilaterales diarios e índices nominal y real del dólar, p. ej. DTWEXBGS) y de otros emisores, con API. Uso: MOTOR (AG-13) y Analistas de segmento para series históricas reproducibles; citar siempre la fuente original declarada.
- **Ámbitos:** Macroeconomía; precios e inflación; tipos de interés; mercado laboral; indicadores de recesión; renta variable a nivel agregado
- **Restricciones de uso:** Uso académico y de referencia; citar la serie concreta y la fuente original que FRED declara en sus metadatos
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Sesgos posibles:** Ninguno editorial conocido; posible sesgo de cobertura hacia series estadounidenses
- **Cambios de propiedad o de metodología:** Sin cambios conocidos; mantiene el hosting del Fed de San Luis; verificar en cada mantenimiento
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Federal Reserve H.10 foreign exchange rates nominal broad dollar index» → https://fred.stlouisfed.org/series/DTWEXBGS; WebFetch: sí, serie DTWEXBGS con último dato 23/10/2026)
- **Origen:** Reutilizada de F9 V3.2 (TF-01) en el Bloque A Forex V1.0 (2026-11-02).

#### FXF-0095 · Q 87 (A) — Banco de México — tipo de cambio FIX

- **Canal oficial (URL raíz):** https://www.banxico.org.mx/apps/dao-web/4/52/Fix48.html (consulta de tipos de cambio peso/dólar: https://www.banxico.org.mx/tipcamb/llenarTiposCambioAction.do?idioma=sp)
- **Emisor:** Banco de México
- **Documentación y notas:** Promedio de cotizaciones del mercado mayorista para operaciones liquidables el segundo día hábil, obtenidas de plataformas de transacción cambiaria y otros medios electrónicos representativos; Banxico lo difunde al mediodía de cada día hábil y se publica en el Diario Oficial de la Federación al día hábil siguiente; sirve para solventar obligaciones en dólares pagaderas en México (p. ej., FIX del 30/10/2026: 18,7962). Base normativa: DOF de 1996, Circular 2012/03 de Banxico y resolución de 2009.
- **Temática:** TFX-05 Datos de mercado, tipos de referencia y posicionamiento (principal) · secundarias: TFX-02
- **Calidad Q:** 87 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 10/10 · Acceso 8/10
- **Tipología:** primaria (tipo oficial de referencia)
- **Acceso:** Abierto
- **Ámbitos:** Tipo de referencia oficial USD/MXN
- **Motivo de inclusión y uso:** Fijación de referencia del par emergente latinoamericano más líquido. Uso: AS-EMLA (AG-06), MOTOR (AG-13) y CUR (AG-12) para normalizar precios.
- **Restricciones de uso:** Uso libre con atribución.
- **Sesgos posibles:** Fotografía del mediodía de México.
- **Historial de exactitud:** No aplicable (dato).
- **Cambios de propiedad o de metodología:** Cambios de fuentes de cotización documentados en la normativa.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Banxico tipo de cambio FIX determinación Diario Oficial»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-05).

#### FXF-0092 · Q 86 (A) — Federal Reserve Board — Nominal Broad Dollar Index (índice amplio del dólar)

- **Canal oficial (URL raíz):** https://www.federalreserve.gov/releases/h10/summary/jrxwtfb_nb.htm (mensual: https://www.federalreserve.gov/releases/h10/summary/jrxwtfb_nm.htm · serie en FRED: https://fred.stlouisfed.org/series/DTWEXBGS)
- **Emisor:** Board of Governors of the Federal Reserve System
- **Documentación y notas:** Índice diario ponderado por comercio de bienes y servicios (enero de 2006 = 100), con subíndices AFE y EME e índices reales mensuales. Último dato en FRED: 121,3202 (23/10/2026); la página resumen histórica de la Fed muestra la serie diaria desde el 02/01/2006.
- **Temática:** TFX-05 Datos de mercado, tipos de referencia y posicionamiento (principal) · secundarias: TFX-03
- **Calidad Q:** 86 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Valor efectivo del dólar frente a sus socios comerciales
- **Motivo de inclusión y uso:** Medida del «dólar amplio» más representativa que el DXY (incluye emergentes y China). Uso: AS-ESTR (AG-08, cesta del dólar amplio), TR-BCM (AG-09, régimen del dólar).
- **Restricciones de uso:** Uso libre con atribución; FRED solicita cita.
- **Sesgos posibles:** Ponderaciones revisadas periódicamente.
- **Historial de exactitud:** No aplicable (dato).
- **Cambios de propiedad o de metodología:** Reindexación de 2019 (ver FXF-0091).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Federal Reserve H.10 foreign exchange rates nominal broad dollar index»; WebFetch: sí, página resumen y serie DTWEXBGS)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-05).

#### FXF-0096 · Q 85 (A) — Banco Central do Brasil — taxa PTAX (tipo de referencia del real)

- **Canal oficial (URL raíz):** https://www.bcb.gov.br/pre/normativos/circ/2010/pdf/circ_3506_v3_p.pdf (Circular 3.506 y su versión vigente)
- **Emisor:** Banco Central do Brasil (Departamento de Operações das Reservas Internacionais, Depin)
- **Documentación y notas:** Cuatro consultas electrónicas diarias de dos minutos a los *dealers* acreditados, iniciadas en momentos aleatorios dentro de las ventanas 10:00–10:10, 11:00–11:10, 12:00–12:10 y 13:00–13:10; en cada consulta se eliminan las dos cotizaciones más altas y las dos más bajas y se promedian las restantes; la PTAX de compra y venta es la media de las cuatro consultas.
- **Temática:** TFX-05 Datos de mercado, tipos de referencia y posicionamiento (principal) · secundarias: TFX-02
- **Calidad Q:** 85 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 7/10
- **Tipología:** primaria (norma y tipo oficial)
- **Acceso:** Abierto (portugués)
- **Ámbitos:** Tipo de referencia USD/BRL para liquidación de contratos y NDF
- **Motivo de inclusión y uso:** Tipo de liquidación de los derivados y NDF sobre el real. Uso: AS-EMLA (AG-06), MOTOR (AG-13) y TR-PFV (AG-21).
- **Restricciones de uso:** Uso libre con atribución.
- **Sesgos posibles:** Normativa en portugués; ventanas modificadas por circulares posteriores (3.537/2011).
- **Historial de exactitud:** No aplicable (dato).
- **Cambios de propiedad o de metodología:** Ventanas cambiadas en 2011.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Banco Central do Brasil PTAX cotações taxa de câmbio»; WebFetch: sí, Circular 3.506)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-05).

#### FXF-0101 · Q 85 (A) — London Foreign Exchange Joint Standing Committee (FXJSC) — encuesta semestral de volumen de divisas

- **Canal oficial (URL raíz):** https://www.bankofengland.co.uk/markets/london-foreign-exchange-joint-standing-committee/results-of-the-semi-annual-fx-turnover-surveys-in-april-2025
- **Emisor:** Bank of England (secretaría del FXJSC)
- **Documentación y notas:** Encuesta de abril y octubre a los principales intermediarios de Londres; abril de 2025: 4,045 billones de dólares diarios, máximo histórico (+26 % frente a octubre de 2024); publicada el 22/07/2025. En abril se realizan encuestas paralelas de los comités de Nueva York, Singapur, Tokio, Canadá y Australia (existe ya la edición de abril de 2026).
- **Temática:** TFX-05 Datos de mercado, tipos de referencia y posicionamiento (principal) · secundarias: TFX-03
- **Calidad Q:** 85 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 8/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Volumen del mercado de Londres por instrumento, divisa y contraparte, cada seis meses
- **Motivo de inclusión y uso:** Actualización semestral de la liquidez del mercado entre ediciones trienales del BPI. Uso: TR-PFV (AG-21), AS-ESTR (AG-08).
- **Restricciones de uso:** Uso libre con atribución.
- **Sesgos posibles:** Panel de entidades informantes; mide por ubicación de la mesa.
- **Historial de exactitud:** No aplicable (dato).
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Foreign Exchange Joint Standing Committee semi-annual turnover survey New York Foreign Exchange Committee volume survey»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-05).

#### RF-0049 · Q 85 (A) — CFTC — Commitments of Traders (COT)

- **Canal oficial (URL raíz):** https://www.cftc.gov/MarketReports/CommitmentsofTraders/index.htm
- **Emisor:** U.S. Commodity Futures Trading Commission (CFTC)
- **Documentación y notas:** La página oficial describe los cuatro informes (Legacy, Supplemental, Disaggregated, Traders in Financial Futures) y remite al calendario de publicación y al Public Reporting Environment (históricos consultables). Catálogo federal: catalog.data.gov/dataset/commitment-of-traders-cot
- **Temática:** TFX-05 Datos de mercado, tipos de referencia y posicionamiento (principal) · secundarias: TFX-06
- **Calidad Q:** 85 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 14/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto (dominio público, datos federales de EE. UU.)
- **Ámbitos:** Posicionamiento semanal en futuros y opciones sobre futuros (mercados con ≥ 20 operadores declarables): comerciales/no comerciales; productores, swap dealers, managed money; dealers, gestores de activos y fondos apalancados en futuros financieros (divisas, Treasuries, índices bursátiles, VIX)
- **Motivo de inclusión y uso:** Dato primario de posicionamiento especulativo y de cobertura en futuros de divisas del CME (EUR, JPY, GBP, CHF, CAD, AUD, NZD, MXN, BRL…) e índice dólar. Uso: TR-PFV (AG-21) para el posicionamiento neto de fondos apalancados y gestores de activos (informe TFF), extremos y *crowding*; AS-ESTR (AG-08) para el riesgo de reversión del carry.
- **Restricciones de uso:** Uso libre; citar informe (Legacy/Disaggregated/TFF), contrato y fecha del martes de referencia.
- **Sesgos y cautelas:** Datos del martes publicados el viernes a las 15:30 ET (desfase de 3 días; festivos alteran el calendario). Categorías amplias; los datos publicados no se revisan. Históricos: Legacy desde 15/01/1986; Disaggregated y TFF desde 13/06/2006.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos; vigilar avisos de calendario de la CFTC.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «CFTC Commitments of Traders reports official»; WebFetch: sí)
- **Origen:** Reutilizada de F9 V3.2 (TF-06) en el Bloque A Forex V1.0 (2026-11-02).

#### FXF-0102 · Q 83 (A) — Foreign Exchange Committee (Fed de Nueva York) — FX Volume Survey

- **Canal oficial (URL raíz):** https://www.newyorkfed.org/medialibrary/media/banking/reportingforms/FX_Volume_Survey_Instructions.pdf
- **Emisor:** Foreign Exchange Committee (patrocinador), con la Federal Reserve Bank of New York como agente recopilador
- **Documentación y notas:** Encuesta semestral voluntaria sobre todas las operaciones de abril y octubre: contado, *forwards* (con NDF como partida «de las cuales»), *FX swaps* y opciones (incluidas exóticas); 21 intermediarios informantes en el apéndice A; entrega en 30 días.
- **Temática:** TFX-05 Datos de mercado, tipos de referencia y posicionamiento (principal) · secundarias: TFX-06
- **Calidad Q:** 83 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 14/15 · Independencia 9/10 · Actualidad 8/10 · Acceso 7/10
- **Tipología:** primaria
- **Acceso:** Abierto (instrucciones y resultados del comité)
- **Ámbitos:** Volumen del mercado de divisas de Norteamérica, incluidos NDF y opciones
- **Motivo de inclusión y uso:** Liquidez semestral de la plaza de Nueva York, con NDF de divisas emergentes. Uso: TR-PFV (AG-21), AS-EMLA y AS-EMAS (NDF).
- **Restricciones de uso:** Uso libre con atribución.
- **Sesgos posibles:** Panel voluntario; el documento de instrucciones no está fechado.
- **Historial de exactitud:** No aplicable (dato).
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Foreign Exchange Joint Standing Committee semi-annual turnover survey New York Foreign Exchange Committee volume survey»; WebFetch: sí, instrucciones)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-05).

#### FXF-0094 · Q 82 (A) — CFETS — tipo central (central parity) del renminbi

- **Canal oficial (URL raíz):** https://www.chinamoney.com.cn/english/bmkcpr/index.html
- **Emisor:** China Foreign Exchange Trade System (CFETS), por autorización del Banco Popular de China
- **Documentación y notas:** Publicación diaria del tipo central del CNY. Para el USD, CFETS recoge cotizaciones de los creadores de mercado antes de la apertura, elimina la más alta y la más baja y pondera el resto; HKD y MOP se calculan por tipos cruzados (cotizaciones internacionales a las 9:00); cotización directa frente a EUR, JPY, GBP, AUD, NZD, SGD, CHF, CAD, MYR, RUB, ZAR, KRW, AED, SAR, HUF, PLN, DKK, SEK, NOK, TRY, MXN y THB.
- **Temática:** TFX-05 Datos de mercado, tipos de referencia y posicionamiento (principal) · secundarias: TFX-02
- **Calidad Q:** 82 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 15/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 8/10
- **Tipología:** primaria (fijación oficial)
- **Acceso:** Abierto (la página describe el método; los valores se muestran como imagen)
- **Ámbitos:** Tipo central diario del CNY; banda de negociación onshore alrededor del tipo central
- **Motivo de inclusión y uso:** Principal señal diaria de la orientación oficial sobre el renminbi (comparar el tipo central con la estimación de mercado). Uso: AS-EMAS (AG-05: CNY/CNH y divisas asiáticas ligadas), TR-BCM (AG-09).
- **Restricciones de uso:** Uso con atribución.
- **Sesgos posibles:** Fijación administrada con componentes discrecionales no publicados.
- **Historial de exactitud:** No aplicable (dato).
- **Cambios de propiedad o de metodología:** Cambios históricos del método de fijación (2015, factor contracíclico): vigilar.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «CFETS RMB central parity rate announcement chinamoney»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-05).

#### FXF-0093 · Q 80 (A) — LSEG — WM/Reuters (WMR) FX Benchmarks (fijación de las 16:00 de Londres)

- **Canal oficial (URL raíz):** https://lseg.com/en/data-analytics/financial-data/benchmarks/foreign-exchange-benchmarks (documento técnico: https://www.lseg.com/content/dam/ftse-russell/en_us/documents/factsheets/wmr-overview-and-request-for-feedback.pdf)
- **Emisor:** LSEG (WM/Refinitiv; administrado por Refinitiv Benchmark Services Limited, RBSL)
- **Documentación y notas:** Fijaciones de contado de cierre a las 16:00 (hora del Reino Unido), las más usadas, y fijaciones intradía en hasta 47 horas alternativas; ventana de cálculo de 5 minutos con mediana y captura por intervalos; índice regulado desde 2015 (BMR de la UE y después del Reino Unido) y conforme con los principios de IOSCO; comité de supervisión que se reúne cada unas seis semanas. Documento de 2022.
- **Temática:** TFX-05 Datos de mercado, tipos de referencia y posicionamiento (principal) · secundarias: —
- **Calidad Q:** 80 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 14/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 6/10
- **Tipología:** primaria (administrador del índice de referencia)
- **Acceso:** Datos con licencia; metodología pública
- **Ámbitos:** Fijaciones de referencia para valoración de índices y carteras; flujos de fin de mes alrededor de la fijación
- **Motivo de inclusión y uso:** Referencia de valoración de la mayor parte de los índices de renta fija y variable globales: concentra los flujos de cobertura de fin de mes. Uso: TR-PFV (AG-21, flujos de fin de mes y estacionales), MOTOR (AG-13).
- **Restricciones de uso:** Licencia de LSEG para los valores; citar solo la metodología pública.
- **Sesgos posibles:** Proveedor privado; la página general de LSEG no detalla la metodología (usar el documento técnico).
- **Historial de exactitud:** No aplicable (dato).
- **Cambios de propiedad o de metodología:** Ventana ampliada a 5 minutos tras las recomendaciones del FSB de 2014 (FXF-0097); cambio de propiedad Refinitiv → LSEG.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «LSEG WM/Reuters FX benchmarks methodology 4pm London fix»; WebFetch: sí, documento técnico; la página general cargó sin detalle)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-05).

#### RF-0620 · Q 80 (A) — SIX — SARON (Swiss Average Rate Overnight) y SARON compuesto

- **Canal oficial (URL raíz):** https://www.six-group.com/en/market-data/indices/switzerland/saron.html (reglamento: https://www.six-group.com/dam/download/market-data/indices/swiss-reference-rates/six-methodology-swiss-reference-rates-rules-en.pdf · datos: https://indexdata.six-group.com/swiss_reference_rates/reference_rates.html)
- **Emisor:** SIX Group (administrador del índice de referencia)
- **Temática:** TFX-05 Datos de mercado, tipos de referencia y posicionamiento (principal) · secundarias: TFX-01
- **Calidad Q:** 80 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 14/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 5/10
- **Tipología:** primaria (índice de referencia sobre operaciones y cotizaciones firmes del repo en francos)
- **Acceso:** Histórico descargable gratis; tipos compuestos públicos con un día de retraso; intradía y difusión pública inmediata con licencia de pago
- **Ámbitos:** Tipo medio ponderado por volumen del repo a un día en francos suizos (desde 30/06/1999), fijaciones a las 12, 16 y 18 h CET; tipos compuestos e índices a 1 semana y 1, 2, 3, 6, 9 y 12 meses
- **Motivo de inclusión y uso:** Tipo libre de riesgo del franco suizo. Uso: MOTOR (AG-13) y TR-PFV (AG-21) como pata en francos de los puntos forward y del coste del carry financiado en CHF; AS-G10N (EUR/CHF, USD/CHF).
- **Sesgos y cautelas:** Operador privado de mercado con licencias costosas (citar con 24 h de retraso); mercado repo concentrado.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «SARON Swiss Average Rate Overnight SIX index data», limitada a six-group.com; WebFetch: sí)
- **Origen:** Reutilizada de F9 V3.2 (TF-18) en el Bloque A Forex V1.0 (2026-11-02).

#### FXF-0098 · Q 79 (B) — ICE — U.S. Dollar Index (USDX/DXY) y sus futuros

- **Canal oficial (URL raíz):** https://www.ice.com/products/194/US-Dollar-Index-Futures (catálogo de índices de divisas de ICE Data Indices: https://developer.ice.com/fixed-income-data-services/catalog/ice-data-indices-currency-indices)
- **Emisor:** Intercontinental Exchange (ICE Futures U.S.)
- **Documentación y notas:** Índice del dólar frente a seis divisas ponderadas (euro, yen, libra, dólar canadiense, corona sueca y franco suizo); futuro DX: 1.000 $ × índice, tic de 0,005 (5 $), vencimientos trimestrales con entrega física el tercer miércoles, liquidación diaria por VWAP de 14:59 a 15:00 ET, unas 21 horas de negociación diaria.
- **Temática:** TFX-05 Datos de mercado, tipos de referencia y posicionamiento (principal) · secundarias: TFX-06
- **Calidad Q:** 79 (B) — Primariedad 18/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 13/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** primaria (índice y contrato de la bolsa)
- **Acceso:** Especificaciones abiertas; datos en tiempo real con licencia
- **Ámbitos:** Índice del dólar más citado por el mercado (sesgado hacia el euro)
- **Motivo de inclusión y uso:** Referencia de mercado del dólar y contrato con posicionamiento en el COT (RF-0049). Uso: AS-ESTR (AG-08) frente al índice amplio de la Fed (FXF-0092); TR-PFV (AG-21).
- **Restricciones de uso:** Marcas registradas de ICE; datos con licencia.
- **Sesgos posibles:** Cesta fija sin emergentes ni China; peso dominante del euro.
- **Historial de exactitud:** No aplicable (dato).
- **Cambios de propiedad o de metodología:** Cesta sin cambios desde la entrada del euro.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ICE U.S. Dollar Index DXY futures methodology currency weights»; WebFetch: sí, página del contrato)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-05).

#### FXF-0097 · Q 78 (B) — Financial Stability Board — Final Report on Foreign Exchange Benchmarks (2014)

- **Canal oficial (URL raíz):** https://fsb.org/2014/09/r_140930 (informe de seguimiento: https://fsb.org/uploads/FX-Benchmarks-progress-report.pdf)
- **Emisor:** Financial Stability Board
- **Documentación y notas:** Informe del 30/09/2014 con recomendaciones sobre la metodología de cálculo de las fijaciones WM/Reuters, la revisión de IOSCO, la publicación de tipos de referencia por los bancos centrales, la infraestructura de ejecución de operaciones a la fijación y la conducta de los participantes en torno a la fijación de las 16:00 de Londres.
- **Temática:** TFX-05 Datos de mercado, tipos de referencia y posicionamiento (principal) · secundarias: TFX-03
- **Calidad Q:** 78 (B) — Primariedad 18/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 2/10 · Acceso 8/10
- **Tipología:** primaria (organismo regulador internacional)
- **Acceso:** Abierto
- **Ámbitos:** Integridad de las fijaciones cambiarias; marco de las referencias actuales
- **Motivo de inclusión y uso:** Explica por qué las fijaciones actuales usan ventanas y medianas y cómo se forman los flujos alrededor de ellas. Uso: TR-PFV (AG-21) y CUR (AG-12) para interpretar fijaciones.
- **Restricciones de uso:** Uso libre con atribución.
- **Sesgos posibles:** Documento de 2014 (marco histórico; comprobar la vigencia en el administrador).
- **Historial de exactitud:** No aplicable.
- **Cambios de propiedad o de metodología:** No aplicable.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «LSEG WM/Reuters FX benchmarks methodology 4pm London fix»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-05).

#### FXF-0099 · Q 74 (B) — CLS Group — CLSMarketData (volúmenes, flujos y posiciones de divisas)

- **Canal oficial (URL raíz):** https://www.cls-group.com/products/data/clsmarketdata/ (página de publicaciones: https://www.cls-group.com/publications/clsmarketdata/)
- **Emisor:** CLS Group (infraestructura de liquidación de divisas)
- **Documentación y notas:** Conjuntos de datos alternativos derivados de las operaciones liquidadas en CLSSettlement (más del 50 % del volumen mundial en las 18 divisas que liquida; más de 3.000 millones de operaciones desde 2011): FX Volume (contado, *forwards* y *swaps* en 40 pares), FX Flow (flujos por segmentos económicos, señal direccional), FX Outstanding (posiciones netas a partir de *forwards* y *swaps* vivos) y FX Pricing.
- **Temática:** TFX-05 Datos de mercado, tipos de referencia y posicionamiento (principal) · secundarias: TFX-04
- **Calidad Q:** 74 (B) — Primariedad 18/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 13/15 · Independencia 8/10 · Actualidad 9/10 · Acceso 5/10
- **Tipología:** primaria (datos de liquidación)
- **Acceso:** Con licencia (presentación pública)
- **Ámbitos:** Volumen y flujo del mercado de divisas con alta frecuencia; flujos por segmentos económicos y posiciones netas a plazo
- **Motivo de inclusión y uso:** Única fuente de flujos reales de alta frecuencia del mercado OTC de divisas. Uso: TR-PFV (AG-21) para flujos de cartera, de cobertura y de fin de mes.
- **Restricciones de uso:** Solo contenidos públicos citables sin licencia (regla F9-c).
- **Sesgos posibles:** Solo divisas y operaciones liquidadas en CLS (sin la mayoría de emergentes ni NDF).
- **Historial de exactitud:** No aplicable (dato).
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «CLS FX market volume data CLSMarketData»; WebFetch: sí, página de producto y de publicaciones)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-05).

#### FXF-0103 · Q 73 (B) — BCE — Foreign Exchange Contact Group (FXCG): actas y presentaciones

- **Canal oficial (URL raíz):** https://ECB.eu/paym/groups/pdf/fxcg/2015/1211/2015-11-12_WM_presentation.pdf (presentación de WM ante el grupo, 12/11/2015)
- **Emisor:** Banco Central Europeo (grupo de contacto con participantes del mercado de divisas)
- **Documentación y notas:** Foro del BCE con operadores del mercado de divisas que publica órdenes del día, resúmenes y presentaciones (p. ej., la presentación de WM sobre las fijaciones tras la reforma de 2015).
- **Temática:** TFX-05 Datos de mercado, tipos de referencia y posicionamiento (principal) · secundarias: TFX-01
- **Calidad Q:** 73 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 14/15 · Independencia 8/10 · Actualidad 5/10 · Acceso 8/10
- **Tipología:** primaria (materiales de un grupo oficial; opiniones de participantes)
- **Acceso:** Abierto
- **Ámbitos:** Inteligencia de mercado del BCE sobre liquidez, microestructura y referencias del mercado de divisas
- **Motivo de inclusión y uso:** Lectura cualitativa de la liquidez y de los cambios de estructura del mercado del euro según sus participantes. Uso: TR-PFV (AG-21) y TR-BCM (AG-09).
- **Restricciones de uso:** Uso con atribución.
- **Sesgos posibles:** Opiniones de bancos participantes (regla F9-a); la ficha se apoya en un documento antiguo devuelto por la búsqueda.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «LSEG WM/Reuters FX benchmarks methodology 4pm London fix»; WebFetch: no)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-05).

#### FXF-0100 · Q 72 (B) — CLS Group — «CLS FX trading activity» (comunicados mensuales de volumen)

- **Canal oficial (URL raíz):** https://www.cls-group.com/news/cls-fx-trading-activity-august-2019/ (serie de comunicados mensuales; p. ej., también https://www.cls-group.com/news/cls-fx-trading-activity-july-2019/)
- **Emisor:** CLS Group
- **Documentación y notas:** Comunicados mensuales con el volumen medio diario liquidado en CLS por instrumento (contado, *swaps*, *forwards*), sindicados también por agregadores de noticias (p. ej., Mondo Visione, octubre de 2023).
- **Temática:** TFX-05 Datos de mercado, tipos de referencia y posicionamiento (principal) · secundarias: —
- **Calidad Q:** 72 (B) — Primariedad 17/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 13/15 · Independencia 8/10 · Actualidad 6/10 · Acceso 7/10
- **Tipología:** primaria (estadística agregada del operador)
- **Acceso:** Abierto
- **Ámbitos:** Volumen mensual del mercado de divisas liquidado en CLS
- **Motivo de inclusión y uso:** Indicador mensual gratuito de actividad del mercado entre encuestas semestrales. Uso: TR-PFV (AG-21).
- **Restricciones de uso:** Uso con atribución; las copias sindicadas no cuentan como fuentes independientes (regla F9-b).
- **Sesgos posibles:** Los resultados devueltos eran de 2019 y 2023: confirmar la vigencia de la serie en el primer barrido.
- **Historial de exactitud:** No aplicable (dato).
- **Cambios de propiedad o de metodología:** Posible sustitución por los informes de CLSMarketData.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «CLS FX market volume data CLSMarketData»; WebFetch: no)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-05).

## TFX-06 Volatilidad y opciones de divisas: mercados y datos

#### RF-0540 · Q 88 (A) — BIS — estadísticas de derivados OTC (semestrales) y Encuesta Trienal

- **Canal oficial (URL raíz):** https://www.bis.org/publ/otc_hy2512.htm (comentario más reciente: https://www.bis.org/stats_derivatives_commentaries/latest.htm · tablas: https://data.bis.org/topics/OTC_DER/tables-and-dashboards/BIS,DER_D9,1.0 · derivados negociados en bolsa, según la página índice de ISDA: http://www.bis.org/statistics/extderiv.htm)
- **Emisor:** Bank for International Settlements (BIS)
- **Documentación y notas:** Estadística semestral (junio y diciembre) de importes nocionales y valores brutos de mercado de derivados OTC por riesgo (tipos, divisas, renta variable, materias primas, CDS), con 12 países y 65 dealers declarantes; ampliada cada tres años por la Encuesta Trienal (más de 30 jurisdicciones adicionales). Publicación de 08/12/2025 (fin de junio de 2025): 846 billones de dólares de nocional (+16 %), 21,8 billones de valor bruto de mercado (+29 %), tipos de interés el 79 % del total. Pieza temática de RF-0003 (portal general de estadísticas del BIS), registrada aparte como RF-0070.
- **Temática:** TFX-06 Volatilidad y opciones de divisas: mercados y datos (principal) · secundarias: TFX-05, TFX-03
- **Calidad Q:** 88 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** primaria (estadística oficial coordinada por bancos centrales)
- **Acceso:** Abierto (API y descargas en data.bis.org)
- **Ámbitos:** Tamaño, composición y riesgo de contraparte del mercado mundial de derivados OTC
- **Motivo de inclusión y uso:** Medida de referencia del tamaño y la evolución de los mercados de swaps, opciones OTC y CDS. Uso en el Bloque A Forex: La Encuesta Trienal (abril, cada tres años) es la medida de referencia del volumen de contado, forwards, swaps de divisas y opciones de divisas por divisa, par y plaza; la semestral da nocionales y valores de mercado de derivados de divisas OTC. TR-PFV (AG-21) para el tamaño y la liquidez del mercado de opciones por par; AS-ESTR (AG-08) y los seis Analistas de segmento para valorar la profundidad de cada divisa; MOTOR (MC de volatilidad) como contexto de liquidez.
- **Restricciones de uso:** Uso libre con atribución.
- **Sesgos y cautelas:** Semestral con unos cinco meses de desfase; los años entre encuestas trienales incluyen estimaciones.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «BIS OTC derivatives statistics end-June 2026 notional ISDA SwapsInfo»; WebFetch: sí)
- **Origen:** Reutilizada de F9 V3.2 (TF-17) en el Bloque A Forex V1.0 (2026-11-02).

#### RF-0541 · Q 87 (A) — CFTC — Weekly Swaps Report

- **Canal oficial (URL raíz):** https://www.cftc.gov/index.php/MarketReports/SwapsReports/index.htm (archivo: https://www.cftc.gov/MarketReports/SwapsReports/Archive/index.htm)
- **Emisor:** U.S. Commodity Futures Trading Commission (CFTC)
- **Documentación y notas:** Informe semanal (lunes, 15:30 ET) con nocional bruto vivo por tipo de participante, estado de compensación y producto (últimas cinco semanas) y volumen de transacciones de swaps de tipos, CDS y swaps de divisas (importe y número de operaciones), a partir de los registros de swaps (CME SDR, DTCC Data Repository, ICE Trade Vault); archivo completo desde su inicio. Canal distinto de RF-0049 (COT).
- **Temática:** TFX-06 Volatilidad y opciones de divisas: mercados y datos (principal) · secundarias: TFX-05
- **Calidad Q:** 87 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** primaria (agregación supervisora de datos de registros)
- **Acceso:** Abierto
- **Ámbitos:** Swaps de tipos, crédito y divisas bajo jurisdicción de la CFTC
- **Motivo de inclusión y uso:** Pulso semanal de la actividad de swaps (cobertura de tipos, demanda de protección de crédito). Uso en el Bloque A Forex: El informe semanal de la CFTC desglosa los nocionales brutos de swaps por clase de activo, incluida la de divisas (forwards, swaps y opciones de divisas notificados a los SDR). TR-PFV (AG-21) para seguir la actividad agregada de derivados de divisas OTC en EE. UU.; CONTRA (AG-11) como contraste de tamaño.
- **Restricciones de uso:** Dominio público.
- **Sesgos y cautelas:** Solo swaps declarados bajo reglas de la CFTC (no cubre swaps basados en valores de la SEC); cambios de registros afectan a la serie.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Bloomberg SDR operó entre 2014 y 2018.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «CFTC Weekly Swaps Report interest rate swaps notional»; WebFetch: sí)
- **Origen:** Reutilizada de F9 V3.2 (TF-17) en el Bloque A Forex V1.0 (2026-11-02).

#### RF-0547 · Q 85 (A) — OCC (Office of the Comptroller of the Currency) — Quarterly Report on Bank Trading and Derivatives Activities

- **Canal oficial (URL raíz):** https://occ.gov/publications-and-resources/publications/quarterly-report-on-bank-trading-and-derivatives-activities/index-quarterly-report-on-bank-trading-and-derivatives-activities.html (archivo histórico en el mismo directorio, p. ej. https://www.occ.gov/publications-and-resources/publications/quarterly-report-on-bank-trading-and-derivatives-activities/files/q2-2013-derivatives-quarterly.html)
- **Emisor:** Office of the Comptroller of the Currency (Tesoro de EE. UU.)
- **Documentación y notas:** Informe trimestral, basado en los informes de condición (Call Reports) de bancos y holdings, con importes nocionales de derivados por tipo y contrato, exposición crediticia, concentración en los mayores bancos e ingresos de trading; serie disponible desde 1995. Ediciones vigentes: primer y segundo trimestre de 2026 (la del segundo trimestre, difundida en septiembre de 2026). No confundir con The Options Clearing Corporation (RF-0463).
- **Temática:** TFX-06 Volatilidad y opciones de divisas: mercados y datos (principal) · secundarias: TFX-05
- **Calidad Q:** 85 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 8/10
- **Tipología:** primaria (datos supervisores de informes de condición bancaria)
- **Acceso:** Abierto y gratuito
- **Ámbitos:** Derivados en balance de los bancos de EE. UU.; ingresos de trading
- **Motivo de inclusión y uso:** Concentración, volumen nocional y riesgo de contraparte de derivados en el sistema bancario estadounidense; ingresos de trading como termómetro de la actividad de los dealers. Uso en el Bloque A Forex: El informe trimestral de la OCC desglosa los nocionales de derivados de los bancos estadounidenses por tipo, incluidos los contratos de divisas (forwards, swaps y opciones). TR-PFV (AG-21) para la concentración de los grandes dealers en derivados de divisas.
- **Restricciones de uso:** Dominio público.
- **Sesgos y cautelas:** Solo entidades con licencia federal o holdings de EE. UU.; el nocional sobrestima el riesgo económico (compresión y compensación). La página índice no cargó en esta sesión (error del servidor); URL vigente confirmada en los resultados de búsqueda junto con la cobertura de prensa de las ediciones de 2026.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Migración del sitio de occ.treas.gov a occ.gov (URL antigua sustituida en esta revisión).
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «OCC Quarterly Report on Bank Trading and Derivatives Activities 2026»; WebFetch: intento fallido, error del servidor de occ.gov)
- **Origen:** Reutilizada de F9 V3.2 (TF-17) en el Bloque A Forex V1.0 (2026-11-02).

#### RF-0560 · Q 84 (A) — ESMA — Annual Statistical Report on EU Derivatives Markets (datos EMIR) y ESMA Statistics on Securities and Markets

- **Canal oficial (URL raíz):** https://www.esma.europa.eu/sites/default/files/library/esma50_157_2025_asr_derivatives.pdf (edición de 2019, datos de 2018) · ediciones de 2020 y 2021: https://www.esma.europa.eu/sites/default/files/library/esma50-165-1362_asr_derivatives_2020.pdf y https://www.esma.europa.eu/sites/default/files/library/esma50-165-2001_emir_asr_derivatives_2021.pdf · estadística estructural más reciente (12/12/2025, tabla 7 de derivados): https://www.esma.europa.eu/sites/default/files/2025-12/ESMA11-239717167-20877_ESMA_statistics_on_securities_and_markets.pdf
- **Emisor:** European Securities and Markets Authority (ESMA)
- **Documentación y notas:** Informe estadístico anual sobre los derivados de la UE a partir de los datos de los registros de operaciones bajo EMIR: nocional vivo, número de operaciones, reparto por clase de activo, compensación central, negociación en plataforma y contrapartes (edición de 2019: 735 billones de euros a fin de 2018; tipos de interés 76 %; 63 % del nocional OTC de tipos compensado centralmente, 25 % en crédito). La «ESMA Statistics on Securities and Markets» de diciembre de 2025 actualiza el nocional del EEE30 a 27/12/2024: 29,0 millones de contratos y 379.140 miles de millones de euros (tipos 314.569).
- **Temática:** TFX-06 Volatilidad y opciones de divisas: mercados y datos (principal) · secundarias: TFX-05
- **Calidad Q:** 84 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 6/10 · Acceso 9/10
- **Tipología:** primaria (estadística supervisora sobre datos regulatorios)
- **Acceso:** Abierto y gratuito (PDF)
- **Ámbitos:** Derivados OTC y cotizados de la UE/EEE por clase de activo; compensación central
- **Motivo de inclusión y uso:** Fuente europea oficial del tamaño y la estructura del mercado de derivados de la UE, complementaria de BIS (RF-0540) y de los datos de EE. UU. (RF-0541). Uso en el Bloque A Forex: El informe anual de ESMA sobre datos EMIR cuantifica nocionales de derivados por clase de activo, con la clase de divisas (forwards, swaps y opciones) desglosada en la UE. TR-PFV (AG-21) para el tamaño y la compensación de los derivados de divisas en la UE; AS-G10N para EUR.
- **Restricciones de uso:** Uso libre con atribución.
- **Sesgos y cautelas:** Calidad de datos de EMIR mejorable (ESMA lo reconoce); cifras de distintas ediciones no siempre comparables por cambios de perímetro y metodología; la serie de informes anuales específicos parece más espaciada (última edición específica no confirmada en esta sesión). Pieza distinta de RF-0027 (informes de tendencias y riesgos).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Cambios de perímetro tras el Brexit y con EMIR Refit.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ESMA Annual Statistical Report EU derivatives markets 2025 EMIR data»; WebFetch: sí, PDF de la edición de 2019 y PDF de la estadística de diciembre de 2025)
- **Origen:** Reutilizada de F9 V3.2 (TF-17) en el Bloque A Forex V1.0 (2026-11-02).

#### RF-0546 · Q 83 (A) — Deutsche Bundesbank — estadística de derivados OTC (contribución a la encuesta semestral del BIS)

- **Canal oficial (URL raíz):** https://www.bundesbank.de/en/statistics/banks-and-other-financial-corporations/banks/otc-derivatives/otc-derivatives-793960 (sección: https://bundesbank.de/en/statistics/banks-and-other-financial-corporations/banks/otc-derivatives)
- **Emisor:** Deutsche Bundesbank
- **Documentación y notas:** Estadística semestral de nocionales y valores brutos de mercado de derivados OTC (divisas, tipos, renta variable, materias primas y crédito) y exposiciones crediticias antes y después de compensación, dentro del ejercicio coordinado por el BIS; tablas en la serie estadística de banca y series en el portal estadístico; directrices (en alemán) de 01/07/2026.
- **Temática:** TFX-06 Volatilidad y opciones de divisas: mercados y datos (principal) · secundarias: TFX-03
- **Calidad Q:** 83 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 6/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Derivados OTC de los dealers alemanes
- **Motivo de inclusión y uso:** Desglose nacional europeo del mercado OTC (complemento de RF-0540). Uso en el Bloque A Forex: La contribución del Bundesbank a la encuesta semestral del BIS ofrece el desglose alemán de derivados OTC, incluidos los contratos de divisas, con nota metodológica pública. TR-PFV (AG-21) como serie nacional de contraste para el euro.
- **Restricciones de uso:** Uso libre con atribución.
- **Sesgos y cautelas:** Semestral; la página no indica la última fecha de referencia.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Directrices actualizadas en julio de 2026.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «BIS OTC derivatives statistics end-June 2026 notional ISDA SwapsInfo»; WebFetch: sí)
- **Origen:** Reutilizada de F9 V3.2 (TF-17) en el Bloque A Forex V1.0 (2026-11-02).

#### FXF-0201 · Q 80 (A) — Federal Reserve Bank of Minneapolis — Market-Based Probabilities (probabilidades implícitas en opciones, incluidos tipos de cambio)

- **Canal oficial (URL raíz):** https://www.minneapolisfed.org/banking/current-and-historical-market-based-probabilities (antecedentes y metodología: https://minneapolisfed.org/banking/current-and-historical-market--based-probabilities/market-based-probabilities-background-commentary-and-analysis)
- **Emisor:** Federal Reserve Bank of Minneapolis
- **Documentación y notas:** Distribuciones de probabilidad neutrales al riesgo derivadas de precios de cierre de opciones con volumen positivo en los cinco días previos; cubre materias primas, renta variable, tipos de interés y tipos de cambio (opciones sobre futuros de tipos de cambio individuales; el euro como ejemplo). Ofrece gráficos de estadísticos históricos y descarga CSV de estadísticos con diccionario de datos. Las probabilidades de inflación se interrumpieron en mayo de 2025. Archivo de informes PDF desde 2012.
- **Temática:** TFX-06 Volatilidad y opciones de divisas: mercados y datos (principal) · secundarias: TFX-05
- **Calidad Q:** 80 (A) — Primariedad 17/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 14/15 · Independencia 10/10 · Actualidad 7/10 · Acceso 9/10
- **Tipología:** primaria (cálculo propio de un banco de la Reserva Federal sobre precios de opciones)
- **Acceso:** Abierto
- **Ámbitos:** Densidades implícitas, probabilidades de grandes movimientos, sesgo y curtosis implícitos por activo, incluidos tipos de cambio
- **Motivo de inclusión y uso:** Única fuente oficial abierta que publica densidades implícitas de tipos de cambio con método documentado. Uso: TR-PFV (AG-21) para probabilidades de movimientos extremos por par; CONTRA (AG-11) para comprobar lo que ya descuenta el mercado de opciones; PROS (AG-10) como referencia de bandas de probabilidad.
- **Restricciones de uso:** Uso libre con atribución; citar fecha y activo.
- **Sesgos posibles:** Densidades neutrales al riesgo (incluyen prima de riesgo); cobertura de divisas limitada a los futuros con opciones líquidas; la página no detalla la lista completa de divisas.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Interrupción de la serie de inflación (mayo de 2025); vigilar posibles recortes de cobertura.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Minneapolis Fed market-based probabilities currencies euro yen option prices»; WebFetch: sí, página principal)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-06).

#### RF-0552 · Q 80 (A) — ESMA — intervención de producto sobre CFD y opciones binarias

- **Canal oficial (URL raíz):** https://esma.europa.eu/investor-corner/product-intervention (también https://www.esma.europa.eu/node/200006 · opinión sobre las medidas españolas de CFD: https://www.esma.europa.eu/sites/default/files/library/esma-35-43-1935-esma_opinion_under_article_432_mifir_es_cfd.pdf)
- **Emisor:** European Securities and Markets Authority (ESMA)
- **Documentación y notas:** Página de intervención de producto: medidas temporales de ESMA (2018-2019) sobre CFD y opciones binarias a minoristas (límites de apalancamiento, cierre de posiciones por margen, protección de saldo negativo, advertencia con el porcentaje de cuentas con pérdidas), medidas nacionales permanentes adoptadas después por las autoridades competentes y opiniones de ESMA sobre ellas (art. 43 MiFIR).
- **Temática:** TFX-06 Volatilidad y opciones de divisas: mercados y datos (principal) · secundarias: TFX-09
- **Calidad Q:** 80 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 5/10 · Acceso 8/10
- **Tipología:** primaria (normativa supervisora)
- **Acceso:** Abierto
- **Ámbitos:** Derivados minoristas apalancados (CFD, opciones binarias) en la UE
- **Motivo de inclusión y uso:** Marco regulatorio que delimita el acceso minorista a derivados apalancados en Europa. Uso en el Bloque A Forex: Las medidas de ESMA sobre CFD (límites de apalancamiento por clase de subyacente, con los pares de divisas principales en el tramo de mayor apalancamiento permitido) acotan el mercado minorista de divisas en la UE. CONTRA (AG-11) y AS-ESTR (AG-08) para contextualizar el posicionamiento minorista y las restricciones regulatorias.
- **Restricciones de uso:** Uso libre con atribución.
- **Sesgos y cautelas:** La página no cargó en esta sesión (error del sitio); contenido confirmado por resultados de búsqueda. Pieza temática distinta de RF-0027.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Medidas temporales de ESMA sustituidas por medidas nacionales.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «ESMA CFD product intervention measures retail investors national competent authorities»; WebFetch: intento fallido, error del sitio)
- **Origen:** Reutilizada de F9 V3.2 (TF-17) en el Bloque A Forex V1.0 (2026-11-02).

#### RF-0554 · Q 80 (A) — V-Lab (NYU Stern) — análisis y previsiones de volatilidad, correlación y riesgo sistémico

- **Canal oficial (URL raíz):** https://vlab.stern.nyu.edu/ (ayuda del resumen de volatilidad: https://vlab.stern.nyu.edu/help/volatility_summary · análisis: https://vlab.stern.nyu.edu/help/volatility_analysis)
- **Emisor:** V-Lab, NYU Stern School of Business (Volatility Institute)
- **Documentación y notas:** Doce modelos de volatilidad (GARCH, GJR-GARCH por defecto, EGARCH, APARCH, Spline-GARCH, MEM, GAS, MF2-GARCH) reestimados a diario tras el cierre, con previsiones a 1 día, 1 semana, 1 mes, 6 meses y 1 año para miles de activos; además análisis de correlación, VaR a largo plazo y SRISK (riesgo sistémico).
- **Temática:** TFX-06 Volatilidad y opciones de divisas: mercados y datos (principal) · secundarias: TMX-02
- **Calidad Q:** 80 (A) — Primariedad 14/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 13/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** analítica (modelos académicos sobre precios de mercado)
- **Acceso:** Abierto
- **Ámbitos:** Volatilidad realizada y prevista de acciones, índices, divisas, materias primas
- **Motivo de inclusión y uso:** Contraste de la volatilidad implícita (VIX y similares) con previsiones econométricas; régimen de volatilidad por mercado. Uso en el Bloque A Forex: V-Lab publica previsiones GARCH de volatilidad para series de divisas e índices de volatilidad cambiaria (p. ej., página de V-Lab para el índice CVIX de Deutsche Bank, devuelta en la búsqueda del 02/11/2026). TR-PFV (AG-21) para contrastar la volatilidad implícita con previsiones de volatilidad realizada; MOTOR (AG-13) como referencia externa de su módulo de volatilidad.
- **Restricciones de uso:** Uso académico con atribución.
- **Sesgos y cautelas:** Resultados dependientes del modelo; algunos activos inactivos conservan su último valor.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «V-Lab NYU Stern volatility laboratory GARCH forecasts»; WebFetch: sí)
- **Origen:** Reutilizada de F9 V3.2 (TF-17) en el Bloque A Forex V1.0 (2026-11-02).

#### FXF-0202 · Q 76 (B) — LSEG — FX Option Volatility Surfaces (superficies de volatilidad de opciones de divisas)

- **Canal oficial (URL raíz):** https://www.lseg.com/en/data-catalogue/forex-and-money-market/derived/options-fx-option-volatility-surfaces (analítica de superficies: https://www.lseg.com/en/data-analytics/financial-data/analytics/pricing-analytics/volatility-surfaces-analytics)
- **Emisor:** London Stock Exchange Group (LSEG Data & Analytics, antes Refinitiv)
- **Documentación y notas:** Superficies de volatilidad implícita de opciones de divisas para los principales pares de todas las regiones (unos 30.000 RIC en la clase «Forex, FX & Money»), construidas a partir de cotizaciones compradoras y vendedoras de volatilidad ATM y de butterflies y risk reversals de 10 y 25 delta, por vencimiento y delta o precio de ejercicio; historia desde 2006; tiempo real e histórico; entrega por API, SFTP (Datastream Data Loader), nube, escritorio o Excel.
- **Temática:** TFX-06 Volatilidad y opciones de divisas: mercados y datos (principal) · secundarias: TFX-05
- **Calidad Q:** 76 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 14/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 7/10
- **Tipología:** primaria (datos de mercado agregados por un proveedor)
- **Acceso:** De pago (licencia LSEG Workspace/Datastream); credenciales en HT-01
- **Ámbitos:** Volatilidad implícita ATM, risk reversals y butterflies por par y plazo; estructura temporal de la volatilidad
- **Motivo de inclusión y uso:** Fuente profesional de la superficie completa de volatilidad cambiaria, necesaria para risk reversals y estructura de plazos. Uso: TR-PFV (AG-21) para el informe de volatilidad; MOTOR (AG-13, módulo de opciones de divisas) como entrada de cálculo; AS-ESTR (AG-08) para estrategias de volatilidad.
- **Restricciones de uso:** Licencia comercial; solo se citan valores agregados; no redistribuir.
- **Sesgos posibles:** La página no nombra a los contribuidores; las superficies dependen de cotizaciones indicativas de brókeres y bancos.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Integrado en LSEG tras la compra de Refinitiv (2021); vigilar cambios de RIC.
- **Estado:** Aprobada
- **Estado del enlace:** MURO_PAGO
- **Última verificación:** 2026-11-02 (búsqueda web: «FX options implied volatility surface data LSEG Workspace Bloomberg OVDV risk reversals butterflies data provider»; WebFetch: sí, ficha del catálogo de datos)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-06).

#### RF-0542 · Q 76 (B) — FIA — informes mensuales y anuales de volumen de derivados cotizados (ETD Volume)

- **Canal oficial (URL raíz):** https://www.fia.org/etd-volume-reports (informe de diciembre de 2025: https://www.fia.org/fia/articles/etd-volume-december-2025 · resumen anual: https://fia.org/node/2439 · datos: https://www.fia.org/data-1)
- **Emisor:** FIA (Futures Industry Association)
- **Documentación y notas:** Informes mensuales y anuales de volumen e interés abierto de futuros y opciones cotizados por región, clase de activo y bolsa (ETD Tracker). 2025: 119,29 miles de millones de contratos (−42,2 %; opciones −50,3 % por la caída de opciones sobre índices en la India; futuros +8,6 %), interés abierto de 1,52 miles de millones de contratos a fin de diciembre (+22,8 %).
- **Temática:** TFX-06 Volatilidad y opciones de divisas: mercados y datos (principal) · secundarias: TFX-05
- **Calidad Q:** 76 (B) — Primariedad 17/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 14/15 · Independencia 6/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** secundaria (agregación de datos de bolsas)
- **Acceso:** Resúmenes abiertos; ETD Tracker con detalle por bolsa
- **Ámbitos:** Derivados cotizados mundiales
- **Motivo de inclusión y uso:** Panorama mundial de la actividad de derivados cotizados por región y clase de activo. Uso en el Bloque A Forex: Los informes de volumen de FIA desglosan los derivados cotizados por categoría, incluida la de divisas (futuros y opciones de divisas en CME, B3, NSE, Moscú y otras bolsas). TR-PFV (AG-21) para comparar la actividad de opciones de divisas cotizadas por bolsa y región; AS-EMLA y AS-EMAS para BRL e INR.
- **Restricciones de uso:** Uso con atribución.
- **Sesgos y cautelas:** Patronal del sector; el recuento por contratos mezcla tamaños nominales muy distintos.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «FIA annual global futures and options volume 2025 exchange-traded derivatives WFE derivatives report»; WebFetch: sí)
- **Origen:** Reutilizada de F9 V3.2 (TF-17) en el Bloque A Forex V1.0 (2026-11-02).

#### RF-0545 · Q 76 (B) — ISDA — investigación y SwapsInfo (volúmenes de derivados OTC)

- **Canal oficial (URL raíz):** https://www.isda.org/ (revisión SwapsInfo del 1S 2026, 11/08/2026: https://www.isda.org/2026/08/11/swapsinfo-first-half-of-2026-and-the-second-quarter-of-2026-review/ · SwapsInfo: https://www.swapsinfo.org/ · directorio de fuentes de datos OTC: https://www.isda.org/1985/01/01/otc-derivatives-data-sources · encuestas: https://www.isda.org/category/research/surveys/)
- **Emisor:** International Swaps and Derivatives Association (ISDA)
- **Documentación y notas:** SwapsInfo: volúmenes y número de operaciones de derivados de tipos y de crédito a partir de datos públicos de registros (1S 2026: 318,5 billones de dólares negociados en derivados de tipos, +27,3 %, impulsados por OIS; 12,5 billones en índices de crédito, +18,5 %); revisiones trimestrales, encuesta de márgenes y notas de tendencias clave; directorio de fuentes de datos OTC.
- **Temática:** TFX-06 Volatilidad y opciones de divisas: mercados y datos (principal) · secundarias: TFX-05
- **Calidad Q:** 76 (B) — Primariedad 17/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 14/15 · Independencia 5/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** secundaria (agregación de datos públicos por la patronal)
- **Acceso:** Abierto
- **Ámbitos:** Swaps de tipos, CDS sobre índices y single-name
- **Motivo de inclusión y uso:** Actividad de swaps por producto y divisa y tendencias del mercado OTC. Uso en el Bloque A Forex: ISDA publica investigación sobre derivados OTC y márgenes; SwapsInfo agrega los datos públicos de los SDR estadounidenses (principalmente tipos y crédito; la cobertura de divisas debe comprobarse pieza a pieza). TR-PFV (AG-21) para contexto de mercado y convenciones de documentación de opciones de divisas.
- **Restricciones de uso:** Uso con atribución.
- **Sesgos y cautelas:** Patronal de los dealers (posiciones de lobby en sus análisis); datos basados en registros de EE. UU.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «BIS OTC derivatives statistics end-June 2026 notional ISDA SwapsInfo»; WebFetch: sí, revisión SwapsInfo y directorio)
- **Origen:** Reutilizada de F9 V3.2 (TF-17) en el Bloque A Forex V1.0 (2026-11-02).

#### RF-0562 · Q 76 (B) — CME Group — CVOL (CME Group Volatility Indexes): volatilidad implícita de tipos, divisas y materias primas

- **Canal oficial (URL raíz):** https://www.cmegroup.com/market-data/cme-group-benchmark-administration/cme-group-volatility-indexes-faq.html (introducción: https://www.cmegroup.com/education/articles-and-reports/introduction-to-the-cme-group-volatility-index-cvol.html · guía de cálculo en tiempo real: https://www.cmegroup.com/market-data/cme-group-benchmark-administration/files/live-streaming-index-calculation-guide.pdf)
- **Emisor:** CME Group Benchmark Administration Limited (CBA)
- **Documentación y notas:** Familia de índices de volatilidad implícita a 30 días basados en varianza simple (admite precios negativos) calculados con opciones sobre futuros: tipos (STIR y bonos del Tesoro, p. ej. el de 10 años), divisas G5, agrícolas, energía, metales y un índice transversal de materias primas (32 productos más 6 índices amplios). Publica además UpVar/DnVar, sesgo (skew), convexidad y volatilidad ATM. Índices de cierre registrados bajo el BMR del Reino Unido y diseñados según los principios de IOSCO; los CVOL de Eurodólar dejaron de publicarse (historia en DataMine).
- **Temática:** TFX-06 Volatilidad y opciones de divisas: mercados y datos (principal) · secundarias: TFX-05
- **Calidad Q:** 76 (B) — Primariedad 18/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 13/15 · Independencia 6/10 · Actualidad 10/10 · Acceso 6/10
- **Tipología:** primaria (índice de referencia calculado sobre precios de opciones cotizadas)
- **Acceso:** Visualizador web con últimos valores (solo consulta, no comercial); histórico de cierre en CME DataMine con registro; flujo en tiempo real vía redistribuidores
- **Ámbitos:** Volatilidad implícita de tipos de interés, divisas y materias primas
- **Motivo de inclusión y uso:** Medida homogénea de volatilidad implícita fuera de la renta variable (complemento del VIX y del MOVE, RF-0561), con sesgo put/call por mercado. Uso en el Bloque A Forex: Los CVOL de divisas G5, con su sesgo UpVar/DnVar, dan una lectura homogénea de volatilidad implícita y del sesgo de cola por par. TR-PFV (AG-21) para el nivel y la estructura de volatilidad implícita; AS-G10N, AS-G10M y AS-EMLA para opciones de tipo VOLATILIDAD; AS-ESTR para estrategias de volatilidad sobre varias divisas.
- **Restricciones de uso:** Visualizador solo para referencia; uso comercial con licencia.
- **Sesgos y cautelas:** Administrador que es a la vez la bolsa que lista las opciones subyacentes; historia relativamente corta (desde 2020); no comparable directamente con índices de varianza logarítmica como el VIX.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Cese de los CVOL de Eurodólar tras la transición del LIBOR.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «CME Group CVOL index methodology implied volatility rates FX commodities»; WebFetch: sí, FAQ de CVOL)
- **Origen:** Reutilizada de F9 V3.2 (TF-17) en el Bloque A Forex V1.0 (2026-11-02).

#### FXF-0203 · Q 75 (B) — TFS-ICAP FX Options (datos en CME DataMine)

- **Canal oficial (URL raíz):** https://www.cmegroup.com/market-data/browse-data/catalog/tfs-icap-fx-options.html (ficha técnica: https://cmegroup.com/market-data/browse/files/tfs-icap-fx-options-fact-sheet.pdf)
- **Emisor:** TFS-ICAP (bróker interdealer de opciones de divisas), distribuido por CME Group DataMine
- **Documentación y notas:** Precios de más de 50 pares procedentes de la plataforma de TFS-ICAP: straddles ATM indicativos (puntos ATM hasta 20 años en los pares más líquidos) y superficie completa con butterflies y risk reversals de 10 y 25 delta; flujo 24 horas. Entrega por API, SFTP, S3, WebSocket o distribuidores autorizados; requiere acuerdo de licencia (ILA).
- **Temática:** TFX-06 Volatilidad y opciones de divisas: mercados y datos (principal) · secundarias: —
- **Calidad Q:** 75 (B) — Primariedad 17/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 13/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 7/10
- **Tipología:** primaria (cotizaciones del mercado interdealer de opciones de divisas OTC)
- **Acceso:** De pago (licencia DataMine)
- **Ámbitos:** Volatilidad implícita OTC de divisas por par, plazo y delta; plazos largos
- **Motivo de inclusión y uso:** Fuente directa del mercado interdealer de opciones de divisas OTC, que es donde se forma la superficie. Uso: TR-PFV (AG-21) como contraste de la superficie de LSEG (FXF-0202); MOTOR (AG-13) para plazos largos.
- **Restricciones de uso:** Licencia comercial; uso interno.
- **Sesgos posibles:** Cotizaciones indicativas que dependen de la liquidez de la plataforma; la página no indica la profundidad histórica.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** MURO_PAGO
- **Última verificación:** 2026-11-02 (búsqueda web: «FX options implied volatility surface data LSEG Workspace Bloomberg OVDV risk reversals butterflies data provider»; WebFetch: sí, página del catálogo de CME)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-06).

#### FXF-0204 · Q 74 (B) — CME Group — futuros y opciones de divisas (volumen, interés abierto e informes del área FX)

- **Canal oficial (URL raíz):** https://www.cmegroup.com/trading/fx/files/fx-quarterly-review.pdf (nota de prensa del récord de interés abierto del 07/09/2026: https://www.cmegroup.com/media-room/press-releases/2026/9/07/cme_group_sets_newfxopeninterestrecord.html · FX Report: https://cmegroup.com/education/fx-report/2018-06-fx-report.html)
- **Emisor:** CME Group (Chicago Mercantile Exchange)
- **Documentación y notas:** Mayor mercado regulado de futuros y opciones sobre futuros de divisas (EUR/USD, JPY, GBP, CAD, AUD, CHF, MXN, BRL…). Nota de 07/09/2026: récord de interés abierto en futuros y opciones de divisas de 4.410.167 contratos el 04/09/2026 (anterior: 4.269.622 el 11/06/2026); 1.446 grandes tenedores en futuros según el COT de la CFTC del 25/08; las gestoras superaron 200.000 millones de dólares de nocional abierto. Publica revisiones trimestrales del área FX.
- **Temática:** TFX-06 Volatilidad y opciones de divisas: mercados y datos (principal) · secundarias: TFX-05
- **Calidad Q:** 74 (B) — Primariedad 17/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 13/15 · Independencia 5/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria (estadística de la bolsa)
- **Acceso:** Abierto (notas de prensa, informes); datos detallados en DataMine (de pago)
- **Ámbitos:** Volumen e interés abierto de futuros y opciones de divisas cotizados; participación de gestoras
- **Motivo de inclusión y uso:** La actividad de opciones de divisas cotizadas complementa los datos OTC y es la base de los CVOL de divisas (RF-0562). Uso: TR-PFV (AG-21) para el interés abierto y la participación institucional por divisa; AS-G10N, AS-G10M y AS-EMLA (MXN, BRL).
- **Restricciones de uso:** Notas de prensa de uso libre con atribución; datos de DataMine con licencia.
- **Sesgos posibles:** Comunicación comercial de la propia bolsa (énfasis en récords); el mercado cotizado es una fracción del OTC.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «CME Group FX options open interest record EUR/USD options on futures weekly options»; WebFetch: sí, nota de prensa del 07/09/2026)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-06).

#### FXF-0205 · Q 72 (B) — TraditionData — Global FX and FX Options (volatilidad de opciones de divisas de Tradition/Volbroker)

- **Canal oficial (URL raíz):** https://www.traditiondata.com/wp-content/uploads/2023/02/Global-FX-and-FX-Options-Package-TraditionData-Q2-2023.pdf (sitio: https://www.traditiondata.com/?p=7130)
- **Emisor:** TraditionData (división de datos de Compagnie Financière Tradition)
- **Documentación y notas:** Volatilidad ATM, risk reversals y butterflies de 25 y 10 delta para 57 pares; producto ampliado con superficies de 1 semana a 30 años según divisa y liquidez; tres capturas diarias (cierres de Londres, Nueva York y Tokio). Precios de su negocio interdealer (voz y la plataforma electrónica Volbroker, integrada en 2001). Folleto de abril de 2023: confirmar la oferta vigente.
- **Temática:** TFX-06 Volatilidad y opciones de divisas: mercados y datos (principal) · secundarias: TFX-05
- **Calidad Q:** 72 (B) — Primariedad 17/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 12/15 · Independencia 7/10 · Actualidad 8/10 · Acceso 8/10
- **Tipología:** primaria (cotizaciones interdealer)
- **Acceso:** De pago (licencia); folleto abierto
- **Ámbitos:** Volatilidad implícita de opciones de divisas OTC, incluidos plazos largos y pares emergentes
- **Motivo de inclusión y uso:** Segunda fuente interdealer independiente de TFS-ICAP para contrastar superficies. Uso: TR-PFV (AG-21) y MOTOR (AG-13) como contraste de datos de volatilidad.
- **Restricciones de uso:** Licencia comercial.
- **Sesgos posibles:** Folleto comercial; profundidad real de liquidez no verificable desde fuera.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos; folleto de 2023.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «FX options implied volatility surface data LSEG Workspace Bloomberg OVDV risk reversals butterflies data provider»; WebFetch: sí, folleto PDF)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-06).

#### RF-0553 · Q 71 (B) — WFE (World Federation of Exchanges) — estadísticas de derivados cotizados (Statistics Portal e informes semestrales)

- **Canal oficial (URL raíz):** https://statistics.world-exchanges.org (sección de estadísticas: https://www.world-exchanges.org/our-work/statistics · informe del 1S 2025, 14/08/2025: https://www.world-exchanges.org/news/articles/new-wfe-hy25-market-data-ipos-down-first-half · documento completo: https://www.world-exchanges.org/our-work/articles/h1-2025-market-highlights · reseña de FOW de los datos anuales de 2025, 27/02/2026: https://www.fow.com/insights/derivatives-trading-volume-decrease-in-2025-wfe-data)
- **Emisor:** World Federation of Exchanges
- **Documentación y notas:** Portal estadístico con volúmenes de contratos de derivados cotizados de las bolsas miembro por región, clase de activo y producto, e informes semestrales y anuales. 1S 2025: 43,92 miles de millones de contratos (−47,8 % interanual, por la regulación de opciones en la India); futuros 14,18 miles de millones (+7,8 %); Américas +11,7 % y EMEA +21,9 % interanual, Asia-Pacífico −64,8 %. Año 2025 (según FOW): 93,75 miles de millones de contratos (−47,1 %). Publica además investigación de estructura de mercado.
- **Temática:** TFX-06 Volatilidad y opciones de divisas: mercados y datos (principal) · secundarias: TFX-05
- **Calidad Q:** 71 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 14/15 · Independencia 6/10 · Actualidad 8/10 · Acceso 6/10
- **Tipología:** secundaria (agregación de datos de bolsas miembro)
- **Acceso:** Notas e informes resumidos abiertos; detalle del portal con registro o suscripción
- **Ámbitos:** Derivados cotizados mundiales; contraste con FIA (RF-0542), que da cifras distintas por cobertura
- **Motivo de inclusión y uso:** Segunda fuente agregada del volumen mundial de derivados cotizados y de su reparto regional. Uso en el Bloque A Forex: Las estadísticas de la WFE incluyen volúmenes de derivados sobre divisas por bolsa miembro. TR-PFV (AG-21) para el peso relativo de las bolsas emergentes en opciones y futuros de divisas.
- **Restricciones de uso:** Uso con atribución.
- **Sesgos y cautelas:** Patronal de bolsas; cobertura limitada a miembros; el recuento por contratos mezcla tamaños muy distintos. El portal estadístico se tomó del enlace de una página oficial leída, sin cargarlo.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sustitución del antiguo informe anual IOMA de derivados por el portal estadístico y los informes de mercado semestrales (URL de pruebas antigua sustituida en esta revisión).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «World Federation of Exchanges 2025 derivatives report statistics world-exchanges.org»; WebFetch: sí, nota del 1S 2025 y página de etiqueta «derivatives»)
- **Origen:** Reutilizada de F9 V3.2 (TF-17) en el Bloque A Forex V1.0 (2026-11-02).

#### FXF-0206 · Q 70 (B) — DTCC Data Repository (DDR) — repositorio de operaciones de divisas notificadas a la CFTC y difusión pública

- **Canal oficial (URL raíz):** No capturado en la verificación (consultar la página de DTCC desde HT-01). Piezas: anuncio de difusión en tiempo real del DDR: https://www.hedgeweek.com/dtcc-sdr-real-time-reporting-now-live/ · índice de noticias sobre el repositorio de divisas de DTCC: https://fx-markets.com/organisations/dtcc?page=1
- **Emisor:** The Depository Trust & Clearing Corporation (DTCC), DTCC Data Repository (U.S.) LLC, registrado como SDR ante la CFTC
- **Documentación y notas:** Según FX Markets, DTCC lanzó su repositorio de divisas en enero de 2013, con plazo para que los dealers notificaran operaciones de divisas hasta el 28/02/2013 (Dodd-Frank). El DDR difunde en tiempo real precios de swaps notificados mediante transferencia de ficheros, RSS, página de cotizaciones, exportación a Excel y búsqueda (Hedgeweek, 04/01/2013). La cobertura concreta de opciones y forwards de divisas en la difusión pública debe confirmarse en la página de DTCC.
- **Temática:** TFX-06 Volatilidad y opciones de divisas: mercados y datos (principal) · secundarias: TFX-05
- **Calidad Q:** 70 (B) — Primariedad 17/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 13/15 · Independencia 7/10 · Actualidad 7/10 · Acceso 5/10
- **Tipología:** primaria (datos regulatorios notificados)
- **Acceso:** Difusión pública gratuita de operaciones anonimizadas; datos completos solo para reguladores
- **Ámbitos:** Operaciones OTC de divisas (opciones, forwards no entregables, swaps) notificadas en EE. UU.
- **Motivo de inclusión y uso:** Única vía pública operación a operación para observar precios y tamaños de opciones de divisas OTC en EE. UU. Uso: TR-PFV (AG-21) para flujos de opciones (vencimientos y strikes con gran volumen) y NDF de divisas emergentes (AS-EMAS, AS-EMLA).
- **Restricciones de uso:** Uso según condiciones de DTCC; datos con tope de tamaño (capped) y retardos.
- **Sesgos posibles:** Solo operaciones sujetas a notificación en EE. UU.; tamaños topados; posibles duplicados entre SDR.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Cambios de las reglas de notificación de la CFTC (campos y formatos) desde 2022; vigilar.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «DTCC public price dissemination dashboard FX options swap data repository CFTC»; WebFetch: sí, sobre Hedgeweek y sobre el índice de FX Markets; la página de DTCC no se leyó)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-06).

#### FXF-0207 · Q 66 (B) — J.P. Morgan Global FX Volatility Index

- **Canal oficial (URL raíz):** No capturado (índice propietario difundido por terminales). Piezas: lanzamiento del índice de volatilidad de divisas de J.P. Morgan: https://www.risk.net/derivatives/structured-products/1498539/jp-morgan-launches-forex-volatility-index · artículo de Euromoney (04/07/2024): https://www.euromoney.com/article/2dgalxn73hd2ftqqnb8qo/foreign-exchange/fx-volatility-indices-useful-or-not/ · récord mínimo de 5,21 (FXStreet): https://www.fxstreet.com/amp/news/jp-morgans-global-fx-volatility-index-hits-record-low-202001210122
- **Emisor:** J.P. Morgan
- **Documentación y notas:** Índice de volatilidad implícita global de divisas calculado con precios de opciones; Euromoney lo cita con el CVIX de Deutsche Bank como principales índices propietarios. Mínimo histórico de 5,21 en enero de 2020; según datos de Bloomberg citados por FXStreet, sus tres mínimos en 25 años precedieron movimientos del índice dólar superiores al 10 %. Metodología detallada no pública.
- **Temática:** TFX-06 Volatilidad y opciones de divisas: mercados y datos (principal) · secundarias: TFX-08
- **Calidad Q:** 66 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 6/15 · Autoridad 13/15 · Independencia 6/10 · Actualidad 10/10 · Acceso 7/10
- **Tipología:** primaria (índice propietario de un banco)
- **Acceso:** Terminales de pago; citas frecuentes en prensa
- **Ámbitos:** Nivel agregado de volatilidad implícita del mercado de divisas G7 y global
- **Motivo de inclusión y uso:** Termómetro de referencia del régimen de volatilidad cambiaria más citado por la prensa. Uso: TR-PFV (AG-21) para el régimen de volatilidad global; AS-ESTR (AG-08) para el carry (la volatilidad baja favorece el carry); CONTRA (AG-11) para la complacencia del mercado.
- **Restricciones de uso:** Citar solo valores publicados; datos de terminal con licencia.
- **Sesgos posibles:** Índice de un dealer; metodología no publicada; Euromoney recoge críticas sobre la utilidad de estos índices.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"JPMorgan Global FX Volatility Index" OR "Deutsche Bank Currency Volatility Index" CVIX»; WebFetch: sí, sobre Euromoney y FXStreet)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-06).

#### FXF-0208 · Q 64 (C) — Deutsche Bank Currency Volatility Index (CVIX)

- **Canal oficial (URL raíz):** No capturado (índice propietario). Piezas: Euromoney (04/07/2024): https://www.euromoney.com/article/2dgalxn73hd2ftqqnb8qo/foreign-exchange/fx-volatility-indices-useful-or-not/ · previsión de volatilidad del CVIX en V-Lab: https://vlab.stern.nyu.edu/volatility/VOL.CVIX%3AVIND-R.SGARCH
- **Emisor:** Deutsche Bank
- **Documentación y notas:** Índice de volatilidad implícita de una cesta de pares de divisas; Euromoney lo usa como referencia en un ejemplo de swap de volatilidad (el comprador paga el nivel del índice y recibe la volatilidad realizada media ponderada de la cesta). V-Lab (RF-0554) publica previsiones GARCH sobre la serie.
- **Temática:** TFX-06 Volatilidad y opciones de divisas: mercados y datos (principal) · secundarias: TFX-08
- **Calidad Q:** 64 (C) — Primariedad 14/20 · Historial 10/20 · Transparencia 5/15 · Autoridad 12/15 · Independencia 6/10 · Actualidad 10/10 · Acceso 7/10
- **Tipología:** primaria (índice propietario de un banco)
- **Acceso:** Terminales de pago; serie visible en V-Lab
- **Ámbitos:** Volatilidad implícita agregada de divisas
- **Motivo de inclusión y uso:** Segundo índice agregado de volatilidad cambiaria, con contraste de previsión en V-Lab. Uso: TR-PFV (AG-21) como contraste del índice de J.P. Morgan (FXF-0207); MOTOR (AG-13) para comparar volatilidad implícita y prevista.
- **Restricciones de uso:** Citar solo valores publicados.
- **Sesgos posibles:** Índice de un dealer; composición y ponderaciones no detalladas en las fuentes leídas.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «"JPMorgan Global FX Volatility Index" OR "Deutsche Bank Currency Volatility Index" CVIX»; WebFetch: sí, sobre Euromoney; la página de V-Lab no se leyó)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-06).

#### FXF-0209 · Q 58 (C) — Cboe/CME FX Volatility Indexes (EUVIX, BPVIX, JYVIX)

- **Canal oficial (URL raíz):** No capturado en la verificación. Pieza: anuncio de difusión (Hedgeweek, 15/01/2015): https://www.hedgeweek.com/cboe-disseminates-volatility-index-values-three-cme-group-fx-options-contracts/ · metodología general de los índices de volatilidad de Cboe (v. 5.0, 26/02/2026): https://cdn.cboe.com/resources/indices/Cboe_Volatility_Index_Mathematics_Methodology.pdf
- **Emisor:** Cboe Global Markets (cálculo) sobre opciones de CME Group
- **Documentación y notas:** Índices de volatilidad implícita a 30 días del euro (EUVIX), la libra (BPVIX) y el yen (JYVIX) que aplican la metodología del VIX a las opciones sobre futuros de divisas de CME; difusión iniciada en enero de 2015. El documento metodológico de 2026 no menciona estos índices: confirmar que siguen publicándose antes de usarlos.
- **Temática:** TFX-06 Volatilidad y opciones de divisas: mercados y datos (principal) · secundarias: —
- **Calidad Q:** 58 (C) — Primariedad 15/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 12/15 · Independencia 6/10 · Actualidad 2/10 · Acceso 3/10
- **Tipología:** primaria (índice calculado por la bolsa)
- **Acceso:** Desconocido en la fecha; históricos en proveedores de datos
- **Ámbitos:** Volatilidad implícita de EUR/USD, GBP/USD y USD/JPY con metodología VIX
- **Motivo de inclusión y uso:** Serie histórica con metodología pública (tipo VIX) comparable con el VIX de renta variable. Uso: MOTOR (AG-13) y TR-PFV (AG-21) solo como serie histórica; para valores actuales usar los CVOL (RF-0562).
- **Restricciones de uso:** Según condiciones de Cboe.
- **Sesgos posibles:** Vigencia no confirmada; posible discontinuidad.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Vigencia no confirmada en 2026 (pendiente de comprobación por HT-02).
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Cboe FX volatility indexes EUVIX JYVIX BPVIX methodology»; WebFetch: sí, sobre Hedgeweek y sobre el documento metodológico de Cboe)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-06).

## TFX-07 Prensa y agencias especializadas en divisas

#### RF-0222 · Q 79 (B) — Associated Press (AP)

- **Canal oficial (URL raíz):** https://apnews.com/ (noticias) · https://www.ap.org/ (corporativo) (según Wikipedia)
- **Emisor:** The Associated Press (cooperativa sin ánimo de lucro, Nueva York, fundada en 1846)
- **Temática:** TFX-07 Prensa y agencias especializadas en divisas (principal) · secundarias: —
- **Calidad Q:** 79 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 13/15 · Independencia 9/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** primaria (reporterismo de agencia)
- **Acceso:** Abierto (apnews.com)
- **Ámbitos:** Noticias generales, económicas y políticas de EE. UU. y el mundo
- **Motivo de inclusión y uso:** Agencia cooperativa de alcance mundial con acceso abierto; segunda raíz independiente frente a Reuters para corroborar hechos de actualidad. Uso en el Bloque A Forex: Agencia de acceso abierto para hechos políticos y geopolíticos con efecto cambiario. AG-02 y CONTRA (AG-11) como raíz independiente para corroborar hechos.
- **Sesgos y cautelas:** Cobertura financiera menos profunda que la de agencias especializadas; las copias en otros medios son sindicadas (enlazar a la raíz).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «list of news agencies wikipedia» → artículo de Wikipedia «Associated Press»; WebFetch: sí, sobre Wikipedia)
- **Origen:** Reutilizada de F9 V3.2 (TF-03) en el Bloque A Forex V1.0 (2026-11-02).

#### FXF-0221 · Q 72 (B) — FX Markets (antes FX Week; Infopro Digital)

- **Canal oficial (URL raíz):** https://www.fx-markets.com/ (página índice leída: https://fx-markets.com/organisations/dtcc?page=1 · pieza sobre la clasificación de previsiones: https://www.fx-markets.com/foreign-exchange/2327656/rabobank-wins-with-12-month-dollar-call)
- **Emisor:** Infopro Digital Services Limited (Londres), propietaria también de Risk.net y Central Banking (RF-0203)
- **Documentación y notas:** Publicación profesional dedicada al mercado de divisas: secciones de negociación, infraestructura, tecnología y datos, y regulación; base de datos de algoritmos y «counterparty radar». Archivo largo (piezas desde 2011 sobre repositorios de operaciones de divisas). Publicó la clasificación semanal de previsiones a 12 meses de FX Week (p. ej., Rabobank en cabeza con su previsión EUR/USD de 01/02/2013).
- **Temática:** TFX-07 Prensa y agencias especializadas en divisas (principal) · secundarias: TFX-05, TFX-08
- **Calidad Q:** 72 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 13/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 6/10
- **Tipología:** secundaria especializada (reporterismo sectorial propio)
- **Acceso:** Suscripción individual o corporativa (prueba disponible)
- **Ámbitos:** Estructura del mercado de divisas, plataformas, liquidez, regulación, bancos dealers, clasificaciones de previsiones
- **Motivo de inclusión y uso:** Principal publicación profesional sobre la microestructura y la industria de divisas. Uso: TR-PFV (AG-21) para cambios de liquidez, plataformas y volúmenes; EVAL (AG-20) para contrastar clasificaciones de acierto de previsiones bancarias.
- **Restricciones de uso:** Contenido de pago: solo extractos citables.
- **Sesgos posibles:** Dependencia de la industria (premios, eventos y patrocinio); comparte propietario con Central Banking y Risk.net (no son raíces independientes).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** FX Week pasó a publicarse bajo la marca FX Markets (las URL antiguas de fxweek.com remiten al mismo artículo).
- **Estado:** Aprobada
- **Estado del enlace:** MURO_PAGO
- **Última verificación:** 2026-11-02 (búsqueda web: «DTCC public price dissemination dashboard FX options swap data repository CFTC» y «RaboResearch Jane Foley FX strategy Rabobank currency forecasts»; WebFetch: sí, página índice y artículo)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-07).

#### RF-0029 · Q 72 (B) — Reuters

- **Canal oficial (URL raíz):** reuters.com (según Wikipedia) · Principios de confianza: https://thomsonreuters.com/en/about-us/trust-principles.html
- **Emisor:** Thomson Reuters (distribución profesional vía LSEG)
- **Temática:** TFX-07 Prensa y agencias especializadas en divisas (principal) · secundarias: TFX-01
- **Calidad Q:** 72 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 13/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 6/10
- **Tipología:** primaria
- **Acceso:** Muro parcial
- **Ámbitos:** Noticias de mercados, empresas, macro, materias primas
- **Motivo de inclusión y uso:** Agencia con reporterismo original (fundada en 1851) sujeta a los Trust Principles (integridad, independencia y ausencia de sesgo, desde 1941). Uso en el Bloque A Forex: Reuters publica cobertura continua de divisas (sección de mercados de divisas, columnas de análisis cambiario y sondeos periódicos de previsiones de tipos de cambio). AG-02 y los seis Analistas de segmento como primera fuente de hechos de actualidad cambiaria (intervenciones, declaraciones, movimientos); los hechos se confirman en la fuente oficial.
- **Sesgos y cautelas:** Titulares tempranos corregidos; verificar contra fuente oficial.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «list of news agencies wikipedia» → artículo de Wikipedia «Reuters»; «Reuters markets business news reuters.com Thomson Reuters Trust Principles»; WebFetch: sí, sobre Wikipedia y sobre los Trust Principles)
- **Origen:** Reutilizada de F9 V3.2 (TF-03) en el Bloque A Forex V1.0 (2026-11-02).

#### RF-0255 · Q 70 (B) — Reuters Breakingviews

- **Canal oficial (URL raíz):** https://www.breakingviews.com/ (página leída: https://breakingviews.com/?p=136)
- **Emisor:** Reuters News (Thomson Reuters), marca internacional de comentario financiero
- **Temática:** TFX-07 Prensa y agencias especializadas en divisas (principal) · secundarias: TFX-08
- **Calidad Q:** 70 (B) — Primariedad 10/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 13/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 7/10
- **Tipología:** secundaria (opinión firmada)
- **Acceso:** Suscripción (prueba gratuita); algunas columnas también en Reuters.com
- **Ámbitos:** Comentario en tiempo real sobre operaciones corporativas, valoraciones, mercados y economía; unos 36 columnistas en centros financieros
- **Motivo de inclusión y uso:** Opinión de referencia con cálculos explícitos (valoración, sinergias) sobre noticias corporativas. Uso en el Bloque A Forex: Comentario financiero con cálculos explícitos, incluido el de divisas y bancos centrales. Segunda lectura crítica para CONTRA (AG-11); nunca como prueba de hechos.
- **Sesgos y cautelas:** Comparte raíz con Reuters (RF-0029); no cuenta como fuente independiente de esta.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Reuters Breakingviews financial commentary»; WebFetch: sí)
- **Origen:** Reutilizada de F9 V3.2 (TF-03) en el Bloque A Forex V1.0 (2026-11-02).

#### RF-0030 · Q 69 (B) — Financial Times

- **Canal oficial (URL raíz):** www.ft.com (según Wikipedia)
- **Emisor:** The Financial Times Ltd. (propiedad de Nikkei Inc.)
- **Temática:** TFX-07 Prensa y agencias especializadas en divisas (principal) · secundarias: TFX-08
- **Calidad Q:** 69 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 13/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 4/10
- **Tipología:** primaria y secundaria (opinión)
- **Acceso:** Suscripción (muro de pago medido desde 2007)
- **Ámbitos:** Mercados globales, empresas, política económica; columnas de opinión
- **Motivo de inclusión y uso:** Prensa financiera de referencia con reporterismo propio (fundada en 1888, Londres). Uso en el Bloque A Forex: Cobertura de divisas y columnas de opinión sobre el dólar, el euro y los emergentes. AS-G10N y AS-ESTR para contexto de mercado y opinión firmada (regla F9 a).
- **Sesgos y cautelas:** Muro de pago; separar noticia de columna de opinión.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «list of financial newspapers wikipedia business newspapers» → artículo de Wikipedia «Financial Times»; WebFetch: sí, sobre Wikipedia)
- **Origen:** Reutilizada de F9 V3.2 (TF-03) en el Bloque A Forex V1.0 (2026-11-02).

#### RF-0223 · Q 69 (B) — Dow Jones Newswires

- **Canal oficial (URL raíz):** dowjones.com (sitio oficial de Dow Jones & Company según Wikipedia)
- **Emisor:** Dow Jones & Company (News Corp)
- **Temática:** TFX-07 Prensa y agencias especializadas en divisas (principal) · secundarias: TFX-01
- **Calidad Q:** 69 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 13/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 3/10
- **Tipología:** primaria (agencia de noticias financieras en tiempo real, desde 1882)
- **Acceso:** Suscripción profesional (terminales y Factiva)
- **Ámbitos:** Noticias financieras en tiempo real: empresas, mercados, materias primas, renta fija
- **Motivo de inclusión y uso:** Agencia financiera en tiempo real del grupo editor de The Wall Street Journal, Barron's y MarketWatch. Uso en el Bloque A Forex: Agencia de cables con titulares de mercado en tiempo real (incluidas divisas y bancos centrales). AG-02 y TR-BCM (AG-09) como segunda raíz de agencia frente a Reuters.
- **Sesgos y cautelas:** Acceso restringido; misma raíz que RF-0032 (no cuentan como fuentes independientes entre sí).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «wsj.com markets The Wall Street Journal Dow Jones» → artículo de Wikipedia «Dow Jones & Company»; WebFetch: sí, sobre Wikipedia)
- **Origen:** Reutilizada de F9 V3.2 (TF-03) en el Bloque A Forex V1.0 (2026-11-02).

#### RF-0031 · Q 68 (B) — Bloomberg News

- **Canal oficial (URL raíz):** https://www.bloomberg.com/ (ejemplo de programa Bloomberg Markets: https://www.bloomberg.com/news/videos/2026-03-26/bloomberg-markets-3-26-2026-video)
- **Emisor:** Bloomberg L.P.
- **Temática:** TFX-07 Prensa y agencias especializadas en divisas (principal) · secundarias: TFX-05
- **Calidad Q:** 68 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 13/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 4/10
- **Tipología:** primaria (reporterismo propio) y secundaria (opinión)
- **Acceso:** Muro de pago (artículos); vídeos y resúmenes parcialmente abiertos
- **Ámbitos:** Noticias de mercados, empresas, macro y política económica; programas de vídeo
- **Motivo de inclusión y uso:** Reporterismo financiero de alta velocidad con fuentes propias. Uso en el Bloque A Forex: Cobertura de divisas en tiempo real con datos de mercado propios; sus piezas sobre volatilidad cambiaria y posicionamiento citan con frecuencia índices de terceros. AG-02 y los Analistas de segmento para hechos de mercado; TR-PFV (AG-21) para noticias de volatilidad.
- **Sesgos y cautelas:** Propiedad vinculada al negocio de terminales; distinguir noticia y opinión; muro de pago limita la citación pública.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Bloomberg News markets bloomberg.com/markets»; WebFetch: sí, página de vídeo cargada con resumen; artículo completo no comprobado)
- **Origen:** Reutilizada de F9 V3.2 (TF-03) en el Bloque A Forex V1.0 (2026-11-02).

#### RF-0032 · Q 68 (B) — The Wall Street Journal

- **Canal oficial (URL raíz):** wsj.com (según Wikipedia)
- **Emisor:** Dow Jones & Company (News Corp)
- **Temática:** TFX-07 Prensa y agencias especializadas en divisas (principal) · secundarias: TFX-08
- **Calidad Q:** 68 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 13/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 4/10
- **Tipología:** primaria y secundaria (opinión)
- **Acceso:** Suscripción
- **Ámbitos:** Mercados y empresas de EE. UU.
- **Motivo de inclusión y uso:** Reporterismo original de referencia en EE. UU. (fundado en 1889, Nueva York). Uso en el Bloque A Forex: Cobertura del dólar y de la política de la Fed con perspectiva estadounidense. AS-G10N y TR-BCM (AG-09) para contexto.
- **Sesgos y cautelas:** Muro de pago; página editorial con línea de opinión diferenciada; misma raíz que Dow Jones Newswires (RF-0223).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «list of financial newspapers wikipedia business newspapers» → artículo de Wikipedia «The Wall Street Journal»; WebFetch: sí, sobre Wikipedia)
- **Origen:** Reutilizada de F9 V3.2 (TF-03) en el Bloque A Forex V1.0 (2026-11-02).

#### RF-0254 · Q 68 (B) — Nikkei Asia

- **Canal oficial (URL raíz):** https://asia.nikkei.com/ (presentación del medio: https://info.asia.nikkei.com/about · anuncio de cambio de nombre: https://asia.nikkei.com/announcements/nikkei-to-rename-flagship-english-publication-nikkei-asia)
- **Emisor:** Nikkei Inc. (grupo propietario también de The Nikkei, del índice Nikkei 225 y del Financial Times)
- **Temática:** TFX-07 Prensa y agencias especializadas en divisas (principal) · secundarias: TFX-02
- **Calidad Q:** 68 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 13/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 5/10
- **Tipología:** primaria (reporterismo propio) y secundaria
- **Acceso:** Suscripción (no se ha confirmado el detalle del muro de pago)
- **Ámbitos:** Empresas, economía, política y mercados de Asia; entrevistas; lista Asia300
- **Motivo de inclusión y uso:** Principal medio económico en inglés centrado en Asia, con reporterismo propio en Japón, China y el Sudeste Asiático. Uso en el Bloque A Forex: Cobertura del yen, del yuan y de las divisas asiáticas desde Asia. AS-EMAS (AG-05) y AS-G10N (USD/JPY) para contexto regional.
- **Sesgos y cautelas:** Mismo grupo propietario que el FT (RF-0030): artículos compartidos no son raíces independientes.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Nikkei Asia business news asia.nikkei.com»; WebFetch: sí)
- **Origen:** Reutilizada de F9 V3.2 (TF-03) en el Bloque A Forex V1.0 (2026-11-02).

#### FXF-0222 · Q 67 (B) — MNI Market News International (MNI Policy)

- **Canal oficial (URL raíz):** https://www.mnimarkets.com/products/policy (noticias de bancos centrales: https://marketnews.com/policy/central_bank · emergentes: https://marketnews.com/em-policy)
- **Emisor:** MNI Market News International
- **Documentación y notas:** Servicio de noticias e inteligencia sobre bancos centrales: G10 Policy, Emerging Markets Policy (incluida China, con oficina en Pekín) y ciclo de encuentros «Connect» con responsables de política. Declara que lo usa el 85 % de las entidades vendedoras de primer nivel. Publica calendarios de mercado (FOMC, revisiones de calificación soberana; ver FXF-0268).
- **Temática:** TFX-07 Prensa y agencias especializadas en divisas (principal) · secundarias: TFX-01, TFX-09
- **Calidad Q:** 67 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 13/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 2/10
- **Tipología:** primaria (reporterismo propio con fuentes de bancos centrales)
- **Acceso:** Suscripción profesional (prueba); titulares y algunos artículos abiertos
- **Ámbitos:** Bancos centrales del G10 y emergentes; datos macro; calendarios
- **Motivo de inclusión y uso:** Fuente especializada en «fuentes de bancos centrales» con capacidad de anticipar cambios de tono. Uso: TR-BCM (AG-09) para señales de política monetaria; AS-EMAS, AS-EMLA y AS-EMEA para bancos centrales emergentes. Las informaciones atribuidas a fuentes anónimas no prueban hechos (regla F9 a).
- **Restricciones de uso:** Contenido de pago; citar solo lo publicado.
- **Sesgos posibles:** Informaciones de fuentes no identificadas; la página no detalla la propiedad.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Propiedad no confirmada en la verificación.
- **Estado:** Aprobada
- **Estado del enlace:** MURO_PAGO
- **Última verificación:** 2026-11-02 (búsqueda web: «MNI Market News International central bank policy news service ION Group»; WebFetch: sí, página de producto)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-07).

#### FXF-0223 · Q 66 (B) — Euromoney (cobertura de divisas)

- **Canal oficial (URL raíz):** https://www.euromoney.com/ (pieza: https://www.euromoney.com/article/2dgalxn73hd2ftqqnb8qo/foreign-exchange/fx-volatility-indices-useful-or-not/)
- **Emisor:** Euromoney
- **Documentación y notas:** Revista de banca y mercados con sección de divisas («foreign-exchange») y premios anuales de bancos de divisas (p. ej., «Germany's best FX bank for corporates 2026»). Pieza leída: «FX volatility indices: useful or not?» (Paul Golden, 04/07/2024), con opiniones de State Street, Record Financial, Kantox, Pepperstone y eToro sobre los índices de volatilidad cambiaria.
- **Temática:** TFX-07 Prensa y agencias especializadas en divisas (principal) · secundarias: TFX-06
- **Calidad Q:** 66 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 13/15 · Independencia 7/10 · Actualidad 8/10 · Acceso 6/10
- **Tipología:** secundaria especializada
- **Acceso:** Parcialmente abierto (algunas piezas abiertas; resto con suscripción)
- **Ámbitos:** Industria de divisas, bancos dealers, volatilidad, gestión de divisas corporativa
- **Motivo de inclusión y uso:** Contexto sectorial y opiniones de profesionales del mercado de divisas. Uso: TR-PFV (AG-21) y AS-ESTR (AG-08) para contexto de la industria; nunca como prueba de hechos.
- **Restricciones de uso:** Extractos citables.
- **Sesgos posibles:** Premios y eventos con la propia industria.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios confirmados en la verificación.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «"JPMorgan Global FX Volatility Index" OR "Deutsche Bank Currency Volatility Index" CVIX»; WebFetch: sí, artículo de 04/07/2024)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-07).

#### RF-0034 · Q 66 (B) — Expansión

- **Canal oficial (URL raíz):** expansion.com (según Wikipedia)
- **Emisor:** Unidad Editorial (controlada por RCS MediaGroup)
- **Temática:** TFX-07 Prensa y agencias especializadas en divisas (principal) · secundarias: —
- **Calidad Q:** 66 (B) — Primariedad 13/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 11/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 6/10
- **Tipología:** primaria y secundaria
- **Acceso:** Muro parcial
- **Ámbitos:** Mercados y empresas españolas
- **Motivo de inclusión y uso:** Prensa económica española de referencia (fundada en 1986, Madrid). Uso en el Bloque A Forex: Cobertura en español de mercados, incluidos euro/dólar y divisas latinoamericanas. AS-G10N y AS-EMLA para contexto en español y efecto sobre el inversor español.
- **Sesgos y cautelas:** Muro parcial; cobertura nacional; Wikipedia da datos de propiedad no coincidentes (infobox: Grupo Recoletos; texto: Unidad Editorial/RCS).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «expansion.com mercados diario Expansión Unidad Editorial» → artículo de Wikipedia «Expansión (Spanish newspaper)»; WebFetch: sí, sobre Wikipedia)
- **Origen:** Reutilizada de F9 V3.2 (TF-03) en el Bloque A Forex V1.0 (2026-11-02).

#### RF-0203 · Q 66 (B) — Central Banking (Infopro Digital)

- **Canal oficial (URL raíz):** https://www.centralbanking.com/
- **Emisor:** Infopro Digital Services Limited (Londres)
- **Temática:** TFX-07 Prensa y agencias especializadas en divisas (principal) · secundarias: TFX-01, TFX-02
- **Calidad Q:** 66 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 12/15 · Independencia 8/10 · Actualidad 9/10 · Acceso 5/10
- **Tipología:** secundaria especializada
- **Acceso:** Muro de pago (suscripción individual o corporativa)
- **Ámbitos:** Banca central: política monetaria, estabilidad financiera, divisas, reservas, gobernanza, fintech; encuestas de benchmarking
- **Motivo de inclusión y uso:** Publicación especializada en bancos centrales con archivo largo (artículos desde al menos 2002). Uso en el Bloque A Forex: Publicación especializada en banca central con cobertura de divisas, reservas e intervención. TR-BCM (AG-09) para contexto sobre política cambiaria e intervención de bancos centrales emergentes; AS-EMAS, AS-EMLA y AS-EMEA.
- **Sesgos y cautelas:** Acceso restringido; parte del negocio son premios y eventos con la propia industria.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** MURO_PAGO
- **Última verificación:** 2026-11-02 (búsqueda web: «Bank of England Monetary Policy Report Monetary Policy Committee minutes»; WebFetch: sí)
- **Origen:** Reutilizada de F9 V3.2 (TF-03) en el Bloque A Forex V1.0 (2026-11-02).

#### RF-0033 · Q 64 (C) — The Economist

- **Canal oficial (URL raíz):** www.economist.com (según Wikipedia)
- **Emisor:** The Economist Group (The Economist Newspaper Limited)
- **Temática:** TFX-07 Prensa y agencias especializadas en divisas (principal) · secundarias: TFX-10
- **Calidad Q:** 64 (C) — Primariedad 12/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 13/15 · Independencia 8/10 · Actualidad 8/10 · Acceso 4/10
- **Tipología:** secundaria (análisis y opinión)
- **Acceso:** Suscripción
- **Ámbitos:** Análisis económico y geopolítico semanal
- **Motivo de inclusión y uso:** Síntesis analítica de tendencias globales (desde 1843); útil para narrativas y consenso. Uso en el Bloque A Forex: Semanario de opinión con el índice Big Mac (PPA ilustrativa). AS-ESTR (AG-08) como contraste divulgativo de valoración; nunca como prueba de equilibrio.
- **Sesgos y cautelas:** Línea editorial liberal explícita; artículos sin firma («voz colectiva»).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «list of financial newspapers wikipedia business newspapers» → artículo de Wikipedia «The Economist»; WebFetch: sí, sobre Wikipedia)
- **Origen:** Reutilizada de F9 V3.2 (TF-03) en el Bloque A Forex V1.0 (2026-11-02).

#### FXF-0224 · Q 63 (C) — The Full FX (Colin Lambert)

- **Canal oficial (URL raíz):** https://thefullfx.com/ (pieza leída: https://thefullfx.com/mixed-fx-volumes-at-cme/)
- **Emisor:** Trading and Risk Education Company Pty Ltd (Australia), con la marca The Full FX; editor Colin Lambert
- **Documentación y notas:** Noticias y análisis del mercado de divisas (secciones The Stream, The Position, Top Stories, The Exchange); boletín semanal gratuito, pódcasts y premios. Publica cada mes los volúmenes de las plataformas: p. ej., junio de 2025 (03/07/2025): EBS 64.000 millones de dólares diarios de media, futuros y opciones de divisas de CME 104.000 millones de nocional, CME FX Link 3.650 millones, índice CME G5 CVOL con media de 8,9; también volúmenes de CLS.
- **Temática:** TFX-07 Prensa y agencias especializadas en divisas (principal) · secundarias: TFX-05, TFX-06
- **Calidad Q:** 63 (C) — Primariedad 12/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 11/15 · Independencia 7/10 · Actualidad 9/10 · Acceso 5/10
- **Tipología:** secundaria especializada (con datos de plataformas recopilados)
- **Acceso:** Abierto en parte; boletín gratuito
- **Ámbitos:** Volúmenes de plataformas de divisas, estructura del mercado, CVOL de divisas
- **Motivo de inclusión y uso:** Recopilación mensual de volúmenes de varias plataformas en un solo lugar. Uso: TR-PFV (AG-21) para la tendencia de actividad del mercado; los datos se citan en su fuente primaria (CME, CLS, EBS).
- **Restricciones de uso:** Extractos con atribución.
- **Sesgos posibles:** Publicación pequeña ligada a la industria (eventos y premios).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «CME Group FX options open interest record EUR/USD options on futures weekly options»; WebFetch: sí, artículo de 03/07/2025)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-07).

#### FXF-0225 · Q 62 (C) — FXStreet

- **Canal oficial (URL raíz):** https://www.fxstreet.com/ (piezas leídas: https://www.fxstreet.com/news/eur-sek-forecast-profile-kept-unchanged-danske-bank-202604170832 · https://www.fxstreet.com/news/asian-fx-scope-for-selective-recovery-on-softer-usd-ocbc-202606302327)
- **Emisor:** FXStreet
- **Documentación y notas:** Portal de noticias y análisis de divisas con equipo «FXStreet Insights Team» que resume a diario la investigación de bancos (Danske, OCBC, Scotiabank, Rabobank…) y calendario económico propio. Las piezas declaran haberse creado «con ayuda de una herramienta de inteligencia artificial» y revisadas por un editor; aviso de que las opiniones son de los autores.
- **Temática:** TFX-07 Prensa y agencias especializadas en divisas (principal) · secundarias: TFX-08, TFX-09
- **Calidad Q:** 62 (C) — Primariedad 8/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 9/15 · Independencia 6/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** secundaria (resumen de análisis de terceros)
- **Acceso:** Abierto (con publicidad)
- **Ámbitos:** Noticias de divisas, resúmenes de investigación bancaria, calendario
- **Motivo de inclusión y uso:** Agregador abierto que permite detectar a diario la visión publicada de muchos bancos. Uso: los Analistas de segmento para localizar la visión de bancos; la opinión se atribuye al banco original (TFX-08) y nunca prueba hechos.
- **Restricciones de uso:** Citar al banco de origen; enlazar a la raíz cuando exista.
- **Sesgos posibles:** Textos generados con ayuda de IA; modelo de negocio basado en publicidad de brókeres; fechas no siempre visibles en las piezas.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Uso de herramientas de IA en la redacción (declarado en las piezas).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Danske Bank FX Forecast Update Nordea FX SEB Research currency outlook EUR/SEK EUR/NOK»; WebFetch: sí, dos piezas)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-07).

#### FXF-0226 · Q 61 (C) — investingLive (antes ForexLive; Finance Magnates)

- **Canal oficial (URL raíz):** https://investinglive.com/ (pieza leída: https://investinglive.com/news/!/finance-magnates-acquires-forexlive-to-enter-retail-market-news-00-20170105/ · URL histórica: https://www.forexlive.com/news/!/finance-magnates-acquires-forexlive-to-enter-retail-market-news-00-20170105)
- **Emisor:** Finance Magnates CY Limited (Ultimate Group)
- **Documentación y notas:** Fuente de noticias de divisas en tiempo real («Live Feed») adquirida por Finance Magnates a Live Analytics Inc. (Adam Button) en enero de 2017; el archivo de forexlive.com aparece hoy bajo investinglive.com, con secciones de divisas, acciones, cripto, materias primas, análisis técnico y calendario económico. La página no anuncia expresamente el cambio de nombre.
- **Temática:** TFX-07 Prensa y agencias especializadas en divisas (principal) · secundarias: TFX-09
- **Calidad Q:** 61 (C) — Primariedad 10/20 · Historial 10/20 · Transparencia 8/15 · Autoridad 9/15 · Independencia 5/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** secundaria (flujo de noticias comentado)
- **Acceso:** Abierto
- **Ámbitos:** Titulares de divisas en tiempo real, datos y bancos centrales
- **Motivo de inclusión y uso:** Flujo rápido y abierto de titulares cambiarios con comentario. Uso: AG-02 y los Analistas de segmento como alerta temprana; los hechos se confirman en la fuente oficial o en agencia (RF-0029).
- **Restricciones de uso:** Extractos con atribución.
- **Sesgos posibles:** Propiedad ligada a la industria de brókeres minoristas (directorio de brókeres en el propio sitio).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Compra por Finance Magnates (2017) y migración a la marca investingLive.
- **Estado:** Aprobada
- **Estado del enlace:** REDIRIGIDO
- **Última verificación:** 2026-11-02 (búsqueda web: «ForexLive DailyFX forex news website acquired»; WebFetch: sí, pieza en investinglive.com)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-07).

#### FXF-0227 · Q 60 (C) — Finance Magnates (noticias de la industria de divisas minorista e institucional)

- **Canal oficial (URL raíz):** https://www.financemagnates.com/ (piezas leídas: https://www.financemagnates.com/institutional-forex/cme-groups-fx-futures-and-options-hit-record-single-day-volume/ · https://www.financemagnates.com/forex/ig-group-redirects-daily-fx-website-launches-trade-live-with-ig-morning-show/)
- **Emisor:** Finance Magnates CY Limited (Ultimate Group)
- **Documentación y notas:** Proveedor B2B de noticias, estudios y eventos de negociación multiactivo, con secciones Retail FX e Institutional FX, informes trimestrales de inteligencia y directorio de empresas. Ejemplos: récord de volumen diario de futuros y opciones de divisas de CME (3,15 millones de contratos, 08/03/2023); cierre de DailyFX y redirección a IG (04/09/2024).
- **Temática:** TFX-07 Prensa y agencias especializadas en divisas (principal) · secundarias: TFX-05
- **Calidad Q:** 60 (C) — Primariedad 11/20 · Historial 10/20 · Transparencia 8/15 · Autoridad 9/15 · Independencia 5/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** secundaria especializada
- **Acceso:** Abierto
- **Ámbitos:** Brókeres, plataformas, volúmenes del sector, regulación minorista
- **Motivo de inclusión y uso:** Seguimiento de la industria de divisas minorista (volúmenes de brókeres, cambios regulatorios), útil para el posicionamiento minorista. Uso: TR-PFV (AG-21) y CONTRA (AG-11).
- **Restricciones de uso:** Extractos con atribución.
- **Sesgos posibles:** Negocio de eventos y publicidad con brókeres; mismo propietario que investingLive (FXF-0226): no son raíces independientes.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «CME Group FX options open interest record…» y «ForexLive DailyFX forex news website acquired»; WebFetch: sí, dos piezas)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-07).

#### FXF-0228 · Q 52 (C) — e-Forex (revista trimestral de negociación electrónica de divisas)

- **Canal oficial (URL raíz):** No capturado. Ficha leída: https://fxstreet.com/company/e-forex-magazine (también https://www.cision.one/media-outlets/e-forex-yV4r7paVLAdwNmPx)
- **Emisor:** e-Forex (la ficha leída no nombra al editor)
- **Documentación y notas:** Revista trimestral sobre tecnología de negociación electrónica de divisas (eFX) para la banca y los inversores: plataformas, capacidades y novedades técnicas del sector.
- **Temática:** TFX-07 Prensa y agencias especializadas en divisas (principal) · secundarias: TFX-05
- **Calidad Q:** 52 (C) — Primariedad 8/20 · Historial 10/20 · Transparencia 6/15 · Autoridad 9/15 · Independencia 5/10 · Actualidad 6/10 · Acceso 8/10
- **Tipología:** secundaria especializada
- **Acceso:** No determinado
- **Ámbitos:** Tecnología y plataformas de negociación de divisas
- **Motivo de inclusión y uso:** Contexto de la estructura electrónica del mercado de divisas. Uso: TR-PFV (AG-21), de forma complementaria.
- **Restricciones de uso:** Extractos con atribución.
- **Sesgos posibles:** Publicación muy vinculada a proveedores de tecnología.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Desconocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Profit & Loss magazine foreign exchange profit-loss.com e-Forex magazine FX industry publication»; WebFetch: sí, ficha de FXStreet)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-07).

#### FXF-0229 · Q 50 (C) — Profit & Loss (revista de divisas y derivados)

- **Canal oficial (URL raíz):** No capturado. Ficha leída: https://en.wikipedia.org/wiki/Profit_%26_Loss (también https://fxstreet.com/company/profit---loss)
- **Emisor:** P&L Services Ltd (Londres)
- **Documentación y notas:** Revista mensual fundada en julio de 1999 por Julie Ros sobre los mercados de divisas y derivados (cambios en la industria, nuevos mercados y productos, tecnología); conocida por su «Hall of Fame» y premios de la industria. Wikipedia no indica su estado actual y su fundadora se incorporó a la plataforma 24 Exchange (Finance Magnates).
- **Temática:** TFX-07 Prensa y agencias especializadas en divisas (principal) · secundarias: —
- **Calidad Q:** 50 (C) — Primariedad 9/20 · Historial 10/20 · Transparencia 6/15 · Autoridad 10/15 · Independencia 6/10 · Actualidad 2/10 · Acceso 7/10
- **Tipología:** secundaria especializada
- **Acceso:** No determinado
- **Ámbitos:** Industria de divisas y derivados; archivo histórico
- **Motivo de inclusión y uso:** Archivo histórico de la industria de divisas (1999 en adelante). Uso: DOC-A (AG-14) y TR-PFV (AG-21) para contexto histórico; no para actualidad.
- **Restricciones de uso:** Extractos con atribución.
- **Sesgos posibles:** Vigencia no confirmada; premios con la propia industria.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Salida de la fundadora; actividad actual no confirmada (candidata a baja si HT-02 no localiza un canal vivo).
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Profit & Loss magazine foreign exchange profit-loss.com e-Forex magazine FX industry publication»; WebFetch: sí, Wikipedia)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-07).

## TFX-08 Análisis de divisas de bancos, gestoras y casas de análisis

#### RF-0238 · Q 74 (B) — Capital Economics

- **Canal oficial (URL raíz):** https://www.capitaleconomics.com/ (la empresa: https://capitaleconomics.com/about-us/the-company/)
- **Emisor:** Capital Economics (Londres, fundada en 1999)
- **Temática:** TFX-08 Análisis de divisas de bancos, gestoras y casas de análisis (principal) · secundarias: —
- **Calidad Q:** 74 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 13/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 7/10
- **Tipología:** secundaria cualificada (casa de análisis independiente)
- **Acceso:** Suscripción; algunos contenidos públicos
- **Ámbitos:** Macro y mercados de más de 100 economías, con más de 60 economistas; previsiones y modelos propios
- **Motivo de inclusión y uso:** Casa independiente sin banca de inversión, intermediación ni cartera propia. Uso en el Bloque A Forex: Casa de análisis independiente con previsiones de divisas de G10 y emergentes. Los Analistas de segmento y PROS (AG-10) como previsión externa no bancaria.
- **Sesgos y cautelas:** Acceso mayoritariamente de pago.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Capital Economics independent macroeconomic research consultancy»; WebFetch: sí)
- **Origen:** Reutilizada de F9 V3.2 (TF-05) en el Bloque A Forex V1.0 (2026-11-02).

#### FXF-0241 · Q 72 (B) — Scotiabank — Global Foreign Exchange (G10 FX Daily, previsiones y posicionamiento CFTC)

- **Canal oficial (URL raíz):** https://gbm.scotiabank.com/en/market-insights/global-foreign-exchange.html (ejemplo de análisis: https://www.gbm.scotiabank.com/en/market-insights/article.research-and-market-commentary.year-end-expectations-for-the-usd.html)
- **Emisor:** Scotiabank Global Banking and Markets (Toronto)
- **Documentación y notas:** Ocho productos con enlace a PDF en scotiaequityresearch.com: G10 FX Daily, CAD Weekly, CAD Technical Overview, Forecast Summary, Monthly Outlook, Weekly Flows and CFTC Positioning, FX Snapshot y G10 Technical Overview. Equipo: Shaun Osborne (director gerente y estratega jefe de divisas) y Eric Theoret; el equipo declara cubrir también Latinoamérica.
- **Temática:** TFX-08 Análisis de divisas de bancos, gestoras y casas de análisis (principal) · secundarias: TFX-05
- **Calidad Q:** 72 (B) — Primariedad 13/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 12/15 · Independencia 6/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** secundaria cualificada (análisis de banco)
- **Acceso:** Abierto (enlaces a PDF sin registro visible)
- **Ámbitos:** G10, CAD, previsiones, flujos y posicionamiento CFTC, análisis técnico
- **Motivo de inclusión y uso:** Uno de los pocos bancos que publican en abierto un informe semanal de flujos y posicionamiento CFTC y un resumen de previsiones. Uso: AS-G10M (AG-04: CAD) y AS-G10N; TR-PFV (AG-21) para el informe de posicionamiento; EVAL (AG-20) para medir el acierto del Forecast Summary.
- **Restricciones de uso:** Uso informativo; citar banco, fecha y autor.
- **Sesgos posibles:** Banco dealer con negocio de divisas (conflicto de interés).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Scotiabank Daily FX Update Shaun Osborne chief FX strategist»; WebFetch: sí, página Global Foreign Exchange)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-08).

#### RF-0042 · Q 72 (B) — BlackRock Investment Institute

- **Canal oficial (URL raíz):** https://www.blackrock.com/corporate/insights/blackrock-investment-institute
- **Emisor:** BlackRock
- **Temática:** TFX-08 Análisis de divisas de bancos, gestoras y casas de análisis (principal) · secundarias: TFX-10
- **Calidad Q:** 72 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 13/15 · Independencia 5/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** secundaria cualificada (visión de gestora)
- **Acceso:** Abierto
- **Ámbitos:** Weekly Market Commentary, Global Investment Outlook trimestral (Q4 2026: 15/09/2026), Geopolitical Risk Dashboard, Capital Market Assumptions
- **Motivo de inclusión y uso:** Visión del mayor gestor del mundo; señal de consenso institucional. El panel de riesgo geopolítico es útil para escenarios. Uso en el Bloque A Forex: Perspectivas de la gestora con visión táctica sobre el dólar y las divisas emergentes. AS-ESTR (AG-08) y PROS (AG-10) como visión de un gran inversor (no prueba de hechos).
- **Sesgos y cautelas:** Comercializa productos ligados a sus tesis.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «BlackRock Investment Institute weekly commentary»; WebFetch: sí)
- **Origen:** Reutilizada de F9 V3.2 (TF-04) en el Bloque A Forex V1.0 (2026-11-02).

#### RF-0205 · Q 72 (B) — CaixaBank Research

- **Canal oficial (URL raíz):** https://www.caixabankresearch.com/ (ejemplo, Financial Markets Daily Report: https://www.caixabankresearch.com/en/publications/financial-markets-daily-report/04-may-2020)
- **Emisor:** CaixaBank (servicio de estudios)
- **Temática:** TFX-08 Análisis de divisas de bancos, gestoras y casas de análisis (principal) · secundarias: —
- **Calidad Q:** 72 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 12/15 · Independencia 6/10 · Actualidad 10/10 · Acceso 10/10 (corregida en la reutilización: el desglose de V3.2 sumaba 72, no 74)
- **Tipología:** secundaria cualificada (análisis de banco)
- **Acceso:** Abierto (ES, CA, EN; PDF descargables)
- **Ámbitos:** Economía española y portuguesa, mercados financieros, sectores, comunidades autónomas, consumo (Monitor de consumo), divisas; Informe Mensual, Pulso Económico Semanal, informe diario de mercados, documentos de trabajo
- **Motivo de inclusión y uso:** Servicio de estudios bancario español de acceso libre con publicaciones de alta frecuencia y datos propios de consumo. Uso en el Bloque A Forex: Informe diario de mercados financieros y notas con previsiones de divisas (euro, dólar). AS-G10N para la visión española del EUR; EVAL (AG-20) para registrar previsiones.
- **Sesgos y cautelas:** Visión de un banco comercial (conflicto de interés potencial en vivienda, crédito y renta variable española); aviso legal en la web de CaixaBank.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Cinco Días cincodias.elpais.com mercados financieros»; WebFetch: sí)

<!-- ===== Tanda 2 (2026-11-02): 22 búsquedas WebSearch. Las fichas siguientes se fusionan en su temática y por Q descendente. ===== -->
<!-- Vía «directorio FCA»: URL tomada de la página oficial de la FCA «Regulators in the EU and European Economic Area (EEA)» (https://www.fca.org.uk/firms/regulators-eu-eea, devuelta por búsqueda y leída con WebFetch); la propia FCA advierte que algunos enlaces pueden estar desactualizados. Vía «Wikipedia»: URL oficial leída en la ficha (infobox) del artículo de Wikipedia alcanzado desde una búsqueda. -->
- **Origen:** Reutilizada de F9 V3.2 (TF-05) en el Bloque A Forex V1.0 (2026-11-02).

#### RF-0229 · Q 72 (B) — BBVA Research

- **Canal oficial (URL raíz):** https://www.bbvaresearch.com/ (quiénes somos: https://www.bbvaresearch.com/en/about-us/)
- **Emisor:** BBVA (servicio de estudios fundado en 1932; economista jefe: Jorge Sicilia)
- **Temática:** TFX-08 Análisis de divisas de bancos, gestoras y casas de análisis (principal) · secundarias: TFX-02
- **Calidad Q:** 72 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 12/15 · Independencia 6/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** secundaria cualificada (análisis de banco)
- **Acceso:** Abierto (publicaciones descargables; no hay declaración expresa de licencia)
- **Ámbitos:** Macro, sistemas financieros, economía digital y geoestrategia; previsiones para más de 10 países (España, México, Turquía, Colombia, Argentina, Perú, China); indicadores de big data
- **Motivo de inclusión y uso:** Servicio de estudios con más de 100 analistas, previsiones publicadas e indicadores de alta frecuencia. Uso en el Bloque A Forex: Análisis macro de España, México, América del Sur y Turquía, con previsiones de tipo de cambio en sus informes de situación por país. AS-EMLA (AG-06: MXN, COP, PEN, ARS) y AS-EMEA (AG-07: TRY).
- **Sesgos y cautelas:** Visión de un banco comercial con intereses en los países que cubre.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ING THINK economic research BBVA Research Allianz Research publications»; WebFetch: sí)
- **Origen:** Reutilizada de F9 V3.2 (TF-05) en el Bloque A Forex V1.0 (2026-11-02).

#### RF-0232 · Q 72 (B) — ING THINK

- **Canal oficial (URL raíz):** https://think.ing.com/ (quiénes somos: https://think.ing.com/about/)
- **Emisor:** ING (más de 40 economistas)
- **Temática:** TFX-08 Análisis de divisas de bancos, gestoras y casas de análisis (principal) · secundarias: TFX-07
- **Calidad Q:** 72 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 12/15 · Independencia 6/10 · Actualidad 10/10 · Acceso 10/10 (corregida en la reutilización: el desglose de V3.2 sumaba 72, no 74)
- **Tipología:** secundaria cualificada (análisis de banco)
- **Acceso:** Abierto
- **Ámbitos:** Macro, bancos centrales, divisas (tabla mensual de previsiones FX Talking), materias primas, sectores; ING Monthly
- **Motivo de inclusión y uso:** Análisis bancario europeo abierto, con tablas de previsiones publicadas. Uso en el Bloque A Forex: ING THINK publica a diario análisis de divisas y la tabla mensual de previsiones FX Talking. Los seis Analistas de segmento y PROS (AG-10) como previsión bancaria publicada; EVAL (AG-20) para medir su acierto frente al paseo aleatorio y al forward.
- **Sesgos y cautelas:** Visión de un banco; la investigación profesional regulada está en otro portal.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ING THINK economic and financial analysis think.ing.com»; WebFetch: sí)
- **Origen:** Reutilizada de F9 V3.2 (TF-05) en el Bloque A Forex V1.0 (2026-11-02).

#### RF-0233 · Q 72 (B) — BNP Paribas Economic Research

- **Canal oficial (URL raíz):** https://economic-research.bnpparibas.com/ (equipos: https://economic-research.bnpparibas.com/Teams/en-US · Eco Flash: https://economic-research.bnpparibas.com/Publications/Eco-Flash/en-US)
- **Emisor:** BNP Paribas, departamento de estudios económicos (París; economista jefa del grupo: Isabelle Mateos y Lago)
- **Temática:** TFX-08 Análisis de divisas de bancos, gestoras y casas de análisis (principal) · secundarias: —
- **Calidad Q:** 72 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 12/15 · Independencia 6/10 · Actualidad 10/10 · Acceso 10/10 (corregida en la reutilización: el desglose de V3.2 sumaba 72, no 73)
- **Tipología:** secundaria cualificada (análisis de banco)
- **Acceso:** Abierto (EN/FR, RSS y suscripción)
- **Ámbitos:** Economías de la OCDE, emergentes y riesgo país, economía bancaria; Eco Flash, Eco Conjoncture, Eco Week, Eco Emerging, escenarios y previsiones
- **Motivo de inclusión y uso:** Estudios de un gran banco de la zona euro con equipo de riesgo país. Uso en el Bloque A Forex: Análisis económico por país, útil para fundamentos de divisas europeas y emergentes. AS-EMEA y AS-G10N para fundamentos.
- **Sesgos y cautelas:** Visión de un banco comercial.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «BNP Paribas Economic Research economic-research.bnpparibas.com EcoFlash»; WebFetch: sí)
- **Origen:** Reutilizada de F9 V3.2 (TF-05) en el Bloque A Forex V1.0 (2026-11-02).

#### FXF-0242 · Q 71 (B) — MUFG Research — Global Markets Research (divisas)

- **Canal oficial (URL raíz):** https://mufgresearch.com/meet-the-team (FX Daily Snapshot, p. ej.: https://www.mufgresearch.com/fx/fx-daily-snapshot-20-february-2023 · pódcast semanal: https://mufgresearch.com/digital-content/the-global-markets-fx-week-ahead-podcast-8-march-2024 · investigación de MUFG Bank: https://www.bk.mufg.jp/global/productsandservices/gm_research.html)
- **Emisor:** MUFG (Mitsubishi UFJ Financial Group), Global Markets Research (Londres, Singapur y Tokio)
- **Documentación y notas:** Equipo de divisas: Derek Halpenny (jefe de análisis, G4 y EMEA), Lee Hardman (G10 y EMEA), Abdul-Ahad Lockhart (G10 y cuantitativo), Lin Li, Lloyd Chan y Khang Sek Lee (Asia), Teppei Ino (yen) y Sumino Kamei (EMEA). Productos: FX Daily Snapshot, FX Weekly, previsiones y el pódcast «The Global Markets FX Week Ahead». Material dirigido a inversores profesionales; el sitio advierte que no es «investment research».
- **Temática:** TFX-08 Análisis de divisas de bancos, gestoras y casas de análisis (principal) · secundarias: —
- **Calidad Q:** 71 (B) — Primariedad 13/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 13/15 · Independencia 6/10 · Actualidad 10/10 · Acceso 8/10
- **Tipología:** secundaria cualificada (análisis de banco)
- **Acceso:** Abierto con aviso de inversor profesional; área de clientes con registro
- **Ámbitos:** G10, yen, Asia y EMEA; previsiones de divisas
- **Motivo de inclusión y uso:** Visión de un gran banco japonés, especialmente valiosa para el yen y la intervención japonesa. Uso: AS-G10N (USD/JPY, EUR/JPY), AS-EMAS (AG-05) y AS-EMEA (AG-07); EVAL (AG-20) para previsiones.
- **Restricciones de uso:** Solo para inversores profesionales según el aviso; citar fecha y autor.
- **Sesgos posibles:** Banco dealer; posible sesgo de perspectiva japonesa.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «MUFG Research FX Daily Snapshot Lee Hardman Derek Halpenny»; WebFetch: sí, página del equipo)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-08).

#### RF-0249 · Q 71 (B) — Amundi Investment Institute — Research Center

- **Canal oficial (URL raíz):** https://research-center.amundi.com/ (Global Investment Views: https://research-center.amundi.com/publications/global-investment-views)
- **Emisor:** Amundi (Amundi Investment Institute)
- **Temática:** TFX-08 Análisis de divisas de bancos, gestoras y casas de análisis (principal) · secundarias: —
- **Calidad Q:** 71 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 13/15 · Independencia 5/10 · Actualidad 10/10 · Acceso 8/10
- **Tipología:** secundaria cualificada (visión de gestora)
- **Acceso:** Abierto con aceptación de condiciones (dirigido a profesionales no estadounidenses)
- **Ámbitos:** Global Investment Views mensual (última: octubre de 2026), convicciones de los CIO, estrategia de mercados e investigación académica
- **Motivo de inclusión y uso:** Visión de la mayor gestora europea. Uso en el Bloque A Forex: Perspectivas de la mayor gestora europea, con previsiones de divisas en sus escenarios. AS-G10N y AS-ESTR como visión de gestora europea.
- **Sesgos y cautelas:** Gestora con productos; audiencia profesional.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Amundi Investment Institute outlook research»; WebFetch: sí)
- **Origen:** Reutilizada de F9 V3.2 (TF-04) en el Bloque A Forex V1.0 (2026-11-02).

#### FXF-0243 · Q 70 (B) — Danske Bank Research — FX Forecast Update (divisas escandinavas y G10)

- **Canal oficial (URL raíz):** https://research.danskebank.com/ (ejemplo de informe: https://research.danskebank.com/abo/FXForecastUpdate240919/%24file/FX_Forecast%20Update_240919.pdf)
- **Emisor:** Danske Bank A/S (Copenhague)
- **Documentación y notas:** Publicación periódica «FX Forecast Update» con previsiones a 1, 3, 6 y 12 meses de EUR/USD, EUR/SEK, EUR/NOK, EUR/DKK y otros cruces (serie de informes en PDF desde al menos 2014). En 2026 sus previsiones se siguen difundiendo (p. ej., EUR/SEK a 11,00 a 6–12 meses, según FXStreet, FXF-0225).
- **Temática:** TFX-08 Análisis de divisas de bancos, gestoras y casas de análisis (principal) · secundarias: —
- **Calidad Q:** 70 (B) — Primariedad 13/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 12/15 · Independencia 6/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** secundaria cualificada (análisis de banco)
- **Acceso:** Abierto (PDF)
- **Ámbitos:** SEK, NOK, DKK, EUR/USD y G10; previsiones con horizonte explícito
- **Motivo de inclusión y uso:** Referencia de análisis para las divisas escandinavas, con previsiones cuantificadas por horizonte. Uso: AS-G10M (AG-04: NOK, SEK); EVAL (AG-20) para medir acierto frente al paseo aleatorio y al forward.
- **Restricciones de uso:** Uso informativo; citar fecha del informe.
- **Sesgos posibles:** Banco dealer nórdico con negocio en esas divisas.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Danske Bank FX Forecast Update Nordea FX SEB Research currency outlook EUR/SEK EUR/NOK»; WebFetch: sí, sobre la pieza de FXStreet que resume su previsión; los PDF de Danske no se leyeron)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-08).

#### FXF-0244 · Q 69 (B) — Commerzbank Research — análisis de divisas (Daily Currency Briefing, FX Hotspot)

- **Canal oficial (URL raíz):** https://www.commerzbank.de/group/research/chief-economist/ (relación de publicaciones, noviembre de 2021: https://www.commerzbank.ae/portal/media/corporatebanking/contentrefresh/research/research-publications/200611_Research_EN_Publication_overview.pdf)
- **Emisor:** Commerzbank AG, Research (Fráncfort)
- **Documentación y notas:** Publicaciones de divisas: Daily Currency Briefing (comentario matinal diario de G10 y emergentes), Strategic Currency Briefing (perspectiva a medio plazo actualizada mensualmente) y FX Hotspot (análisis breves ocasionales). La relación de publicaciones leída es de 2021: confirmar la oferta vigente.
- **Temática:** TFX-08 Análisis de divisas de bancos, gestoras y casas de análisis (principal) · secundarias: —
- **Calidad Q:** 69 (B) — Primariedad 13/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 13/15 · Independencia 6/10 · Actualidad 7/10 · Acceso 9/10
- **Tipología:** secundaria cualificada (análisis de banco)
- **Acceso:** Abierto en parte (comentarios difundidos por agregadores); informes completos para clientes
- **Ámbitos:** EUR, G10 y emergentes (incluida Europa central y del este)
- **Motivo de inclusión y uso:** Análisis de divisas de un gran banco alemán con cobertura de emergentes europeos. Uso: AS-G10N (EUR) y AS-EMEA (AG-07: PLN, HUF, CZK).
- **Restricciones de uso:** Citar fecha y publicación.
- **Sesgos posibles:** Banco dealer; documentación de producto de 2021.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Posibles cambios de catálogo desde 2021.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Commerzbank Research FX Ulrich Leuchtmann Antje Praefcke currency research»; WebFetch: sí, relación de publicaciones)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-08).

#### FXF-0245 · Q 69 (B) — OCBC — Global Markets Research (divisas asiáticas)

- **Canal oficial (URL raíz):** https://www.ocbc.com/assets/pdf/FX%20Outlook/Viewpoint/2020/Asia%20FX%20Update%2023APR20.pdf (archivo de perspectivas diarias: https://www.ocbc.com/assets/pdf/FX%20Outlook/DFO/2016/DFO05012016.pdf · resumen reciente: https://www.fxstreet.com/news/asian-fx-scope-for-selective-recovery-on-softer-usd-ocbc-202606302327)
- **Emisor:** Oversea-Chinese Banking Corporation (Singapur)
- **Documentación y notas:** Archivo de perspectivas de divisas en PDF (Daily FX Outlook desde al menos 2016; Asia FX Update). Visión de 2026 (Christopher Wong): recuperación selectiva de las divisas asiáticas si se frena el dólar; la rupia indonesia destacada por el alivio del petróleo y el apoyo de Bank Indonesia.
- **Temática:** TFX-08 Análisis de divisas de bancos, gestoras y casas de análisis (principal) · secundarias: TFX-02
- **Calidad Q:** 69 (B) — Primariedad 13/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 12/15 · Independencia 6/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** secundaria cualificada (análisis de banco)
- **Acceso:** Abierto (PDF)
- **Ámbitos:** SGD, CNH, IDR, MYR, THB, KRW, TWD y resto de Asia
- **Motivo de inclusión y uso:** Análisis regional desde Asia, con conocimiento de bancos centrales asiáticos. Uso: AS-EMAS (AG-05); EVAL (AG-20) para previsiones.
- **Restricciones de uso:** Citar fecha y autor.
- **Sesgos posibles:** Banco regional con negocio en esas divisas.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «OCBC Global Markets Research FX outlook Asian currencies UOB Global Economics Markets Research FX»; WebFetch: sí, sobre la pieza de FXStreet; los PDF de OCBC no se leyeron)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-08).

#### RF-0230 · Q 69 (B) — Allianz Research

- **Canal oficial (URL raíz):** https://www.allianz.com/en/economic_research/ (publicaciones: https://www.allianz.com/en/economic_research/publications/insights.html)
- **Emisor:** Allianz SE (servicio de estudios económicos)
- **Temática:** TFX-08 Análisis de divisas de bancos, gestoras y casas de análisis (principal) · secundarias: TFX-09
- **Calidad Q:** 69 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 12/15 · Independencia 6/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** secundaria cualificada
- **Acceso:** Abierto (sin declaración expresa de licencia)
- **Ámbitos:** Riesgo país y sectorial, Global Wealth Report (2026), Global Insurance Map, investigación de clima y transición, gráficos y podcast
- **Motivo de inclusión y uso:** Estudios de un gran asegurador europeo, con datos propios de riesgo país y riqueza financiera de los hogares. Uso en el Bloque A Forex: Análisis de riesgo país y de comercio (Allianz Trade), útil para el riesgo soberano de divisas emergentes. AS-EMLA, AS-EMEA y AS-EMAS.
- **Sesgos y cautelas:** Visión de un grupo asegurador con negocio de gestión de activos; el listado de publicaciones no se mostró completo al leerlo.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ING THINK economic research BBVA Research Allianz Research publications»; WebFetch: sí)
- **Origen:** Reutilizada de F9 V3.2 (TF-05) en el Bloque A Forex V1.0 (2026-11-02).

#### RF-0239 · Q 69 (B) — Oxford Economics

- **Canal oficial (URL raíz):** https://www.oxfordeconomics.com/ (Global Macro Service: https://www.oxfordeconomics.com/subscriptions/global-macro-service/)
- **Emisor:** Oxford Economics (grupo que incluye Tourism Economics, Alpine Macro y FrontierView)
- **Temática:** TFX-08 Análisis de divisas de bancos, gestoras y casas de análisis (principal) · secundarias: —
- **Calidad Q:** 69 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 13/15 · Independencia 8/10 · Actualidad 9/10 · Acceso 6/10
- **Tipología:** secundaria cualificada (consultora de previsión)
- **Acceso:** Suscripción; notas de investigación y blogs públicos
- **Ámbitos:** Previsiones nacionales, sectoriales y urbanas de más de 200 economías; Global Economic Model y Global Industry Model
- **Motivo de inclusión y uso:** Modelo macro global usado por empresas y gobiernos. Uso en el Bloque A Forex: Previsiones macroeconómicas globales con modelo propio, incluidas las de tipos de cambio. PROS (AG-10) como escenario macro externo.
- **Sesgos y cautelas:** Acceso mayoritariamente de pago; consultora con encargos de clientes.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Oxford Economics global economic forecasts research»; WebFetch: sí)
- **Origen:** Reutilizada de F9 V3.2 (TF-05) en el Bloque A Forex V1.0 (2026-11-02).

#### FXF-0246 · Q 68 (B) — Rabobank — RaboResearch (estrategia de divisas, Jane Foley)

- **Canal oficial (URL raíz):** No capturado (sitio de RaboResearch). Piezas: clasificación de FX Week: https://www.fx-markets.com/foreign-exchange/2327656/rabobank-wins-with-12-month-dollar-call · resumen de 2026: https://www.tmgm.com/en/analysis/market-news/article/euro-choppy-range-outlook-against-us-dollar-rabobank-202607061003
- **Emisor:** Rabobank (Países Bajos), RaboResearch Global Economics & Markets
- **Documentación y notas:** Jane Foley, estratega sénior de divisas, encabezó la clasificación semanal de previsiones a 12 meses de FX Week con su previsión EUR/USD de 1,40 (01/02/2013). En 2026 sus notas sobre el euro y el yen (intervención y señales del BoJ) se difunden en agregadores.
- **Temática:** TFX-08 Análisis de divisas de bancos, gestoras y casas de análisis (principal) · secundarias: —
- **Calidad Q:** 68 (B) — Primariedad 13/20 · Historial 11/20 · Transparencia 10/15 · Autoridad 12/15 · Independencia 7/10 · Actualidad 9/10 · Acceso 6/10
- **Tipología:** secundaria cualificada (análisis de banco)
- **Acceso:** Parcial (notas abiertas en su sitio y difusión en agregadores)
- **Ámbitos:** EUR, USD, JPY, GBP y G10
- **Motivo de inclusión y uso:** Banco cooperativo con menor negocio de mercados que los grandes dealers y con un acierto documentado en una clasificación pública. Uso: AS-G10N; EVAL (AG-20) para comparar con su historial publicado.
- **Restricciones de uso:** Citar la nota original de Rabobank cuando se localice; los agregadores son copias.
- **Sesgos posibles:** Copias en agregadores de brókeres (no son fuente independiente).
- **Historial de exactitud:** Clasificación externa favorable (FX Week, 2013); pendiente de medición por el Evaluador (puntuación 11/20).
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «RaboResearch Jane Foley FX strategy Rabobank currency forecasts»; WebFetch: sí, artículo de FX Markets)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-08).

#### RF-0046 · Q 66 (B) — Goldman Sachs Global Investment Research

- **Canal oficial (URL raíz):** https://www.goldmansachs.com/insights/goldman-sachs-research (Top of Mind e informes: https://www.goldmansachs.com/insights/reports)
- **Emisor:** Goldman Sachs
- **Temática:** TFX-08 Análisis de divisas de bancos, gestoras y casas de análisis (principal) · secundarias: —
- **Calidad Q:** 66 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 14/15 · Independencia 5/10 · Actualidad 9/10 · Acceso 3/10
- **Tipología:** secundaria cualificada
- **Acceso:** Restringido (clientes, Marquee); resúmenes públicos (Top of Mind, artículos, boletín semanal Briefings)
- **Ámbitos:** Previsiones macro, estrategia, sectores
- **Motivo de inclusión y uso:** Análisis de banco de inversión influyente; usar solo resúmenes públicos citables. Uso en el Bloque A Forex: Análisis público (Top of Mind, informes) con piezas recurrentes sobre el dólar y las divisas. AS-ESTR y AS-G10N como opinión de un gran banco; solo extractos públicos.
- **Sesgos y cautelas:** Conflictos de interés de banca de inversión; acceso restringido; el portal no señala qué contenidos son solo para clientes.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Goldman Sachs Global Investment Research insights Top of Mind»; WebFetch: sí)
- **Origen:** Reutilizada de F9 V3.2 (TF-05) en el Bloque A Forex V1.0 (2026-11-02).

#### RF-0240 · Q 66 (B) — Morgan Stanley — Ideas y pódcast «Thoughts on the Market»

- **Canal oficial (URL raíz):** https://www.morganstanley.com/ideas (pódcasts: https://www.morganstanley.com/ideas/morgan-stanley-podcast-homepage)
- **Emisor:** Morgan Stanley
- **Temática:** TFX-08 Análisis de divisas de bancos, gestoras y casas de análisis (principal) · secundarias: —
- **Calidad Q:** 66 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 14/15 · Independencia 5/10 · Actualidad 10/10 · Acceso 5/10
- **Tipología:** secundaria cualificada
- **Acceso:** Pódcast diario abierto; investigación completa restringida a clientes
- **Ámbitos:** Estrategia de mercados, macro, sectores (pódcast diario con analistas del banco)
- **Motivo de inclusión y uso:** Resumen público diario de la visión de estrategas y analistas de un gran banco de inversión. Uso en el Bloque A Forex: Pódcast y artículos públicos con visiones de divisas del equipo de estrategia. AS-G10N y AS-ESTR como opinión pública citable.
- **Sesgos y cautelas:** Conflictos de interés de banca de inversión; contenido público resumido.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Morgan Stanley Research ideas Thoughts on the Market»; WebFetch: sí)
- **Origen:** Reutilizada de F9 V3.2 (TF-05) en el Bloque A Forex V1.0 (2026-11-02).

#### RF-0243 · Q 65 (B) — Citi GPS (Global Perspectives & Solutions)

- **Canal oficial (URL raíz):** https://www.citigroup.com/global/insights/tags/citi-global-perspectives-solutions
- **Emisor:** Citigroup
- **Temática:** TFX-08 Análisis de divisas de bancos, gestoras y casas de análisis (principal) · secundarias: TFX-10
- **Calidad Q:** 65 (B) — Primariedad 11/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 13/15 · Independencia 5/10 · Actualidad 8/10 · Acceso 8/10
- **Tipología:** secundaria cualificada (informes temáticos)
- **Acceso:** Abierto (suscripción por correo)
- **Ámbitos:** Tendencias globales: mercados y economía, tecnología, sostenibilidad, estrategia empresarial; colaboración con la Oxford Martin School
- **Motivo de inclusión y uso:** Informes temáticos de largo plazo de un banco global. Uso en el Bloque A Forex: Informes temáticos de largo plazo (p. ej., sistema monetario internacional). AS-ESTR (AG-08) y PROS (AG-10) para temas estructurales del dólar.
- **Sesgos y cautelas:** Visión de un banco con intereses comerciales; la página de etiqueta no listó informes concretos.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Citi GPS Global Perspectives and Solutions reports»; WebFetch: sí)
- **Origen:** Reutilizada de F9 V3.2 (TF-05) en el Bloque A Forex V1.0 (2026-11-02).

#### FXF-0247 · Q 64 (C) — UOB — Global Economics and Markets Research (divisas asiáticas)

- **Canal oficial (URL raíz):** No capturado. Pieza: The Edge Malaysia (07/01/2026): https://theedgemalaysia.com/node/788398
- **Emisor:** United Overseas Bank (Singapur), Global Economics and Markets Research
- **Documentación y notas:** Según The Edge Malaysia, el estratega de divisas Peter Chia preveía en enero de 2026 un ringgit en torno a 4,00, apreciación de las divisas asiáticas en 2026 por menores diferenciales de tipos y una caída adicional del dólar de alrededor del 3 %.
- **Temática:** TFX-08 Análisis de divisas de bancos, gestoras y casas de análisis (principal) · secundarias: TFX-02
- **Calidad Q:** 64 (C) — Primariedad 11/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 12/15 · Independencia 6/10 · Actualidad 9/10 · Acceso 7/10
- **Tipología:** secundaria cualificada (análisis de banco)
- **Acceso:** Parcial (seminarios y difusión en prensa)
- **Ámbitos:** MYR, SGD y divisas de la ASEAN
- **Motivo de inclusión y uso:** Segunda visión bancaria desde Singapur para contrastar a OCBC (FXF-0245). Uso: AS-EMAS (AG-05).
- **Restricciones de uso:** Citar la fuente original cuando se localice.
- **Sesgos posibles:** Banco regional con negocio en esas divisas; verificado solo a través de prensa.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «OCBC Global Markets Research FX outlook Asian currencies UOB Global Economics Markets Research FX»; WebFetch: sí, artículo de The Edge Malaysia)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-08).

#### RF-0236 · Q 62 (C) — Deutsche Bank Research (portal profesional)

- **Canal oficial (URL raíz):** https://research.db.com/ (ejemplo: https://research.db.com/Research/Disclosures/FICCDisclosures)
- **Emisor:** Deutsche Bank AG (Fráncfort)
- **Temática:** TFX-08 Análisis de divisas de bancos, gestoras y casas de análisis (principal) · secundarias: —
- **Calidad Q:** 62 (C) — Primariedad 12/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 13/15 · Independencia 5/10 · Actualidad 8/10 · Acceso 3/10
- **Tipología:** secundaria cualificada (análisis de banco de inversión)
- **Acceso:** Restringido (clientes); divulgaciones regulatorias públicas
- **Ámbitos:** Renta fija, divisas, materias primas, crédito, estrategia; históricos de recomendaciones (divulgaciones de octubre de 2026)
- **Motivo de inclusión y uso:** Análisis de un gran banco europeo; las divulgaciones públicas permiten auditar recomendaciones históricas. Uso en el Bloque A Forex: Portal profesional con análisis de divisas (FX) entre sus clases de activo; las divulgaciones públicas permiten auditar recomendaciones históricas. Solo extractos públicos; EVAL (AG-20) para recomendaciones auditables.
- **Sesgos y cautelas:** Conflictos de interés de banca de inversión; casi todo el contenido es de acceso restringido.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Deutsche Bank Research dbresearch.com publications»; WebFetch: sí)
- **Origen:** Reutilizada de F9 V3.2 (TF-05) en el Bloque A Forex V1.0 (2026-11-02).

#### FXF-0248 · Q 58 (C) — Pound Sterling Live (previsiones de tipos de cambio de bancos)

- **Canal oficial (URL raíz):** https://poundsterlinglive.com/ (sección de previsiones, pieza leída: https://poundsterlinglive.com/exchange-rate-forecasts-1/7010-danske-bank-mid-2017-forecast-update)
- **Emisor:** Pound Sterling Live (editor: Gary Howes)
- **Documentación y notas:** Sitio de noticias y datos de divisas centrado en la libra, con sección «Exchange Rate Forecasts» que recoge y comenta previsiones de bancos (p. ej., la actualización de Danske Bank de 19/06/2017), tipos históricos y en vivo. No publica un consenso formal en la pieza leída.
- **Temática:** TFX-08 Análisis de divisas de bancos, gestoras y casas de análisis (principal) · secundarias: TFX-07
- **Calidad Q:** 58 (C) — Primariedad 8/20 · Historial 10/20 · Transparencia 8/15 · Autoridad 8/15 · Independencia 7/10 · Actualidad 8/10 · Acceso 9/10
- **Tipología:** secundaria (recopilación y comentario de previsiones bancarias)
- **Acceso:** Abierto
- **Ámbitos:** GBP y cruces; previsiones publicadas por bancos
- **Motivo de inclusión y uso:** Archivo abierto de previsiones bancarias de la libra, útil para reconstruir el historial de acierto de cada banco. Uso: EVAL (AG-20) y AS-G10N (GBP/USD, EUR/GBP); la previsión se atribuye siempre al banco de origen.
- **Restricciones de uso:** Extractos con atribución.
- **Sesgos posibles:** Selección editorial de bancos; sitio con negocio de transferencias de divisas.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Danske Bank FX Forecast Update Nordea FX SEB Research currency outlook EUR/SEK EUR/NOK»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-08).

## TFX-09 Calendario, política y riesgo soberano

#### FXF-0261 · Q 87 (A) — Bank of England — calendario de anuncios del MPC (2026 y 2027)

- **Canal oficial (URL raíz):** https://www.bankofengland.co.uk/monetary-policy/upcoming-mpc-dates (fechas de 2027 publicadas el 18/12/2025: https://www.bankofengland.co.uk/news/2025/december/mpc-dates-for-2027)
- **Emisor:** Bank of England
- **Documentación y notas:** Fechas provisionales de 2027 (todas en jueves): 4 de febrero, 18 de marzo, 29 de abril, 17 de junio, 29 de julio, 16 de septiembre, 4 de noviembre y 16 de diciembre; Monetary Policy Report en febrero, abril, julio y noviembre. Cada fecha incluye el anuncio del Bank Rate y la publicación del resumen y las actas.
- **Temática:** TFX-09 Calendario, política y riesgo soberano (principal) · secundarias: TFX-01
- **Calidad Q:** 87 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Calendario de decisiones de política monetaria del Reino Unido
- **Motivo de inclusión y uso:** Calendario oficial con un año de antelación, necesario para fijar eventos de riesgo de la libra. Uso: TR-BCM (AG-09) para el calendario de reuniones; AS-G10N (GBP/USD, EUR/GBP) y PROS (AG-10) para fijar fechas de resolución de pronósticos. Complementa a RF-0019 (TFX-01), que cubre el contenido de las decisiones.
- **Restricciones de uso:** Uso libre con atribución.
- **Sesgos posibles:** Fechas provisionales que pueden cambiar.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «FOMC meeting calendars 2026 2027 ECB monetary policy meetings schedule Bank of England MPC dates»; WebFetch: sí, nota de 18/12/2025)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-09).

#### FXF-0262 · Q 85 (A) — Banco Central de la República de Turquía (TCMB) — calendario de anuncios

- **Canal oficial (URL raíz):** https://www.tcmb.gov.tr/wps/wcm/connect/en/tcmb+en/main+menu/announcements/calendar
- **Emisor:** Central Bank of the Republic of Türkiye (TCMB)
- **Documentación y notas:** Calendario de enero de 2026 a junio de 2027 con fechas de decisión del Comité de Política Monetaria, publicación del resumen de la reunión, Informe de Inflación y Informe de Estabilidad Financiera.
- **Temática:** TFX-09 Calendario, política y riesgo soberano (principal) · secundarias: TFX-02
- **Calidad Q:** 85 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 8/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto (inglés y turco)
- **Ámbitos:** Calendario de política monetaria de Turquía
- **Motivo de inclusión y uso:** Calendario oficial de un banco central emergente con historial de decisiones sorpresivas y fuerte efecto sobre la lira. Uso: TR-BCM (AG-09) y AS-EMEA (AG-07: TRY) para fechar los eventos de riesgo de la lira. Pieza de calendario de FXF-0038 (TFX-02, portal del TCMB): misma raíz, no cuenta como fuente independiente.
- **Restricciones de uso:** Uso libre con atribución.
- **Sesgos posibles:** Historial de cambios de independencia del banco central turco (decisiones fuera de calendario posibles).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos en el calendario.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «FOMC meeting calendars 2026 2027 ECB monetary policy meetings schedule Bank of England MPC dates»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-09).

#### FXF-0264 · Q 85 (A) — OFAC (Tesoro de EE. UU.) — listas de sanciones (SDN y Consolidated Non-SDN)

- **Canal oficial (URL raíz):** https://ofac.treasury.gov/ofac-sanctions-lists (ficha de la búsqueda de sanciones, ejemplo: https://sanctionssearch.ofac.treas.gov/Details.aspx?id=38037)
- **Emisor:** Office of Foreign Assets Control, U.S. Department of the Treasury
- **Documentación y notas:** Lista SDN (personas, entidades, buques y aeronaves bloqueados) y Consolidated Non-SDN; Sanctions List Service con descargas, conjuntos personalizados por programa, búsqueda difusa, archivos delta por año y formato «Advanced Sanctions Data Model». Avisos en «Recent Actions» y por correo (GovDelivery); página de programas por país.
- **Temática:** TFX-09 Calendario, política y riesgo soberano (principal) · secundarias: —
- **Calidad Q:** 85 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria (acto administrativo)
- **Acceso:** Abierto
- **Ámbitos:** Sanciones financieras de EE. UU. por programa y país
- **Motivo de inclusión y uso:** Fuente primaria de las sanciones que afectan a la convertibilidad, a los bancos centrales sancionados y al uso del dólar. Uso: capa transversal de geopolítica y sanciones; AS-EMEA (AG-07) y AS-EMAS (AG-05) para divisas con riesgo de sanciones; CONTRA (AG-11).
- **Restricciones de uso:** Uso libre; para cumplimiento normativo usar siempre la versión vigente.
- **Sesgos posibles:** Decisiones de política exterior de EE. UU.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Migración al Advanced Sanctions Data Model; cambios técnicos documentados en su página.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «OFAC Sanctions List Service SDN list search EU Sanctions Map official»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-09).

#### FXF-0263 · Q 84 (A) — IFES — ElectionGuide (calendario y resultados de elecciones nacionales)

- **Canal oficial (URL raíz):** https://www.electionguide.org/p/methodology (acerca de: https://electionguide.org/p/about/ · anuncio de ampliación: https://www.ifes.org/news/every-election-everywhere-ifes-announces-expansion-electionguide-database)
- **Emisor:** International Foundation for Electoral Systems (IFES)
- **Documentación y notas:** Solo elecciones directas de ámbito nacional (ejecutivo, legislativo y referendos nacionales). Identifica elecciones con hasta un año de antelación; perfiles completos unas dos semanas antes; resultados solo de fuentes oficiales; actualización diaria. Desde 2025 cubre países reconocidos por la ONU, territorios con más de 50.000 habitantes y algunas regiones autónomas. Libro de códigos v3.0 (mayo de 2025).
- **Temática:** TFX-09 Calendario, política y riesgo soberano (principal) · secundarias: —
- **Calidad Q:** 84 (A) — Primariedad 17/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 14/15 · Independencia 9/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** primaria y secundaria (compilación verificada con fuentes oficiales)
- **Acceso:** Abierto; condiciones de uso en su página «Use Policy»
- **Ámbitos:** Calendario electoral mundial, resultados y participación
- **Motivo de inclusión y uso:** Calendario electoral verificado y con método publicado, imprescindible para el riesgo político de las divisas emergentes. Uso: TR-BCM (AG-09) para el calendario de eventos; AS-EMLA, AS-EMEA y AS-EMAS para elecciones con efecto cambiario; PROS (AG-10) y CONTRA (AG-11) para escenarios.
- **Restricciones de uso:** Según su política de uso; citar fecha de consulta.
- **Sesgos posibles:** Organización de asistencia democrática financiada en parte por donantes públicos; la ficha no valora la limpieza electoral.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Cambio del criterio de cobertura en 2025.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «IFES ElectionGuide election calendar database»; WebFetch: sí, página de metodología)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-09).

#### FXF-0265 · Q 80 (A) — ESMA — calendarios de calificaciones soberanas (artículo 8 bis del Reglamento de agencias de calificación)

- **Canal oficial (URL raíz):** https://www.esma.europa.eu/publications-data/questions-answers/1463 (también https://www.esma.europa.eu/node/203281)
- **Emisor:** European Securities and Markets Authority (ESMA)
- **Documentación y notas:** Pregunta y respuesta ESMA_QA_1463 (17/07/2023): las agencias registradas en la UE deben publicar a final de diciembre un calendario de los 12 meses siguientes con las fechas de publicación de calificaciones soberanas y perspectivas; las fechas deben caer en viernes; las calificaciones soberanas no solicitadas tienen un máximo de tres fechas al año (régimen vigente desde enero de 2014).
- **Temática:** TFX-09 Calendario, política y riesgo soberano (principal) · secundarias: —
- **Calidad Q:** 80 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 6/10 · Acceso 7/10
- **Tipología:** primaria (regulación)
- **Acceso:** Abierto
- **Ámbitos:** Reglas de publicación de calificaciones soberanas en la UE
- **Motivo de inclusión y uso:** Explica por qué las revisiones soberanas en la UE se publican en viernes tras el cierre y con calendario previo, lo que permite anticipar eventos de riesgo de fin de semana. Uso: TR-BCM (AG-09) y CONTRA (AG-11) para fechar riesgos de rebaja; base de FXF-0266, FXF-0267, FXF-0268 y FXF-0270.
- **Restricciones de uso:** Uso libre con atribución.
- **Sesgos posibles:** Ninguno conocido.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Vigilar revisiones del Reglamento de agencias de calificación.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Fitch Ratings sovereign ratings calendar EU CRA regulation Scope Ratings sovereign calendar 2026»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-09).

#### RF-0097 · Q 75 (B) — World Economic Forum — Global Risks Report

- **Canal oficial (URL raíz):** https://weforum.org/publications/global-risks-report-2026
- **Emisor:** World Economic Forum
- **Temática:** TFX-09 Calendario, política y riesgo soberano (principal) · secundarias: TFX-10
- **Calidad Q:** 75 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 13/15 · Independencia 7/10 · Actualidad 8/10 · Acceso 9/10
- **Tipología:** secundaria
- **Acceso:** Abierto
- **Ámbitos:** Percepción de riesgos globales a corto (2026), medio (2028) y largo plazo (2036); 21.ª edición con más de 1.300 expertos en la encuesta GRPS
- **Motivo de inclusión y uso:** Encuesta anual de percepción de riesgos; útil como medida de consenso. Uso en el Bloque A Forex: Encuesta anual de percepción de riesgos globales (geopolítica, fragmentación económica). PROS (AG-10) para el mapa de riesgos de largo plazo; capa transversal de geopolítica y sanciones.
- **Sesgos y cautelas:** Encuesta de percepción, no de probabilidad; financiación empresarial.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Real Instituto Elcano CSIS McKinsey Global Institute WEF Global Risks Report 2026»; WebFetch: sí)
- **Origen:** Reutilizada de F9 V3.2 (TF-14) en el Bloque A Forex V1.0 (2026-11-02).

#### RF-0417 · Q 75 (B) — Metaculus (plataforma de pronósticos con puntuación)

- **Canal oficial (URL raíz):** https://www.metaculus.com/ (FAQ y método: https://www.metaculus.com/faq)
- **Emisor:** Metaculus
- **Temática:** TFX-09 Calendario, política y riesgo soberano (principal) · secundarias: TFX-10
- **Calidad Q:** 75 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 11/15 · Independencia 9/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** secundaria (agregación de pronósticos de una comunidad puntuada)
- **Acceso:** Abierto
- **Ámbitos:** Probabilidades agregadas sobre geopolítica, tecnología (IA), macroeconomía y ciencia
- **Motivo de inclusión y uso:** Probabilidades explícitas y puntuadas para escenarios del Analizador y para calibrar sus propias probabilidades. AC-ESC y Evaluador (contraste de calibración). Uso en el Bloque A Forex: Pronósticos agregados con puntuación sobre elecciones, conflictos y decisiones de política. CONTRA (AG-11) y PROS (AG-10) para probabilidades de eventos políticos con efecto cambiario.
- **Sesgos y cautelas:** Preguntas a veces poco ligadas a mercados; participación sesgada hacia temas tecnológicos.
- **Criterios anti-manipulación:** Predicción de la Comunidad como mediana ponderada por recencia, resistente a valores atípicos, oculta al abrir cada pregunta y sin bots por defecto; puntuaciones propias (Baseline y Peer); reglas contra el juego de puntos (cierre anticipado, retiradas); historial de exactitud publicado (Brier 0,108 en preguntas resueltas en 2021).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Metaculus forecasting platform track record accuracy»; WebFetch: sí, FAQ)
- **Origen:** Reutilizada de F9 V3.2 (TF-12) en el Bloque A Forex V1.0 (2026-11-02).

#### FXF-0266 · Q 74 (B) — Scope Ratings — calificaciones soberanas y calendario anual

- **Canal oficial (URL raíz):** https://scoperatings.com/ (calendario soberano y del sector público 2026, entidad del Reino Unido: https://scoperatings.com/dam/jcr:b9fcfb49-48b9-4195-896a-0b975a5d2289/Scope%20Ratings_Calendar_Sovereign%20and%20Public%20Sector_2026%20UK.pdf · investigación: https://scoperatings.com/ratings-and-research/research/EN/179748)
- **Emisor:** Scope Ratings (Scope Group, Berlín)
- **Documentación y notas:** Agencia de calificación europea, la única europea aceptada por el BCE en el marco de evaluación del crédito del Eurosistema (según su propio sitio). Publica cada año calendarios de calificación soberana y del sector público para sus entidades de la UE y del Reino Unido (archivo de 2023, 2024 y 2025 devuelto en la búsqueda). MNI la incluye entre las cinco agencias más relevantes.
- **Temática:** TFX-09 Calendario, política y riesgo soberano (principal) · secundarias: —
- **Calidad Q:** 74 (B) — Primariedad 17/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 12/15 · Independencia 7/10 · Actualidad 8/10 · Acceso 8/10
- **Tipología:** primaria (calificaciones propias)
- **Acceso:** Abierto (calificaciones e informes con registro)
- **Ámbitos:** Calificaciones soberanas, sobre todo de Europa
- **Motivo de inclusión y uso:** Quinta opinión soberana, de origen europeo y aceptada por el BCE, útil cuando difiere de las tres grandes. Uso: AS-EMEA (AG-07) y AS-G10N para riesgo soberano europeo; CONTRA (AG-11).
- **Restricciones de uso:** Según condiciones de Scope.
- **Sesgos posibles:** Modelo emisor-pagador en las calificaciones solicitadas.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** REDIRIGIDO
- **Última verificación:** 2026-11-02 (búsqueda web: «Fitch Ratings sovereign ratings calendar EU CRA regulation Scope Ratings sovereign calendar 2026»; WebFetch: sí, el PDF del calendario redirigió a la página de noticias de Scope)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-09).

#### RF-0234 · Q 72 (B) — S&P Global Ratings — Research

- **Canal oficial (URL raíz):** https://www.spglobal.com/ratings/en/research/ (ejemplos: https://spglobal.com/ratings/en/research/articles/210726-sovereign-ratings-history-12029439 · https://www.spglobal.com/ratings/en/research/articles/200511-an-overview-of-sovereign-rating-actions-related-to-covid-19-11484790)
- **Emisor:** S&P Global Ratings
- **Temática:** TFX-09 Calendario, política y riesgo soberano (principal) · secundarias: TFX-02
- **Calidad Q:** 72 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 14/15 · Independencia 5/10 · Actualidad 10/10 · Acceso 5/10
- **Tipología:** primaria (acciones de rating) y secundaria (análisis)
- **Acceso:** Comunicados de calificación y parte de la investigación con registro; el resto, de pago
- **Ámbitos:** Calificaciones de soberanos, empresas y finanzas estructuradas; historial de calificaciones soberanas
- **Motivo de inclusión y uso:** Una de las tres grandes agencias de calificación (junto con Moody's, RF-0231, y Fitch). Uso en el Bloque A Forex: Calificaciones y análisis soberanos con calendario público de revisiones en la UE. AS-EMLA, AS-EMEA y AS-EMAS para el riesgo soberano de divisas emergentes; CONTRA (AG-11) para riesgo de cola por rebaja de calificación.
- **Sesgos y cautelas:** Conflicto «emisor-pagador»; errores documentados en 2008. La página leída cargó vacía.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «S&P Global Ratings research and Fitch Ratings research sovereign outlook»; WebFetch: sí, la página no mostró contenido)
- **Origen:** Reutilizada de F9 V3.2 (TF-05) en el Bloque A Forex V1.0 (2026-11-02).

#### FXF-0267 · Q 71 (B) — Fitch Ratings — calificaciones soberanas

- **Canal oficial (URL raíz):** No capturado en la verificación (sitio oficial de Fitch Ratings). Piezas: calendario de revisiones soberanas de las cinco agencias principales recopilado por MNI (29/12/2025): https://mnimarkets.com/articles/mni-sovereign-rating-review-calendar-2026-1767004684700 · retirada de las calificaciones de Rusia: https://www.hellenicshippingnews.com/fitch-withdraws-russias-ratings/
- **Emisor:** Fitch Ratings (Fitch Group, Hearst)
- **Documentación y notas:** Una de las tres grandes agencias de calificación soberana; publica calendario de revisiones soberanas en la UE (artículo 8 bis, FXF-0265). MNI la incluye con Moody's, S&P, Morningstar DBRS y Scope.
- **Temática:** TFX-09 Calendario, política y riesgo soberano (principal) · secundarias: TFX-02
- **Calidad Q:** 71 (B) — Primariedad 17/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 14/15 · Independencia 6/10 · Actualidad 8/10 · Acceso 5/10
- **Tipología:** primaria (calificaciones propias)
- **Acceso:** Comunicados de calificación abiertos con registro; informes de pago
- **Ámbitos:** Calificaciones soberanas mundiales, perspectivas y vigilancias
- **Motivo de inclusión y uso:** Completa a S&P (RF-0234) y Moody's (RF-0231) para el riesgo soberano de las divisas emergentes. Uso: AS-EMLA, AS-EMEA y AS-EMAS; CONTRA (AG-11) para riesgo de rebaja.
- **Restricciones de uso:** Según condiciones de Fitch.
- **Sesgos posibles:** Modelo emisor-pagador; retiradas de calificación por sanciones.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios confirmados en la verificación.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Fitch Ratings sovereign ratings calendar EU CRA regulation Scope Ratings sovereign calendar 2026»; WebFetch: sí, sobre el artículo de MNI; el sitio de Fitch no se leyó)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-09).

#### RF-0231 · Q 71 (B) — Moody's Ratings

- **Canal oficial (URL raíz):** ratings.moodys.io (según Wikipedia; comprobar en el barrido HT-02)
- **Emisor:** Moody's Ratings (Moody's Corporation; fundada en 1909 por John Moody)
- **Temática:** TFX-09 Calendario, política y riesgo soberano (principal) · secundarias: TFX-02
- **Calidad Q:** 71 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 14/15 · Independencia 5/10 · Actualidad 10/10 · Acceso 5/10
- **Tipología:** primaria (acciones de calificación) y secundaria (análisis)
- **Acceso:** Comunicados de calificación públicos; informes con registro o suscripción
- **Ámbitos:** Calificaciones crediticias de soberanos, empresas, bancos y finanzas estructuradas; perspectivas sectoriales
- **Motivo de inclusión y uso:** Una de las tres grandes agencias (junto con S&P y Fitch, alrededor del 95 % del mercado). Sus cambios de calificación son hechos con efecto en el mercado. Uso en el Bloque A Forex: Calificaciones soberanas y perspectivas, con calendario público en la UE. AS-EMLA, AS-EMEA, AS-EMAS y CONTRA (AG-11).
- **Sesgos y cautelas:** Conflicto «emisor-pagador»; fallos de calificación documentados en la crisis de 2008 (Financial Crisis Inquiry Report).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Big Three credit rating agencies wikipedia» → artículos de Wikipedia «Moody's Ratings» y «Big Three (credit rating agencies)»; WebFetch: sí, sobre Wikipedia)
- **Origen:** Reutilizada de F9 V3.2 (TF-05) en el Bloque A Forex V1.0 (2026-11-02).

#### RF-0237 · Q 70 (B) — Morningstar DBRS

- **Canal oficial (URL raíz):** https://dbrs.morningstar.com/ (ejemplo: https://dbrs.morningstar.com/research/327566/dbrs-releases-report-on-deutsche-bank-ag)
- **Emisor:** Morningstar DBRS (Morningstar Inc.)
- **Temática:** TFX-09 Calendario, política y riesgo soberano (principal) · secundarias: —
- **Calidad Q:** 70 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 12/15 · Independencia 5/10 · Actualidad 9/10 · Acceso 7/10
- **Tipología:** primaria (acciones de rating) y secundaria
- **Acceso:** Comunicados públicos; investigación de crédito con registro o suscripción
- **Ámbitos:** Calificaciones crediticias (agencia NRSRO y CRA registrada); bancos, soberanos, titulizaciones
- **Motivo de inclusión y uso:** Agencia de calificación alternativa a las tres grandes; útil cuando estas difieren. Uso en el Bloque A Forex: Cuarta agencia (y europea) en calificaciones soberanas, con calendario en la UE. Contraste de las tres grandes para AS-EMEA y AS-G10N.
- **Sesgos y cautelas:** Conflicto «emisor-pagador»; mismo grupo que Morningstar (RF-0048).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Deutsche Bank Research dbresearch.com publications»; WebFetch: sí)
- **Origen:** Reutilizada de F9 V3.2 (TF-05) en el Bloque A Forex V1.0 (2026-11-02).

#### FXF-0268 · Q 69 (B) — MNI — calendarios de mercado (reuniones del FOMC y revisiones de calificación soberana)

- **Canal oficial (URL raíz):** https://mnimarkets.com/calendars/fomc-meeting-calendar (fechas del FOMC de 2027: https://www.mnimarkets.com/articles/mni-federal-reserve-sets-2027-fomc-meeting-schedule-1757093400287 · calendario soberano 2026: https://mnimarkets.com/articles/mni-sovereign-rating-review-calendar-2026-1767004684700 · PDF: https://media.marketnews.com/MNI_Sovereign_Rating_Review_Calendar_2026_29077cbd54.pdf)
- **Emisor:** MNI Market News International (misma raíz que FXF-0222)
- **Documentación y notas:** Fechas provisionales del FOMC de 2027 publicadas el 05/09/2025: 26–27 de enero, 16–17 de marzo, 27–28 de abril, 8–9 de junio, 27–28 de julio, 14–15 de septiembre, 26–27 de octubre y 7–8 de diciembre (y 25–26 de enero de 2028). Calendario de revisiones soberanas 2026 de Fitch, Moody's, S&P, Morningstar DBRS y Scope (29/12/2025; «indicativo»; las agencias pueden revisar fuera de calendario).
- **Temática:** TFX-09 Calendario, política y riesgo soberano (principal) · secundarias: TFX-07
- **Calidad Q:** 69 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 12/15 · Independencia 8/10 · Actualidad 9/10 · Acceso 7/10
- **Tipología:** secundaria (recopilación de calendarios oficiales)
- **Acceso:** Artículos de calendario abiertos
- **Ámbitos:** Calendario de la Fed y de las agencias de calificación
- **Motivo de inclusión y uso:** Reúne en un solo documento las fechas de revisión soberana de las cinco agencias, que de otro modo están dispersas. Uso: TR-BCM (AG-09) para la agenda; CONTRA (AG-11) para riesgos de rebaja en fin de semana; las fechas del FOMC se confirman en la Reserva Federal (RF-0016).
- **Restricciones de uso:** Citar la fuente oficial de cada fecha.
- **Sesgos posibles:** Copia de calendarios de terceros; no es raíz independiente de MNI (FXF-0222).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsquedas web: «FOMC meeting calendars 2026 2027…» y «Fitch Ratings sovereign ratings calendar EU CRA regulation…»; WebFetch: sí, dos artículos)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-09).

#### FXF-0269 · Q 68 (B) — Economic Policy Uncertainty (EPU) — índices de incertidumbre de política económica (Baker, Bloom y Davis)

- **Canal oficial (URL raíz):** www.PolicyUncertainty.com (según NBER WP 26243: https://www.nber.org/papers/w26243.pdf)
- **Emisor:** Scott R. Baker, Nicholas Bloom y Steven J. Davis (proyecto académico)
- **Documentación y notas:** Índices de incertidumbre construidos con noticias de prensa (Baker, Bloom y Davis, 2016), con actualizaciones mensuales en PolicyUncertainty.com según Davis (2019), «Rising Policy Uncertainty», NBER WP 26243. Macrosynergy lo clasifica entre las medidas de incertidumbre basadas en noticias.
- **Temática:** TFX-09 Calendario, política y riesgo soberano (principal) · secundarias: TFX-10
- **Calidad Q:** 68 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 14/15 · Independencia 9/10 · Actualidad 4/10 · Acceso 4/10
- **Tipología:** primaria (índice académico construido por los autores)
- **Acceso:** Abierto (descargas en el sitio del proyecto); canal no leído en esta verificación
- **Ámbitos:** Incertidumbre de política económica por país, incertidumbre de política monetaria y comercial
- **Motivo de inclusión y uso:** Medida cuantitativa del riesgo político usada en la literatura de divisas (prima de riesgo y refugio). Uso: TR-BCM (AG-09) y AS-ESTR (AG-08: cestas de refugio); MOTOR (AG-13) como variable explicativa.
- **Restricciones de uso:** Uso académico con cita de los autores.
- **Sesgos posibles:** Basado en recuentos de prensa; sesgo hacia países con prensa digitalizada.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Revisiones de la base de periódicos; vigilar.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «policyuncertainty.com Economic Policy Uncertainty index Geopolitical Risk index Caldara Iacoviello World Uncertainty Index data»; WebFetch: sí, NBER WP 26243 y Macrosynergy; el sitio PolicyUncertainty.com no se leyó)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-09).

#### FXF-0270 · Q 64 (C) — EthiFinance Ratings — calendario de calificaciones soberanas (España y Portugal)

- **Canal oficial (URL raíz):** https://www.ethifinance.com/sovereign-ratings-calendar_en_2026
- **Emisor:** EthiFinance (la página leída no nombra la entidad registrada)
- **Documentación y notas:** Calendario 2026 bajo el Reglamento (CE) 1060/2009: Reino de España (02/01, 26/06 y 18/12/2026) y República Portuguesa (10/04 y 09/10/2026); fechas en viernes; revisión trimestral del calendario.
- **Temática:** TFX-09 Calendario, política y riesgo soberano (principal) · secundarias: —
- **Calidad Q:** 64 (C) — Primariedad 15/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 9/15 · Independencia 6/10 · Actualidad 7/10 · Acceso 7/10
- **Tipología:** primaria (calificaciones propias)
- **Acceso:** Abierto (calendario)
- **Ámbitos:** Calificación soberana de España y Portugal
- **Motivo de inclusión y uso:** Agencia de origen ibérico con calendario soberano propio; contraste menor para el riesgo soberano del euro periférico. Uso: AS-G10N (EUR) y CONTRA (AG-11).
- **Restricciones de uso:** Según condiciones del emisor.
- **Sesgos posibles:** Agencia pequeña; cobertura soberana muy limitada.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** No confirmados en la verificación.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Fitch Ratings sovereign ratings calendar EU CRA regulation Scope Ratings sovereign calendar 2026»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-09).

#### RF-0446 · Q 63 (C) — Good Judgment Inc (Superforecasters)

- **Canal oficial (URL raíz):** https://goodjudgment.com/
- **Emisor:** Good Judgment Inc
- **Temática:** TFX-09 Calendario, política y riesgo soberano (principal) · secundarias: —
- **Calidad Q:** 63 (C) — Primariedad 12/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 12/15 · Independencia 6/10 · Actualidad 9/10 · Acceso 5/10
- **Tipología:** secundaria (pronósticos agregados de superpronosticadores)
- **Acceso:** Restringido (FutureFirst y pronósticos a medida de pago; resúmenes públicos)
- **Ámbitos:** Pronósticos probabilísticos sobre geopolítica, política monetaria y macro
- **Motivo de inclusión y uso:** Contraste de probabilidades de escenarios con un grupo de pronosticadores de historial medido. AC-ESC. Uso en el Bloque A Forex: Pronósticos de superpronosticadores sobre geopolítica y política económica. PROS (AG-10) y CONTRA (AG-11) para escenarios de cola.
- **Sesgos y cautelas:** Empresa comercial; el historial publicado lo presenta la propia empresa (p. ej., 66 % más precisos que los futuros en puntos de giro de la Fed; 554 preguntas resueltas a septiembre de 2023), sin auditoría independiente en la página.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Metaculus Good Judgment superforecasters forecasting track record»; WebFetch: sí, página «The Superforecasters’ Track Record»)
- **Origen:** Reutilizada de F9 V3.2 (TF-14) en el Bloque A Forex V1.0 (2026-11-02).

#### FXF-0271 · Q 62 (C) — Geopolitical Risk Index (GPR) — índice de riesgo geopolítico (Caldara e Iacoviello)

- **Canal oficial (URL raíz):** No capturado en la verificación (página de los autores). Pieza índice: https://macrosynergy.com/?p=40564 (taxonomía de medidas de riesgo; cita Datta et al., 2017, IFDP 1216)
- **Emisor:** Dario Caldara y Matteo Iacoviello (Federal Reserve Board)
- **Documentación y notas:** Índice basado en recuentos de prensa sobre riesgo de guerra, terrorismo y tensiones geopolíticas (Caldara e Iacoviello, 2016, según la taxonomía recogida por Macrosynergy).
- **Temática:** TFX-09 Calendario, política y riesgo soberano (principal) · secundarias: TFX-10
- **Calidad Q:** 62 (C) — Primariedad 14/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 13/15 · Independencia 9/10 · Actualidad 3/10 · Acceso 2/10
- **Tipología:** primaria (índice académico)
- **Acceso:** Canal no verificado; HT-02 debe localizar la página oficial
- **Ámbitos:** Riesgo geopolítico global y por país
- **Motivo de inclusión y uso:** Medida estándar de riesgo geopolítico para estudiar el comportamiento de las divisas refugio (JPY, CHF, USD). Uso: AS-ESTR (AG-08) y capa transversal de geopolítica; MOTOR (AG-13) como variable explicativa.
- **Restricciones de uso:** Uso académico con cita.
- **Sesgos posibles:** Sesgo de cobertura de prensa anglosajona.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Revisiones del índice publicadas por los autores; no comprobadas.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «policyuncertainty.com Economic Policy Uncertainty index Geopolitical Risk index Caldara Iacoviello World Uncertainty Index data»; WebFetch: sí, sobre Macrosynergy)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-09).

#### RF-0244 · Q 58 (C) — Trading Economics

- **Canal oficial (URL raíz):** https://tradingeconomics.com/ (ejemplo: https://tradingeconomics.com/sdr:ln)
- **Emisor:** Trading Economics (titularidad no declarada en la página leída)
- **Temática:** TFX-09 Calendario, política y riesgo soberano (principal) · secundarias: TFX-05
- **Calidad Q:** 58 (C) — Primariedad 8/20 · Historial 10/20 · Transparencia 6/15 · Autoridad 9/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 7/10
- **Tipología:** agregador con previsiones de modelo propio
- **Acceso:** Consulta abierta; API y descargas masivas de pago
- **Ámbitos:** Indicadores económicos por país, calendario, cotizaciones, consenso de beneficios y previsiones propias («global macro models projections and analysts expectations»)
- **Motivo de inclusión y uso:** Previsiones explícitas y masivas por indicador, contrastables por el Evaluador. Uso en el Bloque A Forex: Calendario económico global con previsiones y series por país. TR-BCM (AG-09) para el calendario de datos y reuniones; los Analistas de segmento para la agenda semanal (verificar siempre el dato en la fuente oficial).
- **Sesgos y cautelas:** Metodología de previsión apenas descrita; posible solape con TF-06 (decidir al fusionar).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Schroders insights economic and strategy viewpoint Man Group Man Institute»; WebFetch: sí)
- **Origen:** Reutilizada de F9 V3.2 (TF-05) en el Bloque A Forex V1.0 (2026-11-02).

#### FXF-0272 · Q 55 (C) — Central Bank Watch — calendario de reuniones de bancos centrales

- **Canal oficial (URL raíz):** https://centralbank.watch/tools/calendar/
- **Emisor:** Central Bank Watch (proyecto independiente de análisis de expectativas de política monetaria)
- **Documentación y notas:** Calendario con fechas de reunión de la Fed, el BCE, el BoE, el BoJ, el RBA, el BoC y el RBI (RBNZ, SNB y PBoC en navegación; Norges Bank, Riksbank, BoK y BCB «en ampliación»), descarga .ics y herramientas de tipos reales y curvas. Fecha de actualización contradictoria (01/11/2026 en página, 30/06/2026 en metadatos). «Uso educativo; no es asesoramiento».
- **Temática:** TFX-09 Calendario, política y riesgo soberano (principal) · secundarias: TFX-01
- **Calidad Q:** 55 (C) — Primariedad 7/20 · Historial 10/20 · Transparencia 6/15 · Autoridad 6/15 · Independencia 8/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** secundaria (recopilación)
- **Acceso:** Abierto
- **Ámbitos:** Calendario conjunto de bancos centrales del G10 y algunos emergentes
- **Motivo de inclusión y uso:** Vista conjunta y descargable de fechas de varios bancos centrales para montar la agenda semanal. Uso: TR-BCM (AG-09) como borrador de agenda; cada fecha se confirma en el banco central (TFX-01, TFX-02).
- **Restricciones de uso:** Uso educativo según el sitio.
- **Sesgos posibles:** Autoría no identificada; fuentes de las fechas no declaradas.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Desconocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «FOMC meeting calendars 2026 2027 ECB monetary policy meetings schedule Bank of England MPC dates»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-09).

#### FXF-0273 · Q 52 (C) — Forex Factory — calendario económico con clasificación de impacto

- **Canal oficial (URL raíz):** No capturado en la verificación. Pieza índice: comparación de calendarios económicos en el foro de BabyPips: https://forums.babypips.com/t/a-brief-comparison-of-5-popular-economic-calendars/177165
- **Emisor:** Forex Factory
- **Documentación y notas:** Calendario económico muy usado por operadores de divisas, que filtra los datos por impacto esperado; en la comparación de BabyPips (con BabyPips, DailyFX, MetaQuotes y Myfxbook) muestra solo los datos de mayor impacto y las cifras de consenso difieren entre calendarios.
- **Temática:** TFX-09 Calendario, política y riesgo soberano (principal) · secundarias: TFX-07
- **Calidad Q:** 52 (C) — Primariedad 6/20 · Historial 10/20 · Transparencia 5/15 · Autoridad 7/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 7/10
- **Tipología:** secundaria (recopilación)
- **Acceso:** Abierto
- **Ámbitos:** Calendario de datos macro con consenso e impacto por divisa
- **Motivo de inclusión y uso:** Referencia práctica de los datos que el mercado de divisas minorista considera de alto impacto. Uso: TR-BCM (AG-09) y los Analistas de segmento como borrador de agenda; el consenso se contrasta con Trading Economics (RF-0244) y el dato con la fuente oficial.
- **Restricciones de uso:** Según condiciones del sitio.
- **Sesgos posibles:** Clasificación de impacto subjetiva; consenso de fuente no declarada.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Desconocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Forex Factory economic calendar impact Econoday economic calendar consensus»; WebFetch: sí, sobre el foro de BabyPips; el sitio de Forex Factory no se leyó)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-09).

## TFX-10 Repositorios académicos, think tanks y blogs especializados en divisas

#### FXF-0281 · Q 84 (A) — NBER — Programa International Finance and Macroeconomics (IFM)

- **Canal oficial (URL raíz):** https://www.nber.org/programs-projects/programs-working-groups/international-finance-and-macroeconomics (reunión de primavera de 2020: https://www.nber.org/conferences/international-finance-and-macroeconomics-program-meeting-spring-2020 · historia del programa: https://frankel.scholars.harvard.edu/program-international-finance-and-macroeconomics)
- **Emisor:** National Bureau of Economic Research (NBER)
- **Documentación y notas:** Programa fundado en 1992 y dirigido por Jeffrey Frankel hasta 2017 (después, Mark Aguiar y Linda Tesar); agrupa los documentos de trabajo, reuniones semestrales e informes en el NBER Reporter sobre finanzas internacionales. Ejemplo de trabajo vinculado: «The Global Factor Structure of Exchange Rates» (NBER w27892). Las agendas de las reuniones (p. ej., IFMs20, organizada por Cristina Arellano y Oleg Itskhoki) listan los trabajos presentados.
- **Temática:** TFX-10 Repositorios académicos, think tanks y blogs especializados en divisas (principal) · secundarias: —
- **Calidad Q:** 84 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** primaria (investigación original sin revisión por pares completa)
- **Acceso:** Abierto en su mayor parte
- **Ámbitos:** Tipos de cambio, flujos de capital, dólar dominante, crisis, política monetaria internacional
- **Motivo de inclusión y uso:** Canal más directo para detectar la literatura de frontera sobre divisas antes de su publicación. Uso: DOC-A (AG-14) como fuente de vigilancia para F7; TR-BCM (AG-09) y AS-ESTR (AG-08) para resultados nuevos sobre factores cambiarios. Pieza temática de RF-0008.
- **Restricciones de uso:** Citar como documento de trabajo.
- **Sesgos posibles:** Trabajos sin revisión por pares en su primera versión.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Cambios de dirección del programa (2017).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «NBER International Finance and Macroeconomics program working papers IFM»; WebFetch: sí, página de la reunión de 2020 en nber.org y página de Frankel)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-10).

#### RF-0422 · Q 84 (A) — BIS Working Papers

- **Canal oficial (URL raíz):** https://www.bis.org/wpapers
- **Emisor:** Bank for International Settlements (BIS)
- **Temática:** TFX-10 Repositorios académicos, think tanks y blogs especializados en divisas (principal) · secundarias: TFX-03
- **Calidad Q:** 84 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria (documentos de trabajo)
- **Acceso:** Abierto
- **Ámbitos:** Investigación de economistas del BIS y ocasionalmente de bancos centrales y universidades: política monetaria, estabilidad financiera, mercados
- **Motivo de inclusión y uso:** Investigación de frontera de banca central con datos propios del BIS. AC-MP, AC-RF,. Uso en el Bloque A Forex: Serie con numerosos trabajos sobre divisas (base cruzada, dólar global, intervención, encuesta trienal). DOC-A (AG-14) y los Analistas transversales TR-BCM y TR-PFV para literatura de banco central sobre divisas.
- **Sesgos y cautelas:** Las opiniones son de los autores y no necesariamente del BIS; sin revisión por pares completa.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ECB Working Paper Series BIS Working Papers IMF Working Papers»; WebFetch: sí)
- **Origen:** Reutilizada de F9 V3.2 (TF-13) en el Bloque A Forex V1.0 (2026-11-02).

#### RF-0423 · Q 84 (A) — ECB Working Paper Series

- **Canal oficial (URL raíz):** https://www.ecb.europa.eu/press/research-publications/working-papers
- **Emisor:** Banco Central Europeo (BCE)
- **Temática:** TFX-10 Repositorios académicos, think tanks y blogs especializados en divisas (principal) · secundarias: —
- **Calidad Q:** 84 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria (documentos de trabajo)
- **Acceso:** Abierto
- **Ámbitos:** Investigación económica relevante para las funciones del BCE: política monetaria, transmisión, banca, mercados del área del euro
- **Motivo de inclusión y uso:** Literatura de banca central europea para fundamentar análisis del área del euro. AC-MP, AC-MAC. Uso en el Bloque A Forex: Trabajos del BCE sobre el euro internacional, el tipo de cambio y la transmisión. AS-G10N y TR-BCM (AG-09).
- **Sesgos y cautelas:** Trabajo en curso; las opiniones son de los autores y no necesariamente del BCE.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ECB Working Paper Series BIS Working Papers IMF Working Papers»; WebFetch: sí)
- **Origen:** Reutilizada de F9 V3.2 (TF-13) en el Bloque A Forex V1.0 (2026-11-02).

#### RF-0461 · Q 84 (A) — IMF Working Papers

- **Canal oficial (URL raíz):** https://www.imf.org/en/Publications/WP (ruta de la serie vista en los resultados; página leída: https://www.imf.org/en/Publications/WP/Issues/2016/12/30/Working-Paper-Summaries-WP-95-62-95-146-2022)
- **Emisor:** Fondo Monetario Internacional (FMI)
- **Temática:** TFX-10 Repositorios académicos, think tanks y blogs especializados en divisas (principal) · secundarias: TFX-03
- **Calidad Q:** 84 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria (documentos de trabajo)
- **Acceso:** Abierto (con DOI)
- **Ámbitos:** Unos 300 documentos al año de personal del FMI: balanza de pagos, política monetaria y fiscal, liquidez global, economías nacionales
- **Motivo de inclusión y uso:** Investigación aplicada de un organismo internacional con cobertura de emergentes. AC-MAC, AC-FX. Uso en el Bloque A Forex: Serie con trabajos sobre regímenes cambiarios, controles de capital, intervención y valoración (EBA). TR-BCM (AG-09), AS-EMLA, AS-EMEA y AS-EMAS.
- **Sesgos y cautelas:** No representan la opinión del FMI; sin revisión por pares completa.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «IMF Working Papers series imf.org publications»; WebFetch: sí)
- **Origen:** Reutilizada de F9 V3.2 (TF-13) en el Bloque A Forex V1.0 (2026-11-02).

#### RF-0424 · Q 83 (A) — Banco de España — Documentos de Trabajo

- **Canal oficial (URL raíz):** https://www.bde.es/bde/en/secciones/informes/analisis-economico-e-investigacion/documentos-de-trabajo/ (repositorio: https://repositorio.bde.es/handle/123456789/5661)
- **Emisor:** Banco de España
- **Temática:** TFX-10 Repositorios académicos, think tanks y blogs especializados en divisas (principal) · secundarias: —
- **Calidad Q:** 83 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 14/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria (documentos de trabajo)
- **Acceso:** Abierto (PDF; serie desde 1978 en el repositorio institucional)
- **Ámbitos:** Macroeconomía, política monetaria, banca, finanzas y economía española; último visto: n.º 2640 (26/10/2026)
- **Motivo de inclusión y uso:** Investigación de banco central con foco España y área del euro. AC-MAC y AC-MP con perspectiva española. Uso en el Bloque A Forex: Documentos de trabajo del Banco de España, con líneas sobre Latinoamérica, divisas y flujos de capital. AS-EMLA (AG-06) y AS-G10N.
- **Sesgos y cautelas:** Opiniones de los autores; sin revisión por pares completa.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Banco de España documentos de trabajo Federal Reserve FEDS finance and economics discussion series»; WebFetch: sí)
- **Origen:** Reutilizada de F9 V3.2 (TF-13) en el Bloque A Forex V1.0 (2026-11-02).

#### RF-0008 · Q 82 (A) — NBER Working Papers (National Bureau of Economic Research)

- **Canal oficial:** nber.org/papers
- **Documentación y notas:** Trabajos con página propia por número (nber.org/papers/wNNNNN); citar número de WP y año; versiones abiertas del autor frecuentes
- **Temática:** TFX-10 Repositorios académicos, think tanks y blogs especializados en divisas (principal) · secundarias: —
- **Calidad Q:** 82 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 14/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 9/10
- **Nivel de fiabilidad en V2.4:** B
- **Tipología:** primaria (trabajos originales sin revisión por pares completa)
- **Motivo de inclusión:** Documentos de trabajo de investigación económica de primer nivel; muchos se publican después en revistas revisadas por pares. Uso en el Bloque A Forex: El programa IFM del NBER concentra los trabajos de divisas (FXF-0281). DOC-A (AG-14) para detectar trabajos nuevos sobre tipos de cambio; los Analistas transversales como literatura de frontera.
- **Ámbitos:** Investigación económica y financiera; literatura de frontera; datos y metodologías nuevos
- **Restricciones de uso:** Muchos WP son de descarga gratuita y otros tienen coste o requieren registro; verificar pieza a pieza; un WP no está revisado por pares: citarlo como documento de trabajo
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Sesgos posibles:** Contenido no revisado por pares en el momento de la publicación; verificar si existe versión publicada posterior
- **Cambios de propiedad o de metodología:** Sin cambios conocidos
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «NBER International Finance and Macroeconomics program working papers IFM»; WebFetch: sí, página de conferencia del programa IFM en nber.org, que enlaza la página del programa)
- **Origen:** Reutilizada de F9 V3.2 (TF-13) en el Bloque A Forex V1.0 (2026-11-02).

#### RF-0426 · Q 81 (A) — Fed in Print (catálogo de investigación del Sistema de la Reserva Federal)

- **Canal oficial (URL raíz):** https://www.fedinprint.org/
- **Emisor:** Sistema de la Reserva Federal (Board of Governors y los 12 bancos regionales)
- **Temática:** TFX-10 Repositorios académicos, think tanks y blogs especializados en divisas (principal) · secundarias: —
- **Calidad Q:** 81 (A) — Primariedad 14/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** terciaria (catálogo de publicaciones)
- **Acceso:** Abierto (API y RSS)
- **Ámbitos:** Documentos de trabajo, informes y blogs de toda la Reserva Federal, por banco, serie, autor y código JEL
- **Motivo de inclusión y uso:** Punto único de búsqueda de la investigación de la Fed (FEDS, Staff Reports, Liberty Street, On the Economy). AG-16, AC-MP. Uso en el Bloque A Forex: Catálogo único de la investigación del Sistema de la Reserva Federal (IFDP del Board, Liberty Street, notas FEDS), con mucha literatura sobre el dólar. DOC-A (AG-14) y TR-BCM (AG-09).
- **Sesgos y cautelas:** Enlaza al texto en la web de cada banco; no aloja contenido.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «FRASER Federal Reserve Bank of St. Louis digital library EconStor ZBW open access economics repository»; WebFetch: sí, ficha de registro en fedinprint.org)
- **Origen:** Reutilizada de F9 V3.2 (TF-13) en el Bloque A Forex V1.0 (2026-11-02).

#### FXF-0282 · Q 80 (A) — Bruegel — base de datos de tipos de cambio efectivos reales (Darvas, 178 países)

- **Canal oficial (URL raíz):** https://www.bruegel.org/publications/datasets/real-effective-exchange-rates-for-178-countries-a-new-database (documento de trabajo: https://bruegel.org/working-paper/real-effective-exchange-rates-178-countries-new-database · RePEc: https://ideas.repec.org/p/bre/wpaper/716.html)
- **Emisor:** Bruegel (Bruselas); autor Zsolt Darvas
- **Documentación y notas:** TCER y TCEN basados en el IPC: anual para 178 países y la zona del euro (índice amplio con 172 socios desde 1995; estrecho con 67 desde 1960) y mensual para 177 países (amplio con 120 socios desde 1993; estrecho con 51 desde 1960). Publicada el 15/03/2012 y actualizada regularmente; última versión del 11/10/2026 (fichero REER_database_ver11Oct2026.zip). Metodología en los documentos de trabajo de Darvas (2012 y 2021).
- **Temática:** TFX-10 Repositorios académicos, think tanks y blogs especializados en divisas (principal) · secundarias: TFX-03
- **Calidad Q:** 80 (A) — Primariedad 16/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 13/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** primaria (base de datos construida por el autor con datos oficiales)
- **Acceso:** Abierto (descarga ZIP)
- **Ámbitos:** Tipos de cambio efectivos reales y nominales de casi todos los países
- **Motivo de inclusión y uso:** TCER con cobertura de emergentes más amplia que la del BPI y actualización mensual, base para valoración PPA y BEER. Uso: AS-ESTR (AG-08: valor), los Analistas de emergentes (AS-EMAS, AS-EMLA, AS-EMEA) y MOTOR (AG-13, módulo de valoración). Pieza de RF-0093.
- **Restricciones de uso:** Uso libre con cita del autor y versión.
- **Sesgos posibles:** Ponderaciones basadas en el comercio de bienes; IPC heterogéneos entre países.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Actualizaciones con versión fechada; vigilar revisiones de ponderaciones.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Bruegel real effective exchange rates database Darvas 178 countries update»; WebFetch: sí, página del conjunto de datos)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-10).

#### FXF-0283 · Q 79 (B) — Índice Chinn-Ito de apertura financiera (KAOPEN)

- **Canal oficial (URL raíz):** https://web.pdx.edu/~ito/Chinn-Ito_website.htm (descripción de datos: https://web.pdx.edu/~ito/Readme_kaopen2023.pdf · anuncio de la actualización a 2023, 26/01/2026: https://econbrowser.com/archives/2026/01/chinn-ito-financial-openness-index-updated-to-2023)
- **Emisor:** Menzie Chinn (Universidad de Wisconsin) e Hiro Ito (Universidad Estatal de Portland)
- **Documentación y notas:** Índice de apertura de la cuenta de capital normalizado entre 0 y 1 (1 = más abierto), obtenido como primer componente principal de las clasificaciones de jure de controles del FMI (componente de capital suavizado); publicado originalmente en el Journal of Development Economics (2006); actualizado hasta 2023 (Ito y Chinn, 2025).
- **Temática:** TFX-10 Repositorios académicos, think tanks y blogs especializados en divisas (principal) · secundarias: TFX-09
- **Calidad Q:** 79 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 13/15 · Independencia 10/10 · Actualidad 7/10 · Acceso 9/10
- **Tipología:** primaria (índice académico)
- **Acceso:** Abierto
- **Ámbitos:** Controles de capital y apertura financiera por país
- **Motivo de inclusión y uso:** Medida estándar de controles de capital para clasificar regímenes de convertibilidad en emergentes. Uso: AS-EMAS, AS-EMLA y AS-EMEA para el régimen de controles; MOTOR (AG-13) como variable de control.
- **Restricciones de uso:** Uso académico con cita.
- **Sesgos posibles:** Medida de jure: puede no reflejar la aplicación efectiva; desfase de unos dos años.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Depende de las clasificaciones del AREAER del FMI.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Ilzetzki Reinhart Rogoff exchange rate arrangements classification data update Chinn-Ito financial openness index»; WebFetch: sí, entrada de Econbrowser; la web de Ito no se leyó)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-10).

#### RF-0090 · Q 78 (B) — CEPR — VoxEU

- **Canal oficial (URL raíz):** https://cepr.org/voxeu
- **Emisor:** Centre for Economic Policy Research (CEPR)
- **Temática:** TFX-10 Repositorios académicos, think tanks y blogs especializados en divisas (principal) · secundarias: —
- **Calidad Q:** 78 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 13/15 · Independencia 9/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** secundaria
- **Acceso:** Abierto (columnas descargables sin suscripción)
- **Ámbitos:** Columnas de investigación aplicada de economistas académicos; consorcio de portales asociados (p. ej., Nada es Gratis, RF-0416)
- **Motivo de inclusión y uso:** Síntesis accesibles de investigación reciente con enlace al trabajo de origen. AC-MAC, AC-MP. Uso en el Bloque A Forex: Columnas breves de investigadores sobre divisas, dólar dominante y flujos de capital. DOC-A (AG-14) y los Analistas de segmento como síntesis accesible.
- **Sesgos y cautelas:** Columnas sin revisión por pares completa.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Nada es Gratis blog economía Fedea»; WebFetch: sí, columna en cepr.org/voxeu)
- **Origen:** Reutilizada de F9 V3.2 (TF-13) en el Bloque A Forex V1.0 (2026-11-02).

#### FXF-0284 · Q 77 (B) — Clasificación de regímenes cambiarios de Ilzetzki, Reinhart y Rogoff (datos)

- **Canal oficial (URL raíz):** https://carmenreinhart.com/exchange-rate/ (publicación original: https://rogoff.scholars.harvard.edu/publications/modern-history-exchange-rate-arrangements-reinterpretation)
- **Emisor:** Ethan Ilzetzki, Carmen M. Reinhart y Kenneth S. Rogoff
- **Documentación y notas:** Clasificación de facto de regímenes cambiarios, divisa ancla e índice de mercado unificado (controles de capital), anual y mensual, de enero de 1946 a diciembre de 2016; ficheros anuales en Excel (los enlaces mensuales no funcionaban en la consulta). Acompaña a los NBER WP 23134 («Exchange Rate Arrangements Entering the 21st Century: Which Anchor Will Hold?») y 23135 (cronologías por país).
- **Temática:** TFX-10 Repositorios académicos, think tanks y blogs especializados en divisas (principal) · secundarias: TFX-03
- **Calidad Q:** 77 (B) — Primariedad 17/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 3/10 · Acceso 8/10
- **Tipología:** primaria (base de datos académica)
- **Acceso:** Abierto
- **Ámbitos:** Regímenes cambiarios de facto, anclas, mercados paralelos
- **Motivo de inclusión y uso:** Clasificación de facto de referencia para separar regímenes declarados y reales, útil para divisas con tipo fijo o deslizante. Uso: AS-EMLA (ARS), AS-EMEA (divisas del Golfo, EGP, NGN) y AS-EMAS (HKD, CNY); DOC-A (AG-14).
- **Restricciones de uso:** Uso académico con cita.
- **Sesgos posibles:** Datos hasta 2016: no recoge cambios de régimen posteriores.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Actualización mensual anunciada pero no disponible.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Ilzetzki Reinhart Rogoff exchange rate arrangements classification data update Chinn-Ito financial openness index»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-10).

#### RF-0092 · Q 77 (B) — Peterson Institute for International Economics (PIIE)

- **Canal oficial (URL raíz):** https://www.piie.com/ (política de transparencia: https://www.piie.com/about/transparency-policy)
- **Emisor:** PIIE
- **Temática:** TFX-10 Repositorios académicos, think tanks y blogs especializados en divisas (principal) · secundarias: TFX-09
- **Calidad Q:** 77 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 14/15 · Independencia 8/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** secundaria
- **Acceso:** Abierto
- **Ámbitos:** Comercio, finanzas internacionales, política macroeconómica
- **Motivo de inclusión y uso:** Análisis aplicado de economía internacional. Uso en el Bloque A Forex: Think tank de economía internacional con trabajo sobre divisas, manipulación cambiaria y desequilibrios. AS-ESTR (AG-08) y TR-BCM (AG-09).
- **Sesgos y cautelas:** Unos 150 financiadores (empresas, fundaciones, particulares, instituciones públicas); el mayor donante histórico es la Peter G. Peterson Foundation. Publica sus fuentes de financiación cada año desde 2013 y exige a los autores declarar vínculos financieros.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «brookings.edu piie.com bruegel.org think tank economic policy research»; WebFetch: sí)
- **Origen:** Reutilizada de F9 V3.2 (TF-14) en el Bloque A Forex V1.0 (2026-11-02).

#### RF-0093 · Q 76 (B) — Bruegel

- **Canal oficial (URL raíz):** https://www.bruegel.org/ (datos: https://www.bruegel.org/datasets)
- **Emisor:** Bruegel (fundado en 2005)
- **Temática:** TFX-10 Repositorios académicos, think tanks y blogs especializados en divisas (principal) · secundarias: —
- **Calidad Q:** 76 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 13/15 · Independencia 8/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** secundaria (con bases de datos propias)
- **Acceso:** Abierto
- **Ámbitos:** Política económica europea, energía, comercio; bases de datos: importaciones y demanda de gas, tipos de cambio efectivos reales de 178 países, base de datos de China, seguimiento del comercio global, agregados monetarios Divisia del área del euro, seguimiento del ETS
- **Motivo de inclusión y uso:** Think tank europeo de referencia con bases de datos propias. Uso en el Bloque A Forex: Think tank europeo; aloja la base de datos de tipos de cambio efectivos reales de Darvas (FXF-0282). AS-G10N y AS-EMEA para el euro y las divisas europeas.
- **Sesgos y cautelas:** Miembros: gobiernos de la UE, empresas internacionales e instituciones, que participan en fijar las prioridades de investigación.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «brookings.edu piie.com bruegel.org think tank economic policy research»; WebFetch: sí, páginas «About» y «Datasets»)
- **Origen:** Reutilizada de F9 V3.2 (TF-14) en el Bloque A Forex V1.0 (2026-11-02).

#### RF-0458 · Q 75 (B) — Follow the Money (Brad Setser, CFR)

- **Canal oficial (URL raíz):** https://www.cfr.org/blogs/follow-the-money
- **Emisor:** Brad W. Setser, Council on Foreign Relations
- **Temática:** TFX-10 Repositorios académicos, think tanks y blogs especializados en divisas (principal) · secundarias: TFX-04
- **Calidad Q:** 75 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 14/15 · Independencia 8/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** secundaria (análisis de datos oficiales de flujos)
- **Acceso:** Abierto
- **Ámbitos:** Flujos de capital transfronterizos, reservas, divisas (renminbi, Taiwán), datos TIC, desequilibrios comerciales, deuda soberana
- **Motivo de inclusión y uso:** Referencia en flujos y desequilibrios globales con datos oficiales. AC-FX, AC-MAC. Uso en el Bloque A Forex: Blog de Brad Setser (CFR) centrado en balanza de pagos, reservas, intervención cambiaria encubierta y flujos de Asia. TR-BCM (AG-09), AS-EMAS (AG-05) y AS-ESTR (AG-08).
- **Sesgos y cautelas:** Exfuncionario del Tesoro de EE. UU.; opinión sobre política cambiaria de China.
- **Criterios anti-manipulación:** Autor identificado, investigador sénior de un think tank; gráficos con fuente oficial.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Brad Setser Follow the Money blog Council on Foreign Relations»; WebFetch: sí (última entrada 11/10/2026))
- **Origen:** Reutilizada de F9 V3.2 (TF-12) en el Bloque A Forex V1.0 (2026-11-02).

#### FXF-0285 · Q 74 (B) — CEBRA — International Finance and Macroeconomics Program

- **Canal oficial (URL raíz):** https://cebra.org/programs/ifm/
- **Emisor:** Central Bank Research Association (CEBRA), Basilea
- **Documentación y notas:** Programa de investigación sobre mercados e instituciones financieras internacionales, flujos de capital y efectos de contagio de la política monetaria, que reúne a investigadores académicos y de bancos centrales. Directora: Galina Hale (UC Santa Cruz); comité asesor 2021–2026 con Laura Alfaro, Stijn Claessens (BPI), Kristin Forbes, Linda Goldberg (Fed de Nueva York), Pierre-Olivier Gourinchas, Takatoshi Ito, Philip Lane, Gian Maria Milesi-Ferretti y Neeltje van Horen (BoE). Convocatorias y reunión anual.
- **Temática:** TFX-10 Repositorios académicos, think tanks y blogs especializados en divisas (principal) · secundarias: TFX-04
- **Calidad Q:** 74 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 14/15 · Independencia 9/10 · Actualidad 8/10 · Acceso 7/10
- **Tipología:** secundaria cualificada (red de investigación)
- **Acceso:** Abierto
- **Ámbitos:** Finanzas internacionales e investigación de bancos centrales
- **Motivo de inclusión y uso:** Vía para detectar investigación de bancos centrales sobre flujos y contagio cambiario. Uso: DOC-A (AG-14) para la agenda de vigilancia; TR-BCM (AG-09).
- **Restricciones de uso:** Citar los trabajos en su fuente original.
- **Sesgos posibles:** Perspectiva de bancos centrales.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Renovación del comité asesor tras 2026.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «NBER International Finance and Macroeconomics program working papers IFM»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-10).

#### FXF-0286 · Q 72 (B) — Atlantic Council — Dollar Dominance Monitor

- **Canal oficial (URL raíz):** https://www.atlanticcouncil.org/programs/geoeconomics-center/dollar-dominance-monitor/ (presentación de 12/12/2023: https://www.atlanticcouncil.org/event/debating-the-dollar/ · resumen de resultados de 2024: https://stratnewsglobal.com/world-news/us-dollar-remains-worlds-primary-reserve-currency-atlantic-council-study/)
- **Emisor:** Atlantic Council, GeoEconomics Center
- **Documentación y notas:** Monitor con visualización de datos lanzado el 12/12/2023 que sigue la desdolarización de los BRICS, el papel internacional del dólar y las divisas competidoras (reservas, facturación comercial y transacciones). Resultados de junio de 2024: el dólar sigue dominante; la cuota del renminbi en reservas cayó al 2,3 % (desde 2,8 % en 2022); el sistema CIPS llegó a 142 participantes directos.
- **Temática:** TFX-10 Repositorios académicos, think tanks y blogs especializados en divisas (principal) · secundarias: TFX-09
- **Calidad Q:** 72 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 12/15 · Independencia 8/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** secundaria cualificada (recopilación y análisis de datos oficiales)
- **Acceso:** Abierto
- **Ámbitos:** Dólar dominante, desdolarización, BRICS, renminbi, sistemas de pago alternativos
- **Motivo de inclusión y uso:** Seguimiento periódico del sistema monetario internacional con datos reunidos en un solo lugar. Uso: AS-ESTR (AG-08: dólar amplio y cestas de refugio), AS-EMAS (CNY) y PROS (AG-10) para escenarios de largo plazo. Pieza de RF-0432.
- **Restricciones de uso:** Citar los datos en su fuente primaria (FMI COFER, SWIFT, BPI).
- **Sesgos posibles:** Think tank con perspectiva atlántica; financiación de donantes.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Atlantic Council Dollar Dominance Monitor GeoEconomics Center»; WebFetch: sí, página del acto de lanzamiento y artículo de StratNews; la página del monitor no se leyó)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-10).

#### RF-0409 · Q 72 (B) — Econbrowser (James Hamilton y Menzie Chinn)

- **Canal oficial (URL raíz):** https://econbrowser.com/
- **Emisor:** James D. Hamilton (UC San Diego) y Menzie Chinn (Universidad de Wisconsin)
- **Temática:** TFX-10 Repositorios académicos, think tanks y blogs especializados en divisas (principal) · secundarias: —
- **Calidad Q:** 72 (B) — Primariedad 11/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 14/15 · Independencia 9/10 · Actualidad 6/10 · Acceso 10/10
- **Tipología:** secundaria (bitácora académica)
- **Acceso:** Abierto
- **Ámbitos:** Macroeconomía, petróleo y energía, política monetaria y fiscal, previsiones
- **Motivo de inclusión y uso:** Análisis académico aplicado de coyuntura por economistas de referencia (p. ej., Hamilton sobre shocks petroleros). AC-MAC y AC-MP. Uso en el Bloque A Forex: Blog de Menzie Chinn (coautor del índice Chinn-Ito, FXF-0283) y James Hamilton con entradas frecuentes sobre tipos de cambio y paridades. DOC-A (AG-14) y AS-ESTR (AG-08).
- **Sesgos y cautelas:** Opiniones de autor; la actividad reciente no se comprobó en la página leída (entrada de 2013), aunque figura en el listado de blogs de 2026.
- **Criterios anti-manipulación:** Autores académicos identificados, con publicaciones revisadas por pares; entradas con datos y referencias.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «economics blogs list Calculated Risk Marginal Revolution Econbrowser»; WebFetch: sí)
- **Origen:** Reutilizada de F9 V3.2 (TF-12) en el Bloque A Forex V1.0 (2026-11-02).

#### RF-0428 · Q 72 (B) — Council on Foreign Relations (CFR)

- **Canal oficial (URL raíz):** https://www.cfr.org/
- **Emisor:** Council on Foreign Relations (fundado en 1921)
- **Temática:** TFX-10 Repositorios académicos, think tanks y blogs especializados en divisas (principal) · secundarias: TFX-09
- **Calidad Q:** 72 (B) — Primariedad 13/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 14/15 · Independencia 7/10 · Actualidad 8/10 · Acceso 9/10
- **Tipología:** secundaria
- **Acceso:** Abierto (Foreign Affairs con muro parcial)
- **Ámbitos:** Política exterior, geoeconomía, informes de Independent Task Forces; revista Foreign Affairs
- **Motivo de inclusión y uso:** Análisis de política exterior de EE. UU. y riesgos geopolíticos. Uso en el Bloque A Forex: Think tank estadounidense de política exterior; aloja el blog Follow the Money de Brad Setser (RF-0458) y trackers geoeconómicos. Capa transversal de geopolítica y sanciones.
- **Sesgos y cautelas:** Financiación de fundaciones y grandes donantes (críticas por una donación de 12 M USD en 2019).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Wikipedia list of think tanks»; WebFetch: sí, listado y artículo de Wikipedia; URL oficial confirmada en la ficha de Wikipedia leída con WebFetch a partir del listado devuelto por la búsqueda (lectura lateral); la web oficial no se cargó)
- **Origen:** Reutilizada de F9 V3.2 (TF-14) en el Bloque A Forex V1.0 (2026-11-02).

#### FXF-0287 · Q 70 (B) — Jeffrey Frankel (Harvard Kennedy School) — página personal, artículos de opinión y blog sobre divisas

- **Canal oficial (URL raíz):** https://frankel.scholars.harvard.edu/ (programa IFM: https://frankel.scholars.harvard.edu/program-international-finance-and-macroeconomics · aspectos destacados: https://frankel.scholars.harvard.edu/highlights-research)
- **Emisor:** Jeffrey A. Frankel (Harvard Kennedy School)
- **Documentación y notas:** Biografía, publicaciones, materiales docentes de macroeconomía internacional y sección de artículos de opinión ordenada por temas, entre ellos «Emerging Markets and Currencies», además de política monetaria, materias primas y China; enlaces a su blog en el Belfer Center y a VoxEU. Frankel dirigió el programa IFM del NBER de 1992 a 2017.
- **Temática:** TFX-10 Repositorios académicos, think tanks y blogs especializados en divisas (principal) · secundarias: —
- **Calidad Q:** 70 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 15/15 · Independencia 8/10 · Actualidad 6/10 · Acceso 7/10
- **Tipología:** secundaria cualificada (opinión de experto)
- **Acceso:** Abierto
- **Ámbitos:** Regímenes cambiarios, divisas emergentes, divisas de materias primas, dólar
- **Motivo de inclusión y uso:** Opinión de uno de los principales especialistas en regímenes cambiarios y previsión de tipos de cambio. Uso: DOC-A (AG-14), AS-ESTR (AG-08) y AS-EMLA (AG-06); opinión, nunca prueba de hechos.
- **Restricciones de uso:** Citar la pieza concreta y su fecha.
- **Sesgos posibles:** Opiniones personales; algunas piezas antiguas.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «NBER International Finance and Macroeconomics program working papers IFM»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-10).

#### RF-0432 · Q 66 (B) — Atlantic Council — GeoEconomics Center

- **Canal oficial (URL raíz):** https://www.atlanticcouncil.org/
- **Emisor:** Atlantic Council (fundado en 1961)
- **Temática:** TFX-10 Repositorios académicos, think tanks y blogs especializados en divisas (principal) · secundarias: TFX-09
- **Calidad Q:** 66 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 12/15 · Independencia 5/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** secundaria (con monitores propios)
- **Acceso:** Abierto
- **Ámbitos:** Geoeconomía: futuro del dinero (monedas digitales), sanciones, economía de China, sistema de Bretton Woods
- **Motivo de inclusión y uso:** Seguimiento de sanciones y de monedas digitales de banco central. Uso en el Bloque A Forex: Centro geoeconómico que mantiene el Dollar Dominance Monitor (FXF-0286) y trackers de sanciones. AS-ESTR (AG-08) y TR-BCM (AG-09) para el papel internacional del dólar.
- **Sesgos y cautelas:** Mayor financiación de gobiernos extranjeros entre los think tanks de EE. UU. (2019-2023, Quincy Institute); controversias de donantes.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Wikipedia list of think tanks»; WebFetch: sí, listado y artículo de Wikipedia; URL oficial confirmada en la ficha de Wikipedia leída con WebFetch a partir del listado devuelto por la búsqueda (lectura lateral); la web oficial no se cargó)
- **Origen:** Reutilizada de F9 V3.2 (TF-14) en el Bloque A Forex V1.0 (2026-11-02).

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
| V1.0 | 02/11/2026 | Emisión inicial del archivo específico de divisas del Bloque A Forex: 214 fichas (reutilizadas del Bloque A general V3.2 con su ID original, y nuevas verificadas por búsqueda web con prefijo FX); 0 bajas; orden por temática y Q; índice con recuento de verificadas. |

