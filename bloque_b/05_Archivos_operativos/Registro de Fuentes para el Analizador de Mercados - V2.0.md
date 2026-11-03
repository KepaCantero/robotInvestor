# Archivo operativo F9 — Registro de Fuentes para el Analizador de Mercados

**Bloque B · Robot Investor · Versión óptima V2.0 · 02/11/2026** · Subordinado al Documento 0 del Bloque B V2.0.

**Versión del archivo:** V2.0 (02/11/2026), alineada con el Documento 0 del Bloque B V2.0 · **Código:** F9 · **Propietario:** AG-B20 Buscador de Fuentes Avanzadas (BFA)

## Cómo usar este archivo

**Propósito.** Archivo del Bloque B (taxonomía TFB del Anexo D del Documento 0 del Bloque B); incluye referencias reutilizadas del Bloque A (conservan su ID) y referencias nuevas (prefijo MBF-).  Registro de fuentes de opinión, actualidad, datos de mercado, posicionamiento, grandes inversores, regulación y redes con filtro de calidad (Documento 0, 5.1 y 13.1). No contiene literatura académica de dominio (F7) ni métodos de cálculo (F8).

**Propietario y acceso.** Escribe solo AG-B20 (BFA). Leen: agentes del plano P2, AG-B18, Orquestador, Auditor y Evaluador (este último mide el historial de exactitud de cada fuente). Cualquier otro acceso es una incidencia (Documento 0, 5.2).

**Reglas de uso.**

1. **Lectura.** Lea primero «Novedades»; después el índice de temáticas; dentro de la temática, las fichas aparecen **ordenadas por Q descendente** (a igualdad, la más reciente primero). Cite siempre el ID de la ficha. Para corroboración (PA1) solo cuentan fichas de nivel A o B con `Estado del enlace` distinto de `ROTO`; una ficha `PENDIENTE_VERIFICACION_ALTA` no sustenta evidencia hasta que su propietario la confirme.
2. **Calidad.** Q (0–100) con la rúbrica de fuentes de opinión y actualidad (13.3): Primariedad 20 · Historial de exactitud medido por el Evaluador 20 (neutro 10 mientras no haya pronósticos resueltos) · Transparencia de método y conflictos 15 · Autoridad 15 · Independencia 10 · Actualidad 10 · Accesibilidad 10. Niveles: A (Q ≥ 80), B (65–79), C (50–64), D (< 50: candidata a baja salvo que sea la única fuente de un dato necesario, declarado). En las semillas la Q es provisional hasta la verificación de alta.
3. **Estados del enlace** (HT-02, barrido semanal del domingo): `OK`, `REDIRIGIDO`, `ROTO` (4xx/5xx en dos intentos separados 24 h), `MURO_PAGO`, `CONTENIDO_CAMBIADO` (similitud < 0,8 frente a la copia archivada) y `PENDIENTE_BARRIDO` (estado inicial de esta versión: ningún enlace se ha comprobado aún con HT-02). `Última verificación` recoge la última comprobación documentada, no una del barrido.
4. **Acciones** (potestad plena del propietario, R25): `REPARAR` (DOI, nueva URL oficial o copia archivada; obligatoria cuando la ficha lleva «Alerta»); `DEGRADAR` (bajar Q o nivel, con motivo); `BORRAR` cuando haya enlace roto sin alternativa tras dos barridos, contenido retirado o retractado, falsedad o manipulación demostrada, redundancia total con una ficha de mayor Q, o Q < 50 sin uso en 180 días. Cada borrado añade una línea al «Registro de bajas»; si la ficha sustentaba EVD de F2 se avisa al Curador (CT-B-15, tipo `fuente_retirada`).
5. **Ciclo.** BFA alimenta el registro por su agenda de vigilancia y por las peticiones de búsqueda (CT-B-11); antes de buscar aplica el Fondo metodológico (R25), en especial los criterios de credibilidad (lectura lateral). Mensualmente el propietario informa al Orquestador de altas, reparaciones, bajas, salud de enlaces y lagunas (CT-B-24). Los IDs son inmutables y no se reutilizan; en el «Registro de bajas», «REF-id» es el ID propio de la ficha.

**Reglas propias de F9.** (a) Una fuente de opinión nunca prueba un hecho: los hechos se citan en su fuente primaria. (b) Las copias sindicadas enlazan a su raíz y no cuentan como fuentes independientes. (c) Las fuentes de acceso restringido solo se usan por sus contenidos públicos citables; las credenciales viven en HT-01, nunca en este archivo. (d) Las «piezas» (series, informes o artículos concretos) se registran bajo su fuente y heredan su temática y calidad salvo anotación. (e) Las semillas (`PENDIENTE_VERIFICACION_ALTA`) no sustentan evidencia hasta su confirmación.

## Índice de temáticas (Anexo D, TFB-)

| Código | Temática | Referencias | Verificadas | Pendientes de verificación | A | B | C | D | Q medio |
|---|---|---|---|---|---|---|---|---|---|
| TFB-01 | Estadísticas oficiales y organismos internacionales | 27 | 27 | 0 | 24 | 3 | 0 | 0 | 85,3 |
| TFB-02 | Bancos centrales y datos macro | 21 | 21 | 0 | 20 | 1 | 0 | 0 | 85,8 |
| TFB-03 | Reguladores, registros y documentación corporativa | 25 | 25 | 0 | 21 | 4 | 0 | 0 | 83,2 |
| TFB-04 | Asociaciones sectoriales y datos de industria | 23 | 23 | 0 | 3 | 20 | 0 | 0 | 76,0 |
| TFB-05 | Comercio internacional y cadenas de suministro | 21 | 21 | 0 | 16 | 5 | 0 | 0 | 83,2 |
| TFB-06 | Datos de mercado gratuitos | 25 | 25 | 0 | 13 | 10 | 2 | 0 | 76,7 |
| TFB-07 | Fundamentales de empresas gratuitos | 24 | 24 | 0 | 7 | 3 | 14 | 0 | 68,0 |
| TFB-08 | Fondos, ETF e índices: datos y documentación | 22 | 22 | 0 | 12 | 10 | 0 | 0 | 77,2 |
| TFB-09 | Patentes, innovación y tecnología | 26 | 26 | 0 | 20 | 5 | 1 | 0 | 82,3 |
| TFB-10 | Prensa económica y especializada sectorial | 23 | 23 | 0 | 0 | 16 | 7 | 0 | 66,8 |
| TFB-11 | Análisis de bancos, gestoras, consultoras y think tanks | 21 | 21 | 0 | 1 | 19 | 1 | 0 | 71,0 |
| TFB-12 | Materias primas y energía | 22 | 22 | 0 | 17 | 5 | 0 | 0 | 81,5 |
| TFB-13 | Inmobiliario e infraestructuras | 22 | 22 | 0 | 11 | 11 | 0 | 0 | 79,6 |
| TFB-14 | Cripto: datos en cadena | 24 | 24 | 0 | 4 | 18 | 2 | 0 | 71,8 |
| TFB-15 | Posicionamiento, flujos y sentimiento | 23 | 23 | 0 | 13 | 9 | 1 | 0 | 77,5 |
| TFB-16 | Contratación pública, ayudas y política industrial | 27 | 27 | 0 | 20 | 7 | 0 | 0 | 80,7 |
| TFB-17 | Sostenibilidad y clima: datos | 20 | 20 | 0 | 7 | 12 | 1 | 0 | 75,5 |
| TFB-18 | Repositorios académicos y de investigación abierta | 23 | 23 | 0 | 9 | 14 | 0 | 0 | 78,4 |
| TFB-19 | Ecosistema emprendedor: startups, financiación, salidas a bolsa y escisiones (datos) | 24 | 24 | 0 | 7 | 13 | 4 | 0 | 73,2 |
| **Total** | — | **443** | **443** | 0 | 225 | 185 | 33 | 0 | 77,6 |

«Verificadas»: enlace en estado OK, REDIRIGIDO, MURO_PAGO o VERIFICADO_BUSQUEDA (existencia y datos confirmados por búsqueda web el 02/11/2026), o verificación documental completa en una carga anterior (25–26/10/2026), pendiente solo del barrido automático HT-02. «Pendientes»: semillas aún en PENDIENTE_VERIFICACION_ALTA o fichas con alerta sin resolver.

## Novedades

- 02/11/2026: emisión V2.0 del archivo (primera con fichas verificadas).

## TFB-01 Estadísticas oficiales y organismos internacionales

#### MBF-0001 · Q 89 (A) — INE — Instituto Nacional de Estadística (España)

- **Canal oficial (URL raíz):** https://www.ine.es/en/index.htm
- **Emisor:** Instituto Nacional de Estadística (España)
- **Documentación y notas:** Base de datos INEbase (cuentas nacionales, índices de producción industrial, cifra de negocios, Estadística Estructural de Empresas, comercio minorista, turismo, precios) con calendario de publicación y API JSON. Confirmada vía Índice UK Data Service «National statistics institutes» (https://ukdataservice.ac.uk/help/other-data-providers/international-data/national-statistics-institutes/).
- **Temática:** TFB-01 Estadísticas oficiales y organismos internacionales (principal) · secundarias: TFB-02
- **Calidad Q:** 89 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto (web y API gratuitas, sin clave)
- **Ámbitos:** España: PIB, IPC, producción industrial, índices de cifra de negocios por sector (CNAE), estructura empresarial, turismo, demografía
- **Motivo de inclusión y uso:** Fuente primaria oficial del mercado geográfico doméstico; indispensable para dimensionar sectores en España.
- **Restricciones de uso:** Uso libre con cita de la fuente, tabla y fecha.
- **Sesgos y cautelas:** Revisiones de datos y cambios de base; calendarios propios.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B04 y AG-B05: tamaño y evolución de sectores en España (cifra de negocios, producción, ocupados por CNAE); AG-B08: ciclo doméstico; Motor AG-B16: series para MC-B01…MC-B10.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Wikipedia list of national and international statistical services»; WebFetch: sí, sobre la página índice de UK Data Service)
- **Origen:** Alta 2026-11-02 (F9 Bloque B V2.0, TFB-01).

#### MBF-0005 · Q 89 (A) — ONS — Office for National Statistics (Reino Unido)

- **Canal oficial (URL raíz):** https://www.ons.gov.uk/
- **Emisor:** Office for National Statistics
- **Documentación y notas:** PIB mensual por industria, producción, servicios, comercio, precios; datos de empresas (Annual Business Survey). Confirmada vía Índice UK Data Service «National statistics institutes» (https://ukdataservice.ac.uk/help/other-data-providers/international-data/national-statistics-institutes/).
- **Temática:** TFB-01 Estadísticas oficiales y organismos internacionales (principal) · secundarias: TFB-02
- **Calidad Q:** 89 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto (Open Government Licence)
- **Ámbitos:** Reino Unido: PIB mensual por industria, producción, servicios, comercio
- **Motivo de inclusión y uso:** Fuente primaria del Reino Unido con PIB mensual desglosado por industria.
- **Restricciones de uso:** Open Government Licence con cita.
- **Sesgos y cautelas:** Revisiones de datos y cambios de base; calendarios propios.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Revisiones metodológicas recientes en encuestas de empleo (vigilar notas de calidad).
- **Uso en el bloque:** AG-B04 y AG-B08: actividad mensual por industria en el Reino Unido; AG-B05: producción y servicios.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Wikipedia list of national and international statistical services»; WebFetch: sí, página índice)
- **Origen:** Alta 2026-11-02 (F9 Bloque B V2.0, TFB-01).

#### MBF-0006 · Q 89 (A) — U.S. Census Bureau (estadísticas económicas y de empresas)

- **Canal oficial (URL raíz):** https://www.census.gov/
- **Emisor:** U.S. Census Bureau (Department of Commerce)
- **Documentación y notas:** Economic Census quinquenal, encuestas anuales (AIES, MBF-0007), indicadores mensuales (ventas minoristas, pedidos de bienes duraderos, construcción, inventarios), comercio exterior (MBF-0039) y clasificación NAICS. Confirmada vía Índice UK Data Service «National statistics institutes» (https://ukdataservice.ac.uk/help/other-data-providers/international-data/national-statistics-institutes/).
- **Temática:** TFB-01 Estadísticas oficiales y organismos internacionales (principal) · secundarias: TFB-05
- **Calidad Q:** 89 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto (API con clave gratuita)
- **Ámbitos:** EE. UU.: estructura empresarial por NAICS, ventas, pedidos, inventarios, construcción, comercio
- **Motivo de inclusión y uso:** Fuente primaria para dimensionar industrias de EE. UU. por código NAICS.
- **Restricciones de uso:** Dominio público con cita; la API exige clave gratuita.
- **Sesgos y cautelas:** Revisiones de datos y cambios de base; calendarios propios.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Consolidación de encuestas anuales en la AIES (ver MBF-0007).
- **Uso en el bloque:** AG-B04 y AG-B05: tamaño de mercado, número de establecimientos y concentración por NAICS; AG-B03: estructura de industrias; Motor AG-B16: series mensuales sectoriales.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Wikipedia list of national and international statistical services»; WebFetch: sí, página índice)
- **Origen:** Alta 2026-11-02 (F9 Bloque B V2.0, TFB-01).

#### MBF-0008 · Q 89 (A) — Statistics Canada

- **Canal oficial (URL raíz):** https://www.statcan.gc.ca/eng/start
- **Emisor:** Statistics Canada
- **Documentación y notas:** Tablas de datos (CANSIM) con API, PIB mensual por industria, manufacturas, comercio. Confirmada vía Índice UK Data Service «National statistics institutes» (https://ukdataservice.ac.uk/help/other-data-providers/international-data/national-statistics-institutes/).
- **Temática:** TFB-01 Estadísticas oficiales y organismos internacionales (principal) · secundarias: —
- **Calidad Q:** 89 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto (Open Government Licence – Canada)
- **Ámbitos:** Canadá: PIB por industria, recursos naturales, manufacturas, comercio
- **Motivo de inclusión y uso:** Fuente primaria para sectores de recursos, banca y energía canadienses.
- **Restricciones de uso:** Licencia abierta de Canadá con cita.
- **Sesgos y cautelas:** Revisiones de datos y cambios de base; calendarios propios.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B04 y AG-B05: sectores de recursos naturales y energía de Canadá; AG-B08: ciclo canadiense.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Wikipedia list of national and international statistical services»; WebFetch: sí, página índice)
- **Origen:** Alta 2026-11-02 (F9 Bloque B V2.0, TFB-01).

#### MBF-0014 · Q 89 (A) — ABS — Australian Bureau of Statistics

- **Canal oficial (URL raíz):** https://www.abs.gov.au/
- **Emisor:** Australian Bureau of Statistics
- **Documentación y notas:** Cuentas nacionales, minería, inversión privada (capex) por industria, comercio minorista; API de datos. Confirmada vía Índice UK Data Service «National statistics institutes» (https://ukdataservice.ac.uk/help/other-data-providers/international-data/national-statistics-institutes/).
- **Temática:** TFB-01 Estadísticas oficiales y organismos internacionales (principal) · secundarias: —
- **Calidad Q:** 89 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto (CC BY)
- **Ámbitos:** Australia: minería, inversión privada, consumo
- **Motivo de inclusión y uso:** Fuente primaria para sectores mineros y de recursos.
- **Restricciones de uso:** CC BY con cita.
- **Sesgos y cautelas:** Revisiones de datos y cambios de base; calendarios propios.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B05: capex minero y producción de recursos; AG-B04: consumo australiano.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Wikipedia list of national and international statistical services»; WebFetch: sí, página índice)
- **Origen:** Alta 2026-11-02 (F9 Bloque B V2.0, TFB-01).

#### MBF-0015 · Q 89 (A) — UNSD — Clasificaciones económicas (ISIC Rev.5, CPC 3.0, HS, SITC, BEC, COICOP) y tablas de correspondencia

- **Canal oficial (URL raíz):** https://unstats.un.org/unsd/classifications/Econ
- **Emisor:** División de Estadística de las Naciones Unidas (UNSD)
- **Documentación y notas:** ISIC Rev.5 «forthcoming UN publication» con manual, estructura CSV y notas explicativas; tabla de correspondencia ISIC Rev.4 → Rev.5 (17/01/2025); CPC 3.0 (notas de 30/06/2025); correspondencias HS 1992–2022, HS–SITC–BEC y CPC–ISIC.
- **Temática:** TFB-01 Estadísticas oficiales y organismos internacionales (principal) · secundarias: TFB-05
- **Calidad Q:** 89 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria (norma de clasificación)
- **Acceso:** Abierto
- **Ámbitos:** Clasificaciones de actividades (ISIC), productos (CPC, HS, SITC), usos (BEC, COICOP) y correspondencias
- **Motivo de inclusión y uso:** Base para delimitar sectores y subsectores y enlazar estadísticas de producción (ISIC/NACE/NAICS) con comercio (HS) y consumo (COICOP).
- **Restricciones de uso:** Uso libre con cita.
- **Sesgos y cautelas:** ISIC Rev.5 aún en edición: implantación nacional escalonada.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Transición ISIC Rev.4 → Rev.5 en curso.
- **Uso en el bloque:** AG-B02 y AG-B03: delimitación de sectores y subsectores; AG-B05: puente producto–industria para cadenas de valor; Motor AG-B16: mapeos de códigos entre bases.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ISIC Rev. 5 UN Statistics Division classification NACE Rev. 2.1 NAICS 2022 correspondence tables»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9 Bloque B V2.0, TFB-01).

#### MBF-0016 · Q 89 (A) — Eurostat — NACE Rev. 2.1 (clasificación estadística de actividades económicas de la UE)

- **Canal oficial (URL raíz):** https://en.wikipedia.org/wiki/Statistical_Classification_of_Economic_Activities_in_the_European_Community
- **Emisor:** Eurostat (Comisión Europea)
- **Documentación y notas:** Revisión de NACE alineada con ISIC Rev.5 y aplicada en la UE a partir de 2025; presentación técnica de Eurostat en el taller de la UNSD (unstats.un.org/unsd/classifications/Workshops/Santiago2025/Session3.3_NACE_Rev2.1.pdf). Confirmada vía índice Wikipedia (artículo NACE) y documentos de la UNSD devueltos por la búsqueda.
- **Temática:** TFB-01 Estadísticas oficiales y organismos internacionales (principal) · secundarias: —
- **Calidad Q:** 89 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria (norma de clasificación)
- **Acceso:** Abierto
- **Ámbitos:** Clasificación de actividades de la UE (base de SBS, PRODCOM, cuentas nacionales y CNAE-2025 en España)
- **Motivo de inclusión y uso:** Necesaria para mapear sectores europeos y gestionar la ruptura de series por el cambio NACE Rev.2 → Rev.2.1.
- **Restricciones de uso:** Uso libre con cita.
- **Sesgos y cautelas:** Ruptura de series en la transición; doble codificación temporal.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Transición a NACE Rev.2.1 desde 2025.
- **Uso en el bloque:** AG-B02 y AG-B03: perímetro de sectores europeos; Motor AG-B16: tablas de paso entre NACE Rev.2 y Rev.2.1.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «ISIC Rev. 5 UN Statistics Division classification NACE Rev. 2.1 NAICS 2022 correspondence tables»; WebFetch: no)
- **Origen:** Alta 2026-11-02 (F9 Bloque B V2.0, TFB-01).

#### RF-0022 · Q 89 (A) — U.S. Bureau of Labor Statistics (BLS)

- **Canal oficial (URL raíz):** https://www.bls.gov/ (sala de prensa y calendario: https://www.bls.gov/newsroom/home.htm)
- **Emisor:** U.S. Department of Labor
- **Temática:** TFB-01 Estadísticas oficiales y organismos internacionales (principal) · secundarias: TFB-02
- **Calidad Q:** 89 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** IPC, IPP, empleo (Employment Situation), JOLTS, salarios reales, productividad de EE. UU.
- **Motivo de inclusión y uso:** Publicador original de IPC y nóminas; su sala de prensa fija fecha y hora de cada publicación (p. ej., Employment Situation 6/11/2026 y CPI 10/11/2026, 8:30 ET). Uso: calendario de catalizadores y dato primario para inflación y mercado laboral.
- **Sesgos y cautelas:** Revisiones mensuales y anuales; cambios metodológicos documentados; calendario alterable por cierres administrativos (publica fechas revisadas).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Uso en el bloque:** AG-B08: inflación, empleo y salarios por industria; AG-B05: precios de producción (PPI) por sector como señal de poder de fijación de precios; AG-B09: márgenes sectoriales frente a costes laborales.
- **Origen:** Reutilizada con su ID de F9 V3.2 (Bloque A general); temática reasignada a TFB-01 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «U.S. Bureau of Labor Statistics official site CPI employment situation»; WebFetch: sí)

#### RF-0023 · Q 89 (A) — U.S. Bureau of Economic Analysis (BEA)

- **Canal oficial (URL raíz):** https://www.bea.gov/ (renta y ahorro: https://www.bea.gov/taxonomy/term/1071)
- **Emisor:** U.S. Department of Commerce
- **Temática:** TFB-01 Estadísticas oficiales y organismos internacionales (principal) · secundarias: TFB-02
- **Calidad Q:** 89 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** PIB, renta y gasto personal (PCE), tasa de ahorro, balanza de pagos, renta estatal de EE. UU.
- **Motivo de inclusión y uso:** Publicador original de las cuentas nacionales de EE. UU. y del deflactor PCE (objetivo de inflación de la Fed). Desde 2026 publica renta y gasto personal junto con las estimaciones del PIB. Uso: dato primario de crecimiento e inflación PCE.
- **Sesgos y cautelas:** Revisiones sustanciales del PIB entre estimaciones; calendario reprogramado en 2025–2026 (verificar fecha en el aviso de la BEA).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Uso en el bloque:** AG-B04 y AG-B08: PIB, consumo por categoría y valor añadido por industria de EE. UU.; AG-B05: tablas input-output para cadenas de valor; Motor AG-B16: cuentas por industria.
- **Origen:** Reutilizada con su ID de F9 V3.2 (Bloque A general); temática reasignada a TFB-01 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «U.S. Bureau of Economic Analysis GDP personal income outlays bea.gov»; WebFetch: sí)

#### MBF-0002 · Q 88 (A) — Destatis — Statistisches Bundesamt (Alemania)

- **Canal oficial (URL raíz):** https://www.destatis.de/EN/Home/_node.html
- **Emisor:** Oficina Federal de Estadística de Alemania
- **Documentación y notas:** Base GENESIS-Online, producción industrial, pedidos de manufacturas, comercio exterior, precios. Directorio de oficinas estadísticas europeas en el propio sitio (destatis.de/EN/Service/Address-Book/europe.html). Confirmada vía Índice UK Data Service «National statistics institutes» (https://ukdataservice.ac.uk/help/other-data-providers/international-data/national-statistics-institutes/).
- **Temática:** TFB-01 Estadísticas oficiales y organismos internacionales (principal) · secundarias: —
- **Calidad Q:** 88 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto (GENESIS con registro gratuito opcional para API)
- **Ámbitos:** Alemania: pedidos industriales, producción, comercio exterior, precios de producción
- **Motivo de inclusión y uso:** Primera economía industrial europea; pedidos y producción por rama son indicadores adelantados sectoriales.
- **Restricciones de uso:** Licencia de datos abiertos de Alemania con cita.
- **Sesgos y cautelas:** Revisiones de datos y cambios de base; calendarios propios.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B04 y AG-B05: pedidos y producción por rama (automóvil, química, maquinaria); AG-B08: ciclo industrial europeo.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Wikipedia list of national and international statistical services»; WebFetch: sí, página índice)
- **Origen:** Alta 2026-11-02 (F9 Bloque B V2.0, TFB-01).

#### MBF-0003 · Q 88 (A) — INSEE — Institut national de la statistique et des études économiques (Francia)

- **Canal oficial (URL raíz):** https://www.insee.fr/en/accueil
- **Emisor:** INSEE (Francia)
- **Documentación y notas:** Cuentas nacionales, encuestas de coyuntura empresarial por sector, producción industrial, precios; repertorio SIRENE de empresas. Confirmada vía Índice UK Data Service «National statistics institutes» (https://ukdataservice.ac.uk/help/other-data-providers/international-data/national-statistics-institutes/).
- **Temática:** TFB-01 Estadísticas oficiales y organismos internacionales (principal) · secundarias: —
- **Calidad Q:** 88 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Francia: coyuntura sectorial, producción, empresas (SIRENE), precios
- **Motivo de inclusión y uso:** Fuente primaria de Francia; las encuestas de coyuntura por sector son útiles como indicador adelantado.
- **Restricciones de uso:** Licence Ouverte con cita.
- **Sesgos y cautelas:** Revisiones de datos y cambios de base; calendarios propios.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B04 y AG-B08: coyuntura por sectores en Francia; AG-B12: identificación de empresas vía SIRENE.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Wikipedia list of national and international statistical services»; WebFetch: sí, página índice)
- **Origen:** Alta 2026-11-02 (F9 Bloque B V2.0, TFB-01).

#### RF-0021 · Q 88 (A) — Eurostat

- **Canal oficial (URL raíz):** https://ec.europa.eu/eurostat (guía del sitio: https://ec.europa.eu/eurostat/en/help/website-guide)
- **Emisor:** Comisión Europea — Oficina Estadística de la Unión Europea
- **Temática:** TFB-01 Estadísticas oficiales y organismos internacionales (principal) · secundarias: TFB-05
- **Calidad Q:** 88 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto (acceso gratuito a todas sus bases de datos)
- **Ámbitos:** IPCA (HICP), PIB, empleo, comercio, finanzas públicas de la UE; calendario de publicaciones y «euro indicators»
- **Motivo de inclusión y uso:** Estadística oficial armonizada de la UE con calendario de publicaciones y notas «euro indicators» de los principales indicadores mensuales y trimestrales. Uso: dato primario macro europeo y comparaciones entre países.
- **Sesgos y cautelas:** Datos agregados a partir de institutos nacionales; revisiones y desfases según país.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Uso en el bloque:** AG-B04 y AG-B05: dimensionado de mercados y producción industrial europea (PRODCOM, SBS, comercio Comext); AG-B08: ciclo por país y sector; Motor AG-B16: series armonizadas para MC-B01…MC-B10.
- **Origen:** Reutilizada con su ID de F9 V3.2 (Bloque A general); temática reasignada a TFB-01 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Eurostat official website European statistics database»; WebFetch: sí)

#### MBF-0004 · Q 87 (A) — Istat — Istituto Nazionale di Statistica (Italia)

- **Canal oficial (URL raíz):** https://www.istat.it/en/
- **Emisor:** Istat (Italia)
- **Documentación y notas:** Producción industrial, cifra de negocios, comercio exterior, estructura de empresas; base de datos I.Stat/IstatData. Confirmada vía Índice UK Data Service «National statistics institutes» (https://ukdataservice.ac.uk/help/other-data-providers/international-data/national-statistics-institutes/).
- **Temática:** TFB-01 Estadísticas oficiales y organismos internacionales (principal) · secundarias: —
- **Calidad Q:** 87 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Italia: industria, servicios, comercio exterior, empresas
- **Motivo de inclusión y uso:** Fuente primaria del tercer mercado de la zona del euro.
- **Restricciones de uso:** Licencia CC BY con cita.
- **Sesgos y cautelas:** Revisiones de datos y cambios de base; calendarios propios.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Migración de bases de datos (I.Stat → IstatData) a vigilar.
- **Uso en el bloque:** AG-B04 y AG-B05: sectores italianos (maquinaria, moda, lujo, alimentación); AG-B08: ciclo de Italia.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Wikipedia list of national and international statistical services»; WebFetch: sí, página índice)
- **Origen:** Alta 2026-11-02 (F9 Bloque B V2.0, TFB-01).

#### MBF-0007 · Q 87 (A) — U.S. Census Bureau — Annual Integrated Economic Survey (AIES) y serie histórica 1992–2024

- **Canal oficial (URL raíz):** https://www.census.gov/data/developers/data-sets/aiestimeseries.html
- **Emisor:** U.S. Census Bureau
- **Documentación y notas:** La AIES consolida siete encuestas anuales: Annual Capital Expenditures Survey, Annual Retail Trade Survey, Annual Survey of Manufactures (ASM), Annual Wholesale Trade Survey, Manufacturers' Unfilled Orders Survey, Report of Organization y Services Annual Survey. Serie histórica 1992–2024 por NAICS (ventas, nóminas, empleo, gastos, inventarios, inversión). Endpoint api.census.gov/data/timeseries/aies/historical. Página revisada el 09/09/2026.
- **Temática:** TFB-01 Estadísticas oficiales y organismos internacionales (principal) · secundarias: TFB-03
- **Calidad Q:** 87 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto; «todas las consultas a la API del Census requieren clave» (registro gratuito en api.census.gov/data/key_signup.html)
- **Ámbitos:** EE. UU.: ventas, inversión (capex), nóminas, inventarios por industria NAICS
- **Motivo de inclusión y uso:** Sustituye a la ASM y a otras encuestas anuales: es la fuente oficial de cuentas anuales por industria para dimensionado y márgenes.
- **Restricciones de uso:** Dominio público; clave API gratuita obligatoria.
- **Sesgos y cautelas:** Ruptura de series por la consolidación; empalme con datos heredados documentado por el Census.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Consolidación de siete encuestas anuales en la AIES.
- **Uso en el bloque:** AG-B04: dimensionado de industrias (ventas por NAICS); AG-B05: capex e inventarios por industria; AG-B09: márgenes agregados; Motor AG-B16 (MC-B01…MC-B10): series anuales.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Census Bureau Annual Integrated Economic Survey replaces Annual Survey of Manufactures NAICS 2022»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9 Bloque B V2.0, TFB-01).

#### RF-0005 · Q 87 (A) — World Bank Open Data (Banco Mundial)

- **Canal oficial:** https://data.worldbank.org (indicador cambiario de referencia: https://data.worldbank.org/indicator/PA.NUS.FCRF?lang=en-gb · API: https://api.worldbank.org/v2/country/CMR/indicator/PA.NUS.FCRF)
- **Documentación y notas:** Indicador PA.NUS.FCRF «Official exchange rate (LCU per US$, period average)», con fuente declarada en International Financial Statistics del FMI; licencia CC BY 4.0; último año mostrado: 2025. Útil también para PIB (NY.GDP.MKTP.CD), factores de conversión PPA del ICP e indicadores de deuda externa.
- **Temática:** TFB-01 Estadísticas oficiales y organismos internacionales (principal) · secundarias: TFB-05
- **Calidad Q:** 87 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 8/10 · Acceso 10/10
- **Nivel de fiabilidad en V2.4:** A
- **Tipología:** primaria
- **Motivo de inclusión:** Series anuales comparables de tipos de cambio oficiales medios, PIB y PPA para casi todos los países, incluidas divisas frontera y exóticas sin cobertura de mercado. Uso en el Bloque A Forex: MOTOR (AG-13) para normalizar magnitudes a dólares y calcular desviaciones frente a PPA; AS-EMLA y AS-EMEA para contexto de largo plazo de divisas emergentes y frontera.
- **Ámbitos:** Tipos de cambio oficiales anuales; PIB; PPA; indicadores de desarrollo por país
- **Restricciones de uso:** CC BY 4.0 en general; citar indicador (código), país y año
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Sesgos posibles:** Media anual del tipo oficial: no refleja tipos paralelos ni regímenes múltiples (contrastar con AREAER, FXF-0052); desfase de publicación y revisiones retrospectivas
- **Cambios de propiedad o de metodología:** Sin cambios conocidos; las series se revisan con las actualizaciones del World Development Indicators
- **Uso en el bloque:** AG-B04 y AG-B08: indicadores de desarrollo (WDI) para dimensionar mercados geográficos y emergentes; AG-B07: gobernanza y entorno de negocio por país.
- **Origen:** Reutilizada con su ID de F9 Forex V1.0; temática reasignada a TFB-01 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «World Bank Open Data official exchange rate LCU per US$ period average PA.NUS.FCRF»; WebFetch: sí, página del indicador (variante ?lang=en-gb; la URL sin parámetro dio error de servidor puntual))

#### RF-0006 · Q 87 (A) — OECD Data Explorer (Organización para la Cooperación y el Desarrollo Económicos)

- **Canal oficial (URL raíz):** https://data-explorer.oecd.org/
- **Emisor:** OCDE
- **Documentación y notas:** Portal vigente de datos de la OCDE (sustituye a data.oecd.org), con API SDMX y documentación de descarga; incluye comercio de bienes y servicios, política comercial, comercio digital y cadenas globales de valor, además de cuentas nacionales, productividad e indicadores sectoriales. Confirmado como portal vigente en el índice Harvard Library Research Guide «Trade» (https://guides.library.harvard.edu/trade).
- **Temática:** TFB-01 Estadísticas oficiales y organismos internacionales (principal) · secundarias: TFB-05
- **Calidad Q:** 87 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 9/10
- **Nivel de fiabilidad en V2.4:** A
- **Tipología:** primaria
- **Motivo de inclusión:** Indicadores comparables de países OCDE (crecimiento, empleo, precios, comercio, productividad por industria) con notas metodológicas editoriales
- **Ámbitos:** Países OCDE; empleo; comercio; industria; cadenas globales de valor; política económica comparada
- **Restricciones de uso:** Condiciones de uso del portal; citar conjunto de datos, indicador, país y fecha de extracción
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Sesgos posibles:** Cobertura centrada en países OCDE
- **Cambios de propiedad o de metodología:** Migración de portal (data.oecd.org → data-explorer.oecd.org) ya efectuada; las URL antiguas redirigen
- **Uso en el bloque:** AG-B04 y AG-B08: comparaciones internacionales de mercados y productividad por industria; AG-B05: cadenas globales de valor (véase MBF-0052, TiVA/ICIO); Motor AG-B16: descargas SDMX.
- **Origen:** Semilla de F9 V3.2 (Bloque A general) revalidada con su ID; temática reasignada a TFB-01 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «UN Comtrade database WITS World Integrated Trade Solution free trade data tariff»; WebFetch: sí, sobre la página índice de Harvard Library)

#### MBF-0009 · Q 86 (A) — Statistics Bureau of Japan

- **Canal oficial (URL raíz):** http://www.stat.go.jp/english/index.html
- **Emisor:** Statistics Bureau, Ministry of Internal Affairs and Communications (Japón)
- **Documentación y notas:** Censo económico, encuestas de servicios, IPC y estadísticas de empresas; portal estadístico del Gobierno (e-Stat) no figura en el índice. Confirmada vía Índice UK Data Service «National statistics institutes» (https://ukdataservice.ac.uk/help/other-data-providers/international-data/national-statistics-institutes/).
- **Temática:** TFB-01 Estadísticas oficiales y organismos internacionales (principal) · secundarias: —
- **Calidad Q:** 86 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (parte del contenido solo en japonés)
- **Ámbitos:** Japón: estructura económica, servicios, precios
- **Motivo de inclusión y uso:** Fuente primaria de Japón para dimensionado sectorial.
- **Restricciones de uso:** Cita de la fuente.
- **Sesgos y cautelas:** Parte del detalle solo en japonés; revisiones.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B04: dimensionado de mercados en Japón; AG-B08: precios y consumo.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Wikipedia list of national and international statistical services»; WebFetch: sí, página índice)
- **Origen:** Alta 2026-11-02 (F9 Bloque B V2.0, TFB-01).

#### MBF-0012 · Q 85 (A) — IBGE — Instituto Brasileiro de Geografia e Estatística

- **Canal oficial (URL raíz):** https://www.ibge.gov.br/
- **Emisor:** IBGE (Brasil)
- **Documentación y notas:** Cuentas nacionales, producción industrial (PIM), comercio y servicios mensuales; base SIDRA. Confirmada vía Índice UK Data Service «National statistics institutes» (https://ukdataservice.ac.uk/help/other-data-providers/international-data/national-statistics-institutes/).
- **Temática:** TFB-01 Estadísticas oficiales y organismos internacionales (principal) · secundarias: —
- **Calidad Q:** 85 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 14/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Brasil: industria, comercio, servicios, agricultura
- **Motivo de inclusión y uso:** Fuente primaria de la mayor economía de América Latina.
- **Restricciones de uso:** Cita de la fuente.
- **Sesgos y cautelas:** Revisiones de datos y cambios de base; calendarios propios.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B04: mercados geográficos latinoamericanos; AG-B05: producción industrial y agrícola de Brasil.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Wikipedia list of national and international statistical services»; WebFetch: sí, página índice)
- **Origen:** Alta 2026-11-02 (F9 Bloque B V2.0, TFB-01).

#### MBF-0013 · Q 85 (A) — Statistics Korea (KOSTAT)

- **Canal oficial (URL raíz):** https://kostat.go.kr/anse/
- **Emisor:** Statistics Korea
- **Documentación y notas:** Producción industrial, utilización de capacidad, inventarios (incluidos semiconductores), servicios. Confirmada vía Índice UK Data Service «National statistics institutes» (https://ukdataservice.ac.uk/help/other-data-providers/international-data/national-statistics-institutes/).
- **Temática:** TFB-01 Estadísticas oficiales y organismos internacionales (principal) · secundarias: TFB-05
- **Calidad Q:** 85 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (portal KOSIS)
- **Ámbitos:** Corea del Sur: producción, inventarios y envíos por industria
- **Motivo de inclusión y uso:** Fuente primaria de un mercado clave en semiconductores, baterías y astilleros.
- **Restricciones de uso:** Cita de la fuente.
- **Sesgos y cautelas:** Revisiones de datos y cambios de base; calendarios propios.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B05 y AG-B06: producción e inventarios de semiconductores y electrónica; AG-B08: ciclo tecnológico asiático.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Wikipedia list of national and international statistical services»; WebFetch: sí, página índice)
- **Origen:** Alta 2026-11-02 (F9 Bloque B V2.0, TFB-01).

#### RF-0007 · Q 85 (A) — IMF Data (Fondo Monetario Internacional)

- **Canal oficial:** data.imf.org
- **Documentación y notas:** Nota de verificación: el punto de acceso SDMX histórico (dataservices.imf.org) quedó retirado en 2025; el acceso vigente es el portal data.imf.org, comprobado vivo el 02/11/2026 (páginas de COFER e IRFCL).
- **Temática:** TFB-01 Estadísticas oficiales y organismos internacionales (principal) · secundarias: TFB-02
- **Calidad Q:** 85 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 7/10
- **Nivel de fiabilidad en V2.4:** A
- **Tipología:** primaria
- **Motivo de inclusión:** Portal de datos del FMI que aloja las bases cambiarias y externas de referencia: COFER (composición por divisas de las reservas), IRFCL (reservas y liquidez en divisas), balanza de pagos y posición de inversión internacional, y estadísticas financieras internacionales (tipos de cambio oficiales). Uso: TR-BCM (AG-09) y Analistas de segmento para datos externos comparables; MOTOR (AG-13) para series de valoración.
- **Ámbitos:** Macroeconomía global; balanza de pagos; reservas; estabilidad financiera
- **Restricciones de uso:** Condiciones del portal del FMI; citar base, serie y edición (los datos de proyección cambian por edición)
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Sesgos posibles:** Las proyecciones WEO son estimaciones del FMI, no hechos: tratarlas como previsión
- **Cambios de propiedad o de metodología:** Ediciones WEO semestrales: anotar siempre la edición usada
- **Uso en el bloque:** AG-B08: series macro y financieras por país (IFS y otras bases del FMI); AG-B07: riesgo país; Motor AG-B16: insumos de escenarios macro.
- **Origen:** Reutilizada con su ID de F9 Forex V1.0; temática reasignada a TFB-01 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «IMF COFER currency composition of official foreign exchange reserves 2026» → data.imf.org; WebFetch: sí, https://data.imf.org/cofer y https://data.imf.org/en/Datasets/IRFCL)

#### FXF-0415 · Q 83 (A) — Banco Mundial — International Debt Statistics (IDS)

- **Canal oficial (URL raíz):** https://datacatalog.worldbank.org/search/dataset/0038015/international-debt-statistics (productos del International Debt Report: https://www.worldbank.org/en/programs/debt-statistics/idr/products · guía metodológica IDS 2025: https://thedocs.worldbank.org/en/doc/6e72b0ded996306fa01f5db7a0c38b19-0050052021/related/IDS-2025-User-Guide-and-Methodology.pdf)
- **Emisor:** Banco Mundial (Debtor Reporting System, DRS, creado en 1951)
- **Documentación y notas:** Deuda externa de países de renta baja y media, anual, 1970–2032 (incluye proyecciones de servicio de la deuda); sucesora de Global Development Finance y World Debt Tables; licencia CC BY 4.0; metadatos actualizados el 14/05/2026 (versión 14).
- **Temática:** TFB-01 Estadísticas oficiales y organismos internacionales (principal) · secundarias: TFB-02
- **Calidad Q:** 83 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 5/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Deuda externa por acreedor, moneda y plazo; calendario de amortizaciones; flujos netos de deuda a emergentes y frontera
- **Motivo de inclusión y uso:** Base oficial de la deuda externa y su servicio, clave para el riesgo de crisis cambiaria en emergentes. Uso: AS-EMLA y AS-EMEA para necesidades de financiación exterior y concentración de vencimientos; CONTRA (AG-11) para escenarios de crisis.
- **Restricciones de uso:** CC BY 4.0; citar indicador, país y edición.
- **Sesgos posibles:** Anual con más de un año de desfase; depende de la declaración de los deudores; no cubre economías avanzadas.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B07 y AG-B08: deuda externa de países emergentes para el análisis de mercados geográficos y de segmentos de bonos soberanos y corporativos EM.
- **Origen:** Reutilizada con su ID de F9 Forex V1.0; temática reasignada a TFB-01 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «World Bank International Debt Statistics IDS 2025 external debt low middle income countries»; WebFetch: sí, ficha del catálogo de datos)

#### RF-0024 · Q 83 (A) — FMI — World Economic Outlook y blog del FMI

- **Canal oficial (URL raíz):** https://www.imf.org/en/publications/weo (edición vigente: https://www.imf.org/en/publications/weo/issues/2026/10/13/world-economic-outlook-october-2026)
- **Emisor:** Fondo Monetario Internacional
- **Temática:** TFB-01 Estadísticas oficiales y organismos internacionales (principal) · secundarias: TFB-02
- **Calidad Q:** 83 (A) — Primariedad 16/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria (previsiones propias del organismo)
- **Acceso:** Abierto
- **Ámbitos:** Previsiones macro mundiales y por país (abril y octubre, con actualizaciones en enero y julio); base de datos del WEO
- **Motivo de inclusión y uso:** Escenario central de referencia del sector oficial (WEO de octubre de 2026, «Resilience Under Strain, Urgent Choices»: crecimiento mundial 3,1 % en 2026 y 3,4 % en 2027). Uso: ancla de consenso oficial frente a la que medir escenarios propios.
- **Sesgos y cautelas:** Previsiones, no hechos; sesgo histórico hacia la continuidad; el blog del FMI expresa opiniones del personal.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Uso en el bloque:** AG-B08 y AG-B13: previsiones de crecimiento e inflación por país y región para escenarios de demanda; AG-B14: contraste de consensos.
- **Origen:** Reutilizada con su ID de F9 V3.2 (Bloque A general); temática reasignada a TFB-01 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «IMF World Economic Outlook October 2026»; WebFetch: sí)

#### FXF-0058 · Q 82 (A) — Banco Mundial — International Comparison Program (ICP) y fuentes de paridades de poder adquisitivo

- **Canal oficial (URL raíz):** https://www.worldbank.org/en/programs/icp/brief/Sources_of_PPPs
- **Emisor:** Banco Mundial (coordinador mundial del ICP bajo la Comisión de Estadística de la ONU)
- **Documentación y notas:** Nota que compara las fuentes de PPA: ICP (única que recopila precios nacionales; 44 categorías de gasto en los años de referencia), programa anual Eurostat-OCDE, WEO del FMI (extrapola las PPA del ICP con deflactores y publica previsiones), Penn World Table (Groningen y UC Davis; series desde 1950) y CIA World Factbook. En la fecha de la nota (09/2023) la última referencia publicada era 2017 y la de 2021 se esperaba para 2024.
- **Temática:** TFB-01 Estadísticas oficiales y organismos internacionales (principal) · secundarias: —
- **Calidad Q:** 82 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 4/10 · Acceso 10/10
- **Tipología:** primaria (organismo que coordina la estadística)
- **Acceso:** Abierto
- **Ámbitos:** Paridades de poder adquisitivo y niveles de precios comparados
- **Motivo de inclusión y uso:** Guía oficial para elegir la serie de PPA adecuada y no mezclar fuentes. Uso: MOTOR (AG-13, valoración PPA) y AS-ESTR (AG-08, estrategia de valor).
- **Restricciones de uso:** Licencia del Banco Mundial (por lo general CC BY 4.0).
- **Sesgos posibles:** Las PPA de referencia se revisan en cada ronda; la nota es de 2023 (comprobar la ronda vigente).
- **Historial de exactitud:** No aplicable.
- **Cambios de propiedad o de metodología:** Nueva ronda ICP 2021 posterior a la nota.
- **Uso en el bloque:** AG-B04: comparación de tamaños de mercado entre países en paridad de poder adquisitivo; Motor AG-B16: conversión PPA en dimensionado (TAM).
- **Origen:** Reutilizada con su ID de F9 Forex V1.0; temática reasignada a TFB-01 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «OECD purchasing power parities data World Bank International Comparison Program Penn World Table»; WebFetch: sí)

#### MBF-0017 · Q 81 (A) — UNIDO Statistics Data Portal (INDSTAT y valor añadido manufacturero)

- **Canal oficial (URL raíz):** https://stat.unido.org/
- **Emisor:** Organización de las Naciones Unidas para el Desarrollo Industrial (ONUDI/UNIDO)
- **Documentación y notas:** Bases INDSTAT (estadísticas industriales por rama ISIC: empleo, valor añadido, producción) y valor añadido manufacturero por país; descargas con límite de filas. Fichas de bibliotecas (Rutgers, EUI) la describen como «UNIDO Statistics Data Portal».
- **Temática:** TFB-01 Estadísticas oficiales y organismos internacionales (principal) · secundarias: TFB-04
- **Calidad Q:** 81 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 14/15 · Independencia 10/10 · Actualidad 7/10 · Acceso 8/10
- **Tipología:** primaria (compilación de oficinas nacionales)
- **Acceso:** Abierto (descargas desde el portal)
- **Ámbitos:** Industria manufacturera por país y rama ISIC
- **Motivo de inclusión y uso:** Comparación internacional de industrias manufactureras con definición homogénea.
- **Restricciones de uso:** Cita de la base y la revisión ISIC.
- **Sesgos y cautelas:** Desfase de 2–3 años y huecos por país.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Cambios de revisión ISIC entre bases INDSTAT.
- **Uso en el bloque:** AG-B05 y AG-B03: peso y especialización manufacturera por país y rama; AG-B04: comparación internacional de mercados industriales.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «UNIDO INDSTAT industrial statistics database ILOSTAT UNCTADstat free access»; WebFetch: sí, el portal carga)
- **Origen:** Alta 2026-11-02 (F9 Bloque B V2.0, TFB-01).

#### MBF-0011 · Q 78 (B) — MoSPI — Ministry of Statistics and Programme Implementation (India)

- **Canal oficial (URL raíz):** https://www.mospi.gov.in/
- **Emisor:** Gobierno de la India
- **Documentación y notas:** PIB, índice de producción industrial (IIP), IPC y Annual Survey of Industries. Confirmada vía Índice UK Data Service «National statistics institutes» (https://ukdataservice.ac.uk/help/other-data-providers/international-data/national-statistics-institutes/).
- **Temática:** TFB-01 Estadísticas oficiales y organismos internacionales (principal) · secundarias: —
- **Calidad Q:** 78 (B) — Primariedad 18/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 14/15 · Independencia 8/10 · Actualidad 8/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** India: PIB, IIP por industria, ASI
- **Motivo de inclusión y uso:** Fuente primaria del mayor mercado emergente de crecimiento rápido.
- **Restricciones de uso:** Cita de la fuente.
- **Sesgos y cautelas:** Revisiones de base y debates metodológicos sobre el PIB.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Cambios de año base periódicos.
- **Uso en el bloque:** AG-B04 y AG-B13: dimensionado y crecimiento sectorial en la India; AG-B05: producción industrial.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Wikipedia list of national and international statistical services»; WebFetch: sí, página índice)
- **Origen:** Alta 2026-11-02 (F9 Bloque B V2.0, TFB-01).

#### MBF-0010 · Q 71 (B) — National Bureau of Statistics of China (NBS)

- **Canal oficial (URL raíz):** http://www.stats.gov.cn/english/
- **Emisor:** Oficina Nacional de Estadística de China
- **Documentación y notas:** Producción industrial por producto (acero, cemento, vehículos, energía), inversión en activos fijos, ventas minoristas, PMI oficial. Confirmada vía Índice UK Data Service «National statistics institutes» (https://ukdataservice.ac.uk/help/other-data-providers/international-data/national-statistics-institutes/).
- **Temática:** TFB-01 Estadísticas oficiales y organismos internacionales (principal) · secundarias: TFB-05
- **Calidad Q:** 71 (B) — Primariedad 18/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 13/15 · Independencia 5/10 · Actualidad 8/10 · Acceso 7/10
- **Tipología:** primaria
- **Acceso:** Abierto (versión inglesa más limitada)
- **Ámbitos:** China: producción industrial por producto, inversión, consumo, PMI oficial
- **Motivo de inclusión y uso:** Única fuente oficial de producción física por producto de la mayor economía manufacturera.
- **Restricciones de uso:** Cita de la fuente.
- **Sesgos y cautelas:** Dudas de fiabilidad y suavizado de series; contrastar con datos alternativos (comercio, energía).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Cambios de cobertura y discontinuidades de series.
- **Uso en el bloque:** AG-B05: producción física por producto (capacidad y oferta global); AG-B04: demanda china; AG-B14: contraste con fuentes alternativas.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Wikipedia list of national and international statistical services»; WebFetch: sí, página índice)
- **Origen:** Alta 2026-11-02 (F9 Bloque B V2.0, TFB-01).

#### FXF-0062 · Q 70 (B) — DBnomics — redistribución abierta de bases del FMI, BPI y bancos centrales (COFER, IRFCL…)

- **Canal oficial (URL raíz):** https://db.nomics.world/IMF/COFER (también: https://db.nomics.world/IMF/IRFCL)
- **Emisor:** DBnomics (plataforma de datos abiertos de CEPREMAP)
- **Documentación y notas:** Agregador que redistribuye con API unificada bases oficiales (p. ej., COFER e IRFCL del FMI).
- **Temática:** TFB-01 Estadísticas oficiales y organismos internacionales (principal) · secundarias: TFB-02
- **Calidad Q:** 70 (B) — Primariedad 8/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 11/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** secundaria (redistribución de datos oficiales)
- **Acceso:** Abierto (web y API)
- **Ámbitos:** Acceso programático a series oficiales de reservas, balanza de pagos y tipos de cambio
- **Motivo de inclusión y uso:** Herramienta de descarga reproducible para el MOTOR (AG-13) cuando la API del emisor original no basta. Regla F9-b: citar siempre la fuente original (FXF-0051, FXF-0072).
- **Restricciones de uso:** Licencias de los emisores originales.
- **Sesgos posibles:** Posible desfase frente a la fuente original.
- **Historial de exactitud:** No aplicable.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** Motor AG-B16: descarga reproducible con API unificada de bases oficiales (FMI, BPI, Eurostat, OCDE, bancos centrales); citar siempre la fuente original (regla F9-b).
- **Origen:** Reutilizada con su ID de F9 Forex V1.0; temática reasignada a TFB-01 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsquedas web: «IMF COFER currency composition of official foreign exchange reserves 2026» e «IMF International Reserves and Foreign Currency Liquidity data template»; WebFetch: no)

## TFB-02 Bancos centrales y datos macro

#### MBF-0018 · Q 90 (A) — Federal Reserve Board — G.17 Industrial Production and Capacity Utilization

- **Canal oficial (URL raíz):** https://www.federalreserve.gov/Releases/g17/20260615/table0.htm
- **Emisor:** Board of Governors of the Federal Reserve System
- **Documentación y notas:** Publicación mensual (p. ej., 15/06/2026 con datos de mayo: producción +0,1 % m/m, utilización 76,2 %). Desglose por grupos de mercado, grupos industriales (definidos por NAICS) y fases del proceso. Descarga: federalreserve.gov/datadownload/Choose.aspx?rel=g17; en FRED: release 13.
- **Temática:** TFB-02 Bancos centrales y datos macro (principal) · secundarias: TFB-04
- **Calidad Q:** 90 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** EE. UU.: producción y utilización de capacidad por industria NAICS
- **Motivo de inclusión y uso:** Indicador clave del ciclo industrial y de la holgura de capacidad por industria.
- **Restricciones de uso:** Dominio público con cita de la publicación y fecha.
- **Sesgos y cautelas:** Revisiones mensuales y anuales.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B05: utilización de capacidad por industria (riesgo de exceso o escasez de oferta); AG-B08: ciclo industrial; Motor AG-B16: series para MC-B01…MC-B10.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Federal Reserve G.17 Industrial Production and Capacity Utilization release by industry»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9 Bloque B V2.0, TFB-02).

#### RF-0003 · Q 89 (A) — BIS (Bank for International Settlements), sección de estadísticas

- **Canal oficial:** bis.org/statistics/
- **Documentación y notas:** Portal de datos vigente: data.bis.org · Serie de crédito total de la pieza 4.3: bis.org/statistics/totcredit.htm
- **Temática:** TFB-02 Bancos centrales y datos macro (principal) · secundarias: TFB-01
- **Calidad Q:** 89 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 10/10
- **Nivel de fiabilidad en V2.4:** A
- **Tipología:** primaria
- **Motivo de inclusión:** Estadísticas internacionales de referencia en banca central con módulos cambiarios propios: tipos de cambio bilaterales y efectivos (nominales y reales), encuesta trienal de divisas y derivados OTC, estadísticas bancarias internacionales y crédito global en dólares. Uso: MOTOR (AG-13, REER y valoración), AS-ESTR (AG-08, valor) y TR-PFV (AG-21, volúmenes y crédito en dólares).
- **Ámbitos:** Crédito global; banca central; deuda; derivados de OTC; mercados de divisas
- **Restricciones de uso:** Uso libre con atribución; citar la base estadística concreta y la fecha de extracción
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Sesgos posibles:** Ninguno editorial conocido; cobertura centrada en bancos centrales miembros
- **Cambios de propiedad o de metodología:** Sin cambios conocidos; el BIS revisa metodologías de sus bases periódicamente (vigilar notas de las series)
- **Uso en el bloque:** AG-B08: crédito total, deuda y precios inmobiliarios por país; AG-B07: vulnerabilidades financieras de mercados geográficos.
- **Origen:** Reutilizada con su ID de F9 Forex V1.0; temática reasignada a TFB-02 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «BIS effective exchange rate indices triennial survey 2025 foreign exchange turnover» → páginas de bis.org/statistics/; WebFetch: sí, https://www.bis.org/statistics/rpfx25_fx.htm)

#### RF-0004 · Q 89 (A) — BCE Data Portal (Banco Central Europeo)

- **Canal oficial:** https://data.ecb.europa.eu (balanza de pagos y otras estadísticas exteriores, p. ej.: https://data.ecb.europa.eu/publications/balance-payments-and-other-external-statistics/3032577 · política del BCE/Eurosistema y tipos de cambio: https://data.ecb.europa.eu/publications/ecbeurosystem-policy-and-exchange-rates)
- **Documentación y notas:** Descargas, metadatos SDMX y documentación desde el propio portal · Citar la serie con su clave SDMX y la fecha de consulta. Menús de publicación verificados: balanza de pagos (cuenta corriente, inversión directa, de cartera y otra inversión), reservas internacionales, deuda externa, posición de inversión internacional, tipos de cambio e indicadores de competitividad.
- **Temática:** TFB-02 Bancos centrales y datos macro (principal) · secundarias: TFB-01
- **Calidad Q:** 89 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 10/10 · Acceso 10/10
- **Nivel de fiabilidad en V2.4:** A
- **Tipología:** primaria
- **Motivo de inclusión:** Fuente oficial de datos de la eurozona con módulos cambiarios: tipos de referencia del euro, indicadores de competitividad (tipos de cambio efectivos nominales y reales del BCE), balanza de pagos, posición de inversión internacional y reservas, con API SDMX pública. Uso en el Bloque A Forex: MOTOR (AG-13) para REER del euro y descarga de series; AS-G10N (EUR) para flujos de cartera de la zona del euro; AS-EMEA para tipos de referencia de PLN, HUF, CZK y RON frente al euro.
- **Ámbitos:** Eurozona; tipos de cambio; competitividad; balanza de pagos; posición de inversión internacional; reservas; inflación HICP
- **Restricciones de uso:** Datos públicos con atribución; citar la serie (clave SDMX) y su fecha
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Sesgos posibles:** Ninguno; cobertura eurozona
- **Cambios de propiedad o de metodología:** Portal nuevo (sucesor del SDW clásico): vigilar reorganizaciones de series; adopción futura del MBP7 en las estadísticas exteriores
- **Uso en el bloque:** AG-B08 y AG-B09: crédito bancario por sector, tipos, agregados monetarios y estadísticas de mercados de la zona del euro; Motor AG-B16: series SDMX.
- **Origen:** Reutilizada con su ID de F9 Forex V1.0; temática reasignada a TFB-02 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ECB Data Portal data.ecb.europa.eu exchange rates balance of payments»; WebFetch: sí, subpágina de balanza de pagos con menús de reservas, deuda externa, IIP y tipos de cambio)

#### RF-0015 · Q 89 (A) — ALFRED (Archival FRED)

- **Canal oficial (URL raíz):** https://alfred.stlouisfed.org/ (ayuda: https://alfred.stlouisfed.org/help)
- **Emisor:** Federal Reserve Bank of St. Louis (Research Division)
- **Temática:** TFB-02 Bancos centrales y datos macro (principal) · secundarias: —
- **Calidad Q:** 89 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto (condiciones en fred.stlouisfed.org/legal/)
- **Ámbitos:** Vintages (versiones históricas) de series macro de EE. UU. con fechas de publicación
- **Motivo de inclusión y uso:** Muestra el dato tal como estaba disponible en cada fecha; la St. Louis Fed añade observaciones nuevas y revisadas normalmente en un día hábil y contrasta los vintages con la fuente original. Uso: backtests sin sesgo de anticipación y resolución de pronósticos con el dato de su momento (Evaluador, Motor de Cálculo).
- **Sesgos y cautelas:** Cobertura de series menor que FRED; algunos vintages se reconstruyen con servicios de terceros cuando la fuente no conserva estimaciones pasadas.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Uso en el bloque:** Motor AG-B16 y AG-B08: datos en tiempo real (vintages) para pruebas retrospectivas sin sesgo de revisión.
- **Origen:** Reutilizada con su ID de F9 V3.2 (Bloque A general); temática reasignada a TFB-02 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ALFRED Archival Federal Reserve Economic Data vintage St. Louis Fed»; WebFetch: sí)

#### RF-0001 · Q 88 (A) — FRED (Federal Reserve Economic Data, Banco de la Reserva Federal de San Luis)

- **Canal oficial:** fred.stlouisfed.org
- **Documentación y notas:** Documentación de la API: fred.stlouisfed.org/docs/api/fred/ · Cada serie declara su fuente original y metodología en sus metadatos (p. ej. la serie CPIAUCSL de la pieza 4.3: fred.stlouisfed.org/series/CPIAUCSL)
- **Temática:** TFB-02 Bancos centrales y datos macro (principal) · secundarias: TFB-06
- **Calidad Q:** 88 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 10/10
- **Nivel de fiabilidad en V2.4:** A
- **Tipología:** primaria (hospeda series de los emisores oficiales)
- **Motivo de inclusión:** Portal que redistribuye, con metadatos de fuente, las series oficiales de tipos de cambio de la Reserva Federal (H.10: bilaterales diarios e índices nominal y real del dólar, p. ej. DTWEXBGS) y de otros emisores, con API. Uso: MOTOR (AG-13) y Analistas de segmento para series históricas reproducibles; citar siempre la fuente original declarada.
- **Ámbitos:** Macroeconomía; precios e inflación; tipos de interés; mercado laboral; indicadores de recesión; renta variable a nivel agregado
- **Restricciones de uso:** Uso académico y de referencia; citar la serie concreta y la fuente original que FRED declara en sus metadatos
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Sesgos posibles:** Ninguno editorial conocido; posible sesgo de cobertura hacia series estadounidenses
- **Cambios de propiedad o de metodología:** Sin cambios conocidos; mantiene el hosting del Fed de San Luis; verificar en cada mantenimiento
- **Uso en el bloque:** AG-B08: series macro, de crédito y de mercado en un único punto (con API gratuita); Motor AG-B16: insumos de MC-B01…MC-B10; AG-B10: diferenciales y condiciones financieras.
- **Origen:** Reutilizada con su ID de F9 Forex V1.0; temática reasignada a TFB-02 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Federal Reserve H.10 foreign exchange rates nominal broad dollar index» → https://fred.stlouisfed.org/series/DTWEXBGS; WebFetch: sí, serie DTWEXBGS con último dato 23/10/2026)

#### RF-0016 · Q 88 (A) — Federal Reserve Board (comunicados, actas del FOMC, discursos, proyecciones SEP)

- **Canal oficial (URL raíz):** https://www.federalreserve.gov/ (calendario, comunicados y actas del FOMC: https://federalreserve.gov/monetarypolicy/fomccalendars.htm)
- **Emisor:** Board of Governors of the Federal Reserve System
- **Temática:** TFB-02 Bancos centrales y datos macro (principal) · secundarias: —
- **Calidad Q:** 88 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Política monetaria de EE. UU.: calendario del FOMC, comunicados, actas, conferencias de prensa, Summary of Economic Projections (marzo, junio, septiembre, diciembre)
- **Motivo de inclusión y uso:** Fuente original de las decisiones de tipos y de las proyecciones del FOMC (próxima reunión con SEP: 8–9/12/2026). Uso: catalizadores de calendario y lectura de la función de reacción de la Fed.
- **Sesgos y cautelas:** Comunicación con orientación de política (no neutral sobre su propia actuación); las actas se publican tres semanas después.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Uso en el bloque:** AG-B08: orientación de política monetaria de EE. UU. y proyecciones (SEP) para el ciclo; AG-B09: tipos de descuento sectoriales.
- **Origen:** Reutilizada con su ID de F9 V3.2 (Bloque A general); temática reasignada a TFB-02 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Federal Reserve Board FOMC meeting calendars statements minutes»; WebFetch: sí)

#### RF-0017 · Q 88 (A) — Banco Central Europeo (decisiones, cuentas de política monetaria, discursos, proyecciones)

- **Canal oficial (URL raíz):** https://www.ecb.europa.eu/ (decisiones del Consejo de Gobierno: https://www.ecb.europa.eu/press/govcdec)
- **Emisor:** Banco Central Europeo
- **Temática:** TFB-02 Bancos centrales y datos macro (principal) · secundarias: —
- **Calidad Q:** 88 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Política monetaria de la eurozona: decisiones de tipos (14:15 CET), declaración y preguntas de la conferencia de prensa, cuentas de la reunión (4 semanas después), otras decisiones (supervisión, estabilidad financiera, estadísticas)
- **Motivo de inclusión y uso:** Fuente original de las decisiones del BCE (última conferencia registrada: 29/10/2026). Uso: catalizadores y lectura de la orientación de política monetaria del área del euro.
- **Sesgos y cautelas:** Comunicación con orientación de política; los metadatos de algunas páginas no reflejan la fecha real del contenido.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Uso en el bloque:** AG-B08: orientación de política monetaria y proyecciones de la zona del euro; AG-B09: entorno de tipos para valoración sectorial.
- **Origen:** Reutilizada con su ID de F9 V3.2 (Bloque A general); temática reasignada a TFB-02 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «European Central Bank monetary policy decisions accounts ecb.europa.eu»; WebFetch: sí)

#### RF-0018 · Q 87 (A) — Banco de España (informes, boletín económico, estadísticas)

- **Canal oficial (URL raíz):** https://www.bde.es/ (Boletín Económico: https://www.bde.es/bde/es/secciones/informes/analisis-economico-e-investigacion/boletin-economico/ · Boletín Estadístico: https://www.bde.es/wbe/es/publicaciones/informacion-estadistica/boletin-estadistico/)
- **Emisor:** Banco de España
- **Temática:** TFB-02 Bancos centrales y datos macro (principal) · secundarias: TFB-01
- **Calidad Q:** 87 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Economía española; proyecciones macroeconómicas; Informe Anual; estabilidad financiera; Boletín Estadístico; repositorio institucional (repositorio.bde.es)
- **Motivo de inclusión y uso:** Fuente oficial del análisis de coyuntura y de las estadísticas monetarias y financieras de España. Uso: dato primario y diagnóstico oficial para la economía y el sistema financiero españoles.
- **Sesgos y cautelas:** Perspectiva institucional del Eurosistema; algunos enlaces internos del portal (p. ej., «Notas Económicas») apuntaban a anclas rotas en la fecha de consulta.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Uso en el bloque:** AG-B08: coyuntura y previsiones de España; AG-B05 y AG-B09: Central de Balances (ratios sectoriales de empresas no financieras españolas).
- **Origen:** Reutilizada con su ID de F9 V3.2 (Bloque A general); temática reasignada a TFB-02 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Banco de España Boletín Económico informes estadísticas bde.es»; WebFetch: sí)

#### RF-0019 · Q 87 (A) — Bank of England (Monetary Policy Report, actas del MPC)

- **Canal oficial (URL raíz):** https://www.bankofengland.co.uk/ (índice del Monetary Policy Report: https://www.bankofengland.co.uk/sitemap/monetary-policy-report · ejemplo: https://www.bankofengland.co.uk/monetary-policy-report/2026/july-2026)
- **Emisor:** Bank of England
- **Temática:** TFB-02 Bancos centrales y datos macro (principal) · secundarias: —
- **Calidad Q:** 87 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Política monetaria del Reino Unido: Monetary Policy Report trimestral, Monetary Policy Summary y actas del MPC con votaciones individuales, calendario de reuniones 2026–2027
- **Motivo de inclusión y uso:** Fuente original de las decisiones y proyecciones del MPC (p. ej., MPR de julio de 2026: Bank Rate al 3,75 % con votación 6–3). Uso: catalizadores de libra y gilts; reparto de votos como señal adelantada.
- **Sesgos y cautelas:** Comunicación con orientación de política; documentos extensos (leer resumen y actas).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Uso en el bloque:** AG-B08: política monetaria y coyuntura del Reino Unido (Agents' summary por sectores).
- **Origen:** Reutilizada con su ID de F9 V3.2 (Bloque A general); temática reasignada a TFB-02 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «bankofengland.co.uk monetary-policy-report 2026»; WebFetch: sí)

#### RF-0200 · Q 87 (A) — BIS — Central bankers' speeches (discursos de banqueros centrales)

- **Canal oficial (URL raíz):** https://www.bis.org/ (ejemplo de la colección: https://www.bis.org/speeches/20251010-japans-economy-and-monetary-policy · archivo histórico: https://www.bis.org/review/)
- **Emisor:** Bank for International Settlements
- **Temática:** TFB-02 Bancos centrales y datos macro (principal) · secundarias: —
- **Calidad Q:** 87 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria (textos de los propios banqueros centrales)
- **Acceso:** Abierto
- **Ámbitos:** Discursos de gobernadores y miembros de consejos de bancos centrales de todo el mundo, en un único repositorio
- **Motivo de inclusión y uso:** Agrega en un solo canal los discursos de banqueros centrales (p. ej., Kazuo Ueda, BoJ, 10/10/2025), separado de los discursos de la dirección del BIS. Uso: seguimiento de la comunicación de bancos centrales sin cobertura propia en F9 (orientación futura, tono).
- **Sesgos y cautelas:** Es un agregador oficial: citar el discurso con su banco central emisor; los textos reflejan la visión de cada orador.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Uso en el bloque:** AG-B08 y AG-B07: discursos de banqueros centrales sobre sectores (banca, inmobiliario, energía) y riesgos regulatorios.
- **Origen:** Reutilizada con su ID de F9 V3.2 (Bloque A general); temática reasignada a TFB-02 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Bank of Japan Outlook for Economic Activity and Prices statements on monetary policy boj.or.jp»; WebFetch: sí)

#### RF-0651 · Q 87 (A) — Federal Reserve Board — H.15 Selected Interest Rates

- **Canal oficial (URL raíz):** https://www.federalreserve.gov/releases/h15/
- **Emisor:** Board of Governors of the Federal Reserve System
- **Temática:** TFB-02 Bancos centrales y datos macro (principal) · secundarias: TFB-06
- **Calidad Q:** 87 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria (compilación oficial de tipos de mercado y administrados)
- **Acceso:** Abierto (diario, lunes a viernes, 16:15 ET; histórico en la propia publicación y en FRED)
- **Ámbitos:** Fondos federales efectivos, papel comercial, tipo preferencial (prime), ventanilla de descuento, letras del Tesoro, vencimientos constantes nominales (1 mes a 30 años) y ligados a la inflación (5 a 30 años). Última publicación vista: 30/10/2026
- **Motivo de inclusión y uso:** Serie histórica estándar de la curva del Tesoro y de los tipos a corto en EE. UU. (base de las series de FRED). AG-25: pendiente de la curva y tipos reales; AG-24: prime y fondos federales.
- **Sesgos y cautelas:** Series retiradas a lo largo del tiempo (swaps, eurodólares, bonos corporativos de Moody's en versiones antiguas): comprobar la disponibilidad; el «Build Your Package» del DDP se retira en noviembre de 2026.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Uso en el bloque:** AG-B09 y Motor AG-B16: tipos de referencia (Tesoro, papel comercial) para tasas de descuento y costes de financiación.
- **Origen:** Reutilizada con su ID de F9 V3.2 (Bloque A general); temática reasignada a TFB-02 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «federalreserve.gov releases H.15 selected interest rates commercial paper rates»; WebFetch: sí, publicación de 24/05/2010 y página actual)

#### FXF-0001 · Q 86 (A) — Banco Nacional Suizo (BNS/SNB) — evaluación de política monetaria y resumen de las deliberaciones

- **Canal oficial (URL raíz):** https://www.snb.ch/en/ (resumen de las deliberaciones de septiembre de 2026: https://www.snb.ch/en/publications/communication/summaries/zus_20261022)
- **Emisor:** Swiss National Bank (Schweizerische Nationalbank)
- **Documentación y notas:** El SNB publica la decisión en cada evaluación trimestral de política monetaria y, unas cuatro semanas después, un «Summary of discussion» del Consejo de Gobierno (p. ej., 22/10/2026 sobre la reunión del 22–23/09/2026: tipo oficial al 0 %, franco depreciado ~3 % en términos ponderados por comercio desde junio y señalado como «funding currency» de carry; disposición a intervenir en el mercado de divisas «según sea necesario», retirando la mayor disposición a intervenir señalada antes).
- **Temática:** TFB-02 Bancos centrales y datos macro (principal) · secundarias: —
- **Calidad Q:** 86 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto (inglés, alemán, francés e italiano)
- **Ámbitos:** Tipo oficial del SNB, previsión condicional de inflación, lenguaje sobre intervención en divisas, valoración del franco y condiciones monetarias
- **Motivo de inclusión y uso:** Fuente original del único banco central del G10 que usa la intervención cambiaria como instrumento declarado de política. Uso: TR-BCM (AG-09) para la función de reacción del SNB; AS-G10N (USD/CHF, EUR/CHF) y AS-ESTR (CHF como refugio y como divisa de financiación del carry).
- **Restricciones de uso:** Uso libre con atribución; citar fecha de la evaluación y del resumen.
- **Sesgos posibles:** Comunicación con orientación de política; el lenguaje sobre intervención es deliberadamente condicional.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Publicación del resumen de deliberaciones introducida recientemente; vigilar cambios de calendario.
- **Uso en el bloque:** AG-B08: política monetaria suiza y franco como condicionante de exportadores y del sector financiero suizo; AG-B12: contexto de emisores suizos.
- **Origen:** Reutilizada con su ID de F9 Forex V1.0; temática reasignada a TFB-02 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Swiss National Bank monetary policy assessment 2026»; WebFetch: sí, resumen del 22/10/2026)

#### FXF-0002 · Q 86 (A) — Bank of Canada — anuncios del tipo oficial y calendario de publicaciones

- **Canal oficial (URL raíz):** https://www.bankofcanada.ca/ (calendario 2026: https://www.bankofcanada.ca/2025/08/bank-canada-publishes-2026-schedule-policy-interest-rate-announcements-other-major-publications/)
- **Emisor:** Bank of Canada
- **Documentación y notas:** Ocho anuncios al año a las 9:45 ET (2026: 28/01, 18/03, 29/04, 10/06, 15/07, 02/09, 28/10, 09/12); «Summary of deliberations» del Consejo de Gobierno tras cada decisión; Business Outlook Survey y Canadian Survey of Consumer Expectations trimestrales. El 28/10/2026 el tipo oficial se elevó al 2,5 %.
- **Temática:** TFB-02 Bancos centrales y datos macro (principal) · secundarias: —
- **Calidad Q:** 86 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (inglés y francés)
- **Ámbitos:** Tipo oficial de Canadá, comunicados, resumen de deliberaciones, encuestas de expectativas, calendario anual
- **Motivo de inclusión y uso:** Fuente original de la política monetaria canadiense. Uso: TR-BCM (AG-09) para la senda del tipo y el calendario; AS-G10M (AG-04: USD/CAD, CAD/JPY) para el diferencial de tipos frente a la Fed.
- **Restricciones de uso:** Uso libre con atribución.
- **Sesgos posibles:** Comunicación con orientación de política.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B08: política monetaria de Canadá (economía de materias primas y banca); contexto para sectores de recursos y financiero canadienses.
- **Origen:** Reutilizada con su ID de F9 Forex V1.0; temática reasignada a TFB-02 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Bank of Canada Monetary Policy Report interest rate announcement October 2026»; WebFetch: sí, calendario 2026)

#### RF-0612 · Q 86 (A) — Federal Reserve Board — H.4.1 Factors Affecting Reserve Balances (balance de la Fed)

- **Canal oficial (URL raíz):** https://www.federalreserve.gov/releases/h41/
- **Emisor:** Board of Governors of the Federal Reserve System
- **Temática:** TFB-02 Bancos centrales y datos macro (principal) · secundarias: —
- **Calidad Q:** 86 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria (estado contable semanal oficial)
- **Acceso:** Abierto (cada jueves, hacia las 16:30 ET)
- **Ámbitos:** Factores que aportan y absorben reservas: valores en cartera, préstamos y facilidades, reverse repos (incluido el ON RRP), cuenta general del Tesoro (TGA), billetes; saldo de reservas bancarias. Última actualización vista: 29/10/2026
- **Motivo de inclusión y uso:** Medida semanal de la liquidez del sistema en dólares (reservas = activos − TGA − ON RRP − billetes); clave para anticipar tensiones de fin de mes/trimestre y el fin de la reducción del balance. AG-24.
- **Sesgos y cautelas:** Datos de miércoles y medias semanales: la volatilidad intrasemanal (TGA, fechas fiscales) no se ve; la página índice no describe las tablas (consultar la publicación).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Uso en el bloque:** AG-B08 y AG-B10: balance de la Fed y reservas como indicador de liquidez agregada.
- **Origen:** Reutilizada con su ID de F9 V3.2 (Bloque A general); temática reasignada a TFB-02 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «federalreserve.gov releases H.15 selected interest rates commercial paper rates» → enlace desde la página H.15; WebFetch: sí)

#### FXF-0403 · Q 85 (A) — BPI — Global liquidity indicators (GLI): crédito en dólares, euros y yenes a no residentes

- **Canal oficial (URL raíz):** https://bis.org/statistics/about_banking_stats.htm (calendario y portal: https://www.bis.org/statistics/dataportal/banking.htm)
- **Emisor:** Banco de Pagos Internacionales (BPI)
- **Documentación y notas:** Indicadores del crédito a prestatarios no bancarios que combinan préstamos bancarios y emisión de valores de deuda internacionales, con foco en el crédito en moneda extranjera a no residentes en dólares, euros y yenes; documento metodológico enlazado. Publicación trimestral conjunta con las estadísticas bancarias de localización (29/10/2026: datos de fin de junio de 2026; 31/07/2026: fin de marzo).
- **Temática:** TFB-02 Bancos centrales y datos macro (principal) · secundarias: —
- **Calidad Q:** 85 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 7/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Crédito global en dólares fuera de EE. UU.; financiación en divisas de emergentes; ciclo financiero global
- **Motivo de inclusión y uso:** Mide el «dólar global» del lado de la financiación, determinante del canal de riesgo del dólar. Uso: AS-ESTR (AG-08) y TR-BCM (AG-09) para el ciclo de liquidez en dólares; AS-EMLA y AS-EMEA para vulnerabilidad de divisas emergentes con alta deuda en dólares. Complementa la ficha general RF-0003.
- **Restricciones de uso:** Uso con atribución; citar trimestre de referencia y fecha de publicación.
- **Sesgos posibles:** Desfase de unos cuatro meses; no capta la deuda implícita en dólares de swaps y forwards de divisas.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B08 y AG-B10: liquidez global y crédito en divisas a no residentes como condicionante de mercados emergentes y sectores financiados en dólares.
- **Origen:** Reutilizada con su ID de F9 Forex V1.0; temática reasignada a TFB-02 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «BIS locational banking statistics global liquidity indicators»; WebFetch: sí, páginas about_banking_stats y dataportal/banking)

#### RF-0020 · Q 85 (A) — Bank of Japan (declaraciones de política, Outlook Report)

- **Canal oficial (URL raíz):** https://www.boj.or.jp/en/ (Outlook for Economic Activity and Prices: https://www.boj.or.jp/en/mopo/outlook/index.htm)
- **Emisor:** Bank of Japan
- **Temática:** TFB-02 Bancos centrales y datos macro (principal) · secundarias: —
- **Calidad Q:** 85 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (versión inglesa con cierto desfase respecto a la japonesa)
- **Ámbitos:** Política monetaria de Japón; Outlook Report trimestral (último: «The Bank's View», 30/10/2026); declaraciones de política
- **Motivo de inclusión y uso:** Fuente original de decisiones y previsiones del BoJ, clave para yen, JGB y carry trade. Uso: catalizadores de calendario y lectura de la normalización monetaria japonesa.
- **Sesgos y cautelas:** El texto completo del Outlook se publica días después de «The Bank's View»; traducciones al inglés con retraso.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Uso en el bloque:** AG-B08: política monetaria y perspectivas de Japón; AG-B04: lectura sectorial de la economía japonesa.
- **Origen:** Reutilizada con su ID de F9 V3.2 (Bloque A general); temática reasignada a TFB-02 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Bank of Japan Outlook for Economic Activity and Prices statements on monetary policy boj.or.jp»; WebFetch: sí)

#### RF-0025 · Q 83 (A) — Liberty Street Economics (blog del Federal Reserve Bank of New York)

- **Canal oficial (URL raíz):** https://libertystreeteconomics.newyorkfed.org/
- **Emisor:** Federal Reserve Bank of New York (economistas del Research and Statistics Group)
- **Temática:** TFB-02 Bancos centrales y datos macro (principal) · secundarias: TFB-05
- **Calidad Q:** 83 (A) — Primariedad 16/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 14/15 · Independencia 9/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** secundaria cualificada (análisis de economistas de banco central)
- **Acceso:** Abierto
- **Ámbitos:** Mercados financieros, crédito de hogares, mercados monetarios, inflación, estabilidad financiera
- **Motivo de inclusión y uso:** Blog del NY Fed (desde 2011) con análisis basados en datos propios. Uso: interpretación de mercados monetarios y crédito por economistas del sistema Fed.
- **Sesgos y cautelas:** Aviso expreso: las opiniones son de los autores, no posición oficial del NY Fed ni del Sistema.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Uso en el bloque:** AG-B08 y AG-B05: análisis aplicados de la Fed de Nueva York (cadenas de suministro, inflación, crédito) que sustentan hipótesis sectoriales.
- **Origen:** Reutilizada con su ID de F9 V3.2 (Bloque A general); temática reasignada a TFB-02 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Liberty Street Economics Federal Reserve Bank of New York blog»; WebFetch: sí)

#### RF-0201 · Q 82 (A) — FRASER (Federal Reserve Archival System for Economic Research)

- **Canal oficial (URL raíz):** https://fraser.stlouisfed.org/
- **Emisor:** Federal Reserve Bank of St. Louis
- **Temática:** TFB-02 Bancos centrales y datos macro (principal) · secundarias: TFB-01
- **Calidad Q:** 82 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 14/15 · Independencia 10/10 · Actualidad 6/10 · Acceso 10/10
- **Tipología:** primaria (documentos históricos digitalizados)
- **Acceso:** Abierto (búsqueda a texto completo, API REST y OAI-PMH)
- **Ámbitos:** Historia financiera, económica y bancaria de EE. UU.: publicaciones estadísticas históricas, documentos de la Fed, colecciones de archivo
- **Motivo de inclusión y uso:** Archivo digital de documentos y estadísticas históricas (p. ej., ediciones antiguas de publicaciones de la Fed). Uso: reconstruir series largas, analogías históricas y contexto de episodios de crisis.
- **Sesgos y cautelas:** Cobertura centrada en EE. UU.; fondos históricos, no datos de actualidad.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Uso en el bloque:** AG-B13 y AG-B14: series y documentos históricos para analogías de ciclos sectoriales largos.
- **Origen:** Reutilizada con su ID de F9 V3.2 (Bloque A general); temática reasignada a TFB-02 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ALFRED Archival Federal Reserve Economic Data vintage St. Louis Fed»; WebFetch: sí)

#### RF-0666 · Q 82 (A) — Federal Reserve Board — Senior Loan Officer Opinion Survey on Bank Lending Practices (SLOOS)

- **Canal oficial (URL raíz):** https://www.federalreserve.gov/data/sloos.htm
- **Emisor:** Board of Governors of the Federal Reserve System
- **Temática:** TFB-02 Bancos centrales y datos macro (principal) · secundarias: —
- **Calidad Q:** 82 (A) — Primariedad 17/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 7/10 · Acceso 10/10
- **Tipología:** primaria (encuesta oficial a bancos)
- **Acceso:** Abierto (trimestral, antes de cuatro reuniones del FOMC; última vista: julio de 2026)
- **Ámbitos:** Cambios en criterios y condiciones de concesión de préstamos y en la demanda de crédito de empresas y hogares; hasta 80 grandes bancos nacionales y 24 sucursales de bancos extranjeros; preguntas especiales de actualidad
- **Motivo de inclusión y uso:** Indicador adelantado del ciclo de crédito y de los impagos (el endurecimiento de criterios precede a la ampliación de diferenciales). AG-25.
- **Sesgos y cautelas:** Respuestas cualitativas en «porcentaje neto»; solo crédito bancario (no crédito privado ni bonos).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Uso en el bloque:** AG-B08 y AG-B04: condiciones y demanda de crédito por segmento (empresas, inmobiliario comercial, consumo) como indicador adelantado sectorial.
- **Origen:** Reutilizada con su ID de F9 V3.2 (Bloque A general); temática reasignada a TFB-02 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «federalreserve.gov releases H.15 selected interest rates commercial paper rates» → enlace desde la página H.15; WebFetch: sí)

#### RF-0669 · Q 81 (A) — BCE — Survey of Professional Forecasters (SPF): expectativas de inflación de la zona del euro

- **Canal oficial (URL raíz):** https://www.ecb.europa.eu/stats/ecb_surveys/survey_of_professional_forecasters/html/index.en.html (ejemplo de nota trimestral: https://www.ecb.europa.eu//press/pr/date/2024/html/ecb.pr240126~fae16e158f.en.html)
- **Emisor:** Banco Central Europeo
- **Temática:** TFB-02 Bancos centrales y datos macro (principal) · secundarias: —
- **Calidad Q:** 81 (A) — Primariedad 15/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 7/10 · Acceso 10/10
- **Tipología:** primaria (encuesta oficial; las respuestas son previsiones de expertos)
- **Acceso:** Abierto (resultados trimestrales y microdatos anonimizados en el BCE Data Portal)
- **Ámbitos:** Previsiones trimestrales de HICP general y subyacente, PIB real y paro para el año en curso, los dos siguientes y el largo plazo (unos cinco años vista), con distribuciones de probabilidad. Ejemplo: 1T2024, 59 respuestas, inflación a largo plazo 2,0 %
- **Motivo de inclusión y uso:** Referencia de expectativas de inflación a largo plazo de encuesta para contrastar con la inflación implícita de mercado (swaps y bonos ligados) y estimar la prima de riesgo de inflación en el euro. AG-25.
- **Sesgos y cautelas:** Opinión de expertos (regla F9-a); trimestral; la página índice no se pudo cargar (se leyó la nota de prensa del 26/01/2024).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Uso en el bloque:** AG-B08 y AG-B13: expectativas profesionales de inflación, crecimiento y paro de la zona del euro para escenarios.
- **Origen:** Reutilizada con su ID de F9 V3.2 (Bloque A general); temática reasignada a TFB-02 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ECB Survey of Monetary Analysts SMA results and Survey of Professional Forecasters inflation expectations»; WebFetch: sí, nota de prensa del SPF 1T2024)

#### RF-0202 · Q 76 (B) — The FRED Blog (Federal Reserve Bank of St. Louis)

- **Canal oficial (URL raíz):** https://fredblog.stlouisfed.org/
- **Emisor:** Federal Reserve Bank of St. Louis (Research Division)
- **Temática:** TFB-02 Bancos centrales y datos macro (principal) · secundarias: —
- **Calidad Q:** 76 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 13/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** secundaria cualificada (divulgación sobre datos oficiales)
- **Acceso:** Abierto
- **Ámbitos:** Lectura de series de FRED y ALFRED; revisiones de datos; gráficos reproducibles
- **Motivo de inclusión y uso:** Notas breves que explican cómo leer y combinar series (p. ej., cómo cambian las estimaciones de empleo del BLS entre vintages). Uso: apoyo metodológico para agentes que consumen FRED/ALFRED (RF-0001, RF-0015).
- **Sesgos y cautelas:** Divulgativo; no sustituye a la serie primaria.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Uso en el bloque:** AG-B08 y Motor AG-B16: notas didácticas sobre construcción y lectura de series FRED; apoyo a la elección de indicadores.
- **Origen:** Reutilizada con su ID de F9 V3.2 (Bloque A general); temática reasignada a TFB-02 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ALFRED Archival Federal Reserve Economic Data vintage St. Louis Fed»; WebFetch: sí)

## TFB-03 Reguladores, registros y documentación corporativa

#### RF-0002 · Q 89 (A) — SEC EDGAR (U.S. Securities and Exchange Commission)

- **Canal oficial (URL raíz):** https://www.sec.gov/ (EDGAR; documentación de APIs: https://www.sec.gov/page/sec-api-documentation)
- **Emisor:** U.S. Securities and Exchange Commission
- **Documentación y notas:** Repositorio de presentaciones regulatorias (10-K, 10-Q, 8-K, 20-F, 40-F, 6-K, 13F, folletos) con búsqueda por empresa y de texto completo. Las APIs estructuradas de data.sec.gov (submissions, companyfacts, frames) se registran aparte en MBF-0201 (TFB-07); su página de documentación, consultada en esta verificación, confirma acceso sin clave y cobertura XBRL de 10-K, 10-Q, 8-K, 20-F, 40-F y 6-K. Las posiciones 13F tienen ficha propia (RF-0044, TFB-15).
- **Temática:** TFB-03 Reguladores, registros y documentación corporativa (principal) · secundarias: TFB-07
- **Calidad Q:** 89 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 10/10
- **Nivel de fiabilidad en V2.4:** A
- **Tipología:** primaria
- **Motivo de inclusión:** Repositorio primario de documentos regulatorios de emisores estadounidenses y de emisores extranjeros registrados en la SEC: la fuente de máxima autoridad para hechos corporativos y estados financieros comparables (XBRL)
- **Ámbitos:** Presentaciones regulatorias; estados financieros XBRL; hechos corporativos; participaciones institucionales; emisores estadounidenses y extranjeros registrados
- **Restricciones de uso:** Datos públicos; acceso automatizado sujeto a la política de privacidad y seguridad de SEC.gov (Developer FAQs); citar formulario, fecha de presentación y CIK
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Sesgos posibles:** Documentos primarios redactados por los propios emisores; en frames, los periodos se alinean al calendario y pueden mezclar ejercicios fiscales distintos
- **Cambios de propiedad o de metodología:** Sin cambios conocidos; dependencia del servicio público EDGAR
- **Uso en el bloque:** AG-B12: lectura de 10-K/20-F de candidatos (riesgos, segmentos, litigios); AG-B03: segmentos y cuotas declaradas por competidores; AG-B07: factores de riesgo regulatorio; AG-B09: notas a los estados financieros (para datos XBRL masivos, MBF-0201).
- **Origen:** Semilla de F9 V3.2 (Bloque A general) revalidada con su ID; temática reasignada a TFB-03 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «SEC EDGAR application programming interfaces data.sec.gov submissions companyfacts XBRL frames full-text search»; WebFetch: sí)

#### MBF-0020 · Q 88 (A) — Companies House — productos de datos (Reino Unido)

- **Canal oficial (URL raíz):** https://www.gov.uk/guidance/companies-house-data-products
- **Emisor:** Companies House (Gobierno del Reino Unido)
- **Documentación y notas:** Productos gratuitos: instantánea mensual de datos de empresas (CSV), cuentas en XBRL/iXBRL (ficheros diarios y mensuales), instantánea de titulares reales (PSC, JSON) y servicio URI; pasarela XML de pago. Foro de desarrolladores: forum.companieshouse.gov.uk.
- **Temática:** TFB-03 Reguladores, registros y documentación corporativa (principal) · secundarias: TFB-07
- **Calidad Q:** 88 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto y gratuito (salvo pasarela XML de pago)
- **Ámbitos:** Empresas del Reino Unido: datos registrales, cuentas presentadas, titulares reales
- **Motivo de inclusión y uso:** Fuente primaria de cuentas de empresas británicas, incluidas las no cotizadas (competidores y proveedores).
- **Restricciones de uso:** Uso libre con cita; condiciones de Companies House.
- **Sesgos y cautelas:** Cuentas de pequeñas empresas abreviadas; solo cuentas presentadas electrónicamente en XBRL.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Reforma de Companies House (verificación de identidad) en curso.
- **Uso en el bloque:** AG-B03: estructura competitiva (cuentas de competidores no cotizados); AG-B09: márgenes sectoriales; AG-B12: verificación de entidades y titulares reales.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-03 (búsqueda web: «Companies House free API accounts data bulk download GLEIF LEI search API free»; WebFetch: sí)
- **Origen:** Alta 2026-11-03 (F9 Bloque B V2.0, TFB-03).

#### MBF-0608 · Q 88 (A) — Unión Europea (Oficina de Publicaciones) — EUR-Lex: acceso al Derecho de la UE y procedimientos legislativos

- **Canal oficial (URL raíz):** https://eur-lex.europa.eu/collection/legislative-procedures.html (portal: https://eur-lex.europa.eu/)
- **Emisor:** Oficina de Publicaciones de la Unión Europea
- **Documentación y notas:** Portal oficial del Derecho de la UE: Diario Oficial (series L y C), tratados, legislación vigente y consolidada, preparatorios (propuestas de la Comisión), jurisprudencia y la colección de procedimientos legislativos con su tramitación interinstitucional. Enlazado desde el Observatorio Legislativo (MBF-0609) y el EU Sanctions Helpdesk.
- **Temática:** TFB-03 Reguladores, registros y documentación corporativa (principal) · secundarias: TFB-16
- **Calidad Q:** 88 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria (fuente jurídica oficial)
- **Acceso:** Abierto, sin registro
- **Ámbitos:** Normativa de la UE vigente y en tramitación: reglamentos, directivas, actos delegados y de ejecución
- **Motivo de inclusión y uso:** Fuente primaria de los hechos regulatorios de la UE que afectan a sectores (IA, baterías, química, energía, finanzas, sanciones).
- **Restricciones de uso:** Uso libre con atribución; solo la edición electrónica del DOUE tiene valor jurídico.
- **Sesgos y cautelas:** Las versiones consolidadas son documentación sin valor jurídico; los preparatorios no son normas aprobadas.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B07 Regulación y Geopolítica: textos de reglamentos y directivas sectoriales y su calendario de aplicación; AG-B11 Sostenibilidad y Riesgos: normativa ESG (CSRD, taxonomía); AG-B13 Prospectiva: propuestas en tramitación.
- **Origen:** Alta F9_comp (2026-11-03).
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-03 (búsqueda web: «EUR-Lex official access to EU law and Legislative Observatory OEIL European Parliament procedure file»; WebFetch: no; enlace confirmado también desde la página «Find out more» del OEIL)

#### MBF-0021 · Q 87 (A) — GLEIF — Global Legal Entity Identifier Foundation (LEI Search 2.0 y API)

- **Canal oficial (URL raíz):** https://www.gleif.org/newsroom/press-releases/gleif-answers-industry-demand-for-customized-automated-access-to-rich-lei-data-with-lei-search-2-0-and-companion-api/2021-01-19_gleif-search-2.0-_api_final_approved_v1.pdf
- **Emisor:** Global Legal Entity Identifier Foundation (GLEIF)
- **Documentación y notas:** LEI Search 2.0 y API gratuita (lanzadas el 19/01/2021) con datos de nivel 1 (quién es quién) y nivel 2 (quién posee a quién: matrices directas y últimas). Acuerdo GLEIF–Companies House de 14/01/2025 para enlazar identificadores (comunicado en gleif.org).
- **Temática:** TFB-03 Reguladores, registros y documentación corporativa (principal) · secundarias: TFB-07
- **Calidad Q:** 87 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto (API sin coste)
- **Ámbitos:** Identificadores LEI, matrices, sucursales y estructuras de grupo
- **Motivo de inclusión y uso:** Permite reconstruir estructuras de grupo y vincular emisores, filiales e instrumentos.
- **Restricciones de uso:** Licencia CC0 de los datos LEI.
- **Sesgos y cautelas:** Cobertura limitada a entidades con LEI; relaciones declaradas por las propias entidades.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B12: identificación inequívoca de emisores y grupos; AG-B03: estructuras de propiedad; Motor AG-B16: claves de unión entre bases.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-03 (búsqueda web: «Companies House free API accounts data bulk download GLEIF LEI search API free»; WebFetch: no)
- **Origen:** Alta 2026-11-03 (F9 Bloque B V2.0, TFB-03).

#### MBF-0609 · Q 87 (A) — Parlamento Europeo — Observatorio Legislativo (OEIL): fichas de procedimiento

- **Canal oficial (URL raíz):** https://oeil.secure.europarl.europa.eu/oeil (información: https://oeil.europarl.europa.eu/oeil/en/find-out-more)
- **Emisor:** Parlamento Europeo (DG de la Presidencia; gestión técnica DG ITEC)
- **Documentación y notas:** Fichas de todos los procedimientos legislativos y no legislativos en curso y de los iniciados desde julio de 1994: datos básicos y fase, actores (comisión parlamentaria y ponentes, comisario y DG responsables), acontecimientos clave, pasarela documental con resúmenes neutrales, previsiones (votaciones en comisión y pleno), acto final en el DOUE y enlaces a EUR-Lex e IPEX. Carga diaria; búsquedas guardadas con alertas y RSS por expediente; en inglés y francés.
- **Temática:** TFB-03 Reguladores, registros y documentación corporativa (principal) · secundarias: TFB-16
- **Calidad Q:** 87 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria (registro oficial de la tramitación)
- **Acceso:** Abierto, sin registro (alertas con registro gratuito)
- **Ámbitos:** Tramitación legislativa de la UE: calendario, ponentes y documentos
- **Motivo de inclusión y uso:** Permite anticipar votaciones y cambios regulatorios que mueven sectores antes de la publicación en el DOUE.
- **Restricciones de uso:** Uso libre con atribución.
- **Sesgos y cautelas:** Las previsiones son orientativas; los resúmenes no sustituyen al texto.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B07 Regulación y Geopolítica: seguimiento de expedientes con impacto sectorial (fechas de votación, enmiendas); AG-B13 Prospectiva: calendario de catalizadores regulatorios; AG-B02 Director: agenda de vigilancia.
- **Origen:** Alta F9_comp (2026-11-03).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-03 (búsqueda web: «Legislative Observatory OEIL European Parliament oeil.secure.europarl.europa.eu»; WebFetch: sí, página «Find out more»)

#### MBF-0610 · Q 87 (A) — Office of the Federal Register (NARA) y GPO — FederalRegister.gov

- **Canal oficial (URL raíz):** https://www.federalregister.gov/ (ayuda leída: https://www.federalregister.gov/reader-aids/using-federalregister-gov/document-features-sidebar)
- **Emisor:** Office of the Federal Register (National Archives and Records Administration) en colaboración con la Government Publishing Office (GPO)
- **Documentación y notas:** Edición web diaria del Federal Register: normas, propuestas de norma, avisos y órdenes ejecutivas de las agencias federales de EE. UU.; documentos en inspección pública antes de su publicación, banner con fecha límite de comentarios y enlace a Regulations.gov, PDF oficial en govinfo.gov, suscripciones y recursos para desarrolladores (API).
- **Temática:** TFB-03 Reguladores, registros y documentación corporativa (principal) · secundarias: TFB-16
- **Calidad Q:** 87 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria (publicación oficial; la web no es la edición oficial, que es la de govinfo.gov)
- **Acceso:** Abierto, sin registro; API gratuita
- **Ámbitos:** Regulación federal de EE. UU. en todas las agencias (SEC, FDA, EPA, FCC, Comercio…)
- **Motivo de inclusión y uso:** Fuente primaria para fechar y leer normas federales que afectan a sectores, controles de exportación (BIS) y aranceles.
- **Restricciones de uso:** Uso libre (dominio público).
- **Sesgos y cautelas:** La propia web advierte que no sustituye a la edición oficial de govinfo.gov; verificar la cita jurídica allí.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B07 Regulación y Geopolítica: normas finales y propuestas con impacto sectorial, controles de exportación y aranceles; AG-B13 Prospectiva: plazos de comentarios y fechas de efecto como catalizadores.
- **Origen:** Alta F9_comp (2026-11-03).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-03 (búsqueda web: «FederalRegister.gov API documents and Regulations.gov API public comments dockets»; WebFetch: sí, página de ayuda)

#### RF-0026 · Q 87 (A) — CNMV (registros oficiales, información privilegiada, otra información relevante, participaciones significativas)

- **Canal oficial (URL raíz):** https://www.cnmv.es/ (Otra información relevante: https://www.cnmv.es/portal/Otra-Informacion-Relevante/Consulta-OIR?lang=es · Información privilegiada: https://www.cnmv.es/portal/informacion-privilegiada/consulta-ip?lang=es)
- **Emisor:** Comisión Nacional del Mercado de Valores
- **Temática:** TFB-03 Reguladores, registros y documentación corporativa (principal) · secundarias: —
- **Calidad Q:** 87 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (alertas por correo por entidad o tipo de información)
- **Ámbitos:** Comunicaciones de emisores españoles: información privilegiada, OIR (informes financieros y de auditoría, derechos de voto, autocartera, OPA, operaciones vinculadas, suspensiones, calificaciones), participaciones significativas
- **Motivo de inclusión y uso:** Registro oficial de lo que comunican los emisores cotizados (art. 227 LMV), filtrable por entidad, código LEI, tipo y fecha. Uso: hechos corporativos de primera mano para valores españoles.
- **Sesgos y cautelas:** La CNMV publica sin responsabilizarse de la exactitud del contenido remitido por el emisor; contrastar con cuentas auditadas.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Uso en el bloque:** AG-B12 y AG-B09: información privilegiada, OIR, participaciones significativas e informes financieros de emisores españoles; AG-B07: sanciones y advertencias.
- **Origen:** Reutilizada con su ID de F9 V3.2 (Bloque A general); temática reasignada a TFB-03 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «CNMV registros oficiales información privilegiada otra información relevante participaciones significativas»; WebFetch: sí)

#### RF-0027 · Q 87 (A) — ESMA (registros, informes de tendencias, riesgos y vulnerabilidades)

- **Canal oficial (URL raíz):** https://www.esma.europa.eu/ (TRV n.º 1 2026: https://www.esma.europa.eu/document/trends-risks-and-vulnerabilities-trv-report-no-1-2026)
- **Emisor:** European Securities and Markets Authority
- **Temática:** TFB-03 Reguladores, registros y documentación corporativa (principal) · secundarias: —
- **Calidad Q:** 87 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Supervisión de valores de la UE; informes TRV (Risk Monitor y anexo estadístico, semestrales); indicadores estructurales de mercado; registros
- **Motivo de inclusión y uso:** Diagnóstico oficial de riesgos de los mercados de valores europeos con anexo estadístico. Uso: mapa de riesgos sistémicos y vulnerabilidades del mercado europeo.
- **Sesgos y cautelas:** Perspectiva supervisora (énfasis en riesgos); las fichas de documento no siempre muestran fecha de publicación.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Uso en el bloque:** AG-B07: regulación europea de mercados; AG-B12: registros ESMA (FIRDS, entidades, folletos) para identificar instrumentos; AG-B11: riesgos y vulnerabilidades.
- **Origen:** Reutilizada con su ID de F9 V3.2 (Bloque A general); temática reasignada a TFB-03 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ESMA TRV Trends Risks and Vulnerabilities report registers esma.europa.eu»; WebFetch: sí)

#### RF-0028 · Q 86 (A) — Financial Conduct Authority (FCA)

- **Canal oficial (URL raíz):** https://www.fca.org.uk/ (Financial Services Register: https://www.fca.org.uk/firms/financial-services-register)
- **Emisor:** Financial Conduct Authority (Reino Unido)
- **Temática:** TFB-03 Reguladores, registros y documentación corporativa (principal) · secundarias: —
- **Calidad Q:** 86 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto (API gratuita del Register sin garantías de servicio; extractos masivos de pago)
- **Ámbitos:** Autorizaciones de firmas e individuos (FCA y PRA), firmas no autorizadas y clones, representantes designados, sanciones
- **Motivo de inclusión y uso:** Registro público para comprobar si una entidad o persona está autorizada y su historial disciplinario. Uso: control de credibilidad y detección de fraudes en emisores y gestores del Reino Unido.
- **Sesgos y cautelas:** Jurisdicción británica; la lista de firmas no autorizadas no es exhaustiva.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Uso en el bloque:** AG-B07: regulación y registro de entidades del Reino Unido (FCA Register); AG-B12: comprobación de entidades y productos.
- **Origen:** Reutilizada con su ID de F9 V3.2 (Bloque A general); temática reasignada a TFB-03 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Financial Conduct Authority FCA Financial Services Register fca.org.uk»; WebFetch: sí)

#### MBF-0611 · Q 85 (A) — GSA (programa eRulemaking) — Regulations.gov y su API v4 (expedientes, documentos y comentarios)

- **Canal oficial (URL raíz):** https://open.gsa.gov/api/regulationsgov/ (portal: https://www.regulations.gov/)
- **Emisor:** U.S. General Services Administration (GSA), programa eRulemaking
- **Documentación y notas:** Portal federal de participación en la elaboración de normas: expedientes (dockets), documentos y comentarios públicos de las agencias. API v4 con puntos de acceso separados para documentos, comentarios y expedientes; clave gratuita de api.data.gov en la cabecera X-Api-Key (DEMO_KEY solo para pruebas); límites de uso de api.data.gov (para el envío de comentarios, 50 peticiones/minuto y 500/hora).
- **Temática:** TFB-03 Reguladores, registros y documentación corporativa (principal) · secundarias: TFB-16
- **Calidad Q:** 85 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 14/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** primaria (registro oficial de expedientes normativos)
- **Acceso:** Abierto; API con clave gratuita
- **Ámbitos:** Expedientes normativos federales de EE. UU. y comentarios del público y de la industria
- **Motivo de inclusión y uso:** Permite leer los comentarios de empresas y asociaciones sobre normas en curso: posición de la industria y probabilidad de cambios.
- **Restricciones de uso:** Uso libre; la API exige clave gratuita y respeto de límites.
- **Sesgos y cautelas:** Los comentarios son opiniones de parte; no todas las agencias publican todo en el portal.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Migración de la API v3 a v4 (separación de puntos de acceso).
- **Uso en el bloque:** AG-B07 Regulación y Geopolítica: estado de expedientes y posiciones de la industria en normas sectoriales; AG-B14 Contrarias: argumentos opuestos documentados; Motor AG-B16: descarga por API.
- **Origen:** Alta F9_comp (2026-11-03).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-03 (búsqueda web: «FederalRegister.gov API documents and Regulations.gov API public comments dockets»; WebFetch: sí)

#### RF-0206 · Q 85 (A) — BaFin (Bundesanstalt für Finanzdienstleistungsaufsicht)

- **Canal oficial (URL raíz):** http://www.bafin.de/EN/Homepage/homepage_node.html (según directorio FCA)
- **Emisor:** Autoridad Federal de Supervisión Financiera de Alemania
- **Temática:** TFB-03 Reguladores, registros y documentación corporativa (principal) · secundarias: —
- **Calidad Q:** 85 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (parte del contenido solo en alemán)
- **Ámbitos:** Supervisión integrada (banca, seguros, valores) de Alemania; bases de datos de entidades autorizadas, notificaciones de derechos de voto y posiciones cortas netas, sanciones
- **Motivo de inclusión y uso:** Fuente primaria de hechos regulatorios y de registros de emisores y entidades alemanas. Uso: confirmar autorizaciones, participaciones significativas y medidas supervisoras en Alemania.
- **Sesgos y cautelas:** Cobertura nacional; terminología y versiones en alemán más completas.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Uso en el bloque:** AG-B12: base de datos de derechos de voto y operaciones de directivos de emisores alemanes; AG-B07: supervisión alemana.
- **Origen:** Reutilizada con su ID de F9 V3.2 (Bloque A general); temática reasignada a TFB-03 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «list of financial regulatory authorities by country wikipedia» → directorio FCA; WebFetch: sí, sobre el directorio FCA; sitio de BaFin no leído)

#### RF-0207 · Q 85 (A) — AMF (Autorité des marchés financiers, Francia)

- **Canal oficial (URL raíz):** https://www.amf-france.org/en (según directorio FCA)
- **Emisor:** Autorité des marchés financiers
- **Temática:** TFB-03 Reguladores, registros y documentación corporativa (principal) · secundarias: —
- **Calidad Q:** 85 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Mercados de valores franceses: base documental de emisores (BDIF), declaraciones de umbrales, OPA, sanciones, listas negras de sitios no autorizados
- **Motivo de inclusión y uso:** Regulador del principal mercado de Euronext. Uso: hechos corporativos y regulatorios de emisores franceses y alertas de fraude.
- **Sesgos y cautelas:** Parte de la documentación de emisores solo en francés.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Uso en el bloque:** AG-B12: base documental de emisores franceses (BDIF: declaraciones de umbrales y operaciones); AG-B07: regulación francesa.
- **Origen:** Reutilizada con su ID de F9 V3.2 (Bloque A general); temática reasignada a TFB-03 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «list of financial regulatory authorities by country wikipedia» → directorio FCA; WebFetch: sí, sobre el directorio FCA)

#### RF-0208 · Q 85 (A) — CONSOB (Commissione Nazionale per le Società e la Borsa)

- **Canal oficial (URL raíz):** https://www.consob.it/ (directorio de supervisores europeos: https://www.consob.it/web/consob-and-its-activities/financial-market-supervisory-authorities-in-europe)
- **Emisor:** CONSOB (Italia)
- **Temática:** TFB-03 Reguladores, registros y documentación corporativa (principal) · secundarias: —
- **Calidad Q:** 85 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Mercados de valores italianos: participaciones relevantes, información regulada de emisores, sanciones; directorio de las autoridades nacionales europeas con enlace a sus registros de entidades autorizadas
- **Motivo de inclusión y uso:** Regulador de Borsa Italiana. Su directorio (actualizado el 30/03/2026) da, por país, la web en inglés y el registro de entidades autorizadas de cada supervisor de la UE, el EEE, Suiza y el Reino Unido. Uso: hechos de emisores italianos y punto de entrada a los registros europeos.
- **Sesgos y cautelas:** El directorio enlaza erróneamente a la CNMV en la fila de Suecia (comprobado el 2/11/2026) y no garantiza la vigencia de los enlaces.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Uso en el bloque:** AG-B12: participaciones relevantes y documentación de emisores italianos; AG-B07: regulación del mercado italiano.
- **Origen:** Reutilizada con su ID de F9 V3.2 (Bloque A general); temática reasignada a TFB-03 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «list of financial regulatory authorities by country wikipedia»; WebFetch: sí)

#### MBF-0019 · Q 84 (A) — ESMA — European Single Access Point (ESAP)

- **Canal oficial (URL raíz):** https://www.esma.europa.eu/press-news/esma-news/esma-launches-data-collection-under-first-phase-esap
- **Emisor:** European Securities and Markets Authority (ESMA)
- **Documentación y notas:** Plataforma centralizada de la UE para información financiera y de sostenibilidad de entidades y productos. Desde el 10/07/2026 los organismos de recogida (OAM y autoridades nacionales) remiten información de la Directiva de Transparencia, el Reglamento de Folletos y el Reglamento de Ventas en Corto; acceso público previsto para julio de 2027.
- **Temática:** TFB-03 Reguladores, registros y documentación corporativa (principal) · secundarias: TFB-07
- **Calidad Q:** 84 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 6/10
- **Tipología:** primaria
- **Acceso:** Abierto y gratuito (cuando abra al público, julio de 2027)
- **Ámbitos:** Informes financieros regulados, folletos, información de sostenibilidad de emisores de la UE
- **Motivo de inclusión y uso:** Será el punto único de documentación corporativa europea comparable para la criba de emisores.
- **Restricciones de uso:** Condiciones de reutilización de ESMA.
- **Sesgos y cautelas:** Aún no accesible al público; cobertura por fases.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** En implantación (fase 1 desde julio de 2026).
- **Uso en el bloque:** AG-B12: documentación de emisores europeos para la criba de activos; AG-B09: estados financieros comparables; AG-B11: información de sostenibilidad.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-03 (búsqueda web: «European Single Access Point ESAP ESMA go-live 2026 corporate disclosures»; WebFetch: sí)
- **Origen:** Alta 2026-11-03 (F9 Bloque B V2.0, TFB-03).

#### MBF-0030 · Q 83 (A) — Companies Registration Office (CRO, Irlanda)

- **Canal oficial (URL raíz):** Índice: https://en.wikipedia.org/wiki/List_of_official_business_registers (artículo «Companies Registration Office (Ireland)»); también https://opencorporates.com/registers/118
- **Emisor:** Companies Registration Office (Irlanda)
- **Documentación y notas:** Registro mercantil irlandés (CORE); relevante por la domiciliación en Irlanda de filiales de multinacionales tecnológicas y farmacéuticas. URL oficial no mostrada en la página índice.
- **Temática:** TFB-03 Reguladores, registros y documentación corporativa (principal) · secundarias: —
- **Calidad Q:** 83 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Búsqueda básica gratuita; documentos con tasa
- **Ámbitos:** Empresas irlandesas: inscripciones, cuentas
- **Motivo de inclusión y uso:** Cuentas de filiales europeas de multinacionales domiciliadas en Irlanda.
- **Restricciones de uso:** Condiciones del registro.
- **Sesgos y cautelas:** Cuentas con exenciones para grupos.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B12 y AG-B09: filiales irlandesas de multinacionales (ingresos por región, fiscalidad); AG-B07: contexto regulatorio y fiscal.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Wikipedia list of company registers by country»; WebFetch: sí, página índice)
- **Origen:** Alta 2026-11-02 (F9 Bloque B V2.0, TFB-03).

#### MBF-0031 · Q 83 (A) — Luxembourg Business Registers (RCS Luxemburgo)

- **Canal oficial (URL raíz):** Índice: https://en.wikipedia.org/wiki/List_of_official_business_registers
- **Emisor:** Luxembourg Business Registers
- **Documentación y notas:** Registre de Commerce et des Sociétés de Luxemburgo; relevante para holdings, vehículos de financiación y fondos. URL oficial no mostrada en la página índice.
- **Temática:** TFB-03 Reguladores, registros y documentación corporativa (principal) · secundarias: —
- **Calidad Q:** 83 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Consulta básica gratuita
- **Ámbitos:** Sociedades luxemburguesas, vehículos de financiación
- **Motivo de inclusión y uso:** Verificación de emisores de bonos y vehículos domiciliados en Luxemburgo.
- **Restricciones de uso:** Condiciones del registro.
- **Sesgos y cautelas:** Estructuras complejas; información limitada sobre beneficiarios.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B12: verificación de emisores y vehículos de financiación (bonos, titulizaciones).
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Wikipedia list of company registers by country»; WebFetch: sí, página índice)
- **Origen:** Alta 2026-11-02 (F9 Bloque B V2.0, TFB-03).

#### RF-0212 · Q 83 (A) — Securities and Futures Commission (SFC, Hong Kong)

- **Canal oficial (URL raíz):** https://www.sfc.hk/ (página IOSCO MMoU: https://www.sfc.hk/web/EN/about-the-sfc/collaboration/overseas/iosco-mmou.html)
- **Emisor:** Securities and Futures Commission of Hong Kong
- **Temática:** TFB-03 Reguladores, registros y documentación corporativa (principal) · secundarias: —
- **Calidad Q:** 83 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 14/15 · Independencia 8/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Supervisión de valores y futuros de Hong Kong; registro público de intermediarios; acciones de enforcement; cooperación internacional (IOSCO MMoU)
- **Motivo de inclusión y uso:** Regulador del principal mercado de acceso a renta variable china fuera del continente. Uso: hechos regulatorios y sancionadores de Hong Kong.
- **Sesgos y cautelas:** Contexto político de Hong Kong; cobertura limitada a su jurisdicción.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Uso en el bloque:** AG-B07 y AG-B12: regulación y registros de Hong Kong (acceso a emisores chinos y asiáticos).
- **Origen:** Reutilizada con su ID de F9 V3.2 (Bloque A general); temática reasignada a TFB-03 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «list of financial regulatory authorities by country wikipedia»; WebFetch: sí)

#### MBF-0026 · Q 82 (A) — Unternehmensregister y Handelsregister (Alemania)

- **Canal oficial (URL raíz):** Índice: https://en.wikipedia.org/wiki/List_of_official_business_registers (artículos «Business Register System» y «German Commercial Register»)
- **Emisor:** Bundesanzeiger Verlag / Länder (registro mercantil alemán)
- **Documentación y notas:** El Unternehmensregister centraliza la publicación de cuentas anuales e información de empresas alemanas; el Handelsregister es el registro mercantil. URL oficial no mostrada en la página índice.
- **Temática:** TFB-03 Reguladores, registros y documentación corporativa (principal) · secundarias: TFB-07
- **Calidad Q:** 82 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 7/10
- **Tipología:** primaria
- **Acceso:** Consulta básica gratuita; algunos documentos con tasa
- **Ámbitos:** Empresas alemanas: inscripciones, cuentas anuales publicadas
- **Motivo de inclusión y uso:** Cuentas de empresas alemanas no cotizadas (Mittelstand) para análisis competitivo.
- **Restricciones de uso:** Condiciones del registro.
- **Sesgos y cautelas:** Cuentas abreviadas para pymes; desfase de publicación.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B03 y AG-B09: cuentas de competidores no cotizados alemanes; AG-B12: verificación de entidades.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Wikipedia list of company registers by country»; WebFetch: sí, página índice)
- **Origen:** Alta 2026-11-02 (F9 Bloque B V2.0, TFB-03).

#### MBF-0027 · Q 82 (A) — Registre du commerce et des sociétés (RCS) — Infogreffe (Francia)

- **Canal oficial (URL raíz):** Índice: https://en.wikipedia.org/wiki/List_of_official_business_registers
- **Emisor:** Greffes des tribunaux de commerce (Francia)
- **Documentación y notas:** Registro mercantil francés difundido por Infogreffe; datos de identificación complementarios en el repertorio SIRENE del INSEE (MBF-0003). URL oficial no mostrada en la página índice.
- **Temática:** TFB-03 Reguladores, registros y documentación corporativa (principal) · secundarias: —
- **Calidad Q:** 82 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 7/10
- **Tipología:** primaria
- **Acceso:** Consulta básica gratuita; extractos y cuentas con tasa
- **Ámbitos:** Empresas francesas: inscripciones, cuentas depositadas
- **Motivo de inclusión y uso:** Fuente primaria de entidades francesas y sus cuentas.
- **Restricciones de uso:** Condiciones del registro.
- **Sesgos y cautelas:** Las empresas pueden solicitar confidencialidad de cuentas.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B03 y AG-B12: entidades y cuentas de empresas francesas.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Wikipedia list of company registers by country»; WebFetch: sí, página índice)
- **Origen:** Alta 2026-11-02 (F9 Bloque B V2.0, TFB-03).

#### MBF-0029 · Q 82 (A) — Kamer van Koophandel (KvK) — Handelsregister (Países Bajos)

- **Canal oficial (URL raíz):** https://kvk.nl/en/about-the-business-register/european-business-registers
- **Emisor:** Kamer van Koophandel (Países Bajos)
- **Documentación y notas:** Registro mercantil neerlandés; página de la KvK sobre registros mercantiles europeos. Confirmada también en https://en.wikipedia.org/wiki/List_of_official_business_registers.
- **Temática:** TFB-03 Reguladores, registros y documentación corporativa (principal) · secundarias: —
- **Calidad Q:** 82 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 7/10
- **Tipología:** primaria
- **Acceso:** Consulta básica gratuita; extractos con tasa
- **Ámbitos:** Empresas neerlandesas (incluidas sociedades holding de grupos internacionales)
- **Motivo de inclusión y uso:** Muchas estructuras de grupo europeas tienen holdings en los Países Bajos.
- **Restricciones de uso:** Condiciones del registro.
- **Sesgos y cautelas:** Extractos y cuentas con tasa.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B12: verificación de holdings y filiales neerlandesas; AG-B03: estructuras de grupo.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Wikipedia list of company registers by country»; WebFetch: sí, página índice)
- **Origen:** Alta 2026-11-02 (F9 Bloque B V2.0, TFB-03).

#### MBF-0028 · Q 81 (A) — Registro delle imprese — InfoCamere (Italia)

- **Canal oficial (URL raíz):** Índice: https://en.wikipedia.org/wiki/List_of_official_business_registers (artículo «European Business Register»)
- **Emisor:** Cámaras de comercio italianas / InfoCamere
- **Documentación y notas:** Registro mercantil italiano gestionado por las cámaras de comercio a través de InfoCamere (y portal Infoimprese). URL oficial no mostrada en la página índice.
- **Temática:** TFB-03 Reguladores, registros y documentación corporativa (principal) · secundarias: —
- **Calidad Q:** 81 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 6/10
- **Tipología:** primaria
- **Acceso:** Consulta básica gratuita; documentos con tasa
- **Ámbitos:** Empresas italianas: inscripciones, balances
- **Motivo de inclusión y uso:** Fuente primaria de entidades italianas.
- **Restricciones de uso:** Condiciones del registro.
- **Sesgos y cautelas:** Acceso a balances con tasa.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B03 y AG-B12: entidades y balances de empresas italianas.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Wikipedia list of company registers by country»; WebFetch: sí, página índice)
- **Origen:** Alta 2026-11-02 (F9 Bloque B V2.0, TFB-03).

#### MBF-0023 · Q 78 (B) — Comisión Europea (e-Justice) — Business registers in EU countries

- **Canal oficial (URL raíz):** https://webgate.ec.europa.eu/e-justice/106/EN/business_registers_in_eu_countries
- **Emisor:** Comisión Europea — Portal Europeo de e-Justicia
- **Documentación y notas:** Directorio de registros mercantiles de los Estados miembros (más Islandia, Liechtenstein y Noruega), con fichas por país; describe los servicios básicos comunes (registrar, examinar, almacenar y publicar información de empresas). Última actualización de la página: 03/10/2022.
- **Temática:** TFB-03 Reguladores, registros y documentación corporativa (principal) · secundarias: —
- **Calidad Q:** 78 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 6/10 · Acceso 10/10
- **Tipología:** primaria (directorio oficial)
- **Acceso:** Abierto
- **Ámbitos:** Registros mercantiles nacionales del EEE e interconexión BRIS
- **Motivo de inclusión y uso:** Directorio oficial para llegar al registro mercantil de cualquier país del EEE.
- **Restricciones de uso:** Condiciones del portal e-Justicia.
- **Sesgos y cautelas:** Página poco actualizada; los servicios y tarifas varían por país.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B12 y AG-B03: acceso a registros oficiales para verificar entidades y cuentas en Europa.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Wikipedia list of company registers by country»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9 Bloque B V2.0, TFB-03).

#### MBF-0025 · Q 76 (B) — Companies House — Overseas registries (registros mercantiles de otros países)

- **Canal oficial (URL raíz):** https://www.gov.uk/government/publications/overseas-registries
- **Emisor:** Companies House (Gobierno del Reino Unido)
- **Documentación y notas:** Publicación oficial con el listado de registros mercantiles de otros países y territorios.
- **Temática:** TFB-03 Reguladores, registros y documentación corporativa (principal) · secundarias: —
- **Calidad Q:** 76 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 14/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** terciaria (directorio oficial)
- **Acceso:** Abierto
- **Ámbitos:** Registros mercantiles mundiales
- **Motivo de inclusión y uso:** Directorio oficial de alcance mundial que complementa el directorio europeo (MBF-0023).
- **Restricciones de uso:** Open Government Licence.
- **Sesgos y cautelas:** Puede quedar desfasado en algunos enlaces.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B12: acceso a registros de jurisdicciones fuera del EEE.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Wikipedia list of company registers by country»; WebFetch: no)
- **Origen:** Alta 2026-11-02 (F9 Bloque B V2.0, TFB-03).

#### MBF-0022 · Q 71 (B) — OpenCorporates — índice de registros mercantiles

- **Canal oficial (URL raíz):** https://opencorporates.com/registers
- **Emisor:** OpenCorporates Ltd
- **Documentación y notas:** Base abierta de empresas que agrega registros oficiales de más de 145 jurisdicciones y unos 245 millones de empresas; cada registro con recuento de empresas y directivos y puntuación de apertura.
- **Temática:** TFB-03 Reguladores, registros y documentación corporativa (principal) · secundarias: TFB-07
- **Calidad Q:** 71 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 11/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** secundaria (agregador de registros oficiales)
- **Acceso:** Abierto en web; API y usos comerciales con condiciones
- **Ámbitos:** Empresas y directivos por jurisdicción
- **Motivo de inclusión y uso:** Punto de partida para localizar entidades en registros de muchos países y enlazar con la fuente oficial.
- **Restricciones de uso:** Licencia de OpenCorporates (atribución y compartir igual); citar el registro original.
- **Sesgos y cautelas:** Desfase respecto al registro oficial; cobertura desigual.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B12: localizar filiales, proveedores y competidores no cotizados; AG-B03: mapa de actores de un sector.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Wikipedia list of company registers by country»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9 Bloque B V2.0, TFB-03).

#### MBF-0024 · Q 68 (B) — ICAEW Library — Company information: sources by jurisdiction

- **Canal oficial (URL raíz):** https://icaew.com/library/research-guides/company-information/sources-by-jurisdiction
- **Emisor:** ICAEW (Institute of Chartered Accountants in England and Wales)
- **Documentación y notas:** Guía de investigación de la biblioteca del ICAEW con fuentes de información de empresas por jurisdicción (registros, bases de datos). Complemento: «Knowledge guide to international company registration».
- **Temática:** TFB-03 Reguladores, registros y documentación corporativa (principal) · secundarias: —
- **Calidad Q:** 68 (B) — Primariedad 8/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 12/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 8/10
- **Tipología:** terciaria (guía de fuentes)
- **Acceso:** Abierto (parte de los recursos enlazados es de pago)
- **Ámbitos:** Fuentes de información corporativa por país
- **Motivo de inclusión y uso:** Índice cualificado para localizar registros y fuentes corporativas fuera de la UE.
- **Restricciones de uso:** Cita de la guía.
- **Sesgos y cautelas:** Guía de biblioteca: mantenimiento irregular.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B12 y BFA (AG-B20): localizar registros de jurisdicciones menos habituales.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Wikipedia list of company registers by country»; WebFetch: no)
- **Origen:** Alta 2026-11-02 (F9 Bloque B V2.0, TFB-03).

## TFB-04 Asociaciones sectoriales y datos de industria

#### RF-0319 · Q 83 (A) — Institute for Supply Management — ISM Report On Business

- **Canal oficial (URL raíz):** https://ismworld.org/supply-management-news-and-reports/reports/ism-report-on-business
- **Emisor:** Institute for Supply Management (ISM)
- **Documentación y notas:** PMI manufacturero (1.er día hábil del mes), servicios (3.er día hábil) y hospitalario (5.º día hábil), a las 10:00 EST; comités de encuesta con representación proporcional al PIB sectorial; calendario y notas sobre ajustes estacionales anuales.
- **Temática:** TFB-04 Asociaciones sectoriales y datos de industria (principal) · secundarias: TFB-02
- **Calidad Q:** 83 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 10/10 · Acceso 7/10
- **Tipología:** primaria
- **Acceso:** Abierto (titulares); detalle completo en ismworld.org
- **Ámbitos:** Actividad manufacturera y de servicios de EE. UU. por sector
- **Motivo de inclusión y uso:** Encuesta de referencia del ciclo industrial estadounidense; catalizador de calendario.
- **Restricciones de uso:** Condiciones de ISM; citar informe y mes.
- **Sesgos y cautelas:** Encuesta de opinión de compras; revisiones estacionales anuales.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B08: ciclo manufacturero y de servicios de EE. UU. con comentarios por industria; AG-B05: plazos de entrega y precios de insumos.
- **Origen:** Reutilizada con su ID de F9 V3.2 (Bloque A general); temática reasignada a TFB-04 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ismworld.org Report On Business Manufacturing PMI Services PMI»; WebFetch: sí)

#### RF-0318 · Q 82 (A) — S&P Global — PMI (HCOB Eurozona y otros países)

- **Canal oficial (URL raíz):** https://www.pmi.spglobal.com/Public/Home/PressRelease/0fe4c657a20b4c469a65bd2aaae141d5
- **Emisor:** S&P Global Market Intelligence (patrocinio HCOB en la eurozona)
- **Documentación y notas:** Notas de prensa PMI con metodología: encuesta mensual (segunda quincena), índices de difusión desestacionalizados; PMI manufacturero = pedidos 30 %, producción 25 %, empleo 20 %, plazos de proveedores 15 % (invertido), existencias 10 %; ponderación por país según valor añadido de Eurostat; avance (flash) con ~89 % de respuestas. Página de producto: spglobal.com/marketintelligence/en/mi/products/pmi.html.
- **Temática:** TFB-04 Asociaciones sectoriales y datos de industria (principal) · secundarias: TFB-02
- **Calidad Q:** 82 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 14/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (notas de titulares); series completas de pago
- **Ámbitos:** PMI manufacturero, servicios y compuesto por país y sector
- **Motivo de inclusión y uso:** Indicador adelantado del ciclo industrial y de servicios con avance flash a final de mes.
- **Restricciones de uso:** Condiciones de S&P Global; citar país, sector y mes (flash o final).
- **Sesgos y cautelas:** Proveedor comercial; datos detallados de pago; ajuste estacional revisable.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Patrocinadores nacionales cambian (p. ej., HCOB en la eurozona).
- **Uso en el bloque:** AG-B08: PMI por país y sector (incluidos PMI sectoriales globales) como indicador adelantado del ciclo; AG-B05: presiones en la cadena de suministro.
- **Origen:** Reutilizada con su ID de F9 V3.2 (Bloque A general); temática reasignada a TFB-04 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ISM Report On Business Manufacturing PMI S&P Global PMI HCOB eurozone»; WebFetch: sí)

#### RF-0350 · Q 81 (A) — SIPRI — base de datos de la industria de armamento (Top 100)

- **Canal oficial (URL raíz):** https://sipri.org/databases/armsindustry
- **Emisor:** Stockholm International Peace Research Institute (SIPRI)
- **Documentación y notas:** Ventas de armamento de las 100 principales empresas (Excel 2002–2024), con fuentes abiertas (informes anuales, prensa) y estimaciones; revisión anual de toda la serie; uso comercial con licencia.
- **Temática:** TFB-04 Asociaciones sectoriales y datos de industria (principal) · secundarias: TFB-16
- **Calidad Q:** 81 (A) — Primariedad 16/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 7/10 · Acceso 9/10
- **Tipología:** secundaria
- **Acceso:** Abierto (uso no comercial)
- **Ámbitos:** Industria de defensa: ingresos por armamento por empresa y país
- **Motivo de inclusión y uso:** Referencia para el ciclo de gasto en defensa y sus beneficiarios cotizados.
- **Restricciones de uso:** Términos de SIPRI; uso comercial con autorización.
- **Sesgos y cautelas:** Estimaciones a partir de fuentes abiertas; cobertura limitada de China y Rusia.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Rusia desde 2002 y China parcial desde 2015.
- **Uso en el bloque:** AG-B03 y AG-B12: ranking de ventas de armamento por empresa (estructura y criba del sector defensa); AG-B07: contexto geopolítico.
- **Origen:** Reutilizada con su ID de F9 V3.2 (Bloque A general); temática reasignada a TFB-04 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «SIPRI Top 100 arms-producing companies arms industry database»; WebFetch: sí)

#### RF-0320 · Q 79 (B) — worldsteel — producción mundial de acero

- **Canal oficial (URL raíz):** https://worldsteel.org/media/press-releases
- **Emisor:** World Steel Association (worldsteel)
- **Documentación y notas:** Nota mensual de producción de acero bruto (70 países; septiembre de 2026: 142,4 Mt, −0,2 % interanual, publicada el 23/10/2026); World Steel in Figures (junio) y Short Range Outlook de demanda (abril y octubre).
- **Temática:** TFB-04 Asociaciones sectoriales y datos de industria (principal) · secundarias: TFB-12
- **Calidad Q:** 79 (B) — Primariedad 18/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 14/15 · Independencia 7/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Producción de acero por país; demanda prevista
- **Motivo de inclusión y uso:** Termómetro de construcción, automóvil y maquinaria; demanda de mineral de hierro y carbón.
- **Restricciones de uso:** Citar mes y nota.
- **Sesgos y cautelas:** Asociación sectorial; datos de algunos países estimados.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B05: producción mundial de acero por país (capacidad y oferta); AG-B08: ciclo industrial; AG-B12: siderúrgicas.
- **Origen:** Reutilizada con su ID de F9 V3.2 (Bloque A general); temática reasignada a TFB-04 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «worldsteel monthly crude steel production press release»; WebFetch: sí)

#### RF-0325 · Q 79 (B) — ONU Turismo (UN Tourism, antes UNWTO) — barómetro y estadísticas de turismo

- **Canal oficial (URL raíz):** https://www.untourism.int/
- **Emisor:** Organización Mundial del Turismo de las Naciones Unidas (ONU Turismo)
- **Documentación y notas:** Organismo de la ONU que publica el World Tourism Barometer y estadísticas de llegadas internacionales; dominio untourism.int (el anterior unwto.org sigue apareciendo en resultados).
- **Temática:** TFB-04 Asociaciones sectoriales y datos de industria (principal) · secundarias: —
- **Calidad Q:** 79 (B) — Primariedad 18/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 7/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (parcial)
- **Ámbitos:** Llegadas e ingresos por turismo internacional
- **Motivo de inclusión y uso:** Indicador de demanda turística (relevante para España).
- **Restricciones de uso:** Citar edición y periodo.
- **Sesgos y cautelas:** Frecuencia baja; estimaciones provisionales.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Cambio de denominación UNWTO → UN Tourism.
- **Uso en el bloque:** AG-B04: llegadas e ingresos de turismo internacional por región para hoteles, ocio, viajes y aerolíneas.
- **Origen:** Reutilizada con su ID de F9 V3.2 (Bloque A general); temática reasignada a TFB-04 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «IATA air passenger market analysis monthly UN Tourism World Tourism Barometer»; WebFetch: intentado, error del sitio)

#### MBF-0032 · Q 78 (B) — Cefic — Chemical Trends Report (trimestral) y Facts & Figures

- **Canal oficial (URL raíz):** https://cefic.org//app/uploads/2026/06/Chemical-Trends-Report-Q1-2026.pdf
- **Emisor:** Cefic (European Chemical Industry Council)
- **Documentación y notas:** Informe trimestral de indicadores del sector químico de la UE-27 (producción, comercio, precios, costes energéticos); el informe del 1T 2026 se publicó el 23/07/2026 (reseñado en transition-pathways.europa.eu). Informe anual Facts & Figures (edición 2025 reseñada en el mismo portal de la Comisión). Datos interactivos en iris.cefic.org.
- **Temática:** TFB-04 Asociaciones sectoriales y datos de industria (principal) · secundarias: TFB-12
- **Calidad Q:** 78 (B) — Primariedad 17/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 14/15 · Independencia 6/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** primaria (asociación sectorial)
- **Acceso:** Abierto
- **Ámbitos:** Química europea: producción, utilización, comercio, precios, energía
- **Motivo de inclusión y uso:** Termómetro del sector químico europeo y de su competitividad por costes energéticos.
- **Restricciones de uso:** Cita del informe y trimestre.
- **Sesgos y cautelas:** Asociación sectorial con agenda de política (energía, regulación).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B04 y AG-B05: demanda, producción y comercio químicos; AG-B07: impacto regulatorio y energético; AG-B12: criba de químicas europeas.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-03 (búsqueda web: «Cefic Facts and Figures European chemical industry 2026 Chemical Monthly Report»; WebFetch: sí, reseña de la Comisión Europea)
- **Origen:** Alta 2026-11-03 (F9 Bloque B V2.0, TFB-04).

#### MBF-0034 · Q 78 (B) — EFPIA — The Pharmaceutical Industry in Figures

- **Canal oficial (URL raíz):** https://www.efpia.eu/media/owqczcqz/the-pharmaceutical-industry-in-figures-2026.pdf
- **Emisor:** EFPIA (European Federation of Pharmaceutical Industries and Associations)
- **Documentación y notas:** Publicación anual con producción, empleo, I+D, comercio exterior y mercado farmacéutico por país europeo (ediciones 2024 y 2026 devueltas por la búsqueda).
- **Temática:** TFB-04 Asociaciones sectoriales y datos de industria (principal) · secundarias: —
- **Calidad Q:** 78 (B) — Primariedad 17/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 14/15 · Independencia 6/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** primaria (asociación sectorial)
- **Acceso:** Abierto (PDF)
- **Ámbitos:** Industria farmacéutica europea: producción, I+D, empleo, comercio, mercado
- **Motivo de inclusión y uso:** Datos sectoriales armonizados de la farmacia europea.
- **Restricciones de uso:** Cita de la edición.
- **Sesgos y cautelas:** Asociación sectorial con agenda de precios y propiedad intelectual.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B04: tamaño del mercado farmacéutico por país; AG-B06: intensidad de I+D; AG-B12: criba de farmacéuticas europeas.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-03 (búsqueda web: «EFPIA pharmaceutical industry in figures 2026 EUROFER European steel market outlook CEMBUREAU activity report»; WebFetch: no)
- **Origen:** Alta 2026-11-03 (F9 Bloque B V2.0, TFB-04).

#### RF-0303 · Q 77 (B) — ACEA — estadísticas del automóvil en Europa

- **Canal oficial (URL raíz):** https://www.acea.auto/reliable-data-statistics/
- **Emisor:** European Automobile Manufacturers' Association (ACEA)
- **Documentación y notas:** Notas de prensa mensuales de matriculaciones de turismos (por país, combustible y fabricante) y trimestrales de vehículos comerciales; calendario anual de publicación; series de producción, comercio, parque, empleo y fiscalidad. Directorio de asociaciones nacionales: acea.auto/national-automobile-associations/. Datos avanzados en ACEA Intelligence (servicio aparte).
- **Temática:** TFB-04 Asociaciones sectoriales y datos de industria (principal) · secundarias: —
- **Calidad Q:** 77 (B) — Primariedad 17/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 14/15 · Independencia 6/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto (notas y series públicas); servicio avanzado aparte
- **Ámbitos:** Matriculaciones UE/EFTA/Reino Unido, cuota de vehículo eléctrico, producción
- **Motivo de inclusión y uso:** Indicador mensual de demanda de automóviles y de transición a eléctrico en Europa.
- **Restricciones de uso:** Citar nota de prensa y mes.
- **Sesgos y cautelas:** Asociación sectorial (agenda de lobby).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B04: demanda de automóviles y adopción del vehículo eléctrico en Europa; AG-B03: cuotas por fabricante; AG-B12: criba de fabricantes y proveedores.
- **Origen:** Reutilizada con su ID de F9 V3.2 (Bloque A general); temática reasignada a TFB-04 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «OICA ACEA ANFAC vehicle production registrations statistics official»; WebFetch: sí)

#### RF-0057 · Q 76 (B) — Semiconductor Industry Association (SIA) y WSTS

- **Canal oficial (URL raíz):** https://www.semiconductors.org/
- **Emisor:** Semiconductor Industry Association (SIA); datos de World Semiconductor Trade Statistics (WSTS, https://www.wsts.org/)
- **Documentación y notas:** Nota mensual «Global Semiconductor Sales…» con ventas mundiales (media móvil de 3 meses compilada por WSTS) y desglose regional; SIA Databook (histórico) y paquete de suscripción WSTS (datos mensuales y previsiones) enlazados desde las notas.
- **Temática:** TFB-04 Asociaciones sectoriales y datos de industria (principal) · secundarias: TFB-09
- **Calidad Q:** 76 (B) — Primariedad 17/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 13/15 · Independencia 6/10 · Actualidad 8/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto (notas mensuales); datos detallados de pago
- **Ámbitos:** Ventas mensuales de semiconductores por región; previsiones WSTS
- **Motivo de inclusión y uso:** Indicador sectorial adelantado del ciclo tecnológico.
- **Restricciones de uso:** Citar mes de referencia y que es media móvil de 3 meses.
- **Sesgos y cautelas:** Asociación sectorial (sesgo promocional); desfase de unas 5 semanas.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B04 y AG-B08: ciclo de ventas de semiconductores por región; AG-B05: oferta de chips; AG-B13: previsiones WSTS.
- **Origen:** Reutilizada con su ID de F9 V3.2 (Bloque A general); temática reasignada a TFB-04 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Semiconductor Industry Association global semiconductor sales WSTS monthly»; WebFetch: sí, nota de prensa mensual)

#### RF-0324 · Q 76 (B) — IATA — análisis de mercado de pasajeros y carga aérea

- **Canal oficial (URL raíz):** https://www.iata.org/en/publications/economics/economics-library/?page=25
- **Emisor:** International Air Transport Association (IATA)
- **Documentación y notas:** Biblioteca económica (1.963 informes desde 2005): Air Passenger Market Analysis y Air Cargo Market Analysis mensuales, Chart of the Week, Quarterly Air Transport Chartbook, Global Outlook for Air Transport semestral, Airlines Financial Monitor.
- **Temática:** TFB-04 Asociaciones sectoriales y datos de industria (principal) · secundarias: TFB-05
- **Calidad Q:** 76 (B) — Primariedad 17/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 14/15 · Independencia 6/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (la mayoría de informes)
- **Ámbitos:** Tráfico aéreo de pasajeros (RPK, ASK) y carga; resultados del sector
- **Motivo de inclusión y uso:** Indicador mensual de viajes y comercio aéreo.
- **Restricciones de uso:** Citar informe y mes.
- **Sesgos y cautelas:** Asociación de aerolíneas (sesgo sectorial).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B04: tráfico aéreo de pasajeros y carga; AG-B09: rentabilidad del sector aerolíneas; AG-B12: aerolíneas, aeropuertos y fabricantes.
- **Origen:** Reutilizada con su ID de F9 V3.2 (Bloque A general); temática reasignada a TFB-04 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «IATA air passenger market analysis monthly UN Tourism World Tourism Barometer»; WebFetch: sí)

#### MBF-0033 · Q 75 (B) — EUROFER — Economic and Steel Market Outlook (trimestral)

- **Canal oficial (URL raíz):** https://www.eurofer.eu/publications/economic-market-outlook
- **Emisor:** EUROFER (European Steel Association)
- **Documentación y notas:** Perspectivas trimestrales del mercado europeo del acero (última: 2026-2027, tercer trimestre, septiembre de 2026), con enlaces a estadísticas de consumo aparente, sectores usuarios e importaciones.
- **Temática:** TFB-04 Asociaciones sectoriales y datos de industria (principal) · secundarias: TFB-12
- **Calidad Q:** 75 (B) — Primariedad 17/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 14/15 · Independencia 6/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria (asociación sectorial)
- **Acceso:** Abierto (con aceptación de condiciones del sitio)
- **Ámbitos:** Acero en la UE: consumo aparente, sectores usuarios, importaciones, utilización de capacidad
- **Motivo de inclusión y uso:** Fuente sectorial de referencia para la demanda europea de acero y la presión importadora.
- **Restricciones de uso:** Cita del informe y trimestre.
- **Sesgos y cautelas:** Asociación sectorial con agenda de defensa comercial.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B04 y AG-B05: demanda y capacidad de acero en Europa; AG-B07: medidas de defensa comercial; AG-B12: siderúrgicas europeas.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-03 (búsqueda web: «EFPIA pharmaceutical industry in figures 2026 EUROFER European steel market outlook CEMBUREAU activity report»; WebFetch: sí)
- **Origen:** Alta 2026-11-03 (F9 Bloque B V2.0, TFB-04).

#### MBF-0035 · Q 75 (B) — IFPI — Global Music Report

- **Canal oficial (URL raíz):** https://www.ifpi.org/global-music-report-2026-global-recorded-music-revenues-grow-6-4-as-record-companies-drive-innovation/
- **Emisor:** IFPI (International Federation of the Phonographic Industry)
- **Documentación y notas:** Informe anual de ingresos mundiales de música grabada: 2025 = 31.700 M USD (+6,4 %, undécimo año de crecimiento), streaming 69,6 % del mercado, 837 millones de cuentas de pago; crecimiento por región. Publicado el 18/03/2026; edición «Premium» con el detalle.
- **Temática:** TFB-04 Asociaciones sectoriales y datos de industria (principal) · secundarias: —
- **Calidad Q:** 75 (B) — Primariedad 18/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 14/15 · Independencia 6/10 · Actualidad 10/10 · Acceso 6/10
- **Tipología:** primaria (asociación sectorial)
- **Acceso:** Resumen abierto; edición Premium de pago
- **Ámbitos:** Música grabada: ingresos por formato y región, suscripciones
- **Motivo de inclusión y uso:** Dimensionado del mercado de música grabada y del streaming.
- **Restricciones de uso:** Cita del informe y año.
- **Sesgos y cautelas:** Representa a discográficas: sesgo sectorial.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B04: dimensionado y crecimiento del mercado musical por región; AG-B03: peso del streaming; AG-B12: discográficas y plataformas.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-03 (búsqueda web: «IFPI Global Music Report 2026 recorded music revenues streaming»; WebFetch: sí)
- **Origen:** Alta 2026-11-03 (F9 Bloque B V2.0, TFB-04).

#### MBF-0619 · Q 75 (B) — Association of American Railroads (AAR) — tráfico ferroviario semanal (cargas por mercancía e intermodal)

- **Canal oficial (URL raíz):** https://www.railwayage.com/freight/class-i/aar-intermodal-lifts-u-s-weekly-rail-traffic-in-week-30/ (nota semanal de la AAR reproducida por Railway Age; emisor: aar.org)
- **Emisor:** Association of American Railroads (AAR)
- **Documentación y notas:** Informe semanal de tráfico de mercancías por ferrocarril: vagones cargados en EE. UU. por 10 grupos de mercancías (carbón, químicos, vehículos y piezas, cereales…), unidades intermodales (contenedores y remolques), acumulado anual y datos de Canadá, México y Norteamérica (nueve ferrocarriles). Ejemplo: semana 30 de 2026, 526.410 unidades en EE. UU. (+2,4 % interanual).
- **Temática:** TFB-04 Asociaciones sectoriales y datos de industria (principal) · secundarias: TFB-05, TFB-02
- **Calidad Q:** 75 (B) — Primariedad 17/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 13/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 8/10
- **Tipología:** primaria (agregado de la industria)
- **Acceso:** Abierto (notas semanales); series detalladas para socios
- **Ámbitos:** Actividad de transporte ferroviario de mercancías en Norteamérica
- **Motivo de inclusión y uso:** Indicador semanal de alta frecuencia de la actividad industrial y del consumo de bienes por mercancía.
- **Restricciones de uso:** Condiciones de la AAR; citar semana.
- **Sesgos y cautelas:** URL de un medio que reproduce la nota (raíz aar.org no leída); cambios de cuota modal afectan a la lectura cíclica.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B08 Macro y Ciclo: actividad industrial semanal por mercancía; AG-B05 Oferta y Cadena de Suministro: flujos intermodales (importaciones); AG-B04: demanda de químicos, automóviles y materiales.
- **Origen:** Alta F9_comp (2026-11-03).
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-03 (búsqueda web: «Association of American Railroads weekly rail traffic data carloads intermodal»; WebFetch: sí, nota de Railway Age)

#### RF-0305 · Q 75 (B) — ANFAC — matriculaciones y producción en España

- **Canal oficial (URL raíz):** https://www.anfac.com/
- **Emisor:** Asociación Española de Fabricantes de Automóviles y Camiones (ANFAC)
- **Documentación y notas:** Asociación nacional española miembro de ACEA (listada en el directorio oficial de ACEA). Publica matriculaciones mensuales y datos de producción de vehículos en España.
- **Temática:** TFB-04 Asociaciones sectoriales y datos de industria (principal) · secundarias: —
- **Calidad Q:** 75 (B) — Primariedad 17/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 13/15 · Independencia 6/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto (notas de prensa)
- **Ámbitos:** Mercado y producción de automóviles en España
- **Motivo de inclusión y uso:** Fuente sectorial española para consumo duradero e industria del automóvil.
- **Restricciones de uso:** Citar nota y mes.
- **Sesgos y cautelas:** Asociación sectorial. Productos concretos no leídos directamente: confirmar en el próximo barrido.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B04: matriculaciones y producción del automóvil en España (mercado geográfico doméstico).
- **Origen:** Reutilizada con su ID de F9 V3.2 (Bloque A general); temática reasignada a TFB-04 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «OICA ACEA ANFAC vehicle production registrations statistics official»; URL tomada del directorio de asociaciones nacionales de ACEA leído con WebFetch; WebFetch al sitio: no)

#### RF-0306 · Q 75 (B) — SMMT — matriculaciones y producción en el Reino Unido

- **Canal oficial (URL raíz):** https://www.smmt.co.uk/
- **Emisor:** Society of Motor Manufacturers and Traders (SMMT)
- **Documentación y notas:** Asociación nacional británica listada en el directorio oficial de ACEA; referencia de matriculaciones mensuales y producción de vehículos en el Reino Unido.
- **Temática:** TFB-04 Asociaciones sectoriales y datos de industria (principal) · secundarias: —
- **Calidad Q:** 75 (B) — Primariedad 17/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 13/15 · Independencia 6/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto (notas de prensa)
- **Ámbitos:** Mercado y producción de automóviles en el Reino Unido
- **Motivo de inclusión y uso:** Dato mensual de demanda de vehículos fuera de la UE.
- **Restricciones de uso:** Citar nota y mes.
- **Sesgos y cautelas:** Asociación sectorial. Productos concretos no leídos directamente: confirmar en el próximo barrido.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B04: matriculaciones y producción del automóvil en el Reino Unido.
- **Origen:** Reutilizada con su ID de F9 V3.2 (Bloque A general); temática reasignada a TFB-04 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «OICA ACEA ANFAC vehicle production registrations statistics official»; URL tomada del directorio de asociaciones nacionales de ACEA leído con WebFetch; WebFetch al sitio: no)

#### RF-0321 · Q 75 (B) — SEMI — facturación mundial de equipos de semiconductores

- **Canal oficial (URL raíz):** https://www.semi.org/en/semi-press-release/semi-reports-global-semiconductor-equipment-billings-increased-14-percent-year-over-year-in-q1-2026
- **Emisor:** SEMI (asociación mundial de la cadena de suministro de semiconductores)
- **Documentación y notas:** Notas trimestrales de facturación mundial de equipos (1T 2026: 36.550 M$, +14 % interanual; publicada 04/06/2026) a partir del informe mensual WWSEMS (datos de miembros de SEMI y de SEAJ); suscripción EMDS con informe norteamericano mensual y previsión semestral.
- **Temática:** TFB-04 Asociaciones sectoriales y datos de industria (principal) · secundarias: TFB-05
- **Calidad Q:** 75 (B) — Primariedad 17/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 14/15 · Independencia 6/10 · Actualidad 8/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (notas); datos detallados de pago
- **Ámbitos:** Inversión en equipos de semiconductores por región y segmento
- **Motivo de inclusión y uso:** Indicador del ciclo de inversión (capex) en semiconductores, complemento de RF-0057.
- **Restricciones de uso:** Citar trimestre y nota.
- **Sesgos y cautelas:** Asociación sectorial (sesgo promocional).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B05 y AG-B06: inversión en equipos de semiconductores (capex de fabricación) por región; AG-B12: criba de fabricantes de equipos.
- **Origen:** Reutilizada con su ID de F9 V3.2 (Bloque A general); temática reasignada a TFB-04 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «SEMI worldwide semiconductor equipment billings report»; WebFetch: sí)

#### RF-0307 · Q 74 (B) — VDA — industria del automóvil en Alemania

- **Canal oficial (URL raíz):** https://www.vda.de/
- **Emisor:** Verband der Automobilindustrie (VDA)
- **Documentación y notas:** Asociación nacional alemana listada en el directorio oficial de ACEA; publica producción y exportación de turismos de fabricantes alemanes.
- **Temática:** TFB-04 Asociaciones sectoriales y datos de industria (principal) · secundarias: —
- **Calidad Q:** 74 (B) — Primariedad 17/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 13/15 · Independencia 6/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (parcial; contenidos en alemán)
- **Ámbitos:** Producción, exportación y mercado interior de automóviles en Alemania
- **Motivo de inclusión y uso:** Termómetro del principal productor europeo de automóviles (ciclo industrial alemán).
- **Restricciones de uso:** Citar publicación y mes.
- **Sesgos y cautelas:** Asociación sectorial. Productos concretos no leídos directamente: confirmar en el próximo barrido.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B04 y AG-B05: producción, exportación y empleo del automóvil alemán (principal productor europeo).
- **Origen:** Reutilizada con su ID de F9 V3.2 (Bloque A general); temática reasignada a TFB-04 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «OICA ACEA ANFAC vehicle production registrations statistics official»; URL tomada del directorio de asociaciones nacionales de ACEA leído con WebFetch; WebFetch al sitio: no)

#### RF-0348 · Q 74 (B) — GSMA Intelligence — The Mobile Economy

- **Canal oficial (URL raíz):** https://www.gsma.com/solutions-and-impact/connectivity-for-good/mobile-economy/wp-content/uploads/2026/02/The-Mobile-Economy-2026.pdf
- **Emisor:** GSMA (GSMA Intelligence)
- **Documentación y notas:** Informe anual mundial y regional: 8.800 millones de conexiones y 5.800 millones de abonados únicos, adopción de 5G, ingresos y capex de operadores con previsiones a 2030; serie en gsmaintelligence.com/series/the-mobile-economy.
- **Temática:** TFB-04 Asociaciones sectoriales y datos de industria (principal) · secundarias: TFB-09
- **Calidad Q:** 74 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 14/15 · Independencia 6/10 · Actualidad 8/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto (informe); datos detallados de pago
- **Ámbitos:** Telecomunicaciones móviles: abonados, 5G, ingresos, inversión
- **Motivo de inclusión y uso:** Referencia sectorial para operadores y fabricantes de redes.
- **Restricciones de uso:** Citar edición y región.
- **Sesgos y cautelas:** Asociación de operadores (sesgo sectorial); previsiones propias.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B04 y AG-B06: adopción móvil, 5G y conectividad por región; AG-B03: estructura del sector de telecomunicaciones.
- **Origen:** Reutilizada con su ID de F9 V3.2 (Bloque A general); temática reasignada a TFB-04 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «GSMA Intelligence The Mobile Economy report»; WebFetch: sí)

#### RF-0304 · Q 73 (B) — OICA — producción y ventas mundiales de vehículos

- **Canal oficial (URL raíz):** https://oica.net/statistics
- **Emisor:** Organisation Internationale des Constructeurs d'Automobiles (OICA)
- **Documentación y notas:** Secciones de producción (por fabricante y mercado) y ventas mundiales; Destatis la registra como fuente de estadística internacional.
- **Temática:** TFB-04 Asociaciones sectoriales y datos de industria (principal) · secundarias: —
- **Calidad Q:** 73 (B) — Primariedad 17/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 14/15 · Independencia 7/10 · Actualidad 6/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (tablas); existe área de miembros
- **Ámbitos:** Producción y ventas mundiales de vehículos por país y fabricante
- **Motivo de inclusión y uso:** Comparativa global anual de la industria del automóvil.
- **Restricciones de uso:** Citar año y tabla.
- **Sesgos y cautelas:** Frecuencia anual; la página no indica el último año cubierto.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B04 y AG-B05: producción y ventas mundiales de vehículos por país como base del dimensionado del mercado del automóvil.
- **Origen:** Reutilizada con su ID de F9 V3.2 (Bloque A general); temática reasignada a TFB-04 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «OICA ACEA ANFAC vehicle production registrations statistics official»; WebFetch: sí)

#### RF-0351 · Q 73 (B) — American Chemistry Council — Chemical Activity Barometer

- **Canal oficial (URL raíz):** https://www.americanchemistry.com/
- **Emisor:** American Chemistry Council (ACC)
- **Documentación y notas:** Indicador adelantado mensual de la actividad industrial de EE. UU. basado en la química (media móvil de tres meses); difundido por la prensa sectorial y por Calculated Risk, que enlaza las notas de prensa en americanchemistry.com y lo describe como adelantado de la producción industrial.
- **Temática:** TFB-04 Asociaciones sectoriales y datos de industria (principal) · secundarias: TFB-02
- **Calidad Q:** 73 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 13/15 · Independencia 6/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto (notas de prensa)
- **Ámbitos:** Química estadounidense como indicador adelantado industrial
- **Motivo de inclusión y uso:** Señal temprana del ciclo manufacturero.
- **Restricciones de uso:** Citar mes.
- **Sesgos y cautelas:** Asociación sectorial. Página del barómetro no leída directamente: confirmar URL de la pieza.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B08 y AG-B05: indicador adelantado del ciclo químico e industrial de EE. UU.
- **Origen:** Reutilizada con su ID de F9 V3.2 (Bloque A general); temática reasignada a TFB-04 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «American Chemistry Council Chemical Activity Barometer»; dominio confirmado por el enlace de Calculated Risk leído con WebFetch; WebFetch al sitio: no)

#### MBF-0617 · Q 72 (B) — SolarPower Europe — Global Market Outlook for Solar Power 2025-2029 (y EU Solar Market Outlook)

- **Canal oficial (URL raíz):** https://www.solarpowereurope.org/insights/outlooks/global-market-outlook-for-solar-power-2025-2029 (UE: https://www.solarpowereurope.org/insights/outlooks/eu-solar-market-outlook-2025-2030)
- **Emisor:** SolarPower Europe (asociación europea del sector fotovoltaico, Bruselas)
- **Documentación y notas:** Informe anual insignia (06/05/2025): instalación récord de 597 GW en 2024, potencia mundial acumulada de 2,2 TW y previsiones a 2029 por país, con foco en la India; edición europea con previsiones 2025-2030. Lectura en línea y descarga tras formulario.
- **Temática:** TFB-04 Asociaciones sectoriales y datos de industria (principal) · secundarias: TFB-12, TFB-17
- **Calidad Q:** 72 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 13/15 · Independencia 6/10 · Actualidad 10/10 · Acceso 8/10
- **Tipología:** secundaria cualificada (asociación de industria con datos de mercado)
- **Acceso:** Gratuito con formulario de registro
- **Ámbitos:** Instalaciones solares fotovoltaicas por país, segmento y previsiones
- **Motivo de inclusión y uso:** Dimensionado y crecimiento del mercado solar por región para la cadena de valor (polisilicio, módulos, inversores).
- **Restricciones de uso:** Condiciones de SolarPower Europe; citar edición.
- **Sesgos y cautelas:** Asociación de la industria: sesgo alcista en escenarios; contrastar con IRENA e IEA.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B04 Demanda y Adopción: instalaciones solares por país y escenarios; AG-B05 Oferta y Cadena de Suministro: demanda de módulos e inversores; AG-B13 Prospectiva.
- **Origen:** Alta F9_comp (2026-11-03).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-03 (búsqueda web: «GWEC Global Wind Report 2025 and SolarPower Europe Global Market Outlook for solar power 2025-2029»; WebFetch: sí)

#### MBF-0618 · Q 71 (B) — GWEC — Global Wind Report y Global Wind Market Outlook (trimestral)

- **Canal oficial (URL raíz):** https://marketintelligence.gwec.net/wp-content/uploads/2025/12/GWEC_-Global-Wind-Market-Outlook-_Q3-2025.pdf (presentación del Global Wind Report 2025: https://www.compositesworld.com/news/gwec-launches-2025-global-wind-report)
- **Emisor:** Global Wind Energy Council (GWEC), Bruselas; unidad GWEC Market Intelligence
- **Documentación y notas:** Informe anual de la industria eólica mundial (2024: 117 GW instalados, récord; 320 GW/año necesarios hacia 2030 para triplicar las renovables según la COP28; perspectiva a 2029) y perspectiva de mercado trimestral de GWEC Market Intelligence.
- **Temática:** TFB-04 Asociaciones sectoriales y datos de industria (principal) · secundarias: TFB-12, TFB-17
- **Calidad Q:** 71 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 13/15 · Independencia 6/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** secundaria cualificada (asociación de industria con inteligencia de mercado)
- **Acceso:** Informe anual gratuito con registro; datos detallados de pago
- **Ámbitos:** Instalaciones eólicas terrestres y marinas por país; previsiones; cadena de suministro
- **Motivo de inclusión y uso:** Dimensionado del mercado eólico y de su cadena de valor (turbinas, cimentaciones, cables).
- **Restricciones de uso:** Condiciones de GWEC; citar edición.
- **Sesgos y cautelas:** Asociación de la industria: escenarios con sesgo favorable; la reseña leída es secundaria.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B04 Demanda y Adopción: instalaciones eólicas por mercado; AG-B05 Oferta y Cadena de Suministro: capacidad de fabricación de turbinas; AG-B13 Prospectiva.
- **Origen:** Alta F9_comp (2026-11-03).
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-03 (búsqueda web: «GWEC Global Wind Report 2025 and SolarPower Europe Global Market Outlook for solar power 2025-2029»; WebFetch: sí, reseña de CompositesWorld; el PDF de GWEC no se leyó)

#### RF-0058 · Q 71 (B) — International Federation of Robotics — World Robotics

- **Canal oficial (URL raíz):** https://ifr.org/about-world-robotics/
- **Emisor:** International Federation of Robotics (IFR)
- **Documentación y notas:** Informe anual en dos volúmenes (Industrial Robots, con cobots; Service Robots); estadísticas de proveedores y asociaciones nacionales; instalaciones, parque operativo y densidad robótica; base de datos histórica (desde 1993 en algunos casos) en versión premium. Gratuitos: presentación de la rueda de prensa y notas de prensa (p. ej., «World Robotics 2025 report»).
- **Temática:** TFB-04 Asociaciones sectoriales y datos de industria (principal) · secundarias: TFB-09
- **Calidad Q:** 71 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 13/15 · Independencia 6/10 · Actualidad 7/10 · Acceso 7/10
- **Tipología:** primaria
- **Acceso:** Resúmenes y presentaciones abiertos; informe de pago (VDMA Verlag)
- **Ámbitos:** Instalaciones de robots industriales y de servicio
- **Motivo de inclusión y uso:** Medida de difusión de la automatización.
- **Restricciones de uso:** Citar edición y tabla; usar solo contenidos públicos.
- **Sesgos y cautelas:** Asociación sectorial; informe completo de pago; frecuencia anual.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B04 y AG-B06: adopción de robots industriales por país e industria; AG-B12: fabricantes de automatización.
- **Origen:** Reutilizada con su ID de F9 V3.2 (Bloque A general); temática reasignada a TFB-04 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «IFR World Robotics report International Federation of Robotics»; WebFetch: sí)

## TFB-05 Comercio internacional y cadenas de suministro

#### MBF-0039 · Q 89 (A) — U.S. Census Bureau — Foreign Trade Statistics

- **Canal oficial (URL raíz):** http://www.census.gov/foreign-trade/data/index.html
- **Emisor:** U.S. Census Bureau
- **Documentación y notas:** Estadísticas de comercio exterior de EE. UU.: datos por producto y país, exportaciones por estado y serie histórica desde 1960. Confirmada vía Índice Harvard Library Research Guide «Trade» (https://guides.library.harvard.edu/trade).
- **Temática:** TFB-05 Comercio internacional y cadenas de suministro (principal) · secundarias: TFB-01
- **Calidad Q:** 89 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Comercio de mercancías de EE. UU. por producto y socio
- **Motivo de inclusión y uso:** Fuente primaria del mayor importador mundial, clave ante cambios arancelarios.
- **Restricciones de uso:** Dominio público con cita.
- **Sesgos y cautelas:** Revisiones anuales.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B05 y AG-B07: dependencia de importaciones de EE. UU. por producto y origen; efecto de aranceles.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «UN Comtrade database WITS World Integrated Trade Solution free trade data tariff»; WebFetch: sí, página índice)
- **Origen:** Alta 2026-11-02 (F9 Bloque B V2.0, TFB-05).

#### MBF-0043 · Q 89 (A) — OMC — Estadísticas de comercio y aranceles

- **Canal oficial (URL raíz):** http://www.wto.org/english/res_e/statis_e/statis_e.htm
- **Emisor:** Organización Mundial del Comercio
- **Documentación y notas:** Perfiles de comercio, aranceles y servicios por país, series temporales, publicaciones estadísticas y bases de datos de la OMC. Confirmada vía Índice Harvard Library Research Guide «Trade» (https://guides.library.harvard.edu/trade).
- **Temática:** TFB-05 Comercio internacional y cadenas de suministro (principal) · secundarias: TFB-01
- **Calidad Q:** 89 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Comercio de mercancías y servicios, aranceles, perfiles por país
- **Motivo de inclusión y uso:** Fuente oficial multilateral de comercio y aranceles.
- **Restricciones de uso:** Condiciones de la OMC con cita.
- **Sesgos y cautelas:** Desfase en algunos datos de servicios.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B07: aranceles y política comercial; AG-B04: comercio de servicios; AG-B05: flujos por región.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «UN Comtrade database WITS World Integrated Trade Solution free trade data tariff»; WebFetch: sí, página índice)
- **Origen:** Alta 2026-11-02 (F9 Bloque B V2.0, TFB-05).

#### MBF-0050 · Q 89 (A) — BEA — International Economic Accounts (comercio de bienes y servicios y transacciones internacionales de EE. UU.)

- **Canal oficial (URL raíz):** http://www.bea.gov/international/index.htm
- **Emisor:** U.S. Bureau of Economic Analysis
- **Documentación y notas:** Cuentas internacionales de EE. UU.: comercio de bienes y servicios por tipo y país, transacciones internacionales y posición de inversión. Confirmada vía Índice Harvard Library Research Guide «Trade» (https://guides.library.harvard.edu/trade).
- **Temática:** TFB-05 Comercio internacional y cadenas de suministro (principal) · secundarias: TFB-01
- **Calidad Q:** 89 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Comercio de servicios (software, propiedad intelectual, viajes, transporte) y bienes de EE. UU.
- **Motivo de inclusión y uso:** Única fuente oficial detallada del comercio de servicios de EE. UU., clave para sectores digitales y de propiedad intelectual.
- **Restricciones de uso:** Dominio público con cita.
- **Sesgos y cautelas:** Revisiones anuales; asignación geográfica de servicios con estimaciones.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B04 y AG-B05: exportaciones de servicios por tipo (software, licencias, viajes); AG-B07: exposición a medidas sobre servicios digitales.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «UN Comtrade database WITS World Integrated Trade Solution free trade data tariff»; WebFetch: sí, página índice)
- **Origen:** Alta 2026-11-02 (F9 Bloque B V2.0, TFB-05).

#### MBF-0061 · Q 89 (A) — Eurostat — estadísticas de comercio internacional de mercancías (extra e intra-UE)

- **Canal oficial (URL raíz):** http://ec.europa.eu/eurostat/data/database
- **Emisor:** Eurostat (Comisión Europea)
- **Documentación y notas:** Comercio exterior de la UE y entre Estados miembros, indicadores de corto y largo plazo, en la base de datos de Eurostat (la base detallada por producto es Comext). Confirmada vía Índice Harvard Library Research Guide «Trade» (https://guides.library.harvard.edu/trade).
- **Temática:** TFB-05 Comercio internacional y cadenas de suministro (principal) · secundarias: TFB-01
- **Calidad Q:** 89 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Comercio de mercancías de la UE por producto y socio
- **Motivo de inclusión y uso:** Fuente oficial para dependencias de importación de la UE y cuotas exportadoras europeas por producto.
- **Restricciones de uso:** Uso libre con cita.
- **Sesgos y cautelas:** Asimetrías intra-UE; confidencialidad de algunos flujos.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B05: dependencias de importación de la UE (materias primas críticas, componentes); AG-B07: exposición a aranceles y medidas de defensa comercial; AG-B03: cuotas exportadoras.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «UN Comtrade database WITS World Integrated Trade Solution free trade data tariff»; WebFetch: sí, página índice)
- **Origen:** Alta 2026-11-02 (F9 Bloque B V2.0, TFB-05).

#### MBF-0042 · Q 88 (A) — FMI — International Trade in Goods by Partner Country (IMTS, antes DOTS)

- **Canal oficial (URL raíz):** https://data.imf.org/en/datasets/IMF.STA:IMTS
- **Emisor:** Fondo Monetario Internacional
- **Documentación y notas:** Series bilaterales de exportaciones e importaciones de mercancías desde 1940. Confirmada vía Índice Harvard Library Research Guide «Trade» (https://guides.library.harvard.edu/trade).
- **Temática:** TFB-05 Comercio internacional y cadenas de suministro (principal) · secundarias: TFB-01
- **Calidad Q:** 88 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria (compilación oficial)
- **Acceso:** Abierto
- **Ámbitos:** Comercio bilateral agregado por país socio
- **Motivo de inclusión y uso:** Serie larga y mensual para medir exposición comercial de un mercado geográfico.
- **Restricciones de uso:** Condiciones del FMI con cita.
- **Sesgos y cautelas:** Sin desglose por producto; estimaciones para países sin datos.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Cambio de nombre DOTS → IMTS.
- **Uso en el bloque:** AG-B07 y AG-B08: exposición comercial bilateral de mercados geográficos; Motor AG-B16: matrices de comercio para escenarios.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «UN Comtrade database WITS World Integrated Trade Solution free trade data tariff»; WebFetch: sí, página índice)
- **Origen:** Alta 2026-11-02 (F9 Bloque B V2.0, TFB-05).

#### MBF-0046 · Q 88 (A) — FAO — FAOSTAT

- **Canal oficial (URL raíz):** https://www.fao.org/faostat/en/#home
- **Emisor:** Organización de las Naciones Unidas para la Alimentación y la Agricultura (FAO)
- **Documentación y notas:** Series multilingües de producción, comercio, precios y uso de insumos en agricultura y alimentación por país. Confirmada vía Índice Harvard Library Research Guide «Trade» (https://guides.library.harvard.edu/trade).
- **Temática:** TFB-05 Comercio internacional y cadenas de suministro (principal) · secundarias: TFB-12
- **Calidad Q:** 88 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria (compilación oficial)
- **Acceso:** Abierto
- **Ámbitos:** Agricultura y alimentación: producción, comercio, precios, insumos
- **Motivo de inclusión y uso:** Base para cadenas de valor agroalimentarias (fertilizantes, maquinaria, alimentación).
- **Restricciones de uso:** Licencia abierta de la FAO con cita.
- **Sesgos y cautelas:** Datos anuales con desfase.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B05: cadenas agroalimentarias; AG-B04: demanda de alimentos por país; AG-B12: criba de empresas agroalimentarias y de insumos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «UN Comtrade database WITS World Integrated Trade Solution free trade data tariff»; WebFetch: sí, página índice)
- **Origen:** Alta 2026-11-02 (F9 Bloque B V2.0, TFB-05).

#### MBF-0052 · Q 88 (A) — OCDE — Tablas input-output interpaíses (ICIO) y base Trade in Value Added (TiVA), edición 2025

- **Canal oficial (URL raíz):** https://www.oecd.org/en/blogs/2025/11/oecd-inter-country-input-output-icio-tables-and-trade-in-value-added-tiva-database-launch-of-the-2025-edition.html
- **Emisor:** OCDE
- **Documentación y notas:** Lanzamiento de la edición 2025 de las tablas ICIO y los indicadores TiVA (noviembre de 2025); notas por país (p. ej., España, Alemania) en oecd.org/en/publications/trade-in-value-added-country-notes_f5cbfae2-en.
- **Temática:** TFB-05 Comercio internacional y cadenas de suministro (principal) · secundarias: TFB-01
- **Calidad Q:** 88 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Valor añadido en el comercio, participación en cadenas globales de valor, tablas input-output
- **Motivo de inclusión y uso:** Fuente de referencia para medir cadenas de valor globales y dependencias indirectas por industria.
- **Restricciones de uso:** Condiciones de la OCDE con cita de edición.
- **Sesgos y cautelas:** Desfase de varios años; supuestos de homogeneidad.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Ediciones periódicas con cambios de cobertura.
- **Uso en el bloque:** AG-B05: dependencias directas e indirectas por industria y país; AG-B03: posición en la cadena de valor; Motor AG-B16: análisis input-output.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «OECD Trade in Value Added TiVA database 2025 edition inter-country input-output tables»; WebFetch: sí, sin cuerpo legible)
- **Origen:** Alta 2026-11-02 (F9 Bloque B V2.0, TFB-05).

#### MBF-0038 · Q 87 (A) — Comisión Europea — Access2Markets

- **Canal oficial (URL raíz):** https://trade.ec.europa.eu/access-to-markets/en/home
- **Emisor:** Comisión Europea (DG Trade)
- **Documentación y notas:** Aranceles por producto, impuestos, procedimientos aduaneros, normas de origen y barreras comerciales para exportar desde la UE e importar en ella. Confirmada vía Índice Harvard Library Research Guide «Trade» (https://guides.library.harvard.edu/trade).
- **Temática:** TFB-05 Comercio internacional y cadenas de suministro (principal) · secundarias: TFB-03
- **Calidad Q:** 87 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Aranceles y barreras por producto y mercado de destino
- **Motivo de inclusión y uso:** Fuente oficial para evaluar barreras de acceso a mercados de empresas europeas.
- **Restricciones de uso:** Condiciones de la Comisión.
- **Sesgos y cautelas:** Orientado a exportadores: no da flujos.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B07: barreras de entrada y aranceles en mercados destino; AG-B04: accesibilidad de mercados geográficos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «UN Comtrade database WITS World Integrated Trade Solution free trade data tariff»; WebFetch: sí, página índice)
- **Origen:** Alta 2026-11-02 (F9 Bloque B V2.0, TFB-05).

#### MBF-0036 · Q 86 (A) — UN Comtrade (base de datos de comercio de mercancías de la ONU)

- **Canal oficial (URL raíz):** Índice: https://guides.library.harvard.edu/trade · ficha del catálogo del Banco Mundial: https://datacatalog.worldbank.org/infrastructure-data/search/dataset/0039673/World-Integrated-Trade-Solution-UN-COMTRADE
- **Emisor:** División de Estadística de las Naciones Unidas (UNSD)
- **Documentación y notas:** Datos anuales de comercio de mercancías por producto (HS/SITC) y país socio para más de 130 países, y comercio de servicios desde 2000; nivel Premium con registro individual. URL oficial no mostrada en el índice. Confirmada vía Índice Harvard Library Research Guide «Trade» (https://guides.library.harvard.edu/trade).
- **Temática:** TFB-05 Comercio internacional y cadenas de suministro (principal) · secundarias: TFB-01
- **Calidad Q:** 86 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria (compilación de declaraciones nacionales)
- **Acceso:** Abierto con registro; nivel Premium
- **Ámbitos:** Comercio bilateral por producto
- **Motivo de inclusión y uso:** Base de referencia para cuotas de exportación, dependencias de proveedores y flujos por producto.
- **Restricciones de uso:** Condiciones de uso de la ONU; citar flujo, código y año.
- **Sesgos y cautelas:** Asimetrías espejo entre exportador e importador; desfase.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B05: dependencias de suministro por producto y país; AG-B03: cuotas exportadoras; AG-B07: exposición a aranceles y sanciones.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «UN Comtrade database WITS World Integrated Trade Solution free trade data tariff»; WebFetch: sí, página índice)
- **Origen:** Alta 2026-11-02 (F9 Bloque B V2.0, TFB-05).

#### MBF-0040 · Q 86 (A) — USA Trade Online (U.S. Census Bureau)

- **Canal oficial (URL raíz):** https://usatrade.census.gov/
- **Emisor:** U.S. Census Bureau
- **Documentación y notas:** Datos de importación y exportación de EE. UU. para más de 18.000 productos con clasificación HTS, actuales e históricos. Confirmada vía Índice Harvard Library Research Guide «Trade» (https://guides.library.harvard.edu/trade).
- **Temática:** TFB-05 Comercio internacional y cadenas de suministro (principal) · secundarias: —
- **Calidad Q:** 86 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (consultar condiciones de acceso del portal)
- **Ámbitos:** Comercio de EE. UU. al máximo detalle de producto (HTS 10 dígitos) y por puerto
- **Motivo de inclusión y uso:** Permite seguir mensualmente importaciones de productos muy concretos (componentes, materias primas).
- **Restricciones de uso:** Dominio público con cita.
- **Sesgos y cautelas:** Interfaz compleja; revisiones.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B05: seguimiento de flujos de componentes y materias primas a 10 dígitos; AG-B07: efecto de aranceles por producto.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «UN Comtrade database WITS World Integrated Trade Solution free trade data tariff»; WebFetch: sí, página índice)
- **Origen:** Alta 2026-11-02 (F9 Bloque B V2.0, TFB-05).

#### MBF-0051 · Q 85 (A) — FMI y Universidad de Oxford — PortWatch

- **Canal oficial (URL raíz):** https://www.imf.org/en/news/articles/2023/11/13/pr23390-imf-university-oxford-launch-portwatch-platform-monitor-simulate-trade-disruptions
- **Emisor:** Fondo Monetario Internacional y Environmental Change Institute (Universidad de Oxford)
- **Documentación y notas:** Plataforma abierta (anunciada el 15/11/2023, comunicado 23/390) que vigila disrupciones del comercio marítimo en puertos y rutas críticas con datos de buques por satélite y simula efectos en cadenas de suministro; plataforma en imf.org/portwatch.
- **Temática:** TFB-05 Comercio internacional y cadenas de suministro (principal) · secundarias: TFB-17
- **Calidad Q:** 85 (A) — Primariedad 17/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria (datos satelitales procesados)
- **Acceso:** Abierto
- **Ámbitos:** Actividad portuaria, pasos estratégicos (Suez, Panamá, Ormuz), disrupciones
- **Motivo de inclusión y uso:** Mide en casi tiempo real el impacto de cierres de rutas y fenómenos climáticos en el comercio.
- **Restricciones de uso:** Condiciones del FMI con cita.
- **Sesgos y cautelas:** Estimaciones a partir de datos de buques; versión beta en su lanzamiento.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B05: disrupciones de rutas y puertos; AG-B11: riesgos climáticos en la cadena de suministro; AG-B13: escenarios de cierre de pasos estratégicos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «IMF PortWatch port activity chokepoints data UNCTADstat maritime»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9 Bloque B V2.0, TFB-05).

#### FXF-0053 · Q 84 (A) — FMI — External Sector Report (evaluación de desequilibrios y tipos de cambio)

- **Canal oficial (URL raíz):** https://www.imf.org/en/publications/esr/issues/2026/07/30/external-sector-report-2026 (serie: https://www.imf.org/en/Publications/SPROLLs/external-sector-reports)
- **Emisor:** Fondo Monetario Internacional
- **Documentación y notas:** «2026 External Sector Report: Amid Rising Imbalances, the Case for Rebalancing» (30/07/2026): los saldos por cuenta corriente mundiales se ampliaron de nuevo en 2025, con China y EE. UU. como principales contribuyentes a los saldos excesivos; evaluación de 30 grandes economías con datos de 2025 y la metodología EBA (External Balance Assessment) revisada; anexos en línea por país.
- **Temática:** TFB-05 Comercio internacional y cadenas de suministro (principal) · secundarias: TFB-01
- **Calidad Q:** 84 (A) — Primariedad 17/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** primaria (evaluación oficial con modelos propios)
- **Acceso:** Abierto (informe, capítulos y anexos en PDF)
- **Ámbitos:** Saldos exteriores, brechas de cuenta corriente y de tipo de cambio real (EBA), posición de inversión internacional
- **Motivo de inclusión y uso:** Estimación oficial de la desalineación del tipo de cambio real de las grandes divisas. Uso: AS-ESTR (AG-08, estrategia de valor) y MOTOR (AG-13, contraste de BEER/FEER propios); Analistas de segmento como opinión oficial de valoración.
- **Restricciones de uso:** Condiciones del FMI; citar edición.
- **Sesgos posibles:** Evaluación con juicio del personal del FMI y presiones diplomáticas; no es previsión de tipo de cambio.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Metodología EBA «refinada» en la edición de 2026.
- **Uso en el bloque:** AG-B07 y AG-B08: desequilibrios externos y competitividad por país, contexto para tensiones comerciales y aranceles.
- **Origen:** Reutilizada con su ID de F9 Forex V1.0; temática reasignada a TFB-05 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «IMF External Sector Report 2026 external balance assessment»; WebFetch: sí)

#### MBF-0037 · Q 84 (A) — World Bank — WITS (World Integrated Trade Solution)

- **Canal oficial (URL raíz):** https://wits.worldbank.org/about_wits.html
- **Emisor:** Banco Mundial (con UNCTAD, ITC, ONU y OMC)
- **Documentación y notas:** Software y portal que integra datos de comercio (UN Comtrade), aranceles (TRAINS, OMC) y medidas no arancelarias, con perfiles por país; análisis personalizado con registro gratuito. Confirmada vía Índice Harvard Library Research Guide «Trade» (https://guides.library.harvard.edu/trade) y página «About WITS».
- **Temática:** TFB-05 Comercio internacional y cadenas de suministro (principal) · secundarias: —
- **Calidad Q:** 84 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 9/10
- **Tipología:** secundaria (integración de bases oficiales)
- **Acceso:** Abierto; registro gratuito para análisis personalizado
- **Ámbitos:** Comercio, aranceles aplicados y consolidados, medidas no arancelarias
- **Motivo de inclusión y uso:** Une flujos y aranceles para medir la exposición comercial de un sector.
- **Restricciones de uso:** Condiciones del Banco Mundial; citar base original.
- **Sesgos y cautelas:** Hereda limitaciones de Comtrade y TRAINS.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B07: exposición arancelaria por producto y mercado; AG-B05: orígenes de importación; Motor AG-B16: escenarios de aranceles.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «UN Comtrade database WITS World Integrated Trade Solution free trade data tariff»; WebFetch: sí, página índice)
- **Origen:** Alta 2026-11-02 (F9 Bloque B V2.0, TFB-05).

#### MBF-0048 · Q 84 (A) — Federal Reserve Bank of New York — Global Supply Chain Pressure Index (GSCPI)

- **Canal oficial (URL raíz):** https://www.newyorkfed.org/medialibrary/media/research/staff_reports/sr1017.pdf
- **Emisor:** Federal Reserve Bank of New York
- **Documentación y notas:** Índice mensual de presiones en las cadenas de suministro globales que combina costes de transporte (Baltic Dry, Harpex, fletes aéreos) y componentes de PMI de varias economías; metodología en el Staff Report 1017 (Benigno, di Giovanni, Groen y Noble).
- **Temática:** TFB-05 Comercio internacional y cadenas de suministro (principal) · secundarias: TFB-02
- **Calidad Q:** 84 (A) — Primariedad 16/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria (índice compuesto de banco central)
- **Acceso:** Abierto
- **Ámbitos:** Presión en cadenas de suministro: plazos de entrega, retrasos, costes de transporte
- **Motivo de inclusión y uso:** Indicador sintético de tensiones de suministro con metodología pública.
- **Restricciones de uso:** Cita del índice y mes.
- **Sesgos y cautelas:** Índice compuesto: sensibilidad a la selección de componentes; revisiones.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Revisiones periódicas de la serie.
- **Uso en el bloque:** AG-B05: estado de las cadenas de suministro (cuellos de botella); AG-B08: presiones inflacionistas de oferta; Motor AG-B16: variable de estado en escenarios.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «supply chain pressure indicators GSCPI New York Fed Freightos Baltic Index Kiel Trade Indicator CPB World Trade Monitor»; WebFetch: no)
- **Origen:** Alta 2026-11-02 (F9 Bloque B V2.0, TFB-05).

#### MBF-0041 · Q 81 (A) — International Trade Administration — datos de comercio e industria (trade.gov)

- **Canal oficial (URL raíz):** https://www.trade.gov/data.asp
- **Emisor:** International Trade Administration (U.S. Department of Commerce)
- **Documentación y notas:** Datos de comercio internacional, por estado y algunas áreas metropolitanas, y datos a nivel de industria. Confirmada vía Índice Harvard Library Research Guide «Trade» (https://guides.library.harvard.edu/trade).
- **Temática:** TFB-05 Comercio internacional y cadenas de suministro (principal) · secundarias: —
- **Calidad Q:** 81 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 14/15 · Independencia 9/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Comercio de EE. UU. por industria y territorio
- **Motivo de inclusión y uso:** Visión por industria del comercio estadounidense y guías de mercados exteriores.
- **Restricciones de uso:** Dominio público con cita.
- **Sesgos y cautelas:** Orientación promocional de exportaciones.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B04 y AG-B05: comercio por industria de EE. UU.; AG-B07: contexto de política comercial.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «UN Comtrade database WITS World Integrated Trade Solution free trade data tariff»; WebFetch: sí, página índice)
- **Origen:** Alta 2026-11-02 (F9 Bloque B V2.0, TFB-05).

#### RF-0322 · Q 81 (A) — Baltic Exchange — índices de fletes (BDI y otros)

- **Canal oficial (URL raíz):** https://balticexchange.com/en/who-we-are/faqs.html
- **Emisor:** Baltic Exchange (filial Baltic Exchange Information Services Ltd, administrador de índices autorizado por la FCA; vinculada al grupo SGX)
- **Documentación y notas:** Índices de graneles secos (Capesize, Panamax, Supramax, Handysize; BDI derivado de los tres primeros), petroleros (BDTI, BCTI), gas (BLNG, BLPG), contenedores (con Freightos), carga aérea semanal y curvas forward; evaluaciones de corredores panelistas sin posiciones propias.
- **Temática:** TFB-05 Comercio internacional y cadenas de suministro (principal) · secundarias: TFB-12
- **Calidad Q:** 81 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 6/10
- **Tipología:** primaria
- **Acceso:** Licencia para uso de datos (API, prueba gratuita); valores difundidos por prensa
- **Ámbitos:** Fletes marítimos de graneles, petroleros y gas
- **Motivo de inclusión y uso:** Índice de referencia del comercio de materias primas a granel y del ciclo global.
- **Restricciones de uso:** Licencia Baltic Data para uso contractual; citar índice y fecha.
- **Sesgos y cautelas:** Datos completos de pago; las cifras de prensa son de segunda mano.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Propiedad del grupo SGX (no detallada en la página leída).
- **Uso en el bloque:** AG-B05 y AG-B08: fletes de graneles secos (BDI y otros) como indicador de demanda de materias primas y de costes logísticos; AG-B12: navieras.
- **Origen:** Reutilizada con su ID de F9 V3.2 (Bloque A general); temática reasignada a TFB-05 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «balticexchange.com Baltic Dry Index dry bulk freight indices»; WebFetch: sí)

#### MBF-0044 · Q 79 (B) — CEPII — BACI (comercio bilateral armonizado)

- **Canal oficial (URL raíz):** http://www.cepii.fr/CEPII/en/bdd_modele/presentation.asp?id=37
- **Emisor:** CEPII (Centre d'études prospectives et d'informations internationales)
- **Documentación y notas:** Flujos bilaterales de comercio desagregados para más de 5.000 productos y unos 200 países, construidos a partir de UN Comtrade con conciliación de declaraciones espejo. Confirmada vía Índice Harvard Library Research Guide «Trade» (https://guides.library.harvard.edu/trade).
- **Temática:** TFB-05 Comercio internacional y cadenas de suministro (principal) · secundarias: TFB-18
- **Calidad Q:** 79 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 14/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** secundaria (armonización académica de Comtrade)
- **Acceso:** Abierto (licencia Etalab)
- **Ámbitos:** Comercio bilateral por producto HS6 armonizado
- **Motivo de inclusión y uso:** Datos de comercio limpios para cuotas de mercado mundiales por producto.
- **Restricciones de uso:** Licencia abierta con cita de BACI y versión.
- **Sesgos y cautelas:** Desfase anual; valores conciliados (no oficiales).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Versiones anuales con cambios de nomenclatura HS.
- **Uso en el bloque:** AG-B03: cuotas de exportación mundiales por producto y país; AG-B05: concentración de proveedores; Motor AG-B16: índices de concentración (HHI).
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «UN Comtrade database WITS World Integrated Trade Solution free trade data tariff»; WebFetch: sí, página índice)
- **Origen:** Alta 2026-11-02 (F9 Bloque B V2.0, TFB-05).

#### MBF-0049 · Q 76 (B) — Freightos Baltic Index (FBX) — índice diario de fletes de contenedores

- **Canal oficial (URL raíz):** https://www.balticexchange.com/en/data-services/market-information0/container-services.html
- **Emisor:** Baltic Exchange y Freightos
- **Documentación y notas:** Índice diario (desde febrero de 2021) de tarifas spot de contenedores de 40 pies en 12 rutas (p. ej., China/Asia Oriental–Norte de Europa FBX11; China–Costa Oeste de EE. UU. FBX01), ponderado por volúmenes; descrito como índice de fletes conforme con IOSCO y regulado por ESMA.
- **Temática:** TFB-05 Comercio internacional y cadenas de suministro (principal) · secundarias: TFB-06
- **Calidad Q:** 76 (B) — Primariedad 17/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 13/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 7/10
- **Tipología:** primaria (índice de referencia)
- **Acceso:** Índice global y titulares abiertos; series detalladas de pago
- **Ámbitos:** Fletes spot de contenedores por ruta
- **Motivo de inclusión y uso:** Indicador diario de costes logísticos y tensión en rutas marítimas (complementa RF-0323 Drewry).
- **Restricciones de uso:** Condiciones de Freightos/Baltic Exchange.
- **Sesgos y cautelas:** Tarifas spot (no contractuales); proveedor comercial.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Fórmula actualizada por última vez a mediados de 2021.
- **Uso en el bloque:** AG-B05: costes y cuellos de botella logísticos por ruta; AG-B09: impacto en márgenes de importadores y navieras; AG-B12: criba de navieras y logística.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Freightos Baltic Index FBX global container freight index free data terminal»; WebFetch: sí, artículo Wikipedia)
- **Origen:** Alta 2026-11-02 (F9 Bloque B V2.0, TFB-05).

#### MBF-0045 · Q 74 (B) — Harvard Growth Lab — Atlas of Economic Complexity

- **Canal oficial (URL raíz):** https://atlas.cid.harvard.edu/
- **Emisor:** Growth Lab, Harvard University
- **Documentación y notas:** Visualización de flujos comerciales y oportunidades de crecimiento por país y producto; descargas de datos en atlas.cid.harvard.edu/data-downloads. Confirmada vía Índice Harvard Library Research Guide «Trade» (https://guides.library.harvard.edu/trade).
- **Temática:** TFB-05 Comercio internacional y cadenas de suministro (principal) · secundarias: TFB-04
- **Calidad Q:** 74 (B) — Primariedad 10/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 13/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** secundaria (elaboración académica)
- **Acceso:** Abierto
- **Ámbitos:** Comercio por producto, complejidad económica, diversificación
- **Motivo de inclusión y uso:** Útil para detectar especialización exportadora y productos emergentes de un país.
- **Restricciones de uso:** Cita del Atlas y versión.
- **Sesgos y cautelas:** Métricas de complejidad sujetas a debate académico.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B13: oportunidades de diversificación y especialización por país; AG-B04: productos en expansión.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «UN Comtrade database WITS World Integrated Trade Solution free trade data tariff»; WebFetch: sí, página índice)
- **Origen:** Alta 2026-11-02 (F9 Bloque B V2.0, TFB-05).

#### RF-0323 · Q 71 (B) — Drewry — World Container Index

- **Canal oficial (URL raíz):** https://www.drewry.co.uk/logistics-executive-briefing/logistics-executive-briefing-articles/world-container-index
- **Emisor:** Drewry (consultora marítima)
- **Documentación y notas:** Índice compuesto Este-Oeste en $/FEU con variación semanal; difundido cada semana por prensa marítima. La página leída mostraba un valor de 16/02/2023 (contenido desactualizado o en caché) y no detalla metodología.
- **Temática:** TFB-05 Comercio internacional y cadenas de suministro (principal) · secundarias: —
- **Calidad Q:** 71 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 13/15 · Independencia 7/10 · Actualidad 8/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (valor compuesto)
- **Ámbitos:** Fletes de contenedores en rutas Este-Oeste
- **Motivo de inclusión y uso:** Indicador semanal del coste del transporte marítimo de contenedores.
- **Restricciones de uso:** Citar fecha y ruta.
- **Sesgos y cautelas:** Metodología no publicada en la página; consultora con servicios de pago.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B05: coste del transporte en contenedor por ruta (cuellos de botella y normalización de cadenas); AG-B09: impacto en márgenes de importadores.
- **Origen:** Reutilizada con su ID de F9 V3.2 (Bloque A general); temática reasignada a TFB-05 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Drewry World Container Index drewry.co.uk»; WebFetch: sí)

#### MBF-0047 · Q 70 (B) — Correlates of War — International Trade, 1870–2014

- **Canal oficial (URL raíz):** https://correlatesofwar.org/data-sets/bilateral-trade
- **Emisor:** Correlates of War Project
- **Documentación y notas:** Comercio total nacional y bilateral entre Estados desde 1870 hasta 2014. Confirmada vía Índice Harvard Library Research Guide «Trade» (https://guides.library.harvard.edu/trade).
- **Temática:** TFB-05 Comercio internacional y cadenas de suministro (principal) · secundarias: TFB-18
- **Calidad Q:** 70 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 12/15 · Independencia 10/10 · Actualidad 3/10 · Acceso 10/10
- **Tipología:** secundaria (base académica)
- **Acceso:** Abierto
- **Ámbitos:** Comercio bilateral histórico
- **Motivo de inclusión y uso:** Serie histórica larga para analogías de fragmentación comercial y conflictos.
- **Restricciones de uso:** Cita de la versión.
- **Sesgos y cautelas:** Termina en 2014; estimaciones en periodos antiguos.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin actualización reciente.
- **Uso en el bloque:** AG-B13 y AG-B14: analogías históricas de fragmentación comercial y guerras comerciales.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «UN Comtrade database WITS World Integrated Trade Solution free trade data tariff»; WebFetch: sí, página índice)
- **Origen:** Alta 2026-11-02 (F9 Bloque B V2.0, TFB-05).

## TFB-06 Datos de mercado gratuitos

#### RF-0600 · Q 90 (A) — BCE — €STR (euro short-term rate) y €STR compuesto

- **Canal oficial (URL raíz):** https://www.ecb.europa.eu/stats/financial_markets_and_interest_rates/euro_short-term_rate/html/eurostr_overview.en.html (series: https://data.ecb.europa.eu/data/data-categories/financial-markets-and-interest-rates/euro-money-market/euro-short-term-rate-data)
- **Emisor:** Banco Central Europeo (administrador del índice), con datos recogidos por Bundesbank, Banco de España, Banque de France y Banca d'Italia
- **Temática:** TFB-06 Datos de mercado gratuitos (principal) · secundarias: TFB-02
- **Calidad Q:** 90 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria (índice de referencia oficial calculado sobre transacciones)
- **Acceso:** Abierto y gratuito (sin licencia de uso)
- **Ámbitos:** Tipo de interés a un día no garantizado de los bancos de la eurozona; publicación a las 08:00 CET de cada día TARGET2; tipos compuestos a 1 semana y 1, 3, 6 y 12 meses e índice compuesto (09:15 CET); pre-€STR hasta 30/09/2019; revisión metodológica anual (última vista: 09/12/2025)
- **Motivo de inclusión y uso:** Tipo libre de riesgo de referencia del euro y ancla de la curva OIS en euros. AG-24 (Monetarios y liquidez): nivel y diferencial del €STR frente a la facilidad de depósito; AG-25: tramo corto de la curva.
- **Sesgos y cautelas:** Solo mide préstamos no garantizados captados por bancos (incluye depósitos de entidades no bancarias, por eso cotiza por debajo de la facilidad de depósito); procedimiento de contingencia si informan menos de 20 bancos.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Uso en el bloque:** AG-B09 Finanzas y Valoración: tipo libre de riesgo a corto en euros para tasas de descuento; AG-B08 Macro y Ciclo: tensión en el mercado monetario del euro que afecta a sectores sensibles a tipos (banca, inmobiliario).
- **Origen:** Reutilizada con su ID de F9 V3.2 (Bloque A general); temática reasignada a TFB-06 el 2026-11-03.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ECB euro short-term rate €STR money market statistical reporting»; WebFetch: sí)

#### RF-0602 · Q 90 (A) — Federal Reserve Bank of New York — Reference Rates (SOFR, EFFR, OBFR, TGCR, BGCR)

- **Canal oficial (URL raíz):** https://www.newyorkfed.org/markets/reference-rates (SOFR: https://www.newyorkfed.org/markets/reference-rates/sofr · medias e índice: https://www.newyorkfed.org/markets/reference-rates/sofr-averages-and-index)
- **Emisor:** Federal Reserve Bank of New York (administrador; en cooperación con la OFR para los tipos repo)
- **Temática:** TFB-06 Datos de mercado gratuitos (principal) · secundarias: TFB-02
- **Calidad Q:** 90 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria (índices de referencia oficiales sobre transacciones; declaración de cumplimiento IOSCO)
- **Acceso:** Abierto (API de datos de mercados)
- **Ámbitos:** EFFR y OBFR (mediana ponderada por volumen de fondos federales y eurodólares; ~9:00 ET); TGCR, BGCR y SOFR (repo a un día con colateral del Tesoro; SOFR excluye el 20 % de menor tipo del DVP); medias SOFR a 30, 90 y 180 días e índice SOFR (8:00 ET)
- **Motivo de inclusión y uso:** Fuente primaria de los tipos a un día del dólar. AG-24: posición del EFFR dentro de la banda objetivo, diferencial SOFR–IORB como señal de escasez de reservas; AG-25: tramo corto de la curva en dólares.
- **Sesgos y cautelas:** Revisiones del mismo día (~14:30 ET) posibles; el SOFR se publica con un día de retraso respecto a la fecha valor. RF-0343 (OFR) redistribuye estas series: citar aquí la fuente primaria.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Uso en el bloque:** AG-B09 Finanzas y Valoración: tipo libre de riesgo a corto en dólares para tasas de descuento y coste de financiación; Motor AG-B16 (MC-B de valoración): curva corta en escenarios de tipos.
- **Origen:** Reutilizada con su ID de F9 V3.2 (Bloque A general); temática reasignada a TFB-06 el 2026-11-03.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «New York Fed reference rates SOFR EFFR OBFR TGCR BGCR»; WebFetch: sí, página «additional information about reference rates»)

#### FXF-0090 · Q 89 (A) — BCE — tipos de cambio de referencia del euro

- **Canal oficial (URL raíz):** https://www.ecb.europa.eu/stats/policy_and_exchange_rates/euro_reference_exchange_rates/html/index.en.html (acceso corto: https://www.ecb.europa.eu/stats/eurofxref)
- **Emisor:** Banco Central Europeo
- **Documentación y notas:** 29 divisas frente al euro (tipo del rublo suspendido desde el 01/03/2022), publicadas hacia las 16:00 CET cada día hábil salvo cierres de TARGET; resultan de una concertación diaria entre bancos centrales europeos hacia las 14:10 CET. «Solo a efectos informativos»: el BCE desaconseja su uso para transacciones. Descargas en PDF, CSV, XML, RSS y SDMX-ML (series históricas). Último dato visto: 30/10/2026.
- **Temática:** TFB-06 Datos de mercado gratuitos (principal) · secundarias: TFB-02
- **Calidad Q:** 89 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria (tipo oficial de referencia)
- **Acceso:** Abierto y gratuito
- **Ámbitos:** Tipos de referencia diarios del euro desde 1999 (incluidas divisas emergentes europeas y asiáticas)
- **Motivo de inclusión y uso:** Serie oficial homogénea y gratuita para valoraciones, contabilidad y análisis históricos. Uso: MOTOR (AG-13), CUR (AG-12) para normalizar fechas y convenciones, AS-G10N y AS-EMEA.
- **Restricciones de uso:** Uso libre con atribución; no apta para liquidar transacciones.
- **Sesgos posibles:** Fotografía de una hora concreta (no cierre de Nueva York); no recoge todas las divisas.
- **Historial de exactitud:** No aplicable (dato).
- **Cambios de propiedad o de metodología:** Reforma de 2015 tras las recomendaciones del FSB sobre referencias cambiarias; suspensión del RUB en 2022.
- **Uso en el bloque:** Motor AG-B16: conversión de divisas con tipos oficiales de referencia para comparar empresas de distintos mercados.
- **Origen:** Reutilizada con su ID de F9 Forex V1.0; temática reasignada a TFB-06 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ECB euro foreign exchange reference rates daily 16:00 CET»; WebFetch: sí)

#### FXF-0091 · Q 89 (A) — Federal Reserve Board — H.10/G.5 Foreign Exchange Rates

- **Canal oficial (URL raíz):** https://www.federalreserve.gov/RELEASES/h10/about.htm
- **Emisor:** Board of Governors of the Federal Reserve System (tipos certificados por la Fed de Nueva York)
- **Documentación y notas:** H.10 semanal con tipos diarios («noon buying rates in New York for cable transfers», certificados a efectos aduaneros) e índices nominales del dólar (Broad, AFE —economías avanzadas— y EME —emergentes—); G.5 mensual y G.5A anual; índices reales solo mensuales. Publicaciones anteriores no se revisan; la serie histórica por país se actualiza cada lunes a las 16:15. Cambio de indexación de los índices diarios desde el 24/06/2019.
- **Temática:** TFB-06 Datos de mercado gratuitos (principal) · secundarias: TFB-02
- **Calidad Q:** 89 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto (también vía FRED, RF-0001)
- **Ámbitos:** Tipos bilaterales frente al dólar e índices del dólar
- **Motivo de inclusión y uso:** Serie oficial de referencia del dólar en EE. UU. Uso: MOTOR (AG-13), AS-ESTR (AG-08, dólar amplio), Analistas de segmento.
- **Restricciones de uso:** Uso libre con atribución.
- **Sesgos posibles:** Tipo de mediodía de Nueva York (no cierre); cobertura limitada de divisas.
- **Historial de exactitud:** No aplicable (dato).
- **Cambios de propiedad o de metodología:** Cambio de 2019 en los índices diarios.
- **Uso en el bloque:** Motor AG-B16: tipos de cambio diarios y series históricas oficiales de la Fed.
- **Origen:** Reutilizada con su ID de F9 Forex V1.0; temática reasignada a TFB-06 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Federal Reserve H.10 foreign exchange rates nominal broad dollar index»; WebFetch: sí)

#### RF-0650 · Q 88 (A) — U.S. Treasury — Interest Rate Statistics (curva par diaria, letras y curva real)

- **Canal oficial (URL raíz):** https://home.treasury.gov/policy-issues/financing-the-government/interest-rate-statistics
- **Emisor:** U.S. Department of the Treasury (Office of Debt Management)
- **Temática:** TFB-06 Datos de mercado gratuitos (principal) · secundarias: TFB-02
- **Calidad Q:** 88 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria (curva oficial del emisor)
- **Acceso:** Abierto (vista de texto, ficheros XML)
- **Ámbitos:** Curva par diaria nominal (cierres de los valores recién subastados), curva par real de TIPS (desde 2004), tipos de letras (bid de cierre), tipos a largo plazo y factores de extrapolación a 30 años, medias de tipos reales a largo plazo
- **Motivo de inclusión y uso:** Curva oficial del Tesoro de EE. UU. que alimenta las constantes de vencimiento del H.15 (RF-0651); pendiente 2s10s y 3m10a, y breakevens nominal–real. AG-25; AG-24 para el tramo de letras.
- **Sesgos y cautelas:** Curva par basada solo en emisiones recientes (on-the-run); para tipos cupón cero y a plazo usar RF-0652. Cambios anunciados en los ficheros XML.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Uso en el bloque:** AG-B09 y Motor AG-B16: curva del Tesoro diaria (par y real) para tasas libres de riesgo en valoraciones.
- **Origen:** Reutilizada con su ID de F9 V3.2 (Bloque A general); temática reasignada a TFB-06 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «home.treasury.gov interest rate statistics daily treasury bill rates par yield curve real yield curve»; WebFetch: sí)

#### RF-0656 · Q 88 (A) — BCE — Curvas de rendimiento de la zona del euro (Svensson; AAA y todos los soberanos)

- **Canal oficial (URL raíz):** https://www.ecb.europa.eu/stats/financial_markets_and_interest_rates/euro_area_yield_curves/html/index.en.html (metodología: https://data.ecb.europa.eu/methodology/yield-curves · serie de ejemplo: https://data.ecb.europa.eu/data/datasets/YC/YC.B.U2.EUR.4F.G_N_W.SV_C_YM.SR_6M)
- **Emisor:** Banco Central Europeo
- **Temática:** TFB-06 Datos de mercado gratuitos (principal) · secundarias: TFB-02
- **Calidad Q:** 88 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria (estimación oficial del banco central con metodología publicada)
- **Acceso:** Abierto (publicación diaria a mediodía; conjunto YC del BCE Data Portal)
- **Ámbitos:** Curvas diarias desde el 06/09/2004 de deuda soberana de la eurozona (muestra AAA y muestra de todos los emisores centrales): cupón cero, forwards instantáneos y rendimientos par de 3 meses a 30 años, y parámetros Svensson
- **Motivo de inclusión y uso:** Curva libre de riesgo soberano del euro (AAA) y diferencial con la curva de todos los emisores como medida agregada de prima de riesgo soberano. AG-25: pendiente, forwards y valor relativo frente a OIS (€STR).
- **Sesgos y cautelas:** Excluye bonos ligados a la inflación y de cupón variable; composición AAA cambia con las calificaciones (rupturas). Conjunto específico dentro del BCE Data Portal (RF-0004).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Uso en el bloque:** AG-B09 y Motor AG-B16: curvas soberanas del euro para descontar flujos en euros.
- **Origen:** Reutilizada con su ID de F9 V3.2 (Bloque A general); temática reasignada a TFB-06 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ECB euro area yield curves Svensson AAA all government bonds spot forward rates»; WebFetch: sí, página de metodología)

#### FXF-0092 · Q 86 (A) — Federal Reserve Board — Nominal Broad Dollar Index (índice amplio del dólar)

- **Canal oficial (URL raíz):** https://www.federalreserve.gov/releases/h10/summary/jrxwtfb_nb.htm (mensual: https://www.federalreserve.gov/releases/h10/summary/jrxwtfb_nm.htm · serie en FRED: https://fred.stlouisfed.org/series/DTWEXBGS)
- **Emisor:** Board of Governors of the Federal Reserve System
- **Documentación y notas:** Índice diario ponderado por comercio de bienes y servicios (enero de 2006 = 100), con subíndices AFE y EME e índices reales mensuales. Último dato en FRED: 121,3202 (23/10/2026); la página resumen histórica de la Fed muestra la serie diaria desde el 02/01/2006.
- **Temática:** TFB-06 Datos de mercado gratuitos (principal) · secundarias: TFB-05
- **Calidad Q:** 86 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Valor efectivo del dólar frente a sus socios comerciales
- **Motivo de inclusión y uso:** Medida del «dólar amplio» más representativa que el DXY (incluye emergentes y China). Uso: AS-ESTR (AG-08, cesta del dólar amplio), TR-BCM (AG-09, régimen del dólar).
- **Restricciones de uso:** Uso libre con atribución; FRED solicita cita.
- **Sesgos y cautelas:** Ponderaciones revisadas periódicamente.
- **Historial de exactitud:** No aplicable (dato).
- **Cambios de propiedad o de metodología:** Reindexación de 2019 (ver FXF-0091).
- **Uso en el bloque:** AG-B08 Macro y Ciclo y AG-B09: efecto del dólar amplio sobre márgenes de sectores exportadores e importadores y sobre mercados emergentes; AG-B12 Seleccionador de Activos: sensibilidad cambiaria de candidatos.
- **Origen:** Reutilizada con su ID de F9 Forex V1.0; temática reasignada a TFB-06 el 2026-11-03.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Federal Reserve H.10 foreign exchange rates nominal broad dollar index»; WebFetch: sí, página resumen y serie DTWEXBGS)

#### RF-0051 · Q 85 (A) — Kenneth R. French — Data Library

- **Canal oficial (URL raíz):** https://mba.tuck.dartmouth.edu/pages/faculty/ken.french/data_library.html
- **Emisor:** Kenneth R. French (Tuck School of Business, Dartmouth College)
- **Documentación y notas:** Cada serie enlaza su página de descripción; existen páginas de archivo de versiones anteriores (p. ej., data_library_202412_archive.html). Desde la entrega de enero de 2025 las series de EE. UU. se generan con los ficheros CRSP Flat File Format 2.0 (CIZ).
- **Temática:** TFB-06 Datos de mercado gratuitos (principal) · secundarias: TFB-18
- **Calidad Q:** 85 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 14/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto (TXT y CSV)
- **Ámbitos:** Factores Fama/French de 3 y 5 factores (mensual, semanal, diario), momentum y reversión; carteras por tamaño, B/M, rentabilidad, inversión, E/P, CF/P, D/P, beta, emisiones netas, varianza; carteras sectoriales (5 a 49 industrias); breakpoints; factores de mercados desarrollados y regionales
- **Motivo de inclusión y uso:** Fuente estándar de rentabilidades de factores y carteras para atribución de rentabilidad, contraste de anomalías y primas de estilo.
- **Restricciones de uso:** Uso libre con atribución; citar la serie y el mes de la entrega (la tabla de la página cubría septiembre de 2026 en la consulta).
- **Sesgos y cautelas:** Revisiones retroactivas de las series en cada entrega (cambio CRSP CIZ en 2025): guardar la versión descargada para reproducibilidad.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Cambio de fuente de datos CRSP a formato CIZ (enero de 2025).
- **Uso en el bloque:** AG-B09 y Motor AG-B16: rentabilidades de carteras por industria (5–49 sectores) y factores para valoración relativa y momentum sectorial.
- **Origen:** Reutilizada con su ID de F9 V3.2 (Bloque A general); temática reasignada a TFB-06 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «"data_library" ken.french Current Research Returns Fama/French factors»; WebFetch: sí)

#### RF-0302 · Q 82 (A) — Cboe Global Markets — estadísticas de opciones (put/call) y VIX

- **Canal oficial (URL raíz):** http://www.cboe.com/
- **Emisor:** Cboe Global Markets
- **Documentación y notas:** Fuente original de los ratios put/call (OEX, acciones, total Cboe) publicados a diario tras el cierre, según el catálogo de indicadores de sentimiento DecisionPoint de StockCharts (chartschool.stockcharts.com), que cita cboe.com como fuente. Cboe calcula además el VIX.
- **Temática:** TFB-06 Datos de mercado gratuitos (principal) · secundarias: TFB-15
- **Calidad Q:** 82 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 14/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (estadísticas diarias); datos históricos detallados con licencia
- **Ámbitos:** Volúmenes y ratios put/call; índices de volatilidad (VIX)
- **Motivo de inclusión y uso:** Dato primario de posicionamiento en opciones y de aversión al riesgo, para señales de sentimiento contrarias.
- **Restricciones de uso:** Condiciones de Cboe; citar el ratio exacto (equity, index, total) y la fecha.
- **Sesgos y cautelas:** Bolsa con interés comercial en sus productos; los ratios dependen del universo de opciones elegido.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B10: volatilidad implícita (VIX y otros) y put/call; Motor AG-B16: series de volatilidad para escenarios.
- **Origen:** Reutilizada con su ID de F9 V3.2 (Bloque A general); temática reasignada a TFB-06 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «AAII Investor Sentiment Survey NAAIM Exposure Index Cboe put/call ratio FINRA margin statistics»; URL tomada del catálogo DecisionPoint de StockCharts, leído con WebFetch; WebFetch al sitio: no)

#### RF-0667 · Q 81 (A) — FINRA — Fixed Income Data (TRACE: agregados del mercado de bonos)

- **Canal oficial (URL raíz):** https://www.finra.org/finra-data/fixed-income (datos, informes y publicaciones TRACE: https://www.finra.org/filing-reporting/trade-reporting-and-compliance-engine-trace/trace-data-reports-publications · TRACE FactBook 2025: https://www.finra.org/sites/default/files/2026-02/TRACE_FactBook_2025.pdf)
- **Emisor:** Financial Industry Regulatory Authority (FINRA)
- **Temática:** TFB-06 Datos de mercado gratuitos (principal) · secundarias: —
- **Calidad Q:** 81 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 14/15 · Independencia 9/10 · Actualidad 10/10 · Acceso 7/10
- **Tipología:** primaria (datos de operaciones declaradas al regulador)
- **Acceso:** Consulta y agregados abiertos (aceptando el acuerdo de usuario); ficheros de fin de día, tiempo real e históricos ampliados de pago
- **Ámbitos:** Agregados diarios de actividad y sentimiento del mercado de bonos corporativos y de agencias, bonos más negociados, volumen mensual (corporativos, agencias, titulizaciones), estadísticas agregadas de negociación del Tesoro, actividad en ABS/MBS/TBA/CMO; consulta de operaciones por CUSIP
- **Motivo de inclusión y uso:** Liquidez y volumen reales del crédito de EE. UU. (no cotizaciones indicativas); detección de ventas forzadas o sequía de liquidez. AG-25. Producto distinto de las estadísticas de margen del mismo emisor (RF-0342).
- **Sesgos y cautelas:** No cubre municipales (ver EMMA/MSRB); FINRA no garantiza la exactitud; parte de los datos detallados requiere suscripción.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Uso en el bloque:** AG-B09 y AG-B12: agregados y operaciones del mercado de bonos corporativos de EE. UU. (TRACE) para la criba de emisiones.
- **Origen:** Reutilizada con su ID de F9 V3.2 (Bloque A general); temática reasignada a TFB-06 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «FINRA TRACE corporate bond market data aggregates»; WebFetch: sí)

#### RF-0052 · Q 80 (A) — Robert J. Shiller — datos online (CAPE, series largas)

- **Canal oficial (URL raíz):** https://www.irrationalexuberance.com/index.htm
- **Emisor:** Robert J. Shiller (Yale University)
- **Documentación y notas:** La web oficial del libro *Irrational Exuberance* enlaza el fichero Excel actualizado con precios, beneficios, dividendos y tipos de interés desde 1871 (base del CAPE). El dominio de datos citado en la semilla (shillerdata.com) **no** apareció en los resultados de búsqueda: no se registra; la URL exacta del fichero no se ha confirmado (los destinos de enlace no eran visibles en la lectura). Agregadores derivados (p. ej., multpl.com) no cuentan como fuente independiente.
- **Temática:** TFB-06 Datos de mercado gratuitos (principal) · secundarias: —
- **Calidad Q:** 80 (A) — Primariedad 17/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 14/15 · Independencia 10/10 · Actualidad 7/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** CAPE, dividendos, beneficios, precios del S&P y tipos desde 1871
- **Motivo de inclusión y uso:** Serie larga de valoración de la renta variable estadounidense.
- **Restricciones de uso:** Uso libre con atribución; citar versión/fecha del fichero.
- **Sesgos y cautelas:** Mantenimiento por un único autor; frecuencia de actualización irregular; Acceso rebajado a 8 hasta confirmar la URL directa de descarga.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Migración del alojamiento de datos desde econ.yale.edu (dominio vigente del fichero pendiente de confirmar en el próximo barrido HT-02).
- **Uso en el bloque:** AG-B09 y AG-B13: CAPE y series largas del S&P 500 como contexto de valoración agregada.
- **Origen:** Reutilizada con su ID de F9 V3.2 (Bloque A general); temática reasignada a TFB-06 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Robert Shiller "Online Data" stock market data used in Irrational Exuberance updated» y «"shillerdata.com"»; WebFetch: sí)
- **Alerta:** REPARAR en el próximo barrido: confirmar la URL directa del fichero de datos.

#### RF-0463 · Q 80 (A) — OCC (Options Clearing Corporation) — estadísticas de volumen y préstamo de valores

- **Emisor/organización:** The Options Clearing Corporation (OCC)
- **Año:** Publicación mensual
- **Publicación o institución:** Cámara de compensación de derivados sobre acciones (supervisada por SEC, CFTC y Reserva Federal)
- **Tipo de documento:** Estadísticas oficiales mensuales de volumen de opciones, futuros y préstamo de valores
- **Temática:** TFB-06 Datos de mercado gratuitos (principal) · secundarias: TFB-15
- **Calidad Q:** 80 (A) — Primariedad 20/20 · Exactitud histórica 10/20 · Transparencia 12/15 · Autoridad 14/15 · Independencia 9/10 · Actualidad 9/10 · Accesibilidad 6/10
- **Canal oficial (URL raíz):** https://www.theocc.com · ejemplo leído: https://www.theocc.com/newsroom/press-releases/2024/1-03-occ-reports-december-2023-and-total-2023-volume-data
- **Acceso y licencia:** Notas de prensa mensuales gratuitas; datos detallados en la web de la OCC
- **Uso en el bloque:** AG-B10: volumen de opciones y préstamo de valores en EE. UU.
- **Origen:** Reutilizada con su ID de F9 V3.2 (Bloque A general); temática reasignada a TFB-06 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «OCC Options Clearing Corporation market data volume and open interest statistics»; WebFetch: sí)
- **Contenido:** Volumen mensual y anual de opciones sobre acciones, índices y ETF, futuros y préstamo de valores en EE. UU.; indicador de actividad especulativa y de cobertura.
- **Limitaciones:** Cubre solo mercado estadounidense; el volumen no distingue compra de venta ni intención. Sustituye a RF-0317 (duplicado de Trading Economics).

#### RF-0554 · Q 80 (A) — V-Lab (NYU Stern) — análisis y previsiones de volatilidad, correlación y riesgo sistémico

- **Canal oficial (URL raíz):** https://vlab.stern.nyu.edu/ (ayuda del resumen de volatilidad: https://vlab.stern.nyu.edu/help/volatility_summary · análisis: https://vlab.stern.nyu.edu/help/volatility_analysis)
- **Emisor:** V-Lab, NYU Stern School of Business (Volatility Institute)
- **Documentación y notas:** Doce modelos de volatilidad (GARCH, GJR-GARCH por defecto, EGARCH, APARCH, Spline-GARCH, MEM, GAS, MF2-GARCH) reestimados a diario tras el cierre, con previsiones a 1 día, 1 semana, 1 mes, 6 meses y 1 año para miles de activos; además análisis de correlación, VaR a largo plazo y SRISK (riesgo sistémico).
- **Temática:** TFB-06 Datos de mercado gratuitos (principal) · secundarias: TFB-15
- **Calidad Q:** 80 (A) — Primariedad 14/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 13/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** analítica (modelos académicos sobre precios de mercado)
- **Acceso:** Abierto
- **Ámbitos:** Volatilidad realizada y prevista de acciones, índices, divisas, materias primas
- **Motivo de inclusión y uso:** Contraste de la volatilidad implícita (VIX y similares) con previsiones econométricas; régimen de volatilidad por mercado. AG-23, AG-25.
- **Restricciones de uso:** Uso académico con atribución.
- **Sesgos y cautelas:** Resultados dependientes del modelo; algunos activos inactivos conservan su último valor.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B12 Seleccionador de Activos: volatilidad prevista y correlación de candidatos concretos (acciones, ETF) para criba por riesgo; AG-B11 Sostenibilidad y Riesgos: SRISK de sectores financieros; Motor AG-B16: insumos de volatilidad para escenarios.
- **Origen:** Reutilizada con su ID de F9 V3.2 (Bloque A general); temática reasignada a TFB-06 el 2026-11-03.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «V-Lab NYU Stern volatility laboratory GARCH forecasts»; WebFetch: sí)

#### RF-0562 · Q 76 (B) — CME Group — CVOL (CME Group Volatility Indexes): volatilidad implícita de tipos, divisas y materias primas

- **Canal oficial (URL raíz):** https://www.cmegroup.com/market-data/cme-group-benchmark-administration/cme-group-volatility-indexes-faq.html (introducción: https://www.cmegroup.com/education/articles-and-reports/introduction-to-the-cme-group-volatility-index-cvol.html · guía de cálculo en tiempo real: https://www.cmegroup.com/market-data/cme-group-benchmark-administration/files/live-streaming-index-calculation-guide.pdf)
- **Emisor:** CME Group Benchmark Administration Limited (CBA)
- **Documentación y notas:** Familia de índices de volatilidad implícita a 30 días basados en varianza simple (admite precios negativos) calculados con opciones sobre futuros: tipos (STIR y bonos del Tesoro, p. ej. el de 10 años), divisas G5, agrícolas, energía, metales y un índice transversal de materias primas (32 productos más 6 índices amplios). Publica además UpVar/DnVar, sesgo (skew), convexidad y volatilidad ATM. Índices de cierre registrados bajo el BMR del Reino Unido y diseñados según los principios de IOSCO; los CVOL de Eurodólar dejaron de publicarse (historia en DataMine).
- **Temática:** TFB-06 Datos de mercado gratuitos (principal) · secundarias: TFB-12
- **Calidad Q:** 76 (B) — Primariedad 18/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 13/15 · Independencia 6/10 · Actualidad 10/10 · Acceso 6/10
- **Tipología:** primaria (índice de referencia calculado sobre precios de opciones cotizadas)
- **Acceso:** Visualizador web con últimos valores (solo consulta, no comercial); histórico de cierre en CME DataMine con registro; flujo en tiempo real vía redistribuidores
- **Ámbitos:** Volatilidad implícita de tipos de interés, divisas y materias primas
- **Motivo de inclusión y uso:** Medida homogénea de volatilidad implícita fuera de la renta variable (complemento del VIX y del MOVE, RF-0561), con sesgo put/call por mercado. AG-23, AG-25.
- **Restricciones de uso:** Visualizador solo para referencia; uso comercial con licencia.
- **Sesgos y cautelas:** Administrador que es a la vez la bolsa que lista las opciones subyacentes; historia relativamente corta (desde 2020); no comparable directamente con índices de varianza logarítmica como el VIX.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Cese de los CVOL de Eurodólar tras la transición del LIBOR.
- **Uso en el bloque:** AG-B10 Flujos y Sentimiento: volatilidad implícita y sesgo de materias primas, tipos y divisas que condicionan a sectores expuestos (energía, agrícola, metales); Motor AG-B16: insumos de volatilidad para escenarios sectoriales.
- **Origen:** Reutilizada con su ID de F9 V3.2 (Bloque A general); temática reasignada a TFB-06 el 2026-11-03.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «CME Group CVOL index methodology implied volatility rates FX commodities»; WebFetch: sí, FAQ de CVOL)

#### RF-0660 · Q 76 (B) — ICE Data Indices — ICE BofA bond indices (diferenciales ajustados por opciones)

- **Canal oficial (URL raíz):** https://fred.stlouisfed.org/data/BAMLH0A0HYM2 (distribución pública de ICE Data Indices en FRED; p. ej., también https://fred.stlouisfed.org/data/BAMLHE00EHYIOAS para el high yield en euros)
- **Emisor:** ICE Data Indices, LLC (Intercontinental Exchange; antes índices de BofA Merrill Lynch)
- **Temática:** TFB-06 Datos de mercado gratuitos (principal) · secundarias: —
- **Calidad Q:** 76 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 14/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 7/10
- **Tipología:** primaria (índices del proveedor) redistribuida en FRED
- **Acceso:** Abierto en FRED con licencia restrictiva (solo uso interno; desde abril de 2026, solo tres años de historia en FRED); historia completa de pago en ICE
- **Ámbitos:** Diferenciales ajustados por opciones (OAS), rendimientos efectivos y rentabilidades totales de índices de bonos corporativos investment grade y high yield de EE. UU., euro y emergentes, por calificación (AAA a CCC). Dato visto: OAS high yield EE. UU. 3,26 % el 29/10/2026
- **Motivo de inclusión y uso:** Serie de referencia de los diferenciales de crédito al contado (bonos), complemento de los CDS (RF-0659). AG-25: valoración del crédito por calificación y en el ciclo.
- **Sesgos y cautelas:** Reproducción y difusión a terceros requieren permiso de ICE (citar cifras puntuales con fecha, no redistribuir series); historia en FRED recortada.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Uso en el bloque:** AG-B09 y AG-B10: diferenciales de crédito por calificación (ICE BofA, accesibles vía FRED) para el coste de deuda sectorial.
- **Origen:** Reutilizada con su ID de F9 V3.2 (Bloque A general); temática reasignada a TFB-06 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ICE BofA bond indices ICE Data Indices option-adjusted spread high yield index methodology»; WebFetch: sí, página de datos de FRED)

#### RF-0553 · Q 71 (B) — WFE (World Federation of Exchanges) — estadísticas de derivados cotizados (Statistics Portal e informes semestrales)

- **Canal oficial (URL raíz):** https://statistics.world-exchanges.org (sección de estadísticas: https://www.world-exchanges.org/our-work/statistics · informe del 1S 2025, 14/08/2025: https://www.world-exchanges.org/news/articles/new-wfe-hy25-market-data-ipos-down-first-half · documento completo: https://www.world-exchanges.org/our-work/articles/h1-2025-market-highlights · reseña de FOW de los datos anuales de 2025, 27/02/2026: https://www.fow.com/insights/derivatives-trading-volume-decrease-in-2025-wfe-data)
- **Emisor:** World Federation of Exchanges
- **Documentación y notas:** Portal estadístico con volúmenes de contratos de derivados cotizados de las bolsas miembro por región, clase de activo y producto, e informes semestrales y anuales. 1S 2025: 43,92 miles de millones de contratos (−47,8 % interanual, por la regulación de opciones en la India); futuros 14,18 miles de millones (+7,8 %); Américas +11,7 % y EMEA +21,9 % interanual, Asia-Pacífico −64,8 %. Año 2025 (según FOW): 93,75 miles de millones de contratos (−47,1 %). Publica además investigación de estructura de mercado.
- **Temática:** TFB-06 Datos de mercado gratuitos (principal) · secundarias: TFB-08
- **Calidad Q:** 71 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 14/15 · Independencia 6/10 · Actualidad 8/10 · Acceso 6/10
- **Tipología:** secundaria (agregación de datos de bolsas miembro)
- **Acceso:** Notas e informes resumidos abiertos; detalle del portal con registro o suscripción
- **Ámbitos:** Derivados cotizados mundiales; contraste con FIA (RF-0542), que da cifras distintas por cobertura
- **Motivo de inclusión y uso:** Segunda fuente agregada del volumen mundial de derivados cotizados y de su reparto regional. Uso en el Bloque A Forex: Las estadísticas de la WFE incluyen volúmenes de derivados sobre divisas por bolsa miembro. TR-PFV (AG-21) para el peso relativo de las bolsas emergentes en opciones y futuros de divisas.
- **Restricciones de uso:** Uso con atribución.
- **Sesgos y cautelas:** Patronal de bolsas; cobertura limitada a miembros; el recuento por contratos mezcla tamaños muy distintos. El portal estadístico se tomó del enlace de una página oficial leída, sin cargarlo.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sustitución del antiguo informe anual IOMA de derivados por el portal estadístico y los informes de mercado semestrales (URL de pruebas antigua sustituida en esta revisión).
- **Uso en el bloque:** AG-B03 y AG-B10: estadísticas de bolsas (capitalización, volumen, admisiones) por mercado geográfico.
- **Origen:** Reutilizada con su ID de F9 Forex V1.0; temática reasignada a TFB-06 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «World Federation of Exchanges 2025 derivatives report statistics world-exchanges.org»; WebFetch: sí, nota del 1S 2025 y página de etiqueta «derivatives»)

#### MBF-0058 · Q 69 (B) — Nasdaq Data Link (antes Quandl)

- **Canal oficial (URL raíz):** https://nexusfi.com/d/data-providers/nasdaq-data-link/
- **Emisor:** Nasdaq, Inc. (adquirió Quandl en 2018)
- **Documentación y notas:** Más de 40 conjuntos abiertos de gobiernos, bancos centrales y organismos multilaterales con API REST, librerías Python/R y complemento Excel; límites gratuitos de 300 llamadas/10 s y 50.000/día; conjuntos premium a la carta. Confirmada vía índice NexusFi.
- **Temática:** TFB-06 Datos de mercado gratuitos (principal) · secundarias: TFB-12
- **Calidad Q:** 69 (B) — Primariedad 13/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 13/15 · Independencia 7/10 · Actualidad 8/10 · Acceso 7/10
- **Tipología:** secundaria (plataforma de datos)
- **Acceso:** Clave API gratuita para conjuntos abiertos; premium de pago
- **Ámbitos:** Series macro, financieras y algunas de futuros
- **Motivo de inclusión y uso:** Plataforma unificada de descarga con conjuntos abiertos y premium (futuro).
- **Restricciones de uso:** Clave gratuita; licencias de cada conjunto.
- **Sesgos y cautelas:** Muchos conjuntos gratuitos históricos ya no se actualizan; comprobar fecha.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Integración en Nasdaq (2018).
- **Uso en el bloque:** Motor AG-B16: descargas programáticas; AG-B10: series de mercado; referencia de pago (futuro) para conjuntos premium.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Nasdaq Data Link free datasets API key Quandl free data»; WebFetch: sí, página índice)
- **Origen:** Alta 2026-11-02 (F9 Bloque B V2.0, TFB-06).

#### MBF-0059 · Q 69 (B) — Databento — datos de mercado de grado institucional (de pago, futuro)

- **Canal oficial (URL raíz):** https://databento.com/docs/faqs/usage-pricing-and-data-credits
- **Emisor:** Databento
- **Documentación y notas:** Datos históricos y en directo directamente de bolsas, con crédito único de 125 USD al registrarse (caduca a los seis meses); no hay plan gratuito recurrente y exige datos de pago. Confirmada vía Índice QVeris «Free Stock API comparison» (https://qveris.ai/guides/stock-api-free-comparison/; datos comprobados el 18/08/2026).
- **Temática:** TFB-06 Datos de mercado gratuitos (principal) · secundarias: —
- **Calidad Q:** 69 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 12/15 · Independencia 8/10 · Actualidad 9/10 · Acceso 3/10
- **Tipología:** primaria (datos de bolsa normalizados)
- **Acceso:** De pago (futuro); crédito inicial
- **Ámbitos:** Datos tick, libros de órdenes, barras de bolsas de EE. UU. y otras
- **Motivo de inclusión y uso:** Referencia de pago para microestructura cuando el Bloque B necesite datos de alta frecuencia.
- **Restricciones de uso:** Licencias de bolsa; de pago.
- **Sesgos y cautelas:** Coste por volumen de datos.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** Motor AG-B16 (futuro): datos de alta frecuencia; AG-B10: liquidez y microestructura.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «free stock market data APIs list Alpha Vantage Tiingo Twelve Data Finnhub Stooq EODHD free tier»; WebFetch: sí, página índice)
- **Origen:** Alta 2026-11-02 (F9 Bloque B V2.0, TFB-06).

#### MBF-0056 · Q 68 (B) — Massive (antes Polygon.io) — API de datos de mercado

- **Canal oficial (URL raíz):** https://massive.com/docs/rest/stocks
- **Emisor:** Massive (antes Polygon.io)
- **Documentación y notas:** Plan «Stocks Basic» de 0 USD con 5 llamadas/minuto, históricos y cierres con menos de cinco años de historia y datos de referencia; tiempo real y streaming de pago. Confirmada vía Índice QVeris «Free Stock API comparison» (https://qveris.ai/guides/stock-api-free-comparison/; datos comprobados el 18/08/2026).
- **Temática:** TFB-06 Datos de mercado gratuitos (principal) · secundarias: TFB-07
- **Calidad Q:** 68 (B) — Primariedad 13/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 11/15 · Independencia 8/10 · Actualidad 9/10 · Acceso 6/10
- **Tipología:** secundaria (redistribuidor)
- **Acceso:** Gratuito con registro y límites; planes de pago
- **Ámbitos:** Acciones de EE. UU.: históricos, cierres, datos de referencia
- **Motivo de inclusión y uso:** Datos de referencia (tickers, eventos corporativos) útiles para la criba.
- **Restricciones de uso:** Condiciones del proveedor.
- **Sesgos y cautelas:** Historia corta en el plan gratuito.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Cambio de marca Polygon.io → Massive.
- **Uso en el bloque:** AG-B12: datos de referencia de tickers; Motor AG-B16: históricos recientes.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «free stock market data APIs list Alpha Vantage Tiingo Twelve Data Finnhub Stooq EODHD free tier»; WebFetch: sí, página índice)
- **Origen:** Alta 2026-11-02 (F9 Bloque B V2.0, TFB-06).

#### MBF-0055 · Q 67 (B) — Alpaca — Market Data API

- **Canal oficial (URL raíz):** https://docs.alpaca.markets/us/docs/market-data-faq
- **Emisor:** Alpaca Markets
- **Documentación y notas:** Datos de acciones de EE. UU.: tiempo real IEX gratuito y SIP con 15 minutos de retraso en el plan gratuito, WebSocket incluido; sin tope diario fijo (límites por cuenta). Confirmada vía Índice QVeris «Free Stock API comparison» (https://qveris.ai/guides/stock-api-free-comparison/; datos comprobados el 18/08/2026).
- **Temática:** TFB-06 Datos de mercado gratuitos (principal) · secundarias: —
- **Calidad Q:** 67 (B) — Primariedad 13/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 10/15 · Independencia 7/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** secundaria (redistribuidor)
- **Acceso:** Gratuito con registro; planes de pago
- **Ámbitos:** Acciones de EE. UU.: barras, operaciones y cotizaciones
- **Motivo de inclusión y uso:** Datos intradía gratuitos de EE. UU. para el Motor.
- **Restricciones de uso:** Condiciones de Alpaca; registro.
- **Sesgos y cautelas:** Plan gratuito con solo IEX en tiempo real (fracción del volumen).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** Motor AG-B16: series intradía y diarias de EE. UU.; AG-B10: volumen y flujos de corto plazo.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «free stock market data APIs list Alpha Vantage Tiingo Twelve Data Finnhub Stooq EODHD free tier»; WebFetch: sí, página índice)
- **Origen:** Alta 2026-11-02 (F9 Bloque B V2.0, TFB-06).

#### MBF-0054 · Q 66 (B) — Alpha Vantage — API de datos de mercado

- **Canal oficial (URL raíz):** https://www.alphavantage.co/documentation/
- **Emisor:** Alpha Vantage Inc.
- **Documentación y notas:** Más de 100 API: acciones, ETF, divisas, cripto, indicadores macro, fundamentales e indicadores técnicos; servicio gratuito de 25 peticiones/día con datos de cierre; datos ajustados, diferidos y en tiempo real de EE. UU. son de pago. Confirmada vía Índice QVeris «Free Stock API comparison» (https://qveris.ai/guides/stock-api-free-comparison/; datos comprobados el 18/08/2026).
- **Temática:** TFB-06 Datos de mercado gratuitos (principal) · secundarias: TFB-07
- **Calidad Q:** 66 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 10/15 · Independencia 8/10 · Actualidad 9/10 · Acceso 7/10
- **Tipología:** secundaria (redistribuidor)
- **Acceso:** Clave API gratuita (25 peticiones/día); planes de pago
- **Ámbitos:** Precios diarios, fundamentales básicos, macro, técnicos
- **Motivo de inclusión y uso:** API sencilla para prototipos de criba y descargas puntuales.
- **Restricciones de uso:** Clave gratuita; condiciones del proveedor.
- **Sesgos y cautelas:** Cupo muy bajo; calidad de ajustes a contrastar.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Cambios frecuentes de límites gratuitos.
- **Uso en el bloque:** Motor AG-B16: descargas puntuales de precios y fundamentales; AG-B12: prototipos de criba.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «free stock market data APIs list Alpha Vantage Tiingo Twelve Data Finnhub Stooq EODHD free tier»; WebFetch: sí, página índice)
- **Origen:** Alta 2026-11-02 (F9 Bloque B V2.0, TFB-06).

#### MBF-0053 · Q 65 (B) — Stooq — cotizaciones e históricos gratuitos

- **Canal oficial (URL raíz):** https://apis.io/providers/stooq/
- **Emisor:** Stooq (Polonia)
- **Documentación y notas:** Datos históricos y actuales de acciones, índices, divisas, criptoactivos, materias primas, bonos e indicadores; descarga CSV y bases completas (más de 12.000 valores) en stooq.com/db/h/. Desde principios de 2026 exige clave (obtenida con CAPTCHA) y aplica cupo diario. Confirmada vía índice apis.io.
- **Temática:** TFB-06 Datos de mercado gratuitos (principal) · secundarias: —
- **Calidad Q:** 65 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 7/15 · Autoridad 9/15 · Independencia 8/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** secundaria (agregador de datos de mercado)
- **Acceso:** Gratuito con clave y cupo diario
- **Ámbitos:** Precios diarios e intradía de mercados mundiales
- **Motivo de inclusión y uso:** Alternativa gratuita para históricos largos de índices y acciones internacionales.
- **Restricciones de uso:** Uso personal; clave gratuita (CAPTCHA); cupo diario.
- **Sesgos y cautelas:** Metodología de ajustes poco documentada; contrastar con fuentes de bolsa.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Introducción de clave obligatoria en 2026.
- **Uso en el bloque:** Motor AG-B16: históricos de precios para rentabilidades y volatilidades sectoriales; AG-B10: momentum de índices.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Stooq database historical quotes free download stooq.com db»; WebFetch: sí, página índice)
- **Origen:** Alta 2026-11-02 (F9 Bloque B V2.0, TFB-06).

#### MBF-0060 · Q 65 (B) — Econdb — datos macro agregados con API

- **Canal oficial (URL raíz):** https://www.econdb.com/
- **Emisor:** Econdb
- **Documentación y notas:** Agregador de datos macroeconómicos de numerosos proveedores oficiales; accesible desde pandas-datareader (EcondbReader) con token de API (argumento api_key, variable ECONDB_API_KEY o parámetro token). Confirmada vía documentación de pandas-datareader (https://pandas-datareader.readthedocs.io/en/stable/remote_data.html).
- **Temática:** TFB-06 Datos de mercado gratuitos (principal) · secundarias: TFB-01
- **Calidad Q:** 65 (B) — Primariedad 10/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 10/15 · Independencia 9/10 · Actualidad 8/10 · Acceso 7/10
- **Tipología:** secundaria (agregador)
- **Acceso:** Token de API (registro)
- **Ámbitos:** Series macro por país de fuentes oficiales
- **Motivo de inclusión y uso:** Acceso programático homogéneo a series macro de muchos países.
- **Restricciones de uso:** Condiciones de Econdb; citar fuente original (regla F9-b).
- **Sesgos y cautelas:** Desfase respecto a la fuente original.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** Motor AG-B16: descargas macro homogéneas; AG-B08: panel de indicadores por país.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «pandas-datareader remote data access Stooq Tiingo Alpha Vantage Nasdaq Data Link»; WebFetch: sí, página índice)
- **Origen:** Alta 2026-11-02 (F9 Bloque B V2.0, TFB-06).

#### MBF-0057 · Q 60 (C) — Marketstack — API de cierres

- **Canal oficial (URL raíz):** https://marketstack.com/documentation
- **Emisor:** Marketstack (apilayer)
- **Documentación y notas:** Plan gratuito de 100 peticiones/mes con datos de cierre y un año de historia; sin tarjeta. Confirmada vía Índice QVeris «Free Stock API comparison» (https://qveris.ai/guides/stock-api-free-comparison/; datos comprobados el 18/08/2026).
- **Temática:** TFB-06 Datos de mercado gratuitos (principal) · secundarias: —
- **Calidad Q:** 60 (C) — Primariedad 11/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 9/15 · Independencia 8/10 · Actualidad 8/10 · Acceso 5/10
- **Tipología:** secundaria (redistribuidor)
- **Acceso:** Gratuito muy limitado; planes de pago
- **Ámbitos:** Cierres diarios de bolsas mundiales
- **Motivo de inclusión y uso:** Respaldo para cierres de bolsas no cubiertas por otras fuentes.
- **Restricciones de uso:** Condiciones del proveedor.
- **Sesgos y cautelas:** Cupo mínimo; poca transparencia de origen.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** Motor AG-B16: respaldo de cierres diarios.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «free stock market data APIs list Alpha Vantage Tiingo Twelve Data Finnhub Stooq EODHD free tier»; WebFetch: sí, página índice)
- **Origen:** Alta 2026-11-02 (F9 Bloque B V2.0, TFB-06).

#### RF-0244 · Q 58 (C) — Trading Economics

- **Canal oficial (URL raíz):** https://tradingeconomics.com/ (ejemplo: https://tradingeconomics.com/sdr:ln)
- **Emisor:** Trading Economics (titularidad no declarada en la página leída)
- **Temática:** TFB-06 Datos de mercado gratuitos (principal) · secundarias: TFB-01
- **Calidad Q:** 58 (C) — Primariedad 8/20 · Historial 10/20 · Transparencia 6/15 · Autoridad 9/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 7/10
- **Tipología:** agregador con previsiones de modelo propio
- **Acceso:** Consulta abierta; API y descargas masivas de pago
- **Ámbitos:** Indicadores económicos por país, calendario, cotizaciones, consenso de beneficios y previsiones propias («global macro models projections and analysts expectations»)
- **Motivo de inclusión y uso:** Previsiones explícitas y masivas por indicador, contrastables por el Evaluador. Uso en el Bloque A Forex: Calendario económico global con previsiones y series por país. TR-BCM (AG-09) para el calendario de datos y reuniones; los Analistas de segmento para la agenda semanal (verificar siempre el dato en la fuente oficial).
- **Sesgos y cautelas:** Metodología de previsión apenas descrita; posible solape con TF-06 (decidir al fusionar).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Uso en el bloque:** AG-B08 y AG-B10: panel rápido de indicadores, calendario y cotizaciones; siempre contrastar con la fuente primaria.
- **Origen:** Reutilizada con su ID de F9 Forex V1.0; temática reasignada a TFB-06 el 2026-11-02.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Schroders insights economic and strategy viewpoint Man Group Man Institute»; WebFetch: sí)

## TFB-07 Fundamentales de empresas gratuitos

#### MBF-0201 · Q 88 (A) — SEC — EDGAR XBRL APIs (submissions, companyconcept, companyfacts, frames)

- **Canal oficial (URL raíz):** https://www.sec.gov/page/sec-api-documentation (endpoints en https://data.sec.gov/)
- **Emisor:** U.S. Securities and Exchange Commission (SEC)
- **Documentación y notas:** API JSON sin autenticación ni clave: `submissions/CIK##########.json` (historial de presentaciones), `api/xbrl/companyconcept/…` (un concepto de una empresa), `api/xbrl/companyfacts/CIK##########.json` (todos los hechos XBRL de una empresa) y `api/xbrl/frames/us-gaap/<concepto>/USD/CY2019Q1I.json` (un dato por emisor y periodo: corte transversal de todo el mercado). Descargas masivas `companyfacts.zip` y `submissions.zip`, regeneradas cada noche (~03:00 ET); latencia típica < 1 minuto en las API XBRL.
- **Temática:** TFB-07 Fundamentales de empresas gratuitos (principal) · secundarias: TFB-03
- **Calidad Q:** 88 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto (dominio público); sin clave API
- **Ámbitos:** Estados financieros XBRL (US-GAAP, IFRS, DEI) de todas las sociedades que presentan ante la SEC, por empresa y en corte transversal
- **Motivo de inclusión y uso:** Fuente primaria y gratuita de fundamentales normalizados de cotizadas en EE. UU.; `frames` permite construir en una llamada la distribución sectorial de una magnitud (ventas, margen, deuda) para todos los emisores.
- **Uso en el bloque:** AG-B09 Finanzas y Valoración y AG-B12 Seleccionador de Activos: cribado y ordenación de candidatos con datos oficiales; Motor AG-B16 (módulos MC-B de ratios, distribuciones sectoriales y valoración relativa) como entrada de datos reproducible.
- **Restricciones de uso:** Uso libre; el acceso automatizado debe cumplir la política de privacidad y seguridad de SEC.gov (Developer FAQ: identificación del agente y límites de frecuencia). Sin CORS en data.sec.gov.
- **Sesgos y cautelas:** Datos tal como los etiqueta cada emisor (etiquetas propias, errores de escala o signo); `frames` toma un hecho por emisor y periodo calendario, lo que desalinea ejercicios no naturales. Solo emisores registrados ante la SEC.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «SEC Financial Statement Data Sets XBRL companyfacts API frames data.sec.gov»; WebFetch: sí)
- **Origen:** Alta F9 Bloque B (2026-11-02).

#### MBF-0202 · Q 86 (A) — SEC — Financial Statement Data Sets (conjuntos trimestrales de estados financieros XBRL)

- **Canal oficial (URL raíz):** sec.gov (según el catálogo de datos abiertos) · Ficha de catálogo devuelta por la búsqueda: https://data.amerigeoss.org/en/dataset/financial-statement-data-sets
- **Emisor:** U.S. Securities and Exchange Commission (SEC), División de Análisis Económico y de Riesgos
- **Documentación y notas:** Ficheros trimestrales (tablas SUB, NUM, TAG, PRE) con los datos numéricos de los estados financieros primarios presentados en XBRL por todos los emisores; alternativa en bloque a la API para series largas y cortes sectoriales.
- **Temática:** TFB-07 Fundamentales de empresas gratuitos (principal) · secundarias: TFB-03
- **Calidad Q:** 86 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto (dominio público)
- **Ámbitos:** Balance, cuenta de resultados, flujos de caja y patrimonio de emisores de EE. UU., trimestre a trimestre
- **Motivo de inclusión y uso:** Base masiva y gratuita para reconstruir paneles de fundamentales por sector sin depender de agregadores comerciales.
- **Uso en el bloque:** AG-B09 y Motor AG-B16 (módulos MC-B de cribado y distribuciones sectoriales): paneles históricos para comparar candidatos con su sector; AG-B03 para cuotas de mercado y concentración por ingresos.
- **Restricciones de uso:** Uso libre; la SEC advierte de que los datos se extraen tal como se presentaron (sin corrección).
- **Sesgos y cautelas:** Requiere tratamiento (duplicados por modificaciones, etiquetas propias de cada emisor); no incluye notas en texto libre.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «SEC Financial Statement Data Sets XBRL companyfacts API frames data.sec.gov» → ficha de catálogo «Financial Statement Data Sets» en data.amerigeoss.org; WebFetch: no)
- **Origen:** Alta F9 Bloque B (2026-11-02).

#### MBF-0620 · Q 84 (A) — CSA (Canadian Securities Administrators) — SEDAR+: documentación de emisores canadienses

- **Canal oficial (URL raíz):** https://www.securities-administrators.ca/?p=2379 (sistema: sedarplus.ca · lanzamiento: https://fcnb.ca/en/news-alerts/sedar-filing-system-to-launch-july-25)
- **Emisor:** Canadian Securities Administrators (CSA), consejo de los reguladores provinciales y territoriales de valores
- **Documentación y notas:** Plataforma web para presentar, divulgar y consultar información de los mercados de capitales canadienses; sustituye a SEDAR, CTO, DL, SEDI, NRD y NRS (lanzamiento el 25/07/2023). Búsqueda pública de perfiles de emisores y documentos presentados (estados financieros, informes de gestión y prospectos).
- **Temática:** TFB-07 Fundamentales de empresas gratuitos (principal) · secundarias: TFB-03
- **Calidad Q:** 84 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** primaria (registro regulatorio)
- **Acceso:** Abierto para consulta pública
- **Ámbitos:** Estados financieros, MD&A, AIF y hechos relevantes de emisores canadienses
- **Motivo de inclusión y uso:** Equivalente canadiense de EDGAR: fuente primaria de los fundamentales de mineras, energéticas y bancos canadienses.
- **Restricciones de uso:** Condiciones de uso de SEDAR+; sin descarga masiva documentada.
- **Sesgos y cautelas:** La búsqueda pública recibió críticas de usabilidad tras el lanzamiento; no ofrece API estructurada (XBRL) como EDGAR.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Consolidación de sistemas en SEDAR+ (2023).
- **Uso en el bloque:** AG-B12 Seleccionador de Activos y AG-B09 Finanzas y Valoración: estados financieros primarios de candidatos canadienses (minería, energía, banca); AG-B05: informes técnicos de proyectos mineros.
- **Origen:** Alta F9_comp (2026-11-03).
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-03 (búsqueda web: «SEDAR+ public search issuer filings Canadian Securities Administrators»; WebFetch: sí, página de la CSA, que no detalla la búsqueda pública)

#### MBF-0205 · Q 82 (A) — Banco de España — Central de Balances (resultados anuales y trimestrales de las empresas no financieras)

- **Canal oficial (URL raíz):** https://www.bde.es/wbe/es/publicaciones/informacion-estadistica/central-balances/ (ejemplo devuelto por la búsqueda: …/central-balances--resultados-anuales-empresas-no-financieras-2012.html)
- **Emisor:** Banco de España — Central de Balances
- **Documentación y notas:** Publicaciones anuales y trimestrales con la actividad, resultados, rentabilidad, endeudamiento y carga financiera de las sociedades no financieras españolas, desagregadas por sector y tamaño; base de las ratios sectoriales del Banco de España.
- **Temática:** TFB-07 Fundamentales de empresas gratuitos (principal) · secundarias: TFB-02
- **Calidad Q:** 82 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 14/15 · Independencia 10/10 · Actualidad 7/10 · Acceso 9/10
- **Tipología:** primaria (estadística agregada)
- **Acceso:** Abierto
- **Ámbitos:** Rentabilidad, márgenes, endeudamiento y empleo por sector de actividad en España
- **Motivo de inclusión y uso:** Referencia oficial de márgenes y rentabilidades sectoriales en España para situar a una empresa frente a su sector.
- **Uso en el bloque:** AG-B09 Finanzas y Valoración (benchmarks sectoriales de ROA, ROE, margen y apalancamiento) y AG-B03 (estructura de sectores españoles); Motor AG-B16 (MC-B de comparación con distribuciones sectoriales).
- **Restricciones de uso:** Uso libre con cita del Banco de España.
- **Sesgos y cautelas:** Muestra de colaboración voluntaria (sobrerrepresenta empresas grandes en la trimestral); desfase de publicación anual.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Reorganización del portal bde.es (rutas /wbe/).
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «BACH database ECCBSO harmonised financial statements non-financial companies Banco de España Central de Balances»; WebFetch: no)
- **Origen:** Alta F9 Bloque B (2026-11-02).

#### MBF-0203 · Q 81 (A) — XBRL International — filings.xbrl.org (repositorio de informes ESEF, UKSEF y Ucrania)

- **Canal oficial (URL raíz):** https://filings.xbrl.org/ (acerca de: https://filings.xbrl.org/about.html)
- **Emisor:** XBRL International (con apoyo de Workiva; visor Arelle de código abierto)
- **Documentación y notas:** Repositorio de informes financieros anuales en Inline XBRL de emisores cotizados europeos (formato ESEF), del Reino Unido (UKSEF) y de Ucrania; para cada informe ofrece visor iXBRL, datos en xBRL-JSON y el paquete original. API JSON-API en filings.xbrl.org/api/filings (documentación limitada). Faltan Alemania e Irlanda (sus ESEF no pueden descubrirse de forma fiable).
- **Temática:** TFB-07 Fundamentales de empresas gratuitos (principal) · secundarias: TFB-03
- **Calidad Q:** 81 (A) — Primariedad 17/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 13/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** primaria (copia de los informes oficiales)
- **Acceso:** Abierto
- **Ámbitos:** Estados financieros consolidados NIIF etiquetados de cotizadas europeas
- **Motivo de inclusión y uso:** Única vía gratuita y en bloque para extraer fundamentales normalizados de cotizadas europeas, a la espera del punto de acceso único europeo (ESAP).
- **Uso en el bloque:** AG-B09 y AG-B12: fundamentales de candidatos europeos; Motor AG-B16 (MC-B de ratios y comparables) con datos xBRL-JSON.
- **Restricciones de uso:** Según la propia página, «no hay restricciones» actuales de uso de los datos; citar emisor, LEI y fecha.
- **Sesgos y cautelas:** Repositorio incompleto; muchos informes con errores o avisos de validación; fecha de alta («added») puede ir muy por detrás de la presentación real; ESEF solo etiqueta en detalle los estados primarios (notas en bloque).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «filings.xbrl.org ESEF annual financial reports database XBRL International»; WebFetch: sí)
- **Origen:** Alta F9 Bloque B (2026-11-02).

#### MBF-0204 · Q 81 (A) — BACH (Bank for the Accounts of Companies Harmonised) — estados financieros agregados de empresas no financieras europeas

- **Canal oficial (URL raíz):** https://www.bach.banque-france.fr/?lang=en · Descripción en el Banco de España: https://www.bde.es/wbe/en/areas-actuacion/central-balances/bases-de-datos-y-aplicaciones/base-de-datos-bach/
- **Emisor:** Comité Europeo de Centrales de Balances (ECCBSO); alojada por la Banque de France y documentada por el Banco de España
- **Documentación y notas:** Balances, cuentas de resultados y ratios significativas de sociedades no financieras de 12 países de la UE (Alemania, Austria, Bélgica, Croacia, España, Francia, Hungría, Italia, Luxemburgo, Polonia, Portugal y Eslovaquia), 104 sectores y 5 tamaños por cifra de negocios, desde 2000; valores en porcentaje y absolutos y distribuciones por cuartiles.
- **Temática:** TFB-07 Fundamentales de empresas gratuitos (principal) · secundarias: TFB-01
- **Calidad Q:** 81 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 14/15 · Independencia 10/10 · Actualidad 6/10 · Acceso 9/10
- **Tipología:** primaria (estadística agregada armonizada)
- **Acceso:** Abierto (consulta y descarga en el portal BACH)
- **Ámbitos:** Estructura financiera, rentabilidad y márgenes por sector, tamaño y país en Europa
- **Motivo de inclusión y uso:** Permite comparar márgenes, rentabilidad y endeudamiento de un sector entre países europeos con cuartiles (no solo medias).
- **Uso en el bloque:** AG-B09 (benchmarks sectoriales con cuartiles), AG-B03 (estructura y tamaño de empresas por país), Motor AG-B16 (MC-B de posicionamiento de un candidato en la distribución sectorial).
- **Restricciones de uso:** Uso con cita de BACH/ECCBSO.
- **Sesgos y cautelas:** Cobertura y representatividad de las muestras nacionales desiguales (la propia documentación lo advierte); datos anuales con desfase de uno a dos años; incluye empresas no cotizadas.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «BACH database ECCBSO harmonised financial statements non-financial companies Banco de España Central de Balances»; WebFetch: sí, sobre la página del Banco de España)
- **Origen:** Alta F9 Bloque B (2026-11-02).

#### RF-0050 · Q 81 (A) — Damodaran Online

- **Canal oficial (URL raíz):** https://pages.stern.nyu.edu/~adamodar/New_Home_Page/home.htm
- **Emisor:** Aswath Damodaran (NYU Stern School of Business)
- **Documentación y notas:** Sección de datos con rentabilidades históricas (acciones, bonos, inmobiliario, oro), ERP implícita mensual (desde 09/2008) y anual (desde 1960), primas de riesgo país (CRP); archivo de años anteriores. Última actualización general vista: 09/01/2026; CRP: 01/07/2026; próxima: enero de 2027.
- **Temática:** TFB-07 Fundamentales de empresas gratuitos (principal) · secundarias: TFB-11
- **Calidad Q:** 81 (A) — Primariedad 16/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 14/15 · Independencia 9/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** secundaria
- **Acceso:** Abierto
- **Ámbitos:** Prima de riesgo implícita, múltiplos y costes de capital por sector y país, primas de riesgo país
- **Motivo de inclusión y uso:** Conjuntos de datos de valoración con metodología explicada; referencia para ERP y coste de capital en AC de valoración.
- **Uso en el bloque:** AG-B09 Finanzas y Valoración: múltiplos, márgenes, ROIC, betas y coste de capital por sector (EE. UU., Europa, emergentes, global) como referencia para comparar candidatos; AG-B12 y MC-B de valoración relativa.
- **Restricciones de uso:** Uso libre con atribución; citar fichero y fecha de actualización.
- **Sesgos y cautelas:** Un solo autor y supuestos propios; actualización general anual (datos sectoriales desfasados a lo largo del año).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Damodaran Online data current NYU Stern»; WebFetch: sí)
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0235 · Q 78 (B) — FactSet Insight — Earnings Insight (John Butters)

- **Canal oficial (URL raíz):** https://insight.factset.com/ (ejemplo: https://insight.factset.com/sp-500-earnings-season-update-february-13-2026)
- **Emisor:** FactSet (John Butters, Vice President y Senior Earnings Analyst)
- **Temática:** TFB-07 Fundamentales de empresas gratuitos (principal) · secundarias: TFB-10
- **Calidad Q:** 78 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 13/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 8/10
- **Tipología:** primaria (agregados de consenso propios)
- **Acceso:** Abierto
- **Ámbitos:** Temporada de resultados del S&P 500: crecimiento combinado de beneficios e ingresos, porcentaje de sorpresas positivas, PER adelantado a 12 meses frente a medias a 5 y 10 años
- **Motivo de inclusión y uso:** Serie semanal de referencia sobre beneficios y valoración del S&P 500 (p. ej., 13/02/2026: beneficio combinado del 4T 2025 +13,2 %, PER adelantado de 21,5). Uso: estado de los beneficios y del consenso.
- **Uso en el bloque:** AG-B09: crecimiento de beneficios, sorpresas y revisiones agregadas por sector del S&P 500; AG-B12 para contrastar expectativas de un candidato frente a su sector.
- **Sesgos y cautelas:** Basada en el consenso de analistas (sesgo optimista conocido de las previsiones).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «FactSet Earnings Insight John Butters S&P 500»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 3).
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### MBF-0216 · Q 77 (B) — Banco de España — BELab: microdatos iBACH de empresas españolas y portuguesas

- **Canal oficial (URL raíz):** https://www.bde.es/wbe/en/para-ciudadano/servicios/belab/contenido/microdatos-disponibles/microdatos-de-empresas-espanolas-y-portuguesas--ibach-.html (versión en español en …/wbe/es/punto-informacion/…)
- **Emisor:** Banco de España — Laboratorio de datos BELab
- **Documentación y notas:** Microdatos anonimizados de estados financieros de empresas (versión individual de BACH, iBACH) de España y Portugal, accesibles para investigación a través de BELab.
- **Temática:** TFB-07 Fundamentales de empresas gratuitos (principal) · secundarias: TFB-18
- **Calidad Q:** 77 (B) — Primariedad 19/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 14/15 · Independencia 10/10 · Actualidad 5/10 · Acceso 5/10
- **Tipología:** primaria (microdatos)
- **Acceso:** Restringido: solicitud de acceso para investigación (gratuito, sujeto a aprobación)
- **Ámbitos:** Distribuciones empresa a empresa de márgenes, productividad y endeudamiento
- **Motivo de inclusión y uso:** Permite análisis de dispersión intrasectorial (colas, concentración) que los agregados no muestran.
- **Uso en el bloque:** AG-B03 Estructura y Competencia (dispersión de márgenes, concentración) y Motor AG-B16 en estudios de fondo; uso puntual y planificado por el plazo de acceso.
- **Restricciones de uso:** Solo investigación; condiciones de confidencialidad de BELab; credenciales en HT-01, nunca en este archivo.
- **Sesgos y cautelas:** Acceso no inmediato; datos anonimizados (no identifican candidatos concretos).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «BACH database ECCBSO harmonised financial statements non-financial companies Banco de España Central de Balances»; WebFetch: no)
- **Origen:** Alta F9 Bloque B (2026-11-02).

#### RF-0454 · Q 75 (B) — Musings on Markets (Aswath Damodaran)

- **Canal oficial (URL raíz):** https://aswathdamodaran.blogspot.com/ (réplica: https://aswathdamodaran.substack.com/)
- **Emisor:** Aswath Damodaran (NYU Stern)
- **Temática:** TFB-07 Fundamentales de empresas gratuitos (principal) · secundarias: TFB-11
- **Calidad Q:** 75 (B) — Primariedad 10/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 14/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** secundaria (valoración con modelos y datos publicados)
- **Acceso:** Abierto
- **Ámbitos:** Valoración de empresas, primas de riesgo, tipos de interés y bolsa, OPV (p. ej., valoración de la OPV de Anthropic, 28/10)
- **Motivo de inclusión y uso:** Valoraciones razonadas con hojas de cálculo descargables; contraste de narrativas de mercado. AC-RV.
- **Uso en el bloque:** AG-B09: marco y comentarios de valoración sectorial y de casos concretos que acompañan a los datos de Damodaran Online; AG-B14 Contrarias para contrastar narrativas.
- **Sesgos y cautelas:** Opinión de autor; valoraciones sensibles a supuestos.
- **Criterios anti-manipulación:** Autor académico identificado que publica sus datos y modelos (complementa RF-0050); BFA reproduce los supuestos antes de usarlos.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Aswath Damodaran Musings on Markets blog»; WebFetch: sí, archivo de Substack; la página de NYU Stern redirige al blog)
- **Origen:** Alta F9_S3, tanda 3 (2026-11-02).
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### MBF-0206 · Q 62 (C) — Macrotrends — series largas de precios y fundamentales

- **Canal oficial (URL raíz):** macrotrends.net (según el índice) · Ficha comparativa leída: https://www.findmymoat.com/vs/macrotrends-vs-stockoscope
- **Emisor:** Macrotrends LLC
- **Documentación y notas:** Más de 50 años de precios y dividendos cuando existen, 10 años de fundamentales trimestrales, gráficos históricos de índices, metales, energía, divisas, tipos y economía; cribador con más de 50 criterios; comparación de acciones de EE. UU. y extranjeras. Solo web, sin API. Plan gratuito y suscripción «Premium Access».
- **Temática:** TFB-07 Fundamentales de empresas gratuitos (principal) · secundarias: TFB-06
- **Calidad Q:** 62 (C) — Primariedad 10/20 · Historial 10/20 · Transparencia 7/15 · Autoridad 9/15 · Independencia 8/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** secundaria (agregador)
- **Acceso:** Freemium (sin registro para la consulta básica)
- **Ámbitos:** Históricos de ingresos, márgenes, BPA, múltiplos y precios por empresa
- **Motivo de inclusión y uso:** Visión rápida de 10+ años de una empresa candidata para detectar ciclos de márgenes y crecimiento.
- **Uso en el bloque:** AG-B12 (primer vistazo a candidatos) y AG-B09 (contexto histórico); cifras finales siempre desde MBF-0201/MBF-0203 o informes oficiales.
- **Restricciones de uso:** Sin API; no apto para extracción automatizada; citar página y fecha de consulta.
- **Sesgos y cautelas:** Fuentes y método de normalización no documentados; posibles errores en ajustes por splits y moneda.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «free stock fundamentals data sites Macrotrends Stockanalysis Financial Modeling Prep Simply Wall St comparison»; WebFetch: sí, sobre la página índice findmymoat.com)
- **Origen:** Alta F9 Bloque B (2026-11-02).

#### MBF-0207 · Q 62 (C) — Stock Analysis (stockanalysis.com) — fundamentales, cribador y comparador

- **Canal oficial (URL raíz):** stockanalysis.com (según el índice) · Página índice leída: https://alternativeto.net/software/stockanalysis-com
- **Emisor:** Stock Analysis (empresa privada)
- **Documentación y notas:** Información gratuita sobre más de 100.000 acciones y fondos mundiales, con cribador, herramientas de comparación y gráficos avanzados; modelo freemium.
- **Temática:** TFB-07 Fundamentales de empresas gratuitos (principal) · secundarias: TFB-08
- **Calidad Q:** 62 (C) — Primariedad 10/20 · Historial 10/20 · Transparencia 7/15 · Autoridad 9/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 8/10
- **Tipología:** secundaria (agregador)
- **Acceso:** Freemium
- **Ámbitos:** Estados financieros, ratios, estimaciones, ETF y listas por sector
- **Motivo de inclusión y uso:** Navegación rápida de estados financieros y listas sectoriales de acciones y ETF.
- **Uso en el bloque:** AG-B12 (cribas y listas por sector o industria) y AG-B09 (comparativas rápidas); contraste con fuentes primarias.
- **Restricciones de uso:** Funciones avanzadas y descargas de pago; uso personal.
- **Sesgos y cautelas:** Datos de proveedores terceros sin documentación metodológica pública detallada.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «free stock fundamentals data sites Macrotrends Stockanalysis Financial Modeling Prep Simply Wall St comparison»; WebFetch: sí, sobre la página índice alternativeto.net)
- **Origen:** Alta F9 Bloque B (2026-11-02).

#### MBF-0212 · Q 62 (C) — SimFin — fundamentales normalizados con descarga masiva y API

- **Canal oficial (URL raíz):** https://simfin.com/ (precios: https://simfin.com/en/prices; descarga: https://simfin.com/en/fundamental-data-download; librería Python: https://github.com/SimFin/simfin)
- **Emisor:** SimFin (empresa privada)
- **Documentación y notas:** Plan gratuito (0 $, sin tarjeta): 5.000 acciones de EE. UU., 5 años de fundamentales (la tabla comparativa indica 7 en la API) y precios, descarga masiva con retraso, API web a 2 llamadas/s, cribador y backtesting básico. Excluye en gratis ratios calculadas (PEG, EV, FCF) y variantes «as reported». Planes de pago START 15 $/mes, BASIC 35 $/mes, PRO 71 $/mes (facturación anual).
- **Temática:** TFB-07 Fundamentales de empresas gratuitos (principal)
- **Calidad Q:** 62 (C) — Primariedad 11/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 9/15 · Independencia 8/10 · Actualidad 8/10 · Acceso 7/10
- **Tipología:** secundaria (agregador normalizado)
- **Acceso:** Freemium; registro gratuito y clave API gratuita
- **Ámbitos:** Estados financieros normalizados y precios de acciones de EE. UU.
- **Motivo de inclusión y uso:** Paneles listos para análisis (CSV y Python) que ahorran limpieza frente a XBRL bruto; útil como contraste de MBF-0201.
- **Uso en el bloque:** Motor AG-B16 (MC-B de cribado y prototipos de factores) y AG-B12 para cribas rápidas; las cifras finales se contrastan con la SEC.
- **Restricciones de uso:** Registro y clave API gratuitos; según sus FAQ, los datos descargados deben borrarse al cancelar la cuenta y solo pueden usarse con suscripción vigente. Licencia restrictiva para redistribución.
- **Sesgos y cautelas:** Historia corta en el plan gratuito; normalización propia no auditada; solo EE. UU. en gratuito.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «SimFin free bulk download fundamentals Alpha Vantage fundamental data API free key Finnhub OpenBB»; WebFetch: sí, página de precios)
- **Origen:** Alta F9 Bloque B (2026-11-02).

#### MBF-0213 · Q 62 (C) — Wikipedia — artículos de índices bursátiles con tablas de constituyentes

- **Canal oficial (URL raíz):** https://en.wikipedia.org/ (pieza verificada: https://en.wikipedia.org/wiki/EURO_STOXX_50)
- **Emisor:** Fundación Wikimedia (contenido colaborativo)
- **Documentación y notas:** Los artículos de índices (S&P 500, EURO STOXX 50, IBEX 35, DAX, etc.) suelen incluir tablas de constituyentes con ticker, sector y sede. Pieza leída: EURO STOXX 50, tabla de 50 componentes con ticker, mercado principal, forma societaria, sede, sector y año de fundación, a fecha 22/09/2025; reparto por país (Alemania 17, Francia 15, Países Bajos 8, España 4, Italia 4, Bélgica 1, Finlandia 1).
- **Temática:** TFB-07 Fundamentales de empresas gratuitos (principal) · secundarias: TFB-08
- **Calidad Q:** 62 (C) — Primariedad 8/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 8/15 · Independencia 9/10 · Actualidad 7/10 · Acceso 10/10
- **Tipología:** terciaria (enciclopedia colaborativa)
- **Acceso:** Abierto (CC BY-SA)
- **Ámbitos:** Listas de constituyentes de índices y datos básicos de empresas
- **Motivo de inclusión y uso:** Punto de partida rápido y legible por máquina para construir el universo inicial de un índice o sector.
- **Uso en el bloque:** AG-B12 Seleccionador de Activos (universo inicial de candidatos) y Motor AG-B16 (lista de identificadores); la composición vigente se confirma siempre con el proveedor del índice (TFB-08).
- **Restricciones de uso:** CC BY-SA: atribución y compartir igual; citar revisión y fecha.
- **Sesgos y cautelas:** Puede ir por detrás de las revisiones del índice (la pieza leída está fechada en septiembre de 2025); editable por cualquiera; no es fuente para hechos.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Wikipedia List of S&P 500 companies constituents EURO STOXX 50 IBEX 35»; WebFetch: sí, artículo EURO STOXX 50)
- **Origen:** Alta F9 Bloque B (2026-11-02).

#### MBF-0210 · Q 60 (C) — Koyfin — plataforma de datos de mercado y fundamentales (plan gratuito)

- **Canal oficial (URL raíz):** koyfin.com (según el índice) · Página índice: https://alternativeto.net/software/stockanalysis-com
- **Emisor:** Koyfin (empresa privada)
- **Documentación y notas:** Plataforma freemium de gráficos, fundamentales, estimaciones y paneles; listada como alternativa a Stock Analysis.
- **Temática:** TFB-07 Fundamentales de empresas gratuitos (principal) · secundarias: TFB-06
- **Calidad Q:** 60 (C) — Primariedad 10/20 · Historial 10/20 · Transparencia 7/15 · Autoridad 9/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 6/10
- **Tipología:** secundaria (agregador)
- **Acceso:** Freemium; registro gratuito
- **Ámbitos:** Fundamentales, múltiplos, estimaciones y comparables globales
- **Motivo de inclusión y uso:** Tablas de comparables y múltiplos por sector con gráficos históricos.
- **Uso en el bloque:** AG-B09 (comparables y múltiplos) y AG-B12 (cribas); contraste con fuentes primarias.
- **Restricciones de uso:** Registro gratuito; funciones avanzadas de pago; credenciales en HT-01.
- **Sesgos y cautelas:** Dependencia de proveedores de datos terceros; límites del plan gratuito.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «free stock fundamentals data sites Macrotrends Stockanalysis Financial Modeling Prep Simply Wall St comparison»; WebFetch: sí, sobre la página índice alternativeto.net)
- **Origen:** Alta F9 Bloque B (2026-11-02).

#### MBF-0621 · Q 60 (C) — Finviz — cribador de acciones y mapas de calor (versión gratuita)

- **Canal oficial (URL raíz):** https://www.tikr.com/blog/tikr-vs-finviz-which-stock-screener-is-better (comparativas que describen Finviz; sitio: finviz.com) · https://www.stockrover.com/?p=46612
- **Emisor:** FINVIZ.com, Inc.
- **Documentación y notas:** Cribador de acciones centrado en EE. UU. con unos 70 filtros fijos descriptivos, fundamentales y técnicos, mapas de calor instantáneos y 8 años de historia; la versión Elite (de pago, unos 25 USD/mes con pago anual) añade tiempo real. Considerado por comparativas de 2026 el mejor cribador gratuito.
- **Temática:** TFB-07 Fundamentales de empresas gratuitos (principal) · secundarias: TFB-06
- **Calidad Q:** 60 (C) — Primariedad 9/20 · Historial 10/20 · Transparencia 7/15 · Autoridad 9/15 · Independencia 6/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** secundaria (agregador comercial)
- **Acceso:** Gratuito con limitaciones; Elite de pago (futuro)
- **Ámbitos:** Acciones de EE. UU.: criba por ratios, sectores e indicadores técnicos
- **Motivo de inclusión y uso:** Criba rápida y gratuita de candidatos por sector y ratios para preparar listas largas.
- **Restricciones de uso:** Condiciones de Finviz; sin redistribución.
- **Sesgos y cautelas:** Descrito solo por comparativas de competidores (sesgo comercial); datos de proveedores terceros y cotizaciones diferidas en la versión gratuita.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B12 Seleccionador de Activos: criba inicial de candidatos de EE. UU. por sector, valoración y calidad; AG-B03: mapa de capitalizaciones por industria.
- **Origen:** Alta F9_comp (2026-11-03).
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-03 (búsqueda web: «free stock screener fundamentals comparison Finviz GuruFocus Zacks Morningstar»; WebFetch: sí, comparativas de TIKR y Stock Rover; finviz.com no se leyó)

#### MBF-0209 · Q 59 (C) — Financial Modeling Prep (FMP) — API de fundamentales (plan gratuito)

- **Canal oficial (URL raíz):** financialmodelingprep.com (según el índice) · Página índice leída: https://alternativeto.net/software/financial-modeling-prep
- **Emisor:** Financial Modeling Prep (empresa privada)
- **Documentación y notas:** Sitio y API con cotizaciones, noticias, datos de mercados internacionales y estados financieros; listado como gratuito en el índice (con niveles de pago para volumen y cobertura).
- **Temática:** TFB-07 Fundamentales de empresas gratuitos (principal) · secundarias: TFB-06
- **Calidad Q:** 59 (C) — Primariedad 10/20 · Historial 10/20 · Transparencia 7/15 · Autoridad 8/15 · Independencia 8/10 · Actualidad 9/10 · Acceso 7/10
- **Tipología:** secundaria (agregador)
- **Acceso:** Freemium; clave API gratuita con límites
- **Ámbitos:** Estados financieros, ratios, perfiles de empresa y calendarios
- **Motivo de inclusión y uso:** API sencilla para prototipos de cribado cuando no hay XBRL (emisores no estadounidenses).
- **Uso en el bloque:** Motor AG-B16 (MC-B de cribado) y AG-B12; cifras finales contrastadas con fuentes primarias.
- **Restricciones de uso:** Registro y clave API gratuitos; límites de llamadas; redistribución restringida.
- **Sesgos y cautelas:** Calidad variable fuera de EE. UU.; la página índice no detalla el plan gratuito (comprobar condiciones vigentes antes de usar).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «free stock fundamentals data sites Macrotrends Stockanalysis Financial Modeling Prep Simply Wall St comparison»; WebFetch: sí, sobre la página índice alternativeto.net)
- **Origen:** Alta F9 Bloque B (2026-11-02).

#### MBF-0623 · Q 58 (C) — Stock Rover — investigación fundamental y cribador (plan gratuito limitado)

- **Canal oficial (URL raíz):** https://www.stockrover.com/?p=46612 (sitio: stockrover.com)
- **Emisor:** Stock Rover (Investors Edge)
- **Documentación y notas:** Plataforma de investigación con más de 800 métricas, hasta 20 años de fundamentales, gráficos fundamentales completos, sincronización con intermediarios e informes de cartera; plan gratuito limitado y planes de 29 a 79 USD/mes (pago anual), prueba de 14 días. Página verificada el 01/11/2026.
- **Temática:** TFB-07 Fundamentales de empresas gratuitos (principal) · secundarias: TFB-06
- **Calidad Q:** 58 (C) — Primariedad 9/20 · Historial 10/20 · Transparencia 8/15 · Autoridad 9/15 · Independencia 5/10 · Actualidad 10/10 · Acceso 7/10
- **Tipología:** secundaria (agregador comercial)
- **Acceso:** Freemium: plan gratuito limitado; planes de pago (futuro)
- **Ámbitos:** Fundamentales históricos y ratios de compañías cotizadas
- **Motivo de inclusión y uso:** Series largas de ratios para comparar candidatos y medir consistencia de márgenes y rentabilidades.
- **Restricciones de uso:** Condiciones de Stock Rover; sin redistribución.
- **Sesgos y cautelas:** Página propia con comparativas interesadas; sin futuros ni divisas; detalles del plan gratuito no especificados.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B12 Seleccionador de Activos: criba con métricas de calidad y crecimiento a 10–20 años; AG-B09: históricos de márgenes y retorno sobre capital.
- **Origen:** Alta F9_comp (2026-11-03).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-03 (búsqueda web: «free stock screener fundamentals comparison Finviz GuruFocus Zacks Morningstar»; WebFetch: sí)

#### RF-0260 · Q 58 (C) — MarketScreener

- **Canal oficial (URL raíz):** https://www.marketscreener.com/ (ejemplo leído: https://www.marketscreener.com/news/bofa-sees-resilient-consumers-despite-higher-gas-prices-ce7f59d8de8aff26)
- **Emisor:** Surperformance SAS (grupo Zonebourse)
- **Temática:** TFB-07 Fundamentales de empresas gratuitos (principal) · secundarias: TFB-10
- **Calidad Q:** 58 (C) — Primariedad 8/20 · Historial 10/20 · Transparencia 8/15 · Autoridad 8/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 7/10
- **Tipología:** agregador (noticias sindicadas de MT Newswires, datos de FactSet, Morningstar y S&P Capital IQ)
- **Acceso:** Abierto con registro; funciones de suscripción
- **Ámbitos:** Noticias breves por empresa, calendarios económicos y corporativos, cotizaciones, filtros
- **Motivo de inclusión y uso:** Agregador multimercado con ediciones por país, útil para localizar noticias y calendarios por emisor. Uso: localización; se cita la fuente original (regla F9 b).
- **Uso en el bloque:** AG-B12 Seleccionador de Activos: ficha rápida de empresas cotizadas europeas (consenso, calendario, accionistas); AG-B09 para estimaciones de consenso, siempre contrastadas con el informe oficial.
- **Sesgos y cautelas:** Contenido mayoritariamente sindicado; las marcas de tiempo pueden no coincidir con la publicación original.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Bank of America Institute Consumer Checkpoint»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 3).
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### MBF-0208 · Q 57 (C) — Simply Wall St — análisis visual de fundamentales (plan gratuito)

- **Canal oficial (URL raíz):** simplywall.st (según el índice) · Páginas índice: https://alternativeto.net/software/simply-wall-st y https://alternativeto.net/software/stockanalysis-com
- **Emisor:** Simply Wall St Pty Ltd
- **Documentación y notas:** Plataforma freemium que resume la situación financiera, valoración (modelo DCF propio), crecimiento y dividendos de acciones globales en gráficos («snowflake»); vista gratuita limitada.
- **Temática:** TFB-07 Fundamentales de empresas gratuitos (principal) · secundarias: TFB-11
- **Calidad Q:** 57 (C) — Primariedad 8/20 · Historial 10/20 · Transparencia 8/15 · Autoridad 9/15 · Independencia 7/10 · Actualidad 9/10 · Acceso 6/10
- **Tipología:** secundaria (agregador con modelos propios)
- **Acceso:** Freemium; registro gratuito
- **Ámbitos:** Salud financiera, propiedad, valoración estimada y comparables
- **Motivo de inclusión y uso:** Resumen rápido de accionariado y salud financiera de candidatos fuera de EE. UU.
- **Uso en el bloque:** AG-B12 (vista rápida) y AG-B14 Contrarias (contraste de valoraciones de terceros); sus valores razonables son opinión de modelo, nunca prueba.
- **Restricciones de uso:** Número limitado de consultas en el plan gratuito; credenciales en HT-01.
- **Sesgos y cautelas:** Valoraciones automáticas sensibles a supuestos; orientación al inversor minorista.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «free stock fundamentals data sites Macrotrends Stockanalysis Financial Modeling Prep Simply Wall St comparison»; WebFetch: sí, sobre la página índice alternativeto.net/software/stockanalysis-com)
- **Origen:** Alta F9 Bloque B (2026-11-02).

#### MBF-0622 · Q 57 (C) — TIKR — terminal de fundamentales y cribador (plan gratuito)

- **Canal oficial (URL raíz):** https://www.tikr.com/blog/tikr-vs-finviz-which-stock-screener-is-better (sitio: tikr.com)
- **Emisor:** TIKR, Inc.
- **Documentación y notas:** Terminal de fundamentales con cobertura de más de 56.000 acciones mundiales en los planes Plus y Pro (Pro 29,95 USD/mes con pago anual); el plan gratuito permite cribar solo compañías de EE. UU.
- **Temática:** TFB-07 Fundamentales de empresas gratuitos (principal) · secundarias: TFB-06
- **Calidad Q:** 57 (C) — Primariedad 9/20 · Historial 10/20 · Transparencia 7/15 · Autoridad 9/15 · Independencia 5/10 · Actualidad 10/10 · Acceso 7/10
- **Tipología:** secundaria (agregador comercial)
- **Acceso:** Freemium: plan gratuito limitado; cobertura mundial de pago (futuro)
- **Ámbitos:** Estados financieros, estimaciones y múltiplos de compañías cotizadas
- **Motivo de inclusión y uso:** Alternativa de bajo coste para fundamentales de compañías no estadounidenses frente a terminales profesionales.
- **Restricciones de uso:** Condiciones de TIKR; sin redistribución.
- **Sesgos y cautelas:** Fuente de los datos no declarada en la página leída; la propia página es promocional.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B12 Seleccionador de Activos y AG-B09 Finanzas y Valoración: comparables internacionales de candidatos (con verificación en la fuente primaria).
- **Origen:** Alta F9_comp (2026-11-03).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-03 (búsqueda web: «free stock screener fundamentals comparison Finviz GuruFocus Zacks Morningstar»; WebFetch: sí)

#### MBF-0215 · Q 56 (C) — finbox — modelos de valoración y datos fundamentales (freemium)

- **Canal oficial (URL raíz):** finbox.com (según el índice) · Página índice: https://alternativeto.net/software/stockanalysis-com
- **Emisor:** finbox (empresa privada)
- **Documentación y notas:** Plataforma freemium de datos fundamentales, plantillas de valoración y cribado; listada como alternativa a Stock Analysis.
- **Temática:** TFB-07 Fundamentales de empresas gratuitos (principal)
- **Calidad Q:** 56 (C) — Primariedad 9/20 · Historial 10/20 · Transparencia 7/15 · Autoridad 8/15 · Independencia 8/10 · Actualidad 9/10 · Acceso 5/10
- **Tipología:** secundaria (agregador con modelos)
- **Acceso:** Freemium; registro
- **Ámbitos:** Estados financieros, múltiplos y modelos de valoración
- **Motivo de inclusión y uso:** Contraste de supuestos de valoración (DCF, múltiplos) de terceros.
- **Uso en el bloque:** AG-B09 y AG-B14 Contrarias: contraste de valoraciones; no sustituye al Motor AG-B16.
- **Restricciones de uso:** Funciones principales de pago; credenciales en HT-01.
- **Sesgos y cautelas:** Modelos automáticos con supuestos genéricos.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «free stock fundamentals data sites Macrotrends Stockanalysis Financial Modeling Prep Simply Wall St comparison»; WebFetch: sí, sobre la página índice alternativeto.net)
- **Origen:** Alta F9 Bloque B (2026-11-02).

#### MBF-0211 · Q 54 (C) — Seeking Alpha — análisis de inversores y datos de empresas

- **Canal oficial (URL raíz):** seekingalpha.com (según el índice) · Página índice: https://alternativeto.net/software/stockanalysis-com
- **Emisor:** Seeking Alpha Ltd.
- **Documentación y notas:** Plataforma de artículos de colaboradores, transcripciones de conferencias de resultados, datos fundamentales y calificaciones cuantitativas; contenido gratuito limitado y suscripción Premium.
- **Temática:** TFB-07 Fundamentales de empresas gratuitos (principal) · secundarias: TFB-15
- **Calidad Q:** 54 (C) — Primariedad 8/20 · Historial 10/20 · Transparencia 6/15 · Autoridad 9/15 · Independencia 6/10 · Actualidad 10/10 · Acceso 5/10
- **Tipología:** secundaria y de opinión
- **Acceso:** Muro parcial; registro
- **Ámbitos:** Tesis de inversión de colaboradores, transcripciones de resultados
- **Motivo de inclusión y uso:** Transcripciones de conferencias de resultados y tesis alcistas y bajistas sobre candidatos.
- **Uso en el bloque:** AG-B14 Contrarias (tesis opuestas) y AG-B10 Flujos y Sentimiento; AG-B09 para transcripciones (preferir la versión del emisor). Opinión: nunca prueba un hecho.
- **Restricciones de uso:** Muro de pago; credenciales en HT-01.
- **Sesgos y cautelas:** Autores con posiciones declaradas pero heterogéneos; incentivos por visitas.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «free stock fundamentals data sites Macrotrends Stockanalysis Financial Modeling Prep Simply Wall St comparison»; WebFetch: sí, sobre la página índice alternativeto.net)
- **Origen:** Alta F9 Bloque B (2026-11-02).

#### MBF-0214 · Q 51 (C) — TipRanks — consenso de analistas y precios objetivo (freemium)

- **Canal oficial (URL raíz):** tipranks.com (según el índice) · Página índice: https://alternativeto.net/software/stockanalysis-com
- **Emisor:** TipRanks Ltd.
- **Documentación y notas:** Agregador freemium de recomendaciones y precios objetivo de analistas, con puntuaciones del historial de acierto de cada analista; listado como alternativa a Stock Analysis.
- **Temática:** TFB-07 Fundamentales de empresas gratuitos (principal) · secundarias: TFB-15
- **Calidad Q:** 51 (C) — Primariedad 6/20 · Historial 10/20 · Transparencia 6/15 · Autoridad 8/15 · Independencia 6/10 · Actualidad 10/10 · Acceso 5/10
- **Tipología:** secundaria (agregador)
- **Acceso:** Freemium; registro
- **Ámbitos:** Consenso de recomendaciones y precios objetivo por empresa
- **Motivo de inclusión y uso:** Lectura rápida del consenso de analistas sobre un candidato.
- **Uso en el bloque:** AG-B10 Flujos y Sentimiento y AG-B14 Contrarias (medir cuán consensuada está una tesis); nunca como prueba de valor.
- **Restricciones de uso:** Datos detallados de pago; credenciales en HT-01.
- **Sesgos y cautelas:** Cobertura y método de puntuación propios; recomendaciones de analistas sesgadas a «comprar».
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «free stock fundamentals data sites Macrotrends Stockanalysis Financial Modeling Prep Simply Wall St comparison»; WebFetch: sí, sobre la página índice alternativeto.net)
- **Origen:** Alta F9 Bloque B (2026-11-02).

## TFB-08 Fondos, ETF e índices: datos y documentación

#### MBF-0218 · Q 86 (A) — UE — Documento de datos fundamentales (KID) de PRIIPs: Reglamento (UE) 1286/2014 y Reglamento Delegado (UE) 2017/653

- **Canal oficial (URL raíz):** https://eur-lex.europa.eu/eli/reg_del/2017/653/oj · Ejemplo de repositorio de KID de ETF por distribuidor: https://www.brd.ro/en/en/financial-markets/capital-markets/regulatory-information/etfs
- **Emisor:** Unión Europea (Parlamento Europeo y Consejo; Comisión Europea para las normas técnicas)
- **Documentación y notas:** El Reglamento 1286/2014 (aplicable desde el 01/01/2018) obliga a entregar al inversor minorista un KID normalizado de cada producto empaquetado (incluidos ETF UCITS desde 2023); el Reglamento Delegado 2017/653 fija contenido, indicador resumido de riesgo, escenarios de rentabilidad y presentación de costes. Los KID los publica cada gestora (BlackRock/iShares, DWS/Xtrackers, Amundi, Vanguard, WisdomTree, Invesco…) y los replican los distribuidores.
- **Temática:** TFB-08 Fondos, ETF e índices: datos y documentación (principal) · secundarias: TFB-03
- **Calidad Q:** 86 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 7/10 · Acceso 10/10
- **Tipología:** primaria (norma y documento regulatorio de producto)
- **Acceso:** Abierto
- **Ámbitos:** Riesgo (SRI 1–7), costes de entrada, salida y corrientes, escenarios y periodo recomendado de cada fondo o ETF de la UE
- **Motivo de inclusión y uso:** Documento comparable y obligatorio para todos los vehículos minoristas de la UE; base para comparar costes y riesgo de vehículos candidatos.
- **Uso en el bloque:** AG-B12 Seleccionador de Activos (ficha mínima obligatoria de cada ETF o fondo candidato: costes, SRI, objetivo) y AG-B07 Regulación (régimen de comercialización minorista).
- **Restricciones de uso:** Uso libre de la norma; los KID son documentos de cada emisor (citar emisor, ISIN y fecha).
- **Sesgos y cautelas:** Escenarios de rentabilidad estandarizados poco informativos; costes de transacción estimados; la versión vigente del KID puede cambiar sin aviso.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Revisión del marco PRIIPs dentro de la Estrategia de Inversión Minorista de la UE (seguimiento por AG-B07).
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Regulation (EU) No 1286/2014 PRIIPs key information documents EUR-Lex Delegated Regulation 2017/653»; «iShares ETF holdings download Xtrackers Amundi ETF KID PRIIPs key information document ETF.com»; WebFetch: sí, sobre la página de KID de ETF de BRD)
- **Origen:** Alta F9 Bloque B (2026-11-02).

#### RF-0521 · Q 86 (A) — SEC — Form N-PORT Data Sets (carteras mensuales de fondos registrados)

- **Canal oficial (URL raíz):** https://www.sec.gov/data-research/sec-markets-data/form-n-port-data-sets
- **Emisor:** U.S. Securities and Exchange Commission (División de Análisis Económico y de Riesgos, DERA)
- **Documentación y notas:** Conjuntos de datos estructurados extraídos de los formularios N-PORT públicos (carteras de fondos de inversión y ETF registrados a fin de mes); actualización trimestral; cobertura de octubre de 2019 a septiembre de 2026 (fichero 2026 Q3, ZIP de 441 MB; página actualizada el 30/09/2026); documento «readme» con tablas y definiciones. Complementa los datos de 13F (RF-0044) con la totalidad de la cartera, derivados y liquidez de los fondos.
- **Temática:** TFB-08 Fondos, ETF e índices: datos y documentación (principal) · secundarias: TFB-15
- **Calidad Q:** 86 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 9/10
- **Tipología:** primaria (declaraciones regulatorias)
- **Acceso:** Abierto (descarga masiva)
- **Ámbitos:** Posiciones agregadas de fondos de EE. UU. por activo, emisor, derivado y país
- **Motivo de inclusión y uso:** Medir exposición agregada de la industria de fondos a segmentos (p. ej., crédito privado en fondos abiertos, derivados en ETF apalancados) y concentración. AG-22, AG-23.
- **Uso en el bloque:** AG-B12 y AG-B10: carteras mensuales completas de fondos registrados en EE. UU. (N-PORT) para ver qué valores concentran los ETF temáticos o sectoriales; MC-B de concentración.
- **Restricciones de uso:** Dominio público; citar trimestre del fichero.
- **Sesgos y cautelas:** Solo se publican los datos públicos (con desfase); ficheros voluminosos que requieren tratamiento.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Enmiendas del formulario N-PORT (reglas de 2024 sobre frecuencia de publicación) pueden alterar la serie.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «SEC Form N-PORT data sets Form N-CEN data sets structured data»; WebFetch: sí)
- **Origen:** Alta F9_S4 (2026-11-02).
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0502 · Q 83 (A) — STOXX — Rulebooks (guías de metodología de STOXX, DAX e iSTOXX) y anuncios de revisiones

- **Canal oficial (URL raíz):** https://stoxx.com/rulebooks
- **Emisor:** STOXX Ltd. (ISS STOXX, grupo Deutsche Börse)
- **Documentación y notas:** Guías vinculantes de desarrollo, cálculo, revisión y ajuste: guías armonizadas (clasificación sectorial, cálculo, iNAV, Quality Charter), STOXX (Investable Market, World Equity, estrategia, activos digitales, renta fija ICE), DAX (DAX Equity y Strategy, guía de cálculo, eb.rexx, EUROGOV, REX) y ECPI. Menús de anuncios (actualizaciones de índices, metodología: stoxx.com/methodology) y de datos (información de revisiones periódicas, listas de selección, informes de revisión, operaciones corporativas). Administra EURO STOXX 50, DAX y los índices de volatilidad VSTOXX.
- **Temática:** TFB-08 Fondos, ETF e índices: datos y documentación (principal) · secundarias: —
- **Calidad Q:** 83 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 14/15 · Independencia 7/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (guías y anuncios); datos de composición detallados bajo licencia
- **Ámbitos:** Índices europeos y globales de renta variable, DAX, volatilidad (VSTOXX), renta fija y temáticos
- **Motivo de inclusión y uso:** Reglas y calendario de revisiones de los índices de referencia europeos; listas de selección para anticipar entradas y salidas. AG-21.
- **Uso en el bloque:** AG-B12: rulebooks de STOXX/DAX (índices sectoriales y temáticos europeos) para listas de candidatos y reglas de inclusión; AG-B10 para revisiones trimestrales.
- **Restricciones de uso:** Uso con atribución; datos de índices bajo licencia.
- **Sesgos y cautelas:** Proveedor comercial que licencia sus índices a emisores de ETF y derivados.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Fusión de STOXX con ISS (ISS STOXX, 2023) y absorción de la marca Qontigo; la familia DAX pasó a la gestión de STOXX.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «STOXX index methodology guide rulebook stoxx.com»; WebFetch: sí)
- **Origen:** Alta F9_S4 (2026-11-02).
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0504 · Q 82 (A) — BME (Sociedad de Bolsas) — índices IBEX: normas técnicas y avisos del Comité Asesor Técnico

- **Canal oficial (URL raíz):** https://www.bolsasymercados.es/bme-exchange/docs/docsSubidos/Indices/Regulacion/Normas_Indices_Ibex_esp.pdf (avisos del Comité, p. ej.: https://www.bolsasymercados.es/bme-exchange/docs/Indices/Avisos/esp/comiteasesor/Aviso_Comite_IBEX_01-26.pdf)
- **Emisor:** Sociedad de Bolsas, S.A. (BME, grupo SIX)
- **Documentación y notas:** «Normas técnicas para la composición y cálculo de los Índices IBEX y de Estrategia sobre Acciones» (versión de enero de 2025): Comité Asesor Técnico de 5 a 9 miembros, reuniones ordinarias semestrales y de seguimiento en los otros trimestres, efectividad el día hábil siguiente al tercer viernes; IBEX 35 (35 valores más líquidos del SIBE, umbral de capitalización del 0,30 %, ajuste por free float, tope del 20 %), IBEX Medium Cap, Small Cap, Top Dividendo, índices sectoriales, apalancados e inversos, de estrategia de opciones (VIBEX, SKEW) y ESG. Los avisos del Comité publican altas, bajas y coeficientes.
- **Temática:** TFB-08 Fondos, ETF e índices: datos y documentación (principal) · secundarias: TFB-03
- **Calidad Q:** 82 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 14/15 · Independencia 7/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (PDF)
- **Ámbitos:** Renta variable española; revisiones del IBEX 35 y familia IBEX
- **Motivo de inclusión y uso:** Fuente primaria de las reglas y decisiones de composición del índice de referencia español. AG-21; AG-23 (subyacente de futuros y opciones de MEFF).
- **Uso en el bloque:** AG-B12: normas técnicas y avisos del Comité Asesor Técnico del IBEX para el universo español; AG-B10 para cambios de composición.
- **Restricciones de uso:** Uso con atribución; marcas IBEX registradas.
- **Sesgos y cautelas:** El administrador pertenece al operador del mercado (SIX); las decisiones del Comité tienen margen discrecional.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** BME integrada en SIX Group (2020).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Comité Asesor Técnico IBEX 35 normas técnicas bolsasymercados.es índices revisión»; WebFetch: sí, PDF de normas técnicas)
- **Origen:** Alta F9_S4 (2026-11-02).
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0510 · Q 82 (A) — Nasdaq Global Indexes — metodologías (Nasdaq-100 y otros) y reconstitución anual

- **Canal oficial (URL raíz):** https://indexes.nasdaq.com/ (metodología del Nasdaq-100: https://indexes.NASDAQomx.com/docs/Methodology_NDX.pdf · balance de la reconstitución de enero de 2026: https://indexes.nasdaqomx.com/docs/202601%20NDX%20Reconstitution%20and%20Performance%20Highlights.pdf · consulta de noviembre de 2023: https://indexes.nasdaq.com/docs/NDX%20Index%20Consultation%20November%202023%20-%20Final.pdf)
- **Emisor:** Nasdaq, Inc. (Nasdaq Global Indexes)
- **Documentación y notas:** Repositorio de metodologías por índice (NDX, NDXT, NDXX, NDXESG, NDXMEGA, NGX, NDXLV, etc.), versiones con cambios marcados (redline), consultas de índice y notas de reconstitución anual del Nasdaq-100 (diciembre) con su balance de rendimiento; anuncios de cambios anuales en nasdaq.com.
- **Temática:** TFB-08 Fondos, ETF e índices: datos y documentación (principal) · secundarias: —
- **Calidad Q:** 82 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 14/15 · Independencia 7/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (PDF de metodología y anuncios)
- **Ámbitos:** Renta variable de EE. UU. de gran capitalización no financiera y tecnológica; índices temáticos
- **Motivo de inclusión y uso:** Reglas de concentración, reequilibrios especiales y reconstitución del Nasdaq-100 (subyacente de grandes ETF y derivados). AG-21, AG-23.
- **Uso en el bloque:** AG-B12: metodologías Nasdaq (Nasdaq-100 y temáticos tecnológicos) para delimitar universos; AG-B10 para la reconstitución anual.
- **Restricciones de uso:** Uso con atribución; marcas registradas.
- **Sesgos y cautelas:** El administrador es operador de bolsa (incentivo a mantener listados). No se pudo cargar el PDF en esta sesión (error del sitio); confirmado en resultados de búsqueda.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Consulta de 2023 sobre reglas de ponderación del Nasdaq-100.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Nasdaq Global Indexes methodology Nasdaq-100 annual reconstitution indexes.nasdaqomx.com»; WebFetch: intento fallido, error del sitio)
- **Origen:** Alta F9_S4 (2026-11-02).
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0522 · Q 82 (A) — SEC — Form N-CEN Data Sets (informe censal anual de fondos registrados)

- **Canal oficial (URL raíz):** https://www.sec.gov/dera/data/form-ncen-data-sets (ruta mostrada en los resultados de búsqueda; catálogo federal: https://catalog.data.gov/organization/sec-gov?tags=__)
- **Emisor:** U.S. Securities and Exchange Commission (DERA)
- **Documentación y notas:** Datos estructurados del formulario N-CEN, informe anual de fondos registrados (proveedores de servicios, información específica de ETF —creadores autorizados, unidades de creación—, préstamo de valores, uso de líneas de crédito). Adoptado en la reforma de información de fondos de 2016 junto con N-PORT.
- **Temática:** TFB-08 Fondos, ETF e índices: datos y documentación (principal) · secundarias: —
- **Calidad Q:** 82 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 6/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Estructura de la industria de fondos y ETF de EE. UU.; proveedores y mecanismos de creación/reembolso
- **Motivo de inclusión y uso:** Análisis de la infraestructura del mercado de ETF (concentración de creadores autorizados) y de prácticas de préstamo de valores. AG-22.
- **Uso en el bloque:** AG-B12: datos censales de fondos de EE. UU. (N-CEN: tipo de fondo, índice, proveedores de servicio, préstamo de valores) para caracterizar vehículos candidatos.
- **Restricciones de uso:** Dominio público.
- **Sesgos y cautelas:** Frecuencia anual; la página no se pudo cargar en esta sesión (fuera de la lista permitida), confirmada por resultados de búsqueda.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «SEC Form N-PORT data sets Form N-CEN data sets structured data»; WebFetch: no, URL no admitida)
- **Origen:** Alta F9_S4 (2026-11-02).
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0523 · Q 82 (A) — ESMA — Market report on the costs and performance of EU retail investment products

- **Canal oficial (URL raíz):** https://www.esma.europa.eu/press-news/esma-news/new-investment-funds-drive-reduction-costs-investors (informe de 2025, publicado el 03/03/2026: https://www.esma.europa.eu/sites/default/files/2026-03/ESMA50-1949966494-4065_Market_Report_-_Costs_and_Performance_of_EU_Retail_Investment_Products.pdf)
- **Emisor:** European Securities and Markets Authority (ESMA)
- **Documentación y notas:** Octava edición del informe anual de costes y rentabilidad de UCITS, FIA minoristas y productos estructurados: en 2024 los gastos corrientes bajaron un 8 % en fondos de renta variable y casi un 15 % en renta fija minoristas (impulso de fondos nuevos), rentabilidades reales netas positivas en todas las categorías, UCITS ESG más baratos pero con peor rentabilidad que los no ESG, participación minorista en FIA del 9 %, auge de estructurados ligados a tipos (27 % del mercado). Pieza distinta de RF-0027 (TRV) y de RF-0403 (FIA).
- **Temática:** TFB-08 Fondos, ETF e índices: datos y documentación (principal) · secundarias: TFB-03
- **Calidad Q:** 82 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 6/10 · Acceso 10/10
- **Tipología:** primaria (estadística supervisora)
- **Acceso:** Abierto
- **Ámbitos:** Costes, rentabilidad bruta y neta por categoría de fondo UCITS (incluidos ETF), FIA y estructurados en la UE
- **Motivo de inclusión y uso:** Referencia oficial del coste de implementación por categoría y del diferencial gestión activa/pasiva en Europa. AG-22.
- **Uso en el bloque:** AG-B12: costes y rentabilidades de fondos minoristas de la UE por clase (ESMA) para valorar el lastre de costes de un vehículo candidato; AG-B09.
- **Restricciones de uso:** Uso libre con atribución.
- **Sesgos y cautelas:** Desfase de más de un año; muestras basadas en bases de datos comerciales.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ESMA market report costs and performance of EU retail investment products 2026»; WebFetch: sí)
- **Origen:** Alta F9_S4 (2026-11-02).
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0056 · Q 81 (A) — S&P Dow Jones Indices (metodologías, SPIVA)

- **Canal oficial (URL raíz):** https://www.spglobal.com/spdji/en/research-insights/spiva/
- **Emisor:** S&P Dow Jones Indices (S&P Global)
- **Documentación y notas:** Sección SPIVA con resultados por región, biblioteca (spglobal.com/spdji/en/research-insights/spiva/spiva-library/), vídeos e investigación; blog Indexology del mismo emisor (indexologyblog.com, no cuenta como fuente independiente). Metodologías de índices en las fichas de cada índice de spglobal.com/spdji/en/.
- **Temática:** TFB-08 Fondos, ETF e índices: datos y documentación (principal) · secundarias: TFB-06
- **Calidad Q:** 81 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 14/15 · Independencia 8/10 · Actualidad 8/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto (parcial)
- **Ámbitos:** Metodologías de índices; informes SPIVA (gestión activa frente a índices, persistencia de gestores) por región
- **Motivo de inclusión y uso:** Reglas de índices y evidencia periódica de rendimiento relativo de la gestión activa.
- **Uso en el bloque:** AG-B12: metodologías S&P DJI (incl. GICS y Select Sector) para universos; AG-B09/AG-B14 con SPIVA como contraste gestión activa frente a índice.
- **Restricciones de uso:** Condiciones de S&P DJI; citar informe SPIVA (región, periodo) y fecha.
- **Sesgos y cautelas:** Proveedor comercial de índices (interés en la gestión indexada).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «S&P Dow Jones Indices SPIVA scorecard» y «SPIVA S&P Dow Jones Indices spglobal.com/spdji/en/research-insights/spiva»; WebFetch: sí)
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0505 · Q 81 (A) — Bloomberg Index Services — metodología de índices de renta fija (Global Aggregate, US Aggregate y otros)

- **Canal oficial (URL raíz):** https://data.bloomberglp.com/professional/sites/10/Bloomberg-Index-Publications-Fixed-Income-Index-Methodology.pdf
- **Emisor:** Bloomberg Index Services Limited (BISL)
- **Documentación y notas:** «Bloomberg Fixed Income Index Methodology» (08/01/2026): reglas de elegibilidad (divisa, sector, calidad, importe vivo, vencimiento, país, mercado de emisión), universos Projected y Returns, reequilibrio mensual, precios y rentabilidades; familias Global Aggregate, US Aggregate, Pan-European, Asian-Pacific, EM Local Currency Government (inclusión escalonada de bonos FAR de la India desde enero de 2025), WGILB, High Yield, municipales y Global Leveraged Loan (julio de 2025); revisiones anuales de elegibilidad de mercados; gobierno según el Benchmark Procedures Handbook.
- **Temática:** TFB-08 Fondos, ETF e índices: datos y documentación (principal) · secundarias: TFB-06
- **Calidad Q:** 81 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 7/10 · Actualidad 9/10 · Acceso 7/10
- **Tipología:** primaria
- **Acceso:** Metodología abierta; niveles y composición de índices bajo licencia (terminal)
- **Ámbitos:** Índices de referencia de renta fija global; inclusión de mercados locales emergentes
- **Motivo de inclusión y uso:** Reglas de los índices de bonos más replicados; anticipar flujos por inclusión de países o cambios de elegibilidad. AG-21, AG-25.
- **Uso en el bloque:** AG-B12: universos de bonos por sector y calificación para el segmento de renta fija del análisis; AG-B09 para diferenciales sectoriales.
- **Restricciones de uso:** Uso con atribución; datos bajo licencia.
- **Sesgos y cautelas:** Proveedor comercial; documentos índice-específicos prevalecen en detalles.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Antiguos índices Lehman y Bloomberg Barclays (marca Barclays retirada en 2021).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Bloomberg Indices methodology Bloomberg Global Aggregate index rules index announcements»; WebFetch: sí, PDF de metodología)
- **Origen:** Alta F9_S4 (2026-11-02).
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0054 · Q 80 (A) — MSCI — metodologías de índices

- **Canal oficial (URL raíz):** https://www.msci.com/indexes/index-resources/index-methodology
- **Emisor:** MSCI Inc.
- **Documentación y notas:** Buscador de metodologías vigentes e históricas por nombre o código de índice; documentos clave enlazados (MSCI Index Calculation Methodology, MSCI Index Policies —p. ej., versión 27/01/2026 en msci.com/indexes/documents/methodology/—, Fixed Income Index Policies). Las URL antiguas (msci.com/index-methodology, msci.com/eqb/methodology/) siguen apareciendo en buscadores.
- **Temática:** TFB-08 Fondos, ETF e índices: datos y documentación (principal) · secundarias: TFB-06
- **Calidad Q:** 80 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 14/15 · Independencia 7/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (metodologías); datos de índices de pago
- **Ámbitos:** Reglas de índices (GIMI), reequilibrios, clasificación de mercados
- **Motivo de inclusión y uso:** Reglas oficiales que generan flujos indexados (reclasificaciones, reequilibrios trimestrales).
- **Uso en el bloque:** AG-B12: reglas de elegibilidad, ponderación y revisión de índices MSCI (universos sectoriales GICS y temáticos) para cribar candidatos; AG-B10 para anticipar entradas y salidas por rebalanceo.
- **Restricciones de uso:** Condiciones de MSCI; citar documento y fecha de versión.
- **Sesgos y cautelas:** Proveedor comercial; la página no aclara si algún documento exige acceso de cliente.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Reorganización de URL del sitio (rutas /eqb/ antiguas): vigilar redirecciones.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «MSCI index methodology page»; WebFetch: sí)
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0055 · Q 80 (A) — FTSE Russell — metodologías de índices

- **Canal oficial (URL raíz):** https://lseg.com/en/ftse-russell
- **Emisor:** FTSE Russell (London Stock Exchange Group, LSEG)
- **Documentación y notas:** Las reglas (ground rules) y metodologías se publican como PDF bajo lseg.com/content/dam/ftse-russell/en_us/documents/ (p. ej., «Global Equity Index Methodology», «Russell US Equity Indexes – history of ground rule updates», «Russell Indexes – impacts of reconstitution 2025»). La portada remite al «Benchmark and Index Finder».
- **Temática:** TFB-08 Fondos, ETF e índices: datos y documentación (principal) · secundarias: TFB-06
- **Calidad Q:** 80 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 14/15 · Independencia 7/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (reglas y metodologías); datos de pago
- **Ámbitos:** Reglas de índices FTSE y Russell, reconstitución de los índices Russell de EE. UU., clasificación de países
- **Motivo de inclusión y uso:** Calendario y efectos de reconstituciones como catalizador de flujos indexados.
- **Uso en el bloque:** AG-B12: metodologías FTSE Russell (incl. clasificación ICB) para delimitar universos sectoriales; AG-B10 para la reconstitución anual de Russell.
- **Restricciones de uso:** Condiciones de LSEG; citar documento y versión.
- **Sesgos y cautelas:** Proveedor comercial; la portada no enlaza directamente las reglas (se llega por el buscador de índices). Comprobar el calendario de reconstitución en el documento vigente antes de usarlo.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Integrado en LSEG; el dominio russell.com redirige parcialmente al de LSEG.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «FTSE Russell index ground rules methodology LSEG Russell reconstitution» y «FTSE Russell LSEG index provider home page»; WebFetch: sí)

<!-- Tanda 2 · 2026-11-02 · cupo de 25 búsquedas · verificación de semillas TF-07…TF-10 y altas RF-0300…RF-0316. Convención: «VERIFICADO_BUSQUEDA (directorio)» = URL raíz tomada de un directorio oficial o de referencia leído con WebFetch (indicado en «Última verificación»); el sitio en sí no se pudo leer porque la herramienta solo admite URL devueltas por búsqueda. -->
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0506 · Q 80 (A) — ICE Data Indices — metodologías de índices de bonos (ICE y ICE BofA)

- **Canal oficial (URL raíz):** https://www.ice.com/publicdocs/data/Bond_Index_Methodologies.pdf
- **Emisor:** ICE Data Indices, LLC (Intercontinental Exchange)
- **Documentación y notas:** «Bond Index Methodologies» (30/04/2025): reglas de los índices de bonos ICE e ICE BofA (soberanos, cuasi-gubernamentales, corporativos por vencimiento y calificación, CoCo, convertibles, MBS, ABS, CMBS, sintéticos y ESG/clima); reequilibrio mensual el último día natural con fecha de bloqueo tres días hábiles antes; revisión anual de reglas (propuestas en abril, decisión en julio, aplicación a fin de septiembre). Las series de diferenciales ICE BofA se redistribuyen en FRED (no cuentan como fuente independiente).
- **Temática:** TFB-08 Fondos, ETF e índices: datos y documentación (principal) · secundarias: TFB-06
- **Calidad Q:** 80 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 14/15 · Independencia 7/10 · Actualidad 8/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Metodología abierta; datos completos bajo licencia
- **Ámbitos:** Renta fija investment grade, high yield, emergentes, titulizaciones
- **Motivo de inclusión y uso:** Reglas de los índices de crédito más usados en diferenciales (OAS) y ETF de bonos. AG-21, AG-25.
- **Uso en el bloque:** AG-B12: índices ICE BofA de crédito por sector (alto rendimiento, grado de inversión) como universo y referencia de renta fija.
- **Restricciones de uso:** Uso con atribución; datos bajo licencia.
- **Sesgos y cautelas:** Proveedor que también opera bolsas y cámaras (ICE): conflicto potencial.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Índices de Merrill Lynch/BofA adquiridos por ICE (2017).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ICE Data Indices ICE BofA bond index methodology index rules»; WebFetch: sí, PDF)
- **Origen:** Alta F9_S4 (2026-11-02).
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0525 · Q 78 (B) — INVERCO — estadísticas mensuales de fondos de inversión e IIC en España

- **Canal oficial (URL raíz):** http://www.inverco.es/ (informe mensual de julio de 2026: https://www.inverco.es/wp-content/uploads/2026/08/2607_Julio-2026.pdf · informe anual 2025: https://www.inverco.es/informe/informe-anual-2025)
- **Emisor:** Asociación de Instituciones de Inversión Colectiva y Fondos de Pensiones (INVERCO)
- **Documentación y notas:** Informe mensual de fondos (patrimonio, suscripciones netas, partícipes y rentabilidad por vocación inversora: monetarios, renta fija, mixtos, renta variable nacional e internacional por zonas, globales, garantizados, índice, rentabilidad objetivo, retorno absoluto, inversión libre) y notas de prensa. Julio de 2026: 478.069 M€ de patrimonio (+6 % en el año), 10.959 M€ de suscripciones netas acumuladas, 19,27 millones de cuentas de partícipes.
- **Temática:** TFB-08 Fondos, ETF e índices: datos y documentación (principal) · secundarias: TFB-15
- **Calidad Q:** 78 (B) — Primariedad 19/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 13/15 · Independencia 5/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria (datos agregados de las gestoras asociadas)
- **Acceso:** Abierto
- **Ámbitos:** Fondos de inversión españoles, SICAV, fondos de pensiones
- **Motivo de inclusión y uso:** Flujos y preferencias del inversor español por categoría (rotación de monetarios y renta fija a renta variable). AG-22.
- **Uso en el bloque:** AG-B10: patrimonio, suscripciones y reembolsos de fondos en España por categoría; AG-B12 para contexto del mercado español de vehículos.
- **Restricciones de uso:** Uso con atribución.
- **Sesgos y cautelas:** Patronal del sector; cifras provisionales que la CNMV (RF-0026) publica después con datos oficiales; partícipes contados por cuentas, no personas.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «INVERCO estadísticas fondos de inversión patrimonio suscripciones netas 2026»; WebFetch: sí, informe de julio de 2026)
- **Origen:** Alta F9_S4 (2026-11-02).
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0514 · Q 77 (B) — Morningstar Indexes — reglamentos de índices (incluye la familia CRSP migrada)

- **Canal oficial (URL raíz):** https://indexes.morningstar.com/ (reglamento leído: https://indexes.morningstar.com/api/docs/68b407a0f8270052cc84d908 · página de metodología de CRSP que redirige a Morningstar: https://www.crsp.org/indexes/crsp-market-indexes-methodology/)
- **Emisor:** Morningstar Indexes (Morningstar, Inc.)
- **Documentación y notas:** Reglamentos («Construction Rules») por familia, p. ej., Morningstar Target Allocation Indexes (agosto de 2025: reconstitución anual en junio, reequilibrio mensual), con gobierno en tres comités (metodología, operaciones y supervisión conforme al BMR de la UE y del Reino Unido). El 02/11/2026 la página de metodología de los índices de mercado de CRSP (crsp.org) redirige (302) a un reglamento de Morningstar US Total Market, lo que indica la migración de la familia CRSP (referencia de grandes fondos indexados de EE. UU.) a Morningstar Indexes. Canal distinto de RF-0048 (investigación y calificación de fondos) y de RF-0520 (categorías).
- **Temática:** TFB-08 Fondos, ETF e índices: datos y documentación (principal) · secundarias: —
- **Calidad Q:** 77 (B) — Primariedad 18/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 13/15 · Independencia 6/10 · Actualidad 8/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (reglamentos PDF); datos bajo licencia
- **Ámbitos:** Índices de renta variable de mercado amplio, factores, multiactivo, sostenibilidad
- **Motivo de inclusión y uso:** Reglas de índices de referencia de grandes fondos indexados y de asignación de activos. AG-21, AG-22.
- **Uso en el bloque:** AG-B12: reglamentos de Morningstar Indexes (familia CRSP, índices temáticos y de moat) para universos y referencia.
- **Restricciones de uso:** Uso con atribución.
- **Sesgos y cautelas:** Morningstar es a la vez proveedor de índices, calificador de fondos y proveedor de datos (conflictos potenciales). La continuidad de los índices CRSP bajo Morningstar se deduce de la redirección: confirmar la transición en cada uso.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Integración de los índices CRSP (redirección observada en 2026).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Morningstar Indexes methodology rulebook indexes.morningstar.com» y «CRSP US Total Market Index methodology quarterly reconstitution crsp.org indexes»; WebFetch: sí, reglamento; redirección de crsp.org observada)
- **Origen:** Alta F9_S4 (2026-11-02).
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0509 · Q 74 (B) — Solactive — guías de índices y anuncios de cambios de metodología

- **Canal oficial (URL raíz):** https://www.solactive.com/ (anuncio leído: https://legacy2.solactive.com/methodology-change-several-solactive-indices-effective-date-24-11-2025/ · guías en solactive.com/downloads/, p. ej., https://solactive.com/downloads/Solactive_EU_1Day_Rolling_Future_Index_Guideline.pdf)
- **Emisor:** Solactive AG (Fráncfort)
- **Documentación y notas:** Administrador de índices a medida para emisores de ETF y productos estructurados; guías (Guideline) por índice y sección de anuncios con cambios de metodología, nombre, ISIN y RIC (p. ej., aviso de 10/11/2025 sobre la revisión trimestral ESG de siete índices, efectiva el 24/11/2025).
- **Temática:** TFB-08 Fondos, ETF e índices: datos y documentación (principal) · secundarias: —
- **Calidad Q:** 74 (B) — Primariedad 18/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 11/15 · Independencia 6/10 · Actualidad 9/10 · Acceso 7/10
- **Tipología:** primaria
- **Acceso:** Abierto (guías y anuncios)
- **Ámbitos:** Índices de ETF temáticos, de renta fija y de estrategia
- **Motivo de inclusión y uso:** Reglas de muchos índices subyacentes de ETF europeos de bajo coste y temáticos. AG-21, AG-22.
- **Uso en el bloque:** AG-B12: guías de índices Solactive (muy usados por ETF temáticos) para conocer la cesta real de una temática; AG-B06 Tecnología para revisar qué entra en «IA», «robótica», etc.
- **Restricciones de uso:** Uso con atribución.
- **Sesgos y cautelas:** Índices a medida a petición del emisor del producto (riesgo de diseño orientado a marketing).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos (migración de web con dominio legacy2).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Solactive index guidelines announcements solactive.com»; WebFetch: sí, anuncio)
- **Origen:** Alta F9_S4 (2026-11-02).
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0520 · Q 74 (B) — Morningstar — Category Classifications (metodología de categorías de fondos)

- **Canal oficial (URL raíz):** https://www.morningstar.com/content/cs-assets/v3/assets/blt9415ea4cc4157833/bltc0c557175d70b1fd/68dea997aed382ecc562dbce/Morningstar_Category_Classification_for_Funds_-_October_2024.pdf (clasificación global: https://advisor.morningstar.com/Enterprise/VTC/MorningstarGlobalCategory_April2021.pdf · repositorio de metodologías: https://www.morningstar.com/business/insights/research/methodology-documents?page=7)
- **Emisor:** Morningstar, Inc. (Manager Research)
- **Documentación y notas:** Metodología de octubre de 2024 para fondos de EE. UU.: 127 categorías en nueve grupos; asignación por estadísticas medias de cartera de los tres años previos (no por el folleto); revisiones semestrales por grupo (renta variable abril y septiembre; alternativos, mixtos y materias primas abril y octubre; renta fija julio y noviembre); filtro cuantitativo más validación de analistas y apelaciones. Existen versiones regionales (Europa/global, Japón, Australia) y la clasificación global (Global Category). Canal distinto de RF-0048 (investigación y Medalist Rating) y de RF-0514 (índices).
- **Temática:** TFB-08 Fondos, ETF e índices: datos y documentación (principal) · secundarias: —
- **Calidad Q:** 74 (B) — Primariedad 17/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 13/15 · Independencia 6/10 · Actualidad 7/10 · Acceso 7/10
- **Tipología:** primaria (taxonomía del proveedor)
- **Acceso:** Abierto (PDF); datos por fondo bajo licencia
- **Ámbitos:** Taxonomía de fondos y ETF por estilo, región, sector y clase de activo
- **Motivo de inclusión y uso:** Taxonomía de referencia para agregar flujos y rentabilidades por segmento de forma comparable. AG-22.
- **Uso en el bloque:** AG-B12: categorías Morningstar para comparar fondos y ETF del mismo segmento y evitar comparaciones mal planteadas.
- **Restricciones de uso:** Uso con atribución.
- **Sesgos y cautelas:** Taxonomía propietaria; las reasignaciones alteran series históricas por categoría.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Revisiones periódicas de definiciones (ediciones 2018, 2021, 2024, 2025).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Morningstar Global Category Classifications methodology document»; WebFetch: sí, PDF de octubre de 2024)
- **Origen:** Alta F9_S4 (2026-11-02).
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### MBF-0607 · Q 73 (B) — LPX AG — índices de capital privado cotizado (LPX50, LPX Major Market) y Listed Private Equity Barometer

- **Canal oficial (URL raíz):** https://www.lpx-group.com/ (citado en la ficha del ETF que replica el índice: https://etf.dws.com/nl-nl/AssetDownload/Index/e0151b62-483b-4ee6-9240-069462b88316/Factsheet.pdf · lanzamiento del barómetro: https://www.finews.ch/news/finanzplatz/51858-lpx-listed-private-equity-barometer)
- **Emisor:** LPX AG (Zúrich, Suiza), empresa de investigación e índices de capital privado cotizado
- **Documentación y notas:** Familia de índices de compañías de capital privado cotizadas (gestoras, vehículos y sociedades de inversión): el LPX50 (50 compañías) y el LPX Major Market (25 compañías más líquidas, ponderadas por capitalización ajustada por free float, revisión semestral, tope del 15 % por componente; ficha a 30/09/2026). Desde el 14/06/2022 publica el «Listed Private Equity Barometer» trimestral con valoraciones, descuentos sobre el valor liquidativo (≈ 22 % en mayo de 2022), rentabilidades, asignaciones y métricas ESG.
- **Temática:** TFB-08 Fondos, ETF e índices: datos y documentación (principal) · secundarias: TFB-06, TFB-11
- **Calidad Q:** 73 (B) — Primariedad 17/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 12/15 · Independencia 7/10 · Actualidad 9/10 · Acceso 7/10
- **Tipología:** primaria (proveedor del índice)
- **Acceso:** Valores y fichas públicos en la web; datos completos con licencia
- **Ámbitos:** Capital privado cotizado: rentabilidad, valoración y descuento sobre NAV
- **Motivo de inclusión y uso:** Indicador diario y líquido del ciclo del capital privado (frente a índices de capital privado no cotizado con retraso trimestral), útil para el segmento de gestoras alternativas y vehículos cotizados.
- **Restricciones de uso:** Condiciones de LPX AG; uso de los índices en productos con licencia.
- **Sesgos y cautelas:** Proveedor comercial pequeño y especializado; los índices de cotizadas incorporan beta del mercado de renta variable y descuentos variables sobre NAV. La URL raíz procede de la ficha de DWS, no de una búsqueda directa.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B09 Finanzas y Valoración: descuentos sobre NAV y valoraciones del capital privado cotizado; AG-B12 Seleccionador de Activos: universo de gestoras y vehículos cotizados de capital privado y ETF que replican el índice; AG-B10 Flujos y Sentimiento: señal adelantada del ciclo del capital privado.
- **Origen:** Alta F9_comp (2026-11-03).
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-03 (búsqueda web: «LPX50 index LPX Group listed private equity index methodology»; WebFetch: sí, ficha del ETF de DWS y artículo de finews.ch; la web de LPX no se leyó)

#### RF-0517 · Q 72 (B) — MarketVector Indexes — revisiones trimestrales y semestrales (temáticos y activos digitales)

- **Canal oficial (URL raíz):** https://www.marketvector.com/ (resultados de la revisión del 1T 2025: https://prod.marketvector.com/insights/index-updates/quarterly-and-semi-annual-index-review-results-for-q1-2025 · archivo de noticias: https://marketvector.com/insights/news?page=4)
- **Emisor:** MarketVector Indexes (empresa constituida en Alemania; antes MV Index Solutions, grupo VanEck)
- **Documentación y notas:** Administra índices temáticos, sectoriales y de activos digitales; publica trimestralmente los resultados de sus revisiones (14/03/2025 y anteriores desde 2013) y guías de índices.
- **Temática:** TFB-08 Fondos, ETF e índices: datos y documentación (principal) · secundarias: —
- **Calidad Q:** 72 (B) — Primariedad 17/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 11/15 · Independencia 6/10 · Actualidad 8/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Índices temáticos (semiconductores, energía nuclear, oro y minería, etc.) y de criptoactivos
- **Motivo de inclusión y uso:** Reglas y revisiones de índices subyacentes de ETF temáticos y de criptoactivos. AG-21, AG-22.
- **Uso en el bloque:** AG-B12: índices MarketVector temáticos y sectoriales (semiconductores, uranio, cripto, etc.) como lista inicial de candidatos de una temática.
- **Restricciones de uso:** Uso con atribución.
- **Sesgos y cautelas:** Vinculada a un emisor de ETF (VanEck), según su antigua denominación; la página leída no detalla las familias revisadas.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Cambio de nombre de MV Index Solutions a MarketVector Indexes (2022).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «MarketVector Indexes index guide review announcements marketvector.com»; WebFetch: sí)
- **Origen:** Alta F9_S4 (2026-11-02).
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0526 · Q 68 (B) — ETFGI — informes mensuales del sector mundial de ETF

- **Canal oficial (URL raíz):** https://etfgi.com/ (nota de 19/08/2026 leída: https://etfgi.com/node/28936)
- **Emisor:** ETFGI LLP (consultora independiente; fundadora y socia directora: Deborah Fuhr)
- **Documentación y notas:** Notas de prensa mensuales con patrimonio y flujos de ETF por región, clase de activo y emisor (fin de julio de 2026: 23,11 billones de dólares, récord; entradas de 383.600 M$ en julio y 1,71 billones en el año; 86 meses consecutivos de entradas; 17.654 ETF de 1.025 proveedores en 85 bolsas; ETF activos con 590.460 M$ de entradas en el año). Informes completos por suscripción.
- **Temática:** TFB-08 Fondos, ETF e índices: datos y documentación (principal) · secundarias: TFB-15
- **Calidad Q:** 68 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 12/15 · Independencia 7/10 · Actualidad 9/10 · Acceso 5/10
- **Tipología:** secundaria (agregador)
- **Acceso:** Notas de prensa abiertas; informes de pago
- **Ámbitos:** ETF y ETP mundiales: patrimonio, flujos, lanzamientos y cierres
- **Motivo de inclusión y uso:** Vista global y mensual del mercado de ETF (incluidos ETF activos, temáticos y de cripto). AG-22.
- **Uso en el bloque:** AG-B10 Flujos y Sentimiento: patrimonio y flujos globales de ETF por región, clase y temática; AG-B12 como contexto del universo de vehículos.
- **Restricciones de uso:** Uso con atribución; no redistribuir informes de pago.
- **Sesgos y cautelas:** Metodología de recuento no auditada; titulares orientados a récords; financiada por patrocinio de eventos.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ETFGI reports assets invested in ETFs industry globally record 2026»; WebFetch: sí)
- **Origen:** Alta F9_S4 (2026-11-02).
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0048 · Q 66 (B) — Morningstar — investigación de fondos y valoraciones

- **Canal oficial (URL raíz):** https://global.morningstar.com/ (explicación del Medalist Rating: https://global.morningstar.com/en-gb/funds/whats-changing-not-changing-with-morningstar-medalist-rating · metodología, 31/12/2024: https://morningstar.com/content/cs-images/v3/assets/blt9415ea4cc4157833/blt1a4eaedeeda4b1c2/6781997a969dc5ffde9da0a0/1227010.pdf)
- **Emisor:** Morningstar Inc.
- **Temática:** TFB-08 Fondos, ETF e índices: datos y documentación (principal) · secundarias: TFB-11
- **Calidad Q:** 66 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 12/15 · Independencia 6/10 · Actualidad 9/10 · Acceso 6/10
- **Tipología:** secundaria cualificada
- **Acceso:** Muro parcial (metodologías abiertas)
- **Ámbitos:** Fondos, ETF, flujos, valoraciones de analistas; Medalist Rating (pilares Personas, Proceso y Matriz, más precio; unos 130 analistas, más de 3.200 estrategias)
- **Motivo de inclusión y uso:** Datos y análisis de fondos y flujos con metodología pública. Uso: calidad de gestoras y fondos, y señales de coste.
- **Uso en el bloque:** AG-B12: análisis y calificaciones de fondos y ETF y estimaciones de valor razonable de acciones de Morningstar como contraste (no como prueba); AG-B09.
- **Sesgos y cautelas:** Calificaciones con conflictos potenciales (patrocinio); metodología revisada (sin curva forzada, comparación con la media de la categoría), con más medallas Gold y Silver tras el cambio.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Morningstar Medalist Rating methodology fund research»; WebFetch: sí)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada en verificación de alta 2026-11-02 (tanda 2); URL raíz corregida.

<!-- ===== Tanda 3 (2026-11-02): 25 búsquedas WebSearch. Las fichas se fusionan en su temática y por Q descendente. ===== -->
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0529 · Q 66 (B) — justETF — buscador y base de datos de ETF UCITS en Europa

- **Canal oficial (URL raíz):** https://www.justetf.com/ (buscador: https://justetf.com/en/find-etf.html)
- **Emisor:** justETF (plataforma independiente de información sobre ETF, Alemania)
- **Documentación y notas:** Buscador con unos 4.974 productos cotizados (2.921 de renta variable, 1.564 de bonos, materias primas, cripto, metales preciosos, monetarios e inmobiliarios) y 3.167 índices subyacentes; comparador, fichas por ETF y configuración por país (Alemania, Austria, Suiza, Reino Unido, Italia, Francia, España, Países Bajos, Bélgica, Luxemburgo).
- **Temática:** TFB-08 Fondos, ETF e índices: datos y documentación (principal) · secundarias: —
- **Calidad Q:** 66 (B) — Primariedad 13/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 10/15 · Independencia 6/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** secundaria (agregador)
- **Acceso:** Abierto (funciones avanzadas de pago)
- **Ámbitos:** Oferta de ETF UCITS por índice, clase de activo, coste y domicilio
- **Motivo de inclusión y uso:** Mapear qué índices y segmentos tienen vehículo cotizado en Europa (amplitud de oferta por ámbito), sin seleccionar productos. AG-22, AG-21.
- **Uso en el bloque:** AG-B12: buscador de ETF UCITS (TER, réplica, domicilio, tamaño, índice) para identificar vehículos de acceso a un sector o temática desde Europa.
- **Restricciones de uso:** Uso con atribución; no constituye asesoramiento.
- **Sesgos y cautelas:** Ingresos por afiliación con brókers; cobertura no exhaustiva; datos de terceros.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «justETF ETF screener Europe UCITS ETF database»; WebFetch: sí)
- **Origen:** Alta F9_S4 (2026-11-02).
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### MBF-0217 · Q 65 (B) — Trackinsight — base de datos y buscador de ETF

- **Canal oficial (URL raíz):** https://www.trackinsight.com/ (ficha leída: https://www.trackinsight.com/en/fund/ISRG/characteristics)
- **Emisor:** Trackinsight (empresa privada)
- **Documentación y notas:** Fichas de ETF con emisor, ISIN, patrimonio por fondo y clase, TER, VL, política de dividendos, número de posiciones, fecha de lanzamiento, domicilio, estructura legal y elegibilidad fiscal; pestañas de cartera, rentabilidad, flujos, distribución, riesgo y ESG; páginas por emisor (p. ej., Amundi: 674 fondos y 489.300 M€). Cuenta gratuita («forever free toolbox») con más datos y filtros; servicios de datos de pago; encuesta anual Global ETF Survey.
- **Temática:** TFB-08 Fondos, ETF e índices: datos y documentación (principal) · secundarias: TFB-15
- **Calidad Q:** 65 (B) — Primariedad 11/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 10/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 7/10
- **Tipología:** secundaria (agregador)
- **Acceso:** Freemium; registro gratuito para más datos
- **Ámbitos:** ETF globales (UCITS y EE. UU.): características, carteras, flujos y riesgo
- **Motivo de inclusión y uso:** Complemento de justETF (RF-0529) con flujos y carteras por ETF y comparación entre emisores.
- **Uso en el bloque:** AG-B12 (selección del vehículo para un sector o temática) y AG-B10 Flujos y Sentimiento (flujos por ETF temático).
- **Restricciones de uso:** Registro gratuito para funciones ampliadas; comparación limitada sin cuenta; credenciales en HT-01.
- **Sesgos y cautelas:** Datos de terceros y de emisores; modelo de negocio con servicios a gestoras.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «iShares ETF holdings download Xtrackers Amundi ETF KID PRIIPs key information document ETF.com»; WebFetch: sí)
- **Origen:** Alta F9 Bloque B (2026-11-02).

## TFB-09 Patentes, innovación y tecnología

#### MBF-0219 · Q 89 (A) — Oficina Europea de Patentes (EPO) — Espacenet

- **Canal oficial (URL raíz):** http://worldwide.espacenet.com/ (según la guía de la University at Buffalo: https://research.lib.buffalo.edu/patents/patent-databases)
- **Emisor:** European Patent Office (EPO)
- **Documentación y notas:** Buscador gratuito de documentos de patente de todo el mundo (incluye EE. UU.), con búsqueda por la Clasificación Cooperativa de Patentes (CPC), familias, citas y estado legal (vía INPADOC).
- **Temática:** TFB-09 Patentes, innovación y tecnología (principal)
- **Calidad Q:** 89 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Patentes mundiales: familias, solicitantes, clasificación, citas
- **Motivo de inclusión y uso:** Base oficial para medir la actividad inventiva de empresas y tecnologías y comprobar carteras de patentes de candidatos.
- **Uso en el bloque:** AG-B06 Tecnología (mapa de patentes por tecnología y solicitante; foso tecnológico) y AG-B03 (concentración de la propiedad industrial); AG-B12 para comprobar la cartera de patentes de un candidato.
- **Restricciones de uso:** Uso libre con límites de consulta; para extracción masiva usar los servicios OPS de la EPO (registro gratuito).
- **Sesgos y cautelas:** El recuento de patentes no mide valor; desfase de 18 meses entre solicitud y publicación.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-03 (búsqueda web: «free patent databases Espacenet PATENTSCOPE Google Patents Lens.org PatentsView research guide»; WebFetch: sí, sobre la guía índice de la University at Buffalo)
- **Origen:** Alta F9 Bloque B (2026-11-03).

#### MBF-0220 · Q 89 (A) — OMPI (WIPO) — PATENTSCOPE

- **Canal oficial (URL raíz):** http://patentscope.wipo.int/search/en/search.jsf (según la guía índice https://research.lib.buffalo.edu/patents/patent-databases)
- **Emisor:** Organización Mundial de la Propiedad Intelectual (OMPI/WIPO)
- **Documentación y notas:** Base de datos de la OMPI con más de 67 millones de documentos de patente de más de 50 países, incluidas todas las solicitudes internacionales PCT; traducción automática y búsqueda multilingüe (CLIR).
- **Temática:** TFB-09 Patentes, innovación y tecnología (principal)
- **Calidad Q:** 89 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Solicitudes PCT y colecciones nacionales (incluidas Asia y Latinoamérica)
- **Motivo de inclusión y uso:** Fuente primaria para seguir solicitudes internacionales PCT, indicador temprano de apuestas tecnológicas globales.
- **Uso en el bloque:** AG-B06 Tecnología (vigilancia de solicitudes PCT por tecnología y empresa) y AG-B13 Prospectiva.
- **Restricciones de uso:** Uso libre; condiciones de uso de la OMPI.
- **Sesgos y cautelas:** Calidad de traducción automática variable; las PCT no implican concesión.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-03 (búsqueda web: «free patent databases Espacenet PATENTSCOPE Google Patents Lens.org PatentsView research guide»; WebFetch: sí, sobre la guía índice de la University at Buffalo)
- **Origen:** Alta F9 Bloque B (2026-11-03).

#### MBF-0223 · Q 89 (A) — USPTO — Patent Public Search (patentes y solicitudes de EE. UU.)

- **Canal oficial (URL raíz):** https://www.uspto.gov/patents/search (según la guía índice https://research.lib.buffalo.edu/patents/patent-databases)
- **Emisor:** United States Patent and Trademark Office (USPTO)
- **Documentación y notas:** Texto completo gratuito de las patentes de EE. UU. desde 1790 y de las solicitudes publicadas desde el 15/03/2001.
- **Temática:** TFB-09 Patentes, innovación y tecnología (principal)
- **Calidad Q:** 89 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto (dominio público)
- **Ámbitos:** Patentes concedidas y solicitudes de EE. UU.
- **Motivo de inclusión y uso:** Registro oficial del mayor mercado tecnológico; comprobación de patentes concretas citadas por empresas.
- **Uso en el bloque:** AG-B06 Tecnología y AG-B12 (verificación de patentes clave de un candidato); AG-B07 para litigios y regulación de propiedad industrial.
- **Restricciones de uso:** Uso libre.
- **Sesgos y cautelas:** Solo EE. UU.; búsqueda booleana exigente.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-03 (búsqueda web: «free patent databases Espacenet PATENTSCOPE Google Patents Lens.org PatentsView research guide»; WebFetch: sí, sobre la guía índice de la University at Buffalo)
- **Origen:** Alta F9 Bloque B (2026-11-03).

#### MBF-0228 · Q 88 (A) — OMPI (WIPO) — IP Statistics Data Center

- **Canal oficial (URL raíz):** https://www.wipo.int/ipstats/en/ (ayuda: https://www.wipo.int/ipstats/en/help/)
- **Emisor:** Organización Mundial de la Propiedad Intelectual (OMPI/WIPO)
- **Documentación y notas:** Servicio en línea gratuito con estadísticas de patentes, modelos de utilidad, marcas y diseños por oficina, origen y tecnología; descarga de series actuales e históricas (algunas anteriores a 1980; PCT 1985–1999). Publicaciones asociadas: World Intellectual Property Indicators (anual), PCT Yearly Review, WIPO IP Facts and Figures 2025.
- **Temática:** TFB-09 Patentes, innovación y tecnología (principal) · secundarias: TFB-01
- **Calidad Q:** 88 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** primaria (estadística oficial)
- **Acceso:** Abierto
- **Ámbitos:** Solicitudes y concesiones de PI por país, oficina y campo tecnológico
- **Motivo de inclusión y uso:** Series comparables entre países para medir dónde crece la actividad inventiva en cada tecnología.
- **Uso en el bloque:** AG-B06 Tecnología (dinámica de patentes por campo técnico) y AG-B07 (competencia tecnológica entre países); Motor AG-B16 para series.
- **Restricciones de uso:** Uso con atribución a la OMPI.
- **Sesgos y cautelas:** Datos anuales con desfase; diferencias de práctica entre oficinas.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-03 (búsqueda web: «WIPO Global Innovation Index 2025 IP Statistics Data Center patent filings»; WebFetch: sí)
- **Origen:** Alta F9 Bloque B (2026-11-03).

#### MBF-0224 · Q 87 (A) — USPTO — PatentsView (datos de patentes desambiguados)

- **Canal oficial (URL raíz):** https://patentsview.org/what-is-patentsview · Nota de actualización: https://www.uspto.gov/subscription-center/2026/patentsview-releases-q4-2025-data-update
- **Emisor:** USPTO (Office of the Chief Economist)
- **Documentación y notas:** Plataforma que convierte los registros de patentes de EE. UU. en conjuntos de datos de calidad investigadora (inventores, titulares y ubicaciones desambiguados). Actualización Q4 2025 (datos hasta el 31/12/2025) publicada el 06/05/2026; descargas y diccionarios trasladados al directorio de datos masivos del USPTO Open Data Portal (ODP). Tablas de descarga masiva (reivindicaciones, resúmenes, descripciones).
- **Temática:** TFB-09 Patentes, innovación y tecnología (principal) · secundarias: TFB-18
- **Calidad Q:** 87 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria (datos oficiales procesados)
- **Acceso:** Abierto
- **Ámbitos:** Patentes de EE. UU. por titular, inventor, ubicación y tecnología
- **Motivo de inclusión y uso:** Permite cuantificar carteras de patentes por empresa (titular desambiguado) y por tecnología, en bloque.
- **Uso en el bloque:** Motor AG-B16 (MC-B de intensidad y concentración de patentes por empresa y sector) y AG-B06 Tecnología; AG-B12 para comparar candidatos por actividad inventiva.
- **Restricciones de uso:** Uso libre; la API del ODP puede requerir clave gratuita (comprobar guía de transición).
- **Sesgos y cautelas:** Solo EE. UU.; desambiguación algorítmica con errores; migración al ODP en curso (rutas cambiantes).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** 2026: traslado de descargas al USPTO Open Data Portal.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-03 (búsqueda web: «USPTO PatentsView bulk data download API EPO Patent Index 2025 statistics»; WebFetch: sí, nota del USPTO)
- **Origen:** Alta F9 Bloque B (2026-11-03).

#### MBF-0227 · Q 87 (A) — OCDE — Main Science and Technology Indicators (MSTI)

- **Canal oficial (URL raíz):** https://oecd.org/sti/msti.htm (conjunto de datos: https://www.oecd.org/en/data/datasets/main-science-and-technology-indicators.html)
- **Emisor:** OCDE — Dirección de Ciencia, Tecnología e Innovación
- **Documentación y notas:** Indicadores de recursos financieros y humanos dedicados a I+D (gasto total, empresarial y público en I+D; personal investigador), complementados con datos de patentes y comercio internacional de industrias intensivas en I+D, para países de la OCDE y economías asociadas. Publicación semestral histórica.
- **Temática:** TFB-09 Patentes, innovación y tecnología (principal) · secundarias: TFB-01
- **Calidad Q:** 87 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** primaria (estadística oficial)
- **Acceso:** Abierto (OECD Data Explorer)
- **Ámbitos:** GERD, BERD, investigadores, patentes triádicas, comercio de alta tecnología
- **Motivo de inclusión y uso:** Comparación internacional del esfuerzo en I+D por país y sector ejecutor.
- **Uso en el bloque:** AG-B06 Tecnología y AG-B08 Macro (capacidad innovadora de mercados geográficos); AG-B13 Prospectiva.
- **Restricciones de uso:** Condiciones de la OCDE (uso con atribución).
- **Sesgos y cautelas:** Desfase de uno a dos años; rupturas de serie por cambios metodológicos nacionales.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Migración de OECD.Stat al OECD Data Explorer.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-03 (búsqueda web: «OECD Main Science and Technology Indicators MSTI database GERD BERD 2026»; WebFetch: sí)
- **Origen:** Alta F9 Bloque B (2026-11-03).

#### MBF-0237 · Q 87 (A) — NSF/NCSES y National Science Board — Science and Engineering Indicators 2026

- **Canal oficial (URL raíz):** https://www.ncses.nsf.gov/indicators (citas: https://ncses.nsf.gov/pubs/nsb20262/acknowledgments-and-citation)
- **Emisor:** National Science Board (NSB) y National Center for Science and Engineering Statistics (NCSES) de la National Science Foundation
- **Documentación y notas:** Evaluación de referencia del panorama de la investigación en EE. UU. y el mundo (I+D, educación STEM, fuerza laboral, innovación); edición 2026 publicada el 12/05/2026 según nota de la Universidad de Utah. Indicadores bibliométricos con documentación técnica de Science-Metrix.
- **Temática:** TFB-09 Patentes, innovación y tecnología (principal) · secundarias: TFB-01
- **Calidad Q:** 87 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** primaria (estadística oficial)
- **Acceso:** Abierto (dominio público)
- **Ámbitos:** I+D por país y sector, publicaciones científicas, patentes, industrias intensivas en conocimiento
- **Motivo de inclusión y uso:** Comparación EE. UU.–China–UE de capacidades científicas y tecnológicas.
- **Uso en el bloque:** AG-B06 y AG-B07 Regulación y Geopolítica (competencia tecnológica entre bloques); AG-B13 Prospectiva.
- **Restricciones de uso:** Uso libre con cita.
- **Sesgos y cautelas:** Bienal; centrado en EE. UU.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Formato de informes temáticos desde 2020.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-03 (búsqueda web: «NSF NCSES Science and Engineering Indicators 2026 arXiv submission statistics»; WebFetch: sí, sobre la nota de la Universidad de Utah)
- **Origen:** Alta F9 Bloque B (2026-11-03).

#### MBF-0615 · Q 87 (A) — NLM (NIH) — ClinicalTrials.gov: registro de ensayos clínicos

- **Canal oficial (URL raíz):** https://classic.clinicaltrials.gov/ct2/about-site/modernization (sitio actual: https://clinicaltrials.gov/)
- **Emisor:** U.S. National Library of Medicine (NLM), National Institutes of Health
- **Documentación y notas:** Registro y base de resultados de ensayos clínicos con financiación pública y privada de todo el mundo. El sitio modernizado se lanzó el 21/06/2023 (el clásico se retiró en 2024), con nueva API, guardado de estudios y RSS.
- **Temática:** TFB-09 Patentes, innovación y tecnología (principal) · secundarias: TFB-04
- **Calidad Q:** 87 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria (registro obligatorio para ensayos sujetos a la normativa de EE. UU.)
- **Acceso:** Abierto, sin registro; API gratuita
- **Ámbitos:** Ensayos por fase, patología, intervención, promotor, estado de reclutamiento y resultados
- **Motivo de inclusión y uso:** Fuente primaria para medir la cartera clínica de empresas y terapias y anticipar catalizadores (lecturas de fase 3).
- **Restricciones de uso:** Uso libre; citar el identificador NCT.
- **Sesgos y cautelas:** Datos declarados por el promotor; fechas previstas que se retrasan; no todos los ensayos fuera de EE. UU. se registran.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Modernización del sitio (2023) y retirada del sitio clásico (2024).
- **Uso en el bloque:** AG-B06 Tecnología: carteras clínicas por área terapéutica y fase; AG-B12 Seleccionador de Activos: catalizadores de biotecnológicas y farmacéuticas candidatas; AG-B03 Estructura y Competencia: intensidad competitiva por indicación.
- **Origen:** Alta F9_comp (2026-11-03).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-03 (búsqueda web: «ClinicalTrials.gov API v2 data NLM modernized»; WebFetch: sí, página de modernización)

#### MBF-0229 · Q 86 (A) — OMPI (WIPO) — World Intellectual Property Indicators 2025

- **Canal oficial (URL raíz):** https://www.wipo.int/edocs/pubdocs/en/wipo-pub-941-2025-en-world-intellectual-property-indicators-2025.pdf · Resumen: https://www.wipo.int/web-publications/world-intellectual-property-indicators-2025-highlights/en/index.html
- **Emisor:** OMPI/WIPO
- **Documentación y notas:** Informe anual de patentes, modelos de utilidad, marcas, diseños industriales, microorganismos, obtenciones vegetales, indicaciones geográficas y economía creativa; la edición 2025 usa datos de 2024.
- **Temática:** TFB-09 Patentes, innovación y tecnología (principal)
- **Calidad Q:** 86 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** primaria (informe estadístico)
- **Acceso:** Abierto
- **Ámbitos:** Tendencias mundiales de PI por país, oficina y tecnología
- **Motivo de inclusión y uso:** Lectura anual de qué países y campos técnicos lideran el crecimiento de solicitudes.
- **Uso en el bloque:** AG-B06 Tecnología y AG-B13 Prospectiva.
- **Restricciones de uso:** Uso con atribución.
- **Sesgos y cautelas:** Desfase anual.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-03 (búsqueda web: «WIPO Global Innovation Index 2025 IP Statistics Data Center patent filings»; WebFetch: no)
- **Origen:** Alta F9 Bloque B (2026-11-03).

#### MBF-0238 · Q 86 (A) — Oficina Europea de Patentes (EPO) — estadísticas y descarga de datos (Technology Dashboard / Patent Index)

- **Canal oficial (URL raíz):** https://epo.org/en/about-us/statistics/data-download
- **Emisor:** European Patent Office (EPO)
- **Documentación y notas:** Hojas Excel con todos los datos del EPO Technology Dashboard 2025 (solicitudes de patente europea por país, campo y solicitante), datos de otras oficinas e IP5 y estadísticas de actividad de la EPO; Statistics & Trends Centre como visualizador dinámico.
- **Temática:** TFB-09 Patentes, innovación y tecnología (principal)
- **Calidad Q:** 86 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** primaria (estadística oficial)
- **Acceso:** Abierto
- **Ámbitos:** Solicitudes europeas por tecnología, país y empresa (ranking de solicitantes)
- **Motivo de inclusión y uso:** Ranking anual de empresas solicitantes y campos de mayor crecimiento en Europa.
- **Uso en el bloque:** AG-B06 Tecnología y AG-B03 (liderazgo tecnológico por empresa); AG-B12.
- **Restricciones de uso:** Uso con atribución.
- **Sesgos y cautelas:** Anual; las solicitudes miden intención, no valor.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** El antiguo «Patent Index» se presenta como Technology Dashboard.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-03 (búsqueda web: «USPTO PatentsView bulk data download API EPO Patent Index 2025 statistics»; WebFetch: sí)
- **Origen:** Alta F9 Bloque B (2026-11-03).

#### MBF-0225 · Q 85 (A) — INPIT/JPO — J-PlatPat (Japan Platform for Patent Information)

- **Canal oficial (URL raíz):** https://www.j-platpat.inpit.go.jp/web/all/top/BTmTopEnglishPage (según la guía índice https://research.lib.buffalo.edu/patents/patent-databases)
- **Emisor:** National Center for Industrial Property Information and Training (INPIT), Oficina Japonesa de Patentes
- **Documentación y notas:** Plataforma gratuita de búsqueda de patentes, modelos de utilidad, diseños y marcas de Japón, con interfaz en inglés.
- **Temática:** TFB-09 Patentes, innovación y tecnología (principal)
- **Calidad Q:** 85 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Patentes japonesas (electrónica, automoción, materiales, robótica)
- **Motivo de inclusión y uso:** Cobertura primaria de una de las tres grandes oficinas, clave en cadenas de suministro tecnológicas.
- **Uso en el bloque:** AG-B06 Tecnología y AG-B05 (tecnologías de proveedores japoneses).
- **Restricciones de uso:** Uso libre; límites de consulta.
- **Sesgos y cautelas:** Parte de los documentos solo en japonés.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-03 (búsqueda web: «free patent databases Espacenet PATENTSCOPE Google Patents Lens.org PatentsView research guide»; WebFetch: sí, sobre la guía índice)
- **Origen:** Alta F9 Bloque B (2026-11-03).

#### MBF-0616 · Q 85 (A) — EMA — Clinical Trials Information System (CTIS) y sitio público de ensayos de la UE (Reglamento (UE) 536/2014)

- **Canal oficial (URL raíz):** https://www.ema.europa.eu/en/human-regulatory-overview/research-development/clinical-trials-human-medicines/clinical-trials-information-system (sitio público: https://euclinicaltrials.eu · ensayos anteriores: clinicaltrialsregister.eu)
- **Emisor:** Agencia Europea de Medicamentos (EMA), con los Estados miembros, el EEE y la Comisión Europea
- **Documentación y notas:** Sistema que aplica el Reglamento de ensayos clínicos (UE) 536/2014: solicitudes, evaluación y resultados; sitio público con búsqueda de ensayos desde el 31/01/2022 (número de ensayo UE, área terapéutica, promotor, fechas de reclutamiento, inicio y fin), mapa de ensayos (marzo de 2025) y normas de transparencia revisadas (18/06/2024). Los ensayos iniciados con la Directiva antes del 31/01/2023 están en el EU Clinical Trials Register.
- **Temática:** TFB-09 Patentes, innovación y tecnología (principal) · secundarias: TFB-03, TFB-04
- **Calidad Q:** 85 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** primaria (registro regulatorio oficial)
- **Acceso:** Abierto, sin registro
- **Ámbitos:** Ensayos clínicos autorizados en la UE/EEE
- **Motivo de inclusión y uso:** Complemento europeo de ClinicalTrials.gov para carteras de empresas europeas y ensayos multinacionales.
- **Restricciones de uso:** Uso libre con atribución.
- **Sesgos y cautelas:** Información retenida por confidencialidad comercial o datos personales; cobertura del portal desde 2022.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Transparencia revisada en 2024; transición desde la Directiva de ensayos.
- **Uso en el bloque:** AG-B06 Tecnología y AG-B12 Seleccionador de Activos: ensayos de empresas europeas y calendario de resultados; AG-B07 Regulación: aplicación del Reglamento de ensayos clínicos.
- **Origen:** Alta F9_comp (2026-11-03).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-03 (búsqueda web: «ClinicalTrials.gov API data and EU Clinical Trials Information System CTIS public portal search»; WebFetch: sí)

#### MBF-0614 · Q 84 (A) — ETSI — normas y especificaciones de telecomunicaciones (descarga gratuita en PDF)

- **Canal oficial (URL raíz):** https://www.etsi.org/standards/types-of-standards (buscador: etsi.org/standards-search · ejemplo de entregable: https://www.etsi.org/deliver/etsi_ts/124500_124599/124543/18.00.00_60/ts_124543v180000p.pdf)
- **Emisor:** European Telecommunications Standards Institute (ETSI), Sophia Antipolis
- **Documentación y notas:** Entregables EN, ES, EG, TS, TR, SR, GS y GR (incluidas las especificaciones 3GPP publicadas como TS de ETSI y las normas armonizadas de la Directiva de equipos radioeléctricos y CEM), descargables en PDF gratis; versión Word restringida.
- **Temática:** TFB-09 Patentes, innovación y tecnología (principal) · secundarias: TFB-03
- **Calidad Q:** 84 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 14/15 · Independencia 9/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria (organismo europeo de normalización)
- **Acceso:** Abierto: descarga gratuita en PDF
- **Ámbitos:** Telecomunicaciones (5G/6G vía 3GPP), radio, ciberseguridad, IoT, firma electrónica, normas armonizadas
- **Motivo de inclusión y uso:** Única fuente de normalización con texto completo gratuito: permite seguir la evolución técnica de 5G/6G, ciberseguridad e IoT.
- **Restricciones de uso:** Uso según los términos de ETSI (PDF libre).
- **Sesgos y cautelas:** El volumen de especificaciones no equivale a adopción comercial; peso de los grandes fabricantes en los grupos.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B06 Tecnología: hitos de estandarización (versiones 3GPP, ciberseguridad de IoT) como indicador de madurez; AG-B07: normas armonizadas exigidas por la UE; AG-B03: posición de los fabricantes en la normalización.
- **Origen:** Alta F9_comp (2026-11-03).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-03 (búsqueda web: «ETSI standards search free download deliverables etsi.org»; WebFetch: sí)

#### MBF-0231 · Q 83 (A) — Comisión Europea (JRC) — EU Industrial R&D Investment Scoreboard

- **Canal oficial (URL raíz):** https://iri.jrc.ec.europa.eu/scoreboard (repositorio JRC: https://publications.jrc.ec.europa.eu/repository/handle/JRC144638)
- **Emisor:** Comisión Europea — Centro Común de Investigación (JRC) y DG Investigación e Innovación (proyecto IRI)
- **Documentación y notas:** Clasificación anual de las 2.500 empresas del mundo que más invierten en I+D (gasto, intensidad, ventas, beneficio, empleo por empresa, sector y país). Última edición: 2025, fechada el 22/12/2025.
- **Temática:** TFB-09 Patentes, innovación y tecnología (principal) · secundarias: TFB-07
- **Calidad Q:** 83 (A) — Primariedad 17/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 14/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** primaria (datos compilados de cuentas anuales)
- **Acceso:** Abierto
- **Ámbitos:** I+D empresarial por empresa, sector y región
- **Motivo de inclusión y uso:** Datos comparables de intensidad de I+D por empresa, ideales para ordenar candidatos dentro de un sector tecnológico.
- **Uso en el bloque:** AG-B06 Tecnología y AG-B12 (intensidad de I+D de candidatos); AG-B03 (concentración de la I+D sectorial); Motor AG-B16.
- **Restricciones de uso:** Uso con atribución a la Comisión Europea.
- **Sesgos y cautelas:** I+D contable (criterios distintos entre NIIF y US GAAP); solo grandes empresas.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-03 (búsqueda web: «EU Industrial R&D Investment Scoreboard 2025 JRC European Innovation Scoreboard»; WebFetch: sí)
- **Origen:** Alta F9 Bloque B (2026-11-03).

#### MBF-0236 · Q 83 (A) — arXiv — categorías tecnológicas (cs, quant-ph, cond-mat, eess) y estadísticas de envíos

- **Canal oficial (URL raíz):** https://arxiv.org/ (estadísticas de envíos por área: https://info.arxiv.org/help/stats/2021_by_area)
- **Emisor:** arXiv (Cornell University)
- **Documentación y notas:** Repositorio abierto de preprints; las categorías cs.AI, cs.LG, cs.CL, quant-ph, cond-mat y eess permiten seguir la frontera de la investigación en IA, computación cuántica, materiales y electrónica; publica estadísticas de envíos por área. La categoría q-fin se registra aparte (RF-0010, área TFB-18).
- **Temática:** TFB-09 Patentes, innovación y tecnología (principal) · secundarias: TFB-18
- **Calidad Q:** 83 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 13/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria (preprints sin revisión por pares)
- **Acceso:** Abierto
- **Ámbitos:** Investigación de frontera en IA, cuántica, semiconductores, materiales
- **Motivo de inclusión y uso:** Indicador adelantado de avances técnicos y de qué empresas publican investigación.
- **Uso en el bloque:** AG-B06 Tecnología (madurez y ritmo de una tecnología; autoría corporativa) y AG-B13 Prospectiva.
- **Restricciones de uso:** Licencia de cada artículo; API pública con límites de frecuencia.
- **Sesgos y cautelas:** Sin revisión por pares; volumen enorme (filtrar por citas o fuentes secundarias).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-03 (búsqueda web: «NSF NCSES Science and Engineering Indicators 2026 arXiv submission statistics» → «arXiv submission rate statistics»; WebFetch: no)
- **Origen:** Alta F9 Bloque B (2026-11-03).

#### RF-0349 · Q 83 (A) — Stanford HAI — AI Index Report

- **Canal oficial (URL raíz):** https://hai.stanford.edu/ai-index/2026-ai-index-report
- **Emisor:** Stanford Institute for Human-Centered Artificial Intelligence (HAI)
- **Documentación y notas:** Informe anual en nueve capítulos (I+D, rendimiento técnico, IA responsable, economía, ciencia, medicina, educación, política, opinión pública); inversión privada en IA por país (EE. UU. 285.880 M$ en 2025); datos públicos en carpeta compartida y PDF completo.
- **Temática:** TFB-09 Patentes, innovación y tecnología (principal) · secundarias: TFB-11
- **Calidad Q:** 83 (A) — Primariedad 16/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** secundaria
- **Acceso:** Abierto
- **Ámbitos:** Inversión, adopción, capacidades y regulación de la IA
- **Motivo de inclusión y uso:** Referencia académica independiente sobre el ciclo de inversión en IA.
- **Uso en el bloque:** AG-B06 Tecnología: indicadores anuales de IA (inversión, rendimiento técnico, adopción, coste de modelos, patentes); AG-B04 Demanda y Adopción; AG-B13 Prospectiva.
- **Restricciones de uso:** Citar edición y capítulo; licencia de datos no declarada en la página.
- **Sesgos y cautelas:** Compilación de fuentes de terceros con métodos heterogéneos.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Stanford HAI AI Index Report 2026»; WebFetch: sí)
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### MBF-0222 · Q 81 (A) — The Lens (Cambia) — patentes y literatura científica enlazadas

- **Canal oficial (URL raíz):** https://www.lens.org/ (según la guía índice https://research.lib.buffalo.edu/patents/patent-databases)
- **Emisor:** Cambia (organización sin ánimo de lucro, Australia)
- **Documentación y notas:** Base de datos libre y abierta con millones de registros de patentes de más de 95 jurisdicciones, enlazados con literatura académica; búsqueda de secuencias genéticas.
- **Temática:** TFB-09 Patentes, innovación y tecnología (principal) · secundarias: TFB-18
- **Calidad Q:** 81 (A) — Primariedad 17/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 12/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** secundaria (agregador abierto)
- **Acceso:** Abierto; registro gratuito para exportaciones y colecciones
- **Ámbitos:** Patentes, citas patente-ciencia, biotecnología
- **Motivo de inclusión y uso:** Permite medir el vínculo ciencia–patente de empresas y tecnologías (útil en biotecnología y materiales).
- **Uso en el bloque:** AG-B06 Tecnología y Motor AG-B16 (paneles de patentes y citas).
- **Restricciones de uso:** Uso no comercial gratuito; uso comercial con licencia.
- **Sesgos y cautelas:** Depende de fuentes oficiales para la cobertura.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-03 (búsqueda web: «free patent databases Espacenet PATENTSCOPE Google Patents Lens.org PatentsView research guide»; WebFetch: sí, sobre la guía índice)
- **Origen:** Alta F9 Bloque B (2026-11-03).

#### MBF-0612 · Q 81 (A) — ISO — Online Browsing Platform (OBP) y catálogo de normas internacionales

- **Canal oficial (URL raíz):** https://www.iso.org/obp/ui (ayuda: https://help.iso.org/en/articles/376008-what-is-the-iso-online-browsing-platform-obp · búsqueda avanzada: https://www.iso.org/advanced-search/x/)
- **Emisor:** International Organization for Standardization (ISO), Ginebra
- **Documentación y notas:** Plataforma de búsqueda y acceso a las normas ISO: vista previa gratuita del prólogo, introducción, objeto y campo de aplicación, referencias normativas y términos y definiciones; búsqueda de símbolos gráficos. El texto completo de las normas es de pago.
- **Temática:** TFB-09 Patentes, innovación y tecnología (principal) · secundarias: TFB-03
- **Calidad Q:** 81 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 7/10
- **Tipología:** primaria (organismo internacional de normalización)
- **Acceso:** Búsqueda y vista previa gratuitas; normas completas de pago
- **Ámbitos:** Normas internacionales por sector y tecnología, con estado (en desarrollo, publicada, retirada)
- **Motivo de inclusión y uso:** Seguir qué normas existen o se preparan en una tecnología indica madurez y convergencia del mercado (p. ej., baterías, hidrógeno, IA, ciberseguridad).
- **Restricciones de uso:** Condiciones de ISO; textos completos con licencia (de pago, futuro).
- **Sesgos y cautelas:** El catálogo no mide adopción; la elaboración depende de los comités técnicos con fuerte peso de la industria.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B06 Tecnología: madurez y estandarización de tecnologías (estado de normas por comité técnico); AG-B07 Regulación y Geopolítica: normas citadas por la regulación; AG-B03: barreras de entrada por certificación.
- **Origen:** Alta F9_comp (2026-11-03).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-03 (búsqueda web: «ISO Online Browsing Platform standards catalogue CEN-CENELEC standards search ETSI standards free download»; WebFetch: sí, artículo de ayuda de ISO y guía de KAN)

#### MBF-0230 · Q 80 (A) — OMPI (WIPO) — Global Innovation Index 2025

- **Canal oficial (URL raíz):** https://www.wipo.int/pressroom/en/articles/2025/article_0009.html (nota de lanzamiento devuelta por la búsqueda)
- **Emisor:** OMPI/WIPO (con el Portulans Institute y socios académicos)
- **Documentación y notas:** Índice anual de capacidad innovadora de unas 130 economías; la edición 2025 sitúa en cabeza a Suiza, Suecia, EE. UU., Corea y Singapur, con China en el top 10, y señala la desaceleración de la inversión en innovación. Incluye el rastreador de clústeres de ciencia y tecnología.
- **Temática:** TFB-09 Patentes, innovación y tecnología (principal) · secundarias: TFB-11
- **Calidad Q:** 80 (A) — Primariedad 15/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 14/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** secundaria (índice compuesto)
- **Acceso:** Abierto
- **Ámbitos:** Innovación por economía, clústeres tecnológicos, financiación de la innovación
- **Motivo de inclusión y uso:** Comparar el entorno innovador de mercados geográficos candidatos.
- **Uso en el bloque:** AG-B06 y AG-B08 (atractivo innovador de mercados geográficos); AG-B13.
- **Restricciones de uso:** Uso con atribución.
- **Sesgos y cautelas:** Índice compuesto sensible a ponderaciones y cobertura de datos.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Revisiones metodológicas anuales.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-03 (búsqueda web: «WIPO Global Innovation Index 2025 IP Statistics Data Center patent filings»; WebFetch: no)
- **Origen:** Alta F9 Bloque B (2026-11-03).

#### MBF-0613 · Q 80 (A) — CEN y CENELEC — buscador de normas europeas

- **Canal oficial (URL raíz):** https://standards.cencenelec.eu/ords/f?p=CEN%3A105%3A%3ARESET%3A%3A%3A%3A (portal: https://cencenelec.eu/ · guía de búsqueda de KAN: https://www.kan.de/en/knowledge/searching-for-standards/)
- **Emisor:** Comité Europeo de Normalización (CEN) y Comité Europeo de Normalización Electrotécnica (CENELEC)
- **Documentación y notas:** Buscador oficial de normas europeas (EN) y documentos en preparación por comité técnico, con estado y fechas; incluye las normas armonizadas que dan presunción de conformidad con la legislación de la UE. Búsqueda gratuita; los documentos se compran a los organismos nacionales (p. ej., UNE en España).
- **Temática:** TFB-09 Patentes, innovación y tecnología (principal) · secundarias: TFB-03
- **Calidad Q:** 80 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 14/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 7/10
- **Tipología:** primaria (organismos europeos de normalización)
- **Acceso:** Búsqueda gratuita; normas de pago a través de los organismos nacionales
- **Ámbitos:** Normas europeas y armonizadas por sector (maquinaria, construcción, electrotecnia, energía…)
- **Motivo de inclusión y uso:** Las normas armonizadas condicionan el acceso al mercado de la UE (marcado CE) y el calendario de nuevas regulaciones de producto.
- **Restricciones de uso:** Condiciones de CEN-CENELEC y de los organismos nacionales; textos de pago (futuro).
- **Sesgos y cautelas:** URL de búsqueda tomada de la guía de KAN (página índice), no leída directamente.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B06 Tecnología y AG-B07 Regulación y Geopolítica: normas armonizadas que acompañan a reglamentos de producto (baterías, maquinaria, IA, ecodiseño); AG-B03 Estructura y Competencia: barreras técnicas de entrada.
- **Origen:** Alta F9_comp (2026-11-03).
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-03 (búsqueda web: «ISO Online Browsing Platform standards catalogue CEN-CENELEC standards search ETSI standards free download»; WebFetch: sí, guía «Finding standards» de KAN como página índice)

#### MBF-0234 · Q 79 (B) — Epoch AI — Data on AI Models (Notable AI Models y base de datos de modelos)

- **Canal oficial (URL raíz):** https://epoch.ai/data/epochdb (anuncio del data hub: https://epoch.ai/blog/announcing-epoch-ai-data-hub)
- **Emisor:** Epoch AI (instituto de investigación sin ánimo de lucro)
- **Documentación y notas:** Base de más de 3.700 modelos de aprendizaje automático con cómputo de entrenamiento (FLOP), parámetros, tamaño de datos, coste de entrenamiento (USD de 2023), duración y potencia; CSV de «Notable AI Models» actualizado el 31/10/2026; página actualizada el 02/11/2026.
- **Temática:** TFB-09 Patentes, innovación y tecnología (principal)
- **Calidad Q:** 79 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 12/15 · Independencia 9/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** secundaria (base compilada)
- **Acceso:** Abierto (CC BY 4.0); CSV y ZIP descargables
- **Ámbitos:** Escalado de la IA: cómputo, parámetros, costes y organizaciones
- **Motivo de inclusión y uso:** Mide la demanda de cómputo de la IA, motor de semiconductores, centros de datos y energía.
- **Uso en el bloque:** AG-B06 Tecnología y AG-B04 Demanda y Adopción (demanda de cómputo); Motor AG-B16 (tendencias de escalado); AG-B13 Prospectiva.
- **Restricciones de uso:** CC BY 4.0: citar fuente y autores.
- **Sesgos y cautelas:** Muchos valores estimados (empresas no publican cómputo); criterio propio de «notable».
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-03 (búsqueda web: «Epoch AI data hub notable AI models database training compute»; WebFetch: sí)
- **Origen:** Alta F9 Bloque B (2026-11-03).

#### MBF-0221 · Q 77 (B) — Google Patents

- **Canal oficial (URL raíz):** https://patents.google.com/ (según la guía índice https://research.lib.buffalo.edu/patents/patent-databases)
- **Emisor:** Google LLC
- **Documentación y notas:** Más de 120 millones de publicaciones de más de 100 oficinas de patentes; traducción automática al inglés de documentos sin texto completo en inglés; enlaza literatura (Google Scholar) y documentos citados.
- **Temática:** TFB-09 Patentes, innovación y tecnología (principal)
- **Calidad Q:** 77 (B) — Primariedad 17/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 12/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** secundaria (agregador de documentos oficiales)
- **Acceso:** Abierto
- **Ámbitos:** Búsqueda de texto completo de patentes mundiales
- **Motivo de inclusión y uso:** Búsqueda rápida en lenguaje natural y lectura de patentes traducidas.
- **Uso en el bloque:** AG-B06 Tecnología y AG-B12 (comprobación ágil de patentes de candidatos); los datos de estado legal se confirman en la oficina.
- **Restricciones de uso:** Términos de servicio de Google; sin API oficial de descarga masiva (existe conjunto público en BigQuery).
- **Sesgos y cautelas:** Traducción automática; estado legal no siempre actualizado.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-03 (búsqueda web: «free patent databases Espacenet PATENTSCOPE Google Patents Lens.org PatentsView research guide»; WebFetch: sí, sobre la guía índice)
- **Origen:** Alta F9 Bloque B (2026-11-03).

#### MBF-0232 · Q 76 (B) — GitHub — Innovation Graph (estadísticas de desarrollo de software por economía)

- **Canal oficial (URL raíz):** https://innovationgraph.github.com/ · Balance anual: https://github.blog/news-insights/policy-news-and-insights/year-recap-and-future-goals-for-the-github-innovation-graph/ (28/01/2026)
- **Emisor:** GitHub (Microsoft)
- **Documentación y notas:** Fuente estable y actualizada de estadísticas agregadas de actividad pública de desarrollo de software por economía: git pushes, repositorios, desarrolladores, organizaciones, lenguajes y colaboraciones entre economías; publicaciones trimestrales (datos hasta Q3 2025 en el balance; actualización Q1 2026 anunciada).
- **Temática:** TFB-09 Patentes, innovación y tecnología (principal) · secundarias: TFB-01
- **Calidad Q:** 76 (B) — Primariedad 17/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 12/15 · Independencia 7/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria (datos de plataforma)
- **Acceso:** Abierto
- **Ámbitos:** Actividad de software abierto por país, lenguaje y tema
- **Motivo de inclusión y uso:** Indicador de capacidad digital de mercados geográficos y de adopción de lenguajes y herramientas.
- **Uso en el bloque:** AG-B06 Tecnología y AG-B04 Demanda y Adopción (adopción de herramientas de desarrollo y de IA); AG-B08 para mercados geográficos.
- **Restricciones de uso:** Licencia del repositorio de datos (comprobar; la nota leída no la indica).
- **Sesgos y cautelas:** Solo actividad pública en GitHub; plataforma propiedad de Microsoft (conflicto en temas de IA para desarrolladores).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-03 (búsqueda web: «GitHub Innovation Graph data Octoverse 2025 report developers repositories»; WebFetch: sí)
- **Origen:** Alta F9 Bloque B (2026-11-03).

#### MBF-0226 · Q 75 (B) — CNIPA — Administración Nacional de Propiedad Intelectual de China (consulta de patentes)

- **Canal oficial (URL raíz):** https://english.cnipa.gov.cn/ (según la guía índice https://research.lib.buffalo.edu/patents/patent-databases, que enlaza el China Patent Inquiry System)
- **Emisor:** China National Intellectual Property Administration (CNIPA)
- **Documentación y notas:** Sitio oficial con estadísticas anuales y acceso al sistema de consulta de patentes de China, la mayor oficina del mundo por volumen de solicitudes.
- **Temática:** TFB-09 Patentes, innovación y tecnología (principal) · secundarias: TFB-07
- **Calidad Q:** 75 (B) — Primariedad 20/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 14/15 · Independencia 7/10 · Actualidad 9/10 · Acceso 6/10
- **Tipología:** primaria
- **Acceso:** Abierto (interfaz parcial en inglés)
- **Ámbitos:** Patentes y estadísticas de PI de China
- **Motivo de inclusión y uso:** Imprescindible para medir la actividad tecnológica china (baterías, solar, telecomunicaciones, IA).
- **Uso en el bloque:** AG-B06 Tecnología y AG-B07 Regulación y Geopolítica (competencia tecnológica con China).
- **Restricciones de uso:** Condiciones del sitio; buena parte solo en chino.
- **Sesgos y cautelas:** Incentivos administrativos históricos a solicitar patentes de baja calidad; interfaz inestable.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-03 (búsqueda web: «free patent databases Espacenet PATENTSCOPE Google Patents Lens.org PatentsView research guide»; WebFetch: sí, sobre la guía índice)
- **Origen:** Alta F9 Bloque B (2026-11-03).

#### MBF-0233 · Q 71 (B) — GitHub — Octoverse (informe anual)

- **Canal oficial (URL raíz):** https://github.blog/2025-10-28-octoverse-a-new-developer-joins-github-every-second-as-ai-leads-typescript-to-1/
- **Emisor:** GitHub (Microsoft)
- **Documentación y notas:** Informe anual sobre la actividad en GitHub; la edición del 28/10/2025 destaca que se une un desarrollador por segundo y que, impulsado por la IA, TypeScript pasa a ser el lenguaje n.º 1.
- **Temática:** TFB-09 Patentes, innovación y tecnología (principal)
- **Calidad Q:** 71 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 12/15 · Independencia 6/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria (datos de plataforma) con interpretación corporativa
- **Acceso:** Abierto
- **Ámbitos:** Desarrolladores, lenguajes, adopción de IA en programación, código abierto
- **Motivo de inclusión y uso:** Medida anual de adopción de herramientas de IA para programar y de crecimiento de desarrolladores por región.
- **Uso en el bloque:** AG-B04 Demanda y Adopción (IA generativa en software) y AG-B06.
- **Restricciones de uso:** Uso con atribución.
- **Sesgos y cautelas:** Informe corporativo con interés comercial (Copilot); métricas propias.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-03 (búsqueda web: «GitHub Innovation Graph data Octoverse 2025 report developers repositories»; WebFetch: no)
- **Origen:** Alta F9 Bloque B (2026-11-03).

#### MBF-0235 · Q 63 (C) — Hugging Face — Trending Papers (sucesor de Papers with Code)

- **Canal oficial (URL raíz):** huggingface.co (según la noticia índice) · Noticia leída: https://hyper.ai/en/news/42900
- **Emisor:** Hugging Face (con Meta y el equipo de Papers with Code)
- **Documentación y notas:** Papers with Code (Meta) se cerró el 24/07/2025 tras caídas a comienzos de julio; el 25/07/2025 Hugging Face anunció «Trending Papers», que sigue los artículos populares y los enlaza con su código en GitHub, pero sin las clasificaciones SOTA (leaderboards) de su predecesor.
- **Temática:** TFB-09 Patentes, innovación y tecnología (principal) · secundarias: TFB-18
- **Calidad Q:** 63 (C) — Primariedad 10/20 · Historial 10/20 · Transparencia 7/15 · Autoridad 9/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** secundaria (agregador)
- **Acceso:** Abierto
- **Ámbitos:** Artículos de IA con código, tendencias de investigación aplicada
- **Motivo de inclusión y uso:** Termómetro de qué técnicas de IA ganan tracción práctica (artículos con código).
- **Uso en el bloque:** AG-B06 Tecnología y AG-B13 Prospectiva; no sustituye a arXiv (MBF-0236).
- **Restricciones de uso:** Términos de Hugging Face.
- **Sesgos y cautelas:** Popularidad no equivale a relevancia; sin leaderboards; las referencias antiguas a paperswithcode.com están rotas o redirigidas.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Julio de 2025: cierre de Papers with Code y sustitución por Trending Papers.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-03 (búsqueda web: «Papers with Code shut down Hugging Face trending papers Epoch AI data on notable AI models»; WebFetch: sí, sobre la noticia de hyper.ai)
- **Origen:** Alta F9 Bloque B (2026-11-03).

## TFB-10 Prensa económica y especializada sectorial

#### RF-0222 · Q 79 (B) — Associated Press (AP)

- **Canal oficial (URL raíz):** https://apnews.com/ (noticias) · https://www.ap.org/ (corporativo) (según Wikipedia)
- **Emisor:** The Associated Press (cooperativa sin ánimo de lucro, Nueva York, fundada en 1846)
- **Temática:** TFB-10 Prensa económica y especializada sectorial (principal) · secundarias: —
- **Calidad Q:** 79 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 13/15 · Independencia 9/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** primaria (reporterismo de agencia)
- **Acceso:** Abierto (apnews.com)
- **Ámbitos:** Noticias generales, económicas y políticas de EE. UU. y el mundo
- **Motivo de inclusión y uso:** Agencia cooperativa de alcance mundial con acceso abierto; segunda raíz independiente frente a Reuters para corroborar hechos de actualidad. Uso: hechos de actualidad, a confirmar con la fuente oficial.
- **Uso en el bloque:** Todos los especialistas de P2: confirmación rápida de hechos de actualidad (agencia de noticias de alcance mundial).
- **Sesgos y cautelas:** Cobertura financiera menos profunda que la de agencias especializadas; las copias en otros medios son sindicadas (enlazar a la raíz).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «list of news agencies wikipedia» → artículo de Wikipedia «Associated Press»; WebFetch: sí, sobre Wikipedia)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 2).
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0029 · Q 72 (B) — Reuters

- **Canal oficial (URL raíz):** reuters.com (según Wikipedia) · Principios de confianza: https://thomsonreuters.com/en/about-us/trust-principles.html
- **Emisor:** Thomson Reuters (distribución profesional vía LSEG)
- **Temática:** TFB-10 Prensa económica y especializada sectorial (principal) · secundarias: —
- **Calidad Q:** 72 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 13/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 6/10
- **Tipología:** primaria
- **Acceso:** Muro parcial
- **Ámbitos:** Noticias de mercados, empresas, macro, materias primas
- **Motivo de inclusión y uso:** Agencia con reporterismo original (fundada en 1851) sujeta a los Trust Principles (integridad, independencia y ausencia de sesgo, desde 1941). Uso: primera fuente de hechos de actualidad.
- **Uso en el bloque:** Todos los especialistas de P2 (AG-B03…AG-B11): hechos de actualidad sobre empresas, sectores y materias primas; AG-B12 para noticias de candidatos (siempre contrastadas con la fuente primaria).
- **Sesgos y cautelas:** Titulares tempranos corregidos; verificar contra fuente oficial.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «list of news agencies wikipedia» → artículo de Wikipedia «Reuters»; «Reuters markets business news reuters.com Thomson Reuters Trust Principles»; WebFetch: sí, sobre Wikipedia y sobre los Trust Principles)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada en verificación de alta 2026-11-02 (tanda 2), por vía Wikipedia.
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0255 · Q 70 (B) — Reuters Breakingviews

- **Canal oficial (URL raíz):** https://www.breakingviews.com/ (página leída: https://breakingviews.com/?p=136)
- **Emisor:** Reuters News (Thomson Reuters), marca internacional de comentario financiero
- **Temática:** TFB-10 Prensa económica y especializada sectorial (principal) · secundarias: TFB-11
- **Calidad Q:** 70 (B) — Primariedad 10/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 13/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 7/10
- **Tipología:** secundaria (opinión firmada)
- **Acceso:** Suscripción (prueba gratuita); algunas columnas también en Reuters.com
- **Ámbitos:** Comentario en tiempo real sobre operaciones corporativas, valoraciones, mercados y economía; unos 36 columnistas en centros financieros
- **Motivo de inclusión y uso:** Opinión de referencia con cálculos explícitos (valoración, sinergias) sobre noticias corporativas. Uso: segunda lectura crítica de operaciones; nunca como prueba de hechos (regla F9 a).
- **Uso en el bloque:** AG-B09 y AG-B14 Contrarias: comentario breve y opinado sobre operaciones y valoraciones de empresas y sectores (opinión).
- **Sesgos y cautelas:** Comparte raíz con Reuters (RF-0029); no cuenta como fuente independiente de esta.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Reuters Breakingviews financial commentary»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 3).
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### MBF-0239 · Q 69 (B) — Industry Dive (Informa) — red de publicaciones sectoriales B2B

- **Canal oficial (URL raíz):** según Wikipedia: https://en.wikipedia.org/wiki/Industry_Dive
- **Emisor:** Industry Dive, propiedad mayoritaria de Informa plc desde 2022 (operada por Informa TechTarget)
- **Documentación y notas:** Fundada en 2012 en Washington D. C.; 36 cabeceras sectoriales con boletines diarios y semanales (Agriculture, Automotive, Banking, BioPharma, CFO, CIO, Construction, Cybersecurity, Food, Grocery, Healthcare, Manufacturing, MedTech, Packaging, Payments, Restaurant, Retail, Supply Chain, Trucking, Utility, Waste Dive, entre otras).
- **Temática:** TFB-10 Prensa económica y especializada sectorial (principal) · secundarias: TFB-04
- **Calidad Q:** 69 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 11/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** primaria (periodismo sectorial)
- **Acceso:** Abierto; boletines gratuitos con registro de correo
- **Ámbitos:** Noticias sectoriales de EE. UU. en una treintena de industrias
- **Motivo de inclusión y uso:** Cobertura homogénea y gratuita de muchos sectores; permite vigilar varios subsectores con un mismo estándar editorial.
- **Uso en el bloque:** AG-B03, AG-B04 y AG-B05 (vigilancia sectorial diaria de estructura, demanda y suministro); AG-B07 (regulación sectorial de EE. UU.).
- **Restricciones de uso:** Uso con atribución; contenidos patrocinados identificados como tales.
- **Sesgos y cautelas:** Centrada en EE. UU.; parte de los ingresos procede de marketing de contenidos para empresas del sector.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** 2022: compra por Informa a Falfurrias Capital Partners (unos 525 M$).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-03 (búsqueda web: «Industry Dive publications list Utility Dive BioPharma Dive Supply Chain Dive»; WebFetch: sí, sobre Wikipedia)
- **Origen:** Alta F9 Bloque B (2026-11-03).

#### MBF-0240 · Q 69 (B) — Utility Dive — prensa sectorial de electricidad y utilities

- **Canal oficial (URL raíz):** https://utilitydive.com/ (acerca de: https://utilitydive.com/about)
- **Emisor:** Industry Dive / Informa TechTarget
- **Documentación y notas:** Periodismo y análisis del sector eléctrico: generación, transporte y distribución, fiabilidad de red, electrificación, gestión de carga, renovables, almacenamiento, recursos distribuidos y regulación; boletines gratuitos Daily Dive, Storage Weekly, Load Management Weekly y Renewable Energy Weekly.
- **Temática:** TFB-10 Prensa económica y especializada sectorial (principal) · secundarias: TFB-12
- **Calidad Q:** 69 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 11/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** primaria (periodismo sectorial)
- **Acceso:** Abierto; boletines gratuitos
- **Ámbitos:** Utilities, redes, renovables y almacenamiento (EE. UU.)
- **Motivo de inclusión y uso:** Seguimiento diario de regulación (FERC, comisiones estatales), interconexión y demanda eléctrica (centros de datos).
- **Uso en el bloque:** AG-B04 (demanda eléctrica y de centros de datos), AG-B05 (colas de interconexión, equipos) y AG-B07 (regulación) para utilities y renovables.
- **Restricciones de uso:** Uso con atribución.
- **Sesgos y cautelas:** Boletines temáticos patrocinados; foco en EE. UU.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-03 (búsqueda web: «Industry Dive publications list Utility Dive BioPharma Dive Supply Chain Dive»; WebFetch: sí)
- **Origen:** Alta F9 Bloque B (2026-11-03).

#### MBF-0241 · Q 69 (B) — BioPharma Dive — prensa sectorial de biotecnología y farmacia

- **Canal oficial (URL raíz):** https://biopharmadive.com/ (acerca de: https://biopharmadive.com/about/)
- **Emisor:** Industry Dive / Informa TechTarget
- **Documentación y notas:** Resultados de ensayos clínicos, aprobaciones de la FDA, terapia génica, precios de medicamentos, fusiones y alianzas; boletines gratuitos Daily Dive, Commercialization Weekly, Emerging Biotech Weekly y Gene Therapy Weekly.
- **Temática:** TFB-10 Prensa económica y especializada sectorial (principal)
- **Calidad Q:** 69 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 11/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** primaria (periodismo sectorial)
- **Acceso:** Abierto; boletines gratuitos
- **Ámbitos:** Biotecnología y farmacia: ensayos, regulación, operaciones
- **Motivo de inclusión y uso:** Catalizadores clínicos y regulatorios de candidatos del sector salud.
- **Uso en el bloque:** AG-B06 (cartera de I+D y ensayos), AG-B07 (FDA y precios de medicamentos) y AG-B12 (catalizadores de candidatos biotecnológicos).
- **Restricciones de uso:** Uso con atribución.
- **Sesgos y cautelas:** Comunicados de empresa como fuente frecuente; confirmar en ClinicalTrials.gov o FDA.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-03 (búsqueda web: «Industry Dive publications list Utility Dive BioPharma Dive Supply Chain Dive»; WebFetch: sí)
- **Origen:** Alta F9 Bloque B (2026-11-03).

#### MBF-0242 · Q 69 (B) — Supply Chain Dive — prensa sectorial de logística y cadenas de suministro

- **Canal oficial (URL raíz):** https://supplychaindive.com/ (acerca de: https://supplychaindive.com/about)
- **Emisor:** Industry Dive / Informa TechTarget
- **Documentación y notas:** Gestión de la cadena de suministro: riesgo, tecnología, operaciones, compras, logística, fletes y regulación; boletines gratuitos Daily Dive, Operations Weekly, Logistics Weekly y Procurement Weekly.
- **Temática:** TFB-10 Prensa económica y especializada sectorial (principal) · secundarias: TFB-05
- **Calidad Q:** 69 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 11/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** primaria (periodismo sectorial)
- **Acceso:** Abierto; boletines gratuitos
- **Ámbitos:** Logística, compras, aranceles, relocalización
- **Motivo de inclusión y uso:** Señales tempranas de cuellos de botella, relocalización y cambios de proveedores.
- **Uso en el bloque:** AG-B05 Oferta y Cadena de Suministro y AG-B07 (aranceles y regulación comercial).
- **Restricciones de uso:** Uso con atribución.
- **Sesgos y cautelas:** Foco en EE. UU.; anecdotario de empresas.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-03 (búsqueda web: «Industry Dive publications list Utility Dive BioPharma Dive Supply Chain Dive»; WebFetch: sí)
- **Origen:** Alta F9 Bloque B (2026-11-03).

#### RF-0030 · Q 69 (B) — Financial Times

- **Canal oficial (URL raíz):** www.ft.com (según Wikipedia)
- **Emisor:** The Financial Times Ltd. (propiedad de Nikkei Inc.)
- **Temática:** TFB-10 Prensa económica y especializada sectorial (principal) · secundarias: —
- **Calidad Q:** 69 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 13/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 4/10
- **Tipología:** primaria y secundaria (opinión)
- **Acceso:** Suscripción (muro de pago medido desde 2007)
- **Ámbitos:** Mercados globales, empresas, política económica; columnas de opinión
- **Motivo de inclusión y uso:** Prensa financiera de referencia con reporterismo propio (fundada en 1888, Londres). Uso: hechos y contexto de mercados globales; columnas como opinión.
- **Uso en el bloque:** AG-B03 Estructura y Competencia, AG-B07 Regulación y Geopolítica y AG-B09: información y análisis de empresas y sectores globales; Lex como opinión, nunca como hecho.
- **Sesgos y cautelas:** Muro de pago; separar noticia de columna de opinión.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «list of financial newspapers wikipedia business newspapers» → artículo de Wikipedia «Financial Times»; WebFetch: sí, sobre Wikipedia)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada en verificación de alta 2026-11-02 (tanda 2), por vía Wikipedia.
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0223 · Q 69 (B) — Dow Jones Newswires

- **Canal oficial (URL raíz):** dowjones.com (sitio oficial de Dow Jones & Company según Wikipedia)
- **Emisor:** Dow Jones & Company (News Corp)
- **Temática:** TFB-10 Prensa económica y especializada sectorial (principal) · secundarias: —
- **Calidad Q:** 69 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 13/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 3/10
- **Tipología:** primaria (agencia de noticias financieras en tiempo real, desde 1882)
- **Acceso:** Suscripción profesional (terminales y Factiva)
- **Ámbitos:** Noticias financieras en tiempo real: empresas, mercados, materias primas, renta fija
- **Motivo de inclusión y uso:** Agencia financiera en tiempo real del grupo editor de The Wall Street Journal, Barron's y MarketWatch. Uso: hechos de última hora cuando se accede por licencia; para citar, preferir la versión publicada en WSJ o la fuente primaria.
- **Uso en el bloque:** AG-B09 y AG-B12: flujo de noticias corporativas y de resultados en tiempo real (vía terceros); AG-B10.
- **Sesgos y cautelas:** Acceso restringido; misma raíz que RF-0032 (no cuentan como fuentes independientes entre sí).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «wsj.com markets The Wall Street Journal Dow Jones» → artículo de Wikipedia «Dow Jones & Company»; WebFetch: sí, sobre Wikipedia)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 2).
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0031 · Q 68 (B) — Bloomberg News

- **Canal oficial (URL raíz):** https://www.bloomberg.com/ (ejemplo de programa Bloomberg Markets: https://www.bloomberg.com/news/videos/2026-03-26/bloomberg-markets-3-26-2026-video)
- **Emisor:** Bloomberg L.P.
- **Temática:** TFB-10 Prensa económica y especializada sectorial (principal) · secundarias: —
- **Calidad Q:** 68 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 13/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 4/10
- **Tipología:** primaria (reporterismo propio) y secundaria (opinión)
- **Acceso:** Muro de pago (artículos); vídeos y resúmenes parcialmente abiertos
- **Ámbitos:** Noticias de mercados, empresas, macro y política económica; programas de vídeo
- **Motivo de inclusión y uso:** Reporterismo financiero de alta velocidad con fuentes propias. Uso: hechos de actualidad a corroborar con la fuente primaria; las piezas de Bloomberg Opinion se tratan como opinión.
- **Uso en el bloque:** AG-B03, AG-B05 y AG-B09: noticias de empresas, operaciones corporativas y cadenas de suministro; AG-B10 para flujos y mercado.
- **Sesgos y cautelas:** Propiedad vinculada al negocio de terminales; distinguir noticia y opinión; muro de pago limita la citación pública.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Bloomberg News markets bloomberg.com/markets»; WebFetch: sí, página de vídeo cargada con resumen; artículo completo no comprobado)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada en verificación de alta 2026-11-02.
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0032 · Q 68 (B) — The Wall Street Journal

- **Canal oficial (URL raíz):** wsj.com (según Wikipedia)
- **Emisor:** Dow Jones & Company (News Corp)
- **Temática:** TFB-10 Prensa económica y especializada sectorial (principal) · secundarias: —
- **Calidad Q:** 68 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 13/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 4/10
- **Tipología:** primaria y secundaria (opinión)
- **Acceso:** Suscripción
- **Ámbitos:** Mercados y empresas de EE. UU.
- **Motivo de inclusión y uso:** Reporterismo original de referencia en EE. UU. (fundado en 1889, Nueva York).
- **Uso en el bloque:** AG-B03 y AG-B09: noticias corporativas y sectoriales de EE. UU.; Heard on the Street como opinión.
- **Sesgos y cautelas:** Muro de pago; página editorial con línea de opinión diferenciada; misma raíz que Dow Jones Newswires (RF-0223).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «list of financial newspapers wikipedia business newspapers» → artículo de Wikipedia «The Wall Street Journal»; WebFetch: sí, sobre Wikipedia)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada en verificación de alta 2026-11-02 (tanda 2), por vía Wikipedia.
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0254 · Q 68 (B) — Nikkei Asia

- **Canal oficial (URL raíz):** https://asia.nikkei.com/ (presentación del medio: https://info.asia.nikkei.com/about · anuncio de cambio de nombre: https://asia.nikkei.com/announcements/nikkei-to-rename-flagship-english-publication-nikkei-asia)
- **Emisor:** Nikkei Inc. (grupo propietario también de The Nikkei, del índice Nikkei 225 y del Financial Times)
- **Temática:** TFB-10 Prensa económica y especializada sectorial (principal) · secundarias: —
- **Calidad Q:** 68 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 13/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 5/10
- **Tipología:** primaria (reporterismo propio) y secundaria
- **Acceso:** Suscripción (no se ha confirmado el detalle del muro de pago)
- **Ámbitos:** Empresas, economía, política y mercados de Asia; entrevistas; lista Asia300
- **Motivo de inclusión y uso:** Principal medio económico en inglés centrado en Asia, con reporterismo propio en Japón, China y el Sudeste Asiático. Uso: hechos y contexto de empresas y mercados asiáticos.
- **Uso en el bloque:** AG-B03, AG-B05 y AG-B06: empresas y cadenas de suministro asiáticas (semiconductores, automoción, electrónica); AG-B07 para geopolítica regional.
- **Sesgos y cautelas:** Mismo grupo propietario que el FT (RF-0030): artículos compartidos no son raíces independientes.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Nikkei Asia business news asia.nikkei.com»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 3).
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### MBF-0243 · Q 66 (B) — Automotive Dive — prensa sectorial del automóvil

- **Canal oficial (URL raíz):** https://automotivedive.com/ (acerca de: https://automotivedive.com/about)
- **Emisor:** Industry Dive / Informa TechTarget
- **Documentación y notas:** Cabecera de la red Industry Dive dedicada a fabricantes, proveedores, vehículo eléctrico y tecnología del automóvil (listada en Wikipedia «Industry Dive»).
- **Temática:** TFB-10 Prensa económica y especializada sectorial (principal)
- **Calidad Q:** 66 (B) — Primariedad 11/20 · Historial 10/20 · Transparencia 8/15 · Autoridad 10/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** primaria (periodismo sectorial)
- **Acceso:** Abierto; boletines gratuitos
- **Ámbitos:** Automoción, vehículo eléctrico, proveedores
- **Motivo de inclusión y uso:** Actualidad de fabricantes y proveedores (EE. UU.) complementaria de las estadísticas de asociaciones (TFB-04).
- **Uso en el bloque:** AG-B03, AG-B04 (adopción del VE) y AG-B05 (proveedores y baterías).
- **Restricciones de uso:** Uso con atribución.
- **Sesgos y cautelas:** Foco en EE. UU.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-03 (búsqueda web: «Industry Dive publications list Utility Dive BioPharma Dive Supply Chain Dive»; WebFetch: no, cabecera confirmada en Wikipedia «Industry Dive»)
- **Origen:** Alta F9 Bloque B (2026-11-03).

#### MBF-0244 · Q 66 (B) — MedTech Dive — prensa sectorial de tecnología médica

- **Canal oficial (URL raíz):** https://www.medtechdive.com/ (acerca de: https://www.medtechdive.com/about/)
- **Emisor:** Industry Dive / Informa TechTarget
- **Documentación y notas:** Cabecera de la red Industry Dive sobre dispositivos médicos, diagnóstico y regulación (listada en Wikipedia «Industry Dive»).
- **Temática:** TFB-10 Prensa económica y especializada sectorial (principal)
- **Calidad Q:** 66 (B) — Primariedad 11/20 · Historial 10/20 · Transparencia 8/15 · Autoridad 10/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** primaria (periodismo sectorial)
- **Acceso:** Abierto; boletines gratuitos
- **Ámbitos:** Tecnología sanitaria: aprobaciones, retiradas, operaciones
- **Motivo de inclusión y uso:** Catalizadores regulatorios y competitivos del subsector de dispositivos médicos.
- **Uso en el bloque:** AG-B03, AG-B07 (FDA) y AG-B12 (candidatos de tecnología médica).
- **Restricciones de uso:** Uso con atribución.
- **Sesgos y cautelas:** Foco en EE. UU.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-03 (búsqueda web: «Industry Dive publications list Utility Dive BioPharma Dive Supply Chain Dive»; WebFetch: no, cabecera confirmada en Wikipedia «Industry Dive»)
- **Origen:** Alta F9 Bloque B (2026-11-03).

#### RF-0034 · Q 66 (B) — Expansión

- **Canal oficial (URL raíz):** expansion.com (según Wikipedia)
- **Emisor:** Unidad Editorial (controlada por RCS MediaGroup)
- **Temática:** TFB-10 Prensa económica y especializada sectorial (principal) · secundarias: —
- **Calidad Q:** 66 (B) — Primariedad 13/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 11/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 6/10
- **Tipología:** primaria y secundaria
- **Acceso:** Muro parcial
- **Ámbitos:** Mercados y empresas españolas
- **Motivo de inclusión y uso:** Prensa económica española de referencia (fundada en 1986, Madrid).
- **Uso en el bloque:** AG-B03 y AG-B12: actualidad de empresas cotizadas y sectores en España; AG-B07 para regulación española.
- **Sesgos y cautelas:** Muro parcial; cobertura nacional; Wikipedia da datos de propiedad no coincidentes (infobox: Grupo Recoletos; texto: Unidad Editorial/RCS).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «expansion.com mercados diario Expansión Unidad Editorial» → artículo de Wikipedia «Expansión (Spanish newspaper)»; WebFetch: sí, sobre Wikipedia)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada en verificación de alta 2026-11-02 (tanda 2), por vía Wikipedia.
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0035 · Q 66 (B) — Cinco Días

- **Canal oficial (URL raíz):** cincodias.elpais.com (según Wikipedia: https://en.wikipedia.org/wiki/Cinco_D%C3%ADas)
- **Emisor:** PRISA (editado por su filial Estructura)
- **Documentación y notas:** Diario económico fundado en marzo de 1978 (el más antiguo de España en su género), propiedad de PRISA desde 1989; tabloide de lunes a viernes con sección de artículos de The Wall Street Journal y suplementos; directora: Amanda Mars (desde 2022); sede en Madrid.
- **Temática:** TFB-10 Prensa económica y especializada sectorial (principal) · secundarias: —
- **Calidad Q:** 66 (B) — Primariedad 13/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 11/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 6/10
- **Tipología:** primaria
- **Acceso:** Muro parcial
- **Ámbitos:** Mercados y empresas españolas, sectores regulados (energía, banca, telecomunicaciones)
- **Motivo de inclusión y uso:** Prensa económica española de referencia.
- **Uso en el bloque:** AG-B03 y AG-B12: actualidad de empresas y sectores en España (tercera fuente española junto a RF-0034 y RF-0256); AG-B07 para regulación sectorial española.
- **Restricciones de uso:** Muro de pago parcial; citar pieza y fecha.
- **Sesgos y cautelas:** Muro parcial; cobertura nacional; línea editorial del grupo.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-03 (búsqueda web: «Cinco Días diario económico PRISA Wikipedia»; WebFetch: sí, sobre el artículo de Wikipedia)
- **Origen:** Semilla V3.0 (2026-11-01) del Bloque A, confirmada en la verificación del Bloque B (2026-11-03) por vía Wikipedia; conserva su ID.

#### MBF-0245 · Q 64 (C) — CIO Dive — prensa sectorial de tecnología empresarial

- **Canal oficial (URL raíz):** https://ciodive.com/ (acerca de: https://ciodive.com/about)
- **Emisor:** Industry Dive / Informa TechTarget
- **Documentación y notas:** Cabecera de la red Industry Dive sobre gasto y estrategia tecnológica de las empresas (nube, IA, software), listada en Wikipedia «Industry Dive».
- **Temática:** TFB-10 Prensa económica y especializada sectorial (principal) · secundarias: TFB-09
- **Calidad Q:** 64 (C) — Primariedad 10/20 · Historial 10/20 · Transparencia 8/15 · Autoridad 10/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** primaria (periodismo sectorial)
- **Acceso:** Abierto; boletines gratuitos
- **Ámbitos:** Gasto en TI, adopción de IA y nube en empresas
- **Motivo de inclusión y uso:** Señales de adopción empresarial de IA y software.
- **Uso en el bloque:** AG-B04 Demanda y Adopción y AG-B06 Tecnología.
- **Restricciones de uso:** Uso con atribución.
- **Sesgos y cautelas:** Encuestas de terceros con muestras pequeñas; contenido patrocinado.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-03 (búsqueda web: «Industry Dive publications list Utility Dive BioPharma Dive Supply Chain Dive»; WebFetch: no, cabecera confirmada en Wikipedia «Industry Dive»)
- **Origen:** Alta F9 Bloque B (2026-11-03).

#### RF-0033 · Q 64 (C) — The Economist

- **Canal oficial (URL raíz):** www.economist.com (según Wikipedia)
- **Emisor:** The Economist Group (The Economist Newspaper Limited)
- **Temática:** TFB-10 Prensa económica y especializada sectorial (principal) · secundarias: TFB-11
- **Calidad Q:** 64 (C) — Primariedad 12/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 13/15 · Independencia 8/10 · Actualidad 8/10 · Acceso 4/10
- **Tipología:** secundaria (análisis y opinión)
- **Acceso:** Suscripción
- **Ámbitos:** Análisis económico y geopolítico semanal
- **Motivo de inclusión y uso:** Síntesis analítica de tendencias globales (desde 1843); útil para narrativas y consenso.
- **Uso en el bloque:** AG-B08 Macro y Ciclo, AG-B07 y AG-B13 Prospectiva: análisis de fondo de industrias y temas (informes especiales); opinión, no prueba.
- **Sesgos y cautelas:** Línea editorial liberal explícita; artículos sin firma («voz colectiva»).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «list of financial newspapers wikipedia business newspapers» → artículo de Wikipedia «The Economist»; WebFetch: sí, sobre Wikipedia)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada en verificación de alta 2026-11-02 (tanda 2), por vía Wikipedia.
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0224 · Q 64 (C) — finews.com / finews.ch

- **Canal oficial (URL raíz):** https://www.finews.com/ (edición en inglés; ejemplo leído: https://www.finews.com/news/english-news/23784-guide-to-the-markets-jpm-asset-management)
- **Emisor:** Finews AG (Suiza)
- **Temática:** TFB-10 Prensa económica y especializada sectorial (principal) · secundarias: —
- **Calidad Q:** 64 (C) — Primariedad 11/20 · Historial 10/20 · Transparencia 8/15 · Autoridad 10/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 8/10
- **Tipología:** secundaria especializada
- **Acceso:** Abierto (alertas gratuitas por correo)
- **Ámbitos:** Banca privada y gestión de patrimonios en Suiza; nombramientos, fintech; ediciones en alemán e inglés y finews.asia
- **Motivo de inclusión y uso:** Actualidad del centro financiero suizo (UBS, banca privada, gestoras). Uso: vigilancia de la industria suiza de gestión de patrimonios.
- **Uso en el bloque:** AG-B03 (subsector de banca privada y gestión de patrimonios): actualidad del sector financiero suizo y asiático.
- **Sesgos y cautelas:** Medio pequeño centrado en la industria; contraste con fuentes primarias.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «am.jpmorgan.com Guide to the Markets quarterly US»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 2).
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0256 · Q 63 (C) — elEconomista.es

- **Canal oficial (URL raíz):** https://www.eleconomista.es/ (mercados: https://www.eleconomista.es/mercados-cotizaciones/)
- **Emisor:** Editorial Ecoprensa, S.A.
- **Temática:** TFB-10 Prensa económica y especializada sectorial (principal) · secundarias: —
- **Calidad Q:** 63 (C) — Primariedad 12/20 · Historial 10/20 · Transparencia 8/15 · Autoridad 10/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 6/10
- **Tipología:** primaria y secundaria
- **Acceso:** Muro parcial (no confirmado en la página leída)
- **Ámbitos:** Mercados y empresas españolas; índice propio Eco10 (difundido también en Bloomberg y Reuters con el código eco10p)
- **Motivo de inclusión y uso:** Tercera cabecera económica española, independiente de Expansión (RF-0034) y de Cinco Días. Uso: corroboración de actualidad española entre raíces distintas.
- **Uso en el bloque:** AG-B03 y AG-B12: actualidad de empresas y sectores en España (segunda fuente española para corroboración).
- **Sesgos y cautelas:** Cobertura nacional; el índice Eco10 es un producto editorial, no una referencia oficial.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «elEconomista.es diario económico mercados»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 3).
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0326 · Q 61 (C) — gCaptain — noticias marítimas

- **Canal oficial (URL raíz):** https://gcaptain.com/tag/baltic-dry-index
- **Emisor:** gCaptain
- **Documentación y notas:** Medio de noticias marítimas y offshore; etiqueta del Baltic Dry Index con artículos (último visto: 07/05/2026).
- **Temática:** TFB-10 Prensa económica y especializada sectorial (principal) · secundarias: TFB-05
- **Calidad Q:** 61 (C) — Primariedad 9/20 · Historial 10/20 · Transparencia 7/15 · Autoridad 9/15 · Independencia 7/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** secundaria
- **Acceso:** Abierto
- **Ámbitos:** Transporte marítimo, fletes, puertos
- **Motivo de inclusión y uso:** Contexto de noticias del sector naval; los datos se citan en RF-0322 o RF-0323.
- **Uso en el bloque:** AG-B05 Oferta y Cadena de Suministro: incidencias del transporte marítimo, puertos y flota (prensa sectorial naval); AG-B11 para riesgos operativos.
- **Restricciones de uso:** Opinión/noticia: los hechos se citan en su fuente primaria.
- **Sesgos y cautelas:** Entidad editora no declarada en la página leída.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin datos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «balticexchange.com Baltic Dry Index dry bulk freight indices»; WebFetch: sí)
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0204 · Q 60 (C) — Funds Society

- **Canal oficial (URL raíz):** https://www.fundssociety.com/ (edición en español: https://www.fundssociety.com/es/)
- **Emisor:** Funds Society (editor de medios para la industria de gestión de activos y patrimonios)
- **Temática:** TFB-10 Prensa económica y especializada sectorial (principal) · secundarias: TFB-08
- **Calidad Q:** 60 (C) — Primariedad 10/20 · Historial 10/20 · Transparencia 7/15 · Autoridad 9/15 · Independencia 6/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** secundaria especializada
- **Acceso:** Abierto
- **Ámbitos:** Industria de fondos y banca privada: negocio, regulación, ETF, nombramientos, alternativos, pensiones; ediciones España, internacional, offshore, LATAM y Brasil
- **Motivo de inclusión y uso:** Actualidad del sector gestor en español (lanzamientos, cambios de gestores, flujos comentados). Uso: vigilancia de gestoras y productos (TF-04) y señales de industria.
- **Uso en el bloque:** AG-B03 (subsector de gestión de activos): actualidad de gestoras, fondos y lanzamientos en España, Latinoamérica y EE. UU. offshore.
- **Sesgos y cautelas:** Modelo de negocio basado en eventos y relación con gestoras (riesgo de contenido patrocinado); propiedad no declarada en la página consultada.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «site:expansion.com mercados»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1).
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0259 · Q 57 (C) — Investment Week

- **Canal oficial (URL raíz):** https://www.investmentweek.co.uk/
- **Emisor:** Incisive Business Media Limited (red Arc de Incisive Media)
- **Temática:** TFB-10 Prensa económica y especializada sectorial (principal) · secundarias: TFB-08
- **Calidad Q:** 57 (C) — Primariedad 10/20 · Historial 10/20 · Transparencia 7/15 · Autoridad 9/15 · Independencia 5/10 · Actualidad 9/10 · Acceso 7/10
- **Tipología:** secundaria especializada
- **Acceso:** Abierto con registro
- **Ámbitos:** Industria de fondos del Reino Unido: fondos, investment trusts, ETF, gestión de patrimonios, regulación
- **Motivo de inclusión y uso:** Actualidad de gestoras y fondos británicos (cambios de gestores, flujos, lanzamientos). Uso: vigilancia sectorial.
- **Uso en el bloque:** AG-B03 (subsector de gestión de activos) y AG-B12: actualidad del sector de fondos del Reino Unido y Europa.
- **Sesgos y cautelas:** Publica contenido patrocinado de gestoras («Partner Insight», «Industry Voice», rutas «/sponsored/»), p. ej., de PIMCO. Excluir ese contenido como evidencia.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «PIMCO secular outlook cyclical outlook insights pimco.com»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 3).
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

## TFB-11 Análisis de bancos, gestoras, consultoras y think tanks

#### RF-0241 · Q 81 (A) — UBS Global Investment Returns Yearbook (Dimson, Marsh y Staunton)

- **Canal oficial (URL raíz):** https://www.ubs.com/global/en/investment-bank/insights-and-data/articles/global-investment-returns-yearbook-2026.html (resumen público: https://www.ubs.com/content/dam/assets/wm/static/cio/documents/giry2026-summary-public.pdf)
- **Emisor:** UBS, con Elroy Dimson (Cambridge) y Paul Marsh y Mike Staunton (London Business School)
- **Temática:** TFB-11 Análisis de bancos, gestoras, consultoras y think tanks (principal) · secundarias: TFB-07
- **Calidad Q:** 81 (A) — Primariedad 17/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 8/10 · Actualidad 7/10 · Acceso 10/10
- **Tipología:** primaria (base de datos DMS propia) y secundaria
- **Acceso:** Resumen público en PDF; informe completo para clientes de UBS Investment Bank (UBS Neo)
- **Ámbitos:** Rentabilidades anuales de acciones, bonos, letras, inflación, divisas y, desde 2026, oro, en 35 mercados desde 1900 (126 años)
- **Motivo de inclusión y uso:** Referencia de rentabilidades y primas de riesgo de muy largo plazo. Uso: supuestos de largo plazo del Motor de Cálculo y contraste de narrativas.
- **Uso en el bloque:** AG-B09: rentabilidades históricas de largo plazo por país, clase de activo e industria; AG-B14 para contrastar narrativas sectoriales.
- **Sesgos y cautelas:** Informe completo restringido; el título HTML de la página decía «2025» aunque el contenido era de 2026.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «UBS Global Investment Returns Yearbook 2026 Dimson Marsh Staunton»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 3).
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0092 · Q 77 (B) — Peterson Institute for International Economics (PIIE)

- **Canal oficial (URL raíz):** https://www.piie.com/ (política de transparencia: https://www.piie.com/about/transparency-policy)
- **Emisor:** PIIE
- **Temática:** TFB-11 Análisis de bancos, gestoras, consultoras y think tanks (principal) · secundarias: TFB-05
- **Calidad Q:** 77 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 14/15 · Independencia 8/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** secundaria
- **Acceso:** Abierto
- **Ámbitos:** Comercio, finanzas internacionales, política macroeconómica
- **Motivo de inclusión y uso:** Análisis aplicado de economía internacional.
- **Uso en el bloque:** AG-B07 Regulación y Geopolítica: comercio, aranceles, política industrial y sanciones con impacto sectorial.
- **Sesgos y cautelas:** Unos 150 financiadores (empresas, fundaciones, particulares, instituciones públicas); el mayor donante histórico es la Peter G. Peterson Foundation. Publica sus fuentes de financiación cada año desde 2013 y exige a los autores declarar vínculos financieros.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «brookings.edu piie.com bruegel.org think tank economic policy research»; WebFetch: sí)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada por BFA en F9_S3 (2026-11-02). Q corregida de 76 a 77 por la transparencia de financiación.
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0093 · Q 76 (B) — Bruegel

- **Canal oficial (URL raíz):** https://www.bruegel.org/ (datos: https://www.bruegel.org/datasets)
- **Emisor:** Bruegel (fundado en 2005)
- **Temática:** TFB-11 Análisis de bancos, gestoras, consultoras y think tanks (principal) · secundarias: TFB-16
- **Calidad Q:** 76 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 13/15 · Independencia 8/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** secundaria (con bases de datos propias)
- **Acceso:** Abierto
- **Ámbitos:** Política económica europea, energía, comercio; bases de datos: importaciones y demanda de gas, tipos de cambio efectivos reales de 178 países, base de datos de China, seguimiento del comercio global, agregados monetarios Divisia del área del euro, seguimiento del ETS
- **Motivo de inclusión y uso:** Think tank europeo de referencia con bases de datos propias.
- **Uso en el bloque:** AG-B07: política de competencia, industrial y digital de la UE; AG-B03 para estructura de mercados europeos.
- **Sesgos y cautelas:** Miembros: gobiernos de la UE, empresas internacionales e instituciones, que participan en fijar las prioridades de investigación.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «brookings.edu piie.com bruegel.org think tank economic policy research»; WebFetch: sí, páginas «About» y «Datasets»)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada por BFA en F9_S3 (2026-11-02). Q corregida de 75 a 76 (primariedad por sus bases de datos).
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0438 · Q 76 (B) — Funcas

- **Canal oficial (URL raíz):** https://www.funcas.es/
- **Emisor:** Funcas (creada y mantenida por CECA)
- **Temática:** TFB-11 Análisis de bancos, gestoras, consultoras y think tanks (principal) · secundarias: TFB-02
- **Calidad Q:** 76 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 13/15 · Independencia 7/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** secundaria
- **Acceso:** Abierto
- **Ámbitos:** Coyuntura española y autonómica, Funcas Europe, encuestas sociales, notas técnicas, revistas y libros
- **Motivo de inclusión y uso:** Seguimiento de la economía española; consenso de previsiones. AC-MAC con foco España.
- **Uso en el bloque:** AG-B08 y AG-B04: previsiones y análisis sectorial de la economía española (panel de previsiones).
- **Sesgos y cautelas:** Vinculada al sector de cajas de ahorros (CECA).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Funcas Fedea CIDOB EsadeEcPol think tanks economía España»; WebFetch: sí, página «About us»)
- **Origen:** Alta F9_S3 (2026-11-02).
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0091 · Q 74 (B) — Brookings Institution

- **Canal oficial (URL raíz):** https://www.brookings.edu/
- **Emisor:** Brookings Institution (fundada en 1916)
- **Temática:** TFB-11 Análisis de bancos, gestoras, consultoras y think tanks (principal) · secundarias: —
- **Calidad Q:** 74 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 14/15 · Independencia 7/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** secundaria
- **Acceso:** Abierto
- **Ámbitos:** Política económica, fiscal y monetaria (Hutchins Center), geopolítica
- **Motivo de inclusión y uso:** Think tank de referencia en política económica de EE. UU.
- **Uso en el bloque:** AG-B07 y AG-B13: política económica, tecnológica y regulatoria de EE. UU.
- **Sesgos y cautelas:** Financiación privada y de gobiernos extranjeros con controversias documentadas (Qatar, 2014; Huawei, 2012-2018; dimisión de su presidente en 2022 por una investigación del FBI sobre presión a favor de Qatar).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Wikipedia list of think tanks»; WebFetch: sí, listado y artículo de Wikipedia; URL oficial confirmada en la ficha de Wikipedia leída con WebFetch a partir del listado devuelto por la búsqueda (lectura lateral); la web oficial no se cargó)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada por BFA en F9_S3 (2026-11-02). Q corregida de 76 a 74 (independencia 7/10 y transparencia 11/15 por las controversias de financiación).
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0205 · Q 74 (B) — CaixaBank Research

- **Canal oficial (URL raíz):** https://www.caixabankresearch.com/ (ejemplo, Financial Markets Daily Report: https://www.caixabankresearch.com/en/publications/financial-markets-daily-report/04-may-2020)
- **Emisor:** CaixaBank (servicio de estudios)
- **Temática:** TFB-11 Análisis de bancos, gestoras, consultoras y think tanks (principal) · secundarias: TFB-02
- **Calidad Q:** 74 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 12/15 · Independencia 6/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** secundaria cualificada (análisis de banco)
- **Acceso:** Abierto (ES, CA, EN; PDF descargables)
- **Ámbitos:** Economía española y portuguesa, mercados financieros, sectores, comunidades autónomas, consumo (Monitor de consumo), divisas; Informe Mensual, Pulso Económico Semanal, informe diario de mercados, documentos de trabajo
- **Motivo de inclusión y uso:** Servicio de estudios bancario español de acceso libre con publicaciones de alta frecuencia y datos propios de consumo. Uso: segunda opinión sobre coyuntura española frente a Banco de España e INE.
- **Uso en el bloque:** AG-B04 y AG-B08: informes sectoriales de España (agroalimentario, turismo, inmobiliario, industria) y consumo; AG-B03.
- **Sesgos y cautelas:** Visión de un banco comercial (conflicto de interés potencial en vivienda, crédito y renta variable española); aviso legal en la web de CaixaBank.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Cinco Días cincodias.elpais.com mercados financieros»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1).

<!-- ===== Tanda 2 (2026-11-02): 22 búsquedas WebSearch. Las fichas siguientes se fusionan en su temática y por Q descendente. ===== -->
<!-- Vía «directorio FCA»: URL tomada de la página oficial de la FCA «Regulators in the EU and European Economic Area (EEA)» (https://www.fca.org.uk/firms/regulators-eu-eea, devuelta por búsqueda y leída con WebFetch); la propia FCA advierte que algunos enlaces pueden estar desactualizados. Vía «Wikipedia»: URL oficial leída en la ficha (infobox) del artículo de Wikipedia alcanzado desde una búsqueda. -->
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0232 · Q 74 (B) — ING THINK

- **Canal oficial (URL raíz):** https://think.ing.com/ (quiénes somos: https://think.ing.com/about/)
- **Emisor:** ING (más de 40 economistas)
- **Temática:** TFB-11 Análisis de bancos, gestoras, consultoras y think tanks (principal) · secundarias: TFB-12
- **Calidad Q:** 74 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 12/15 · Independencia 6/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** secundaria cualificada (análisis de banco)
- **Acceso:** Abierto
- **Ámbitos:** Macro, bancos centrales, divisas (tabla mensual de previsiones FX Talking), materias primas, sectores; ING Monthly
- **Motivo de inclusión y uso:** Análisis bancario europeo abierto, con tablas de previsiones publicadas. Uso: previsiones de divisas y tipos para el Evaluador; consenso europeo.
- **Uso en el bloque:** AG-B08 y AG-B05: análisis sectorial (energía, materias primas, transporte, tecnología) y macro europeo.
- **Sesgos y cautelas:** Visión de un banco; la investigación profesional regulada está en otro portal.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ING THINK economic and financial analysis think.ing.com»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 3).
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0238 · Q 74 (B) — Capital Economics

- **Canal oficial (URL raíz):** https://www.capitaleconomics.com/ (la empresa: https://capitaleconomics.com/about-us/the-company/)
- **Emisor:** Capital Economics (Londres, fundada en 1999)
- **Temática:** TFB-11 Análisis de bancos, gestoras, consultoras y think tanks (principal) · secundarias: —
- **Calidad Q:** 74 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 13/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 7/10
- **Tipología:** secundaria cualificada (casa de análisis independiente)
- **Acceso:** Suscripción; algunos contenidos públicos
- **Ámbitos:** Macro y mercados de más de 100 economías, con más de 60 economistas; previsiones y modelos propios
- **Motivo de inclusión y uso:** Casa independiente sin banca de inversión, intermediación ni cartera propia. Uso: contrapunto independiente a los bancos de inversión y previsiones contrastables para el Evaluador.
- **Uso en el bloque:** AG-B08: notas públicas de macro y mercados; AG-B14 Contrarias por su perfil independiente.
- **Sesgos y cautelas:** Acceso mayoritariamente de pago.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Capital Economics independent macroeconomic research consultancy»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 3).
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0233 · Q 73 (B) — BNP Paribas Economic Research

- **Canal oficial (URL raíz):** https://economic-research.bnpparibas.com/ (equipos: https://economic-research.bnpparibas.com/Teams/en-US · Eco Flash: https://economic-research.bnpparibas.com/Publications/Eco-Flash/en-US)
- **Emisor:** BNP Paribas, departamento de estudios económicos (París; economista jefa del grupo: Isabelle Mateos y Lago)
- **Temática:** TFB-11 Análisis de bancos, gestoras, consultoras y think tanks (principal) · secundarias: —
- **Calidad Q:** 73 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 12/15 · Independencia 6/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** secundaria cualificada (análisis de banco)
- **Acceso:** Abierto (EN/FR, RSS y suscripción)
- **Ámbitos:** Economías de la OCDE, emergentes y riesgo país, economía bancaria; Eco Flash, Eco Conjoncture, Eco Week, Eco Emerging, escenarios y previsiones
- **Motivo de inclusión y uso:** Estudios de un gran banco de la zona euro con equipo de riesgo país. Uso: escenario y previsiones de la eurozona y de emergentes.
- **Uso en el bloque:** AG-B08: análisis económico y sectorial de la zona euro y emergentes.
- **Sesgos y cautelas:** Visión de un banco comercial.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «BNP Paribas Economic Research economic-research.bnpparibas.com EcoFlash»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 3).
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0229 · Q 72 (B) — BBVA Research

- **Canal oficial (URL raíz):** https://www.bbvaresearch.com/ (quiénes somos: https://www.bbvaresearch.com/en/about-us/)
- **Emisor:** BBVA (servicio de estudios fundado en 1932; economista jefe: Jorge Sicilia)
- **Temática:** TFB-11 Análisis de bancos, gestoras, consultoras y think tanks (principal) · secundarias: TFB-02
- **Calidad Q:** 72 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 12/15 · Independencia 6/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** secundaria cualificada (análisis de banco)
- **Acceso:** Abierto (publicaciones descargables; no hay declaración expresa de licencia)
- **Ámbitos:** Macro, sistemas financieros, economía digital y geoestrategia; previsiones para más de 10 países (España, México, Turquía, Colombia, Argentina, Perú, China); indicadores de big data
- **Motivo de inclusión y uso:** Servicio de estudios con más de 100 analistas, previsiones publicadas e indicadores de alta frecuencia. Uso: segunda opinión sobre España y Latinoamérica, y previsiones para el Evaluador.
- **Uso en el bloque:** AG-B08 Macro y Ciclo y AG-B04: análisis sectorial y de consumo (Big Data de tarjetas) de España y Latinoamérica; AG-B13.
- **Sesgos y cautelas:** Visión de un banco comercial con intereses en los países que cubre.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ING THINK economic research BBVA Research Allianz Research publications»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 2).
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0045 · Q 71 (B) — J.P. Morgan Asset Management — Guide to the Markets

- **Canal oficial (URL raíz):** https://am.jpmorgan.com/ (Guide to the Markets: https://am.jpmorgan.com/lu/en/asset-management/nra/insights/market-insights/guide-to-the-markets/)
- **Emisor:** J.P. Morgan Asset Management
- **Temática:** TFB-11 Análisis de bancos, gestoras, consultoras y think tanks (principal) · secundarias: —
- **Calidad Q:** 71 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 13/15 · Independencia 5/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** secundaria (compendio de datos)
- **Acceso:** Abierto (PDF por región: EE. UU., Latinoamérica)
- **Ámbitos:** Gráficos de valoración, macro y mercados por clase de activo
- **Motivo de inclusión y uso:** Compendio trimestral de datos y gráficos; útil para contexto y consenso.
- **Uso en el bloque:** AG-B09 y AG-B08: datos de valoración, beneficios y márgenes por sector en gráficos trimestrales.
- **Sesgos y cautelas:** Gestora con productos; compilación de datos de terceros (citar la fuente primaria de cada gráfico).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «am.jpmorgan.com Guide to the Markets quarterly US»; WebFetch: sí)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada en verificación de alta 2026-11-02 (tanda 2).
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0249 · Q 71 (B) — Amundi Investment Institute — Research Center

- **Canal oficial (URL raíz):** https://research-center.amundi.com/ (Global Investment Views: https://research-center.amundi.com/publications/global-investment-views)
- **Emisor:** Amundi (Amundi Investment Institute)
- **Temática:** TFB-11 Análisis de bancos, gestoras, consultoras y think tanks (principal) · secundarias: TFB-08
- **Calidad Q:** 71 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 13/15 · Independencia 5/10 · Actualidad 10/10 · Acceso 8/10
- **Tipología:** secundaria cualificada (visión de gestora)
- **Acceso:** Abierto con aceptación de condiciones (dirigido a profesionales no estadounidenses)
- **Ámbitos:** Global Investment Views mensual (última: octubre de 2026), convicciones de los CIO, estrategia de mercados e investigación académica
- **Motivo de inclusión y uso:** Visión de la mayor gestora europea. Uso: consenso institucional europeo y asignación táctica.
- **Uso en el bloque:** AG-B09 y AG-B13: perspectivas de mercados y temáticas (gestora europea); opinión.
- **Sesgos y cautelas:** Gestora con productos; audiencia profesional.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Amundi Investment Institute outlook research»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 3).
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0096 · Q 69 (B) — McKinsey Global Institute

- **Canal oficial (URL raíz):** https://www.mckinsey.com/mgi
- **Emisor:** McKinsey & Company (MGI, fundado en 1990)
- **Temática:** TFB-11 Análisis de bancos, gestoras, consultoras y think tanks (principal) · secundarias: —
- **Calidad Q:** 69 (B) — Primariedad 13/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 13/15 · Independencia 7/10 · Actualidad 8/10 · Acceso 8/10
- **Tipología:** secundaria
- **Acceso:** Abierto (registro para algunos informes)
- **Ámbitos:** Productividad, tecnología, demografía, comercio, mercados de capitales, salud
- **Motivo de inclusión y uso:** Estudios de tendencias de largo plazo con estimaciones cuantitativas.
- **Uso en el bloque:** AG-B13 Prospectiva y AG-B04: dimensionado de mercados y tendencias de largo plazo; opinión con datos propios, contrastar cifras.
- **Sesgos y cautelas:** Brazo de investigación de una consultora; declara que sus informes no están encargados ni pagados por terceros, pero lo dirigen socios de McKinsey; estimaciones a veces optimistas.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «McKinsey Global Institute research reports mckinsey.com/mgi»; WebFetch: sí, resumen ejecutivo de MGI en mckinsey.com; la URL raíz /mgi no salió literalmente en los resultados)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada por BFA en F9_S3 (2026-11-02).
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0230 · Q 69 (B) — Allianz Research

- **Canal oficial (URL raíz):** https://www.allianz.com/en/economic_research/ (publicaciones: https://www.allianz.com/en/economic_research/publications/insights.html)
- **Emisor:** Allianz SE (servicio de estudios económicos)
- **Temática:** TFB-11 Análisis de bancos, gestoras, consultoras y think tanks (principal) · secundarias: —
- **Calidad Q:** 69 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 12/15 · Independencia 6/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** secundaria cualificada
- **Acceso:** Abierto (sin declaración expresa de licencia)
- **Ámbitos:** Riesgo país y sectorial, Global Wealth Report (2026), Global Insurance Map, investigación de clima y transición, gráficos y podcast
- **Motivo de inclusión y uso:** Estudios de un gran asegurador europeo, con datos propios de riesgo país y riqueza financiera de los hogares. Uso: riesgo país e insolvencias, y contexto de ahorro y riqueza.
- **Uso en el bloque:** AG-B11 Sostenibilidad y Riesgos y AG-B03: insolvencias empresariales y análisis sectorial (Allianz Trade); AG-B08.
- **Sesgos y cautelas:** Visión de un grupo asegurador con negocio de gestión de activos; el listado de publicaciones no se mostró completo al leerlo.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ING THINK economic research BBVA Research Allianz Research publications»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 2).
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0239 · Q 69 (B) — Oxford Economics

- **Canal oficial (URL raíz):** https://www.oxfordeconomics.com/ (Global Macro Service: https://www.oxfordeconomics.com/subscriptions/global-macro-service/)
- **Emisor:** Oxford Economics (grupo que incluye Tourism Economics, Alpine Macro y FrontierView)
- **Temática:** TFB-11 Análisis de bancos, gestoras, consultoras y think tanks (principal) · secundarias: —
- **Calidad Q:** 69 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 13/15 · Independencia 8/10 · Actualidad 9/10 · Acceso 6/10
- **Tipología:** secundaria cualificada (consultora de previsión)
- **Acceso:** Suscripción; notas de investigación y blogs públicos
- **Ámbitos:** Previsiones nacionales, sectoriales y urbanas de más de 200 economías; Global Economic Model y Global Industry Model
- **Motivo de inclusión y uso:** Modelo macro global usado por empresas y gobiernos. Uso: escenarios y previsiones de terceros independientes de la banca.
- **Uso en el bloque:** AG-B04 y AG-B08: previsiones sectoriales e industriales (contenidos públicos).
- **Sesgos y cautelas:** Acceso mayoritariamente de pago; consultora con encargos de clientes.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Oxford Economics global economic forecasts research»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 3).
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### MBF-0246 · Q 66 (B) — BCG Henderson Institute (BCG Institute) — think tank de Boston Consulting Group

- **Canal oficial (URL raíz):** https://www.bcg.com/en-us/bcg-henderson-institute
- **Emisor:** Boston Consulting Group (BCG)
- **Documentación y notas:** Seis equipos: Estrategia, Geopolítica, Tecnología e IA, Clima y transición energética, Macroeconomía y Futuros humanos. Publicaciones recientes: «Who Will Pay the $2.6 Trillion AI Infrastructure Bill?» (29/10/2026), «The Great Divide: How the US and China Are Splitting the AI World» (30/06/2026), «Beyond Tomorrow: Four Scenarios for the World of 2050» (20/04/2026). Boletín y pódcast «Thinkers and Ideas».
- **Temática:** TFB-11 Análisis de bancos, gestoras, consultoras y think tanks (principal) · secundarias: TFB-09
- **Calidad Q:** 66 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 8/15 · Autoridad 12/15 · Independencia 6/10 · Actualidad 10/10 · Acceso 8/10
- **Tipología:** secundaria y de opinión (consultora)
- **Acceso:** Abierto (boletín con registro)
- **Ámbitos:** Estrategia competitiva, IA, geopolítica, transición energética, escenarios
- **Motivo de inclusión y uso:** Marcos de estrategia y dimensionado de inversiones (p. ej., infraestructura de IA) útiles como hipótesis a contrastar.
- **Uso en el bloque:** AG-B03 (dinámica competitiva), AG-B06 (IA), AG-B13 Prospectiva (escenarios) y AG-B14 Contrarias; opinión, nunca prueba.
- **Restricciones de uso:** Uso con atribución.
- **Sesgos y cautelas:** Interés comercial de consultoría; cifras de mercado sin metodología completa.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** La página se presenta ahora como «BCG Institute».
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-03 (búsqueda web: «BCG Henderson Institute publications Deloitte Insights industry outlooks Bain research reports free»; WebFetch: sí)
- **Origen:** Alta F9 Bloque B (2026-11-03).

#### MBF-0247 · Q 66 (B) — Deloitte Insights — perspectivas sectoriales y centros de investigación

- **Canal oficial (URL raíz):** https://www.deloitte.com/us/en/insights/about
- **Emisor:** Deloitte (red de firmas miembro de Deloitte Touche Tohmatsu Limited)
- **Documentación y notas:** Plataforma de artículos, informes, infografías y pódcast por industria (consumo, energía e industria, servicios financieros, sector público, ciencias de la vida y salud, tecnología, medios y telecomunicaciones); colección «2026 Industry outlooks» y Weekly Global Economic Outlook.
- **Temática:** TFB-11 Análisis de bancos, gestoras, consultoras y think tanks (principal) · secundarias: TFB-04
- **Calidad Q:** 66 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 8/15 · Autoridad 12/15 · Independencia 6/10 · Actualidad 10/10 · Acceso 8/10
- **Tipología:** secundaria y de opinión (consultora)
- **Acceso:** Abierto (suscripción opcional MyDeloitte)
- **Ámbitos:** Perspectivas anuales por industria, encuestas a directivos, macro semanal
- **Motivo de inclusión y uso:** Panorámica anual por industria con encuestas propias a directivos.
- **Uso en el bloque:** AG-B04 (intención de inversión y adopción según encuestas) y AG-B13; AG-B02 Director para el marco de cada sector.
- **Restricciones de uso:** Uso con atribución.
- **Sesgos y cautelas:** Interés comercial; encuestas con muestras propias y poco documentadas.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-03 (búsqueda web: «BCG Henderson Institute publications Deloitte Insights industry outlooks Bain research reports free»; WebFetch: sí)
- **Origen:** Alta F9 Bloque B (2026-11-03).

#### RF-0046 · Q 66 (B) — Goldman Sachs Global Investment Research

- **Canal oficial (URL raíz):** https://www.goldmansachs.com/insights/goldman-sachs-research (Top of Mind e informes: https://www.goldmansachs.com/insights/reports)
- **Emisor:** Goldman Sachs
- **Temática:** TFB-11 Análisis de bancos, gestoras, consultoras y think tanks (principal) · secundarias: —
- **Calidad Q:** 66 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 14/15 · Independencia 5/10 · Actualidad 9/10 · Acceso 3/10
- **Tipología:** secundaria cualificada
- **Acceso:** Restringido (clientes, Marquee); resúmenes públicos (Top of Mind, artículos, boletín semanal Briefings)
- **Ámbitos:** Previsiones macro, estrategia, sectores
- **Motivo de inclusión y uso:** Análisis de banco de inversión influyente; usar solo resúmenes públicos citables.
- **Uso en el bloque:** AG-B09 y AG-B13: notas públicas de temática (IA, energía, demografía) y de valoración sectorial; AG-B14 para contrastar consenso.
- **Sesgos y cautelas:** Conflictos de interés de banca de inversión; acceso restringido; el portal no señala qué contenidos son solo para clientes.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Goldman Sachs Global Investment Research insights Top of Mind»; WebFetch: sí)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada en verificación de alta 2026-11-02 (tanda 2); URL raíz corregida.
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0240 · Q 66 (B) — Morgan Stanley — Ideas y pódcast «Thoughts on the Market»

- **Canal oficial (URL raíz):** https://www.morganstanley.com/ideas (pódcasts: https://www.morganstanley.com/ideas/morgan-stanley-podcast-homepage)
- **Emisor:** Morgan Stanley
- **Temática:** TFB-11 Análisis de bancos, gestoras, consultoras y think tanks (principal) · secundarias: —
- **Calidad Q:** 66 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 14/15 · Independencia 5/10 · Actualidad 10/10 · Acceso 5/10
- **Tipología:** secundaria cualificada
- **Acceso:** Pódcast diario abierto; investigación completa restringida a clientes
- **Ámbitos:** Estrategia de mercados, macro, sectores (pódcast diario con analistas del banco)
- **Motivo de inclusión y uso:** Resumen público diario de la visión de estrategas y analistas de un gran banco de inversión. Uso: consenso de la banca de inversión.
- **Uso en el bloque:** AG-B09 y AG-B13: ideas temáticas y sectoriales públicas; AG-B14.
- **Sesgos y cautelas:** Conflictos de interés de banca de inversión; contenido público resumido.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Morgan Stanley Research ideas Thoughts on the Market»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 3).
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0243 · Q 65 (B) — Citi GPS (Global Perspectives & Solutions)

- **Canal oficial (URL raíz):** https://www.citigroup.com/global/insights/tags/citi-global-perspectives-solutions
- **Emisor:** Citigroup
- **Temática:** TFB-11 Análisis de bancos, gestoras, consultoras y think tanks (principal) · secundarias: —
- **Calidad Q:** 65 (B) — Primariedad 11/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 13/15 · Independencia 5/10 · Actualidad 8/10 · Acceso 8/10
- **Tipología:** secundaria cualificada (informes temáticos)
- **Acceso:** Abierto (suscripción por correo)
- **Ámbitos:** Tendencias globales: mercados y economía, tecnología, sostenibilidad, estrategia empresarial; colaboración con la Oxford Martin School
- **Motivo de inclusión y uso:** Informes temáticos de largo plazo de un banco global. Uso: detección de megatendencias para el Analizador.
- **Uso en el bloque:** AG-B13 y AG-B04: informes temáticos de dimensionado de mercados (Citi GPS); contrastar cifras con fuentes primarias.
- **Sesgos y cautelas:** Visión de un banco con intereses comerciales; la página de etiqueta no listó informes concretos.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Citi GPS Global Perspectives and Solutions reports»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 3).
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0236 · Q 62 (C) — Deutsche Bank Research (portal profesional)

- **Canal oficial (URL raíz):** https://research.db.com/ (ejemplo: https://research.db.com/Research/Disclosures/FICCDisclosures)
- **Emisor:** Deutsche Bank AG (Fráncfort)
- **Temática:** TFB-11 Análisis de bancos, gestoras, consultoras y think tanks (principal) · secundarias: —
- **Calidad Q:** 62 (C) — Primariedad 12/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 13/15 · Independencia 5/10 · Actualidad 8/10 · Acceso 3/10
- **Tipología:** secundaria cualificada (análisis de banco de inversión)
- **Acceso:** Restringido (clientes); divulgaciones regulatorias públicas
- **Ámbitos:** Renta fija, divisas, materias primas, crédito, estrategia; históricos de recomendaciones (divulgaciones de octubre de 2026)
- **Motivo de inclusión y uso:** Análisis de un gran banco europeo; las divulgaciones públicas permiten auditar recomendaciones históricas. Uso: solo extractos públicos citables.
- **Uso en el bloque:** AG-B08 y AG-B13: temas estructurales europeos y alemanes (portal profesional).
- **Sesgos y cautelas:** Conflictos de interés de banca de inversión; casi todo el contenido es de acceso restringido.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Deutsche Bank Research dbresearch.com publications»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9_S1, tanda 3).
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

## TFB-12 Materias primas y energía

#### RF-0059 · Q 90 (A) — U.S. Energy Information Administration (EIA)

- **Canal oficial (URL raíz):** https://www.eia.gov/
- **Emisor:** U.S. Energy Information Administration (Departamento de Energía de EE. UU.)
- **Documentación y notas:** Pieza principal: Weekly Petroleum Status Report (https://eia.gov/petroleum/supply/weekly; calendario en …/weekly/schedule.php; descargas XLSX/CSV/JSON; notas explicativas y fe de erratas). Enlaza Short-Term Energy Outlook (eia.gov/outlooks/steo/), Annual Energy Outlook, Monthly Energy Review, precios spot diarios y precios minoristas semanales. Último número listado en la consulta: 21/10/2026.
- **Temática:** TFB-12 Materias primas y energía (principal) · secundarias: TFB-01
- **Calidad Q:** 90 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto (dominio público)
- **Ámbitos:** Inventarios semanales de crudo y productos, producción, importaciones; previsiones STEO
- **Motivo de inclusión y uso:** Dato primario de energía; catalizador semanal para H1-H2.
- **Uso en el bloque:** AG-B05 Oferta y Cadena de Suministro y AG-B08: inventarios, producción y precios de energía de EE. UU.; MC-B para series de oferta y demanda.
- **Restricciones de uso:** Uso libre; citar informe, tabla y semana.
- **Sesgos y cautelas:** Cobertura centrada en EE. UU.; estimaciones semanales sujetas a revisión mensual.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «EIA Weekly Petroleum Status Report Short-Term Energy Outlook eia.gov»; WebFetch: sí)
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0061 · Q 89 (A) — USDA — WASDE

- **Canal oficial (URL raíz):** https://www.usda.gov/about-usda/general-information/staff-offices/office-chief-economist/commodity-markets/wasde-report
- **Emisor:** U.S. Department of Agriculture — World Agricultural Outlook Board (WAOB)
- **Documentación y notas:** Informe mensual (12:00 ET) de oferta y demanda de trigo, arroz, cereales secundarios, oleaginosas y algodón (EE. UU. y mundo) y de azúcar, carne, aves, huevos y leche (EE. UU.). Último visto: 09/10/2026; siguiente: 10/11/2026. Acceso corto: usda.gov/wasde. Archivo histórico en ESMIS (esmis.nal.usda.gov).
- **Temática:** TFB-12 Materias primas y energía (principal) · secundarias: —
- **Calidad Q:** 89 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto (dominio público)
- **Ámbitos:** Balances mundiales de oferta y demanda agrícola
- **Motivo de inclusión y uso:** Informe mensual que mueve los precios agrícolas (catalizador de calendario).
- **Uso en el bloque:** AG-B05 y AG-B04: balances de oferta y demanda agrícola para subsectores agroalimentarios.
- **Restricciones de uso:** Uso libre; citar edición mensual.
- **Sesgos y cautelas:** Revisiones mensuales de las estimaciones.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Reorganización de URL en usda.gov (la URL antigua /oce/commodity/wasde aparece aún en buscadores).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «USDA WASDE World Agricultural Supply and Demand Estimates report»; WebFetch: sí)
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0067 · Q 89 (A) — FAO — Índice de precios de los alimentos

- **Canal oficial (URL raíz):** https://www.fao.org/worldfoodsituation/FoodPricesIndex/en
- **Emisor:** Organización de las Naciones Unidas para la Alimentación y la Agricultura (FAO)
- **Documentación y notas:** Índice mensual ponderado por cuotas de exportación 2014-2016 de cinco subíndices (cereales, aceites vegetales, azúcar, carne, lácteos). Última publicación vista: 02/10/2026 (septiembre: 136,0 puntos); próxima: 06/11/2026.
- **Temática:** TFB-12 Materias primas y energía (principal) · secundarias: —
- **Calidad Q:** 89 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Precios internacionales de alimentos
- **Motivo de inclusión y uso:** Indicador mensual de inflación alimentaria global.
- **Uso en el bloque:** AG-B04 y AG-B08: precios internacionales de alimentos para márgenes de la industria alimentaria.
- **Restricciones de uso:** Uso con atribución; citar mes y versión (se revisa).
- **Sesgos y cautelas:** Índice agregado; el subíndice de carne usa precios proyectados y se revisa de forma significativa.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «EIA WASDE FAO food price index OPEC MOMR World Bank Pink Sheet LBMA LME World Gold Council»; WebFetch: sí)
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0356 · Q 86 (A) — USGS — Mineral Commodity Summaries

- **Canal oficial (URL raíz):** https://www.usgs.gov/centers/national-minerals-information-center/mineral-commodity-summaries
- **Emisor:** U.S. Geological Survey (National Minerals Information Center)
- **Documentación y notas:** Publicación anual con fichas de más de 90 minerales (estructura de la industria, aranceles, cinco años de estadísticas, producción mundial y reservas); edición 2026 y publicación de datos (doi.org/10.5066/P1WKQ63T).
- **Temática:** TFB-12 Materias primas y energía (principal) · secundarias: —
- **Calidad Q:** 86 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 6/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto (dominio público)
- **Ámbitos:** Producción, reservas y precios de minerales y metales críticos
- **Motivo de inclusión y uso:** Referencia oficial sobre minerales críticos (litio, cobre, tierras raras).
- **Uso en el bloque:** AG-B05 y AG-B07: producción, reservas y dependencia de importación por mineral (litio, cobre, tierras raras); MC-B de concentración de la oferta.
- **Restricciones de uso:** Uso libre; citar edición y mineral.
- **Sesgos y cautelas:** Frecuencia anual; datos del año anterior estimados.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «USGS Mineral Commodity Summaries 2026»; WebFetch: sí)
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0062 · Q 85 (A) — OPEP — Monthly Oil Market Report

- **Canal oficial (URL raíz):** https://www.opec.org/
- **Emisor:** Organización de Países Exportadores de Petróleo (OPEP)
- **Documentación y notas:** URL raíz confirmada en la lista de organizaciones socias de JODI (jodidata.org). La página concreta del Monthly Oil Market Report no se ha leído (sitio no accesible con la herramienta).
- **Temática:** TFB-12 Materias primas y energía (principal) · secundarias: —
- **Calidad Q:** 85 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 14/15 · Independencia 9/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Oferta, demanda y producción de crudo de la OPEP
- **Motivo de inclusión y uso:** Fuente primaria de la política de oferta de la OPEP.
- **Uso en el bloque:** AG-B05 y AG-B08: balance mundial de petróleo (visión OPEP) para el sector de petróleo y gas.
- **Restricciones de uso:** Citar edición del MOMR.
- **Sesgos y cautelas:** Parte interesada en el precio; producción de miembros por fuentes secundarias y comunicación directa.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «JODI Oil World Database partner organisations APEC Eurostat GECF IEA OPEC»; URL tomada de la página de socios de JODI leída con WebFetch; WebFetch al sitio: no)
- **Alerta:** REPARAR en el próximo barrido: leer y registrar la URL de la pieza MOMR.
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0066 · Q 85 (A) — Banco Mundial — Commodity Markets (Pink Sheet y Outlook)

- **Canal oficial (URL raíz):** https://www.worldbank.org/en/research/commodity-markets
- **Emisor:** Banco Mundial
- **Documentación y notas:** Pink Sheet mensual (PDF de precios, XLS mensual y anual; última actualización vista 02/10/2026, siguiente 03/11/2026) y Commodity Markets Outlook semestral (última edición octubre de 2026, siguiente abril de 2027). Ficheros en Open Knowledge Repository; licencia CC BY para datos.
- **Temática:** TFB-12 Materias primas y energía (principal) · secundarias: —
- **Calidad Q:** 85 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** secundaria
- **Acceso:** Abierto (CC BY)
- **Ámbitos:** Precios mensuales de materias primas y previsiones semestrales
- **Motivo de inclusión y uso:** Serie homogénea larga de precios y previsiones institucionales.
- **Uso en el bloque:** AG-B05 y AG-B09: precios mensuales de materias primas (Pink Sheet) y previsiones para márgenes sectoriales.
- **Restricciones de uso:** Atribución CC BY; citar edición.
- **Sesgos y cautelas:** Frecuencia mensual; previsiones con supuestos propios.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «World Bank Commodity Markets Pink Sheet monthly prices Commodity Markets Outlook»; WebFetch: sí)
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0358 · Q 85 (A) — CORES — Boletín Estadístico de Hidrocarburos

- **Canal oficial (URL raíz):** https://www.cores.es/sites/default/files/archivos/publicaciones/boletin-est-hidrocarburos-333-agosto-2025.pdf
- **Emisor:** Corporación de Reservas Estratégicas de Productos Petrolíferos (CORES; tutelada por el MITECO)
- **Documentación y notas:** Boletín numerado mensual con consumo de productos petrolíferos y gas natural, importaciones de crudo por origen, balances, precios, comercio exterior y reservas en España (n.º 333, agosto de 2025: importaciones de crudo de 5.138 kt, −10,9 % interanual).
- **Temática:** TFB-12 Materias primas y energía (principal) · secundarias: —
- **Calidad Q:** 85 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 7/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Consumo de carburantes y gas, importaciones de crudo en España
- **Motivo de inclusión y uso:** Fuente oficial española de energía (demanda doméstica y seguridad de suministro).
- **Uso en el bloque:** AG-B04 y AG-B05: consumo de productos petrolíferos y gas en España por producto.
- **Restricciones de uso:** Uso con atribución; citar número y mes.
- **Sesgos y cautelas:** Desfase de unos dos meses.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «CORES Corporación de Reservas Estratégicas de Productos Petrolíferos boletín estadístico consumo»; WebFetch: sí)
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0354 · Q 84 (A) — IRENA — estadísticas de energías renovables

- **Canal oficial (URL raíz):** https://www.irena.org/-/media/Files/IRENA/Agency/Publication/2026/Jul/IRENA_DAT_RE_Statistics_2026.pdf
- **Emisor:** International Renewable Energy Agency (IRENA)
- **Documentación y notas:** Renewable Energy Statistics 2026: capacidad 2016–2025 y producción 2016–2024 por tecnología, país y región, capacidad aislada, financiación pública e indicadores ODS 7; datos en irena.org/statistics. Publica además Renewable Capacity Statistics (marzo/abril).
- **Temática:** TFB-12 Materias primas y energía (principal) · secundarias: TFB-17
- **Calidad Q:** 84 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 7/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Capacidad y generación renovable mundial
- **Motivo de inclusión y uso:** Fuente oficial intergubernamental de despliegue renovable.
- **Uso en el bloque:** AG-B04 y AG-B05: capacidad y costes de renovables por tecnología y país para los subsectores de energías renovables.
- **Restricciones de uso:** Uso con atribución; citar edición.
- **Sesgos y cautelas:** Desfase de uno a dos años en producción.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «IRENA Renewable Capacity Statistics 2026»; WebFetch: sí)
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0355 · Q 84 (A) — GIE — AGSI+ y ALSI (almacenamiento de gas y GNL en Europa)

- **Canal oficial (URL raíz):** https://www.gie.eu/agsi-and-alsi-transparency-platforms/
- **Emisor:** Gas Infrastructure Europe (GIE)
- **Documentación y notas:** Plataformas de transparencia con datos diarios de existencias de almacenamiento subterráneo (AGSI, agsi.gie.eu; 100 % del mercado UE-27) y de terminales de GNL (ALSI, alsi.gie.eu), aportados por los operadores; plataforma de información privilegiada iip.gie.eu.
- **Temática:** TFB-12 Materias primas y energía (principal) · secundarias: —
- **Calidad Q:** 84 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 14/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Llenado de almacenes de gas y emisión de GNL en Europa
- **Motivo de inclusión y uso:** Indicador diario clave del equilibrio del gas europeo (precio TTF).
- **Uso en el bloque:** AG-B05 y AG-B11: llenado de almacenamientos de gas y GNL en Europa para utilities y química.
- **Restricciones de uso:** Citar fecha y país.
- **Sesgos y cautelas:** Datos declarados por operadores de forma voluntaria.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «GIE AGSI+ aggregated gas storage inventory»; WebFetch: sí)
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### MBF-0249 · Q 83 (A) — AIE (IEA) — Global Critical Minerals Outlook (2024, 2025 y 2026)

- **Canal oficial (URL raíz):** https://iea.org/reports/global-critical-minerals-outlook-2025 (ediciones: https://www.iea.org/reports/global-critical-minerals-outlook-2024 · https://iea.org/reports/global-critical-minerals-outlook-2026)
- **Emisor:** Agencia Internacional de la Energía (AIE/IEA)
- **Documentación y notas:** Informe anual de oferta, demanda, precios, inversión y concentración geográfica de minerales críticos (litio, níquel, cobalto, cobre, grafito, tierras raras); la edición 2025 alertó de la falta de diversificación geográfica de la oferta. Existe edición 2026.
- **Temática:** TFB-12 Materias primas y energía (principal) · secundarias: TFB-05
- **Calidad Q:** 83 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** primaria (análisis de agencia intergubernamental)
- **Acceso:** Abierto (informe gratuito; licencia de la AIE)
- **Ámbitos:** Minerales críticos: balances, concentración, refinado, riesgos de suministro
- **Motivo de inclusión y uso:** Referencia para dimensionar el mercado y los riesgos de suministro de los minerales de la transición energética.
- **Uso en el bloque:** AG-B05 Oferta y Cadena de Suministro (concentración de minería y refinado), AG-B07 (geopolítica de minerales) y AG-B04 (demanda por tecnología); Motor AG-B16 (MC-B de concentración tipo HHI).
- **Restricciones de uso:** Licencia y condiciones de la AIE; citar edición.
- **Sesgos y cautelas:** Proyecciones dependientes de escenarios de política; la AIE es parte interesada en el debate de transición.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-03 (búsqueda web: «IEA Critical Minerals Data Explorer Global Critical Minerals Outlook 2025 ENTSO-E Transparency Platform»; WebFetch: no)
- **Origen:** Alta F9 Bloque B (2026-11-03).

#### RF-0308 · Q 83 (A) — JODI — Joint Organisations Data Initiative (JODI-Oil y JODI-Gas)

- **Canal oficial (URL raíz):** https://www.jodidata.org/oil/database.aspx
- **Emisor:** Joint Organisations Data Initiative, coordinada por el International Energy Forum (IEF); socios: APEC, Eurostat, GECF, IEA, OLADE, OPEP, UNSD
- **Documentación y notas:** Base mundial de petróleo actualizada mensualmente con datos de unos 100 países (≈ 90 % de la oferta y demanda mundial); calendario de actualización y lista de economías participantes; cuestionario normalizado.
- **Temática:** TFB-12 Materias primas y energía (principal) · secundarias: —
- **Calidad Q:** 83 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (descargas; algunas funciones con registro)
- **Ámbitos:** Producción, demanda, existencias y comercio de crudo y productos por país (y gas en JODI-Gas)
- **Motivo de inclusión y uso:** Base multilateral oficial para balances petroleros por país, independiente de una sola agencia.
- **Uso en el bloque:** AG-B05: producción, demanda e inventarios de petróleo y gas por país (JODI).
- **Restricciones de uso:** Citar país, serie y mes de actualización.
- **Sesgos y cautelas:** Calidad heterogénea según el país declarante; la página de base de datos mostraba «Coming soon» en la sección de visualización.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «JODI Oil World Database partner organisations APEC Eurostat GECF IEA OPEC»; WebFetch: sí)
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0352 · Q 83 (A) — Energy Institute — Statistical Review of World Energy

- **Canal oficial (URL raíz):** https://www.energyinst.org/__data/assets/pdf_file/0004/1822009/Statistical-Review-of-World-Energy-2026-Summary-version.pdf
- **Emisor:** Energy Institute (con Ember, Kearney y KPMG; compilación de Wattage)
- **Documentación y notas:** 75.ª edición (2026, datos de 2025): producción, consumo, comercio y emisiones de energía por país; libro Excel y base de datos con histórico desde 1965 en energyinst.org/statistical-review. Heredera de la antigua revisión de BP.
- **Temática:** TFB-12 Materias primas y energía (principal) · secundarias: —
- **Calidad Q:** 83 (A) — Primariedad 17/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** secundaria
- **Acceso:** Abierto
- **Ámbitos:** Balances energéticos mundiales por país y fuente
- **Motivo de inclusión y uso:** Serie larga homogénea de energía mundial para análisis estructural.
- **Uso en el bloque:** AG-B05 y AG-B13: serie larga de energía mundial por fuente y país para dimensionar mercados energéticos.
- **Restricciones de uso:** Citar edición y tabla.
- **Sesgos y cautelas:** Frecuencia anual; datos del año anterior.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Editor desde 2023: Energy Institute (antes BP).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Energy Institute Statistical Review of World Energy 2026»; WebFetch: sí)
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### MBF-0248 · Q 82 (A) — AIE (IEA) — Critical Minerals Data Explorer

- **Canal oficial (URL raíz):** https://www.iea.org/data-and-statistics/data-tools/critical-minerals-data-explorer (conjunto de datos: https://origin.iea.org/data-and-statistics/data-product/critical-minerals-dataset)
- **Emisor:** Agencia Internacional de la Energía (AIE/IEA)
- **Documentación y notas:** Herramienta interactiva con proyecciones de demanda de 37 minerales críticos (destacados cobre, litio, níquel, cobalto y neodimio; también grafito, aluminio y tierras raras) por tecnología limpia, en los tres escenarios principales de la AIE y 12 casos tecnológicos alternativos; proyecciones de oferta a largo plazo previstas. Se actualiza con el modelo Global Energy and Climate. Cita sugerida: IEA (2023), Critical Minerals Data Explorer, IEA, París.
- **Temática:** TFB-12 Materias primas y energía (principal) · secundarias: TFB-17
- **Calidad Q:** 82 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 8/10 · Acceso 9/10
- **Tipología:** primaria (proyecciones de agencia)
- **Acceso:** Abierto (herramienta pública)
- **Ámbitos:** Demanda de minerales críticos por tecnología y escenario
- **Motivo de inclusión y uso:** Cuantifica la demanda futura de cada mineral por tecnología (baterías, redes, eólica, solar, VE).
- **Uso en el bloque:** AG-B04 Demanda y Adopción y AG-B05 (balances de minerales); Motor AG-B16 (escenarios de demanda); AG-B13 Prospectiva.
- **Restricciones de uso:** Condiciones de la AIE; licencia no indicada en la página (comprobar antes de redistribuir).
- **Sesgos y cautelas:** Sin proyecciones de oferta todavía; resultados muy sensibles al escenario.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-03 (búsqueda web: «IEA Critical Minerals Data Explorer Global Critical Minerals Outlook 2025 ENTSO-E Transparency Platform»; WebFetch: sí)
- **Origen:** Alta F9 Bloque B (2026-11-03).

#### RF-0060 · Q 82 (A) — International Energy Agency (IEA)

- **Canal oficial (URL raíz):** https://www.iea.org/
- **Emisor:** International Energy Agency (IEA)
- **Documentación y notas:** URL raíz confirmada en la lista de organizaciones socias de JODI. Las piezas (Oil Market Report, World Energy Outlook) no se han leído (sitio no accesible con la herramienta).
- **Temática:** TFB-12 Materias primas y energía (principal) · secundarias: TFB-17
- **Calidad Q:** 82 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 7/10
- **Tipología:** primaria
- **Acceso:** Parcialmente abierto
- **Ámbitos:** Oil Market Report, World Energy Outlook, transición energética
- **Motivo de inclusión y uso:** Referencia global de oferta y demanda de energía y escenarios.
- **Uso en el bloque:** AG-B04, AG-B05 y AG-B13: informes de mercado y escenarios energéticos (WEO, petróleo, gas, electricidad, renovables).
- **Restricciones de uso:** Condiciones de la IEA (parte de los datos con licencia).
- **Sesgos y cautelas:** Escenarios con supuestos de política; parte de pago.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «JODI Oil World Database partner organisations APEC Eurostat GECF IEA OPEC»; URL tomada de la página de socios de JODI leída con WebFetch; WebFetch al sitio: no)
- **Alerta:** REPARAR en el próximo barrido: registrar URL de las piezas OMR y WEO.
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0063 · Q 82 (A) — LBMA — precios y estadísticas de metales preciosos

- **Canal oficial (URL raíz):** https://www.lbma.org.uk/prices-and-data/london-vault-data
- **Emisor:** London Bullion Market Association (LBMA)
- **Documentación y notas:** Sección Prices & Data: LBMA Gold/Silver/Platinum/Palladium Price, datos diarios de negociación (trade reporting), compensación, origen por país, encuesta anual de previsiones. Datos de cámaras de Londres mensuales (5.º día hábil, mes vencido): fin de septiembre de 2026, 9.821 t de oro y 28.985 t de plata.
- **Temática:** TFB-12 Materias primas y energía (principal) · secundarias: —
- **Calidad Q:** 82 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 14/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (parcial); precios de referencia con licencia
- **Ámbitos:** Precios de referencia de metales preciosos; existencias en Londres; volúmenes negociados
- **Motivo de inclusión y uso:** Referencia oficial del mercado de lingotes y de existencias físicas.
- **Uso en el bloque:** AG-B05 y AG-B09: precios de referencia de oro, plata, platino y paladio para el sector minero de metales preciosos.
- **Restricciones de uso:** Licencia para uso de precios; citar mes de datos.
- **Sesgos y cautelas:** La página mostraba una cifra de metadatos (US$430 000 M) incoherente con el cuerpo (US$1,3 billones): usar el cuerpo/tabla.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «LBMA Gold Price LBMA Silver Price London vault holdings data»; WebFetch: sí)
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0065 · Q 82 (A) — London Metal Exchange (LME)

- **Canal oficial (URL raíz):** https://www.lme.com/market-data
- **Emisor:** London Metal Exchange (grupo HKEX)
- **Documentación y notas:** Precios de referencia diarios (LME Official y Closing Prices), informes de almacenes y existencias (lme.com/market-data/reports-and-data/warehouse-and-stocks-reports), volumen e interés abierto; datos en tiempo real, diferidos o históricos vía LMElive, LMEsource y distribuidores con licencia; Benchmark Statement de precios oficiales publicada.
- **Temática:** TFB-12 Materias primas y energía (principal) · secundarias: —
- **Calidad Q:** 82 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 14/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Parcial (informes públicos; datos detallados y tiempo real con licencia)
- **Ámbitos:** Precios, inventarios y actividad de metales industriales
- **Motivo de inclusión y uso:** Inventarios y estructura de curva de metales básicos.
- **Uso en el bloque:** AG-B05 y AG-B09: precios e inventarios de metales básicos (cobre, aluminio, níquel, zinc) para minería e industria.
- **Restricciones de uso:** Licencia de datos de mercado de la LME.
- **Sesgos y cautelas:** Datos detallados de pago; la página no aclara qué conjuntos son gratuitos.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «London Metal Exchange LME official prices stocks warehouse reports»; WebFetch: sí)
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0353 · Q 80 (A) — Ember — datos de electricidad

- **Canal oficial (URL raíz):** https://ember-energy.org/data/electricity-data-explorer/
- **Emisor:** Ember Energy Research CIC (think tank energético)
- **Documentación y notas:** Generación, capacidad, emisiones y demanda eléctrica de 215 países (anual para 91 países, ~93 % de la demanda; mensual para 88); actualización mensual o quincenal (última vista 30/10/2026); licencia CC BY 4.0.
- **Temática:** TFB-12 Materias primas y energía (principal) · secundarias: TFB-17
- **Calidad Q:** 80 (A) — Primariedad 16/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 13/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** secundaria
- **Acceso:** Abierto (CC BY 4.0)
- **Ámbitos:** Mix eléctrico, emisiones del sector eléctrico, demanda
- **Motivo de inclusión y uso:** Datos mensuales de transición energética (solar, eólica, carbón).
- **Uso en el bloque:** AG-B04 y AG-B05: generación y mix eléctrico por país para utilities y renovables.
- **Restricciones de uso:** Atribución CC BY 4.0; citar país y mes.
- **Sesgos y cautelas:** Organización con misión de transición (posible sesgo de enfoque).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Ember electricity data explorer»; WebFetch: sí)
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0064 · Q 77 (B) — World Gold Council

- **Canal oficial (URL raíz):** https://gold.org/goldhub/research/central-banks
- **Emisor:** World Gold Council (WGC)
- **Documentación y notas:** Goldhub: estadísticas mensuales de reservas de oro de bancos centrales (última vista: agosto de 2026), Gold Demand Trends trimestral (último visto: 2T 2026), datos de precios y primas; las notas «Gold Focus» tratan flujos de ETF (gold.org/goldhub/gold-focus/…). Invest.gold para particulares.
- **Temática:** TFB-12 Materias primas y energía (principal) · secundarias: —
- **Calidad Q:** 77 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 14/15 · Independencia 6/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** secundaria
- **Acceso:** Abierto (algunas descargas con registro)
- **Ámbitos:** Demanda de oro por segmento; compras de bancos centrales; flujos de ETF
- **Motivo de inclusión y uso:** Datos de demanda y flujos de oro.
- **Uso en el bloque:** AG-B04: demanda de oro por sector (joyería, tecnología, bancos centrales, ETF) para el subsector aurífero.
- **Restricciones de uso:** Condiciones de Goldhub; citar informe y trimestre.
- **Sesgos y cautelas:** Asociación financiada por mineras (sesgo promocional).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «World Gold Council Gold Demand Trends Goldhub gold ETF flows central banks»; WebFetch: sí)
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0309 · Q 73 (B) — International Energy Forum (IEF)

- **Canal oficial (URL raíz):** https://www.ief.org/
- **Emisor:** International Energy Forum (IEF)
- **Documentación y notas:** Coordinador de JODI (según jodidata.org) y foro de productores y consumidores; publica materiales sobre JODI (p. ej., FAQ y reuniones de jefes de organizaciones socias en ief.org).
- **Temática:** TFB-12 Materias primas y energía (principal) · secundarias: —
- **Calidad Q:** 73 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 13/15 · Independencia 9/10 · Actualidad 7/10 · Acceso 8/10
- **Tipología:** secundaria
- **Acceso:** Abierto
- **Ámbitos:** Diálogo productor-consumidor; transparencia de datos energéticos
- **Motivo de inclusión y uso:** Contexto institucional de JODI y comparativas de perspectivas energéticas.
- **Uso en el bloque:** AG-B05 y AG-B07: diálogo productores-consumidores y datos de mercado petrolero.
- **Restricciones de uso:** Citar documento y fecha.
- **Sesgos y cautelas:** Foro intergubernamental (lenguaje de consenso); productos de datos vía JODI (RF-0308): no duplicar raíz.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «JODI Oil World Database partner organisations APEC Eurostat GECF IEA OPEC» —ief.org en resultados y en la lista de socios de JODI—; WebFetch al sitio: no)
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0357 · Q 70 (B) — Our World in Data — energía

- **Canal oficial (URL raíz):** https://ourworldindata.org/grapher/installed-solar-PV-capacity?tab=map
- **Emisor:** Global Change Data Lab (con la Universidad de Oxford)
- **Documentación y notas:** Gráficos y datos reprocesados con atribución explícita a la fuente original (p. ej., IRENA 2026); licencia CC BY 4.0 para lo propio; fecha de actualización y próxima actualización visibles (28/07/2026 y 28/07/2027).
- **Temática:** TFB-12 Materias primas y energía (principal) · secundarias: TFB-17
- **Calidad Q:** 70 (B) — Primariedad 8/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 12/15 · Independencia 9/10 · Actualidad 7/10 · Acceso 10/10
- **Tipología:** terciaria (agregador)
- **Acceso:** Abierto (CC BY 4.0)
- **Ámbitos:** Series energéticas y de emisiones armonizadas
- **Motivo de inclusión y uso:** Acceso rápido y documentado a series de terceros; citar siempre la fuente original.
- **Uso en el bloque:** AG-B04 y AG-B13: series largas y comparables de energía para dimensionar transiciones.
- **Restricciones de uso:** Citar la fuente original indicada en cada gráfico.
- **Sesgos y cautelas:** No es fuente primaria; actualización anual.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «IRENA Renewable Capacity Statistics 2026»; WebFetch: sí)
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0310 · Q 69 (B) — Gas Exporting Countries Forum (GECF)

- **Canal oficial (URL raíz):** https://www.gecf.org/
- **Emisor:** Gas Exporting Countries Forum (GECF)
- **Documentación y notas:** Organización socia de JODI (JODI-Gas) según jodidata.org; foro de países exportadores de gas.
- **Temática:** TFB-12 Materias primas y energía (principal) · secundarias: —
- **Calidad Q:** 69 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 12/15 · Independencia 5/10 · Actualidad 8/10 · Acceso 8/10
- **Tipología:** secundaria
- **Acceso:** Abierto (parcial)
- **Ámbitos:** Mercado mundial de gas natural y GNL desde la óptica de los exportadores
- **Motivo de inclusión y uso:** Contraste de la visión de productores de gas frente a IEA/EIA.
- **Uso en el bloque:** AG-B05: oferta y comercio de gas natural y GNL (visión de productores).
- **Restricciones de uso:** Citar publicación y fecha.
- **Sesgos y cautelas:** Parte interesada (exportadores). Publicaciones concretas no leídas: confirmar en el próximo barrido.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «JODI Oil World Database partner organisations APEC Eurostat GECF IEA OPEC»; URL tomada de la página de socios de JODI leída con WebFetch; WebFetch al sitio: no)
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

#### RF-0311 · Q 69 (B) — OLADE — Organización Latinoamericana de Energía

- **Canal oficial (URL raíz):** https://www.olade.org/
- **Emisor:** Organización Latinoamericana de Energía (OLADE)
- **Documentación y notas:** Organización socia de JODI para América Latina y el Caribe (lista de socios de jodidata.org; olade.org aparece en resultados de búsqueda sobre JODI).
- **Temática:** TFB-12 Materias primas y energía (principal) · secundarias: —
- **Calidad Q:** 69 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 12/15 · Independencia 8/10 · Actualidad 6/10 · Acceso 7/10
- **Tipología:** secundaria
- **Acceso:** Abierto (parcial)
- **Ámbitos:** Estadística energética regional de América Latina y el Caribe
- **Motivo de inclusión y uso:** Diversidad geográfica en balances energéticos (región relevante para empresas españolas).
- **Uso en el bloque:** AG-B05: estadísticas energéticas de Latinoamérica y el Caribe.
- **Restricciones de uso:** Citar publicación y año.
- **Sesgos y cautelas:** Productos concretos no leídos: confirmar en el próximo barrido.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «JODI Oil World Database partner organisations APEC Eurostat GECF IEA OPEC»; WebFetch al sitio: no)
- **Reutilización:** ficha del Bloque A V3.2 (F9) reutilizada en el Bloque B V2.0 con su ID original (2026-11-03).

## TFB-13 Inmobiliario e infraestructuras

#### RF-0313 · Q 89 (A) — FHFA — House Price Index

- **Canal oficial (URL raíz):** https://www.fhfa.gov/taxonomy/term/301
- **Emisor:** Federal Housing Finance Agency (FHFA)
- **Documentación y notas:** Índice de ventas repetidas ponderado de viviendas unifamiliares desde mediados de los setenta (nacional, división censal, estado, metro, condado, código postal, sección censal); informes mensuales (última semana del mes; último visto: 27/10/2026) y trimestrales (finales de feb., may., ago., nov.).
- **Temática:** TFB-13 Inmobiliario e infraestructuras (principal) · secundarias: TFB-01
- **Calidad Q:** 89 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto (dominio público)
- **Ámbitos:** Precios de vivienda en EE. UU. (hipotecas conformes)
- **Motivo de inclusión y uso:** Índice oficial de precios de vivienda de EE. UU., contraste del Case-Shiller (RF-0071). **Uso en el Bloque B:** AG-B04 y AG-B08 (ciclo de precios de vivienda en EE. UU. para promotoras, materiales y REIT residenciales), MC-B05 (betas sectoriales al ciclo inmobiliario).
- **Restricciones de uso:** Uso libre; citar versión (purchase-only o all-transactions) y periodo.
- **Sesgos y cautelas:** Cobertura limitada a préstamos de Fannie Mae/Freddie Mac; revisiones.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «FHFA House Price Index Freddie Mac Primary Mortgage Market Survey NAHB Housing Market Index NAR existing-home sales»; WebFetch: sí)
- **Origen:** Reutilizada del Bloque A (ID original) en F9 Bloque B (TFB-13) el 2026-11-02.

#### RF-0360 · Q 89 (A) — U.S. Census Bureau / HUD — New Residential Construction

- **Canal oficial (URL raíz):** https://www.census.gov/construction/nrc/pdf/newresconst_202609.pdf
- **Emisor:** U.S. Census Bureau y U.S. Department of Housing and Urban Development
- **Documentación y notas:** Publicación mensual conjunta (8:30 ET) de viviendas iniciadas, permisos y terminadas: septiembre de 2026, 1.221.000 iniciadas y 1.400.000 permisos (tasa anual desestacionalizada), publicada 20/10/2026; siguiente 18/11/2026.
- **Temática:** TFB-13 Inmobiliario e infraestructuras (principal) · secundarias: TFB-01
- **Calidad Q:** 89 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto (dominio público)
- **Ámbitos:** Construcción residencial en EE. UU.
- **Motivo de inclusión y uso:** Dato oficial adelantado de la actividad inmobiliaria. **Uso en el Bloque B:** AG-B04 y AG-B05 (indicador adelantado de demanda para constructoras, materiales y equipamiento), MC-B01 (series y estacionalidad).
- **Restricciones de uso:** Uso libre; citar mes y revisión.
- **Sesgos y cautelas:** Márgenes de error amplios; revisiones.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Census Bureau New Residential Construction housing starts building permits release»; WebFetch: sí)
- **Origen:** Reutilizada del Bloque A (ID original) en F9 Bloque B (TFB-13) el 2026-11-02.

#### RF-0070 · Q 88 (A) — BIS — precios de la vivienda residencial

- **Canal oficial (URL raíz):** https://data.bis.org/topics/RPP
- **Emisor:** Bank for International Settlements (BIS)
- **Documentación y notas:** Dos conjuntos: «Selected» (un indicador por país, nominal y real) y «Detailed» (más de 300 series de unos 60 países); series retrotraídas a ~1970 en 23 países. Actualización mensual (última semana): última 29/10/2026, próxima 26/11/2026. Documentación en bis.org/pages/statistics/pp-documentation.pdf; notas de publicación trimestrales.
- **Temática:** TFB-13 Inmobiliario e infraestructuras (principal) · secundarias: TFB-02
- **Calidad Q:** 88 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Precios de vivienda por país, series largas
- **Motivo de inclusión y uso:** Base comparada internacional de precios de vivienda. **Uso en el Bloque B:** AG-B08 (comparación internacional del ciclo inmobiliario por país), AG-B12 (contexto de REIT/SOCIMI por mercado) y MC-B05.
- **Restricciones de uso:** Uso con atribución; citar conjunto, país y fecha de extracción.
- **Sesgos y cautelas:** Métodos nacionales heterogéneos (usar «Selected» para comparar).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Migración del portal de bis.org/statistics/pp.htm a data.bis.org.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «BIS residential property price statistics data.bis.org»; WebFetch: sí)
- **Origen:** Reutilizada del Bloque A (ID original) en F9 Bloque B (TFB-13) el 2026-11-02.

#### RF-0072 · Q 88 (A) — INE — Índice de Precios de Vivienda y estadísticas inmobiliarias

- **Canal oficial (URL raíz):** https://www.ine.es/htdocs/prensa/ipv_prensa.htm
- **Emisor:** Instituto Nacional de Estadística (INE)
- **Documentación y notas:** Página de prensa del IPV con último dato y enlace al calendario del INE; metadatos de la operación en ine.es/dynt3/metadatos/es/RespuestaDatos.html?oper=15; metodología 2025 (ine.es/daco/daco42/ipv/metodologia2025.pdf).
- **Temática:** TFB-13 Inmobiliario e infraestructuras (principal) · secundarias: TFB-01
- **Calidad Q:** 88 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Precios de vivienda libre (nueva y de segunda mano) en España
- **Motivo de inclusión y uso:** Fuente estadística oficial de España. **Uso en el Bloque B:** AG-B04 y AG-B08 (ciclo inmobiliario español para SOCIMI, promotoras y bancos), AG-B12 (contexto de candidatos españoles).
- **Restricciones de uso:** Uso libre con atribución; citar trimestre y base.
- **Sesgos y cautelas:** Frecuencia trimestral. En la lectura, la página de prensa mostraba como último dato el 3T 2025 (+12,8 % anual), lo que parece desfasado: confirmar el último dato en INEbase o en el calendario.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Nueva metodología 2025 publicada.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «INE Índice de Precios de Vivienda IPV último dato Registradores Notariado Banco de España indicadores mercado vivienda»; WebFetch: sí)
- **Origen:** Reutilizada del Bloque A (ID original) en F9 Bloque B (TFB-13) el 2026-11-02.

#### RF-0331 · Q 88 (A) — ONS / HM Land Registry — UK House Price Index

- **Canal oficial (URL raíz):** https://www.ons.gov.uk/releases/ukhousepriceindexnovember2023
- **Emisor:** Office for National Statistics (datos de HM Land Registry, Registers of Scotland y Land and Property Services NI)
- **Documentación y notas:** Índice oficial mensual de precios de vivienda del Reino Unido; boletines en ons.gov.uk/economy/inflationandpriceindices/bulletins/housepriceindex/.
- **Temática:** TFB-13 Inmobiliario e infraestructuras (principal) · secundarias: TFB-01
- **Calidad Q:** 88 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Precios de vivienda en el Reino Unido por nación y región
- **Motivo de inclusión y uso:** Fuente oficial británica de precios de vivienda. **Uso en el Bloque B:** AG-B08 (ciclo de vivienda del Reino Unido para REIT y constructoras británicas), MC-B01.
- **Restricciones de uso:** Licencia de datos abiertos del Gobierno británico; citar mes.
- **Sesgos y cautelas:** Desfase de dos meses por el registro de transacciones; revisiones.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «HM Land Registry UK House Price Index monthly release gov.uk»; WebFetch: sí)
- **Origen:** Reutilizada del Bloque A (ID original) en F9 Bloque B (TFB-13) el 2026-11-02.

#### RF-0330 · Q 86 (A) — Federal Reserve Bank of Dallas — International House Price Database

- **Canal oficial (URL raíz):** https://www.dallasfed.org/institute/houseprice
- **Emisor:** Federal Reserve Bank of Dallas (Globalization Institute)
- **Documentación y notas:** Panel trimestral desde 1975 de 26 países (incluida España): índice de precios nominal y real, renta disponible per cápita nominal y real; indicadores de exuberancia (pruebas SADF/GSADF, Pavlidis et al., 2016); última versión 2T 2026 (publicada 09/10/2026).
- **Temática:** TFB-13 Inmobiliario e infraestructuras (principal) · secundarias: TFB-02
- **Calidad Q:** 86 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Precios reales de vivienda y ratio precio/renta comparados; detección de burbujas
- **Motivo de inclusión y uso:** Base homogénea para valoración relativa de la vivienda y señales de exuberancia. **Uso en el Bloque B:** AG-B08 y MC-B05 (panel internacional homogéneo de precios y alquileres; sobrevaloración relativa por país), AG-B14 (tesis contrarias de burbuja).
- **Restricciones de uso:** Uso con atribución; citar versión trimestral.
- **Sesgos y cautelas:** Algunos datos recientes son previsiones que se sustituyen en revisiones posteriores.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Dallas Fed International House Price Database»; WebFetch: sí)
- **Origen:** Reutilizada del Bloque A (ID original) en F9 Bloque B (TFB-13) el 2026-11-02.

#### RF-0327 · Q 85 (A) — Freddie Mac — Primary Mortgage Market Survey (PMMS)

- **Canal oficial (URL raíz):** https://freddiemac.gcs-web.com/node/32031/pdf
- **Emisor:** Freddie Mac
- **Documentación y notas:** Encuesta semanal de tipos hipotecarios (prestamistas encuestados de lunes a miércoles; publicación los jueves a las 10:00 ET). Nota leída: 03/09/2026 (30 años 6,71 %; 15 años 6,04 %). Según Mortgage News Daily, el 29/10/2026 el tipo a 30 años era del 7,24 %.
- **Temática:** TFB-13 Inmobiliario e infraestructuras (principal) · secundarias: TFB-02
- **Calidad Q:** 85 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Tipos hipotecarios fijos a 30 y 15 años en EE. UU.
- **Motivo de inclusión y uso:** Coste de financiación de la vivienda; insumo de asequibilidad. **Uso en el Bloque B:** AG-B08 (coste de financiación hipotecaria y asequibilidad), AG-B09 (sensibilidad de promotoras y REIT a tipos).
- **Restricciones de uso:** Citar semana y plazo.
- **Sesgos y cautelas:** Tipos de préstamos conformes de primera calidad; entidad patrocinada por el Gobierno.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Freddie Mac Primary Mortgage Market Survey weekly mortgage rates»; WebFetch: sí)
- **Origen:** Reutilizada del Bloque A (ID original) en F9 Bloque B (TFB-13) el 2026-11-02.

#### RF-0314 · Q 83 (A) — Consejo General del Notariado — Portal Estadístico del Notariado

- **Canal oficial (URL raíz):** https://www.penotariado.com/
- **Emisor:** Consejo General del Notariado (desarrollado por CTNotariado)
- **Documentación y notas:** Portal gratuito con precios reales de compraventa (€/m²) a partir de escrituras anonimizadas, por comunidad, provincia, municipio y código postal; número de compraventas, tipo de vivienda, edad y nacionalidad de compradores, esfuerzo en años de renta; histórico de 12 años; actualización mensual. Lanzado el 23/10/2025 (según Vozpópuli, 28/10/2026).
- **Temática:** TFB-13 Inmobiliario e infraestructuras (principal) · secundarias: TFB-01
- **Calidad Q:** 83 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 14/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Precios de transacción y compraventas de vivienda en España, con granularidad local
- **Motivo de inclusión y uso:** Precios efectivos de escritura (no tasación ni oferta) para contrastar INE, tasadoras y portales. **Uso en el Bloque B:** AG-B04 (compraventas y precios notariales en España por zona), AG-B12 (SOCIMI y promotoras españolas).
- **Restricciones de uso:** Citar ámbito geográfico y mes.
- **Sesgos y cautelas:** Fuente colegial; URL obtenida de prensa: confirmar en el próximo barrido.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Portal nuevo (2025).
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Estadística Registral Inmobiliaria Registradores portal estadístico Notariado Tinsa IMIE valor tasado vivienda Ministerio»; URL tomada del artículo de Vozpópuli leído con WebFetch; WebFetch al sitio: no)
- **Origen:** Reutilizada del Bloque A (ID original) en F9 Bloque B (TFB-13) el 2026-11-02.

#### RF-0328 · Q 81 (A) — NAHB/Wells Fargo — Housing Market Index (HMI)

- **Canal oficial (URL raíz):** https://www.nahb.org/hmi
- **Emisor:** National Association of Home Builders (con Wells Fargo)
- **Documentación y notas:** Confianza de los constructores de vivienda unifamiliar (0–100) con ventas actuales (peso 0,5920), ventas esperadas (0,1358) y visitas de compradores (0,2722); mensual; octubre de 2026: 29 (−3), con el 43 % de constructores rebajando precios.
- **Temática:** TFB-13 Inmobiliario e infraestructuras (principal) · secundarias: TFB-10
- **Calidad Q:** 81 (A) — Primariedad 17/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 13/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Confianza y condiciones del mercado de vivienda nueva en EE. UU.
- **Motivo de inclusión y uso:** Indicador adelantado de construcción residencial. **Uso en el Bloque B:** AG-B10 (sentimiento de constructores de vivienda), AG-B13 (señal adelantada del ciclo de construcción residencial).
- **Restricciones de uso:** Citar mes y componente.
- **Sesgos y cautelas:** Asociación sectorial; encuesta de opinión.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Panel renovado anualmente.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «NAHB Wells Fargo Housing Market Index builder confidence»; WebFetch: sí)
- **Origen:** Reutilizada del Bloque A (ID original) en F9 Bloque B (TFB-13) el 2026-11-02.

#### RF-0071 · Q 80 (A) — S&P Cotality Case-Shiller Home Price Indices (antes S&P CoreLogic Case-Shiller)

- **Canal oficial (URL raíz):** https://www.spglobal.com/spdji/en/index-announcements/article/sp-cotality-case-shiller-index-reports-annual-gain-in-august-2026/
- **Emisor:** S&P Dow Jones Indices (con Cotality, antes CoreLogic)
- **Documentación y notas:** Anuncios mensuales «S&P Cotality Case-Shiller Index Reports…» en spglobal.com/spdji/en/index-announcements/ (último visto en resultados: datos de agosto de 2026). Series en FRED: CSUSHPINSA y CSUSHPISA.
- **Temática:** TFB-13 Inmobiliario e infraestructuras (principal) · secundarias: TFB-06
- **Calidad Q:** 80 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 14/15 · Independencia 8/10 · Actualidad 8/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (parcial)
- **Ámbitos:** Precios de vivienda en EE. UU. por ventas repetidas (nacional, 20 y 10 ciudades)
- **Motivo de inclusión y uso:** Índice de referencia de vivienda en EE. UU. **Uso en el Bloque B:** AG-B08 y MC-B05 (índice de referencia de precios de vivienda de EE. UU.), AG-B14.
- **Restricciones de uso:** Condiciones de S&P DJI; citar mes de datos y serie (SA/NSA).
- **Sesgos y cautelas:** Desfase de dos meses.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Cambio de nombre: CoreLogic → Cotality (el índice pasa a «S&P Cotality Case-Shiller»).
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «S&P Cotality Case-Shiller U.S. National Home Price NSA Index»; WebFetch: intentado, error del sitio)
- **Origen:** Reutilizada del Bloque A (ID original) en F9 Bloque B (TFB-13) el 2026-11-02.

#### RF-0363 · Q 80 (A) — RICS — UK Residential Market Survey

- **Canal oficial (URL raíz):** https://www.rics.org/news-insights/uk-residential-survey-may-2026
- **Emisor:** Royal Institution of Chartered Surveyors (RICS)
- **Documentación y notas:** Encuesta mensual a tasadores con balances netos de precios, consultas de compradores, ventas y expectativas; mayo de 2026: balance de precios −35 % y nuevas consultas −34 %. PDF mensuales en rics.org/content/dam/ricsglobal/documents/market-surveys/.
- **Temática:** TFB-13 Inmobiliario e infraestructuras (principal) · secundarias: TFB-10
- **Calidad Q:** 80 (A) — Primariedad 16/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 14/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Sentimiento y condiciones del mercado de vivienda británico
- **Motivo de inclusión y uso:** Indicador adelantado de precios de vivienda del Reino Unido. **Uso en el Bloque B:** AG-B10 y AG-B13 (expectativas de agentes inmobiliarios británicos), AG-B08.
- **Restricciones de uso:** Citar mes y balance.
- **Sesgos y cautelas:** Encuesta de opinión; organismo profesional.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «RICS UK Residential Market Survey»; WebFetch: sí)
- **Origen:** Reutilizada del Bloque A (ID original) en F9 Bloque B (TFB-13) el 2026-11-02.

#### RF-0068 · Q 79 (B) — Nareit

- **Canal oficial (URL raíz):** https://reit.com/data-research/reit-indexes/real-time-index-returns
- **Emisor:** National Association of Real Estate Investment Trusts (Nareit)
- **Documentación y notas:** Rentabilidades en tiempo real de la serie FTSE Nareit U.S. Real Estate (total y por sector: industrial, oficinas, comercial, residencial, salud, centros de datos, hipotecarios) y del FTSE EPRA Nareit Global Real Estate Index (por región).
- **Temática:** TFB-13 Inmobiliario e infraestructuras (principal) · secundarias: TFB-08
- **Calidad Q:** 79 (B) — Primariedad 17/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 14/15 · Independencia 7/10 · Actualidad 8/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Rentabilidades, valoraciones y datos de REIT estadounidenses
- **Motivo de inclusión y uso:** Datos sectoriales del inmobiliario cotizado de EE. UU. **Uso en el Bloque B:** AG-B09 y AG-B12 (universo, índices FTSE Nareit, rentabilidad y valoración de REIT de EE. UU. por segmento: centros de datos, logística, torres, residencial), MC-B06 (múltiplos FFO/AFFO).
- **Restricciones de uso:** Citar índice y fecha/hora.
- **Sesgos y cautelas:** Asociación sectorial (sesgo promocional); marcas de tiempo distintas entre índices.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «FTSE EPRA Nareit Global Real Estate Index Series EPRA Nareit REIT data»; WebFetch: sí)
- **Origen:** Reutilizada del Bloque A (ID original) en F9 Bloque B (TFB-13) el 2026-11-02.

#### RF-0361 · Q 77 (B) — National Association of Realtors — Existing-Home Sales

- **Canal oficial (URL raíz):** https://nar.realtor/node/156145
- **Emisor:** National Association of Realtors (NAR)
- **Documentación y notas:** Encuesta mensual de ventas de vivienda usada a partir de datos de asociaciones locales y MLS (los datos recibidos antes del día 15 entran en la publicación principal); calendario de publicaciones estadísticas de NAR. La página leída es la de ampliación de la encuesta, no una nota de cifras.
- **Temática:** TFB-13 Inmobiliario e infraestructuras (principal) · secundarias: TFB-04
- **Calidad Q:** 77 (B) — Primariedad 18/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 14/15 · Independencia 6/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto (titulares)
- **Ámbitos:** Ventas, precio mediano e inventario de vivienda usada en EE. UU.
- **Motivo de inclusión y uso:** Indicador mensual del mercado de reventa (aprox. 90 % de las transacciones). **Uso en el Bloque B:** AG-B04 (volumen de transacciones y existencias de vivienda usada), AG-B08.
- **Restricciones de uso:** Citar mes y revisión.
- **Sesgos y cautelas:** Asociación de agentes (sesgo promocional); revisiones de referencia.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «NAR existing-home sales monthly report National Association of Realtors»; WebFetch: sí)
- **Origen:** Reutilizada del Bloque A (ID original) en F9 Bloque B (TFB-13) el 2026-11-02.

#### RF-0402 · Q 77 (B) — NCREIF — NCREIF Property Index (NPI)

- **Canal oficial (URL raíz):** https://user.ncreif.org/data-products/property/
- **Emisor:** National Council of Real Estate Investment Fiduciaries (NCREIF)
- **Temática:** TFB-13 Inmobiliario e infraestructuras (principal) · secundarias: TFB-08
- **Calidad Q:** 77 (B) — Primariedad 18/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 14/15 · Independencia 7/10 · Actualidad 8/10 · Acceso 7/10
- **Tipología:** primaria (índice construido con datos de propiedades de los miembros)
- **Acceso:** Muro parcial (rentabilidades trimestrales abiertas; desgloses y apalancadas para miembros)
- **Ámbitos:** Rentabilidad trimestral sin apalancar del inmobiliario privado institucional de EE. UU. (oficinas, residencial, industrial, retail, hoteles) desde 4T1977; desglose geográfico
- **Motivo de inclusión y uso:** Referencia histórica del inmobiliario privado (no cotizado) en EE. UU.; comparación con REIT (RF-0068). **Uso en el Bloque B:** AG-B09 y MC-B06 (rentabilidades del inmobiliario privado institucional por tipo de inmueble: oficinas, logística, retail, residencial), AG-B14 (desfase de tasaciones frente a REIT cotizados).
- **Sesgos y cautelas:** Basado en tasaciones (suavizado y retraso frente a precios de transacción); índice congelado desde 1T2003 salvo correcciones; asociación del sector.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «NCREIF Property Index NPI quarterly returns»; WebFetch: sí)
- **Origen:** Alta F9_S3 (2026-11-02). Reutilizada en F9 Bloque B (TFB-13) el 2026-11-02.

#### RF-0069 · Q 76 (B) — EPRA

- **Canal oficial (URL raíz):** https://epra.com/indexes/index-data
- **Emisor:** European Public Real Estate Association (EPRA)
- **Documentación y notas:** Panel de datos del índice global (capitalización, rentabilidades, sectores, constituyentes) **solo para miembros de pleno derecho**; informes mensuales en la sección Research; boletines estadísticos mensuales históricos (prodapp.epra.com/media/…). Metodología del índice en LSEG (ftse-epra-nareit-global-real-estate-index-series-methodology-overview.pdf).
- **Temática:** TFB-13 Inmobiliario e infraestructuras (principal) · secundarias: TFB-08
- **Calidad Q:** 76 (B) — Primariedad 17/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 14/15 · Independencia 7/10 · Actualidad 8/10 · Acceso 6/10
- **Tipología:** primaria
- **Acceso:** Restringido (datos de índice para miembros); informes públicos parciales
- **Ámbitos:** Índices FTSE EPRA Nareit, NAV, mejores prácticas contables (EPRA NTA)
- **Motivo de inclusión y uso:** Inmobiliario cotizado europeo y métricas estándar. **Uso en el Bloque B:** AG-B09 y AG-B12 (universo de inmobiliarias cotizadas europeas, índices FTSE EPRA Nareit, NAV y métricas EPRA para comparar SOCIMI y REIT), MC-B06.
- **Restricciones de uso:** Solo contenidos públicos citables.
- **Sesgos y cautelas:** Asociación sectorial; Acceso rebajado de 9 a 6 por la restricción a miembros (Q provisional 79 → 76).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «FTSE EPRA Nareit Global Real Estate Index Series EPRA Nareit REIT data»; WebFetch: sí)
- **Origen:** Reutilizada del Bloque A (ID original) en F9 Bloque B (TFB-13) el 2026-11-02.

#### RF-0329 · Q 76 (B) — Colegio de Registradores — Estadística Registral Inmobiliaria (ERI)

- **Canal oficial (URL raíz):** https://datos.gob.es/es/catalogo/a16003011-estadistica-registral-inmobiliaria-20221
- **Emisor:** Colegio de Registradores de la Propiedad y Mercantiles de España (estadística ERI; ficha en el catálogo nacional datos.gob.es)
- **Documentación y notas:** La ERI figura en el catálogo de datos abiertos datos.gob.es con ediciones anuales (2020, 2022, 2025); Euskadi publica una estadística registral derivada con metodología propia. Precios, compraventas e hipotecas según inscripciones registrales.
- **Temática:** TFB-13 Inmobiliario e infraestructuras (principal) · secundarias: TFB-01
- **Calidad Q:** 76 (B) — Primariedad 18/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 14/15 · Independencia 8/10 · Actualidad 7/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Compraventas, precios e hipotecas de vivienda en España por inscripción registral
- **Motivo de inclusión y uso:** Contraste registral de los precios notariales (RF-0314) y del INE (RF-0072). **Uso en el Bloque B:** AG-B04 (transacciones, hipotecas y precios registrales en España), AG-B03 (compradores extranjeros, segmentos).
- **Restricciones de uso:** Citar edición y trimestre.
- **Sesgos y cautelas:** Editor de la ficha del catálogo no leído (la página dio error): confirmar en el próximo barrido.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Colegio de Registradores Estadística Registral Inmobiliaria ERI trimestral»; WebFetch: intentado, error del sitio)
- **Origen:** Reutilizada del Bloque A (ID original) en F9 Bloque B (TFB-13) el 2026-11-02.

#### RF-0332 · Q 76 (B) — Zillow Research — datos de vivienda (ZHVI, ZORI)

- **Canal oficial (URL raíz):** https://www.zillow.com/research/data/
- **Emisor:** Zillow Group (Zillow Research)
- **Documentación y notas:** Descargas CSV gratuitas: ZHVI (valor típico, percentiles 35–65), ZORI (alquiler observado de repetición), previsiones, inventario, ventas, días en mercado, rebajas, Market Heat Index, obra nueva y asequibilidad; metodologías publicadas (neural ZHVI, ZORI); calendario de publicación.
- **Temática:** TFB-13 Inmobiliario e infraestructuras (principal) · secundarias: TFB-04
- **Calidad Q:** 76 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 12/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** secundaria
- **Acceso:** Abierto (licencia no declarada en la página)
- **Ámbitos:** Valores y alquileres de vivienda en EE. UU. con gran detalle geográfico
- **Motivo de inclusión y uso:** Alquileres y precios de alta frecuencia (útil para la inflación de vivienda). **Uso en el Bloque B:** AG-B04 (precios y alquileres de vivienda en EE. UU. a nivel metro, útil para REIT residenciales y single-family rental), MC-B01.
- **Restricciones de uso:** Citar serie y fecha de descarga; seguir la guía de cita de ZHVI.
- **Sesgos y cautelas:** Modelo propio (valoración automática); portal inmobiliario comercial.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Cambios de metodología documentados (p. ej., obra nueva desde 08/2025).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Zillow Research data ZHVI ZORI home value rent index»; WebFetch: sí)
- **Origen:** Reutilizada del Bloque A (ID original) en F9 Bloque B (TFB-13) el 2026-11-02.

#### RF-0312 · Q 75 (B) — Tinsa — IMIE (Mercados Locales y General)

- **Canal oficial (URL raíz):** https://www.tinsa.es/informes/imie-mercados-locales/imie-mercados-locales-1o-trimestre-2026-143/
- **Emisor:** Tinsa (sociedad de tasación)
- **Documentación y notas:** Valor unitario (€/m²) de vivienda libre terminada a partir de tasaciones hipotecarias (base de más de 6 millones de valoraciones, más del 25 % de las tasaciones anuales en España), por CCAA, provincia, capital, municipio y distritos de grandes ciudades; trimestral. 1T 2026: +14,3 % anual nominal (+11,8 % real). Metodología: medias móviles ponderadas estratificadas con tasaciones según normativa del Banco de España.
- **Temática:** TFB-13 Inmobiliario e infraestructuras (principal) · secundarias: TFB-04
- **Calidad Q:** 75 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 12/15 · Independencia 7/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Valor de tasación de vivienda en España con detalle local
- **Motivo de inclusión y uso:** Indicador de tasación con mayor granularidad y menor desfase que el IPV. **Uso en el Bloque B:** AG-B04 (precios de tasación por municipio en España), AG-B12 (contexto local de SOCIMI y promotoras).
- **Restricciones de uso:** Citar edición y trimestre.
- **Sesgos y cautelas:** Valor de tasación (no precio de transacción); empresa privada.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Estadística Registral Inmobiliaria Registradores portal estadístico Notariado Tinsa IMIE valor tasado vivienda Ministerio»; WebFetch: sí)
- **Origen:** Reutilizada del Bloque A (ID original) en F9 Bloque B (TFB-13) el 2026-11-02.

#### RF-0364 · Q 72 (B) — Calculated Risk — blog de vivienda y economía (Bill McBride)

- **Canal oficial (URL raíz):** https://www.calculatedriskblog.com/2018/07/chemical-activity-barometer-increased.html
- **Emisor:** Bill McBride (Calculated Risk)
- **Documentación y notas:** Blog con seguimiento diario de datos de vivienda y economía de EE. UU., gráficos propios y enlaces a la fuente primaria (p. ej., notas del ACC).
- **Temática:** TFB-13 Inmobiliario e infraestructuras (principal) · secundarias: TFB-11
- **Calidad Q:** 72 (B) — Primariedad 9/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 12/15 · Independencia 9/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** secundaria
- **Acceso:** Abierto
- **Ámbitos:** Vivienda, hipotecas y ciclo económico de EE. UU.
- **Motivo de inclusión y uso:** Pista de descubrimiento y lectura experta del dato inmobiliario; los hechos se citan en la fuente primaria que enlaza. **Uso en el Bloque B:** AG-B08 y AG-B14 (lectura experta del ciclo de vivienda y crédito en EE. UU.; opinión, no hecho).
- **Restricciones de uso:** Opinión: citar la fuente primaria.
- **Sesgos y cautelas:** Un solo autor.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin datos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «American Chemistry Council Chemical Activity Barometer»; WebFetch: sí)
- **Origen:** Reutilizada del Bloque A (ID original) en F9 Bloque B (TFB-13) el 2026-11-02.

#### RF-0451 · Q 72 (B) — EDHEC Infra & Private Assets / Scientific Infra & Private Assets (SIPA) — índices de infraestructuras y capital privado

- **Canal oficial (URL raíz):** https://www.edhec.edu/en/research-and-faculty/centres-and-chairs/edhec-infra (índices: https://edhecinfraprivateassets.com/)
- **Emisor:** EDHEC Infrastructure & Private Assets Research Institute; índices comercializados por SIPA (escisión de 2019, adquirida por PEI Group en marzo de 2026)
- **Temática:** TFB-13 Inmobiliario e infraestructuras (principal) · secundarias: TFB-08
- **Calidad Q:** 72 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 13/15 · Independencia 7/10 · Actualidad 9/10 · Acceso 4/10
- **Tipología:** secundaria (índices construidos con modelos de valoración de activos no cotizados)
- **Acceso:** Restringido (índices de pago; investigación académica abierta)
- **Ámbitos:** Índices y benchmarks de capital y deuda de infraestructuras no cotizadas y de capital privado (infraMetrics, privateMetrics); clasificaciones TICCS y PECCS; proveedor de índices registrado en ESMA
- **Motivo de inclusión y uso:** Único benchmark académico de infraestructuras no cotizadas, con valoración a precio de mercado (menos suavizado que la tasación). **Uso en el Bloque B:** AG-B09 y AG-B12 (rentabilidad y valoración de infraestructuras no cotizadas como referencia para utilities, concesionarias y fondos de infraestructuras cotizados), MC-B06.
- **Sesgos y cautelas:** Desde 2026 propiedad de PEI Group (grupo de medios y datos de mercados privados); modelos sujetos a riesgo de especificación.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «EDHECinfra Scientific Infra private infrastructure index infraMetrics»; WebFetch: sí, página de EDHEC y nota de prensa de PEI (23/03/2026))
- **Origen:** Alta F9_S3, tanda 3 (2026-11-02). Reutilizada en F9 Bloque B (TFB-13) el 2026-11-02.

#### RF-0362 · Q 69 (B) — idealista — informes de precios de vivienda

- **Canal oficial (URL raíz):** https://www.idealista.com/news/estadisticas/
- **Emisor:** idealista
- **Documentación y notas:** Informes de evolución del precio de la vivienda en venta y alquiler por comunidad, provincia, municipio y barrio; indicadores de demanda (diferencia entre precio anunciado y ofertas) y euríbor; idealista aparece como caso de éxito en datos.gob.es.
- **Temática:** TFB-13 Inmobiliario e infraestructuras (principal) · secundarias: TFB-04
- **Calidad Q:** 69 (B) — Primariedad 13/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 11/15 · Independencia 6/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** secundaria
- **Acceso:** Abierto
- **Ámbitos:** Precios de oferta de venta y alquiler en España
- **Motivo de inclusión y uso:** Indicador adelantado y granular (precios de oferta, no de cierre). **Uso en el Bloque B:** AG-B04 (precios de oferta y alquiler en España por zona, alta frecuencia), AG-B10.
- **Restricciones de uso:** Citar informe y mes; contrastar con RF-0314 y RF-0072.
- **Sesgos y cautelas:** Precios de anuncio, no de transacción; portal comercial; metodología no leída.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «idealista informe precio vivienda venta índice mensual»; WebFetch: sí)
- **Origen:** Reutilizada del Bloque A (ID original) en F9 Bloque B (TFB-13) el 2026-11-02.

#### RF-0333 · Q 66 (B) — Mortgage News Daily — índice diario de tipos hipotecarios

- **Canal oficial (URL raíz):** https://www.mortgagenewsdaily.com/mortgage-rates/freddie-mac
- **Emisor:** Mortgage News Daily, LLC
- **Documentación y notas:** Índice diario propio de tipos (30 años: 7,27 % a 30/10/2026) y reproducción del PMMS de Freddie Mac; existe una página sobre el índice diario, pero su metodología no se leyó.
- **Temática:** TFB-13 Inmobiliario e infraestructuras (principal) · secundarias: TFB-06
- **Calidad Q:** 66 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 8/15 · Autoridad 10/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** secundaria
- **Acceso:** Abierto
- **Ámbitos:** Tipos hipotecarios diarios en EE. UU.
- **Motivo de inclusión y uso:** Alta frecuencia entre publicaciones semanales del PMMS (RF-0327). **Uso en el Bloque B:** AG-B08 (tipo hipotecario diario de EE. UU. para seguimiento de alta frecuencia), AG-B09.
- **Restricciones de uso:** Citar fecha; contrastar con RF-0327.
- **Sesgos y cautelas:** Metodología no leída; medio comercial.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin datos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Freddie Mac Primary Mortgage Market Survey weekly mortgage rates»; WebFetch: sí)
- **Origen:** Reutilizada del Bloque A (ID original) en F9 Bloque B (TFB-13) el 2026-11-02.

## TFB-14 Cripto: datos en cadena

#### RF-0338 · Q 83 (A) — CCAF — Cambridge Bitcoin Electricity Consumption Index (CBECI)

- **Canal oficial (URL raíz):** https://cbeci.org/
- **Emisor:** Cambridge Centre for Alternative Finance (Cambridge Judge Business School)
- **Documentación y notas:** Índice en tiempo real del consumo eléctrico anual de la red Bitcoin (modelo ascendente con eficiencia de más de 60 equipos de minería), lanzado el 02/07/2019. URL cbeci.org confirmada en la página de la Judge Business School (jbs.cam.ac.uk/insight/2019/cambridge-bitcoin-electricity-consumption-index-cbeci/) y en Decrypt.
- **Temática:** TFB-14 Cripto: datos en cadena (principal) · secundarias: TFB-17
- **Calidad Q:** 83 (A) — Primariedad 16/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** secundaria
- **Acceso:** Abierto
- **Ámbitos:** Consumo energético y geografía de la minería de bitcoin
- **Motivo de inclusión y uso:** Fuente académica de referencia para el impacto energético (riesgo ESG y regulatorio). **Uso en el Bloque B:** AG-B11 (huella energética y riesgo ESG de bitcoin), AG-B05 (economía de la minería), AG-B12 (mineras cotizadas).
- **Restricciones de uso:** Citar estimación (central/rango) y fecha.
- **Sesgos y cautelas:** Estimación de modelo con rango amplio.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Cambridge Bitcoin Electricity Consumption Index CCAF»; URL tomada de la página de la Judge Business School leída con WebFetch; WebFetch al sitio: no)
- **Origen:** Reutilizada del Bloque A (ID original) en F9 Bloque B (TFB-14) el 2026-11-02.

#### RF-0076 · Q 82 (A) — DefiLlama

- **Canal oficial (URL raíz):** https://defillama.com/
- **Emisor:** DefiLlama (proyecto abierto)
- **Documentación y notas:** Secciones de visión de mercado (cadenas, protocolos, TVL puenteado), stablecoins, comisiones e ingresos (por protocolo y cadena), rendimientos; enlaces «Data Definitions» y «Report Incorrect Data».
- **Temática:** TFB-14 Cripto: datos en cadena (principal) · secundarias: TFB-06
- **Calidad Q:** 82 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 12/15 · Independencia 9/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** terciaria
- **Acceso:** Abierto
- **Ámbitos:** Valor total bloqueado (TVL), ingresos de protocolos, stablecoins, rendimientos
- **Motivo de inclusión y uso:** Datos agregados de DeFi. **Uso en el Bloque B:** AG-B04 y AG-B03 (TVL, comisiones e ingresos por protocolo y cadena; cuotas de mercado DeFi), AG-B12 y MC-B07 (cribado de protocolos y tokens).
- **Restricciones de uso:** Citar métrica, protocolo/cadena y fecha.
- **Sesgos y cautelas:** TVL con doble cómputo; datos autodeclarados por protocolos; la página leída no incluía declaración de código abierto (comprobar).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «DefiLlama DeFi TVL dashboard stablecoins fees revenue»; WebFetch: sí, defillama.com/revenue/chain/vaulta)
- **Origen:** Reutilizada del Bloque A (ID original) en F9 Bloque B (TFB-14) el 2026-11-02.

#### RF-0074 · Q 80 (A) — Coin Metrics

- **Canal oficial (URL raíz):** https://docs.coinmetrics.io/network-data
- **Emisor:** Coin Metrics (sus productos Pro se comercializan bajo Talos, según talos.com)
- **Documentación y notas:** Documentación de datos en cadena (metodologías, disponibilidad, glosario); paquete Community (docs.coinmetrics.io/packages/coin-metrics-community-data); boletín «State of the Network» (coinmetrics.substack.com). Aviso de 28/10/2025: retirada de parte de métricas Community; siguen gratis Research Asset Metrics, Reference Rates y Atlas (con restricciones).
- **Temática:** TFB-14 Cripto: datos en cadena (principal) · secundarias: TFB-06
- **Calidad Q:** 80 (A) — Primariedad 17/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 13/15 · Independencia 9/10 · Actualidad 10/10 · Acceso 7/10
- **Tipología:** secundaria
- **Acceso:** Freemium (Community reducida desde 2025)
- **Ámbitos:** Datos en cadena y de mercado con documentación metodológica
- **Motivo de inclusión y uso:** Métricas en cadena con metodología documentada. **Uso en el Bloque B:** AG-B04 (métricas de red: direcciones activas, comisiones, oferta) y MC-B01/MC-B06 (NVT, MVRV y series de referencia), AG-B12.
- **Restricciones de uso:** Licencia Community para datos gratuitos.
- **Sesgos y cautelas:** Cobertura gratuita recortada (Acceso 8 → 7; Q 81 → 80).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Integración comercial con Talos (la nota no detalla la operación): vigilar.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Coin Metrics State of the Network Community network data»; WebFetch: sí)
- **Origen:** Reutilizada del Bloque A (ID original) en F9 Bloque B (TFB-14) el 2026-11-02.

#### RF-0337 · Q 80 (A) — L2BEAT — análisis de redes de capa 2 de Ethereum

- **Canal oficial (URL raíz):** https://www.l2beat.com/scaling/tvs
- **Emisor:** L2BEAT
- **Documentación y notas:** Valor total asegurado (TVS) de rollups de Ethereum con desglose (puenteado canónico, nativo, externo); vistas de riesgo (l2beat.com/?view=risk). Instantánea leída: 33.260 M$ a 04/02/2026 (Arbitrum One, Base, OP Mainnet en cabeza).
- **Temática:** TFB-14 Cripto: datos en cadena (principal) · secundarias: TFB-09
- **Calidad Q:** 80 (A) — Primariedad 16/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 12/15 · Independencia 9/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** secundaria
- **Acceso:** Abierto
- **Ámbitos:** Capa 2 de Ethereum: valor asegurado, riesgos y fases
- **Motivo de inclusión y uso:** Evaluación independiente de riesgos y adopción de redes de capa 2. **Uso en el Bloque B:** AG-B03 y AG-B06 (cuotas, riesgos y madurez de las redes de capa 2), AG-B12 (criptoactivos L2).
- **Restricciones de uso:** Citar proyecto, métrica y fecha.
- **Sesgos y cautelas:** La página leída no describe el operador ni la metodología completa.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Cambio de métrica TVL → TVS.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «L2BEAT layer 2 rollups risk analysis value secured»; WebFetch: sí)
- **Origen:** Reutilizada del Bloque A (ID original) en F9 Bloque B (TFB-14) el 2026-11-02.

#### RF-0341 · Q 79 (B) — mempool.space — explorador de la red Bitcoin

- **Canal oficial (URL raíz):** https://mempool.space
- **Emisor:** mempool.space (proyecto de código abierto)
- **Documentación y notas:** Explorador de bloques y del mempool para estimar comisiones y congestión; URL confirmada en el glosario de River (river.com/learn/terms/m/mempool-explorer/), que cita también Blockstream (blockstream.info) y el explorador de Jochen Hoenicke.
- **Temática:** TFB-14 Cripto: datos en cadena (principal) · secundarias: TFB-09
- **Calidad Q:** 79 (B) — Primariedad 18/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 10/15 · Independencia 9/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Comisiones, mempool, bloques y hashrate de Bitcoin
- **Motivo de inclusión y uso:** Dato directo de la cadena para congestión y demanda de espacio de bloque. **Uso en el Bloque B:** AG-B05 (comisiones, hashrate y congestión de la red Bitcoin), AG-B12 (mineras).
- **Restricciones de uso:** Citar bloque/fecha.
- **Sesgos y cautelas:** Instancia pública de un proyecto comunitario; datos en tiempo real sin archivo oficial.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «mempool.space bitcoin explorer fees mempool»; URL tomada del glosario de River leído con WebFetch; WebFetch al sitio: no)
- **Origen:** Reutilizada del Bloque A (ID original) en F9 Bloque B (TFB-14) el 2026-11-02.

#### RF-0365 · Q 78 (B) — Etherscan — explorador de Ethereum

- **Canal oficial (URL raíz):** https://etherscan.io/charts
- **Emisor:** Etherscan
- **Documentación y notas:** Explorador de bloques y gráficos y estadísticas de Ethereum (y más de 60 cadenas EVM con una sola clave de API); documentación en docs.etherscan.io.
- **Temática:** TFB-14 Cripto: datos en cadena (principal) · secundarias: TFB-03
- **Calidad Q:** 78 (B) — Primariedad 18/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 12/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto; API con niveles
- **Ámbitos:** Transacciones, comisiones, contratos y estadísticas de Ethereum
- **Motivo de inclusión y uso:** Verificación directa en cadena de transacciones y métricas de Ethereum. **Uso en el Bloque B:** AG-B04 (uso de Ethereum y contratos), AG-B12 (verificación de suministro y concentración de tenedores de un token).
- **Restricciones de uso:** Condiciones de Etherscan; citar transacción o gráfico y fecha.
- **Sesgos y cautelas:** Etiquetas de direcciones propias; empresa privada.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Etherscan Ethereum blockchain explorer charts statistics»; WebFetch: sí, documentación)
- **Origen:** Reutilizada del Bloque A (ID original) en F9 Bloque B (TFB-14) el 2026-11-02.

#### RF-0334 · Q 77 (B) — CoinGecko — precios y capitalización de criptoactivos

- **Canal oficial (URL raíz):** https://www2.coingecko.com/en/methodology
- **Emisor:** CoinGecko
- **Documentación y notas:** Metodología publicada: índice de precio de BTC por VWAP, eliminación de valores atípicos, capitalización = precio × oferta circulante verificada; Trust Score de exchanges (liquidez, regulación, ciberseguridad, prueba de reservas; actualización «Basilisk» de mayo de 2026); cambios de metodología aprobados en un foro de gobernanza; sin cobro por listar.
- **Temática:** TFB-14 Cripto: datos en cadena (principal) · secundarias: TFB-06
- **Calidad Q:** 77 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 12/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** terciaria (agregador)
- **Acceso:** Abierto; API con niveles de pago
- **Ámbitos:** Precios, capitalización y volumen de criptoactivos y exchanges
- **Motivo de inclusión y uso:** Agregador de precios con metodología transparente. **Uso en el Bloque B:** AG-B12 y HT-11 (universo, capitalización, liquidez y categorías de criptoactivos para el cribado), MC-B07.
- **Restricciones de uso:** Condiciones de CoinGecko; citar activo, métrica y hora.
- **Sesgos y cautelas:** Volúmenes de exchanges con posibles lavados; oferta circulante declarada por los proyectos.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Trust Score revisado en 2026.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «CoinGecko methodology cryptocurrency market capitalization»; WebFetch: sí)
- **Origen:** Reutilizada del Bloque A (ID original) en F9 Bloque B (TFB-14) el 2026-11-02.

#### RF-0315 · Q 76 (B) — Dune

- **Canal oficial (URL raíz):** https://docs.dune.com/data-catalog/overview
- **Emisor:** Dune Analytics
- **Documentación y notas:** Catálogo de datos brutos, decodificados y curados de más de 100 cadenas (EVM y Solana con decodificación; Bitcoin y otras con datos brutos); consultas SQL, API de datos, Datashare (Snowflake, BigQuery, Databricks); conjuntos públicos en todos los planes y conjuntos premium (stablecoins, RWA, etc.) con derecho de acceso.
- **Temática:** TFB-14 Cripto: datos en cadena (principal) · secundarias: TFB-06
- **Calidad Q:** 76 (B) — Primariedad 17/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 11/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 8/10
- **Tipología:** secundaria
- **Acceso:** Freemium
- **Ámbitos:** Datos en cadena consultables por SQL; paneles comunitarios
- **Motivo de inclusión y uso:** Verificación directa de métricas en cadena (consultas reproducibles) frente a cifras de terceros. **Uso en el Bloque B:** AG-B04 y AG-B12 (consultas SQL comunitarias sobre uso y flujos en cadena), MC-B01.
- **Restricciones de uso:** Citar consulta/panel (ID) y fecha; los paneles de terceros heredan la calidad de su autor.
- **Sesgos y cautelas:** Paneles comunitarios sin revisión; etiquetas de direcciones heurísticas.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «mempool.space Etherscan Dune Analytics Token Terminal CoinGecko L2BEAT on-chain data sources»; WebFetch: sí)
- **Origen:** Reutilizada del Bloque A (ID original) en F9 Bloque B (TFB-14) el 2026-11-02.

#### RF-0367 · Q 76 (B) — Kaiko — datos e investigación de mercado cripto

- **Canal oficial (URL raíz):** https://www.kaiko.com/use-cases/research
- **Emisor:** Kaiko
- **Documentación y notas:** Datos de mercado (nivel 1 y 2, CeFi y DeFi, contado y derivados), Market Explorer (volumen y profundidad), tipos de referencia administrados según los principios IOSCO; cuenta de investigación gratuita.
- **Temática:** TFB-14 Cripto: datos en cadena (principal) · secundarias: TFB-06
- **Calidad Q:** 76 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 13/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 7/10
- **Tipología:** secundaria
- **Acceso:** Freemium (investigación gratuita; datos de pago)
- **Ámbitos:** Liquidez, profundidad de libro y volúmenes de exchanges
- **Motivo de inclusión y uso:** Calidad de mercado y liquidez de criptoactivos. **Uso en el Bloque B:** AG-B10 y AG-B12 (liquidez, profundidad y volumen por exchange; criterio de invertibilidad).
- **Restricciones de uso:** Condiciones de Kaiko.
- **Sesgos y cautelas:** Proveedor comercial; datos detallados de pago.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Kaiko Research crypto market liquidity data»; WebFetch: sí)
- **Origen:** Reutilizada del Bloque A (ID original) en F9 Bloque B (TFB-14) el 2026-11-02.

#### RF-0073 · Q 74 (B) — Glassnode

- **Canal oficial (URL raíz):** https://docs.glassnode.com/
- **Emisor:** Glassnode AG
- **Documentación y notas:** Documentación oficial con catálogo de métricas y acceso a Glassnode Studio (studio.glassnode.com); suscripciones de pago referidas en el FAQ.
- **Temática:** TFB-14 Cripto: datos en cadena (principal) · secundarias: TFB-15
- **Calidad Q:** 74 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 12/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 6/10
- **Tipología:** secundaria
- **Acceso:** Freemium (métricas avanzadas de pago)
- **Ámbitos:** Métricas en cadena de Bitcoin y Ethereum (MVRV, SOPR, flujos a plataformas)
- **Motivo de inclusión y uso:** Métricas en cadena de referencia para PERF-CHR. **Uso en el Bloque B:** AG-B10 (métricas de comportamiento de tenedores, flujos a exchanges), MC-B06 (indicadores de valoración en cadena).
- **Restricciones de uso:** Condiciones de Glassnode.
- **Sesgos y cautelas:** Metodologías propietarias (la página de inicio de la documentación no explica cálculos); heurísticas de etiquetado de direcciones.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Glassnode Coin Metrics Messari DefiLlama The Block crypto data»; WebFetch: sí)
- **Origen:** Reutilizada del Bloque A (ID original) en F9 Bloque B (TFB-14) el 2026-11-02.

#### MBF-0481 · Q 71 (B) — Token Terminal — métricas financieras estandarizadas de cadenas de bloques y aplicaciones

- **Canal oficial (URL raíz):** https://tokenterminal.com/about
- **Emisor:** Token Terminal (equipo técnico de unas 25 personas)
- **Documentación y notas:** Plataforma de datos en cadena que extrae datos brutos directamente de nodos, decodifica contratos inteligentes y produce «GAAP-like metrics» de uso y rendimiento financiero; más de 100 cadenas y miles de aplicaciones y activos tokenizados; API sobre BigQuery y ClickHouse. Según una comparativa de terceros (eco.com), nivel gratuito con histórico y exportación CSV, plan Pro de pago.
- **Temática:** TFB-14 Cripto: datos en cadena (principal) · secundarias: TFB-07
- **Calidad Q:** 71 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 11/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 7/10
- **Tipología:** secundaria (métricas derivadas de datos en cadena con método propio)
- **Acceso:** Mixto: nivel gratuito; Pro, API y Data Room de pago (futuro)
- **Ámbitos:** Ingresos por comisiones, ingresos del protocolo, usuarios y valoraciones (P/S, P/F) de protocolos y cadenas
- **Motivo de inclusión y uso:** Fundamentales tipo empresa para cribar criptoactivos. Bloque B: AG-B09 (valoración relativa de protocolos), AG-B12 (ranking de criptoactivos por ingresos y uso), MC-B06 y MC-B07 (múltiplos y z-scores).
- **Restricciones de uso:** Condiciones del nivel gratuito; la API requiere plan de pago (credenciales en HT-01).
- **Sesgos y cautelas:** Definiciones propias de «revenue» y «earnings»; cobertura sesgada a protocolos grandes; datos de precios de pago no verificados en esta ficha.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «free on-chain crypto data sources list Token Terminal Artemis growthepie Blockchair ultrasound.money beaconcha.in»; WebFetch: sí, página «About»; precios por comparativa de eco.com)
- **Origen:** Alta 2026-11-02 (F9 Bloque B, TFB-14).

#### RF-0077 · Q 70 (B) — Messari

- **Canal oficial (URL raíz):** https://docs.messari.io/docs/research
- **Emisor:** Messari Inc.
- **Documentación y notas:** Research Reports, Protocol Reporting (en colaboración directa con los protocolos), Diligence Reports; boletín y pódcast «Unqualified Opinions»; niveles Free, Pro y Enterprise (Pro accede a informes Enterprise 90 días después). Informe anual «Crypto Theses».
- **Temática:** TFB-14 Cripto: datos en cadena (principal) · secundarias: TFB-11
- **Calidad Q:** 70 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 12/15 · Independencia 7/10 · Actualidad 9/10 · Acceso 6/10
- **Tipología:** secundaria
- **Acceso:** Freemium
- **Ámbitos:** Informes de protocolos y activos digitales; tesis anuales
- **Motivo de inclusión y uso:** Investigación estructurada del sector cripto. **Uso en el Bloque B:** AG-B09 y AG-B12 (perfiles, tokenomics y métricas de protocolos), AG-B06.
- **Restricciones de uso:** Solo contenidos públicos citables.
- **Sesgos y cautelas:** Protocol Reporting en asociación con los propios protocolos (posible conflicto de interés; la página no detalla la financiación).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Messari crypto research reports Crypto Theses»; WebFetch: sí)
- **Origen:** Reutilizada del Bloque A (ID original) en F9 Bloque B (TFB-14) el 2026-11-02.

#### RF-0335 · Q 70 (B) — Farside Investors — flujos diarios de ETF de bitcoin y ether

- **Canal oficial (URL raíz):** https://farside.co.uk/?p=997
- **Emisor:** Farside Investors
- **Documentación y notas:** Tablas diarias de flujos netos (millones de dólares) por ETF al contado de bitcoin (IBIT, FBTC, GBTC…) y de ether (farside.co.uk/?p=1518); generadas automáticamente a partir de webs de emisores y proveedores de datos; advierte que prioriza rapidez sobre exactitud y que contiene estimaciones.
- **Temática:** TFB-14 Cripto: datos en cadena (principal) · secundarias: TFB-15
- **Calidad Q:** 70 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 10/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** secundaria
- **Acceso:** Abierto
- **Ámbitos:** Flujos de ETF de criptoactivos en EE. UU.
- **Motivo de inclusión y uso:** Medida diaria de demanda institucional de criptoactivos; muy citada por la prensa. **Uso en el Bloque B:** AG-B10 (flujos diarios de ETF al contado de bitcoin y ether como demanda institucional), AG-B12 (comparación de ETF/ETP cripto).
- **Restricciones de uso:** Citar fecha y ETF; contrastar con datos de emisores.
- **Sesgos y cautelas:** Estimaciones con errores declarados; gestora con producto propio.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin datos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Farside Investors bitcoin ETF flow data»; WebFetch: sí)
- **Origen:** Reutilizada del Bloque A (ID original) en F9 Bloque B (TFB-14) el 2026-11-02.

#### RF-0336 · Q 70 (B) — CoinShares — Digital Asset Fund Flows (semanal)

- **Canal oficial (URL raíz):** https://coinshares.com/us/insights/research-data/fund-flows-18-03-24
- **Emisor:** CoinShares (investigación: James Butterfill)
- **Documentación y notas:** Informe semanal de flujos de ETP de activos digitales por proveedor, país de cotización y activo (bitcoin, ether, Solana, cortos, acciones blockchain), volumen negociado y flujos sobre patrimonio; sin metodología ni fuentes detalladas en la página.
- **Temática:** TFB-14 Cripto: datos en cadena (principal) · secundarias: TFB-15
- **Calidad Q:** 70 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 12/15 · Independencia 6/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** secundaria
- **Acceso:** Abierto
- **Ámbitos:** Flujos semanales de productos cotizados de criptoactivos a escala mundial
- **Motivo de inclusión y uso:** Serie semanal global de flujos (incluye Europa), complemento de RF-0335. **Uso en el Bloque B:** AG-B10 (flujos semanales a productos cotizados de activos digitales por activo y emisor, incluida Europa), AG-B12 (ETP cripto accesibles al minorista europeo).
- **Restricciones de uso:** Citar semana; aviso legal del emisor.
- **Sesgos y cautelas:** Emisor de ETP (conflicto de interés); metodología no publicada.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «CoinShares Digital Asset Fund Flows Weekly Report»; WebFetch: sí)
- **Origen:** Reutilizada del Bloque A (ID original) en F9 Bloque B (TFB-14) el 2026-11-02.

#### MBF-0482 · Q 69 (B) — Artemis — terminal de analítica cripto (cadenas, aplicaciones y stablecoins)

- **Canal oficial (URL raíz):** https://artemis.xyz/terminal
- **Emisor:** Artemis Analytics
- **Documentación y notas:** Plataforma sin código para comparar cadenas (incluidas L1), dApps y perpetuos; monitor de actividad por cadena, panel de stablecoins por categoría, aplicación y contrato; constructor de gráficos con exportación CSV. Una comparativa de terceros (eco.com) cita unas 75 cadenas, direcciones activas, comisiones, MEV e ingresos de aplicaciones, con nivel gratuito y Pro de pago (exportación, histórico largo, API).
- **Temática:** TFB-14 Cripto: datos en cadena (principal) · secundarias: TFB-07
- **Calidad Q:** 69 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 10/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 8/10
- **Tipología:** secundaria (métricas derivadas de datos en cadena)
- **Acceso:** Mixto: nivel gratuito con la mayoría de métricas; Pro y API de pago (futuro)
- **Ámbitos:** Actividad y fundamentales de cadenas, aplicaciones y stablecoins
- **Motivo de inclusión y uso:** Comparación de adopción entre cadenas y del mercado de stablecoins. Bloque B: AG-B04 (adopción y uso), AG-B03 (cuotas entre cadenas), AG-B12.
- **Restricciones de uso:** Condiciones del proveedor; API de pago.
- **Sesgos y cautelas:** Método propio; cambios de cobertura; la página leída no detalla las condiciones de acceso.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «free on-chain crypto data sources list Token Terminal Artemis growthepie Blockchair ultrasound.money beaconcha.in»; WebFetch: sí, página del Terminal; precios por comparativa de eco.com)
- **Origen:** Alta 2026-11-02 (F9 Bloque B, TFB-14).

#### MBF-0626 · Q 67 (B) — CryptoQuant — métricas en cadena y de derivados cripto

- **Canal oficial (URL raíz):** https://cryptoquant.com/
- **Emisor:** CryptoQuant (fundada en 2018)
- **Documentación y notas:** Flujos de exchanges calculados por bloque a partir de direcciones etiquetadas, flujos de mineros, ballenas y fondos, reservas, MVRV, SOPR y comportamiento de tenedores a corto y largo plazo; datos de mercado (OHLCV, financiación, interés abierto, liquidaciones) e índice diario de consenso de analistas. Cubre Bitcoin, Ethereum, XRP, TRON, stablecoins y tokens ERC-20; API REST con más de 245 métricas, servidor MCP, SQL y exportación CSV. Plan básico gratuito (10.000 créditos de API al mes, datos de mercado diarios, 30 días de historia, sin datos en cadena); niveles de pago con datos en cadena.
- **Temática:** TFB-14 Cripto: datos en cadena (principal) · secundarias: TFB-15
- **Calidad Q:** 67 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 11/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 6/10
- **Tipología:** analítica (etiquetado propio de direcciones)
- **Acceso:** Freemium: plan gratuito sin datos en cadena; datos en cadena de pago (futuro)
- **Ámbitos:** Flujos de exchanges, reservas, métricas de valoración en cadena y derivados
- **Motivo de inclusión y uso:** Fuente especializada en flujos hacia y desde exchanges, útil para posicionamiento y presión vendedora en cripto.
- **Restricciones de uso:** Condiciones de CryptoQuant; redistribución solo con licencia empresarial.
- **Sesgos y cautelas:** Etiquetado de direcciones propietario y no auditable; el plan gratuito no incluye datos en cadena; contrastar con Glassnode (RF-0073) y Coin Metrics (RF-0074).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B10 Flujos y Sentimiento: flujos netos a exchanges y reservas como señal de presión vendedora; AG-B09: MVRV y SOPR como medidas de valoración en cadena; AG-B14 Contrarias.
- **Origen:** Alta F9_comp (2026-11-03).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-03 (búsqueda web: «free on-chain analytics CryptoQuant blockchain.com charts rwa.xyz tokenized assets dashboard»; WebFetch: sí)

#### MBF-0627 · Q 67 (B) — RWA.xyz — analítica de activos reales tokenizados y stablecoins

- **Canal oficial (URL raíz):** https://www.rwa.xyz/ (aplicación: https://app.rwa.xyz/)
- **Emisor:** RWA.xyz
- **Documentación y notas:** Plataforma de datos sobre activos reales tokenizados: fondos del Tesoro de EE. UU. tokenizados (p. ej., USDY y USYC), crédito privado, materias primas, acciones, inmobiliario, PE/VC y estrategias activas, más stablecoins (USDT ≈ 178.500 M USD, USDC ≈ 70.700 M USD). Portada a 02/11/2026: 39.050 M USD de valor distribuido, 397.980 M USD de valor representado, ≈ 5,49 M de tenedores y 285.890 M USD en stablecoins; clasificaciones por red, gestora y plataforma; catálogo de datos, documentación, descargas CSV y API empresarial.
- **Temática:** TFB-14 Cripto: datos en cadena (principal) · secundarias: TFB-08, TFB-06
- **Calidad Q:** 67 (B) — Primariedad 13/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 11/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 7/10
- **Tipología:** analítica (agregación de datos en cadena y de emisores)
- **Acceso:** Freemium: parte abierta; muchas métricas tras inicio de sesión; API empresarial de pago (futuro)
- **Ámbitos:** Tokenización de activos reales y stablecoins por emisor, red y plataforma
- **Motivo de inclusión y uso:** Única fuente especializada para dimensionar el segmento de tokenización (fondos monetarios tokenizados, crédito privado) y sus cuotas de mercado.
- **Restricciones de uso:** Condiciones de RWA.xyz; sin redistribución.
- **Sesgos y cautelas:** Mezcla de datos en cadena y declarados por emisores; definiciones de «valor distribuido» y «representado» propias; cifras con fecha de corte que cambian a diario.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B04 Demanda y Adopción: crecimiento de la tokenización de activos; AG-B03 Estructura y Competencia: cuotas de gestoras y redes; AG-B06 Tecnología; AG-B12: candidatos expuestos a la tokenización.
- **Origen:** Alta F9_comp (2026-11-03).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-03 (búsqueda web: «free on-chain analytics CryptoQuant blockchain.com charts rwa.xyz tokenized assets dashboard»; WebFetch: sí, app.rwa.xyz)

#### RF-0075 · Q 67 (B) — The Block

- **Canal oficial (URL raíz):** https://www.theblock.co/
- **Emisor:** The Block
- **Documentación y notas:** Noticias, investigación y panel de datos gratuito (lanzado en 2020 con más de 70 gráficos: en cadena, mercados, finanzas abiertas, métricas alternativas; fuentes declaradas: Coin Metrics, Chainalysis, CFTC COT, Dune, entre otras). Páginas de equipo editorial, conflictos de interés y divulgaciones; contenido patrocinado etiquetado.
- **Temática:** TFB-14 Cripto: datos en cadena (principal) · secundarias: TFB-10
- **Calidad Q:** 67 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 11/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 7/10
- **Tipología:** primaria
- **Acceso:** Muro parcial
- **Ámbitos:** Noticias e investigación de criptoactivos; panel de datos
- **Motivo de inclusión y uso:** Reporterismo e investigación del sector cripto. **Uso en el Bloque B:** AG-B04 y AG-B10 (panel de datos gratuito en cadena y de mercados; reporterismo sectorial con hechos citados en su fuente).
- **Restricciones de uso:** Citar artículo y fecha; los datos del panel citan su fuente original.
- **Sesgos y cautelas:** Historial de cambios de propiedad y conflictos de interés en el sector; uso declarado de IA con revisión editorial.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Vigilar propiedad (no declarada en la página leída).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «The Block crypto news research data dashboard theblock.co»; WebFetch: sí, artículo del panel de datos)
- **Origen:** Reutilizada del Bloque A (ID original) en F9 Bloque B (TFB-14) el 2026-11-02.

#### RF-0316 · Q 67 (B) — DL News

- **Canal oficial (URL raíz):** https://www.dlnews.com/
- **Emisor:** DL News
- **Documentación y notas:** Medio de noticias sobre cripto y finanzas descentralizadas; sección educativa «Llama U» (p. ej., guía de DefiLlama, 16/08/2023). La página leída no declara la propiedad ni relación alguna con DefiLlama.
- **Temática:** TFB-14 Cripto: datos en cadena (principal) · secundarias: TFB-10
- **Calidad Q:** 67 (B) — Primariedad 11/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 10/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** secundaria
- **Acceso:** Abierto
- **Ámbitos:** Noticias de DeFi, cripto y regulación
- **Motivo de inclusión y uso:** Segunda raíz periodística en cripto independiente de CoinDesk (RF-0036) y The Block (RF-0075).
- **Restricciones de uso:** Opinión/noticia: los hechos se citan en su fuente primaria.
- **Sesgos y cautelas:** Propiedad no declarada en la página leída: verificar posible vínculo con DefiLlama antes de usarla como corroboración independiente de RF-0076.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin datos.
- **Uso en el bloque:** AG-B06 Tecnología y AG-B07 Regulación y Geopolítica: noticias de DeFi, protocolos y regulación cripto; los datos se citan en su fuente primaria (DefiLlama, exploradores).
- **Origen:** Reutilizada con su ID de F9 V3.2 (Bloque A general); temática reasignada a TFB-14 el 2026-11-03.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «DefiLlama DeFi TVL dashboard stablecoins fees revenue»; WebFetch: sí)

#### RF-0366 · Q 67 (B) — Chainalysis — Crypto Crime Report

- **Canal oficial (URL raíz):** https://chainalysis.com/reports/crypto-crime-2026
- **Emisor:** Chainalysis
- **Documentación y notas:** Informe anual sobre blanqueo, estafas, exploits de DeFi y ransomware (edición 2026), en varios idiomas, con boletín semanal; la página no describe metodología.
- **Temática:** TFB-14 Cripto: datos en cadena (principal) · secundarias: TFB-03
- **Calidad Q:** 67 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 8/15 · Autoridad 14/15 · Independencia 6/10 · Actualidad 8/10 · Acceso 7/10
- **Tipología:** secundaria
- **Acceso:** Abierto con descarga (posible formulario)
- **Ámbitos:** Actividad ilícita en criptoactivos
- **Motivo de inclusión y uso:** Referencia sectorial de riesgo regulatorio y reputacional. **Uso en el Bloque B:** AG-B07 y AG-B11 (riesgo de actividad ilícita, sanciones y regulación), AG-B14.
- **Restricciones de uso:** Citar edición y cifra; contrastar con datos oficiales.
- **Sesgos y cautelas:** Vende herramientas de análisis relacionadas (conflicto de interés); metodología no publicada en la página.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Chainalysis Crypto Crime Report 2026»; WebFetch: sí)
- **Origen:** Reutilizada del Bloque A (ID original) en F9 Bloque B (TFB-14) el 2026-11-02.

#### RF-0340 · Q 66 (B) — Decrypt — noticias cripto

- **Canal oficial (URL raíz):** https://decrypt.co/7741/cambridge-bitcoin-electricity-index
- **Emisor:** Decrypt Media, Inc.
- **Documentación y notas:** Medio de noticias sobre criptoactivos y web3; páginas de divulgación financiera (decrypt.co/financial-disclosures), manifiesto y código de conducta.
- **Temática:** TFB-14 Cripto: datos en cadena (principal) · secundarias: TFB-10
- **Calidad Q:** 66 (B) — Primariedad 10/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 10/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** secundaria
- **Acceso:** Abierto
- **Ámbitos:** Noticias de criptoactivos
- **Motivo de inclusión y uso:** Raíz periodística con política de divulgación publicada.
- **Restricciones de uso:** Opinión/noticia: los hechos se citan en su fuente primaria.
- **Sesgos y cautelas:** Medio sectorial; revisar las divulgaciones financieras.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin datos.
- **Uso en el bloque:** AG-B06 Tecnología y AG-B04 Demanda y Adopción: actualidad de criptoactivos y web3 como alerta temprana; los hechos se citan en su fuente primaria.
- **Origen:** Reutilizada con su ID de F9 V3.2 (Bloque A general); temática reasignada a TFB-14 el 2026-11-03.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Cambridge Bitcoin Electricity Consumption Index CCAF»; WebFetch: sí)

#### RF-0339 · Q 65 (B) — Blockworks — noticias, investigación y análisis cripto

- **Canal oficial (URL raíz):** https://blockworks.com/news/layer-2-secured-by-ethereum
- **Emisor:** Blockworks Inc. (Nueva York)
- **Documentación y notas:** Red con noticias, pódcasts, boletines, eventos, Analytics y Blockworks Research (plataforma de investigación). La página leída no enlaza política editorial ni de divulgación.
- **Temática:** TFB-14 Cripto: datos en cadena (principal) · secundarias: TFB-10
- **Calidad Q:** 65 (B) — Primariedad 11/20 · Historial 10/20 · Transparencia 8/15 · Autoridad 11/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 8/10
- **Tipología:** secundaria
- **Acceso:** Abierto (noticias); investigación de pago
- **Ámbitos:** Noticias e investigación de criptoactivos y finanzas descentralizadas
- **Motivo de inclusión y uso:** Raíz periodística adicional en cripto. **Uso en el Bloque B:** AG-B06 y AG-B14 (investigación y análisis cripto como contraste; opinión, no hecho).
- **Restricciones de uso:** Opinión/noticia: los hechos se citan en su fuente primaria.
- **Sesgos y cautelas:** Sin política de conflictos visible; ingresos por eventos y patrocinios.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin datos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «L2BEAT layer 2 rollups risk analysis value secured»; WebFetch: sí)
- **Origen:** Reutilizada del Bloque A (ID original) en F9 Bloque B (TFB-14) el 2026-11-02.

#### MBF-0483 · Q 63 (C) — GeckoTerminal — precios y liquidez de tokens en exchanges descentralizados (CoinGecko)

- **Canal oficial (URL raíz):** URL raíz no leída; citada en https://eco.com/support/en/articles/14800365-artemis-vs-token-terminal-compared
- **Emisor:** CoinGecko
- **Documentación y notas:** Rastreador de pares de exchanges descentralizados recomendado en comparativas para tokens que no cubren las plataformas curadas (p. ej., memecoins).
- **Temática:** TFB-14 Cripto: datos en cadena (principal) · secundarias: TFB-06
- **Calidad Q:** 63 (C) — Primariedad 13/20 · Historial 10/20 · Transparencia 7/15 · Autoridad 9/15 · Independencia 7/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** secundaria (agregador de datos de DEX)
- **Acceso:** Abierto
- **Ámbitos:** Precios, volumen y liquidez de pares en DEX
- **Motivo de inclusión y uso:** Liquidez real en cadena de tokens pequeños. Bloque B: AG-B12 (filtro de invertibilidad y liquidez de criptoactivos), AG-B10.
- **Restricciones de uso:** Condiciones de CoinGecko.
- **Sesgos y cautelas:** Tokens de baja calidad y manipulación de liquidez; no aplicar sin filtros.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «free on-chain crypto data sources list Token Terminal Artemis growthepie Blockchair ultrasound.money beaconcha.in»; WebFetch: sí, comparativa de eco.com (página índice); GeckoTerminal no se leyó)
- **Origen:** Alta 2026-11-02 (F9 Bloque B, TFB-14).

#### MBF-0484 · Q 59 (C) — Electric Capital — seguimiento de la actividad de desarrolladores cripto

- **Canal oficial (URL raíz):** URL raíz no leída; citada en https://eco.com/support/en/articles/14800365-artemis-vs-token-terminal-compared
- **Emisor:** Electric Capital
- **Documentación y notas:** Seguimiento de la actividad de desarrolladores en ecosistemas cripto, citado en comparativas como solapado con el seguimiento de desarrolladores de Artemis.
- **Temática:** TFB-14 Cripto: datos en cadena (principal) · secundarias: TFB-09
- **Calidad Q:** 59 (C) — Primariedad 12/20 · Historial 10/20 · Transparencia 7/15 · Autoridad 9/15 · Independencia 6/10 · Actualidad 7/10 · Acceso 8/10
- **Tipología:** secundaria (estudio propio sobre repositorios públicos)
- **Acceso:** Abierto (informe)
- **Ámbitos:** Desarrolladores activos por ecosistema
- **Motivo de inclusión y uso:** Indicador de oferta tecnológica y salud de ecosistemas. Bloque B: AG-B06 (tecnología), AG-B13 (prospectiva de ecosistemas).
- **Restricciones de uso:** Uso con cita.
- **Sesgos y cautelas:** Gestora de capital riesgo con posiciones en el sector; URL del informe no leída.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «free on-chain crypto data sources list Token Terminal Artemis growthepie Blockchair ultrasound.money beaconcha.in»; WebFetch: sí, comparativa de eco.com (página índice); el sitio de Electric Capital no se leyó)
- **Origen:** Alta 2026-11-02 (F9 Bloque B, TFB-14).

## TFB-15 Posicionamiento, flujos y sentimiento

#### RF-0342 · Q 86 (A) — FINRA — estadísticas de margen

- **Canal oficial (URL raíz):** https://www.finra.org/investors/margin-statistics
- **Emisor:** Financial Industry Regulatory Authority (FINRA)
- **Documentación y notas:** Saldos deudores en cuentas de margen y saldos acreedores libres (regla 4521(d)), a fin de mes, publicados hacia la tercera semana del mes siguiente; histórico desde enero de 1997 en Excel (serie homogénea desde febrero de 2010). Septiembre de 2026: 1,48 billones de dólares de saldos deudores.
- **Temática:** TFB-15 Posicionamiento, flujos y sentimiento (principal) · secundarias: TFB-03
- **Calidad Q:** 86 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto (web y Excel; sin feed)
- **Ámbitos:** Apalancamiento de inversores minoristas y de intermediarios en EE. UU.
- **Motivo de inclusión y uso:** Indicador de apalancamiento y euforia (deuda de margen) para el régimen de riesgo. **Uso en el Bloque B:** AG-B10 y AG-B11 (apalancamiento minorista agregado como señal de euforia o fragilidad).
- **Restricciones de uso:** Uso con atribución; citar mes.
- **Sesgos y cautelas:** Cambios de método de cálculo de algunas firmas desde 2021; ruptura de serie en 2010.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Integración NYSE/NASD (2010).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «FINRA margin statistics customer margin balances»; WebFetch: sí)
- **Origen:** Reutilizada del Bloque A (ID original) en F9 Bloque B (TFB-15) el 2026-11-02.

#### RF-0344 · Q 86 (A) — Tesoro de EE. UU. — Treasury International Capital (TIC)

- **Canal oficial (URL raíz):** https://home.treasury.gov/archives-of-tic-monthly-data-releases
- **Emisor:** U.S. Department of the Treasury
- **Documentación y notas:** Notas mensuales de flujos de capital transfronterizos (p. ej., nota de 16/09/2026 sobre julio de 2026: entrada neta de 83.700 M$, 73.500 M$ privados y 10.200 M$ oficiales; siguiente 16/10/2026); archivo histórico de publicaciones.
- **Temática:** TFB-15 Posicionamiento, flujos y sentimiento (principal) · secundarias: TFB-02
- **Calidad Q:** 86 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 7/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Compras extranjeras de valores de EE. UU.; tenencias de Treasuries por país
- **Motivo de inclusión y uso:** Flujos de capital extranjero hacia activos estadounidenses (demanda de Treasuries). **Uso en el Bloque B:** AG-B10 (flujos de cartera transfronterizos hacia y desde EE. UU. por tipo de activo), AG-B08.
- **Restricciones de uso:** Uso libre; citar mes de referencia.
- **Sesgos y cautelas:** Desfase de unos dos meses y medio; atribución por país de custodia.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Treasury International Capital TIC system monthly data»; WebFetch: sí, nota de septiembre de 2026)
- **Origen:** Reutilizada del Bloque A (ID original) en F9 Bloque B (TFB-15) el 2026-11-02.

#### RF-0049 · Q 85 (A) — CFTC — Commitments of Traders (COT)

- **Canal oficial (URL raíz):** https://www.cftc.gov/MarketReports/CommitmentsofTraders/index.htm
- **Emisor:** U.S. Commodity Futures Trading Commission (CFTC)
- **Documentación y notas:** La página oficial describe los cuatro informes (Legacy, Supplemental, Disaggregated, Traders in Financial Futures) y remite al calendario de publicación y al Public Reporting Environment (históricos consultables). Catálogo federal: catalog.data.gov/dataset/commitment-of-traders-cot
- **Temática:** TFB-15 Posicionamiento, flujos y sentimiento (principal) · secundarias: TFB-12
- **Calidad Q:** 85 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 14/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto (dominio público, datos federales de EE. UU.)
- **Ámbitos:** Posicionamiento semanal en futuros y opciones sobre futuros (mercados con ≥ 20 operadores declarables): comerciales/no comerciales; productores, swap dealers, managed money; dealers, gestores de activos y fondos apalancados en futuros financieros (divisas, Treasuries, índices bursátiles, VIX)
- **Motivo de inclusión y uso:** Dato primario de posicionamiento especulativo y de cobertura para divisas, materias primas, bonos e índices; insumo de señales de sentimiento extremo y de crowding. **Uso en el Bloque B:** AG-B10 (posicionamiento de gestores apalancados y comerciales en futuros de materias primas, divisas, bonos e índices sectoriales), AG-B14 (extremos de consenso).
- **Restricciones de uso:** Uso libre; citar informe (Legacy/Disaggregated/TFF), contrato y fecha del martes de referencia.
- **Sesgos y cautelas:** Datos del martes publicados el viernes a las 15:30 ET (desfase de 3 días; festivos alteran el calendario). Categorías amplias; los datos publicados no se revisan. Históricos: Legacy desde 15/01/1986; Disaggregated y TFF desde 13/06/2006.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos; vigilar avisos de calendario de la CFTC.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «CFTC Commitments of Traders reports official»; WebFetch: sí)
- **Origen:** Reutilizada del Bloque A (ID original) en F9 Bloque B (TFB-15) el 2026-11-02.

#### MBF-0624 · Q 84 (A) — FINRA — archivos de volumen de ventas en corto (Reg SHO): diarios por valor y mensuales por operación

- **Canal oficial (URL raíz):** https://finra.org/filing-reporting/trf/technical-notices/technical-notices/trf-short-sale-files (página de datos: https://www.finra.org/filing-reporting/trf/trf-regulation-sho-2021 · ADF: https://www.finra.org/filing-reporting/adf/adf-regulation-sho)
- **Emisor:** Financial Industry Regulatory Authority (FINRA)
- **Documentación y notas:** Archivo diario de volumen agregado de ventas en corto por valor de las operaciones comunicadas a los TRF de FINRA (desde el 24/09/2018 incluye el TRF de Chicago) y archivo mensual a nivel de operación (hora, precio y número de acciones de cada venta en corto) publicado tras el cierre de cada mes. Complementa las estadísticas de margen (RF-0342).
- **Temática:** TFB-15 Posicionamiento, flujos y sentimiento (principal) · secundarias: TFB-06
- **Calidad Q:** 84 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** primaria (autorregulador del mercado)
- **Acceso:** Abierto, sin registro
- **Ámbitos:** Volumen de ventas en corto por valor en mercados fuera de bolsa (OTC) de EE. UU.
- **Motivo de inclusión y uso:** Indicador diario de presión vendedora y de cobertura por valor y sector.
- **Restricciones de uso:** Uso libre con atribución.
- **Sesgos y cautelas:** El volumen de ventas en corto no equivale al interés en corto (posiciones abiertas) e incluye ventas de creadores de mercado que se cubren en el día; no cubre las operaciones en bolsa.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Incorporación del TRF de Chicago (2018).
- **Uso en el bloque:** AG-B10 Flujos y Sentimiento: presión vendedora en corto por valor y sector; AG-B14 Contrarias: posiciones bajistas concentradas; AG-B12: riesgo de compresión de cortos en candidatos.
- **Origen:** Alta F9_comp (2026-11-03).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-03 (búsqueda web: «FINRA equity short interest data publication schedule and Reg SHO daily short sale volume files»; WebFetch: sí, nota técnica de archivos de ventas en corto)

#### MBF-0512 · Q 83 (A) — CNMV — posiciones cortas netas en acciones (España)

- **Canal oficial (URL raíz):** http:www.cnmv.es/portal/Consultas/Busqueda.aspx?id=29 (enlace tal como figura en la lista de ESMA)
- **Emisor:** Comisión Nacional del Mercado de Valores (CNMV)
- **Documentación y notas:** Sitio central donde la autoridad nacional publica las posiciones cortas netas en acciones (artículo 9 del Reglamento (UE) 236/2012), según la lista oficial de ESMA (ESMA50-164-770 «Links to National Websites where Net Short Positions in Shares are Disclosed» (actualizado 13/05/2025): https://www.esma.europa.eu/sites/default/files/library/ssr_websites_ss_positions.pdf).
- **Temática:** TFB-15 Posicionamiento, flujos y sentimiento (principal) · secundarias: TFB-03
- **Calidad Q:** 83 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 9/10
- **Tipología:** primaria (declaraciones regulatorias publicadas por la autoridad)
- **Acceso:** Abierto
- **Ámbitos:** Posiciones cortas netas significativas en acciones admitidas en España
- **Motivo de inclusión y uso:** Detecta apuestas bajistas de gestoras y fondos sobre candidatos de España. Bloque B: AG-B10 (posicionamiento bajista y riesgo de short squeeze), AG-B12 (señal en el cribado de candidatos), AG-B14 (tesis contrarias).
- **Restricciones de uso:** Uso libre con cita de la autoridad y la fecha.
- **Sesgos y cautelas:** Solo se publican las posiciones que superan el umbral de publicación del Reglamento 236/2012 (las de notificación al supervisor, más bajas, no son públicas); no revela posiciones agregadas inferiores ni la cobertura subyacente.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «FINRA equity short interest data; ESMA net short positions notifications national competent authorities; CNMV posiciones cortas»; WebFetch: sí, lista oficial de ESMA (página índice); el sitio nacional no se leyó)
- **Origen:** Alta 2026-11-02 (F9 Bloque B, TFB-15).

#### MBF-0513 · Q 83 (A) — AMF — BDIF, posiciones cortas netas (Francia)

- **Canal oficial (URL raíz):** https://bdif.amf-france.org/fr?typesInformation=VAD (inglés: https://bdif.amf-france.org/en?typesInformation=VAD)
- **Emisor:** Autorité des marchés financiers (AMF)
- **Documentación y notas:** Sitio central donde la autoridad nacional publica las posiciones cortas netas en acciones (artículo 9 del Reglamento (UE) 236/2012), según la lista oficial de ESMA (ESMA50-164-770 «Links to National Websites where Net Short Positions in Shares are Disclosed» (actualizado 13/05/2025): https://www.esma.europa.eu/sites/default/files/library/ssr_websites_ss_positions.pdf).
- **Temática:** TFB-15 Posicionamiento, flujos y sentimiento (principal) · secundarias: TFB-03
- **Calidad Q:** 83 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 9/10
- **Tipología:** primaria (declaraciones regulatorias publicadas por la autoridad)
- **Acceso:** Abierto
- **Ámbitos:** Posiciones cortas netas significativas en acciones admitidas en Francia
- **Motivo de inclusión y uso:** Detecta apuestas bajistas de gestoras y fondos sobre candidatos de Francia. Bloque B: AG-B10 (posicionamiento bajista y riesgo de short squeeze), AG-B12 (señal en el cribado de candidatos), AG-B14 (tesis contrarias).
- **Restricciones de uso:** Uso libre con cita de la autoridad y la fecha.
- **Sesgos y cautelas:** Solo se publican las posiciones que superan el umbral de publicación del Reglamento 236/2012 (las de notificación al supervisor, más bajas, no son públicas); no revela posiciones agregadas inferiores ni la cobertura subyacente.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «FINRA equity short interest data; ESMA net short positions notifications national competent authorities; CNMV posiciones cortas»; WebFetch: sí, lista oficial de ESMA (página índice); el sitio nacional no se leyó)
- **Origen:** Alta 2026-11-02 (F9 Bloque B, TFB-15).

#### MBF-0515 · Q 83 (A) — CONSOB — posiciones cortas netas (Italia)

- **Canal oficial (URL raíz):** http://www.consob.it/web/area-pubblica/pnc (inglés: http://www.consob.it/web/consob-and-its-activities/short-selling)
- **Emisor:** Commissione Nazionale per le Società e la Borsa (CONSOB)
- **Documentación y notas:** Sitio central donde la autoridad nacional publica las posiciones cortas netas en acciones (artículo 9 del Reglamento (UE) 236/2012), según la lista oficial de ESMA (ESMA50-164-770 «Links to National Websites where Net Short Positions in Shares are Disclosed» (actualizado 13/05/2025): https://www.esma.europa.eu/sites/default/files/library/ssr_websites_ss_positions.pdf).
- **Temática:** TFB-15 Posicionamiento, flujos y sentimiento (principal) · secundarias: TFB-03
- **Calidad Q:** 83 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 9/10
- **Tipología:** primaria (declaraciones regulatorias publicadas por la autoridad)
- **Acceso:** Abierto
- **Ámbitos:** Posiciones cortas netas significativas en acciones admitidas en Italia
- **Motivo de inclusión y uso:** Detecta apuestas bajistas de gestoras y fondos sobre candidatos de Italia. Bloque B: AG-B10 (posicionamiento bajista y riesgo de short squeeze), AG-B12 (señal en el cribado de candidatos), AG-B14 (tesis contrarias).
- **Restricciones de uso:** Uso libre con cita de la autoridad y la fecha.
- **Sesgos y cautelas:** Solo se publican las posiciones que superan el umbral de publicación del Reglamento 236/2012 (las de notificación al supervisor, más bajas, no son públicas); no revela posiciones agregadas inferiores ni la cobertura subyacente.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «FINRA equity short interest data; ESMA net short positions notifications national competent authorities; CNMV posiciones cortas»; WebFetch: sí, lista oficial de ESMA (página índice); el sitio nacional no se leyó)
- **Origen:** Alta 2026-11-02 (F9 Bloque B, TFB-15).

#### MBF-0511 · Q 82 (A) — ESMA — enlaces oficiales a los sitios nacionales de publicación de posiciones cortas netas en acciones (UE/EEE)

- **Canal oficial (URL raíz):** https://www.esma.europa.eu/sites/default/files/library/ssr_websites_ss_positions.pdf
- **Emisor:** Autoridad Europea de Valores y Mercados (ESMA)
- **Documentación y notas:** Documento ESMA50-164-770, actualizado el 13/05/2025, con los sitios centrales gestionados o supervisados por cada autoridad nacional donde se publican las posiciones cortas netas en acciones según el artículo 9 del Reglamento (UE) 236/2012; ESMA lo actualiza al recibir información de las autoridades.
- **Temática:** TFB-15 Posicionamiento, flujos y sentimiento (principal) · secundarias: TFB-03
- **Calidad Q:** 82 (A) — Primariedad 17/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 7/10 · Acceso 10/10
- **Tipología:** primaria (directorio regulatorio oficial)
- **Acceso:** Abierto
- **Ámbitos:** Posiciones cortas netas publicadas en los Estados del EEE
- **Motivo de inclusión y uso:** Punto de entrada único para reunir posiciones cortas sobre candidatos europeos. Bloque B: AG-B10, AG-B12 y HT-11 (conectores por país).
- **Restricciones de uso:** Uso libre con cita.
- **Sesgos y cautelas:** Directorio, no datos; algunos enlaces nacionales pueden cambiar entre actualizaciones.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «FINRA equity short interest data; ESMA net short positions notifications national competent authorities; CNMV posiciones cortas»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9 Bloque B, TFB-15).

#### RF-0044 · Q 82 (A) — SEC EDGAR — formularios 13F (posiciones de grandes gestores)

- **Canal oficial (URL raíz):** https://www.sec.gov/ (FAQ del Form 13F: https://www.sec.gov/divisions/investment/13ffaq; búsqueda de presentaciones en EDGAR)
- **Emisor:** U.S. Securities and Exchange Commission
- **Temática:** TFB-15 Posicionamiento, flujos y sentimiento (principal) · secundarias: TFB-03
- **Calidad Q:** 82 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 14/15 · Independencia 9/10 · Actualidad 6/10 · Acceso 10/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Posiciones trimestrales de gestores institucionales con discreción sobre ≥ 100 M USD en valores 13(f)
- **Motivo de inclusión y uso:** Movimientos documentados de grandes inversores. Presentación obligatoria en EDGAR dentro de los 45 días siguientes al cierre del trimestre (p. ej., 15/05/2026 para el trimestre de marzo de 2026). Pieza especializada del portal general RF-0002. **Uso en el Bloque B:** AG-B10 (posiciones trimestrales de grandes gestores en candidatos y sectores), AG-B12 (propiedad institucional y crowding).
- **Sesgos y cautelas:** Desfase de hasta 45 días; solo posiciones largas en valores 13(f) de EE. UU.; tratamiento confidencial posible para algunas posiciones.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «SEC Form 13F frequently asked questions institutional investment managers»; WebFetch: sí)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada en verificación de alta 2026-11-02 (tanda 2); URL raíz corregida a la FAQ oficial del 13F. Reutilizada en F9 Bloque B (TFB-15) el 2026-11-02.

#### RF-0053 · Q 82 (A) — Investment Company Institute (ICI) — flujos de fondos

- **Canal oficial (URL raíz):** https://www.ici.org/research/stats/flows
- **Emisor:** Investment Company Institute
- **Documentación y notas:** Publicación semanal (miércoles) de los flujos estimados de fondos de inversión a largo plazo; la estimación de flujos combinados ETF + fondos se publica aparte; históricos descargables en ici.org. Última publicación vista: 28/10/2026 (semana cerrada el 21/10/2026).
- **Temática:** TFB-15 Posicionamiento, flujos y sentimiento (principal) · secundarias: TFB-08
- **Calidad Q:** 82 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 14/15 · Independencia 9/10 · Actualidad 8/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Flujos netos semanales de fondos de inversión de EE. UU.: renta variable (doméstica y mundial), mixtos, renta fija (gravable y municipal)
- **Motivo de inclusión y uso:** Dato primario de flujos de inversores en fondos de EE. UU. (cobertura ≈ 98 % de los activos del sector) para medir apetito por riesgo y rotaciones entre clases de activo. **Uso en el Bloque B:** AG-B10 (flujos semanales y mensuales a fondos y ETF por categoría como medida de demanda del inversor), AG-B13.
- **Restricciones de uso:** Uso con atribución; citar la semana de referencia y si la cifra excluye ETF.
- **Sesgos y cautelas:** Asociación sectorial; estimaciones semanales que se revisan; excluye ETF y fondos de fondos en la serie principal.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Investment Company Institute weekly estimated long-term mutual fund flows»; WebFetch: sí)
- **Origen:** Reutilizada del Bloque A (ID original) en F9 Bloque B (TFB-15) el 2026-11-02.

#### MBF-0514 · Q 81 (A) — Bundesanzeiger — publicación de posiciones cortas netas (Alemania)

- **Canal oficial (URL raíz):** https://www.bundesanzeiger.de/nlp/
- **Emisor:** Bundesanzeiger Verlag (sitio designado; supervisión de BaFin)
- **Documentación y notas:** Sitio central donde la autoridad nacional publica las posiciones cortas netas en acciones (artículo 9 del Reglamento (UE) 236/2012), según la lista oficial de ESMA (ESMA50-164-770 «Links to National Websites where Net Short Positions in Shares are Disclosed» (actualizado 13/05/2025): https://www.esma.europa.eu/sites/default/files/library/ssr_websites_ss_positions.pdf).
- **Temática:** TFB-15 Posicionamiento, flujos y sentimiento (principal) · secundarias: TFB-03
- **Calidad Q:** 81 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 14/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 9/10
- **Tipología:** primaria (declaraciones regulatorias publicadas por la autoridad)
- **Acceso:** Abierto
- **Ámbitos:** Posiciones cortas netas significativas en acciones admitidas en Alemania
- **Motivo de inclusión y uso:** Detecta apuestas bajistas de gestoras y fondos sobre candidatos de Alemania. Bloque B: AG-B10 (posicionamiento bajista y riesgo de short squeeze), AG-B12 (señal en el cribado de candidatos), AG-B14 (tesis contrarias).
- **Restricciones de uso:** Uso libre con cita de la autoridad y la fecha.
- **Sesgos y cautelas:** Solo se publican las posiciones que superan el umbral de publicación del Reglamento 236/2012 (las de notificación al supervisor, más bajas, no son públicas); no revela posiciones agregadas inferiores ni la cobertura subyacente.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «FINRA equity short interest data; ESMA net short positions notifications national competent authorities; CNMV posiciones cortas»; WebFetch: sí, lista oficial de ESMA (página índice); el sitio nacional no se leyó)
- **Origen:** Alta 2026-11-02 (F9 Bloque B, TFB-15).

#### RF-0346 · Q 81 (A) — CME Group — FedWatch Tool

- **Canal oficial (URL raíz):** https://www.cmegroup.com/markets/interest-rates/cme-fedwatch-tool.html
- **Emisor:** CME Group
- **Documentación y notas:** Probabilidades de decisiones del FOMC implícitas en futuros de fondos federales a 30 días; metodología publicada (cmegroup.com/articles/2023/understanding-the-cme-group-fedwatch-tool-methodology.html): árbol de probabilidades por reunión, movimientos de 25 pb, tipo efectivo no negativo.
- **Temática:** TFB-15 Posicionamiento, flujos y sentimiento (principal) · secundarias: TFB-02
- **Calidad Q:** 81 (A) — Primariedad 17/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 14/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto
- **Ámbitos:** Expectativas de mercado sobre el tipo de los fondos federales
- **Motivo de inclusión y uso:** Expectativas de política monetaria descontadas por el mercado (catalizador H1). **Uso en el Bloque B:** AG-B10 y AG-B08 (expectativas implícitas de tipos de la Fed: sentimiento de mercado sobre la política monetaria que afecta a sectores sensibles a tipos).
- **Restricciones de uso:** Condiciones de CME; citar fecha y hora.
- **Sesgos y cautelas:** Probabilidades de mercado (no previsión de la Fed); supuestos simplificadores.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «CME FedWatch Tool fed funds target rate probabilities»; WebFetch: sí, página de metodología)
- **Origen:** Reutilizada del Bloque A (ID original) en F9 Bloque B (TFB-15) el 2026-11-02.

#### FXF-0201 · Q 80 (A) — Federal Reserve Bank of Minneapolis — Market-Based Probabilities (probabilidades implícitas en opciones, incluidos tipos de cambio)

- **Canal oficial (URL raíz):** https://www.minneapolisfed.org/banking/current-and-historical-market-based-probabilities (antecedentes y metodología: https://minneapolisfed.org/banking/current-and-historical-market--based-probabilities/market-based-probabilities-background-commentary-and-analysis)
- **Emisor:** Federal Reserve Bank of Minneapolis
- **Documentación y notas:** Distribuciones de probabilidad neutrales al riesgo derivadas de precios de cierre de opciones con volumen positivo en los cinco días previos; cubre materias primas, renta variable, tipos de interés y tipos de cambio (opciones sobre futuros de tipos de cambio individuales; el euro como ejemplo). Ofrece gráficos de estadísticos históricos y descarga CSV de estadísticos con diccionario de datos. Las probabilidades de inflación se interrumpieron en mayo de 2025. Archivo de informes PDF desde 2012.
- **Temática:** TFB-15 Posicionamiento, flujos y sentimiento (principal) · secundarias: TFB-06
- **Calidad Q:** 80 (A) — Primariedad 17/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 14/15 · Independencia 10/10 · Actualidad 7/10 · Acceso 9/10
- **Tipología:** primaria (cálculo propio de un banco de la Reserva Federal sobre precios de opciones)
- **Acceso:** Abierto
- **Ámbitos:** Densidades implícitas, probabilidades de grandes movimientos, sesgo y curtosis implícitos por activo, incluidos tipos de cambio
- **Motivo de inclusión y uso:** Única fuente oficial abierta que publica densidades implícitas de tipos de cambio con método documentado. Uso: TR-PFV (AG-21) para probabilidades de movimientos extremos por par; CONTRA (AG-11) para comprobar lo que ya descuenta el mercado de opciones; PROS (AG-10) como referencia de bandas de probabilidad.
- **Restricciones de uso:** Uso libre con atribución; citar fecha y activo.
- **Sesgos y cautelas:** Densidades neutrales al riesgo (incluyen prima de riesgo); cobertura de divisas limitada a los futuros con opciones líquidas; la página no detalla la lista completa de divisas.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Interrupción de la serie de inflación (mayo de 2025); vigilar posibles recortes de cobertura.
- **Uso en el bloque:** AG-B10 Flujos y Sentimiento: probabilidades implícitas de grandes movimientos en índices, materias primas y tipos (lo que ya descuenta el mercado); AG-B14 Contrarias: contraste de consenso; AG-B13 Prospectiva: bandas de probabilidad.
- **Origen:** Reutilizada con su ID de F9 Forex V1.0; temática reasignada a TFB-15 el 2026-11-03.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Minneapolis Fed market-based probabilities currencies euro yen option prices»; WebFetch: sí, página principal)

#### RF-0345 · Q 79 (B) — EFAMA — estadísticas de fondos europeos

- **Canal oficial (URL raíz):** https://efama.org/node/501
- **Emisor:** European Fund and Asset Management Association (EFAMA)
- **Documentación y notas:** Estadísticas mensuales y trimestrales de UCITS y AIF (patrimonio y ventas netas), estadística internacional trimestral con ICI para IIFA y Fact Book. 2T 2026: 27,51 billones de euros de patrimonio y 267.000 M€ de entradas netas, con récord de ventas de ETF UCITS (117.000 M€).
- **Temática:** TFB-15 Posicionamiento, flujos y sentimiento (principal) · secundarias: TFB-08
- **Calidad Q:** 79 (B) — Primariedad 18/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 14/15 · Independencia 7/10 · Actualidad 8/10 · Acceso 9/10
- **Tipología:** primaria
- **Acceso:** Abierto (resúmenes); más datos para miembros
- **Ámbitos:** Flujos y patrimonio de fondos europeos por categoría
- **Motivo de inclusión y uso:** Contraparte europea de RF-0053 (ICI) para medir flujos de inversores. **Uso en el Bloque B:** AG-B10 (ventas netas de fondos UCITS/FIA europeos por categoría), AG-B12 (demanda de ETF y fondos del ámbito).
- **Restricciones de uso:** Citar trimestre o mes.
- **Sesgos y cautelas:** Asociación sectorial; datos agregados de asociaciones nacionales.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «EFAMA fund market statistics quarterly UCITS AIF net sales»; WebFetch: sí)
- **Origen:** Reutilizada del Bloque A (ID original) en F9 Bloque B (TFB-15) el 2026-11-02.

#### FXF-0099 · Q 74 (B) — CLS Group — CLSMarketData (volúmenes, flujos y posiciones de divisas)

- **Canal oficial (URL raíz):** https://www.cls-group.com/products/data/clsmarketdata/ (página de publicaciones: https://www.cls-group.com/publications/clsmarketdata/)
- **Emisor:** CLS Group (infraestructura de liquidación de divisas)
- **Documentación y notas:** Conjuntos de datos alternativos derivados de las operaciones liquidadas en CLSSettlement (más del 50 % del volumen mundial en las 18 divisas que liquida; más de 3.000 millones de operaciones desde 2011): FX Volume (contado, *forwards* y *swaps* en 40 pares), FX Flow (flujos por segmentos económicos, señal direccional), FX Outstanding (posiciones netas a partir de *forwards* y *swaps* vivos) y FX Pricing.
- **Temática:** TFB-15 Posicionamiento, flujos y sentimiento (principal) · secundarias: TFB-06
- **Calidad Q:** 74 (B) — Primariedad 18/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 13/15 · Independencia 8/10 · Actualidad 9/10 · Acceso 5/10
- **Tipología:** primaria (datos de liquidación)
- **Acceso:** Con licencia (presentación pública)
- **Ámbitos:** Volumen y flujo del mercado de divisas con alta frecuencia; flujos por segmentos económicos y posiciones netas a plazo
- **Motivo de inclusión y uso:** Única fuente de flujos reales de alta frecuencia del mercado OTC de divisas. **Uso en el Bloque B:** AG-B10 (flujos y posiciones de divisas como contexto para ámbitos expuestos al tipo de cambio).
- **Restricciones de uso:** Solo contenidos públicos citables sin licencia (regla F9-c).
- **Sesgos posibles:** Solo divisas y operaciones liquidadas en CLS (sin la mayoría de emergentes ni NDF).
- **Historial de exactitud:** No aplicable (dato).
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «CLS FX market volume data CLSMarketData»; WebFetch: sí, página de producto y de publicaciones)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-05). Reutilizada en F9 Bloque B (TFB-15) el 2026-11-02.

#### RF-0300 · Q 74 (B) — AAII — Investor Sentiment Survey

- **Canal oficial (URL raíz):** https://www.aaii.com/sentimentsurvey
- **Emisor:** American Association of Individual Investors (AAII)
- **Documentación y notas:** Encuesta semanal a miembros (votación de jueves a miércoles; publicación los jueves) desde julio de 1987. Promedios históricos publicados: alcistas 37,5 %, neutrales 31,0 %, bajistas 31,5 %. Lectura vista: semana al 28/10/2026 (37,8 / 20,7 / 41,4).
- **Temática:** TFB-15 Posicionamiento, flujos y sentimiento (principal) · secundarias: TFB-10
- **Calidad Q:** 74 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 12/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 6/10
- **Tipología:** primaria
- **Acceso:** Lectura semanal gratuita; histórico completo solo para miembros (de pago)
- **Ámbitos:** Sentimiento del inversor minorista estadounidense (alcista/neutral/bajista)
- **Motivo de inclusión y uso:** Indicador contrario clásico de sentimiento minorista con serie larga. **Uso en el Bloque B:** AG-B10 (sentimiento minorista semanal como indicador contrario), AG-B14.
- **Restricciones de uso:** Condiciones de AAII; citar semana y porcentajes.
- **Sesgos y cautelas:** Muestra autoseleccionada de miembros; ruido semanal elevado.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Encuesta postal hasta 2000, en línea desde entonces.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «AAII Investor Sentiment Survey NAAIM Exposure Index Cboe put/call ratio FINRA margin statistics»; WebFetch: sí)
- **Origen:** Reutilizada del Bloque A (ID original) en F9 Bloque B (TFB-15) el 2026-11-02.

#### RF-0528 · Q 72 (B) — LSEG Lipper — U.S. Weekly FundFlows Insight Report (Lipper Alpha)

- **Canal oficial (URL raíz):** https://lipperalpha.refinitiv.com/ (ejemplo leído: https://lipperalpha.refinitiv.com/2024/05/u-s-weekly-fundflows-insight-report-fund-market-reports-first-outflow-in-six-weeks/)
- **Emisor:** LSEG Lipper (London Stock Exchange Group)
- **Documentación y notas:** Informe semanal de flujos netos de fondos de inversión y ETF de EE. UU. por clasificación Lipper (renta variable, renta fija, mixtos, monetarios, materias primas, alternativos, ETF de bitcoin al contado), con rentabilidades de índices y tipos; semana de jueves a miércoles; datos de Lipper Global Fund Flows.
- **Temática:** TFB-15 Posicionamiento, flujos y sentimiento (principal) · secundarias: TFB-08
- **Calidad Q:** 72 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 13/15 · Independencia 7/10 · Actualidad 8/10 · Acceso 7/10
- **Tipología:** secundaria (proveedor de datos)
- **Acceso:** Comentarios abiertos; datos completos bajo licencia
- **Ámbitos:** Flujos semanales de fondos y ETF por clasificación
- **Motivo de inclusión y uso:** Contraste semanal de los flujos de ICI (RF-0053) con desglose por clasificación más fino. **Uso en el Bloque B:** AG-B10 (flujos semanales de fondos y ETF de EE. UU. por clase y sector), AG-B13.
- **Restricciones de uso:** Uso con atribución.
- **Sesgos y cautelas:** Muestra del propio proveedor; la última pieza leída es de 2024 (comprobar continuidad del blog tras la migración de marca Refinitiv a LSEG).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Refinitiv integrada en LSEG (2021).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «LSEG Lipper weekly fund flows report US ETFs mutual funds»; WebFetch: sí)
- **Origen:** Alta F9_S4 (2026-11-02). Reutilizada en F9 Bloque B (TFB-15) el 2026-11-02.

#### FXF-0077 · Q 70 (B) — Institute of International Finance (IIF) — Capital Flows Tracker

- **Canal oficial (URL raíz):** https://www.iif.com/Products/Capital-Flows-Tracker/lapg-7321/22 (lanzamiento: https://www.iif.com/About-Us/Press/View/ID/1152/IIFs-New-Capital-Flows-Tracker-Sees-Pick-up-in-Portfolio-Flows-to-Emerging-Markets)
- **Emisor:** Institute of International Finance (asociación de entidades financieras)
- **Documentación y notas:** Estimaciones mensuales de flujos de cartera (deuda y renta variable) hacia mercados emergentes, publicadas la última semana de cada mes desde el 26/03/2014; usan datos diarios de las economías que los publican. Los informes completos son para miembros; los titulares se difunden en notas de prensa.
- **Temática:** TFB-15 Posicionamiento, flujos y sentimiento (principal) · secundarias: TFB-02
- **Calidad Q:** 70 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 13/15 · Independencia 6/10 · Actualidad 10/10 · Acceso 7/10
- **Tipología:** secundaria cualificada (estimaciones propias a partir de datos oficiales)
- **Acceso:** Restringido a miembros (titulares públicos)
- **Ámbitos:** Flujos de cartera de no residentes hacia emergentes, por país y clase de activo
- **Motivo de inclusión y uso:** Indicador de alta frecuencia de entradas y salidas de capital en emergentes, adelantado a la balanza de pagos oficial. **Uso en el Bloque B:** AG-B10 (flujos de cartera hacia mercados emergentes por país), AG-B08 (ámbitos geográficos emergentes).
- **Restricciones de uso:** Solo contenidos públicos citables (regla F9-c).
- **Sesgos posibles:** Asociación de la industria financiera; estimaciones que se revisan con los datos oficiales.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Rebautizado de «Portfolio Flows Tracker» a «Capital Flows Tracker».
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «IIF Capital Flows Tracker emerging markets portfolio flows»; WebFetch: sí, nota de prensa de lanzamiento)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-04). Reutilizada en F9 Bloque B (TFB-15) el 2026-11-02.

#### RF-0301 · Q 70 (B) — NAAIM — Exposure Index

- **Canal oficial (URL raíz):** https://www.naaim.org/
- **Emisor:** National Association of Active Investment Managers (NAAIM)
- **Documentación y notas:** Exposición media a la renta variable de EE. UU. declarada por gestores activos miembros, actualizada semanalmente (según el catálogo DecisionPoint de StockCharts, que cita naaim.org como fuente).
- **Temática:** TFB-15 Posicionamiento, flujos y sentimiento (principal) · secundarias: TFB-11
- **Calidad Q:** 70 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 10/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 8/10
- **Tipología:** primaria
- **Acceso:** Abierto (lectura semanal)
- **Ámbitos:** Posicionamiento de gestores activos en renta variable estadounidense
- **Motivo de inclusión y uso:** Complemento profesional al sentimiento minorista (RF-0300) para medir crowding. **Uso en el Bloque B:** AG-B10 (exposición de gestores activos a renta variable de EE. UU.), AG-B14.
- **Restricciones de uso:** Citar semana y valor.
- **Sesgos y cautelas:** Muestra pequeña y autodeclarada; asociación sectorial.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «AAII Investor Sentiment Survey NAAIM Exposure Index Cboe put/call ratio FINRA margin statistics»; URL tomada del catálogo DecisionPoint de StockCharts, leído con WebFetch; WebFetch al sitio: no)
- **Origen:** Reutilizada del Bloque A (ID original) en F9 Bloque B (TFB-15) el 2026-11-02.

#### FXF-0269 · Q 68 (B) — Economic Policy Uncertainty (EPU) — índices de incertidumbre de política económica (Baker, Bloom y Davis)

- **Canal oficial (URL raíz):** www.PolicyUncertainty.com (según NBER WP 26243: https://www.nber.org/papers/w26243.pdf)
- **Emisor:** Scott R. Baker, Nicholas Bloom y Steven J. Davis (proyecto académico)
- **Documentación y notas:** Índices de incertidumbre construidos con noticias de prensa (Baker, Bloom y Davis, 2016), con actualizaciones mensuales en PolicyUncertainty.com según Davis (2019), «Rising Policy Uncertainty», NBER WP 26243. Macrosynergy lo clasifica entre las medidas de incertidumbre basadas en noticias.
- **Temática:** TFB-15 Posicionamiento, flujos y sentimiento (principal) · secundarias: TFB-02
- **Calidad Q:** 68 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 14/15 · Independencia 9/10 · Actualidad 4/10 · Acceso 4/10
- **Tipología:** primaria (índice académico construido por los autores)
- **Acceso:** Abierto (descargas en el sitio del proyecto); canal no leído en esta verificación
- **Ámbitos:** Incertidumbre de política económica por país, incertidumbre de política monetaria y comercial
- **Motivo de inclusión y uso:** Medida cuantitativa del riesgo político usada en la literatura de divisas (prima de riesgo y refugio). **Uso en el Bloque B:** AG-B07 y AG-B10 (incertidumbre de política económica como factor de sentimiento sectorial y por país), MC-B05 (variable explicativa).
- **Restricciones de uso:** Uso académico con cita de los autores.
- **Sesgos posibles:** Basado en recuentos de prensa; sesgo hacia países con prensa digitalizada.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Revisiones de la base de periódicos; vigilar.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «policyuncertainty.com Economic Policy Uncertainty index Geopolitical Risk index Caldara Iacoviello World Uncertainty Index data»; WebFetch: sí, NBER WP 26243 y Macrosynergy; el sitio PolicyUncertainty.com no se leyó)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-09). Reutilizada en F9 Bloque B (TFB-15) el 2026-11-02.

#### MBF-0625 · Q 68 (B) — Google — Google Trends (índice de volumen de búsquedas como medida de atención)

- **Canal oficial (URL raíz):** https://rady.ucsd.edu/faculty/directory/engelberg/pub/portfolios/GOOGLE.pdf (página índice: Da, Engelberg y Gao, «In Search of Attention», que documenta la fuente; sitio: http://www.google.com/trends)
- **Emisor:** Google LLC
- **Documentación y notas:** Índice de volumen de búsquedas (SVI) normalizado por término, región y periodo. Da, Engelberg y Gao lo usan para los tickers del Russell 3000 (2004–2008): el SVI anómalo (log SVI semanal menos la mediana de las 8 semanas previas) adelanta otras medidas de atención, refleja sobre todo atención minorista y predice subidas a dos semanas con reversión en un año.
- **Temática:** TFB-15 Posicionamiento, flujos y sentimiento (principal) · secundarias: TFB-04
- **Calidad Q:** 68 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 7/15 · Autoridad 10/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria (dato de comportamiento de búsqueda)
- **Acceso:** Abierto, sin registro
- **Ámbitos:** Interés de búsqueda por término, tema, país y periodo (desde 2004)
- **Motivo de inclusión y uso:** Medida directa y gratuita de la atención minorista hacia empresas, productos y temáticas; también aproxima la adopción de productos.
- **Restricciones de uso:** Condiciones de Google; datos normalizados (0–100) y muestreados.
- **Sesgos y cautelas:** Índice relativo y muestreado (puede variar entre descargas); términos ambiguos; sin metodología pública detallada. Verificado solo vía página índice.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Cambios periódicos en la recogida y la categorización de datos anunciados por Google.
- **Uso en el bloque:** AG-B10 Flujos y Sentimiento: atención minorista hacia candidatos y temáticas (euforia o desinterés); AG-B04 Demanda y Adopción: interés por productos y marcas; AG-B14 Contrarias: señales de exceso de atención.
- **Origen:** Alta F9_comp (2026-11-03).
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-03 (búsqueda web: «SEC fails-to-deliver data and Google Trends as investor attention sentiment indicator data source»; WebFetch: sí, artículo de Da, Engelberg y Gao como página índice)

#### RF-0347 · Q 68 (B) — Crane Data — datos de fondos del mercado monetario

- **Canal oficial (URL raíz):** https://www.cranedata.com/archives/all-articles/4480/
- **Emisor:** Crane Data LLC
- **Documentación y notas:** Editor de noticias y datos de fondos monetarios: Money Fund Intelligence (mensual, con versión XLS), Money Fund Wisdom, conferencias; noticias diarias (p. ej., patrimonio mundial de fondos monetarios de 13,7 billones de dólares según MFI).
- **Temática:** TFB-15 Posicionamiento, flujos y sentimiento (principal) · secundarias: TFB-02
- **Calidad Q:** 68 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 11/15 · Independencia 8/10 · Actualidad 9/10 · Acceso 6/10
- **Tipología:** secundaria
- **Acceso:** Noticias abiertas; datos de pago
- **Ámbitos:** Patrimonio, rentabilidades y flujos de fondos monetarios
- **Motivo de inclusión y uso:** Seguimiento del «efectivo al margen» como munición potencial para activos de riesgo. **Uso en el Bloque B:** AG-B10 (liquidez aparcada en fondos monetarios como «dinero en espera»), AG-B08.
- **Restricciones de uso:** Citar publicación y fecha; datos completos solo por suscripción.
- **Sesgos y cautelas:** Proveedor comercial; artículo leído de 2013.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin datos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «New York Fed primary dealer statistics weekly positions»; WebFetch: sí)
- **Origen:** Reutilizada del Bloque A (ID original) en F9 Bloque B (TFB-15) el 2026-11-02.

#### FXF-0271 · Q 62 (C) — Geopolitical Risk Index (GPR) — índice de riesgo geopolítico (Caldara e Iacoviello)

- **Canal oficial (URL raíz):** No capturado en la verificación (página de los autores). Pieza índice: https://macrosynergy.com/?p=40564 (taxonomía de medidas de riesgo; cita Datta et al., 2017, IFDP 1216)
- **Emisor:** Dario Caldara y Matteo Iacoviello (Federal Reserve Board)
- **Documentación y notas:** Índice basado en recuentos de prensa sobre riesgo de guerra, terrorismo y tensiones geopolíticas (Caldara e Iacoviello, 2016, según la taxonomía recogida por Macrosynergy).
- **Temática:** TFB-15 Posicionamiento, flujos y sentimiento (principal) · secundarias: TFB-05
- **Calidad Q:** 62 (C) — Primariedad 14/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 13/15 · Independencia 9/10 · Actualidad 3/10 · Acceso 2/10
- **Tipología:** primaria (índice académico)
- **Acceso:** Canal no verificado; HT-02 debe localizar la página oficial
- **Ámbitos:** Riesgo geopolítico global y por país
- **Motivo de inclusión y uso:** Medida estándar de riesgo geopolítico para estudiar el comportamiento de las divisas refugio (JPY, CHF, USD). **Uso en el Bloque B:** AG-B07 y AG-B10 (riesgo geopolítico como factor de sentimiento para defensa, energía y cadenas de suministro), MC-B05.
- **Restricciones de uso:** Uso académico con cita.
- **Sesgos posibles:** Sesgo de cobertura de prensa anglosajona.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Revisiones del índice publicadas por los autores; no comprobadas.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «policyuncertainty.com Economic Policy Uncertainty index Geopolitical Risk index Caldara Iacoviello World Uncertainty Index data»; WebFetch: sí, sobre Macrosynergy)
- **Origen:** Alta 2026-11-02 (F9 Forex, TFX-09). Reutilizada en F9 Bloque B (TFB-15) el 2026-11-02.

## TFB-16 Contratación pública, ayudas y política industrial

#### MBF-0401 · Q 87 (A) — TED (Tenders Electronic Daily) — anuncios de contratación pública de la UE y datos abiertos

- **Canal oficial (URL raíz):** https://ted.europa.eu/ (descripción oficial: https://single-market-economy.ec.europa.eu/single-market/public-procurement/digital-procurement/tenders-electronic-daily_en)
- **Emisor:** Oficina de Publicaciones de la UE y Comisión Europea (DG GROW)
- **Documentación y notas:** Versión en línea del Suplemento del Diario Oficial (DO S): más de 250 números al año, unos 800.000 anuncios anuales de planificación, licitación y adjudicación por valor superior a 815.000 millones de euros, en el estándar eForms. Todos los anuncios están disponibles en XML en data.europa.eu; DG GROW ofrece además un subconjunto CSV (solo algunos años, países y tipos de anuncio).
- **Temática:** TFB-16 Contratación pública, ayudas y política industrial (principal) · secundarias: TFB-03, TFB-01
- **Calidad Q:** 87 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** primaria (anuncios oficiales de los poderes adjudicadores)
- **Acceso:** Abierto (datos abiertos en data.europa.eu)
- **Ámbitos:** Licitaciones y adjudicaciones por encima de los umbrales UE en los 27 Estados miembros y el EEE
- **Motivo de inclusión y uso:** Mide la demanda pública por CPV, país y comprador y quién gana los contratos. Bloque B: AG-B04 (demanda pública de un sector: defensa, sanidad, obra civil, TIC), AG-B07 (ciclos de gasto y prioridades regulatorias), AG-B12 (cartera de adjudicaciones de candidatos cotizados) y MC-B02 (dimensionado del segmento público del mercado).
- **Restricciones de uso:** Reutilización libre de los datos abiertos de la UE con cita; el CSV de DG GROW es parcial.
- **Sesgos y cautelas:** Solo contratos sobre umbrales UE; calidad desigual de los campos de valor y adjudicatario; un mismo contrato puede aparecer en varios anuncios (riesgo de doble cómputo).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «TED Tenders Electronic Daily open data API public procurement notices EU»; WebFetch: sí, página de la Comisión sobre TED)
- **Origen:** Alta 2026-11-02 (F9 Bloque B, TFB-16).

#### MBF-0603 · Q 87 (A) — Consejo de Seguridad de las Naciones Unidas — Lista consolidada de sanciones (UN Security Council Consolidated List)

- **Canal oficial (URL raíz):** https://main.un.org/securitycouncil/en/content/un-sc-consolidated-list (antes https://www.un.org/sc/suborg/en/sanctions/un-sc-consolidated-list.html, redirigida)
- **Emisor:** Consejo de Seguridad de las Naciones Unidas (Secretaría; comités de sanciones)
- **Documentación y notas:** Reúne en una sola lista a todas las personas y entidades sujetas a medidas del Consejo de Seguridad (733 personas y 274 entidades en la versión del 29/10/2026), con número de referencia permanente cuyo prefijo identifica el comité (1267/1989 ISIL y Al-Qaida «QD», 1718 RPDC «KP», 1737 Irán «IR», 1970 Libia «LY», 1988 talibanes «TA», etc.). Descarga en PDF, XML y HTML por orden alfabético o por referencia; buscador; comunicados de prensa por cambio y lista de correo.
- **Temática:** TFB-16 Contratación pública, ayudas y política industrial (principal) · secundarias: TFB-01
- **Calidad Q:** 87 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria (decisiones del Consejo de Seguridad)
- **Acceso:** Abierto, sin registro (PDF, XML, HTML)
- **Ámbitos:** Sanciones de la ONU por régimen y comité (14 regímenes)
- **Motivo de inclusión y uso:** Capa multilateral de sanciones que los Estados miembros deben aplicar; base común de las listas de la UE y del Reino Unido.
- **Restricciones de uso:** Uso libre; cada versión sustituye a las anteriores.
- **Sesgos y cautelas:** La inclusión en una lista consolidada no implica un mismo régimen ni criterios iguales; las razones de inclusión están en la página de cada comité.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Cambio de dominio a main.un.org (redirección 302 observada el 03/11/2026).
- **Uso en el bloque:** AG-B07 Regulación y Geopolítica: sanciones multilaterales que afectan a mercados geográficos (RPDC, Irán, Libia…) y a sectores (armas, transporte marítimo); AG-B12: filtro de exclusión de contrapartes.
- **Origen:** Alta F9_comp (2026-11-03).
- **Estado:** Aprobada
- **Estado del enlace:** REDIRIGIDO
- **Última verificación:** 2026-11-03 (búsqueda web: «United Nations Security Council Consolidated List sanctions download»; WebFetch: sí, URL redirigida)

#### MBF-0402 · Q 86 (A) — Plataforma de Contratación del Sector Público (PLACSP) — conjuntos de datos abiertos de licitaciones

- **Canal oficial (URL raíz):** https://www.hacienda.gob.es/es-es/gobiernoabierto/datos%20abiertos/paginas/licitaciones_plataforma_contratacion.aspx
- **Emisor:** Ministerio de Hacienda (Dirección General del Patrimonio del Estado), España
- **Documentación y notas:** Seis conjuntos de datos: licitaciones en perfiles de contratante (sin menores), licitaciones por mecanismos de agregación (desde 01/01/2016), contratos menores (desde 01/01/2018), encargos a medios propios (desde 01/07/2021), consultas preliminares de mercado (desde 01/04/2022) y relación de perfiles de contratante (XLSX). Datos de licitaciones desde el 1 de enero de 2012. Incluye la herramienta OpenPLACSP, especificación de sindicación y recurso CODICE.
- **Temática:** TFB-16 Contratación pública, ayudas y política industrial (principal) · secundarias: TFB-03
- **Calidad Q:** 86 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** primaria (publicación oficial de los órganos de contratación)
- **Acceso:** Abierto (información pública disponible para su reutilización)
- **Ámbitos:** Contratación pública española (Estado, CC. AA. agregadas y entidades locales)
- **Motivo de inclusión y uso:** Fuente primaria de la demanda pública española por sector y comprador. Bloque B: AG-B04 y AG-B07 (gasto público y plan de recuperación), AG-B12 (adjudicatarios cotizados españoles, p. ej. constructoras, ingenierías, TIC) y HT-11 (cribado de universos de proveedores).
- **Restricciones de uso:** Reutilización libre (la página no nombra licencia concreta); citar conjunto y fecha de descarga.
- **Sesgos y cautelas:** Formatos técnicos (ATOM/CODICE) que exigen procesamiento; cobertura autonómica vía agregación con diferencias de calidad.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Plataforma de Contratación del Sector Público datos abiertos licitaciones sindicación»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9 Bloque B, TFB-16).

#### MBF-0403 · Q 86 (A) — USAspending.gov — base oficial del gasto federal de EE. UU. (contratos, subvenciones, préstamos)

- **Canal oficial (URL raíz):** https://www.usaspending.gov
- **Emisor:** U.S. Department of the Treasury (Bureau of the Fiscal Service)
- **Documentación y notas:** Registros históricos de adjudicaciones de contratos, subvenciones, préstamos y otra asistencia financiera desde 2000, con importe, beneficiario, agencia y código NAICS; descrita como «the official public database of all federal spending». Dispone de API pública.
- **Temática:** TFB-16 Contratación pública, ayudas y política industrial (principal) · secundarias: TFB-03, TFB-01
- **Calidad Q:** 86 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** primaria (datos oficiales de adjudicaciones federales)
- **Acceso:** Abierto (dominio público)
- **Ámbitos:** Gasto federal de EE. UU. por agencia, programa, beneficiario y sector
- **Motivo de inclusión y uso:** Cuantifica la exposición de empresas y sectores al gasto federal (defensa, sanidad, TI, infraestructura, IRA/CHIPS). Bloque B: AG-B04 (demanda pública), AG-B07 (dependencia política de ingresos), AG-B12 (peso del cliente federal en candidatos) y MC-B09 (riesgo de concentración en un cliente público).
- **Restricciones de uso:** Uso libre; citar fecha de extracción, ya que las adjudicaciones se modifican.
- **Sesgos y cautelas:** No lista oportunidades abiertas; calidad de los datos según la agencia notificante; modificaciones y desobligaciones posteriores.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «USAspending.gov API federal contracts grants data SAM.gov contract opportunities»; WebFetch: sí, página índice govprocure.northwest.net/databases.html; el sitio oficial no se leyó)
- **Origen:** Alta 2026-11-02 (F9 Bloque B, TFB-16).

#### MBF-0604 · Q 86 (A) — FCDO (Reino Unido) — UK Sanctions List (sustituye a la lista consolidada de la OFSI)

- **Canal oficial (URL raíz):** https://gov.uk/government/publications/the-uk-sanctions-list (buscador: search-uk-sanctions-list.service.gov.uk · lista OFSI cerrada: https://www.gov.uk/government/publications/financial-sanctions-consolidated-list-of-targets)
- **Emisor:** Foreign, Commonwealth & Development Office (FCDO), Sanctions Directorate; la OFSI (HM Treasury) aplica las sanciones financieras
- **Documentación y notas:** Personas, entidades y buques designados con arreglo a la Sanctions and Anti-Money Laundering Act 2018, con los motivos de cada designación. Descargas en HTML, texto, CSV, ODT, ODS, XML y PDF, esquema XML y guía de formato; buscador con guía de usuario (12/02/2026). La OFSI Consolidated List of Asset Freeze Targets cerró el 28/01/2026: desde entonces la UK Sanctions List es la única fuente de todas las designaciones británicas (la de la OFSI queda solo como referencia). Última actualización vista: 30/10/2026.
- **Temática:** TFB-16 Contratación pública, ayudas y política industrial (principal) · secundarias: TFB-03
- **Calidad Q:** 86 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria (designaciones oficiales)
- **Acceso:** Abierto, sin registro
- **Ámbitos:** Sanciones del Reino Unido por régimen (Rusia, ciberataques, ISIL y Al-Qaida, Irán…), incluidas sanciones financieras y de transporte
- **Motivo de inclusión y uso:** Fuente primaria única de las designaciones británicas tras el cierre de la lista OFSI; complemento de UE, ONU y OFAC.
- **Restricciones de uso:** Uso libre (Open Government Licence en GOV.UK); para cumplimiento usar la versión vigente.
- **Sesgos y cautelas:** Las fichas antiguas que citen la lista OFSI deben migrar a esta fuente; las designaciones reflejan la política exterior británica.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Cierre de la lista consolidada de la OFSI el 28/01/2026 y concentración en la UK Sanctions List del FCDO.
- **Uso en el bloque:** AG-B07 Regulación y Geopolítica: exposición de sectores y emisores a sanciones británicas (incluidos buques y comercio marítimo); AG-B12 Seleccionador de Activos: filtro de exclusión; AG-B11: riesgo de cumplimiento.
- **Origen:** Alta F9_comp (2026-11-03).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-03 (búsquedas web: «OFSI consolidated list of asset freeze targets UK sanctions list gov.uk» y «"UK Sanctions List" FCDO only source designations 28 January 2026 download»; WebFetch: sí, ambas páginas de GOV.UK)

#### FXF-0264 · Q 85 (A) — OFAC (Tesoro de EE. UU.) — listas de sanciones (SDN y Consolidated Non-SDN)

- **Canal oficial (URL raíz):** https://ofac.treasury.gov/ofac-sanctions-lists (ficha de la búsqueda de sanciones, ejemplo: https://sanctionssearch.ofac.treas.gov/Details.aspx?id=38037)
- **Emisor:** Office of Foreign Assets Control, U.S. Department of the Treasury
- **Documentación y notas:** Lista SDN (personas, entidades, buques y aeronaves bloqueados) y Consolidated Non-SDN; Sanctions List Service con descargas, conjuntos personalizados por programa, búsqueda difusa, archivos delta por año y formato «Advanced Sanctions Data Model». Avisos en «Recent Actions» y por correo (GovDelivery); página de programas por país.
- **Temática:** TFB-16 Contratación pública, ayudas y política industrial (principal) · secundarias: TFB-03
- **Calidad Q:** 85 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria (acto administrativo)
- **Acceso:** Abierto
- **Ámbitos:** Sanciones financieras de EE. UU. por programa y país
- **Motivo de inclusión y uso:** Fuente primaria de las sanciones que afectan a la convertibilidad, a los bancos centrales sancionados y al uso del dólar. Uso: capa transversal de geopolítica y sanciones; AS-EMEA (AG-07) y AS-EMAS (AG-05) para divisas con riesgo de sanciones; CONTRA (AG-11).
- **Restricciones de uso:** Uso libre; para cumplimiento normativo usar siempre la versión vigente.
- **Sesgos y cautelas:** Decisiones de política exterior de EE. UU.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Migración al Advanced Sanctions Data Model; cambios técnicos documentados en su página.
- **Uso en el bloque:** AG-B07 Regulación y Geopolítica: exposición de sectores, cadenas de suministro y empresas a sanciones de EE. UU. por programa y país; AG-B12 Seleccionador de Activos: filtro de exclusión de emisores o contrapartes sancionados; AG-B11: riesgo de cumplimiento.
- **Origen:** Reutilizada con su ID de F9 Forex V1.0; temática reasignada a TFB-16 el 2026-11-03.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «OFAC Sanctions List Service SDN list search EU Sanctions Map official»; WebFetch: sí)

#### MBF-0410 · Q 85 (A) — Comisión Europea — Recovery and Resilience Scoreboard (Mecanismo de Recuperación y Resiliencia)

- **Canal oficial (URL raíz):** https://ec.europa.eu/economy_finance/recovery-and-resilience-scoreboard/
- **Emisor:** Comisión Europea (DG ECFIN)
- **Documentación y notas:** Plataforma pública de seguimiento del MRR y de cada plan nacional: hitos y objetivos cumplidos, solicitudes de pago y desembolsos, 14 indicadores comunes (Reglamento Delegado de 2/12/2021), financiación por área política y desglose de gasto verde, digital y social; base de los informes anuales sobre el MRR.
- **Temática:** TFB-16 Contratación pública, ayudas y política industrial (principal) · secundarias: TFB-01
- **Calidad Q:** 85 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria (datos de seguimiento oficial)
- **Acceso:** Abierto
- **Ámbitos:** NextGenerationEU: ejecución del MRR por Estado miembro
- **Motivo de inclusión y uso:** Mide el ritmo real de los fondos NextGen por país y área. Bloque B: AG-B07 y AG-B08 (impulso fiscal sectorial), AG-B13 (riesgo de fin de programa en 2026), AG-B04.
- **Restricciones de uso:** Reutilización con cita.
- **Sesgos y cautelas:** Hitos cumplidos no equivalen a gasto final en la economía real; indicadores declarados por los Estados.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Recovery and Resilience Scoreboard data Kohesio EU funded projects open data»; WebFetch: sí, noticia de data.europa.eu que describe el Scoreboard; la página del Scoreboard no se leyó)
- **Origen:** Alta 2026-11-02 (F9 Bloque B, TFB-16).

#### MBF-0404 · Q 84 (A) — SAM.gov — oportunidades de contratación federal y registro de proveedores (EE. UU.)

- **Canal oficial (URL raíz):** https://sam.gov
- **Emisor:** U.S. General Services Administration (GSA)
- **Documentación y notas:** Registro obligatorio de proveedores para cobrar del Gobierno federal y publicación de licitaciones abiertas con plazos, códigos NAICS, reservas (set-asides) y contactos. No contiene subvenciones ni histórico de adjudicaciones (para eso, USAspending, MBF-0403).
- **Temática:** TFB-16 Contratación pública, ayudas y política industrial (principal) · secundarias: TFB-03
- **Calidad Q:** 84 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria (anuncios oficiales de licitación)
- **Acceso:** Abierto; la API requiere clave gratuita
- **Ámbitos:** Licitaciones federales en curso de EE. UU.
- **Motivo de inclusión y uso:** Señal adelantada de la demanda federal (licitaciones antes de la adjudicación). Bloque B: AG-B04 y AG-B13 (cartera de oportunidades del sector), AG-B12 (proveedores registrados en un nicho).
- **Restricciones de uso:** Uso libre; API con clave gratuita (custodia en HT-01).
- **Sesgos y cautelas:** Las licitaciones no garantizan adjudicación; descripciones heterogéneas.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «USAspending.gov API federal contracts grants data SAM.gov contract opportunities»; WebFetch: sí, página índice govprocure.northwest.net/databases.html)
- **Origen:** Alta 2026-11-02 (F9 Bloque B, TFB-16).

#### MBF-0406 · Q 84 (A) — Comisión Europea (DG COMP) — buscador de casos de ayudas de Estado

- **Canal oficial (URL raíz):** https://competition-cases.ec.europa.eu/search?caseInstrument=SA (enlazado desde https://competition-policy.ec.europa.eu/state-aid/procedures/transparency-and-evaluation_en)
- **Emisor:** Comisión Europea, Dirección General de Competencia
- **Documentación y notas:** Buscador oficial de expedientes de ayudas de Estado (instrumento SA) con decisiones y documentos. La página de procedimientos recuerda que los regímenes de exención por categorías (RGEC) con presupuesto anual superior a 150 millones de euros deben evaluarse por expertos independientes y publicar los resultados.
- **Temática:** TFB-16 Contratación pública, ayudas y política industrial (principal) · secundarias: TFB-03
- **Calidad Q:** 84 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 8/10
- **Tipología:** primaria (decisiones oficiales)
- **Acceso:** Abierto
- **Ámbitos:** Ayudas de Estado notificadas y decididas en la UE (regímenes y ayudas individuales: IPCEI, chips, hidrógeno, baterías, energía)
- **Motivo de inclusión y uso:** Confirma qué empresas y proyectos reciben ayudas aprobadas y en qué condiciones. Bloque B: AG-B07 (regulación y riesgo de recuperación de ayudas), AG-B05 (capacidad subvencionada que entrará en el mercado), AG-B12 (beneficiarios cotizados).
- **Restricciones de uso:** Reutilización de documentos de la Comisión con cita.
- **Sesgos y cautelas:** Las decisiones se publican con retraso y versiones no confidenciales; importe aprobado no es importe desembolsado.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «State aid Transparency Award Module public search European Commission competition state aid register cases»; WebFetch: sí, página de procedimientos de DG COMP)
- **Origen:** Alta 2026-11-02 (F9 Bloque B, TFB-16).

#### MBF-0408 · Q 84 (A) — Transparency Award Module (TAM) — búsqueda pública de concesiones individuales de ayudas de Estado

- **Canal oficial (URL raíz):** https://webgate.ec.europa.eu/competition/transparency/public/search/home/
- **Emisor:** Comisión Europea (DG COMP); los Estados miembros cargan los datos
- **Documentación y notas:** Sistema para registrar y publicar concesiones individuales de ayudas de Estado: número SA, beneficiario e identificador nacional, tipo, región, sector NACE, instrumento, objetivo, fecha, importe nominal y concedido y autoridad concedente. Umbrales de publicación según la base jurídica: 500.000 € en general (RGEC), 100.000 € en los marcos COVID-19 y de crisis temporal y en varias normas revisadas, 10.000 € para producción agraria primaria y pesca en las normas de 2023 (guía de usuario V16, marzo de 2025).
- **Temática:** TFB-16 Contratación pública, ayudas y política industrial (principal) · secundarias: TFB-03
- **Calidad Q:** 84 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 8/10
- **Tipología:** primaria (registro oficial de concesiones)
- **Acceso:** Abierto (búsqueda pública)
- **Ámbitos:** Ayudas individuales sobre umbral concedidas por los Estados miembros
- **Motivo de inclusión y uso:** Identifica qué empresas concretas reciben ayudas y cuánto. Bloque B: AG-B12 (beneficiarios cotizados de un régimen), AG-B07 y AG-B09 (peso de las ayudas en la inversión y márgenes de candidatos).
- **Restricciones de uso:** Reutilización con cita; comprobar el umbral aplicable a cada base jurídica.
- **Sesgos y cautelas:** Umbrales distintos por base jurídica; carga nacional heterogénea; no todos los Estados usan el TAM (algunos tienen registros propios).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «State aid Transparency Award Module public search European Commission competition state aid register cases»; WebFetch: sí, guía de usuario TAM V16 (marzo de 2025) en stateaid.minfin.bg)
- **Origen:** Alta 2026-11-02 (F9 Bloque B, TFB-16).

#### MBF-0411 · Q 84 (A) — Sistema Nacional de Publicidad de Subvenciones y Ayudas Públicas (SNPSAP) / Base de Datos Nacional de Subvenciones (BDNS) — Infosubvenciones

- **Canal oficial (URL raíz):** https://www.infosubvenciones.gob.es (portal); nota oficial: https://www.pap.hacienda.gob.es/bdnstrans/estaticos/noticia/pdf/SNPSNotaInformativaJulio2023.pdf
- **Emisor:** Ministerio de Hacienda (Intervención General de la Administración del Estado como gestora de la BDNS)
- **Documentación y notas:** Publica convocatorias y concesiones de subvenciones y ayudas públicas de todas las administraciones españolas, ayudas de Estado (desde el 1/7/2016), registro centralizado de ayudas de minimis y planes estratégicos de subvenciones; servicio de alertas por criterios.
- **Temática:** TFB-16 Contratación pública, ayudas y política industrial (principal) · secundarias: TFB-03
- **Calidad Q:** 84 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria (registro oficial)
- **Acceso:** Abierto (consulta pública)
- **Ámbitos:** Subvenciones y ayudas públicas en España, incluidas las del Plan de Recuperación
- **Motivo de inclusión y uso:** Identifica beneficiarios y cuantías de ayudas en España por sector. Bloque B: AG-B07 (política industrial española, PERTE), AG-B12 (subvenciones recibidas por candidatos), AG-B04.
- **Restricciones de uso:** Uso con cita; datos personales de personas físicas sujetos a protección de datos.
- **Sesgos y cautelas:** La nota no menciona API ni descargas masivas; plazos de publicación y calidad según el órgano concedente.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Gestión de la BDNS por la IGAE según normativa; la nota leída no lo menciona expresamente.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Base de Datos Nacional de Subvenciones Infosubvenciones PERTE Plan de Recuperación datos»; WebFetch: sí, nota informativa de julio de 2023 (PDF))
- **Origen:** Alta 2026-11-02 (F9 Bloque B, TFB-16).

#### MBF-0605 · Q 84 (A) — BIS (Departamento de Comercio de EE. UU.) — Entity List (control de exportaciones)

- **Canal oficial (URL raíz):** https://www.bis.gov/media/documents/entity-list-faqs-11.10.2025.pdf (página de la lista citada en el documento: http://www.bis.doc.gov/index.php/policy-guidance/lists-of-parties-of-concern/entity-list)
- **Emisor:** Bureau of Industry and Security (BIS), U.S. Department of Commerce
- **Documentación y notas:** Lista de partes extranjeras sujetas a requisitos de licencia adicionales de las Export Administration Regulations (EAR): cada entrada indica nombre, dirección, país, anuncio del Federal Register que la incorporó, fecha de efecto, requisito de licencia (p. ej., «para todos los artículos sujetos a las EAR», §744.11) y política de licencias (normalmente «presunción de denegación»; algunas «caso por caso»). Integrada también en la Consolidated Screening List (MBF-0606).
- **Temática:** TFB-16 Contratación pública, ayudas y política industrial (principal) · secundarias: TFB-09, TFB-05
- **Calidad Q:** 84 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 15/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** primaria (acto administrativo publicado en el Federal Register)
- **Acceso:** Abierto, sin registro
- **Ámbitos:** Controles de exportación de EE. UU. sobre empresas, universidades y centros de investigación extranjeros (semiconductores, IA, defensa, telecomunicaciones)
- **Motivo de inclusión y uso:** Fuente primaria de las restricciones tecnológicas que reconfiguran cadenas de valor (semiconductores, equipos, IA) y el acceso a mercados de empresas chinas y de otros países.
- **Restricciones de uso:** Uso libre; la versión jurídicamente vinculante es la del Federal Register/eCFR (suplemento n.º 4 de la parte 744 de las EAR).
- **Sesgos y cautelas:** El extracto descargado leído estaba incompleto; comprobar cada entrada en el Federal Register (MBF-0610). La lista cambia con frecuencia y por motivos de política exterior y de seguridad nacional.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Ampliaciones frecuentes ligadas a controles de semiconductores e IA; cambios de dominio de bis.doc.gov a bis.gov.
- **Uso en el bloque:** AG-B07 Regulación y Geopolítica: controles de exportación que afectan a semiconductores, telecomunicaciones y defensa; AG-B05 Oferta y Cadena de Suministro: clientes y proveedores incluidos en la lista; AG-B06 Tecnología: acceso a tecnología crítica; AG-B12: riesgo de ingresos por clientes restringidos.
- **Origen:** Alta F9_comp (2026-11-03).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-03 (búsqueda web: «BIS Entity List Supplement No. 4 part 744 Consolidated Screening List trade.gov API»; WebFetch: sí, documento de bis.gov)

#### MBF-0418 · Q 83 (A) — Financial Transparency System (FTS) — beneficiarios del presupuesto de la UE

- **Canal oficial (URL raíz):** https://ec.europa.eu/budget/financial-transparency-system/about.html
- **Emisor:** Comisión Europea (DG BUDG)
- **Documentación y notas:** Beneficiarios de fondos de gestión directa e indirecta de la Comisión y del Fondo Europeo de Desarrollo: subvenciones, premios, contratos, instrumentos financieros y apoyo presupuestario, con importe, finalidad, ubicación, servicio, línea presupuestaria y año; datos del año N publicados antes del 30 de junio de N+1.
- **Temática:** TFB-16 Contratación pública, ayudas y política industrial (principal) · secundarias: TFB-03
- **Calidad Q:** 83 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 7/10 · Acceso 8/10
- **Tipología:** primaria (registro oficial)
- **Acceso:** Abierto (formato legible por máquina según art. 38 del Reglamento Financiero)
- **Ámbitos:** Gasto de gestión directa de la UE (Horizonte Europa, CEF, Fondo de Innovación, defensa, etc.)
- **Motivo de inclusión y uso:** Identifica empresas que reciben financiación directa de la UE. Bloque B: AG-B12 (beneficiarios cotizados), AG-B06 (I+D financiada), AG-B07.
- **Restricciones de uso:** Reutilización con cita.
- **Sesgos y cautelas:** Excluye la gestión compartida (hasta el 75 % del presupuesto; ver MBF-0409); contratos menores de 15.000 € no publicados; desfase anual.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «EU Financial Transparency System beneficiaries of EU budget; CORDIS Horizon Europe projects open data; EIB financed projects list»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9 Bloque B, TFB-16).

#### MBF-0601 · Q 83 (A) — Comisión Europea (DG FISMA) — Lista consolidada de personas, grupos y entidades sujetos a sanciones financieras de la UE

- **Canal oficial (URL raíz):** https://data.europa.eu/data/datasets/consolidated-list-of-persons-groups-and-entities-subject-to-eu-financial-sanctions?locale=en (recursos del EU Sanctions Helpdesk: https://eu-sanctions-compliance-helpdesk.europa.eu/resources_bg · panorama de sanciones: https://finance.ec.europa.eu/eu-and-world/sanctions-restrictive-measures/overview-sanctions-and-related-resources_en)
- **Emisor:** Comisión Europea, Dirección General de Estabilidad Financiera, Servicios Financieros y Unión de los Mercados de Capitales (DG FISMA)
- **Documentación y notas:** Lista consolidada de las personas y entidades sujetas a congelación de activos de la UE (más de 5.000 según el Helpdesk), publicada como conjunto de datos abierto en data.europa.eu; los archivos «Financial Sanctions Files» (FSF) se actualizan a diario y su descarga masiva en webgate.ec.europa.eu exige credenciales gratuitas. El Helpdesk enlaza además el EU Sanctions Tracker (data.europa.eu/apps/eusanctionstracker), la lista de restricciones de viaje, TARIC y las listas de bienes de alta prioridad y económicamente críticos.
- **Temática:** TFB-16 Contratación pública, ayudas y política industrial (principal) · secundarias: TFB-03
- **Calidad Q:** 83 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 15/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 8/10
- **Tipología:** primaria (acto jurídico: reglamentos del Consejo consolidados por la Comisión)
- **Acceso:** Abierto (conjunto de datos en data.europa.eu); descarga masiva FSF con registro gratuito
- **Ámbitos:** Sanciones financieras de la UE por régimen: personas, entidades, alias, identificadores y base jurídica
- **Motivo de inclusión y uso:** Fuente primaria de las designaciones de la UE; necesaria para medir la exposición sancionadora de sectores, cadenas de suministro y emisores europeos o con negocio en la UE.
- **Restricciones de uso:** Uso libre con atribución (datos abiertos de la UE); para cumplimiento normativo prevalece el Diario Oficial (EUR-Lex).
- **Sesgos y cautelas:** La base jurídica vinculante es el reglamento publicado en el DOUE; la lista consolidada es una ayuda y puede ir con retraso de horas. Conviene casarla con la lista ONU (MBF-0603), la británica (MBF-0604) y la estadounidense (FXF-0264).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Gestión de la lista por DG FISMA; el Helpdesk de sanciones es el punto de entrada desde 2023.
- **Uso en el bloque:** AG-B07 Regulación y Geopolítica: exposición de sectores y empresas a sanciones de la UE por régimen (Rusia, Bielorrusia, Irán…); AG-B12 Seleccionador de Activos: filtro de exclusión de emisores o filiales designados; AG-B05: proveedores y clientes sancionados en la cadena de suministro.
- **Origen:** Alta F9_comp (2026-11-03).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-03 (búsqueda web: «sanctionsmap.eu EU Sanctions Map European Commission DG FISMA financial sanctions database»; WebFetch: sí, página de recursos del EU Sanctions Helpdesk y ficha del conjunto FSF en opensanctions.org)

#### MBF-0412 · Q 81 (A) — ELISA «El Plan en cifras» — seguimiento de la ejecución del Plan de Recuperación, Transformación y Resiliencia (España)

- **Canal oficial (URL raíz):** https://planderecuperacion.gob.es/ejecucion/elisa-el-plan-en-cifras
- **Emisor:** Ministerio de Economía, Comercio y Empresa, con Hacienda y la Secretaría de Estado de Asuntos Económicos y G20
- **Documentación y notas:** Herramienta de seguimiento con actualización mensual: resolución de convocatorias por nivel de administración, importes adjudicados (más de 35.190 millones de euros a más de 600.000 beneficiarios a 31/03/2024), reparto por comunidad autónoma, listados de empresas y autónomos adjudicatarios y microdatos de proyectos aprobados.
- **Temática:** TFB-16 Contratación pública, ayudas y política industrial (principal) · secundarias: TFB-01
- **Calidad Q:** 81 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 14/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria (datos oficiales de ejecución)
- **Acceso:** Abierto
- **Ámbitos:** Fondos NextGenerationEU en España por región, tema y beneficiario
- **Motivo de inclusión y uso:** Seguimiento de la ejecución real de los fondos NextGen y PERTE en España. Bloque B: AG-B07 (ritmo y destino de fondos), AG-B12 (empresas adjudicatarias), AG-B13.
- **Restricciones de uso:** Uso con cita de la fecha de actualización.
- **Sesgos y cautelas:** Fuente gubernamental (posible sesgo de presentación); contrastar con IGAE, AIReF o MBF-0410.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Base de Datos Nacional de Subvenciones Infosubvenciones PERTE Plan de Recuperación datos»; WebFetch: sí, nota de prensa de La Moncloa (24/04/2024))
- **Origen:** Alta 2026-11-02 (F9 Bloque B, TFB-16).

#### MBF-0606 · Q 81 (A) — International Trade Administration (EE. UU.) — Consolidated Screening List (CSL) con API

- **Canal oficial (URL raíz):** https://www.trade.gov/consolidated-screening-list (ficha de la API en el catálogo de datos: https://catalog.data.gov/dataset/consolidated-screening-list-api-0226f)
- **Emisor:** International Trade Administration (ITA), U.S. Department of Commerce
- **Documentación y notas:** Agrega en una búsqueda las listas de partes restringidas de Comercio (BIS: Denied Persons, Unverified, Entity y Military End-User), Estado (sanciones de no proliferación ACN, AECA Debarred) y Tesoro (OFAC: SDN, FSE, SSI, CAP, MBS, CMIC, PLC). Búsqueda difusa con puntuación de coincidencia, descargas CSV, TSV y JSON y API abierta; actualización automática diaria a las 5:00 (hora del Este).
- **Temática:** TFB-16 Contratación pública, ayudas y política industrial (principal) · secundarias: TFB-03, TFB-05
- **Calidad Q:** 81 (A) — Primariedad 15/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 14/15 · Independencia 9/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** secundaria oficial (agregación de listas primarias)
- **Acceso:** Abierto; la API usa clave gratuita
- **Ámbitos:** Listas de partes restringidas de EE. UU. (exportación, sanciones y no proliferación)
- **Motivo de inclusión y uso:** Punto único y automatizable para cribar candidatos y sus contrapartes contra todas las listas estadounidenses.
- **Restricciones de uso:** Uso libre; la propia herramienta advierte de que es una ayuda y que hay que verificar en el Federal Register y en las listas oficiales antes de actuar.
- **Sesgos y cautelas:** Depende de que cada agencia entregue sus archivos; las coincidencias difusas exigen diligencia adicional. Desde el 01/10/2026 algunas designaciones ACN figuran solo en la SDN.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Cambio en la cobertura de la lista ACN (octubre de 2026).
- **Uso en el bloque:** AG-B12 Seleccionador de Activos: cribado automático de candidatos, filiales y principales clientes frente a listas de EE. UU.; Motor AG-B16: consulta por API en los flujos de criba; AG-B07: contexto de sanciones y controles.
- **Origen:** Alta F9_comp (2026-11-03).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-03 (búsqueda web: «BIS Entity List Supplement No. 4 part 744 Consolidated Screening List trade.gov API»; WebFetch: sí)

#### MBF-0407 · Q 80 (A) — Comisión Europea (DG COMP) — State aid Scoreboard (cuadro de indicadores de ayudas de Estado)

- **Canal oficial (URL raíz):** https://competition-policy.ec.europa.eu/state-aid/scoreboard_en
- **Emisor:** Comisión Europea, Dirección General de Competencia
- **Documentación y notas:** Cuadro anual de gasto en ayudas de Estado por Estado miembro, objetivo e instrumento; enlazado desde la página oficial de procedimientos de ayudas de Estado.
- **Temática:** TFB-16 Contratación pública, ayudas y política industrial (principal) · secundarias: TFB-01
- **Calidad Q:** 80 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 7/10 · Acceso 8/10
- **Tipología:** primaria (estadística oficial agregada de los informes de los Estados)
- **Acceso:** Abierto
- **Ámbitos:** Gasto agregado en ayudas de Estado en la UE
- **Motivo de inclusión y uso:** Contexto macro de la política industrial por país y objetivo. Bloque B: AG-B07 y AG-B08 (intensidad de apoyo público por país), AG-B13.
- **Restricciones de uso:** Reutilización con cita.
- **Sesgos y cautelas:** Publicación anual con desfase; agregados sin detalle por empresa.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «State aid Transparency Award Module public search European Commission competition state aid register cases»; WebFetch: sí, la página de procedimientos de DG COMP lo enlaza; el Scoreboard no se leyó (fuera de la lista permitida))
- **Origen:** Alta 2026-11-02 (F9 Bloque B, TFB-16).

#### MBF-0409 · Q 80 (A) — Kohesio — proyectos y beneficiarios de la política de cohesión de la UE

- **Canal oficial (URL raíz):** https://kohesio.ec.europa.eu/en/
- **Emisor:** Comisión Europea
- **Documentación y notas:** Plataforma de datos abiertos sobre proyectos financiados por la política de cohesión: enlaza proyectos, beneficiarios, programas y regiones mediante un grafo de conocimiento europeo; descargas en CSV, XLSX y RDF.
- **Temática:** TFB-16 Contratación pública, ayudas y política industrial (principal) · secundarias: TFB-01
- **Calidad Q:** 80 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 14/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 8/10
- **Tipología:** primaria (datos de los programas operativos)
- **Acceso:** Abierto
- **Ámbitos:** Proyectos FEDER, FSE+, Fondo de Cohesión por región y beneficiario
- **Motivo de inclusión y uso:** Localiza la inversión pública cofinanciada por región y tema (energía, transporte, digitalización). Bloque B: AG-B04 (demanda regional), AG-B07 y AG-B12 (empresas beneficiarias).
- **Restricciones de uso:** Datos abiertos con cita.
- **Sesgos y cautelas:** Calidad y retraso según autoridades de gestión; importes programados frente a pagados.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Recovery and Resilience Scoreboard data Kohesio EU funded projects open data»; WebFetch: sí, nota de la Región de Murcia (murciaregioneuropea.carm.es) que describe la plataforma; kohesio.ec.europa.eu no se leyó)
- **Origen:** Alta 2026-11-02 (F9 Bloque B, TFB-16).

#### MBF-0413 · Q 80 (A) — IEA — Policies and Measures Database (base de datos de políticas energéticas y climáticas)

- **Canal oficial (URL raíz):** https://www.iea.org/policies/about
- **Emisor:** Agencia Internacional de la Energía (IEA)
- **Documentación y notas:** Políticas pasadas, vigentes y planificadas que reducen emisiones, mejoran la eficiencia y apoyan las renovables y otras tecnologías limpias: regulación, programas de gasto, política comercial, metano, minerales críticos y CCUS. Información recogida desde 1999 de gobiernos, socios y análisis de la IEA; los gobiernos revisan sus fichas al menos una vez al año; base conjunta con IRENA para renovables.
- **Temática:** TFB-16 Contratación pública, ayudas y política industrial (principal) · secundarias: TFB-12, TFB-17
- **Calidad Q:** 80 (A) — Primariedad 17/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** secundaria (compilación oficial de políticas)
- **Acceso:** Abierto (consulta web)
- **Ámbitos:** Política energética, climática e industrial por país, sector y tecnología
- **Motivo de inclusión y uso:** Inventario de incentivos y regulaciones que mueven la demanda de una tecnología. Bloque B: AG-B07 (mapa regulatorio por país), AG-B06 y AG-B04 (adopción inducida por política), AG-B13 (escenarios de política).
- **Restricciones de uso:** La página no declara licencia; citar la ficha y la fecha.
- **Sesgos y cautelas:** No es exhaustiva para ningún país; fichas con distinta actualización.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «IEA Policies database renewable energy climate policies search; Global Trade Alert industrial policy subsidies database»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9 Bloque B, TFB-16).

#### MBF-0602 · Q 80 (A) — Unión Europea — EU Sanctions Map (mapa de medidas restrictivas de la UE)

- **Canal oficial (URL raíz):** https://sanctionsmap.eu/ (presentación en data.europa.eu: https://data.europa.eu/en/news/find-out-about-eu-restrictive-measures-across-globe-through-eu-sanctions-map)
- **Emisor:** Unión Europea (Comisión Europea; herramienta enlazada por el EU Sanctions Helpdesk de DG FISMA)
- **Documentación y notas:** Mapa interactivo de todos los regímenes de medidas restrictivas de la UE frente a terceros países: congelación de activos, embargos de armas, restricciones de admisión y sectoriales, con sus actos jurídicos y guías; enlaza la herramienta de denuncia anónima de sanciones. Ruta de entrada visual; los datos nominales se citan en la lista consolidada (MBF-0601).
- **Temática:** TFB-16 Contratación pública, ayudas y política industrial (principal) · secundarias: TFB-03
- **Calidad Q:** 80 (A) — Primariedad 17/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 14/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria (presentación oficial de regímenes y actos jurídicos)
- **Acceso:** Abierto, sin registro
- **Ámbitos:** Regímenes de sanciones de la UE por país y tipo de medida; actos jurídicos y guías
- **Motivo de inclusión y uso:** Vista rápida de qué países y sectores están bajo medidas restrictivas de la UE y con qué base jurídica.
- **Restricciones de uso:** Uso libre; citar el acto jurídico de EUR-Lex como prueba.
- **Sesgos y cautelas:** Herramienta de navegación: no sustituye al texto del DOUE; el operador concreto no figura en la página leída.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-20) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Uso en el bloque:** AG-B07 Regulación y Geopolítica: mapa de regímenes y medidas sectoriales (energía, tecnología, finanzas) que afectan a mercados geográficos; AG-B13 Prospectiva: seguimiento de nuevos paquetes de sanciones.
- **Origen:** Alta F9_comp (2026-11-03).
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-03 (búsqueda web: «sanctionsmap.eu EU Sanctions Map European Commission DG FISMA financial sanctions database»; WebFetch: sí, nota de data.europa.eu y recursos del EU Sanctions Helpdesk, no el mapa)

#### MBF-0405 · Q 79 (B) — Grants.gov — convocatorias de subvenciones federales de EE. UU.

- **Canal oficial (URL raíz):** https://www.grants.gov
- **Emisor:** U.S. Department of Health and Human Services (gestor del portal federal de subvenciones)
- **Documentación y notas:** Lista las convocatorias de subvenciones discrecionales de las agencias federales con plazos, importes, solicitantes elegibles, códigos CFDA y paquetes de solicitud. No incluye contratos ni datos de gasto ejecutado.
- **Temática:** TFB-16 Contratación pública, ayudas y política industrial (principal) · secundarias: TFB-03
- **Calidad Q:** 79 (B) — Primariedad 18/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 14/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 8/10
- **Tipología:** primaria (convocatorias oficiales)
- **Acceso:** Abierto
- **Ámbitos:** Subvenciones federales de EE. UU. (energía, sanidad, investigación, infraestructuras)
- **Motivo de inclusión y uso:** Detecta programas de apoyo público que crean demanda o financian a un sector. Bloque B: AG-B07 (política industrial), AG-B13 (prospectiva de programas), AG-B04.
- **Restricciones de uso:** Uso libre.
- **Sesgos y cautelas:** Convocatoria no equivale a desembolso; contrastar ejecución en USAspending.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «USAspending.gov API federal contracts grants data SAM.gov contract opportunities»; WebFetch: sí, página índice govprocure.northwest.net/databases.html)
- **Origen:** Alta 2026-11-02 (F9 Bloque B, TFB-16).

#### MBF-0414 · Q 77 (B) — Global Trade Alert — base de intervenciones estatales (subvenciones, comercio y política industrial)

- **Canal oficial (URL raíz):** https://globaltradealert.org/
- **Emisor:** Global Trade Alert, iniciativa de SGEPT (con apoyo de la Universidad de San Galo y la Fundación Schmidheiny)
- **Documentación y notas:** Base de intervenciones públicas que afectan al comercio, con hilos temáticos; p. ej., «Green Goods Subsidies» sigue subvenciones internas (préstamos, subvenciones, ayudas a la producción, desgravaciones) para vehículos eléctricos, células fotovoltaicas, aerogeneradores, hidrógeno y equipos ambientales, con método basado en Sauvage (OCDE, 2014). Descarga Excel/CSV; contenido bajo CC BY-NC 4.0 salvo indicación.
- **Temática:** TFB-16 Contratación pública, ayudas y política industrial (principal) · secundarias: TFB-05
- **Calidad Q:** 77 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 13/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** secundaria (compilación documentada de medidas oficiales)
- **Acceso:** Abierto; registro gratuito para alertas
- **Ámbitos:** Subvenciones, aranceles, controles de exportación y medidas de política industrial en el mundo
- **Motivo de inclusión y uso:** Cuantifica la carrera de subvenciones y el proteccionismo que afecta a un sector. Bloque B: AG-B07 (riesgo geopolítico y comercial), AG-B05 (relocalización de cadenas), AG-B14 (tesis contrarias por sobrecapacidad subvencionada).
- **Restricciones de uso:** CC BY-NC 4.0 (uso no comercial con atribución).
- **Sesgos y cautelas:** Cobertura dependiente de fuentes públicas; clasificación propia de intervenciones.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «IEA Policies database renewable energy climate policies search; Global Trade Alert industrial policy subsidies database»; WebFetch: sí, hilo «Green Goods Subsidies»)
- **Origen:** Alta 2026-11-02 (F9 Bloque B, TFB-16).

#### MBF-0415 · Q 75 (B) — Clean Investment Monitor — inversión en fabricación y despliegue de tecnologías limpias (Rhodium Group y MIT CEEPR)

- **Canal oficial (URL raíz):** https://www.cleaninvestmentmonitor.org/about
- **Emisor:** Rhodium Group y MIT Center for Energy and Environmental Policy Research (CEEPR), con contribuciones de Bruegel
- **Documentación y notas:** Sigue la inversión pública y privada en fabricación y despliegue de tecnologías de descarbonización y sus componentes, con base desde 2018 (electricidad limpia, transporte, electrificación de edificios, industria de bajas emisiones, gestión de carbono); actualización trimestral; datos por país, estado, distrito y planta en la plataforma ClimateDeck de Rhodium, descargables gratis.
- **Temática:** TFB-16 Contratación pública, ayudas y política industrial (principal) · secundarias: TFB-17, TFB-12
- **Calidad Q:** 75 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 13/15 · Independencia 8/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** secundaria (base de proyectos con método propio)
- **Acceso:** Abierto (descarga gratuita en ClimateDeck)
- **Ámbitos:** Inversión en tecnología limpia vinculada a la IRA y a la política industrial
- **Motivo de inclusión y uso:** Mide la capacidad industrial que se está construyendo (baterías, solar, hidrógeno) y su ritmo. Bloque B: AG-B05 (oferta futura y sobrecapacidad), AG-B07 (efecto IRA), AG-B12 (empresas con proyectos), MC-B04.
- **Restricciones de uso:** Uso con atribución; condiciones de ClimateDeck.
- **Sesgos y cautelas:** Anuncios de proyectos pueden cancelarse; método propio de clasificación.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Clean Investment Monitor Rhodium MIT manufacturing investments tracker CHIPS Act semiconductor investments tracker SIA»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9 Bloque B, TFB-16).

#### MBF-0419 · Q 75 (B) — Single Market Scoreboard — indicadores de contratación pública por país (Comisión Europea)

- **Canal oficial (URL raíz):** https://single-market-scoreboard.ec.europa.eu
- **Emisor:** Comisión Europea (DG GROW)
- **Documentación y notas:** Cuadro de indicadores del mercado único, enlazado desde la página oficial de TED como herramienta de análisis de datos de contratación pública.
- **Temática:** TFB-16 Contratación pública, ayudas y política industrial (principal) · secundarias: TFB-01
- **Calidad Q:** 75 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 14/15 · Independencia 10/10 · Actualidad 7/10 · Acceso 8/10
- **Tipología:** secundaria (indicadores oficiales derivados de TED)
- **Acceso:** Abierto
- **Ámbitos:** Rendimiento de la contratación pública por Estado miembro
- **Motivo de inclusión y uso:** Contexto comparado de los mercados públicos nacionales. Bloque B: AG-B07 y AG-B03 (apertura y competencia en mercados públicos).
- **Restricciones de uso:** Reutilización con cita.
- **Sesgos y cautelas:** Indicadores agregados; contenido no leído en esta verificación.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «TED Tenders Electronic Daily open data API public procurement notices EU»; WebFetch: sí, página de la Comisión sobre TED (lo enlaza); el Scoreboard no se leyó)
- **Origen:** Alta 2026-11-02 (F9 Bloque B, TFB-16).

#### MBF-0420 · Q 72 (B) — Public Procurement Data Space (PPDS) — espacio europeo de datos de contratación pública

- **Canal oficial (URL raíz):** https://public-procurement-data-space.europa.eu/en
- **Emisor:** Comisión Europea
- **Documentación y notas:** Espacio de datos de contratación pública de la UE, enlazado desde la página oficial de TED junto a los conjuntos de datos abiertos de TED.
- **Temática:** TFB-16 Contratación pública, ayudas y política industrial (principal) · secundarias: TFB-01
- **Calidad Q:** 72 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 14/15 · Independencia 10/10 · Actualidad 7/10 · Acceso 6/10
- **Tipología:** secundaria (integración de datos oficiales)
- **Acceso:** Abierto (condiciones no leídas)
- **Ámbitos:** Datos de contratación pública de la UE (por encima y, según el país, por debajo de umbrales)
- **Motivo de inclusión y uso:** Vía complementaria a TED para análisis de mercados públicos. Bloque B: AG-B04, AG-B12.
- **Restricciones de uso:** Comprobar condiciones al primer uso.
- **Sesgos y cautelas:** Contenido y cobertura no leídos en esta verificación; usar como complemento de MBF-0401.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «TED Tenders Electronic Daily open data API public procurement notices EU»; WebFetch: sí, página de la Comisión sobre TED (lo enlaza); el PPDS no se leyó)
- **Origen:** Alta 2026-11-02 (F9 Bloque B, TFB-16).

#### MBF-0416 · Q 66 (B) — GMF Technology — Semiconductor Investment Tracker (inversiones en chips en EE. UU. y Europa)

- **Canal oficial (URL raíz):** https://www.gmfus.org/gmf-technology-semiconductor-investment-tracker
- **Emisor:** German Marshall Fund of the United States (GMF Technology)
- **Documentación y notas:** Mapa interactivo y conjunto de datos (Excel) de inversiones en semiconductores en EE. UU. y Europa con ubicación, importe, tipo de fábrica o chip y empleo estimado, ligado a la CHIPS and Science Act (52.700 millones de dólares) y a la Ley Europea de Chips; fuentes abiertas, prensa y notas de empresa; actualización continua.
- **Temática:** TFB-16 Contratación pública, ayudas y política industrial (principal) · secundarias: TFB-09
- **Calidad Q:** 66 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 11/15 · Independencia 8/10 · Actualidad 7/10 · Acceso 8/10
- **Tipología:** secundaria (compilación de anuncios)
- **Acceso:** Abierto (mapa y Excel)
- **Ámbitos:** Fábricas de semiconductores anunciadas y subvencionadas
- **Motivo de inclusión y uso:** Inventario de capacidad de fabricación de chips anunciada. Bloque B: AG-B05 (oferta futura), AG-B07 (CHIPS Act y Ley Europea de Chips), AG-B12 (candidatos con fábricas subvencionadas).
- **Restricciones de uso:** Uso con cita.
- **Sesgos y cautelas:** Basado en anuncios y prensa; cifras sujetas a revisión; frecuencia de actualización real no verificada.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Clean Investment Monitor Rhodium MIT manufacturing investments tracker CHIPS Act semiconductor investments tracker SIA»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9 Bloque B, TFB-16).

#### MBF-0417 · Q 66 (B) — Semiconductor Industry Association (SIA) — seguimiento de los programas de I+D de la CHIPS Act

- **Canal oficial (URL raíz):** https://www.semiconductors.org/tracking-the-progress-of-the-chips-rd-programs/
- **Emisor:** Semiconductor Industry Association (SIA)
- **Documentación y notas:** Recurso (25/06/2024) que sigue los programas de I+D de la CHIPS Act (13.000 millones de dólares a cinco años: NSTC, NAPMP, metrología, Manufacturing USA y Microelectronics Commons del DoD) con compromisos de financiación por programa.
- **Temática:** TFB-16 Contratación pública, ayudas y política industrial (principal) · secundarias: TFB-04, TFB-09
- **Calidad Q:** 66 (B) — Primariedad 13/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 12/15 · Independencia 6/10 · Actualidad 7/10 · Acceso 8/10
- **Tipología:** secundaria (patronal; seguimiento de programas oficiales)
- **Acceso:** Abierto
- **Ámbitos:** Política industrial de semiconductores en EE. UU.
- **Motivo de inclusión y uso:** Estado de los programas públicos de I+D de chips. Bloque B: AG-B06 (tecnología), AG-B07 (política industrial EE. UU.), AG-B13.
- **Restricciones de uso:** Uso con cita.
- **Sesgos y cautelas:** Patronal del sector (interés en la continuidad de las ayudas); cifras a la fecha del artículo.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Clean Investment Monitor Rhodium MIT manufacturing investments tracker CHIPS Act semiconductor investments tracker SIA»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9 Bloque B, TFB-16).

## TFB-17 Sostenibilidad y clima: datos

#### MBF-0452 · Q 88 (A) — Global Carbon Project — Global Carbon Budget 2025 (presupuesto mundial de carbono)

- **Canal oficial (URL raíz):** https://essd.copernicus.org/articles/18/3211/2026/
- **Emisor:** Global Carbon Project (Friedlingstein, O'Sullivan, Jones, Andrew, Bakker et al.)
- **Documentación y notas:** «Global Carbon Budget 2025», Earth System Science Data 18(5): 3211–3288, publicado el 13/05/2026; DOI 10.5194/essd-18-3211-2026; datos en https://doi.org/10.18160/GCP-2025: emisiones fósiles, por cambio de uso del suelo, crecimiento atmosférico y sumideros oceánico y terrestre, 1959–2024 con proyección 2025. Hay corrigendum publicado.
- **Temática:** TFB-17 Sostenibilidad y clima: datos (principal) · secundarias: TFB-18
- **Calidad Q:** 88 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria (síntesis científica revisada por pares)
- **Acceso:** Abierto
- **Ámbitos:** Emisiones mundiales de CO2 y sumideros
- **Motivo de inclusión y uso:** Contexto de la trayectoria global de emisiones y presupuesto de carbono restante. Bloque B: AG-B13 y AG-B11 (escenarios de transición), AG-B08.
- **Restricciones de uso:** Acceso abierto con cita del artículo y del DOI de datos.
- **Sesgos y cautelas:** Revisiones anuales; leer el corrigendum.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Global Carbon Budget fossil CO2 data; EU taxonomy compass; Copernicus Climate Change Service climate indicators»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9 Bloque B, TFB-17).

#### MBF-0441 · Q 87 (A) — JRC — EDGAR (Emissions Database for Global Atmospheric Research): emisiones de GEI de todos los países

- **Canal oficial (URL raíz):** https://edgar.jrc.ec.europa.eu/report_2025
- **Emisor:** Comisión Europea, Centro Común de Investigación (JRC)
- **Documentación y notas:** Informe y base «GHG emissions of all world countries» 2025 (Crippa, Guizzardi, Pagani, Banja, Muntean et al.; Oficina de Publicaciones de la UE, 2025; doi:10.2760/9816914; JRC143227): CO2 fósil, CH4, N2O y gases fluorados por país y sector hasta 2024 (cuotas de 2024: 74,5 %, 17,9 %, 4,8 % y 2,8 %); descargas XLSX por sector y país. Existe ya una edición 2026 (JRC147815) y nota del JRC de 07/09/2026.
- **Temática:** TFB-17 Sostenibilidad y clima: datos (principal) · secundarias: TFB-01
- **Calidad Q:** 87 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria (inventario científico oficial con metodología publicada)
- **Acceso:** Abierto (CC BY 4.0; los datos IEA-EDGAR CO2 bajo CC BY-NC-ND 4.0)
- **Ámbitos:** Emisiones de GEI por país, gas y sector desde la serie histórica hasta 2024
- **Motivo de inclusión y uso:** Mide la intensidad y tendencia de emisiones de sectores y países. Bloque B: AG-B11 (riesgo de transición por sector y país), AG-B07 (exposición a regulación climática), MC-B09 (escenarios de coste del carbono).
- **Restricciones de uso:** CC BY 4.0 con atribución; condiciones distintas para IEA-EDGAR CO2.
- **Sesgos y cautelas:** Estimaciones de inventario con incertidumbre por gas (mayor en CH4 y N2O); revisiones entre ediciones.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «EDGAR Emissions Database for Global Atmospheric Research JRC GHG emissions of all world countries 2025 report»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9 Bloque B, TFB-17).

#### MBF-0444 · Q 86 (A) — AEMA (EEA) — EU ETS data viewer (emisiones verificadas y derechos del régimen de comercio de emisiones)

- **Canal oficial (URL raíz):** https://www.eea.europa.eu/en/analysis/maps-and-charts/emissions-trading-viewer-1-dashboards
- **Emisor:** Agencia Europea de Medio Ambiente (EEA)
- **Documentación y notas:** Datos del Registro de la Unión (antes EUTL, extracción de 01/07/2026): emisiones verificadas, asignación gratuita, derechos subastados (EUA, EUAA) y unidades entregadas por país, actividad y año (2005–2024); más de 16.000 instalaciones fijas, 1.600 operadores aéreos y 2.600 marítimos; datos de subasta de EEX e ICE; descarga completa en el datahub de la EEA.
- **Temática:** TFB-17 Sostenibilidad y clima: datos (principal) · secundarias: TFB-12
- **Calidad Q:** 86 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** primaria (registro oficial)
- **Acceso:** Abierto
- **Ámbitos:** Emisiones y derechos del EU ETS por sector y país
- **Motivo de inclusión y uso:** Cuantifica la exposición al coste del CO2 de sectores europeos (acero, cemento, electricidad, aviación, transporte marítimo). Bloque B: AG-B11 y AG-B09 (coste del carbono en márgenes), AG-B05, MC-B08.
- **Restricciones de uso:** Reutilización con cita de la EEA.
- **Sesgos y cautelas:** Datos por instalación requieren casar con la empresa matriz; desfase anual.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «EU Taxonomy Compass; EEA EU Emissions Trading System data viewer verified emissions installations»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9 Bloque B, TFB-17).

#### MBF-0446 · Q 84 (A) — Banco Mundial — Carbon Pricing Dashboard (impuestos al carbono y sistemas de comercio de emisiones)

- **Canal oficial (URL raíz):** https://carbonpricingdashboard.worldbank.org/about
- **Emisor:** Banco Mundial (datos de ETS aportados por ICAP)
- **Documentación y notas:** Instrumentos de precio directo del carbono en el mundo (ETS, impuestos y créditos): cobertura de emisiones, precios nominales a 1 de abril, ingresos anuales y emisión, registro y retirada de créditos; actualización completa cada mayo con el informe «State and Trends of Carbon Pricing»; descarga en Excel.
- **Temática:** TFB-17 Sostenibilidad y clima: datos (principal) · secundarias: TFB-01, TFB-12
- **Calidad Q:** 84 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** primaria (compilación oficial con fuentes gubernamentales)
- **Acceso:** Abierto (descarga Excel)
- **Ámbitos:** Precios del carbono, cobertura e ingresos por jurisdicción
- **Motivo de inclusión y uso:** Precio del carbono por país para estimar costes de transición. Bloque B: AG-B07 y AG-B11, AG-B09 y MC-B08 (sensibilidad de márgenes al precio del carbono).
- **Restricciones de uso:** La página no declara licencia; citar edición.
- **Sesgos y cautelas:** No recoge todas las exenciones ni la asignación gratuita; precios a una fecha.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «World Bank Carbon Pricing Dashboard; ICAP Allowance Price Explorer; CDP open data portal emissions disclosure»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9 Bloque B, TFB-17).

#### MBF-0443 · Q 83 (A) — NGFS — Scenarios Portal (escenarios climáticos para bancos centrales y supervisores)

- **Canal oficial (URL raíz):** https://www.ngfs.net/ngfs-scenarios-portal/data-resources/
- **Emisor:** Network for Greening the Financial System (NGFS), con IIASA y Climate Analytics
- **Documentación y notas:** Escenarios de largo plazo Fase V (noviembre de 2024; fases anteriores 2019–2023) y escenarios de corto plazo; datos de transición y macro en el IIASA NGFS Scenario Explorer (xlsx, csv, API REST, pyam), NiGEM, MAGICC y daños físicos en el Climate Impact Explorer. Aviso: el artículo de Kotz et al. (2024) que sustentaba estimaciones de daños físicos de la Fase V fue retractado; nueva versión prevista a finales de 2026.
- **Temática:** TFB-17 Sostenibilidad y clima: datos (principal) · secundarias: TFB-02
- **Calidad Q:** 83 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 8/10 · Acceso 9/10
- **Tipología:** primaria (escenarios oficiales con modelos documentados)
- **Acceso:** Abierto (licencia de IIASA, sección 5)
- **Ámbitos:** Trayectorias de precio del carbono, mix energético, emisiones y PIB por escenario
- **Motivo de inclusión y uso:** Base de escenarios de transición para proyecciones sectoriales. Bloque B: AG-B13 (escenarios de largo plazo), AG-B11 (riesgo de transición y físico), MC-B08 (simulación por escenarios).
- **Restricciones de uso:** Licencia de IIASA; NGFS no asume responsabilidad por el uso.
- **Sesgos y cautelas:** Variables de daño físico afectadas por la retractación de Kotz et al.; escenarios no son previsiones.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «NGFS Scenarios Portal climate scenarios data download; Climate Action Tracker country ratings»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9 Bloque B, TFB-17).

#### MBF-0442 · Q 82 (A) — SBTi — Target Dashboard (objetivos climáticos validados de empresas)

- **Canal oficial (URL raíz):** https://sciencebasedtargets.org/target-dashboard
- **Emisor:** Science Based Targets initiative (SBTi)
- **Documentación y notas:** Base de empresas e instituciones financieras con objetivos validados o compromisos: 14.427 con objetivos o compromiso, 12.256 con objetivos validados, 2.873 con objetivos de cero neto (cifras vistas el 02/11/2026); campos de sector, ámbito, año base y objetivo, alineación de temperatura; descarga Excel por empresa y por objetivo con diccionario de datos; actualización cada jueves.
- **Temática:** TFB-17 Sostenibilidad y clima: datos (principal) · secundarias: TFB-07
- **Calidad Q:** 82 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 13/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria (registro de validaciones propias)
- **Acceso:** Abierto (descarga Excel)
- **Ámbitos:** Objetivos de reducción de emisiones a nivel de empresa
- **Motivo de inclusión y uso:** Filtro de candidatos por compromiso climático validado. Bloque B: AG-B11 (calidad de la transición de candidatos), AG-B12 y MC-B07 (variable de cribado y pureza de exposición).
- **Restricciones de uso:** La página no declara licencia; consultar condiciones del sitio.
- **Sesgos y cautelas:** Un objetivo validado no garantiza su cumplimiento; solo cubre objetivos de reducción de GEI.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «SBTi target dashboard companies; CDP open data portal; Net Zero Tracker; Transition Pathway Initiative company assessments»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9 Bloque B, TFB-17).

#### MBF-0459 · Q 81 (A) — IIASA — NGFS Scenario Explorer (descarga de los datos de transición de los escenarios NGFS)

- **Canal oficial (URL raíz):** URL raíz no leída; enlazado desde https://www.ngfs.net/ngfs-scenarios-portal/data-resources/ (licencia: data.ene.iiasa.ac.at/ngfs/#/license)
- **Emisor:** International Institute for Applied Systems Analysis (IIASA), para la NGFS
- **Documentación y notas:** Repositorio de los datos de transición y macroeconómicos de los escenarios NGFS (Fase V, noviembre de 2024): descarga xlsx o csv, API REST y paquete abierto pyam de Python; licencia en la sección 5 de la página de IIASA.
- **Temática:** TFB-17 Sostenibilidad y clima: datos (principal) · secundarias: TFB-02
- **Calidad Q:** 81 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 14/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 9/10
- **Tipología:** primaria (base de datos oficial de los escenarios)
- **Acceso:** Abierto (licencia IIASA; descarga y API)
- **Ámbitos:** Variables de escenarios: emisiones, energía por fuente, precio del carbono, PIB por región
- **Motivo de inclusión y uso:** Insumo directo del Motor para escenarios sectoriales de transición. Bloque B: MC-B08 (simulación por escenarios), AG-B13 y AG-B11; conector en HT-01.
- **Restricciones de uso:** Licencia de IIASA (no leída en detalle).
- **Sesgos y cautelas:** Ver la advertencia de retractación de Kotz et al. (2024) en las variables de daño físico (MBF-0443); sitio no leído.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «NGFS Scenarios Portal climate scenarios data download; Climate Action Tracker country ratings»; WebFetch: sí, portal de escenarios NGFS (índice))
- **Origen:** Alta 2026-11-02 (F9 Bloque B, TFB-17).

#### MBF-0453 · Q 79 (B) — Transition Pathway Initiative (TPI Centre, LSE) — evaluaciones de preparación para la transición

- **Canal oficial (URL raíz):** https://www.environmental-finance.com/content/analysis/explainer-the-transition-pathway-initiative.html (canal oficial: transitionpathwayinitiative.org)
- **Emisor:** TPI Global Climate Transition Centre (Grantham Research Institute, London School of Economics)
- **Documentación y notas:** Unos 600 valores de 16 sectores intensivos en carbono: calidad de gestión (19 indicadores, niveles 0–4) y rendimiento de carbono frente a trayectorias sectoriales (1,5 °C, por debajo de 2 °C, compromisos nacionales); datos públicos y gratuitos en Excel; respaldado por 131 inversores con más de 50 billones de dólares; también evalúa bancos, emisores de bonos y soberanos; usado por Climate Action 100+.
- **Temática:** TFB-17 Sostenibilidad y clima: datos (principal) · secundarias: TFB-11
- **Calidad Q:** 79 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 14/15 · Independencia 9/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** secundaria (evaluación independiente con método publicado)
- **Acceso:** Abierto (Excel gratuito)
- **Ámbitos:** Alineación climática de empresas cotizadas de sectores intensivos
- **Motivo de inclusión y uso:** Clasifica a los candidatos de sectores intensivos por calidad de transición. Bloque B: AG-B11, AG-B12 y MC-B07 (variable de cribado).
- **Restricciones de uso:** Uso libre con cita.
- **Sesgos y cautelas:** Cobertura limitada a grandes emisores; actualización por ciclos sectoriales.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Transition Pathway Initiative TPI Centre company assessments data; Climate Bonds Initiative green bond database; EM-DAT disaster database; ND-GAIN index»; WebFetch: sí, artículo explicativo de Environmental Finance (21/02/2023) y ficha de Altiorem)
- **Origen:** Alta 2026-11-02 (F9 Bloque B, TFB-17).

#### MBF-0455 · Q 78 (B) — Climate Policy Initiative — Net Zero Finance Tracker (NZFT)

- **Canal oficial (URL raíz):** https://www.climatepolicyinitiative.org/wp-content/uploads/2026/09/Net-Zero-Finance-Tracker-Methodology-2026.pdf
- **Emisor:** Climate Policy Initiative (CPI)
- **Documentación y notas:** Plataforma interactiva y gratuita sobre el alineamiento de instituciones financieras con el cero neto: 18 indicadores y 170 acciones estándar en tres dimensiones (objetivos, implantación, impacto); edición 2026 con 1.500 instituciones privadas (bancos, aseguradoras, gestoras y propietarios de activos) con unos 315 billones de dólares (≈63 % de los activos financieros mundiales); metodología de octubre de 2026.
- **Temática:** TFB-17 Sostenibilidad y clima: datos (principal) · secundarias: TFB-11
- **Calidad Q:** 78 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 12/15 · Independencia 9/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** secundaria (evaluación independiente con método publicado)
- **Acceso:** Abierto
- **Ámbitos:** Compromisos y actuación climática de entidades financieras
- **Motivo de inclusión y uso:** Evaluación climática de bancos, aseguradoras y gestoras candidatos. Bloque B: AG-B11 y AG-B12 (sector financiero).
- **Restricciones de uso:** Uso con cita.
- **Sesgos y cautelas:** Basado en información pública de las entidades; financiado por fundaciones filantrópicas.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «library guide climate ESG data sources Climate Action Tracker Net Zero Tracker Transition Pathway Initiative CDP Copernicus»; WebFetch: sí, documento de metodología 2026)
- **Origen:** Alta 2026-11-02 (F9 Bloque B, TFB-17).

#### MBF-0445 · Q 75 (B) — Climate TRACE — inventario independiente de emisiones por activo

- **Canal oficial (URL raíz):** https://www.climatetrace.org/about
- **Emisor:** Coalición Climate TRACE (fundada por WattTime, TransitionZero y otros; más de 100 organizaciones)
- **Documentación y notas:** Estimaciones de emisiones a nivel de activo para sectores que suman el 75 % de las emisiones mundiales, con datos de más de 300 satélites y más de 11.000 sensores y aprendizaje automático; publicaciones mensuales con dos meses de desfase (datos de agosto de 2026 publicados en octubre de 2026). Inventario también depositado en Zenodo.
- **Temática:** TFB-17 Sostenibilidad y clima: datos (principal) · secundarias: TFB-12
- **Calidad Q:** 75 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 12/15 · Independencia 9/10 · Actualidad 10/10 · Acceso 8/10
- **Tipología:** secundaria (estimaciones por teledetección y modelos)
- **Acceso:** Abierto (condiciones en climatetrace.org/terms, no leídas)
- **Ámbitos:** Emisiones por planta, mina, campo, puerto y país
- **Motivo de inclusión y uso:** Contraste independiente de las emisiones declaradas por candidatos. Bloque B: AG-B11 (riesgo de greenwashing), AG-B05 (activos de mayor emisión), AG-B12.
- **Restricciones de uso:** Consultar términos de uso antes de redistribuir.
- **Sesgos y cautelas:** Estimaciones de modelo con incertidumbre; métodos cambian entre versiones.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Copernicus Climate Data Store ERA5; Climate TRACE asset-level emissions; Global Carbon Budget data»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9 Bloque B, TFB-17).

#### MBF-0451 · Q 74 (B) — CDP — Corporate Environmental Action Tracker (CEAT)

- **Canal oficial (URL raíz):** https://cdp.net/en/data/corporate-environmental-action-tracker
- **Emisor:** CDP
- **Documentación y notas:** Herramienta interactiva (2023) con datos agregados de divulgación climática de CDP desde 2019: divulgación, gobernanza, objetivos, estrategia y planes de transición, cumplimiento e impacto de objetivos, por país, índice financiero y sector. Casi 12.000 empresas divulgaron en 2022 (18 % de las emisiones mundiales; 93 % del FTSE 100 y 86 % del S&P 500).
- **Temática:** TFB-17 Sostenibilidad y clima: datos (principal) · secundarias: TFB-07
- **Calidad Q:** 74 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 13/15 · Independencia 8/10 · Actualidad 7/10 · Acceso 8/10
- **Tipología:** secundaria (agregados de cuestionarios autodeclarados)
- **Acceso:** Abierto (agregados); datos por empresa de pago (futuro)
- **Ámbitos:** Divulgación y acción climática corporativa agregada
- **Motivo de inclusión y uso:** Comparar la madurez climática de sectores e índices. Bloque B: AG-B11 (calidad de la transición del sector), AG-B12.
- **Restricciones de uso:** Condiciones de CDP; datos detallados con licencia.
- **Sesgos y cautelas:** Datos autodeclarados; año de reporte desfasado un año.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «library guide climate ESG data sources Climate Action Tracker Net Zero Tracker Transition Pathway Initiative CDP Copernicus»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9 Bloque B, TFB-17).

#### MBF-0448 · Q 73 (B) — Climate Action Tracker — Data Explorer (calificaciones de países y referencias sectoriales)

- **Canal oficial (URL raíz):** URL raíz no leída; listado en NewClimate Institute, página de herramientas (https://www.newclimate.org/resources/tools)
- **Emisor:** Climate Action Tracker (NewClimate Institute y Climate Analytics)
- **Documentación y notas:** Herramienta interactiva para explorar los análisis de emisiones de países, sus calificaciones climáticas y referencias sectoriales.
- **Temática:** TFB-17 Sostenibilidad y clima: datos (principal) · secundarias: TFB-01
- **Calidad Q:** 73 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 12/15 · Independencia 9/10 · Actualidad 8/10 · Acceso 8/10
- **Tipología:** secundaria (análisis independiente con método publicado)
- **Acceso:** Abierto
- **Ámbitos:** Ambición y políticas climáticas por país
- **Motivo de inclusión y uso:** Riesgo regulatorio climático por país. Bloque B: AG-B07, AG-B11 y AG-B13 (escenarios de política por país).
- **Restricciones de uso:** Uso con cita.
- **Sesgos y cautelas:** Calificaciones normativas; sitio no leído en esta verificación.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «library guide climate ESG data sources Climate Action Tracker Net Zero Tracker Transition Pathway Initiative CDP Copernicus»; WebFetch: sí, NewClimate Institute, página de herramientas (https://www.newclimate.org/resources/tools))
- **Origen:** Alta 2026-11-02 (F9 Bloque B, TFB-17).

#### MBF-0460 · Q 72 (B) — ISIMIP — base de datos de impactos climáticos intersectoriales (datos físicos ampliados de la NGFS)

- **Canal oficial (URL raíz):** URL raíz no leída; enlazado desde https://www.ngfs.net/ngfs-scenarios-portal/data-resources/
- **Emisor:** Inter-Sectoral Impact Model Intercomparison Project (ISIMIP)
- **Documentación y notas:** Base de datos que, según el portal NGFS, aloja los datos ampliados de impacto físico de los escenarios NGFS (complemento del Climate Impact Explorer, MBF-0458).
- **Temática:** TFB-17 Sostenibilidad y clima: datos (principal) · secundarias: TFB-18
- **Calidad Q:** 72 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 12/15 · Independencia 10/10 · Actualidad 7/10 · Acceso 7/10
- **Tipología:** primaria (resultados de modelos de impacto intercomparados)
- **Acceso:** Abierto
- **Ámbitos:** Impactos físicos por sector (agua, agricultura, energía, salud) y región
- **Motivo de inclusión y uso:** Riesgo físico detallado para sectores expuestos al clima. Bloque B: AG-B11, AG-B05 y MC-B08.
- **Restricciones de uso:** Condiciones de ISIMIP.
- **Sesgos y cautelas:** Datos de modelos con alta incertidumbre; sitio no leído.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «NGFS Scenarios Portal climate scenarios data download; Climate Action Tracker country ratings»; WebFetch: sí, portal de escenarios NGFS (índice))
- **Origen:** Alta 2026-11-02 (F9 Bloque B, TFB-17).

#### MBF-0457 · Q 71 (B) — Climate Action 100+ — Net Zero Company Benchmark

- **Canal oficial (URL raíz):** https://embeddingproject.org/resources/climate-action-100-net-zero-benchmark/ (canal oficial: https://www.climateaction100.org/net-zero-company-benchmark/)
- **Emisor:** Climate Action 100+ (AIGCC, Ceres, IGCC, IIGCC y PRI)
- **Documentación y notas:** Base consultable con más de 150 evaluaciones de empresas focales sobre reducción de emisiones, gobernanza climática y divulgación, con investigación de TPI, Carbon Tracker, InfluenceMap y Rocky Mountain Institute; resumen de resultados 2024.
- **Temática:** TFB-17 Sostenibilidad y clima: datos (principal) · secundarias: TFB-11
- **Calidad Q:** 71 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 13/15 · Independencia 7/10 · Actualidad 7/10 · Acceso 9/10
- **Tipología:** secundaria (evaluación de una iniciativa inversora)
- **Acceso:** Abierto
- **Ámbitos:** Grandes emisores mundiales cotizados
- **Motivo de inclusión y uso:** Evaluación climática de grandes emisores del ámbito. Bloque B: AG-B11 y AG-B12.
- **Restricciones de uso:** Uso con cita.
- **Sesgos y cautelas:** Iniciativa de inversores con agenda de implicación; universo limitado.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «library guide climate ESG data sources Climate Action Tracker Net Zero Tracker Transition Pathway Initiative CDP Copernicus»; WebFetch: sí, ficha de The Embedding Project)
- **Origen:** Alta 2026-11-02 (F9 Bloque B, TFB-17).

#### MBF-0458 · Q 71 (B) — Climate Analytics — Climate Impact Explorer (datos de impacto físico de los escenarios NGFS)

- **Canal oficial (URL raíz):** URL raíz no leída; enlazado desde https://www.ngfs.net/ngfs-scenarios-portal/data-resources/
- **Emisor:** Climate Analytics (para la NGFS)
- **Documentación y notas:** Explorador de datos de impacto físico de los escenarios NGFS (descarga y API), con datos ampliados en la base ISIMIP.
- **Temática:** TFB-17 Sostenibilidad y clima: datos (principal) · secundarias: TFB-02
- **Calidad Q:** 71 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 12/15 · Independencia 9/10 · Actualidad 7/10 · Acceso 8/10
- **Tipología:** secundaria (resultados de modelos de impacto)
- **Acceso:** Abierto (descarga y API)
- **Ámbitos:** Impactos físicos del cambio climático por país y escenario
- **Motivo de inclusión y uso:** Riesgo físico por geografía para sectores expuestos (agricultura, seguros, inmobiliario, utilities). Bloque B: AG-B11 y MC-B08.
- **Restricciones de uso:** Condiciones de Climate Analytics y NGFS.
- **Sesgos y cautelas:** Resultados de modelos; sitio no leído.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «NGFS Scenarios Portal climate scenarios data download; Climate Action Tracker country ratings»; WebFetch: sí, portal de escenarios NGFS (índice))
- **Origen:** Alta 2026-11-02 (F9 Bloque B, TFB-17).

#### MBF-0449 · Q 70 (B) — Net Zero Tracker — objetivos de cero neto de países, regiones, ciudades y empresas

- **Canal oficial (URL raíz):** URL raíz no leída; listado en NewClimate Institute, página de herramientas (https://www.newclimate.org/resources/tools)
- **Emisor:** Net Zero Tracker (consorcio con participación de NewClimate Institute)
- **Documentación y notas:** Revisión independiente y de código abierto de los objetivos de cero neto de países, regiones, ciudades y empresas.
- **Temática:** TFB-17 Sostenibilidad y clima: datos (principal) · secundarias: TFB-07
- **Calidad Q:** 70 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 11/15 · Independencia 9/10 · Actualidad 8/10 · Acceso 8/10
- **Tipología:** secundaria (base de objetivos declarados)
- **Acceso:** Abierto
- **Ámbitos:** Objetivos de cero neto y su calidad
- **Motivo de inclusión y uso:** Complemento a SBTi (MBF-0442) para empresas sin validación. Bloque B: AG-B11 y AG-B12.
- **Restricciones de uso:** Uso con cita.
- **Sesgos y cautelas:** Basado en declaraciones públicas; sitio no leído.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «library guide climate ESG data sources Climate Action Tracker Net Zero Tracker Transition Pathway Initiative CDP Copernicus»; WebFetch: sí, NewClimate Institute, página de herramientas (https://www.newclimate.org/resources/tools))
- **Origen:** Alta 2026-11-02 (F9 Bloque B, TFB-17).

#### MBF-0450 · Q 69 (B) — Climate Policy Database — seguimiento de políticas climáticas por país

- **Canal oficial (URL raíz):** URL raíz no leída; listado en NewClimate Institute, página de herramientas (https://www.newclimate.org/resources/tools)
- **Emisor:** NewClimate Institute y colaboradores
- **Documentación y notas:** Herramienta abierta y colaborativa para seguir el estado de implantación de las políticas climáticas.
- **Temática:** TFB-17 Sostenibilidad y clima: datos (principal) · secundarias: TFB-16
- **Calidad Q:** 69 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 11/15 · Independencia 9/10 · Actualidad 7/10 · Acceso 8/10
- **Tipología:** secundaria (compilación colaborativa)
- **Acceso:** Abierto
- **Ámbitos:** Políticas climáticas por país y sector
- **Motivo de inclusión y uso:** Contraste de la IEA Policies Database (MBF-0413). Bloque B: AG-B07 y AG-B11.
- **Restricciones de uso:** Uso con cita.
- **Sesgos y cautelas:** Cobertura y actualización desiguales; sitio no leído.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «library guide climate ESG data sources Climate Action Tracker Net Zero Tracker Transition Pathway Initiative CDP Copernicus»; WebFetch: sí, NewClimate Institute, página de herramientas (https://www.newclimate.org/resources/tools))
- **Origen:** Alta 2026-11-02 (F9 Bloque B, TFB-17).

#### MBF-0447 · Q 68 (B) — ICAP — datos de sistemas de comercio de emisiones (fuente de la Carbon Pricing Dashboard)

- **Canal oficial (URL raíz):** URL raíz no leída; citado como proveedor de datos ETS en https://carbonpricingdashboard.worldbank.org/about
- **Emisor:** International Carbon Action Partnership (ICAP)
- **Documentación y notas:** Organización que aporta los datos de sistemas de comercio de emisiones a la Carbon Pricing Dashboard del Banco Mundial (MBF-0446).
- **Temática:** TFB-17 Sostenibilidad y clima: datos (principal) · secundarias: TFB-12
- **Calidad Q:** 68 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 12/15 · Independencia 9/10 · Actualidad 7/10 · Acceso 6/10
- **Tipología:** secundaria (compilación de datos oficiales de ETS)
- **Acceso:** Abierto (según el Banco Mundial; no leído)
- **Ámbitos:** Diseño, cobertura y precios de los ETS del mundo
- **Motivo de inclusión y uso:** Detalle de ETS nacionales y subnacionales. Bloque B: AG-B07 y AG-B11.
- **Restricciones de uso:** Comprobar condiciones al primer uso.
- **Sesgos y cautelas:** Sitio no leído; usar a través de MBF-0446 hasta verificarlo.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «World Bank Carbon Pricing Dashboard; ICAP Allowance Price Explorer; CDP open data portal emissions disclosure»; WebFetch: sí, página «About» de la Carbon Pricing Dashboard (índice))
- **Origen:** Alta 2026-11-02 (F9 Bloque B, TFB-17).

#### MBF-0454 · Q 66 (B) — Open Net Zero (Icebreaker One) — catálogo de datos de transición, incluidos los conjuntos del TPI

- **Canal oficial (URL raíz):** https://opennetzero.org/organization/transition-pathway-initiative
- **Emisor:** Icebreaker One (IB1)
- **Documentación y notas:** Servicio para encontrar, acceder y compartir datos de cero neto; publica fichas de los conjuntos del TPI (bancos: piloto de 27 entidades con IIGCC; 30 mayores emisores de bonos de electricidad y petróleo y gas; todos los sectores).
- **Temática:** TFB-17 Sostenibilidad y clima: datos (principal) · secundarias: TFB-18
- **Calidad Q:** 66 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 10/15 · Independencia 9/10 · Actualidad 7/10 · Acceso 9/10
- **Tipología:** terciaria (catálogo de datos)
- **Acceso:** Abierto
- **Ámbitos:** Conjuntos de datos climáticos y de transición
- **Motivo de inclusión y uso:** Descubrimiento de datos abiertos de transición. Bloque B: AG-B20 y AG-B11.
- **Restricciones de uso:** Licencias según cada conjunto; el catálogo indica que la licencia del TPI «no es definitiva».
- **Sesgos y cautelas:** Catálogo, no fuente primaria; enlazar siempre a la raíz.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Transition Pathway Initiative TPI Centre company assessments data; Climate Bonds Initiative green bond database; EM-DAT disaster database; ND-GAIN index»; WebFetch: sí)
- **Origen:** Alta 2026-11-02 (F9 Bloque B, TFB-17).

#### MBF-0456 · Q 54 (C) — S&P Global — Net-Zero Commitments Tracker (conjunto de datos de pago)

- **Canal oficial (URL raíz):** https://www.marketplace.spglobal.com/en/datasets/net-zero-commitments-tracker-(1705058628)
- **Emisor:** S&P Global
- **Documentación y notas:** Conjunto de datos del Marketplace de S&P Global que sigue y analiza los objetivos corporativos de reducción de emisiones y su alineamiento con los objetivos climáticos; la ficha no detalla cobertura, campos ni precios.
- **Temática:** TFB-17 Sostenibilidad y clima: datos (principal) · secundarias: TFB-07
- **Calidad Q:** 54 (C) — Primariedad 10/20 · Historial 10/20 · Transparencia 6/15 · Autoridad 12/15 · Independencia 7/10 · Actualidad 7/10 · Acceso 2/10
- **Tipología:** secundaria (proveedor de datos)
- **Acceso:** De pago (futuro)
- **Ámbitos:** Objetivos corporativos de cero neto
- **Motivo de inclusión y uso:** Referencia para una futura conexión de pago. Bloque B: AG-B11 y AG-B12.
- **Restricciones de uso:** De pago (futuro); requiere licencia gestionada por el Broker.
- **Sesgos y cautelas:** Contenido no verificable sin licencia.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «library guide climate ESG data sources Climate Action Tracker Net Zero Tracker Transition Pathway Initiative CDP Copernicus»; WebFetch: sí, ficha del Marketplace)
- **Origen:** Alta 2026-11-02 (F9 Bloque B, TFB-17).

## TFB-18 Repositorios académicos y de investigación abierta

#### RF-0420 · Q 84 (A) — Crossref (registro de DOI y metadatos abiertos)

- **Canal oficial (URL raíz):** https://www.crossref.org/
- **Emisor:** Crossref (organización sin ánimo de lucro con más de 19.000 miembros)
- **Temática:** TFB-18 Repositorios académicos y de investigación abierta (principal) · secundarias: —
- **Calidad Q:** 84 (A) — Primariedad 16/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 14/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria (registro oficial de metadatos de DOI)
- **Acceso:** Abierto (API REST de metadatos)
- **Ámbitos:** Unos 150 millones de registros DOI; metadatos de obras, financiadores, referencias y retractaciones
- **Motivo de inclusión y uso:** detección de retractaciones vía datos de Retraction Watch (RF-0421). **Uso en el Bloque B:** AG-B18 y AG-B20 (verificación de DOI y metadatos de toda referencia), AG-B15.
- **Sesgos y cautelas:** Calidad de metadatos dependiente de lo que depositan los editores.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Crossref Retraction Watch database open retraction data»; WebFetch: sí, nota de EASE (14/09/2023) que enlaza crossref.org; la web no se cargó)
- **Origen:** Alta F9_S3 (2026-11-02). Reutilizada en F9 Bloque B (TFB-18) el 2026-11-02.

#### RF-0422 · Q 84 (A) — BIS Working Papers

- **Canal oficial (URL raíz):** https://www.bis.org/wpapers
- **Emisor:** Bank for International Settlements (BIS)
- **Temática:** TFB-18 Repositorios académicos y de investigación abierta (principal) · secundarias: TFB-02
- **Calidad Q:** 84 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria (documentos de trabajo)
- **Acceso:** Abierto
- **Ámbitos:** Investigación de economistas del BIS y ocasionalmente de bancos centrales y universidades: política monetaria, estabilidad financiera, mercados
- **Motivo de inclusión y uso:** Investigación de frontera de banca central con datos propios del BIS. **Uso en el Bloque B:** AG-B08 y AG-B09 (investigación del BIS sobre crédito, inmobiliario, sistema financiero y tecnología).
- **Sesgos y cautelas:** Las opiniones son de los autores y no necesariamente del BIS; sin revisión por pares completa.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ECB Working Paper Series BIS Working Papers IMF Working Papers»; WebFetch: sí)
- **Origen:** Alta F9_S3 (2026-11-02). Reutilizada en F9 Bloque B (TFB-18) el 2026-11-02.

#### RF-0423 · Q 84 (A) — ECB Working Paper Series

- **Canal oficial (URL raíz):** https://www.ecb.europa.eu/press/research-publications/working-papers
- **Emisor:** Banco Central Europeo (BCE)
- **Temática:** TFB-18 Repositorios académicos y de investigación abierta (principal) · secundarias: TFB-02
- **Calidad Q:** 84 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria (documentos de trabajo)
- **Acceso:** Abierto
- **Ámbitos:** Investigación económica relevante para las funciones del BCE: política monetaria, transmisión, banca, mercados del área del euro
- **Motivo de inclusión y uso:** Literatura de banca central europea para fundamentar análisis del área del euro. **Uso en el Bloque B:** AG-B08 (investigación del BCE sobre sectores, empresas y transmisión monetaria en la zona del euro).
- **Sesgos y cautelas:** Trabajo en curso; las opiniones son de los autores y no necesariamente del BCE.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «ECB Working Paper Series BIS Working Papers IMF Working Papers»; WebFetch: sí)
- **Origen:** Alta F9_S3 (2026-11-02). Reutilizada en F9 Bloque B (TFB-18) el 2026-11-02.

#### RF-0461 · Q 84 (A) — IMF Working Papers

- **Canal oficial (URL raíz):** https://www.imf.org/en/Publications/WP (ruta de la serie vista en los resultados; página leída: https://www.imf.org/en/Publications/WP/Issues/2016/12/30/Working-Paper-Summaries-WP-95-62-95-146-2022)
- **Emisor:** Fondo Monetario Internacional (FMI)
- **Temática:** TFB-18 Repositorios académicos y de investigación abierta (principal) · secundarias: TFB-02
- **Calidad Q:** 84 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria (documentos de trabajo)
- **Acceso:** Abierto (con DOI)
- **Ámbitos:** Unos 300 documentos al año de personal del FMI: balanza de pagos, política monetaria y fiscal, liquidez global, economías nacionales
- **Motivo de inclusión y uso:** Investigación aplicada de un organismo internacional con cobertura de emergentes. **Uso en el Bloque B:** AG-B07 y AG-B08 (investigación del FMI sobre política industrial, comercio y sectores por país).
- **Sesgos y cautelas:** No representan la opinión del FMI; sin revisión por pares completa.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «IMF Working Papers series imf.org publications»; WebFetch: sí)
- **Origen:** Alta F9_S3, tanda 3 (2026-11-02). Reutilizada en F9 Bloque B (TFB-18) el 2026-11-02.

#### RF-0424 · Q 83 (A) — Banco de España — Documentos de Trabajo

- **Canal oficial (URL raíz):** https://www.bde.es/bde/en/secciones/informes/analisis-economico-e-investigacion/documentos-de-trabajo/ (repositorio: https://repositorio.bde.es/handle/123456789/5661)
- **Emisor:** Banco de España
- **Temática:** TFB-18 Repositorios académicos y de investigación abierta (principal) · secundarias: TFB-02
- **Calidad Q:** 83 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 14/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria (documentos de trabajo)
- **Acceso:** Abierto (PDF; serie desde 1978 en el repositorio institucional)
- **Ámbitos:** Macroeconomía, política monetaria, banca, finanzas y economía española; último visto: n.º 2640 (26/10/2026)
- **Motivo de inclusión y uso:** Investigación de banco central con foco España y área del euro. **Uso en el Bloque B:** AG-B08 y AG-B03 (investigación del Banco de España sobre empresas, vivienda y sectores españoles).
- **Sesgos y cautelas:** Opiniones de los autores; sin revisión por pares completa.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Banco de España documentos de trabajo Federal Reserve FEDS finance and economics discussion series»; WebFetch: sí)
- **Origen:** Alta F9_S3 (2026-11-02). Reutilizada en F9 Bloque B (TFB-18) el 2026-11-02.

#### RF-0008 · Q 82 (A) — NBER Working Papers (National Bureau of Economic Research)

- **Canal oficial:** nber.org/papers
- **Documentación y notas:** Trabajos con página propia por número (nber.org/papers/wNNNNN); citar número de WP y año; versiones abiertas del autor frecuentes
- **Temática:** TFB-18 Repositorios académicos y de investigación abierta (principal) · secundarias: —
- **Calidad Q:** 82 (A) — Primariedad 18/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 14/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 9/10
- **Nivel de fiabilidad en V2.4:** B
- **Tipología:** primaria (trabajos originales sin revisión por pares completa)
- **Motivo de inclusión:** Documentos de trabajo de investigación económica de primer nivel; muchos se publican después en revistas revisadas por pares. **Uso en el Bloque B:** AG-B03, AG-B06 y AG-B09 (investigación de frontera en organización industrial, productividad, innovación y finanzas).
- **Ámbitos:** Investigación económica y financiera; literatura de frontera; datos y metodologías nuevos
- **Restricciones de uso:** Muchos WP son de descarga gratuita y otros tienen coste o requieren registro; verificar pieza a pieza; un WP no está revisado por pares: citarlo como documento de trabajo
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Sesgos posibles:** Contenido no revisado por pares en el momento de la publicación; verificar si existe versión publicada posterior
- **Cambios de propiedad o de metodología:** Sin cambios conocidos
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «SSRN NBER working papers RePEc IDEAS arXiv q-fin EconStor open access economics repositories»; WebFetch: sí, página índice https://guides.libraries.emory.edu/main/economics/working_papers; el sitio propio no se leyó)
- **Origen:** Reutilizada del Bloque A (ID original) en F9 Bloque B (TFB-18) el 2026-11-02.

#### RF-0421 · Q 82 (A) — Retraction Watch Database (datos abiertos vía Crossref)

- **Canal oficial (URL raíz):** https://retractionwatch.com/the-retraction-watch-database/ (datos: https://gitlab.com/crossref/retraction-watch-data)
- **Emisor:** Retraction Watch / Center for Scientific Integrity; datos adquiridos y abiertos por Crossref en 2023
- **Temática:** TFB-18 Repositorios académicos y de investigación abierta (principal) · secundarias: —
- **Calidad Q:** 82 (A) — Primariedad 17/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 13/15 · Independencia 9/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** primaria (registro de retractaciones)
- **Acceso:** Abierto
- **Ámbitos:** Retractaciones, expresiones de preocupación y correcciones de artículos académicos
- **Motivo de inclusión y uso:** **Uso en el Bloque B:** AG-B15 y AG-B22 (comprobar que ninguna evidencia citada esté retractada).
- **Sesgos y cautelas:** Cobertura incompleta en ciencias sociales y documentos de trabajo.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Crossref Retraction Watch database open retraction data»; WebFetch: sí)
- **Origen:** Alta F9_S3 (2026-11-02). Reutilizada en F9 Bloque B (TFB-18) el 2026-11-02.

#### RF-0462 · Q 82 (A) — Zenodo (repositorio abierto de CERN y OpenAIRE)

- **Emisor/organización:** CERN, en el marco de OpenAIRE (Comisión Europea)
- **Año:** Servicio vigente
- **Publicación o institución:** Repositorio multidisciplinar de investigación abierta
- **Tipo de documento:** Repositorio de publicaciones, datos y software con DOI
- **Temática:** TFB-18 Repositorios académicos y de investigación abierta (principal) · secundarias: —
- **Calidad Q:** 82 (A) — Primariedad 16/20 · Exactitud histórica 10/20 · Transparencia 15/15 · Autoridad 14/15 · Independencia 10/10 · Actualidad 8/10 · Accesibilidad 9/10
- **Canal oficial (URL raíz):** https://zenodo.org (confirmada en la página oficial de OpenAIRE, https://www.openaire.eu/zenodo/)
- **Acceso y licencia:** Gratuito; cada depósito recibe DOI; recolectable por OAI-PMH; licencia según depósito
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Zenodo open repository CERN research data publications»; WebFetch: sí, a openscience.web.cern.ch/zenodo y openaire.eu/zenodo, que confirman operador, DOI y URL)
- **Contenido:** Repositorio de CERN para cualquier resultado de investigación (artículos, datos, código), con DOI y vínculo a financiadores; útil para localizar datos y código de réplica de artículos.
- **Uso en el bloque:** DOC-A, DOC-M y Motor: obtener datos y código de réplica citables; Curador: identificar versiones y DOI de depósitos.
- **Limitaciones:** No hay revisión por pares de los depósitos; la calidad depende del autor. Sustituye a RF-0425 (duplicado de FRASER).
- **Origen:** Reutilizada del Bloque A (ID original) en F9 Bloque B (TFB-18) el 2026-11-02.

#### RF-0426 · Q 81 (A) — Fed in Print (catálogo de investigación del Sistema de la Reserva Federal)

- **Canal oficial (URL raíz):** https://www.fedinprint.org/
- **Emisor:** Sistema de la Reserva Federal (Board of Governors y los 12 bancos regionales)
- **Temática:** TFB-18 Repositorios académicos y de investigación abierta (principal) · secundarias: TFB-02
- **Calidad Q:** 81 (A) — Primariedad 14/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** terciaria (catálogo de publicaciones)
- **Acceso:** Abierto (API y RSS)
- **Ámbitos:** Documentos de trabajo, informes y blogs de toda la Reserva Federal, por banco, serie, autor y código JEL
- **Motivo de inclusión y uso:** Punto único de búsqueda de la investigación de la Fed (FEDS, Staff Reports, Liberty Street, On the Economy). **Uso en el Bloque B:** AG-B08 (investigación del Sistema de la Reserva Federal sobre sectores y ciclo).
- **Sesgos y cautelas:** Enlaza al texto en la web de cada banco; no aloja contenido.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «FRASER Federal Reserve Bank of St. Louis digital library EconStor ZBW open access economics repository»; WebFetch: sí, ficha de registro en fedinprint.org)
- **Origen:** Alta F9_S3 (2026-11-02). Reutilizada en F9 Bloque B (TFB-18) el 2026-11-02.

#### RF-0089 · Q 79 (B) — OpenAlex

- **Canal oficial (URL raíz):** https://openalex.org/ (API: api.openalex.org)
- **Emisor:** OurResearch (organización sin ánimo de lucro, fundada en 2011)
- **Temática:** TFB-18 Repositorios académicos y de investigación abierta (principal) · secundarias: —
- **Calidad Q:** 79 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 12/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** terciaria
- **Acceso:** Abierto (datos CC0; API con cuota gratuita diaria y precios por uso desde febrero de 2026; búsquedas por ID o DOI gratuitas; volcado completo en S3)
- **Ámbitos:** Índice abierto de obras, autores, revistas, instituciones y conceptos; sustituto del Microsoft Academic Graph desde enero de 2022
- **Motivo de inclusión y uso:** Metadatos abiertos, citas y detección de acceso abierto con API documentada; **Uso en el Bloque B:** AG-B18 y AG-B20 (búsqueda bibliométrica abierta y grafos de citas para revisar la literatura de un sector).
- **Sesgos y cautelas:** Errores de desambiguación de autores; parte de la jerarquía de conceptos heredada de MAG.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «OpenAlex Unpaywall OurResearch open scholarly metadata API»; WebFetch: sí, artículo de Priem, Piwowar y Orr (2022) en arXiv:2205.01833 y guía de CASRAI; openalex.org no se cargó)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada por BFA en F9_S3 (2026-11-02). Q corregida de 80 a 79 por el nuevo modelo de precios de la API. Reutilizada en F9 Bloque B (TFB-18) el 2026-11-02.

#### RF-0419 · Q 79 (B) — Unpaywall

- **Canal oficial (URL raíz):** https://unpaywall.org/
- **Emisor:** OurResearch
- **Temática:** TFB-18 Repositorios académicos y de investigación abierta (principal) · secundarias: —
- **Calidad Q:** 79 (B) — Primariedad 13/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 12/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** terciaria (base de estado de acceso abierto)
- **Acceso:** Abierto (API REST gratuita por DOI con correo de contacto; volcados periódicos; extensión de navegador)
- **Ámbitos:** Estado de acceso abierto por DOI (gold, hybrid, green, bronze, closed) y mejor ubicación abierta legal
- **Motivo de inclusión y uso:** Comprobación automática de la existencia de versión abierta legal para cada DOI de F7, F8 y FM; alimenta el campo «Acceso y licencia». **Uso en el Bloque B:** AG-B18 y AG-B20 (localizar versiones en acceso abierto de artículos de pago).
- **Sesgos y cautelas:** No aloja contenido; la clasificación puede errar en versiones de autor.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «OpenAlex Unpaywall OurResearch open scholarly metadata API»; WebFetch: sí, guía de CASRAI sobre Unpaywall; unpaywall.org no se cargó)
- **Origen:** Alta F9_S3 (2026-11-02). Reutilizada en F9 Bloque B (TFB-18) el 2026-11-02.

#### MBF-0564 · Q 78 (B) — OCDE — Economics Department Working Papers

- **Canal oficial (URL raíz):** https://www.oecd-ilibrary.org/economics/oecd-economics-department-working-papers_18151973
- **Emisor:** Organización para la Cooperación y el Desarrollo Económicos (OCDE)
- **Documentación y notas:** Serie de documentos de trabajo del Departamento de Economía de la OCDE a texto completo, listada en la guía de la biblioteca del Imperial College.
- **Temática:** TFB-18 Repositorios académicos y de investigación abierta (principal) · secundarias: TFB-01
- **Calidad Q:** 78 (B) — Primariedad 17/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 14/15 · Independencia 9/10 · Actualidad 8/10 · Acceso 9/10
- **Tipología:** primaria (documentos de trabajo)
- **Acceso:** Abierto
- **Ámbitos:** Productividad, competencia, regulación de mercados de productos, política estructural
- **Motivo de inclusión y uso:** Evidencia comparada por país sobre competencia, regulación y productividad sectorial. Bloque B: AG-B03, AG-B07 y AG-B08.
- **Restricciones de uso:** Condiciones de la OCDE.
- **Sesgos y cautelas:** Opiniones de los autores, no de la OCDE.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «SSRN NBER working papers RePEc IDEAS arXiv q-fin EconStor open access economics repositories»; WebFetch: sí, página índice https://imperial.ac.uk/admin-services/library/subject-support/business/academic-journals-and-working-papers)
- **Origen:** Alta 2026-11-02 (F9 Bloque B, TFB-18).

#### RF-0090 · Q 78 (B) — CEPR — VoxEU

- **Canal oficial (URL raíz):** https://cepr.org/voxeu
- **Emisor:** Centre for Economic Policy Research (CEPR)
- **Temática:** TFB-18 Repositorios académicos y de investigación abierta (principal) · secundarias: TFB-11
- **Calidad Q:** 78 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 13/15 · Independencia 9/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** secundaria
- **Acceso:** Abierto (columnas descargables sin suscripción)
- **Ámbitos:** Columnas de investigación aplicada de economistas académicos; consorcio de portales asociados (p. ej., Nada es Gratis, RF-0416)
- **Motivo de inclusión y uso:** Síntesis accesibles de investigación reciente con enlace al trabajo de origen. **Uso en el Bloque B:** AG-B07 y AG-B08 (síntesis divulgativa de investigación sobre comercio, política industrial y mercados).
- **Sesgos y cautelas:** Columnas sin revisión por pares completa.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Nada es Gratis blog economía Fedea»; WebFetch: sí, columna en cepr.org/voxeu)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada por BFA en F9_S3 (2026-11-02). Reutilizada en F9 Bloque B (TFB-18) el 2026-11-02.

#### RF-0418 · Q 78 (B) — CORE (agregador de investigación en acceso abierto)

- **Canal oficial (URL raíz):** https://core.ac.uk/
- **Emisor:** CORE, Open University (Reino Unido)
- **Temática:** TFB-18 Repositorios académicos y de investigación abierta (principal) · secundarias: —
- **Calidad Q:** 78 (B) — Primariedad 13/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 12/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** terciaria (agregador de texto completo)
- **Acceso:** Abierto
- **Ámbitos:** Millones de textos completos en acceso abierto de cientos de repositorios y revistas; búsqueda, minería y desarrollo de aplicaciones
- **Motivo de inclusión y uso:** Localiza el texto completo abierto de trabajos citados en F7 y F8 cuando el editor tiene muro de pago. **Uso en el Bloque B:** AG-B18 y AG-B20 (texto completo agregado de repositorios institucionales).
- **Sesgos y cautelas:** Metadatos heterogéneos de los repositorios de origen; duplicados de versiones.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «CORE core.ac.uk Semantic Scholar BASE Bielefeld open access aggregator»; WebFetch: sí)
- **Origen:** Alta F9_S3 (2026-11-02). Reutilizada en F9 Bloque B (TFB-18) el 2026-11-02.

#### RF-0459 · Q 78 (B) — Semantic Scholar

- **Canal oficial (URL raíz):** https://www.semanticscholar.org/
- **Emisor:** Ai2 (Allen Institute for Artificial Intelligence)
- **Temática:** TFB-18 Repositorios académicos y de investigación abierta (principal) · secundarias: —
- **Calidad Q:** 78 (B) — Primariedad 13/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 12/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** terciaria (buscador académico con IA)
- **Acceso:** Abierto (API gratuita; datos con licencia ODC-BY 1.0)
- **Ámbitos:** Más de 214 millones de artículos; grafo de citas, recomendaciones, resúmenes TLDR; lanzado en 2015
- **Motivo de inclusión y uso:** Búsqueda y grafo de citas con API abierta; alternativa a RF-0088. **Uso en el Bloque B:** AG-B18 y AG-B20 (búsqueda semántica y recomendaciones de literatura).
- **Sesgos y cautelas:** Fusiones de registros erróneas; TLDR en beta y con cobertura parcial.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Semantic Scholar Allen Institute for AI academic search engine API»; WebFetch: sí, guía de CASRAI; semanticscholar.org no se cargó)
- **Origen:** Alta F9_S3, tanda 3 (2026-11-02). Reutilizada en F9 Bloque B (TFB-18) el 2026-11-02.

#### RF-0460 · Q 77 (B) — DOAJ — Directory of Open Access Journals

- **Canal oficial (URL raíz):** https://doaj.org/
- **Emisor:** DOAJ (independiente, financiado con donaciones; activo desde 2003)
- **Temática:** TFB-18 Repositorios académicos y de investigación abierta (principal) · secundarias: —
- **Calidad Q:** 77 (B) — Primariedad 13/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 12/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** terciaria (índice de revistas en acceso abierto)
- **Acceso:** Abierto (datos abiertos)
- **Ámbitos:** Índice de revistas de acceso abierto revisadas por editores y voluntarios
- **Motivo de inclusión y uso:** Filtro de revistas de acceso abierto legítimas (prevención de revistas depredadoras en F7 y F8). **Uso en el Bloque B:** AG-B18 (filtrar revistas de acceso abierto legítimas).
- **Sesgos y cautelas:** La página leída no detalla los criterios de inclusión ni el número de revistas.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «DOAJ Directory of Open Access Journals about»; WebFetch: sí)
- **Origen:** Alta F9_S3, tanda 3 (2026-11-02). Reutilizada en F9 Bloque B (TFB-18) el 2026-11-02.

#### MBF-0561 · Q 75 (B) — EconStor — repositorio abierto de economía (ZBW)

- **Canal oficial (URL raíz):** http://www.econstor.eu/ (según la guía de la Marshall Library, Cambridge)
- **Emisor:** ZBW – Leibniz Information Centre for Economics
- **Documentación y notas:** Repositorio de documentos de trabajo, documentos de discusión y actas de congresos de instituciones económicas alemanas y algunas estadounidenses; acceso sin restricciones.
- **Temática:** TFB-18 Repositorios académicos y de investigación abierta (principal) · secundarias: —
- **Calidad Q:** 75 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 12/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** primaria (documentos de trabajo depositados por sus autores e instituciones)
- **Acceso:** Abierto
- **Ámbitos:** Economía y finanzas, con fuerte presencia de institutos europeos
- **Motivo de inclusión y uso:** Literatura gris europea sobre sectores y política industrial. Bloque B: AG-B18 y AG-B20 (búsqueda de evidencia), especialistas AG-B03 a AG-B11.
- **Restricciones de uso:** Licencias por documento.
- **Sesgos y cautelas:** Calidad heterogénea; sin revisión por pares.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «SSRN NBER working papers RePEc IDEAS arXiv q-fin EconStor open access economics repositories»; WebFetch: sí, página índice https://www.marshall.econ.cam.ac.uk/onlineresources/economics-subject-repositories)
- **Origen:** Alta 2026-11-02 (F9 Bloque B, TFB-18).

#### RF-0010 · Q 75 (B) — arXiv q-fin (Quantitative Finance)

- **Canal oficial:** arxiv.org/list/q-fin/recent
- **Documentación y notas:** Documentación de API: info.arxiv.org/help/api/ · Citar identificador arXiv y versión (ficha)
- **Temática:** TFB-18 Repositorios académicos y de investigación abierta (principal) · secundarias: TFB-09
- **Calidad Q:** 75 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 10/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 10/10
- **Nivel de fiabilidad en V2.4:** B
- **Tipología:** primaria (preprints)
- **Motivo de inclusión:** Repositorio abierto de preprints de finanzas cuantitativas y econofísica: acceso gratuito e inmediato. **Uso en el Bloque B:** AG-B06 y AG-B16 (preprints de finanzas cuantitativas y métodos para el Motor, MC-B07/MC-B10).
- **Ámbitos:** Finanzas cuantitativas; modelización; econofísica; métodos estadísticos
- **Restricciones de uso:** Licencias abiertas por pieza (frecuente arXiv non-exclusive); citar identificador arXiv y versión
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Sesgos posibles:** Sin revisión por pares (solo moderación de ámbito); calidad heterogénea
- **Cambios de propiedad o de metodología:** Sin cambios conocidos
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «SSRN NBER working papers RePEc IDEAS arXiv q-fin EconStor open access economics repositories»; WebFetch: sí, página índice https://imperial.ac.uk/admin-services/library/subject-support/business/academic-journals-and-working-papers; el sitio propio no se leyó)
- **Origen:** Reutilizada del Bloque A (ID original) en F9 Bloque B (TFB-18) el 2026-11-02.

#### RF-0088 · Q 75 (B) — Google Scholar

- **Canal oficial (URL raíz):** https://scholar.google.com/
- **Emisor:** Google
- **Temática:** TFB-18 Repositorios académicos y de investigación abierta (principal) · secundarias: —
- **Calidad Q:** 75 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 12/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 10/10
- **Tipología:** terciaria
- **Acceso:** Abierto
- **Ámbitos:** Búsqueda académica, recuento de citas, versiones de autor; cobertura estimada del 79–90 % de los artículos académicos en inglés
- **Motivo de inclusión y uso:** Descubrimiento de literatura, búsqueda hacia adelante y localización de versiones abiertas. **Uso en el Bloque B:** AG-B18 y AG-B20 (búsqueda amplia y recuento de citas como señal de influencia).
- **Sesgos y cautelas:** No publica la lista de fuentes que rastrea ni su frecuencia de actualización; sin API pública ni exportación de DOI; indexa revistas depredadoras; recuentos de citas manipulables (artículos generados con SCIgen, servicios de compra de citas documentados en 2024).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «Wikipedia list of academic databases and search engines»; WebFetch: sí, listado y artículo de Wikipedia sobre Google Scholar; scholar.google.com no se cargó)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada por BFA en F9_S3 (2026-11-02). Q corregida de 78 a 75 por la opacidad de cobertura y la manipulabilidad de citas documentadas. Reutilizada en F9 Bloque B (TFB-18) el 2026-11-02.

#### MBF-0563 · Q 74 (B) — CEPR — Discussion Papers (documentos de trabajo)

- **Canal oficial (URL raíz):** Enlace persistente de la guía de Emory: http://pid.emory.edu/cj16d
- **Emisor:** Centre for Economic Policy Research (CEPR)
- **Documentación y notas:** Red europea de investigación económica: documentos de discusión a texto completo, resúmenes de los anteriores y documentos de política. Complementa VoxEU (RF-0090).
- **Temática:** TFB-18 Repositorios académicos y de investigación abierta (principal) · secundarias: TFB-11
- **Calidad Q:** 74 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 13/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 7/10
- **Tipología:** primaria (documentos de trabajo)
- **Acceso:** Mixto (resúmenes abiertos; texto completo según suscripción o acceso)
- **Ámbitos:** Economía industrial, comercio, finanzas, macroeconomía
- **Motivo de inclusión y uso:** Investigación de frontera sobre organización industrial y comercio para el análisis sectorial. Bloque B: AG-B03, AG-B05 y AG-B07.
- **Restricciones de uso:** Condiciones de CEPR.
- **Sesgos y cautelas:** Sin revisión por pares completa.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «SSRN NBER working papers RePEc IDEAS arXiv q-fin EconStor open access economics repositories»; WebFetch: sí, página índice https://guides.libraries.emory.edu/main/economics/working_papers)
- **Origen:** Alta 2026-11-02 (F9 Bloque B, TFB-18).

#### RF-0009 · Q 72 (B) — SSRN (Social Science Research Network)

- **Canal oficial:** ssrn.com
- **Documentación y notas:** Resúmenes y descargas gratuitas con registro; citar el abstract_id de cada trabajo
- **Temática:** TFB-18 Repositorios académicos y de investigación abierta (principal) · secundarias: —
- **Calidad Q:** 72 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 10/15 · Independencia 9/10 · Actualidad 10/10 · Acceso 8/10
- **Nivel de fiabilidad en V2.4:** B
- **Tipología:** primaria (preprints)
- **Motivo de inclusión:** Principal repositorio de preprints de finanzas y economía: acceso temprano a la investigación antes de su publicación en revista. **Uso en el Bloque B:** AG-B09, AG-B12 y AG-B16 (preprints de finanzas, valoración sectorial y selección de activos).
- **Ámbitos:** Finanzas; economía; literatura de frontera; versiones de autor
- **Restricciones de uso:** Descarga gratuita con registro; citar como preprint con su abstract_id y comprobar si existe versión publicada posterior
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Sesgos posibles:** Sin revisión por pares garantizada; sesgo de publicación de autores y de papers aún no filtrados
- **Cambios de propiedad o de metodología:** Propiedad de Elsevier desde 2016; vigilar cambios de acceso
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «SSRN NBER working papers RePEc IDEAS arXiv q-fin EconStor open access economics repositories»; WebFetch: sí, página índice https://www.marshall.econ.cam.ac.uk/onlineresources/economics-subject-repositories, https://guides.libraries.emory.edu/main/economics/working_papers y https://imperial.ac.uk/admin-services/library/subject-support/business/academic-journals-and-working-papers; el sitio propio no se leyó)
- **Origen:** Reutilizada del Bloque A (ID original) en F9 Bloque B (TFB-18) el 2026-11-02.

#### MBF-0562 · Q 70 (B) — EconPapers — interfaz de RePEc (Örebro University)

- **Canal oficial (URL raíz):** http://econpapers.repec.org/ (también http://econpapers.hhs.se/)
- **Emisor:** Örebro University School of Business, sobre los datos de RePEc
- **Documentación y notas:** Acceso a la colección RePEc de documentos de trabajo, artículos y software de economía; la guía de Emory la describe con más de 100.000 documentos de trabajo referenciados y texto completo en más de la mitad.
- **Temática:** TFB-18 Repositorios académicos y de investigación abierta (principal) · secundarias: —
- **Calidad Q:** 70 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 11/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** terciaria (índice bibliográfico)
- **Acceso:** Abierto
- **Ámbitos:** Economía y finanzas
- **Motivo de inclusión y uso:** Vía alternativa a IDEAS (RF-0011) para localizar trabajos y series. Bloque B: AG-B18 y AG-B20.
- **Restricciones de uso:** Uso libre; citar la fuente original del documento.
- **Sesgos y cautelas:** Índice; enlazar siempre a la raíz.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «SSRN NBER working papers RePEc IDEAS arXiv q-fin EconStor open access economics repositories»; WebFetch: sí, páginas índice https://guides.libraries.emory.edu/main/economics/working_papers y https://imperial.ac.uk/admin-services/library/subject-support/business/academic-journals-and-working-papers)
- **Origen:** Alta 2026-11-02 (F9 Bloque B, TFB-18).

#### RF-0011 · Q 70 (B) — RePEc / IDEAS (Research Papers in Economics)

- **Canal oficial:** ideas.repec.org
- **Documentación y notas:** Espejo: econpapers.repec.org · Útil para metadatos normalizados de trabajos y revistas económicas que sustentan otras entradas (NBER, SSRN, FAJ)
- **Temática:** TFB-18 Repositorios académicos y de investigación abierta (principal) · secundarias: —
- **Calidad Q:** 70 (B) — Primariedad 8/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 12/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 10/10
- **Nivel de fiabilidad en V2.4:** B
- **Tipología:** terciaria (agregador)
- **Motivo de inclusión:** Agregador académico descentralizado de literatura económica: localiza versiones de acceso gratuito (verdes) de artículos publicados en revistas de pago. **Uso en el Bloque B:** AG-B18 y AG-B20 (índice de documentos de trabajo y perfiles de autores en economía).
- **Ámbitos:** Economía y finanzas; localización de versiones de trabajo y de acceso gratuito; bibliografía estructurada
- **Restricciones de uso:** Es un agregador: citar la fuente primaria que RePEc enlaza, no IDEAS
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador (AG-B23) la mida.
- **Sesgos posibles:** Cobertura dependiente de los archivos participantes; metadatos a veces incompletos
- **Cambios de propiedad o de metodología:** Sin cambios conocidos
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «SSRN NBER working papers RePEc IDEAS arXiv q-fin EconStor open access economics repositories»; WebFetch: sí, página índice https://www.marshall.econ.cam.ac.uk/onlineresources/economics-subject-repositories y https://guides.libraries.emory.edu/main/economics/working_papers; el sitio propio no se leyó)
- **Origen:** Reutilizada del Bloque A (ID original) en F9 Bloque B (TFB-18) el 2026-11-02.

## TFB-19 Ecosistema emprendedor: startups, financiación, salidas a bolsa y escisiones (datos)

#### MBF-0701 · Q 88 (A) — SEC — Form D Data Sets (avisos de ofertas exentas de Regulation D)

- **Canal oficial (URL raíz):** https://www.sec.gov/dera/data/form-d (ficha en el catálogo federal: https://catalog.data.gov/dataset/form-d-data-sets)
- **Emisor:** U.S. Securities and Exchange Commission (SEC), Division of Economic and Risk Analysis (DERA)
- **Documentación y notas:** Datos estructurados extraídos de la parte XML del Form D (avisos de ofertas exentas al amparo de las Rules 504, 506(b) y 506(c) de Regulation D y de la Sección 4(a)(5)); formato plano, un ZIP por trimestre «tal como se presentó»; actualización trimestral (lo presentado tras las 17:30 ET del último día hábil pasa al trimestre siguiente); la cabecera dice septiembre de 2009, aunque la lista de descargas llega a 2008 T1; definiciones de tablas en PDF aparte. Página revisada el 30/09/2026.
- **Temática:** TFB-19 Ecosistema emprendedor: startups, financiación, salidas a bolsa y escisiones (datos) (principal) · secundarias: TFB-03
- **Calidad Q:** 88 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria (registro regulatorio)
- **Acceso:** Abierto (descarga masiva sin registro)
- **Ámbitos:** Rondas privadas de empresas de EE. UU. y extranjeras que captan en EE. UU.: emisor, sector, importe ofrecido y vendido, número de inversores, exención usada, intermediarios y comisiones
- **Motivo de inclusión y uso:** Única fuente oficial y gratuita que registra de forma sistemática las rondas privadas (incluidas las de capital riesgo) en EE. UU.; permite contar rondas por sector y trimestre sin depender de bases comerciales.
- **Uso en el bloque:** AG-B10 Flujos y Sentimiento (flujo de capital privado hacia un subsector); AG-B04 Demanda y Adopción (intensidad de creación de empresas en una temática); AG-B12 Seleccionador de Activos (identificar competidores privados y futuros candidatos a salida a bolsa); Motor AG-B16 (series trimestrales de número e importe de rondas).
- **Restricciones de uso:** Datos públicos de la SEC; respetar la política de acceso de sec.gov (identificación en el User-Agent y límite de peticiones en descargas automatizadas).
- **Sesgos y cautelas:** Presentación a menudo tardía u omitida (la sanción es limitada); el importe es el de la oferta, no siempre el cierre; no incluye valoración; también lo usan fondos y vehículos inmobiliarios (filtrar por tipo de emisor); la SEC no garantiza la exactitud.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-03 (búsqueda web: «SEC Form D data sets structured data download»; WebFetch: sí)
- **Origen:** Alta F9 Bloque B, TFB-19 (2026-11-03).

#### MBF-0702 · Q 86 (A) — CORDIS — proyectos y resultados de la investigación financiada por la UE (FP1 a Horizonte Europa)

- **Canal oficial (URL raíz):** https://cordis.europa.eu/ (búsqueda de proyectos: https://www.cordis.europa.eu/projects; descripción para máquinas: https://cordis.europa.eu/llms.txt)
- **Emisor:** Comisión Europea (Oficina de Publicaciones de la UE), Community Research and Development Information Service
- **Documentación y notas:** Repositorio público de proyectos de los programas marco desde FP1 (1984) hasta Horizonte Europa (2021–2027): más de 150.000 proyectos (35.386 de Horizonte 2020 y 25.785 de FP7), con participantes, importes y resultados. Conjuntos masivos en data.europa.eu (CSV, JSON, XML, RDF), grafo EURIO con punto SPARQL y API REST de extracción (requiere EU Login).
- **Temática:** TFB-19 Ecosistema emprendedor: startups, financiación, salidas a bolsa y escisiones (datos) (principal) · secundarias: TFB-16, TFB-09
- **Calidad Q:** 86 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 14/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria (registro oficial de concesiones)
- **Acceso:** Abierto (CC BY 4.0 para el contenido editorial de la UE; la API de extracción exige cuenta EU Login gratuita)
- **Ámbitos:** Proyectos, consorcios y organizaciones beneficiarias (incluidas pymes y startups, también las del EIC), contribución de la UE, temática, entregables y publicaciones
- **Motivo de inclusión y uso:** Permite rastrear qué empresas privadas europeas reciben financiación pública de I+D en una tecnología y con quién colaboran; señal temprana de capacidades tecnológicas antes de que haya rondas o salidas a bolsa.
- **Uso en el bloque:** AG-B06 Tecnología (mapa de actores europeos por tecnología); AG-B05 Oferta y Cadena de Suministro (consorcios industriales); AG-B12 Seleccionador de Activos (cotizadas y no cotizadas con proyectos financiados); AG-B13 Prospectiva (temas emergentes por volumen de proyectos).
- **Restricciones de uso:** Atribución «European Union, CORDIS — CC BY 4.0»; los materiales aportados por beneficiarios siguen los términos de su acuerdo de subvención; las fichas contienen datos personales (Reglamento (UE) 2018/1725).
- **Sesgos y cautelas:** Mide financiación concedida, no éxito comercial; nombres de organizaciones no siempre normalizados; desfase entre firma del acuerdo y publicación.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-03 (búsqueda web: «CORDIS Horizon Europe projects open data search organisations»; WebFetch: sí, cordis.europa.eu/llms.txt)
- **Origen:** Alta F9 Bloque B, TFB-19 (2026-11-03).

#### MBF-0703 · Q 85 (A) — Consejo Europeo de Innovación (EIC) — EIC Accelerator: listas de empresas seleccionadas por convocatoria

- **Canal oficial (URL raíz):** https://eic.ec.europa.eu/ (ejemplo de anuncio con lista: https://eic.ec.europa.eu/news/38-start-ups-and-smes-secure-eic-support-latest-round-eic-accelerator-2026-06-15_en)
- **Emisor:** Comisión Europea — European Innovation Council (EIC) y EIC Fund
- **Documentación y notas:** Tras cada corte, el EIC publica una nota con el número de empresas, el reparto subvención/capital y un PDF «List of selected companies». Corte de enero–marzo de 2026 (nota del 15/06/2026): 38 startups y pymes de 87 entrevistadas; unos 90 M€ en subvenciones y 202 M€ reservados para posibles inversiones de capital (presupuesto estimado 292 M€); el 84 % recibe financiación mixta. Corte anterior: 61 empresas (nota del 17/02/2026).
- **Temática:** TFB-19 Ecosistema emprendedor: startups, financiación, salidas a bolsa y escisiones (datos) (principal) · secundarias: TFB-16
- **Calidad Q:** 85 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 13/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 9/10 · Acceso 9/10
- **Tipología:** primaria (resoluciones de financiación pública)
- **Acceso:** Abierto (notas y PDF de listas)
- **Ámbitos:** Startups y pymes europeas de tecnología profunda seleccionadas, país, tecnología, subvención y tramo de capital del EIC Fund
- **Motivo de inclusión y uso:** Filtro de calidad público sobre la tecnología profunda europea: las seleccionadas pasan una evaluación exigente y el EIC Fund suele atraer coinversión privada (la nota cita tres o más euros privados por cada euro del EIC).
- **Uso en el bloque:** AG-B06 Tecnología (qué tecnologías profundas financia la UE); AG-B07 Regulación y Geopolítica (política industrial y soberanía tecnológica); AG-B12 Seleccionador de Activos (canteras de futuras salidas a bolsa y objetivos de adquisición de cotizadas); AG-B13 Prospectiva.
- **Restricciones de uso:** Aviso legal de europa.eu (reutilización autorizada con cita de la fuente).
- **Sesgos y cautelas:** Selección orientada a objetivos de política pública; el tramo de capital es «reservado» y puede no ejecutarse; listas en PDF sin formato estructurado.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Cambios periódicos de reglas de convocatoria en el programa de trabajo anual del EIC.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-03 (búsqueda web: «EIC Accelerator funded companies list beneficiaries European Innovation Council»; WebFetch: sí)
- **Origen:** Alta F9 Bloque B, TFB-19 (2026-11-03).

#### MBF-0706 · Q 84 (A) — Jay R. Ritter (University of Florida) — Initial Public Offerings: Updated Statistics

- **Canal oficial (URL raíz):** https://site.warrington.ufl.edu/ritter/files/IPO-Statistics.pdf (página del autor: https://site.warrington.ufl.edu/ritter/?p=106)
- **Emisor:** Jay R. Ritter, Eugene F. Brigham Department of Finance, Insurance, and Real Estate, Warrington College of Business, University of Florida
- **Documentación y notas:** Compendio en PDF actualizado periódicamente (última actualización vista: 05/10/2026; cada tabla con su fecha, p. ej. Tabla 1 del 13/07/2026): número de salidas a bolsa, rentabilidad del primer día y «dinero dejado sobre la mesa» desde 1980 (Tabla 8 desde 1960), salidas respaldadas por capital riesgo y por fondos de compra, tecnológicas frente a ciencias de la vida, precio/ventas, rentabilidades a largo plazo y clase dual. Filtros explícitos: precio de oferta ≥ 5 USD; excluye ADR, unidades, SPAC, fondos cerrados, REIT, bancos y ofertas pequeñas a mejor esfuerzo. Recuento 2025: 90 salidas de empresas operativas (67 de EE. UU.).
- **Temática:** TFB-19 Ecosistema emprendedor: startups, financiación, salidas a bolsa y escisiones (datos) (principal) · secundarias: TFB-18
- **Calidad Q:** 84 (A) — Primariedad 16/20 · Historial 10/20 · Transparencia 15/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 8/10 · Acceso 10/10
- **Tipología:** secundaria académica (elaboración propia; filtros sobre empresas listadas en CRSP)
- **Acceso:** Abierto (PDF sin registro)
- **Ámbitos:** Ciclo de salidas a bolsa en EE. UU., infravaloración inicial, edad y ventas de las empresas, respaldo de capital riesgo, rentabilidad a largo plazo
- **Motivo de inclusión y uso:** Referencia académica estándar y gratuita para medir si la ventana de salidas a bolsa está «caliente» o «fría» y comparar la valoración de nuevas cotizadas con la historia.
- **Uso en el bloque:** AG-B10 Flujos y Sentimiento (temperatura del mercado de salidas a bolsa); AG-B09 Finanzas y Valoración (precio/ventas de salidas tecnológicas frente a la historia); AG-B14 Contrarias (rentabilidad a largo plazo inferior de las salidas en olas calientes); Motor AG-B16 (series anuales para el módulo de ciclo).
- **Restricciones de uso:** Material académico de libre consulta; citar autor y fecha de la tabla.
- **Sesgos y cautelas:** Definición estrecha de salida a bolsa (cifras inferiores a las de otras fuentes); solo EE. UU.; tablas con fechas de actualización distintas.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-03 (búsqueda web: «Jay Ritter IPO statistics data University of Florida initial public offerings updated»; WebFetch: sí)
- **Origen:** Alta F9 Bloque B, TFB-19 (2026-11-03).

#### MBF-0704 · Q 83 (A) — SBIR.gov — base de adjudicaciones SBIR/STTR y API de empresas (EE. UU.)

- **Canal oficial (URL raíz):** https://www.sbir.gov/awards (recursos de datos: https://www.sbir.gov/api/company)
- **Emisor:** U.S. Small Business Administration (SBA), programas Small Business Innovation Research (SBIR) y Small Business Technology Transfer (STTR)
- **Documentación y notas:** Buscador de adjudicaciones de las agencias federales participantes y APIs de adjudicaciones, empresas y convocatorias con diccionario de datos. La API de empresas busca por palabra clave, nombre o UEI y devuelve, entre otros, número de adjudicaciones, UEI y marcas de propiedad (mujer, HUBZone); JSON por defecto o XML, hasta 5.000 filas por llamada. En la fecha de verificación la página advertía de que las APIs estaban «en mantenimiento».
- **Temática:** TFB-19 Ecosistema emprendedor: startups, financiación, salidas a bolsa y escisiones (datos) (principal) · secundarias: TFB-16
- **Calidad Q:** 83 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 8/10 · Acceso 9/10
- **Tipología:** primaria (registro oficial de adjudicaciones)
- **Acceso:** Abierto (sin registro; API pública)
- **Ámbitos:** Adjudicaciones de fase I/II/III por agencia, tema, empresa, estado y año; convocatorias abiertas
- **Motivo de inclusión y uso:** Mayor programa público de financiación no dilutiva a pequeñas empresas tecnológicas de EE. UU.; al reunir las adjudicaciones de todas las agencias participantes, cubre también las SBIR de la NSF sin ficha aparte.
- **Uso en el bloque:** AG-B06 Tecnología (temas que financian defensa, salud y energía); AG-B07 (prioridades de política industrial de EE. UU.); AG-B12 Seleccionador de Activos (proveedores emergentes de contratistas cotizados); Motor AG-B16 (series por agencia y tema).
- **Restricciones de uso:** Datos públicos federales; las APIs pueden estar temporalmente fuera de servicio.
- **Sesgos y cautelas:** Calidad desigual de los campos según la agencia que reporta; importes concedidos, no desembolsados (contrastar con USAspending, MBF-0403).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Reautorización periódica de los programas por el Congreso; mantenimiento de APIs anunciado en 2026.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-03 (búsqueda web: «SBIR.gov awards database API search SBIR STTR»; WebFetch: sí, página de recursos de datos)
- **Origen:** Alta F9 Bloque B, TFB-19 (2026-11-03).

#### MBF-0707 · Q 81 (A) — SEC EDGAR — seguimiento de registros de salida a bolsa (S-1, F-1, S-1/A, 424B) y de escisiones (Form 10) por tipo de formulario

- **Canal oficial (URL raíz):** https://www.sec.gov/edgar/search/ (búsqueda de texto completo; consulta por formulario, p. ej. https://efts.sec.gov/LATEST/search-index?q=%22S-1%22&dateRange=custom&startdt=2026-01-01&enddt=2026-12-31&forms=S-1; listado de últimos registros por tipo: https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&type=S-1&dateb=&owner=include&count=40&search_text=&action=getcompany), según la guía índice https://pagecrawl.io/blog/ipo-monitoring-sec-s1-filing-alerts
- **Emisor:** U.S. Securities and Exchange Commission (SEC)
- **Documentación y notas:** Uso específico de EDGAR (ficha general: RF-0002) para el ciclo de salidas a bolsa y escisiones: filtrar por tipo de formulario S-1 y F-1 (emisores extranjeros), sus enmiendas (S-1/A), folletos definitivos 424B (p. ej. 424B4, que fija precio) y Form 10 (registro bajo la Exchange Act que usan las escisiones), con rango de fechas y por CIK de empresa.
- **Temática:** TFB-19 Ecosistema emprendedor: startups, financiación, salidas a bolsa y escisiones (datos) (principal) · secundarias: TFB-03
- **Calidad Q:** 81 (A) — Primariedad 20/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 15/15 · Independencia 10/10 · Actualidad 10/10 · Acceso 5/10
- **Tipología:** primaria (documentos de registro presentados por los emisores)
- **Acceso:** Abierto; la consulta masiva exige respetar la política de acceso de sec.gov (User-Agent identificado, límite de peticiones)
- **Ámbitos:** Cartera de futuras salidas a bolsa (incluidas las presentadas en confidencial cuando se hacen públicas), métricas financieras previas a la cotización, factores de riesgo, uso de fondos, estructura de clase dual; documentos de escisión con estados financieros de la filial
- **Motivo de inclusión y uso:** La fuente original de toda salida a bolsa y escisión en EE. UU.; los calendarios comerciales derivan de ella. Permite leer las cifras de la empresa antes de que cotice.
- **Uso en el bloque:** AG-B12 Seleccionador de Activos (nuevas cotizadas y filiales escindidas como candidatas para el Bloque C); AG-B09 Finanzas y Valoración (múltiplos de salida frente a cotizadas comparables); AG-B03 Estructura y Competencia (datos de mercado y competidores declarados en el folleto); AG-B10 (volumen de registros como indicador de ventana).
- **Restricciones de uso:** Datos públicos; sin API específica para estos formularios fuera de las de EDGAR (MBF-0201).
- **Sesgos y cautelas:** Muchas empresas registran primero en confidencial (la cartera visible está incompleta); un S-1 no garantiza la salida (retiradas frecuentes); el Acceso se puntúa bajo por la necesidad de construir consultas propias.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-03 (búsqueda web: «SEC Form 10 spin-off registration statement EDGAR S-1 F-1 IPO filings full-text search»; WebFetch: sí, sobre la guía índice de PageCrawl, que da las URL de EDGAR; las páginas de sec.gov no se leyeron)
- **Origen:** Alta F9 Bloque B, TFB-19 (2026-11-03).

#### MBF-0709 · Q 80 (A) — BME Growth (BME, SIX) — mercado de empresas en expansión: listado de cotizadas, información de emisores y requisitos

- **Canal oficial (URL raíz):** https://www.bolsasymercados.es/en/bme-growth/listing.html (presentación institucional: https://www.bolsasymercados.es/dam/descargas/bme-growth/presentacion-bme-growth-es.pdf)
- **Emisor:** BME Growth (Bolsas y Mercados Españoles, grupo SIX); antiguo Mercado Alternativo Bursátil (MAB)
- **Documentación y notas:** Mercado para pymes en crecimiento (la mayoría con capitalización inferior a 200 M€). Requisitos de admisión: sociedad anónima, al menos 2 M€ en manos de accionistas con menos del 5 % y 20 accionistas independientes; información semestral y anual a través de un Asesor Registrado; Documento Informativo de Incorporación o folleto de la CNMV; proveedor de liquidez. Publica precios, índices IBEX Growth Market 15 y All Share, información privilegiada y otra información relevante de cada emisor, operaciones corporativas y boletín diario.
- **Temática:** TFB-19 Ecosistema emprendedor: startups, financiación, salidas a bolsa y escisiones (datos) (principal) · secundarias: TFB-03, TFB-02
- **Calidad Q:** 80 (A) — Primariedad 19/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 14/15 · Independencia 8/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria (operador del mercado)
- **Acceso:** Abierto (precios con retardo e información de emisores)
- **Ámbitos:** Incorporaciones y exclusiones, ampliaciones de capital, documentos de incorporación, hechos relevantes de pymes españolas y SOCIMI
- **Motivo de inclusión y uso:** Principal vía de salida a bolsa de pymes en España; base para cribar pequeñas cotizadas españolas en crecimiento.
- **Uso en el bloque:** AG-B12 Seleccionador de Activos (pequeñas cotizadas españolas candidatas, con sus documentos de incorporación); AG-B10 (flujo de nuevas incorporaciones); AG-B03 (estructura de subsectores con cotizadas pequeñas).
- **Restricciones de uso:** Condiciones de BME para datos de mercado (tiempo real y redistribución bajo licencia).
- **Sesgos y cautelas:** Baja liquidez y cobertura de análisis escasa; varias SOCIMI y empresas con concursos (riesgo de selección adversa); requisitos menos exigentes que el mercado principal.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** BME es filial de SIX Group desde 2020; MAB renombrado BME Growth.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-03 (búsqueda web: «BME Growth empresas cotizadas listado Euronext Growth admissions list»; WebFetch: sí, página de listing; la presentación en PDF redirigió y no se leyó)
- **Origen:** Alta F9 Bloque B, TFB-19 (2026-11-03).

#### MBF-0710 · Q 79 (B) — Euronext — balance anual de admisiones y Euronext Growth (salidas a bolsa en la mayor red de bolsas de la UE)

- **Canal oficial (URL raíz):** https://www.euronext.com/en/investor-relations/financial-information/news/2025-euronext-strengthened-its-position-leading (marco de admisión 2026: https://www.euronext.com/en/news/euronext-introduces-new-admission-framework)
- **Emisor:** Euronext N.V. (bolsas de Ámsterdam, Bruselas, Dublín, Lisboa, Milán, Oslo y París)
- **Documentación y notas:** Nota del 22/12/2025: 76 admisiones en 2025 (50 nuevas cotizaciones de acciones, casi un tercio de las de Europa, con 17.000 M€ de capitalización agregada), más de 15.000 M€ en ampliaciones de 200 cotizadas, más de 14.500 bonos nuevos; Euronext Growth supera las 500 pymes en seis plazas y cumplió 20 años. En junio de 2026, con la entrada en aplicación de la Listing Act de la UE, Euronext lanzó un nuevo marco de admisión e IPOgo, vía rápida de salida a bolsa para pymes.
- **Temática:** TFB-19 Ecosistema emprendedor: startups, financiación, salidas a bolsa y escisiones (datos) (principal) · secundarias: TFB-03
- **Calidad Q:** 79 (B) — Primariedad 18/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 14/15 · Independencia 7/10 · Actualidad 9/10 · Acceso 10/10
- **Tipología:** primaria (operador del mercado)
- **Acceso:** Abierto
- **Ámbitos:** Número de salidas a bolsa y admisiones por plaza y segmento (Euronext Growth, Euronext Access), capital captado, ampliaciones, reformas de las normas de admisión
- **Motivo de inclusión y uso:** Fuente original del ritmo de salidas a bolsa en la Europa continental y de las reformas que facilitan la cotización de pymes.
- **Uso en el bloque:** AG-B10 Flujos y Sentimiento (ventana de salidas a bolsa en Europa); AG-B07 Regulación y Geopolítica (Listing Act y nuevas vías de admisión); AG-B12 Seleccionador de Activos (nuevas cotizadas europeas).
- **Restricciones de uso:** Notas de prensa de libre uso con cita; datos de mercado en tiempo real bajo licencia.
- **Sesgos y cautelas:** Comunicado comercial del propio operador (incentivo a presentar cifras favorables); cifras provisionales a fecha de la nota; el recuento de admisiones mezcla traslados y cotizaciones técnicas.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Nuevo marco de admisión en 2026 (Listing Act).
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-03 (búsqueda web: «Euronext IPO listings list new admissions Euronext Growth ESMA prospectus register»; WebFetch: sí, nota del 22/12/2025)
- **Origen:** Alta F9 Bloque B, TFB-19 (2026-11-03).

#### MBF-0711 · Q 79 (B) — CDTI — programa Neotec y financiación pública a empresas de base tecnológica (España)

- **Canal oficial (URL raíz):** https://www.cdti.es/en/node/19726 (nota «Public funding opportunities in 2024 for startups and EBTs»; sección de transparencia «Proyectos aprobados» enlazada desde el sitio)
- **Emisor:** Centro para el Desarrollo Tecnológico y la Innovación (CDTI), E.P.E., Ministerio de Ciencia, Innovación y Universidades
- **Documentación y notas:** Neotec apoya a empresas de base tecnológica (EBT) cuyo negocio se basa en tecnología y conocimiento procedente de la investigación (excluye las de servicios a terceros sin desarrollo tecnológico); nació en 2002 con ayudas parcialmente reembolsables de hasta 1 M€ y desde 2014 es subvención; convocatoria anual, con fondos del Mecanismo de Recuperación y Resiliencia. El CDTI gestiona también Innvierte (capital riesgo público). La nota leída es del 06/03/2024.
- **Temática:** TFB-19 Ecosistema emprendedor: startups, financiación, salidas a bolsa y escisiones (datos) (principal) · secundarias: TFB-16
- **Calidad Q:** 79 (B) — Primariedad 19/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 15/15 · Independencia 9/10 · Actualidad 7/10 · Acceso 8/10
- **Tipología:** primaria (organismo concedente)
- **Acceso:** Abierto
- **Ámbitos:** Ayudas a startups tecnológicas españolas, proyectos aprobados, inversión pública en capital riesgo (Innvierte)
- **Motivo de inclusión y uso:** Principal financiador público de startups tecnológicas en España; sus resoluciones identifican empresas tecnológicas jóvenes con validación técnica.
- **Uso en el bloque:** AG-B06 Tecnología (tecnologías emergentes financiadas en España); AG-B07 (política industrial española); AG-B12 Seleccionador de Activos (futuras candidatas a BME Growth, MBF-0709); contraste con la BDNS (MBF-0411).
- **Restricciones de uso:** Aviso legal del CDTI; la página leída no describe el formato de la lista de proyectos aprobados.
- **Sesgos y cautelas:** Concesión no implica éxito comercial; dependencia de fondos europeos temporales (MRR); información dispersa entre notas, convocatorias y transparencia.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Neotec pasó de ayuda reembolsable a subvención en 2014.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-03 (búsqueda web: «enisa.es informe actividad préstamos participativos CDTI Neotec resolución startups datos»; WebFetch: sí)
- **Origen:** Alta F9 Bloque B, TFB-19 (2026-11-03).

#### MBF-0705 · Q 75 (B) — Startup Genome — Global Startup Ecosystem Report (GSER)

- **Canal oficial (URL raíz):** https://startupgenome.com/ (edición 2025: https://startupgenome.com/report/gser2025/introduction)
- **Emisor:** Startup Genome (con Global Entrepreneurship Network como socio habitual)
- **Documentación y notas:** Informe anual (14 años en publicación) que clasifica ecosistemas emprendedores; la página cita más de 350 ecosistemas analizados y 5,5 millones de empresas estudiadas. La edición 2025 se presentó en VivaTech (París, 12/06/2025) con caída del valor global de ecosistemas; la de 2026 («Now Live») señala que el valor de los ecosistemas subió 2,8 billones USD, dos tercios en tres ciudades de EE. UU., por la IA.
- **Temática:** TFB-19 Ecosistema emprendedor: startups, financiación, salidas a bolsa y escisiones (datos) (principal) · secundarias: TFB-09
- **Calidad Q:** 75 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 13/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** secundaria (índice compuesto con datos propios y de terceros)
- **Acceso:** Abierto (lectura web del informe)
- **Ámbitos:** Clasificación de ecosistemas por rendimiento, financiación, talento, conectividad y conocimiento; ecosistemas emergentes; subsectores (IA, tecnología climática, biotecnología)
- **Motivo de inclusión y uso:** Comparación entre ciudades y países de la profundidad del ecosistema emprendedor; útil para mercados geográficos.
- **Uso en el bloque:** AG-B08 Macro y Ciclo y AG-B04 Demanda y Adopción (dinamismo emprendedor de un mercado geográfico); AG-B06 Tecnología (concentración de subsectores); AG-B13 Prospectiva.
- **Restricciones de uso:** Condiciones del sitio; citar edición.
- **Sesgos y cautelas:** Patrocinado por agencias públicas de ecosistemas que figuran en el informe; metodología no detallada en la página leída; «valor del ecosistema» depende de valoraciones privadas.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Cambios de método entre ediciones.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-03 (búsqueda web: «Startup Genome Global Startup Ecosystem Report 2025»; WebFetch: sí)
- **Origen:** Alta F9 Bloque B, TFB-19 (2026-11-03).

#### MBF-0708 · Q 75 (B) — Renaissance Capital — IPO Center (calendario, cartera de registros, precios y estadísticas de salidas a bolsa en EE. UU.)

- **Canal oficial (URL raíz):** https://renaissancecapital.com/IPO-Center/Calendar
- **Emisor:** Renaissance Capital (también gestor de ETF de salidas a bolsa de EE. UU. e internacionales)
- **Documentación y notas:** Calendario de salidas a bolsa de la semana con calendarios separados de NYSE y Nasdaq, actualizado a diario; páginas de precios (Pricings), cartera de registros (IPO Pipeline), estadísticas (IPO Stats), índices, sectores y noticias semanales («US IPO Week Ahead», «US IPO Weekly Recap»). La fecha de negociación y el análisis detallado se reservan a IPO Pro (prueba gratuita); hay IPO Intelligence y APIs de pago.
- **Temática:** TFB-19 Ecosistema emprendedor: startups, financiación, salidas a bolsa y escisiones (datos) (principal) · secundarias: TFB-15
- **Calidad Q:** 75 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 12/15 · Autoridad 14/15 · Independencia 6/10 · Actualidad 10/10 · Acceso 8/10
- **Tipología:** secundaria (agregación y análisis de registros de la SEC y de bolsas)
- **Acceso:** Muro parcial (calendario, noticias y estadísticas básicas abiertas; IPO Pro, Intelligence y API de pago)
- **Ámbitos:** Salidas a bolsa previstas y realizadas en EE. UU. (incluidas SPAC), tamaño, colocadores, sector, rentabilidad tras la salida
- **Motivo de inclusión y uso:** Calendario de referencia del sector, que cubre en una sola página los calendarios de NYSE y Nasdaq pedidos en el encargo.
- **Uso en el bloque:** AG-B10 Flujos y Sentimiento (actividad semanal de salidas a bolsa como termómetro del apetito por riesgo); AG-B12 Seleccionador de Activos (nuevas cotizadas por sector); AG-B13 Prospectiva (cartera de registros).
- **Restricciones de uso:** Condiciones del sitio; datos completos y API de pago (futuro).
- **Sesgos y cautelas:** Gestora de ETF de salidas a bolsa (interés en un mercado activo, independencia 6/10); cifras propias con definiciones distintas de las de Ritter (MBF-0706).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-03 (búsquedas web: «Renaissance Capital IPO calendar priced upcoming IPOs pricing data» y «Nasdaq IPO calendar NYSE IPO center upcoming listings»; WebFetch: sí)
- **Origen:** Alta F9 Bloque B, TFB-19 (2026-11-03).

#### MBF-0713 · Q 72 (B) — ARPA-E (Departamento de Energía de EE. UU.) — buscador de proyectos financiados

- **Canal oficial (URL raíz):** https://arpa-e.energy.gov/?q=projects%2Fsearch-projects&field_program_tid=All&field_project_state_value=All&term_node_tid_depth=All&page=12 (según la ficha del catálogo de datos https://data.amerigeoss.org/en/dataset/arpa-e-projects; informe anual FY2022: https://arpa-e.energy.gov/sites/default/files/2025-07/EXEC-2022-008205%20-%20ARPA-E%20FY%202022%20Annual%20Report_PDF.pdf)
- **Emisor:** Advanced Research Projects Agency–Energy (ARPA-E), U.S. Department of Energy
- **Documentación y notas:** Buscador de proyectos por programa, estado y tecnología, con adjudicatario (empresas, universidades, laboratorios), importe y descripción. La ficha del catálogo federal (licencia CC BY 4.0) cubre 2005–2014 y no se actualiza desde 2014; el buscador del sitio es la fuente viva.
- **Temática:** TFB-19 Ecosistema emprendedor: startups, financiación, salidas a bolsa y escisiones (datos) (principal) · secundarias: TFB-16, TFB-12
- **Calidad Q:** 72 (B) — Primariedad 18/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 14/15 · Independencia 9/10 · Actualidad 5/10 · Acceso 7/10
- **Tipología:** primaria (agencia concedente)
- **Acceso:** Abierto
- **Ámbitos:** Proyectos de tecnología energética en fase temprana (almacenamiento, redes, nuclear avanzada, captura de carbono), adjudicatarios y seguimiento
- **Motivo de inclusión y uso:** Financiación pública de alto riesgo en energía que precede a muchas startups de tecnología climática; señal temprana de tecnologías que pueden llegar a mercado.
- **Uso en el bloque:** AG-B06 Tecnología (frontera tecnológica en energía); AG-B13 Prospectiva; AG-B11 Sostenibilidad y Riesgos (soluciones de descarbonización emergentes).
- **Restricciones de uso:** Datos públicos federales; la ficha de catálogo usa CC BY 4.0.
- **Sesgos y cautelas:** Conjunto del catálogo desactualizado; la URL del buscador procede del catálogo y no se cargó; financiación sujeta a vaivenes presupuestarios.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-03 (búsqueda web: «ARPA-E projects database awardees»; WebFetch: sí, ficha del catálogo AmeriGEOSS; el sitio de ARPA-E no se leyó)
- **Origen:** Alta F9 Bloque B, TFB-19 (2026-11-03).

#### MBF-0714 · Q 72 (B) — Dealroom.co — base de datos de startups, rondas y ecosistemas (foco europeo)

- **Canal oficial (URL raíz):** https://dealroom.co/products/global-data-platform (descripción: https://knowledge.dealroom.co/knowledge/what-is-dealroom.co; precios: https://content.dealroom.co/pricing)
- **Emisor:** Dealroom.co
- **Documentación y notas:** Perfiles de empresas (sector, modelo de negocio, fecha de fundación, plantilla, fase, valoración, accionistas), rondas y ubicación, y señales de crecimiento (evolución de plantilla, visitas web mensuales, descargas de apps), con grupos de comparables. Las startups y fundadores tienen cuenta gratuita con acceso a la base de inversores; el acceso de inversores es de pago. Mantiene paneles de ecosistema para gobiernos y agencias (muchos públicos) e colaboraciones con medios (p. ej., tech.eu Radar, «powered by Dealroom»).
- **Temática:** TFB-19 Ecosistema emprendedor: startups, financiación, salidas a bolsa y escisiones (datos) (principal) · secundarias: TFB-09
- **Calidad Q:** 72 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 13/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 8/10
- **Tipología:** secundaria (agregación de fuentes públicas, datos aportados y algoritmos)
- **Acceso:** Muro parcial (cuenta gratuita limitada y paneles públicos de ecosistemas; plataforma completa y API de pago, futuro)
- **Ámbitos:** Startups y scaleups europeas y mundiales, rondas, inversores, valoraciones, unicornios, señales de tracción
- **Motivo de inclusión y uso:** Referencia de datos sobre el ecosistema tecnológico europeo; los paneles públicos de ecosistemas cubren regiones y ciudades sin coste.
- **Uso en el bloque:** AG-B04 Demanda y Adopción (tracción de startups en una temática); AG-B03 Estructura y Competencia (entrantes financiados que amenazan a cotizadas); AG-B10 (flujo de capital riesgo europeo); AG-B12 (comparables privados).
- **Restricciones de uso:** Cuenta gratuita con registro; reutilización masiva sujeta a licencia.
- **Sesgos y cautelas:** Cobertura y calidad desiguales fuera de Europa; valoraciones estimadas; la página leída no describe el método de captura ni de verificación.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-03 (búsqueda web: «Dealroom.co free access startup ecosystem data European tech»; WebFetch: sí, knowledge.dealroom.co)
- **Origen:** Alta F9 Bloque B, TFB-19 (2026-11-03).

#### RF-0453 · Q 71 (B) — Carta — State of Private Markets

- **Canal oficial (URL raíz):** https://carta.com/data/
- **Emisor:** Carta (plataforma de gestión de participaciones de empresas no cotizadas)
- **Temática:** TFB-19 Ecosistema emprendedor: startups, financiación, salidas a bolsa y escisiones (datos) (principal) · secundarias: TFB-11
- **Calidad Q:** 71 (B) — Primariedad 16/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 12/15 · Independencia 7/10 · Actualidad 9/10 · Acceso 8/10
- **Tipología:** primaria (datos agregados y anonimizados de la propia plataforma)
- **Acceso:** Abierto (informe trimestral y libro de datos descargable)
- **Ámbitos:** Rondas de financiación, valoraciones medianas y tamaño de ronda de startups de EE. UU. por fase
- **Motivo de inclusión y uso:** Datos de financiación de startups de una plataforma con cobertura amplia; contraste de RF-0079. AC-AL, AC-TEC.
- **Uso en el bloque:** AG-B09 Finanzas y Valoración (valoraciones previas a la ronda por fase, rondas a la baja); AG-B10 (ritmo de rondas); AG-B04 (sectores con más rondas); contraste de Form D (MBF-0701).
- **Restricciones de uso:** Uso con cita; libro de datos descargable.
- **Sesgos y cautelas:** Muestra limitada a clientes de Carta; la página leída no publica método, muestra ni definiciones.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-02 (búsqueda web: «Carta State of Private Markets report startup data»; WebFetch: sí)
- **Origen:** Alta F9_S3, tanda 3 (2026-11-02). Reutilizada en F9 Bloque B, TFB-19 (2026-11-03).

#### MBF-0715 · Q 70 (B) — KPMG Private Enterprise — Venture Pulse (informe trimestral de capital riesgo mundial)

- **Canal oficial (URL raíz):** https://kpmg.com/at/de/insights/2026/10/q3-26-kpmg-venture-pulse-report.html (ediciones previas: https://kpmg.com/at/de/insights/2026/08/q2-26-kpmg-venture-pulse-report.html, https://kpmg.com/at/de/insights/2026/04/q1-26-kpmg-venture-pulse-report.html)
- **Emisor:** KPMG Private Enterprise (red KPMG; página de KPMG Austria)
- **Documentación y notas:** Informe trimestral gratuito con análisis mundial y por regiones de la inversión en capital riesgo; la edición del T3 2026 sitúa la inversión en Europa en 28.400 M USD (26.500 M el trimestre anterior) en 1.497 operaciones; PDF descargable. Hermano del «Pulse of Private Equity» (https://assets.kpmg.com/content/dam/kpmgsites/xx/pdf/2026/10/kpmg-pe-pulse-q3-2026.pdf).
- **Temática:** TFB-19 Ecosistema emprendedor: startups, financiación, salidas a bolsa y escisiones (datos) (principal) · secundarias: TFB-11
- **Calidad Q:** 70 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 13/15 · Independencia 7/10 · Actualidad 10/10 · Acceso 9/10
- **Tipología:** secundaria (análisis sobre base de datos de terceros)
- **Acceso:** Abierto (PDF)
- **Ámbitos:** Inversión de capital riesgo por región, fase y sector; salidas (a bolsa, adquisiciones); tendencias (IA, defensa, tecnología climática)
- **Motivo de inclusión y uso:** Lectura trimestral gratuita y comparable del ciclo de capital riesgo global y regional, publicada pocas semanas después del cierre del trimestre.
- **Uso en el bloque:** AG-B10 Flujos y Sentimiento (flujo de capital riesgo por sector); AG-B08 Macro y Ciclo (ciclo de financiación privada); AG-B13 Prospectiva (sectores que concentran la inversión).
- **Restricciones de uso:** Copyright de KPMG; citar edición.
- **Sesgos y cautelas:** La página leída no nombra el proveedor de datos (comprobar en el PDF); cifras revisables; la fecha de evento de la página (19-10-2025) contradice la URL de 2026; consultora con clientes en el sector.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-03 (búsqueda web: «KPMG Venture Pulse Q3 2026 Invest Europe Investing in Europe private equity activity report»; WebFetch: sí)
- **Origen:** Alta F9 Bloque B, TFB-19 (2026-11-03).

#### MBF-0718 · Q 70 (B) — Invest Europe — Investing in Europe: Private Equity Activity (estadísticas anuales de capital riesgo y capital privado europeos)

- **Canal oficial (URL raíz):** https://tech.eu/2026/05/07/investing-in-europe-private-equity-activity-2025-report-highlights-strong-fundraising-and-investment-performance/ (reseña de la edición 2025; edición 2024 reseñada por SECA: https://www.seca.ch/en/knowledge-library/newsletters/2025/seca-enewsletter-no-550/private-equity-int-news/investing-in-europe-private-equity-activity-2024/)
- **Emisor:** Invest Europe (asociación europea de capital privado y capital riesgo)
- **Documentación y notas:** Informe anual sobre la actividad del capital privado en Europa (la edición con datos de 2025, reseñada por tech.eu el 07/05/2026, destaca una captación y una inversión sólidas; la de 2024 fue reseñada por la asociación suiza SECA). Cubre captación, inversión y desinversión, con el capital riesgo como segmento; el detalle por fase, país y vía de salida debe comprobarse en el informe original, que no se leyó.
- **Temática:** TFB-19 Ecosistema emprendedor: startups, financiación, salidas a bolsa y escisiones (datos) (principal) · secundarias: TFB-11
- **Calidad Q:** 70 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 10/15 · Autoridad 14/15 · Independencia 6/10 · Actualidad 7/10 · Acceso 8/10
- **Tipología:** secundaria (estadística sectorial de la asociación)
- **Acceso:** Abierto (informe descargable; la URL oficial no apareció en los resultados)
- **Ámbitos:** Capital riesgo y capital privado europeos: captación, inversión por fase y país, desinversiones por vía de salida
- **Motivo de inclusión y uso:** Estadística paneuropea de referencia sobre el capital riesgo por país, comparable año a año; contraparte europea de la NVCA.
- **Uso en el bloque:** AG-B10 (flujo de capital riesgo hacia un país o sector europeo); AG-B08 Macro y Ciclo (profundidad del mercado de capital privado por país); AG-B12 (vías de salida: frecuencia de salidas a bolsa frente a ventas).
- **Restricciones de uso:** Copyright de Invest Europe; citar edición.
- **Sesgos y cautelas:** Asociación del sector (incentivo a presentar cifras favorables, independencia 6/10); datos autodeclarados; verificado solo a través de reseñas.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-03 (búsqueda web: «KPMG Venture Pulse Q3 2026 Invest Europe Investing in Europe private equity activity report»; WebFetch: no)
- **Origen:** Alta F9 Bloque B, TFB-19 (2026-11-03).

#### MBF-0716 · Q 68 (B) — Crunchbase — base de datos de empresas, rondas e inversores (plan gratuito)

- **Canal oficial (URL raíz):** https://www.crunchbase.com/ (según la página índice https://prospeo.io/s/what-is-crunchbase; integración documentada: https://posthog.com/docs/cdp/sources/crunchbase)
- **Emisor:** Crunchbase, Inc. (nacida en 2007 como proyecto de TechCrunch; independiente desde 2015)
- **Documentación y notas:** Plan Free (0 USD): búsqueda básica y vistas limitadas de perfiles, sin exportación ni alertas (útil para consultar el historial de rondas de una empresa); Pro desde 49 USD/mes (anual) con 2.000 filas de exportación al mes; Business 199 USD/mes; Enterprise con API (200 llamadas/min). Fuentes declaradas: perfiles autodeclarados por fundadores e inversores, actividad de más de 80 millones de usuarios, registros oficiales, socios de datos, web y modelos de IA con supervisión humana. Varios medios de 2026 señalan la retirada de la antigua API gratuita.
- **Temática:** TFB-19 Ecosistema emprendedor: startups, financiación, salidas a bolsa y escisiones (datos) (principal)
- **Calidad Q:** 68 (B) — Primariedad 12/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 13/15 · Independencia 8/10 · Actualidad 9/10 · Acceso 7/10
- **Tipología:** secundaria (agregación con datos colaborativos)
- **Acceso:** Muro parcial (plan gratuito con registro; exportación y API de pago, futuro)
- **Ámbitos:** Perfiles de empresas privadas y cotizadas, rondas, inversores, adquisiciones, salidas a bolsa, plantilla
- **Motivo de inclusión y uso:** Directorio más extendido para consultar rondas e inversores de una startup concreta; contraste rápido de datos de Form D (MBF-0701) y Dealroom (MBF-0714).
- **Uso en el bloque:** AG-B03 Estructura y Competencia (competidores privados financiados); AG-B12 Seleccionador de Activos (historial de financiación de nuevas cotizadas); AG-B10 (rondas recientes en un subsector).
- **Restricciones de uso:** Registro gratuito; términos de uso prohíben la extracción masiva; sin API gratuita.
- **Sesgos y cautelas:** Datos autodeclarados de calidad variable; las rondas pueden aparecer con 1–3 meses de retraso; la página índice es de un competidor (posible sesgo).
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Planes de pago desde 2016; API gratuita retirada (según medios, 2026).
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-03 (búsqueda web: «Crunchbase free plan basic API access startup funding data»; WebFetch: sí, página índice de Prospeo; crunchbase.com no se leyó)
- **Origen:** Alta F9 Bloque B, TFB-19 (2026-11-03).

#### MBF-0717 · Q 67 (B) — CB Insights — State of Venture (informe trimestral y anual de capital riesgo)

- **Canal oficial (URL raíz):** https://www.cbinsights.com/research/ (resultados: «State of Venture Q3'25 Report», https://www.cbinsights.com/research/insurtech/page/2; «The State of Venture: 2025 in review and what's next in 2026», https://www.cbinsights.com/research/events/past/page/11; compendio «257 pages of venture data», https://research.cbinsights.com/257-pages-of-venture-data)
- **Emisor:** CB Insights
- **Documentación y notas:** Informe trimestral y balance anual del capital riesgo mundial (financiación, número de operaciones, megarrondas, unicornios, salidas, por región y sector), presentado en seminario web y descargable (el acceso habitual pide registro; comprobar); la última edición citada en resultados es la del T1 2026. Publica además listas temáticas (Fintech 100, Digital Health 50, con seminarios en noviembre de 2026).
- **Temática:** TFB-19 Ecosistema emprendedor: startups, financiación, salidas a bolsa y escisiones (datos) (principal) · secundarias: TFB-11
- **Calidad Q:** 67 (B) — Primariedad 13/20 · Historial 10/20 · Transparencia 8/15 · Autoridad 13/15 · Independencia 8/10 · Actualidad 9/10 · Acceso 6/10
- **Tipología:** secundaria (base de datos propia)
- **Acceso:** Muro parcial (informes públicos con registro; plataforma de pago, futuro)
- **Ámbitos:** Financiación de capital riesgo por fase, región y sector; IA; unicornios; salidas
- **Motivo de inclusión y uso:** Una de las tres lecturas trimestrales de referencia del capital riesgo (con PitchBook-NVCA, RF-0079, y KPMG Venture Pulse, MBF-0715); útil para triangular cifras.
- **Uso en el bloque:** AG-B10 Flujos y Sentimiento (concentración del capital riesgo en IA); AG-B06 Tecnología; AG-B13 Prospectiva (listas de startups destacadas por sector).
- **Restricciones de uso:** Registro gratuito para descargar; copyright.
- **Sesgos y cautelas:** Método no detallado en las páginas vistas; cifras distintas de otras bases por definiciones de ronda; el informe no se leyó directamente.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-03 (búsqueda web: «CB Insights State of Venture report 2025»; WebFetch: sí, página de eventos de cbinsights.com, que no describe el informe)
- **Origen:** Alta F9 Bloque B, TFB-19 (2026-11-03).

#### RF-0079 · Q 67 (B) — PitchBook

- **Canal oficial (URL raíz):** https://pitchbook.com/ (informe público PitchBook-NVCA Venture Monitor: https://nvca.org/research/pitchbook-nvca-venture-monitor)
- **Emisor:** PitchBook (Morningstar); Venture Monitor en coautoría con la National Venture Capital Association (NVCA)
- **Temática:** TFB-19 Ecosistema emprendedor: startups, financiación, salidas a bolsa y escisiones (datos) (principal) · secundarias: TFB-11
- **Calidad Q:** 67 (B) — Primariedad 15/20 · Historial 10/20 · Transparencia 11/15 · Autoridad 13/15 · Independencia 7/10 · Actualidad 8/10 · Acceso 3/10
- **Tipología:** secundaria
- **Acceso:** Restringido (suscripción, de pago (futuro)); Venture Monitor trimestral con PDF y paquete de datos enlazados desde NVCA
- **Ámbitos:** Capital riesgo, operaciones, valoraciones, salidas y captación en EE. UU.
- **Motivo de inclusión y uso:** Base de datos de capital riesgo; usar sus informes públicos periódicos (Venture Monitor). AC-AL / AC-TEC: ciclo de financiación de startups.
- **Uso en el bloque:** AG-B10 Flujos y Sentimiento (ciclo trimestral del capital riesgo en EE. UU., salidas y captación de fondos); AG-B09 Finanzas y Valoración (valoraciones medianas por fase como referencia para comparables privados); AG-B12 (salidas recientes); cubre el informe NVCA pedido en el encargo.
- **Restricciones de uso:** Plataforma de pago (futuro); el Venture Monitor es de descarga gratuita desde NVCA.
- **Sesgos y cautelas:** Acceso restringido; la asociación del sector (NVCA) es coautora del informe público.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-02 (búsqueda web: «PitchBook NVCA Venture Monitor report»; WebFetch: sí, sobre la página de NVCA; la raíz pitchbook.com solo se confirmó en resultados)
- **Origen:** Semilla V3.0 (2026-11-01) confirmada por BFA en F9_S3 (2026-11-02). Reutilizada en F9 Bloque B, TFB-19 (2026-11-03).

#### MBF-0712 · Q 66 (B) — ENISA — préstamos participativos a startups y pymes (España): informes de actividad

- **Canal oficial (URL raíz):** https://emprendedores.es/ayudas/enisa-informe-prestamos-participativos-2023 (informe de actividad de ENISA difundido por Emprendedores; resumen de cierre de fondos del PRTR: https://ecosistemastartup.com/?p=107777)
- **Emisor:** Empresa Nacional de Innovación, S.A. (ENISA), Ministerio de Industria y Turismo
- **Documentación y notas:** ENISA concede préstamos participativos sin garantías personales a startups y pymes (líneas para jóvenes emprendedores, emprendedores y crecimiento) y publica informes anuales de actividad e impacto. Según el titular de ecosistemastartup.com, cerró los fondos del PRTR con 456 préstamos y 79,8 M€ para startups. La web oficial (enisa.es) no apareció en los resultados.
- **Temática:** TFB-19 Ecosistema emprendedor: startups, financiación, salidas a bolsa y escisiones (datos) (principal) · secundarias: TFB-16
- **Calidad Q:** 66 (B) — Primariedad 14/20 · Historial 10/20 · Transparencia 9/15 · Autoridad 13/15 · Independencia 7/10 · Actualidad 7/10 · Acceso 6/10
- **Tipología:** primaria en origen (datos del organismo), consultada a través de medios
- **Acceso:** Abierto
- **Ámbitos:** Número e importe de préstamos participativos por línea, sector y comunidad autónoma
- **Motivo de inclusión y uso:** Segunda gran vía pública de financiación de startups en España (deuda participativa); complementa al CDTI (MBF-0711).
- **Uso en el bloque:** AG-B04 Demanda y Adopción y AG-B08 Macro y Ciclo (dinamismo emprendedor en España); AG-B07 (política pública de apoyo).
- **Restricciones de uso:** Condiciones de los medios citados; usar el informe original de ENISA cuando se localice.
- **Sesgos y cautelas:** Fichas apoyadas en medios (una es contenido patrocinado); verificar en enisa.es antes de usar cifras; la segunda URL no cargó.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-03 (búsquedas web: «ENISA préstamos participativos startups CDTI NEOTEC empresas financiadas» y «enisa.es informe actividad préstamos participativos CDTI Neotec resolución startups datos»; WebFetch: no carga ecosistemastartup.com)
- **Origen:** Alta F9 Bloque B, TFB-19 (2026-11-03).

#### MBF-0719 · Q 64 (C) — SPACInsider — estadísticas de salidas a bolsa de SPAC y de fusiones (de-SPAC)

- **Canal oficial (URL raíz):** https://spacinsider.com/stats
- **Emisor:** SPACInsider
- **Documentación y notas:** Sección de estadísticas con tres bloques: IPO Stats (tendencias de emisión y volúmenes), DeSPAC Stats (rendimiento de las fusiones por sector y valoración) y Trackers and Returns (precio y rentabilidad sobre valor liquidativo); histórico actualizado a diario; enlace de suscripción a una página de precios. En 2026 anunció un acceso con IA a su base de SPAC.
- **Temática:** TFB-19 Ecosistema emprendedor: startups, financiación, salidas a bolsa y escisiones (datos) (principal) · secundarias: TFB-15
- **Calidad Q:** 64 (C) — Primariedad 13/20 · Historial 10/20 · Transparencia 7/15 · Autoridad 11/15 · Independencia 8/10 · Actualidad 10/10 · Acceso 5/10
- **Tipología:** secundaria (base especializada sobre registros de la SEC)
- **Acceso:** Muro parcial (la página no aclara qué es gratuito; suscripción de pago, futuro)
- **Ámbitos:** Número e importe de salidas a bolsa de SPAC, fusiones anunciadas y completadas, rentabilidad posterior
- **Motivo de inclusión y uso:** Fuente especializada en la vía SPAC de salida a bolsa, útil para medir episodios especulativos y la calidad de las empresas que cotizan por esta vía.
- **Uso en el bloque:** AG-B10 Flujos y Sentimiento (auge de SPAC como señal de exceso especulativo); AG-B14 Contrarias (bajo rendimiento posterior de los de-SPAC); AG-B12 (filtro de nuevas cotizadas por vía de salida).
- **Restricciones de uso:** Condiciones del sitio; datos completos de pago.
- **Sesgos y cautelas:** Método no descrito en la página; cobertura de redenciones y liquidaciones no confirmada.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-03 (búsqueda web: «SPACInsider SPAC Research SPAC data IPO trust deSPAC statistics»; WebFetch: sí)
- **Origen:** Alta F9 Bloque B, TFB-19 (2026-11-03).

#### MBF-0721 · Q 60 (C) — Product Hunt — plataforma de lanzamientos de productos (señales de tracción temprana)

- **Canal oficial (URL raíz):** https://www.producthunt.com/ (ejemplo de ficha de producto: https://www.producthunt.com/products/yc-company-explorer)
- **Emisor:** Product Hunt
- **Documentación y notas:** Plataforma donde los creadores lanzan productos y los usuarios los reseñan, debaten y votan, con clasificaciones diarias y semanales; cada producto conserva su historial de lanzamientos y posiciones (p. ej., n.º 1 del día y n.º 2 de la semana).
- **Temática:** TFB-19 Ecosistema emprendedor: startups, financiación, salidas a bolsa y escisiones (datos) (principal) · secundarias: TFB-15
- **Calidad Q:** 60 (C) — Primariedad 13/20 · Historial 10/20 · Transparencia 6/15 · Autoridad 8/15 · Independencia 6/10 · Actualidad 10/10 · Acceso 7/10
- **Tipología:** primaria (datos de plataforma)
- **Acceso:** Abierto (lectura); votar o comentar exige cuenta gratuita
- **Ámbitos:** Lanzamientos de software, IA y productos de consumo; votos, reseñas, creadores
- **Motivo de inclusión y uso:** Indicador cualitativo de qué productos de software despiertan interés temprano entre usuarios técnicos; útil para detectar nuevos entrantes en una categoría.
- **Uso en el bloque:** AG-B04 Demanda y Adopción (interés temprano por categorías de producto); AG-B03 (nuevos entrantes frente a cotizadas de software); AG-B06 Tecnología.
- **Restricciones de uso:** Condiciones de uso de la plataforma; la extracción automatizada puede estar limitada.
- **Sesgos y cautelas:** Votos manipulables y sesgo hacia productos para desarrolladores y fundadores; popularidad no equivale a ingresos.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-03 (búsqueda web: «Y Combinator startup directory companies Techstars portfolio Product Hunt launches»; WebFetch: sí)
- **Origen:** Alta F9 Bloque B, TFB-19 (2026-11-03).

#### MBF-0720 · Q 58 (C) — Boardroom Alpha — SPAC Research & Database

- **Canal oficial (URL raíz):** https://www.boardroomalpha.com/SPAC
- **Emisor:** Boardroom Alpha
- **Documentación y notas:** Base y noticias sobre SPAC (salidas a bolsa, fusiones, consejeros y patrocinadores), con un archivo paginado de entradas de investigación. Alternativa a SPACInsider (MBF-0719) y a SPAC Research (de pago).
- **Temática:** TFB-19 Ecosistema emprendedor: startups, financiación, salidas a bolsa y escisiones (datos) (principal)
- **Calidad Q:** 58 (C) — Primariedad 11/20 · Historial 10/20 · Transparencia 6/15 · Autoridad 10/15 · Independencia 8/10 · Actualidad 8/10 · Acceso 5/10
- **Tipología:** secundaria
- **Acceso:** Muro parcial (no comprobado)
- **Ámbitos:** SPAC: calendario, fusiones, patrocinadores y gobierno corporativo
- **Motivo de inclusión y uso:** Contraste de datos de SPAC; aporta el ángulo de gobierno corporativo (consejeros y patrocinadores).
- **Uso en el bloque:** AG-B10 y AG-B14 (episodios especulativos); AG-B12 (calidad de patrocinadores en de-SPAC candidatos).
- **Restricciones de uso:** Condiciones del sitio, no leídas.
- **Sesgos y cautelas:** Solo confirmada en resultados de búsqueda; método y cobertura desconocidos.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** VERIFICADO_BUSQUEDA
- **Última verificación:** 2026-11-03 (búsqueda web: «SPACInsider SPAC Research SPAC data IPO trust deSPAC statistics»; WebFetch: no)
- **Origen:** Alta F9 Bloque B, TFB-19 (2026-11-03).

#### MBF-0722 · Q 56 (C) — ExploreYC — capa de datos abierta sobre el directorio de startups de Y Combinator (y a16z)

- **Canal oficial (URL raíz):** https://www.producthunt.com/products/yc-company-explorer (ficha del proyecto en Product Hunt; alternativas: https://aiindigo.com/tools/alternatives/exploreyc)
- **Emisor:** Konstantin Borimechkov (proyecto de código abierto)
- **Documentación y notas:** Búsqueda, mapas, inteligencia por empresa, contratación, financiación y analítica por promoción sobre más de 5.773 empresas de Y Combinator; lanzamientos el 07/05/2026 y el 08/07/2026 («Open-source API for Y Combinator & a16z company data», n.º 1 del día). Se apoya en el directorio público de YC.
- **Temática:** TFB-19 Ecosistema emprendedor: startups, financiación, salidas a bolsa y escisiones (datos) (principal)
- **Calidad Q:** 56 (C) — Primariedad 9/20 · Historial 10/20 · Transparencia 8/15 · Autoridad 7/15 · Independencia 7/10 · Actualidad 9/10 · Acceso 6/10
- **Tipología:** secundaria (reelaboración de datos públicos de aceleradoras)
- **Acceso:** Abierto (código abierto y API)
- **Ámbitos:** Empresas de Y Combinator por promoción, sector, ubicación, estado y contratación; datos de cartera de a16z
- **Motivo de inclusión y uso:** Acceso programático gratuito al universo de startups de la aceleradora más influyente; útil para medir el peso de temáticas (IA, defensa, biotecnología) en cada promoción.
- **Uso en el bloque:** AG-B13 Prospectiva y AG-B06 Tecnología (temáticas que capta la financiación semilla); AG-B03 (nuevos entrantes).
- **Restricciones de uso:** Licencia del repositorio (no comprobada); respetar condiciones de YC sobre sus datos.
- **Sesgos y cautelas:** Proyecto individual sin garantía de continuidad; el directorio oficial de YC (no confirmado en resultados) es la fuente primaria.
- **Historial de exactitud:** Sin uso observado: puntuación neutra 10/20 hasta que el Evaluador la mida.
- **Cambios de propiedad o de metodología:** Sin cambios conocidos.
- **Estado:** Aprobada
- **Estado del enlace:** OK
- **Última verificación:** 2026-11-03 (búsqueda web: «Y Combinator startup directory companies Techstars portfolio Product Hunt launches»; WebFetch: sí)
- **Origen:** Alta F9 Bloque B, TFB-19 (2026-11-03).

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
| V2.0 | 02/11/2026 | Primera carga de fichas del Bloque B V2.0: 443 fichas (reutilizadas de los Bloques A con su ID original, y nuevas verificadas por búsqueda web con prefijo MB); 0 bajas; orden por temática y Q; índice con recuento de verificadas. |

