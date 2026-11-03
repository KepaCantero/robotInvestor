# Registro de Fuentes Fiables para el Analizador de Mercados

VERSIÓN V1.2 · Archivo operativo del Bloque B de la arquitectura Robot Investor · Catálogo de fuentes de mercado, datos y actualidad verificadas para el análisis profundo de mercados y activos concretos · Propietario de escritura y mantenimiento: Documentador para el Analizador de Mercados · Lectura: Analizador de Mercados y Buscador de fuentes avanzadas para el Analizador de Mercados · Nace sembrado desde el «Registro de Fuentes Fiables para el Analizador de Tendencias» del Bloque A con un subconjunto curado y nota de trazabilidad (decisión D5 del Anexo J del Documento 0 del Bloque B) · Gobernanza: «Documento 0 --- Protocolo maestro del Bloque B» (óptima V1.2, 31/10/2026); régimen operativo: system prompt del Documentador para el Analizador de Mercados (óptima V1.2) · Esquema ampliado por la «Adenda de arquitectura --- Bloque B» (V1.0, 30/10/2026): bloque de procedencia y calidad de la evidencia por ficha (D14) y fiabilidad por ámbito en el mantenimiento mensual · Esquema ampliado por la «Adenda de arquitectura --- Bloque B: Asimilación de la propuesta de mejoras y evolución arquitectónica» (V1.0, 31/10/2026): bloque de procedencia, contexto y calidad con ocho campos (añade metodología de la fuente, alcance geográfico y sectorial y accesibilidad y estabilidad; D28) · es-ES

## 1. Rol del archivo en la arquitectura del Bloque B

Este archivo es el catálogo de fuentes del Bloque B: la memoria de qué fuentes de mercado, datos y actualidad existen verificadas para el análisis profundo, en qué estado están y qué historia de uso tienen. El Analizador de Mercados lo consulta antes de pedir búsquedas (aporte marginal: no se pide lo ya cubierto); el Buscador avanzado de Mercados lo consulta para no duplicar y para conocer niveles y estados; el Documentador de Mercados lo registra y mantiene. Su criterio de calidad es el de todo archivo del bloque: que un tercero pueda confiar en lo que dice sin rehacerlo. No es un archivo del Bloque A: es el Registro de Mercados propio del bloque, nacido por siembra curada (D5) y con vida propia desde su creación.

La diferencia con el Registro del Bloque A es de servicio, no de naturaleza: aquel alimenta el ciclo semanal de tendencias (amplitud, descubrimiento); este alimenta ciclos on-demand de análisis profundo (precisión, corroboración, antigüedad declarada). De ahí que la siembra excluya las fuentes de descubrimiento comercial de nivel C del Bloque A: en el análisis profundo, los datos entran por fuentes primarias o se declaran como laguna.

## 2. Ficha de uso para los agentes

**Analizador de Mercados (lectura).** Antes de cada petición al Buscador (CT-B-03) consulta este archivo: lo que una fuente vigente de calidad no inferior ya cubre, no se pide. Las fuentes en estado «en revisión» o «retirada» no sostienen [HECHO] críticos; las «heredada, pendiente de re-verificación en primer uso» se re-verifican en su primer uso antes de sostener nada (regla crítica 6 del Analizador: herencia no es evidencia).

**Buscador avanzado de Mercados (lectura).** Consulta el archivo en cada comprobación previa de petición (4.2 de su prompt): si lo pedido está cubierto, devuelve la petición con la referencia; las fuentes nuevas que entregue entran al archivo por remisión al Documentador, nunca por escritura propia.

**Documentador de Mercados (escritura y mantenimiento).** Alta con aporte marginal declarado, estados del ciclo de vida V1.2, revisión post-solicitud en 48 horas naturales desde la entrega autorizada y revisión mensual ligera en la primera semana natural del mes (decisión D6). Toda escritura se confirma con identificador y fecha; el historial es append-only; la retirada es siempre lógica.

**Auditor de Mercados (sin acceso directo).** No accede al archivo: sus referencias son las de los extractos que el Orquestador remite por el CT-B-07.

## 3. Convenciones de formato

1. **Identificadores únicos e inmutables** con prefijo `RF-B-` y cuatro dígitos (RF-B-0001, RF-B-0002…) para cada fuente registrada. La numeración arranca en la siembra y es del bloque; los identificadores de origen del Bloque A (RF-xxxx) se citan solo en la nota de trazabilidad, nunca como identificador local.
2. **Fechado ISO 8601** en todos los campos de fecha: fecha de verificación, fecha de alta, fecha de último estado.
3. **Registro de solo añadir**: los cambios de estado, nivel o ámbito son entradas nuevas con fecha y motivo en el historial (5.5); nunca se borran ni se renumeran identificadores.
4. **Nivel de fiabilidad A/B/C** con el criterio compartido del ecosistema: A, fuentes primarias u oficiales y revistas académicas de referencia; B, fuentes académicas o institucionales intermedias que exigen contraste adicional antes de citar afirmaciones sensibles; C, agregadores comerciales y secundarios, útiles como contexto y nunca como base de premisas falsables. En este registro, el nivel C se admite con excepción documentada (Anexo E del prompt del Documentador, criterios de curación).
5. **Estados del ciclo de vida (estándar V1.2)**: vigente · en revisión · retirada · pendiente de acceso · heredada, pendiente de re-verificación en primer uso. El cambio de estado es siempre una entrada nueva con fecha y motivo; la retirada es lógica (la ficha permanece como evidencia, deja de alimentar el índice y las respuestas).
6. **Nota de trazabilidad de siembra**: toda entrada nacida de la D5 lleva, de forma permanente, la nota «sembrado desde el Bloque A» con su identificador de origen y la fecha de la siembra. El origen debe poder demostrarse siempre.
7. **Formato compacto de ficha**: un bloque de párrafos por entrada con los campos etiquetados en negrita, agrupados por temas (identificación y estado · ámbito y motivo · historial y riesgos · canal oficial), en la misma convención de formato compacto que el Registro del Bloque A desde el 26/10/2026.
8. **Campo no disponible se declara**: «desconocido», «no aplicable» o «sin uso en el bloque aún», nunca inventado; ante la duda, no se registra.
9. **Esquema 1.0 del ecosistema**: el conjunto de campos es el del esquema compartido; este archivo solo fija la disposición y los estados propios del bloque.

## 4. Estructura del archivo

El archivo se compone de seis secciones, en este orden: 4.1 índice operativo; 4.2 entradas del Registro (sección principal); 4.3 registro de mantenimiento; 4.4 registro de servicios; 4.5 historial de altas y cambios de estado; 4.6 acta de siembra (entrada de nacimiento). La siembra rellena 4.1, 4.2, 4.5 y 4.6; los registros de mantenimiento y de servicios se abren con la primera operación del Documentador de Mercados.

### 4.1 Índice operativo del Registro

| Campo | Valor |
|---|---|
| Versión del esquema | 1.2 (adenda de arquitectura, 31/10/2026: bloque de procedencia, contexto y calidad con ocho campos por ficha; D14, D28. Antecedente 1.1: procedencia y calidad, 30/10/2026) |
| Entradas registradas | 12 (todas sembradas desde el Bloque A, 28/10/2026) |
| Entradas por nivel | Nivel A (8): RF-B-0001 a RF-B-0008 · Nivel B (4): RF-B-0009 a RF-B-0012 |
| Entradas por estado | Heredada, pendiente de re-verificación en primer uso (12) |
| Entradas por acceso | Acceso gratuito íntegro (11) · Acceso variable por pieza (1: RF-B-0008) |
| Mapa de coberturas por ámbito | Datos macro y precios (buena: FRED, Banco Mundial, OCDE, FMI, BCE) · Filings y regulatorio (buena: SEC EDGAR) · Banca central y crédito (buena: BIS, BCE) · Investigación académica (buena: NBER, SSRN, arXiv q-fin, RePEc, FAJ) · Valoración y análisis de calidad (parcial: FAJ) |
| Coberturas ausentes declaradas | Sin fuente aún de prensa financiera de referencia (nivel B) para actualidad y corroboración de eventos corporativos; sin fuente especializada en materias primas y futuros como clase de activo; sin fuentes de consenso de estimaciones (los tipos estructurales del AM-8 las requerirán: alta prevista por demanda del ciclo) |
| Última revisión del índice | 2026-10-28 (siembra D5) |
| Carencias y prioridades | Alta futura de prensa financiera de referencia (nivel B) y de una fuente de consenso de estimaciones conforme a la escalera de acceso gratuito; revalidar en el primer mantenimiento la entrada de acceso variable por pieza (RF-B-0008) |

### 4.2 Entradas del Registro (sección principal)

Una entrada por fuente estable. Las doce entradas de esta sección son sembradas desde el Bloque A (decisión D5) el 28/10/2026: en cada ficha se indican solo los valores que difieren del patrón común de siembra. Patrón común: Estado «heredada, pendiente de re-verificación en primer uso»; Origen «sembrado desde el Bloque A (siembra D5, 28/10/2026)» con su identificador de origen; Nivel de verificación «heredada (verificación completa en origen el 25/10/2026; re-verificación propia pendiente del primer uso)»; Fecha de incorporación «2026-10-28»; Historial de correcciones «sin correcciones registradas (alta por siembra)»; Fiabilidad histórica «sin uso observado aún en el bloque». La re-verificación en primer uso (5.3 del prompt del Documentador) promueve la ficha a «vigente» con su fecha.

**Bloque de procedencia, contexto y calidad (V1.1-V1.2; D14, D28).** Toda ficha nueva añade a su estructura ocho campos: **titularidad_e_intereses** (naturaleza del editor --- regulador, emisor, proveedor comercial, asociación --- y su interés declarado); **ámbito_de_competencia** (qué clases de afirmaciones puede respaldar legítimamente, en el lenguaje de las dimensiones y los tipos de búsqueda); **frecuencia_y_revisiones** (cadencia de publicación, cambios de metodología y series revisadas conocidos); **limitaciones_conocidas** (sesgos, cobertura insuficiente, discontinuidades); **fuente_de_origen** (la dependencia primaria cuando la entrada es republicación: cinco artículos que reproducen un comunicado son una corroboración, no cinco); y, desde la V1.2 (D28), **metodología_de_la_fuente** (cómo produce sus datos o conclusiones: encuesta, registro administrativo, modelo, agregación; su ausencia se declara, nunca se supone); **alcance_geográfico_y_sectorial** (qué cubre y qué no: un índice de precios de un país no es el de su unión monetaria) y **accesibilidad_y_estabilidad** (régimen de acceso, escalera aplicable, estabilidad de la referencia y riesgo de discontinuidad). Una fuente reputada no recibe puntuación alta para cualquier tipo de afirmación: el ámbito de competencia delimita para qué sirve. Las doce fichas sembradas completan estos campos por entrada nueva en su re-verificación en primer uso; la fiabilidad por ámbito se consolida en el mantenimiento mensual a partir de la historia de uso.

#### RF-B-0001 — FRED (Federal Reserve Economic Data, Banco de la Reserva Federal de San Luis)

*Identificación y estado.* **source_id:** RF-B-0001 · **Nota de trazabilidad:** sembrado desde el Bloque A (RF-0001) · **Nivel:** A · los demás campos: patrón común de siembra.

*Ámbito y motivo.* **Motivo de inclusión en el bloque:** portal de datos oficiales de referencia para series macroeconómicas y financieras de Estados Unidos, con metadatos de fuente y metodología por serie; sostiene las dimensiones 1-3 y 6 de la espina dorsal en el universo estadounidense · **Ámbitos de especialización:** Macroeconomía; precios e inflación; tipos de interés; mercado laboral; indicadores de recesión; renta variable a nivel agregado · **Restricciones de uso:** citar la serie concreta y la fuente original que FRED declara en sus metadatos.

*Historial y riesgos.* **Fiabilidad histórica:** sin uso en el bloque aún · **Sesgos posibles:** cobertura hacia series estadounidenses · **Cambios de propiedad o metodología:** sin cambios conocidos en origen; verificar en cada mantenimiento.

*Canal oficial.* **Acceso:** fred.stlouisfed.org · **Documentación:** fred.stlouisfed.org/docs/api/fred/ · cada serie declara su fuente original en sus metadatos.

#### RF-B-0002 — SEC EDGAR (U.S. Securities and Exchange Commission)

*Identificación y estado.* **source_id:** RF-B-0002 · **Nota de trazabilidad:** sembrado desde el Bloque A (RF-0002) · **Nivel:** A · los demás campos: patrón común de siembra.

*Ámbito y motivo.* **Motivo de inclusión:** repositorio primario de documentos regulatorios de emisores estadounidenses (10-K, 10-Q, 8-K, 13F); fuente de máxima autoridad para hechos corporativos y para el despliegue estructural (4a-4b) de objetos estadounidenses · **Ámbitos:** Filings y documentos regulatorios; hechos corporativos; participaciones institucionales · **Restricciones:** citar formulario, fecha de presentación y CIK del emisor.

*Historial y riesgos.* **Fiabilidad histórica:** sin uso en el bloque aún · **Sesgos posibles:** los emisores redactan sus propias declaraciones (matiz, no sesgo editorial) · **Cambios:** dependencia del servicio público EDGAR.

*Canal oficial.* **Acceso:** sec.gov/edgar · **Búsqueda:** sec.gov/edgar/search/ · **Documentación:** sec.gov/edgar/sec-api-documentation.

#### RF-B-0003 — BIS (Bank for International Settlements), sección de estadísticas

*Identificación y estado.* **source_id:** RF-B-0003 · **Nota de trazabilidad:** sembrado desde el Bloque A (RF-0003) · **Nivel:** A · los demás campos: patrón común de siembra.

*Ámbito y motivo.* **Motivo de inclusión:** estadísticas internacionales de banca central (crédito, tipos efectivos, derivados OTC, deuda global); sostiene las dimensiones 3, 6 y 11 · **Ámbitos:** Crédito global; banca central; deuda; derivados OTC; divisas · **Restricciones:** citar la base estadística concreta y la fecha de extracción.

*Historial y riesgos.* **Fiabilidad histórica:** sin uso en el bloque aún · **Sesgos posibles:** cobertura centrada en bancos centrales miembros · **Cambios:** el BIS revisa metodologías periódicamente (vigilar notas de las series).

*Canal oficial.* **Acceso:** bis.org/statistics/ · **Portal de datos:** data.bis.org.

#### RF-B-0004 — BCE Data Portal (Banco Central Europeo)

*Identificación y estado.* **source_id:** RF-B-0004 · **Nota de trazabilidad:** sembrado desde el Bloque A (RF-0004) · **Nivel:** A · los demás campos: patrón común de siembra.

*Ámbito y motivo.* **Motivo de inclusión:** fuente oficial de datos de la eurozona (tipos, agregados monetarios, inflación HICP, balanza de pagos) con API pública; sostiene las dimensiones 1-3, 6 y 11 en el universo euro · **Ámbitos:** Eurozona; tipos de cambio; política monetaria; inflación HICP; agregados monetarios · **Restricciones:** citar la serie con su clave SDMX y la fecha de consulta.

*Historial y riesgos.* **Fiabilidad histórica:** sin uso en el bloque aún · **Sesgos posibles:** cobertura eurozona · **Cambios:** portal nuevo (sucesor del SDW clásico); vigilar reorganizaciones de series.

*Canal oficial.* **Acceso:** data.ecb.europa.eu · descargas y metadatos SDMX desde el propio portal.

#### RF-B-0005 — World Bank Open Data (Banco Mundial)

*Identificación y estado.* **source_id:** RF-B-0005 · **Nota de trazabilidad:** sembrado desde el Bloque A (RF-0005) · **Nivel:** A · los demás campos: patrón común de siembra.

*Ámbito y motivo.* **Motivo de inclusión:** indicadores macro globales comparables con metodología documentada y API; sostiene la dimensión 11 (macro-país y mercados emergentes) y el encaje geográfico de la máquina de proyecciones (TAM-SAM-SOM por geografía) · **Ámbitos:** Macroeconomía global; desarrollo; indicadores por país · **Restricciones:** CC BY 4.0 en general; citar indicador (código), país y año.

*Historial y riesgos.* **Fiabilidad histórica:** sin uso en el bloque aún · **Sesgos posibles:** revisión retrospectiva de datos nacionales; desfase de publicación en varios indicadores · **Cambios:** las series se revisan con las actualizaciones anuales del World Development Indicators.

*Canal oficial.* **Acceso:** data.worldbank.org · **Documentación:** datahelpdesk.worldbank.org.

#### RF-B-0006 — OECD Data (Organización para la Cooperación y el Desarrollo Económicos)

*Identificación y estado.* **source_id:** RF-B-0006 · **Nota de trazabilidad:** sembrado desde el Bloque A (RF-0006) · **Nivel:** A · los demás campos: patrón común de siembra.

*Ámbito y motivo.* **Motivo de inclusión:** indicadores comparables de países OCDE con notas metodológicas editoriales; sostiene las dimensiones 3 y 11 y el encaje geográfico de las proyecciones · **Ámbitos:** Países OCDE; empleo; comercio; industria; política económica comparada · **Restricciones:** citar indicador y país; condiciones del portal.

*Historial y riesgos.* **Fiabilidad histórica:** sin uso en el bloque aún · **Sesgos posibles:** cobertura OCDE · **Cambios:** migración de portal (data.oecd.org → oecd.org): revalidar URLs en el primer mantenimiento.

*Canal oficial.* **Acceso:** data-explorer.oecd.org (portal vigente) · documentación y límites de descarga en el propio portal.

#### RF-B-0007 — IMF Data (Fondo Monetario Internacional)

*Identificación y estado.* **source_id:** RF-B-0007 · **Nota de trazabilidad:** sembrado desde el Bloque A (RF-0007) · **Nivel:** A · los demás campos: patrón común de siembra.

*Ámbito y motivo.* **Motivo de inclusión:** bases de datos oficiales del FMI (Perspectivas de la Economía Mundial, estadísticas financieras internacionales); sostiene las dimensiones 3 y 11 y los escenarios macro de la F4 · **Ámbitos:** Macroeconomía global; balanza de pagos; reservas; estabilidad financiera · **Restricciones:** citar base, serie y edición (las proyecciones cambian por edición; son estimaciones del FMI, no hechos).

*Historial y riesgos.* **Fiabilidad histórica:** sin uso en el bloque aún · **Sesgos posibles:** las proyecciones WEO son previsión, no hecho · **Cambios:** ediciones WEO semestrales; anotar siempre la edición usada.

*Canal oficial.* **Acceso:** data.imf.org · **Nota de verificación heredada:** el punto de acceso SDMX histórico (dataservices.imf.org) quedó retirado en 2025; el acceso vigente es el propio portal; revalidar en el primer mantenimiento.

#### RF-B-0008 — Financial Analysts Journal (CFA Institute / Taylor & Francis)

*Identificación y estado.* **source_id:** RF-B-0008 · **Nota de trazabilidad:** sembrado desde el Bloque A (RF-0012) · **Nivel:** A · **Acceso:** variable por pieza · los demás campos: patrón común de siembra.

*Ámbito y motivo.* **Motivo de inclusión:** revista de referencia de investigación en inversión y valoración; sostiene la dimensión 2 (valoración) y la metodología de la máquina de proyecciones con literatura revisada por pares · **Ámbitos:** Valoración; gestión de carteras; mercados de capital; metodología de análisis · **Restricciones:** acceso variable por pieza; verificar cada artículo en el primer uso; citar artículo, volumen y DOI.

*Historial y riesgos.* **Fiabilidad histórica:** sin uso en el bloque aún · **Sesgos posibles:** ninguno editorial conocido · **Cambios:** institución editora estable (CFA Institute).

*Canal oficial.* **Acceso:** tandfonline.com (página de la revista en Taylor & Francis) · **Institución editora:** cfainstitute.org · verificar el acceso de cada pieza en el primer uso.

#### RF-B-0009 — NBER Working Papers (National Bureau of Economic Research)

*Identificación y estado.* **source_id:** RF-B-0009 · **Nota de trazabilidad:** sembrado desde el Bloque A (RF-0008) · **Nivel:** B · los demás campos: patrón común de siembra.

*Ámbito y motivo.* **Motivo de inclusión:** documentos de trabajo de investigación económica de primer nivel; sostiene las dimensiones 3 y 10 (historia y analogías) y la literatura de metodología de valoración · **Ámbitos:** Investigación económica y financiera; literatura de frontera · **Restricciones:** muchos WP gratuitos y otros con coste; verificar pieza a pieza; un WP no está revisado por pares: citarlo como documento de trabajo.

*Historial y riesgos.* **Fiabilidad histórica:** sin uso en el bloque aún · **Sesgos posibles:** contenido no revisado por pares al publicarse; verificar si existe versión publicada posterior · **Cambios:** sin cambios conocidos.

*Canal oficial.* **Acceso:** nber.org/papers · páginas propias por número (nber.org/papers/wNNNNN); citar número de WP y año.

#### RF-B-0010 — SSRN (Social Science Research Network)

*Identificación y estado.* **source_id:** RF-B-0010 · **Nota de trazabilidad:** sembrado desde el Bloque A (RF-0009) · **Nivel:** B · los demás campos: patrón común de siembra.

*Ámbito y motivo.* **Motivo de inclusión:** principal repositorio de preprints de finanzas y economía; sostiene la dimensión 2 y el conocimiento metodológico de la Documentación de Mercados · **Ámbitos:** Finanzas; economía; literatura de frontera; versiones de autor · **Restricciones:** descarga gratuita con registro; citar como preprint con su abstract_id y comprobar si existe versión publicada posterior.

*Historial y riesgos.* **Fiabilidad histórica:** sin uso en el bloque aún · **Sesgos posibles:** sin revisión por pares garantizada · **Cambios:** propiedad de Elsevier desde 2016; vigilar cambios de acceso.

*Canal oficial.* **Acceso:** ssrn.com · resúmenes y descargas gratuitas con registro.

#### RF-B-0011 — arXiv q-fin (Quantitative Finance)

*Identificación y estado.* **source_id:** RF-B-0011 · **Nota de trazabilidad:** sembrado desde el Bloque A (RF-0010) · **Nivel:** B · los demás campos: patrón común de siembra.

*Ámbito y motivo.* **Motivo de inclusión:** repositorio abierto de preprints de finanzas cuantitativas; sostiene los métodos cuantitativos de la máquina de proyecciones y los instrumentos de familias de derivados · **Ámbitos:** Finanzas cuantitativas; modelización; econofísica; métodos estadísticos · **Restricciones:** licencias abiertas por pieza; citar identificador arXiv y versión.

*Historial y riesgos.* **Fiabilidad histórica:** sin uso en el bloque aún · **Sesgos posibles:** sin revisión por pares (solo moderación); calidad heterogénea · **Cambios:** sin cambios conocidos.

*Canal oficial.* **Acceso:** arxiv.org/list/q-fin/recent · **Documentación:** info.arxiv.org/help/api/.

#### RF-B-0012 — RePEc / IDEAS (Research Papers in Economics)

*Identificación y estado.* **source_id:** RF-B-0012 · **Nota de trazabilidad:** sembrado desde el Bloque A (RF-0011) · **Nivel:** B · los demás campos: patrón común de siembra.

*Ámbito y motivo.* **Motivo de inclusión:** agregador académico que localiza versiones de acceso gratuito (verdes) de artículos publicados en revistas de pago; soporte directo de la escalera de acceso gratuito del bloque para las búsquedas académicas · **Ámbitos:** Economía y finanzas; localización de versiones de trabajo y de acceso gratuito · **Restricciones:** es un agregador: citar la fuente primaria que enlaza, no IDEAS.

*Historial y riesgos.* **Fiabilidad histórica:** sin uso en el bloque aún · **Sesgos posibles:** ninguno editorial conocido (metadatos normalizados) · **Cambios:** sin cambios conocidos.

*Canal oficial.* **Acceso:** ideas.repec.org · **Espejo:** econpapers.repec.org · útil para metadatos normalizados de las entradas académicas (RF-B-0009 a RF-B-0011).

### 4.3 Registro de mantenimiento

Sección abierta con la primera operación de mantenimiento del Documentador de Mercados. Cada revisión (post-solicitud en 48 horas, mensual ligera) es una entrada con fecha, alcance y resultado.

*(Sin entradas aún: el archivo acaba de nacer por siembra.)*

### 4.4 Registro de servicios

Sección abierta con el primer servicio a los agentes lectores. Cada entrega relevante de fuentes a un ciclo se anota con su referencia (request_id, paquete del Buscador).

*(Sin entradas aún.)*

### 4.5 Historial de altas y cambios de estado

| Fecha | Entrada | Evento | Detalle |
|---|---|---|---|
| 2026-10-28 | RF-B-0001 a RF-B-0012 | Alta por siembra (D5) | Doce fuentes sembradas desde el Registro del Bloque A con nota de trazabilidad; estado inicial «heredada, pendiente de re-verificación en primer uso» en todas; acta en 4.6 |

### 4.6 Acta de siembra (entrada de nacimiento del archivo)

| Campo | Valor |
|---|---|
| Fecha de la siembra | 2026-10-28 |
| Decisión que la funda | D5 del Anexo J del Documento 0 del Bloque B («Registro de Fuentes Fiables del Bloque B sembrado desde el del Bloque A con subconjunto curado y nota de trazabilidad»), codificada como «criterio de diseño» reversible por el operador |
| Archivo de origen | «Registro de Fuentes Fiables para el Analizador de Tendencias» del Bloque A (V2.6, carga de arranque del 25/10/2026: 14 entradas) |
| Criterios aplicados | Los de la sección 6.2 del prompt del Documentador de Mercados: (a) nivel A o B como base de la selección; (b) temática aplicable al análisis profundo de las once familias del Analizador; (c) verificación al día en origen; (d) compatibilidad con el esquema compacto de este archivo. Sin copias en bloque: cada fuente decidida por su aporte al análisis profundo |
| Resultado | 14 fuentes evaluadas · 12 seleccionadas (8 de nivel A, 4 de nivel B) · 2 descartadas: RF-0013 Yahoo Finance y RF-0014 Investing.com (nivel C, agregadores comerciales de descubrimiento; en el análisis profundo los datos entran por fuentes primarias o se declaran como laguna: su exclusión es la mitad del criterio) |
| Estado inicial de las sembradas | «Heredada, pendiente de re-verificación en primer uso» en todas (5.3 del prompt del Documentador): la re-verificación en primer uso las promueve a «vigente» con fecha; ninguna sembrada sostiene un [HECHO] crítico antes de su re-verificación |
| Reversibilidad | La selección es reversible por el operador (como toda decisión «criterio de diseño» del Anexo J): cualquier fuente descartada puede incorporarse por alta ordinaria con su aporte marginal, y cualquier sembrada puede retirarse lógicamente con su motivo |

## 5. Qué se registra y qué no

Se registran fuentes estables de mercado, datos y actualidad verificables aplicables al análisis profundo: portales de datos, repositorios regulatorios, publicaciones académicas e institucionales, prensa financiera de referencia (cuando se dé de alta) y proveedores de datos con metodología declarada. No se registran: piezas sueltas (las piezas concretas se citan por su URL dentro de la fuente de su source_id, como en el Bloque A), fuentes personales o de opinión sin metodología, credenciales o canales de acceso restringido ilegal, ni fuentes cuyo único valor sea la promoción comercial. La duda se resuelve no registrando y documentando la razón en el historial de mantenimiento.

## 6. Reglas de mantenimiento y ciclo de vida

El mantenimiento es híbrido (decisión D6): revisión ligera post-solicitud dentro de las 48 horas naturales siguientes a cada entrega autorizada (altas y cambios del ciclo, índice al día) y revisión mensual ligera en la primera semana natural del mes (aporte marginal de las altas del periodo, retirada lógica de lo superado, duplicidades, mapas de cobertura, estados colgados). Las reglas completas están en las secciones 5 y 8 del prompt del Documentador de Mercados; este archivo nunca se borra ni se renumera, y toda corrección es una entrada nueva que referencia a la anterior. Las entradas «heredada, pendiente de re-verificación en primer uso» se promueven a «vigente» en el primer uso de cada ciclo; las que acumulen usos sin re-verificación se señalan en la revisión mensual. Desde la V1.1, la revisión mensual consolida además la fiabilidad de fuentes por ámbito a partir de la historia de uso (D14) y completa los campos de procedencia de las fichas sembradas conforme se re-verifican.

## 7. Control de versiones del archivo

| Versión | Fecha | Cambios |
|---|---|---|
| V1.0 | 2026-10-28 | Nacimiento del archivo por siembra D5: 12 entradas seleccionadas del Registro del Bloque A (8 de nivel A, 4 de nivel B), acta de siembra en 4.6, índice operativo y convenciones propias del bloque (formato compacto, estados V1.2, identificadores RF-B). Sin fichas de pieza registradas ni registros de mantenimiento y servicios: se abren con la primera operación |
| V1.1 | 2026-10-30 | Esquema ampliado por la adenda de arquitectura (antes de la primera alta propia): bloque «Procedencia y calidad» por ficha con cinco campos (D14), versión de esquema 1.1 en el índice operativo y fiabilidad por ámbito en el mantenimiento mensual. Las fichas sembradas completan los campos nuevos en su re-verificación en primer uso |
| V1.2 | 2026-10-31 | Esquema ampliado por la adenda de arquitectura V1.2 (antes de la primera alta propia): el bloque de procedencia y calidad pasa a «Procedencia, contexto y calidad» con ocho campos, añadiendo metodología_de_la_fuente, alcance_geográfico_y_sectorial y accesibilidad_y_estabilidad (D28); versión de esquema 1.2 en el índice operativo. Las fichas sembradas completan los campos nuevos en su re-verificación en primer uso |

## 8. Canales transversales de verificación

| Canal | Uso en este archivo |
|---|---|
| Wayback Machine (web.archive.org) | Capturas históricas para reparar enlaces rotos: corrección anotada con fecha y motivo en el historial |
| Políticas de uso de cada servicio | Revisar antes de cualquier acceso programático; los cambios relevantes se anotan como «cambios de propiedad o de metodología» |
| Crossref / OpenAlex | Para las entradas académicas (RF-B-0008 a RF-B-0012): comprobar citas normalizadas, versiones y metadatos antes de dar por buena una referencia |
| Registro del mercado correspondiente | Para la condición de cotización de un objeto o actor (AM-10): el alta de una fuente no sustituye la verificación puntual de cotización con fecha en el registro del mercado |
